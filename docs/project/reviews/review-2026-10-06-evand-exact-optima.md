Review: Evan Daniel’s Exact Optima of 48 Known-Best Packings (T-098)

I am Claude Opus 5.5 (`claude-opus-5-5`), running as the tbd-strong sub-agent at that tier's configured reasoning setting. I was prompted separately from the lane that retained the packet, replayed the certificates and registered T-098, and I share none of its context beyond the brief and the committed record. I worked read-only in the detached worktree at `4421c513f` (branch `claude/ecstatic-pascal-pothtx-exact`) and read the lane's diff against `4fa04caf2`.

**What I could not see or run:**

- **No code execution.** Every attempt was refused by this session's permission layer:
  - Python, both `.venv/bin/python3` and `uv run`
  - `node`, `bc` and `python -c`
  - `gh issue view 375`
  - listing anything outside the worktree
- **What did run.** `sha256sum`, `grep`, `git show` and `git diff` on local objects, and file reads.
- **What this costs the review.**
  - I did not read the issue itself. Its wording is quoted here as the records quote it.
  - I did not read the source repository beyond the packet, so the intake-watch account of `ab2bf47` is unchecked.
  - I re-ran nothing.
- **Scratch files.** Writes to the brief's scratch path were also refused, so my scratch files are in the session scratchpad.
- **n = 17.** I was blind to the n = 17 certificate by instruction and did not read it. While reading the retained `results.md` and `s12/search/exact/README.md` I saw that each carries an n = 17 row. I used neither and say nothing about them beyond their retention (EX-8).

## What Was Reviewed

- The claim of T-098 (`packing/frontier/results.yaml`) and its rendering in `RESULTS.md`.
- The three evidence entries `E-evand-exact-optima-2026-10-05-{report,exact-replay,source-replay}`.
- The verifiers `V-evand-verify-cert-py`, `V-evand-verify-cert2-py` and `V-evand-exact-certificates`.
- The bibliography key **[evand exact optima 2026-10-05]**.
- Result request #375 and the evand intake-watch read.
- The coverage entry and its 48 overrides and superseded reports.
- The case records:
  - read whole at n = 126, 206 and 305;
  - exact-optimum sections at n = 131, 211, 259, 263 and 306;
  - front matter of all 48 checked for a stray `conjectured_optimum`.
- The packet `packing/resources/web/evand-square-packing-2026-10-05/`:
  - README, declaration and acquisition record (spot-read);
  - subtree manifest;
  - the five receipts;
  - the source's `verify_cert.py`, `verify_cert2.py`, `geom.py`, `verify_all.sh`, `reproduce.sh` and both READMEs;
  - `results.md`, read in its rows for the 48.
- The tools:
  - `devtools/evand_exact_certificates.py` and `devtools/apply_exact_optima.py`, in full;
  - the `check_rational_witness_independent.py` refactor;
  - the hooks in `apply_upper_bound_packets.py`, `generate_frontier_case.py`, `check_source_coverage.py` and `build_known_best_atlas.py`;
  - the parts of `sqpack.witness` and `sqpack.verify` that decide a `center-basis` witness;
  - `tests/test_evand_exact_certificates.py` and the edits to three other tests.
- The frontier README's account of the lanes, `result-import.md`'s triage table, and T-088/T-089 as precedent.

## Verdict

**The bound is sound.** Each accepted certificate proves `s(n) ≤ S'`. I re-derived both of the source's checkers and both of this repository's deciders from their code. Each is a correct exact decision of "n closed unit squares, pairwise interior-disjoint, in `[0, S']²`", and each skips only pairs it may soundly skip.

**The common mode cannot inflate the claim.** The two first-party decisions share only the parse and the map from `t` to `(c, s)`. Both deciders then check, each in its own code, that what they materialized are unit squares. So a misreading of `(x, y, t)` could only yield some other valid packing in the same box, which proves the same bound. Only `n` and `S'` must be read right. `n` is held to the file name and the row count, and both are confirmed by the source's own checkers run here.

**The packet and receipts hold together.**

- All 53 retained files match the manifest.
- All 48 certificate digests appear in both replay receipts.
- Every verdict in the receipts is VALID.
- The comparison's numbers add up.

