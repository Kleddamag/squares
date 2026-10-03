"""The T-060 overview diagrams explain only accepted, source-bound premises."""

from __future__ import annotations

import gzip
import hashlib
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any
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
    facts = figures.caption_facts()
    assert set(facts) == {
        "LOCAL_BRANCHES",
        "LOCAL_MARGINS",
        "LOCAL_RADII_TABLE",
        "ROLE_MAP_TABLE",
        "COVER_SITES_TABLE",
    }
    assert {key: facts[key] for key in ("LOCAL_BRANCHES", "LOCAL_MARGINS")} == {
        "LOCAL_BRANCHES": f"{accepted['required_branches']:,}",
        "LOCAL_MARGINS": f"{accepted['signed_coordinate_margins_checked']:,}",
    }
    assert facts["LOCAL_BRANCHES"] == "128"
    assert facts["LOCAL_MARGINS"] == "8,448"

    endpoint = " ".join(roots["ENDPOINT_SVG"].itertext())
    assert "same packing" in endpoint
    assert "No physical shrinking" in endpoint
    assert "Fixed-T local theorem" in endpoint
    assert "T > S: contradiction" in endpoint


LOCAL_RADII_TABLE = """\
| Label | $r_x$ | $r_y$ | $r_\\theta$ |
| --- | --- | --- | --- |
| 0 | $18767167/10000000000$ | $4435327/2000000000$ | $5670363/2500000000$ |
| 1 | $1636033/1000000000$ | $6880181/5000000000$ | $1764113/1000000000$ |
| 2 | $8962451/10000000000$ | $5212397/5000000000$ | $5670363/2500000000$ |
| 3 | $1635053/1000000000$ | $10683139/10000000000$ | $1890121/1250000000$ |
| 4 | $4087019/2500000000$ | $13962901/10000000000$ | $20161291/10000000000$ |
| 5 | $12900283/10000000000$ | $534153/500000000$ | $1890121/1250000000$ |
| 6 | $678279/500000000$ | $4124329/5000000000$ | $35312013/10000000000$ |
| 7 | $11182451/10000000000$ | $3232837/5000000000$ | $8824483/2500000000$ |
| 8 | $9356857/10000000000$ | $8671199/10000000000$ | $7549783/5000000000$ |
| 9 | $293551/400000000$ | $10335557/10000000000$ | $40352153/10000000000$ |
| 10 | $1920157/2500000000$ | $8222903/2500000000$ | $67647473/10000000000$ |"""

ROLE_MAP_TABLE = """\
| Local label | Square | Capture owner cell |
| --- | --- | --- |
| 0 | $A(0,0)$ | 3 |
| 1 | $A(T-1,0)$ | 15 |
| 2 | $A(x_0,T-1)$ | 8 |
| 3 | $A(0,T-1)$ | 0 |
| 4 | $A(1,T-1)$ | 4 |
| 5 | $A(0,T-2)$ | 1 |
| 6 | $F(A(0,0))$ | 2 |
| 7 | $F(A(\\eta,-1))$ | 11 |
| 8 | $F(A(1,v))$ | 9 |
| 9 | $F(A(\\eta+1,v-1))$ | 10 |
| 10 | $F(A(\\eta+2,-\\zeta))$ | 13 |"""

COVER_SITES_TABLE = """\
| Site | First coordinate | Second coordinate | Reflected site |
| --- | --- | --- | --- |
| 0 | 209982 | 265837 | 15 |
| 1 | 746404 | 91006 | 14 |
| 2 | 1267243 | 277512 | 13 |
| 3 | 1731123 | 205608 | 12 |
| 4 | 206181 | 800758 | 11 |
| 5 | 742311 | 625866 | 10 |
| 6 | 1270514 | 832045 | 9 |
| 7 | 1781756 | 671052 | 8 |"""


def test_the_exact_tables_print_the_retained_interface() -> None:
    """The paper's three tables are the retained objects' values, row for row: the 33
    radii the local and pose-inclusion receipts both name, the local-to-owner map the
    role guard, the pose result and the focused rectangle all state, and the cover's
    first eight sites, whose half-turn images are the other eight exactly."""
    facts = figures.caption_facts()
    assert facts["LOCAL_RADII_TABLE"] == LOCAL_RADII_TABLE
    assert facts["ROLE_MAP_TABLE"] == ROLE_MAP_TABLE
    assert facts["COVER_SITES_TABLE"] == COVER_SITES_TABLE
    for table in (LOCAL_RADII_TABLE, ROLE_MAP_TABLE, COVER_SITES_TABLE):
        lines = table.splitlines()
        assert all(line.startswith("| ") and line.endswith(" |") for line in lines)
        assert lines[1] == "| " + " | ".join("---" for _ in lines[0].split(" | ")) + " |"
        assert not [line for line in lines if line != line.rstrip()]
    # Labels 9 and 10, capture owners 10 and 13, are the two with the wider angular
    # radius: coordinates 29 and 32.
    rows = ROLE_MAP_TABLE.splitlines()[2:]
    assert [row.split(" | ")[2].rstrip(" |") for row in rows[9:]] == ["10", "13"]


