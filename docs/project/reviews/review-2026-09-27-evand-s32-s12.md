# Proof Review: Evan Daniel’s `s(32) = 6`, `s(12) ≥ 15680/3951` and `s(21) ≥ 5000/1001`

Reviewed 2026-09-27 from a clone of `github.com/evand/square-packing` at
`167d842cd27ba1451cb2833773ea930c80b9e65b` (2026-09-26T19:42:14−06:00), read-only, by a
Fable max sub-agent acting as the mathematical reviewer.
This is an adversarial soundness review of one published computer-assisted exact value,
`s(32) = 6`, and of two lower bounds and one re-proof from the same repository, where
`s(n)` is the least side of a square containing `n` unit squares with disjoint
interiors, each freely rotated.
It is evidence for the coordinator, not a verdict of record: no result row was
registered and no bound was moved by writing it.

**In one line:** `s(32) = 6` rests on a weighted closed cover of `[0,6]²` of total
weight `31.7135 < 32`, checked exactly at the container itself by an exhaustive
subdivision of pose space, with the reduction, the symmetry fold and the cover’s data
facts proved in Lean 4 from one named computational hypothesis; the hypothesis is
exactly what the shipped checker run establishes, every acceptance in that checker is an
exact integer or rational test, and no mathematical defect was found.
The bound is at margin zero in the scale direction by necessity, not by accident, and
the argument handles that correctly: no limit or compactness step is needed.
The two lower bounds are positive-margin covers of the same family, exact and consistent
with the record, and each displaces a first-party rung.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `github.com/evand/square-packing`, directory `s12/` |
| Commit | `167d842cd27ba1451cb2833773ea930c80b9e65b`, `main`, 2026-09-26 |
| Claims | `s(32) = 6`; `s(12) ≥ 15680/3951 = 3.968615…`; `s(21) ≥ 5000/1001 = 4.995004…`; `s(13) = 4` without case analysis |
| `s(32)` cover | `certificates/s32/s32_closed_cover_6.txt`, `a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144` |
| second cover | `certificates/s32/s32_shift_v1.txt`, `7598d39a899adbdd2352d8054d98cb3e8818e4e4cd9c7a23830795a8f9847793` |
| `s(12)` cover | `certificates/s12_lower_3.9686.txt`, `75f1cc891a8b8739…` |
| `s(21)` cover | `certificates/s21/s21_lower_4.9950.txt`, `c8e8f878205f2da9…` |
| `s(13)` cover | `certificates/rung2/s13_closed_cover_4.txt`, `ea303acea08cc17a…` |
| Python checker | `search/zeromargin.py`, `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab`, byte-identical to the bundle’s frozen copy |

Files read line by line: `certificates/s32/README.md`, `certificates/FORMAT.md`,
`search/S32_EXACT.md`, `search/S32_SHIFT.md`, `search/RUNG2.md` §§3, 6 and 7,
`search/RUNG2_XCHECK.md` §§1 and 2, `search/S21_LB.md`, `notes/lean-s32.md`,
`notes/literature-s32.md`, `lean/Sqpack/{Basic,D4,Cover,S32}.lean` in full and the
statements of `ZeroMargin.lean`, `lean/Axioms.lean`, `lean/scripts/gen_s32_data.py`,
`search/zeromargin.py` in full (1,498 lines), the root loop, certificate loader,
`empty`, `check_d4` and exact-maximum routines of `verify2/src/main.rs`, the bundle’s
`SUMMARY.txt`, `manifest.json` and `roots.jsonl`, the three `zmcheck` sweep summaries,
`VERIFICATION.md`, the root and `s12/` READMEs and the rendered `docs/s32.html`. Lean
was not built here (no toolchain in the container); the Lean files were reviewed as text
against the source’s stated build and axiom report.

First-party context: `packing/frontier/n-012.md`, `n-013.md`, `n-021.md`, `n-032.md`,
[`epistemics.md`](../../../epistemics.md), the
[Kleddamag `4.640020` review](review-2026-09-27-n17-kleddamag-4640020.md) §8 for the
capacity-one ceiling lemma, and the
[Tokoharu density review](review-2026-09-22-tokoharu-density-mathematics.md).

Scratch instruments written for this review live outside the repository at
`/tmp/claude-0/review-evand/`: `static.py` (exact data checks), `poses.py` (exact
captures at chosen poses), `fscan.py` (a float scan), `mycheck.py` (an independent exact
box checker) and `rerun_zm.py` (a self-checking rerun of the source’s checker).
They share no code with the source.

