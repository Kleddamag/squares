---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: closed
priority: 2
version: 10
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T12:07:44.057Z
closed_at: 2026-09-30T12:07:44.056Z
close_reason: Implemented, independently reviewed, pushed in01572bb8b, and all hosted PR checks pass. CIselector optimized with68focusedtests and measured cold-profile improvement; proofcostreporter covers17retained batches with fivecontrols and unknownmetric handling.
resolution: null
duplicate_of: null
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

Measured/fixed dependency-selector hotspot without changing CI thresholds: imports ast.walk visited2.66millionnodes,6.36s cumulative of13.933s profiled selection. Skipping expression subtrees (cannotcontain importstatements) retains exception/match suites; same profile selection7.259s.68focusedselector tests pass6.83s, Ruff/typesclean. Candidate awaiting independentreview and hostedcheckpoint; broadlocaltests notrun.
