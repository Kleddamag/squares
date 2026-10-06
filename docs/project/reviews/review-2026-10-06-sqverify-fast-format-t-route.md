# Review of the sqverify-fast format T route: census rows and controls for T-068's 34 rectangle certificates

This review was written on 2026-10-06 by an AI agent (model claude-opus-5-5, tbd-strong tier). It was prompted separately for lane R5 of the 2026-10-06 intake round. It was written after the census rows and control receipts existed and before any register entry rests on them. It covers commit `cb1b4b88d`, which extends `devtools/sqverify_fast_census.py` to format T (`--control`, `--evidence`). It also covers the 34 census rows and control receipts of `packing/benchmarks/measure-verifier/census/2026-10-01/` that `T-068` reports. It registers nothing and moves no bound.

## Verdict

**Accept with conditions.** The crate's theorem covers format T directly: Tokoharu's centre domain is the theorem's own domain, and format M is the extension. All 34 census rows pass every check this review made. All 34 control receipts are sound under the new `tightest_centre` rule, and every capture this review recomputed agrees as an exact rational. A passing census row with a passing control receipt is a complete replay here, *independently re-implemented*, for each of these certificates.

The conditions are:

1. **Retain this document at the path the driver cites.** `FORMAT_T_ROUTE_REVIEW` names `docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md`, which does not exist yet. Map it as a review before any entry cites it (FT-2).
2. **Correct the controls sentence of each generated entry.** It must name the control centre for what it is (FT-1).
3. **Add the limitations FT-3 and FT-4 list.**
4. **Check each certificate against the list in §5.**

No verified lower bound moves from these 34:

- The 30 that the source's checker replayed already hold `T-074`, or sit below a mixed certificate (n = 76).
- At n = 66, 86, 87 and 90, the mixed certificates of `T-069` and `T-071` are higher: 421/50, 471/50, 471/50 and 48/5.

## What Was Read and Run

**Read:**

- The diff `ebf232767..cb1b4b88d` of the driver and its test, line by line.
- `SOUNDNESS.md` in full.
- `INDEPENDENCE.md` lines 55–100 and `independence-record.yaml`.
- `certificate.rs` lines 200–290 and 550–879, `main.rs` `run`, and `lib.rs` `run_direction_inner` and `premises`.
- `git diff 4ddf37d9c cb1b4b88d -- packing/sqverify_fast/src Cargo.toml`.
- `sqpack/rectangle_density.py` lines 250–640 and `git log` on it. It was created 2026-09-29 and last changed 2026-09-30, before the crate's lane began on 2 October.
- The 3 October soundness review in full.
- The 5 October route review: the replays, confirmation, carrying and records-lane sections.
- The 2 October `T-068` review: the argument, hypotheses, R3E-3 and the replay plan.
- The head of the afternoon review of 2 October.
- `epistemics.md`: Verification, Confirmation, Which Code Confirmed It and Review Records.
- `result-import.md` stage 4.
- The register entries `T-046`, `T-068`, `T-071`, `T-074`, `T-077` and `V-sqverify-fast`.

**Ran,** from `packing/` with the project interpreter, everything under `nice -n 19` and single-threaded:

- **Build digests.** `crate_source_sha256()` gives `d97758bb…`. `--source-digest` exits 0 and names the declared-net review. `sha256sum` of the r5 binary gives `567a0fd5…`.
- **A checking script** (`review-scratch/check_rows.py`). For all 34 rows, it compares the census row, the per-certificate receipt, the candidate files, the README's pinned digests and the control receipt.
- **Retained data.** `devtools.retained_data check resources/web/wand125-rectangle-certificates-2026-10-01` exits 0.
- **Census check.** `sqverify_fast_census --check --packets 2026-10-01` prints "37 of 37 retained certificates VERIFIED" and exits 0.
- **Three single directions at one thread** with binary `567a0fd5…`:
  - `rect_n19_L48175` r = 23
  - `rect_n87_L941` r = 76, its least-bound direction
  - `rect_n66_L8385` r = 0, the axis sweep

  Each returned the census receipt's row field for field: verdict, boxes, leaves, depth, least bound, least-bound box, and at the axis the vertices and argmin. Only the timings differed.
