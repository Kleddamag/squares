# Evan Daniel’s Square Packing Atlas and Repository at `7ff3b211`, Pinned 2026-10-04

This packet retains the Square Packing Atlas, Evan Daniel’s site at
<https://evand.github.io/square-packing/>, with its open-problems page
<https://evand.github.io/square-packing/problems.html>, as the repository
[evand/square-packing](https://github.com/evand/square-packing) builds it at one commit.
It also retains the notes, certificates and Lean files with claims that the repository
added after the [October 3 packet](../evand-square-packing-2026-10-03/README.md)’s pin
`2eb15455`.
On 5 October an intake pass (bead `think-83zc`) added 44 files from the same clone and
commit. Earlier commits had changed them, no packet retained them, and they bear on
entries this record holds; [Added for Earlier Commits](#added-for-earlier-commits)
lists them.

The owner asked on 5 October 2026 for a review, a citation and an import of the site
and its pages. No issue was opened for the request; the bead `think-plrl` holds the
claim map. The claims are stated here as the source states them.
The frontier records decide what this record makes of them, and
[the review](../../../../docs/project/reviews/review-2026-10-05-evand-square-packing-atlas.md)
explains how each claim is mapped.

## Source and Pin

| Field | Value |
| --- | --- |
| Site | <https://evand.github.io/square-packing/>, deployed by `.github/workflows/pages.yml`: `site/www/` is the site root, and `s12/docs/` is served at `/s12/`, `/s13/`, `/s21/`, `/s32/`, `/s45/`, `/s60/` and `/k2m3/` |
| Repository | <https://github.com/evand/square-packing> |
| Revision | [`7ff3b2113532889708a3baa4d56bc44294022e63`](https://github.com/evand/square-packing/tree/7ff3b2113532889708a3baa4d56bc44294022e63), tree `479154fb`: “Open problems: plateau-optimality and alternative packings (§6); proofreading fixes” |
| Committed | 2026-10-04T20:17:38Z (14:17:38 −06:00), by Evan Daniel |
| Retrieved | 2026-10-05T00:34Z, a blobless clone; `main` was this commit when it was fetched and when it was read |
| Licence | MIT, `LICENSE` and `s12/LICENSE`. The root `README.md` says that `site/www/data/` is derived from David Ellsworth’s SVG catalogue, quotes his attribution text, and is not covered by the MIT licence |
| Request | The owner’s request of 5 October 2026; bead `think-plrl`, and `think-kqc3` for the homepage link |

**The deployed pages were not fetched.**
This session’s egress policy blocks `evand.github.io`.
The pages retained here are the files the Pages workflow copies from this commit.
The workflow runs on every push to `main` that touches `site/www/`, and this commit
does.

**Credit and AI assistance.** `s12/CREDITS.md` has not changed since the October 3
packet.
It credits the weighted covering method to Sam Burns and Gustavo Massaccesi, and says
the work “was produced by Claude (Anthropic) in a single session under human
direction”. The site’s Sources page credits the packings to David Ellsworth’s catalogue
and Erich Friedman’s survey, and says the parsing and the contact and rigidity
analysis are the site’s own.
`s12/tasks/s20-review/REPORT.md` describes its reviewer as “an independent agent”.

## What Is Retained

The manifest ([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256))
covers 115 files, 3,924,631 bytes.
113 are retained under [`square-packing/`](square-packing/), byte-identical after
decompression: the 69 of the table below and the 44 added on 5 October. Two are pinned
by digest only;
[`acquisition/sources.json`](acquisition/sources.json) gives the reason for each.

| Upstream path | What it is |
| --- | --- |
| `site/www/index.html`, `explore.html`, `compare.html`, `bounds.html`, `proofs.html`, `problems.html`, `sources.html`, `k2m4/index.html` | The site’s pages: the overview, the packing explorer, the comparison and morph view, the bounds page, proofs and results, open problems, sources, and the write-up of $s(k^2 - 4) = k$ |
| `site/www/css/`, `site/www/js/` | The stylesheet and the six scripts the pages run |
| `site/www/data/lower_bounds.json`, `timeline.json`, `bentz13.json`, `cert_56.txt`, `cert_81.txt` | The floors table for $n \le 100$, the dated record history parsed from Ellsworth’s catalogue, and the data of the proofs page’s two interactive figures |
| `site/README.md`, `site/notes/lower-bounds-notes.md` | The site’s own description and the sourcing notes for its floors table |
| `s12/docs/*.html` | The write-ups the site serves at `/s12/`, `/s13/`, `/s21/`, `/s32/`, `/s45/`, `/s60/` and `/k2m3/` |
| `s12/search/S20_LB.md`, `s20lb_cover_4886.txt`, `s12/tasks/s20-review/REPORT.md` | $s(20) > 3 + 4\sqrt{2}/3$: the note, the 12,864-point cover and the source’s review of it |
| `s12/verify2/Cargo.toml`, `Cargo.lock`, `src/bin/zmx2.rs`, `s12/search/ZMX2.md` | `zmx2` at blob `d42cbde2`, the version of commit `b8157df` that accepts a side not a multiple of $1/10$, which the $s(20)$ cover was checked with, and its notes |
| `s12/search/CEILINGS_17_20.md`, `ceil_nuf_*_exact_support.txt` | The exact fractional-packing ceilings at sides $4.660$, $4.823$, $4.8856$ and $4.886$ |
| `s12/lean/Sqpack/LebMass.lean`, `LebMass7.lean`, `LebMass7Data.lean`, `ValidSplit7.lean`, `SpecChelokot.lean`, `s12/lean/scripts/gen_lebmass_data.py`, `s12/notes/lean-leb-mass.md`, `s12/lean/LADDER.md`, `Axioms.lean`, `Sqpack.lean` | The Lean added since `2eb15455`: Lemmas U and K with the LEB and CAP leaves of the `ValidTilt7` run, the reduction of `Valid7` to `ValidTilt7`, and the bridge to chelokot’s definitions |
| `s12/search/WISHLIST.md`, `FRIEDMAN.md`, `record_structure.py`, `goebel_alt/`, `s12/notes/wishlist-literature-2026-10-03.md`, `conjectures-literature-2026-10-04.md` | The working list behind the open-problems page, the literature checks behind its “stated here” items, the script for its plateau-family table, and the exploratory $n = 149$ computation it cites |
| `s12/notes/jlevy-s17-techniques.md` | Daniel’s reading of this repository on 3 October, with what it says of his results and what it asks of this record |
| `README.md`, `LICENSE`, `.github/workflows/pages.yml`, `s12/README.md`, `s12/CREDITS.md`, `s12/LICENSE` | The repository’s statement of its results, its licence and credits, and the Pages build |

**Pinned by digest only.**
`site/data/lower_bounds.json` has the same bytes as `site/www/data/lower_bounds.json`,
and the manifest gives both the digest `1434d54f…`.
`site/www/data/index.json`, 675,174 bytes on one line, is the overview’s per-packing
analysis of Ellsworth’s catalogue.
`site/build.sh` regenerates it from the SVGs, and it states no bound.

**Not retained.**
The 547 packing files under `site/www/data/p/`, about 90 MB, are parsed from
Ellsworth’s SVGs and are pinned by the commit.
Also left out: the site’s build tools, its working notes and TODO lists, and the task
briefs and reports under `s12/tasks/` other than the $s(20)$ review and the reviews and
briefs added on 5 October.
The research scripts and data that no claim of the site rests on are left out too.

## Added for Earlier Commits

The intake sweep of 5 October listed 41 commits of 1 to 4 October, from `27dd68a` to
`40e442f`, that this pin contains and whose changed paths no packet retained.
Where such a commit changed a file that bears on an entry this record holds, the file
as it stands at this pin was added here, read from the same clone of 00:34Z; every file
retained before came out byte-identical.
The declaration’s scope gained 44 files.

| Upstream path | Changed by | Bears on |
| --- | --- | --- |
| `s12/certificates/k2m3/README.md` | `02629f2`, `a40e2bc`, `2eb1545`, `37f2d09`, `ca6d988` (3 October) | `T-064` |
| `s12/tasks/k2m3-review/README.md` and its six `REPORT.md` | `0f55a52` (3 October) | `T-064` |
| `s12/search/ZMX2_AREA.md`, ten records in `s12/search/zmx2_area/`, `zmx2_area_tests.sh`, `zmx2_tools.py` | `bfbdf04` (2 October) | `T-064` |
| `s12/tasks/k2m4-review/README.md` and its three `REPORT.md` | `0f55a52` | `T-081` |
| `s12/VERIFICATION.md`, `s12/certificates/s21/`, `s32/`, `s45/` and `s60/README.md` | `6383ad8` (1 October, local time) | `T-052`, `T-051`, `T-053`, `T-062` |
| `s12/tasks/s21-finish/`, seven files | `0f55a52` | `T-051`, `T-052`, `T-053`, `T-062` |
| `s12/lean/Sqpack/Attain.lean`, `Spec.lean`, `SpecBridge.lean`, `FCSquarePacking.lean`, `SpecFC.lean`, `SpecHeadline.lean`, `S13Lower.lean` | `f7b4430`, `87726c9`, `c2ae715` (1 October, local time) | `T-006`, and `T-086`’s note on `SpecChelokot.lean`, which imports them |

What they add, as the source states it; nothing here was run:

- **The $k^2 - 3$ bundle README** records wand125’s checker as an independent second
  implementation of `Valid7`. The source reran its record check in a sandbox, `RECORD
  OK` over all 156,800 roots with three mutant covers refused, and read its method,
  finding the measure-zero gap this record’s review calls D-1.
  The README says the D4 reduction and Lemma Z are kernel-checked, leaving `ValidTilt7`.
  It cites chelokot’s Lean `s6_eq_three` for $k = 3$, and it points at the six
  adversarial reviews of 29 September, which were private until `0f55a52`.
- **`zmx2` decides `Valid7`.** At `bfbdf04` the source’s `zmx2` with area density closed
  the 120 D4 boxes at the double germs it had left open (§11.4 of `ZMX2_AREA.md`).
  `cert --first-order` reports `VERIFIED-D4` over 4,900 roots and `VERIFIED` over all
  39,200 roots of the unreduced pose space, none uncertified, in 399 CPU-seconds.
  This is an interval-certified implementation by the source’s agent, written without
  opening `qx2_zm.py`. Its §13 is the same agent’s self-audit: four refinements of the
  newest lemmas survive its mutation tests, and a second reader should check them first.
  So the bundle README and the TODO list still call `zmx2` partial.
  The `_v2` records were made by `zmx2.rs` blob `08bea466`, the version at `bfbdf04`.
  The copy retained above is `d42cbde2`, from `b8157df`, which the source says leaves the
  roots and atoms of every integer side unchanged.
- **The $k^2 - 4$ reviews.** The three reports the `k2m4` bundle README summarises,
  kept in private notes when the 3 October packet was made, report no BREAKS.
  The claim report’s one GAP is the step from the run’s D4 region to `Valid9`, which
  `ValidSplit9.lean` in the 3 October packet kernel-checks.
- **The claims audit** of `6383ad8`, which the
  [2 October packet](../evand-square-packing-2026-10-02/README.md) read without
  retaining these files, is unchanged at this pin. It calls the bundles’ checkers
  separately written rather than independent, because they share `zeromargin.py`’s
  point-test formulation, and it notes, citing Karakuş, that the published proof of
  Nagamochi’s 2005 general result is incomplete.
- **The brief of `zmx2`**, `s12/tasks/s21-finish/xcheck.md` of 27 September, was not
  public when `T-051` was reviewed. It forbids `zm_mixed.py`, its tests, `ZM_MIXED.md`
  and its audits. It permits `zmcheck`, `zeromargin.py`, `RUNG2.md` and `ZEROMARGIN.md`
  for pose-space subdivision and point primitives, as the source said on
  [#238](https://github.com/jlevy/squares/issues/238).
- **The Lean.** `isLeast_minSide` proves that the infimum is attained for every
  $n \ge 1$. `Spec.lean` states the problem as `UnitSquarePacking.Packs`, and
  `SpecBridge.lean` and `SpecFC.lean` connect it to the source’s definitions and to
  formal-conjectures’ `SquarePacking`. `SpecHeadline.lean` restates $s(13) = 4$ in both
  forms (`s13`, `s13_fc`), and `S13Lower.lean` adds `s13_isLeast`. These files were not
  built here.

Each is an evidence update on the entry it bears on, and none moves a rung.
The rest of those commits is working material, left out by the rules above. That covers
the TODO and Completed lists, task briefs and the source’s session reviews, the research
notes and scripts (the SOS probe, the S2 insertable LPs, the seam capacity, the `qx2`
margin studies, the $s(20)$ cover’s generator tools), the literature and proof-anatomy
notes, and the reviewers’ scratch code and logs. Two Lean files are left out too:
`S3Lower.lean`’s `s3_eq_2`, a toy run of the mixed verifier on a classical value, and
`Average.lean`’s averaging lemma, which bounds nothing.
A read in [`intake-watch.yaml`](../../../campaign/intake-watch.yaml), through `40e442f`,
records them.

## Checks Here, 5 October 2026

- [`receipts/site_floors_compare.json`](receipts/site_floors_compare.json): the floors
  table compared with the case records by
  [`devtools.compare_site_floors`](../../../devtools/compare_site_floors.py), with the
  overview’s family rings `1:3,2:2,3:6` from `site/www/js/overview.js`.
  Of its 100 floors, 99 equal this record’s verified lower bound.
  Of those 99, 73 equal the reported one too, and 25 are below a reported bound this
  record has not replayed.
  The last is $n = 12$, where the reported lane holds squarepacker’s lower
  $31360/7901$ (`T-078`).
  The exception is $n = 96$, where the table takes $s(96) = 10$ from Daniel’s
  $k^2 - 4$ family, the reported lane of `T-081`, and does not mark it verified.
  All 20 floors the table marks `register: verified` are values the verified lane
  holds, and so are the 24 counts past $n = 100$ that the overview rings for
  $c = 1, 2, 3$.

Nothing in this packet was replayed.
The $s(20)$ cover, the ceilings and the Lean files are the source’s reports.

## Compressed Files

Three files of more than 1,000 lines are stored as deterministic `gzip -9n`. Each row
gives the Git blob and SHA-256 of the decompressed bytes, as `devtools.retained_data`
produces them.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing/s12/search/goebel_alt/partial_149.jsonl.gz` | upstream | `b393c630e53c7126302b6a1981d75341462552f8` | `fdfebc88169cb13eccc90f214a2af26f0ee6ca278728e2187a7a51884ed7d901` |
| `square-packing/s12/search/s20lb_cover_4886.txt.gz` | upstream | `515ab8cad8a6be874bcc103afad71874847dff1c` | `e0e25a0644fe8db1c2a346a1295eb8e966aedb2b36658d89d75813396338af97` |
| `square-packing/site/www/data/lower_bounds.json.gz` | upstream | `484dce3af6671d0a7cd2da543b0388e9ab139550` | `1434d54f37225b7e6982aaa543bcb8925328a9183c97cfd170ad923910c4d25f` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
