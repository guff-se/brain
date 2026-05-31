#!/usr/bin/env python3
"""LLM judge applying the durability rubric (PLAN.md §7.1).

Input: a candidate item — Gustaf's post text, and/or the content of a URL he shared.
Output: {verdict: save|skip, confidence, register_hint, kind_hint, tags_hint, reason}.

Cached by content hash. Re-runs are free.
"""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, time
from dataclasses import dataclass, asdict
from typing import Optional


class TokenLimitError(Exception):
    """Raised when the Cursor agent subprocess signals a usage/token/session limit."""
    pass


# Substrings in agent stdout/stderr that mean "stop the bulk run", not "retry".
_TOKEN_LIMIT_SIGNALS = (
    'usage limit',
    'session limit',       # CLI OAuth / session cap
    'hit your session',    # "You've hit your session limit …"
    'hit your usage',
    'rate limit',
    'rate_limit',
    'out of tokens',
    'token limit',
    'context limit',
    'maximum context',
    'context window',
    'billing',
    'quota',
    'insufficient_quota',
    'out of credit',
    'out of credits',
    'no credits',
    'not enough credit',
    'credit balance',
    'spend limit',
    'capacity',
    'temporarily unavailable',
    'please try again',
    'too many requests',
    'overloaded',
    '429',
    'resets ',             # "resets 10am (Europe/Stockholm)" on session limit
    'likely usage/session/credits',  # exit 1 with empty CLI capture
)

# Infrastructure glitches — retry the item, do not stop the bulk run.
_TRANSIENT_ERROR_SIGNALS = (
    'cli-config.json',
    'enoent:',
    'enotfound',
    'econnreset',
    'econnrefused',
    'etimedout',
    'getaddrinfo',
    'socket hang up',
    'fetch failed',
    'eai_again',
)


def is_transient_agent_error(text: str) -> bool:
    """True if *text* looks like a retryable CLI/network/filesystem glitch."""
    if not text:
        return False
    low = text.lower()
    return any(sig in low for sig in _TRANSIENT_ERROR_SIGNALS)


def is_token_limit_message(text: str) -> bool:
    """True if *text* looks like an agent usage/session/rate/credit limit (not a generic bug)."""
    if not text or is_transient_agent_error(text):
        return False
    low = text.lower()
    return any(sig in low for sig in _TOKEN_LIMIT_SIGNALS)


def is_retriable_judge_error(error: str) -> bool:
    """True if a prior judge-error should be retried on the next bulk run.

    Retriable: usage/session limits (after reset), transient CLI/network errors,
    empty ``agent exited 1`` (legacy limit heuristic).

    Non-retriable: model returned prose instead of JSON (missing content in prompt) — rare.
    """
    if not error or not error.strip():
        return True
    if is_transient_agent_error(error):
        return True
    if is_token_limit_message(error):
        return True
    low = error.lower()
    if ('agent exited 1' in low or 'claude exited 1' in low
            or 'cursor agent exited 1' in low):
        return True
    if 'timed out' in low or 'timeout' in low:
        return True
    if 'no json' in low:
        return False
    if 'valueerror' in low and 'no json' in low:
        return False
    # Unknown — retry once more rather than leave stuck
    return True

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
STAGING = os.path.join(PROJECT, 'staging')
CACHE = os.path.join(STAGING, 'judged')
os.makedirs(CACHE, exist_ok=True)

BACKEND = os.environ.get('FB_JUDGE_BACKEND', 'cursor').lower()
MODEL = os.environ.get('FB_JUDGE_MODEL', '')
CURSOR_BIN = os.environ.get(
    'CURSOR_BIN',
    shutil.which('cursor') or '/usr/local/bin/cursor',
)
CLAUDE_BIN = os.environ.get(
    'CLAUDE_BIN',
    shutil.which('claude') or os.path.expanduser('~/.local/bin/claude'),
)

_DEFAULT_MODEL = {'cursor': 'auto', 'claude': 'claude-haiku-4-5'}


