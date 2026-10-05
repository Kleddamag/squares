"""Every paper of the series defines each term before it uses it, in reading order.

`devtools.paper_terms` reads a rendered paper as a reader meets it and holds it to the
paper's term registry (`templates/<slug>-terms.yaml`) and to the series registry
(`templates/n11-series-terms.yaml`); its docstring states the six rules. The first half
of this module runs them on every paper of the series, one entry per paper in `PAPERS`;
the second half proves each rule on a page small enough to read, so a rule that stopped
biting would fail here rather than pass on the papers.

Part I is advisory (series plan §9.4): it is published and older than the rule, so its
findings are reported as an expected failure rather than a failure. A paper joins the
gate by one entry in `PAPERS`; a paper whose page is not built here yet is named in
`PENDING`, and links to it are accepted until it joins. All three papers are under it.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pytest

from devtools import paper_links, paper_terms, render_n11_lower_bounds_explainer
from devtools import render_n11_optimality_review as review
from devtools import render_n11_threshold_bound_review as threshold
from devtools.paper_terms import Banned, Concept, Forward, Registry, Series, Term

REVISION = "a" * 40


@dataclass(frozen=True)
class PaperCase:
    """One paper under the gate: how to render its page, its article's source, and
    whether its findings fail the build or are reported."""

    slug: str
    render: Callable[[], str]
    article: Path
    advisory: bool = False


def _explainer() -> str:
    return render_n11_lower_bounds_explainer.render(
        render_n11_lower_bounds_explainer.WALKTHROUGH
    ).page


def _optimality_review() -> str:
    page, _ = review.render(
        review.ARTICLE.read_text(encoding="utf-8"),
        figures=review.render_all_figures(),
        facts=review.render_all_facts(),
        revision=REVISION,
    )
    return page


def _threshold_review() -> str:
    page, _ = threshold.render(
        threshold.ARTICLE.read_text(encoding="utf-8"),
        figures=threshold.render_all_figures(),
        facts=threshold.render_all_facts(),
        revision=REVISION,
    )
    return page


#: The papers under the gate, in reading order. Adding a paper is one entry here.
PAPERS = (
    PaperCase(
        render_n11_lower_bounds_explainer.SLUG,
        _explainer,
        render_n11_lower_bounds_explainer.MARKDOWN,
        advisory=True,
    ),
    PaperCase(threshold.SLUG, _threshold_review, threshold.ARTICLE),
    PaperCase(review.SLUG, _optimality_review, review.ARTICLE),
)
#: Papers of the series whose page this module does not build yet. A link to one is
#: accepted unchecked until it joins `PAPERS`, and then this set must drop it.
PENDING: frozenset[str] = frozenset()
ADVISORY = frozenset(case.slug for case in PAPERS if case.advisory)


@pytest.fixture(scope="module")
def html() -> dict[str, str]:
    """Every paper's rendered page, rendered once."""
    return {case.slug: case.render() for case in PAPERS}


@pytest.fixture(scope="module")
def pages(html: dict[str, str]) -> dict[str, paper_terms.Page]:
    """Every paper's rendered page, read once."""
    return {slug: paper_terms.read_page(page) for slug, page in html.items()}


@pytest.fixture(scope="module")
def registries() -> dict[str, Registry]:
    return {case.slug: paper_terms.load_registry(case.slug) for case in PAPERS}


def _hold(findings: list[paper_terms.Finding], *, advisory: bool) -> None:
    if not findings:
        return
    if advisory:
        pytest.xfail("advisory:\n" + paper_terms.report(findings))
    pytest.fail(paper_terms.report(findings))


@pytest.mark.parametrize("case", PAPERS, ids=[case.slug for case in PAPERS])
def test_every_term_is_defined_once_before_its_first_use(
    case: PaperCase,
    pages: dict[str, paper_terms.Page],
    registries: dict[str, Registry],
) -> None:
    """Rules 1-5 on the paper's rendered page."""
    findings = paper_terms.check_paper(pages[case.slug], registries[case.slug])
    _hold(findings, advisory=case.advisory)


@pytest.mark.parametrize("case", PAPERS, ids=[case.slug for case in PAPERS])
def test_every_formula_is_typeset(case: PaperCase, html: dict[str, str]) -> None:
    """Rule 7 on every paper, Part I included: no TeX reaches the reader as text, in the
    prose, the captions or the title."""
    _hold(paper_terms.check_math(html[case.slug]), advisory=False)


def test_the_series_links_each_concept_to_its_owner(
    pages: dict[str, paper_terms.Page], registries: dict[str, Registry]
) -> None:
    """Rule 6: a recap links the owner, an owner defines at its anchor, a symbol has one
    meaning across the series unless the series registry lists the clash."""
    findings = paper_terms.check_series(pages, registries, paper_terms.load_series())
    binding = [finding for finding in findings if finding.paper not in ADVISORY]
    _hold(binding, advisory=False)
    _hold(findings, advisory=True)


