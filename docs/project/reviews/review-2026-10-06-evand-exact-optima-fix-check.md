# Fix Check: The Review of T-098, Evan Daniel’s Exact Optima

I am Claude Opus 5.5 (`claude-opus-5-5`), running as the tbd-strong sub-agent at that tier's configured reasoning setting (xhigh in its agent definition). I was prompted separately from the lane that registered and fixed T-098 and from the reviewer who wrote the review. I worked read-only in the detached worktree at `aa9fb46dc` (branch `claude/ecstatic-pascal-pothtx-exact`).

**What I read.**

- The review `docs/project/reviews/review-2026-10-06-evand-exact-optima.md`.
- `git show 65bb9851b`: the code, test, record, bibliography and packet README diffs in full; the receipt diffs in part.
- `git show aa9fb46dc`: all 96 changed lines.
- T-098 in `packing/frontier/results.yaml`, and T-094's `reviews:` block for comparison.
- `packing/frontier/n-126.md` in full, plus the fix diffs at n = 103, 206, 211, 259, 263 and 305.
- The committed receipts: `reproduction-sample.json` at `4421c513f` and at `aa9fb46dc`, the overlap rows and header of `negative-controls.json`, and the summary keys and several rows of `register-comparison.json`.
- The source's batch `README.md`, the Method and Test-set legend of `s12/search/exact/README.md`, and the rows of `results.md` for n = 68, 126, 177, 211, 263 and 305.
- The acquisition entries for `summarize.py`.
- `check_case_semantics` and `_conjecture_errors` in `sqpack/assurance.py`, and their callers.
- Every non-null `conjectured_optimum` under `packing/frontier/`, and the verified ceilings at the closest of them.

**What I could not run.** This session's permission layer refused all of the following, so this check rests on reading:

- every Python invocation (`.venv/bin/python3`, including `--version`);
- `zcat` and `gzip -dc` of the batch's `results.json.gz`;
- `gh issue view 375`;
- several compound shell pipelines.

As a result:

- **No tests or schema checks ran.** I ran neither the tests nor `validate_schemas`.
- **The per-count KKT reports are unread.** I could not read the `status` and `second` fields of `results.json.gz` (see EX-11).
- **No certificate was decided by this check.** The review's What Remains item, a decision by code that shares nothing with the tools, is still open. It is a gap in confirmation, not a finding against the fixes.
- **n = 17.** By instruction I did not read or replay the n = 17 certificate, and I say nothing about it.

## EX-1 (blocking): n = 126 kept a refuted `conjectured_optimum`

**What the review asked.**

- Null the conjecture in `front_matter` and regenerate n = 126.
- Add a record check that a non-null conjecture lies within `[verified_lower_bound, verified_upper_bound]`.

**What the fix did.**

- **The record.** `n-126.md:72` is now `conjectured_optimum: null`.
- **The layer.** `apply_exact_optima.front_matter` sets it to null at all 48 counts.
- **The guard.** `_conjecture_errors`, called from `check_case_semantics` (so `validate_schemas` runs it on every case), refuses a decimal conjecture that exceeds the decimal `value` of the verified ceiling by more than half a unit in its last place.
- **The tests.** Two tests at the end of `test_evand_exact_certificates.py`.

**The tolerance.** Half a unit is the right allowance for a display rounded to nearest. A displayed `d` within half a unit of a true conjecture `c ≤ U` gives `d − U ≤ ½ ulp`. The catalogue truncates rather than rounds: `source-coverage.yaml:1339` calls `11.77473513240654` "the truncation" of `11.774735132406546`. Truncation never exceeds the true value, so the allowance is generous there, not tight.

**Can it refuse a correct record?** Only if a verified ceiling's `value` were written rounded down. The ceilings I read are exact or rounded up, so I found no such record.

**Does any other record trip it?** I checked the closest cases by hand:

| n | Conjecture | Verified ceiling | Trips? |
| --- | --- | --- | --- |
| 69 | `8.82719465572973` | `8.82719465572975` | No |
| 83 | `9.63475764863108` | `9.63475764863195` | No |
| 87 | `9.83881526994826` | `9.83881526994915` | No |
| 52 | `7.70710678118654` | `7.70710678118654752…` | No |

Every other decimal conjecture I listed sits under an integer grid ceiling. That agrees with the commit's "n = 126 was the only record it caught", but I could not execute `validate_schemas` to confirm it over all records.

**Can it pass a contradicted record?** Yes, in three ways:

- It checks only the ceiling, not the floor the review asked for.
- It skips non-decimal conjectures (`integer`) and non-decimal ceilings without comparing them. My spot checks of `integer` records (n = 12, 30, 74, 95, 112, 138, 189, 319) found every ceiling equal to `⌈√n⌉`, so nothing is wrong today.
- The tests never exercise the tolerance band (FX-4).

**A note on history.** The record no longer says anywhere that the catalogue conjectured de Winter's packing optimal. Nulling the value follows the review's fix, but one sentence in the body would keep that history.

**Resolved.** The contradiction is gone, the layer cannot reintroduce it, and the guard refuses this case. The missing lower half of the guard and the untested tolerance are non-blocking (FX-4).

## EX-2: displacement bounds rounded to nearest

**The fix.**

- `pose_match` stores each maximum rounded up to four significant digits (`round_up`).
- `section` prints them rounded up again to two (`_bound`).
- Rounding up twice can only loosen a bound, never understate it.
- The `log10` exponent can only err toward fewer digits, which is still a round-up.

**Checked against the regenerated receipt.**

| n | Bound | Receipt | Written |
| --- | --- | --- | --- |
| 103 | largest | `1.441e-3` | `1.5e-3` |
| 103 | non-free | `2.544e-5` | `2.6e-5` |
| 103 | unmoved | `1.024e-11` | `1.1e-11` |
| 126 | largest | `5.492e-4` | `5.5e-4` |
| 126 | unmoved | `6.445e-11` | `6.5e-11` |
| 206 | largest | `1.415e-4` | `1.5e-4` |
| 206 | unmoved | `5.412e-12` (review) | `5.5e-12` |
| 259 | non-free | `8.029e-8` (review) | `8.1e-8` |
| 263 | non-free | `4.136e-5` | `4.2e-5` |
| 305 | non-free | `1.329e-5` (review) | `1.4e-5` |
| all | non-free | `4.136e-5` | `4.2e-5` (packet README) |
| all | unmoved | `9.192e-9` | `9.2e-9` |

T-098's claim, "within `1.5e-3`" and "within `4.2e-5`", holds against these. The one figure that does not match its receipt is the packet README's "at most `1.442e-3`" (FX-2). It is still a true upper bound.

**Resolved.**

## EX-3: frontier README miscount

The sentence now reads "exact optima of 47 of those packings and of de Winter’s n = 126". That is 46 of Couzo's packings plus de Winter's n = 211, then n = 126: 48.

**Resolved.**

## EX-4: reproduction-sample figures not in the receipt

**The fix.** The reproduction sample was re-run, and the receipt now carries `cpu_seconds: 178.3`, `workers: 2` and a per-row `largest_tangent_difference`.

**Checked against the receipt.**

- **CPU total.** The rows sum to 4.3 + 11.3 + 20.2 + 66.2 + 76.3 = 178.3.
- **Same certificates.** All five `produced_sha256` values are identical to the receipt at `4421c513f`, so the re-run regenerated the same certificates.
- **Packet README.** It now says "178 CPU seconds in all on two workers", "centres by at most `2.5e-24`" (receipt `2.466e-24`) and "tangents `t` by at most `3.3e-24`" (receipt `3.208e-24`, rounded up). All three agree with the receipt.
- **Unaffected sentence.** A `|Δt|` of `3.2e-24` moves a corner by well under `1e-23`, so "far inside the `1e-20` gaps" stays true.

**What was missed.** The review named the T-098 notes as a second location. They are unchanged: `results.yaml:8720–8721` still says "squares within 2.5e-24 of the retained ones", which the tangent difference of `3.208e-24` exceeds (FX-1).

**Partly resolved.**

## EX-5: Ellsworth statement attributed to the wrong file

**The fix.** The bibliography note now credits the solver's README with Ellsworth's "nested Jacobian-determinant conditions" (its Method, step 3), and the issue with "his analytic minimisation reimplemented". This matches the packet README's Credit row.

**What I could not confirm.** The issue's wording, since `gh` was refused. The issue's text is not retained in the packet, so neither reviewer has read it.

**Resolved**, as an attribution, subject to that reading.

## EX-6: overlap control's cause of refusal not recorded

**What the review asked.** Record each checker's failure message and the mutant's least wall clearance.

**What the fix did.**

- **What it recorded.** The receipt now has each overlap control's `moved_square_wall_clearance` and a header flag `overlap_controls_inside_the_box: true`.
- **How it was added.** `annotate_controls` regenerates each mutant from its retained certificate, requires the recorded digest, and adds the exact clearance of the moved square's corners. It decides nothing again.
- **What the receipt shows.** All 48 values are positive. The least is `1.0729e-20`, at one count; every other is at least `0.907`. The evidence entry and packet README state the least as `1.07e-20`.

