# Guzhou0806’s R067 and R068 Lower Bounds for `s(17)`, Retrieved 2026-09-28

Two third-party exact computer-assisted lower bounds on `s(17)`, the least side of a
square holding seventeen unit squares with disjoint interiors.
Both continue Kleddamag’s public `466001/100000` charge, retained in the
[4.66001 packet](../n17-kleddamag-466001-2026-09-27/README.md): R067 rebuilds its strict
cores over 2,808 angle intervals and claims `233009/50000 = 4.66018`; R068 moves one
zero-weight site orbit, adds one weighted four-site orbit, rebuilds the cores over 4,991
intervals and claims `116511/25000 = 4.66044`, the strongest public claim for this case
the record has seen.
R068’s publisher ran no local validation of it and did not observe its CI, so the full
replay below is the first independent one.

This packet holds the source bytes, the replay receipts and a structural comparison with
the 4.66001 certificate.
Retaining it registers no result and moves no bound; registration and review are
separate records.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Guzhou0806/n17-square-packing> |
| R067 commit | `d4e2c287408b416683f7d1b7f19e69fb7c592d73`, tree `79c376767db4e9c9e397b2986d9abac36a55c96f`, committed 2026-09-28T07:53:00Z (15:53 in the author’s `+08:00`) |
| R068 commit | `815b16261f852e389968513eec94b4b9e5b3206d`, tree `2f71d01b259c294fee553636121b28d8d0b8d02c`, committed 2026-09-28T12:44:22Z (20:44 `+08:00`); `main` at retrieval |
| Retrieved | 2026-09-28 |
| Previous retained pin | `6f64e4b2`, in the [R052 continuation packet](../n17-guzhou-r052-continuation-2026-09-26/README.md) |
| R067 package | `certificates/R067-4.66018/`, 36 files; `MANIFEST.json` `c2c1b20c…424c` |
| R067 certificate | `certificate.json`, SHA-256 `101dd164906c7b71dc1397eaa32e25626548cd71995e532113823f434f8e5d26` |
| R068 package | `certificates/R068-C010/`, 44 files; `MANIFEST.json` `0f85f709…a666` |
| R068 certificate | `accepted/4.66044/certificate.json`, SHA-256 `cf70f74ddb47071b1d7333d8a43885d2915f43d45f26f6084a106dfdb0c5205f` |
| Baseline | Kleddamag’s `bounds/4.66001/certificate.json` at `57519bb7`, SHA-256 `280af3d4…e6e5`, which both packages pin |
| Upstream CI | Not observed here: the GitHub API for this repository is not reachable from this session. R068’s own `PUBLICATION_STATUS.json` records `actions_status_observed: false` |

Each certificate digest is the one its package’s `MANIFEST.json`, its publication record
and its source records state, and the one both checkers reported here.