- **This review's own exact capture** (`review-scratch/own_capture.py`): a D4 expansion and a polygon clip in `Fraction`. It was written after reading `rectangle_density`'s image function. It covers the control centre and both mutants' witnesses of `rect_n87_L941` and `rect_n19_L48175`. All six equal the receipts' `exact_capture_independent`, `exact_capture_crate`, `capture_at_witness` and the crate's `witness.exact_coverage`.
- **The selection rule, rechecked.** For `rect_n19_L48175` the same code evaluated all 200 oblique least-bound leaf centres. The minimum is index 72 at 1.0009001081, the receipt's index. The next is index 101 at 1.0010049987.
- **Witness agreement.** In all 68 mutant runs of the 34 receipts, the crate's `--confirm` witness capture equals the independent `capture_at_witness`, and `exact_below_threshold` is true.
- **Tests.** `uv run --frozen --all-extras --group dev python -m pytest tests/test_sqverify_fast_census.py -q` gives 66 passed in 7.65 s.
- **Evidence text.** `sqverify_fast_census --evidence --only rect_n87_L941 …`, reviewed in §6.
- **Other packets.** A survey of the census rows of the 27 and 28 September and 2 October packets.

The total cost was a few CPU-minutes.

## 1. The Argument for Format T

**The theorem covers format T as stated.** SOUNDNESS.md's Claim checks every centre in $[a_r, L - a_r]^2$ with $a_r = B(\cos\theta_r + \sin\theta_r)/2$. That is Tokoharu's domain; lemma D's per-bin domain is the format M change.

From a row that is `VERIFIED` at all 201 directions at threshold $T = 10001/10000$, the chain is:

- **Admission.** In exact rationals: $0 < M < n$, $B(1 + D) = 399908091/400000000 < 1$, the endpoint polynomial $89/40000 > 0$, $t_{\max} \le 1/2$, $L^2 \ge 2B^2$ and containment.
- **The threshold.** `main.rs` refuses a threshold below 1, and every accept compares against the upper end of $T$'s enclosure (I2). A capture of at least $T$ at every centre therefore gives the theorem's capture of at least 1.
- **The bound.** N1–N4 then give $s(n) \ge L$.

The crate needs no smoothing margin. N4 integrates the indicator density over closed cores strictly inside the open unit squares. Tokoharu's $B(1 + D) + 3\varepsilon < 1$, which the `T-068` review checked, is not used.

**Lemmas format T uses that format M does not, and whether they were reviewed:**

| Lemma or path | Format T | Reviewed |
| --- | --- | --- |
| N2, the fold | The same fold; Tokoharu's domain does not need it at $\pi/4$ | 3 October table: "Sound for formats T and L" |
| N3, the shrink | Half-angle form only; the tangent-form premise is format M's alone | 3 October §7.3: half-angle form sound for both domains |
| Lemma D | First branch, $U_r = L - B(c_r + s_r)/2$ | 3 October: `domain_upper` exact; C1 sound |
| Mass identity | $\int g = M$ is a tautology of the construction, computed rather than assumed | 3 October §4.1 |
| Threshold $T > 1$ | Declared, or passed with `--threshold`; refused if below 1 | 3 October §4.1 |
| A1/A2, the axis sweep | Used at r = 0, as for format M without atoms | 3 October (S1 fixed) |
| Metadata net (`certificate.D`, `angle_count`) | Format T only: it may *change* the net, and the premises are checked on the net used | Implicitly. The 3 October review discussed this override for format L, and N0's proof says nothing uses the net's values. See FT-7. |

Format T uses no N0, B1–B3, Z1/Z2 or per-bin domain.

**Fields the crate reads from a format T candidate** (`admit` and `sources`):

- `n`, which must match.
- `L` and `B`.
- `rectangles` and `weights`. These alone make the density, and zero weights are skipped.
- `certificate.D` and `certificate.angle_count`. These can change the net.
- `certificate.L` and `certificate.B`, which must agree with `L` and `B`.
- `coverage_lower_bound_exact`. This is only the default threshold, and the census overrides it with `--threshold 10001/10000`.
- `total_mass` if present, which must equal the computed mass.
- `schema` and an object-shaped first row, which would switch the file to format L or M.
- `proof_net` and `net`, which build `d97758bb` refuses in format T.

Never read: `rhs`, `mass`, `scaling_experiment`, `globally_verified`, `status`, and the metadata's `mass_exact`, `epsilon`, `safety_exact`, `rescaled` and digests.

