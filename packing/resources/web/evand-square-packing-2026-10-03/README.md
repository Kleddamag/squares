# Evan Daniel’s Square-Packing Repository at `2eb15455`, Pinned 2026-10-03

This packet retains the files of
[evand/square-packing](https://github.com/evand/square-packing) that
[jlevy/squares#316](https://github.com/jlevy/squares/issues/316) asks this record to
register: the `s12/certificates/k2m4/` bundle for $s(k^2 - 4) = k$ for every $k \ge 5$,
the run record of its finite premise, and the Lean closure of its reduction.

The claims are stated as the source states them.
What the frontier makes of them is decided in the frontier records, where the claim is
`T-081` (provisional until merged).

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

## Full Replay of `ValidTilt9`: Plan and Calibration, 3 October 2026

The run’s record carries every root’s CPU time: 815,343 s, 226.48 CPU-hours on the
source’s host.
[`devtools.plan_valid9_replay`](../../../devtools/plan_valid9_replay.py) prices the
replay from that record, splits it into shards, stages the digest-checked checker and
cover, and compares a sharded replay with the record root for root.
Nothing below is a replay of `ValidTilt9`; the coordinator launches the shards.

- [`receipts/valid9/qx2_calibration_x23-24_y16-17.log`](receipts/valid9/qx2_calibration_x23-24_y16-17.log)
  and
  [`qx2_calibration_x33-34_y22-23.log`](receipts/valid9/qx2_calibration_x33-34_y22-23.log):
  two centre cells near the mean cell cost, 8 roots each, run with the published
  settings on 4 processes.
  They took 931.9 CPU-s here against 802.9 s recorded, so the speed is 1.17 CPU-s here
  per recorded CPU-s, measured on a host loaded by other work.
  [`qx2_calibration_compare.json`](receipts/valid9/qx2_calibration_compare.json): `ok`,
  every leaf list of the 16 roots equal to the published one, 420 leaves.
- [`receipts/valid9/qx2_replay_plan.json`](receipts/valid9/qx2_replay_plan.json): 14
  shards of 4 cores, about 265 CPU-hours here.
  Each shard is at most three region-restricted runs.
  The wall bound is CPU / 4 plus three quarters of the largest root, summed over the
  shard’s runs.

| Shard | Cells | Priced CPU-h | Largest root (s) | Wall estimate (h) | Wall bound (h) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 704 | 16.27 | 1,799 | 4.76 | 5.52 |
| 2 | 320 | 16.39 | 1,359 | 4.79 | 5.58 |
| 3 | 80 | 16.15 | 1,980 | 4.72 | 5.70 |
| 4 | 13 | 16.10 | 4,196 | 4.71 | 5.73 |
| 5 | 40 | 15.55 | 2,247 | 4.55 | 5.42 |
| 6 | 46 | 16.02 | 2,180 | 4.69 | 5.61 |
| 7 | 82 | 16.46 | 1,675 | 4.81 | 5.81 |
| 8 | 90 | 15.99 | 1,679 | 4.68 | 5.70 |
| 9 | 58 | 16.39 | 1,619 | 4.79 | 5.57 |
| 10 | 78 | 16.25 | 1,694 | 4.75 | 5.68 |
| 11 | 93 | 16.42 | 1,227 | 4.80 | 5.68 |
| 12 | 137 | 16.45 | 1,319 | 4.81 | 5.60 |
| 13 | 164 | 16.19 | 1,293 | 4.74 | 5.36 |
| 14 | 120 | 15.85 | 1,160 | 4.64 | 5.20 |
| All | 2,025 | 226.48 | 4,196 | | |

The wall times assume speed 1.17. The Valid7 replay ran 13% above its record, against
1% for its calibration, so give each runner at least the bound.

**Runner procedure**, one shard per 4-core runner, from `packing/` on a fresh clone set
up as `AGENTS.md` describes:

1. Stage:
   `uv run --frozen --all-extras --group dev python -m devtools.plan_valid9_replay stage --work WORK`,
   which refuses any checker file or cover whose digest is not the record’s.
2. For each run of the shard in `qx2_replay_plan.json`, in order:
   `uv run --frozen --all-extras --group dev python -m devtools.replay_receipt --receipt <receipt> --cwd-label "work dir staged by plan_valid9_replay" --python-note "packing/.venv/bin/python3" --chdir WORK -- <command>`,
   with the command’s leading `python3` replaced by the absolute path of
   `packing/.venv/bin/python3`.
3. If a run is interrupted, run the same command again with the receipt renamed
   `<run>_try2.log`, `_try3.log` and so on; `--resume` skips every root already in its
   record. Keep every receipt.
4. When the shard’s runs end, each with `VERIFIED-D4` and no uncertified box, compress
   each record with `gzip -9n -k runs/<run>.jsonl` and commit the `.jsonl.gz` and `.log`
   files into `receipts/valid9/`.
5. When all 14 shards are in:
   `uv run --frozen --all-extras --group dev python -m devtools.plan_valid9_replay compare receipts/valid9/qx2_k008_shard*.jsonl.gz --json receipts/valid9/qx2_replay_compare.json`,
   which must report `ok`, 16,200 roots each recorded once, and every leaf list equal to
   the published one.

`stage --work WORK --s12` also stages the complete upstream `s12` tree at `WORK/s12`,
where `NPROC=4 sh certificates/k2m4/verify.sh --full` runs the bundle’s own unsharded
check, about 265 CPU-hours here.

## Lean Build Here, 3 October 2026

The reduction
`SquarePacking.Bentz4.bentz4_of_validTilt9 : ValidTilt9 → ∀ k ≥ 8, minSide (k² − 4) = k`
was built in this container from retained bytes.
[`devtools.stage_evand_bentz4_lean`](../../../devtools/stage_evand_bentz4_lean.py) staged
the sixteen-module closure of `Sqpack.ValidSplit9`, each file at its `2eb15455` Git blob
([`receipts/lean/bentz4_stage.json`](receipts/lean/bentz4_stage.json)). It regenerated
`Bentz4Data`, `ValidSplitData`, `BentzData` and `S32Data` with the source’s own
generators, each byte-identical to the retained module, and found no kernel-escape token
(`sorry`, `axiom`, `native_decide` and the rest).
Two inputs come from earlier packets at the same blobs: `L4_k02_family.txt` from the
October 1 packet and the $s(32)$ cover from the September 26 packet.
elan installed `leanprover/lean4:v4.33.1`, and Mathlib came from `lake exe cache get`
(8,690 files).

- **Build:** `lake build Sqpack.ValidSplit9` finished with exit 0 and 8,721 jobs, no
  `sorry`, and 13 linter or deprecation warnings only (`longLine`, `open Classical`,
  deprecated `push_neg` and `Set.mem_setOf_eq`). Wall 1,933 s.
  Receipt: [`receipts/lean/build_bentz4.log`](receipts/lean/build_bentz4.log).
- **Axioms:** `#print axioms` for `bentz4_of_validTilt9`, `valid9_of_tilt`,
  `valid9_of_tilt_axis`, `validAxis9`, `box9_grid`, `d4_box9`, `bentz4_of_valid9`,
  `box9Cover_measure`, `famCover_total4`, `ValidSplit.valid_of_tilt_axis` and
  `ValidSplit.validAxis_packed` each print `[propext, Classical.choice, Quot.sound]`.
  Receipt: [`receipts/lean/axioms_bentz4.log`](receipts/lean/axioms_bentz4.log), from
  the staged `AxiomsBentz4.lean`, which also prints `ValidTilt9`, `Valid9`, `minSide`
  and `Packs`.
- **Memory:** `Sqpack/Bentz.lean` again dominates, at 1,487 s and about 13 GB resident;
  with `LEAN_NUM_THREADS=1` and a 10 GB swapfile, up to about 9.6 GB of swap was in use,
  sampled every 20 s outside the receipt. On a 16 GB host without swap, plan for swap.
- **Scope:** the Lean source compiles against Mathlib and uses only the three standard
  axioms. `ValidTilt9`, the tilted part, stays a hypothesis; the axis face `validAxis9`
  and the D4 reduction are proved. It is the source’s own Lean, so this is the same
  implementation as the source, not an independent statement of the theorem.

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