**What is wrong is in the records and the prose:**

- **One blocking record defect (EX-1).** At n = 126 the case keeps a `conjectured_optimum` that the new certified ceiling now refutes.
- **Systematic understatement (EX-2).** The case records state displacement bounds rounded to nearest, which understates the receipts at most counts.
- **Smaller faults.** A miscount (EX-3), two reproduction-sample figures the receipt does not support (EX-4), a misattributed quotation (EX-5), and a few smaller points.

**This review is short of its brief on computation.** Its own decision of the certificates could not be executed. That is a gap in the review, not a finding against T-098. A review that can run code should close it before V3/C3 rests on this record (What Remains).

Disposition: **defect-open**.

## From Certificate to Claim

**What a certificate says.**

- The format is a header `n S'`, then `n` rows `x y t` of rationals.
- Square *i* has centre `(x, y)` and rotation `θ` with `t = tan(θ/2)`, so `c = (1 − t²)/(1 + t²)` and `s = 2t/(1 + t²)`. Then `c² + s² = 1` holds exactly for every rational `t`, and the square is a unit square for any `t`.
- Its corners are `(x + c·a − s·b, y + s·a + c·b)` for `a, b = ±1/2`, in counter-clockwise order, since the rotation has determinant `c² + s² = 1`.
- The origin is the lower-left corner of the box `[0, S']²`.

`s(n)` is the least side of a square holding `n` unit squares with disjoint interiors. Any such certificate whose squares are pairwise interior-disjoint and lie in the closed box therefore gives `s(n) ≤ S'`.

**`verify_cert.py`.**

- **Walls.** It requires each square strictly inside the open box, using the axis-aligned half-extent `e = (|c| + |s|)/2`. That half-extent is exact for a unit square.
- **Pairs it decides.** For pairs with `|Δcentre|² ≤ 2` it needs one of the four face normals to separate strictly: `|n·Δ| > h_i(n) + h_j(n)`, with `h(n) = (|n·u| + |n·v|)/2`. Both terms of `h` match `u = (c, s)` and `v = (−s, c)`.
- **Pairs it skips.** Pairs with `|Δ|² > 2` have disjoint circumscribed discs, since the circumradius is `√2/2`. Skipping them is sound.
- **Separation test.** The separating-axis test with the four edge normals is complete for two rectangles.
- **Asserts.** It asserts `c² + s² = 1`, which always holds. The assert would vanish under `python -O`, harmlessly.

**`verify_cert2.py`.**

- **Walls.** Every corner must be strictly inside `(0, S')²`.
- **Pairs.** For each close pair, no vertex of either square may lie in the other closed square, and no two closed edges may meet. For convex polygons that is exactly disjointness of the closed sets: containment of one in the other shows up as vertex containment, and any other intersection shows up as an edge crossing.
- **Edge test.** `seg_meet` handles proper crossings, touching endpoints and collinear overlap.
- **Orientation.** `in_closed` relies on the counter-clockwise order, which the corner construction gives.
- **Skips.** It uses the same disc skip as `verify_cert.py`.

**`sqpack.witness.exact_verify` on the converted `center-basis` witness.**

- It builds its own corners from `(c, s)` (`_square_from_pose`).
- It checks unit edges and right angles (`check_unit_squares`).
- It requires every corner coordinate in `[0, S']` (closed).
- It decides all `n(n−1)/2` pairs, since `bucket=False`, by edge-normal separation, accepting a gap of zero.
- The receipt's `pairs_tested` (2,278 at n = 68) confirms that no pairs were skipped.

**`check_rational_witness_independent.check_squares` on the converter's corners.**

- It checks unit edges, orthogonality and closure.
- It requires every corner coordinate in `[0, S']`, failing only below zero.
- It decides all pairs, failing only a gap below zero.

**Open versus closed.** The source's checkers are strict: open box, closed squares disjoint. This repository's two are closed: touching is accepted, which is still sound for `s(n)`. A certificate with an exact contact would therefore be accepted here and refused by the source. That cannot arise for these 48, whose least clearances are about `5e-21` and `1e-20`, and it is not a defect. Neither the packet nor the evidence says it, though, and it belongs in the exact-replay limitations.

