# Review: wand125’s Checker on ValidTilt9 (`T-081`), Lane R3

*Written 2026-10-06 by an AI agent (model `claude-opus-5-5`, tbd-strong tier), separately prompted for lane R3 of the 2026-10-06 intake round of jlevy/squares. It worked in a detached worktree at `2d0fb83ba`, edited and committed nothing, posted nothing, and started no sub-agents.*

**Verdict.** The run can be recorded on `T-081` as reported evidence: a second, separately written exact checker reports deciding ValidTilt9. A future full replay of it would count as a confirming, independently re-implemented decision of ValidTilt9.

- **Statement.** What the checker certifies, as run, contains ValidTilt9 exactly as the Lean defines it. Centres cover $[0, 9/2]^2$ and $u$ covers $[0, 7/16] \supset (0, \sqrt2 - 1]$. The admissibility test and the rotation $c + R_\theta[-\tfrac12, \tfrac12]^2$ match. The cover is read with every file entry counted, the 16 doubled segments included, and the polygon has density 1.
- **Method.** Every lemma premise that the 2 October review found met on the k = 7 cover is also met on the box-9 cover and in this run. The fixes at `da469ec` are correct line by line. Neither the v2 hand-off nor the options changed mid-run can put an uncertified pose into a recorded leaf.
- **No blocking defect** was found in the method or the statement.
- **What is open is evidential.**
  - The 9.5 million leaves rest on the source's run. Its record checker re-certifies only 2,300 of them.
  - Which code and options each root ran under is stated in prose and cannot be checked from the published files.
  - The read log can only declare independence. Both programs were made with Anthropic Claude models.
- **Rungs.** The run changes neither of `T-081`'s rungs (V0/C1). It does make one sentence of `T-081`'s evidence stale and one clause of its `next_rung` incomplete, and it must not be recorded with a confirming origin.

## What Was Read and Run

**Read, in full unless stated:**

- In the 2026-10-06 wand125 packet:
  - `README.md`;
  - `release/`: `MERGE.md`, `NOTES_machine1.txt`, `NOTES_machine2.txt`, `check_tilt9.out` and `records.sha256`;
  - `valid7-independent-check/`: `DESIGN.md`, `README.md`, `READ_LOG.md`, `versions/VERSIONS.md` and `verify_tilt9.sh`;
  - every line of `src/cover.py`, `tier_a.py`, `solver.py`, `rf.py`, `tier_b.py`, `tier_b2.py`, `run_all.py` and `check_record.py`.
- Diffs: `diff` of `src/run_all.py` against `versions/V2/run_all.py`; of `src/tier_b2.py` against `versions/V2/tier_b2.py`; and `diff -r` of `src/` against the 3 October packet's `src/`.
- The 3 October wand125 packet `README.md`, and the 2 October review (`docs/project/reviews/review-2026-10-02-valid7-independent-checker.md`).
- Lean:
  - `ValidSplit.lean` §1, with `ValidTilt`, `exists_u_of_theta_pos` and `valid_of_tilt_axis`;
  - `ValidSplit9.lean` in full;
  - `coord`, `sq` and `sqInt` in `Basic.lean`, and `box` in `Chord.lean`;
  - `MixedCover`, `measure`, `segMeasure`, `segFrac`, `areaMeasure` and `areaFrac` in `MixedMeasure.lean`;
  - the `box9Cover` and `Valid9` section of `Bentz4.lean`;
  - the retained receipts `receipts/lean/build_bentz4.log` (head) and `axioms_bentz4.log`, which print the elaborated `ValidTilt`.
- Daniel's side:
  - k2m4 `README.md` and `verify.sh`;
  - `qx2_zm/run_k4x_k008_leaves.out`;
  - the imports of the four `qx2_zm/checker/` files;
  - `s12/CREDITS.md` §Provenance.
- In this repository: `T-081` in `packing/frontier/results.yaml`; the three `E-k2m4-evand-*` entries in `evidence.yaml`; `V-wand125-valid7-checker` in `verifiers.yaml`; `epistemics.md` (Verification, Confirmation, Which Code Confirmed It, Review Records, Scope and Composition); and `derive_confirmation`, `derive_verification` and `_machine_proof_shaped` in `packing/devtools/check_results.py`.

