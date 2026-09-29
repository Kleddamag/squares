# Proof Review: Evan Daniel’s `s(21) = 5` and `s(45) = 7` by Mixed Covers

Reviewed 2026-09-28 and 2026-09-29 from a read-only checkout of
`github.com/evand/square-packing` at `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3`
(2026-09-28T09:36:28−06:00), copied to scratch before anything ran, by a Fable max
sub-agent acting as the mathematical reviewer.
This is an adversarial soundness review of two published computer-assisted exact values,
`s(21) = 5` and `s(45) = 7`, where `s(n)` is the least side of a square containing `n`
unit squares with disjoint interiors, each freely rotated.
It follows the
[review of the same author’s `s(32) = 6`](review-2026-09-27-evand-s32-s12.md) and reuses
its findings about `zeromargin.py`, which both new proofs import unchanged.
It is evidence for the coordinator, not a verdict of record: no result row was
registered and no bound was moved by writing it.

**In one line:** each value rests on a *mixed cover* of the closed container, a finite
measure made of weighted points and of mass spread uniformly along short segments of the
interior grid lines, of total `20.8947 < 21` (side 5) and `44.7735 < 45` (side 7), such
that every closed unit square inside the container captures mass at least 1, the edge
mass counting in full; the packing argument is the classical concentric shrink, proved
in Lean for arbitrary measures; the cover property is decided at margin zero by two
programs that share no code, an exact-rational subdivision (`zm_mixed.py`) and an
interval-enclosed subdivision (`zmx2`), whose lemmas I re-derived against their code and
found sound; and the shipped run records re-summarise cleanly, reproduce here root for
root wherever I re-ran them, and reject the covers when I weaken them.
No mathematical defect was found in either claim.
What is not machine-checked is the two checker programs themselves, and for `s(45)` the
data facts and the top theorem, which are script-checked rather than kernel-checked.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `github.com/evand/square-packing`, directory `s12/` |
| Commit | `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3`, `main`, 2026-09-28 |
| Claims | `s(21) = 5`; `s(45) = 7` |
| `s(21)` cover | `certificates/s21/s21_mixed_cover_5.txt`, `8b415ceeb5f20b02c4e338ce2feb21bc206051ef6bc5c7e433bebae2ef39fc23` |
| `s(45)` cover | `certificates/s45/s45_mixed_cover_7.txt`, `5da180d18434ec52a48b05e8ae0ce70453a280dd482df01d997f73bfbc627c6c` |
| Exact checker | `search/zm_mixed.py`, `ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac`; its reader `search/mixed_cover.py`, `bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5`; imported `search/zeromargin.py`, `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab`, all three byte-identical to the frozen copies in both bundles’ `zm_mixed_d4/checker/` |
| Interval checker | `verify2/src/bin/zmx2.rs`, `6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed` (the post-audit parser) |
| Lean, `s(21)` only | `lean/Sqpack/S21.lean` `9fd69971…`, `S21Data.lean` `a0632ed9…`, `MixedMeasure.lean` `157bcb4d…`, `SegTree.lean` `7f122c73…`, generator `lean/scripts/gen_s21_data.py` `f2bf5d66…` |
| Bundle scripts | `certificates/s21/verify.sh` `437ebc21…`, `certificates/s45/verify.sh` `a15a6714…`, `search/s21_records.py` `d0edf416…`, `search/mixed_records.py` `60c9e972…` |

Files read in full: both bundle `README.md`s and `certificates/s21/FORMAT.md`,
`search/ZM_MIXED.md`, `search/ZM_MIXED_AUDIT.md`, `search/ZMX2.md`,
`search/ZMX2_AUDIT.md`, `notes/lean-s21.md`, `search/zm_mixed.py` (1,699 lines),
`search/mixed_cover.py`, `verify2/src/bin/zmx2.rs` (2,069 lines),
`lean/Sqpack/{S21,MixedMeasure,SegTree}.lean`, the header and tail of `S21Data.lean`,
the `Packs`, `minSide`, `packs_grid` and `d4_reduce` statements of `S32.lean` and
`D4.lean`, `lean/Axioms.lean`, the segment section of `lean/LADDER.md`, both
`verify.sh`, `search/s45_cert_runs.sh`, all six run manifests, and the parts of
`search/zeromargin.py` that the phantom mechanism relies on (`Checker.__init__`,
`_adm_specs`, `_cond_poly`, `_adm_cond_ok*`, `cert_adm`, `_p1_mask`, `_p1_exact`,
`cert_p1`, `cert_mix`, `_gcoef`, `_gle0`, `_box_ctx`, the `T` set of `cert_chain_fast`,
`_quad_le0`, `_bern_le0_i`, `clip_bin`, `bin_data`, `roots`, `d4_roots`). The rest of
`zeromargin.py` is covered by the earlier review.
Lean was not built here (no toolchain in the container); the Lean files were reviewed as
text against the source’s stated build and axiom report.

First-party context: [`epistemics.md`](../../../epistemics.md), the
[retained packet](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md)
of 2026-09-27 (an earlier commit of the same repository), and the frontier files
`packing/frontier/n-021.md` (reported lower bound `5000/1001`, the same author) and
`n-045.md` (reported lower bound `1391/200`, wand125).

Scratch instruments written for this review live outside the repository at
`/tmp/claude-0/…/scratchpad/rev2145/`: `static2.py` (an independent parser, exact
totals, all eight symmetries as a measure, an exact pose evaluator), `records.py` (an
independent re-summary of all six shipped run records), `rerun.sh`, `compare.py` and
`leafcheck.py` (single-root reruns of the shipped checker, census comparison, and exact
checks of the dumped leaves), and two exactly scaled covers for rejection runs.
They import nothing from the source.

## 2. Verdict

**(a) `s(21) = 5`: no mathematical defect found.** The theorem is stated in Lean as the
standard `s(21)`, `minSide 21 = 5`, from one named hypothesis, `S21CheckerCover`, and
that hypothesis is, term for term, the statement the shipped
`zm_mixed.py --d4 --cert-mode` run certifies over its 40,000 closed root boxes and the
shipped `zmx2 --d4` run over its 2,500; `zmx2 --full` certifies the unfolded statement
over 20,000 roots without using the symmetry at all.
The reduction from a measure to a packing, the D4 fold for measures, the cover’s total
and its invariance are kernel-checked.
Every acceptance in `zm_mixed.py` is a `Fraction` or integer comparison and every one in
`zmx2` is an integer comparison on quantities enclosed by outward-rounded binary64
arithmetic; the float pre-screens of both can only lose certifications.