**The margins match the construction.** The source scales the KKT point by `1 + 10⁻²⁰` about the origin, rounds centres to `10⁻³⁵` and rounds the side up. That gives contact gaps of about `10⁻²⁰ × centre distance` and wall clearances of about `5 × 10⁻²¹`. Both deciders report exactly that at every one of the 48: least containment `5e-21`, and least pair gap `9.99999999999998…e-21`, identical between the two deciders to the printed digits.

## Trust Boundaries

| Boundary | What crosses it | How it is held |
| --- | --- | --- |
| Source to packet | 48 certificates, 2 checkers, solver, drivers, reports | SHA-256 manifest of 632 + 58 paths at commit `13ee36e`. I recomputed SHA-256 for the 48 certificates and 5 scripts, and all 53 match their manifest lines exactly (`grep -x -F`, 53 of 53) |
| Packet to receipts | Each certificate's digest per row | The 48 digests occur in 48 rows of each of `first-party-check.json` and `source-replay.json`. There are no n = 17 rows in either, and the manifest lists 320 certificates and nothing for n = 17 |
| Certificate to decision | Parse and `t → (c, s)` | The only shared code of the two first-party legs. Benign, as argued above, because each leg checks unit-squareness itself and `n` is cross-checked |
| Decision to record | `S'` written out in full | Each `S'` has a denominator `2^a·5^b`, so it terminates. I checked n = 68, 206, 211 and 307 by hand against the coverage values and the claim |
| Witness to atlas | The finder's binary64 pose pictured under the side `S'` | 1e-8 side tolerance in `_assert_side_matches`. The record lists a witness that does not attain its value (EX-9) |

## The Replays Run Here

None. Python execution was refused for `check --check`, `source-replay`, `compare`, `controls` and the tests. What I could do was hold the receipts to the packet by reading:

- **First-party check.**
  - The header says `all_passed: true`, with 320 rows read from a checkout, `cpu_seconds` 2,820.0 and `wall_seconds` 2,619.7 on 2 workers.
  - No row has `"passed":false`.
  - Summing the 48 rows' CPU seconds by hand gives **801.9**, against the README's 802.
- **Source replay.**
  - Header: CPython 3.14.7, both checker digests equal to the retained files, 202.0 CPU seconds and 246.7 s wall.
  - For each of the 48, both checkers exit 0.
  - `verify_cert.py` prints `VALID: s(n) <= S` with least wall clearance `5.000e-21` and least pair separation `1.000e-20`.
  - `verify_cert2.py` prints `VALID: n closed unit squares …`.
  - The 48 rows sum to 54.1 CPU seconds, against the stated "55" (nit, EX-10).
- **Controls.**
  - 144 rows, `all_as_expected: true`, wall 3,276.1 s.
  - Every overlap control moved the square by exactly the gap plus one unit, with no doubling needed. Units run from `1e-30` (n = 102, …) to `8e-29` (n = 297).
  - The shrink controls record a clearance of about `5.0000000004e-21` against the unit.
  - The `verify_all_vacuity` record shows exit 1 with only `verify_cert2 FAIL certs/n-68.cert`, and `first_leg_reported_the_failure: false`.
- **Comparison.** I read all 48 rows; the numbers are under Numbers Checked.
- **Reproduction sample.**
  - 5 rows: exit 0, `byte_identical: false`, `same_side: true`, `produced_decided_valid: true`.
  - 1 to 46 squares differ, with `largest_coordinate_difference` at most `2.466e-24`.

## The Review’s Own Computation

**The checker I wrote could not be run.** I wrote a decider from the format and the geometry alone, sharing nothing with the tools under review: `mydecide.py` in the session scratchpad.

- It reads strictly and computes corners from `(x, y, t)`.
- It requires strict corner containment.
- For each pair, it computes each of the four edge-normal projection intervals from the eight corners themselves, not from a support-function formula.
- It skips pairs only when their binary64 centre distance exceeds 1.5. The circumradii sum to `√2 ≈ 1.4142`, so a margin of 0.08 absorbs any rounding.

I launched it at n = 68, 126, 211, 263, 270 and 305, then on the other 42. Both runs were refused permission, so **no certificate was decided by this review**.

**What I could do by hand is consistent with the receipts, but it is not a decision:**

- **n = 68 side.** `S' = 4399397618609141951332334459697 / 5·10²⁹ = 8.798795237218283902664668919394` exactly. That matches the table (`…2839027…`, rounded up at 19 decimals), the coverage value and the claim. The printed `8.798795237222592` minus `S'` is `4.3081e-12`, as the comparison says.
- **n = 68 walls.** Row 2 has `x = 100000000000000000001/2·10²⁰`, `t = 0`, so its left clearance is `5e-21`. Row 5 has `x = 207469880930457097566491722984839423/2.5·10³⁴ = 8.29879523721828390265966891939357692`, `t = 0`, so its right clearance is `S' − (x + 1/2) = 5.00000000042308e-21`. That is exactly the clearance the shrink controls record for n = 68.
- **n = 68 pair.** Rows 1 and 2 are axis-parallel and stacked: `y₁ − y₂ = 1.00000000000000000001`, a gap of `1e-20`, which is the `1e-20` the receipts report. Under the corner convention above, axis-aligned squares give exactly these margins.
- **n = 206.** `232189979115498488075628916091 × 64 = 14860158663391903236840250629824`, so `S' = 14.860158663391903236840250629824`, as recorded. Below the printed side by `3.9558e-12`.
- **n = 211.** `S' = 14.997960704967361565181004478378`, and `14.99796070496771500150 − S' = 3.534e-13`.
- **n = 270.** `16.937810329390629 − 16.937810329340954110200… = 4.9675e-11`.
- **n = 307.** `17.981030548643712 − 17.981030548633310696277… = 1.0401e-11`.
- **n = 172 and 199.** `S'(199) − S'(172) = 1.00000000000000000001000000000`, exactly `1 + 10⁻²⁰`. That is what scaling two sides exactly 1 apart by `1 + ε` gives. The source's "exactly 1 apart" is about the KKT values, not the certificates, and T-098 does not repeat it.

