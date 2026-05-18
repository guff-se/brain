# Content kinds

Canonical values for the `kind:` frontmatter field. Adding a new kind requires: this entry, a folder under `sources/`, an entry in `pipelines.md`, and a template under `templates/`.

## The four registers (mandatory `register:` field on every `sources/` note)

| Register | Where it lives | What it is | Agent rule |
|---|---|---|---|
| `voice` | `sources/mine/voice/` | Polished, user's literal language: scripts, talks, finished texts | Quote verbatim only; never paraphrase |
| `thinking` | `sources/mine/thinking/` | Topical reasoning in bullets/fragments; user's view, unfinished | Can expand toward voice with explicit user approval |
| `facts` | `sources/mine/facts/` | Meeting notes, plans, info-capture | Reference only; does NOT ground concept synthesis |
| `consumed` | `sources/consumed/<kind>/` | External material — articles, books, podcasts, clippings | Attribution mandatory; never paraphrase as user's view |

**Register is determined by content, not by source.** A pasted article in Apple Notes is `register: consumed`. A talk script in Evernote is `register: voice`.

## Kinds × landing folders

| kind | party | landing folder | typical register | longform? | notes |
|---|---|---|---|---|---|
| `note` | first | `sources/mine/{voice,thinking,facts}/` | one of those three | no | catch-all for personal notes; register is required |
| `podcast-episode` | first | `sources/mine/podcasts/` | `voice` | yes | your own podcast recordings; transcript in `_longform/` |
| `conversation` | first | `sources/mine/conversations/` | `thinking` or `facts` | yes | chats/voice memos you participated in |
| `article` | third | `sources/consumed/articles/` | `consumed` | optional | external articles (Pocket, web reads) |
| `clipping` | third | `sources/consumed/clippings/` | `consumed` | no | saved quote/excerpt from external content; not a full article |
| `podcast-episode` | third | `sources/consumed/podcasts/` | `consumed` | yes | podcasts you listened to |
| `book` | third | `sources/consumed/books/` | `consumed` | yes | books you read; highlights in `_longform/` |
| `video` | third | `sources/consumed/videos/` | `consumed` | optional | videos you watched |
| `person` | — | `sources/people/` | — | no | entity pages, one per person referenced ≥2× |
| `concept` | — | `wiki/concepts/` | — | no | compiled atomic ideas (`provenance: inferred`) |
| `map` | — | `wiki/maps/` | — | no | Maps of Content |
| `project` | first | `projects/` | — | no | active outcomes |
| `area` | first | `areas/` | — | no | ongoing life areas |
| `daily` | first | `daily/` | — | no | `YYYY-MM-DD.md` daily notes |
