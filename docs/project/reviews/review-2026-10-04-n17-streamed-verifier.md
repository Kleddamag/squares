---
title: n17 Streamed Kernel Verifier Review
date: 2026-10-04
status: planning-review
---
# n17 Streamed Kernel Verifier Review

**Session:** 168, lane R8 (independent adversarial reviewer), bead `think-2dpm`.
**Reviewed:** the standing kernel verifier
`packing/devtools/verify_n17_kernel_certificate.py` at `601bbf110` (Git blob
`1ad706c2…`, lane M1’s change) against the listed `318c28c42` (blob `859b6c56…`).
`git diff 318c28c42 601bbf110` touches the verifier (177 lines added, 11 removed) and
its test file (61 added), nothing else.
The file is unchanged from `601bbf110` to `e145e6b4d`, where every run below was made.
**Question:** may the ledger
`packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml` list
`601bbf110` under `verifiers:`, so that a full pass at it admits an n17 kernel
certificate?
**Method:** the diff read in full, beside the checker’s own streaming reader
(`check_n17_subpattern.stream_node`) and the two earlier reviews of this verifier
(`review-2026-10-02-n17-w7-closure.md`, `review-2026-10-03-n17-verifier-rewrites.md`);
then tools of my own, kept with their logs and receipts under
`packing/campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/streamed-reader/`:
`nodestream_differential.py.txt` (the reader against `json.loads` on generated and
damaged nodes), `nodestream_saved_check.py.txt` (every saved node read and held to its
bytes), `memo_audit.py.txt` (the memos traced, removed and mutated),
`run_mutants.py.txt` with `mutant_plugin.py.txt` (13 mutants of the new code against
three checks), `escapes.py.txt` and `number_guard_demo.py.txt`, and `run_full.py.txt`,
`measure.py.txt` and `compare_receipts.py.txt` for the full re-verifications.
Nothing in the repository was edited except this document, that directory, a new test
file `packing/tests/test_verify_n17_node_stream.py`, and the ledger listing of section
7\. The verifier is untouched.

## Verdict

**ADMIT.** No blocking finding and no condition.

- **The reader is sound.** For every input tried, `NodeStream` either yields exactly
  what `json.loads` of the decompressed file yields, member by member and step by step,
  with that document’s content id, or refuses before it sets a content id: 0 divergences
  in 440,079 reads of 6,000 generated nodes and their damaged variants, at read sizes
  down to one byte. The verifier cannot pass a node it has not read to the end.
  Every saved node, 30 distinct content ids (the four under `packing/campaign/` and 26
  more in the session’s lane directories), is canonical JSON whose bytes equal, byte for
  byte, the canonical re-serialisation of what the reader yields.
- **The memo bounds change nothing proved.** Both bounded memos hold pure functions of
  their keys, are read only by accessors that recompute on a miss, and a missing entry
  read as absent would fail toward refusal, not acceptance.
  A replaced hull’s regions are not asked for again on W7, SW9 or N1, and would be
  recomputed if they were.
- **The refusals cost nothing in the record.** No saved node has a member out of
  canonical order, a repeated member, or anything but UTF-8.
- **W7, SW9 and N1 re-verify in full** at this revision, PASS, every receipt field equal
  to the receipt recorded at the entry’s listed revision and to the `318c28c42` runs,
  with peaks of 199, 244 and 283 MB. With the listing below, the census counts these
  three receipts under it; without it, it refuses them.

The committed tests at `601bbf110` miss three mutants of the new code and never replace
an owned hull, so the memo drop they describe does not run in them (N1). The 2026-10-03
review made missed mutants a condition because they weakened the verifier; none of these
three does, so here it is a note.
This review’s test file catches all three and runs the drop; it should be committed with
the listing, and is in this patch.

## Findings

Severity: **blocking** would let a false certificate pass, or a receipt name objects
other than the ones checked; a **condition** would have to land with the listing; a
**note** changes no verdict.

