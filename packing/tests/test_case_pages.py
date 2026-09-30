"""The case records: one record per case at one address, opened the same way from the
overview's atlas grid and from the frontier atlas."""

from __future__ import annotations

import re

import pytest

from devtools import overview_sections, render_case_pages, render_overview
from devtools import render_research_tables as tables
from devtools.render_overview import PAGES, assert_self_contained

#: Measured at 9.1 MB on 2026-09-30 (324 records): 1.6 MB of site shell, 1.3 MB of large
#: drawings, 2.1 MB of formulas (TeX and its MathML fallback) and the rest the records'
#: prose, bounds and links. One page of every record replaces 324 pages that would each
#: carry the shell; a change that crosses the ceiling should shrink something.
PAGE_CEILING_BYTES = 11 * 1024 * 1024

SECTION = re.compile(r'<section class="site-case" id="n-(\d+)" data-n="(\d+)"')


@pytest.fixture(scope="module")
def page() -> str:
    return PAGES["cases.html"]().html


@pytest.fixture(scope="module")
def numbers() -> list[int]:
    return sorted(int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md"))


def _record(page: str, n: int) -> str:
    start = page.index(f'<section class="site-case" id="n-{n}"')
    end = page.find('<section class="site-case" id=', start + 1)
    return page[start : end if end > 0 else page.index("</article>", start)]


def test_every_case_has_one_record_at_its_own_address(page: str, numbers: list[int]) -> None:
    found = [(int(a), int(b)) for a, b in SECTION.findall(page)]
    assert [a for a, _ in found] == numbers
    assert all(a == b for a, b in found)
    assert "cases.html" in render_overview.SITE_PAGES
    assert render_case_pages.case_url(11) == "cases.html#n-11"


def test_the_atlas_grid_and_the_frontier_atlas_open_the_same_record(
    numbers: list[int],
) -> None:
    """Both entry points link each case to `cases.html#n-N` with `data-case`, which the
    shared popover script opens, and carry the one popover it opens in."""
    grid = overview_sections.atlas_grid()
    frontier = PAGES["frontier.html"]().html
    for source in (grid, frontier):
        links = re.findall(r'href="cases\.html#n-(\d+)" data-case="(\d+)"', source)
        assert [int(n) for n, _ in links] == numbers
        assert all(n == case for n, case in links)
        assert source.count(render_case_pages.case_popover()) == 1


def test_both_entry_pages_carry_the_popover_scripts() -> None:
    popover = render_overview.POPOVER_SCRIPT.read_text(encoding="utf-8")
    case_popover = render_case_pages.CASE_POPOVER_SCRIPT.read_text(encoding="utf-8")
    for name in ("index.html", "frontier.html"):
        html = PAGES[name]().html
        assert popover in html, name
        assert case_popover in html, name


def test_the_popover_frames_the_record_and_expands_to_it() -> None:
    markup = render_case_pages.case_popover()
    assert 'id="pop-case" popover' in markup
    assert 'data-go="page"' in markup
    assert "<iframe" in markup
    assert "data-case-frame" in markup
    assert 'data-case-expand href="cases.html"' in markup


def test_the_page_shows_one_record_by_its_fragment(page: str) -> None:
    assert render_case_pages.CASE_VIEW_SCRIPT.read_text(encoding="utf-8") in page
    assert "data-case-records" in page
    assert 'id="cases"' in page


def test_the_page_is_self_contained_and_under_its_ceiling(page: str) -> None:
    assert_self_contained("cases.html", page)
    assert len(page.encode()) < PAGE_CEILING_BYTES


def test_every_record_draws_its_packing_and_sets_its_bounds_as_math(
    page: str, numbers: list[int]
) -> None:
    for n in numbers:
        record = _record(page, n)
        assert '<figure class="site-case-figure' in record, n
        assert "<svg " in record, n
        assert f"s({n})" in record, n
        assert "data-kpress-math" in record, n


def test_no_math_is_left_as_source_text(page: str) -> None:
    article = re.sub(r"<script.*?</script>", "", page, flags=re.DOTALL).split("<article", 1)[1]
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article)
    # The case files' formulas, which they write in code spans, are set as math.
    assert "<code>s(11)</code>" not in article
    assert "<code>31/8</code>" not in article


