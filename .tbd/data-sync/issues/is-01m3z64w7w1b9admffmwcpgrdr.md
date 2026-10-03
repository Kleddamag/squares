---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-03T00:40:19.135Z
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

Review 30a6c9753. Rank 1 done: kernel verifier rewrite e0b66f07b (5c550f7c), W7 full re-verification PASS in 242 s vs 4,258 s with identical counts. Ledger digest addition waits on R6's independent review. Next: N1 full verification with it, then rank 3 without gmpy2 (producer/checker facet cache, indexed sweep) in a separate worktree, byte-identical outputs required. gmpy2 (2.9-4.7x whole-tool) is a pending user decision.