**Ran.** Everything ran in memory with the brief's interpreter (`…/r3/venv/bin/python`, CPython 3.14 with python-flint 0.9.0), under `nice -n 19`, single-threaded, with `-I`. The cover was read from the 3 October evand packet's `.txt.gz`. Total CPU was under a minute.

1. **Cover facts, using wand125's `cover.py`.**
   - SHA-256 `4151d7c4…27801`, 48,380 bytes.
   - $s = 9$, 0 points, 2,076 segments, all of length 1/5 and none of zero weight.
   - 2,060 distinct segment geometries. 16 occur twice, each time with different weights; none is repeated with the same weight, and none appears reversed.
   - One polygon $[14/5, 31/5]^2$, mass $289/25$, area $289/25$, **density 1**.
   - Total $3835229774429/50000000000$, so $81 - \text{total} = 214770225571/50000000000 = 4D$.
   - The segment densities are D4-invariant.
   - No segment midpoint lies strictly inside the polygon.
2. **Mass cross-check.** `solver.point_mass` against my own evaluator, written directly from the Lean definitions (`coord`, `sq`, the parametric `segFrac` over every file entry, and `areaFrac × gw`): equal, exactly, at 40 poses (4 chosen, 36 random). The mass at $+u$ and $-u$ differs at an off-axis pose (0.8313 against 0.9098), so the rotation sign was actually exercised.
3. **The fixed primitives.**
   - `nonneg_open(−(u − ½)², (0, 1))` returns False, which is D-1 fixed.
   - `rf.nonneg_on(u(u − 1), 0, 2)` returns False, which is D-2 fixed.
   - `(u − ½)²` on $(0, 1)$ returns True; $u^2 - 1/9$ on $(0, 1)$ returns False.
   - `wmin(0, 7/16) = 1` and `wmin(13/32, 7/16) = 431/305`.
4. **Tier B on this cover.**
   - On boxes $[1/2, 21/40] \times [31/10, 25/8]$, $u \in (0, 1/32)$, and $[3/2, 61/40] \times [3, 121/40]$, $u \in (1/32, 1/16)$: `ok`, in 1.3 s and 2.2 s.
   - At $\theta = 0$ on the wall line $x = 1/2$, 35 of 161 centres on the $1/40$ grid have mass exactly 1. On the tight box $[1/2, 21/40] \times [319/80, 321/80]$, $u \in (0, 1/32)$, Tier B certifies the real cover.
   - A mutant with every segment mass scaled by $1 - 10^{-4}$ is **refused**, with the witness $u \approx 2.3 \times 10^{-4}$, $y = 319/80$, exact mass $0.99995$.

**Not run.** The release records were not downloaded: `gh` network calls needed an approval this session did not have. So the record headers, the per-root leaves and the option regimes were not inspected; their digests are pinned in the retained `release/records.sha256`.

**Housekeeping.** Importing `cover.py` in the first command, before I added `-B`, wrote `packing/resources/web/wand125-valid7-independent-check-2026-10-06/valid7-independent-check/src/__pycache__/cover.cpython-314.pyc` into the worktree. It is untracked, and I could not delete it without an approval I did not have. Delete it before any acquisition `--check` of the packet.

## 1. The Statement

**Lean.** The receipt `axioms_bentz4.log` prints the elaborated definition, which matches the source file:

```
ValidTilt m μ := ∀ c u, c.1 ∈ [0, m/2] → c.2 ∈ [0, m/2] → 0 < u → u² + 2u ≤ 1 →
                 sq c (2 arctan u) 1 ⊆ box m → 1 ≤ μ (sq c (2 arctan u) 1)
```

Here:

- `sq c θ 1 = {p : |coord₁| ≤ ½ ∧ |coord₂| ≤ ½}`, with $\text{coord} = R_{-\theta}(p - c)$, so `sq c θ 1` is $c + R_\theta[-\tfrac12, \tfrac12]^2$, a closed square.
- `box 9` is $[0, 9]^2$, closed.
- `box9Cover` is `fileCover` over the file's segments indexed by `Fin boxSegs.length`, so a segment listed twice counts twice. Each segment has mass $w/(2\cdot10^{12})$ spread by the push-forward of Lebesgue measure on $[0, 1]$. The one polygon carries `boxPolyW` spread uniformly by area.

