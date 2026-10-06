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

**The receipts of this import** are under [`receipts/`](receipts/): the records audit,
the source’s `verify_tilt9.sh` run here, the sample’s plan, logs, records and
comparison, and the controls (A-4 to A-7).

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

## Audit Here, 6 October 2026

Stages 1 to 3 of the [result import](../../../campaign/result-import.md) for an
evidence update to `T-081`, with as much of stage 4 as a sample affords (bead
`think-dsz4`). Every command ran from `packing/` on a 4-core container shared with
other work, the checker under CPython 3.14.7 and python-flint 0.9.0, as
`requirements.txt` pins, in a scratch venv. All of it took about 2.4 CPU-hours, 1.75 of
them the sample.

### A-1. The Statement Is ValidTilt9, over a Larger Region

The checker’s claim is ValidTilt9 as the Lean states it, and its run covers the
statement’s region with room to spare.

- **The Lean statement.** `ValidTilt 9 box9Cover.measure` (`ValidSplit.lean`) quantifies
  over centres $c \in [0, 9/2]^2$ and $u > 0$ with $u^2 + 2u \le 1$, for the closed
  square `sq c (2 arctan u) 1 ⊆ box 9`. `coord` rotates $p - c$ by $-\theta$, so
  `sq c θ 1` is $c + R_\theta[-\tfrac12, \tfrac12]^2$, and `box 9` is the closed
  $[0, 9]^2$. `box9Cover` is the file read verbatim, its segments indexed by their place
  in the file, and `MixedCover.measure` sums a measure per index: the 16 segments the
  file lists twice count twice.
- **The checker.** Its pose is $c + R_t[-\tfrac12, \tfrac12]^2$ with $u = \tan(t/2)$, the
  same convention. The admissible centres at angle $t \in [0, \pi/2]$ are
  $[w/2, 9 - w/2]^2$ with $w = \cos t + \sin t$ (`tier_a.core_bound`, `tier_b2`), which is
  exactly `sq ⊆ box 9`. `cover.py` keeps every segment line as its own entry and sums
  them, as `mass_convex` and `solver.Local` do, so the doubled segments count twice
  there too; it reads one polygon, $[14/5, 31/5]^2$ of density 1, no point mass, side 9
  and total $3835229774429/50000000000$, the source’s `D` exactly.
- **The run’s region.** The 28,350 roots are centres $[0, 9/2]^2$ at pitch $1/10$ by
  $u \in [0, 7/16]$ in 14 bins of $1/32$. $7/16 > \sqrt2 - 1$, since
  $(7/16)^2 + 2 \cdot 7/16 = 273/256 \ge 1$. The region therefore contains ValidTilt9’s,
  as `qx2_zm.py`’s run does with $u \in [0, 1/2]$ over the same centres.
  `check_record.py --claim tilt` asks exactly this of the roots: a product grid of
  $[0, s/2]^2$ by $[0, U_1]$ with $U_1^2 + 2U_1 \ge 1$, each root once.
- **What the run need not cover.** The statement excludes $u = 0$, which Lean’s
  `validAxis9` (Lemma Z) decides; the checker’s closure argument at $\theta = 0$, which
  its Valid7 run used, plays no part here.

### A-2. Independence From `qx2_zm.py`

By its read log the checker was written without Daniel’s checker, and nothing in the
files contradicts that. What the two share is named here.

- **The checking code is the Valid7 checker’s,** written before the box-9 run from
  `FORMAT.md` and the Valid7 statement, under the read log the 2 October review assessed.
  For this run the author read the k2m4 README’s claim and table, the Lean definitions
  of the statement and the cover; the only code change is the driver’s hand-off option.
- **Shared lines.** `devtools.audit_validtilt9_independent` compares the 903
  non-trivial lines of the checker’s eight modules with Daniel’s four retained checker
  files. Ten occur in both: three imports and an `argparse` line, the
  `if __name__ == '__main__':` guard, one line of a comment-stripping parser, the
  half-angle formula $(1 - u^2)/(1 + u^2), 2u/(1 + u^2)$, two lines of a
  Sutherland–Hodgman clip and one of Andrew’s monotone-chain hull, written with the same
  variable names. They are textbook idioms; no function is shared.
- **Shared inputs.** The statement, the cover (Daniel’s, the object both decide; neither
  checker generates it) and the cover format specification.
