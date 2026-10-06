# Fix Check: Evan Daniel's Exact Certificates as Verified Ceilings (T-118)

**Reviewer.** I am Claude Opus 5.5 (`claude-opus-5-5`), run as the tbd-strong sub-agent tier, whose configured reasoning setting is xhigh. I was prompted separately to check the fixes. I share no context with the lane that registered T-118 and made the fixes, or with the reviewer who wrote `review-2026-10-06-evand-exact-ceilings.md`. I worked from the brief, `AGENTS.md`, and the committed record.

**Commit read.** `27994978d` on `claude/ecstatic-pascal-pothtx-r8`, in a detached worktree. I read the whole of `git diff a91d9b385..27994978d`, which covers the fix commits 4afa30a7a, 90d8e250a and 27994978d, plus 1e2d89334, which stores the review.

**What I could and could not run.** The session refused every invocation of the project interpreter (`packing/.venv/bin/python3`, with or without `nice -n 15`). It also refused piped `grep | sort | uniq` commands. I could run `git diff`, `grep`, `wc` and `head -c … | sha256sum`, and I read files. So I re-ran no tool, test, `survey` or `survey_problems`, and decided no certificate. I checked n = 50's certificate by reading all 50 rows and doing exact decimal arithmetic by hand.

**`n = 17`.** I did not open, read, decide or comment on any n = 17 certificate, input or record.

## Verdict

The fixes resolve the blocking finding, EC-1. The claim, blockers, case-record ceiling sections, packet README, docstrings and `next_rung` now split the 55 closed forms into 49 irrational and 6 rational ones. That split is correct, and each irrational form is irrational by elementary argument, not only by SymPy. The README's account of n = 50's certificate is true as written: I checked it row by row. Of the six non-blocking findings:

- **Resolved:** EC-2, EC-3, EC-4, EC-5 and EC-6.
- **Resolved where the review pointed (README and evidence):** EC-7. The claim, the controls receipt and the tool docstring keep the older wording.

I raise four new findings, none blocking:

- **FC-1:** the remedy at the five rational counts other than n = 50 is stated more firmly than anything checked.
- **FC-2:** the n = 50 measurement lives in prose only.
- **FC-3:** `survey_problems` no longer checks the survey receipt's own digest column.
- **FC-4:** a "within 1e-10" tolerance hides two squares that sit about 8e-17 off the grid.

## EC-1 (blocking): "no rational certificate reaches" at the six rational closed forms

**Disposition: resolved.**

The sentence is gone from every place the review listed:

- **Claim.** It now says: "Forty-nine of those closed forms are irrational, which no rational certificate reaches; the other six, at n = 50, 171, 198, 230, 261 and 293, are rational, which a rational certificate that closes the packing's contacts exactly would reach." It also gives the cause of the gap: "the certificate's outward rounding".
- **Blocker template.** `trailing_blocker` now branches on `printed_exact_form_degree`. At n = 50 the blocker reads "a rational side, which this certificate, rounded outward, does not reach … needs a rational certificate of the packing that closes its contacts exactly". At n = 53 and n = 127 it reads "an irrational side, which no rational certificate reaches".
- **Other places.** The module docstring, the README's "What they carry" and "Not Done Here", `next_rung`, and every case record's ceiling section were changed the same way.

`grep` over the tree finds no remaining unqualified "no rational certificate" outside the stored review.

**The 49/6 split.** `closed_form_degree` parses the catalogue form with SymPy's `parse_expr`, using implicit multiplication so that `(5/2)sqrt(2)` and `4 sqrt(2)` parse. It then returns the degree of `sp.minimal_polynomial`, and degree 1 means rational. The regenerated `ceiling-survey.json` carries `printed_exact_form_degree` on all 77 rows:

| Rows | Degree |
| --- | --- |
| 22 decimal-only rows | null |
| n = 50, 171, 198, 230, 261, 293 (`7 + (4/7)`, `13 + (4/7)`, `14 + (4/7)`, `15 + (28/41)`, `16 + (28/41)`, `17 + (26/41)`) | 1 |
| every `a + b·sqrt(2)` and `a + b·sqrt(7)` form, b ≠ 0 | 2 |
| n = 54, 107, 178, 267 (`k − (1/2)sqrt(2) + sqrt(1 + sqrt(2))`) | 4 |

That makes 55 closed forms, 6 rational and 49 irrational. I confirmed the irrationality independently of SymPy:

- `a + b√2` and `a + b√7` with rational b ≠ 0 are irrational.
- For the degree-4 forms, rationality would put √(1+√2) in Q(√2). That is impossible, because 1+√2 has norm −1, which is not a square in Q.

The test `test_every_closed_form_lies_below_its_certificate_and_six_are_rational` pins the six counts and the blocker wording. SymPy is in the `dev` group of `pyproject.toml`, which is the group the gate runs.

**The packet README's account of n = 50.** I read all 50 rows of `n-50.cert`.

- **Side.** S' = 7571428571428571428647142857143/10^30. Expanding (53/7)(1 + 10^-20) exactly gives the fractional digits `571428571428571428 64 7142857142|857142…`, with digit 19 carried from 5 to 6. Rounded up at 30 decimals, that is S' exactly. So S'/(1 + 10^-20) exceeds 53/7 by less than 10^-30. "53/7 rounded up" is a fair description.
- **Free squares.** The source's free list for n = 50 (0-based, from the survey's `pose.moved.squares`) is [5, 19, 23, 26, 32, 46], which is certificate rows 8, 22, 26, 29, 35 and 49. That leaves 50 − 6 = 44 non-free squares, as stated.
- **Tangents.** Every non-free row has t = 0 or t = 33333333333333333333333333333333333/10^35. The second is 1/3 − 1/(3·10^35), within 1e-30 of 1/3. No non-free row has a negative t or t near 3. So "0, ±1/3 or ±3" is true but wider than n = 50 needs. t = 1/3 gives (c, s) = (4/5, 3/5), a rational rotation. The free rows carry t ≈ −5.0e-5, 0.33329889, 0.33333333333333332076 and 0.33324888, none within 1e-30 of the listed values, which is consistent with their being free.
- **Centres.** For every non-free row, x·350 and y·350 are integers to the printed digits once the scaling is undone, for example:
  - row 20: 1143 and 2151;
  - row 23: 1409 and 1913;
  - row 47: 1507 and 499;
  - row 52: 1759 and 1213;
  - the axis-aligned rows: multiples of 175, plus 2475, 2125, 1775 and 1425.

  Nearly all match k/350 · (1 + 10^-20) to all 35 printed digits. Rows 27 and 28 do not. Their unscaled centres lie (−6.4e-17, −4.8e-17) from (1465/350, 1430/350) and from (1185/350, 1220/350). That offset is 1.6e-17·(−4, −3), a slide along the squares' own 3-4-5 edge direction. "Within 1e-10" covers it, but see FC-4.

The hedge in `next_rung` and the README ("appears to be one") is the right strength. Nobody has decided the snapped packing at side 53/7.

## EC-2 (non-blocking): n = 29 described as an "interval enclosure of the exact optimum"

**Disposition: resolved.** The notes, the packet README, the module docstring, the test docstring and `frontier/README.md` now say "interval-certified bound (`E-n029-interval-certified-upper`)". The receipt's `unmoved` row shows `certified_above_verified_by: 5e-21` and the evidence `E-n029-interval-certified-upper`, which matches "lies 5e-21 below S'". The phrase "interval enclosure of the exact optimum" no longer appears in T-118's text.

## EC-3 (non-blocking): nothing refuses a certificate below a closed form

**Disposition: resolved.**