ValidTilt9 is therefore: every closed unit square inside $[0, 9]^2$ with centre in $[0, 9/2]^2$ and $0 < \theta \le 45°$ has mass at least 1.

**What the run certifies.**

- **Region.** `MERGE.md` and the README give centres $[0, 9/2]^2$ at pitch 1/10 and $u \in [0, 7/16]$ in 14 bins: $45 \times 45 \times 14 = 28{,}350$ roots. `check_record.py --claim tilt` requires:
  - $U_0 = 0$ and $U_1^2 + 2U_1 \ge 1$; at $U_1 = 7/16$ this is $1.066 \ge 1$;
  - the root x-, y- and u-intervals each partition $[0, s/2]$, $[0, s/2]$ and $[U_0, U_1]$;
  - the roots to be exactly their product, each root once.

  The retained `check_tilt9.out` reports `RECORD OK` with 28,350 roots. The line counts in the packet README (23,941, 3,781 and 631) equal one header plus one line per root.
- **Admissibility.** `core_bound` and `box_min` clip the centre box to $[\text{lo}, s - \text{lo}]^2$ with $\text{lo} = (|\cos t| + |\sin t|)/2$. `tier_b2.certify` uses the same bound as an exact rational function of $u$. That is exactly `sq ⊆ box 9` for a square, closed at both ends, so no admissible square is dropped. Inadmissible poses are never claimed.
- **Rotation.** `tier_a.cs`, `solver.frame` and `outer_hull` use $\cos t = (1-u^2)/(1+u^2)$, $\sin t = 2u/(1+u^2)$, edge normals $(\cos, \sin)$ and $(-\sin, \cos)$, and vertices $R_t(\pm\tfrac12, \pm\tfrac12)$. That is `coord`'s convention, and the 40-pose check confirms it. Even the opposite sign would certify an equivalent statement, because the swap $x \leftrightarrow y$ maps $[0, 9/2]^2$ to itself and $\theta$ to $-\theta$, and `d4_box9` is kernel-checked. Still, the conventions agree.
- **Reading of the cover.**
  - `cover.load` appends every entry to a list.
  - `Tier A.mass_convex` de-duplicates by list index (the `seen` set), so both copies of a doubled segment count.
  - `solver.Local` sums densities per `(line, lo, hi)` key, and `point_mass` iterates over every entry.
  - The 16 doubled segments are therefore counted twice, as in Lean, and the exact equality with my Lean-semantics evaluator confirms it.
  - Segment mass is $w \times$ the parametric fraction on the closed square, which is `segFrac`. `validate` refuses zero-length segments, so no Dirac case arises.
- **Polygon.** The left half-planes of its directed edges, density $w/\text{area} = 1$; this is Lean's `areaMeasure` with `gw`.

**Against `qx2_zm.py`'s region.** `qx2_zm.py` covers $[0, 9/2]^2 \times u \in [0, 1/2]$ in 8 bins of 1/16 (16,200 roots). It labels leaves `AXIS` at $u = 0$ (Lemma Z) and `SYM` for $\theta_0 \ge 45°$, delegated to $\theta \mapsto \pi/2 - \theta$. Both regions contain ValidTilt9. wand125's run uses no symmetry and reaches 47.2° directly. Its `CORE` leaves also cover the face $u = 0$, which ValidTilt9 does not need. Neither run depends on the other's region.

**Does `RECORD OK` imply that the published leaves cover the region?** Yes for coverage: the roots are exactly the product grid, and `tiles()` proves each root's leaves are a bisection partition.

- I re-read `tiles()`, including a degenerate leaf counted on both sides of a cut. Any such list ends with a single leaf that differs from a non-degenerate node, so it returns False.
- Every root must have empty `uncert` and `cex` lists.
- `EMPTY` is re-decided exactly.

It does **not** imply that the leaves are certified:

- `CORE` and `TIERB2` leaves are re-decided only for the random sample: 2,000 of 6,565,165, and $15 \times 20 = 300$ of 2,940,689 at fixed seeds 1001 to 1015.
- `check_record.py` skips the header, so nothing binds a record to the cover's or the code's digests. The cover enters only through $s$, the `EMPTY` test and the sampled re-certifications (W-5).

