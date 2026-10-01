---
title: Deterministic n17 Common-Core Stress Certificate
date: 2026-10-01
status: mathematical-review
---
# Deterministic n17 Common-Core Stress Certificate

A deterministic stress candidate reduces the n17 first-order stationarity question to
exact rational-function identities and signs of five face-moment allocations.
It uses the same 58 rows common to the two corner branches in the
[first-order review](review-2026-10-01-n17-first-order-branches.md), keeping all 52
variables. The corner row has weight zero in either branch.
A successful certificate would therefore prove nonnegative side velocity on both cones.
Failure of this candidate would leave other duals and nonlinear local minimality
unresolved.

The force and moment formulas below were derived without target arithmetic.
They need independent symbolic replay and the frozen sign test before any certificate is
accepted. No numerical LP, fitted weights, primitive-element construction, or bivariate
quotient-field implementation is required by this recipe.

The prerequisites are the accepted
[H255 root](../../../packing/campaign/hypotheses/H-255-n17-exact-polynomial-root.md),
the
[H256 endpoint](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md),
and the exact-root feature inventory specified in the first-order review.
Use the unchanged H254 centres, centroid sliders, and root enclosure.
The functions $F_1,F_2,G_3$ are those in the
[projection-branch review](review-2026-10-01-n17-projection-branches.md).

## Load Parameters and Derivative Convention

All angular derivatives here are partial derivatives with $S$ held fixed.
Compute the following rational formulas first, then substitute $S=(6+4t)/(1+2t-t^2)$.
Differentiating after that substitution would make $F_1$ identically zero and destroy
the required derivative.

$$
P=S-2-s+\frac{s(S-3)-2}{c},\qquad
Q=S-3+\frac{c(S-3)-2}{s},
$$

$$
P_\theta=\frac{S-3-2s}{c^2}-c,\qquad
Q_\theta=\frac{2c-S+3}{s^2},
$$

$$
(F_1)_\theta=-s(S-3)+c(S-2),\qquad
(F_2)_\theta=dP_\theta+eQ_\theta,\qquad
(F_2)_\beta=-eP+dQ,
$$

$$
(G_3)_\theta=c(S-3)-s(S-2)+e\alpha Q_\theta-e\gamma Q+\gamma-\alpha,
$$

$$
(G_3)_\beta=\gamma-\alpha+Q(\alpha d-\gamma e).
$$

Define the three load parameters and auxiliary force scales

$$
\nu=(G_3)_\beta,\qquad \rho=-(F_2)_\beta,\qquad
\mu=-\frac{\nu(F_2)_\theta+\rho(G_3)_\theta}{(F_1)_\theta},
$$

$$
Z=\nu+\alpha\rho,\qquad L=\frac{\nu d}{c},\qquad
R=\frac{Ze}{s}.
$$

The retained H254 coarse bounds give $\nu\ge0.127$, $\rho\ge0.000273$, $\rho\le0.105$,
and $(F_1)_\theta\ge0.9395165>0$. Also

$$
\nu(F_2)_\theta+\rho(G_3)_\theta
\le-0.127\cdot0.236+0.105\cdot0.037=-0.026087<0.
$$

Thus $\mu,\nu,\rho,Z,L,R$ are positive.
Every terminating decimal denotes an exact rational bound.
The two aggregate angular balances are built into the definitions:

$$
\nu(F_2)_\beta+\rho(G_3)_\beta=0,\qquad
\mu(F_1)_\theta+\nu(F_2)_\theta+\rho(G_3)_\theta=0.
$$

## Normal Forces and Side Normalization

A force here means the sum of the row weights for a parallel-face or tied-wall
constraint, or the single weight for a smooth constraint.
Use these unnormalized contact forces:

