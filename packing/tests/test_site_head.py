"""What every page says of itself in its head, and the one card they all name.

`render_overview.head_tags` writes a page's title, description, canonical link and link
preview from a small record, for every page kind: the site's own pages, the two papers
and the workbench. These hold the function, the pages it is rendered into here, the
checks the deployed site gets from `check_published_site`, and the card
`devtools.social_card` draws. The papers' and the workbench's own heads are held in
their modules' tests (`test_n11_lower_bounds_explainer`, `test_render_n11_optimality_review`,
`packages/workbench/tests/test_site_nav.py`).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools import (
    check_published_site,
    overview_sections,
    render_overview,
    rung_scale,
    social_card,
)
from devtools.check_published_site import (
    REQUIRED_META,
    forwarder_problems,
    head_checks,
    head_problems,
    local_head_checks,
    read_head,
    shared_descriptions,
)
from devtools.render_frontier_page import packing_svg
from devtools.render_overview import (
    DESCRIPTION_LIMIT,
    PROJECT_NAME,
    SITE_URL,
    SOCIAL_CARD,
    SOCIAL_CARD_HEIGHT,
    SOCIAL_CARD_WIDTH,
    PageMeta,
    canonical_url,
    head_tags,
    page_title,
)
from tests import site_renders

RESULTS = PageMeta(
    name="Every Result",
    description="Every reviewed result, with its claim, its credit and its ratings.",
    path="all-results.html",
)


def document(head: str) -> str:
    """A page around a head, as the reader meets one."""
    return f'<!doctype html><html lang="en"><head>{head}</head><body><p>Text</p></body></html>'


@pytest.fixture(scope="module")
def pages() -> dict[str, str]:
    """Every page `render_overview` builds, from the process's one render of each."""
    return site_renders.pages()


@pytest.fixture(scope="module")
def card() -> bytes:
    return social_card.card_png()


def test_head_tags_writes_each_tag_once_from_a_page_record() -> None:
    """One record gives the whole set: the title, the description, the canonical link,
    Open Graph and Twitter, each once, the addresses in full under the published root."""
    head = read_head(document(head_tags(RESULTS)))
    url = SITE_URL + "all-results.html"
    assert head.titles == ("Every Result · The Squares Project",)
    assert head.link("canonical") == [url]
    assert [key for key, _ in head.metas] == list(REQUIRED_META)
    assert dict(head.metas) == {
        "description": RESULTS.description,
        "og:type": "website",
        "og:site_name": "The Squares Project",
        "og:locale": "en_US",
        "og:title": "Every Result",
        "og:description": RESULTS.description,
        "og:url": url,
        "og:image": SITE_URL + "social-card.png",
        "og:image:type": "image/png",
        "og:image:width": "1200",
        "og:image:height": "630",
        "og:image:alt": render_overview.social_card_alt(),
        "twitter:card": "summary_large_image",
        "twitter:title": "Every Result",
        "twitter:description": RESULTS.description,
        "twitter:image": SITE_URL + "social-card.png",
        "twitter:image:alt": render_overview.social_card_alt(),
    }
    assert head_problems(document(head_tags(RESULTS)), url) == []
    # Open Graph's tags are `property` and the rest are `name`, which consumers require.
    tags = head_tags(RESULTS)
    assert '<meta property="og:title" content="Every Result">' in tags
    assert '<meta name="twitter:title" content="Every Result">' in tags
    assert 'name="og:' not in tags
    assert 'property="twitter:' not in tags


def test_the_overview_is_titled_with_the_projects_name_alone() -> None:
    """A page's title is its own name and then the project's; the overview's name is the
    project's, so it is written once and not on both sides of the dot."""
    assert page_title("Papers") == "Papers · The Squares Project"
    assert page_title(PROJECT_NAME) == PROJECT_NAME == "The Squares Project"
    head = read_head(
        document(head_tags(PageMeta(PROJECT_NAME, "The front door.", "index.html")))
    )
    assert head.titles == (PROJECT_NAME,)
    assert head.meta("og:title") == head.meta("og:site_name") == [PROJECT_NAME]
    assert head.link("canonical") == head.meta("og:url") == [SITE_URL]


