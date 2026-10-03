"""The two papers share one structure, and cannot drift apart without this failing.

The owner asked on 2026-10-01 that the papers' "formats, formatting, and all structure
should be similar". `devtools.paper_structure` reads each rendered paper on every
structural axis and `devtools.paper_front` writes both papers' fronts from one record;
these tests render both papers and hold every form axis equal, and hold the credits of
each to the owner's dictated form (think-2cqu).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import paper_front, paper_structure, render_n11_lower_bounds_explainer
from devtools import render_n11_optimality_review as paper
from devtools.render_overview import paper_path
from sqpack import release

EXPLAINER = render_n11_lower_bounds_explainer.SLUG
REVIEW = paper.SLUG


@pytest.fixture(scope="module")
def structures() -> dict[str, paper_structure.Structure]:
    """Both papers as this checkout renders them, read as a reader meets them."""
    explainer = render_n11_lower_bounds_explainer.render(
        render_n11_lower_bounds_explainer.WALKTHROUGH
    )
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision="a" * 40,
    )
    return {
        EXPLAINER: paper_structure.read(EXPLAINER, explainer.page, explainer.markdown),
        REVIEW: paper_structure.read(REVIEW, html, markdown),
    }


@pytest.fixture(scope="module")
def rows(structures: dict[str, paper_structure.Structure]) -> list[dict[str, object]]:
    return paper_structure.compare(structures[EXPLAINER], structures[REVIEW])


def test_every_form_axis_is_the_same_on_both_papers(rows: list[dict[str, object]]) -> None:
    """The head, the formats row, the title, the credits' weights and links, the version
    and dates lines' form, the heading case, the captions, the footnotes, the colophon
    and the Markdown edition's opening: one way on both."""
    assert paper_structure.differences(rows) == []
    forms = {str(row["axis"]) for row in rows if row["compared"] == "form"}
    assert {
        "head: title",
        "head: og:type",
        "head: modified is the revised date",
        "formats row",
        "formats row: titles",
        "title: h1",
        "credits: names bold",
        "credits: addresses plain",
        "credits: dates end with",
        "sections: h2 case",
        "sections: h3 case",
        "figures: captions",
        "footnotes",
        "closing: colophon",
        "markdown: opening",
    } <= forms


def test_the_shared_form_is_the_one_the_design_names(rows: list[dict[str, object]]) -> None:
    found = {str(row["axis"]): str(row[EXPLAINER]) for row in rows}
    assert found["head: title"] == "name · project"
    assert found["head: og:type"] == "article"
    assert found["formats row"] == (
        "MD → <slug>.md · PDF → <slug>.pdf · GITHUB → https://github.com/jlevy/squares"
    )
    assert found["title: h1"] == "1, Title Case"
    assert found["credits: names bold"] == "yes"
    assert found["credits: addresses plain"] == "yes"
    assert found["credits: dates end with"] == paper_front.REVISED
    assert found["sections: h2 case"] == "Title Case"
    assert found["sections: h3 case"] == "sentence case"
    assert found["figures: captions"] == "Figure N. lead, numbered from 1"
    assert found["footnotes"] == "a footnotes section"
    assert found["closing: colophon"].startswith(
        "The Squares Project · github.com/jlevy/squares /"
    )


