---
type: is
id: is-01m3zcv8xq2f9njty9g8dgw4w3
title: Taylor relaxation for the n17 branch and bound, with verifier support (lane P2, F1 rank 4)
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:04.791Z
updated_at: 2026-10-02T23:36:11.127Z
---
Rank 4 of the cost-reduction plan (review section 4.2). Add a first-order Taylor relaxation of the trigonometric coefficients to devtools/pilot_n17_subpattern_bb.py as an option (off = byte-identical certificates), extend verify_n17_bb_certificate.py to re-prove it exactly with mutant tests, measure on A against 41,598 nodes, and Knuth-estimate two or three stalled interior classes. Falsifier: Taylor estimates above 10^6 nodes at arity 8. Lane P2 started 2026-10-02 22:55 UTC.

## Notes

2026-10-02 23:40 UTC. Built and verified (uncommitted): --taylor option in pilot_n17_subpattern_bb.py (schema v2, interval mode byte-identical), verifier re-proves Taylor cuts exactly (X1-X5), 9 mutants refused. FALSIFIER MET: Knuth estimates at arity 8 exceed 1e6 in both forms (I8 interval 8.0e6/2.2e6 mean/median vs Taylor 9.6e6/2.3e6; N8 4.7e8/2.7e5 vs 1.8e9/1.8e5; C9 arity 9 ~1e10 means). On A, Taylor tree ~30% smaller but nodes 1.4-1.5x dearer. Also found and fixed: process-wide enclosure cache leaked unrelated angles into certificates (fresh-process certificates such as A unaffected); verifier retries enclosures at 2,400 bits. Next (P2): diagnose the binding loss (hypothesis: per-pair normals of a shared square decouple), prototype a coupled form only if it dominates.
