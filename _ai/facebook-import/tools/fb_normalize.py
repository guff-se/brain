#!/usr/bin/env python3
"""Phase 0: normalize Facebook export into JSONL + stats.

Reads your_facebook_activity/posts/*.json and saved_items/*.json,
fixes the Facebook latin1->utf8 double-encoding, and emits:
  staging/all_posts.jsonl  — one normalized row per post
  staging/stats.md         — human-readable summary
"""
import json, os, datetime, collections, re, sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))            # _ai/facebook-import/tools
PROJECT = os.path.dirname(HERE)                              # _ai/facebook-import
VAULT = os.path.dirname(os.path.dirname(PROJECT))            # vault root
FB = os.path.join(VAULT, 'your_facebook_activity')
OUT = os.path.join(PROJECT, 'staging')
os.makedirs(OUT, exist_ok=True)


def fix_mojibake(s):
    """Repair Facebook's latin1->utf8 double-encoding."""
    if not isinstance(s, str):
        return s
    try:
        return s.encode('latin1').decode('utf8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def walk_fix(obj):
    if isinstance(obj, str):
        return fix_mojibake(obj)
    if isinstance(obj, list):
        return [walk_fix(x) for x in obj]
    if isinstance(obj, dict):
        return {k: walk_fix(v) for k, v in obj.items()}
    return obj


def load(name):
    with open(os.path.join(FB, name)) as f:
        return walk_fix(json.load(f))


def extract_post_text(post):
    text_parts = []
    for d in post.get('data', []) or []:
        if isinstance(d, dict) and 'post' in d:
            text_parts.append(d['post'])
    return '\n\n'.join(text_parts).strip()


def extract_urls(post):
    urls = []
    for att in post.get('attachments', []) or []:
        for d in att.get('data', []) or []:
            ec = d.get('external_context') or {}
            url = ec.get('url')
            if url:
                urls.append({'url': url, 'name': ec.get('name', ''), 'source': ec.get('source', '')})
            media = d.get('media') or {}
            if media.get('uri') and (media.get('uri', '').startswith('http')):
                urls.append({'url': media['uri'], 'name': media.get('title', ''), 'source': ''})
    return urls


def title_pattern(title):
    t = title or ''
    t = re.sub(r'^Gustaf Tadaa\s+', '', t)
    return t[:80]


def length_bucket(n):
    if n == 0: return '0'
    if n < 50: return '1-49'
    if n < 200: return '50-199'
    if n < 500: return '200-499'
    if n < 1500: return '500-1499'
    return '1500+'


def domain_of(url):
    try:
        d = urlparse(url).netloc.lower()
        return d[4:] if d.startswith('www.') else d
    except Exception:
        return ''


def main():
    sources = {
        'main1': 'posts/your_posts__check_ins__photos_and_videos_1.json',
        'main2': 'posts/your_posts__check_ins__photos_and_videos_2.json',
        'archive': 'posts/archive.json',
        'check_ins': 'posts/check-ins.json',
        'other_walls': 'posts/posts_on_other_pages_and_profiles.json',
        'tagged_places': 'posts/places_you_have_been_tagged_in.json',
        'memories_media': 'posts/media_used_for_memories.json',
        'saved': 'saved_items_and_collections/your_saved_items.json',
    }

    rows = []

    def emit(src, post):
        if not isinstance(post, dict):
            return
        ts = post.get('timestamp') or 0
        text = extract_post_text(post)
        urls = extract_urls(post)
        title = post.get('title', '')
        rows.append({
            'src': src,
            'ts': ts,
            'year': datetime.datetime.fromtimestamp(ts).year if ts else None,
            'date': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else None,
            'title': title,
            'title_pattern': title_pattern(title),
            'text': text,
            'len': len(text),
            'bucket': length_bucket(len(text)),
            'urls': urls,
            'n_urls': len(urls),
        })

    for label, path in sources.items():
        full = os.path.join(FB, path)
        if not os.path.exists(full):
            continue
        d = load(path)
        if isinstance(d, list):
            for p in d:
                emit(label, p)
        elif isinstance(d, dict):
            # archive_v2 / saves_v2 / other_photos_v2 / videos_v2
            for k in ('archive_v2', 'saves_v2', 'other_photos_v2', 'videos_v2'):
                if k in d and isinstance(d[k], list):
                    for p in d[k]:
                        emit(label, p)

    # write jsonl
    with open(os.path.join(OUT, 'all_posts.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

    # ---- stats ----
    by_src = collections.Counter(r['src'] for r in rows)
    by_year = collections.Counter(r['year'] for r in rows if r['year'])
    by_bucket = collections.Counter(r['bucket'] for r in rows)
    year_bucket = collections.Counter((r['year'], r['bucket']) for r in rows if r['year'])
    title_patterns = collections.Counter(r['title_pattern'] for r in rows if r['title_pattern'])

    # domain counts (only main + archive + other_walls + saved)
    relevant_for_domains = {'main1', 'main2', 'archive', 'other_walls', 'saved'}
    domain_counts = collections.Counter()
    domain_examples = collections.defaultdict(list)
    for r in rows:
        if r['src'] not in relevant_for_domains:
            continue
        for u in r['urls']:
            d = domain_of(u['url'])
            if not d:
                continue
            domain_counts[d] += 1
            if len(domain_examples[d]) < 3 and u.get('name'):
                domain_examples[d].append(u['name'][:80])

    # commented vs bare shares
    commented_with_link = 0
    bare_link = 0
    text_only = 0
    pure_empty = 0
    for r in rows:
        if r['src'] not in {'main1', 'main2'}:
            continue
        has_text = r['len'] >= 30
        has_url = r['n_urls'] > 0
        if has_text and has_url:
            commented_with_link += 1
        elif has_url and not has_text:
            bare_link += 1
        elif has_text and not has_url:
            text_only += 1
        else:
            pure_empty += 1

    # write stats.md
    lines = []
    lines.append('# Facebook Export — Phase 0 Stats\n')
    lines.append(f'Generated: {datetime.datetime.now().isoformat(timespec="seconds")}\n')
    lines.append('## Row counts per source\n')
    for s, c in sorted(by_src.items(), key=lambda x: -x[1]):
        lines.append(f'- `{s}`: {c}')
    lines.append(f'\n**Total rows normalized:** {len(rows)}\n')

    lines.append('## Year distribution (all sources combined)\n')
    for y in sorted(by_year):
        lines.append(f'- {y}: {by_year[y]}')
    lines.append('')

    lines.append('## Length buckets (all sources)\n')
    order = ['0', '1-49', '50-199', '200-499', '500-1499', '1500+']
    for b in order:
        lines.append(f'- {b}: {by_bucket.get(b, 0)}')
    lines.append('')

    lines.append('## Year × length bucket (main stream only)\n')
    main_rows = [r for r in rows if r['src'] in {'main1', 'main2'}]
    yb_main = collections.Counter((r['year'], r['bucket']) for r in main_rows if r['year'])
    years = sorted({r['year'] for r in main_rows if r['year']})
    lines.append('| year | ' + ' | '.join(order) + ' | total |')
    lines.append('|' + '---|' * (len(order) + 2))
    for y in years:
        row = [str(y)]
        total = 0
        for b in order:
            n = yb_main.get((y, b), 0)
            row.append(str(n))
            total += n
        row.append(str(total))
        lines.append('| ' + ' | '.join(row) + ' |')
    lines.append('')

    lines.append('## Main stream — share patterns\n')
    main_total = sum(1 for r in rows if r['src'] in {'main1', 'main2'})
    lines.append(f'- Total main stream rows: {main_total}')
    lines.append(f'- Commented + linked (text ≥30 chars AND has url): **{commented_with_link}**')
    lines.append(f'- Bare link share (url, no/short text): **{bare_link}**')
    lines.append(f'- Text only (no link): **{text_only}**')
    lines.append(f'- Pure empty (title-only / photo-only): **{pure_empty}**\n')

    lines.append('## Top title patterns (top 25)\n')
    for t, c in title_patterns.most_common(25):
        lines.append(f'- {c}\t`{t}`')
    lines.append('')

    lines.append('## Top 100 shared domains\n')
    lines.append(f'Total unique domains: {len(domain_counts)}. Total link shares: {sum(domain_counts.values())}.\n')
    lines.append('| # | domain | shares | sample titles |')
    lines.append('|---|---|---|---|')
    for i, (dom, c) in enumerate(domain_counts.most_common(100), 1):
        ex = ' / '.join(domain_examples[dom][:2]).replace('|', '\\|')
        lines.append(f'| {i} | {dom} | {c} | {ex} |')
    lines.append('')

    lines.append('## Domain shares — distribution\n')
    counts = sorted(domain_counts.values(), reverse=True)
    cutoffs = [1, 2, 3, 5, 10, 20, 50, 100]
    for c in cutoffs:
        n = sum(1 for v in counts if v >= c)
        total_shares = sum(v for v in counts if v >= c)
        lines.append(f'- domains shared ≥{c} times: **{n} domains**, covering {total_shares} link shares')
    lines.append('')

    # mojibake spot check — sample text that contained the smoking-gun sequence pre-fix
    lines.append('## Mojibake repair — sanity check\n')
    sample = next((r['text'] for r in rows if r['len'] > 100 and any(ch in r['text'] for ch in ['ö', 'ä', 'å', 'é'])), '')
    lines.append('A long-text sample after repair (should read as normal Swedish/English):\n')
    lines.append('```')
    lines.append(sample[:400])
    lines.append('```\n')

    with open(os.path.join(OUT, 'stats.md'), 'w') as f:
        f.write('\n'.join(lines))

    print(f'Wrote {len(rows)} rows to staging/all_posts.jsonl')
    print(f'Wrote staging/stats.md')


if __name__ == '__main__':
    main()
