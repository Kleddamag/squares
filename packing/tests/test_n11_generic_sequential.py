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


def test_multinode_case_remains_unproved(tmp_path: Path) -> None:
    result = generic.run(_args(tmp_path, 2053))
    assert result["status"] == "REFUSED"
    assert "multi-node" in result["error"]
    assert result["geometry_verified"] is False
    assert result["excluded_case_ids"] == []


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


def test_imported_frozen_helper_pin_mismatch_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(generic, "FROZEN_GENERIC_SHA", "0" * 64)
    result = generic.run(_args(tmp_path, 2135))
    assert result["status"] == "REFUSED"
    assert "frozen generic" in result["error"]
    assert result["excluded_case_ids"] == []


def test_missing_angular_row_and_changed_source_state_refuse() -> None:
    manifest, recipe = _recipe(2135)
    source = generic.load_object(recipe["source_sha256"], manifest, generic.OBJECTS)
    seed = generic.load_object(recipe["seed_sha256"], manifest, generic.OBJECTS)
    cover = generic.load_object(
        generic.geometry.COVER_SHA,
        manifest,
        generic.PACKET / "receipts/d4-independent/objects",
    )
    groups, rows, world, bins = generic.seed_state(
        seed,
        cover,
        2135,
        tuple(recipe["mask"]),
        budget=generic.geometry.Budget(time.monotonic() + 30, 50_000),
    )
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
