# sqverify-fast Declared Nets: Re-Check of the Fixes for DR-1 to DR-3 (`36b52538a`) and the Proposed Flip

**Verdict: accept the fixes** of `36b52538a` for DR-1, DR-2 and DR-3, and **accept the
flip** (`proposed-flip.patch`, `declared_nets=True` on `d97758bb…`). Two wording
corrections (FC-2, FC-5) and one generated-file repair (FC-7) belong in the same commit.
FC-7 is the only finding that blocks a merge: `36b52538a` leaves `SYNOPSIS.md`’s
document map stale, so the edit tier fails on it.

- **DR-1 is fixed.** `mixed_exact` and everything that feeds it now evaluate on the net
  the file declares, and the census control refuses a row whose decided step differs
  from the file’s. On `mixed_n18_L470` the evaluator, a second exact evaluator written
  for this re-check, and the crate’s probe agree exactly at 12 of 12 poses on the
  declared net. On the standard net, the full `check_sqverify_fast --only mixed` output
  is byte-identical to `34e87a86b`’s, apart from the wall-time line.
- **DR-2 and DR-3 are fixed.** Every count, step and net sentence of `--evidence` is now
  read from the row, and the build sentence comes from the reviewed source the row was
  built from. `--evidence` refuses a row of an unreviewed source, and it refuses a
  declared-net row of a source whose review did not read the declared net.
  One sentence about `d97758bb…` is imprecise (FC-2).
- **`net_problems` implements checklist (b)’s net items**, lemma N0’s (a) to (e)
  included, and admits nothing the checklist excludes.
  Some of its conditions have no negative case in the tests (FC-4).

The control receipt in the scratch directory for the declared-net certificate
`mixed_n18_L470` is `CONTROL_FAILED`, and DR-1 is not the cause.
`captures_agree` is true.
The 99/100 mutant is verified at index 408, because the certificate has more than 1%
slack at that direction: the crate certifies the mutant there, and its refusals at 230
other directions all carry exact witnesses below 1. The control picks its index by the
least certified lower bound, which on a verified direction is a termination margin and
says nothing about tightness (FC-1). This fails closed.
It does not block the flip.
It does mean that `--control` as written cannot give `mixed_n18_L470` a
`CONTROLS_REFUSED` receipt, and that it may not give one for wand125’s `mixed_n18_L4704`
or `mixed_n19_L48229` either.
A change to how the control chooses its direction or its scale is a change to control
logic and needs a reviewer.

This re-check was written on 2026-10-06 by an AI agent (model `claude-opus-5-5`,
tbd-strong tier), separately prompted for lane R1 of the 2026-10-06 intake round.
It shares no context with that lane, with the lane that wrote the fixes, or with the
soundness review it re-checks.
It registers nothing and moves no bound.

## Scope and Evidence

The subject is `36b52538a` against its parent chain from `34e87a86b` (`origin/main`).
`307d934aa` adds the soundness review byte for byte, and `36b52538a` changes
`packing/devtools/check_sqverify_fast.py` (+56 −5),
`packing/devtools/sqverify_fast_census.py` (+198 −47, with `--summary` moved into a
function), `packing/tests/test_sqverify_fast_census.py` (+224 −14) and one line of
`docs/project/document-map.yaml`. No file under `packing/sqverify_fast/` changed
(`git diff --stat 34e87a86b 36b52538a -- packing/sqverify_fast` is empty), so the crate
is still `d97758bb…`. The second subject is `proposed-flip.patch` in the scratch
directory (SHA-256 `57e2325fe85bdbec…`).

**Read in full:**

- `review-2026-10-06-sqverify-fast-declared-net-soundness.md`;
- `git diff 34e87a86b 36b52538a`, which reproduces the scratch
  `fixes-34e87a86b-to-36b52538a.diff` byte for byte (`cmp`);
- `proposed-flip.patch`;
- in `check_sqverify_fast.py` at `36b52538a`: `direction`, `crate_source_sha256`,
  `net_step`, `read_raw`, `mixed_rows`, `mixed_exact`, `mixed_mutant`, `mixed_refused`,
  `mixed`, `summary_of`, `declared_net` and `main`;
- in `sqverify_fast_census.py`: `net_directions`, `mixed_reference`, `run`,
  `direction_row`, `control`, `ReviewedSource`, `REVIEWED_SOURCES`, `reviewed_source`,
  `net_assumption`, `uncovered`, `evidence_entry`, `records_mode`, `source_digest` and
  `main`;
- `tests/test_sqverify_fast_census.py`, whole;
- `sqverify_fast/build.rs`, and in `src/certificate.rs` the functions `rational_of` and
  `declared_net` and the metadata block of `admit`;
- `INDEPENDENCE.md` lines 215–256, and the head of `independence-record.yaml` at
  `34e87a86b`;