| ID | Severity | Finding |
| --- | --- | --- |
| N1 | Note | The committed tests miss three mutants of the new code, none of them weakening: a reader without its split-number guard (it refuses valid nodes), a content id hashing early members in file order (it changes the id of a non-canonical file), and a drop of the new hull’s regions instead of the old (it costs time). Their fixtures never replace a hull. The new tests catch all three (sections 2.4, 3.3, 3.4). |
| N2 | Note | The reader is written apart from the checker’s but follows the same design step for step, so an error in that design would be common to both (section 2.5). |
| N3 | Note, pre-existing | Four kinds of damage end `verify` with an uncaught exception and no receipt, at this revision and at `318c28c42` alike; none is a PASS (section 2.6). |
| N4 | Note | The new refusals reject inputs that `json.loads` of the bytes accepts: a byte-order mark, UTF-16 or UTF-32, a UTF-8-encoded surrogate, a repeated top-level member, a member sorting before `steps` placed after it. None occurs in a saved node (section 4). |
| N5 | Note | The memory bound is about a step for a well-formed node only, and a step can be large: the largest pending certificate has a 118.6 MB step, and the reader alone peaked at 1,022 MB on it (section 4). |
| N6 | Note | Two statements in the record are inexact: the commit says the imports are unchanged (`codecs` and `Iterator` were added, both standard library), and M1’s memo test says the regions of every replaced hull are dropped in it (its fixtures replace none). |

## 1. What Changed

Three things, and nothing else in the module:

- **The node is streamed.** `verify_objects` reads the seed whole, as before, and the
  node through `NodeStream` (lines 771–880): the members before `steps` into `header`
  when the object is opened, then the steps one at a time from `steps()`, then the
  members after the array, and only then `sha256`, the content id.
  The closure path now asks `next(steps, None) is None` (line 1418) where it asked
  `si == len(steps) - 1`, and the receipt requires `stream.sha256` to be set (line
  1422). `load_object` is refactored around a shared `canonical`.
- **Two memos are bounded.** `bound_memos` (lines 1323–1338) runs after each step: when
  the step changed its owner’s hull it removes every forbidden region keyed on the hull
  the step replaced, and when the facet memo holds more than $2^{15}$ pairs it empties
  it.
- **Input is stricter.** A repeated top-level member, a member sorting before `steps`
  that follows it, a node without `steps`, and anything that does not decode as UTF-8
  are refused.

The imports gain `codecs` and `collections.abc.Iterator`, both standard library; the
committed `test_a_verifier_imports_no_producer_checker_or_solver` passes.

## 2. The Reader Is Sound

### 2.1 The Argument

The claim is that an accepted node’s header and steps are `json.loads`’s document and
its content id is `sha256(canonical(document))`.

- **Decoding.** `gunzip_text` (line 762) reads `gzip.open` in 1 MiB blocks through a
  strict incremental UTF-8 decoder.
  `gzip.open` and `gzip.decompress` give the same bytes for every stream both accept,
  including several members and zero padding; a bad checksum, trailing garbage or a cut
  stream raises in both.
  `json.loads` of bytes picks UTF-8, UTF-16 or UTF-32 by the first bytes and decodes
  with `surrogatepass`. On any input the reader accepts, the first character that is not
  JSON whitespace is `{`, so neither of the first two bytes is zero and there is no
  byte-order mark: `json.loads` chooses UTF-8 too, and `surrogatepass` matters only for
  an encoded surrogate, which the strict decoder refuses.
  So the reader sees exactly the text `json.loads` sees.
- **Values.** Every value is parsed by `json.JSONDecoder().raw_decode`, the decoder
  `json.loads` uses, with the same defaults: the same numbers, `NaN` and infinities,
  escapes, surrogate pairs, lone surrogates, and the last of a repeated name inside a
  step. A value that does not parse in the buffer is retried after the buffer has grown
  by at least as much again (`_fill`), and raises only when the file is exhausted, so a
  value split between reads is parsed whole.
