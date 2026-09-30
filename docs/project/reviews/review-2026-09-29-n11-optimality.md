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

**Pose inclusion, case-438 capture and all 2,180 exclusions remain unaccepted.** The
receipt sets each corresponding conclusion, including global optimality, to false.
T-060 remains S5/V0/C1; this component result does not promote the whole theorem.

## Next Bounded Checks

The [census and capture contract](review-2026-09-29-n11-optimality-census-contract.md)
maps the remaining case census (`think-ncw8`) and candidate ancestry (`think-pgie`),
including exact source keys and refusal rules.
Metadata agreement is not geometric acceptance.

The next slice checks whether every live near-state pose lies in the accepted local
rectangle. Select the one near-trace object (27,653,954 compressed bytes) and its role
guard, then check all 136 closed angular rows and 1,542 vertices through the exact
coordinate conversion.
This remains conditional on the trace’s geometric ancestry.
Run the small case census alongside it.
Record refusals and counterexamples as carefully as passes, with wall and CPU time and
complete-domain scope.

A source-level reviewer found no critical flaw in the examined center-cover, strict-core
inclusion, focused-local, frame-bridge and $U$-to-$T$ implications, conditional on their
exact geometric and dual premises.
That review did not replay the 1,931 baseline exclusions or the full candidate
instances; the baseline spans earlier v4/v5/v6 geometry, not only the inspected v9
checker. Its scope supports C1, not an optimality verdict.
The source review also compared those earlier baseline versions with v9 and examined
field-counting rules, without finding a critical mathematical defect.
Exact instance and ancestry acceptance remains unchecked.
For the 59 field certificates in particular, the conditional counting obligations
include capacity one for strict-core points, capacity $\lfloor m/k\rfloor$ for a
threshold or floor atom, and capacity one for the complete TRUE odd-majority
median-strip region by convex separation.
Each transferred mask must retain its supported owners, and total per-cell lower charge
must exceed the global budget.
These rules were read at source level; none of their certificate instances has been
independently run in this intake.

Only after the selective checks and a data, space and runtime plan should the full
public replay be considered.
Running the publisher’s checker unchanged would test reproducibility; an independent
method or adversarial controls must also establish the mathematical steps it implements.
Until then T-060 stays V0/C1 and the established interval between T-037 and T-011
remains open in this record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
