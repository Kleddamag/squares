# Native Rectangle-Density Verification Contract

The native checker proves the rectangle-density obstruction using exact rational polygon
intersections and a subdivision of the legal square-centre domain.
It uses neither Tokoharu’s `verify.cpp` nor its floating-point derivative bounds.
Its acceptance theorem is the same nonnegative-density argument reviewed in the
[rectangle mathematics review](review-2026-09-22-tokoharu-density-mathematics.md).
This W7 pipeline-improvement contract specifies the independent implementation and the
conditions required before its result can support a bound.

The implementation is
[`sqpack.rectangle_density`](../../../packing/src/sqpack/rectangle_density.py), with the
command
[`devtools.verify_rectangle_density`](../../../packing/devtools/verify_rectangle_density.py)
and [independent controls](../../../packing/tests/test_rectangle_density.py).

## Data and the Admission Theorem

The input declares rational container side $L$, core side $B$, rectangles
$R_j=[a_j,d_j]\times[b_j,e_j]$, and nonnegative rational masses $w_j$. A requested
positive integer count $n$ belongs to the admission decision.
Parse decimal tokens exactly; reject malformed rationals, duplicate JSON keys, nonfinite
numbers, mismatched array lengths, and negative weights.
Positive-mass rectangles must have positive area and lie inside the container.
Retaining the source format’s stricter smoothing margin is a permissible input
restriction.

Expand every source rectangle through all eight symmetries of $[0,L]^2$, with each image
assigned density $w_j/(8|R_j|)$. Coincident images retain their multiplicity.
This construction establishes $D_4$ invariance and gives the exact integral

$$
M=\int_{[0,L]^2}g=\sum_jw_j.
$$

Require $0<M<n$. Merely trusting a stored `mass` or `n` field is insufficient; the
admitted count and side must agree with the requested claim.
There is no need to import source-generated interval input or verification summaries to
establish these facts.

Put $D=83/40000$, $t_r=rD$, and

$$
(c_r,s_r)=\left(\frac{1-t_r^2}{1+t_r^2},\frac{2t_r}{1+t_r^2}\right),
\qquad r=0,\ldots,200.
$$

All coefficients are rational and $c_r^2+s_r^2=1$. Check $L>0$, $0<B<1$, $L^2>2B^2$,
$t_{200}^2+2t_{200}-1\ge0$, and $B(1+D)<1$. The source’s stronger $B(1+D)+3/20000<1$ is
sufficient when the implementation retains its smoothing-safe preconditions.

At every net angle prove that every legal closed side-$B$ square has integral at least
$\gamma$, where $\gamma\ge1$ is a declared exact threshold.
Choosing $\gamma=1$ proves the packing obstruction; reproducing the source’s stronger
$10001/10000$ is optional and must be recorded explicitly.
Every orientation has a nearby net direction with discrepancy at most $\arctan D$. The
corresponding concentric side-$B$ square lies strictly inside the unit square, because
$B(\cos\delta+\sin|\delta|)\le B(1+D)<1$. Symmetry reduces arbitrary orientations to the
net’s arc.

Nonnegativity then gives integral at least one on every legal unit square.
Interiors of packed squares are disjoint, and boundaries have zero mass for this bounded
rectangle density. Hence a packing of $n$ squares would imply $n\le M<n$. The checker
proves exclusion at the exact admitted side $L$; compactness can additionally convert
that exclusion to a strict lower bound on the minimum packing side.

## Closed Centre Domains and Common-Core Bounds

For an angle $(c,s)$ in the retained net, both coefficients are nonnegative.
Put $h=B(c+s)/2$. The complete legal centre domain is $[h,L-h]^2$. Quarter-turn
invariance of both the density and the square shape reduces it to the closed quadrant
$[L/2,L-h]^2$. This reduction uses rotations; reflection alone would reverse the
orientation. The stated side precondition makes the reduced domain nonempty.

Let a centre box have midpoint $m=(m_x,m_y)$ and nonnegative half-widths $h_x,h_y$. For
the rotated orthonormal axes $e_1=(c,s)$ and $e_2=(-s,c)$, define

$$
u=\frac B2-|c|h_x-|s|h_y,
\qquad
v=\frac B2-|s|h_x-|c|h_y.
$$

When $u,v>0$, the rotated rectangle

$$
P=\{m+\xi e_1+\eta e_2:|\xi|\le u,\ |\eta|\le v\}
$$

lies inside every translated side-$B$ square whose centre belongs to the box.
Indeed, the change in the first local coordinate between two such centres and the
midpoint is at most $|c|h_x+|s|h_y$, with the analogous bound for the second.
Adding these changes to $u,v$ gives $B/2$. Equivalently, $P$ is the intersection of all
those squares. When either half-width is nonpositive, use the sound lower bound zero; a
degenerate intersection contributes zero area.

Enumerate the four corners of $P$ in boundary order and clip it against each expanded
rectangle using rational half-plane intersections.
Every crossing parameter is a rational quotient with a nonzero denominator.
Shoelace area gives the exact intersection area, including tangency and repeated
boundary vertices. Therefore

$$
\operatorname{LB}(X)=\sum_j\rho_j|R_j\cap P|
\le \inf_{z\in X}\int_{Q(z)}g.
$$

The sum is over expanded images with multiplicity.
Nonnegative densities justify omitting any term proved disjoint.
No floating-point clipping, gradient enclosure, or sampled minimum participates in this
inequality.

