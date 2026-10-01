# n17 Mixed-Capacity Centre Cover

## Registered Mathematical and Census Contract

**Registered:** October 1, 2026, 13:46 UTC, before the occupancy census.
**Scope:** a source and exact mathematical review under
[X-048 R2](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md),
followed only after the coordinator’s separate preregistration by one bounded exact
count. No orientation search, geometric target evaluation, H258 retry, or global
exclusion is authorized by this review.

Freeze the rational container cap and centre-cell width

$$
U=\frac{1169}{250},\qquad
a=\frac{U-1}{5}=\frac{919}{1250}.
$$

Cover the complete closed centre box $[1/2,U-1/2]^2$ by its 25 closed axis-aligned grid
cells of side $a$. The proposed capacities are one for the 16 boundary cells and two for
the nine interior cells.
Assign each centre to the lexicographically least index pair of its containing closed
cells, so every centre has one deterministic label.
This tie rule does not discard cell boundaries.
Do not quotient the occupancy vectors by symmetry in this round.
For the arithmetic receipt, list the boundary cells first in spatial lexicographic
order, then the interior cells in that order.
This explicit permutation gives the input list of 16 ones followed by nine twos; it does
not change spatial seam ownership or the generating-polynomial coefficient.

Mathematical acceptance requires an exact support-function proof of boundary capacity
one, including both cases $c\le3/10$ and $c\ge3/10$, a diameter proof of interior
capacity two, and a complete-cover and seam-assignment argument.
All orientations are admitted.

The frozen census compares

$$
\operatorname{coeff}_{x^{17}}\bigl((1+x)^{16}(1+x+x^2)^9\bigr)
\quad\text{with}\quad
\binom{36}{17}.
$$

A reusable exact integer instrument must retain the full capacity list, coefficient,
baseline count and ratio, with independently reviewed small synthetic controls, before
the target is run. The coordinator owns its hypothesis, execution and acceptance.
A smaller count is a census improvement, not a packing exclusion or a global capture
theorem. No threshold on the count establishes that a subsequent geometric proof is
affordable.

## Result and Relation to the Eleven-Square Cover

The capacity claims below have an exact proof for every orientation.
The improvement uses containment at a wall, which is stronger than the centre-distance
test alone. The occupancy coefficient remains unevaluated at this mathematical review
checkpoint.

The accepted
[eleven-square proof, section 4](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md)
uses 16 closed Voronoi cells whose physical diameters are strictly below one.
Inscribed open disks of radius $1/2$ show that distinct centres of interior-disjoint
unit squares are at distance at least one.
Every cell therefore has capacity one, giving $\binom{16}{11}$ raw masks.
The cover, strict diameters, symmetry action and exclusions were all checked for that
geometry; none follows from the number of squares alone.

The accepted
[H256 endpoint packing](../../../packing/campaign/hypotheses/H-256-n17-exact-endpoint-feasibility.md)
fits under the present cap.
Its 17 distinct centres already rule out any complete cover by only 16 cells of capacity
one: choose a containing cell for each centre and apply the pigeonhole principle.
Thus the n11 cell count and binary-mask model cannot simply be copied.
Rescaling the old cells does not preserve their capacity proof.

A uniform five-by-five grid also fails if all 25 cells are assigned capacity one.
The exact interior-cell counterexample below shows this directly.
The wall argument permits the 16 boundary cells to retain capacity one while the nine
interior cells receive capacity two.

## A Support Inequality for Every Square Orientation

For a unit square at orientation $\phi$, write

$$
H_\phi(n)=\frac{|n\cdot a_\phi|+|n\cdot b_\phi|}{2},
\qquad h_\phi=H_\phi(e_x)=H_\phi(e_y),
$$

where $a_\phi,b_\phi$ are its orthonormal edge directions.
Let $n=(c,s)$ be a unit normal in the first quadrant, and put $t=c+s$. For every
$0\le A\le1$,

$$
\boxed{\displaystyle A h_\phi+H_\phi(n)\ge\frac{1+At}{2}.}
$$