- the headings of the 5 October declared-net review, with its sections “What the
  Authors’ Code Shows” (first paragraph only, to check the flip’s description of it) and
  DN-10.

**Not opened:** any `code/` folder or `proof/verify.cpp` under `packing/resources/web`.

**Data read:** `census-row.json` (SHA-256 `0f18fcc746c042c1…`),
`mixed_n18_L470.jsonl.gz` (`68bd3a3321342cb3…`) and `mixed_n18_L470.control.json`
(`0b639f10505fab0d…`) in the scratch directory.

**Commands and results.** The commands ran in the worktree at `36b52538a`, and from run
13 with `proposed-flip.patch` applied.
Python was `packing/.venv/bin/python3` (3.14.7) or `uv run --frozen`. The binary was the
brief’s release build, `packing/sqverify_fast/target/release/sqverify-fast`, SHA-256
`567a0fd58f7ae4e981580f2a90bed5c92ac44fa8f3ebb442b166e93043c15ed4`, which embeds
`d97758bb…`. Everything ran under `nice -n 10`, at two threads or fewer except run 17.

| # | Command | Result |
| --- | --- | --- |
| 1 | `pytest -q tests/test_sqverify_fast_census.py` (at `36b52538a`) | 28 passed, 2.43 s |
| 2 | `ruff check` and `ruff format --check` on the three changed Python files | all checks passed; 3 files already formatted |
| 3 | `basedpyright` on the same three files | 0 errors, 0 warnings, 0 notes |
| 4 | `packing-validate --only "measure verifier Rust"` | passed; the step took 71.6 s (73 s wall); `SQVERIFY-FAST CHECKS PASSED` |
| 5 | `sqverify_fast_census --source-digest` | prints `d97758bbc9639edc…88 reviewed source (910b6b12c; docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md)`, exit 0 |
| 6 | `check_sqverify_fast --binary … --only mixed` (full, at `36b52538a`) | 19 of 19 ok, `SQVERIFY-FAST CHECKS PASSED`, exit 0, 74 s |
| 7 | the same with `check_sqverify_fast.py` from `34e87a86b` (`git show` into the tree under another module name, deleted after) | exit 0, 73 s; `diff` of the two logs differs only in the wall-time line, the worst-gap figures included |
| 8 | `--evidence --only mixed_n67_L848` on the retained census (a `7c49cf79…` row) | exit 0; entry read below (question 2) |
| 9 | `--evidence` on copies of that row with the build digest set to `9985c465…`, to `d97758bb…` and to `11…1` (a scratch `--out` folder each, holding the retained receipts) | exit 0, exit 0, and exit 1 with “built from crate source 11111111…, which no review accepted” |
| 10 | `--evidence --only mixed_n18_L470` on the retained census (the `73959cae…` row) | exit 1, “which no review accepted” |
| 11 | `--evidence` on the scratch `d97758bb…` row with the scratch `CONTROL_FAILED` receipt, and with a stand-in receipt marked `CONTROLS_REFUSED` (before the flip) | both exit 1, “which no review of the declared net accepted” |
| 12 | scratch `own_capture.py` (an exact evaluator written for this re-check: `json`, `fractions` and Sutherland–Hodgman clipping, nothing imported from the crate or the tools) against `mixed_exact` and the crate’s `--probe`, on `mixed_n18_L470` | 12 of 12 poses equal three ways (question 1) |
| 13 | `git apply proposed-flip.patch` | applies cleanly; seven files changed |
| 14 | run 11 again after the flip | stand-in receipt: exit 0, entry read below; the real receipt: exit 1, “not verified and controlled” |
| 15 | `pytest -q tests/test_sqverify_fast_census.py` (flipped) | 28 passed |
| 16 | `render_verifiers --check`; `pytest -q tests/test_verifier_registry.py` (flipped) | “VERIFIERS.md agrees with verifiers.yaml and evidence.yaml”, exit 0; 31 passed |
| 17 | `packing-validate --edit` (flipped) | exit 1, 335 s wall, at the default 4 jobs, which is above the brief’s two-thread limit. Two steps failed: “browser floor” (its pinned tools are not installed: no `npm ci` in this worktree) and “synopsis agrees with the artifacts” (“SYNOPSIS.md document map is stale”, which `36b52538a` causes without the patch; FC-7). Every other step passed |
| 18 | the binary on `mixed_n18_L470` with every mass scaled by 99/100 (`mixed_mutant`), `--directions all --threads 2` | exit 1, `REFUSED`: 230 directions `counterexample-candidate`, 186 verified (408 among them); 134 s |
| 19 | each of the 230 refusals’ witness centres through `mixed_exact`, times 99/100; four of them through `own_capture.py` on the mutant file | all 230 below 1 (least 0.99639 at index 212, greatest 0.9999999999987 at 241); the four agree |
| 20 | scratch `min408.py`: grid and pattern search for the least exact capture of the original at a direction, with `mixed_exact` | 408: least found 1.014382 (50×50 grid); at ten other directions, least found 1.0156 to 1.0175 on a 20×20 grid. A coarse search, not a minimum (question 4) |
| 21 | scratch `mutants.py`: 17 single-edit mutants of the three changed files, each followed by the census test | every mutant of the fix itself (F1 to F6, F17) is caught; of the ten mutants of `net_problems`’ conditions, two are caught and eight survive (FC-4); the tree is restored byte for byte (`cmp`) |

