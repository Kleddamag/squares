---
type: is
id: is-01m3zcv9fnbp290a5vaw5fn83t
title: Octagon (second-order) core in the hull kernel; W7 at 32 and 16 rows (lane K2, F1 rank 1)
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:05.365Z
updated_at: 2026-10-02T23:00:48.880Z
---
Rank 1 of the cost-reduction plan (review section 4.1): a 4- to 16-fold cut in every kernel certificate's size and verification if W7 closes at 32 or 16 rows with the octagon core. Falsifier: W7 fails to close at 32 rows with the octagon. Lane K2 started 2026-10-02 22:45 UTC, after N1's --check-saved and standing verification.

## Notes

Octagon core implemented by K2 (uncommitted, sqpack/hull_kernel/producer.py, opt-in core='octagon'; tests/test_hull_kernel_octagon.py). Correction to F1 section 4.1: the raw two-end-square intersection is not inside every intermediate square; scaling by cos^2(delta/2) is sufficient (loss ~delta^2/4). Min support 0.4981 at 16 bins vs envelope 0.4924 at 64. Blind pair closes; standing verifier unchanged and PASS. W7 at 32 and 16 bins next.
