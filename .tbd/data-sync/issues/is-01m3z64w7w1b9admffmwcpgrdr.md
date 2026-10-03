---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-03T05:41:34.507Z
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

gmpy2 port integrated c401c81d6 (owner-approved): producer 2.78x, check-saved 4.20x on W7 round 1, byte-identical; full W7 check-saved 173 s (930 s indexed before rank 3, 1,634 s reference). Lock regenerated with CI's uv 0.12.8 (revision 3, additive). Verifiers stay on CPython integers. Next F2: profile the capture producer (C1's ~155 CPU-s per update at 128 rows) vs the branch-and-bound verifier cut cache; build the larger payoff.