What failed along the way, and what was redone:

- The first comparison in run 12 read each centre as its decimal literal
  (`Fraction(repr(x))`). The crate and the control read the binary64 value
  (`Fraction(x)`), so all ten probe comparisons failed.
  Rerun with the binary64 value: all agree.
- The search in run 20 is weak.
  On the 20×20 grid it found nothing below 1.0156 at directions 150, 207, 250, 350 and
  380, where run 19 shows centres of exact capture below 1.0101. Run 20 is reported only
  as consistent with run 18, never as a bound.
- One wait was written as `sleep 60` and was refused by the harness; it was replaced by
  a background `until` loop over the log file.
- Run 17 used `packing-validate`’s default of 4 jobs, above the brief’s two-thread
  limit, for its 335 s. Single-threaded exact checks (runs 12 and 19) ran beside it for
  part of that time.
- To learn whether run 17’s documentation failure came from the patch, I saved the
  flipped tree’s diff, ran `git checkout -- .`, ran `check_documentation`, and applied
  the saved diff again.
  The mutation pass (run 21) then confirmed with `cmp` that the tree was restored to
  that diff.

Nothing the brief asked for went unestablished because of a tool or permission failure.

## 1. DR-1: The Control’s Evaluator on the Declared Net

**The fix (read).**

- `direction(index, step=STEP)` now takes the step.
- `net_step(raw)` returns `Fraction(str(raw["proof_net"]["step"]))` when `proof_net` is
  an object, and $83/40000$ otherwise.
- `mixed_exact` calls `direction(index, net_step(raw))`.

Every capture the census control computes goes through `mixed_exact(raw, …)` on the
original candidate’s `raw`: the capture at the least-bound leaf’s centre, the
near-threshold factor and both mutants’ witness captures.
The mutants are built by `mixed_mutant`, which copies the whole object, `proof_net`
included, and so are run by the crate on the same net.

**Is it the net admission decides, for every admitted file?** I read `admit` and
`declared_net` in `certificate.rs`.

- A format M file’s step is `proof_net.step` when the key is present.
  Its metadata may set `certificate.D`, but for format M only to the same value, or it
  is refused.
- `rational_of` reads a JSON number by its text and a string as a rational, and
  `read_raw` keeps every float token as its text (`parse_float=str`). So the two readers
  parse the same token.
- Where they could still differ (a duplicate key, which Python resolves to the last
  value and the crate refuses; a token the two parsers read differently), the control
  now refuses. It compares `Fraction(premises["D"])`, the step the crate decided, with
  `net_step(raw)`, and exits with “the control would evaluate another net” on any
  difference or a missing `D`.
- The angle count does not enter the evaluator, and the index comes from the row.
- Format L files carry `net`, which `net_step` ignores.
  The crate pins format L’s net to the standard one, so $83/40000$ is right there.
- A `proof_net` that is not an object makes `net_step` return the standard step, and the
  crate refuses such a file at admission, so no row exists for it.

So for every file admission accepts, the control evaluates at the angle the crate
decided, or it refuses to run.

**Exact recomputation (run 12).** `own_capture.py` reads the candidate with `json` alone
and takes the angle from the file’s `proof_net`. It clips each of the eight images of
every row against the rotated core in `Fraction`s. On `mixed_n18_L470`:

| Pose | `own_capture` | Equal to |
| --- | --- | --- |
| least-bound leaf, index 408, centre `(3.445831961381131, 3.9656702563847714)` | 1.0703183550454765 | the crate’s `exact_capture_crate`, `mixed_exact`, and the receipt’s `exact_capture_independent`, exactly |
| the same centre at the standard step | 1.2947048866177389 | DR-1’s figure |
| the near-threshold mutant’s witness `(3.1714728612403205, 3.1714728612403205)`, times the factor $467150262015973/500000000000000$ | 0.9900116870345023 | the receipt’s `capture_at_witness` and the crate’s witness `exact_coverage`, exactly |
| ten random centres at indices 1, 2, 207, 300 and 415 | 1.034 to 1.445 | the crate’s `--probe` `exact_coverage` and `mixed_exact`, exactly, 10 of 10 |

Both mutants’ `capture_at_centre` equal factor × the recomputed capture, exactly.

