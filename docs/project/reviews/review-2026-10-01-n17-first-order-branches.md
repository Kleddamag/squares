---
title: n17 First-Order Branch Inventory and Capture Readiness
date: 2026-10-01
status: mathematical-review
---
# n17 First-Order Branch Inventory and Capture Readiness

The expected first-order nonoverlap model at the n17 centroid endpoint consists of two
linear cones, each described by 59 inequalities in 52 variables.
This count is a mathematical prediction conditional on the exact-root feature inventory
below.
It is not a measured cone certificate, a local minimum proof, or coverage of other
packing configurations.

The prerequisite geometry is the
[H254 contact chart](../../../packing/campaign/hypotheses/H-254-n17-contact-chart-fidelity.md)
at the
[H255 root](../../../packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md),
with the fixed centroid sliders and geometric obligations in
[H256](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md).
The [projection-branch theorem](review-2026-10-01-n17-projection-branches.md) proves a
minimum under particular directed projections and common-angle assumptions.
The first-order model here permits every square angle to vary independently and retains
all local separating-axis alternatives.
This derivation uses no target reads, numerical evaluation, or new root solve.

## Exact-Root Feature Audit Required First

For each touching pair $i<j$, retain eight raw separating-axis options: both square
owners, both basis axes of each owner, and both axis signs.
An option with normal $n$ has directed gap

$$
g_{ij,n}=n\cdot(r_j-r_i)-H_i(n)-H_j(n).
$$

Keep owner labels even when the two owners have identical normals at the endpoint.
Their normals rotate with different variables under an independent-angle perturbation.
The frozen inventory predicts the following counts:

| Contact type | Pairs | Zero options per pair | Negative options per pair | Total zero | Total negative |
| --- | --- | --- | --- | --- | --- |
| Parallel faces | 9 | 2 | 6 | 18 | 54 |
| Nonparallel contact with one owner axis | 11 | 1 | 7 | 11 | 77 |
| The 2/3 corner contact | 1 | 4 | 4 | 4 | 4 |
| Total | 21 |  |  | 33 | 135 |

The nine parallel contacts, in their directed orientations, are

$$
1\to2:e_x,\quad1\to3:e_y,\quad5\to7:e_y,\quad
9\to10:u,\quad9\to11:-v,\quad10\to12:-v,
$$

$$
11\to12:u,\quad12\to14:-v,\quad13\to14:u.
$$

Each named normal occurs as a zero option at both owners.
The remaining eleven contacts have the following predicted unique zero options,
expressed for the sorted pair direction $i\to j$:

| Sorted pair | Axis owner | Normal |
| --- | --- | --- |
| 3/9 | 3 | $e_y$ |
| 4/10 | 10 | $-v$ |
| 3/11 | 11 | $u$ |
| 2/13 | 13 | $u$ |
| 10/15 | 10 | $u$ |
| 14/17 | 14 | $u$ |
| 15/16 | 16 | $p$ |
| 8/16 | 16 | $-q$ |
| 7/14 | 14 | $v$ |
| 16/17 | 16 | $p$ |
| 12/16 | 12 | $u$ |

For the sorted pair 2/3, the zero options are $-e_x$ and $e_y$, each at both owners.
There are 33 raw zero options and 22 distinct zero directions across the 21 pairs.
Direction deduplication alone loses information needed for differentiation.

The fifteen active walls are

| Square | Walls |
| --- | --- |
| 1 | left, bottom |
| 2 | bottom |
| 3 | left |
| 4 | left, top |
| 5 | right, bottom |
| 6 | bottom |
| 7 | right |
| 8 | right, top |
| 9 | left |
| 15 | top |
| 17 | right |

Fourteen walls touch an edge of an axis-aligned square.
Each has two zero corner-wall clearances and two strictly positive ones.
Square 9’s left wall has one zero corner, at offset $(-u+v)/2$, and three strictly
positive ones. Thus the 60 corner incidences on these active walls comprise 29 zeros and
31 positive clearances.
An audit of all 68 walls would instead have 272 incidences: the same 29 zeros and 243
positive clearances.
These are different coverage scopes and must not share an ambiguous count.