## The Record Design

**A new entry is right.** The triage table in `result-import.md` gives a bound the record does not hold its own entry, with bounds of one kind at several counts in one release under one entry. That is what was done, and it follows T-092 (Couzo lowering his own T-056 sides) and T-088/T-089 (an optimized or certified packing of an already-reported count). T-056, T-057 and T-092 keep their claims:

- T-057 and T-092 derive as superseded by T-098 in `RESULTS.md`, since all their counts moved.
- T-056 stays current, correctly, because 105, 130 and 292 remain its counts.

**Moving the reported lane is right.** The frontier README defines `reported_upper_bound` as "the strongest literal claims in the named source set". Daniel publishes `S'` as a side, below every earlier printed one, so it is the strongest literal claim. T-088 differs because its certificate lay above the printed side: there the printed side stayed reported.

**The lanes agree, so no blocker is owed.** Both lanes now hold the same exact value, which satisfies the assurance rule. Dropping the `replay-failure` conflicts and `mathematics` blockers at n = 206, 259, 305 and 306 follows, since both were about a printed side that is no longer the reported one. The bodies keep that history: "The certified ceiling this count held before … lay above that printed side". The 22 one-unit trailing counts and the four blocked counts reconcile with the frontier README's counts: 83 − 78 = 5 (these four plus n = 126), and 43 − 21 = 22.

**The known-best witness staying the finder's pose is acceptable as a picture, but not as a witness.**