To prove this, reduce $\phi$ modulo $\pi/2$ to $[0,\pi/2]$ and write
$\theta=\arg n\in[0,\pi/2]$. The only interior change of the support formula is at
$\phi=\theta$. On each interval between $0,\theta,\pi/2$, the function
$f(\phi)=A h_\phi+H_\phi(n)$ is positive and satisfies $f''=-f<0$. It is concave there,
so its minimum lies at an endpoint.
The two axis orientations give $(A+t)/2$, while alignment with $n$ gives $(1+At)/2$.
Since

$$
(A+t)-(1+At)=(1-A)(t-1)\ge0,
$$

the aligned value is a global minimum.
This includes $A=0$, $A=1$, axis normals and every square orientation.

## Every Wall Cell Has Capacity One

Consider two unit squares contained on the inward side of the left container wall, with
centres in

$$
[1/2,1/2+a]\times[y_0,y_0+a],\qquad 0<a\le3/4.
$$

Suppose they have disjoint interiors.
The separating-axis theorem supplies a directed unit normal along which their projection
gap is nonnegative. Exchange their labels if necessary to make its horizontal component
nonnegative, and reflect the tangential coordinate if necessary to make its vertical
component nonnegative.
These operations preserve the wall and cell premises.
Write this normal as $n=(c,s)$ with $c,s\ge0$, and set $t=c+s$.

Let square $i$ be the first square in the directed separation.
Containment gives $x_i\ge h_i$, the cell gives $x_j\le1/2+a$, and the tangential
coordinate difference is at most $a$. Therefore its projection gap satisfies

$$
\begin{aligned}
g&=n\cdot(r_j-r_i)-H_i(n)-H_j(n)\cr
&\le c(1/2+a)+sa-[c h_i+H_i(n)]-H_j(n)\cr
&\le at-1-\frac{c(t-1)}2.
\end{aligned}
$$

The last line uses the support inequality with $A=c$, together with $H_j(n)\ge1/2$.
There are two cases.

If $c\le3/10$, then $t\le1+c\le13/10$, so

$$
g\le\frac34\frac{13}{10}-1=-\frac1{40}<0.
$$

If $c\ge3/10$, first increase $a$ to $3/4$. The coefficient $3/4-c/2$ is nonnegative,
and $t\le\sqrt2$, giving

$$
\begin{aligned}
g&\le(3/4-c/2)t+c/2-1\cr
&\le\frac{3\sqrt2}{4}-1-\frac c2(\sqrt2-1)\cr
&\le\frac{12\sqrt2-17}{20}<0.
\end{aligned}
$$

The final strict sign is exactly $288<289$. Both cases contradict the nonnegative
separating gap. Thus the entire closed cell has capacity one, including its boundary.
Reflections and quarter turns give the other three container walls; corner cells need no
separate argument.

## Interior Capacity, Complete Cover and Seam Assignment

Divide any interior cell vertically into two closed rectangles of dimensions $a/2$ by
$a$. Each has squared diameter

$$
\frac{5a^2}{4}\le\frac{45}{64}<1.
$$

The inscribed-disk argument gives capacity one for each rectangle.
Assign a centre on their common seam to the left rectangle; every centre receives a
label. Three centres in the original cell would place two in one rectangle, so every
interior cell has capacity at most two.

For the chosen cap, $a=919/1250<3/4$. Every contained unit square has centre in
$[1/2,U-1/2]^2$, and the 25 closed grid cells cover that square exactly.
Assigning the lexicographically least containing index pair $(i,j)$, with
$0\le i,j\le4$, preserves containment in the selected closed cell.
The proved capacities therefore hold for the resulting occupancy vector.
The boundary cells are those with $i\in\lbrace0,4\rbrace$ or $j\in\lbrace0,4\rbrace$:
there are $25-9=16$. The remaining nine have capacity two.
No orientation, contact graph, owner choice or endpoint normalization is imposed on a
packing by this cover.

## Exact Interior-Cell Falsifier

The larger capacity is necessary for this grid.
Take the rational orthonormal basis

$$
u=(21/29,20/29),\qquad v=(-20/29,21/29),
$$

and two unit squares with that common basis and centres

$$
r_\pm=(U/2,U/2)\pm\frac{101}{200}u.
$$

Their maximum coordinate separation is

$$
\frac{2121}{2900}<\frac{919}{1250}=a,
\qquad a-\frac{2121}{2900}=\frac{277}{72500}>0.
$$

