# Review: Evan Daniel's Exact Certificates as Verified Ceilings at 77 Counts (T-118)

**Reviewer.** Claude Opus 5.5 (`claude-opus-5-5`), run as the tbd-strong sub-agent tier (configured reasoning effort xhigh). I was prompted separately as an adversarial reviewer and shared no context with the lane that retained, replayed and registered the result (think-70bh, lane R8). I worked from the brief, the committed record and my own reading.

**Commit read.** `a91d9b385` on `claude/ecstatic-pascal-pothtx-r8`, in a detached worktree. The branch's change is `git diff 7f2a01816..a91d9b385`.

**What I could and could not run.** The session refused every invocation of the project interpreter (`packing/.venv/bin/python3`, with or without `nice`), and also `awk`, `sed`, `bc` and most piped commands. I could run `sha256sum`, `grep`, `git diff` and `git show`, and I read files. As a result:

- No certificate was decided in full by code I wrote. This is the gap the T-098 reviews also left open, and it is still open.
- I checked parts of one certificate (`n = 50`) by hand in exact decimal arithmetic.
- I checked every retained certificate's digest against all four records that pin or decide it, with `sha256sum`.
- I reproduced the closed-form gaps at `n = 50` and `n = 53` by hand.

**`n = 17`.** I did not open, read, decide or use any `n = 17` certificate, input or record. One bulk `grep` over `packing/frontier/n-*.md` printed a single front-matter line of `n-017.md` in its preview. I did not use it, and nothing below depends on it.

**Verdict line.** The bound `s(n) ≤ S'_n` at the 77 counts, and the verified value `S'_n` rounded up at the fourteenth decimal, follow from the receipts as the record says. The selection is right, `n = 29` is handled correctly, and so are `n = 69, 83, 87`. One blocking finding is open: the claim (and the blockers and prose generated from the same sentence) states that no rational certificate reaches the catalogue's closed-form side. That is false at the six counts whose closed form is rational, and at `n = 50` the source's own exact point appears to be such a certificate. Seven non-blocking findings follow.

## Findings

### EC-1 (blocking): "which no rational certificate reaches" is false at the six rational closed forms

T-118's claim says: "At the other 55 the catalogue also gives the side as a closed form, which no rational certificate reaches". The same sentence appears in other places:

- the generated `mathematics` blocker at each closed-form count (`apply_exact_ceilings.trailing_blocker`: "the report's exact form …, which no rational certificate reaches");
- the module docstring ("where the report has a closed form, which no rational certificate reaches");
- the packet README, "What they carry": "a rational certificate bounds such a side from above and does not reach it".

Six of the 55 closed forms are rational numbers:

| n | Closed form |
| --- | --- |
| 50 | `7 + (4/7)` = 53/7 |
| 171 | `13 + (4/7)` |
| 198 | `14 + (4/7)` |
| 230 | `15 + (28/41)` |
| 261 | `16 + (28/41)` |
| 293 | `17 + (26/41)` |

A rational side can be reached by a rational certificate. The project's two deciders accept contact (packet README, "Open and closed"), so a contact-exact rational packing at side 53/7 would verify `s(50) ≤ 53/7` here and close the gap.

At `n = 50` the retained certificate shows that such a packing almost certainly exists, as the source's own exact point before outward rounding:

- **Squares off the grid.** Every square the source does not list as free has `t = 0` or `t` equal to 1/3 rounded to 35 digits (`33333333333333333333333333333333333/10^35`). An exact `t = 1/3` gives `(c, s) = (4/5, 3/5)`, a rational 3-4-5 rotation.
- **Centres.** The centres are 1/350-grid rationals scaled by `1 + 10^-20`. Row 20's x is `3.26571428571428571431837142857142857`. That equals (1143/350)(1 + 10^-20) = 3.265714285714285714285714… + 3.2657142857e-20 to every digit shown. Its y is (2151/350)(1 + 10^-20) to every digit shown.
- **Side.** The side is `53/7 · (1 + 10^-20)` rounded up. The receipt's gap above the closed form, `7.5714e-20`, is exactly (53/7)·10^-20.
- **Free squares.** The rows whose `t` is off 1/3 or 0 (rows 8, 22, 26, 29, 35, 49) are exactly squares 5, 19, 23, 26, 32 and 46. Those are the six the survey lists as free.

The other five rational forms are of the same shape: k + 4/7, and k + 28/41 or 26/41, which suggests 9-40-41 rotations. I did not open those certificates.

This does not affect the bound `s(n) ≤ S'`. It is a false mathematical statement in the `claim`, which is the text the rungs attach to (epistemics, "Scope and Composition"). It also points the next rung at the wrong remedy for those six counts.

The fix is to rephrase in the claim, the blocker template, the README ("What they carry" and "Not Done Here"), the docstring and `next_rung`:

- the 49 irrational closed forms are not reached by any rational certificate;
- at the six rational ones, this certificate stops about `S·10^-20` short by construction (it was scaled and kept clear), and a contact-exact rational certificate would reach the report.

The ceiling-section prose ("its squares are rational and each is kept clear … so it bounds the exact side from above and does not reach it") is about this certificate, so it is correct as written.

### EC-2 (non-blocking): `n = 29` is described as an "interval enclosure of the exact optimum"

T-118's notes, the packet README ("its interval enclosure of the exact optimum lies `5e-21` below the certificate's side") and the module docstring all describe `n = 29`'s ceiling this way. The evidence it cites, `E-n029-interval-certified-upper`, says the opposite. That entry proves `s(29) ≤ 5.93383346267692918974379895098` "at a declared relaxation of 1e-20", and "It is not the optimum … and not the value the enclosures surround".

The handling of `n = 29` is correct (see the checks below). Only the description is wrong. Suggested wording: "its interval-certified bound (`E-n029-interval-certified-upper`) lies `5e-21` below `S'`".

### EC-3 (non-blocking): nothing refuses a certificate whose side falls below a closed-form side

`survey_row` records `certified_above_exact_side_by` as a signed float. Nothing in `survey`, `survey_problems` or `test_each_ceiling_is_the_certified_side_rounded_up_at_the_printed_precision` requires it to be positive.

Suppose a future certificate's `S'` lay above the truncated printed decimal but below the catalogue's closed form. That would mean a packing smaller than the catalogue's exact side, which is a discovery and not a ceiling. The layer would still file it as a T-118-style ceiling, and its blocker would read "lies -x above it".

No current count is affected. All 55 gaps are positive, from `7.5714e-20` (n = 50) to `1.7823e-19` (n = 299), each equal to `S·10^-20` to four or five figures. Add a refusal in `survey` and an assertion in the test.

### EC-4 (non-blocking): the significance rationale says the ceilings moved "onto the report itself at 22"

At those 22 counts the ceiling is the printed side plus one unit of its fourteenth decimal. The certified packing's own side lies above the printed decimal there, by up to `9.3e-15` (n = 28). For example, `n = 28`'s witness side is `5.82444461667405929695…` against the printed `5.82444461667405`. The two agree under `bounds_agree_at_declared_precision`, which is a display relation; the claim's own wording ("agrees with the report to one unit of its last place") is the right one. Use it in the rationale too.

### EC-5 (non-blocking): dropping `E-kingbird-upper-register` from T-088 and T-089

The removal does what it says. T-088 and T-089 claim only their certified sides (8.82719465572975; 9.63475764863195 and 9.83881526994915). T-118's bounds imply those claims, so the derived mark "superseded by T-118" is correct for the claimed bounds, and `test_result_status` pins it. The notes record the removal and why.

Two consequences are not stated:

1. The evidence list changed on entries that the 2026-10-05 review accepted with that citation in place, and the review is not told.
2. The reported lanes at 69, 83 and 87 (Ellsworth's and Chang's improvements) now rest on no register entry. Those improvements are what T-088's and T-089's S2 rationales score ("Lowers the best known side …"), and those entries now display "superseded". A reader can take that to mean the packings were superseded. T-118 is a certificate of the same packings and claims no packing.

Add a sentence to each note: "superseded as a ceiling; the packing it registered remains the best known and the reported bound". Alternatively, record that the owner chose this reading.

### EC-6 (non-blocking): a new entry departs from two rows of the register-action table, and the notes name neither

Two rows of `result-import.md` Stage 1 bear on this:

- "Bounds of one kind at several counts in one release → One entry whose `scope` covers them". The T-046 widening of 6 October follows this row ("One entry for one revision's replays … rather than a second"), and both point toward widening T-098.
- "Below the standing bound and asking for no work → None; it stays in the packet". Each `S'` is weaker than the reported side, and the author asked for nothing.

T-118's notes justify a separate entry soundly. T-098's claim, score and two reviews are about the 48 that lower a printed side, which #375 asked for. These 77 move only the ceiling, on the owner's decision of 6 October. Widening T-098 would have changed a reviewed claim. I judge the new entry correct; it misstates nothing.

The notes should still name both rows they depart from, and say that the owner's decision overrides the second.

### EC-7 (non-blocking): the overlap control's invalidity is established in part by a decider under test

`overlap_control` accepts a mutant only once `independent.pair_gap(...) < 0`. That is the same function behind the `independent` verdict the receipt then reports as a refusal, so that one refusal is circular. The other three are not:

- `sqpack.witness.exact_verify`;
- `verify_cert.py`;
- `verify_cert2.py`.

