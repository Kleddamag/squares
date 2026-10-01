# n12 Weighted Cycles: Exact Inequality and Capture Scope

## Registered Review Contract

**Registered:** October 1, 2026, 13:31 UTC, before the detailed review.
**Authorized slice:** 13:36–14:01 UTC, at most 25 minutes, within
[X-048’s low-n secondary work](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md).
This is a source and mathematical review, with no target evaluation, solver, sweep,
dependency change, or new bound claim.

The fixed source is the retained
[T4 cycle note](../../../packing/resources/web/evand-square-packing-2026-10-01/source/s12/search/T4_CYCLES.md),
especially its row convention in section 1 and cycle repair in sections 4 and 6. The
review tests the proposed extension to arbitrary nonnegative link weights, rather than
assuming the source’s numerical residual checks prove it.

The domain consists of finitely many fixed-orientation unit squares in a square
container, declared directed separating inequalities, all four container-wall
inequalities for each square, and a common additive margin in those rows.
Every weight must be nonnegative and the total row weight must be positive.
Zero weights and zero coordinate components are allowed.

Acceptance requires an exact hand derivation of every centre-coordinate cancellation,
the wall-weight signs, the constant term and positive normalization; an exact 45-degree
control recovering the source’s proposed bound; a non-axis turn control that detects the
invalid one-wall Euclidean repair; and an explicit statement of the additional
quantified coverage premise needed for a global packing conclusion.
An inequality with unproved row premises remains conditional.
Source searches and floating residuals are not independent verification, and a failed
certificate search is not an exclusion theorem.

## Result and Scope

The repaired cycle inequality is valid with arbitrary nonnegative link weights.
Its wall repair uses coordinate components of the force imbalance, not its Euclidean
length. The same proof applies to any finite directed graph, including a tree.
At side 4 this repair loses no certificate with a nonpositive margin bound on the
specified pair-row support.

This is a finite geometric inequality with declared separation premises.
It is not a first-order statement and does not depend on the incomplete H258 stress
instrument. It does not prove that the required rows occur in every packing, or give a
new lower bound for twelve squares.
The source’s sampled cycle searches do not establish that coverage statement.

## Exact Row Convention

Let square $i$ have centre $r_i=(x_i,y_i)$ and orthonormal edge directions $a_i,b_i$.
Its support function about the centre is

$$
H_i(v)=\frac{|v\cdot a_i|+|v\cdot b_i|}{2}.
$$

Write $P_i=H_i(e_x)=H_i(e_y)$. The equality is specific to squares, and
$1/2\le P_i\le\sqrt{2}/2$. The four wall inequalities in a container of side $T$, with a
common margin $\delta$, are

$$
x_i-\delta\ge P_i,\qquad -x_i-\delta\ge P_i-T,
$$

$$
y_i-\delta\ge P_i,\qquad -y_i-\delta\ge P_i-T.
$$

Choose a directed cycle $1\to2\to\cdots\to k\to1$. For each link choose a unit normal
$n_i$ and require

$$
n_i\cdot(r_{i+1}-r_i)-\delta\ge m_i,
\qquad m_i=H_i(n_i)+H_{i+1}(n_i),
$$

with cyclic indices.
A square’s edge normals are sufficient for exact pairwise separation, but the algebra
below is valid for any declared unit normals whose inequalities hold.
Pairwise nonoverlap does not imply an arbitrarily chosen directed normal inequality.
That premise must be checked or covered by alternatives.

The margin occurs once in every row, including the wall rows.
Changing that convention changes the denominator of the certificate.
Negative values of $\delta$ are permitted in the row system; they need not describe
nonoverlapping squares.

## Unequal Link Weights and the Wall Repair

Choose $f_i\ge0$, with at least one positive weight, and define

$$
d_i=f_i n_i-f_{i-1}n_{i-1},\qquad
D_i=|d_{i,x}|+|d_{i,y}|,
$$

$$
F=\sum_i f_i,\qquad D=\sum_iD_i,\qquad W=F+D>0.
$$

The weighted pair rows have centre coefficient $-d_i$ at vertex $i$. Assign the
following nonnegative wall weights at that square:

| Wall | Weight |
| --- | --- |
| Left | $(d_{i,x})_+$ |
| Right | $(-d_{i,x})_+$ |
| Bottom | $(d_{i,y})_+$ |
| Top | $(-d_{i,y})_+$ |

Here $z_+=\max(z,0)$. Their centre coefficient is exactly $d_i$, so every centre
coordinate cancels. Zero components and zero link weights require no separate branch.
Since $\sum_i d_i=0$, the total left and right weights are equal, and the total bottom
and top weights are equal.
This concerns weights, not the number of wall rows.
In particular the total right-plus-top weight is $D/2$.

