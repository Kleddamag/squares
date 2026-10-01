"""The T-060 illustrations stay bound to retained geometric and graph inputs."""

from __future__ import annotations

import json
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from devtools import n11_optimality_figures as figures

SVG = "{http://www.w3.org/2000/svg}"
CASE_438 = {0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15}


def description(root: ET.Element) -> str:
    value = root.find(f"{SVG}desc")
    assert value is not None
    assert value.text is not None
    return value.text


def test_geometric_illustrations_are_self_contained_and_source_bound() -> None:
    rendered = figures.render_figures()
    assert set(rendered) == {
        "WITNESS_SVG",
        "COVER_SVG",
        "CAPTURE_SVG",
        "MASK_SVG",
        "CAPACITY_SVG",
    }
    roots = {name: ET.fromstring(svg) for name, svg in rendered.items()}
    assert all(root.tag == f"{SVG}svg" for root in roots.values())
    assert all(root.find(f"{SVG}title") is not None for root in roots.values())
    assert all(root.find(f"{SVG}desc") is not None for root in roots.values())
    assert all(root.find(f".//{SVG}script") is None for root in roots.values())
    assert all(root.find(f".//{SVG}image") is None for root in roots.values())
    ids = [
        node.attrib["id"]
        for root in roots.values()
        for node in root.iter()
        if "id" in node.attrib
    ]
    assert len(ids) == len(set(ids))
    for root in roots.values():
        labelled = root.attrib["aria-labelledby"].split()
        assert all(label in ids for label in labelled)

    witness = roots["WITNESS_SVG"]
    assert len(witness.findall(f'.//{SVG}polygon[@data-feature="square-outline"]')) == 11
    assert len(witness.findall(f'.//{SVG}rect[@data-feature="container-outline"]')) == 1
    assert "exact Trump construction" in description(witness)

    cover = roots["COVER_SVG"]
    mask = roots["MASK_SVG"]
    for root in (cover, mask):
        cells = root.findall(f".//{SVG}polygon[@data-cell]")
        assert [int(cell.attrib["data-cell"]) for cell in cells] == list(range(16))
        assert {
            int(cell.attrib["data-cell"])
            for cell in cells
            if cell.attrib["data-selected"] == "true"
        } == CASE_438
    assert "not an owned-hull diagram" in description(mask)

    capture = roots["CAPTURE_SVG"]
    assert len(capture.findall(f".//{SVG}rect")) == 10
    assert len(capture.findall(f".//{SVG}line")) == 9
    labels = set(capture.itertext())
    assert {"far15", "far13", "far2", "near"} <= labels
    assert "local enclosure" in labels
    assert "dependency diagram" in description(capture)


def test_changed_d4_receipt_refuses_to_supply_illustrated_cells(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    altered = json.loads(figures.D4_RECEIPT.read_text(encoding="utf-8"))
    altered["input_sha256"]["cover"] = "0" * 64
    path = tmp_path / "d4-result.json"
    path.write_text(json.dumps(altered), encoding="utf-8")
    monkeypatch.setattr(figures, "D4_RECEIPT", path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.render_figures()


def test_capture_drawing_refuses_an_unknown_parent_hash() -> None:
    graph = json.loads(figures.SOURCE_GRAPH.read_text(encoding="utf-8"))
    child = "research/candidate-capture/tree438-rebuilt/r1.json"
    graph["source_parent_edges"][child] = "0" * 64
    with pytest.raises(ValueError, match="unknown parent hash"):
        figures._capture_svg(graph)  # noqa: SLF001 - malformed graph boundary  # pyright: ignore[reportPrivateUsage]


def test_capture_label_refuses_a_lost_inherited_boundary() -> None:
    graph = json.loads(figures.SOURCE_GRAPH.read_text(encoding="utf-8"))
    graph["source_headers"]["research/candidate-capture/tree438-rebuilt/r10.json"][
        "constraints"
    ][0]["keep"] = "le"
    with pytest.raises(ValueError, match="inherited conditions"):
        figures._capture_svg(graph)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def test_closed_cut_labels_and_capacity_use_exact_inputs() -> None:
    from fractions import Fraction  # noqa: PLC0415

    rendered = figures.render_figures()
    capture = ET.fromstring(rendered["CAPTURE_SVG"])
    assert {
        node.attrib["data-closed-cut"]
        for node in capture.findall(f".//{SVG}text[@data-closed-cut]")
    } == {
        "y₁₅ ≤ 5/4",
        "y₁₅ ≥ 5/4",
        "t₁₃ ≤ 147/512",
        "t₁₃ ≥ 147/512",
        "t₂ ≤ 183/512",
        "t₂ ≥ 183/512",
    }
    capacity = ET.fromstring(rendered["CAPACITY_SVG"])
    cell = capacity.find(f".//{SVG}polygon[@data-capacity-cell]")
    assert cell is not None
    assert 0 < Fraction(cell.attrib["data-diameter-squared"]) < 1
    assert "U Trump" not in rendered["WITNESS_SVG"]
