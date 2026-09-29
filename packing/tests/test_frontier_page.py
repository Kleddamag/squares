"""The frontier atlas page: one row per case record, every value read from the record."""

from __future__ import annotations

import shutil
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from devtools import render_frontier_page as frontier
from devtools import render_overview
from devtools import render_research_tables as tables
from devtools.render_overview import PAGES, assert_self_contained
from sqpack.yamlio import safe_load

#: Measured at 3.6 MB on 2026-09-29 (324 cases): 1.6 MB is the site shell every page
#: carries (the explainer's inlined faces and KaTeX), about 0.95 MB the 324 thumbnails
#: and the rest the cells and their record links. The ceiling leaves room for the corpus
#: to grow a little; a change that crosses it should shrink something rather than lift it.
PAGE_CEILING_BYTES = 4 * 1024 * 1024

#: The value columns and the record field each one's `data-value` carries.
VALUE_COLUMNS = {
    2: "reported_upper_bound",
    3: "verified_upper_bound",
    4: "reported_lower_bound",
    5: "verified_lower_bound",
}


class Rows(HTMLParser):
    """Each body row's attributes and its cells' attributes, in order."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[tuple[dict[str, str | None], list[dict[str, str | None]]]] = []
        self._body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tbody":
            self._body = True
        elif tag == "tr" and self._body:
            self.rows.append((dict(attrs), []))
        elif tag == "td" and self._body and self.rows:
            self.rows[-1][1].append(dict(attrs))

    def handle_endtag(self, tag: str) -> None:
        if tag == "tbody":
            self._body = False


@pytest.fixture(scope="module")
def page() -> str:
    return PAGES["frontier.html"]().html


@pytest.fixture(scope="module")
def rows(page: str) -> list[tuple[dict[str, str | None], list[dict[str, str | None]]]]:
    parser = Rows()
    parser.feed(page)
    return parser.rows


@pytest.fixture(scope="module")
def cases() -> dict[int, dict[str, Any]]:
    return {case["n"]: case for case in tables.load_cases()}


def test_every_case_file_is_a_row_and_every_row_a_case_file(rows) -> None:
    files = sorted(int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md"))
    shown = [int(attributes["data-n"] or 0) for attributes, _ in rows]
    assert shown == files
    assert len(shown) == len(set(shown))


def test_every_value_cell_carries_the_records_value(rows, cases) -> None:
    for attributes, cells in rows:
        case = cases[int(attributes["data-n"] or 0)]
        assert cells[0]["data-value"] == str(case["n"])
        assert cells[1]["data-value"] == case["status"]
        assert attributes["data-status"] == case["status"]
        for column, field in VALUE_COLUMNS.items():
            assert cells[column]["data-value"] == str(case[field]["value"]), (case["n"], field)


def test_the_gap_is_exact_where_both_bounds_are(rows, cases) -> None:
    gaps = {
        int(attributes["data-n"] or 0): cells[6]["data-value"] for attributes, cells in rows
    }
    for n, case in cases.items():
        if case["status"] == "proved":
            assert gaps[n] == "0", n
    # s(12): verified upper 4, verified lower 15680/3951, so the gap is 124/3951.
    assert gaps[12] is not None
    assert abs(float(gaps[12]) - 124 / 3951) < 1e-15
    html_12, _ = frontier.gap(cases[12])
    assert r"\dfrac{124}{3951}" in html_12


def test_an_invalid_record_fails_the_render(tmp_path: Path, monkeypatch) -> None:
    source = tables.FRONTIER / "n-011.md"
    shutil.copy(tables.FRONTIER / "square-packing-case.schema.yaml", tmp_path)
    text = source.read_text(encoding="utf-8")
    front = safe_load(text.split("---\n")[1])
    assert front["packing"]["status"] == "open"
    broken = text.replace("\n  status: open\n", "\n  status: unknown\n", 1)
    assert broken != text
    (tmp_path / "n-011.md").write_text(broken, encoding="utf-8")
    monkeypatch.setattr(tables, "FRONTIER", tmp_path)
    with pytest.raises(SystemExit, match=r"n-011\.md is not a valid case record"):
        frontier.frontier_cases()


def test_the_page_is_self_contained_and_under_its_ceiling(page: str) -> None:
    assert_self_contained("frontier.html", page)
    size = len(page.encode("utf-8"))
    assert size < PAGE_CEILING_BYTES, f"frontier.html is {size:,} bytes"


def test_the_page_carries_the_table_script_and_its_controls(page: str) -> None:
    assert frontier.TABLE_SCRIPT.read_text(encoding="utf-8") in page
    assert 'class="site-table-tools" data-table="frontier" hidden' in page
    assert 'aria-current="page" href="frontier.html"' in page


def test_no_math_is_left_as_source_text_in_the_table(page: str) -> None:
    table = page[page.index("<tbody>") : page.index("</tbody>")]
    assert "$" not in table
    assert "sqrt(" not in table
    assert r"\(\dfrac{31}{8}\)" in table


def test_the_frontier_inputs_are_render_inputs() -> None:
    for path in frontier.FRONTIER_INPUTS:
        assert path in render_overview.inputs()
        assert path.exists(), path


@pytest.mark.parametrize(
    ("form", "tex"),
    [
        ("31/8", r"\frac{31}{8}"),
        ("2 + (1/2)sqrt(2)", r"2 + \frac{1}{2}\sqrt{2}"),
        ("4 + 2 sqrt(2)", r"4 + 2\sqrt{2}"),
        ("sqrt(37 - 2*floor(sqrt(37)) + 1) + 1", r"1 + \sqrt{26}"),
        ("94*sqrt(2)/41 + 247/41", r"\frac{94\sqrt{2}}{41} + \frac{247}{41}"),
        (
            "7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))",
            r"7 - \frac{1}{2}\sqrt{2} + \sqrt{1 + \sqrt{2}}",
        ),
    ],
)
def test_exact_forms_render_as_latex(form: str, tex: str) -> None:
    assert tables.latex(form) == tex


def test_a_polynomial_root_has_no_closed_form() -> None:
    with pytest.raises(ValueError, match="polynomial root"):
        tables.latex("root(P_trump11, 3.877)")
    bound = {"value": "3.87708359002281417730789706010096", "exact_form": "root(P, 3.877)"}
    assert "3.87708359…" in frontier.value_html(bound)


def test_every_thumbnail_draws_its_cases_squares() -> None:
    svg = frontier.thumbnail_svg(11)
    assert svg.count("z") == 11
    assert "id=" not in svg


def test_a_minimal_polynomial_with_radical_coefficients_renders_as_latex() -> None:
    tex = tables.polynomial_latex("24s^4-(1400+352sqrt(2))s^3+641430=0")
    assert tex == r"24s^4-(1400+352\sqrt{2})s^3+641430=0"
    with pytest.raises(ValueError, match="no LaTeX form"):
        tables.polynomial_latex("s^2 - log(2) = 0")