Both centres therefore lie strictly inside the central grid cell.
Each square has axis support $41/58<3/4$, and its centre is displaced from the container
centre by less than $3/8$ in either coordinate.
The total coordinate extent is less than $9/8<U/2$, proving strict containment.
Their directed separation along $u$ is $101/100$, while their support sum in that
direction is one. The pair gap is exactly $1/100>0$. Hence a universal capacity-one
assertion for the central cell is false, even for two squares separated as closed sets.
This is a hand-verified rational construction, not a numerical pose search.

## What the Accepted n17 Geometry Contributes

The
[H254 anchor roster](../../../packing/campaign/hypotheses/H-254-n17-contact-chart-fidelity.md)
contains 11 distinct wall-touching squares: labels $1$ through $9$, $15$ and $17$. Embed
the accepted endpoint of side $S$ in the cap by translating its centres through
$((U-S)/2,(U-S)/2)$, without scaling its unit squares.
The accepted side domain gives $0\le(U-S)/2\le1/2000$. Every wall-touching centre is at
most $\sqrt2/2+1/2000$ from its corresponding cap wall, strictly inside the boundary
layer of centre-cells ending at $1/2+a$. Those 11 centres therefore occupy distinct
boundary cells by the lemma above.

This uses the accepted geometry as a positive control without evaluating its grid
assignment or selecting one occupancy vector.
Its sliding freedoms remain admitted.
The statement that these particular 11 centres are in boundary cells is not a universal
lower bound of 11 on boundary occupancy in other n17 packings and must not be used as a
global cut.

## Exact Census to Be Run Separately

The model counts integer occupancy vectors, not permutations of labelled squares.
For capacities $c_1,\ldots,c_{25}$, its generating polynomial is

$$
\prod_{i=1}^{25}(1+x+\cdots+x^{c_i})
=(1+x)^{16}(1+x+x^2)^9.
$$

The coefficient of $x^{17}$ is therefore the complete count in this necessary occupancy
relaxation. An independent expression is obtained by choosing the $j$ interior cells
occupied twice, then choosing all singly occupied cells:

$$
\sum_{j=0}^{8}\binom9j\binom{25-j}{17-2j}.
$$

There is no multinomial factor for assigning square identities.
The census must retain the exact capacities and recurrence or binomial terms so that an
independent reader can reconstruct its meaning.

Before evaluating that coefficient, the sum of all coefficients already gives the
analytic ceiling

$$
2^{16}3^9=1,289,945,088<8,597,496,600=\binom{36}{17}.
$$

The right-hand value is the previously retained six-by-six binary-mask baseline in
[X-048](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md).
That baseline is valid at the same cap: a six-by-six cell has diameter strictly below
one.
The pending dynamic program will quantify the sharper comparison at occupancy 17; it
need not enumerate any vector or read an endpoint certificate.

No symmetry quotient is used.
The n11 parity shortcut cannot be copied blindly: this five-by-five grid has a cell
fixed by a half turn, and an odd total occupancy may therefore have a half-turn-fixed
vector. The deterministic seam assignment also needs care if a later symmetry transport
is introduced.

The census admits occupancy patterns that may be geometrically impossible.
Its count is not a count of packings or proof leaves, and the reduction alone gives no
measured cost per geometric exclusion.
Further cuts require independent validity over their whole domains and another declared
comparison. This result supplies a smaller complete occupancy problem; it does not solve
global capture or establish n17 optimality.

## Accepted Census

The coordinator accepted
[H259](../../../packing/campaign/hypotheses/H-259-n17-mixed-capacity-cover.md) after the
independent receipt review.
The
[frozen run](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-240-n17-mixed-capacity-census/run-001/)
at commit `b8e3e170f` returned 161,100,756 mixed-capacity occupancy vectors, compared
with 8,597,496,600 for the six-by-six binary baseline.
Their exact ratio is

$$
\frac{161100756}{8597496600}=\frac{4475021}{238819350}.
$$

Both independent arithmetic audits passed.
The recorded group took 0.35 seconds, including four Python process startups.
This is a measured reduction in the complete necessary occupancy census at the fixed
cap. It supplies no geometric exclusions and does not measure the cost of proving any
occupancy case impossible.
The values above were appended after acceptance; the earlier unevaluated checkpoint
records the order in which the mathematical criterion and target run were established.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
