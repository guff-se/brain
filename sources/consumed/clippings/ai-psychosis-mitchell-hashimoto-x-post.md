---
title: "AI psychosis"
summary: "Mitchell Hashimoto beskriver hur hela företag kan hamna i ett slags AI-psykos: lokal optimering, snabb återhämtning och fina mätvärden används för att rättfärdiga system som blir allt mer obegripliga och sköra."
kind: clipping
party: third
register: consumed
source: web
source_id: "https://xcancel.com/mitchellh/status/2055380239711457578"
provenance: extracted
url: "https://xcancel.com/mitchellh/status/2055380239711457578"
author: "Mitchell Hashimoto"
tags: [ai, ai-psychosis]
status: reference
ingested: 2026-05-24
created: 2026-05-15
updated: 2026-05-15
---

“I strongly believe there are entire companies right now under heavy AI psychosis and its impossible to have rational conversations about it with them. I can't name any specific people because they include personal friends I deeply respect, but I worry about how this plays out.

I lived through the great MTBF vs MTTR (mean-time-between-failure vs. mean-time-to-recovery) reckoning of infrastructure during the transition to cloud and cloud automation. All those arguments are rearing their ugly heads again but now its... the whole software development industry (maybe the whole world, really). It's frightening, because the psychosis folks operate under an almost absolute \"MTTR is all you need\" mentality: \"its fine to ship bugs because the agents will fix them so quickly and at a scale humans can't do!\"

We learned in infrastructure that MTTR is great but you can't yeet resilient systems entirely.

The main issue is I don't even know how to bring this up to people I know personally, because bringing this topic up leads to immediately dismissals like \"no no, it has full test coverage\" or \"bug reports are going down\" or something, which just don't paint the whole picture.

We already learned this lesson once in infrastructure: you can automate yourself into a very resilient catastrophe machine. Systems can appear healthy by local metrics while globally becoming incomprehensible. Bug reports can go down while latent risk explodes. Test coverage can rise while semantic understanding falls. Changes happens so fast that nobody notices the underlying architecture decaying. I worry.”
