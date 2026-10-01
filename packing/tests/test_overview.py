"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import functools
import html
import html.parser
import re
from collections import Counter
from collections.abc import Callable
from html.parser import HTMLParser

import pytest

from devtools import overview_data, overview_sections, render_overview, render_recent_results
from devtools.render_explainer import COMPOSITE_ASSETS, OVERVIEW_FILM_POSTER
from devtools.render_explainer import MARKDOWN as EXPLAINER_ARTICLE
from devtools.render_explainer import TEMPLATE as EXPLAINER_SHELL
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, hash_pinned_links, repo_url
from devtools.result_credit import OTHERS, source_lineage
from sqpack.yamlio import safe_load

ID = re.compile(r'\sid="([^"]+)"')
#: A results-table row: its id, whose result it is, and its confirmation rung's level.
ROW = re.compile(
    r'<tr id="(t-\d{3})" data-source="(ours|others)" data-v="\d" data-c="(\d)"[^>]*>'
)


@pytest.fixture(scope="module")
def page() -> str:
    return render_overview.overview_page().html


@pytest.fixture(scope="module")
def results() -> str:
    return render_overview.results_page().html


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


@functools.cache
def _rendered(name: str) -> str:
    """One render of each site page per test process. Rendering is deterministic
    (`test_the_render_is_deterministic`), so the checks below that only read a page share
    it; `cases.html` alone is about 9 MB and several seconds, and was rendered afresh by
    each of them."""
    return render_overview.PAGES[name]().html


@pytest.fixture(scope="module")
def rendered() -> Callable[[str], str]:
    """`_rendered`, with `cases.html` rendered during setup rather than inside whichever
    test reaches it first, so no single check carries that page's render in its own
    call time."""
    _rendered("cases.html")
    return _rendered


def test_every_register_entry_is_one_row(results: str, register: list[dict]) -> None:
    rows = ROW.findall(results)
    assert sorted(row_id for row_id, _, _ in rows) == sorted(r["id"].lower() for r in register)
    declared = {r["id"].lower(): r for r in register}
    for row_id, source, confirmation in rows:
        record = declared[row_id]
        assert source == ("others" if record.get("attribution") else "ours"), row_id
        assert f"C{confirmation}" == record["confirmation"], row_id


def test_counts_are_the_declared_rungs(register: list[dict]) -> None:
    stats = overview_data.stats(overview_data.load())
    ours = [r for r in register if not r.get("attribution")]
    others = [r for r in register if r.get("attribution")]
    assert (stats.total, stats.ours, stats.others) == (len(register), len(ours), len(others))
    assert stats.verification == Counter(r["verification"] for r in register)
    assert stats.confirmation_ours == Counter(r["confirmation"] for r in ours)
    assert stats.confirmation_others == Counter(r["confirmation"] for r in others)
    assert stats.cases_1_100_proved + stats.cases_1_100_open == 100


def test_the_render_is_deterministic(page: str, results: str) -> None:
    assert render_overview.overview_page().html == page
    assert render_overview.results_page().html == results


def test_the_results_table_has_its_own_page_and_the_overview_points_to_it(
    page: str, results: str
) -> None:
    """The table is on `all-results.html`, marked current in the bar, with its sorting
    and filters; the overview keeps no row of it, only a pointer under the recent table."""
    assert render_overview.RESULTS_PAGE == "all-results.html"
    assert "all-results.html" in render_overview.SITE_PAGES
    assert "results.html" in render_overview.DOCUMENT_PAGES
    assert 'aria-current="page" href="all-results.html">Results</a>' in results
    assert "data-site-table" in results
    assert render_overview.TABLE_SCRIPT.read_text(encoding="utf-8") in results
    assert '<h1 id="every-result">' in results
    assert not ROW.findall(page)
    assert 'id="every-result"' not in page
    recent = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    assert '<a href="all-results.html">See all results' in recent


def test_every_link_to_a_result_goes_to_its_row(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """The overview's recent table and replay table, and the case records, link a
    result at its row on the results page, never at a fragment of their own page."""
    rows = {row_id for row_id, _, _ in ROW.findall(results)}
    linked = re.findall(r'href="all-results\.html#([^"]+)"', page)
    assert linked
    assert set(linked) <= rows
    assert not re.search(r'href="#t-\d+"', page)
    cases = rendered("cases.html")
    assert set(re.findall(r'href="all-results\.html#([^"]+)"', cases)) <= rows
    assert 'href="index.html#t-' not in cases


def test_every_moved_fragment_is_one_the_forwarder_sends_on(page: str, results: str) -> None:
    """`forward.js` sends `#every-result` and a row's id from the overview to the results
    page (`tests/node/overview_forward` runs it): every row id is of the form it
    recognises, the section's lands on the page's title, and no id the overview keeps is."""
    forward = render_overview.FORWARD_SCRIPT.read_text(encoding="utf-8")
    assert 'id === "every-result" || /^t-\\d+$/.test(id)' in forward
    assert "all-results.html" in forward
    moved = re.compile(r"every-result|t-\d+")
    assert all(moved.fullmatch(row_id) for row_id, _, _ in ROW.findall(results))
    assert 'id="every-result"' in results
    assert not [i for i in ID.findall(page) if moved.fullmatch(i)]


def test_the_page_fetches_nothing(page: str) -> None:
    render_overview.assert_self_contained("index.html", page)


def test_the_bar_leads_with_case_11_beside_the_name(page: str) -> None:
    """The bar's home link carries case 11, the tab's icon, in the bar's own ink."""
    link = page.split('<a class="site-name"', 1)[1].split("</a>", 1)[0]
    assert '<svg class="site-logo" ' in link
    assert 'aria-hidden="true"' in link.split("<svg", 1)[1].split(">", 1)[0]
    assert '<span class="site-name-text">Square Packing</span>' in link
    assert render_overview.site_logo() in link


def test_the_site_icon_is_case_11_and_fetches_nothing(page: str) -> None:
    icon = render_overview.favicon_html()
    assert page.count(icon) == 1
    assert icon.startswith('<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,')
    with pytest.raises(SystemExit):
        render_overview.assert_self_contained("x.html", '<link rel="icon" href="icon.svg">')


def test_the_hero_draws_its_case_and_links_to_its_row(page: str) -> None:
    n = overview_sections.HERO_CASE
    hero = page.split('class="site-hero-figure', 1)[1].split("</figure>", 1)[0]
    assert f'href="frontier.html#n-{n}"' in hero
    assert hero.count("<svg ") == 1


def _atlas_cards(page: str) -> list[tuple[str, str]]:
    """The atlas's direct cards, between its grid and its note: each href and body."""
    section = page.split('id="the-atlas"', 1)[1].split("<h2", 1)[0]
    after_grid = section.split('class="site-cards-frame', 1)[1]
    return re.findall(
        r'<a class="site-card site-card-link" href="([^"]+)"(.*?)</a>', after_grid, re.DOTALL
    )


def test_the_atlas_posters_are_hero_cards_each_opening_its_pdf(page: str) -> None:
    """Each poster is a card headed by its picture that is itself the link to its PDF,
    typed as PDF and never marked for download, so the browser opens it in place."""
    cards = dict(_atlas_cards(page))
    for stem, hero in (
        ("known-best-1-100", "known-best-1-100-card.png"),
        ("known-best-1-324", "known-best-1-324.png"),
    ):
        body = cards[f"{stem}.pdf"]
        assert body.startswith(' type="application/pdf"'), stem
        assert f'<span class="site-card-hero"><img src="{hero}" alt=""' in body, stem
        assert (COMPOSITE_ASSETS[0].parent / hero).is_file(), hero
    assert re.search(r"<a\b[^>]*\sdownload\b", page) is None


def test_the_atlas_film_is_a_hero_card_opening_the_visualize_page(page: str) -> None:
    """The film is no longer embedded here: its card, headed by a frame of the film served
    beside the page, opens the Visualize page, which shows the film alone."""
    cards = _atlas_cards(page)
    assert [href for href, _ in cards] == [
        "known-best-1-100.pdf",
        "known-best-1-324.pdf",
        overview_sections.VISUALIZE_PAGE,
    ]
    body = dict(cards)[overview_sections.VISUALIZE_PAGE]
    assert f'<img src="{OVERVIEW_FILM_POSTER.name}" alt=""' in body
    assert '<span class="site-card-label">Visualize</span>' in body
    assert OVERVIEW_FILM_POSTER in COMPOSITE_ASSETS
    assert OVERVIEW_FILM_POSTER.is_file()
    assert "<video" not in page


def test_every_direct_card_opens_in_a_new_tab(page: str) -> None:
    """A card that is itself the link opens its target in a new tab, on the site or off
    it, and never hands the new tab a way back to this one."""
    direct = re.findall(r'<a class="site-card[^"]*"[^>]*>', page)
    assert len(direct) == len(overview_sections.OTHER_PROJECTS) + len(
        overview_sections.ATLAS_CARDS
    )
    for tag in direct:
        assert 'target="_blank"' in tag, tag
        assert 'rel="noopener noreferrer"' in tag, tag


def test_a_card_hero_is_served_beside_the_page_never_fetched() -> None:
    hero = overview_sections.card_hero("known-best-1-100-card.png")
    assert hero.startswith('<span class="site-card-hero"><img ')
    assert 'loading="lazy"' in hero
    for address in ("https://example.org/x.png", "//example.org/x.png"):
        with pytest.raises(SystemExit):
            overview_sections.card_hero(address)
    button = overview_sections.card(
        "pop-x", "Label", "Value", "Note", href="#x", action="Go", hero="x.png"
    )
    assert button.index('class="site-card-hero"') < button.index('class="site-card-label"')


def test_the_atlas_grid_draws_every_case_and_places_it_lazily(page: str) -> None:
    """One cell per tracked case, each linking to its case record, in two templates the
    script places: the first hundred when the grid comes near, the rest on expanding."""
    grid = page.split("data-atlas-grid>", 1)[1].split("data-atlas-facts>", 1)[0]

    def cells(which: str) -> list[int]:
        template = grid.split(f"<template data-atlas-{which}>", 1)[1]
        template = template.split("</template>", maxsplit=1)[0]
        found = re.findall(
            r'<a class="site-atlas-cell" href="cases\.html#n-(\d+)" data-atlas-n="(\d+)"',
            template,
        )
        assert all(n == cell for n, cell in found)
        assert template.count("<svg ") == len(found)
        return [int(n) for n, _ in found]

    assert cells("first") == list(range(1, 101))
    assert cells("rest") == list(range(101, 325))
    assert grid.count("<template") == 2
    assert re.findall(r'aria-label="n = 11, [a-z]+"', grid)
    assert render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8") in page


def test_the_atlas_grid_expands_from_100_to_324_with_one_button() -> None:
    """Under the grid one centred button, the site's action button, reads "Show all 324"
    and says it is collapsed; its row ships hidden, since only the script makes it act.
    The script places the rest on the first expand, flips the label and `aria-expanded`,
    and expands the grid when the popover steps past the last case shown."""
    grid = overview_sections.atlas_grid()
    (row,) = re.findall(r'<p class="site-atlas-toggle-row" hidden>(.*?)</p>', grid)
    assert row == (
        '<button type="button" class="site-popover-action site-atlas-toggle" '
        'data-atlas-toggle aria-expanded="false" data-label-more="Show all 324" '
        'data-label-less="Show 1 to 100">Show all 324</button>'
    )
    assert grid.index("data-atlas-toggle") < grid.index('class="site-atlas-note"')
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert 'toggle.setAttribute("aria-expanded", String(open))' in script
    assert "rest.append(restTemplate.content.cloneNode(true))" in script
    step = script[script.index("A case the grid does not show yet") :]
    assert "expandGrid(true)" in step[: step.index("show(next)")]


def test_the_atlas_expander_reuses_the_action_button_and_tokens() -> None:
    """The expander takes the popover action button's own rule, widened to a <button>,
    not a style of its own; its spacing is a token, and the placed rest is one box the
    grid lays out as its cells, hidden when collapsed."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert ".kpress :is(.site-popover a, button).site-popover-action {" in css
    assert ".site-atlas-toggle {" not in css
    row = css[css.index(".site-atlas-grid .site-atlas-toggle-row {") :]
    row = row[: row.index("}")]
    assert "margin-block: var(--site-atlas-toggle-space) 0;" in row
    grid = css[css.index(".site-page .site-atlas-grid {") :]
    assert "--site-atlas-toggle-space:" in grid[: grid.index("}")]
    rest = css[css.index(".site-atlas-rest {") :]
    assert "display: contents;" in rest[: rest.index("}")]
    assert ".site-atlas-rest[hidden] {\n  display: none;" in css


def _atlas_facts(page: str) -> dict[int, dict]:
    import json  # noqa: PLC0415

    body = page.split('<script type="application/json" data-atlas-facts>', 1)[1]
    return {fact["n"]: fact for fact in json.loads(body.split("</script>", 1)[0])}


def test_the_atlas_popover_carries_what_the_film_shows_for_each_case(page: str) -> None:
    """The one atlas popover is filled from the grid's facts: for n = 11, settled by
    T-060, the exact value, its star and badges and both bounds' sources with this
    project's notes; for n = 17, still open, the film's chained bound and what is open;
    all read from the atlas figure and `bound-citations.json`."""
    facts = _atlas_facts(page)
    assert sorted(facts) == list(range(1, 325))
    eleven = facts[11]
    assert eleven["exact"] is True
    assert (eleven["lower"], eleven["upper"]) == (None, "3.877084")
    assert eleven["star"] is True
    assert [label for _, _, label in eleven["badges"]] == ["optimal", "exact", "rigid"]
    assert eleven["open"] == []
    assert eleven["record"] == "n-011"
    assert eleven["cite"]["lower"] == {
        "text": "Queuingtheorydotcom after Levy et al. 2026, Web",
        "note": "(confirmed T-060)",
    }
    assert eleven["cite"]["upper"] == {
        "text": "Trump 1979, Squares in Squares",
        "note": "(confirmed T-011)",
    }
    seventeen = facts[17]
    assert seventeen["exact"] is False
    assert (seventeen["lower"], seventeen["upper"]) == ("4.660440", "4.675531")
    assert seventeen["open"] == ["optimality"]
    assert seventeen["cite"]["lower"]["note"] == "(confirmed T-043)"
    assert facts[1] == {**facts[1], "exact": True, "upper": "1", "lower": None, "open": []}
    assert page.count('id="pop-atlas" popover') == 1
    assert page.count(" data-atlas-popover ") == 1


def test_the_atlas_popover_sets_its_math_and_leads_to_the_record(page: str) -> None:
    """Its math is kpress's own math node (the formulas under the gap bar, and the
    template every value is typeset from), never raw TeX; its button is Expand to the
    case record, which the script points at `cases.html#n-N` for the case shown."""
    popover = page.split('id="pop-atlas" popover', 1)[1].split("</template></div>", 1)[0]
    assert popover.count('class="kpress-math kpress-math-inline"') == 3
    assert r"\sqrt{n} + 1" in popover
    assert "$" not in popover
    (action,) = re.findall(r'<a class="site-popover-action"[^>]*>([^<]*)</a>', popover)
    assert action == "See All Cases"
    assert "data-atlas-expand" in popover
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    assert 'expand.setAttribute("href", cell.getAttribute("href")' in script
    assert "site-atlas-tip" not in page


def test_the_document_is_kpress_viewport_with_its_contents_behaviours(page: str) -> None:
    """A site page scrolls the document, so the document is the element kpress watches:
    with `<main>` marked instead, the contents rail's scroll-spy observed a pane that
    never scrolls. kpress's contents-rail and history modules ride on every page, since
    without them nothing marks the section in view."""
    assert page.count("<html data-kpress-viewport ") == 1
    assert '<main class="kpress-page-main kpress-viewport">' in page
    for module in render_overview.KPRESS_CLIENT_MODULES:
        assert f"/* kpress: js/{module} */" in page, module


def test_every_card_grid_sits_in_a_frame_it_can_measure(page: str) -> None:
    """A section of three cards or fewer centres them only when its grid can ask how many
    columns its frame fits, so every grid is the only child of a `.site-cards-frame`."""
    grids = re.findall(r'<div class="([^"]*)"><div class="(site-cards[^"]*)">', page)
    every = re.findall(r'<div class="site-cards[" ]', page)
    assert len(grids) == len(every), "a card grid outside a frame"
    assert all(frame == "site-cards-frame site-wide" for frame, _ in grids)
    assert any("site-cards-dimensions" in grid for _, grid in grids)


def test_each_dimension_card_carries_every_level_of_the_rubric(page: str) -> None:
    levels = overview_sections.rubric_levels()
    assert [len(levels[scale]) for scale in "VCS"] == [6, 6, 5]
    for scale, _, section, _ in overview_sections.DIMENSIONS:
        panel = page.split(f'popovertarget="pop-dimension-{scale.lower()}"', 1)[1]
        panel = panel.split("</button>", 1)[0]
        for level, meaning in levels[scale]:
            assert f'data-rung="{scale}" data-level="{level}">{scale}{level}</span>' in panel
            assert html.escape(meaning, quote=True) in panel
        assert f'href="epistemics.html#{section}"' in page


def test_no_placeholder_or_raw_math_is_left(page: str) -> None:
    article = re.sub(r"<script.*?</script>", "", page, flags=re.DOTALL).split("<article", 1)[1]
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not re.search(r"\bs\(\d+\) *[<>]=", article)
    assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article)


def test_every_record_link_is_on_main_or_a_site_page() -> None:
    for result in overview_data.load().results:
        for link in result.records:
            assert (
                link.url.startswith(f"{REPO_URL}/blob/{DEFAULT_BRANCH}/")
                or link.url == "frontier.html"
            ), (result.id, link)


def test_every_repository_link_on_the_page_names_main(page: str) -> None:
    """The deployed-site check refuses a repository link pinned to a commit: every one
    names `main`, the prose's `repo:` links and the "On GitHub" links alike."""
    from devtools.check_published_site import repository_links  # noqa: PLC0415

    assert not hash_pinned_links(page)
    links = repository_links(page)
    assert links
    assert {ref for _, ref, _ in links} == {DEFAULT_BRANCH}


