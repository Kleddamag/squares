---
type: is
id: is-01m3qgvz4ka0qqjz4rrham7a3g
title: Fan out post-merge deferred validation jobs
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:24:26.375Z
updated_at: 2026-09-29T21:24:26.375Z
---
Reuse the reviewed deep-gate whole-Step bins in .github/workflows/packing-validation.yml so push/daily validation does not retain the predecessor serial deferred critical path. Preserve an exact disjoint union with the complete integration job, immutable push SHA binding, unique receipts, and existing aggregate semantics. Measure hosted critical-path wall and runner-minutes before replacing the current topology budgets.
