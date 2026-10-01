# Evand: Mathematical Review and Transfer to Low-n Research

**Date:** October 1, 2026. **Lane:** W2 review supporting W3, bead `think-yew8`. This
review reads Evan Daniel’s latest proof sources and identifies experiments for
[X-048’s reviewed draft](https://github.com/jlevy/squares/blob/d7b77066424ab0d94b57f700659425e18ecb7080/packing/campaign/explorations/X-048-n17-optimality-after-n11.md).
It does not replay a certificate, build Lean, or promote a bound or assurance rating.

The principal new result is a reported proof of $s(k^2 - 3) = k$ for **every integer
$k \ge 6$**, with one exact checker for the 7-by-7 cover and a Lean reduction
conditional on that cover.
I found no blocking error in the reviewed mathematical reduction or new checker logic.
The useful research additions are exact constraints for limiting poses, continuous
anchored-clique features, and a wider periodic cover for the $k^2 - 4$ family.
Public exact-dual support now makes the n12 and n20 additive obstructions replayable;
adding line or area density does not evade those obstructions.

One auxiliary anchored-clique proof contains an incorrect convexity assertion.
The algebraic repair below proves the required inequality over the original parameter
range. This affects the exposition of a prospective research tool, not the new $k^2 - 3$
certificate.

## Sources and Review Scope

The external source is
[`evand/square-packing` at `08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5),
dated October 1, 2026, 04:17:47 UTC. The live
[Proofs](https://evand.github.io/square-packing/proofs.html) and
[Sources](https://evand.github.io/square-packing/sources.html) pages were read on
October 1. The parallel
[source-coverage review](review-2026-10-01-evand-source-coverage.md) and
[retained packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md)
record acquisition and omissions.
The packet preserves source bytes; this review does not edit those sources.

The local comparison is the September 26 and 28 packets, the two earlier evand reviews,
`origin/main` at `f9a3409f0f03298fbeeb0a03788cd016087626b9`, and X-048’s initial draft
at `d7b770664`. X-048 was added after that main snapshot.
The coordinator is updating X-048 and the session plan separately.

The detailed inspection covered `Bentz.lean`, `qx2_zm.py`, the finite-box write-up, the
family README and fast verification script, `qx2_records.py`, the n60 bundle report,
`dual_exact.py`, the side-4 and side-5 dual notes and support descriptions, and the
research notes cited below.
This is a source and mathematical review.
It does not independently establish the reported checker outputs, audit every imported
geometric primitive, or establish that the Lean files compile in this environment.
All upstream run counts, timings and numerical experiments below remain source-reported.

## The New Family: What Is Proved Conditionally

The
[family bundle](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3/README.md)
uses fixed corners, period-one wall profiles and a Lebesgue interior.
At side 7 its cover has no point masses, 800 segments on 60 lines of pitch $1/5$, and
density one on $[9/5, 26/5]^2$. Its corner deficit is

$$
D=\frac{423621306389}{500000000000}=0.847242612778,
\qquad \mu_k([0,k]^2)=k^2-4D=k^2-3.388970451112<k^2-3.
$$

The Lean endpoint is
[`SquarePacking.Bentz.bentz_of_valid7`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/lean/Sqpack/Bentz.lean):

```text
(h : Valid7) → ∀ k : ℕ, 6 ≤ k → minSide (k^2 - 3) = k
```

`Valid7` says that the exact 7-by-7 mixed measure assigns at least one unit of mass to
every closed unit square in the box.
Lean identifies the finite cover with the family at 7, computes the total mass and
proves the reduction to all $k \ge 6$. It does **not** discharge `Valid7` from the
checker output. The inspected proof uses ordinary Lean proof terms rather than a `sorry`
or `native_decide` replacement for that hypothesis.

The localization argument merits attention because it is stronger than repeating a large
numerical experiment.
A unit square has coordinate widths at most $\sqrt{2} < 2$. For each coordinate
interval, the reduction preserves a near-wall interval, shifts the opposite wall to 7,
or translates an interior interval by an integer into $(2,5)$. Integer translations
preserve the periodic wall pattern.
A width below two cannot simultaneously encounter the two boundary changes that would
obstruct this choice, including at $k = 6$. Applying the two coordinate shifts preserves
the captured line and area mass.
A universal cover check at 7 therefore suffices.
The stated range is $k \ge 6$, not $k \ge 7$.

The endpoint contradiction handles boundary mass correctly.
If a packing exists in side $s < k$, dilate it by $k/s$ and take concentric closed
unit-square cores. Each core lies strictly inside its enlarged parent, so these closed
cores are pairwise disjoint.
Their masses sum to at least $k^2 - 3$, exceeding the total measure.
At side $k$ itself, adjacent squares may share boundary mass; directly summing their
masses would be invalid.
The dilation step is what permits a zero-margin endpoint certificate.
A grid supplies the matching upper bound.

### What the Checker and Fast Script Establish

The source reports 9,800 roots, 54,358 boxes, 32,079 leaves, maximum depth 17 and no
uncertified leaves. The run took 81,377 CPU-seconds and 10,232 wall-seconds on eight
processes. This is one Python implementation, with six reported agent reviews.
The independent Rust mixed-cover checker used for earlier finite results does not
independently implement this new family’s entire geometric argument.

The
[fast verification script](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3/verify.sh)
checks identities and record structure: hashes, total mass, symmetry, family
reconstruction, the axis-aligned face, root and leaf coverage, and generated Lean data.
Its record checker does not recompute the mathematical inequality at every positive-tilt
leaf. For example, acceptance of a `PIECE`, `LEB` or `CAP` label in `qx2_records.py`
includes interval and coverage checks but does not independently prove that leaf’s
claimed mass bound. Passing this script would not constitute a fresh geometric replay or
a second checker.

The current
[Lean ladder](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/lean/LADDER.md)
also reports a fully discharged theorem for $s(12) \ge 15680/3951$, in addition to the
earlier point-cover results.
Its data generation and build are substantial and were not attempted.
The n21 top theorem remains conditional on its checker’s covering statement; n45 and n60
do not have a full Lean covering proof.
The general family’s conditional Lean theorem must be recorded separately from any of
these fully discharged point-cover theorems.

### The Separate n60 Result and n61 Corollary

The
[n60 bundle](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s60/README.md)
reports 23,744 weighted points and 5,216 segments with total
$748233441/12500000 = 59.85867528 < 60$, and universal closed capture at least one in
$[0,8]^2$. Its mathematical reduction is the same dilation and disjoint-core argument
above. I found no defect in that implication, or in the derived $s(61) \ge s(60) = 8$
with an 8-by-8 grid supplying $s(61) \le 8$. Neither implication recomputes the cover’s
total or universal validity.

The source reports two implementations for this finite cover: the Python
`Fraction`/integer checker and the independent Rust `zmx2` checker.
The latter uses outward-rounded binary64 intervals for chord endpoints, so its validity
depends on the stated floating-point arithmetic assumptions as well as its exact integer
mass sums. The n60 bundle has no Lean data or top theorem.
This review read its report and endpoint reduction; it did not replay the cover or newly
audit every primitive of the two inherited checkers.
Unlike the family’s fast script, the n60 default script includes a fresh Rust geometric
run according to its source.
The scripts’ default verification scopes must not be conflated.

## Exact Zero-Margin Logic Worth Transferring

The
[finite-box analysis](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/QUADRANT_EXACT.md)
and frozen
[`qx2_zm.py`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3/qx2_zm/checker/qx2_zm.py)
give three useful mechanisms.

1. **Treat exact contact strata explicitly.** On the axis-aligned face, captured mass is
   multiaffine within the breakpoint grid.
   One-sided corner limits give the lower bound in a cell, and closed capture handles
   the boundary. A positive numerical margin at nearby sampled poses cannot substitute
   for these limits.
2. **Partition where the mass formula changes.** At a fixed positive tilt, cumulative
   line profiles are piecewise affine.
   Splitting at density changes, disappearing chords and area-cap boundaries yields
   concave lower bounds in the centre variables.
   Their minima occur at arrangement vertices.
   The vertices become rational functions of the half-angle parameter; exact polynomial
   sign checks then cover an angle interval.
3. **Prove the easy continua directly.** A unit square wholly in the Lebesgue interior
   captures exactly one.
   Near an area boundary, line density can compensate an area cap through a proved
   chord-and-depth bound.
   These exact equalities avoid subdivision that can never obtain a positive margin.

In the inspected new checker logic, floating calculations choose candidate splits,
pieces or multipliers; exact predicates guard the ensuing proof.
Dropping a nonnegative contribution only weakens a lower bound.
This observation explains why some floating selection code is compatible with an exact
certificate; it does not exempt a predicate that discards a domain or chooses a sign
from exact checking.
Singular endpoints are handled separately, and a factored power of the half-angle
parameter is positive only on the positive-tilt domain where it is removed.

The source’s failed intermediate cover is particularly relevant to n17. It passed
ordinary sampling but captured approximately $0.999935986$ at a rational pose with
half-angle parameter $10^{-12}$. A positional tolerance can overcount a near-horizontal
intersection by an amount proportional to the tolerance divided by the tilt.
The later construction added exact limiting-pose constraints.
It then projected the weights onto the resulting tight identities before rational
rounding, keeping slack for the remaining poses.

For X-048 R1/R7, the useful next artifact is therefore an exact catalogue of tight
contact strata and one-sided perturbations, parameterized over the sliding n17 family.
At its nonzero algebraic tilts, the corresponding formulas may require algebraic
arithmetic rather than the family checker’s rational specialization.
The first test is whether a fixed feature dictionary can satisfy those exact constraints
with total mass below 17. An exact dual can refute that dictionary; one exact
undercovered pose refutes a proposed measure.
Feasibility of the finite system would still leave universal coverage and endpoint
feasibility to prove.

## The n12 and n20 Obstructions Now Have Public Endpoint Support

The pin contains
[`cover4_exact_support.txt`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/cover4_exact_support.txt)
and
[`s21_nuf5_exact_support.txt`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/s21_nuf5_exact_support.txt),
along with their
[exact checker](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/dual_exact.py).
The source reports:

| Box side | Rational support poses; D4 images | Total dual mass | Maximum closed depth $M$ | Normalized mass $L$ |
| --- | --- | --- | --- | --- |
| 4 | 294; 2,352 | $\frac{2453760771}{200000000}$ | $\frac{1999999999}{2000000000}$ | $\frac{24537607710}{1999999999} \approx 12.2688038611$ |
| 5 | 748; 5,984 | $\frac{10323890641}{500000000}$ | $\frac{499999999}{500000000}$ | $\frac{10323890641}{499999999} \approx 20.6477813233$ |

The checker verifies rational rotations and containment, enumerates corners and edge
intersections, and measures weighted closed depth at those arrangement vertices.
The maximum of a finite nonnegative weighted family of closed polygons is attained at
such a vertex: intersect the polygons covering a maximizing point and choose a vertex of
that nonempty bounded intersection.
This also covers degenerate intersections.
D4 permits a reduced-domain check, while `--full` removes that reduction.
I found no mathematical defect in this underlying enumeration argument or its reviewed
implementation; the outputs above have not been recomputed here.

### The Obstruction Covers Lines and Areas Too

Normalize the dual weights so that `Σ αᵢ 1_Qᵢ(x) ≤ 1` everywhere in the container $K$,
where each $Q_i$ is an admissible closed unit square.
For any finite nonnegative spatial measure $\mu$ satisfying $\mu(Q) \ge 1$ on every
admissible square,

$$
\sum_i\alpha_i
\leq \sum_i\alpha_i\mu(Q_i)
=\int_K\sum_i\alpha_i\mathbf 1_{Q_i}(x)\thinspace d\mu(x)
\leq\mu(K).
$$

Thus the endpoint witnesses, if accepted on replay, preclude any such additive spatial
cover of mass below 12 at side 4 or below 20 at side 5. The conclusion includes point,
line, area and mixed measures.
It is not limited to the sites used by the LP that produced the witness.
Conditional constraints, capacity rules and cliques of poses may escape this argument;
their validity and dual constraints must be established separately.
In particular, this is not a no-go theorem for all R068 features.

X-048’s original missing-support caveat should therefore be narrowed: the side-4 and
side-5 endpoint data are public and retained, while replay remains pending.
The side-3.99 files referenced by both the older `DUAL_EXACT.md` result and the newer
`CLIQUE_CONTINUUM.md` result remain absent from the pinned public tree.
An endpoint obstruction does not automatically give the reported obstruction at 3.99;
that stronger claim needs its own support or derivation.

### Bounded Replay Decision and Execution Requirements

No focused replay was launched under the requested 60-second wall ceiling.
The
[side-4 report](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/COVER4.md)
already reports 117 seconds for its reduced check on four processes, with 448,330
vertices and 154.8 million incidences; its full check took 982 seconds.
The
[side-5 report](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/S21_KILL.md)
reports 92 seconds on eight processes for 1,311,398 reduced-domain vertices and
456,658,626 incidences, or 668 seconds for the full check.
These are not local performance estimates, but both exceed the proposed ceiling before
allowance for host differences.
The mandated external scratch volume was visible but not writable in the sandbox, and no
disk-heavy fallback was used.

The `check` path uses only Python’s standard library; NumPy and SciPy belong to the
producer’s LP path. Before a later replay:

- Preserve the pinned script and supports outside disposable scratch; create its
  expected `s12/runs/` output directory in an isolated working copy.
- Address multiprocessing explicitly.
  The script populates module globals and starts a default `multiprocessing.Pool`.
  Spawned workers do not inherit those values.
  [Python’s documented start methods](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)
  use spawn by default on macOS; Python 3.14 also changes the POSIX default away from
  fork. A reviewed launcher selecting `fork`, or explicit worker initialization, is
  needed with the project interpreter.
  `--procs 1` still uses the pool.
- Use `--stream` to avoid retaining the incidence lists.
  This preserves the mathematical check, but does not remove vertex generation or the
  incidence work.
- Check support syntax, nonnegative masses, expected counts and the exact final $M$ and
  $L$. The source’s `--n` only changes the displayed comparison; exit status zero alone
  does not assert the desired inequality.
  Retain complete stdout, stderr, environment, wall time and termination status.

After satisfying those prerequisites, the upstream arguments are:

```text
dual_exact.py check cover4_exact_support.txt --t 4 --n 12 --stream --procs 4
dual_exact.py check s21_nuf5_exact_support.txt --t 5 --n 20 --stream --procs 8
```

Run with `packing/.venv/bin/python3` and a reviewed multiprocessing launcher, under a
separately selected wall ceiling.
These are proposed commands, not execution receipts.
A full-domain replay is a subsequent assurance choice, not part of a 60-second quick
check.

## Anchored Cliques: A New Feature with a Repairable Proof Gap

The source’s
[anchored-clique construction](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/notes/clique-family.md)
offers a concrete feature beyond an additive spatial measure.
For a point $p$ and nonempty anchor set $A$, define

$$
K(p,A)=\lbrace Q:p\in Q,\ Q\cap A\ne\varnothing\rbrace
\thickspace\cup\thickspace\lbrace Q:A\subseteq Q\rbrace.
$$

Every two members intersect as closed sets: two from the first family share $p$, two
from the second share $A$, and a mixed pair shares a point of $Q \cap A$. It is
therefore a capacity-one feature for pairwise disjoint closed cores.
This validity statement does not require the more ambitious claim that it contains every
square through $p$. That dominance claim needs a transversal theorem for the anchor.
Nor does a closed intersection prove positive interior overlap; the chosen packing
reduction must supply the appropriate closed cores.

For a vertical anchor offset by $\varepsilon$ from a wall-near point, Lemma 2 states the
sufficient threshold $\rho \ge \varepsilon p_x / \sqrt{1 - p_x^2}$, where
$0 < \varepsilon < 1 - p_x$. Its proof introduces

$$
f(\theta)=p_x/\cos\theta+\varepsilon\cos\theta-\rho\sin\theta-1
$$

and asserts convexity.
This assertion is false in the stated range: $f^{\prime\prime}(0) = p_x - \varepsilon$,
which is negative for $p_x = 1/4$, $\varepsilon = 1/2$. The source’s tabulated wall
anchors happen to lie in a range where that specific problem does not arise, but the
printed general argument needs correction.

Here is a replacement for the affected step.
Set $a = p_x$, $z = \cos \theta \in [a,1]$, $S = \sqrt{1 - a^2}$ and
$T = \sqrt{1 - z^2}$. It suffices to use the least allowed $\rho = \varepsilon a/S$,
since increasing $\rho$ lowers $f$. Then

$$
f=\frac{a-z}{z}+\varepsilon B,
\qquad
B=z-\frac{aT}{S}
=\frac{(z-a)(z+a)}{S(zS+aT)}.
$$

All denominators are positive, and

$$
0\leq B
\leq\frac{(z-a)(z+a)}{z(1-a^2)}
\leq\frac{z-a}{z(1-a)}.
$$

Since $\varepsilon < 1 - a$, this gives $f \le 0$ throughout the required interval.
The other separating-axis case in the source uses the same inequality with $\theta$
replaced by $\pi/2 - \theta$. This repairs the sufficiency step without weakening the
lemma’s range. Its necessity direction retains the source’s extra vertical room
hypothesis; it should not be quoted as an unconditional “if and only if.”
This repair is a derivation made in this review, not an upstream amendment or a
formalized result.
Bead `think-2z60` tracks independent review of the repair before reuse
in a proof.

For n17, anchored cliques are a specific candidate for X-048 R3/R8: place anchors near
an observed low-charge family and compare their exact finite relaxation with the same
frozen R068 rows. A finite improvement would justify continuous validation.
An exact matching dual can reject the claimed gain on that frozen finite problem; it
does not establish that the feature set is useless on the full continuum.
Existing source experiments already warn against expecting a large gain from thickening
a sampled clique: some apparent finite gains depend on almost-tangent intersections and
disappear when robust pose neighborhoods are required.

## Other Transfer Ideas and Their First Falsifiers

The following are refinements or additions to X-048’s routes, not fresh experiment
verdicts. Each needs a hypothesis and executable measurement before W10 selection.

| Candidate | What the new sources add | First discriminating artifact | Failure that actually rejects the candidate |
| --- | --- | --- | --- |
| n17 endpoint strata, R1/R7 | Tight limiting constraints can be enforced before rationalization, including along a flexible family. | Exact contact and perturbation formulas for one chart, with a known feasible packing retained as control. | An exact undercovered pose rejects a proposed measure; an exact dual rejects the chosen dictionary. A same-side slide does not refute endpoint optimality. |
| n17 continuous clique features, R3/R8 | $K(p,A)$ supplies a proved capacity-one family and an explicit wall-anchor threshold. | A frozen finite primal/dual comparison with the current feature set, followed by a universal membership check for a candidate gain. | Invalid pairwise intersection or a wrongly removed pose rejects the proposed validity argument. An exact matching dual can reject a claimed gain on the frozen finite problem. |
| n12 conditional geometry, R6 | `RANK8.md` reports exact feasible proper subcases of a hard Bentz leaf, while the whole leaf has a numerically observed zero-margin plateau. | Recover and independently check a hardest proper-subcase witness; state one whole-leaf inequality that preserves it. | A checked subcase witness refutes a proposed exclusion of that subcase. Failed searches for the whole leaf do not establish its infeasibility. |
| n12/n17 terminal wall chains, R1/R5/R6 | `T4_CYCLES.md` finds nested wall-chain Farkas combinations where a simple cycle argument fails. | An exact local inequality with its domain, remainder bound and all contact alternatives stated. | A feasible counterexample to the chain hypothesis, or a nonlinear remainder of the wrong sign, rejects that argument. A linearized contradiction alone is insufficient. |
| n20 conditional adaptation | The recovered side-5 dual makes unconditional spatial reweighting an implausible next job pending replay. | An occupancy or class-count inequality that supplies a quantified gain beyond the n21 mixed cover. | A certified feasible class-count counterexample, or insufficient gain in the declared relaxation. The existing cover needs more than $0.89474919732$ of saving to get below 20. |
| $k^2 - 4$ plateau family | The successful fixed-corner/periodic-wall/area decomposition has a concrete width-three extension to try. | A width-three candidate after density-layer and tilt-margin constraints, exact tight-identity projection and nonnegativity checks. | Deficit $D \le 1$ rejects that candidate before a global checker run; a rational undercovered pose rejects its cover. Neither rules out wider profiles. |

The
[rank-eight note](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/RANK8.md)
and
[wall-cycle note](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/T4_CYCLES.md)
are particularly useful negative evidence.
They separate exact proper-subcase witnesses from numerical evidence about the whole
leaf. The reported plateau includes tilted configurations, not just tilings with tiles
removed. A proposed global n12 proof cannot silently restrict to the grid family.
The wall-cycle work also reports counterexamples to a proposed chain-or-cycle dichotomy
and uses successive powers of a small tilt in more elaborate combinations.
Those calculations suggest terminal lemmas, but do not establish capture or a theorem
covering every contact type.

The
[clique continuum experiments](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/CLIQUE_CONTINUUM.md)
are lower bounds on the corresponding fractional packing relaxation.
A sampled clique-relaxed value below 12 does not prove that a universal cover costing
below 12 exists.
Conversely, one finite LP that fails to gain enough does not establish a
universal ceiling. Preserve this direction of inference in W3’s selection record.

### A Separate Plateau Campaign

The new
[Friedman-family analysis](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/FRIEDMAN.md)
reports a floating width-three corner deficit near $1.154$, before the cost of making
the cover exact.
A deficit strictly above one would give total mass $k^2 - 4D < k^2 - 4$.
Its proposed base box is 9, with localization to $k \ge 8$. Together with the separately
reported finite results at sides 5 through 8, a successful family would imply
$s(k^2 - 4) = k$ for every $k \ge 5$. It would not settle n12 at $k = 4$.

The source estimates 5–10 CPU-hours for the initial LP work and 50–80 CPU-hours for a
full exact check, with substantial uncertainty.
This belongs in a separately selected reserve campaign, not an unpriced addition to the
n17 overnight block.
Its first checkpoint is whether $D > 1$ survives the exactness constraints.
Checking a corner window plus one wall period could reduce the cost, but requires a new
localization proof. Deeper limiting-pose lemmas may matter more than a faster generic
subdivision loop.

The family source also corrects an appealing but unsupported inference from
Roth–Vaughan: wasted-area growth away from integer sides does not imply an unbounded
eventual integer plateau.
Near-integer behavior needs its own argument.
Likewise, numerical failure of a proposed descent operation on selected packings does
not by itself refute every possible descent theorem.

## Disposition for the Next Block

Use the new results to sharpen the existing n17-first plan.
Start with the exact endpoint-family audit and the actual R068 charge semantics already
required by X-048; add limiting-pose constraints or anchored cliques only where those
audits identify a specific loss.
For the low-n secondary lane, replaying the recovered endpoint duals is now a concrete
prerequisite rather than a source hunt.
If accepted, it directs n12/n20 work toward conditional or nonadditive constraints.
Keep the wider periodic family as a costed alternative campaign.

The separate source intake also located an evand replay of wand125’s point-only
$s(61) = 8$ certificate at wand commit `f8846cec`. That is a distinct evidence chain
from evand’s $s(60)$ corollary and from the all-k family.
It was not audited here and must not be counted as a second implementation of the new
7-by-7 checker.

The review leaves no new bound, replay receipt, hypothesis verdict or human-review
claim. Its deliverables are the source-level distinctions above, the repaired anchor
inequality, and the proposed discriminators for the coordinator’s W3/W10 selection.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
