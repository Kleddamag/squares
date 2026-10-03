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

## Replay of `s(60) = 8` Here, 2 October 2026

Stage 4 of the [result import](../../../campaign/result-import.md) for
[jlevy/squares#256](https://github.com/jlevy/squares/issues/256) replayed the source’s
interval checker on the retained cover. The receipts are in [`receipts/`](receipts/).

| Run | Roots | Boxes | Uncertified | Verdict | Wall, CPU |
| --- | ---: | ---: | ---: | --- | --- |
| `zmx2 cert … --d4 --threads 3` | 6,400 | 2,617,534 | 0 | `VERIFIED-D4` | 16 s, 48 s |
| `zmx2 cert … --full --threads 3` | 51,200 | 21,036,120 | 0 | `VERIFIED` | 128 s, 380 s |

- **The checker** is `zmx2.rs` SHA-256 `6b7f0f79…`, the version both of the source’s
  `zmx2` manifests name, retained in the
  [September 28 packet](../evand-square-packing-2026-09-28/README.md), built with the
  crate files of the [September 26 packet](../evand-square-packing-2026-09-26/README.md)
  by `cargo build --release` under rustc 1.97.0; binary SHA-256 `cba78a9e…`
  ([`zmx2_6b7f0f79_build.log`](receipts/zmx2_6b7f0f79_build.log)). It was read before it
  was run, as the review of 28 September read it. The source’s `verify.sh` was not run:
  it builds the pin’s later `zmx2.rs`, not the one that made the records (finding F2 of
  the [review of the geometric premises](../../../../docs/project/reviews/review-2026-10-02-evand-s60-geometric-premises.md)),
  so its sweep was run directly with the version the records name.
- **The host** was a 4-core x86-64 Linux container; each receipt’s header and footer give
  the command, load, wall and CPU, written by `devtools.replay_receipt`.
- **The audit** by `devtools.audit_evand_mixed_covers`, which parses with its own code:
  both root logs cover their regions exactly once with no uncertified or capped box
  ([`s60_zmx2_d4_audit.json`](receipts/s60_zmx2_d4_audit.json),
  [`s60_zmx2_full_audit.json`](receipts/s60_zmx2_full_audit.json)), and root for root
  their census equals the source’s `zmx2_d4/roots.log` and `zmx2_full/roots.log`, 6,400
  of 6,400 and 51,200 of 51,200 roots, with identical headers
  ([`s60_zmx2_d4_compare.json`](receipts/s60_zmx2_d4_compare.json),
  [`s60_zmx2_full_compare.json`](receipts/s60_zmx2_full_compare.json)). The cover’s exact
  total, D4 invariance and loaded lines are in
  [`s60_cover_audit.json`](receipts/s60_cover_audit.json).
- **Not run:** the exact-rational `zm_mixed.py` sweep, about 19.6 CPU-hours at the
  source, which is the same author’s second checker and is recorded as a second route
  when it runs (`think-mx3k`).

## `T-064`: Checks and Plans Here, 2 October 2026

Stage 4 of the result import for `T-064`, Valid7 and the Lean reduction.
The [method review](../../../../docs/project/reviews/review-2026-10-02-valid7-independent-checker.md)
explains each of these; none is a complete replay of either checker.

- [`receipts/valid7/k2m3_verify_fast.log`](receipts/valid7/k2m3_verify_fast.log): the
  bundle’s fast `verify.sh` on `source/s12` as retained, exit 0. That covers the hashes,
  the cover’s total and D4 invariance, the family rebuilding the cover, Lemma Z re-run
  and identical to `lemmaZ.out`, the run V3 record re-checked, and `BentzData.lean`
  regenerated identical. It recomputes no positive-tilt leaf.
- [`receipts/valid7/qx2_calibration_x27-28_y23-24.log`](receipts/valid7/qx2_calibration_x27-28_y23-24.log)
  and [`qx2_calibration_compare.json`](receipts/valid7/qx2_calibration_compare.json):
  one centre cell of `qx2_zm.py` with run V3’s settings, 8 roots, 123.6 CPU-s against
  122.5 recorded, every leaf list equal to V3’s.
- [`receipts/valid7/qx2_replay_plan.json`](receipts/valid7/qx2_replay_plan.json): the
  full replay priced and split into two 4-core shards by
  [`devtools.plan_valid7_replay`](../../../devtools/plan_valid7_replay.py), 22.8 CPU-hours
  here.
- [`receipts/lean/bentz_stage.json`](receipts/lean/bentz_stage.json): the import closure
  of `bentz_of_valid7` staged by
  [`devtools.stage_evand_bentz_lean`](../../../devtools/stage_evand_bentz_lean.py), every
  file at its `08e8a5fa` blob. `S32Data.lean` was regenerated from the September 26
  packet’s $s(32)$ cover. It was not built: this container lacked the disk for the
  toolchain and Mathlib’s cache.

## Full Replay of `Valid7` Here, 2 and 3 October 2026

Daniel’s `qx2_zm.py` was replayed in full on the retained cover, in the two shards of
[`qx2_replay_plan.json`](receipts/valid7/qx2_replay_plan.json), each run staged by
`devtools.plan_valid7_replay stage` from the digest-checked retained checker and cover,
on 4-core cloud runners.
Each shard is two region-restricted runs with run V3’s settings, resumed from its own
record after interruptions; every attempt’s receipt is kept (`*_try2.log` to
`*_try4.log`).

- **Records:** [`qx2_shard01_1.jsonl.gz`](receipts/valid7/qx2_shard01_1.jsonl.gz),
  [`qx2_shard01_2.jsonl.gz`](receipts/valid7/qx2_shard01_2.jsonl.gz),
  [`qx2_shard02_1.jsonl.gz`](receipts/valid7/qx2_shard02_1.jsonl.gz) and
  [`qx2_shard02_2.jsonl.gz`](receipts/valid7/qx2_shard02_2.jsonl.gz), with a `.log`
  receipt for each run. Every run reports `VERIFIED-D4` with no uncertified box: 54,358
  boxes in all, the published count, and about 25.6 CPU-hours by the checker’s own count.
- **Comparison:** `devtools.plan_valid7_replay compare --checker qx2` on the four records
  ([`qx2_replay_compare.json`](receipts/valid7/qx2_replay_compare.json)): `ok`, every
  root recorded once, exactly the 9,800 published roots, and each root’s leaf list equal
  to run V3’s, 32,079 leaves.
- **The axis face:** Lemma Z, $\theta = 0$, is decided by the exact enumeration
  `qx2_zm.py axis`, which the fast `verify.sh` above re-ran identical to `lemmaZ.out`.

This is the source’s checker on the source’s cover, a same-implementation replay. It
discharges `Valid7` for this cover, the one hypothesis of the reduction built below, so
the two give `T-064`’s lower half. wand125’s independent checker was not replayed.

## Lean Build Here, 2 October 2026

`T-064`'s Lean reduction, `SquarePacking.Bentz.bentz_of_valid7 : Valid7 → ∀ k ≥ 6, minSide (k² − 3) = k`,
was built in this container.
`devtools.stage_evand_bentz_lean` staged the ten-module closure from retained bytes, each
file at its `08e8a5fa` Git blob; elan installed `leanprover/lean4:v4.33.1`, and Mathlib
came from `lake exe cache get` (8,690 files).

- **Build:** `lake build Sqpack.Bentz` finished with exit 0 and 8,715 jobs, no `sorry`,
  and linter warnings only (`open Classical`, deprecated `push_neg` and
  `Set.mem_setOf_eq`).
  Receipt: [`receipts/lean/build_bentz.log`](receipts/lean/build_bentz.log).
  The kept log is the final, successful run; the first modules show as `Replayed` because
  the two earlier runs had already built them.
- **Axioms:** `#print axioms` for `bentz_of_valid7`, `valid_of_valid7`,
  `box7Cover_measure`, `famCover_total` and `mass_shift` each print
  `[propext, Classical.choice, Quot.sound]`, which is what the source reports.
  Receipt: [`receipts/lean/axioms_bentz.log`](receipts/lean/axioms_bentz.log), from
  `AxiomsBentz.lean`, which also prints `Valid7`, `minSide` and `Packs`.
- **Memory:** `Sqpack/Bentz.lean` peaks above 13 GB resident.
  On this 16 GB host with no swap, the build was killed by the kernel twice (two threads,
  then one thread, exit 137 and −9).
  With a 10 GB swapfile and `LEAN_NUM_THREADS=1` it finished in 1,207 s wall.
  A host with at least 16 GB of free memory should not need swap.
  The killed runs' logs were not retained.
- **Scope:** this checks that the reduction's Lean source compiles against Mathlib and
  uses only the three standard axioms.
  It is the source's own Lean, so it is the same implementation as the source, not an
  independent statement of the theorem; `Valid7` remains a hypothesis.

## Compressed Files

Five `s60` files have more than 1,000 lines and were compressed locally with `gzip -9n`,
and so were three replay receipts of 2 October and the four `Valid7` shard records of 2
and 3 October, the rows whose origin is `receipt`, whose byte totals below exclude the
shard records:
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
| `receipts/s60_zmx2_full.log.gz` | receipt | `6cae3dd180d1eec4e088e0a05d953da86492a40d` | `f8843b53108141c626fcb7332fd3c8ca999dd182ac9090aa4712fe9f3286215c` |
| `receipts/s60_zmx2_d4_roots.log.gz` | receipt | `58a884336118da5db3253947e81dec54d1e71be0` | `58f90b89e220fa5ef623ae75a7b48e3bdfe8d6ce5e5181a8f8f96afd0342edf3` |
| `receipts/s60_zmx2_full_roots.log.gz` | receipt | `06fad9c541064734aff448a375d77d22363d1190` | `c3ed66ea3c1ee768f48a0e4e5281647907fb36e8ca81d4dd69d256621ecd26c7` |
| `receipts/valid7/qx2_shard01_1.jsonl.gz` | receipt | `06a8a0b0bd08c846ce5b4c6256837df93e7963a1` | `e81eafee58fbfd37c8b0ff90e9d7b868a6601f836a8846a27f1b8771b2d068e4` |
| `receipts/valid7/qx2_shard01_2.jsonl.gz` | receipt | `c405ead3f4e5902026e362464d1671faeab43ad2` | `0f548964a4891601cb083aba2f0cb00cf675a07105b07a2311d0bda88cdfbbae` |
| `receipts/valid7/qx2_shard02_1.jsonl.gz` | receipt | `28876588bbc146887d7ea62ac05a6ac05bf9a3e3` | `2bb8c407c0b4237ef9a9cdbaaa600bc224a1d41268e854cae1fba80f40044098` |
| `receipts/valid7/qx2_shard02_2.jsonl.gz` | receipt | `695eba8e753c2e542dcdf460504d2d9f5b8e374e` | `79e640b1e6066c1857cdc42fde7cd3edcc11a4ecec87214b28b9f13f25d4ee9d` |

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