**(b) `s(45) = 7`: sound as stated.** The same two checkers, the same bytes, on a cover
of `[0,7]²`; `zm_mixed.py` over 78,400 roots, `zmx2` over 4,900 (`--d4`) and 39,200
(`--full`). The reduction is the `m = 7` case of lemmas proved in Lean for every `m`;
the data facts (total `< 45`, exact D4 invariance) are checked by three independent
parsers, the source’s two and mine, but not by the kernel, and no top theorem exists.
Nothing about this cover is weaker mathematically; it has one fewer kernel-checked link.

Both proofs are at margin zero in the scale direction by necessity: 25 and 49 grid tiles
each capture at least 1 by sharing edge mass, so a cover of total `< n` at the integer
side exists only because a closed square counts a segment lying along its edge in full.
That is exactly what the checkers implement and what the closed-square reduction needs
(§3.2). The findings (§8) are about provenance, reproducibility and what remains
unformalised; none is blocking.

## 3. The Theorem and Its Architecture

### 3.1 Statement

Lean (`S21.lean`, definitions from `S32.lean`): `Packs n s` is the existence of `n`
centres and angles with each closed unit square `sq c θ 1 ⊆ box s = [0,s]²` and pairwise
disjoint open interiors; `minSide n = sInf {s | Packs n s}`. The theorem proved is

```lean
theorem s21_eq_five_of_checker (h : S21CheckerCover) : minSide 21 = 5
```

via `s21_isLeast : IsLeast {s | Packs 21 s} 5`, so the infimum is attained;
`s21_packs : Packs 21 5` is `packs_grid 5 21` with no hypothesis.
This is the standard `s(21)`. For `s(45)` there is no Lean file; the statement is the
same one on paper with `m = 7`, `n = 45`, and the `7 × 7` grid.

### 3.2 The reduction for measures, and why edge mass is not double-counted

A mixed cover is the measure `μ = Σ w_p δ_p + Σ_σ w_σ · (uniform probability on σ)`; in
Lean (`MixedCover.measure`) the segment part is the push-forward of Lebesgue measure on
`[0,1]` by `t ↦ a + t(b − a)`, so `μ(Q)` for a closed square is the explicit real
`Σ_{p ∈ Q} w_p + Σ_σ w_σ · segFrac(σ, Q)` (`MixedCover.measure_apply`, `S21Data.mu_sq`),
`segFrac` being the Lebesgue measure of the parameters whose point lies in `Q`. For a
convex closed `Q` that is `|σ ∩ Q| / |σ|`, the “parametric fraction” of `FORMAT.md`, and
it is what both checkers compute: `zm_mixed.py` clips the segment’s parameter interval
by the four closed half-planes of `Q` and multiplies the length by the density; `zmx2`
takes `F(hi) − F(lo)` of the line’s cumulative mass over a closed chord.
A segment lying along an edge of `Q` has all its points in the closed `Q` and counts in
full; one crossing an edge counts its inside part; a segment ending at a grid crossing
where another begins shares only a point of zero length with it; and a point mass at a
corner of `Q` counts once.
No piece is counted twice for one square.

`packing_le_measure` (Lean, `MixedMeasure.lean`): if every closed unit square inside `C`
has `μ(Q) ≥ 1`, then `n` squares of side `L > 1` inside `C` with pairwise disjoint
interiors satisfy `n ≤ μ(C)`. The concentric closed unit square of each lies in the open
interior of its `L`-square (`unit_subset_interior`), so those `n` closed unit squares
are pairwise disjoint measurable sets, and `n ≤ Σ μ(Q_i) = μ(⋃ Q_i) ≤ μ(C)` by
additivity. `not_packs_of_measure` adds the scaling: a packing of `n` unit squares in
side `s < m`, scaled by `m/s > 1`, is such a family in `[0,m]²`, so `μ([0,m]²) < n`
excludes it for every `s < m` at once.
No limit and no compactness argument is needed.

The question the coordinator asked, whether “a segment along an edge counts in full” is
consistent with disjointness, has a clean answer: the cover property is a statement
about *one* square at a time, and squares that share an edge (the 25 grid tiles, each
capturing `≥ 1`, total `> 21`) are simply not disjoint, so nothing is claimed about
their sum. Disjointness enters only after the strict shrink, where two closed unit
squares are disjoint as sets and therefore cannot both contain a point of the same
segment. The measure argument needs nothing about the pieces beyond nonnegativity, which
`MixedCover.Nonneg` states and `validate` enforces; containment in the container is not
even needed (`μ(box m) ≤ μ(univ) ≤ total`).

### 3.3 The D4 fold and the angle parametrisation

`d4_reduction_measure` (Lean) is `d4_reduce` from `D4.lean`, the fold the earlier review
checked for point sets, applied to a measure invariant under `x ↦ m − x` and `x ↔ y`
(`D4InvM`): a pose is moved by quarter turns, which keep `θ`, into the closed quadrant
`[0, m/2]²`, and by a reflection, which sends `θ ↦ −θ ≡ π/2 − θ`, into `θ ∈ [0, π/4]`,
each move preserving admissibility and `μ(Q)`. `d4_reduction_measure_u` restates the
region as `θ = 2 arctan u`, `u ∈ [0, ½]`, which contains `[0°, 45°]` since
`tan 22.5° = 0.4142 < ½` (`exists_u_of_theta`). The region is an *over*-cover of a
fundamental domain (angles up to `53.13°`, the shared edge `c_x = m/2`), which is
harmless: the checkers certify more poses than the fold needs, and the lemmas hold there
because `cos θ, sin θ ≥ 0` on `[0°, 90°)`. Admissibility is the closed condition
`w(θ)/2 ≤ c_x, c_y ≤ m − w(θ)/2`, `w = cos θ + sin θ` (`sq_subset_box_iff`), and
inadmissible poses are exempt in the hypothesis and in both checkers alike.

