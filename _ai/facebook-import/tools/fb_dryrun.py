#!/usr/bin/env python3
"""Phase 0.5 — stratified 100-item dry-run.

Samples a representative cross-section of items, fetches URLs, runs the LLM judge,
and writes `staging/judge_sample.md` for Gustaf to sanity-check the rubric.
"""
from __future__ import annotations
import json, os, random, sys, concurrent.futures as cf
from dataclasses import asdict
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from fb_fetch import fetch, classify_domain, domain_of  # noqa
from fb_judge import judge, TokenLimitError, is_token_limit_message  # noqa

STAGING = os.path.join(PROJECT, 'staging')
JSONL = os.path.join(STAGING, 'all_posts.jsonl')


def load_rows():
    rows = []
    with open(JSONL) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def primary_url(row):
    for u in row.get('urls', []):
        url = u.get('url') or ''
        if url.startswith('http'):
            return u
    return None


def sample(rows, seed=42):
    rng = random.Random(seed)
    main = [r for r in rows if r['src'] in ('main1', 'main2')]

    text_only = [r for r in main if r['len'] >= 30 and r['n_urls'] == 0]
    commented = [r for r in main if r['len'] >= 30 and r['n_urls'] > 0]
    bare = [r for r in main if r['len'] < 30 and r['n_urls'] > 0]

    # tail vs top: top = domain count >= 20 (the 43 domains)
    from collections import Counter
    dom_counts = Counter()
    for r in main:
        for u in r['urls']:
            dom_counts[domain_of(u.get('url', ''))] += 1
    top_doms = {d for d, c in dom_counts.items() if c >= 20}

    bare_top = [r for r in bare if any(domain_of(u.get('url', '')) in top_doms for u in r['urls'])]
    bare_tail = [r for r in bare if not any(domain_of(u.get('url', '')) in top_doms for u in r['urls'])]

    # stratified buckets
    buckets = {
        'text_only_short':   [r for r in text_only if r['len'] < 200][:],
        'text_only_medium':  [r for r in text_only if 200 <= r['len'] < 500][:],
        'text_only_long':    [r for r in text_only if r['len'] >= 500][:],
        'commented_short':   [r for r in commented if r['len'] < 200][:],
        'commented_long':    [r for r in commented if r['len'] >= 200][:],
        'bare_top':          bare_top[:],
        'bare_tail':         bare_tail[:],
    }
    quotas = {
        'text_only_short': 15,
        'text_only_medium': 12,
        'text_only_long': 8,
        'commented_short': 15,
        'commented_long': 10,
        'bare_top': 25,
        'bare_tail': 15,
    }
    out = []
    for name, pool in buckets.items():
        k = min(quotas[name], len(pool))
        if pool:
            rng.shuffle(pool)
            for r in pool[:k]:
                out.append((name, r))
    rng.shuffle(out)
    return out


def process(bucket, row):
    """Run fetch (if applicable) + judge. Returns enriched dict."""
    out = {'bucket': bucket, 'row': row, 'fetch': None, 'judgement': None}
    u = primary_url(row)
    item_type = 'own_text'
    payload = {
        'text': row.get('text', ''),
        'date': row.get('date'),
    }
    fetched = None
    if u:
        url = u.get('url')
        cls = classify_domain(url)
        payload['url'] = url
        payload['domain'] = domain_of(url)
        # title from FB itself
        if u.get('name'):
            payload['title'] = u['name']
        if cls['action'] == 'skip':
            out['fetch'] = {'action': 'skipped', 'reason': cls['reason'], 'kind': cls['kind']}
            # don't judge if no commentary and we skipped — produce a synthetic skip verdict
            if not row.get('text'):
                out['judgement'] = {
                    'verdict': 'skip', 'confidence': 1.0,
                    'register_hint': None, 'kind_hint': None,
                    'tags_hint': [], 'reason': f'domain skipped ({cls["reason"]}) and no commentary',
                    'item_type': 'shared_article', 'error': '',
                }
                return out
            item_type = 'own_text'
        elif cls['action'] == 'own':
            out['fetch'] = {'action': 'own', 'reason': cls['reason'], 'kind': 'own'}
            if not row.get('text'):
                out['judgement'] = {
                    'verdict': 'skip', 'confidence': 0.9,
                    'register_hint': None, 'kind_hint': None,
                    'tags_hint': [], 'reason': 'own-domain link with no commentary — handle as fact, not consumed',
                    'item_type': 'shared_article', 'error': '',
                }
                return out
            item_type = 'own_commentary'
        else:
            try:
                fr = fetch(url, throttle=0.5)
                out['fetch'] = asdict(fr)
                fetched = fr
                if fr.title and not payload.get('title'):
                    payload['title'] = fr.title
                if fr.author:
                    payload['author'] = fr.author
                # Only feed fetched_text to the judge if it's substantive AND not a paywall stub
                if fr.action in ('ok', 'wayback') and fr.text_len > 100:
                    payload['fetched_text'] = fr.text
                if fr.action == 'paywalled':
                    payload['fetch_note'] = 'paywall — only title and commentary available; judge by those'
                if (fr.extra or {}).get('mp3_url'):
                    payload['fetch_note'] = (payload.get('fetch_note', '') + ' mp3 located').strip()
                if row.get('text'):
                    item_type = 'own_commentary'
                elif fr.kind == 'video':
                    item_type = 'shared_video'
                elif fr.kind == 'podcast':
                    item_type = 'shared_podcast'
                else:
                    item_type = 'shared_article'
            except Exception as e:
                out['fetch'] = {'action': 'error', 'error': str(e)}
    j = judge(item_type, payload)
    if j.verdict == 'error' and is_token_limit_message(j.error or ''):
        raise TokenLimitError(j.error)
    out['judgement'] = asdict(j)
    return out


