---
type: is
id: is-01m474970jceyrnd6gfejksmp5
title: "Import evand (no issue ask): exact certificates as verified ceilings at the 78 counts whose ceiling trails its report (13ee36e)"
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
hold: null
hold_until: null
created_at: 2026-10-05T22:52:19.858Z
updated_at: 2026-10-06T18:07:14.609Z
started_at: 2026-10-06T15:32:07.196Z
---
evand/square-packing 13ee36e (s12/search/exact/batch/certs) certifies 321 of the 324 register records exactly. Issue #375 asks only for the 48 that improve the register (T-098, think-t6ok); the author offers the rest as an independent exact replay of existing upper bounds and asks for nothing. But at all 78 counts where the record's verified upper bound now trails its reported side (after T-098), the source holds a certificate 1e-20 to 1e-14 above the printed side: rounded up at the printed precision it would carry the verified lane to the report, off the integer grid at most of them (by up to 0.464 at n = 101, 122, 145, 170, 197, 226, 257, 290, 291), including 16 counts n <= 100 (28, 29, 37, 39, 41, 50, 51, 53, 54, 55, 69, 70, 71, 83, 87, 88). The packet evand-square-packing-2026-10-05 pins those certificates by digest (only the 48 are retained) and receipts/first-party-check.json and source-replay.json already decide all 320 (n = 17 held, think-x4v4). An import would retain the 78 (about 1.5 MB), register them (one upper-bound entry or an evidence update per the runbook's table), and move the verified lanes through a layer like devtools.apply_exact_optima. Owner decision: whether the record acts on certificates the author did not ask to register.

## Notes

2026-10-06 15:40Z: the owner decided to import (AskUserQuestion answer: '70bh: import 78 ceilings'). Lane R8, worktree /home/user/squares-lanes/r8, branch claude/ecstatic-pascal-pothtx-r8 from 7f2a01816.

2026-10-06 18:20Z, lane R8 done (not pushed; head e1a2b11aa):
- Counts by tool (devtools.apply_exact_ceilings survey, receipts/ceiling-survey.json): of the 272 certificates beside T-098's 48 and the held n = 17, 77 lower the verified ceiling under the T-056/T-088 rule (certified side rounded up at the printed precision): the 78 trailing counts less n = 29, whose interval-certified bound already lies 5e-21 below S'. No other count moves.
- 22 of the 77 now agree with the report; 55 have catalogue closed forms and trail by one unit of the 14th decimal (S' 7.6e-20 to 1.8e-19 above): 49 irrational, 6 rational (n = 50, 171, 198, 230, 261, 293; follow-up think-l8gt).
- Register: new entry T-118 (provisional), V3/C3 derived, confirmed, independently re-implemented; S2 confirmed by the review. T-088 and T-089 drop E-kingbird-upper-register and read as superseded by T-118 (as ceilings).
- Packet: the 77 certificates retained (1.97 MB) from a second clone at 13ee36e, byte for byte the pinned and decided ones; controls --ceilings on all 77 (231 controls, all as expected, 4,696 s wall at two workers).
- Reviews: docs/project/reviews/review-2026-10-06-evand-exact-ceilings.md (defect-open, EC-1 blocking: rational closed forms), fixed; fix check review-2026-10-06-evand-exact-ceilings-fix-check.md (defects-resolved), FC-1..FC-4 handled. Neither reviewer could run the project interpreter.
- Open for the coordinator: T-118 renumbering (check_results contiguity); result-requests.yaml mapping; the negative-controls snapshot cap (base 7f2a01816 already 164 KB over, this branch adds 630 KB).
- n = 17 never read; the scratch clone that held it is deleted.
