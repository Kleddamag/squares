---
type: is
id: is-01m3zcv8xq2f9njty9g8dgw4w3
title: Taylor relaxation for the n17 branch and bound, with verifier support (lane P2, F1 rank 4)
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:04.791Z
updated_at: 2026-10-02T22:48:04.791Z
---
Rank 4 of the cost-reduction plan (review section 4.2). Add a first-order Taylor relaxation of the trigonometric coefficients to devtools/pilot_n17_subpattern_bb.py as an option (off = byte-identical certificates), extend verify_n17_bb_certificate.py to re-prove it exactly with mutant tests, measure on A against 41,598 nodes, and Knuth-estimate two or three stalled interior classes. Falsifier: Taylor estimates above 10^6 nodes at arity 8. Lane P2 started 2026-10-02 22:55 UTC.
