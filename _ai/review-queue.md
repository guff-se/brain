# Review Queue

Items requiring Gustaf's decision. The agent reads this at the start of every session and surfaces open items before doing other work.

**To add an item**: append under `## Open` with a checkbox, file path, reason, date added, and session link.
**To resolve**: move the entry to `## Resolved`, check the box, and note what was done.

---

## Open

- [ ] **4 blog posts already existed as voice notes — published version is richer.** During the guff.se blog import (session [[2026-06-16-1130]]), 4 of 25 posts matched existing Evernote-sourced voice notes. I enriched each existing note with `url:` (safe) but did **not** overwrite the body, per the no-rewrite-voice rule. The scraped published versions contain extra material the Evernote drafts lack (intro lines, correct publish dates). Decide per note whether to restore the published body:
    - `sources/mine/voice/Be different.md` — published version has intro line *"Idag bloggar jag på Gustaf Oscarsons site Nytt Företag…"*; published date 2010-04-27 vs Evernote `created: 2010-05-26`.
    - `sources/mine/voice/Today I did this to save the world..md` — compare against https://guff.se/en/2010/06/today-i-did-this-to-save-the-world/
    - `sources/mine/voice/Superzappare och Gigonomics.md` — compare against https://guff.se/en/2010/02/superzappare-och-gigonomics/
    - `sources/mine/voice/Socialt Entreprenörskap.md` — compare against https://guff.se/en/2010/02/socialt-entreprenorskap/
    - Re-scrapes are staged in `_ai/import/guff-blog/` if you want to diff. Added 2026-06-16, session [[2026-06-16-1130]].
- [ ] **`hello-world` blog post skipped.** WordPress default placeholder ("Welcome to WordPress…"), not real content — not ingested. Note if you actually want it kept. Added 2026-06-16, session [[2026-06-16-1130]].

---

## Resolved

- [x] `sources/consumed/podcasts/2026-02-11-we-didnt-ask-for-this-internet.md` — superseded stub (Facebook import, `source_id: fb-1770812804`), enriched by session [[2026-05-26-1100]] then superseded by transcript-backed ingest in [[2026-05-26-1200]]. Deleted 2026-05-27.
