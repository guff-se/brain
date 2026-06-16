#!/usr/bin/env python3
"""Scrape all posts from https://guff.se/en/blog/ into a staging area for LLM ingest.

These are Gustaf's OWN published blog posts → first-party `voice` material.
This script only does the mechanical part (crawl + download + HTML→Markdown).
The classification/frontmatter/dedupe-resolution is done by the agent afterwards.

Output:
  _ai/import/guff-blog/<YYYY-MM-slug>.md   one staged post each (metadata header + body)
  _ai/import/guff-blog/_scrape_manifest.json   list of posts + dedupe candidates

Usage:
  python3 _ai/scripts/scrape_blog.py
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://guff.se/en/blog/"
ROOT = Path(__file__).resolve().parents[2]          # vault root
OUT = ROOT / "_ai" / "import" / "guff-blog"
VOICE = ROOT / "sources" / "mine" / "voice"
POST_RE = re.compile(r"^https?://guff\.se/en/(\d{4})/(\d{2})/([^/]+)/?$")
HEADERS = {"User-Agent": "Mozilla/5.0 (brain-vault blog importer)"}


def get(url, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
        except requests.RequestException as e:
            print(f"  ! {url} attempt {i+1}: {e}", file=sys.stderr)
        time.sleep(2)
    return None


def discover_post_urls():
    """Walk /blog/page/N/ until a page yields no new posts."""
    urls, page = [], 1
    seen = set()
    while True:
        page_url = BASE if page == 1 else f"{BASE}page/{page}/"
        html = get(page_url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        found = []
        for a in soup.find_all("a", href=True):
            href = a["href"].split("#")[0]
            if POST_RE.match(href) and href not in seen:
                seen.add(href)
                found.append(href)
        if not found:
            break
        urls.extend(found)
        print(f"page {page}: +{len(found)} posts (total {len(urls)})")
        page += 1
        time.sleep(1)
    return urls


def html_to_md(html_fragment):
    """Convert an HTML fragment to Markdown via pandoc."""
    p = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
        input=html_fragment, capture_output=True, text=True,
    )
    return p.stdout.strip()


def extract_post(url, html):
    soup = BeautifulSoup(html, "html.parser")
    m = POST_RE.match(url)
    year, month, slug = m.group(1), m.group(2), m.group(3)

    # Title
    title = None
    h1 = soup.find(["h1"], class_=re.compile(r"(entry-title|post-title|title)"))
    if not h1:
        og = soup.find("meta", property="og:title")
        title = og["content"].strip() if og and og.get("content") else None
    else:
        title = h1.get_text(strip=True)
    if not title and soup.title:
        title = soup.title.get_text(strip=True)

    # Date — prefer machine-readable
    date = None
    t = soup.find("time")
    if t and t.get("datetime"):
        date = t["datetime"][:10]
    if not date:
        date = f"{year}-{month}-01"

    # Body container (WordPress)
    body_el = (
        soup.find("div", class_=re.compile(r"entry-content"))
        or soup.find("div", class_=re.compile(r"post-content"))
        or soup.find("article")
    )
    if body_el is None:
        return None
    # strip share buttons / nav / related
    for sel in body_el.find_all(class_=re.compile(
            r"(share|sharedaddy|related|nav|comment|post-tags|jp-relatedposts)")):
        sel.decompose()
    body_md = html_to_md(str(body_el))

    return {
        "url": url, "year": year, "month": month, "slug": slug,
        "title": title or slug, "date": date,
        "stage_name": f"{year}-{month}-{slug}.md",
        "body": body_md,
    }


def existing_voice_index():
    """Normalized title -> filename, for dedupe hints."""
    idx = {}
    for f in VOICE.glob("*.md"):
        norm = re.sub(r"[^a-z0-9]+", "", f.stem.lower())
        idx[norm] = f.name
    return idx


def dedupe_candidate(post, idx):
    """Find a likely existing voice note for this post (title or slug match)."""
    keys = [
        re.sub(r"[^a-z0-9]+", "", post["title"].lower()),
        re.sub(r"[^a-z0-9]+", "", post["slug"].lower().replace("-", "")),
    ]
    for k in keys:
        if not k:
            continue
        for norm, fname in idx.items():
            if k and (k in norm or norm in k) and min(len(k), len(norm)) >= 6:
                return fname
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Discovering post URLs...")
    urls = discover_post_urls()
    print(f"\nFound {len(urls)} posts. Downloading...\n")

    idx = existing_voice_index()
    manifest = []
    for url in urls:
        html = get(url)
        if not html:
            print(f"  ! failed: {url}")
            continue
        post = extract_post(url, html)
        if not post:
            print(f"  ! no body extracted: {url}")
            continue
        dup = dedupe_candidate(post, idx)
        header = (
            f"<!-- SCRAPED BLOG POST — for agent ingest, not final note -->\n"
            f"source_url: {post['url']}\n"
            f"title: {post['title']}\n"
            f"date: {post['date']}\n"
            f"slug: {post['slug']}\n"
            f"possible_existing_note: {dup or 'NONE'}\n\n"
            f"---\n\n"
        )
        (OUT / post["stage_name"]).write_text(header + post["body"] + "\n", encoding="utf-8")
        manifest.append({
            "url": post["url"], "title": post["title"], "date": post["date"],
            "slug": post["slug"], "stage_file": post["stage_name"],
            "word_count": len(post["body"].split()),
            "possible_existing_note": dup,
        })
        flag = f"  ⚠ dup? -> {dup}" if dup else ""
        print(f"  ✓ {post['stage_name']}  ({len(post['body'].split())}w){flag}")
        time.sleep(1)

    (OUT / "_scrape_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    dups = [m for m in manifest if m["possible_existing_note"]]
    print(f"\nDone. {len(manifest)} posts staged in {OUT.relative_to(ROOT)}")
    print(f"{len(dups)} flagged as possible duplicates of existing voice notes.")


if __name__ == "__main__":
    main()
