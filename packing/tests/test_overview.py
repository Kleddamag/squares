"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import functools
import html
import html.parser
import re
import textwrap
from collections import Counter
from collections.abc import Callable
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from typing import cast

import pytest

from devtools import overview_data, overview_sections, render_overview, render_recent_results
from devtools.render_explainer import COMPOSITE_ASSETS, OVERVIEW_FILM_POSTER
from devtools.render_explainer import MARKDOWN as EXPLAINER_ARTICLE
from devtools.render_explainer import TEMPLATE as EXPLAINER_SHELL
from devtools.repo_links import DEFAULT_BRANCH, REPO_URL, hash_pinned_links, repo_url
from devtools.result_credit import OTHERS, source_lineage
from sqpack.yamlio import safe_load
from tests import site_renders

ID = re.compile(r'\sid="([^"]+)"')
#: A results-table row: its id, whose result it is, and its confirmation rung's level.
ROW = re.compile(
    r'<tr id="(t-\d{3})" data-source="(ours|others)" data-v="\d" data-c="(\d)"[^>]*>'
)


@pytest.fixture(scope="module")
def page() -> str:
    return site_renders.html("index.html")


@pytest.fixture(scope="module")
def results() -> str:
    return site_renders.html(render_overview.RESULTS_PAGE)


@pytest.fixture(scope="module")
def register() -> list[dict]:
    return safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]


@pytest.fixture(scope="module")
def rendered() -> Callable[[str], str]:
    """Any site page by name, from the one render of each the test process shares
    (`tests.site_renders`). Every page is rendered here, during setup, `cases.html` and
    its 9 MB among them, so no check carries a render in its own call time."""
    site_renders.pages()
    return site_renders.html


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
    """A fresh render of each page is the shared one, byte for byte, which is what lets
    every other check read the shared render."""
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


def _page_cards(page: str) -> list[tuple[str, str, str]]:
    """The overview's page cards, its first card section: each card's address, the rest
    of its opening tag, and its body."""
    frame = page.split('<div class="site-cards-frame', 1)[1].split("</div></div>", 1)[0]
    cards = re.findall(
        r'<a class="site-card site-card-link" href="([^"]+)"([^>]*)>(.*?)</a>', frame, re.DOTALL
    )
    assert frame.count("site-card-label") == len(cards), "a page card that is not a link"
    return cards


def _page_card_parts(page: str, href: str) -> tuple[str, str]:
    """A page card's value and note on the overview, as `card_parts` gives a button's."""
    (body,) = [body for address, _, body in _page_cards(page) if address == href]
    value, note = body.split('class="site-card-value">', 1)[1].split(
        '<span class="site-card-note">'
    )
    return value, note


def test_each_page_card_is_a_plain_link_to_its_page(page: str) -> None:
    """The overview's four page cards lead to full pages the site serves, so each card
    is the link itself and goes there in the same tab: an `<a href>` with the page icon
    (`data-go="page"`), no popover, no framed preview and no new tab. Each keeps its
    label, headline, note and size."""
    cards = _page_cards(page)
    pages = overview_sections.PAGES
    assert [href for href, _, _ in cards] == [href for href, *_ in pages]
    assert [href for href, *_ in pages] == [
        "explainer.html",
        "tutorial.html",
        "workbench/",
        "frontier.html",
    ]
    served = {*render_overview.SITE_PAGES, "workbench/"}
    size = overview_sections.SECTION_CARD_SIZES["pages"]
    for (href, tag, body), (_, label, title, note) in zip(cards, pages, strict=True):
        assert href in served, href
        assert tag == f' data-go="page" data-card-size="{size}"', href
        assert "popovertarget" not in tag, href
        assert 'target="_blank"' not in tag, href
        assert "<button" not in body, href
        assert f'<span class="site-card-label">{label}</span>' in body, href
        value, shown = _page_card_parts(page, href)
        assert card_text(value) == title, href
        assert card_text(shown) == note, href
        assert f'src="{overview_sections.embed_url(href)}"' not in page, href
    assert "pop-page-" not in page
    frame = page.split('<div class="site-cards-frame', 1)[1].split("</div></div>", 1)[0]
    for popover in ("popover", "<iframe", "<button"):
        assert popover not in frame, popover


def test_a_same_tab_link_card_leads_only_to_a_page_of_the_site() -> None:
    """`link_card` opens a new tab unless told otherwise; told otherwise, it emits no
    `target`, and refuses an address off the site, which never replaces this page."""
    made = overview_sections.link_card("frontier.html", "Label", "Headline", "A note.")
    assert ' target="_blank" rel="noopener noreferrer">' in made
    same = overview_sections.link_card(
        "frontier.html", "Label", "Headline", "A note.", new_tab=False
    )
    assert same.startswith(
        '<a class="site-card site-card-link" href="frontier.html" data-go="page" '
        'data-card-size="small">'
    )
    assert "target=" not in same
    assert "rel=" not in same
    assert same.split(">", 1)[1] == made.split(">", 1)[1]
    with pytest.raises(SystemExit, match="only a page of this site"):
        overview_sections.link_card(
            "https://github.com/jlevy/squares", "Label", "Headline", "A note.", new_tab=False
        )


def test_every_other_direct_card_opens_in_a_new_tab(page: str) -> None:
    """A card that is itself the link, other than a page card, opens its target in a new
    tab, on the site or off it, and never hands the new tab a way back to this one: a
    poster's PDF, the film, another project."""
    direct = re.findall(r'<a class="site-card[^"]*"[^>]*>', page)
    assert len(direct) == len(overview_sections.PAGES) + len(
        overview_sections.OTHER_PROJECTS
    ) + len(overview_sections.ATLAS_CARDS)
    for tag in direct[len(overview_sections.PAGES) :]:
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
    """A card is as wide as a column of the grid its frame fits, which it can know only by
    asking the frame, so every card section is the only child of a `.site-cards-frame`."""
    grids = re.findall(r'<div class="([^"]*)"><div class="(site-cards[^"]*)">', page)
    every = re.findall(r'<div class="site-cards[" ]', page)
    assert len(grids) == len(every), "a card grid outside a frame"
    assert all(frame == "site-cards-frame site-wide" for frame, _ in grids)
    assert "site-cards-dimensions" not in page, "the rating ladders are no card grid"


#: A container query naming how many cards of one size its frame fits to a line from a
#: given width.
_CARDS_TO_A_LINE = re.compile(
    r"@container \(width >= ([\d.]+)rem\) \{\s*\.site-cards \{\s*"
    r"--site-cards-(small|medium|large): (\d+);\s*\}\s*\}"
)
#: Each card size's minimum column, in rem, and the most to a line the stylesheet steps
#: to: `paper-design.md`, Cards.
CARD_COLUMNS = {"small": (12, 6), "medium": (16, 5), "large": (21, 4)}


def _screen_card_rules() -> str:
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    screen = css[css.index("@media screen {\n  .site-cards {") :]
    return screen[: screen.index("\n}\n")]


def test_every_card_line_centres_on_its_line() -> None:
    """On screen the cards are one wrapping row that centres every line it does not fill,
    four cards on a wide screen and the last line of a long section alike, and a medium
    card keeps the width of a column of the grid the frame fits: n 16rem columns and
    n - 1 1rem gaps. Print keeps that grid, filled from the left."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    base = css[css.index(".site-cards {") :]
    base = base[: base.index("}")]
    assert "--site-card-gap: 1rem;" in base
    assert "grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));" in base
    screen = _screen_card_rules()
    row = screen[: screen.index("}")]
    for declaration in ("display: flex;", "flex-wrap: wrap;", "justify-content: center;"):
        assert declaration in row
    card = screen[screen.index(".site-cards > .site-card {") :]
    card = card[: card.index("}")]
    assert "--site-cards-line: var(--site-cards-medium);" in card
    assert "calc((var(--site-cards-line) - 1) * var(--site-card-gap));" in card
    assert "flex: 0 0 calc((100% - var(--site-cards-gaps)) / var(--site-cards-line));" in card
    assert "min-inline-size: 0;" in card
    cards = css[css.index("/* ---------- Cards") : css.index(".kpress .site-card {")]
    assert ":has(" not in cards, "a card line centres without counting its cards"


def test_each_card_size_is_a_column_of_its_own_grid() -> None:
    """A card of each size is as wide as a column of the grid of that size's columns the
    frame fits: n columns of minimum m rem and n - 1 1rem gaps need (m + 1)n - 1 rem, so
    each size's count steps at exactly those widths, and a card that names no size is
    medium."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    steps: dict[str, list[tuple[float, int]]] = {size: [] for size in CARD_COLUMNS}
    for width, size, count in _CARDS_TO_A_LINE.findall(css):
        steps[size].append((float(width), int(count)))
    assert tuple(steps) == overview_sections.CARD_SIZES
    for size, (minimum, most) in CARD_COLUMNS.items():
        assert [count for _, count in steps[size]] == list(range(2, most + 1)), size
        assert all(width == (minimum + 1) * count - 1 for width, count in steps[size]), size
    base = css[css.index(".site-cards {") :]
    base = base[: base.index("}")]
    screen = _screen_card_rules()
    for size in CARD_COLUMNS:
        assert f"--site-cards-{size}: 1;" in base
        if size != "medium":
            rule = screen[
                screen.index(f'.site-cards > .site-card[data-card-size="{size}"] {{') :
            ]
            assert f"--site-cards-line: var(--site-cards-{size});" in rule[: rule.index("}")]
    assert '[data-card-size="medium"]' not in css


#: A card, as its opening tag's size and everything after its caps label: the headline,
#: the note and a direct card's address.
_CARD_ELEMENT = re.compile(
    r'<(button|a)\b[^>]*class="site-card[ "][^>]*data-card-size="([^"]*)"[^>]*>'
    r'.*?<span class="site-card-value">(.*?)</\1>',
    re.DOTALL,
)


def _card_sections(page: str) -> dict[str, list[tuple[str, str]]]:
    """Each card section of the overview, in page order, as its cards' (size, text)."""
    frames = page.split('<div class="site-cards-frame')[1:]
    assert len(frames) == len(overview_sections.SECTION_CARD_SIZES)
    return {
        name: [(size, text) for _, size, text in _CARD_ELEMENT.findall(frame)]
        for name, frame in zip(overview_sections.SECTION_CARD_SIZES, frames, strict=True)
    }


def test_every_card_names_one_of_three_sizes(page: str) -> None:
    """Every card says its size in `data-card-size`, small, medium or large, and a
    section's cards are all the size the section declares, so its lines are one grid."""
    assert overview_sections.CARD_SIZES == ("small", "medium", "large")
    sections = _card_sections(page)
    assert sum(len(cards) for cards in sections.values()) == len(
        re.findall(r'<(?:button|a)\b[^>]*class="site-card[ "]', page)
    ), "a card with no size"
    assert [len(cards) for cards in sections.values()] == [
        len(overview_sections.PAGES),
        len(overview_sections.ATLAS_CARDS),
        len(overview_sections.OTHER_PROJECTS),
        len(overview_sections.DOCUMENTS),
    ]
    for name, cards in sections.items():
        declared = overview_sections.SECTION_CARD_SIZES[name]
        assert {size for size, _ in cards} == {declared}, name
    assert overview_sections.SECTION_CARD_SIZES == {
        "pages": "medium",
        "atlas": "medium",
        "projects": "medium",
        "documents": "small",
    }


