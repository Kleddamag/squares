# wand125’s Independent Valid7 Checker, Pinned 2026-10-03

This packet retains
[wand125/valid7-independent-check](https://github.com/wand125/valid7-independent-check)
at its second commit, which fixes the three implementation findings, D-1 to D-3, of this
repository’s
[method review of 2 October](../../../../docs/project/reviews/review-2026-10-02-valid7-independent-checker.md).
The checker is the second exact checker of **Valid7**, the finite statement on which
T-064’s lower half rests; the
[2 October packet](../wand125-valid7-independent-check-2026-10-02/README.md) retains its
first commit and describes the checker, its records and its full replay here.
Nothing on jlevy/squares asked for the fix.
Its commit answers
[evand/square-packing#1](https://github.com/evand/square-packing/issues/1), closed on
2026-10-03, whose points are the review’s findings.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/valid7-independent-check> |
| Revision | [`da469ecff5da0c71882e894b65d680ce57a0c87e`](https://github.com/wand125/valid7-independent-check/tree/da469ecff5da0c71882e894b65d680ce57a0c87e), tree `2ebd1556`, the repository’s second commit: “Fix the three points raised in evand/square-packing#1 (no change to any certified result)” |
| Committed | 2026-10-03T23:14:42Z (2026-10-04 08:14 in the commit’s +09:00); the commit’s author name is Hiroaki Hosono, and `LICENSE` reads “Copyright (c) 2026 wand125” |
| Retrieved | 2026-10-05T04:23Z, a full clone; `main` pointed at this commit |
| Release | `records-v1`, unchanged: its three assets were downloaded again at 2026-10-05T04:23Z, GitHub reports them last modified 2026-10-02T02:49:35Z to 02:49:39Z, and `records.sha256` is byte-identical to the 2 October packet’s |
| Licence | MIT. `NOTICE` says `cover/L4_k02_box7.txt` is Evan Daniel’s, MIT, taken unchanged from evand/square-packing `d9f79bc1` |
| Request | None on this repository |

The repository still has no credit or AI-assistance statement beyond `LICENSE`, `NOTICE`
and `READ_LOG.md`.

## What Changed

The commit changes four files of `src/`, 60 lines added and 20 removed; the rest of the
tree, `README.md` and `verify.sh` included, is byte-identical to the first commit.

- **D-1:** `tier_b2.nonneg_open` now tests the sign at an interior point that is not a
  root of the polynomial, moving the sample until it is not, and requires the value
  there to be positive.
  Before, it accepted a value of zero.
- **D-2:** the unused `rf.nonneg_on` now refuses a root of odd multiplicity strictly
  inside the interval and tests the sign the same way.
- **D-3:** `tier_b2` de-duplicates lines and caches edge values by the exact canonical
  text of each rational function, where it used Python’s 64-bit `hash`.
- **`check_record.py`** takes `--seed S` for the leaves `--recheck` and `--recheck-b`
  sample, by default a fresh random seed that it prints, following Evan Daniel’s note on
  evand/square-packing#1. It also takes `--claim tilt`, which checks a record over
  centres $[0, s/2]^2$ and $u$ from 0 to at least $\sqrt2 - 1$, the domain of the
  ValidTilt9 statement; `--claim valid`, the default, is the check it made before.
- `cover.py`’s self-test prints $s^2$ minus the total mass where it printed $49$ minus
  it.

The commit message says no certified result changes.
The release records were not regenerated: they are still the runs of the first commit’s
V1 and V2 code, whose files the 2 October packet retains.

## What Is Retained

All 29 tracked files are in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)), 218,820
bytes. Twenty-eight are retained under
[`valid7-independent-check/`](valid7-independent-check/), byte-identical, 200,582 bytes.
`cover/L4_k02_box7.txt` (18,238 bytes, SHA-256 `c0a67509…`) is pinned by digest only, as
in the 2 October packet, because the
[October 1 evand packet](../evand-square-packing-2026-10-01/README.md) retains the same
bytes. [`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check`
re-derives the packet from its manifest.

The release records are pinned, not retained; their checksum file is retained as
[`release/records.sha256`](release/records.sha256), and the 2 October packet’s table
gives their sizes and digests.

## Replay Here, 5 October 2026

**`verify.sh`** ([`receipts/valid7_verify.log`](receipts/valid7_verify.log)), written by
`devtools.replay_receipt`, ran on a scratch copy of the retained tree as published.
The three release files were downloaded first and checked against `records.sha256`, so
the script fetched nothing, and the cover was the October 1 evand packet’s copy.
The interpreter was CPython 3.14.7 with python-flint 0.9.0, as `requirements.txt` pins.
The script:

1. checks the four SHA-256 digests (all `OK`);
2. runs the fixed `check_record.py` on both records with
   `--recheck 2000 --recheck-b 300` and a fresh seed, which it printed as
   `2431791605250748986`: `RECORD OK`, with
   `claim valid roots 156800 leaf kinds {'EMPTY': 79927, 'TIERB2': 2886043, 'CORE':
   6674090}`, the counts of 2 October;
3. runs the three mutant covers, each the cover with one tight family lighter by a
   relative $10^{-4}$, under the fixed code: Tier B returns `'ok': False` with an exact
   pose of mass below 1 for M1 on both sides of $u = 0$ and for M3, and the driver
   reports two counterexamples and `NOT VERIFIED` for M2.

Exit 0, 427 s of wall and 408 CPU-s on a 4-core container shared with another lane, from
2026-10-05T04:24:41Z.

**The fixes** ([`receipts/valid7_fix_probe.json`](receipts/valid7_fix_probe.json)),
written by [`devtools.probe_valid7_fixes`](../../../devtools/probe_valid7_fixes.py) in
the same interpreter, against the retained `src/` of both packets.
At the first commit `nonneg_open` accepts $-(u - \tfrac12)^2$ on $(0, 1)$, `nonneg_on`
accepts $u(u - 1)$ on $[0, 2]$ (the review’s example) and $-u^2 (u - 1)^2$ on $[0, 1]$
(the author’s), and `tier_b2.py` calls `hash(`. At this commit all three polynomials are
refused, `hash(` is gone, and $(u - \tfrac12)^2$ on $(0, 1)$ and $u(2 - u)$ on $[0, 2]$
are still accepted.
[`packing/tests/test_probe_valid7_fixes.py`](../../../tests/test_probe_valid7_fixes.py)
holds the receipt.

### What the Replay Establishes, and What It Does Not

It establishes that the fixed record checker accepts the unchanged published records,
re-certifying 2,000 Tier A and 300 Tier B leaves of another random sample under the
fixed code, and that the fixed code still refuses the three lighter covers.
It establishes that the fixed `nonneg_open` and `nonneg_on` refuse the review’s
counterexamples.

It does not re-certify the other 9.6 million leaves, which is what the full replay of 2
and 3 October did, with D-1 guarded, under the first commit’s V2 code.
That replay stands: the guard made the one case D-1 names a refusal, and it refused
nothing. Nor was the fixed code reviewed line by line here; the diff is four files, and
the record above says what it changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