**Judging the departure.** The argument is sound:

- The unmodified certificate passed every check, and only one square moved.
- That square's corners all lie strictly inside the open box.
- So no checker, strict or closed, can refuse the mutant for a wall. Its refusal must come from a pair involving the moved square.
- `overlap_control` confirmed a negative exact gap for the tightest pair before returning, so a sound checker must refuse it.

Failure messages would add nothing this argument does not already establish.

**Resolved.**

## EX-7: the `verify_all.sh` conclusion went too far

**The fix.** The packet README and the source-replay evidence now say that `summarize.py`, which wrote the ✓✓ column, makes the same `'VALID' in` test on the last line. They also say that, held to its exit status, `verify_cert.py` accepts all 320.

**What I could not confirm.** `summarize.py` is pinned by digest only (4,926 bytes, `79c8ab9c…`). It is not retained, so I could not check what it tests (FX-7).

**Resolved** in wording. The supporting fact rests on an unretained file.

## EX-8: the hold's wording

**The fix.**

- The packet README now says "not pinned by digest", and that the commit pins the whole tree.
- `s12/search/exact/README.md` now stands beside `results.md` and `results.json` among the retained files that keep their n = 17 rows.

**Resolved.**

## EX-9: the listed witness does not attain the reported value

**What the review asked.** Either register the certificate as a rational witness, as T-088 did, or state in the witness entry that it pictures the finder's pose and certifies only the earlier side.

**What the fix did.** Each of the 48 bodies now says: "The known-best witness this record lists is that binary64 pose, at the side its finder prints; the witness of the side above is the certificate itself."

**Judging the departure.**

- **For a reader of the body,** the sentence is accurate and enough.
- **The front matter is unchanged.** `reported_upper_bound.witnesses: [W-known-best-nNNN]` still sits under a `value` of `S'`.
- **The witness entry is unchanged.** `witnesses/known-best/n-126.yaml` still says `side: '11.774735132406546'`. So a machine reader of the record still finds a witness that does not attain the value it is listed under.
- **A small inaccuracy.** At n = 126 the witness's side is not exactly "the side its finder prints": the catalogue prints the truncation `11.77473513240654`.

Neither of the review's two options was taken, though the review itself called the finding non-blocking.

**Partly resolved.**

## EX-10: nits

- "Least pair gap about `1e-20`" is now used in the evidence and the packet README.
- The source replay's figure for the 48 is "54" (receipt 54.1).
- The module docstring now limits the common mode to the parse and the map from `t` to `(c, s)`. It also discloses that `controls` copies the source's checkers into a scratch tree.

**Resolved.**

## EX-11: the KKT sentence overstated the curvature

**What the review asked.** Write "non-negative".

**What the fix did.** The sentence now reads "a reduced Hessian positive definite once its exact flat motions are set aside (its per-count report)".

**Judging the departure against the source's own files.**

- **The source's vocabulary supports it.** The Test-set legend of `s12/search/exact/README.md` defines "exact flat modes" as "zero modes verified to be exact motions at fixed S". It separates `PD (strict)` from `PSD, k exact flat modes`.
- **The reading follows.** A reduced Hessian that is PSD, with every zero mode an exact flat motion, is positive definite on the complement of those motions. The batch README's "PSD/PD modulo exact flat motions" reads naturally as "one of those two cases".
- **On that reading, the new wording is better than the review's.** "Non-negative" would understate the counts the source reports as PD.

**What I could not verify.**

- **The 44 per-count reports.** My attempts to decompress `results.json.gz` were refused, so I could not check that each KKT count's `second` field says PD, or PSD with all zero modes exact. The Method section (step 5) lets negative modes be "tested against the critical cone". A count classed as a KKT local minimum on that basis would make the sentence false there.
- **Nothing enforces it.** The layer picks the sentence from `status` alone (`apply_exact_optima.py:158–161, 370`), so no code checks the parenthetical "(its per-count report)" against the report (FX-3).

**Partly resolved.** The wording is sound against the source's definitions. It is unverified here against the per-count fields, and nothing guards it.

## New Findings

**FX-1 (non-blocking): the T-098 notes keep the reproduction figure EX-4 named.**

