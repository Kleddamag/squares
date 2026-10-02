# Evan Daniel’s October 2026 Square-Packing Source Packet

This partial packet retains source bytes for the
[October 1 source-coverage review](../../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md).
It does not contain a complete clone or a complete proof replay.
The new claims are `s(60) = 8` and `s(k² − 3) = k` for every integer `k ≥ 6`; the latter
rests on the single exact `Valid7` checker plus a conditional Lean reduction.
The retained dual notes and supports provide context for research on `s(12)` and
`s(21)`. The packet also holds the source’s run records for two requests to this
repository: `s(60) = 8`
([jlevy/squares#256](https://github.com/jlevy/squares/issues/256)) and the `s(32)` sweep
without the D4 fold
([comment on jlevy/squares#238](https://github.com/jlevy/squares/issues/238#issuecomment-5923097530)).

## Provenance and Layout

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Commit | [`08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5), `main` when fetched |
| Commit time | 2026-10-01 04:17:47 UTC, by GitHub API |
| Retrieved | 2026-10-01 |
| Previous local packets | [September 26](../evand-square-packing-2026-09-26/README.md) at `167d842c`; [September 28](../evand-square-packing-2026-09-28/README.md) at `6aa82ba4` |
| Compare | GitHub reports the pinned commit 54 commits ahead of `6aa82ba4`, none behind |
| Credit and license | [CREDITS.md](source/s12/CREDITS.md) and [MIT LICENSE](source/s12/LICENSE), retained unmodified |

The `source/` directory preserves the source repository’s relative paths.
Every row of [`source-manifest.tsv`](source-manifest.tsv) names the upstream path,
source Git blob, source byte count and retained path.
Each plain retained file matches its source Git blob.
The source’s `s60_mixed_cover_8.txt` exceeds 1,000 lines, so it is stored as
deterministic `gzip -9n` at
[`s60_mixed_cover_8.txt.gz`](source/s12/certificates/s60/s60_mixed_cover_8.txt.gz); its
*decompressed* Git blob matches the upstream file.
Four `s60` run records are stored the same way ([Compressed Files](#compressed-files)).
The upstream
[`runV3_6294052a_leaves.jsonl.gz`](source/s12/certificates/k2m3/qx2_zm/runV3_6294052a_leaves.jsonl.gz)
and `s32/zmx2_full_sym/roots.log.xz` were already compressed and are retained byte for
byte. No source file was edited to make this packet.

The retained sources include the live [Proofs](source/site/www/proofs.html) and
[Sources](source/site/www/sources.html) HTML, the two new write-ups, the `k2m3`
certificate files and frozen checker, the `s60` cover, README and run records, the `s32`
no-fold run, and the Lean reduction and data.
For adjacent research it includes [`FRIEDMAN.md`](source/s12/search/FRIEDMAN.md),
[`QUADRANT_EXACT.md`](source/s12/search/QUADRANT_EXACT.md),
[`CLIQUE_CONTINUUM.md`](source/s12/search/CLIQUE_CONTINUUM.md), the side-4 and side-5
exact dual supports and their checker, and selected `s(12)` negative-route notes.
The full retained file list, rather than this summary, defines the packet’s scope.

## Run Records for the Two Requests

Both requests name a revision earlier than this packet’s pin.
The directories they point to were compared across the two revisions in a clone of the
source.

| Request | Revision it names | Directory | Difference from the pin |
| --- | --- | --- | --- |
| [jlevy/squares#256](https://github.com/jlevy/squares/issues/256), `s(60) = 8` | `d9f79bc1beb52a38854b675c330fd25a6d37eeee`, 20 commits before the pin | `s12/certificates/s60/` | `git diff --stat d9f79bc1 08e8a5fa -- s12/certificates/s60` reports one file, `README.md`, with 2 insertions: a note dated 2026-09-30 on the `zmx2` flag `--sym-atoms`. The cover and every run record are the same blobs at both revisions |
| [Comment of 2026-10-01 on jlevy/squares#238](https://github.com/jlevy/squares/issues/238#issuecomment-5923097530), `s(32)` without the D4 fold | `2bf33bc36728baa7e7f4c7ff1859756e952dd621`, 11 commits before the pin | `s12/certificates/s32/` | None: the directory is Git tree `b4e020288b678792ad8470dd037e07efa0b1447a` at both revisions |

The comment is retained as
[`issue-238-author-2026-10-01.json`](issue-238-author-2026-10-01.json), body verbatim
from the GitHub API. It is the source of the statement that the author of `zmx2` was
permitted to read `zeromargin.py`: the brief it cites, `tasks/s21-finish/xcheck.md`, is
not in the public tree.

**The `s60` bundle** has 16 files at the pin.
Thirteen are retained under `source/s12/certificates/s60/`: the cover, `README.md`,
`SHA256SUMS`, `verify.sh` and the nine run records.

| Directory | Retained files | What its manifest records |
| --- | --- | --- |
| `zm_mixed_d4/` | `manifest.json`, `roots.jsonl.gz`, `run.log` | `zm_mixed.py cert … --d4 --cert-mode`, 102,400 roots, verdict `VERIFIED-D4` |
| `zmx2_d4/` | `manifest.txt`, `roots.log.gz`, `run.out` | `zmx2 cert … --d4`, 6,400 `ROOT` lines, 0 `UNCERT` lines |
| `zmx2_full/` | `manifest.txt`, `roots.log.gz`, `run.out.gz` | `zmx2 cert … --full`, 51,200 `ROOT` lines, 0 `UNCERT` lines |

The other three are the checker copies in `zm_mixed_d4/checker/`. They are **pinned by
digest only**, because each is the same blob as a file this packet retains at its
`search/` path:

| Upstream path | Bytes | Git blob | SHA-256 | Retained copy |
| --- | ---: | --- | --- | --- |
| `s12/certificates/s60/zm_mixed_d4/checker/mixed_cover.py` | 13,195 | `9779d73c390e676a3acbea4ae94e8ab47d3fe79b` | `bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5` | `source/s12/search/mixed_cover.py` |
| `s12/certificates/s60/zm_mixed_d4/checker/zeromargin.py` | 79,383 | `cd881bdd391cbeeb1eba80d8954d16bf1d82e3bc` | `640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab` | `source/s12/search/zeromargin.py` |
| `s12/certificates/s60/zm_mixed_d4/checker/zm_mixed.py` | 86,265 | `577d4f22058d452513b3f287cf1c9a57b6d97897` | `1fd203469bb43a55ca7ce376b9717437e0970eead31941ec7fa100ab24d5ba95` | `source/s12/search/zm_mixed.py` |

Those three SHA-256 values are the ones `zm_mixed_d4/manifest.json` records for the run.
The two `zmx2` manifests record `zmx2.rs` at SHA-256 `6b7f0f79…`, which is the file the
[September 28 packet](../evand-square-packing-2026-09-28/README.md) retains.
This packet’s `source/s12/verify2/src/bin/zmx2.rs` is the pin’s later version,
`1cd4dcbd…`.

**The `s32` bundle** has 20 files at the pin.
Six are retained under `source/s12/certificates/s32/`: `README.md`, `SHA256SUMS` and
`verify.sh`, which differ from the copies the earlier packets hold, and
`zmx2_full_sym/manifest.txt`, `roots.log.xz` and `run.out`. The manifest describes
`zmx2 cert s32_closed_cover_6.txt --full --pair-points --sym-atoms` with 28,800 `ROOT`
lines and 0 `UNCERT` lines.
Twelve more are in the
[September 26 packet](../evand-square-packing-2026-09-26/README.md) with the same Git
blobs, the larger ones after `gunzip`: the two covers, the two `zeromargin_d4*`
directories apart from `SUMMARY.txt`, and the four `zmcheck_d4/` files.
The two `SUMMARY.txt` files are pinned by digest in that packet’s README.

The no-fold run’s manifest records Git HEAD `e4af291c` and `zmx2.rs` at SHA-256
`92a4cfe87b4e33d57ce132c9c517eded3fe62b4a5a2151b5ba250b8ee329fe64`. That version (Git
blob `8ce809d617d239dcc40032e97b780a82bd4fb851`, 77,198 bytes, 19 commits before the
pin) is in no packet here.

## Unretained Inputs and Verification Scope

- Making this packet ran no source program and replayed no run record; any replay is
  recorded outside it.
  The source’s own checks are `source/s12/certificates/s60/verify.sh` and
  `source/s12/certificates/s32/verify.sh`. The shared Python checker and record-parser
  sources they call are retained at their upstream `source/s12/search/` paths.
  Frozen Python copies used by `k2m3` are retained separately under
  `source/s12/certificates/k2m3/qx2_zm/checker/`; the Rust `zmx2.rs` is under
  `source/s12/verify2/`. The complete upstream Rust build files are omitted.
- The `k2m3` packet includes its compressed leaf record, box and family files, checker
  and `verify.sh`. A Lean build still needs the rest of upstream `s12/lean` and Mathlib.
  No local check of the leaf record, fresh `qx2_zm.py` run, source `verify.sh`, or Lean
  build has been performed for this intake.
- The exact side-3.99 fractional packing value `12.028160810092…` in
  [`CLIQUE_CONTINUUM.md`](source/s12/search/CLIQUE_CONTINUUM.md) points to
  `runs/cqx_PURE99_support.txt`. That file is absent from the pinned public Git tree, as
  is the older `runs/dual_exact_3.99_support.txt` cited by
  [`DUAL_EXACT.md`](source/s12/search/DUAL_EXACT.md).
  The newer number improves the older `12.00823078252…`; their absence blocks a
  source-only replay of those two exact witnesses.
  By contrast, the side-4
  [`cover4_exact_support.txt`](source/s12/search/cover4_exact_support.txt) and side-5
  [`s21_nuf5_exact_support.txt`](source/s12/search/s21_nuf5_exact_support.txt) are
  public and retained here.
- This packet retains selected research notes but not the float LP runs under upstream
  `runs/`. Reported experimental values in those notes are source claims, not local
  measurements.

GitHub’s Git blob hashes, rather than a fresh checksum layer, verify identity across the
retained files. For a locally compressed file, compare the decompressed bytes with the
manifest blob using `gzip -dc` and `git hash-object --stdin`. A future certificate
replay should use the exact upstream commit and record its own commands, environment and
outputs in a separate receipt.

The retained bytes also agree with the digests the source wrote down.
The SHA-256 values in the table below for the cover and the three root records are those
in `s60/SHA256SUMS`, and each run manifest gives the same value for its root record.
`s32/SHA256SUMS` lists `zmx2_full_sym/roots.log.xz` as `b353d3c8…` and `manifest.txt` as
`fdf22af6…`, which the retained files have.
Decompressed, the `xz` log is 3,261,664 bytes in 28,801 lines with SHA-256 `3b867c39…`,
the manifest’s `log sha256`. These are identity checks on bytes; they decide nothing
about coverage.

## Compressed Files

Five `s60` files have more than 1,000 lines and were compressed locally with `gzip -9n`:
38,022,279 bytes upstream, 2,210,505 stored.
Each row gives the Git blob and SHA-256 of the decompressed upstream bytes, as produced
by `devtools.retained_data.describe`. `gunzip -k` on a stored file restores the upstream
file beside it.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `source/s12/certificates/s60/s60_mixed_cover_8.txt.gz` | upstream | `abf6acbbe24db7941bd2b6e7bb935700fe1931f1` | `2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41` |
| `source/s12/certificates/s60/zm_mixed_d4/roots.jsonl.gz` | upstream | `dcecef5747952100a03e57b9e0db2f2b43cc5c50` | `8b4019ce7a47904e7846be81cf929290a79e98ac9e5e453494f0cee5663c7810` |
| `source/s12/certificates/s60/zmx2_d4/roots.log.gz` | upstream | `b50d1309b86ed04898b336326259a7cf20eab29e` | `8a599325e8db3670eff8a3645ae035eb9d125716f10811d651ecc62841c656c8` |
| `source/s12/certificates/s60/zmx2_full/roots.log.gz` | upstream | `93686590cf2a8d396205cbc96d2f25c6644ee2dd` | `b88c66565acee3c6c2154b9d487f68b47200ace31d8f4182e7b69f71f244578a` |
| `source/s12/certificates/s60/zmx2_full/run.out.gz` | upstream | `14d03caf272a80746f0578af5d7955a77b80776f` | `f03e4620f114755b2c96d8f727ed2d6233510202e8c9acecda9706b9a7f8bcec` |

Two files were compressed by the source and are stored verbatim, so their *compressed*
bytes match the raw Git blob in the source manifest:
`k2m3/qx2_zm/runV3_6294052a_leaves.jsonl.gz`, a gzip file that keeps the source’s
filename and timestamp header, and `s32/zmx2_full_sym/roots.log.xz`. The generic
`retained_data.check_packet` gate assumes every `.gz` in a packet was made locally with
a deterministic header, so that gate does not apply to this mixed packet.
The focused source-manifest test checks every file with the appropriate byte
interpretation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