def test_case_11_carries_its_polynomial_results_and_links(page: str) -> None:
    record = _record(page, 11)
    assert "Minimal polynomial, degree 8" in record
    assert "s^8 - 20s^7" in record
    for result in ("T-018", "T-026", "T-033"):
        assert f'<a href="index.html#{result.lower()}">{result}</a>' in record
    assert '<a href="frontier.html#n-11">' in record
    branch = f"{render_overview.REPO_URL}/blob/{render_overview.DEFAULT_BRANCH}/"
    assert f'class="site-case-github" href="{branch}packing/frontier/n-011.md"' in record
    assert 'href="#n-10" rel="prev"' in record
    assert 'href="#n-12" rel="next"' in record


def test_repository_links_name_the_build_commit_except_on_github(page: str) -> None:
    from devtools.check_published_site import branch_links, repository_links  # noqa: PLC0415
    from devtools.render_explainer import link_revision  # noqa: PLC0415

    branch = branch_links(page)
    assert {ref for _, ref, _ in branch} == {render_overview.DEFAULT_BRANCH}
    links = repository_links(page) - branch
    assert {ref for _, ref, _ in links} == {link_revision()}


def test_a_link_to_another_case_file_opens_its_record_here(page: str) -> None:
    """`n-013.md` links `n-012.md`; on this page that is case 12's record."""
    record = _record(page, 13)
    assert 'href="#n-12"' in record
    assert 'href="#n-32"' in record


@pytest.mark.parametrize(
    ("code", "tex"),
    [
        ("s(11) > 31/8 = 3.875", "s (11) > 31 / 8 = 3.875"),
        ("2 + 4/sqrt(5) = 3.788854\u2026", r"2 + 4 / \sqrt{5} = 3.788854 \ldots"),
        ("18*sqrt(5)/101", r"18 \sqrt{5} / 101"),
        ("\u2308\u221a112\u2309 = 11", r"\lceil\sqrt{112}\rceil = 11"),
        ("cos \u03b8\u2081", r"\cos \theta _{1}"),
        ("n \u2264 100", r"n \le 100"),
        ("10\u207b\u2079", "10 ^{-9}"),
        ("4.85e-30", r"4.85 \times 10^{-30}"),
        ("2 + \u00bd\u221a2", r"2 + \tfrac{1}{2} \sqrt{2}"),
        ("x, y \u2208 {1, 2}", r"x , y \in \{1 , 2\}"),
        ("k", "k"),
    ],
)
def test_a_code_span_that_is_mathematics_becomes_tex(code: str, tex: str) -> None:
    assert render_case_pages.code_tex(code) == tex


@pytest.mark.parametrize(
    "code",
    [
        "T-026",
        "V4/C5",
        "n-012.md",
        "reported_lower_bound",
        "minSide 32 = 6",
        "uv run --frozen --group dev packing-validate",
        "280af3d4\u2026e6e5",
        "campaign/series/x.json",
        "D4",
        "",
    ],
)
def test_a_code_span_that_names_something_stays_code(code: str) -> None:
    assert render_case_pages.code_tex(code) is None


def test_the_prose_sets_formulas_and_keeps_names() -> None:
    body = (
        "# Title\n\nA bound `s(11) > 31/8` from [`T-018`](RESULTS.md), in `exact_form`.\n\n"
        "## Section\n\n```\ns(61) > 7\u221a3/2 + 2\u221a2 \u2212 1\n```\n\n"
        "```bash\nuv run x\n```\n"
        "<!-- footer -->\n"
    )
    shown = render_case_pages.prose_markdown(body)
    assert "$s (11) > 31 / 8$" in shown
    assert "[`T-018`](RESULTS.md)" in shown
    assert "`exact_form`" in shown
    assert "### Title" in shown
    assert "#### Section" in shown
    assert "$$\ns (61) > 7 \\sqrt{3} / 2 + 2 \\sqrt{2} - 1\n$$" in shown
    assert "```bash\nuv run x\n```" in shown
    assert "footer" not in shown