- **Shared trust.** Both decide in CPython’s `fractions.Fraction` and `int`.
  `qx2_zm.py` also uses NumPy arrays; wand125’s checker uses python-flint’s `fmpq_poly`
  for polynomial arithmetic, with its own Sturm sequences, and no floating-point number
  in a decision.
- **Shared authorship tools.** The commit carries a `Co-Authored-By: Claude Opus 5.5`
  trailer, and Daniel’s `CREDITS.md` says his work was produced by Claude. Two checkers
  written with models of one family can share blind spots that a read log cannot rule
  out; the identical idioms above are what that looks like when it is harmless.

### A-3. The Trust Boundary

- **What decides.** `tier_a.core_bound` (an exact inner polygon of every square of a
  pose box, and an outer hull for the Lebesgue square) and `tier_b2.certify` (symbolic
  execution of the fixed-angle solver in $u$, with exact real-root isolation), on the
  cover `cover.py` reads. The driver chooses which tier to try and records a leaf only
  when that tier certifies it.
- **What checks the record.** `check_record.py` re-derives, apart from the driver, that
  the roots are the region’s product grid, that each root’s leaves are a bisection
  partition of it, that every `EMPTY` leaf has no admissible centre, and that no Tier B
  leaf has $u = 0$ inside; it re-certifies sampled leaves on request.
- **What is trusted.** CPython 3.14.7’s integers and `Fraction`, python-flint 0.9.0’s
  polynomial arithmetic, and the soundness of the lemmas in `DESIGN.md` and the module
  docstrings, which the
  [2 October review](../../../../docs/project/reviews/review-2026-10-02-valid7-independent-checker.md)
  read for the $k = 7$ cover. For the published run, every leaf not re-certified here is
  taken on the label the source’s machines gave it.
- **The fixed code.** The run used `da469ec`’s `tier_b2.py` and `rf.py`, which fix the
  review’s D-1 to D-3; the 3 October packet’s probe shows each finding gone, and the
  review of A-8 read the fixed lines one by one.

### A-4. The Records

[`devtools.audit_validtilt9_independent`](../../../devtools/audit_validtilt9_independent.py)
`audit` ([`receipts/validtilt9_records_audit.json`](receipts/validtilt9_records_audit.json))
read the three downloaded records in about 3 CPU-minutes and checks what the source’s
`check_record.py` leaves out:

- each file, compressed and decompressed, has the digest of this packet’s retained
  `release/records.sha256`, not of a copy fetched with the records;
- each header names, by SHA-256, the cover the 3 October evand packet retains and
  checker files this packet retains: `da469ec`’s six checking modules, the driver v1
  (`899144f9`, kept at `versions/V2/run_all.py`) in `tilt9_a.jsonl` and
  `tilt9_b.jsonl`, whose headers were written before the switch, and v2 (`cd6627de`) in
  `tilt9_c.jsonl`;
- the roots are exactly the $45 \times 45 \times 14$ grid, each once, split by centre
  $x$ as `MERGE.md` says, and that grid covers ValidTilt9’s region;
- no root records an uncertified box or a counterexample, the leaf kinds are the
  README’s, and the recorded per-root times sum to 765.85 hours;
- each root is given the options of its place in its record (`PHASES`): the run notes’
  root counts at each change, less, in `tilt9_a.jsonl`, the 350 pilot roots of
  $[4, 9/2]^2$ that machine 1’s record was seeded with and the restriction dropped. That
  gives 16,755 roots at the default `--amin 1/320`
  (111.7 recorded hours), 8,339 at `--amin 1/1280` (542.9), 157 at `--bmid-u 3/16`
  (7.2) and 3,099 at `--bmid-u 7/16` (104.0). The width of a Tier B leaf off $u = 0$
  says which hand-off rule made it, so 2,396 roots test their assignment, and none
  contradicts it. A root with no such leaf is not tested, so the phases remain the
  source’s account, checked where the leaves can check it;
- the shared lines of A-2.

### A-5. The Source’s `verify_tilt9.sh`

[`receipts/validtilt9_verify.log`](receipts/validtilt9_verify.log), written by
`devtools.replay_receipt`, on a scratch export of the retained tree at `c561dbb`. The
release files were downloaded first and checked, so the script’s `curl` fetched nothing.
It checked the six digests, all `OK`, and ran `check_record.py --claim tilt` on the
three records: `RECORD OK`, with `claim tilt roots 28350 leaf kinds {'CORE': 6565165,
'TIERB2': 2940689, 'EMPTY': 31489}` and the fresh seed `2467181006204197608`, so 2,000
`CORE` and 20 `TIERB2` leaves of another random sample than the source’s were
re-certified. Exit 0, 600 s of wall and 582 CPU-s, from 2026-10-06T05:44:09Z.

