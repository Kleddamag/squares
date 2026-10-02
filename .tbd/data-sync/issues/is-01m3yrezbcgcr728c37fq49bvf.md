---
type: is
id: is-01m3yrezbcgcr728c37fq49bvf
title: "Independent fast measure verifier: a clean-room, high-performance checker for net-direction and continuous-angle certificates"
kind: epic
status: open
priority: 1
version: 11
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
child_order_hints:
  - is-01m3yssz1abf448yycr6hj6nr9
  - is-01m3ystaq4ef5xmnmf4f802x3n
  - is-01m3ystck294q971jb9d2war1h
  - is-01m3ystff276btdyf2nxewyzyc
  - is-01m3yt01stqppbqjedb0xe3d61
  - is-01m3yt043ad0fdz31rfe5spgyx
  - is-01m3yt067qc3s5wfdc6586gebv
  - is-01m3z564t0yxdye6gt6hzsjww5
  - is-01m3z566ftxbm195y6f68b3chw
created_at: 2026-10-02T16:51:50.251Z
updated_at: 2026-10-02T20:47:29.447Z
---
Owner requirement: an independent implementation of the verifier, made extremely fast. Slice 1 (running): spec from the reviews' mathematics, clean-room protocol producing an independence record, profile of verify.cpp / mixed_rotated_verify.cpp / unified_linear_verify.cpp, slice plan. Slice 2: Rust engine for rectangle-density certificates (f64 outward-rounded intervals, exact-rational fallback near threshold via sqpack.rectangle_density, spatial index, incremental bounds, batched evaluation, reuse across net directions), validated against every replayed rectangle certificate and all mutation controls. Slice 3: points and segments (mixed, linear). Slice 4: continuous-angle (zmx2-family) covers. Slice 5: adversarial review; record each passing certificate as confirming evidence with verifier_relation independent-implementation. Ships in the stacked PR on top of #298 (slices that finish later may follow in their own PR). Not a rung change: an attribute beside the rung (epistemics.md, Confirmation).

## Notes

Spec + profile: claude/lane-w1-verifier-spec (beads think-s333, think-fcxx closed; think-r07y adversarial reviews, think-3ok2 independence audit open). Implementation: claude/lane-w2-fast-verifier-wip (local agent W2 running; crate packing/sqverify_fast, experiment-loop registry, INDEPENDENCE.md). Clean-room rule: implementers must not read authors' checker code nor W1's dirty-side files (research-2026-10-02-author-checker-profile.md, attribution/, profile script). Headline benchmark vs verify.cpp to be run on an idle cloud runner.
