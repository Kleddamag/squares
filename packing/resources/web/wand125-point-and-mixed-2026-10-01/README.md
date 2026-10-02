# wand125 Mixed Covers and Mixed-Rectangle Certificates, Pinned 2026-10-01

This packet pins seven certificate directories of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at its
commit of 1 October 2026, for three registration requests:

- **$s(59) = 8$**, a cover of points and axis-parallel segments on $[0,8]^2$ in Evan
  Daniel’s “mixed 1” format
  ([jlevy/squares#280](https://github.com/jlevy/squares/issues/280));
- **$s(77) = 9$**, a cover in the same format on $[0,9]^2$
  ([jlevy/squares#279](https://github.com/jlevy/squares/issues/279)); and
- **five rectangle-density lower bounds**, $s(37) \ge 161/25$, $s(65) \ge 167/20$,
  $s(66) \ge 421/50$, $s(90) \ge 48/5$ and $s(92) \ge 969/100$, of the same kind as the
  $s(50) \ge 37/5$ certificate in the
  [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md)
  ([jlevy/squares#282](https://github.com/jlevy/squares/issues/282)).

Its Frontier keys are **[wand125 exact covers 2026-10-01]** for the two covers and
**[wand125 mixed bounds 2026-10-01]** for the five densities.
The claims below are stated as the source states them.
Nothing in this packet was replayed or checked here beyond SHA-256 digests and Git blob
ids. Retention registers the claims for review; what the frontier makes of them is
decided in the frontier records.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `1a25a5ed745fdd905a52f48fcc48150a0669032d`, branch `main`, tree `d9a5b5e0b32f01eb643c7f701d081b45d0be9a1d` |
| Committed | Authored and committed 2026-10-01T21:10:40Z, which is 2 October by the author’s clock (`+09:00`) |
| Author | wand125, building on Evan Daniel’s method, format and checkers for the two covers and on Tokoharu’s format and verifier for the five densities |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” and is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T00:18Z, a depth-1 clone of `main`. On 2 October the GitHub API listed one branch, no tag and no release |
| Pinned subtree | 99 files, 127,975,196 bytes: the seven claim directories and the root `README.md`, `LICENSE` and `.gitignore`, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The other 2,798 files of the tree are pinned by the commit alone |
| Retained here | 37 files, 2,803,669 bytes upstream and 678,495 bytes as stored, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

The clone has no history, so the dates below come from the GitHub commits API, filtered
by path at the pinned revision.
Each directory has exactly one commit, with equal author and committer dates.

| Claim | Directory | First commit | Committed (UTC) |
| --- | --- | --- | --- |
| $s(65) \ge 167/20$ | `certificates/mixed_n65_L835` | `c21d1bd5b3f344b9478908097d09869cacc9017e` | 2026-09-29T13:37:05Z |
| $s(37) \ge 161/25$ | `certificates/mixed_n37_L644` | `baff9d23bd9940c678a0d83e495aa3353b26d9a9` | 2026-09-30T13:08:55Z |
| $s(90) \ge 48/5$ | `certificates/mixed_n90_L960` | `8038d64dd0001f1cbe79e295857e85b89aadc25e` | 2026-10-01T00:52:31Z |
| $s(92) \ge 969/100$ | `certificates/mixed_n92_L969` | `8038d64dd0001f1cbe79e295857e85b89aadc25e` | 2026-10-01T00:52:31Z |
| $s(66) \ge 421/50$ | `certificates/mixed_n66_L842` | `1807160d85a027b14122599871933a77fb316a06` | 2026-10-01T08:20:08Z |
| $s(77) = 9$ | `certificates/k2m4_n77_L9` | `bd4de4f67401779977b40752b15505c0689e9f73` | 2026-10-01T20:23:50Z |
| $s(59) = 8$ | `certificates/k2m5_n59_L8` | `1a25a5ed745fdd905a52f48fcc48150a0669032d` | 2026-10-01T21:10:40Z |

## Credit and AI Assistance, as the Source States Them

The tree’s only attribution files are `LICENSE` and `point_n21_L5/UPSTREAM-LICENSE.txt`,
Evan Daniel’s MIT licence.
It has no credits, notice, authors or citation file, so credit is read from the READMEs.

- **The root README** opens its Attribution section with “The method is not ours.”
  It credits Walter Stromquist, Hiroshi Nagamochi, Sam Burns and Gustavo Massaccesi, and
  this repository for the method, and claims the search runs and the certificates.
  Its Status section says: “Parts of this work were produced with AI assistance under
  human direction.”
- **$s(59) = 8$.** The directory README says the result “is built directly on Evan
  Daniel’s work”: the linear-program recipe, the cover format and both checkers are his,
  and the warm start and part of the column set come from his $s(60) = 8$ cover.
  It claims the decision to apply the recipe to the $k^2 - 5$ case, the further rounds,
  the restart and the recorded runs.
- **$s(77) = 9$.** The directory README credits Daniel with the base cover, the format
  and both checkers, and claims the central band insertion, the band measure and the
  replacement of points by short segments.
- **The five densities.** The $n = 65$ README calls the verifier a research copy of
  Tokoharu’s `verify.cpp`, and the other four name the same checker.
  Issue 282 says the format and base checker are Tokoharu’s and the measures and the
  modified checker are wand125’s. The `route` field of each `completion-audit.json` says
  how the measure was produced; for $n = 65$ it ends “Codex A pipeline continued by
  mathematics-f0”, and for $n = 37$ it ends “mathematics-f0”.

Both cover READMEs say the certificate “has not been reviewed by anyone outside this
project” and has not been formalised in Lean.

## What Is Retained

Retained byte-identical at their upstream paths:

- **`certificates/k2m5_n59_L8/`** whole, six files: `n59_mixed_cover_8.txt`,
  `README.md`, `verify.sh`, `SHA256SUMS`, `zm_mixed_d4/manifest.json` and
  `zm_mixed_root/manifest.json`;
- **`certificates/k2m4_n77_L9/`** whole, five files: `n77_mixed_cover_9.txt`,
  `README.md`, `verify.sh`, `SHA256SUMS` and `zm_mixed_d4/manifest.json`;
- from each of **`certificates/mixed_n37_L644/`**, **`mixed_n65_L835/`**,
  **`mixed_n66_L842/`**, **`mixed_n90_L960/`** and **`mixed_n92_L969/`**: `README.md`,
  `candidate.json`, `certificate.json`, `completion-audit.json` and `manifest.json`; and
- the root **`README.md`** (SHA-256 `80bee537…`, 44,137 bytes), which differs from the
  37,650-byte copy the September 28 rectangle packet retains.

Pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why not retained |
| --- | ---: | --- | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c81335f74a2fdbf1a98f5977bab14c0c4c30e3abcc97c34904` | Retained byte-identical by the September 27 rectangle packet |
| `.gitignore` | 132 | `0a31c24fe622ff8b4b012fbf790686063a84da3dd306d47e7283aad434653308` | A retained `.gitignore` would act on this repository’s tree. Its patterns are `__pycache__/`, `*.py[cod]`, `.venv/`, `*.pkl`, `*.npy` and `*.log` |
| `certificates/mixed_n37_L644/n37-L6.44-proof-bundle.tar.gz` | 13,231,440 | `1e3420bb16e6caf80048b66ca8a6a16ae766ec3e0db87a09fddd10db68c8c246` | Complete proof bundle |
| `certificates/mixed_n65_L835/n65-L8.35-proof-bundle.tar.gz` | 32,096,961 | `016f32f6a8be9bd03e6920d4cf3606676f63fac2caa90b029463655faa01eab8` | Complete proof bundle |
| `certificates/mixed_n66_L842/n66-L8.42-proof-bundle.tar.gz` | 25,981,553 | `0f06a42bd26f8a0dcdcbf408099ed003c6c6c16f6ed9317138f58bf2f8193109` | Complete proof bundle |
| `certificates/mixed_n90_L960/n90-L9.60-proof-bundle.tar.gz` | 25,998,524 | `98a828a0dc3673ee793de8ea37d8f55b335690c9b9bfbd17b36a58f46da493e2` | Complete proof bundle |
| `certificates/mixed_n92_L969/n92-L9.69-proof-bundle.tar.gz` | 27,668,753 | `52555aa331d6fe8d8f65911d0581cb4b46a2674e1a188ee35b9daecc258b4445` | Complete proof bundle |
| `certificates/mixed_*/code/*` | 193,070 in 50 | each in the subtree list | Each is byte-identical to the file of the same name in `mixed_n50_L740/code/`, which the [September 28 packet](../wand125-point-and-mixed-2026-09-28/README.md) retains |
| `certificates/mixed_*/requirements.txt` | 30 in 5 | `e09f656c130b9c08b2c5ab7187c891295e449ed77febea2a6ceee9cc98ccb0fc` | Byte-identical to `mixed_n50_L740/requirements.txt` in the same packet |

Each tarball digest is also the one its directory’s README and `completion-audit.json`
state. Each audit’s `certificate_sha256` is the digest of the retained
`certificate.json`.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
the pinned-only rules, and [`acquisition/sources.json`](acquisition/sources.json)
records the pin and every pinned-only file with its size, digest, reason and, where one
exists, the retained copy with the same bytes.
From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-point-and-mixed-2026-10-01 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision. It only reads the checkout and compares each file’s Git blob with
`git ls-tree`. With `--check` in place of `--checkout CHECKOUT` it needs no checkout: it
re-derives from this packet that every retained file has the digest the subtree list
records, that every pinned-only file named as identical to a retained copy is, and that
the record is complete.
The tool is [`devtools/acquire_source.py`](../../../devtools/acquire_source.py), and
[`tests/test_acquire_source.py`](../../../tests/test_acquire_source.py) runs the check.

## The Claims, as the Source States Them

| Claim | Directory | Measure | Total | Checks the source reports |
| --- | --- | --- | --- | --- |
| $s(59) = 8$ | `k2m5_n59_L8` | 26,308 points and 5,240 segments of length $1/50$ on the 14 interior lattice lines, invariant under $D_4$ | $1474762899/25000000 = 58.99051596$ | `zmx2 cert --d4` over 6,400 roots and `--full` over 51,200; `zm_mixed.py cert --d4 --cert-mode` in two runs, described below |
| $s(77) = 9$ | `k2m4_n77_L9` | 28,273 points and 6,420 segments, invariant under $D_4$ | $43347137744028965/2^{49} = 76.999984600031\ldots$ | `zmx2 cert --d4 --pair-points` over 8,100 roots and `--full --pair-points` over 64,800; `zm_mixed.py cert --d4 --cert-mode` at depth 24 over 129,600 roots, verdict `VERIFIED-D4` |
| $s(37) \ge 161/25$ | `mixed_n37_L644` | 350 rectangles | $3699999/100000$ | `code/mixed_rotated_verify.cpp` at 200 oblique net angles and integer tables at angle zero; least bound stated $1.0000000054\ldots$ |
| $s(65) \ge 167/20$ | `mixed_n65_L835` | 787 rectangles | $6499999/100000$ | The same; least bound stated $1.0000000004\ldots$ |
| $s(66) \ge 421/50$ | `mixed_n66_L842` | 631 rectangles | $6599999/100000$ | The same; least bound stated $1.0000000009$ |
| $s(90) \ge 48/5$ | `mixed_n90_L960` | 762 rectangles | $8999999/100000$ | The same; least bound stated $1.000000000042$ |
| $s(92) \ge 969/100$ | `mixed_n92_L969` | 832 rectangles | $9199999/100000$ | The same; least bound stated $1.0000000034$ |

“Mixed” means two different things here.
The two covers are mixed in Daniel’s sense: point masses plus mass spread uniformly
along axis-parallel segments, with every closed unit square in the container required to
capture at least $1$. The five `mixed_*` directories hold rectangle densities with no
point mass (each `candidate.json` has an empty `points` list), with core side
$B = 9977/10000$, 201 net half-angles of step $83/40000$ and coverage threshold $1$, as
for $n = 50$. Each `certificate.json` has status `ALL_ANGLES_VERIFIED_AND_REPLAYED`, and
its `replay_scope` says the oblique replay is not a separate implementation.

Both covers start from Daniel’s $s(60) = 8$ cover, SHA-256 `2d0e456e…`, which the
[October 1 evand packet](../evand-square-packing-2026-10-01/README.md) retains.
The $s(59)$ cover uses it as a warm start and column source for his line-cover linear
program. The $s(77)$ cover cuts it at $4$ in both coordinates, moves the far parts by
$1$, and adds a band measure of mass about $16.43$; 84 of its points on loaded lattice
lines were replaced by segments of length $2/1000$.

## Facts About the Two Cover Directories

**The published directories are incomplete against their own checksum files.** The
repository’s `.gitignore` excludes `*.log`, and none of the 2,897 files at the pin has a
name ending in `.log`. `k2m5_n59_L8/SHA256SUMS` lists `zmx2_d4/run.log`,
`zmx2_full/run.log`, `zm_mixed_d4/run.log` and `zm_mixed_root/run.log`, and
`k2m4_n77_L9/SHA256SUMS` lists the first three.
Each `verify.sh` runs under `set -eu`, and its first check is `sha256sum -c SHA256SUMS`,
so on a fresh checkout it cannot pass its first step.
That is read from the scripts; they were not run.
The other five entries of the first file and four of the second match the retained
files. The manifests name their per-root records, `roots.jsonl`, by SHA-256 only.

**The exact-rational evidence for $s(59)$ is two runs.** `zm_mixed_d4/manifest.json`
records the complete run at depth 24: 102,400 roots, 1,514,784 boxes, 6 uncertified,
verdict `NOT VERIFIED`. `zm_mixed_root/manifest.json` records a second run of the same
checker at depth 34 on the region $[27/20, 7/5] \times [13/10, 27/20]$ with
$u \in [1/4, 9/32]$: 1 root, 13,767 boxes, none uncertified, verdict
`VERIFIED-D4 (PARTIAL)`. The README says the six boxes lie in that region; the log that
lists them is not in the tree.
For $s(77)$ the one manifest records 826,120 boxes, none uncertified.
Every manifest’s input digest is that of the retained cover.

**The checkers are Evan Daniel’s and are not bundled.** Each `verify.sh` clones
[evand/square-packing](https://github.com/evand/square-packing), checks out
`b91d70b6ed314624c1434b628a9c7bf9a132c743` (committed 2026-09-29T01:21:40Z) and requires
four SHA-256 values.
This repository already retains all four files byte for byte: each has the required
SHA-256, and the Git blob the GitHub API reports at `b91d70b6`.

| Upstream path | SHA-256 `verify.sh` requires | Git blob | Retained in |
| --- | --- | --- | --- |
| `s12/verify2/src/bin/zmx2.rs` | `6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed` | `7725c08c` | [September 28 evand packet](../evand-square-packing-2026-09-28/square-packing/s12/verify2/src/bin/zmx2.rs) |
| `s12/search/zm_mixed.py` | `ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac` | `2edf8ca4` | [September 28 evand packet](../evand-square-packing-2026-09-28/square-packing/s12/search/zm_mixed.py) |
| `s12/search/mixed_cover.py` | `bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5` | `9779d73c` | [September 28 evand packet](../evand-square-packing-2026-09-28/square-packing/s12/search/mixed_cover.py) |
| `s12/search/zeromargin.py` | `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab` | `cd881bdd` | [September 26 evand packet](../evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py) |

The September 26 packet also retains `s12/verify2/Cargo.toml` and `Cargo.lock` with the
blobs `3d17ad2a` and `fb74714e` they have at `b91d70b6`. The October 1 evand packet
holds later versions of `zmx2.rs` and `zm_mixed.py`, which are not the pinned ones.

## Where the Requests and the Retained Files Differ

- **Logs.** Issues 279 and 280 say the logs are in the directory.
  They are not in the tree.
- **`--pair-points`.** Issue 279 describes the two `zmx2` sweeps of the $s(77)$ cover
  without this flag. The README and `verify.sh` run both with it.
- **Independence.** The $s(77)$ README says the certificate passes “three independent
  sweeps”, and the $s(59)$ README names “two independently written checkers”.
  Both issues say the two checkers are Daniel’s and share the common mode described in
  issue 256.
- **How the $n = 65$ measure was found.** Issue 282 says the $n = 37$ and $n = 65$
  measures were generated directly at the target side.
  The $n = 65$ README and audit say it was contracted from a search state at $L = 8.40$
  by the factor $167/168$ and then repaired.
- **Whose format.** Issue 282 says the format is Tokoharu’s. Each directory README says
  the certificate is not in his format, because its least coverage bound is below the
  $1.0001$ his `verify.cpp` requires.
- **Where the second replay ran.** Issue 282 says each full replay was run again from
  the published tarball on a separate machine.
  The directory READMEs say it was run again from the tarball and do not say where.
- **The earlier value at $n = 59$.** Issue 280 gives $7.93$ as the register’s current
  value. The source’s READMEs call $793/100$ the previous best lower bound.
  The tree at the pin holds the source’s own rectangle directories `rect_n59_L793` and
  `rect_n59_L79325`.

Within the source, the $n = 92$ README and the root README give the earlier value as
$9.645$, and the `compared_note` of the $n = 92$ `completion-audit.json` says $9.6475$.

## Limitations

- **Nothing was replayed.** No checker was built or run, no tarball was unpacked, and
  neither `verify.sh` was executed.
  The statements above are read from the retained files or are digest comparisons.
- **The bundles are pinned and not held.** A replay of the five densities needs the
  tarballs from the source at the pinned revision; each must have the digest above.
- **Dates come from GitHub.** The clone is shallow, so first-commit dates rest on the
  commits API and not on local history.

## Replay of `s(59) = 8` Here, 2 October 2026

Stage 4 of the [result import](../../../campaign/result-import.md) for
[jlevy/squares#280](https://github.com/jlevy/squares/issues/280) replayed Daniel’s
interval checker, the one the source’s `verify.sh` requires, on the retained cover. The
receipts are in [`receipts/`](receipts/).

| Run | Roots | Boxes | Uncertified | Max depth | Verdict | Wall, CPU |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `zmx2 cert … --d4 --threads 3` | 6,400 | 9,844,124 | 0 | 31 | `VERIFIED-D4` | 49 s, 143 s |
| `zmx2 cert … --full --threads 3` | 51,200 | 79,108,328 | 0 | 31 | `VERIFIED` | 394 s, 1,161 s |

- **The checker** is `zmx2.rs` SHA-256 `6b7f0f79…`, the version `verify.sh` requires,
  retained in the [September 28 evand packet](../evand-square-packing-2026-09-28/README.md)
  and built as for `s(60)`
  ([October 1 evand packet](../evand-square-packing-2026-10-01/README.md#replay-of-s60--8-here-2-october-2026)):
  rustc 1.97.0, binary SHA-256 `cba78a9e…`, on a 4-core x86-64 Linux container. The
  source’s `verify.sh` cannot pass as published (its checksum step names unpublished
  logs), so its two `zmx2` steps were run as this repository’s own sequence, with the
  same flags.
- **The audit** by `devtools.audit_evand_mixed_covers`: both root logs cover their
  regions exactly once with no uncertified or capped box
  ([`n59_zmx2_d4_audit.json`](receipts/n59_zmx2_d4_audit.json),
  [`n59_zmx2_full_audit.json`](receipts/n59_zmx2_full_audit.json)), and the box totals
  equal those the source’s README states for its unpublished runs. The source’s logs
  are not published, so no root-for-root comparison is possible. The cover facts are in
  [`n59_cover_audit.json`](receipts/n59_cover_audit.json) and
  [`n77_cover_audit.json`](receipts/n77_cover_audit.json).
- **The exact-rational route is undecided** from what is published:
  [`n59_zm_mixed_manifest_audit.json`](receipts/n59_zm_mixed_manifest_audit.json) records
  that the two `zm_mixed.py` manifests do not say whether the complete run’s six
  uncertified boxes lie in the region the second run certified, and only the
  unpublished per-root records could. The review of 2 October found that blocking for
  recording that route as evidence, and the `zmx2` route above is the one recorded.

## Replay of `s(77) = 9` Here, 2 October 2026

Stage 4 for [jlevy/squares#279](https://github.com/jlevy/squares/issues/279) runs the two
`zmx2` sweeps `verify.sh` names, with the checker built as for `s(59)` above.

| Run | Roots | Boxes | Uncertified | Max depth | Verdict | Wall, CPU |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `zmx2 cert … --d4 --pair-points --threads 3` | 8,100 | 5,810,824 | 0 | 36 | `VERIFIED-D4` | 4,112 s, 12,154 s |
| `zmx2 cert … --full --pair-points --threads 4`, in two halves | 64,800 | 46,583,600 | 0 | 36 | `REGION CLEAN` in each half | 34,255 s, 134,363 s |

- **The d4 root log** covers its region once per root with no uncertified or capped
  box, and its box total equals the one the source’s README states
  ([`n77_zmx2_d4_pairpoints_audit.json`](receipts/n77_zmx2_d4_pairpoints_audit.json)).
- **The unreduced sweep** was split by root column, `--xlo 0 --xhi 44` and
  `--xlo 45 --xhi 89`, and run by `devtools.replay_evand_zmx2` from the same retained
  `zmx2.rs` and cover on 4-core containers.
  Each half ran in three parts of at most 6,600 s, the later two resuming its root log,
  so each has a first receipt, `_resume1`, `_resume2` and a root log
  ([`n77_zmx2_full_pairpoints_x0-44_y0-89.log`](receipts/n77_zmx2_full_pairpoints_x0-44_y0-89.log),
  [`n77_zmx2_full_pairpoints_x45-89_y0-89.log`](receipts/n77_zmx2_full_pairpoints_x45-89_y0-89.log)).
  Each half ended `REGION CLEAN` over 32,400 roots with 23,291,800 boxes and none
  uncertified; the two regions are mirror images under $x \mapsto 9 - x$, and their
  totals are equal.
- **The audit** gives the whole-cover verdict, which `zmx2` does not give a region run:
  [`n77_zmx2_full_pairpoints_audit.json`](receipts/n77_zmx2_full_pairpoints_audit.json)
  reads the two root logs as one joined record and finds each of the 64,800 roots of
  the unreduced region present once, none uncertified or capped, with headers equal
  apart from the region and the box total the source’s README states.
  The source’s logs are not published, so no root-for-root comparison is possible.
- **The source’s `verify.sh` cannot pass as published**, for the reason given for
  `s(59)`: its checksum step names three logs that are not in the tree.
  Its two `zmx2` steps were run here as this repository’s own sequence, with the same
  flags.

## Controls for the Mixed Checker

[`receipts/n37/control.json`](receipts/n37/control.json) holds the stage-4 controls of
2 October for `mixed_rotated_verify.cpp`, made by
`audit_wand125_point_and_mixed mixed-control n37` with the shipped compile: the checker
accepts `mixed_n37_L644` at net index 99, its least recorded bound, matching the shipped
record, and refuses two mutated copies there (`ANGLE_UNRESOLVED`): every mass scaled by
99/100, and the heaviest orbit at a witness centre deleted, whose exact coverage falls to
0.99918 and 0.97768. `tests/test_wand125_checker_controls.py` holds them.

## Compressed Files

Twelve upstream data files of more than 1,000 lines are stored as deterministic gzip
made by `gzip -9n`: the two covers and the five candidates and certificates.
Each has no file name or timestamp in its header.
The table gives the Git blob and SHA-256 of the decompressed bytes, which are the file’s
blob and digest at the pinned commit; each SHA-256 is also the one
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) pins.
The repository’s readers take the upstream path and decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

Before running any of the source’s own programs on this packet, restore the exact
upstream tree from the repository root:

```sh
find packing/resources/web/wand125-point-and-mixed-2026-10-01 -name '*.gz' -exec gunzip -k {} +
```

The restored plain files are untracked, so remove them afterwards; while both copies are
present, the acquisition check reports each as retained twice.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/k2m4_n77_L9/n77_mixed_cover_9.txt.gz` | upstream | `46a69f3bd8ec143bb470d3f80ed8a88b960c3686` | `47b57cfe38cbfdbcf5320e59caffe712f4ef32df8aad42b0d7f697de6d26cdd7` |
| `square-packing-bounds/certificates/k2m5_n59_L8/n59_mixed_cover_8.txt.gz` | upstream | `2d232ce8561619a45aafe9a6e509ba60ff730118` | `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19` |
| `square-packing-bounds/certificates/mixed_n37_L644/candidate.json.gz` | upstream | `94a4fd2f7e784caa52d0a862be9b1fb93989d9ab` | `7ec9710b726e993bb0cba78f1e6ffcc04d922683dbb5b715999d24f77f1fa181` |
| `square-packing-bounds/certificates/mixed_n37_L644/certificate.json.gz` | upstream | `d289b71cbcc39cf7b48f5b30a737a4d9a7083e8b` | `e7e37a8185ea41b2ffa0ad055ae44a1510b0cd3d09b6e1ad21c145864e056ebf` |
| `square-packing-bounds/certificates/mixed_n65_L835/candidate.json.gz` | upstream | `7d64036d204c4c8fff7d401575f13f51fecd94a9` | `3efa71a4ed1d8ab9b10a53c0380decda8efd8b58b6cff9976f62d7b59e250ac0` |
| `square-packing-bounds/certificates/mixed_n65_L835/certificate.json.gz` | upstream | `adda24733a3947ed6b84ba7b6cb4dba8cbfa67ce` | `4938349af713e5ebee4756544304251a6b94705697b5811fd94be5d31ca7ead1` |
| `square-packing-bounds/certificates/mixed_n66_L842/candidate.json.gz` | upstream | `ce64de981c5086e3ffe701498976befe6d679073` | `8bbd7b41c39b194c530aca7553758d344f17bf0880a16eb3e0069883fc5c22a7` |
| `square-packing-bounds/certificates/mixed_n66_L842/certificate.json.gz` | upstream | `db6c93c8fce5eed9ffdb4086fc2232d84ef85322` | `304f36d50b58d462e8a754fe62da29496bc8bc9bb48cad8f221fb7aceb726053` |
| `square-packing-bounds/certificates/mixed_n90_L960/candidate.json.gz` | upstream | `f865fa203faf68d151adf2b3cec8e2de4ca64b42` | `23736896dba071806fac66394461799ba98c22ea7db851e51ad90557876a28c3` |
| `square-packing-bounds/certificates/mixed_n90_L960/certificate.json.gz` | upstream | `3d4dfae78ccc193faa89ae83e8430f2dc95f40a7` | `ad166589b414c861f5b882d109b30ae3b50b66ca062d92df06cc84720ee53e62` |
| `square-packing-bounds/certificates/mixed_n92_L969/candidate.json.gz` | upstream | `6575f6e3af85e163d7b3e7b1212557fa31e152de` | `4cab1b5e21a24c12e6718b17c78c27b58af2c6d7215425939732e424bbc0e5bc` |
| `square-packing-bounds/certificates/mixed_n92_L969/certificate.json.gz` | upstream | `e33f3931c1e5714eab70bfc24140a2068779a432` | `d4a9aeacf4409efa2aec531df3163a7bb0b74bfdc02e6416b625c66914218469` |
| `receipts/n59_zmx2_full.log.gz` | receipt | `9ad580f1383546bc35f20d3ebef17bf42b9937b6` | `ce60c5f6e0644a0f437d30b838158c4f482a6a55699b2fa1cff02b14d85f73d9` |
| `receipts/n59_zmx2_d4_roots.log.gz` | receipt | `39dd994f89fc468d7fc35f235fa875afa413fb5f` | `8e012c81d21603dd8140dfc9fb4ccdde1ffbd3d38ad46ed4497319c4071d1261` |
| `receipts/n59_zmx2_full_roots.log.gz` | receipt | `d64d9c33fd19f03ef842ce67d3b62c76a5c090ab` | `2d6c765a4a7120ed3d60d640acb77088b621a93c8f6a5475d05ced800208b79e` |
| `receipts/n77_zmx2_d4_pairpoints_roots.log.gz` | receipt | `e6939fed684335c5916eed9576b8afa0fdff797b` | `8a8f54c4f353bf5712a3fa92511a3b3ed92b5c84e0d0d32fcc30c3bbeecafc6a` |
| `receipts/n77_zmx2_full_pairpoints_x0-44_y0-89_roots.log.gz` | receipt | `f19c5c646611b85b1db0572a9799f9109564426e` | `fa3c979493b2d1eca106d2c6c2663d6ac04cc665c97731ac068b0a096e823663` |
| `receipts/n77_zmx2_full_pairpoints_x45-89_y0-89_roots.log.gz` | receipt | `7c28864933444cd81abb75f58fd0df2eb744d0ba` | `dd5671350795bbb295d9943560cd7c5dddbaa11af98b2fad6c9df697914734cc` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
