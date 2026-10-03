# Evan Daniel’s Square-Packing Repository at `7d6f46d9`, Pinned 2026-10-02

This packet retains the files of
[evand/square-packing](https://github.com/evand/square-packing) that Evan Daniel’s
[comment of 2 October on jlevy/squares#238](https://github.com/jlevy/squares/issues/238)
points to, at the `main` of that morning:

- **his replay of wand125’s point-only cover for $s(61) = 8$**,
  `s12/search/s61_wand125/` and `s12/search/S61_WAND125_REPLAY.md`;
- **Lemma 2 of the clique family kernel-checked in Lean**,
  `s12/lean/Sqpack/AnchorLemma2.lean`, with the note it repairs;
- **the `dual_exact.py` fixes** and the two side-3.99 supports it now publishes; and
- **the claims audit and the Nagamochi gap** of commits `6383ad8`, `4e11002` and
  `9ff4866`, in the files they changed that bear on this record’s claims.

Nothing here was replayed.
The claims below are stated as the source states them; what the frontier makes of them
is decided in the frontier records.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | [`7d6f46d9d0780241245dfbf77bad28aa1594c6b5`](https://github.com/evand/square-packing/tree/7d6f46d9d0780241245dfbf77bad28aa1594c6b5), `main` when fetched, tree `1694f28e`: “Merge Lean attainment: s(n) is a minimum for n >= 1 …” |
| Committed | 2026-10-02T01:10:42Z, by Evan Daniel; 14 commits after the [October 1 packet’s](../evand-square-packing-2026-10-01/README.md) pin `08e8a5fa` |
| Retrieved | 2026-10-02T07:44Z, a blobless clone with a sparse checkout of the declared paths |
| Licence | MIT; `s12/LICENSE` is byte-identical to the October 1 packet’s copy |
| Request | [jlevy/squares#238](https://github.com/jlevy/squares/issues/238), the comment of 2026-10-02T01:03Z |

**Credit and AI assistance.** `s12/CREDITS.md` still says the work “was produced by
Claude (Anthropic) in a single session under human direction”.
The one change since the October 1 pin adds to its Nagamochi entry that Lemma 1 is
false, so the published proofs of the rectangle bound and its consequences are
incomplete, and that none of the source’s results uses that lemma.

## What Is Retained

The manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)) covers 33
files, 1,328,506 bytes.
Twenty-nine are retained under [`square-packing/`](square-packing/), byte-identical
after decompression.

| Upstream path | What it is |
| --- | --- |
| `s12/search/S61_WAND125_REPLAY.md` | The replay’s write-up |
| `s12/search/s61_wand125/` | The cover (`s61_wand125_cover_8.txt`, stored as `.gz`), the run records of `zeromargin.py`, `zmcheck` and `zmx2` (the source’s own `.xz` files), the float scan, and two helper scripts |
| `s12/lean/Sqpack/AnchorLemma2.lean` | `anchor_lemma2`, `anchor_lemma2_sharp`, `anchor_lemma2_iff` |
| `s12/notes/clique-family.md` | Lemma 2’s erratum and repaired proof |
| `s12/search/dual_exact.py`, `DUAL_EXACT.md` | The fixed checker and its write-up |
| `s12/search/dual_exact_3.99_support.txt`, `cqx_PURE99_support.txt` | The two side-3.99 supports |
| `s12/certificates/k2m3/README.md`, `verify.sh` | The claims audit’s scope statements for T-064’s bundle |
| `s12/certificates/s21/FORMAT.md` | Its checker-independence wording |
| `site/notes/lower-bounds-notes.md` | The Nagamochi gap and the $n = 17$ entries |
| `s12/README.md`, `s12/CREDITS.md` | The repository’s own statement of its results and credits |

**Pinned by digest only**, because another packet already holds the same bytes:

| Upstream path | Bytes | SHA-256 | Retained copy |
| --- | ---: | --- | --- |
| `s12/search/zm_mixed.py` | 86,265 | `1fd203469bb43a55ca7ce376b9717437e0970eead31941ec7fa100ab24d5ba95` | [October 1 packet](../evand-square-packing-2026-10-01/source/s12/search/zm_mixed.py) |
| `s12/search/s61_wand125/MANIFEST.txt` | 3,545 | `bd584efe835af84d…` | [October 1 packet](../evand-square-packing-2026-10-01/source/s12/search/s61_wand125/MANIFEST.txt) |
| `s12/search/s61_wand125/zeromargin_d4/checker/zeromargin.py` | 79,383 | `640fe453c1a32f4a…` | [September 26 packet](../evand-square-packing-2026-09-26/square-packing/s12/search/zeromargin.py) |
| `s12/LICENSE` | 1,068 | `c51886c0f7e6724a…` | [October 1 packet](../evand-square-packing-2026-10-01/source/s12/LICENSE) |

`zm_mixed.py` at `1fd20346` is the version the source re-pinned its $s(21)$, $s(45)$ and
$s(60)$ bundles to on 30 September (commit `37b2ac2`, “census identical root for root”).
It differs from the `b91d70b6` copy the
[September 28 packet](../evand-square-packing-2026-09-28/square-packing/s12/search/zm_mixed.py)
retains (`ee3e2915…`), the one wand125’s $s(59)$ and $s(77)$ bundles require, by one
added line, 860:

```python
    if u0 >= u1: return None            # zero-width bin: no sub-bin is examined, so 'EMPTY' would be unproved (audit B1)
```

From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-square-packing-2026-10-02 --check`
re-derives the packet from its manifest.

## The $s(61)$ Point-Only Replay

**The files predate this pin.** `s12/search/s61_wand125/` is Git tree `6ca22d81` and
`S61_WAND125_REPLAY.md` blob `b6f57d2c` at both `08e8a5fa` and `7d6f46d9`; the replay
was committed on 2026-10-01T03:20Z (`551f2c7`). The October 1 packet retained only
`MANIFEST.txt` from it.

**The claim, as the source states it.** wand125’s D4-invariant point measure on
$[0,8]^2$, 15,193 points of total $8584985072679551 / 2^{47} = 60.99998780\ldots < 61$,
is certified by two of Daniel’s separately written exact point checkers: `zeromargin.py`
certifies all 12,800 roots of the D4 region (two of them only after a depth-30 rerun),
and `zmcheck --d4` with the opt-in branch order `ZM_MIXPAIR=1` all 6,400, 0 uncertified.
With its default order `zmcheck` stalled at interior tile germs and was stopped.
`zmx2 --d4` reproduces wand125’s box count, 800,042, and `zmx2 --full --sym-atoms` is
clean over the unreduced region; the source calls these a reproduction, not a third
independent check, because `zmx2`’s author read `zeromargin.py`. About 4.8 CPU-hours in
all.

**Facts checked here.**

- The retained cover is wand125’s `point_n61_L8/cover.txt` byte for byte: both are Git
  blob `cb6797c8`, at wand125/square-packing-bounds `f8846cec` (committed
  2026-09-30T01:34:53Z, unchanged on that repository’s `main` since), in a local clone
  of it. SHA-256 `bcb66c79…`, as `MANIFEST.txt` records.
- Every checker `MANIFEST.txt` names is already retained here byte for byte:
  `zeromargin.py` `640fe453…`, `zm_d4_sweep.py` `cc7fa8c7…` and `verify2/src/main.rs`
  (`zmcheck`) `94b7d83e…` in the
  [September 26 packet](../evand-square-packing-2026-09-26/README.md), and `zmx2.rs`
  `92a4cfe8…` in the
  [`zmx2 --sym-atoms` packet](../evand-zmx2-sym-atoms-2026-09-30/README.md).

## What the Claims Audit Says About Claims This Record Holds

Read in the commits, not replayed.

- **T-064’s fast check is structure only.** The k2m3 `README.md` and `verify.sh` now say
  that the fast `verify.sh` and `qx2_records.py` check hashes, structure and coverage
  but recompute no positive-tilt leaf; only `verify.sh --full`, the same program, does.
  The Lean `bentz_of_valid7` is stated as conditional on Valid7. A partial second
  implementation, `zmx2` with area density, certifies $\theta = 0$ and $\theta \ge
  0.014°$ but leaves 120 D4 boxes open at $0 < \theta < 0.01°$. None of this contradicts
  T-064 as registered, which already says the tilted part rests on one checker.
- **New corollary, not registered:** $s(k^2 - 2) = k$ for every $k \ge 2$ without
  Nagamochi’s Lemma 1, by monotonicity from $s(k^2 - 3) = k$, for $k \ge 9$ resting on
  T-064’s single-checker certificate alone.
  The bounds notes say the source does not carry it in its own data either.
- **Checker independence restated.** `zm_mixed.py` and `zmx2`, and `zeromargin.py` and
  `zmcheck`, are now “separately written”: they share no code but share the point-test
  formulation of `zeromargin.py`’s write-up, and `zm_mixed.py` calls `zeromargin.py`.
  The $s(60)$ and k2m3 certificates share `zm_mixed.py`’s piece bounds.
  The register’s E-n060 evidence already records the shared trust boundary.
- **Nagamochi 2005 has a proof gap.** Lemma 1 is false (chelokot’s Lean counterexample;
  Karakuş, arXiv:2609.37410), so the published proofs of Theorem 2’s families and
  general bound are incomplete; the source marks every such entry `gap` and moves its
  `best`. This reaches T-007, already reviewed for it in
  [jlevy/squares#305](https://github.com/jlevy/squares/pull/305) on
  [#295](https://github.com/jlevy/squares/issues/295); this packet adds a dated second
  statement of it.
- **$n = 17$ reports**, as `reported` only: Kleddamag 4.6601, Guzhou0806 R070 and R071.
  The source keeps R068, this record’s replayed floor, as its best.

## What a Replay Here Would Need

Every input is now in the archive: the cover in this packet, the checkers in the
September 26 and `--sym-atoms` packets.
The cheapest full replay is wand125’s own `verify.sh` of `point_n61_L8/` with its clone
replaced: `zmx2.rs` `6b7f0f79…`, which it requires and the
[September 28 packet](../evand-square-packing-2026-09-28/README.md) retains, then
`zmx2 d4` and `zmx2 cert --d4 --pair-points`, about 0.13 CPU-hours at the source.
wand125’s `check_cover.py` and `verify.sh` are not retained here; a wand125 packet at
`f8846cec` would hold them.
Daniel’s two independent routes cost about 0.85 CPU-hours (`zeromargin.py` through
`zm_d4_sweep.py`, depth 24 then 30 on two roots) and 1.07 (`zmcheck --d4` with
`ZM_MIXPAIR=1`), and his records here let either be compared root for root.
Two mutated covers refused by each checker would be the controls.

## Compressed Files

One upstream file of more than 1,000 lines is stored as deterministic `gzip -9n`. The
row gives the Git blob and SHA-256 of the decompressed bytes, as
`devtools.retained_data` produces them.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing/s12/search/s61_wand125/s61_wand125_cover_8.txt.gz` | upstream | `cb6797c87930f8bcb57618e74a19ed0d2a19dded` | `bcb66c7910ef844ce8d39c423d7a5a419bd530a344689331f7665ba6971d0374` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