def test_a_page_is_canonical_at_the_address_it_is_served_at() -> None:
    """A directory's `index.html` is served as the directory: the overview at the root,
    the workbench at `workbench/`. Every other page is served under its own name."""
    assert canonical_url("index.html") == SITE_URL == "https://jlevy.github.io/squares/"
    assert canonical_url("workbench/index.html") == SITE_URL + "workbench/"
    assert canonical_url("papers.html") == SITE_URL + "papers.html"
    nested = "papers/n11-optimality-review.html"
    assert canonical_url(nested) == SITE_URL + nested
    # A directory that only forwards is canonical nowhere: its forwarder names the paper.
    assert canonical_url("n11-optimality/index.html") == SITE_URL + "n11-optimality/"


def test_what_a_record_says_is_escaped_and_read_back_whole() -> None:
    """A description with a quote, an ampersand and an angle bracket is one attribute."""
    said = 'Squares & "bounds" for n < 12, the project\'s own.'
    head = read_head(document(head_tags(RESULTS._replace(name="A & B", description=said))))
    assert head.meta("description") == head.meta("og:description") == [said]
    assert head.titles == ("A & B · The Squares Project",)
    assert head.meta("og:title") == ["A & B"]


def test_an_article_states_its_dates_and_a_page_of_the_site_does_not() -> None:
    paper = RESULTS._replace(kind="article", published="2026-09-05", modified="2026-09-28")
    head = read_head(document(head_tags(paper)))
    assert head.meta("og:type") == ["article"]
    assert head.meta("article:published_time") == ["2026-09-05"]
    assert head.meta("article:modified_time") == ["2026-09-28"]
    assert head_problems(document(head_tags(paper)), SITE_URL + paper.path) == []
    assert "article:" not in head_tags(RESULTS)
    with pytest.raises(SystemExit, match="only an article"):
        head_tags(RESULTS._replace(published="2026-09-05"))
    with pytest.raises(SystemExit, match="not an ISO date"):
        head_tags(paper._replace(modified="September 28, 2026"))


@pytest.mark.parametrize(
    "description",
    ["", "   ", "x" * (DESCRIPTION_LIMIT + 1), "One line.\nAnd another."],
    ids=["empty", "blank", "too long", "two lines"],
)
def test_a_description_that_would_break_a_preview_is_refused(description: str) -> None:
    with pytest.raises(SystemExit, match="a description is one line"):
        head_tags(RESULTS._replace(description=description))
    head_tags(RESULTS._replace(description="x" * DESCRIPTION_LIMIT))


def test_every_page_of_the_site_carries_the_set_once_at_its_own_address(
    pages: dict[str, str],
) -> None:
    """Each page the renderer builds passes the deployed site's own check: one of each
    tag, the canonical link and `og:url` the address it is served at, the title ending in
    the project's formal name, the site's name the formal name, and the site's one card."""
    assert set(pages) == set(render_overview.PAGES)
    for name, page in pages.items():
        assert head_problems(page, canonical_url(name)) == [], name
        head = read_head(page)
        assert head.lang == "en", name
        (title,) = head.titles
        (shown,) = head.meta("og:title")
        assert title == page_title(shown), name
        assert "Square Packing Project" not in title, name
        # kpress's own four tags are gone, not added to.
        assert len(head.meta("og:type")) == len(head.meta("twitter:card")) == 1, name
    assert read_head(pages["index.html"]).titles == (PROJECT_NAME,)
    assert read_head(pages["tutorial.html"]).meta("og:type") == ["article"]
    kinds = {name: read_head(page).meta("og:type") for name, page in pages.items()}
    assert [name for name, kind in kinds.items() if kind != ["website"]] == ["tutorial.html"]


