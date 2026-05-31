#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path('/Users/dante/brain')
THINKING_DIR = ROOT / 'sources' / 'mine' / 'thinking'
REPORT_PATH = ROOT / '_ai' / 'reports' / 'thought-tag-normalization-latest.md'

TAG_LINE_RE = re.compile(r'^Tags:\s*(.+?)\s*$', re.M)
FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
INLINE_TAGS_RE = re.compile(r'^tags:\s*\[(.*?)\]\s*$', re.M)
BLOCK_TAGS_RE = re.compile(r'^tags:\s*\n((?:\s*-\s+.*\n?)*)', re.M)
REVIEW_RE = re.compile(r'^review:\s*(true|false)\s*$', re.M)
SOURCE_ID_RE = re.compile(r'^source_id:\s*"?(.*?)"?\s*$', re.M)


def split_frontmatter(text: str) -> Tuple[str, str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return '', '', text
    return '---\n', m.group(1), text[m.end():]


def parse_tags_from_tag_line(text: str) -> List[str]:
    m = TAG_LINE_RE.search(text)
    if not m:
        return []
    raw = m.group(1)
    tags = [normalize_tag(part) for part in raw.split(',')]
    return unique([t for t in tags if t])


def parse_frontmatter_tags(frontmatter: str) -> List[str]:
    inline = INLINE_TAGS_RE.search(frontmatter)
    if inline:
        return unique([normalize_tag(x) for x in inline.group(1).split(',') if x.strip()])
    block = BLOCK_TAGS_RE.search(frontmatter)
    if not block:
        return []
    tags = []
    for line in block.group(1).splitlines():
        m = re.match(r'^\s*-\s+(.*)$', line)
        if m:
            tags.append(normalize_tag(m.group(1)))
    return unique(tags)


def normalize_tag(tag: str) -> str:
    t = tag.strip().strip('"\'').lower()
    t = re.sub(r'\s+', '-', t)
    return t


def unique(items: List[str]) -> List[str]:
    out = []
    seen = set()
    for item in items:
        if item and item not in seen:
            out.append(item)
            seen.add(item)
    return out


def get_source_path(frontmatter: str) -> Path | None:
    m = SOURCE_ID_RE.search(frontmatter)
    if not m:
        return None
    value = m.group(1).strip()
    if not value.startswith('inbox/thoughts/'):
        return None
    return ROOT / value


def replace_tags(frontmatter: str, tags: List[str]) -> str:
    tag_text = 'tags: [' + ', '.join(tags) + ']'
    if INLINE_TAGS_RE.search(frontmatter):
        return INLINE_TAGS_RE.sub(tag_text, frontmatter, count=1)
    if BLOCK_TAGS_RE.search(frontmatter):
        return BLOCK_TAGS_RE.sub(tag_text + '\n', frontmatter, count=1)
    lines = frontmatter.splitlines()
    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith('status:'):
            insert_at = idx
            break
    lines.insert(insert_at, tag_text)
    return '\n'.join(lines)


def ensure_review(frontmatter: str) -> str:
    if REVIEW_RE.search(frontmatter):
        return REVIEW_RE.sub('review: true', frontmatter, count=1)
    lines = frontmatter.splitlines()
    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith('status:'):
            insert_at = idx
            break
    lines.insert(insert_at, 'review: true')
    return '\n'.join(lines)


def strip_body_tag_line(body: str) -> str:
    return TAG_LINE_RE.sub('', body).replace('\n\n\n', '\n\n')


def process_note(path: Path, apply: bool = False) -> dict:
    text = path.read_text()
    prefix, frontmatter, body = split_frontmatter(text)
    if not frontmatter:
        return {'path': str(path.relative_to(ROOT)), 'status': 'no-frontmatter', 'tags': []}

    current_tags = parse_frontmatter_tags(frontmatter)

    if current_tags:
        return {'path': str(path.relative_to(ROOT)), 'status': 'already-tagged', 'tags': current_tags}

    tags = parse_tags_from_tag_line(body)
    source_path = get_source_path(frontmatter)
    source_rel = None
    if source_path and source_path.exists():
        source_rel = str(source_path.relative_to(ROOT))
        source_tags = parse_tags_from_tag_line(source_path.read_text())
        tags = unique(tags + source_tags)

    fallback = False
    if not tags:
        tags = ['thoughts']
        fallback = True

    status = 'would-fix-fallback' if fallback else 'would-fix'
    if apply:
        updated_frontmatter = replace_tags(frontmatter, tags)
        if fallback:
            updated_frontmatter = ensure_review(updated_frontmatter)
        updated_body = strip_body_tag_line(body)
        path.write_text(prefix + updated_frontmatter + '\n---\n' + updated_body)
        status = 'fixed-fallback' if fallback else 'fixed'

    return {
        'path': str(path.relative_to(ROOT)),
        'status': status,
        'tags': tags,
        'source': source_rel,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--report', type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    results = []
    for path in sorted(THINKING_DIR.glob('*.md')):
        results.append(process_note(path, apply=args.apply))

    fixed = [r for r in results if r['status'].startswith('fixed')]
    fallback = [r for r in results if 'fallback' in r['status']]
    already = [r for r in results if r['status'] == 'already-tagged']

    lines = [
        '# Thought tag normalization',
        '',
        f'- Apply mode: {args.apply}',
        f'- Thinking notes scanned: {len(results)}',
        f'- Fixed: {len(fixed)}',
        f'- Fallback-tagged (`thoughts` + `review: true`): {len(fallback)}',
        f'- Already tagged: {len(already)}',
        '',
        '## Results',
        '',
    ]
    for item in results:
        lines.append(f"- `{item['path']}` — {item['status']} — tags: `{', '.join(item['tags']) if item['tags'] else '(none)'}`")
        if item.get('source'):
            lines.append(f"  - source: `{item['source']}`")
    args.report.write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
