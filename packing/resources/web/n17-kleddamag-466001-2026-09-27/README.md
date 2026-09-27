# Kleddamag’s `4.66001` Lower Bound for `s(17)`, Retrieved 2026-09-27

A third-party exact computer-assisted lower bound on `s(17)`, the least side of a square
holding seventeen unit squares with disjoint interiors.
Kleddamag, building on Squares Project (Joshua Levy), Mira and Guzhou0806: an exact
weighted-certificate proof over 2,168 orientation intervals.
It is retained because it is the strongest public claim for this case the record has
seen, `1999/100000 = 0.01999` above the same repository’s `v1.1.0` bound `232001/50000`
then on the frontier, and because its replay is cheap enough to repeat here: a fixed
rational certificate and two exact sweeps.

This packet holds the source bytes and the replay receipts.
The registration is in [`n-017.md`](../../../frontier/n-017.md) and
`E-n017-kleddamag-466001-source-replay` in
[`evidence.yaml`](../../../frontier/evidence.yaml); the mathematical review is a
separate record, `docs/project/reviews/review-2026-09-27-n17-kleddamag-466001.md`.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Kleddamag/17-squares-certified-bound> |
| Tag | none; the commit is `main`’s head at retrieval, and the release’s `CHANGELOG.md` lists it as unreleased |
| Commit | `57519bb74085157cb7047ae94c599bce4a006430`, “Publish verified bound s(17) > 4.66001” |
| Tree | `024ead7cae9ca349cf1e7b4a2155f0a990a7d7b6` |
| Committed | 2026-09-27T16:26:09+02:00 |
| Retrieved | 2026-09-27 |
| Previous release | `v1.1.0` at `13821ddf`, retained in [`../n17-kleddamag-4640020-2026-09-26/`](../n17-kleddamag-4640020-2026-09-26/README.md) |
| Certificate | `bounds/4.66001/certificate.json`, SHA-256 `280af3d46150ca990917d714d83ee73baf4e6c45a0563090bf35588fb22de6e5` |
| Release `MANIFEST.json` | `c671346cefe181803f6b575ae4b50ded0b6f367d27a163e52b96fbad94087716` |

The certificate digest is the one the release’s README, `CURRENT_BOUND.json`,
`PROOF.md`, `MANIFEST.json` and `evidence/theorem-identities.json` all state, and the
one both checkers report.

**Credit.** Kleddamag, building on Squares Project (Joshua Levy), Mira and Guzhou0806.
`ATTRIBUTION.md` places the result in the lineage it already named for `v1.1.0`:
Joshua Levy’s squares project for the weighted-covering, strict-core, event-cell and
threshold-budget methods, citing the parent-centre contract and the T-025 threshold
certificate; Mira-acc/17squares for the numerical support and parent-angle catalogue;
and Guzhou0806 / N17 project’s R038 for the parent-side reduction.
It claims no invention of those methods, says attribution implies no upstream
coauthorship or endorsement, and says no external Guzhou source or C++ code is included
in or run by this proof path.
Kleddamag publishes a handle only, and no fuller name is inferred here.
`AUTHORS.md` says the work was produced with AI agents (OpenAI Codex) under Kleddamag’s
direction, combining completed charges from separate research tasks, and that
“independent” in the release means distinct implementations or separately written
audits, not independent human peer review or a proof assistant.

## The claim

$$
s(17) > \frac{466001}{100000} = 4.66001
$$

The container side is `L = 4613/1000` and the parent side is `A = 461300/466001`, so the
bound is `L/A`. Weights have denominator `10^9`; site coordinates have denominator
`10^10`.

| Quantity | Exact value |
| --- | ---: |
| Total budget `M` | 17000402008 units |
| Certificate’s requested minimum | 1000023648 units |
| Replayed minimum core charge `Γ` | 1000026844 units |
| `17Γ − M` | 54340 units |
| Angle intervals | 2,168 |
| Least strict core margin | just above `10^−10` (exact value in the controls receipt) |

The release makes no claim about the exact minimum and no better packing; its unchanged
`upper-packing-certificate.json` is the Bidwell reconstruction retained with `v1.0.0`.

## Method

