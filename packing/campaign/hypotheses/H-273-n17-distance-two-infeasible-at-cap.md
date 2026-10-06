---
title: H-273 — every distance-2 n17 residue orbit is infeasible at the cap
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-273
  kind: hypothesis
  claim: >-
    Each of the 95 orbits at Hamming distance 2 from the endpoint's state in
    survey_n17_residue's arity8 frame (the 2,256 orbits on the H-266 unique-state cover
    that survive the 90 arity-at-most-8 selector flags) is infeasible at U = 1169/250:
    no packing of 17 unit squares of side at most U realises it.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      An exact placement at U of any of the 95 distance-2 orbits, checked from a float
      placement the survey reports
    direction: >-
      Reject on one exact placement. A float search can refute the claim but never
      confirm it, so 95 searches without a placement leave it unresolved, recorded as no
      placement in that many searches.
  instrument: >-
    devtools.survey_n17_residue --flag-set arity8 --distance 2 --sample 0 --shard K/10
    for K = 0 to 9, with its default full rounds, at --timeout 3600 per shard, from a
    clean run worktree at this registration commit; a placement's exact check by
    devtools.diagnose_n17_flag check on the placement receipt, or a W7 slice if the
    survey's witness format is not accepted
  instrument_ready: true
  regime: >-
    n=17; the H-266 unique-state cover at cap U; the arity8 frame's distance-2 stratum,
    every one-cell move from the endpoint that the arity-8 flags leave. Each shard places
    the endpoint's own state first as its positive control, which must place.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: About 95 x 205 s, 5.4 CPU-hours, in ten shards of 9 or 10 orbits
  prereqs: [H-266]
  replication: false
  registered: '2026-10-05'
  notes: >-
    Session 182's lane E (BC-421), the backfill of the n17 overnight plan, registered
    when slot 4 opened. The candidate form is the first half of the W3 draft's C1, split
    from its second half (the per-state kernel price, which duplicated H-264) on the Opus
    review's finding F14; the comparison of the selector's penetration with the side's
    slack is not a ratio of like measures and is not the mechanism claimed here. The
    distance-2 states may be feasible at U because each differs from the endpoint's own
    state by one cell, which is why H-264 reports its two distance-2 draws separately.
    A positive result makes the near-endpoint stage non-empty and moves the composed
    argument to exclusion at U'. The plan's run line named shards of 30 on two workers;
    on one slot the same 3,600 s ceiling holds ten shards of 9 or 10.
---
# H-273: The One-Cell Moves From the Endpoint at the Cap

The endpoint’s own state is feasible at $U$, and the 95 surviving orbits one cell away
from it are where a second feasible state is likeliest.
If one of them packs at $U$, a proof must exclude a near-endpoint stage as well as the
residue; if none does in 95 searches, the stage is unresolved and smaller than feared.

The instrument is the float survey on the whole distance-2 frame, in ten shards so that
each process stays under its wall ceiling.
A placement is a candidate until an exact check confirms it, and the run stops there for
the coordinator.

## Evidence

2026-10-06: `s182-bc428-u8` (mask 3078077, distance 2) was certified excluded by the
standing kernel verifier at 00:36 UTC under
[exp-257](../series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md),
one certified instance among the 95 distance-2 orbits; exp-255’s unresolved verdict is
unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
