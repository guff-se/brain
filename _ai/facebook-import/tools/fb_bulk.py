#!/usr/bin/env python3
"""Phase 1–5 bulk runner — resumable, idempotent, crash-safe.

Processes all posts from all_posts.jsonl:
  1. Fetch URLs (cached per sha)
  2. Judge content (cached per content-hash)
  3. Write routed notes to sources/ (skipped if file already exists)
  4. Log every decision to staging/run_log.jsonl (append-only)

RESUME: just re-run this script. Anything already cached or written is skipped.
STATUS: run with --status to see counts without processing anything.

Usage:
  python tools/fb_bulk.py              # run everything
  python tools/fb_bulk.py --status     # show progress counts
  python tools/fb_bulk.py --year 2016  # only process one year (for testing)
  python tools/fb_bulk.py --dry-run    # fetch+judge but don't write to sources/
"""
from __future__ import annotations
import argparse, json, os, re, sys, datetime, unicodedata, hashlib, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
VAULT = os.path.dirname(os.path.dirname(PROJECT))
STAGING = os.path.join(PROJECT, 'staging')
JSONL = os.path.join(STAGING, 'all_posts.jsonl')
RUN_LOG = os.path.join(STAGING, 'run_log.jsonl')

sys.path.insert(0, HERE)
from fb_fetch import fetch, classify_domain, domain_of  # noqa
from fb_judge import (  # noqa
    judge, TokenLimitError, is_token_limit_message, is_retriable_judge_error,
    load_cached_judgement, judgement_cache_path,
)

# Global stop flag — set when a token limit is detected. Workers check this
# before starting new items so we drain cleanly without killing mid-write.
_stop = threading.Event()

# ── Routing map ──────────────────────────────────────────────────────────────

REGISTER_PATH = {
    'voice':    os.path.join(VAULT, 'sources', 'mine', 'voice'),
    'thinking': os.path.join(VAULT, 'sources', 'mine', 'thinking'),
    'facts':    os.path.join(VAULT, 'sources', 'mine', 'facts'),
    'consumed': {
        'article': os.path.join(VAULT, 'sources', 'consumed', 'articles'),
        'video':   os.path.join(VAULT, 'sources', 'consumed', 'videos'),
        'podcast': os.path.join(VAULT, 'sources', 'consumed', 'podcasts'),
        'book':    os.path.join(VAULT, 'sources', 'consumed', 'books'),
        'clipping':os.path.join(VAULT, 'sources', 'consumed', 'clippings'),
    },
}

YEAR_BUNDLE_PATHS = {
    'thinking': os.path.join(VAULT, 'sources', 'mine', 'thinking', '{year}-fb-stream.md'),
    'consumed': os.path.join(VAULT, 'sources', 'consumed', 'clippings', '{year}-fb-shares.md'),
}

_log_lock = threading.Lock()

# Terminal run_log statuses — safe to skip fetch/judge on re-run (see load_run_resume).
TERMINAL_RESUME = frozenset({
    'written', 'already-written', 'skipped', 'skipped-empty', 'skipped-short',
    'skipped-domain', 'skipped-own-domain', 'bundle-facts', 'dry-run-save',
})

# Length gates (v2 — see PLAN.md §7.3, fb_reset_v1)
MIN_OWN_TEXT_CHARS = 200
MIN_OWN_TEXT_HARD_SKIP = 80
MIN_COMMENTARY_CHARS = 80
MIN_FETCH_BODY_CHARS = 100
_last_run_status: dict[tuple, str] = {}
_last_run_error: dict[tuple, str] = {}
_retry_errors = False


