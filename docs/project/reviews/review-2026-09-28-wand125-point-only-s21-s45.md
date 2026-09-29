# Proof Review: wand125’s Point-Only Certificates for `s(45) = 7` and `s(21) = 5`

Reviewed 2026-09-29 from a read-only sparse checkout of
`github.com/wand125/square-packing-bounds` at `39d8ecc74d651b54ec977c331c8f2015b442a6c4`
(2026-09-29T07:20:47+09:00), copied to scratch before anything ran, by a Fable max
sub-agent acting as the mathematical reviewer (Session 161, W2 factual review,
correctness lane).
The two claims are computer-assisted proofs of exact values of `s(n)`,
the least side of a square containing `n` unit squares with disjoint interiors, each
freely rotated: a point-only closed cover of `[0,7]²` for `s(45) = 7` (`point_n45_L7/`),
decided by Evan Daniel’s `zmx2`, and a point-only cover of `[0,5]²` with a capture
threshold below 1 for `s(21) = 5` (`point_n21_L5/`), decided by wand125’s own rational
replay.
Both values were first proved by Evan Daniel with mixed point-and-segment covers,
reviewed in the [companion review](review-2026-09-28-evand-s21-s45-mixed-covers.md);
this review covers only what is specific to the point-only certificates and takes
`zmx2`’s own soundness from that review and from the source’s audit.
It is evidence for the coordinator, not a verdict of record: no result row was
registered and no bound was moved by writing it.

**In one line:** both certificates are sound as stated, given a passing complete replay.
For `s(45)` the pinned `zmx2` is the post-audit parser, `--pair-points` is a sound
treatment of off-grid point pairs at margin zero, the data facts hold exactly, the cover
carries a uniform pointwise margin of `8.35 × 10⁻⁴` with essentially no room in the
scale direction, and a complete sweep rebuilt here from the pinned source reproduces the
reference census and verdict.
For `s(21)` every acceptance in the runner is an exact rational comparison: floating
point appears only in the proposal code the replay never calls, and each retained proof
object is re-derived and compared before it counts; the Lean overlay states the standard
`s(21)` from one hypothesis that matches the runner’s domain term for term; and my own
exact probes, including a from-scratch `zmx2` sweep of the normalised cover, find the
least captured mass at `1.00105`, above the certified threshold `0.999948` and above
`1`. No blocking finding; the notes are about method distinctness, documentation of the
runner’s closure, and what remains unformalised.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Source | `github.com/wand125/square-packing-bounds`, `point_n45_L7/` and `point_n21_L5/` |
| Commit | `39d8ecc74d651b54ec977c331c8f2015b442a6c4`, `main`, 2026-09-29; the four commits `b97c796`, `d38917c`, `b64f96e` (2026-09-28) and `39d8ecc` created the two directories |
| Claims | `s(45) = 7`; `s(21) = 5` (with `s(n) = 5` for `22 ≤ n ≤ 25` as corollaries) |
| `s(45)` cover | `point_n45_L7/cover.txt`, `f7d706aa07506c351d9c4b76082cc391ae3f1fd20f6759496bd7c601bb0ca192` |
| `s(45)` checker | `zmx2` from `evand/square-packing` at `6e1223cf7ef2be4c70baaa36c0e7e7197076735a`, `s12/verify2/src/bin/zmx2.rs`, `6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed` |
| `s(21)` cover | `point_n21_L5/certificates/n21-original.txt`, `84a7dae793f05ff72de52ddcd3058e8518c1f84c461f94d11305adefe6137679`; normalised copy `n21-capture-one.txt`, `9f631fbae4…` |
| `s(21)` runner | `verify_portable.py`, `assemble_portable.py`, the bundle’s `portable_replay.py`, and the 29-module import closure under `verifier-source/` (2,267 lines) |
| `s(21)` Lean | `lean/Sqpack/{N21Pts,N21PtsAxioms,N21PtsData}.lean`, `lean/scripts/gen_n21pts_data.py`, `lean/build_lean.sh`, as an overlay on the same upstream commit |
| Upstream (evand) | `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3` in scratch; the pinned `6e1223cf` read with `git show` |

Files read in full: both `README.md`s, `check_cover.py`, `verify.sh`, `provenance.json`;
`FORMAT.md`, `PROOF-LEMMAS.md`, `PUBLICATION.md`, `lemma-code-map.json`,
`inspect_certificate.py`, `unpack_bundle.py`, `verify_portable.py`,
`assemble_portable.py`, `verifier-source/portable_replay.py`, the three runner scripts
under `verifier-source/runs/…/n21_L5_refit29_final_replay/` (`frontier.py`,
`run_prefix.py`, `run_frontier.py`), the six retained audit and test scripts beside
them, every module the runner imports (`closed_cover_bridge`,
`compile_box_capture_rows`, `point_box_sieve`, `stratified_box_cover`,
`verify_angle_clip`, `physical_pose_enclosure`, `replay_physical_point_witness`,
`predicate_lp_capture`, `predicate_conflict`, `predicate_branch`, `predicate_partition`,
`physical_predicate_conflict`, `physical_predicate_branch`, `replay_capture_margin`,
`transfer_point_capture`, `reoptimize_capture_weights`,
`reoptimize_physical_tree_weights`, `extend_reweighted_physical_tree`,
`near_axis_partition_bridge`, `near_axis_projection`, `certify_near_axis_sweep`,
`certify_n21_near_axis_path`, `exact_fixed_angle_separator`,
`probe_external_integer_bridge`, `checkpoint_external_cover`,
`inherit_monotone_cover_roots`, `score`), the `acceptance/` receipts, the Lean overlay,
`s12/verify2/src/bin/zmx2.rs` at `6e1223cf` (2,069 lines), `search/ZMX2.md`,
`search/ZMX2_AUDIT.md`, `certificates/s45/README.md` and `verify.sh` upstream, and the
`MixedMeasure.lean`, `Basic.lean` and `D4.lean` declarations the overlay uses.
The 2.54 GB proof-object bundle was not unpacked: its records are what the replay lane’s
run exercises, and this review checks the code that reads them.
Lean was not built (about 24 minutes and 8 GB per the source).

First-party context: [`epistemics.md`](../../../epistemics.md), the frontier files
`packing/frontier/n-021.md` and `n-045.md`, the
[`s(32)` review](review-2026-09-27-evand-s32-s12.md) for `zeromargin.py` and the
closed-cover reduction, and the
[companion review](review-2026-09-28-evand-s21-s45-mixed-covers.md) for `zmx2` and
`zm_mixed.py`.

