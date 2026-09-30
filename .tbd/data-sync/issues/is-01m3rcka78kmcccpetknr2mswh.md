---
type: is
id: is-01m3rcka78kmcccpetknr2mswh
title: Reduce independent rectangle verification work before full corpus replay
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rbmdd2knptgfj454y4exak
child_order_hints:
  - is-01m3rd34xb2w4qe423qk5dtymp
created_at: 2026-09-30T05:29:02.939Z
updated_at: 2026-09-30T05:58:58.516Z
---
W5 support for independent rectangle coverage: paired analytic control under benchmark a31a41c0 completed all201 angles at matching effective cutoff, but native1781 nodes versus C++209 and native process CPU0.426s versus C++0.00916s. Hypothesize stronger reviewed geometric/derivative bound reduces branching, then profile exact arithmetic cost per node before selecting compiled/Rust kernels. Predeclare fixed external corpus and alternating complete paired trials; require no weaker threshold, same full domain, no unresolved work and preserved adversarial refusals. Partial probes cannot establish speedup. Keep secondary to T060 field/capture proof lanes.

## Notes

Bounded cProfile source 44a88aad / receipt db5a0873 on pinned n11 angle1, effective threshold, 10 s internal/15 s outer: 338 nodes; inclusive _coverage_polygon 9.949 s, exact_intersection_area 9.261 s, _clip_axis 8.062 s, Fraction.forward 5.430 s, math.gcd self 1.306 s (5.17M calls). Profile overhead means no speed baseline. Exact Python clip fast path reviewed by Astra: direct closed-plane vertex comparisons, all-in tuple reuse, strict all-out empty, interpolation only on crossings. Kernel SHA1e9ca048; differential original-clip oracle 49 cases, focused19 tests pass, Ruff/BasedPyright zero. Authoritative source-bound A/B runner a364dbb2: retained n11 fixed1000 frontier result82d51365, identical exact report including 13 pending boxes, 494 accepted, node_limit; verification CPU7.305245→5.506285 s (24.6% less), wall7.572→5.747 s. Complete analytic n3 all201 resultcfcb32e2, both VERIFIED with1781 nodes and exact reports; CPU0.373918→0.238158 s. Earlier pre-guard receipts explicitly superseded by clip-ab-supersession.json. This is fixed-work improvement, not external/full-domain parity. Batched arbitrary-precision Rust geometry remains child think-rmj3, independent stronger gradient bound proposed but unimplemented.
