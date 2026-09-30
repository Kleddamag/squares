---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: in_progress
priority: 2
version: 19
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
child_order_hints:
  - is-01m3s98kgj0s9pg4ybk685nc7t
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T14:48:02.931Z
closed_at: 2026-09-30T12:07:44.056Z
close_reason: Implemented, independently reviewed, pushed in01572bb8b, and all hosted PR checks pass. CIselector optimized with68focusedtests and measured cold-profile improvement; proofcostreporter covers17retained batches with fivecontrols and unknownmetric handling.
resolution: null
duplicate_of: null
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

Weighted partition executed correctly at c32fd6f73 in run36730867640, clean validated merge fd75217add4938f5dd88a86d9d58822ecf555834. A154.71/168s, B96.49/154s, both pass; actual assignment matches record (A226files, B207), zero missing/duplicate. A3540passed+7skips; B4408passed. Actual summed cost541.583/302.072 versus predicted524.136/480.458; B runner-speed variation is material, so no pure repartition speedup is claimed. Aggregate alone fails live jobs-API step observation; think-dh2d owns the repair. Reports retained tmp/n11-ci-shards-new/{a,b}.