def test_every_page_has_a_description_of_its_own(pages: dict[str, str]) -> None:
    """No two pages say the same thing of themselves, the workbench and the two papers
    among them, and none is the site-wide sentence under another page's name."""
    from devtools import render_n11_optimality_review as paper  # noqa: PLC0415
    from workbench_tools import build_site  # noqa: PLC0415

    assert shared_descriptions(pages) == []
    described = {name: read_head(page).meta("description")[0] for name, page in pages.items()}
    described["workbench/index.html"] = build_site.PAGE.description
    described[paper.SITE_PATH] = paper.DESCRIPTION
    assert len(set(described.values())) == len(described)
    for name, description in described.items():
        assert 20 <= len(description) <= DESCRIPTION_LIMIT, (name, len(description))
        assert description.endswith("."), name
    assert described["index.html"] == render_overview.OVERVIEW_DESCRIPTION
    assert described["frontier.html"] == render_overview.FRONTIER_DESCRIPTION
    assert described[render_overview.RESULTS_PAGE] == render_overview.RESULTS_DESCRIPTION
    assert described["papers.html"] == render_overview.PAPERS_DESCRIPTION
    assert described["visualize.html"] == render_overview.VISUALIZE_DESCRIPTION


def test_a_document_cards_note_is_its_pages_description(pages: dict[str, str]) -> None:
    """A reader document's card on the overview and its page's preview say one thing."""
    notes = [note for _, _, note in overview_sections.DOCUMENTS]
    described = [
        read_head(pages[name]).meta("description")[0] for name in render_overview.DOCUMENT_PAGES
    ]
    assert described == notes


def broken(change: tuple[str, str]) -> str:
    """The results page's head with one string replaced."""
    old, new = change
    tags = head_tags(RESULTS)
    assert old in tags, old
    return document(tags.replace(old, new, 1))


OG_TITLE = '<meta property="og:title" content="Every Result">'


