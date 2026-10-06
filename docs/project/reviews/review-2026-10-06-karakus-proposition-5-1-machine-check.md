# Review: the Machine Check of Karakuş’s Proposition 5.1 (d7f2c6186)

Reviewed on 2026-10-06 by an AI agent (model claude-opus-5-5, tbd-strong tier). The review
ran in a separately prompted lane that shares no context with the lane that wrote the
checker, at commit d7f2c6186, in the detached worktree `/home/user/squares-lanes/r6-review`.
I modified nothing in the repository. Scratch code and its outputs are under
`/tmp/claude-0/-home-user-squares/1fb2d4ab-96d0-5b24-9e36-157598bdbf06/scratchpad/r6-review-work/`.

## Verdict

**Accept with non-blocking findings.** The checker decides two reduced inequalities. Its
docstring’s hand reductions, which I re-derived, turn them into Proposition 5.1 exactly as
the paper states it: every a ≥ 2, b ≥ 3, every closed square of side 1 < λ ≤ 101/100,
μ(S°) > 1. I found no gap in the case split, the tangency conventions, the point-row
argument, the reflection or the central symmetry. Every enclosure and rule is sound: I
reviewed each by hand and found no violation over 6,739 boxes sampled against my own exact
geometry. I also proved the reduced inequality myself in a few lines. The certificate
replays, the tests pass, and every mutation I tried was judged consistently with my own
exact evaluator: the checker refused every false variant and accepted nothing false. The
findings concern what the checker’s self-checks can detect, how precisely the docstring and
receipt state the trust boundary, and one test’s cost. If the check were registered as
evidence, it would support V3/C3 for both T-083 and T-084, and I argue below that C3 is
honest.

## What I Read

- `AGENTS.md`, and `epistemics.md` from the Four Classifications through Status.
- Karakuş, arXiv:2609.37410v1: Section 5 in full, plus Sections 1, 2 and 6, from the
  retained cleaned copy. I checked the measure’s definition and Proposition 5.1 against the
  retained `pdftotext` extraction (lines 365–402). The PDF’s SHA-256 is `39ae2ae4…6513`, the
  recorded digest.
- `packing/devtools/check_karakus_strip_measure.py` (887 lines) and
  `packing/tests/test_karakus_strip_measure.py` (223 lines), in full, plus every field of
  the receipt.
- Register context: T-083, T-084, T-085, T-006 and T-039 in `results.yaml`, and
  E-karakus-strip-lower, E-nagamochi-lemma1-counterexample, E-bentz13-figure2-audit and
  E-n017-guzhou-r052-source-replay in `evidence.yaml`. Also the Proposition 5.1 section of
  `review-2026-10-02-nagamochi-lemma1-karakus.md`, the machine-entry rules in
  `packing/frontier/README.md`, and the quick-lane ceilings in
  `packing/src/sqpack/cli/validate.py`.

## What I Ran

All commands ran from `packing/` in the worktree, under `nice -n 10`, on Python 3.14.7. The
first `uv run` created the worktree’s `.venv`.

| Command | Result |
| --- | --- |
| `uv run --frozen --all-extras --group dev python -m devtools.check_karakus_strip_measure` | Exit 0. “replayed the retained certificate, every leaf re-decided: part A 5939 leaves, part B 1 leaves”; “the fresh search, identities, spot checks, corollaries and controls match it”; part A `{'margin': 5933, 'area': 2, 'corner': 4}`, depth 34; 20 identities, 212 spot checks, 301 values of (6.1), 3 controls refused; 6.0 s CPU. |
| `uv run --frozen --all-extras --group dev python -m pytest -q tests/test_karakus_strip_measure.py` | 211 passed in 6.23 s. With `--durations=6`, the slowest call is `test_the_tool_replays_and_matches_its_receipt` at 3.59 s. |
| `ruff check` and `ruff format --check` on both files | “All checks passed!”, “2 files already formatted”. |
| `basedpyright` on both files | 0 errors, 0 warnings, 0 notes. |

## The Reduction Against Proposition 5.1

**What the trees decide.** A square’s pose is (τ, λ, u). The orientation is θ = 2 atan τ,
with τ in [0, 5/12], which passes tan(π/8). The side is λ in [1, 101/100], and u is the
height of the line y = 1 above the lowest vertex. Write m = min(cos θ, sin θ),
M = max(cos θ, sin θ), p = mM and h = m + M. Write C(v) for the area below relative height
v and w(v) for the open chord there, and let E(v) = −C(v) + w(v)/2.