- Visually the two poses are indistinguishable: the largest displacement is `1.44e-3`, and the atlas tolerance is 1e-8 in side.
- But each case lists `W-known-best-nNNN` under `reported_upper_bound.witnesses`. Its side is the finder's printed side, and its pose does not fit in `S'`. The record therefore names a witness that does not attain the value it is listed under (EX-9).
- The bodies do tell the reader that the atlas pictures the binary64 pose. T-088 registered a rational witness (`witnesses/kingbird-2026/n-069-rational.yaml`) instead.

**Case records at the named counts.**

- **n = 126.** The opener, the exact-optimum section, "the verified ceiling here was the trivial grid bound 12", and "1.9e-11 below the side the Kingbird catalogue prints" are right. But `conjectured_optimum: '11.77473513240654'` survives from the catalogue, now above the certified ceiling `11.7747351323878328…` (EX-1). It is the only one of the 48 records that carries a non-null `conjectured_optimum`.
- **n = 206, 259, 305 and 306.** The prose is right, but the displacement bounds understate the receipts (EX-2):

  | n | Written "within" | Receipt | Written "at most" | Receipt |
  | --- | --- | --- | --- | --- |
  | 206 | `1.4e-4` | `1.414e-4` | `5.4e-12` | `5.412e-12` |
  | 305 | `1.3e-5` | `1.329e-5` | `1.3e-5` (non-free squares) | `1.329e-5` |

  At n = 259, five non-free squares move by at most `8.0e-8` (receipt `8.029e-8`).
- **n = 263** (bound only). The second paragraph correctly uses the bound-only sentence, but "within `4.1e-5`" and "at most `4.1e-5`" understate `4.136e-5`.

## Numbers Checked

| Statement | Where | Against | Result |
| --- | --- | --- | --- |
| The 48 counts | Claim, scope, coverage, `IMPROVING` | `results.md` rows, retained certificates, manifest | Agree |
| `3.5e-13` (n = 211) to `5.0e-11` (n = 270) | Claim, headline, evidence, README | Receipt `3.5344e-13`, `4.9675e-11`; hand checks | Right |
| Couzo 46 (39 T-056, 7 T-092), de Winter 126 and 211 | Claim, README | `earlier_result` per row | Right |
| 44 KKT, 4 bound-only (177, 211, 263, 272) | Claim, evidence, README | `results.md` status column | Right |
| 11 squeezed inputs | Evidence, README | `results.md` input `P`: 102, 103, 106, 123, 152, 172, 207, 236, 237, 269, 302 | Right |
| Every pose within `1.5e-3` | Claim | `1.44e-3` (n = 103) | Right; rounded up |
| Non-free squares within `4.2e-5` | Claim | `4.136e-5` (n = 263) | Right; rounded up |
| Non-free squares "at most `4.1e-5`" | Packet README | `4.136e-5` | Understated (EX-2) |
| 1,543 moved, 358 listed free, 1,185 others at 24 counts that include all eleven squeezed inputs | README | Row sums (hand-added); 24 counts with non-free motion, all 11 `P` counts among them | Right |
| Unmoved squares at most `9.2e-9` | README | `9.191e-9` | Right |
| Free-square indexing | `pose_match` | At n = 68 (4/4), 206 (41/41) and 228 (9/9) every moved square is on the source's free list | Consistent with 0-based alignment |
| 802 / 2,820 CPU s first-party; 202 / 55 source replay | README, evidence | 801.9 / 2,820.0; 202.0 / 54.1 | Right; "55" is a nit |
| Controls: gap `1e-20` + unit `1e-30` to `8e-29`; clearance `5e-21` | Claim, evidence, README | Receipt rows | Right |
| Reproduction: "1 to 46 places … at most `2.5e-24`" | README, notes | Rows: 17, 46, 2, 1, 6 squares; `2.466e-24` max, centres only | Centres only (EX-4) |
| Reproduction: "247 CPU seconds in all" | README | Row sum 172.9 CPU s (326.8 s wall) | Not in the receipt (EX-4) |
| `S'` written out in full | Claim, coverage, cases | Hand checks at 68, 206, 211, 307 | Right |
| Frontier README: "exact optima of 48 of those packings and of de Winter’s n = 126" | Frontier README | 46 Couzo + n = 211 = 47, plus n = 126 = 48 | Miscount (EX-3) |
| 272 other certificates; 1e-20 to 1e-14 above | Notes, coverage | 321 − 48 − 1 held; spot rows in `results.md` | Right |
| Seventy-eight trailing and 21 one-unit; `TRAILING_BY_CORPUS` 78, 46 | Frontier README, test | 22 one-unit counts among the 48, plus the 5 counts leaving the trailing set | Consistent |

## Provenance, Credit, Licence and Dates

**Credit.** `Daniel after Couzo, de Winter, Ellsworth, Levy` with `builds-on-project` is right:

- The batch README says the inputs are this register's witnesses ("Register data: CC BY 4.0, Joshua Levy, the squares project").
- It says the packings are their finders'.
- The solver's README (Method, step 3) says its stationarity rows give "exactly David Ellsworth's nested Jacobian-determinant conditions".