- **The refusal.** `survey` now raises when `_closed_form_gap(...)` is not positive. It does so before the row is written, in the branch that moves a count. That is the only branch where such a certificate could be filed as a ceiling.
- **The arithmetic.** The gap is computed at `DIGITS + 10` = 70 decimal digits. Gaps of order 1e-19 keep their sign, and anything that underflows to 0 is refused, which is the conservative direction.
- **The test.** The new test asserts `certified_above_exact_side_by > 0` at all 55 rows. It exercises the committed receipt, not the refusal path on a constructed bad input. That is what the review asked for, though it is weaker than a test that feeds `survey` a bad certificate.

## EC-4 (non-blocking): the rationale's "onto the report itself at 22"

**Disposition: resolved.** The rationale now reads "to within one unit of the report's last place at 22", which matches the claim's own wording. The score stays S2. The `by:` line now cites the review as "confirms the registering lane's draft", the form used throughout the register. The review did confirm S2. It also asked for exactly this reword, so "confirms the draft, reworded per EC-4" would be more exact, but this is not a defect.

## EC-5 (non-blocking): dropping `E-kingbird-upper-register` from T-088 and T-089

**Disposition: resolved.** Both notes now say each entry is "superseded … as a ceiling; the packing it registered stays the best known, and the catalogue's printed side of it the reported bound". They also say that the review of 2026-10-05 accepted them while they cited `E-kingbird-upper-register`, and why that citation was dropped. That covers both consequences the review named.

## EC-6 (non-blocking): departures from the register-action table

**Disposition: resolved.** T-118's notes name both rows, quoting them as they stand at `result-import.md` lines 234 and 242:

- "Bounds of one kind at several counts in one release", with T-046's widening;
- "below the standing bound and asking for no work".

The notes say the owner's decision overrides the second.

## EC-7 (non-blocking): the overlap control's invalidity, partly established by a decider under test

**Disposition: resolved in the README and the evidence entry, where the review pointed.**

`E-evand-exact-ceilings-2026-10-05-exact-replay` and the README's controls paragraph now say three things:

- the mutant moves "along the pair's best separating face axis by that axis's gap plus one unit";
- the independent checker's refusal of it is circular;
- it is invalid regardless, because the edge normals are rational unit vectors and a negative gap on every face axis means the interiors meet by the separating-axis theorem.

I checked `tightest_pair` (`evand_exact_certificates.py:807`). It takes, per pair, the largest projection gap over the four face normals and returns that axis, so the new wording describes the code. The separating-axis argument is sound for two convex polygons.

Three places keep the older wording:

- the claim ("moved one unit of the side's denominator past touching");
- `overlap_control`'s docstring ("closing normal");
- the `what` field of `negative-controls-ceilings.json` ("closing normal").

The receipt is a dated run output and the control code is shared with T-098, so leaving them is defensible. A reader of the claim alone still gets the looser phrase.

## The `reviews` List, `external_review` and *Confirmed*

**`reviews`.** T-118's new entry records the review faithfully:

| Field | Value | Matches the review? |
| --- | --- | --- |
| `kind` | `adversarial` | yes |
| `reviewer_kind` | `ai` | yes |
| `relation` | `project` | yes |
| `date` | 2026-10-06 | yes |
| `verdict` | `defect-open` | yes |
| `covers` | `[T-118]` | yes |
| `scope` | at a91d9b385 against 7f2a01816; n = 50 by hand; the session refused the project interpreter, so nothing was re-run | yes |

The scope also names "bibliography rows", which the review does not mention. It names only coverage entries. That is a trivial overreach. With a `defect-open` review on file, `result_status` correctly derives T-118's status as `incomplete` in `RESULTS.md`, in place of the earlier "confirmed, independently re-implemented". That is the intended state until a fix check is recorded.

**`external_review`.** The new entry on `E-evand-exact-ceilings-2026-10-05-report` follows the T-098 precedent: `informally-verified`, the same reviewer description, and the review's path. Its note states the review's findings accurately, including:

- the bound and the rounded values follow from the receipts;
- the selection is right;
- 125 digests match;
- n = 50's clearances and gap were checked by hand;
- the session was refused the interpreter.

