"""The overview page: its sections, cards, table, chips and media, and the scripts behind them.

Most tests render the page from fixture instances of the three contracts it reads
(`overview_data`, `overview_media`, `reader_documents`), so they hold the page's own
structure whatever the record says today. The completeness tests render it from the record
itself: every recent result is a card and every register entry a row. The page's ids are
held disjoint from the explainer's, since the fragment forwarder sends any fragment the
overview lacks to the explainer. The scripts' behaviour is tested in Node against a small
document (`tests/node/overview_page/`), one test here per script.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from functools import cache
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools import (
    overview_data,
    overview_media,
    overview_page,
    reader_documents,
    render_explainer,
    render_overview,
)
from devtools.overview_data import (
    AtlasTotals,
    Bound,
    ExplainerEdition,
    Link,
    NotableSource,
    OverviewData,
    Result,
    ResultGroup,
    RungCount,
    SourceRelease,
)
from devtools.overview_media import Film, Preview
from devtools.overview_page import SECTIONS, Media, render
from devtools.reader_documents import ReaderDocument

REPO = Path(__file__).resolve().parents[2]
NODE_TESTS = Path(__file__).resolve().parent / "node" / "overview_page"
COMMIT = "0" * 40
PERMALINK = f"https://github.com/jlevy/squares/blob/{COMMIT}"

# ── Fixtures ─────────────────────────────────────────────────────────────────────────


def bound(n: int, relation: str, exact: str, decimal: str, tex: str) -> Bound:
    value = Fraction(exact) if re.fullmatch(r"\d+(/\d+)?", exact) else None
    return Bound(n, relation, exact, decimal, tex, value)


def result(identifier: str, **changes: object) -> Result:
    """A register entry by this project, holding its case, with `changes` applied."""
    base = Result(
        id=identifier,
        n_values=(11,),
        cases="11",
        headline="`s(11) ≥ 381/100 = 3.81`",
        claim="s(11) >= 381/100 = 3.81, by a point certificate.",
        bound=bound(11, "≥", "381/100", "3.81", r"s(11) \ge \frac{381}{100}"),
        verification="V4",
        confirmation="C5",
        significance=5,
        novelty="apparently-novel",
        ours=True,
        credit="Squares Project (Levy)",
        ai_assistance=None,
        lineage="this-project",
        relation=None,
        standing="holds",
        superseded_by=None,
        reported=False,
        exact_value=False,
        recent=True,
        established="2026-09-04",
        published=None,
        registered="2026-09-05",
        next_rung="V5 by a proof-assistant port.",
        composition=None,
        records=(
            Link("n-011.md", f"{PERMALINK}/packing/frontier/n-011.md", "case"),
            Link("results.yaml", f"{PERMALINK}/packing/frontier/results.yaml#L1", "register"),
            Link("E-one", f"{PERMALINK}/packing/frontier/evidence.yaml#L2", "evidence"),
            Link("E-two", f"{PERMALINK}/packing/frontier/evidence.yaml#L9", "evidence"),
        ),
        artifacts=(),
    )
    return replace(base, **changes)  # pyright: ignore[reportArgumentType]


OURS_HOLDS = result("T-018")
OURS_SUPERSEDED = result(
    "T-026",
    headline="`s(11) ≥ 955000√(518400042893309449)/179696714646249 = 3.8264474…`",
    bound=bound(
        11,
        "≥",
        "955000*sqrt(518400042893309449)/179696714646249",
        "3.8264474…",
        r"s(11) \ge \frac{955000\sqrt{518400042893309449}}{179696714646249}",
    ),
    standing="superseded",
    superseded_by="T-037, Kleddamag",
    established="2026-09-09",
)
OURS_NOT_A_BOUND = result(
    "T-014",
    n_values=(5,),
    cases="5",
    headline="Goebel's `n = 5` optimum is rigid at fixed side",
    bound=None,
    standing="—",
    significance=3,
    confirmation="C3",
    verification="V3",
    recent=False,
    composition="The rigidity is exact.",
)
OTHERS_EXACT = result(
    "T-052",
    n_values=(21,),
    cases="21",
    headline="`s(21) = 5`, by a mixed cover of points and grid-line segments",
    bound=bound(21, "=", "5", "5", "s(21) = 5"),
    ours=False,
    credit="Daniel after Burns, Massaccesi",
    ai_assistance="The source's `CREDITS.md` says the work was produced with Claude.",
    lineage="independent",
    relation="independent",
    exact_value=True,
    confirmation="C3",
    significance=4,
    novelty="previously-published",
    established=None,
    published="2026-09-27",
    registered="2026-09-28",
)
OTHERS_REPORTED = result(
    "T-046",
    n_values=tuple(range(18, 96)),
    cases="48 in 18\u201395",
    headline="Rectangle-density lower bounds reported for 48 counts in `n = 18…95`",
    bound=None,
    ours=False,
    credit="wand125 after Tokoharu, Levy",
    lineage="builds-on-project",
    relation="builds on",
    standing="holds, reported",
    reported=True,
    verification="V0",
    confirmation="C0",
    significance=3,
    novelty="previously-published",
    established=None,
    published="2026-09-27",
    registered="2026-09-27",
)
OTHERS_BEFORE = result(
    "T-011",
    headline="Trump's 1979 packing is exactly valid",
    bound=None,
    ours=False,
    credit="Trump",
    lineage="independent",
    relation=None,
    recent=False,
    established=None,
    published="1979",
    registered="2026-08-31",
    novelty="previously-published",
)


def edition() -> ExplainerEdition:
    return ExplainerEdition(
        lead_result="T-026",
        lead_bound=bound(11, "≥", "3.8264474", "3.8264474…", r"s(11) \ge 3.8264474\ldots"),
        current_bound=bound(11, ">", "31/8", "3.875", r"s(11) \gt \frac{31}{8}"),
        current_credit="Kleddamag",
        current_results=("T-037",),
        is_current=False,
        first_published="2026-09-05",
        edition="v0.4.0",
        edition_first_published="2026-09-13",
    )


def data() -> OverviewData:
    counts = tuple(
        RungCount(axis, rung, f"{axis}{rung} words", f"{axis}{rung} support", rung, 1)  # pyright: ignore[reportArgumentType]
        for axis, rungs in (("V", range(6)), ("C", range(6)), ("S", range(1, 6)))
        for rung in rungs
    )
    return OverviewData(
        edition="v0.4.2-test",
        data_revision="0" * 64,
        recent_ours=(OURS_HOLDS, OURS_SUPERSEDED),
        recent_others=(OTHERS_EXACT, OTHERS_REPORTED),
        groups=(
            ResultGroup("ours", "This project's results", (OURS_HOLDS, OURS_SUPERSEDED)),
            ResultGroup("independent", "Independent", (OTHERS_EXACT, OTHERS_REPORTED)),
            ResultGroup(
                "before-project", "Published before", (OURS_NOT_A_BOUND, OTHERS_BEFORE)
            ),
        ),
        rung_counts=counts,
        atlas=AtlasTotals(cases=100, proved=38, open=62, recent_verified_lower=27),
        sources=(
            NotableSource(
                id="friedman",
                title="Packing Unit Squares in Squares",
                kind="website",
                url="https://erich-friedman.github.io/packing/squinsqu/",
                credit="Friedman",
                summary="Erich Friedman's page on packing unit squares in squares.",
                archive=Link("retained", f"{PERMALINK}/packing/resources/web/x/", "archive"),
                releases=(),
                cases=(),
            ),
            NotableSource(
                id="kleddamag-11",
                title="11-squares-certified-bound",
                kind="repository",
                url="https://github.com/Kleddamag/11-squares-certified-bound",
                credit="Kleddamag after Levy",
                summary="Kleddamag's certified lower bound for eleven squares.",
                archive=None,
                releases=(
                    SourceRelease(
                        "v1.0.2", "https://example.org/v1.0.2", "2026-09-22", superseded=False
                    ),
                    SourceRelease(
                        "v1.0.1", "https://example.org/v1.0.1", "2026-09-21", superseded=True
                    ),
                ),
                cases=(Link("n-011.md", f"{PERMALINK}/packing/frontier/n-011.md", "case"),),
            ),
        ),
        explainer=edition(),
    )


def media() -> Media:
    previews = tuple(
        Preview(
            image=f"known-best-1-{n}-preview.png",
            width=560,
            height=640,
            alt=f"The atlas of one through {n}",
            pdf=f"known-best-1-{n}.pdf",
            size="87 KB",
            pages="25 by 30 in",
            edition="v0.4.2-test",
        )
        for n in (100, 324)
    )
    film = Film(
        src="films/ascent-n1-324-1080p60-citations.mp4",
        type='video/mp4; codecs="avc1.640028"',
        poster="ascent-n1-324-poster.png",
        width=1920,
        height=1080,
        size="216 MB",
        duration="8m 14s",
        edition="v0.4.2-film",
        release="https://github.com/jlevy/squares/releases/tag/v0.4.2",
    )
    hero = '<svg viewBox="0 0 2 2"><path d="M0 0H1V1H0Z"/></svg>'
    return Media(previews=previews, film=film, hero=hero)


def documents() -> tuple[ReaderDocument, ...]:
    research = min((REPO / "docs" / "project" / "research").glob("research-*.md"))
    rows = (
        ("README.md", "README", "start", None, False),
        ("TUTORIAL.md", "Tutorial", "start", None, False),
        ("epistemics.md", "Epistemics", "results", None, False),
        (
            research.relative_to(REPO).as_posix(),
            "A research report",
            "reports",
            "2026-08-22",
            True,
        ),
    )
    return tuple(
        ReaderDocument(
            path=path,
            title=title,
            summary=f"What {title} covers.",
            group=group,  # pyright: ignore[reportArgumentType]
            url="tutorial.html"
            if path == "TUTORIAL.md"
            else f"https://github.com/jlevy/squares/blob/main/{path}",
            date=date,
            dated=dated,
        )
        for path, title, group, date, dated in rows
    )


@pytest.fixture(scope="module")
def body() -> str:
    return render(data(), media(), documents())


@cache
def real_body() -> str:
    """The page from the record, or a skip naming the contract that is not built yet."""
    try:
        return render(
            overview_data.load(), overview_page.media(), reader_documents.reader_documents()
        )
    except NotImplementedError as missing:  # pragma: no cover - the lanes land together
        pytest.skip(f"a contract the page reads is not implemented yet: {missing!r}")


def section_ids(html: str) -> list[str]:
    return re.findall(r'<h2 id="([^"]+)">', html)


def ids_of(html: str) -> set[str]:
    return set(re.findall(r'\sid="([^"]+)"', html))


def element(html: str, pattern: str) -> str:
    match = re.search(pattern, html, re.DOTALL)
    assert match is not None, pattern
    return match.group(0)


def card_of(html: str, identifier: str) -> str:
    """The result card for one register entry."""
    return element(
        html,
        r'<article class="site-card site-card-result"[^>]*>(?:(?!</article>).)*'
        rf"{identifier}.*?</article>",
    )


# ── The page ─────────────────────────────────────────────────────────────────────────


def test_the_page_opens_with_its_sections_in_order_and_no_h1(body: str) -> None:
    assert section_ids(body) == [anchor for anchor, _ in SECTIONS]
    assert "<h1" not in body
    assert body.index('class="site-hero"') < body.index('<h2 id="problem">')


def test_the_page_renders_into_the_site_shell() -> None:
    page = overview_page.Page(
        key="overview",
        path="index.html",
        title="Square Packing",
        description=overview_page.DESCRIPTION,
        html=render(data(), media(), documents()),
        scripts=overview_page.SCRIPTS,
    )
    html = render_overview.page_html(page, commit=COMMIT)
    assert "<h1" not in html
    assert '<a href="./" aria-current="page">Overview</a>' in html
    assert html.count('<nav class="site-nav"') == 1


def test_every_recent_result_is_a_card_that_opens_its_row(body: str) -> None:
    recent = [*data().recent_ours, *data().recent_others]
    cards = re.findall(
        r'<a class="site-card-link" href="#(result-t-\d+)" [^>]*data-popover="result"', body
    )
    assert cards == [overview_page.result_anchor(r) for r in recent]
    for anchor in cards:
        assert f'<tr id="{anchor}" ' in body


def test_every_register_entry_is_a_table_row_in_the_registers_order(body: str) -> None:
    rows = re.findall(r'<tr id="(result-t-\d+)"', body)
    expected = [
        overview_page.result_anchor(r) for group in data().groups for r in group.results
    ]
    assert rows == expected
    groups = re.findall(r'<tbody data-group="([^"]+)">', body)
    assert groups == [group.key for group in data().groups]


def test_a_reported_result_is_labelled_reported_and_never_verified(body: str) -> None:
    card = card_of(body, "T-046")
    assert "reported" in card
    assert "verified" not in card.lower().replace("unverified", "")
    row = element(body, r'<tr id="result-t-046".*?</tr>')
    assert 'data-flags="others recent reported holds"' in row


def test_new_exact_values_are_marked_apart_from_bounds(body: str) -> None:
    card = card_of(body, "T-052")
    assert 'title="A new exact value, not only a bound">exact value</span>' in card
    bound_card = card_of(body, "T-018")
    assert "exact value" not in bound_card


def test_a_superseded_card_names_the_current_holder(body: str) -> None:
    card = card_of(body, "T-026")
    assert "Now held by T-037, Kleddamag." in card
    assert 'data-tone="muted">superseded</span>' in card
    # A forty-digit radical is shown on the card by its decimal and set whole in the row.
    assert r"\(s\mkern1mu(11) \ge 3.8264474\ldots\)" in card
    assert "Exact form." in element(body, r'<tr id="result-t-026".*?</tr>')


def test_credit_is_printed_whole_with_the_sources_statement_of_ai_assistance(body: str) -> None:
    card = card_of(body, "T-052")
    assert "Daniel after Burns, Massaccesi" in card
    assert (
        "AI assistance, in the source\u2019s words: The source&#x27;s <code>CREDITS.md</code>"
        in card
    )


def test_chips_are_one_component_with_rung_badges_by_axis_and_rung(body: str) -> None:
    chips = re.findall(r'<span class="(site-chip[^"]*)"([^>]*)>', body)
    assert chips
    assert all(classes.split()[0] == "site-chip" for classes, _ in chips)
    rungs = {
        (axis, int(rung))
        for axis, rung in re.findall(
            r'class="site-chip site-rung" data-axis="([vcs])" data-rung="(\d)"', body
        )
    }
    assert {axis for axis, _ in rungs} == {"v", "c", "s"}
    assert ("v", 0) in rungs
    assert ("c", 5) in rungs
    assert 'class="site-chip site-chip-star"' in body
    assert "data-wrap>previously published</span>" in body
    # Every rung badge carries the record's words for its rung.
    assert 'data-axis="v" data-rung="4" title="V4: V4 words"' in body


def test_every_card_is_a_link_and_only_one(body: str) -> None:
    cards = re.findall(r'<(article|figure) class="site-card[ "].*?</\1>', body, re.DOTALL)
    assert len(cards) >= 15
    for match in re.finditer(
        r'<(article|figure) class="site-card[ "].*?</\1>', body, re.DOTALL
    ):
        assert match.group(0).count('class="site-card-link"') == 1, match.group(0)[:200]
    goes = set(re.findall(r'data-goes="([a-z]+)"', body))
    assert goes == {"down", "page", "out"}


def test_the_verification_cards_count_each_rung_this_projects_and_others(body: str) -> None:
    for axis in "vcs":
        card = element(
            body, rf'<article class="site-card site-card-axis" data-axis="{axis}">.*?</article>'
        )
        counts = re.findall(r'<td data-count="(\d+)">', card)
        rungs = [c for c in data().rung_counts if c.axis.lower() == axis]
        assert len(counts) == 2 * len(rungs)
    atlas = element(body, r'<article class="site-card site-card-atlas">.*?</article>')
    for figure in ("38</span> proved", "62</span> open", "27</span> with a recent verified"):
        assert figure in atlas


def test_the_film_is_one_player_that_never_autoplays(body: str) -> None:
    videos = re.findall(r"<video\b[^>]*>", body)
    assert len(videos) == 1
    video = videos[0]
    assert "autoplay" not in video
    assert 'preload="none"' in video
    assert " controls " in video
    assert 'poster="ascent-n1-324-poster.png"' in video
    assert '<source src="films/ascent-n1-324-1080p60-citations.mp4"' in body
    assert '<a href="films/ascent-n1-324-1080p60-citations.mp4">Open the MP4</a>' in body
    assert "edition v0.4.2-film" in body


def test_the_media_are_site_relative_inside_the_marked_element(body: str) -> None:
    section = element(
        body,
        r'<div class="site-media site-wide" data-site-media>.*?'
        r'<figure class="site-film.*?</figure></div>',
    )
    references = re.findall(r'\s(?:href|src|poster)="([^"]+)"', section)
    media_refs = [
        ref
        for ref in references
        if not ref.startswith("https://github.com/jlevy/squares/releases/tag/")
    ]
    assert len(media_refs) == 7
    for reference in media_refs:
        assert "://" not in reference
        assert not reference.startswith("/")
    for preview in media().previews:
        assert f'href="{preview.pdf}"' in section
        assert f'src="{preview.image}"' in section


def test_the_explainer_card_carries_its_edition_note(body: str) -> None:
    card = element(
        body,
        r'<article class="site-card site-card-page">(?:(?!</article>).)*'
        r"explainer\.html.*?</article>",
    )
    assert "The v0.4.0 proof edition, first published 13 September 2026" in card
    assert "earlier edition" in card
    assert "This edition leads with T-026" in card


def test_document_cards_link_github_and_carry_their_opening_section(body: str) -> None:
    island = element(
        body, r'<script type="application/json" id="site-default-branch-links">(.*?)</script>'
    )
    listed = json.loads(re.sub(r"^<[^>]+>|</script>$", "", island))
    github = [d.url for d in documents() if d.url.startswith("https://")]
    assert listed == sorted(github)
    for document in documents():
        if document.url.startswith("https://"):
            card = element(
                body,
                r'<article class="site-card site-card-document"(?:(?!</article>).)*'
                rf"{re.escape(document.url)}.*?</article>",
            )
            assert 'data-popover="document"' in card
            assert '<template class="site-card-preview">' in card
    # The tutorial is a page card, not a second document card.
    assert body.count('href="tutorial.html"') == 1
    dated = element(
        body, r'<article class="site-card site-card-document" data-group="reports".*?</article>'
    )
    assert "dated record" in dated


def test_other_projects_list_websites_first_then_repositories_with_releases(body: str) -> None:
    section = body[body.index('<h2 id="other-projects">') :]
    assert section.index("Websites and catalogues") < section.index("Repositories and releases")
    assert "v1.0.1</a>, reviewed 2026-09-21" in section
    assert 'data-tone="muted" title="Covered by a later release">superseded' in section


def test_the_table_works_without_javascript(body: str) -> None:
    table = element(
        body,
        r'<table class="kpress-table site-table site-table-fixed" data-site-table '
        r'id="results-table">.*?</table>',
    )
    assert table.count("<details>") == sum(len(group.results) for group in data().groups)
    filters = element(
        body, r'<div class="site-table-filters[^"]*" data-filters-for="results-table"[^>]*>'
    )
    assert filters.endswith("hidden>")
    sortable = re.findall(r'<th scope="col" class="[^"]+" data-sort="(number|text)">', table)
    assert len(sortable) == 10


def test_the_page_names_no_bound_in_its_template() -> None:
    """Every number on the page is filled from the record; the template holds prose only."""
    source = overview_page.template_text(overview_page.TEMPLATE.read_text(encoding="utf-8"))
    prose = re.sub(r"\{\{[A-Z_]+\}\}", "", source)
    assert re.findall(r"\d", prose) == []
    assert re.findall(r"[≥≤<>=]\s*\$?\s*\d|\d+/\d+|\d+\.\d+", source) == []


def test_a_template_that_moves_a_section_or_a_block_is_refused() -> None:
    template = overview_page.TEMPLATE.read_text(encoding="utf-8")
    with pytest.raises(SystemExit, match="sections"):
        render(
            data(),
            media(),
            documents(),
            template=template.replace("## Read Further", "## Reading"),
        )
    with pytest.raises(SystemExit, match="stand alone"):
        render(
            data(), media(), documents(), template=template.replace("{{HERO}}", "The {{HERO}}")
        )
    with pytest.raises(SystemExit, match="no value"):
        render(data(), media(), documents(), template=template + "\n{{UNKNOWN}}\n")


def test_the_overview_and_the_explainer_share_no_id(body: str) -> None:
    """The forwarder sends a fragment the overview lacks to the explainer, so no id may be
    on both: an old deep link would stop on the overview. The icon sprite both pages
    inline names symbols, not places, and no link targets it."""
    explainer = ids_of(render_explainer.render(render_explainer.WALKTHROUGH).page)
    sprite = {i for i in explainer if i.startswith("kpress-icon-")}
    overview = ids_of(body) | ids_of(real_body())
    assert overview & (explainer - sprite) == set()
    assert {"recent-results", "results-table"} <= overview


def test_the_site_templates_own_no_inline_programs(body: str) -> None:
    """HTML is not a Biome, ESLint or tsc input: every script body is a placeholder for a
    file, and the page's own script elements are JSON data islands."""
    script = re.compile(r"<script(\s[^>]*)?>(.*?)</script>", re.DOTALL)
    for template in (
        render_overview.SHELL,
        overview_page.TEMPLATE,
        render_overview.site_kit.NAV_TEMPLATE,
    ):
        for _, text in script.findall(template.read_text(encoding="utf-8")):
            assert re.fullmatch(r"\s*\{\{[A-Z_]+\}\}\s*", text), template.name
    for attributes, _ in script.findall(body):
        assert 'type="application/json"' in attributes


