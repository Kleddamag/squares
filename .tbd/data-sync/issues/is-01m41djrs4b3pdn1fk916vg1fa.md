---
type: is
id: is-01m41djrs4b3pdn1fk916vg1fa
title: "Deploy check: every published page carries complete link-preview metadata"
kind: task
status: open
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:39:23.555Z
updated_at: 2026-10-03T23:41:23.389Z
---
Hold every published page to the metadata contract in a test and in check_published_site, so a page added later cannot ship without a preview; forwarders state what they carry by rule.

## Notes

State 2026-10-03 23:40 UTC: in jlevy/squares#319 at 5216f82e8; MERGEABLE/CLEAN, 29 checks pass, 28 skipped by design; merges cleanly into main at 0ca18df47. No review on GitHub and no agent review this session. Closes when #319 merges.


The parent of this bead is:
---
type: is
id: is-01m41d7edgm9wc99zdrkaa5ehy
title: Register links and the results tables' significance column, 2026-10-03 (jlevy/squares#315 and its stacked PR)
kind: epic
status: open
priority: P2
version: 16
labels: []
dependencies: []
child_order_hints:
  - is-01m41amwkn2j6r6jh6de7as7fb
  - is-01m41cpg0dt26sjs7vse6fyc53
  - is-01m41d7k4fe8tbgjcqxejavg5k
  - is-01m41d7kxjyd26rw8smgh96b17
  - is-01m41d7mmrmyb877fgfqpq2ve3
  - is-01m41djpvwrf0tc3tqyp1cnh43
  - is-01m41djqwgbjxhgvqp28w7nedq
  - is-01m41djrs4b3pdn1fk916vg1fa
  - is-01m41dx898hx7y5qajde59hqds
  - is-01m41e7rnk49hg6a6cm8731m5k
  - is-01m4202h72xj9pn4phvcbeqkbm
  - is-01m4202j4rsx4m7ejt42tvxpre
  - is-01m4219scr8whmzt1xxq4kb1pn
  - is-01m421pnn9vr4pfhrmc9dwcs8t
created_at: 2026-10-03T17:33:12.496Z
updated_at: 2026-10-03T23:40:48.365Z
---
The owner's requests of 2026-10-03 afternoon, under one epic: the supersession links (think-xm4t and its children, jlevy/squares#315, with its backfill think-rl2b and gate fixes think-kmi4), and the stacked PR: significance as its own column (think-m3m4), every site colour a named token enforced by a test, the results table bleeding wider on very wide screens, and the 1280 width budget the new column needs.

## Notes

Three PRs: #315 (supersession links, green, clean), #319 (page metadata, green, clean), #330 (significance column, stacked on #315, CI running). Open follow-ups: think-wviw (per-page token declarations), think-ojid (n = 12 reported below verified, main's data).