The same parent-core argument as `v1.1.0`, with the same feature kinds and budget
rules on many more orbits. Over `2,620` site orbits (`20,856` sites) there are `889`
positive charge orbits, `7,048` feature images in all:

| Feature | Orbits | Budget per image | Share of `M` |
| --- | ---: | --- | ---: |
| Point capture (one of one) | 224 | 1 | 4940613824 |
| Two of three | 225 | 1 | 3499582848 |
| Three of five | 30 | 1 | 1189979088 |
| Four of seven | 2 | 1 | 1368144 |
| Weighted `2, 1, 1, 1` at 3 | 144 | `⌊5/3⌋ = 1` | 1721097168 |
| Weighted `2, 1, 1, 1, 1, 1` at 4 | 3 | `⌊7/4⌋ = 1` | 75379744 |
| Weighted `2, 1, 1, 1, 1, 1, 1, 1` at 5 | 1 | `⌊9/5⌋ = 1` | 8711680 |
| Weighted `4, 1, 1, 1, 1, 1` at 5 | 6 | `⌊9/5⌋ = 1` | 74581096 |
| Pairwise-intersecting winning subsets on 3, 4, 5, 6, 7, 9 and 10 sites | 15, 78, 41, 9, 104, 2, 5 | 1 | 5489088416 |

The shares sum to `M`, recomputed here from the certificate’s weights and images, and
every one of the `86` distinct rules has capacity one, which the controls confirm by
exhausting its capture patterns.
The charge combines two completed candidates, and eight of an original `2,048`
intervals are subdivided sixteen ways with regenerated strict cores, the charge held
fixed.
The certificate’s embedded `source` string still reads “Best complete new-target
numerical scan, exact diagnostic pending”; the release explains this as text from an
earlier construction stage, kept so the certificate hash does not change.

The two checkers are the `v1.1.0` ones byte for byte: `verify_global_python.py`
(arbitrary-precision rational geometry and a Numba integer sweep),
`verify_global_variable.js` (BigInt geometry and an exact integer sweep), and their
three `global_src/` modules. The launcher `verify.py` differs from `v1.1.0`’s only in
its default target and the interval count it asserts, and `controls.py` only in its
target and the four intervals it samples. The launcher runs both checkers concurrently
and requires every interval from each, equal minima and cell counts on every interval,
the certificate identity, and the strict count.

## What Is Retained, and What Is Not

