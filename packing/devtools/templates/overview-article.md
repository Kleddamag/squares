<div class="site-hero">

# The Squares Project

<p class="subtitle">Packing unit squares in the smallest square · {{EDITION}}</p>

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
The [explainer](explainer.html) walks through the $n = 11$ proof with interactive
figures, the [tutorial](tutorial.html) introduces the problem from first principles, and
the [synopsis](synopsis.html) is the full research record.

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
[`epistemics.md`](https://github.com/jlevy/squares/blob/main/epistemics.md): **V**, the
strongest verification its evidence supports, and **C**, what this repository has
checked itself. A result by others is credited to its authors as their source states it;
its `V` and `C` are this repository’s own verification of it.
Open a row for the full claim, and follow the records to the case file, the evidence,
the retained source and the review.

{{RESULTS_TABLE}}

## Verification at a Glance

{{VERIFICATION}}

## Recently Registered

{{RECENT}}

## Read Further

- [**The explainer**](explainer.html): the $n = 11$ lower bound, with the certificate
  drawn and checkable in the page.
- [**The frontier atlas**](frontier.html): every case from $n = 1$ to $324$, with the
  reported and verified bounds side by side.
- [**The tutorial**](tutorial.html): square packing from first principles.
- [**The synopsis**](synopsis.html): the research program, its results and its status.
- [**The workbench**](workbench/): pack squares by hand and watch the known packings.
- [**The repository**](https://github.com/jlevy/squares): the code, the certificates,
  the literature archive and the process that produced all of this.
