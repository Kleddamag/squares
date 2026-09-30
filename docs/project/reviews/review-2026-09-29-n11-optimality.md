# Eleven-Square Global Optimality: Source Intake and Verification Handoff

The external
[11SquaresOptimal source](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c)
claims that eleven congruent unit squares, with independent rotations and legal boundary
contact, require a square container of side at least Trump’s algebraic construction side
$T=3.8770835900228141773078970601\ldots$. This is **T-060, S5/V0/C1** in the
[result register](../../../packing/frontier/results.yaml): potentially decisive for the
smallest open case, but still a reported external theorem.
C1 records a scoped source review, not independent acceptance of the finite certificates
or the global conclusion.
The proof-audit parent is `think-3i74`; `think-pqg7` owns the measured, independent
verifier lane.

The current verified lower bound is the distinct **T-037** result $s(11)>31/8=3.875$.
The exact Trump construction is the established upper witness, **T-011**. **T-059**
concerns wand125’s reported equality of 12,028 row minima for a separate certificate; it
neither asserts nor establishes global optimality.
No result that landed from the current upstream main branch closes this gap.

## Pinned Source and Acquisition Limit

The captured Git commit is `f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c`, tree
`3fed944c5a0c1dda5e61cb9f45f0dd3d4dc6360c`. The
[source packet](../../../packing/resources/web/n11-optimality-2026-09-29/README.md)
retains the claim,
[proof exposition](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
reproduction and publication notes, verifier entry point, attribution, and the
compressed full content index.
Its
[provenance record](../../../packing/resources/web/n11-optimality-2026-09-29/provenance.json)
binds each copied file by SHA-256 and decoded length.
The checkout at `attic/11SquaresOptimal` is an ignored working copy, not the durable
evidence packet.

The public data store has 2,646 index objects behind 2,524 decoded paths.
All 2,638 unique Git LFS blob paths are reachable from the index, with 2,344,331,966
declared compressed bytes; the publisher estimates about 11.3 GB after decoding.
The
[pointer inventory](../../../packing/resources/web/n11-optimality-2026-09-29/lfs-pointer-inventory.json.gz)
records their identities.
Initial intake acquired no payloads; the independent symmetry check below subsequently
acquired three, totaling 102,046 compressed bytes.
The publisher’s proof checker has not been executed here.
The publisher’s
[publication note](../../../packing/resources/web/n11-optimality-2026-09-29/source/docs/PUBLICATION.md)
says the privacy-normalized public derivative has **not** had a fresh full geometric
replay. It describes a narrower integrity and final-composition diagnostic, while the
private source project is said to have completed a 23-stage calculation.
The published `RUN_ALL.py` docstring still describes an incomplete combined run and a
checked recovery after a stage-5 argument error.
Whether that text predates the reported private completion is an unresolved provenance
question, not a mathematical refutation.

The
[third-party notices](../../../packing/resources/web/n11-optimality-2026-09-29/source/THIRD_PARTY_NOTICES.md)
credit Walter Trump for the construction and David Ellsworth for the reconstruction
diagram in pinned `jlevy/squares` material.
They assert no blanket license over the collected sources.

## Claimed Reduction and Verification Route

The
[proof exposition, Sections 3–10](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md)
sets a rational cap $U>T$, maps centers into sixteen closed cells, and reduces the 4,368
eleven-cell masks by half-turn symmetry to 2,184 canonical cases.
It claims exact certificates exclude 1,931 baseline, 76 extension and 173 returned
cases, leaving four cases.
An exact $D_4$ bridge reduces those four to case 438; a complete branch cover and local
isolation argument would then exclude every side below $T$. The counts alone do not
prove completeness: the actual case sets, closed boundaries, geometric inclusion
directions, source bindings and branch partition must be checked.

The published
[`RUN_ALL.py`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/blob/f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c/src/evidence/RUN_ALL.py)
defines this ordered, stop-on-first-failure route:

| Stages | Names | Dataflow role |
| --- | --- | --- |
| 1 | `original-package-check` | Check the existing manifest and recorded result bindings. |
| 2–5 | `baseline-full-geometry`, `prior-76-full-geometry`, `returned-173-full-geometry`, `prior-strict-integration` | Replay the three exclusion families, then bind the baseline and extensions into the 2,007-case prior union. |
| 6 | `symmetry` | Check the exact $D_4$ bridge for the four residual masks. |
| 7–13 | `candidate-construction`, `candidate-cover`, `candidate-local-algebra`, `candidate-local-baseline`, `candidate-local-weighted`, `candidate-focused`, `candidate-feature-bridge` | Check the exact upper witness, cell cover and local algebra and isolation premises. |
| 14–18 | `candidate-root-geometry`, `candidate-far15-geometry`, `candidate-far13-geometry`, `candidate-far2-geometry`, `candidate-near-geometry` | Replay the case-438 root and four branches; each branch wrapper requires the root output. |
| 19–21 | `candidate-composition`, `candidate-consumer-tests`, `candidate-summary` | Bind the branch conclusion, exercise rejection controls, and bind nine named candidate result files. |
| 22–23 | `fresh-manifest`, `final-global-composition` | Seal current input and result bytes; decide the complete union, symmetry and candidate conclusion together. |

This is the runner’s operational order, not a claim that every earlier stage is a
logical premise of every later stage.
[`VERIFY.py`](../../../packing/resources/web/n11-optimality-2026-09-29/source/VERIFY.py)
materializes **every** indexed decoded path before it starts stage 1, so the unmodified
published entry point needs all 2,638 LFS payloads.
The exact minimum payload subset for a separate selected-stage replay is not known from
this source-only inventory: the decoded `PROOF_MANIFEST.json` and some dynamic read
traces are among the missing payloads.
The publisher says a full replay can take hours, but no wall time or CPU cost of this
public derivative has been measured here.
A successful composition checker alone would be a source-dependent consistency check,
not independent geometric confirmation.

## Independently Checked Symmetry Lemma

The first-party [exact checker](../../../packing/devtools/check_n11_optimality_d4.py)
returned `PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE`. Its
[retained receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/result.json)
and adjacent provenance and replay script bind the checker and all three input objects.
It imports no upstream verifier: rational arithmetic reconstructs the closed cover,
enumerates 4,368 masks and 2,184 half-turn representatives, and constructs the four-view
overlay with 212 polygons and eight singleton cells.
It checks 1,572 strict distance bans and independently exhausts the three residual
constraint problems, using 75, 61 and 31 search nodes respectively.

This proves the symmetry reduction **conditional on the four surviving masks and the
case-438 conclusion**. It does not check the 2,180 preceding exclusions or the case-438
capture. The receipt explicitly records `global_optimality_proved: false`. Seven focused
tests cover boundary and rejection behavior; Astra-max mathematical review found no
blocker in this checker.
The retained execution took 0.927 seconds wall and 0.923 seconds CPU inside the checker,
1.00 seconds wall including interpreter startup.
The selected ceiling was 45 seconds inside a 55-second process timeout.
No native-code optimization is justified by this measurement.

## Recomputed Local Dual Residuals

The first-party
[residual consumer](../../../packing/devtools/check_n11_optimality_local_dual.py)
recomputed all 128 branches times 66 signed coordinates: **8,448 exact residual
checks**. Its
[receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/result.json)
deliberately reports `INCOMPLETE_LOCAL_DUAL_PROFILE`. It checks root isolation,
matrix-entry enclosures, nonnegative dual weights, complete signed-coordinate inventory
and the residual error bound.
Four focused tests exercise arithmetic and refusals; Astra-max source review found no
mathematical blocker in these residual checks.

The retained run took 14.713 seconds wall and 14.632 seconds CPU inside the checker,
15.41 seconds including startup, under a 25-second internal and 30-second process
ceiling. Two source-bound proposal objects total 1,560,204 compressed bytes.
The consumer uses our exact construction and branch primitives, which are byte-identical
to the publisher’s copies: this is fresh residual arithmetic with shared geometry
source, not an independently derived geometric model.

That residual checkpoint alone establishes no local-isolation theorem.
The subsequent complete local check below discharges its curvature and feature
obligations.

## Accepted Fixed-T Local Isolation Component

The [local checker](../../../packing/devtools/check_n11_optimality_local_isolation.py)
returned `PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION`. The
[full receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/local-isolation/result.json)
and adjacent provenance bind the reviewed implementation, its frozen residual-checker
dependency, and the two retained proposal objects.
It checks all 112 features, 88 strict unavailable-feature margins, the 512-to-128
nonlinear branch mapping, and all 8,448 strict weighted dual inequalities.
For any proposed nonzero feasible displacement in the anisotropic rectangle, those
inequalities force its normalized radius to exceed one, a contradiction.
This isolates the labelled Trump pose at fixed container side T within that rectangle.

The run took **17.298 seconds wall / 17.144 seconds CPU**, **17.98 seconds including
startup**, under a 45-second internal and 55-second process ceiling.
Four focused tests include strict-boundary refusal and a retained one-branch run that
correctly stays incomplete.
Astra-max review checked the mathematical implications, source identities, full receipt
and partial control and found no blocker.
The shared construction primitives remain an explicit trust dependency.

The local receipt does not claim pose inclusion or capture.
The subsequent inclusion check below closes only the first of those obligations.
T-060 remains S5/V0/C1; these component results do not promote the whole theorem.

## Checked Near-State Pose Inclusion

The [pose checker](../../../packing/devtools/check_n11_optimality_pose_inclusion.py) and
[retained receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/pose-inclusion/result.json)
check all **136 live closed angular rows and 1,542 vertices across eleven owners**
against the accepted local rectangle, including both angle-chart endpoints.
The inverse quarter-turn, exact coordinate conversion and whole-interval angle bounds
are checked; the narrowest certified coordinate slack is positive, about
$2.28\times10^{-12}$. The receipt binds the original near trace and guard, the retained
compact extraction, the extractor, and the accepted local-isolation result.

The bounded run took **3.300 seconds wall**, **3.38 seconds including startup**.
Python’s own process CPU was 0.418 seconds; the outer measurement includes the jq child
and records 2.73 seconds user plus 0.54 seconds system CPU. Six focused tests pass;
Astra-max review approved the exact inclusion argument and inspected its receipt.
This proves inclusion **conditional on the supplied domains being valid**. Their
geometric ancestry and complete case-438 capture remain unaccepted.

## Checked Case Census

The [census checker](../../../packing/devtools/check_n11_optimality_case_census.py)
returned `PASS_CASE_CENSUS_ONLY`; its
[receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/case-census/result.json)
reconstructs all 2,184 canonical IDs and verifies the exact 1,931 baseline, 76 extension
and 173 returned-case lists across twelve jobs.
Their complement is exactly 438, 999, 1462 and 1659. Eleven focused controls and
Astra-max source review passed.
Runtime was 0.044 seconds wall / 0.043 seconds CPU, 0.11 seconds including startup.

This is a complete metadata census, **not acceptance of the exclusions**. It explicitly
records `geometry_verified: false`; the subsequent field check below separately
establishes 459 exclusions.
Global optimality remains open.

## Accepted First Field Certificate

The
[mask-0 field checker](../../../packing/devtools/check_n11_optimality_field_mask0.py)
and
[receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/field-mask0/result.json)
independently establish 55 ownership obligations (34 strict disk and 21 rational wall)
and all 136 closed angular rows of the two positive-charge cells.
Exact arrangement coverage includes endpoints; the complete charge argument and
supported owners give 453 direct and **459 canonical exclusions** after half-turn
transfer, matching the pinned proposal set.
This accepts one of 59 field certificates, not the complete union.

Seven focused controls pass.
Astra-max mathematical review accepted the stated scope.
The run took **16.515 seconds wall / 16.458 seconds CPU**, 16.58 seconds including
startup, under a 30-second ceiling.
The subsequent mask-202 check below expands this coverage.
Case coverage is not a percentage of the whole proof: capture and composition remain
separate obligations.

## Accepted Second Field Certificate

The [mask-202 checker](../../../packing/devtools/check_n11_optimality_field_mask202.py)
checks all 50 ownership points (23 disk and 27 wall) and all 439 closed angular rows.
It imports the hash-bound frozen rational primitives of the first checker, with the
correct three-site median, and independently reconstructs the selected charge regions.
Using a smaller subset of regions reduces arrangement work: acceptance still requires
that subset to cover the entire closed domain.
A subset miss returns incomplete and accepts no exclusions.

The full run accepted 764 canonical exclusions, 653 outside the accepted mask-0 set:
**1,112 distinct exclusions are independently accepted; 1,068 remain unchecked.** This
is two of 59 field certificates, not the whole proof.
Checker wall time was 17.532 seconds, CPU 17.235 seconds, and outer wall 17.61 seconds,
under the selected 30-second ceiling.
Five focused controls pass, and Astra-max review accepted the implementation and
complete result. Its full result is retained compressed beside the compact summary,
provenance and replay in
[the receipt directory](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/field-mask202/).

## Confirmed Public Replay Binding Defect

The
[retained refusal](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/refusal-result.json)
records a mismatch between the pinned near trace and its published B7 audit:

| Quantity | SHA-256 |
| --- | --- |
| Actual near `final_state`, canonical JSON | `a6d45c0c383496fbffd0934e37d735badecc6d05f1e8346da8c063ee5f44fd80` |
| B7 recorded `final_state_sha256` | `810027063afb57bda360cc16eced4bf0e62c6cb29f112237f945cabab8613f9f` |

Two independent calculations agree on the actual digest.
This is a confirmed binding and reproducibility defect, tracked by **think-gzju**, not a
geometric counterexample.
The pinned publisher’s `audit_capture_portable.py` rereads the raw input at line 401 and
hashes its final state at line 408. Its `replay_candidate.py` lines 272–282 compare the
fresh result with historical B7, including this mandatory digest: that comparison would
reject with `Portable geometry differs at final_state_sha256` if reached.
`audit_complete_capture438.py` line 158 also requires the equality.
The later sealing stage cannot repair an earlier failed comparison.
We have demonstrated the incompatible inputs and comparison; we have not run the full
23-stage publisher pipeline.

The
[source-graph receipt](../../../packing/resources/web/n11-optimality-2026-09-29/receipts/source-graph/result.json)
subsequently checks all ten hash-verified source nodes and nine actual parent edges,
including ordered branch assumptions and contradiction markers.
This establishes structural ancestry, not validity of the geometric reductions or the
external root induction.
It took 4.95 seconds including startup.

The same digest mismatch occurs in **all four** published leaf audits, with an
independent serializer cross-check for each.
The far15 mandatory comparison would therefore fail before the near comparison, if
preceding stages completed.
Exact hashes for all leaves are retained in the source-graph receipt.
A contradiction marker in a source trace is not independent acceptance of that
contradiction.

A consistent repair requires fresh accepted leaf replays and coherently regenerated
dependent receipts and bindings.
Changing the stored digest alone does not establish geometric ancestry.
Our accepted local isolation and conditional pose inclusion remain valid: the latter
binds the actual near source directly.
Full capture and global optimality are unconfirmed.
**T-060 remains S5/V0/C1.**

## Next Bounded Checks

The [census and capture contract](review-2026-09-29-n11-optimality-census-contract.md)
maps the remaining exclusions (`think-ncw8`) and candidate ancestry (`think-pgie`). The
implementation and mathematical-review lanes select additional certificates by marginal
coverage and measured kernel cost.
The capture lane proceeds from structural ancestry to the root induction and actual
geometric premises; the binding defect remains open.
The coordinator batches integration and concrete CI repairs alongside these lanes,
without gating proof work on unrelated tests.

A source-level reviewer found no critical flaw in the examined center-cover, strict-core
inclusion, focused-local, frame-bridge and $U$-to-$T$ implications, conditional on their
exact geometric and dual premises.
That review did not replay the 1,931 baseline exclusions or the full candidate
instances; the baseline spans earlier v4/v5/v6 geometry, not only the inspected v9
checker. Its scope supports C1, not an optimality verdict.
The source review also compared those earlier baseline versions with v9 and examined
field-counting rules, without finding a critical mathematical defect.
Most exact instances and complete ancestry remain unchecked.
For the 59 field certificates in particular, the conditional counting obligations
include capacity one for strict-core points, capacity $\lfloor m/k\rfloor$ for a
threshold or floor atom, and capacity one for the complete TRUE odd-majority
median-strip region by convex separation.
Each transferred mask must retain its supported owners, and total per-cell lower charge
must exceed the global budget.
The mask-0 instance above independently checks its applicable rules; other field
instances still require acceptance.

Only after the selective checks and a data, space and runtime plan should the full
public replay be considered.
Running the publisher’s checker unchanged would test reproducibility; an independent
method or adversarial controls must also establish the mathematical steps it implements.
Until then T-060 stays V0/C1 and the established interval between T-037 and T-011
remains open in this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
