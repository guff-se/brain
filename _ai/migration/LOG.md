# Activity Log — ARCHIVED

> Migration complete 2026-05-18. Future entries belong in `../sessions/` (per-session logs), not here.

Reverse-chronological. One line per decision or milestone. Newest first.

## 2026-05-18 — closeout
- Migration and Phase 8 register-classification declared complete.
- Project folder converted to archival status. README, PLAN, LOG headers updated to mark it as a historical record.
- Live vault at `/Users/gustaf/Library/CloudStorage/Dropbox/GustafAI/Obsidian/`. Future work happens there, driven by the agent constitution in `CLAUDE.md`.
- Open items handed off to ongoing agent operation: (1) compile initial `wiki/concepts/` under the 2-source rule; (2) review 139 tag candidates; (3) review 269 stubs; (4) ingest the ~70 podcast transcripts when ready; (5) extract ENEX attachments if/when needed.

## 2026-05-13
- Project kicked off. Created README, PLAN, INVENTORY, VAULT_DESIGN, LOG.
- Reviewed best-practice articles: Stefan Imhoff's agentic Obsidian workflow, Obsidian Importer docs, Jordan Crawford's Evernote→Obsidian write-up.
- User replaced previous Apple Notes exports with a fresh one in `export 260513/` (Notes/ + iCloud/). Older `apple notes/` and `notes export/` folders removed.
- User clarified: migrated Evernote → Apple Notes at some point, so **Apple Notes is the newer source** for any overlap. Source priority flipped to **Apple Notes > Evernote**.
- Confirmed the doubled-lines bug is also present in the fresh iCloud export → within-file dedupe is a mandatory step, not a one-off cleanup.
- iCloud account ≈ superset of "On My Mac" by filename (117/117 overlap); contents may still differ per file.
- User clarified the vault's purpose: **external brain for thoughts and research**. To-do lists, packing lists, contact fragments and filename-stub notes are out of scope — quarantined to `staging/_excluded/` for review, not deleted.
- Pocket highlights decision: inline as `## Highlights` blockquotes in the note body (keeps frontmatter scalar-only).
- iCloud-vs-Notes tie-break decision: iCloud canonical; fall back to `Notes/` copy when iCloud has the doubled-lines bug.
- Phase 1 inventory script run. Real counts: Evernote 100 notes + 52 attachments (2010–2023); Apple Notes iCloud 197 (Notes/ 117 is a strict subset by filename); Pocket 366 bookmarks (361 unread, 10-year span). Doubled-lines bug affects ~30% of Apple Notes files in both accounts.
- **Vault design overhauled** to follow 2026 best practices for AI-managed vaults (Karpathy LLM-Wiki, Foundry pattern, Imhoff CLAUDE.md). Key shifts from a classic PARA setup: layered `inbox/` → `sources/` → `wiki/` curation, claim provenance in frontmatter (`extracted`/`inferred`/`ambiguous`), 2-source rule for concept promotion, controlled tag taxonomy in `_meta/taxonomy.md`, `.manifest.json` for delta-ingest, `_ai/sessions/` folder for agent run logs, CLAUDE.md + SOUL.md as agent constitution. See [VAULT_DESIGN.md](VAULT_DESIGN.md) for full spec and source links.
- **Vault location decided**: `../Obsidian` (i.e. `/Users/gustaf/Library/CloudStorage/Dropbox/GustafAI/Obsidian`). Migration folder stays as a workshop; Obsidian opens against the vault folder.
- **Long-term framing locked in**: user will feed continuous content (70+ own podcast transcripts, articles read, podcasts listened to, books, conversations). Design extended with per-kind `inbox/` subfolders, `_longform/` for transcript bodies, `kind:` + `party:` frontmatter fields, per-kind capture pipelines, additional agent skills.
- **`mine/` vs `consumed/` made the top-level axis of `sources/`** per user request. Distinction lifts from frontmatter into the filesystem so it's unmissable. Folder layout: `sources/mine/{notes,podcasts,conversations}`, `sources/consumed/{articles,podcasts,books,videos}`, `sources/people/` (neutral), `sources/_longform/` (shared). Agent writing rules differ per side (table in VAULT_DESIGN.md).
- Vault skeleton created at `/Users/gustaf/Library/CloudStorage/Dropbox/GustafAI/Obsidian/` with `inbox/`, `sources/`, `wiki/`, `projects/`, `areas/`, `archive/`, `daily/`, `_meta/`, `_ai/`, `_originals/`. Seeded `README.md`, `_meta/content-kinds.md`, `_meta/pipelines.md`, `_meta/taxonomy.md`, empty `.manifest.json`.
- **Phase 3 conversions revised after user added two more ENEX files** (`Entreprenörsjakten.enex`, `Privat.enex`). Original `My Notes.enex` was a partial export — Privat alone has 812 notes. Total Evernote parsed across 3 files: 1014. After intra-Evernote + cross-source dedupe: **801 unique Evernote notes** remain in migration. `convert_enex.py` now accepts multiple `.enex` files and tags each note with `evernote_notebook:` frontmatter.
- **Phase 4 dedupe revised**: title normalization now strips macOS NFD AND collision suffixes (`(1)`, `(2)`). 59 dedupe groups, 166 losers moved to `_ai/excluded/duplicates/`. 1 near-miss remaining.
- **Phase 5 done**: 35/65 Pocket stubs enriched (24 original URL, 11 Wayback), 30 truly dead links retained as `enrichment: failed` stubs with CSV metadata intact.
- **Phase 6 done**: 1347 notes routed from `inbox/_migration/` into `sources/mine/notes/` (981) and `sources/consumed/articles/` (366). Built `_meta/taxonomy.md` (224 unique tags, kebab-case, NFD-stripped, sorted by frequency). All Pocket tags normalized in-place. 1026 untagged notes (the Apple+Evernote imports) listed in `_ai/reports/untagged-2026-05-13.md` for incremental agent tagging. `.manifest.json` populated with ingest ledger.
- **Phase 7 done**: Wrote `vault/CLAUDE.md` (agent constitution, 8 sections: who/where/how/each-session/never/skills/migration-context/tone) and `vault/SOUL.md` (capture and voice rules). Ran lint — 1347 notes scanned, 0 missing frontmatter, 0 missing required fields, 0 tags outside taxonomy, 52 empty-body stragglers (non-blocking), 30 enrichment-failed Pocket stubs (known dead links). `_originals/` left as a pointer to project folder to avoid duplicating 380 MB of exports in Dropbox.
- **Migration complete.** Vault at `/Users/gustaf/Library/CloudStorage/Dropbox/GustafAI/Obsidian/` is ready to open in Obsidian. Project folder remains as scripts + docs archive.
- **Design revision (2026-05-13, post-migration):** user pointed out two errors in the Phase 6 routing:
  1. Source ≠ party. Apple Notes and Evernote contain both mine and consumed material — articles, quotes, and clippings were pasted alongside original thought. Auto-classifying all of them as `mine/` is wrong.
  2. Within "mine", there are meaningfully different registers: **voice** (polished, my-language — scripts, talks, published texts), **thinking** (bullet-form topical reasoning), **facts** (meeting notes, plans, info-capture). Each warrants different agent behavior.
