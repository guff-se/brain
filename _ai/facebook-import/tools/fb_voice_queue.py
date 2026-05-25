#!/usr/bin/env python3
"""Generate staging/voice_queue.md — manual review queue for posts ≥500 chars.

These are the top-tier candidates for mine/voice/ or mine/thinking/. You
mark each with: [ ] voice  [ ] thinking  [ ] skip  [ ] private

After you fill in the queue, run fb_voice_write.py to write the accepted ones.
"""
from __future__ import annotations
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
STAGING = os.path.join(PROJECT, 'staging')
JSONL = os.path.join(STAGING, 'all_posts.jsonl')
OUT = os.path.join(STAGING, 'voice_queue.md')


def main():
    rows = []
    with open(JSONL) as f:
        for line in f:
            rows.append(json.loads(line))

    # Only main stream posts with substantial original text
    candidates = [
        r for r in rows
        if r['src'] in ('main1', 'main2', 'archive')
        and r['len'] >= 500
        and r.get('text', '').strip()
    ]
    # Sort oldest first
    candidates.sort(key=lambda r: r.get('ts', 0))

    print(f'{len(candidates)} candidates ≥500 chars')

    lines = []
    lines.append('# Voice queue — manual review')
    lines.append('')
    lines.append(f'Generated {datetime.date.today()}. {len(candidates)} posts ≥500 chars from the main Facebook stream.')
    lines.append('')
    lines.append('**For each post, fill ONE checkbox:**')
    lines.append('- `[voice]` — polished, finished Gustaf-language. Will go to `sources/mine/voice/`. Quote verbatim, never paraphrase.')
    lines.append('- `[thinking]` — your view, not yet prose. Goes to `sources/mine/thinking/`.')
    lines.append('- `[skip]` — the bulk judge will handle it (or it\'s noise).')
    lines.append('- `[private]` — exclude entirely. Not stored.')
    lines.append('')
    lines.append('Hint: length ≥1500 chars is marked 🔴 (more likely voice). 500–1499 is 🟡.')
    lines.append('')
    lines.append('---')
    lines.append('')

    for i, r in enumerate(candidates, 1):
        date = r.get('date', 'n/a')
        text = r.get('text', '').strip()
        length = r['len']
        marker = '🔴' if length >= 1500 else '🟡'
        year = r.get('year', '')

        lines.append(f'## {i}. {date} {marker} ({length} chars)')
        lines.append('')
        lines.append(f'**call:** `[ ] voice`  `[ ] thinking`  `[ ] skip`  `[ ] private`')
        lines.append('')
        lines.append('```')
        lines.append(text)
        lines.append('```')
        lines.append('')
        lines.append('---')
        lines.append('')

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Wrote {OUT}')
    print(f'🔴 ≥1500 chars: {sum(1 for r in candidates if r["len"] >= 1500)}')
    print(f'🟡 500–1499 chars: {sum(1 for r in candidates if 500 <= r["len"] < 1500)}')


if __name__ == '__main__':
    main()
