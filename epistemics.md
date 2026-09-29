# Epistemics

This document defines the four classifications attached to whole results in this
repository, and the policy for results by others: their scope, credit and intake.
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
| Verification (`V`) | What is the highest verification rung supported by the cited evidence, regardless of who performed it? | Structurally derived, except `V0` and `V2` |
| Confirmation (`C`) | What has this repository recorded, replayed, or established itself? | Structurally derived |
| Significance (`S`) | How important is the result? | Dated judgment; never gating |
| Novelty (`N`) | What does the retained source search support saying about novelty? | Declared and reviewed; not derived at result level |

Use `V4/C3` when describing a whole result.
The unqualified term `verified` remains the formal assurance label for an individual
evidence entry.

## Verification

Verification uses a project-prioritized ordering of evidence types.
The rungs are not cumulative: `V4` does not imply publication, and `V5` means that a
proof assistant has checked a formalization, not that the formal statement matches every
intended prose claim.

| Rung | Meaning | Structural support |
| --- | --- | --- |
| `V0` | Claimed or recorded only | No higher predicate; the result explains the classification in `notes` |
| `V1` | Numerically checked | A numerical method with recorded precision |
| `V2` | Proof asserted but not publicly recoverable | Declared with `notes` explaining the unavailable proof |
| `V3` | Published or audited proof | `method: published-proof` or `proof-audited`, with a `proof` block |
| `V4` | Machine-verified | Exact-algebraic or interval-certified evidence with a certificate, replay command, and passing replay status |
| `V5` | Proof-assistant checked | `method: proof-assistant-checked` |

The checker derives `V1` and `V3`–`V5` from the evidence cited by the result.
`V0` and `V2` are declared because the current evidence fields do not distinguish an
ordinary unsupported claim from an asserted but unavailable proof; both require an
explanatory `notes` field.
The evidence schema separately enforces its own provenance, limitations, and
method-specific fields.

## Confirmation

Confirmation counts only work recorded as `audited-here` or `replayed-here`, except
`C1`, which describes a qualifying read of external evidence.

| Rung | Meaning | Structural support |
| --- | --- | --- |
| `C0` | Recorded | No qualifying read or repository replay |
| `C1` | Read | An `external_review` with a qualifying state, date, reviewer, and note |
| `C2` | Replayed | Repository-origin evidence with a replay command and `replay_status: passed` |
| `C3` | Machine-confirmed | Repository-origin exact-algebraic or interval-certified evidence with a certificate and passing replay |
| `C4` | Confirmed by distinct methods | At least two `C3` evidence entries with different `method` values |
| `C5` | Review-ready | `C3` or `C4`, plus an existing `review_artifact` mapped as a non-superseded review |

For `C1`, a qualifying review state is `informally-verified` or `defect-found`; the
review note records what was examined and what remains unchecked.
A `C3` or higher result must also name at least one existing control path.
The evidence schema requires a limitations statement on every evidence entry.

These predicates are deliberately literal.
Two independently written implementations using the same method still derive `C3`, not
`C4`. A control path proves that a control is retained; the checker does not infer from
its filename that the control is adversarial.
The test suite, validation configuration, and review establish those stronger facts.

## Scope and Composition

A classification attaches to the exact statement in a result’s `claim` field and its
declared scope.

- A compound claim takes the minimum rung of its load-bearing parts.
- A derived claim takes the minimum rung of its inputs and the derivation itself.
- A construction’s feasibility, the sharpness of its parameter, and global optimality
  are separate claims.

The checker derives the strongest rung present among the cited evidence entries.
When a compound or derived result declares a lower rung, its `composition` note
identifies the part that sets the minimum.
That note, the relevance of each evidence reference, and coverage of every load-bearing
premise are review obligations rather than machine inferences.

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

Other people work on `s(n)` alongside this project: some from its certificates, some
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
  `4.66001` builds on Squares Project (Joshua Levy), Mira and Guzhou0806. The atlas
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
README’s three results tables, [New Results](README.md#new-results),
[Results by Others](README.md#results-by-others) and the recent results by case.
The README keeps a little prose around those tables, the `s(11)` thread and the results
outside the register, and that prose names the `T-NNN` it restates, so the register gate
can find it.

| Record | Holds | Reader view |
| --- | --- | --- |
| [`n-NNN.md`](packing/frontier/README.md) case records | Both lanes’ bounds for each case, with their evidence | [`STATUS.md`](packing/frontier/STATUS.md); README’s [recent results by case](README.md#recent-results-all-sources); the standing column of README’s register tables |
| [`evidence.yaml`](packing/frontier/evidence.yaml) | Who performed each check, by which method, within which limits | [`INVENTORY.md`](packing/frontier/INVENTORY.md) |
| [`results.yaml`](packing/frontier/results.yaml) | Each result’s headline, claim, date, `V`/`C`/`S`, novelty and attribution | [`RESULTS.md`](packing/frontier/RESULTS.md), grouped by lineage; README’s New Results and Results by Others tables |
| [`bibliography.yaml`](packing/resources/bibliography.yaml) | Each source’s date, credit and lineage | The atlas citation line; the holders in README’s recent results; the credit and relation in README’s Results by Others |
| [`source-coverage.yaml`](packing/frontier/source-coverage.yaml) | Which sources were read, and when | None |

## Enforcement and Register

Run the executable contract from `packing/` with:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_results
```

The checker:

- resolves evidence references and artifact, control, and review-document paths;
- derives the structural `V` and `C` rungs described above;
- refuses unsupported promotion and unexplained understatement;
- requires `C5` review documents to be non-superseded reviews in
  [`document-map.yaml`](docs/project/document-map.yaml);
- requires `attribution` on every `previously-published` result and refuses it on a
  novel one, resolves its source keys in the bibliography, and requires a `lineage` on
  the sources of a result by others published since 22 August 2026;
- requires a `headline` of at most 100 characters on every result, stating no number its
  claim does not, and an `established` date on every result without `attribution`, the
  day its certificate or proof first passed here, which it refuses beside `attribution`
  and before 22 August 2026;
- fails when a case’s reported or verified lower bound cites evidence from a source
  dated on or after 22 August 2026 that no register entry covering that `n` cites; and
- rejects unknown `T-NNN` references in the README and synopsis.

[`packing/frontier/results.yaml`](packing/frontier/results.yaml) states each result’s
headline, claim, scope, classifications, evidence, artifacts, and `next_rung`. The
headline is the claim shortened for a table cell; the claim stays the statement the
rungs attach to. That final field records the next evidence-improving action or explains
why no independent rung change applies.
[`packing/frontier/RESULTS.md`](packing/frontier/RESULTS.md) is generated from the
register and sorted for readers.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
