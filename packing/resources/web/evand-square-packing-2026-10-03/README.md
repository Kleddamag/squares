# Evan Daniel’s Square-Packing Repository at `2eb15455`, Pinned 2026-10-03

This packet retains the files of
[evand/square-packing](https://github.com/evand/square-packing) that
[jlevy/squares#316](https://github.com/jlevy/squares/issues/316) asks this record to
register: the `s12/certificates/k2m4/` bundle for $s(k^2 - 4) = k$ for every $k \ge 5$,
the run record of its finite premise, and the Lean closure of its reduction.

The claims are stated as the source states them.
What the frontier makes of them is decided in the frontier records, where the claim is
`T-080` (provisional until merged).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | [`2eb15455a6f178213287a84ab4d0576c060baabe`](https://github.com/evand/square-packing/tree/2eb15455a6f178213287a84ab4d0576c060baabe), tree `0315afb3`: “certificates/k2m4: s(k^2-4) = k for all k >= 5 …” |
| Committed | 2026-10-03T17:15:04Z, by Evan Daniel |
| Retrieved | 2026-10-03T17:33Z, a blobless clone checked out at the pin |
| Later `main` | `c321d35c`, eight minutes after the pin; its changes are to the site and `s12/README.md`, not to the bundle, the search scripts or the Lean |
| Licence | MIT, `s12/LICENSE` |
| Request | [jlevy/squares#316](https://github.com/jlevy/squares/issues/316), opened 2026-10-03T17:19Z |

**Credit and AI assistance.** `s12/CREDITS.md` is unchanged since the
[October 2 packet](../evand-square-packing-2026-10-02/README.md): the method is credited
to Burns and Massaccesi, and the work “was produced by Claude (Anthropic) in a single
session under human direction”. The bundle’s README credits wand125 with publishing
$s(77) = 9$ first, on 1 October.

## What Is Retained

The manifest ([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256))
covers 53 files, 2,516,215 bytes.
Fifty-two are retained under [`square-packing/`](square-packing/), byte-identical after
decompression; [`acquisition/declaration.json`](acquisition/declaration.json) lists the
scope.

| Upstream path | What it is |
| --- | --- |
| `s12/certificates/k2m4/` | The bundle: README, `verify.sh`, `SHA256SUMS`, the box cover `K4_k008_box9.txt`, the family, the exact LP solution, the four checker files under `qx2_zm/checker/`, the run log, `lemmaZ.out` and `germscan.out` |
| `s12/search/qx2_records.py`, `qx2_family_check.py`, `qx2_germscan.py` | The record, family and germ checks `verify.sh` runs |
| `s12/search/qx2_data/` | The box-9 cover and family, and the $k = 7$ cover `L4_k02_box7.txt`, which the Lean data generator also reads |
| `s12/search/K2M4_MARGIN.md`, `QUADRANT_EXACT.md`, `ZM_MIXED.md` | How the family was found, and the paper proofs of the checker’s primitives |
| `s12/notes/lean-k2m4-reduction.md`, `lean-valid-split.md` | The Lean write-ups |
| `s12/lean/` | The toolchain and lake files, `Axioms.lean`, the sixteen modules in the import closure of `ValidSplit9.lean`, and the four data generators |
| `s12/certificates/s21/FORMAT.md` | The mixed cover format |
| `s12/README.md`, `CREDITS.md`, `LICENSE` | The repository’s own statement of its results, credits and licence |

The four checker files are byte-identical to the `k2m3` copies the
[October 1 packet](../evand-square-packing-2026-10-01/README.md) retains, the code that
`T-064`’s Valid7 replay ran: `qx2_zm.py` `6294052a…`, `zm_mixed.py` `1fd20346…`,
`zeromargin.py` `640fe453…` and `mixed_cover.py` `bb89de15…`.

**The run record.** The upstream `qx2_zm/run_k4x_k008_leaves.jsonl.gz` is pinned by
digest only, because the archive reads every stored `.gz` as this repository’s
compression of the file beside it.
It is retained at [`record/run_k4x_k008_leaves.jsonl.gz`](record/), made by
`devtools.retained_data compress` from the decompressed record, and that file is the
upstream file byte for byte: SHA-256
`e8f1f2bff3a5d8ca4c75dd2c689439aa6453b1f6741931c54000d023a03e43dd`, the bundle’s
`SHA256SUMS` line, because the source made it with `gzip -9n` too.
Decompressed it is 16,201 lines, a header and one line per root.

## Checks Here, 3 October 2026

- [`receipts/k2m4_verify_fast.log`](receipts/k2m4_verify_fast.log): the bundle’s fast
  `verify.sh` on a staging of this packet, `square-packing/s12` with its `.gz` files
  decompressed and the record at its upstream path, under the project’s CPython 3.14.7.
  Exit 0 in 18 s.
  It checked the bundle’s eleven hashes; the cover’s exact total
  $3835229774429/50000000000 = 76.7046 < 77$ and its D4 invariance, by the source’s own
  parser; the family rebuilding the cover’s 2,076 segments exactly, with
  $D = 214770225571/200000000000$; Lemma Z, 1,600 one-sided limit corners with minimum
  exactly 1, identical to the shipped `lemmaZ.out`; the record’s header digests,
  settings, the 16,200 roots each once, 115,268 leaves, coverage with the 3,043
  `clip_bin` slabs to the exact volume $81/8$, and the census against the run log; and
  `Bentz4Data.lean` regenerated identical.
  It recomputes no tilted leaf, so it is a diagnostic and not a replay of `ValidTilt9`.

## Replay Plan

Pending: the full `qx2_zm.py` replay’s shard plan is written by
`devtools.plan_valid9_replay`.

## Lean Build

Pending.

## Compressed Files

Three files of more than 1,000 lines are stored as deterministic `gzip -9n`. Each row
gives the Git blob and SHA-256 of the decompressed bytes, as `devtools.retained_data`
produces them.
The upstream file of the third is itself `gzip -9n` of the same bytes, so the stored
file and the upstream `.gz` are identical.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing/s12/certificates/k2m4/K4_k008_box9.txt.gz` | upstream | `cb803ebb08c3271301bc11e483aa4e377199d4be` | `4151d7c4059d5dcf56130c9373e6b5b60635e1a4250f46562d7ecc4d64a27801` |
| `square-packing/s12/search/qx2_data/K4_k008_box9.txt.gz` | upstream | `cb803ebb08c3271301bc11e483aa4e377199d4be` | `4151d7c4059d5dcf56130c9373e6b5b60635e1a4250f46562d7ecc4d64a27801` |
| `record/run_k4x_k008_leaves.jsonl.gz` | upstream | `2db26c51f24d1146bdbd653e3a1aa93f3eebdfcc` | `7a8d5ad493c15a5d26d04d682e102e1c7864848784f75afe7bc1e6411c0f128b` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
