#!/usr/bin/env python3
"""Quarantine vault files from the current bulk run_log and reset log resume for re-run.

Moves every path listed as written/already-written in run_log.jsonl (if file exists).
Removes those log lines so fb_bulk does not instant-skip them.
Invalidates judged/ save verdicts for own_commentary + shared_article (keeps skip).
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
RUN_LOG = os.path.join(STAGING, 'run_log.jsonl')
JUDGED = os.path.join(STAGING, 'judged')
QUARANTINE = os.path.join(
    VAULT, '_ai', 'excluded', f'facebook-import-batch-{date.today().isoformat()}',
)
SOURCES = os.path.join(VAULT, 'sources')

FB = re.compile(r'^source:\s*"?facebook"?', re.M)


def collect_written_paths() -> tuple[set[str], set[tuple]]:
    paths: set[str] = set()
    keys: set[tuple] = set()
    if not os.path.exists(RUN_LOG):
        return paths, keys
    with open(RUN_LOG, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if e.get('status') not in ('written', 'already-written'):
                continue
            keys.add((e.get('ts'), e.get('row_src') or e.get('src')))
            p = e.get('path')
            if p:
                paths.add(p)
            for pp in e.get('paths') or []:
                paths.add(pp)
    return paths, keys


def collect_all_fb_sources() -> list[str]:
    out = []
    for root, _dirs, fns in os.walk(SOURCES):
        for fn in fns:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(root, fn)
            try:
                if FB.search(open(path, encoding='utf-8').read(2048)):
                    out.append(path)
            except OSError:
                pass
    return sorted(out)


def quarantine_files(paths: list[str], dry_run: bool) -> int:
    n = 0
    for path in paths:
        if not os.path.isfile(path):
            continue
        rel = os.path.relpath(path, SOURCES)
        dest = os.path.join(QUARANTINE, rel)
        if dry_run:
            print(f'  move: {rel}')
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(path, dest)
        n += 1
    return n


def prune_run_log(keys: set[tuple], dry_run: bool) -> tuple[int, int]:
    if not os.path.exists(RUN_LOG):
        return 0, 0
    kept, dropped = [], 0
    with open(RUN_LOG, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            key = (e.get('ts'), e.get('row_src') or e.get('src'))
            if e.get('status') in ('written', 'already-written') or key in keys:
                dropped += 1
                continue
            kept.append(line)
    if dry_run:
        return len(kept), dropped
    tmp = RUN_LOG + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        for line in kept:
            f.write(line + '\n')
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, RUN_LOG)
    return len(kept), dropped


def invalidate_batch_judgements(dry_run: bool) -> int:
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
        if j.get('verdict') != 'save':
            continue
        if j.get('item_type') not in ('own_commentary', 'shared_article', 'shared_video', 'shared_podcast'):
            continue
        if dry_run:
            print(f'  judged save: {fn} ({j.get("item_type")})')
        else:
            os.remove(path)
        removed += 1
    return removed


def main():
    ap = argparse.ArgumentParser(description='Quarantine last bulk batch for FB re-run')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--all-fb-in-sources', action='store_true',
                    help='Also move any source:facebook file under sources/ (default: on)')
    ap.add_argument('--no-all-fb', dest='all_fb', action='store_false',
                    help='Only move paths explicitly listed in run_log')
    ap.set_defaults(all_fb=True)
    args = ap.parse_args()

    log_paths, keys = collect_written_paths()
    to_move = sorted(log_paths)
    if args.all_fb:
        to_move = sorted(set(to_move) | set(collect_all_fb_sources()))

    print(f'Quarantine → {QUARANTINE}')
    print(f'Files to move: {len(to_move)}')
    n = quarantine_files(to_move, args.dry_run)

    print(f'\nPrune run_log (drop written/already-written):')
    kept, dropped = prune_run_log(keys, args.dry_run)
    print(f'  keep {kept} lines, drop {dropped}')

    print(f'\nInvalidate shared_* + own_commentary save judgements:')
    inv = invalidate_batch_judgements(args.dry_run)
    print(f'  remove {inv}')

    if args.dry_run:
        print('\n[DRY RUN]')
    else:
        print(f'\nDone. Moved {n} files. Re-run: .venv/bin/python tools/fb_bulk.py')


if __name__ == '__main__':
    main()
