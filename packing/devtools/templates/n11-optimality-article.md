<div class="hero">

# A Review of the Optimality Proof of the Trump Packing of 11 Squares

<div class="credits centred">
  <span>From the original proof by <strong>Queuingtheorydotcom</strong></span>
  <span><a href="https://github.com/Queuingtheorydotcom/11SquaresOptimal">github.com/Queuingtheorydotcom/11SquaresOptimal</a></span>
  <span class="credits-review">Human oversight: <a href="https://x.com/ojoshe"><strong>Joshua Levy</strong></a></span>
  <span>Agents: <strong>GPT-6 Astra</strong> and <strong>GPT-6 Sol</strong></span>
  <span>Draft v0.1.0</span>
  <span class="publication-date">Original proof September 29, 2026 · This review revised October 1, 2026</span>
</div>

</div>

This paper explains the computer-assisted optimality proof published by
[Queuingtheorydotcom in **11SquaresOptimal**](https://github.com/Queuingtheorydotcom/11SquaresOptimal).
The original
[mathematical argument](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/PROOF.md),
[verification driver](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/VERIFY.py),
[certificate data](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/data),
and
[reproduction instructions](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/docs/REPRODUCING.md)
are pinned to the source revision reviewed here.
[Queuingtheorydotcom’s announcement](https://x.com/MathCompSciFTW/status/2104772485816168618)
credits Astra’s work building on the Squares Project and Kleddamag.

The components have distinct provenance:

- **Attaining construction:** Walter Trump’s packing, with
  [David Ellsworth’s reconstruction and exact formulas](https://kingbird.myphotos.cc/packing/square-11.svg),
  retained in the
  [construction source record](../../resources/papers/kingbird-square-11-provenance.svg).
- **Mathematical antecedents:** the Squares Project’s
  [threshold-certificate method](../../cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md)
  and [local-isolation theorem](../../cases/trump11/isolation-theorem.md), together with
  [Kleddamag’s earlier lower-bound proof](https://github.com/Kleddamag/11-squares-certified-bound)
  that $s(11)>31/8$
  ([retained source](../../resources/web/external-square-certificates-2026-09-22/kleddamag-11/README.md)).
  The original proof’s
  [third-party notices](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/THIRD_PARTY_NOTICES.md)
  identify its incorporated Squares Project revision.
- **Verification and exposition here:** the Squares Project’s
  [T-060 result record](../../frontier/RESULTS.md),
  [retained proof and verification packet](../../resources/web/n11-optimality-2026-09-29/README.md),
  and
  [mathematical acceptance review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance)
  document the confirmation explained in this paper.[^credit]

For a technical review, start with the
[T-060 validation guide](../../resources/web/n11-optimality-2026-09-29/VALIDATION.md).
It links the published proof, certificate inputs, independent checks, and accepted
evidence for each obligation.
The guide distinguishes checking retained evidence from a fresh geometric replay and
states the remaining work needed for a standalone executable package.

## The Result

Place eleven unit squares inside a larger square.
Each small square may rotate independently.
Their edges may touch, but their interiors may not overlap.
How small can the container be?

The answer is the side length of Trump’s construction in Figure 1:

$$
s(11)=T=3.8770835900228141773078970601\ldots.
$$

This is an exact algebraic number.
Let $u$ be the unique real root in $(9/25,37/100)$ of

$$
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0.
$$

Then

$$
T=\frac{6u+4}{1+2u-u^2}.
$$

**Theorem.** Eleven congruent unit squares with arbitrary independent rotations and
pairwise disjoint interiors fit in a square of side $T$, and do not fit in any square of
side $S<T$.[^proof]

<figure>
{{WITNESS_SVG}}
<figcaption><strong>Figure 1.</strong> The attaining construction: six squares are
axis-aligned and five share a tilted orientation. The drawing is rounded for display;
the <a href="../../cases/trump11/verify_exact.py">exact witness check</a> uses algebraic coordinates.
Touching edges and corners are legal.
The construction reaches both opposite walls in each coordinate direction.</figcaption>
</figure>

An upper bound needs one example: the packing drawn above.
A lower bound must exclude every arrangement in a smaller container, including
unfamiliar contact patterns and eleven independently chosen angles.
Numerical search can suggest a good packing, but failing to find a better one does not
exhaust those possibilities.

Suppose a packing fits in a smaller square, of side $S<T$. The proof must handle that
packing without knowing any of its positions or angles.
It first classifies the centers and uses exact certificates to eliminate impossible
classes. Every survivor, after a symmetry of the container, enters a capture argument
that encloses its positions and angles near the known construction.

The last step connects this global restriction to a local theorem.
The same smaller packing can be placed inside the exact side-$T$ container, within a
checked neighborhood where only the construction is feasible.
But the construction spans $T$, so it cannot fit inside the smaller container.
Figure 2 shows both halves of the proof.

<figure>
{{ROADMAP_SVG}}
<figcaption><strong>Figure 2.</strong> Two routes to the exact optimum. The construction
supplies an upper bound. The lower-bound route follows an arbitrary hypothetical
smaller packing through restrictions that preserve every feasible possibility, ending
in a contradiction. The case counts classify continuous families of positions and
angles; they do not count individual packings. The
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/final-composition.json">accepted composition</a>
checks the joins between these obligations.</figcaption>
</figure>

The geometric steps are
[center classification](#sixteen-regions-cover-all-possible-centers),
[safe exclusions](#one-geometric-invariant-supports-the-certificates),
[symmetry](#symmetry-reduces-the-four-survivors-to-one), and
[capture](#capture-forces-case-438-near-the-construction).
The [local estimate](#the-local-argument-excludes-every-nonzero-motion) and
[exact frame change](#closing-the-gap-between-the-rational-cap-and-the-exact-optimum)
complete the contradiction.

The Squares Project records this result as **T-060, S5/V3/C3**: a result resolving the
global optimum, supported by exact computational verification and a mapped mathematical
review, machine-checked here with its review record pending.
Under the ladder of 2026-09-30, rung 4 on either axis also needs a second adversarial
review by a distinct reviewer and a retained human oversight record, which this result
awaits. This is a computer-assisted proof with a stated software trust base; a completed
proof-assistant formalization is not claimed.[^review]

## From Weighted Points to a Global Proof

The [earlier explainer][earlier] develops a lower-bound method based on weighted points.
Select a small **core** strictly inside each packed square.
If every possible core must collect at least one unit of weight, eleven disjoint cores
must collect at least eleven units.
A certificate with less than eleven units available proves a contradiction.
Exact coverage checks turn that idea into a theorem about every position and
orientation.

Threshold features strengthen the method by assigning weight when a prescribed condition
on several points holds.
The earlier paper explains the point certificate T-018, the threshold certificate T-025
and T-026’s dilation bound $s(11)\ge3.8264474\ldots$. Kleddamag’s subsequent T-037
establishes $s(11)>31/8=3.875$.[^lineage]

The gap between $3.875$ and $T$ is small, but closeness of two numbers supplies no
geometric information about a hypothetical packing in between.
The optimality proof adds two kinds of information.
It conditions geometric and charge arguments on occupied center regions, so they can
eliminate individual patterns.
For the pattern that survives, it proves where every square must be, then applies a
quantitative local theorem at the exact endpoint.

These are mathematical antecedents, not extra numerical assumptions.
The final proof does not infer equality from a sequence of improving lower bounds.
Nor is wand125’s separate check of certificate row minima, or Tokoharu’s C++
rectangle-density verifier, a verifier of this global optimality argument.
Those tools concern related certificates; the case exclusions, capture and local
endpoint require the additional checks below.[^tools]

## The Construction Gives One Half of the Answer

The algebraic parameter $u$ determines a rotation:

$$
c=\frac{1-u^2}{1+u^2},\qquad s=\frac{2u}{1+u^2},\qquad c^2+s^2=1.
$$

Here $c$ and $s$ are the cosine and sine of the common tilted orientation in Figure 1.
Appendix A gives the placement formulas.
Because a rotation preserves length and right angles, those formulas produce eleven unit
squares.

Feasibility has two finite checks.
Each of the 44 vertices must lie in $[0,T]^2$. Each of the 55 pairs of squares must
admit a **weak separating axis**: a direction in which their projection intervals have
disjoint interiors. For convex polygons it suffices to examine normals to their edges.
A zero gap is accepted, since it represents legal contact.

The calculations take place in the number field $\mathbb Q(u)$. Polynomial expressions
are reduced using the equation defining $u$; the selected root is isolated by rational
bounds. Exact identities establish zero, while rational interval refinement determines
the signs of nonzero expressions.
A small floating-point residual is never substituted for an equality.[^construction]

These checks prove $s(11)\le T$. The wall contacts also prove a fact needed at the end:
the construction’s horizontal and vertical spans are both exactly $T$.

## Sixteen Regions Cover All Possible Centers

Most of the global calculations use the rational number

$$
U=\frac{387708359002281417731}{10^{20}}>T.
$$

This **cap** is slightly larger than the proposed optimum.
If a packing existed in a square of side $S<T$, we could translate its container
concentrically into $[0,U]^2$. Its unit squares would keep their sizes, angles and
relative positions. Thus excluding possibilities in the cap also excludes them for every
smaller container.

A unit square contains an open disk of radius $1/2$ about its center.
Two packed squares therefore have centers at least one unit apart: otherwise those
disks, and hence the square interiors, would overlap.
Also, each center $p$ lies in $[1/2,U-1/2]^2$. Normalize this center domain by writing

$$
z=\frac{p-(1/2,1/2)}{U-1}\in[0,1]^2.
$$

Choose sixteen rational sites.
Assign each point of $[0,1]^2$ to any nearest site, keeping ties.
The resulting **closed Voronoi cells** cover the whole square.
They are the polygons in Figure 3, rather than the squares of a uniform grid.
The exact checker reconstructs them from nearest-site halfplanes and proves

$$
(U-1)^2\operatorname{diam}(C_j)^2<1
\qquad\text{for every cell }C_j.
$$

**Center-cover lemma.** A physical cell contains at most one packed-square center.
Indeed, two centers in it would be less than one unit apart, contradicting the disk
argument. At a cell boundary either containing label may be chosen; the same argument
still prevents two centers from receiving one label.[^cover]

<figure>
<div class="figure-pair">
{{COVER_SVG}}
{{MASK_SVG}}
</div>
<figcaption><strong>Figure 3.</strong> Left: the sixteen closed Voronoi cells, drawn
from rational vertices bound by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">retained cover receipt</a>.
Right: the eleven occupied cell labels of
case 438. A highlighted cell specifies where a center may be; it is not a small
square or an owned inner hull. Shared cell boundaries remain in the proof.</figcaption>
</figure>

<figure>
{{CAPACITY_SVG}}
<figcaption><strong>Figure 4.</strong> Why a center cell has capacity one. Two
hypothetical centers in the same cell would be less than one unit apart, so their open
radius-1/2 disks would overlap. Each disk lies inside its unit square, independent of
the square’s angle. The selected cell comes from the exact cover; the centers illustrate
the lemma and are not a candidate packing. The
<a href="../../devtools/check_n11_optimality_d4.py">cell checker</a>
proves the strict diameter bound for all sixteen closed cells.</figcaption>
</figure>

An eleven-square packing therefore chooses eleven different labels among sixteen.
There are

$$
\binom{16}{11}=4368
$$

possible subsets, called **masks**. A half-turn maps cell $j$ to cell $15-j$. No
eleven-element mask is fixed by this pairing, since a fixed mask would have even size.
Choosing one representative from each half-turn pair leaves 2,184 cases.
These representatives are sorted and numbered starting at zero.

The center-cover reduction permits every orientation.
For each square separately, write $t=\tan(\theta/2)$, with $0\le\theta\le\pi/2$. Then

$$
0\le t\le1,\qquad
\cos\theta=\frac{1-t^2}{1+t^2},\qquad
\sin\theta=\frac{2t}{1+t^2}.
$$

This rational parameterization makes interval calculations exact.
Both endpoints are retained, even though they describe the same square orientation.
Each certificate row covers a whole closed interval of $t$, not a sampled angle.

## One Geometric Invariant Supports the Certificates

Fix an occupied-cell pattern.
A **pose** is a square’s center and angle.
An **owner** is the square assigned to an occupied cell.
Although the packing is unknown, we can maintain two kinds of rigorous information about
each owner:

- An **outer pose cover** contains every center and angle still possible for that
  square. It consists of closed angle intervals with associated center polygons.
- An **owned hull** lies strictly inside that square in every valid packing under the
  current assumptions.
  It records points that the square must contain, even while its position is uncertain.

The first is an overestimate of possibilities; the second is a guaranteed interior.
In every valid packing under the current assumptions, each square’s pose belongs to its
outer cover and its interior contains its owned hull.
The outer cover may also retain artificial poses that no valid packing realizes.
The same invariant supports case exclusion and, later, capture near the construction.

### Removing poses that force overlap

Suppose another square must contain a small inner region.
A proposed position of our square is impossible if it forces their interiors to overlap.
We can reject a whole region of centers at once, provided the collision is guaranteed
for every angle in the row.
All other positions remain available until a further argument excludes them.

<figure>
{{POSE_SVG}}
<figcaption><strong>Figure 5.</strong> A schematic of one safe exclusion. A possible-center
region records uncertainty; a guaranteed inner region records what a valid packing must
contain. A translated strict core meeting the other square’s owned hull forces overlap.
The forbidden centers can be discarded, while the retained region remains an
overestimate. The drawing illustrates the
<a href="../../devtools/check_n11_generic_fresh.py">geometric checker’s</a>
invariant; it is not a certificate for the displayed schematic.</figcaption>
</figure>

For an angle interval, choose a convex core $Q$ around the origin that lies strictly
inside the centered unit square at every angle in the interval.
After substituting the half-angle formulas, the needed inequalities reduce to signs of
rational quadratic polynomials.
Checking endpoints and any interior minimum establishes the inequality over the entire
interval.

Let $K$ be an owned hull of another square.
A proposed center $x$ is forbidden if

$$
x\in K+(-Q)=\{k-q:k\in K,\ q\in Q\}.
$$

For such a center, $k=x+q$ belongs to both squares’ interiors.
This proves overlap.
The strict interior guarantees justify rejecting even the boundary of this closed
forbidden region.
If the cores merely touched the squares’ boundaries, the same rejection
could incorrectly remove a legal touching configuration.

<figure>
{{ROW_SVG}}
<figcaption><strong>Figure 6.</strong> One accepted row: case 2095, step 1, owner 10,
row 17, over the complete interval 17/32 ≤ t ≤ 9/16. The panels use retained exact
geometry, rounded only for display, and distinguish field center coordinates from
square-relative core offsets. This row contributes one triangular residual to the update. A complete
ownership update must also check every other row, closed angular coverage, common-core
inclusion and compression. The
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/generic-mask2095-intake/full-result.json">accepted case result</a>
and <a href="../../devtools/check_n11_generic_fresh.py">independent checker</a>
supply the evidence. This is an excluded noncandidate case, not the case-438 capture.</figcaption>
</figure>

A stronger collision check compares a proposed pose against another square’s entire
possible pose cover.
It may exclude the proposal only when collision is forced for every partner row,
including the endpoints of its angle intervals.

### Keeping everything else

Removing a list of forbidden polygons is insufficient unless the remainder is accounted
for. After independently justified wall and self-containment cuts, each update checks
that the accepted predecessor domain is covered by verified forbidden regions together
with the retained residual regions.
A larger proposed domain may contain impossible points that those necessary cuts already
remove. Exact arrangement checks include segments, singleton points and zero-area
intersections.
An area sum alone cannot detect a missing segment where a touching packing
might live.

After the complete surviving angle cover has been checked, points that lie strictly
inside the square for every surviving pose can be used as new owned points.
The corresponding convex hull is also strictly inside.
These points can then constrain the other squares.
Initial owned points need their own proofs, using open inscribed disks, wall
inequalities or independently checked seeds.

**Pose-preservation lemma.** Starting from a valid outer cover and valid ownership, each
accepted update preserves every actual packing under its stated assumptions.
If an occupied square’s complete pose cover becomes empty, the case is impossible.
If two independently established owned hulls intersect, the two square interiors overlap
and the case is again impossible.[^geometry]

The order of updates matters.
A point cannot be used as owned before the check establishing its ownership.
Parent and child states must match, and parallel updates must refer to their declared
common prior. The certificate consumers check these dependencies as well as the local
inequalities.

## Charge Budgets Exclude Many Patterns at Once

The weighted-point idea becomes more selective when the occupied cells are known.
A field certificate specifies a charge function on strict inner cores.
It proves that a square centered in cell $i$ must receive charge at least $q_i$, unless
it would collide with an already proved owned hull.
In a legal packing the collision alternative is unavailable, so the charge lower bound
must hold.

One useful charge is defined by five sites.
For each projection direction, consider the median of the five projected sites.
A core receives charge one when its projection interval contains that median in every
direction. The certificate reduces this condition to finitely many direction
inequalities. For the square cores used by these field certificates, directions parallel
to the core’s axes and normals to site-pair lines divide the directions into sectors.
Within each sector the median site and the signs in the core’s support function stay
fixed, so the inequalities are linear in the direction normal; the bounding directions
suffice. This definition concerns median projections; it does not say that the core
contains three of the five sites.

Two disjoint strict cores cannot both receive that charge.
A strictly separating direction gives them disjoint projection intervals, which cannot
both contain the same median.
The charge therefore has capacity one.
A checked example forces the squares in two occupied cells each to receive charge one,
giving $2>1$. Owned-point collision regions help prove that each cell must be charged,
but those collision regions add nothing to the charge budget.[^field]

<figure>
{{CHARGE_SVG}}
<figcaption><strong>Figure 7.</strong> Median-projection charge as a capacity argument.
In a separating direction, two disjoint strict cores have disjoint projection
intervals, so both cannot contain the same median. Receiving charge one requires the
median condition in every direction; a single projection illustrates the capacity
argument, not that full test. Required owners and a strict excess over the budget are
necessary for the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json">accepted field certificate</a>
to transfer to another mask.</figcaption>
</figure>

Suppose the charge function has total capacity $b$ across disjoint cores.
A certificate may require certain owner cells $O$ to be present and assign lower bounds
to cells in a set $P$. It excludes a mask $J$ only when

$$
O\subseteq J,
\qquad
\sum_{i\in P\cap J}q_i>b.
$$

This explains why one checked certificate can exclude many masks.
The masks must contain its required owners, and each must satisfy the strict budget
inequality. Neither an equal budget nor an unsupported transfer to a larger mask
suffices.

The accepted exclusion inventory combines **1,904 cases excluded by field certificates
and 276 other cases**. Its conclusion is the exact set equality

$$
E=\{0,\ldots,2183\}\setminus\{438,999,1462,1659\}.
$$

The check compares case identities and dependencies, not only the number 2,180. The
publisher groups the same excluded set by provenance as $1931+76+173$. These are
different groupings of the same obligation, not different totals or additional
exclusions.[^exclusions]

Some exclusions have extra assumptions that must be discharged.
In particular, the symmetry cuts used in cases 2175 and 2176 depend on the original
1,931-case baseline.
They cannot use the final four-survivor reduction to prove its own premise.
Case 1383 requires both sides of a closed center split at $y_{13}=4/3$. Here
$y_{13}=p_y-U/2$ is the centered physical height of the square assigned to cell 13.
Those branches and their common parent remain part of the accepted proof, even though
the common geometric invariant lets us describe them briefly.

## Symmetry Reduces the Four Survivors to One

Rotating or reflecting the entire container preserves feasibility.
It is tempting to rotate the cell labels and declare the four surviving masks
equivalent, but the irregular Voronoi cover does not permit that shortcut.
A quarter-turn or reflection need not send a whole cell to another cell.

Instead, consider four views of each normalized center:

$$
(x,y),\quad(1-x,y),\quad(1-y,x),\quad(y,x).
$$

Together with half-turns these represent the eight symmetries of a square, usually
called $D_4$. Intersect the inverse images of the cells in the four views.
The result is a finite overlay of 220 nonempty closed regions: 212 polygons and eight
singleton points. A center in one overlay region has a specified allowable label in each
view.

<figure>
{{SYMMETRY_SVG}}
<figcaption><strong>Figure 8.</strong> Four views of a center against the fixed cell
cover. The point changes position under square symmetries; the irregular cell polygons
are not permuted by those transformations. An overlay region records the allowed
cell labels in every view. This illustration explains the construction used by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json">accepted symmetry check</a>;
its exhaustive assignment search, including boundary ties and strict distance bans,
is a separate obligation.</figcaption>
</figure>

For two overlay regions, exact vertex calculations sometimes prove that every pair of
points, one in each region, is less than one unit apart in physical coordinates.
Such a pair cannot contain two centers.
The check retains 1,572 strict distance bans; a distance equal to one is not banned.

**Symmetry lemma.** Once the 2,180 exclusions hold, some square symmetry of every
remaining packing admits case 438. To prove this, suppose every view avoids 438 and its
half-turn. Each view must then have a mask from the other three candidates and their
half-turns. Exhaustive finite enumeration tries the compatible overlay assignments,
requiring distinct occupied labels in each view and respecting all distance bans.
None exists.[^symmetry]

Every genuine packing would supply such an assignment by choosing containing closed
cells in each view. Their nonexistence proves the lemma, including all boundary ties.
The enumeration may allow geometric arrangements that no real packing realizes; that
only makes its impossibility conclusion stronger.

## Capture Forces Case 438 Near the Construction

Case 438 specifies the occupied cells

$$
\{0,1,2,3,4,8,9,10,11,13,15\}.
$$

The pose-preservation invariant now serves a different purpose.
Rather than emptying every pose domain, the checks progressively enclose surviving poses
near the exact construction.
Initial ownership, fourteen root rounds and the subsequent capture graph are all
verified before the local theorem is invoked.

Three closed splits produce four possibilities.
Here square subscripts denote owner-cell labels; $y_{15}$ is a centered physical height
and $t_i$ is the half-angle parameter of the square assigned to cell $i$.

| Branch assumptions | Checked conclusion |
| --- | --- |
| $y_{15}\le5/4$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\le147/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\le183/512$ | Contradiction |
| $y_{15}\ge5/4$, $t_{13}\ge147/512$, $t_2\ge183/512$ | Enclosure in the local neighborhood |

Equality belongs to both sides of every split.
The overlap is harmless and prevents a missing boundary branch.

<figure>
{{CAPTURE_SVG}}
<figcaption><strong>Figure 9.</strong> The accepted ten-node capture ancestry.
Intermediate nodes propagate a checked state; three far leaves end in contradiction
and the near leaf encloses every surviving pose. Edges denote proof dependencies,
not trajectories of moving squares. Here y₁₅ = pᵧ − U/2 is a physical centered height
and tᵢ = tan(θᵢ/2) is an owner’s half-angle parameter.
Edge labels give each new closed split condition;
the branch table collects the inherited conditions. Both sides retain equality.
The near leaf is an enclosure; the fixed-T local theorem is still needed.
The fourteen root rounds precede the descendants shown here; the descendants’ parent
edges are bound by the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json">accepted source graph</a>.</figcaption>
</figure>

The final near state contains 136 live closed angular rows and 1,542 center vertices.
The inclusion checker proves that all their center polygons and all their angle
intervals lie inside the same local rectangle.
Convexity extends center bounds from vertices to whole polygons.
Exact bounds for $2\arctan(t)$ convert interval endpoints to angular displacements in
radians; intervals near the quarter-turn seam use the chart change $(t-1)/(t+1)$. A
half-angle parameter is never substituted for a radian angle.
The accepted ten nodes and nine parent edges bind this enclosure to the original
unconditional case, rather than to an assumed favorable starting pose.[^capture]

## The Local Argument Excludes Every Nonzero Motion

Fix the container as $[0,T]^2$ and label the eleven squares as in the exact
construction. A perturbation has 33 coordinates:

$$
h=(\Delta x_0,\Delta y_0,\Delta\theta_0,\ldots,
\Delta x_{10},\Delta y_{10},\Delta\theta_{10}).
$$

The checked local neighborhood is a rectangle $|h_j|\le r_j$, with positive coordinate
radii $r_j$. Different coordinates have different radii, allowing the rectangle to fit
the captured domains.
All radii lie within the analytic working box of radius $1/64$.

The local theorem excludes any nonzero displacement in this rectangle that remains
feasible in the fixed-$T$ container.
Its mechanism is quantitative: the linear gap constraints obstruct motion, and an exact
bound on their curvature proves that the nonlinear terms cannot overcome that
obstruction anywhere in the rectangle.

Write $\tau$ for the largest displacement as a fraction of its allowed coordinate
radius. A nonzero displacement has $0<\tau\le1$. The certificate for a coordinate
attaining that maximum forces $\tau\le c_j\tau^2$, with $c_j<1$. This is impossible:
throughout that interval, $c_j\tau^2<\tau$.

<figure>
{{LOCAL_SVG}}
<figcaption><strong>Figure 10.</strong> The local contradiction. The upper line is
τ and the lower curve is cτ², with a coefficient below one. A feasible
nonzero displacement would require the line to lie at or below the curve. This is an
algebraic illustration of the
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json">accepted exact inequalities</a>,
not a projection of the 33-dimensional feasible set. The theorem applies in the checked
rectangle inside the fixed side-T container.</figcaption>
</figure>

### Covering all possible local contact patterns

Nearby squares can change which edges separate them, so the proof must consider more
than one contact pattern.
The construction has fourteen contacting pairs.
Each pair has eight possible separation features: choose which square supplies the axis,
one of its two edge-normal directions, and a separation order.
There are 112 features altogether.
Exact signs show 24 available at the construction and 88 unavailable.
Taylor bounds prove that those 88 remain unavailable throughout the full rectangle.

For the remaining features, the check enumerates 512 raw choices, reducing identical
derivative systems to 128 branches.
Each has 42 necessary tied inequalities, including wall inequalities.
Omitting the constraints of pairs that do not touch at the construction weakens this
necessary system; it cannot discard a feasible packing.
Conversely, every feasible perturbation must select one of the checked branches.[^local]

### From a linear obstruction to a finite neighborhood

Let $g_i(h)$ be a gap that must be nonnegative in a chosen branch, with $g_i(0)=0$.
Write its linear part as $A_i h$. A linear calculation alone would describe only
infinitesimal motion.
To control an actual displacement, the proof bounds the quadratic remainder.

Normalize the size of a hypothetical nonzero displacement by

$$
\tau=\max_j\frac{|h_j|}{r_j},\qquad 0<\tau\le1,
\qquad R=\max_j r_j.
$$

The checked curvature bounds $K_i$ give the necessary inequalities

$$
A_i h\ge-\frac{\tau^2K_i}{2}.
$$

Choose a coordinate $j$ attaining $|h_j|=\tau r_j$, and choose the sign $\sigma$
opposite to $h_j$. A certificate supplies nonnegative rational weights $\lambda_i$ such
that

$$
\left\|\lambda^{\mathsf T}A-\sigma e_j^{\mathsf T}\right\|_1
\le\epsilon_j.
$$

Here $e_j$ selects coordinate $j$, and the norm sums absolute coefficient errors.
The weighted combination nearly isolates $\sigma h_j=-\tau r_j$. Its residual
contributes at most $\epsilon_j\tau R$. Multiplying the gap inequalities by the
nonnegative weights yields

$$
\tau r_j\le\epsilon_j\tau R+\frac{\tau^2M_j}{2},
\qquad M_j=\sum_i\lambda_iK_i.
$$

Every one of the $128\times33\times2=8,448$ certificates verifies the strict margin

$$
M_j<2(r_j-\epsilon_jR).
$$

The quantity $2(r_j-\epsilon_jR)$ is positive.
Rearranging gives

$$
\tau\le c_j\tau^2,
\qquad
c_j=\frac{M_j}{2(r_j-\epsilon_jR)}<1.
$$

This is impossible for $0<\tau\le1$: dividing by $\tau$ would give $1\le c_j\tau<1$. The
largest certified ratio is approximately $0.676505208$; the proof uses exact strict
comparisons, not this rounded display value.

**Local-isolation lemma.** The zero perturbation is the only feasible packing in the
declared labeled rectangle inside the fixed container $[0,T]^2$. The quadratic bounds
make this a theorem about a finite neighborhood, including its boundary.
Appendix B describes the curvature and negative-feature checks.

## Closing the Gap Between the Rational Cap and the Exact Optimum

The global geometry was computed at $U>T$, while isolation holds at the exact side $T$.
The conclusion needs a precise connection between the two frames.

Some certificates use field coordinates $p_f=Bp$, where

$$
L=191/50,\qquad B=L/U.
$$

In that frame the container has side $L$ and each small square has side $B$. This is a
change of coordinates; it is not a claim that eleven unit squares fit in a side-$L$
square.

Let $Q(x,y)=(-y,x)$ be the checked quarter-turn; undo it to align the captured case with
the construction. The local center corresponding to a field center is

$$
p_T=Q^{-1}\!\left(\frac{p_f}{B}-(U/2,U/2)\right)+(T/2,T/2).
$$

After undoing the field scale, this is a rigid rotation and translation.
An original side-$S$ container centered inside $U$ becomes

$$
[(T-S)/2,(T+S)/2]^2\subset[0,T]^2
\qquad(S<T).
$$

Its small squares are still unit squares.
The complete capture and inclusion checks place their labeled poses in the local
rectangle, and they are feasible in the fixed-$T$ container.
The local-isolation lemma forces them to be the exact construction.
But that construction spans $T$, so it cannot lie in a square of side $S<T$. This
contradiction excludes every smaller side directly.
Together with the exact witness, it proves $s(11)=T$.[^endpoint]

<figure>
{{ENDPOINT_SVG}}
<figcaption><strong>Figure 11.</strong> Why the rational cap settles the exact endpoint.
The same hypothetical side-S container, with S &lt; T, fits concentrically inside the cap
and then inside the fixed side-T container after the checked rigid alignment. Its
unit squares keep their size. Capture and
<a href="../../resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json">pose inclusion</a>
put the packing in the local rectangle; isolation forces the construction, whose span
T contradicts its containment in side S. Gaps are exaggerated for visibility;
the drawing does not depict a feasible smaller packing.</figcaption>
</figure>

This deduction does not rule out perturbations in the larger cap $U$. It needs only the
impossibility of a smaller packing.
It also makes no separate claim of global uniqueness of all optimal packings.

## What Was Verified, and What the Verification Means

The public proof source is
[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c),
linked at the revision that was confirmed.
The Squares Project’s confirmation uses independently written consumers of its proposed
certificate data and a mathematical review of the implications above.
The accepted computation covers the required proof ensemble, including all 2,180
exclusions and all ten capture nodes.[^review]

| Mathematical obligation | Accepted evidence |
| --- | --- |
| Exact endpoint and matching upper bound | Algebraic root, unit-square construction, 44 vertex containment checks, 55 pair checks, $T<U$, opposite-wall span |
| Exhaustive global classification | Sixteen closed cells, 4,368 masks, 2,184 half-turn representatives |
| Noncandidate impossibility | Exact 2,180-case exclusion set with discharged conditional premises |
| Reduction to case 438 | Closed symmetry overlay and exhaustive assignment check |
| Capture | Complete root induction, ten nodes, nine parent joins and all four closed leaves |
| Local isolation and inclusion | Complete feature census, 8,448 dual checks, nonlinear bounds and enclosure of the accepted near state |
| Final theorem | Composition of those premises with the rigid smaller-container embedding |

Search programs may choose promising cuts, cores or dual weights.
They need not be trusted to find correct ones: a certificate checker recomputes the
finite conditions that make each proposal sound.
The review must still establish why those conditions imply the continuous geometric
claim. Reexecution tests reproducibility; it does not, by itself, prove that a checker
implements a sound mathematical rule.

The independence has limits.
The local construction, derivative calculations and exact arithmetic include shared
first-party primitives.
The confirmation follows the same mathematical argument, rather than supplying a
distinct proof method.
V3/C3 consequently means a machine certificate replayed here with its review record
pending, not distinct-method confirmation, not the adversarially reviewed and
human-overseen rung 4, and not V5 formal verification.
The trust base includes the reviewed mathematical reductions, checker source, arithmetic
libraries, runtime and executing system.

The final composition receipt reconciles the completed geometric executions and their
reviewed dependencies.
It does **not** rerun those calculations.
Four stale final-state digest bindings in the publisher’s packet prevented accepting its
unchanged full runner as a successful replay; the independent confirmation uses freshly
observed component executions and checked state joins instead.
A fresh one-command rerun of the entire independent ensemble still needs a reviewed way
to rebind newly generated parent receipts, whose timing fields change their bytes.
That automation issue is tracked separately from the completed mathematical
obligations.[^reproduce]

The [T-060 validation guide][reproduction] separates fast checks of retained evidence
from fresh geometric replay, and links each checker, source binding and recorded
execution. It is the place to reproduce a component; merely rerunning the final composer
is not an independent end-to-end proof run.

## Appendix A: Exact Placement Formulas

For a direct construction, let $A(a,b)=[a,a+1]\times[b,b+1]$, and define

$$
\begin{aligned}
\rho&=1-(T-3)c, &
\eta&=\frac{(1+\rho)c-1}{s},\\
v&=c-s, &
\zeta&=\frac{T-1}{s}-\rho-(3+\eta)\frac{c}{s},\\
x_0&=1+\frac{2}{c}-(T-2)\frac{s}{c}.
\end{aligned}
$$

The six axis-aligned squares are

$$
\begin{gathered}
A(0,0),\quad A(T-1,0),\quad A(x_0,T-1),\\
A(0,T-1),\quad A(1,T-1),\quad A(0,T-2).
\end{gathered}
$$

Define the rigid map

$$
F(x,y)=(1,1)+
\begin{pmatrix}c&-s\\s&c\end{pmatrix}(x,y-\rho).
$$

The remaining five squares are the images under $F$ of

$$
\begin{gathered}
A(0,0),\quad A(\eta,-1),\quad A(1,v),\\
A(\eta+1,v-1),\quad A(\eta+2,-\zeta).
\end{gathered}
$$

All quantities are elements of $\mathbb Q(u)$. These formulas, together with the
isolated root, specify the construction without relying on coordinates read from a
drawing.[^construction]

## Appendix B: The Nonlinear Estimates

For a pair gap, let square $o$ supply the separating axis and square $p$ supply the
tested corner. Put $w_i=r_{3i+2}$ for square $i$’s angular radius.
A bound on the second derivative along any direction in the coordinate rectangle is

$$
\begin{aligned}
K={}&D_{op}w_o^2\\
&+2\sqrt{(r_{3o}+r_{3p})^2+(r_{3o+1}+r_{3p+1})^2}\,w_o\\
&+\frac{(w_o+w_p)^2}{\sqrt2}.
\end{aligned}
$$

Here $D_{op}$ bounds center separation throughout the analytic working box.
The terms bound the rotation of the center projection, the mixed translation–rotation
derivative and the relative rotation of the corner.
A wall gap has $K=w_i^2/\sqrt2$. Checked rational upper bounds replace the square roots.
When several elementary gap functions share one gradient, the checker uses the largest
applicable curvature bound.

An unavailable separation feature has a corner gap $g$ with $g(0)<0$. The checker
establishes

$$
g(0)+\sum_j|\partial_jg(0)|r_j+K/2<0.
$$

Taylor’s theorem then keeps that corner gap negative throughout the closed rectangle.
The feature cannot become available there.
These 88 exclusions, the exhaustive remaining feature choices, and the
curvature-weighted dual inequalities supply the nonlinear premises of local
isolation.[^local]

## Sources and Verification Record

The [simplification review][simplification] freezes the dependency map used in this
exposition. It consolidates repeated geometric rules and the endpoint argument without
claiming fewer necessary cases, rounds or branches.
The figures are explanatory renderings of retained data; their rounded screen
coordinates are not inputs to certificate acceptance.

[^credit]: [T-060 attribution and evidence](../../frontier/results.yaml);
    [upstream source and third-party credits](../../resources/web/n11-optimality-2026-09-29/README.md).
    Trump’s construction is credited to Walter Trump; the bundled exact reconstruction
    credits David Ellsworth’s diagram.
    This paper explains the imported proof and the repository’s confirmation, rather
    than claiming a new global argument.

[^proof]: [Original proof, §1: exact statement](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#1-statement-and-exact-endpoint)
    and
    [§10: final deduction](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [whole-proof acceptance review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance).

[^review]: [T-060](../../frontier/results.yaml);
    [current review disposition](../../../docs/project/reviews/review-2026-09-29-n11-optimality.md);
    [whole-proof acceptance](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [verification and confirmation levels](../../../epistemics.md).

[^lineage]: [Historical T-018/T-025/T-026 explainer](https://jlevy.github.io/squares/);
    [n = 11 result history](../../frontier/n-011.md);
    [result register](../../frontier/results.yaml).

[^tools]: [Tooling overview and scope of independent verification](../../../docs/project/verification-tooling.md).
    T-059 concerns reported row-minimum equality, while T-060 concerns global
    optimality. A rectangle-density or row-minimum check cannot substitute for the
    latter’s complete case and capture argument.

[^construction]: [Exact construction source](../../cases/trump11/packing.py);
    [exact feasibility checker](../../cases/trump11/verify_exact.py);
    [original proof, §2: construction and upper bound](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#2-exact-construction-and-upper-bound).

[^cover]: [Original proof, §4: closed center cover and masks](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#4-closed-center-cover-and-the-2184-cases);
    [exact cover consumer](../check_n11_optimality_d4.py);
    [independent cover receipt](../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json);
    [case census](../../resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json).

[^geometry]: [Original proof, §5: case-exclusion implications](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves);
    [independent row geometry checker](../check_n11_capture_transition_pilot.py) and
    [first-row receipt](../../resources/web/n11-optimality-2026-09-29/receipts/capture-transition-row0/result.json);
    [complete ownership update](../../resources/web/n11-optimality-2026-09-29/receipts/capture-step0/result.json).
    The
    [mathematical transition review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-complete-capture-owner-update)
    separates a checked row from a promoted complete step.

[^field]: [Original proof, §5: field charges and transfer](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves);
    [exact field consumer](../check_n11_optimality_field_mask0.py);
    [accepted mask-0 field receipt](../../resources/web/n11-optimality-2026-09-29/receipts/shared-field-mask0/summary.json);
    [mathematical review of the five-site charge](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#first-independent-field-exclusion-mask-0).

[^exclusions]: [Complete exclusion inventory](../../resources/web/n11-optimality-2026-09-29/receipts/exclusion-inventory.json);
    [case census, which counts the field certificates](../../resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json);
    [original proof, §9: accepted global obligations](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#9-accepted-global-verification-obligations);
    [independent exclusion and conditional-premise review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#complete-exclusion-execution-census).

[^symmetry]: [Closed-overlay checker](../check_n11_optimality_d4.py),
    [accepted symmetry receipt](../../resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json)
    and
    [original proof, §6: the D4 implication](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438).

[^capture]: [Capture ancestry](../../resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json);
    [fourteen-round root chain](../../resources/web/n11-optimality-2026-09-29/receipts/capture-root-chain/result.json);
    [accepted near node](../../resources/web/n11-optimality-2026-09-29/receipts/capture-child-near/result.json)
    and
    [pose-inclusion receipt](../../resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json);
    [original proof, §8: capture and frame bridge](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge).

[^local]: [Exact local-isolation checker](../check_n11_optimality_local_isolation.py)
    and
    [accepted local-isolation receipt](../../resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json);
    [original proof, §7: contact branches and finite rectangle](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle).
    The focused rectangle is distinct from the earlier uniform-radius local theorem.

[^endpoint]: [Original proof, §10: deduction of the optimum](../../resources/web/n11-optimality-2026-09-29/source/PROOF.md#10-deduction-of-the-optimum);
    [endpoint and final-composition review](../../../docs/project/reviews/review-2026-09-29-n11-optimality-census-contract.md#whole-proof-acceptance);
    [accepted final composition](../../resources/web/n11-optimality-2026-09-29/receipts/final-composition.json).

[^reproduce]: [Reproduction guide and disclosed limits](../../resources/web/n11-optimality-2026-09-29/README.md#reproducing-the-independent-checks);
    [tooling overview](../../../docs/project/verification-tooling.md).
    The final composition has `geometry_rerun: false`; it binds the observed executions
    rather than replacing them.

[earlier]: https://jlevy.github.io/squares/
[reproduction]: ../../resources/web/n11-optimality-2026-09-29/VALIDATION.md
[simplification]: ../../../docs/project/reviews/review-2026-09-30-n11-expository-simplification.md

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