The invariance actually holds: `S21Data.d4` proves `D4InvM 5 μ` from `check_ok` by
kernel evaluation of the entry-level involutions (segments compared after normalising
their endpoint order, `segNorm`, with `segMeasure_comm` covering the orientation), and I
re-checked both covers, as *measures* (aggregated point weights and merged line
densities), under all eight group elements (§6).

`zmx2 --full` uses a different fold: the cover on `u ∈ [0, ½]` plus its image under
`y ↦ s − y` on `u ∈ [0, ½]`, which covers `θ ∈ [0°, 53.13°] ∪ [36.87°, 90°]` and, with
the `90°` periodicity of the square, every pose, assuming no symmetry of the cover.
For `s(21)` and `s(45)` it therefore decides the unfolded statement directly.

### 3.4 The one hypothesis, term by term

```lean
def S21CheckerCover : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 (5 / 2) → c.2 ∈ Set.Icc 0 (5 / 2) →
    u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box 5 →
      1 ≤ ∑ e ∈ pentries.filter (fun e => pt e ∈ sq c (2 * Real.arctan u) 1), pw e
        + ∑ e ∈ sentries, sw e * segFrac (sa e) (sb e) (sq c (2 * Real.arctan u) 1)
```

| Hypothesis | `zm_mixed.py --d4` | `zmx2 --d4` |
| --- | --- | --- |
| `c ∈ [0, 5/2]²`, `u ∈ [0, ½]` | `d4_roots`: `50 × 50` cells of pitch `1/20` times 16 bins of width `1/32`; the 40,000 closed roots tile the region (re-derived here from the records) | `25 × 25` cells of pitch `1/10` times 4 bins of width `1/8`; 2,500 roots, ids complete |
| `sq c θ 1 ⊆ box 5` | admissible; inadmissible poses exempt (`clip_bin`, `EMPTY`, wall bounds `W`/`M`) | admissible; `box_empty` (Lemma E), Lemma W at walls |
| `pt e ∈ sq`, closed | every containment test is `≤ ½` (`in_rot_square`, `_cond_poly ≤ 0`) | `G_k ≤ 0` (Lemma P), non-strict |
| `segFrac`, closed `Q` | parameter interval clipped by closed half-planes | closed chords `[lo*, hi*]` |
| `1 ≤ …` | leaf `EMPTY`, or `PIECE`/`ADM`/`CHAIN`/`SPLIT` with an exact bound `≥ 1` at every admissible pose | `L(B) ≥ 1` in integer bound units |
| `pentries`, `sentries` | the file’s 7,536 and 1,872 lines, no repeats (`check_ok`; also checked here) | the same file, own parser |
| `pt, pw, sa, sb, sw` | integers over `D = 1000`, `W = 10¹¹` | the same |

So the run’s verdict *is* `S21CheckerCover`, provided the programs are correct.
What Lean does not do, plainly stated by the source and confirmed here: it formalises
none of `zm_mixed.py`’s lemmas (Lemma S, T, L, L′, V, R, P, Corollary L) and none of
`zmx2`’s; `ZeroMargin.lean` covers only `zeromargin.py`’s point primitives, which
`zm_mixed.py` calls through the phantom point.
`lean/LADDER.md` scopes the segment terms as “not started”.
The same file is the certificate the checkers ran on by `gen_s21_data.py --check` (byte
for byte, sha256 in the header), which is a script check, not a kernel one.

## 4. `zm_mixed.py`: The Certification Lemmas as Implemented

For each pose box `[cx₀,cx₁] × [cy₀,cy₁] × [u₀,u₁]` (after `clip_bin`, which only lowers
`u₁` and drops no admissible pose), the checker computes a certified lower bound `L` on
the segment mass at every admissible pose, then hands `L` to `zeromargin.py`’s point
primitives as a *phantom point* that is declared inside `Q` at every admissible pose,
and finally, if those fail, tries `SPLIT`. Children inherit `max(L, L_parent)` and the
exact set of points proved inside `Q` on the parent.
I state each lemma as the code implements it and where its acceptance is decided.

- **Lemma S (certified core of a line, `line_cond_iv`).** For a bound choice `χ` (box
  side, or the wall term), the Lemma-B polynomial `G_{k,χ}(u; p)` of `zeromargin.py` is
  affine in the point `p` (`U`, `V` are affine in `p_x`, `p_y`, and `_cond_poly` is
  affine in `U`, `V`; the both-`R` branch divides by `1 + u²`, which does not depend on
  `p`). Its five degree-4 Bernstein coefficients on the bin are therefore affine in the
  line parameter `t`, so `{t : all β_i(t) ≤ 0}` is an exact rational interval, and by
  Lemma C (`β_i ≤ 0 ⇒ G ≤ 0`) and Lemma A every point of it satisfies inequality `k` at
  every admissible pose.
  The hull over choices is certified because the true set is convex (an intersection of
  half-planes in `p`). The intersection `J₄` over the four inequalities is in `Q` at
  every admissible pose; the mass of the pieces in `J₄` is `L`’s baseline.
  Exact throughout.
- **Lemma T (the germ pair, `_group`).** For lines `x = ξ` and `x = ξ + 1` I re-derived:
  inequality (1) at `(ξ, t)` reads `t ≥ T := c_y + (−½ − (ξ − c_x)cos θ)/sin θ` and
  inequality (0) at `(ξ + 1, t)` reads `t ≤ T + (1 − cos θ)/sin θ = T + u`, so with
  `u ≥ u₀` one threshold governs both lines; at `θ = 0` both inequalities are
  independent of `t` and `T = ±∞` covers the two cases.
  The horizontal pair (`y = η + 1` with (2), `y = η` with (3)) is the same computation
  with `T = T′ − u₀`. The pair’s mass is at least
  `f(T) = F↑(min(T, τ↑)) + G↓(max(T + u₀, τ↓))` on the `J₃`-clipped pieces, a continuous
  piecewise-linear function whose breakpoints are exactly the candidate set the code
  enumerates (piece ends, `τ`, and their `u₀`-shifts); its infimum over the extended
  line is taken at those candidates and on the two constant tails, which the code
  samples at `cand[0] − 1` and `cand[−1] + 1`. Exact (`Fraction`). This is what closes
  the tile germs, where a fixed witness set cannot terminate.
