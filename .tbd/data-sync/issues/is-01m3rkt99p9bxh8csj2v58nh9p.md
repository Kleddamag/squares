---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: in_progress
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T09:44:07.710Z
closed_at: 2026-09-30T08:52:47.572Z
close_reason: Hosted Packing validation36691851635 at48c403add passes every required job including macOS, behavioral A/B, types, geometry, frontend and aggregate. Exact-source Rust cache fixes runtime; generated Rustdoc exclusion and measured2135 replay registration fixes pass focused controls. No timing thresholds relaxed. Future heads require their own hosted certification.
resolution: null
duplicate_of: null
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

Hosted shardA all4100 tests pass but172.23s exceeded168s. Two focused setup fixes retain rejection predicates while removing redundant seed geometry: generic_fresh7controls0.40s, sequential structurecontrol0.14s; full golden replays unchanged. Separate frozen-worktree executor defect was found during actual batches: shared-input path passed admission but invocation serialization used checkout-relative path.16 checker records retained without credit; supervisors stopped. Source_archive_reference now handles both repository roots;22 runner/inventory controls pass. Fresh actual replay required, no budget or proof acceptance relaxed.