def test_each_papers_credits_follow_the_owners_form(
    structures: dict[str, paper_structure.Structure],
) -> None:
    """The review credits its source first, by name in bold and address as a plain link,
    then its own credits after a line's space; the explainer, which explains the
    project's own proofs, begins at its own. Both: oversight, agents, the version plain,
    then the dates, ending with when the paper was last revised."""
    explainer, review = structures[EXPLAINER].credits, structures[REVIEW].credits
    assert [line.kind for line in review] == list(paper_structure.CREDIT_KINDS)
    assert [line.kind for line in explainer] == list(paper_structure.CREDIT_KINDS[2:])
    source, address = review[:2]
    assert source.text == "From the original proof by Queuingtheorydotcom"
    assert source.bold == ("Queuingtheorydotcom",)
    assert address.bold == ()
    assert address.links == (
        (
            "github.com/Queuingtheorydotcom/11SquaresOptimal",
            "https://github.com/Queuingtheorydotcom/11SquaresOptimal",
        ),
    )
    for lines in (explainer, review):
        oversight, agents, version, dates = lines[-4:]
        assert oversight.text == "Human oversight: Joshua Levy"
        assert oversight.bold == ("Joshua Levy",)
        assert oversight.links == (("Joshua Levy", "https://x.com/ojoshe"),)
        assert agents.text.startswith("Agents: ")
        assert agents.bold == tuple(
            agents.text.removeprefix("Agents: ")
            .replace(", and ", ", ")
            .replace(" and ", ", ")
            .split(", ")
        )
        assert version.bold == ()
        assert dates.bold == ()
        assert dates.links == ()
        assert dates.text.endswith(
            f"{paper_front.REVISED} {release.EXPLAINER_REVISED}"
        ) or dates.text.endswith(f"{paper_front.REVISED} {release.OPTIMALITY_REVIEW_REVISED}")
    # Each paper's version line is its own version (the owner, 2026-10-01), never the
    # site's edition or the data hash.
    assert explainer[-2].text == f"{release.EXPLAINER_VERSION} (version history)"
    assert explainer[-2].links == (("version history", "#version-history"),)
    assert review[-2].text == f"{release.OPTIMALITY_REVIEW_EDITION} (version history)"
    assert review[-2].links == (("version history", "#version-history"),)
    for lines in (explainer, review):
        assert release.PUBLICATION_EDITION not in lines[-2].text
        assert release.DATA_REVISION[: release.DATA_REVISION_LENGTH] not in lines[-2].text
    assert explainer[-1].text == (
        f"First published {release.EXPLAINER_FIRST_PUBLISHED} · "
        f"Last revised {release.EXPLAINER_REVISED}"
    )
    assert review[-1].text == (
        f"Original proof {release.OPTIMALITY_PROOF_PUBLISHED} · "
        f"Last revised {release.OPTIMALITY_REVIEW_REVISED}"
    )


def test_the_markdown_editions_open_as_the_pages_do(
    structures: dict[str, paper_structure.Structure],
) -> None:
    """Each edition opens with the title as a heading and the credits as a list, the
    lines the page shows, in the page's order, with no chip row."""
    for name, structure in structures.items():
        head = structure.markdown_head
        assert head[0].startswith("# "), name
        items = [line.removeprefix("- ") for line in head[1:]]
        assert len(items) == len(structure.credits), name
        for item, line in zip(items, structure.credits, strict=True):
            for bold in line.bold:
                assert f"**{bold}**" in item, (name, item)
            for text, href in line.links:
                assert f"]({href})" in item, (name, item)
                assert text in item, (name, item)
        assert "chip" not in " ".join(head)