### A-6. A Sample of Roots, and the Price of a Full Replay

The source’s run recorded about 766 hours of wall time in its workers, so a full replay
here is far above this lane’s ceiling of 6 CPU-hours. It is priced from a sample
and held under `think-hwpr`.

`audit_validtilt9_independent sample --per-phase 5 --heavy 10 --max-seconds 600`
([`receipts/validtilt9_sample_plan.json`](receipts/validtilt9_sample_plan.json), seed
`20261006`) took, from each of the four phases, five roots of at most 600 recorded
seconds at evenly spaced points of their cumulative cost, and ten heavier roots the same
way over all phases. `stage` copied the retained checker and the decompressed cover into
one work directory per driver, refusing any file whose digest is not the one the headers
name; `run` ran each root alone, `run_all.py --centers … --u u0 u1 --ubins 1`, under the
`fork` start method and `devtools.replay_receipt`, two at a time at `nice 10`; `compare`
([`receipts/validtilt9_sample_compare.json`](receipts/validtilt9_sample_compare.json))
read every run’s record and receipt. All 45 runs end `VERIFIED` with exit 0, with no
uncertified box and no counterexample, and each record’s header names the staged files
and its argv the planned options.

- **Replays.** The 20 light roots and the one heavy root of the last phase re-ran under
  the driver and options of their phase, and each leaf list equals the published one,
  leaf for leaf. They include the roots on each side of the first change of options,
  roots 16,374 and 16,413 of `tilt9_a.jsonl`, counted from 0, which the phases put at
  `--amin 1/320` and `--amin 1/1280`.
- **Under the last options.** The 15 light roots of the three earlier phases and the
  nine heavy ones re-ran under `--amin 1/1280 --bmid-u 7/16 --bmid-w 1/20`, the options
  the source’s README gives for the full run. Their leaves differ, as the hand-off
  differs, and each root is certified.
- **Coverage.** 30 distinct roots were re-decided here, holding 2.9% of the run’s
  recorded cost, in 1.75 CPU-hours.