Scratch instruments written for this review live outside the repository at
`/tmp/claude-0/…/scratchpad/rev/`: `scan.py` (a float scan of the D4 region with exact
confirmation of the lowest poses, own parser and evaluator), `uncert.py` (exact probes
of `zmx2`’s uncertified boxes), `n21src/fixed_angle.py` (drives the source’s exact
fixed-angle sweep and re-evaluates every witness independently), a band driver, and
`zmx2build/` (the pinned `verify2` tree built with `cargo 1.94.1`, binary
`5ee58adea339e1a911712108aeec044d57b268ee3025821397c64c1c6476c39b`, the same bytes the
companion review built from HEAD). Everything ran on one core.

## 2. Verdict

**(a) `s(45) = 7`: sound as stated, given a passing replay of `verify.sh`.** The pin is
the post-audit `zmx2`; the closed-square convention, the admissibility exemption and the
D4 fold are those of the companion review, unchanged; `--pair-points` turns 6,105
off-grid points into atoms of 2,530 “partner lines” so that the pair lemma couples them,
and each atom’s membership is still decided by exact integer tests; the total,
nonnegativity and D4 invariance hold exactly; and the complete D4 sweep, rebuilt from
the pinned source and run here on one thread, returns `VERIFIED-D4` with the reference
run’s census. The reduction from the cover to the packing bound is the `m = 7` case of
`not_packs_of_measure`, proved in Lean upstream for every `m`; nothing about this cover
is in Lean.

**(b) `s(21) = 5`: sound as stated, given a passing complete replay of
`verify_portable.py`.** The runner is an exact rational replay of a retained tree of
local certificates; I found no acceptance decided by a floating-point quantity, no
inherited success flag, and no rule in `PROOF-LEMMAS.md` whose code departs from the
written argument. The threshold `q = 249987/250000 < 1` is a device for the checker’s
looseness, not a weakness of the measure: the exact fixed-angle minima at seven angles,
the exact near-axis band, a float scan, and the uncertified boxes of an independent
`zmx2` sweep all put the least captured mass at `1.001050000003`, at the corner tile.
The Lean overlay proves `minSide 21 = 5` from one hypothesis that is the runner’s
statement term for term.

Neither route claims priority; both supports come from Evan Daniel’s certificates, and
the `s(21)` coordinates are his `s21_lower_4.9950.txt` scaled by `1001/1000`, entry for
entry, with new weights.

## 3. `s(45) = 7`: `cover.txt` Under `zmx2 --d4 --pair-points`

### 3.1 The pin

`verify.sh` clones `evand/square-packing`, checks out `6e1223cf`, and refuses to build
unless `s12/verify2/src/bin/zmx2.rs` hashes `6b7f0f79…`. Checked here with
`git merge-base --is-ancestor`: the parser fix
`dd6f63aa7e9ba2d7a19c46cb9776ee610ddb3c48` (2026-09-27T13:21:30−06:00, “bound every
input integer in the parser”, `ZMX2_AUDIT.md` F1) is an ancestor of `6e1223cf`
(2026-09-27T22:57:02−06:00), and `6e1223cf` is an ancestor of the upstream head
`6aa82ba`. Only two commits touch `zmx2.rs`, its creation `5d91695` and the fix, and the
file at `6e1223cf` hashes `6b7f0f79…`, the same bytes the companion review audited at
HEAD. So the bounds `s_num, s_den < 2⁴⁰`, `D < 2²⁰`, `s·D < 2²⁷`, `W` and every weight
`< 2⁵⁰`, total `< 2⁵⁶` are in the parser that runs.
`cover.txt` sits inside them: `D = 2000`, `s·D = 14000`, `W = 2⁴⁹`, the largest weight
`43243284027951 < 2⁴⁶`, total numerator `25332742837415646 < 2⁵⁵`. The `Iv::rat`
assertion `|n|, d < 2⁵³` holds with room: denominators reach `10 · 2²⁷ · 2000 < 2⁴²`.

`verify.sh` accepts only `VERIFIED-D4`, no `NOT VERIFIED`, and, from the per-root log,
exactly 4,900 distinct `(pass, root)` records with `uncert 0` and `capped 0`; a worker
panic aborts `zmx2` without a verdict and `set -e` stops the script.
The root grid is `35 × 35 × 4` over `[0, 7/2]² × [0, ½]`, which `--d4` requires and
which contains the `[0°, 45°]` fold (`u ≤ √2 − 1 < ½`). The reference run in
`provenance.json` used rustc 1.86.0 on Apple silicon under Rosetta: 1,295,460 boxes,
maximum depth 38, 204 s on eight threads.

### 3.2 The statement checked

`zmx2 cert … --d4` certifies: every closed unit square `Q ⊆ [0,7]²` with centre in
`[0, 7/2]²` and `θ = 2 arctan u`, `u ∈ [0, ½]`, has `μ(Q) ≥ 1`, and `check_d4` proves
exactly that `μ` is invariant under `x ↦ 7 − x` and `x ↔ y`, so the fold of
`d4_reduction_measure_u` gives every admissible square.
Closedness is built into every point test: Lemma P’s four violation quadratics are
accepted when `≤ 0`, so a point on the boundary of `Q` counts, as the closed-square
reduction needs. With `μ([0,7]²) = 12666371418707823/2⁴⁸ < 45`,
`not_packs_of_measure 7 μ … 45` excludes 45 squares at every side below 7, and the
`7 × 7` grid gives the upper bound.

### 3.3 What `--pair-points` does, and why it is sound at margin zero

Without segments, `zmx2` has two ways to count a point.
An ordinary point counts on a box only if all four of its containment conditions hold at
every pose of the box (Lemma P), which can never terminate at a *germ*: a square sitting
on a grid cell, tilted by `θ → 0⁺`, loses points along one edge line and gains their
partners one unit away, and no fixed witness set is captured throughout a box around
such a pose. The line machinery exists for this.
A point whose abscissa is an interior grid line becomes an *atom* of that vertical line
(then ordinates, then, under `--pair-points`, any abscissa or ordinate that has a
partner point exactly one unit away, `build_cover` lines 450–503); each atom’s four
conditions are decided per box by the same exact integer test (`pt_conds`), and for a
pair of lines at distance exactly 1 the pair lemma (Lemma Z) counts an atom of the left
line whose only uncertain condition is `y ≥ ζ` and an atom of the right line whose only
uncertain condition is `y ≤ ζ + u` together, as functions of the one unknown crossing
`ζ`, taking the infimum over the enclosed range of `ζ` exactly (`pair_bound` lines
889–974). I checked three things that matter for a point-only cover:

