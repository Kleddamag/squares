"""Bounded refusal and exact ancestry controls for the first fresh-wall generic proof."""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import copy
import json
import shutil
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_generic_sequential as sequential


def _source() -> dict[str, Any]:
    return generic._load_pin(
        generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz", generic.SOURCE_PIN
    )


def test_initial_state_requires_exact_owner_inventory() -> None:
    source = _source()
    groups = {
        owner: generic.hull(generic.points(source["initial"]["groups"][str(owner)]))
        for owner in generic.MASK
    }
    rows = {
        owner: [
            {"reference": reference}
            for reference in source["initial"]["cell_references"][str(owner)]
        ]
        for owner in generic.MASK
    }
    generic._source_header(source, groups, rows)
    changed = copy.deepcopy(source)
    changed["initial"]["cell_references"]["unused"] = []
    with pytest.raises(ValueError, match="inventory"):
        generic._source_header(changed, groups, rows)


def test_compression_witness_must_be_an_exact_convex_combination() -> None:
    prior = [(Q(0), Q(0)), (Q(2), Q(0)), (Q(0), Q(2))]
    step = {
        "compression_source_hull": generic._encoded(prior),
        "inner_grid_compression": {
            "vertices": [["1", "0"]],
            "witnesses": [{"point": ["1", "0"], "indices": [0, 1], "weights": ["1/2", "1/2"]}],
            "denominator": 1,
            "original_vertices": 3,
            "retained_vertices": 1,
        },
    }
    assert generic._compressed(step, prior, []) == generic.hull(prior)
    step["inner_grid_compression"]["witnesses"][0]["weights"] = ["1", "1"]
    with pytest.raises(ValueError, match="convex-combination"):
        generic._compressed(step, prior, [])


def test_strict_core_rejects_boundary_touch() -> None:
    core = [(Q(0), Q(0)), (generic.geometry.B / 2, Q(0)), (Q(0), generic.geometry.B / 4)]
    with pytest.raises(ValueError, match="strict containment"):
        generic._strict_core(core, Q(0), Q(1, 32))


@pytest.fixture(scope="module")
def proposed_state() -> tuple[
    dict[str, Any],
    dict[int, generic.Polygon],
    dict[int, list[dict[str, Any]]],
    list[generic.Polygon],
]:
    source = _source()
    seed = generic._load_pin(generic.OBJECTS / f"{generic.SEED_PIN[0]}.gz", generic.SEED_PIN)
    # These are inputs to refusal predicates, not independently accepted state.
    # The full golden replay below checks seed ownership and every transition.
    groups = {
        owner: generic.hull(generic.points(seed["groups"][str(owner)]))
        for owner in generic.MASK
    }
    rows = {owner: seed["cells"][str(owner)] for owner in generic.MASK}
    world = [generic.points(polygon) for polygon in seed["world"]]
    return source, groups, rows, world


def test_removing_a_needed_residual_does_not_cover_domain(
    proposed_state: tuple[
        dict[str, Any],
        dict[int, generic.Polygon],
        dict[int, list[dict[str, Any]]],
        list[generic.Polygon],
    ],
) -> None:
    source, groups, rows, world = proposed_state
    changed = copy.deepcopy(source)
    changed["steps"][0]["rows"][0]["residual_polygons"] = []
    with pytest.raises(ValueError, match=r"cover|uncovered"):
        generic._check_row(
            changed,
            changed["steps"][0],
            changed["steps"][0]["rows"][0],
            0,
            6,
            prior=groups,
            predecessor=rows[6][0],
            world=world,
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
        )


def test_sequential_step_rejects_changed_predecessor(
    proposed_state: tuple[
        dict[str, Any],
        dict[int, generic.Polygon],
        dict[int, list[dict[str, Any]]],
        list[generic.Polygon],
    ],
) -> None:
    source, groups, rows, world = proposed_state
    changed = copy.deepcopy(source)
    changed["steps"][0]["prior_owned_hulls"]["1"] = [["0", "0"]]
    audit = generic._load_pin(generic.OBJECTS / f"{generic.AUDIT_PIN[0]}.gz", generic.AUDIT_PIN)
    a1 = generic._load_pin(generic.A1_OBJECT, generic.A1_PIN)
    with pytest.raises(ValueError, match="predecessor"):
        generic._full(
            changed,
            audit,
            a1,
            groups,
            rows,
            world=world,
            result={},
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
            workers=1,
        )


def test_tampered_source_refuses_without_exclusion(tmp_path: Path) -> None:
    objects = tmp_path / "objects"
    objects.mkdir()
    for pin in (generic.SOURCE_PIN, generic.SEED_PIN, generic.AUDIT_PIN):
        shutil.copyfile(generic.OBJECTS / f"{pin[0]}.gz", objects / f"{pin[0]}.gz")
    source_path = objects / f"{generic.SOURCE_PIN[0]}.gz"
    with source_path.open("ab") as stream:
        stream.write(b"x")
    result = generic.run(
        argparse.Namespace(
            objects=objects,
            scope="full",
            max_seconds=30,
            max_events=50_000,
            workers=1,
            out=tmp_path / "result.json",
        )
    )
    assert result["status"] == "REFUSED"
    assert result["excluded_case_ids"] == []
    assert result["geometry_verified"] is False
    assert json.loads((tmp_path / "result.json").read_text())["status"] == "REFUSED"


def test_expired_full_run_cannot_exclude_a_case(tmp_path: Path) -> None:
    result = generic.run(
        argparse.Namespace(
            objects=generic.OBJECTS,
            scope="full",
            max_seconds=0.001,
            max_events=50_000,
            workers=1,
            out=tmp_path / "expired.json",
        )
    )
    assert result["status"] == "INCOMPLETE"
    assert result["excluded_case_ids"] == []
    assert result["geometry_verified"] is False


@pytest.mark.slow
def test_complete_2095_receipt_has_every_step_and_no_pending_row(tmp_path: Path) -> None:
    manifest = sequential.load_manifest(sequential.MANIFEST)
    recipe = next(row for row in manifest["cases"] if row["mask_index"] == 2095)
    assert recipe["source_sha256"] == generic.SOURCE_PIN[0]
    assert recipe["seed_sha256"] == generic.SEED_PIN[0]
    assert recipe["audit_sha256"] == generic.AUDIT_PIN[0]
    # One reviewed exact-cover worker avoids a nested pool inside the slow lane.
    # The finite clock remains live, and every row must finish before acceptance.
    result = sequential.run(
        argparse.Namespace(
            case_id=2095,
            manifest=sequential.MANIFEST,
            objects=generic.OBJECTS,
            max_seconds=60,
            max_events=50_000,
            workers=1,
            cover_backend="fast",
            collision_backend="reference",
            out=tmp_path / "complete.json",
        )
    )
    assert result["status"] == "PASS_ONE_GENERIC_EXCLUSION"
    assert result["geometry_verified"] is True
    assert result["excluded_case_ids"] == [2095]
    assert result["source_sha256"]["source_node_0"] == generic.SOURCE_PIN[2]
    assert result["steps_completed"] == 5
    assert result["rows_checked"] == 160
    assert [item["rows"] for item in result["step_timings"]] == [32] * 5
    assert result["current_step"] is None
    assert result["current_row"] is None
    assert result["pending_row_indices"] == []
    assert result["global_optimality_proved"] is False
    assert json.loads((tmp_path / "complete.json").read_text()) == result
