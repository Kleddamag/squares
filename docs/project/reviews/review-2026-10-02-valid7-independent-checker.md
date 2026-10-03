# Method Review: wand125’s Independent Checker of Valid7 (`T-064`)

**Date:** 2026-10-02. **Lane:** Y, a lane of the W2 phase that is stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md) for `T-064`, bead
`think-4k80`, issue [296](https://github.com/jlevy/squares/issues/296). **Reviewer:**
Claude (Anthropic), an AI agent, prompted for this lane alone; the session the lane’s
commits link to records the model and its reasoning setting.

The review has three parts.
It reviews the method of the second exact checker of Valid7, the finite statement on
which `T-064`’s lower half rests.
It states what Evan Daniel’s Lean reduction proves and assumes, and stages its build
from retained bytes.
And it prices a full replay of each checker and splits it into shards.
Neither checker’s sweep was repeated here.
The runs quoted below are one-cell calibrations, the source’s fast `verify.sh`, and what
this lane computed, and each says which it is.

**In one line:** the independent checker’s mathematics is sound, but one line of its
exact positivity test is not.
The line accepts a polynomial that vanishes at the one point where its sign is sampled
(D-1). D-1 cannot make a true Valid7 fail, and it could hide a counterexample only in a
coincident configuration.
The published records cannot show whether it ever fired; a replay with the line guarded
can. The checker’s independence from Daniel’s code is declared, and is consistent with
everything the files let anyone check.
The Lean reduction proves exactly “Valid7 implies $s(k^2-3) = k$ for every $k \ge 6$”
and assumes nothing else.
It stages here blob for blob, but it was not built: this container has 2.8 GB of free
disk, and Mathlib’s cache needs more than that.
A full replay of Daniel’s checker costs about 23 CPU-hours on this host, and of
wand125’s about 216. Both split by region into shards that resume.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Claim | `T-064`: $s(k^2 - 3) = k$ for every integer $k \ge 6$, reported by Evan Daniel; its lower half is Valid7 plus the Lean reduction |
| Statement checked | **Valid7**: every closed unit square in $[0,7]^2$, at every centre and every angle, has mass at least 1 under the measure `L4_k02_box7.txt` (SHA-256 `c0a67509…694b`), retained in the [October 1 evand packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md) at `source/s12/certificates/k2m3/` |
| Independent checker | [wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check) at `38dd31b369991b0d96c917a4af0c7139b44a038d`, retained in [its packet](../../../packing/resources/web/wand125-valid7-independent-check-2026-10-02/README.md); code V2 is `src/`, and V1’s two changed files are under `versions/V1/` |
| Records | Release `records-v1`, `full.jsonl.gz` `f553751d…` and `full_b.jsonl.gz` `8eaf90f3…`, downloaded here again and checked against the retained `release/records.sha256` |
| Write-ups read | `DESIGN.md`, `README.md`, `READ_LOG.md`, `versions/VERSIONS.md`, `NOTICE`, `verify.sh`, `tests/` |
| Code read | Every line of `src/`: `cover.py`, `axis_mass.py`, `solver.py`, `tier_a.py`, `rf.py`, `tier_b.py`, `tier_b2.py`, `run_all.py`, `run_a.py`, `check_record.py`; `versions/V1/` against `src/` |
| Lean read | `Bentz.lean` §1, §9 and its doc header; `MixedMeasure.lean` §2 and §5; the definitions `coord` and `sq` (`Basic.lean`), `box` (`Chord.lean`), `Packs` and `minSide` (`S32.lean`); `notes/lean-bentz-reduction.md` |
| Daniel’s side, for comparison | The k2m3 `README.md` and `verify.sh`; `qx2_zm.py`’s `main` and its record format; the identifiers of `zm_mixed.py` and `zeromargin.py` |
| Earlier reviews relied on | The [1 October transfer review](review-2026-10-01-evand-mathematical-transfer.md), for the reduction and for `qx2_zm.py` |

What this lane ran, each at two processes or fewer on a shared 4-core host, and each but
the demonstrations with a receipt written by `devtools.replay_receipt`:

- the source’s fast k2m3 `verify.sh` on the October 1 packet as retained, exit 0
  ([`k2m3_verify_fast.log`](../../../packing/resources/web/evand-square-packing-2026-10-01/receipts/valid7/k2m3_verify_fast.log));
- one centre cell of `qx2_zm.py` run V3 and two of wand125’s `run_all.py`, each staged
  by [`devtools.plan_valid7_replay`](../../../packing/devtools/plan_valid7_replay.py),
  which refuses any file whose digest is not the one the run record names (§8);
- `check_record.py`’s leaf re-certification of one of those cells (§8.3);
- [`devtools.stage_evand_bentz_lean`](../../../packing/devtools/stage_evand_bentz_lean.py),
  which assembles the Lean build (§7);
- two short demonstrations of D-1 and D-2 against the retained `src/` (§10).

## 2. Verdict

**The method is sound, with one implementation defect.** Each lemma in `DESIGN.md` and
the module docstrings was re-derived.
Each holds as stated, or holds under a premise that this cover meets and that the table
names. The defect, D-1, is in `tier_b2.nonneg_open`, the exact test that a polynomial is
nonnegative on an open interval.
It is used for every Tier B value, at vertices and at edge critical points.

**D-1 is non-blocking for `T-064`.** Valid7 has two checkers.
The cheaper replay is Daniel’s, and it is the source’s own verification, which is what
stage 4 asks for. D-1 also cannot make a true Valid7 fail, and it can hide a false one
only in the case §10 describes.
It is blocking for recording wand125’s run as confirming evidence of Valid7. A replay
with the guard of §8.5 closes it, and so would a fix by the author.

| Step | Where | Verdict |
| --- | --- | --- |
| Cover facts: 800 segments, one polygon, exact total, D4 invariance | `cover.py`, Step 0 | Sound; recomputed here by the checker’s own code and by the source’s `qx2_records.py`, which agree |
| $\theta = 0$ by closure | `DESIGN.md` Step 1 | Sound with a stated premise: no point masses, and the run covers $\theta \ne 0$ on both sides of 0 |
| F1, piecewise quadratic in the centre | `solver.py` | Sound with a stated premise: the arrangement contains every mass line and every density breakpoint within reach, which `Local` builds from all segments of a line |
| F2, no interior minima | `solver.py` | Sound with a stated premise: at most one polygon of positive density can meet a square of the box; this cover has one |
| A1, angular core | `tier_a.py` | Sound; needs $t_1 - t_0 < \pi$, and a box spans at most $1/32$ in $u$ |
| A2, erosion by the centre box | `tier_a.py` | Sound |
| A3, outer hull | `tier_a.py` | Sound; the arc-in-triangle step needs an arc under $\pi$, as A1 does |
| `wmin`, the narrowest admissible width | `tier_a.py` | Sound: $\lvert\cos t\rvert + \lvert\sin t\rvert$ is concave on each side of 0 and at least 1 |
| `mass_convex`, $\mu$ of a convex polygon | `tier_a.py` | Sound for every polygon the run builds; latent over-count on a degenerate polygon (D-4), unreachable here |
| B1, symbolic execution in $u$ | `rf.py`, `tier_b.py` | Sound with a stated premise: every branch is a logged sign test or an exact identity, and every denominator is nonzero on a piece; both hold in `solver.py` as read |
| B2, continuity in $u$ for $u \ne 0$ | `tier_b.py` | Sound |
| B3, vertices by pairs of lines | `tier_b2.py` | Sound; a line is dropped only on an exact strict-sign proof |
| B4, edge critical points line by line | `tier_b2.py` | Sound given F2 |
| Sturm counts, isolation, `Alg`, `alg_cmp`, `between` | `rf.py`, `tier_b.py`, `tier_b2.py` | Sound, including roots at interval ends |
| `nonneg_open`, the exact positivity test | `tier_b2.py` | **Defect D-1** |
| `rf.nonneg_on` | `rf.py` | Defect D-2; dead code, called by nothing in the run |
| Hash-keyed line and value caches | `tier_b2.py` | Exact up to 64-bit hash collisions (D-3); non-blocking |
| Record checks: product grid, bisection tiling, `EMPTY`, Tier B away from $u = 0$ | `check_record.py` | Sound |
| The V1 to V2 hand-off change | `run_all.py`, `versions/VERSIONS.md` | Not a proof step; sound |

## 3. From Certificate to Claim

### 3.1 The statement

Both checkers decide the statement the Lean development calls `Valid7` (§7.2). Here
$\mu_7$ is the uniform-by-length measure on 800 axis-parallel segments of length $1/5$
on 60 lines of the $1/5$ grid, plus Lebesgue measure on $S = [9/5, 26/5]^2$. Its total
is $5701378693611/125000000000 = 49 - 4D < 46$. A closed square captures each segment’s
parametric fraction of its closed intersection with the square.
There are no point masses, which Tier B and the closure argument both need (§4.2, §4.6).

### 3.2 How the run covers pose space

A pose is $Q(c, t) = c + R_t[-\tfrac12, \tfrac12]^2$ with $u = \tan(t/2)$, so that
$\cos t$ and $\sin t$ are rational in $u$. The roots are $70 \times 70$ centre squares
of side $1/10$ over $[0,7]^2$, times 32 bins of width $1/32$ over
$u \in [-\tfrac12, \tfrac12]$. That range is $t \in [-53.13°, 53.13°]$, more than the
square’s period $\pi/2$. There is no D4 reduction.
The record audit of 2 October showed the roots are exactly that grid, each once
([packet README](../../../packing/resources/web/wand125-valid7-independent-check-2026-10-02/README.md)).
$u = 0$ is a bin boundary, so no root, and hence no leaf, contains $u = 0$ in its
interior.

Every leaf is one of three kinds.
An `EMPTY` leaf has no admissible centre, which `check_record.py` re-decides exactly.
A `CORE` leaf is closed by Tier A’s bound, which is valid on the closed box, $u = 0$
included. A `TIERB2` leaf is closed by Tier B on the open $u$-interval, extended to its
ends by continuity, except at an end where $u = 0$. So the leaves prove $\mu \ge 1$ at
every admissible pose with $t \ne 0$ and $|t| \le 53.13°$, and the closure argument of
§4.2 extends this to $t = 0$.

### 3.3 From Valid7 to the claim

That step is Daniel’s Lean reduction, which this review reads in §7. Neither checker
touches it.

## 4. The Method, Lemma by Lemma

### 4.1 Step 0: the cover

`cover.py` parses the format from `FORMAT.md` alone.
It checks well-formedness and strict convexity, and reports the exact total, the D4
invariance of the segment measure as densities on elementary grid edges, and the
polygon’s density.
Run here, it gives 0 points, 800 segments of length $1/5$ on 60 lines,
one polygon $[9/5, 26/5]^2$ of mass $289/25$ and density 1, total
$5701378693611/125000000000$, D4 invariance `True`, and $D > 3/4$. The source’s
`qx2_records.py cover`, in the fast `verify.sh` run here, gives the same.
The checker does not use the D4 invariance; it reports it.

### 4.2 Step 1: $\theta = 0$ by closure

The claim is that $\mu(Q(c,0)) \ge 1$ follows from $\mu \ge 1$ at nearby tilted poses.
Re-derived:

1. **Upper semicontinuity.** $\{(c, t, p) : p \in Q(c,t)\}$ is closed.
   So along any sequence of poses converging to $(c, t)$,
   $\limsup 1_{Q_n}(p) \le 1_Q(p)$ for every $p$. Since $\mu$ is finite, reverse Fatou
   gives $\limsup \mu(Q_n) \le \mu(Q)$. This needs nothing about the cover beyond a
   finite nonnegative measure.
2. **Approach.** At $t = 0$ the admissible centres are $[\tfrac12, \tfrac{13}{2}]^2$,
   and at small $t > 0$ they are $[w/2, 7 - w/2]^2$ with $w = \cos t + \sin t \to 1$. So
   clamping $c$ into the smaller square gives admissible tilted poses converging to
   $(c, 0)$.
3. Each of those has $\mu \ge 1$ by the leaves, so $\mu(Q(c,0)) \ge 1$.

**Sound.** The premise that matters is that the leaves cover $0 < |t| < \varepsilon$,
which §3.2 establishes.
The design states continuity of $\mu$ for $t \notin (\pi/2)\mathbb Z$ as well, but the
closure step itself uses only semicontinuity.
This is the step that replaces Daniel’s Lemma Z, an exact enumeration of 900 one-sided
corner limits on the $\theta = 0$ face.
It is the one place where the two checkers differ in kind, not only in implementation.

### 4.3 F1: piecewise quadratic in the centre

For $t \notin (\pi/2)\mathbb Z$, no segment is parallel to an edge of $Q$. A vertical
mass line meets $Q$ in an interval whose ends are affine in $c$ while the same two edges
of $Q$ cut it. That changes only when a vertex of $Q$ crosses the line, which is type
(a). The captured mass is the integral of a piecewise-constant density between those
ends. It is affine until an end crosses a density breakpoint, that is, until an edge of
$Q$ passes through the breakpoint, which is type (b). For the polygon, the intersection
$Q \cap S$ changes shape only when a vertex of $Q$ crosses an edge line of $S$, or an
edge of $Q$ passes through a vertex of $S$. On each face its area is a polynomial of
degree at most 2.

`Local` builds the mass lines and breakpoints from every segment of a line, so densities
add correctly where segments abut or overlap.
It keeps every line and breakpoint within the reach $7072/10000 > \sqrt2/2$ of the box.
A superset of lines only refines the arrangement, which is harmless.
**Sound with that premise, which the code meets.**

### 4.4 F2: no interior minima

On a face, $g(c) = \operatorname{area}(Q(c) \cap S)$ is either identically 0, or
positive throughout.
The support’s boundary is made of type (a) and (b) lines, so it cannot cross a face.
Where $g > 0$, $\sqrt g$ is concave by Brunn’s concavity principle: the sections of a
convex body in $\mathbb R^4$ have concave square-root area.
So $\nabla^2 g = 2\nabla h \nabla h^{\mathsf T} + 2h\nabla^2 h$ with $h = \sqrt g$ is a
rank-one positive term plus a negative semidefinite one, and has at most one positive
eigenvalue. The segment part is affine on a face, so $\nabla^2\mu = \nabla^2 g$. A
quadratic whose Hessian has at most one positive eigenvalue has a direction along which
it is concave or affine.
Through any interior point of a compact convex face, that direction reaches the boundary
without lowering the minimum.
So the minimum over a face is on its boundary, and on an edge it is at an end or at the
edge’s critical point.

**Sound with a stated premise: one polygon.** With two polygons, each term has at most
one positive eigenvalue, but their sum can have two.
A square meeting both could then have an interior minimum.
The docstring speaks of “the polygon term” in the singular, and the code does not check
the premise. This cover has one polygon, so the lemma applies.

### 4.5 Tier A: the box core bound

**A1, the angular core.** For $t \in [t_0, t_1]$, write
$n(t) = \ell_0 n_0 + \ell_m n_m$, where $n_m$ is the bisector,
$\ell_0 = \sin(h-a)/\sin h$ and $\ell_m = \sin a/\sin h$, with $h = (t_1 - t_0)/2$. Then
$x \cdot n(t) \le (\ell_0 + \ell_m\cos h)/2 = \cos a/2 \le 1/2$, as the docstring says.
The chord half-plane $m \cdot x \le m \cdot p_0$ with $m = n_0 + n_1$ is that bisector
condition. Applied to all four rotated normals, the intersection lies in every $Q(0,t)$
of the interval. **Sound**, given $0 < h < \pi/2$; a box spans at most $1/32$ in $u$.

**A2, erosion.** $P_B = \{x : a_i \cdot (x - c_{\mathrm{mid}}) \le b_i - h_B(a_i)\}$ is
contained in $c + P$ for every $c$ in the box, since $a_i \cdot d \le h_B(a_i)$. So
$P_B \subseteq Q$ for every pose of the box, and $\mu(Q) \ge \mu(P_B)$ by nonnegativity.
**Sound.** The box is first clipped to $[w_{\min}/2, 7 - w_{\min}/2]^2$. That set
contains every admissible centre of the interval, so the bound is taken over a superset
of the admissible poses, which is the safe direction.

**A3, the outer hull.** A vertex of $Q$ sweeps an arc of radius $\sqrt2/2$, and the
tangent at $v$ is $\{x : x \cdot v = 1/2\}$. The arc lies in the triangle formed by its
chord and the two tangents.
Then $O = \operatorname{conv}(\text{12 points}) + \text{box}$ contains every square of
the box, and $\operatorname{area}(Q \cap S) \ge 1 - \operatorname{area}(O \setminus S)$
because $\operatorname{area}(Q) = 1$. The bound adds
$\text{density} \times \max(\text{inner}, \text{outer})$, both lower bounds.
**Sound.** It is what certifies the three-dimensional set of poses with $Q \subseteq S$,
where the mass is exactly 1.

**`wmin`** returns 1 when the interval contains $u = 0$, and the smaller endpoint width
otherwise. $\lvert\cos t\rvert + \lvert\sin t\rvert$ is concave on $[0, \pi/2]$ and on
$[-\pi/2, 0]$, and at least 1, so this is the minimum.
**Sound.**

**`mass_convex`** clips each segment by Cyrus–Beck against a closed polygon, using a
grid index that finds every segment meeting the polygon’s cells, with a `seen` set
against double counting.
A polygon with fewer than three vertices is given mass 0, which is a valid lower bound.
See D-4 for a degenerate polygon with three or more.
**Sound** for every polygon the run builds: with box half-widths at most $1/20$, the
eroded core is a near-square of side above $0.85$.

### 4.6 Tier B: exact in $u$

**The number type.** `rf.RF` is a rational function over $\mathbb Q$ with a sample point
$u^*$. Each order comparison is decided by the sign at $u^*$, and logs $N \cdot D$ as a
guard. A value that is not identically 0 but vanishes at $u^*$ raises `Resample`.
Equality, `==`, is an identity of rational functions: $N_1 D_2 = N_2 D_1$ as
polynomials, with no guard.
So only identities, never sample signs, decide `==`.

**B1.** If no guard has a root in an open interval $J \ni u^*$, every logged sign is
constant on $J$. Every identity holds for all $u$, so every branch is the same and the
outputs are the same rational functions on $J$. Read against `solver.py`, every branch
is one of three things: an identity (`den == 0` in `point_mass`, `det == 0` for parallel
lines); a logged sign (`den > 0`, the clip tests, `abs`, the membership tests, the sort
keys); or a test on a list’s length, which those signs determine.
Every division is by $1 + u^2$, or by a quantity whose sign was logged nonzero, or by a
determinant whose roots are breakpoints (B3). A denominator of the result therefore
cannot vanish inside a piece.
Where the trace is valid, the result equals the true, finite mass, so a pole inside the
piece would contradict it.
**Sound with that premise, which the code meets as read.**

**B2.** For $u \ne 0$ and no point masses, $\mu$ is continuous in the pose.
$R(u) = X \cap [\mathrm{lo}(u), 7 - \mathrm{lo}(u)]^2$ moves continuously while it is
nonempty. So $m(u) = \min_{R(u)} \mu$ is continuous, and $m \ge 1$ off finitely many
points gives $m \ge 1$ everywhere.
**Sound.** `chain` joins components left to right and compares their algebraic ends
exactly.
A component ending at its predecessor’s end leaves that one point to continuity.

**B3, vertices.** The line set $\mathcal L$ holds the eight lines bounding $R(u)$, and
every type (a) or (b) line that is not proved to miss $X$ on all of $[a, b]$. The proof
of a miss is exact: the line’s value at the four corners of $X$ has one strict sign over
the closed interval.
The sign is read through a Taylor bound (`root_free`), a sufficient test for having no
root. For each pair, the pieces where the vertex lies in $R(u)$ are cut by the roots of
eight membership polynomials and of the determinant.
On each piece, the membership signs are sampled once and the vertex mass is traced
symbolically, splitting at guard roots.
**Sound.** Without a polygon, $\mu$ is affine on faces, and the vertices of the
arrangement restricted to $R(u)$ suffice.
With one, B4 adds the edges.

**B4, edges.** On line $i$, the breakpoints are its intersections with the other lines
that lie in $R(u)$. Between consecutive ones the mass along the line is one quadratic
(F1), with the segment part affine.
So the second difference is taken from the polygon term alone, the critical point is
$t = -B/2A$ when $A > 0$, and its value joins the candidates.
Each line is certified by B1 and B2 on its own.
**Sound given F2**, and therefore resting on the one-polygon premise.

### 4.7 The exact real-algebraic primitives

- **Sturm counts.** For squarefree $p$, sign variations are counted with zeros dropped.
  $V(a) - V(b)$ is then the number of roots in $(a, b]$, ends included or not as stated.
  This holds even at a root, since at a simple root $V$ equals its right-hand limit.
  `isolate` bisects at non-roots, moving a midpoint that hits a root.
  **Sound.**
- **`Alg`** keeps a root of a squarefree polynomial in an open interval whose ends are
  not roots, established by exact counts at construction.
  That invariant is the fix of the defect `VERSIONS.md` says was found and fixed before
  V1, with every earlier record discarded.
  `refine` uses the sign change at a simple root.
  **Sound.**
- **`alg_cmp`** separates by intervals, or proves equality by a common factor with a
  root in the intersection of the two intervals; for a rational, by evaluation.
  Each case is exact, and failing to separate raises rather than guessing.
  **Sound.**
- **`between`** returns a rational strictly between $A < B$. **Sound.**
- **`nonneg_open`** rejects when an odd-multiplicity root lies strictly inside $(A, B)$,
  and otherwise accepts when $p(s) \ge 0$ at one sample $s$. Without odd roots, $p$ has
  one sign off its zeros.
  But if $s$ is itself a zero, the test decides nothing, and it accepts.
  **Defect D-1.**
- **`rf.nonneg_on`** checks the ends and the ends of each isolating interval.
  When $p$ vanishes at the left end, the first interval starts there, and negativity
  just to its right is missed.
  **Defect D-2**, in code that nothing in the run calls.

### 4.8 Records and driver

`check_record.py` does five things, independently of the driver’s control flow.
It re-checks that the roots of all record files are exactly a product grid covering
$[0,7]^2 \times [-\tfrac12, \tfrac12]$, each once.
It re-checks that each root’s leaves form a bisection partition.
Recursive halving that ends with every leaf equal to a node proves both disjointness and
cover. It re-decides `EMPTY` exactly, and refuses a Tier B leaf with $u = 0$ inside.
`--recheck` and `--recheck-b` re-certify sampled leaves.
**Sound.**

The driver’s V1 to V2 change moves only the hand-off threshold between Tiers A and B,
and adds a witness to failure messages.
`nonneg_open` and every other function the certificate rests on are the same in V1 and
V2. **Not a proof step; sound.**

## 5. Independence

**What the source states.** `READ_LOG.md` lists what was read at evand/square-packing
`d9f79bc1`: the k2m3 `README.md`, `s21/FORMAT.md`, lines 1–60 of the bundle’s
`verify.sh`, and the cover.
It also lists what was not read, by design: `qx2_zm.py`, `zm_mixed.py`, `zeromargin.py`,
`mixed_cover.py`, `QUADRANT_EXACT.md`, `ZM_MIXED.md`, `qx2_records.py`,
`qx2_family_check.py`, the V3 record and `lemmaZ.out`. Another checker, for covers of
the same kind in a C4-symmetric container, was being written at the same time, “possibly
with reference to the upstream checker”.
With it, only specifications and usage were exchanged.
The README says the code was “written from the cover format specification … and the
statement of the claim only”.
Neither file says how the code was written, or with what assistance.

**What can be checked, and what it shows.**

- **No code is shared.** None of the identifiers distinctive of Daniel’s checker appears
  in `src/`: `clip_bin`, `region_phi`, `piece_bound`, `LineMass`, `QXChecker`,
  `lines_in_reach`, `Wnum`, `d4_roots`, `u_square`. The architecture differs.
  wand125’s checker has two tiers, fixed-angle vertex and edge enumeration, and a
  Sturm-based algebraic type.
  Daniel’s has the leaf kinds PIECE, EXACT, LEB, CAP, SYM and AXIS, float screening, a
  McCormick relaxation in Lemma E, and D4 folding.
  The primitives differ too: python-flint polynomials here, `Fraction` with numpy there.
- **One constant is shared**, the reach $7072/10000$ (`solver.Local`). It appears in
  `zm_mixed.py` as `REACH`. It also appears in the one k2m3 `README.md` paragraph the
  log says was read: “radius `0.7072 + ½·diagonal`”.
- **One idea is shared**: certify near the tight set by bounding the mass at the
  vertices of a line arrangement as rational functions of $u = \tan(\theta/2)$. The same
  README paragraph states it, as the description of Daniel’s Lemma E. wand125’s
  realization of it differs in each lemma: F2 by Brunn–Minkowski rather than McCormick,
  and B1 to B4 by symbolic execution with guards.
- **The same author had Daniel’s checkers on disk.** wand125’s `square-packing-bounds`
  bundles for $s(59)$ and $s(77)$, committed 1 October, have `verify.sh` scripts that
  fetch, hash-check and run `zm_mixed.py`, `zeromargin.py` and `zmx2` at a pinned commit
  ([packet](../../../packing/resources/web/wand125-point-and-mixed-2026-10-01/README.md)).
  Running a checker is not reading it, and the read log’s claim is about reading.
  No file can confirm it either way.

**Assessment.** The checker is an independent implementation: it shares no code, and its
decisive lemmas differ from Daniel’s. Its independence of thought is declared, and is
consistent with every trace the files leave.
The shared constant and the shared idea are both explained by the README it says it
read. For the record this is `relationship_to_generator: independent-implementation`, as
the evidence entry already says.
The method overlap of §6 is what a reader should weigh, more than the declaration.

## 6. Trust Boundary and What the Two Checkers Share

**wand125’s checker trusts** CPython’s `Fraction`; python-flint 0.9.0’s `fmpq_poly`
arithmetic (`gcd`, exact division, evaluation, `factor_squarefree`) and `fmpq`;
CPython’s 64-bit `hash` for de-duplication (D-3); and the JSON records as written by the
driver. No floating-point number enters a decision.
**It decides** every leaf, the closure at $\theta = 0$, and the coverage of the pose
grid.
It does not decide the cover’s meaning: `cover.py` parses the format as `FORMAT.md`
states it.

**Shared by both checkers:**

- the statement Valid7 and the cover file;
- `FORMAT.md`’s semantics: parametric segment fractions on closed squares, uniform area
  density, closed containment;
- the reach constant (harmless: any value above $\sqrt2/2$ is correct);
- the arrangement-vertex idea for the tight set, as above.

**Not shared:** the $\theta = 0$ argument (closure against Lemma Z’s enumeration); the
symmetry (none against D4); the polygon lemma (Brunn–Minkowski against McCormick); the
arithmetic (flint and Sturm against `Fraction` with numpy screening); and the record
format and record checker.

An error in the statement or in the format’s reading would pass both checkers.
An error in the closure, D4 or polygon lemmas would pass only one.
The Lean statement of §7.2 fixes the format’s reading for Valid7, independently of both.

## 7. The Lean Reduction

### 7.1 What it proves

```lean
theorem SquarePacking.Bentz.bentz_of_valid7 (h : Valid7) :
    ∀ k : ℕ, 6 ≤ k → minSide (k ^ 2 - 3) = k
```

`minSide n = sInf {s | Packs n s}`. `Packs n s` says there are centres and angles with
every closed unit square `sq c θ 1 ⊆ box s`, where `box s` is $[0,s]^2$, and pairwise
disjoint open interiors.
That is the record’s convention: closed unit squares, independent real rotations,
contact allowed. So the conclusion is `T-064`’s claim for every $k \ge 6$, the scope’s
$k = 6, \ldots, 18$ included.
The proof is `not_packs_of_measure`, dilation applied to $\mu_k$, for the lower half,
and `packs_grid`, the $k \times k$ grid, for the upper.

### 7.2 What it assumes

**One hypothesis, `Valid7`:**

```lean
def Valid7 : Prop :=
  ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box 7 → 1 ≤ box7Cover.measure (sq c θ 1)
```

`box7Cover` is the cover file verbatim as a `MixedCover`. It has no points.
It has the 800 segments of `BentzData.boxSegs` in file order, each with mass $w/10^{12}$
spread by the push-forward of Lebesgue measure on $[0,1]$ along the segment.
It has one polygon, `convPoly 5 boxPolyVerts`, proved equal to $[9/5, 26/5]^2$, with
mass $11560000000000
/ 10^{12}$ spread uniformly by area.
That is the statement of §3.1, over every real $\theta$, without reduction.
Both checkers’ conventions agree with it: the parametric fraction, the closed square,
and area density.

**No other premise about the cover is assumed.** The finite facts are kernel-checked by
`decide +kernel`, not supplied as hypotheses:

- `box7Cover_measure`: the file is `famCover 7`;
- `famCover_total`: the total is $k^2 - 4D$ for every $k \ge 4$;
- nonnegativity;
- `mass_shift`: the integer-shift localization of each $\mu_k$ to $\mu_7$.

The trusted base is the Lean kernel, Mathlib, and the definitions `coord`, `sq`, `box`,
`Packs`, `minSide`, `segMeasure`, `areaMeasure` and `MixedCover.measure`, which were
read for this review.
The source states that `BentzData.lean` is generated from the files, and that is checked
twice: by the source’s `verify.sh` here (identical), and by `stage_evand_bentz_lean`,
which regenerates it byte for byte.

### 7.3 How it maps to the claim

`T-064`’s lower half is Valid7 plus `bentz_of_valid7`, and nothing else.
Once built with its axiom receipt, the reduction is proof-assistant-checked evidence for
the implication. It is not evidence for Valid7, and it does not discharge the checkers.
D4 enters only inside Daniel’s checker.
The independent checker needs no D4 at all.

### 7.4 Build status here

**Staged, not built.** `devtools.stage_evand_bentz_lean` assembled the import closure
from retained bytes
([receipt](../../../packing/resources/web/evand-square-packing-2026-10-01/receipts/lean/bentz_stage.json)).
The closure is ten project modules and Mathlib: `Basic`, `Chord`, `ZeroMargin`, `D4`,
`Cover`, `S32Data`, `S32`, `MixedMeasure`, `BentzData` and `Bentz`.

- Nine of the modules and the three lake files are retained in the September 26 and
  October 1 packets.
- `S32Data.lean`, which no packet retains, is regenerated by the source’s
  `gen_s32_data.py` from the retained $s(32)$ cover.
- Every staged file has the Git blob of the `08e8a5fa` tree.
  A blobless clone of the source supplied the list.
- Outside comments, no project source contains `sorry`, `axiom`, `native_decide`,
  `ofReduceBool`, `implemented_by`, `@[extern` or `unsafe`.

The toolchain is `leanprover/lean4:v4.33.1`, with Mathlib `0df444a3`.

**Why the build did not run.** The network allows it: the elan installer and the v4.33.1
release both answer 200 through the proxy.
Disk does not: at 19:28Z this container had 2.8 GB free on its one 252 GB volume, 93%
used. The toolchain archive alone is 570 MB and unpacks to several times that.
Mathlib’s cache is the 8,690 files that the $s(13)$ build of 30 September fetched, and
importing it mapped 6.3 to 6.6 GB there.

**What would make it run:** a host with at least 10 GB of free disk and 10 GB of memory.
The $s(13)$ table’s small targets peaked at 6.3 GB, against 15 GB here.
Two cores are enough.
The source reports `lake build Sqpack.Bentz` at 127 s with four threads.
Then:

```bash
cd packing
uv run --frozen --all-extras --group dev python -m devtools.stage_evand_bentz_lean \
  --out "$W" --json "$W/stage.json"
curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh \
  | sh -s -- -y --default-toolchain none
( cd "$W/s12/lean" && lake exe cache get )
R=resources/web/evand-square-packing-2026-10-01/receipts/lean
uv run --frozen --all-extras --group dev python -m devtools.replay_receipt \
  --receipt "$R/build_bentz.log" --cwd-label "s12/lean staged by stage_evand_bentz_lean" \
  --chdir "$W/s12/lean" -- env LEAN_NUM_THREADS=2 lake build Sqpack.Bentz
uv run --frozen --all-extras --group dev python -m devtools.replay_receipt \
  --receipt "$R/axioms_bentz.log" --cwd-label "s12/lean staged by stage_evand_bentz_lean" \
  --chdir "$W/s12/lean" -- lake env lean AxiomsBentz.lean
```

The probe `AxiomsBentz.lean` prints the theorem, `Valid7`, `minSide` and `Packs`, and
the axioms of `bentz_of_valid7`, `valid_of_valid7`, `box7Cover_measure`,
`famCover_total` and `mass_shift`. **The axiom receipt must read**
`'SquarePacking.Bentz.bentz_of_valid7' depends on
axioms: [propext, Classical.choice, Quot.sound]`. That is what the source reports, and
it is not yet reproduced here.

## 8. The Cost of a Full Replay

### 8.1 What the records say

| Checker | Roots | Leaves | Recorded CPU | What “CPU” is |
| --- | ---: | ---: | ---: | --- |
| Daniel’s `qx2_zm.py` run V3, D4 region | 9,800 | 32,079 | 81,377 s, 22.6 h | `time.process_time()` per root |
| wand125’s `run_all.py`, whole pose space | 156,800 | 9,640,060 | 2,254,888 s, 626.4 h | `time.time()` per root: wall time in a worker of a 32-process pool |

wand125’s first 31,825 roots ran under V1, whose earlier hand-off to Tier B cost more.
A replay runs V2, so `plan_valid7_replay` prices each V1 root at its mirror image under
$x \mapsto 7 - x$, $u \mapsto -u$, which ran under V2. That gives **540.5 hours at V2**.
Where both a root and its mirror ran under V2, the left half totals 271.2 h and its
mirror 253.3 h, with a per-pair spread of 10%. So the mirror price is good to about 7%.

### 8.2 Calibration on this host

One centre cell per checker was run with the staged, digest-checked code, at two
processes, on a host whose 4 cores carried a load of 20 to 30 from other lanes.
`plan_valid7_replay compare --partial` confirmed that every root’s leaf list equals the
published one.

| Checker | Cell (centres) | Roots | Recorded | Here, CPU | Ratio | Leaves equal |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `qx2_zm.py` | $[2.7, 2.8] \times [2.3, 2.4]$ | 8 | 122.5 s | 123.6 s | 1.01 | 8 of 8 |
| `run_all.py` | $[5.1, 5.2] \times [2.5, 2.6]$ | 32 | 122.6 s | 42.3 s | 0.35 | 32 of 32 |
| `run_all.py`, 438 Tier B leaves | $[5.4, 5.5] \times [6.3, 6.4]$ | 32 | 232.0 s | 92.4 s | 0.40 | 32 of 32 |

wand125’s ratio is well below 1 because its recorded time is wall time under a loaded
32-process pool. The plan uses 0.40.

Under CPython 3.14’s default `forkserver` start method, `run_all.py`’s workers are not
children the receipt waits for.
A first calibration receipt read 0.2 CPU-s for 162 s of wall
([receipt](../../../packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/valid7_calibration_forkserver_x51-52_y25-26.log)).
The plan therefore launches the unmodified `run_all.py` under `fork`, which changes no
decision.

### 8.3 Estimates

| Checker | Host CPU-hours | 4-core runners | Wall per runner |
| --- | ---: | --- | --- |
| `qx2_zm.py` | **22.8** | 2 shards | 2.9 h |
| `qx2_zm.py`, unsharded | 22.8 | 1 | 5.7 h |
| `run_all.py`, V2 | **216** | 14 shards | 3.8 to 4.0 h |

The longest single root is 536 s for `qx2_zm.py`, and 2,261 s recorded for `run_all.py`,
about 900 s here. Neither bounds a shard.

**A leaf-only replay is not cheaper.** `check_record.py --partial` re-certifying every
leaf of the Tier B cell took 94.5 CPU-s, against the search’s 92.4
([receipt](../../../packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/valid7_leaf_recheck_x54-55_y63-64.log)).
The search spends its time where the leaves do.

### 8.4 Sharding and resuming

Both checkers shard by region and resume from their own records, as `replay_evand_zmx2`
does for `zmx2`:

- `qx2_zm.py` takes `--cx-lo --cx-hi --cy-lo --cy-hi`. `--resume FILE` appends one
  flushed line per root, skips recorded roots, and refuses a file whose header names
  other digests.
- `run_all.py` takes `--centers x0 x1 y0 y1` on the $1/10$ grid.
  `--resume` skips recorded roots, and drops a line cut short by an interruption.

`plan_valid7_replay plan` cuts the centre cells, in x-major order, into runs of nearly
equal priced CPU. Each shard is at most three rectangles, and each rectangle is one
checker run with its own record and receipt.
An interrupted shard is finished by running the same command again.

**One caveat for `qx2_zm.py`.** The source’s `qx2_records.py record` refuses a record
whose argv restricts the region; that is one of its mutation tests.
A sharded replay is therefore checked by `plan_valid7_replay compare`. It requires the
retained digests, the V3 settings, region flags only, no root twice, exactly the 9,800
published roots, no uncertified box, and each root’s leaves equal to V3’s. An unsharded
run on one runner can be checked by the source’s own tool as well.
It fits a 6-hour runner with little margin.

### 8.5 The commands

Each runner bootstraps a clone as `AGENTS.md` says, then stages and runs its shard from
`packing/`. The plans hold every shard’s literal argv:
[`qx2_replay_plan.json`](../../../packing/resources/web/evand-square-packing-2026-10-01/receipts/valid7/qx2_replay_plan.json)
and
[`valid7_replay_plan.json`](../../../packing/resources/web/wand125-valid7-independent-check-2026-10-02/receipts/valid7_replay_plan.json).

```bash
cd packing
P="uv run --frozen --all-extras --group dev python -m"
$P devtools.plan_valid7_replay stage --checker qx2 --work "$W"
$P devtools.replay_receipt --receipt "$W/receipts/qx2_shard01_1.log" \
  --cwd-label "work dir staged by plan_valid7_replay" \
  --python-note "packing/.venv/bin/python3, CPython 3.14.7 with numpy" --chdir "$W" -- \
  "$PWD/.venv/bin/python3" checker/qx2_zm.py L4_k02_box7.txt --depth 18 --nproc 4 \
  --exact-umax 1/2 --exact-from 3 --progress 200 \
  --cx-lo 0 --cx-hi 21/10 --cy-lo 0 --cy-hi 7/2 \
  --resume runs/qx2_shard01_1.jsonl --dump-leaves
```

| `qx2_zm.py` shard | Rectangles $[x_0, x_1] \times [y_0, y_1]$ | Priced CPU |
| --- | --- | ---: |
| 1 | $[0, 2.1] \times [0, 3.5]$; $[2.1, 2.2] \times [0, 1.6]$ | 11.4 h |
| 2 | $[2.1, 2.2] \times [1.6, 3.5]$; $[2.2, 3.5] \times [0, 3.5]$ | 11.2 h |

After both shards, Lemma Z and the record are checked:

```bash
$P devtools.plan_valid7_replay compare --checker qx2 SHARD_RECORDS... \
  --json resources/web/evand-square-packing-2026-10-01/receipts/valid7/qx2_replay_compare.json
```

Lemma Z is checked by `.venv/bin/python3 "$W/checker/qx2_zm.py" axis
"$W/L4_k02_box7.txt"`, compared with the shipped `lemmaZ.out`. The fast `verify.sh` run
here already did that.

For wand125’s checker, each runner makes `$W/.venv` with python-flint 0.9.0, as
`requirements.txt` pins: `uv venv --python 3.14.7 "$W/.venv"`, then
`uv pip install --python "$W/.venv/bin/python" python-flint==0.9.0`. It stages with
**`--guard-d1`**, which turns D-1’s accepting line into a refusal, so the replay closes
D-1. Then it runs each of its rectangles:

```bash
$P devtools.plan_valid7_replay stage --checker wand125 --guard-d1 --work "$W"
$P devtools.replay_receipt --receipt "$W/receipts/wand125_shard01_1.log" \
  --cwd-label "work dir staged by plan_valid7_replay --guard-d1" \
  --python-note "W/.venv: CPython 3.14.7, python-flint 0.9.0" --chdir "$W" -- \
  .venv/bin/python -c "import multiprocessing, runpy, sys; \
multiprocessing.set_start_method('fork'); sys.argv = sys.argv[1:]; \
sys.path.insert(0, 'src'); runpy.run_path(sys.argv[0], run_name='__main__')" \
  src/run_all.py cover/L4_k02_box7.txt --centers 0 11/5 0 7 --nproc 4 \
  --record runs/wand125_shard01_1.jsonl --resume
$P devtools.plan_valid7_replay compare --checker wand125 --guard-d1 \
  --records RELEASE_DIR SHARD_RECORDS...
```

| `run_all.py` shard | Rectangles | Priced CPU at V2 |
| --- | --- | ---: |
| 1 | $[0, 2.2] \times [0, 7]$; $[2.2, 2.3] \times [0, 4]$ | 39.5 h |
| 2 | $[2.2, 2.3] \times [4, 7]$; $[2.3, 2.4] \times [0, 7]$; $[2.4, 2.5] \times [0, 2.5]$ | 38.9 h |
| 3 | $[2.4, 2.5] \times [2.5, 3.9]$ | 37.7 h |
| 4 | $[2.4, 2.5] \times [3.9, 7]$; $[2.5, 2.6] \times [0, 3.3]$ | 38.3 h |
| 5 | $[2.5, 2.6] \times [3.3, 7]$; $[2.6, 2.7] \times [0, 7]$; $[2.7, 2.8] \times [0, 4.5]$ | 38.7 h |
| 6 | $[2.7, 2.8] \times [4.5, 7]$; $[2.8, 3.0] \times [0, 7]$; $[3.0, 3.1] \times [0, 4.6]$ | 38.8 h |
| 7 | $[3.0, 3.1] \times [4.6, 7]$; $[3.1, 3.4] \times [0, 7]$; $[3.4, 3.5] \times [0, 2.4]$ | 38.3 h |
| 8 | $[3.4, 3.5] \times [2.4, 7]$; $[3.5, 3.7] \times [0, 7]$; $[3.7, 3.8] \times [0, 4.6]$ | 39.5 h |
| 9 | $[3.7, 3.8] \times [4.6, 7]$; $[3.8, 4.1] \times [0, 7]$; $[4.1, 4.2] \times [0, 2.3]$ | 38.2 h |
| 10 | $[4.1, 4.2] \times [2.3, 7]$; $[4.2, 4.4] \times [0, 7]$; $[4.4, 4.5] \times [0, 2.5]$ | 39.1 h |
| 11 | $[4.4, 4.5] \times [2.5, 7]$; $[4.5, 4.6] \times [0, 2.6]$ | 37.7 h |
| 12 | $[4.5, 4.6] \times [2.6, 4.2]$ | 38.9 h |
| 13 | $[4.5, 4.6] \times [4.2, 7]$; $[4.6, 4.7] \times [0, 4.6]$ | 39.0 h |
| 14 | $[4.6, 4.7] \times [4.6, 7]$; $[4.7, 7] \times [0, 7]$ | 38.1 h |

With the guard, a root where D-1’s case arises fails Tier B and is split further, so its
leaves differ from the published ones.
Identical leaves throughout would show that no accepted piece of the published run
rested on a sample at a zero.
The V1 roots are not compared, since V1 split differently.
The guarded run certifies them afresh.

**Recommendation.** Replay Daniel’s `qx2_zm.py` for `C3`: two 4-core runners and about 3
hours, or one runner and about 6. Record wand125’s guarded replay beside it if it is
run, as the second machine method; it is not a condition of the rung.

## 9. What a Fast Verifier Would Need for This Cover

The fast verifier of `think-gpe0` could make the second route cheap.
For this cover, its slice 4 (continuous angle) would need the following:

1. **Mixed format v1 with area density.** Uniform-by-length axis-parallel segments on a
   grid, plus a convex polygon with uniform area density, and the exact area of a
   rotated square intersected with it.
   `zmx2` takes no polygons, and the Lebesgue square cannot be removed from this cover.
2. **Zero-margin poses.** Wall squares and tile germs have mass exactly 1 at
   $\theta = 0$, and grow like $1 + c\lvert u\rvert$ with $c \approx 0.3$ to $0.5$. No
   interval method closes a neighbourhood of them.
   The verifier needs an exact primitive there: rational functions of $u$ at arrangement
   vertices, as both checkers use, or an equivalent.
   It also needs either a closure argument for $\theta = 0$ or an exact axis-face
   enumeration. The source’s partial area-density `zmx2` stops exactly here: it leaves
   120 D4 boxes open at $0 < \theta < 0.01°$.
3. **The plateau inside the polygon.** Every square inside $S$ has mass exactly 1, on a
   three-dimensional set of poses.
   A lower bound needs an outer-hull term like A3, or a proof that the polygon is the
   whole of a square’s mass.
4. **Exact fallback**, with no decision resting on a floating-point comparison, and
   outward rounding everywhere else.
5. **The whole pose space**, or a check of the cover’s D4 invariance before folding.
6. **Leaf records** comparable root for root with either published run, and the three
   mutant covers `M1`–`M3` and two mutated certificates refused.

## 10. Findings

### D-1. `nonneg_open` accepts a polynomial that vanishes at its sample (defect; non-blocking for `T-064`, blocking for wand125’s run as confirming evidence)

`tier_b2.py` line 103 reads `return p(s) >= 0`, where $s$ is `between(A, B)`, a rational
inside the piece. Without odd-multiplicity roots inside, $p$ has one sign off its zeros,
but $p(s) = 0$ says nothing about that sign.
Against the retained code, `nonneg_open` accepts $-(u - \tfrac12)^2$ on $(0, 1)$, whose
sample is $\tfrac12$, although the polynomial is $-\tfrac1{16}$ at $u = \tfrac14$. It is
used for every Tier B vertex value (`check_value`) and every edge critical value
(`tier_b.chain`).

**Reach.** A wrong acceptance needs $p = (N - D)D \le 0$ on the piece, not identically
0, with an even-order zero exactly at the rational sample.
That means the candidate pose has mass below 1 at all but finitely many $u$ of the
piece: a family of genuine counterexamples to Valid7. So D-1 never makes a true Valid7
fail.
It can hide a false one only if the mass touches 1 from below at exactly the sample
point, which is an algebraic coincidence.
The mutants lower tight families by a relative $10^{-4}$. They make the mass strictly
below 1, so they do not exercise D-1. The records keep counts, not pieces, so they
cannot show whether D-1’s case arose.

**Fix:** accept only on $p(s) > 0$, and resample if $p(s) = 0$.
`plan_valid7_replay stage --guard-d1` stages that line as a refusal for a replay.
The author should be told.

### D-2. `rf.nonneg_on` misses negativity next to a root at the left end (defect; non-blocking, dead code)

`nonneg_on(u(u - 1), 0, 2)` returns `True` against the retained code, though the value
at $\tfrac12$ is $-\tfrac14$. Only `tier_b.nonneg` calls it, and nothing calls
`tier_b.nonneg`. It should be removed or fixed before anyone reuses it.

### D-3. De-duplication by 64-bit hash (non-blocking)

`tier_b2.certify` de-duplicates lines by `(hash(a), hash(b), hash(k))`, and
`edge_runner` caches masses by `(hash(x), hash(y))`. A collision would drop a line or
return another point’s mass.
With about $10^3$ lines per box and $2.9 \times 10^6$ Tier B leaves, the chance of any
collision in the run is of order $10^{-7}$. Keying by the exact `(str(n), str(d))` pairs
would cost nothing.

### D-4. `mass_convex` on a degenerate polygon (non-blocking, unreachable)

A clipped polygon of zero area but three or more vertices yields edge normals that
constrain only to a line.
A segment along that line, within the indexed cells, could be counted in full.
No core polygon in this run is degenerate (§4.5). The guard should be on area, not on
vertex count.

### F-5. The Lean reduction is not built here (blocking for the proof-assistant-checked entry)

§7.4 gives the cause, disk space, and the commands.

### F-6. wand125’s “626 core-hours” is wall time (note)

`run_all.py` records `time.time()` per root in a 32-process pool.
Measured CPU here is 0.35 to 0.40 of it.
That is not a correctness matter.
It does mean the source’s cost figure overstates the replay by about two and a half
times.

## 11. For the Records Lane

**This review**, in `T-064`’s `reviews`:

- `kind: adversarial`
- `reviewer`: Claude (Anthropic), method-review lane Y of the 2 October W2 phase,
  separately prompted
- `reviewer_kind: ai`; `relation: project`; `date: '2026-10-02'`
- `scope`: the method of wand125’s independent Valid7 checker (`DESIGN.md`, every module
  of `src/`), its independence, the statement and assumptions of the Lean reduction, and
  the replay cost of both checkers
- `verdict: accepted`, with D-1 dispositioned as non-blocking for the claim and closed
  by a guarded replay or the author’s fix
- `covers: [T-064]`

**The rung does not move on this review.** `V3/C3` needs a complete replay of one
checker, recorded as an exact-algebraic `replayed-here` entry, and the Lean build with
its axiom receipt. §8.5 and §7.4 give the commands.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
