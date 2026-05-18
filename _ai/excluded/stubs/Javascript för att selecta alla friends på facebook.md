---
title: "Javascript för att selecta alla friends på facebook"
source: evernote
source_id: "Privat:812"
evernote_notebook: "Privat"
provenance: extracted
ingested: 2026-05-13
created: 2010-01-28
updated: 2010-01-28
status: reference
register: stub
kind: note
party: first
tags: [code, facebook]
reclassified: 2026-05-18
classify_reason: "JS code snippet only"
classify_confidence: high
---

javascript:elms=document.getElementById('friends').getElementsByTagName('li');for(var fid in elms){if(typeof elms[fid] === 'object'){fs.click(elms[fid]);}}