**Can a receipt now claim `CONTROLS_REFUSED` or `captures_agree` falsely?**
`captures_agree` is exact rational equality of two independently computed values, at the
angle the crate decided.
`held` still requires both mutants refused at exit 1 with a non-`verified` verdict, and
an exact capture below 1 at the leaf’s centre or at the witness, evaluated on the same
net. I found no path to a false `CONTROLS_REFUSED`.

Two things are outside the receipt.
The control does not compare the row’s `candidate_sha256` with the file it reads, and
`--evidence` trusts a receipt’s `status` without re-deriving `held`. Both are as before;
the census test holds both for cited entries (FC-6).

**Standard nets unchanged (runs 6, 7).** With no `proof_net`, `net_step` returns `STEP`,
so `mixed_exact` is unchanged.
Every retained mixed census row has `premises.D`, so the new refusal reaches none of
them. Run 7 confirms this on the `mixed` group: the same 19 lines, outcomes and worst
gaps as `34e87a86b`’s tool.

**The tests (mutants, run 21).** Reverting DR-1’s fix (F1), or making `net_step` ignore
`proof_net` (F2), fails `test_the_exact_evaluator_reads_a_declared_net`. Removing the
control’s net check (F3) fails `test_a_control_refuses_a_row_decided_on_another_net`.

`check_sqverify_fast`’s `declared-net` group gained one check: the binary’s embedded
`source_sha256` must equal `crate_source_sha256()` of the tree.
That function follows `build.rs`’s rule exactly (read):

- the same file list, `Cargo.toml`, `Cargo.lock`, `build.rs`, then the `src/*.rs`
  entries sorted by name;
- the same framing: name, NUL, bytes, NUL.

Run 5 gives `d97758bb…`, which is the digest the brief’s binary embeds, and run 4 passed
the new check.

## 2. DR-2 and DR-3: The Evidence Text

**What changed (read).**

- `REVIEWED_BUILD` and `REVIEWED_SOURCE` are gone.
  Each accepted digest is now a `ReviewedSource` with its commit, review, build sentence
  and a `declared_nets` flag.
- `evidence_entry` refuses a row whose `source_sha256` is not a key of
  `REVIEWED_SOURCES`, and a row with `net_origin` `proof_net` whose source has
  `declared_nets` false.
- The count is `premises.angle_count`, the oblique count `angle_count − 1`, the step
  `premises.D`. On a declared net the text names `proof_net`, `shrink_bound`,
  `net_last_tangent` and lemma N0, and the pinpoints add the soundness review.
- The fixed 201-direction assumption is now `net_assumption(premises)`.

**Entries generated and read (runs 8, 9, 14).**

- *`7c49cf79…` (`mixed_n67_L848`, retained row and receipt):* “at all 201 directions of
  the standard net”, “the source at e020eb1e2”, the old build sentence, which is true of
  `7c49cf79…`, and the assumption “the standard net of 201 half-angles of step 83/40000
  at core side 9977/10000”. Every sentence is true.

- *`9985c465…` (the same row, digest substituted):* differs only in “the source at
  4ddf37d9c” and “the crate source at 4ddf37d9c, the build the two reviews of 3 October
  accepted”. True.

- *`d97758bb…`, standard net (digest substituted):* differs only in “the source at
  910b6b12c” and the build sentence “the crate source at 910b6b12c, the source of
  4ddf37d9c with the declared net of format M (proof_net, SOUNDNESS.md lemma N0) and its
  review fixes, which the soundness review … read in full and accepted”.
  That is imprecise in two ways (FC-2):
  - `d97758bb…` is the source of `e020eb1e2` (`7c49cf79…`, which added the gate’s test
    profile to `Cargo.toml`) plus the declared net, not 4ddf37d9c’s;
  - the review read the diff from `e020eb1e2`, and `certificate.rs`, in full, not the
    whole crate.

- *`d97758bb…`, declared net (the scratch row, a stand-in `CONTROLS_REFUSED` receipt,
  after the flip):*
  - “at all 416 directions of the net it declares”;
  - “decided … at all 416 net directions”;
  - “of 416 half-angles of step 1/1001, with B(1 + D) = 500499/500500 < 1 and the last
    tangent 415/1001 past tan(pi/8) and at most 1/2 (SOUNDNESS.md, lemma N0)”;
  - “the other 415 by interval branch and bound over 37,882,813 boxes”;
  - the assumption “the net its candidate declares (proof_net), lemma N0 of
    SOUNDNESS.md, of 416 half-angles of step 1/1001 at core side 999/1000”;
  - pinpoints naming both soundness reviews.

  I checked each value against the row: $415/1001 \approx 0.414585 > \tan(\pi/8)
  \approx 0.414214$, and $999/1000 \cdot 1002/1001 = 500499/500500$. The control
  sentences in this entry come from my stand-in receipt, not from a real one.
  They are not evidence of anything, only of the template: `uncovered` printed “at its
  witness” for a run whose witness capture is null, because a real receipt cannot be
  `CONTROLS_REFUSED` with such a run (FC-6).