def test_the_tables_are_bound_to_the_accepted_receipts_hashes() -> None:
    """Each table's object is the one an accepted receipt names, at the hash the final
    composition accepted that receipt at."""
    composition = json.loads(figures.COMPOSITION.read_text(encoding="utf-8"))
    accepted = composition["reviewed_receipt_sha256s"]
    local = json.loads(figures.LOCAL.read_bytes())
    pose = json.loads(figures.POSE.read_bytes())
    d4 = json.loads(figures.D4.read_bytes())
    for path, receipt in ((figures.LOCAL, "local-isolation"), (figures.POSE, "pose-inclusion")):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == accepted[receipt]
    assert hashlib.sha256(figures.D4.read_bytes()).hexdigest() == accepted["d4-independent"]
    assert local["input_sha256"]["focused"] == figures.FOCUSED_SHA == pose["focused_sha256"]
    assert pose["accepted_local_result_sha256"] == accepted["local-isolation"]
    assert d4["input_sha256"]["cover"] == figures.COVER_SHA
    assert hashlib.sha256(figures.GUARDS.read_bytes()).hexdigest() == pose["guard_sha256"]
    for path, sha in (
        (figures.FOCUSED, figures.FOCUSED_SHA),
        (figures.COVER, figures.COVER_SHA),
    ):
        assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == sha
    assert (
        hashlib.sha256(figures.WITNESS_SOURCE.read_bytes()).hexdigest()
        == local["source_hashes"]["cases/trump11/packing.py"]
    )


def _regzipped(path: Path, destination: Path, change: Callable[[dict[str, Any]], None]) -> Path:
    record = json.loads(gzip.decompress(path.read_bytes()))
    change(record)
    destination.write_bytes(gzip.compress(json.dumps(record).encode()))
    return destination


def test_a_changed_table_object_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def widen(record: dict[str, Any]) -> None:
        record["radii"][29] = "1/128"

    def move(record: dict[str, Any]) -> None:
        record["cells"][15]["center"][0] = "1/2"

    focused = _regzipped(figures.FOCUSED, tmp_path / "focused.json.gz", widen)
    monkeypatch.setattr(figures, "FOCUSED", focused)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.caption_facts()
    monkeypatch.undo()
    cover = _regzipped(figures.COVER, tmp_path / "cover.json.gz", move)
    monkeypatch.setattr(figures, "COVER", cover)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.caption_facts()
    monkeypatch.undo()
    guards = json.loads(figures.GUARDS.read_bytes())
    guards["guards"][0]["label_to_cell"][9] = 13
    path = tmp_path / "guard.json"
    path.write_text(json.dumps(guards), encoding="utf-8")
    monkeypatch.setattr(figures, "GUARDS", path)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.caption_facts()


@pytest.mark.parametrize("name", ["FOCUSED_SHA", "COVER_SHA"])
def test_a_table_input_no_accepted_receipt_names_is_refused(
    monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.setattr(figures, name, "0" * 64)
    with pytest.raises(ValueError, match="names a different table input"):
        figures.caption_facts()


def test_a_changed_construction_source_refuses_the_role_map(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The squares are named in the order the hashed construction builds them."""
    source = tmp_path / "packing.py"
    source.write_text(
        figures.WITNESS_SOURCE.read_text(encoding="utf-8") + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(figures, "WITNESS_SOURCE", source)
    with pytest.raises(ValueError, match="retained receipt changed"):
        figures.caption_facts()


def test_the_tables_own_checks_refuse_inconsistent_interfaces() -> None:
    """Past the hashes, each table checks the property it prints."""
    cover = json.loads(gzip.decompress(figures.COVER.read_bytes()))
    cover["cells"][15]["center"] = ["1/2", "1/2"]
    with pytest.raises(ValueError, match="cover site 15 is not site 0 reflected"):
        figures.cover_sites_table(cover)
    focused = json.loads(gzip.decompress(figures.FOCUSED.read_bytes()))
    guards = json.loads(figures.GUARDS.read_bytes())
    pose = json.loads(figures.POSE.read_bytes())
    assert figures.capture_owners(focused, guards, pose) == [
        3,
        15,
        8,
        0,
        4,
        1,
        2,
        11,
        9,
        10,
        13,
    ]
    pose["owners"][9]["owner"] = 13
    with pytest.raises(ValueError, match="local-to-owner map changed"):
        figures.capture_owners(focused, guards, pose)
    focused["inclusion"][9]["radii"][2] = "1/128"
    with pytest.raises(ValueError, match="focused local rectangle changed"):
        figures.local_radii_table(focused)
    assert (
        figures.markdown_table(("a", "b"), [("1", "2")])
        == "| a | b |\n| --- | --- |\n| 1 | 2 |"
    )
    with pytest.raises(ValueError, match="wrong number of cells"):
        figures.markdown_table(("a", "b"), [("1",)])


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
