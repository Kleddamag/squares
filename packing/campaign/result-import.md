# The Result Import Process: Runbook

How a result that someone else publishes becomes a registered, validated and rated
result in this record, and how its author is told what was done.
[`epistemics.md`](../../epistemics.md#results-by-others) owns the policy: which results
enter, how they are credited, and what the `V`, `C` and `S` ratings mean.
[The frontier README](../frontier/README.md) owns the fields of each record.
This page is the sequence between them, and the one place that sequence is written down.

A result of this project follows
[Registering a First-Party Result](../frontier/README.md#registering-a-first-party-result)
instead. Its certificate is replayed from the repository before it is registered, so it
has nothing to import; stages 5 and 6 below apply to it unchanged.

## The Process at a Glance

An import has three parts.
**Import** brings the source and its claim into the record as reported.
**Correctness** replays the certificate, reviews the mathematics and derives the rungs.
**Publication** brings the reader documents up to date, sometimes writes a review paper,
and answers the author.

| Part | Stage | Workflow | What it leaves | State afterwards |
| --- | --- | --- | --- | --- |
| Import | 1. Triage | W1 `research-survey` | A claim map and a priced validation plan in the import’s bead; the author acknowledged | None yet |
|  | 2. Retain | W1 | The source at a pinned revision in a packet, a coverage entry, a bibliography key | None yet |
|  | 3. Record | W1 | The claim in the reported lane, typed evidence, a register entry with its ratings and `next_rung`, the views rendered, all merged | *imported*; status `recorded` |
| Correctness | 4. Validate | W2 `factual-review` | Replay evidence, a mapped mathematics review, the derived rungs, the verified lane | status `reviewed`, then `confirmed`, or `incomplete` |
| Publication | 5. Publish | The phase that changed the record | Reader documents that state the result with its credit and `T-NNN` | *integrated* |
|  | 6. Explain | W8 `documentation-pass`, with a W2 review of the exposition | A review paper under `papers/`, for the results that warrant one | Optional |
|  | 7. Answer | The owner, or an agent at the owner’s request | The reply on the author’s issue; the bead closed | *answered* |

The three end points, *imported*, *integrated* and *answered*, are defined in
[epistemics.md → Import, Integration, and Reply](../../epistemics.md#import-integration-and-reply).
The status words are derived by
[`devtools/result_status.py`](../devtools/result_status.py) and never stored.

Stages 1 to 3 land together as one pull request, on the day the result is first seen.
Stage 4 lands as a second one when its replay and review are done, which can be days
later: the source’s own exact sweep of the $s(59) = 8$ cover took about 126 CPU-hours.
The split is what keeps a reported result visible while it waits, and it shortens the
time a branch holds an unmerged `T-NNN`.

### Where It Sits Among the Workflows

The result import process is a standard sequence of phases of the existing workflows,
not an eleventh workflow.
A [workflow](../../SYNOPSIS.md#workflow-entry-contracts) is the contract for one
contiguous phase with one kind of durable output.
An import has three kinds of output, pauses between them while a replay runs, and puts a
different model and focus on each, so it is a unit of work that spans phases, as a bead
or a bounded commitment does.
[The process review of 2026-10-01](../../docs/project/reviews/review-2026-10-01-result-import-process.md)
gives the evidence: the session records behind past imports declare a different workflow
sequence almost every time, six import pull requests declared none, and the work was the
same five steps throughout.

A session that runs an import declares each phase as usual.
A routine import needs no session record: its bead carries the workflow, the bounded
objective, the intended artifact and the focused check for the phase in hand.
Open an [agent-session record](agent-sessions/README.md) only under the ordinary rule,
when the work coordinates independently tracked delegates or needs durable recovery
state. Three delegations are standard inside stage 4:

- **W7 `pipeline-improvement`** when no verifier here reads the certificate’s format and
  one is worth building for more than this result.
- **W5 `efficiency-loop`** when a complete replay misses its declared wall ceiling or
  its cost is unknown, as
  [the synopsis](../../SYNOPSIS.md#result-import-and-efficient-confirmation) says.
- **W10 `review-planning-oversight`** after the import, when the result changes what is
  worth working on. That block plans; it is not part of the import.

### One Import, One Bead

The unit is one request: one source release and the claims it makes, or the part of a
release that one issue asks about.
Requests that share a release share its packet and its bibliography key.
Each import has one bead, labelled `result-import`, titled
`Import <author>: <claim> (#<issue>)`, and open until the import is answered, or
integrated where no author asked.
Its description holds the claim map from stage 1 and the checklist at the end of this
page. A replay handed to another session gets a child bead that names the certificate,
the command, the wall ceiling and the branch its receipts are pushed to.

The register shows the same state to readers.
An entry’s derived status says how far the work has gone, and its `activity` says who
has the next move: `in-analysis` while a replay or review is under way here, `waiting`
on the `source` while a question is with the author.

## Stage 1: Triage

Triage starts when an author opens an issue, when a source this record already covers
publishes a new revision, when a catalogue capture prints a side the record does not
hold, or when the owner points at a result.
It takes an hour or less and decides what the import is before anything is retained.

1. **Pin the source.** Read it at its current head and fix the revision the import will
   use: a full commit id, or a DOI with file checksums.
   Where an issue names an older revision, say which was used and why.

2. **List every claim the release makes**, including those the request does not mention.
   Issue 227 asked about $n = 102$ and $103$; the source held 49 packings.

3. **Map each claim to the register** by the table below.
   The [scope rule](../../epistemics.md#results-by-others) decides whether it enters at
   all, and [Updates, Families and Corollaries](#updates-families-and-corollaries)
   covers the cases that are not a plain new entry.

4. **Check priority and overlap.** Say who else holds each value and when, from the
   record and from the other sources the release names.

5. **Price the validation.** For each certificate, name the checkers a complete replay
   needs, where each is pinned, the cost the source reports, and whether a verifier that
   does not share the source’s code exists here.
   A replay that needs a tool this repository lacks is a W7 slice to schedule, and the
   plan says so.

6. **Open the bead and acknowledge the author.** The acknowledgement goes on the issue
   within a day. It says the request was received, which revision was pinned, and what
   will be checked. It states no `T-NNN` and no rung.

Triage exits with the claim map and the validation plan in the bead.

| Claim | Register action |
| --- | --- |
| A bound or value the record does not hold | A new entry |
| The same kind of certificate at further counts, in the same release | One entry whose `scope` covers them |
| A later release that raises values an earlier entry reports | A new entry; the earlier one is left as it stands |
| A second proof of a value the record holds | A new `simplification` entry that names the result it proves again |
| A consequence of another claim, such as monotonicity | Its own entry only when it settles a case; otherwise a sentence in the parent’s claim |
| New evidence about an entry already registered | No new entry: an evidence update |
| A request for a result already registered from another route | No new entry: link the issue and go to the stage the entry is at |
| Below the standing bound and asking for no work | None; it stays in the packet and the case record |

## Stage 2: Retain

1. **Retain the source in a packet** under
   [`../resources/web/`](../resources/README.md), named
   `<author>-<repository or subject>-<date of the pinned revision>`. A later revision of
   the same source is a new packet; the earlier one is not edited.
   The packet’s `README.md` records:

   - the source’s address, the pinned revision, the date of that revision and the time
     it was retrieved;
   - the licence, and where there is none, that only derived facts are kept;
   - which attribution files were read, what they say about credit, and the source’s
     statement on AI assistance or its absence;
   - what is retained and what is not, with the reason and the upstream location of
     anything left out;
   - a manifest of the retained files with their digests, and the Compressed Files table
     the [resources README](../resources/README.md) requires for large data;
   - the issue that asked for the registration, and a retained copy of any comment by
     the author that the record relies on, such as a credit or an AI statement.

   Retain every repository the certificate needs.
   A certificate checked by another author’s verifier at its own revision needs both
   pins, and the packet names the second where it does not hold it.

2. **Add the coverage entry** to
   [`source-coverage.yaml`](../frontier/source-coverage.yaml), with the pinned address,
   the `source_date` of the pinned revision and the `reviewed` date it was read here.

3. **Give the source a bibliography key** in
   [`bibliography.yaml`](../resources/bibliography.yaml) with `dated`, `credit`,
   `lineage` and a `note` naming the file the credit was read from.
   `dated` is the date of the pinned revision.
   Credit follows
   [Parallel Projects and Their Credit](../../epistemics.md#parallel-projects-and-their-credit):
   every link the source names, and nothing inferred here.
   Where the source states that AI assisted its work, add the key to
   `devtools.state_ai_assistance` so the case records are held to the statement.

## Stage 3: Record

1. **Write one evidence entry per claim** in
   [`evidence.yaml`](../frontier/evidence.yaml) for what the source reports:
   `assurance: reported`, `reported_method`, `performed_by: source-author`,
   `origin: external`, `replay_status: not-attempted`, the `certificate` path in the
   packet, the `source_key`, and `limitations` that give the full pinned commit and say
   what the source ran and what it did not.

2. **Put the literal claim in the reported lane** of each case record it improves, and
   name the entry’s `T-NNN` there.
   Where the verified lane now trails the reported one, the record carries a blocker
   that cites the reported evidence.
   Preserve a disagreement with the source as a conflict or a typed blocker; do not edit
   the claim to match a checker.
   Where the source gives a packing, adapt its geometry once to
   [`Witness/v2`](../witnesses/witness.schema.yaml).

3. **Write the register entry** with the fields
   [results.schema.yaml](../frontier/results.schema.yaml) requires, at the rungs the
   cited evidence derives.
   [Rating an Imported Result](#rating-an-imported-result) says how each rating is set.
   The `claim` is short paragraphs: the statement, the certificate, how the source
   checked it, what was done here, and the credit with a link to the source.
   `attribution.published` is the day the claim first appeared in its source, which can
   be earlier than the pinned revision; `next_rung` names the replay, the review and the
   bead they are tracked under.
   Every count in `scope` is covered by the scope of a cited evidence entry.

4. **Take the `T-NNN` last and merge the same day.** An id is its row’s position, so it
   cannot be reserved across branches: three ids collided between 21 and 30 September.
   Take the next id in the commit that registers the result, check open pull requests
   first, and renumber before merging if `main` moved.
   State no `T-NNN` outside the repository until it is on `main`.

5. **Render and check**, from `packing/`, then run
   [New Result Publication](documentation-pass.md#new-result-publication) for the
   generated tables and the data pin:

   ```shell
   uv run --frozen python -m devtools.validate_schemas
   uv run --frozen python -m devtools.check_source_coverage
   uv run --frozen python -m devtools.check_results
   uv run --frozen --all-extras --group dev packing-validate --records
   ```

The result is *imported* when this is on `main`: its status reads `recorded`.

## Stage 4: Validate

Stage 4 is one W2 phase under a correctness focus, run as two lanes that share no
context: a replay and a review of the mathematics.
[The synopsis](../../SYNOPSIS.md#result-import-and-efficient-confirmation) owns how W2
chooses the smallest sufficient check and measures its cost.

### The Replay

1. **Check the retained bytes against the pin** before running anything.
2. **Run the source’s own verification on the retained bytes, in full.** The source’s
   fast tier, a sample of roots or a green test suite is a diagnostic and not a replay.
   Compare the outcome with the census the source reports, root for root where it ships
   one.
3. **Decide the certificate a second way where one exists here**: a verifier of this
   repository’s that reads the format, or a second checker of the source’s that shares
   no code with the first.
   Two implementations of one method are one method; the entry’s `composition` says what
   the checkers share, as the source’s own account of its common mode does.
4. **Retain negative controls.** At least two mutated certificates, such as a mass
   lowered below the count or a point moved off its orbit, are refused by every checker
   that accepted the original, and a test holds them.
5. **Commit the receipts when the run ends.** The command, the outcome, the counts and
   the wall and CPU time go into the packet’s `receipts/`, on a pushed branch that the
   bead names, before anything else is done with them.
   A replay that passed in a session’s scratch space and was never committed did not
   happen: about 45 CPU-hours of the $s(21)$ and $s(45)$ re-sweeps were lost that way.
6. **Write one evidence entry per decision**, with `origin: replayed-here` or
   `audited-here`, the `method`, the `certificate`, a `replay` command that runs from
   `packing/`, `replay_status: passed`, the `relationship_to_generator`, and
   `limitations` that name what the run trusted.

### The Mathematics Review

The review is a document under `docs/project/reviews/`, named
`review-YYYY-MM-DD-<author>-<subject>.md` and mapped in
[`document-map.yaml`](../../docs/project/document-map.yaml).
Its reviewer is the strongest model available, named with its reasoning setting, and has
not seen the replay lane’s conclusions.
It states:

- the claim, and each `T-NNN` it covers;
- the argument from the certificate to the claim, re-derived, with every hypothesis the
  certificate’s checker assumes and does not decide;
- the trust boundary of each checker: what it reads, what it decides, what it takes on
  trust, and what any two of them share;
- each defect found, marked blocking or not, and what was told to the author;
- the disposition: accepted, defects resolved, defect open, or refuted.

Record the read as `external_review` on the reported evidence entry, with its state,
date, reviewer and a note of what was examined and what was not.
That is what raises `C0` to `C1`. Then list the document in the register entry’s
`reviews`, with its kind, reviewer, date, scope and verdict, as `T-060` does.

### The Exit

Stage 4 changes the record in one commit, after both lanes have reported:

1. The register entry cites the new evidence, declares the rungs `check_results`
   derives, and names its `controls`.
2. The verified lane takes the bound only when a complete replay here has passed and the
   review has no blocking defect open.
3. The entry’s `claim`, `notes`, `next_rung` and `activity` are rewritten together, so
   that none says a replay is pending while another says it passed.
4. Stage 3’s render and checks are run again.

The status then reads `confirmed`. It reads `incomplete` while a defect is open, and the
review goes to the author with the reply.
An import normally rests at `V3/C3`. Rung 4 needs two adversarial reviews by distinct
reviewers and a human oversight record
([Review Records](../../epistemics.md#review-records)), and the owner chooses which
results are taken there.

## Rating an Imported Result

`V` and `C` are derived and never chosen: the entry declares what
[`check_results`](../devtools/check_results.py) derives from the evidence it cites, by
the predicates of [epistemics.md](../../epistemics.md#verification).
Significance, novelty and kind are declared and reviewed.

| Rating | At stage 3 | At stage 4 |
| --- | --- | --- |
| `V` | `V0`, with `notes` saying what the source ran and why nothing higher is derived | The rung the replay and review evidence derive, `V3` for a machine certificate that replays |
| `C` | `C0`; `C1` once a read is recorded as `external_review` | `C3` for a machine replay here with a named control; `C2` where the method yields no certificate |
| `S` | Scored on the claim, marked a draft in `by` | Confirmed or changed by the review lane, which `by` then names |
| Novelty | `previously-published`, with `attribution` | Unchanged |
| Kind | What the claim concludes, by the three rules of [Result Kinds](../../epistemics.md#result-kinds) | Unchanged |

A compound claim takes the minimum rung of its parts, and its `composition` says which
part sets it.
An exact value by others is the usual case: the grid replays the upper half
at `V3/C3`, and the reported lower half holds the entry at `V0`.

Significance follows the three scoring rules of
[epistemics.md](../../epistemics.md#significance-and-novelty): the score is of the
claim, the stage 3 score is a draft that the stage 4 reviewer confirms against the
entries nearest to it, and a later result that supersedes the entry does not lower it.
Quote a `by` or a rationale that contains ` #`, which YAML otherwise reads as the start
of a comment.

## Updates, Families and Corollaries

- **A later release that raises a reported ladder** gets a new entry for the counts it
  changes, under its own bibliography key.
  The earlier entry keeps its claim, and the case records decide which is current.
  A replay already run on an earlier certificate still proves that certificate’s bound.
  It enters the verified lane where it beats the standing verified value, and the plan
  says which replays in flight are still worth finishing.
- **A family that grows** by further counts in a later release is a new entry too.
  One entry covers several counts only within one release.
- **A family with an unbounded parameter** is registered as the theorem its source
  states, with a `scope` that lists the cases this record holds.
  The claim says that the scope is a projection.
- **A result that makes another a corollary** supersedes nothing when both state the
  same value. Both entries stand, and the older one’s claim gains a sentence naming the
  newer route.
- **A certificate built from another author’s certificate** is checked as its own
  object. Its rung does not wait on the certificate it grew from; its credit names that
  author.
- **An author’s answer that changes what is known**, such as a new run or a correction
  to how independent two checkers are, is a new revision of the source: a new packet, a
  reported evidence entry, and an update to the `composition` and `limitations` it bears
  on. It needs no new register entry.
- **A rolling request**, where the author says more will follow, is one import for each
  release. The issue stays open and each import is answered on it.

## Stage 5: Publish

Each change to the record publishes itself: the commit that registers or raises a result
also runs [New Result Publication](documentation-pass.md#new-result-publication), which
renders the register, the tables and the atlas data and re-pins the data revision.
No separate documentation phase is opened for that.
Open a W8 pass only when hand-written prose in the README, the synopsis or the tutorial
needs reconciling beyond the generated tables.

The result is *integrated* when the verified lane carries it and the reader documents
state it with its credit and its `T-NNN`.

## Stage 6: Explain

Some results deserve more than a register entry: a paper that explains the proof and
this project’s review of it to a reader outside the project.
[A Review of the Optimality Proof of the Trump Packing of 11 Squares](https://jlevy.github.io/squares/papers/n11-optimality-review.html)
is the model. Write one when the result is confirmed and one of these holds:

- it is scored `S5`;
- it is scored `S4` and its proof cannot be followed from the source alone, as with a
  computer-assisted proof that composes several certificate families;
- the owner asks for one.

The paper states no claim the register does not hold, so writing it is a W8 phase.
It contains:

- the result, and credits that lead with the original proof and its author;
- the provenance of each component, with the source pinned;
- the argument from start to finish, at the level a mathematician outside the project
  can check;
- what was verified here, by which checks, and what that verification does and does not
  establish;
- the limits, and the sources and verification record.

Its exposition gets its own W2 review, retained under `docs/project/reviews/`, which
checks every statement against the accepted evidence and changes none of it.
The paper is named by a slug, `n<NN>-<subject>-review`, and is published at
`papers/<slug>` with its Markdown and PDF, as
[conventions.md → Naming](../../conventions.md#2-naming) and
[the development guide](../../development.md) describe.
A renderer for a new paper is a W7 slice.
The paper is an explanation: it is neither a replay nor the human oversight record that
rung 4 requires.

## Stage 7: Answer

The owner posts the reply, or an agent does at the owner’s request.
The agent’s part is to have the reply drafted in the bead when the pull request merges.

- **Reply after the merge, from `main`.** Every link points at `main` or at a commit on
  it. A link into a working branch dies with the branch, and a `T-NNN` quoted from one
  can change: issue 247 was told `T-058` for the result that is `T-061`.
- **Say what the author needs**: what was registered and as which `T-NNN`; its status
  and rungs, with one line on what they mean; what was replayed, by which commands and
  with what counts; what the review found; what remains and who has the next move; and
  any question for the author.
- **Reply once for each end point.** One reply when the result is imported, and one when
  it is confirmed or a defect is found.
- **Correct a reply the record has left behind.** Post a follow-up when an id changes, a
  rung changes, queued work lands or is dropped, or a later result supersedes the one
  the reply described.
- **Keep the issue open while work the author asked for is queued**, and say what it is
  waiting on. Close it with a final comment when nothing is.

The import is *answered* when the reply that matches the entry’s present state is on the
issue. Close the bead with a link to that comment.

## What Holds Each Step

A check holds a step when something refuses the record without it.
The rest are obligations of the stage 4 review and of the pull request’s reviewer.

| Step | Held by |
| --- | --- |
| A packet exists, is pinned, and has the contents of stage 2 | Review. `check_results` requires only that a packet file named in `artifacts` exists |
| A coverage entry exists for each source | Review. `check_source_coverage` checks the entries that exist |
| Bibliography `dated` and `lineage` | `build_bound_citations`, `check_results` |
| Bibliography `credit` matches the source’s files | Review; a test holds `credit` to `lineage` |
| The source’s AI statement is in the case records | `state_ai_assistance`, for the keys listed in it |
| The claim is in the reported lane | Review |
| A recent lower bound a case holds has a register entry | `check_results` |
| An upper bound by others has a register entry | Review |
| The entry’s fields, kind, headline and rungs | `validate_schemas`, `check_results` |
| The evidence covers every count in the entry’s scope | Review |
| No commit id, digest or disclaimer in a claim | `check_prose_ceremony` |
| The replay passed on the retained bytes | Review. The checker reads the recorded status and runs nothing |
| The verified lane waits for a replay here and a review | Review |
| A review document is mapped | `check_documentation`, and `check_results` for a path in `reviews` |
| A disagreement on a lower bound is kept as a conflict | Review. The check covers upper bounds only |
| `activity` is present while work is under way, and is no older than 30 days | Review for presence; `check_results` for age |
| Generated views match the records | `packing-validate --records` |
| The author is answered | The import’s bead |

## Checklist

Copy this into the import’s bead and tick each line with the commit or the comment that
did it.

```text
Triage
[ ] source pinned at a full revision; every claim listed and mapped to the register
[ ] priority and overlap stated; validation priced; bead opened; author acknowledged
Retain
[ ] packet with README, manifest, licence, attribution and AI statement
[ ] coverage entry; bibliography key with dated, credit, lineage and note
Record
[ ] reported evidence entry for each claim; reported lane and T-NNN in each case record
[ ] register entry: kind, headline, claim, scope, V0/C0 with notes, draft S, attribution,
    next_rung with its bead
[ ] views rendered; validate_schemas, check_source_coverage, check_results and
    packing-validate --records pass; merged to main; status reads recorded
Validate
[ ] bytes checked against the pin; the source's full verification run on them
[ ] second route run, or recorded as absent; two negative controls refused and tested
[ ] receipts committed and pushed; one evidence entry for each decision
[ ] review document mapped, recorded as external_review and in reviews
[ ] rungs as derived; controls named; S confirmed; claim, notes, next_rung and activity
    agree; verified lane moved, or the blocking defect recorded
Publish
[ ] New Result Publication run; reader documents state the result, its credit and T-NNN
Explain
[ ] review paper written and its exposition reviewed, or not warranted and why
Answer
[ ] reply drafted from main; posted; follow-up posted after any later change
[ ] issue closed, or left open with what it waits on; bead closed with the comment link
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
