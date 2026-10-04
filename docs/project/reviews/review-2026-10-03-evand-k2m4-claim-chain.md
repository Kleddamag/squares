# Claim-Chain Review: Evan Daniel’s `s(k² − 4) = k` for Every `k ≥ 5`

**Date:** 2026-10-03. **Lane:** the review lane of the W2 phase that is stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md) for issue
[316](https://github.com/jlevy/squares/issues/316), bead `think-4uir`; the entry is
provisionally `T-081`. **Reviewer:** Claude (AI review; model unstated), claim-chain
review lane of the 3 October import of #316, separately prompted.
This lane shared no context with the replay or registering lanes.

**In one line:** the chain from the box certificate to the claim holds as the source
states it. For every $k \ge 8$ it rests on one finite statement, `ValidTilt9`, and the
Lean hypothesis matches the run’s region.
That statement has one implementation and no full replay here yet.
I found no blocking defect.
Four non-blocking items are listed in §7, three of them about this record’s wording.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Claim | $s(k^2 - 4) = k$ for every integer $k \ge 5$ (Evan Daniel, evand/square-packing at `2eb15455a6f178213287a84ab4d0576c060baabe`) |
| Retained source | [`square-packing/s12/`](../../../packing/resources/web/evand-square-packing-2026-10-03/square-packing/s12/certificates/k2m4/README.md) of the 3 October evand packet; the run record at `record/run_k4x_k008_leaves.jsonl.gz` |
| Statement checked | `ValidTilt9`, the tilted part of `Valid9`: every closed unit square in $[0,9]^2$ has mass at least 1 under `K4_k008_box9.txt` (SHA-256 `4151d7c4…`) |
| Read | The k2m4 `README.md` and `verify.sh`; `K4_k008_family.txt`; `notes/lean-k2m4-reduction.md`, `notes/lean-valid-split.md`; `search/K2M4_MARGIN.md` §4; in Lean `ValidSplit9.lean` in full, `ValidSplit.lean` §1, `Bentz4.lean` §§1, 4, 5, `BentzFam.lean` `mass_shift`, `valid_of_box`, `minSide_eq`, `MixedMeasure.lean` `D4InvM`, `d4_reduction_measure`, and the definitions `coord`, `sq` (`Basic.lean`), `box` (`Chord.lean`), `Packs`, `minSide` (`S32.lean`); `qx2_zm.py`’s header and `lines_in_reach` |
| Run here | The fast `verify.sh` receipt ([`k2m4_verify_fast.log`](../../../packing/resources/web/evand-square-packing-2026-10-03/receipts/k2m4_verify_fast.log)), produced by the replay lane and read here; this lane’s own parser and checks (§6), run under the project interpreter |
| Precedent | `T-064` ($k^2 - 3$, `Valid7`) and its [method review](review-2026-10-02-valid7-independent-checker.md); the [1 October transfer review](review-2026-10-01-evand-mathematical-transfer.md) of `qx2_zm.py` |

## 2. The Claim, Split by `k`

The upper half is the $k \times k$ grid at every $k$. The lower half differs by $k$:

| `k` | `n` | Lower half | Held here as | Rung now |
| --- | --- | --- | --- | --- |
| 5 | 21 | The s21 mixed cover; `zmx2` and `zm_mixed.py`, which share point-test lineage; Lean reduction conditional on the checkers’ region statement | `T-052` | V3/C3; `zmx2` replayed in full here, `zm_mixed.py` only sampled; no retained review |
| 6 | 32 | The s32 point cover; `zeromargin.py` and `zmx2`; hypothesis-free Lean `s32_eq_6` at the source | `T-051` | V3/C3; both checkers replayed here; `s32_eq_6` not built here |
| 7 | 45 | The s45 mixed cover; `zm_mixed.py` and `zmx2`; **not in Lean** | `T-053`, second route `T-054` | V3/C3 each; `zmx2` replayed in full for both covers, `zm_mixed.py` only sampled; no retained review |
| ≥ 8 | 60, 77, 96, … | The family below, through `Valid9` | provisionally `T-081` | V0/C0 as drafted |

At $k = 7$ the source says “two separately written exact checkers”.
The record is narrower.
One of them, `zmx2`, has been replayed here in full, and it is the same checker that
decides `T-054`’s point cover.
So the two $k = 7$ routes have two covers but only one checker replayed here.
Second routes for the family’s own range are $k = 8$ by `T-062` and $k = 9$ by `T-067`;
wand125 published $s(77) = 9$ first.

Monotonicity gives $s(k^2 - 3) = k$ for $k \ge 5$: $s(k^2-3) \ge s(k^2-4) = k$, and the
grid gives the upper bound.
That overlaps `T-064` for $k \ge 6$, and at $k = 5$ it is Bentz’s $s(22) = 5$
(`E-bentz-2016-proof`). The new cases in the record’s range are $k = 10$ to $18$, that
is $n = 96, 117, \dots, 320$.

## 3. From Certificate to Claim

**The measure.** For $k \ge 7$, $\mu_k$ on $[0,k]^2$ has a corner module on $[0,3]^2$ in
each corner and a wall band of width $w = R = 3$ along each wall.
The band’s profile has period 1 along the wall.
Lebesgue measure fills $[14/5, k - 14/5]^2$, and all non-Lebesgue mass is on unit pieces
of the $1/5$-grid. Its total is $k^2 - 4D$ with $D = 214770225571/200000000000$. I
checked the accounting exactly from the coefficients the Lean note gives: segment mass
$(22400000000000\,m + 85489190977160)/(2\cdot10^{12})$ for $k = m + 7$, plus
$(k - 28/5)^2$, equals $k^2 - 4D$ for $m = 0$ to $11$. Since
$4D = 214770225571/50000000000 = 4.2954\ldots > 4$, the total is below $k^2 - 4$ for
every $k$. The kernel proves the same identity for every $m$ (`famCover_total4`).

**Dilation.** Suppose $k^2 - 4$ unit squares pack a square of side $s < k$. Scaling the
centres by $k/s$ gives that many squares of side $k/s > 1$ with disjoint interiors in
$[0,k]^2$, and the concentric closed unit squares are pairwise disjoint.
If each has mass at least 1, the total is at least $k^2 - 4 > k^2 - 4D$, a
contradiction. In Lean this is `not_packs_of_measure` inside `minSide_eq`. `Packs` asks
for closed squares inside `box s` with disjoint open interiors.

**Localisation to the 9 × 9 box.** `mass_shift` applies for $k \ge 2R + 2 = 8$ and maps
into $[0, 2R + 3]^2 = [0,9]^2$. Take a closed unit square and its axis-parallel bounding
interval $[x_0, x_1]$ on each axis, of width $w(\theta) \le \sqrt2 < 2$. Per axis the
shift is 0 if the square is near the low wall, $k - 9$ if it is near the high wall, and
otherwise $\lceil x_0\rceil - R - 1$, an integer.
In the third case $[x_0, x_1] \subset (R, k - R)$, where only the band’s phase matters.
Integer shifts keep the phase because the profile has period 1, and the Lebesgue edge
$14/5$ sits inside the band (the hypothesis $A \le 5R$, $14 \le 15$). So
$\mu_k(Q) = \mu_9(Q - v)$ exactly.
The bound $k \ge 8$ is what makes the three cases exhaustive when the square’s width is
below 2. At $k = 8$ the box is larger than the container, and the high-wall shift is
$-1$. I checked the period-1 property on the box file directly (§6).

**`Valid9` and its split.** `Valid9` says that every closed unit square in $[0,9]^2$, at
every centre and angle, has `box9Cover`-mass at least 1. `box9Cover` is the box file
verbatim, and `box9Cover_measure` identifies it with `famCover fam4 9` in the kernel.
`valid9_of_tilt_axis` reduces `Valid9` to two parts, using D4 invariance (`d4_box9`, a
kernel check of the packed weights).
The first part is `ValidAxis9`, Lemma Z: every axis-parallel square in the box.
It is **proved** in Lean (`validAxis9`, 6,400 corner limits over the whole box, 832
tight, no symmetry used).
The second part is `ValidTilt9`, which stays a hypothesis.
The Python Lemma Z run covers 1,600 corners on $[1/2, 9/2]^2$ with 208 tight.
It agrees with the kernel ($832 = 4 \cdot 208$) and is no longer load-bearing.

**What `ValidTilt9` says** (`ValidSplit.lean`, `ValidTilt 9 box9Cover.measure`). For
every $c \in [0, 9/2]^2$ (closed) and every real $u > 0$ with $u^2 + 2u \le 1$, if the
closed square `sq c (2 arctan u) 1` lies inside `box 9`, its mass is at least 1. In
other words: closed squares, centres in the closed quadrant, $0 < \theta \le 45°$ via
$\theta = 2\arctan u$, $u \le \sqrt2 - 1$, admissible squares only.
`exists_u_of_theta_pos` turns every $\theta \in (0, \pi/4]$ into such a $u$, and
`d4_reduction_measure` needs exactly the closed quadrant and $\theta \in [0, \pi/4]$.

**Does it match the run?** The record’s header argv is `--depth 18 --exact-umax 1/2
--exact-from 3 --dump-leaves` with no region restriction.
My own read of the record (§6) finds 16,200 distinct roots: centre cells of pitch $1/10$
covering $[0, 9/2]^2$ (lower ends $0 \dots 22/5$, upper ends $1/10 \dots 9/2$) and 8
bins of width $1/16$ over $u \in [0, 1/2]$. Since $u = 1/2$ is $\theta = 53.13°$, the
run covers more than $\theta \le 45°$. The extra range is cut off by `SYM` leaves, which
have $u_0 \ge \sqrt2 - 1$ on the whole leaf and lie outside `ValidTilt9`. `AXIS` leaves
have $u_1 = 0$ and also lie outside it, since Lemma Z decides them.
`EMPTY` leaves and the `clip_bin` slabs hold no admissible pose.
The $45°$ poses have irrational $u$, so they never fall in a `SYM` leaf.
The run’s region therefore contains `ValidTilt9`’s. The match itself is a reading of
`qx2_zm.py`; no machine check links its pose parametrisation to Lean’s `sq`. The
source’s note checks the rotation sign.
Even a slip there could not move the run off the domain: $\theta \mapsto -\theta$ with
$x \leftrightarrow y$ maps the closed quadrant to itself, and the cover’s diagonal
symmetry is kernel-checked.
That last step is mine and is not in Lean (§7, R-4).

## 4. Each Checker’s Trust Boundary

- **`qx2_zm.py`** (`6294052a…`, with `zm_mixed.py` `1fd20346…`, `zeromargin.py`
  `640fe453…`, `mixed_cover.py` `bb89de15…`) decides `ValidTilt9`. It works in exact
  `Fraction` arithmetic, and floats only choose which exact test to try.
  The one exception is `lines_in_reach`. It drops grid lines farther than
  $0.7072 + \tfrac12\,\mathrm{diag}(\text{box})$ from the box midpoint, about
  $9.3\cdot10^{-5}$ above the unit square’s circumradius $\sqrt2/2$. Dropping a line
  lowers a lower bound, because every mass here is positive, so the filter cannot
  certify a false leaf.
  Its leaf lemmas (S, T, L, R, U, K, E with E′ and E″) are proved on paper, not in Lean.
  The four files are **byte-identical** to the k2m3 checker.
  I compared SHA-256 against the 1 October packet’s `k2m3/qx2_zm/checker/`.
- **`qx2_records.py`** re-checks the record’s structure: header digests, argv, the root
  grid, labels, the census, and coverage (leaves plus slabs tile each root, total volume
  $81/8$ exact). It recomputes no leaf’s mass bound.
  It is the source’s own code.
- **Lean** (the kernel, standard axioms, no `sorry`, no `native_decide`, as the source
  reports) checks everything from `ValidTilt9` to `minSide (k^2 - 4) = k`: the family,
  the box identity, the accounting, localisation, dilation, D4 and Lemma Z. It does not
  prove `ValidTilt9`.

**What the k2m3 replay transfers.** `T-064`’s replay ran this exact code to completion
on `Valid7` and matched every root’s leaves.
That transfers the program’s determinism, its record format and its behaviour on a cover
of the same kind. It does not transfer correctness on box 9, which is a different cover
in three respects:

- $R = 3$ instead of 2;
- Lebesgue measure from $14/5$ instead of $9/5$;
- 16 unit segments listed twice, where the corner module meets the band’s end lines.

The source’s own `leaves` reviewer re-checked Lemma E’s hypotheses at box 9. Those
reviews are its own, and their reports are not retained (§5).

## 5. What Is and Is Not Established Now

1. **The fast `verify.sh` passed here** on the retained bytes, in 18 s with exit 0. It
   checked the hashes, the cover’s total and D4 invariance with the source’s own parser,
   that the family rebuilds the cover, the Lemma Z re-run, the record’s structure and
   coverage, and the Lean data regenerated byte for byte.
   This is a reproduction with the producer’s code, and it recomputes no tilted leaf.
2. **The full replay has not run here.** The source puts it at 815,343 CPU-s. Until it
   runs, `ValidTilt9` is the source’s report.
3. **The Lean build.** The Lean build’s result is recorded in the packet README. This
   review does not state it.
4. **`ValidTilt9` has a single implementation.** wand125’s independent checker is
   `T-064`’s `E-k2m3-wand125-valid7-independent`. It reads this format but was run on
   `Valid7` only, not on box 9. It would need a new run, and in this record that run
   would need its defect D-1 guarded.
   `zmx2` certified box 9 except 4,844 tiny-tilt boxes, so it is not a second route.
5. **The source’s three adversarial reviews** (break-it, leaves, claim) are its own.
   Per the README their reports are in private notes and were not retained.
   They count as `relation: source` at most.

**The route to an independent check.** This repository’s clean-room verifier
[`sqverify_fast`](../../../packing/sqverify_fast/README.md) decides only the
net-and-shrink families, not continuous-angle closed covers.
Its [Milestone C](../specs/active/plan-2026-10-03-measure-verifier-milestone-c.md) would
decide the closed claim exactly, with its own lemmas and enclosures, over the pose box
$(c_x, c_y, u)$. It would use a $D_4$ mode on $[0, s/2]^2 \times [0, \tfrac12]$ or a
full mode, and would not read the authors’ checker code.
For box 9 it needs two things the plan does not yet list:

- **A uniform-polygon primitive**, at least for an axis-parallel square of density 1.
  Milestone C covers formats D and P, which are points and segments only.
- **An exact argument inside the Lebesgue block**, where every square has mass exactly 1
  at every angle. A slack comparison cannot close those boxes.
  They need the analogue of Lemma U, and near the block’s edges a bound like Lemma K or
  E′.

The doubled segments are already handled, because admission merges line densities.
Its pair Lemma Z and Lemma H target the $\theta \to 0^+$ germs that left `zmx2` open.
Whether they close box 9’s germs is untested.

## 6. Spot Checks Made Here

Own parser and script, run under the project interpreter, reading only the box file and
the record:

- **Cover.** $s = 9$, coordinate denominator 5, $W = 2\cdot10^{12}$, no points, 2,076
  segments, every one an axis-parallel unit piece of the $1/5$-grid with $w > 0$, on 80
  lines. There is one polygon $[14/5, 31/5]^2$ with mass $289/25$ = its area.
- **Total.** $3835229774429/50000000000 = 81 - 4D$ exactly; $D > 1$.
- **D4.** The multiset of (segment, mass) is invariant under all eight maps of the
  square, which is stricter than invariance of the summed line density.
- **Doubled segments.** Exactly 16 pieces appear twice, none more often.
  They lie on the lines $x = 3$, $x = 6$, $y = 3$ and $y = 6$, which are the band’s end
  lines $R$ and $k - R$, at $[4/5, 6/5]$ and $[39/5, 41/5]$ along them, four per line.
  That matches “16 in layer 2” in the Lean data.
- **Period 1.** In the bottom band’s zone $x \in [3, 6]$, I compared 295 pairs of unit
  pieces one period apart: horizontal pieces on $y \in [0,3]$ and vertical pieces on
  interior lines. There were no mismatches.
- **Region.** The record has 16,200 roots, all distinct, with the grid given in §3,
  115,268 leaves and no uncertified boxes.
  $\theta(u = 1/2) = 53.13°$, and $u$ at $45°$ is $\sqrt2 - 1 = 0.41421$.
- **Code identity.** The four checker files are byte-identical to the k2m3 checker
  files.

## 7. Defects

None of these is blocking.
None touches the mathematics of the claim.

- **R-1. The draft `next_rung` overstates Milestone C (non-blocking; records).** It says
  an independent `ValidTilt9` check “would take” Milestone C. As planned, Milestone C
  stops at points and segments.
  The wording should add the polygon primitive and the exact Lebesgue-block argument of
  §5, or a slice should be added to the plan.
- **R-2. The draft omits `T-054` and the review gap at $k \le 7$ (non-blocking;
  records).** The draft claim and composition name only `T-053` for $k = 7$. `T-054` is
  a second route there, decided by the same `zmx2`. None of `T-052`, `T-053` and `T-054`
  carries a retained review.
  A reader of `T-081` should see that the $k = 5$ to $7$ cases stand at those entries’
  rungs.
- **R-3. A carried-over assumption overstates exactness (non-blocking; records).**
  `E-k2m3-evand-valid7-qx2-replay` assumes `qx2_zm.py` makes “no decision on a
  floating-point comparison”.
  The source itself names `lines_in_reach` as a float filter.
  It is conservative (§4), but the `ValidTilt9` replay entry should state it as it is,
  not copy the earlier wording.
- **R-4. The run-to-hypothesis match is not machine-linked (non-blocking; source).**
  Nothing formal ties `qx2_zm.py`’s $(c, u)$ boxes to `sq c (2 arctan u) 1`. The
  source’s note and §3 match them by reading, and they hold even if the sign convention
  were wrong. A formal tie would need the leaves themselves in Lean, which is the open
  step the source names.

## 8. Verdict and Significance

**Verdict: accepted.** The source states the chain correctly: $\mu_k$ and its
accounting, the dilation, localisation for $k \ge 8$, the D4 reduction, Lemma Z, and
`ValidTilt9` equal to the run’s region.
The hypothesis the Lean leaves open is no stronger than what the run claims.
$k = 5$ to $7$ rest on `T-052`, `T-051`, `T-053` and `T-054` as recorded.
This review moves no rung.
`V3/C3` at $k \ge 8$ needs the complete `qx2_zm.py` replay (same-implementation) and the
Lean build with its axiom receipt, both recorded here.

**Significance: S4, agreed.** This is a bound family: the deficit-4 case of Friedman’s
conjecture, giving nine new exact values in the record’s range and every later $k$ by
one finite certificate.
That is the same anchor as `T-064`. It is not S5, because no case it settles is central
to this project.

**For the records lane:** `kind: adversarial`; `reviewer`: Claude (AI review; model
unstated), claim-chain review lane of the 3 October import of #316, separately prompted;
`reviewer_kind: ai`; `relation: project`; `date: '2026-10-03'`; `scope`: the claim chain
from the box-9 certificate to $s(k^2-4) = k$, the Lean statement of `ValidTilt9` against
the run’s region, each checker’s trust boundary, and the per-$k$ split; `verdict:
accepted`; `covers: [T-081]` (provisional id).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