The smallest feature audit binds to the accepted H255 enclosure $m\pm\eta$ and the
unchanged H256 reconstruction.
It proves the 33 declared pair zeros and 29 declared wall-corner zeros by exact
identities at the certified root; it proves all 135 other pair options strictly negative
and the 31 other active-wall corner clearances strictly positive by exact interval
bounds. It also checks strict interior overlap along each parallel face, as below.
The 53 inactive walls and 115 noncontact pairs retain their accepted H256 strict
margins.

Failure of an expected sign or an undecided interval prevents use of the predicted
inventory. It does not authorize dropping an alternative.
H254’s feature check was at the distinct rational source packing; H256’s noncontact
check does not by itself classify all alternatives at the zero contacts of the exact
root.

## First-Order Variables and Wall Rows

Let $\varepsilon\downarrow0$. Write translational velocities as $V_i=(\xi_i,\eta_i)$,
angular velocities in radians as $\omega_i$, and the side velocity as $\sigma$:

$$
r_i(\varepsilon)=r_i+\varepsilon V_i+o(\varepsilon),\qquad
\phi_i(\varepsilon)=\phi_i+\varepsilon\omega_i+o(\varepsilon),\qquad
S(\varepsilon)=S+\varepsilon\sigma+o(\varepsilon).
$$

There are $34+17+1=52$ variables.
In particular, the physical angle of square 16 is $-\beta$ at the endpoint; its velocity
is $\omega_{16}=-\dot\beta$ when using the class parameter $\beta$. No equality between
different $\omega_i$ is imposed in the full model.

At an axis-aligned square, the coordinate support radius has one-sided derivative
$|\omega_i|/2$. The active wall conditions are therefore

$$
\xi_i\ge|\omega_i|/2\quad\text{(left)},\qquad
\sigma-\xi_i\ge|\omega_i|/2\quad\text{(right)},
$$

$$
\eta_i\ge|\omega_i|/2\quad\text{(bottom)},\qquad
\sigma-\eta_i\ge|\omega_i|/2\quad\text{(top)}.
$$

Each is equivalent to two simultaneous linear inequalities, obtained by replacing the
absolute value with its two signed linear bounds.
At square 9 the left-wall support is smooth, giving the single row

$$
\xi_9-\frac{c-s}{2}\omega_9\ge0.
$$

The wall total is consequently $14\cdot2+1=29$ rows.
These rows preserve tied supporting corners; choosing one corner at an axis-aligned wall
would be incomplete.

## Parallel Faces: Two Owner Alternatives Become Two Simultaneous Rows

Let $J(x,y)=(-y,x)$. At a parallel-face contact choose the common directed normal $n$
and write

$$
r_j-r_i=n+\tau Jn,\qquad |\tau|<1.
$$

The normal projection is one because both squares have support radius $1/2$ along $n$.
The strict bound on $\tau$ means that the touching edges overlap in their interiors.
The perpendicular separating-axis alternatives have negative gaps and remain unavailable
in a sufficiently small neighbourhood.

The normal owned by square $i$ rotates as
$n_i(\varepsilon)=n+\varepsilon\omega_iJn+o(\varepsilon)$. Its owner’s support along
that normal is exactly $1/2$. The other square’s support is

$$
\frac{|\cos(\varepsilon(\omega_j-\omega_i))|
+|\sin(\varepsilon(\omega_j-\omega_i))|}{2}
=\frac12+\frac{\varepsilon}{2}|\omega_j-\omega_i|+o(\varepsilon).
$$

Thus the two owner-gap derivatives are

$$
D_i=n\cdot(V_j-V_i)+\tau\omega_i-\frac12|\omega_j-\omega_i|,
$$

$$
D_j=n\cdot(V_j-V_i)+\tau\omega_j-\frac12|\omega_j-\omega_i|.
$$

The absolute value records the changing extremal vertices; it is required even though
the base supports are tied.
Nonoverlap uses the disjunction of the two owner axes, so its first-order condition is
$\max(D_i,D_j)\ge0$. Direct algebra gives

$$
\max(D_i,D_j)=n\cdot(V_j-V_i)
+\frac{\tau}{2}(\omega_i+\omega_j)
-\frac{1-|\tau|}{2}|\omega_j-\omega_i|.
$$

Put $L=n\cdot(V_j-V_i)+\tau(\omega_i+\omega_j)/2$ and $k=(1-|\tau|)/2>0$. The condition
$L-k|\omega_j-\omega_i|\ge0$ is equivalent to the conjunction