Accept a leaf only if its exact lower bound is at least $\gamma$. Otherwise bisect a
nondegenerate coordinate interval at its exact midpoint and keep both closed children.
Their union equals the parent, including the shared split boundary.
Starting with the whole closed domain and resolving every leaf proves full coverage.
A depth, node, time, or arithmetic-resource limit leaves the direction unresolved.

The common-core lower bound converges to point coverage as the box widths tend to zero.
The density is bounded and has finite rectangular support, so the lost integral tends to
zero uniformly. A strict coverage margin above $\gamma$ therefore permits a finite
subdivision proof. Equality at the threshold need not terminate under this method.
No termination claim is necessary for sound acceptance.

## Exact Axis Shortcut

For $r=0$, an expanded rectangle’s contribution at centre $(x,y)$ is its density times
the product of two overlap lengths.
Each length is piecewise affine, with breakpoints at each rectangle endpoint plus or
minus $B/2$. Include both centre-domain endpoints and all such interior breakpoints,
independently for the x and y coordinates.

The complete coverage function is bilinear on each event cell.
Its value is a convex combination of its four corner values, so checking every
event-grid vertex proves its minimum on the whole domain.
Include boundary vertices and deduplicate coordinates, not rectangle images.
An exact vertex below $\gamma$ refutes this net-coverage condition.
It does not refute the packing bound itself, which could have another proof.

## Evidence and Refusal Semantics

| Result | Meaning |
| --- | --- |
| All 201 distinct directions verified, all input and mass premises checked | Complete native proof of the admitted rectangle-density obstruction |
| Selected directions verified | Partial coverage evidence; never a complete packing bound |
| Exact legal centre with integral below the chosen threshold | Counterexample to that net-coverage condition; if the threshold exceeds one, this need not defeat the weaker admission condition |
| Node, time, depth, or arithmetic cap reached | Inconclusive direction; no promotion |
| Malformed data, mismatched side/count, or failed mass premise | Input or admission refusal; no promotion |

Bind receipts to the exact candidate bytes, requested count and side, checker revision,
threshold, complete direction census, and work limits.
A receipt must state the number of accepted and unresolved leaves and any exact
counterexample. A resumable or merged result needs the same input identity and disjoint,
complete direction accounting; a successful restricted run must never acquire a
full-proof label.

## Independent Controls

An analytic positive control uses $n=3$, $L=3/2$, $B=9977/10000$, and one rectangle
$[1/1000,1499/1000]^2$ with mass $1683003/625000$. Its eight symmetry images coincide,
giving constant density $6/5$ inside that rectangle.
The omitted boundary strip has area at most $4L/1000=3/500$. Every legal core
consequently has integral at least

$$
\frac65\left(B^2-\frac3{500}\right)>1,
\qquad
M=\frac{1683003}{625000}<3.
$$

This supplies a complete expected result independent of the checker’s polygon code.
Other controls should cover exact rotated containment and tangency, duplicate symmetry
images, a negative weight, wrong target count, missing directions, a cap reached before
completion, an underweighted density, and agreement of box lower bounds with exact point
evaluations at rational interior and boundary centres.

The existing [`exact_area` oracle](../../../packing/devtools/audit_tokoharu_density.py)
is rational and independent of Tokoharu’s C++; it can provide differential tests for a
new implementation. The existing point-measure
[`fractional.interval` checker](../../../packing/src/sqpack/fractional/interval.py)
supplies precedent for full-domain subdivision and explicit refusal, but its point
containment calculation does not establish a rectangle integral.
The [`promote.interval` arithmetic](../../../packing/src/sqpack/promote/interval.py)
supports a future interval acceleration; it is unnecessary for the exact rational
implementation specified here.

## Astra-Max Adversarial Review

A separate GPT-6 Astra subagent at max thinking reviewed the admission, mass, symmetry,
angular containment, common-core bounds, clipping, axis events, subdivision and final
angle-census conditions.
It found no unsound acceptance path within that source review.
The
[PR review comment](https://github.com/jlevy/squares/pull/246#issuecomment-5886295719)
records the findings before their fixes were pushed.
This is not a formal correctness certificate or a complete replay of an external
certificate.

The review found two inaccurate counterexample receipts: the rotated path dropped
previously depth-capped boxes, and the axis path reset prior accepted and unvisited
vertex counts. Both exits already refused the certificate.
The counts are now preserved and tested using a density on $[3/10,6/5]^2$ with mass
$6/5$, at $n=3$, $L=3/2$, $B=9977/10000$. The rotated three-node run retains one
unresolved box; the axis three-node run retains two accepted and six unvisited vertices.

The [native tests](../../../packing/tests/test_rectangle_density.py) also include an
asymmetric eight-image orbit: $n=2$, $L=4$, $B=1/2$, source rectangle
$[9/20,11/20]\times[7/5,8/5]$, and mass 1. Each image has area $1/50$ and density
$25/4$. At direction $(c,s)=(3/5,4/5)$, a core centred at $(1/2,3/2)$ contains exactly
one whole image and misses the others, so its mass is exactly $1/8$. The same answer
holds at the three quarter-turn images of that centre, without changing the direction
coefficients.

Over the centre box equal to that source rectangle, the common core has four vertices,
area $21/250$, and captured mass $1/8$. Every polygon vertex satisfies both exact
local-coordinate containment inequalities for each of the four box-corner squares.
Their affine dependence on centre and polygon position extends containment throughout
both convex hulls; the positive exact area prevents an empty polygon from passing the
control vacuously. These analytic controls exercise asymmetric symmetry images and
unequal projected box widths without treating sampled coverage as a global proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
