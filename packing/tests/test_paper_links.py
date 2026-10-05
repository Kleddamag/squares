"""A paper links another paper through one placeholder, filled per edition."""

from __future__ import annotations

import pytest

from devtools import paper_links, render_overview

SOURCE = (
    "See [Part I]({{PAPER:n11-lower-bounds-explainer}}) and the "
    "[optimality proof]({{PAPER:n11-optimality-review#the-result}})."
)


def test_a_page_links_its_sibling_by_a_page_relative_address() -> None:
    page = paper_links.fill_paper_links(SOURCE, edition="page")
    assert "(n11-lower-bounds-explainer.html)" in page
    assert "(n11-optimality-review.html#the-result)" in page
    assert "{{PAPER:" not in page


def test_the_markdown_edition_links_the_published_site() -> None:
    markdown = paper_links.fill_paper_links(SOURCE, edition="markdown")
    site = render_overview.SITE_URL
    assert f"({site}papers/n11-lower-bounds-explainer.html)" in markdown
    assert f"({site}papers/n11-optimality-review.html#the-result)" in markdown


def test_targets_are_listed_in_order() -> None:
    assert paper_links.paper_link_targets(SOURCE) == [
        ("n11-lower-bounds-explainer", None),
        ("n11-optimality-review", "the-result"),
    ]


def test_a_slug_that_is_not_a_paper_is_refused() -> None:
    with pytest.raises(ValueError, match="names no paper"):
        paper_links.fill_paper_links("{{PAPER:n11-nonexistent}}", edition="page")


def test_every_paper_slug_is_served_by_the_site() -> None:
    for slug in paper_links.PAPER_SLUGS:
        assert render_overview.paper_path(slug).startswith(render_overview.PAPERS_DIR + "/")