def main(n=100):
    rows = load_rows()
    items = sample(rows)
    print(f'sampled {len(items)} items; processing with 6 workers...')
    results = []
    limit_hit = False
    ex = cf.ThreadPoolExecutor(max_workers=6)
    futs = {ex.submit(process, b, r): (b, r) for b, r in items}
    try:
        for i, fut in enumerate(cf.as_completed(futs), 1):
            if limit_hit:
                break
            try:
                results.append(fut.result())
            except TokenLimitError as e:
                limit_hit = True
                print(f'\n⚠️  Agent limit reached after {len(results)} items: {e}')
                print('Re-run later; judged items are cached.')
            except Exception as e:
                b, r = futs[fut]
                if is_token_limit_message(str(e)):
                    limit_hit = True
                    print(f'\n⚠️  Agent limit reached after {len(results)} items: {e}')
                else:
                    results.append({'bucket': b, 'row': r, 'error': str(e)})
            if i % 5 == 0:
                print(f'  {i}/{len(items)}')
    finally:
        ex.shutdown(wait=False, cancel_futures=True)

    # group by verdict
    saves = [r for r in results if r.get('judgement', {}).get('verdict') == 'save']
    skips = [r for r in results if r.get('judgement', {}).get('verdict') == 'skip']
    errors = [r for r in results if r.get('judgement', {}).get('verdict') not in ('save', 'skip')]

    # write report
    out = []
    out.append('# Facebook import — Phase 0.5 judge dry-run\n')
    out.append(f'Sampled {len(results)} items. **Save: {len(saves)}** · **Skip: {len(skips)}** · **Error: {len(errors)}**\n')
    out.append('Inspect a handful in each bucket. If the verdicts look wrong, edit `tools/fb_judge.py` (RUBRIC) and re-run — the cache is keyed by content, so changing the rubric does NOT auto-invalidate. Delete `staging/judged/` to force a fresh pass.\n')

    def render(items, header):
        out.append(f'\n## {header} ({len(items)})\n')
        for r in items:
            row = r['row']
            j = r.get('judgement') or {}
            f = r.get('fetch') or {}
            date = row.get('date') or 'n/a'
            bucket = r.get('bucket')
            text = (row.get('text') or '').strip()
            urls = row.get('urls') or []
            url = (urls[0].get('url') if urls else '') or ''
            dom = domain_of(url) if url else ''
            out.append(f'### {date} · {bucket}' + (f' · {dom}' if dom else ''))
            out.append('')
            out.append(f'- **verdict:** `{j.get("verdict")}` · conf `{j.get("confidence", 0):.2f}` · '
                       f'reg `{j.get("register_hint")}` · kind `{j.get("kind_hint")}` · '
                       f'tags `{", ".join(j.get("tags_hint", []))}`')
            out.append(f'- **reason:** {j.get("reason","")}')
            if url:
                fa = f.get('action', '')
                tl = f.get('text_len', 0)
                ft = (f.get('title') or '')[:120]
                out.append(f'- **url:** {url}  ·  fetch=`{fa}` len={tl}  ·  title={ft!r}')
            if text:
                snippet = text.replace('\n', ' ')
                if len(snippet) > 400:
                    snippet = snippet[:400] + '…'
                out.append(f'- **text:** {snippet}')
            if f.get('text') and not text:
                snippet = f['text'].replace('\n', ' ')[:300]
                out.append(f'- **fetched:** {snippet}…')
            out.append('')

    render(saves, 'SAVED')
    render(skips, 'SKIPPED')
    if errors:
        render(errors, 'ERRORS')

    path = os.path.join(STAGING, 'judge_sample.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))
    print(f'wrote {path}')

    # also dump raw results for inspection
    with open(os.path.join(STAGING, 'judge_sample.jsonl'), 'w') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + '\n')


if __name__ == '__main__':
    main()