## 2. Verdict

**(a) `s(32) = 6`: no mathematical defect found.** The theorem is stated in Lean as the
standard `s(32)`; the reduction from a closed cover of `[0,6]²` to “no packing at any
side below 6” is proved in Lean; the D4 fold and the cover’s total and symmetry are
kernel-checked; and the one hypothesis left to computation is, term for term, the
statement the shipped `zeromargin.py` run certifies over its 7,200 closed root boxes.
The checker’s primitives are sound and their float pre-screens can only lose
certifications.
The findings below are about presentation and reproducibility, none about
the mathematics.

**(b) `s(12) ≥ 15680/3951` and (c) `s(21) ≥ 5000/1001`: sound as stated.** Both are
positive-margin closed covers checked by the source’s angle-net verifier and its Python
re-implementation; the rational bound in each header is exactly what the verifier
certifies, with `≥` rather than `>` because the squares are closed.
Both displace a first-party rung (`99/25` at n = 12, `122/25` at n = 21).

**(d) `s(13) = 4` without case analysis: sound.** It is the same architecture as (a) at
`m = 4`, with both checkers run over the whole pose domain.
The theorem is Bentz’s; the proof is new.

## 3. The `s(32)` Theorem and Its Architecture

### 3.1 Statement

Lean (`S32.lean`): `Packs n s` is the existence of `n` centres and angles with each
closed unit square `sq c θ 1 ⊆ box s = [0,s]²` and pairwise disjoint open interiors;
`minSide n = sInf {s | Packs n s}`. The theorem proved is

```lean
theorem s32_eq_six_of_checker (h : S32CheckerCover) : minSide 32 = 6
```

via `s32_isLeast : IsLeast {s | Packs 32 s} 6`, so the infimum is attained.
`Packs 32 6` is the `6 × 6` grid (`packs_grid`, no hypothesis).
This is the standard definition of `s(n)`: closed squares, boundary contact allowed, any
orientation.

### 3.2 The reduction, and why margin zero is not a gap

The cover is a finite weighted point set `(A, w)` in `[0,6]²`, `w ≥ 0`, with the **cover
property**: every closed unit square `Q ⊆ [0,6]²`, at every centre and angle, contains
points of total weight at least 1. Its total is `31.713505… < 32`.

`not_packs_of_cover` (Lean): if 32 unit squares pack in `[0,s]²` with `s < 6`, scale by
`μ = 6/s > 1`. The images are squares of side `μ` inside `[0,6]²` with disjoint
interiors. Each strictly contains its concentric closed unit square
(`unit_subset_interior`), so those 32 closed unit squares are pairwise disjoint, not
merely interior-disjoint, and no cover point lies in two of them.
Each captures weight `≥ 1` by the cover property, so `32 ≤ Σ w < 32`. Hence
`¬ Packs 32 s` for every `s < 6`, and with `Packs 32 6` the set of feasible sides is
`[6, ∞)`, whose least element is 6.

This is the crux the review was asked to check, and it is right.
The cover is stated at the closed container `[0,6]²` for closed unit squares, and the
scaling step converts *every* `s < 6` at once; there is no `δ`, no sequence of
certificates and no compactness argument to get wrong.
What “margin zero” means here is different from a pointwise margin: the least captured
weight over admissible poses is positive (about `1.0109`, §4), but the cover has no
slack in the *scale* direction.
Any concentric shrink of the squares, equivalently any container side `6 + ε`, loses the
weight on the grid lines, which is where 77 % of the mass sits and which the 36 tiles
share. That is forced: `RUNG2.md` Theorem 1 shows that a subdivision certified by fixed
witness sets must total at least `m² = 36`, and, as `notes/literature-s32.md` observes,
an absolutely continuous density cannot certify an integer side at all, since the `k²`
grid tiles would partition its mass; that is why the rectangle-density certificates of
the [Tokoharu review](review-2026-09-22-tokoharu-density-mathematics.md) stop strictly
below the grid. So the usual angle-net verifier with `σ_k`-shrunk squares cannot be
applied, and the check has to be an exact subdivision of pose space with a disjunctive
primitive.

### 3.3 The D4 reduction

