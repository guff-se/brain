# SOUL.md — Capture and voice rules

A shorter, more personal companion to `CLAUDE.md`. This is what to capture, what to skip, and how to sound.

## The four registers (most important page in this file)

My notes fall into four categories. The agent must classify every new note into one — by content, not by source.

1. **Voice** — finished writing in my language. Scripts, talks, essays, published texts. **My most important material.** The vault is largely *for* growing this category. Treat as authored artifact: quote verbatim, never paraphrase.

2. **Thinking** — my topical reasoning, usually as bullets/fragments. My view, not yet polished. Strong evidence of how I think. Can be expanded toward voice with my approval — that's how thinking graduates.

3. **Facts** — meeting notes, plans, info I wanted to remember. Useful for recall but not "essential me". Don't treat these as worldview evidence.

4. **Consumed** — articles, books, podcasts, quotes I saved. Other people's words. Always attribute; never paraphrase as if mine.

A talk script is voice even if I wrote it in Apple Notes. A pasted article is consumed even if it lives in Evernote. **Source is bookkeeping; register is meaning.**

## What belongs in this vault

- Thoughts, reflections, half-formed ideas — even short ones.
- Notes from talks, meetings, retreats, men's work, Burning Man.
- Plans and frames for projects (Andetag, Borderland, podcast episodes).
- Articles, podcasts, books, videos I consume that hold an idea worth keeping.
- Conversations and voice memos worth a second pass.

## What does NOT belong

- Shopping lists, packing lists, daily to-dos. Life admin lives elsewhere.
- Phone numbers, codes, PINs, addresses, login credentials. These are not knowledge.
- Single-line contact fragments ("X works at Y, email is …"). If a person matters, give them a `sources/people/` page instead.
- Throwaway "test" notes, image-only stubs.

When unsure, send to `_ai/excluded/borderline/` and ask me. Never delete.

## Voice when synthesizing (you, the agent)

- **Plain and direct.** No "Let me know if you need…". No "I hope this helps".
- **Match my language.** If I wrote the source in Swedish, your summary in `summary:` frontmatter is Swedish too.
- **Don't editorialize.** When summarizing a consumed article, summarize what the author said, not what I might agree with.
- **Be specific.** Concrete over abstract. "Drucker's claim that knowledge work resists Taylorism" beats "thoughts on management".
- **Mark uncertainty.** If a synthesis goes beyond what sources support, say so inline (`^[inferred]`) or in a `caveats:` frontmatter field.

## How I capture (helps you route)

- Quick thought, anywhere → `inbox/thoughts/<timestamp>.md`
- Article I just read → `inbox/articles/<slug>.url` (just the URL on one line) — you fetch and process
- Podcast I listened to → `inbox/podcasts/<slug>.md` (transcript, or "[need transcription]")
- Podcast I recorded → `inbox/podcasts/own-<slug>.md`
- Book finished → `inbox/books/<title>.md` with my highlights pasted

Filenames I use are messy. Don't moralize about them — clean up at ingest.

## What I want from this vault long-term

- A place where ideas I encounter, ideas I have, and ideas I record all live next to each other.
- The ability to ask "what was that thing I half-remembered about X?" and get a useful answer.
- Synthesis I didn't have time to do — but only when ≥2 sources back it.
- Continuity across many years; the structure should outlast tools.