def configure_judge(*, backend: str | None = None, model: str | None = None) -> None:
    """Set judge backend/model for this process. Call once from fb_bulk / fb_dryrun."""
    global BACKEND, MODEL
    prev_backend = BACKEND
    if backend is not None:
        backend = backend.lower()
        if backend not in ('cursor', 'claude'):
            raise ValueError(f'unknown judge backend: {backend!r} (use cursor or claude)')
        BACKEND = backend
    if model:
        MODEL = model
    elif not MODEL:
        MODEL = _DEFAULT_MODEL[BACKEND]
    elif backend is not None and prev_backend != BACKEND and MODEL == _DEFAULT_MODEL.get(prev_backend):
        MODEL = _DEFAULT_MODEL[BACKEND]
    os.makedirs(_cache_dir(), exist_ok=True)


def judge_backend() -> str:
    return BACKEND


def judge_model() -> str:
    _ensure_configured()
    return MODEL


def judge_backend_label() -> str:
    return 'Claude' if BACKEND == 'claude' else 'Cursor agent'


def _cache_dir() -> str:
    """Cursor keeps the legacy flat judged/ layout; Claude uses judged/claude/."""
    if BACKEND == 'cursor':
        return CACHE
    return os.path.join(CACHE, BACKEND)


def _ensure_configured() -> None:
    if not MODEL:
        configure_judge()


def _handle_subprocess(name: str, proc: subprocess.CompletedProcess[str]) -> str:
    stdout = proc.stdout or ''
    stderr = proc.stderr or ''
    combined = stdout + stderr
    out_stripped = stdout.strip()
    err_stripped = stderr.strip()
    combined_stripped = (out_stripped + err_stripped).strip()
    limit_prefix = 'Claude limit' if name == 'claude' else 'Agent limit'

    if proc.returncode != 0:
        detail = (combined_stripped or f'exit {proc.returncode}')[:500]
        if (is_transient_agent_error(combined)
                or is_transient_agent_error(stdout)
                or is_transient_agent_error(stderr)):
            raise RuntimeError(f'{name} exited {proc.returncode}: {detail}')
        if (is_token_limit_message(combined)
                or is_token_limit_message(stdout)
                or is_token_limit_message(stderr)):
            raise TokenLimitError(f'{limit_prefix} (exit {proc.returncode}): {detail}')
        if proc.returncode == 1 and not combined_stripped:
            raise TokenLimitError(
                f'{limit_prefix} (exit 1, no output — likely usage/session/credits): {detail}'
            )
        raise RuntimeError(f'{name} exited {proc.returncode}: {detail}')

    if name == 'cursor agent':
        stdout_has_verdict = '"verdict"' in stdout
        if not stdout_has_verdict and is_token_limit_message(stderr):
            raise TokenLimitError(f'{limit_prefix} (exit 0, stderr): {err_stripped[:500]}')
    elif is_token_limit_message(combined):
        raise TokenLimitError(f'{limit_prefix} (exit 0): {combined_stripped[:500]}')
    return stdout


def _call_claude(system: str, user: str, timeout: int = 90) -> str:
    """Invoke `claude -p` non-interactively. Uses OAuth from keychain."""
    cmd = [
        CLAUDE_BIN, '-p',
        '--model', MODEL,
        '--append-system-prompt', system,
        '--disable-slash-commands',
        '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
        '--disallowedTools', 'Bash,Edit,Write,Read,Glob,Grep,Agent,Task,WebFetch,WebSearch',
    ]
    try:
        proc = subprocess.run(
            cmd, input=user, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f'claude timed out after {timeout}s')
    return _handle_subprocess('claude', proc)