`D4.lean` proves `d4_reduction`: if `(A, w)` is invariant under `x ↦ m − x` and `x ↔ y`
(`D4Inv`, the two generators) and every admissible closed unit square with centre in
`[0, m/2]²` and `θ ∈ [0, π/4]` captures `≥ 1`, then every admissible closed unit square
in `[0,m]²` does. The proof reduces `θ` modulo `π/2` (the axis square is fixed by the
quarter turn), reflects across `x ↦ m − x` when `θ > π/4` (sending `θ ↦ −θ ≡ π/2 − θ`),
and applies the quarter turn `reflX ∘ swapXY`, which keeps `θ`, to bring the centre into
the closed quadrant; each move preserves admissibility (`sq_subset_box_reflX_iff`,
`sq_subset_box_swapXY_iff`) and captured weight (`capt_reflX`, `capt_swapXY`,
`capt_add_pi_div_two`). `d4_reduction_u` restates the region as `θ = 2 arctan u`,
`u ∈ [0, ½]`, which contains `[0°, 45°]` since `tan 22.5° = √2 − 1 < ½`
(`exists_u_of_theta`). The invariance of the actual data is `S32Data.d4Inv`, derived
from `check_ok` by kernel evaluation; both generators were also re-checked here for all
eight group elements on the aggregated weight map (§4).

### 3.4 The one hypothesis, and what discharges it

```lean
def S32CheckerCover : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 3 → c.2 ∈ Set.Icc 0 3 →
    u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box 6 →
      1 ≤ ∑ e ∈ entries.filter (fun e => pt e ∈ sq c (2 * Real.arctan u) 1), wt e
```

with `entries` the 13,085 integer triples of the certificate (no repeated key, by
`check_ok`), `pt e = (x/1000, y/1000)` and `wt e = w/10¹¹`. Term by term against
`zeromargin.py --d4`:

| Hypothesis | Checker |
| --- | --- |
| `c ∈ [0,3]²`, `u ∈ [0,½]` | `d4_roots`: 30 × 30 centre cells of pitch `1/10` times 8 bins of width `1/16`; the union of the 7,200 *closed* root boxes is exactly `[0,3]² × [0,½]` |
| `sq c θ 1 ⊆ box 6` | admissible: `w(θ)/2 ≤ c_x, c_y ≤ 6 − w(θ)/2`, `w = cos θ + sin θ`; inadmissible poses are exempt in both (`sq_subset_box_iff`) |
| `pt e ∈ sq c θ 1`, closed | every containment test is a non-strict inequality: `in_core` uses `−½ ≤ x ≤ ½`, the violation polynomials `G ≤ 0`, Lemma A’s `≤ ½` |
| `1 ≤ Σ wt e` | a leaf is `EMPTY` (no admissible pose, decided exactly) or carries points proved captured at every admissible pose of the leaf with weight `≥ 1`, compared as integers over `W` |
| sum over `entries` | duplicates would add in Lean (`coverW`) and in the checker; the file has none |

The run (`certificates/s32/zeromargin_d4/`): 7,200 roots, 164,130 boxes, max depth 27,
leaves ADM 12,201 / CHAIN 70,007 / EMPTY 3,457 / UNCERTIFIED 0, 2.77 CPU-hours, on
checker `640fe453…` and certificate `a0d2d38f…`; 7,199 roots at depth limit 24 and one
root, `x ∈ [1.5,1.6], y ∈ [0.5,0.6], u ∈ [0,1/16]`, by a second complete run at depth 30
(139 boxes, max depth 27). The bundle’s `roots.jsonl` holds 7,201 records for 7,200
roots; the totals in `SUMMARY.txt` are the census of the record shown per root, and the
raw totals over all 7,201 records (ADM 12,209, CHAIN 70,058, EMPTY 3,464, UNCERT 1)
differ by exactly the superseded depth-24 record, as they should.

### 3.5 The checker’s primitives and their soundness

`zeromargin.py` subdivides each root box `[cx₀,cx₁] × [cy₀,cy₁] × [u₀,u₁]` and certifies
a leaf by one of:

- **EMPTY.** `cx₁ < w_lo/2` or `cx₀ > m − w_lo/2` (or in `y`), `w_lo` the least `w` on
  the bin. `w(u) = (1 + 2u − u²)/(1 + u²)` is unimodal with its maximum at 45°, so the
  least value is at an endpoint and the test is exact.
- **clip_bin.** Shrinks a bin to `[u₀, u*]` with `u* ≥ u⁻`, the largest angle at which
  the box still holds an admissible pose; bins reaching past 45° are left alone.
  Lean `clip_bin_no_loss` shows no admissible pose is dropped.
