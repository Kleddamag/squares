---
type: is
id: is-01m3z64w7w1b9admffmwcpgrdr
title: "Cost reduction to hundreds of CPU-hours: performance engineering review (lane F2)"
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:59.452Z
updated_at: 2026-10-02T22:46:29.052Z
---
Owner request, Session 168: profile the kernel, branch and bound and verifiers (pure-Python exact arithmetic), estimate gains from integer arithmetic, gmpy2/flint, Rust kernels, caching, parallelism, under the soundness and verifier-independence rules. Deliverable: docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md (uncommitted until reported).

## Notes

2026-10-02 22:50 UTC. Profiles and micro-benchmarks preserved in packing/campaign/explorations/X048-session-168-pilots/handoff/f2/ (scripts as .txt, rustbench sources). F2 resumed at 22:45 to write docs/project/reviews/review-2026-10-02-n17-cost-reduction-performance.md, composing with F1's section 5 and ranked plan, measuring at 64 and 32 rows.