**Credit, as the source states it.** R067 is “Guzhou0806 / N17 project with AI
assistance”: it keeps Kleddamag’s 4.66001 sites, rules, integer weights and budget,
rebuilds the strict cores and angle catalogue, and says the charge and baseline remain
Kleddamag’s. R068 attributes its geometry compensation and the 4.66044 endpoint to the
same project’s AI-assisted research stages C007 to C009, and describes C010 as carrying
that proof and adding local continuous tools and a counterexample, “without claiming
inherited results as new discoveries”.
Both say the original charge, proof and independent JavaScript checker come from
Kleddamag’s pinned repository; the C++ checker’s front end implements Kleddamag’s
general validation logic and its arbitrary-precision sweep derives from Guzhou’s earlier
native engine. The C++ checker is Guzhou0806’s own code
([below](#what-is-retained-and-what-is-not)). Neither claims a world record, optimality,
human peer review or a proof-assistant formalization.
R067’s acceptance upstream was a non-proposer AI review that reused the complete
supplied ledgers and recomputed four intervals; R068’s `README.md` and
`PUBLICATION_STATUS.json` say this publication ran no local scientific validation and no
non-proposer review.

## The claims

$$
s(17) > \frac{233009}{50000} = 4.66018 \quad\text{(R067)},\qquad
s(17) > \frac{116511}{25000} = 4.66044 \quad\text{(R068)}
$$

The container side stays `L = 4613/1000`; the parent sides are `A = 32950/33287` and
`A = 115325/116511`, so each bound is `L/A`. Weights have denominator `10⁹` and site
coordinates `10¹⁰`, as in 4.66001.

| Quantity | 4.66001 | R067 | R068 |
| --- | ---: | ---: | ---: |
| Target | `466001/100000` | `233009/50000` | `116511/25000` |
| Site orbits / physical sites | 2,620 / 20,856 | 2,620 / 20,856 | 2,621 / 20,860 |
| Charge (rule) orbits | 889 | 889, unchanged | 889, unchanged |
| Total budget `M` | 17000402008 | 17000402008 | 17000448944 |
| Certificate’s requested minimum | 1000023648 | 1000023648 | 1000026409 |
| Replayed minimum core charge `Γ` | 1000026844 | 1000026844 | 1000026844 |
| `17Γ − M` | 54340 | 54340 | 7404 |
| Angle intervals | 2,168 | 2,808 | 4,991 |
| Least strict core margin | just above `10⁻¹⁰` | just above `10⁻¹²` | just above `10⁻¹²` |

Each requested minimum is `⌈M/17⌉`, the least integer charge that makes the count work;
the replayed `Γ` is higher, and the same on every interval of all three certificates.
The exact margins are in the C++ records, and for 4.66001 in its controls receipt.
R068’s advance over 4.66001 is exactly `43/100000`, and over R067 `13/50000`.

## How They Differ From 4.66001

[`packing/devtools/audit_guzhou_r068.py`](../../../devtools/audit_guzhou_r068.py)
`structure` reads each certificate beside Kleddamag’s and measures the difference; the
outputs are [`receipts/r067/structure.json`](receipts/r067/structure.json) and
[`receipts/r068/structure.json`](receipts/r068/structure.json), and
[`packing/tests/test_guzhou_r068_packet.py`](../../../tests/test_guzhou_r068_packet.py)
re-derives them.

**R067** changes only `A`, `normalized_target`, the entries and metadata, as its
`SOURCE_PIN.json` says.
Every site orbit, rule orbit, weight and the budget are 4.66001’s exactly.
Of the 2,168 original intervals, 1,528 are kept and 640 are split exactly at their
midpoint, giving 2,808; every original endpoint is an endpoint of the new chain, which
runs contiguously from `0` to `207107/500000`. The cores are rebuilt for the smaller
parent.

**R068** makes two edits to the site orbits and none to the rules:

- Orbit 1480, of weight 0, moves from `(9897067092, 9898744747)` to
  `(9897067092, 9897944747)` in units of `10⁻¹⁰`: its second coordinate falls by
  `0.00008`. Its eight images keep their sorted order, so its site indices 11832 to
  11839 name the same symmetry images as before; exactly one of the 889 rule orbits
  refers to them. Its weight is zero, so the move changes the geometry of that rule and
  not the budget.
- A new orbit 2620 at `(1.34, 1.34)` with weight 11734 per site lies on the diagonal, so
  it has four images, sites 20856 to 20859, appended after every existing site.
  No rule refers to them.

The 889 rule orbits are equal to 4.66001’s as JSON, so the budget changes only by the
new points: `17000402008 + 4 × 11734 = 17000448944`, the certificate’s own figure.
The 4,991 intervals again refine the original 2,168 without moving an original endpoint:
825 are kept, 994 are split exactly in two, and the rest are cut into 3 to 55 pieces.
The certificate’s requested minimum `1000026409` would leave a surplus of 9 units; the
replayed minimum is higher.

R068’s certificate records its lineage: the compensation geometry is a C007 research
candidate, the endpoint is C009’s continuation of an earlier complete target
`11651/2500` (certificate `08a2f9f0…6ed0`, not published), and the prior acceptance of
C009’s geometry is not reused.

## C010’s Local Material, a Research Record

R068 also publishes C010, which adds no global bound.
Its `STRIP_PROOF.md` gives a shifted-core method for 17 narrow half-angle intervals and
their wall-adjacent centre strips at the target `9321/2000 = 4.6605`, on a separate
model `FIT02` (`research/fit02/model.json`, budget `17000401055`, 20,949 sites), and
reports minimum open charge `1000026908` in every region.
It also supplies an exact interior counterexample to the same `FIT02` charge: a legal
parent at half-tangent `90505759/819200000` whose open and closed charge are both
`999975439`, so `17F − M = −818592`. The source’s own words are that this defeats that
fixed charge, not the method, and that local positive surplus does not become a global
`4.6605` bound. Both were replayed here and reproduce byte for byte; neither is a bound.

## What Is Retained, and What Is Not

**Retained byte-identical** under `n17-square-packing/`, at their upstream paths: the 93
files that changed or were added between `6f64e4b2` and `815b1626`. That is both whole
packages, `certificates/R067-4.66018/` (36 files) and `certificates/R068-C010/` (44),
the two publication records `R067_PUBLICATION.json` and `R068_PUBLICATION.json`, the two
workflows `.github/workflows/r067.yml` and `r068-c010.yml`, and the nine root files R068
last edited: `CHANGELOG.md`, `CITATION.cff`, `NOTICE.md`, `README.md`, `RESULTS.md`,
`docs/EVIDENCE_MAP.md`, `docs/RELEASE_NOTES.md`, `docs/REPRODUCIBILITY.md` and
`scripts/check_release_hashes.py`. Every file’s `git hash-object` equals its blob at
`815b1626`; ten large data files are stored as deterministic gzip, and for those the
identity holds after decompression ([Compressed Files](#compressed-files)). Several
files carry CRLF line endings as published, and those bytes are part of each package’s
manifest.

Every retained file is also described by a digest the source published: all 54 entries
of `R068_PUBLICATION.json` match, and 37 of the 46 in `R067_PUBLICATION.json`. The other
nine are the root files above, which that record describes as they stood at `d4e2c287`;
those earlier versions are not retained.

Some retained files repeat others.
R067’s `src/` and R068’s `upstream/cpp/` are the same six files, and R067’s
`upstream_notices/` and R068’s `upstream/notices/` the same twelve.
All twelve notices are Kleddamag’s release files, byte-identical to copies already
retained: `ATTRIBUTION.md`, `AUTHORS.md` and `LICENSING.md` as of 4.66001, and `LICENSE`
and the eight `NOTICES/` files as of
[`v1.0.0`](../n17-kleddamag-certified-bound-2026-09-21/README.md).
Despite the directory name, only one file under `upstream/cpp/` is Kleddamag’s:
`reference/verify_global_variable.js`, the BigInt checker, byte for byte Kleddamag’s
`bounds/4.66001/verify_global_variable.js` (`c2209186…49b7`). The rest is Guzhou0806’s
own code. `native_geometry.hpp`, the exact sweep kernel, is byte-identical to
`certificates/R052-4.62003/src/native_exact.cpp` at `6f64e4b2` (blob `7975877b`), the
kernel the
[R052 continuation packet](../n17-guzhou-r052-continuation-2026-09-26/README.md)
replayed; `verify.cpp` is the front end, which its header describes as adapted from
Kleddamag’s MIT general-rule checker; `replay.js` is the paired launcher; and
`probe.cpp` is C010’s finite-parent probe.

**Not retained:** the rest of the upstream repository, unchanged since `6f64e4b2` and
covered by the earlier Guzhou packets; `.git/`; and the replay intermediates too large
to be useful, such as C010’s 4.2 MB `strip.json`, whose digests are in the receipts.

**Licensing.** The upstream repository has no repository-wide licence.
The packages say the inherited sources and upstream notices keep their own licence
scopes, which repackaging does not broaden, that Boost is under the Boost Software
License 1.0 and is not distributed, and that no blanket licence is granted.
This packet is retained for verification and research use on the same basis as the
earlier Guzhou retentions.

## Replay Here

Every command ran between 2026-09-28T23:48Z and 2026-09-29T01:32Z in a clean clone of
the source at `815b1626`, outside this repository (`WORK` in the receipts), with outputs
in fresh directories inside it.
Both packages in that clone are byte-identical to this packet’s after the `gunzip -k`
below, and the source’s own record checks pass on such a restored copy of the packet too
([`receipts/packet/`](receipts/packet/)).

The host is a Linux 6.18 x86-64 container with four cores of an Intel Xeon Processor @
2.10GHz and 16 GB, shared with three other agent lanes; one-minute load averages ran
between about 3 and 13. Every command was pinned to two cores with `taskset -c 2,3`, so
the walls are contended readings, not benchmarks.
The compiler is Ubuntu’s `g++` 13.3.0 at the source’s `-O3 -std=c++17`, with Boost 1.83
headers (`libboost1.83-dev` 1.83.0-2.1ubuntu3.2, installed through apt for this replay).
Node is `v24.18.0`; the source asks for Node 22, its CI pins 22 and its own runs used
22.16.0. `N17_TIMEOUT_MINUTES=600`, the launcher’s documented setting, raised its
per-process timeout from the default 60 minutes, which the contended Node checkers would
have exceeded. [`receipts/replays.json`](receipts/replays.json) records every command,
start, end, wall, CPU and exit, and the digests of inputs and outputs.

R068, from `certificates/R068-C010/`, as its `REPRODUCIBILITY.md` and CI workflow give
it:

```sh
node check_package.js
mkdir -p .recheck/bin
g++ -O3 -std=c++17 upstream/cpp/verify.cpp -o .recheck/bin/verify
N17_TIMEOUT_MINUTES=600 node upstream/cpp/replay.js accepted/4.66044/certificate.json .recheck/global .recheck/bin/verify 2
node assert_ci.js global
```

R067, from `certificates/R067-4.66018/`, as its `REPRODUCIBILITY.md` gives it:

```sh
node check_records.js
g++ -O3 -std=c++17 src/verify.cpp -o verify
N17_TIMEOUT_MINUTES=600 node src/replay.js certificate.json fresh-paired-run ./verify 2
```

The launcher `replay.js` runs, for each of two partitions, the C++ checker and
Kleddamag’s Node BigInt checker concurrently; it writes `THEOREM.json` only if all four
processes exit 0, both checkers cover every interval, their minima and cell counts agree
on every interval, every minimum reaches the certificate’s requested threshold, and
`17Γ − M > 0`.

| Run | Wall | CPU | Exit | Status | What it establishes |
| --- | ---: | ---: | ---: | --- | --- |
| R068 package | 0.14 s | 0.06 s | 0 | `PASS_PACKAGE_BYTES_ONLY` | All 43 other package files match `MANIFEST.json` |
| R068 build | 16.9 s | 13.9 s | 0 | — | Executable `cf761bb5…19d5` |
| R068 global | 4,648.5 s | 4,093.0 s | 0 | `PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION` | Both checkers over all 4,991 intervals: target `116511/25000`, budget `17000448944`, minimum `1000026844`, surplus `7404` |
| R068 `assert_ci.js global` | 0.07 s | 0.03 s | 0 | `PASS_FRESH_EXPECTED_RESULTS` | The source’s CI assertions on the fresh `THEOREM.json` |
| R067 records | 0.16 s | 0.06 s | 0 | `PASS_RECORDED_FULL_COVERAGE` | Manifest identities and the shipped ledgers: all 2,808 intervals, C++ and Node rows equal, surplus `54340`; no geometry |
| R067 build | 24.0 s | 10.9 s | 0 | — | Executable `cf761bb5…19d5` again |
| R067 replay | 1,550.9 s | 2,105.2 s | 0 | `PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION` | Both checkers over all 2,808 intervals: target `233009/50000`, budget `17000402008`, minimum `1000026844`, surplus `54340` |
| C010 local, seven steps | 65.1 s | 57.2 s | 0 each | `PASS_FRESH_EXPECTED_RESULTS` | The two builds, the strip sweep and its BigInt check, both counterexample probes, and the source’s `assert_ci.js local` |

CPU is user plus system time of the command and all its children.
Inside the R068 run the C++ partitions took 1,671.8 s and 1,965.4 s and the Node
partitions 4,520.4 s and 4,648.1 s, each sharing two cores with three other processes;
the source’s own run took 1,265 s. Inside the R067 run the C++ partitions took 878.4 s
and 892.9 s and the Node partitions 1,546.8 s and 1,550.5 s; the source’s took 528 s at
three partitions. Both builds produce the same executable, `cf761bb5…19d5`; the source’s
was `8f4d59ac…aa42`, from GCC 14.2.0.

**Every row compared.** `audit_guzhou_r068 compare` reduces each ledger to
`(interval, minimum, cells)` and compares the fresh C++ and Node ledgers and the
published C++ and Node ledgers row by row
([`receipts/r068/compare.json`](receipts/r068/compare.json),
[`receipts/r067/compare.json`](receipts/r067/compare.json)):

|  | R068 | R067 |
| --- | ---: | ---: |
| Ledgers × rows compared | 4 × 4,991 | 4 × 2,808 |
| Rows differing | 0 | 0 |
| Rows at the minimum `1000026844` | 4,991 | 2,808 |
| Cells swept, summed | 2,210,145,745,763 | 1,249,459,677,392 |
| C++ sites / signed terms | 20,860 / 49,208 | 20,856 / 49,204 |
| Triples SHA-256 | `d2c47f4a…7407` | `5fe449f6…2d00` |
| Object-form SHA-256 | `3baf8875…bbcc` | `924b5f51…1b92` |

The triples digest is that of the compact JSON array of `[interval, minimum, cells]`,
the form the
[review](../../../../docs/project/reviews/review-2026-09-28-n17-guzhou-r067-r068.md)
used; the object form is the one the 4.66001 packet’s receipts used.
The triples digests equal the review’s, both digests equal the published ledgers’, and
the least strict margins in the fresh C++ records equal the published ones.
Beyond the rows, each fresh R068 partition record equals its published counterpart apart
from `seconds` and `verified_utc`, and each fresh `THEOREM.json` and `INPUTS.json` apart
from those and the executable digest.
R067 ran at two partitions where the source’s record has three, so its partitions are
compared by row; its `THEOREM.json` and `INPUTS.json` equal the source’s apart from
timing, the executable digest and the list of processes.
The fresh ledgers are kept, gzip-compressed, in `receipts/r068/replay/` and
`receipts/r067/replay/`, so the comparison can be re-derived from this packet;
[`packing/tests/test_guzhou_r068_packet.py`](../../../tests/test_guzhou_r068_packet.py)
does so.

**C010’s local material** reproduces byte for byte: the fresh `strip-independent.json`,
`failure-cpp.json` and `failure-bigint.json` are identical to the published
`research/fit02/` records, and the fresh `strip.json` (4.2 MB, not retained) has the
SHA-256 `437322b8…0c8a` that the published record binds.
All 17 regions give minimum `1000026908`, and the counterexample gives charge
`999975439` and surplus `−818592` from both the C++ probe and the BigInt check.

**What these replays do not establish** is independence of method.
Both checkers decide the same exact event-cell sweep of the same certificate.
The Node checker is Kleddamag’s, already replayed for 4.66001 and reviewed; the C++
checker is Guzhou0806’s and was first reviewed in the 2026-09-28 review above, which
also re-derived every premise and swept sampled rows with its own code.
That supports `V4`/`C3`, as for 4.66001. This repository’s native parent-core route
models only `k`-of-`m` threshold atoms, so it cannot read these certificates’
weighted-threshold and winning-subset orbits, and no method-distinct decision was
attempted. The upstream CI outcome was not observed.

## Compressed Files

Eighteen data files of more than 1,000 lines: ten of the source’s, the two certificates,
R067’s three shipped Node ledgers, R068’s four shipped partition records and C010’s
`FIT02` model, and this packet’s eight fresh partition records.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at `815b1626` and for a receipt are the bytes the
replay wrote. The repository’s readers take the upstream path and decompress
transparently through `devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.
The source’s `check_package.js`, `check_records.js` and launchers expect the plain
files.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/n17-guzhou-r068-2026-09-28 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `n17-square-packing/certificates/R067-4.66018/certificate.json.gz` | upstream | `b6ec14b0fcb6a970ef117f3a253593d896da1f19` | `101dd164906c7b71dc1397eaa32e25626548cd71995e532113823f434f8e5d26` |
| `n17-square-packing/certificates/R067-4.66018/evidence/node-0.json.gz` | upstream | `b7d85ef70ad9a638922fb71c57525bef9bdfb7a7` | `c389a741ce281602a06562617d8f88aa1e0513f553a1ecdc8badca58c1d1d06e` |
| `n17-square-packing/certificates/R067-4.66018/evidence/node-1.json.gz` | upstream | `0b01960f1db9eed54ff06dbc62e70d3363c53fd8` | `6e8cd587a32b5d29a6e88bbc6a030b6f2f25721448aba393e0f24efd6b529cb6` |
| `n17-square-packing/certificates/R067-4.66018/evidence/node-2.json.gz` | upstream | `654ef76ec86262615d005c098e0d446e60449186` | `2821f6c3f7d8b0c2b46f529a4df466ce12d2f4a459f9def4c3549f130a1913ec` |
| `n17-square-packing/certificates/R068-C010/accepted/4.66044/certificate.json.gz` | upstream | `a802d32febe4adbab0f2d3c6ea7ed900900d7307` | `cf70f74ddb47071b1d7333d8a43885d2915f43d45f26f6084a106dfdb0c5205f` |
| `n17-square-packing/certificates/R068-C010/accepted/4.66044/paired_replay/cpp-0.json.gz` | upstream | `bdb7f7da3d71fa9a37196862c237265aff0c3355` | `f0f6795f7357d873757e4b45fce9a5656052695b0db22fdce3fafae6a2bd4445` |
| `n17-square-packing/certificates/R068-C010/accepted/4.66044/paired_replay/cpp-1.json.gz` | upstream | `1b56f98cfe91adea72d9847912199916f640a1da` | `4df9c5423db54adda97f856f316a16de3a4713ecbe7aa9e088863ec44d9c34db` |
| `n17-square-packing/certificates/R068-C010/accepted/4.66044/paired_replay/node-0.json.gz` | upstream | `7b4e8afac378b8e035e61d767e6caa0636a40b0b` | `6b5c2479e392e56e4bd41cb04c4fdad950042dd70d6f8aa6027efb850488633f` |
| `n17-square-packing/certificates/R068-C010/accepted/4.66044/paired_replay/node-1.json.gz` | upstream | `d58fb0ec04641c40aa412582f52f7a1902dd5308` | `f8fd37f874c3d55fa38f1edc4e4016eeab94610e582b7021b4db8089285b37d3` |
| `n17-square-packing/certificates/R068-C010/research/fit02/model.json.gz` | upstream | `82c169a8cb011c100ed75b8d41d17fccb0c21c44` | `b9d9ec28b5a56681e0b0d9f083d6f723cab700ccfedc9cca1ff0f0ce85318da4` |
| `receipts/r068/replay/cpp-0.json.gz` | receipt | `3336867ca148c5536e55e3e8c59982c5e30a3011` | `75251c7d66792a043fa5b20fdc18b4d080e89979adf8309a86e1954226739dcd` |
| `receipts/r068/replay/cpp-1.json.gz` | receipt | `faea2c391adbaf2066eae1705c5aa80cb0f1cdf5` | `998d3c7f32285dbdaeeda898049b2ee4fcc1135d714bd53e443176186513a76c` |
| `receipts/r068/replay/node-0.json.gz` | receipt | `b3fe3d95bc03c971c0424016b992606d62759713` | `b7618d0055617873b31bdb0914bf533ce6e48048abe45f3bc56d6e60e221abc8` |
| `receipts/r068/replay/node-1.json.gz` | receipt | `5e54ea2c2e9d774b232e027d7e8ecb2275919974` | `c678409d9e9314acc58d0fb05797dabb2f868f75e040e967d1ddd7d4249c0405` |
| `receipts/r067/replay/cpp-0.json.gz` | receipt | `f231d64354e26635f9f99c825a21f15a92fcd04e` | `18987be5846f208aa4a85db8f1cb5a678c6f40d79e3bd32d5e18463a51f4e976` |
| `receipts/r067/replay/cpp-1.json.gz` | receipt | `9864a6b5a4da6ecff6cb4ef73bb7e721b9a9c249` | `fedc636e134290cb1912a85087dc712e06ad9beb694d614ce73c2e7d559b11e9` |
| `receipts/r067/replay/node-0.json.gz` | receipt | `eca817f7e8883f48e98a30a3696adcb6464e5a9f` | `176171add713a66c8a2e13337664d081538bebce88ce1c71e2fffec7281855c7` |
| `receipts/r067/replay/node-1.json.gz` | receipt | `e145fb1b886a8415ef998bba50b27303895853fc` | `4d524de287afca1562850d211c4b90d3b08783e8da1836797b046bf41b0848d7` |

## Retrieval Hashes

Digests of this packet’s copies, which are the source’s bytes unchanged.
Each package’s `MANIFEST.json` lists every other package file’s size and SHA-256, and
the source’s `check_package.js` and `check_records.js` check them.

| File | SHA-256 |
| --- | --- |
| `R067_PUBLICATION.json` | `61e1d41144a67e2e893d33ffdd46c6d2bbb5fef7784cbf95c4748c1a1fa5a949` |
| `R068_PUBLICATION.json` | `8898a00b60130a7b1f689ae92c2118c02633620676fa5cf12015a1a9effbc0f0` |
| `certificates/R067-4.66018/MANIFEST.json` | `c2c1b20c2c301079cc1c9b77c7dc6b615f28d4682eebf3d720bc38b00590424c` |
| `certificates/R067-4.66018/PROOF.md` | `8c7df39aecb216b1457bc96852c1bc09c06ae33b5d612d65f9b92d631b99b1a9` |
| `certificates/R067-4.66018/check_records.js` | `68f6591dbecf7d14e1ed34da9a60904f8277d60cb50786c37d32c155e92fe1f8` |
| `certificates/R068-C010/MANIFEST.json` | `0f85f7092ec27e5b552c434749f41a1f5500a6a26628afdf0ebc95ac11c3a666` |
| `certificates/R068-C010/PROOF.md` | `a97b6e9eb19c1cabc8f2bb5eb2325cff763f0917aa6ed3d924ce4bef3936eda1` |
| `certificates/R068-C010/STRIP_PROOF.md` | `58eaf2a47162996900623fea927a1377707dd6f95b86638cd44243242166bf2d` |
| `certificates/R068-C010/PUBLICATION_STATUS.json` | `d2286174c77f20c3f2654ee5371ed1ad2d8ef1e1aed6d06dbb5242a6d09420d2` |
| `certificates/R068-C010/check_package.js` | `23a4a8449536cd73b3d7e09bf4f83c4b82a64866b6636a645dce0050eb3e21a6` |
| `certificates/R068-C010/upstream/cpp/verify.cpp` | `3ba09554cef0ea0ee15444c4d30476f0e2435144e18b1ec2c908970ca306532c` |
| `certificates/R068-C010/upstream/cpp/native_geometry.hpp` | `ade0091aa238e2d6dd078f89c9877dce6e0d80f3bb22aedc7e19d6fd85a7ec22` |
| `certificates/R068-C010/upstream/cpp/replay.js` | `1125e5969fe0a22e92ea42845ac0dfe68aae5a2a0110550591a01fa43f297712` |
| `certificates/R068-C010/upstream/cpp/reference/verify_global_variable.js` | `c22091862df631f8cfd1f1bb8e5013f0b9c216f20be268fcd7104768919c49b7` |
| `README.md` | `136114a4d4711ac03accdf357c9cc6960adc72c0c51b4ea2c3bc4739eff4fa85` |

The C++ sources, launcher and BigInt checker match the `source_bindings` in R067’s
`evidence/ACCEPTANCE.json`; the certificate digests are in the Provenance table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
