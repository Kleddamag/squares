---
title: A Top-Level Overview Page for the Published Site
description: A clean landing page on GitHub Pages that summarizes the project and every current result, with navigation to the explainer, tutorial, synopsis and workbench
author: Claude (agent), for the repository owner
---
# Feature: A Top-Level Overview Page for the Published Site

**Date:** 2026-09-29

**Author:** Claude (agent), for the repository owner

**Status:** Draft

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
- A results table with full details: identifier, `n`, bound, credit, `V`, `C` and `S`
  rungs, novelty, date, and links to the case record, the register entry, the evidence,
  the retained source copy and the review, where each exists.
- Verification statistics: how many results stand at each `V` and `C` rung, how many are
  this project’s and how many are others’, and how many of the hundred atlas cases are
  proved, open with a verified bracket, or carry a recent verified lower bound.
- A “what changed recently” section that summarizes the newest results and the releases
  they arrived in, generated from the register and the release record rather than
  written by hand.
- A local preview of the whole site (overview, explainer, tutorial, synopsis, workbench)
  with desktop and phone screenshots, reviewed by the owner before anything deploys.

## Non-Goals

- Deploying. Nothing in this plan pushes to `main` or runs the Pages deploy until the
  owner has seen the full overview in a local preview and approved it.
  Pull-request builds of `pages.yml` do not deploy, so a branch push is safe.
