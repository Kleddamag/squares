# Proof Review: The Geometric Premises of Evan Daniel’s `s(60) = 8` and `s(61) = 8`

Reviewed 2026-10-02 from the retained packets, read-only, by Claude (AI review; model
unstated) at maximum thinking effort, as review lane R2 of the W2 phase that is stage 4
of the [result import](../../../packing/campaign/result-import.md) for
[jlevy/squares#256](https://github.com/jlevy/squares/issues/256) (bead `think-x73z`).
The lane was prompted separately from the replay lane and shares no context with it;
this document was written without sight of any replay result, as the
[plan](../specs/active/plan-2026-10-01-result-import-first-application.md) requires.
It covers `T-062` ($s(60) = 8$) and `T-063` ($s(61) = 8$).

The argument from the cover to the bound was read on 1 October
([mathematical transfer](review-2026-10-01-evand-mathematical-transfer.md),
[source coverage](review-2026-10-01-evand-source-coverage.md)) and no defect was found.
What that read left owed, in the plan’s words, is a review of the geometric premises:
the closed-square capture convention, boundary points and segment mass along edges, the
scaling from a side below 8 to side 8, the validity of the D4 reduction, the pose-space
parametrisation, whether every rotation is covered, the outward-rounding assumptions of
the interval checker on x86-64, and the corollary.
The two checkers themselves were re-derived against their code on
[28 September](review-2026-09-28-evand-s21-s45-mixed-covers.md) for the same bytes; that
review is reused, not repeated.
This is evidence for the coordinator, not a verdict of record: no rung moves by writing
it.

**In one line:** every premise holds.
The certificate is a finite nonnegative measure on the closed container, the cover
property is a statement about one closed square at a time, the scaling step turns any
packing at a side below 8 into 60 pairwise disjoint closed unit squares whose captured
masses add, the D4 fold is a theorem about an invariant measure that the data satisfy
exactly, the root boxes of all four shipped runs tile their regions with every angle
reached, the interval checker’s float model is the language’s and holds on x86-64, and
$s(61) = 8$ is one line of monotonicity.
No blocking defect; five notes, none about the mathematics.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `github.com/evand/square-packing`, directory `s12/certificates/s60/` |
| Commit | `08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`, 2026-10-01; the bundle is byte for byte the one at `d9f79bc1`, which the issue names |
| Claims | $s(60) = 8$ (`T-062`); $s(61) = 8$ (`T-063`) |
| Cover | `s60_mixed_cover_8.txt`, sha256 `2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41` |
| Exact checker | `zm_mixed.py` `1fd20346…` (the 28 September review’s `ee3e2915…` plus one guard line, re-read here as a diff), `mixed_cover.py` `bb89de15…`, `zeromargin.py` `640fe453…` |
| Interval checker | `verify2/src/bin/zmx2.rs` `6b7f0f79…` for the shipped runs, retained in the 28 September packet; the pin’s `1cd4dcbd…` is what `verify.sh` builds |
| Run records | `zm_mixed_d4/` (102,400 roots), `zmx2_d4/` (6,400), `zmx2_full/` (51,200), all retained in the [1 October packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md) |

Read in full: the bundle `README.md`, `verify.sh`, `SHA256SUMS`, the three manifests and
`run.log`; `certificates/s21/FORMAT.md` (the format and the reduction); `search/ZMX2.md`
at the pin, §§1 to 7, 10 to 12; `search/S60_COVER.md` §§0 to 2; the retained
`zeromargin.py` functions `clip_bin`, `roots` and `d4_roots`; `zmx2.rs` at `6b7f0f79`
and at `92a4cfe8` as a diff, and its `parse_cover`, `reflect_y`, `check_d4`, `cmd_cert`,
`family_bound`, `pair_bound` and `line_atoms`; the register entries `T-051`, `T-052`,
`T-053`, `T-062`, `T-063`, `T-066` and their evidence; the case records `n-060.md` and
`n-061.md`; the source’s commits `6383ad8` and `4e11002` of 1 October, which postdate
the pin, in a read-only clone.

Scratch instruments written for this review live outside the repository at
`/tmp/claude-0/…/scratchpad/r2/`: `check_cover.py` (an independent parser, exact totals,
the eight symmetries as a measure), `roots_cover.py` (do the shipped root records tile
their regions), and `poses.py` (exact closed-square capture at chosen rational poses).
They import nothing from the source.
Every number below that is not quoted from a named source file comes from one of them.

## 2. Verdict

**(a) $s(60) = 8$, `T-062`: the geometric premises hold, and no defect was found.** The
certificate asserts a statement about closed unit squares inside a closed container,
decided by two programs whose lemma layers were re-derived on 28 September for these
same bytes; the premises the plan listed are each either a theorem (the reduction, the
fold, the mirror), a fact about the data that was recomputed here (the total, the
invariance, the shape of the pieces), or a fact about the records that was recomputed
here (the roots tile the regions, none is uncertified).

**(b) $s(61) = 8$, `T-063`: sound as stated,** and worth nothing on its own: it is
$s(61) \ge s(60)$ by deleting a square and $s(61) \le 8$ by the grid.

What is not machine-checked is unchanged from the $s(45)$ case: the two checker
programs, their lemma layers, the interval checker’s float model, and, because there is
no Lean data file for this cover, the data facts and the top theorem, which rest on
scripts and on the checks of this review.
The findings of §6 are about provenance and wording.
**None is blocking.**

## 3. The Claim

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors, each freely rotated; closed squares, boundary contact allowed.
The source claims no packing of 60 at any side below 8; with the $8 \times 8$ grid,
which holds 64, $s(60) = 8$, the infimum attained.
This is the standard definition, the one `S32.lean` and `S21.lean` formalise
([27 September review](review-2026-09-27-evand-s32-s12.md) §3.1), and the one the
register’s `claim` fields state.
The $s(60)$ bundle has no Lean file; the statement is the same one on paper with
$m = 8$, $n = 60$.

## 4. The Premises, One at a Time

### 4.1 The cover is a measure, and “captures” means the closed square

`s60_mixed_cover_8.txt` is `mixed 1`, $s = 8$, $D = 1000$, $W = 10^8$: 23,744 weighted
points and 5,216 segments, no polygons (`check_cover.py`). The measure is

$$
\mu = \sum_p w_p\thinspace\delta_p + \sum_\sigma w_\sigma \cdot \frac{\lambda|_\sigma}{|\sigma|},
$$

each weight a total, so
$\mu(Q) = \sum_{p \in Q} w_p + \sum_\sigma w_\sigma \cdot |\sigma \cap Q| / |\sigma|$
for any convex closed $Q$ (`FORMAT.md`, “What a file asserts”). What the data are:

- 23,744 distinct point coordinates, every weight positive, numerators in $[2, 964439]$;
  no point on a segment line; all inside $[0, 8000]^2$ at $D = 1000$.
- 2,608 vertical and 2,608 horizontal segments, every one of length exactly $20/1000 =
  1/50$, on the 14 interior grid lines $x, y \in \lbrace 1, \ldots, 7 \rbrace$, no two
  overlapping, weights positive with numerators in $[2, 9279869]$.
- Total $748233441 / 12500000 = 59.85867528 < 60$: points $18.47810664$, segments
  $41.38056864$ (the README’s “41.4 of the 59.86”).

The **cover property** is: for every closed unit square $Q \subseteq [0, 8]^2$, at every
centre and angle, $\mu(Q) \ge 1$. “Closed” is load-bearing twice.
A point on the boundary of $Q$ is in $Q$; a segment lying along an edge of $Q$ has all
its points in $Q$ and counts in full; a segment crossing an edge counts its inside part;
a segment that ends at a grid crossing where another begins shares with it a point of
length zero. This is what both checkers compute: `zm_mixed.py` clips the parameter
interval by four closed half-planes, `zmx2` takes $F(hi) - F(lo)$ over a closed chord,
and every point test is a non-strict inequality
([28 September review](review-2026-09-28-evand-s21-s45-mixed-covers.md) §3.2, §3.4). My
evaluator (`poses.py`) uses the same closed convention and nothing else.

Nothing is double-counted for one square, and nothing need be said about two squares:
the cover property is a statement about one $Q$ at a time, and the 64 grid tiles, which
each capture at least 1 by sharing edge mass and total far more than 60, are simply not
disjoint.

### 4.2 From a packing at side below 8 to a contradiction

Suppose 60 unit squares with disjoint interiors lie in a square of side $s < 8$, closed
or open container, it does not matter.
Scale by $\lambda = 8/s > 1$ about the container’s corner (or its centre; any
homothety). The images $P_i$ are squares of side $\lambda > 1$ in $[0, 8]^2$ with
pairwise disjoint interiors.
The concentric closed unit square $Q_i$ of each lies in the open interior of $P_i$, so
for $i \ne j$, $Q_i \cap Q_j \subseteq \operatorname{int} P_i \cap
\operatorname{int} P_j = \varnothing$: the $Q_i$ are pairwise disjoint closed sets, each
inside $[0, 8]^2$, hence admissible.
Then

$$
60 \le \sum_i \mu(Q_i) = \mu\Big(\bigcup_i Q_i\Big) \le \mu([0,8]^2) \le \mu(\mathbb{R}^2) = 59.85867528,
$$

a contradiction. The equality is additivity over disjoint measurable sets; the argument
uses that $\mu$ is a finite nonnegative measure and nothing else, not even that its
pieces lie in the container.
Every side $s < 8$ is excluded at once; there is no $\delta$, no sequence of
certificates and no compactness step.
This is `packing_le_measure` and `not_packs_of_measure` of `MixedMeasure.lean`, proved
for every $m$ and every measure, read on 28 September and not built here; `FORMAT.md`
gives it on paper. The register’s wording for `T-062`, “its centres scaled by $8/s$”, is
this argument in one step: scaling the centres and keeping the squares unit *is* taking
the concentric cores of the scaled squares.

### 4.3 Why margin zero is forced, and why it is not a gap

At the integer side 8 the grid is a packing, so no cover of total below 60 can have
slack in the scale direction: any shrink of the squares, equivalently any container side
$8 + \varepsilon$, loses the edge mass the tiles share.
That is why 69 % of the mass is on the grid lines and why the certification has to be an
exact subdivision of pose space at the container itself, with germ lemmas for the poses
$\theta \to 0^+$ at which a tile loses one edge’s line mass and gains its partner’s one
unit away (the 28 September review, §3.2 and §6). The least captured masses are not near
1 by accident of sampling: the exact values at the poses the lemmas exist for, by
`poses.py`, are

| Pose | $\mu(Q)$, exact | Decimal |
| --- | --- | --- |
| corner tile $(\tfrac12, \tfrac12)$, $\theta = 0$ | $10250009 / 10^7$ | $1.025000900$ |
| edge tile $(\tfrac32, \tfrac12)$, $\theta = 0$ | $38437573 / (25 \cdot 10^6)$ | $1.537502920$ |
| interior tile $(\tfrac32, \tfrac32)$, $\theta = 0$; at $u = 10^{-5}$ | $183753933 / 10^8$; $1709606365119831 / (1.6 \cdot 10^{15})$ | $1.837539330$; $1.068493293$ |
| central tile $(\tfrac72, \tfrac72)$, $\theta = 0$; at $u = 10^{-3}$ | $10028321 / (6.25 \cdot 10^6)$; $4112003648913 / (4.004 \cdot 10^{12})$ | $1.604531360$; $1.026973938$ |
| box centre $(4, 4)$, $\theta = 0$; at $u = \tfrac12$ ($53.13^\circ$) | $29567323 / (25 \cdot 10^6)$; $14988021 / (12.5 \cdot 10^6)$ | $1.182692920$; $1.199041680$ |
| wall-tight $c_y = w(\theta)/2$ at $c_x = \tfrac32$, $u = 10^{-2}$ | $208587418841137 / (2.020202 \cdot 10^{14})$ | $1.032507734$ |
| tilted $(2.3, 3.2)$, $u = 0.4389$ ($47.4^\circ$, the $s(45)$ cover’s binding region) | — | $1.024080603$ |

The $\theta = 0$ values count whole edges; the $\theta \to 0^+$ values are what the
checkers must beat. The source puts the cover about $0.77\thinspace\%$ above its exact
threshold by `zmx2` bisection (`S60_COVER.md` §0), which these samples are consistent
with. They are samples, not a check; the check is the subdivision.

### 4.4 The D4 reduction

Both `--d4` runs certify only centres in $[0, 4]^2$ and $u = \tan(\theta/2) \in [0,
\tfrac12]$. That suffices by `d4_reduction_measure_u` (`MixedMeasure.lean`, generic in
$m$; the point-set version is `D4.lean`, whose proof the 27 September review read,
§3.3): if $\mu$ is invariant under $x \mapsto m - x$ and $x \leftrightarrow y$, which
generate the dihedral group of the square, then every admissible pose is carried by a
group element to one with $\theta' \in [0^\circ, 45^\circ]$ and centre in $[0, m/2]^2$,
the element preserving admissibility and $\mu(Q)$. The order of the moves matters and is
right: a reflection first, which sends $\theta \mapsto -\theta \equiv 90^\circ - \theta$
and so brings the angle into $[0^\circ, 45^\circ]$ while moving the centre; then quarter
turns, which keep $\theta$ and cycle the four quadrants, to bring the centre into the
closed quadrant. The region $u \in [0, \tfrac12]$ is an over-cover, since
$\tan 22.5^\circ = \sqrt2 - 1 <
\tfrac12$; the checkers certify angles up to $53.13^\circ$ that the fold does not need,
harmlessly, because their lemmas hold wherever $\cos\theta, \sin\theta \ge 0$.

The premise is the invariance, and it must hold of the **measure**, not merely of the
entry list: a segment reflected end for end is the same piece.
`check_cover.py` aggregates the point weights by coordinate and merges the line
densities into piecewise-constant functions on the $1/D$ grid, then applies all eight
group elements to both: the point measure and the segment measure are each invariant
under all eight. `zmx2`’s `check_d4` does the same at the measure level (aggregated
points, canonical density runs per line), which is what its `--d4` run printed;
`zm_mixed.py` printed the same sentence, and its check was not re-read here, since the
fold needs only that the invariance be true, which it is.

Side 8 is the first even side in the family.
Its only consequence is that the quadrant edge $c_x = 4$ lies on the interior grid line
$x = 4$: the fold is indifferent to that, `d4_roots` needs only that $m/2$ be a multiple
of the pitch ($4 / \tfrac{1}{20} = 80$), and `zmx2` that $m$ be a multiple of
$\tfrac15$. Poses on $c_x = 4$ are in the closed region and are certified like any
other.

### 4.5 The pose space and its root boxes

A pose is $(c, u)$ with $Q(c, \theta) = c + R(\theta)[-\tfrac12, \tfrac12]^2$, $\theta =
2\arctan u$, so $\cos\theta = (1 - u^2)/(1 + u^2)$ and $\sin\theta = 2u/(1 + u^2)$ are
rational in $u$; $Q(c, \theta + 90^\circ) = Q(c, \theta)$, so $\theta \in [0^\circ,
90^\circ)$ is every rotation.
A pose is admissible, $Q \subseteq [0, 8]^2$, iff $w(\theta)/2 \le c_x, c_y \le 8 -
w(\theta)/2$ with $w = \cos\theta + \sin\theta$ (`sq_subset_box_iff` in Lean; the
rotated square’s bounding box has half-width $w/2$), and inadmissible poses are exempt
in the statement and in both checkers alike.

The root boxes are closed and must tile the region, so that every pose lies in at least
one; a pose on a face lies in two, and both certify it.
`roots_cover.py` re-derived this from the shipped records, not from the programs:

| Run | Roots in the record | Region | Tiles it | Boxes | Uncertified; capped | Max depth |
| --- | --- | --- | --- | --- | --- | --- |
| `zm_mixed_d4/roots.jsonl` | 102,400 records, 102,400 distinct roots of pitch $\tfrac{1}{20}$ and $u$-width $\tfrac{1}{32}$ | $[0, 4]^2 \times [0, \tfrac12]$ | yes | 500,134 | 0 (the `unc` list of every record is empty) | 18 |
| `zmx2_d4/roots.log` | 6,400, pitch $\tfrac{1}{10}$, $u$-width $\tfrac18$ | the same | yes | 2,617,534 | 0; 0 | 24 |
| `zmx2_full/roots.log` | 51,200: 25,600 in each of two passes | $[0, 8]^2 \times [0, \tfrac12]$, twice | yes | 21,036,120 | 0; 0 | 24 |

The `zm_mixed.py` census (ADM 132,043 / CHAIN 72,081 / SPLIT 59,067 / PIECE 8,666 /
EMPTY 29,410 / UNCERTIFIED 0) equals the manifest’s, and the records satisfy the
binary-tree identity $\text{boxes} - \text{leaves} = \text{leaves} - \text{roots}$
($500134 - 301267 = 301267 - 102400$), so every internal node has two recorded children.
The `zmx2` totals equal the two manifests’.
These are checks that the records describe complete sweeps; that each leaf’s verdict is
right is the checkers’ business (§4.7) and a replay’s.

Within a box each checker certifies “for every *admissible* pose of the box, $\mu(Q)
\ge 1$”, or proves the box holds no admissible pose (`EMPTY`, exact in both: $w(u)$ is
unimodal on $[0, 1]$ with its maximum at $45^\circ$), or halves it; halves are closed
and cover the parent.
`zm_mixed.py`’s `clip_bin` shrinks a bin’s upper end only, only when the bin lies inside
$[0^\circ, 45^\circ]$, and never past the last admissible angle (`clip_bin_no_loss` in
Lean). So a root with no uncertified leaf is certified at every admissible pose.

### 4.6 Every rotation is reached

- **`--d4`**, both checkers: the fold of §4.4 carries every pose into the region, and
  the region’s $u \in [0, \tfrac12]$ contains the fold’s $[0^\circ, 45^\circ]$.
- **`--full`** (`zmx2`, `cmd_cert`): pass 0 sweeps the cover over all of $[0, 8]^2$ with
  $u \in [0, \tfrac12]$, that is $\theta \in [0^\circ, 53.13^\circ]$; pass 1 sweeps the
  cover reflected by $y \mapsto 8 - y$ (`reflect_y`, exact on the integer coordinates
  since $sD = 8000$) over the same boxes.
  The reflection $\rho$ maps $Q(c, \theta)$ to $Q(\rho c, -\theta)$ and $-\theta \equiv
  90^\circ - \theta$, preserves admissibility, and $\rho_*\mu(Q) = \mu(\rho Q)$; so pass
  1 certifying $\rho_*\mu$ at angles $[0^\circ, 53.13^\circ]$ is $\mu$ certified at
  $[36.87^\circ, 90^\circ]$. The union is every angle.

This uses no property of the cover.
It does use the same elementary identity as the fold’s reflection step; what `--full`
drops is the premise that the cover is invariant and the quarter-turn reduction of the
centre, not the identity.
For this cover, which *is* invariant, $\rho_*\mu = \mu$, so pass 1 recomputes pass 0 and
the 51,200-root run carries the same information as a 25,600-root sweep of the cover
over all centres at $u \le \tfrac12$; the argument is nonetheless free of the
invariance, and that is what “no symmetry used” means.
(For the $s(32)$ point cover, where the atom assignment is not rotation-invariant, the
two passes do differ in what they find; that is the subject of
[the companion review](review-2026-10-02-evand-s32-no-fold-run.md).)

### 4.7 What each checker assumes, and what the two share

**`zm_mixed.py --d4 --cert-mode`** (`1fd20346`), exact `Fraction` and integer
arithmetic. Its trust boundary is the lemma layer on paper (`ZM_MIXED.md` §2: Lemmas S,
T, L, L′, V, R, P and Corollary L, re-derived against the code on 28 September, §4 of
that review), the program (subdivision, clipping, inheritance, `SPLIT` bookkeeping,
`--resume`, the parser `mixed_cover.py`), and `zeromargin.py`’s program, whose point
primitives are kernel-checked in `ZeroMargin.lean` and enter through the phantom point.
The only change since that review is the guard at `region_phi`, which refuses a
zero-width angle bin instead of returning an unproved `EMPTY` (one added line in the
diff of the two retained files; the source’s audit item B1, unreachable in the earlier
runs); it can only turn an acceptance into a refusal.
Its floats steer which exact test is tried and never decide one.
Its `int64` region sums carry numerators over $W = 10^8$ totalling about $6.0 \times
10^9$, far below $2^{63}$.

**`zmx2`** (`6b7f0f79`), exact `i128` for every point test and every mass, binary64
intervals rounded outward for the chord ends (Lemma R). Its trust boundary is its own
lemma layer (`ZMX2.md` §§2 to 7: P, C, M, S, Z, W, H, DP, E, R, re-derived on 28
September, §5), its program and parser, and the float model of §4.8. At $s = 8$ its
parser bounds ($s_{num}, s_{den} < 2^{40}$, $D < 2^{20}$, $sD <
2^{27}$, every weight $< 2^{50}$, total $< 2^{56}$, $\mathrm{lcm}$ of segment lengths
$\le 2^{24}$) are met with room ($sD = 8000$, $W = 10^8$, $L_c = 20$), so the size
bounds its audit established ($F \cdot 2^{30} L_c < 2^{110}$) hold for this file as for
the $s(45)$ one.

**Shared**, and so the common mode of a two-checker confirmation: the author and the AI
agent; the statement decided and the reduction of §4.2; the pose parametrisation, the
closed root boxes and the admissibility exemption; branch and bound over $(c, u)$ with
closed halves; in the `--d4` runs, the fold; and the point-in-square formulation, which
the source now states plainly (`6383ad8`, in the bundle READMEs and `FORMAT.md` after
the pin): `zmx2`’s Lemma P uses the violation polynomials $G_0$ to $G_3$ of
`zeromargin.py`’s write-up, and `zm_mixed.py` tests points by calling `zeromargin.py`,
so “an error in that formulation would be common to both”.
For this cover the point part is $18.5$ of $59.9$, and the formulation is kernel-checked
on the `zeromargin.py` side (`lemmaA`, `polyOk_quad` in `ZeroMargin.lean`), which bounds
that risk. **Not shared:** the line and segment mathematics (Lemmas T, L, R with chains,
against Lemma Z’s pair dynamic programme), the arithmetic, the parsers, and, in
`zmx2 --full`, the fold.
The pin’s own README still says “two independently written checkers”; the author’s
commit of 1 October changes it to “separately written” with the shared lineage stated,
and the register should use the later wording.

### 4.8 The float model, and x86-64

Lemma R needs: IEEE-754 binary64 with correctly rounded $+\thinspace-\thinspace\times
\thinspace\div\thinspace\sqrt{}$ in the default round-to-nearest mode; no contraction of
a multiply and add into a fused operation; no evaluation in a wider format; and exact
`next_up` / `next_down`. Then every rounded result $r$ of an exact $x$ satisfies $x \in
[\text{next\_down}(r), \text{next\_up}(r)]$, the widening is an enclosure, and the step
onto the integer grid $G = D \cdot 2^{30}$ rounds a lower bound down and an upper bound
up.
The 28 September review (§5, F4) found that these are guarantees of Rust for `f64` on
every tier-1 target, not of x86-64: no fast-math flags are ever emitted, contraction
needs an LLVM flag Rust does not set, `f64::sqrt` lowers to the correctly rounded
instruction, and `next_up` is bit-level (stable since Rust 1.86; the shipped runs used
1.91.1). On x86-64 the operations are SSE2 scalar with no x87 extended precision, which
is the case the source states (“x86-64 SSE2”) and the case of this project’s replays, so
the source’s stated platform and the replay platform coincide.
Checked here in addition: `verify2/Cargo.toml` at the pin sets `opt-level = 3` and `lto
= true` and no `target-cpu` or `overflow-checks`; there is no `.cargo/config.toml`; and
`s60_cert_runs.sh`, `zmx2_sym_run.sh`, `zmx2_run.sh` and `verify.sh` all build with a
bare `cargo build --release --bin zmx2` and set no `RUSTFLAGS`. What a replay owes the
record is the target triple from `rustc -vV`, the absence of `RUSTFLAGS` in its
environment, the compiler version and the binary digest, beside the source digest that
is the reproducibility handle (the earlier review’s F2).

### 4.9 The corollary: $s(61) = 8$

Deleting one square from a packing of 61 unit squares at side $s$ leaves a packing of 60
at side $s$, so $\lbrace s : 61 \text{ pack} \rbrace \subseteq \lbrace s : 60 \text{
pack} \rbrace$ and $s(61) \ge s(60) = 8$; the $8 \times 8$ grid holds 61, so $s(61) \le
8$. That is the whole of `T-063`, and it inherits the un-replayed premise of `T-062` and
nothing else. Two other routes to the same value exist in the record and are no evidence
for this entry: the same source’s family $s(k^2 - 3) = k$ at $k = 8$ (`T-064`, one exact
checker, a conditional Lean reduction, `V0/C1`), and wand125’s $s(59) = 8$ (`T-066`,
`V0/C0`), which by the same monotonicity would give $s(60) = s(61) = 8$ as well.
By the runbook nothing is superseded; each entry gains a sentence naming the others, and
`T-062` and `T-063` already carry theirs.

## 5. Evidence

| Obligation | Result here |
| --- | --- |
| Cover digest and identity | the retained `.gz` decompresses to sha256 `2d0e456e…`, the value in `SHA256SUMS` and in all three manifests |
| Well-formedness, total, shape of the pieces | §4.1, `check_cover.py`, about a second |
| Invariance as a measure under all eight elements of D4 | points and segments both invariant, `check_cover.py` |
| The records tile their regions, none uncertified, tree identity | §4.5, `roots_cover.py` |
| Checker identity | `zm_mixed_d4/manifest.json` and `run.log` name `zm_mixed.py 1fd20346`, `mixed_cover.py bb89de15`, `zeromargin.py 640fe453`, the retained `search/` files of the 1 October packet; the two `zmx2` manifests name `zmx2.rs 6b7f0f79`, the 28 September packet’s file, binary `0247012e`, rustc 1.91.1, git `86cb2d80` with no local change; `86cb2d80` is an ancestor of the pin and its `zmx2.rs` hashes `6b7f0f79` (clone, `git cat-file`) |
| The two retained `zm_mixed.py` versions | differ by the one guard line at `region_phi` (`diff`) |
| Exact captures at critical poses | §4.3, `poses.py`; every sampled admissible pose captures $> 1$, the least $1.0250$ at the corner tile |
| Compiler and build flags | §4.8 |

## 6. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. The README’s provenance paragraph describes records the bundle no longer ships (non-blocking)

`README.md`, “Provenance of `zm_mixed_d4/`”, says the records were imported from the 28
September run (19.6 CPU-h, 12 processes) with only the input path changed, that
`manifest.json` therefore shows `wall_s` 0.1 and `--nproc 1`, and that `run.log` is the
original log followed by the resume’s. The shipped `manifest.json` is a complete fresh
run: `created 2026-09-30 00:42:56`, `--nproc 8`, `wall_s 9024.2`, CPU $71978.8$ s
($20.0$ CPU-h), and `run.log` holds that one run.
This is the re-run of 29 September that the README’s last paragraph describes (“records
and `checker/` replaced”), so the provenance paragraph is stale, not wrong about the
bytes. A replay compares censuses and is unaffected; tell the author.

### F2. `verify.sh` builds `zmx2` from the pin’s source, not the one that made the records (non-blocking)

The manifests name `zmx2.rs 6b7f0f79`; `verify.sh` runs `cargo build` on whatever
`verify2/src/bin/zmx2.rs` is, which at the pin is `1cd4dcbd`, a diff of 1,786 lines
later (`--sym-atoms`, area densities, `--first-order`, all opt-in by the source’s
account). The README’s note of 30 September says the fresh run reproduces the shipped
census root for root.
The replay should either build `6b7f0f79` from the 28 September packet, or build the
pin’s source and let the root-for-root comparison test the claim; either way the receipt
names which.

### F3. No Lean data file or top theorem for this cover (note)

As for $s(45)$: `not_packs_of_measure` and `d4_reduction_measure_u` are proved for every
$m$, and the data facts (total $< 60$, invariance) rest on the source’s scripts, on
`zmx2 d4`, and now on `check_cover.py`. The source says so plainly.
This is the part that sets the rung, as in the 28 September review (F5, F6).

### F4. The source has made no cover-specific controls for this bundle (note)

The README’s review record says no adversarial component tests or holed-cover rejection
runs were made on this cover.
The runbook asks the replay for two mutated certificates refused by every checker that
accepted the original, held by a test; for this cover those will be the first.

### F5. Wording the register should take from the source’s later commit (note)

The pin’s README and site call the two checkers “independently written”; the author’s
`6383ad8` and `4e11002` of 1 October, which postdate the pin, say “separately written,
sharing no code but sharing the point-test formulation”, as §4.7 states.
`T-062`’s claim does not use the word “independent” and needs no change; the reply on
issue 256 should quote the later wording.

## 7. What the Replay Must Show

For `T-062` and `T-063` to reach `V3/C3`, with this review as the mapped review and no
blocking defect open, the replay lane must retain receipts showing, from a clean copy of
the source tree at the pin with the packet’s `.gz` files restored and `python3` the
project interpreter:

- `certificates/s60/verify.sh` ending `s(60) bundle: OK`, with every step passed:
  `sha256sum -c` clean; `mixed_records.py cover` reporting the total
  $748233441/12500000 < 60$ and the measure D4-invariant; the shipped `zm_mixed.py`
  records re-summarised with header digests equal to the checker files and the cover and
  all 102,400 roots certified; the three checker files `cmp`-equal to the $s(21)$
  bundle’s and `zeromargin.py` to the $s(32)$ bundle’s; both shipped `zmx2` records
  re-summarised (6,400 and 51,200 roots, every root of each region, none uncertified);
  `zmx2 d4` passing; a fresh `zmx2 cert … --full` printing `VERIFIED` with 51,200 roots,
  21,036,120 boxes, 10,414,200 certified, 129,460 empty, 0 uncertified, max depth 24;
  and `fresh census identical to the shipped zmx2_full/roots.log, root for root`.
- A fresh `zmx2 cert … --d4`, which `verify.sh` does not run: `VERIFIED-D4`, 6,400
  roots, 2,617,534 boxes, 1,295,988 certified, 15,979 empty, 0 uncertified, max depth
  24, and its census equal to the shipped `zmx2_d4/roots.log` root for root.
- Which `zmx2.rs` was built (F2), its digest, `rustc -vV` with the target triple, that
  `RUSTFLAGS` was unset, and the binary digest; the host’s architecture.
- Two mutated covers refused by `zmx2` (and by `zm_mixed.py` where it is run), with the
  refusing pose, and a test that holds them.
  Scaling every weight down exactly while keeping the invariance (the 28 September
  review used $\times 0.994$ and $\times 0.985$) and removing one segment orbit are the
  natural pair. The source’s bisection puts the exact threshold of the unscaled round
  cover between the factors $1.016875$ (refused) and $1.0171875$ (verified), and the
  shipped cover is that round cover times $41/40 = 1.025$; so a copy of the shipped
  cover scaled by $1.016875 / 1.025 = 0.99207$ or less is refused and one scaled by
  $0.99238$ verifies. A factor of $0.99$ should fail, and the 28 September review’s
  $0.985$ certainly; $0.995$ would verify and is not a control.
- The measured CPU of each run beside the source’s 22 s and 177 s.

The `zm_mixed.py --d4 --cert-mode` sweep (`verify.sh --full`, about 20 CPU-h) is the
second route the plan names and not a condition of `C3`; if it runs, it must print
`census identical to the shipped records for 102400 / 102400 roots`, `VERIFIED-D4`,
500,134 boxes, 0 uncertified, with no `note: search/… differs from the shipped checker`
line.
`devtools.audit_evand_mixed_covers` must be extended to case 60 before the receipts
are read by it (`think-ubor`).

## 8. Rung, Significance and Credit

Under [`epistemics.md`](../../../epistemics.md):

- **Now:** `V0/C1` for both entries, unchanged by this read; a second read is no kind of
  verification.
- **On a passing replay:** `V3/C3`, the rungs `T-052` and `T-053` stand at on the same
  kind of evidence (a complete replay of the source’s checker, its controls, and a
  mapped review with no blocking defect open), with the `zm_mixed.py` route, if run,
  recorded beside the rung as the second arithmetic and not as a condition.
  Rung 4 needs a second adversarial review by a distinct reviewer and a human oversight
  record, and rung 5 a proof-assistant check of the covering statement, which the source
  has not attempted for this cover.
  `T-063` rises with `T-062` and never above it.

**Significance.** `T-062` was drafted `S3`. Compared with the entries nearest it:
`T-053` ($s(45) = 7$, `S4`, scored as the third of a bound family by a technique that
“alone would argue for S3”), `T-066` ($s(59) = 8$, `S3` draft, set beside `T-062`), and
the source-coverage review’s own suggestion (`S3`, `S4` only for a reusable advance
beyond the $s(21)$/$s(45)$ method).
The claim settles an open case by the route of `T-052` and `T-053` (`S60_COVER.md` §0:
“the $m = 7$ line-cover recipe at $s = 8$”) and adds no technique, so by the anchor “a
substantive case result” it is **`S3`, confirmed**. The family argument that lifted
`T-053` to `S4` applies to `T-062` exactly as it did there, so consistency requires
`T-053` and `T-062` to carry the same score; which score that is belongs to the
rescoring pass the plan names (`think-qh3s`), and this review does not settle it.
`T-063` is **`S1`, confirmed**: a routine consequence, immediate once its premise is
proved.

**Credit.** The result is Evan Daniel’s (`evand`), computer-assisted, with the mixed
cover and both checkers his; the weighted-cover idea is credited by the source to Burns
and Massaccesi and the verification practices to Mira’s `17squares`, as in `CREDITS.md`,
which says the work was produced by Claude under human direction.
The source claims no peer review and says the bundle has had no independent review; this
document and the 1 October read are the first.

**Licence.** MIT (`LICENSE` under `s12/`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
