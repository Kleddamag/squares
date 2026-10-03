"""Controls for the n=11 D4 incidence-propagation bridge (review S3)."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from cases.trump11.packing import build
from devtools import check_n11_optimality_d4 as d4
from devtools import check_n11_optimality_d4_incidence as incidence

F = Fraction


class Geometry(NamedTuple):
    sites: list[tuple[F, F]]
    canonical: list[tuple[int, ...]]
    labels: list[tuple[int, ...]]
    vertices: list[d4.Polygon]


@pytest.fixture(scope="module")
def geometry() -> Geometry:
    cover = incidence.load_object(incidence.OBJECTS, "cover")
    overlay = incidence.load_object(incidence.OBJECTS, "overlay")
    cells, canonical = d4.check_cover(cover)
    labels, vertices, _, _ = d4.check_overlay(cells, overlay)
    sites = [(F(row["center"][0]), F(row["center"][1])) for row in cover["cells"]]
    return Geometry(sites, canonical, labels, vertices)


@pytest.fixture(scope="module")
def result() -> dict[str, Any]:
    return incidence.verify(incidence.OBJECTS, max_seconds=45)


def test_published_objects_pass_with_the_review_census(result: dict[str, Any]) -> None:
    assert result["status"] == incidence.PASS
    assert result["global_optimality_proved"] is False
    assert "2175 and 2176" in result["scope"]
    counts = {
        entry["source_canonical_index"]: (
            entry["immediate_contradictions"],
            entry["propagation_contradictions"],
            entry["surviving_triples"],
        )
        for entry in result["sources"]
    }
    assert counts == incidence.REVIEW_COUNTS
    survivors = {
        entry["source_canonical_index"]: entry["survivor_other_view_masks"]
        for entry in result["sources"]
    }
    assert survivors == {
        999: [["J1462", "J1462", "J999"]],
        1462: [["J999", "HJ999", "HJ1462"]],
        1659: [],
    }
    reduction = result["reflection_reduction_1462"]
    assert reduction["reflected_view_mask_names"] == ["J999", "J1462", "J1462", "J999"]
    assert reduction["regions_carried_by_g1"] == 220


def test_allowing_case_438_leaves_survivors(geometry: Geometry) -> None:
    cases = (incidence.TARGET, *incidence.SOURCES)
    names = incidence.mask_names(geometry.canonical, cases)
    censuses = incidence.run_census(
        geometry.labels, geometry.canonical, cases, sorted(names), float("inf")
    )
    assert all(entry.counts["survivor"] > 0 for entry in censuses.values())
    found = [incidence.named(triple, names) for triple, _ in censuses[438].survivors]
    assert list(incidence.CONSTRUCTION_PATTERN[1]) in found


def construction_rows(geometry: Geometry) -> dict[str, list[tuple[int, ...]]]:
    """Exact closed-cell labels of the construction's centers under all eight of D4."""
    squares, _, field = build()
    k = field.rational
    one, half, scale = k(1), k(F(1, 2)), k(d4.U - 1)
    centers = []
    for corners in squares:
        x = sum((corner[0] for corner in corners[1:]), corners[0][0]) / k(4)
        y = sum((corner[1] for corner in corners[1:]), corners[0][1]) / k(4)
        centers.append(((x - half) / scale, (y - half) / scale))

    def cell(point: tuple[Any, Any]) -> int:
        fx, fy = float(point[0]), float(point[1])
        sites = geometry.sites
        best = min(range(16), key=lambda i: (fx - sites[i][0]) ** 2 + (fy - sites[i][1]) ** 2)
        for other, site in enumerate(sites):
            a, b = 2 * (site[0] - sites[best][0]), 2 * (site[1] - sites[best][1])
            c = site[0] ** 2 + site[1] ** 2 - sites[best][0] ** 2 - sites[best][1] ** 2
            assert other == best or (point[0] * k(a) + point[1] * k(b) - k(c)).sign() <= 0
        return best

    views: list[Callable[[Any, Any], tuple[Any, Any]]] = [
        lambda x, y: (x, y),
        lambda x, y: (one - x, y),
        lambda x, y: (one - y, x),
        lambda x, y: (y, x),
    ]
    frames = {f"g{index}": view for index, view in enumerate(views)}
    frames |= {f"Hg{index}": view for index, view in enumerate(views)}
    rows: dict[str, list[tuple[int, ...]]] = {}
    for name, frame in frames.items():
        moved = [frame(*center) for center in centers]
        if name.startswith("H"):
            moved = [(one - x, one - y) for x, y in moved]
        rows[name] = [tuple(cell(view(*point)) for view in views) for point in moved]
    return rows