- **Lemma L, general ends (`lemma_l_data`, `end_minorant`).** The eight threshold
  polynomials of the table (V and H lines, up and lo types, denominators `S = 2u` or
  `C = 1 − u²`) were re-derived from `X = (aC + bS)/N`, `Y = (−aS + bC)/N` and all agree
  with `thr_num`. On a box the typed inequalities hold exactly on `[r↓, r↑]` with
  `r↑ = min_k t_k(P) ≥ a↑`, `r↓ = max_j t_j(P) ≤ b↓`, and the untyped ones (S-type when
  `u₀ = 0`) are required, by their Lemma S intervals, on the whole window
  `[b↓ − Δ↓, a↑ + Δ↑]` (line 521–524). The end gain is bounded by an edge of the lower
  convex hull of the piecewise-linear gain function, which lies below it and has slope
  `≥ 0` because the gain is nondecreasing from `0`; any `Δ > 0` is sound and the
  float-guided choice of edge and cap only affects tightness.
- **Lemma L′, hull form, and Lemma V (`vertex`, `vertex_split`).** When the certified
  core is empty (a vertex of `Q` crossing the line) the bound is
  `ℓ₁(min(r↑, B) − p) − ℓ₂(max(r↓, A) − p)` with a lower-hull minorant `ℓ₁ ≤ g` and an
  upper-hull majorant `ℓ₂ ≥ g`, both nondecreasing; it is valid at every pose because
  when `x < y` the right-hand side is `≤ g(x−p) − g(y−p) ≤ 0 ≤ μ`. Lemma V splits the
  box on the sign of `t_k − t_j`, affine in the centre, and counts the line as `0` on
  one side; soundness reduces to Lemma R below, whatever `D` is chosen.
- **Corollary L (`lemma_l_joint`, `phi_at`, `rf_bound`).** At fixed `u` every term is a
  minimum of affine functions of the centre with nonnegative slopes, so the sum is
  concave and its minimum over any rectangle containing the admissible centre rectangle
  is at a corner; replacing `max(c₀, w/2)` by either `c₀` or `w/2` (and dually) gives
  such a rectangle for every `u` (`corner_choices`), whichever the float picks.
  In `u` the corner values are rational functions with denominators `S^a C^b N^c`; the
  option chosen by float at mid-bin is corrected by an exact slack
  `σ ≥ max_u (A_{i*} − A_i)`, and the bound is `min_i β_i(P)/β_i(Den)` over degree-`n`
  Bernstein coefficients, which is a lower bound whenever all `β_i(Den) > 0` (checked;
  `S` in a denominator is refused when `u₀ = 0`). I re-derived the Bernstein conversion
  in `bern` and `bern_n` (`β_i = Σ_{j≤i}
  C(i,j)/C(n,j) b_j` on the shifted, scaled power basis) and the ratio argument
  `P − λ·Den = Σ B_i (β_i(P) − λ β_i(Den)) ≥ 0`. Exact.
- **Lemma R, `SPLIT` (`cert_split`, `region_phi`).** `T` is the set of points proved in
  `Q` at every admissible pose (inherited, or exact P1/ADM tests).
  A swing point has exactly one inequality not exactly verified (the other three are
  decided by `_adm_cond_ok`, exact; a float mask may only decide *which* one is the
  swing). A chain `G_{q₁} ≤ … ≤ G_{q_k}` of one kind is built greedily and every link is
  `_gle0`, the exact integer corner-and-vertex test over the whole box.
  The region of a pose is `r = max{j : G_{q_j} ≤ 0}`; the down-set and up-set membership
  binary searches are monotone by the chain’s exact transitivity (and valid across
  kinds); in region `r` a point with `G_p ≤ G_{q_r}` or `a G_p + b G_{q_{r+1}} ≤ 0`
  (`(a,b) ∈ {(1,1),(2,1),(1,2)}`, and `G_{q_{r+1}} > 0` there) is in `Q`. The piece
  bound on the region is Corollary L minimised over the polygon
  `rect(u) ∩ {G_{q_r} ≤ 0} ∩ {G_{q_{r+1}} ≥ 0}`, whose constraint lines are parallel, so
  every vertex is a rectangle corner or a constraint line meeting an edge line; the code
  keeps every such candidate not *proved* excluded by an exact Bernstein bound on the
  sub-bin, so every true vertex at every `u` survives, and by concavity the minimum over
  the polygon is at least the minimum over any finite set whose hull contains it.
  `EMPTY` is returned only when no candidate survives on any sub-bin, which proves the
  region holds no admissible pose (a nonempty compact convex polygon has a vertex).
  The region weights `w(T) + w(D_r ∪ U_r)` are `Fraction` sums over distinct indices;
  the acceptance `w(T) + w(D_r ∪ U_r) + rest + max(core, Φ_r) ≥ 1` is exact.
  Boxes with `u₀ = 0` never use `SPLIT`.
- **Lemma P (the phantom).** The phantom sits at `(−1000, −1000)`, is placed first in
  `zc.order`, and enters `cert_adm`, `cert_mix` and `cert_chain` only through the `inh`
  mask, where each primitive accepts an `inh` point without a geometric test (traced in
  `cert_adm` line 565, `cert_mix` 615, `cert_chain_fast` 903). `_p1_mask` cannot select
  it (`px + 1 ≥ m` and `cx₁ ≤ px + t` are both false).
  Its three weights are set together per box: `Wnum = ⌊L·Wden⌋`, `W = Wnum/Wden`,
  `Wf = float(W)`, so `CHAIN`’s `int64` region sums see a weight `≤ L`, and
  `zeromargin.py` reads the arrays live (no cached weights).
  Every primitive proves “witness weight in `Q` at every admissible pose `≥ 1`”, and
  replacing “`φ ∈ Q` with weight `L′`” by “piece mass `≥ L ≥ L′`” gives `μ(Q) ≥ 1`.
  `int64` totals: `2.09 × 10¹²` numerators over `10¹¹` (`s(21)`), `4.5 × 10⁹` over `10⁸`
  (`s(45)`), far below `2⁶³`.
- **Inheritance.** A child receives `max(L, L_parent)` (a sub-box has fewer admissible
  poses) and `_last_inT`, the exact `T` set of the parent’s last `CHAIN` attempt, with
  the phantom bit cleared (`kid[ph] = False`, line 1404) so a stale phantom weight
  cannot be inherited; `_last_inT` is reset to `None` before each box.
  `SPLIT` receives the parent’s `inh`, not the phantom.
