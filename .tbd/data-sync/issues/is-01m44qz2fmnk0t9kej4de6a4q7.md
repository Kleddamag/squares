---
type: is
id: is-01m44qz2fmnk0t9kej4de6a4q7
title: "Import wand125: mixed rectangle-measure lower bounds of 4 October at 14 counts n = 53, 54, 58, 69, 70, 71, 73, 76, 86, 87, 88, 90, 91, 94 (#282)"
kind: task
status: in_progress
priority: 1
version: 7
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
updated_at: 2026-10-05T01:52:30.408Z
started_at: 2026-10-05T00:48:54.642Z
---
14 comments on #282 (2026-10-04T07:04Z..19:04Z), commits 683264c..797bdf6 of wand125/square-packing-bounds. Stages 1-3: claim map against the record, packet at the last commit, register T-090 at V0, read_through on #282. Replay (stage 4) priced and queued, not run: same verifier as mixed_n84_L940, ~7 CPU-h per certificate.

## Notes

2026-10-05 01:05Z stages 1-3 and 5 (tbd-moderate lane, branch claude/ecstatic-pascal-pothtx-wand125, commits 861a9f258 and 696167be9; not pushed).

Pin: wand125/square-packing-bounds 797bdf6e10eba5f9dccca9da06f8352e81ba9dde (head; committed 2026-10-04T19:03:58Z; ls-remote: one branch, no tags). Nothing after it. Between 8aa6a10 and 797bdf6: 12 certificate commits, plus 3f063bd (k2m4_n77_L9: run logs, full replay record, hardened verify.sh, cover unchanged; evidence update for T-067, #279/#280 review points) and 781afb3 (point_n21_L5: relativized paths, English status messages, lemma-code map fixed, certificate unchanged; evidence update for T-055). Neither is a new claim; both are separate evidence-update imports, not retained here.

Claim map (record before this import -> T-090):
- n53 3051/400 (62ff7b2) > 3043/400 rect_n53_L76075 (T-068 rep, T-074 ver)
- n54 1537/200 (d62b47f) > 3069/400 rect_n54_L76725 (T-068 rep, T-074 ver)
- n58 1587/200 (797bdf6) > 1581/200 mixed_n58_L7905 (T-082); ver 3113/400 (T-074)
- n69 431/50 (8aa6a10) > 2153/250 mixed_n69_L8612 (T-082); ver 1717/200 (T-074)
- n70 3463/400 (4df6bcc) > 3459/400 (T-082); ver 69/8 (T-074)
- n71 8721/1000 (5d09521) > 1741/200 (T-082); ver 1737/200 (T-070)
- n73 8813/1000 (23e75da) > 8809/1000 (T-082); ver 1737/200 (T-070)
- n76 1793/200 (a2cbd0f) > 224/25 (T-082); ver 447/50 (T-072)
- n86 9503/1000 (683264c) > 19/2 (T-082); ver 473/50 (T-075)
- n87 479/50 (98bb266) > 191/20 (T-082); ver 237/25 (T-075)
- n88 481/50 (9a26e8d) > 48/5 (T-082) and the unregistered mixed_n88_L96125 769/80 (8aa6a10 packet); ver 237/25 (T-075)
- n90 973/100 (324c189) > 389/40 (T-082); ver 48/5 (T-069)
- n91 781/80 (02f981a) > 39/4 (T-082); ver 97/10 (T-075)
- n94 199/20 (8a81f65) > 248/25 (T-082) and the unregistered mixed_n94_L994 497/50; ver 1961/200 (T-074)
None carries to n+1 by monotonicity.

Packet: packing/resources/web/wand125-mixed-bounds-evening-2026-10-04 ([wand125 mixed bounds evening 2026-10-04]); retains the 12 new dirs, pins mixed_n69_L862 and mixed_n86_L9503 identical_to the 8aa6a10 packet's copies (they stay registered from that packet; no duplicate audit rows). acquire_source --check: PACKET_MATCHES_ITS_CONTRACT. mixed-audit: all 12 pass; mixed-fetch: all 12 BUNDLE_READY (2.5 min wall, 2 parallel).

Register: T-090 (pre-assigned), V0/C0, S3 draft, scope 14 counts, attribution both keys, published 2026-10-04. check_results fails only on id contiguity until T-088/T-089 merge.

Replay plan (think-wrdq): 153.3 CPU-h planned (136.9 mixed-price x 1.119 observed ratio; 160.9 by the source's own oblique seconds). mixed-shard wand125-mixed-bounds-evening-2026-10-04 --runners 6: 21.0-22.3 CPU-h, ~5.5 wall-h per runner at 4 workers (130.9 CPU-h for the 12); plus n69-L862 0-200 and n86-L9503 0-200 under the 8aa6a10 packet (12.1 + 10.3 = 22.4 CPU-h, ~5.6 wall-h) unless that packet's own replay (think-e6ss/think-wpuu plan r3, r7, r8) runs them. Then two mutated controls (mixed-control) and a separately prompted review for C1.

Open for the coordinator: the 8aa6a10 packet's entry (think-e6ss planned 16) must now scope to its other 14 (oct3-oct4-mixed-14) since T-090 holds n69 and n86. Acknowledgement draft for #282: received 14 certificates (683264c..797bdf6), pinned at 797bdf6, exact premises and pre-replay checks pass, full 201-angle replays and a review queued; no T-NNN until merged.

2026-10-05 01:55Z validation (commits 861a9f258, 696167be9, 805313037 re-pin DATA_REVISION): records tier fails only check_results' id contiguity (T-088/T-089 not on this branch); with T-090 renumbered to T-088 in a scratch worktree check_results and tests/test_results_register.py, test_result_status.py, test_negative_controls (93 tests) pass. Push tier: ruff, basedpyright, edit checks green; browser floor green once packages/workbench/node_modules is linked (worktree bootstrap gap); reachable tests 5038 passed, 11 failed = 6 contiguity-only, 1 data pin (fixed by 805313037), 2 n11_generic_sequential load timeouts (pass alone), 2 fixed_core_packet process-reaping tests that fail on clean main in this container too. check_requests: every id resolves; #282 reply due (oct3-oct4-mixed-14 ack, T-090), #281 no reply due.
