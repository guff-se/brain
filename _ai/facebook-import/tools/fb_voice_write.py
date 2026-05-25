#!/usr/bin/env python3
"""Parse voice_queue.md decisions (first 50) and write accepted notes to vault.

Also handles special third-party quote entries (#10, #11, #30 → consumed/clippings).
"""
from __future__ import annotations
import re, os, sys, datetime, unicodedata, json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
VAULT = os.path.dirname(os.path.dirname(PROJECT))
STAGING = os.path.join(PROJECT, 'staging')

# Third-party quotes that Gustaf wants saved as consumed/clippings
THIRD_PARTY_QUOTES = {
    10: {'author': 'Banksy', 'title': 'On Advertisers', 'tags': ['advertising', 'subversion', 'consumer-culture']},
    11: {'author': 'John Hodge', 'title': 'Choose Life — Trainspotting', 'tags': ['consumerism', 'meaning', 'culture']},
    30: {'author': 'Alan Watts', 'title': 'The Dream of Life', 'tags': ['consciousness', 'meaning', 'philosophy']},
}

def slugify(text: str, max_words: int = 6) -> str:
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text).lower()
    words = text.split()[:max_words]
    return '-'.join(words) or 'untitled'

def detect_lang(text: str) -> str:
    sv_chars = sum(1 for c in text if c in 'åäöÅÄÖ')
    if sv_chars / max(len(text), 1) > 0.01:
        return 'sv'
    sv_words = {'och', 'att', 'det', 'är', 'en', 'ett', 'jag', 'för', 'som', 'inte', 'vi', 'på', 'om'}
    if len(sv_words & set(text.lower().split())) >= 2:
        return 'sv'
    return 'en'

def atomic_write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def build_fm(fields: dict) -> str:
    lines = ['---']
    for k, v in fields.items():
        if v is None: continue
        if isinstance(v, list):
            if v: lines.append(f'{k}: [{", ".join(str(x) for x in v)}]')
        else:
            val = str(v).replace('"', '\\"')
            lines.append(f'{k}: "{val}"')
    lines.append('---')
    return '\n'.join(lines)

def write_own_note(num: int, date: str, call: str, text: str):
    register = 'voice' if call == 'voice' else 'thinking'
    dest_dir = os.path.join(VAULT, 'sources', 'mine', register)
    slug = slugify(text)
    path = os.path.join(dest_dir, f'{date}-{slug}.md')

    if os.path.exists(path):
        print(f'  #{num} already exists, skipping: {path}')
        return

    lang = detect_lang(text)
    title_short = text[:60].replace('"', "'") + ('…' if len(text) > 60 else '')
    tags = []  # LLM will tag in bulk pass; manual notes get empty tags for now

    fm = build_fm({
        'title': title_short,
        'summary': text[:120].replace('"', "'") + ('…' if len(text) > 120 else ''),
        'kind': 'note',
        'party': 'first',
        'register': register,
        'source': 'facebook',
        'source_id': f'fb-voice-queue-{num}',
        'provenance': 'extracted',
        'lang': lang,
        'tags': tags,
        'status': 'reference',
        'ingested': datetime.date.today().isoformat(),
        'created': date,
    })

    content = fm + '\n\n' + text + '\n'
    atomic_write(path, content)
    print(f'  #{num} [{call}] → {os.path.relpath(path, VAULT)}')

def write_clipping(num: int, date: str, text: str, meta: dict):
    dest_dir = os.path.join(VAULT, 'sources', 'consumed', 'clippings')
    slug = slugify(meta['title'])
    path = os.path.join(dest_dir, f'{date}-{slug}.md')

    if os.path.exists(path):
        print(f'  #{num} clipping already exists, skipping')
        return

    lang = detect_lang(text)
    fm = build_fm({
        'title': meta['title'],
        'summary': text[:120].replace('"', "'") + '…',
        'kind': 'clipping',
        'party': 'third',
        'register': 'consumed',
        'source': 'facebook',
        'source_id': f'fb-voice-queue-{num}',
        'author': meta['author'],
        'provenance': 'extracted',
        'lang': lang,
        'tags': meta.get('tags', []),
        'status': 'reference',
        'ingested': datetime.date.today().isoformat(),
        'created': date,
    })

    content = fm + '\n\n' + text + f'\n\n— {meta["author"]}\n'
    atomic_write(path, content)
    print(f'  #{num} [clipping/{meta["author"]}] → {os.path.relpath(path, VAULT)}')

def main():
    queue_path = os.path.join(STAGING, 'voice_queue.md')
    with open(queue_path, encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'\n(?=## \d+\.)', content)

    written = 0
    skipped = 0

    for sec in sections[1:51]:  # first 50
        num_m = re.match(r'## (\d+)\.', sec)
        if not num_m: continue
        num = int(num_m.group(1))

        date_m = re.search(r'## \d+\. (\d{4}-\d{2}-\d{2})', sec)
        date = date_m.group(1) if date_m else '2000-01-01'

        call_m = re.search(r'\[x\]\s*(voice|thinking|skip|private)', sec, re.IGNORECASE)
        if not call_m:
            call_m = re.search(r'\[(voice|thinking|skip|private)\]', sec, re.IGNORECASE)
        call = call_m.group(1).lower() if call_m else 'unmarked'

        text_m = re.search(r'```\n(.*?)```', sec, re.DOTALL)
        text = text_m.group(1).strip() if text_m else ''

        # Third-party quotes — always write as clipping regardless of checkbox
        if num in THIRD_PARTY_QUOTES:
            write_clipping(num, date, text, THIRD_PARTY_QUOTES[num])
            written += 1
            continue

        # Duplicate of a quote — skip
        if num == 23:
            print(f'  #{num} [duplicate of #10, skip]')
            skipped += 1
            continue

        # Unmarked non-quote entries — let bulk handle
        if call == 'unmarked':
            print(f'  #{num} [unmarked, will be handled by bulk runner]')
            skipped += 1
            continue

        if call in ('skip', 'private'):
            skipped += 1
            continue

        if call in ('voice', 'thinking') and text:
            write_own_note(num, date, call, text)
            written += 1
        else:
            skipped += 1

    print(f'\nDone. Written: {written}, Skipped/delegated: {skipped}')

if __name__ == '__main__':
    main()
