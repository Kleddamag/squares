---
title: "H-257 \u2014 complete n17 endpoint contact-feature inventory"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-257
  kind: hypothesis
  claim: At the accepted H255 root and H256 centroid packing, all owner-axis alternatives and active-wall
    corner features have the predicted exact zero or strict sign, and all nine parallel-face tangential
    offsets lie strictly between minus one and one.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: Complete168raw owner-axis/order alternatives at21zero pairs,60corner gaps at15active walls
      and9parallel-face offset intervals.
    direction: Confirm only if33pair options are exact root identities and135 have strictly negative interval
      upper bounds;29active-wall corners are exact root identities and31 have strictly positive interval
      lower bounds; all9tangent offset intervals lie strictly inside(-1,1). Complete labeled coverage,
      synthetic controls and independent mathematical/code/output review are required. A straddling or
      failed enclosure is unresolved inventory, not a refutation of endpoint feasibility.
    threshold: Exact zero identities; strict interval signs and strict abs(tau)<1 without numerical tolerances.
  instrument: devtools.check_n17_endpoint_features; exact symbolic zero identities and Fraction interval
    sign checks, with both owner labels retained.
  instrument_ready: true
  regime: H255 fixed coordinatewise inclusion enclosure m plus/minus eta; H256 fixed centroid geometry.
    Existing Sympy and standard-library exact arithmetic, one worker, no root refinement or slider change.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: One25minute instrument/review slice; one180second single-worker target,10MiB per output,
    followed by independent output review.
  prereqs:
  - think-6dg0
  replication: false
  registered: '2026-10-01'
  notes: Feature completeness supports a subsequent first-order cone calculation. It proves neither stationarity
    nor local/global optimality and does not meet the class-angle derivative threshold in H027.
---
# H-257: Complete n17 Endpoint Contact Features

This round audits the alternatives omitted when an exact packing certificate retains
only one successful separating direction per pair.
Its inputs are the accepted [H255 root](H-255-n17-exact-polynomial-root.md) and
[H256 centroid packing](H-256-n17-exact-endpoint-feasibility.md).
No target feature calculation has occurred at preregistration.

## Frozen Inputs and Criterion

Bind the H256 receipt to
`ad7a36ed0:packing/campaign/series/series-000-smoke-and-calibration/results/exp-238-n17-endpoint-feasibility/run-001/certificate.json`
and the H255 root to its accepted `7866e2623` Git blob.
Use the same midpoint and exact coordinatewise inclusion bounds, reconstructed centres,
bases and centroid sliders.
No root search, fitting, refinement, slider adjustment or alternate geometry is allowed.

For each of the 21 unordered zero-contact pairs, retain both owner labels, both local
edge-normal axes and both directed orders: eight labeled options, 168 in total.
A pair gap is the directed centre projection minus both support radii.
Do not deduplicate owner labels even when their axes coincide at the endpoint.

| Pair Kind | Pairs | Exact Zero Options | Strictly Negative Options |
| --- | --- | --- | --- |
| Parallel face interior | 9 | 18 | 54 |
| Cross-orientation contact | 11 | 11 | 77 |
| Additional 2/3 corner | 1 | 4 | 4 |
| Total | 21 | 33 | 135 |

The nine parallel-face pairs are 1/2, 1/3, 5/7, 9/10, 9/11, 11/12, 10/12, 13/14 and
12/14. Their centre displacements in the unit tangent direction must have entire exact
intervals inside $(-1,1)$. Pair 2/3 is a corner and is excluded from this strict
face-interior condition.

Audit all four vertices on each of the 15 active wall incidences: 60 corner clearances.
Fourteen axis-aligned wall incidences have two zero vertices each; square 9’s left-wall
incidence has one. Require exactly 29 symbolic zeros and 31 strictly positive interval
lower bounds. The other 53 wall incidences and 115 noncontact pairs remain covered by
accepted H256; this round does not repeat their proof or claim to inspect all 272
wall-corner combinations.

Declared zeros must follow from exact rational-function identities or the accepted root
polynomials with explicit normalizations.
They are assertions at the root, not zero intervals throughout the enclosure.
Every remaining alternative must have a strict sign on the entire enclosure.
An interval containing zero is never rounded into a decision.

The instrument also checks the nine explicit tangent-offset identities in the
[first-order derivation](../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md).
This binds the subsequent coefficient formulas without changing the sign criterion.

## Controls and Resource Limits

Before target use, independently review controls for parallel owner ties, corner-axis
alternatives, displaced contacts and walls, negative alternative gaps, omitted or
duplicate coverage, zero-straddling refusal and malformed or altered input.
Controls use synthetic geometry rather than reading the target.
Commit the instrument and controls before the single target run.

Use project Python with existing dependencies, one worker, a 180-second process timeout,
10 MiB per output and an optional 1 GiB data-segment cap where supported.
Record unsupported optional limits, host contention, phase timings, exact command, Git
state and exits. No automatic retry or changed classification is allowed.
Preserve every raw output.
Independent output review precedes acceptance.

The criterion is a complete contact-feature inventory.
A later first-order argument must still derive the nonsmooth owner-axis alternatives
correctly, certify any optimization result and distinguish stationarity from local or
global minimality. H027’s stronger class-angle threshold is a separate claim.

## Pretarget Instrument Review

Sol implemented the producer and synthetic controls.
Two Astra max reviewers and the coordinator checked raw owner coverage, the 22 distinct
identities underlying 33 labeled zero options, all 29 wall-corner identities, nine
tangent-offset identities, root normalizations and frozen prerequisite binding.
Seven target-free controls passed in 29.14 seconds; the uncached symbolic test accounted
for 28.33 seconds. Ruff and BasedPyright reported no findings.
The full symbolic test is measured and declared in the slow lane; the six remaining
controls stay on the pull-request surface.

Pretarget controls caught an expected-count typo, an exact-half type mismatch in the
interval corner helper, and a Python chained-comparison typo in a test.
All were corrected and controls rerun before any target evaluation.
The source/root/slider inputs and scientific criterion were not adjusted.
These are instrument-control corrections, not scientific outcomes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
