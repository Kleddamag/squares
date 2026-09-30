"""Conditional D4 planes cannot be detached from their execution and source."""

from __future__ import annotations

import copy
import gzip
import json
from fractions import Fraction as Q

import pytest

from devtools import n11_nonfield_d4_admission as admission


def fixture():
    manifest = json.loads(
        gzip.decompress(
            (
                admission.geometry.PACKET / "receipts/nonfield-manifest/manifest.json.gz"
            ).read_bytes()
        )
    )
    recipe = next(item for item in manifest["cases"] if item["mask_index"] == 2175)
    node = recipe["ordered_ancestry_proposal"][0]
    source = {
        "mask_index": 2175,
        "mask": recipe["mask"],
        "node_id": node["node_id"],
        "parent": None,
        "guard_source": None,
        "U": str(admission.geometry.U),
        "B": str(admission.geometry.B),
        "constraints": copy.deepcopy(node["constraints_proposal"]),
    }
    # Deliberately synthetic premise: only the join is tested here.
    report = {
        "status": "PASS_CONDITIONAL_BASELINE_D4_CUTS",
        "checker_sha256": admission.CUT_CHECKER_SHA,
        "source_revision": admission.geometry.SOURCE_REVISION,
        "finite_obligations_complete": True,
        "baseline_execution_premise_admitted": True,
        "necessary_cuts_verified": True,
        "proof_credit": True,
        "baseline_pending_case_ids": [],
        "excluded_case_ids": [],
        "global_optimality_proved": False,
        "dependency_sha256": {
            name: value[1] for name, value in admission.d4_cuts.DEPENDENCIES.items()
        },
        "cases": [
            {
                "mask_index": 2175,
                "node_id": node["node_id"],
                "source_sha256": recipe["source_sha256"],
                "constraints": copy.deepcopy(node["constraints_proposal"]),
            }
        ],
    }
    return source, recipe, report


def test_join_preserves_exact_planes_for_every_owner() -> None:
    source, recipe, report = fixture()
    planes = admission.admitted_constraint_planes(source, recipe, report)
    assert set(planes) == set(recipe["mask"])
    assert sum(map(len, planes.values())) == 72
    for item in source["constraints"]:
        assert (*map(Q, item["normal"]), Q(item["upper_field"])) in planes[item["owner"]]


@pytest.mark.parametrize(
    "changed",
    [
        {"status": "PASS_DIAGNOSTIC_FINITE_CUT_OBLIGATIONS"},
        {"baseline_pending_case_ids": [1723]},
        {"baseline_execution_premise_admitted": False},
        {"necessary_cuts_verified": False},
        {"checker_sha256": "0" * 64},
        {"global_optimality_proved": True},
    ],
)
def test_incomplete_or_different_premise_cannot_supply_planes(changed) -> None:
    source, recipe, report = fixture()
    with pytest.raises(ValueError, match="execution premise"):
        admission.admitted_constraint_planes(source, recipe, {**report, **changed})


def test_exact_plane_or_source_change_cannot_reuse_cut_result() -> None:
    source, recipe, report = fixture()
    source["constraints"][0]["upper_field"] = str(
        Q(source["constraints"][0]["upper_field"]) + Q(1, 10**70)
    )
    with pytest.raises(ValueError, match="constraints differ"):
        admission.admitted_constraint_planes(source, recipe, report)
    source, recipe, report = fixture()
    report["cases"][0]["source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source identity"):
        admission.admitted_constraint_planes(source, recipe, report)