def test_every_link_to_another_paper_names_a_heading_it_has(
    pages: dict[str, paper_terms.Page],
) -> None:
    """A `{{PAPER:<slug>#<anchor>}}` link lands on a heading of the target's own page."""
    sources = {case.slug: case.article.read_text(encoding="utf-8") for case in PAPERS}
    findings, pending = paper_terms.check_paper_anchors(sources, pages)
    _hold(findings, advisory=False)
    assert {target for _, target, _ in pending} <= PENDING
    assert not PENDING & set(pages), "a paper under the gate is still listed as pending"
    assert PENDING <= paper_links.PAPER_SLUGS


def test_every_paper_has_a_registry_and_the_series_names_known_papers() -> None:
    for case in PAPERS:
        assert paper_terms.load_registry(case.slug).paper == case.slug
    series = paper_terms.load_series()
    assert {concept.owner for concept in series.concepts} <= paper_links.PAPER_SLUGS
    assert {"A", "\N{GREEK SMALL LETTER RHO}", "C"} <= set(series.clashes)


# --- each rule, on a page small enough to read ---

PAGE = """<html><body><nav><p>The core of the site.</p></nav>
<article>
<div class="hero"><h1 id="t">Title</h1><p>Credits name a core.</p></div>
<h2 id="intro">Intro</h2>
<p>A roadmap names the core before Section 2.</p>
<h2 id="cores">Cores</h2>
<p>Select a <strong>core</strong> strictly inside each square.
Its side is <span class="kpress-math"><span class="kpress-math-render">\\(B\\)</span>\
<span class="kpress-math-semantic"><math><mi>B</mi></math></span></span>.</p>
<figure><svg><text>core</text></svg><figcaption><strong>Figure 1.</strong> A core.\
</figcaption></figure>
<p><strong>Lemma.</strong> Every core is closed.<sup class="kpress-footnote-ref">1</sup></p>
<div class="kpress-math kpress-math-display"><div class="kpress-math-render">\\[B<1\\]</div>\
</div>
<h2 id="version-history">Version History</h2>
<p><strong>v0.1</strong> named a core first.</p>
<section class="kpress-footnotes"><p>A footnote's core.</p></section>
</article></body></html>"""


def _registry(*terms: Term, banned: tuple[Banned, ...] = ()) -> Registry:
    return Registry(paper="n11-optimality-review", terms=terms, banned=banned)


CORE = Term(
    term="core",
    uses=r"\bcores?\b",
    defined_by="Select a core strictly inside each square.",
    anchor="cores",
    forward=(Forward("names the core before Section 2", "roadmap"),),
)
SIDE = Term(term="B", uses=r"\bB\b", symbol=True, defined_by="Its side is $B$", anchor="cores")


def _rules(findings: list[paper_terms.Finding]) -> list[int]:
    return sorted(finding.rule for finding in findings)


def test_the_reader_keeps_exposition_in_order_and_reads_formulas_as_tex() -> None:
    page = paper_terms.read_page(PAGE)
    texts = [block.text for block in page.blocks]
    assert texts == [
        "Intro",
        "A roadmap names the core before Section 2.",
        "Cores",
        "Select a core strictly inside each square. Its side is $B$.",
        "Figure 1. A core.",
        "Lemma. Every core is closed.",
        "$B<1$",
    ]
    assert page.blocks[3].sections == ("cores",)
    assert page.blocks[3].prose.endswith("Its side is    .")
    assert page.blocks[3].tex.strip() == "B"
    assert page.blocks[-1].kind == "math"
    assert {"t", "intro", "cores", "version-history"} <= page.heading_ids


def test_a_registered_page_passes() -> None:
    page = paper_terms.read_page(PAGE)
    assert paper_terms.check_paper(page, _registry(CORE, SIDE)) == []


def test_rule_1_a_definition_occurs_once_in_its_section() -> None:
    page = paper_terms.read_page(PAGE)
    twice = Term(term="core", uses=r"\bcore\b", defined_by="core", anchor="cores")
    elsewhere = Term(term="core", uses=r"\bcore\b", defined_by=CORE.defined_by, anchor="intro")
    missing = Term(term="core", uses=r"\bcore\b", defined_by=CORE.defined_by, anchor="none")
    for term, message in (
        # Four in the exposition: the navigation, the credits, the drawing, the
        # footnote and the version history are not read.
        (twice, "occurs 4 times"),
        (elsewhere, "outside its section"),
        (missing, "is no heading id"),
    ):
        findings = paper_terms.check_paper(page, _registry(term))
        assert [finding.rule for finding in findings if finding.rule == 1] == [1], term
        assert message in str(findings[0])


