---
title: "H-260 \u2014 D4 quotient of the closed n17 occupancy cover"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-260
  kind: hypothesis
  claim: D4 acts on existential closed-cell assignments of the H259 cover and its exact seventeen-square
    occupancy orbit count is smaller than the raw count.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: Eight exact fixed-count polynomials and Burnside orbit census of existential closed assignments.
    direction: Confirm only after closed-cover equivariance review, tiny-grid brute-force controls, producer
      cycle DP and independent polynomial audit agree for all eight terms, their sum is divisible by8,
      identity equals H259161100756 and orbit count is strictly smaller.
    threshold: Exact integer agreement, complete eight-element group and strict reduction; no tuned factor
      or optimality inference.
  instrument: devtools.count_grid_symmetry cycle DP and independent devtools.audit_grid_symmetry polynomial/binomial
    auditor.
  instrument_ready: true
  regime: Fixed H259 cap1169/250 and5by5 capacities, row-major indexing, existential closed membership.
    No lex-priority seam exclusions. Eight D4 elements R^k and R^kF.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: Ready by14:15UTC;one30second single-worker producer/audit group;1MiB output each;reviewdone14:25UTC.
  prereqs:
  - think-gr22
  replication: false
  registered: '2026-10-01'
  notes: H259 raw count161100756 already known. Symmetry coefficients and orbit count unobserved at registration14:12UTC.
    Necessary occupancy orbit census only; no geometric exclusions.
---
# H-260: Closed-Cell Symmetry for n17

Registered at14:12UTC before evaluating any nonidentity fixed count or orbit count.
The
[mathematical review](../../../docs/project/reviews/review-2026-10-01-n17-closed-cell-symmetry.md)
fixes all eight actions, cycle profiles, polynomials and the exact acceptance rule.

A state assigns each centre to any containing closed cell.
These existential states transform under square symmetries; the lexicographically owned
state need not. Future quotient leaves must retain closed membership and must not add
lex-priority exclusions.

The producer uses permutation cycles and weighted integer dynamic programming.
The auditor uses the separately derived polynomial coefficient formulas.
Tiny-grid brute force and malformed input controls precede instrument readiness.
No target evaluation is authorized after14:25UTC. If readiness misses14:15UTC, retain
the proof and instrument gap without a target round.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
