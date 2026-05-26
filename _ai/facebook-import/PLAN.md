---
title: "Facebook Export Ingest Plan"
summary: "How to fold 20 years of Facebook posts (2006–2026) into the vault without drowning the signal."
kind: note
party: first
register: facts
source: manual
source_id: "fb-export-2026-05-22"
provenance: inferred
tags: [migration, facebook]
status: project
ingested: 2026-05-23
created: 2026-05-23
updated: 2026-05-23
---

# Facebook Export Ingest Plan

## 1. What is in `your_facebook_activity/`

### Raw inventory
| File | Rows | Notes |
|---|---|---|
| `posts/your_posts__check_ins__photos_and_videos_1.json` | 10,000 | Main post stream (pt 1) |
| `posts/your_posts__check_ins__photos_and_videos_2.json` | 1,754 | Main post stream (pt 2) |
| `posts/archive.json` | 16 | Archived/hidden posts (often longer, more personal) |
| `posts/check-ins.json` | 68 | Location check-ins |
| `posts/posts_on_other_pages_and_profiles.json` | 87 | Posts on other people's walls / pages |
| `posts/edits_you_made_to_posts.json` | 1,024 | Edit history — meta, not content |
| `posts/your_uncategorized_photos.json` | ? | Photo uploads w/o caption album |
| `posts/your_videos.json` | ? | Video uploads |
| `posts/places_you_have_been_tagged_in.json` | 348 | Tagged-in places |
| `posts/media_used_for_memories.json` | 43 | Auto "memories" media |
| `posts/birthday_media.json` | small | Birthday-wall media |
| `posts/shared_memories.json` | ~empty | |
| `posts/facebook_editor.json` | small | Editor metadata |
| `posts/content_sharing_links_you_have_created.json` | small | Share links generated |
| `posts/your_received_shared_album_invites.json` | small | Album invites |
| `posts/your_sent_shared_album_invites.json` | small | Album invites |
| `saved_items_and_collections/your_saved_items.json` | 54 | Things I bookmarked on FB |
| `saved_items_and_collections/collections.json` | 1 | Collection metadata |

**Main stream total: 11,754 posts spanning 2006–2026.**

### Year distribution (main stream)
2006:19 · 2007:113 · 2008:133 · 2009:466 · 2010:685 · 2011:820 · 2012:706 · 2013:906 · 2014:894 · 2015:1287 · 2016:1582 · 2017:936 · 2018:1153 · 2019:695 · 2020:419 · 2021:306 · 2022:188 · 2023:201 · 2024:111 · 2025:108 · 2026:26

Peak posting 2015–2018 (≈4,950 posts). Falls off sharply after 2020 — Facebook is no longer where Gustaf thinks.

### Signal vs. noise (text length, main stream)
| Bucket | Count | Treatment |
|---|---|---|
| 0 chars (pure share/photo) | 4,648 | **Low signal.** Mostly bare link shares. Skip body-as-note; consider aggregated "share log". |
| 1–49 chars | 1,878 | **Low/medium.** Captions, one-liners, reactions. Keep only if attached to a longer thread. |
| 50–199 chars | 4,078 | **Medium.** Real status updates — most of Gustaf's "online voice" lives here. |
| 200–499 chars | 853 | **High signal.** Mini-essays, opinions. |
| 500–1499 chars | 253 | **High signal.** Essays, rants, manifestos. |
| 1500+ chars | 44 | **Top signal.** Long-form posts — treat almost as authored artifacts. |

So roughly **1,150 long posts** carry most of the worldview signal, **4,000 mediums** carry texture, and **~6,500 short/empty rows** are noise.

### Title patterns (top 15)
- `shared a link.` 5608
- `updated his status.` 1918
- `shared a post.` 1298
- `added a new photo.` 357
- `shared a reel.` 322
- `shared an event.` 285
- `shared a photo.` 168
- `Shared from Instagram` 156
- `Bambuser` 100
- `Facebook for iPhone.` 82
- `shared a link to the group: The Borderland.` 64
- `shared a link to Olle Bjerkås's timeline.` 58
- `shared a group.` 56
- (bare) `Gustaf Tadaa` 52
- `NetworkedBlogs.` 40