def test_on_github_links_open_the_latest_version() -> None:
    """Each document card and rubric card has an "On GitHub" link on `main`."""
    page = render_overview.overview_page().html
    branch = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/"
    also = re.findall(r'<a class="site-popover-also" href="([^"]+)"[^>]*>On GitHub</a>', page)
    assert len(also) == len(overview_sections.DOCUMENTS) + len(overview_sections.DIMENSIONS)
    assert all(url.startswith(branch) for url in also)


def test_other_projects_include_every_source_repository_the_record_reviews() -> None:
    coverage = safe_load(
        (overview_data.REPO / "packing/frontier/source-coverage.yaml").read_text(
            encoding="utf-8"
        )
    )
    reviewed = {
        re.sub(r"/tree/.*", "", source["url"])
        for source in coverage["sources"]
        if source["role"] == "source-repository" and "github.com" in source["url"]
    }
    listed = [url for url, _, _ in overview_sections.OTHER_PROJECTS]
    assert reviewed <= set(listed)
    assert len(set(listed)) == len(listed)
    assert not any("jlevy/squares" in url for url in listed)


def test_other_project_cards_are_links_showing_their_address(page: str) -> None:
    """Each other project's card is the link itself, with no popover, and shows its
    address beside GitHub's mark (or the host's saved favicon)."""
    section = page.split('id="other-square-packing-projects"', 1)[1].split("<h2", 1)[0]
    cards = re.findall(r'<a class="site-card site-card-link" href="([^"]+)"(.*?)</a>', section)
    assert [url for url, _ in cards] == [url for url, _, _ in overview_sections.OTHER_PROJECTS]
    for url, body in cards:
        assert url.removeprefix("https://") in body.replace("<wbr>", ""), url
        assert 'class="site-link-icon"' in body, url
    assert "popovertarget" not in section
    assert "pop-project-" not in page


def test_record_line_links_point_at_their_entry() -> None:
    lines = overview_data.RESULTS.read_text(encoding="utf-8").splitlines()
    for result in overview_data.load().results:
        (register,) = (link for link in result.records if link.label == "register")
        line = int(register.url.rsplit("#L", 1)[1])
        assert lines[line - 1].strip() == f"- id: {result.id}", result.id


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def test_overview_ids_never_shadow_an_explainer_anchor(page: str) -> None:
    """`forward.js` sends a fragment the overview lacks to the explainer, so an old
    explainer deep link lands on the overview only if the overview has the same id."""
    explainer = EXPLAINER_ARTICLE.read_text(encoding="utf-8")
    explainer_ids = set(ID.findall(explainer + EXPLAINER_SHELL.read_text(encoding="utf-8")))
    explainer_ids |= {
        _slug(h) for h in re.findall(r"^#{1,4} (.+)$", explainer, flags=re.MULTILINE)
    }
    ours = {i for i in ID.findall(page) if not i.startswith("kpress-")}
    assert not ours & explainer_ids
    moved = {i for i in ID.findall(render_overview.results_page().html) if i.startswith("t-")}
    assert moved
    assert not moved & explainer_ids


def test_the_nav_links_only_to_served_pages() -> None:
    nav = render_overview.nav_html("overview")
    served = {"./", *render_overview.SITE_PAGES, "workbench/"}
    for href in re.findall(r'href="([^"]+)"', nav):
        assert href.startswith("https://") or href in served, href
    assert nav.count('aria-current="page"') == 1


