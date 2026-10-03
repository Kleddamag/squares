---
type: is
id: is-01m3z64sddkyk2qq5vep420mqf
title: Selector finish stage, re-search the 90 flags, then F1 rank-2 residue sweep (lane S2)
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:56.556Z
updated_at: 2026-10-03T05:14:05.357Z
---
Session 168. Q1's residue survey (0e110249) found the selector's L-BFGS-B descent stops at maxiter 600 and polishes only below 1e-4, so flags between 1e-4 and 1e-2 may be false. S2 is adding a finish stage (long descent) to devtools/select_n17_sub_patterns.py, re-searching all 90 flags (arity-6/7/8 receipts) and running the full arity-8 sweep with --restrict-to-survivors 8 (Q1 found an arity-8 north-wall class removing 539 orbits deferred by the missing-pairs subset). Next: commit tool, tests and receipts; recompute projections.

## Notes

2026-10-03 05:25 UTC. Float-search speedup integrated 7581197f2: random-first stage, exact witness cache, early stop, vectorised penalty; verdict-equivalent on 1,608 classes (one old false flag now placed, mask 983968). Placed 4.5x, chunk 1.7x, full queue 26.4 -> 15.6 CPU-hours. Sweep restarted with --levers combined-fast from chunk 59. At 05:05: 29,500 of 423,756 classes, 49 flags, greedy cover 889 of 2,264 residue orbits (39%) in 26 picks; queue 1 done (14 flags), queue 2 hit rate 0.98%. Top flags: south-wall a8 539 orbits (stalls at 64 bins; adaptive rows next), a9 122 orbits pen 9.3e-3 and a9 66 orbits pen 1.3e-2 (queued for K2 at 64 bins). Next for S2: resume-from-screen (exact) and a compiled penalty (numba or extension), numbers first.
