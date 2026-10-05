"""The series figure vocabulary: roles, exact print helpers, and the bound ladder."""

from __future__ import annotations

import math
import re
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest
import yaml

from devtools import paper_figures as pf

SVG = f"{{{pf.SVG_NS}}}"


def test_a_diagram_wider_than_a_phone_is_refused() -> None:
    assert 'width="390"' in pf.svg("ok", "t", "d", width=390, height=10, body="")
    with pytest.raises(ValueError, match="wider than a phone"):
        pf.svg("wide", "t", "d", width=391, height=10, body="")


def test_a_diagram_is_titled_described_and_escaped() -> None:
    text = pf.svg(
        "x",
        "A < B",
        "C & D",
        width=100,
        height=50,
        body=pf.text(1, 2, "k < m", note=True),
        defs=pf.hatch("x-hatch"),
    )
    root = ET.fromstring(text)
    assert root.attrib["class"] == "n11-diagram n11-x"
    assert root.attrib["aria-labelledby"] == "n11-x-title n11-x-desc"
    title, desc = root.find(f"{SVG}title"), root.find(f"{SVG}desc")
    pattern = root.find(f"{SVG}defs/{SVG}pattern")
    assert title is not None
    assert desc is not None
    assert pattern is not None
    assert (title.text, desc.text, pattern.attrib["id"]) == ("A < B", "C & D", "x-hatch")
    label = root.find(f"{SVG}text")
    assert label is not None
    assert label.text == "k < m"
    assert label.attrib["class"] == "n11-diagram-note"


def test_each_role_paints_its_object_in_fixed_ink() -> None:
    """One stroke and colour role per object, every ink a fixed hex colour, so the
    paper's stylesheet must give these diagrams a light ground on the dark theme."""
    roles = (pf.CONTAINER, pf.PARENT, pf.CORE, pf.PAID_CORE, pf.UNPAID_CORE, pf.POINT_CHARGE)
    for role in roles:
        for ink in (role.fill, role.stroke):
            assert ink == "none" or re.fullmatch(r"#[0-9a-f]{6}", ink)
    assert pf.CORE.dash, "a core is dashed"
    assert pf.CONTAINER.fill == "none", "the container is an outline"
    assert pf.PARENT.fill != "none", "a parent is filled"
    assert set(pf.FAMILY_INKS) == {"point", "2-of-3", "2-of-5", "3-of-5"}
    assert len(set(pf.FAMILY_INKS.values())) == 4


def test_a_k_of_m_hull_carries_its_badge_and_sites() -> None:
    drawn = pf.hull([(0, 0), (10, 0), (5, 8), (5, 3), (2, 2)], 3, badge_at=(30, 30))
    root = ET.fromstring(f'<g xmlns="{pf.SVG_NS}">{drawn}</g>')
    hull = root.find(f"{SVG}polygon")
    assert hull is not None
    # The hull goes through the outer three points only.
    assert len(hull.attrib["points"].split()) == 3
    assert len(root.findall(f"{SVG}circle")) == 5
    assert [node.text for node in root.iter(f"{SVG}text")] == ["3/5"]


def test_convex_hull_is_counter_clockwise_and_drops_inner_points() -> None:
    hull = pf.convex_hull([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])
    assert hull == [(0, 0), (2, 0), (2, 2), (0, 2)]


@pytest.mark.parametrize(
    ("value", "places", "expected"),
    [
        (Fraction(1, 8), 2, "0.13"),
        (Fraction(-1, 8), 2, "-0.13"),
        (Fraction(999962528, 10**9), 9, "0.999962528"),
        (Fraction(764, 775), 6, "0.985806"),
        (Fraction(1, 3), 0, "0"),
    ],
)
def test_decimal_rounds_exactly(value: Fraction, places: int, expected: str) -> None:
    assert pf.decimal(value, places) == expected


def test_exact_decimal_refuses_a_repeating_expansion() -> None:
    assert pf.exact_decimal(Fraction(1374934993, 125000000)) == "10.999479944"
    with pytest.raises(ValueError, match="terminating"):
        pf.exact_decimal(Fraction(1, 3))