@pytest.mark.parametrize(
    ("prose", "tex"),
    [
        ("s(11) >= 2 + 4/sqrt(5) by a repair", [r"s(11) \ge 2 + 4/\sqrt{5}"]),
        ("s(17), s(18), s(19) >= 459/100 by", [r"s(17), s(18), s(19) \ge 459/100"]),
        ("a bound on s(N) for every 4 <= N <= 100", ["s(N)", r"4 \le N \le 100"]),
        ("s(46) = 7 from the 7 x 7 grid", ["s(46) = 7", r"7 \times 7"]),
        ("need side >= 3.8770835..., equal", [r"\ge 3.8770835\ldots"]),
        ("s(11) > 31/8 by a certificate", ["s(11) > 31/8"]),
        ("Goebel's n = 5 packing", ["n = 5"]),
    ],
)
def test_register_prose_math_is_found_and_set_in_tex(prose: str, tex: list[str]) -> None:
    runs = [match.group(0) for match in overview_data.MATH.finditer(prose)]
    assert [overview_data.prose_tex(run) for run in runs] == tex
    assert overview_data.tex_bounds(prose).count("data-kpress-math") >= len(tex)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_site_page_loads_math_through_the_explainers_pipeline(
    name: str, rendered: Callable[[str], str]
) -> None:
    """One math pipeline: the explainer's KaTeX bundle and host adapter, driven by the
    site's queue, and neither of kpress's whole-page entry points (auto-render and its
    native initializer), which typeset every formula in one task at DOMContentLoaded."""
    from devtools.render_explainer import katex_js, kpress_static  # noqa: PLC0415

    page = rendered(name)
    static = kpress_static()
    assert katex_js(static) in page
    assert render_overview.MATH_SCRIPT.read_text(encoding="utf-8") in page
    for entry in ("katex/auto-render.min.js", "katex/katex-init.js"):
        assert (static / entry).read_text(encoding="utf-8") not in page, entry


@pytest.mark.parametrize("name", ["index.html", "tutorial.html"])
def test_every_site_page_carries_the_explainers_text_tokens(
    name: str, rendered: Callable[[str], str]
) -> None:
    """The type base, measure and heading scale come from the one file the explainer
    inlines too, after kpress's stylesheets so they win at kpress's own scopes."""
    page = rendered(name)
    tokens = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert tokens in page
    assert page.index(tokens) > page.index("/* kpress: css/style-tokens.css */")
    assert page.index(tokens) < page.index(render_overview.SITE_CSS.read_text(encoding="utf-8"))


def test_the_text_tokens_are_declared_in_one_place() -> None:
    """No page layer re-declares what `paper-type.css` owns, so no page can drift."""
    owned = (
        "--kpress-host-font-size-base:",
        "--kpress-measure:",
        "--kpress-font-size-h2:",
        "--kpress-host-font-sans:",
    )
    tokens = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    for name in owned:
        assert name in tokens, name
    for layer in (EXPLAINER_SHELL, render_overview.SITE_CSS, render_overview.SITE_NAV_CSS):
        text = layer.read_text(encoding="utf-8")
        for name in owned:
            assert name not in text, f"{layer.name} re-declares {name}"
    assert "{{PAPER_TYPE_CSS}}" in EXPLAINER_SHELL.read_text(encoding="utf-8")


def test_the_nav_ends_in_an_accessible_theme_control() -> None:
    """The gear is a named button that opens a menu of three radio items, System, Light
    and Dark, and it is the bar's last item."""
    nav = render_overview.nav_html("overview")
    gear = re.search(r'<button type="button" class="site-theme-button"[^>]*>', nav)
    assert gear, "the nav has no theme gear"
    for attribute in (
        'aria-label="Color theme"',
        'aria-haspopup="menu"',
        'aria-expanded="false"',
        'popovertarget="site-theme-menu"',
    ):
        assert attribute in gear[0], attribute
    assert '<div class="site-theme-menu" id="site-theme-menu" popover role="menu"' in nav
    choices = re.findall(
        r'<button type="button" role="menuitemradio" aria-checked="false" tabindex="-1" '
        r'data-theme-choice="(\w+)">.*?<span>(\w+)</span>',
        nav,
    )
    assert choices == [("system", "System"), ("light", "Light"), ("dark", "Dark")]
    assert nav.index("site-theme") > nav.rindex('data-page="')


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_site_page_carries_the_theme_control(
    name: str, rendered: Callable[[str], str]
) -> None:
    page = rendered(name)
    script = render_overview.THEME_SCRIPT.read_text(encoding="utf-8")
    assert page.count('class="site-theme-button"') == 1
    assert script in page
    # kpress's own bootstrap applies the stored choice before first paint, and the
    # control stores into the key that bootstrap reads.
    assert 'stored("kpress.theme")' in page
    assert 'storageKey = "kpress.theme"' in script


SITE_NAV_BLOCK = re.compile(r'<nav class="site-nav" aria-label="Site">.*?</nav>', re.DOTALL)


def _the_bar(page: str, *, root: str) -> str:
    """The page's one navigation bar with its current mark and its root prefix taken out."""
    bars = SITE_NAV_BLOCK.findall(page)
    assert len(bars) == 1, "a page carries exactly one navigation bar"
    assert bars[0].count(' aria-current="page"') == 1, "the bar marks one page current"
    return bars[0].replace(' aria-current="page"', "").replace(f'href="{root}', 'href="')