### Known data-quality issues
1. **Mojibake.** Facebook double-encodes Latin-1 → UTF-8 (`Ã¶` should be `ö`, `â\x80\x9d` should be `”`). Must be repaired on ingest with `bytes(s, 'latin1').decode('utf8')` (with a try/except fallback).
2. **No raw media in the export folder.** No `posts/media/` directory shipped — only photo *metadata*. Attachments are reference-only (no images to import). Skip photo-only posts entirely.
3. **Edit history is meta.** `edits_you_made_to_posts.json` shows revisions of posts; not a register, not content. Skip for note generation; keep only as a side index if a post's text changed significantly over time.
4. **Title-only posts (297)** = pure action ("shared a reel") with no commentary, no embedded link text. Skip.

---

## 2. Register classification (per CLAUDE.md §3)

Per the four-register model, Facebook posts map roughly:

| FB content shape | Register | Path | Notes |
|---|---|---|---|
| Long original post, ≥200 chars, in Gustaf's voice (essay, manifesto, life update written out) | `voice` | `sources/mine/voice/` | Treat as authored. **Quote verbatim, never paraphrase.** |
| Status update / opinion fragment 50–500 chars | `thinking` | `sources/mine/thinking/` | His view, not yet prose. Strong concept evidence. |
| Check-in / event RSVP / "I'm at X" / pure logistics | `facts` | `sources/mine/facts/` | Reference only. Don't ground concepts on these. |
| Link share **with substantive commentary** | split: commentary as `thinking`; link as `consumed/clippings/` | both | The commentary is his; the link is external. |
| Link share **without commentary** | `consumed/clippings/` (only if link domain is interesting) OR skip | | Bare "shared a link" with no text → almost always skip. |
| Posts on other people's walls (`posts_on_other_pages_and_profiles.json`) | `thinking` if substantive, else skip | | Birthday wishes, "hej" → skip. Substantive comments → keep. |
| Saved items (`your_saved_items.json`) | `consumed/clippings/` | | 54 items — small enough to fully process. |
| Archived posts (`archive.json`) | usually `voice` or `thinking` | | Only 16, all reviewed individually. |

**Heuristic rules for the classifier:**
- text length ≥ 500 → `voice` candidate (human-spot-check before promoting)
- 200 ≤ length < 500 → `thinking`
- 50 ≤ length < 200 → `thinking` if contains opinion verbs / first-person reflection; else `facts`
- length < 50 → skip unless attached to a check-in or event of clear meaning
- attachment is link + no/short text → if link-only, skip; if commentary present, treat commentary as `thinking`

---

## 3. Pipeline — staged, mindful, revertible

The vault has 1,141 notes today. A naive ingest of all 11,754 FB rows would 10× the vault and bury existing signal. We process in **layers, highest signal first**, with explicit Gustaf checkpoints between layers.

### Phase 0 — Prep (no writes to `sources/`)
- [ ] Create `_ai/facebook-import/staging/` for intermediate JSONL.
- [ ] Write `tools/fb_normalize.py`:
  - Load all `posts/*.json`
  - Fix mojibake (`bytes(text,'latin1').decode('utf8','replace')`)
  - Emit one normalized JSONL row per post: `{timestamp, year, text, title, attachments[], length, kind, src_file}`
- [ ] Output `staging/all_posts.jsonl` + a `staging/stats.md` (year × length-bucket matrix, **top 100 shared domains with counts and sample titles**, top mentioned names, count of dead-vs-live links via a fast HEAD pass on a sample).
- [ ] **Checkpoint:** Gustaf eyeballs stats.md and confirms the cutoffs below.

