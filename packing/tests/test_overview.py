"""The overview page: every register entry shown, every count read from the record."""

from __future__ import annotations

import html
import re
from collections import Counter

import pytest

from devtools import overview_data, overview_sections, render_overview
from devtools.render_explainer import MARKDOWN as EXPLAINER_ARTICLE
from devtools.render_explainer import TEMPLATE as EXPLAINER_SHELL
from sqpack.yamlio import safe_load

ID = re.compile(r'\sid="([^"]+)"')
ROW = re.compile(r'<tr id="(t-\d{3})" data-source="(ours|others)" data-c="(C\d)">')


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


def test_the_atlas_film_plays_quietly_by_itself(page: str) -> None:
    """Muted, looping and inline, which is what lets a browser autoplay it; the script
    that holds it still for reduced motion is on the page."""
    (video,) = re.findall(r"<video\b[^>]*>", page)
    for attribute in ("autoplay", "muted", "loop", "playsinline", "controls"):
        assert re.search(rf"\s{attribute}\b", video), attribute
    assert (
        "ascent-n1-324-1080p60-citations.mp4"
        in page.split(video, 1)[1].split("</video>", maxsplit=1)[0]
    )
    assert render_overview.FILM_SCRIPT.read_text(encoding="utf-8") in page


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


def test_every_record_link_is_a_permalink_or_a_site_page() -> None:
    for result in overview_data.load().results:
        for link in result.records:
            assert (
                link.url.startswith(render_overview.REPO_URL + "/blob/")
                or link.url == "frontier.html"
            ), (result.id, link)
            assert "/blob/main/" not in link.url, (result.id, link)


def test_every_repository_link_on_the_page_names_the_build_commit(page: str) -> None:
    """The deployed-site check requires one ref across the page, the commit it was built
    at, besides the "On GitHub" links, which name the default branch.

    The template's prose linked `epistemics.md` at `blob/main/`, which that check would
    have failed on the first deploy; this asks the same question of the render here.
    """
    from devtools.check_published_site import branch_links, repository_links  # noqa: PLC0415
    from devtools.render_explainer import link_revision  # noqa: PLC0415

    links = repository_links(page) - branch_links(page)
    assert links
    assert {ref for _, ref, _ in links} == {link_revision()}


def test_on_github_links_open_the_latest_version() -> None:
    """Each "On GitHub" link names the default branch, and only those do."""
    page = render_overview.overview_page().html
    branch = f"{render_overview.REPO_URL}/blob/{render_overview.DEFAULT_BRANCH}/"
    also = re.findall(r'<a class="site-popover-also" href="([^"]+)"[^>]*>On GitHub</a>', page)
    assert len(also) == len(overview_sections.DOCUMENTS) + len(overview_sections.DIMENSIONS)
    assert all(url.startswith(branch) for url in also)
    assert page.count(branch) == len(also)

    from devtools.check_published_site import branch_links  # noqa: PLC0415

    assert {ref for _, ref, _ in branch_links(page)} == {render_overview.DEFAULT_BRANCH}
    assert len(branch_links(page)) == len(set(also))


def test_other_projects_are_the_source_repositories_the_record_reviews() -> None:
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
    assert sorted(listed) == sorted(reviewed)
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
