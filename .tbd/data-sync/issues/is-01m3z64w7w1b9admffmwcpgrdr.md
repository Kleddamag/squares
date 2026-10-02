---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-02T23:00:47.976Z
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

Review committed 30a6c9753: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md. Verifiers are 71-74% of cost; gmpy2 drop-in 2.9-4.7x whole-tool; integer facets 23x. Combined with F1: about 100-360 CPU-hours. F2 now implementing its rank 1 (kernel verifier hot loops in CPython integers, own sweep and caches; no new dependency). Ownership of verify_n17_kernel_certificate.py moved from K2 to F2 for independence. gmpy2 as a dependency is a pending user decision.