So the only field besides the weights that can steer the decision is the metadata net. In all 37 files of the packet it restates $D = 83/40000$ and 201 directions, and every row's premises record exactly that. `rhs`, `mass` and `scaling_experiment` cannot change a verdict. A false `mass` field would go unnoticed, but it would also be harmless, because $M$ is recomputed from the weights.

## 2. The Census Rows

All 34 pass, and no row fails. For each certificate:

- `status` `VERIFIED`, `returncode` 0, `directions_verified` 201, and `refused_directions` empty.
- `threshold` `10001/10000`, and `least_bound_leaf_exact.clears_threshold` true with its exact capture at least $T$.
- The premises:
  - format T, `centre_domain` `tokoharu`, `angle_count` 201, `D` `83/40000` and `B` `9977/10000`;
  - `mass_exact` equal to $n - 1/100$, with `mass_below_n` `1/100`;
  - no expanded points or segments;
  - `n` and `L` equal to the directory name's.
- The receipt has directions 0–200 once each, each `verified` at `10001/10000`. Its single summary line is `VERIFIED` with `fault_injected_at_box` null and the same build and premises as the row, and its node total equals the row's. The row's least certified bound equals the receipts' minimum.
- **Candidate binding.** `candidate_sha256` equals the stored `.gz` file's SHA-256 and equals `premises.input_sha256`. The file decompresses to the SHA-256 the packet README pins (for example `d3826bec…` → `b0d6b0bc…` for n = 87). `retained_data check` passes.
- **Build.** `source_sha256` `9985c465…` (the source at `4ddf37d9c`), profile `release`, `rustc 1.98.0 (88d9e12ae 2026-08-18)`, x86-64 Linux, binary `b7581bb2…`.

The rows are of 3 October (`e6cb2e581`). The re-layout `feb2edfa1` changed formatting only.

The three re-run directions matched the receipts exactly. They ran on a different build, at one thread instead of two.

## 3. The Controls

**The logic, read line by line, does what the brief describes:**

- `tightest_centre` reads the row's receipts. It takes the `least_bound_box` centre of every direction r ≥ 1 (200 centres), evaluates each with `sqpack.rectangle_density.coverage_at_point` at `direction(r, net_step(raw))`, and takes the least, with ties broken by index.
- At that centre it runs the crate's `--probe`, whose `exact_coverage` must equal the independent value (`captures_agree`).
- The original is run at that index with `--threshold 10001/10000 --confirm`.
- Two mutants are run: the weights × 99/100, and the weights × a factor rounded down so that factor × capture ≤ $T(1 - 10^{-6})$. Each is written by `scaled`, which drops `certificate`, so the mutant runs on the standard net, which is the same net.
- `held` requires the original verified at exit 0, and each mutant at exit 1 with a non-`verified` verdict and an exact capture below $T$, either at the centre (factor × the independent capture) or at the refusal's witness (factor × the independent capture there).
- The net check refuses a row whose decided $D$ is not the file's.

All 34 receipts are `CONTROLS_REFUSED`, with:

- `selection` "tightest least-bound leaf centre", `centres_weighed` 200, index ≥ 1;
- the centre equal to that direction's least-bound box;
- the binary `567a0fd5…`, the build `d97758bb…`, and the threshold recorded.

Every refusal is `counterexample-candidate`. The selected centres capture between 1.000598 (n = 27) and 1.010964 (n = 94).

**Below the threshold is the right test.** The row was decided at $T$, so the control has to show that the verifier at $T$ refuses an admissible input whose claim at $T$ is false. A refusal with an exact witness below $T$ is the verifier's correct answer. "Below 1" would test something else: that the mutant fails as a packing obstruction. The near-threshold mutant cannot meet that test by construction, since its centre sits at about 1.000099.

The difference is visible in the receipts:

- In 25 of the 34, the near-threshold mutant is never shown below 1.
- At n = 93 and 94, the 99/100 mutant is not shown below 1 either. Its witness is about $10^{-10}$ below $T$.

The controls therefore show discrimination at $T$, very finely. Discrimination near 1 still rests on the crate's own tests (IR-3 of 5 October; FT-9).

**What not controlling at the least-bound direction costs.** Very little. At $T$, the search stops each leaf once its bound clears $T$, so every direction's least bound is about 1.0001 and "least-bound direction" picks almost arbitrarily. At `rect_n87_L941`'s least-bound direction (76), the leaf centre captures 1.1428, and the 99/100 mutant verified there. The new rule finds the tightest centre the census saw, for example 1.0103 at index 145.

