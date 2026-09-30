---
title: A Top-Level Overview Page for the Published Site
description: A clean landing page on GitHub Pages that summarizes the project and every current result, with navigation to the explainer, tutorial, synopsis and workbench
author: Claude (agent), for the repository owner
---
# Feature: A Top-Level Overview Page for the Published Site

**Date:** 2026-09-29

**Author:** Claude (agent), for the repository owner

**Status:** Reviewed; in implementation

**Tracking:** `think-xjq4` (epic) and its sixteen child beads

**Workflow:** W7 pipeline improvement

**Reviewed baseline:** `8af542a9` (main after PRs #241, #242 and #243)

## Overview

The published site at `https://jlevy.github.io/squares/` has one top-level page, and it
is the n = 11 explainer (`packing/site/index.html`, rendered by
`packing/devtools/render_explainer.py`). The workbench sits at `/workbench/` and links
back to it. A reader who arrives from a citation or a search result lands in the middle
of a certificate proof, with no page that says what the project is, what it has found,
or where the other documents are.

This plan adds an overview page at the site root: a clean, simpler cousin of `README.md`
that states the problem, the headline bounds, what this project and others have proved
since 22 August 2026, and how each result is verified.
It carries a results table generated from the register, with verification statistics and
a link from every row to the records that back it.
A shared navigation bar joins it to the explainer, the tutorial, the synopsis and the
workbench, so a reader can move between pages without going through GitHub.

The overview is generated from the record, never hand-maintained: a result in
`packing/frontier/results.yaml` is a row on the page, and a case bound on the page is
the one in `packing/frontier/n-NNN.md`.

## Goals

- A top-level overview page at the site root, simpler than `README.md` but covering the
  same ground: the problem, the headline brackets (`s(11)`, `s(17)`, the new exact
  values), this project’s results, results by others, the survey, and the research
  process.
- Links from the overview to the explainer, the tutorial (`TUTORIAL.md`) and the
  synopsis (`SYNOPSIS.md`), and to the workbench, the atlas figures and the ascent
  films.
- One navigation bar, the same on every site page, so each page links to every other.
- Every new page follows the kpress design system the explainer already uses (its
  tokens, reading faces, math, tables, TOC rail, light and dark themes and print rules),
  extended only where a page needs something the system lacks, such as sortable and
  filterable tables.
- A results table with full details: identifier, `n`, bound, credit, `V`, `C` and `S`
  rungs, novelty, date, and links to the case record, the register entry, the evidence,
  the retained source copy and the review, where each exists.
- Verification statistics: how many results stand at each `V` and `C` rung, how many are
  this project’s and how many are others’, and how many of the hundred atlas cases are
  proved, open with a verified bracket, or carry a recent verified lower bound.
- A “what changed recently” section that summarizes the newest results and the releases
  they arrived in, generated from the register and the release record rather than
  written by hand.
- A frontier atlas page, separate from the overview: one table with a row for every
  `n = 1…324`, each value rendered cleanly from the case’s `SquarePackingCase/v2`
  softschema record in `packing/frontier/n-NNN.md`.
- Mathematics written as LaTeX math (`$…$` and `$$…$$`) across the repository’s Markdown
  wherever it is currently set as monospace code, and rendered wherever the documents
  are read: on GitHub, on the site pages, and in generated documents.
- A local preview of the whole site (overview, frontier atlas, explainer, tutorial,
  synopsis, workbench) with desktop and phone screenshots, reviewed by the owner before
  anything deploys.

## Non-Goals

- Deploying. Nothing in this plan pushes to `main` or runs the Pages deploy until the
  owner has seen the full overview in a local preview and approved it.
  The Pages deploy and `upload-pages-artifact` run only for a push to `main`, and `push`
  is filtered to `main`, so a branch push runs nothing and a pull-request build checks
  without deploying.

- Changing the explainer’s content, its PDF, or the workbench beyond the shared
  navigation bar and the move described under [URL Layout](#url-layout).

- Changing data under `DATA_PATHS` beyond the two register fields the page needs
  (`registered` and `headline`, under [Data Changes](#data-changes)). Everything else is
  read as it stands.

- Rewriting the prose of `README.md`, `TUTORIAL.md` or `SYNOPSIS.md`. They are rendered
  as they are, apart from the math markup migration in Phase 3.

- Editing archived source material under `packing/resources/` or the vendored
  submodules, or quoted source text anywhere, even to convert its math.
  Archived source is never edited to look tidy.

- Live data. The page is static and self-contained, built at a commit, like the
  explainer.

## Background

What the site publishes now (from `.github/workflows/pages.yml` and the builders):

| Path | What | Built by |
| --- | --- | --- |
| `/` | the n = 11 `t-018` explainer | `devtools.render_explainer` |
| `/t-018-explainer.md`, `/t-018-explainer.pdf` | its Markdown and PDF editions | `render_explainer`, `render_explainer_pdf` |
| `/known-best-1-100.*`, `/known-best-1-324.*`, `/ascent-n1-100-poster.png` | atlas composites and the film poster | copied beside the page (`COMPOSITE_ASSETS`) |
| `/workbench/` | the interactive workbench | `workbench_tools.build_site` |

The films are GitHub release assets, and every other document is reached through
repository permalinks.

The data the overview summarizes already exists and is already gated (counts at the
baseline):

- `packing/frontier/results.yaml` (`ResultsRegister/v1`), 55 entries `T-001` to `T-055`,
  with `claim`, `scope`, `verification`, `confirmation`, `significance`, `novelty`,
  `evidence`, `artifacts`, `review_artifact` (set on 9 entries) and, on 27 entries,
  `attribution`, 19 of which (`T-037`–`T-055`) PR #243 added.
  `devtools.check_results` derives the rungs; `devtools.render_results` renders
  `frontier/RESULTS.md`; `devtools.significance` ranks them.
- `packing/frontier/n-001.md` … `n-324.md` (`SquarePackingCase/v2`), with reported and
  verified bounds, rendered to `frontier/STATUS.md` by
  `devtools.render_research_tables`.
- `packing/atlas/known-best/` (`manifest.json`, `bound-citations.json`,
  `composite-figure.json`), which already knows which bounds are recent and whom they
  credit.
- `packing/src/sqpack/release.py`: `PUBLICATION_EDITION` and `DATA_REVISION`, which
  every published artifact stamps.

The recent merges the page has to reflect:

- PR #243: others’ results registered beside this project’s (`T-037`–`T-055`), with
  original credit and this repository’s verification tracked apart.
- PR #242: every results listing and the survey refreshed for all sources, grouped by
  lineage.
- PR #241: Evan Daniel’s `s(21) = 5` and `s(45) = 7`, Guzhou0806’s R068 at
  `s(17) > 116511/25000`, and wand125’s rectangle bounds to `n = 95`.
- PRs #239 and #240: the v0.4.2 edition, the starred recent results on the atlas, and
  the ascent films.

## Design

### Approach

A new renderer, `packing/devtools/render_overview.py`, built on the same kpress calls as
`render_explainer.py`: it reads declared inputs, fills Markdown article templates,
renders them with kpress `render_page`, writes self-contained pages into
`packing/site/`, and declares its inputs as `RENDER_INPUTS`. It renders four pages: the
overview, the frontier atlas, and HTML editions of the tutorial and the synopsis.
The explainer and workbench builders gain only the shared navigation bar.

These pages render math with kpress’s `math="auto"` and KaTeX, and do **not** use the
explainer’s `--prepare-math` geometry pass, which measures math in Chromium for the
explainer’s figures and PDF. The tutorial has no math and the synopsis has about
fourteen inline spans and one display block, so no new geometry, typography or PDF jobs
are added to `pages.yml`.

Each page is deterministic at a commit.
`--check` compares a fresh render with the file on disk, as the explainer’s does, and
the `overview` job renders twice and compares the bytes, as the explainer’s twin step
does.

The data layer reuses the register’s own code rather than re-deriving it:

- grouping and ordering: `render_results`’ `_lineage`, `_credit`, `_order`,
  `holds_a_bound` and `OTHERS` are made public and composed into one `grouped_results()`
  that both `RESULTS.md` and the overview call (it puts others’ entries still awaiting a
  replay first, then orders by `significance`);
- summaries, scopes and rung legends: `significance.headline`, `scope_label` and
  `anchors`, the last generalized to take the axis letter so the `V` and `C` tables in
  `epistemics.md` supply the tooltips;
- case values: `render_research_tables.load_cases`, `pretty`, `compact_bound` and
  `case_disposition`;
- atlas totals: the `known-best-1-100` totals in `composite-figure.json`
  (`proved_optimal`, `lower_bound_recent_result`, `lower_bound_first_proved_here`), read
  rather than recounted.

### URL Layout

| Path | Page |
| --- | --- |
| `/` | the overview (new) |
| `/frontier.html` | the frontier atlas, `n = 1…324` (new) |
| `/explainer.html` | the n = 11 explainer (moved from `/`) |
| `/tutorial.html` | `TUTORIAL.md`, rendered (new) |
| `/synopsis.html` | `SYNOPSIS.md`, rendered (new) |
| `/workbench/` | the workbench (unchanged) |
| `/t-018-explainer.{md,pdf}` and the composite assets | unchanged |

The explainer moves to `/explainer.html` rather than `/explainer/` so it stays beside
the composite assets and PDF it references with relative paths.

**The explainer is renamed at publish, not at render.** `pages.yml` names
`site/index.html` about forty times across the twin render, the PDF, and the geometry,
typography and font jobs, and `render_explainer_pdf.PAGE` and several tests pin it.
Renaming the render output would touch every one of them for no reader-visible gain.
Instead the explainer build keeps writing `site/index.html` inside its own artifact, and
`publish` renames it to `explainer.html` before the overview’s `index.html` is merged
in. What does change, because a reader or a checker sees it:

- `render_explainer.CANONICAL_URL` (and `og:url`) becomes `SITE_URL + "explainer.html"`;
  `SITE_URL` itself stays the directory URL, since `site_file`, the PDF link base and
  `absolute_links.js` resolve against it;
- the Markdown edition’s links to “the page”;
- `check_published_site`: the explainer is fetched as `explainer.html`, the overview as
  the root, and each is checked for its edition stamp and canonical URL;
- `README.md` lines 64 and 90 and `TUTORIAL.md` line 129
  (`/#proof-of-the-new-lower-bound`) point at `/explainer.html`, and the README gains a
  link to the overview.

**Old deep links keep working.** Links into the explainer carry its state in the
fragment: section ids, footnotes (`#fn-3`) and the certificate picker (`#19-5`,
`#381-100`, read by `explainer/page.js`). A list of anchors would miss the last two.
So the overview’s forwarding script sends any non-empty fragment that is not an id on
the overview to `explainer.html` with the same fragment and query string
(`?review=fonts` must survive).
A test asserts that the overview’s ids and the explainer’s are disjoint, so no old link
is captured by the overview.
The script lives in a `.js` file under the browser floor and needs nothing from the
explainer build, so the overview job does not depend on `prepare`.

### The Overview Page

Sections, top to bottom:

1. **Header and navigation bar.** The project name, the edition stamp
   (`PUBLICATION_EDITION`), and links to Overview, Frontier, Explainer, Tutorial,
   Synopsis, Workbench and the GitHub repository.
   The current page is marked.
2. **The problem.** Two or three sentences defining `s(n)`, and the central bracket
   `31/8 < s(11) ≤ 3.8770835…` with its gap, read from `n-011.md`.
3. **Headline results.** Cards for the `S5` results (six at the baseline) and the new
   exact values (cases whose `status` is now `proved` by a recent result), each with its
   bound, its credit, its `V`/`C` rungs, and a link into the table.
4. **The atlas.** The `known-best-1-100` figure (already served beside the page), with
   links to the PDF, the `1…324` poster and the two ascent films on the release.
5. **Results table.** Described [below](#the-results-table).
6. **Verification at a glance.** The statistics in the goals, as a small set of counts
   and one stacked bar of `C` rungs by source, drawn as inline SVG at render time.
7. **What changed recently.** The newest results by registration date and the release
   each arrived in, with the release notes linked.
8. **Read further.** One-line descriptions of and links to the explainer, the tutorial,
   the synopsis, the workbench, the survey (`frontier/STATUS.md`), the results register
   (`frontier/RESULTS.md`), `epistemics.md`, and the research process.
9. **Footer.** Edition, data revision, build commit, and the licence.

The prose around generated blocks (the problem statement, section introductions) lives
in a template, `packing/devtools/templates/overview-article.md`, so it is reviewed as
prose and formatted by flowmark.
The facts inside it are placeholders filled from the record, so a bound never appears in
the template as a literal.

### The Results Table

One row per register entry, grouped and ordered exactly as `RESULTS.md` is, through the
shared `grouped_results()`.

| Column | Source |
| --- | --- |
| ID | `id` |
| `n` | `scope.n_values`, compressed to ranges |
| Result | `headline`, else `significance.headline`; the full `claim` in an expandable row |
| Credit | “This project”, or `attribution.source_keys` resolved through `resources/bibliography.yaml` (`credit`, else `authors`), as `render_results` does |
| `V` / `C` / `S` | `verification`, `confirmation`, `significance.score`, with the rung definitions from `epistemics.md` as tooltips |
| Novelty | `novelty` |
| Registered | `registered`; `attribution.published` alongside for others |
| Records | the case file (or the frontier atlas filtered to the scope, for ranges such as `18–95`), each `evidence` entry at its line in `evidence.yaml`, the entry’s line in `results.yaml`, `review_artifact` where set, and the retained source copy through the evidence entry’s `certificate` or `proof.source` path |

The expanded row adds `composition`, `next_rung`, `artifacts` and `controls`, each
linked. Every repository link names `main` (`devtools/repo_links.py`); the deployed-site
check refuses one pinned to a commit hash.
Amended 2026-09-30: build-commit permalinks 404ed once a squash merge left the commit on
no branch.

Behaviour: the table works with JavaScript off (all rows present, `<details>` for
expansion). A small script adds sorting by column and filters by source, `n` and `C`
rung. It lives in `packing/devtools/overview/table.js` with JSDoc types, its own
`tsconfig.overview.json`, and Biome and `tsc` coverage, the same arrangement as the
explainer’s scripts.

The overview links to the [frontier atlas](#the-frontier-atlas-page) for case-by-case
bounds rather than repeating them.

### The Frontier Atlas Page

A separate page, `/frontier.html`, with one row for every case `n = 1…324`. Each row is
rendered from the case’s softschema record, the `packing:` envelope of
`packing/frontier/n-NNN.md` under the enforced `packing.squares:SquarePackingCase/v2`
contract, loaded and validated the way `validate.py` and
`devtools.render_research_tables.load_cases` already load it.
No value on the page is typed by hand or read from `STATUS.md`.

| Column | Source in the case record |
| --- | --- |
| `n` and thumbnail | `packing.n`; the drawing `atlas/known-best/rendering/n-NNN.svg`, inlined |
| Status | `status` (and `reported_status` where they differ) |
| Best known packing | `reported_upper_bound`: `value`, `exact_form`, `found_by`, `found_year`, `construction_method`, `catalogue_rigid` |
| Verified upper | `verified_upper_bound`: `exact_form`, else `value` |
| Reported lower | `reported_lower_bound`: `exact_form`, `kind`, `proved_by`, `proved_year`, `source_key` |
| Verified lower | `verified_lower_bound`: `exact_form`, else `value` |
| Gap | verified upper minus verified lower, computed exactly where both are exact |
| Recent | a star when the verified lower bound is recent, from `bound-citations.json`, as on the atlas figure |
| Records | the case file, and each `evidence` id on the bounds, linked |

**Rendering values cleanly.** Exact forms are shown as mathematics, not as ASCII: `31/8`
as a fraction, `2 + (1/2)√2` with a radical, a `root(P, x)` form as its decimal with the
minimal polynomial (`minimal_polynomial`) in the expanded row.
The formatting reuses `render_research_tables.pretty` and `compact_bound` where they
already do this, and extends them in one place rather than forking them.
A reported value that agrees with the verified one at declared precision is shown once,
using `sqpack.assurance.bounds_agree_at_declared_precision`, the same test `STATUS.md`
applies.

**Behaviour.** The full table is in the HTML, so it reads with JavaScript off.
The same script as the results table adds sorting and filters (status, open only, recent
only, a range of `n`). The thumbnails are small inline SVGs; the page is checked against
a size ceiling so 324 drawings do not make it slow to load.

**Tests.** Every case file is a row and every row is a case file; each rendered value
equals the record’s value (parsed back from the cell’s `data-` attribute); an invalid
record fails the render rather than rendering a blank cell.

### Tutorial and Synopsis Pages

`TUTORIAL.md` (about 1,600 lines) and `SYNOPSIS.md` (about 6,900 lines) are rendered
with kpress `render_page` in `trust_mode="sanitized"`, with its TOC rail from the
headings. Heading ids come from kpress’s GitHub-compatible slugger, so existing
`SYNOPSIS.md#…` anchors carry over.

Links are rewritten in the rendered HTML (`href` and `src` after parsing), never by a
regular expression over the Markdown, which would also match `](` inside code spans:

- a link to another rendered document (`README.md#…`, `SYNOPSIS.md#…`, `TUTORIAL.md#…`)
  becomes the site page (`README.md` maps to the overview, with a fallback to the
  repository for README-only anchors);
- any other relative link becomes its link on `main`, `blob/` or `tree/` according to
  whether the target is a file or a directory (amended 2026-09-30, formerly a permalink
  at the build commit);
- images under the repository become raw files on `main`, or served assets when they
  already are.

The synopsis has 1,655 relative links to 1,143 targets.
They are checked offline, against the rendered commit’s tree (`git ls-tree`), which is
`main` at the deploy, and kpress’s `broken_anchor` diagnostic is raised to a failure.
`check_published_site`’s per-link HTTP check stays on the overview and frontier pages
only, so the deployed-site check does not send over a thousand requests to GitHub.

### Shared Navigation and Style

**The explainer’s design system is the site’s design system.** Every page is rendered by
kpress with the same style tokens (`style-tokens.css`), reading faces, KaTeX setup,
components and print rules the explainer inlines, so a reader moving between pages sees
one publication. The overview and frontier pages use kpress’s own table component
(`.kpress-table`, with its wide-table scale, numeric-column alignment and in-table code
sizing) and its TOC rail for the long tutorial and synopsis pages.

**Additions are layered on the system, not beside it.** What the pages need and kpress
does not yet have lives in one small stylesheet, `packing/devtools/templates/site.css`,
written only in kpress tokens (`--kpress-*` colours, spacing and font variables), so it
follows the theme and the print rules:

- the site navigation bar;
- sortable column headers, a sticky header row, and filter controls above a table;
- expandable rows (`<details>` within a table row) for the full claim and records;
- a thumbnail cell for the frontier atlas;
- the stacked verification bar.

Each addition is written so it could move upstream into kpress unchanged; moving it is a
follow-up in the kpress repository, not part of this plan.

**The explainer’s bytes and its PDF are protected.** The navigation bar sits outside the
article column and is `display: none` in print, and `site.css` is scoped so it never
matches the explainer’s article or math selectors.
`--check` and the existing typography, geometry and print-layout jobs, not hashes,
confirm that nothing in the explainer moved.

One navigation partial, `packing/devtools/templates/site-nav.html`, is included by the
overview, frontier, tutorial, synopsis and explainer pages.
The workbench is a full-viewport app and gets no bar: its `#site-note` element stays,
since the layout checks measure its clearance, and only its link changes from “the
explainer” at `../` to the overview.
`WORKBENCH_HOME` in `check_published_site`, the `check_published_site/startup.js` probe,
and `test_explainer.py`’s pin on the link’s target and text change with it.

### Components

- `packing/devtools/render_overview.py`: overview, frontier atlas, tutorial and synopsis
  pages; `RENDER_INPUTS`; `--update`, `--check` and `--output` options.
- `packing/devtools/templates/overview-article.md`, `frontier-article.md`,
  `site-nav.html`, `site.css`.
- `packing/devtools/overview/*.js`: table sorting and filtering and the fragment
  forwarder, with `node:test` tests.
- `tsconfig.overview.json` at the repository root, extending `tsconfig.base.json` with
  no relaxed flags, and `tsc -p tsconfig.overview.json` added to `package.json`’s
  `typecheck` script. Biome and ESLint discover the files already.
- Data passed to a script (the explainer’s anchor list, table metadata) goes into the
  page as a JSON data island through a placeholder, which the `.js` file reads; no
  script text is written from Python.
  A test mirrors `test_the_explainer_shell_owns_no_inline_programs` for the new
  templates.
- `render_results.py` and `significance.py`: the shared functions made public, as listed
  under [Approach](#approach).
- `render_explainer.py`: includes the nav partial (hidden in print, so the PDF’s 22
  pages and the print-layout checks do not move) and the new canonical URL; see
  [URL Layout](#url-layout) for why its output file does not change.
- `packages/workbench/tools/workbench_tools/build_site.py`: the `#site-note` link target
  and text, and its docstring.
- `.github/workflows/pages.yml` and its tests, in one change:
  - an `overview` job that runs beside `prepare` rather than after it (the pull-request
    wall is 176 s against a 180 s budget), with an `overview-unchanged` job for when its
    inputs did not move;
  - `scope` outputs `overview` and `overview_reason`; `pages_scope.BUILDER_INPUTS` gains
    the half, whose `_HALF_GATE` refuses unknown halves;
  - `pages-required` needs both new jobs, and its jq decision array reads the new
    output;
  - `publish` downloads the overview artifact and renames the explainer;
  - the `push.paths` deploy filter gains the overview’s `RENDER_INPUTS` (`SYNOPSIS.md`,
    `TUTORIAL.md`, `README.md`, `frontier/`, `epistemics.md`, the templates), or a merge
    that changes them would not republish, with a filter-coverage test like
    `test_the_pages_filter_covers_every_render_input`;
  - the sparse checkout gains what the renderer reads (`frontier/`,
    `resources/bibliography.yaml`, `atlas/known-best/*.json`, `epistemics.md`,
    `TUTORIAL.md`, `SYNOPSIS.md`); it still omits most of `packing/resources/` and all
    history and tags, so the renderer tests a link target’s existence with
    `git cat-file -e <commit>:<path>`, never the filesystem, and never reads `git log`
    or `git tag`;
  - `gate-budgets.yaml` gains a budget for each new job, which the budget test requires
    to cite a measured run, so the first pull-request run of the job is the measurement
    and the entry follows it;
  - `test_pages_workflow.py` pins that change the scope outputs, the `pages-required`
    needs and decision array, and `publish`’s needs and downloads.
- `packing/devtools/check_published_site.py`: `SERVED` gains the new pages, each checked
  for its stamp and canonical URL; `WORKBENCH_HOME` follows the workbench’s new link;
  its live per-link HTTP check covers the overview and frontier pages, while the
  tutorial and synopsis links are proved at build time.
- `packing/devtools/preview_site.py`: builds every page into one directory, serves it,
  and takes screenshots; its page probes live in
  `packing/devtools/probes/preview_site/`, registered in `probe-typecheck.json`.
- `README.md`: links updated.

### Data Changes

Two fields are added to `results.schema.yaml`, in one data commit followed by the
`DATA_REVISION` re-pin and atlas re-stamp that `tests/test_release.py` requires:

- **`registered: YYYY-MM-DD`** (required).
  The record has no registration date: `significance.scored` is when a result was last
  assessed (19 entries carry the 2026-09-29 re-scoring date), and the Pages build cannot
  read git history. The backfill takes each entry’s date from the commit that added it,
  once, by a script whose output is reviewed.
  “What changed recently” assigns each result to the first `PUBLICATION_HISTORY` edition
  dated on or after its registration, and links a release only where a tag exists
  (`v0.4.1`, `v0.4.2`).
- **`headline`** (optional, under about 90 characters).
  `significance.headline()`, the claim’s first sentence, runs from 10 to 816 characters
  with a median near 250, which is too long for a table cell.
  The table shows `headline` where it is set and falls back to the first sentence; the
  backfill writes one for every entry, for review.

`check_results` gains the two field checks.
The verification statistics count the **declared** `verification` and `confirmation`
rungs, split by whether an entry has `attribution`, never re-derived ones:
`check_results` accepts a declared rung below the derived one when a `composition` note
explains it, so a re-derivation would disagree with the record.
The overview build runs after the `check_results` gate.

### API Changes

None to `sqpack`. The command-line surface gains `python -m devtools.render_overview`
and `python -m devtools.preview_site`.

## Implementation Plan

### Phase 1: The Overview and Its Data

- [ ] `render_overview.py` skeleton: inputs, `RENDER_INPUTS`, shell, deterministic
  `--check`
- [ ] Register fields `registered` and `headline`: schema, backfill script,
  `check_results` checks, `DATA_REVISION` re-pin
- [ ] Shared `grouped_results()` and the public `significance` helpers
- [ ] Data layer: read the register, case files, atlas citations and release stamp into
  one typed model; derive the statistics and the recent-changes list
- [ ] Overview article template and the problem, headline, atlas and read-further
  sections
- [ ] The results table (static HTML, expandable rows, permalinks)
- [ ] The frontier atlas page from the `SquarePackingCase/v2` records, with clean value
  rendering, thumbnails and its tests
- [ ] Verification-at-a-glance counts and the inline SVG bar
- [ ] Table sorting and filtering script under the browser floor
- [ ] Tests: every register entry is a row; every record link resolves at the build
  commit; statistics equal the register’s own counts; byte-identical double render

### Phase 2: Navigation, Pages and Preview

- [ ] Shared nav partial and stylesheet, included by the overview, explainer and
  workbench
- [ ] Explainer moved to `explainer.html`, anchor list emitted, fragment forwarder on
  the overview
- [ ] Tutorial and synopsis pages with link rewriting and a table of contents
- [ ] `preview_site.py`: build every page into one directory and serve it
- [ ] `pages.yml`, `pages_scope`, the filter-coverage test and `check_published_site`
  updated; `README.md` links updated
- [ ] Local preview with desktop and phone screenshots of each page, for the owner’s
  review

### Phase 3: Math Everywhere

The repository’s Markdown writes most mathematics as code spans:
`` `s(11) ≥ 3.8269975…` ``, `` `31/8` ``, `` `2 + (1/2)√2` ``. The toolchain already
supports LaTeX math: GitHub renders `$…$` and `$$…$$`, `kpress` renders it with KaTeX on
the site, and the pinned flowmark keeps math spans whole (`devtools.check_math_spans`
measures that). This phase moves the prose to LaTeX math so it renders as mathematics
everywhere it is read.

Measured at the baseline: 86 math-like code spans in `README.md`, 145 in `SYNOPSIS.md`,
28 in `TUTORIAL.md`, and about 1,500 tracked Markdown files outside the archive.

**What converts and what does not.** A code span converts when its content is a
mathematical expression: a bound or equation in `s(n)`, a number or fraction standing as
a value, a formula (`2 + 4/√5`, `k² − 4`), or a variable (`n`, `k`). It stays code when
it is an identifier or literal text: result and evidence ids (`T-018`, `E-…`), rung
labels (`V4`, `C3`, `S5`), file paths, commands, field names, commit hashes, version
tags, and anything inside a fenced block.
Conversion is to idiomatic LaTeX: `s(11) \ge \frac{31}{8}` or `31/8` as the context
reads best, `\sqrt{2}`, `k^2 - 4`, `\ldots` for elided digits.

**A tool, not hand edits** (`OR-1`). `packing/devtools/migrate_math.py`:

- classifies every code span in a file as math, identifier, or uncertain, with the rule
  that matched, and prints a report;
- rewrites the math spans to LaTeX with `--apply`, leaving uncertain spans untouched and
  listed for review;
- runs the `check_math_spans` measurement on the result, so a conversion the formatter
  would split or retype fails before commit.

A ratchet check, `devtools.check_math_markup`, runs on the pull-request surface: in a
file marked migrated it fails on a new math-like code span, and it reports the count of
unmigrated files so the backlog is visible.
It never touches a file that is not yet migrated.

**Generated documents.** Generated Markdown is migrated at its renderer, never by
editing the output: `render_results` (`RESULTS.md`), `render_research_tables`
(`STATUS.md`), `render_results_headline`, the claim-document renderers, and the overview
and frontier pages. The data stays ASCII (`results.yaml` claims such as
`s(11) >= 381/100` do not change), and the renderers format it as math, so no data file
moves and `DATA_REVISION` is unaffected.

**Order.** One commit per group, each run through the tool and the gate:

1. The site’s reader documents: `README.md`, `TUTORIAL.md`, `SYNOPSIS.md`,
   `conventions.md`, `epistemics.md`.
2. The renderers of generated documents, and their regenerated outputs.
3. `docs/project/` (specs, research, reviews, handoffs), except quoted source text and
   the dated reviews `.flowmarkignore` protects.
4. The Markdown under `packing/` outside `resources/`: case files’ bodies, case
   directories, the atlas and frontier READMEs.

**Rendering everywhere.** The site pages render math through `kpress`, like the
explainer; the renderers of the tutorial and synopsis pages get a test that no `$`
reaches the page unrendered.
The workbench and any other HTML that shows register text use the same KaTeX path.

- [ ] `migrate_math.py` with classification report, `--apply`, and span-safety check,
  and tests over a fixture of math and identifier spans
- [ ] `check_math_markup` ratchet on the pull-request surface
- [ ] Group 1: the reader documents
- [ ] Group 2: renderers of generated documents, outputs regenerated
- [ ] Group 3: `docs/project/`
- [ ] Group 4: Markdown under `packing/` outside the archive
- [ ] Rendered-math tests on the site pages; preview screenshots of math-heavy sections

## Testing Strategy

- **Unit and render tests** under `packing/tests/test_overview.py`: row-per-entry
  completeness, link resolution at the build commit, statistics against `check_results`’
  derivation, determinism, self-containment (`assert_self_contained`), and no unresolved
  relative links in the tutorial and synopsis pages.
- **Filter coverage:** a test like `test_the_pages_filter_covers_every_render_input` for
  the overview’s `RENDER_INPUTS`.
- **Browser floor:** Biome, `tsc` and `node:test` for the new scripts; no JavaScript in
  Python strings, with any page probe in a `probes/` file.
- **Browser checks:** a Playwright pass (launched with `SQPACK_CHROMIUM`, since the
  pinned Playwright expects a different Chromium build than the container provides) over
  the local preview at desktop and phone widths that fails on horizontal overflow,
  broken internal links and console errors, and saves screenshots.
- **Gates:** `packing-validate --edit` while working, `--push` before each push, and
  `--fast`, which is what the pull request runs.

## Rollout Plan

1. Implement on a new branch, with beads linked to this spec.
2. Build the whole site locally with `preview_site.py` and share screenshots of every
   page with the owner.
   Nothing is deployed.
3. With the owner’s approval, open a pull request.
   The branch push alone runs no Pages workflow; the pull request runs every check
   without deploying, and its first run measures the new job for its budget entry.
4. Merge only with the owner’s approval.
   Deployment happens on the merge to `main`, and `verify-deployment` checks the live
   site.

## Open Questions

- **URL layout.** The plan puts the overview at `/` and moves the explainer to
  `/explainer.html` with fragment forwarding.
  The alternative is to leave the explainer at `/` and put the overview at `/overview/`,
  which keeps every existing link exact but does not give the site a front door.
  Recommended: the plan as written.
- **Math style for fractions.** Inline `31/8` can become `\frac{31}{8}` or stay `31/8`
  in math italics. Recommended: keep the slash inline in running text and use `\frac` in
  display math and tables, which reads better at small sizes.
- **Synopsis weight.** `SYNOPSIS.md` renders to a long page.
  Keep it as one page with a table of contents, or split it at its top-level headings?
  Recommended: one page.
- **Recent changes.** The plan generates the list from registration dates and release
  tags. If the owner wants pull requests named explicitly, the list needs a small
  hand-kept `site/news.yaml`, since the page cannot fetch from GitHub at render time.

## Technical Review

Three read-only reviews of the first draft, on 2026-09-29, each checked against the code
at the baseline: the Pages build and published-site checks, the data layer and results
table, and rendering and the browser floor.
Their findings are folded into the sections above; the ones that changed the design:

- the explainer is renamed at publish, not at render, because about forty workflow steps
  and several tests pin `site/index.html`;
- deep-link forwarding keys on “not an id on the overview” rather than an anchor list,
  because the explainer keeps certificate state and footnotes in the fragment;
- the workbench keeps its `#site-note` rather than gaining a nav bar;
- the register gains `registered` and `headline`, because it has no registration date
  and its first sentences are too long for a table;
- statistics count declared rungs, and grouping, ordering and case formatting reuse the
  register’s and survey’s own functions;
- the tutorial and synopsis skip the explainer’s math-geometry pass, rewrite links in
  the parsed HTML, and check their 1,100-odd link targets offline;
- the new Pages half is wired through scope, `pages-required`, `publish`, the deploy
  filter, the sparse checkout and the job budgets in one change.

## References

- `packing/devtools/render_explainer.py` and `packing/devtools/templates/`
- `packages/workbench/tools/workbench_tools/build_site.py`
- `.github/workflows/pages.yml` and `packing/devtools/pages_scope.py`
- `packing/devtools/check_published_site.py`
- `packing/frontier/results.yaml`, `RESULTS.md` and `STATUS.md`
- [`epistemics.md`](../../../../epistemics.md)
- [Others’ results in the results register](plan-2026-09-29-third-party-results-register.md)
- [development.md → Validation Loops](../../../../development.md#validation-tiers)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
