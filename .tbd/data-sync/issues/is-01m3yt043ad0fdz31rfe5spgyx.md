---
type: is
id: is-01m3yt043ad0fdz31rfe5spgyx
title: "W2-P: sqverify_fast performance loop against verify.cpp"
kind: task
status: in_progress
priority: 1
version: 2
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:18:40.746Z
updated_at: 2026-10-02T21:01:16.577Z
---
Experiment-loop campaign: fixed benchmark (several directions of 3-4 certificates), verify.cpp timed as a black box on the same directions, pre-declared accept rule, hypotheses kept and rejected recorded in packing/benchmarks/measure-verifier/.

## Notes

Campaign at packing/benchmarks/measure-verifier (README runbook, ideas, H-001..H-009, exp-001..exp-011). Accepted: H-002 admission (-34% process instr), H-006 inherited derivative bounds (-18.5% search), H-007 branch-free directed rounding (-52% search). Rejected: H-001, H-005, H-008, H-004, H-009. Standing build c2: 28.8x less CPU than verify.cpp on six single-direction cells, 43x on whole rect_n32_L595 (loaded host). Headline for the idle runner: python -m benchmarks.bench_measure_verifier --headline --arm fast:candidate=... --arm verify-cpp.