Two things are not covered, and neither was covered on the format M route:

- The axis sweep at r = 0 is never controlled (FT-10).
- The tightest centre is the least of 200 sampled centres, not the global minimum.

Soundness never rests on the controls. It rests on the lemmas.

**The later build does not matter here.** Between `9985c465` and `d97758bb`, the format T path changed only in two respects:

- format T files with a `proof_net` or `net` key are now refused (none of these files has one);
- `net_origin`, `net_last_tangent` and `shrink_bound` are now recorded.

Every other line that decides a format T file is the same. The three directions re-run on `567a0fd5` reproduced the `9985c465` receipts exactly. So the controls exercised behaviour identical to the deciding build's (FT-8).

**Independence of `sqpack.rectangle_density`.** It is written apart from the crate:

- it is first-party Python sharing no code with the Rust crate;
- it was created 29–30 September, before the crate's lane began;
- it is unchanged since.

It is not blind to the crate, though. INDEPENDENCE.md records that the crate's authors read it "in full: the candidate format …, the D4 images, and the exact oracle". The captures agreeing therefore cannot rule out a common misreading of the format.

That gap is closed from another side. The source's own checker accepted these files, and the `T-068` preflight regenerates the checker's input from each candidate and requires the source's recorded `input_sha256`, which pins the rectangle order and the weights. This review's own clipper, though written after reading the module's image function, also agrees exactly (FT-4).

**Recomputed here:**

| Certificate | What | Value |
| --- | --- | --- |
| `rect_n87_L941`, index 145 | Centre capture | 1.010293609010473 |
| | 99/100 witness | 0.9989248795923895 |
| | Near-threshold witness | 0.998833322588997 |
| `rect_n19_L48175`, index 72 | Centre capture | 1.0009001080995297 |
| | 99/100 witness | 1.000099997274088, below $T$ and not below 1 |
| | Near-threshold witness | 1.0000999998543696 |

All six equal the receipts as rationals. The tests pass: 66 in 7.65 s.

## 4. The Route

**It is a complete replay here.** The census row decides all 201 directions of the standard net from the admitted candidate alone, at a threshold of at least 1. It used a build of exactly the source the 3 October reviews accepted, on a candidate bound to the packet's pin. A refused control is held by the test. That is what the 5 October review accepted for format M. The format T differences are:

- the domain, which is the theorem's base case;
- the threshold, which only makes acceptance harder;
- the metadata net, which here restates the standard net.

Each was reviewed (§1). With the 2 October review of the mathematics, which was separately prompted and lists `T-068` and `T-074` as covered, a records lane may record each certificate as `origin: replayed-here`, `relationship_to_generator: independent-implementation`, `verifiers: [V-sqverify-fast]`, `method: interval-certified`, `replay_status: passed`. This holds once the conditions in the verdict are met.

The 2 October review planned the source-checker replay as the route to `V3/C3`. Stage 4 now admits either route, and one complete replay is what `C3` needs.

**The confirmation, in `epistemics.md`'s words,** is `C3`, "Machine-replayed here or by a third party". It is confirming-origin interval-certified evidence with a certificate, a replay command and a passing replay, and the control receipt is its control path. The mark is *confirmed, independently re-implemented*. It is a second implementation, not a second method: the crate shares the net-and-shrink theorem, the net, the core side, Tokoharu's domain and the threshold with `verify.cpp`.

**What it adds beside the 30 source-checker replays:**

- **The 30.** The rung stays `V3/C3`, and the count of distinct methods stays one. The relation of each part moves from *reproduced with the producer's code* to *independently re-implemented*, since each part takes the confirming run furthest from the producer's code. The census route cannot share an implementation defect with `verify.cpp`; the source-checker replay alone checks the source's own records.
- **The four never replayed (66, 86, 87, 90).** These are their first confirming replays, raising those parts from `V0/C1` to `V3/C3`.
- **`T-068` as a whole.** With all 34 parts replayed on one route or the other, `T-068` itself could derive `V3/C3`. That is the records lane's call.
- **Bounds.** No verified bound moves.

## 5. Carrying the Route

**A records lane checks, for each format T certificate:**

