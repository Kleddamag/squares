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
| Complete exclusion of 2,180 masks, including whole-angle strict cores, degenerate legal-domain residuals, median-projection field capacity and strict budget, early D4 cuts from the accepted 1,931-case baseline, and both closed center branches | [Exact exclusion rule](source/PROOF.md#5-what-an-exact-case-exclusion-certificate-proves), and for the field charge the paper’s charge lemma, since the original states none; its [section 12](source/PROOF.md#12-how-the-23-verification-stages-support-the-theorem) names the certificates and the transfer rule | [Execution inventory](receipts/exclusion-inventory.json) and [center partition](receipts/center-partition-1383-indexed/provenance.json) |
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

Run the inventory and the composer as
[Portable Replay Commands](#portable-replay-commands) gives them under retained
composition.
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

## Portable Replay Commands

These commands rerun each retained check from a clone of this repository.
They need the project’s Python 3.14 environment
(`uv sync --frozen --all-extras --group dev` in `packing/`; see the
[fresh-clone steps](../../../../AGENTS.md#a-fresh-clone)), `gzip`, `jq`, `sha256sum`
(`shasum -a 256` on macOS) and an ordinary `timeout` (GNU coreutils; Homebrew’s
coreutils names it `gtimeout` on macOS).
The first block starts at the repository root and enters `packing/`; every later path is
relative to `packing/`, and every output goes to a new directory outside the source
tree.
Each command below ran in this checkout on Linux on 2026-10-03.
Each result matched its retained receipt in every field except timing and the
field-runner additions noted below; the table at the end records what each reported.

The `replay.sh` beside a receipt and the command in its `provenance.json` are
provenance.
They record the original runs on the author’s Mac: several source a mounted scratch
volume’s environment or call Homebrew’s `timeout` or `gtimeout`, and some refuse to run
without that machine’s scratch variables.
They stay unchanged and are not the portable entry points.

```sh
cd packing
R=resources/web/n11-optimality-2026-09-29/receipts
COVER=$R/d4-independent/objects/df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e.gz
OUT=$(mktemp -d)
```

There are three verification modes, and each establishes more than the one before it.

**Input integrity: hash checks only.** Every retained object stored under its decoded
SHA-256 must decode to that hash.
The loop prints nothing when all 36 do.
The seven role-named packets in `capture-ancestry/objects/` are bound by their
[provenance](receipts/capture-ancestry/provenance.json) instead.
Each checker below also verifies its own inputs’ hashes before computing.

```sh
for f in $R/*/objects/[0-9a-f]*.gz; do
  test "$(gzip -cd "$f" | sha256sum | cut -d ' ' -f 1)" = "$(basename "$f" .gz)" \
    || echo "CHANGED $f"
done
```

**Retained composition: the inventory and the composer, no geometry.** They check
identities, case IDs and state joins over the recorded executions.
[Recheck the Retained Execution](#recheck-the-retained-execution) says which results to
accept.

```sh
timeout 120 .venv/bin/python3 -m devtools.inventory_n11_completion --out "$OUT/completion.json"
timeout 120 .venv/bin/python3 -m devtools.check_n11_final_composition --out "$OUT/composition.json"
```

**Fresh geometry: the checkers.** Each recomputes its component from the retained
inputs and refuses an input whose hash is not the one it pins.
The `--max-seconds` values are the receipts’ recorded ceilings.
A run that reaches its ceiling stops without a verdict, so on a slower or busier
machine raise `--max-seconds` and the outer `timeout` together.

The exact witness:

```sh
timeout 60 .venv/bin/python3 -m cases.trump11.verify_exact
```

The D4 reduction and the case census. The D4 checker reads decoded JSON, so the three
objects its receipt names are decoded first.

```sh
for role in cover overlay distance; do
  key=$(jq -r ".input_sha256.$role" $R/d4-independent/result.json)
  gzip -cd "$R/d4-independent/objects/$key.gz" > "$OUT/d4-$role.json"
done
timeout 60 .venv/bin/python3 -B -m devtools.check_n11_optimality_d4 \
  --cover "$OUT/d4-cover.json" --overlay "$OUT/d4-overlay.json" \
  --distance "$OUT/d4-distance.json" --max-seconds 45 --output "$OUT/d4.json"
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_case_census \
  --objects $R/case-census/objects --cover $COVER --max-seconds 30 \
  --output "$OUT/case-census.json"
```

Local isolation, its one-branch partial control, and the dual residuals, from the two
objects the local receipt names:

```sh
for role in weighted focused; do
  key=$(jq -r ".input_sha256.$role" $R/local-isolation/result.json)
  gzip -cd "$R/local-dual-residual/objects/$key.gz" > "$OUT/local-$role.json"
done
timeout 60 .venv/bin/python3 -B -m devtools.check_n11_optimality_local_isolation \
  --weighted "$OUT/local-weighted.json" --focused "$OUT/local-focused.json" \
  --branch-limit 128 --max-seconds 45 --output "$OUT/local-isolation.json"
timeout 60 .venv/bin/python3 -B -m devtools.check_n11_optimality_local_isolation \
  --weighted "$OUT/local-weighted.json" --focused "$OUT/local-focused.json" \
  --branch-limit 1 --max-seconds 45 --output "$OUT/local-isolation-partial.json"
timeout 30 .venv/bin/python3 -B -m devtools.check_n11_optimality_local_dual \
  --weighted "$OUT/local-weighted.json" --focused "$OUT/local-focused.json" \
  --branch-limit 128 --max-seconds 25 --output "$OUT/local-dual.json"
```

Pose inclusion reads the publisher’s near-leaf state, which this repository does not
retain.
Acquire it at the pinned URL in its [provenance](receipts/pose-inclusion/provenance.json):
a Git LFS object of 27,653,954 compressed bytes, SHA-256
`5d74352c6c05fd4e0ea4d4842915061603669a54205af2a59cf2303051a48949`.
Decompressed, it is 185,901,535 bytes, and its SHA-256 must be the one the receipt binds
as `source_sha256`, which the command tests first.
The checker uses `jq` to extract the live rows.

```sh
NEAR=/path/to/near-refined1024-240.json
test "$(sha256sum "$NEAR" | cut -d ' ' -f 1)" = \
  491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_pose_inclusion \
  --source "$NEAR" --guards $R/pose-inclusion/guard.json \
  --focused $R/local-dual-residual/objects/9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3.gz \
  --local-result $R/local-isolation/result.json --max-seconds 30 \
  --output "$OUT/pose-inclusion.json" --derived-output "$OUT/pose-derived-state.json.gz"
```

The six field certificates. Masks 0 and 202 each have a dedicated checker and a run of
the shared field runner; masks 612 and 1155 have the runner alone.

```sh
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_field_mask0 \
  --objects $R/field-mask0/objects --cover $COVER --all \
  --max-seconds 30 --max-nodes 100000 --output "$OUT/field-mask0.json"
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_field_mask202 \
  --objects $R/field-mask202/objects --cover $COVER --all \
  --max-seconds 30 --max-nodes 100000 --output "$OUT/field-mask202.json"
timeout 35 .venv/bin/python3 -m devtools.check_n11_optimality_field_runner \
  --mask-index 0 --objects $R/field-mask0/objects --cover $COVER --all \
  --max-seconds 30 --max-work 100000 --output "$OUT/shared-field-mask0.json"
timeout 35 .venv/bin/python3 -m devtools.check_n11_optimality_field_runner \
  --mask-index 202 --objects $R/field-mask202/objects --cover $COVER --all \
  --max-seconds 30 --max-work 100000 --output "$OUT/shared-field-mask202.json"
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_field_runner \
  --mask-index 612 --objects $R/field-mask612/objects --cover $COVER --all \
  --workers 3 --max-seconds 55 --max-work 5000000 --output "$OUT/field-mask612.json"
timeout 60 .venv/bin/python3 -m devtools.check_n11_optimality_field_runner \
  --mask-index 1155 --objects $R/field-mask1155/objects --cover $COVER --all \
  --workers 3 --max-seconds 55 --max-work 5000000 --output "$OUT/field-mask1155.json"
```

The field runner in this checkout is newer than the revision that wrote the shared,
612 and 1155 receipts.
Its results carry the current checker hash and add `physical_atom_ids`,
`required_charge` and CPU-accounting fields; every field the retained receipts have
matches.

| Check | Result it reported | Wall seconds here |
| --- | --- | --- |
| Exact witness | `VALID: 11 squares, 55 pairs tested` | 0.6 |
| D4 reduction | `PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE` | 2.8 |
| Case census | `PASS_CASE_CENSUS_ONLY` | 0.2 |
| Local isolation | `PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION` | 22 to 39 |
| Partial control, one branch of 128 | `INCOMPLETE_FIXED_T_LOCAL_ISOLATION`, as intended | 8.9 |
| Dual residuals, which leave curvature to local isolation | `INCOMPLETE_LOCAL_DUAL_PROFILE`, as retained | 13.8 |
| Pose inclusion | `PASS_POSE_INCLUSION` | 4.4 |
| Field mask 0, dedicated and shared runs | 459 cases excluded by each | 16.7 and 17.3 |
| Field mask 202, dedicated and shared runs | 764 cases excluded by each | 18.4 and 18.6 |
| Field masks 612 and 1155 | 459 and 252 cases excluded | 7.5 and 10.7 |
| Completion inventory | 2,180 accepted exclusions; none missing | 2.9 |
| Final composition | `PASS_REVIEWED_COMPONENT_COMPOSITION`; no pending obligations | 3.2 |

Wall times varied with load from other processes on the machine.
Under heavy load the shared mask-202 run reached its 30-second ceiling and stopped
without a verdict; rerun when the machine was less busy, it passed.
The checkers refuse to overwrite an existing output, so each rerun needs a new `OUT`.

These are separate component executions.
The capture nodes are not among them: their checkers need the publisher’s source states
and byte-exact parent receipts, as the next section explains.

## Retained Replacement Components

GPT-6 Pro’s [review of October 3](../../../../docs/project/reviews/review-2026-10-03-n11-optimality-adversarial-gpt6-pro-unified.md)
proposed four checked replacements for components of this packet, and the
[integration record](../../../../docs/project/reviews/review-2026-10-03-n11-gpt6-pro-review-integration.md)
retains each beside the accepted component it would replace.
None of them is a premise of the accepted proof, and none changes a frozen checker or an
accepted receipt; each is a second route to the same conclusion, bound by its own
receipt.

| Component | Replaces | Checker and receipt | Replay |
| --- | --- | --- | --- |
| Corrected closed-interval cover kernel | the interval helper inside the frozen union-cover sweep, for new callers only | `devtools/n11_closed_interval_cover.py`; its 12,180-case control is `tests/test_n11_closed_interval_cover.py` | `pytest tests/test_n11_closed_interval_cover.py` |
| D4 incidence bridge | the exhaustive assignment search of the symmetry lemma | `devtools/check_n11_optimality_d4_incidence.py`; [`receipts/d4-incidence/`](receipts/d4-incidence/result.json) | `receipts/d4-incidence/replay.sh` |
| Two-radius local box | the fitted 33-radius rectangle of the local isolation theorem | `devtools/check_n11_optimality_local_two_radius.py`; [`receipts/local-isolation-two-radius/`](receipts/local-isolation-two-radius/result.json) | `receipts/local-isolation-two-radius/replay.sh` |
| Minimal field-certificate selection | nothing; a reading aid naming the 44 of 46 accepted field packets whose union is the whole field exclusion | `devtools/select_n11_field_minimum.py`; [`receipts/field-batch-a/minimal-selection.json`](receipts/field-batch-a/minimal-selection.json) | `python -m devtools.select_n11_field_minimum` |

The two replay scripts use repository-relative paths and verify their inputs’ hashes
themselves; run from any directory, each reproduces its `result.json` exactly, timings
aside.

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
The four, by leaf, with the prefix the publisher states and the prefix of the object as
observed and bound by the [source graph](receipts/source-graph/result.json), for whoever
rebinds them in a corrected release:

| Leaf | Publisher’s final-state digest | Observed final-state digest |
| --- | --- | --- |
| Far 15 | `3b7f1ea0` | `9e28b092` |
| Far 13 | `f83eb23c` | `87482985` |
| Far 2 | `7551646f` | `11d4a28e` |
| Near | `81002706` | `a6d45c0c` |


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