@pytest.mark.parametrize(
    ("change", "finding"),
    [
        ((OG_TITLE, OG_TITLE * 2), "2 og:title tags"),
        ((OG_TITLE, ""), "0 og:title tags"),
        (
            ('content="Every Result">', 'content="Every Result · Square Packing">'),
            "og:title is",
        ),
        (("<title>Every Result · The", "<title>Every Result · A"), "does not end in"),
        (
            ("<title>Every Result · The Squares Project", "<title>Squares"),
            "does not end",
        ),
        (
            (
                'og:site_name" content="The Squares Project',
                'og:site_name" content="Squares',
            ),
            "og:site_name is 'Squares'",
        ),
        (
            (
                'og:url" content="https://jlevy.github.io/squares/all-results.html',
                'og:url" content="https://jlevy.github.io/squares/results.html',
            ),
            "og:url is",
        ),
        (
            (
                'rel="canonical" href="https://jlevy.github.io/squares/',
                'rel="canonical" href="',
            ),
            "the canonical link is 'all-results.html'",
        ),
        (
            ('og:image" content="https://jlevy.github.io/squares/', 'og:image" content="'),
            "og:image is 'social-card.png'",
        ),
        (('og:image:width" content="1200', 'og:image:width" content="2400'), "og:image:width"),
        (
            ('twitter:card" content="summary_large_image', 'twitter:card" content="summary'),
            "twitter:card is 'summary'",
        ),
        (
            (
                '<meta name="description" content="Every',
                '<meta name="description" content="Each',
            ),
            "og:description is",
        ),
        (('og:type" content="website', 'og:type" content="page'), "og:type is 'page'"),
        (('og:locale" content="en_US', 'og:locale" content="en'), "og:locale is 'en'"),
        (("</title>", "</title><title>Another</title>"), "2 <title>"),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_a_head_that_would_show_a_worse_preview_is_named(
    change: tuple[str, str], finding: str
) -> None:
    """Each way the heads were wrong before, and each way one could drift, is a finding:
    a tag twice or missing, the site's name after the preview's title, the old names, an
    address that is not the page's or not in full, a size the card is not."""
    problems = head_problems(broken(change), SITE_URL + RESULTS.path)
    assert any(finding in problem for problem in problems), problems


def test_a_head_is_read_by_a_parser_and_only_to_its_end() -> None:
    """A tag spelt in a stylesheet's comment or in the body is not the head's."""
    page = (
        '<!doctype html><html lang="en"><head>'
        "<style>/* <title>Not this</title> <meta name=description content=no> */"
        f"</style>{head_tags(RESULTS)}</head><body>"
        "<svg><title>A figure</title></svg>"
        '<meta property="og:title" content="Body"></body></html>'
    )
    head = read_head(page)
    assert head.titles == ("Every Result · The Squares Project",)
    assert head.meta("og:title") == ["Every Result"]
    assert head_problems(page, SITE_URL + RESULTS.path) == []
    assert read_head(
        "<div class='site-result'>A fragment</div>"
    ) == check_published_site.PageHead(None, (), (), ())


def test_a_long_or_missing_description_is_a_finding() -> None:
    long = "x" * (DESCRIPTION_LIMIT + 1)
    tags = head_tags(RESULTS).replace(RESULTS.description, long)
    assert any("over 160" in p for p in head_problems(document(tags), SITE_URL + RESULTS.path))
    tags = head_tags(RESULTS).replace(f'content="{RESULTS.description}"', 'content=""')
    assert any("empty" in p for p in head_problems(document(tags), SITE_URL + RESULTS.path))


def test_two_pages_with_one_description_are_named() -> None:
    first = document(head_tags(RESULTS))
    second = document(head_tags(RESULTS._replace(name="Papers", path="papers.html")))
    third = document(head_tags(RESULTS._replace(description="Another sentence.")))
    (shared,) = shared_descriptions({"a.html": first, "b.html": second, "c.html": third})
    assert shared.startswith("a.html, b.html: ")
    assert shared_descriptions({"a.html": first, "c.html": third}) == []


def test_a_forwarder_names_where_it_sends_a_reader_in_full_and_carries_no_card() -> None:
    """A forwarder is no page to share: a canonical link to its target, in full, and no
    card. Every forwarder is the renderer's, the papers' old addresses among them: the
    optimality paper's page, the directory it was served from, and the explainer's."""
    from devtools import render_n11_lower_bounds_explainer as explainer  # noqa: PLC0415
    from devtools import render_n11_optimality_review as paper  # noqa: PLC0415

    named = check_published_site.forwarder_canonicals()
    forwarders = {page.name: page.html for page in render_overview.forwarder_pages()}
    assert set(named) == set(forwarders)
    for name, page in forwarders.items():
        assert forwarder_problems(page, named[name]) == [], name
        assert named[name].startswith("https://"), name
    landing = forwarders["n11-optimality/index.html"]
    target = canonical_url(paper.SITE_PATH)
    assert target == SITE_URL + "papers/n11-optimality-review.html"
    assert named["n11-optimality/index.html"] == target
    assert named["n11-optimality/t-060-explainer.html"] == target
    assert named["explainer.html"] == canonical_url(explainer.SITE_PATH) == explainer.PAGE_URL
    assert explainer.PAGE_URL == SITE_URL + "papers/n11-lower-bounds-explainer.html"
    assert forwarder_problems(landing, target) == []
    # The landing address named the paper by its file name alone until 2026-10-01.
    relative = landing.replace(
        f'href="{target}"', 'href="../papers/n11-optimality-review.html"'
    )
    assert forwarder_problems(relative, target)
    assert any("not an address in full" in p for p in forwarder_problems(relative, "a.html"))
    carded = landing.replace("<title>", f"{OG_TITLE}<title>", 1)
    assert any("card tags" in problem for problem in forwarder_problems(carded, target))


def test_a_results_overview_is_a_fragment_with_no_head() -> None:
    """A result's overview is fetched into a popover and is no document: it has no head,
    so it carries no card and no broken one."""
    fragment = render_overview.result_fragments()[0]
    assert fragment.html.startswith('<div class="site-result"')
    assert read_head(fragment.html) == check_published_site.PageHead(None, (), (), ())
    assert "<meta" not in fragment.html
    assert "<title" not in fragment.html


def test_the_card_is_the_heros_drawing_on_the_pages_background() -> None:
    """The card is the homepage's hero and no second drawing: the same case at the same
    resolution through the same function, so its squares, colours and line weights are
    the page's, in the light theme's ink on its background, with the project's name."""
    hero = overview_sections.hero()
    case = overview_sections.HERO_CASE
    assert case == 53
    assert f"The best packing known for {case} squares" in hero
    assert packing_svg(case, units=social_card.HERO_UNITS) in hero
    light = rung_scale.page_colours()["light"]
    ink, paper = rung_scale.hex_colour(light["text"]), rung_scale.hex_colour(light["bg"])
    assert social_card.page_colours() == (ink, paper) == ("#111827", "#ffffff")
    drawing = packing_svg(case, units=social_card.HERO_UNITS, ink=ink)
    svg = social_card.card_svg()
    body = drawing.split(">", 1)[1]
    assert svg.count(body) == 1, "the hero's drawing, in the page's ink, is in the card whole"
    assert svg.startswith(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" '
        'viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#ffffff"/>'
    )
    # The packing and the name sit inside the square at the card's centre, which is what
    # a consumer that shows a square thumbnail keeps.
    placed = re.search(r'<svg x="([\d.]+)" y="([\d.]+)" width="(\d+)" height="(\d+)"', svg)
    assert placed is not None
    x, y, width, height = (float(part) for part in placed.groups())
    assert width == height == social_card.PACKING_SIDE
    assert x == (SOCIAL_CARD_WIDTH - width) / 2
    margin = (SOCIAL_CARD_WIDTH - SOCIAL_CARD_HEIGHT) / 2
    outline, name_width, cap_height = social_card.name_outline(
        PROJECT_NAME.upper(), social_card.NAME_SIZE
    )
    assert outline in svg
    assert margin < (SOCIAL_CARD_WIDTH - name_width) / 2
    foot = y + height + social_card.NAME_GAP + cap_height
    assert y == pytest.approx(SOCIAL_CARD_HEIGHT - foot, abs=0.01), "equal margins"
    assert y >= 40
    # Without the name the drawing is the whole card, larger and centred.
    plain = social_card.card_svg(named=False)
    assert outline not in plain
    assert plain.count(body) == 1
    assert f'width="{social_card.PLAIN_PACKING_SIDE}"' in plain


def test_the_cards_name_is_set_as_the_bar_sets_the_sites() -> None:
    """The name under the packing is the bar's: the bar's sans at its weight and letter
    spacing, in capitals. The values are the bar's rule's, read from the stylesheet."""
    css = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    rule = re.search(r"\.site-nav \.site-name \{([^}]*font-weight[^}]*)\}", css)
    assert rule is not None
    assert f"font-weight: {social_card.NAME_WEIGHT};" in rule.group(1)
    assert f"letter-spacing: {social_card.NAME_TRACKING}em;" in rule.group(1)
    assert "text-transform: uppercase;" in rule.group(1)
    face = render_overview.nav_shell("visualize", root="../").head
    assert '"Source Sans 3 Variable"' in face
    assert social_card.SANS_FACE.startswith("source-sans-3-")
    # Outlines, not text: a rasteriser would set text in a face the machine happens to have.
    svg = social_card.card_svg()
    assert "<text" not in svg
    assert "font-family" not in svg
    outline, width, cap_height = social_card.name_outline("THE", 34)
    assert outline.startswith("M")
    assert 40 < width < 80
    assert 20 < cap_height < 26


def test_the_card_is_a_png_of_the_declared_size_under_the_ceiling(card: bytes) -> None:
    """The bytes are what every head declares: a PNG, 1200 by 630, and light enough that
    no consumer refuses it. Two drawings agree, which is what the Pages job compares."""
    assert social_card.png_dimensions(card) == (SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT)
    assert (SOCIAL_CARD_WIDTH, SOCIAL_CARD_HEIGHT) == (1200, 630)
    assert social_card.card_problems(card) == []
    assert 10_000 < len(card) <= social_card.BYTE_CEILING == 300_000
    assert social_card.card_png() == card
    assert social_card.card_png(named=False) != card


def test_bytes_that_are_not_the_card_are_named(card: bytes) -> None:
    import cairosvg  # noqa: PLC0415

    assert social_card.card_problems(b"<html>404</html>") == ["it is not a PNG"]
    assert social_card.png_dimensions(b"") is None
    wide = cairosvg.svg2png(
        bytestring=social_card.card_svg().encode(), output_width=2400, output_height=1260
    )
    assert isinstance(wide, bytes)
    (problem,) = social_card.card_problems(wide)
    assert problem == "it is 2400x1260, and every page declares 1200x630"
    heavy = card + b"\0" * social_card.BYTE_CEILING
    assert social_card.card_problems(heavy) == [
        f"it is {len(heavy)} bytes, over the 300000-byte ceiling"
    ]


def test_the_tool_writes_the_card_under_its_served_name_and_checks_it(
    tmp_path: Path, card: bytes, capsys: pytest.CaptureFixture[str]
) -> None:
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 1
    assert "stale or missing" in capsys.readouterr().err
    assert social_card.main(["--output-dir", str(tmp_path)]) == 0
    assert sorted(path.name for path in tmp_path.iterdir()) == [SOCIAL_CARD]
    assert (tmp_path / SOCIAL_CARD).read_bytes() == card
    assert "1200x630" in capsys.readouterr().out
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 0
    (tmp_path / SOCIAL_CARD).write_bytes(social_card.card_png(named=False))
    assert social_card.main(["--output-dir", str(tmp_path), "--check"]) == 1
    assert social_card.main(["--output-dir", str(tmp_path), "--plain", "--check"]) == 0


def test_a_built_site_is_held_to_its_heads_and_its_card(
    tmp_path: Path, pages: dict[str, str], card: bytes
) -> None:
    """The local mode reads a directory as the deploy check reads the site: every page
    there, every forwarder there and the card, with what a build left out reported and
    not failed, and a card that is missing or the wrong picture failed."""
    # A build with none of the site's pages names no card, so it misses none.
    assert all(passed for passed, _ in local_head_checks(tmp_path))
    for name in ("index.html", "papers.html"):
        (tmp_path / name).write_text(pages[name], encoding="utf-8")
    for forwarder in render_overview.forwarder_pages():
        # A forwarder stands where its page was, which for a paper was a directory down.
        (tmp_path / forwarder.name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / forwarder.name).write_text(forwarder.html, encoding="utf-8")
    results = local_head_checks(tmp_path)
    assert [line for passed, line in results if not passed] == [
        f"card {SOCIAL_CARD}: not served"
    ]
    (tmp_path / SOCIAL_CARD).write_bytes(card)
    results = local_head_checks(tmp_path)
    assert all(passed for passed, _ in results), results
    lines = [line for _, line in results]
    assert "index.html: one of each identity and card tag, agreeing with its address" in lines
    assert "each of 2 pages has a description of its own" in lines
    assert f"card {SOCIAL_CARD}: a PNG of 1200x630, {len(card)} bytes" in lines
    assert "papers/n11-lower-bounds-explainer.html: not in this build, so not checked" in lines
    assert "papers/n11-optimality-review.html: not in this build, so not checked" in lines
    assert "workbench/index.html: not in this build, so not checked" in lines
    assert check_published_site.main(["--local", str(tmp_path)]) == 0
    # A page under another's head, and a card that is not the card.
    (tmp_path / "papers.html").write_text(pages["index.html"], encoding="utf-8")
    (tmp_path / SOCIAL_CARD).write_bytes(b"not a picture")
    failed = [line for passed, line in local_head_checks(tmp_path) if not passed]
    assert len(failed) == 3
    assert failed[0].startswith("papers.html: head: the canonical link is")
    assert failed[1].startswith("descriptions shared between pages: index.html, papers.html")
    assert failed[2] == f"card {SOCIAL_CARD}: it is not a PNG"
    assert check_published_site.main(["--local", str(tmp_path)]) == 1


def test_head_checks_report_one_line_a_page_a_forwarder_and_the_card(card: bytes) -> None:
    page = document(head_tags(RESULTS))
    target = SITE_URL + "all-results.html"
    forwarder = f'<html lang="en"><head><link rel="canonical" href="{target}"></head></html>'
    results = head_checks(
        {"all-results.html": page}, {"results.html": (forwarder, target)}, card
    )
    assert [passed for passed, _ in results] == [True, True, True, True]
    results = head_checks({"papers.html": page}, {"results.html": (forwarder, "x")}, None)
    assert [passed for passed, _ in results] == [False, True, False, False]
