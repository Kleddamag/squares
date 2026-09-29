---
type: is
id: is-01m3qfvpn0dgprt6f2pb61bjza
title: Fan out hosted deferred validation across immutable-tree jobs
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:06:49.119Z
updated_at: 2026-09-29T22:32:38.225Z
---
Split the deep gate's eight existing complete deferred Step verdicts into four balanced explicit hosted jobs and the exhaustive_exact lane into three stable whole-file shards through packing-validate. Resolve one immutable checkout SHA for every job; preserve nonempty, pairwise-disjoint complete coverage, unique timing artifacts, required aggregation, and honest inherited/derived job budgets until hosted cells provide direct baselines.

## Notes

Implemented deep-gate immutable resolver, four whole-Step deferred jobs, three whole-file exhaustive shards, exact aggregate and receipt contracts, tracked pending hosted measurements, and suite-file provenance. Added exhaustive-file-costs.json from retained run 35579234418. Focused evidence: 93 workflow/shard/budget tests pass; root's full validation CLI/selector run 191 pass; Ruff format/check clean; BasedPyright 0 findings; collect-only exhaustive union 60 nodes = shards 2+30+28, disjoint. First hosted candidate must replace pending_measurement entries and report critical-path wall plus runner-minutes. Upload-artifact remains warn/non-gating; in-job HEAD equality is fail-closed. Post-merge parity tracked as think-08ht.

Independent budget review of 5060cb6f8: GitHub API for successful workflow_dispatch run 36636552951 confirms head 9174140a, all ten declared workers completed successfully, wall 1133s, and worker durations 17/778/475/621/623/957/953/858/1015/1111s totaling 7408s. The register records the eight new-topology observations plus wall with spread null for the single sample; existing multi-run slow-lane and screen baselines and spreads are preserved. Only wall, resolve-tree, and deferred-atlas-grid ceilings tighten (3430->1900, 36->30, 980->900), each under 2x headroom. Focused budget/post-merge contracts pass 61/61. No enforcement change or speedup claim; keep open for repeat hosted evidence and publication.