**Refusals (runs 9, 10, 11, 14).**

- An unreviewed digest is refused, as is the retained `73959cae…` row of
  `mixed_n18_L470`.
- The declared-net `d97758bb…` row is refused before the flip and admitted after it.
- After the flip, it is still refused with its real `CONTROL_FAILED` receipt.

The declared-net refusal message ends “rebuild from reviewed source and re-run the row”,
which cannot help when the source is reviewed and only its declared-net scope is missing
(FC-3, wording).

**Mutants (run 21).** Admitting a declared-net row on any reviewed source (F4) fails the
`standard net only` case of
`test_an_evidence_entry_on_a_declared_net_states_the_net_and_its_review`. Admitting
unreviewed sources (F5) fails
`test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source`. Restoring 201 (F6)
fails the declared-net evidence test.

So DR-2 and DR-3 are fixed.
FC-2 is a precision fix to one sentence, best made in the flip commit.

## 3. The Census Test

**`net_problems` against checklist (b).**

| Checklist item | Where it is held |
| --- | --- |
| 1: format M, `points` empty, `scaling_factor` 1 | `premises.format == "M"`, `raw["points"] == []`, `scaling_factor` (in the calling test) |
| 1: `proof_net` an object with exactly `step` and `last`, `count = last + 1` if present, `last` an integer | `net_problems`: `isinstance`, the key-set inclusion, `type(last) is int` (which excludes `bool`), and the count; `read_raw` turns `416.0` into a string, which fails |
| 1: no top-level `net`; metadata only restates | `"net" in raw`; `metadata.get("D", step)` and `metadata.get("angle_count", count)` against the declaration |
| 1: eight times the densest row’s density at most $2^{32}$ | the calling test |
| 2: `directions_verified = last + 1`, indices exactly `0 … last`, each verified; status, returncode, threshold `1`, `refused_directions` empty, `clears_threshold` | `test_every_mixed_census_case_is_verified_at_every_direction_of_its_net` (by `net_directions`) and the calling test |
| 3: `net_origin`, `D`, `angle_count`, `net_last_tangent`, `B`, `shrink_bound` | `net_problems`, each in exact rationals |
| 3: `mass_exact` $= n - 1/100000$, points and segments 0, no fault injected | the calling test |
| 3: lemma N0’s (a) to (e), recomputed apart from the crate | `net_problems`, each condition exactly as the review states it, (c) as $t^2 + 2t - 1 > 0$, (e) as $B(1 + D/(1 - D^2/4)) < 1$ |
| 5: source `d97758bb…` with `declared_nets`, release, rustc 1.98.0 | `net_problems` and the calling test |
| 6: `CONTROLS_REFUSED`, `captures_agree`, both mutants refused with a capture below 1 | `test_every_entry_the_verifier_decides_has_a_verified_case_and_a_refused_control` and `test_each_control_refuses_both_mutants_where_the_original_verifies` |
| 7: a review read the certificate | `test_every_entry_the_verifier_decides_rests_on_a_review_of_its_certificate` |

Item 4 (`devtools.retained_data check`) and item 2’s match with the report entry’s claim
are not in this test, as before.

**Does it admit anything the checklist excludes?** I found nothing:

- a listed-node or offset net is refused by the key set;
- a non-uniform net cannot be expressed;
- a declared net outside format M is refused by `premises.format`;
- a net outside N0 fails (a) to (e);
- a declared net on a source without `declared_nets` is a problem.

The scratch `d97758bb…` row passes `net_problems` after the flip with no problem.
Under the code at `36b52538a` it gives exactly the one problem, “a declared net, built
from a source no declared-net review read”.

**What the other new tests hold, by mutant (run 21).** Each mutant is one text edit,
followed by the census test; the tree is restored after each.

| Mutant | Edit | Tests that failed |
| --- | --- | --- |
| F1 | `mixed_exact` on `direction(index)` (DR-1 reverted) | `test_the_exact_evaluator_reads_a_declared_net` |
| F2 | `net_step` always the standard step | the same, and `test_a_control_refuses_a_row_decided_on_another_net` |
| F3 | no net check in `control` | `test_a_control_refuses_a_row_decided_on_another_net` |
| F4 | `evidence_entry` admits a declared-net row on any reviewed source | `…_states_the_net_and_its_review[standard net only]` |
| F5 | `evidence_entry` admits any source | the same, and `test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source` |
| F6 | the count back to 201 | `…_states_the_net_and_its_review[declared nets]` |
| F9 | `net_problems` without (e) | `test_the_net_conditions_admit_the_declared_net_only_on_a_source_that_read_it` |
| F15 | `net_problems` ignores the source’s scope | the same |
| F17 | `declared_nets=True` on `9985c465…` too | `test_each_reviewed_source_names_the_review_that_accepted_it` |
| F7, F8, F10 to F14, F16 | `net_problems` without (a), without (d), without the metadata rule, `net_origin`, `angle_count`, `B`, the count rule, or the exact key set | none: these survive (FC-4) |

