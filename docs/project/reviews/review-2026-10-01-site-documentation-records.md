# Review: The Site’s Documentation Cards and the Records Behind Them

Reviewed 2026-10-01 on `claude/site-docs-records`, cut from `main` at `fe6399451`, under
bead `think-bk2e`. The owner asked whether the site’s documentation section should still
carry `RESULTS.md` and `STATUS.md`, whether they are maintained or subsumed, whether
`SYNOPSIS.md` is properly maintained, and directed that `defects.md` leave the site and
that `README.md` and `epistemics.md` come first.

This is a dated record.
Line numbers in `SYNOPSIS.md` are those at `fe6399451`, before this branch’s edits.
“The site” is the build of `devtools.preview_site` at that commit, without the two
papers and the workbench.

## Answers

**`RESULTS.md` and `STATUS.md` are maintained, and the site no longer needs either.**
Both are generated, both matched their sources at `fe6399451` (`render_results --check`,
`render_research_tables --check`), and the gate fails when either drifts.
Neither is edited by hand: the gate refuses a file that differs from a fresh render.
The site’s results table and frontier atlas are built from the same records by the same
functions, and show everything the two files show except three things listed below.
Their cards and pages are removed from the site.
The files stay in the repository, where they are the plain-text views a person working
in a checkout reads, and where the gate, the synopsis and the campaign’s records depend
on them.

