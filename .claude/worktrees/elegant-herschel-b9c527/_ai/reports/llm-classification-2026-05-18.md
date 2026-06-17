# LLM classification — 2026-05-18

Input batches: 980 records
Agent decisions received: 980

## Routing counts
- **facts**: 294
- **thinking**: 236
- **stub**: 206
- **voice**: 147
- **conflict-flagged**: 88
- **consumed-clipping**: 6
- **consumed-article**: 3

## Tag candidates (proposed, count < 3 → review)
Total new tag proposals: 244 (157 unique)
Auto-promoted (count ≥3): 18
  - `andetag` × 14
  - `entrepreneurship` × 9
  - `consumed` × 8
  - `mens-work` × 7
  - `mkp` × 7
  - `ikea` × 5
  - `codes` × 5
  - `attachment` × 4
  - `nordic-mens-work` × 4
  - `todo` × 3
  - `strawbees` × 3
  - `url` × 3
  - `shopping` × 3
  - `crypto` × 3
  - `podcast` × 3
  - `mkpnordic` × 3
  - `exploring-tech` × 3
  - `bookkeeping` × 3
Candidates kept for review: 139 (in `_meta/_tag_candidates.md`)

## Register conflicts (agent disagrees with prior classification)
88 files flagged. Frontmatter has `agent_register_suggestion:` for inspection.

