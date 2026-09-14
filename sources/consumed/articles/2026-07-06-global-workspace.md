---
title: "A global workspace in language models"
summary: "Anthropic presents evidence that Claude has developed a small internal 'J-space' that behaves like a shared workspace for reportable, controllable, multi-step reasoning, while also arguing that this does not establish consciousness."
kind: article
party: third
register: consumed
source: web
source_id: "https://www.anthropic.com/research/global-workspace"
provenance: extracted
url: "https://www.anthropic.com/research/global-workspace"
author: "Anthropic"
enrichment: "Fetched via web"
tags: [ai, consciousness, neuroscience, machine-learning]
status: reference
ingested: 2026-07-07
created: 2026-07-06
updated: 2026-07-06
---

An Anthropic interpretability post arguing that modern language models may have evolved a small internal workspace for deliberate reasoning. The key move is the "J-space": a compact set of neural patterns linked to concepts the model can silently hold in mind, report on, manipulate on request, and use across multiple reasoning steps. Anthropic frames this as an architectural analogy to global workspace theory in neuroscience, not as proof that Claude is conscious.

## Key claims

- Claude appears to have a privileged internal channel, the J-space, whose contents can often be surfaced as concepts or words that are "on its mind" even when they never appear in the output.
- This space seems unusually reportable and controllable: if Claude is asked what it is thinking about, or told to hold a concept in mind while doing something else, the J-space tracks that internal activity more clearly than the rest of the network.
- Anthropic argues the J-space is causally involved in multi-step reasoning rather than merely reflecting it. Swapping intermediate concepts in the space changes downstream answers.
- The same representation can be reused across different tasks, which is the core reason Anthropic likens it to a global workspace or broadcasting hub rather than a narrow task-specific circuit.
- Most fluent language behavior does not seem to depend on this workspace. When Anthropic suppresses the J-space, Claude can still do many automatic tasks, but higher-order reasoning degrades sharply.
- Anthropic explicitly says this does not answer whether Claude is conscious or feels anything. The claim is architectural and interpretability-focused: there is a practically useful internal layer that reveals some silent reasoning.

## Why it matters here

This is a strong primary source for the growing split between "models are just autocomplete" and "models have structured inner cognition." It matters both for consciousness talk and for more practical questions about interpretability, hidden goals, and whether models can privately notice things they do not say. It also pairs naturally with consumed notes that push the other way, especially [[No, Artificial Intelligence Is Not Conscious]], because the article sharpens the distinction between having an internal workspace and being a conscious subject.
