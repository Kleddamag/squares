# Guzhou0806’s R070 and R071 Lower Bounds for `s(17)`, Retrieved 2026-10-05

Two third-party exact computer-assisted lower bounds on `s(17)`, the least side of a
square holding seventeen unit squares with disjoint interiors, published after R068.
Both keep R068’s charge unchanged and rebuild its strict cores for a smaller parent:
R070 claims `46604427/10000000 = 4.6604427` over 5,107 angle intervals, and R071 claims
`18641771/4000000 = 4.66044275` over 5,114.
R071 is the strongest public claim for this case the record has seen, `11/4000000`
above R068’s `116511/25000`.
R071 was replayed here in full on 5 October 2026 and passed
([Stage 4 Replay of R071](#stage-4-replay-of-r071)); R070 was not replayed.

This packet holds the source bytes, the source’s CI metadata, a pre-replay audit of both
certificates against R068’s, and the receipts of R071’s replay and its two controls.
Retaining it registers no result and moves no bound; the register entry (`T-093`), the
[stage 4 review](../../../../docs/project/reviews/review-2026-10-05-guzhou-r071.md) and
the case record are separate records.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Guzhou0806/n17-square-packing> |
| R070 commit | `8988d933e10fe89709a01d98b602396c29dd7bd1`, committed 2026-09-29T07:56:05Z (15:56 in the author’s `+08:00`) |
| R071 commit | `8c11f6962506940c5de67a9fa73b3d1e2e151196`, tree `bf552164d6eb3c99a46f6508cc83fdabc3c99106`, committed 2026-09-30T22:53:43Z (06:53 on 1 October, `+08:00`); `main` at retrieval, and the pin |
| Retrieved | 2026-10-05T03:11Z, a blobless clone |
| Previous retained pin | `815b1626`, R068, in the [R068 packet](../n17-guzhou-r068-2026-09-28/README.md) |
| R070 package | `certificates/R070-4.6604427/`, 50 files; `MANIFEST.json` `cbcbcd1a…b198` |
| R070 certificate | `project/followup_c016/results/target_4.6604427/certificate.json`, SHA-256 `8438cae4da93c98a92b0b96560f95d9da8d0ef47287783f3b18a9cb8208167b9` |
| R071 package | `certificates/R071-C029/`, 123 files; `MANIFEST.json` `ec8c77bc…6459` |
| R071 certificate | `bounds/c027/certificate.json`, SHA-256 `15b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469` |
| Acquisition | [`acquisition/`](acquisition/), written by `devtools.acquire_source` from the declaration there |
| Upstream CI | Both workflows passed on their commits; observed here through the GitHub API, [below](#upstream-ci) |

Each certificate digest is the one its package’s `MANIFEST.json`, its publication record
and its run records state.

**Credit, as the source states it.** R070’s `ATTRIBUTION.md` says the original 4.66001
construction, proof and independent JavaScript checker come from Kleddamag’s pinned
commit `57519bb7`, that the C007 to C015 compensation charge and research tools are
inputs, and that C016 constructed the 4.6604427 certificate “through AI-assisted work in
the Guzhou/N17 project”. R071’s says the improvements to 4.6604427 and the retained
4.66044275 “belong to AI-assisted research in the Guzhou0806/N17 project; they are not
new results of Kleddamag”, that the 4.66001 framework, proof and JavaScript checker are
Kleddamag’s, and that “Nagamochi’s measure, chelokot’s repair/compensation proof and
Lean work, and other upstream algorithms retain their original attribution”. Both
retain the historical notices for Mira, Guzhou0806’s R038 and Joshua Levy’s squares
project under `project/base/upstream/notices/`, the same twelve files R068 retained.
Neither claims a world record, priority, optimality, human peer review or a
proof-assistant formalization.

Both packages say their publisher checked file identities and saved records only, ran
no fresh geometry, and did not observe CI (`PUBLICATION_STATUS.json`).
R071 adds that the old C027 partition records “remain missing”, that 276 historical C020
files are missing, and that an external sealed-archive replay audit its documents cite
was not received.

## The Claims

$$
s(17) > \frac{46604427}{10000000} = 4.6604427 \quad\text{(R070)},\qquad
s(17) > \frac{18641771}{4000000} = 4.66044275 \quad\text{(R071)}
$$

The container side stays `L = 4613/1000`; the parent sides are
`A = 46130000/46604427` and `A = 18452000/18641771`, so each bound is `L/A`.

| Quantity | R068 | R070 | R071 |
| --- | ---: | ---: | ---: |
| Target | `116511/25000` | `46604427/10000000` | `18641771/4000000` |
| Advance over R068 | — | `27/10000000` | `11/4000000` |
| Site orbits / physical sites | 2,621 / 20,860 | the same | the same |
| Rule orbits | 889 | the same | the same |
| Budget `M` | 17000448944 | the same | the same |
| Requested minimum | 1000026409 | the same | the same |
| Reported minimum core charge `Γ` | 1000026844 | 1000026844 | 1000026844 |
| `17Γ − M` | 7404 | 7404 | 7404 |
| Angle intervals | 4,991 | 5,107 | 5,114 |
| Row-level records published | 2 + 2 partitions | 4 + 4 partitions | none |
| Replayed here | 2026-09-28 | no | 2026-10-05 |

Every proof step is R068’s with the new `A`: the same charge, the same budget rules, the
same contradiction `17Γ − M = 7404 > 0` and the same compactness step for the strict
inequality (`PROOF.md` and `BOUND_PROOF.md`).
R071’s advance over R070 is `1/20000000`.

## How They Differ From R068

[`packing/devtools/audit_guzhou_r071.py`](../../../devtools/audit_guzhou_r071.py)
`structure` reads each certificate beside R068’s; the outputs are
[`receipts/r070/structure.json`](receipts/r070/structure.json) and
[`receipts/r071/structure.json`](receipts/r071/structure.json), and
[`packing/tests/test_guzhou_r071_packet.py`](../../../tests/test_guzhou_r071_packet.py)
re-derives them.

- **The charge is R068’s.** `L`, both denominators, the budget, the requested minimum,
  all 2,621 point orbits and all 889 rule orbits equal R068’s as JSON. The bound moves
  only through `A` and the cores.
- **R070** keeps every R068 endpoint: 4,888 intervals are kept, 101 are bisected
  exactly, and one is cut into 5 and one into 12, giving 5,107. Each kept interval keeps
  its core’s angle and gets a new core side.
- **R071** is built on R070: its certificate names R070’s digest as `base_sha256`. It
  keeps all of R070’s endpoints and bisects seven intervals exactly, giving 5,114; again
  every shared interval keeps its core’s angle and no core is unchanged.
  The certificate’s own `source` string says “All 5111 core intervals rebuilt”, three
  fewer than it holds.

## The Other Results, None a Bound

**R070’s `GEOMETRIC_RESULTS.md`** gives two results the source says establish no higher
global bound. A same-budget overlay upgrades 319 orbits and 2,552 images to rules whose
winning sets have pairwise intersecting convex hulls, with budget one each; the source
checks it charges at least as much as the original everywhere and inherits the
4.6604427 conclusion without a separate sweep. And at one exact legal parent at
`T = 186417711/40000000`, every one of the 6,574 non-firing images is separated from the
parent, so within the stated class of fixed-weight enhancements that parent’s charge,
`999880603`, cannot rise: the source says this blocks a uniform per-parent proof in that
class and nothing wider, and is not an upper bound on `s(17)`.

**R071’s `GEOMETRY_PROOF.md`** is conditional joint geometry. At `T = 9321/2000 =
4.6605` and inside one specified first-anchor box, it covers the point-avoiding parents
by 18 components, finds 17 conflict edges and 2 forced holes, and bounds the number of
avoiding parents by `9 ≤ Vmax ≤ 11`; eight component pairs remain unknown. The source
says in its README that this “does not prove s(17)>4.6605”. Its machine checks are the
C028 and C029 paired C++ and BigInt programs that `run_public.js geometry` replays.

These are recorded here as research material, as R068’s C010 was. None carries a bound
in this record, and their programs and data are pinned by digest rather than retained
([below](#what-is-retained-and-what-is-not)).

## Upstream CI

The source delegated its replays to GitHub Actions and did not observe them.
[`receipts/ci/r070-actions-run.json`](receipts/ci/r070-actions-run.json) and
[`receipts/ci/r071-actions-run.json`](receipts/ci/r071-actions-run.json) are the API’s
records of the two runs, retrieved at 2026-10-05T03:18:10Z:

| Workflow | Run | Commit | Job | Started | Wall | Conclusion | Artifact |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| R070 final exact replay | 36539632653 | `8988d933` | `global` | 2026-09-29T07:56:27Z | 21 min 8 s | success | `r070-global`, 77,412 bytes |
| R070 final exact replay | 36539632653 | `8988d933` | `geometry` | 2026-09-29T07:56:27Z | 44 s | success | `r070-geometry`, 159,985 bytes |
| R071 exact replay | 36788162356 | `8c11f696` | `replay (bound)` | 2026-09-30T22:53:56Z | 16 min 43 s | success | `r071-bound`, 212,890 bytes |
| R071 exact replay | 36788162356 | `8c11f696` | `replay (geometry)` | 2026-09-30T22:53:57Z | 3 min 17 s | success | `r071-geometry`, 3,288,383 bytes |

Each job’s steps all report success, and each artifact’s SHA-256 is in the receipts.
The `bound` job runs `run_public.js bound`, which compiles the C++ checker, runs it and
Kleddamag’s BigInt checker over all 5,114 intervals in two partitions, and fails unless
`THEOREM.json` gives `PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION`, target
`18641771/4000000`, minimum `1000026844`, budget `17000448944`, surplus `7404` and the
certificate digest above.
The artifacts expire on 28 and 29 December 2026.
The artifact and job-log downloads redirect to an Azure blob host this session’s egress
refuses (HTTP 403), so the fresh partition records the `r071-bound` artifact holds, the
source’s only row-level record of R071, are not retained here; the replay here
regenerated both ledgers ([below](#stage-4-replay-of-r071)).
A passing CI run is the source’s own replay on the source’s own runner, not a replay
here.

## Pre-Replay Audit

Two checks read only the retained bytes and decide nothing about the geometry.

**R070’s published ledgers agree row by row**
([`receipts/r070/published-ledgers.json`](receipts/r070/published-ledgers.json)). The
four C++ and four BigInt partitions cover all 5,107 intervals contiguously, each names
the certificate digest and the interval total, and the two reduced ledgers are identical:
every row has minimum `1000026844`, the cells sum to 2,260,759,562,719, and the surplus
is `7404`. The C++ header gives 20,860 sites and 49,208 signed terms, as R068’s did, and
a least strict core margin just above `10⁻¹²`. The published `THEOREM.json` agrees with
all of it and with `INPUTS.json`; the source’s run took 868.951 s at four partitions.

**R071’s completion summary is consistent with its certificate**
([`receipts/r071/summary.json`](receipts/r071/summary.json)).
`history/c027/C027_GLOBAL_THEOREM.json` names the certificate’s digest, 5,114 intervals,
the certificate’s budget and a minimum of `1000026844` with surplus `7404`, and six
processes, a C++ and a BigInt checker on each of three partitions, all exiting 0 in
1,694.142 s. The checker and launcher digests it gives are those of R068’s
`verify_global_variable.js` and `replay.js` as the R068 packet retains them, and its
executable digest is the one R068’s and R070’s own runs record.
It is a summary: the rows behind it are the missing C027 partitions.

## Stage 4 Replay of R071

R071 was replayed here on 5 October 2026 by its own launcher, from 04:53:42Z to
05:51:40Z, with [`devtools.replay_guzhou_r071`](../../../devtools/replay_guzhou_r071.py)
staging the package and keeping the receipts in [`receipts/r071/`](receipts/r071/).

- **Staging.** `stage` writes the 123 files of `certificates/R071-C029/`, refusing any
  whose SHA-256 is not the subtree manifest’s: the retained ones from this packet and
  the sixteen pinned `upstream/` files from the R068 packet. The run staged the research
  files from this packet, which then retained them; since the packet pins them, `stage
  --checkout` takes them from a clone at `8c11f696`, and that staging is byte-identical
  to the one the run used.
- **The package check.** `node check_package.js`: `PASS_BYTES_ONLY`
  ([`check_package.log`](receipts/r071/check_package.log)).
- **The replay.** `N17_TIMEOUT_MINUTES=600 taskset -c 2,3 node run_public.js bound`
  ([`bound.log`](receipts/r071/bound.log)) built `verify.cpp` with g++ 13.3.0 at `-O3
  -std=c++17` against the Boost 1.83 headers, giving executable `cf761bb5…19d5`, the
  bytes R068’s replay here built from the same source, and ran it beside Kleddamag’s
  BigInt checker under `replay.js` at two partitions with Node v22.22.0, on a shared
  four-core host at load 5 to 21. The C++ partitions took 1,577 s and 1,693 s and the
  BigInt ones 3,409 s and 3,464 s; the whole took 3,478 s of wall and 3,238 CPU-seconds,
  about a fifth less than the 4,200 the import priced. `run_public.js` wrote
  [`REPLAY.json`](receipts/r071/replay/REPLAY.json) `PASS_R071_C027_GLOBAL_REPLAY`, and
  `replay.js` wrote [`THEOREM.json`](receipts/r071/replay/THEOREM.json)
  `PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION` with target `18641771/4000000`, 5,114
  intervals, budget `17000448944`, minimum `1000026844`, surplus `7404` and the
  certificate’s digest.
- **The rows.** `audit_guzhou_r071 compare R071 FRESH --published FRESH`
  ([`compare.json`](receipts/r071/compare.json)) finds the two C++ and two BigInt
  partitions identical, 0 of 4 × 5,114 rows differing: every row at minimum
  `1000026844`, 2,263,809,819,494 cells in all, 20,860 sites and 49,208 signed terms,
  least strict core margin just above `10⁻¹²` at row 2647, reduced triples SHA-256
  `6c9d7202…bfe3`. The source retains no row of R071, so this compares the two fresh
  ledgers with each other. The stage 4 review’s own sweep of 227 rows, written before
  this replay and sharing no code with the source, equals them at every one of those
  rows, minimum and cell count, and its least core margin is the C++ header’s.
- **The controls** ([`receipts/r071/controls/`](receipts/r071/controls/)). `control`
  feeds two mutated copies of the certificate to the built C++ checker and the BigInt
  checker. The over-claim keeps every core and shrinks the parent to target
  `9321/2000`: both refuse it before any sweep, as a non-strict core. The drop-rule
  zeroes the heaviest rule orbit’s weight and takes its 198,960,224 units off the
  budget, which still passes the counting check: both refuse it by the sweep at interval
  0, minimum 950,286,788 against the requested 1,000,026,409.
  `tests/test_guzhou_r071_packet.py` holds both refusals, the replay’s values and the
  row agreement.

The partition records are stored as deterministic gzip
([Compressed Files](#compressed-files)). In the logs and `REPLAY.json` the scratch
directory is written `WORK`; the partition records, `THEOREM.json` and `INPUTS.json`
name no path and are byte for byte as written.
The run measured here replaces the import’s estimate, which scaled R068’s measured
4,093 CPU-seconds by R070’s published cells. R070 needs no replay of its own; its
published ledgers already agree row by row, and its geometry, like R071’s, decides no
bound.

## What Is Retained, and What Is Not

The packet retains what the R071 bound, its replay and the audit read, and the
documents that state the claims and their credit; it pins the rest by digest
([`OR-18`](../../../../operating-rules.md): bulk data out of Git, retain what the claim
needs). `acquisition/upstream-subtree.sha256` lists all 186 files the two commits
changed or added since `815b1626`, retained or not, and `acquire_source --check`
re-derives the packet from it.

**Retained byte-identical**, 45 files under `n17-square-packing/`, at their upstream
paths, each Git blob equal to the commit’s:

- R071’s C027 certificate, its completion summary `history/c027/C027_GLOBAL_THEOREM.json`,
  the launcher `run_public.js` and `check_package.js`, and the package’s documents:
  `README.md`, `BOUND_PROOF.md`, `GEOMETRY_PROOF.md`, `ATTRIBUTION.md`,
  `PUBLICATION_STATUS.json`, `REPRODUCIBILITY.md`, `MANIFEST.json` and `SOURCE_MAP.json`.
- R070’s certificate and its published four-partition C++ and BigInt ledgers with their
  `THEOREM.json` and `INPUTS.json` under `project/followup_c016/results/target_4.6604427/`,
  which the audit reads, and the package’s documents, `check_package.js` and
  `assert_results.js`.
- `R070_PUBLICATION.json`, `R071_PUBLICATION.json`, the workflows
  `.github/workflows/r070.yml` and `r071.yml`, and the nine root files R071 last edited:
  `CHANGELOG.md`, `CITATION.cff`, `NOTICE.md`, `README.md`, `RESULTS.md`,
  `docs/EVIDENCE_MAP.md`, `docs/RELEASE_NOTES.md`, `docs/REPRODUCIBILITY.md` and
  `scripts/check_release_hashes.py`.

Nine large data files, R070’s certificate and its eight ledgers, are stored as
deterministic gzip ([Compressed Files](#compressed-files)).

**Pinned by digest only**, 141 files, each listed with its size, SHA-256 and reason in
`acquisition/sources.json`:

- The 32 files under each package’s `project/base/upstream/`: the C++ checker
  `verify.cpp`, its kernel `native_geometry.hpp`, the launcher `replay.js`, Kleddamag’s
  BigInt checker `reference/verify_global_variable.js` and the twelve notices, the same
  sixteen in both packages. Each is byte-identical to the copy the R068 packet retains
  under `certificates/R068-C010/upstream/`, which `acquisition/sources.json` names and
  `--check` compares. They are the code R068’s replay here ran, and R071’s.
- 95 files of R071’s research, 2.2 MB: the C028 and C029 conditional joint-geometry
  programs, data trees and frozen outputs under `project/followup_c028/` and
  `project/followup_c029/`, and the C021 and C026 inputs they reuse. They claim no
  bound ([above](#the-other-results-none-a-bound)), and neither the C027 bound, its
  paired replay nor the audit reads them. The 20 `.tree` files among them were 136,452
  of the packet’s 146,029 lines when it was first retained on 2026-10-05; stage 4 of
  the import pinned them on the owner’s request the same day.
- 14 files of R070’s research, 3.8 MB: the C015 model and pose, the same-budget overlay,
  the overlay and obstruction programs and outputs (among them a 1.98 MB one-line
  obstruction record), and a research library. None carries a bound or is read by
  either bound, the replay or the audit.

Every retained file is described by a digest the source published: all 133 entries of
`R071_PUBLICATION.json` match the pinned bytes, and 51 of the 60 in
`R070_PUBLICATION.json`; the other nine are the root files above, which that record
describes as they stood at `8988d933`, versions not retained here. Every entry of both
packages’ `MANIFEST.json` matches too, the pinned-only files through their digests.
The source’s `check_package.js`, which `run_public.js` calls first, reads every file of
its package, so restoring either package for it needs the research files from the
source at `8c11f696` and the `upstream/` files from the R068 packet;
[`devtools.replay_guzhou_r071`](../../../devtools/replay_guzhou_r071.py) `stage` does
both and refuses any byte whose digest is not the manifest’s. The bound itself reads
only the certificate and the four checker files.

**Not retained:** the rest of the upstream repository, unchanged since `815b1626` and
covered by the earlier Guzhou packets; `.git/`; and the CI artifacts and logs, which
could not be fetched.

**Licensing.** The upstream repository has no repository-wide licence. Both packages say
that repackaging does not expand third-party licences and that attribution is not
endorsement; the inherited notices keep their own scopes, Kleddamag’s MIT `LICENSE`
among them. This packet is retained for verification and research use on the same basis
as the earlier Guzhou retentions.

## Compressed Files

Each is stored as deterministic gzip made by `gzip -9n`, by `devtools.acquire_source`;
the table gives the Git blob and SHA-256 of the decompressed bytes, which are the
upstream blob and digest at `8c11f696`. The repository’s readers take the upstream path
and decompress transparently through `devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row. The source’s own
`check_package.js` and launchers expect plain files; restore them from the repository
root with

```sh
find packing/resources/web/n17-guzhou-r071-2026-09-30 -name '*.gz' -exec gunzip -k {} +
```

and remove the restored copies afterwards.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/certificate.json.gz` | upstream | `c2811e355363ef0229280f4c6e38be8824a8d9f0` | `8438cae4da93c98a92b0b96560f95d9da8d0ef47287783f3b18a9cb8208167b9` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/cpp-0.json.gz` | upstream | `6759c5d54de14893f66524ae98d566ec453f1e44` | `2e5374306e7316737f8312413799beae8bd1a9977f91fa09f9e3df65c2ff574c` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/cpp-1.json.gz` | upstream | `879f1a78eec847a3e37adea76ede41de1bea261d` | `a7e65d506c8c4dfcb2c0d374c9904ab3c5d3e0a07032f0a6d70049b6c1cb55bd` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/cpp-2.json.gz` | upstream | `b40e69a230525a99d8aaf181a8926913492fcaa5` | `cd1f24776fe27f34e5709aa762504e30d3d3e3bd80f27dbf7d1b2b82eadeae6d` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/cpp-3.json.gz` | upstream | `9ba117de3855480d139fd3b4b3ad1e17e2662ae8` | `faacc4749997025a80dce69392f3980eae30800af79f19c3b60ce3f52605f591` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/node-0.json.gz` | upstream | `8c22e56c92db3fa73e3a0a43f5216c3b49c29961` | `bdb68887a27cc5263270346bc1187d070b4753153cdc9a4915122eea301bc6f4` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/node-1.json.gz` | upstream | `c523f75bb8296d95cab3a6ecd4e91f8003173bf1` | `7f0fd09fa687e7c9061e07c397e989f3bace317d73cfd5e3e7dca6c753aed9c6` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/node-2.json.gz` | upstream | `5091ff6147f924fb223c98a513a375b176ba0fca` | `da743ccf691f9980ab1184e40100cf7cace597378b7bea3d11e3b6c8714a8e90` |
| `n17-square-packing/certificates/R070-4.6604427/project/followup_c016/results/target_4.6604427/paired_replay/node-3.json.gz` | upstream | `f9e497c461b959ee98c44f4169076e599f791da3` | `72a6da299375ac89873948124ea278cb0b6dd939361165bd9b3afbb818b6df9f` |
| `receipts/r071/replay/cpp-0.json.gz` | receipt | `27609e7cf774afeeb5c26cb5e4a024a8768df15a` | `0d1d6d6281e6c6990c980469096fdcb4f98935f74af602a43fd99111e96333dd` |
| `receipts/r071/replay/cpp-1.json.gz` | receipt | `9ca802b96266ac9c7d395491170c4e642e92259a` | `969bd5e3f433038415baac7cceab42b3644b92d01ead0e6aecf7791bc10a57b1` |
| `receipts/r071/replay/node-0.json.gz` | receipt | `a00dc36c11952c48feaed9070ab0d59d8eb8d456` | `d272e71ba8f856987ba8bc30aab6589c9be2b1fe710ea8ad7735d2531459a66d` |
| `receipts/r071/replay/node-1.json.gz` | receipt | `8dc9ac377da4f7b775226286c3a787f909052726` | `d87012f1edaef49cea43971f9b53fd2d2df3f93ccc072f5dbc6e0769bf05f381` |

## Retrieval Hashes

Digests of this packet’s copies of the files a reader checks first; the full list is
`acquisition/upstream-subtree.sha256`.

| File | SHA-256 |
| --- | --- |
| `R070_PUBLICATION.json` | `e464ba2877db7c9d0cb07c5bcb79616479d3f43301136b560e9ef0967f2ecb7e` |
| `R071_PUBLICATION.json` | `8553c5de403428b026c659ded8189c3c064d3b5884b6170cb963fdfc6ba1fb85` |
| `certificates/R070-4.6604427/PROOF.md` | `dcd0fbb0b67386fa9191e6cf12fb04d4760a7103b3cc3c414465154621915ae8` |
| `certificates/R070-4.6604427/GEOMETRIC_RESULTS.md` | `7be65390379aa4747ea7413c57d03f5b6dd2c9aae3acf0646bba8db00f76283b` |
| `certificates/R070-4.6604427/assert_results.js` | `87b296789886fa4988deae0446a0d947e17e845f49db444c11a4bd2f1dc0a9a8` |
| `certificates/R071-C029/BOUND_PROOF.md` | `255e0f5d55e91ef6298763598ab7de966c6b0690a3b880c309dd0569721ab6de` |
| `certificates/R071-C029/GEOMETRY_PROOF.md` | `a5c053ae0f6df314708e7346fc0e639f6725b4355448c9fffa05f4aec2207f16` |
| `certificates/R071-C029/run_public.js` | `45f6ef8e5b5e16b0c32ddc243ae18416b5781de8edc9b4daa11972e76423160f` |
| `certificates/R071-C029/history/c027/C027_GLOBAL_THEOREM.json` | `136040243fd9141a69f7b5590a852ea3dfea9e6e4c03be826f08095dc57c75d9` |
| `README.md` | `a27e77efb955598a2e8784431d9e83b4ae8ee4f227623a77f76528605b281499` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
