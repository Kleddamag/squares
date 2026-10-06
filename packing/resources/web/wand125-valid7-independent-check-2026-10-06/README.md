# wand125’s Independent Checker on ValidTilt9, Pinned 2026-10-06

This packet retains
[wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check)
at its third commit, which runs the checker this repository replayed for `T-064`’s
Valid7 on a second statement: **ValidTilt9**, the finite premise on which `T-081`’s
$s(k^2 - 4) = k$ rests for every $k \ge 8$. ValidTilt9 says that every closed unit
square in $[0,9]^2$ with centre in $[0, 9/2]^2$ and angle $\theta = 2\arctan u$,
$u > 0$, $u^2 + 2u \le 1$ ($0 < \theta \le 45°$), has mass at least 1 under Evan
Daniel’s box cover `K4_k008_box9.txt`. Daniel’s Lean development reduces the theorem to
it, and until this commit it was decided by one program, Daniel’s `qx2_zm.py`
(`E-k2m4-evand-validtilt9-qx2-report`). Nothing on jlevy/squares has reported the run
yet; jlevy/squares#316 queues an independent check of ValidTilt9 as an ask, under bead
`think-y3vy`. This import is bead `think-dsz4`.

The checker itself, its first run and its full replay here are described by the
[2 October packet](../wand125-valid7-independent-check-2026-10-02/README.md); the fixes
of the review’s D-1 to D-3 by the
[3 October packet](../wand125-valid7-independent-check-2026-10-03/README.md).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/valid7-independent-check> |
| Revision | [`c561dbb3fcea9178599db017f51f56b42ad9f91f`](https://github.com/wand125/valid7-independent-check/tree/c561dbb3fcea9178599db017f51f56b42ad9f91f), tree `f48d1064`, the repository’s third commit: “Add the ValidTilt9 check: cover, driver v2, verify_tilt9.sh and README” |
| Committed | 2026-10-06T02:36:04Z (11:36 in the commit’s +09:00); the commit’s author name is Hiroaki Hosono, and `LICENSE` reads “Copyright (c) 2026 wand125” |
| Retrieved | 2026-10-06T05:34Z, a full clone; `main` pointed at this commit |
| Release | `records-tilt9-v1`, “ValidTilt9 run records”, published 2026-10-06T02:36:24Z; its eight assets were downloaded at 2026-10-06T05:35Z, and GitHub reports them last modified 2026-10-06T02:36:18Z to 02:36:24Z |
| Licence | MIT. `NOTICE` says `cover/L4_k02_box7.txt` and `cover/K4_k008_box9.txt` are Evan Daniel’s, MIT, the second taken unchanged from evand/square-packing `0c243090`, SHA-256 `4151d7c4…` |
| Request | None on this repository. jlevy/squares#316’s ask for an independent check of ValidTilt9 (bead `think-y3vy`) is what it answers; on 3 October wand125 wrote on evand/square-packing#1 that the result would be reported on #316, and by 2026-10-06T06:00Z it had not been |

**Credit and AI assistance.** The commit message ends with the trailer
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, the repository’s first
statement of AI assistance; its two earlier commits carry none, and `LICENSE`, `NOTICE`
and `READ_LOG.md` say nothing of how the code was written.
Daniel’s `CREDITS.md` says his work was produced by Claude (Anthropic) under human
direction.

## What Changed

Seven files, 2,173 lines added and 5 removed, against the second commit `da469ec`:

- **`cover/K4_k008_box9.txt`** is added, byte-identical to the cover the
  [3 October evand packet](../evand-square-packing-2026-10-03/README.md) retains and
  `T-081` cites; `NOTICE` names it.
- **`src/run_all.py`**, the driver, gains `--bmid-u` and `--bmid-w`: a box not touching
  $u = 0$ with $\lvert u\rvert \le$ `bmid_u` is handed to the exact Tier B once its
  centre width is at most `bmid_w`. With the default `--bmid-u 0` it behaves as before.
  The source calls this driver v2 (SHA-256 `cd6627de…`); v1 is the Valid7 run’s V2
  driver, `899144f9…`, which this tree keeps at `versions/V2/run_all.py`.
- **`verify_tilt9.sh`** downloads the three records of the release, checks their
  digests, and runs `check_record.py --claim tilt --recheck 2000 --recheck-b 20`.
- **`README.md`**, **`READ_LOG.md`** and **`versions/VERSIONS.md`** describe the run, what
  was read for it, and the driver change.

No checking module changed: `cover.py`, `tier_a.py`, `tier_b.py`, `tier_b2.py`,
`solver.py`, `rf.py` and `check_record.py` are `da469ec`’s, the fixed code.

## What Is Retained

All 31 tracked files are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)), 272,541
bytes. Twenty-nine are retained under
[`valid7-independent-check/`](valid7-independent-check/), byte-identical, 205,923 bytes.
Two are **pinned by digest only**, because another packet retains the same bytes:

