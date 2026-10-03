---
type: is
id: is-01m3z64p1mx8yrv14xk2e77xz2
title: "Capture pilot 2: lift the live-row cap per the capture-after-pilot review (lane C1)"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:53.101Z
updated_at: 2026-10-03T04:55:36.228Z
---
Session 168. Pilot 1 (cea300a4) met the capture falsifier (position g=1.000), but review-2026-10-02-n17-capture-after-pilot.md (3f90fc2d) finds it producer-limited by the 24 live-row cap. Pilot 2: max-live 128/256, all live rows bisected to 2^-22, end-angle core, hull cap 48, per-side bounds, widest-row/extent ratio, n11 case-438 contraction control. Falsifier: 3 rounds with widest row < 1/20 of extent and no two-sided extent falling 10%. In-flight uncommitted edits to packing/devtools/pilot_n17_capture.py and its test; runs and receipts in the session scratchpad lanes/c1/p2. Next: integrate receipts into X048-session-168-pilots, record per-round g, decide the capture route.

## Notes

2026-10-03 05:00 UTC. 128 rows (box1024, tool 85e8d2ab): 13 rounds, 208 certified updates, endpoint control held; worst two-sided position extent stays 2*rho (g = 1.000) every round; only one-sided wall movement, frozen since round 10. Widest-row-to-extent ratio max stuck at 0.200 (side-N2, tilted, angle range ~0.03 rad), so the review's 1/20 falsifier is undecidable at this cap; ~512 rows needed. Cost at the cap ~155 CPU-s per update, ~42 min per round. 256-row run started 04:54 from round 0 (checkpoint refused across the 841e368dd kernel digest change), 3-hour ceiling. Capture is angular-resolution and exact-arithmetic bound, so F2's gmpy2 port and X1's Rust checker apply directly.
