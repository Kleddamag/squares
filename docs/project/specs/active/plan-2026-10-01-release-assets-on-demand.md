# Plan: Release Assets on Demand, and One Rule per Date

**Date:** 2026-10-01

**Author:** Claude (agent), for the repository owner

**Status:** Implemented on `claude/release-assets-on-demand`, provisional where
[the owner has a choice](#decisions-for-the-owner).
The version bump to v0.5.0 is not part of it (`think-pt1k`).

**Workflow:** W7 pipeline improvement, with a W5 measurement in front of it

**Beads:** `think-4kyd` (large assets on demand), `think-tjpn` (dates)

## Summary

Until this change, every commit that touched the data was followed by a second commit
that set `DATA_REVISION` in `packing/src/sqpack/release.py` and ran
`build_known_best_atlas --update`, because the atlas posters drew the stamp
`v0.4.2-<six hex>` and the stamp had to equal the pin.
That rewrote eight tracked files (two SVGs, four PNGs, two PDFs) for a change of six
characters.

Measured on 2026-10-01:

- All 30 of the last 30 re-pin commits on `main` changed nothing in either drawing but
  the stamp. Each added 13.6 MB of blobs, 5.9 MB compressed, and they came 8 to 15 a day.
- The rebuild took 415 s on this machine at a load average near 35, and 95% of it was
  re-deriving 324 witnesses that the stamp does not depend on.
- The two posters conflicted in every merge between open branches.

The owner’s rule is that large assets are regenerated at an official version bump and on
demand, and do not pile up in git.
The contract below follows it: **a poster states the data it was drawn from and is never
re-stamped.** A data commit is followed by a one-line re-pin that takes about a second
and touches no binary.
A poster is redrawn by `build_known_best_atlas --update-composites`, at a version bump
or when someone wants it, in 42 s of CPU.

The dates get one rule each.
What the owner saw on 1 October, a PDF that says September 29, is the review paper’s
“Original proof September 29, 2026”: no other dateline in any generated artifact says
the 29th. That date is right.
The date beside it, “This review revised September 30, 2026”, was stale by a day, and
five other dates were stale or read from the build clock.
[The table](#one-rule-per-date) lists every date and what was fixed.

## What Was Measured

Every number here comes from `python -m devtools.measure_release_assets`, run from
`packing/`: `--timings` for the builds and `--history` for git.

### Where the Time Goes

Ten CPUs, load average 19 to 38 while measuring, so each wall time is beside the CPU
time its process was charged.

| Build | Wall | CPU |
| --- | ---: | ---: |
| Atlas: 324 witnesses and both composite SVGs rebuilt (the first half of `--update`) | 397.1 s | 950.5 s |
| Atlas: four PNG exports | 10.8 s | 9.8 s |
| Atlas: two PDF exports | 7.2 s | 6.7 s |
| Atlas: `--check --sample`, the pull request’s stand-in | 76.6 s | 138.5 s |
| Explainer page (`render_explainer --prepare-math`) | 18.2 s | 17.8 s |
| Explainer PDF (`render_explainer_pdf --update`) | 9.7 s | 10.6 s |
| Optimality paper, page and Markdown | 5.3 s | 4.1 s |
| Optimality paper, page and PDF | 9.2 s | 6.5 s |
| `preview_site`: explainer | 19.7 s | 16.5 s |
| `preview_site`: site pages and result overviews | 45.5 s | 20.7 s |
| `preview_site`: workbench | 70.7 s | 29.4 s |
| `preview_site`: optimality paper with its PDF | 13.0 s | 6.6 s |
| `preview_site`, end to end (the four above) | 148.9 s | 73.3 s |

The papers’ PDFs cost 4 to 10 s each, and they are built at deploy, never committed.
They are not the problem.
The cost is the atlas rebuild, which re-derives every witness’s feasibility receipt in
order to draw two figures whose inputs had not changed.
Both composites drawn from the *retained* witnesses are byte-identical to the retained
SVGs and take 25 s of CPU, which is what `--update-composites` now does.
With the six exports the whole redraw is 42 s of CPU; it took 2 min 47 s of wall time
here at a load average of 42.

`--restamp-only` existed to skip the rebuild.
Its guard proved the geometry unchanged by comparing git trees, with one frontier case
exempted by name, and it refused whenever a card’s source had moved.
It is removed: nothing re-stamps a poster any more.

### What Git Pays

| Measure | Value |
| --- | ---: |
| Re-pin commits on `main` | 43, of which 36 in the three days 29 September to 1 October |
| Blob bytes added by each of the last 30 | 13.6 to 13.8 MB, all but 13 KB of it the eight composite files |
| Compressed, as git stores a loose object | 5.9 MB each |
| The last 30 together | 410.5 MB of blobs; 74.1 MB as stored today |
| Of those 30, drawings changed anywhere but the stamp | 0 |
| Commits that redrew a card, 5 to 30 September | 31, about one a day |
| The repository | 813.7 MB packed, 178.0 MB loose |

A pack stores a re-stamped SVG as a small delta, so the cost is uneven: 36 KB for some
commits and 4.9 MB for others, where a PNG did not delta.

### Who Reads the Stamp

| Consumer | Reads | Needs the stamp inside a binary? |
| --- | --- | --- |
| Site footer and explainer credits | `PUBLICATION_EDITION` | No. It is text on the page |
| `check_published_site` | `PUBLICATION_EDITION` in each served page | No |
| Workbench stage, and so every film frame | `PUBLICATION_EDITION` when the frame is captured | Yes, and it is frozen at capture: a film is a release asset |
| Explainer PDF | The page’s credits, and a receipt of the HTML it was printed from | No. It is built at deploy from the page |
| Atlas posters | The stamp in the footer, and through the SVG’s digest every PNG and PDF | Only so that a poster that travels alone names its data |
| `test_release`, `test_explainer`, `test_known_best_atlas`, the workbench’s `test_citations` | The pin against git; the stamp against the pin | No |

Only the films and the posters carry the stamp where a rebuild is expensive.
The films already work the way this plan makes the posters work: stamped when cut,
published with a release, never re-stamped.

### Why Nothing Reads Git at Render Time

All 14 checkouts in `.github/workflows/pages.yml` are sparse and blobless at depth 1,
except `scope` at depth 2. In a shallow clone git reports the cut as the last commit to
change every path, so a stamp derived there would name the wrong commit;
`release.data_revision` refuses the cut for that reason.
The second reason was the posters: a committed file that is compared byte for byte
cannot contain a hash read at build time.
This plan removes the second reason and leaves the first.

## The Options

| Option | A data commit costs | What it gives up |
| --- | --- | --- |
| **(a)** The stamp leaves the per-commit path; posters are redrawn at a bump or on demand | One line of `release.py`; no binary | A poster can trail the data between bumps |
| **(b)** Posters leave git, built in CI and attached to releases | The same | `packing/atlas/README.md` and the figure playbook show the posters from the tree; the explainer build, the overview and the atlas tests read the retained SVG; an offline clone has no figure. Each needs a new source |
| **(c)** Posters stay stamped with the pin, but the test is relaxed between bumps | The same | The stamp on a poster names data it was not drawn from |
| **Derive the data revision in CI** and drop the pin | Nothing | One Pages job fetches full history and passes the hash to every render job; `PUBLICATION_EDITION` becomes a function of the environment in the eight files that read it, two of them changed by pull requests now open |

**Recommended, and implemented: (a), in a form that keeps the hash in the poster.** The
poster keeps its stamp, `v0.4.2-afd831`, as a statement of what it was drawn from, and
the test that held it to the current pin now holds it to the poster’s own record.
A poster printed alone can still be traced to its data, which a bare `v0.4.2` could not
do.

**(b)** is the right next step only if history size still matters afterwards.
With (a) the posters change at bumps and on demand: four bumps in September would have
been about 24 MB compressed, against 74 MB in three days.

**(c)** saves the same time and makes the stamp false.

**Deriving the revision** removes the last chore, the one-line re-pin and the one-line
merge conflict between branches that both re-pinned.
It is recommended as a follow-up once `#276` and `#277` have landed, since it changes
the Pages workflow and every stamp consumer at once.

## The Contract

`packing/src/sqpack/release.py` states it in its docstring.
In short:

1. **Every page prints `PUBLICATION_EDITION`**, the version and six characters of the
   pinned `DATA_REVISION`. Nothing reads git to render.
2. **The pin is what git says**: `tests/test_release.py` fails when `DATA_REVISION` is
   not the last commit that changed `DATA_PATHS`.
3. **A data commit is followed by a re-pin, and a re-pin is one line.**
   `python -m devtools.release_pin --update` writes it.
   No artifact is rebuilt.
4. **A drawn release asset states what it was drawn from and is never re-stamped.** Each
   composite SVG records its data revision and that commit’s date in its metadata, and
   prints them in its footer and its dateline.
   Its PNGs and PDF are bound to it by the digest receipts they already carried.
5. **A poster may trail the data until the next version bump.** While its revision is
   the pin, every label on it must agree with the figure record, as before.
   Once the pin has moved, the cards that differ are listed by every check and fail
   none. `COMPOSITES_MAY_TRAIL` in `release.py` is the switch; set to `False`, a trailing
   card fails.
6. **A version bump redraws them.** A poster whose stamp does not carry
   `PUBLICATION_VERSION` fails `build_known_best_atlas --check-composites` and the
   pull-request surface.
7. **The stamped files are not data** (`DATA_EXCLUDED`), as before, so redrawing a
   poster does not move the pin.

What each check holds, and what it costs:

| Check | Where it runs | Holds |
| --- | --- | --- |
| `tests/test_release.py` | Behavioral shards, every pull request | The pin against git; the stamp’s shape; that no data file carries the stamp |
| `build_known_best_atlas --check-composites` | Its findings are part of `known-best atlas records and sample`, every pull request; alone on demand, in about five seconds | Each poster’s record names a data commit and its date; stamp, dateline and canvas agree with it; the version is current; labels agree with the figure record, or trail and are listed; PNG and PDF receipts |
| `build_known_best_atlas --check` | Deferred surface | All 324 cases byte for byte; each poster redrawn under its own record and compared, exactly when it claims the pin, and listed card by card when it trails |

## What a Data Commit Costs

|  | Before | After |
| --- | --- | --- |
| Commands | Edit `DATA_REVISION`; `build_known_best_atlas --update` | `python -m devtools.release_pin --update` |
| Wall time | 415 s here; 10 to 18 minutes per branch on 1 October | 1.6 s |
| Files in the commit | `release.py` and eight composite files | `release.py` |
| Bytes in git | 13.6 MB of blobs, 5.9 MB compressed | About 200 bytes |
| Merge between two branches that both did it | Nine conflicts, eight binary | One line |

## What a Version Bump Consists Of

One command prepares it and prints the rest.
From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.5.0 \
    --scope "One sentence on what the edition adds."
```

It refuses a dirty tree or a stale pin, then:

1. Adds the edition to the front of `PUBLICATION_HISTORY` with the date given by
   `--date` (today in UTC by default), and sets `PUBLICATION_REVISION` to `HEAD`.
2. Redraws both posters and their six exports (`--update-composites`).
3. Regenerates the claim documents (`render_verifiable_claim`).
4. Runs `--check-composites` and the release, explainer and claim tests.
5. Prints what is left, none of which it does: commit and merge; wait for the deploy and
   run `check_published_site`; tag `v0.5.0`; create the GitHub release with the poster
   PDFs and PNGs attached.

The papers’ PDFs need no step: Pages builds them from the merge.
The films stay on the release that carries them (`render_overview.FILM_RELEASE`) until
they are cut again, which is its own
[runbook](../../../../packages/workbench/README.md#regenerating-and-publishing-the-ascent-videos).

## One Rule per Date

`python -m devtools.artifact_dates` prints this table from the tree, and
`tests/test_artifact_dates.py` holds each rule.

| Artifact | Showed on `main` | Source | Rule | Fixed |
| --- | --- | --- | --- | --- |
| Poster dateline, “Including new results (…)”, in SVG, PNG and PDF | September 28, 2026 | `PUBLICATION_DATE`, the day v0.4.2 was first published | The date of the data commit the poster was drawn from | Yes. The drawings took in results on 29 and 30 September under the old date |
| Poster PDF `CreationDate` | The build clock, to the second | cairo | Noon UTC of the poster’s data date, and `ModDate` with it | Yes |
| Poster PNG | No date |  |  |  |
| Explainer, “First published” | September 5, 2026 | Oldest entry of `PUBLICATION_HISTORY` | The first Pages deployment, in UTC | Right |
| Explainer, “Last revised” | September 28, 2026 | `PUBLICATION_DATE` | The date of the last commit that changed the article | Yes: September 30, 2026 |
| Explainer version history | One date per edition | `PUBLICATION_HISTORY`, with the deployment behind each | First publication, in UTC | Right |
| Explainer PDF `CreationDate` and `ModDate` | The build clock | Chromium | Noon UTC of “Last revised” | Yes |
| Optimality paper, “Original proof” | September 29, 2026 | Typed in the article | The date the register gives T-060 | Right, and now held to the register |
| Optimality paper, “This review revised” | September 30, 2026 | Typed in the article | The date of the last commit that changed the article | Yes: October 1, 2026 |
| Optimality paper PDF `CreationDate` and `ModDate` | The build clock | Chromium | Noon UTC of “This review revised” | Yes |
| Films, “as it stood 28 September”, and their release | v0.4.2 | `PUBLICATION_HISTORY` at `FILM_RELEASE` | The release the films were cut for | Right |
| `RESULTS.md`, “Register reviewed” | 2026-10-01 | `last_reviewed` in `results.yaml` | Typed by the reviewer; `check_results` refuses an entry dated after it | Right |
| `STATUS.md`, the `reviewed` column | One date per case | Each case record | Typed by the reviewer | Not examined case by case |
| `INVENTORY.md` | No date |  |  |  |
| `SYNOPSIS.md`, “Date” | 2026-10-01 | Typed | `check_synopsis` holds its shape; it matched the file’s last change | Right |
| `defects.md` | One date per defect | `defects.yaml` | When the defect was recorded | Right |
| Page footers and the link-preview card | No date |  |  |  |

A date that is derived from a commit is that commit’s author date, on the author’s own
calendar. A paper’s date is read over the commits that changed its article, merges
excluded. A PDF’s dates are given at noon UTC because a reader shows the instant in its
own timezone, and midnight UTC is the evening before in California.

## Decisions for the Owner

1. **May a poster trail the data between bumps?** Implemented: yes, with the trailing
   cards listed by every check.
   That is the rule as stated, and its cost is that the overview and the explainer can
   show a poster whose bound for some case is older than the table beside it.
   The poster says so itself: its dateline and stamp name its data.
   The alternative is `COMPOSITES_MAY_TRAIL = False`: a poster is redrawn whenever a
   card changes, about once a day in September at 13.6 MB each.
   Recommended: yes.
2. **What does a poster’s stamp say?** Implemented: the version and the data revision it
   was drawn from. The alternative is the version alone.
   Recommended: keep the revision.
3. **What is a poster’s dateline?** Implemented: the date of its data.
   The alternative is the release’s first-published date, which is only right for a
   poster drawn on the day of a release.
   Recommended: the data’s date.
4. **What does the explainer’s “Last revised” mean?** Implemented: the last change to
   its article. The alternative is to keep the edition’s date under another label, such
   as “This edition”. Recommended: the last change.
5. **Derive the data revision in CI and drop the pin?** Not implemented.
   Recommended after the open branches land.
6. **Move the posters out of git?** Not implemented.
   Recommended only if history size still matters after the above.

## Follow-Ups

- `#276` gives every page `article:modified_time` from `PUBLICATION_DATE`, and reads the
  optimality paper’s revised date with a pattern of its own.
  Once it lands, both should read `sqpack.release.EXPLAINER_REVISED` and
  `devtools.artifact_dates`.
- The composite PDFs still differ between two runs in their font-subset tags, which
  cairo assigns per process.
  The date no longer differs.

## References

- [`release.py`](../../../../packing/src/sqpack/release.py), the contract
- [Publishing the Explainer](../../../../development.md#publishing-the-explainer), the
  procedure
- [Plan: the GitHub Pages overview](plan-2026-09-29-github-pages-overview.md), whose
  epic carries both beads
- `OR-13`, `OR-14`, `OR-16` and `OR-17` in
  [the operating rules](../../../../operating-rules.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
