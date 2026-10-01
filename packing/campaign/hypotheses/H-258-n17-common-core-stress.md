---
title: "H-258 \u2014 exact common-core n17 first-order stress"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-258
  kind: hypothesis
  claim: The fixed analytic common-core stress at the accepted n17 endpoint has nonnegative weights and
    exact normalized stationarity identities, thereby excluding negative-side first-order directions in
    both complete corner branches.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: Exact52column stress residual identities, complete58commonrow weights and zero corner weight,
      with exact interval guards and nonnegative weights.
    direction: Confirm only if all52 normalized residuals vanish exactly at the H255root, all prescribed
      weights are nonnegative by exact identities or interval lowerbounds at leastzero, every denominator
      and normal-force guard is strictpositive, H257feature completeness is accepted, syntheticcontrols
      pass and independent mathematical/code/output review finds no blocking defect. Failed or unresolved
      bounds test only this fixed common-core stress; they do not refute stationarity or optimality.
    threshold: Exact A-transpose-lambda=e-side identity at the certified root; weight lowerbounds at leastzero
      with no tolerance; strictpositive denominator/force guards.
  instrument: devtools.check_n17_core_stress; deterministic symbolic stress construction, exact rational-function
    residual reduction and Fraction interval sign audit. No numerical optimizer or fitted parameters.
  instrument_ready: false
  regime: Unchanged H255 inclusion box and accepted H256centroid/H257feature inventory; fixed analytic
    force and torque allocation, no rootrefinement or alternate allocation.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: One25minute controlled implementation/review slice; one300second singleworker target,10MiB
    per output; independent output review beforeacceptance.
  prereqs:
  - think-wrgx
  - think-6dg0
  replication: false
  registered: '2026-10-01'
  notes: This is first-order stationarity of the complete local model, not local minimality, rigidity,
    nonlinear continuation or global optimality. H027 quantitativeclass-angle threshold remains separate.
---
# H-258: An Exact Common-Core First-Order Stress

This round tests one deterministic dual for the two complete n17 first-order branches.
The accepted [H255 root](H-255-n17-exact-polynomial-root.md),
[H256 endpoint](H-256-n17-exact-endpoint-feasibility.md), and accepted
[H257 feature inventory](H-257-n17-endpoint-contact-features.md) are prerequisites.
H257 output review is accepted before any H258 target arithmetic.
The
[core-stress derivation](../../../docs/project/reviews/review-2026-10-01-n17-core-stress.md)
fixes the complete force, torque and row-order contract.

The
[first-order derivation](../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md)
fixes all 52 variables and both 59-row branches.
This candidate assigns zero weight to each branch’s corner row and uses the same 58
common rows for both.
Preserve every row and variable, including structural zero weights and rattler
coordinates.

## Frozen Analytic Allocation

Use the H254 functions $F_1,F_2,G_3$ before eliminating the independent side $S$.
Differentiate with respect to the class angles while holding $S$ fixed, and only then
substitute $S=(6+4t)/(1+2t-t^2)$. Set

$$
\nu=(G_3)_\beta,\qquad \rho=-(F_2)_\beta,\qquad
\mu=-\frac{\nu(F_2)_\theta+\rho(G_3)_\theta}{(F_1)_\theta},
$$

$$
Z=\nu+\alpha\rho,\qquad L=\nu d/c,\qquad R=Ze/s.
$$

The contact-force and wall-force roster, axis torque allocation and five oblique-tree
moment formulas are fixed by the independently reviewed core-stress derivation before
instrument freeze. There is no numerical LP, coefficient fitting or alternative stress
search in this round.
For the five oblique tree edges use the prescribed baseline angular residuals $b_i$:

$$
q_{9,10}=-b_9,\quad q_{10,12}=-b_9-b_{10},\quad q_{11,12}=-b_{11},
\quad q_{13,14}=-b_{13},\quad q_{12,14}=b_{13}+b_{14}.
$$

A face with normal force $f$, offset $\tau$ and moment $q$ splits into the two reduced
row weights $E_-\mapsto(f+q/k)/2$ and $E_+\mapsto(f-q/k)/2$, with $k=(1-|\tau|)/2$.
Prove the sign branches used to simplify $|\tau|$; do not infer them from decimal
display. Axis-wall torque $m$ splits into $W_-\mapsto f/2-m$ and $W_+\mapsto f/2+m$. The
linked derivation fixes the complete row and variable order.
Normalize every weight by

$$
K=(c+s)\mu+\gamma\nu/c+\gamma Z/s+\gamma\rho(d+e)>0.
$$

Require every prescribed weight to be nonnegative.
The five oblique moment capacities $kf\pm q$ are explicit obligations.
An interval containing negative values and zero does not certify nonnegativity.
A structurally zero weight needs an exact identity.

For the stationarity equation $A^{\mathsf T}\lambda=e_\sigma$, prove 50 residuals
identically zero and reduce the remaining two to the prescribed opposite multiples at
$\omega_{12}$ equal to $+\rho\gamma F_2/K$ and at $\omega_{16}$ equal to
$-\rho\gamma F_2/K$, then use the accepted root identity $F_2=0$. An interval merely
containing zero is insufficient: the cone variables are unbounded.
Independently review every normalization and sign direction.

## Controls, Bounds and Disposition

Before the target, test parallel owner derivatives against the reduced rows for both
signs of relative angular velocity, including nonzero offsets and the corner limit;
check a rotating owner at a nonparallel contact; mutate a force, moment, residual sign,
normalization, row or required input.
Synthetic controls must not read the target.
Retain exact symbolic equalities and independently audit all interval conclusions.

Freeze the criterion, analytic recipe, instrument, controls and prerequisite Git blobs
before one target run.
Use existing dependencies, project Python, one worker, a 300-second process limit and 10
MiB per output; record an optional 1 GiB data-segment limit if supported.
Retain preparation, symbolic proof, interval checking and output costs separately where
measured. No automatic retry, root refinement or changed torque allocation is allowed
after observing output.

Acceptance proves nonnegative side velocity throughout the complete first-order model,
conditional on its accepted feature premises.
A certified strictly negative weight or moment-capacity interval rejects this fixed
allocation only. An interval straddling zero or a time limit leaves its sign unresolved.
A defective identity or invalid instrument requires repair and a separately registered
run, not an inference about feasible packing motions.
Other stresses may still work.
Even success leaves zero-side motions, higher-order local analysis and global
capture/exclusion as separate obligations.
It does not meet H027’s stronger quantitative class-angle criterion by substitution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
