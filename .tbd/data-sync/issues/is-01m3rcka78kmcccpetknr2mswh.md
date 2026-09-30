---
type: is
id: is-01m3rcka78kmcccpetknr2mswh
title: Reduce independent rectangle verification work before full corpus replay
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rbmdd2knptgfj454y4exak
child_order_hints:
  - is-01m3rd34xb2w4qe423qk5dtymp
created_at: 2026-09-30T05:29:02.939Z
updated_at: 2026-09-30T05:38:52.581Z
---
W5 support for independent rectangle coverage: paired analytic control under benchmark a31a41c0 completed all201 angles at matching effective cutoff, but native1781 nodes versus C++209 and native process CPU0.426s versus C++0.00916s. Hypothesize stronger reviewed geometric/derivative bound reduces branching, then profile exact arithmetic cost per node before selecting compiled/Rust kernels. Predeclare fixed external corpus and alternating complete paired trials; require no weaker threshold, same full domain, no unresolved work and preserved adversarial refusals. Partial probes cannot establish speedup. Keep secondary to T060 field/capture proof lanes.

## Notes

Bounded cProfile source 44a88aad / receipt db5a0873 on pinned n11 angle1, effective threshold, 10 s internal/15 s outer: 338 nodes; inclusive _coverage_polygon 9.949 s, exact_intersection_area 9.261 s, _clip_axis 8.062 s, Fraction.forward 5.430 s, math.gcd self 1.306 s (5.17M calls). Profile overhead means no speed baseline. Implement one reviewed exact Python clip fast path: direct closed-halfplane vertex comparisons, all-in tuple reuse, strict all-out empty, and rational interpolation only on crossings; differential exact tests and bounded matched controls. No full-domain or speed-parity claim. Batched arbitrary-precision Rust geometry is separate think-rmj3.