"No defect in the source's certificates" is fair, since the review raised none. "Since reworded" was not yet confirmed when it was written; this check now confirms it.

**Confirmed.** The only added line that contains "confirm" is the significance `by:` line ("confirms the registering lane's draft"). That is about the score, not a verification status, and it is the register's standard form. No changed text uses *confirmed* as a verification word without its kind. The old "confirmed, independently re-implemented" in `RESULTS.md` was replaced by the derived `incomplete`.

## New Findings

### FC-1 (non-blocking): the remedy at n = 171, 198, 230, 261 and 293 is asserted, not checked

The blockers, ceiling sections, README "Not Done Here", claim and module docstring say the gap at the six rational counts needs, or would be closed by, "a rational certificate of the packing that closes its contacts exactly". The docstring says "only one that closes its contacts exactly". A rational side does not by itself make the packing's exact point rational: its coordinates and rotations could still be irrational algebraic numbers.

That has been looked at only at n = 50, and even there only as "appears". Neither the review nor the fixes opened the other five certificates. I could not tabulate their tangents, because the session refused the pipeline. At those five, an exact certificate at the closed-form side, rational if the exact point is, is what is needed.

Suggested wording: "would be reached by an exact certificate at that side; at n = 50 a rational one appears to exist". This is the review's own suggested wording carried one step too far, and it does not affect the bound.

### FC-2 (non-blocking): the n = 50 measurement lives only in prose (OR-1)

The README states a specific measurement: centres within 1e-10 of a 1/350 grid, tangents within 1e-30 of 0, ±1/3 or ±3, and side 53/7 rounded up. It marks it "checked here". No tool, test or receipt in the diff performs this check: there is no "350" in `apply_exact_ceilings.py`, `evand_exact_certificates.py` or the test. The statement is true (see EC-1), but under OR-1 it should come from a retained check, such as a test over `n-50.cert`, rather than from one-off code.

### FC-3 (non-blocking): `survey_problems` dropped its check of the survey receipt's digest column

Commit 90d8e250a replaced this condition:

```python
certificates.sha256(path) != row["sha256"] or row["sha256"] != first[n]["sha256"]
```

with `not certificates.is_decided(path, n)`. That still ties the retained file to the first-party receipt, which is the download boundary OR-16 keeps. But `ceiling-survey.json` still carries a `sha256` field on all 77 rows, and nothing now checks that field. A wrong or hand-edited digest there would pass `survey_problems`. The field should either be checked against `is_decided`'s source or dropped from the row.

### FC-4 (non-blocking): "within 1e-10" hides two squares 8e-17 off the grid

At n = 50, 42 of the 44 non-free squares sit on k/350·(1 + 10^-20) to all 35 printed digits. Rows 27 and 28 are not listed free, have t = 1/3, and are displaced 8e-17 along (−4, −3)/5 from their grid points. The README's 1e-10 tolerance is true but loose enough to hide this. That matters for "appears to be one", because the snapped configuration has not been decided. One clause naming the two squares and their offset would make the hedge visible.

## Not Checked

- Running anything with the project interpreter: `survey`, `survey_problems`, `check --check`, the new test, `closed_form_degree` itself, or the validation tiers. I read the receipt's degrees and checked them by hand.
- Whether the certificates at n = 171, 198, 230, 261 and 293 have rational rotations or rational grids (see FC-1).
- Whether the case records' regenerated text matches what `ceiling_section` and `trailing_blocker` would write at all 55 counts. I read n = 50, 53 and 127 and the generated `RESULTS.md` rows.
- The generated `INVENTORY.md`, `STATUS.md` and site output, beyond the one `INVENTORY.md` row in the diff.
- That the 2026-10-05 review of T-088 and T-089 accepted them while they cited `E-kingbird-upper-register`, as their new notes say. I took this from the T-118 review.

I did check the `.flowmarkignore` statement about the stored review: the first 19,174 bytes have SHA-256 `f681eaca2c79c931…`, and the file is 19,307 bytes including the footer.

defects-resolved

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
