# Kleddamag’s `v1.1.0` Lower Bound for `s(17)`, Retrieved 2026-09-27

A third-party release claiming an exact computer-assisted lower bound on `s(17)`, the
least side of a square holding seventeen unit squares with disjoint interiors.
It is retained because it is numerically the strongest public claim for this case that
the record has seen, `0.02` above Guzhou0806’s R052 `231001/50000` then on the frontier,
and because its replay is cheap enough to repeat here: a fixed rational certificate and
two exact sweeps over 2,048 angle intervals.

Since 2026-09-27 it is the previous verified bound, superseded by the same repository’s
[`4.66001` package](../n17-kleddamag-466001-2026-09-27/README.md), which keeps this
release’s two checkers byte for byte.

This packet holds the source bytes and the replay receipts.
The registration is in [`n-017.md`](../../../frontier/n-017.md) and
`E-n017-kleddamag-4640020-source-replay` in
[`evidence.yaml`](../../../frontier/evidence.yaml); the mathematical review is a
separate record, `docs/project/reviews/review-2026-09-27-n17-kleddamag-4640020.md`.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Kleddamag/17-squares-certified-bound> |
| Tag | `v1.1.0`, a lightweight tag on the commit below |
| Commit | `13821ddfa24133a8d796648383464574404d5fa0`, “Publish verified bound s(17) > 4.640020” |
| Tree | `020920b8052e206787f3d5f518d19327d513beb8` |
| Committed | 2026-09-26T08:47:21+02:00 |
| Retrieved | 2026-09-27 |
| Previous release | `v1.0.0` at `a499e2c7`, retained in [`../n17-kleddamag-certified-bound-2026-09-21/`](../n17-kleddamag-certified-bound-2026-09-21/README.md) |
| Certificate | `bounds/4.640020/certificate.json`, SHA-256 `5f4f0988acc23b738bdf29ee855b9827cda10fce0e12a7b3a78e6923cc5f8dda` |
| Release `MANIFEST.json` | `48695b48f72e7a1bc49d50c55d84a716597a0057c61ef8d7eb0e7db97de56627` |

The certificate digest is the one the release’s README, `PROOF.md`, `MANIFEST.json`
and `evidence/theorem-identities.json` all state, and the one both checkers report.

**Credit.** Kleddamag, building on Squares Project (Joshua Levy), Mira and Guzhou0806.
`ATTRIBUTION.md` places the result in the lineage of Mira-acc/17squares, Guzhou0806 /
N17 project’s R038, and this repository’s weighted-covering, strict-core, event-cell
and threshold-budget work, citing the parent-centre contract and the T-025 threshold
certificate, and it claims no invention of those methods and no priority.
It also says that no code from Guzhou0806’s R052 was used.
Kleddamag publishes a handle only. `AUTHORS.md` says Kleddamag initiated and directed
the project and chose to publish, and that the work was produced with AI agents (OpenAI
Codex) under that direction, combining findings from separate research tasks.
It is explicit that “independent” in the release means distinct implementations or
separately written audits, not independent human peer review or a proof assistant.

The release measures its advance against its own `v1.0.0` value `4.619791…`, “closing
36.29%” of that gap to Bidwell’s packing. It does not mention R052’s `4.62002`, which
was public and on this record’s frontier a day earlier. Against R052 the advance is
exactly `1/50`.

## The claim

$$
s(17) > \frac{232001}{50000} = 4.640020
$$

The container side is `L = 4613/1000` and the parent side is `A = 32950/33143`, so the
bound is `L/A`. Weights have denominator `10^9`; the site coordinate denominator is a
104-digit integer.

| Quantity | Exact value |
| --- | ---: |
| Total budget `M` | 16978369232 units |
| Certificate’s requested minimum | 998727602 units |
| Replayed minimum core charge `Γ` | 998727933 units |
| `17Γ − M` | 5629 units |
| Angle intervals | 2,048 |
| Least strict core margin | `10^−11` |

