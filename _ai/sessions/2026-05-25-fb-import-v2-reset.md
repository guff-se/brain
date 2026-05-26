---
title: "Session: Facebook import v2 reset"
summary: "Quarantined v1 FB notes, fixed dual-write routing, tightened length gates and judge rubric."
kind: note
party: first
register: facts
source: agent
provenance: inferred
tags: [migration, facebook]
status: reference
ingested: 2026-05-25
---

## Done

- **Quarantine:** 415 notes → `_ai/excluded/facebook-import-v1/` (mirrors `sources/` layout).
- **Judged cache:** removed 517 `save` verdicts; kept 3190 `skip` + `shared_article`/`consumed` saves.
- **run_log:** archived to `staging/run_log.v1-2026-05-25.jsonl`.
- **Pipeline v2** (`fb_bulk.py`):
  - Dual-write: fetched URL → `consumed/<kind>/`; commentary ≥80 chars → optional `mine/thinking/` with `[[wikilink]]`.
  - Bare link / short commentary: article only, no thinking stub.
  - `own_text`: hard-skip <80 chars; strict LLM <200.
  - Dedupe `main1`/`main2` by `ts` (longer text wins; tie → `main2`).
- **Rubric** (`fb_judge.py`): stricter short-text rules; no “crisp one-liner” auto-save.
- **Tool:** `tools/fb_reset_v1.py` for repeatable rollback.

## Thresholds

| Gate | Chars |
|---|---|
| `own_text` hard skip | < 80 |
| `own_text` strict judge | 80–199 |
| `own_text` normal | ≥ 200 |
| Commentary side-note | ≥ 80 |
| Fetched body for article | ≥ 100 |

## Next

```bash
cd _ai/facebook-import
.venv/bin/python tools/fb_bulk.py --status
.venv/bin/python tools/fb_bulk.py          # or --year 2015 first
```

Skips remain cached — no mass re-judge of skipped items.

## Follow-up

- Spot-check 2015 link shares (Göteborg → full Aftonbladet article in `consumed/articles/`).
- Confirm Universal Music–style posts stay skipped.
