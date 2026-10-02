---
type: is
id: is-01m3yrezbcgcr728c37fq49bvf
title: "Independent fast measure verifier: a clean-room, high-performance checker for net-direction and continuous-angle certificates"
kind: epic
status: open
priority: 1
version: 1
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:50.251Z
updated_at: 2026-10-02T16:51:50.251Z
---
Owner requirement: an independent implementation of the verifier, made extremely fast. Slice 1 (running): spec from the reviews' mathematics, clean-room protocol producing an independence record, profile of verify.cpp / mixed_rotated_verify.cpp / unified_linear_verify.cpp, slice plan. Slice 2: Rust engine for rectangle-density certificates (f64 outward-rounded intervals, exact-rational fallback near threshold via sqpack.rectangle_density, spatial index, incremental bounds, batched evaluation, reuse across net directions), validated against every replayed rectangle certificate and all mutation controls. Slice 3: points and segments (mixed, linear). Slice 4: continuous-angle (zmx2-family) covers. Slice 5: adversarial review; record each passing certificate as confirming evidence with verifier_relation independent-implementation. Ships in the stacked PR on top of #298 (slices that finish later may follow in their own PR). Not a rung change: an attribute beside the rung (epistemics.md, Confirmation).