## 2. The Method on This Cover

I took each premise the 2 October review named and checked it against box 9 and this run.

| Premise | Status on box 9 and this run |
| --- | --- |
| Side 9 | `cov.s` comes from the file and is used for `hi` in Tier A, `box_min` and Tier B. Met |
| One-sided $u \in [0, 7/16]$, with $u = 0$ as an end | Not needed. ValidTilt9 excludes $u = 0$, so no closure at $\theta = 0$ is required, and `ValidAxis9` is Lean's. Tier A at $u_0 = 0$ uses `wmin = 1`, which is sound. Tier B on $(0, b)$ is an open interval not containing 0, and `roots_in` and `guard_roots` strip the factor $u^k$ when an end is 0 |
| Slab next to $u = 0$ | Bins are $7/16/14 = 1/32 = $ `ub0`, so no u-split. The root's centre width $1/10 = $ `bwidth`, so a root touching 0 that Tier A cannot close goes whole to Tier B, then splits in the centre down to `bmin`. As in Valid7. Met |
| Tier B's open intervals, and the ends of a leaf | B1 and B2 are sound, and so is `chain`'s algebraic chaining. For a `TIERB2` leaf with ends $a < b$: the leaf proves $\mu \ge 1$ on the open pieces, and a pose at an end is the limit of admissible poses inside some leaf. On $(0, \sqrt2 - 1]$, lo$(u)$ increases with $u$, so $R(u) \supseteq R(u^*)$ for $u < u^*$, and a pose at a leaf boundary $u^*$ is approached from the leaf below. Above $\sqrt2 - 1$ the direction reverses, but ValidTilt9 needs no pose there. So the closed region is covered, though by an argument across leaves rather than DESIGN's "$m(u)$ continuous", which fails where $R(u)$ empties on one side (W-6) |
| Reach of `solver.Local` | $7072/10000 > \sqrt2/2$. Lines, breakpoints and polygons are kept if within reach of the box, and densities are built from all segments of a line, so the doubled segments add. Met |
| F2's one-polygon premise | One polygon. Met; the premise is still not checked in code |
| Point masses | 0 in the file. Tier B asserts it. Met |
| A1 and A3, an arc under $\pi$ | Boxes span at most 1/32 in $u$. Met |
| `wmin` | $\lvert\cos\rvert + \lvert\sin\rvert$ is concave on $[0, \pi/2]$, so the minimum is at an end, including across $\sqrt2 - 1$ in the last bin. Met |
| The `EMPTY` rule | `core_bound` returns `None` exactly when the clipped box is empty. `check_record` re-decides it with the same `wmin`, strict on both sides. Consistent and exact |
| D-4, degenerate `mass_convex` | Unchanged and still unreachable: centre width at most 1/10 and $u$-width at most 1/32, so the eroded core is a near-square |

**The `da469ec` code, line by line.**

- **`tier_b2.nonneg_open`.** It forms the odd-multiplicity part from `factor_squarefree`, which is squarefree and coprime. It isolates that part's roots in $(A.l, B.r]$ and rejects any root strictly inside $(A, B)$ by exact `alg_cmp`, where a rational endpoint root becomes `Alg.rat`. It then samples at `between(A, B)`, moving the sample while $p(s) = 0$, and accepts only on $p(s) > 0$. Without an odd root inside, $p$ has one sign off its zeros, so the test is **sound**, and it terminates because $p$ has finitely many zeros.
- **`rf.nonneg_on`.** It checks both ends, odd roots in $(lo, hi]$ less a root at $hi$, and an interior sample that is not a root. Sound. It loops forever if `lo == hi` and $p(lo) = 0$ (W-11), but nothing in the run calls it.
- **`exact_key`.** It keys on `('rf', str(n), str(d))` or `('q', str(Fraction))`. Distinct values cannot share a key; equal values in different forms only cost a duplicate. It is used in `certify`'s line de-duplication and in `edge_runner`'s two caches, which live inside one `run(u)`, so every cached RF shares its context's guards. Sound. `RF.__hash__` remains, but nothing in `tier_b2` keys on it now.