| Directed contact | Force |
| --- | --- |
| $1\to2:e_x$ | $cR$ |
| $1\to3:e_y$ | $s(L+\rho)$ |
| $5\to7:e_y$ | $c\mu$ |
| $3\to9:e_y$ | $sL$ |
| $9\to10:u$ | $L$ |
| $4\to10:w$ | $\mu$ |
| $3\to11:u$ | $\rho$ |
| $11\to12:u$ | $\rho$ |
| $10\to12:w$ | $\mu$ |
| $2\to13:u$ | $R$ |
| $13\to14:u$ | $R$ |
| $12\to14:w$ | $\mu$ |
| $10\to15:u$ | $L$ |
| $14\to17:u$ | $R$ |
| $15\to16:p$ | $\nu$ |
| $16\to8:q$ | $\gamma\rho$ |
| $14\to7:w$ | $\mu$ |
| $16\to17:p$ | $Z$ |
| $12\to16:u$ | $\rho$ |

The force on the parallel contact $9\to11:w$ is zero.
The wall forces are

| Wall | Force |
| --- | --- |
| 1 left | $cR$ |
| 1 bottom | $s(L+\rho)$ |
| 2 bottom | $sR$ |
| 3 left | $c\rho$ |
| 4 left | $s\mu$ |
| 4 top | $c\mu$ |
| 5 bottom | $c\mu$ |
| 7 right | $s\mu$ |
| 8 right | $e\gamma\rho$ |
| 8 top | $d\gamma\rho$ |
| 9 left | $cL$ |
| 15 top | $\gamma\nu/c$ |
| 17 right | $\gamma Z/s$ |

Walls 5 right and 6 bottom have zero force.
Each row at those tied walls, and both rows of the 9/11 face, receive zero weight.
This gives six prescribed zero weights among the 58 common rows.
All 52 variable columns remain in the identity check.

These forces balance translation at every square.
For example, square 15 has net force $Lu-\nu p-(\gamma\nu/c)e_y=0$, square 17 has
$Ru+Zp-(\gamma Z/s)e_x=0$, and square 16 has $\nu p-Zp-\gamma\rho q+\rho u=0$. The other
balances follow directly along the three chains, using the force table.
The checker must verify all 34 translational coefficients, including columns of squares
whose forces vanish.

The coefficient of side velocity is the sum of the right- and top-wall forces:

$$
K=(c+s)\mu+\frac{\gamma\nu}{c}+\frac{\gamma Z}{s}
+\gamma\rho(d+e)>0.
$$

Divide every final row weight by $K$. This fixes the side coefficient to one.

## Row and Moment Conventions

Freeze the column order as
$(\xi_1,\eta_1,\omega_1,\ldots,\xi_{17},\eta_{17},\omega_{17},\sigma)$. Emit wall rows
in the H254 anchor order: 1 left, 1 bottom, 2 bottom, 3 left, 4 left, 4 top, 5 right, 5
bottom, 6 bottom, 7 right, 8 right, 8 top, 9 left, 15 top, 17 right.
Within an axis-aligned wall emit $W_-$ followed by $W_+$; square 9 contributes one
smooth row. Then emit pair rows in the original H254 contact-table order:

$$
(1,2),(1,3),(5,7),(3,9),(9,10),(4,10),(3,11),(9,11),(11,12),(10,12),
$$

$$
(2,13),(13,14),(12,14),(10,15),(14,17),(15,16),(16,8),(14,7),(16,17),(12,16).
$$

Preserve these directed endpoint orders and their H254 normals.
Each parallel contact emits $E_-$ followed by $E_+$; each nonparallel contact emits its
single smooth row. The result is 29 wall rows followed by 29 pair rows.
Either corner row would be appended as a 59th row with weight zero, so neither belongs
to the stored common core.

For the smooth contact derivatives, use these fixed nonowner supporting-corner offsets
in the original directed normals: $(u+v)/2$ for $3\to9$; $(e_x-e_y)/2$ for $4\to10$,
$14\to7$, $15\to16$, and $16\to17$; $(p+q)/2$ for $12\to16$; and $(e_x+e_y)/2$ for the
other five nonparallel contacts.
Their dot-product signs follow from $c,s,d,e,\alpha,\gamma>0$ and must be checked as
guards, rather than inferred from a numerical sample.

For a parallel face $i\to j$ with normal $n$, tangential offset $\tau$, and total force
$f$, put $k=(1-|\tau|)/2>0$. Keep the rows in the explicit order

$$
E_-=n\cdot(V_j-V_i)+\frac{\tau}{2}(\omega_i+\omega_j)
-k(\omega_j-\omega_i),
$$