- **Closedness of the atom tests.** An `a`-atom counts at `z` iff `y ≥ z` and a `b`-atom
  iff `y ≤ z + u₀ᴳ`, with `u₀ᴳ = ⌊u₀ G⌋ ≤ uG`, so an atom is counted only when its true
  condition holds with the closed inequality, and a point exactly on an edge of `Q` is
  counted, never double-counted (an atom belongs to one line, Lemma DP). The code takes,
  at every candidate `z`, the minimum of the two one-sided limits `A(z) + B(z⁻)` and
  `A(z⁺) + B(z)`, each `≤ Φ(z)` since `A` is nonincreasing and `B` nondecreasing, so the
  reported value is a lower bound of `inf Φ`.
- **`θ = 0` inside a `u₀ = 0` box (Lemma H).** At `θ = 0` the `a`-atom’s missing
  condition is `d ≤ ½` and the `b`-atom’s is `d ≥ ½` independently of `y`; the clamped
  range `[−big, big]` of `ζ` contains the values `z = ∓∞` that reproduce exactly those
  cases, and both ends are among the candidates evaluated.
  The source’s audit checked the same case (its §3.2, “conditional `a`-atoms at
  `z = −big` are in `Q` iff `d ≤ ½`”).
- **Walls (Lemma W).** For a line one unit from a wall the `H1` (or `L1`) condition of
  an atom is granted when `y ≤ y₀ + q_lo` (or `y ≥ y₁ − q_lo`), using admissibility; the
  grid values `h1w = ⌊(y₀ + q_lo)G⌋` and `l1w = ⌈(y₁ − q_lo)G⌉` are rounded in the safe
  direction. At `θ = 0` the granted condition is admissibility itself.

Everything float-derived that reaches an atom decision (the `ζ`-range ends, the wall
thresholds, `u₀ᴳ`) is an outward-rounded enclosure of Lemma R; the reach filters
(`|c − ℓ| ≤ 0.75`, atoms within `0.75` of the centre range along the line) can only drop
mass, since a unit square reaches at most `√2/2 = 0.7071` from its centre.
The mode was exercised upstream on the `s(32)` point cover, where
`zmx2 --d4 --pair-points` agrees with `zmcheck` and `zeromargin.py`, two checkers that
share no code with it, and by the 686 random covers of the audit’s A6, which mix in
partner lines and `--pair-points`. On `cover.txt` the assignment is: 2,722 atoms of
vertical grid lines, 2,694 of horizontal grid lines, 4,533 of vertical partner lines,
1,572 of horizontal partner lines (1,265 partner positions each way), and 1,124 ordinary
points; 91 % of the points, and 31.68 of the 45.0 in mass on grid lines plus 12.10 on
partner lines, go through the line machinery.

### 3.4 The data

Exact, own parser: 12,645 entries, 12,645 distinct coordinates, no zero weight, all
inside `[0, 14000]²` at `D = 2000`, none on the container boundary, total
`12666371418707823 / 281474976710656 = 44.999991000011`, so `45 − μ = 2533271697/2⁴⁸ =
9.0 × 10⁻⁶`; invariant under all eight elements of the dihedral group as an aggregated
weight map, 1,602 orbits.
`check_cover.py` (the shipped exact check) and `zmx2 info`/`d4` agree on every figure.
The weights are an LP solution scaled by `14999997000000/14987483391827 = 1.000834937…`
and rounded up on the `2⁴⁹` grid, which the float scan confirms: the least captured mass
found is `1.000834937` at several unrelated poses, `(307/500, 1693/500, t = 67/500)`,
`(7/2, 7/2, t = 117/500)`, `(1451/500, 1227/500, t = 83/500)`, and at wall-tight poses
`(h(t), 5/2)` and `(h(t), 7/2)` for small `t`, each confirmed with exact rationals; the
LP was tight at many contacts, and the scaling turned exact contacts into a uniform
margin of `8.35 × 10⁻⁴`. Tile-centre germs are comfortable: the corner tile `(½, ½)`
captures `1.010146844` at `θ = 0`, the interior tiles at least `1.038872517` at
`t = 10⁻⁶`.

The three roots containing the float minima, run here with the pinned binary under
`--d4 --pair-points`, certify with 445, 1,041 and 3,507 boxes at depths 12, 25 and 27
and no uncertified box (`REGION CLEAN`); the first also certifies without
`--pair-points`. A complete single-thread sweep here returns `VERIFIED-D4` with exactly
the reference run’s 1,295,460 boxes and depth 38 (§5).

### 3.5 Why a point-only cover works at side 7

The obstruction to a point cover at an integer side is not margin zero as such but LP
room: the `k²` closed grid cells must each capture `≥ 1` while the total stays below
`k² − 4`, which is possible only because points on the interior grid lines are shared by
two or four cells.
Evan Daniel measured 2.4 % of room for points at side 6 (`s(32)`), and
at side 5 his search found no closed point cover below 21, which is why his `s(21)` and
`s(45)` covers carry segment mass (totals `20.8947` and `44.7735`, half a percent of
room each after scaling).
wand125’s LP at side 7 found `≈ 0.08 %` of room on its support (total `≈ 44.9625` before
the scale-up, then `44.999991`), enough for a certificate but nothing more: the scale
direction is spent, and a pointwise margin of `8 × 10⁻⁴` is what `zmx2` must resolve,
hence depth 38 against 24 for the mixed cover.
At side 5 the same author’s point cover has `8 × 10⁻⁶` of normalised room, the thinnest
object in this record (§4.1). So point-only covers do work at the integer side; they are
simply much tighter than mixed ones, and the checker that decides them has to be
correspondingly finer.

## 4. `s(21) = 5`: The Point-Only Runner

### 4.1 The argument with a threshold below 1

The measure `μ` has 4,604 entries at `(X/1000, Y/1000)` with weights `w/10¹²`, 84 of
them zero, total `M = 2624862500021/125000000000 = 20.998900000168`. The certified
statement is: every closed unit square `Q ⊆ [0,5]²` has `μ(Q) ≥ q = 249987/250000`. Then
`μ/q` has capture `≥ 1` and total `M/q = 2624862500021/124993500000 = 20.999991999752
< 21`, so the closed-cover reduction applies verbatim (`not_packs_of_measure 5 (μ/q)`):
21 squares in side `L < 5`, scaled by `5/L`, contain 21 pairwise disjoint concentric
closed unit squares of total mass `≥ 21 > M/q`. The strict gap is `21q − M =
999979/125000000000 = 8.0 × 10⁻⁶`; the runner’s weakest leaf bound is
`249987033421/250000000000 = q + 1.34 × 10⁻⁷`. These margins are small but irrelevant to
soundness, because nothing in the acceptance path is approximate (§4.3).

