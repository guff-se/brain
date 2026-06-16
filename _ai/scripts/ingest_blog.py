#!/usr/bin/env python3
"""Ingest scraped guff.se blog posts into the vault as first-party `voice` notes.

Reads:
  _ai/import/guff-blog/_scrape_manifest.json   (mechanical: url/title/date/body)
  _ai/import/guff-blog/_ingest_plan.json       (agent judgment: summary/tags/dupes/skip)

For each NEW post: prepend frontmatter to the verbatim body, write to
  sources/mine/voice/<YYYY-MM-DD>-<slug>.md  (body never paraphrased — voice rule).
For each DUPLICATE: enrich the existing voice note with `url:` (idempotent), leave body
  untouched, and let the agent flag it for review (richer published version exists).
SKIP posts are removed from staging without ingest.

Updates .manifest.json with one ingestion record. Deletes staged files after success.

Usage:
  python3 _ai/scripts/ingest_blog.py --apply      # do it
  python3 _ai/scripts/ingest_blog.py              # dry run
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGE = ROOT / "_ai" / "import" / "guff-blog"
VOICE = ROOT / "sources" / "mine" / "voice"
MANIFEST = ROOT / ".manifest.json"
TODAY = "2026-06-16"
AUTHOR = "Gustaf Josefsson"

APPLY = "--apply" in sys.argv


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def strip_header(text):
    """Drop the scrape header; return the verbatim post body."""
    marker = "\n---\n\n"
    i = text.find(marker)
    return text[i + len(marker):].strip() if i != -1 else text.strip()


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def build_frontmatter(title, summary, tags, url, lang, created):
    taglist = ", ".join(tags)
    return (
        "---\n"
        f"title: {yaml_str(title)}\n"
        f"summary: {yaml_str(summary)}\n"
        "kind: note\n"
        "party: first\n"
        "register: voice\n"
        "source: web\n"
        f"source_id: {yaml_str(url)}\n"
        "provenance: extracted\n"
        f"url: {url}\n"
        f"author: {yaml_str(AUTHOR)}\n"
        f"lang: {lang}\n"
        f"tags: [{taglist}]\n"
        "status: reference\n"
        f"ingested: {TODAY}\n"
        f"created: {created}\n"
        "import_source: guff.se-blog\n"
        "---\n\n"
    )


def main():
    scrape = {m["stage_file"]: m for m in load(STAGE / "_scrape_manifest.json")}
    plan = load(STAGE / "_ingest_plan.json")

    produced, enriched, skipped = [], [], []

    # --- NEW posts -> voice notes ---
    for stage_file, meta in plan["new"].items():
        s = scrape[stage_file]
        date = s["date"]
        slug = s["slug"]
        body = strip_header((STAGE / stage_file).read_text(encoding="utf-8"))
        fm = build_frontmatter(s["title"], meta["summary"], meta["tags"],
                               s["url"], meta["lang"], date)
        out_name = f"{date}-{slug}.md"
        out_path = VOICE / out_name
        if out_path.exists():
            print(f"  ! SKIP (exists, would be dup): {out_name}")
            continue
        print(f"  + voice/{out_name}  [{', '.join(meta['tags'])}]")
        if APPLY:
            out_path.write_text(fm + body + "\n", encoding="utf-8")
            (STAGE / stage_file).unlink()
        produced.append(f"sources/mine/voice/{out_name}")

    # --- DUPLICATES -> enrich existing note with url: ---
    for stage_file, existing in plan["duplicates"].items():
        s = scrape[stage_file]
        target = VOICE / existing
        if not target.exists():
            print(f"  ! dup target missing: {existing}")
            continue
        txt = target.read_text(encoding="utf-8")
        if "url:" in txt.split("---", 2)[1] if txt.startswith("---") else False:
            print(f"  = url already present: {existing}")
        else:
            # insert url: right after the opening frontmatter line block (after title)
            new_txt = re.sub(r"(\n)(register:|source:)",
                             rf"\nurl: {s['url']}\g<1>\g<2>", txt, count=1)
            if new_txt == txt:  # fallback: insert after first frontmatter line
                new_txt = txt.replace("---\n", f"---\nurl: {s['url']}\n", 1)
            print(f"  ~ enrich {existing}  (+url: {s['url']})")
            if APPLY:
                target.write_text(new_txt, encoding="utf-8")
        if APPLY:
            (STAGE / stage_file).unlink()
        enriched.append({"note": existing, "url": s["url"], "stage": stage_file})

    # --- SKIP ---
    for stage_file, reason in plan["skip"].items():
        print(f"  x skip {stage_file}: {reason}")
        if APPLY and (STAGE / stage_file).exists():
            (STAGE / stage_file).unlink()
        skipped.append(stage_file)

    # --- manifest ---
    if APPLY:
        man = load(MANIFEST)
        man["last_ingest"] = TODAY
        man["ingestions"].append({
            "ingest_date": TODAY,
            "scope": "guff.se blog import (first-party voice)",
            "sources": ["https://guff.se/en/blog/ (25 posts crawled)"],
            "produced": produced,
            "produced_count": len(produced),
            "enriched_existing": [e["note"] for e in enriched],
            "skipped": skipped,
            "tool": "_ai/scripts/scrape_blog.py + ingest_blog.py",
        })
        MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n{'APPLIED' if APPLY else 'DRY RUN'}: "
          f"{len(produced)} new voice notes, {len(enriched)} enriched, {len(skipped)} skipped.")


if __name__ == "__main__":
    main()
