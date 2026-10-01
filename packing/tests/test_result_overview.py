"""The result overview: every part present, every link resolving, nothing borrowed from
the popover that will hold it."""

from __future__ import annotations

import html
import re

import pytest

from devtools import (
    overview_data,
    overview_sections,
    register_prose,
    render_overview,
    repo_links,
    result_overview,
)
from devtools.render_case_pages import BROAD_RESULT
from devtools.render_recent_results import HOLDS, SUPERSEDED
from devtools.repo_links import DEFAULT_BRANCH, REPO, REPO_URL
from sqpack.yamlio import safe_load
from tests import site_renders

#: The three results the tests read part by part: one that settles a case, the result it
#: superseded on the same case, and one about 49 cases.
SETTLED, EARLIER, BROAD = "T-060", "T-037", "T-056"

HREF = re.compile(r'href="([^"]+)"')
LINE_LINK = re.compile(re.escape(REPO_URL) + r"/blob/main/([^\"?#]+)\?plain=1#L(\d+)")
STEP = re.compile(
    r'<li class="site-result-step" data-step="(t-\d{3})" data-standing="([a-z-]+)"'
)


@pytest.fixture(scope="module")
def overview() -> overview_data.Overview:
    return site_renders.overview()


@pytest.fixture(scope="module")
def bodies() -> dict[str, str]:
    """Every register result's overview, rendered once: that none fails is the first check."""
    return site_renders.result_bodies()


def _result(overview: overview_data.Overview, result_id: str) -> overview_data.Result:
    return next(result for result in overview.results if result.id == result_id)


