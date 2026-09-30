"""Source admission and full-square self-cut controls for generic replay."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import copy
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_generic_sequential as generic


def _recipe(case_id: int) -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = generic.load_manifest(generic.MANIFEST)
    recipe = next(row for row in manifest["cases"] if row["mask_index"] == case_id)
    return manifest, recipe


def _args(
    tmp_path: Path, case_id: int, *, manifest: Path = generic.MANIFEST
) -> argparse.Namespace:
    return argparse.Namespace(
        case_id=case_id,
        manifest=manifest,
        objects=generic.OBJECTS,
        workers=1,
        max_seconds=30,
        max_events=50_000,
        cover_backend="reference",
        collision_backend="reference",
        out=tmp_path / "result.json",
    )


def test_manifest_and_case_assignment_are_pinned(tmp_path: Path) -> None:
    manifest, recipe = _recipe(2135)
    generic.admit_assignment(2135, recipe, manifest)
    changed = copy.deepcopy(recipe)
    changed["job_id"] = "wrong-job"
    with pytest.raises(ValueError, match="assignment"):
        generic.admit_assignment(2135, changed, manifest)
    corrupt = tmp_path / "manifest.json.gz"
    corrupt.write_bytes(generic.MANIFEST.read_bytes() + b"x")
    result = generic.run(_args(tmp_path, 2135, manifest=corrupt))
    assert result["status"] == "REFUSED"
    assert result["excluded_case_ids"] == []


def test_a2_assignment_is_bound_before_geometry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, recipe = _recipe(221)
    generic.admit_assignment(221, recipe, manifest)
    changed = copy.deepcopy(recipe)
    changed["audit_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="A2 extension differs"):
        generic.admit_assignment(221, changed, manifest)
    monkeypatch.setattr(generic, "A2_HELPER_SHA", "0" * 64)
    result = generic.run(_args(tmp_path, 221))
    assert result["status"] == "REFUSED"
    assert "A2 assignment helper" in result["error"]
    assert result["excluded_case_ids"] == []


def test_multinode_case_remains_unproved(tmp_path: Path) -> None:
    result = generic.run(_args(tmp_path, 2053))
    assert result["status"] == "REFUSED"
    assert "multi-node" in result["error"]
    assert result["geometry_verified"] is False
    assert result["excluded_case_ids"] == []


def test_integer_collision_backend_refuses_case_without_collision_work(tmp_path: Path) -> None:
    args = _args(tmp_path, 2135)
    args.collision_backend = "integer"
    result = generic.run(args)
    assert result["status"] == "REFUSED"
    assert result["excluded_case_ids"] == []
    assert "no collision work" in result["error"]


def test_expired_case_has_no_promoted_exclusion(tmp_path: Path) -> None:
    args = _args(tmp_path, 2135)
    args.max_seconds = 0.001
    result = generic.run(args)
    assert result["status"] == "INCOMPLETE"
    assert result["geometry_verified"] is False
    assert result["excluded_case_ids"] == []


def test_self_cut_uses_full_square_support_and_handles_equality() -> None:
    boundary = generic.geometry.B / 2
    cut = {"normal": [1, 0], "upper": str(boundary)}
    assert generic.necessary_self_cuts(
        {"self_hull_cuts": [cut]}, [(Q(0), Q(0))], Q(0), Q(0)
    ) == [(Q(1), Q(0), boundary)]
    cut["upper"] = str(boundary - Q(1, 10_000))
    with pytest.raises(ValueError, match="full square"):
        generic.necessary_self_cuts({"self_hull_cuts": [cut]}, [(Q(0), Q(0))], Q(0), Q(0))


def test_2135_proposed_cut_is_independently_admitted() -> None:
    manifest, recipe = _recipe(2135)
    source = generic.load_object(recipe["source_sha256"], manifest, generic.OBJECTS)
    seed = generic.load_object(recipe["seed_sha256"], manifest, generic.OBJECTS)
    step = source["steps"][0]
    row = step["rows"][0]
    prior = generic.frozen.hull(generic.frozen.points(seed["groups"][str(step["owner"])]))
    assert len(generic.necessary_self_cuts(row, prior, Q(0), Q(1, 8))) == 4
    changed = copy.deepcopy(row)
    changed["self_hull_cuts"][0]["upper"] = "-100"
    with pytest.raises(ValueError, match="full square"):
        generic.necessary_self_cuts(changed, prior, Q(0), Q(1, 8))


def test_unjustified_2135_input_shrink_is_refused() -> None:
    manifest, recipe = _recipe(2135)
    source = generic.load_object(recipe["source_sha256"], manifest, generic.OBJECTS)
    seed = generic.load_object(recipe["seed_sha256"], manifest, generic.OBJECTS)
    step = copy.deepcopy(source["steps"][0])
    step["rows"][0]["input_domain"] = [["0", "0"]]
    prior = {
        owner: generic.frozen.hull(generic.frozen.points(seed["groups"][str(owner)]))
        for owner in recipe["mask"]
    }
    with pytest.raises(ValueError, match="row input domain"):
        generic.check_row(
            source,
            step,
            0,
            prior=prior,
            predecessor=seed["cells"][str(step["owner"])][0],
            world=[],
            bins=8,
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
        )


def test_input_domain_may_conservatively_enlarge_but_never_shrink() -> None:
    required = generic.frozen.hull([(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))])
    larger = [["-1", "-1"], ["2", "-1"], ["2", "2"], ["-1", "2"]]
    assert generic.covering_input_domain(required, larger) == required
    smaller = [["0", "0"], ["1/2", "0"], ["1/2", "1/2"], ["0", "1/2"]]
    with pytest.raises(ValueError, match="row input domain"):
        generic.covering_input_domain(required, smaller)


def test_empty_and_closed_segment_legal_rows_are_handled_exactly() -> None:
    center = generic.geometry.L / 2
    base_row = {
        "interval": ["0", "1"],
        "prior_reference": {"kind": "seed"},
        "reference": {"kind": "phase3", "node": "test", "step": 0, "row": 0},
        "input_domain": [],
        "core_vertices": [],
        "residual_polygons": [],
        "collision_regions": [],
        "common_core_halfplanes": [],
        "outer_bounds": [],
        "outer_domain": [],
    }
    step = {"owner": 0, "index": 0, "rows": [base_row]}
    predecessor = {"reference": {"kind": "seed"}, "interval": ["0", "1"], "outer_domain": []}

    def check():
        return generic.check_row(
            {"node_id": "test"},
            step,
            0,
            prior={0: [(Q(), Q())], 1: [(center, center)]},
            predecessor=predecessor,
            world=[],
            bins=1,
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
        )

    coverage, vertices, planes, accepted = check()
    assert coverage == {
        "events": 0,
        "probes": 0,
        "edge_segments": 0,
        "collision_facet_checks": 0,
    }
    assert vertices == planes == accepted["residual_polygons"] == []
    base_row["core_vertices"] = [["0", "0"]]
    with pytest.raises(ValueError, match="empty legal row"):
        check()
    radius = generic.geometry.B / 8
    base_row["core_vertices"] = [
        [str(x), str(y)]
        for x, y in [(-radius, -radius), (radius, -radius), (radius, radius), (-radius, radius)]
    ]
    segment = [(center - Q(1, 100), center), (center + Q(1, 100), center)]
    base_row["input_domain"] = [[str(x), str(y)] for x, y in segment]
    predecessor["outer_domain"] = [[str(x), str(y)] for x, y in segment]
    coverage, vertices, planes, accepted = check()
    assert coverage["events"] > 0
    assert coverage["probes"] > 0
    assert vertices == planes == accepted["residual_polygons"] == []


def test_imported_frozen_helper_pin_mismatch_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(generic, "FROZEN_GENERIC_SHA", "0" * 64)
    result = generic.run(_args(tmp_path, 2135))
    assert result["status"] == "REFUSED"
    assert "frozen generic" in result["error"]
    assert result["excluded_case_ids"] == []


def test_fast_cover_pin_mismatch_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(generic, "FAST_COVER_SHA", "0" * 64)
    args = _args(tmp_path, 2135)
    args.cover_backend = "fast"
    result = generic.run(args)
    assert result["status"] == "REFUSED"
    assert "fast cover kernel" in result["error"]
    assert result["excluded_case_ids"] == []


def test_missing_angular_row_and_changed_source_state_refuse() -> None:
    manifest, recipe = _recipe(2135)
    source = generic.load_object(recipe["source_sha256"], manifest, generic.OBJECTS)
    # These are deliberately unverified inputs to two early structural guards.
    # The complete replay control separately proves the actual seed geometry.
    groups = {
        int(owner): generic.frozen.hull(generic.frozen.points(points))
        for owner, points in source["initial"]["groups"].items()
    }
    rows = {
        int(owner): [{"reference": reference} for reference in references]
        for owner, references in source["initial"]["cell_references"].items()
    }
    world: list[generic.Polygon] = []
    bins = len(source["steps"][0]["rows"])
    changed = copy.deepcopy(source)
    changed["steps"][0]["rows"].pop()
    with pytest.raises(ValueError, match="angular inventory"):
        generic.replay_one_node(
            changed,
            groups,
            rows,
            world=world,
            bins=bins,
            mask=tuple(recipe["mask"]),
            result={},
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
            workers=1,
        )
    changed = copy.deepcopy(source)
    changed["initial"]["groups"][str(recipe["mask"][0])] = [["0", "0"]]
    with pytest.raises(ValueError, match="initial state"):
        generic.replay_one_node(
            changed,
            groups,
            rows,
            world=world,
            bins=bins,
            mask=tuple(recipe["mask"]),
            result={},
            budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
            workers=1,
        )


def test_preflight_allows_repeated_owner_and_supported_partner_cover_shape() -> None:
    manifest, recipe = _recipe(2135)
    source = generic.load_object(recipe["source_sha256"], manifest, generic.OBJECTS)
    mask = tuple(recipe["mask"])
    repeated = copy.deepcopy(source)
    extra = copy.deepcopy(repeated["steps"][0])
    extra["index"] = len(repeated["steps"])
    repeated["steps"].append(extra)
    generic.capability_preflight(repeated, mask, 8)
    repeated["steps"][0]["prior_partner_pose_covers"] = {"1": []}
    generic.capability_preflight(repeated, mask, 8)


@pytest.mark.slow
def test_complete_2135_exclusion(tmp_path: Path) -> None:
    args = _args(tmp_path, 2135)
    args.workers = 3
    result = generic.run(args)
    assert result["status"] == "PASS_ONE_GENERIC_EXCLUSION"
    assert result["excluded_case_ids"] == [2135]
    assert result["geometry_verified"] is True
    assert result["steps_completed"] == 6
    assert result["rows_checked"] == 48
    assert result["current_node"] is None
    assert result["current_step"] is None
    assert result["current_row"] is None
    assert result["global_optimality_proved"] is False


@pytest.mark.slow
def test_reference_and_fast_complete_2135_results_match(tmp_path: Path) -> None:
    results = []
    for backend in ("reference", "fast"):
        args = _args(tmp_path, 2135)
        args.workers = 3
        args.cover_backend = backend
        args.out = tmp_path / f"{backend}.json"
        results.append(generic.run(args))
    for result, backend in zip(results, ("reference", "fast"), strict=True):
        assert result["status"] == "PASS_ONE_GENERIC_EXCLUSION"
        assert result["geometry_verified"] is True
        assert result["excluded_case_ids"] == [2135]
        assert result["cover_backend"] == backend
        assert result["steps_completed"] == 6
        assert result["rows_checked"] == 48
    reference, fast = results
    assert [
        (row["events"], row["probes"])
        for step in reference["step_timings"]
        for row in step["row_timings"]
    ] == [
        (row["events"], row["probes"])
        for step in fast["step_timings"]
        for row in step["row_timings"]
    ]
