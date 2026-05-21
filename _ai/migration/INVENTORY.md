# Source Inventory — ARCHIVED

> Snapshot of the source exports as of the migration. Live vault state: `../../`.

Phase 1 scan complete (2026-05-13). Numbers below are pre-dedupe. The underlying scan output and the script that produced it are no longer retained — this file is the snapshot of record.

## 1. Evernote — three `.enex` exports (2026-05-13)
User discovered `My Notes.enex` (2023) was a partial export. Replaced with:
- `My Notes.enex` — 122 MB, 100 notes (legacy; mostly subset of Privat)
- `Entreprenörsjakten.enex` — 4.5 MB, 102 notes (notebook about a project)
- `Privat.enex` — 255 MB, **812 notes** (the main notebook)
- **Total parsed: 1014**, written 966, excluded 48 stubs.
- After intra-Evernote + cross-source dedupe: **801 unique Evernote notes** in migration.

## 2. Apple Notes — `export 260513/` (exported 2026-05-13)
Two subfolders, one per account:

### 2a. `export 260513/Notes/` — "On My Mac" account
- **117 .md files**, avg 1.6 KB, max 42 KB
- 36 files (31%) show the doubled-lines bug
- 14 files <50 chars (likely excluded as stubs)

### 2b. `export 260513/iCloud/` — iCloud account
- **197 .md files**, avg 1.4 KB, max 42 KB
- 59 files (30%) show the doubled-lines bug
- 18 files <50 chars; 1 UUID-stub; 4 attachment-filename stubs (e.g. `FRIENDSHIP 1.mp4.md`)
- **iCloud is a strict superset by filename**: 117 shared with `Notes/` + 80 unique. `Notes/` has zero unique files.

Implication: `Notes/` is useful only as a tie-breaker for the 117 shared files when iCloud's copy has the doubled-lines bug. Otherwise iCloud is canonical, as decided above.

## 3. Pocket — `Pocket Data Export/`
- `part_000000.csv` — **366 rows** (361 unread, 5 archived)
- Time range: 2015-06-09 → 2025-05-14 (10 years of bookmarking, still active)
- 150 unique tags. Top: `future` (31), `ai` (27), `leadership` (12), `politics` (10), `psychology` (9), `art` (9), `consciousness` (8), `philosophy` (7), `economy` (7), `trends` (6).
- `annotations/part_000000.json` — highlights to inline as `## Highlights`
- `reflect_notes/` — 301 pre-converted `.md` files (article bodies fetched by `toReflect.py`)
- **~65 CSV entries lack a reflect_note** → re-fetch candidates for Phase 5 (try original URL, fall back to Wayback Machine).

## Source priority for dedupe (revised)

Because the user migrated Evernote → Apple Notes once, the **newer copy wins by source**:

1. **Apple Notes (`export 260513/`)** — newest for any note that was migrated
2. **Evernote (`My Notes.enex`)** — only authoritative for notes that never made it to Apple Notes
3. Pocket sits in its own track (bookmarks/articles, no overlap with the other two)

Within Apple Notes, when the same filename exists in both `Notes/` and `iCloud/`:
- Pick the file with fewer duplicated-paragraph artifacts.
- If both clean, prefer `iCloud/` (most recently used surface).

## Overlap matrix

| | Evernote (100) | Notes/ (117) | iCloud/ (197) | Pocket (366) |
|---|---|---|---|---|
| Evernote | — | TBD (Phase 4) | TBD (Phase 4) | none |
| Notes/ | | — | **117/117 subset of iCloud** | none |
| iCloud/ | | | — | none |
| Pocket | | | | — |

Pre-dedupe upper-bound total: 100 + 197 + 366 = **663 notes**. After Apple↔Evernote dedupe and exclusion filter we should land closer to ~500.

## Resolved decisions (2026-05-13)
1. **Apple Notes accounts**: iCloud is canonical. `Notes/` (On My Mac) is consulted only when the iCloud copy has the doubled-lines bug or is otherwise corrupt.
2. **Pocket highlights**: inlined into the note body under a `## Highlights` section, each highlight as a `> blockquote`. Frontmatter stays scalar-only and clean.
3. **Exclusions** (the database is an external brain — thoughts and research, not life admin). Heuristics to filter out into `staging/_excluded/` for user review:
   - Pure to-do / shopping / packing lists (heuristic: title starts with "Fixa", "Att göra", "Packlista", or body is ≥80% bulleted line items with no prose)
   - Contact fragments (whole note is a single email/phone/address line)
   - Filename-stub notes whose title matches `^[0-9a-f-]{8,}$` (UUIDs), or ends in `.mp4`/`.3dm`/`.jpg`/`.png`/`.JPG` etc. with no real content
   - Notes shorter than ~50 chars of prose after stripping markdown/whitespace
   - **All exclusions are quarantined, never deleted.** User reviews `staging/_excluded/` at the end of Phase 4.