def test_rule_2_no_use_precedes_the_definition_but_a_declared_forward_one() -> None:
    page = paper_terms.read_page(PAGE)
    bare = Term(term="core", uses=CORE.uses, defined_by=CORE.defined_by, anchor="cores")
    findings = paper_terms.check_paper(page, _registry(bare))
    assert _rules(findings) == [2]
    assert "a roadmap names the core" in str(findings[0]).lower()
    stale = Term(
        term="core",
        uses=CORE.uses,
        defined_by=CORE.defined_by,
        anchor="cores",
        forward=(*CORE.forward, Forward("Every core is closed", "roadmap")),
    )
    findings = paper_terms.check_paper(page, _registry(stale))
    assert _rules(findings) == [2]
    assert "covers no earlier use" in str(findings[0])
    # A formula is not prose: the symbol's pattern reads only the TeX.
    word = Term(term="B", uses=r"\bB\b", defined_by="Its side is $B$", anchor="cores")
    assert paper_terms.check_paper(page, _registry(CORE, word)) == []


def test_rule_3_a_required_term_is_registered_and_defined_first() -> None:
    page = paper_terms.read_page(PAGE)
    early = Term(
        term="core",
        uses=CORE.uses,
        defined_by=CORE.defined_by,
        anchor="cores",
        forward=CORE.forward,
        requires=("B",),
    )
    findings = paper_terms.check_paper(page, _registry(early, SIDE))
    assert _rules(findings) == [3]
    assert "defined after it" in str(findings[0])
    findings = paper_terms.check_paper(page, _registry(early))
    assert _rules(findings) == [3]
    assert "unregistered" in str(findings[0])


def test_rule_4_every_bold_run_is_a_definition_or_labels_a_block() -> None:
    page = paper_terms.read_page(PAGE.replace("Every core is closed", "Every <b>core</b> is"))
    findings = paper_terms.check_paper(page, _registry(CORE, SIDE))
    assert [(finding.rule, finding.subject) for finding in findings] == [(4, "core")]
    # Without the registry entry, the definition's own bold run is refused too; the
    # run-in head and the caption's label never are.
    findings = paper_terms.check_paper(paper_terms.read_page(PAGE), _registry(SIDE))
    assert [(finding.rule, finding.subject) for finding in findings] == [(4, "core")]


def test_rule_5_a_banned_bare_form_is_refused_in_prose_or_in_tex() -> None:
    page = paper_terms.read_page(PAGE)
    prose = Banned(r"\bstrictly\b", "say how strictly")
    symbol = Banned(r"B<1", "write the bound as a lemma", symbol=True)
    findings = paper_terms.check_paper(page, _registry(CORE, SIDE, banned=(prose, symbol)))
    assert [(finding.rule, finding.subject) for finding in findings] == [
        (5, "strictly"),
        (5, "B<1"),
    ]
    # A prose pattern does not read formulas, nor a TeX pattern prose.
    crossed = (Banned(r"B<1", "prose"), Banned(r"strictly", "tex", symbol=True))
    assert paper_terms.check_paper(page, _registry(CORE, SIDE, banned=crossed)) == []


def _series_case(
    *, link: str, owner_anchor: str = "cores"
) -> tuple[dict[str, paper_terms.Page], dict[str, Registry], Series]:
    owner = paper_terms.read_page(PAGE)
    recap = paper_terms.read_page(
        '<article><h2 id="r">Recap</h2>'
        f"<p>A <strong>core</strong> sits inside a square{link}.</p></article>"
    )
    pages = {"n11-lower-bounds-explainer": owner, "n11-optimality-review": recap}
    owned = Term(
        term="core",
        uses=CORE.uses,
        defined_by=CORE.defined_by,
        anchor=owner_anchor,
        forward=CORE.forward,
        series="core",
    )
    recapped = Term(
        term="core",
        uses=CORE.uses,
        defined_by="A core sits inside a square",
        anchor="r",
        series="core",
    )
    registries = {
        "n11-lower-bounds-explainer": Registry("n11-lower-bounds-explainer", (owned,)),
        "n11-optimality-review": Registry("n11-optimality-review", (recapped,)),
    }
    series = Series((Concept("core", "n11-lower-bounds-explainer", "cores"),))
    return pages, registries, series


def test_rule_6_a_recap_sits_in_a_block_that_links_the_owner() -> None:
    linked = ' (<a href="n11-lower-bounds-explainer.html#cores">Part I</a>)'
    assert paper_terms.check_series(*_series_case(link=linked)) == []
    findings = paper_terms.check_series(*_series_case(link=""))
    assert [(finding.rule, finding.paper) for finding in findings] == [
        (6, "n11-optimality-review")
    ]
    assert "does not link its owner" in str(findings[0])
    findings = paper_terms.check_series(*_series_case(link=linked, owner_anchor="intro"))
    assert [(finding.rule, finding.paper) for finding in findings] == [
        (6, "n11-lower-bounds-explainer")
    ]
    assert "not at the series anchor" in str(findings[0])