- Changing the explainer’s content, its PDF, or the workbench beyond the shared
  navigation bar and the move described under [URL Layout](#url-layout).
- Changing the register’s schema or any data under `DATA_PATHS`. The overview reads the
  record as it stands.
  (See [Open Questions](#open-questions) on a `headline` field.)
- Rewriting `README.md`, `TUTORIAL.md` or `SYNOPSIS.md`. They are rendered as they are;
  prose improvements are separate work.
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

The data the overview summarizes already exists and is already gated:

- `packing/frontier/results.yaml` (`ResultsRegister/v1`), 55 entries `T-001` to `T-055`,
  with `claim`, `scope`, `verification`, `confirmation`, `significance`, `novelty`,
  `evidence`, `artifacts`, `review_artifact` and, for results by others, `attribution`
  (added by PR #243). `devtools.check_results` derives the rungs;
  `devtools.render_results` renders `frontier/RESULTS.md`; `devtools.significance` ranks
  them.
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

A new renderer, `packing/devtools/render_overview.py`, in the same shape as
`render_explainer.py`: it reads declared inputs, fills an HTML shell and Markdown
article templates, renders the Markdown through the vendored `kpress`, writes
self-contained pages into `packing/site/`, and declares its inputs as `RENDER_INPUTS`.
It renders three pages: the overview and HTML editions of the tutorial and the synopsis.
The explainer and workbench builders gain only the shared navigation bar.

Each page is deterministic at a commit: `--check` renders twice and compares bytes, as
the explainer and workbench builds do.

### URL Layout

| Path | Page |
| --- | --- |
| `/` | the overview (new) |
| `/explainer.html` | the n = 11 explainer (moved from `/`) |
| `/tutorial.html` | `TUTORIAL.md`, rendered (new) |
| `/synopsis.html` | `SYNOPSIS.md`, rendered (new) |
| `/workbench/` | the workbench (unchanged) |
| `/t-018-explainer.{md,pdf}` and the composite assets | unchanged |

The explainer moves to `/explainer.html` rather than `/explainer/` so it stays beside
the composite assets and PDF it references with relative paths, and nothing it links to
moves. The overview carries a small script (in a `.js` file, under the browser floor)
that forwards a root URL whose fragment names an explainer anchor to
`/explainer.html#…`, so existing deep links into the explainer keep working.
The anchor list is written by the explainer renderer at build time, not maintained by
hand.

`README.md` links to `https://jlevy.github.io/squares/` as “the explainer page” in two
places; those links change to `/explainer.html` in the same change, and the README gains
a link to the overview.

### The Overview Page

Sections, top to bottom:

1. **Header and navigation bar.** The project name, the edition stamp
   (`PUBLICATION_EDITION`), and links to Overview, Explainer, Tutorial, Synopsis,
   Workbench and the GitHub repository.
   The current page is marked.
2. **The problem.** Two or three sentences defining `s(n)`, and the central bracket
   `31/8 < s(11) ≤ 3.8770835…` with its gap, read from `n-011.md`.
3. **Headline results.** Cards for the `S5` and `S4` results and the new exact values,
   each with its bound, its credit, its `V`/`C` rungs, and a link into the table.
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

One row per register entry, grouped as `RESULTS.md` groups them (this project’s results,
then others’ by lineage), each group ranked by `devtools.significance`.

| Column | Source |
| --- | --- |
| ID | `id` |
| `n` | `scope.n_values`, compressed to ranges |
| Result | the claim’s leading statement; the full `claim` in an expandable row |
| Credit | “This project”, or `attribution.source_keys` resolved to names |
| `V` / `C` / `S` | `verification`, `confirmation`, `significance.score`, with the rung definitions from `epistemics.md` as tooltips |
| Novelty | `novelty` |
| Date | `significance.scored`, or `attribution.published` for others |
| Records | links to the case file(s), the `RESULTS.md` entry, each `evidence` entry, `review_artifact`, and the retained source copy |

The expanded row adds `composition`, `next_rung`, `artifacts` and `controls`, each
linked. Every repository link is a permalink at the build commit, which
`check_published_site` already requires.

Behaviour: the table works with JavaScript off (all rows present, `<details>` for
expansion). A small script adds sorting by column and filters by source, `n` and `C`
rung. It lives in `packing/devtools/overview/table.js` with JSDoc types, its own
`tsconfig.overview.json`, and Biome and `tsc` coverage, the same arrangement as the
explainer’s scripts.

A second, compact table lists the case status for `n = 1…30`, from the same data as
`STATUS.md`: reported and verified bounds, status and gap, with a link to the full
survey for the rest.

### Tutorial and Synopsis Pages

`TUTORIAL.md` (about 1,600 lines) and `SYNOPSIS.md` (about 6,900 lines) are rendered
with `kpress` into the shared shell.
Links are rewritten at render time:

- a link to another rendered document (`README.md#…`, `SYNOPSIS.md#…`, `TUTORIAL.md#…`)
  becomes the site page (`README.md` maps to the overview, with a fallback to the
  repository for README-only anchors);
- any other relative link becomes a permalink at the build commit;
- images under the repository become permalinks to the raw file, or are copied beside
  the page if they are already among the served assets.

Each rendered page has a table of contents from its headings.
The synopsis’s generated blocks and math spans are rendered as they are; a render test
fails on an unresolved relative link.

### Shared Navigation and Style

One navigation partial and one stylesheet, `packing/devtools/templates/site-nav.html`
and `site.css`, inlined into every page so each stays self-contained.
The explainer shell and the workbench template include the same partial; the workbench’s
`../` back link becomes the nav bar’s Overview link.
Typography follows the explainer’s existing fonts and palette, with light and dark
themes and a layout that works at phone width.

### Components

- `packing/devtools/render_overview.py`: overview, tutorial and synopsis pages;
  `RENDER_INPUTS`; `--update`, `--check` and `--output` options.
- `packing/devtools/templates/overview-shell.html`, `overview-article.md`,
  `site-nav.html`, `site.css`.
- `packing/devtools/overview/*.js`: the table behaviour and the fragment forwarder;
  `tsconfig.overview.json`.
- `render_explainer.py`: writes `explainer.html` instead of `index.html`, includes the
  nav partial, and emits its anchor list.
- `packages/workbench/tools/workbench_tools/build_site.py` and its template: the nav
  partial.
- `.github/workflows/pages.yml`: an `overview` job and artifact, merged by `publish`;
  the `push.paths` list extended; `pages_scope` taught the new half.
- `packing/devtools/check_published_site.py`: `SERVED` gains the new pages.
- `packing/devtools/preview_site.py`: builds every page into one directory and serves it
  locally (see [Testing Strategy](#testing-strategy)).
- `README.md`: links updated.

### API Changes

None to `sqpack`. The command-line surface gains `python -m devtools.render_overview`
and `python -m devtools.preview_site`.

## Implementation Plan

### Phase 1: The Overview and Its Data

- [ ] `render_overview.py` skeleton: inputs, `RENDER_INPUTS`, shell, deterministic
  `--check`
- [ ] Data layer: read the register, case files, atlas citations and release stamp into
  one typed model; derive the statistics and the recent-changes list
- [ ] Overview article template and the problem, headline, atlas and read-further
  sections
- [ ] The results table (static HTML, expandable rows, permalinks) and the compact case
  table
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

## Testing Strategy

- **Unit and render tests** under `packing/tests/test_overview.py`: row-per-entry
  completeness, link resolution at the build commit, statistics against `check_results`’
  derivation, determinism, self-containment (`assert_self_contained`), and no unresolved
  relative links in the tutorial and synopsis pages.
- **Filter coverage:** a test like `test_the_pages_filter_covers_every_render_input` for
  the overview’s `RENDER_INPUTS`.
- **Browser floor:** Biome, `tsc` and `node:test` for the new scripts; no JavaScript in
  Python strings, with any page probe in a `probes/` file.
- **Browser checks:** a Playwright pass over the local preview at desktop and phone
  widths that fails on horizontal overflow, broken internal links and console errors,
  and saves screenshots.
- **Gates:** `packing-validate --edit` while working, `--push` before each push, and
  `--fast`, which is what the pull request runs.

## Rollout Plan

1. Implement on a new branch, with beads linked to this spec.
2. Build the whole site locally with `preview_site.py` and share screenshots of every
   page with the owner.
3. Push the branch; the pull-request build of `pages.yml` runs every check and does not
   deploy.
4. Open a pull request and merge only with the owner’s approval.
   Deployment happens on the merge to `main`, and `verify-deployment` checks the live
   site.

## Open Questions

- **URL layout.** The plan puts the overview at `/` and moves the explainer to
  `/explainer.html` with fragment forwarding.
  The alternative is to leave the explainer at `/` and put the overview at `/overview/`,
  which keeps every existing link exact but does not give the site a front door.
  Recommended: the plan as written.
- **Result summaries.** Register claims are long and do not have a short form.
  The plan shows the claim’s leading statement and puts the full claim in the expanded
  row. An optional `headline` field in `results.yaml` would give cleaner summaries, at
  the cost of a data change and a `DATA_REVISION` re-pin.
  Recommended: start without it and add it if the extracted statements read poorly in
  the preview.
- **Synopsis weight.** `SYNOPSIS.md` renders to a long page.
  Keep it as one page with a table of contents, or split it at its top-level headings?
  Recommended: one page.
- **Recent changes.** The plan generates the list from registration dates and release
  tags. If the owner wants pull requests named explicitly, the list needs a small
  hand-kept `site/news.yaml`, since the page cannot fetch from GitHub at render time.

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
