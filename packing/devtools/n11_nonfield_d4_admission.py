"""Join freshly checked baseline D4 cuts to an actual constrained source node.

The caller must execute the frozen cut checker with an explicitly bound baseline
inventory, bind all source objects, and recheck those bindings before acceptance.
This helper validates the join only; a supplied receipt is not proof of execution.
"""

from __future__ import annotations

from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_baseline_d4_cuts as d4_cuts
from devtools import check_n11_optimality_field_mask0 as geometry

CUT_CHECKER_SHA = "338fb431d381502fa1a9721647f231f1a3e9db73a3c6337c3561e69d16bf5d32"
Plane = tuple[Q, Q, Q]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def constraint_rows(items: Any) -> list[tuple[int, Plane]]:
    require(isinstance(items, list), "D4 constraint list")
    result = []
    for item in items:
        require(
            isinstance(item, dict)
            and type(item.get("owner")) is int
            and isinstance(item.get("normal"), list)
            and len(item["normal"]) == 2,
            "D4 constraint grammar",
        )
        nx, ny = map(Q, item["normal"])
        require((nx, ny) != (0, 0), "D4 zero normal")
        result.append((item["owner"], (nx, ny, Q(item["upper_field"]))))
    return result


def admitted_constraint_planes(
    source: dict[str, Any], recipe: dict[str, Any], cut_report: dict[str, Any]
) -> dict[int, list[Plane]]:
    """Match exact necessary planes after the caller completes the finite check."""
    require(
        cut_report.get("status") == "PASS_CONDITIONAL_BASELINE_D4_CUTS"
        and cut_report.get("checker_sha256") == CUT_CHECKER_SHA
        and cut_report.get("source_revision") == geometry.SOURCE_REVISION
        and cut_report.get("finite_obligations_complete") is True
        and cut_report.get("baseline_execution_premise_admitted") is True
        and cut_report.get("necessary_cuts_verified") is True
        and cut_report.get("proof_credit") is True
        and cut_report.get("baseline_pending_case_ids") == []
        and cut_report.get("excluded_case_ids") == []
        and cut_report.get("global_optimality_proved") is False,
        "D4 finite-cut execution premise is incomplete",
    )
    case = recipe["mask_index"]
    require(
        type(case) is int
        and case in (2175, 2176)
        and recipe["adapter"] == "baseline_necessary_d4"
        and recipe["required_baseline_cases"] == 1931
        and len(recipe["ordered_ancestry_proposal"]) == 1,
        "D4 recipe identity",
    )
    node = recipe["ordered_ancestry_proposal"][0]
    require(
        source["mask_index"] == case
        and source["mask"] == recipe["mask"]
        and source["node_id"] == node["node_id"]
        and node["source_sha256"] == recipe["source_sha256"]
        and source["parent"] is None
        and source["guard_source"] is None
        and Q(source["U"]) == geometry.U
        and Q(source["B"]) == geometry.B,
        "D4 actual source identity",
    )
    matches = [item for item in cut_report["cases"] if item["mask_index"] == case]
    require(len(matches) == 1, "D4 cut report case inventory")
    checked = matches[0]
    require(
        checked["node_id"] == source["node_id"]
        and checked["source_sha256"] == recipe["source_sha256"],
        "D4 cut report source identity",
    )
    actual = constraint_rows(source["constraints"])
    require(
        len(actual) == {2175: 72, 2176: 73}[case]
        and actual == constraint_rows(node["constraints_proposal"])
        and actual == constraint_rows(checked["constraints"]),
        "D4 actual constraints differ from proved planes",
    )
    planes: dict[int, list[Plane]] = {owner: [] for owner in recipe["mask"]}
    for owner, plane in actual:
        require(owner in planes, "D4 plane owner outside mask")
        planes[owner].append(plane)
    require(
        cut_report["dependency_sha256"]
        == {name: value[1] for name, value in d4_cuts.DEPENDENCIES.items()},
        "D4 cut dependency identity",
    )
    return planes
