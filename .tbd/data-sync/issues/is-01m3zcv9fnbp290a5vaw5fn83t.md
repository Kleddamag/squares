---
type: is
id: is-01m3zcv9fnbp290a5vaw5fn83t
title: Octagon (second-order) core in the hull kernel; W7 at 32 and 16 rows (lane K2, F1 rank 1)
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:05.365Z
updated_at: 2026-10-02T22:48:05.365Z
---
Rank 1 of the cost-reduction plan (review section 4.1): a 4- to 16-fold cut in every kernel certificate's size and verification if W7 closes at 32 or 16 rows with the octagon core. Falsifier: W7 fails to close at 32 rows with the octagon. Lane K2 started 2026-10-02 22:45 UTC, after N1's --check-saved and standing verification.
