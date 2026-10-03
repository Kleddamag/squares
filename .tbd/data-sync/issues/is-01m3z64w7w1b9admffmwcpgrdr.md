---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: open
priority: 1
version: 5
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-03T01:19:47.362Z
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

Rank 3 (no gmpy2) integrated 841e368dd: producer 1.58x, check-saved 2.47x, byte-identical. Owner approved gmpy2 (2026-10-03); F2 now porting producer and checker onto gmpy2 in a worktree (verifiers stay on CPython integers for independence). Compiled checker split out to lane X1.
