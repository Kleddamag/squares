---
type: is
id: is-01m3z64sddkyk2qq5vep420mqf
title: Selector finish stage, re-search the 90 flags, then F1 rank-2 residue sweep (lane S2)
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:56.556Z
updated_at: 2026-10-02T23:03:49.159Z
---
Session 168. Q1's residue survey (0e110249) found the selector's L-BFGS-B descent stops at maxiter 600 and polishes only below 1e-4, so flags between 1e-4 and 1e-2 may be false. S2 is adding a finish stage (long descent) to devtools/select_n17_sub_patterns.py, re-searching all 90 flags (arity-6/7/8 receipts) and running the full arity-8 sweep with --restrict-to-survivors 8 (Q1 found an arity-8 north-wall class removing 539 orbits deferred by the missing-pairs subset). Next: commit tool, tests and receipts; recompute projections.

## Notes

Committed 16ea38d81. Finish stage in the selector (one long L-BFGS-B descent; --no-finish is byte-identical old search). Recheck of 90 flags (seed 1, 6,209 s): 89 hold, 1 false (arity 8, penetration 1.0e-4). Confirmed projection: 17,696 states, 2,264 orbits, endpoint surviving. Rank-2 sweep tool sweep_n17_residue_universe.py: universe 77,359 / 142,140 / 211,812 at arity 8/9/10; queue 423,756. Running detached (PID 7560, one worker) in the session scratchpad lanes/s2/universe; after a restart rerun run-sweep.sh (copy in X048 receipts/residue-universe). First 3,000 classes: 1 flag (south-wall arity 8, corner-SW corner-SE side-S0 side-W0 side-E0 side-S1 side-S2 interior-SW, pen 4.19e-3) covering 539 of 2,264 orbits. Queues 1-3 due around 00:15 UTC. Falsifier (greedy cover < 1,132 orbits) undecided. South-wall flag queued to K2 for certification.
