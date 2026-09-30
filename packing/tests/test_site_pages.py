"""The frontier atlas and the tutorial are rendered from the record, and their links hold.

`devtools.site_pages` renders the frontier atlas from the validated case records and the
tutorial from `TUTORIAL.md`, and proves every site page's links offline. Held here: every
case file is a row and every row a case file, each rendered value parses back to its
record, an invalid record refuses the render, the relation on a lower bound comes from the
register, decimals are cut rather than rounded, the tutorial's links go where the spec
sends them and no `$` reaches its page unrendered, and the link check finds a planted
missing path while passing the real pages.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from html.parser import HTMLParser
from pathlib import Path

import pytest

from devtools import overview_media, render_overview, render_research_tables, site_pages
from devtools.render_research_tables import pretty
from devtools.site_kit import REPO_URL, Page
from devtools.site_pages import (
    ELLIPSIS,
    PLACES,
    anchor_problems,
    cut,
    default_branch_links,
    gap,
    link_problems,
    read_exact,
    repository_link,
    repository_link_problems,
    rewrite_links,
    shown,
    surd,
    tex,
)
from sqpack.assurance import bounds_agree_at_declared_precision

COMMIT = render_overview.render_explainer.link_revision()
#: The frontier page's HTML in the shared shell, measured at 2,967,588 bytes on
#: 2026-09-30: the shell's inlined faces and scripts are 1.64 MB of it, and the table's
#: 503 formulas, each with the MathML kpress writes beneath it, most of the rest.
FRONTIER_CEILING = 3_300_000
#: The tutorial page in the shell, measured at 1,851,670 bytes on 2026-09-30.
TUTORIAL_CEILING = 2_100_000


@dataclass
class Cell:
    attrs: dict[str, str]
    html: list[str] = field(default_factory=list)
    classes: set[str] = field(default_factory=set)

    @property
    def text(self) -> str:
        return "".join(self.html)


@dataclass
class TableRow:
    attrs: dict[str, str]
    cells: list[Cell] = field(default_factory=list)


class Rows(HTMLParser):
    """The frontier table's body rows, each cell's attributes, text and image sources."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[TableRow] = []
        self.images: dict[int, list[dict[str, str]]] = {}
        self.in_body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if tag == "tbody":
            self.in_body = True
        elif self.in_body and tag == "tr":
            self.rows.append(TableRow(values))
        elif self.in_body and tag == "td":
            self.rows[-1].cells.append(Cell(values))
        elif self.in_body and tag == "img":
            self.images.setdefault(len(self.rows) - 1, []).append(values)
        if self.in_body and tag != "td" and self.rows and self.rows[-1].cells:
            self.rows[-1].cells[-1].classes.update(values.get("class", "").split())

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tbody":
            self.in_body = False

    def handle_data(self, data: str) -> None:
        if self.in_body and self.rows and self.rows[-1].cells:
            self.rows[-1].cells[-1].html.append(data)


class Unrendered(HTMLParser):
    """Text outside formulas, code and scripts, where a `$` would be unrendered math."""

    SKIPPED = frozenset({"code", "pre", "script", "style"})
    VOID = frozenset(
        {"area", "br", "col", "hr", "img", "input", "link", "meta", "source", "wbr"}
    )

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth: list[str] = []
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        if tag not in self.VOID and (
            self.depth or tag in self.SKIPPED or "kpress-math" in classes
        ):
            self.depth.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self.depth and self.depth[-1] == tag:
            self.depth.pop()

    def handle_data(self, data: str) -> None:
        if not self.depth:
            self.text.append(data)


def unrendered_dollars(html: str) -> list[str]:
    parser = Unrendered()
    parser.feed(html)
    parser.close()
    text = "".join(parser.text)
    return [text[max(0, i - 30) : i + 30] for i, char in enumerate(text) if char == "$"]


@pytest.fixture(scope="module")
def frontier() -> Page:
    return site_pages.frontier_page(COMMIT)


@pytest.fixture(scope="module")
def tutorial() -> Page:
    return site_pages.tutorial_page(COMMIT)


