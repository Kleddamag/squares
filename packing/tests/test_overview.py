"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import html
import re
from collections import Counter

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
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


def test_every_register_entry_is_one_row(page: str, register: list[dict]) -> None:
    rows = ROW.findall(page)
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


def test_the_render_is_deterministic(page: str) -> None:
    assert render_overview.overview_page().html == page


def test_the_page_fetches_nothing(page: str) -> None:
    render_overview.assert_self_contained("index.html", page)


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


def test_the_atlas_shows_both_posters_each_opening_its_pdf(page: str) -> None:
    """The PDFs open in the browser: typed as PDF, and never marked for download."""
    atlas = page.split('class="site-wide site-atlas"', 1)[1].split(
        'class="site-atlas-note"', maxsplit=1
    )[0]
    for stem in ("known-best-1-100", "known-best-1-324"):
        assert f'<img src="{stem}.png"' in atlas
        assert atlas.count(f'<a href="{stem}.pdf" type="application/pdf">') == 2
    assert re.search(r"<a\b[^>]*\sdownload\b", page) is None


def test_the_atlas_grid_draws_every_case_and_places_it_lazily(page: str) -> None:
    """One cell per tracked case, each linking to its case record, all inside a
    template the script places when the grid comes near."""
    grid = page.split("data-atlas-grid>", 1)[1]
    template = grid.split("<template>", 1)[1].split("</template>", maxsplit=1)[0]
    cells = re.findall(
        r'<a class="site-atlas-cell" href="cases\.html#n-(\d+)" data-atlas-n="(\d+)"', template
    )
    assert [int(n) for n, _ in cells] == list(range(1, 325))
    assert all(n == cell for n, cell in cells)
    assert template.count("<svg ") == 324
    assert re.findall(r'aria-label="n = 11, [a-z]+"', template)
    assert render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8") in page


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


def test_the_atlas_film_waits_for_the_reader_behind_its_poster(page: str) -> None:
    """Embedded as the explainer embeds its film: controls, inline, nothing fetched and
    nothing moving until a reader presses play, and a poster that is a frame of the film
    served beside the page."""
    (video,) = re.findall(r"<video\b[^>]*>", page)
    for attribute in ("controls", "playsinline"):
        assert re.search(rf"\s{attribute}\b", video), attribute
    for attribute in ("autoplay", "loop", "muted"):
        assert not re.search(rf"\s{attribute}\b", video), attribute
    assert 'preload="none"' in video
    assert f'poster="{OVERVIEW_FILM_POSTER.name}"' in video
    assert OVERVIEW_FILM_POSTER in COMPOSITE_ASSETS
    assert OVERVIEW_FILM_POSTER.is_file()
    assert (
        "ascent-n1-324-1080p60-citations.mp4"
        in page.split(video, 1)[1].split("</video>", maxsplit=1)[0]
    )


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
def test_every_site_page_retries_untypeset_math(name: str) -> None:
    page = render_overview.PAGES[name]().html
    assert render_overview.MATH_RETRY_SCRIPT.read_text(encoding="utf-8") in page


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


def _visualizer_page() -> str:
    """The Visualizer's page as `build_site` gives it the bar, on its own template."""
    from workbench_tools import build_site  # noqa: PLC0415

    template = build_site.WORKBENCH_PACKAGE / "assets" / "template.html"
    return build_site.with_nav(template.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", [*sorted(render_overview.PAGES), "workbench/index.html"])
def test_every_site_page_carries_the_same_bar(name: str) -> None:
    """Every page the Python build renders carries the bar byte for byte as the partial
    writes it, but for which item is current and the prefix that reaches the site's root."""
    assert name in render_overview.SITE_PAGES
    if name == "workbench/index.html":
        page, root = _visualizer_page(), "../"
    else:
        page, root = render_overview.PAGES[name]().html, ""
    partial = render_overview.SITE_NAV.read_text(encoding="utf-8").replace("{{ROOT}}", "")
    assert _the_bar(page, root=root) == SITE_NAV_BLOCK.findall(partial)[0]


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
    there. The card's icon and the button's agree, and every target on the site exists."""
    cards = CARD.findall(page)
    assert {kind for _, kind in cards} == {"scroll", "page", "external"}
    assert page.count('class="site-card"') == len(cards)
    ids = set(ID.findall(page))
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


@pytest.mark.parametrize("name", ["index.html", "frontier.html"])
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
    page: str, overview: overview_data.Overview, records: render_recent_results.Records
) -> None:
    """Standing is `render_recent_results.standing`, never restated: every table row
    carries it as an attribute and a chip, and only `holds` takes the accent."""
    for result in overview.results:
        expected = render_recent_results.standing(result.record, records)
        assert result.standing == expected, result.id
        row = _row(page, result.id)
        assert f'data-standing="{overview_sections.standing_key(expected)}"' in row, result.id
        assert overview_sections.standing_chip(expected) in row, result.id
    held = overview_sections.standing_chip(render_recent_results.HOLDS)
    assert 'data-tone="accent">holds</span>' in held
    for other in render_recent_results.STANDINGS[1:]:
        assert "data-tone" not in overview_sections.standing_chip(other), other
    recent = overview_sections.recent_list(overview)
    assert recent in page
    assert recent.count('data-standing="') == recent.count("<li>")


def test_the_s5_cards_say_which_still_hold(overview: overview_data.Overview) -> None:
    headline = overview_sections.headline_cards(overview)
    s5 = [r for r in overview.results if r.record["significance"]["score"] >= 5]
    assert s5
    for result in s5:
        button = re.search(
            rf'<button[^>]*popovertarget="pop-{result.id.lower()}"[^>]*>.*?</button>',
            headline,
            re.DOTALL,
        )
        assert button, result.id
        assert overview_sections.standing_chip(result.standing) in button.group(0), result.id
    holding = {r.id for r in s5 if r.standing == render_recent_results.HOLDS}
    # The audit's reading of the record; update it when the record moves on.
    assert holding == {"T-037"}


def test_the_standing_filter_offers_each_standing_on_the_page(
    page: str, overview: overview_data.Overview
) -> None:
    tools = re.search(r'<select data-filter="standing">(.*?)</select>', page, re.DOTALL)
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
    page: str, overview: overview_data.Overview
) -> None:
    for result in overview.results:
        row = _row(page, result.id)
        attribution = result.record.get("attribution")
        if attribution:
            published = str(attribution["published"])
            assert result.dated == ("published", published)
            assert f'<span class="site-date-kind">published</span> {published}' in row
        else:
            assert result.dated[0] == "established"
    recent = overview_sections.recent_list(overview)
    dates = re.findall(r'<span class="site-date">(\w+) ([\d-]+)</span>', recent)
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
    page: str, overview: overview_data.Overview
) -> None:
    labels = overview_sections.novelty_labels()
    assert labels["apparently-novel"].startswith("Not found in the recorded search")
    assert labels["confirmed-novel"].startswith("Priority confirmed")
    for result in overview.results:
        chip = (
            f'<dt>Novelty</dt><dd><span class="site-chip" data-novelty="{result.novelty}">'
            f"{result.novelty}</span> {html.escape(labels[result.novelty])}</dd>"
        )
        assert chip in _row(page, result.id), result.id