**Retained byte-identical** under `kleddamag-17-squares-certified-bound/`, at their
release paths: the 33 files that changed or were added between `v1.1.0` and
`57519bb7`.
That is the whole `bounds/4.66001/` package (23 files: the certificate, proof, method
note and package README, the launcher, both checkers and their three shared modules,
the controls script, the theorem identities, and the source’s publication and
coordinator receipts), the new `README-v1.1.0.md` (the `v1.1.0` `README.md`, moved),
`CURRENT_BOUND.json`, and the eight root files the commit edited: `README.md`,
`ATTRIBUTION.md`, `AUTHORS.md`, `CHANGELOG.md`, `LICENSING.md`, `MANIFEST.json`,
`PROOF.md` and `VERIFICATION.md`.
Every file’s `git hash-object` equals its blob at `57519bb7`; seven ledgers are
stored as deterministic gzip, and for those the identity holds after decompression
([Compressed Files](#compressed-files)).

**Not duplicated:** the release’s other 103 files, unchanged since `v1.1.0`. Their blobs
at `57519bb7` equal the copies already retained, checked file by file: 29 in the
[`v1.1.0` packet](../n17-kleddamag-4640020-2026-09-26/README.md) (the rest of
`bounds/4.640020/` and `README-v1.0.0.md`) and 74 in the
[`v1.0.0` packet](../n17-kleddamag-certified-bound-2026-09-21/README.md), among them
`LICENSE`, `NOTICES/` and `global-certificate.json`.
Overlaying the three packets’ trees in release order reconstitutes the full 136-file
tree at `57519bb7`, and the release’s own `check_integrity.py` passes over it (below).

**Omitted:** `.git/`, and the replay outputs themselves. `receipts/` keeps the
launcher’s `theorem.json`, each checker’s log, the controls’ `controls.json`, and
digests of the fresh row ledgers with their comparison against the source’s.

**Licensing.** `LICENSING.md` adds that the new package reuses the project’s own
general-rule engines from `bounds/4.640020/` with their licence and attribution scope
unchanged, under the MIT `LICENSE` retained with the `v1.0.0` packet. This packet is
retained for verification and research use.

## Replay Here

Every command ran on 2026-09-27 in a Linux container with 4 cores, against the
retained bytes before they were compressed (restore them to repeat it), from `kleddamag-17-squares-certified-bound/`, with outputs written
outside this packet and `PYTHONDONTWRITEBYTECODE=1` so the checkers’ subprocesses left
no bytecode in it. The checkers ran under a separate CPython 3.14.7 environment holding
exactly the release’s pinned `numpy==2.3.5`, `numba==0.67.0` and `llvmlite==0.49.0`,
with Node `v22.22.2`. [`receipts/replays.json`](receipts/replays.json) records each
command, interpreter, start, wall and exit.

```sh
python -X utf8 -B bounds/4.66001/verify.py --output-directory OUT/full --workers 1
python -X utf8 -B bounds/4.66001/controls.py --output-directory OUT/controls
```

| Run | Wall | Exit | Status | What it establishes |
| --- | ---: | ---: | --- | --- |
| full | 2,203.59 s | 0 | `PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION` | Both complete checkers over all 2,168 intervals: minimum `1000026844`, budget `17000402008`, surplus `54340` |
| controls | 23.76 s | 0 | `PASS_RULE_BUDGET_SWEEP_AND_NEGATIVE_CONTROLS` | Every capture pattern of the 86 distinct rules and their disjoint-winner budgets, direct against segment-tree sweeps with Node agreement at intervals 0, 541, 1084 and 2167, and eight corrupted certificates rejected by both checkers |
| integrity | under 1 s | 0 | `PASS: 135 release files match their SHA-256 manifest.` | The `v1.0.0`, `v1.1.0` and this packet’s trees overlaid are the release, file for file |

Inside the full run the Python checker took 2,185 s on one worker and the Node process
2,203 s over all 2,168 intervals, while two unrelated sweeps held about 2.5 of the four
cores and a validation tier ran for part of it; walls are readings, not benchmarks.

The launcher checks everything it prints: both checkers cover every interval, their
minima and cell counts agree interval by interval, both report the certificate digest,
and `17 × 1000026844 = 17000456348 > 17000402008`. Beyond that, the fresh ledgers
reduced to `(interval, minimum, cells)` are identical to the source’s two published
pairs of ledgers, the coordinator’s replay and the publication replay, all hashing to
`19952dbb…dbb4`. Every one of the 2,168 intervals attains the same minimum
`1000026844`, and the sweeps visit `966,922,806,680` centre cells in all. The fresh `controls.json` equals the source’s
`publication-controls.json` apart from its timestamp.

What these replays do **not** establish is independence of method.
Both checkers decide the same exact event-cell sweep of the same certificate, written by
the same project, and they are the bytes already replayed for `v1.1.0`. This
repository’s native parent-core route (`devtools.verify_guzhou_r052_native` and its
engine) models only `k`-of-`m` threshold atoms, so the weighted-threshold and
winning-subset orbits have no representation there yet and no method-distinct decision
was attempted.

## Retrieval Hashes

Digests of this packet’s copies, which are the source’s bytes unchanged.
The release’s own `MANIFEST.json` lists every release file’s SHA-256, and
`check_integrity.py` checks the tree against it.

| File | SHA-256 |
| --- | --- |
| `bounds/4.66001/certificate.json` | `280af3d46150ca990917d714d83ee73baf4e6c45a0563090bf35588fb22de6e5` |
| `bounds/4.66001/PROOF.md` | `33b82dfd4482ebcc2ecacfa0a617e54c4ac1ddef7a071091417cd654f950f984` |
| `bounds/4.66001/METHOD.md` | `acc0e6870e720b056e7b31cd13cae590eef97a67d1d0054d18c21017f2c4ad04` |
| `bounds/4.66001/verify.py` | `2885bb142a31c461084269a2111235140a0628d746d437e572817554665f331a` |
| `bounds/4.66001/verify_global_python.py` | `c4ace7ff58bdc6593cf6ec3179f2914aa81e0f0f2a16db1332915a45dcb0a219` |
| `bounds/4.66001/verify_global_variable.js` | `c22091862df631f8cfd1f1bb8e5013f0b9c216f20be268fcd7104768919c49b7` |
| `bounds/4.66001/controls.py` | `b8ffcc69bbe97815f1bf8b20f289825651a9090442a6fc275eab6e1bb4498afa` |
| `README.md` | `46483929263683e5f135fc942f5b0e4dcc08b8d5d1a93cb79d15cd7c1a59b4d4` |
| `CURRENT_BOUND.json` | `f5b1310dfa9aa2afbbd20cbcc894a37fa29db1fbc51ce51701caab6fcc3727f1` |
| `AUTHORS.md` | `f762d47d1b3d06c02d06e2b4c4743584993e35c31f9f1dfd25b653a997eaa617` |
| `ATTRIBUTION.md` | `b6f041d5ec47d076a9d1a629e203957c1f48a1f9b957afd96331474d183732bb` |
| `LICENSING.md` | `4b16777736049d84fda497b8524d41bfdf38705353b5da77b7966e13c481079a` |
| `MANIFEST.json` | `c671346cefe181803f6b575ae4b50ded0b6f367d27a163e52b96fbad94087716` |

The two checkers and the three `global_src/` modules match the digests in the
release’s `evidence/theorem-identities.json` and the `v1.1.0` packet’s copies.

## Compressed Files

Nine data files of more than 1,000 lines: seven of the release’s ledgers under
`bounds/4.66001/evidence/`, and this packet’s controls receipt and its console log,
which equal the source’s `publication-controls.json` apart from its timestamp.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for a receipt are the
bytes this repository wrote.
The repository’s readers take the upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` (run by
`packing/tests/test_retained_data.py`) re-derives every row.
The release’s `MANIFEST.json` and `check_integrity.py` expect the plain files.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/n17-kleddamag-466001-2026-09-27 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies
are present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/coordinator-replay/node-0.json.gz` | upstream | `2d7cb2bf247f3c93395918e79ca5e4de6b12ad74` | `c2eb8eda4e377d48119441b27ec1034b995fae26b8298b8cd763052940315a02` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/coordinator-replay/node-1.json.gz` | upstream | `6e2fbc1664db9f9e8438c029936446ecbae5e919` | `83169e119fd1603cada5f91c72e0b8d1574550e51a51923ca7dcee4ebd486787` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/coordinator-replay/node-2.json.gz` | upstream | `03f8f7652ae816cd2feef8387a9fdb0706b5b22b` | `34a9b2645391cdcccce8989b6ae0a8f8a88342f074921a418327ff95889bea38` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/publication-controls.json.gz` | upstream | `1c2fbda6fe8a817ce81fc971b0c852f50447d385` | `3a4b12e06e181c64c5d3f2056585924aadda7a4c8ddbba206ea50215a5699b37` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/publication/node-0.json.gz` | upstream | `0bdd12d1189bbbf51d521f5d1973a01983964020` | `da011ed19f147bf970349aaf91d132b983918eff34b1649dad959e530bfd2dfe` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/publication/node-1.json.gz` | upstream | `afd38485d7aa40c134b5cb894541999ec5d56cd5` | `aead74039daa3baf685ed9e125e0a409425ce5beab3997c89fbd5584eb0c7543` |
| `kleddamag-17-squares-certified-bound/bounds/4.66001/evidence/publication/node-2.json.gz` | upstream | `697c70dc4aa1a7f962d8d87d29577fe149c1abb0` | `2d5fea0cc2aa3cd78342842dd4b14464800e8980102198df406baa774d3f35fb` |
| `receipts/controls/console.log.gz` | receipt | `42ab5d25b1411fd986e67c8d11aefdc9583139ee` | `8b63fc8711adfe10034bfa48f378acdd94782e10c30af4c24b1e570b5d9a1da2` |
| `receipts/controls/controls.json.gz` | receipt | `42ab5d25b1411fd986e67c8d11aefdc9583139ee` | `8b63fc8711adfe10034bfa48f378acdd94782e10c30af4c24b1e570b5d9a1da2` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
