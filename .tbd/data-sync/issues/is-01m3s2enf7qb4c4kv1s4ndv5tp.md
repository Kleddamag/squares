---
type: is
id: is-01m3s2enf7qb4c4kv1s4ndv5tp
title: Index exact cover events by closed x-overlap for costly center rows
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T11:50:59.302Z
updated_at: 2026-09-30T11:50:59.302Z
---
Build an opt-in exact cover helper that enumerates only segment pairs with overlapping closed x-projections, preserving all vertex and line-crossing events including equal-endpoint tangency. Differential-check event sets and cover verdicts against the frozen all-pairs backend on analytic adversarial shapes and representative pinned 1383 source geometry. Measure matched row cost before connecting the backend to accepted replay; no source proof credit from a primitive benchmark.
