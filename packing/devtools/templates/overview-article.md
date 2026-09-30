<div class="site-hero">

{{HERO}}

</div>

<!-- The explainer has a section of this name, and an old explainer link to it must
     still reach the explainer (forward.js), so this heading keeps the overview's own id. -->
<h2 id="the-problem">The Square Packing Problem</h2>

How small can a square be and still hold $n$ unit squares that do not overlap?
Call the answer $s(n)$. The squares may be rotated, and they may touch.
The question is easy to state and hard to settle: for most $n$ the answer is known only
to lie between the best packing found and a proved lower bound.

This site collects what the project has proved, what others have proved alongside it,
and how each claim was checked.

{{PAGE_CARDS}}

## Recent Results

The central thread is eleven squares.
T-010 repaired the printed argument behind Stromquist’s
$2 + 4/\sqrt{5} = 3.7888543\ldots$, stated in 1984 and published in 2003; T-018 passed
it with a weighted fractional certificate at $381/100$, whose
[proof card](repo:packing/cases/n11_fractional_certificate/t-018-proof-card.md) states
the whole proof and the one command that checks it; threshold atoms and exact dilation
limits then carried this project’s bound to T-033’s $3.8269975\ldots$. Kleddamag’s
$31/8$, developed from T-026’s certificate, now holds the case.

The results scored
<span class="site-chip site-rung-fill" data-rung="S" data-level="5">S5</span>, the
highest significance:

{{HEADLINE_CARDS}}

The cases a recent lower bound has closed, where the exact value is now known.
Evan Daniel’s are the exact values of $s(k^2 - 4)$ for $k = 5, 6, 7$, the first for any
$k \ge 4$:

{{EXACT_CARDS}}

A result by others is registered as *reported* when its source is taken in, and as
*verified* only after its certificate is replayed here in full and its mathematics
reviewed, with the credit its authors give;
[`epistemics.md`](epistemics.html#results-by-others) states the policy.
The newest results, each dated by its publication if it is by others and by the day it
was established if it is this project’s, with its standing: *holds* where a verified
case bound rests on it now, and otherwise why not.

{{RECENT}}

A reported bound counts here only once its certificate is replayed.
These are the cases up to $n = 100$ where a source reports a recent lower bound above
the one verified so far, each linked to its case in the frontier atlas:

{{AWAITING_REPLAY}}

## Verification at a Glance

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
film below shows for it: its bounds, where each comes from, and what is still open,
beside the packing drawn large, with a link to its case record.

{{ATLAS_GRID}}

<div class="site-wide site-atlas">
<figure>
<a href="known-best-1-100.pdf" type="application/pdf"><img src="known-best-1-100.png" alt="One hundred known-best square packings, n = 1 to 100, each labelled with its best-known side and, where the case is open, its strongest verified lower bound." loading="lazy"></a>
<figcaption>n = 1 to 100 · <a href="known-best-1-100.pdf" type="application/pdf">PDF</a></figcaption>
</figure>
<figure>
<a href="known-best-1-324.pdf" type="application/pdf"><img src="known-best-1-324.png" alt="Every tracked case, n = 1 to 324, each drawn as its best-known square packing." loading="lazy"></a>
<figcaption>n = 1 to 324 · <a href="known-best-1-324.pdf" type="application/pdf">PDF</a></figcaption>
</figure>
<figure class="site-atlas-film">
<video class="site-film" controls preload="none" playsinline width="1920" height="1080" poster="ascent-n1-324-poster.png" aria-label="The atlas built one unit square at a time, from n = 1 to n = 324, at 1080p60.">
<source src="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-324-1080p60-citations.mp4" type="video/mp4; codecs=&quot;avc1.640028&quot;">
<a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-324-1080p60-citations.mp4">The film of the ascent from 1 to 324</a>.
</video>
<figcaption>The ascent from n = 1 to 324, one square at a time, each step naming the bound it reaches and its source · 8 m 14 s · <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-324-1080p60-citations.mp4">open the film</a></figcaption>
</figure>
<p class="site-atlas-note">The best packings known. A star marks a verified lower bound proved since 22 August 2026. There is also a shorter film of the <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-100-1080p60-citations.mp4">ascent from 1 to 100</a> (2 m 20 s). Both films are on the <a href="https://github.com/jlevy/squares/releases/tag/v0.4.2">v0.4.2 release</a> with the receipt recording each file and the page it was drawn from. Each poster is also an SVG (<a href="repo:packing/atlas/known-best/known-best-1-100.svg">1 to 100</a>, <a href="repo:packing/atlas/known-best/known-best-1-324.svg">1 to 324</a>); the larger prints at 44 by 51 inches. The <a href="repo:packing/atlas/known-best/README.md">atlas README</a> describes both.</p>
</div>

## Every Result

Each result has an identifier, a claim, and two ratings defined in
[`epistemics.md`]({{EPISTEMICS_URL}}): **V**, the strongest verification its evidence
supports, and **C**, what this repository has checked itself.
A result by others is credited to its authors as their source states it; its `V` and `C`
are this repository’s own verification of it.
Its standing says whether a case bound rests on it now: it *holds* a verified bound, or
only a reported one; it is a *second certificate* for an exact value another result
holds; it is *superseded*; or it is not a bound at all, such as a rigidity or an
erratum. Open a row for the full claim and its novelty label, and follow the records to
the case file, the evidence, the retained source and the review.

{{RESULTS_TABLE}}

## The Survey

The survey records the best-known packing and the strongest verified lower bound for
every $n \le 324$, with its provenance, keeping the bound a source reports apart from
the bound verified here.
An external certificate counts once it is replayed in full and its mathematical
assumptions are discharged, and each record says who ran the checks and how independent
they were. The [frontier atlas](frontier.html) shows every case, and the
[status table](status.html) is the generated summary.
{{SURVEY_COUNTS}}
The [literature archive](repo:packing/resources/README.md) keeps each primary source, a
cleaned transcription and the unedited extraction it was checked against, and the
[evidence inventory](repo:packing/frontier/INVENTORY.md) shows what each claim rests on
and who did the work.

The survey audits rather than transcribes.
The earliest published proof of $s(7) = 3$ carries four recorded defects in its printed
route, so the [$n = 7$ record](repo:packing/frontier/n-007.md) rests the case on
independent later proofs.

Before this project’s work began on 22 August 2026, seven authors published lower bounds
for seventeen squares, some also for eighteen, all independently: Brandwijk’s $89/20$
(18 July), Burns’s $4.4811$ (6 August), MacIver’s $4.4502\ldots$ (8 August), Mira’s and
Fort’s sixteen-point sets (10 and 11 August), anabologyco-maker’s $4.57$ and $9141/2000$
(13 and 16 August), and Massaccesi’s $4.5058$ (21 August), replayed here as T-015 and
T-016. The [seventeen-square record](repo:packing/frontier/n-017.md) lists them all;
each has since been superseded.

## Other Square Packing Projects

Others are working on the problem in the open.
These are the projects on GitHub that the research frontier cites, each credited to its
author.

{{OTHER_PROJECTS}}

## On GitHub

The code, the certificates, the literature archive and the documents that record all of
this live in the Squares Project’s [repository](https://github.com/jlevy/squares).

{{DOCUMENT_CARDS}}
