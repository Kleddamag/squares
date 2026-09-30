---
type: is
id: is-01m3sqcscz61hcv90x46w4ck31
title: Profile Rust exact arithmetic slowdown against the Python rectangle verifier
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3rcka78kmcccpetknr2mswh
child_order_hints:
  - is-01m3st0ft2fa2av6mts8sc0v24
hold: null
hold_until: null
created_at: 2026-09-30T17:56:57.880Z
updated_at: 2026-09-30T18:42:40.577Z
started_at: 2026-09-30T17:59:38.171Z
---
User requests a careful first-principles diagnosis of why the native Rust exact backend is slower, whether the design is fundamentally inefficient, and a PR review update. Compare actual pinned arithmetic libraries, algorithms, normalization/GCD cost, allocations, caching, setup and transport on equivalent admitted work. Start from retained 201-angle and 1000-node matched benchmarks and the failed batching experiment. Distinguish observed causes from hypotheses; use a reusable bounded profile only when it isolates a concrete question, not a full certificate replay or unrelated suite. Evaluate targeted representation/library/algorithm improvements with exact-result parity and refusal controls. Do not claim Rust language speed guarantees or accept a weaker numerical verifier. Sol investigates; Astra max reviews any mathematical representation changes. Publish the findings and next measured action on the PR.

## Notes

Predeclared at 18:24 UTC before measurement: same-source opt-in Rust experimental-normalized-mul (Ratio::new) versus experimental-coprime-mul (Ratio::new_raw), identical cross-cancellation helper, fixed184 rectangles/128 angle-1 polygons, 3 interleaved pairs, exact Python equality. Primary child CPU criterion candidate median <=90% baseline and full ranges separated. Measured at18:29 UTC in retained receipt packing/resources/web/wand125-tools-2026-09-29/receipts/rust-exact-arithmetic-ab-2026-09-30.json SHA95247e0c: normalized median0.554884s range0.553031–0.556015; coprime median0.483236s range0.480792–0.485800; paired ratios0.8694/0.8755/0.8691. Positive 12.9% lower whole-child CPU; Python production _coverage_polygon ~0.3185s CPU, so coprime Rust remains ~1.52x slower on this fixed work. All128 exact values match in each pair. Child CPU includes parse/startup/encoding, so no pure GCD fraction inferred. Two feature builds from same source/compiler/profile, separate external target dirs; default Rust expressions unchanged. Fast exact-Rust gate46.06s cold/7.44s warm, includes both feature clippy/tests plus default differential210polygon/10refusal/2whole-verifier; candidate direct differential also passed same controls. Benchmark builder2 focused tests pass, Ruff/format/BasedPyright clean. OS sample receipt rust-exact-os-sample-2026-09-30.json shows gcd/shift/subtract hot but has startup bias and no causal percentage. Historical production Rust binary SHA407021 is context, not A/B baseline. Remaining hypotheses: num-bigint binary GCD versus CPython Lehmer, rational clone/allocation, extra convexity admission and clipping copies; profile or isolate separately before any further performance claim. No production backend switch or proof credit. Source review underway.
