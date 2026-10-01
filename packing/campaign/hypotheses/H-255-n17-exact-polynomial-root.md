---
title: H-255 — exact existence of the n17 contact-chart root
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-255
  kind: hypothesis
  claim: The two exact n17 chart polynomials have a unique real root in the fixed rational box of radius 1e-12 around the retained source half-angles, and that box satisfies the original parameter and side-domain guards.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: Strict exact rational Krawczyk inclusion and contraction, with a nonsingular rational midpoint-Jacobian inverse and every frozen domain guard certified on the whole box.
    direction: Confirm only if the producer and separately implemented certificate checker agree, all synthetic controls pass and independent mathematical/output review finds no blocking defect. Failure to certify is unresolved, not a refutation of root existence. No radius adjustment or midpoint fitting is allowed in this round.
    threshold: 'rho = 1/1000000000000; each inclusion bound strictly below rho; contraction norm strictly below 1.'
  instrument: devtools.make_n17_root_certificate and devtools.check_n17_root_certificate; independently reviewed exact rational implementations with synthetic controls, committed before target computation.
  instrument_ready: true
  regime: Python standard-library Fraction arithmetic; fixed integer polynomials, source midpoint and radius; no Newton search, floating arithmetic, dependency changes or endpoint feasibility claim.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: One 20-minute instrument/control slice and one 90-second target certificate run, with a separate checker capped at90seconds; one worker and10MiB per output file.
  prereqs: [think-bj81]
  replication: false
  registered: '2026-10-01'
  notes: Exact root existence is one missing premise of the reviewed conditional minimum. Root existence alone is not a packing, an endpoint feasibility certificate, or a local/global optimality proof.
---
# H-255: Exact n17 Polynomial Root

The
[reviewed polynomial reduction](../../../docs/project/reviews/review-2026-10-01-post-optimality-w3-opening.md#smaller-root-isolation-problem)
fixes the two integer polynomials $F=(\Pi_2,\Pi_3)$ and their positive normalization
relative to the three contact equations.
The independently reviewed conditional theorem establishes uniqueness and minimal side
inside the declared necessary system if an exact root exists there.
This round tests only root existence and uniqueness in a smaller fixed box.

## Frozen Box and Acceptance Rule

Use exactly the H-253 source bytes and label map, already accepted by H-253 and H-254.
The midpoint $m=(t_9,-t_{16})$ consists of the source’s exact rational half-angle
parameters, without fitting or numerical refinement.
Set $\rho=10^{-12}$ and $X_i=[m_i-\rho,m_i+\rho]$ for both coordinates.
Every quantity below is evaluated using exact rational arithmetic.

1. Verify that $X$ lies in $[0.36,0.37]\times[0.33,0.34]$ and that throughout $X$ the
   positive denominators $t,L,D,E,K$ and the two original side guards hold:
   $187t^2-214t+53\ge0$ and $1169t^2-1338t+331\le0$.
2. Compute $F(m)$ and $J(m)$ exactly.
   Refuse a singular midpoint Jacobian.
   Compute its rational inverse $C$ and verify both $CJ(m)=I$ and $J(m)C=I$.
3. Enclose every polynomial derivative on $X$ by exact interval arithmetic to obtain
   $J(X)$, then enclose $M=I-CJ(X)$.
4. Let $q_i=\sum_j\max(|\inf M_{ij}|,|\sup M_{ij}|)$. Require $q=\max_i q_i<1$ and, for
   both rows, $|(CF(m))_i|+\rho q_i<\rho$.
5. A separately implemented checker must rederive the fixed polynomial system and its
   derivatives, independently recompute or validate all interval bounds, and verify the
   frozen source identity, midpoint, radius, domain, inverse and strict inequalities.
   It must not import the producer’s arithmetic or acceptance functions.

For $T(x)=x-CF(x)$, these conditions make $T$ a contraction taking the closed box
strictly into itself.
The fixed point is a root because $C$ is nonsingular; contraction gives uniqueness in
the box. This is an exact rational instance of the Krawczyk argument.
The independent implementation still uses the same mathematical method, so this is not
method-distinct confirmation.

## Controls and Resource Limits

The nontrivial positive control is $F=(x^2+2y-3,3x+y^2-4)$, with midpoint $(101/100,1)$
and radius $1/50$. Its exact root $(1,1)$ lies inside the box.
The hand-derived inverse is

$$
C=\begin{pmatrix}-50/49&50/49\cr75/49&-101/98\end{pmatrix}.
$$

The expected correction is $(99/9800,-3/19600)$, row norms are $(4/49,251/2450)$, and
inclusion bounds are $(23/1960,1079/490000)$, both strictly below $1/50$. Also test the
primitive product $[-2,3]\cdot[-5,-1]=[-15,10]$.

**Pretarget control correction, October 1.** The first handwritten control used
$C_{22}=-50/49$, with second correction $3/19600$, norm $5/49$, and bound $43/19600$.
Sol found that this matrix fails the required inverse identities.
The coordinator and independent checker author separately recomputed the determinant
$-49/25$ and the corrected values above before instrument tests or target execution.
Retain the incorrect matrix as a negative inverse control.
This correction changes no target polynomial, source, midpoint, radius or acceptance
inequality.

Negative controls must refuse an affine root outside the box, a root exactly on the
boundary, a singular midpoint Jacobian, and a wide box containing two roots despite a
nonsingular midpoint.
Mutations to the inverse, Jacobian interval endpoint, polynomial coefficient, source
identity and box must be rejected by the independent checker.
Malformed dimensions, floats, booleans, reversed intervals and zero-width boxes are
invalid inputs.

Commit both implementations after synthetic controls and independent review, before
target computation. Cap producer and checker separately at90seconds, with one worker,
10MiB output per file, and a1GiB memory cap where supported.
Retain unavailable guard notices, exact certificate, checker receipt, source/commit
provenance and separate preparation/producer/checker costs.
No retries change the midpoint, radius, polynomials or acceptance rule.

Even an accepted root does not certify endpoint containment or all pair separations.
Those require exact contact identities, certified noncontact inequalities and a joint
slider domain. Orientation, branch and parameter capture remain separate obligations.

## Instrument Review Before Target Use

Sol implemented the producer; Astra max implemented the checker without reading or
importing the producer’s arithmetic.
A separate Astra max reviewer checked both implementations against the fixed polynomial
derivation and the contraction theorem.
The coefficient maps, source-label indexing, positive normalization factors and both
side guards agree. Thirteen synthetic controls pass across the two implementations,
including a JSON serialization boundary.
Ruff and BasedPyright report no findings.

The review corrected a missing JSON field, enforced the stated tracked-clean Git
provenance and added structured refusals for malformed JSON. These were pretarget
instrument corrections.
No target midpoint or root certificate was evaluated during implementation or review.
The hand-control correction above remains part of the record.
Git records the reviewed implementation used by exp-237.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