def load_run_resume() -> tuple[dict[tuple, str], dict[tuple, str]]:
    """Last status + error per (ts, src) from append-only run_log."""
    last: dict[tuple, str] = {}
    err: dict[tuple, str] = {}
    if not os.path.exists(RUN_LOG):
        return last, err
    with open(RUN_LOG, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = (e.get('ts'), e.get('row_src') or e.get('src'))
            st = e.get('status')
            if key[0] is not None and st:
                last[key] = st
                err[key] = e.get('error') or ''
    return last, err


def _should_resume_skip(ts, src: str) -> bool:
    """Skip fetch/judge on re-run when prior outcome does not need another attempt."""
    prior = _last_run_status.get((ts, src))
    if prior in TERMINAL_RESUME:
        return True
    if prior == 'judge-error':
        if is_retriable_judge_error(_last_run_error.get((ts, src), '')):
            return False  # limit/CLI failures — retry after reset
        return not _retry_errors  # e.g. no-json — skip unless forced
    if prior in ('fetch-error', 'error'):
        return False  # network / transient — always retry
    return False


def _row_work_priority(row: dict) -> int:
    """Lower = earlier in queue. pending-judge first, then retries, stuck errors last."""
    key = (row.get('ts'), row.get('src'))
    st = _last_run_status.get(key)
    if _should_resume_skip(key[0], key[1]):
        return 0
    if st == 'pending-judge':
        return 1
    if st == 'judge-error':
        return 2  # retriable limit errors
    return 2


def _sort_rows_for_work(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: (_row_work_priority(r), r.get('ts', 0)))


def dedupe_rows(rows: list[dict]) -> list[dict]:
    """One row per timestamp for main1/main2 — keep longer text, tie-break main2."""
    main: dict[int, dict] = {}
    other: list[dict] = []
    for r in rows:
        if r.get('src') not in ('main1', 'main2'):
            other.append(r)
            continue
        ts = r.get('ts')
        if ts not in main:
            main[ts] = r
            continue
        a, b = main[ts], r
        la, lb = len(a.get('text') or ''), len(b.get('text') or '')
        if lb > la or (lb == la and b.get('src') == 'main2'):
            main[ts] = b
    return other + list(main.values())


def _length_note(item_type: str, text: str, *, pairing: str | None = None) -> str | None:
    n = len(text or '')
    if item_type == 'own_text':
        if n < MIN_OWN_TEXT_HARD_SKIP:
            return f'{n} chars — under {MIN_OWN_TEXT_HARD_SKIP}; auto-skip tier'
        if n < MIN_OWN_TEXT_CHARS:
            return f'{n} chars — under {MIN_OWN_TEXT_CHARS}; strict own_text rules apply'
    if item_type == 'own_commentary':
        if pairing == 'standalone' and n < MIN_OWN_TEXT_CHARS:
            return f'{n} chars — article failed; standalone commentary needs ≥{MIN_OWN_TEXT_CHARS}'
        if pairing == 'paired' and n < MIN_COMMENTARY_CHARS:
            return f'{n} chars — paired commentary needs ≥{MIN_COMMENTARY_CHARS}'
    return None

# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str, max_words: int = 6) -> str:
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).lower()
    words = text.split()[:max_words]
    return '-'.join(words) or 'untitled'


def note_path(date: str, slug: str, register: str, kind: str) -> str:
    """Determine the vault path for a note."""
    fname = f'{date}-{slug}.md'
    if register in ('voice', 'thinking', 'facts'):
        return os.path.join(REGISTER_PATH[register], fname)
    else:  # consumed
        k = kind if kind in REGISTER_PATH['consumed'] else 'clipping'
        return os.path.join(REGISTER_PATH['consumed'][k], fname)


def detect_lang(text: str) -> str:
    if not text:
        return 'unknown'
    sv_chars = sum(1 for c in text if c in 'åäöÅÄÖ')
    ratio = sv_chars / max(len(text), 1)
    if ratio > 0.01:
        return 'sv'
    # heuristic: count common Swedish words
    sv_words = {'och', 'att', 'det', 'är', 'en', 'ett', 'jag', 'för', 'som', 'inte', 'vi', 'på', 'om'}
    words = set(text.lower().split())
    if len(sv_words & words) >= 2:
        return 'sv'
    return 'en'


def build_frontmatter(fields: dict) -> str:
    lines = ['---']
    for k, v in fields.items():
        if v is None:
            continue
        if isinstance(v, list):
            if v:
                lines.append(f'{k}: [{", ".join(str(x) for x in v)}]')
        elif isinstance(v, bool):
            lines.append(f'{k}: {"true" if v else "false"}')
        else:
            val = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{val}"')
    lines.append('---')
    return '\n'.join(lines)