The mutant is provably invalid in any case. The corners are built from `(c, s)` with `c² + s² = 1` exactly, so the edge normals are rational unit vectors. A negative maximum over all four face axes then implies, by the separating-axis theorem, that the two closed squares' interiors meet.

The README says the mutant is moved "one unit … past touching". More exactly, the mutant moves the pair's best face-axis gap plus one unit along that axis. Say "past the pair's separating-axis gap".

The receipt shows `moved_by_gap_plus` equal to `unit` at all 77 counts in order, so the "doubled until it overlaps" branch never ran.

## Checked and Found Correct

**What each certificate proves, and when it was decided.** Each certificate is `n` rational squares (centre and `t = tan(θ/2)`) in a box of rational side `S'`, and it proves `s(n) ≤ S'`.

- `first-party-check.json` decided all 320 non-held certificates with both of the project's deciders: `all_passed: true`, 320 rows with `"passed":true`, none false. The certificates were read from a checkout at the pin on 5 October, with `minimum_containment_clearance` `5e-21` at every count.
- `source-replay.json` ran the source's two checkers on the same 320: `all_passed: true`, `wall_seconds` 246.7, 2 workers.

**The verified value follows.** `verified_value` returns `max(printed, ceil₁₄(S'))`. All 77 printed sides have exactly 14 decimals, and `0 < S' − printed < 10^-14` at every count (receipt range `1.1624e-16` to `9.78e-15`). So the value is printed + `10^-14`, and it is at least `S'` (the bound is sound). By hand:

| Count | Hand check |
| --- | --- |
| n = 28 | `S' = 728055577084257412127109150627/125·10^27 = 5.824444616674059297016873205016`, so `ceil₁₄ = 5.82444461667406`; exact form `291222230833703/5·10^13` |
| n = 37 | `6.59861960924437` |
| n = 50 | `7.57142857142858` = `378571428571429/5·10^13` |
| n = 53 | `7.82287565553230` = `78228756555323/10^13` |
| n = 69 | `8.82719465572974` |
| n = 83 | `9.63475764863109` |
| n = 87 | `9.83881526994827` |
| n = 124 | `11.65685424949239` |
| n = 300 | `17.82412338847855` |

**Byte identity.** The packet retains 125 certificates. `sha256sum` of all 125 matches `upstream-subtree.sha256`, `first-party-check.json` and `source-replay.json` (125 of 125 each). Exactly 77 match `ceiling-survey.json`. I spot-checked path-to-digest pairing against the manifest at `n = 50, 69, 83, 87, 124, 127, 129, 233, 260, 299, 300`, and against the survey at `n = 28` and `n = 300`. `n-17.cert` is absent.

**`n = 50` by hand.**

- Square 1 (row 3) has centre `x = (1 + 10^-20)/2` and `y = 7.07142857142857142864214285714285714`, `t = 0`. Its left clearance is `5e-21`, and its top clearance is `7.571428571428571428647142857143 − 7.57142857142857142864214285714285714 = 5.0e-21`.
- Squares 1 and 2 (rows 3, 4) are axis-aligned at `x = 0.5(1 + 10^-20)` and `1.5(1 + 10^-20)`, with gap `10^-20`.
- These agree with the receipts' least clearance `5e-21` and least gap about `1e-20`.

**Selection.**

- `considered` is 272, which is 321 certified − 48 improving − held `n = 17`.
- `moved` equals `CEILINGS`, the 77 in the claim, scopes and SYNOPSIS.
- `agreeing_after` (22) and `trailing_after` (55) partition them.
- Every integer verified ceiling left in `frontier/n-*.md` lies in a range where the best known side is the grid itself: `k² − k + 1 … k²` for `k ≤ 14`, and from `k² − k + 2` for `k = 15 … 18`, with 211, 241, 273 and 307 below the grid. None is a missed count.
- The `frontier/README.md` arithmetic holds: trailing cases fall from 78 to 56 (78 − 77 moved + 55 still trailing). The cases within one unit rise from 21 to 43.
- The test's `TRAILING_BY_CORPUS` values are 4 / 28 / 56. n ≤ 100: 29, 50, 53, 54. n ≤ 200: 27 closed forms up to 200 inclusive, plus 29. The largest trailing gap is now ≤ `1e-14`.

**`n = 29`.** It keeps its ceiling, correctly. The candidate `5.93383346267693` exceeds the interval bound `5.93383346267692918974379895098`, and `S'` itself lies above that bound by `5.0e-21` (by hand: `…18974|8798950979` against `…18974|3798950980`). It is the only `unmoved` row.

**`n = 69, 83, 87`.**

