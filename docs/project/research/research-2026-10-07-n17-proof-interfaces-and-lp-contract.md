---
title: n17 Proof Interfaces and Finite-Angle LP Contract
date: 2026-10-07
status: research-contract
---
# n17 Proof Interfaces and Finite-Angle LP Contract

The fixed-container local theorem composes with a centred global search without moving
the packing after capture.
The finite-angle reconnaissance below uses 19 pairs, 27 allowed owner options and 256
feature branches. Its sampled values concern a specified relaxation; they do not
establish a widened terminal theorem.

This is the mathematical contract for BC-431 and BC-433 under the
[ten-hour plan](../specs/active/plan-2026-10-06-n17-ten-hour-session.md), derived from
source at `f3a13e3a2`. The coordinator owns hypothesis and experiment registration.
No new target measurement or verdict is recorded here.
The centred-container join is a hand derivation by the session’s sole Astra agent; it
has not received independent mathematical review or been machine-checked.
Existing receipts keep their existing assurance and scope.

## Proof Interfaces

Write $S^*$ for the accepted exact endpoint side, $U=1169/250$, $m=(U/2,U/2)$, and
$C(V)=[(U-V)/2,(U+V)/2]^2$. Every cell remains in the original $[0,U]^2$ cover frame.
A smaller cap changes the container walls, not the cells.
The endpoint family in that frame is $F(w)=x^*(w)+(\sigma,\sigma)$, with
$\sigma=(U-S^*)/2$ and $w=(a,b,z)$.

The [W3 consolidation](../reviews/review-2026-10-06-n17-w3-consolidation.md) records the
accepted local parts, the admitted residue and the capture failure.
The following obligations state how those parts can be used in one proof.

| Interface | Required input and implication | Evidence and check | Remaining obligation |
| --- | --- | --- | --- |
| Container normalization | A putative packing in side $s\le S^*$ is translated into $C(s)\subset C(S^*)\subset C(U)$. Preserve this placement thereafter. | The centred-container lemma below; inclusion is exact for ordered side lengths. | Independent review of this hand join; consumers must use the same walls and cell coordinates. |
| Closed-cell assignment | Every centre is in the closed cover. Choose one containing cell per square. Capacity one makes the chosen cells distinct, giving a 17-cell mask. Boundary membership may allow several masks. | exp-247 and `check_n17_capacity_one_cover`; the census must retain all geometrically allowed assignment masks. | A deterministic choice is safe only with a proof that its transported assignments remain represented. Discarding seam cases because they are non-generic is invalid. |
| D4 and labels | Apply a symmetry about $m$ to the packing, its chosen cell assignment and its angle axes together. Transfer the mask to its representative. In the endpoint mask, label each assigned square by the corresponding family cell. | Exact cover cell permutations and admitted consumer semantics; $gC(V)=C(V)$ for every $g\in D_4$. | Retain a symmetry/label witness. Handle the endpoint mask’s stabilizer explicitly: prove it fixes the target family modulo permitted labels/sliders, or capture every distinct stabilizer image. |
| Global exclusions | Each admitted exclusion rules out its declared cell subpattern at a declared cap $V\ge S^*$, with matching frame, cells and full closed-branch coverage. | Full certificate verification and admission ledger; a subpattern exclusion removes every containing assignment mask and its valid symmetry images. | Close or capture every remaining orbit. The current 36,784 states / 4,685 orbits under 58 entries are a residue, not a cover of terminal neighbourhoods. Held closures require their ruling. |
| Cap monotonicity | The normalized packing stays inside $C(S^*)\subseteq C(V)$ whenever a certificate uses $V\ge S^*$. | Exact inequalities for the certificate cap and the certified root enclosure. | Tightening a cap below $S^*$ is invalid; changing from centred to origin-anchored walls without transporting cells changes the claim. |
| Capture cap | Use a rational $U'$ proved to satisfy $S^*\le U'\le U$; the current design requests $0<U'-S^*\le10^{-12}$. Capture runs in $C(U')$ with the original cells. | Root certificate and outward side evaluation; retained producer configuration and verifier. | Prove the cap inequalities and input identities. A small cap excess does not itself bound a coordinate error. |
| Outer capture | Every packing in an unresolved cell state at the admitted cap reaches a declared terminal region, or is excluded. Every split retains a closed cover of its parent. | A complete capture/exclusion certificate from the actual cells. | Open. Success from a small pose box, contraction of a pilot box, or a widened terminal theorem alone does not cover the outer cells. |
| Coordinate frame and root | Capture returns bounds on the exact-root family in the same cover frame, with H254 angle lifts modulo $\pi/2$. | Layout identities, exp-237/238 root enclosures, and the explicit allowance below. | Certify all frame, centre, basis and angle conversion errors. Charge them to the delivered enclosure before comparison with the terminal radius. |
| Square 6 | In the endpoint assignment, the square labelled 6 has its centre in the complete closed `side-S2` cell, at any orientation. | exp-247 assignment and exp-248 slider coverage; `check_n17_slider_coverage.SIX_CELL`. | Keep the cell premise through symmetry and capture. No closeness premise on square 6 is licensed. Dropping it from the local/LP subsystem is a relaxation, not permission to drop it from slide coverage. |
| Slider domain | Once the 45 coordinates meet $r=1/5000$ and square 6 meets its cell premise, exp-248 places $(a,b,z)$ in $B_W'$ below. | The accepted slider composition and the local ratio receipt on $B_W'$. | A widened neighbourhood needs new slider coverage, or explicit capture bounds on the sliders. The old implication cannot be used at a larger radius. |
| Terminal radius | All 45 exact non-slider coordinates satisfy their componentwise closed bound $\le1/5000$. | exp-244/248 local theorem, with its reviewed hand lemmas and recorded ratio test. | Capture must establish every component, not only three widest owners or a scalar extent statistic. Use the correct 29 position functionals and 16 angles. |
| Terminal conclusion | Inside $C(S^*)$, the local theorem forces the sixteen retained squares onto $F(w)$; that family spans $S^*$ in both coordinates. | C10 and the fixed-container theorem in the [recipe](../reviews/review-2026-10-02-n17-local-theorem-recipe.md). | Combine the conclusion with the original containment in $C(s)$. This proves $s\ge S^*$ only after the exclusion/capture coverage obligations are discharged. |
| Evidence custody | The admitted ledger identifies complete retained objects, their checker, parameters and interpretation. | Hosted manifest, transfer integrity, full replay receipts and recorded admission. | Recover absent objects; representative replays do not replace required full verification. Missing custody blocks reproducibility even when the abstract implication is clear. |

