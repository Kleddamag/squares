---
type: is
id: is-01m41gv134xbbtnamrd9nn94x9
title: "Merge main (PRs 292 and 311) into PR 305: renumber to T-080..T-084 and reconcile the floors"
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - session-169
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-03T18:36:19.940Z
updated_at: 2026-10-03T20:45:45.701Z
---
Main merged jlevy/squares#292 and #311 on 2026-10-03 (228 commits): T-066..T-079 are now wand125's rectangle-density and mixed-cover certificates (replayed at coverage one; s(59) = 8, s(77) = 9, and floors from n = 19 to 105) and two s(12) bounds, none resting on Nagamochi; main also added a generated Verification Code section to all 324 case records. PR 305 conflicts in 67 files (46 case records). Done so far: this branch's results renumbered T-066..T-070 -> T-080..T-084 (commit ff4157988, held on local branch hold/renumber-t080 until the merge, since alone it breaks the register's contiguity). Lane E (Opus, max effort) merges: T-007 stays V0; each case takes the strongest verified floor, never Nagamochi's; both sides' dated prose kept and adjusted where superseded; T-084 is superseded at n = 37 (6.44, T-069) and n = 61 (s(61) = 8) and stays registered by the register's precedent; generated views regenerated; counts re-derived; re-pin alone if needed.

## Notes

2026-10-03 20:55 (import coordinator) Register-id collision warning: main now holds T-080 (wand125 linear n101-105, #320) and T-081 (Daniel's s(k^2-4)=k, #322), and open PR #324 claims T-082 (wand125's 22 mixed certificates of 3 October). PR 305 cannot use T-080..T-082; renumber from the first id free on main at its merge (T-083 if #324 lands first).