def test_no_card_leaves_its_math_as_plain_text(page: str) -> None:
    """A card's headline and note are prose whose mathematical runs are set as math
    (`n = 21`, a bound on `s(11)`), so on a card, which is sans, they are sans math
    rather than upright words: nothing `overview_data.MATH` would match is left outside
    a formula on any card."""
    cards = [text for section in _card_sections(page).values() for _, text in section]
    assert len(cards) > len(overview_sections.OTHER_PROJECTS)
    typeset = 0
    for text in cards:
        left = overview_data.MATH.findall(overview_sections.words(text))
        assert not left, (left, overview_sections.reading_text(text))
        typeset += overview_sections.formulas(text)
    assert typeset >= 9


def test_each_sections_size_is_what_its_typical_card_asks_for(page: str) -> None:
    """A section's declared size is the size its median card's text takes by default, so
    the sizes follow the text: a section whose cards grow or shrink past a threshold
    fails here until its size is declared again."""
    for name, cards in _card_sections(page).items():
        lengths = sorted(len(overview_sections.reading_text(text)) for _, text in cards)
        typical = lengths[len(lengths) // 2]
        assert (
            overview_sections.size_for_length(typical)
            == overview_sections.SECTION_CARD_SIZES[name]
        ), (name, lengths)


def test_a_card_without_a_declared_size_takes_its_texts() -> None:
    """The default size counts a card's headline and note as they read, a formula once,
    and is small under 80 characters, large from 160 and medium between; a declared size
    wins, and a size that is not one of the three is refused."""
    assert (overview_sections.CARD_SMALL_BELOW, overview_sections.CARD_LARGE_FROM) == (80, 160)
    formula = overview_data.math_html("n = 11")
    assert overview_sections.reading_text(f"Earlier {formula} lower  bounds") == (
        "Earlier n=11 lower bounds"
    )
    assert [overview_sections.size_for_length(n) for n in (0, 79, 80, 159, 160, 400)] == [
        "small",
        "small",
        "medium",
        "medium",
        "large",
        "large",
    ]
    assert overview_sections.card_size("x" * 30, "y" * 49) == "small"
    assert overview_sections.card_size("x" * 30, "y" * 50) == "medium"
    assert overview_sections.card_size("x" * 30, "y" * 130) == "large"

    def built(note: str, size: str | None = None) -> str:
        made = overview_sections.card(
            "pop-x",
            "Label",
            "Headline",
            note,
            href="#recent-results",
            action="Go",
            size=cast("overview_sections.CardSize | None", size),
        )
        return made.split(">", 1)[0]

    assert built("A short note.").endswith('data-card-size="small"')
    assert built("y" * 200).endswith('data-card-size="large"')
    assert built("y" * 200, size="small").endswith('data-card-size="small"')
    link = overview_sections.link_card("frontier.html", "Label", "Headline", "A short note.")
    assert ' data-card-size="small" ' in link.split(">", 1)[0]
    with pytest.raises(SystemExit, match="not a card size"):
        built("A short note.", size="huge")


#: A cell of the rating-ladder diagram: the ladder it belongs to, then, where it holds a
#: rung, the chip's title, scale, level and label, the description and the count.
_LADDER_CELL = re.compile(
    r'<div class="site-ladders-cell(?P<empty> site-ladders-empty)?" role="cell" '
    r'data-ladder="(?P<ladder>[SVC])">'
    r'(?:<div class="site-ladders-rung">'
    r'<span class="site-chip site-rung-fill" title="(?P<title>[^"]*)" '
    r'data-rung="(?P<scale>[SVC])" data-level="(?P<level>\d)">(?P<label>[SVC]\d)</span>'
    r'<span class="site-ladders-meaning">(?P<meaning>[^<]*)</span>'
    r'<span class="site-ladders-count">(?P<count>[^<]*)</span></div>)?</div>'
)


def _ladders(page: str) -> str:
    """The Verification at a Glance section's diagram, the one block between its heading
    and the prose under it."""
    section = page.split('id="verification-at-a-glance"', 1)[1].split("<h2", 1)[0]
    assert section.count('class="site-ladders"') == 1
    return section.split('<div class="site-ladders-frame site-wide">', 1)[1].split("<p", 1)[0]


def test_verification_at_a_glance_is_one_ladder_diagram_significance_first(page: str) -> None:
    """The section is one diagram, not three cards: a column a dimension in the order
    Significance, Verification, Confirmation, each headed by its name and question with
    no caps label, and a row a level, the highest first, so the rungs line up. It is a
    grid with table roles, never a `<table>`, which kpress would wrap and restyle and
    `overview/table.js` would look for."""
    assert [scale for scale, *_ in overview_sections.DIMENSIONS] == ["S", "V", "C"]
    diagram = _ladders(page)
    for foreign in ("<table", "site-table", "site-card", "popovertarget"):
        assert foreign not in diagram, foreign
    assert "pop-dimension-" not in page
    assert diagram.startswith('<div class="site-ladders" role="table" aria-label="')
    heads = re.findall(
        r'<div class="site-ladders-head" role="columnheader" data-ladder="([SVC])">'
        r'<a class="site-ladders-name" href="([^"]+)">([^<]+)</a> '
        r'<span class="site-ladders-question">([^<]+)</span></div>',
        diagram,
    )
    assert heads == [
        (scale, f"epistemics.html#{section}", name, html.escape(question, quote=True))
        for scale, name, section, question in overview_sections.DIMENSIONS
    ]
    rows = diagram.split('<div class="site-ladders-row" role="row"')[1:]
    assert len(rows) == diagram.count('role="row"')
    assert rows[0].count('role="columnheader"') == 1 + len(heads)
    levels = [re.match(r' data-level="(\d)">', row) for row in rows[1:]]
    assert [int(level.group(1)) for level in levels if level] == [5, 4, 3, 2, 1, 0]
    for level, row in zip(range(5, -1, -1), rows[1:], strict=True):
        assert f'<span class="site-ladders-level" role="rowheader">Level {level}</span>' in row
        cells = list(_LADDER_CELL.finditer(row))
        assert row.count('role="cell"') == len(cells) == len(heads), level
        assert [cell["ladder"] for cell in cells] == ["S", "V", "C"], level
        held = [cell["label"] for cell in cells if cell["label"]]
        # Significance has no level 0, so its cell there is empty and holds its place.
        assert held == ([f"{scale}{level}" for scale in "SVC"] if level else ["V0", "C0"])
        assert [bool(cell["empty"]) for cell in cells] == [not cell["label"] for cell in cells]


def test_the_ladder_diagram_says_what_the_rubric_says(page: str, register: list[dict]) -> None:
    """Every rung of `epistemics.md` is a cell: its chip, titled with the rubric's own
    meaning, its description, which is that meaning unless the rung has a short form, and
    the count of register entries at that level."""
    levels = overview_sections.rubric_levels()
    assert [len(levels[scale]) for scale in "VCS"] == [6, 6, 5]
    meanings = {
        f"{scale}{level}": meaning
        for scale, rungs in levels.items()
        for level, meaning in rungs
    }
    assert overview_sections.rung_meanings() == meanings
    short = overview_sections.rung_short_meanings()
    assert set(short) == set(meanings)
    assert {label for label in short if short[label] != meanings[label]} == set(
        overview_sections.RUNG_SHORT_MEANINGS
    )
    declared = {
        "V": Counter(int(r["verification"][1]) for r in register),
        "C": Counter(int(r["confirmation"][1]) for r in register),
        "S": Counter(int(r["significance"]["score"]) for r in register),
    }
    assert overview_sections.rung_counts() == declared
    cells = {
        cell["label"]: cell for cell in _LADDER_CELL.finditer(_ladders(page)) if cell["label"]
    }
    assert set(cells) == set(meanings)
    for label, cell in cells.items():
        assert (cell["ladder"], cell["scale"], cell["level"]) == (label[0], label[0], label[1])
        assert html.unescape(cell["title"]) == meanings[label], label
        assert html.unescape(cell["meaning"]) == short[label], label
        count = declared[label[0]][int(label[1])]
        assert cell["count"] == overview_sections.count_label(count), label
    assert [overview_sections.count_label(n) for n in (0, 1, 2)] == [
        "no result yet",
        "1 result",
        "2 results",
    ]


def test_every_rung_has_a_description_that_fits_two_lines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cell's description is a box of exactly two lines, so every rung's text wraps to
    at most two lines of the narrowest cell, `SHORT_MEANING_LINE` characters each, and
    none is cut with an ellipsis. One that does not fit stops the build and asks for a
    short form, as does a short form for a rung the rubric does not have.
    `test_site_ladders` measures the same lines in a browser."""
    short = overview_sections.rung_short_meanings()
    for label, text in short.items():
        lines = textwrap.wrap(text, overview_sections.SHORT_MEANING_LINE)
        assert 1 <= len(lines) <= 2, (label, lines)
        assert not re.search(r"…|\.\.\.", text), label
    long_form = "A reusable technique, bound family, or resolved disputed value"
    assert overview_sections.rung_meanings()["S4"] == long_form
    try:
        monkeypatch.setattr(overview_sections, "RUNG_SHORT_MEANINGS", {})
        overview_sections.rung_short_meanings.cache_clear()
        with pytest.raises(SystemExit, match=r"S4's description.*does not fit two lines"):
            overview_sections.rung_short_meanings()
        monkeypatch.setattr(overview_sections, "RUNG_SHORT_MEANINGS", {"S0": "No such rung"})
        overview_sections.rung_short_meanings.cache_clear()
        with pytest.raises(SystemExit, match=r"names no rung of epistemics\.md: S0"):
            overview_sections.rung_short_meanings()
    finally:
        monkeypatch.undo()
        overview_sections.rung_short_meanings.cache_clear()
    assert overview_sections.rung_short_meanings() == short


def test_the_ladder_diagram_is_its_own_component_on_the_shared_tokens() -> None:
    """The diagram's rules are its own (`.site-ladders`), and its measures agree with one
    another: the description's box is two lines and is never clipped; a rung sets its
    description beside the rail only where the cell holds the rail, the gap and the least
    description; and three columns stand only where each still holds that least. It
    stands the tables' space clear of the text."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    for retired in (".site-level", "site-cards-dimensions"):
        assert retired not in css, retired
    rules = css.split("/* ---------- The rating ladders ----------", 1)[1]
    rules = rules.split("/* The atlas grid:", 1)[0]
    assert "margin-block: var(--site-table-space);" in rules
    boxes = re.findall(r"\.site-ladders-meaning \{([^}]*)\}", rules)
    assert "block-size: calc(2 * var(--site-ladders-line));" in boxes[0]
    assert not any("overflow" in box or "clamp" in box for box in boxes)
    assert not re.search(r"text-overflow|line-clamp", rules)

    def rem(token: str) -> float:
        found = re.search(rf"--site-ladders-{token}: ([\d.]+)rem;", rules)
        assert found, token
        return float(found.group(1))

    rail, gap, least, inset = rem("rail"), rem("gap"), rem("meaning-min"), rem("inset")
    beside = re.search(r"@container \(inline-size >= ([\d.]+)rem\)", rules)
    columns = re.search(r"@container site-ladders \(inline-size < ([\d.]+)rem\)", rules)
    assert beside, "no query sets a description beside its rail"
    assert columns, "no query stacks the ladders"
    assert float(beside.group(1)) == rail + gap + least
    assert float(columns.group(1)) / len(overview_sections.DIMENSIONS) - inset >= least


def test_no_placeholder_or_raw_math_is_left(page: str) -> None:
    article = re.sub(r"<script.*?</script>", "", page, flags=re.DOTALL).split("<article", 1)[1]
    assert not re.search(r"\{\{[A-Z0-9_]+\}\}", page)
    assert not re.search(r"\bs\(\d+\) *[<>]=", article)
    assert not re.search(r"(?<![\w\\])\$[^$\s][^$<]*\$", article)


def test_every_record_link_is_on_main_or_a_site_page(overview: overview_data.Overview) -> None:
    for result in overview.results:
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


def test_on_github_links_open_the_latest_version(page: str) -> None:
    """Each document card has an "On GitHub" link on `main`."""
    branch = f"{REPO_URL}/blob/{DEFAULT_BRANCH}/"
    also = re.findall(r'<a class="site-popover-also" href="([^"]+)"[^>]*>On GitHub</a>', page)
    assert len(also) == len(overview_sections.DOCUMENTS)
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


def test_record_line_links_point_at_their_entry(overview: overview_data.Overview) -> None:
    lines = overview_data.RESULTS.read_text(encoding="utf-8").splitlines()
    for result in overview.results:
        (register,) = (link for link in result.records if link.label == "register")
        line = int(register.url.rsplit("#L", 1)[1])
        assert lines[line - 1].strip() == f"- id: {result.id}", result.id


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def test_overview_ids_never_shadow_an_explainer_anchor(page: str, results: str) -> None:
    """`forward.js` sends a fragment the overview lacks to the explainer, so an old
    explainer deep link lands on the overview only if the overview has the same id."""
    explainer = EXPLAINER_ARTICLE.read_text(encoding="utf-8")
    explainer_ids = set(ID.findall(explainer + EXPLAINER_SHELL.read_text(encoding="utf-8")))
    explainer_ids |= {
        _slug(h) for h in re.findall(r"^#{1,4} (.+)$", explainer, flags=re.MULTILINE)
    }
    ours = {i for i in ID.findall(page) if not i.startswith("kpress-")}
    assert not ours & explainer_ids
    moved = {i for i in ID.findall(results) if i.startswith("t-")}
    assert moved
    assert not moved & explainer_ids


def test_the_nav_links_only_to_served_pages() -> None:
    nav = render_overview.nav_html("overview")
    served = {"./", *render_overview.SITE_PAGES, "workbench/"}
    for href in re.findall(r'href="([^"]+)"', nav):
        assert href.startswith("https://") or href in served, href
    assert nav.count('aria-current="page"') == 1


#: The bar's entries, in order: each one's key, where it leads and its label.
NAV_ENTRIES = [
    ("overview", "./", "Overview"),
    ("frontier", "frontier.html", "Frontier"),
    ("results", "all-results.html", "Results"),
    ("papers", "papers.html", "Papers"),
    ("visualize", "visualize.html", "Visualize"),
    ("github", "https://github.com/jlevy/squares", "GitHub"),
]
#: The pages the bar's Papers entry is current on, of those this renderer owns; the
#: explainer, the third, is rendered by its own module and held there (`test_explainer`).
PAPERS_SECTION = {"papers.html", "tutorial.html"}


def test_the_nav_has_one_papers_entry_for_the_explainer_and_the_tutorial() -> None:
    """The explainer and the tutorial have no entry of their own: Papers leads to the page
    that holds them both, and neither old key can be marked current."""
    nav = render_overview.nav_html("papers")
    entries = re.findall(
        r'<a data-page="(\w+)"(?: aria-current="page")? href="([^"]+)">([^<]+)</a>', nav
    )
    assert entries == NAV_ENTRIES
    assert '<a data-page="papers" aria-current="page" href="papers.html">Papers</a>' in nav
    assert "papers.html" in render_overview.SITE_PAGES
    assert "papers.html" in render_overview.PAGES
    for gone in ("explainer", "tutorial"):
        with pytest.raises(SystemExit):
            render_overview.nav_html(gone)


@pytest.mark.parametrize("name", sorted(render_overview.PAGES))
def test_papers_is_current_on_the_papers_page_and_the_tutorial_alone(
    name: str, rendered: Callable[[str], str]
) -> None:
    """Papers is the current entry on `papers.html` and on the tutorial, which keeps its
    own address, and on no other page this renderer owns."""
    current = re.findall(r'<a data-page="(\w+)" aria-current="page"', rendered(name))
    assert len(current) == 1
    assert (current == ["papers"]) is (name in PAPERS_SECTION), current
    assert set(render_overview.PAGES) >= PAPERS_SECTION


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


def test_the_film_page_shows_no_title_and_keeps_one_for_a_screen_reader(
    rendered: Callable[[str], str],
) -> None:
    """The Visualize page shows the bar, the section tabs and the film: no page title and
    no subtitle. It keeps its document title and one `h1`, for a screen reader alone, and
    the film, the first block a reader sees, brings no margin of its own."""
    page = rendered("visualize.html")
    assert "<title>Visualize · Square Packing</title>" in page
    assert re.findall(r"<h1\b[^>]*>.*?</h1>", page, re.DOTALL) == [
        '<h1 class="site-visually-hidden" id="visualize">Visualize</h1>'
    ]
    article = page.split('class="kpress-prose kpress-long-text site-page">', 1)[1]
    assert article.lstrip().startswith('<h1 class="site-visually-hidden"')
    assert re.search(r'</h1>\s*<figure class="site-film-frame', article)
    for gone in ('class="site-hero"', 'class="subtitle"', "The ascent"):
        assert gone not in article, gone
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    hidden = css[css.index("\n.site-visually-hidden {") :]
    hidden = hidden[: hidden.index("}")]
    for declaration in (
        "block-size: 1px;",
        "clip-path: inset(50%);",
        "inline-size: 1px;",
        "overflow: hidden;",
        "position: absolute;",
    ):
        assert declaration in hidden, declaration
    assert "display: none" not in hidden
    assert "visibility" not in hidden
    assert (
        "@media screen {\n"
        "  .site-page .site-visually-hidden:first-child + .site-film-frame {\n"
        "    margin-block-start: 0;\n  }\n}"
    ) in css


def test_no_site_stylesheet_keys_on_the_system_theme_alone() -> None:
    """An explicit Light or Dark choice must win over the system theme, so the site's
    styles key on kpress's resolved theme, never on `prefers-color-scheme`."""
    for sheet in (render_overview.SITE_CSS, render_overview.SITE_NAV_CSS, EXPLAINER_SHELL):
        assert "prefers-color-scheme" not in sheet.read_text(encoding="utf-8"), sheet.name


CARD = re.compile(
    r'<button type="button" class="site-card" popovertarget="([^"]+)" '
    r'data-go="(scroll|external|page)" data-card-size="(?:small|medium|large)">'
)
ACTION = re.compile(
    r'<a class="site-popover-action" href="([^"]+)" data-go="(scroll|external|page)"'
)


def test_every_card_shows_where_it_goes_and_gets_there(page: str, results: str) -> None:
    """Every card opens a popover that shows its target and ends in one button that goes
    there. Another page is rendered in a frame, in its embedded view, and the button
    expands it; a place on this page, or another site, is previewed, and the button goes
    there; a row on another page, such as a result's on the results page, is previewed
    too, and the button goes to that page. The card's icon and the button's agree, and
    every target on the site exists.
    The exceptions are the cards that are the link itself, with no popover: the page
    cards, the atlas's and the other projects' (their own tests above)."""
    cards = CARD.findall(page)
    assert "page" in {kind for _, kind in cards} <= {"scroll", "page", "external"}
    assert page.count('class="site-card"') == len(cards)
    ids = set(ID.findall(page))
    rows = set(ID.findall(results))
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


#: A rung chip, and what may stand between two chips of one run: white space.
RUNG_CHIP = re.compile(
    r'<span class="site-chip site-rung-fill" data-rung="([SVC])" data-level="(\d)">'
    r"([SVC]\d)</span>"
)
#: The order the site lists a result's rungs in: significance first (think-ucon).
RUNG_ORDER = "SVC"


def _rung_runs(html: str) -> list[list[str]]:
    """Every run of rung chips with only white space between them, as their labels."""
    runs: list[list[str]] = []
    end = None
    for match in RUNG_CHIP.finditer(html):
        if end is not None and not html[end : match.start()].strip():
            runs[-1].append(match.group(3))
        else:
            runs.append([match.group(3)])
        end = match.end()
    return runs


def test_a_results_rungs_run_significance_first(overview: overview_data.Overview) -> None:
    """`rung_chips` is the one place the order is set: S, then V, then C. The status
    cell and a result overview's head open with it (`status_chips`)."""
    assert overview.results
    for result in overview.results:
        record = result.record
        rungs = overview_sections.result_rungs(result)
        assert rungs == (
            f"S{record['significance']['score']}",
            record["verification"],
            record["confirmation"],
        )
        chips = overview_sections.rung_chips(result)
        assert [label for _, _, label in RUNG_CHIP.findall(chips)] == list(rungs)
        assert overview_sections.status_chips(result).startswith(chips + " ")


@pytest.mark.parametrize(
    "name", ["index.html", render_overview.RESULTS_PAGE, "cases.html", "frontier.html"]
)
def test_every_page_lists_significance_first(name: str, rendered: Callable[[str], str]) -> None:
    """Wherever rung chips sit side by side, on any page, they run S, V, C: a result's
    three in a row, a popover, an overview or a case record, and the V and C of an entry
    awaiting replay. No run repeats a scale or puts a later one first."""
    runs = [run for run in _rung_runs(rendered(name)) if len(run) > 1]
    if name != "frontier.html":
        assert any(len(run) == len(RUNG_ORDER) for run in runs), name
    for run in runs:
        places = [RUNG_ORDER.index(label[0]) for label in run]
        assert places == sorted(set(places)), (name, run)


def test_each_results_row_shows_its_rungs_significance_first(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """The Rungs cell of the results table and the Status cell of Recent Results both
    open with the result's S, V and C chips, in that order."""
    recent = {result.id for result in overview_sections.recent_results(overview)}
    assert recent
    table = _recent_table(page)

    def cell(row: str, column: str) -> str:
        """A row's cell of this class, from the end of its opening tag."""
        found = re.search(rf'<td class="{column}"[^>]*>', row)
        assert found, column
        return row[found.end() :]

    for result in overview.results:
        chips = overview_sections.rung_chips(result)
        assert cell(_row(results, result.id), "site-rungs").startswith(chips), result.id
        if result.id in recent:
            status = cell(_recent_row(table, result.id), "site-col-status")
            assert status.startswith(chips + " "), result.id
    for title in re.findall(
        r'<th[^>]* title="([^"]*whether a case bound[^"]*)"', page + results
    ):
        assert title.startswith("Significance, verification and confirmation, then "), title


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
    return site_renders.overview()


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


def _outside_row_popovers(page: str) -> str:
    """A page's text with every row popover cut out of it, each one whole."""
    opening = '<div class="site-popover site-row-pop" id="'
    while opening in page:
        target = page[page.index(opening) + len(opening) :].split('"', 1)[0]
        page = page.replace(_row_popover(page, target), "", 1)
    return page


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
    card or list is left in it, and its only popovers are its rows' own. What a row's
    popover holds is the popover's own business, so the section is read without them."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    recent = _recent_table(page)
    assert recent in section
    before_replay = section.split("site-replay", 1)[0]
    assert set(re.findall(r'<div class="(site-popover(?: [^"]*)?)"', before_replay)) == {
        "site-popover site-row-pop"
    }
    section = _outside_row_popovers(section)
    before_replay = section.split("site-replay", 1)[0]
    assert "site-popover" not in before_replay
    assert not re.search(r'class="site-card[ "]', before_replay)
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
        # Every chip in the one status cell, side by side: S, V and C, then the standing.
        chips = re.findall(r'<span class="site-chip[^"]*"[^>]*>([^<]+)</span>', status)
        record = result.record
        assert chips[:3] == [
            f"S{record['significance']['score']}",
            record["verification"],
            record["confirmation"],
        ]
        assert "<br" not in status
        assert "site-standing" not in status
    # Evan Daniel's three exact values, the closures the exact-value cards used to show.
    exact = {n for n in overview.recent_lower if overview.cases[n]["status"] == "proved"}
    shown = {r.first_n for r in newest}
    assert exact <= shown


def test_the_recent_table_lists_every_result_filtered_to_s4_and_180_days(
    page: str, overview: overview_data.Overview
) -> None:
    """Every result is a row, and no date the page fixes leaves one out: what makes the
    table recent is where its bar starts, Significance at S4 and up and Max age at 180
    days. The rows outside those are hidden in the HTML, their age measured from the
    register's own reference date, and the count is already written, so the first paint
    is the filtered table."""
    defaults = overview_sections.RECENT_DEFAULTS
    assert defaults == overview_sections.FilterDefaults(significance=4, max_age=180)
    assert not hasattr(overview_sections, "RECENT_FROM")
    recent = _recent_table(page)
    listed = re.findall(r'<tr data-result="(t-\d+)"', recent)
    assert sorted(listed) == sorted(r.id.lower() for r in overview.results)
    dates = [overview_sections.first_day(r.dated[1]) for r in overview.results]
    assert min(dates) < "2026-08-01", "the table should reach back past the old floor"
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    tools = _filter_bar(section)
    assert section.index(tools) < section.index(recent)
    assert '<label>Significance <select data-filter="s" data-bound="min">' in tools
    significance = tools.split('data-filter="s"', 1)[1].split("</select>", 1)[0]
    options = re.findall(r'<option value="(\d?)"( selected)?>([^<]+)</option>', significance)
    assert ("4", " selected", "S4 and up") in options
    assert ("3", "", "S3 and up") in options
    assert options[0] == ("", "", "All")
    assert (
        '<label>Max age <input type="number" data-filter="date" data-bound="age" '
        'min="0" placeholder="any" value="180"> days</label>'
    ) in tools
    reference = overview_sections.reference_date(overview)
    cutoff = (reference - timedelta(days=180)).isoformat()
    shown = 0
    for result in overview.results:
        row = _recent_row(recent, result.id)
        score = result.record["significance"]["score"]
        dated = overview_sections.first_day(result.dated[1])
        assert f'data-s="{score}"' in row, result.id
        assert f'data-date="{dated}"' in row, result.id
        keeps = score >= 4 and dated >= cutoff
        assert (" hidden>" in row.split(">", 1)[0] + ">") == (not keeps), result.id
        shown += keeps
    assert 0 < shown < len(overview.results)
    assert f"{shown} of {len(overview.results)} results</span>" in tools
    text = " ".join(re.sub(r"<[^>]+>", "", section).split())
    assert (
        "The table lists every result, newest first: new bounds for particular numbers of "
        "squares, found here or by others."
    ) in text
    assert "1 August" not in text
    assert "every result since" not in text
    starts = (
        "The table starts filtered to significance S4 and up and to a maximum age of 180 "
        "days; choose All and clear Max age to see every row."
    )
    assert text.count(starts) == 1
    assert "It starts filtered" not in text


def test_the_html_measures_an_age_from_the_register_and_never_from_the_clock(
    overview: overview_data.Overview, register: list[dict]
) -> None:
    """The rows a render starts `hidden`, and the count beside them, are measured from
    the newest `registered` date in the register, so two renders of one tree are the
    same bytes whatever day they run on. The script measures again from the reader's
    day (`tests/node/overview_table/`), by the same reckoning: a row dated exactly the
    maximum age ago still shows."""
    reference = overview_sections.reference_date(overview)
    assert reference == max(date.fromisoformat(str(r["registered"])) for r in register)
    source = Path(overview_sections.__file__).read_text(encoding="utf-8")
    for clock in ("today()", "now()", "time.time"):
        assert clock not in source, clock
    # The same answer `overview/table.js` gives (`ageCutoff`), which its Node test pins.
    assert overview_sections.age_cutoff(date(2026, 9, 30), 180) == "2026-04-03"
    assert overview_sections.age_cutoff(date(2026, 10, 1), 0) == "2026-10-01"
    assert overview_sections.age_cutoff(date(2024, 3, 1), 1) == "2024-02-29"

    def result(dated: str, score: int) -> overview_data.Result:
        record = {
            "id": "T-900",
            "scope": {"n_values": [11]},
            "established": dated,
            "registered": "2026-09-30",
            "significance": {"score": score},
        }
        return overview_data.Result(record, group="", credit="", ours=True)

    shows = overview_sections.shown_by_default
    recent = overview_sections.RECENT_DEFAULTS
    every = overview_sections.RESULTS_DEFAULTS
    assert every == overview_sections.FilterDefaults(significance=None, max_age=None)
    day = date(2026, 9, 30)
    assert shows(result("2026-04-03", 4), recent, day)
    assert not shows(result("2026-04-02", 5), recent, day)
    assert not shows(result("2026-09-29", 3), recent, day)
    assert not shows(result("1979", 5), recent, day)
    # A result dated after the reference is no older than any age.
    assert shows(result("2026-10-15", 4), recent, day)
    # The same row a day later is a day older.
    assert not shows(result("2026-04-03", 4), recent, date(2026, 10, 1))
    for dated, score in (("1979", 2), ("2026-04-02", 3), ("2026-09-29", 5)):
        assert shows(result(dated, score), every, day), dated
    assert shows(result("1979", 4), overview_sections.FilterDefaults(significance=4), day)
    assert not shows(result("1979", 2), overview_sections.FilterDefaults(max_age=30), day)


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


def test_recent_results_has_no_lead_line(page: str) -> None:
    """Nothing stands between the section's prose and its filter bar: the generated
    "Lead result" line the owner dropped on 2026-10-01 is gone, from the page, the
    template and the module that wrote it."""
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    assert "site-recent-lead" not in section
    assert "Lead result" not in section
    before = section.split('<div class="site-table-tools', 1)[0]
    assert re.search(r'</p>\s*<div class="site-wide">$', before)
    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    assert "RECENT_LEAD" not in template
    assert not hasattr(overview_sections, "recent_lead")
    assert not hasattr(overview_sections, "lead_result")


def _shared(page: str, name: str) -> str:
    """One shared block of README as the overview renders it: the run between its
    markers."""
    from devtools import site_documents  # noqa: PLC0415

    (block,) = (b for b in site_documents.SHARED_BLOCKS if b.name == name)
    assert page.count(block.opened) == page.count(block.closed) == 1
    return page.split(block.opened, 1)[1].split(block.closed, 1)[0]


def _intro(page: str) -> str:
    """README's first paragraph as the overview's first section renders it."""
    return _shared(page, "project-intro")


def _progress(page: str) -> str:
    """README's coverage and newest-result paragraphs as Recent Results renders them."""
    return _shared(page, "recent-progress")


#: One formula as kpress writes it: the TeX for KaTeX, then its MathML.
_KPRESS_MATH = re.compile(
    r'<span class="kpress-math [^>]*><span class="kpress-math-render"[^>]*>'
    r"\\\((.*?)\\\)</span>.*?</math></span></span>",
    re.DOTALL,
)


def _rendered_text(markup: str) -> str:
    """Rendered prose as its words, each formula written back as `$tex$`."""
    text = _KPRESS_MATH.sub(lambda match: f"${html.unescape(match.group(1))}$", markup)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", text)).split())


def _markdown_text(markdown: str) -> str:
    """Markdown prose as its words: each link reduced to its text, code spans unmarked."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", markdown)
    return " ".join(text.replace("`", "").split())


def _template_paragraphs(section: str) -> list[str]:
    """A section of the overview's template after its heading, as its paragraphs."""
    prose = re.sub(r"<!--.*?-->", "", section, flags=re.DOTALL)
    return [" ".join(part.split()) for part in prose.split("\n\n") if part.strip()]


def test_the_overviews_two_sections_are_readmes_two_blocks(page: str) -> None:
    """The overview says what README's introduction says, word for word and formula for
    formula, in two places: the first section opens with README's `project-intro` block,
    and Recent Results with its `recent-progress` block. Together they are README's three
    paragraphs, in README's order. The template holds a placeholder where each would be,
    and nothing about eleven squares of its own in the first section."""
    from devtools import site_documents  # noqa: PLC0415

    readme = site_documents.README.read_text(encoding="utf-8")
    blocks = site_documents.shared_blocks(readme)
    assert list(blocks) == ["project-intro", "recent-progress"]
    assert blocks["project-intro"] == site_documents.intro_block(readme)
    assert blocks["recent-progress"] == site_documents.progress_block(readme)
    assert _rendered_text(_intro(page)) == _markdown_text(blocks["project-intro"])
    assert _rendered_text(_progress(page)) == _markdown_text(blocks["recent-progress"])
    assert len(re.findall(r"<p>", _intro(page))) == 1
    assert len(re.findall(r"<p>", _progress(page))) == 2
    assert _markdown_text(blocks["project-intro"]).startswith("The Squares Project studies")
    assert _markdown_text(blocks["recent-progress"]).startswith(
        "The project covers the problem at every $n$."
    )
    for block in blocks.values():
        assert not re.search(r"^#", block, re.MULTILINE)
        assert "<!--" not in block
    # README keeps the three paragraphs together and in order: only the markers part them.
    intro, progress = site_documents.INTRO, site_documents.PROGRESS
    between = readme.split(intro.end, 1)[1].split(progress.begin, 1)[0]
    assert between.strip() == ""
    assert readme.index(intro.begin) < readme.index(intro.end) < readme.index(progress.end)

    template = render_overview.OVERVIEW_ARTICLE.read_text(encoding="utf-8")
    section = template.split('id="the-problem"', 1)[1].split("{{PAGE_CARDS}}", 1)[0]
    paragraphs = _template_paragraphs(section.split("</h2>", 1)[1])
    assert paragraphs[0] == "{{README_INTRO}}"
    own = " ".join(paragraphs[1:])
    assert not re.search(r"\bT-\d{3}\b", own)
    assert "eleven" not in own.lower()
    recent = template.split("## Recent Results", 1)[1].split("\n## ", 1)[0]
    assert _template_paragraphs(recent)[0] == "{{README_PROGRESS}}"


def test_recent_results_opens_with_readmes_progress_paragraphs(page: str) -> None:
    """Recent Results opens with README's two paragraphs, right under its heading and
    above the section's own prose, the filter bar and the table; the first section no
    longer holds them. The section has one opening: its own prose starts at the table,
    which lists every result, and ends on where the filter bar under it starts."""
    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    progress = _progress(page)
    assert progress in section
    assert progress not in problem
    assert "The project covers the problem at every" not in _rendered_text(problem)
    assert "settles eleven squares" not in _rendered_text(problem)
    # Only the template's own note stands between the heading and README's block.
    opening = section.split("</h2>", 1)[1].split("<!-- README recent-progress -->", 1)[0]
    assert re.sub(r"<!--.*?-->", "", opening, flags=re.DOTALL).strip() == ""
    # README's block, then the section's prose, then the filter bar, then the table.
    tools = section.index('<div class="site-table-tools')
    table = section.index(_recent_table(page))
    after = section.index("<!-- /README recent-progress -->")
    assert section.index(progress) < after < tools < table
    own = _rendered_text(section[after:tools])
    assert own.startswith(
        "The table lists every result, newest first: new bounds for particular numbers of "
        "squares, found here or by others."
    )
    assert own.endswith(
        "The table starts filtered to significance S4 and up and to a maximum age of 180 "
        "days; choose All and clear Max age to see every row."
    )
    assert own.count("The table lists every result") == 1
    assert " since " not in own
    assert "These are the recent results this project tracks" not in _rendered_text(section)


def test_recent_results_says_eleven_squares_is_settled(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """Recent Results names T-060 and case 11 through README's `recent-progress` block,
    each link at the site's own page for it, and README is in the reader tier, so the
    gate refuses a result the section names that the register does not hold."""
    from devtools import check_results, site_documents  # noqa: PLC0415

    section = page.split('id="recent-results"', 1)[1].split("<h2", 1)[0]
    intro = _progress(page)
    assert intro in section
    text = _rendered_text(intro)
    assert "settles eleven squares" in text
    assert "Trump\u2019s 1979 packing" in text
    assert "$n = 1\\ldots324$" in text
    assert '<a href="all-results.html#t-060">T-060</a>' in intro
    assert '<a href="all-results.html#t-011">T-011</a>' in intro
    assert '<a href="cases.html#n-11">case record</a>' in intro
    assert '<a href="frontier.html">frontier</a>' in intro
    assert '<a href="all-results.html">results register</a>' in intro
    assert 'id="t-060"' in results
    assert 'id="t-011"' in results
    assert 'id="n-11"' in rendered("cases.html")
    hrefs = re.findall(r'href="([^"]+)"', intro)
    review = "docs/project/reviews/review-2026-09-29-n11-optimality.md"
    assert f"{REPO_URL}/blob/{DEFAULT_BRANCH}/{review}" in hrefs
    for href in hrefs:
        assert (
            href.startswith("https://") or href.partition("#")[0] in render_overview.SITE_PAGES
        ), href
    assert site_documents.README in check_results.READER_TIER
    assert render_overview.OVERVIEW_ARTICLE in check_results.READER_TIER
    # The reader tier holds both ids through README's own text, block markers and all.
    readme = site_documents.README.read_text(encoding="utf-8")
    for result in ("T-060", "T-011"):
        assert result in site_documents.progress_block(readme), result


#: The site's own statement, the owner's words of 2026-09-30 with only hyphenation and
#: punctuation edited, and one sentence on what the project checks.
SITE_STATEMENT = (
    (
        "The Square Packing Project site collects all known historic research and "
        "current new results on the square packing problem. Work on this problem has "
        "exploded in the summer of 2026 thanks to AI-powered research efforts. This "
        "project tracks all results here and by all others known. The project also "
        "independently checks the proofs and certificates behind them, replaying each "
        "where it can, and records how far every result has been verified and confirmed."
    ),
    (
        "If you have new results or know of newer results, please file an issue to "
        "report them, and we will gladly incorporate them and cite your work."
    ),
)


def test_the_sites_own_statement_follows_readmes_introduction(page: str) -> None:
    """After README's introduction the section has two paragraphs of its own: what the
    site collects and checks, and where to report a result it lacks. The first links the
    rungs it names to their section; the second opens a new issue on the repository."""
    from devtools import site_documents  # noqa: PLC0415

    problem = page.split('id="the-problem"', 1)[1].split('id="recent-results"', 1)[0]
    own = problem.split(site_documents.OVERVIEW_INTRO_CLOSE, 1)[1].split("<div", 1)[0]
    paragraphs = re.findall(r"<p>(.*?)</p>", own, re.DOTALL)
    assert [_rendered_text(paragraph) for paragraph in paragraphs] == list(SITE_STATEMENT)
    assert '<a href="#verification-at-a-glance">verified and confirmed</a>' in paragraphs[0]
    assert 'id="verification-at-a-glance"' in page
    assert render_overview.NEW_ISSUE_URL == "https://github.com/jlevy/squares/issues/new"
    assert re.search(
        rf'<a href="{re.escape(render_overview.NEW_ISSUE_URL)}"[^>]*>file an issue</a>',
        paragraphs[1],
    )
    assert "formal" not in " ".join(SITE_STATEMENT).lower()


def _the_central_case() -> re.Pattern[str]:
    """The framing the owner refused on 2026-09-30, as `site_documents` holds README's
    shared blocks to it: eleven squares is a central case, never the central one."""
    from devtools import site_documents  # noqa: PLC0415

    return site_documents.THE_CENTRAL_CASE


@pytest.mark.parametrize(
    "path",
    [
        render_overview.REPO / "README.md",
        render_overview.OVERVIEW_ARTICLE,
        render_overview.TEMPLATES / "paper-design.md",
        render_overview.PACKING / "devtools" / "render_overview.py",
    ],
    ids=lambda path: path.name,
)
def test_no_case_is_called_the_central_one(path: Path) -> None:
    """The project covers square packing at every n. "A central case" may be said of
    eleven squares; "the central case", "its central case" and "the central open case"
    may not, in README, the overview's template, the design notes or this renderer."""
    pattern = _the_central_case()
    found = pattern.findall(path.read_text(encoding="utf-8"))
    assert not found, f"{path.name}: {found}"
    assert not pattern.search("a central case, and a central open case")
    for phrase in ("the central case", "Its central\ncase", "the central open case"):
        assert pattern.search(phrase), phrase


def card_text(fragment: str) -> str:
    """A card's text as a reader reads it, each formula as its TeX."""
    fragment = re.sub(r'<span class="kpress-math-semantic">.*?</math></span>', "", fragment)
    fragment = re.sub(r"\\\((.*?)\\\)", r"\1", fragment)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


#: The explainer's card as the owner worded it (2026-09-30), with the date the record gives.
EXPLAINER_TITLE = "New lower bounds for square packing for n = 11"
EXPLAINER_NOTE = (
    "An explainer and proof of certain lower bounds for n = 11. It explains the earlier, "
    "simpler proofs as of early September; newer optimality proofs now exist (T-060)."
)


def card_parts(page: str, target: str) -> tuple[str, str, str]:
    """A card's value and note, and the popover it opens, on `page`."""
    card = page.split(f'popovertarget="{target}"', 1)[1].split("</button>", 1)[0]
    value, note = card.split('class="site-card-value">', 1)[1].split(
        '<span class="site-card-note">'
    )
    start = page.index(f'<div class="site-popover" id="{target}" popover')
    panel = page[start:].split('<button type="button" class="site-card"', 1)[0]
    return value, note, panel


def test_the_explainer_card_says_what_the_explainer_now_is(
    page: str, results: str, rendered: Callable[[str], str]
) -> None:
    """The explainer proves the earlier, simpler lower bounds, so its card is titled and
    described as the owner put it, `n = 11` set as math. On the overview the card is the
    link to the explainer, so it holds no other; T-060, the optimality proof since
    registered, is linked from the popover of its card on the Papers page, which is a
    button. The wording stays within T-060's rungs: proved, never formally."""
    value, note = _page_card_parts(page, "explainer.html")
    _, _, panel = card_parts(rendered("papers.html"), "pop-paper-explainer")
    assert card_text(value) == EXPLAINER_TITLE
    assert card_text(note) == EXPLAINER_NOTE
    assert "kpress-math" in value
    assert "kpress-math" in note
    assert "formal" not in card_text(value + note).lower()
    assert '<a class="site-popover-also" href="all-results.html#t-060">' in panel
    assert 'id="t-060"' in results


def test_the_explainer_cards_date_is_the_records(register: list[dict]) -> None:
    """'Early September' is what the record says of the explainer's proofs: T-018, T-025
    and T-026 were established in September's first ten days, and the two editions that
    first published them went live in its first half. The owner's draft said early August,
    which the record does not support."""
    from datetime import date, datetime  # noqa: PLC0415

    from sqpack.release import PUBLICATION_HISTORY  # noqa: PLC0415

    assert overview_sections.EXPLAINER_AS_OF == "early September"
    established = [
        date.fromisoformat(str(r["established"]))
        for r in register
        if r["id"] in {"T-018", "T-025", "T-026"}
    ]
    assert len(established) == 3
    assert all((d.year, d.month) == (2026, 9) and d.day <= 10 for d in established)
    published = [
        datetime.strptime(e.first_published, "%B %d, %Y").date()  # noqa: DTZ007
        for e in PUBLICATION_HISTORY
        if e.version in {"v0.3.0", "v0.4.0"}
    ]
    assert len(published) == 2
    assert all((d.year, d.month) == (2026, 9) and d.day <= 15 for d in published)


PAPER_CARD = re.compile(
    r'<button type="button" class="site-card" popovertarget="([^"]+)" data-go="page" '
    r'data-card-size="large">'
)
#: A popover's quiet links, beside its button: each one's address and its words.
ALSO = re.compile(r'<a class="site-popover-also" href="([^"]+)">([^<]+)</a>')


def test_the_papers_page_holds_one_large_card_for_each_paper(
    rendered: Callable[[str], str],
) -> None:
    """`papers.html` is one large card per paper and nothing else in cards, in the order of
    the one list that defines them (`overview_sections.PAPERS`), so a new paper is one
    entry there. The whole card is the button, its popover frames the paper in its
    embedded view, and the popover's one button expands to the paper's own page. (The
    overview's page cards are plain links instead, with no popover.)"""
    page = rendered("papers.html")
    papers = overview_sections.PAPERS
    assert [paper.href for paper in papers] == [
        "n11-optimality/t-060-explainer.html",
        "explainer.html",
        "tutorial.html",
    ]
    assert {paper.size for paper in papers} == {"large"}
    cards = PAPER_CARD.findall(page)
    assert cards == [
        "pop-paper-n11-optimality-t-060-explainer",
        "pop-paper-explainer",
        "pop-paper-tutorial",
    ]
    assert page.count('class="site-card"') == len(cards)
    for target, paper in zip(cards, papers, strict=True):
        assert paper.href in render_overview.SITE_PAGES
        _, _, panel = card_parts(page, target)
        assert ACTION.findall(panel) == [(paper.href, "page")], target
        frame = f'<iframe class="site-popover-frame" src="{paper.href}?view=embed"'
        assert frame in panel, target
        assert ALSO.findall(panel) == list(paper.links), target
    assert render_overview.POPOVER_SCRIPT.read_text(encoding="utf-8") in page


def test_a_popover_carries_every_quiet_link_its_card_is_given() -> None:
    """A card is a button and holds no link, so what its note names is linked from its
    popover, beside the button: `also` first, then each of `links`, in order. The
    explainer's are the optimality links, listed in one place: the paper that explains
    the newer proof, then T-060's row."""
    markup = overview_sections.card(
        "pop-x",
        "X",
        "x",
        "x",
        href="x.html",
        action="Open",
        also=("a.html", "A"),
        links=(("b.html", "B"), ("c.html", "C")),
    )
    assert ALSO.findall(markup) == [("a.html", "A"), ("b.html", "B"), ("c.html", "C")]
    assert markup.count("<a ") == 4
    explainer = overview_sections.EXPLAINER
    assert explainer is overview_sections.PAPERS[1]
    assert explainer.href == "explainer.html"
    assert explainer.links == overview_sections.OPTIMALITY_LINKS
    assert explainer.links == (
        ("n11-optimality/t-060-explainer.html", "The optimality paper"),
        ("all-results.html#t-060", "The optimality proof, T-060"),
    )


def test_the_papers_page_says_what_each_paper_is(
    page: str, rendered: Callable[[str], str]
) -> None:
    """The explainer's card is its card on the overview, word for word, and its popover
    here links the optimality paper and T-060, which the overview's card, a plain link
    to the explainer, cannot; the tutorial's is `TUTORIAL.md`'s own opening, whom it is
    for and what it covers. The overview keeps a card for the explainer and the
    tutorial."""
    papers = rendered("papers.html")
    value, note, panel = card_parts(papers, "pop-paper-explainer")
    assert card_text(value) == EXPLAINER_TITLE
    assert card_text(note) == EXPLAINER_NOTE
    assert (value, note) == _page_card_parts(page, "explainer.html")
    also = (
        '<a class="site-popover-also" href="n11-optimality/t-060-explainer.html">'
        "The optimality paper</a>"
        ' <a class="site-popover-also" href="all-results.html#t-060">'
    )
    assert also in panel

    value, note, _ = card_parts(papers, "pop-paper-tutorial")
    assert card_text(value) == "Square packing from first principles"
    opening = (overview_data.REPO / "TUTORIAL.md").read_text(encoding="utf-8")
    opening = " ".join(opening.split("## Contents", 1)[0].split())
    assert "Square Packing from First Principles" in opening
    assert "anyone new to the problem" in card_text(note)
    for phrase in (
        "what the objects are",
        "why the approach is shaped the way it is",
        "what the research has and has not established",
        "linear programming",
        "is first needed",
    ):
        assert phrase in card_text(note), phrase
        assert phrase in opening, phrase
    assert {"explainer.html", "tutorial.html"} <= {href for href, _, _ in _page_cards(page)}


def test_the_optimality_papers_card_says_what_t060s_rungs_allow(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The optimality paper is the first card: served where its renderer writes it,
    titled as its renderer titles it, in sentence case, and described as explaining the
    accepted proof, T-060, in the words T-060's rungs allow, V4 and C5: a proof, never a
    formal one. Its popover frames the paper and links T-060's row."""
    from devtools import render_n11_optimality_explainer as renderer  # noqa: PLC0415

    paper = overview_sections.PAPERS[0]
    assert paper.href == overview_sections.OPTIMALITY_PAPER == renderer.SITE_PATH
    assert paper.href in render_overview.SITE_PAGES
    assert paper.title.lower() == renderer.TITLE.lower()
    assert paper.title == "Why eleven squares need this much room"
    value, note, panel = card_parts(
        rendered("papers.html"), "pop-paper-n11-optimality-t-060-explainer"
    )
    assert card_text(value) == paper.title
    text = card_text(note)
    assert text.startswith("Explains the accepted proof that Trump\u2019s 1979 packing")
    assert "(T-060)" in text
    assert "is optimal" in text
    assert "s(11) = 3.8770835" in text
    assert "kpress-math" in note
    assert "formal" not in text.lower()
    t060 = next(r for r in register if r["id"] == "T-060")
    assert (t060["verification"], t060["confirmation"]) == ("V4", "C5")
    assert ALSO.findall(panel) == [("all-results.html#t-060", "The optimality proof, T-060")]
    assert "Expand the optimality paper</a>" in panel


def test_the_papers_page_introduces_the_papers_within_t060s_rungs(
    register: list[dict], rendered: Callable[[str], str]
) -> None:
    """The introduction names T-060 with a link to its row, in the words its rungs allow,
    V4 and C5: proved optimal, machine-verified and reviewed, never formally. Its
    template is in the reader tier, so the gate refuses a result it names that the
    register does not hold."""
    from devtools import check_results  # noqa: PLC0415

    page = rendered("papers.html")
    article = page.split("<article", 1)[1].split("</article>", 1)[0]
    text = card_text(article)
    assert re.search(r"<h1\b[^>]*>Papers</h1>", article)
    assert '<a href="all-results.html#t-060">T-060</a>' in article
    assert "proved optimal" in text
    assert "machine-verified and reviewed here" in text
    assert "the optimality paper explains that proof" in " ".join(text.split())
    assert "formal" not in text.lower()
    t060 = next(r for r in register if r["id"] == "T-060")
    assert (t060["verification"], t060["confirmation"]) == ("V4", "C5")
    assert render_overview.PAPERS_ARTICLE in check_results.READER_TIER
    assert render_overview.PAPERS_ARTICLE in render_overview.RENDER_INPUTS


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


def test_card_headlines_take_the_page_titles_sans_face_and_weight() -> None:
    """A card's headline, and its popover's repeat of it, is set in the sans face at the
    medium weight by the same two tokens the page title uses, which KPress's sans `h3`
    resolves to as well; no value of its own."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    title = css[css.index(".site-hero h1,\n.kpress .site-title {") :]
    headline = css[
        css.index(".kpress .site-card .site-card-value,\n.site-popover .site-popover-value {") :
    ]
    for rule in (title[: title.index("}")], headline[: headline.index("}")]):
        assert "font-family: var(--kpress-font-sans);" in rule
        assert "font-weight: var(--site-font-weight-sans-medium);" in rule
    assert "--site-font-weight-sans-medium: var(--paper-font-weight-sans-medium);" in css
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert "--paper-font-weight-sans-medium: 550;" in text


def test_every_heading_and_headline_shares_one_leading() -> None:
    """One line height, 1.15, for every heading on screen: the text layer every page
    carries sets it on `h1` to `h6`, and the site's stylesheet reads the same token for a
    card's headline, a popover's, a case record's title, a page's subtitle and a column's
    name in the rating ladders. Print is left to KPress, and a formula in any of them
    takes no line of its own."""
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    assert text.count("--paper-heading-leading: 1.15;") == 1
    assert (
        "@media screen {\n  .kpress-prose :is(h1, h2, h3, h4, h5, h6) {\n"
        "    line-height: var(--paper-heading-leading);\n  }\n}"
    ) in text
    assert text.count("var(--paper-heading-leading)") == 1
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    for selector in (
        ".kpress .site-card .site-card-value,\n.site-popover .site-popover-value {",
        ".kpress .site-case-title {",
        ".kpress .site-hero .subtitle {",
        ".kpress .site-ladders .site-ladders-name {",
    ):
        rule = css[css.index(selector) :]
        assert "line-height: var(--paper-heading-leading);" in rule[: rule.index("}")], selector
    assert css.count("var(--paper-heading-leading)") == 4
    assert "--paper-heading-leading:" not in css
    math = css[css.index(".site-page :is(h1, h2, h3, h4) :is(.kpress-math, .katex),\n") :]
    math = math[: math.index("}")]
    assert ":is(.site-card-value, .site-popover-value, .site-case-title," in math
    assert "  :is(.kpress-math, .katex) {\n" in math
    assert "line-height: 0;" in math
    # The explainer's hero title keeps KPress's own leading, which its math is fitted to.
    shell = (render_overview.TEMPLATES / "explainer-shell.html").read_text(encoding="utf-8")
    assert "paper-heading-leading" not in shell
    assert "height: 1.05em !important;" in shell


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
    assert "--site-page-top: 4rem;" in nav
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


def test_section_headings_share_one_space_above_and_one_below() -> None:
    """The space above an `h2` and the space below it are two tokens in the text layer
    both the site and the explainer read. Each has a screen value and, under print, the
    paper's own, so the explainer's PDF paginates as it did."""
    text = render_overview.PAPER_TYPE_CSS.read_text(encoding="utf-8")
    start = "@media print {\n  .kpress {\n    --paper-section-space"
    screen, _, printed = text.partition(start)
    assert "  --paper-section-space: calc(var(--kpress-font-size-base) * 2.7);\n" in screen
    assert "  --paper-section-space-below: 1.7rem;\n" in screen
    assert printed.startswith(": calc(var(--kpress-font-size-base) * 2.8);\n")
    assert "    --paper-section-space-below: 1.3rem;\n  }\n}" in printed[:120]
    shell = (render_overview.TEMPLATES / "explainer-shell.html").read_text(encoding="utf-8")
    for css in (render_overview.SITE_CSS.read_text(encoding="utf-8"), shell):
        assert (
            "margin-block: var(--paper-section-space) var(--paper-section-space-below);" in css
        )
        assert "var(--paper-section-space) 1.3rem" not in css


def test_a_page_title_stands_one_space_above_what_follows_it() -> None:
    """The space under a page's title is one token: around its subtitle, and under a title
    that has none, a document's own `h1` among them, on screen. A hero title with a
    subtitle hands the space to the subtitle."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-subtitle-space: 1.5rem;") == 1
    assert "  margin-block: var(--site-subtitle-space);\n" in css
    assert (
        "@media screen {\n  .site-page h1 {\n"
        "    margin-block-end: var(--site-subtitle-space);\n  }\n}\n"
        ".kpress .site-hero:has(.subtitle) h1 {\n  margin-block-end: 0;\n}"
    ) in css
    shell = (render_overview.TEMPLATES / "explainer-shell.html").read_text(encoding="utf-8")
    assert "  .cert-page .hero .credits { margin-block-start: 2.25rem; }\n}" in shell
    assert "  margin-block: 2rem 2.2rem;\n" in shell


def test_every_table_stands_one_shared_space_from_the_text_around_it() -> None:
    """The space above and below a table is one token: above the filter bar of a table
    that has one, below every table's wrap, around the awaiting-replay disclosure, and
    around a document's own table, which KPress wraps. The rules that read it are for
    the screen alone, so print keeps KPress's spacing; the bar is not printed at all."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-table-space: 2rem;") == 1
    bar = css[css.index("\n.site-table-tools {") :]
    assert "margin-block: var(--site-table-space) 0.5rem;" in bar[: bar.index("}")]
    start = css.index("@media screen {\n  .kpress details.site-replay,")
    screen = css[start : css.index("\n}\n", start)]
    assert (
        "  .kpress details.site-replay,\n  .kpress-table-wrap,\n  .site-table-wrap {\n"
        "    margin-block: var(--site-table-space);\n  }"
    ) in screen
    # The bar keeps its own gap to its table, and the disclosure's table sits flush.
    assert (
        "  .site-table-tools + .site-table-wrap,\n  .site-replay .site-table-wrap {\n"
        "    margin-block-start: 0;\n  }"
    ) in screen
    assert "  .site-replay .site-table-wrap {\n    margin-block-end: 0;\n  }" in screen
    # The rating ladders, which are no table, stand the same space clear of the text.
    ladders = css[css.index("@media screen {\n  .site-ladders-frame {") :]
    assert "margin-block: var(--site-table-space);" in ladders[: ladders.index("}")]
    assert css.count("var(--site-table-space)") == 3
    assert "@media print {\n  .site-nav,\n  .site-table-tools {\n    display: none;" in css
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    assert "| Above and below a table | `--site-table-space` | 2rem, 32px |" in design


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
    """Every hero's subtitle ("A survey of all reviewed results") is set from one scale of
    the sans base, a small step above it."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert "--site-subtitle-scale: 1.1;" in css
    rule = css[css.index(".kpress .site-hero .subtitle {") :]
    assert "var(--site-subtitle-scale)" in rule[: rule.index("}")]


def test_the_frontier_results_and_papers_pages_carry_their_subtitles(
    rendered: Callable[[str], str],
) -> None:
    """Each page's subtitle is one line under its title. The atlas's names its range as a
    formula, kpress's own math markup, with both ends read from the case records; the
    results page's carries no count, so its template takes none."""
    from devtools.render_frontier_page import (  # noqa: PLC0415
        FRONTIER_ARTICLE,
        frontier_cases,
        math_html,
    )

    numbers = [case["n"] for case in frontier_cases()]
    cases = math_html(rf"n = {min(numbers)}, \ldots, {max(numbers)}")
    for name, subtitle in (
        ("frontier.html", f"A survey of everything known for cases {cases}"),
        (render_overview.RESULTS_PAGE, "A survey of all reviewed results"),
        ("papers.html", "Papers and interactive explanations for specific results"),
    ):
        page = rendered(name)
        assert page.count('<p class="subtitle">') == 1, name
        assert f'<p class="subtitle">{subtitle}</p>' in page, name
    assert 'class="kpress-math' in cases
    assert "<var>" not in cases
    assert "{{CASE_RANGE}}" in FRONTIER_ARTICLE.read_text(encoding="utf-8")
    assert "{{COUNT}}" not in render_overview.RESULTS_ARTICLE.read_text(encoding="utf-8")


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


def test_a_headline_that_is_all_math_sets_it_serif(page: str) -> None:
    """A headline that is mathematics standing alone, such as `n = 11`, is marked for
    serif mathematics, on a card and in its popover; a headline with words in it carries
    no mark, so its math follows the words into the sans. No popover forces sans
    mathematics on everything inside it."""
    formula = overview_data.math_html("n = 11")
    assert overview_sections.is_all_math(formula)
    assert overview_sections.is_all_math(f" {formula} {formula}\n")
    for mixed in (f"Earlier {formula} lower bounds", f"{formula}.", "Results", ""):
        assert not overview_sections.is_all_math(mixed), mixed
    assert overview_sections.SERIF_MATH == 'data-math-face="serif"'

    def built(value: str) -> str:
        return overview_sections.card(
            "pop-x", "Case", value, "A note.", href="#recent-results", action="Go"
        )

    alone = built(formula)
    assert f'<span class="site-card-value" data-math-face="serif">{formula}</span>' in alone
    assert f'<p class="site-popover-value" data-math-face="serif">{formula}</p>' in alone
    assert "data-math-face" not in built(f"Earlier {formula} lower bounds")
    link = overview_sections.link_card("frontier.html", "Case", formula, "A note.")
    assert f'<span class="site-card-value" data-math-face="serif">{formula}</span>' in link
    assert "data-math-face" not in overview_sections.link_card(
        "frontier.html", "Case", f"{formula} to 100", "A note."
    )

    headlines = re.findall(
        r'<span class="site-card-value"([^>]*)>(.*?)</span><span class="site-card-note">', page
    ) + re.findall(r'<p class="site-popover-value"([^>]*)>(.*?)</p>', page)
    assert len(headlines) > len(overview_sections.DOCUMENTS)
    for attributes, value in headlines:
        if "data-atlas-title" in attributes:
            continue
        marked = overview_sections.SERIF_MATH in attributes
        assert marked == overview_sections.is_all_math(value), value

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


def test_a_wide_block_keeps_one_gutter_inside_the_pages_content_area() -> None:
    """A table and its filter bar, a row of cards, the atlas grid and the film stop one
    token short of the page's content area on either side. That area is KPress's page
    container, `100cqw`, never the window: `100vw` counts a scrollbar the layout does
    not, and a narrow page clips at the document's edge. A wide track, a table's bleed
    and the film all read the one room; a document's own table keeps to its column in
    KPress's own narrow band, a phone's row cards are padded, and a result overview's
    bounds scroll inside their own box."""
    css = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert css.count("--site-wide-gutter: 0.5rem;") == 1
    assert css.count("--site-wide-gutter:") == 1
    wide = css[css.index(".site-page .site-wide {") :]
    wide = wide[: wide.index("}")]
    assert "--site-wide-room: calc(100cqw - 2 * var(--site-wide-gutter));" in wide
    assert "max-width: min(var(--site-wide), var(--site-wide-room));" in wide
    rule = css[css.index(TABLE_BLEED) :]
    assert "    var(--site-wide-room),\n" in rule[: rule.index("\n}")]
    film = css[css.index(".site-page .site-film-frame {") :]
    assert "min(100cqw - 2 * var(--site-wide-gutter), " in film[: film.index("}")]
    # No block in the page's flow is sized from the window: only a popover, which is
    # laid out in the window's own top layer, and a table's growth above 1280 pixels,
    # which the room still caps.
    sized = [
        line.strip()
        for line in css.splitlines()
        if "100vw" in line and re.match(r"\s*[\w-]+:\s", line)
    ]
    assert sized == [
        "--site-table-grow: max(0px, 100vw - var(--site-table-bleed-from));",
        "max-width: min(36rem, 100vw - 2rem);",
        "inline-size: min(46rem, 100vw - 2rem);",
        "inline-size: min(62rem, 100vw - 2rem);",
        "inline-size: calc(100vw - 1rem);",
    ]
    assert (
        "@container kpress-doc (max-width: 47.99rem) {\n"
        "  .kpress .site-page .kpress-table-wrap {\n    max-inline-size: 100%;\n  }\n}"
    ) in css
    row = css[css.index("  .site-results tr {") :]
    assert "padding: 0.7rem 0.5rem;" in row[: row.index("}")]
    result = render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8")
    bounds = result[result.index(".site-result-bounds {") :]
    bounds = bounds[: bounds.index("}")]
    assert "max-inline-size: 100%;" in bounds
    assert "overflow-x: auto;" in bounds


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
    parser.feed(site_renders.html(name))
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
    """`result_row_popover_body` is the one source of what a result's row opens to, on
    the overview's recent table and on the results page alike: the result's whole
    overview. It is written once, as the result's fragment beside the pages; a row's
    popover names that fragment and holds the short detail, and no cell repeats either."""
    from devtools import result_overview  # noqa: PLC0415

    result = overview_sections.recent_results(overview)[0]
    body = overview_sections.result_row_popover_body(result, overview)
    assert body == result_overview.result_popover_html(result, overview)
    assert body.startswith(
        f'<div class="site-result" data-result-overview="{result.id.lower()}">'
    )

    def marked(result: overview_data.Result, _: overview_data.Overview) -> str:
        return f"<p>BODY OF {result.id}</p>"

    monkeypatch.setattr(overview_sections, "result_row_popover_body", marked)
    fragments = render_overview.result_fragments()
    assert [(file.name, file.html) for file in fragments] == [
        (f"result/{row.id.lower()}.html", f"<p>BODY OF {row.id}</p>\n")
        for row in overview.results
    ]
    for table, listed in (
        (overview_sections.results_table(overview), overview.results),
        (overview_sections.recent_table(overview), overview_sections.recent_results(overview)),
    ):
        assert "BODY OF" not in table
        for row in listed:
            panel = _row_popover(table, f"pop-result-{row.id.lower()}")
            opening = (
                '<div class="site-row-pop-body" '
                f'data-row-pop-src="result/{row.id.lower()}.html">'
                '<dl class="site-detail"><dt>Claim</dt>'
            )
            assert table.count(opening) == 1, row.id
            assert opening in panel, row.id
            for term in ("<dt>Significance</dt>", "<dt>Novelty</dt>"):
                assert term in panel, row.id


#: What the two pages that list results may weigh. The result overviews are 2.8 MB
#: between them; a page that carried them, as both once would have, crosses its ceiling.
#: The shell every page carries, its faces and math, is about 1.8 MB of each.
PAGE_CEILINGS = {"index.html": 4_300_000, render_overview.RESULTS_PAGE: 2_800_000}


def test_no_page_carries_a_result_overview(
    page: str, results: str, overview: overview_data.Overview
) -> None:
    """A result's overview is fetched when its row is opened, never written into a page:
    the two pages that list results hold only each row's short detail and the address
    of its overview, and stay under their ceilings. The overviews are served from one
    directory that no page's address shadows."""
    for name, html_text in (("index.html", page), (render_overview.RESULTS_PAGE, results)):
        assert "data-result-overview=" not in html_text, name
        assert 'class="site-result"' not in html_text, name
        size = len(html_text.encode("utf-8"))
        assert size < PAGE_CEILINGS[name], f"{name} is {size:,} bytes"
    sources = re.findall(r'data-row-pop-src="([^"]+)"', results)
    assert sources == [
        overview_sections.result_fragment(result.id)
        for _, members in overview.groups
        for result in members
    ]
    assert set(re.findall(r'data-row-pop-src="([^"]+)"', page)) == {
        overview_sections.result_fragment(result.id)
        for result in overview_sections.recent_results(overview)
    }
    directory = overview_sections.RESULT_FRAGMENTS
    assert directory == "result"
    served = {
        name.split("/", 1)[0].removesuffix(".html") for name in render_overview.SITE_PAGES
    }
    assert directory not in served
    assert render_overview.ROW_POPOVER_SCRIPT.read_text(encoding="utf-8").count(
        "data-row-pop-src"
    )


def test_the_site_writes_each_result_overview_once_and_drops_a_withdrawn_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`write_site` writes the pages at the root and the fragments in their directory,
    and removes a fragment a directory built earlier still holds for a result the
    register no longer has; nothing else in the directory is touched."""
    files = [
        render_overview.Page("index.html", "<p>page</p>"),
        render_overview.Page("result/t-001.html", "<p>one</p>\n"),
    ]
    (tmp_path / "result").mkdir()
    (tmp_path / "result" / "t-999.html").write_text("withdrawn", encoding="utf-8")
    (tmp_path / "explainer.html").write_text("another build's", encoding="utf-8")
    render_overview.write_site(tmp_path, files)
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*.html")
    ) == [
        "explainer.html",
        "index.html",
        "result/t-001.html",
    ]
    assert (tmp_path / "result" / "t-001.html").read_text(encoding="utf-8") == "<p>one</p>\n"
    monkeypatch.setattr(render_overview, "render_all", lambda: files[:1])
    monkeypatch.setattr(render_overview, "result_fragments", lambda: files[1:])
    assert [file.name for file in render_overview.render_site()] == [
        "index.html",
        "result/t-001.html",
    ]
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 0
    (tmp_path / "result" / "t-001.html").write_text("changed", encoding="utf-8")
    assert render_overview.main(["--output", str(tmp_path), "--check"]) == 1


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
    face = overview_sections.headline_math_face(overview_sections.tex_bounds(result.summary))
    for panel in (away, here):
        assert f'<span class="site-card-label">{result.id}</span>' in panel
        assert f'<p class="site-popover-value"{face} id="{target}-title">' in panel
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
    assert "<template" not in plain.popover
    assert "data-row-pop-src" not in plain.popover
    assert overview_sections.plain_text("`s(11) >= 3`,  reported") == "s(11) >= 3, reported"


def test_a_deferred_row_body_waits_in_a_template_with_a_fallback_for_no_scripts(
    overview: overview_data.Overview,
) -> None:
    """A body too heavy to render once per row at load is held in a `<template>`, which
    `row-popover.js` places when the popover first opens (`tests/node/overview_rows`),
    with a `<noscript>` beside it for a reader whose template would stay inert. A body
    too heavy to carry at all is named instead (`source`), with the short form in its
    place for the script to replace; a body is one or the other. The result rows take
    the second way, on both tables, so neither holds a template."""
    held = overview_sections.row_detail(
        "pop-z",
        name="n",
        trigger="k",
        label="l",
        title="t",
        body="<p>long</p>",
        deferred=True,
        fallback="<p>short</p>",
    )
    assert (
        '<div class="site-row-pop-body"><template data-row-pop-body><p>long</p></template>'
        "<noscript><p>short</p></noscript></div>"
    ) in held.popover
    bare = overview_sections.row_detail(
        "pop-z", name="n", trigger="k", label="l", title="t", body="<p>long</p>", deferred=True
    )
    assert "<noscript>" not in bare.popover
    named = overview_sections.row_detail(
        "pop-z",
        name="n",
        trigger="k",
        label="l",
        title="t",
        body="<p>short</p>",
        source="beside/z.html?a=1&b=2",
    )
    assert (
        '<div class="site-row-pop-body" data-row-pop-src="beside/z.html?a=1&amp;b=2">'
        "<p>short</p></div>"
    ) in named.popover
    with pytest.raises(SystemExit, match="in a template or is fetched, not both"):
        overview_sections.row_detail(
            "pop-z",
            name="n",
            trigger="k",
            label="l",
            title="t",
            body="b",
            deferred=True,
            source="z",
        )
    for table in (
        overview_sections.results_table(overview),
        overview_sections.recent_table(overview),
    ):
        assert "<template" not in table
        assert table.count("data-row-pop-src=") == table.count(
            '<div class="site-popover site-row-pop"'
        )


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
    ("date", "age"),
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


def _without_defaults(bar: str) -> str:
    """A bar less what is a table's own: its count, which option each select starts at
    and the value an input starts with."""
    bar = _COUNT.sub(r"\1</span>", bar).replace(" selected>", ">")
    return re.sub(r'(<input\b[^>]*?) value="[^"]*"', r"\1", bar)


def test_both_tables_of_results_carry_the_identical_filter_set(page: str, results: str) -> None:
    """The overview's recent table and the results page's table sit under one bar: the
    same controls with the same choices in the same order. They differ only in where
    two of them start, and in the count. Recent Results starts at Significance S4 and up
    and a maximum age of 180 days; the results page starts with both off, and every
    other control starts at All on both. No control is a date, and none is a range."""
    here = _filter_bar(page.split('id="recent-results"', 1)[1])
    there = _filter_bar(results)
    assert _without_defaults(here) == _without_defaults(there)
    assert here != there
    assert _controls(here) == _controls(there) == RESULT_FILTERS
    everything = {"s": "", "v": "", "c": "", "standing": "", "source": ""}
    for bar in (here, there):
        assert bar.count(" selected>") == bar.count("<select ") == 5
        assert bar.count("<input ") == 2
        assert 'type="date"' not in bar
        assert " checked" not in bar
        assert "<label>Max age <input " in bar
        assert "> days</label>" in bar
    assert dict(_SELECTED.findall(here)) == everything | {"s": "4"}
    assert dict(_SELECTED.findall(there)) == everything
    started = r'<input\b[^>]*data-bound="([a-z]+)"[^>]* value="([^"]*)"'
    assert re.findall(started, here) == [("age", "180")]
    assert re.findall(started, there) == []
    assert page.count('class="site-table-tools site-result-filters"') == 1
    assert results.count('class="site-table-tools site-result-filters"') == 1


def test_the_filter_bar_is_one_helpers_and_reads_the_whole_register(
    overview: overview_data.Overview,
) -> None:
    """`result_filters` writes the bar for both tables, each passing where its own
    starts. Its choices come from the whole register, so a table that lists fewer
    results offers the same ones; only its count is the table's. Each rung select offers
    the rubric's levels above the lowest as floors, the top one bare."""
    recent = overview_sections.recent_results(overview)
    assert sorted(r.id for r in recent) == sorted(r.id for r in overview.results)
    assert [r.id for r in recent] == [
        r.id
        for r in sorted(
            overview.results,
            key=lambda r: (overview_sections.first_day(r.dated[1]), r.id),
            reverse=True,
        )
    ]
    every = overview_sections.RESULTS_DEFAULTS
    full = overview_sections.result_filters(overview, overview.results, every)
    part = overview_sections.result_filters(overview, recent, overview_sections.RECENT_DEFAULTS)
    few = overview_sections.result_filters(overview, recent[:3], every)
    assert full in overview_sections.results_table(overview)
    assert part in overview_sections.recent_table(overview)
    assert few.endswith(">3 results</span></div>")
    assert _COUNT.sub("", full) == _COUNT.sub("", few)
    assert _without_defaults(full) == _without_defaults(part)
    for defaults in (every, overview_sections.RECENT_DEFAULTS):
        assert overview_sections.result_filters(overview, [], defaults).endswith(
            ">0 results</span></div>"
        )
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
    assert 'data-bound="age" min="0" placeholder="any"> days</label>' in full
    assert 'data-bound="age" min="0" placeholder="any" value="180"> days</label>' in part
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


def test_the_results_page_starts_with_every_result_showing(
    results: str, overview: overview_data.Overview
) -> None:
    """The results page's bar starts with Significance at All and no maximum age, so no
    row and no group heading is `hidden` in its HTML and its count is the whole
    register's."""
    for result in overview.results:
        tag = _row(results, result.id).split(">", 1)[0] + ">"
        assert not tag.endswith(" hidden>"), result.id
    assert f">{len(overview.results)} results</span>" in _filter_bar(results)
    headings = re.findall(r'<tr class="site-group-row" data-group="[^"]+"( hidden)?>', results)
    assert len(headings) == len(overview.groups)
    assert not any(headings)
    text = " ".join(re.sub(r"<[^>]+>", "", results).split())
    assert "The table starts with every result showing." in text
    assert "case and age, and they combine." in text
    assert "starts filtered" not in text


def test_rows_outside_a_tables_defaults_are_hidden_in_the_html_and_stay_in_it(
    overview: overview_data.Overview,
) -> None:
    """Under defaults that hide rows, as the overview's are, a row outside them is
    `hidden` in the HTML, never left out of it, and the count is written for the rows
    left, so the first paint is the filtered table. A group heading with no row left
    under it is hidden with them. The results table is the one with groups, so it is
    rendered here under the overview's defaults."""
    defaults = overview_sections.RECENT_DEFAULTS
    reference = overview_sections.reference_date(overview)
    table = overview_sections.results_table(overview, defaults)
    shown = 0
    for result in overview.results:
        tag = _row(table, result.id).split(">", 1)[0] + ">"
        keeps = overview_sections.shown_by_default(result, defaults, reference)
        assert tag.endswith(" hidden>") == (not keeps), result.id
        shown += keeps
    assert 0 < shown < len(overview.results)
    assert f"{shown} of {len(overview.results)} results</span>" in _filter_bar(table)
    headings = re.findall(r'<tr class="site-group-row" data-group="[^"]+"( hidden)?>', table)
    assert len(headings) == len(overview.groups)
    for hidden, (title, members) in zip(headings, overview.groups, strict=True):
        left = any(
            overview_sections.shown_by_default(result, defaults, reference)
            for result in members
        )
        assert bool(hidden) == (not left), title
    assert {bool(hidden) for hidden in headings} == {True, False}


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