- `sources/mine/thinking/Playing for change.md`: was **thinking**, agent says **facts** — _application form template fields_
- `sources/mine/thinking/akavia.md`: was **thinking**, agent says **facts** — _meeting prep notes for Akavia AI lecture_
- `sources/mine/thinking/Anteckningar Leonard, 15 12.md`: was **thinking**, agent says **facts** — _meeting notes dated, action items_
- `sources/mine/voice/There are cemeteries that are lonely,.md`: was **voice**, agent says **consumed** — _Neruda poem, external_
- `sources/mine/voice/föreläsning anteckningar insikter.md`: was **voice**, agent says **thinking** — _quotes and insights fragmentary, not polished_
- `sources/mine/thinking/received through your own NWTA..md`: was **thinking**, agent says **consumed** — _external MKP NWTA event description_
- `sources/mine/facts/Metaverse.md`: was **facts**, agent says **thinking** — _lecture brainstorm bullets on metaverse_
- `sources/mine/thinking/Skype med Niklas, 23 10.md`: was **thinking**, agent says **facts** — _dated Skype call notes_
- `sources/mine/thinking/Rim till Elsa & Tilda.md`: was **thinking**, agent says **voice** — _polished rhyming Christmas poem_
- `sources/mine/thinking/Bekk telemark.md`: was **thinking**, agent says **facts** — _client prep notes for Bekk lecture_
- `sources/mine/thinking/Mamma 70.md`: was **thinking**, agent says **voice** — _birthday greeting rhymed message_
- `sources/mine/thinking/tomra - kite.md`: was **thinking**, agent says **facts** — _Tomra lecture prep notes_
- `sources/mine/thinking/UC föreläsning.md`: was **thinking**, agent says **facts** — _UC lecture prep notes_
- `sources/mine/thinking/findwise - katarina.md`: was **thinking**, agent says **facts** — _Findwise lecture prep notes_
- `sources/mine/thinking/NineYards Daniel Fredrik.md`: was **thinking**, agent says **facts** — _NineYards client prep bullets_
- `sources/mine/thinking/1012 sprint.md`: was **thinking**, agent says **facts** — _dated sprint meeting bullets_
- `sources/mine/thinking/Pernilla, Riksutställningar.md`: was **thinking**, agent says **facts** — _meeting fragment with name in title_
- `sources/mine/thinking/Agenda 13 8.md`: was **thinking**, agent says **facts** — _dated agenda bullets_
- `sources/mine/thinking/Curry’s Birmingham.md`: was **thinking**, agent says **facts** — _event planning notes with schedule_
- `sources/mine/thinking/Decom notes.md`: was **thinking**, agent says **facts** — _event planning schedule_
- `sources/mine/thinking/Framtiden är i dig.md`: was **thinking**, agent says **voice** — _polished poem for Ebba_
- `sources/mine/voice/Tim Minchin.md`: was **voice**, agent says **consumed** — _Tim Minchin speech transcript pasted_
- `sources/mine/thinking/Förslag till Strategiworkshop, Innvationskontoret.md`: was **thinking**, agent says **voice** — _polished proposal prose for workshop_
- `sources/mine/thinking/Skype med Niklas.md`: was **thinking**, agent says **facts** — _meeting notes with Niklas about Sydney_
- `sources/mine/thinking/YEoS Dagordning 100527.md`: was **thinking**, agent says **facts** — _dated agenda for board meeting_
- `sources/mine/thinking/skola beksrivning föreläsning.md`: was **thinking**, agent says **voice** — _polished talk description prose_
- `sources/mine/thinking/Projektdagbok.md`: was **thinking**, agent says **facts** — _dated project diary entries_
- `sources/mine/thinking/Slottet Lejfjord.md`: was **thinking**, agent says **facts** — _client meeting notes Slottet_
- `sources/mine/thinking/The little you inside of me..md`: was **thinking**, agent says **voice** — _polished poem_
- `sources/mine/thinking/Reflektioner sprint 3.md`: was **thinking**, agent says **facts** — _sprint reflections task list_
- `sources/mine/thinking/They live in you.md`: was **thinking**, agent says **consumed** — _Lion King song lyrics pasted_
- `sources/mine/thinking/Sinnernas Bjudning.md`: was **thinking**, agent says **facts** — _checklist for sensory party_
- `sources/mine/thinking/🎖Awarded keynote speaker with 10 years of experience and over 400….md`: was **thinking**, agent says **voice** — _polished bio paragraph_
- `sources/mine/thinking/helsingborg skola ing-marie.md`: was **thinking**, agent says **facts** — _talk prep notes for school audience_
- `sources/mine/thinking/Andrum notes.md`: was **thinking**, agent says **facts** — _todo bullets and contacts_
- `sources/mine/thinking/Inför Solidmakarna.md`: was **thinking**, agent says **facts** — _meeting prep bullets_
- `sources/mine/thinking/Protokoll, IK 131028.md`: was **thinking**, agent says **facts** — _meeting protocol bullets_
- `sources/mine/voice/Ted presentation nites.md`: was **voice**, agent says **thinking** — _fragmentary feedback notes_
- `sources/mine/voice/Why we are polarized.md`: was **voice**, agent says **thinking** — _mixed quote and reflections_
- `sources/mine/thinking/Volontärer, Stockholm.md`: was **thinking**, agent says **facts** — _volunteer contact list_
- `sources/mine/thinking/Konrad,.md`: was **thinking**, agent says **voice** — _personal letter to friend_
- `sources/mine/thinking/Notes, Telia, Connect2Business.md`: was **thinking**, agent says **facts** — _meeting notes with dates_
- `sources/mine/thinking/Invite text, The Pirate Bay.md`: was **thinking**, agent says **voice** — _polished invite text_
- `sources/mine/thinking/Alumndagen.md`: was **thinking**, agent says **facts** — _event agenda_
- `sources/mine/thinking/Manus, Federley hangout.md`: was **thinking**, agent says **facts** — _hangout agenda_
- `sources/mine/thinking/Ramböll Matilda.md`: was **thinking**, agent says **facts** — _client meeting notes for Ramboll workshop_
- `sources/mine/thinking/Kampanjsöndagar med Fredrick.md`: was **thinking**, agent says **facts** — _campaign agenda with dates and action points_
- `sources/mine/thinking/Klevfors Oslo - Elköp - Elgiganten.md`: was **thinking**, agent says **facts** — _client meeting notes Elkop/Elgiganten_
- `sources/mine/thinking/San Fran, Resa.md`: was **thinking**, agent says **facts** — _trip planning logistics SF_
- `sources/mine/thinking/Script for Prezi.md`: was **thinking**, agent says **voice** — _first-person Prezi script bio_