- **A value cut by the buffer’s end.** Strings, arrays, objects and the literals end at
  a character the scanner must see, so a parse that succeeds in a prefix succeeds with
  the same value in the whole text.
  Only a number can parse shorter in a prefix.
  If it does, the character after the shorter match is part of the longer one (a digit,
  `.`, `e`, `E`, `+` or `-`) or the buffer has ended; none of those is in `AFTER_VALUE`
  (blank, `,`, `:`, `]`, `}`), so the guard at line 877 refuses the short value and the
  read continues. Without the guard a cut number would still not be accepted: the rest of
  it is the next character read, and the separator check refuses it.
  The guard is what lets a valid node whose number straddles a read through.
- **The object and the array.** `__init__`, `steps()` and `_name` parse `{`, members
  `"name":value` separated by `,`, the `[...]` of `steps`, and `}`, with JSON whitespace
  free between tokens, as `json`’s scanner does; a trailing comma, a missing separator,
  a non-string name or a non-array `steps` is refused, as `json` refuses or the verifier
  would. After the closing brace only whitespace may follow (line 826), as for
  `json.loads`.
- **Names.** A repeated top-level name is refused (line 863), where `json.loads` keeps
  the last; a name sorting before `steps` after the array is refused (line 823). So
  every accepted node has distinct names and the header is the document less `steps`.
- **The content id.** Each step is hashed as `canonical(step)` before it is yielded, and
  the members before `steps` in name order when the array opens, the members after it in
  name order once it closes (`_member` encodes a name as `json.dumps` encodes a dict
  key). That is the byte sequence `json.dumps(document, sort_keys=True,
  separators=(",", ":"))` writes, since a member sorting after `steps` that the file
  placed before it is hashed at the end with the others.
  The verifier mutates no parsed value before it is hashed.
- **The end.** `sha256` is set only after the closing brace and the end-of-file check.
  The closure path calls `next(steps)` after the closure step, which reads on to the end
  or refuses, and the stall path leaves its loop only when `steps()` returns; line 1422
  then requires the content id.
  A node whose tail is cut, or that carries a step after its closure, fails.

### 2.2 Differential Evidence

`nodestream_differential.py.txt` generates node texts from a seeded generator: random
JSON whitespace between every pair of tokens; strings with short escapes, `\u` escapes,
surrogate pairs as escapes, lone surrogates, control characters, raw non-ASCII and
astral characters; numbers in every form the grammar allows, `-0`, `1e400`, `NaN`,
`Infinity` and `-Infinity`; repeated names inside steps; nesting; and members that sort
after `steps` on either side of the array.
Each text is gzipped and varied: cut at random points, single bytes changed, data
appended, members moved or repeated, a byte-order mark, UTF-16 with and without one, an
encoded surrogate, two gzip members split at a random byte, gzip padding, trailing
garbage, a bad checksum and a cut gzip stream.
Each variant is read at three of eight read sizes (1, 2, 3, 5, 7, 13, 64 bytes and 1
MiB); each valid text at all eight.

| Seed | Nodes | Reads | Divergences | Refusals where `json.loads` accepts |
| --- | ---: | ---: | ---: | --- |
| 20261004 | 3,000 | 220,032 | 0 | the five classes of N4, and 480 byte changes that renamed `steps`, or renamed a member after the array to one sorting before `steps` |
| 7 | 3,000 | 220,047 | 0 | the same classes; 447 byte changes of the same two kinds |

A divergence is a read that completes where `json.loads` refuses, or that completes with
any difference in a member, a step, a value’s type, or the content id.

### 2.3 The Tail Must Be Read

The blind-pair closure closes at its only step, so every mathematical check passes
before its file runs out.
Cut at nine points from inside that step to the last brace, with its gzip stream cut
twice, or with `{}` appended, it never passes
(`test_a_closure_whose_node_is_cut_after_its_last_step_never_passes`); undamaged, it
does.

### 2.4 Mutants of the Reader

`run_mutants.py.txt` writes each mutant to a scratch copy and binds it under the
committed module’s name (`mutant_plugin.py.txt`). Each runs against the committed tests
of `601bbf110` (`old`, 73 tests), this review’s new test file (`new`, 33), and the
differential harness at 300 nodes (`diff`).