$$
E_+=n\cdot(V_j-V_i)+\frac{\tau}{2}(\omega_i+\omega_j)
+k(\omega_j-\omega_i).
$$

For a moment-allocation parameter $q$, assign

$$
\lambda_-^{\rm raw}=\frac{f+q/k}{2},\qquad
\lambda_+^{\rm raw}=\frac{f-q/k}{2}.
$$

The contributions to the source and target angular coefficients are respectively
$f\tau/2+q$ and $f\tau/2-q$. Both weights are nonnegative exactly when $|q|\le kf$.

For an axis-aligned active wall, write its two rows as $W_-=a-\omega_i/2$ and
$W_+=a+\omega_i/2$, with $a$ the appropriate translational and side expression from the
first-order review. A total force $f$ and angular moment $m$ give

$$
\lambda_-^{\rm raw}=f/2-m,\qquad
\lambda_+^{\rm raw}=f/2+m.
$$

The total angular contribution is $m$; nonnegativity is equivalent to $|m|\le f/2$.
Square 9’s smooth left-wall row retains its single weight $cL$.

## Deterministic Axis-Aligned Allocations

Define

$$
B_2=\frac{R(c-s)}2,\qquad
B_3=sL(1/2-s)+\frac{\rho(c-s)}2,\qquad
B_7=\frac{\mu(c-s)}2.
$$

Use $q_{12}=B_2$, $q_{13}=B_3$, and $q_{57}=B_7$ on the three axis-aligned faces.
The subscript $13$ here denotes the pair 1/3, not square 13. Allocate the wall moments
as follows:

| Wall | Moment |
| --- | --- |
| 1 left | $-B_2$ |
| 1 bottom | $-B_3$ |
| 2 bottom, 3 left, 4 left, 7 right, 8 right | $0$ |
| 4 top, 5 bottom | $-B_7$ |
| 8 top | $\gamma\rho(d-e)/2$ |
| 15 top | $\nu(ds/c-e)/2$ |
| 17 right | $Z(d-ec/s)/2$ |

The smooth-contact angular contributions at axis-aligned squares 2, 3, 4, 7, 8, 15, and
17 are respectively

$$
B_2,\quad B_3,\quad B_7,\quad B_7,\quad
\frac{\gamma\rho(e-d)}2,\quad
\frac{\nu(e-ds/c)}2,\quad\frac{Z(ec/s-d)}2.
$$

Those at squares 1 and 5 are zero.
Substitution of the face and wall allocations cancels every axis-aligned square’s
angular coefficient.
Square 6 has zero weight throughout.

These allocations satisfy their bounds throughout the H254 box.
In particular, $0<s<1$, $c>s$, and $c<2s$ imply

$$
|B_2|<cR/2,\qquad |B_7|<c\mu/2,\qquad
|B_3|\le sL|1/2-s|+\rho(c-s)/2<s(L+\rho)/2.
$$

The bounds for the moments at squares 15 and 17 use $|e-ds/c|<e+ds/c$ and
$|d-ec/s|<d+ec/s$. The remaining wall bounds follow from $0<s<c$ and $0<e<d$. No free
moment variables or numerical proposal remain in this block.

## Five Oblique Face Allocations

Form a baseline angular residual $b_i$ at each square 9 through 14 by using the listed
forces on every smooth contact and the smooth left wall, and splitting each
parallel-face force equally between $E_-,E_+$. Thus $q=0$ in this baseline, and each
face contributes $f\tau/2$ to both of its owners.
The generic owner-rotation derivative in the first-order review determines every
smooth-contact coefficient.
This is a direct recipe for $b_i$ from the independently built matrix, without fitting.

After removing the zero-force 9/11 edge, the oblique face graph is the tree with edges
$9\to10$, $10\to12$, $11\to12$, $12\to14$, and $13\to14$. Root it at square 12 and set

$$
q_{9,10}=-b_9,\qquad q_{10,12}=-b_9-b_{10},\qquad
q_{11,12}=-b_{11},
$$

$$
q_{13,14}=-b_{13},\qquad q_{12,14}=b_{13}+b_{14}.
$$

