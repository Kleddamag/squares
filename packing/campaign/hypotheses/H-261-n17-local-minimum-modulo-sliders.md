---
title: H-261 — the n17 endpoint is a strict local minimum modulo its slider cone
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-261
  kind: hypothesis
  claim: >-
    For an explicit rational radius r > 0, every packing of 17 unit squares in [0,S]^2
    whose 45 non-slider coordinates lie within r of the accepted n17 endpoint family,
    with slider coordinates anywhere in the physical slider domain, has S >= S*, with
    equality only on the family. The slider coordinates are square 6's three, xi_5 <= 0,
    square 11 along -v and square 13 along +-v; the kernel of the 52 positively weighted
    H-258 rows is exactly their span.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: >-
      An exact rational basis of the kernel of the 52 positive H-258 rows; exact
      nonnegative duals for all 90 signed non-slider coordinate directions; per-row
      curvature bounds by the n11 focused-rectangle recipe; Taylor checks that the 135
      unavailable owner alternatives stay negative; nonnegativity of the stress and the
      duals uniformly over the slider domain; and the ratio test (1/2) M_j < r_j at one
      declared rational radius vector.
    direction: >-
      Confirm only if H-258 is accepted, every item above is certified exactly or by
      outward intervals, synthetic controls pass, and an independent Fable max review
      of the composition (in particular the angle-chart reduction modulo pi/2 and the
      product form of the neighbourhood) finds no blocking defect. A failed ratio test
      at the declared radius is inconclusive for local minimality and selects interval
      enlargement along omega_11 - omega_12 and omega_16; it refutes nothing.
    threshold: >-
      Kernel dimension exactly 6 with the six named generators; every dual exact and
      nonnegative; worst ratio below 1 at the declared radius. Exploratory first-order
      estimate: worst ratio 0.86 at uniform radius 3e-4.
  instrument: >-
    devtools.check_n17_local_minimum, to be built: exact Fraction linear algebra and
    LP duals over the H-258 rows, the n11 curvature-bound recipe, and outward interval
    checks over the slider domain, with an independent kernel and dual checker
  instrument_ready: false
  regime: >-
    The H255 root box and H256 centroid endpoint; the H257 feature inventory; the H-258
    allocation; angles reduced modulo pi/2 in the H254 labelling; the l-infinity norm on
    non-slider coordinates
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    One controlled build and review slice of about two hours; target arithmetic in
    seconds to minutes on one worker
  prereqs: [H-258, think-wrgx]
  replication: false
  registered: '2026-10-01'
  notes: >-
    From the PR 265 route review
    (docs/project/reviews/review-2026-10-01-n17-route-after-pr265.md). Exploratory
    receipts in packing/campaign/explorations/X048-route-review/receipts/: kernel rank
    46 of 52 with the six slider generators, coordinate duals with largest coefficient
    175.8 for -omega_11 (ten minor duals need exact redo), radius ratios 0.86, 1.43, 2.9
    and 8.6 at 3e-4, 5e-4, 1e-3 and 3e-3. The certified radius is the target the global
    capture step must reach.
---
# H-261: Local Minimum Modulo the Slider Cone

The known n17 packing cannot be isolated: three squares slide and one rotates freely.
The terminal theorem must therefore say that nothing near the endpoint family is
smaller, with the slider coordinates left free.
Exploratory checks find a first-order conical minimum outside the six slider directions,
so the n11 focused-rectangle method applies once those directions are quotiented out.

The certified radius matters as much as the verdict: it is what the global capture step
must reach.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
