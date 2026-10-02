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
| 5. Publish | The change that moves the record | The reader documents state the result: *integrated* |
| 6. Explain | W8, with a W2 review | A review paper, for the results that warrant one |
| 7. Answer | The owner | The reply on the issue: *answered* |

Stages 1 to 3 are the import, stage 4 is the correctness part, and stages 5 to 7 are the
publication.
It is a sequence of ordinary workflow phases, not a workflow of its own, and
each phase is declared as any other is.

Two rules shape every import:

- **One bead.** Each import has a bead labelled `result-import`, titled
  `Import <author>: <claim> (#<issue>)`, that holds the claim map and stays open until
  the author is answered.
- **Two pull requests.** Stages 1 to 3 merge on the day the result is first seen.
  Stage 4 merges when its replay and review are done, which can be days later.
  A reported result is then visible while it waits, and no branch holds an unmerged
  `T-NNN` for long. That is the separable boundary for which
  [`OR-9`](../../operating-rules.md#or-9-a-pull-request-leads-with-what-the-branch-cost)
  allows a second pull request.

## Stage 1: Triage

Triage decides what the import is before anything is retained, in an hour or less.

1. **Pin the source**, the author’s own publication and not a report of it, at a full
   commit id or a DOI with file checksums.
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
   It states no `T-NNN` and no rung, and the owner posts it within a day, as with every
   reply.

| Claim | Register action |
| --- | --- |
| A bound or an exact value the record does not hold | A new entry; each exact value has its own |
| Bounds of one kind at several counts in one release | One entry whose `scope` covers them |
| A later release that raises an earlier entry’s values or adds counts | A new entry; the earlier one keeps its claim, and the case records decide which is current |
| A theorem with an unbounded parameter | One entry stating the theorem, whose `scope` lists the cases this record holds |
| A second proof of a value the record holds | A new `simplification` entry |
| A consequence of another claim, such as monotonicity | Its own entry only when it settles a case; otherwise the parent’s `scope` covers it |
| A result that makes a registered one a corollary | Both stand; the older claim gains a sentence naming the newer route |
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
- **The bibliography key** carries the date of the pinned revision as `dated`, and is
  defined in the [resources README](../resources/README.md) as well.
  Credit is read from the source’s own files, now and not after the review.

## Stage 3: Record

Record the claim as reported, by the frontier README’s rules: a reported evidence entry,
a coverage entry that cites it, the reported lane of each case it improves, and a
register entry with its ratings and `next_rung`. Three rules are the process’s own:

- **`attribution.published` is the claim’s date, not the pin’s:** the date the source
  gives for it, or the UTC date of the first commit that contains the certificate.
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
entry `reviewed`, and listed in the register entry’s `reviews` under the kind it was run
as.

**The exit** follows both lanes.
It adds the replay evidence, moves the verified lane if the review has no blocking
defect open, rewrites the entry’s `claim`, `notes` and `next_rung` together and removes
its `activity`, so that no field says a replay is pending while another says it passed.
The reviewer also confirms or changes the draft significance score.
An open defect goes to the author with the review.

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
- The issue is closed with a final comment when nothing the author asked for is queued.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