- Introduced the **four-register model** (voice / thinking / facts / consumed) as a first-class concept. Encoded both at folder level (`sources/mine/{voice,thinking,facts}/`, `sources/consumed/clippings/`) and in a required `register:` frontmatter field. Updated `VAULT_DESIGN.md`, `vault/CLAUDE.md`, `vault/SOUL.md`, `vault/_meta/content-kinds.md`.
- New folders created (empty, ready): `sources/mine/{voice,thinking,facts}/`, `sources/consumed/clippings/`. Old `sources/mine/notes/` still holds the 981 unclassified imports — to be re-routed in Phase 8 (next).
- **Phase 8 heuristic pass:** routed 428/981 with a feature-scoring heuristic. Conservative — 553 ended up in `_ai/excluded/uncategorized/`. Spot-check showed real notes stuck there.
- **Phase 8 LLM pass (six parallel Claude Code sub-agents):** processed all 980 remaining notes (553 uncategorized + 427 already-routed-needing-tags). Each sub-agent read its batch JSON + taxonomy, output strict JSON decisions. Total: ~1.5M tokens across 6 sub-agents, ~145s each, fit within one Pro 5h window.
- **LLM apply pass routed:** 147 voice / 236 thinking / 294 facts / 6 consumed-clipping / 3 consumed-article / 206 stub. Plus 88 register conflicts where the LLM disagreed with the heuristic on already-routed files — all flagged with `agent_register_suggestion:` frontmatter, then auto-applied (LLM judgement is consistently better than the heuristic on samples).
- **Tag candidates:** 157 new tags proposed (2-3 per file); 18 auto-promoted to taxonomy at count ≥3 (`andetag`, `entrepreneurship`, `mens-work`, `mkp`, `ikea`, `nordic-mens-work`, etc.). 139 kept in `_meta/_tag_candidates.md` for user review. 6 junk auto-promotions stripped (todo/url/shopping/attachment/codes/consumed — these are register-markers, not topics).
- **Final state after Phase 8:** sources/ holds **1141 classified notes** (165 voice, 248 thinking, 342 facts, 377 consumed articles, 9 consumed clippings). Excluded: 269 stubs + 166 dupes. `_ai/excluded/uncategorized/` is empty. Lint: 0 missing frontmatter, 0 missing required fields. 123 tags outside taxonomy (=the unpromoted candidates, intentional). Migration is finished.
- **Phase 3 conversions complete (original).** All three sources landed in `inbox/_migration/`:
  - Apple Notes: 182 promoted, 15 quarantined. 109 files had the doubled-lines bug (cleaned by collapsing consecutive identical lines).
  - Evernote: 97 promoted, 3 quarantined empties. ENML→Markdown via regex-based converter; created/updated dates preserved.
  - Pocket: all 366 rows materialized; 301 have article bodies from existing reflect_notes; 65 are stubs with `enrichment: pending` for Phase 5.
  - Stub filter tuned after first pass over-excluded real short notes (e.g. "Is the future hopeful"). Now only quarantines on strong signals: UUID/attachment-extension filenames, IMG_*, email-as-filename, todo/packlista title patterns, empty body, single-line contact fragment.
  - Inter-source overlap not yet resolved (Phase 4). Known case: "AI religion" exists in both Apple Notes and Evernote — Evernote copy is cleaner (no doubled lines, original 2022 version).