### The centred-container lemma

Let $P$ be a packing in a square of side $s\le S^*$. Translate the centre of that
containing square to $m$; then

$$
P\subset C(s)\subset C(S^*)\subset C(U')\subset C(U).
$$

For any $g\in D_4$ about $m$, these containments also hold for $gP$. Suppose a
transported closed-cell assignment gives $gP$ the endpoint labels, square 6 is in
`side-S2`, and all 45 non-slider coordinates relative to $F$ are at most $r=1/5000$.
Translate $gP$ by $-(\sigma,\sigma)$. It is a packing in the fixed container
$[0,S^*]^2$, so apply slide coverage with the declared containing side $S=S^*$, then the
local theorem on $B_W'$. Its sixteen retained squares equal $x^*(w)$. These squares
touch both opposite walls in each coordinate at every permitted $w$; their coordinate
spans are therefore $S^*$. But $gP\subset C(s)$ has each span at most $s$. Thus
$s\ge S^*$; if $s<S^*$ there is a contradiction.

The theorem’s quantifier is containment in $[0,S^*]^2$. It does not require the declared
container to be the smallest one containing the configuration: the
[recipe’s theorem and corollary](../reviews/review-2026-10-02-n17-local-theorem-recipe.md#the-theorem-and-its-lemmas)
state this directly.
Consequently the equality choice $S=S^*$ is legitimate even when the original packing
fit inside a smaller square.
This use also satisfies slide coverage’s right-wall bound $x_5^*+1/2=S^*$.

No translation by $(S^*-s)/2$ is made after capture.
The argument therefore avoids the radius loss discussed for a change of embeddings in
the
[local-half composition](../reviews/review-2026-10-02-n17-local-half-composition.md#the-composition).
It supplies the abstract normalization and D4 join; an implementation that uses
different walls, labels or cell coordinates still needs a separate correction and
verification.

### Checks on the lemma’s scope

- Choosing the declared side $S^*$ does not prove that $s=S^*$ in advance.
  The family conclusion supplies the span bound only after all local premises hold.
- The local theorem covers the sixteen-square subsystem.
  The preceding slide-coverage step uses the full 17-square packing and square 6’s
  actual cell, with no assumed pose.
- A D4 transformation preserves centred boxes.
  A reflection also changes angle axes; relabelling cells alone does not transport the
  H254 angle chart.
- A mask in the endpoint orbit supplies labels, but supplies no metric closeness.
  That is still the capture obligation.
  Endpoint-mask stabilizers cannot be discarded.
- The argument uses the restricted capture-target theorem.
  It does not close H-261 as worded, whose unrestricted slider domain includes the
  square-5/6 exchange.
- The argument remains valid at $s=S^*$, where its conclusion describes the retained
  family. It claims neither uniqueness of square 6’s pose nor global uniqueness before
  the other states are handled.

### Exact-root allowance and coordinate inventory

Let $I=\{1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17\}$ and $J=I\setminus\{5,11,13\}$. The
45 quantities are the 16 lifted angle differences and these 29 position quantities, in a
single translated frame:

$$
y_5-y_5^*,\qquad
u^*\!\cdot(r_{11}-r_{11}^*),\qquad
u^*\!\cdot(r_{13}-r_{13}^*),\qquad
(x_i-x_i^*,y_i-y_i^*)\quad(i\in J).
$$

The projections kill the slides of 11 and 13 because $u^*\cdot v^*=0$. The omitted
position quantity of square 5 is its slide.
Every angle except square 6’s remains a non-slider quantity.

For each centre, enclose the exact cover-frame value $r_i^*$ around the value
$\widehat r_i$ used by capture with $\|r_i^*-\widehat r_i\|_\infty\le E_i$. This
enclosure includes any rounding of $\sigma$. Enclose $\|u^*-\widehat u\|_1\le E_u$ and
bound $\|r_i-\widehat r_i\|_\infty\le M_i$ on the entire captured set, including the
possible slider displacement.
Then

$$
\left|u^*\cdot(r_i-r_i^*)-
\widehat u\cdot(r_i-\widehat r_i)\right|
\le E_uM_i+\|u^*\|_1E_i.
$$

Ordinary coordinate errors need only the corresponding component allowance $E_i$. For an
angle, certify the H254 lift and add an outward bound on the nominal angle error to the
delivered angle radius.
If $R_j$ is the reported radius and $E_j$ its complete conversion allowance, the
terminal check is $R_j+E_j\le1/5000$ for every component.
Do not replace $r$ by a larger radius because the root enclosure is small.
The accepted root box has tiny parameter widths, but this consumer check still needs an
explicit bound and the actual representation used.

## Finite-Angle LP

### Variables, endpoint and position domain

The primal variables are $X=((x_i,y_i)_{i\in I},S)\in\mathbb R^{33}$. They are
unrestricted solver variables; containment and domain restrictions are explicit rows.
In particular there is no solver default $x_i\ge0$ standing in for a missing row, and no
imposed upper bound $S\le S^*$. The objective is $\min S$.

Use the accepted exp-237/238 root data and the centroid layout implemented by
[`_layout`](../../../packing/devtools/check_n17_endpoint_feasibility.py).
Its nominal axes are $(e_x,e_y)$ for $1$–$5$, $7$, $8$, $15$, $17$; $(u^*,v^*)$ for
$9$–$14$; and $(p^*,q^*)$ for $16$, whose nominal angle is $-\beta$. All centre and
domain formulas below use the same chosen endpoint representation.

For a **numerical reconnaissance**, the exact rational midpoint of the accepted root box
is an allowed nominal point.
It is not the exact root.
Record the root source, the midpoint parameters, the resulting nominal side $S_0$ and
the accepted exact-side enclosure separately.
Even exact rational arithmetic at that midpoint does not certify a claim at the
algebraic endpoint.

Define the slider projections by

$$
a=x_5^*-x_5,\qquad
b=-v^*\!\cdot(r_{11}-r_{11}^*),\qquad
z=v^*\!\cdot(r_{13}-r_{13}^*).
$$

The `bounded_tube` profile has six rows placing these projections in

$$
B_W'=[0,1/4]\times[-1/2500,1/12]\times[-1/8,1/16],
$$

and 58 rows bounding each of the 29 position quantities above by $\rho_p$ in absolute
value. The registration supplies the exact rational $\rho_p$. This is the affine family
with independent non-slider position errors; it does not pin the slider coordinates to
the centroid.

The comparison profiles are nested relaxations:

| Profile | Slider rows | Position-tube rows | Purpose |
| --- | ---: | ---: | --- |
| `bounded_tube` | 6 | 58 | Declared candidate terminal region |
| `drop_sliders` | 0 | 58 | Determine dependence on slider bounds |
| `free_positions` | 6 | 0 | Determine dependence on non-slider position bounds |
| `fully_relaxed` | 0 | 0 | Bare chain and containment relaxation |

Removing rows cannot increase an optimum, branch by branch or after the outer minimum.
The two middle profiles need not be ordered relative to each other.
The historical scratch V0/V2/V3 domains are not reconstructed by assigning those names
to different rows. At a widened radius, $B_W'$ is an explicit premise: exp-248 does not
prove that every packing in the widened tube has those sliders.

### Exact finite-angle rows

A point is a vector of 16 signed rational half-angle turns $q_i=\tan(\delta_i/2)$, in
the ordered label set $I$. Define

$$
c(q)=\frac{1-q^2}{1+q^2},\qquad d(q)=\frac{2q}{1+q^2},
$$

$$
u_i=c(q_i)u_i^*+d(q_i)v_i^*,\qquad
v_i=-d(q_i)u_i^*+c(q_i)v_i^*.
$$

The actual turn is $\delta_i=2\arctan q_i$. The half-angle parameter is not an angle in
radians. For any vector $n$, the support of square $i$ is exactly

$$
h_i(n)=\frac{|n\cdot u_i|+|n\cdot v_i|}{2}.
$$

Every point has 64 containment rows:

$$
x_i\ge h_i(e_x),\quad S-x_i\ge h_i(e_x),\quad
y_i\ge h_i(e_y),\quad S-y_i\ge h_i(e_y)\qquad(i\in I).
$$

For a selected option on an ordered pair $i<j$, let its signed owner normal be $n$. Its
one complete support row is

$$
n\cdot(r_j-r_i)\ge h_i(n)+h_j(n).
$$

At fixed angles this is linear in $X$, and is the full separating-axis inequality for
that owner normal. It uses neither a tangent row nor an assumed common perturbed angle.
The support’s absolute values are evaluated at that point; a later interval certificate
must enclose them or prove their sign branches separately.
With rational nominal axes and rational $q_i$, all row coefficients and right-hand sides
can be evaluated exactly as rationals before any conversion to a numerical solver.

### Pair and feature branches

Use `CONTACTS` from
[`check_n17_contact_chart`](../../../packing/devtools/check_n17_contact_chart.py), omit
$(9,11)$, and do not add the extra $(2,3)$ pair.
Filter [`option_manifest`](../../../packing/devtools/check_n17_endpoint_features.py) to
those 19 pairs and its `identity` options.
The resulting complete roster is below; an entry $+u_k$ means the current axis of owner
$k$, not a common global $u$.

| Ordered pair | Allowed signed owner normals |
| --- | --- |
| $(1,2)$ | $+u_1$ or $+u_2$ |
| $(1,3)$ | $+v_1$ or $+v_3$ |
| $(2,13)$ | $+u_{13}$ |
| $(3,9)$ | $+v_3$ |
| $(3,11)$ | $+u_{11}$ |
| $(4,10)$ | $-v_{10}$ |
| $(5,7)$ | $+v_5$ or $+v_7$ |
| $(7,14)$ | $+v_{14}$ |
| $(8,16)$ | $-v_{16}$ |
| $(9,10)$ | $+u_9$ or $+u_{10}$ |
| $(10,12)$ | $-v_{10}$ or $-v_{12}$ |
| $(10,15)$ | $+u_{10}$ |
| $(11,12)$ | $+u_{11}$ or $+u_{12}$ |
| $(12,14)$ | $-v_{12}$ or $-v_{14}$ |
| $(12,16)$ | $+u_{12}$ |
| $(13,14)$ | $+u_{13}$ or $+u_{14}$ |
| $(14,17)$ | $+u_{14}$ |
| $(15,16)$ | $+u_{16}$ |
| $(16,17)$ | $+u_{16}$ |

There are 11 singleton and 8 binary choices, hence 27 options and $2^8=256$ raw
branches. The 21-pair inventory has 33 identities; dropping $(2,3)$ removes four and
dropping $(9,11)$ removes two.
The nine parallel pairs in the full inventory include the dropped $(9,11)$. This
explains the branch-count correction to the
[historical scope](../reviews/review-2026-10-02-n17-widened-projection-scope.md).

For manifest axes, `ex/u/p` select the owner’s $u_i$, and `ey/v/q` its $v_i$; retain the
manifest’s pair-order sign.
Sort binary pairs lexicographically and select their lower/higher owner by bit 0/1,
respectively, for reproducible branch IDs 0 through 255. One branch chooses one of the
two normals on each binary pair.
Requiring both would replace a union by an intersection and could exclude valid
packings.

The `bounded_tube` branch has 147 inequalities: 64 containment, 19 pair, 6 slider and 58
tube rows. Square 6 and all unlisted pairs are absent.
An implementation may merge exactly equal branch row systems at a particular point, but
it must retain all raw branch IDs represented by each merged solve.
Approximate equality is insufficient for a certified merge.

This branch union is necessary for a real packing only after feature forcing is proved.
The 19 pairs have 152 raw owner-axis options; the 125 omitted options must have strictly
negative separation gap throughout the declared region, or another valid argument must
cover their alternatives.
The existing local proof supplies this at its certified radius and slider domain.
A wider tube requires a new proof.
The LP may investigate the conditional selected-feature system before that proof; its
report must say that feature coverage is unproved.

### Objective, dual and coverage signs

Normalize a branch as $AX\ge b$, with $c=e_S$. Its primal and dual are

$$
L_k=\inf\{c^{\mathsf T}X:AX\ge b\},\qquad
D_k=\sup\{b^{\mathsf T}\lambda:A^{\mathsf T}\lambda=c,
\ \lambda\ge0\}.
$$

Any feasible dual gives a lower bound for its branch.
A lower-valued dual sheet does not refute a stronger bound: other feasible duals can
raise the supremum. With the solver convention $A_{\rm ub}X\le b_{\rm ub}$, use
$A_{\rm ub}=-A$, $b_{\rm ub}=-b$; nonnegative multipliers satisfy
$c+A_{\rm ub}^{\mathsf T}\lambda=0$ and give $-b_{\rm ub}^{\mathsf T}\lambda$.

The union’s value is $L=\min_{0\le k<256}L_k$. Thus a pointwise lower bound needs a
valid bound or an infeasibility certificate for every branch.
A dual sheet from one branch says nothing about the other 255. For an exactly infeasible
branch, set $L_k=+\infty$ only after checking a Farkas certificate, for example
$\lambda\ge0$, $A^{\mathsf T}\lambda=0$, $b^{\mathsf T}\lambda>0$. Every feasible branch
is bounded below: containment implies $S\ge1$. A numerical `unbounded` outcome is
therefore a model/solver diagnostic requiring investigation.

Record execution coverage separately from mathematical coverage.
All 256 branches can have terminal numerical statuses while exact bound coverage is
still absent. A numerical infeasibility report may enter a labelled heuristic
aggregation; it does not supply certified $+\infty$. If any branch is omitted, times
out, errors or has unknown solver status, retain the solved branch results and mark the
point incomplete.
A minimum over only solved branches is an observed candidate value, not
a lower bound for the full union.

A feasible primal candidate with $S<S^*$ is a possible counterexample to the proposed
relaxation bound after exact-root and row verification.
It is not a 17-square packing counterexample: square 6 and many pairs were omitted.
Failure of one numerical dual is neither kind of counterexample.

## Reconnaissance and Controls

### Deterministic point semantics

The registration freezes the root representation, ordered labels, branch roster,
profiles, exact rational $\rho_p$, rational half-angle radii $\tau$, direction roster,
solver settings, tolerances and wall/worker ceilings before target execution.
It may instead freeze a fully specified direction generator and seed, provided the
generated roster is retained before the target solves begin.

A direction is an explicit integer vector $d\in\mathbb Z^{16}\setminus\{0\}$. At radius
$\tau>0$, construct

$$
q_i=\tau\,d_i/\|d\|_\infty.
$$

This has actual angular infinity radius $r_a=2\arctan\tau$. Store each rational $q_i$,
not merely a rounded displayed angle.
Coordinate directions are all $\pm e_i$ for the 16 labels.
Mixed directions have at least two nonzero entries; retain separate strata for
directions supported on the seven backbone labels $\{9,10,11,12,13,14,16\}$ and
directions using the full 16-angle system.
Include signed mixtures rather than only common-angle turns.
Exact duplicate points may share one evaluation with all sample aliases retained.

Seven-angle sampling supplies no reduction of the nine other angles.
That reduction would require a separate domination argument over their complete domains.
Similarly, a finite mixed-direction roster supplies no coverage of the direction sphere.
An adaptive adversarial follow-up is a separate recorded stage with its selection rule
and consumed budget, not an undisclosed change to the frozen sample.

Report the raw nominal gap $S_{\rm LP}-S_0$ and, for nonzero turns, its ratio to $r_a$.
A comparison to the accepted side enclosure is separate.
If a quadratic ratio is useful, label $(S_{\rm LP}-S_0)/r_a^2$ explicitly; the linear
slope and quadratic ratio are different measurements.
Use complete point evaluations, with their branch counts and deduplication, when
calibrating cost. A direction/radius point is not one LP solve.

### Readiness controls

| Control | Required observation or refusal |
| --- | --- |
| Finite support | Compare selected row supports with direct extrema of all four rotated vertices, including mixed and opposite-sign turns. Pair-order reversal with $n\mapsto-n$ must preserve the inequality. |
| Synthetic objective/dual | A small retained LP with known optimum verifies the solver’s inequality convention, unrestricted variables, multiplier sign, stationarity, complementary slackness and primal/dual gap reporting. Mutating a multiplier sign or omitting its identity must be refused. |
| Roster and coverage | Assert 19 pairs, 27 allowed options, 8 binary pairs, 256 raw branch IDs, 33 variables and profile row counts. Removing one branch alias must make the point incomplete. |
| Endpoint | At $q=0$, compare the objective and the nominal centroid’s row residuals with the accepted endpoint enclosure and a declared root-rounding/solver tolerance. Record the actual residual; do not replace it by zero. Parallel-owner rows coincide here, so merged solves must still account for all 256 branches. |
| Signed turns | Construct both signs of every coordinate turn. In particular positive turn of label 16 decreases its positive parameter $\beta$; label 16’s turn is not a positive $\beta$ increment. |
| Relaxed sliders | On matched complete points, `drop_sliders` cannot have a larger optimum than `bounded_tube` beyond the declared numerical tolerance. Also compare `fully_relaxed` to each restricted profile. No particular historical negative slope is required to reproduce. |
| Slider meaning | Construct the affine family at the centroid and declared box vertices and verify that the three projections recover $(a,b,z)$ and the 29 position quantities are zero. A vertex with $b<0$ need not be a physical packing. |
| Failure preservation | Exercise timeout/unknown/error and numerical-infeasible statuses. Preserve partial branch work and refuse a complete-union lower-bound claim. |

Run endpoint and relaxed-slider controls with the same source, rows and settings used by
the target. Tolerances are registration inputs; loosening one after a failure is a new
controlled run. A failed geometric or dual-sign control suspends dependent target
interpretation.

### Degeneracy, stop rules and later proof work

Record numerical primal residuals, dual residuals, objective gaps, solver status and
active-row information per solved branch.
A solver may return different valid bases at a degenerate optimum.
Row signatures and observed basis counts describe the sample; they do not count all
possible bases or unobserved direction patches.
If a proposed unseen-basis estimator is undefined or rests on nondegeneracy that was not
checked, its forecast is `unknown`. Do not turn zero observed novelty into zero
remaining proof cost.

The ten-hour plan mentions competing 100,000- and 1,000,000-patch routing figures.
Neither is an accept/kill threshold in this contract: a sampled basis census has not
been shown to estimate certified patches.
The first retained reconnaissance reports measured complete-point cost and observed
signatures.
Any later cost hypothesis must define its estimator, degeneracy treatment and
threshold before the applicable target.

Stop a point at its registered ceiling and retain partial work.
Stop interpretation on failed controls, missing branch coverage or a provenance/domain
mismatch. Positive sampled margins can justify scoping an interval-dual instrument; they
cannot accept a widened theorem.
A verified relaxation counterexample rejects that exact row/domain bound, while leaving
open a stronger subsystem or a smaller declared region.
Any changed region, omitted option rule or sample criterion is a new contract.

A widened terminal proof would still need complete angle-region and feature coverage,
verified dual or infeasibility certificates for every allowed branch, treatment of the
apex and equality set, exact-root arithmetic, and slider-domain coverage at the widened
radius. It would then replace the terminal-region obligation in the proof table.
Outer capture from the actual closed cells would remain separate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