The bibliography note attributes the "Ellsworth's analytic minimisation, reimplemented" statement to the batch README, which does not contain it. The packet README attributes it to the issue (EX-5).

**AI assistance.** The case records and the claim quote the issue: "written with Claude (Anthropic) as a coding and research agent, directed and reviewed by me". That agrees with the batch README ("written by the same author and agent as the solver") and with the commit's co-author line as the packet records it. I could not read the issue to confirm the quotation.

**Licence.** MIT. `LICENSE` and `s12/LICENSE` are pinned with digest `c51886c0…`, identical to the 4 October packet's, and `s12/CREDITS.md` is identical too.

**Dates.**

- `published: '2026-10-05'` matches the commit (2026-10-05T20:54:59Z) and the issue's opening date as recorded.
- Retrieval at 22:08Z, with `main` unchanged at 22:22Z, is consistent.

**Retention against OR-18.** About 1.6 MB of text certificates and a few small scripts, with `results.json` gzip-compressed, is far below OR-18's "a few megabytes" per object. Retaining the 48 certificates the claim rests on and pinning the other 272 by digest is the right split. The receipts' SHA-256 values guard a real boundary (a downloaded source) under OR-16.

**The hold.**

- No n = 17 file is in the manifest, the scope, the receipts or the controls.
- The tools refuse n = 17 (`HELD`, tested).
- Two wording points (EX-8):
  - "not pinned" is true by digest only, since commit `13ee36e` (tree `4cfac04…`) pins the whole tree.
  - The README lists `results.md` and `results.json` as retained files that keep their n = 17 rows, but not `s12/search/exact/README.md`, whose test-set table has one too.

**Intake watch.** The read moved to `13ee36e`, and the note describes `ab2bf47` as a working note on the algebraic degree of `s(83)`'s printed polynomial. I could not fetch the source to check that description.

**`verify_all.sh`.** Its first leg runs `python3 verify_cert.py c | tail -1 | grep -q VALID` without `pipefail`. `INVALID` contains `VALID`, and the exit status is discarded, so the first leg reports a failure only when `verify_cert.py` prints no verdict line at all, as on a crash. It can never report an INVALID verdict, and the vacuity record shows exactly that. The packet's account is right.

The conclusion drawn from it goes slightly too far. The batch README's ✓✓ column comes from `summarize.py`, which "runs both verifiers". That script is pinned by digest only, and the packet does not say whether it reads exit statuses. Whatever the answer, the replay here, held to exit status and verdict line, establishes the source's claim for all 320 (EX-7).

## The Tooling

**Parser.** It is strict where the source is loose:

- It refuses rows past `n`, extra fields, exponents, underscores, leading zeros in `n`, a zero denominator and a non-positive side.
- It holds `n` to the file name.

So no certificate is accepted here that the source would read differently. The converse difference is only strict versus closed, as above. `splitlines()` splits on a few more characters than the source's file iteration does; it is moot for these fixed bytes.

**Conversion.** The conversion is exact, and the tests pin it:

- `c² + s² = 1` for several values of `t`.
- `t = 1/3` gives `(4/5, 3/5)`.
- `t = 1` gives a quarter turn.

The module docstring lists "the corner arithmetic" in the common mode. Only the independent leg consumes those corners, and that leg checks their shape, so the evidence's "the parse and the map" is the accurate statement. The docstring also says no code here reads the source's checkers, yet `verify_all_vacuity` copies them byte for byte. That is harmless (EX-10).

**Controls.**

- The overlap control moves along a unit face normal by gap plus unit and confirms a negative SAT gap before use.
- The shrink control places a corner exactly one unit outside.
- The receipt keeps only booleans, though, so it cannot show that the overlap control was refused for the overlap rather than for a wall. A move of `1e-20` exceeds the `5e-21` wall clearance whenever the closing normal points partly toward a wall (EX-6).
- The one-unit shrink is honestly labelled a positive control.

**Compare.** Nearest-centre matching, one to one, with rotation taken modulo 90°, is fine. Reading the earlier holders from the packets and the catalogue rather than from the rewritten cases is the right design.

**`apply_exact_optima`.**