- **`EMPTY` and `clip_bin`** are `zeromargin.py`’s, proved in Lean (`clip_bin_no_loss`)
  and reviewed before.

Where a false acceptance would have to hide, and why it cannot: every leaf kind ends in
an exact comparison (`L ≥ 1` as a `Fraction`; `total ≥ 1` over `Fraction` weights in
`ADM`/`P1`/`MIX`; `int64` numerator sums in `CHAIN`, with links accepted only by
`_gle0`; `Fraction` sums in `SPLIT`); the float reach windows (`window`,
`R = 0.7072 + …`, the `0.3` band for germ candidates, the `0.75` reach of `zmx2`) only
drop pieces or candidates; the float choice of hull edge, split point, mid-bin option
and chord centre only chooses *which* exact bound is computed; and the Bernstein tests
are sufficient conditions.
The sole float that reaches an exact test is `nfail`/`cmasks` deciding which of a swing
point’s inequalities is left to the chain, and the other three are then tested exactly.
In certificate mode the polygon code asserts if reached and Corollary T′ is unreachable;
both covers have no polygon and no point on a segment line, so neither path ran.

## 5. `zmx2`: The Interval Enclosure

`zmx2` bounds each box by `P(B)`, the exact weight of points certainly inside `Q` (Lemma
P: four violation quadratics in `u` at the four centre corners, decided in `i128` by
endpoints and the vertex test `4p₂p₀ − p₁² < 0`; I re-derived `G₀…G₃`), plus, per family
of lines, a dynamic programme over chains of lines at unit spacing that takes the better
of single-line bounds (Lemma S: `F(hi*) − F(lo*)` on a chord certainly inside) and pair
bounds (Lemma Z). Lemma Z is the germ mechanism: for lines `x = ℓ` and `x = ℓ + 1`, with
`ζ` the crossing of the left edge line with `x = ℓ`, `H1_b = ζ + u` *exactly*
(`f₂(d − 1, u) − f₁(d, u) = u`, checked symbolically), so whatever `ζ` does as `θ → 0⁺`,
line `b` gets the complementary part; `inf_ζ Φ(ζ)` over the enclosed `ζ`-range is exact
because after rounding every quantity is an integer on the grid of pitch `1/(D·2³⁰)` and
`Φ` is piecewise linear with breakpoints in the enumerated candidate set.
Lemma W lowers the ends of a line at distance 1 from a wall using admissibility
(`q(u) = (1 − u² + 2u³)/(2(1+u²))`, re-derived from `f₂` at `d = (C+S)/2 − 1`; the
numerator is positive on `[0,1]`, so the direction of the bound on `[u₀,u₁]` is right),
which closes the wall germs.
Horizontal lines are vertical lines in the frame rotated by `(x, y) ↦ (−y, x)`, which
commutes with the square and carries the walls to `x′ = −s` and `0`. Lemma H covers
`θ = 0` inside a `u₀ = 0` box by the limits `±∞` of `f₁`, `f₂` and the clamp.
All of this matches the code, as the source’s own audit also found.

**Lemma R, the float argument (§5 of `ZMX2.md`).** Every `f64` operation on the
certification path is followed by `next_down`/`next_up` in the safe direction
(`Iv::add/mul`, `recip_pos`, `sqrt`; `rat` converts numerators and denominators below
`2⁵³` exactly and widens the one rounded quotient by four ulps; an exact zero factor
gives an exact zero), and a lower or upper endpoint `v` becomes `⌊next_down(fl(v·G))⌋`
or `⌈next_up(fl(v·G))⌉` with `G = D·2³⁰` exactly representable, which is `≤ v·G` resp.
`≥ v·G` because a round-to-nearest result `r` of `x` satisfies `x ∈ [r⁻, r⁺]`. Values
beyond `±(4s + 10)` are clamped, which changes no `F` value and no atom comparison
because `F` is constant outside `[0, s]` and every shift is at most `u₀ ≤ ½`. After the
grid step everything is `i128`. What the argument needs from the host is
round-to-nearest IEEE-754 binary64 with correctly rounded `+ − × ÷ √`, no contraction or
reassociation, and exact `next_up`/`next_down`. Rust guarantees all of this for `f64` on
every tier-1 target: it sets no fast-math flags, LLVM contracts only under flags Rust
does not emit, `f64::sqrt` lowers to the correctly rounded instruction, and `next_up` is
bit-level. On x86-64 the operations are SSE2 scalar (no x87 extended precision), so the
argument is sound there, and it is not x86-64-specific.
What it does assume is the process’s default rounding mode and no flush-to-zero, neither
of which Rust changes and neither of which matters at these magnitudes.

**The parser fix and what the shipped runs used.** The audit’s one must-fix (F1:
unchecked `i128` wrap on crafted input printed a false side or total next to
`VERIFIED-D4`) is commit `dd6f63aa7e9ba2d7a19c46cb9776ee610ddb3c48`
(2026-09-27T13:21:30−06:00), which is the only change to `zmx2.rs` after its creation;
`zmx2.rs` at `dd6f63a` and at HEAD both hash `6b7f0f79…`. The four shipped `zmx2`
manifests record git HEAD `dd6f63a` (`s(21)`) and `5ae38b9` (`s(45)`), of which
`dd6f63a` is an ancestor (checked with `git merge-base`), zero local changes to
`zmx2.rs`, source sha256 `6b7f0f79…` and the same binary `0247012e…` for all four runs.
So the fixed parser is what ran.
With its bounds (`s_num, s_den < 2⁴⁰`; `D < 2²⁰`; `s·D < 2²⁷`; `W` and every weight
`< 2⁵⁰`; total `< 2⁵⁶`; `lcm` of segment lengths `≤ 2²⁴`; `cl, ul ≤ 27`) I traced every
integer product on the certification path: the point test’s terms are below `2¹²¹` even
without the reach filter; `fval` stays below `2¹¹¹` because `y` lies inside one density
piece; bound sums are below `2¹¹¹`; atom weights below `2¹⁰⁴`; grid values below `2⁸⁰`.
All are below `2¹²⁷`. `Cargo.toml` still has no `overflow-checks` in the release profile
(F3).