def test_every_register_result_has_an_overview(bodies: dict[str, str]) -> None:
    register = safe_load(overview_data.RESULTS.read_text(encoding="utf-8"))["results"]
    assert set(bodies) == {record["id"] for record in register}
    for result_id, body in bodies.items():
        assert body.startswith(
            f'<div class="site-result" data-result-overview="{result_id.lower()}">'
        )
        assert body.endswith("</div>")
        # The body is placed in a Markdown HTML block, which a blank line would end.
        assert "\n\n" not in body, result_id
        assert not re.search(r"\{\{[A-Z_]+\}\}", body), result_id


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_head_states_the_result_as_the_site_does(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """The claim with its math set, the rung and standing chips of the tables, the date
    and what it dates, and the register's credit. The id and the headline are not
    repeated: the popover that holds the body carries them, above it."""
    result = _result(overview, result_id)
    record = result.record
    head = bodies[result_id].split("</header>", 1)[0]
    assert head.startswith(
        f'<div class="site-result" data-result-overview="{result_id.lower()}">'
        '<header class="site-result-head"><p class="site-result-status">'
    )
    assert "site-card-label" not in head
    assert "site-popover-value" not in head
    # One paragraph element for each paragraph of the claim, in order.
    paragraphs = register_prose.paragraphs(record["claim"])
    claim = "".join(
        f'<p class="site-result-claim">{overview_data.tex_bounds(paragraph)}</p>'
        for paragraph in paragraphs
    )
    assert claim in head
    assert head.count('<p class="site-result-claim">') == len(paragraphs)
    assert "kpress-math" in claim
    assert overview_sections.status_chips(result) in head
    for rung in (record["verification"], record["confirmation"]):
        assert f'data-rung="{rung[0]}" data-level="{rung[1:]}">{rung}</span>' in head
    kind, dated = result.dated
    assert f'<span class="site-date-kind">{kind}</span> {dated}' in head
    assert html.escape(result.credit) in head
    assert "Significance" in head
    assert f'data-novelty="{result.novelty}"' in head


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER])
def test_a_single_case_shows_the_films_panel_and_the_packing(
    result_id: str, bodies: dict[str, str]
) -> None:
    """The number line, the chained bound, the badges and the citation are the atlas
    popover's panel, from the film's own facts, beside the atlas drawing of the case; the
    case record's verified and reported bounds and the gap follow."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    body = bodies[result_id]
    fact = result_overview.film_facts()[11]
    assert body.count('class="site-atlas-pop site-result-film" data-overview-case="11"') == 1
    assert packing_svg(11, units=overview_sections.ATLAS_UNITS) in body
    # The gap bar: the scale's integers, sqrt(n) and sqrt(n) + 1, and the best known side.
    bar = body.split('<div class="site-atlas-gap">', 1)[1].split("site-atlas-pop-head", 1)[0]
    for label in ("3", "4", "5", "3.317", "4.317"):
        assert f">{label}</span>" in bar, label
    assert '<span class="is-upper" style="left: ' in bar
    assert ">3.877</span>" in bar
    assert bar.count('class="site-atlas-gap-rule"') == 1  # exact: one rule, no lower
    # The chained bound, as the film states it, with its star and badges.
    assert overview_data.math_html(f"s(11) = {fact['upper']}") in body
    assert '<span class="site-atlas-pop-star" aria-hidden="true">\u2605</span>' in body
    for _, _, label in fact["badges"]:
        assert f"</span>{label}</li>" in body
    for which in ("lower", "upper"):
        assert html.escape(fact["cite"][which]["text"]) in body
    # The record's four bounds and its gap, each a link into the case file's frontmatter.
    table = body.split('class="site-result-bounds"', 1)[1].split("</div></div></div>", 1)[0]
    assert table.count('role="row"') == 4
    lines = result_overview.case_bound_lines(11)
    for key, _ in result_overview.CASE_BOUNDS:
        assert f"packing/frontier/n-011.md?plain=1#L{lines[key]}" in table
    assert "solved: the verified bounds meet" in table


def test_an_open_case_draws_both_bounds_and_the_span_between(bodies: dict[str, str]) -> None:
    """T-057, de Winter's 211 squares: the proved lower bound and the best known side each
    get a rule and a value, with the open span between them, and the statement chains
    them."""
    body = bodies["T-057"]
    fact = result_overview.film_facts()[211]
    bar = body.split('<div class="site-atlas-gap">', 1)[1].split("site-atlas-pop-head", 1)[0]
    assert bar.count('class="site-atlas-gap-rule"') == 2
    assert f">{float(fact['lower']):.3f}</span>" in bar
    assert f">{float(fact['upper']):.3f}</span>" in bar
    assert '<span class="site-atlas-gap-open" style="left: ' in bar
    assert f'<span class="is-lower">{overview_data.math_html(fact["lower"])}</span>' in body
    assert overview_data.math_html(r"{}\le s(211) \le{}") in body
    assert f'<span class="is-upper">{overview_data.math_html(fact["upper"])}</span>' in body


def test_a_broad_result_lists_its_cases_instead_of_drawing_them(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """Couzo's 49 packings: no number line and no drawing, a sentence saying so, and one
    row per case linking its record, its frontier row and its case file."""
    body = bodies[BROAD]
    cases = result_overview.scope(_result(overview, BROAD))
    assert len(cases) == 49 > BROAD_RESULT
    assert "site-atlas-gap" not in body
    assert "<svg" not in body
    assert "This result concerns 49 cases, too many to draw one by one." in body
    listing = body.split('class="site-result-cases"', 1)[1].split("</div></div></section>", 1)[
        0
    ]
    assert re.findall(r'data-overview-case="(\d+)"', listing) == [str(n) for n in cases]
    facts = result_overview.film_facts()
    for n in cases:
        row = listing.split(f'data-overview-case="{n}"', 1)[1].split('role="row"', 1)[0]
        assert f'<a href="cases.html#n-{n}">{n}</a>' in row
        assert f'<a href="frontier.html#n-{n}">frontier</a>' in row
        assert f"{REPO_URL}/blob/main/packing/frontier/n-{n:03d}.md" in row
        assert f'<span class="is-upper">{facts[n]["upper"]}</span>' in row


def test_a_result_about_a_few_cases_draws_each(bodies: dict[str, str]) -> None:
    """T-019 concerns n = 17, 18 and 19: three panels, each headed by its n."""
    body = bodies["T-019"]
    assert re.findall(r'site-result-film" data-overview-case="(\d+)"', body) == [
        "17",
        "18",
        "19",
    ]
    assert body.count('<div class="site-atlas-gap">') == 3
    assert body.count('class="site-popover-value site-result-case-n"') == 3


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_chain_is_every_result_on_the_case_oldest_first(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """Each step names its result, links its row, and carries its standing; the result the
    overview is about is marked; and each step links the register entry at its line."""
    result = _result(overview, result_id)
    cases = set(result_overview.scope(result))
    expected = [
        other for other in overview.results if cases & set(result_overview.scope(other))
    ]
    expected.sort(key=lambda other: (other.dated[1], other.id))
    body = bodies[result_id]
    steps = STEP.findall(body)
    assert [step for step, _ in steps] == [other.id.lower() for other in expected]
    assert len(steps) > 1
    assert body.count('data-current=""') == 1
    current = body.split('data-current=""', 1)[0].rsplit("<li ", 1)[1]
    assert f'data-step="{result_id.lower()}"' in current
    lines = result_overview.result_lines()
    for other in expected:
        step = body.split(f'data-step="{other.id.lower()}"', 1)[1].split("</li>", 1)[0]
        assert f'<a href="all-results.html#{other.id.lower()}">{other.id}</a>' in step
        assert overview_data.tex_bounds(other.summary) in step
        assert overview_sections.standing_chips(other.standing) in step
        assert f"packing/frontier/results.yaml?plain=1#L{lines[other.id]}" in step
        assert html.escape(other.credit) in step
        for key in (other.record.get("attribution") or {}).get("source_keys") or []:
            assert html.escape(key.strip("[]")) in step


def test_the_chain_on_eleven_squares_says_how_each_result_stands_there(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    """T-060 holds the case and T-037 is superseded; T-047 is the current best at other
    cases and superseded at n = 11, and its step says both."""
    steps = dict(STEP.findall(bodies[SETTLED]))
    assert steps["t-060"] == overview_sections.standing_key(HOLDS)
    assert steps["t-037"] == overview_sections.standing_key(SUPERSEDED)
    wide = _result(overview, "T-047")
    assert wide.standing == HOLDS
    assert result_overview.standing_on(wide, [11]) == SUPERSEDED
    step = bodies[SETTLED].split('data-step="t-047"', 1)[1].split("</li>", 1)[0]
    assert overview_sections.standing_chips(HOLDS) in step
    assert "on this case, superseded" in step
    assert steps["t-047"] == overview_sections.standing_key(SUPERSEDED)


@pytest.mark.parametrize("result_id", [SETTLED, EARLIER, BROAD])
def test_the_links_reach_the_site_and_the_record(
    result_id: str, overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    result = _result(overview, result_id)
    record = result.record
    links = bodies[result_id].split('class="site-result-section site-result-links"', 1)[1]
    assert f'<a href="all-results.html#{result_id.lower()}">' in links
    if result_id == BROAD:
        assert '<a href="frontier.html">' in links
        assert '<a href="cases.html">' in links
    else:
        assert '<a href="cases.html#n-11">' in links
        assert '<a href="frontier.html#n-11">' in links
        assert '<a href="explainer.html">' in links
        assert f'{REPO_URL}/blob/main/packing/frontier/n-011.md"' in links
    line = result_overview.result_lines()[result_id]
    assert f"packing/frontier/results.yaml?plain=1#L{line}" in links
    assert f"line {line}" in links
    for item in record["evidence"]:
        at = result_overview.evidence_lines()[item]
        assert f"packing/frontier/evidence.yaml?plain=1#L{at}" in links, item
        assert f"<code>{item}</code>" in links
    for key in record["attribution"]["source_keys"]:
        at = result_overview.bibliography_lines()[key]
        assert f"packing/resources/bibliography.yaml?plain=1#L{at}" in links, key
    for path in [*record["artifacts"], *record["controls"]]:
        assert f'{REPO_URL}/blob/main/{path}"' in links, path
    assert "README.md" in links.split("Source packet", 1)[1].split("</dd>", 1)[0]
    if record.get("review_artifact"):
        assert f'{REPO_URL}/blob/main/{record["review_artifact"]}"' in links


def test_every_github_link_names_main_and_a_path_in_the_tree(bodies: dict[str, str]) -> None:
    """No overview links a commit, every repository link is a `blob` or `tree` on `main`,
    and every path is in the tree at `HEAD`, which `main` holds when the site deploys."""
    tree = repo_links.repository_tree()
    on_main = re.compile(re.escape(REPO_URL) + rf"/(?:blob|tree)/{DEFAULT_BRANCH}/")
    total = 0
    for result_id, body in bodies.items():
        assert not repo_links.hash_pinned_links(body), result_id
        github = [href for href in HREF.findall(body) if href.startswith(REPO_URL + "/")]
        assert github, result_id
        total += len(github)
        for href in github:
            assert on_main.match(href), (result_id, href)
        paths = repo_links.branch_paths(body)
        assert paths
        assert not tree.missing(paths), (result_id, tree.missing(paths))
    assert total > 1000


def test_every_line_anchor_opens_the_entry_it_names(bodies: dict[str, str]) -> None:
    """A line link into the register, the evidence, the bibliography or a case file lands
    on the entry or the field, read from the files as they are."""
    texts: dict[str, list[str]] = {}
    seen: set[str] = set()
    for result_id, body in bodies.items():
        own = False
        for path, number in LINE_LINK.findall(body):
            if path not in texts:
                texts[path] = (REPO / path).read_text(encoding="utf-8").splitlines()
            line = texts[path][int(number) - 1]
            name = path.rsplit("/", 1)[-1]
            seen.add(name if not name.startswith("n-") else "case file")
            if name == "results.yaml":
                assert re.fullmatch(r"  - id: T-\d{3}", line), (result_id, line)
                own = own or line == f"  - id: {result_id}"
            elif name == "evidence.yaml":
                assert re.fullmatch(r"  - id: E-[a-z0-9-]+", line), (result_id, line)
            elif name == "bibliography.yaml":
                assert re.fullmatch(r"  - key: '\[.+\]'", line), (result_id, line)
            else:
                assert re.fullmatch(r"n-\d{3}\.md", name), path
                assert re.match(r"  (verified|reported)_(lower|upper)_bound:", line), line
        assert own, f"{result_id} does not link its own register entry"
    assert seen == {"results.yaml", "evidence.yaml", "bibliography.yaml", "case file"}


def test_every_site_link_is_a_served_page_and_a_real_fragment(
    overview: overview_data.Overview, bodies: dict[str, str]
) -> None:
    rows = {result.id.lower() for result in overview.results}
    cases = {f"n-{n}" for n in overview.cases}
    for result_id, body in bodies.items():
        for href in HREF.findall(body):
            if href.startswith("https://"):
                continue
            page, _, fragment = href.partition("#")
            assert page in render_overview.SITE_PAGES, (result_id, href)
            if page == render_overview.RESULTS_PAGE:
                assert fragment in rows, href
            elif page in {"cases.html", "frontier.html"}:
                assert not fragment or fragment in cases, href
            else:
                assert page == "explainer.html", href
                assert not fragment


def test_a_link_to_nothing_fails_the_render(overview: overview_data.Overview) -> None:
    """The check a render runs: a path the tree lacks, a commit, a page the site does not
    serve and a fragment no row carries are each refused."""
    check = result_overview.check_links
    check("T-000", f'<a href="{REPO_URL}/blob/main/README.md">ok</a>', overview)
    refused = (
        f'<a href="{REPO_URL}/blob/main/packing/frontier/n-999.md">x</a>',
        f'<a href="{REPO_URL}/tree/main/README.md">x</a>',
        f'<a href="{REPO_URL}/blob/0123456789abcdef/README.md">x</a>',
        '<a href="nowhere.html">x</a>',
        '<a href="cases.html#n-999">x</a>',
        '<a href="all-results.html#t-999">x</a>',
    )
    for body in refused:
        with pytest.raises(SystemExit):
            check("T-000", body, overview)


def test_the_overview_depends_on_no_popover(bodies: dict[str, str]) -> None:
    """The body is content alone: no id, no popover of its own, no script, and no table
    for a results table's script to count, so any page may place it, more than once. The
    module calls nothing of the row mechanism that shows it."""
    for result_id, body in bodies.items():
        assert not re.search(r'\sid="', body), result_id
        assert "popover" not in re.sub(r'class="[^"]*"', "", body), result_id
        for tag in ("<script", "<table", "<tr", "<iframe", "<button"):
            assert tag not in body, (result_id, tag)
        assert not re.search(r"\sdata-(result|n|case|atlas-(?!open))[=\s>]", body), result_id
    source = (render_overview.PACKING / "devtools" / "result_overview.py").read_text(
        encoding="utf-8"
    )
    assert "result_row_popover_body" not in source
    assert "import overview_sections" not in source.split('"""', 2)[2].split("\ndef ", 1)[0]