- It is idempotent, and the tests confirm it at four counts and on the coverage file.
- Unlike `apply_upper_bound_packets` (line 408), it does not null `conjectured_optimum` (EX-1).
- `_scientific` rounds to nearest, and bounds need rounding up (EX-2).
- The KKT sentence says "curvature positive away from its exact flat motions". The source says the reduced Hessian is "PSD/PD modulo exact flat motions", so "non-negative" would be faithful (EX-11).

**Hooks and tests.**

- The atlas hook pictures the earlier holder's packet, by the comparison receipt.
- The coverage loader accepts a certificate directory as a claims record.
- The test edits update expectations without weakening them: the trailing tests now assert agreement and the absence of `replay-failure` at the 48 counts.

## Which Code Confirmed It

- **`E-evand-exact-optima-2026-10-05-exact-replay`** is "independently re-implemented", and that is right. Its deciders are this repository's own, predate the import, and share no code with each other or with the source. The converter is first-party and imports nothing of the source's. Its author's prior reading of the source's checkers is disclosed, and only the conversion depends on it.
- **`E-evand-exact-optima-2026-10-05-source-replay`** is "reproduced with the producer's code", `same-implementation`. That is right, and the entry says it is not an independent check.
- **The reproduction sample** reruns the producer's solver. It is described as such and is not used as evidence for a rung.
- **The T-098 claim and `RESULTS.md`** say "independently re-implemented" only of the first-party decision, and "reproduced with the producer's code" only of the source checkers' replay. Both phrases are used where, and only where, they are true.

## Significance

I confirm **S2**. The 48 sides fall by `3.5e-13` to `5.0e-11`, the binary64 slack of packings already reported, and no theorem moves. At n = 126 the verified ceiling leaves the 12 × 12 grid by 0.225, but by certifying a packing the record already reported. That is the case T-088 scored S2 when it took n = 69 off the 9 × 9 grid. Removing four trailing ceilings is record hygiene. The exact solver is the source's method, not a result here.

## Findings

**EX-1 (blocking): n = 126 keeps a refuted `conjectured_optimum`.**

- **Location.** `packing/frontier/n-126.md`, front matter line 72: `conjectured_optimum: '11.77473513240654'`.
- **Defect.** The same record's `verified_upper_bound` is `11.774735132387832842560264587322`. The record therefore asserts a conjectured optimum that it also proves false.
- **Cause.** `apply_exact_optima.front_matter` never touches `conjectured_optimum`. `apply_upper_bound_packets` sets it to null when it moves the lanes. n = 126 is the one count of the 48 that did not pass through that intake first.
- **Fix.**
  - Set `conjectured_optimum` to null in `front_matter`, since Daniel conjectures no optimum, and regenerate n = 126.
  - Add a record check that a non-null `conjectured_optimum` lies within `[verified_lower_bound, verified_upper_bound]`.

**EX-2 (non-blocking): displacement bounds are rounded to nearest.**

- **Location.** `devtools/apply_exact_optima.py`, `_scientific` (`f"{value:.1e}"`), used for "within …" and "at most …" in the exact-optimum section of the 48 case records. Also the packet README, "move by at most `4.1e-5`".
- **Defect.** These are upper bounds rounded to nearest, so most of them understate the receipts:
  - "within `1.4e-4`" against `1.414e-4`, at many counts including 132, 177, 206, 209, 210, 228, 259 and 306;
  - `4.1e-5` against `4.136e-5` (n = 263);
  - `1.3e-5` against `1.329e-5` (n = 305);
  - `5.1e-10` against `5.123e-10` (n = 211);
  - `6.4e-11` against `6.445e-11` (n = 126).
- **Fix.** Round the mantissa up for bounds (or print three significant digits), regenerate, and write `4.2e-5` in the README.

**EX-3 (non-blocking): the frontier README miscounts the packings.**

- **Location.** `packing/frontier/README.md`, the baseline paragraph (about line 175 of the diff).
- **Defect.** "Evan Daniel’s exact optima of 48 of those packings and of de Winter’s n = 126" counts 49. It should be 47 of those packings (46 Couzo's and de Winter's n = 211) plus n = 126.
- **Fix.** Correct the count.

**EX-4 (non-blocking): two reproduction-sample figures are not in the receipt.**

