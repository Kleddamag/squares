---
type: is
id: is-01m41d7mmrmyb877fgfqpq2ve3
title: "Results table: fit the significance column in the 1280 width budget"
kind: task
status: open
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T17:33:18.872Z
updated_at: 2026-10-03T23:41:38.074Z
---
Adding the S column put the table 111px past its 1200px frame at 1280 (floors: S 121, result 288). Win the room back by measurement (a compact mark; the result column's floor to its widest formula piece, 248.5px) and update the column tests' pinned widths.

## Notes

Resumed after the sub-agent stopped at a usage limit with its work committed (be33790fe, 3b8974b82). After #315's second merge with main, two results' tenth evidence links set the details column 6.3px wider and the floors 4.3 past 1200 at 1280; the result floor went to 16.55rem and the S padding to 0.2rem, floors 1197.9, 2.1 to spare (577ccf2cd). State 2026-10-03 23:40 UTC: in jlevy/squares#330 at c8b03f91d, stacked on #315 (base claude/amazing-bohr-ytjim9); hosted CI running; push gate passes but for the two sandbox-only tests. Reviewed by a strong-tier agent (think-uer5, one blocking finding fixed). Closes when #330 merges, after #315.


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