def test_the_page_scripts_are_files_under_the_browser_floor() -> None:
    config = (REPO / "tsconfig.overview.json").read_text(encoding="utf-8")
    assert '"packing/devtools/overview/**/*.js"' in config
    assert not re.search(
        r'"(noImplicitAny|strict[A-Za-z]*|noUnchecked[A-Za-z]*)"\s*:\s*false', config
    )
    for script in overview_page.SCRIPTS:
        assert script.suffix == ".js"
        assert script.parent == overview_page.SCRIPTS_DIR
    assert overview_page.SCRIPTS[0] == overview_page.FORWARD_SCRIPT


def test_the_render_inputs_cover_every_contract_and_document() -> None:
    inputs = set(overview_page.RENDER_INPUTS)
    for module in (overview_data, overview_media, reader_documents):
        assert set(module.RENDER_INPUTS) <= inputs, module.__name__
    assert set(overview_page.SCRIPTS) <= inputs
    try:
        listed = reader_documents.reader_documents()
    except NotImplementedError:  # pragma: no cover - the lanes land together
        pytest.skip("reader_documents is not implemented yet")
    for document in listed:
        path = REPO / document.path
        assert any(path == source or path.is_relative_to(source) for source in inputs), (
            document.path
        )


# ── The record, complete ─────────────────────────────────────────────────────────────


