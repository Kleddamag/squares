---
title: H-274 — n17 residue states that stall at 32 uniform bins close under adaptive rows
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-274
  kind: hypothesis
  claim: >-
    Of the four counted draws of H-264's seed-182 draw that stalled under N1's recipe by
    this registration (masks 2817021, 3063677, 2878207 and 2784767, at distances 4, 4, 6
    and 4 from the endpoint's state), at least half close as whole 17-cell patterns on
    the H-266 unique-state cover at U = 1169/250 under SW9's frozen adaptive-row kernel
    recipe, each closure re-proved in full by the standing kernel verifier.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      How many of the four frozen states the kernel closes under SW9's recipe within the
      7,000 s ceiling, each closure admitted on the standing verifier's full pass
    direction: >-
      Confirm if at least two of the four close; reject if fewer than two do. The
      endpoint-state control under the same recipe must not close; a closure of it is a
      soundness alarm and voids the round.
    threshold: 2
  instrument: >-
    devtools.check_n17_subpattern --cells CELLS17 --bins 64 --max-rounds 24 --hull-limit
    16 --producer-share 0.6 --split-floor 512 --max-rows 1152 --split-patience 1
    --max-seconds 7000, from the clean run worktree at the session-182 registration
    commit cebb5d15a (the producer and checker are unchanged since); closures re-proved
    by devtools.verify_n17_kernel_certificate in full mode under the kernel-streamed
    listing
  instrument_ready: true
  regime: >-
    n=17; the H-266 unique-state cover at U; the four frozen states only, one run each,
    in mask order, after the endpoint-state control. The distance-2 draw 1964767 is left
    out: it is not counted by H-264, and lane D found it consistency-limited at a true
    fixed point, the one stall that no pairwise cut at any row width addresses.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: At most 7,000 s per state and for the control, about 10 CPU-hours at most
  prereqs: [H-264, H-266]
  replication: false
  registered: '2026-10-05'
  notes: >-
    Registered by Session 182 (BC-424) as a future slice at the coordinator's check-in;
    H-264 is untouched and runs to its own verdict on N1's recipe. Mechanism, from lane
    D's stall classification (Session 182, docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    when filed): the distance-4 per-state stalls share one north-wall knot, side-N1 and
    side-N2 mutually unsupported by margins of about 0.011 to 0.015. Those margins lie
    below the first-order losses of 32 uniform bins (about 0.0149 on 1/32 rows) but two
    to three times a collision cut at the 1/512 split floor, under which lane K closed
    eight of its nine arity-7 flags the same night. Limits: lane A runs N1's recipe
    without adaptive rows, so its nodes never reached the 1/512 floor; a closure here
    prices a per-state exclusion under the stronger recipe, and each closed state removes
    only its own orbit.
---
# H-274: Per-State Closure Under Adaptive Rows

H-264 prices per-state exclusion with N1’s recipe of 32 uniform bins.
Lane D’s reading of its stalls suggests the stalls come from that recipe rather than
from the states: the knot that stops them sits between the uniform rows’ losses and the
cuts that adaptive rows reach.
This hypothesis runs the stalled states again under the recipe that closed lane K’s
flags and asks whether half of them close.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