For example, the square-10 balance is $b_{10}-q_{9,10}+q_{10,12}=0$, and the square-14
balance is $b_{14}-q_{12,14}-q_{13,14}=0$. These signs correspond to the directed
contact table, not an independently sorted endpoint order.
The five nonroot balances vanish identically.
Square 12 retains the residual $\sum_{i=9}^{14}b_i$.

Use the exact offsets from the first-order review: $\delta$ for 9/10 and 11/12, $c(1-s)$
for 10/12, $c-s$ for 12/14, and $\delta+T/3$ for 13/14. All are positive on the retained
H254 box, so $k=(1-\tau)/2$ on these five faces.
The undecided acceptance clauses are

$$
|q_{ij}|\le\frac{1-\tau_{ij}}2f_{ij}
$$

for these five allocations, or equivalently nonnegativity of their ten row weights.
They must be checked on the unchanged accepted root enclosure under a frozen rule.
No alternative loads or moments are selected after seeing a failed bound.

## Exact Residual Identities

There is a short proof of the aggregate residuals that avoids constructing an algebraic
number field. Temporarily treat $\mu,\nu,\rho$ as formal constants.
At the H254 equality-chart centres, all weighted wall clearances and defining contact
gaps vanish. The three closing gaps are $F_1,F_2,F_3$ with forces $\mu,Z,\rho$. The
weighted sum of gaps is therefore

$$
\mu F_1+ZF_2+\rho F_3=\mu F_1+\nu F_2+\rho G_3.
$$

Differentiate with $S$ fixed along a common rotation of squares 9 through 14. Terms from
differentiating the centres cancel because translation is balanced.
Derivatives of the force coefficients multiply zero gaps except for the closing force
$Z$; $Z_\theta=-\gamma\rho$. Hence

$$
\sum_{i=9}^{14}b_i
=\mu(F_1)_\theta+\nu(F_2)_\theta+\rho(G_3)_\theta+\gamma\rho F_2.
$$

The same argument in $\beta$ uses $Z_\beta=-\gamma\rho$ and the physical angle $-\beta$
of square 16. Its angular residual is

$$
M_{16}=-\nu(F_2)_\beta-\rho(G_3)_\beta-\gamma\rho F_2.
$$

Now substitute the chosen load formulas.
The normalized matrix identity must have exactly these residuals:

$$
(A^{\mathsf T}\lambda-e_\sigma)_{\omega_{12}}
=\frac{\gamma\rho F_2}{K},\qquad
(A^{\mathsf T}\lambda-e_\sigma)_{\omega_{16}}
=-\frac{\gamma\rho F_2}{K},
$$

and zero in the other 50 columns.
The H255 root has $F_2=0$, so these identities give $A^{\mathsf T}\lambda=e_\sigma$ at
the root. They are rational-function identities after substituting $S(t)$ and can be
checked by exact cancellation before any target evaluation.
No small residual is promoted to zero.

## Bounded Certificate Contract

Freeze the complete 58-row order, 52-variable order, derivative convention, force
tables, moment formulas, and the accepted H255/H256/feature inputs before evaluation.
Retain the six prescribed zero weights explicitly.
Check all 52 residual identities against the two specified $F_2$ multiples, together
with the known positive normalization of $F_2$ to the H255 polynomial.
Require positive denominator guards, positive $K$, the correct offset branches, and a
certified nonnegative lower bound for every remaining normalized weight.
An undecided sign leaves this candidate unresolved; it does not permit changing its load
rule.

A separate checker can reconstruct the matrix and weights from the frozen formulas,
replay the exact identities, and recompute interval signs with independent arithmetic.
Synthetic controls should reverse a tree-edge moment sign, interchange the face row
weights, flip the physical square-16 angular sign, differentiate after substituting
$S(t)$, and omit one of the two exceptional residual columns.
Each mutation must fail the declared identity or guard.
A positive control checks the generic identities at symbolic parameters or unrelated
rational parameters without claiming those parameters are a feasible packing or a root.

A successful nonnegative dual is a first-order stationarity result under the complete
feature inventory. The retained zero-side motions and possible higher-order motion still
require a separate local-minimum argument.
The candidate gives no global coverage beyond the endpoint neighbourhood and does not by
itself meet H027’s quantitative class-angle derivative threshold.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