def atomic_write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def append_log(entry: dict):
    with _log_lock:
        with open(RUN_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def primary_url(row: dict) -> dict | None:
    for u in row.get('urls', []):
        if u.get('url', '').startswith('http'):
            return u
    return None


# ── Note composers ───────────────────────────────────────────────────────────

def compose_own_note(row: dict, j: dict, fetch_res=None, *, link_title: str | None = None) -> str:
    """Compose a mine/voice or mine/thinking note from a Gustaf post."""
    text = row.get('text', '')
    date = row.get('date', '')
    lang = detect_lang(text)
    tags = j.get('tags_hint') or []
    u = primary_url(row)
    url_str = u['url'] if u else ''

    fm = build_frontmatter({
        'title': (text[:60].replace('"', "'") + ('…' if len(text) > 60 else '')),
        'summary': text[:120].replace('"', "'") + ('…' if len(text) > 120 else ''),
        'kind': 'note',
        'party': 'first',
        'register': j.get('register_hint', 'thinking'),
        'source': 'facebook',
        'source_id': f'fb-{row.get("ts","")}',
        'fb_url': url_str or None,
        'provenance': 'extracted',
        'lang': lang,
        'tags': tags,
        'status': 'reference',
        'ingested': datetime.date.today().isoformat(),
        'created': date,
    })
    body = text
    if link_title:
        body += f'\n\n→ [[{link_title.replace("]]", "")}]]'
    elif url_str:
        body += f'\n\n---\n*Shared link: {url_str}*'
    return fm + '\n\n' + body + '\n'


def _note_title_from_path(path: str) -> str | None:
    """Read title from frontmatter of a written note."""
    try:
        with open(path, encoding='utf-8') as f:
            head = f.read(2048)
    except OSError:
        return None
    m = re.search(r'^title:\s*"(.*)"', head, re.M)
    return m.group(1) if m else None


def _fetched_substantive(fr) -> bool:
    return bool(
        fr
        and fr.action in ('ok', 'wayback')
        and (fr.text_len or 0) >= MIN_FETCH_BODY_CHARS
    )


def _shared_item_type(fr) -> str:
    if fr.kind == 'video':
        return 'shared_video'
    if fr.kind == 'podcast':
        return 'shared_podcast'
    return 'shared_article'


def _run_judge(
    item_type: str, payload: dict, cache_only: bool, *, pairing: str | None = None,
) -> tuple[dict | None, str | None]:
    """Return (judgement_dict, error_status) or raise TokenLimitError."""
    payload = dict(payload)
    if pairing:
        payload['pairing_note'] = pairing
    ln = _length_note(item_type, payload.get('text', ''), pairing=pairing)
    if ln:
        payload['length_note'] = ln
    try:
        if cache_only:
            if not os.path.exists(judgement_cache_path(item_type, payload)):
                return None, 'pending-judge'
            j = load_cached_judgement(item_type, payload)
            if j is None:
                return None, 'pending-judge'
        else:
            j = judge(item_type, payload)
        if j.verdict == 'error':
            if is_token_limit_message(j.error or ''):
                raise TokenLimitError(j.error)
            return None, 'judge-error'
        return asdict(j), None
    except TokenLimitError:
        raise
    except RuntimeError as e:
        if is_token_limit_message(str(e)):
            raise TokenLimitError(str(e)) from e
        return None, 'judge-error'
    except Exception as e:
        if is_token_limit_message(str(e)):
            raise TokenLimitError(str(e)) from e
        return None, 'judge-error'


def _try_write(path: str, content: str, dry_run: bool) -> str:
    if os.path.exists(path):
        return 'already-written'
    if dry_run:
        return 'dry-run-save'
    atomic_write(path, content)
    return 'written'


def compose_consumed_note(row: dict, j: dict, fr) -> str:
    """Compose a consumed note from a fetched URL."""
    date = row.get('date', '')
    text = row.get('text', '')  # Gustaf's commentary
    title = fr.title or (primary_url(row) or {}).get('name', '') or fr.url
    author = fr.author or ''
    body_text = fr.text or ''
    lang = detect_lang(body_text or text)
    tags = j.get('tags_hint') or []
    kind = fr.kind or 'article'

    fm = build_frontmatter({
        'title': title[:120].replace('"', "'"),
        'summary': (body_text[:120] or title[:120]).replace('"', "'") + '…',
        'kind': kind,
        'party': 'third',
        'register': 'consumed',
        'source': 'web' if fr.action == 'ok' else ('wayback' if fr.action == 'wayback' else 'facebook'),
        'source_id': f'fb-{row.get("ts","")}',
        'url': fr.final_url or fr.url,
        'fb_url': None,
        'author': author or None,
        'provenance': 'extracted' if body_text else 'inferred',
        'enrichment': fr.action,
        'lang': lang,
        'tags': tags,
        'status': 'reference',
        'ingested': datetime.date.today().isoformat(),
        'created': date,
    })

    parts = [fm, '']
    if body_text:
        # Long-form split: keep first 800 words inline, rest is ref only
        words = body_text.split()
        if len(words) > 800:
            inline = ' '.join(words[:800])
            parts.append(inline)
            parts.append('\n*[Content truncated — full text in fetch cache]*')
        else:
            parts.append(body_text)
    else:
        parts.append(f'*Full text unavailable ({fr.action}). Title: {title}*')

    if text:
        parts.append(f'\n---\n**Gustaf\'s commentary:** {text}')

    return '\n'.join(parts) + '\n'


def append_to_bundle(bundle_path: str, row: dict, j: dict, fr=None):
    """Append a dated bullet to a year-bundle file."""
    os.makedirs(os.path.dirname(bundle_path), exist_ok=True)
    date = row.get('date', 'n/a')
    text = (row.get('text', '') or '').replace('\n', ' ').strip()
    u = primary_url(row)
    url = u['url'] if u else ''
    tags = ', '.join(j.get('tags_hint') or [])

    parts = [f'- **{date}**']
    if text:
        parts.append(f' — {text[:200]}{"…" if len(text) > 200 else ""}')
    if url:
        parts.append(f' [{domain_of(url)}]({url})')
    if tags:
        parts.append(f' `{tags}`')
    bullet = ''.join(parts) + '\n'

    # Ensure header exists
    if not os.path.exists(bundle_path):
        year = row.get('year', '')
        header = f'---\ntitle: "{year} Facebook stream"\nkind: note\nparty: first\nregister: thinking\nsource: facebook\nprovenance: extracted\nstatus: reference\ningested: {datetime.date.today().isoformat()}\n---\n\n# {year} Facebook stream\n\nCompressed year-bundle of Facebook posts that passed the year-bundle threshold but not the individual-note durability bar.\n\n'
        with _log_lock:
            with open(bundle_path, 'a', encoding='utf-8') as f:
                if os.path.getsize(bundle_path) == 0:
                    f.write(header)
    with _log_lock:
        with open(bundle_path, 'a', encoding='utf-8') as f:
            f.write(bullet)


# ── Core item processor ──────────────────────────────────────────────────────

def _process_own_text(row: dict, payload: dict, dry_run: bool, cache_only: bool) -> dict:
    """Status-only posts (no external URL to fetch)."""
    ts, date, src = row.get('ts', 0), row.get('date', '2000-01-01'), row.get('src')
    text = (row.get('text') or '').strip()
    result = {'ts': ts, 'date': date, 'src': src, 'status': 'pending',
              'verdict': None, 'path': None, 'error': None}

    if len(text) < MIN_OWN_TEXT_HARD_SKIP:
        result['status'] = 'skipped-short'
        return result

    j_dict, err = _run_judge('own_text', payload, cache_only)
    if err:
        result['status'] = err
        return result
    result['verdict'] = j_dict['verdict']
    if j_dict['verdict'] == 'skip':
        result['status'] = 'skipped'
        return result

    register = j_dict.get('register_hint') or 'thinking'
    if register == 'consumed':
        register = 'thinking'
    slug = slugify(text)
    path = note_path(date, slug, register, 'note')
    result.update(path=path, register=register, kind='note')
    try:
        st = _try_write(path, compose_own_note(row, j_dict), dry_run)
        result['status'] = st
    except Exception as e:
        result['status'] = 'write-error'
        result['error'] = str(e)
    return result


def _process_url_share(
    row: dict, fr, base_payload: dict, dry_run: bool, cache_only: bool,
) -> dict:
    """Link shares: both-or-neither when commentary present; bare link = article only."""
    ts, date, src = row.get('ts', 0), row.get('date', '2000-01-01'), row.get('src')
    text = (row.get('text') or '').strip()
    result = {'ts': ts, 'date': date, 'src': src, 'status': 'pending',
              'verdict': None, 'path': None, 'error': None, 'paths': []}

    shared_type = _shared_item_type(fr)
    article_payload = {k: v for k, v in base_payload.items() if k != 'text'}
    if _fetched_substantive(fr):
        article_payload['fetched_text'] = fr.text
    elif fr.action == 'paywalled':
        article_payload['fetch_note'] = 'paywall — only title and commentary available; judge by those'

    article_ok = False
    j_art = None
    if _fetched_substantive(fr) or article_payload.get('fetch_note') or fr.title:
        j_art, err = _run_judge(shared_type, article_payload, cache_only)
        if err:
            result['status'] = err
            return result
        article_ok = bool(j_art and j_art['verdict'] == 'save')

    has_commentary = len(text) >= MIN_COMMENTARY_CHARS

    # Substantive commentary on a link: require both passes, or standalone thinking only.
    if has_commentary:
        if article_ok:
            j_comm, err = _run_judge(
                'own_commentary', {**base_payload, 'text': text}, cache_only,
                pairing='paired',
            )
            if err:
                result['status'] = err
                return result
            if not (j_comm and j_comm['verdict'] == 'save'):
                result['status'] = 'skipped'
                result['verdict'] = 'skip'
                return result
            return _write_paired_notes(
                row, j_art, j_comm, fr, base_payload, text, date, dry_run, result,
            )

        # Article failed — short reaction to unworthy link is noise.
        if len(text) < MIN_OWN_TEXT_CHARS:
            result['status'] = 'skipped-short'
            result['verdict'] = 'skip'
            return result

        j_comm, err = _run_judge(
            'own_commentary', {**base_payload, 'text': text}, cache_only,
            pairing='standalone',
        )
        if err:
            result['status'] = err
            return result
        if not (j_comm and j_comm['verdict'] == 'save'):
            result['status'] = 'skipped'
            result['verdict'] = 'skip'
            return result
        return _write_thinking_only(row, j_comm, text, date, dry_run, result)

    # Bare link (no commentary) — article only.
    if article_ok:
        return _write_consumed_only(row, j_art, fr, base_payload, date, dry_run, result)

    result['status'] = 'skipped'
    result['verdict'] = 'skip'
    return result


def _write_paired_notes(
    row, j_art, j_comm, fr, base_payload, text, date, dry_run, result,
) -> dict:
    kind = fr.kind or j_art.get('kind_hint') or 'article'
    consumed_path = note_path(
        date, slugify(fr.title or base_payload.get('title') or 'untitled'), 'consumed', kind,
    )
    register = j_comm.get('register_hint') or 'thinking'
    if register == 'consumed':
        register = 'thinking'
    think_path = note_path(date, slugify(text), register, 'note')
    try:
        cst = _try_write(consumed_path, compose_consumed_note(row, j_art, fr), dry_run)
        if cst not in ('written', 'dry-run-save', 'already-written'):
            result['status'] = 'skipped'
            result['verdict'] = 'skip'
            return result
        consumed_title = _note_title_from_path(consumed_path) or fr.title
        tst = _try_write(
            think_path,
            compose_own_note(row, j_comm, link_title=consumed_title),
            dry_run,
        )
        if tst not in ('written', 'dry-run-save', 'already-written'):
            result['status'] = 'skipped'
            result['verdict'] = 'skip'
            return result
        result['paths'] = [consumed_path, think_path]
        result['path'] = think_path
        result['register'] = register
        result['kind'] = kind
        result['verdict'] = 'save'
        result['status'] = 'written'
    except Exception as e:
        result['status'] = 'write-error'
        result['error'] = str(e)
    return result


def _write_consumed_only(row, j_art, fr, base_payload, date, dry_run, result) -> dict:
    kind = fr.kind or j_art.get('kind_hint') or 'article'
    consumed_path = note_path(
        date, slugify(fr.title or base_payload.get('title') or 'untitled'), 'consumed', kind,
    )
    try:
        st = _try_write(consumed_path, compose_consumed_note(row, j_art, fr), dry_run)
        if st in ('written', 'dry-run-save', 'already-written'):
            result['paths'] = [consumed_path]
            result['path'] = consumed_path
            result['register'] = 'consumed'
            result['kind'] = kind
            result['verdict'] = 'save'
            result['status'] = 'written'
        else:
            result['status'] = 'skipped'
            result['verdict'] = 'skip'
    except Exception as e:
        result['status'] = 'write-error'
        result['error'] = str(e)
    return result


def _write_thinking_only(row, j_comm, text, date, dry_run, result) -> dict:
    register = j_comm.get('register_hint') or 'thinking'
    if register == 'consumed':
        register = 'thinking'
    think_path = note_path(date, slugify(text), register, 'note')
    try:
        st = _try_write(think_path, compose_own_note(row, j_comm), dry_run)
        if st in ('written', 'dry-run-save', 'already-written'):
            result['paths'] = [think_path]
            result['path'] = think_path
            result['register'] = register
            result['kind'] = 'note'
            result['verdict'] = 'save'
            result['status'] = 'written'
        else:
            result['status'] = 'skipped'
            result['verdict'] = 'skip'
    except Exception as e:
        result['status'] = 'write-error'
        result['error'] = str(e)
    return result


def process_item(row: dict, dry_run: bool = False, cache_only: bool = False) -> dict:
    """Full pipeline for one row: fetch → judge → route → write (v2 dual-write)."""
    ts = row.get('ts', 0)
    date = row.get('date', '2000-01-01')
    text = (row.get('text') or '').strip()
    src = row.get('src')

    if _should_resume_skip(ts, src):
        prior = _last_run_status.get((ts, src))
        return {
            'ts': ts, 'date': date, 'src': src,
            'status': prior, 'verdict': None, 'path': None, 'error': None,
            'resumed': True,
        }

    if _stop.is_set():
        return {'ts': ts, 'date': date, 'src': src, 'status': 'stopped',
                'verdict': None, 'path': None, 'error': None}

    result = {'ts': ts, 'date': date, 'src': src, 'status': 'pending',
              'verdict': None, 'path': None, 'error': None}

    if src in ('check_ins', 'tagged_places', 'memories_media'):
        result['status'] = 'bundle-facts'
        return result

    u = primary_url(row)
    payload: dict = {'text': text, 'date': date}

    if u:
        url = u['url']
        cls = classify_domain(url)
        payload['url'] = url
        payload['domain'] = domain_of(url)
        if u.get('name'):
            payload['title'] = u['name']

        if cls['action'] == 'skip':
            if not text:
                result['status'] = 'skipped-domain'
                return result
            return _process_own_text(row, payload, dry_run, cache_only)

        if cls['action'] == 'own':
            if not text:
                result['status'] = 'skipped-own-domain'
                return result
            return _process_own_text(row, payload, dry_run, cache_only)

        try:
            fr = fetch(url, throttle=0.8)
            if fr.title and not payload.get('title'):
                payload['title'] = fr.title
            if fr.author:
                payload['author'] = fr.author
            if (fr.extra or {}).get('mp3_url'):
                payload['fetch_note'] = 'mp3 located'
            return _process_url_share(row, fr, payload, dry_run, cache_only)
        except Exception as e:
            result['status'] = 'fetch-error'
            result['error'] = str(e)
            return result

    if not text:
        result['status'] = 'skipped-empty'
        return result

    return _process_own_text(row, payload, dry_run, cache_only)


# ── Status command ────────────────────────────────────────────────────────────

def show_status():
    rows = []
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            rows = [json.loads(l) for l in f]
    print(f'Total rows in all_posts.jsonl: {len(rows)}')

    import glob
    judged = len(glob.glob(os.path.join(STAGING, 'judged', '*.json')))
    fetched = len(glob.glob(os.path.join(STAGING, 'fetched_meta', '*.json')))
    print(f'Judged (cached):  {judged}')
    print(f'Fetched (cached): {fetched}')

    last_st, last_err = load_run_resume()
    if last_st:
        from collections import Counter
        st = Counter(last_st.values())
        finished = sum(st.get(s, 0) for s in TERMINAL_RESUME)
        pending = st.get('pending-judge', 0)
        je = [(k, last_err.get(k, '')) for k, v in last_st.items() if v == 'judge-error']
        retry_je = sum(1 for _, e in je if is_retriable_judge_error(e))
        skip_je = len(je) - retry_je
        print(f'Run log (deduped): finished={finished} pending-judge={pending} '
              f'judge-error retry={retry_je} skip={skip_je}')

    written = 0
    for reg in ('mine/voice', 'mine/thinking', 'mine/facts',
                'consumed/articles', 'consumed/videos',
                'consumed/podcasts', 'consumed/books', 'consumed/clippings'):
        p = os.path.join(VAULT, 'sources', reg)
        if os.path.isdir(p):
            written += len([f for f in os.listdir(p) if f.endswith('.md')])
    print(f'Notes written:    {written}')

    if os.path.exists(RUN_LOG):
        log_entries = []
        with open(RUN_LOG) as f:
            for line in f:
                try: log_entries.append(json.loads(line))
                except: pass
        from collections import Counter
        statuses = Counter(e.get('status') for e in log_entries)
        print(f'\nRun log ({len(log_entries)} entries):')
        for s, c in sorted(statuses.items(), key=lambda x: -x[1]):
            print(f'  {s}: {c}')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='Fetch+judge but skip vault writes')
    ap.add_argument('--cache-only', action='store_true',
                    help='Only apply existing judged/ cache (no agent calls). Skips uncached rows.')
    ap.add_argument('--year', type=int, help='Only process this year')
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--limit', type=int, help='Cap total rows (for testing)')
    ap.add_argument('--retry-errors', action='store_true',
                    help='Also re-attempt non-retriable judge-errors (e.g. no-json). '
                         'Limit/CLI judge-errors retry automatically.')
    args = ap.parse_args()

    if args.status:
        show_status()
        return

    # Load rows
    rows = []
    with open(JSONL) as f:
        for line in f:
            rows.append(json.loads(line))

    before = len(rows)
    rows = dedupe_rows(rows)
    if len(rows) != before:
        print(f'Deduped main1/main2: {before} → {len(rows)} rows')

    if args.year:
        rows = [r for r in rows if r.get('year') == args.year]
        print(f'Filtered to year {args.year}: {len(rows)} rows')
    if args.limit:
        rows = rows[:args.limit]
        print(f'Capped to {args.limit} rows')

    global _last_run_status, _last_run_error, _retry_errors
    _retry_errors = args.retry_errors
    _last_run_status, _last_run_error = load_run_resume()
    resume_n = sum(1 for r in rows if _should_resume_skip(r.get('ts'), r.get('src')))
    retry_err_n = sum(
        1 for r in rows
        if _last_run_status.get((r.get('ts'), r.get('src'))) == 'judge-error'
        and not _should_resume_skip(r.get('ts'), r.get('src'))
    )
    rows = _sort_rows_for_work(rows)
    todo_n = len(rows) - resume_n

    print(f'Processing {len(rows)} rows with {args.workers} workers'
          + (' [DRY RUN]' if args.dry_run else '')
          + (' [CACHE ONLY]' if args.cache_only else '')
          + (' [RETRY ALL ERRORS]' if _retry_errors else '') + '...')
    if resume_n:
        print(f'  Resume: {resume_n} instant skip, ~{todo_n} need work'
              + (f' (incl. {retry_err_n} retriable judge-errors)' if retry_err_n else ''))

    _stop.clear()

    counts = {'written': 0, 'skipped': 0, 'already-written': 0,
              'error': 0, 'bundle': 0, 'dry-run-save': 0, 'pending-judge': 0,
              'resumed': 0, 'deferred': 0}

    token_limit_hit = False
    limit_detail = ''
    limit_logged = False
    processed = 0

    ex = ThreadPoolExecutor(max_workers=args.workers)
    futs = {ex.submit(process_item, r, args.dry_run, args.cache_only): r for r in rows}
    try:
        for fut in as_completed(futs):
            if token_limit_hit:
                break
            row = futs[fut]
            processed += 1
            try:
                res = fut.result()
            except TokenLimitError as e:
                if not token_limit_hit:
                    token_limit_hit = True
                    limit_detail = str(e)
                    _stop.set()
                    print('\n⚠️  Cursor agent usage/session limit reached. Stopping gracefully.')
                    print('   Re-run `python tools/fb_bulk.py` to resume — judged items are cached.')
                    if limit_detail:
                        print(f'   ({limit_detail[:200]})')
                res = {'status': 'token-limit-stop',
                       'ts': row.get('ts'), 'date': row.get('date'),
                       'src': row.get('src'),
                       'error': limit_detail or str(e)}
            except Exception as e:
                if is_token_limit_message(str(e)):
                    if not token_limit_hit:
                        token_limit_hit = True
                        limit_detail = str(e)
                        _stop.set()
                        print('\n⚠️  Cursor agent usage/session limit reached. Stopping gracefully.')
                        print('   Re-run `python tools/fb_bulk.py` to resume — judged items are cached.')
                    res = {'status': 'token-limit-stop',
                           'ts': row.get('ts'), 'date': row.get('date'),
                           'src': row.get('src'), 'error': str(e)}
                else:
                    res = {'status': 'error', 'error': str(e),
                           'ts': row.get('ts'), 'date': row.get('date'),
                           'src': row.get('src')}

            status = res.get('status', 'unknown')

            if res.get('resumed'):
                counts['resumed'] += 1
                prior = _last_run_status.get((row.get('ts'), row.get('src')))
                if prior == 'judge-error' and _should_resume_skip(row.get('ts'), row.get('src')):
                    counts['deferred'] += 1
                continue  # do not append_log again

            # After limit: skip per-item drain noise; log the triggering row once
            if status == 'stopped':
                continue
            if status == 'token-limit-stop':
                if not limit_logged:
                    append_log({**res, 'row_src': row.get('src')})
                    limit_logged = True
                continue

            if status == 'judge-error' and is_token_limit_message(res.get('error') or ''):
                if not token_limit_hit:
                    token_limit_hit = True
                    limit_detail = res.get('error', '')
                    _stop.set()
                    print('\n⚠️  Cursor agent usage/session limit reached. Stopping gracefully.')
                    print('   Re-run `python tools/fb_bulk.py` to resume — judged items are cached.')
                continue

            if 'error' in status:
                counts['error'] += 1
            elif status == 'written':
                counts['written'] += 1
            elif status == 'pending-judge':
                counts['pending-judge'] += 1
            elif status in ('skipped', 'skipped-domain', 'skipped-own-domain',
                            'skipped-empty'):
                counts['skipped'] += 1
            elif status == 'already-written':
                counts['already-written'] += 1
            elif status == 'dry-run-save':
                counts['dry-run-save'] += 1
            elif 'bundle' in status:
                counts['bundle'] += 1

            append_log({**res, 'row_src': row.get('src')})

            if processed % 100 == 0 or processed == len(rows):
                print(f'  {processed}/{len(rows)} — resumed:{counts["resumed"]} '
                      f'deferred:{counts["deferred"]} written:{counts["written"]} '
                      f'skipped:{counts["skipped"]} errors:{counts["error"]}'
                      + (' [STOPPING]' if _stop.is_set() else ''))
    finally:
        cancelled = 0
        for fut in futs:
            if fut.cancel():
                cancelled += 1
        ex.shutdown(wait=False, cancel_futures=True)
        if token_limit_hit and cancelled:
            print(f'   Cancelled {cancelled} queued tasks.')

    if token_limit_hit:
        print(f'\nStopped early after {processed} completed tasks — agent limit. Re-run to resume.')
        sys.exit(2)  # distinguish from success; safe to re-run
    else:
        print('\nDone.')
    if counts.get('resumed'):
        print(f'  Resumed (skip): {counts["resumed"]}')
    if counts.get('deferred'):
        print(f'  Stuck errors skipped: {counts["deferred"]} (non-retriable; use --retry-errors)')
    print(f'  Written:       {counts["written"]}')
    print(f'  Skipped:       {counts["skipped"]}')
    print(f'  Already done:  {counts["already-written"]}')
    print(f'  Dry-run saves: {counts["dry-run-save"]}')
    print(f'  Errors:        {counts["error"]}')
    if counts.get('pending-judge'):
        print(f'  Pending judge: {counts["pending-judge"]} (re-run without --cache-only after limit resets)')
    if args.dry_run:
        print('\n[DRY RUN] Nothing written to vault.')


if __name__ == '__main__':
    main()