def test_every_recent_result_in_the_record_is_a_card() -> None:
    record = overview_data.load()
    html = real_body()
    cards = re.findall(r'href="#(result-t-\d+)" data-goes="down" data-popover="result"', html)
    assert cards == [
        overview_page.result_anchor(r) for r in (*record.recent_ours, *record.recent_others)
    ]


def test_every_register_entry_in_the_record_is_a_row() -> None:
    record = overview_data.load()
    rows = re.findall(r'<tr id="(result-t-\d+)"', real_body())
    assert rows == [overview_page.result_anchor(r) for g in record.groups for r in g.results]
    register = (REPO / "packing" / "frontier" / "results.yaml").read_text(encoding="utf-8")
    assert len(rows) == len(re.findall(r"^  - id: T-\d+$", register, re.MULTILINE))


# ── Mathematics ──────────────────────────────────────────────────────────────────────


def test_a_formula_is_written_as_kpress_writes_it() -> None:
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    source = r"s(11) \ge \frac{31}{8}"
    kpress = parse_markdown(
        f"${render_explainer.kerned_math(source)}$",
        title="t",
        trust_mode="trusted",
        math="auto",
    ).html
    assert overview_page.math_html(source) in kpress


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("s(11) ≥ 2 + 4/√5", r"s(11) \ge 2 + 4/\sqrt{5}"),
        (
            "955000*sqrt(518400042893309449)/179696714646249",
            r"955000\sqrt{518400042893309449}/179696714646249",
        ),
        ("n = 26…72", r"n = 26\ldots 72"),
        ("≤ U_hi", r"\le U_{\mathrm{hi}}"),
    ],
)
def test_the_registers_mathematics_is_set_as_tex(code: str, expected: str) -> None:
    assert overview_page.ascii_tex(code) == expected