- **Part A:** λ² + E(u) + ½[p < u − 1/5 < λh − p] > 1 for λ > 1 and 0 < u ≤ 1.
- **Part B:** E(v) ≥ 0 for 0 < v ≤ 3/7.

**Why that is Proposition 5.1.** I re-derived every step of the docstring’s reduction.

- **The bound F.** S ⊆ R gives S° ⊆ (0, a) × (0, b), so S° meets L− in its whole open chord.
  An open chord at y = 4/5 longer than one lies in (0, a) and contains an integer j with
  1 ≤ j ≤ ⌈a⌉ − 1, which is a point of W. Hence μ(S°) ≥ F. Neither a ≥ 2 nor the second
  row is needed for this.
- **The four cases, by which strip lines meet S°.** The open square is convex and connected,
  so a line that misses it leaves it on one side.
  - *Neither line meets S°:* the square cannot lie below y = 1 or above y = b − 1, because
    its height λh exceeds 1 and S ⊆ [0, b]. So it lies in H and F ≥ λ².
  - *Only y = 1 meets S°:* this is z0 ≥ 0 written as 0 < u ≤ 1, and S° lies below
    y = b − 1. F is exactly Part A’s left side.
  - *Only y = b − 1 meets S°:* the reflection y ↦ b − y maps R, H, the lines and the rows
    to themselves, and maps this case to the previous one.
  - *Both lines meet S°:* the two cut heights differ by b − 2 ≥ 1. Both depths, u1 and
    λh − u2, are therefore below λh − 1 ≤ 101√2/100 − 1 ≈ 0.42836 < 3/7. Central symmetry
    gives C(λh − x) = λ² − C(x) and w(λh − x) = w(x), so F ≥ λ² + E(u1) + E(λh − u2), and
    Part B applies.

  This is the only place that b ≥ 3 enters, and it covers b = 3.
- **Tangency.** The open chord is zero on a tangent line, including the θ = 0 line along an
  edge. Open and closed chords differ only there, and every case above has u strictly
  inside (0, λh). A point of W on the square’s boundary is not counted, and the row test
  requires the chord to be strictly longer than one.
- **Orientation.** The profile depends only on |cos θ| and |sin θ|, so [0, π/4] suffices,
  and the reflection x ↦ −x is covered by the same symmetry.
- **The side ceiling.** The checker uses 101/100 only in Part B, and through (10/7)² ≥
  2(101/100)². My own proof (Independent Checks, item 1) shows that Part A holds for every
  λ > 1 and Part B up to λ = 3/(2√2) ≈ 1.0607. In the paper, the ceiling is used in
  Lemma 5.2(i), in the top-height bound z_c + λ/√2 < 2, and in (5.8).

**The proof route.** The checker’s decomposition differs from the paper’s. The paper splits
by centre height and uses Lemma 5.2 and (5.8); the checker splits by which lines meet the
open square and never evaluates Lemma 5.2. It confirms Proposition 5.1’s statement, not the
paper’s proof of it (finding 4).

## Soundness of the Enclosures and Rules

- **τ and monotonicity.** On [0, √2 − 1], m = s and p, h rise while M = c falls. Past that
  point m = c, and p, h fall while M = s rises. The sympy identities factor each derivative,
  and the signs follow on [0, 1]. A straddling interval uses min/max endpoint values,
  together with 1/√2 bounds from rational bounds on √2. All of this is correct.
- **Per-cell lower bounds.**
  - Cell L uses v(2α − v)/(2p): its first branch divides a non-negative numerator by p1,
    its concave branch takes the endpoint minimum, and −10⁹ is valid because E ≥ −λ².
  - Cell P chooses l0/big1 or l1/big0 by the sign of x.
  - Cell T clamps g to non-negative values below l0·h0 − min(v1, l1·h1) and divides by p1.

  The cell-membership tests are necessary conditions, and every clamp bounds the cell’s
  true range. All of these are sound.
- **The point-row rule.** p1 < v0 − 1/5 and v1 − 1/5 < l0·h0 − p1 imply the row condition at
  every pose in the box, and for λ > 1 that condition is equivalent to a chord longer than
  one. This is sound.
- **Margin and area.** These are sound. A box that includes λ = 1 is sound because each
  bound needs to hold only at λ > 1.
- **Corner.** By hand I re-derived 2MΦ = K0 + K1δ + K2δ² with
  K0 = (2β − 1)M + h + 2α − 2 and 2p(F − 1) ≥ T0 + T1δ + T2δ². At α = β = ½ these reduce to
  K0 = h − 1 and T0 = (h − 1)²/2, with K1, T1 > 0. They are strictly positive for δ > 0,
  which is the right strictness argument, since F − 1 vanishes with λ − 1 at θ = 0, u = 1.
  Each premise the derivation uses is checked: u ≤ 1, W = 1, and no cell L.
