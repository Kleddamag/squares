# wand125 Rectangle-Density Certificates Pinned 2026-10-02

This packet pins
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at
`b00fc70`, which raised seven of the 53 standing rectangle-density certificates that the
[October 1 packet](../wand125-rectangle-certificates-2026-10-01/README.md) pinned at
`1a25a5e`, at `n = 20`, 42, 59, 70, 77, 91 and 93, and added no count. It keeps this
repository’s exact preflight of all 53 standing certificates.
Its proposed Frontier key is **[wand125 rectangle bounds 2026-10-02]**. No issue requests
these certificates: the import of 2 October took them in from the source’s own commits.
Three of the seven raise what this record reports, at `n = 20`, 42 and 70; the other four
are below bounds registered or retained separately, as [Claims](#claims) says.

The three earlier packets stay as the records at `ad43d29`, `39d8ecc` and `1a25a5e`, with
their receipts. This packet retains only what is new at `b00fc70` and reads everything
else from them. The same revision also holds the six mixed certificates of the
[afternoon mixed packet](../wand125-mixed-bounds-afternoon-2026-10-02/README.md) and the
linear `mixed_n82_L932` of the [linear $n = 82$ packet](../wand125-linear-n82-2026-10-02/README.md),
pinned at this revision in packets of their own. Both read the root `README.md` from
here, and this packet’s tree manifest pins the whole tree they come from.

## Source and Pin

| Field | Value |
| --- | --- |
| Address | <https://github.com/wand125/square-packing-bounds> |
| Revision | `b00fc70f1904e9b1b567afee056d347f911209e8`, branch `main`, tree `03f0999d13d1c1462d15471908b43628f38bb01d` |
| Committed | 2026-10-02T15:16:36Z, stamped `2026-10-03T00:16:36+09:00` in the commit; the seven raised certificates arrived in three commits from 2026-10-02T05:58Z to 13:37Z |
| Retrieved | 2026-10-02T16:53:02Z, a depth-1 clone whose `main` was this revision |
| Requested | not requested; taken in with the afternoon’s requests on jlevy/squares#282 and #294 |
| Licence | MIT, copyright wand125 2026, byte-identical to the September 27 packet’s [`LICENSE`](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Tags, releases, submodules, Git LFS | none: `git ls-remote` lists only `refs/heads/main`, and the tree has no `.gitmodules` or `.gitattributes` |
| Upstream tree | 3,167 files, 1,365 MB, each pinned by SHA-256 in [`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256) |
| Retained here | 29 files under [`wand125-rectangles/`](wand125-rectangles/), byte-identical to the pinned tree after decompression ([Compressed Files](#compressed-files)) |
| Read from the earlier packets | 191 files, byte-identical to the pinned tree: 124 from the October 1 packet, 44 from the September 28 packet and 23 from the September 27 packet |

The clone has no history, so every commit date here is from a blob-filtered clone of the
whole history fetched in the same session. Each of the seven new certificate directories
has exactly one commit, given in the Claims table.

Of the 2,897 files pinned at `1a25a5e`, 2,852 are in this tree with the same digest.
Sixteen are gone, the withdrawn `mixed_n50_L7318`, and 29 changed: the top-level
`README.md`, three files of `point_n21_L5/acceptance/`, `mixed_n50_L735/README.md`, and
the `README.md`, `completion-audit.json` and proof bundle of eight mixed certificates,
which commit `23e2284` re-hashed after making a path in each bundle relative (the
[afternoon mixed packet](../wand125-mixed-bounds-afternoon-2026-10-02/README.md#what-23e2284-changed)
records what changed). No rectangle file changed. The source added 286 files: eight
rectangle certificate directories, the seven standing ones and `rect_n93_L973`, which
`rect_n93_L9735` superseded the same afternoon, and thirteen mixed and linear
directories.
[`acquisition/sources.json`](acquisition/sources.json) records the pin, the file counts,
the referenced files by packet and the claim list.
`python -m devtools.audit_wand125_rectangles --packet 2026-10-02 --acquire CHECKOUT`
rebuilds both acquisition files and the retained subset from a clean checkout at the
pinned revision. It first derives the standing certificate of every count from the
checkout’s candidates and refuses to run unless that set is the tool’s pinned table.

## Credit and AI Assistance

The source has no `CREDITS`, `NOTICE` or `AUTHORS` file.
Its attribution files are `LICENSE` and `point_n21_L5/UPSTREAM-LICENSE.txt`, Evan
Daniel’s MIT text for the point-only bundle. Credit is in the README, retained here as
[`wand125-rectangles/README.md`](wand125-rectangles/README.md), and its sections are
unchanged since the October 1 packet in what they say:

- **The method** (lines 868–892, “Attribution”): the section opens “The method is not
  ours.” It credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns and Gustavo
  Massaccesi, and this repository for row generation, column generation and branch and
  bound, and claims the search runs and the certificates.
- **The checker** (lines 314 onward, “Checking them”): `verify.cpp` and `run_verify.py`
  are Tokoharu’s, unchanged.
- **AI assistance** (line 920, “Status”): “Parts of this work were produced with AI
  assistance under human direction.” The same section says none of the certificates has
  been peer reviewed.

The three commits that add the seven certificates, `06eeb40`, `7d77022` and `4318bdf`,
each say every certificate was “accepted by tokoharu’s unmodified verifier (verify.cpp
a75140df) on all 201 angle cases and replayed from the published files with identical
node counts”, and each ends with a co-author trailer naming an AI assistant.

## What Is Retained

The tree has 325 rectangle certificate directories, one per rung of each count’s ladder.
The evidence for a count is its standing (highest) certificate:
`certified_candidate.json` (the exact side, shrink, rectangles and rational weights),
`certificate_metadata.json` (exact mass and input digest), and the upstream accepting
run’s `verification_summary.json` and `verified_angles.jsonl`.

- **Retained here**: the source `README.md`, which changed, and those four files for the
  seven standing certificates raised since `1a25a5e`.
- **Read from the earlier packets**: the four files of the 46 standing certificates
  unchanged since `1a25a5e`, 31 from the October 1 packet, 11 from the September 28 packet
  and 4 from the September 27 packet, and `LICENSE`, `requirements.txt` and the five
  files of `docs/` from the September 27 packet.
- **Pinned by digest only**, because the audit regenerates it: `certificate_input.txt`,
  which is the candidate as outward-rounded binary64 intervals and must hash to the
  recorded SHA-256.
- **Pinned by digest only**, because this repository already holds the bytes:
  `verify.cpp` and `run_verify.py`, byte-identical in every certificate directory to
  Tokoharu’s copies (SHA-256 `a75140df…` and `7bce2467…`).
- **Pinned by digest only**, because no claim here rests on it, or another packet holds
  it: the lower rungs, the matching certificates, the point certificates and `src/`; and
  the point-only, exact-cover, mixed and linear bundles, of which the mixed and linear
  certificates new at this revision are the two sibling packets’.

The audit tool reads a file held by an earlier packet from that packet’s
`wand125-rectangles/` directory and requires the digest this pin’s tree manifest records
for it.

## Claims

Each standing certificate proves `s(n) >= L`: its exact mass is strictly below `n`, and
every rotated, translated unit square captures mass at least one.
“Rectangles” counts the positive-weight orbit representatives; the checker sees eight
images of each. The seven raised certificates:

| `n` | Certificate | Side | Mass | Rectangles | Since `1a25a5e` | First commit (UTC) |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | `rect_n20_L49` | `49/10` = 4.9 | `1999/100` = 19.99 | 254 | raised from `1959/400` by 0.0025 | 2026-10-02T13:37:33Z, `4318bdf` |
| 42 | `rect_n42_L68275` | `2731/400` = 6.8275 | `4199/100` = 41.99 | 479 | raised from `1363/200` by 0.0125 | 2026-10-02T13:37:33Z, `4318bdf` |
| 59 | `rect_n59_L79375` | `127/16` = 7.9375 | `5899/100` = 58.99 | 604 | raised from `3173/400` by 0.005 | 2026-10-02T05:58:20Z, `06eeb40` |
| 70 | `rect_n70_L86275` | `3451/400` = 8.6275 | `6999/100` = 69.99 | 883 | raised from `69/8` by 0.0025 | 2026-10-02T08:25:06Z, `7d77022` |
| 77 | `rect_n77_L894` | `447/50` = 8.94 | `7699/100` = 76.99 | 663 | raised from `3573/400` by 0.0075 | 2026-10-02T05:58:20Z, `06eeb40` |
| 91 | `rect_n91_L96475` | `3859/400` = 9.6475 | `9099/100` = 90.99 | 915 | raised from `1929/200` by 0.0025 | 2026-10-02T13:37:33Z, `4318bdf` |
| 93 | `rect_n93_L9735` | `1947/200` = 9.735 | `9299/100` = 92.99 | 879 | raised from `3889/400` by 0.0125 | 2026-10-02T13:37:33Z, `4318bdf` |

The other 46 standing certificates are those of the
[October 1 packet’s table](../wand125-rectangle-certificates-2026-10-01/README.md#claims),
unchanged.

**What each raises.** At `n = 20`, 42 and 70 the new side is above what the case record
reports, `1959/400`, `1363/200` and `69/8`, all the source’s own earlier certificates; these
are the three the import takes in for registration. The other four are below bounds
registered or retained separately:

- at `n = 59` and 77 the source’s own exact covers prove `s(59) = 8` and `s(77) = 9`, both
  verified here;
- at `n = 91` the same revision’s mixed certificate proves `s(91) >= 97/10`; and
- at `n = 93` the same revision’s mixed `s(92) >= 39/4` carries to `n = 93` by
  monotonicity, above `1947/200`.

Until those two mixed certificates are registered, the record reports `1929/200` at
`n = 91` and `3889/400` at `n = 93`, which the new rectangles exceed.

**Carried upward.** A certificate of mass below `k` refutes `k` squares, so it also bounds
every larger count. The one transfer new at this revision is the `n = 91` certificate to
`n = 92`, `3859/400`, which the mixed certificates at `n = 92` exceed. The others are those
of the October 1 packet.

## How the Certificates Were Made

The method and checker are Tokoharu’s, reviewed on 2026-09-22 in the
[density mathematics review](../../../../docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md)
and, for sides up to `1791/200`, in the
[checker-scaling review](../../../../docs/project/reviews/review-2026-09-27-wand125-rectangle-scaling.md).
The seven are within the sides and orbit counts the October 1 certificates already
reached: the largest side among them is `1947/200` and the most orbits 915, against
`49259/5000` and 926 at `1a25a5e`. The
[afternoon review](../../../../docs/project/reviews/review-2026-10-02-wand125-afternoon-certificates.md)
covers them.

As at the earlier pins, every candidate’s weights were multiplied by one exact rational
factor before the recorded run, recorded under `scaling_experiment` as `factor_exact` with
its source and target masses. All seven have mass `n - 1/100`; the factors lie between
1.00009 and 1.03993. The checker reads the scaled data, and the preflight checks the
scaled mass exactly, so scaling bears only on how a certificate was found.

## Receipts

The audit tool is
[`devtools/audit_wand125_rectangles.py`](../../../devtools/audit_wand125_rectangles.py);
`--packet 2026-10-02` selects this packet.
It reuses the exact preflight of `devtools/audit_tokoharu_density.py`, with each
certificate’s own pinned side, and requires the candidate’s own `n` to be the pinned
count.

- [`receipts/preflight/audit.json.gz`](receipts/preflight/audit.json.gz): the exact
  preflight of all 53 standing certificates, the 46 unchanged ones read from the earlier
  packets. For each, the regenerated input matches the published SHA-256, every interval
  encloses its exact datum, the axis-event partition is complete, orbit normalization
  preserves mass, and the exact mass is below `n`. All 53 pass, in 32 s on one core; the
  46 unchanged entries equal those of the October 1 receipt.
- [`receipts/replay/audit.json`](receipts/replay/audit.json) and one directory per case:
  complete 201-direction replays of the three certificates this import registers,
  `rect_n20_L49`, `rect_n42_L68275` and `rect_n70_L86275`, with Tokoharu’s unchanged
  `verify.cpp` through `run_verify.py` at 4 workers, each reproducing the upstream
  accepting run’s nodes, leaves and lower bound at every direction. They ran in cloud
  batches on 3 October (`claude/replay-wand125-afternoon-r5` and `-r6`) and were merged
  on 6 October with `--merge`. None of the source’s programs was run in making this
  packet. The checker’s stage-4 controls are the October 1 packet’s
  [`receipts/controls/rect_n41_L676.json`](../wand125-rectangle-certificates-2026-10-01/receipts/controls/rect_n41_L676.json);
  the checker is the same byte for byte.

The preflight proves every obligation except global rotated coverage, which the external
checker decides; for the three replayed certificates the replay decides it here.

`python -m devtools.apply_wand125_rectangles --packet 2026-10-02 --replay-plan` lists
the standing certificates whose replay would raise a verified lower bound, each costed by
its upstream per-angle CPU time. For the three this import registers that is 5.25
CPU-hours at `n = 42`, 3.56 at `n = 70` and 1.36 at `n = 20`. Each is replayed into the
packet that retains it, from `packing/` with the project CPython 3.14 environment and a
C++17 `g++` on `PATH`:

```bash
.venv/bin/python3 -m devtools.audit_wand125_rectangles --packet 2026-10-02 \
  --out resources/web/wand125-rectangle-certificates-2026-10-02/receipts/replay \
  --resume --replay --workers 4 --n 42 --n 70 --n 20
.venv/bin/python3 -m devtools.apply_wand125_rectangles --packet 2026-10-02
```

A replay run elsewhere writes its own `--out` and is folded in with `--merge`. The first
promotion from this packet’s own receipt needs a replay entry,
`E-wand125-rectangle-2026-10-02-source-replay`, in `frontier/evidence.yaml`;
`apply_wand125_rectangles` stops and names it until it exists.

## Compressed Files

The seven candidates retained here, `certified_candidate.json` in each certificate
directory, are over 1,000 lines each, and so is the preflight receipt.
Each is stored as deterministic gzip made by `gzip -9n`, with no file name or timestamp
in the header, following the [R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes, which for an
upstream file are its blob and digest at the pinned commit and for the receipt are the
bytes this repository wrote.
The repository’s readers take the upstream path and decompress transparently through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.
Each upstream SHA-256 is also the one
[`acquisition/upstream-tree.sha256`](acquisition/upstream-tree.sha256) pins, and
`devtools.audit_wand125_rectangles` checks the retained subset against that manifest
through the decompressed bytes.

Before running any of the source’s own programs on this packet, restore the exact
upstream files from the repository root, in all four packets, since this one reads the
unchanged certificates from the other three:

```sh
find packing/resources/web/wand125-rectangle-certificates-2026-09-27 \
  packing/resources/web/wand125-rectangle-certificates-2026-09-28 \
  packing/resources/web/wand125-rectangle-certificates-2026-10-01 \
  packing/resources/web/wand125-rectangle-certificates-2026-10-02 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the repository’s readers require them to agree.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `wand125-rectangles/certificates/rect_n20_L49/certified_candidate.json.gz` | upstream | `20e16b65c87122ad80d113a6bc0651e5e3773773` | `4dc652d360d928a54d6607abbc312b4eb3d2d80dec59827fdc2b08b808af45a1` |
| `wand125-rectangles/certificates/rect_n42_L68275/certified_candidate.json.gz` | upstream | `0aa95f79603e92107f2c736f9ae78c911ae1a498` | `70d208063aeeb844c7f0db0d58f66cf6a1f1c5691543e825d11e3b3691eeb1f5` |
| `wand125-rectangles/certificates/rect_n59_L79375/certified_candidate.json.gz` | upstream | `001a7da41b8b4159a3c20146aed70d1684d8e3df` | `2a5ecc96c40349c52eeee2cf2eb36fd2ef37423160911ccfddfe1143484fb3e7` |
| `wand125-rectangles/certificates/rect_n70_L86275/certified_candidate.json.gz` | upstream | `201d6d6e6ff093d15f96766c59cce2e26daf53da` | `c21a24a1aaa11fb28456ed730f3032a970a25c3e07d84a446cbb458dfd3d3f91` |
| `wand125-rectangles/certificates/rect_n77_L894/certified_candidate.json.gz` | upstream | `0c5959fb78843a21b02c962873bd2cd02496fa1d` | `b27b66f0096b41c4ffab0a99bbf3ea31c6758dd68675fd96641007ef7aeecee8` |
| `wand125-rectangles/certificates/rect_n91_L96475/certified_candidate.json.gz` | upstream | `c3496abcad97c5ed8ae7785fbf365d9a52de645a` | `eb29ecbb1c905653aa2a053c8c6747f0321f0e17855aca013fee26b2ff6521b1` |
| `wand125-rectangles/certificates/rect_n93_L9735/certified_candidate.json.gz` | upstream | `cd0593a92228bafd3f4656af2260527759e9c0ad` | `fc70ef81a5644a9762a11f2db622f2fda745af8cc9f28e452cb939e35ffdfc76` |
| `receipts/preflight/audit.json.gz` | receipt | `434b35785a952dd7da342ee819fd4a844754c1e7` | `1ec08f25195b7266816cc78c0b517b7f1c5b973b474ba724d011d2a90b90c505` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
