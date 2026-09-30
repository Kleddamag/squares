<!--
The overview page's article, rendered by devtools.overview_page through kpress in trusted
mode. Inline placeholders in double braces are filled from the record before parsing, and
a placeholder standing alone in a paragraph is replaced by a generated block after it, so
no bound is ever written here as a literal. The seven `##` headings are the page's
sections, in the order overview_page.SECTIONS gives them their ids. The page has no `#`
title: its name is in the navigation bar and the document title. The components the
blocks are built from are described in site-design.md.
-->

{{HERO}}

## The Square Packing Problem

How small a square can hold $n$ unit squares?
Write $s(n)$ for the side of the smallest square that holds $n$ non-overlapping unit
squares, each free to rotate.
A packing that fits in a square of some side shows that $s(n)$ is at most that side; a
proof that no smaller square can hold them shows that $s(n)$ is at least a value.
A case is settled when the two meet, and every bound on this page is one of the two.

## Recent Results

The results registered since {{RECENT_SINCE}}: {{RECENT_OURS}} by this project and
{{RECENT_OTHERS}} by others, listed as the project’s README lists them.
Each card gives the result’s rungs for verification ($V$), confirmation ($C$) and
significance ($S$), and whether it still holds a case’s bound.
A result its source reports and this repository has not yet replayed is marked
*reported*.

### By This Project

{{RECENT_OURS_CARDS}}

### By Others

Credit is printed whole, as the source gives it; this repository’s rungs never change a
credit.

{{RECENT_OTHERS_CARDS}}

## Verification at a Glance

Every result in the register is graded on three axes, whose rungs are defined in
[the project’s epistemics]({{EPISTEMICS_URL}}): how far its proof has been checked, what
this repository has itself replayed, and how much it moves the problem.
The counts are the rungs each entry declares, split between this project’s results and
others’.

{{VERIFICATION_CARDS}}

## The Atlas and Its Film

The atlas draws the best known packing of every case, each labeled with its best known
side and, where the case is open, its strongest verified lower bound.
Each preview opens the full atlas as a PDF. The film climbs through the same packings
one case at a time; it loads only when it is played.

{{ATLAS_MEDIA}}

## Results

Every entry in the results register, {{RESULT_COUNT}} in all, grouped as the register’s
own listing groups them.
Open a result for its full claim, how its rungs compose and what would raise them; the
records column links the case file, the register entry, the evidence and the reviews.
The [frontier atlas](frontier.html) gives the bounds case by case.

{{RESULTS_TABLE}}

## Read Further

The site’s other pages, then the project’s documents on GitHub.
A research report kept as a dated record describes the frontier as it stood on its date.

{{READ_FURTHER}}

## Other Square Packing Projects

The public websites, catalogues and repositories on square packing that this project
draws on, credited as their authors are credited in the project’s bibliography.

{{PROJECT_CARDS}}

{{DEFAULT_BRANCH_LINKS}}