The receipts are [`receipts/sample/`](receipts/sample/), each run’s log and its record,
compressed ([Compressed Files](#compressed-files)).

**The price.** Each phase’s recorded time, split at 600 s into light and heavy roots,
is scaled by the ratio of receipt CPU here to recorded time over its sampled runs.

| Replay | CPU-hours here | How it is priced |
| --- | ---: | --- |
| As published, each root under its own phase’s options, compared leaf for leaf | about 435 | Light roots at 0.46 to 0.61 of their recorded time (one 11-second root at 0.99), 0.52 to 0.59 per phase; the last phase’s heavy root at 0.50; the earlier phases’ heavy roots, never run as published here, at their phase’s light ratio |
| Every root under the last options, certified afresh | about 118 | The last phase as published; the earlier phases’ light roots at 0.44 to 1.03 per phase; their heavy roots at 0.012, the cost-weighted ratio of nine probes that ranged from 0.0002 to 0.57 |

The first is what a root-for-root comparison costs, and two thirds of it is the 266
heavy roots that ran at `--amin 1/1280`. The second is softer: it rests on nine heavy
probes, seven of which the last options closed in at most 73 CPU-seconds where the
published run spent 2 to 3.6 hours, so a heavy root that they do not close quickly would
raise it. The review’s design (A), re-certifying every published leaf, was not priced
here; for Valid7 a leaf re-check cost about as much as the search.

### A-7. Controls

`audit_validtilt9_independent control`
([`receipts/validtilt9_controls.json`](receipts/validtilt9_controls.json), logs in
[`receipts/controls/`](receipts/controls/)) writes two covers, each lighter by a relative
$10^{-4}$ on one tight family, and runs the checker’s own entry points on them and on
the original. The source’s `tests/` mutate only the $k = 7$ cover.

- **The wall family.** A scan of `tier_a.core_bound` at $u = 1/2000$ finds the squares
  resting on the bottom wall with centre $x$ near $4.1$ the tightest, with mass about
  $1 + 0.158u$. M1 lightens the 34 segments in $[18/5, 23/5] \times [0, 1]$. Tier B on
  centres $[81/20, 83/20] \times [1/2, 3/5]$, $u \in (0, 1/64)$ accepts the original
  (`'ok': True`, 273 pairs) and refuses M1 with an exact pose of mass
  $0.99995\ldots$ at $u \approx 2.6 \times 10^{-4}$.
- **The Lebesgue square.** M2 lightens it, inside which every square has mass exactly 1.
  The driver on centres $[22/5, 9/2]^2$, $u \in [0, 1/16]$ verifies both roots of the
  original and reports a counterexample of mass $9999/10000$ in each root of M2,
  `NOT VERIFIED`.

### A-8. The Review

A separately prompted adversarial review, run as its own process in a detached worktree
of the branch at the retention commit and blind to this audit, is
[`review-2026-10-06-wand125-validtilt9-independent-check.md`](../../../../docs/project/reviews/review-2026-10-06-wand125-validtilt9-independent-check.md),
stored as its reviewer printed it. It found no blocking defect in the statement or the
method:

- the statement, as run, contains ValidTilt9, and the checker’s mass equals an evaluator
  written from the Lean definitions at 40 poses;
- every premise of the 2 October review holds on the box-9 cover;
- `da469ec`’s fixes are correct line by line;
- no driver or option change can admit an uncertified pose into a recorded leaf.

Its open items are evidential, and each is handled here or held:

| Finding | Disposition |
| --- | --- |
| W-1, every leaf outside a sample rests on the source’s run | The entry is reported; the full replay is held under `think-hwpr` |
| W-2, code provenance is asserted: headers are written once, the run began 19 minutes before `da469ec` was committed, and `MERGE.md` gives the restricted `tilt9_a.jsonl`’s digest as “as run” | The audit binds every header to retained bytes; the entry’s limitations say the rest is the source’s statement |
| W-3, options per root are not recorded | The audit assigns each root its phase and tests it against its leaves; the 21 replays reproduce their leaves under it. The held replay may use the review’s design (A), which needs no options |
| W-4, `verify_tilt9.sh` checks the records against a digest file from the same release | The audit checks them against the retained `release/records.sha256` |
| W-5, `check_record.py` binds a record to no cover or code | The audit does, from the headers |
| W-6, a Tier B leaf’s $u$-ends are closed across leaves, not by `DESIGN.md`’s continuity | Wording for the source; non-blocking |
| W-7, no mutation control on the box-9 cover | A-7 |
| W-8, the code is independent by its read log, the model family is shared | Recorded in the evidence entry |
| W-11, `rf.nonneg_on` loops when `lo == hi` at a root | Dead code; for the source |
| W-12, record the run as `reported`, `external`, `not-attempted`, and update the stale sentences | Done: `E-k2m4-wand125-validtilt9-report`, the qx2 entry’s evidence update and `T-081`’s `next_rung` |
| W-13, a replay of this run lifts only the ValidTilt9 part | `T-081`’s `next_rung`; the Lean entry is `think-1b7c` |
| W-14, the price was not measured on this cover | A-6 |
| W-15, the source’s Tier B samples used fixed seeds | A-5 used a fresh seed |

### What This Establishes, and What It Does Not

It establishes that the three published records are the ones the release names; that
their roots are exactly a grid over a region containing ValidTilt9’s, each once, with no
uncertified box and no counterexample; that each names the retained checker and the
cover `T-081` cites; that the checker, run here on 30 of the roots, certifies each and
reproduces the published leaves of the 21 it re-ran as published; and that it refuses
two covers made lighter on tight families. The review found the checker’s statement and
method sound for this cover.

It does not re-decide the other 28,320 roots, 97% of the run’s cost: they stand as the
source reports them. So the run is recorded on `T-081` as reported evidence,
`E-k2m4-wand125-validtilt9-report`, and moves no rung. Nor does any of it bear on the
Lean reduction from ValidTilt9 to $s(k^2 - 4) = k$, which is Daniel’s own.

## Compressed Files

The 45 sample records are receipts, compressed here with `gzip -9n` by
`devtools.retained_data compress`. Each row gives the Git blob and SHA-256 of the
decompressed bytes. `gunzip -k` on a stored file restores the record beside it.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `receipts/sample/v1/replay_tilt9_a_02686_x22y25u11.jsonl.gz` | receipt | `27abb98493cabb0c788408801c72249d2a05672c` | `8928b30542ccbe206861712feae76fe88db566fbf98acba965ccf841cd3bbdc3` |
| `receipts/sample/v1/replay_tilt9_a_12432_x16y24u07.jsonl.gz` | receipt | `dd70e52106e3f2453a71390dafc74c57d5302e15` | `59d0fa4d8718dc0ecde4df37c6c8ec40ded35a8cdaa4aea0140b8961720a06a9` |
| `receipts/sample/v1/replay_tilt9_a_15594_x23y16u06.jsonl.gz` | receipt | `c95ca1346ee035f11a0c1c57ff9a159992ae80ba` | `bc44d96a10ce49c5991877a123abf09ccd2d026c37a679d5d856d5371346acbb` |
| `receipts/sample/v1/replay_tilt9_a_15596_x23y15u03.jsonl.gz` | receipt | `1c19103b634d0b9db42458d51d2d3e9fa78da339` | `3f713a5f7ca289535d648501085472db68cef46f1840ea6b618c84e0d724c507` |
| `receipts/sample/v1/replay_tilt9_a_16374_x24y40u08.jsonl.gz` | receipt | `ad149b56f32611dc0f91e7fb9f2e0b84f0e75431` | `161624cf2c84e9856ec536239d8b4a4b5ef49083e55f9dfdac25e924d7f856db` |
| `receipts/sample/v1/replay_tilt9_a_16413_x24y42u06.jsonl.gz` | receipt | `ca5525ac29b85627b893b3f3a0ea64b33fdf37ce` | `6e9a2ad9baa28eaece07942b718fe5af8d67f9092316ba8bd77bf943defbc60e` |
| `receipts/sample/v1/replay_tilt9_a_17755_x27y29u00.jsonl.gz` | receipt | `26972e0858a69f18a56b9976c583da9334c1d129` | `78417cf6bbe4bdb042dc01f411008484d32df9b413d1aec79537eb936f541196` |
| `receipts/sample/v1/replay_tilt9_a_20983_x33y14u10.jsonl.gz` | receipt | `936e23157a9d49e28122c0a2e90ad5f609a791d3` | `45460117868133b67f86e33f9c0d3ac8c2d6ef71f01c652f1f8ae0ebec0e7501` |
| `receipts/sample/v1/replay_tilt9_a_21906_x34y35u11.jsonl.gz` | receipt | `ecec963a3dfd247cfbae3f052ef10537cac8d1e0` | `43c013eddcc6534775849ca511e8ee7a928701d3bda9123f5d3753b63339bdd7` |
| `receipts/sample/v1/replay_tilt9_b_00809_x39y24u08.jsonl.gz` | receipt | `2ceb21e493cc6d53912b1b24088286571664a87e` | `b029bf26ad43f8aaabba1e3a658c2518ce706195f8faf837345a72a5a6913194` |
| `receipts/sample/v2/final_tilt9_a_02686_x22y25u11.jsonl.gz` | receipt | `e05a05b1ac1dc6e41fcc2cd1778886e219257dec` | `84f2075c6f725cb9615b806d34b524e902f6f5e126877cf781fb5e2926850d13` |
| `receipts/sample/v2/final_tilt9_a_12432_x16y24u07.jsonl.gz` | receipt | `9d7dbebc1fd176ede88f93a07d502d1124814639` | `80ee3a5723c1cba7c49711b68ba8c4859475e9bfd6ce9b6b18c8582cf849e0de` |
| `receipts/sample/v2/final_tilt9_a_15594_x23y16u06.jsonl.gz` | receipt | `a57001c26a6fd4c7fda6695b1776df0a2d47553f` | `38b39d420c54edf5751d940b4486372eb03d7b106491a1bdda17b7a13ab9d0d8` |
| `receipts/sample/v2/final_tilt9_a_15596_x23y15u03.jsonl.gz` | receipt | `0c60d1199b5b9c8dc5f6f3302f64ccdc4e0fe49b` | `3fe783e8e34c504f61857dda6f32ab79e66c222bcfb9427035b1a2b884851e4a` |
| `receipts/sample/v2/final_tilt9_a_16113_x23y36u10.jsonl.gz` | receipt | `8a04edc4b6eee8aef2b6cc10473aacbc8e15a14f` | `5386547e23df43e26f98b357480b6b3157b8873806dcdc7b975375ed2843245c` |
| `receipts/sample/v2/final_tilt9_a_16374_x24y40u08.jsonl.gz` | receipt | `9ae22e6bd87efd5f0c1d099cb48cd23856403d47` | `84c9daa264034ce94e394eb098a8dbf030a1dc1f3aebbbf11bb2c21fe76642c2` |
| `receipts/sample/v2/final_tilt9_a_16413_x24y42u06.jsonl.gz` | receipt | `90250f26295e1a730190ceb99d99173ff57dbc06` | `2ca6e1ab47e26dabddd32157487eaa321171237f5ad18703ff846e2bbbb59497` |
| `receipts/sample/v2/final_tilt9_a_16801_x25y25u02.jsonl.gz` | receipt | `378de4f5545f7b82aedd3488d6b777a4ded6db6b` | `7047e38d3c14257377b37a299f7c22afb0d68786dee2f7fbd7d650e66766e01d` |
| `receipts/sample/v2/final_tilt9_a_17755_x27y29u00.jsonl.gz` | receipt | `0074e175929800388899b8b6d63fa71a13cd61fb` | `6a0d7314f8078d7bb10daed77bdb76804fab5cf2577cd6e3e8347187f6d97dab` |
| `receipts/sample/v2/final_tilt9_a_20983_x33y14u10.jsonl.gz` | receipt | `451f3728fe64e22741e8eb459b5736df8cc6cb71` | `9a962451d0bc90afbc2c458b2a53902fdd861c8dfb41d5ae985ba82a5ac25e30` |
| `receipts/sample/v2/final_tilt9_a_21887_x33y42u01.jsonl.gz` | receipt | `a51a0229d964a6af8c6a71c848c07c9a78a632e2` | `b50c931e406ce89e08d71a75eaf9cb17cd45694e8fbdca1e8e8d53e098fd6ef6` |
| `receipts/sample/v2/final_tilt9_a_21906_x34y35u11.jsonl.gz` | receipt | `6526884774f4e411cb9ebf4e864facd0d8e933ee` | `3f16c6aa9a077fe046dc9be12740212a99809873ab3672c9d58268a94ee4ae27` |
| `receipts/sample/v2/final_tilt9_a_21918_x34y33u01.jsonl.gz` | receipt | `04d09aadcaa85009b3b01ca07fcebbcdd198cb2b` | `efa8f207a2cff960f18f8208d441c329d96e789658b99c865b6f10955407e5d7` |
| `receipts/sample/v2/final_tilt9_a_21940_x34y36u05.jsonl.gz` | receipt | `e1b54fc704dfbfd6dec8832b0a671ff0f3ac4ec4` | `503679622a78063ba5b8a9617d347125656200f23c78fdabbb46eef45fb86989` |
| `receipts/sample/v2/final_tilt9_a_21943_x34y36u07.jsonl.gz` | receipt | `4bba55839c525894d7b2218362900d9c8da8715e` | `214c2ce0b0c50efd249065be41e75fb7e9c850be07539495deee45668fe88e8c` |
| `receipts/sample/v2/final_tilt9_a_21986_x34y39u06.jsonl.gz` | receipt | `7254dfbc9ffb4bd0593a0616959f014fd3663a09` | `0596d56647bc00a5ff765eb56817c88df4f82f35191515dafcc2d4cec8338beb` |
| `receipts/sample/v2/final_tilt9_b_00809_x39y24u08.jsonl.gz` | receipt | `e3fc84b09e3615a133230b74420960019011810a` | `b877b83f0ffe4bb64a2cec6121f4431080192ba4221bebed53be652f5a9d3e80` |
| `receipts/sample/v2/final_tilt9_b_01451_x39y35u12.jsonl.gz` | receipt | `063c2cdece8e3d81f88cc42326caca29d08b2098` | `38a45dd38a71998516dbb66ae8dab64d60be84f114f59bee4fd575659f409323` |
| `receipts/sample/v2/final_tilt9_b_01846_x40y33u03.jsonl.gz` | receipt | `18ac59b21a49693397f1f812899e5d156ab6bca2` | `2d4341a89d7d768b3929b3321ad63ecc84e3bfac4eda2e9e26a22daaeaecd494` |
| `receipts/sample/v2/final_tilt9_b_02444_x42y23u12.jsonl.gz` | receipt | `89bcbef5695df8572f5c45ba85824e2bd5852ff7` | `ad40778366d91d13f13e0539e93bc7a0567b00fac7a6eeb9c547ca7479cba6ed` |
| `receipts/sample/v2/final_tilt9_b_02447_x42y25u09.jsonl.gz` | receipt | `72d7f8b197fe985daaf62ccf2950a8617b7ee99d` | `46b923ee077e42ffcba19180b61c5d860e1451e3a6ef786f35a6902a28fd8850` |
| `receipts/sample/v2/final_tilt9_b_02508_x42y29u01.jsonl.gz` | receipt | `df7f4947c7d03be95968397938c9537baef4ed0d` | `8364e97b1bb57aea0fbf6e5461a74abbb55777a0e5d6c69112dcfb4cfeadd38e` |
| `receipts/sample/v2/final_tilt9_b_02511_x42y27u04.jsonl.gz` | receipt | `babc78f91eb9163fd13dadaa66131e7c22451a24` | `fc40c1f01233da55d5427043577401558c8907f9f458c1ee53cf34906e84b7e8` |
| `receipts/sample/v2/final_tilt9_b_02546_x42y31u01.jsonl.gz` | receipt | `2f93560476de452297ebc065a9b92e247db374c3` | `19525c2f65a8aa5cc90e96927c3241640e3af133481aa5e7f9b92352fd732392` |
| `receipts/sample/v2/final_tilt9_b_02993_x43y22u07.jsonl.gz` | receipt | `2e72aeb8daf34a942c82fcc658d2c1d6a66e5fe2` | `ad374380c3740087c750c9190dbc825ab988b398cb3086838346e21f69d686da` |
| `receipts/sample/v2/replay_tilt9_a_22982_x36y21u12.jsonl.gz` | receipt | `489052e3b8fcfbb78676c099ba78d1fb3fc7660b` | `6f7f6f7ec19431944ace60db812dc9b875d09a76f7f03e89a8b2a2b07513b218` |
| `receipts/sample/v2/replay_tilt9_a_23074_x36y27u12.jsonl.gz` | receipt | `41da017c26c538394fafbc3a89359225d0d279bb` | `d38f5f31bc3233b944a0ac0835683b309d2b99c739c5887c65274b449bdb3403` |
| `receipts/sample/v2/replay_tilt9_a_23099_x36y30u09.jsonl.gz` | receipt | `5600f3b426826dec9d829be7f76760cc3ae52c7f` | `e061e0d4e40d182fe0dbf14389b4e7f18e975429ca68bbe88b04febc7e452be5` |
| `receipts/sample/v2/replay_tilt9_b_02444_x42y23u12.jsonl.gz` | receipt | `7b440a1fd21b77a4c5017e4a1e9fd6c347d940f3` | `2997835f4d9098fc97d81d812a1e1336c5ace763538ea15ba88013284ad5abbb` |
| `receipts/sample/v2/replay_tilt9_b_02447_x42y25u09.jsonl.gz` | receipt | `75f7fd7a67c18e97b3ed0b9842893b466aefe8c8` | `fd2d4ed4eb1b5d250503a632e0632ac874c17ef04539d5585baeb35a43e9ad47` |
| `receipts/sample/v2/replay_tilt9_b_02508_x42y29u01.jsonl.gz` | receipt | `b909cd12b746584dc409e90c74237b7f5139b0d4` | `af4c002d11638cb8c742b22624d8883547a4a92137b8565be9e57ce4ccb187c4` |
| `receipts/sample/v2/replay_tilt9_b_02511_x42y27u04.jsonl.gz` | receipt | `2c4278a114e83389180fa8475686effdcd27ebd6` | `115a26b08b450a7775392dd754735e8d1a2b8d4c769f24b707bb5fc33eb9c3db` |
| `receipts/sample/v2/replay_tilt9_b_02546_x42y31u01.jsonl.gz` | receipt | `bd3e3887346078104c3f6c3eb711ffc516b04c35` | `3c562c105acc8ea0adf5e2e63c724595b634f752758e6d1be06737504b0387a2` |
| `receipts/sample/v2/replay_tilt9_b_03573_x44y25u10.jsonl.gz` | receipt | `666bd705d3e470cc04bd337286eeb400e446fe7c` | `c615b149fd9f971a6450c74c4fef486097b935c47312bfb89689e8d92deb4a51` |
| `receipts/sample/v2/replay_tilt9_c_00205_x38y14u02.jsonl.gz` | receipt | `f11ac39447192625bb469a0dc442b409ff1d09da` | `af270290416729dec85a5397f365a79c93b31929c03b7fdc45f302b8b4313af8` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