def test_powers_and_scientific_notation_are_exact() -> None:
    assert pf.power_of_ten(Fraction(1, 10**12)) == "10⁻¹²"
    assert pf.power_of_ten(Fraction(1000)) == "10³"
    with pytest.raises(ValueError, match="not a power of ten"):
        pf.power_of_ten(Fraction(2, 10**12))
    assert pf.scientific(Fraction(31, 7999999992)) == "3.9 \N{MULTIPLICATION SIGN} 10⁻⁹"
    assert pf.scientific(Fraction(9999, 10**8)) == "1.0 \N{MULTIPLICATION SIGN} 10⁻⁴"
    assert pf.percent(Fraction(79, 100)) == "79%"


@pytest.fixture(scope="module")
def ladder() -> ET.Element:
    return ET.fromstring(pf.bound_ladder("T-037"))


def test_the_ladder_has_every_rung_in_order_evenly_spaced(ladder: ET.Element) -> None:
    rungs = [node for node in ladder.iter(f"{SVG}circle") if "data-rung" in node.attrib]
    assert [node.attrib["data-rung"] for node in rungs] == [rung[0] for rung in pf.LADDER_RUNGS]
    heights = [float(node.attrib["cy"]) for node in rungs]
    gaps = {round(a - b, 6) for a, b in pairwise(heights)}
    assert len(gaps) == 1, "the ladder is not to scale: its rungs are evenly spaced"
    results = [
        node.attrib["data-result"] for node in ladder.iter() if "data-result" in node.attrib
    ]
    assert results == [identifier for rung in pf.LADDER_RUNGS for identifier in rung]


def test_the_ladders_values_are_the_registers_headlines(ladder: ET.Element) -> None:
    register = yaml.safe_load(pf.RESULTS.read_text(encoding="utf-8"))
    headlines = {row["id"]: row["headline"] for row in register["results"]}
    values = {
        node.attrib["data-value"]: node.text
        for node in ladder.iter()
        if "data-value" in node.attrib
    }
    for identifier in ("T-018", "T-025", "T-037"):
        assert f"= {values[identifier]}`" in headlines[identifier]
    for identifier in ("T-026", "T-033", "T-061"):
        stem = (values[identifier] or "").rstrip("…")
        assert f"= {stem}" in headlines[identifier]
    assert values["T-061"] != values["T-037"]
    # T-010's headline is a surd, T-060's names a packing: their values are computed.
    assert values["T-010"] == f"{math.floor((2 + 4 / math.sqrt(5)) * 10**7) / 10**7:.7f}…"
    assert values["T-060"] == "3.8770835…"


def test_the_ladder_highlights_one_rung(ladder: ET.Element) -> None:
    lit = [
        node.attrib["data-rung"]
        for node in ladder.iter(f"{SVG}circle")
        if node.attrib.get("fill") == pf.ACCENT
    ]
    assert lit == ["T-037"]
    other = ET.fromstring(pf.bound_ladder("T-060"))
    assert [
        node.attrib["data-rung"]
        for node in other.iter(f"{SVG}circle")
        if node.attrib.get("fill") == pf.ACCENT
    ] == ["T-060"]
    with pytest.raises(ValueError, match="not on the ladder"):
        pf.bound_ladder("T-001")


def test_a_changed_rung_record_is_refused(tmp_path: Path) -> None:
    text = pf.RESULTS.read_text(encoding="utf-8")
    changed = text.replace("`s(11) ≥ 381/100 = 3.81`", "`s(11) ≥ 382/100 = 3.82`", 1)
    assert changed != text
    path = tmp_path / "results.yaml"
    path.write_text(changed, encoding="utf-8")
    with pytest.raises(ValueError, match="changed figure input"):
        pf.bound_ladder("T-037", path=path)


def test_a_changed_ladder_pin_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pf, "LADDER_DIGEST", "0" * 64)
    with pytest.raises(ValueError, match="changed figure input"):
        pf.bound_ladder("T-037")