So each new test holds what its name claims.
The conditions of `net_problems` are right as written, but eight of them are never shown
failing.

**One docstring.** `test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source`
says `73959cae…` is “a source no review accepted”.
The soundness review covered it for files with no top-level `net` key in format T or M,
and said it “may be added”.
The test is right that it is not in `REVIEWED_SOURCES`; the docstring overstates (FC-3).

## 4. The Control on a Declared Net

**What the scratch receipts show.** The row is complete and clean: 416 of 416 verified,
built from `d97758bb…`, candidate digest equal to the retained file’s. Its premises are
`D 1/1001`, `angle_count 416`, `net_origin proof_net`, `shrink_bound 500499/500500`, and
it meets every item of checklist (b) 1 to 3 and 5. The control receipt:

- `captures_agree` true: both evaluators give $1.0703183550454765$ at index 408. DR-1 is
  fixed in practice as well as in the code.
- `original` verified, exit 0.
- `near-threshold` (factor $467150262015973/500000000000000$) refused,
  `counterexample-candidate`, exit 1, with an exact witness capture of
  $0.99001168703450$, recomputed in run 12.
- `scaled-99-100` **verified**, exit 0, least certified bound 1.0000002639721404. So
  `held` is false and the status is `CONTROL_FAILED`.

**Why.** For the 99/100 mutant to verify at index 408, the original’s capture must be at
least $100/99 \approx 1.010101$ at every centre of that direction’s domain.
The crate certifies exactly that, and nothing I computed contradicts it: run 20’s search
found nothing below 1.014382 there.

The mutant is not a certificate, though.
On all 416 directions (run 18) it is refused at 230, and each refusal’s witness has an
exact capture below 1 by `mixed_exact`, four of them confirmed by `own_capture.py` (run
19). The least is 0.99639 at index 212. The 18 directions 398 to 415 are among the 186
it verifies.

The control’s direction is the oblique row with the least `min_certified_lower_bound`.
On a verified direction that is the margin at which the branch and bound stopped above
the threshold: over this row’s 415 oblique directions it ranges from 1.0000000000741
(index 408) to 1.0000053973 (index 15). It ranks directions by noise, not by how tight
the certificate is. On every retained standard-net control receipt the 99/100 mutant was
refused at the chosen index, but nothing in the design guarantees that.

**What it means for the next lane.**

- The flip is not blocked.
  A receipt that cannot be `CONTROLS_REFUSED` stops `--evidence`
  (`not verified and controlled`) and fails the census test.
  The failure is closed.
- `mixed_n18_L470` cannot get a `CONTROLS_REFUSED` receipt from `--control` as written.
  `mixed_n18_L4704` (832 nodes) and `mixed_n19_L48229` (416) will get one only if their
  least-margin direction happens to have less than 1% slack.
  Run `--control` first and read the receipt; do not assume it.
- A lane must not obtain a receipt by choosing the index by hand, by editing the
  receipt, or by changing `CONTROL_SCALE` or the index rule without a review.
  Each of these is a change to control logic, which the soundness review lists among the
  changes that need another review.
- What would work, for a reviewer to read (FC-1): keep the near-threshold run, which is
  scaled relative to the exact capture at the chosen centre and was refused here.
  Then replace the fixed-index 99/100 run with a run of the 99/100 mutant at all
  directions with `--confirm`. Require at least one refused direction, and require every
  refused direction’s witness to be below 1 by `mixed_exact`. The `declared-net` group
  of `check_sqverify_fast` already does this at 0.985. On `mixed_n18_L470` that run took
  134 s at two threads and gives 230 witnessed refusals.

## 5. The Flip

**Should `d97758bb…` be marked as reviewed for declared nets?** Yes.

- The soundness review accepted the crate for format M on a declared net, conditional on
  DR-1 being fixed and read, and on DR-3.
- Both are fixed (questions 1 and 2), and this re-check has read the fix.
- `declared_nets=True` lets a declared-net row stand only together with `net_problems`’
  checks, a `CONTROLS_REFUSED` receipt and a review of the certificate.
- The tightened test (`== {d97758bb…}` in place of `<=`) holds the flag to exactly that
  digest.

**Each statement the patch adds (checked):**

- *`REVIEWED_SOURCES` comment and the census test’s comment:* true once this file is
  committed at the path they name.
- *`verifiers.yaml` and `VERIFIERS.md`:*
  - “format T, M or L on the 201-direction net, or of format M on the uniform net its
    file declares (proof_net, lemma N0)” is true;
  - `f007d7afd and 910b6b12c, source_sha256 d97758bb...` is true (the soundness review’s
    run 4);
  - “tests/test_sqverify_fast_census.py admits a census row as evidence only for a build
    of a reviewed source” is true;
  - `render_verifiers --check` agrees, and the registry tests pass (run 16).