**Is anything left that could turn a false statement into `VERIFIED`?** I found nothing.
The verdict is printed only after every worker thread has joined; a panic anywhere (NaN,
an assertion, an overflow under debug checks, a malformed log line) aborts the process
without a verdict; capped roots push their whole stack into `uncert`; `INCOMPLETE` and
`REGION CLEAN` are distinguished from `VERIFIED`; the D4 check for `--d4` is exact on
aggregated points and canonical line densities; and the `--log` resume is keyed on an
FNV hash of the file and settings (audit S3), which the shipped runs did not exercise
(“0 already done” in all four manifests; `verify.sh` writes to a fresh `mktemp` log).

## 6. The Two Covers

Independent checks (`static2.py`, own parser, `Fraction` arithmetic, about 2 s and 4 s):

| Fact | `s21_mixed_cover_5.txt` | `s45_mixed_cover_7.txt` |
| --- | --- | --- |
| Header | `mixed 1`, `s = 5`, `D = 1000`, `W = 10¹¹` | `mixed 1`, `s = 7`, `D = 1000`, `W = 10⁸` |
| Points, segments, polygons | 7,536; 1,872; 0 | 19,989; 3,912; 0 |
| Total, exact | `522368729933 / 25·10⁹ = 20.894749197320 < 21` | `2238676387 / 5·10⁷ = 44.773527740000 < 45` |
| Point part; segment part | `3.506855058`; `17.387894139` | `11.937117100`; `32.836410640` |
| All pieces in the container, all weights `≥ 0` | yes; point numerators in `[2006, 867085476]`, segment numerators in `[192576, 9292637529]` | yes; `[2, 765520]` and `[2, 9730382]` |
| Segments | all 1,872 axis-parallel, of length exactly `1/50`, on `x, y ∈ {1, 2, 3, 4}`, no overlaps, no repeats | all 3,912, length `1/50`, on `x, y ∈ {1, …, 6}`, no overlaps, no repeats |
| Points on a segment line; zero weights; repeated coordinates | 0; 0; 0 | 0; 0; 0 |
| Invariance of the measure under all 8 elements of D4 | exact | exact |

The totals agree with both bundle headers, with `S21Data.total_eq`
(`2089474919732 / 10¹¹`, the same rational) and with both `zmx2 info` lines.
The `s(21)` file is the source’s candidate scaled by `1003/1000`, the `s(45)` file its
LP round scaled by `409/400`; the first comment line of each says so.

Exact masses at a few poses show what margin zero means here (my evaluator, closed
squares): the tile `(3/2, 3/2)` captures `1.839105825` at `θ = 0` and `1.027096552` at
`u = 10⁻⁵` (`0.00115°`) for `s(21)`, `1.844477490` and `1.065071855` for `s(45)`; the
corner tile `(½, ½)` at `θ = 0` captures `1.007029753` and `1.022501040`; the central
tile `(5/2, 5/2)` of `[0,5]²` captures `1.713467146` at `θ = 0` and `1.007542407` at
`u = 10⁻³`. The `θ = 0` values count the whole edge mass; the `θ → 0⁺` values are what
the checkers must beat, and the germ lemmas (T and Z) are what make a box at such a pose
closable at all.
The source’s own rejection experiments put the least mass of the `s(21)`
cover near `1.0057` (at `(0.5736, 1.4406, 9.21°)`, a tilted dip, not a germ) and the
`s(45)` cover about `0.7 %` above its threshold.

## 7. Evidence

| Obligation | Result here |
| --- | --- |
| Certificate and checker identities | all sha256 in both `SHA256SUMS` confirmed; the three checker files in both `zm_mixed_d4/checker/` equal `search/` at HEAD and each other; `zeromargin.py` equals the `s(32)` bundle’s pinned copy |
| Totals, D4 invariance, well-formedness | re-derived, both files (§6) |
| Lean statement matches `s(21)` and the checkers’ conventions | confirmed by reading (§3) |
| Shipped `zm_mixed.py` records (`records.py`, own code) | `s(21)`: 40,000 records, 40,000 distinct roots, exactly the `[0, 5/2]² × [0, ½]` grid, header shas equal the checker files and the cover, settings `D4, depth 24, pitch 1/20, 16 bins, chain from 0, cert mode`, census 461,204 boxes, max depth 21, ADM 146,017 / CHAIN 23,518 / SPLIT 53,951 / PIECE 9,058 / EMPTY 18,058 / UNCERT 0, 46,426 CPU-s; `s(45)`: 78,400 records, the `[0, 7/2]²` grid, 437,510 boxes, depth 19, ADM 122,892 / CHAIN 45,866 / SPLIT 54,276 / PIECE 9,458 / EMPTY 25,463 / UNCERT 0, 59,469 CPU-s. Both satisfy the binary-tree identity `boxes − leaves = leaves − roots`, so every internal node has two recorded children |
| Shipped `zmx2` logs | `s(21)` `--d4`: 2,500 roots with ids `0…2499` and the expected boxes, 1,826,222 boxes, 888,945 certified, 25,416 empty, 0 uncertified, 0 capped, depth 26; `--full`: 20,000 roots, 14,709,448 boxes, depth 27; `s(45)` `--d4`: 4,900 roots, 2,071,984 boxes, depth 24; `--full`: 39,200 roots, 16,648,752 boxes, depth 24; the tree identity holds in all four |
| `zmx2 --d4` replayed here (built from HEAD with rustc 1.94.1, one thread) | `s(21)`: `VERIFIED-D4`, 28 CPU-s, census identical to the shipped log on all 2,500 roots (boxes, certified, empty, uncertified, max depth, capped); `s(45)`: `VERIFIED-D4`, 48 CPU-s, identical on all 4,900 roots; both `zmx2 d4` checks pass |
| `zmx2 box` against my exact evaluator | germ box `x ∈ [1.5, 1.5 + 1/1280]`, `y ∈ [1.5 − 1/1280, 1.5]`, `u ∈ [0, 1/2048]`: bound `1.005246975`, exact mass at 28 admissible sampled poses `≥ 1.017324417`; the next `u`-slice `1.005274680` vs `1.014433360`; a wall box at `(½, 3/2)`: `1.004799014` vs `1.007043668`; the corner root and the dip root are correctly not certified at depth 0 (bounds `0.742`, `0.883` against exact `≥ 1.007`, `≥ 1.049`) |
| Single-root reruns of the shipped `zm_mixed.py` (same bytes, `--cert-mode`, one process) | 11 roots chosen for their geometry: `s(21)` interior germs `[1.5,1.55] × [1.45,1.5]` and `[1.45,1.5]²` at `u ∈ [0, 1/32]` (115 and 91 boxes, depths 10 and 9, CHAIN 16 and 12), the corner root (one `PIECE` leaf), the wall root `[0.5,0.55] × [1.5,1.55]` (one `ADM` leaf), a `SPLIT` root at `θ ≈ 31°` (9 boxes), and the tilted-dip root `[0.55,0.6] × [1.4,1.45] × [1/16, 3/32]` (671 boxes, depth 17, ADM 276 / SPLIT 3 / PIECE 3 / EMPTY 54); `s(45)` the germs `[1.5,1.55] × [1.45,1.5]` and `[1.5,1.55]²`, the central tile root `[2.5,2.55]²`, the dip root (295 boxes, depth 14) and a CHAIN root. Every census (boxes, depth, every leaf kind, the empty uncertified list) is identical to the shipped record of that root; CPU here 1.0 to 1.4 times the source’s |
| Exact check of the dumped leaves (`leafcheck.py`, own evaluator, `Fraction` arithmetic) | the 630 leaves of those 11 roots (553 certified, 77 `EMPTY`): at the 8 corners, 8 random rational interior poses, and 2 poses on the low-`u` face of every leaf, 7,718 admissible poses in all, the exact total mass is `≥ 1` in every certified leaf (least `1.007029753`, the corner tile at `θ = 0`), the exact segment mass is `≥` the phantom weight `L` recorded in the witness of every non-`EMPTY` leaf (least slack `5.3 × 10⁻⁵`, at the corner `PIECE` leaf, so the checks are sharp), and no sampled pose of an `EMPTY` leaf is admissible; 0 violations |
| Rejection: covers weakened exactly (`W × 1000`, weights `× 994` resp. `× 985`; D4 invariance kept) under `zmx2 --d4`, one thread | `s(21) × 0.994` (total `20.7694`): `NOT VERIFIED`, 1,085 uncertified boxes at depth 40 in 209 CPU-s, the deepest at `(0.573593, 1.440624, u = 0.0805601)`, float mass `0.999690`, which is the tilted dip the source’s audit found (`ZMX2_AUDIT.md` A1, `ZMX2.md` T5) to the sixth digit; `s(45) × 0.985` (total `44.1019`): `NOT VERIFIED`, 4,887 uncertified boxes in 328 CPU-s, the tightest at `(2.3000, 3.2000, u = 0.4389)`, `θ = 47.4°`, float mass `0.998789`, so the `s(45)` cover’s binding region is a tilted pose near `(2.3, 3.2)` at about `1.4 %` above 1 by float, not a germ |