@pytest.fixture(scope="module")
def frontier_html(frontier: Page) -> str:
    return render_overview.page_html(frontier, commit=COMMIT)


@pytest.fixture(scope="module")
def tutorial_html(tutorial: Page) -> str:
    return render_overview.page_html(tutorial, commit=COMMIT)


@pytest.fixture(scope="module")
def rows(frontier: Page) -> Rows:
    parser = Rows()
    parser.feed(frontier.html or "")
    parser.close()
    return parser


@pytest.fixture(scope="module")
def cases() -> dict[int, dict]:
    return {case["n"]: case for case in render_research_tables.load_cases()}


def test_the_pages_are_the_frontier_atlas_and_the_tutorial() -> None:
    assert [(page.key, page.path) for page in site_pages.pages(COMMIT)] == [
        ("frontier", "frontier.html"),
        ("tutorial", "tutorial.html"),
    ]


def test_every_case_file_is_a_row_and_every_row_a_case_file(rows: Rows) -> None:
    files = sorted(int(path.stem[2:]) for path in site_pages.FRONTIER.glob("n-*.md"))
    shown_n = [int(row.attrs["data-n"]) for row in rows.rows]
    assert shown_n == files
    assert len(shown_n) == len(set(shown_n))


BOUND_COLUMNS = (
    (2, "reported_upper_bound"),
    (3, "verified_upper_bound"),
    (4, "reported_lower_bound"),
    (5, "verified_lower_bound"),
)


def test_each_rendered_value_parses_back_to_its_record(rows: Rows, cases: dict) -> None:
    for row in rows.rows:
        case = cases[int(row.attrs["data-n"])]
        assert row.attrs["data-status"] == case["status"]
        assert ("open" in row.attrs["data-flags"].split()) == (case["status"] == "open")
        assert row.cells[0].attrs["data-value"] == str(case["n"])
        for column, key in BOUND_COLUMNS:
            attrs = row.cells[column].attrs
            bound = case[key]
            assert Decimal(attrs["data-value"]) == Decimal(str(bound["value"])), (
                case["n"],
                key,
            )
            assert attrs.get("data-exact") == bound["exact_form"], (case["n"], key)


def test_every_verified_value_is_printed_and_cut_never_rounded(rows: Rows, cases: dict) -> None:
    unit = Fraction(1, 10**PLACES)
    for row in rows.rows:
        case = cases[int(row.attrs["data-n"])]
        for column, key in ((3, "verified_upper_bound"), (5, "verified_lower_bound")):
            bound = case[key]
            view = shown(bound)
            assert view.decimal in row.cells[column].text, (case["n"], key)
            # The printed digits are a prefix of the value, never rounded up past it ...
            digits = Fraction(Decimal(view.decimal.removesuffix(ELLIPSIS)))
            assert digits <= view.magnitude < digits + unit, (case["n"], key)
            # ... and the value read from the exact form is the record's, to the places the
            # record's own decimal declares.
            recorded = Decimal(str(bound["value"]))
            exponent = recorded.as_tuple().exponent
            assert isinstance(exponent, int)
            declared = Fraction(10) ** exponent
            assert abs(view.magnitude - Fraction(recorded)) <= declared, (case["n"], key)


def test_a_reported_value_the_verified_lane_confirms_is_printed_once(
    rows: Rows, cases: dict
) -> None:
    for row in rows.rows:
        case = cases[int(row.attrs["data-n"])]
        agrees = bounds_agree_at_declared_precision(
            case["reported_lower_bound"], case["verified_lower_bound"]
        )
        cell = row.cells[4]
        assert ("frontier-verified" in cell.classes) == agrees, case["n"]
        assert ("frontier-value" in cell.classes) != agrees, case["n"]