| Mutant | What it changes | `old` | `new` | `diff` |
| --- | --- | --- | --- | --- |
| `reader-number-at-buffer-end` | a value ending at the buffer’s end is taken as read | missed | caught | caught |
| `reader-order-unchecked` | a member sorting before `steps` is accepted after the array | caught | caught | caught |
| `reader-repeats-allowed` | a repeated top-level member is read as `json.loads` reads it | caught | caught | agrees with `json.loads` |
| `reader-trailing-data` | data after the closing brace is ignored | caught | caught | caught |
| `reader-step-separator-free` | any character separates steps | caught | caught | caught |
| `reader-hash-skips-late-members` | the members after `steps` are left out of the content id | caught | caught | caught |
| `reader-hash-in-file-order` | the members before `steps` are hashed in file order | missed | caught | caught |
| `verify-stops-at-the-closure` | no read past the closure step, and no end required | caught | caught | not applicable |
| `verify-no-end-check` | only line 1422 removed | missed | missed | not applicable |

`verify-no-end-check` is equivalent: the closure path reads to the end through
`next(steps)` at line 1418, and the stall path leaves its loop only when `steps()`
returns, so line 1422 can never fail.
`verify-stops-at-the-closure` fails every valid certificate, since `terminal` sorts
after `steps` and is never read.
`reader-hash-in-file-order` changes the content id only of a node whose early members
are out of name order; the old tests’ re-spaced node is re-written from a sorted
document, so they never present one.
The id it gives still binds the content, so it is not a weakening either; the census
would refuse the receipt for naming other objects.

The committed tests do not catch the mutant without the number guard.
Their step-at-a-time test reads at five bytes, but neither the blind pair’s node nor any
saved node has a bare number as a top-level value (`B` and `U` are strings, `mask_index`
is null), and a number inside a step is never at the end of the buffer when the step
parses.
The mutant cannot accept a cut number, though: the rest of the number is the next
character the reader sees, and a digit, `.`, `e` or sign fails the separator check.
A node declaring `"B":10` whose first read ends after the `1` is refused by the mutant
with “the node’s members are not comma-separated”, and by the committed verifier with
“field and physical coordinates differ” (`number-guard-demo.log`). So the guard keeps
the reader complete, not sound, and its gap in the committed tests is a note (N1). The
new tests catch the mutant on their first generated node.

### 2.5 Independence

`NodeStream` imports nothing from the checker, and `codecs` is its only new import.
It does follow `check_n17_subpattern`’s `GzipJsonText`, `SavedSteps` and `stream_node`
step for step: the same `raw_decode` loop with the buffer grown by at least as much
again, the same `AFTER_VALUE` set and the same comment on it, the same rule for members
after `steps`, the same hashing order and the same 1 MiB read.
It is independent code but not an independent design, so a flaw in the design would be
common to the checker and the verifier.
This review therefore does not rest the reader on independence: it holds it to
`json.loads`, a third implementation, and holds every saved node’s bytes to the reader’s
output (section 4). The new tests keep that check in the suite.

### 2.6 Inputs That End the Run Without a Receipt

`verify` turns a `VerificationError` and seven exception types into a FAIL receipt.
Four malformations raise something else, so the command exits with a traceback and
writes no receipt (`escapes.py.txt`, `escapes.log`):

| Damage to the blind-pair closure | `601bbf110` | `318c28c42` |
| --- | --- | --- |
| `Infinity` or `1e400` as a coordinate | `OverflowError` escapes | the same |
| `NaN` as a coordinate | FAIL, malformed | the same |
| gzip stream cut | `EOFError` escapes | the same |
| deflate data corrupted | `zlib.error` escapes | the same |
| an array nested 100,000 deep in a step | `RecursionError` escapes | the same |

None is a PASS and none is new, so none bears on the listing.
Catching them, so that every damaged certificate gets a FAIL receipt, is a change for
another lane.

## 3. The Memo Bounds Change Nothing Proved

