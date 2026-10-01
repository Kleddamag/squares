# Epistemics

This document defines the four classifications attached to whole results in this
repository, the kind each result carries, and the policy for results by others: their
scope, credit and intake.
[`conventions.md`](conventions.md) owns field formats and identifiers;
[`packing/frontier/evidence.yaml`](packing/frontier/evidence.yaml) holds the evidence
entries; and the results register holds each classified claim in
[`results.yaml`](packing/frontier/results.yaml), with a generated reader view in
[`RESULTS.md`](packing/frontier/RESULTS.md).

The results checker validates structural support for a declared classification.
Human review remains responsible for deciding whether the cited evidence is relevant and
complete for the stated claim.

## The Four Classifications

| Axis | Question | Treatment |
| --- | --- | --- |
| Verification (`V`) | What level of verification does the result carry as certified by its own source: the producing run’s retained certificate, reviews and oversight for a result of this project, or the retained source packet and the literature for a result by others? | Structurally derived, except `V0` and `V2` |
| Confirmation (`C`) | To what level has that verification been independently confirmed, and by whom: replayed, rebuilt and reviewed here, or by a third party, beyond the run that produced it? | Structurally derived |
| Significance (`S`) | How important is the result? | Dated judgment; never gating |
| Novelty (`N`) | What does the retained source search support saying about novelty? | Declared and reviewed; not derived at result level |

Use `V4/C3` when describing a whole result.
The unqualified term `verified` remains the formal assurance label for an individual
evidence entry.

The two ladders carry the same rung meanings and differ in who earns each rung.
`V` is self-certification or historic certification: it asks what kind of verification
exists and how it was examined, and does not require this project to have replayed
anything.
`C` is confirmation: the same rungs, earned by a party other than the producing
run. For a result of this project that is a later replay from the repository, a second
implementation, another project’s replay or an external reviewer; for a result by others
it is this project, or another third party whose replay is retained here.
Every confirmation beyond a read is also verification evidence, so `C` never exceeds `V`
from `C2` up.

## No Blind Trust

