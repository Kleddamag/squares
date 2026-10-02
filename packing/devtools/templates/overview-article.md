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

<!-- One paragraph before the table (the owner, 2026-10-02): the headline of recent
     progress with its result ids, which check_results.READER_TIER holds to the
     register, then the star legend and where the table's filters start. README carries
     its own fuller account of the same progress, and the two stopped being one shared
     block that day (site_documents, think-ekw5). The ratings, the kinds, the statuses
     and the dating rule are defined once, on the Results page; a result's rungs, review
     and retained packet are its row's; and when a bound by others counts as verified is
     said once, on the Frontier page. -->

Eleven squares is settled: $s(11) = 3.8770835\ldots$, the exact side of Trump’s 1979
packing, by [T-060](all-results.html#t-060). Seventeen squares is bracketed by
machine-checked bounds, [T-043](all-results.html#t-043) below and
[T-065](all-results.html#t-065) above, and [$n = 21$](cases.html#n-21),
[$32$](cases.html#n-32) and [$45$](cases.html#n-45) have new exact values.
{{STAR_LEGEND}}
The table starts at significance S4 and up, max age 180 days and superseded hidden.

{{RECENT}}

<p class="site-action-row site-more"><a class="site-action" href="all-results.html">See all results{{ARROW_RIGHT}}</a></p>

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

<!-- This section's fragment was #the-atlas until 2026-10-01. The empty anchor in its
     heading keeps an old link landing here, as Verification Ladders keeps its own. -->

## The Atlas of Square Packings<a id="the-atlas"></a>

The best packings known for every tracked case, n = 1 to 324. Press one to see what the
film shows for it: its bounds, where each comes from, and what is still open, beside the
packing drawn large, with a link to its case record.

{{ATLAS_GRID}}

<!-- This section's fragment was #the-survey until 2026-10-01. The empty anchor in its
     heading keeps an old link landing here, as Verification Ladders keeps its own. It
     followed PDFs and Videos until the same day, when the owner set it directly after
     the atlas. What the survey counts, how a bound comes to count as verified, the
     audit of its sources and the seventeen-square history before this project are the
     Frontier page's own prose since 2026-10-02; here the survey is said in one
     paragraph and its cards lead there. -->

## The Frontier Survey<a id="the-survey"></a>

The frontier survey is the record the atlas is drawn from: for every case, the
best-known packing and the strongest verified lower bound, each with its source and the
evidence it rests on.
The [Frontier](frontier.html) page lists every case, counts the cases that have moved
since this project began, and says how the survey audits its sources and when a bound by
others counts as verified.

{{SURVEY_CARDS}}

<!-- The atlas as files and as a film: the two posters, each opening its PDF, and the
     film. The cards and their note stood under the grid, in The Atlas, until 2026-10-01,
     and this section followed the atlas directly until the survey moved between them
     the same day. -->

## PDFs and Videos

{{ATLAS_CARDS}}

<p class="site-wide site-atlas-note">The best packings known, each star a <a href="#recent-results">new result</a>. There is also a shorter film of the <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-100-1080p60-citations.mp4">ascent from 1 to 100</a> (2 m 20 s). Both films are on the <a href="https://github.com/jlevy/squares/releases/tag/v0.4.2">v0.4.2 release</a> with the receipt recording each file and the page it was drawn from. Each poster is also an SVG (<a href="repo:packing/atlas/known-best/known-best-1-100.svg">1 to 100</a>, <a href="repo:packing/atlas/known-best/known-best-1-324.svg">1 to 324</a>). The <a href="repo:packing/atlas/known-best/README.md">atlas README</a> describes both.</p>

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