- *`result-import.md`:* true.
  The anchor `#for-the-records-lane` matches the review’s heading “For the Records
  Lane”.
- *`INDEPENDENCE.md` and `independence-record.yaml`:*
  - `910b6b12c` is the last commit to touch `packing/sqverify_fast/`
    (`git log -1 -- packing/sqverify_fast`);
  - the 5 October review’s section is titled “What the Authors’ Code Shows”, and
    `INDEPENDENCE.md` lines 234–237 record that lane B skipped it;
  - the session trailer on `36b52538a` is `session_01NeZ3ofjKFC4rydmZMTkhSq`;
  - the lane’s own reads and its period start I cannot check, and take as declared;
  - “changed no file of this crate” (`INDEPENDENCE.md`) and “changed nothing in the
    crate” (`independence-record.yaml`) are true of `36b52538a`, but the flip commit
    itself edits these two files under `packing/sqverify_fast/`. Say “no source file of
    the crate (none that `source_sha256` covers)” (FC-5).
- *The `V-sqverify-fast` note:* “for a declared net once the control’s exact evaluator
  read that net (its DR-1), which the same day’s re-check confirmed” is true of this
  re-check. It must not be read as saying that a declared-net certificate has a control
  receipt. None has (FC-1).

**Sufficiency.** When this review is committed, it needs an entry in
`docs/project/document-map.yaml`. `check_documentation` reports an unmapped durable
document otherwise, and the patch adds none (FC-5). Run 17 is the edit tier on the
flipped tree without this file.
Its one failure that belongs to the change predates the patch (FC-7). The other is the
browser floor, whose pinned tools are not installed in this worktree.

## 6. Anything New

- **FC-1**, above, is the one finding that bears on what a control receipt can be
  obtained for.
- **FC-7.** `36b52538a` mapped the soundness review but left `SYNOPSIS.md` stale, and
  the edit tier fails on it.
  This affects no claim, but it blocks the merge.
- `--source-digest` exits 0 for any reviewed source, including one without
  `declared_nets`. Its printed line names the commit and review, not the scope.
  The `--evidence` refusal closes this for declared-net rows, so it is a wording matter
  only (FC-3).
- The `--summary` move kept its behaviour: `--binary` and `--out` are still required for
  it, as before.
- `REVIEWED_SOURCES` does not include `73959cae…`, which the soundness review allowed.
  That is conservative and correct: the retained `mixed_n18_L470` row must be rebuilt
  from `d97758bb…` before it can stand, which the scratch row already is.

## Findings

### FC-1 — Non-blocking (closed failure; constrains every declared-net control receipt): the 99/100 control runs at an index chosen by termination margin

`control` runs the 99/100 mutant at one direction only: the oblique row with the least
`min_certified_lower_bound`, a value that on a verified direction is just above the
threshold whatever the certificate’s slack.

On `mixed_n18_L470` that is index 408, where the mutant is verified (scratch receipt;
least certified bound 1.0000002639721404). Runs 18 to 20 show that this is correct
behaviour, not a defect: the mutant is refused at 230 other directions with exact
witnesses below 1, and at 408 nothing below 1.0101 was found.
The receipt is `CONTROL_FAILED`. That is closed: no false `verified` and no false
`CONTROLS_REFUSED` can follow.

The consequence is that `--control`, unchanged, cannot give this certificate a
`CONTROLS_REFUSED` receipt, and may not give one for the next two declared-net
certificates.

Fix: replace the fixed-index 99/100 run with the 99/100 mutant at all directions with
`--confirm`. Require at least one refusal, and an exact witness below 1, re-evaluated by
`mixed_exact`, at every refused direction.
Keep the near-threshold run at the least-bound leaf.
Have a reviewer read the change before a receipt made with it counts.
Until then, do not obtain a receipt by choosing the index by hand.

### FC-2 — Non-blocking, evidence text: the `d97758bb…` build sentence omits the test profile and overstates what was read

`REVIEWED_SOURCES["d97758bb…"].statement` reads “the source of 4ddf37d9c with the
declared net of format M … and its review fixes, which the soundness review … read in
full and accepted”.

- The source is `e020eb1e2`’s (`7c49cf79…`, `Cargo.toml` with the gate’s test profile)
  plus `f007d7afd` and `910b6b12c`.
- The soundness review read the diff from `e020eb1e2` in full, and `certificate.rs`, not
  the whole crate.

Nothing about a verdict changes, since IR-4 of the route review already accepted the
profile.

Fix, in the flip commit, a statement such as:

```text
the crate source at 910b6b12c: the source of e020eb1e2 (7c49cf79...) with the declared
net of format M (proof_net, SOUNDNESS.md lemma N0) and its review fixes, a diff the
soundness review {DECLARED_NET_REVIEW} read in full and accepted
```

