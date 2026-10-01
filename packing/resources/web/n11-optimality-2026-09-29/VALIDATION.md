# Validating T-060

**T-060 claims that eleven freely rotated unit squares fit in a square of side $T$, and
in no smaller square.** Here $T=(6u+4)/(1+2u-u^2)$, where $u$ is the specified root of
the polynomial in the [published proof](source/PROOF.md#1-statement-and-exact-endpoint).
The [exact construction](source/PROOF.md#2-exact-construction-and-upper-bound) gives the
upper bound. The independent geometric execution and its reviewed composition supply the
lower bound; see the [final result](receipts/final-composition.json) and
[packet overview](README.md). The register records T-060 at S5/V3/C3: machine-checked
here, with the review record that rung 4 requires still pending
([epistemics](../../../../epistemics.md)).

This is a reviewer guide **inside the Squares checkout**, not a standalone executable
release. It separates inspection of retained executions from a fresh geometric replay.
The selected [upstream source](source/) and its
[reproduction guide](source/docs/REPRODUCING.md) do not by themselves supply the
complete source and Git LFS object store required for the upstream driver.

## What the Validation Has to Establish

| Obligation | Mathematical source | Accepted evidence or consumer |
| --- | --- | --- |
| Exact root and $T$, a rational cap $U>T$, and an attaining unit-square witness | [Construction and algebra](source/PROOF.md#2-exact-construction-and-upper-bound) | [Exact witness checker](../../../cases/trump11/verify_exact.py) and [fixed-$T$ local check](receipts/local-isolation/result.json) |
| Closed Voronoi center-cell cover, strict cell-diameter bound, and all 2,184 canonical masks with ties retained | [Coordinate framework and case partition](source/PROOF.md#4-closed-center-cover-and-the-2184-cases) | [Case census](receipts/case-census/result.json) and [independent D4 geometry](receipts/d4-independent/result.json) |
| Complete exclusion of 2,180 masks, including whole-angle strict cores, degenerate legal-domain residuals, median-projection field capacity and strict budget, early D4 cuts from the accepted 1,931-case baseline, and both closed center branches | [Exact exclusion rule](source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves) | [Execution inventory](receipts/exclusion-inventory.json) and [center partition](receipts/center-partition-1383-indexed/provenance.json) |
| D4 reduction of the surviving masks to case 438 | [D4 argument](source/PROOF.md#6-the-exact-d4-reduction-to-case438) | [Independent D4 result](receipts/d4-independent/result.json) |
| Fourteen-round root induction, ten capture nodes and nine state joins, closed branch endpoints, three far contradictions, and the near enclosure | [Capture argument](source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge) | [Root chain](receipts/capture-root-chain/result.json), [near leaf](receipts/capture-child-near/result.json), and [final composition](receipts/final-composition.json) |
| Fixed-$T$ local theorem over all contact branches and signed-coordinate residual and curvature obligations | [Contact and local theorem](source/PROOF.md#7-local-contact-analysis-and-the-focused-isolation-rectangle) | [Local isolation](receipts/local-isolation/result.json) |
| Field-to-physical frame, angle and role joins; inclusion of the near leaf in the local rectangle; contradiction from any side $S<T$ | [Capture bridge and deduction](source/PROOF.md#8-complete-case438-capture-and-the-exact-u-to-t-bridge) | [Pose inclusion](receipts/pose-inclusion/result.json) and [final composition](receipts/final-composition.json) |

The [packet overview](README.md#reproducing-the-independent-checks) links the individual
field, non-field, capture, and source-bound replay commands.
The checkers share some first-party exact geometry primitives; “independent” here does
not mean independently implemented arithmetic at every layer.
The
[proof data and trust-boundary discussion](source/PROOF.md#11-proof-data-and-trust-boundary)
is part of reviewing the implication, not a substitute for it.

## Recheck the Retained Execution

From the repository root, use the project Python 3.14 environment and a writable mounted
scratch volume. Replace the example path with your own external scratch directory; check
the mount before creating outputs.

```sh
set -eu
export TASK_SCRATCH=/path/to/mounted/writable/scratch
test -d "$TASK_SCRATCH"
test -w "$TASK_SCRATCH"
export TMPDIR="$TASK_SCRATCH/tmp"
export UV_CACHE_DIR="$TASK_SCRATCH/uv-cache"
export CARGO_TARGET_DIR="$TASK_SCRATCH/cargo"
mkdir -p "$TMPDIR" "$UV_CACHE_DIR" "$CARGO_TARGET_DIR"
cd packing
.venv/bin/python3 -m devtools.inventory_n11_completion --out "$TASK_SCRATCH/completion.json"
.venv/bin/python3 -m devtools.check_n11_final_composition --out "$TASK_SCRATCH/composition.json"
```

The [inventory](../../../devtools/inventory_n11_completion.py) reports any missing case
or capture executions and checks the identities it consumes; its exit code alone is not
a completeness verdict.
The [composer](../../../devtools/check_n11_final_composition.py) checks pinned evidence
identities, recorded final-state joins, and reviewed composition premises.
Accept its retained-evidence result only with status
`PASS_REVIEWED_COMPONENT_COMPOSITION`, an empty `pending_obligations` list, and exit
code zero. Its conclusion depends on the reviewed observed geometric executions.
**These commands do not rerun the geometric exclusions or capture.** Keep their outputs
distinct from the [recorded final receipt](receipts/final-composition.json).

## Fresh Replay and a Standalone Release

A fresh replay needs the pinned upstream commit and object index from the
[packet overview](README.md), every required compressed object verified against its Git
LFS pointer and decoded hash, and the first-party checker revisions bound by the
accepted receipts. The larger acquired cache under `attic/` is local and ignored by Git.
The upstream [publication note](source/docs/PUBLICATION.md) says its privacy-normalized
public derivative has not received a fresh full geometric replay.
The retained [audit-binding refusal](receipts/capture-ancestry/refusal-result.json)
records four stale final-state digests in that derivative; it is a public replay
obstacle, not a counterexample to the packing theorem.

The independent child capture checkers pin byte-exact historical parent receipts,
including timing fields.
A fresh parent may reach the same checked state with different bytes.
A single fresh end-to-end runner therefore still requires reviewed state-equivalence and
parent rebinding (`think-e2ot`); the retained-evidence composer cannot serve as that
runner.

The earlier
[T-026 verifiable claim](../../../cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md)
embeds its certificate, theorem, and standard-library verifier in one document; the
[older $s(11)\geq19/5$ package](../../../cases/n11_fractional_certificate/thirdparty/README.md)
is also copyable. An analogous T-060 release (`think-22uw`) would need a concise
`PROOF.md`, a manifest of the minimal source-bound certificate and input closure,
verifier code with pinned dependencies, one fresh runner, and a separate
retained-receipt mode.
It should omit discovery tools, unrelated history, and duplicate payloads.
A relocated clean environment with no full Squares checkout, prefilled local cache, or
network access must check every declared input and obligation.
Negative controls must refuse an invalid source, omitted case, wrong parent state, or
lost closed endpoint.
Until that runner and closure exist, this checkout guide makes the current evidence
navigable without presenting it as a portable full replay.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
