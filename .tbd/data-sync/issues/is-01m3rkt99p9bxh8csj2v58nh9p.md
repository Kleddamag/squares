---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: in_progress
priority: 2
version: 16
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
child_order_hints:
  - is-01m3s98kgj0s9pg4ybk685nc7t
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T13:50:00.721Z
closed_at: 2026-09-30T12:07:44.056Z
close_reason: Implemented, independently reviewed, pushed in01572bb8b, and all hosted PR checks pass. CIselector optimized with68focusedtests and measured cold-profile improvement; proofcostreporter covers17retained batches with fivecontrols and unknownmetric handling.
resolution: null
duplicate_of: null
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

Run36717374480 at0a474: all functional tests pass; suite-A165.1s exceeds1.5x109.92 baseline by0.22s. Other required shards pass. Prior a7a06 suite-B retry dropped159s to91s, but partial attempt aggregator intentionally unmeasurable. No budget relaxation or broad local suite; inspect timing artifacts and verify next substantive full run.

Read-only diagnosis at run 36717374480: suite-A 165.10 s, 4,163 tests, 553.087 summed test-seconds; suite-B 113.22 s, 3,776 tests, 381.581 test-seconds. Adjacent suite-A runs 36712293007 and 36712919119 were 163.13/164.37 s with 4,141/4,147 tests and 539.479/549.064 test-seconds, so this is a repeatable current-workload imbalance rather than a new 0a474 test slowdown. The tracked record came from run 35175474610 with 325 files/545.746 total recorded seconds; 109 current files absent from it account for 142.416 test-seconds. Rebuilt suite-file-costs.json through maintained devtools.suite_files record from both successful same-GITHUB_SHA=597ac9ec... shard reports in run 36717374480, now 433 files and predicted 467.334/467.334 cost seconds. This is a predicted partition only, not hosted wall evidence or a budget relaxation; next integrated push measures it. Focused test_suite_files.py 25 passed.

Selection audit after re-recording: current tree has443 test_*.py files under both behavioural roots,433 named in the new record and10 deterministic path-hash fallback files (browser-floor contract plus nine newer proof tests). The three n11 inventory/composition files are recorded, so adding assertions inside them does not move their shard. Maintained test_suite_files partition property covers every current file exactly once; marker filtering and ignore settings are unchanged. This check is file-assignment evidence, not a fresh hosted wall result.
