# Wang Ke and Li Can’s `s(11)` Certificate, Zenodo 23038546

Wang Ke (王可) and Li Can (李灿) of Fudan University report
`s(11) > 3875000000/999999999 = 3.875000003875…`, which is `31/7999999992` above the
registered `s(11) > 31/8` of Kleddamag’s certificate (retained in
[`external-square-certificates-2026-09-22/kleddamag-11/`](../external-square-certificates-2026-09-22/kleddamag-11/)).
Their certificate is Kleddamag’s `global-certificate.json` with thirteen
threshold-charge orbit weights raised and the parent side `A` and every row’s core side
`B` multiplied by `999999999/1000000000`. The claim reached this repository as
[jlevy/squares#247](https://github.com/jlevy/squares/issues/247), opened by GitHub user
XiaoLiaoShe on 2026-09-29 at 13:38 UTC.

This packet holds the Zenodo record’s two files byte-identical, the archive extracted
beside them, the replay receipts made here, and one minimally adapted copy of
Kleddamag’s launcher.
Retention registers the claim for review; it does not move a Frontier bound.

## Provenance

| Field | Value |
| --- | --- |
| Record | <https://zenodo.org/records/23038546>, version `1.0.0`, resource type Preprint |
| DOI | [10.5281/zenodo.23038546](https://doi.org/10.5281/zenodo.23038546); concept DOI `10.5281/zenodo.23038545` |
| Title | *An Exact Computer-Assisted Improvement of the Lower Bound for Packing Eleven Unit Squares* |
| Creators | Wang, Ke and Li, Can, both Fudan University |
| Published | 2026-09-29 (record created and modified 2026-09-29T12:27:13Z; the two file entries were last updated 13:13:57Z and 13:27:50Z) |
| Licence | The record lists CC-BY-4.0 only. The archive’s `LICENSE_STATUS.md` scopes it as mixed: the authors’ prose, paper and records CC BY 4.0, their verifier code MIT, the bundled Kleddamag code under Kleddamag’s MIT notice, and the certificates under the upstream attribution in `THIRD_PARTY_NOTICES.md` |
| Related identifiers | `isDerivedFrom` <https://github.com/Kleddamag/11-squares-certified-bound>; `references` <https://github.com/jlevy/squares> |
| Retrieved | 2026-09-30T05:27Z, from `https://zenodo.org/api/records/23038546` and each file’s `/content` link |

The API responses are retained as [`zenodo-23038546.json`](zenodo-23038546.json) (the
record) and [`zenodo-23038546-files.json`](zenodo-23038546-files.json) (the file
listing).

**Credit, as the source states it.** `AUTHORS.md` claims only “the 13-orbit reweighting,
the exact common rational parent/core shrink, the derived certificate, and the
verification/release work for the improved ratio”, and disclaims Kleddamag’s
certificate, the Squares Project framework and data, Trump’s packing and the general
threshold-counting method.
`SOURCE_ATTRIBUTION.md` traces the certificate through Kleddamag to this repository’s
T-026 at `7ccb679c`. Neither the record, the archive nor the preprint says whether AI
tools were used in the work.

## Retained Files

| File | Bytes | What it is |
| --- | ---: | --- |
| [`n11_wang_li_zenodo_release_2026-09-29_stage10_doi_23038546-1.zip`](n11_wang_li_zenodo_release_2026-09-29_stage10_doi_23038546-1.zip) | 2,495,053 | The release archive, 49 entries (42 files) |
| [`n11_lower_bound_wang_li.pdf`](n11_lower_bound_wang_li.pdf) | 294,739 | The preprint, six pages, as a separate record file |
| [`n11_wang_li_zenodo_release_2026-09-29/`](n11_wang_li_zenodo_release_2026-09-29/) | 9,899,885 in all | The archive extracted with `unzip`, every entry at its archive path |

**The one digest boundary.** Both downloads were compared with the MD5 checksums the
Zenodo API publishes for them, `ae343d3220a5a11f7bd22e59f4382873` (PDF) and
`52c82aee798ab94d3733c749eecd70de` (archive), and both match.
The extracted `certificate/improved-global-certificate.json` has SHA-256
`31e10ceb8368cc858e61f45ce7cfee783e8d0c7910893559164810f45439cc34`, the value the
authors published in the issue and the preprint.
These comparisons detect a transfer or storage fault between Zenodo and this checkout
and a certificate other than the one the authors announced; everything after them is
identified by path and Git revision.

The archive’s `certificate/global-certificate-original.json` is byte-identical to
Kleddamag’s retained `global-certificate.json` (`cmp`), and its
`verifier/primary_kleddamag/exact_mixed.py` to Kleddamag’s. Its `integer_sweep.py`
differs from Kleddamag’s only by two blank lines, and its `replay_parallel.py` by a
docstring and blank lines.

The archive’s `paper/n11_lower_bound_wang_li.pdf` (254,473 bytes) is a different build
from the record’s separate PDF; `AUDIT_LOG.md` says the PDF was regenerated from the
LaTeX source during packaging.
The record’s PDF was read in full and agrees with `paper/n11_lower_bound_wang_li.tex`.

Seven extracted data files exceed 1,000 lines: the two certificates, the merged fresh
replay receipt and its four quarter receipts.
They are kept plain rather than as the deterministic gzip that
[`packing/resources/README.md`](../../README.md) describes: the source certificate is
then the same Git blob as Kleddamag’s retained copy, and the retained archive already
carries every file compressed.
The source trees are not passed through this repository’s Markdown formatter.

## The Change, Derived From the Two Files

[`devtools.audit_wang_li_n11 diff`](../../../devtools/audit_wang_li_n11.py) derives the
change from the source and improved files alone and compares it with the stated one, in
5.0 s wall and 2.9 s CPU; its output is
[`receipts/certificate/diff.json`](receipts/certificate/diff.json).

| Quantity | Kleddamag | Wang and Li |
| --- | --- | --- |
| Container side `L` | `191/50` | unchanged |
| Parent side `A` | `764/775` | `190999999809/193750000000 = A·λ`, `λ = 999999999/1000000000` |
| Core side `B` of each of the 12,028 rows | as listed | each exactly `λ·B`; every interval `[a, b]` and core half-tangent `t` unchanged |
| Point orbits (679) | as listed | unchanged |
| Charge orbits (284) | as listed | thirteen weights raised, nothing else changed |
| Budget `M`, units of `10⁻⁹` | 10,999,479,944 | 11,000,095,024 (+615,080) |
| Minimum charge `Γ`, units of `10⁻⁹` | 999,962,528 | 1,000,047,559 (+85,031) |
| Counting surplus `11Γ − M` | 107,864 | 428,125 |
| Bound `L/A` | `31/8` | `3875000000/999999999 = (31/8)/λ` |
| Minimum strict core margin | `1/10¹²` | `λ/10¹²` |

The certificate’s own `bound` field changes from `31/8` to `3875000000/999999999`; no
checker reads it.

The thirteen raised orbits, all nonnegative increments:

| Orbit | Feature | Features in orbit | Weight before | Increment | Budget increment |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3 | 2-of-3 | 8 | 863,818 | +1 | +8 |
| 27 | 2-of-3 | 8 | 370,820 | +4 | +32 |
| 43 | 2-of-3 | 8 | 9,293,472 | +3 | +24 |
| 51 | 3-of-5 | 8 | 1,924,284 | +4,384 | +35,072 |
| 52 | 2-of-5 | 8 | 5,679,789 | +7 | +112 |
| 130 | 2-of-5 | 8 | 14,211,519 | +34,344 | +549,504 |
| 131 | 2-of-5 | 8 | 4,083,535 | +1 | +16 |
| 174 | 3-of-5 | 8 | 878,087 | +3,776 | +30,208 |
| 206 | 2-of-3 | 4 | 19,257,662 | +5 | +20 |
| 207 | 2-of-3 | 8 | 58,655 | +1 | +8 |
| 218 | 3-of-5 | 4 | 9,486,754 | +7 | +28 |
| 232 | 2-of-3 | 8 | 15,651 | +5 | +40 |
| 259 | 2-of-3 | 8 | 153,071 | +1 | +8 |

Exact arithmetic: `L/A′ = (191/50)/(190999999809/193750000000) = 3875000000/999999999`,
and `3875000000/999999999 − 31/8 = 31/7999999992 ≈ 3.875 × 10⁻⁹`.

**Why only coverage needs rechecking.** Every premise of the transfer theorem other than
coverage is homogeneous of degree one in `(A, B)`, so a common factor `λ > 0` preserves
it exactly: the strict containment margin `A − B·max(cos δ + |sin δ|)` becomes `λ` times
itself, as do the centre margin `r = A·min(cos u + sin u)/2` and both sides of the
envelope condition `B(cos t + sin t)/2 ≤ r`. The angle cover and the charges do not
involve `A` or `B`. The diff tool checks each of these row by row with exact fractions,
and every checker below re-derives them from the new parameters rather than assuming
them. Coverage is not homogeneous, because the sites stay where they are while the cores
shrink and the parent-centre domain `[r, L − r]²` grows.

## Replays Here

All runs used the pinned bytes, on a four-core Linux container shared with other lanes
(load averages 4 to 13 throughout), so every wall time is a contended reading.
The authors’ and Kleddamag’s checkers ran in a separate environment, CPython 3.14.7 with
the authors’ pins `numpy==2.3.5`, `numba==0.65.1` and `llvmlite==0.47.0`, installed with
`uv pip` instead of the README’s `pip`; Node.js was 22.22.2. Each receipt under
[`receipts/`](receipts/) records its command, start time and load, exit status, wall and
CPU.

| Route | Command | Wall | CPU | Result |
| --- | --- | ---: | ---: | --- |
| Authors, integrity | `python verify.py --mode integrity` in a fresh extraction of the retained archive | 0.3 s | 0.2 s | `PASS_STATIC_INTEGRITY` ([log](receipts/authors/integrity.log)) |
| Authors, smoke | `python verify.py --mode quick` | 9.0 s | 8.1 s | `PASS_QUICK_SMOKE`: row 0 is `1000047559` in both verifiers ([log](receipts/authors/quick.log)) |
| Authors, primary full replay | first half of `python verify.py --mode full --jobs 1` (the README says `--jobs 5`) | 4,206 s | in the total below | `PASS_FULL_EXACT_PYTHON_REPLAY`: histogram `{1000047559: 12028}`, 86,299,918 slabs, 511,649,696,956 cells; every row’s minimum, cells and slabs equal the archive’s fresh receipt ([`primary.json`](receipts/authors/fresh-full-replay/primary.json)) |
| Authors, independent full replay | second half of the same command | 5,146 s | in the total below | `PASS_INDEPENDENT_FULL_REPLAY`: histogram `{1000047559: 12028}`, zero bad rows ([`independent.json`](receipts/authors/fresh-full-replay/independent.json)) |
| Authors, full mode in total | `python verify.py --mode full --jobs 1` | 9,356 s | 5,299 s | `PASS_FRESH_TWO_IMPLEMENTATION_FULL_REPLAY` ([`RESULT.json`](receipts/authors/fresh-full-replay/RESULT.json), [log](receipts/authors/full.log)) |
| Kleddamag’s checkers | `check_integrity.py`, `verify_threshold_algebra.py`, then `verify_wang_li.py --output-dir OUT`, the adapted launcher below, from 2026-09-30T08:14:51Z | 8,207 s | 5,564 s | `PASS_FRESH_PORTABLE_FULL_VERIFICATION`: all 12,028 intervals by the Python and the BigInt JavaScript sweeps, minimum `1000047559`, budget `11000095024`, surplus `428125`; `independent_controls.py` gives `PASS_INDEPENDENT_EXACT_CONTROLS` over 48,112 containment quadratics ([`RESULT.json`](receipts/kleddamag/full-replay/RESULT.json), [log](receipts/kleddamag/run.log)) |
| Native interval, pilot | `.venv/bin/python3 -m devtools.verify_n11_parent_core_native --pilot --workers 1 --output …` | 45.8 s | 19.6 s | rows 0, 11962 and 12027 certified at `1000047559` with zero stalls ([receipt](receipts/native/native-pilot.json)) |
| Native interval, all rows | the same with `--all --workers 2 --batch-size 2048`, 05:48 to 11:02 UTC | 18,854 s | 11,957 s | `PASS_COMPLETE`: all 12,028 rows certified at the threshold `1000047559`, 136,388,356 boxes, zero stalls, no exhausted budget, no refutation ([`native-all.json`](receipts/native/native-all.json), [log](receipts/native/native-all.log), row journal `native-all.rows.jsonl`) |

**The authors’ two verifiers.** The primary is Kleddamag’s event-cell sweep, copied
(above). The second, `verifier/independent/`, is the authors’ own block range-minimum
sweep. It never reads `improved-global-certificate.json`: at import it rebuilds the
certificate from the source file, the weight deltas in
`evidence/reweighted_fullscan_receipt.json` and `λ`, and compares every row with a
hard-coded target `1000047559`, passing on equality with it rather than on the theorem’s
`11·min > M`. The rebuilt certificate equals the improved file in every field it reads;
it keeps the source’s declared `bound`, `budget_units` and `minimum_units`, which it
does not read. The tie between the two is the integrity mode’s structural comparison.

**Kleddamag’s checkers.** The Python sweep, the BigInt JavaScript sweep that
`prepare_secondary.py` reconstructs from Guzhou’s R038 source, and
`independent_controls.py` all read `A`, the rows, the budget and `Γ` from the
certificate; the JavaScript and `exact_mixed.py` fix `L = 191/50`, which is unchanged.
Only the launcher `verify.py` pins Kleddamag’s certificate: its path, SHA-256, bound,
`Γ`, budget and surplus.
[`replay/kleddamag-verify-wang-li.py`](replay/kleddamag-verify-wang-li.py) changes those
values and the job count from three to one, three lines in all
([`replay/kleddamag-verify-wang-li.diff`](replay/kleddamag-verify-wang-li.diff)). It
runs from a scratch copy of `kleddamag-11/` holding the improved certificate as
`improved-global-certificate.json`, after `prepare_secondary.py --source` on the
retained R038 file, as in the
[2026-09-22 receipts](../external-square-certificates-2026-09-22/receipts/n11/README.md).

**The native interval checker.** `devtools.verify_kleddamag_n11_native` reads `A`, the
rows, the charges, `M` and `Γ` from the certificate; its loader fixes `L = 191/50` and
`n = 11`. Its one Kleddamag-specific constant is the release pin `REVIEWED_SHA256`, and
the file is a frozen proof input of the retained T-037 run, so it is unchanged.
[`devtools.verify_n11_parent_core_native`](../../../devtools/verify_n11_parent_core_native.py)
clears the pin for one run and calls the frozen `run`; its receipt records that all 19
frozen inputs still equal their blobs at `c183cc9a`. On a Kleddamag row it decides
exactly as the frozen tool does (`tests/test_wang_li_n11.py`). The native premise check
gives the minimum containment numerator `999999999/10²¹`, `λ` times the source’s.

## Controls

Every mutation must be refused, and was, by each checker that reads what it changes.
The mutations are defined once, in `devtools.audit_wang_li_n11.MUTATIONS`.
[`receipts/controls/source-checkers.json`](receipts/controls/source-checkers.json) runs
them through Kleddamag’s `exact_mixed.py`, the authors’ independent verifier and the
BigInt JavaScript sweep (32.7 s wall, 21.2 s CPU);
[`receipts/controls/native.json`](receipts/controls/native.json) through the native
checker (36.5 s wall, 22.2 s CPU), which refutes each coverage mutation with an exact,
admissible witness.

| Mutation | Row | Kleddamag Python | Authors’ independent | BigInt JavaScript | Native interval |
| --- | ---: | --- | --- | --- | --- |
| `Γ` raised by one unit | 0 | refused, minimum `1000047559` | not applicable: reads no `Γ` | refused | refuted, witness `1000047559` |
| `Γ` lowered to `⌊M/11⌋` | 0 | refused, counting | not applicable | refused, counting | refused, “no strict counting gap” |
| Orbit 130 back to its source weight | 8844 | refused, `999978871` | refused, `999978871` | refused, `999978871` | refuted, witness `999978871` |
| `λ = 1 − 2·10⁻⁹` in place of `1 − 10⁻⁹` | 615 | refused, `998920060` | refused, `998920060` | refused, `998920060` | refuted, witness `998920060` |
| Scaled until `L/A ≥ 3.877084`, above Trump’s packing | 0 | refused, `419457180` | refused | refused | refuted, witness `975617953` |

**The scaling is at its edge.** One more step of `10⁻⁹` opens a cell of charge
`998920060` at row 615, so `λ = 1 − 10⁻⁹` is the last passing value on the authors’
grid. The preprint’s own control is coarser: it reports that `λ = 1 − 2 × 10⁻⁷` fails at
rows 543 to 574 and 615 to 626. `devtools.audit_wang_li_n11 cliff`, run in the upstream
interpreter over those 44 rows, finds exactly those rows below `Γ` at `2 × 10⁻⁷`, only
row 615 at `2 × 10⁻⁹`, and none at `10⁻⁹` (56.3 s wall, 32.2 s CPU;
[`receipts/controls/cliff.json`](receipts/controls/cliff.json)).

## Reproduce

From `packing/`:

```bash
.venv/bin/python3 -m devtools.audit_wang_li_n11 diff --output OUT/diff.json
.venv/bin/python3 -m devtools.verify_n11_parent_core_native --pilot --output OUT/pilot.json
.venv/bin/python3 -m devtools.verify_n11_parent_core_native --all --workers 2 --output OUT/all.json
.venv/bin/python3 -m devtools.verify_n11_parent_core_native --controls --output OUT/native-controls.json
```

The source-checker controls and the source replays need a separate interpreter with
NumPy and Numba, and writable scratch copies of `kleddamag-11/` and of the extracted
release:

```bash
uv venv --python 3.14.7 UPSTREAM
uv pip install --python UPSTREAM/bin/python numpy==2.3.5 numba==0.65.1 llvmlite==0.47.0
cp -R resources/web/external-square-certificates-2026-09-22/kleddamag-11 KLEDDAMAG
UPSTREAM/bin/python KLEDDAMAG/prepare_secondary.py --source \
  resources/web/external-square-certificates-2026-09-22/dependencies/guzhou-r038/certificates/R038/src/exact_parent_side_scan.js
unzip -d RELEASE resources/web/wang-li-n11-2026-09-29/n11_wang_li_zenodo_release_2026-09-29_stage10_doi_23038546-1.zip
.venv/bin/python3 -m devtools.audit_wang_li_n11 controls --upstream-python UPSTREAM/bin/python \
  --kleddamag-tree KLEDDAMAG --release-tree RELEASE/n11_wang_li_zenodo_release_2026-09-29 \
  --output OUT/source-controls.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