They are also not the measure’s margins.
The exact fixed-angle sweep of the source (`exact_fixed_angle_separator.separate`, an
arrangement sweep whose returned witness pose I re-evaluated with my own exact code at
every angle) gives the global minimum over all admissible centres of `1.001050000003` at
`t = 0, 10⁻⁶, 10⁻³, 10⁻²` (at the corner tile, near `(0.52, 0.52)`), `1.004577882254` at
`t = 1/10`, `1.001766415788` at `t = 1/4` and `1.003275113575` at `t = 5/12`; the exact
near-axis band recomputed here (`sweep`, 212,680 polynomial sign conditions,
`T = 1/80014`) has the same minimum on `(0, T]`, cross-checked at `t = T, T/2, T/10⁷`; a
float scan of 476,000 poses finds nothing below `1.00105`; and the boxes an independent
`zmx2` sweep leaves uncertified (§5) probe exactly to `1.001050000003`. So the measure
almost certainly captures `≥ 1` everywhere, with `M < 21` directly; the runner certifies
the weaker `≥ q` because its local bounds lose about `10⁻³` at the worst leaves, and the
weaker statement is enough.
A record entry should describe the certificate as it is certified: capture
`≥ 249987/250000`, total `20.998900`, normalised total `20.999992 < 21`.

### 4.2 What the runner replays

The bundle is a retained tree of local certificates from the author’s search campaign
(75,130 files, 2.54 GB), a frozen source tree, and a manifest; `verify_portable.py`
refuses `python -O`, records the hashes of itself, the assembler, the bundle runner and
the manifest, runs four stages as subprocesses with BLAS threads pinned to one, requires
exit 0 from each, then assembles and re-checks the hashes.
`portable_replay.py` binds every `.py` in the manifest by SHA-256 before importing any,
maps the campaign’s historical absolute paths into the bundle, refuses paths outside it
or absent from the manifest, and installs an audit hook so that no read of the original
tree can occur; every artifact is loaded through `checked_bytes`, which compares its
hash with the manifest, and `assemble` re-hashes every read at the end.

- **Root stage** (`run_prefix.py --stage root`, 139 s upstream).
  The 5,000 roots are the `25 × 25 × 8` grid of `[0, 5/2]² × [0, ½]` (asserted box by
  box). For each root a source record from the earlier candidate lists closed leaves
  (`ADM` or `EMPTY`), angle clips and uncertified boxes; the replay proves each `ADM`
  leaf on the *new* weights by an exact point witness (`replay_physical_point_witness`,
  mass `≥ 1`) or by a repair partition (`replay_partition`, bound `≥ q`), each `EMPTY`
  leaf by the exact physical enclosure (`enclose` returns no admissible pose), each clip
  by `verify_angle_clip`, and then proves from scratch that closed leaves, uncertified
  boxes and clipped boxes cover the root on every stratum
  (`stratified_box_cover.verify`). Uncertified boxes become the 8,758 pending parents;
  12 repairs are counted and asserted.
- **Sieve stage** (412 s upstream).
  Each pending parent is partitioned (containment, disjoint interiors, exact volume),
  each leaf’s enclosure recomputed and compared, and each leaf proved by an exact
  witness on the enclosing box (`point_box_sieve.replay`, mass `≥ 1`), a repair
  partition, or left pending; 38,730 pending, 104 repairs, and the pending list must
  equal, box for box, the frontier file the campaign used.
- **Frontier stage** (7,873 and 7,968 s on two shards upstream).
  Of the 38,730 parents, the 31,678 with `t₀ ≤ 5/12` are required and the 7,052 with
  `t₀ > 5/12` are outside the fold; `Checker.parent` re-partitions each required parent
  from its source record and proves every piece by one of: a direct partition proof on
  the new weights (`replay_partition`: predicate-LP duals, signed conflicts, branch
  trees, all exact); a recomputed near-axis band (`replay_band`); a reweighted model or
  tree (`linear_replay`, `tree_replay`, `extended_replay`: the old proof is replayed on
  the old weights, its rows are recomputed, and new rational duals on the same rows with
  the new costs are checked); or, last, transfer (`bound_alpha_one`, `bound`) from an
  old bound replayed on the same physical box.
  A piece with no proof raises; an empty piece is recorded as such.
- **Assembly** (`assemble_portable.py`). Root grid, stage-to-stage pending identities,
  every partition, every required index exactly once, every leaf bound `≥ q` as a
  `Fraction`, candidate hash, nonnegativity, D4 invariance on the two generators, the
  total, the gap `21q − M > 0`, `(17/12)² > 2`, 21 distinct grid cells, and the closing
  hash check of every artifact read.

Nothing is trusted from a saved flag: `lower`, `success`, `certified` fields are
compared with recomputed values or ignored.
The design is fail-closed throughout; every mismatch is an exception, and
`verify_portable.py` writes `failure.json` and re-raises.

### 4.3 Every numerical stage, and what makes it rigorous

This is the question the coordinator asked.
I traced every function reachable from `run_prefix.py`, `frontier.Checker.parent` and
`assemble` and classified each use of floating point.

| Where floats appear | What they do | What decides acceptance |
| --- | --- | --- |
| `point_box_sieve.witness` | numpy screen of candidate points (search only) | `replay`: `contains_all` in `Fraction` for each listed index, `Fraction` mass `≥ 1`, string-equal to the record |
| `predicate_lp_capture.certify` | `scipy.optimize.linprog` (HiGHS) proposes dual multipliers, rounded to `10⁻¹²` rationals (search only) | `replay_certificate` passes the record’s multipliers, so `linprog` is not called; predicates, implications and opposed rows are recomputed by exact quadratic maxima; `rational_bound` is `Fraction`; `baseline`, `lower`, `rows`, `cost`, `predicate_ids`, `point_records`, `residual_penalty` must equal the record |
| `predicate_conflict.find_conflict`, `strengthen` | LP proposes a cut’s multipliers (search only) | `verify_sum`: `Fraction` maximum of the signed sum over the box, strict-positivity rule, row equality with the record |
| `predicate_branch.solve`, `solve_tree` | LP picks branch variables and duals (search only) | `replay_tree`: both children required, `BOUND` leaves by `rational_bound`, `EMPTY` leaves by a rational dual of the slack model with bound `> 0`, `OPEN` leaves never certify |
| `physical_predicate_*` | the same LPs with four wall predicates (search only) | wall polynomials exact; `reduce_wall_clause` substitutes the fixed wall truth values exactly |
| `reoptimize_*`, `extend_reweighted_physical_tree` | new duals proposed by LP under the new costs (search only) | old proof replayed first; cost and baseline mappings checked; every new leaf by `replay_dual`; new cuts re-verified geometrically |
| `transfer_point_capture` | none | `classify` by exact quadratic maxima, `α` from a finite rational set |
| `certify_near_axis_sweep`, `certify_n21_near_axis_path` | none | integer polynomial arithmetic; every sign comparison recorded and re-verified at the final `T` by an exact remainder bound |
| `exact_fixed_angle_separator` | none | `Fraction` arrangement sweep; the witness is re-evaluated by polygon containment |
| `compile_box_capture_rows`, `replay_physical_point_witness`, `physical_pose_enclosure` | none | `Fraction` quadratic maxima at the stated corner; `Fraction` quartic Bernstein coefficients with wall substitution; `Fraction` enclosure |
| `stratified_box_cover`, `verify_angle_clip`, `validate_partition` | none | `Fraction` |
| `assemble_portable`, `inspect_certificate` | none | `Fraction` |