1. **The case.** `census.json` names it, with `n` and `L` equal to its report entry's claim. It has `status` `VERIFIED`, `returncode` 0, `directions_verified` 201, `refused_directions` empty, `threshold` `10001/10000`, and `least_bound_leaf_exact.clears_threshold` true.
2. **The receipts.** Directions 0–200 appear once each, each `verified` at `10001/10000`. There is one summary, `VERIFIED`, with `fault_injected_at_box` null, and its build and premises equal the row's.
3. **The premises.**
   - Format T, `centre_domain` `tokoharu`, `angle_count` 201, `D` `83/40000`, `B` `9977/10000`.
   - `mass_exact` equal to $n - 1/100$, and no expanded point or segment.
   - The file has no `points`, `segments`, `proof_net` or `net`.
   - Its metadata `D` and `angle_count`, if present, restate the standard net. Where a build records `net_origin`, it is `standard`, or `metadata` with the standard values.
   - Densities are far below lemma F3's caps.
4. **The candidate.** `candidate_sha256` equals `premises.input_sha256`, which equals the stored `.gz` file's SHA-256. `devtools.retained_data check` passes on the packet.
5. **The build.**
   - The row's `source_sha256` is in `REVIEWED_SOURCES` (`9985c465…`, `7c49cf79…` or `d97758bb…`), profile `release`, rustc 1.98.0.
   - The control's build is in `REVIEWED_SOURCES` too.
   - If the two differ, the diff touches no format T path (as for `9985c465` → `d97758bb`).
6. **The control.**
   - Status `CONTROLS_REFUSED`, `threshold` `10001/10000`.
   - The rule's fields: `selection` `tightest least-bound leaf centre`, `centres_weighed` 200, index ≥ 1, centre equal to that direction's `least_bound_box`, and `captures_agree`.
   - The runs: the original verified at exit 0, and each mutant at exit 1 with an exact capture below $T$ at the centre or the witness.
   - The near-threshold factor × capture ≤ $T(1 - 10^{-6})$.
   - `tests/test_sqverify_fast_census.py` passes with the new entry in the register.
7. **The review.** The entry's `audit_record` is a retained review that read the certificate's mathematics, with verdict accepted, listed in `reviews` and covering every result that cites the entry.
8. **The values.** A verified bound moves only where the certificate exceeds the standing verified value, checked against the monotone carry to the next count.
9. **The words.** The entry says *independently re-implemented*, and `next_rung` no longer plans a source-checker replay as the condition.

**`T-077`: `rect_n20_L49`, `rect_n42_L68275`, `rect_n70_L86275`.** The route carries **without another review of the route**, once each control receipt lands and the checks above pass.

- **Census rows.** These already exist: `VERIFIED` at all 201 directions, threshold `10001/10000`, source `9985c465`, format T, Tokoharu's domain, standard net and core, mass $n - 1/100$.
- **Packet.** They are the same format, generator, checker and scaling as `T-068`'s.
- **Their review.** The mathematics review is `review-2026-10-02-wand125-afternoon-certificates.md`. It was written by the retaining lane rather than a separately prompted one, as `T-077`'s reviews entry already says, but it is a lane separate from the replay's, which is what stage 4 asks. Each entry's limitations must say so, and the review does not count toward a later rung 4.
- **The evidence entry.** `--evidence` takes its source key from the packet's single reported entry (`E-wand125-rectangle-2026-10-02-report`).
- **Bounds.** These three can move verified bounds, since they raise `T-074` by 0.0025 to 0.0125. Check 8 applies.

**`T-046`, the 27 and 28 September packets.** The route **does not carry as things stand.** Three things are needed.

- **Rows from unreviewed builds.** 23 of the 82 rows in these packets were built from source `bc2a6201`, and `rect_n18_L4695` records no build at all. None of these is reviewed source, and they record no threshold. They must be re-run on reviewed source before anything counts. Before then, `--control` must not run on them (FT-5).
- **No mathematics review on `T-046`.** `T-046` lists no `reviews` and stands at `C0`; the 27 September scaling review is recorded only on a replay entry. A retained, accepted review that read each certificate's mathematics must be mapped on `T-046`, or on the result that cites the entry. For the 28 September packet, that means a review that read those certificates, not only the 27 September review.
- **Another mass.** `rect_n21_L4985`, `rect_n27_L56` and `rect_n21_L49875` have mass $n - 1/1000$. The theorem uses only $M < n$, which admission recomputes, so this needs no new mathematics. But the test's `format_t_problems` refuses it. Widening that condition is a change to the route's conditions, and the review that maps those certificates' mathematics should read it.

