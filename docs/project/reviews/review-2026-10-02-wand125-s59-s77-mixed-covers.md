# Proof Review: wand125’s `s(59) = 8` and `s(77) = 9` by Mixed Covers

**Date:** 2026-10-02. **Lane:** R1, the review lane of the W2 phase that is stage 4 of
the [result import runbook](../../../packing/campaign/result-import.md) for issues
[280](https://github.com/jlevy/squares/issues/280) and
[279](https://github.com/jlevy/squares/issues/279), beads `think-oy3i` and `think-xujq`.
**Reviewer:** Claude, model Fable, at maximum thinking effort, separately prompted, with
no shared context with the replay lane: nothing of the replay lane’s work, and no
receipt or log written after 2026-10-02T00:00Z, was read.
It is an adversarial soundness review of two computer-assisted exact values registered
as reported, $s(59) = 8$ (`T-066`) and $s(77) = 9$ (`T-067`), and of the corollaries the
record states for them in `T-062`, `T-063` and `T-064`. It replays nothing: the verdicts
of the checkers below are the source’s, and what was computed here is said to be.

**In one line:** each value rests on a mixed cover of the closed container, a finite
nonnegative measure of weighted points and of mass spread uniformly along axis-parallel
segments, of total $58.9905 < 59$ (side 8) and $76.99998 < 77$ (side 9), such that every
closed unit square inside the container captures mass at least 1; the reduction from
that to the bound is the concentric-shrink argument already reviewed for Evan Daniel’s
$s(21)$, $s(45)$ and $s(60)$ covers, and both covers are in his format and were decided
by his two checkers at a pinned revision; I re-derived the argument, re-checked both
covers’ data facts exactly with my own code, read every lemma the new cover shapes
touch, and found no mathematical defect in either claim.
What the published tree does not let anyone verify is the exact-rational route for
$s(59)$: it is a composite of two `zm_mixed.py` runs whose logs and per-root records are
pinned by digest but absent, so that route is a reported one.
The claim does not rest on it: one complete `zmx2` sweep, replayed here, is what the
rung rules need, and the replay lane is what decides the rung.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `wand125/square-packing-bounds` at `1a25a5ed745fdd905a52f48fcc48150a0669032d` (2026-10-01T21:10:40Z), retained in [`packing/resources/web/wand125-point-and-mixed-2026-10-01/`](../../../packing/resources/web/wand125-point-and-mixed-2026-10-01/README.md) |
| Claims | $s(59) = 8$ (`certificates/k2m5_n59_L8/`, `T-066`); $s(77) = 9$ (`certificates/k2m4_n77_L9/`, `T-067`) |
| $s(59)$ cover | `n59_mixed_cover_8.txt`, SHA-256 `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`, retained gzipped |
| $s(77)$ cover | `n77_mixed_cover_9.txt`, SHA-256 `47b57cfe38cbfdbcf5320e59caffe712f4ef32df8aad42b0d7f697de6d26cdd7`, retained gzipped |
| Base cover of $s(77)$ | Daniel’s `s60_mixed_cover_8.txt`, `2d0e456e…2a41`, in the [October 1 evand packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md) |
| Checkers, pinned by both `verify.sh` at `evand/square-packing` `b91d70b6ed314624c1434b628a9c7bf9a132c743` (2026-09-29T01:21:40Z) | `s12/verify2/src/bin/zmx2.rs` `6b7f0f79…3fed` and `s12/search/zm_mixed.py` `ee3e2915…60ac`, `mixed_cover.py` `bb89de15…aae5`, both retained in the [September 28 evand packet](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md); `s12/search/zeromargin.py` `640fe453…86ab`, retained in the [September 26 packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md), which also holds `verify2/Cargo.toml` and `Cargo.lock` at their `b91d70b6` blobs |
| Run records | `k2m5_n59_L8/zm_mixed_d4/manifest.json`, `k2m5_n59_L8/zm_mixed_root/manifest.json`, `k2m4_n77_L9/zm_mixed_d4/manifest.json`; the four `zmx2` logs and three `zm_mixed` logs named in the two `SHA256SUMS` are not in the tree |
| Write-ups read | both certificate READMEs and `verify.sh`; the packet README; `certificates/s21/FORMAT.md` (mixed v1); `search/ZMX2.md` (the pinned version and the 2026-09-30 §4.9, §4.10 and §12 added upstream in `6c3f625`); `search/ZM_MIXED.md` §1, §2 (Lemma T, Corollary T′), §5, §8; `search/ZM_MIXED_AUDIT.md`; Daniel’s `s60` README; upstream commits `6717ff8`, `37b2ac2`, `e4af291`, `2360b46`, `5085c00` after the pin; Daniel’s comment of 2026-10-02T01:03Z on issue 279 |
| Code read | `zmx2.rs` (2,069 lines): parser and input bounds, `build_cover` (atoms, `--pair-points`), `check_d4`, `reflect_y`, `line_atoms`, `eval_node`, `split`, `run_root`, `cmd_cert`; `zm_mixed.py` (1,699 lines): `Cover`, `LineMass`, `line_pieces`, `piece_bound`, `_group`, `lemma_l_data`, `region_phi`, `vertex_split`, `cert_split`, `run_box`, `_set_phantom`, `main`; `zeromargin.py`: `bin_data`, `clip_bin`, `Checker.__init__`, the `Wnum`/`Wden` paths of `CHAIN`; `mixed_cover.py`: `load`, `validate`, `total` |
| Earlier reviews relied on | [the $s(21)$ and $s(45)$ review](review-2026-09-28-evand-s21-s45-mixed-covers.md), which re-derived every lemma of both checkers against their code at these exact hashes; [the $s(32)$ review](review-2026-09-27-evand-s32-s12.md) for `zeromargin.py`; [the 1 October transfer review](review-2026-10-01-evand-mathematical-transfer.md) for the $s(60)$ report and its corollary |

Scratch instruments written for this review live outside the repository under
`scratchpad/r1/`: `check_cover.py` (an independent parser; exact totals;
well-formedness; segment geometry; points on loaded and grid lines; the `zmx2` parser
bounds; the `--pair-points` atom census; invariance of the measure under all eight
elements of $D_4$, and separately under `zm_mixed.py`’s raw-multiset criterion) and
`mass.py` (an exact evaluator of $\mu(Q)$ at a rational pose, closed square, parametric
segment fractions). They import nothing from the source.
Every number below that is not quoted from a source file is from one of them, in
`Fraction` arithmetic, and took seconds on one core.

## 2. Verdict

**(a) $s(59) = 8$, `T-066`: no mathematical defect found; the exact-rational route is
reported, not reproducible from the tree.** The cover is well formed, totals exactly
$1474762899/25000000 < 59$, and is invariant under $D_4$ as a measure; the reduction
from the cover property to the bound is the one proved in Lean for every side for
Daniel’s covers (§3); the two `zmx2` sweeps the source reports, 6,400 roots with the
symmetry and 51,200 without, are decisions of the checker reviewed on 28 September at
the same source hash, on a cover of the same shape as the $s(60)$ cover it was built
from. The `zm_mixed.py` evidence is two runs that together cover the $D_4$ region if and
only if the six boxes the complete depth-24 sweep leaves uncertified lie in the one root
the depth-34 run certifies; that premise is stated in the README and checked by
`verify.sh`, but the log and the records that would show it are not published (§7.3).
The zero-width-bin guard that Daniel added to `zm_mixed.py` the day after the pin could
not fire in either run, by an argument given in §7.4.

**(b) $s(77) = 9$, `T-067`: no mathematical defect found.** The cover totals exactly
$43347137744028965/2^{49} < 77$ and is $D_4$-invariant as a measure and as
`zm_mixed.py`’s raw multisets, so the cut-and-shift construction and the band measure
kept the invariance (§8.4). The shapes this cover brings that the reviewed covers did
not, three segment lengths including $2/1000$, 632 overlapping segment pairs on one
line, a weight unit of $2^{-49}$, and partner lines made from off-grid point pairs by
`--pair-points`, each enter a lemma only through quantities the lemmas allow, and the
integer sizes they produce are inside the bounds both checkers enforce (§8.2, §8.3). The
register’s worry that the cover has points on loaded lines is moot: after the
replacement it has none, on a loaded line or on any grid line.

Both values stand on the two checkers’ verdicts as the source reports them.
The findings (§10) are about what is published and how, and none is blocking for the
claims; one is blocking for recording the `zm_mixed.py` route of $s(59)$ as evidence.

## 3. From Certificate to Claim

### 3.1 The statement

$s(n)$ is the least side of a square containing $n$ unit squares with pairwise disjoint
interiors, each freely rotated, boundary contact allowed; in Daniel’s Lean,
`minSide n = sInf {s | Packs n s}` with `Packs n s` the existence of $n$ closed unit
squares inside $[0,s]^2$ with pairwise disjoint open interiors.
The claims are $s(59) = 8$ and $s(77) = 9$ in that sense, for the unrestricted problem.

### 3.2 The measure and the closed conventions

A file in Daniel’s `mixed 1` format
([`FORMAT.md`](../../../packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/certificates/s21/FORMAT.md))
defines $\mu = \sum_p w_p\,\delta_p + \sum_\sigma w_\sigma\,\lambda_\sigma$ on
$[0,s]^2$, where $\lambda_\sigma$ is the uniform probability measure on the closed
segment $\sigma$, all coordinates integers over $D$ and all masses integers over $W$.
The file asserts

> for every closed unit square $Q \subseteq [0,s]^2$, at every centre and every angle,
> $\mu(Q) \ge 1$.

For a convex closed $Q$, $\mu(Q) = \sum_{p \in Q} w_p + \sum_\sigma w_\sigma\,
|\sigma \cap Q|/|\sigma|$. The conventions the checkers implement, and that the
reduction needs, are: a point on $\partial Q$ counts in full; a segment lying along an
edge of $Q$ counts in full; a segment crossing $\partial Q$ counts the parametric
fraction of its closed intersection with $Q$ (`zm_mixed.py` clips the parameter interval
by the four closed half-planes, `zmx2` takes $F(\mathrm{hi}^*) - F(\mathrm{lo}^*)$ over
a closed chord); two segments that share an endpoint share a set of measure zero, so
nothing is counted twice for one square; and overlapping segments on one line add, as
measures do. Nonnegativity of every weight is checked by both parsers (`validate`,
`parse_cover`) and is the one property of $\mu$ the reduction uses beyond measurability.

### 3.3 The reduction

Suppose $n$ unit squares with disjoint interiors fit in $[0,s']^2$ with $s' < s$. Scale
by $\lambda = s/s' > 1$: the images are $n$ squares of side $\lambda$ inside $[0,s]^2$
with disjoint interiors.
The concentric closed unit square of each lies in the open interior of its parent, so
the $n$ closed unit cores $Q_1, \dots, Q_n$ are pairwise disjoint as sets, not only
interior-disjoint, and each is contained in $[0,s]^2$. By the cover property and
additivity of $\mu$ on disjoint measurable sets,

$$
n \le \sum_i \mu(Q_i) = \mu\Big(\bigcup_i Q_i\Big) \le \mu([0,s]^2) \le \text{total} < n,
$$

a contradiction. Hence no packing of $n$ exists at any side below $s$, so $s(n) \ge s$.
The 25 tiles of the $5 \times 5$ grid, each capturing at least 1 at the integer side
while the total is below $n$, are not a contradiction: the cover property speaks of one
square at a time and the tiles are not disjoint; disjointness is only used after the
strict shrink. This is `packing_le_measure` and `not_packs_of_measure` in Daniel’s
`MixedMeasure.lean`, proved for arbitrary finite measures and every side, as the 28
September review verified; no limit, compactness or $\varepsilon$ enters, which is why a
cover at margin zero in the scale direction is a proof and not a near miss.

### 3.4 The pose space, the fold and its hypothesis

A pose is $(c, \theta)$ with $Q(c,\theta) = c + R_\theta[-\tfrac12,\tfrac12]^2$;
$Q(c, \theta + 90^\circ) = Q(c, \theta)$, so $\theta \in [0^\circ, 90^\circ)$ is every
pose. Both checkers use $u = \tan(\theta/2)$, $\cos\theta = (1-u^2)/(1+u^2)$,
$\sin\theta = 2u/(1+u^2)$, so that everything is rational in $u$. $Q \subseteq [0,s]^2$
iff $w/2 \le c_x, c_y \le s - w/2$ with $w = \cos\theta + \sin\theta$; poses outside
this closed set are exempt from the cover property and from both checkers alike.

**The $D_4$ fold.** If $\mu$ is invariant under $x \mapsto s - x$ and
$x \leftrightarrow y$, then it is invariant under the group they generate, and every
pose is carried by some element to one with $c \in [0, s/2]^2$ and
$\theta \in [0^\circ, 45^\circ]$, since quarter turns keep $\theta$ and reflections send
it to $90^\circ - \theta$; the image square has the same mass.
So it suffices to certify centres in $[0,s/2]^2$ and $u \in [0, \tfrac12]$, which
contains $\tan 22.5^\circ = 0.4142$ and is an over-cover.
`zmx2 --d4` and `zm_mixed.py --d4` check the two generators exactly before sweeping, on
the aggregated point weights and on the lines’ densities, and refuse otherwise; the
sweep covers $[0, s/2]^2 \times [0, \tfrac12]$ by closed root boxes: `zmx2` at centre
pitch $1/10$ with four $u$-bins of width $1/8$ (6,400 roots at $s = 8$, 8,100 at
$s = 9$), `zm_mixed.py` at pitch $1/20$ with sixteen bins of width $1/32$ (102,400 and
129,600). `zmx2 --full` uses no symmetry: the cover on $u \in [0,\tfrac12]$ over all
centres ($\theta \le 53.13^\circ$), then the cover reflected by $y \mapsto s - y$ on the
same boxes, which covers $\theta \in [36.87^\circ, 90^\circ]$ (51,200 and 64,800 roots).

### 3.5 The upper half and the exact value

The $8 \times 8$ grid holds $64 \ge 59$ unit squares and the $9 \times 9$ grid holds
$81 \ge 77$, so $s(59) \le 8$ and $s(77) \le 9$ (`E-basic-grid-upper`, replayed here).
With the lower bounds, the feasible sides are exactly $[8, \infty)$ and $[9, \infty)$;
the infimum is attained and the values are exact.

## 4. `zmx2`: Trust Boundary

**What it decides.** For every root box
$B = [x_0,x_1] \times [y_0,y_1] \times [u_0,u_1]$ of the region, by branch and bound,
that $\mu(Q(c,\theta)) \ge 1$ at every admissible pose of $B$: a bound $L(B) \le \mu(Q)$
valid at every admissible pose is computed, a box is a leaf when $L(B) \ge 1$ or when no
pose of it is admissible (Lemma E), otherwise it is halved (closed halves that cover it)
down to depth 40, a centre or $u$ denominator exponent of 28, or a node cap of
$2 \times 10^7$ per root, beyond which the remaining boxes are reported uncertified.
`VERIFIED-D4` or `VERIFIED` is printed only when every root of the region ran and none
has an uncertified box (`cmd_cert`); a capped root pushes its whole stack into the
uncertified list; a panic prints no verdict.

**What the bound is.** $L(B) = P(B) + \sum_{\text{families}} \Phi(B)$: $P$ is the exact
weight of the ordinary points certainly inside $Q$ at every pose of $B$ (Lemma P, four
quadratics in $u$ at the four centre corners, decided in `i128`); for each family of
lines a dynamic programme over chains of lines at unit spacing (Lemma DP) takes the
better of single-line chord bounds (Lemma S) and the pair bound of Lemma Z, which closes
the tile germs at $\theta \to 0^+$ because the right edge’s crossing of $x = \ell + 1$
is exactly $u$ above the left edge’s crossing of $x = \ell$; Lemma W lowers the chord
ends of a line at distance 1 from a wall using admissibility; Lemma H covers
$\theta = 0$ itself inside a $u_0 = 0$ box by the limits of the chord-end functions;
horizontal lines are vertical lines in the frame rotated by $(x,y) \mapsto (-y,x)$
(Lemma T). A point on a line of the family (an interior unit grid line, a segment line,
or with `--pair-points` an abscissa or ordinate with a partner point at distance exactly
1\) is an *atom* of that line, counted inside the line bounds by its own four
conditions; the assignment order is vertical grid or segment line, then horizontal, then
vertical partner, then horizontal partner, and a point is an atom of exactly one line.

**What it assumes.** (i) The lemmas, proved on paper in `ZMX2.md` and audited by the
source and by the 28 September review, not in Lean.
(ii) Lemma R: every `f64` operation on the certification path is IEEE-754 binary64
round-to-nearest with correctly rounded $+\,-\,\times\,\div\,\surd$, no contraction and
no reassociation, and `next_up`/`next_down` are exact; each result is widened by one ulp
in the safe direction and then rounded outward onto the integer grid of pitch
$1/(D \cdot 2^{30})$, after which everything is `i128`. Rust guarantees the compiler
side on every tier-1 target and the run was on x86-64 SSE2; the process assumptions are
the default rounding mode and no flush-to-zero.
(iii) The parser’s input bounds ($s_{num}, s_{den} < 2^{40}$, $W < 2^{50}$,
$D < 2^{20}$, $sD < 2^{27}$, every weight $< 2^{50}$, total $< 2^{56}$, lcm of segment
lengths $\le 2^{24}$), which make every `i128` product on the certification path smaller
than $2^{127}$; release builds have no overflow checks.
(iv) For `--d4`, that $\mu$ is $D_4$-invariant, which it checks exactly (`check_d4`:
aggregated points, canonical line densities).
(v) The program: its own parser (not `mixed_cover.py`), the subdivision and bookkeeping,
the `--log` resume keyed on an FNV hash of the file and settings.
The float pre-filter of points only chooses which points are tested; dropping lowers
$L$.

**`--pair-points`.** The flag only changes which points become atoms and on which lines.
Soundness does not depend on the assignment: the line lemmas hold for a line carrying
any finite set of positive atoms, each point is an atom of exactly one line or ordinary,
so the decomposition $\mu = \mu_{\text{ord}} + \sum_\ell \nu_\ell$ into nonnegative
measures that Lemma DP sums over is valid for either rule (Daniel’s Lemma A of
2026-09-30 states this for the pinned code’s rule and its mirror; the 28 September
review had already traced the atom conditions in §5). Completeness does: the rule is not
invariant under the quarter turns, which is why Daniel’s `--full --pair-points` run of
the $s(32)$ point cover left 152 boxes at rotated images of one germ (`ZMX2.md` §12,
after the pin). That is a loss a run reports, never a false acceptance.

## 5. `zm_mixed.py`: Trust Boundary

**What it decides.** The same statement over the same kind of closed boxes, root grid
pitch $1/20$ and sixteen $u$-bins, in exact `Fraction` and integer arithmetic.
Per box, after `clip_bin` (which only lowers $u_1$, §7.4), it computes a certified lower
bound $L$ on the segment mass at every admissible pose by Lemma S (the certified core of
each line, from Bernstein enclosures of the four containment polynomials, which are
affine in the point), Lemma T (the germ pair: lines $x = \xi$ and $x = \xi + 1$ share
one threshold $T$ with $T + u_0 \le T + u$, and the pair’s mass is a piecewise-linear
function of $T$ minimised exactly over its breakpoints and tails), Lemma L and L′ (chord
ends moving within exact windows, hull minorants) and Corollary L (concavity in the
centre, Bernstein ratio bounds in $u$); then hands $L$ to `zeromargin.py`’s point
primitives `ADM → P1 → MIX → CHAIN` as a phantom point of weight $\lfloor L \cdot
W_{den} \rfloor / W_{den}$ declared inside $Q$ at every admissible pose (Lemma P), and
last tries `SPLIT` (Lemma R), which couples pieces and points region by region along one
exact pivot chain. A leaf is `PIECE`, `ADM`, `P1`, `MIX`, `CHAIN`, `SPLIT` or `EMPTY`;
otherwise the box is halved to the depth limit and reported uncertified.
Children inherit $\max(L, L_{\text{parent}})$ and the exact set of points proved inside
$Q$ on the parent, with the phantom bit cleared.

**What it assumes.** (i) Its lemmas, proved in `ZM_MIXED.md` §2 and audited
(`ZM_MIXED_AUDIT.md`, the 28 September review §4), not in Lean; `zeromargin.py`’s
primitives have their lemmas in `ZeroMargin.lean` but the programs are unverified.
(ii) `--cert-mode`: Corollary T′ (points on germ lines counted inside the groups) and
the polygon code are unreachable, so a point on a loaded line is an ordinary point;
sound and possibly weaker.
(iii) `--d4`: invariance of the raw entries as multisets under the two generators
(`symmetric_d4`), a criterion stronger than invariance of the measure.
(iv) `CHAIN`’s region sums are `int64` numerators over $W_{den} = \mathrm{lcm}$ of the
weight denominators, with `CHAIN` disabled when $W_{den} > 10^{15}$; the exact
comparisons elsewhere are `Fraction`s. (v) Floats choose which exact bound to compute
(hull edges, split points, the mid-bin option corrected by an exact slack, the swing
inequality of a point, the reach window) and can only lose certifications.
(vi) The program: `mixed_cover.py`’s parser, `multiprocessing`, `--resume` records keyed
by a header that holds the four SHA-256 values, the settings and the total, and refused
on mismatch. The partial-region options filter *roots* by strict overlap with the region
and sweep each kept root whole; the verdict then carries `(PARTIAL)`.

## 6. What the Two Checkers Share

They share the statement they decide, the closed-square conventions of §3.2, the
reduction and the $D_4$ fold of §3, the architecture (branch and bound over closed
$(c, u)$ boxes, $u = \tan(\theta/2)$, admissibility exemption, the germ closed by a pair
lemma at unit spacing), and their author: both were written in Evan Daniel’s repository
with an AI agent under his direction, as his `CREDITS.md` says, and `ZMX2.md` §10 says
the harness and the code were written by the same agent.
`ZMX2.md` states that `zmx2` was written from the format statement alone, without
reading `zm_mixed.py` or its write-up, and the code bears that out: `zmx2` has its own
parser, `zm_mixed.py` uses `mixed_cover.py`; the lemma families differ (T, L, L′, R and
`zeromargin.py`’s chains against Z, W, DP and Lemma P alone); the arithmetic differs
(rationals against outward-rounded binary64 on an integer grid); the symmetry assumed
differs (`zmx2 --full` assumes none).
What they share is also what wand125 shares with them: the runs on both covers were made
by wand125, on the same cover bytes, so the cover file is the common input.
A wrong total or a broken invariance would be caught by either parser and by mine; a
wrong lemma shared by both would not be, and there is no such shared lemma.
The residual common mode is the architecture and the authorship, as the 28 September
review recorded for $s(21)$ and $s(45)$.

## 7. The $s(59)$ Certificate (C, `T-066`)

### 7.1 The cover, checked here

`check_cover.py`, own parser, exact: header `mixed 1`, $s = 8$, $D = 1000$, $W = 10^8$;
26,308 points and 5,240 segments, every segment of length exactly $1/50$, axis-parallel,
on the fourteen lines $x, y \in \{1, \dots, 7\}$; no zero weight, no repeated point
coordinate, no repeated or overlapping segment; every piece inside $[0,8]^2$; total
$1474762899/25000000 = 58.990515960$ exactly, of which $18.387529960$ in points and
$40.602986000$ on the lines, as the README, the manifests and the register state; no
point on a loaded line and none on an interior grid line, so under `zmx2`’s default rule
the cover has no atoms, as the $s(60)$ cover has none; the measure is invariant under
all eight elements of $D_4$, and the raw multisets under both generators; the `zmx2`
parser bounds hold with room (largest weight numerator $9{,}793{,}627$, total numerator
$5{,}899{,}051{,}596$, $\mathrm{lcm} = 20$). Its shape is the $s(60)$ cover’s shape at
the same side, with 2,564 more points and 24 more segments.
Exact masses at a few poses (`mass.py`, closed squares): the tile germ $(3/2, 3/2)$
captures $1.822524230$ at $\theta = 0$ and $1.061323343$ at $u = 10^{-5}$; the corner
tile $(1/2, 1/2)$ captures $1.009500880$ at $\theta = 0$; at the corner $(7/5, 13/10)$,
$u = 9/32$ of the root $R$ below, $1.011195020$, and at $R$’s centre $1.095705437$. The
README puts the cover at about $0.09\,\%$ above `zmx2`’s exact threshold, so the margins
are of that order where the cover is tight.

### 7.2 The `zmx2` sweeps, as reported

`zmx2 cert COVER --d4`: 6,400 roots, 9,844,124 boxes, 0 uncertified, `VERIFIED-D4`, 243
CPU-s; `--full`: 51,200 roots, 79,108,328 boxes, 0 uncertified, `VERIFIED`, 1,944 CPU-s
(README table).
The runs’ logs are pinned in `SHA256SUMS` (`zmx2_d4/run.log` `672bdd1e…`,
`zmx2_full/run.log` `d4ae699b…`) and absent; no `zmx2` manifest, binary hash or compiler
version is published for either cover.
The counts are consistent with Daniel’s $s(60)$ runs on the same geometry (2,617,534 and
21,036,120 boxes): a cover $0.09\,\%$ above threshold needs about four times the boxes
of one $0.77\,\%$ above.
The region, the root grids and the verdict logic are those of §3.4 and §4; `verify.sh`
asserts, from the per-root log, exactly 6,400 and 51,200 distinct roots, each with
`uncert 0` and `capped 0`.

### 7.3 Is the two-run `zm_mixed.py` composite a proof?

The two manifests are consistent with each other and with the cover: both record the
input SHA-256 `6f4d2b64…`, the three checker hashes of the pin, the total
`1474762899/25000000`, and the settings `D4, depth, pitch 1/20, ubins 16, chain from 0,
theta_bias 4, clip, lemma_T, lemma_L, split, cert_mode, tprime false,
split_maxchain 400, reach 442/625`, the only differences being the depth limit (24, 34)
and the region (none; `cx [27/20, 7/5], cy [13/10, 27/20], u [1/4, 9/32]`). The complete
sweep: 102,400 roots, 1,514,784 boxes, max depth 24, leaves ADM 346,399 / CHAIN 217,278
/ SPLIT 206,137 / PIECE 8,470 / EMPTY 30,302 / UNCERT 6, `TPTS 0`, 455,030 CPU-s,
verdict `NOT VERIFIED`. The region run: 1 root, 13,767 boxes, max depth 26, ADM 4,207 /
CHAIN 426 / SPLIT 2,251 / EMPTY 0 / UNCERT 0, 3,259 CPU-s, verdict
`VERIFIED-D4 (PARTIAL)`. Both censuses satisfy the binary-tree identity
$\text{boxes} - \text{leaves} = \text{leaves} - \text{roots}$ (706,192 and 6,883), so
every recorded internal node has two children.

The logic is sound. The root filter of `main` keeps a root iff it overlaps the region
with positive width, so with pitch $1/20$ and bins of $1/32$ the region
$[27/20, 7/5] \times [13/10, 27/20] \times [1/4, 9/32]$ selects exactly the root
$R = [27/20, 28/20] \times [26/20, 27/20] \times [8/32, 9/32]$ and sweeps it whole, at
the same settings and a deeper limit; the depth-24 sweep certifies every root in which
it left no uncertified box.
If the six boxes lie in $R$, the two runs together certify all 102,400 closed roots,
which tile the $D_4$ region, and the composite is a proof of the checker statement at
the same standing as a single `VERIFIED-D4` run.

Whether they lie in $R$ is not decidable from the published tree.
The manifest records only `uncertified: 6`; the boxes’ coordinates are printed in
`zm_mixed_d4/run.log` (pinned `d7fb69fd…`, absent) and recorded per root in
`roots.jsonl` (pinned `279b928e…` in the manifest, absent).
The README asserts it, and `verify.sh --zm` checks it on a *fresh* depth-24 run, by
parsing the rounded six-decimal print of the box list (a box of a neighbouring root with
an edge on $x = 7/5$ would print `1.400000` and pass its `x1 <= 1.4` test; the per-root
`unc` lists would be the right thing to check).
The region manifest was created at 08:50:20 and the complete one at 17:25:28 on
2026-10-01: the deep run finished before the sweep’s manifest was written, so it was
launched from the sweep’s partial records, which are appended root by root; that is
consistent, and it means the sweep’s own records are the only thing that ties the two.
**As published, the exact-rational route is a reported composite whose premise rests on
the README.** It becomes a proof the moment the records are published and match their
pinned digests, or when a replay regenerates them.

### 7.4 The zero-width angle bin

Daniel’s commit `6717ff895a50924f923e592cf8471343bf26ef27` (2026-09-29T20:28:51−06:00,
2026-09-30T02:28:51Z, a day after the pin) adds one line to `region_phi`:
`if u0 >= u1: return None`, with the comment “zero-width bin: no sub-bin is examined, so
‘EMPTY’ would be unproved (audit B1)”; `37b2ac2` re-pins `zm_mixed.py` to `1fd20346…`
for the $s(21)$, $s(45)$ and $s(60)$ bundles and reports censuses identical root for
root. The defect it guards: `region_phi` enumerates sub-bins between the points
`[u0, u1] ∪ (corner-choice breakpoints)`; with $u_0 = u_1$ the list has one point, the
loop over sub-bins does not run, and the function returns `'EMPTY'`, which `cert_split`
takes as a proof that the region holds no admissible pose and skips it, and
`vertex_split` as permission to drop a term.
A zero-width box reaching it would be a false acceptance.
The pinned `ee3e2915…` lacks the guard.

It cannot be reached in these sweeps.
Boxes are halved at exact midpoints, so every box of a root has $u_1 > u_0$ unless
`clip_bin` sets $u_1 := u_0$. `clip_bin` returns $u_0$ in two places only
(`zeromargin.py` lines 90–91): when $w(u_0) > K$, with
$K = 2\min(c_{x1}, m - c_{x0}, c_{y1}, m - c_{y0})$, and when $w(u_0) = K$. In the first
case `run_box` finds $w_{lo}/2 = w(u_0)/2 > \min(\cdot)$ and marks the box `EMPTY`
before any primitive runs.
The second case is impossible for $u_0 > 0$: with $u_0 = n/2^b$ in lowest terms,
$b \ge 2$ since $u_0 < \tfrac12$, $w(u_0) = (2^{2b} + 2n2^b - n^2)/(2^{2b} + n^2)$ is in
lowest terms (the numerator and the odd denominator are coprime, as
$\gcd(2^{2b} + n^2, n) = \gcd(2^{2b} + n^2, n - 2^b) = 1$), while $K$ is
$k/(10 \cdot 2^j)$ because every centre coordinate is $k'/(20 \cdot 2^j)$ and $m$ is an
integer; equality would force the odd number $2^{2b} + n^2$ to divide $10 \cdot 2^j$,
hence to divide 5, impossible for $b \ge 2$. The same arithmetic shows that no bisection
midpoint `lo` satisfies $w(\text{lo}) = K$, so the bisection always returns `hi`
$> u_0$. For $u_0 = 0$, `cert_split` and `vertex_split` both return before calling
`region_phi`. Hence every box that reaches `region_phi` in a `--d4` sweep at pitch
$1/20$ and sixteen bins has $u_1 > u_0$, and the guard is dead code there.
Daniel’s comment on issue 279 says the same from the bisection alone; the `clip_bin`
branches are where a zero width could arise and they are covered above.

### 7.5 Does `zmx2` alone suffice?

As this record’s rung rules read: yes.
`V3` needs interval-certified evidence with a certificate, a replay command and a
passing replay; `C3` needs the same with a confirming origin and a control; two machine
methods are an attribute shown beside the rung, not a rung
([`epistemics.md`](../../../epistemics.md#confirmation)); and the runbook says one
complete replay is what `C3` needs, a second route being recorded beside it.
`T-052` and `T-053` stand at `V3/C3` on exactly that: a complete `zmx2` replay with
`zm_mixed.py` sampled.
The `--full` sweep decides the unfolded statement with no symmetry hypothesis and is the
one to replay; `--d4` is a cheap second control.
Mathematically what one then trusts is §4: the paper lemmas and the IEEE-754 model.

## 8. The $s(77)$ Certificate (D, `T-067`)

### 8.1 The cover, checked here

Header `mixed 1`, $s = 9$, $D = 1000$, $W = 2^{49}$; 28,273 points and 6,420 segments;
total $43347137744028965/2^{49} = 76.999984600031\ldots$ exactly ($26.575814537$ in
points, $50.424170063$ on the lines); every piece in $[0,9]^2$, no zero or negative
weight, no repeated point or segment geometry; lines $x, y \in \{1, \dots, 8\}$. Segment
lengths: 5,952 of $1/50$, 368 of $1/8$ and 100 of $2/1000$, so $\mathrm{lcm} = 500$
units. 632 pairs of consecutive segments on one line overlap with positive length.
No point lies on a loaded line or on an interior grid line.
The measure is invariant under all eight elements of $D_4$, and the raw entries are
invariant as multisets under both generators, which is what `zm_mixed.py --d4` demands.
The `zmx2` bounds hold: $W = 2^{49} < 2^{50}$, largest weight numerator
$62{,}184{,}450{,}026{,}366 < 2^{50}$, total numerator
$43{,}347{,}137{,}744{,}028{,}965 < 2^{56}$, $\mathrm{lcm} \le 2^{24}$.

The construction the README describes is corroborated where it can be: the $s(60)$ cover
has 736 segments on the cut lines $x = 4$ and $y = 4$, none crossing a cut in its
interior and no point on a cut line, and $5{,}216 + 736 = 5{,}952$ is the count of
$1/50$ segments here, as halving each cut-line segment onto two lines gives; the 100
short segments are $84 + 16$, the sixteen being points at line crossings split over two
lines; and the 1,047 points of this cover with both coordinates below $5/2$ coincide in
position with the 1,047 of the $s(60)$ cover there, with one weight ratio $1.009349$ to
within the rounding to $2^{-49}$. None of this is needed for the proof, which is about
the file as it is. Exact masses: the square $[1,2] \times [3,4]$ captures $1.679631546$
at $\theta = 0$ and $1.041693727$ at $u = 10^{-5}$ (the README’s pre-replacement dip sat
near here); the band tile $(7/2, 9/2)$ captures $1.500409642$ at $\theta = 0$ and
$1.011537727$ at $u = 10^{-5}$; the central tile $(9/2, 9/2)$, $1.446802952$ and
$1.011293246$ at $u = 10^{-3}$.

### 8.2 The shapes new to the checkers, lemma by lemma

The register’s `next_rung` asks whether either checker’s lemmas depend on the shape of
the reviewed covers.
The named worry, points on loaded lines, does not arise: there are none (§8.1), so
`zm_mixed.py`’s `CERT MODE` line will report `0 points on segment lines` and `zmx2`
makes no atoms by its default rule.
Four shapes are new, and I read each lemma they touch.

- **Segments shorter than the pitch, and of three lengths.** No lemma of either checker
  uses a pitch. `zm_mixed.py` keeps each line as a list of parameter intervals with a
  density; `LineMass` computes $G(y) = \sum_i d_i\,|[e_{0i}, e_{1i}] \cap (-\infty, y]|$
  from prefix sums over the sorted starts and the sorted ends separately, which is
  correct for pieces of any length; Lemma T’s candidate set is the union of all piece
  ends; `line_pieces` clips every piece to the window.
  `zmx2` merges each line’s endpoints into one breakpoint list and accumulates densities
  on it (`build_cover`), and the pair bound’s candidates are those breakpoints.
  The only length-dependent quantity is `zmx2`’s $L_c$, the lcm of the lengths in $1/D$
  units, $500$ here against $20$ before, which scales every mass integer; the sizes stay
  inside the bounds of §4 (the target $W L_c 2^{30} \approx 2^{88}$, $F$ values below
  $2^{95}$, atom weights below $2^{89}$).
- **Overlapping segments on one line.** `zmx2` adds densities on shared breakpoints and
  `canon` merges equal adjacent densities, so the $D_4$ check compares measures;
  `zm_mixed.py`’s `LineMass` formula is additive per piece and never looks up “the piece
  containing $y$”, `lcore` sums pieces, and its $D_4$ check compares raw multisets,
  which this file passes.
  Both are additive, as the measure is.
- **The weight unit $2^{-49}$.** `zeromargin.py` takes $W_{den} = \mathrm{lcm}$ of the
  reduced weight denominators, here $2^{49} = 5.6 \times 10^{14}$, below its $10^{15}$
  cap, so `CHAIN` is live (the manifest counts 181,324 `CHAIN` leaves), and its `int64`
  numerators sum to at most the total numerator $4.3 \times 10^{16}$, against
  $2^{63} = 9.2 \times 10^{18}$; the phantom’s numerator is at most the segment mass
  times $2^{49}$, far smaller.
  `zmx2`’s `i128` sizes are bounded by the parser as above; `Iv::rat`’s $2^{53}$
  assertion concerns box coordinates and $u$, not weights.
- **Point pairs at distance 1 off the grid.** The band measure’s points lie on a $1/8$
  lattice (1,451 of the 28,273 abscissae are multiples of $1/8$), so one-cut germs at
  $\theta \to 0^+$ exist whose decisive mass is a point pair on parallel lines at unit
  distance, which `zmx2` closes only when the points are atoms of lines Lemma Z couples:
  with `--pair-points`, 4,217 vertical and 4,217 horizontal partner lines carry 26,035
  and 2,094 atoms and 144 points stay ordinary.
  That is why the README’s runs carry the flag that issue 279 omits; §4 says why the
  flag cannot cause a false acceptance and what it can cost.
  Partner lines never sit at distance 1 from a wall (those positions are integers, hence
  grid lines), so Lemma W is applied to the same lines as without the flag.
  `zm_mixed.py` has no such mechanism and needs none: its point primitives are
  `zeromargin.py`’s chains, which closed the $s(32)$ point cover.

### 8.3 `--pair-points` and the `--full` sweep

The source reports `zmx2 cert COVER --full --pair-points`: 64,800 roots, 46,583,600
boxes, 0 uncertified, `VERIFIED`, 8,431 s wall on 16 threads; and `--d4 --pair-points`:
8,100 roots, 5,810,824 boxes, 0 uncertified, `VERIFIED-D4`, 1,102 s wall.
The `--full` pass reflects the cover by $y \mapsto s - y$ and rebuilds it through
`build_cover` with the flag still set, so the partner lines of the reflected cover are
its own. The atom-assignment asymmetry of `ZMX2.md` §12 would show as uncertified boxes
at rotated germ images, not as a false verdict; the source reports none, and the replay
will see whether that holds on the pinned source, which predates `--sym-atoms`.

### 8.4 $D_4$ invariance after cut and shift

The construction (cut at 4, far parts moved by 1, mass on a cut line split in halves
between $x = 4$ and $x = 5$, segments crossing a cut split in proportion to length, a
$D_4$-symmetric band measure added, 84 points moved onto short segments with a crossing
point split half and half) preserves invariance only if every step does, and the
splitting rules are exactly the ones that do.
Rather than trust that, I checked the result: the final measure is invariant under all
eight group elements, and the raw multisets under both generators (§8.1). `zmx2 d4` and
`zm_mixed.py --d4` will each re-check the two generators before sweeping and refuse
otherwise.

### 8.5 The `zm_mixed.py` sweep, as reported

`--d4 --cert-mode --disj --depth 24 --pitch 1/20 --ubins 16 --nproc 16`, the
`--chain-from` default being 0, which the manifest’s settings record as `chain_from 0`:
129,600 roots, 826,120 boxes, max depth 23, ADM 156,385 / CHAIN 181,324 / SPLIT 97,450 /
PIECE 9,032 / EMPTY 33,669 / UNCERT 0, `TPTS 0`, 337,745 CPU-s, 21,176 s wall,
`VERIFIED-D4`; the tree identity holds (348,260). The manifest’s input is `cover.txt`
with the retained SHA-256, so the run was on these bytes under a working name.
Its `run.log` (`f9ce073f…`) and records (`1480b48b…`) are absent.
By §7.4 the missing guard is dead code in this sweep too, and `TPTS 0` with no points on
lines means Corollary T′ is doubly absent.

## 9. The Corollaries

$s$ is nondecreasing: removing one square from a packing of $n + 1$ leaves a packing of
$n$ at the same side, so $s(n) \le s(n+1)$. Hence $s(60) \ge s(59) = 8$ and
$s(61) \ge 8$, and the $8 \times 8$ grid holds 60 and 61, so $s(60) = s(61) = 8$: second
routes to `T-062` and `T-063`, whose claims name them.
Likewise $s(78) \ge s(77) = 9 \ge s(78)$ by the $9 \times 9$ grid, which holds 78; and
$78 = 9^2 - 3$, so this is the $k = 9$ case of the family `T-064` reports, as its claim
and `T-067`’s say; $77 = 9^2 - 4$ and $59 = 8^2 - 5$ are the series the source names.
Under the runbook’s triage table a consequence another entry already registers gets no
entry and no scope change, and the older claim a sentence naming the newer route; that
is what the record does.
Note that the two routes to $s(78)$ are of different strength: `T-064`’s rests on one
checker and a Lean reduction conditional on `Valid7`; `T-067`’s rests on two checkers
and no Lean.

## 10. Findings

Severity is blocking or non-blocking, each with the claim it would block.

### F1. The exact-rational route for $s(59)$ is not reproducible from the tree (non-blocking for the claim; blocking for recording that route as evidence)

§7.3: the composite’s premise, that the six uncertified boxes of the complete depth-24
sweep lie in the root $R$, is published as prose; `zm_mixed_d4/run.log` and
`roots.jsonl` are pinned by digest and absent.
The claim does not depend on it, since `zmx2` decides the whole statement.
For the author: publish the two `roots.jsonl` files and the logs, or a listing of the
six boxes with their root, so that `sha256sum -c SHA256SUMS` passes and the premise is
checkable; and make `verify.sh --zm` test the premise from the per-root `unc` lists
rather than from the rounded print.

### F2. The published directories fail their own first step (non-blocking)

Both `SHA256SUMS` list run logs the repository’s `.gitignore` excludes (`*.log`), so
`verify.sh` under `set -eu` stops at `sha256sum -c` on a fresh checkout; the `zmx2` runs
have no published log, manifest, binary hash or compiler version.
Already in the evidence entries’ `limitations`. The replay here supplies what the source
does not.

### F3. Issue 279 and the README differ on `--pair-points` (non-blocking)

The issue describes both `zmx2` sweeps without the flag; the README and `verify.sh` run
both with it, and §8.2 explains why the flag is load-bearing for completeness.
The record should state the flag in `T-067`’s claim, as it does in `next_rung`; the
author should correct the issue.
A run without the flag that verifies would also be a proof (§4), so nothing turns on
which was meant.

### F4. “Independent” and “independently written” (non-blocking)

The $s(77)$ README calls its three sweeps independent and the $s(59)$ README its two
checkers independently written.
§6 is the precise statement: two implementations, two lemma families, two arithmetics,
one author, one architecture, one input.
The issues say so; the READMEs should.

### F5. The register’s stated worry for `T-067` is the wrong one (non-blocking)

`E-n077-wand125-mixed-cover-report` and `T-067`’s `next_rung` say the cover’s shape is
new because the reviewed covers have no point on a segment line.
This cover has none either (§8.1). What is new is listed in §8.2; the record should say
that instead when the exit rewrites the entry.

### F6. The zero-width guard (non-blocking, closed)

§7.4: unreachable in both runs.
Daniel’s reruns of `s21`, `s45` and `s60` at the guarded version matched root for root,
consistent with this.
No action.

### F7. A first-line working note in each cover (note)

Each file’s first comment line is a working note (`scaled by 2019/2000 from
lc_m8d_r1.txt`; `scratch variant: on-line points -> segments half-length 1/D (zmC
investigation)`), kept so that the hashes in the manifests match.
Comments are ignored by both parsers; the note on the $s(77)$ file names the replacement
step. No action.

## 11. What the Replay Lane Must Show

For either entry to move from `V0/C0` to `V3/C3`, per the runbook and
[`epistemics.md`](../../../epistemics.md#confirmation), the replay lane must retain, on
a branch the bead names:

- **The checker as pinned.** `zmx2` built from the retained `zmx2.rs` `6b7f0f79…` with
  the retained `Cargo.toml` and `Cargo.lock`, the compiler version and the binary hash
  recorded; the binary hash will not match the source’s (none is published), so the
  source hash and the census are the handle.
- **The data facts, independently.** The exact total ($< 59$, $< 77$) and the $D_4$
  invariance from a parser of this repository (the numbers in §7.1 and §8.1 are what it
  must find), and `zmx2 d4 COVER` printing `D4: measure invariant`.
- **One complete sweep per cover, logged per root.** For $s(59)$:
  `zmx2 cert COVER --full --threads T --log FULL.log` ending in a line
  `VERIFIED: every closed unit square in [0,s]^2 has mu >= 1 (unreduced sweep, all roots)`,
  with 51,200 distinct `ROOT` lines, each `uncert 0` and `capped 0`; `--d4` likewise
  with 6,400 roots and `VERIFIED-D4:`. For $s(77)$: the same with `--pair-points` on
  both, 64,800 and 8,100 roots; the log header must read `atoms=pairpts`. A box count
  equal to the README’s (79,108,328; 9,844,124; 46,583,600; 5,810,824) is the expected
  root-for-root agreement; a different count with a `VERIFIED` verdict is still a pass
  and is noted. No `--xlo`, `--bins` or other region option: `REGION CLEAN` is not a
  verdict.
- **Two mutated certificates refused by every checker that accepted the original**, held
  by a test: for instance every weight scaled by $99/100$ (D4 invariance kept), which
  must end `NOT VERIFIED` with uncertified boxes, and one segment’s mass zeroed on a
  tile germ (`ZMX2.md` test T5 is the model), which must be refused at $\theta \to 0^+$.
  For $s(59)$ the README’s bisection puts the threshold at $0.9991$ of the published
  weights, so $0.99$ is comfortably below it.
- **Receipts** with the commands, walls, CPU and output digests, and the `replay` field
  of a new `replayed-here` evidence entry written as
  `E-n021-evand-mixed-cover-zmx2-replay`’s is.

Not a condition of `C3`, and recorded beside it if run: `zm_mixed.py` on the root $R$ of
$s(59)$ at depth 34 (about one CPU-hour; expected `VERIFIED-D4 (PARTIAL)`, 13,767 boxes,
max depth 26), which reproduces the deep run but not the premise; the complete depth-24
sweep (126 CPU-hours) and the $s(77)$ sweep (94 CPU-hours), which would give each lower
half a second machine method and, for $s(59)$, settle F1 by regenerating the records.
`zm_mixed.py` forks a `multiprocessing` pool and must run under the project interpreter
with `numpy`, with `--nproc` and, if resumed, the same header.

## 12. Rung and Significance

**Rung.** Both entries stand at `V0/C0` as registered; this review is a qualifying read
and makes each `reviewed` (`C1`) once recorded as `external_review` on its reported
evidence entry. With the `zmx2` replay of §11 retained, each lower half becomes `V3/C3`
by the structural predicate, as `T-052` and `T-053` did, and the entries follow the
lower half. Rung 4 on either axis would need a second adversarial review by a distinct
reviewer and a human oversight record; rung 5 a Lean statement for each cover, which
neither has.

**Not machine-checked, numbered, as for $s(21)$ and $s(45)$:** (1) `zm_mixed.py`’s
lemmas and program and `mixed_cover.py`; (2) `zeromargin.py`’s program; (3) `zmx2`’s
lemmas, program and parser; (4) the IEEE-754 model of the host; (5) that the source’s
runs were produced by the pinned files on these bytes (hash-linked manifests for
`zm_mixed.py`, prose for `zmx2`; only a replay removes this); (6) for $s(59)$, the
premise of §7.3; (7) the total and the invariance (three parsers, no kernel); (8) the
reduction of §3.3 for these sides, which is the $m = 8$ and $m = 9$ case of lemmas
proved in Lean upstream for every $m$ and not built here.

**Significance, confirmed at `S3` for both.** `T-066`: an exact value for a case that
was open, by Daniel’s recipe applied one count lower, and a second route to two values
Daniel reported; a substantive case result, not a new technique or a family, so `S3`
beside `T-062` and below `T-052`, which introduced line mass.
`T-067`: an exact value for an open case and a second route to $s(78)$; the band
insertion that carries a side-8 cover to side 9 is the one new idea here, and if it
carries to $k = 10$ and $11$ as Daniel’s comment anticipates it would become a
technique; at one instance it is a substantive case result, `S3`.

**Credit.** The results are wand125’s, computer-assisted, built directly on Evan
Daniel’s method, format, checkers and $s(60)$ cover, as both READMEs say; the source
says parts of the work were produced with AI assistance under human direction.
The source claims no outside review.
Licence MIT.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
