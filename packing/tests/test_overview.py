"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import html
import re
from collections import Counter
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
ROW = re.compile(r'<tr id="(t-\d{3})" data-source="(ours|others)" data-c="(C\d)"[^>]*>')


@pytest.fixture(scope="module")
def page() -> str:
    return render_overview.overview_page().html


@pytest.fixture(scope="module")
def results() -> str:
    return render_overview.results_page().html


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


def test_every_register_entry_is_one_row(results: str, register: list[dict]) -> None:
    rows = ROW.findall(results)
    assert sorted(row_id for row_id, _, _ in rows) == sorted(r["id"].lower() for r in register)
    declared = {r["id"].lower(): r for r in register}
    for row_id, source, confirmation in rows:
        record = declared[row_id]
        assert source == ("others" if record.get("attribution") else "ours"), row_id
        assert confirmation == record["confirmation"], row_id


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


def test_every_link_to_a_result_goes_to_its_row(page: str, results: str) -> None:
    """The overview's recent table and replay table, and the case records, link a
    result at its row on the results page, never at a fragment of their own page."""
    rows = {row_id for row_id, _, _ in ROW.findall(results)}
    linked = re.findall(r'href="all-results\.html#([^"]+)"', page)
    assert linked
    assert set(linked) <= rows
    assert not re.search(r'href="#t-\d+"', page)
    cases = render_overview.cases_page().html
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
    """The one atlas popover is filled from the grid's facts: for n = 11, the film's
    chained bound, its star and badges, both bounds' sources with this project's notes,
    and what is open, read from the atlas figure and `bound-citations.json`."""
    facts = _atlas_facts(page)
    assert sorted(facts) == list(range(1, 325))
    eleven = facts[11]
    assert eleven["exact"] is False
    assert (eleven["lower"], eleven["upper"]) == ("3.875000", "3.877084")
    assert eleven["star"] is True
    assert [label for _, _, label in eleven["badges"]] == ["exact", "rigid"]
    assert eleven["open"] == ["optimality"]
    assert eleven["record"] == "n-011"
    assert eleven["cite"]["lower"] == {
        "text": "Kleddamag after Levy et al. 2026, GitHub",
        "note": "(confirmed T-037)",
    }
    assert eleven["cite"]["upper"]["text"] == "Trump 1979, Squares in Squares"
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
def test_every_site_page_loads_math_through_the_explainers_pipeline(name: str) -> None:
    """One math pipeline: the explainer's KaTeX bundle and host adapter, driven by the
    site's queue, and neither of kpress's whole-page entry points (auto-render and its
    native initializer), which typeset every formula in one task at DOMContentLoaded."""
    from devtools.render_explainer import katex_js, kpress_static  # noqa: PLC0415

    page = render_overview.PAGES[name]().html
    static = kpress_static()
    assert katex_js(static) in page
    assert render_overview.MATH_SCRIPT.read_text(encoding="utf-8") in page
    for entry in ("katex/auto-render.min.js", "katex/katex-init.js"):
        assert (static / entry).read_text(encoding="utf-8") not in page, entry


@pytest.mark.parametrize("name", ["index.html", "tutorial.html"])
def test_every_site_page_carries_the_explainers_text_tokens(name: str) -> None:
    """The type base, measure and heading scale come from the one file the explainer
    inlines too, after kpress's stylesheets so they win at kpress's own scopes."""
    page = render_overview.PAGES[name]().html
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
def test_every_site_page_carries_the_theme_control(name: str) -> None:
    page = render_overview.PAGES[name]().html
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
def test_every_site_page_carries_the_same_bar(name: str) -> None:
    """Every page the Python build renders carries the bar byte for byte as the partial
    writes it, but for which item is current and the prefix that reaches the site's root."""
    assert name in render_overview.SITE_PAGES
    if name == "workbench/index.html":
        page, root = _workbench_page(), "../"
    else:
        page, root = render_overview.PAGES[name]().html, ""
    partial = (
        render_overview.SITE_NAV.read_text(encoding="utf-8")
        .replace("{{ROOT}}", "")
        .replace("{{LOGO}}", render_overview.site_logo())
    )
    assert _the_bar(page, root=root) == SITE_NAV_BLOCK.findall(partial)[0]


def test_the_visualize_section_is_marked_current_on_both_its_pages() -> None:
    """The bar's Visualize entry leads to the film and is current on the film's page and
    on the workbench, which share one tab bar with their own tab current."""
    nav = render_overview.nav_html("overview")
    assert '<a data-page="visualize" href="visualize.html">Visualize</a>' in nav
    assert "Visualizer" not in nav
    film = render_overview.PAGES["visualize.html"]().html
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