### 3.1 What Is Memoised and Why a Drop Only Costs Time

| Memo | Key | Value | Bound | Read by |
| --- | --- | --- | --- | --- |
| `State.facets` | the partner core and the row core as tuples of homogeneous integer vertices | `difference_facets(partner, core)`, which reads only those two tuples | emptied after a step that leaves more than $2^{15}$ pairs | `State.difference` (line 911): look up, and on a miss compute and store |
| `State.forbidden` | `(tuple(owned hull), tuple(core))`, exact `Fraction` points | `minkowski_diff(hull, core)`, which reads only those points | every entry keyed on the hull a step replaced is removed after that step | `State.forbidden_region` (line 918): the same |

Each value is a pure function of exact inputs that equal keys make equal: the facet key
is the argument pair itself, and the forbidden key is the two argument lists as tuples,
element for element.
No caller mutates a value: the collision loop iterates the facets, and the cover builds
new lists from the regions.
`CoverRow.minima` and `Row.cover` are unbounded and unchanged.

A removed entry is therefore recomputed, equal, on its next use.
The AST of the module shows that the only functions touching `.facets` or `.forbidden`
are the two accessors and `bound_memos`, which only removes
(`test_the_memos_are_reached_only_through_their_accessors`), so no path reads a removed
entry as absent. Had one done so, it would fail toward refusal: a forbidden region read
as missing leaves the cover with fewer regions, and a facet set read as empty meets
`require(len(facets) >= 3)` at line 1070. Section 3.4 shows both mutants refusing.

### 3.2 The Replaced Hull

`forbidden_region` is called from one place, `check_cover` (line 1097), with
`state.groups[oj]`, the current hull of each other owner.
After the step in which an owner’s hull is replaced, the old vertex list is no longer
any owner’s current hull unless another owner has the same list or the owner’s hull
returns to it; in either case the region is recomputed.
`compress` replaces the hull with a new list and never mutates the old one, so `before`
(line 1389) still holds the replaced value when `bound_memos` compares it.

Traced in full on the admitted certificates (`memo_audit.py.txt`, mode `trace`):

| Certificate | Hull replacements | Regions dropped | Later lookups of a dropped hull | Region lookups, computed | Largest facet memo | Facet clears |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| W7 8-bin fixture (stall) | 1 | 8 | 0 | 192, 24 | 64 | 0 |
| W7 | 50 | 2,816 | 0 | 16,252, 3,264 | 4,096 | 0 |
| SW9 | 97 | 8,730 | 0 | 23,864, 9,361 | 22,529 | 0 |
| N1 | 55 | 1,280 | 0 | 26,278, 1,824 | 1,024 | 0 |

Every receipt of the traced runs equals the untraced one.
No dropped hull was asked for again, so on these certificates the drop removed only
entries that could not be read.
The facet memo stayed below $2^{15}$ on all three, the adaptive SW9 included, so the
clear never fired on an admitted certificate; it is exercised by the unit test, by M1’s
test with the bound at zero, and, per M1’s commit, on W7-split and SW8.

### 3.3 Equivalence

On the blind and wall pairs with refined rows, the receipt with no memo at all, and the
receipt with both memos emptied after every step, equal the bounded verifier’s in every
field but `seconds` (`test_no_memo_and_an_emptied_memo_give_the_same_receipt`). Neither
pair ever replaces an owned hull (N1): M1’s
`test_the_kernel_verifier_bounds_its_memos_without_changing_a_count` says the regions of
every replaced hull are dropped in it, and none is.
The W7 8-bin fixture replaces one hull (8 entries dropped); its receipt with no memo
equals the bounded one
(`test_the_w7_fixture_replaces_a_hull_and_its_receipt_needs_no_memo`, marked slow), and
two unit tests check the drop and the clear directly.
On the full certificates the receipts of section 5 equal those written at `318c28c42`,
whose memos were unbounded.

### 3.4 Mutants of the Memos

Run as in section 2.4 (`old`, `new`; the differential harness does not reach the memos):

