---
type: is
id: is-01m41amwkn2j6r6jh6de7as7fb
title: "Results: a superseded result links the results that supersede it"
kind: epic
status: open
priority: 2
version: 10
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
child_order_hints:
  - is-01m41amx70t1g1zb8r3j2vnjc0
  - is-01m41amxskm37e8b3h76n38sm5
  - is-01m41amybe38g9zssby0xdsx2f
  - is-01m41cpevn6nbaataejd13t6bk
  - is-01m41cpfe7rfkas78e4mvx12aa
created_at: 2026-10-03T16:48:07.280Z
updated_at: 2026-10-03T23:41:03.891Z
---
Owner, 2026-10-03: represent supersession linkages clearly. For a bound, the superseding results are derived from the case records (whatever a case bound rests on now) and shown as links. For a result of another kind, a later result that implies all or part of it is declared in a new register field, superseded_by, checked against the register. T-036 is the first declared one: T-060 (s(11) = T) implies its bound clause, while its equality clause (uniqueness in the six-plus-five family) still stands alone, since T-060 makes no uniqueness claim (n11-optimality-review-article.md).

## Notes

State 2026-10-03 23:40 UTC: in jlevy/squares#315 at 03833707a, merged with main at 0ca18df47; MERGEABLE/CLEAN, 29 checks pass, 28 skipped by design. Reviewed by a strong-tier agent (think-rf21, nothing blocking, findings fixed). No human GitHub review. Closes when #315 merges.


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