- **ADM** (Lemmas A–C, Lean `lemmaA`, `polyOk_quad`, `polyOk_bern`). A point is a
  witness when its four containment inequalities hold at the four extreme admissible
  corners for every angle of the bin, each a polynomial of degree at most 4 in `u`,
  decided exactly (quadratic: endpoints and interior vertex; quartic: Bernstein upper
  bound, sound). The wall bounds `c ≥ w/2` and `c ≤ m − w/2` are offered as alternatives
  to the box sides, each separately sound.
- **P1**, the `2 × 2` box lemma, and **MIX**, the union of ADM and P1 witnesses.
- **CHAIN** (Lemmas E–H, Lean `gsum_le_gmax`, `lemmaG_box`, `lemmaH_box`,
  `chain_regions_cover`). A *swing* point fails exactly one of its four inequalities on
  the box; a monotone chain `G_{q₁} ≤ … ≤ G_{q_k}` of swing polynomials of one kind
  partitions the box into `k + 1` regions; on region `r` the chain members up to `q_r`,
  every point with `G_p ≤ G_{q_r}` (the suffix down-set), and every point with
  `G_p + λ G_{q_{r+1}} ≤ 0` for some `λ ∈ {1, ½, 2}` (Lemma G) are captured; two chains
  of different kinds are multiplied for interior tile germs and Lemma H discharges empty
  product regions. Every `max` over a box is exact because each combination is affine in
  the centre and quadratic in `u` (Lemma E).

The fast path (`cert_chain_fast`, `_adm_cond_ok_int`) was traced acceptance by
acceptance. Chain links are appended only after `_gle0`, an exact integer test; every
binary search over a chain is float-steered but its final accepted probe is re-decided
exactly (`fconfirm`), and a failed confirmation redoes the row all-exact (`fmismatch`,
zero in the shipped run and in the reruns here); region weights are `int64` sums of
integer numerators whose total is `3.2 × 10¹²`; the transitivity steps rest on exactly
accepted links.
A float can reject a good pair or stop a search early, never accept a bad
one. The numpy pre-screens in `cert_adm` and `cert_chain` are lenient supersets by
construction (`tol = 10⁻⁹`), and the subtree cache `inh` is sound because a child box is
a subset of its parent after clipping.
The reach filter uses `0.7072 > √2/2`.

The Lean file `ZeroMargin.lean` formalises Lemma A, the quadratic maximum, the Bernstein
bound, Lemmas E–H, the chain partition and `clip_bin`; the D4 file adds the fold.
What is *not* in Lean, as the source says plainly: the subdivision, bookkeeping and
parsing of either program.

### 3.6 The second checker and the partial run

`verify2/zmcheck` (Rust, `i128`) is a separately designed checker: one polynomial class
(affine in the centre, degree at most 4 in `u`), one exact-maximum routine in a local
parameter with an explicit overflow refusal (`4 d_u + d_xy > 74`), one inference rule
(Lemma I: nonnegative multipliers on hypotheses), with admissibility carried as
hypotheses and the disjunction as recursive sign splitting rather than chains.
It shares no code with the Python checker.
On the Lean-transcribed cover its D4 sweep certified 3,595 of 3,600 roots; the 5 open
roots (52 boxes at depth 22, all at interior tile germs `(1.5,1.5)`, `(1.5,2.5)`,
`(2.5,1.5)` with `u ≤ 1/8`) were closed by `zeromargin.py`, which also covers them in
its full run. On the second cover `s32_shift_v1.txt` both checkers certify every root.

Two things follow.
The theorem needs only one complete exact checker plus the Lean chain,
and it has that twice over (either cover suffices).
But the sentence “certified at margin zero by two independently written exact checkers”
is true of the theorem through the *second* cover, and true of the Lean-transcribed
cover only up to five roots (F1).

## 4. Evidence

Independent checks run here, sharing no code with the source, exact unless marked:

- **Data** (`static.py`, under a second).
  All six certificates parse to their stated counts with no repeated point, all points
  inside the closed container, all weights nonnegative, and totals
  `3171350535386/10¹¹ = 31.713505354` (`s32`), `31.697940049` (`shift_v1`),
  `2591194431/200000000 = 12.955972155` (`s13`), `29934509/2500000 = 11.9738036`
  (`s12`), `260057/12500 = 20.80456` (`s21`), each below its `n`; every one is invariant
  under all eight elements of the container’s dihedral group on the aggregated weight
  map. `gen_s32_data.py --check` reproduces `S32Data.lean` byte for byte; all
  `SHA256SUMS` in `certificates/s32/` and `certificates/s21/` match.