**The v2 hand-off and the mid-run option changes.** The diff against `versions/V2/run_all.py` is exactly the `--bmid-u`/`--bmid-w` clause, a disjunct of `handoff` restricted to boxes not touching $u = 0$, and its two options.

`solve_root` writes a leaf in only three ways:

- `EMPTY` when `core_bound` returns `None`;
- `CORE` when `core_bound(...) >= 1`, computed exactly;
- `TIERB2` when `tier_b2.certify` returns `ok`; exceptions are caught and treated as failures.

`--amin` and `--bmid-*` change only which of these is tried and when. A failure splits the box further or records it uncertified. So **no option or driver change can admit an uncertified pose into a recorded leaf**.

Resuming is root-atomic: one flushed line per finished root, a cut line is dropped on `--resume`, and a stray partial line would make `check_record`'s `json.loads` fail. Duplicate roots between machines would fail `RECORD OK`.

What the changes do cost is provenance and comparability (W-2, W-3):

- The record header is written only when a file is created, so `tilt9_a.jsonl`'s header names the v1 driver throughout.
- Which option regime each root ran under is not recorded per root. The notes give counts at each switch, but `tilt9_a` was restricted after the run, which shifts its line numbers.
- `MERGE.md`'s "sha256 as run" for `tilt9_a` equals the published value, although that file is a restriction of machine 1's record. So the unrestricted record is not published.
- Machine 1 started at 2026-10-03T22:55Z, seeded with pilot blocks run earlier. `da469ec`, the code `MERGE.md` says ran throughout, was committed at 23:14Z. The pilot roots' code version rests on the source's word.

## 3. Independence From `qx2_zm.py`

**What can be checked.**

- **Code.** No code is shared.
  - None of `qx2_zm`'s distinctive identifiers occurs in `src/`: `clip_bin`, `d4_roots`, `u_square`, `LineMass`, `lines_in_reach`, `Wnum`, `piece_bound`, `region_phi`, `QXChecker`, `REACH`.
  - The checking modules are byte-identical to `da469ec`'s (`diff -r` with the 3 October packet; only `run_all.py` differs). The 2 October review compared those with Daniel's code.
  - The only code new for this run is `check_record --claim tilt` (added at `da469ec`) and the v2 driver option. Neither is a geometric primitive.
- **Components and libraries.**
  - wand125: CPython `fractions` plus python-flint (`fmpq_poly`, `factor_squarefree`) and its own Sturm isolation.
  - `qx2_zm`: CPython `fractions` plus numpy, used for float screening and a float line-omission test with about $10^{-4}$ slack.
  - Shared: CPython and `fractions.Fraction`.
- **Shared constant and idea.** The reach constant $7072/10000$ is shared; it is harmless at any value above $\sqrt2/2$. So is the idea of arrangement-vertex values as rational functions of $u$. Both appear in the k2m3 README the earlier read log lists, and in lines 1–80 of the k2m4 README it lists now.
- **Cover generation.** One cover file, Daniel's, is the object both decide. wand125 generates nothing.
- **Statement.** It comes from Daniel's Lean, which was written to describe `qx2_zm`'s region. The statement is shared by construction; §1 checks that it is the right one.

**What `READ_LOG.md` can and cannot establish.** It is a declaration of what was read: at `0c243090`, k2m4 README lines 1–80, the `ValidTilt9`/`ValidTilt` definitions and doc comments, `coord`, `sq`, `sqInt` and the cover; not the checker programs, lemma documents, records or other Lean.

- It is consistent with every trace the files leave.
- It cannot establish what an author or agent saw outside the log: for example, the `square-packing-bounds` bundles of 1 October, whose `verify.sh` fetches and runs Daniel's `zm_mixed.py` and `zeromargin.py`, or an agent's own browsing.
- It cannot establish what the separately developed C4 checker the log mentions exchanged.
- Its dates read as JST: "2026-10-04" for a run that started 22:55Z on 10-03.

**AI assistance.**