@pytest.mark.parametrize(
    ("code", "is_math"),
    [
        ("n", True),
        ("s(n)", True),
        ("(1.74, 1)", True),
        ("rho", True),
        ("T-037", False),
        ("V4", False),
        ("CREDITS.md", False),
        ("devtools.verify_kleddamag_n11_native", False),
        ("packing/", False),
        ("frontier/n-011.md", False),
        ("n/2", True),
    ],
)
def test_a_code_span_is_mathematics_only_when_it_states_some(
    code: str,
    is_math: bool,  # noqa: FBT001 -- a parametrized expectation
) -> None:
    assert overview_page.looks_like_math(code) is is_math


def test_punctuation_after_a_formula_keeps_its_line() -> None:
    html = overview_page.inline_html("the case $n = 324$: done, and `s(11)`.")
    assert html.count(f"</math></span></span>{overview_page.WORD_JOINER}") == 2


# ── Scripts ──────────────────────────────────────────────────────────────────────────


def run_node(script: str) -> Callable[[], None]:
    def check() -> None:
        completed = node(
            [str(NODE_TESTS / script)],
            return_completed_process=True,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, f"{completed.stdout}{completed.stderr}"

    return check


def test_table_sorts_and_filters_to_its_contract() -> None:
    run_node("table.test.mjs")()


def test_forward_sends_old_deep_links_to_the_explainer() -> None:
    run_node("forward.test.mjs")()


def test_the_popover_opens_results_pages_and_documents() -> None:
    run_node("popover.test.mjs")()


def test_site_math_typesets_lazily() -> None:
    run_node("site-math.test.mjs")()