So no floating-point value decides an acceptance; the floats live in proposal functions
that sit in the same modules and that the replay never enters (which is why `numpy` and
`scipy` must be installed even though they do no work).
I also checked the mathematics behind each exact rule against its code, since a wrong
exact rule would be worse than a float: the four predicate polynomials in `t = tan(θ/2)`
(`closed_cover_bridge.predicate`) and their corner maxima; the `×2` variants and their
stated maximising corners in `contains_all`; the wall-substituted quartics and the
Bernstein test in `replay_physical_point_witness.contains`; the LP relaxation
(`y − Σ z ≥ 1 − k`, implications from `max(g_i − g_j) ≤ 0`, opposed pairs from
`max(g_i + λ g_j) ≤ 0`, `λ > 0`) and the residual bound `λᵀb + Σ min(0, c − Aᵀλ)` on
`[0,1]` variables; the strictness rule of a conflict cut (`max H < 0`, or `≤ 0` with a
false predicate in the support); the slack model’s claim that every `x ∈ [0,1]ⁿ` admits
slack in `[0,1]`; the transfer identity at any `α ≥ 0`; the fixed-angle sweep’s boundary
argument (a boundary centre has a nearby interior centre capturing a subset); the
near-axis projection formulas (re-derived from `ℓ ≤ aU − bV ≤ H`, `ℓ ≤ bU + aV ≤ H`),
the tail bound `|Σ_{j>k} c_j t^j| ≤ t^k · S · T ≤ t^k |c_k|/2` that freezes every
comparison on `(0, T]`, and the fact that `T` only shrinks so earlier conditions stay
valid; the closed-partition argument (containment, disjoint interiors and equal volume
imply a cover of every boundary point); the stratified check; and the clip (`w` strictly
increasing below `√2 − 1`). All agree with `PROOF-LEMMAS.md` and with the code.
The 12 retained unit tests (`test_edges`, `test_partition`, `test_sweep_algebra`) pass
here in 0.9 s under CPython 3.14.7, numpy 2.5.2, scipy 1.17.1, versions other than the
tested `3.12.2 / 2.5.3 / 1.18.1`.

### 4.4 The lemma map, sampled

`lemma-code-map.json` pins `PROOF-LEMMAS.md` (hash matches) and 23 source files; all 23
hashes match the readable copies under `verifier-source/`, and the manifest binds the
same bytes inside the bundle.
Sampled mappings, all found where the appendix says:

| Appendix | Code | Checked |
| --- | --- | --- |
| §1 uniform polynomial tests | `closed_cover_bridge.predicate`, `quad_max`; `compile_box_capture_rows.contains_all`, `quadmax` | polynomials and corner choice re-derived |
| §2 physical container, Bernstein | `physical_pose_enclosure.enclose`; `physical_predicate_conflict.wall_polynomials`; `replay_physical_point_witness.contains` | `h` unimodal, endpoint minimum; wall quadratics; quartic Bernstein conversion |
| §3 exact dual residual | `predicate_lp_capture.rational_bound`, `certify` | rows and residual as written; `test_dual_residual_exhaustive` |
| §4 cuts, branches, empties | `predicate_conflict.verify_sum`; `predicate_branch.replay_tree`, `slack_model` | strictness rule; both children; slack dual `> 0` |
| §5 transfer | `transfer_point_capture.bound`, `bound_alpha_one`; `replay_capture_margin` | identity at any `α`; old bound replayed on the same box (`frontier.leaf` asserts `proof['box'] == outer`) |
| §6 fixed angle | `exact_fixed_angle_separator.separate` | run here at seven angles with independent witness checks |
| §7 near-axis band | `certify_near_axis_sweep.sweep`, `Signs`; `near_axis_partition_bridge.replay_band` | run here; projection formulas and tail bound re-derived |
| §8 closed partitions, clips | `compile_box_capture_rows.validate_partition`; `stratified_box_cover.verify`; `verify_angle_clip.verify` | volume argument; strata; monotone `w` |

The map is not the replay’s closure, which has 29 modules (F7).

### 4.5 The Lean overlay, term for term

`build_lean.sh` clones the same upstream commit, checks that `Sqpack.lean` hashes
`094c02f9…` (it does at `6e1223cf`), copies three files and the generator in, appends
two `import` lines, regenerates `N21PtsData.lean` with `--check`, greps the overlay for
`sorry`, `native_decide` and `axiom`, builds, and requires both `#print axioms` reports
to be exactly `propext, Classical.choice, Quot.sound`. The generator, run here with
upstream’s `gen_s21_data.py` from `6e1223cf`, regenerates `N21PtsData.lean` byte for
byte from `n21-original.txt` (hash asserted; header `5 1 1000 10¹² 4604`; 4,604 distinct
keys; integer mass sum `20998900000168`). Every upstream name the overlay uses
(`d4_reduce`, `sq_add_pi_div_two`, `sq_subset_box_{reflX,swapXY}_iff`, `mem_sq_self`,
`sin_two_arctan`, `cos_two_arctan`, `packs_grid`, `PTree.chainB`, `nodup_of_chainB`,
`all_iff`, `mem_sound`, `wsum_eq`, `Packs`, `minSide`, `reflX`, `swapXY`,
`MixedCover.measure_univ_{eq,le}`, `d4InvM`, `not_packs_of_measure`) exists at that
commit; the build itself was not run here.

