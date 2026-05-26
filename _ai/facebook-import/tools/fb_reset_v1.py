#!/usr/bin/env python3
"""Roll back Facebook import v1: quarantine vault notes, invalidate save-judgements, archive run_log.

Keeps judged/ entries with verdict=skip (and shared_article+save+consumed that were routed correctly).
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
VAULT = os.path.dirname(os.path.dirname(PROJECT))
STAGING = os.path.join(PROJECT, 'staging')
QUARANTINE = os.path.join(VAULT, '_ai', 'excluded', 'facebook-import-v1')
SOURCES = os.path.join(VAULT, 'sources')
JUDGED = os.path.join(STAGING, 'judged')
RUN_LOG = os.path.join(STAGING, 'run_log.jsonl')

FB_SOURCE_RE = re.compile(r'^source:\s*"?facebook"?', re.M)


def find_facebook_notes() -> list[str]:
    out = []
    for root, _dirs, files in os.walk(SOURCES):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(root, fn)
            try:
                head = open(path, encoding='utf-8').read(4096)
            except OSError:
                continue
            if FB_SOURCE_RE.search(head):
                out.append(path)
    return sorted(out)


def quarantine_notes(paths: list[str], dry_run: bool) -> int:
    n = 0
    for path in paths:
        rel = os.path.relpath(path, SOURCES)
        dest = os.path.join(QUARANTINE, rel)
        if dry_run:
            print(f'  would move: {rel}')
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(path, dest)
        n += 1
    return n


def invalidate_commentary_saves(dry_run: bool) -> int:
    """Drop own_commentary save caches — pairing rules changed (v2.1)."""
    removed = 0
    if not os.path.isdir(JUDGED):
        return 0
    for fn in os.listdir(JUDGED):
        if not fn.endswith('.json'):
            continue
        path = os.path.join(JUDGED, fn)
        try:
            j = json.load(open(path, encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue
        if j.get('item_type') == 'own_commentary' and j.get('verdict') == 'save':
            if dry_run:
                print(f'  would delete commentary save: {fn}')
            else:
                os.remove(path)
            removed += 1
    return removed


def invalidate_save_judgements(dry_run: bool) -> tuple[int, int]:
    kept = removed = 0
    if not os.path.isdir(JUDGED):
        return kept, removed
    for fn in os.listdir(JUDGED):
        if not fn.endswith('.json'):
            continue
        path = os.path.join(JUDGED, fn)
        try:
            j = json.load(open(path, encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue
        verdict = j.get('verdict')
        if verdict == 'skip':
            kept += 1
            continue
        if verdict != 'save':
            kept += 1
            continue
        it = j.get('item_type', '')
        reg = j.get('register_hint')
        if it == 'shared_article' and reg == 'consumed':
            kept += 1
            continue
        if dry_run:
            print(f'  would delete judged: {fn} ({it}, {reg})')
        else:
            os.remove(path)
        removed += 1
    return kept, removed


def archive_run_log(dry_run: bool) -> bool:
    if not os.path.exists(RUN_LOG):
        return False
    dest = os.path.join(STAGING, f'run_log.v1-{date.today().isoformat()}.jsonl')
    if dry_run:
        print(f'  would archive run_log → {os.path.basename(dest)}')
        return True
    if os.path.exists(dest):
        os.remove(dest)
    shutil.move(RUN_LOG, dest)
    return True


def main():
    ap = argparse.ArgumentParser(description='Reset Facebook import v1 outputs')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--commentary-only', action='store_true',
                    help='Only invalidate own_commentary save judgements (v2.1 pairing)')
    args = ap.parse_args()

    print('Facebook import v1 reset')
    print(f'  Vault: {VAULT}')
    print(f'  Quarantine: {QUARANTINE}')

    if args.commentary_only:
        print('\nInvalidate own_commentary save judgements only')
        n = invalidate_commentary_saves(args.dry_run)
        print(f'   removed {n}')
        if not args.dry_run:
            print('Also run: .venv/bin/python tools/fb_purge_link_stubs.py')
        return

    paths = find_facebook_notes()
    print(f'\n1. Quarantine {len(paths)} notes under sources/')
    n = quarantine_notes(paths, args.dry_run)

    print(f'\n2. Invalidate save judgements (keep skip + shared_article/consumed saves)')
    kept, removed = invalidate_save_judgements(args.dry_run)
    print(f'   kept {kept}, remove {removed}')

    print('\n3. Archive run_log.jsonl')
    archived = archive_run_log(args.dry_run)
    print(f'   {"archived" if archived else "no run_log"}')

    if args.dry_run:
        print('\n[DRY RUN] No changes made.')
    else:
        print(f'\nDone. Moved {n} notes. Re-run: .venv/bin/python tools/fb_bulk.py')


if __name__ == '__main__':
    main()