- The earlier ceilings come from `catalogue_upper_bounds.certification()` and match T-088 and T-089: `8.82719465572975`, `9.63475764863195`, `9.83881526994915`. They are `2e-14`, `8.7e-13` and `8.9e-13` above the printed sides, and the new values are below each.
- The certificates are solved from `witnesses/known-best/n-0NN.yaml`. Those witnesses are themselves the binary64 parse (`evand/square-packing@7ff3b21:site/www/data/p/square-69.json`) that T-088 certified. So "the same packing, refined on its active contacts" is accurate.
- The past-tense rewrites in `n-069.md` read correctly.
- The upper-gap `mathematics` blocker is gone at all three, because the new values agree with decimal reports.

**Blockers.** The diff removes exactly 77 upper-gap blockers: 74 "No formal certificate …" and the three T-088/T-089 blockers. It adds exactly 55 closed-form blockers. The 27 "Green's …" blockers are only reflowed.

**Closed-form gaps.**

- By hand, `n = 50` gives `S' − 53/7 = 7.5714285714…e-20` and `n = 53` gives `S' − (13 + √7)/2 = 7.8228756556e-20`, both matching the receipt.
- At all 55, the gap equals `S_exact·10^-20` to the receipt's four or five figures, from `7.5714e-20` to `1.7823e-19`. The printed range `7.6e-20` to `1.8e-19` is correct.
- None is negative, so no certificate's side falls below a closed form.

**Packings.**

- `largest_centre_displacement` is `7.072e-4`, printed as `7.1e-4`.
- Moved squares sum to 416 (357 plus `n = 299`'s 59). Of those, 332 are listed free, and the other 84 move by at most `1.19e-7` (printed `1.2e-7`). Of the 84, 55 are at `n = 299` after the squeeze.
- `all_matched_one_to_one` is true.
- `source_input` is the SLP squeeze at exactly 127, 129, 260 and 299.
- `source_status` is "bound only" at 230 and 261, so 75 counts are KKT local minima, as claimed.
- `witness_source_key` is "Kingbird derived numerical facts" in all 77 rows.

**Controls.**

- There are 231 rows (77 × 3), all with `as_expected: true`, and `overlap_controls_inside_the_box: true`.
- Units run from `1e-30` to `1.6e-28`.
- The least wall clearance of a moved square is `0.7114`.
- `wall_seconds` is 4,695.9.
- The shrink-past control (side − top/right clearance − unit) is provably invalid by its construction.
- The one-unit shrink is provably valid, because every top/right clearance (about `5e-21`) exceeds the unit and nothing else changes.
- Every row reports all four verdicts as stated.

**Wording and arithmetic in the prose.**

- "Above the printed side by up to 0.464 at n = 101, 122, 145, 170, 197, 226, 257, 290 and 291": these are exactly the counts whose printed side ends in `.5355…`, with gap `0.46447`. Every other moved count's grid gap is smaller.
- "2e-14 to 8.9e-13" (T-088/T-089 margins): correct.
- "555 files" pinned by digest only: equals 632 − 77, and `sources.json` lists 555 paths.
- Coverage entries list each certificate as a superseded report of `kingbird-current`, citing T-118. That matches the claim.
- No register `claim`, `composition` or `next_rung` written here uses "confirmed" without a kind. The claim names both kinds ("independently re-implemented"; "reproduced with the producer's code").

**Composition and rungs.** V3/C3 with two machine entries of one method (exact rational decision) and no reviews yet follows T-098.

**Significance.** I confirm **S2**. T-118 moves no best known side and no theorem, so it does not reach S3, unlike T-056, whose S3 rests on 49 lowered best known sides. It lowers 77 verified ceilings, 74 of them off the integer grid by up to 0.464, and the project records the verified ceiling as a quantity of its own. That is more than bookkeeping (S1), and on par with T-098 and T-088 (both S2). The rationale should be reworded per EC-4.

## Not Checked

- Deciding any certificate in full by code of my own. Code execution was refused, so the record still has no certificate decided by code that shares nothing with the tools under review.
- Re-running `survey`, `survey_problems`, `check --check`, `controls`, or any test.
- Whether the rule fails to lower the ceiling at each of the 195 non-moved counts. I checked only the integer-ceiling counts, by scan; non-integer ceilings rest on `survey_problems`, which I read but did not run.
- The CPU-time splits: 838 of 2,820 seconds and 59 of 202.
- The `4.3 MB` and `2.0 MB` sizes.
- The generated `STATUS.md`, `INVENTORY.md`, `VERIFIERS.md`, `RESULTS.md` and site output.
- Whether the five other rational closed forms (171, 198, 230, 261, 293) have exact points on rational grids like `n = 50`'s.
- Pre-existing and outside this branch: `n-069.md`'s packing section ("Found by Maurizio Morandi in 2010. Improved by David W. Cantrell in August 2023") and its atlas line ("Morandi et al.") do not name Ellsworth's optimization, which T-088 credits.

defect-open

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
