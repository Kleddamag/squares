# The Result Import Process: Process Review

**Date:** 2026-10-01

**Reviewer:** Claude (Opus 5.5), coordinating three read-only audit lanes (Opus 5.5 at
extra-high reasoning), for the repository owner

**Workflow:** W4 process review, process focus

**Tracking:** `think-5xr9`, under the results-register epic `think-z9wy`

## Summary

The owner asked for a review of the recent GitHub issues and of how results by Evan
Daniel and others were taken in, and for the process of importing, recording,
validating, rating and documenting such results to be written down so that it can be
repeated for every new issue.

The work on each result was sound and followed one shape.
The process around it did not: it was written in four places under no one name, each
import declared a different sequence of workflows or none, and three of its steps had no
owner. The consequences are visible on the issues.
Every rung an author has been told is now different on `main`, one author was given a
`T-NNN` that now names another result, five requests have no reply, and about 45
CPU-hours of replay never reached the record.

This change writes the process down once, as
[the result import process](../../../packing/campaign/result-import.md), and fits it to
the workflow contracts as a standard sequence of existing phases.
[Decisions for the Owner](#decisions-for-the-owner) lists seven points it leaves open.
[The first-application plan](../specs/active/plan-2026-10-01-result-import-first-application.md)
applies it to the six requests now waiting.

## What Was Reviewed

- **Issues:** 170, 227, 238, 247, 256 and 279 to 282, with every comment, as they stood
  on 2026-10-01 at about 23:00 UTC.
- **Records:** the 29 register entries `T-037` to `T-065`, all of which carry an
  `attribution`, with their evidence, packets, coverage entries, bibliography keys, case
  records and review documents, at `origin/main` `eaa1a4b45`.
- **History:** the session records from 149 on, the eleven pull requests that carried
  imports, and the commits behind each stage.

Three lanes worked without shared context.
One built a step-by-step fidelity matrix for the 29 entries and read every checker that
gates these records.
One derived `V` and `C` by hand for each entry from the predicates of
[`epistemics.md`](../../../epistemics.md) and compared the significance scores.
One reconstructed each import’s timeline and declared phases from Git and GitHub.
No replay was run, no packet was re-hashed against its upstream, and no review’s
mathematics was judged.

## How Well the Written Procedure Was Followed

`check_results`, `check_source_coverage` and `state_ai_assistance --check` all pass on
the reviewed tree, so every gap below is one the gate accepts today.

| Step of the procedure | Followed | Gaps |
| --- | --- | --- |
| Source retained at a pinned revision | All 17 packets exist, have a README and record a pin | Nine packet shapes; no schema for the acquisition record, which three tools write with different fields; the directory date is the source’s date in six packets and the retrieval date in the rest |
| Coverage entry | 18 of 20 source keys | None for `[wand125 rectangle bounds 2026-09-28]` (`T-046`) or `[wand125 tools 2026]` (`T-058`, `T-059`) |
| Bibliography key with `dated`, `credit`, `lineage` | 20 of 20 | The three dates of a source disagree on nine entries with no stated rule; credit lines were corrected after the fact in at least six commits |
| Reported lane and typed evidence | Every entry that holds a lane is cited there | `T-055` is reported and not in the reported lane; `T-045` claims $n = 32$ with no evidence entry covering it; no case record cites `T-058` or `T-059` |
| Register entry at import | All required fields on 29 of 29 | `T-037` to `T-055` were registered in one batch on 29 September, up to eight days after they were acted on; three entries were renumbered after id collisions |
| Verified lane after replay and review | Every entry in a verified lane has a mapped review | The review is linked in four different places and typed in `reviews` on one entry; `T-056` and `T-057` replay entries name no review |
| Disagreement preserved | `T-056` carries three typed conflicts | Nothing for a reported lower bound awaiting replay |
| Author answered | Issues 227, 238 and 247 | Issue 170 was never answered and its author closed it; issue 256 was registered as `T-062` and `T-063` with no reply; every answer given is now stale |

Six steps are held by no check: that a packet and a coverage entry exist; that credit
comes from the source’s files; that an upper bound by others is registered; that
evidence covers an entry’s scope; that the verified lane waits for a replay here and a
review; and that the author is answered.

## How the Work Was Run

The written procedure changed during the period.
Until 29 September it had six steps, no register entry at import and no reply step; the
“W1/W2 Intake” subsection of the synopsis dates from 30 September.

Each import did the same five things: retain the source at a pin; replay the certificate
and review the mathematics in parallel; register and regenerate the views; merge `main`,
renumber and re-pin; and, sometimes, reply.
The declared workflows varied every time.

| Import | Declared sequence |
| --- | --- |
| Session 149, Guzhou R012 and Mira | W1 → W2 → W8 |
| Session 150, Kleddamag $n = 17$ | W9 → W1 → W2 → W10 |
| Session 152, Tokoharu, Kleddamag $n = 11$, wand125 points | W2 |
| Session 159, Guzhou R052 | W2 → W10 |
| Session 160, Kleddamag, Daniel, wand125 rectangles | W2 → W10 → W2 |
| Session 161, wand125’s update and the 28 September results | W1 → W2 |
| Session 162, wand125 tools | W2 → W7 → W8 → W8, reconstructed afterwards |
| Session 164, including the `T-060` source | W7 throughout |
| Pull requests 243, 245, 248, 249, 258 | None |
| Pull request 267, Daniel’s October survey | W1 and W2, named in its review documents only |

Retention was declared as W1 in three sessions and done inside W2 elsewhere.
Registration and publication were declared as W8 twice and done inside W2 elsewhere.
Integration and the reply were never a declared phase.

| Import | Source public to first seen here | First seen to `main` | Request to first reply |
| --- | --- | --- | --- |
| `T-032`, Guzhou R012 and Mira | Same day; Mira 13 days | 34 h | No issue |
| `T-039`, Guzhou R052 | Same day | 59 h | No issue |
| `T-044`, wand125 points, issue 170 | 8 days after the issue | 10 h | Never |
| `T-049` to `T-051`, Daniel, issue 238 | 1 day; $s(12)$ 33 days | 18 h | 33 h |
| `T-056`, `T-057`, Couzo and de Winter, issue 227 | 6 days after the issue; de Winter 13 days | 13 h | 6.4 days |
| `T-061`, Wang and Li, issue 247 | Same day | 36 h | 16 h |
| `T-062` to `T-064`, Daniel, issue 256 | 1 to 3 days | 10 h | None yet |

## Failure Modes

Ordered by how often each recurred.
`packing/defects.yaml` records none of them, since its scope is the toolchain.

1. **Text left stale by a later change.** Every rung quoted in a reply is now wrong on
   `main`, because the ladder changed on 30 September.
   A review of pull request 245 found the old rung standing in five places after an
   entry was raised. The runbook’s answer: reply after the merge and from `main`, and
   post a follow-up when an id or a rung changes.
2. **Replay evidence that never reached `main`.** The $s(21)$ and $s(45)$ re-sweeps,
   about 45 CPU-hours, stayed in a session’s scratch space and were lost.
   Twenty-one rectangle replays for `T-046`, and the replays for `T-048` and `T-055`,
   passed on 29 September and sit on unmerged branches while their entries read `V0/C0`.
   The runbook’s answer: receipts are committed and pushed when a run ends, and the bead
   names the branch.
3. **Results found late.** Daniel’s $s(12)$ bound was public for 33 days, during which
   this project registered its own weaker bound as apparently novel.
   Issues 170 and 227 waited eight and six days.
   The runbook’s answer: triage starts when an issue is opened, with an acknowledgement
   within a day.
4. **Credit corrected after the fact**, in at least six commits, one of them correcting
   its predecessor 25 minutes later.
   The runbook’s answer: credit is read from the source’s attribution files at the pin,
   during stage 2.
5. **Identifier collisions.** `T-031`, `T-056` and `T-057`, and `T-058` each collided
   between two branches.
   The third was foreseen six hours before issue 247 was told `T-058`. The runbook’s
   answer: take the id last, merge the import the same day, and state no id outside the
   repository until it is on `main`.
6. **Integration churn.** Thirty-one commits across eleven pull requests re-pinned the
   data revision or re-stamped the atlas.
   The runbook’s answer: a small import pull request that merges the same day.
   Since pull request 285 the re-pin is one line.
7. **Missing session records.** Five import pull requests had none, and session 162’s
   was reconstructed. The runbook’s answer: one bead for each import.
   A routine import needs no session record, as the synopsis already says.

## How the Ratings Were Assessed

**Verification and confirmation.** A hand derivation from the predicates agrees with the
declared rungs on 30 of 31 entries.
Two ambiguities remain.

- `epistemics.md` defines `V` twice.
  Its axis table says `V` is the verification a result carries “as certified by its own
  source” and needs no replay here.
  Its section on results by others says a reported result enters at `V0/C0`. Six entries
  whose sources ship a machine certificate and report a passing run of their own sit at
  `V0`: `T-046`, `T-048`, `T-055`, `T-062`, `T-063` and `T-064`. The cause is
  mechanical: the source’s claim is typed `assurance: reported`, which may not carry a
  `method`, and the derivation reads `method` only.
  The evidence contract already admits the other typing, a `verified` machine entry of
  `origin: external`, which derives `V3/C0`; no entry uses it.
- A result’s scope is not held to its evidence’s scope.
  `T-045` claims $s(32) \ge 119/20$ and cites one entry whose scope is 27, 28 and 31.

**Significance.** No rule said whether a score is of the claim or of its confirmation,
who scores, or when a score is revisited, and practice was mixed.
Twenty-three scores are marked drafts.
On three of them the marker and the issue number are lost, because
`by: issue #227 intake …` is read by YAML as the one word `issue`. The rationales do not
explain these pairs:

| Pair | Scores | What the rationales leave unexplained |
| --- | --- | --- |
| `T-062`, $s(60) = 8$, against `T-051` to `T-053` | S3, S4 | The same technique and the next member of the same family |
| `T-061`, $+3.9 \times 10^{-9}$ at $n = 11$, against `T-022` | S2, S5 | Both spend the slack of an existing certificate at a central case |
| `T-065`, Bidwell’s packing verified, against `T-011`, Trump’s | S3, S2 | Both are the first exact check here of a long-standing packing |
| `T-063`, $s(61) = 8$, against `T-016` | S1, S3 | Both are one-line monotone corollaries |
| `T-044`, `T-046`, `T-056` against `T-019`, `T-020` | S3, S4 | “Bound family” is applied to three counts and not to 14, 48 or 49 |

Working rules that scorers cite live inside rationale fields, not in `epistemics.md`:
the calibration note in `T-020`, the `T-015` and `T-032` precedent, and `T-042` as the
precedent for scoring a step by what it changes.

## The Decision: A Sequence of Existing Workflows

The question was whether importing a result is a workflow of its own or an orchestration
of the existing ones.
The workflow contracts answer it.

| Test from the contracts | An import |
| --- | --- |
| A workflow is one contiguous phase | It pauses for hours or days while a replay runs: 20 CPU-hours for $s(60)$, 94 for $s(77)$, 126 for $s(59)$, by the sources’ own figures |
| A workflow has one kind of durable output | It has three: a source packet with a reported entry, which is W1’s stated exit; replay evidence with a review and derived rungs, which is W2’s; and reader documents, which is W8’s |
| One primary focus and one level of model | Retention is mechanical, the mathematics review takes the strongest model, and the two lanes of validation must share no context |
| “Workflow selection should reduce context, not create paperwork” | An eleventh workflow would add an enum value to three schemas, a row to two tables and a count to a check, and would still contain a survey, a review and a documentation step |

Three options were weighed.

- **An eleventh workflow.** Rejected by the four tests above.
- **Everything inside one W2 phase,** as sessions 152, 159 and 160 did.
  It hides the import behind the replay: the result is invisible until the replay ends,
  the branch holds its id for the whole time, and the rating at import is skipped.
- **A named sequence of existing phases.** Adopted.
  W1 imports the result as reported, W2 validates and rates it, the phase that changes
  the record publishes it, and the author is answered.
  It is tracked as one bead per import, the way a bounded commitment spans phases.

The sequence needed three clarifications in the workflow contracts, and no change to
what any workflow owns.

- **W1** names a reported result as an entry condition and its register entry as an
  exit. The contract already listed “a pinned source packet” and “stable claim IDs”.
- **W2** was “read-only by default”, yet it has always written the replay evidence and
  the rungs. The row now says it never edits the claim under review and writes only the
  confirmation it produces.
- **W8** was a reconciliation workflow “rather than an authoring one”, which left no
  owner for a review paper.
  It now owns one, under its existing boundary that nothing is stated which the record
  does not hold. Registering a result opens no W8 phase: the generated tables and the
  data pin are rendered in the same change.

## What This Change Codifies

The runbook restates nothing another document owns: the rungs, the credit policy and the
end points stay in `epistemics.md`, the record rules in the frontier README, the
workflow contracts in the synopsis, and the render and check commands in the W8 runbook.
It holds the sequence and the rules that had no home: the entry from an issue or a link,
one bead and two pull requests for each import, the claim map, the packet’s name and
README, which date is the publication date, when the `T-NNN` is taken, how a replay is
run and its receipts kept, what a review states, the exit commit, when a review paper is
written, and when the author is answered.

Outside the runbook, `epistemics.md` gains three rules for scoring significance, and
`.github/` gains a registration request form in the shape Daniel’s and wand125’s
requests already use.

## Decisions for the Owner

1. **What `V` is for a result whose source ships a machine certificate and its own
   passing run.** `epistemics.md` states the rule in force, `V0/C0` for a reported
   result, and the runbook defers to it.
   The recommendation is `V3/C0` where the packet retains the certificate, the command
   and the source’s run record, which is what the axis definition and the `V3` predicate
   say. It should follow `think-mt6e`, because the verified lane today admits any
   `verified` evidence whatever its origin.
   Up to six entries would move from `V0` to `V3` with `C` unchanged.
   `T-062`’s notes say the root records of its source’s runs are not in the retained
   packet, so it and its corollary `T-063` would stay at `V0` until they are.
2. **One register entry for each release of a rolling ladder.** The runbook follows the
   written granularity rule: a later release that raises values gets a new entry and the
   earlier one keeps its claim.
   The alternative is to amend the reported entry in place.
   Issues 281 and 282 are the first cases.
3. **Significance.** Whether the three scoring rules stand, whether the working rules
   buried in rationales become policy, and the rescoring pass over the 23 drafts
   (`think-qh3s`).
4. **When a review paper is written.** The runbook’s test is a confirmed result scored
   S5, or S4 with a proof that cannot be followed from its source, or the owner’s
   request. The mixed-cover exact values, once confirmed, are the likely next subject, as
   one paper over several results.
5. **Who posts replies.** Policy says the owner, or an agent at the owner’s request.
   The runbook has the agent draft each reply when the pull request merges.
   A standing permission for the three routine replies would remove the step at which
   five requests are now waiting.
6. **An acknowledgement within a day.** The first replies so far took 16 hours to 6.4
   days.
7. **Whether this project’s review of another author’s result counts toward rung 4.**
   `T-051`’s `next_rung` leaves it to the owner.
   The runbook has every stage 4 review listed in the entry’s `reviews`, which records
   it without deciding the question.

## Checks to Build and Records to Repair

Each is a bead under `think-z9wy`, labelled `result-import`.

| Bead | What |
| --- | --- |
| `think-g6d5` | `check_source_coverage` fails when a cited source has no coverage entry; the two missing entries |
| `think-3jsj` | One packet contract: a schema for the acquisition record and one acquirer |
| `think-rs0t` | An import ledger: a typed link from an entry to its issue, an answered date, and a generated view of every import and its stage |
| `think-mt6e` | The verified lane of a result by others requires a replay here and a mapped review |
| `think-506q` | An entry’s scope is held to its evidence’s scope; the register coverage gate reads upper bounds; the $n = 32$ entry for `T-045` |
| `think-j5so` | The AI-assistance statement is read from the bibliography and checked in `packing-validate` |
| `think-nr59` | Three truncated `significance.by` values; three entries whose claim and `activity` disagree |
| `think-qh3s` | The rescoring pass over the draft scores |

Beads that already track the stranded replays are `think-20mv`, `think-nnlg`,
`think-ifsv`, `think-wcex`, `think-0rrj` and `think-l6la`.

## Limits

- The audit read records and history.
  It ran no replay and judged no mathematics.
- Issue state was read on 2026-10-01 and changes.
- Whether the owner answered an author elsewhere is not recoverable from the repository.
- The detailed audit reports, with a citation for each finding, are working files of
  this session and are not retained.
  The findings a reader needs to check are restated above with the entry, issue or
  commit they concern.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
