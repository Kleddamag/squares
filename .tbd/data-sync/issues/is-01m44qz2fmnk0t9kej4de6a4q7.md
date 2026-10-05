---
type: is
id: is-01m44qz2fmnk0t9kej4de6a4q7
title: "Import wand125: mixed rectangle-measure lower bounds of 4 October at 14 counts n = 53, 54, 58, 69, 70, 71, 73, 76, 86, 87, 88, 90, 91, 94 (#282)"
kind: task
status: in_progress
priority: 1
version: 8
delegate: claude-code@vm
labels:
  - result-import
dependencies:
  - type: blocks
    target: is-01m44qz4sp4xrmggh6fkwgv2x9
  - type: blocks
    target: is-01m44qz5cez2hhdr2b5p4m1sya
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:38:35.764Z
updated_at: 2026-10-05T02:11:19.636Z
started_at: 2026-10-05T00:48:54.642Z
---
14 comments on #282 (2026-10-04T07:04Z..19:04Z), commits 683264c..797bdf6 of wand125/square-packing-bounds. Stages 1-3: claim map against the record, packet at the last commit, register T-090 at V0, read_through on #282. Replay (stage 4) priced and queued, not run: same verifier as mixed_n84_L940, ~7 CPU-h per certificate.

## Notes

2026-10-05 re-scope (coordinator): this bead's import is now T-091 = the 12 certificates at 797bdf6 (n = 53, 54, 58, 70, 71, 73, 76, 87, 88, 90, 91, 94); n69 L862 and n86 L9503 moved to T-090 (the 16 at 8aa6a10, think-e6ss). Branch claude/ecstatic-pascal-pothtx-wand125, commits 861a9f258 (packet + audit rows + tests), 696167be9 (first registration), 805313037 (re-pin), 905621e8b (T-090/T-091 split), 76e73f5ab (think-aigs updates), d5271d182 (re-pin). Not pushed.

Pin: 797bdf6e10eba5f9dccca9da06f8352e81ba9dde (head, 2026-10-04T19:03:58Z, nothing later). Packet packing/resources/web/wand125-mixed-bounds-evening-2026-10-04, key [wand125 mixed bounds evening 2026-10-04]; acquire_source --check PACKET_MATCHES_ITS_CONTRACT; mixed-audit all 12 pass; mixed-fetch all 12 BUNDLE_READY.

Claim map for T-091 (prior reported value, holder): n53 3051/400 > 3043/400 rect (T-068/T-074); n54 1537/200 > 3069/400 rect (T-068/T-074); n58 1587/200 > 1581/200 (T-082); n70 3463/400 > 3459/400 (T-082); n71 8721/1000 > 1741/200 (T-082); n73 8813/1000 > 8809/1000 (T-082); n76 1793/200 > 224/25 (T-082); n87 479/50 > 191/20 (T-082); n88 481/50 > 769/80 (T-090; T-082 48/5 before); n90 973/100 > 389/40 (T-082); n91 781/80 > 39/4 (T-082); n94 199/20 > 497/50 (T-090; T-082 248/25 before). Margins 0.004-0.03; none carries by monotonicity.

T-091: V0/C0, S3 draft, published 2026-10-04. #282 result oct4-mixed-12 -> T-091. Replay (think-wrdq): 130.8 CPU-h planned (116.9 x 1.119; 137.7 by the source's oblique seconds), mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6 (~21-22 CPU-h, ~5.5 wall-h per runner at 4 workers). Blind review pending: brief at the coordinator.

Validation: records tier fails only on id contiguity (T-088/T-089 on the Kingbird lane); renumbered to T-088/T-089 in a scratch worktree, check_results and 93 register tests pass. See the final report for the push tier.