- **Critical poses** (`poses.py`, exact rationals).
  At the nine tile centres of the fundamental region with `θ = 0` the cover captures
  `1.010904751` (corner tile `(½,½)`), `1.512466729` (edge tiles), `1.481319889`,
  `1.834572020` (`(1.5,1.5)`), `1.752258375`, `1.700452075`; at the twelve corners of
  `zmcheck`’s open germ box `x ∈ [1.49922,1.5], y ∈ [2.49922,2.5], u ∈ [0,1/2048]`
  between `1.019862943` and `1.752258375`; at wall-tight poses `c_y = w(θ)/2` with
  `c_x = 1.5013` (the depth-30 root) at least `1.011952650`; at tilted poses up to
  `u = ½` (53.13°) at least `1.109`. Every admissible pose sampled captures `≥ 1`; the
  least, `1.010904751` at the corner tile, equals the float scan’s global minimum.
- **Float scan** (`fscan.py`, heuristic, 300,000 poses per cover in five families:
  uniform, tile germs, wall-tight, corner-tight, half-integer lines with tilt below
  0.6°). Least capture `1.010904751` (`s32`), `1.004229479` (`shift_v1`, near
  `(0.505, 2.499, 0.09°)`), `1.027914195` (`s13`), `1.0000056` (`s12`), `1.0010177`
  (`s21`). The `s12` value is the signature of a certificate scaled to its critical
  container; the `s21` value exceeds the verifier’s own net minimum `1.0000083`, as it
  must, since the verifier tests shrunk squares.
- **Independent box checker** (`mycheck.py`, exact integers).
  A monotone-witness checker written from the definition: centre rectangle clipped to
  the admissible range at the bin’s least `w`, the four containment inequalities at the
  four corners as quadratics in `u` with integer coefficients, endpoints and vertex
  exact, no wall polynomials and no disjunction.
  On 57 sampled D4 roots (30 that the source closes in one box, 10 that it closes
  without CHAIN, 12 that it closes with CHAIN, and 5 chosen germ and wall roots) it
  certifies 49 at depth 14 in 37,269 boxes and 276 s; the 8 it leaves open are exactly
  the sets the theory says a fixed-witness checker cannot close: the interior germ
  `(1.5,1.5)`, the wall germ `(1.5,0.5)`, the corner-wall sliver `x ∈ [0.4,0.5]`, and
  three sliding-cut boxes on grid lines.
  Of the source’s 33 CHAIN roots in the sample this checker still closes 26 by
  subdividing further.
- **Reproducibility of the shipped run** (`rerun_zm.py`, the bundle’s frozen checker in
  `--selfcheck` mode, which evaluates the Fraction reference beside the fast path at
  every CHAIN call and ADM condition test).
  The depth-30 root at depth 24 (133 boxes, 1 uncertified) and at depth 30 (139 boxes, 0
  uncertified) reproduce the two shipped records exactly; 118 and 123 CHAIN calls
  self-checked, 39,799 and 40,567 exact pair tests, `fmismatch = 0`. Further roots: see
  the table.
- **`zmcheck` built from HEAD** (sha256 `833a23ce…`, not one of the three binaries the
  sweep summaries record): see the table.

| Obligation | Result here |
| --- | --- |
| Certificate and checker identities | all hashes confirmed; Lean data equals the certificate |
| Totals, D4 invariance, well-formedness | re-derived, all six files |
| Lean statement matches `s(32)` and the checker’s conventions | confirmed by reading (§3) |
| Closed-square convention throughout | confirmed in both checkers and in `sq` |
| Exactness of every fast-path acceptance | confirmed by reading; `fmismatch = 0` in reruns |
| Angles above 45° | `clip_bin` declines to clip; `w_hi = 14143/10000 > √2` when the bin holds 45°; Lemma A needs only `cos, sin ≥ 0`; sound |
| Shipped censuses reproduce | the depth-30 root at both depth limits, box for box and leaf for leaf, under `--selfcheck`; a self-checked rerun of an interior germ root did not finish inside the 15 min allowed (the Fraction reference is about 100× slower than the fast path), so the germ censuses rest on the source’s own `--selfcheck` and `--ref` regressions |
| `zmcheck` at HEAD on the candidate’s sanity cells and on the `s(13)` cover | cells `(24–25, 4–5)` of the D4 region, 16 roots, one thread, 69 s: 342 boxes, max depth 11, ADM 50 / DISJ 88 / EMPTY 41 / 0 uncertified, the census the source records for the same cells; the D4 invariance check passes; `zmcheck pose` agrees with `poses.py` to all eleven digits at two poses; `s(13)` cells `(14–15, 4–5)`: 90 boxes, 0 uncertified |
| `s(12)` certificate under the source’s verifier at `N = 6000` | built from HEAD, one thread, 5 min 11 s: `VERIFIED`, least covered weight `10000056/10⁷` at bin `k = 0`, equal to the source’s recorded minimum and to the float scan’s `1.0000056` |