The rows that are already `9985c465` and $n - 1/100$ carry once a mapped review of their mathematics exists and their controls land.

Separately, the 5 October triggers for another review still hold: a crate change, another core side, net, domain or threshold, points or segments, densities near F3's caps, a change to the driver's verdict, admission or control logic, or a defect in the shared mathematics.

## 6. The Evidence Text

The entry printed for `rect_n87_L941` matches the receipts on all of the following:

- the identifiers, scope, source key `[wand125 rectangle bounds 2026-10-01]` and certificate path;
- both digests (IR-1 closed);
- n, L, mass, core, net, the 691 orbits and 5,512 images;
- the axis vertices 7,198,489 and least capture 1.0045278173031715;
- the 28,941,188 boxes and least bound 1.0001000008254144 at index 76;
- the least-bound leaf's capture 1.1428350178 at index 76;
- the CPU and wall time, the build and its review;
- the controls' index 145, verdicts and threshold;
- the statement that the crate shares the mathematics but no code.

It says more than the receipts show in these places:

- **"The least-bound leaf's centre", used twice in the controls sentence.** The near-threshold mutant was scaled at the tightest centre, at index 145 with capture 1.0103. The sentence before it names a *different* least-bound leaf (index 76, capture 1.1428), and `uncovered_below` repeats the misnomer. A reader would take index 76's centre to be the control point (FT-1).
- **"Each capture was evaluated again by sqpack.rectangle_density, an exact evaluator written apart from the crate"** is true, but it omits that the crate's authors read that module in full (FT-4).
- **"In the census of 3 October 2026" and "a shared 4-core x86-64 Linux container under load"** are hard-coded. They are true for these 34 and for the 2 October packet's rows, and would be false for any re-run (FT-6).

It leaves out:

- how the control point was chosen and what it captures;
- whether the source's checker ran on this certificate;
- the spot checks.

**Each format T entry's `limitations` must state:**

- That sqverify-fast decided the retained candidate at all 201 directions, each `verified`, with summary `VERIFIED` and exit 0, at Tokoharu's threshold 10001/10000, with Tokoharu's centre domain and the standard net. The file's metadata restates that net and nothing else in the file was read for the decision. Include the axis vertices and least capture, the oblique boxes and least bound with its index, CPU and wall time, threads and host.
- The candidate binding: the stored gzip file's SHA-256 and the decompressed SHA-256 the README pins, tied by `retained_data check`.
- The build: `9985c465…`, the source at `4ddf37d9c` that both 3 October reviews accepted, rustc 1.98.0, release, x86-64 Linux.
- That it is a second implementation, not a second method: the crate shares the theorem, net, core side, Tokoharu's domain and the threshold with `verify.cpp`, and uses no smoothing margin.
- The controls:
  - run on build `d97758bb…` (binary `567a0fd5…`), whose format T path is identical to the row's build;
  - at the least-capture least-bound leaf centre of the 200 oblique directions (index *r*, exact capture *c*);
  - the original verified again there;
  - every weight × 99/100, and every weight scaled to put that centre's capture $10^{-6}$ of $T$ below $T$, each refused with an exact capture below $T$ at the centre or the witness;
  - recomputed by `sqpack.rectangle_density`, written before the crate, sharing no code with it, and read by its authors;
  - held by `tests/test_sqverify_fast_census.py`.
- Whether the source's checker ran here:
  - for the 30, "also replayed with the source's own checker (`E-wand125-rectangle-2026-10-01-source-replay`)";
  - for n = 66, 86, 87 and 90, "the source's own checker was not run here on this certificate; its records are not reproduced";
  - in both cases, the node counts and bounds are the crate's own.
- That this review re-ran three directions on a binary of the later build, which reproduced the census receipts exactly, and recomputed two receipts' captures with its own exact code.
- `relationship_to_generator: independent-implementation`, with `V-sqverify-fast`'s independence record and the audit record.

## Findings

No finding blocks recording the mathematics or the receipts. The two marked blocking block the entry text as `--evidence` generates it, until fixed.

