<div class="site-hero">

{{HERO}}

</div>

<!-- The explainer has a section of this name, and an old explainer link to it must
     still reach the explainer (forward.js), so this heading keeps the overview's own id. -->
<h2 id="the-problem" class="site-title">The Square Packing Problem</h2>

<!-- The section's first two paragraphs are README's, read from its project-intro block
     (site_documents.overview_intro), so the problem is introduced in one text. Edit them
     in README.md. Only the site's own statement is written here, under its own
     heading, The Squares Project. -->

{{README_INTRO}}

## The Squares Project

This Squares Project site collects all known historic research and current new results
on the square packing problem.
Work on this problem has exploded in the summer of 2026 thanks to AI-powered research
efforts.

We and several others have proved new results as part of this project for low values of
$n$, including $n = 11$, $n = 12$, $n = 17$ and many others.
As part of a collaborative open effort, several people have built on results from this
project or developed other new proofs, and this site
[independently checks and documents](#verification-ladders) the proofs and certificates
behind them.

If you have new results or know of newer results, please
[file an issue]({{NEW_ISSUE_URL}}) to report them, and we will gladly incorporate them
and cite your work.

{{PAGE_CARDS}}

## Recent Results

<!-- The section opens with README's next two paragraphs, what the project covers and
     its newest major result, read from its recent-progress block
     (site_documents.overview_progress). Edit them in README.md. -->

{{README_PROGRESS}}

The table lists every result, newest first: new bounds for particular numbers of
squares, found here or by others.
Each is dated by its publication if it is by others and by the day it was established if
it is this project’s, and carries its rungs, its kind, which says what it is, and its
status, how far the work on it here has gone: *recorded* when it has been registered
from its source and nothing here has read or replayed it, *reviewed* once its argument
has been read here, *confirmed* once a replay of its certificate has passed, and
*incomplete* while a defect found in it is open.
A bound that no case bound rests on now is marked *superseded*.
{{STAR_LEGEND}}

A result by others is recorded when its source is taken in, and its bound counts as
verified only after its certificate is replayed here in full and its mathematics
reviewed, with the credit its authors give;
[`epistemics.md`](epistemics.html#results-by-others) states the policy.
{{STATUS_COUNTS}}
The table starts with superseded results hidden, at significance S4 and up and a maximum
age of 180 days; clear Hide superseded, choose All and clear Max age to see every row.

{{RECENT}}

<p class="site-more"><a href="all-results.html">See all results{{ARROW_RIGHT}}</a></p>

<!-- This section's fragment was #verification-at-a-glance until 2026-10-01. The empty
     anchor in its heading keeps an old link landing here, with no script, and keeps
     forward.js from sending that fragment on to the explainer as one the overview lacks. -->

## Verification Ladders<a id="verification-at-a-glance"></a>

{{VERIFICATION}}

Evidence carries one of three assurance labels: *reported*, a named source’s claim not
checked here; *numerically checked*, a finite-precision calculation with its precision,
rounding and tolerance recorded; and *verified*, an exact check, rigorous interval
certificate or complete proof covering the claim and its preconditions.
A verified packing proves an upper bound only; calling it optimal needs a matching
verified lower bound.

Finite precision is not enough where squares touch exactly.
A tolerance that accepts a true zero-gap contact also accepts a small overlap, so a
contact-heavy packing is verified only with exact algebraic signs or outward-rounded
intervals ([why](synopsis.html#why-exactness-is-not-optional)). Schadt’s $n = 29$
packing passes its 300-digit numerical check, while the interval witness that is
verified proves a slightly weaker side; Trump’s $n = 11$ packing is verified exactly
over a degree-eight number field, fourteen zero-gap contacts included.

The same checks audit published work, where the theorem stays the source’s and this
repository adds an exact machine check: T-004 and T-008 check Bentz’s 2010 Theorem 8,
both halves of $s(46) = 7$ included, and T-011 checks Trump’s 1979 packing for eleven
squares.

## The Atlas

The best packings known for every tracked case, n = 1 to 324. Press one to see what the
film shows for it: its bounds, where each comes from, and what is still open, beside the
packing drawn large, with a link to its case record.

{{ATLAS_GRID}}

<!-- The atlas as files and as a film: the two posters, each opening its PDF, and the
     film. The cards and their note stood under the grid, in The Atlas, until 2026-10-01. -->

## PDFs and Videos

{{ATLAS_CARDS}}

<p class="site-wide site-atlas-note">The best packings known. A star marks a verified lower bound proved since 22 August 2026. There is also a shorter film of the <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-100-1080p60-citations.mp4">ascent from 1 to 100</a> (2 m 20 s). Both films are on the <a href="https://github.com/jlevy/squares/releases/tag/v0.4.2">v0.4.2 release</a> with the receipt recording each file and the page it was drawn from. Each poster is also an SVG (<a href="repo:packing/atlas/known-best/known-best-1-100.svg">1 to 100</a>, <a href="repo:packing/atlas/known-best/known-best-1-324.svg">1 to 324</a>). The <a href="repo:packing/atlas/known-best/README.md">atlas README</a> describes both.</p>

<!-- This section's fragment was #the-survey until 2026-10-01. The empty anchor in its
     heading keeps an old link landing here, as Verification Ladders keeps its own. -->

## The Frontier Survey<a id="the-survey"></a>

The frontier survey records the best-known packing and the strongest verified lower
bound for every $n \le 324$, with its provenance, keeping the bound a source reports
apart from the bound verified here.
An external certificate counts once it is replayed in full and its mathematical
assumptions are discharged, and each record says who ran the checks and how independent
they were. The [Frontier](frontier.html) page shows every case.
{{SURVEY_COUNTS}}
The [literature archive](repo:packing/resources/README.md) keeps each primary source, a
cleaned transcription and the unedited extraction it was checked against, and the
[evidence inventory](repo:packing/frontier/INVENTORY.md) shows what each claim rests on
and who did the work.

The frontier survey audits rather than transcribes.
The earliest published proof of $s(7) = 3$ carries four recorded defects in its printed
route, so the [$n = 7$ record](cases.html#n-7) rests the case on independent later
proofs.

Before this project’s work began on 22 August 2026, seven authors published lower bounds
for seventeen squares, some also for eighteen, all independently: Brandwijk’s $89/20$
(18 July), Burns’s $4.4811$ (6 August), MacIver’s $4.4502\ldots$ (8 August), Mira’s and
Fort’s sixteen-point sets (10 and 11 August), anabologyco-maker’s $4.57$ and $9141/2000$
(13 and 16 August), and Massaccesi’s $4.5058$ (21 August), replayed here as T-015 and
T-016. The [seventeen-square record](cases.html#n-17) lists them all; each has since
been superseded.

## Other Square Packing Projects

Others are working on the problem in the open.
These are the projects on GitHub that the research frontier cites, each credited to its
author. They are ordered by the significance of their results in the
[register](all-results.html): by how many stand at S5, then at S4, and so on down, the
newest first among equals.
Each card ends with a count that opens those results.

{{OTHER_PROJECTS}}

## Squares Project Documentation

The code, the certificates, the literature archive and the documents that record all of
this live in the Squares Project’s [repository](https://github.com/jlevy/squares).

{{DOCUMENT_CARDS}}