No rung rests on blind trust in a formal system or in an agent.
Every rung from 4 up names the human who examined the work and states what they
examined, in a record retained in this repository and specific enough to audit.
A kernel check, a passing certificate replay and an AI review are evidence; a human
reading them is what turns evidence into a rung.
Rung 4 needs a human’s oversight of the mechanization and of the AI checking; rung 5
needs human experts’ review of the formalization itself.
[Review Records](#review-records) says what each record holds.

## Verification

The rungs are ordered by the kind of verification and how it was examined; they are not
cumulative. `V3` does not imply publication, and `V5` means that a proof assistant
checked a formalization *and* a human expert attested that the formal statement says
what the claim says.

| Rung | Meaning | Short | Structural support |
| --- | --- | --- | --- |
| `V0` | Claimed or recorded only | Claimed or recorded only | No higher predicate; the result explains the classification in `notes` |
| `V1` | Numerically checked | Numerically checked | A numerical method with recorded precision |
| `V2` | Proof asserted but not publicly recoverable | Proof asserted, not recoverable | Declared with `notes` explaining the unavailable proof |
| `V3` | Checkable: a published or audited proof, or a machine certificate that replays; review record not yet retained | Checkable; review record pending | `method: published-proof` or `proof-audited` with a `proof` block; or exact-algebraic, interval-certified or proof-assistant-checked evidence of any origin with a certificate, replay command and passing replay status |
| `V4` | Mechanized, adversarially reviewed and human-overseen | Mechanized, AI-reviewed, human-overseen | `V3` machine evidence, plus two retained adversarial AI reviews by distinct reviewers whose latest verdict accepts the claim, plus a retained human oversight record |
| `V5` | Formal, expert-reviewed | Formal, expert-reviewed | Proof-assistant-checked evidence with a certificate, passing replay and an axiom receipt, plus a retained formalization review by a human expert who is not the formalization’s author |

The `Short` column is the form the site’s rubric cards print where a row has two lines;
the `Meaning` is the chip’s title and the rubric’s own words.

The checker derives `V1` and `V3`–`V5` from the evidence cited by the result, of any
`origin`, and from the result’s retained `reviews`. `V0` and `V2` are declared because
the current evidence fields do not distinguish an ordinary unsupported claim from an
asserted but unavailable proof; both require an explanatory `notes` field.
The evidence schema separately enforces its own provenance, limitations, and
method-specific fields.

## Confirmation

Confirmation counts only work performed beyond the producing run: evidence recorded as
`audited-here`, `replayed-here` or `independently-external` (a third party’s own replay,
retained here), and reviews performed on the confirming side; `C1` describes a
qualifying read of external evidence.

| Rung | Meaning | Short | Structural support |
| --- | --- | --- | --- |
| `C0` | Recorded | Recorded | No qualifying read or confirming replay |
| `C1` | Read | Read | An `external_review` with a qualifying state, date, reviewer, and note |
| `C2` | Replayed without a machine certificate | Replayed, no machine certificate | Confirming-origin evidence with a replay command and `replay_status: passed` on a method that yields no certificate |
| `C3` | Machine-replayed here or by a third party; review record not yet retained | Machine-replayed; review record pending | Confirming-origin exact-algebraic, interval-certified or proof-assistant-checked evidence with a certificate, replay command and passing replay |
| `C4` | Mechanized confirmation, adversarially reviewed and human-overseen | Mechanized confirmation, AI-reviewed, overseen | `C3`, plus two retained adversarial AI reviews by distinct reviewers whose latest verdict accepts the claim, plus a retained human oversight record, all on the confirming side |
| `C5` | Formal confirmation: replayed here, open, and reviewed by two experts | Formal, replayed here, open, two experts | Proof-assistant-checked evidence with `origin: replayed-here`, a replay command from the repository at a pinned toolchain, passing status and an axiom receipt; an `open_review` pointer to the public sources and replay instructions, so that anyone can review and replay it; and two formalization reviews by distinct named human experts |

For `C1`, a qualifying review state is `informally-verified` or `defect-found`; the
review note records what was examined and what remains unchecked.
A `C3` or higher result must also name at least one existing control path.
The evidence schema requires a limitations statement on every evidence entry.

These predicates are deliberately literal.
A recorded execution performed here, with its receipt retained and hash-bound, is a
replay at `C3` and `C4` even when the final composer reconciles receipts rather than
rerunning geometry; a fresh end-to-end replay from the repository is what `C5`’s
“replayed here” requires.
Two independently written implementations using the same method, or two different
methods, do not change the rung: the count of distinct machine methods among the
confirming entries, and a third party’s retained replay, are attributes the register
shows beside the rung, not rungs.
A control path proves that a control is retained; the checker does not infer from its
filename that the control is adversarial.
The test suite, validation configuration, and review establish those stronger facts.

## Review Records

A result’s `reviews` list the retained review documents the rungs rest on, each mapped
in [`document-map.yaml`](docs/project/document-map.yaml) as a non-superseded `review`.
Each entry records the document’s `path`, its `kind`, the `reviewer` as the document
names itself, whether that reviewer is `ai` or `human`, the reviewer’s `relation` to
this project (`owner`, `project`, `external`, or `source` for a review the result’s own
source performed), the `date`, the `scope` in the reviewer’s words, and the `verdict`
(`accepted`, `defects-resolved`, `defect-open` or `refuted`). A record shared by a
family of results names every result it `covers`.

- **Adversarial AI review** (`kind: adversarial`, `reviewer_kind: ai`). Rung 4 on either
  axis needs at least two, by distinct reviewers: a different model family, or a
  separately prompted independent lane with no shared context.
  The reviewer names the model and its reasoning setting.
  The latest-dated review of the result must carry an accepting verdict, so that every
  defect found has a recorded disposition.
  A review with `relation: source` counts toward `V` and not toward `C`.
- **Human oversight** (`kind: oversight`, `reviewer_kind: human`). Rung 4 on either axis
  needs one. The record names the person and their relation, and its `checked` list
  includes `trust-boundary` (what the checker trusts and what it decides),
  `certificate-meaning` (that the accepted statement is the claim) and `ai-findings`
  (that every adversarial review’s defects were dispositioned).
  The owner of this project may serve.
  An approved pull request is not such a record unless the record cites it and says what
  was inspected.
- **Formalization review** (`kind: formalization`, `reviewer_kind: human`,
  `independent_of_author: true`). `V5` needs one and `C5` needs two, each by a named
  person who states their competence in the proof assistant and the mathematics and is
  not the formalization’s author; its `checked` list includes `statement-fidelity`,
  `definitions`, `axioms` and `build`.
- **Open review** (`open_review` on the result).
  `C5` needs the proof, its formalization and everything needed to replay it to be
  openly available, so that any other expert can review and replay it: the record points
  at the public `sources` at a pinned revision, the `terms` under which they may be
  inspected and run, the public `replay` instructions, and the copy `retained` here.
  No particular review venue is required.

The checker verifies the fields, the mapping, the counts, the distinctness and the
coverage. Whether a review was in fact adversarial, whether the models were the best
available, and whether the human read what the record says they read, are what the
record itself lets a reader judge.

## Scope and Composition

A classification attaches to the exact statement in a result’s `claim` field and its
declared scope.

- A compound claim takes the minimum rung of its load-bearing parts, on both axes.
- An equality whose upper half is a packing replayed exactly (`E-basic-grid-upper` or a
  witness replay) takes the `C` of its lower half; a construction is confirmed by its
  replay, and no second method is asked of it.
  The composition note says which half sets the rung.
- A derived claim takes the minimum rung of its inputs and the derivation itself.
- A construction’s feasibility, the sharpness of its parameter, and global optimality
  are separate claims.
- `C` never exceeds `V` from `C2` up: a replay, a rebuild or a review record is also
  verification evidence, so the checker refuses a confirmation rung above the
  verification rung. A read (`C1`) of a recorded claim (`V0`) is the one exception,
  reading being no kind of verification.

The checker derives the strongest rung present among the cited evidence entries and
reviews. When a compound or derived result declares a lower rung, its `composition` note
identifies the part that sets the minimum.
That note, the relevance of each evidence reference, and coverage of every load-bearing
premise are review obligations rather than machine inferences.

## What Changed on 2026-09-30

Ratings published between 2026-08-31 and 2026-09-30 used a ladder on which `V4` meant
machine-verified (a certificate with a passing replay), `C4` meant confirmed by two
distinct machine methods, `C5` meant review-ready (one mapped review document), and `V5`
meant a proof assistant had checked a formalization.
On 2026-09-30 the owner reserved rung 5 for formal verification with human experts’
review of the formalization, and required at rung 4 adversarial AI review and a human
oversight record, under the no-blind-trust principle above.
Every result that held `V4` moved to `V3`, and every result that held `C4` or `C5` moved
to `C3`, because no retained record of human oversight existed; each such result’s
`notes` says what it held and what restores the rung.
Dated prose in reviews, handoffs and the synopsis that names a rung describes the ladder
in force when it was written.
The proposal behind the change is
[the ladder review of 2026-09-30](docs/project/specs/active/plan-2026-09-30-epistemics-ladder-review.md).

## Significance and Novelty

Significance is recorded as a score, rationale, date, and scorer.
The score guides reading order and never changes validation behavior.

| Score | Anchor |
| --- | --- |
| `S1` | Bookkeeping or a routine consequence |
| `S2` | A citable detail that changes no theorem |
| `S3` | A substantive case result or machine audit |
| `S4` | A reusable technique, bound family, or resolved disputed value |
| `S5` | Movement on a central open case or broad external adoption |

The `scored` field dates the current assessment; Git retains earlier values.

Novelty uses four labels:

| Label | Meaning |
| --- | --- |
| `common-knowledge` | Standard fact not attributed to a particular source |
| `previously-published` | Present in an identified source |
| `apparently-novel` | Not found in the recorded search, subject to its stated gaps |
| `confirmed-novel` | Priority confirmed outside this repository |

Novelty is a scoped statement about a performed search, not a claim of priority.
An `apparently-novel` evidence entry records the corpus, search, narrow novel object,
and known gaps in `novelty_basis`. The result-level label is declared and reviewed; the
results checker validates its enum value but does not derive it from the cited entries.

## Result Kinds

Every result carries one `kind`, which says what the result is.
The four classifications above say how well a claim is supported and how much it
matters; the kind says what sort of claim it is.

| Kind | A result of this kind |
| --- | --- |
| lower bound | Proves $s(n) \ge v$ or $s(n) > v$: no packing of $n$ unit squares fits in a smaller square |
| upper bound | Proves $s(n) \le v$ by a verified packing of $n$ unit squares in a square of side $v$ |
| optimality | Settles an exact value $s(n) = v$: a lower bound that meets an upper bound |
| simplification | Proves again a result the record already holds, by a shorter, cleaner or more elementary route, and moves no bound |
| rigidity | Says whether one named packing can move at fixed side: its flexes, its rigidity at first or second order, the isolation of its pose |
| case exclusion | Shows that one named class of configurations, such as a branch, a corner class or a region of pose space, holds no packing at a stated side, and moves no bound by itself |
| restricted optimality | Finds the best packing within a declared family, such as fixed orientation classes near one pose, and says nothing about $s(n)$ outside it |
| method limit | Says how far one proof method or construction can reach: a ceiling on what a point set or a certificate format can certify |
| correction | Shows that a published statement is false as printed, and gives the corrected statement that holds |
| audit | Checks an existing proof or certificate independently and finds it correct as published |

The register stores a kind in lowercase with hyphens, `lower-bound` or `case-exclusion`.
A result has exactly one, chosen by three rules.

- The kind is what the claim concludes.
  Where a claim ends in a bound or a value of $s(n)$, the kind is that bound, however it
  was reached: by a repaired proof, an exact check of a published packing, or
  monotonicity from another result.
- A lower bound that meets a known upper bound is optimality, because the claim states
  the value.
- A second proof of a result the record already holds is a simplification, and its claim
  names the result it proves again.

The kind is declared, and the checker holds it to what the record already says.
A headline that opens with a relation on $s(n)$ states its kind: `≥` or `>` is a lower
bound, `≤` or `<` an upper bound and `=` optimality, and only a simplification may
restate one.
A bound cites evidence that claims that bound, and optimality cites an exact
value or both halves.
Rigidity, case exclusion and restricted optimality cite `derived-structure` evidence and
state no relation on $s(n)$ in their headline.
Method limit, correction and audit are told apart by review alone.

A result’s standing, whether a case bound rests on it now, is about bounds.
A result whose evidence claims no bound has no standing, and the register’s views show
its kind in that place.

## Results by Others

The register holds others’ results beside this project’s, under the same `T-NNN`
identifiers and the same derived rungs, because the work this repository does on them is
the same work: register the claim, replay its certificate, review its mathematics.
It holds every result of this project, and every result by others published on or after
22 August 2026, the day this project’s square-packing work began, that the record acts
on: its bound is or was a case’s reported or verified lower or upper bound, or it has
been or is queued to be replayed or reviewed here.
Older results enter only when they hold or held a verified field here or are machine
audits of the literature.
Rungs of a ladder that the same release supersedes, publication records never replayed,
and results below the standing bound that ask for no work stay in their case records and
packets.

Two things are tracked apart for such a result.
**Credit** belongs to the original result: the entry’s `attribution` names its source
keys and the date it was published, and the authors, the credit line and the lineage are
read from [`bibliography.yaml`](packing/resources/bibliography.yaml), never restated.
A source’s `lineage` says how it stands to this project, as the source itself says:
`builds-on-project`, `credits-project` (inspiration or second-hand credit, with its own
method), or `independent`. **Verification** is this register’s: `V` is the strongest
verification anywhere, and `C` what this repository has done.
A reported result enters at `V0/C0`, or `C1` once a review has read it, with a
`next_rung` naming the replay and review it waits on, and rises by the same derivation
as this project’s own results.
Whether an entry is current or superseded is derived from the case records and never
stored.

### Parallel Projects and Their Credit

Other people work on $s(n)$ alongside this project: some from its certificates, some
crediting it second-hand, and some independently.
The policy is to take in every result of theirs that the scope rule above reaches, and
to credit it as carefully as this project’s own.

- **The source says who did what.** Credit and lineage are read from the source’s own
  attribution files (README, CREDITS, NOTICE, ATTRIBUTION) at the pinned revision, never
  inferred here from whose method a result resembles.
  When a later release changes its attribution, the bibliography key for that release
  records the new wording.
- **Credit text has one home.** A source’s `credit` in
  [`bibliography.yaml`](packing/resources/bibliography.yaml) is written once: its
  authors, then `after` and the work the source says it builds on
  (`Daniel after Burns, Massaccesi`). The atlas citation line and the register renderers
  print it, and hand-written prose may add to it but never drops a link.
  A chain through an intermediate author names every link the source names: Kleddamag’s
  $4.66001$ builds on Squares Project (Joshua Levy), Mira and Guzhou0806. The atlas
  stage sets each line in 66 characters, so where the whole line does not fit it prints
  the source’s `short_credit`: the same authors and the first of the same links, ending
  in `et al.` (`Tokoharu after Levy, wand125 et al.`), a shape
  `devtools.build_bound_citations` enforces.
  The explainer’s figure, which prints the atlas’s own citation line, shows the same
  shortened form; every other renderer prints the full line.
- **Method credit travels with the result.** A result built with another author’s
  method, solver or checker credits them in the same line
  (`wand125 after Tokoharu, Levy, Stromquist, Nagamochi, Burns, Massaccesi`). This
  project is credited as `after Levy` only where the source itself says so.
- **People and projects, never tools.** Credit names people, or the handles they publish
  under. This project is `Squares Project (Levy)` where it holds a bound and `Levy`
  inside another source’s credit line.
  An AI agent is never a credited author.
  Where a source states that AI assisted its work, its case record or register entry
  says so in the source’s own terms, and so does any README prose about the result;
  `devtools.state_ai_assistance` names a case record that cites such a source without
  saying so.
- **Our rung is not their credit.** `V` and `C` describe verification.
  A result replayed here remains its authors’ result, and a rung never changes a credit
  line. A defect found here goes back to the authors with the review that found it.
- **Priority is stated, not defended.** When a parallel result predates or matches one
  of this project’s, the other result’s date is stated beside ours.
  Our entry keeps its dated source search and gains a dated annotation that it was
  reached independently.
  When a parallel result supersedes ours, the case records move to it, and the register
  derives the supersession from them.
- **Upper bounds count too.** A parallel packing that improves a best-known side enters
  its case’s reported upper lane from a retained source, with the same credit.
  It reaches the verified upper lane only after an exact or interval witness replay.
  The coverage gate below checks lower bounds only, so the register entry for an upper
  bound by others is kept by hand.

### Intake, Integration, and Reply

The procedure is
[Adding or Reviewing a Result](packing/frontier/README.md#adding-or-reviewing-a-result)
in the frontier README. Its three end points are fixed here.

1. **Taken in.** The source is retained at a pinned revision, with a coverage entry.
   Its bibliography key carries `dated`, `credit` and `lineage`. Its literal claim is in
   the reported lane, and its register entry is at the derived rung with a `next_rung`.
2. **Integrated.** A complete replay here and a review of the mathematics have
   discharged the certificate’s assumptions, and the verified lane carries the bound.
   The reader documents (README, synopsis, atlas) state it with its credit and its
   `T-NNN`.
3. **Answered.** An author who asked for the registration, on an issue here or
   otherwise, has been told what was registered, at which rung, what was replayed, and
   what remains. The answer goes on their issue, which stays open while work they asked
   for is still queued; the owner posts it, or an agent does at the owner’s request.

### Where the Frontier Is Recorded

Each fact about the frontier has one home, and reader-facing lists of results are
generated from these files (`OR-1`): `RESULTS.md`, `STATUS.md`, `INVENTORY.md`, and the
project site’s [overview](https://jlevy.github.io/squares/), whose recent results,
results table and survey are rendered from them by `devtools.render_overview`. A `T-NNN`
named in the README or the synopsis must be a registered result; the register gate
checks it.

| Record | Holds | Reader view |
| --- | --- | --- |
| [`n-NNN.md`](packing/frontier/README.md) case records | Both lanes’ bounds for each case, with their evidence | [`STATUS.md`](packing/frontier/STATUS.md); the site’s [recent results](https://jlevy.github.io/squares/#recent-results) and [survey](https://jlevy.github.io/squares/#the-survey); the standing column of `RESULTS.md` and the site’s [results table](https://jlevy.github.io/squares/all-results.html) |
| [`evidence.yaml`](packing/frontier/evidence.yaml) | Who performed each check, by which method, within which limits | [`INVENTORY.md`](packing/frontier/INVENTORY.md) |
| [`results.yaml`](packing/frontier/results.yaml) | Each result’s kind, headline, claim, date, `V`/`C`/`S`, novelty and attribution | [`RESULTS.md`](packing/frontier/RESULTS.md), grouped by lineage; the site’s [results table](https://jlevy.github.io/squares/all-results.html) |
| [`bibliography.yaml`](packing/resources/bibliography.yaml) | Each source’s date, credit and lineage | The atlas citation line; the holders, credit and relation in `RESULTS.md` and on the site’s [overview](https://jlevy.github.io/squares/#recent-results) |
| [`source-coverage.yaml`](packing/frontier/source-coverage.yaml) | Which sources were read, and when | None |

## Enforcement and Register

Run the executable contract from `packing/` with:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_results
```

The checker:

- resolves evidence references and artifact, control, and review-document paths;
- derives the structural `V` and `C` rungs described above, from the cited evidence and
  the retained `reviews`;
- refuses unsupported promotion, unexplained understatement, and a `C` above `V`;
- requires every review in `reviews` to be a non-superseded review in
  [`document-map.yaml`](docs/project/document-map.yaml) with the fields of
  [Review Records](#review-records), counts the adversarial reviews and their distinct
  reviewers, and requires the human oversight record at rung 4 and the human
  formalization reviews, the axiom receipt and the open-review pointer at rung 5;
- requires `attribution` on every `previously-published` result and refuses it on a
  novel one, resolves its source keys in the bibliography, and requires a `lineage` on
  the sources of a result by others published since 22 August 2026;
- requires a `kind` on every result, one of the [Result Kinds](#result-kinds), and
  cross-checks it against the relations the headline and the claim state, the claims of
  the cited evidence, and, for a simplification, the result its claim names;
- requires a `headline` of at most 100 characters on every result, stating no number its
  claim does not, and an `established` date on every result without `attribution`, the
  day its certificate or proof first passed here, which it refuses beside `attribution`
  and before 22 August 2026;
- fails when a case’s reported or verified lower bound cites evidence from a source
  dated on or after 22 August 2026 that no register entry covering that $n$ cites; and
- rejects unknown `T-NNN` references in the README and synopsis.

[`packing/frontier/results.yaml`](packing/frontier/results.yaml) states each result’s
kind, headline, claim, scope, classifications, evidence, artifacts, and `next_rung`. The
headline is the claim shortened for a table cell; the claim stays the statement the
rungs attach to. That final field records the next evidence-improving action or explains
why no independent rung change applies.
[`packing/frontier/RESULTS.md`](packing/frontier/RESULTS.md) is generated from the
register and sorted for readers.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