### Phase 1 — Long voice posts (≈44 posts, length ≥ 1500)
- [ ] One note per post in `sources/mine/voice/`.
- [ ] Filename: `YYYY-MM-DD-<slug>.md` where slug = first 6 meaningful words.
- [ ] Frontmatter: `register: voice`, `party: first`, `source: facebook`, `source_id: <fb post id or timestamp>`, `provenance: extracted`.
- [ ] Body: verbatim text. No edits. Wikilinks added only if a clear existing canonical page exists.
- [ ] **Checkpoint:** Gustaf reviews 5 random ones — is `voice` the right register, or should some drop to `thinking`?

### Phase 2 — Medium-long thinking (≈1,106 posts, 200 ≤ length < 1500)
- [ ] One note per post in `sources/mine/thinking/`.
- [ ] Same naming + frontmatter pattern, `register: thinking`.
- [ ] **Checkpoint:** Gustaf reviews a sample after first 100 written; tune length threshold if too noisy.

### Phase 3 — Short thinking (≈4,078 posts, 50–199 chars) — **the hard one**
Two options to choose from at the checkpoint:
- **Option A (per-note):** one note each. Pro: granular, searchable. Con: ~4k notes — risks burying the vault.
- **Option B (year-bundles, recommended):** one note per year, `sources/mine/thinking/YYYY-fb-stream.md`, with each post as a dated bullet. Pro: keeps the vault breathable, easy to skim chronologically. Con: less individually linkable.
- [ ] **Checkpoint:** Gustaf picks A or B before this phase runs.

### Phase 4 — Link shares with commentary (fetch + ingest the linked content)
- [ ] Filter: post has text ≥ 30 chars *and* an external link.
- [ ] **Three-step pattern per item:**
  1. `sources/mine/thinking/YYYY-MM-DD-<slug>.md` — Gustaf's commentary (`register: thinking`, `party: first`). Links to the clipping via `[[wikilink]]`.
  2. **Fetch the linked URL** (live first, Wayback fallback if dead). Extract clean article text/title/author.
  3. `sources/consumed/<kind>/YYYY-MM-DD-<domain>-<slug>.md` (`register: consumed`, `party: third`, `source: web|wayback`, `enrichment: fetched|wayback|failed`). Body holds extracted text or the longform split (see `_meta/content-kinds.md`). Routing by URL shape:
     - article / blog / news domain → `sources/consumed/articles/`
     - YouTube/Vimeo → `sources/consumed/videos/` (transcript later if available)
     - Spotify/podcast → `sources/consumed/podcasts/`
     - book retailer (Adlibris, Amazon, Goodreads) → `sources/consumed/books/`
     - PDF / generic doc → `sources/consumed/clippings/` (excerpt only)
     - dead + no Wayback snapshot → keep as a failed-stub clipping (per existing precedent — see migration stub-handling)
