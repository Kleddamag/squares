---
type: is
id: is-01m3nqe7r63b3vd9avkf849tfq
title: "frontier/README: external-certificate values for n = 26-31 are stale since 27 September, and the non-trivial gap ordering omits n = 26, 27"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - documentation
  - wand125-update
dependencies: []
parent_id: is-01m3neehm7hq4apdvzg9925738
created_at: 2026-09-29T04:40:47.622Z
updated_at: 2026-09-29T05:11:45.151Z
closed_at: 2026-09-29T05:11:45.151Z
close_reason: Fixed in e80332c0d on claude/magical-davinci-ueqmu1-docs-refresh
resolution: null
duplicate_of: null
---
packing/frontier/README.md 'Complete interval and exact replays add 18 more external-certificate cases: n = 26,27,28 at 1377/250; n = 29,30,31 at 571/100' -> n = 26 at 1377/250, n = 29, 30 at 571/100 (Tokoharu); n = 27, 28 at 28/5 and n = 31 at 148/25 (wand125). 'n = 19 follows n = 11 and n = 17 at 0.0856, then n = 18 at 0.1439' -> n = 27 at 0.1071 and n = 26 at 0.1133 come before n = 18; external certificates now carry 11, 17, 26, 27; wand125's reported bounds stand above 18, 19. Counts and the gap table already moved in 901dbc59. Inventory §3.4 items 4, 10.
