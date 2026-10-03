# The Result Import Process: Runbook

An import starts from one thing: a GitHub issue, or a link to a result someone else has
published.
Everything below follows from that input, and ends with the result registered,
validated and rated in this record and its author answered.

This page holds the sequence, and the few rules that belong to no single record.
The rest has an owner, and is not repeated here:

- [`epistemics.md`](../../epistemics.md#results-by-others) owns which results enter, how
  they are credited, the `V`, `C` and `S` ratings, and the three end points.
- [The frontier README](../frontier/README.md#adding-or-reviewing-a-result) owns the
  rules and fields of the records.
- [The synopsis](../../SYNOPSIS.md#result-import-and-efficient-confirmation) owns the
  workflow contracts, and how a W2 phase chooses and prices a check.
- [New Result Publication](documentation-pass.md#new-result-publication) owns the
  commands that render and check a changed record.

## The Sequence

| Stage | Workflow | Exit |
| --- | --- | --- |
| 1. Triage | W1 | A claim map and a priced validation plan in the import’s bead; the author acknowledged |
| 2. Retain | W1 | The source in a packet at a pinned revision, with its bibliography key |
| 3. Record | W1 | The claim registered as reported, with its coverage entry, and merged: *imported* |
| 4. Validate | W2 | Replay evidence, a mapped review and the rungs they derive: status `confirmed`, or `incomplete` |
| 5. Publish | The change that moves the record | The reader documents state the result; once stage 4 has passed, *integrated* |
| 6. Explain | W8, with a W2 review | A review paper, for the results that warrant one |
| 7. Answer | The owner | The reply on the issue: *answered* |

Stages 1 to 3 are the import, stage 4 is the correctness part, and stages 5 to 7 are the
publication.
It is a sequence of ordinary workflow phases, not a workflow of its own, and
each phase is declared as any other is.

Two rules shape every import:

- **One bead.** Each import has a bead labelled `result-import`, titled
  `Import <author>: <claim> (#<issue>)`, that holds the claim map and stays open until
  the author is answered, or until the result is integrated where no author asked.
- **Two pull requests.** Stages 1 to 3 merge on the day the result is first seen.
  Stage 4 merges when its replay and review are done, which can be days later.
  A reported result is then visible while it waits, and no branch holds an unmerged
  `T-NNN` for long. That is the separable boundary for which
  [`OR-9`](../../operating-rules.md#or-9-a-pull-request-leads-with-what-the-branch-cost)
  allows a second pull request.

## Stage 1: Triage

Triage decides what the import is before anything is retained, in an hour or less.

1. **Pin the source**, the author’s own publication and not a report of it, at a full
   commit id or a DOI with file checksums: its current head, unless the claim depends on
   an older revision.
2. **List every claim the release makes**, including those the request does not mention.
   Issue 227 asked about $n = 102$ and $103$; the source held 49 packings.
   A claim in scope that the request does not mention becomes an import of its own.
3. **Map each claim to the register** by the table below, and say who else holds each
   value.
4. **Price the validation:** the checkers a complete replay needs, the cost the source
   reports, and whether anything here decides the certificate without the source’s code.
   A missing tool is a W7 slice, and the plan says so.
5. **Open the bead and draft the acknowledgement:** what was received, the revision
   pinned, and what will be checked.
   It states no `T-NNN` and no rung, and the owner, or an agent at the owner’s request,
   posts it within a day.

| Claim | Register action |
| --- | --- |
| A bound or an exact value the record does not hold | A new entry; each exact value has its own |
| Bounds of one kind at several counts in one release | One entry whose `scope` covers them |
| A later release that raises an earlier entry’s values or adds counts | A new entry; the earlier one keeps its claim, and the case records decide which is current |
| A theorem with an unbounded parameter | One entry stating the theorem, whose `scope` lists the cases this record holds |
| A second certificate for a value the record holds | A new `simplification` entry |
| A consequence of another claim, such as monotonicity, at a count where the record holds no such value | Its own entry only when it settles a case; otherwise the parent’s `scope` covers it |
| A consequence that another entry already registers | No new entry and no change of scope: both stand, and the older claim gains a sentence naming the newer route |
| New evidence or an author’s answer about a registered entry | No new entry: the source retained at the revision that holds it, and an evidence update |
| A request for a result already registered | No new entry: link the issue and continue from the entry’s stage |
| Below the standing bound and asking for no work | None; it stays in the packet |

## Stage 2: Retain

- **The packet** holds one subject of one source at one pinned revision.
  It goes under [`../resources/web/`](../resources/README.md), named
  `<author>-<subject>-<date of the pinned revision>`. Its README records the address,
  the pin and its date, the retrieval time, the licence, what the source’s attribution
  files say about credit and AI assistance, what is retained and what is not, a manifest
  with digests, and the issue.
  It retains every repository the certificate needs, such as a checker pinned in another
  author’s repository.
  A later revision is a new packet; files added later from the same revision join the
  packet they belong to.
  [`devtools.acquire_source`](../devtools/acquire_source.py) writes a packet from a
  declaration kept in its `acquisition/` directory, and its `--check` re-derives the
  packet from its manifest.
- **The bibliography key** carries the date of the pinned revision as `dated`, and is
  defined in the [resources README](../resources/README.md) as well.
  Credit is read from the source’s own files, now and not after the review.

## Stage 3: Record

Record the claim as reported, by the frontier README’s rules: a reported evidence entry,
a coverage entry that cites it, the reported lane of each case it improves, and a
register entry with its ratings and `next_rung`. Three rules are the process’s own:

- **`attribution.published` is the claim’s date, not the pin’s:** the date the source
  gives for it, or the UTC date of the first commit that contains the certificate; for
  an entry over several certificates, the last of those dates.
- **The entry’s `scope` is covered** by the scopes of the evidence it cites.
- **The `T-NNN` is taken last.** An id is its row’s position and cannot be reserved
  across branches, so take it in the commit that registers the result, merge that day,
  and quote it to no author until it is on `main`.

The record checks pass without a packet, a coverage entry or evidence over the whole
scope. The reviewer of the pull request looks for those.

## Stage 4: Validate

Stage 4 is one W2 phase with two lanes that share no context: a replay of the
certificate and a review of its mathematics.

**The replay** runs the source’s own verification on the retained bytes, in full.
A fast tier or a sample of roots is a diagnostic.
One complete replay is what `C3` needs; a second route is recorded beside the rung and
is not a condition of it.

- It runs the retained copy of each checker, which is read before it is run.
  A script that fetches one over the network is run with the fetch replaced, and the
  receipt says so.
- Its evidence entry names every program the replay runs in `verifiers`, deciders and
  premise checks alike, and registers a new one in
  [`verifiers.yaml`](../frontier/verifiers.yaml) with the digest that ran and the
  retained path of its source.
  `relationship_to_generator` is read from the deciding programs: `same-implementation`
  for the source’s own checker, `shared-components` with the reused parts listed,
  `independent-implementation` with the record of what its authors read
  ([epistemics.md](../../epistemics.md#which-code-confirmed-it)).
  `devtools.backfill_verifier_relation --dry-run` shows what it would write and which
  values look wrong.
- Where the source’s script cannot pass as published, the evidence entry’s `limitations`
  say so, the author is told, and the same checks are run as this repository’s own
  sequence.
- A replay that fails is recorded with `replay_status: failed`, which makes the entry
  `incomplete`.
- Two mutated certificates are refused by every checker that accepted the original, and
  a test holds them.
- The receipts are committed and pushed when the run ends, on a branch the bead names.
  A replay that passed in scratch space and was never committed did not happen.

**The review** is a mapped document under `docs/project/reviews/`, a
[review record](../../epistemics.md#review-records) like any other.
It states the claim and each `T-NNN` it covers; re-derives the argument from the
certificate to the claim, with every hypothesis the checker assumes; gives each
checker’s trust boundary and what any two share; and marks each defect blocking or not.
It is recorded as `external_review` on the reported evidence entry, which makes the
entry `reviewed`, or `incomplete` when the read found a defect, and listed in the
register entry’s `reviews` under the kind it was run as.

**The exit** follows both lanes.
It adds the replay evidence, moves the verified lane if the review has no blocking
defect open, rewrites the entry’s `claim`, `notes` and `next_rung` together and removes
its `activity`, so that no field says a replay is pending while another says it passed.
The reviewer also confirms or changes the draft significance score.
An open defect goes to the author with the review.

The reviewer of the pull request checks one thing in every sentence the stage writes:
where the claim, the case record, the review or the reply says the result is
*confirmed*, it says which confirmation, reproduced with the producer’s code,
re-implemented sharing named components, or independently re-implemented.
The checker holds the register’s `claim`, `composition` and `next_rung` to it; the case
record, the review and the reply are held to it here.

## Stage 5: Publish

The pull request that registers or raises a result runs
[New Result Publication](documentation-pass.md#new-result-publication): the views are
rendered in the commit that changes the record, and the data pin moves in the next.
No documentation phase is opened for it.

## Stage 6: Explain

Some results warrant a paper that explains the proof and this project’s review of it to
a reader outside the project.
[The review of the eleven-square optimality proof](https://jlevy.github.io/squares/papers/n11-optimality-review.html)
is the model. Write one when a result is confirmed and is scored `S5`, or is scored `S4`
with a proof that cannot be followed from its source alone, or when the owner asks.

The paper leads its credits with the original proof and its author.
It gives the argument from start to finish, what was verified here and what that
verification does and does not establish.
It states nothing the register does not hold, and its exposition gets its own W2 review.
It is neither a replay nor the human oversight record that rung 4 requires.
[conventions.md → Naming](../../conventions.md#2-naming) owns its slug, and
[the development guide](../../development.md) how it is built and served.

## Stage 7: Answer

[epistemics.md](../../epistemics.md#import-integration-and-reply) says what an answer
contains and who posts it.
The process adds when and how:

- An agent drafts the reply in the bead when the pull request merges.
- A reply is written after the merge and links only to `main`. A link into a working
  branch dies with the branch, and a `T-NNN` quoted from one can change.
- There is one reply when the result is imported and one when it is confirmed or a
  defect is found, and a follow-up whenever the record moves past what a reply said.
  The reply that reports a confirmation names the programs that ran, and says whether
  they were the author’s own code re-run or a re-implementation.
- The issue is closed with a final comment when nothing the author asked for is queued.

### The Requests Record

[`result-requests.yaml`](result-requests.yaml) has one entry for each issue that reports
a result, a defect or a correction.
It records what the issue reports, and for each reported result the register and
evidence ids it maps to, or why it is not registered and whether it is queued.
It also names the beads that track the issue, the bead that answers it, every reply
posted with the state that reply reported, and when the issue can close.
It records no current rung.
[`devtools.check_requests`](../devtools/check_requests.py) derives each result’s state
from the register:

- *confirmed*, when every register entry it maps to is at `V3` and `C3` or above;
- *refuted* or *defect recorded*, from the entries’ reviews and evidence;
- *open* while validation runs, and *queued* while it waits for import.

A **reply is due** when the issue has had no reply, when an entry has been registered,
renumbered or moved a rung since the last reply that spoke of it, or when a reply’s
statement is marked `outdated` and no later reply `corrects` it.
An issue is **closeable** when triage is done, every result is confirmed or refuted (a
reported defect: recorded against the entry it names), and no `ask` is queued.

A confirmation is described from the confirming evidence’s `relationship_to_generator`:
*reproduced with the author’s own checker* for `same-implementation`, *re-verified by an
independent implementation* for `independent-implementation`. The programs are the
entry’s `verifiers`, named from `frontier/verifiers.yaml`; without them no program is
named, and without a usable relation the report and the draft say it is not yet
recorded. An exact value is described by its lower half alone, as its confirmation is.

Run each command from `packing/` as
`uv run --frozen --all-extras --group dev python -m devtools.check_requests`, with:

| Option | What it does |
| --- | --- |
| none | The gate step: the schema holds and every id resolves; one line per issue |
| `--report` | A table per issue: each result’s entries, rungs, state, how it was confirmed and whether its id is on `main`; the replies due; whether it is closeable |
| `--backlog` | Every register entry below `V3` or `C3`, with its `next_rung`, its `activity`, the beads it names and the issues it serves |
| `--draft N` | The status comment for issue N, ending in the Claude Code footer; it refuses unless `HEAD` is on `origin/main` |
| `--github` | Read-only: the issues the record lacks, the replies missing from it and the comments after an entry’s `read_through` |

A reply due is reported and never fails the gate: it is the owner’s next move, not a
broken record.

### After the Merge

1. On `main`, run `--github` and take into the record any issue, reply or comment it
   lacks. A new issue enters with `triage: pending`, and stage 1 maps its results.
2. For each issue that `--report` marks reply due, render `--draft N`. The owner posts
   it, or an agent does at the owner’s request.
3. Record the reply under the issue’s `replies`: its URL, date and kind, and in
   `reported` the id, rungs and status it stated for each result.
   Name in `corrects` any earlier reply whose `outdated` statements it corrects.
4. When `--report` says an issue is closeable, close it with the final comment and set
   the entry’s `state` and `closed`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