## 5. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. The two-checker claim is exact for the second cover, five roots short for the Lean-transcribed one (non-blocking)

`certificates/s32/README.md` and the site say the cover is “certified at margin zero by
two independently written exact checkers”.
For `s32_closed_cover_6.txt`, the file transcribed into `S32Data.lean`, `zmcheck`
certifies 3,595 of 3,600 roots and `zeromargin.py` supplies the other five, so those
five roots have one exact checker.
For `s32_shift_v1.txt` both checkers are complete, but that cover is not the one in
Lean. The source states both facts in its own table.
A record entry should say: the theorem has two complete exact certifications (one per
cover), and the Lean-linked cover has one complete certification plus a 99.86 % second.

### F2. The `zmcheck` run records are tied to binaries, not to source commits (note)

`zmcheck_d4/binaries_*.txt` names three binaries by sha256 (`67e760bf`, `2043cff8`,
`4fc06e86`), described in prose as the pre-§9 build, the §9 build and the §9 build with
`ZM_MIXPAIR`. None is shipped, and a build from HEAD here hashes differently, as Rust
builds do across toolchains.
The `zmcheck` half of the evidence is therefore reproducible only by rerunning (80
CPU-hours for the candidate; 6 for the second cover), not by matching a hash.
The `zeromargin.py` half is pinned: the checker that ran is in the bundle and equals
`search/zeromargin.py` at HEAD.

### F3. P1 is a corollary, not a named Lean lemma (note)

`zeromargin.py`’s P1 primitive (`|c − p|_∞ ≤ 1 − w_hi/2 ⇒ p ∈ Q`, wall sides exempt)
produced no leaf in the `s(32)` run but feeds the witness set `T` of every CHAIN leaf.
It is not a theorem of `ZeroMargin.lean`; `notes/lean-zeromargin.md` treats it as a case
of Lemma A. Checked here: with `t = 1 − w_hi/2 ≤ 1 − w(θ)/2`, condition (i) of Lemma A
reads `(p_x − A_x) cos θ + (p_y − A_y) sin θ ≤ t·w(θ) = w − w²/2 ≤ ½` since
`(w − 1)² ≥ 0`, and a wall-exempt side has `p_x − A_x ≤ 1 − w/2` because `A_x ≥ w/2`. So
P1 is a corollary of `lemmaA`; the source’s “every primitive both checkers rest on” is
right in substance, and a one-line Lean lemma would close the gap between the sentence
and the file.

### F4. `int64` region sums have no guard (note)

CHAIN’s region weights are `int64` sums of numerators over `W = 10¹¹`; the total is
`3.17 × 10¹²`, far below `2⁶³`, and `Wden` is set to 0 (disabling CHAIN) if the common
denominator exceeds `10¹⁵`. The source’s pre-publication review lists a guard on
`Σ W·weight` as a should-fix; it does not affect this certificate.

### F5. The novelty statement is consistent with the record (note)

“First exact value of `s(k² − 4)` for `k ≥ 4`” agrees with this repository’s case files:
n = 12, 21, 32 and 45 are all open here, Bentz’s exact values are the `k² − 3` family,
and `s(5) = 2 + 1/√2` (Göbel 1979) is the `k = 3` member, where the grid loses.
The reference to Friedman is to DS7’s Conjecture 1, “if `s(n² − k) = n` then
`s((n+1)² − k) = n + 1`” (retained DS7, line 139), read correctly as a conjecture: it
would carry `s(32) = 6` to `s(45) = 7` and beyond, and is not a theorem.
The “previous best” the source names, wand125’s `119/20 = 5.95` of 2026-09-26, is not in
this repository’s n = 32 file, which still carries Nagamochi’s `1 + √23 = 5.7958`; both
are now superseded.