- `c561dbb` ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. The two earlier commits, which hold every checking module, carry no statement either way; the absence of a trailer is not evidence of no assistance.
- Daniel's `CREDITS.md` says his work was "produced by Claude (Anthropic) in a single session under human direction".
- So both deciding programs were at least partly produced with models from one vendor's family.
- Separate prompting and a clean-room read log keep the *code* independent, and `relationship_to_generator: independent-implementation` is right for code.
- What they do not exclude is correlated error from a common generator: the same misreading of a statement, or the same blind spot in a lemma.
- This review is a third instance of the same family (W-8). The statement match in §1 and the exact evaluator check against Lean's definitions are the parts that do not depend on any model's reading.

## 4. The Trust Boundary

**wand125's checker trusts:**

- CPython and `Fraction`;
- python-flint 0.9.0's `fmpq_poly` and `fmpq`: arithmetic, `gcd`, exact division, evaluation, `factor_squarefree`;
- `cover.py`'s reading of mixed format v1, which matches Lean's measure (§1);
- for every leaf outside the sample, the driver's control flow and the run's honesty: the records carry `TIERB2` counts, not certificates;
- the hand transcription of the statement into `--claim tilt` and the driver arguments, checked in §1.

No floating-point value enters a decision.

**It decides:** every leaf (Tier A exactly; Tier B by symbolic execution and Sturm isolation); the tiling of the region and the `EMPTY` leaves (`check_record`); and nothing about the reduction, the axis face or D4.

**`qx2_zm.py` trusts:**

- CPython and `Fraction`;
- numpy floats for choosing tests, and one float decision, `lines_in_reach` (slack about $9 \cdot 10^{-5}$);
- paper lemmas (`QUADRANT_EXACT.md`, `ZM_MIXED.md`, including the McCormick bound of Lemma E);
- the D4 fold and the `SYM` delegation;
- `qx2_records.py` for coverage, which re-decides no leaf.

**It decides:** its leaves, and Lemma Z, which Lean also proves.

**Both share:** the cover bytes; mixed-format semantics, closed squares and parametric segment fractions; the statement ValidTilt9 and Daniel's Lean reduction (kernel-checked; build and axiom receipts here, not yet cited); CPython `Fraction`; the reach constant; the vertex-of-arrangement idea; and a model family. An error in the statement, the format reading, the Lean reduction or `Fraction` would pass both. An error in Brunn–Minkowski against McCormick, closure against Lemma Z, flint against numpy screening, or no symmetry against D4 would pass only one.

## 5. What a Replay Here Must Establish

**To count as a replayed independent decision of ValidTilt9:**

1. **Pinned inputs.**
   - The cover: SHA-256 `4151d7c4…`, from the 3 October evand packet.
   - The code: `c561dbb`'s `src/`, with the checking modules at `da469ec` and `run_all.py` `cd6627de…`.
   - CPython 3.14 and python-flint 0.9.0.
   - The records: checked against **this packet's retained** `release/records.sha256`, not the copy `verify_tilt9.sh` fetches from the same release (W-4).
2. **Bind each record to code and cover.** Read each header and record its `sha256` map and `argv`. The digests should be `4151d7c4…` and `da469ec`'s modules (`tier_b2` `5fb2a7cc…`, `rf` `5a86a6a7…`, `tier_a` `bb23e935…`, `tier_b` `ca72a149…`, `solver` `aa462c15…`, `cover` `93906681…`), with `run_all` `899144f9…` or `cd6627de…`. A mismatch is a finding, not a failure, if step 3 holds, but it must be reported (W-2, W-5).
3. **Re-decide every leaf, or the whole region.** Two designs are valid; the first is preferred.
   - **(A) Leaf re-certification of the published record.** Run `check_record.py --claim tilt` once for the tiling and `EMPTY`. Then run it with `--partial --recheck N --recheck-b M`, with N and M at least the `CORE` and `TIERB2` counts, sharded by lines, so that every `CORE` and `TIERB2` leaf is re-certified. This is option-free, so the unknown per-root regimes (W-3) do not matter, and it tests the published certificate itself.
   - **(B) A fresh `run_all.py` over the whole region** with stated options and its own records, then `check_record --claim tilt`. This decides ValidTilt9 again with the same independent code, but it does not test the published record. It can be compared root for root only where a root's original options are known.
