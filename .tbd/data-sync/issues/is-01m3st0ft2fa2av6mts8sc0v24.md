---
type: is
id: is-01m3st0ft2fa2av6mts8sc0v24
title: Measure coprime multiplication in the bounded full rectangle verifier
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3sqcscz61hcv90x46w4ck31
hold: null
hold_until: null
created_at: 2026-09-30T18:42:40.577Z
updated_at: 2026-09-30T18:51:25.544Z
started_at: 2026-09-30T18:51:25.186Z
---
Follow the completed 12.912% fixed-primitive ablation in PR251 with a source-bound production-default versus experimental-coprime comparison on the retained external angle1/1000-node workload. Use the complete201-angle analytic fixture and malformed/source/deadline controls for correctness. Freeze sources, build flags, effective cutoff, traversal, node counts, timing metrics and accept rule before three alternating pairs. Require identical normalized reports; capped external runs remain INCONCLUSIVE and earn no certificate credit. Report coordinator CPU, child CPU and wall separately. Adopt only if the measured benefit justifies the small canonical helper; do not conflate this with a GMP/library comparison. Keep GCD/operand-size/allocation profiling and one alternative engine as separately measured hypotheses under parent think-3cwg.

## Notes

Design preflight before measurement: existing check_exact_rust_kernel._benchmark measures only one Rust binary, so create one reusable paired whole-verifier benchmark using the maintained verify_rectangle_density CLI and existing supervised run_command; no production checker edit. Inputs pinned analytic n3 SHA bfd6e4dea67a048321836c69c9c9fe782687ffc512ccb1afc43249212ba5f01e and external n11 SHA 8e3339eefb2fad81868f51e3f72cbc8487b40b66f9d8fbc711cdbd5e5edeff4. Same-source lib SHA87e7c231, default binary SHAee453972 and coprime binary SHAd25afa57; exact source recheck before/after. Run all201 analytic angles with max_nodes_per_angle10000/depth20, and external angle1 with1000/depth20/retain-pending, common-core threshold1 and internal30s. Three alternating baseline/candidate pairs per workload, per-invocation supervised<=40s, overall<=300s. Require every analytic result VERIFIED and external result INCONCLUSIVE with same 1781/1000 nodes and identical normalized report SHA across arms/pairs (exclude timing and binary metadata only); any refusal/timeout has zero comparison credit. Record wall, Python coordinator CPU and Rust child CPU separately. Material full-verifier candidate criterion: external child CPU median<=0.90 baseline with nonoverlapping full ranges, external wall median<=1.05 baseline, analytic wall median<=1.05 baseline; otherwise negative/unresolved. No certificate/proof promotion, no default backend change. Source and tool hashes will be frozen before timing.