| Mutant | What it changes | `old` | `new` |
| --- | --- | --- | --- |
| `memo-drops-the-new-hull` | the regions of the step’s new hull are removed instead of the replaced one’s | missed | caught |
| `memo-forbidden-absent-is-none` | the cover reads the forbidden memo directly, a missing entry as no region | caught | caught |
| `memo-facets-absent-is-none` | the collision check reads the facet memo directly, a missing entry as no facet | caught | caught |
| `memo-facets-absent-is-none-unguarded` | the same, without the three-facet guard: a vacuous collision check | caught | caught |

The first is safe, since a miss recomputes, and only the new unit test sees it.
The second and third are the “absent means not needed” error and fail every certificate
that needs a forbidden region or a facet, which is to say they refuse.
The fourth is the one weakening mutant here.
Among the committed tests only `test_the_kernel_verifier_checks_every_live_partner_row`
refuses it.
The doctored closure `shift_region`, which looks as if it tests the collision
set, fails earlier at the required-domain check (“collision region escapes the required
domain”) under the committed verifier and under the mutant alike, and its expected
“escapes” matches both.

## 4. The Refusals Cost Nothing in the Record

`nodestream_saved_check.py.txt` reads each node with `NodeStream` and, at a second
`gzip` reader’s pace, compares the decompressed bytes with the canonical JSON re-written
from what the reader yielded.
Equal bytes mean the file is canonical, its members are in canonical order, and
`json.loads` would give what the reader gave.

| Nodes | Read to the end | Name is the content id | Bytes are canonical | Members after `steps` |
| --- | ---: | ---: | ---: | --- |
| All `node-*.json.gz` under `packing/campaign/` (W7, SW9, N1 and the W7 8-bin fixture) | 4 of 4 | 4 | 4 | `terminal` only, after the array |
| Every distinct node in the session’s lane directories (29 content ids, three of them the record’s; among the rest W7-split, SW8 and the pending flag 2 and flag 3 certificates) | 29 of 29 | 29 | 29 | `terminal` only, after the array |

That is 30 distinct nodes.
Every one has the same sixteen members before `steps` and `terminal` after it.
None would meet a new refusal.
The largest step is 118.6 MB of JSON, in the pending flag 2 certificate split to 2,304
rows (`node-3de853f3…`, 303 MB compressed).
The reader alone peaked at 1,022 MB on it, so a verification of that certificate should
be planned for about a step’s worth of parsed objects on top, not for the 200 to 300 MB
measured on the admitted three (N5). A malformed value is retried until the file is
exhausted, so a damaged node may be buffered whole before it is refused.

## 5. Re-Verification

Each admitted kernel certificate, verified in full by the committed command at
`e145e6b4d` (the verifier’s blob `1ad706c2…`, the file of `601bbf110`, `dirty: false`),
one at a time, while two capture pilots and a kernel run shared the machine
(`run_full.py.txt`; receipts `full-W7.json`, `full-SW9.json`, `full-N1.json`):

| Entry | Status | Seconds | Peak RSS | Closure | Facet checks | Rows in full | Against the recorded receipts |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| W7 | PASS | 227 | 199 MB | owner 5, step 57 | 30,952,184 | 3,324 | all 23 shared fields equal to `certificates/W7/verification.json` (at `556561586`) and to `full-fixed-W7.json` (at `318c28c42`) |
| SW9 | PASS | 278 | 244 MB | owner 5, step 101 | 28,321,424 | 3,359 | all 23 equal to `certificates/flag3-a9-pending/verification.json` (at `fd2c9602e`) and to `full-fixed-flag3-a9-pending.json` |
| N1 | PASS | 450 | 283 MB | owner 18, step 81 | 16,709,184 | 2,611 | all 23 equal to `certificates/N1-state-pending/verification.json` (at `ae4f5fb43`) and to `full-fixed-N1-state-pending.json` |

