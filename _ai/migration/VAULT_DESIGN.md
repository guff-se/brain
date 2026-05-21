# Vault Design — ARCHIVED design rationale

> This document explains *why* the live vault is shaped the way it is. The vault itself implements the design.
> The operational spec (what agents do daily) is `../../CLAUDE.md`, not this file.
> Edit this only if you're revising the underlying design rationale; otherwise edit `CLAUDE.md`.

**Purpose:** a long-lived external brain that AI agents (Claude Code primarily) continuously curate. Design favors agent operability and growth over human-centric Zettelkasten convention where the two conflict.

**Long-term scope (informs every design choice below):**
- The migration is the *seed*. The vault will grow continuously after.
- Incoming streams the user has flagged: their own podcast transcripts (~70 episodes already), articles read, podcasts listened to, books, conversations — essentially every piece of content consumed or produced.
- Two content tracks: **first-party** (user's own thoughts, podcasts, writing) and **third-party** (articles, others' podcasts, books). Provenance distinguishes them.
- **Source ≠ party.** Apple Notes and Evernote contain BOTH categories — the user pasted articles, quotes, and clippings into notes alongside original thought. Routing must be content-based, not source-based.
- Long-form items (1-hour transcripts ≈ 10k words) cannot be atomic. Pattern: store the full text once, generate atomic notes and a summary from it, link back.

**Four registers** (within `mine/` plus `consumed/`) — each one gets a folder so the agent's writing rules are visible at filesystem level:

| Register | Lives in | What it is | Agent rule |
|---|---|---|---|
| **Voice** | `sources/mine/voice/` | Polished, your-language. Scripts, talks, finished texts. | Quote only; never paraphrase. These are gospel. |
| **Thinking** | `sources/mine/thinking/` | Topical reasoning in bullet/fragment form. Your view, not yet polished. | Can expand or draft toward voice with explicit user approval. Strong evidence for concept synthesis. |
| **Facts** | `sources/mine/facts/` | Meeting notes, plans, info-capture. Things you wanted to remember but aren't "essential you". | Reference material. Searchable, but does not contribute to concept synthesis. |
| **Consumed** | `sources/consumed/<kind>/` | External authors' material. | Attribution mandatory; never paraphrase as user's view. |

Voice + Thinking are the source of the user's worldview. Facts are reference. Consumed is external evidence. Concepts in `wiki/` are strongest when they cite at least one Voice/Thinking note + one Consumed source.