- **Location.** `packing/frontier/results.yaml`, T-098 `notes`, lines 8720–8721.
- **Defect.** It says "regenerated each certificate with the same S' and squares within 2.5e-24 of the retained ones". The receipt's `largest_tangent_difference` is `3.208e-24` at n = 211.
- **Fix.** Write "centres within 2.5e-24 and tangents within 3.3e-24", as the packet README does.

**FX-2 (non-blocking): a displacement figure that is in no receipt.**

- **Location.** `packing/resources/web/evand-square-packing-2026-10-05/README.md:89`, "the largest centre displacement is at most `1.442e-3`".
- **Defect.** The receipt's top-level value and its n = 103 row are both `0.001441`.
- **Fix.** Write `1.441e-3`, or `1.5e-3` as the claim does.

**FX-3 (non-blocking): the KKT sentence cites a field the layer never reads.**

- **Location.** `packing/devtools/apply_exact_optima.py`: `statuses()` (lines 158–161) and `KKT` (lines 106–113).
- **Defect.** Every count whose `status` is `KKT local min` gets "a reduced Hessian positive definite once its exact flat motions are set aside (its per-count report)", whatever its `second` field says.
- **Fix.**
  - Read `second` beside `status`.
  - Refuse a KKT count whose report is neither PD nor PSD with only exact flat modes.
  - Add a test over the 44 counts.

**FX-4 (non-blocking): the guard's tolerance is untested, and its scope is narrower than the review asked.**

- **Location.** `packing/tests/test_evand_exact_certificates.py`, the last two tests, and `packing/src/sqpack/assurance.py`, `_conjecture_errors`.
- **Defect.** Both decimal cases in `test_a_conjecture_at_the_ceiling_to_its_last_place_is_kept` lie below the ceiling. Removing the tolerance entirely, or changing `/ 2`, still passes every test. The guard also leaves out the floor of the review's proposed interval, and skips non-decimal conjectures and ceilings without saying so.
- **Fix.**
  - Add `11.774735132387833` (`1.6e-16` above the ceiling, inside `5e-16`: kept).
  - Add `11.77473513238784` (`7.2e-15` above, outside `5e-15`: refused).
  - Either check the conjecture against `verified_lower_bound` too, or state the one-sided scope in the docstring.

**FX-5 (non-blocking): the packet README's Review section overstates the fix.**

- **Location.** `packing/resources/web/evand-square-packing-2026-10-05/README.md`, `## Review`.
- **Defect.**
  - "Refuses any decimal conjecture above its record's verified ceiling" omits the half-unit allowance.
  - "Each is fixed in the same pass" is not true of EX-4 (FX-1). EX-9 was met in body prose only, and EX-11 rests on an unread field (FX-3).
- **Fix.** Say "by more than half a unit in its last place", and name what remains open.

**FX-6 (non-blocking): T-098 does not record its review.**

- **Location.** `packing/frontier/results.yaml`, T-098: no `reviews:` entry; `next_rung` (line 8706); `significance.by` (line 8673).
- **Defect.**
  - The committed review is not listed with its verdict, as T-094's is.
  - `next_rung` asks for a reviewer "distinct from the one of 2026-10-05", but the review is dated 2026-10-06.
  - `significance.by` is still the lane's draft, although the review confirmed S2.
- **Fix.** Add the `reviews:` entry (adversarial, 2026-10-06, `defect-open`, then this fix check), correct the date, and credit the S2 confirmation.

**FX-7 (non-blocking): the `summarize.py` statement rests on a file the packet does not hold.**

- **Location.** The packet README, "The source’s own driver", and the source-replay evidence.
- **Defect.** "`'VALID' in` the last line" cannot be checked from the packet, which pins `summarize.py` by digest only.
- **Fix.** Retain `summarize.py` (4,926 bytes), or quote its test line with the file's digest.

## Disposition

`defects-resolved`

The one blocking finding, EX-1, is resolved:

- n = 126 no longer conjectures a side its own certificate refutes.
- The exact layer nulls the field at all 48 counts.
- `sqpack.assurance` now refuses that contradiction, with an allowance that is correct for displays rounded to nearest or truncated. No other record I checked comes near it.

EX-2, EX-3, EX-5, EX-6, EX-7, EX-8 and EX-10 are resolved; the EX-6 departure is sound by the argument given there. EX-4, EX-9 and EX-11 are partly resolved: one stale sentence in the T-098 notes, a front-matter witness still listed under a value it does not attain, and a curvature sentence nothing checks against the per-count field. All are non-blocking, and so are the seven new findings.

Two limits apply. This check executed nothing, so neither the tests nor `validate_schemas` were run here. And no certificate has yet been decided by code that shares nothing with the tools under review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