def test_the_film_page_embeds_the_film_at_its_own_proportions() -> None:
    """The film is inline with its controls, fetches nothing until played, and shows a
    poster at the video's own 16:9, so starting playback moves nothing."""
    page = render_overview.PAGES["visualize.html"]().html
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
        panel = page[start:].split('<button type="button" class="site-card"', 1)[0]
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
def test_every_small_label_is_one_chip(name: str) -> None:
    """Rungs and case statuses share one chip; a rung chip carries its scale and level,
    which the stylesheet colours, and names the rung it shows."""
    html = render_overview.PAGES[name]().html
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


def test_every_result_shows_the_standing_readme_derives(
    page: str,
    results: str,
    overview: overview_data.Overview,
    records: render_recent_results.Records,
) -> None:
    """Standing is `render_recent_results.standing`, never restated: every table row
    carries it as an attribute and a chip, and only `holds` takes the accent."""
    for result in overview.results:
        expected = render_recent_results.standing(result.record, records)
        assert result.standing == expected, result.id
        row = _row(results, result.id)
        assert f'data-standing="{overview_sections.standing_key(expected)}"' in row, result.id
        assert overview_sections.standing_chip(expected) in row, result.id
    held = overview_sections.standing_chip(render_recent_results.HOLDS)
    assert 'data-tone="accent">holds</span>' in held
    for other in render_recent_results.STANDINGS[1:]:
        assert "data-tone" not in overview_sections.standing_chip(other), other
    recent = _recent_table(page)
    for result in overview_sections.newest_results(overview):
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
    """The section is one `.site-table` of the newest results, one row each, with the
    date, the result linking its row, the method, the credit and the status chips; no
    card, popover or list is left in it."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    recent = _recent_table(page)
    assert recent in section
    before_replay = section.split("site-replay", 1)[0]
    assert "site-card" not in before_replay
    assert "popover" not in before_replay
    assert "<li>" not in before_replay
    assert section.count("<table") == 2  # the recent table, then the replay table
    assert 'class="kpress-table site-table site-results site-recent-table"' in recent
    assert "data-site-table" not in recent
    heads = re.findall(r"<th[^>]*>([^<]+)</th>", recent.split("</thead>", 1)[0])
    assert heads == ["Date", "Result", "Method", "Credit", "Status"]
    newest = overview_sections.newest_results(overview)
    assert len(newest) == overview_sections.RECENT_COUNT
    assert re.findall(r'<tr data-result="(t-\d+)"', recent) == [r.id.lower() for r in newest]
    for result in newest:
        row = _recent_row(recent, result.id)
        cells = re.findall(r'<td class="(site-col-[a-z]+)"', row)
        assert cells == [
            f"site-col-{c}" for c in ("date", "result", "method", "credit", "status")
        ]
        assert f'<a href="all-results.html#{result.id.lower()}">' in row
        assert f'<span class="site-cell-quiet">{result.id}</span>' in row
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
    held = overview_sections.standing_chips("holds, reported")
    assert 'data-tone="accent">holds</span>' in held
    assert 'data-standing="reported">reported</span>' in held


def test_only_t037_of_the_s5_results_still_holds(overview: overview_data.Overview) -> None:
    s5 = [r for r in overview.results if r.record["significance"]["score"] >= 5]
    holding = {r.id for r in s5 if r.standing == render_recent_results.HOLDS}
    # The audit's reading of the record; update it when the record moves on.
    assert holding == {"T-037"}


def test_the_standing_filter_offers_each_standing_on_the_page(
    results: str, overview: overview_data.Overview
) -> None:
    tools = re.search(r'<select data-filter="standing">(.*?)</select>', results, re.DOTALL)
    assert tools
    offered = re.findall(r'<option value="([^"]*)">', tools.group(1))
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
    labels = overview_sections.novelty_labels()
    assert labels["apparently-novel"].startswith("Not found in the recorded search")
    assert labels["confirmed-novel"].startswith("Priority confirmed")
    for result in overview.results:
        chip = (
            f'<dt>Novelty</dt><dd><span class="site-chip" data-novelty="{result.novelty}">'
            f"{result.novelty}</span> {html.escape(labels[result.novelty])}</dd>"
        )
        assert chip in _row(results, result.id), result.id


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
    assert "--site-page-top: 2rem;" in nav
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
    """Both stepper arrows are the same drawing, the back one mirrored, never the arrow
    characters, which the site's face lacks and browsers draw from mismatched fallbacks."""
    popover = overview_sections.atlas_popover()
    step = popover[popover.index('<span class="site-atlas-pop-step">') :]
    step = step[: step.index("</span>")]
    assert "←" not in step
    assert "→" not in step
    assert step.count(overview_sections.step_arrow()) == 1
    assert step.count(overview_sections.step_arrow(back=True)) == 1


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
    """A data table's wide track is one rule on shared tokens. It stops at its own maximum,
    short of the atlas grid's, and its growth term is zero at or below
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
