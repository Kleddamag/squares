# wand125’s Independent Valid7 Checker, Pinned 2026-10-02

This packet retains
[wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check),
a second exact checker for the finite statement **Valid7** on which T-064’s lower half
rests, and pins the records of its run by SHA-256. Valid7 says that every closed unit
square in $[0,7]^2$, at every position and angle, has mass at least 1 under Evan
Daniel’s $k = 7$ measure `L4_k02_box7.txt`; Daniel’s Lean reduction derives
$s(k^2 - 3) = k$ for every $k \ge 6$ from it.
Until this source, Valid7 was decided by one program, Daniel’s `qx2_zm.py`. The request
is [jlevy/squares#296](https://github.com/jlevy/squares/issues/296), also announced on
[#279](https://github.com/jlevy/squares/issues/279).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/valid7-independent-check> |
| Revision | [`38dd31b369991b0d96c917a4af0c7139b44a038d`](https://github.com/wand125/valid7-independent-check/tree/38dd31b369991b0d96c917a4af0c7139b44a038d), tree `5667d8de`, the repository’s only commit: “Independent checker for Valid7 (s(k^2 - 3) = k): code, cover, tests, design notes” |
| Committed | 2026-10-02T02:49:17Z; the commit’s author name is Hiroaki Hosono, and `LICENSE` reads “Copyright (c) 2026 wand125” |
| Retrieved | 2026-10-02T07:42Z, a full clone |
| Release | `records-v1`, assets downloaded 2026-10-02T07:42Z; GitHub reports them last modified 2026-10-02T02:49:36Z and 02:49:39Z |
| Licence | MIT. `NOTICE` says `cover/L4_k02_box7.txt` is Evan Daniel’s, MIT, taken unchanged from evand/square-packing `d9f79bc1` |
| Request | [jlevy/squares#296](https://github.com/jlevy/squares/issues/296), opened 2026-10-02T03:02Z by wand125 |

The repository has no credit or AI-assistance statement beyond `LICENSE`, `NOTICE` and
`READ_LOG.md`; none of them says how the code was written.

## What Is Retained

All 29 tracked files are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)), 216,830
bytes. Twenty-eight are retained under
[`valid7-independent-check/`](valid7-independent-check/), byte-identical: the checker
(`src/`, eight modules), the record checker `src/check_record.py`, `verify.sh`, the
mutant tests (`tests/`), the V1 and V2 copies of the two files changed during the run
(`versions/`), and `README.md`, `DESIGN.md`, `READ_LOG.md`, `LICENSE`, `NOTICE`.

`cover/L4_k02_box7.txt` (18,238 bytes, SHA-256 `c0a67509…`) is **pinned by digest
only**, because the
[October 1 evand packet](../evand-square-packing-2026-10-01/README.md) retains the same
bytes at `source/s12/certificates/k2m3/L4_k02_box7.txt`, the cover T-064 cites.
The independent checker therefore decided the statement about the very cover the
register holds.

**The release records are pinned, not retained.** Their checksum file is retained as
[`release/records.sha256`](release/records.sha256), byte-identical to the release asset.

| Release asset | Bytes | SHA-256 | Decompressed |
| --- | ---: | --- | --- |
| `full.jsonl.gz` | 48,233,250 | `f553751df065f06708ea4226b1e18cb36a47f6fb1a47f0f0afd9ba0b628a4845` | 935,226,793 bytes, 123,201 lines, `bff065fe…` |
| `full_b.jsonl.gz` | 2,338,077 | `8eaf90f342429cae3245965a18e08452f73b9270b1f61aa9b129e08de45d6a4f` | 39,909,832 bytes, 33,601 lines, `e0fb45b6…` |
| `records.sha256` | 318 | retained | lists the four digests above |

At 50.6 MB compressed they are too large for the archive’s retained-data rule; the
digests make any copy checkable.
[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives
the packet from its manifest; it does not cover the release.

## The Claim and the Independence Statement, as the Source Makes Them

The source’s README states the result: “Every pose was certified, with no symmetry
reduction: 156,800 root boxes covering centres $[0,7]^2$ × $u = \tan(\theta/2) \in
[-1/2, 1/2]$, 0 uncertified, 0 counterexamples; 9,640,060 leaves; about 626 core-hours.”
The $u$-range is $\theta \in [-53.13°, 53.13°]$, more than the square’s period of $90°$.

Its independence statement, in the README and `READ_LOG.md`:

- **Read:** the k2m3 bundle’s `README.md` (claim, proof paragraph, leaf-kind names,
  lemma names without proofs), `s21/FORMAT.md`, lines 1–60 of the bundle’s `verify.sh`,
  and the cover, all at evand/square-packing `d9f79bc1`; and the author’s own earlier
  `checker2/README.md` in wand125/squares-in-triangle.
- **Not read, by design:** `qx2_zm.py`, `zm_mixed.py`, `zeromargin.py`,
  `mixed_cover.py`, `QUADRANT_EXACT.md`, `ZM_MIXED.md`, `qx2_records.py`,
  `qx2_family_check.py`, the V3 run record and `lemmaZ.out`.
- **Contact:** another checker for covers of the same kind, for a different container
  with C4 symmetry, was being written at the same time, “possibly with reference to the
  upstream checker”; only specifications and usage were exchanged with it.
- **Different by design:** no D4 reduction; $\theta = 0$ by a closure argument (mass is
  upper semicontinuous in the pose) rather than an enumeration; its own exact
  primitives, `fractions.Fraction` and python-flint polynomials with its own
  Sturm-sequence root isolation, with no floating-point number in any decision.

What the two checkers share is the statement, the cover file and its format
specification.
Whether they share a lemma is a question for the review lane: the source’s
proofs are in `DESIGN.md` and the module docstrings, and were not reviewed here.

**History of the run** (`versions/VERSIONS.md`). Roots 1–31,825 of `full.jsonl` ran
under V1 and the rest under V2; V2 changed the hand-off rule between the two tiers and
the failure messages, and the source says no proof step.
A defect in the algebraic-number class found before V1 was fixed and every record made
before it discarded.
From 2026-10-01T20:47Z the remaining roots were split over two machines, `full.jsonl`
taking centres $x < 11/2$ and `full_b.jsonl` the rest.
Before publication only each record’s header line was edited, to make its file paths
relative.

## Replay Here, 2 October 2026

Stage 4 of the [result import](../../../campaign/result-import.md), within what this
container affords: the source’s own `verify.sh`, run as published, and an audit of what
it leaves out. The source’s run took about 626 core-hours and was **not** repeated.

**`verify.sh`** ([`receipts/valid7_verify.log`](receipts/valid7_verify.log)), written by
`devtools.replay_receipt`. The three release files were downloaded first and checked
against `records.sha256`, so the script’s `curl` and `gunzip` steps found them present
and fetched nothing.
The cover was the October 1 evand packet’s copy.
The interpreter was CPython 3.14.7 with python-flint 0.9.0, as `requirements.txt` pins.
The script:

1. checks the four SHA-256 digests (all `OK`);
2. runs `check_record.py` on both records with `--recheck 2000 --recheck-b 300`:
   `RECORD OK`, with `roots 156800 leaf kinds {'EMPTY': 79927, 'TIERB2': 2886043,
   'CORE': 6674090}`;
3. runs the three mutant covers of `tests/run_mutants.sh`, each the cover with one tight
   family lighter by a relative $10^{-4}$: Tier B returns `'ok': False` with an exact
   pose of mass below 1 for the wall mutant M1 on both sides of $u = 0$ and for the
   corner mutant M3, and the driver reports two counterexamples and `NOT VERIFIED` for
   the Lebesgue-square mutant M2.

Exit 0, 623 s of wall and 451 CPU-s on a 4-core container shared with other replays,
from 2026-10-02T07:44:47Z.

**The audit** by
[`devtools.audit_valid7_independent`](../../../devtools/audit_valid7_independent.py)
([`receipts/valid7_records_audit.json`](receipts/valid7_records_audit.json)) reads the
two records again and checks what `check_record.py` does not read, in 16 CPU-s, with its
log in [`receipts/valid7_records_audit.log`](receipts/valid7_records_audit.log):

- both files, compressed and decompressed, have the release’s digests;
- each header names, by SHA-256, the retained cover and the retained code: the
  `versions/V1/` copies of `run_all.py` and `tier_b2.py` for `full.jsonl`, whose header
  V1 wrote, and `src/` for `full_b.jsonl`, written by V2. The V2 roots that `full.jsonl`
  gained on resuming carry no header of their own; `versions/VERSIONS.md` alone names
  them;
- the 156,800 roots are exactly the grid `run_all.py` builds by default, each once, with
  `full.jsonl` holding the 123,200 at $x < 11/2$ and `full_b.jsonl` the other 33,600;
- no root records an uncertified box or a counterexample; and
- the totals are the README’s: 9,640,060 leaves, and 626.36 core-hours summed over the
  roots’ recorded CPU times.

[`packing/tests/test_audit_valid7_independent.py`](../../../tests/test_audit_valid7_independent.py)
holds both receipts, re-deriving the header linkage from the retained files.

### What the Replay Establishes, and What It Does Not

It establishes that the published records are the ones the release names; that their
roots are exactly the whole pose grid, each once, with no uncertified box and no
counterexample; that inside every root the leaves are an exact bisection partition; that
every `EMPTY` leaf has no admissible centre and no Tier B leaf contains $u = 0$; that
the code each record’s header names is the code retained here; and that 2,000 random
Tier A leaves and 300 random Tier B leaves re-certify under the retained V2 code.
Three covers each made lighter by $10^{-4}$ on a tight family are refused.

It does not re-certify the other 9.6 million leaves: each was accepted on the label the
run gave it. That is the 626 core-hours, the certification itself, and stands as the
source reports it. Nor does it review the method: the closure argument at $\theta = 0$,
the core bound of Tier A, the two lemmas of the fixed-angle solver, and the symbolic
execution of Tier B are proved in `DESIGN.md` and the module docstrings, and a review of
them is the other lane of stage 4.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
