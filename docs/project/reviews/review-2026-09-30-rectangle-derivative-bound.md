---
title: Exact Rectangle Derivative Bound — Preregistered Diagnostic
date: '2026-09-30'
bead: think-r97y
status: in-progress
---
# Exact Rectangle Derivative Bound

The independent rectangle verifier has a reviewed Rust area kernel, but that kernel is
slower than the Python reference on the retained matched workloads.
The next experiment tests whether a stronger exact geometric bound removes enough
unresolved work to merit integration.
This supports the rectangle-certificate pipeline; the completed T-060 optimality proof
has a separate verification path.

## Frozen Question and Acceptance Rule

Registered before measurement on 2026-09-30 under `think-r97y`: does an exact signed
edge-chord derivative bound close at least one pending box that the current common-core
bound cannot close, across a complete fixed-work n11 frontier?

The diagnostic is promising only if all exact analytic controls and the independent
mathematical review pass, every frozen pending box is evaluated, at least one new box
crosses the same exact threshold, and the complete comparison takes at most 120 seconds
wall time. For this ceiling, add the separately reported preflight and diagnostic wall
times; only fresh frontier generation is excluded and reported separately.
A timeout or missing box gives an incomplete result, not an acceptance.
CPU and wall costs are reported separately.
This is a categorical screening experiment; a single timing is a resource observation,
not a speedup estimate.

Production adoption requires a subsequent complete, paired verification comparison with
unchanged coverage and acceptance conditions.
Neither a stronger bound nor a completed local diagnostic establishes full external
certificate acceptance or C++ performance parity.

## Input and Instrument

Freeze a fresh run from the current committed verifier source before comparing bounds:
angle 1, 1,000 visited nodes, maximum depth 48, exact cutoff
`2252024993666617/2251799813685248`, 30-second internal limit and 40-second outer limit.
Use the retained n11 candidate from the
[parity packet](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/).
The complete pending-box inventory produced by that run is the diagnostic input; its
size is an observation, not a required count.
The historical 13-box receipt pins an older checker and is not silently rebound to the
current implementation.

Record candidate and source identities, command and resource settings, complete box
coordinates, the common-core bound, exact midpoint coverage, both derivative intervals,
the derivative bound, the maximum bound, and threshold decisions.
Keep incomplete attempts and refusals distinguishable from completed results.

## Mathematical Contract

For a unit rational orientation with positive cosine and sine, the horizontal derivative
of rectangle-weighted square coverage is the signed sum of the vertical edge chords:
left minus right. The vertical derivative is bottom minus top.
Chord endpoints are minima and maxima of rational affine functions of the center.
Enclose each affine function over the entire center box before taking those extrema;
chord values at the box corners alone do not bound an interior maximum.

If `Gx` and `Gy` enclose those signed derivatives everywhere in the box, `m` is its
midpoint and `hx`, `hy` are its half-widths, the lower bound is

$$
\max\{0,L_{\mathrm{common}},F(m)-h_x\max|G_x|-h_y\max|G_y|\}.
$$

Coverage is absolutely continuous along coordinate segments.
The derivative identity holds almost everywhere, which suffices for integration through
tangent and event boundaries.
For fixed vertical center, each rectangle contribution is the integral of its clipped
vertical chord over a translated horizontal interval; differentiating the endpoints
gives the left-minus-right identity.
At a non-axis orientation the min/max-affine chord is continuous, so this argument
applies along each coordinate segment, including event boundaries.
The horizontal argument is identical.
The fundamental theorem of calculus then gives the stated midpoint lower bound.
All arithmetic is rational.
Split coincident edge segments at their exact endpoints and combine signed density jumps
before interval evaluation so equal adjacent densities cancel exactly.
Preserve duplicates and partial coincidences as mass.

The divided formulas refuse zero cosine or sine; the existing axis verifier remains
unchanged. Resource expiry must discard an unfinished sum.
The implementation has no runtime dependency on `verify.cpp`. The underlying identity is
shared mathematics, which does not establish confirmation by a distinct method.

## Required Controls

Controls cover constant coverage with zero gradient, equal-density cancellation, unequal
signed density jumps, translated asymmetric geometry at cosine 3/5 and sine 4/5, a point
center box, tangency and closed ties, an interior chord maximum across endpoint events,
near-axis orientation, zero-angle refusal, duplicate rectangles, and partly coincident
edges. Exact sampled coverage checks are regression controls; the whole-box guarantee
comes from the reviewed interval derivation.

## Outcome

Implementation and mathematical review are in progress.
No diagnostic measurements, threshold improvements, performance gains or new
verification credit are claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
