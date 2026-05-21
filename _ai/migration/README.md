# Obsidian Migration — archived

> **This folder is the historical record of a one-time migration completed 2026-05-18.**
> It lives inside the vault at `_ai/migration/`. The live operating manual is `../../CLAUDE.md`.
> The raw export files and conversion scripts that performed the migration are not retained — the vault is the artifact.

## What this was

A bootstrap project that consolidated Gustaf's notes from Evernote, Apple Notes, and Pocket into a clean Obsidian vault designed for continuous AI-managed curation. See [PLAN.md](PLAN.md) for the full 8-phase plan, [LOG.md](LOG.md) for the decision log, and [VAULT_DESIGN.md](VAULT_DESIGN.md) for the design rationale.

## What landed in the vault

**1,141 classified notes** in `../../sources/`:

| folder | count | meaning |
|---|---:|---|
| `mine/voice/` | 165 | polished prose in Gustaf's language |
| `mine/thinking/` | 248 | topical reasoning, bullet/fragment |
| `mine/facts/` | 342 | meeting notes, plans, info-capture |
| `consumed/articles/` | 377 | external articles (Pocket + LLM-identified pastes) |
| `consumed/clippings/` | 9 | short external excerpts |

Plus quarantine (never deleted, traceable): 269 stubs, 166 dedupe losers.

The vault has its own `CLAUDE.md` (agent constitution), `SOUL.md` (capture rules), `_meta/taxonomy.md` (controlled tag vocabulary), `.manifest.json` (ingest ledger), and `_ai/` working folders (sessions, reports, excluded). All conventions are documented inside the vault.

## What's in this folder

- `PLAN.md` — the 8 phases, marked done
- `LOG.md` — every decision and revision
- `INVENTORY.md` — what each source contained
- `VAULT_DESIGN.md` — design rationale with 2026-era AI-vault citations

The raw exports (Evernote `.enex` files, Apple Notes `export 260513/`, `Pocket Data Export/`) and the Python conversion scripts are not retained — Gustaf has the exports backed up elsewhere, and the scripts were one-shot tools for the migration. If a future ENEX or similar import is needed, write a fresh ingest under `inbox/_migration/` (or extend the `/ingest` skill).

## If you're an agent reading this

The migration is done. Operate from `../../CLAUDE.md` and check `../sessions/` for the latest session log. This folder explains *why* the vault is shaped the way it is — read `VAULT_DESIGN.md` if you need design rationale, `LOG.md` if you need to know when/why a decision was made.

The *normal* operating mode is via the vault's `/ingest`, `/compile`, `/lint` skills. A new one-time import (e.g. another ENEX dump) would need fresh scripting — the original migration scripts are not retained.

## If you're Gustaf, returning

Open the vault folder in Obsidian. Start a Claude Code session inside it. Say "read CLAUDE.md, then suggest what to do this session". The agent will pick up from where the migration left off — and if it needs context for *why* something is the way it is, this folder is where to look.