4. **Controls.** Box-9 mutants must be refused, for instance the $1 - 10^{-4}$ segment scaling of §0, which Tier B refused here with an exact witness, plus a lighter Lebesgue square and a corner family. `tests/` holds only k = 7 mutants (W-7).
5. **Receipts** written by `devtools.replay_receipt`, with workers started by `fork`, as the 2 October review found was needed for CPU accounting. The cost is about 766 h of wall time per root at the source, which per F-6 means roughly 0.35–0.40 of that in CPU (about 270–310 CPU-hours), unmeasured on this cover (W-14). The 2 October review found leaf re-certification costs about as much as the search.

**What a sample of roots re-run here can and cannot establish.**

- It can show that the pinned code reproduces those roots' leaf lists under the options they ran with, where those are known, and that those leaves certify.
- It cannot speak for any other root.
- Recorded as `audited-here` or `replayed-here` with `replay_status: passed`, it would wrongly satisfy `_machine_proof_shaped` for the whole claim.

**What the source's `verify_tilt9.sh` run here can and cannot establish.**

- It can establish the record digests (against the retained list), the complete tiling of the region, exact `EMPTY` leaves, and 2,000 `CORE` plus 20 `TIERB2` re-certifications at a fresh seed.
- That makes it a diagnostic, the analogue of Daniel's fast `verify.sh`.
- It is not a decision of ValidTilt9: it covers about 0.03% of `CORE` and 0.0007% of `TIERB2` leaves.

## 6. What `T-081` May Claim

**Rungs: no change.**

- **V.** `derive_verification` needs a machine-proof-shaped entry: a certificate, a replay command and `replay_status: passed`. A reported run has none. `T-081` stays V0.
- **C.** C2 and above need a confirming-origin entry (`replayed-here`, `audited-here` or `independently-external`) with a passing replay. wand125's run is a third party's own decision, reported, with records pinned but not retained and nothing replayed here.

**Recording the run.** Record it as:

```yaml
origin: external
assurance: reported
performed_by: independent-external
relationship_to_generator: independent-implementation
independence_record: …/valid7-independent-check/READ_LOG.md
replay_status: not-attempted
verifiers: [V-wand125-valid7-checker]   # a new versions entry for c561dbb / cd6627de
```

Recording it as `independently-external` with a passing status would make `derive_confirmation` return C3 and `derive_verification` return V3 for the part, with no replay done anywhere. That is blocking for (a) as a recording condition (W-12). An `external_review` with a qualifying state can keep C1.

**Wording.**

- `E-k2m4-evand-validtilt9-qx2-report`'s "ValidTilt9 has one implementation; no second checker has run on this cover" becomes false. It should become: a second, separately written exact checker (wand125's) reports deciding ValidTilt9, not replayed here.
- `T-081`'s claim and composition may add that sentence. They must not say "confirmed", and they must not imply independence beyond the code (W-8).
- `next_rung`'s "A second, independent check of ValidTilt9 would build on … Milestone C" should name this run's full replay (§5) as the nearer route.
- The reported 766 core-hours is wall time per root (F-6).

**Scope and composition.**

- This source bears only on k ≥ 8 ($n \ge 60$). It adds nothing at k = 5, 6, 7.
- `T-081` is compound. Even a confirming replay of this run lifts only the ValidTilt9 part. The Lean reduction needs its own `replayed-here` proof-assistant entry, from the build and axiom receipts already in the packet, before `T-081` can reach V3/C3.
- By the rule that the result takes the part closest to the producer, `T-081` would then read "reproduced with the producer's code", since the reduction is Daniel's own Lean, even with wand125's replay deciding ValidTilt9.
- A `C3` result must also name a control path (W-7).

## Findings

For each finding, (a) is recording this run as reported evidence on `T-081`, and (b) is counting a future full replay of it as confirming evidence.

- **W-1. Leaf certification rests on the source's run.** `RECORD OK` decides coverage, `EMPTY` and a sample of 2,300 out of 9.5 million leaves, not ValidTilt9.
  - (a) Non-blocking; this is what *reported* means.
  - (b) **Blocking** until every leaf, or the whole region, is re-decided here (§5, step 3).
- **W-2. Code provenance is asserted, not bound.**
  - Headers are written only at file creation, and resumes after the switch to v2 write none.
  - The unrestricted machine-1 record is not published; `MERGE.md`'s "as run" digest is the restricted file's.
  - The run started 19 minutes before `da469ec` was committed, and the pilot roots' code version is prose only.
  - (a) Non-blocking if the entry's limitations say "the source states".
  - (b) Non-blocking under design (A) or (B), which re-decide with pinned code; blocking for any replay that relies on the records' own provenance.
