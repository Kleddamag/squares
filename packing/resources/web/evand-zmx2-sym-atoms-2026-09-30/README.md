# Evan Daniel’s `zmx2` at the `--sym-atoms` Commit, Pinned 2026-09-30

This packet retains the version of Evan Daniel’s interval checker `zmx2` that made the
$s(32)$ run without the D4 fold, which Daniel reported in his
[comment of 1 October on jlevy/squares#238](https://github.com/jlevy/squares/issues/238#issuecomment-5923097530).
The run’s records are in the
[October 1 evand packet](../evand-square-packing-2026-10-01/README.md) under
`source/s12/certificates/s32/zmx2_full_sym/`. Its manifest names this checker by Git HEAD
`e4af291c` and `zmx2.rs` SHA-256 `92a4cfe8…`, a version that was in no packet here; the
[review of the run](../../../../docs/project/reviews/review-2026-10-02-evand-s32-no-fold-run.md)
recorded that as its finding F1, and this packet is its remedy.
It holds one subject, the checker, and replays nothing.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Revision | [`e4af291cf52711a3ef7cedfea262f001fa2cafe1`](https://github.com/evand/square-packing/tree/e4af291cf52711a3ef7cedfea262f001fa2cafe1), “zmx2: --sym-atoms (opt-in): also bound each box with the mirrored atom assignment …” |
| Committed | 2026-09-30T23:45:14Z, by Evan Daniel |
| Retrieved | 2026-10-02T04:50Z, from a blobless clone with a sparse checkout of the declared paths |
| Licence and credit | MIT; the source’s `s12/LICENSE` and `s12/CREDITS.md` are retained unmodified in the [October 1 evand packet](../evand-square-packing-2026-10-01/README.md), where its credit and AI-assistance statements are recorded |
| Request | [jlevy/squares#238](https://github.com/jlevy/squares/issues/238), the comment of 2026-10-01 |

## What Is Retained

| Upstream path | Bytes | SHA-256 | Note |
| --- | ---: | --- | --- |
| `s12/verify2/src/bin/zmx2.rs` | 77,198 | `92a4cfe87b4e33d57ce132c9c517eded3fe62b4a5a2151b5ba250b8ee329fe64` | The checker the run’s manifest names; Git blob `8ce809d6` |
| `s12/search/zmx2_sym_run.sh` | 2,940 | `843286a0459c6ad1d064bbfb22966fb27ae6ebbadc4579dc17254a566013486a` | The script the run’s manifest says wrote it |

Pinned by digest only, because the
[September 26 evand packet](../evand-square-packing-2026-09-26/README.md) retains the
same bytes: `s12/verify2/Cargo.toml` (`4e0f078e…`), `s12/verify2/Cargo.lock`
(`e1daec4d…`) and `s12/verify2/src/main.rs` (`94b7d83e…`). With them the crate builds as
it did at the source.
Lemma A, which `--sym-atoms` implements, is written up in §4.9 of `search/ZMX2.md` at
the October 1 evand packet’s later pin, `08e8a5fa`; the copy at this revision predates
that section and is not retained.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope, and
[`acquisition/sources.json`](acquisition/sources.json) and
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) record the
pin and every file’s digest. From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-zmx2-sym-atoms-2026-09-30 --check`
re-derives the packet from its manifest.

## Replay Here, 2 October 2026

This checker, built from the retained `zmx2.rs` with the crate files of the September 26
packet (rustc 1.97.0; [`zmx2_92a4cfe8_build.log`](receipts/zmx2_92a4cfe8_build.log)),
replayed the source’s run on the retained cover as stage 4 of the
[result import](../../../campaign/result-import.md):
`zmx2 cert s32_closed_cover_6.txt --full --pair-points --sym-atoms --threads 3` on a
4-core x86-64 Linux container, with its receipts written by `devtools.replay_receipt`.

- **Two receipts, one sweep.** A container restart stopped the first run after 6,173
  roots, so [`s32_zmx2_full_sym.log`](receipts/s32_zmx2_full_sym.log) has no closing
  line. `zmx2` resumes from its own root log, and
  [`s32_zmx2_full_sym_resume.log`](receipts/s32_zmx2_full_sym_resume.log) ran the other
  22,627 roots: `VERIFIED` for the unreduced sweep, 28,800 roots, 11,268,760 boxes, none
  uncertified, maximum depth 29, in 7,186 s of wall and 18,386 CPU-s.
- **The audit** by `devtools.audit_evand_mixed_covers` finds the joined root log
  covering the region once per root with no uncertified or capped box, the header’s
  atoms `pairpts+sym` as required
  ([`s32_zmx2_full_sym_audit.json`](receipts/s32_zmx2_full_sym_audit.json)), and every
  one of the 28,800 roots identical to the source’s `roots.log.xz`, with identical
  headers ([`s32_zmx2_full_sym_compare.json`](receipts/s32_zmx2_full_sym_compare.json)).
  The box, certified and empty totals equal the source manifest’s.
- **Controls.** The same checker refuses two mutated copies of the cover on the root
  where each loss shows; the receipts are in [`receipts/controls/`](receipts/controls/),
  held by `packing/tests/test_replay_controls.py`.

## Compressed Files

One replay receipt of more than 1,000 lines is stored as deterministic `gzip -9n`. The
row gives the Git blob and SHA-256 of the decompressed bytes, as
`devtools.retained_data` produces them.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/s32_zmx2_full_sym_roots.log.gz` | receipt | `0122534263e2af09d2a7d734dcaf2d001f87db3d` | `f365bd82df96822bfe66d963f5ca7fbaccebc8c0ca6e9e13f99480de83aaff4f` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