### F6. The source’s own record of adjacent claims (note)

`notes/literature-s32.md` notes that the source’s `s(11) ≥ 3040/797 = 3.8143` is below
this repository’s `31/8 = 3.875` and below its earlier `3.827`, and that its README’s
“previous published bound” for n = 12 predates this repository’s `99/25 = 3.96` (T-017,
2026-09-04). Those are the source’s corrections of itself, and they are right.
The same note reports, from chelokot’s Lean archive, that two of Bentz’s printed
auxiliary point sets in the `s(13)` proof are avoidable and were repaired in the
formalisation, and that Nagamochi’s Lemma 1 has a counterexample; neither is checked
here and both belong in the n = 13 and n = 14 case files as reported items.

## 6. The Two Lower Bounds and the Re-proof

### 6.1 `s(12) ≥ 15680/3951`

The certificate is 1,736 weighted points in `[0, 15680/3951]²` (D4-symmetric,
`D = 3951`, `W = 10⁷`), total `11.9738036 < 12`, asserting that every closed unit square
inside the container captures weight `≥ 1`. The reduction is the one of §3.2 with
`m = 15680/3951`, and the bound is `s(12) ≥ 15680/3951`, not `>`: the closed convention
and the scaling step give a non-strict inequality, which is what the source claims.
The verifier (`verify/`, Rust `i128`) enumerates rational rotations
`θ_k = 2 arctan(k/N)`, uses that a unit square at any angle of `[θ_k, θ_{k+1}]` contains
the concentric square of side `σ_k = 1/(cos δ + sin δ)` at angle `θ_k`, and takes the
exact minimum over all centres by an arrangement sweep; `xcheck.py` re-derives every bin
in Python rationals.
A positive margin is what makes the shrink admissible, and the source records that the
verifier correctly refuses the certificate at `N ≤ 4000`, where the shrink exceeds the
slack. Verified by the source at `N = 6000` and `12000`; replayed here (§4 table).
The two checkers are one method, an angle net with an arrangement sweep, in two
implementations.

### 6.2 `s(21) ≥ 5000/1001`

Same method: 4,604 points, `D = 1001`, `W = 10⁷`, total `20.80456 < 21`, verifier
minimum `10000083/10⁷` at `N = 6000` and `12000`, `xcheck.py --all` at `N = 6000`
agreeing on the minimum and the binding bin `k = 684` (87 min on 12 workers, not
replayed here). The float scan here gives a least capture of `1.0010177` for the true
squares, above the net minimum as required.
This bound exceeds this repository’s n = 21 ceiling remark, “a certificate for `n`
cannot exist above `⌈√n⌉·B = 4.9885`”: that ceiling is a property of the first-party
core-shrink format at `B = 9977/10000`, not of the method, and `n-021.md` should say so.

### 6.3 `s(13) = 4` without case analysis

3,621 points of `[0,4]²`, total `12.955972155 < 13`, closed cover checked over the
*full* pose domain by `zmcheck` (12,800 roots, 30,258 boxes, 0 uncertified) and over the
reflection-reduced domain by `zeromargin.py` (16,872 boxes, 0 uncertified), the same
Lean reduction, 23 rejection tests.
The value is Bentz’s (2010); the proof replaces his six-leaf case analysis with one
weighted object.
A kernel-checked proof of `s(13) = 4` along Bentz’s lines already exists
in chelokot’s archive, so the value is not new and the source does not say it is.
Independent evidence here: data checks, a float minimum of `1.0279`, and a partial
`zmcheck --d4` replay (§4 table).

## 7. Relation to the Programme

### 7.1 The capacity-one ceiling lemma and the closed-cover dual

The [`4.640020` review](review-2026-09-27-n17-kleddamag-4640020.md) §8 states that a
weighting of legal squares with total `≥ n` and clique sums `≤ 1` on the parent-overlap
graph refutes every capacity-one certificate at that side.
Points are the simplest capacity-one rule, and for point covers the source has the exact
dual in closed semantics: `search/COVER4.md` certifies a fractional packing of mass
`12.2688` at side 4, so no closed point cover of `[0,4]²` weighs below `12.2688` and the
`s(32)` route is closed at n = 12 for good, as this repository’s n = 12 file already
expects. A pointwise-feasible weighting is weaker than a clique-feasible one (every
family of squares through a point is a clique), so the source’s dual does not by itself
decide H-244; but its measurements that the sub-12 duals at `t = 4` need non-Helly
cliques and that the extremal support has independence number 11 against fractional mass
12 are the strongest evidence in hand that a clique-feasible family of value 12 does not
exist at side 4, and H-244’s search at `399/100` should read them before it runs.