$$
L-k(\omega_j-\omega_i)\ge0,\qquad
L+k(\omega_j-\omega_i)\ge0.
$$

This explains the reduction from an owner-axis disjunction to two simultaneous rows.
It is an exact identity of first-order expressions.
It does not assert that every vector satisfying those rows integrates to a feasible
nonlinear path.

The H254 reconstruction provides explicit offsets.
Put

$$
\delta=c(S-3)-s-c^2,\qquad T=c(c+4-S).
$$

The offsets are

| Contact | $\tau$ |
| --- | --- |
| $1\to2$, $1\to3$, $5\to7$ | $0$ |
| $9\to10$, $11\to12$ | $\delta$ |
| $9\to11$, $10\to12$ | $c(1-s)$ |
| $12\to14$ | $c-s$ |
| $13\to14$ | $\delta+T/3$ |

These formulas use the directed normals listed above, especially $J(-v)=u$. The feature
audit checks $|\tau|<1$ from the reconstructed coordinates at the accepted root.
The subsequent matrix builder must bind the displayed coefficient identities, including
the exact zero offsets; an interval containing zero alone does not determine the sign
needed to simplify $|\tau|$. The resulting face-contact contribution is $9\cdot2=18$
rows.

## Nonparallel Contacts and the 2/3 Corner

For a nonparallel contact, the proposed feature audit leaves one owner axis with zero
gap and strictly negative alternatives.
Its support on the other square is smooth.
It contributes one linear derivative row, with the rotation of the owning normal
included.

For an explicit formula, let $k$ be the axis owner, and let $a_\ell(n)$ be the unique
supporting corner offset of a nonowner square $\ell$ in direction $n$. Define
$h'_\ell(n)=Jn\cdot a_\ell(n)$, the derivative obtained by rotating the normal while
holding square $\ell$ fixed.
Its support derivative under both motions is $(\omega_k-\omega_\ell)h'_\ell(n)$. The
owner has zero support derivative along its own rotating normal.
Hence the gap derivative is

$$
n\cdot(V_j-V_i)+\omega_kJn\cdot(r_j-r_i)
-\sum_{\ell\in\lbrace i,j\rbrace\setminus\lbrace k\rbrace}
(\omega_k-\omega_\ell)h'_\ell(n).
$$

There are eleven such rows if the unique-axis prediction passes the feature audit.

At the 2/3 corner, $r_3-r_2=(-1,1)$. Both the direction $e_y$ from square 2 to square 3
and the direction $e_x$ from square 3 to square 2 can separate the pair.
Applying the preceding owner-max calculation at $\tau=1$ and $\tau=-1$ gives

$$
C_y=\eta_3-\eta_2+\frac{\omega_2+\omega_3}{2},\qquad
C_x=\xi_2-\xi_3-\frac{\omega_2+\omega_3}{2}.
$$

The pair’s first-order condition is $C_y\ge0$ **or** $C_x\ge0$. These are different
spatial separating directions, so the disjunction remains.
The four raw zero owner options have reduced to these two linear alternatives, not four
independent branches.

Thus the complete first-order model is the union of two cones.
Each has the same 29 wall rows, 18 parallel-face rows, and 11 nonparallel-contact rows,
together with one corner row: $29+18+11+1=59$. This count precedes any restriction to
class-angle velocities or deletion of duplicate rows after such a restriction.

## Zero-Side Motions and Valid Elimination

Square 6 has no active pair contact.
Its sole active constraint is its bottom wall, so its variables form the independent
factor

$$
K_6=\lbrace(\xi_6,\eta_6,\omega_6):\eta_6\ge|\omega_6|/2\rbrace.
$$

This factor is independent of $\sigma$. Setting all three variables to zero gives a
feasible extension of any vector in the remaining cone.
Projecting it out therefore preserves whether a negative-side first-order direction
exists, leaving 49 variables and 57 rows per branch.
This is elimination of an independent cone factor; $K_6$ is not a linear space of
motions that can all be reversed.

Square 13 has a two-sided translational direction $V_{13}=v$, with every other velocity
zero. Both of its active contacts have normal $u$, and it has no active wall.
This direction and its negative are lineality directions of both cones.
One may fix $v\cdot V_{13}=0$ as a linear gauge, leaving 48 variables and the same 57
rows. Its angular variable $\omega_{13}$ must remain.