- **The split and the replay.** The split is deterministic, and the preorder walk matches
  the search’s stack order. My own re-implementation of the bisection reproduced a partition
  whose leaf volumes sum to exactly the root’s.
- **The sympy identities.** All 20 are correct statements of what the rules use.

## Independent Checks

`mu_exact.py` is my own exact evaluator. It imports nothing from the repository. It builds
each square from a rational rotation and computes μ(S°) directly: the area clipped to
1 ≤ y ≤ b − 1, the open chords on both lines, and the points of W strictly inside. The
abscissa is chosen adversarially, the exact minimum over the finitely many critical shifts.
`mutations.py` and `enclosure_check.py` import the checker to drive it, but every value they
compare it against comes from `mu_exact.py`.

1. **An analytic proof of the reduced claim** (`analytic_check.py`: 11 sympy identities and
   5 rational inequalities, all passing). Take θ ∈ [0, π/4], m = sin θ, M = cos θ, and let R
   be the row indicator.
   - *(A1)* u − 1/5 ≤ 4/5 < √2 − ½ ≤ h − p ≤ λh − p, so R = [u − 1/5 > p].
   - *(A2)* For u ≤ λm, F ≥ λ² + u(1 − u)/(2p) ≥ λ².
   - *(A3)* For λm ≤ u ≤ λM, take the two values of R in turn. If R = 0, then
     E ≥ (λ/M)(3/10 − m(M − ½)) > 0, because m(M − ½) ≤ ¼ when m ≤ ½ and
     m(M − ½) ≤ (√3 − 1)/(2√2) < 0.259 otherwise. If R = 1, then
     2M(F − 1) ≥ G(λ) = (2M + m)λ² − λ − M, with G(1) = h − 1 ≥ 0 and G′ > 0.
   - *(A4)* For λM ≤ u ≤ 1, M(1 − m) ≥ (√2 − 1)/2 > 1/5 gives R = 1. Then
     2p(F − 1) = g² + g − p > (h − 1)²/2 ≥ 0, with g = λh − u > h − 1.
   - *(B)* Depths at most ½ < λM lie in cells L and P, where E ≥ 0. So Part A needs no
     ceiling on λ, and Part B holds up to 3/(2√2).
2. **An exact adversarial search** (`search_exact.py 200`). The grid covers seven containers,
   including (2, 3) and (2, 301/100), 46 orientations up to 5/12, 4 sides from 1 + 10⁻⁴ to
   101/100, and 201 centre heights plus the critical heights. Result: 271,932 squares, of
   which 27,511 are cut by both lines, all with μ > 1. The least is μ = 1.000150010
   = 1 + (λ − 1)(λ + ½), at the axis-parallel square of side 1.0001 standing on y = 0. The
   least (μ − 1)/(λ − 1) is 1.5001. This took 152.1 s of CPU.
3. **The two-line identity on explicit squares** (`both_cut.py`). On 4,313 squares cut by both
   lines, with b ∈ {3, 301/100, 31/10}, the area-and-line part of μ equals
   λ² + E(u1) + E(λh − u2) exactly, and both E values are non-negative. The deepest cut was
   0.421692, below 3/7.
4. **Every leaf of the retained certificate** (`leaf_sampling.py 4`). My own bisection walked
   the tree: 5,939 leaves whose volumes sum to exactly 1. I scored 47,504 poses in those
   leaves (the box corners with λ pulled just above 1, plus random points) on explicit
   squares, and all had μ > 1. The least (μ − 1)/(λ − 1), 1.5, falls in a corner leaf at
   τ = 0, u = 1. This took 39.7 s of CPU. An earlier attempt with a container ten wide was
   too slow, and I stopped it at 8 min 51 s of CPU, before it printed anything.
5. **Enclosure soundness** (`enclosure_check.py`, 46.8 s of CPU). The samples covered the
   5,939 leaves and 400 random boxes in each part, 6,739 boxes in all, with poses at the
   corners and inside. They found no case of e_lo > E(pose), no row claimed where the chord
   is at most one, and no m, M, p or h outside its enclosure. Four deliberately unsound
   variants are discussed under finding 1.
