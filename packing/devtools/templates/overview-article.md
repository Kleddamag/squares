<div class="site-hero">

# Square Packing

</div>

## The Problem

How small can a square be and still hold $n$ unit squares that do not overlap?
Call the answer $s(n)$. The squares may be rotated, and they may touch.
The question is easy to state and open even at small $n$: the first case nobody has
settled is eleven squares.

For $n = 11$ the best packing known was found by {{S11_UPPER_BY}} in {{S11_UPPER_YEAR}},
and with the strongest verified lower bound the case now stands at

$$
{{S11_LOWER}} < s(11) \le {{S11_UPPER}},
$$

a gap of about {{S11_GAP}}. Before this project the lower bound had stood at
Stromquist’s $2 + 4/\sqrt{5} \approx 3.7889$ since 2003.

This site collects what the project has proved, what others have proved alongside it,
and how each claim was checked.

{{PAGE_CARDS}}

## Verification at a Glance

{{VERIFICATION}}

## Headline Results

The results scored `S5`, for movement on the central open case:

{{HEADLINE_CARDS}}

And the cases a recent lower bound has closed, where the exact value is now known:

{{EXACT_CARDS}}

## The Atlas

<figure class="site-wide site-atlas">
<a href="known-best-1-100.pdf"><img src="known-best-1-100.png" alt="One hundred known-best square packings, n = 1 to 100, each labelled with its best-known side and, where the case is open, its strongest verified lower bound." loading="lazy"></a>
<figcaption>The best packings known for n = 1 to 100. A star marks a verified lower bound proved since 22 August 2026. Also as a <a href="known-best-1-100.pdf">PDF</a>, the full <a href="known-best-1-324.pdf">n = 1 to 324 poster</a>, and a film of the <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-100-1080p60-citations.mp4">ascent from 1 to 100</a>. Every case is in the <a href="frontier.html">frontier atlas</a>.</figcaption>
</figure>

## Every Result

Each result has an identifier, a claim, and two ratings defined in
[`epistemics.md`]({{EPISTEMICS_URL}}): **V**, the strongest verification its evidence
supports, and **C**, what this repository has checked itself.
A result by others is credited to its authors as their source states it; its `V` and `C`
are this repository’s own verification of it.
Open a row for the full claim, and follow the records to the case file, the evidence,
the retained source and the review.

{{RESULTS_TABLE}}

## Recently Registered

{{RECENT}}

## On GitHub

The code, the certificates, the literature archive and the documents that record all of
this live in the Squares Project’s [repository](https://github.com/jlevy/squares).

{{DOCUMENT_CARDS}}
