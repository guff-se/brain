#!/usr/bin/env python3
"""Move orphan FB thinking notes (link stub, no consumed wikilink) to quarantine."""
from __future__ import annotations
import argparse
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
THINKING = os.path.join(VAULT, 'sources', 'mine', 'thinking')
QUARANTINE = os.path.join(VAULT, '_ai', 'excluded', 'facebook-link-stubs-v2')

FB = re.compile(r'^source:\s*"?facebook"?', re.M)


def is_orphan_stub(text: str) -> bool:
    if not FB.search(text[:2000]):
        return False
    if '→ [[' in text:
        return False
    return '*Shared link:' in text or 'fb_url:' in text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    moved = 0
    for fn in sorted(os.listdir(THINKING)):
        if not fn.endswith('.md'):
            continue
        path = os.path.join(THINKING, fn)
        text = open(path, encoding='utf-8').read()
        if not is_orphan_stub(text):
            continue
        dest = os.path.join(QUARANTINE, fn)
        if args.dry_run:
            print(f'  {fn}')
        else:
            os.makedirs(QUARANTINE, exist_ok=True)
            shutil.move(path, dest)
        moved += 1
    print(f'{"Would move" if args.dry_run else "Moved"} {moved} orphan link stubs')


if __name__ == '__main__':
    main()
