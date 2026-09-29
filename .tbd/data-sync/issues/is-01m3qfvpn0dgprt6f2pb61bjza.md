---
type: is
id: is-01m3qfvpn0dgprt6f2pb61bjza
title: Fan out hosted deferred validation across immutable-tree jobs
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:06:49.119Z
updated_at: 2026-09-29T21:10:54.206Z
---
Split the deep gate's eight existing complete deferred Step verdicts into four balanced explicit hosted jobs and the exhaustive_exact lane into three stable whole-file shards through packing-validate. Resolve one immutable checkout SHA for every job; preserve nonempty, pairwise-disjoint complete coverage, unique timing artifacts, required aggregation, and honest inherited/derived job budgets until hosted cells provide direct baselines.
