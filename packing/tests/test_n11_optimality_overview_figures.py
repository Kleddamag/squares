"""The T-060 overview diagrams explain only accepted, source-bound premises."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from devtools import n11_optimality_overview_figures as figures

SVG = "{http://www.w3.org/2000/svg}"


def test_overview_figures_are_complete_static_svg_with_distinct_roles() -> None:
    rendered = figures.render_overview_figures()
    assert set(rendered) == {"ROADMAP_SVG", "LOCAL_SVG", "ENDPOINT_SVG"}
    roots = {name: ET.fromstring(svg) for name, svg in rendered.items()}
    ids = [
        node.attrib["id"]
        for root in roots.values()
        for node in root.iter()
        if "id" in node.attrib
    ]
    assert len(ids) == len(set(ids))
    for root in roots.values():
        assert root.tag == f"{SVG}svg"
        assert root.find(f"{SVG}title") is not None
        assert root.find(f"{SVG}desc") is not None
        assert root.find(f".//{SVG}script") is None
        assert root.find(f".//{SVG}image") is None
        assert root.find(f".//{SVG}foreignObject") is None
        assert set(root.attrib["aria-labelledby"].split()) <= set(ids)
        assert root.findall(f'.//{SVG}text[@class="n11-diagram-label"]')
        assert root.findall(f'.//{SVG}text[@class="n11-diagram-note"]')

    roadmap = " ".join(roots["ROADMAP_SVG"].itertext())
    assert "2,184 case classes" in roadmap
    assert "2,180 excluded" in roadmap
    assert "fixed-T rectangle" in roadmap
    assert "No packing has S < T" in roadmap
    # A diagram's title is its figure's caption, not a line of the drawing.
    assert "Two routes to the exact optimum" not in roadmap.replace(
        "Two routes to the exact eleven-square optimum", ""
    )

    local = roots["LOCAL_SVG"]
    curve = local.find(f".//{SVG}polyline[@data-accepted-ratio]")
    assert curve is not None
    accepted = json.loads(figures.LOCAL.read_text(encoding="utf-8"))
    ratio = Fraction(accepted["worst_dual_ratio"])
    assert curve.attrib["data-accepted-ratio"] == str(ratio)
    assert ratio < 1
    # The local diagram is the two curves and their labels; its census is the caption's,
    # from the receipt the curve is drawn from.
    assert {node.text for node in local.iter(f"{SVG}text")} == {"τ", "cτ²", "0", "1"}
    assert figures.caption_facts() == {
        "LOCAL_BRANCHES": f"{accepted['required_branches']:,}",
        "LOCAL_MARGINS": f"{accepted['signed_coordinate_margins_checked']:,}",
    }
    assert figures.caption_facts() == {"LOCAL_BRANCHES": "128", "LOCAL_MARGINS": "8,448"}

    endpoint = " ".join(roots["ENDPOINT_SVG"].itertext())
    assert "same packing" in endpoint
    assert "No physical shrinking" in endpoint
    assert "Fixed-T local theorem" in endpoint
    assert "T > S: contradiction" in endpoint


def test_a_changed_receipt_refuses_the_captions_facts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A caption's count comes from the receipt and is refused with the figure."""
    path = _altered(figures.LOCAL, tmp_path / "local.json", "required_branches", 127)
    monkeypatch.setattr(figures, "LOCAL", path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.caption_facts()


def _altered(path: Path, destination: Path, field: str, value: object) -> Path:
    record = json.loads(path.read_text(encoding="utf-8"))
    record[field] = value
    destination.write_text(json.dumps(record), encoding="utf-8")
    return destination


def test_changed_composition_refuses_a_global_roadmap(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = _altered(
        figures.COMPOSITION, tmp_path / "composition.json", "accepted_exclusions", 2179
    )
    monkeypatch.setattr(figures, "COMPOSITION", path)
    with pytest.raises(ValueError, match="accepted final composition changed"):
        figures.render_overview_figures()


def test_non_strict_local_margin_refuses_the_curve(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = _altered(figures.LOCAL, tmp_path / "local.json", "worst_dual_ratio", "1/1")
    monkeypatch.setattr(figures, "LOCAL", path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.render_overview_figures()


def test_changed_field_frame_refuses_the_endpoint(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    record = json.loads(figures.POSE.read_text(encoding="utf-8"))
    record["source_frame"]["B"] = "1/2"
    path = tmp_path / "pose.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    monkeypatch.setattr(figures, "POSE", path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.render_overview_figures()


@pytest.mark.parametrize(
    ("source", "field", "value"),
    [
        ("D4", "wall_seconds", 999),
        ("EXCLUSIONS", "geometry_rerun", True),
        ("LOCAL", "wall_seconds", 999),
        ("POSE", "wall_seconds", 999),
    ],
)
def test_unpictured_source_change_refuses_a_figure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    source: str,
    field: str,
    value: object,
) -> None:
    path = _altered(getattr(figures, source), tmp_path / f"{source}.json", field, value)
    monkeypatch.setattr(figures, source, path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.render_overview_figures()
