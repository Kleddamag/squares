# Evan Daniel’s October 2026 Square-Packing Source Packet

This partial packet retains source bytes for the
[October 1 source-coverage review](../../../../docs/project/reviews/review-2026-10-01-evand-source-coverage.md).
It does not contain a complete clone or a complete proof replay.
The new claims are `s(60) = 8` and `s(k² − 3) = k` for every integer `k ≥ 6`; the latter
rests on the single exact `Valid7` checker plus a conditional Lean reduction.
The retained dual notes and supports provide context for research on `s(12)` and
`s(21)`.

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
The upstream
[`runV3_6294052a_leaves.jsonl.gz`](source/s12/certificates/k2m3/qx2_zm/runV3_6294052a_leaves.jsonl.gz)
was already compressed and is retained byte for byte.
No source file was edited to make this packet.

The retained sources include the live [Proofs](source/site/www/proofs.html) and
[Sources](source/site/www/sources.html) HTML, the two new write-ups, the `k2m3`
certificate files and frozen checker, the `s60` cover and README, and the Lean reduction
and data. For adjacent research it includes
[`FRIEDMAN.md`](source/s12/search/FRIEDMAN.md),
[`QUADRANT_EXACT.md`](source/s12/search/QUADRANT_EXACT.md),
[`CLIQUE_CONTINUUM.md`](source/s12/search/CLIQUE_CONTINUUM.md), the side-4 and side-5
exact dual supports and their checker, and selected `s(12)` negative-route notes.
The full retained file list, rather than this summary, defines the packet’s scope.

## Unretained Inputs and Verification Scope

- The `s60` bundle’s 30,932,080-byte `zm_mixed_d4/roots.jsonl`, its `zmx2_d4` and
  `zmx2_full` root logs, and their run manifests are not in this packet.
  The pinned
  [source bundle](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s60)
  is the retrieval point for a full replay.
  The verifier’s shared Python checker and record-parser sources are retained at their
  upstream `source/s12/search/` paths.
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
retained files. For the compressed `s60` cover, compare the decompressed bytes with the
manifest blob using `gzip -dc` and `git hash-object --stdin`. A future certificate
replay should use the exact upstream commit and record its own commands, environment and
outputs in a separate receipt.

## Compressed Files

The `s60` cover has more than 1,000 lines and was compressed locally with `gzip -9n`.
The row gives the Git blob and SHA-256 of its decompressed upstream bytes, as produced
by `devtools.retained_data.describe`.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `source/s12/certificates/s60/s60_mixed_cover_8.txt.gz` | upstream | `abf6acbbe24db7941bd2b6e7bb935700fe1931f1` | `2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41` |

The upstream `k2m3/qx2_zm/runV3_6294052a_leaves.jsonl.gz` was already a gzip file.
It retains the source’s filename and timestamp header and is stored here verbatim.
Its *compressed* bytes match the raw Git blob in the source manifest.
The generic `retained_data.check_packet` gate assumes every `.gz` in a packet was made
locally with a deterministic header, so that gate does not apply to this mixed packet.
The focused source-manifest test checks both files with the appropriate byte
interpretation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