What is proved in Lean, by kernel evaluation where data is involved: `check_ok` (the
entries form a valid search tree with no repeated key, `X ≤ 5000`, and the images under
`pX : (X, Y, w) ↦ (5000 − X, Y, w)` and `pS : (X, Y, w) ↦ (Y, X, w)` are entries, which
gives `Y ≤ 5000` through `pS`); `card_pentries = 4604`; `total_eq`; `nonneg`;
`d4 : D4InvM 5 μ` via upstream’s `MixedCover.d4InvM`; `q_pos`, `margin_eq`,
`normalized_total_eq`, `normalized_box_lt : (μ/q)(box 5) < 21`;
`n21pts_exists_t_of_theta : tan(π/8) < 5/12`; the reduction from the checker domain to
all poses (`n21pts_checker_reduction`, an instance of `d4_reduce`); `n21pts_not_packs`
from `not_packs_of_measure`; `n21pts_packs` from `packs_grid`; and

```lean
theorem n21pts_eq_five_of_checker (h : N21PtsCheckerCover) : minSide 21 = 5
```

with the single hypothesis

```lean
def N21PtsCheckerCoverFor (ν : Measure (ℝ × ℝ)) (a : ℝ≥0∞) : Prop :=
  ∀ (c : ℝ × ℝ) (t : ℝ), c.1 ∈ Set.Icc 0 (5 / 2) → c.2 ∈ Set.Icc 0 (5 / 2) →
    t ∈ Set.Icc 0 (5 / 12) → sq c (2 * Real.arctan t) 1 ⊆ box 5 →
      a ≤ ν (sq c (2 * Real.arctan t) 1)
```

at `ν = μ`, `a = ENNReal.ofReal q`. Against the runner:

| Hypothesis | Runner |
| --- | --- |
| `c ∈ [0, 5/2]²` | roots `[x/10, (x+1)/10]`, `x = 0…24`, in both coordinates |
| `t ∈ [0, 5/12]` | roots `[t/16, (t+1)/16]`, `t = 0…7`, cover `[0, ½]`; every frontier parent with `t₀ ≤ 5/12` is required, only `t₀ > 5/12` (strict) is excluded, so a pose with `t ≤ 5/12` lies in a certified leaf or a required parent |
| `sq c θ 1 ⊆ box 5` | admissibility `h(t) ≤ c ≤ 5 − h(t)`, `h = (cos θ + sin θ)/2`: enclosures, wall predicates, clips; empty leaves are exactly “no admissible pose” |
| closed `sq` | every containment is `g ≤ 0`; a false predicate is `g > 0` |
| `ofReal q ≤ μ(sq)` | every nonempty leaf has a rational lower bound `≥ 249987/250000`; `mu_sq` identifies `μ(sq)` with the filtered weight sum |
| `pentries`, `pt`, `pw` | the file’s 4,604 triples, no repeated coordinate, `(X/1000, Y/1000)`, `w/10¹²`, exactly `geometry()` |

So a passing run of `verify_portable.py` is `N21PtsCheckerCover`, provided the programs
are correct. What Lean does not do: none of `PROOF-LEMMAS.md` is formalised, in contrast
to upstream’s `ZeroMargin.lean` for `zeromargin.py`; the README’s “everything except the
capture computation is also checked in Lean” is true of the reduction and the data and
should be read that way (F10).

## 5. Evidence

Run here on one core, x86-64 Linux, project CPython 3.14.7, `cargo 1.94.1`, on scratch
copies; exact unless marked.

| Obligation | Result |
| --- | --- |
| `zmx2` pin | `dd6f63a` is an ancestor of `6e1223cf`; `zmx2.rs` at `6e1223cf` hashes `6b7f0f79…`, unchanged through `6aa82ba`; built here in 17 s, binary `5ee58ade…` |
| `s(45)` data | own parser: counts, ranges, total, `45 − μ = 9.0 × 10⁻⁶`, full D4 invariance, orbits, atom census (§3.4); `check_cover.py` prints `COVER_OK points=12645 total=… < 45, D4-invariant`; `zmx2 info` and `zmx2 d4` agree |
| `s(45)` least mass (float scan, 930,000 poses, then exact) | `1.000834937274` at `(307/500, 1693/500, 67/500)`, the same value at `(7/2, 7/2, 117/500)` and `(1451/500, 1227/500, 83/500)`; corner tile `1.010146844` at `θ = 0`; interior tiles `≥ 1.038872517` at `t = 10⁻⁶` |
| `s(45)` weakest roots under `zmx2 --d4 --pair-points` | roots `(34, 34, bin 1)`, `(6, 33, bin 1)`, `(29, 24, bin 1)`: 445 / 1,041 / 3,507 boxes, depths 12 / 25 / 27, 0 uncertified, `REGION CLEAN` |
| `s(45)` complete `zmx2 --d4 --pair-points`, one thread (the pinned source, binary `5ee58ade…`) | `VERIFIED-D4`: 4,900 roots, 1,295,460 boxes, 629,884 certified, 20,296 empty, 0 uncertified, 0 capped, maximum depth 38, 1,749 CPU-s; the box count and depth equal the reference run’s in `provenance.json` (rustc 1.86.0, Apple silicon), so the two censuses agree in the only two figures the reference records |
| `s(21)` data | `inspect_certificate.py`: `EXACT_CERTIFICATE_DATA_CHECKED`, hashes, `q`, `M`, normalised mass, gap, D4, support scale `1001/1000` in order; my parser agrees; 84 zero weights retained |
| `s(21)` fixed-angle minima (source sweep, my witness check) | `t = 0, 10⁻⁶, 10⁻³, 10⁻²`: `1.001050000003`; `t = 1/10`: `1.004577882254`; `t = 1/4`: `1.001766415788`; `t = 5/12`: `1.003275113575`; every witness agrees exactly |
| `s(21)` near-axis band (source `sweep`, 9 s) | `(0, 1/80014]`, minimum `1.001050000003`, 8,525 strips, 212,680 conditions, all re-verified at `T`; anchor at `t = 0` the same; `separate` at `T`, `T/2`, `T/10⁷` agrees |
| `s(21)` float scan, 476,000 poses, then exact | least `1.001050000003` on the corner-tile plateau; tile germs at `t = 10⁻⁶`: `(5/2, 5/2)` `1.006443044`; wall-tight `(h(t), 5/2)`: `1.006380729` |
| `s(21)` normalised cover under `zmx2 --d4 --pair-points` (independent checker, 607 CPU-s) | `NOT VERIFIED`: 2,500 roots, 769,766 boxes, 368,010 certified, 17,896 empty, **238 uncertified** in roots 416, 420, 516 (222, capped at the 200-box uncertified cap), 520, 596, all at the corner-tile germ `c ≈ (½, ½)`, `u < 1/131072`, and the wall germ `(½, 5/2)`, maximum depth 40; the float minima `zmx2` reports over those boxes are `1.001102 … 1.005725` and my exact probes of them give `1.001050000003 ≥ q`; a completeness loss of `zmx2` at a `0.11 %` normalised margin (its own tightness experiment puts its loss below `0.1 %`), not a counterexample |
| retained unit tests | 12 pass (`test_edges` 5, `test_partition` 4, `test_sweep_algebra` 3) |
| lemma map and appendix hashes | 23 / 23 files and the appendix match |
| Lean data | `gen_n21pts_data.py --check` regenerates `N21PtsData.lean` byte for byte; `Sqpack.lean` at `6e1223cf` hashes `094c02f9…`; all referenced upstream names exist |
| acceptance receipts | `m1-full-replay.json`: `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`, four exits 0, 8,577.3 s; both linkage records: `PORTABLE_COMPLETE_REPLAY_LINKAGE`, `minimum_frontier_leaf 249987033421/250000000000`, 75,130 source reads |