6. **Mutations, judged by the checker and by my evaluator** (`mutations.py`, plus
   `probe_offset.py` for one case). The grid has containers (2, 3) and (3, 6) and least μ
   over 23 orientations, 3–4 sides and the centre heights.

   | Mutation | Checker, part A / part B | Reviewer’s least μ |
   | --- | --- | --- |
   | Karakuş’s measure | accepted (11,877 nodes) / accepted | 1.000150 |
   | Row at 19/20, 23/25 or 13/20 | refused (depth limit) / accepted | 0.572, 0.585, 0.889 |
   | Row at 7/10 | refused (depth limit) / accepted | 1.000150 on the grid; 0.99982 by a targeted probe at τ = 3817/10000 |
   | Row at 9/10, 17/20, 79/100 or 3/4 | accepted / accepted | 1.000150 each |
   | Point mass 499/1000, or line density 499/1000 | refused with a witness, F = 0.999998408, which my evaluator reproduces exactly / accepted | 0.99915 |
   | (line, point) = (3/5, 2/5) or (11/20, 9/20) | accepted / accepted | 1.000160, 1.000155 |
   | (line, point) = (2/5, 3/5) | refused (depth limit) / refused | 1.000140 |
   | Side ceiling 106/100, Part B depth ½ | accepted / accepted | 1.000150, and true by item 1 |
   | Side ceiling 107/100, depth 52/100 | accepted / refused (depth limit) | 1.000150 |
   | Part B depth 2/5, or τ ceiling 2/5 | premise refused | not applicable |

   Every acceptance agrees with my evaluator, and every claim my evaluator refutes is
   refused. The 79/100 row lies just outside Lemma 5.2’s range, which is sufficient but not
   necessary.

   The (2/5, 3/5) refusal is incompleteness, not unsoundness. The corner rule bounds
   K0 = 0.2M + h − 1.2 with M and h decoupled, which loses the bound at θ = 0. For Karakuş’s
   weights K0 = h − 1 and nothing is lost.

   The 107/100 refusal is correct for Part B’s sufficient statement: E < 0 at θ = 0 for
   v > ½.
7. **A random continuous search** (`search_float.py`). Among 150,000 squares, 57,343 of them
   cut by both lines, the least (μ − 1)/(λ − 1) is 1.982, and an exact re-score of that pose
   is 1.0104. This took 4.6 s of CPU.

## Rung Assessment

**The evidence entry.** Registered, it would be a `lower-bound` entry over T-083’s scope:

- `method: exact-algebraic`, since no arithmetic rounds;
- `origin: audited-here`, a first-party machine audit of a published proof, as for
  E-bentz13-figure2-audit;
- the receipt as `certificate`, the default command as `replay`, and `replay_status: passed`;
- a new first-party verifier that decides the claim;
- `relationship_to_generator: independent-implementation`, with an `independence_record`
  (the source publishes no code, and the docstring says the checker was written from
  Section 5 alone);
- the test file as the control path.

**Verification: V3, unchanged.** The published proof and this certificate each meet V3. V4
needs two retained adversarial AI reviews by distinct reviewers whose latest verdict
accepts, and a human oversight record that checks the trust boundary, the certificate’s
meaning and the AI findings. Neither exists for the machine check. This review could be
one of the two.

**Confirmation: C3 for both.** The entry meets C3’s literal predicate. T-083 takes C3
directly. T-084 is an equality whose upper half, the grid, is already C3, and it takes the C
of its lower half, so C3. The status of both moves from *reviewed* to *confirmed,
independently re-implemented*. Both claims’ sentence “is not machine-checked”, T-084’s
composition note and both `next_rung` fields would need rewriting.

**What remains read.** The following load-bearing steps stay outside the machine:

1. The chord profile (5.3) as the tilted square’s chord function. It is standard; the
   checker spot-checks it exactly at 212 poses and the tests at 195.
2. μ(S°) ≥ F: S° ⊆ (0, a) × (0, b), and an open interval longer than one contains an
   integer in range.
3. The four-way split by connectedness, the reflection, and the central-symmetry identity.
4. The soundness of the rules as coded. This is a review obligation, discharged above.
5. Theorem 1.1’s scale-and-sum: additivity over disjoint open squares, and
   μ(R) = ab − Δ(a).
6. For T-083, Corollary 6.2’s step from ν(t, t) < N to s(N) ≥ t. The algebra is checked at
   all 301 values of N.
7. For T-084, Corollary 6.1 at a = b = k ≥ 3, where Δ(k) = 1.

**Why C3 is honest.** The machine decides the one step that quantifies over a continuum of
poses, including the corner where the margin vanishes. Each read step is a one-line fact
of plane geometry, measure additivity or arithmetic, and none estimates anything over the
pose space. Every branch of the case split is closed by the machine or by λ² > 1.

