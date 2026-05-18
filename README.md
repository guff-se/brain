# Gustaf's External Brain

An AI-managed Obsidian vault — long-lived storage for thoughts, research, and consumed content.

## Quick map
- **inbox/** — raw captures. You drop here; the agent never edits.
- **sources/mine/** — your own words: thoughts, podcasts, conversations.
- **sources/consumed/** — other people's content you read/heard/watched.
- **sources/people/** — entity pages, neutral.
- **wiki/** — agent-compiled concept pages (2-source rule).
- **projects/ areas/ archive/ daily/** — PARA layers.
- **_meta/** — taxonomy, content-kinds, pipelines, templates.
- **_ai/** — agent session logs, lint reports, excluded items.
- **_originals/** — raw export files, read-only.

Full design + rationale: see `../obsidian migration/VAULT_DESIGN.md`.

## How to use day-to-day
- Drop an article URL into `inbox/articles/<slug>.url`, run agent's `ingest` skill.
- Drop a podcast transcript into `inbox/podcasts/`, run `ingest`.
- Quick thought? `inbox/thoughts/<timestamp>.md`. Weekly batch into `sources/notes/`.
- Ask the agent to `compile` to grow the wiki, `lint` to keep it healthy.

## Agent
See `CLAUDE.md` (root) for the agent constitution and `SOUL.md` for capture/voice rules. Both are written at the end of the migration (Phase 7).