- **FT-1. Blocking for the generated entry text.** The controls sentence calls the control point "the least-bound leaf's centre" right after naming the census row's least-bound leaf, which is a different point (index 76 against index 145 at n = 87). `uncovered_below` repeats the phrase. Name it "the control centre, the least-capture least-bound leaf centre at index *r*, exact capture *c*", and say how it was chosen.
- **FT-2. Blocking until done.** `FORMAT_T_ROUTE_REVIEW` cites `docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md`, which does not exist. Retain this review there, map it in `document-map.yaml`, or change the constant.
- **FT-3. Non-blocking.** The limitations omit whether the source's checker ran on the certificate: it ran for 30, and did not for n = 66, 86, 87 and 90.
- **FT-4. Non-blocking.** `sqpack.rectangle_density` is described as "written apart from the crate", and the test says it "shares no code with the crate". Both are true, but the crate's authors read it in full (INDEPENDENCE.md). Say so. The format reading is pinned independently by the preflight's regenerated `input_sha256`. Separately, `V-sqverify-fast`'s `source` should list `packing/src/sqpack/rectangle_density.py`, which the controls now run, as IR-4 asked for `check_sqverify_fast.py`.
- **FT-5. Non-blocking.** `control()` sets `threshold = entry.get("threshold") or 1` and passes it to the crate for format T. A format T row with no recorded threshold, such as the 27 and 28 September `bc2a6201` rows, would be controlled at 1 although it was decided at the declared 10001/10000. It should refuse such a row instead. The test would fail on it, so nothing wrong could be recorded, but it fails late.
- **FT-6. Non-blocking.** `rectangle_evidence_entry` hard-codes the census date and the host description. Derive them from the row or require them as arguments.
- **FT-7. Non-blocking, note.** Format T's metadata can change the net. This is sound, since admission checks every premise on the net used, but the 3 October review addressed the override only for format L. Each certificate's check must confirm the standard values (check 3).
- **FT-8. Note.** The controls ran on `d97758bb`, while the rows were decided on `9985c465`. The diff and the identical re-runs show the format T behaviour is the same. Future controls should run on the row's build, or the stage-4 text should say a later reviewed build is acceptable when the format's path is unchanged.
- **FT-9. Note.** At the selected centre, the 99/100 mutant keeps more than 1% slack at n = 87, 93 and 94 (centre captures 1.0103 to 1.0110), so its refusal came from a witness elsewhere. At n = 93 and 94 that witness is about $10^{-10}$ below $T$ and not below 1. The controls show discrimination at $T$; discrimination near 1 rests on the crate's tests (IR-3). FC-1's closed failure still applies to a future certificate.
- **FT-10. Note.** The controls never exercise the axis sweep at r = 0; the test requires index ≥ 1. This is the same as the format M route.
- **FT-11. Note.** The test checks that the control centre is a least-bound box, but not that it is the least of the 200. This review checked that for `rect_n19_L48175`.

## For the Records Lane

1. Retain this review at `docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md` and map it (FT-2).
2. Generate each of the 34 entries with:

   ```bash
   .venv/bin/python3 -m devtools.sqverify_fast_census --evidence --only <name> \
     --audit-record docs/project/reviews/review-2026-10-02-wand125-rectangle-bounds-t068.md \
     --date <the replay day> \
     --binary sqverify_fast/target/release/sqverify-fast \
     --out benchmarks/measure-verifier/census
   ```

   Then rewrite the controls sentence (FT-1) and add the limitations in §6, including FT-3 and FT-4. Better still, fix the generator first and regenerate.
3. Check each certificate against §5's checks 1–9. Every row this review checked passes checks 1–6.
4. No verified lower bound moves. For the 30, the relation of each part becomes *independently re-implemented*, and `T-074` stays `V3/C3`. For n = 66, 86, 87 and 90 these are the first replays. Whether `T-068` itself derives `V3/C3` is the register's call, and its `next_rung`, `composition` and `notes` change with that call.
5. Add `packing/src/sqpack/rectangle_density.py` to `V-sqverify-fast`'s `source` (FT-4).
6. For `T-077`, run `--control` on the three rows. The route then carries with the afternoon review as `audit_record`, and the limitations must say that review was the retaining lane's own. For `T-046`, see §5: re-run the unreviewed rows, fix FT-5 first, and map a review of the mathematics.
7. FT-5, FT-6 and FT-11 are for the driver's next change. Per stage 4, a change to the control logic needs a review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
