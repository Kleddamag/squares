"""Focused source and semantics controls for the T-060 mechanism illustrations."""

from __future__ import annotations

import re
from fractions import Fraction
from xml.etree import ElementTree as ET

import pytest

from devtools import n11_optimality_mechanism_figures as figures


def test_rendered_figures_are_standalone_accessible_svg() -> None:
    rendered = figures.render_mechanism_figures()
    assert set(rendered) == {"POSE_SVG", "ROW_SVG", "CHARGE_SVG", "SYMMETRY_SVG"}
    identifiers: list[str] = []
    for content in rendered.values():
        root = ET.fromstring(content)
        assert root.tag == f"{{{figures.SVG_NS}}}svg"
        assert root.attrib["role"] == "img"
        labelled_by = root.attrib["aria-labelledby"].split()
        assert len(labelled_by) == 2
        local_ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
        assert set(labelled_by) <= set(local_ids)
        identifiers.extend(local_ids)
        assert not re.search(r"<\s*(script|image|foreignObject)\b", content, re.IGNORECASE)
        assert not re.search(r"\b(?:href|onload|onclick)\s*=", content, re.IGNORECASE)
    assert len(identifiers) == len(set(identifiers))


def test_worked_row_and_charge_retain_accepted_scope() -> None:
    rendered = figures.render_mechanism_figures()
    row = rendered["ROW_SVG"]
    assert 'data-row-domain="2095-1-10-17"' in row
    assert set(re.findall(r'data-obstacle-owner="(\d+)"', row)) == {"6", "11", "14"}
    assert 'data-core-vertices="8"' in row
    assert 'data-residual-vertices="3"' in row
    assert "32-row update" in row
    assert "Field-scaled coordinates" in row
    charge = rendered["CHARGE_SVG"]
    assert "Required owners O = {0,1,2,3,6}" in charge
    assert "Mask J = {0,…,10}; O ⊆ J" in charge
    assert "Charged cells P ∩ J = {1,2}" in charge
    assert "q₁ + q₂ = 2 &gt; 1 = b" in charge
    assert "all-direction" in charge
    assert "one-direction capacity only" in charge


def test_d4_views_use_fixed_cells_and_one_strict_pair() -> None:
    symmetry = figures.render_mechanism_figures()["SYMMETRY_SVG"]
    root = ET.fromstring(symmetry)
    points = [node for node in root.iter() if "data-view-point" in node.attrib]
    assert [node.attrib["data-view-point"] for node in points] == ["0", "1", "2", "3"]
    assert all(
        len([node for node in root.iter() if node.attrib.get("data-view") == str(i)]) == 16
        for i in range(4)
    )
    assert "view 1: cell 0" in symmetry
    assert "view 2: cell 7" in symmetry
    assert "view 3: cell 3" in symmetry
    assert "view 4: cell 5" in symmetry
    assert "regions 9 and 12" in symmetry
    assert "220 closed regions and 1,572 bans" in symmetry


def test_changed_accepted_result_refuses_before_drawing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(figures, "GENERIC_RESULT_SHA", "0" * 64)
    with pytest.raises(ValueError, match="changed figure input"):
        figures.render_mechanism_figures()


def test_closed_contact_cannot_be_omitted() -> None:
    point = ((Fraction(0), Fraction(0)),)
    segment = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)))
    assert figures.complete_obstacles_for_display({1: ()}) == {}
    with pytest.raises(ValueError, match="lower-dimensional obstacle contact"):
        figures.complete_obstacles_for_display({1: point})
    with pytest.raises(ValueError, match="lower-dimensional obstacle contact"):
        figures.complete_obstacles_for_display({1: segment})
