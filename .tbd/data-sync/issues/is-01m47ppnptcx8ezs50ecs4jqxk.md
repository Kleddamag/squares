---
type: is
id: is-01m47ppnptcx8ezs50ecs4jqxk
title: "sqverify-fast census --control: the 99/100 mutant at the least-certified-bound direction can be a true certificate (FC-1); choose by slack or run all directions, then review"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
created_at: 2026-10-06T04:14:15.257Z
updated_at: 2026-10-06T04:14:15.257Z
---
FC-1 of docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-fix-check.md (non-blocking, fails closed). sqverify_fast_census --control runs the 99/100 mutant at one direction, the oblique row with the least min_certified_lower_bound, which on a verified direction is only the branch and bound's termination margin and says nothing about slack. On mixed_n18_L470 (declared net, step 1/1001) that is index 408, where the 99/100 mutant is a true certificate: main's build (d97758bb) verifies it there (least bound 1.0000002639721404), so the receipt is CONTROL_FAILED with captures_agree true (receipt kept, uncommitted, at lane R1's scratchpad r1/recheck/mixed_n18_L470.control.json). The mutant is refused at 230 of 416 directions, each with an exact witness below 1. Lane R2 reports CONTROLS_REFUSED for mixed_n18_L4704 (node 797) and mixed_n19_L48229 (node 198) with the step fix, so this does not block them. Fix proposed by the re-check: keep the near-threshold run at the least-bound leaf; replace the fixed-index 99/100 run by the 99/100 mutant at all directions with --confirm, requiring at least one refusal and an exact witness below 1 (re-evaluated by mixed_exact) at every refused direction, as check_sqverify_fast's declared-net group does at 0.985. A change of control logic: a reviewer must read it before a receipt made with it counts. Also FC-4/FC-6 notes if touched.