## 8. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. The `s(45)` `zm_mixed.py` record was imported, not regenerated for the bundle (non-blocking)

The bundle’s `zm_mixed_d4/roots.jsonl` was produced on 2026-09-27 under the working path
`runs/s45_mixed_candidate_7.txt` (16.5 CPU-h, 12 processes), then copied with only the
header’s `input` *path* changed, and `zm_mixed.py --resume` was run on the copy, which
recomputes the header from the files (all four sha256, settings, total), refuses a
mismatch, found all 78,400 roots done and wrote the manifest (hence `wall_s 0.1` and
`--nproc 1` in its `argv`). The `README.md` discloses this and `run.log` shows both
invocations with the same input sha256 `5da180d1…`. The cover-specific evidence for
`s(45)` is therefore thinner than for `s(21)`: no holed-cover rejection runs and no
component tests were made on it, as the README says.
A complete `verify.sh --full` replay, which the intake lane is running, closes both
gaps; my rejection run on the exactly weakened cover (§7) is a partial substitute.

### F2. `zmx2` binaries are toolchain-bound; the census is the reproducibility handle (note)

All four manifests name the binary `0247012e…` built with rustc 1.91.1. A build from the
same source here with rustc 1.94.1 hashes `5ee58ade…` and reproduces every root’s
census. As with `zmcheck` in the earlier review (F2), a replay cannot match the binary
hash; it should record the source hash `6b7f0f79…`, the compiler, and the root-for-root
census comparison that `verify.sh` performs.

### F3. Release builds still run without integer overflow checks (note)

The parser bounds make every `i128` path safe (§5), but `Cargo.toml`’s release profile
(`opt-level = 3`, `lto = true`) sets no `overflow-checks`. Enabling it would turn any
residual overflow into a panic, hence no verdict, at some speed cost, and would guard
the `box` and `boxes` subcommands, whose box coordinates are not bounded by the parser.
Defence in depth, not a defect.

### F4. The float model is Rust’s, not the machine’s (note)

`certificates/s21/README.md` states the caveat correctly (“IEEE-754 requires the former;
Rust guarantees the latter; x86-64 SSE2”). For the record: the enclosure argument
depends on the language guarantees listed in §5, which hold on every Rust tier-1 target,
and a replay on aarch64 is as valid as one on x86-64. The one environmental assumption
is the default rounding mode, which a foreign library linked into the process could
change; `zmx2` links none.

### F5. The lemma layer of both checkers is unformalised (note)

For `s(32)` the primitives that certify (`ZeroMargin.lean`) are kernel-checked and only
the programs are not.
For `s(21)` and `s(45)` the lemmas that do the work on the segments, `zm_mixed.py`’s S,
T, L, L′, V, R and P and all of `zmx2`’s, are proved on paper and audited (twice by the
source, once here) but not in Lean; `zeromargin.py`’s kernel-checked primitives enter
only through the phantom.
`LADDER.md` §“Next: segments” scopes the formalisation.
This is the part that sets the rung (§9), and it is why the two checkers’ independence
matters more here than for `s(32)`.

### F6. `s(45)` has no kernel-checked data facts and no top theorem (note)

`not_packs_of_measure` and `d4_reduction_measure_u` are proved for every `m`, so the
missing pieces are mechanical: a `S45Data.lean` from a generalised `gen_s21_data.py`
(`X ≤ 7000`, `W = 10⁸`), `check_ok`, `total_eq`, `d4`, and the eight-line top theorem.
Until then the data facts rest on three independent parsers (`mixed_records.py`, `zmx2`,
and mine), which agree.

### F7. Regions and settings, for the record (note)