- **Location.** The packet README, "A reproduction sample", and the T-098 notes.
- **Defect.**
  - "247 CPU seconds in all" does not appear in `reproduction-sample.json`, whose rows sum to 172.9 CPU s (326.8 s wall).
  - "Squares differ … by at most `2.5e-24`" measures centres only: `largest_coordinate_difference` ignores `t`.
- **Fix.**
  - Record the total in the receipt, or quote the row sum.
  - Add the largest `|Δt|` to the receipt, or say "centres differ by at most".

**EX-5 (non-blocking): the Ellsworth statement is attributed to the wrong file.**

- **Location.** `packing/resources/bibliography.yaml`, the **[evand exact optima 2026-10-05]** note.
- **Defect.** It credits the batch README with saying the method is Ellsworth's analytic minimisation reimplemented. The batch README does not say that. The solver's README cites Ellsworth's conditions, and the packet README attributes the statement to the issue.
- **Fix.** Name the right sources.

**EX-6 (non-blocking): the overlap control's cause of refusal is not recorded.**

- **Location.** `receipts/negative-controls.json` and `evand_exact_certificates._all_checkers`.
- **Defect.** Only booleans are kept. So the record cannot show that each overlap control is refused for the overlap and not for a wall breach caused by the same `1e-20` move.
- **Fix.** Record each checker's failure reason (`verify_cert2`'s message, both first-party failure lists) and the mutant's least wall clearance. Where the move breaches a wall, move the other square of the pair.

**EX-7 (non-blocking): the `verify_all.sh` conclusion goes slightly too far.**

- **Location.** The packet README, "The source’s own driver", and the source-replay limitations.
- **Defect.** "Rests, for `verify_cert.py`, on something its driver did not test" leaves out `summarize.py`, which produced the ✓✓ column and is pinned unread.
- **Fix.** Qualify the sentence, or read `summarize.py` and say what it checks.

**EX-8 (non-blocking): the hold's wording is loose.**

- **Location.** The packet README's opening and "Left out".
- **Defect.** "Not pinned" should be "not pinned by digest". The list of retained files that keep n = 17 rows should name `s12/search/exact/README.md` beside `results.md` and `results.json`.
- **Fix.** Make both wording changes.

**EX-9 (non-blocking): the listed witness does not attain the reported value.**

- **Location.** The 48 case records, `reported_upper_bound.witnesses: [W-known-best-nNNN]`.
- **Defect.** The witness's side is the finder's printed side, which is not the reported value.
- **Fix.** Either register the certificate as a rational witness, as T-088 did at n = 69, or state in the witness entry that it pictures the finder's pose and certifies only the earlier side.

**EX-10 (non-blocking, nits).**

- "Least pair gap `1e-20`" is `9.99999999999998e-21` exactly; "about `1e-20`" is accurate.
- The source replay's "55" CPU seconds for the 48 is 54.1 by the receipt.
- The module docstring's common-mode list and its "not read by any code here" need the corrections described under The Tooling.

**EX-11 (non-blocking): the KKT sentence overstates the curvature.**

- **Location.** `apply_exact_optima.KKT`, in 44 case records.
- **Defect.** "Curvature positive away from its exact flat motions" claims more than the source's "PSD/PD modulo exact flat motions".
- **Fix.** Write "non-negative".

## What Remains

- **This review's own decision.** Run `mydecide.py`, or any decider sharing nothing with the tools, on at least n = 68, 126, 211 and one of 263, 270 and 305, and compare its least margins with the receipts. Re-run `check --check` and a sample of `source-replay` rows. All of this was refused here.
- **The issue.** Read issue #375 and its acknowledgement, to confirm the AI-assistance quotation and the Ellsworth attribution.
- **The source.** Read `ab2bf47` and `summarize.py` at the pin.
- **The fixes.** Apply EX-1 and regenerate. Then V4/C4 need a second adversarial review by a distinct reviewer and a human oversight record, as `next_rung` says. EX-2 to EX-11 can land in the same pass.

## Disposition

**defect-open.** The bound `s(n) ≤ S'` at the 48 counts is sound as reasoned here and as the receipts record it. EX-1 is a contradiction inside a case record and blocks merge until it is fixed. The other findings do not block. This review did not decide any certificate itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