The release makes no claim about the exact minimum and no better packing; its unchanged
`upper-packing-certificate.json` is the Bidwell reconstruction retained with `v1.0.0`.

## Method

The same parent-core argument as `v1.0.0`: a nonnegative `D4`-invariant charge on sites
in `[0, L]²`, a catalogue of rational half-angle intervals each carrying a concentric
closed core strictly inside every parent of that interval, an exact sweep of the legal
centre domain for each interval, and the count `17Γ > M`.
What changes is the charge dictionary. Over `1,116` site orbits (`8,876` sites) there
are `546` positive charge orbits, `4,328` feature images in all:

| Feature | Orbits | Budget per image | Share of `M` |
| --- | ---: | --- | ---: |
| Point capture (one of one) | 280 | 1 | 8646880660 |
| Two of three | 155 | `⌊3/2⌋ = 1` | 3799348860 |
| Three of five | 26 | `⌊5/3⌋ = 1` | 1274273224 |
| Four of seven | 1 | `⌊7/4⌋ = 1` | 54285144 |
| Weighted threshold, coefficients `2, 1, 1, 1`, threshold 3 | 54 | `⌊5/3⌋ = 1` | 1114736304 |
| Winning subsets of seven sites, pairwise intersecting | 30 | 1 | 2088845040 |

The shares sum to `M`, recomputed here from the certificate’s weights and images.
The two new budget rules are the ones the review has to carry: a weighted threshold
firing on disjoint cores consumes each site’s coefficient at most once, so it fires at
most `⌊Σaᵢ/k⌋` times; and when every two listed winning subsets intersect, two disjoint
cores cannot both contain one, so the feature fires at most once.
Each capture rule is expanded by integer Möbius inversion into signed all-subset
captures, which are rectangles in rotated centre coordinates, so the sweep is a signed
integer rectangle sum with a checked absolute bound below `2^50`.

Two checkers run it. `verify_global_python.py` uses arbitrary-precision rational
geometry and a Numba integer sweep; `verify_global_variable.js` recomputes the geometry
in BigInt and sweeps with exact integers. Both are the release’s own general-rule
implementations; unlike `v1.0.0`, neither adapts Guzhou0806’s R038 scanner, so the
replay needs no download and no reconstructed checker. The launcher `verify.py` runs
both concurrently and requires every interval from each, equal minima and cell counts
on every interval, the certificate identity, and the strict count.

## What Is Retained, and What Is Not

