"""Replay both halves of an admitted closed center partition.

This module joins already checked generic transitions. It does not admit source
objects or seed geometry: the caller supplies pinned objects and the accepted
seed state, then grants case credit only after both leaves return.
"""

from __future__ import annotations

import copy
from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_generic_fresh as frozen
from devtools import check_n11_generic_sequential as generic
from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_nonfield_ancestry as ancestry
from devtools import n11_nonfield_center_partition as partition

Polygon = frozen.Polygon


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _branch_child_state(
    child: dict[str, Any],
    *,
    parent_sha: str,
    seed_sha: str,
    case_id: int,
    mask: tuple[int, ...],
    groups: dict[int, Polygon],
    rows: dict[int, list[dict[str, Any]]],
) -> tuple[dict[int, Polygon], dict[int, list[dict[str, Any]]]]:
    """Bind a constrained child to its own accepted predecessor state."""
    require(
        isinstance(child["parent"], dict)
        and child["parent"].get("sha256") == parent_sha
        and child["mask_index"] == case_id
        and child["mask"] == list(mask)
        and child["source"]["sha256"] == seed_sha
        and Q(child["U"]) == geometry.U
        and Q(child["B"]) == geometry.B
        and child["guard_source"] is None,
        "branch child identity",
    )
    require(set(groups) == set(mask) and set(rows) == set(mask), "branch parent inventory")
    initial = child["initial"]
    require(
        set(initial["groups"]) == set(map(str, mask))
        and set(initial["cell_references"]) == set(map(str, mask)),
        "branch initial inventory",
    )
    for owner in mask:
        require(
            frozen.hull(frozen.points(initial["groups"][str(owner)]))
            == frozen.hull(groups[owner])
            and initial["cell_references"][str(owner)]
            == [row["reference"] for row in rows[owner]],
            "branch initial state differs from accepted parent",
        )
    return copy.deepcopy(groups), copy.deepcopy(rows)


def replay_center_partition(
    recipe: dict[str, Any],
    tree: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    groups: dict[int, Polygon],
    rows: dict[int, list[dict[str, Any]]],
    *,
    world: list[Polygon],
    mask: tuple[int, ...],
    result: dict[str, Any],
    budget: geometry.Budget,
    workers: int,
    cover_backend: str,
    collision_backend: str,
) -> partition.CenterPartition:
    """Join a checked common chain and two isolated, complete terminal leaves."""
    plan = partition.admit_center_partition(recipe, tree, sources)
    require(
        recipe["mask_index"] == result["mask_index"] and tuple(recipe["mask"]) == mask,
        "partition case identity",
    )
    for chain, constrained in (
        (plan.common_sources, False),
        (plan.branches[0].sources, True),
        (plan.branches[1].sources, True),
    ):
        parent_sha = plan.common_sources[-1] if constrained else None
        for sha in chain:
            generic.capability_preflight(
                sources[sha],
                mask,
                budget.max_nodes,
                parent_sha,
                admitted_constraints=constrained,
            )
            parent_sha = sha

    for index, sha in enumerate(plan.common_sources):
        result["current_node"] = index
        result["current_branch"] = "common"
        if index:
            groups, rows = ancestry.admit_child_state(
                sources[sha],
                parent_source_sha256=plan.common_sources[index - 1],
                seed_sha256=recipe["seed_sha256"],
                case_id=recipe["mask_index"],
                mask=mask,
                accepted_groups=groups,
                accepted_rows=rows,
            )
        groups, rows = generic.replay_one_node(
            sources[sha],
            groups,
            rows,
            world=world,
            mask=mask,
            result=result,
            budget=budget,
            workers=workers,
            cover_backend=cover_backend,
            collision_backend=collision_backend,
            parent_sha=plan.common_sources[index - 1] if index else None,
            final_node=False,
        )
        result["nodes_completed"] = index + 1

    common_groups, common_rows = copy.deepcopy(groups), copy.deepcopy(rows)
    node_number = len(plan.common_sources)
    for branch in plan.branches:
        groups, rows = copy.deepcopy(common_groups), copy.deepcopy(common_rows)
        parent_sha = plan.common_sources[-1]
        for index, sha in enumerate(branch.sources):
            result["current_node"] = node_number
            result["current_branch"] = branch.side
            groups, rows = _branch_child_state(
                sources[sha],
                parent_sha=parent_sha,
                seed_sha=recipe["seed_sha256"],
                case_id=recipe["mask_index"],
                mask=mask,
                groups=groups,
                rows=rows,
            )
            groups, rows = generic.replay_one_node(
                sources[sha],
                groups,
                rows,
                world=world,
                mask=mask,
                result=result,
                budget=budget,
                workers=workers,
                cover_backend=cover_backend,
                collision_backend=collision_backend,
                parent_sha=parent_sha,
                final_node=index == len(branch.sources) - 1,
                center_planes={branch.owner: [branch.plane]},
            )
            result["nodes_completed"] += 1
            node_number += 1
            parent_sha = sha
        result.setdefault("branches_completed", []).append(branch.side)
    require(result["branches_completed"] == ["le", "ge"], "incomplete center partition")
    result["current_node"] = result["current_branch"] = None
    generic.remaining(budget)
    return plan