def _workbench_page() -> str:
    """The workbench page as `build_site` gives it the bar, on its own template."""
    from workbench_tools import build_site  # noqa: PLC0415

    template = build_site.WORKBENCH_PACKAGE / "assets" / "template.html"
    return build_site.with_nav(template.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", [*sorted(render_overview.PAGES), "workbench/index.html"])
def test_every_site_page_carries_the_same_bar(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every page the Python build renders carries the bar byte for byte as the partial
    writes it, but for which item is current and the prefix that reaches the site's root."""
    assert name in render_overview.SITE_PAGES
    if name == "workbench/index.html":
        page, root = _workbench_page(), "../"
    else:
        page, root = rendered(name), ""
    partial = (
        render_overview.SITE_NAV.read_text(encoding="utf-8")
        .replace("{{ROOT}}", "")
        .replace("{{LOGO}}", render_overview.site_logo())
    )
    assert _the_bar(page, root=root) == SITE_NAV_BLOCK.findall(partial)[0]


def test_the_visualize_section_is_marked_current_on_both_its_pages(
    rendered: Callable[[str], str],
) -> None:
    """The bar's Visualize entry leads to the film and is current on the film's page and
    on the workbench, which share one tab bar with their own tab current."""
    nav = render_overview.nav_html("overview")
    assert '<a data-page="visualize" href="visualize.html">Visualize</a>' in nav
    assert "Visualizer" not in nav
    film = rendered("visualize.html")
    for page, root, tab in ((film, "", "film"), (_workbench_page(), "../", "workbench")):
        assert re.findall(r'<a data-page="(\w+)" aria-current="page"', page) == ["visualize"]
        tabs = render_overview.visualize_tabs(tab, root=root)
        assert page.count('class="site-tabs"') == 1
        assert tabs in page
        assert re.findall(r'<a data-tab="(\w+)" aria-current="page"', tabs) == [tab]
        # In the header slot, after the bar, on both pages alike.
        header = page.split('class="kpress-site-header"', 1)[1].split("</header>", 1)[0]
        assert header.index('class="site-nav"') < header.index(tabs)
    with pytest.raises(SystemExit):
        render_overview.visualize_tabs("stills")


def test_the_film_page_embeds_the_film_at_its_own_proportions(
    rendered: Callable[[str], str],
) -> None:
    """The film is inline with its controls, fetches nothing until played, and shows a
    poster at the video's own 16:9, so starting playback moves nothing."""
    page = rendered("visualize.html")
    video = re.search(r"<video [^>]*>", page)
    assert video is not None
    for attribute in (
        'class="site-film"',
        "controls",
        'preload="none"',
        "playsinline",
        'width="1920" height="1080"',
        'poster="ascent-n1-324-poster.png"',
    ):
        assert attribute in video[0], attribute
    assert f'<source src="{render_overview.FILM_URL}" type="video/mp4' in page
    assert page.index('class="site-tabs"') < page.index("<h1") < page.index("<video")


def test_no_site_stylesheet_keys_on_the_system_theme_alone() -> None:
    """An explicit Light or Dark choice must win over the system theme, so the site's
    styles key on kpress's resolved theme, never on `prefers-color-scheme`."""
    for sheet in (render_overview.SITE_CSS, render_overview.SITE_NAV_CSS, EXPLAINER_SHELL):
        assert "prefers-color-scheme" not in sheet.read_text(encoding="utf-8"), sheet.name


CARD = re.compile(
    r'<button type="button" class="site-card" popovertarget="([^"]+)" '
    r'data-go="(scroll|external|page)">'
)
ACTION = re.compile(
    r'<a class="site-popover-action" href="([^"]+)" data-go="(scroll|external|page)"'
)


def test_every_card_shows_where_it_goes_and_gets_there(page: str) -> None:
    """Every card opens a popover that shows its target and ends in one button that goes
    there. Another page is rendered in a frame, in its embedded view, and the button
    expands it; a place on this page, or another site, is previewed, and the button goes
    there; a row on another page, such as a result's on the results page, is previewed
    too, and the button goes to that page. The card's icon and the button's agree, and
    every target on the site exists.
    An other project's card is the exception, the link itself with no popover (its own
    test above)."""
    cards = CARD.findall(page)
    assert "page" in {kind for _, kind in cards} <= {"scroll", "page", "external"}
    assert page.count('class="site-card"') == len(cards)
    ids = set(ID.findall(page))
    rows = set(ID.findall(render_overview.results_page().html))
    served = {*render_overview.SITE_PAGES, "workbench/"}
    for target, kind in cards:
        start = page.index(f'<div class="site-popover" id="{target}" popover')
        # A card's panel ends where the next card begins, or the next popover: a table
        # row's popover, with a button of its own, can follow the section's last card.
        panel = re.split(
            r'<button type="button" class="site-card"|<div class="site-popover[ "]',
            page[start + 1 :],
            maxsplit=1,
        )[0]
        (action,) = ACTION.findall(panel)
        href, action_kind = action
        assert action_kind == kind == overview_sections.card_kind(href), target
        if kind == "scroll":
            assert 'class="site-popover-preview"' in panel, target
            assert href[1:] in ids, href
        elif kind == "external":
            assert 'class="site-popover-preview"' in panel, target
        elif 'class="site-popover-preview"' in panel:
            base, _, row = href.partition("#")
            assert base == render_overview.RESULTS_PAGE, href
            assert row in rows, href
            assert "<iframe" not in panel, target
        else:
            assert re.split(r"[?#]", href, maxsplit=1)[0] in served, href
            found = re.search(r'<iframe [^>]*src="([^"]+)"', panel)
            assert found is not None, target
            frame = html.unescape(found.group(1))
            assert frame == overview_sections.embed_url(href), target
            assert "view=embed" in frame, target


def test_an_embedded_page_keeps_its_query_and_fragment() -> None:
    embed = overview_sections.embed_url
    assert embed("explainer.html") == "explainer.html?view=embed"
    assert embed("frontier.html?recent=true") == "frontier.html?recent=true&view=embed"
    assert embed("frontier.html#n-21") == "frontier.html?view=embed#n-21"
    assert embed("workbench/") == "workbench/?view=embed"


CHIP = re.compile(r'<span class="site-chip( site-rung-fill)?"([^>]*)>([^<]+)</span>')


@pytest.mark.parametrize("name", ["index.html", "frontier.html", "all-results.html"])
def test_every_small_label_is_one_chip(name: str, rendered: Callable[[str], str]) -> None:
    """Rungs and case statuses share one chip; a rung chip carries its scale and level,
    which the stylesheet colours, and names the rung it shows."""
    html = rendered(name)
    chips = CHIP.findall(html)
    assert chips, name
    for fill, attributes, label in chips:
        if fill:
            assert f'data-rung="{label[0]}" data-level="{label[1:]}"' in attributes, label
    assert "site-rung " not in html
    assert "site-status-proved" not in html


def test_the_prose_links_repository_files_on_main(page: str) -> None:
    """Every `repo:` link in the template becomes a link on `main` to a file that exists."""
    from devtools.render_explainer import REPO  # noqa: PLC0415

    article = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    paths = re.findall(r'(?:\]\(|href=")repo:([^)"\s#]+)', article)
    assert paths
    assert 'href="repo:' not in page
    for path in paths:
        assert (REPO / path).exists(), path
        assert f'href="{repo_url(path)}"' in page, path


# ---------- What the page shares with the register's views (think-o0om) ----------


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return overview_data.load()


@pytest.fixture(scope="module")
def records() -> render_recent_results.Records:
    return render_recent_results.load_records()


def _row(page: str, result_id: str) -> str:
    match = re.search(rf'<tr id="{result_id.lower()}"[^>]*>.*?</tr>', page, re.DOTALL)
    assert match, result_id
    return match.group(0)


_DIV = re.compile(r"<(/?)div\b")


def _row_popover(page: str, target: str) -> str:
    """A row's popover, from its opening tag to the `</div>` that closes it."""
    start = page.index(f'<div class="site-popover site-row-pop" id="{target}" popover')
    depth = 0
    for match in _DIV.finditer(page, start):
        depth += -1 if match.group(1) else 1
        if depth == 0:
            return page[start : match.end() + 1]
    raise AssertionError(f"{target}: its popover never closes")


def test_every_result_shows_the_standing_readme_derives(
    page: str,
    results: str,
    overview: overview_data.Overview,
    records: render_recent_results.Records,
) -> None:
    """Standing is `render_recent_results.standing`, never restated: every table row
    carries it as an attribute and a chip, and only `current best` takes the accent."""
    for result in overview.results:
        expected = render_recent_results.standing(result.record, records)
        assert result.standing == expected, result.id
        row = _row(results, result.id)
        assert f'data-standing="{overview_sections.standing_key(expected)}"' in row, result.id
        assert overview_sections.standing_chip(expected) in row, result.id
    held = overview_sections.standing_chip(render_recent_results.HOLDS)
    assert 'data-tone="accent">current best</span>' in held
    for other in render_recent_results.STANDINGS[1:]:
        assert "data-tone" not in overview_sections.standing_chip(other), other
    recent = _recent_table(page)
    for result in overview_sections.recent_results(overview):
        row = _recent_row(recent, result.id)
        assert f'data-standing="{overview_sections.standing_key(result.standing)}"' in row
        assert overview_sections.standing_chips(result.standing) in row, result.id


def _recent_row(table: str, result_id: str) -> str:
    match = re.search(rf'<tr data-result="{result_id.lower()}"[^>]*>.*?</tr>', table, re.DOTALL)
    assert match, result_id
    return match.group(0)


def _recent_table(page: str) -> str:
    """The recent table as the page carries it, after kpress has wrapped it and labelled
    its cells, from its opening tag to its close."""
    match = re.search(
        r'<table class="kpress-table site-table site-results site-recent-table">.*?</table>',
        page,
        re.DOTALL,
    )
    assert match
    return match.group(0)


def test_recent_results_is_one_table_not_cards_or_a_list(
    page: str, overview: overview_data.Overview
) -> None:
    """The section is one `.site-table` of the recent results, one row each, with the
    date, the result linking its row, the method, the credit and the status chips; no
    card or list is left in it, and its only popovers are its rows' own."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    recent = _recent_table(page)
    assert recent in section
    before_replay = section.split("site-replay", 1)[0]
    assert not re.search(r'class="site-card[ "]', before_replay)
    assert set(re.findall(r'<div class="(site-popover[^"]*)"', before_replay)) == {
        "site-popover site-row-pop"
    }
    assert "<li>" not in before_replay
    assert section.count("<table") == 2  # the recent table, then the replay table
    assert 'class="kpress-table site-table site-results site-recent-table"' in recent
    assert "data-site-table" not in recent
    heads = re.findall(r"<th[^>]*>([^<]+)</th>", recent.split("</thead>", 1)[0])
    assert heads == ["Date", "Result", "Method", "Credit", "Status"]
    newest = overview_sections.recent_results(overview)
    assert re.findall(r'<tr data-result="(t-\d+)"', recent) == [r.id.lower() for r in newest]
    for result in newest:
        row = _recent_row(recent, result.id)
        cells = re.findall(r'<td class="(site-col-[a-z]+)"', row)
        assert cells == [
            f"site-col-{c}" for c in ("date", "result", "method", "credit", "status")
        ]
        assert f'<a href="all-results.html#{result.id.lower()}">' in row
        # The quiet id is the row's native trigger, which opens its popover unscripted.
        assert (
            '<span class="site-cell-quiet"><button type="button" class="site-row-open" '
            f'popovertarget="pop-result-{result.id.lower()}">{result.id}</button></span>'
        ) in row
        status = row.split('<td class="site-col-status"', 1)[1]
        # Every chip in the one status cell, side by side: V, C and S, then the standing.
        chips = re.findall(r'<span class="site-chip[^"]*"[^>]*>([^<]+)</span>', status)
        record = result.record
        assert chips[:3] == [
            record["verification"],
            record["confirmation"],
            f"S{record['significance']['score']}",
        ]
        assert "<br" not in status
        assert "site-standing" not in status
    # Evan Daniel's three exact values, the closures the exact-value cards used to show.
    exact = {n for n in overview.recent_lower if overview.cases[n]["status"] == "proved"}
    shown = {r.first_n for r in newest}
    assert exact <= shown


def test_the_recent_table_lists_every_result_since_august_filtered_to_s4(
    page: str, overview: overview_data.Overview
) -> None:
    """Every result dated on or after 1 August 2026 is a row, and none before it; the
    Significance filter starts at S4 and up, with the rows below it hidden in the HTML
    and the count already written, so the first paint is the filtered table."""
    assert overview_sections.RECENT_FROM.isoformat() == "2026-08-01"
    since = [r for r in overview.results if r.dated[1] >= "2026-08-01"]
    before = [r for r in overview.results if r.dated[1] < "2026-08-01"]
    assert before, "the floor should leave older results to the results page"
    recent = _recent_table(page)
    listed = re.findall(r'<tr data-result="(t-\d+)"', recent)
    assert sorted(listed) == sorted(r.id.lower() for r in since)
    assert not {r.id.lower() for r in before} & set(listed)
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    tools = _filter_bar(section)
    assert section.index(tools) < section.index(recent)
    assert '<label>Significance <select data-filter="s" data-bound="min">' in tools
    significance = tools.split('data-filter="s"', 1)[1].split("</select>", 1)[0]
    options = re.findall(r'<option value="(\d?)"( selected)?>([^<]+)</option>', significance)
    assert ("4", " selected", "S4 and up") in options
    assert ("3", "", "S3 and up") in options
    assert options[0] == ("", "", "All")
    shown = 0
    for result in since:
        row = _recent_row(recent, result.id)
        score = result.record["significance"]["score"]
        assert f'data-s="{score}"' in row, result.id
        assert (" hidden>" in row.split(">", 1)[0] + ">") == (score < 4), result.id
        shown += score >= 4
    assert 0 < shown < len(since)
    assert f"{shown} of {len(since)} results</span>" in tools
    text = re.sub(r"<[^>]+>", "", section)
    assert "every result since 1 August 2026" in text
    assert "It starts filtered to significance S4 and up; choose All to see every row." in text


def test_the_recent_table_splits_method_credit_and_standing() -> None:
    split = overview_sections.split_summary
    assert split("`s(21) = 5` by a point-only route, reported") == (
        "`s(21) = 5`",
        "point-only route",
    )
    assert split("`s(45) = 7`, by a mixed cover of points and grid-line segments") == (
        "`s(45) = 7`",
        "mixed cover of points and grid-line segments",
    )
    assert split("`s(50) ≥ 37/5 = 7.4`, reported") == ("`s(50) ≥ 37/5 = 7.4`", "")
    batch = "`s(27), s(28) ≥ 28/5`, `s(31) ≥ 148/25` and `s(32) ≥ 119/20`"
    assert split(batch) == (batch, "")
    credit = overview_sections.credit_cell("wand125 after Daniel, Tokoharu, Levy, Stromquist")
    assert (
        credit == 'wand125 <span class="site-cell-quiet">after Daniel, Tokoharu, Levy, …</span>'
    )
    assert overview_sections.credit_cell("This project") == "This project"
    chips = overview_sections.standing_chips("second certificate, reported")
    assert chips.count('class="site-chip"') == 2
    assert (
        overview_sections.standing_chips(render_recent_results.NOT_A_BOUND).count("site-chip")
        == 1
    )
    held = overview_sections.standing_chips("current best, reported")
    assert 'data-tone="accent">current best</span>' in held
    assert 'data-standing="reported">reported</span>' in held


def test_only_t060_of_the_s5_results_still_holds(overview: overview_data.Overview) -> None:
    s5 = [r for r in overview.results if r.record["significance"]["score"] >= 5]
    holding = {r.id for r in s5 if r.standing == render_recent_results.HOLDS}
    # The audit's reading of the record; update it when the record moves on. T-060's
    # exact n = 11 value superseded T-037's 31/8.
    assert holding == {"T-060"}


def _lead_candidate(
    result_id: str, score: int, published: str, standing: str
) -> overview_data.Result:
    record = {
        "id": result_id,
        "headline": f"Result {result_id}",
        "verification": "V4",
        "confirmation": "C3",
        "significance": {"score": score},
        "attribution": {"published": published},
    }
    return overview_data.Result(
        record, group="", credit="A. Source", ours=False, standing=standing
    )


def test_the_recent_lead_is_chosen_by_the_register_not_typed() -> None:
    """The lead is the highest significance among recent results that are the current
    best, the newest of equals: a newer superseded S5 result, a newer S4 one that holds,
    and an S5 one from before the recent window all lose to the newest S5 that holds."""
    holds, superseded = render_recent_results.HOLDS, render_recent_results.SUPERSEDED
    candidates = [
        _lead_candidate("T-901", 5, "2026-09-01", holds),
        _lead_candidate("T-902", 5, "2026-09-10", holds),
        _lead_candidate("T-903", 5, "2026-09-20", superseded),
        _lead_candidate("T-904", 4, "2026-09-25", holds),
        _lead_candidate("T-905", 5, "2026-07-01", holds),
    ]
    overview = overview_data.Overview(
        results=candidates, cases={}, recent_lower=frozenset(), groups=[]
    )
    lead = overview_sections.lead_result(overview)
    assert lead is not None
    assert lead.id == "T-902"
    line = overview_sections.recent_lead(overview)
    assert '<a href="all-results.html#t-902">Result T-902</a>' in line
    nobody = overview_data.Overview(
        results=candidates[2:3], cases={}, recent_lower=frozenset(), groups=[]
    )
    assert overview_sections.lead_result(nobody) is None
    assert overview_sections.recent_lead(nobody) == ""


def test_the_recent_lead_names_t060_above_the_table(
    page: str, overview: overview_data.Overview
) -> None:
    """On today's register the lead is T-060, with its headline linking its row, its id,
    its credit and its chips, set between the section's prose and the recent table."""
    holding = [
        r
        for r in overview_sections.recent_results(overview)
        if r.standing == render_recent_results.HOLDS
    ]
    expected = max(holding, key=lambda r: (overview_sections.significance(r), r.dated[1], r.id))
    lead = overview_sections.lead_result(overview)
    assert lead is not None
    assert lead is expected
    # The audit's reading of the record; update it when the record moves on.
    assert lead.id == "T-060"
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    match = re.search(r'<p class="site-recent-lead">.*?</p>', section, re.DOTALL)
    assert match
    line = match.group(0)
    assert section.index(line) < section.index(_recent_table(page))
    assert '<a href="all-results.html#t-060">' in line
    assert '<span class="site-cell-quiet">T-060</span>' in line
    assert "Queuingtheorydotcom" in line
    chips = re.findall(r'<span class="site-chip[^"]*"[^>]*>([^<]+)</span>', line)
    assert chips == ["V4", "C5", "S5", render_recent_results.HOLDS]


def test_the_problem_section_says_eleven_squares_is_settled(page: str) -> None:
    """The problem section names T-060 and case 11, and the template is in the reader
    tier, so the gate refuses a result it names that the register does not hold."""
    from devtools import check_results  # noqa: PLC0415

    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    text = re.sub(r"<[^>]+>", "", problem)
    assert "Trump\u2019s 1979" in text
    assert "packing is optimal" in text
    assert '<a href="all-results.html#t-060">T-060</a>' in problem
    assert '<a href="cases.html#n-11">case 11</a>' in problem
    assert render_overview.OVERVIEW_ARTICLE in check_results.READER_TIER


def test_the_explainer_card_names_the_earlier_bound_it_proves(page: str) -> None:
    """The explainer proves T-026's historical bound, so its card says so, with the bound
    the explainer itself states cut to the card's four places and set as math."""
    from devtools.render_explainer import current_bound_facts  # noqa: PLC0415

    card = page.split('popovertarget="pop-page-explainer"', 1)[1].split("</button>", 1)[0]
    assert "Earlier " in card
    assert "lower bounds" in card
    assert "before T-060 settled the case" in card
    assert current_bound_facts().bounded_side_decimal.startswith("3.8264")
    note = card.split('class="site-card-note">', 1)[1]
    assert "kpress-math" in note
    assert "3.8264" in note
    assert "&gt;=" not in note


def test_the_film_note_says_the_films_predate_t060(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The films were cut before T-060, so the film page says what they show at n = 11,
    dated from the release; a film cut after T-060 fails here until the note goes."""
    from datetime import datetime  # noqa: PLC0415

    from sqpack.release import PUBLICATION_HISTORY  # noqa: PLC0415

    page = rendered("visualize.html")
    assert render_overview.film_release_date() == "28 September"
    text = re.sub(r"<[^>]+>", "", page)
    assert (
        "Both predate T-060, so at n = 11 they show the lower bound of 28 September, "
        "not the proved value." in text
    )
    assert '<a href="all-results.html#t-060">T-060</a>' in page
    release = next(e for e in PUBLICATION_HISTORY if e.version == render_overview.FILM_RELEASE)
    released = datetime.strptime(release.first_published, "%B %d, %Y").date()  # noqa: DTZ007
    t060 = next(r for r in register if r["id"] == "T-060")
    assert released.isoformat() < str(t060["registered"])


def test_the_standing_filter_offers_each_standing_on_the_page(
    results: str, overview: overview_data.Overview
) -> None:
    tools = re.search(r'<select data-filter="standing">(.*?)</select>', results, re.DOTALL)
    assert tools
    offered = re.findall(r'<option value="([^"]*)"[^>]*>', tools.group(1))
    present = {overview_sections.standing_key(r.standing) for r in overview.results}
    assert offered[0] == ""
    assert set(offered[1:]) == present


def test_the_survey_counts_are_readmes(page: str, overview: overview_data.Overview) -> None:
    counts = render_recent_results.recent_counts(render_recent_results.recent_rows())
    assert overview.counts == counts
    sentence = overview_sections.survey_counts(overview)
    for number in counts:
        assert f" {number} " in sentence, number
    text = re.sub(r"<[^>]+>", "", page)
    assert f"{counts.cases} have a lower bound published or proved since 22 August 2026" in text


def test_reported_bounds_awaiting_replay_are_listed(
    page: str, overview: overview_data.Overview
) -> None:
    """Every recent case whose reported lane differs from the verified one has a row
    linking its frontier record, with the reported value set as math, not code."""
    waiting = [row.n for row in overview.recent if row.shows_reported]
    assert waiting
    assert waiting == [row.n for row in overview.awaiting_replay]
    block = overview_sections.awaiting_replay(overview)
    assert '<details class="site-wide site-replay">' in page
    for n in waiting:
        assert f'<tr id="replay-n-{n}"' in page, n
    listed = [int(n) for n in re.findall(r'<tr id="replay-n-(\d+)"', block)]
    assert sorted(listed) == waiting
    for n in waiting:
        assert f'<a href="frontier.html#n-{n}">{n}</a>' in block, n
    assert "`" not in block
    assert "<code>" not in block
    assert {18, 19, 20} <= set(listed)
    # n = 11 reports T-060 rounded, and T-060 is verified: nothing awaits (think-pd2g).
    assert 11 not in listed
    eighteen = re.search(r'<tr id="replay-n-18".*?</tr>', block, re.DOTALL)
    assert eighteen
    assert "939/200" in eighteen.group(0)
    assert "kpress-math" in eighteen.group(0)
    assert "wand125" in block


def test_results_by_others_show_their_publication_date(
    results: str, overview: overview_data.Overview
) -> None:
    for result in overview.results:
        row = _row(results, result.id)
        attribution = result.record.get("attribution")
        if attribution:
            published = str(attribution["published"])
            assert result.dated == ("published", published)
            assert f'<span class="site-date-kind">published</span> {published}' in row
        else:
            assert result.dated[0] == "established"
    recent = overview_sections.recent_table(overview)
    dates = re.findall(r'<span class="site-date-kind">(\w+)</span> ([\d-]+)</td>', recent)
    assert dates
    assert [d for _, d in dates] == sorted((d for _, d in dates), reverse=True)
    assert max(r.dated[1] for r in overview.results) == dates[0][1]


def test_grouping_agrees_with_readmes_relation(
    overview: overview_data.Overview, records: render_recent_results.Records
) -> None:
    """The table's groups are `source_lineage`'s, the lineage `render_recent_results.relation`
    names, so wand125's T-048, T-054 and T-055 read as crediting this project
    second-hand in both."""
    titles = dict(OTHERS)
    for title, members in overview.groups[1:]:
        for result in members:
            lineage = source_lineage(result.record, records.sources)
            assert titles[lineage] == title, result.id
            if render_recent_results.is_recent_by_others(result.record):
                relation = render_recent_results.relation(result.record, records)
                assert render_recent_results.LINEAGES[str(lineage)] == relation, result.id
    group = {r.id: title for title, members in overview.groups for r in members}
    for result_id in ("T-048", "T-054", "T-055"):
        assert group[result_id] == "Crediting this project second-hand", result_id
        relation = render_recent_results.relation(records.results[result_id], records)
        assert relation == "credits second-hand", result_id


def test_each_row_detail_names_its_novelty_label(
    results: str, overview: overview_data.Overview
) -> None:
    """The novelty label is in the detail a row opens, its popover, not in a cell."""
    labels = overview_sections.novelty_labels()
    assert labels["apparently-novel"].startswith("Not found in the recorded search")
    assert labels["confirmed-novel"].startswith("Priority confirmed")
    for result in overview.results:
        chip = (
            f'<dt>Novelty</dt><dd><span class="site-chip" data-novelty="{result.novelty}">'
            f"{result.novelty}</span> {html.escape(labels[result.novelty])}</dd>"
        )
        assert chip in _row_popover(results, f"pop-result-{result.id.lower()}"), result.id
        assert "<dt>" not in _row(results, result.id), result.id


def test_the_page_title_style_is_upright() -> None:
    """KPress sets `h2` in italic; the title style, which the homepage's first `h2` takes
    through `site-title`, overrides it, so it reads as the frontier atlas's `h1` does."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index(".site-hero h1,\n.kpress .site-title {") :]
    assert "font-style: normal;" in rule[: rule.index("}")]


def test_the_bar_sits_close_to_the_top_of_every_page() -> None:
    """The space above the bar is kpress's page top margin, narrowed once in the stylesheet
    every page carries, so the explainer, the KPress pages and the workbench all agree."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--kpress-page-margin-block-start: 1rem;" in css


def test_the_gear_sits_level_with_the_tab_text() -> None:
    """The gear's centre is set at the middle of the tab text's capitals by one token, on
    every page and at every width, rather than at the middle of the bar's row."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--site-gear-drop: 0.11em;" in css
    assert "translate: 0 var(--site-gear-drop);" in css


def test_every_page_starts_one_shared_space_below_the_bar() -> None:
    """The space from the bar's rule to a page's first block is one token, declared in the
    stylesheet every page carries and read by the site's column and the explainer's hero."""
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert "--site-page-top: 3rem;" in nav
    assert "padding-block-start: var(--site-page-top);" in render_overview.SITE_CSS.read_text(
        encoding="utf-8"
    )
    shell = (render_overview.TEMPLATES / "explainer-shell.html").read_text(encoding="utf-8")
    assert "padding-block-start: var(--site-page-top);" in shell


def test_an_opening_picture_sits_one_token_nearer_the_bar() -> None:
    """The homepage's packing opens the page a token nearer the bar than a title does."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-hero-lift: 0.5rem;" in css
    assert "margin-block-start: calc(-1 * var(--site-hero-lift));" in css


def test_section_headings_share_one_space_above() -> None:
    """The space above an `h2` is one token in the text layer both the site and the
    explainer read, narrower on screen than in print."""
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert "--paper-section-space: calc(var(--kpress-font-size-base) * 1.8);" in text
    shell = (render_overview.TEMPLATES / "explainer-shell.html").read_text(encoding="utf-8")
    for css in (render_overview.SITE_CSS.read_text(encoding="utf-8"), shell):
        assert "margin-block: var(--paper-section-space) 1.3rem;" in css


def test_the_icon_frame_is_one_pixel_at_icon_size() -> None:
    """The logo and the favicon draw case 11's container as one whole pixel at the size
    each is shown, with its outer edge on the drawing's edge: (200 + w) / px = w."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    for px in (render_overview.SITE_LOGO_PX, render_overview.FAVICON_PX):
        svg = packing_svg(11, units=200, frame_px=px)
        view = re.search(r'viewBox="([^"]+)"', svg)
        stroke = re.search(r'<rect [^>]*stroke-width="([\d.]+)"', svg)
        assert view is not None
        assert stroke is not None
        box = [float(v) for v in view.group(1).split()]
        width = float(stroke.group(1))
        assert box[2] / px == pytest.approx(width, abs=1e-3)
        assert box[0] == pytest.approx(-width / 2, abs=1e-3)
        assert 'shape-rendering="crispEdges"' in svg
        lines = re.search(r'<g stroke="[^"]+" stroke-width="([\d.]+)"', svg)
        assert lines is not None
        assert float(lines.group(1)) == pytest.approx(width / 2, abs=1e-3)
    assert "block-size: 18px;" in render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert render_overview.SITE_LOGO_PX == 18


def test_page_subtitles_share_one_size() -> None:
    """Every hero's subtitle ("The ascent, n = 1 to 324") is set from one scale of the sans
    base, a small step above it."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-subtitle-scale: 1.1;" in css
    rule = css[css.index(".kpress .site-hero .subtitle {") :]
    assert "var(--site-subtitle-scale)" in rule[: rule.index("}")]


def test_wrapped_chips_never_touch() -> None:
    """Chips wrap like words; every chip carries a block margin, so a wrapped row keeps a
    gap from the row above wherever chips sit."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index(".site-chip {") :]
    assert "margin-block: 0.15rem;" in rule[: rule.index("}")]


def test_the_atlas_stepper_draws_one_arrow_mirrored() -> None:
    """Both stepper arrows are the site's one arrow, left and right, never the arrow
    characters, which the site's face lacks and browsers draw from mismatched fallbacks."""
    popover = overview_sections.atlas_popover()
    step = popover[popover.index('<span class="site-atlas-pop-step">') :]
    step = step[: step.index("</span></p>")]
    assert not ARROW_CHARACTERS.search(step)
    assert step.count(overview_sections.arrow_icon("right")) == 1
    assert step.count(overview_sections.arrow_icon("left")) == 1
    assert overview_sections.step_arrow(back=True) == overview_sections.arrow_icon("left")


#: Every arrow a typed character could draw, as characters and as CSS or HTML escapes.
ARROW_CHARACTERS = re.compile(
    r"[\u2190-\u21ff\u27f0-\u27ff\u2b00-\u2b0d\u2b60-\u2bff]"
    r"|\\21[9a-f][0-9a-f]|\\u21[9a-f][0-9a-f]|&(?:[lrudh]arr|nearr|varr);|&#x?21[9a-f]",
    re.IGNORECASE,
)


class _VisibleText(html.parser.HTMLParser):
    """The text a reader sees: no styles, scripts, math, or code."""

    SKIP = frozenset({"style", "script", "math", "code", "pre", "svg"})

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:  # noqa: ARG002
        if tag in self.SKIP:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.depth:
            self.parts.append(data)


def _visible_text(page: str) -> str:
    parser = _VisibleText()
    parser.feed(page)
    return "".join(parser.parts)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_no_arrow_on_a_site_page_is_a_typed_character(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every arrow a site page shows is the one drawn icon set. The one exception is a
    repository document's own prose, where its author writes an arrow as notation
    (`experiment → series` in conventions.md): its article may show no more arrows than
    its Markdown source has, and the page around the article none."""
    from devtools.site_documents import DOCUMENTS  # noqa: PLC0415

    page = rendered(name)
    sources = {doc.name: doc.source for doc in DOCUMENTS}
    if name in sources:
        body = re.search(r"<article\b.*?</article>", page, re.DOTALL)
        assert body is not None, name
        written = len(ARROW_CHARACTERS.findall(sources[name].read_text(encoding="utf-8")))
        assert len(ARROW_CHARACTERS.findall(_visible_text(body.group(0)))) <= written, name
        page = page.replace(body.group(0), "")
    assert not ARROW_CHARACTERS.findall(_visible_text(page)), name


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_every_arrow_icon_comes_from_the_one_set(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Every inline arrow is `arrow_icon`'s markup, hidden from assistive technology, and
    no page draws an arrow of its own."""
    page = rendered(name)
    icons = re.findall(r"<span class=\"site-icon-arrow\"[^>]*></span>", page)
    allowed = {overview_sections.arrow_icon(d) for d in overview_sections.ARROW_DIRECTIONS}
    assert set(icons) <= allowed, name
    assert 'class="site-arrow' not in page


def test_the_icon_set_is_one_drawing_in_the_stylesheet() -> None:
    """The stylesheet draws every arrow from `--site-arrow` (and the sort pair), declared
    once, and no generated content or site script is an arrow character."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    assert css.count("--site-arrow: url(") == 1
    assert css.count("--site-arrow-sort: url(") == 1
    assert "--site-arrow" not in nav
    for content in re.findall(r"content:\s*([^;]+);", css):
        assert not ARROW_CHARACTERS.search(content), content
    for mask in re.findall(r"mask(?:-image)?:\s*([^;]+);", css):
        assert re.match(r"var\(--site-arrow(?:-sort)?\)", mask), mask
    scripts = (render_overview.PACKING / "devtools" / "overview").glob("*.js")
    for script in scripts:
        assert not ARROW_CHARACTERS.search(script.read_text(encoding="utf-8")), script.name
    assert not ARROW_CHARACTERS.search(
        render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    )
    with pytest.raises(ValueError, match="unknown arrow direction"):
        overview_sections.arrow_icon("sideways")


#: The stylesheets that carry every hover on the site.
_HOVER_SHEETS = (
    render_overview.SITE_CSS,
    render_overview.SITE_NAV_CSS,
    EXPLAINER_SHELL,
)


def test_every_hover_runs_on_the_one_motion_token() -> None:
    """One timing for every hover, declared once where every page reads it, 120 to 150ms
    ease-out and instant under reduced motion; no transition names its own time or
    transitions `all`."""
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    duration = re.findall(r"--site-hover-duration:\s*(\d+)ms;", nav)
    assert [int(d) for d in duration] == [140, 0]
    assert "--site-hover-easing: ease-out;" in nav
    timing = "var(--site-hover-duration) var(--site-hover-easing)"
    assert f"--kpress-transition-fast: {timing};" in nav
    for sheet in _HOVER_SHEETS:
        text = sheet.read_text(encoding="utf-8")
        assert "--site-hover-duration:" not in text or sheet == render_overview.SITE_NAV_CSS
        for value in re.findall(r"transition:\s*([^;]+);", text):
            assert not re.search(r"\d(?:m?s)\b", value), (sheet.name, value)
            assert not re.search(r"\ball\b", value), (sheet.name, value)
            if value.strip() != "none":
                assert "var(--site-hover-duration) var(--site-hover-easing)" in value, value


def test_every_popover_shares_one_margin_and_close_target() -> None:
    """Popover margins are one token on all four sides, and the close cross is one square
    tap target set in from the corner by another."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    popover = css[css.index(".site-popover {") :]
    assert "padding: var(--site-popover-pad);" in popover[: popover.index("}")]
    close = css[css.index(".site-popover .site-popover-close {") :]
    close = close[: close.index("}")]
    for token in ("--site-popover-close)", "--site-popover-close-inset)"):
        assert f"var({token}" in close


def test_popover_headlines_set_their_math_serif() -> None:
    """Every popover's headline is marked for serif mathematics, and no popover forces sans
    mathematics on everything inside it."""
    card = overview_sections.atlas_popover()
    assert 'data-math-face="serif" id="pop-atlas-title"' in card
    assert "data-kpress-prose-font" not in card.split(">", 1)[0]
    shell = (
        render_overview.PACKING
        / "devtools"
        / "probes"
        / "render_explainer"
        / "host_math_init.js"
    ).read_text(encoding="utf-8")
    assert "closest('[data-math-face=\"serif\"]')" in shell


TABLE_BLEED = (
    ".site-page .site-wide:is(.site-table-wrap, :has(> .site-table-wrap)):not(.site-replay) {"
)


def test_data_tables_bleed_like_the_atlas_only_above_1280_pixels() -> None:
    """A data table's wide track is one rule on shared tokens. It stops at its own
    maximum, short of the atlas grid's, and its growth term is zero at or below
    `--site-table-bleed-from` (80rem), so a table at 1280 pixels or narrower keeps the
    plain wide track."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-bleed-max: 140rem;" in css
    assert "--site-table-bleed-from: 80rem;" in css
    grid = css[css.index(".site-page .site-atlas-grid {") :]
    assert "--site-wide: var(--site-bleed-max);" in grid[: grid.index("}")]
    rule = css[css.index(TABLE_BLEED) :]
    rule = rule[: rule.index("\n}")]
    assert "--site-table-max: 100rem;" in css
    assert "var(--site-table-max)," in rule
    assert "--site-table-grow: max(0px, 100vw - var(--site-table-bleed-from));" in rule
    assert "calc(var(--site-wide) + var(--site-table-grow))" in rule
    assert "max-width: var(--site-table-wide);" in rule


class _TableAncestry(HTMLParser):
    """Each `<table>`'s own classes and the classes of the elements around it."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, str]] = []
        self.tables: list[tuple[str, list[str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class") or ""
        if tag == "table":
            # KPress's own table wrap, where it adds one, is not the site's.
            around = [c for _, c in reversed(self.stack) if c != "kpress-table-wrap"]
            self.tables.append((classes, around))
        if tag in {"div", "details", "section", "table"}:
            self.stack.append((tag, classes))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def test_every_data_table_is_the_shared_component(page: str, results: str) -> None:
    """Every `.site-table` on the overview, the results page and the frontier atlas is a
    KPress table directly in a `.site-table-wrap`, and every one that fills its track is
    in a `.site-wide` the bleed rule takes (the wrap itself, or its parent). Only the
    compact replay table keeps to its content, and it is the rule's one exclusion."""
    from devtools.render_frontier_page import frontier_cases, table_html  # noqa: PLC0415

    seen = 0
    for text in (page, results, table_html(frontier_cases())):
        parser = _TableAncestry()
        parser.feed(text)
        for classes, around in parser.tables:
            if "site-table" not in classes.split():
                continue
            seen += 1
            assert "kpress-table" in classes.split()
            wrap = around[0].split()
            parent = around[1].split() if len(around) > 1 else []
            assert "site-table-wrap" in wrap, classes
            if "site-replay-table" in classes.split():
                assert "site-replay" in parent
            else:
                assert "site-wide" in wrap or "site-wide" in parent, classes
    assert seen >= 3


# ---------- Row popovers: the row is the unit (think-br9e) ----------

#: The pages whose tables have rows with detail.
ROW_PAGES = ("index.html", "all-results.html", "frontier.html")


class _RowWiring(HTMLParser):
    """What ties a page's table rows to their popovers: every body row of a `.site-table`
    that is not a group heading, with the triggers in its cells; every row popover, with
    whether it sits inside a table; how many cells the page has and how many `<details>`
    sit inside one; and how often each id occurs.
    """

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[dict[str, str | None], list[str | None]]] = []
        self.popovers: dict[str, dict[str, str | None]] = {}
        self.inside_tables: list[str] = []
        self.cells = 0
        self.cell_details = 0
        self.ids: Counter[str] = Counter()
        self.closers: Counter[str] = Counter()
        self._depth = {"table": 0, "tbody": 0, "td": 0, "th": 0}
        self._site_table = False
        self._row: list[str | None] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        found = dict(attrs)
        classes = (found.get("class") or "").split()
        if found.get("id"):
            self.ids[str(found["id"])] += 1
        if tag in self._depth:
            self._depth[tag] += 1
        if tag == "table":
            self._site_table = "site-table" in classes
        elif tag in {"td", "th"}:
            self.cells += 1
        elif tag == "tr":
            self._row = None
            if self._site_table and self._depth["tbody"] and "site-group-row" not in classes:
                self._row = []
                self.rows.append((found, self._row))
        elif tag == "button" and "site-row-open" in classes and self._row is not None:
            self._row.append(found.get("popovertarget"))
        elif tag == "button" and "site-popover-close" in classes:
            hides = found.get("popovertargetaction") == "hide"
            self.closers[str(found.get("popovertarget"))] += int(hides)
        elif tag == "details" and (self._depth["td"] or self._depth["th"]):
            self.cell_details += 1
        elif tag == "div" and "site-row-pop" in classes:
            self.popovers[str(found.get("id"))] = found
            if self._depth["table"]:
                self.inside_tables.append(str(found.get("id")))

    def handle_endtag(self, tag: str) -> None:
        if tag in self._depth:
            self._depth[tag] -= 1
        if tag == "tr":
            self._row = None
        elif tag == "table":
            self._site_table = False


@functools.cache
def _row_wiring(name: str) -> _RowWiring:
    parser = _RowWiring()
    parser.feed(_rendered(name))
    return parser


@pytest.mark.parametrize("name", ROW_PAGES)
def test_no_table_cell_expands_on_its_own(name: str) -> None:
    """No `<td>` or `<th>` on a page with a site table holds a `<details>`: a row's
    detail is its popover. The replay table's own disclosure wraps the whole table."""
    wiring = _row_wiring(name)
    assert wiring.rows, name
    assert wiring.cells > len(wiring.rows), name
    assert wiring.cell_details == 0, name


@pytest.mark.parametrize("name", ROW_PAGES)
def test_every_row_with_detail_is_wired_to_one_popover(name: str) -> None:
    """Every body row of every site table names one popover, has an accessible name, and
    carries exactly one native trigger for that popover, so it opens without scripts.
    The popover is on the page once, outside every table, a dialog labelled by its own
    headline, with a close cross of its own; no popover is left without a row.
    A row carries no `tabindex`: `row-popover.js` makes it focusable when it takes the
    trigger out of the tab order, so without scripts the trigger is the one stop."""
    wiring = _row_wiring(name)
    targets = []
    for attributes, triggers in wiring.rows:
        target = attributes.get("data-row-popover")
        assert target, attributes
        assert attributes.get("aria-label"), target
        assert "tabindex" not in attributes, target
        assert triggers == [target], target
        targets.append(target)
    assert len(targets) == len(set(targets)), name
    assert set(targets) == set(wiring.popovers), name
    assert not wiring.inside_tables, name
    for target, popover in wiring.popovers.items():
        assert wiring.ids[target] == 1, target
        assert "popover" in popover, target
        assert (popover.get("class") or "").split()[0] == "site-popover", target
        assert popover.get("role") == "dialog", target
        assert popover.get("aria-labelledby") == f"{target}-title", target
        assert wiring.ids[f"{target}-title"] == 1, target
        assert wiring.closers[target] == 1, target


def test_the_tables_with_row_detail_are_the_ones_named(
    overview: overview_data.Overview,
) -> None:
    """The recent table and the replay table on the overview, the results table on its
    page and the frontier atlas: each row's popover is its own, by its key."""
    from devtools.render_frontier_page import frontier_cases  # noqa: PLC0415

    recent = {f"pop-result-{r.id.lower()}" for r in overview_sections.recent_results(overview)}
    replay = {f"pop-replay-n-{row.n}" for row in overview.awaiting_replay}
    assert recent
    assert replay
    assert set(_row_wiring("index.html").popovers) == recent | replay
    assert set(_row_wiring("all-results.html").popovers) == {
        f"pop-result-{r.id.lower()}" for r in overview.results
    }
    assert set(_row_wiring("frontier.html").popovers) == {
        f"pop-frontier-n-{case['n']}" for case in frontier_cases()
    }


@pytest.mark.parametrize("name", ROW_PAGES)
def test_a_page_with_row_detail_carries_the_row_and_popover_scripts(
    name: str, rendered: Callable[[str], str]
) -> None:
    """The row script makes the row the control, and the popover script typesets a
    popover's math when it opens and closes it when a link inside is followed."""
    page = rendered(name)
    assert render_overview.ROW_POPOVER_SCRIPT.read_text(encoding="utf-8") in page
    assert render_overview.POPOVER_SCRIPT.read_text(encoding="utf-8") in page
    assert render_overview.TABLE_SCRIPT.read_text(encoding="utf-8") in page


def test_a_result_rows_popover_body_comes_from_one_function(
    overview: overview_data.Overview, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`result_row_popover_body` is the one source of a result row's detail, on the
    overview's recent table and on the results page alike: whatever it returns is the
    body of that row's popover, once, and no cell of the row repeats it."""
    result = overview_sections.recent_results(overview)[0]
    body = overview_sections.result_row_popover_body(result, overview)
    assert body.startswith('<dl class="site-detail"><dt>Claim</dt>')
    for term in ("<dt>Significance</dt>", "<dt>Novelty</dt>"):
        assert term in body

    def marked(result: overview_data.Result, _: overview_data.Overview) -> str:
        return f"<p>BODY OF {result.id}</p>"

    monkeypatch.setattr(overview_sections, "result_row_popover_body", marked)
    for table, listed in (
        (overview_sections.results_table(overview), overview.results),
        (overview_sections.recent_table(overview), overview_sections.recent_results(overview)),
    ):
        assert "<dt>Claim</dt>" not in table
        for row in listed:
            target = f"pop-result-{row.id.lower()}"
            marker = f'<div class="site-row-pop-body"><p>BODY OF {row.id}</p></div>'
            assert table.count(marker) == 1, row.id
            assert marker in _row_popover(table, target), row.id


def test_a_result_row_popover_leads_to_its_row_only_from_another_page(
    overview: overview_data.Overview,
) -> None:
    """A result's popover is the same panel on both pages, a card's: the id as its caps
    label and the summary as its headline. On the overview it ends in the button to the
    result's row on the results page; on that page, where the row is the one pressed,
    it has no button."""
    result = overview_sections.recent_results(overview)[0]
    target = f"pop-result-{result.id.lower()}"
    away = _row_popover(overview_sections.recent_table(overview), target)
    here = _row_popover(overview_sections.results_table(overview), target)
    for panel in (away, here):
        assert f'<span class="site-card-label">{result.id}</span>' in panel
        assert (
            f'<p class="site-popover-value" data-math-face="serif" id="{target}-title">'
            in panel
        )
        assert 'popovertargetaction="hide" aria-label="Close">' in panel
    (action,) = ACTION.findall(away)
    assert action == (f"all-results.html#{result.id.lower()}", "page")
    assert f"Open {result.id} in the results table</a>" in away
    assert not ACTION.findall(here)
    assert (
        away.replace(away[away.index('<p class="site-popover-actions">') :], "</div>") == here
    )


def test_a_replay_rows_popover_body_comes_from_one_function(
    overview: overview_data.Overview, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`replay_row_popover_body` is the one source of an awaiting-replay row's detail:
    the reported and the verified bound, each with its holder and its entries. The
    popovers follow the disclosure rather than sit in it, and each ends in the button
    to its case in the frontier atlas."""
    row = overview.awaiting_replay[0]
    body = overview_sections.replay_row_popover_body(row)
    assert "<dt>Reported</dt>" in body
    assert "<dt>Verified here</dt>" in body
    assert html.escape(row.reported.holder) in body
    block = overview_sections.awaiting_replay(overview)
    assert body in _row_popover(block, f"pop-replay-n-{row.n}")
    assert block.index("</details>") < block.index('<div class="site-popover site-row-pop"')
    (action,) = ACTION.findall(_row_popover(block, f"pop-replay-n-{row.n}"))
    assert action == (f"frontier.html#n-{row.n}", "page")

    def marked(row: render_recent_results.Row) -> str:
        return f"<p>BODY OF {row.n}</p>"

    monkeypatch.setattr(overview_sections, "replay_row_popover_body", marked)
    block = overview_sections.awaiting_replay(overview)
    for waiting in overview.awaiting_replay:
        assert block.count(f"<p>BODY OF {waiting.n}</p>") == 1, waiting.n


def test_a_row_detail_escapes_its_words_and_keeps_its_html() -> None:
    """`row_detail` is the component: the row's attributes, its native trigger and its
    popover. The name, the label and the action's words are escaped; the trigger, the
    headline and the body are HTML and pass through."""
    detail = overview_sections.row_detail(
        "pop-x",
        name='a < b & "c"',
        trigger="<b>key</b>",
        label="A & B",
        title="<i>title</i>",
        body="<p>body</p>",
        action=("other.html#x", "Go <there>"),
    )
    assert detail.attributes == (
        'data-row-popover="pop-x" aria-label="a &lt; b &amp; &quot;c&quot;"'
    )
    assert detail.trigger == (
        '<button type="button" class="site-row-open" popovertarget="pop-x"><b>key</b></button>'
    )
    assert detail.popover.startswith(
        '<div class="site-popover site-row-pop" id="pop-x" popover role="dialog" '
        'aria-labelledby="pop-x-title">'
    )
    assert '<span class="site-card-label">A &amp; B</span>' in detail.popover
    assert 'id="pop-x-title"><i>title</i></p>' in detail.popover
    assert '<div class="site-row-pop-body"><p>body</p></div>' in detail.popover
    assert (
        '<a class="site-popover-action" href="other.html#x" data-go="page">Go &lt;there&gt;</a>'
    ) in detail.popover
    plain = overview_sections.row_detail(
        "pop-y", name="n", trigger="k", label="l", title="t", body="b"
    )
    assert "site-popover-actions" not in plain.popover
    assert overview_sections.plain_text("`s(11) >= 3`,  reported") == "s(11) >= 3, reported"


def test_a_row_with_detail_takes_the_shared_wash_and_no_disclosure_style() -> None:
    """The row's hover wash is the shared table rule's; a row with detail keeps it on
    keyboard focus, with a ring, and while its popover is open, and shows the pointer
    once the script has made it the control. No rule styles a `<details>` in a table."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hover = css[css.index(".kpress .site-table tbody tr:not(.site-group-row):hover {") :]
    assert "background: var(--site-wash);" in hover[: hover.index("}")]
    row = ".kpress .site-table tbody tr[data-row-popover]"
    held = css[css.index(f'{row}:is(:focus-visible, [aria-expanded="true"]) {{') :]
    assert "background: var(--site-wash);" in held[: held.index("}")]
    ring = css[css.index(".kpress .site-table tbody tr[data-row-popover]:focus-visible {") :]
    assert "outline: 2px solid var(--kpress-doc-accent);" in ring[: ring.index("}")]
    ready = css[css.index(".kpress .site-table tbody tr[data-row-ready] {") :]
    assert "cursor: pointer;" in ready[: ready.index("}")]
    trigger = css[css.index(".kpress .site-table .site-row-open {") :]
    for declaration in ("background: none;", "border: 0;", "color: inherit;", "font: inherit;"):
        assert declaration in trigger[: trigger.index("}")], declaration
    assert not re.search(r"\.site-(?:table|frontier)[^{}]*\b(?:details|summary)\b[^{}]*\{", css)


# ---------- Result filters: one bar on both tables of results (think-3pi5) ----------

#: The bar's controls, in its order: the row attribute each filters and how.
RESULT_FILTERS = [
    ("s", "min"),
    ("v", "min"),
    ("c", "min"),
    ("standing", ""),
    ("source", ""),
    ("n", "covers"),
    ("date", "from"),
    ("date", "to"),
]

_COUNT = re.compile(r'(<span class="site-count"[^>]*>)[^<]*</span>')
_SELECTED = re.compile(
    r'<select data-filter="([a-z]+)"[^>]*>'
    r'(?:<option value="[^"]*">[^<]*</option>)*<option value="([^"]*)" selected>'
)


def _filter_bar(page: str) -> str:
    """A results table's tools bar as the page carries it, from its tag to its close."""
    match = re.search(
        r'<div class="site-table-tools site-result-filters">.*?</div>', page, re.DOTALL
    )
    assert match
    return match.group(0)


def _controls(bar: str) -> list[tuple[str, str]]:
    """Each control's row attribute and bound, in the bar's order."""
    found = []
    for attributes in re.findall(r"<(?:select|input)\b([^>]*)>", bar):
        key = re.search(r'data-filter="([^"]+)"', attributes)
        bound = re.search(r'data-bound="([^"]+)"', attributes)
        assert key, attributes
        found.append((key[1], bound[1] if bound else ""))
    return found


def test_both_tables_of_results_carry_the_identical_filter_set_and_default(
    page: str, results: str
) -> None:
    """The overview's recent table and the results page's table sit under one bar: the
    same controls with the same choices in the same order, starting from the same
    default, Significance at S4 and up and everything else at All. Only the count, which
    is each table's own, differs."""
    here = _filter_bar(page.split('id="recent-results"', 1)[1])
    there = _filter_bar(results)
    assert _COUNT.sub(r"\1</span>", here) == _COUNT.sub(r"\1</span>", there)
    assert here != there
    assert _controls(here) == RESULT_FILTERS
    assert here.count(" selected>") == here.count("<select ") == 5
    assert dict(_SELECTED.findall(here)) == {
        "s": "4",
        "v": "",
        "c": "",
        "standing": "",
        "source": "",
    }
    for control in re.findall(r"<input\b[^>]*>", here):
        assert " value=" not in control, control
        assert " checked" not in control, control
    assert page.count('class="site-table-tools site-result-filters"') == 1
    assert results.count('class="site-table-tools site-result-filters"') == 1


def test_the_filter_bar_is_one_helpers_and_reads_the_whole_register(
    overview: overview_data.Overview,
) -> None:
    """`result_filters` writes the bar for both tables. Its choices come from the whole
    register, so a table that lists fewer results offers the same ones; only its count
    is the table's. Each rung select offers the rubric's levels above the lowest as
    floors, the top one bare."""
    recent = overview_sections.recent_results(overview)
    assert 0 < len(recent) < len(overview.results)
    full = overview_sections.result_filters(overview, overview.results)
    part = overview_sections.result_filters(overview, recent)
    assert full in overview_sections.results_table(overview)
    assert part in overview_sections.recent_table(overview)
    assert _COUNT.sub("", full) == _COUNT.sub("", part)
    assert overview_sections.result_filters(overview, []).endswith(">0 results</span></div>")
    assert overview_sections.SIGNIFICANCE_DEFAULT == 4
    assert overview_sections.rung_options("S") == [
        ("", "All"),
        ("2", "S2 and up"),
        ("3", "S3 and up"),
        ("4", "S4 and up"),
        ("5", "S5"),
    ]
    for scale in "VC":
        choices = overview_sections.rung_options(scale)
        assert choices[0] == ("", "All")
        assert choices[1] == ("1", f"{scale}1 and up")
        assert choices[-1] == ("5", f"{scale}5")
    standings = re.search(r'<select data-filter="standing">(.*?)</select>', full)
    assert standings
    assert set(re.findall(r'<option value="([^"]+)"', standings[1])) == {
        overview_sections.standing_key(result.standing) for result in overview.results
    }
    assert f' min="1" max="{max(overview.cases)}" ' in full
    dates = sorted(overview_sections.first_day(r.dated[1]) for r in overview.results)
    assert full.count(f' min="{dates[0]}" max="{dates[-1]}">') == 2
    assert overview_sections.count_text(3, 3) == "3 results"
    assert overview_sections.count_text(2, 3) == "2 of 3 results"


def _facets(tag: str) -> dict[str, str]:
    """A row's `data-*` attributes but for the two that name it and its popover."""
    found = dict(re.findall(r'\sdata-([a-z-]+)="([^"]*)"', tag))
    return {key: value for key, value in found.items() if key not in {"result", "row-popover"}}


def test_every_facet_a_result_row_carries_has_a_filter_and_every_filter_a_facet(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A row of either table carries the same facets, each from the register: whose
    result it is, its V, C and S levels, its standing, its cases and its date. The bar
    has a control for each and no control without one."""
    filtered = {key for key, _ in RESULT_FILTERS}
    recent = _recent_table(page)
    listed = {r.id for r in overview_sections.recent_results(overview)}
    for result in overview.results:
        record = result.record
        expected = {
            "source": "ours" if result.ours else "others",
            "v": record["verification"][1:],
            "c": record["confirmation"][1:],
            "s": str(record["significance"]["score"]),
            "standing": overview_sections.standing_key(result.standing),
            "n": overview_sections.result_cases(result),
            "date": overview_sections.first_day(result.dated[1]),
        }
        assert set(expected) == filtered
        tags = [_row(results, result.id).split(">", 1)[0]]
        if result.id in listed:
            tags.append(_recent_row(recent, result.id).split(">", 1)[0])
        for tag in tags:
            assert _facets(html.unescape(tag)) == expected, result.id
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", expected["date"]), result.id
        assert re.fullmatch(r"\d+(?:-\d+)?(?: \d+(?:-\d+)?)*", expected["n"]), result.id


def test_a_results_cases_and_date_are_written_for_the_filters() -> None:
    """A result's cases are a list of counts and ranges, and a date the register gives
    to the year or the month is the first day of it, so both order as the script reads
    them."""

    def cases(scope: dict) -> str:
        record = {"id": "T-900", "scope": scope}
        result = overview_data.Result(record, group="", credit="", ours=True)
        return overview_sections.result_cases(result)

    assert cases({"n_values": [11]}) == "11"
    assert cases({"n_values": [17, 18]}) == "17 18"
    assert cases({"n_values": [26, 18, 19, 20, 21]}) == "18-21 26"
    assert cases({"n_min": 1, "n_max": 100}) == "1-100"
    assert overview_sections.first_day("1979") == "1979-01-01"
    assert overview_sections.first_day("2005-03") == "2005-03-01"
    assert overview_sections.first_day("2026-09-04") == "2026-09-04"


def test_rows_below_the_default_are_hidden_in_the_html_and_stay_in_it(
    results: str, overview: overview_data.Overview
) -> None:
    """On the results page as on the overview, a row below S4 is `hidden` in the HTML,
    never left out of it, and the count is written for the rows left, so the first
    paint is the filtered table. A group heading with no row left under it is hidden
    with them."""
    shown = 0
    for result in overview.results:
        tag = _row(results, result.id).split(">", 1)[0] + ">"
        below = result.record["significance"]["score"] < 4
        assert overview_sections.shown_by_default(result) == (not below), result.id
        assert tag.endswith(" hidden>") == below, result.id
        shown += not below
    assert 0 < shown < len(overview.results)
    assert f"{shown} of {len(overview.results)} results</span>" in _filter_bar(results)
    headings = re.findall(r'<tr class="site-group-row" data-group="[^"]+"( hidden)?>', results)
    assert len(headings) == len(overview.groups)
    for hidden, (title, members) in zip(headings, overview.groups, strict=True):
        left = any(overview_sections.shown_by_default(result) for result in members)
        assert bool(hidden) == (not left), title
    assert {bool(hidden) for hidden in headings} == {True, False}
    text = re.sub(r"<[^>]+>", "", results)
    assert (
        "The table starts filtered to significance S4 and up; choose All to see every" in text
    )


def test_a_row_named_by_the_address_shows_whatever_the_filters_hide() -> None:
    """A link to a result's row (`all-results.html#t-048`) must land on the row even
    when the default filter hides it. With scripts `table.js` keeps the row the fragment
    names, which `tests/node/overview_table/filters.test.mjs` runs; without them one
    rule shows a hidden row that is the target, as a table row and, on a phone, as the
    card a results row is there. A targeted row takes the wash in every site table."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hidden = css[css.index("\n.site-table tr[hidden] {") :]
    assert "display: none;" in hidden[: hidden.index("}")]
    target = css[css.index("\n.site-table tr[hidden]:target {") :]
    assert "display: table-row;" in target[: target.index("}")]
    assert css.index("\n.site-table tr[hidden] {") < css.index(
        "\n.site-table tr[hidden]:target {"
    )
    phone = css[css.index("  .site-results tr[hidden]:target {") :]
    assert "display: grid;" in phone[: phone.index("}")]
    assert "  .site-results tr.site-group-row:not([hidden]) {" in css
    wash = css[css.index("\n.kpress .site-table tbody tr:target {") :]
    assert "background: var(--site-wash);" in wash[: wash.index("}")]


def test_without_scripts_no_row_stays_filtered() -> None:
    """A reader without scripts cannot change a filter, so the default must not hide
    anything from them: under `scripting: none` every row shows, as a table row or, on a
    phone, as the results table's card, each group under its heading, and the bar, which
    would do nothing, is not shown."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    block = css[css.index("\n@media (scripting: none) {") :]
    block = block[: block.index("\n}\n")]
    assert ".site-result-filters {\n    display: none;" in block
    assert ".site-table tbody tr[hidden] {\n    display: table-row;" in block
    phone = css[css.index("\n@media (scripting: none) and (width < 40rem) {") :]
    phone = phone[: phone.index("\n}\n")]
    assert ".site-results tbody tr[hidden] {\n    display: grid;" in phone
    assert ".site-results tbody tr.site-group-row[hidden] {\n    display: block;" in phone


def test_secondary_cell_content_is_quiet(results: str) -> None:
    """A credit in the results table and a finder under a frontier bound take the one
    quiet style: the support colour in the sans face."""
    from devtools.render_frontier_page import frontier_cases, table_html  # noqa: PLC0415

    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    rule = css[css.index("\n.site-cell-quiet {") :]
    rule = rule[: rule.index("}")]
    assert "color: var(--site-support-color);" in rule
    assert "font-family: var(--kpress-font-sans);" in rule
    assert 'class="site-col-credit site-cell-quiet"' in results
    assert 'class="site-frontier-note site-cell-quiet"' in table_html(frontier_cases())
