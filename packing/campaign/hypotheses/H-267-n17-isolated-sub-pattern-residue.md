---
title: H-267 — isolated sub-pattern exclusion leaves at most 10^4 n17 occupancy orbits on the minimal cover
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-267
  kind: hypothesis
  claim: >-
    On the H-266 cover, forbidden occupancy sub-patterns of arity at most seven, each
    certified infeasible at cap U by the n11 kernel adapted to n17 or by a
    majority-feature packet, exclude by containment all but at most 10^4 of the D4
    orbits of closed capacity-one assignments, and never exclude the endpoint's state.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      The exact number of D4 orbits not containing any certified forbidden sub-pattern,
      with the endpoint state surviving as positive control and n11's mask-0 field
      replayed through the same adapter as the method control
    direction: >-
      Confirm if the certified residue is at most 10^4 orbits with every certificate
      independently checked; reject if it exceeds 10^4 at arity seven, or if any
      certified pattern excludes the endpoint state.
    threshold: 10000
  instrument: >-
    A heuristic selector (the bulk-exclusion lane's sampling and descent proxy as a
    retained tool), the n11 v9 kernel adapted to the n17 frame as prover, and an exact
    set-union consumer, to be built after H-266
  instrument_ready: false
  regime: >-
    n=17; cap 1169/250; the H-266 cover; sub-patterns of arity at most seven
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: About a week to adapt the kernel; hours of CPU for the certificates
  prereqs: [H-266]
  replication: false
  registered: '2026-10-02'
  notes: >-
    From the bulk-exclusion design review (its H-F2). n11 excluded 1,904 of its 2,180
    cases with 59 isolated sub-pattern certificates of arity five to seven. An
    exploratory proxy at arity at most five on the 24-cell design flags ten D4 classes
    and leaves 11,939 orbits with the endpoint surviving; arity six already finds the
    analogue of n11's mask-0 wall-row field. Not a certificate: the proxy is a float
    penetration heuristic.
---
# H-267: Isolated Sub-Pattern Exclusion on the Minimal Cover

n11’s census became affordable because most cases contain one of a few small
sub-patterns that cannot be realised at all, so one certificate excludes hundreds of
cases. This hypothesis tests whether the same mechanism brings n17 to a residue that
geometric exclusion at one to two CPU-hours per case can absorb.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
