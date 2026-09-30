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
records their identities, but this intake has not acquired their payloads.
No fetched proof code or certificate has been executed here.
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

## Next Bounded Checks

The next slice under `think-pqg7` should bind the exact source and selected input
hashes, then check a small, decisive obligation independently before acquiring the whole
data store. The three small $D_4$ source payloads identified in the plan are a starting
set: reconstruct closed-cell coverage and symmetry mapping, enumerate the 2,184
canonical masks, and test boundary cases and omitted or duplicated masks against a
first-party checker.
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
threshold atom, and capacity one for a true odd-majority median strip by convex
separation. Each transferred mask must retain its supported owners, and total per-cell
lower charge must exceed the global budget.
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