The constant contributed by the wall rows is therefore

$$
\sum_i P_iD_i-\frac{T D}{2}.
$$

Adding the pair constants and cancelling the centres gives

$$
-W\delta\ge
\sum_i f_im_i+\sum_iP_iD_i-\frac{TD}{2}.
$$

Dividing by the strictly positive $W$ proves the weighted-cycle bound

$$
\boxed{\displaystyle
\delta\le
\frac{\sum_i(T/2-P_i)D_i-\sum_i f_im_i}{F+D}.}
$$

Every coefficient cancellation is exact.
No differentiability, small-angle condition, constraint qualification, numerical
residual, or optimization claim is used.
The orientations may be arbitrary; their support values remain part of the declared
data.

### The Same Inequality for a Directed Graph

For a finite directed graph, assign a normal $n_e$ and weight $f_e\ge0$ to each selected
row $e=(i,j)$, with pair support $m_e=H_i(n_e)+H_j(n_e)$. Replace the cycle imbalance by

$$
d_i=\sum_{e\text{ out of }i}f_en_e-
\sum_{e\text{ into }i}f_en_e.
$$

Again $\sum_i d_i=0$, and every preceding step is unchanged, with $F=\sum_e f_e$ and
pair term $\sum_e f_em_e$. Thus a cyclic graph is not required by the cancellation
mechanism. A tree or a disconnected selected support is permitted.
This does not establish the source’s proposed chain-plus-one-link coverage claim.

### What the Canonical Repair Loses

Any nonnegative wall weights producing coefficient $d_i$ have the form

$$
w_L=(d_{i,x})_++z_x,\qquad
w_R=(-d_{i,x})_++z_x,
$$

with $z_x\ge0$, and the analogous formula with $z_y\ge0$ for bottom and top.
The componentwise repair above minimizes total wall weight at that vertex.

An extra opposed wall pair of weight $z$ adds $2z$ to the denominator and $z(T-2P_i)$ to
the numerator of the margin bound.
For $T=4$, $T-2P_i\ge4-\sqrt2>0$. Consequently, if a different wall allocation with the
same pair weights has a nonpositive numerator, the canonical repair has a nonpositive
numerator too. It loses no certificate with a nonpositive bound on that fixed pair-row
support. This sign conclusion does not claim that the canonical repair minimizes every
positive numerical bound.

A certificate using only wall rows cannot have a nonpositive bound at $T=4$: centre
cancellation pairs opposing wall weights, and each nonzero such pair has positive
numerator $z(4-2P_i)$. Thus every certificate of the desired sign has $F>0$, and its
pair weights can be normalized by $F=1$ without changing the bound.
The remaining exact sign condition on a fixed support is

$$
\sum_e f_em_e\ge
\sum_i(2-P_i)
\left\Vert\sum_{e\text{ out of }i}f_en_e-
\sum_{e\text{ into }i}f_en_e\right\Vert_1.
$$

This removes the wall variables from that conditional certificate problem.
It does not supply the pair weights or a complete selection of valid row supports.

## Exact Hand Controls

### Common Tilt and the Source’s 45-Degree Value

At a common square orientation $\theta\in[0,\pi/2]$, put $u=\cos\theta+\sin\theta$. If
every link normal is an edge normal of these squares, then $P_i=u/2$ and $m_i=1$. The
bound becomes

$$
\delta\le\frac{(T-u)D/2-F}{F+D}
=\omega(T+2-u)-1,
\qquad \omega=\frac{D}{2(F+D)}.
$$

Here $\omega$ is the normalized total weight on the right and top walls.
This verifies the source’s scalar reduction for arbitrary link weights.

For an explicit four-cycle at 45 degrees, take unit link weights and successive normals
$a,a,b,b$, where

$$
a=(1,1)/\sqrt2,\qquad b=(-1,1)/\sqrt2.
$$

There are two nonzero imbalances: $a-b=(\sqrt2,0)$ and its negative.
Hence $F=4$, $D=2\sqrt2$, $P_i=\sqrt2/2$, and $T=4$ gives

$$
\delta\le\frac{4\sqrt2-6}{4+2\sqrt2}
=\frac{7\sqrt2-10}{2}<0.
$$

The strict sign follows from $98<100$. This is an exact certificate for the four
declared link inequalities and walls.
It recovers the value in the source’s section 4.3 without evaluating a pose or a solver.
It does not establish the source’s reported optimum: that additionally requires an
appropriate matching feasible point or a separate argument, and global n12 coverage
requires the cycle’s occurrence to be proved.