### 7.2 Does the zero-margin technique transfer to n = 11 or n = 17?

Not as a bound-raiser.
The technique buys exactly one thing: certification *at* the container when the
conjectured optimum is attained by a configuration whose squares share boundary weight,
a grid. Its cost is the exhaustive subdivision; its precondition is LP room, that a
closed cover below `n` exists at the integer side, which the source measures as 2.4 % at
n = 32 and finds absent at n = 21 (`ν_f^closed(5) ≥ 20.6478`, no closed cover below 21
found) and impossible at n = 12.

- **n = 11.** The target lies in `(31/8, 3.87708…]`, an irrational tilted optimum, not a
  tiling; there is no boundary weight to share and nothing for closed semantics to gain.
  The obstruction at n = 11 is the LP ceiling, not the verification margin: the source’s
  pure cover LP crosses 11 near `3.815`, and it reports that cliques on both sides, the
  corner branch and level-2 Sherali–Adams buy nothing beyond it at n = 11. What does
  transfer is the *exact dual instrument* (`search/dual_exact.py`, rational fractional
  packings as certified ceilings), which prices the point-cover architecture at any side
  exactly and complements the clique-weighted family search of H-243.
- **n = 17.** Bidwell’s `4.6755…` is tilted and non-integer; the strongest bound,
  `4.640020`, already uses free sites and intersecting-family rules at positive margin.
  The zero-margin machinery adds nothing there.
- **Where it does transfer.** Integer-target cases below the grid with LP room: n = 45
  (`k = 7`; the source has a closing loop written up) and n = 60, and n = 21 if a closed
  cover of `[0,5]²` below 21 can be found in the `0.35` of room its dual leaves.
  For this repository the exact pose-space checker is also a method-distinct verifier
  for any closed-square point cover, which is relevant to `C4` for our own covers
  wherever both of our routes are event-cell or core-shrink methods.

## 8. The Rung

Under [`epistemics.md`](../../../epistemics.md):

- **`V4`** for all three bounds: exact-algebraic certificates with replay commands and
  the source’s passing replays; not `V5`, because the computational hypothesis
  `S32CheckerCover` is not proof-assistant checked, and a compound claim takes the rung
  of its weakest load-bearing part.
- **`C1`** now: this review is a qualifying read with the examined and unexamined parts
  stated. **`C3`** once the intake lane records a passing repository replay:
  `certificates/s32/verify.sh --full` (about 5 CPU-hours for both covers) or the
  `zeromargin.py --d4` sweep of the Lean-transcribed cover alone (2.8 CPU-hours), and
  `verify` at `N = 6000` plus a sample of `xcheck.py` bins for n = 12 and n = 21.
- **Not `C4`.** Both `s(32)` checkers are one method, exact subdivision of pose space,
  in two implementations; both `s(12)`/`s(21)` checkers are one angle-net method.
  This repository’s native interval route certifies shrunk cores and cannot decide a
  margin-zero cover as it stands; a method-distinct route for `s(32)` would be a new
  zero-margin checker, and none exists.

External bounds carry no `T-NNN` row, so the `C5` mapping is not recorded; this review
is the case files’ `audit_record`. On replay the n = 32 file moves to `status: proved`
with verified lower bound `6`, the n = 12 file’s verified lower bound moves from `99/25`
to `15680/3951`, and the n = 21 file’s from `122/25` to `5000/1001`, with the displaced
first-party rungs kept as previous bounds and their exact-value ceilings re-worded (F5,
§6.2). The source’s `s(11) ≥ 3040/797` is below the record and is a publication record
only. The `s(13)` proof is a second proof of a `V3` value and changes no field; it
belongs in `n-013.md` as a reported item with the chelokot repair noted alongside.

**Credit.** The results are Evan Daniel’s (`evand`), computer-assisted, with the
weighted-cover idea credited to Burns and Massaccesi, the verification practices to
Mira’s `17squares`, and the unavoidable-set lineage to Göbel, Stromquist, Friedman,
Kearney–Shiu, Nagamochi and Bentz, all acknowledged in the source’s `CREDITS.md` and
README. The source claims no peer review and hedges its priority claim on its own
literature search.

**Licence.** MIT (`LICENSE` at the repository root and under `s12/`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