**Retained byte-identical** under `kleddamag-17-squares-certified-bound/`, at their
release paths: the 37 files that changed or were added between `v1.0.0` and `v1.1.0`.
That is the whole `bounds/4.640020/` package (28 files: the certificate, proof, method
note, launcher, both checkers and their three shared modules, the controls script, and
the source’s own receipts), the new `README-v1.0.0.md`, and the eight root files the
release edited: `README.md`, `ATTRIBUTION.md`, `AUTHORS.md`, `CHANGELOG.md`,
`LICENSING.md`, `MANIFEST.json`, `PROOF.md` and `VERIFICATION.md`.
Every file’s `git hash-object` equals its blob at `13821ddf`; seven ledgers are
stored as deterministic gzip, and for those the identity holds after decompression
([Compressed Files](#compressed-files)).

**Not duplicated:** the release’s other 74 files, unchanged since `v1.0.0`, among them
`LICENSE`, `NOTICES/`, `global-certificate.json` and the `v1.0.0` checkers. Their blobs
at `13821ddf` equal the copies already retained in the
[`v1.0.0` packet](../n17-kleddamag-certified-bound-2026-09-21/README.md), checked file by
file. Overlaying this packet’s tree on that one reconstitutes the full 111-file release,
and the release’s own `check_integrity.py` passes over it (below).

**Omitted:** `.git/`, and the replay outputs themselves. `receipts/` keeps the launcher’s
`theorem.json`, each checker’s console log, the controls’ `controls.json`, and digests of
the fresh row ledgers with their comparison against the source’s.

**Licensing.** `v1.1.0`’s `LICENSING.md` applies the MIT `LICENSE` to the project’s own
code, documentation and additions, and says the new `bounds/4.640020/` package is the
project’s own general-rule implementation with no source download and no third-party
checker. That is a cleaner position than `v1.0.0`, whose second checker was
reconstructed from R038 source carrying no identified general grant. The upstream
`NOTICES/` keep their own terms and are retained with the `v1.0.0` packet. This packet is
retained for verification and research use; the MIT notice travels with it through
that packet’s `LICENSE`.

## Replay Here

Every command ran on 2026-09-27 in a Linux container with 4 cores, against the
retained bytes before they were compressed (restore them to repeat it), from `kleddamag-17-squares-certified-bound/`, with outputs written
outside this packet. The checkers ran under a separate CPython 3.14.7 environment
holding exactly the release’s pinned `numpy==2.3.5`, `numba==0.67.0` and
`llvmlite==0.49.0`, with Node `v22.22.2`; the release tested CPython 3.12.14 and Node
`v25.6.1`. [`receipts/replays.json`](receipts/replays.json) records each command,
interpreter, start, wall and exit.

```sh
python -X utf8 -B bounds/4.640020/verify.py --output-directory OUT/full --workers 2
python -X utf8 -B bounds/4.640020/controls.py --output-directory OUT/controls
```

| Run | Wall | Exit | Status | What it establishes |
| --- | ---: | ---: | --- | --- |
| full | 2,204.37 s | 0 | `PASS_COMPLETE_SEVENTEEN_SQUARE_EXCLUSION` | Both complete checkers over all 2,048 intervals: minimum `998727933`, budget `16978369232`, surplus `5629` |
| controls | 21.74 s | 0 | `PASS_RULE_BUDGET_SWEEP_AND_NEGATIVE_CONTROLS` | Every capture pattern of the 29 distinct rules, their disjoint-winner budgets, direct against segment-tree sweeps with Node agreement at intervals 0, 511, 1024 and 2047, and eight corrupted certificates rejected by both checkers |
| integrity | under 1 s | 0 | `PASS: 110 release files match their SHA-256 manifest.` | The `v1.0.0` packet’s tree overlaid with this one is the release, file for file |

Inside the full run the Python checker took 2,184 s on two workers and the two Node
processes 2,189 s and 2,204 s on half the intervals each; the release’s own publication
replay, one worker per checker on an Apple-silicon Mac, took 431 s and 313 s.

The launcher checks everything it prints: both checkers cover every interval, their
minima and cell counts agree interval by interval, both report the certificate digest,
and `17 × 998727933 = 16978374861 > 16978369232`. Beyond that, the fresh ledgers reduced
to `(interval, minimum, cells)` are identical to the source’s three published pairs of
ledgers — the original audit, the coordinator’s repeat and the publication replay — all
hashing to `aa526d8a…314b`. The minimum falls only on interval 1207, and the sweeps
visit `263,623,242,504` centre cells in all. The fresh `controls.json` equals the
source’s `publication-controls.json` apart from its timestamp.

What these replays do **not** establish is independence of method.
Both checkers decide the same exact event-cell sweep of the same certificate, written by
the same project. This repository’s native parent-core route
(`devtools.verify_guzhou_r052_native` and its engine) models only `k`-of-`m` threshold
atoms, so the weighted-threshold and winning-subset orbits have no representation there
yet and no method-distinct decision was attempted.

## Retrieval Hashes

Digests of this packet’s copies, which are the source’s bytes unchanged.
The release’s own `MANIFEST.json` lists every release file’s SHA-256, and
`check_integrity.py` checks the tree against it.

| File | SHA-256 |
| --- | --- |
| `bounds/4.640020/certificate.json` | `5f4f0988acc23b738bdf29ee855b9827cda10fce0e12a7b3a78e6923cc5f8dda` |
| `bounds/4.640020/PROOF.md` | `ec73f004ed980b8f58c535b855ee811fa818d308c1fcf377d77e403d9eb82e9d` |
| `bounds/4.640020/METHOD.md` | `3bc668a3ab8b3018dce9ac495402589cfba3445ff55dbc37178932d0026eff2e` |
| `bounds/4.640020/verify.py` | `6a027666c393033aac632b33419b182ef16677878fd1a6e3fd390d1603066258` |
| `bounds/4.640020/verify_global_python.py` | `c4ace7ff58bdc6593cf6ec3179f2914aa81e0f0f2a16db1332915a45dcb0a219` |
| `bounds/4.640020/verify_global_variable.js` | `c22091862df631f8cfd1f1bb8e5013f0b9c216f20be268fcd7104768919c49b7` |
| `bounds/4.640020/controls.py` | `4dd9bfc84faaa3718323d302d6d72c1f3a1801aaf9c5800f1dea5ad3bca08d5f` |
| `README.md` | `b3a133e6377934132adb5c58adad34cb2a272adf606f3e60b6f011ea3ad7936f` |
| `AUTHORS.md` | `477bb74f679119ac551173d8481653633affff18c474f61e934b5b0551794184` |
| `ATTRIBUTION.md` | `78d83a0337a207cb24ad82f7a40a92b3b76d552669d8e18abdac63cab3576d33` |
| `LICENSING.md` | `d148751df996d0b4cb3ecdf67a270d7b5ba43dcaebc4b68373b53fe57c31d22d` |
| `MANIFEST.json` | `48695b48f72e7a1bc49d50c55d84a716597a0057c61ef8d7eb0e7db97de56627` |

The three checker files and the three `global_src/` modules also match the digests in
the release’s `evidence/theorem-identities.json`, which records them as the bytes of
the original complete replay.

## Compressed Files

Seven of the release’s ledgers under `bounds/4.640020/evidence/`, each over 1,000
lines.
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
find packing/resources/web/n17-kleddamag-4640020-2026-09-26 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies
are present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/publication/node-0.json.gz` | upstream | `d2ccf8526de2549aee148dd6588856b11160145f` | `94e054cd752d050be82280db318969b30a2b93178eac8a698715c172f359973b` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-fresh-node-0.json.gz` | upstream | `23ed771593992cc02d41470f8eb3d5f853a67dd4` | `56b475d96bd8b7bde0a58e37d1a56cea6df1860384de58f49af9a09b5412c838` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-fresh-node-1.json.gz` | upstream | `5057ed55ab31c2089ddccb2e2c27baadf2b29ae5` | `20d2038eae22e4c83a77a3aebf6438777cf8c8617a9752d88231139493ace85b` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-fresh-node-2.json.gz` | upstream | `515f710322ca98389d6500cd8a96ad48eeb16937` | `bf99d3df3038af90bcdec8fdf8e281da63d34d362974e697ac81d3a6dae6bfe3` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-global-js-0.json.gz` | upstream | `3c9b4062eaa4e44f79fb4ca64161e3fb1186a7ed` | `1be1c8d4e1ccb3e2cb61428c50d5c56c0ad975b3823da077f13409d7f39d5a41` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-global-js-1.json.gz` | upstream | `b235b21dd4622345959b3a5bce43dd8f3a9b90b4` | `d8c66192b454b97a64bf11afb3030e5193af858934995964e4c842e7e4d8534f` |
| `kleddamag-17-squares-certified-bound/bounds/4.640020/evidence/r464002-global-js-2.json.gz` | upstream | `70c1e8ac7d3c3e74b2a2556026d1449641221f27` | `0d2e77f8e75bc89bbaaa82c66bbaaa2e313730014e9c7757e1bf742abb562f93` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