`zm_mixed.py` certifies `u ∈ [0, ½]` in 16 bins at centre pitch `1/20`; `zmx2` in 4 bins
at pitch `1/10`; both are over-covers of the `[0°, 45°]` fold and both are what the Lean
hypothesis states. The load-bearing `zm_mixed.py` options are `--d4 --cert-mode --disj
--chain-from 0 --depth 24 --pitch 1/20 --ubins 16`; a run without `--cert-mode` would
still be sound (it enables code the covers never reach) but would not match the shipped
header, and `--resume` would refuse it.

### F8. Record context (note)

`packing/frontier/n-021.md` carries the same author’s `5000/1001` as reported lower
bound and `n-045.md` wand125’s `1391/200`; on replay both files move to exact values,
`s(21) = 5` and `s(45) = 7`, so that the members `k = 5, 6, 7` of the family
`s(k² − 4) = k` are settled (`k = 3` fails, `s(5) = 2 + 1/√2`; the `k = 4` member,
`s(12)`, is open and cannot be reached by any cover measure at side 4, since the
source’s exact fractional packing of mass `12.2688` at side 4, noted in the
[earlier review](review-2026-09-27-evand-s32-s12.md) §7.1, bounds every such measure
from below). The source’s claims of the “second” and “third” exact value of `s(k² − 4)`
for `k ≥ 4` are consistent with this repository’s record.

## 9. The Rung

Under [`epistemics.md`](../../../epistemics.md):

- **`V4`** for both: exact-algebraic (`zm_mixed.py`) and interval-certified (`zmx2`)
  certificates with replay commands and the source’s passing replays.
  Not `V5`: the computational hypothesis is not proof-assistant checked, and a compound
  claim takes the rung of its weakest load-bearing part (F5). The Lean chain for `s(21)`
  raises what is kernel-checked, not the rung.
- **`C1`** now: this review is a qualifying read with the examined and unexamined parts
  stated. **`C3`** once the intake lane records one complete repository replay per claim:
  `certificates/s21/verify.sh` (fresh `zmx2 --full`, about 100 CPU-s) or its `--full`
  tier (the `zm_mixed.py` D4 sweep, 12.9 CPU-h), and likewise for `s(45)` (150 CPU-s;
  16.5 CPU-h).
- **`C4`** once both replays pass, on the structural predicate: two `C3` entries with
  different `method` values.
  Substantively the two decisions differ in their bounding mathematics (Lemmas T, L and
  R with `zeromargin.py`’s chains, against Lemma Z’s pair dynamic programme with Lemma
  P), in their arithmetic (rationals, against outward-rounded binary64 on an integer
  grid), and in the symmetry assumed (`zmx2 --full` assumes none).
  What they share is the architecture, branch and bound over the `(c, u)` pose space
  with admissibility exemption, and the statement they decide; the composition note
  should name that shared architecture as the residual common-mode risk.
  This is a stronger position than `s(32)`’s, where both checkers were exact
  subdivisions with the same lemma family.

**Not machine-checked, numbered:**

1. `zm_mixed.py`’s lemmas (S, T, L, L′, V, R, P, Corollary L) and its program:
   subdivision, clipping, inheritance, the `SPLIT` bookkeeping, `--resume`, and the
   parser `mixed_cover.py`.
2. `zeromargin.py`’s program (its primitives’ lemmas are in Lean).
3. `zmx2`’s lemmas (C, M, Z, W, H, DP, E, P, R) and its program, including its own
   parser.
4. The IEEE-754 model of the host and compiler that Lemma R needs (§5, F4).
5. The Lean build: `lake build` clean against Mathlib `v4.33.1`, no `sorry`, axioms
   `propext`, `Classical.choice`, `Quot.sound` only, as `notes/lean-s21.md` reports; not
   built here.
6. That `S21Data.lean` is the certificate (`gen_s21_data.py --check`, a script).
7. That the shipped run records were produced by the shipped files (hash-linked headers
   and manifests; only a replay removes this).
8. For `s(45)`: the total `< 45` and the entry-level D4 invariance (three parsers, no
   kernel) and the top theorem (absent).

**What the replay lane must check.** From `s12/` of a clean copy of the source tree at
`6aa82ba…`, with `python3` resolving to the project interpreter (CPython 3.14.7 with
numpy; `zm_mixed.py` forks a `multiprocessing` pool):

- `certificates/s21/verify.sh` and `certificates/s45/verify.sh` must end with
  `s(21) bundle: OK` and `s(45) bundle: OK`; along the way `COVER CLEAN`,
  `zm_mixed D4 RECORDS CLEAN`, `zmx2 d4 RECORDS CLEAN`, `zmx2 full RECORDS CLEAN`, the
  fresh `zmx2 --full` verdict `VERIFIED` with 14,709,448 resp.
  16,648,752 boxes and 0 uncertified, and
  `fresh census identical to the shipped zmx2_full/roots.log, root for
  root`. Record the rustc version and the binary hash; confirm `verify2/src/bin/zmx2.rs`
  hashes `6b7f0f79…` (the post-fix parser).
- The `--full` tier must print `census identical to the shipped records for
  40000 / 40000 roots` and `78400 / 78400 roots`, verdict `VERIFIED-D4`, totals 461,204
  and 437,510 boxes with 0 uncertified, and no `note: search/… differs from the shipped
  checker` line; the run headers must carry `cert_mode: true`.
- For `C4` both replays of each claim are needed: the `zm_mixed.py` D4 sweep and the
  `zmx2 --full` sweep.
  The `zmx2 --d4` sweeps (28 and 48 CPU-s here) are a cheap additional control, not a
  substitute for `--full`.
- Optional: `search/zmx2_tests.sh` (45 tests, including the two overflow inputs and the
  differential `cert` test) and `zm_mixed_test.py selftest`.

External bounds carry no `T-NNN` row, so the `C5` mapping is not recorded; this review
is the case files’ `audit_record`.

**Credit.** The results are Evan Daniel’s (`evand`), computer-assisted, with the mixed
cover, the germ lemmas and both checkers his; the weighted-cover idea is credited by the
source to Burns and Massaccesi and the verification practices to Mira’s `17squares`, as
in `CREDITS.md`. The source claims no peer review.

**Licence.** MIT (`LICENSE` at the repository root and under `s12/`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
