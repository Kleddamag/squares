"""Focused closed-cut and premise controls for the r1 capture adapter."""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_capture_branch_r1 as branch
from devtools import check_n11_capture_root_bridge as bridge
from devtools import check_n11_capture_root_node as root
from devtools import check_n11_capture_root_pilot as pilot


def accepted_root() -> dict[str, Any]:
    return {
        "status": "PASS_ROOT_NODE_STATE",
        "root_node_state_checked": True,
        "capture_tree_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": branch.ROOT_CHECKER_SHA,
        "root_source_sha256": bridge.ROOT_SOURCE_SHA,
        "adaptive_sha256": pilot.ADAPTIVE_SHA,
        "step0_result_sha256": root.STEP0_RESULT_SHA,
        "collision_backend": "integer",
        "row_limit": 0,
        "stop_step": 13,
        "steps_checked": 14,
        "steps": [{"index": index, "complete": index < 13} for index in range(1, 14)],
    }


def sample_state() -> tuple[dict[str, Any], dict[str, Any]]:
    groups = {str(owner): [["0", "0"], ["1", "0"], ["0", "1"]] for owner in pilot.MASK}
    cells = {}
    references = {}
    for owner in pilot.MASK:
        ref = {"kind": "phase3", "node": "root-self-240", "step": 11, "row": 0}
        row = {
            "reference": ref,
            "interval": ["0", "1"],
            "outer_domain": [["0", "0"], ["4", "0"], ["4", "4"], ["0", "4"]],
            "residual_polygons": [],
        }
        cells[str(owner)] = [row]
        references[str(owner)] = [ref]
    return {"groups": groups, "cells": cells}, {
        "groups": copy.deepcopy(groups),
        "cell_references": references,
    }


def test_root_premise_requires_complete_actual_sequence() -> None:
    accepted = accepted_root()
    branch.admit_root_result(accepted)
    for change in (
        {"status": "INCOMPLETE"},
        {"steps_checked": 13},
        {"row_limit": 1},
        {"steps": accepted["steps"][:-1]},
    ):
        with pytest.raises(ValueError, match="complete accepted root"):
            branch.admit_root_result({**accepted, **change})


def test_root_receipt_bytes_are_pinned(tmp_path: Path) -> None:
    receipt = (
        Path(__file__).resolve().parents[1]
        / "resources/web/n11-optimality-2026-09-29/receipts"
        / "capture-root-node-full-integer/result.json"
    )
    assert branch.root_receipt_digest(receipt) == branch.ROOT_RESULT_SHA
    altered = tmp_path / "altered.json"
    altered.write_bytes(receipt.read_bytes().replace(b"PASS_ROOT_NODE_STATE", b"INCOMPLETE"))
    with pytest.raises(ValueError, match="accepted root receipt changed"):
        branch.root_receipt_digest(altered)


def test_center_cut_preserves_closed_boundary_and_references() -> None:
    parent, initial = sample_state()
    groups, cells = branch.branch_state(parent, initial)
    bound = -branch.center_cut()[2]
    assert set(groups) == set(pilot.MASK)
    assert cells[15][0]["reference"] == parent["cells"]["15"][0]["reference"]
    assert all(Q(y) >= bound for _, y in cells[15][0]["outer_domain"])
    assert any(Q(y) == bound for _, y in cells[15][0]["outer_domain"])
    assert cells[13][0]["outer_domain"] == parent["cells"]["13"][0]["outer_domain"]

    singleton_parent = copy.deepcopy(parent)
    singleton_parent["cells"]["15"][0]["outer_domain"] = [["1", str(bound)]]
    _, singleton_cells = branch.branch_state(singleton_parent, initial)
    assert singleton_cells[15][0]["outer_domain"] == [["1", str(bound)]]

    bad_initial = copy.deepcopy(initial)
    bad_initial["cell_references"]["15"][0]["row"] = 1
    with pytest.raises(ValueError, match="row references"):
        branch.branch_state(parent, bad_initial)


def test_r1_header_requires_exact_closed_cut_and_parent() -> None:
    nx, ny, upper = branch.center_cut()
    header = {
        "schema": "exact_branch_owned_hull_v1",
        "node_id": branch.R1_NODE,
        "mask_index": 438,
        "mask": list(pilot.MASK),
        "U": str(branch.geometry.U),
        "B": str(branch.geometry.B),
        "parent": {"path": branch.ROOT_PATH, "sha256": bridge.ROOT_SOURCE_SHA},
        "source": {"path": "adaptive"},
        "guard_source": {"path": "guard"},
        "constraints": [
            {
                "owner": 15,
                "normal": [int(nx), int(ny)],
                "upper_field": str(upper),
                "axis": 1,
                "bound_centered_unit": "5/4",
                "keep": "ge",
            }
        ],
    }
    parent = {"source": header["source"], "guard_source": header["guard_source"]}
    branch.check_r1_header(header, parent)
    changed = copy.deepcopy(header)
    changed["constraints"][0]["upper_field"] = str(upper + Q(1, 10**9))
    with pytest.raises(ValueError, match="center condition"):
        branch.check_r1_header(changed, parent)
    changed = copy.deepcopy(header)
    changed["parent"]["sha256"] = "wrong"
    with pytest.raises(ValueError, match="ancestry or frame"):
        branch.check_r1_header(changed, parent)