def test_the_gap_bar_keeps_the_films_scale() -> None:
    """The bar is placed here with the scale `atlas-grid.js` draws the atlas popover's
    with; the script's constants are read so the two cannot drift apart."""
    script = render_overview.ATLAS_GRID_SCRIPT.read_text(encoding="utf-8")
    # The constants are read out of the script by pattern, not quoted as JavaScript.
    inset = re.search(r"\bINSET = (\d+);", script)
    span = re.search(r"\(value - lo\) / (\d+)\)\) \* \(100 - 2 \* INSET\)", script)
    assert inset is not None
    assert int(inset.group(1)) == result_overview.GAP_INSET
    assert span is not None
    assert int(span.group(1)) == result_overview.GAP_SPAN
    assert re.search(r"\blo = Math\.ceil\(root\) - 1;", script)
    assert "value.toFixed(3)" in script
    assert [result_overview.grid_floor(n) for n in (1, 2, 4, 5, 11, 16, 17)] == [
        0,
        1,
        1,
        2,
        3,
        3,
        4,
    ]
    assert result_overview.bar_at(3, 3) == 5
    assert result_overview.bar_at(4, 3) == 50
    assert result_overview.bar_at(5, 3) == 95
    assert result_overview.bar_at(9, 3) == 95
    assert result_overview.bar_number(18.0) == "18"
    assert result_overview.bar_number(3.8770836) == "3.877"


