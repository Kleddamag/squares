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
[independently checks and documents](all-results.html#verification-ladders) the proofs
and certificates behind them.

If you have new results or know of newer results, please
[file an issue]({{NEW_ISSUE_URL}}) to report them, and we will gladly incorporate them
and cite your work.

{{PAGE_CARDS}}

## Recent Results

<!-- The table first, then its one action, then what it shows (the owner, 2026-10-02,
     think-tgjv; the paragraph stood between the heading and the filter bar until that
     day). The first paragraph is the headline of recent progress, with its result ids,
     which check_results.READER_TIER holds to the register, the star legend and where
     the filters start. The second says what the three ratings on a row mean, rung by
     rung in brief, and the key under it shows every chip with its short meaning
     (rung_key); the ladders that define each rung in full, and the ratings' kinds,
     statuses and dating rule, are the Results page's. README carries its own fuller
     account of the same progress (site_documents, think-ekw5). -->

{{RECENT}}

<p class="site-action-row site-more"><a class="site-action" href="all-results.html">See all results{{ARROW_RIGHT}}</a></p>

Eleven squares is settled: $s(11) = 3.8770835\ldots$, the exact side of Trump’s 1979
packing, by [T-060](all-results.html#t-060). Seventeen squares is bracketed by
machine-checked bounds, [T-043](all-results.html#t-043) below and
[T-065](all-results.html#t-065) above, and [$n = 21$](cases.html#n-21),
[$32$](cases.html#n-32) and [$45$](cases.html#n-45) have new exact values.
{{STAR_LEGEND}}
The table above starts at significance S4 and up, max age 180 days and superseded
hidden.

Each row carries three ratings, each a rung of its own ladder.
Significance, S1 to S5, is how much the result matters, from bookkeeping at S1 to a move
on a central open case at S5. Verification, V0 to V5, is how it was first established: a
bare claim at V0, a numerical check at V1, a checkable proof or machine certificate at
V3, a formal proof at V5. Confirmation, C0 to C5, is how far it has been checked since:
recorded at C0, read at C1, replayed at C2, replayed by machine at C3, and up to a
formal confirmation at C5. The key below gives every rung in brief, and the
[Verification Ladders](all-results.html#verification-ladders) on the Results page define
each one in full.

{{RUNG_KEY}}

<!-- Verification Ladders stood here, between Recent Results and the atlas, until
     2026-10-02 (the owner, think-hqb3): the section is the Results page's, under its
     table, and Recent Results' second paragraph says what the ratings mean, over a key
     of every rung (think-tgjv), and links it. Its two
     fragments, #verification-ladders and the older #verification-at-a-glance, are sent
     there by forward.js (overview/forward.js). -->

<!-- This section's fragment was #the-atlas until 2026-10-01. The empty anchor in its
     heading keeps an old link landing here. -->

## The Atlas of Square Packings<a id="the-atlas"></a>

The best packings known for every tracked case, n = 1 to 324. Press one to see what the
film shows for it: its bounds, where each comes from, and what is still open, beside the
packing drawn large, with a link to its case record.

{{ATLAS_GRID}}

<!-- The Frontier Survey stood here, between the atlas and PDFs and Videos, until
     2026-10-02 (the owner, think-ec5k): its account is the Frontier page's own prose,
     and its card to that page is one of the page cards under The Squares Project. Its
     two fragments, #the-frontier-survey and the older #the-survey, are sent to the
     Frontier page by forward.js (overview/forward.js). -->

<!-- The atlas as files and as a film: the two posters, each opening its PDF, and the
     film. The cards and their note stood under the grid, in The Atlas, until 2026-10-01,
     and The Frontier Survey stood between this section and the atlas from that day until
     2026-10-02. -->

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