## 6. Findings

Severity is blocking, non-blocking, or note.
**None is blocking.**

### F1. `verify.sh`’s standalone D4 gate is decorative (non-blocking, `s(45)`)

`"$Z" d4 "$HERE/cover.txt" | tee "$WORK/d4.log"; grep -q 'invariant' "$WORK/d4.log"`
passes on the failure message too (`ERROR: --d4: cover is not D4-invariant: …` contains
the word), and the pipeline’s exit status is `tee`’s, so `set -e` does not stop a
non-invariant cover there.
The real gate is `cert --d4`, which repeats the exact check and dies with exit 2 before
any root runs; `check_cover.py` also checks the three generators.
The proof is unaffected; the line should read `grep -q '^D4: measure invariant'` under
`set -o pipefail`.

### F2. Only the D4-reduced sweep is run, and the reference log is not shipped (note, `s(45)`)

Unlike upstream’s `s(45)` bundle, which also runs `zmx2 --full` over 39,200 roots with
no symmetry assumed, `point_n45_L7/` relies on the fold.
The fold is proved for measures upstream and its premise is checked exactly, so this is
a matter of defence in depth; a `--full` run costs about eight times the `--d4` sweep.
`provenance.json` records the reference run only by census and by the SHA-256 of its
`roots.log`; the log itself is not in the repository, so a replay can compare its census
against the figures in `provenance.json` (4,900 roots, 1,295,460 boxes, depth 38) but
not root for root. The single-thread sweep here reproduces both figures (§5); its
per-root log, `n45_zmx2_d4.log` in the scratch directory, is the nearest substitute for
a shipped one.

### F3. The point-only route leans on `zmx2`’s least-exercised path (note, `s(45)`)

With `--pair-points`, 11,521 of the 12,645 points are atoms of grid or partner lines and
only 1,124 are decided by Lemma P alone; the certificate therefore rests on the atom and
pair code (`line_atoms`, `pair_bound`, Lemma H at `θ = 0`, Lemma W at the walls), which
upstream exercised on one shipped point cover (`s(32)`, cross-checked by two independent
checkers) and on the audit’s random covers, and which the companion review and this one
re-derived. That is reasonable evidence, and §3.3 records why the path is sound; but a
method-distinct decision of *this* cover would come from a point checker that shares
nothing with `zmx2` (`zeromargin.py --d4`, or `zmcheck`), and at a pointwise margin of
`8 × 10⁻⁴` its cost is unknown (the `s(32)` cover, at `1.1 %`, took 2.8 and 80
CPU-hours). Not required for the claim.

### F4. No room in the scale direction (note, `s(45)`)

`45 − μ([0,7]²) = 9 × 10⁻⁶` and the pointwise margin is a uniform `8.35 × 10⁻⁴` obtained
by scaling an LP solution that was tight at exact contacts.
Nothing can be shaved from the weights, and any reweighting means a new LP and a new
sweep. The margins are what they are; exact totals and exact integer tests make them
safe.

### F5. Nothing about this cover is in Lean (note, `s(45)`)

As with upstream’s `s(45)`: the reduction is the `m = 7` case of lemmas proved for every
`m`, the data facts rest on `check_cover.py`, `zmx2`’s parser and mine, and no top
theorem exists.
The same mechanical additions the companion review lists (F6 there) would
close it.

### F6. The threshold `q < 1` is a checker artefact; the record should say what was certified (note, `s(21)`)

§4.1: every exact probe of the measure gives `≥ 1.00105`, the certified bound at the
worst leaf is `q + 1.3 × 10⁻⁷`, and `21q − M = 8 × 10⁻⁶`. The proof is valid as stated
with `q`; it is not a proof that `μ` captures `≥ 1`, although it very probably does.
The sentence in `README.md`, “all-pose capture threshold is `q = 249987/250000`”, is the
accurate one.

### F7. The lemma map is not the replay closure (non-blocking, `s(21)`)

`lemma-code-map.json` omits three modules on the acceptance path:
`probe_external_integer_bridge.py` (the certificate parser, which also asserts full D4
invariance on every read), `predicate_partition.py` (the dispatcher
`replay_capture_record` through which direct proofs are replayed), and
`certify_n21_near_axis_path.py` (`sign_on_open_interval`, the exact remainder test that
`Signs.replay` relies on); it lists `near_axis_projection.py`, which the replay never
imports. All 29 modules are hash-bound by the manifest and by every stage’s
`inputs.json`, so nothing is unpinned; the appendix’s `Code:` lines are just incomplete
as a map of what runs.

### F8. The runner replays a certificate tree; it does not decide the cover (note, `s(21)`)

The proof object is the 2.54 GB tree plus the point file, and the runner is a checker of
that tree in the proof-carrying sense; it searches nothing and cannot certify the cover
from `n21-original.txt` alone.
That is a legitimate design, and it is why the replay costs four CPU-hours rather than
the campaign’s. A from-scratch second decision is not available cheaply:
`zmx2 --d4 --pair-points` on the normalised cover leaves 238 boxes uncertified at its
depth limit (§5), at the same corner-tile germ whose exact minimum is `1.00105`;
`zeromargin.py`, with its `CHAIN` primitive, is the remaining candidate and was not
tried here. The companion mixed-cover route is the method-distinct evidence for the
*value* (§7).

### F9. Environment (note, `s(21)`)

`numpy` and `scipy` are imported at module level by `predicate_lp_capture`,
`predicate_conflict` and `predicate_branch` and must be installed although the replay
never calls them; `python -O` is refused; CPython 3.14 works (12 tests, the sweep, the
generator). The receipts carry the author’s absolute paths
(`/Users/Hosono_1/SquarePacking/…`) as identifiers, mapped by `portable_replay.locate`.
The bundle needs 2.5 GB unpacked plus temporary space, and the M1 timing (8,577 s, two
workers) should be scaled up on slower hardware.