**`SYNOPSIS.md` is maintained where a check holds it, and has drifted where none does.**
Of 31 factual statements checked across its sections, 13 are current, 16 are stale and 2
are wrong today. Every current one is in a generated block, is held by one of
`check_synopsis`’s fifteen checks, or is prose from the last week that nothing has yet
overtaken. Every stale or wrong one is free prose.
Seven of the sixteen stale ones name rungs from the ladder in force before 2026-09-30,
which [`epistemics.md`](../../../epistemics.md#what-changed-on-2026-09-30) says to read
as dated; the rest are counts and narrative that later work passed.

**`defects.md` is off the site**, and the cards now lead with `README.md` and
`epistemics.md`.

## The Documents, One by One

The documentation section listed eight documents, and the site built a page for each and
one more for the tutorial, which is a card on the Papers page.
Two documents a reader might expect are not on the site and are included for comparison.

| Document | Produced | Last real change | Held current by | On the site also as | Recommendation |
| --- | --- | --- | --- | --- | --- |
| `README.md` | Hand-written. Two marked blocks are read by the overview as its own prose (`site_documents.shared_blocks`); nothing writes them | 2026-10-01: the introduction rewritten, the ladders’ wording | `check_readme` (links, layout tree, report index, work model, the two blocks); `check_results` (every result id it names); the render fails on a dead link | The overview’s first two sections | **Card, first** |
| `epistemics.md` | Hand-written. The site reads each rung’s short form from it | 2026-09-30: the ladders redefined, a short form for every rung | `check_results` derives every rung from its predicates; `tests/test_results_register.py`; the site’s ladder tests | The overview’s Verification Ladders, in short | **Card, second** |
| `SYNOPSIS.md` | Hand-written, 7,195 lines, with three generated blocks (823 lines: the results headline, the document map, the session-close report) and two marked blocks a check keeps attached to their sources | 2026-10-01: ten commits by the research session, each to the handoff, the roll-ups or a round’s row | `check_synopsis`, fifteen checks, on numbers and statuses; `render_results_headline --check`; `render_document_map --check`. Prose outside those is unchecked | Nothing; the overview and four documents link into it | **Card, third**, with the drift below listed for the owner |
| `conventions.md` | Hand-written | 2026-09-14: the correction rule in §7. Since then only the math migration | `check_documentation` (map, footer, links); `check_session_gate` and `check_synopsis` read parts | Nothing | **Card, fourth** |
| `development.md` | Hand-written | 2026-09-30: the tier drift rules, the optimality paper’s build | `check_gate_budgets` (every tier is named); `check_documentation` | Nothing | **Card, fifth** |
| `TUTORIAL.md` | Hand-written | 2026-09-30: brought up to T-060 | `check_documentation`; the render fails on a dead link | A paper on the Papers page | **Page, as now**; not a documentation card |
| `packing/frontier/RESULTS.md` | Generated whole by `render_results` from `results.yaml` and the bibliography | 2026-09-30: every rung re-derived; ten commits that day, each a regeneration after a register edit | `render_results --check`, in the step “results rungs are earned and the view agrees”, on every change | The results table, each result’s overview, the case records | **Repository only**; forward `results.html` |
| `packing/frontier/STATUS.md` | Generated whole by `render_research_tables` from the 324 case files and `evidence.yaml` | 2026-10-01: the $n = 17$ row, twice; each of the last ten commits regenerates one to three rows | `render_research_tables --check`, in “generated tables in sync with frontier/” | The frontier atlas and the case records | **Repository only**; forward `status.html` |
| `defects.md` | Generated whole by `render_defects` from `defects.yaml`, 511 defects | 2026-10-01: two commits, each a regeneration after a defect was logged | `render_defects --check`, in “defect log” | Nothing | **Repository only**, by the owner’s decision; forward `defects.html` to the file |
| `operating-rules.md` | Hand-written; `AGENTS.md` mirrors its summary | 2026-09-30 | `render_operating_rules --check` | Not on the site | Leave off the site: it is for agents working in the repository |
| `packing/frontier/README.md` | Hand-written | 2026-10-01 | `check_nagamochi_bounds` and two contract tests read parts | Not on the site | Leave off the site; the frontier atlas’s own prose covers what a reader needs |

Each of the three removed pages was linked from the others’ pages, because a relative
link to a rendered document became its page: 121 links to `results.html` (94 from the
synopsis, 11 from the case records), 9 to `status.html`, and 153 to `defects.html` (137
from the synopsis). No template of the site linked `results.html` or `defects.html`
outside the cards; the overview’s survey linked `status.html` once.

## `RESULTS.md` Against the Site

| In `RESULTS.md` | On the site |
| --- | --- |
| The opening paragraph on the axes | The results page’s own prose, the overview’s Verification Ladders, and `epistemics.html` |
| This project’s results: id, $n$, `V`, `C`, `S`, novelty, claim | The results table’s rows, filtered to this project; the full claim and the novelty label are in each result’s overview |
| Results by others, with credit, date, rungs and standing | The same rows, with the same credit line and standing, from the same functions (`result_credit`, `render_recent_results.standing`) |
| Four lineage groups as headings | **Not shown as groups.** Each row’s credit names whom the source builds on (“after Levy, Kleddamag”), and a filter separates this project’s results from others’; the four-way classification itself is only in the file |
| Within a group, results still waiting on a replay here listed first | **Not an order the table offers.** It sorts by any column and filters by `C` |
| Next actions, one line per result | Each result’s overview, under “Next rung” |
| “Register reviewed 2026-09-30” | **Not shown** |

So three things are only in the file: the lineage headings, the replay queue’s order,
and the register’s review date.
None is a reason to keep a page.
All three matter to someone working the register, which is what the file is for.

## `STATUS.md` Against the Site

`STATUS.md` is one table of 324 rows.
The frontier atlas is the same table from the same records, formatted by the same
module, with the packing drawn in each row.
The reported and verified bounds, the status, the gap, the verification origin and the
conflict notes are all there, the last two in the row’s popover.
Only the per-case **review date** is in the file and not on the site.

## `SYNOPSIS.md`: Thirty-One Statements

| Line | Statement | Verdict | Against |
| ---: | --- | --- | --- |
| 3 | Date 2026-09-30 | stale, fixed | Last revised 2026-10-01 (`58d237c8c`) |
| 10 | Evidence cutoff: the T-060 replay of 2026-09-30 | stale, fixed | The handoff at line 1314 covers Session 165 of 2026-10-01 |
| 24 | $n = 11$ is solved at Trump’s side | current | `n-011`, T-060 |
| 41 | A claim register for every $n \le 100$ | stale, fixed | 324 case files |
| 72 | T-026 at `V4/C5` | stale rung | `V3/C3` in the register |
| 74 | T-033 at `V4/C3` | stale rung | `V3/C3` |
| 74 | $s(11) = T = 3.877083590022814\ldots$, T-060 matching T-011 | current | `n-011` |
| 76 | T-037 and T-061 are earlier bounds | current | Both superseded |
| 92 | The native decision supports `V4/C4` for Kleddamag’s bound | stale rung | T-037 is `V3/C3` |
| 121 | R068’s $116511/25000$ is the verified bound, $0.0151$ below the packing | current | `n-017`: the gap is $0.01509$ |
| 123 | T-038 to T-043 are registered | current | The register |
| 132 | $s(32) = 6$ and $s(12) \ge 15680/3951$ at `V4/C4`; $s(21) = 5$, $s(45) = 7$ at `V4/C3` | stale rungs | T-049 and T-051 to T-053 are `V3/C3`; the bounds stand |
| 137 | Daniel’s proof of $s(13) = 4$ “is recorded as a report” | **wrong**, fixed | T-006: kernel-checked in Lean here on 2026-09-30 |
| 155 | The headline table: 61 results and their rungs | current | Generated; `--check` passes |
| 247 | The status block: 165 sessions, 170 experiments, 61 results, 33 by others | current | Check 11 |
| 268 | Agenda 040 is the current overnight queue | stale | Agendas 041 and 042 are active and later |
| 271 | Session 143 is the latest terminal closeout | stale | Session 165, as line 1314 says |
| 320 | The exact value is $s(11) = T$ by T-060 and T-011 | current | `n-011` |
| 324 | Method-distinct `C4` confirmation of the strict bound | stale rung | T-037 is `C3` |
| 456 | Bounds side by side through $n = 100$ | stale, fixed | 324 |
| 1314 | The handoff: Session 165, seven $n = 17$ rounds, the verified ceiling $4.67553009360455\ldots$, the lower bound $4.66044$, next `think-11ma` | current | The session record, `n-017`, check 13 |
| 1335 | T-060 is `V3/C3/S5` under the current rubric | current | The register |
| 3975 | The $n = 11$ fact table | current | Check 15 |
| 4049 | $n = 11$: proved, a settled target | current | `n-011` |
| 4050 | $n = 12$: open, two rounds | stale | True as far as it goes; omits T-017 and the verified $15680/3951$ |
| 4052 | $n = 17$: one round, `exp-011` | stale | Seven more on 2026-10-01, `exp-235` to `exp-241` |
| 4054 | The corpus: 1–100, 39 proved, 61 open | stale, fixed | Right for $n \le 100$; the corpus is 324 cases, 63 proved and 261 open |
| 4178 | The $n = 11$ ladder’s rung column: `V4/C5` and `V4/C3` | stale rungs | All six are `V3/C3` |
| 4480 | T-060 audited here at `V4/C5/S5` | **wrong**, fixed | `V3/C3/S5`; contradicts line 1335 |
| 6204 | The log contains 511 defects | current | Check 5 |
| 6815 | “All four stand at V4 … T-018 at C5 — the rung epistemics.md defines as review-ready” | stale | `epistemics.md` no longer defines `C5` so; all four are `V3/C3` |

The split follows the checks.
The generated blocks and the checked numbers are current to the day, and so is the
handoff, which check 13 ties to the latest session.
The free prose around them was last true on the day each passage was written.

### What Was Fixed

Counts and plain facts with one right value in the record: the date and the cutoff; the
three places that still said $n \le 100$; the corpus counts; T-060’s rung in the section
that announces it; and the $s(13)$ sentence.
One sentence was added under the headline table’s introduction, saying that the table
carries the current rungs and that a rung in the prose is the one in force when the
passage was written, with a link to the rule in `epistemics.md`. `TUTORIAL.md` and
`conventions.md` each had one $n \le 100$ of the same kind, also fixed.

### What Is Left for the Owner

These are rewrites of narrative, not corrections of a value:

1. **Results and their significance** (lines 66–152) reads as a current summary and
   names ten pre-ladder rungs.
   The added sentence covers it.
   Recommendation: trim this section to its first paragraph and the generated table,
   since the site’s results table now tells the same story from the record.
2. **Research Program Status and Roadmap** (lines 257–438): the agenda eras stop at
   Agenda 040 and the session narrative at Session 143, twenty-two sessions back.
   Recommendation: cut the narrative to the generated status block and a pointer to the
   Current Handoff, which a check holds.
3. **The Lay of the Land, by `n`** (lines 4040–4083): the rows for $n = 12$ and $n = 17$
   predate the September intake and the October rounds.
   Recommendation: mark the table as the search programme’s view as of August, or drop
   the two rows’ round counts.
4. **`n = 11`, End to End** (lines 4085–4472) and **Where This Stands** (lines
   6768–7159) argue from the old rungs, the second from a definition of `C5` that
   `epistemics.md` no longer has.
   Recommendation: mark both as dated record, as the first already half does (“the
   former open-case account”).
5. **`README.md`, lines 111–117**: the small-$n$ audit and the W10 route-selection
   review of 14 September are introduced as challenging “the current research
   approaches”. They predate T-060. Recommendation: drop the two sentences.

Overall recommendation for the synopsis: **keep it on the site, and trim it toward what
is generated or checked.** It is the only document that holds the workflow contracts,
the terminology and the handoff, and the overview and four documents link into it.
Its unchecked narrative is where it goes stale, and most of that narrative now has a
generated counterpart on the site.

## What Depends on `RESULTS.md` and `STATUS.md`

Neither should be deleted or left ungenerated without replacing these:

- **Gates.** `render_results --check` and `render_research_tables --check` run on the
  pull-request surface.
  `check_generated_markdown` and `.flowmarkignore` name both files.
- **The synopsis.** Every row of its generated headline links `RESULTS.md`
  (`render_results_headline.REGISTER_VIEW`), and 94 links in its prose do.
- **Other records.** `RESULTS.md` is linked from 53 campaign records, 18 documents under
  `docs/project/`, two case files, `README.md`, `TUTORIAL.md`, `epistemics.md`, one
  defect, and both papers.
  `STATUS.md` is linked from 26 campaign records, 10 documents under `docs/project/`,
  the frontier guide (which says to start there), `INVENTORY.md` and `README.md`.
- **Tests.** Nine test modules name `RESULTS.md` and four name `STATUS.md`, among them
  the typography test of the generated tables and the change-scoped selection of gate
  steps.
- **The document map** lists both as generated views.

Retiring either would mean repointing every one of those at a site page, which only
exists once the site is deployed.
A checkout has no site.
The recommendation is to keep generating both.

## What This Pass Changed

- **Cards**, in order: `README.md`, `epistemics.md`, `SYNOPSIS.md`, `conventions.md`,
  `development.md`. The first two are the owner’s; the synopsis follows as the full
  record; the two reference documents close, the record’s formats before the code.
- **Pages removed:** `results.html`, `status.html`, `defects.html`. Each old address is
  still served, as a forwarder with a refresh and a link for a reader without scripts:
  to `all-results.html`, to `frontier.html`, and to `defects.md` on GitHub.
  The query string and the fragment are kept.
- **Links repointed.** In every reader document and case record, a link to `RESULTS.md`
  now leads to the results table, at the result’s row when the link’s text is a result’s
  id (106 of the 121); a link to `STATUS.md` leads to the frontier atlas; a link to a
  case file leads to that case’s record on the site.
  A link whose text names the file itself, as `epistemics.md` does where it says the
  view is generated, opens the file on GitHub.
  A link to `defects.md` opens the file on GitHub: each is a citation of a defect.
- **The overview’s survey** no longer links the status table, and links the $n = 7$ and
  $n = 17$ case records on the site instead of their files.

## Not Changed

The two papers link `RESULTS.md` on GitHub: the explainer’s footnote on the register,
and the optimality paper’s “T-060 result record”, which is pinned to its commit.
Both could lead to the results table.
They are left because the papers are being moved to new addresses on another branch, and
the explainer’s bytes are bound to its PDF.

The reader documents cite experiments, reviews and research reports under
`packing/campaign/` and `docs/project/` as evidence.
Those links were left: no page of the site shows the same thing.

## How This Was Measured

From `packing/`, with the project interpreter:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_results --check
uv run --frozen --all-extras --group dev python -m devtools.render_research_tables --check
uv run --frozen --all-extras --group dev python -m devtools.render_defects --check
uv run --frozen --all-extras --group dev python -m devtools.render_results_headline --check
uv run --frozen --all-extras --group dev python -m devtools.check_synopsis
uv run --frozen --all-extras --group dev python -m devtools.preview_site --output DIR \
  --skip explainer --skip workbench --skip optimality
```

All five checks passed at `fe6399451`. Inbound links were counted in the built pages.
Each document’s history is `git log --numstat` on its path; a commit that only merged is
not counted as a change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