def test_construction_assignment_survives_propagation_in_every_frame(
    geometry: Geometry,
) -> None:
    names = incidence.mask_names(geometry.canonical, (438, 999, 1462, 1659))
    for frame, rows in construction_rows(geometry).items():
        masks = [tuple(sorted({row[view] for row in rows})) for view in range(4)]
        assert all(len(mask) == 11 and mask in names for mask in masks), frame
        found = incidence.propagate(geometry.labels, masks)
        assert found.status == "survivor", frame
        for row in rows:
            assert geometry.labels.index(row) in found.domains[row[0]], (frame, row)
        if frame == "g2":
            source, others = incidence.CONSTRUCTION_PATTERN
            assert incidence.named(masks, names) == [source, *others]


def test_forced_regions_lie_in_the_stated_boxes(geometry: Geometry) -> None:
    for region, stated in incidence.FORCED_BOXES.items():
        box = incidence.bounding_box(geometry.vertices[geometry.labels.index(region)])
        assert incidence.box_inside(box, stated)
    left = geometry.vertices[geometry.labels.index((1, 1, 11, 4))]
    assert incidence.bounding_box(left)[1][0] == 0
    tight = dict(incidence.FORCED_BOXES)
    tight[2, 5, 6, 9] = ((F(11, 25), F(1, 2)), (F(23, 100), F(7, 25)))
    survivor = survivor_outcome(geometry, 999)
    with pytest.raises(ValueError, match="leaves its stated box"):
        incidence.close_forced_pair(geometry.labels, geometry.vertices, survivor, tight)


def survivor_outcome(geometry: Geometry, source: int) -> incidence.Outcome:
    names = incidence.mask_names(geometry.canonical, incidence.SOURCES)
    triple = [
        mask
        for name in incidence.REVIEW_SURVIVORS[source][0]
        for mask, label in names.items()
        if label == name
    ]
    return incidence.propagate(geometry.labels, (geometry.canonical[source], *triple))


def test_distance_inequality_is_exact_and_strict(geometry: Geometry) -> None:
    scale = d4.U - 1
    review = F(1, 10) ** 2 + F(7, 25) ** 2
    assert scale < 3
    assert 9 * review == F(1989, 2500)
    assert scale**2 * review < F(1989, 2500) < 1
    survivor = survivor_outcome(geometry, 999)
    closure = incidence.close_forced_pair(
        geometry.labels, geometry.vertices, survivor, incidence.FORCED_BOXES
    )
    assert [row["owner"] for row in closure["forced_regions"]] == [1, 2]
    exact = F(closure["exact_vertex_max_squared_physical_distance"])
    assert exact < scale**2 * review
    corner = next(row for row in geometry.labels if row[0] == 15)
    far = dict(survivor.domains)
    far[2] = frozenset({geometry.labels.index(corner)})
    moved = survivor._replace(domains=far)
    boxes: dict[tuple[int, ...], incidence.Box] = {
        (1, 1, 11, 4): incidence.FORCED_BOXES[1, 1, 11, 4]
    }
    boxes[corner] = ((F(0), F(1)), (F(0), F(1)))
    with pytest.raises(ValueError, match="exceed review"):
        incidence.close_forced_pair(geometry.labels, geometry.vertices, moved, boxes)


def test_rules_reserve_force_and_contradict() -> None:
    masks = ((0, 1), (0, 1), (0, 1), (0, 1))
    labels = [(0, 0, 0, 0), (0, 1, 1, 1), (1, 1, 1, 1), (1, 1, 0, 0)]
    forced = incidence.propagate(labels, masks)
    assert forced.status == "survivor"
    assert forced.domains == {0: {0}, 1: {2}}
    uncarried = incidence.propagate([(0, 0, 0, 0), (1, 0, 0, 0)], masks)
    assert (uncarried.status, uncarried.operations) == ("immediate", 0)
    emptied = incidence.propagate([(0, 0, 0, 0), (1, 0, 1, 1), (1, 1, 0, 0)], masks)
    assert emptied.status == "propagation"


def copy_objects(target: Path) -> Path:
    target.mkdir()
    for pin in incidence.PINS.values():
        name = f"{pin.decoded_sha256}.gz"
        shutil.copyfile(incidence.OBJECTS / name, target / name)
    return target


def test_refuses_a_changed_input(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    objects = copy_objects(tmp_path / "objects")
    cover = objects / f"{incidence.PINS['cover'].decoded_sha256}.gz"
    decoded = json.loads(gzip.decompress(cover.read_bytes()))
    decoded["cells"][0]["center"][0] = "1/10"
    cover.write_bytes(gzip.compress(json.dumps(decoded).encode()))
    output = tmp_path / "result.json"
    assert incidence.main(["--objects", str(objects), "--output", str(output)]) == 1
    refused = json.loads(output.read_text())
    assert refused["status"] == incidence.REFUSED
    assert "cover stored object hash mismatch" in refused["reason"]
    stored = hashlib.sha256(cover.read_bytes()).hexdigest()
    pin = incidence.PINS["cover"]._replace(stored_sha256=stored)
    monkeypatch.setitem(incidence.PINS, "cover", pin)
    with pytest.raises(ValueError, match="cover source hash mismatch"):
        incidence.verify(objects, max_seconds=45)
