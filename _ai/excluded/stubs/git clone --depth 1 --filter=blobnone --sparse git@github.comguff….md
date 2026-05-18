---
title: "git clone --depth 1 --filter=blobnone --sparse git@github.comguff…"
source: apple-notes
source_id: "iCloud/git clone --depth 1 --filter=blobnone --sparse git@github.comguff….md"
provenance: extracted
ingested: 2026-05-13
status: reference
register: stub
kind: note
party: first
tags: [code]
reclassified: 2026-05-18
classify_reason: "git command snippet"
classify_confidence: high
---

git clone --depth 1 --filter=blob:none --sparse git@github.com:guff-se/andetag-data.git  
cd andetag-data  
git sparse-checkout set cli  
cd cli  
npm install  
npm run build
