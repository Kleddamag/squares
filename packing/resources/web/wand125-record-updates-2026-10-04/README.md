# wand125 Certificate-Record Updates of 4 October 2026, Pinned at `797bdf6`

This packet retains four updates that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) made on
4 October 2026 to certificates this record already holds, each changing the records,
logs or scripts around a certificate and not the certificate itself. Each answers review
points of this project; three name [jlevy/squares#279](https://github.com/jlevy/squares/issues/279)
and [#280](https://github.com/jlevy/squares/issues/280). None is a new claim, so each is
recorded as an evidence update on the entry it concerns and moves no rung.
Its proposed Frontier key is **[wand125 record updates 2026-10-04]**.

| Commit | Committed (UTC) | Directory | Register entry | What changed |
| --- | --- | --- | --- | --- |
| `c56b9b7a` | 2026-10-04T01:42:52Z | `certificates/k2m5_n59_L8` | T-066, $s(59) = 8$ | The zm_mixed.py per-root records (every root at depth 24, the root R at depth 34) with `check_records.py`, which checks them in exact rational arithmetic and which `verify.sh` now runs; the zmx2 per-root logs, a toolchain record and the run logs; `SHA256SUMS` listing exactly the published files. The source’s answer to the 2 October review’s findings F1 and F2 |
| `1ebd4845` | 2026-10-04T06:48:52Z | `point_n45_L7` | T-054, $s(45) = 7$ | `verify.sh` judges D4 invariance from zmx2’s `D4: measure invariant` line (the earlier check also accepted its “not D4-invariant” message), runs under `set -euo pipefail` and writes `toolchain.txt`; `reference/` holds the original reference run, which a fresh per-root log is compared with |
| `3f063bd5` | 2026-10-04T08:04:06Z | `certificates/k2m4_n77_L9` | T-067, $s(77) = 9$ | The run logs and a full replay record ending `N77_COVER_VERIFIED`; `verify.sh` hardened as for $n = 45$ and run with `--resume`; `SHA256SUMS` listing exactly the tracked files. The answer to finding F2 |
| `781afb3b` | 2026-10-04T10:49:48Z | `point_n21_L5` | T-055, $s(21) = 5$ | Absolute machine paths removed from the records in the archive and from the two acceptance linkage files, with their embedded hashes updated and `path-relativization-map.json` listing each edited file’s digest before and after; English status messages in `mixed_proof_pipeline.py`, which is not on the checking path; `lemma-code-map.json` listing the 27 files the checking path runs. The source reports a fresh replay of the rebuilt archive ending `FRESH_ALL_DOMAIN_REPLAY_VERIFIED` |

Each commit message says the cover or certificate is unchanged, and the three covers
pinned here are byte-identical to the copies the earlier packets retain. What was checked
here is digests and Git blob ids. None of the new records or scripts has been run here.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `797bdf6e10eba5f9dccca9da06f8352e81ba9dde`, branch `main`, tree `2f4a2d442ea6c8568f8bd2f6a4a9f5b483157d37`; the head when retrieved, the pin of the [evening packet](../wand125-mixed-bounds-evening-2026-10-04/README.md) as well, and unchanged in the four directories since each commit above |
| Committed | 2026-10-04T19:03:58Z |
| Licence | MIT. The root `LICENSE` reads “Copyright (c) 2026 wand125” |
| Retrieved | 2026-10-05, about 00:44Z: a blobless clone of the whole history, checked out sparsely at this revision |
| Pinned subtree | 57 files, 18,543,921 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 45 files, 1,106,276 bytes upstream, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |

**Scope.** The directories of the $s(59)$ and $s(77)$ covers and of the $s(45)$ point
cover are pinned whole. For `point_n21_L5`, a 468 MB directory, the scope is the 17 files
`781afb3b` changed other than its 14 bundle parts, which together are 455 MB: the retained
`archive-index.json` and `distribution.json` list each part with its size and SHA-256, and
the commit pins them. A replay of the rebuilt archive would fetch them by Git.

## Credit and AI Assistance, as the Source States Them

The root README’s Attribution section opens “The method is not ours.”, and its Status
section says “Parts of this work were produced with AI assistance under human
direction.” Each of the four commit messages ends with a co-author trailer naming an AI
assistant. The $s(59)$, $s(77)$ and $s(45)$ covers extend Evan Daniel’s covers and are
checked with his zmx2 and zm_mixed.py, as the earlier packets record.

## What Is Retained

Everything in the scope but the files below is retained byte-identical at its upstream
path. Pinned by digest only:

| Upstream path | Bytes | SHA-256 |
| --- | ---: | --- |
| `certificates/k2m4_n77_L9/n77_mixed_cover_9.txt` | 845,159 | `47b57cfe38cbfdbcf5320e59caffe712f4ef32df8aad42b0d7f697de6d26cdd7` |
| `certificates/k2m4_n77_L9/record/zm_mixed_roots.jsonl.gz` | 2,015,971 | `cf0efa1c7c65ceb1e2e021d6c17f10a27a5f1ad91581e1543a1ec51137549fb9` |
| `certificates/k2m4_n77_L9/record/zmx2_d4_roots.txt.gz` | 91,231 | `25b17101fe3d1be27d27d11ab0399fb1bf644873d7f933283be4d2bc2277d5c9` |
| `certificates/k2m4_n77_L9/record/zmx2_full_roots.txt.gz` | 758,108 | `2c4e694a795e51a8b28252ef46f75ebb338b3ce22dd021c1d6d36cbd908b1d58` |
| `certificates/k2m5_n59_L8/n59_mixed_cover_8.txt` | 552,155 | `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19` |
| `certificates/k2m5_n59_L8/zm_mixed_d4/roots.jsonl.gz` | 1,654,112 | `eac7061c693760a62d7fb45216e98cc66842f98dafc5e65431e277fd751a7fae` |
| `certificates/k2m5_n59_L8/zmx2_d4/roots_log.txt.gz` | 64,274 | `c7279174cd72a9ba016ce7cefa93804d877b94c444e268a7edd70d6ad1289b6f` |
| `certificates/k2m5_n59_L8/zmx2_full/roots_log.txt.gz` | 537,423 | `1f2bfa796ab5a1c18dfc4274f62da1e55c5218d5a3cf17b073edbb623132231d` |
| `point_n21_L5/acceptance/m1-full-linkage.json.gz` | 5,302,637 | `a8862552946a906799b53aa9035883ac02b7f9a820ffcdb0868c909125b00562` |
| `point_n21_L5/acceptance/split-linkage.json.gz` | 5,314,372 | `e83b8042fa77e0aba95782b07da7143ac8e4c794648d71b7b5bea63b3b0c52f7` |
| `point_n45_L7/check_cover.py` | 1,223 | `bca2bf4c059acfca0ebc009bd1cad8e87a9e10564aaa972b96c9212059592530` |
| `point_n45_L7/cover.txt` | 300,980 | `f7d706aa07506c351d9c4b76082cc391ae3f1fd20f6759496bd7c601bb0ca192` |

Each `.gz` file is the source’s own gzip, which the archive cannot keep beside its own
compression. The covers and `check_cover.py` are byte-identical to the copies the
[1 October packet](../wand125-point-and-mixed-2026-10-01/README.md) and the
[28 September packet](../wand125-point-and-mixed-2026-09-28/README.md) retain, which the
acquisition check compares.

From `packing/`,

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  wand125-record-updates-2026-10-04 --checkout CHECKOUT
```

rebuilds the retained files and both acquisition files from a checkout at the pinned
revision, and with `--check` in place of `--checkout CHECKOUT` re-derives the packet from
its manifest without one.

## Limitations

- **Nothing here was run.** `check_records.py`, the new `verify.sh` scripts and the
  source’s replay records are retained and not executed; each entry’s rungs rest on the
  replays already recorded.
- **The $s(21)$ archive changed.** The replay recorded for T-055 is of the archive at
  `39d8ecc7`; the rebuilt parts have other digests, and the source’s fresh replay of them
  was not checked here.
- **The $s(45)$ D4 check.** The bug `1ebd4845` fixes did not affect the replay recorded
  for T-054: zmx2 printed `VERIFIED-D4` at every root, and
  `devtools.audit_wand125_point_and_mixed` checks the cover’s D4 invariance exactly.

## Compressed Files

The upstream data files of more than 1,000 lines are stored as deterministic gzip made by
`gzip -9n`, with no file name or timestamp in the header. The table gives the Git blob and
SHA-256 of the decompressed bytes, which are the file’s blob and digest at the pinned
commit. `python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/k2m4_n77_L9/record/zm_mixed_run.txt.gz` | upstream | `e7718f11392fda81a27f6e288b4e6e67da91e996` | `1e1be79c23d980497314d0dfb46e7e9b56d93e97a9244d844f2eda5a5dd7db81` |
| `square-packing-bounds/certificates/k2m4_n77_L9/record/zmx2_full_run.txt.gz` | upstream | `8cfe6bb63d82a70606e6cd4a7599c92adb5a96d0` | `f3f09458a48f6e8998f59c0e649c51bb9f03390f1cbf8a0ddf85a124d11ba237` |
| `square-packing-bounds/certificates/k2m4_n77_L9/zm_mixed_d4/run.txt.gz` | upstream | `8452dbb0156793514ba16889b9b33fb541ea9138` | `f9ce073f1e6733682c4f128d6da72062eb869d16b0f16b7b853805acf02647b9` |
| `square-packing-bounds/certificates/k2m4_n77_L9/zmx2_full/run.txt.gz` | upstream | `2555980528a7595898c71c3f3fef90f962b5af60` | `d0d747ca1d2e81d30333cc6eac5e00e8c2127cfc237d2f4801dbb1b22887fcab` |
| `square-packing-bounds/certificates/k2m5_n59_L8/zmx2_full/run_log.txt.gz` | upstream | `fe29b9b850c78a029989e85c6f9ff22155d5632a` | `fd3bde7f07cb484d978e19afc7cb267fd623d6d1997e62f74ec436c94bee58fd` |
| `square-packing-bounds/point_n45_L7/reference/roots.txt.gz` | upstream | `af44f2f5e1154b063f79c977fb3dfbfaa6c925fb` | `a353a0ca945241f2f6dc46bb3d5b2beb91720b42ba7b9637620b280d66df746b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