def test_an_invalid_record_refuses_the_render(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for path in site_pages.FRONTIER.glob("n-*.md"):
        shutil.copy(path, tmp_path / path.name)
    shutil.copy(
        site_pages.FRONTIER / "square-packing-case.schema.yaml",
        tmp_path / "square-packing-case.schema.yaml",
    )
    planted = tmp_path / "n-011.md"
    planted.write_text(
        planted.read_text(encoding="utf-8").replace(
            "  status: open\n", "  status: closed\n", 1
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(render_research_tables, "FRONTIER", tmp_path)
    with pytest.raises(SystemExit, match="fail their contract"):
        site_pages.frontier_cases()
    case = render_research_tables.load_cases()[10]
    problems = site_pages.case_problems(planted, case)
    assert any("status" in problem for problem in problems)


def test_a_record_declaring_a_softer_contract_is_refused(tmp_path: Path) -> None:
    source = site_pages.FRONTIER / "n-005.md"
    planted = tmp_path / "n-005.md"
    planted.write_text(
        source.read_text(encoding="utf-8").replace("status: enforced", "status: soft", 1),
        encoding="utf-8",
    )
    shutil.copy(
        site_pages.FRONTIER / "square-packing-case.schema.yaml",
        tmp_path / "square-packing-case.schema.yaml",
    )
    case = render_research_tables.load_cases()[4]
    assert site_pages.case_problems(planted, case)
    assert not site_pages.case_problems(source, case)


def test_the_strict_relation_comes_from_the_register(rows: Rows) -> None:
    by_n = {int(row.attrs["data-n"]): row for row in rows.rows}
    eleven = by_n[11].cells[5]
    assert eleven.attrs["data-relation"] == ">"
    assert eleven.text.lstrip().startswith(">")
    assert r"\frac{31}{8}" in eleven.text
    assert "T-037" in by_n[11].cells[8].text
    # A bound no entry claims strictly reads as the record states it.
    assert by_n[5].cells[5].attrs["data-relation"] == "≥"
    assert by_n[5].cells[5].text.lstrip().startswith("≥")


def test_a_strict_claim_at_another_value_or_without_the_evidence_is_not_taken() -> None:
    claims = site_pages.register_claims(
        [{"id": "T-900", "headline": "`s(11) > 31/8`", "evidence": ["E-a"]}]
    )
    bound = {"evidence": ["E-a"]}
    assert site_pages.relation(11, bound, Fraction(31, 8), claims) == (">", ("T-900",))
    assert site_pages.relation(11, bound, Fraction(38, 10), claims)[0] == "≥"
    assert site_pages.relation(11, {"evidence": ["E-b"]}, Fraction(31, 8), claims)[0] == "≥"
    assert site_pages.relation(12, bound, Fraction(31, 8), claims)[0] == "≥"


def test_an_algebraic_side_shows_its_minimal_polynomial(rows: Rows) -> None:
    by_n = {int(row.attrs["data-n"]): row for row in rows.rows}
    eleven = by_n[11].cells[8].text
    assert "minimal polynomial" in eleven
    assert "s^8 - 20s^7" in eleven
    assert "3.8770835" in by_n[11].cells[3].text


def test_every_row_loads_its_thumbnail_lazily(rows: Rows) -> None:
    for index, row in enumerate(rows.rows):
        n = int(row.attrs["data-n"])
        (image,) = rows.images[index]
        assert image["src"] == overview_media.thumbnail_path(n)
        assert image["loading"] == "lazy"
        assert "site-thumb" in image["class"].split()
        assert image["width"] == image["height"]
        assert int(image["width"]) > 0
        assert str(n) in image["alt"]


def test_the_recent_star_follows_the_atlas_citations(rows: Rows) -> None:
    recent = site_pages.recent_lower_bounds()
    assert recent
    for row in rows.rows:
        starred = "recent" in row.attrs["data-flags"].split()
        assert starred == (int(row.attrs["data-n"]) in recent)
        assert row.cells[7].attrs["data-value"] == ("1" if starred else "0")


def test_evidence_links_name_their_line_at_the_build_commit(rows: Rows, cases: dict) -> None:
    lines = site_pages.entry_lines(site_pages.EVIDENCE, "E-")
    text = site_pages.EVIDENCE.read_text(encoding="utf-8").splitlines()
    for identifier, line in lines.items():
        assert text[line - 1] == f"  - id: {identifier}"
    records = rows.rows[10].cells[8].text
    assert "n-011.md" in records
    for key in ("verified_upper_bound", "verified_lower_bound"):
        for identifier in cases[11][key]["evidence"]:
            assert identifier in records


def test_the_frontier_page_sorts_and_filters_by_the_table_scripts_contract(
    frontier: Page,
) -> None:
    html = frontier.html or ""
    assert '<table class="kpress-table site-table frontier-table" data-site-table' in html
    assert 'id="frontier-table"' in html
    assert 'data-filters-for="frontier-table"' in html
    for control in (
        'data-filter="status"',
        'data-filter-flag="open"',
        'data-filter-flag="recent"',
        'data-filter-min="n"',
        'data-filter-max="n"',
    ):
        assert control in html
    headers = re.findall(r"<th [^>]*>", html)
    assert sum('data-sort="number"' in header for header in headers) == 7
    assert "<details" in html
    assert frontier.scripts == (site_pages.TABLE_SCRIPT,)


def test_the_frontier_template_states_no_fact_as_a_literal() -> None:
    template = site_pages.FRONTIER_TEMPLATE.read_text(encoding="utf-8")
    prose = re.sub(r"<!--.*?-->", "", template, flags=re.DOTALL)
    assert not re.search(r"\d", prose)
    assert "{{FRONTIER_TABLE}}" in prose


def test_the_pages_stay_under_their_byte_ceilings(
    frontier_html: str, tutorial_html: str
) -> None:
    assert len(frontier_html.encode("utf-8")) <= FRONTIER_CEILING
    assert len(tutorial_html.encode("utf-8")) <= TUTORIAL_CEILING


# ---- Exact forms, decimals and gaps -------------------------------------------------


@pytest.mark.parametrize(
    ("exact", "expected"),
    [
        ("31/8", r"\frac{31}{8}"),
        ("2 + (1/2)sqrt(2)", r"2 + \tfrac{1}{2}\sqrt{2}"),
        ("9 + 4 sqrt(2)", r"9 + 4\sqrt{2}"),
        ("(13/2) + (1/2)sqrt(7)", r"\frac{13}{2} + \tfrac{1}{2}\sqrt{7}"),
        ("sqrt(37 - 2*floor(sqrt(37)) + 1) + 1", r"1 + \sqrt{26}"),
        (
            "18*sqrt(5)/101 + 2*sqrt(2) + 709/101",
            r"\frac{18\sqrt{5}}{101} + 2\sqrt{2} + \frac{709}{101}",
        ),
        (
            "7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))",
            r"7 - \tfrac{1}{2}\sqrt{2} + \sqrt{1 + \sqrt{2}}",
        ),
    ],
)
def test_exact_forms_are_set_as_mathematics(exact: str, expected: str) -> None:
    assert tex(read_exact(pretty(exact))) == expected


def test_exact_values_stay_in_the_square_root_field_where_they_can() -> None:
    assert surd(read_exact("2 + (1/2)√2")) == {1: Fraction(2), 2: Fraction(1, 2)}
    assert surd(read_exact("√48")) == {3: Fraction(4)}
    assert surd(read_exact("sqrt(37 - 2*floor(sqrt(37)) + 1) + 1")) == {26: 1, 1: 1}
    assert surd(read_exact("sqrt(1 + √2)")) is None


def test_decimals_are_cut_never_rounded() -> None:
    assert cut(Fraction(31, 8)) == "3.875"
    assert cut(Fraction("4.66044")) == "4.66044"
    assert cut(Fraction(2, 3)) == f"0.6666666{ELLIPSIS}"
    assert cut(Fraction("3.87708359002281")) == f"3.8770835{ELLIPSIS}"
    assert cut(Fraction(5)) == "5"
    with pytest.raises(ValueError, match="non-negative"):
        cut(Fraction(-1))


def test_a_gap_is_exact_where_both_bounds_are() -> None:
    upper = shown({"value": "4.88561808316412", "exact_form": "3 + (4/3)sqrt(2)"})
    lower = shown({"value": "4.8", "exact_form": "24/5"})
    difference = gap(upper, lower)
    assert difference.exact
    assert difference.decimal == f"0.0856180{ELLIPSIS}"
    assert difference.sort == "0.085618083164"
    grid = gap(
        shown({"value": "5", "exact_form": "5"}), shown({"value": "4.8", "exact_form": "24/5"})
    )
    assert (grid.decimal, grid.exact) == ("0.2", True)
    rooted = shown(
        {
            "value": "3.87708359002281417730789706010096",
            "exact_form": "root(P_trump11, 3.87708359002281417730789706010096)",
        }
    )
    inexact = gap(rooted, shown({"value": "3.875", "exact_form": "31/8"}))
    assert not inexact.exact
    assert inexact.decimal == f"0.0020835{ELLIPSIS}"
    with pytest.raises(SystemExit, match="below"):
        gap(lower, upper)


# ---- The tutorial ---------------------------------------------------------------------


def test_no_dollar_reaches_the_tutorial_unrendered(tutorial: Page) -> None:
    assert unrendered_dollars(tutorial.html or "") == []


def test_the_unrendered_math_check_has_teeth() -> None:
    html = site_pages.markdown_page_html(
        "# T\n\nInline $x^2$ is math, `$5` is code, and $$y$$ mid-sentence leaks.\n",
        commit=COMMIT,
        source_path="TUTORIAL.md",
        page="tutorial.html",
        title="T",
    )
    assert 'class="kpress-math' in html
    assert unrendered_dollars(html)


def test_the_tutorial_keeps_its_heading_ids_and_toc(tutorial: Page) -> None:
    html = tutorial.html or ""
    assert 'id="2-the-configuration-space"' in html
    assert 'class="kpress-toc kpress-no-print"' in html
    assert 'href="#2-the-configuration-space"' in html


def test_the_tutorial_links_the_explainer_on_the_site(tutorial: Page) -> None:
    html = tutorial.html or ""
    assert "jlevy.github.io" not in html
    assert 'href="explainer.html#proof-of-the-new-lower-bound"' in html


def test_the_tutorial_links_reader_documents_on_main_and_records_at_the_commit(
    tutorial: Page,
) -> None:
    html = tutorial.html or ""
    links = site_pages.repository_links(html)
    readers = [link for link in links if link.path in {"README.md", "SYNOPSIS.md"}]
    assert {link.path for link in readers} == {"README.md", "SYNOPSIS.md"}
    assert all((link.kind, link.ref) == ("blob", "main") for link in readers)
    records = [link for link in links if link.path.startswith("packing/")]
    assert records
    assert all(link.ref == COMMIT for link in records)
    images = re.findall(r'<img[^>]* src="([^"]+)"', html)
    assert images
    assert all(
        src.startswith(f"https://raw.githubusercontent.com/jlevy/squares/{COMMIT}/")
        for src in images
    )


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("https://jlevy.github.io/squares/#proof", "explainer.html#proof"),
        ("https://jlevy.github.io/squares/explainer.html#19-5", "explainer.html#19-5"),
        ("https://jlevy.github.io/squares/", "./"),
        ("https://jlevy.github.io/squares/tutorial.html#x", "#x"),
        ("https://jlevy.github.io/squares/frontier.html", "frontier.html"),
        ("TUTORIAL.md#2-the-configuration-space", "#2-the-configuration-space"),
        ("TUTORIAL.md", "tutorial.html"),
        ("#local", "#local"),
        ("SYNOPSIS.md#terminology", f"{REPO_URL}/blob/main/SYNOPSIS.md#terminology"),
        (
            "docs/project/research/research-2026-08-22-packing-11-unit-squares.md",
            (
                f"{REPO_URL}/blob/main/docs/project/research/"
                "research-2026-08-22-packing-11-unit-squares.md"
            ),
        ),
        ("packing/frontier/", f"{REPO_URL}/tree/{COMMIT}/packing/frontier"),
        ("packing/frontier/n-011.md", f"{REPO_URL}/blob/{COMMIT}/packing/frontier/n-011.md"),
        ("https://example.org/x", "https://example.org/x"),
    ],
)
def test_a_tutorial_link_goes_where_the_spec_sends_it(target: str, expected: str) -> None:
    assert (
        repository_link(target, commit=COMMIT, source="TUTORIAL.md", page="tutorial.html")
        == expected
    )


def test_a_directory_is_a_tree_at_the_commit_even_outside_the_checkout() -> None:
    placeholder = "0" * 40
    assert repository_link(
        "packing/frontier", commit=placeholder, source="TUTORIAL.md", page="tutorial.html"
    ) == (f"{REPO_URL}/tree/{placeholder}/packing/frontier")
    with pytest.raises(SystemExit, match="cannot list commit"):
        site_pages.listing(placeholder)


def test_a_site_asset_is_linked_on_the_site_not_on_github() -> None:
    path, name = next(iter(site_pages.served_assets().items()))
    assert (
        repository_link(path, commit=COMMIT, source="TUTORIAL.md", page="tutorial.html") == name
    )


def test_a_link_outside_the_repository_is_refused() -> None:
    with pytest.raises(SystemExit, match="outside the repository"):
        repository_link("../x.md", commit=COMMIT, source="TUTORIAL.md", page="tutorial.html")


def test_links_are_rewritten_in_attributes_never_in_text() -> None:
    html = (
        '<p><code>[a](README.md)</code> and <a class="x" href="README.md">README</a>'
        '<img alt="a" src="packing/a.svg"></p>'
    )
    rewritten = rewrite_links(html, lambda tag, name, value: f"{tag}:{name}:{value}")
    assert "<code>[a](README.md)</code>" in rewritten
    assert 'href="a:href:README.md"' in rewritten
    assert 'src="img:src:packing/a.svg"' in rewritten


# ---- Link checks, for every page of the site ------------------------------------------


def test_the_link_check_passes_both_real_pages(frontier_html: str, tutorial_html: str) -> None:
    assert link_problems(frontier_html, COMMIT) == []
    assert link_problems(tutorial_html, COMMIT) == []


def test_the_link_check_finds_a_planted_missing_path() -> None:
    html = (
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/frontier/n-011.md">ok</a>'
        f'<a href="{REPO_URL}/blob/{COMMIT}/packing/frontier/n-999.md">missing</a>'
        f'<a href="{REPO_URL}/tree/{COMMIT}/packing/frontier">ok</a>'
        f'<a href="{REPO_URL}/tree/{COMMIT}/packing/frontier/n-011.md">a file as a tree</a>'
        f'<a href="{REPO_URL}/blob/main/NOPE.md">missing on main</a>'
        f'<a href="{REPO_URL}/blob/v0.4.2/README.md">another ref</a>'
        f'<img src="https://raw.githubusercontent.com/jlevy/squares/{COMMIT}/nope.svg">'
    )
    problems = repository_link_problems(html, COMMIT)
    assert len(problems) == 5
    assert any("n-999.md" in problem for problem in problems)
    assert any("no directory" in problem for problem in problems)
    assert any("NOPE.md" in problem for problem in problems)
    assert any("v0.4.2" in problem for problem in problems)
    assert any("nope.svg" in problem for problem in problems)


def test_the_link_check_finds_a_broken_in_page_anchor() -> None:
    assert anchor_problems('<h2 id="a">A</h2><a href="#a">a</a>') == []
    assert anchor_problems('<a href="#b">b</a>') == ["in-page link #b has no target"]
    assert anchor_problems('<a href="#">top</a>') == []


def test_the_default_branch_links_are_listed_for_the_ref_rule(tutorial_html: str) -> None:
    listed = default_branch_links(tutorial_html)
    assert listed
    assert all(url.startswith(f"{REPO_URL}/blob/main/") for url in listed)
    assert f"{REPO_URL}/blob/main/SYNOPSIS.md" in listed
