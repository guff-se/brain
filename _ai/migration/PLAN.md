# Migration Plan — ARCHIVED

> **Migration complete 2026-05-18.** All 8 phases done. This file is the historical record, kept in the vault at `_ai/migration/PLAN.md`.
> Ongoing operating manual: `../../CLAUDE.md`. Per-session logs: `../sessions/`.
> Do not extend this plan — open new work as agent sessions, not phases.

---

## Phase 0 — Project setup
**Status:** done (2026-05-13)
- Created project docs (README, PLAN, INVENTORY, VAULT_DESIGN, LOG)
- Identified the four data sources on disk
- Reviewed best-practice articles for Claude-Code-driven Obsidian migrations

## Phase 1 — Deep inventory
**Status:** done (2026-05-13) — see [INVENTORY.md](INVENTORY.md). Raw scan data not retained.
**Goal:** know exactly what's in every source, so dedupe and routing decisions are informed.

Tasks:
1. Parse `My Notes.enex` — count notes, list notebooks/tags, span of `<created>`/`<updated>` timestamps, attachment count and total bytes.
2. Inspect `notes export/` — extract title + first-modified timestamp from each HTML, build a CSV index.
3. Inspect `apple notes/Archive/` and `apple notes/evernote/` — same, plus detect the doubled-line artifact seen in some files (e.g. `AI religion.md`).
4. Inspect `Pocket Data Export/` — count entries per status (unread/archive), how many `reflect_notes` files already exist, overlap with CSV by URL.
5. Write findings into [INVENTORY.md](INVENTORY.md).

**Decision point:** which copy is canonical when titles overlap across sources? Revised rule (user confirmed Evernote→Apple-Notes migration history): **Apple Notes (`export 260513/`) > Evernote (`My Notes.enex`)**. ENEX wins only for notes that never made it into Apple Notes. Within Apple Notes, iCloud account is treated as canonical, with `Notes/` (On My Mac) as a tie-breaker when iCloud has the doubled-lines bug.

## Phase 2 — Vault design
**Status:** pending
**Goal:** lock in the folder structure, frontmatter schema, tag taxonomy in [VAULT_DESIGN.md](VAULT_DESIGN.md). Confirm with user before any large-scale conversion.

## Phase 3 — Convert each source to Markdown (into `vault/inbox/_migration/`)
**Status:** done (2026-05-13). 645 notes promoted to `Obsidian/inbox/_migration/{apple-notes,evernote,pocket}/`, 18 quarantined as stubs. 65 Pocket entries flagged `enrichment: pending` for Phase 5. (Conversion scripts not retained.)

Per the revised design ([VAULT_DESIGN.md](VAULT_DESIGN.md)), all conversions land in `vault/inbox/_migration/<source>/` first. The agent only promotes them to `sources/` in Phase 6 once frontmatter + provenance + dedupe are settled.

| Source | Method | Output |
|---|---|---|
| `My Notes.enex` | Custom Python ENEX parser → MD with full metadata (created/updated/tags/resources) | `vault/inbox/_migration/evernote/` |
| `export 260513/iCloud/` + `Notes/` | Within-file dedupe (collapse doubled paragraphs), pick best per filename, add frontmatter | `vault/inbox/_migration/apple-notes/` |
| Pocket CSV + reflect_notes | Use existing `reflect_notes/` where present; stub for missing | `vault/inbox/_migration/pocket/` |

Every converted file gets `source:` + `source_id:` + `provenance: extracted` from the start.

Each note must end up with YAML frontmatter (see [VAULT_DESIGN.md](VAULT_DESIGN.md)) including `source:` and `source_id:` so we can trace it.

## Phase 4 — Deduplicate
**Status:** done (2026-05-13). 59 dedupe groups, 166 losers moved to `_ai/excluded/duplicates/`. Title key strips macOS NFD and collision suffixes `(1)`/`(2)`. 1 near-miss remains for manual review. Pocket untouched (no overlap with the other two).

