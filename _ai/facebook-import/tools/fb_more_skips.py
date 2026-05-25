#!/usr/bin/env python3
"""Pull 30 more skipped items, varied across buckets, for human calibration review.

Re-uses the cache. New items are sampled with a different seed so we don't
just see the same 100.
"""
from __future__ import annotations
import json, os, random, sys, concurrent.futures as cf
from dataclasses import asdict

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from fb_dryrun import load_rows, sample, process  # type: ignore
from fb_fetch import domain_of  # noqa

STAGING = os.path.join(PROJECT, 'staging')


def main():
    rows = load_rows()
    # Use a fresh seed and oversample so we end up with >=30 SKIPs across buckets
    rng = random.Random(7)
    main_rows = [r for r in rows if r['src'] in ('main1', 'main2')]
    rng.shuffle(main_rows)

    # Build same buckets as fb_dryrun but with fresh items
    from collections import Counter
    dom_counts = Counter()
    for r in main_rows:
        for u in r['urls']:
            dom_counts[domain_of(u.get('url', ''))] += 1
    top_doms = {d for d, c in dom_counts.items() if c >= 20}

    def primary_url(row):
        for u in row.get('urls', []):
            if u.get('url', '').startswith('http'):
                return u
        return None

    text_only = [r for r in main_rows if r['len'] >= 30 and r['n_urls'] == 0]
    commented = [r for r in main_rows if r['len'] >= 30 and r['n_urls'] > 0]
    bare = [r for r in main_rows if r['len'] < 30 and r['n_urls'] > 0]

    bare_top = [r for r in bare if any(domain_of(u.get('url', '')) in top_doms for u in r['urls'])]
    bare_tail = [r for r in bare if not any(domain_of(u.get('url', '')) in top_doms for u in r['urls'])]

    # already-seen content keys to avoid re-rendering the same items
    seen_keys = set()
    if os.path.exists(os.path.join(STAGING, 'judge_sample.jsonl')):
        for line in open(os.path.join(STAGING, 'judge_sample.jsonl')):
            d = json.loads(line)
            r = d['row']
            key = (r.get('ts'), r.get('text', '')[:120])
            seen_keys.add(key)

    def keyof(r): return (r.get('ts'), r.get('text', '')[:120])

    buckets = {
        'text_only_short':  [r for r in text_only if r['len'] < 200 and keyof(r) not in seen_keys],
        'text_only_medium': [r for r in text_only if 200 <= r['len'] < 500 and keyof(r) not in seen_keys],
        'text_only_long':   [r for r in text_only if r['len'] >= 500 and keyof(r) not in seen_keys],
        'commented_short':  [r for r in commented if r['len'] < 200 and keyof(r) not in seen_keys],
        'commented_long':   [r for r in commented if r['len'] >= 200 and keyof(r) not in seen_keys],
        'bare_top':         [r for r in bare_top if keyof(r) not in seen_keys],
        'bare_tail':        [r for r in bare_tail if keyof(r) not in seen_keys],
    }
    # Oversample to ~80 items; we'll keep first 30 SKIPs.
    target = {'text_only_short': 12, 'text_only_medium': 12, 'text_only_long': 8,
              'commented_short': 14, 'commented_long': 12, 'bare_top': 18, 'bare_tail': 14}
    pool = []
    for name, lst in buckets.items():
        rng.shuffle(lst)
        for r in lst[:target[name]]:
            pool.append((name, r))

    print(f'oversampled {len(pool)} items; processing...')
    results = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(process, b, r): (b, r) for b, r in pool}
        for i, fut in enumerate(cf.as_completed(futs), 1):
            try:
                results.append(fut.result())
            except Exception as e:
                pass
            if i % 10 == 0:
                print(f'  {i}/{len(pool)}')

    # filter to SKIPs, take 30
    skips = [r for r in results if r.get('judgement', {}).get('verdict') == 'skip']
    # ensure cross-bucket variety: round-robin pick
    by_bucket = {}
    for r in skips:
        by_bucket.setdefault(r['bucket'], []).append(r)
    final = []
    while len(final) < 30 and any(by_bucket.values()):
        for b in list(by_bucket.keys()):
            if by_bucket[b]:
                final.append(by_bucket[b].pop(0))
                if len(final) >= 30:
                    break

    # render
    out = ['# Borderline-skip calibration — 30 more skipped items\n']
    out.append(f'Sampled {len(results)} new items from the corpus (none overlapping the first 100). Showing 30 SKIP verdicts across buckets so you can spot rubric drift.\n')
    out.append('For each item, mark in the brackets:\n')
    out.append('- `[ok]` skip is correct')
    out.append('- `[promote]` should be saved as a note')
    out.append('- `[bundle]` keep out of individual notes, but include in year-bundle')
    out.append('')
    for r in final:
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
        out.append('  - call: `[ ]`  (fill: ok | promote | bundle)')
        out.append(f'  - **verdict reason:** {j.get("reason","")}')
        if url:
            fa = f.get('action', '')
            tl = f.get('text_len', 0)
            ft = (f.get('title') or '')[:120]
            out.append(f'  - **url:** {url}  ·  fetch=`{fa}` len={tl}  ·  title={ft!r}')
        if text:
            snippet = text.replace('\n', ' ')
            if len(snippet) > 500:
                snippet = snippet[:500] + '…'
            out.append(f'  - **text:** {snippet}')
        if (f.get('text') or '') and not text:
            snippet = (f.get('text') or '').replace('\n', ' ')[:400]
            out.append(f'  - **fetched:** {snippet}…')
        out.append('')

    path = os.path.join(STAGING, 'calibration_skips.md')
    with open(path, 'w') as fp:
        fp.write('\n'.join(out))
    print(f'wrote {path}')


if __name__ == '__main__':
    main()