### FC-3 — Note, wording: three messages

- The declared-net refusal in `evidence_entry` ends “rebuild from reviewed source and
  re-run the row”. For a source that is reviewed but lacks `declared_nets`, say that the
  source’s review did not read the declared net.
- `--source-digest` could print the source’s `declared_nets` scope beside its review.
- The docstring of `test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source`
  calls `73959cae…` “a source no review accepted”.
  The soundness review covered it conditionally.
  Say “a source not in REVIEWED_SOURCES”.

### FC-4 — Note, tests: some of `net_problems`’ conditions have no negative case

Mutants F7, F8, F10, F11, F12, F13, F14 and F16 (run 21) each remove one condition of
`net_problems`: (a), (d), the metadata rule, `net_origin`, `angle_count`, `B`, the count
rule, and the exact key set.
Each passes the whole census test, because the one declared-net row meets them all, and
no variant in
`test_the_net_conditions_admit_the_declared_net_only_on_a_source_that_read_it` breaks
them alone.
(b) and (c) are shown failing by the `1/999` and `last 414` variants, and (e)
by the `1/999` variant (F9 is caught).

The helper’s conditions are right as written (question 3). Only the tests of the test
are thin. Fix: extend
`test_the_net_conditions_admit_the_declared_net_only_on_a_source_that_read_it` with one
variant per surviving condition.
Examples: `last` 2000 at step 1/1001 for (d), which also leaves the reach of (c)
satisfied; a metadata `D` of `1/1000`; `premises` with `net_origin` `standard`, with
`angle_count` 417, and with `B` `9977/10000`; a `count` of 415; a key `offset`.

### FC-5 — Note, the flip: two wording points and one missing map entry

- In `INDEPENDENCE.md` and `independence-record.yaml`, “changed no file of this crate”
  and “changed nothing in the crate” are true of `36b52538a`, but the commit carrying
  them edits those two files under `packing/sqverify_fast/`. Say “no source file of the
  crate (none that source_sha256 covers)”.
- Add this review to `docs/project/document-map.yaml` when it is committed, as
  `36b52538a` did for the soundness review.

### FC-6 — Note, unchanged since the soundness review: the receipt is trusted, not re-derived

`control` does not compare the row’s `candidate_sha256` with the file it reads, and
`evidence_entry` trusts a receipt’s `status` and prints `uncovered`’s sentence without
re-deriving `held`. A stand-in receipt showed the template printing “exact capture below
1 at its witness” for a run whose witness capture was null.

The census test re-derives all of it for every cited entry: the digest,
`captures_agree`, each mutant’s capture below 1, exit 1. So nothing false reaches the
register through a retained receipt.

No change is needed.
If one is wanted, have `evidence_entry` call the test’s checks, or re-evaluate `held`
from the receipt’s runs.

### FC-7 — Non-blocking for the verdict, blocking for the merge: `36b52538a` leaves `SYNOPSIS.md` stale

`36b52538a` adds the soundness review to `docs/project/document-map.yaml` but not to
`SYNOPSIS.md`’s generated document map.
`check_documentation` then fails with “SYNOPSIS.md document map is stale”.
This was run at `36b52538a` with the patch removed, and again inside the edit tier (run
17). At `34e87a86b` the synopsis is current: `expected_synopsis` over that commit’s
files returns `SYNOPSIS.md` unchanged.

The missing row is

```
| [sqverify-fast on `main` (`d97758bb…`): Soundness Re-Review of the Declared-Net Change](docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md) | dated review record | record | retained | — |
```

at line 579 of `SYNOPSIS.md`. “synopsis agrees with the artifacts” is an edit-tier step,
so a branch at `36b52538a` fails the gate.

Fix: add that row, and the corresponding row for this review once it is mapped (FC-5).
Then re-run `check_documentation`.

## Disposition

- The fixes of `36b52538a` for DR-1, DR-2 and DR-3 are accepted.
  DR-1’s fix has now been read by a reviewer, which the soundness review required.
- `proposed-flip.patch` is accepted: `d97758bb…` may be marked `declared_nets=True`.
  Fold FC-2 and FC-5 into the same commit, and map this review.
- FC-7 must be fixed before the branch merges: add the soundness review’s row, and this
  review’s, to `SYNOPSIS.md`’s document map, and re-run `check_documentation`.
- FC-1 does not block the flip.
  It must be resolved before a declared-net certificate can get a `CONTROLS_REFUSED`
  receipt from a reviewed control driver, unless `--control`, run unchanged, refuses
  both mutants for that certificate.
  Resolving it is a change to control logic and needs a reviewer.
- FC-3, FC-4 and FC-6 need no action for the route.
  FC-4 is worth doing with FC-1.
- No finding is in the crate or in its mathematics.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