1. Group notes by normalized title + creation date proximity.
2. For each group: pick newest by `updated`/`modified` timestamp, fall back to source-priority rule from Phase 1.
3. Quarantine losers in `staging/_duplicates/` (don't delete) until user confirms.
4. Within-file dedupe pass: detect repeating paragraph artifacts and collapse.

## Phase 5 — Enrich Pocket bookmarks
**Status:** done (2026-05-13). Of 65 stubs: 24 fetched from original URL, 11 from Wayback Machine, 30 truly dead (paywalled, deleted, expired X/Twitter redirects). All 30 failed stubs retain their CSV metadata (title/url/tags/date) and `enrichment: failed` for future hand-curation.

For Pocket entries whose `reflect_notes` body is empty or missing:
- Fetch the article (WebFetch); if dead, try `web.archive.org` snapshot.
- Save as Markdown body; flag with `enrichment: archive` or `enrichment: original`.
- Notes that 404 everywhere stay as a stub with `enrichment: failed`.

## Phase 6 — Tag taxonomy + promote inbox → sources + compile wiki concepts
**Status:** routing done (2026-05-13). All 1347 notes routed: 981 to `sources/mine/notes/` (180 Apple + 801 Evernote), 366 to `sources/consumed/articles/` (Pocket). `_meta/taxonomy.md` seeded with 224 unique tags (Pocket-derived). `.manifest.json` populated. 1026 notes have empty `tags: []` — listed in `_ai/reports/untagged-2026-05-13.md` for incremental agent tagging. **Wiki concept compilation deferred to agent operation (post-migration).**

1. **Build `_meta/taxonomy.md`** from existing Pocket tags (366 bookmarks, 150 tags — strong starting signal) + LLM-suggested clusters for the untagged Evernote/Apple notes. 2–3 tags max per note, specific over broad.
2. **Promote** cleaned notes from `vault/inbox/_migration/` into `vault/sources/notes/`, `sources/articles/`, etc., applying the taxonomy.
3. **Compile wiki concepts** — agent scans `sources/` for themes appearing in ≥2 notes (2-source rule), promotes to `wiki/concepts/` with `provenance: inferred` and a `sources_cited:` list. Themes with one source go to `wiki/_candidates.md`.
4. Maps-of-Content for the heaviest topics live in `wiki/maps/`.

## Phase 7 — Final review, agent constitution, hand-off
**Status:** done (2026-05-13). Wrote `vault/CLAUDE.md` (8-section agent constitution) and `vault/SOUL.md` (capture/voice rules). Ran lint pass — 0 frontmatter/field issues, 52 empty-body stragglers logged. `vault/_originals/README.md` points back to project folder rather than duplicating 380 MB of exports.

## Phase 8 — Re-classify by register (voice / thinking / facts / consumed)
**Status:** structure prepared (2026-05-13). Routing pending.

**Why:** Phase 6 routed every Apple Notes and Evernote note into `sources/mine/notes/` — wrong on two counts:
1. Both sources contain consumed material (pasted articles, quotes, clippings) that should be in `consumed/`, not `mine/`.
2. Within "mine", three meaningfully different registers exist (voice, thinking, facts) with different agent rules.

**Done already:**
- VAULT_DESIGN.md, vault/CLAUDE.md, vault/SOUL.md, vault/_meta/content-kinds.md updated with the four-register model.
- New folders created: `sources/mine/{voice,thinking,facts}/`, `sources/consumed/clippings/`.
- New required frontmatter field: `register: voice|thinking|facts|consumed`.

**Done (2026-05-18):**
1. Heuristic pass routed 428/981 with confidence; 553 went to uncategorized.
2. LLM pass via six parallel Claude Code sub-agents covered all 980 remaining files (553 + 427 already-routed needing tags). Strict JSON output per agent.
3. Apply pass routed 692 (voice/thinking/facts/consumed) + 206 stubs + 88 conflict-resolutions.
4. 18 new tags auto-promoted to taxonomy; 139 candidates in `_meta/_tag_candidates.md` for review.
5. `sources/mine/notes/` removed; four-register split fully in place.

**Final tally:** sources/ = **1141 notes** (165 voice / 248 thinking / 342 facts / 377 articles / 9 clippings). Quarantine: 269 stubs + 166 dupes. Lint clean except 123 below-threshold tag candidates (expected).

- Run `lint` pass: orphans, broken `[[wikilinks]]`, missing frontmatter, tags outside taxonomy, contradictions.
- **Write `vault/CLAUDE.md`** — the agent constitution (5 sections per VAULT_DESIGN.md). This is what makes the vault self-managing in future Claude Code sessions.
- **Write `vault/SOUL.md`** — capture rules and voice, drafted from observed patterns in the user's notes.
- **Initialize `.manifest.json`** with the migration ledger (which export produced which pages).
- Verify the vault opens cleanly in Obsidian, install Smart Connections or equivalent for semantic search.
- Move original exports into `vault/_originals/` (read-only).
- Write a one-page `vault/README.md` explaining the layout for future humans.

---

## How we keep this living
- Each phase's **Status** line is updated as work progresses (`pending` → `in progress` → `done (YYYY-MM-DD)`).
- Major decisions (e.g. tag taxonomy, dedupe rules) get a one-line entry in [LOG.md](LOG.md).
- If a phase changes shape mid-way, edit this file rather than carrying a stale plan.