The register’s own practice draws the same line. T-039 and its n = 17 siblings stand at C3
on exact certificates whose route from certificate to bound is read: upper semicontinuity,
disjoint cores and the budget. By contrast, T-006’s next_rung says Bentz’s route reaches C3
only by machine-checking Sections 3.1–3.2. There, a geometric case analysis stays in prose
(E-bentz13-figure2-audit is `derived-structure` for that reason). Here none does.

This lane also checked steps 1–3 independently: on explicit squares (items 2–4), with the
exact two-line identity (item 3), and with a separate proof of the reduced claim (item 1).
C3 is as far as the evidence goes. Rung 4’s human `certificate-meaning` attestation is
precisely the check on steps 1–3.

## Findings

1. **The self-checks cannot detect an unsound rule.** Non-blocking: no shipped rule is
   unsound.
   - *Evidence.* I patched four unsound variants into the module in turn: cell T dividing
     by the least p, the row rule using the least p, the margin rule using the largest λ,
     and the corner rule skipping its W = 1 premise. Each still certified parts A and B, and
     each still refused all three controls. The controls mutate only the measure, so they
     show that false claims are refused, not that the rules are sound. My enclosure test
     caught the first two variants (120 and 203 violations) and found none in the shipped
     rules.
   - *Fix.* Add a quick test that samples exact poses (from `point_value` or the polygon
     scorer) in every retained leaf and in random boxes. It should assert e_lo ≤ E,
     w_lo = 1 ⇒ a chord longer than one, enclosure containment, and each rule’s own
     inequality (margin: λ² + E + β·R ≥ l0² + e_lo + β·w_lo; corner: 2M(F − 1) ≥ k0 + k1·δ).
     Keep at least one unsound variant as a negative control that this test must reject.
2. **The docstring misstates the trust boundary.** Non-blocking.
   - *Evidence.* It calls the reduction “by hand, and the only part that is”, and then says
     the scale-and-sum “is also by hand”. The chord profile itself, the connectedness
     argument, and the soundness of the coded rules are also outside the machine’s decision.
   - *Fix.* Replace the phrase with an enumerated list of the hand steps (steps 1–7 above),
     and say that rule soundness is a review obligation.
3. **The receipt does not say what the trees decide.** Non-blocking.
   - *Evidence.* Its `statement` is the geometric proposition, and no field records the
     Part A and Part B inequalities or the hand premises that connect them to it.
   - *Fix.* Add `decides` and `premises` fields, so that the evidence entry’s assumptions can
     be copied from them, as E-n017-guzhou-r052-source-replay’s are.
4. **The checker’s proof route is not the paper’s, and nothing says so.** Non-blocking.
   - *Evidence.* The paper splits by centre height and uses Lemma 5.2 and (5.8). The checker
     splits by which lines meet S° and never evaluates Lemma 5.2. A reader of “written from
     the paper’s Section 5” could take Lemma 5.2 as checked.
   - *Fix.* Add one sentence each to the docstring and to the future entry’s limitations:
     the statement of Proposition 5.1 is confirmed by an independent decomposition, and
     Lemma 5.2 and the paper’s three strip cases remain read, no longer load-bearing.
5. **The replay test is above the quick lane’s marking threshold.** Non-blocking.
   - *Evidence.* `test_the_tool_replays_and_matches_its_receipt` measured 3.59 s of call
     time on a shared machine. `validate.py` marks tests at 2 s and backstops at 12 s, and
     records runner inflation of up to 3.7×.
   - *Fix.* Mark it `slow`. The leaf-by-leaf replay stays quick in
     `test_the_retained_trees_re_decide_leaf_by_leaf`, at 0.46 s. Alternatively, split the
     fresh search, the identities and the controls into separate tests.
6. **Two corollary checks cannot fail.** Non-blocking, low.
   - *Evidence.* `k*k - (k + 1 - k) == n` with `n = k*k - 1` is k² − 1 = k² − 1. The bracket
     tests for (6.1) reduce to k² < N ≤ (k + 1)² − 1 and N − k ≥ 6, which hold by the choice
     of k for every nonsquare N ≥ 8. They restate the paper’s algebra correctly but carry no
     evidence beyond the sympy root identity, which is the pattern of D-518.
   - *Fix.* Say so in the docstring and the receipt, or drop the T-084 line. Leave the
     per-case values to `check_nagamochi_bounds`, which already reads Karakuş’s (6.1).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
