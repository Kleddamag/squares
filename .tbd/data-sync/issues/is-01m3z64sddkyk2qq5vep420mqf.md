---
type: is
id: is-01m3z64sddkyk2qq5vep420mqf
title: Selector finish stage, re-search the 90 flags, then F1 rank-2 residue sweep (lane S2)
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:56.556Z
updated_at: 2026-10-02T22:46:27.732Z
---
Session 168. Q1's residue survey (0e110249) found the selector's L-BFGS-B descent stops at maxiter 600 and polishes only below 1e-4, so flags between 1e-4 and 1e-2 may be false. S2 is adding a finish stage (long descent) to devtools/select_n17_sub_patterns.py, re-searching all 90 flags (arity-6/7/8 receipts) and running the full arity-8 sweep with --restrict-to-survivors 8 (Q1 found an arity-8 north-wall class removing 539 orbits deferred by the missing-pairs subset). Next: commit tool, tests and receipts; recompute projections.

## Notes

2026-10-02 22:50 UTC. The unfinished finish stage is packing/campaign/explorations/X048-session-168-pilots/handoff/s2/selector-finish-stage-wip.patch (git apply from repo root; clean on 83783ab29). S2 resumed at 22:45 on one worker: finish the stage and re-search the 90 flags, then F1's rank 2, a resumable float sweep of the residue's arity-8-to-10 universe in locality-filtered queue order (about 35 CPU-hours). Falsifier: the flags' greedy cover removes less than half of the 2,256 residue orbits.