- **W-3. Options per root are not recorded.** `--amin` and `--bmid-*` changed mid-run, and line positions in `tilt9_a` are shifted by the restriction.
  - (a) Non-blocking.
  - (b) **Blocking** for a root-for-root leaf-list comparison; resolved by design (A).
- **W-4. `verify_tilt9.sh` is self-attesting.** It checks the records against a `records.sha256` downloaded from the same release.
  - (a) Non-blocking.
  - (b) Non-blocking if the replay uses the retained `release/records.sha256`.
- **W-5. `check_record.py` does not bind a record to the cover or code.** It skips the header and takes the cover from the command line.
  - (a) Non-blocking.
  - (b) Non-blocking with §5 step 2, or with full re-certification against the pinned cover.
- **W-6. The closure of a `TIERB2` leaf at its $u$-ends works across leaves, not by DESIGN B2's "$m(u)$ continuous".** That claim fails where $R(u)$ empties on one side. The leaves still cover the closed region, because lo$(u)$ increases on $(0, \sqrt2 - 1]$ and nothing above $\sqrt2 - 1$ is needed.
  - (a) Non-blocking. (b) Non-blocking.
  - A wording fix for the source.
- **W-7. No mutation control on the box-9 cover.** `tests/` mutates only the k = 7 cover. My in-memory mutant was refused with an exact witness of mass 0.99995.
  - (a) Non-blocking.
  - (b) Non-blocking for the decision. It is required if this replay is the one carrying `T-081`'s control path for C3.
- **W-8. Independence holds for code, not for the generator.** The read log is a declaration. The same author had Daniel's checkers on disk, and both programs were made with Anthropic Claude models (`c561dbb` trailer; `CREDITS.md`). This review is a third instance of that family.
  - (a) Non-blocking, provided the limitations say so.
  - (b) Non-blocking for `relationship_to_generator: independent-implementation`, but the common model family must be recorded.
- **W-9. The statement contains ValidTilt9.** No defect: region, admissibility, rotation, doubled segments and density all match Lean. The evaluator equals the Lean-definition mass exactly at 40 poses.
  - (a) Non-blocking. (b) Non-blocking.
- **W-10. The method's premises hold on box 9.** No defect: side 9, a one-sided $u$-range, the slab at 0, reach, one polygon, no point masses, `EMPTY`, A1/A3 widths and `wmin`. D-1 to D-3 are correctly fixed at `da469ec`, and the v2 hand-off cannot admit an uncertified pose.
  - (a) Non-blocking. (b) Non-blocking.
- **W-11. `rf.nonneg_on` does not terminate when `lo == hi` and $p(lo) = 0$.** It is dead code, and D-4 is unchanged but unreachable here.
  - (a) Non-blocking. (b) Non-blocking.
- **W-12. Recording rule and wording on `T-081`.**
  - The run must be `origin: external`, `assurance: reported`, `replay_status: not-attempted`. Any confirming origin with `passed` would mechanically raise the part to V3/C3.
  - The "one implementation" sentence and the `next_rung` clause must be updated, and no "confirmed" may appear.
  - (a) **Blocking** as conditions of recording. (b) Not applicable.
- **W-13. The composition caps what a replay can show.** A confirming replay of this run lifts only the ValidTilt9 part. `T-081` also needs the Lean reduction's own `replayed-here` entry. The result's confirmation-code attribute would read "reproduced with the producer's code" because of the reduction.
  - (a) Non-blocking.
  - (b) Non-blocking for counting the run, but `T-081`'s rungs do not move on it alone.
- **W-14. The cost figure is wall time per root (F-6).** A replay is estimated at roughly 270–310 CPU-hours, unmeasured on this cover.
  - (a) Non-blocking. (b) Non-blocking.
- **W-15. The source's own Tier B samples used fixed seeds.** `check_tilt9.out` uses seeds 1001 to 1015, chosen by the author.
  - (a) Non-blocking.
  - (b) Non-blocking; any sampled diagnostic here should use a fresh, printed seed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