def test_the_tool_prints_the_audit_of_a_built_site(
    structures: dict[str, paper_structure.Structure],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`python -m devtools.paper_structure SITE --markdown` prints the table and exits
    0 when every form axis agrees, names the axes that differ when one does, and
    refuses a site that lacks a paper."""
    explainer = render_n11_lower_bounds_explainer.render(
        render_n11_lower_bounds_explainer.WALKTHROUGH
    )
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        figures=paper.render_all_figures(),
        facts=paper.render_all_facts(),
        revision="a" * 40,
    )
    for slug, page, document in (
        (EXPLAINER, explainer.page, explainer.markdown),
        (REVIEW, html, markdown),
    ):
        (tmp_path / paper_path(slug)).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / paper_path(slug)).write_text(page, encoding="utf-8")
        (tmp_path / paper_path(slug, ".md")).write_text(document, encoding="utf-8")
    assert paper_structure.main([str(tmp_path), "--markdown"]) == 0
    out = capsys.readouterr().out
    assert "| axis |" in out
    assert "| head: title | form | name · project | name · project | True |" in out
    assert structures[REVIEW].pdf == {}

    # A paper whose credits set a name plain is a form difference, and the tool says so.
    broken = html.replace("<strong>Queuingtheorydotcom</strong>", "Queuingtheorydotcom")
    (tmp_path / paper_path(REVIEW)).write_text(broken, encoding="utf-8")
    assert paper_structure.main([str(tmp_path)]) == 1
    assert "credits: names bold" in capsys.readouterr().err
    (tmp_path / paper_path(REVIEW)).unlink()
    with pytest.raises(SystemExit, match=r"has no papers/n11-optimality-review\.html"):
        paper_structure.main([str(tmp_path)])


def test_the_pdf_is_read_for_its_title_size_and_dates() -> None:
    pdf = (
        b"%PDF-1.4\n1 0 obj\n<</Title (A paper \\(draft\\))\n/Creator (Chromium)\n"
        b"/CreationDate (D:20261001120000+00'00')\n/ModDate (D:20261001120000+00'00')>>\n"
        b"endobj\n2 0 obj\n<</Type /Pages /Kids [3 0 R 4 0 R]>>\nendobj\n"
        b"3 0 obj\n<</Type /Page /MediaBox [0 0 612 792]>>\nendobj\n"
        b"4 0 obj\n<</Type /Page /MediaBox [0 0 612 792]>>\nendobj\n"
    )
    html = (
        "<html><head><title>A paper (draft)</title>"
        '<meta property="og:title" content="A paper (draft)"></head><body>'
        '<div class="credits centred"><span class="publication-date">'
        "Last revised October 1, 2026</span></div></body></html>"
    )
    found = paper_structure.axes(paper_structure.read("x", html, "", pdf))
    assert found["pdf: page size"] == "612 x 792 pt"
    assert found["pdf: pages"] == "2"
    assert found["pdf: title"] == "the page's title"
    assert found["pdf: dates"] == "the revised date, at noon UTC"
    assert paper_structure.axes(paper_structure.read("x", html))["pdf: pages"] == "no PDF"


@pytest.mark.parametrize(
    ("headings", "case"),
    [
        (("The Result and Proof Roadmap", "From a Continuum of Angles to 181"), "Title Case"),
        (("T-025: a direct certificate at 3.82", "Keeping everything else"), "sentence case"),
        (("The Result", "Keeping everything else"), "mixed"),
        ((), "none"),
    ],
)
def test_heading_case_is_read_as_a_reader_reads_it(
    headings: tuple[str, ...], case: str
) -> None:
    assert paper_structure.heading_case(headings) == case


def test_caption_form_names_what_departs_from_the_lead() -> None:
    assert paper_structure.caption_form(("Figure 1. A", "Figure 2. B")) == (
        "Figure N. lead, numbered from 1"
    )
    assert paper_structure.caption_form(("Figure 1. A", "Figure 3. B")) == "numbered [1, 3]"
    assert paper_structure.caption_form(("Figure 1. A", "B")) == (
        "a caption without a `Figure N.` lead"
    )
    assert paper_structure.caption_form(()) == "no figures"


def test_the_front_record_is_refused_where_it_departs_from_the_form() -> None:
    """`paper_front.check` refuses a record the owner's form has no line for."""
    front = paper.FRONT
    good = paper_front.check(front)
    assert good is front
    for broken, refusal in (
        (front._replace(version="**Draft v0.1.0**"), "plain text"),
        (front._replace(dates=front.dates[:1]), "ends with 'Last revised'"),
        (
            front._replace(dates=(paper_front.Dated(paper_front.REVISED, "2026-10-01"),)),
            "not `October 1, 2026`",
        ),
        (front._replace(oversight=()), "names someone"),
        (front._replace(agents=()), "the agents are named"),
        (front._replace(source=paper_front.Source("Q", "http://example.com")), "https"),
        (front._replace(history="Version History"), "by its id"),
        (front._replace(slug="papers/x"), "slug"),
    ):
        with pytest.raises(ValueError, match=refusal):
            paper_front.check(broken)
    assert paper_front.revised(front) == release.OPTIMALITY_REVIEW_REVISED
    assert "{{FRONT_MATTER}}" not in paper_front.front_matter(front)
    with pytest.raises(ValueError, match="exactly once"):
        paper_front.fill("no slot here", front)
    with pytest.raises(ValueError, match="does not carry the paper's front once"):
        paper_front.published("no front here", front)
