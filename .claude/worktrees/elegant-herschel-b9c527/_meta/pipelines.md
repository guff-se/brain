# Capture pipelines

Each content kind has a defined path from raw capture to compiled concept. This is what makes the vault scale: every new piece of input has a known landing slot and a known ingest command.

## article (read on web)
1. Drop URL into `inbox/articles/<slug>.url` (single-line `.url` file containing the URL), OR paste HTML/Markdown into `inbox/articles/<slug>.md`.
2. Agent skill `ingest`: fetches body (Wayback fallback), writes `sources/consumed/articles/<slug>.md` with frontmatter (`kind: article`, `party: third`, `provenance: extracted`, `url`, `author`, `publication`). Long bodies optionally split to `_longform/`.
3. `compile`: ideas crystallized from this article + ≥1 other → `wiki/concepts/`.

## podcast-episode (third-party, listened)
1. Drop transcript (`.md` or `.txt`) into `inbox/podcasts/<slug>.md`. Filename does **not** start with `own-`.
2. `ingest`: full transcript → `_longform/<slug>-transcript.md`. Summary, key claims, guest list → `sources/consumed/podcasts/<slug>.md`. `party: third`.
3. Atomic claims → `wiki/_candidates.md` until a second source corroborates.

## podcast-episode (first-party, your own recordings)
1. Drop transcript into `inbox/podcasts/own-<slug>.md` (prefix `own-` is the routing signal).
2. `ingest`: same split as above, lands in `sources/mine/podcasts/`. `party: first`.
3. Quotable lines become high-confidence wiki contributions (your own voice is authoritative).

## book
1. Drop highlights export into `inbox/books/<title>.md` (Readwise, Kindle, or hand-typed).
2. `ingest`: highlights body → `_longform/highlights-<title>.md`. Metadata + your summary → `sources/consumed/books/<title>.md`. Author and publication-date populated by `enrich`.

## video
1. Drop URL or transcript into `inbox/podcasts/` ... actually `inbox/videos/`? *TBD when first video arrives — kept off the active list for now*.

## conversation
1. Drop transcript or voice memo + transcript into `inbox/conversations/<date>-<topic>.md`.
2. `ingest`: same shape as podcasts. `party: first`.

## thought (quick capture)
1. Drop into `inbox/thoughts/YYYY-MM-DD-HHMM.md` (any device, any format, anytime).
2. Weekly: agent batches recent thoughts, drafts cleaned-up versions in `sources/mine/notes/`, links related concepts. User reviews before promotion.

---

## Operating rhythm (for the agent)

- **On every ingest**: update `.manifest.json` with source hash + produced page list.
- **End of each day**: write a session log to `_ai/sessions/YYYY-MM-DD-HHMM.md`.
- **Weekly (`synthesize-weekly`)**: scan last 7 days of `sources/` and `daily/`, update relevant `wiki/concepts/`, surface new themes in `wiki/_candidates.md`.
- **Monthly**: run `lint` end-to-end, prune `_ai/excluded/` after user review, archive stale `projects/`.