- `cover/L4_k02_box7.txt` (18,238 bytes, `c0a67509…`), as in the earlier packets, is the
  [October 1 evand packet](../evand-square-packing-2026-10-01/README.md)’s copy;
- `cover/K4_k008_box9.txt` (48,380 bytes, `4151d7c4…`) is the 3 October evand packet’s
  `square-packing/s12/certificates/k2m4/K4_k008_box9.txt.gz`, decompressed.

[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives
the packet from its manifest.

**The release’s small files are retained** under [`release/`](release/),
byte-identical: `records.sha256`, `MERGE.md` (how the three records combine, the code
each ran and the run’s history), `NOTES_machine1.txt` and `NOTES_machine2.txt` (the
run’s notes) and `check_tilt9.out` (the source’s `check_record.py` output).

**The three records are pinned, not retained.** At 46.6 MB compressed they are past the
archive’s retained-data rule; the digests make any copy checkable.

| Release asset | Bytes | SHA-256 | Decompressed |
| --- | ---: | --- | --- |
| `tilt9_a.jsonl.gz` | 39,752,376 | `f38e33a2a4aa8d32f0abc757bfbf30027fb1d926bae44ac75d9e297f88b591bf` | 846,508,528 bytes, 23,941 lines, `1e7ac2fe…` |
| `tilt9_b.jsonl.gz` | 6,780,378 | `76ec2ef1c72ea8b104dcc3f6d86e1166292e3bb339632ac18c10fe6db828a1ce` | 149,251,411 bytes, 3,781 lines, `f802a0e4…` |
| `tilt9_c.jsonl.gz` | 19,447 | `0f7275dbdfa2f92702253ba797e8bc660bad1a16c8cf44f1b705edad99d51622` | 244,390 bytes, 631 lines, `4a1e798d…` |

## The Claim and the Independence Statement, as the Source Makes Them

The README states the result: “ValidTilt9 holds. Centres $[0, 9/2]^2$ (pitch 1/10) ×
$u \in [0, 7/16]$ (14 bins; $7/16 > \sqrt2 - 1$), no symmetry used: 28,350 roots, 0
uncertified, 0 counterexamples; 9,537,343 leaves (CORE 6,565,165 / TIERB2 2,940,689 /
EMPTY 31,489); about 766 core-hours.” It took the statement from the Lean definitions
`ValidTilt9`, `ValidTilt`, `sq` and `coord`, with the rotation $c + R_\theta[-\tfrac12,
\tfrac12]^2$ that its checker uses.

`READ_LOG.md` adds a section for this run, against evand/square-packing `0c243090`:

- **Read:** lines 1–80 of `s12/certificates/k2m4/README.md` (claim, proof paragraph, the
  table of what is checked by what, lemma names only); in `ValidSplit9.lean` and
  `ValidSplit.lean`, only the definitions `ValidTilt9` and `ValidTilt` and their doc
  comments; in `Basic.lean`, the definitions `coord`, `sq` and `sqInt`; and the cover.
- **Not read:** the checker programs and lemma documents its Valid7 section lists, the
  k2m4 run records and outputs, and the rest of the Lean.

**The run’s history** (`release/MERGE.md` and the two notes). Machine 1 started the whole
region on 2026-10-03T22:55Z with the default options, its record seeded with four pilot
blocks of the same grid and code, and was resumed at 10-04 06:10 with `--amin 1/1280`.
Machine 2 took centres $x \ge 39/10$ from 10-05 05:06, its record seeded with the 350
pilot roots of $[4, 9/2]^2$. At 10-05 11:34 both switched to driver v2 with
`--bmid-u 3/16 --bmid-w 1/20`, and at 13:07 to `--bmid-u 7/16`. Machine 1 stopped at
15:44 with every root of $x < 38/10$ done, and machine 2 ran the column
$38/10 \le x < 39/10$ into `tilt9_c.jsonl`. The source says the checking code was the same
throughout, `da469ec`’s. `tilt9_a.jsonl` is machine 1’s record without its roots of
$x \ge 38/10$; only `tilt9_c.jsonl`’s header was edited before publication, to make its
paths relative.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