### A Non-Axis Turn Rejects the Euclidean Repair

Two unit normals can give imbalance $d=(1,1)$, for example $n_i=e_x$ and $n_{i-1}=-e_y$
at equal unit weights.
The pair-row coefficient at that vertex is $(-1,-1)$. A single axis wall with weight
$\Vert d\Vert_2=\sqrt2$ cannot cancel both coordinates.
Using the left wall leaves residual $(\sqrt2-1,-1)$; any other single wall also leaves a
nonzero coordinate.

The valid repair uses left and bottom walls, each at weight one, with total weight
$\Vert d\Vert_1=2$. A single-wall repair works only when the actual imbalance has at
most one nonzero coordinate.
The source’s 45-degree observation concerns a jump between the two edge normals of a
common orientation; it is not a restriction on every possible mixed-orientation turn.

### A Feasible Zero-Margin Control

Four axis-aligned squares with centres $(1/2,1/2)$, $(3/2,1/2)$, $(5/2,1/2)$ and
$(7/2,1/2)$ lie in the side-4 box.
Use the three consecutive $+e_x$ pair rows, each at weight one.
The directed-graph formula gives $F=3$, $D=2$, $P_i=1/2$, and $m_e=1$, so its bound is
exactly $\delta\le0$. The displayed squares satisfy every selected row at margin zero.
Thus a mutation that makes this bound strictly negative would contradict an exact
feasible control. Their shared edges are allowed here; they are not pairwise disjoint as
closed sets.

## The Global Coverage Obligation

The inequality is valid whenever its selected pair rows and walls hold.
A nonpositive right-hand side excludes positive common margin in that domain.
It does not follow that any arbitrary collection of separated squares has a cycle, graph
or weights giving that sign.

The reduction from a smaller packing to positive margin is exact.
Suppose unit squares with disjoint interiors fit in side $S<T$, and let $\lambda=T/S>1$.
Keep their orientations and multiply every centre by $\lambda$. For each pair, choose a
directed unit SAT normal that separates the original squares.
If its combined support is $m$, the new pair gap is at least $(\lambda-1)m$. Each new
wall gap is at least $(\lambda-1)P_i$. Since $m\ge1$ and $P_i\ge1/2$, all four walls and
one selected row for every pair satisfy the common positive margin

$$
\delta_0=\frac{T/S-1}{2}>0.
$$

For n12 at $T=4$, a sufficient global theorem would therefore assert: every such
strictly separated twelve-square configuration admits a selected valid row support and
nonnegative weights for which the proved bound is nonpositive.
A complete branch cover with exact exclusions would be another way to discharge the same
missing implication.
The support may depend on the configuration, but every possible orientation, owner-axis
alternative, degeneracy and zero weight must be covered.
Restrictions to minimizers or a normalized representative need their own reduction.

The dilation need not preserve a previously assigned point-pattern region such as the
rank-eight leaf in the
[RANK8 note](../../../packing/resources/web/evand-square-packing-2026-10-01/source/s12/search/RANK8.md).
Any classification by those regions must be proved for the dilated configuration or
shown to survive the transformation.
Excluding one leaf is not a complete n12 theorem.

## What the Retained Source Does and Does Not Verify

The source explicitly limits its cycle search to tight rows, cycles of length at most
nine, and a sampled subset when the cycle list is large.
Complementary slackness justifies tight support for a dual attaining an established
optimum; a certificate that merely reaches a nonpositive bound may use other rows.
Failure to find a successful cycle in that search therefore does not refute an
unrestricted cycle-existence statement.
The note’s headline that the chain-or-cycle dichotomy is false must be read at the scope
of its sampled restricted searches.

Likewise, a certificate found at each sampled negative-margin optimum does not cover the
positive-margin configurations that a hypothetical smaller packing would produce.
The reported tree, ladder and cycle frequencies describe selected solver outputs.
They do not establish a unique dual structure, and floating residual checks do not
establish exact cancellation.
No reported source optimization or geometric run was replayed in this review.

The exact reusable result is the conditional graph inequality and its wall-variable
elimination.
A future bounded discriminator can freeze one proposed support class and ask
for an exact sign certificate over a stated orientation domain, or test a precisely
quantified capture statement by its negation.
The present review selects neither a target evaluation nor a new hypothesis.
It sharpens the existing
[X-048 R5/R6 obligations](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md),
while the capacity-one obstruction owned by
[H248](../../../packing/campaign/hypotheses/H-248-n17-clique-weighted-family-at-4-675.md)
remains a separate question.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