def _call_cursor(system: str, user: str, timeout: int = 90) -> str:
    """Invoke `cursor agent -p` non-interactively (--mode ask, JSON-only rubric)."""
    prompt = f'{system}\n\n---\n\n{user}'
    cmd = [
        CURSOR_BIN, 'agent', '-p',
        '--mode', 'ask',
        '--model', MODEL,
        '--trust',
        '--output-format', 'text',
        '--workspace', PROJECT,
        prompt,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError(f'cursor agent timed out after {timeout}s')
    return _handle_subprocess('cursor agent', proc)


def _call_llm(system: str, user: str, timeout: int = 90) -> str:
    _ensure_configured()
    if BACKEND == 'claude':
        return _call_claude(system, user, timeout=timeout)
    return _call_cursor(system, user, timeout=timeout)


configure_judge()


RUBRIC = """You are curating Gustaf's external brain (an Obsidian vault). He is importing 20 years of his own Facebook posts and the links he shared.

You receive ONE candidate item. Decide whether it deserves to live as its own note in the vault.

# Save the item if it:
- Contains durable knowledge, ideas, frameworks, or insights that remain useful over time
- Explores causality, mechanisms, patterns, or principles (not just events)
- Shares perspective, analysis, or expertise worth building on
- Could deepen understanding of a topic, domain, or human experience

# Do NOT save if it:
- Is primarily a news announcement or time-bound event report
- Is social banter, small talk, or relational exchange with no embedded knowledge
- Describes that something happened without explaining why or what it means
- Is promotional, transactional, or logistical in nature
- Is a one-liner reaction, quote, meme caption, or link title with no added reasoning
- Merely signals agreement/disgust with something external (save the article instead, not this)

# Item types
- `own_text`        — Gustaf wrote this. No external link, or the link was incidental.
- `own_commentary`  — ONLY Gustaf's commentary on a share (not the article body). Saved separately from the article.
- `shared_article`  — The fetched body (or metadata) of a URL Gustaf shared.
- `shared_video`    — Video metadata (title, description) from YouTube/Vimeo/etc.
- `shared_podcast`  — Podcast episode metadata.

# Length rules (strict — apply before other criteria)
If `length_note` is present, follow it exactly.

For `own_text`:
- Under 200 characters: default **skip**. Save only if Gustaf develops a clear argument with mechanism/causality in multiple sentences — not a quip, quote, or slogan.
- 200–499 characters: save only with a non-trivial claim or reasoning chain, not mood or hot take.

For `own_commentary` — read `pairing_note` if present:
- **paired** (article already passed): save only if commentary adds real framing beyond the headline — a reaction, quote, or hot take is **skip** (the article note will be dropped too).
- **standalone** (article failed durability): default **skip** unless ≥200 chars of Gustaf's own reasoning (mechanism, principle, causal claim). Reactions to ephemeral news do not qualify.
- Under 80 characters: always **skip**.
- 80–199 characters: default **skip** unless standalone mode and exceptional argument density.

For `shared_article` / `shared_video` / `shared_podcast`:
- Judge the external content for durable substance. Gustaf's short reaction is irrelevant here.
- `register_hint` must be `consumed` when saving external content.

# Special: paywalled articles
If the input includes `fetch_note: paywall — only title and commentary available`, judge by title + author signal. Save only if the topic is clearly durable analysis, not breaking news.

# Special: thin video/podcast metadata
Save only if title/description names a durable topic (framework, named expert, structural issue). Generic entertainment → skip.

# Register hint (if save)
- `voice`    — Polished, finished prose by Gustaf. Rare. Manifestos, essays (usually ≥500 chars).
- `thinking` — Gustaf's own view with reasoning. For `own_commentary` / `own_text` only.
- `consumed` — External authored content (`shared_*` only). Never use `thinking` for article bodies.

# Output
Respond with ONLY a JSON object, no prose:
{
  "verdict": "save" | "skip",
  "confidence": 0.0-1.0,
  "register_hint": "voice" | "thinking" | "consumed" | null,
  "kind_hint": "article" | "video" | "podcast" | "book" | "clipping" | "note" | null,
  "tags_hint": [up to 3 kebab-case English tags, or branded proper-name tags like "burning-man" or "the-borderland"],
  "reason": "one short sentence — why this verdict"
}
"""


@dataclass
class Judgement:
    verdict: str          # save|skip|error
    confidence: float
    register_hint: Optional[str]
    kind_hint: Optional[str]
    tags_hint: list
    reason: str
    model: str
    item_type: str
    content_sha: str
    error: str = ''


def _atomic_write_json(path: str, data) -> None:
    """tmp + rename so a mid-write kill never corrupts the cache."""
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def hash_item(item_type: str, payload: dict) -> str:
    """Content hash for judged/ cache filenames."""
    h = hashlib.sha1()
    h.update(item_type.encode())
    h.update(b'\0')
    h.update(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())
    return h.hexdigest()[:20]


_hash_item = hash_item  # backward compat


def judgement_cache_path(item_type: str, payload: dict) -> str:
    return os.path.join(_cache_dir(), hash_item(item_type, payload) + '.json')


def load_cached_judgement(item_type: str, payload: dict) -> Optional[Judgement]:
    path = judgement_cache_path(item_type, payload)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return Judgement(**json.load(f))


def judge(item_type: str, payload: dict, *, retries: int = 2) -> Judgement:
    """item_type: own_text|own_commentary|shared_article|shared_video|shared_podcast
    payload keys (any subset):
      text: Gustaf's text
      url: source url (if any)
      title: page/video title
      author: author/channel
      domain: domain
      date: ISO date
      fetched_text: extracted body of the URL
    """
    _ensure_configured()
    sha = hash_item(item_type, payload)
    cache_path = judgement_cache_path(item_type, payload)
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return Judgement(**json.load(f))

    # Build user message
    parts = [f'Item type: {item_type}']
    for k in ('date', 'url', 'domain', 'title', 'author', 'fetch_note'):
        v = payload.get(k)
        if v:
            parts.append(f'{k}: {v}')
    if payload.get('length_note'):
        parts.append(f"length_note: {payload['length_note']}")
    if payload.get('pairing_note'):
        parts.append(f"pairing_note: {payload['pairing_note']}")
    if payload.get('text'):
        parts.append(f"\nGustaf's text:\n---\n{payload['text'][:4000]}\n---")
    if payload.get('fetched_text'):
        parts.append(f"\nFetched content (truncated):\n---\n{payload['fetched_text'][:6000]}\n---")
    user_msg = '\n'.join(parts)

    last_err = ''
    for attempt in range(retries + 1):
        try:
            raw = _call_llm(RUBRIC, user_msg)
            data = _parse_json(raw)
            j = Judgement(
                verdict=data.get('verdict', 'skip'),
                confidence=float(data.get('confidence', 0.0)),
                register_hint=data.get('register_hint'),
                kind_hint=data.get('kind_hint'),
                tags_hint=data.get('tags_hint') or [],
                reason=data.get('reason', ''),
                model=MODEL,
                item_type=item_type,
                content_sha=sha,
            )
            _atomic_write_json(cache_path, asdict(j))
            return j
        except TokenLimitError:
            raise  # propagate immediately — don't retry, don't cache
        except Exception as e:
            last_err = f'{type(e).__name__}: {e}'
            if is_token_limit_message(last_err) or is_token_limit_message(str(e)):
                raise TokenLimitError(last_err) from e
            # Transient CLI races / network blips — backoff a bit longer before retry.
            delay = 2.5 * (attempt + 1) if is_transient_agent_error(last_err) else 1.5 * (attempt + 1)
            time.sleep(delay)

    if is_token_limit_message(last_err):
        raise TokenLimitError(last_err)
    j = Judgement('error', 0.0, None, None, [], '', MODEL, item_type, sha, error=last_err)
    return j


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith('```'):
        raw = raw.split('```', 2)[1]
        if raw.startswith('json'):
            raw = raw[4:]
        raw = raw.rsplit('```', 1)[0]
    # find first { and last }
    a = raw.find('{')
    b = raw.rfind('}')
    if a < 0 or b < 0:
        raise ValueError(f'no json in: {raw[:200]}')
    return json.loads(raw[a:b+1])


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Test the durability judge on one item.')
    ap.add_argument('text', nargs='?', default='hej hej grattis på födelsedagen')
    ap.add_argument('--backend', choices=['cursor', 'claude'],
                    default=os.environ.get('FB_JUDGE_BACKEND', 'cursor'))
    ap.add_argument('--model', default=os.environ.get('FB_JUDGE_MODEL') or None)
    args = ap.parse_args()
    configure_judge(backend=args.backend, model=args.model)
    payload = {'text': args.text}
    print(json.dumps(asdict(judge('own_text', payload)), indent=2, ensure_ascii=False))