### F10. The runner’s lemmas are unformalised, and the audit scripts in the tree cannot run (note, `s(21)`)

`PROOF-LEMMAS.md` is a written argument and `lemma-code-map.json` pins it to code; no
part of it is in Lean, unlike upstream’s point primitives.
The retained
`n21_L5_refit29_{soundness_review,scoped_gate,theorem_audit,binding_scope_review}/`
scripts reference files that are not distributed (`review.md`, `terminals.json`,
`review-bindings.json`, the original worker outputs), so they document the campaign’s
own audits without being runnable from the bundle; the distributed acceptance is
`verify_portable.py` alone, which is what the README says.

## 7. The Rung, Method Classes, and the Replay

Under [`epistemics.md`](../../../epistemics.md):

- **`s(45) = 7`, point-only route.** `V4` (interval-certified: `zmx2`’s enclosures with
  exact integer acceptance; exact data checks) on a passing replay; `C1` now, this
  review being the qualifying read; `C3` once the intake lane records a passing local
  `verify.sh`. It is the *same implementation* as one of the two checkers of the mixed
  route, so it adds a second certificate for the value under an existing method, not a
  second method: the `C4` position for `s(45) = 7` is the one the companion review
  describes, `zm_mixed.py` against `zmx2` on Evan Daniel’s cover.
- **`s(21) = 5`, point-only route.** `V4` (exact-algebraic) on a passing replay; `C1`
  now; `C3` on a passing `verify_portable.py`. Its method class is distinct from both of
  upstream’s: an exact rational replay of retained local certificates, namely point
  witnesses by quadratic and quartic Bernstein containment, LP-dual residual bounds over
  a closed predicate relaxation with verified conflict cuts and binary branch trees,
  weight transfer from a replayed predecessor, and a symbolic near-axis band from an
  exact fixed-angle arrangement sweep, joined by closed partitions and stratified
  coverage; against `zm_mixed.py`’s exact subdivision with chord lemmas and `zmx2`’s
  interval pair dynamic programme.
  The measures differ too (points only, against points and segments).
  With one `C3` entry from each route the value `s(21) = 5` meets the structural `C4`
  predicate, and substantively the routes share only the pose-space architecture and the
  closed-cover reduction; the composition note should say so.
- **Neither is `V5`.** The capture computations are not proof-assistant checked, and a
  compound claim takes the rung of its weakest load-bearing part.

**Credit.** wand125’s (the repository author’s; the `s(21)` bundle says its code was
developed with Codex and that its own executions are not third-party verification).
Both READMEs and `PUBLICATION.md` state that Evan Daniel published each value first
(`s(21)` bundle commit `086a129a…`, 2026-09-27) and claim no priority; the `s(21)`
support is his `s21_lower_4.9950.txt` scaled by `1001/1000` (hashes and the ordered
comparison in `support-provenance.json`, confirmed by `inspect_certificate.py`), the
`s(45)` weights came from an LP iterated against `zmx2`’s own weak poses, and his MIT
licence is retained in `UPSTREAM-LICENSE.txt`. The weighted-cover reduction and the D4
fold are his Lean lemmas; the `s(21)` runner and its lemma write-up are wand125’s.

**What the replay lane must check.**

- `s(45)`: from a copy of `point_n45_L7/`, with `cargo` (Rust `≥ 1.86`) on `PATH`,
  `sh verify.sh <new directory> <threads>`. The script clones from GitHub; on a machine
  without network, edit the scratch copy’s `UPSTREAM_URL` to a local mirror, since the
  SHA-256 check of `zmx2.rs` pins the source regardless of origin.
  Expect
  `COVER_OK points=12645 total=12666371418707823/281474976710656 (44.999991000011) < 45,
  D4-invariant`, `D4: measure invariant under x->s-x and x<->y (exact)`, a `VERIFIED-D4`
  line, `ROOTS_OK 4900 roots, uncertified 0, capped 0`, and `N45_POINT_COVER_VERIFIED`;
  record the rustc version, the binary hash, and the census (upstream and here:
  1,295,460 boxes, depth 38; 204 s on eight threads upstream, 1,749 CPU-s on one thread
  here). Optional: `zmx2 cert cover.txt --full --pair-points` for the unfolded statement
  (39,200 roots).
- `s(21)`: in a venv with `numpy` and `scipy`, from a copy of `point_n21_L5/`:
  `python inspect_certificate.py` (expect `EXACT_CERTIFICATE_DATA_CHECKED`),
  `python unpack_bundle.py` (expect `BUNDLE_BYTES_VERIFIED`, 75,130 files; 2.5 GB plus
  temporary space), then `python verify_portable.py --workers 2 --out <new directory>`
  without `-O`. Expect four `*-exit.json` with exit 0, `linkage.json` with
  `PORTABLE_COMPLETE_REPLAY_LINKAGE` and `minimum_frontier_leaf
  249987033421/250000000000`, and `result.json` with `FRESH_ALL_DOMAIN_REPLAY_VERIFIED`,
  `root_count 5000`, `sieve_count 8758`, `frontier_count 31678`, `excluded_count 7052`,
  `threshold 249987/250000`, `mass 2624862500021/125000000000`, `strict_gap
  999979/125000000000`. Upstream took 139 s (root), 412 s (sieve) and about 7,900 s per
  frontier shard on an M1; set the wall ceiling above twice that.
  The result does not depend on the worker count.
- Both: register the certificate hashes, the checker identities (`6b7f0f79…` and the
  bundle manifest `bb2883c5…`), and this review as the audit record.

## 8. What Remains Unchecked

The complete replays (both).
The Lean build of the overlay (toolchain `v4.33.1`, Mathlib cache), and therefore the
axiom report; the overlay was checked as text and its data regenerated.
The contents of the 75,130 retained proof objects, which only the replay exercises; this
review checked the code that reads them and the mathematics it applies.
`zmx2`’s internals beyond what §3.3 and the companion review cover, in particular its
chord enclosures, which a point-only cover does not use.
Any method-distinct decision of the `s(45)` point cover (F3) or of the `s(21)` point
cover (F8). The upstream `s(21)` bundle’s own replay status is the companion review’s
business, not this one’s.

**Licence.** MIT (`LICENSE` at the repository root, copyright 2026 wand125); Evan
Daniel’s MIT licence is retained as `point_n21_L5/UPSTREAM-LICENSE.txt`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