The endpoint also has two one-sided motions involving other squares.
Square 5 can translate by $-a e_x$: its right-wall clearance increases by $a$, while its
bottom wall and the contact $5\to7$ along $e_y$ remain exact.
Square 11 can translate by $-b v$: the contact gap $9\to11$ along $-v$ increases by $b$,
while $3\to11$ and $11\to12$ along $u$ remain exact.
All other incident wall and pair obligations are strict in the H256 inventory.

These motions have a simultaneous quantitative certificate.
Let $\mu>0$ be the minimum of the 53 strict wall and 115 strict pair rational lower
bounds in an accepted H256 receipt.
For $0\le a,b<\mu/3$, the two translations leave every strict pair gap at least
$\mu-a-b>0$ and every strict wall gap at least $\mu-\max(a,b)>0$. The selected axes are
unit, so these bounds follow directly from the change in a projection.
The remaining zero contacts are unchanged; the two named clearances open.
This establishes an actual two-parameter family at unchanged side, using only the
already certified margins.

The corresponding first-order rays must be retained.
Their negatives close the right wall of square 5 or the contact $9\to11$, so treating
them as a removable linear subspace would discard constraints.
They also show why equality of the backbone angles does not recover every equality-chart
anchor or centre. In particular, the omitted $9\to11$ equality is not forced in every
physical endpoint packing.

## Smallest Subsequent Cone Certificate

After a successful exact-root feature audit, freeze the two matrices and the variable
convention before evaluating their cones.
With every row written as $Az\ge0$, a nonnegative vector $\lambda$ satisfying the exact
identity

$$
A^{\mathsf T}\lambda=e_\sigma
$$

proves $\sigma\ge0$ on that branch.
Both corner branches need a certificate.
The coefficients are algebraic quantities defined by the H255 root.
An exact symbolic identity reduced by the root equations, together with interval proofs
of the weight signs and denominator guards, would make such a certificate independently
checkable. A merely small floating or interval residual in
$A^{\mathsf T}\lambda-e_\sigma$ is insufficient because the other cone variables are
unbounded. A bounded normalization and explicit residual error can prove a quantitative
weaker statement, but must be reported with that bound.

Such a dual establishes first-order stationarity under the complete local branch
inventory. Zero-side directions require higher-order or exact continuation analysis
before they can settle a local minimum.
A vector with negative side in the first-order outer model also needs feasible
continuation before it proves a smaller packing.
Global optimality requires coverage of configurations outside this neighbourhood.

[H027](../../../packing/campaign/hypotheses/H-027-record-angle-cones.md) has a narrower
fixed-class regime and a quantitative minimum directional derivative over its declared
quotient unit sphere.
A class-angle restriction must be an explicit substitution in the complete matrices; it
must specify whether the axis-aligned class angle is fixed and which norm defines a unit
direction. A nonnegative-side cone dual alone does not meet H027’s $10^{-4}$ derivative
threshold or settle independent split-angle motions.

The [Trump tangent-cone tool](../../../packing/cases/trump11/tangent_cones.py) contains
owner-aware feature derivatives and exact certificate replay, but its 33-variable,
42-row fixed-side controls seek trivial cones.
The n17 zero-side motions rule out copying that isolation criterion.
The
[generic local-rigidity system](../../../packing/src/sqpack/local_rigidity/system.py)
refuses disjunctive touches; its current single-branch reduction cannot supply the 2/3
corner model. The [exact LP kernel](../../../packing/src/sqpack/exact_lp.py) provides
exact linear algebra and dual checking, while the present H255 root representation still
needs an explicit compatible algebraic coefficient and sign contract.
The
[n11 interval-dual audit](../../../packing/devtools/check_n11_optimality_local_dual.py)
labels its residual controls as partial arithmetic evidence, a distinction the n17
instrument must retain.

Synthetic controls for the new matrix builder should include parallel faces with
$\tau=0$ and nonzero $\tau$, each sign of the relative angular velocity, the $|\tau|=1$
corner limit, and a nonparallel contact whose axis owner rotates.
They should compare raw owner derivatives against the reduced formulas and reject
deduplication that erases owner rotation.
Complete coverage controls should mutate a missing zero option, an inactive option’s
sign, an active wall corner, and either corner branch.
No target evaluation is part of this readiness review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