def test_rule_6_a_symbol_with_two_meanings_must_be_a_listed_clash() -> None:
    def defining(slug: str, series: str | None) -> Registry:
        return Registry(slug, (Term("A", r"A", "$A$", "x", symbol=True, series=series),))

    registries = {
        "n11-optimality-review": defining("n11-optimality-review", None),
        "n11-threshold-bound-review": defining("n11-threshold-bound-review", "parent"),
    }
    parent = (Concept("parent", "n11-threshold-bound-review", "x"),)
    findings = paper_terms.check_series({}, registries, Series(parent))
    assert [(finding.rule, finding.subject) for finding in findings] == [(6, "A")]
    assert "different meanings" in str(findings[0])
    listed = Series(parent, clashes={"A": "a local square against the parent side"})
    assert paper_terms.check_series({}, registries, listed) == []
    same = {slug: defining(slug, "parent") for slug in registries}
    assert paper_terms.check_series({}, same, Series(parent)) == []


def test_rule_6_a_cross_paper_link_names_a_heading_of_its_target() -> None:
    sources = {
        "n11-optimality-review": (
            "[a]({{PAPER:n11-lower-bounds-explainer#cores}}) "
            "[b]({{PAPER:n11-lower-bounds-explainer#nowhere}}) "
            "[c]({{PAPER:n11-threshold-bound-review#the-result}}) "
            "[d]({{PAPER:n11-lower-bounds-explainer}})"
        )
    }
    pages = {"n11-lower-bounds-explainer": paper_terms.read_page(PAGE)}
    findings, pending = paper_terms.check_paper_anchors(sources, pages)
    assert [finding.subject for finding in findings] == ["n11-lower-bounds-explainer#nowhere"]
    assert pending == [("n11-optimality-review", "n11-threshold-bound-review", "the-result")]


def test_rule_7_tex_printed_as_text_is_refused_in_prose_captions_and_title() -> None:
    assert paper_terms.check_math(PAGE) == []
    # A display formula run into its sentence is never typeset, and its TeX is prose.
    run_in = PAGE.replace(
        "<p>A roadmap names",
        "<p>so that\n$$\n\\frac{L_0}{A}=\\frac{31}{8},\n$$\nholds. A roadmap names",
    )
    assert {finding.subject for finding in paper_terms.check_math(run_in)} == {"$", "\\frac"}
    # A caption's formula written as `$...$` inside an HTML block.
    caption = PAGE.replace("A core.</figcaption>", "the side $T$.</figcaption>")
    assert caption != PAGE
    assert _rules(paper_terms.check_math(caption)) == [7, 7]
    # The title is read too, though the exposition reader skips the front.
    title = PAGE.replace(
        '<h1 id="t">Title</h1>',
        '<h1 id="t">Bound <span class="tex">s(11) \\gt 31/8</span></h1>',
    )
    assert paper_terms.check_math(title) == []
    raw_title = PAGE.replace('<h1 id="t">Title</h1>', '<h1 id="t">Bound s(11) \\gt 31/8</h1>')
    assert [finding.subject for finding in paper_terms.check_math(raw_title)] == ["\\gt"]
    # A display formula is a `$$` block, never a hand-wrapped `.tex-d` run.
    hand = PAGE.replace(
        "<p>A roadmap names",
        '<p class="centred"><span class="tex-d">s(11) \\ge L</span></p><p>A roadmap names',
    )
    assert [finding.subject for finding in paper_terms.check_math(hand)] == ["tex-d"]


def test_a_registry_out_of_form_is_refused() -> None:
    entry = {"term": "core", "uses": "core", "defined_by": "a core", "anchor": "cores"}
    assert paper_terms.parse_registry({"paper": "p", "terms": [entry]}).terms[0].term == "core"
    for bad, message in (
        ({**entry, "uses": "("}, "not a pattern"),
        ({**entry, "colour": "red"}, "unknown fields"),
        ({**entry, "forward": [{"text": "x", "reason": "because"}]}, "not one of the three"),
        ({**entry, "defined_by": ""}, "nonempty string"),
    ):
        with pytest.raises(paper_terms.RegistryError, match=message):
            paper_terms.parse_registry({"paper": "p", "terms": [bad]})
    with pytest.raises(paper_terms.RegistryError, match="twice"):
        paper_terms.parse_registry({"paper": "p", "terms": [entry, entry]})
    with pytest.raises(paper_terms.RegistryError, match="is no paper"):
        paper_terms.parse_series(
            {"concepts": [{"concept": "c", "owner": "n11-nonexistent", "anchor": "a"}]}
        )