Synthesized 2026-05-13 from:
- [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) — Karpathy LLM-Wiki pattern: provenance, `.manifest.json`, taxonomy
- [jameesy/foundry-vault](https://github.com/jameesy/foundry-vault) — `inbox/` → `sources/` → `wiki/` curation layers
- [Stefan Imhoff's vault](https://www.stefanimhoff.de/agentic-note-taking-obsidian-claude-code/) — `CLAUDE.md` as agent constitution
- [buildmvpfast: Obsidian + Claude AI 2026](https://www.buildmvpfast.com/blog/obsidian-claude-ai-knowledge-management-system-2026)
- [aimaker: Karpathy LLM Wiki + Obsidian](https://aimaker.substack.com/p/llm-wiki-obsidian-knowledge-base-andrej-karphaty)

---

## Folder structure

```
vault/
├── CLAUDE.md                     # Agent constitution: who, where, how, never
├── SOUL.md                       # Capture rules, voice, tag rules
├── .manifest.json                # Ingested-source ledger (path, hash, produced-pages)
│
├── inbox/                        # USER LAYER — raw captures land here, untouched by agent
│   ├── _migration/               # one-time: 2026-05 migration drops
│   ├── articles/                 # paste-URL or fetched articles awaiting ingest
│   ├── podcasts/                 # raw transcripts awaiting ingest
│   ├── books/                    # book highlights/notes awaiting ingest
│   ├── conversations/            # chat/voice transcripts awaiting ingest
│   └── thoughts/                 # quick captures from the user
│
├── sources/                      # AGENT LAYER — cleaned 1:1 records with provenance
│   ├── mine/                     # YOUR material. Always party: first.
│   │   ├── voice/                # polished, your-language: scripts, talks, finished texts
│   │   ├── thinking/             # bullet-form reasoning on topics; your view, unfinished
│   │   ├── facts/                # meeting notes, plans, info-capture
│   │   ├── podcasts/             # your own podcast episodes (transcript in _longform/)
│   │   └── conversations/        # chats/voice memos you participated in
│   │
│   ├── consumed/                 # OTHER PEOPLE's content. Always party: third.
│   │   ├── articles/             # external articles (web, Pocket)
│   │   ├── clippings/            # consumed material saved as a note: quotes, excerpts
│   │   ├── podcasts/             # podcasts you listened to
│   │   ├── books/                # books you read
│   │   └── videos/               # videos you watched
│   │
│   ├── people/                   # entity pages (neutral, referenced from both sides)
│   └── _longform/                # full transcripts/text bodies for items above
│
├── wiki/                         # AGENT LAYER — compiled concepts (2-source rule)
│   ├── concepts/                 # crystallized ideas with backlinks
│   ├── maps/                     # Maps of Content (topic hubs)
│   └── _candidates.md            # themes awaiting 2nd source before promotion
│
├── projects/                     # ACTIVE outcomes with deadlines
├── areas/                        # Ongoing life areas (Andetag, Burning Man, …)
├── archive/                      # Completed/inactive
├── daily/                        # YYYY-MM-DD daily notes
│
├── _meta/
│   ├── taxonomy.md               # controlled tag vocabulary
│   ├── content-kinds.md          # legal values for `kind:` frontmatter field
│   ├── pipelines.md              # how each kind enters the vault (capture → ingest → compile)
│   ├── attachments/              # single attachments folder, hashed names
│   └── templates/                # one template per content kind
│
├── _ai/
│   ├── sessions/                 # session logs: YYYY-MM-DD-HHMM.md, one per agent run
│   ├── reports/                  # audit/lint output, link checks, dedupe reports
│   └── excluded/                 # quarantined notes (to-do lists, stubs) — never deleted
│
└── _originals/                   # raw export files, read-only, traceable provenance
```

**Why `mine/` vs `consumed/` is the top-level split inside `sources/`:** the agent's writing rules differ fundamentally between them, so the boundary must be visible at the filesystem level — not just buried in frontmatter.

| | `mine/voice/` | `mine/thinking/` | `mine/facts/` | `consumed/` |
|---|---|---|---|---|
| Whose words | Gustaf, finished | Gustaf, in-progress | Gustaf, admin | external authors |
| Agent may quote | **verbatim only** | freely | freely | **with attribution** |
| Agent may paraphrase | **no** | yes (toward voice, on approval) | yes | **never as user's view** |
| Used for concept synthesis | strongest evidence | strong evidence | reference only | always cited |
| `party` frontmatter | `first` | `first` | `first` | `third` |
| `register` frontmatter | `voice` | `thinking` | `facts` | `consumed` |
| Provenance | `extracted` | `extracted` | `extracted` | `extracted` (verbatim external) |

A `wiki/concepts/` page typically cites at least one mine/{voice,thinking} source + one consumed source — that's how user thinking meets external research. **Facts are reference material; they don't justify a wiki concept on their own.**

**Notes from Apple Notes / Evernote can land in any of the four buckets.** Source (apple-notes, evernote) is preserved in frontmatter but does NOT determine register. A pasted article from Apple Notes is `consumed/clippings/`. A meeting note is `mine/facts/`. A talk script is `mine/voice/`.

**Why `_longform/` exists**: a 90-minute podcast transcript shouldn't sit in the same scannable folder as a 200-word note. The source record (with summary, key claims, links) stays in `sources/podcasts-own/`, while the full transcript lives in `_longform/`, referenced by `transcript: _longform/2024-03-15-ep42-transcript.md` in the frontmatter.

**Why layered (`inbox/` → `sources/` → `wiki/`):** the agent never edits user-curated input. Inbox is yours. Sources are cleaned 1:1 from inbox. Wiki concepts emerge only when 2+ sources support a theme. This prevents AI from rewriting your own words and prevents speculation from being indistinguishable from your captures.

## Frontmatter schema

Every note has YAML frontmatter. **Bold = required**, italic = optional.

```yaml
---
title: "Cosmo Consulting"
summary: "Notes from a 2022 consulting talk on AI and bureaucratic resistance."
kind: note                     # see _meta/content-kinds.md
party: first                   # first (user-produced) | third (external)
register: thinking             # voice | thinking | facts | consumed — see register table above
created: 2022-09-13
updated: 2026-05-13
ingested: 2026-05-13           # when the agent processed this into the vault
source: apple-notes            # apple-notes | evernote | pocket | own-recording | web | manual | agent
source_id: "iCloud/Cosmo Consulting.md"
provenance: extracted          # extracted | inferred | ambiguous | mixed
tags: [consulting, ai-and-organizations, talks]
status: reference              # project | area | reference | archive | fleeting
# Long-form items only:
transcript: _longform/2024-03-15-ep42-transcript.md
duration_minutes: 67
# External items only:
url: "https://…"
author: "Peter Drucker"
publication: "The Economist"
enrichment: original           # original | archive | failed | none
# Wiki concepts only:
sources_cited: ["sources/notes/cosmo-consulting", "sources/articles/0042-the-next-society"]
---
```

### `kind` values (canonical, lives in `_meta/content-kinds.md`)
`note` · `article` · `clipping` · `podcast-episode` · `book` · `video` · `conversation` · `person` · `concept` · `map` · `project` · `area` · `daily`

### `register` values (the four-way register; required for `sources/mine/*` and `sources/consumed/*`)
`voice` · `thinking` · `facts` · `consumed`

**Provenance is critical.** Apple/Evernote/Pocket imports are always `extracted` (your own words or external article verbatim). AI-synthesized concept pages in `wiki/` are `inferred`. Pages that mix both get `mixed` with inline `^[inferred]` markers on individual sentences (Karpathy pattern).

## Tag conventions

- Defined in `_meta/taxonomy.md`. Agent prefers existing tags over creating new ones.
- Lowercase, kebab-case (`burning-man`, not `BurningMan`).
- **2–3 tags maximum per note.** More tags = less signal.
- Specific subtopics, not broad buckets: `llm-inference` over `ai`, `nordic-mens-work` over `community`.
- New tag requires 3+ notes that justify it; agent proposes via `_meta/_tag_candidates.md` for user review.

## Capture pipelines (the vault must scale to daily new input)

Each content kind has a defined path from capture to compiled concept. Documented in `_meta/pipelines.md`. Sketches:

**Article you read** → drop URL into `inbox/articles/<slug>.url` → `ingest` fetches body, writes `sources/articles/<slug>.md` with `provenance: extracted`, `party: third` → `compile` may produce wiki concepts citing it.

**Podcast you listen to** → drop transcript or RSS link into `inbox/podcasts/` → `ingest` writes full transcript to `_longform/`, summary + key claims to `sources/podcasts/<slug>.md` → atomic claims extracted as inferred wiki candidates (need second source).

**Podcast episode you record** → transcript dropped into `inbox/podcasts/` with filename prefix `own-` → `ingest` routes to `sources/podcasts-own/`, `party: first`. Quotable lines become high-confidence wiki contributions.

**Book you finish** → highlights file into `inbox/books/` → `sources/books/<title>.md` + linked `_longform/highlights-<title>.md`.

**Conversation** → voice memo or chat export into `inbox/conversations/` → ditto.

**Quick thought** → `inbox/thoughts/YYYY-MM-DD-HHMM.md` → batched into `sources/notes/` weekly.

The point: **every new piece of input has a known landing slot and a known ingest command**. Adding a new content type means adding a folder + a pipeline doc + a template + (optionally) extending the agent's `ingest` skill.

## Atomic note rule

- `sources/notes/` and `sources/articles/` notes can be any size (they preserve original captures).
- `wiki/concepts/` pages stay **under 200 words** of body text — one idea per page, links to sources for depth.
- Long thoughts get split into multiple wiki concepts at the agent's discretion during compile.

## The 2-source rule

The agent does not create a `wiki/concepts/` page from a single source. It logs the theme in `wiki/_candidates.md` instead. Only when a second source touches the same theme does the agent compile the concept page. This prevents the wiki from filling with one-off speculation.

## What belongs where (decision tree)

```
Is it a raw capture I just dropped?         → inbox/<kind>/
Is it finished writing in my voice?         → sources/mine/voice/
Is it my topical thinking in bullets?       → sources/mine/thinking/
Is it admin/meeting/info I want kept?       → sources/mine/facts/
Is it my own podcast/conversation?          → sources/mine/{podcasts,conversations}/
Is it external content I consumed?          → sources/consumed/<kind>/
Is it a saved quote/excerpt from elsewhere? → sources/consumed/clippings/
Is it a person I want to track?             → sources/people/
Is it AI-synthesized from ≥2 sources?       → wiki/concepts/
Does it have a deadline and outcome?        → projects/
Is it an ongoing life area?                 → areas/
Is it a stub/to-do/contact fragment?        → _ai/excluded/
Is it the original export file?             → _originals/ (read-only)
```

## What's filtered out (external-brain principle)
Quarantined to `_ai/excluded/` for user review, never deleted:
- Daily/temporary to-do, shopping, packing lists
- Contact fragments (single email/phone/address)
- Filename-stub notes left from attachments (UUID titles, `.mp4`/`.3dm`/`.jpg`)
- Notes with <~50 chars of prose after stripping markdown

## CLAUDE.md (agent constitution)

Lives at vault root. Five sections per [Imhoff](https://www.stefanimhoff.de/agentic-note-taking-obsidian-claude-code/) / [buildmvpfast](https://www.buildmvpfast.com/blog/obsidian-claude-ai-knowledge-management-system-2026):

1. **Who you are** — agent's role, the user's role
2. **Where files live** — folder map (copy of the tree above)
3. **How to write** — frontmatter schema, atomic rule, 2-source rule, tag taxonomy
4. **What to do each session** — start: read latest `_ai/sessions/`, scan `inbox/`. End: write session log, update `.manifest.json`
5. **What you must never do** — edit `inbox/` content, delete from `_ai/excluded/`, create tags outside taxonomy, write `inferred` content without marking it

## SOUL.md (capture and voice rules)

Smaller, more personal. Tone of voice, what *not* to capture, the user's writing patterns. Defines how the agent speaks back when summarizing.

## Filename rules

- `Title Case With Spaces.md` for human notes. Obsidian-friendly, searchable.
- `NNNN_slug.md` (zero-padded) for `sources/articles/` (preserves Pocket reflect_notes ordering).
- Strip filesystem-illegal chars (`/`, `:`, etc.) → space.
- Collisions: dedupe pass picks winner; loser moves to `_ai/excluded/duplicates/`.

## Attachments

- All under `_meta/attachments/`, filename = `YYYYMMDD-<original-name>` to avoid collisions.
- Wikilinks rewritten during conversion.

## Agent skills (defined as slash-commands in `CLAUDE.md`)

Inspired by foundry-vault's pattern, expanded for the long-term content streams:

- `ingest` — promote `inbox/<kind>/` items into `sources/<kind>/` with frontmatter, provenance, and (for long-form) `_longform/` split. Updates `.manifest.json`.
- `compile` — scan `sources/` for recurring themes, promote to `wiki/concepts/` when 2-source rule fires. Single-source themes go to `wiki/_candidates.md`.
- `lint` — orphans, broken links, missing frontmatter, untagged notes, tags outside taxonomy, contradictions.
- `enrich` — re-fetch missing article bodies (Wayback fallback). Pull metadata for `books/`, `podcasts/` (RSS), `people/`.
- `synthesize-weekly` — pass over last 7 days of `sources/`, update relevant wiki concepts, write a synthesis note in `daily/`.
- `transcribe` — (future) accept an audio file, run transcription, route to `inbox/podcasts/`.
