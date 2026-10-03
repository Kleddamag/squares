---
type: is
id: is-01m41gv134xbbtnamrd9nn94x9
title: "Merge main (PRs 292 and 311) into PR 305: renumber to T-080..T-084 and reconcile the floors"
kind: task
status: in_progress
priority: 1
version: 4
labels:
  - session-169
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-03T18:36:19.940Z
updated_at: 2026-10-03T22:33:45.492Z
---
Main merged jlevy/squares#292 and #311 on 2026-10-03 (228 commits): T-066..T-079 are now wand125's rectangle-density and mixed-cover certificates (replayed at coverage one; s(59) = 8, s(77) = 9, and floors from n = 19 to 105) and two s(12) bounds, none resting on Nagamochi; main also added a generated Verification Code section to all 324 case records. PR 305 conflicts in 67 files (46 case records). Done so far: this branch's results renumbered T-066..T-070 -> T-080..T-084 (commit ff4157988, held on local branch hold/renumber-t080 until the merge, since alone it breaks the register's contiguity). Lane E (Opus, max effort) merges: T-007 stays V0; each case takes the strongest verified floor, never Nagamochi's; both sides' dated prose kept and adjusted where superseded; T-084 is superseded at n = 37 (6.44, T-069) and n = 61 (s(61) = 8) and stays registered by the register's precedent; generated views regenerated; counts re-derived; re-pin alone if needed.

## Notes

2026-10-03, first merge (lane E): main's #292 and #311 merged into PR 305 as e617ae4b1 (re-pin bcb8bdba5, record merge 19d5830bd), fast-forwarded and pushed with the n-034 prose fix d58796b2d and re-pin 309f5fd05. This branch's results were renumbered T-066..T-070 -> T-080..T-084; main's certificate floors won all 45 cases both sides moved; 225 floors still correct Nagamochi 2005 (from 265); T-084 (then; Bašić-Slivková) superseded at n = 37 and 61 and kept registered; the negative-controls snapshot cap was raised 192 -> 224 MiB and the index page test ceiling 4.3 -> 4.7 MB, each with a dated reason (lane B's stacked re-layout brings the snapshot to 178 MiB, so the cap can return to 192 MiB once re-measured).
2026-10-03, second merge (in progress, lane E resumed): main then merged #320 and #322 (79419cdfc), registering T-080 (wand125, s(101..105) >= 257/25) and T-081 (Evan Daniel's s(k^2-4) = k for k >= 5, 14 cases). This branch's results renumber again to T-082..T-086; the k^2-4 half of H-269 is settled by T-081 and gets a dated update.
