#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path
from typing import Optional, Tuple

ROOT = Path('/Users/dante/brain')
ARTICLES_DIR = ROOT / 'sources' / 'consumed' / 'articles'
REPORT_PATH = ROOT / '_ai' / 'reports' / 'article-filename-check-latest.md'
FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.S)
FIELD_RE = re.compile(r'^([a-z_]+):[ \t]*(.*?)[ \t]*$', re.M)
DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})$')


def split_frontmatter(text: str) -> Tuple[str, str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return '', '', text
    return '---\n', m.group(1), text[m.end():]


def field(frontmatter: str, name: str) -> Optional[str]:
    for key, value in FIELD_RE.findall(frontmatter):
        if key == name:
            return value.strip().strip('"\'')
    return None


def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'&', ' and ', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-{2,}', '-', text).strip('-')
    return text


def expected_name(path: Path) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    prefix, frontmatter, _ = split_frontmatter(path.read_text())
    if not prefix:
        return None, None, 'missing frontmatter'

    title = field(frontmatter, 'title')
    if not title:
        return None, None, 'missing title'

    date = field(frontmatter, 'published') or field(frontmatter, 'created') or field(frontmatter, 'captured') or field(frontmatter, 'ingested')
    if not date or not DATE_RE.match(date):
        return None, title, 'missing canonical date'

    return f'{date}-{slugify(title)}.md', title, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--report', type=Path, default=REPORT_PATH)
    parser.add_argument('paths', nargs='*', help='optional article paths relative to repo root or absolute')
    args = parser.parse_args()

    if args.paths:
        article_paths = []
        for raw in args.paths:
            p = Path(raw)
            if not p.is_absolute():
                p = ROOT / p
            article_paths.append(p)
    else:
        article_paths = sorted(ARTICLES_DIR.glob('*.md'))

    rows = []
    renamed = 0
    mismatches = 0
    errors = 0

    for path in article_paths:
        expected, title, error = expected_name(path)
        current = path.name
        rel = path.relative_to(ROOT)

        if error:
            errors += 1
            rows.append((str(rel), 'error', error, current, expected or ''))
            continue

        if current == expected:
            rows.append((str(rel), 'ok', title or '', current, expected))
            continue

        mismatches += 1
        rows.append((str(rel), 'mismatch', title or '', current, expected))
        if args.apply:
            target = path.with_name(expected)
            path.rename(target)
            renamed += 1

    lines = [
        '# Article filename check',
        '',
        '- Rule: `sources/consumed/articles/YYYY-MM-DD-slug.md`',
        '- Date precedence: `published` → `created` → `captured` → `ingested`',
        f'- Apply mode: {args.apply}',
        f'- Files scanned: {len(rows)}',
        f'- Mismatches: {mismatches}',
        f'- Renamed: {renamed}',
        f'- Errors: {errors}',
        '',
        '## Results',
        '',
    ]

    for rel, status, detail, current, expected in rows:
        lines.append(f'- `{rel}` — {status}')
        if detail:
            lines.append(f'  - detail: {detail}')
        lines.append(f'  - current: `{current}`')
        if expected:
            lines.append(f'  - expected: `{expected}`')

    args.report.write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