- [ ] **Fetch rules:**
  - Polite: ≥1s/domain delay, retries with backoff, respect robots.
  - Cache raw HTML once under `_ai/facebook-import/staging/fetched/<hash>.html` so re-runs are cheap.
  - Strip boilerplate (use readability-style extraction).
  - Skip fetches to: facebook.com (already in export), known login walls (we'll log them as failed-stubs).
  - Hard rate-limit: max ~50 fetches per minute, configurable.
- [ ] **Checkpoint:** sample 20 → confirm extraction quality and routing rules before bulk fetch.

### Phase 5 — Bare link shares (no commentary, ≈3,500 posts)
Two sub-decisions, **per domain** rather than blanket:
- [ ] **Tier 1 — high-value domains** (substack, longreads, nytimes, dn.se, aftonbladet opinion, academic, personal blogs Gustaf shared from repeatedly): **fetch & ingest** as `consumed/<kind>/` even without commentary. The act of sharing is signal — these are the corpus of what Gustaf read.
- [ ] **Tier 2 — low-value domains** (youtube auto-shares, FB events, viral aggregators, dead promo links): aggregate into one per-year log `sources/consumed/clippings/YYYY-fb-shares.md` with `[date] domain — title — url`.
- [ ] How to draw the line: Phase 0's stats output must include **top 100 shared domains with counts**. Gustaf picks the Tier-1 cutoff at the checkpoint (e.g. "everything ≥5 shares + this manual allow-list" / "everything except this manual block-list").
- [ ] Tier-1 fetches reuse the Phase 4 fetcher and cache.

### Phase 6 — Check-ins, tagged places, events
- [ ] `check-ins.json` (68) → one digest per year: `sources/mine/facts/YYYY-fb-checkins.md` (date, place, city). Useful timeline reference.
- [ ] `places_you_have_been_tagged_in.json` (348) → similar yearly digest, `register: facts`.
- [ ] Event RSVPs / "shared an event" → skip unless commentary present.

### Phase 7 — Saved items (54)
- [ ] One pass through `your_saved_items.json` → `sources/consumed/clippings/` per item (small enough to do individually).
- [ ] Try enrichment.

### Phase 8 — Archive.json (16 posts)
- [ ] Individual review. These are posts Gustaf chose to hide — often personal/political. Default to `voice` if long, else `thinking`.

### Phase 9 — Skip list (explicit, documented)
The following are **not** ingested as notes:
- `edits_you_made_to_posts.json` (meta — edit log only, not content)
- `your_uncategorized_photos.json` / `your_videos.json` / `birthday_media.json` / `media_used_for_memories.json` — no media payload in this export and no captions of value
- `facebook_editor.json`, `content_sharing_links_you_have_created.json`, `*_shared_album_invites.json`, `shared_memories.json` — metadata
- Title-only posts (297) — pure action
- Posts on other walls that are pure greetings ("Grattis!", "Hej")

Skip-list rationale lives here so future-me knows what was excluded and why.

### Phase 10 — Wire into the vault
- [ ] Update `.manifest.json` with every produced page, source-id → file.
- [ ] Update `_meta/pipelines.md` with a new "Facebook export" section (lessons learned).
- [ ] Run `/lint` → fix orphans, tag drift.
- [ ] Run `/compile` over the new corpus — expect a wave of new candidates in `wiki/_candidates.md` (Burning Man, polyamory, entrepreneurship, men's work, andetag, AI all likely to ripen).
- [ ] Final session log under `_ai/sessions/`.

---

## 4. Volume sanity check

Conservative projected note counts:
- Phase 1: ~40 voice notes
- Phase 2: ~1,100 thinking notes
- Phase 3 (Option B recommended): ~21 year-bundle notes; (Option A: ~4,000)
- Phase 4: ~1,500 thinking + ~1,500 consumed notes (commented shares — every commented link fetched and ingested; refine in Phase 0 stats)
- Phase 5: ~500–1,500 Tier-1 consumed notes (high-value bare shares, fetched) + ~21 yearly aggregate logs for Tier-2
- Phase 6: ~40 facts notes
- Phase 7: ~54 clipping notes
- Phase 8: ~16 notes

**Likely total with Option B + link-fetching: ~5,000–6,000 new notes** (vault grows ~5×, dominated by consumed articles). Without link-fetching it would be ~4,250.

**Fetch budget:** ~3,000–5,000 URLs to fetch across Phases 4+5. At polite rates (~50/min, with per-domain throttling and Wayback fallbacks) that is roughly **2–4 hours of background fetch time**, plus cache reuse on re-runs. Worth running as a background task in chunks per year.

Recommendation: Option B for Phase 3 + Phase 5. Vault stays focused on long-form signal; the short stuff is preserved but compressed.

---

## 5. Open questions for Gustaf (decide before Phase 0 runs)

1. **Option A vs Option B for Phase 3 (short statuses)?** — recommend B.
2. **Same for Phase 5 (bare link shares)?** — recommend B (aggregate).
3. **Cutoff for "voice" vs "thinking"?** — current proposal: ≥1500 chars defaults to voice candidate. Lower it?
4. **Language tags.** Many posts are Swedish, some English. Should we add `lang: sv|en|mixed` to frontmatter for FB notes specifically? (Not currently in the frontmatter schema — would be a small extension.)
5. **Posts on other people's walls** — by default we skip pure greetings. OK to drop ~50 trivial "grattis" posts entirely?
6. **Tagged-in places (348)** — keep as one yearly facts digest, or skip entirely? Marginal value.
7. **Privacy.** Some posts may name third parties, exes, family in ways Gustaf wouldn't want indexed forever. Should Phase 1 (voice) require an explicit accept/reject per note before write?
8. **Link-fetch scope for Phase 5 (bare shares).** Tier-1 cutoff: by minimum share count (e.g. ≥3 shares from same domain), by manual allow-list, or both? And any hard block-list (facebook.com is in by default — anything else like specific tabloids)?
9. **Domain → kind routing.** Confirm the URL → `consumed/<kind>/` mapping in Phase 4 (articles vs videos vs podcasts vs books vs clippings). Anything missing?

---

## 6. Suggested first execution session

Run Phase 0 only. Produce `staging/stats.md`. Stop. Let Gustaf read it and answer §5 before any `sources/` writes happen.

---

## 7. Decisions locked after Phase 0 (2026-05-23)

### 7.1 Durability bar (applied across all phases)
Replaces the per-domain Tier-1 cutoff. Every candidate item (post text, linked article, video description) is judged by an LLM against this rubric:

**Save if the content:**
- Contains durable knowledge, ideas, frameworks, or insights that remain useful over time
- Explores causality, mechanisms, patterns, or principles (not just events)
- Shares perspective, analysis, or expertise worth building on
- Could deepen understanding of a topic, domain, or human experience

**Do NOT save if the content:**
- Is primarily a news announcement or time-bound event report
- Is social banter, small talk, or relational exchange with no embedded knowledge
- Describes that something happened without explaining why or what it means
- Is promotional, transactional, or logistical in nature

This rubric is the single gatekeeper. Domain count is no longer the cutoff — the rubric is.

### 7.2 Domain handling (still applies before the rubric)
| Class | Domains | Action |
|---|---|---|
| Skip — forms | docs.google.com (Google Forms), guff.typeform.com, *.typeform.com, forms.gle | Never fetch. Not content. |
| Skip — link shorteners | t.co, bit.ly, buff.ly, goo.gl, wired.trib.al | Resolve to final URL where possible, then judge the destination. Never ingest the shortener itself. |
| Skip — meme/image hosts | imgur.com, i.imgur.com, media1.tenor.co | Never fetch as articles. |
| Skip — own domains | guff.se, theborderland.se, wiki.theborderland.se, talk.theborderland.se, dreams.theborderland.se, entreprenorsjakten.se, imbuedart.com, makerspark.se, incrediblemusicmachine.se | Reference only — treat as `mine/facts/` index entries, not consumed clippings. |
| Route — video | youtube.com, youtu.be, m.youtube.com, vimeo.com | `sources/consumed/videos/` if rubric passes. Metadata only (title, channel, description) for now; transcript later. |
| Route — podcast | open.spotify.com (when an episode), soundcloud.com | `sources/consumed/podcasts/` if rubric passes. |
| Route — book | adlibris.com, bokus.com, amazon (book product), goodreads.com | `sources/consumed/books/`. |
| Default | everything else | `sources/consumed/articles/` if rubric passes. |

### 7.3 Pipeline revised

The per-phase plan above (Phases 1–10) stands, with these overrides:

- **Voice tier (Phase 1, ≥500 chars, ~282 posts):** Manual per-note review. I produce `staging/voice_queue.md` — each candidate post inline with metadata. You mark each: `voice` / `thinking` / `skip` / `private` (= skip). I then write the accepted ones to `sources/mine/{voice,thinking}/`.
- **Medium thinking (Phase 2, 200–499 chars, ~853 posts):** LLM rubric. Pass → individual `sources/mine/thinking/YYYY-MM-DD-<slug>.md`. Fail → year-bundle.
- **Short statuses (Phase 3, 50–199 chars, ~4,065 posts):** LLM rubric. Pass → individual `sources/mine/thinking/YYYY-MM-DD-<slug>.md`. Fail → bullet in `sources/mine/thinking/YYYY-fb-stream.md` (year-bundle, for archaeology). This gives the best of both: durable fragments are individually linkable; banter is preserved but compressed. **Rationale:** I'm the primary reader of this vault — individual notes for everything below the durability bar slows down `/compile` and clutters search; bundles for the non-durable keep the corpus breathable.
- **Link shares (Phases 4+5 merged):** No domain cutoff. For every URL share (with or without commentary):
  1. Apply domain handling rules above.
  2. If not skipped, fetch the URL (live → Wayback fallback).
  3. Apply LLM durability rubric to the fetched content.
  4. If pass: write to the routed `sources/consumed/<kind>/`.
  5. If the Facebook post had commentary ≥30 chars, also write `sources/mine/thinking/YYYY-MM-DD-<slug>.md` linking the clipping (commentary itself also LLM-judged for individual-vs-bundle).
  6. If fail or unfetchable: log to `staging/skipped_urls.jsonl` (not the vault).

### 7.4 New Phase 0.5 — Judge infrastructure
Before Phase 1 runs, build:
- [ ] `tools/fb_fetch.py` — polite URL fetcher with cache (`staging/fetched/<sha1>.html`), Wayback fallback, readability extraction.
- [ ] `tools/fb_judge.py` — LLM batch judge applying the §7.1 rubric. Input: text + optional fetched content. Output: `{verdict: save|skip, register_hint, kind_hint, reason}`. Cached by content hash so re-runs are cheap.
- [ ] `tools/fb_route.py` — given a judged item, write the actual `sources/...md` with frontmatter.
- [ ] Run a 100-item dry-run sample across all categories. Show Gustaf the save/skip decisions. Tune the rubric prompt before bulk.

### 7.5 Revised volume estimate
| Phase | Estimated output |
|---|---|
| 1 (voice, manual) | ~30–80 voice notes after your review |
| 2 (medium, judged) | ~300–500 thinking notes (estimating ~40–60% pass rate) |
| 3 (short, judged + bundle) | ~400–800 individual thinking notes + 21 year-bundle notes |
| 4 (commented shares) | ~1,000–1,500 thinking commentary notes (judged) + ~1,000–2,500 consumed notes (judged) |
| 5 (bare shares) | ~1,000–2,000 consumed notes (judged from ~3,000 raw) |
| 6 (check-ins/places) | ~40 facts digests |
| 7 (saved) | ~20–40 clippings (judged) |
| 8 (archive) | ~10–16 notes |
| **Estimated total** | **~3,000–5,500 new notes** |

Fetch budget: ~6,000 URLs to fetch (after domain skips). Judge budget: ~10,000 LLM calls (every post text + every fetched URL). This is the dominant cost — design `fb_judge.py` to batch aggressively and cache.

### 7.6 Final decisions (2026-05-23 round 2)
- **Execution mode:** run all at once, fully cached. Single long background job. Cache layout: `staging/fetched/<sha1>.html` for raw HTML, `staging/judged/<sha1>.json` for LLM verdicts. Re-runs are free.
- **Voice queue:** one file `staging/voice_queue.md` containing all ~282 candidates as sections. Each section has date, full text, suggested register, and a checkbox line: `[ ] voice  [ ] thinking  [ ] skip  [ ] private`. You edit checkboxes; a parser reads the result and writes notes.
- **Durability rubric scope:** applies to **everything** — own text-only posts, commented shares, bare URL shares, fetched articles. One gatekeeper. Banter → year-bundle; durable → individual note.
- **Frontmatter extension:** add `lang: sv|en|mixed` (auto-detected) to all FB-imported notes. No other schema changes. Provenance lives in existing `source_id` and a new optional `fb_url:` where the export gives us one. (Decision: include `fb_url:` opportunistically — it's free if the export contains it — but don't call it out as a schema commitment.)
- **No `privacy:` field for now.** Private posts get flagged `[ ] private` in the voice queue → skipped entirely, not stored with a flag.

### 7.7 Resume protocol (token limits, crashes, restarts)

The bulk pass is long enough that **token-limit failures or session restarts will happen mid-run.** The system is designed so you only need to say "keep going" and a fresh agent re-runs the same command — anything already done is skipped.

**The durability layer** is on disk, not in agent context:

| Stage | Cache location | Skip rule on re-run |
|---|---|---|
| URL fetch | `staging/fetched_meta/<sha>.json` + `staging/fetched/<sha>.html` | If meta file exists, fetch is skipped. |
| LLM judge | `staging/judged/<sha>.json` | If judged file exists, LLM call is skipped. |
| Vault write | the actual `sources/<register>/<kind>/YYYY-MM-DD-<slug>.md` file | If destination path exists, write is skipped. |
| Progress trail | `staging/run_log.jsonl` (append-only) | One line per item, status=fetched/judged/saved/skipped/error. |

**Atomicity:** all cache writes use tmp + rename (`fb_fetch._save_meta`, `fb_judge._atomic_write_json`). A kill mid-write leaves either the old file or the new file — never a corrupt half. Vault writes will use the same pattern.

**Errors are never cached.** If the LLM judge returns `verdict: "error"` (e.g. token-limit failure, network blip), nothing is written to the judged cache. The next run hits an empty cache slot and retries that item.

**The "keep going" incantation:**
1. New session opens. You say "keep going on the facebook import".
2. I re-read `_ai/facebook-import/PLAN.md` and run `python tools/fb_bulk.py --status` to see what's left.
3. I run `python tools/fb_bulk.py` — the script walks all 12,370 items, skips anything already cached/written, and processes the rest.
4. If interrupted again, repeat.

**What you should NOT do during a bulk run:**
- Don't delete `staging/fetched_meta/`, `staging/judged/`, or `staging/fetched/` mid-run.
- Don't manually edit cache files — only the rubric prompt invalidates them logically, and even then, the script doesn't auto-detect it. To force re-judgment of a subset, delete the matching `staging/judged/<sha>.json` files.

### 7.9 Import v2 reset (2026-05-25)

v1 bulk mis-routed link shares (commentary-only `mine/thinking` stubs, fetched articles dropped). Reset:

1. `tools/fb_reset_v1.py` — quarantine `source: facebook` notes, delete `judged/` **save** entries (keep `skip` + `shared_article`/`consumed` saves), archive `run_log.jsonl`.
2. `fb_bulk.py` v2 — link-share pairing (v2.1): **commentary on a URL → both article+comment save, or neither**; article fail + short comment → skip both; article fail + long comment → standalone thinking only if commentary passes strict rubric; bare link → article only. `own_text` hard-skip <80, strict judge <200; main1/main2 dedupe.
3. Stricter `fb_judge.py` rubric; `pairing_note: paired|standalone` on commentary judges.
4. `fb_purge_link_stubs.py` — quarantine thinking notes with `*Shared link:*` but no `→ [[article]]`.

Re-run: `.venv/bin/python tools/fb_bulk.py` (skips stay cached in `judged/`).

### 7.8 Execution order — what runs next
1. **Phase 0.5 (done 2026-05-23):** built `tools/fb_fetch.py` (with paywall/youtube/spotify fixes), `tools/fb_judge.py` (atomic, resumable), `tools/fb_dryrun.py`. Produced 100-item dry-run + 30-item calibration sample.
2. **Phase 1 voice queue:** generate `staging/voice_queue.md`. Wait for your edits.
3. **Phase 2–5 bulk pass:** run the full fetch + judge + route pipeline as one long background job. Year-by-year progress logged to `staging/run.log`.
4. **Phase 6–8:** check-ins / saved / archive — small batches, run after the bulk.
5. **Phase 10:** wire `.manifest.json`, run `/lint`, run `/compile`, write the session log.
