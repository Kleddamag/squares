# wand125 Point-Only Cover for s(61) = 8, Pinned 2026-09-30

This packet pins one directory of
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds), the
point-only cover `point_n61_L8`, at the commit that added it.
The source states that it proves $s(61) = 8$ by a route that uses points only, and says
the value already follows from Evan Daniel’s $s(60) = 8$.
The packet was asked for in
[a comment on jlevy/squares#238](https://github.com/jlevy/squares/issues/238) of 2 October
2026, in which Daniel reports certifying the cover with his own checkers; his records are
in the [October 2 evand packet](../evand-square-packing-2026-10-02/README.md).
Its proposed Frontier key is **[wand125 point n61 2026-09-30]**.

This repository replayed the cover with `zmx2`, the checker the source’s own `verify.sh`
runs, and the replay passed. The receipts are in [`receipts/`](receipts/).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds> |
| Revision | `f8846cec9661773dbd0cc7cbeee7d01ddb12a2b8`, tree `4e76cfc46278341b2257eab527d1608b35ac1c9a`: “Point-only certificate for s(61) = 8” |
| Committed | 2026-09-30T01:34:53Z (10:34 on 30 September by the author’s clock) |
| Licence | MIT, “Copyright (c) 2026 wand125”; the root `LICENSE` is byte-identical to the [September 27 packet’s copy](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE) |
| Retrieved | 2026-10-02T17:37Z: a blob-filtered clone of `main`, checked out sparse at this revision over the root `README.md` and `LICENSE` and the claim directory |
| Pinned subtree | 7 files, 416,232 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256); the rest of the tree is pinned by the commit alone |
| Retained here | 6 files, 415,168 bytes, under [`square-packing-bounds/`](square-packing-bounds/), byte-identical to the pinned files after decompression |
| Request | [jlevy/squares#238](https://github.com/jlevy/squares/issues/238), the comment of 2026-10-02 |

The packet holds one revision. The October 1 [wand125 packet](../wand125-point-and-mixed-2026-10-01/README.md)
pins the root README of a later revision (`1a25a5ed`), which links this directory but
retains none of it.

## Credit and AI Assistance, as the Source States Them

The claim README says the work is “Computer-assisted” and that “Independent external
review and a proof-assistant proof are not claimed.”
It credits the capture check to Evan Daniel’s “unmodified `zmx2` checker”, fetched from
his repository at `6e1223cf` and not copied, and says the measure was lifted from the
source’s own point-only $s(45)$ cover.
The root README’s Status section ends “Parts of this work were produced with AI
assistance under human direction.”
It also says that Daniel’s earlier mixed-measure proof is acknowledged and that
$s(61) = 8$ “also follows from Evan Daniel’s” $s(60)$.

## What Is Retained

Byte-identical at their upstream paths:

- from **`point_n61_L8/`**: `README.md`, `check_cover.py`, `cover.txt` (stored as `.gz`),
  `provenance.json` and `verify.sh`; and
- the root **`README.md`**.

Pinned by digest only: `LICENSE` (1,064 bytes, `c0dd43e7…`), retained by the September 27
packet.

`point_n61_L8/README.md` also links `../point_n21_L5/UPSTREAM-LICENSE.txt`, which is
outside this scope.

[`acquisition/declaration.json`](acquisition/declaration.json) declares the scope and
[`acquisition/sources.json`](acquisition/sources.json) records the pin. From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-point-n61-2026-09-30 --check`
re-derives the packet from its manifest.

## The Claim, as the Source States It

| Claim | Directory | Measure | Total |
| --- | --- | --- | --- |
| $s(61) = 8$ | `point_n61_L8` | 15,193 points, $D_4$-invariant, in `[81/500, 3919/500]²` | $8584985072679551 / 2^{47} = 60.99998780001\ldots < 61$ |

If every closed unit square in $[0,8]^2$ captures mass at least 1, then 61 disjoint
unit squares in a square of side $L < 8$ would capture 61, more than the total. The
$8 \times 8$ grid packs 64 squares, so $s(61) = 8$. The capture condition is checked by
`zmx2 cert cover.txt --d4 --pair-points`, which the source reports as `VERIFIED-D4` over
6,400 roots with 800,042 boxes and maximum depth 30 (`provenance.json`).
`check_cover.py` decides only the format, the $D_4$ invariance and the total.

## The Replay

From `packing/`, `devtools.replay_evand_zmx2` assembles `zmx2.rs` `6b7f0f79…` (the
version `verify.sh` pins by that digest) and its crate from retained bytes, builds it, and
runs it under `devtools.replay_receipt`:

```sh
python3 -m devtools.replay_evand_zmx2 build --checker 6b7f0f79 --work /tmp/z61
python3 -m devtools.replay_evand_zmx2 run --case 61 --mode d4 --work /tmp/z61 --out OUT --threads 4
```

| Receipt | Result |
| --- | --- |
| [`n61_zmx2_d4_pairpoints.log`](receipts/n61_zmx2_d4_pairpoints.log) | `VERIFIED-D4`: 6,400 of 6,400 roots (all of `[0,4]²` by four $u$ bins), 800,042 boxes, 392,572 certified leaves, 10,649 empty, **0 uncertified, 0 capped**, maximum depth 30; 256 s wall, 1,004 CPU-seconds on four cores |
| [`n61_zmx2_d4_pairpoints_audit.json`](receipts/n61_zmx2_d4_pairpoints_audit.json) | `devtools.audit_evand_mixed_covers zmx2 --case 61`: every root of the region present once, ids as `zmx2` numbers them, none uncertified, box total and depth equal to the source’s |
| [`n61_cover_audit.json`](receipts/n61_cover_audit.json) | `audit_evand_mixed_covers cover --case 61`, exact integers: the digest, the counts, the total, and $D_4$ invariance entry by entry and as a measure |

The box total and depth equal the source’s reference run, which was a different binary
build on a different machine, and Daniel’s own `--d4 --pair-points` census in
`S61_WAND125_REPLAY.md`.

The $D_4$ reduction is the checker’s own and is justified by the exact invariance check
the audit repeats. The weakest hypothesis here is that `zmx2`’s interval arithmetic is
sound; this repository has not re-derived it.

### The Controls

Two mutated covers, each with one $D_4$ orbit of points removed, are refused by the same
`zmx2` over one root region chosen where the removed mass mattered
([`receipts/controls/`](receipts/controls/), held by `tests/test_replay_controls.py`):

| Mutation | Orbit removed | Region (centre cells) | Result |
| --- | --- | --- | --- |
| `drop-heaviest-point` | the 8 points of weight $0.0777\ldots$ at $(15/16, 3)$ | `x26-26, y8-8` | `NOT VERIFIED`, 460 uncertified boxes |
| `drop-second-heaviest-point` | the 4 points at $(29/8, 29/8)$ | `x36-36, y36-36` | `NOT VERIFIED`, 452 uncertified boxes |

## Limitations

- **One checker.** `zmx2` is the only program that decides the capture condition here.
  Daniel’s `zeromargin.py` and `zmcheck`, which his report says certify the same cover,
  were not run by this repository.
- **A third party’s checker, by the source’s own choice.** wand125 ships no capture
  checker of their own for this cover, so no first-party check by the source exists.
- **The controls are local.** Each refusal is one root cell, not a sweep of the mutated
  cover.

## Compressed Files

Two data files are stored as deterministic gzip made by `gzip -9n`: the cover (an
upstream file of more than 1,000 lines) and the root log of the replay (a receipt).
The table gives the Git blob and SHA-256 of the decompressed bytes; the cover’s SHA-256 is
also the one [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)
pins. `python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/point_n61_L8/cover.txt.gz` | upstream | `cb6797c87930f8bcb57618e74a19ed0d2a19dded` | `bcb66c7910ef844ce8d39c423d7a5a419bd530a344689331f7665ba6971d0374` |
| `receipts/n61_zmx2_d4_pairpoints_roots.log.gz` | receipt | `509dbbc59d08b3be40831c4e645e8b8faba5a4d1` | `fd3d78b63fd94329b713e5de43005e1528a4afa0188a016fdf3c7ef4f0620528` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