The fields compared are every top-level field and every count except `seconds` and the
verifier’s own identity (`provenance`, or `verifier_sha256` in W7’s earlier receipt):
schema, verifier, directory, cells source, mode, sample settings, both content ids,
mask, cells, bins, closure, closed, status, failure, and the eight counts
(`compare_receipts.py.txt`). The only difference anywhere is in N1’s
`verification-5c550f7c.json`, a review receipt that names its directory relative to
`packing/`.

For scale, `318c28c42`’s verifier on W7, run the same way just after (`measure.py.txt`,
`peak-318c28c42-W7.log`): PASS, 258 s, peak 552 MB, its receipt equal to this revision’s
in every field.
This revision peaked at 199 MB on the same certificate, in line with M1’s
598 to 258 MB on W7-split.

## 6. Tests Added

`packing/tests/test_verify_n17_node_stream.py`, 33 tests (one marked slow), all passing;
the 73 tests of `test_verify_n17_certificates.py` still pass.

- `test_the_node_stream_reads_what_json_reads`: 120 generated nodes at five read sizes
  down to one byte.
- `test_a_cut_or_damaged_node_is_refused_or_read_exactly`: every prefix of two nodes,
  sampled prefixes of 22 more, byte changes and appended data; whatever the reader
  accepts equals `json.loads`.
- `test_the_node_stream_reads_what_json_reads_at_the_edges` (8 cases) and
  `test_the_node_stream_refuses_input_json_would_read_otherwise_or_not_at_all` (14
  cases): `NaN` and the infinities, repeated names in a step, a late member before
  `steps`, an escaped `steps`, surrogates, blanks, several gzip members and padding; and
  each refusal of N4, data after the node, a missing or non-array `steps`, trailing
  commas, and three kinds of damaged gzip stream.
- `test_a_closure_whose_node_is_cut_after_its_last_step_never_passes` (section 2.3).
- `test_the_memos_are_reached_only_through_their_accessors`,
  `test_a_replaced_hull_loses_only_its_own_regions_and_recomputes_them`,
  `test_the_facet_memo_is_cleared_only_past_its_bound`,
  `test_no_memo_and_an_emptied_memo_give_the_same_receipt` (four cases) and the slow
  `test_the_w7_fixture_replaces_a_hull_and_its_receipt_needs_no_memo` (section 3).

## 7. The Ledger

**`601bbf110` can be listed, with this review’s tests committed beside it.** The listing
added to `certified-sub-patterns.yaml` in this patch:

```yaml
  - path: packing/devtools/verify_n17_kernel_certificate.py
    revision: 601bbf1107a622b306a3fe1fc57faebc9e28d27f
    review: docs/project/reviews/review-2026-10-04-n17-streamed-verifier.md
```

It carries no `admits`: the cover fix of `318c28c42` is unchanged in it, and nothing
found here limits which entries it may verify.
The three receipts of section 5 were written at `e145e6b4d`, where the file is
`601bbf110`’s, with `dirty: false`. With a copy of the patched ledger whose W7, SW9 and
N1 entries point at them, the census admits all four entries under this review and
reports what it reports with their own receipts, 126,168 surviving states in 15,953
orbits; with the same copy less this listing it refuses W7 (“is not a reviewed
verifier”). The patched ledger itself keeps the entries’ existing verifications, which
stand, and gives the same count; the 22 census tests pass.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured, this review | the 440,079 differential reads; the 33 node files (30 distinct) held to their bytes; the census with and without the listing; the tail cuts; the 13 mutants against three checks; the escapes at both revisions; the memo traces and the no-memo and emptied-memo receipts; the three full re-verifications and their field-for-field comparison; the 33 new tests and the 73 existing ones |
| Read from code, this review | the argument of section 2.1; the purity, readers and replaced-hull argument of sections 3.1 and 3.2; the comparison with the checker’s reader |
| Taken from the record | the receipts at the entries’ listed revisions and at `318c28c42`; M1’s W7-split and SW8 measurements in the commit message |
| Not checked here | the mathematics unchanged since `318c28c42` (reviewed in `review-2026-10-03-n17-verifier-rewrites.md`); the producer and checker |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