def test_two_close_values_sit_either_side_of_their_marks() -> None:
    """Values that would overlap centred on their marks are anchored apart."""
    near = {"n": 17, "exact": False, "upper": "4.675531", "lower": "4.660440"}
    bar = result_overview.gap_bar(near)
    assert '<span class="is-lower" data-anchor="end"' in bar
    assert '<span class="is-upper" data-anchor="start"' in bar
    far = {"n": 211, "exact": False, "upper": "14.997961", "lower": "14.100000"}
    assert "data-anchor" not in result_overview.gap_bar(far)


def test_the_stylesheet_is_its_own_file_on_the_sites_tokens() -> None:
    """The overview's styles ride every site page after `site.css`, declare no text token
    and no colour of their own, key on no system theme and add no hover timing."""
    css = render_overview.SITE_RESULT_CSS.read_text(encoding="utf-8")
    assert render_overview.SITE_RESULT_CSS.name == "site-result.css"
    head, _ = render_overview.page_assets()
    site = render_overview.SITE_CSS.read_text(encoding="utf-8")
    assert head.index(site) < head.index(css)
    assert render_overview.SITE_RESULT_CSS in render_overview.RENDER_INPUTS
    assert "prefers-color-scheme" not in css
    assert "transition" not in css
    for owned in (
        "--kpress-host-font-size-base:",
        "--kpress-measure:",
        "--kpress-font-size-h2:",
    ):
        assert owned not in css
    rules = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|oklch\(|rgb\(|hsl\(", rules)
    assert not re.search(r"^\s*--[a-z-]+:", rules, flags=re.MULTILINE)
    assert ".site-popover:has(.site-result, [data-row-pop-src])" in rules
    # The panel's height has one limit. `max-height` is the same property as
    # `max-block-size` here, and the later of the two in a rule is the one that holds.
    opened = rules.split(
        ".site-popover:has(.site-result, [data-row-pop-src]):popover-open {", 1
    )[1]
    opened = opened.split("}", 1)[0]
    assert "max-block-size: min(92dvh, 58rem);" in opened
    assert "max-height" not in opened
    assert "preview" not in css


def test_the_design_document_describes_the_overview() -> None:
    design = (render_overview.TEMPLATES / "paper-design.md").read_text(encoding="utf-8")
    assert "\n## Result Overview\n" in design
    section = design.split("\n## Result Overview\n", 1)[1].split("\n## ", 1)[0]
    for name in ("site-result.css", "result_overview.py", "atlas_film_facts"):
        assert name in section, name
