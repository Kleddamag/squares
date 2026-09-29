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

## Rust and Golden-Testing Review

The
[PR review record](https://github.com/jlevy/squares/pull/246#issuecomment-5886554596)
applies tbd’s general code-review and testing rules, Rust language, lint, testing and
review rules, and golden-testing guidelines.
The review separates the Python exact rectangle checker, the floating-point Rust search
engine and the retained standalone upstream Rust verifier.
Cargo validation of one cannot establish correctness of the others.

Two **Medium** gate findings concern the first-party search crate:
`packing/sqsearch/Cargo.toml` left missing documentation and pedantic lints at warning
level despite a pinned compiler, and `_rust_quality` in
`packing/src/sqpack/cli/validate.py` compiled tests under Clippy without running them.
The repair denies those lints, warnings and unchecked unwraps in the manifest, and adds
the five existing Rust tests and warnings-as-errors rustdoc to the validation step.
Worker-pool initialization reports an error and exits before producing search output.
This changes the failure path without altering search arithmetic.
The expanded Rust gate passed with five Rust tests, rustdoc, Clippy, formatting, one
clean compiler control and four deliberately rejected lint probes.
It took 8.85 seconds on its first measured expansion and 1.67 seconds warm; those runs
are not a before/after performance comparison.
The gate refuses a missing compiler or an empty Rust test run.
Its 134 focused Python contract and validation tests passed.

The [CLI golden tests](../../../packing/tests/test_rectangle_density_cli_golden.py)
capture all five decision outcomes through real subprocesses, preserving complete
receipts, exit status and both output streams.
Expected source and candidate hashes remain exact.
Separate assertions check the full direction census, strict mass margin, exact
counterexample and unresolved work.
The read-only comparison rejects a changed fixture; only an explicit update can write
one. The [analytic controls](../../../packing/tests/test_rectangle_density.py) provide
mathematical oracles independently of the golden approval process.
The existing native controls and new golden tests passed together: 15 tests in 1.60
seconds. A final Astra-max review caught newline translation in the test capture; the
harness now captures bytes and reads fixtures without newline translation.
The largest golden has 1,648 lines, including all 201 angle results.
Each session also captures the input bytes before launch, checks that they remain
unchanged, and records their hash and size, including the refusal case whose CLI receipt
carries only the error.
The final read-only golden check passed all three tests in 0.95 seconds after adding
these headers. The harness uses the project’s pytest lane and typed session records
rather than adding Tryscript to Python-only CI jobs.
This keeps the existing test entry point and exact rational assertions together without
another runtime dependency.
The text fixtures retain portable commands and full outputs for reuse by a later
implementation.

The follow-up push selection finished in 618.13 seconds: 2,039 behavioral tests passed,
one tracked-file snapshot test failed because the new files were unstaged, and three
tests were deselected.
After staging, that snapshot test and the final native controls passed together: 16
tests in 24.05 seconds.
The campaign-record check still reports the inherited Session 161 expired phase.
Its owner status remains unresolved; this review does not claim a green full checkpoint.

Hosted run `36544631396` passed both behavioral shards, types, frontend, geometry,
sweeps and macOS portability; the Rust gate passed in 10.09 seconds.
Rustdoc also exposed a documentation-scan interaction: its generated font-license
Markdown under `packing/sqsearch/target` was treated as durable source.
The scanner now excludes that exact build-output tree, with a regression proving that
unrelated `target` directories and similarly named paths remain checked.
Both documentation tests and the real 1,494-document scan passed.
The
[CI review comment](https://github.com/jlevy/squares/pull/246#issuecomment-5886864717)
records the finding before this repair.

Broader search-CLI contracts, an explicit platform and minimum-Rust support policy,
dependency auditing and review of existing lint exceptions remain in **think-cr8l**. The
scoped repair does not claim full adoption of every Rust guideline across the repository
or its archived sources.

The review found no reason to introduce a Rust port solely to apply the Rust rules.
The exact Python implementation remains the independently implemented rectangle checker;
a future port must satisfy the same geometric contract and account explicitly for
integer overflow. Complete independent coverage of a retained external certificate
remains the open acceptance criterion in **think-bmf3**.

## End-to-End Integration Review

The W7 continuation under **think-8cps** reviews PR 246 at `45eaf8e75` and repairs its
remaining CI failures.
Three parallel lanes inspect frontend timing (**think-sewp**), the inherited Session 161
record, and verifier integration (GPT-6 Astra, max thinking).
The coordinator owns the final diff, generated records, validation and publication.

| Review surface | Completed evidence | Remaining obligation |
| --- | --- | --- |
| Upstream intake | Pinned MIT source, maintained-repository citations, T-056 and T-057 registration, transformation and admission review | Repair the upstream ceiling/admission gaps; replay T-057’s complete 12,028-row census |
| Native mathematics | Astra-max review of mass, symmetry, angular containment, common-core geometry, clipping, axis events and exhaustive subdivision; analytic and refusal controls | Complete native coverage of a retained external certificate; no formal kernel proof claimed |
| Native CLI | Five real subprocess decision goldens with byte-exact output and independent semantic assertions; normal CI behavioral coverage | Keep incomplete and refused runs separate from certificate acceptance |
| Rust | Scoped source review, executed tests, strict Clippy, formatting, rustdoc and live lint rejection probes for the first-party search crate | Broader Rust support and CLI contracts remain in **think-cr8l**; archived Rust is not certified by this crate’s gate |
| Repository integration | Hosted behavioral shards, types, geometry, sweeps, macOS portability and certificate-page checks passed | Resolve record and timing failures and obtain the full checkpoint |
| Review approval | Agent reviews retained here and in PR comments | GitHub has no submitted formal review or human approval at this checkpoint |

The atlas regeneration changes the release stamp after the data revision moved to
`3dab8e`; the two SVG trees retain the same geometry.
This review does not claim an independent pixel comparison of every raster or PDF
export.

The existing synopsis handoff incorrectly still described PR publication as pending.
It now links the published PR and names CI integration and certification as the
remaining work. The native research continuation remains **think-bmf3**.

The
[integration review comment](https://github.com/jlevy/squares/pull/246#issuecomment-5893038192)
records this checkpoint.
Session 161’s owner branch and `main` retain the same expired phase, with no subsequent
disposition. At `2026-09-29T15:10:35Z`, the coordinator administratively stopped that
recorded interval, preserving its original clocks and Recovery State.
Its certification debt remains with the active **think-1an7** epic.
This does not declare remote jobs stopped or the research completed.
The ledger, schema, session-clock and certification checks pass after this change; the
certification check explicitly reports the session as uncertified.

The handoff selector previously distinguished administrative closeouts only when their
resource usage was unmeasured.
A top-level `handoff_role: administrative_closeout` now also represents a stopped
interval with retained usage receipts.
The schema and selector require stopped status and a nonblank disposition; active and
completed sessions cannot use it.
Resource accounting and certification gates still apply.
This prevents closing an old record from replacing Session 162’s current work handoff.

Frontend timing receipts from the failed hosted run and its predecessor show similar
slowdown across browser work, lint liveness and independent TypeScript commands.
That supports runner-wide slowdown without identifying its cause.
The frontend runner also serialized eight independent browser contracts after one page
build. Each contract owns its Playwright driver, browser and temporary output; the
completed page is read-only shared input.
The repair allows at most two contracts concurrently, preserves result order and
propagates any failure.
The validation entry point chooses one worker on smaller or fully occupied hosts and two
when the outer topology leaves room.

A sequential same-host comparison on the Mac, based on `45eaf8e75` with the scheduling
change uncommitted, passed the identical eight contracts in 67.331 seconds with one
worker and 49.606 seconds with two (26.3 percent less wall time).
Page builds took 18.22 and 19.05 seconds; the longest browser contract took 23.76 and
24.54 seconds. This measures reduced serial waiting, not removed checks or a hosted
performance guarantee.
The reusable `workbench_tools.check_frontend --workers 1|2
--timings PATH` command retains per-contract timings; the gate’s time thresholds remain
unchanged. Hosted validation is still required.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
