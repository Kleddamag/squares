---
type: is
id: is-01m3qn7w7yphc9530wk4p70qmz
title: Investigate reachable normal-lane tail balancing
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T22:40:50.941Z
updated_at: 2026-09-29T22:40:50.941Z
---
After publication of the pool-heavy split, diagnose and measure normal-lane scheduling on an identical retained selection and source. Frozen primary a2b8e696c receipt run 6085bce8a0eb46a287d2cd1a1b52cccb completed 7750 passed, 9 skipped in 416.24s at 10 xdist workers and PACK_JOBS=1. Per-worker progress shows at most four busy during the final ~121s and at most two during the final ~62s; one indivisible 141.16s node also limits gains. Current wrapper passes -n 10 without a distribution override, and installed xdist maps -n to load. Investigate bounded work-stealing or long-first scheduling with the same exact nodes, markers, fixtures, and failure semantics. Record comparable phase walls and worker utilization before accepting any change or claiming speedup; do not tune the frozen candidate.
