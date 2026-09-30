---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T08:11:41.617Z
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

Repeated hosted checks-budget failures are timing-only: latest119ae49ce run36686375268 passed54 logical checks but128.67s versus75.67s baseline (1.70x). SuiteB now passes. Exact Rust gate39.3s includes uncached crate builds. Focused selector optimization retains exact selections83/68/54 and reduces CPU7.506→6.767,7.356→6.953,7.918→6.891 seconds across three cold calls; 24 controls pass6.97s. Preserved sources/receipt aed1ee4eb; wall varied under concurrent proof load. Exact-source/compiler-only crate cache now published690e6fd2f, no prefix restore, all original verification commands retained; two safety contracts pass. No thresholds changed. Await hosted validation.
