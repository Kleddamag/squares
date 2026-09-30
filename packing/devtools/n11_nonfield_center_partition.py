"""Bind a closed two-way center split to exact source ancestry.

This establishes only an exhaustive branch plan. The caller must replay the
common chain, copy its accepted state separately into both branches, and prove
both terminal contradictions before granting any case exclusion.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_optimality_field_mask0 as geometry


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Branch:
    side: str
    sources: tuple[str, ...]
    owner: int
    plane: tuple[Q, Q, Q]


@dataclass(frozen=True)
class CenterPartition:
    common_sources: tuple[str, ...]
    branches: tuple[Branch, Branch]


def admit_center_partition(
    recipe: dict[str, Any], tree: dict[str, Any], sources: dict[str, dict[str, Any]]
) -> CenterPartition:
    """Check closed complementary halfspaces and every actual source parent edge."""
    require(
        recipe["adapter"] == "closed_center_partition"
        and tree["schema"] == "generic_binary_partition_tree_v1"
        and tree["mask_index"] == recipe["mask_index"]
        and tree["mask"] == recipe["mask"]
        and tree["root_source"]["sha256"] == recipe["seed_sha256"],
        "center partition identity",
    )
    declared = {node["source_sha256"]: node for node in recipe["ordered_ancestry_proposal"]}
    require(
        len(declared) == len(recipe["ordered_ancestry_proposal"])
        and set(sources) == set(declared),
        "center partition source inventory",
    )
    for sha, source in sources.items():
        require(
            source["node_id"] == declared[sha]["node_id"]
            and source["mask_index"] == recipe["mask_index"]
            and source["mask"] == recipe["mask"]
            and source["source"]["sha256"] == recipe["seed_sha256"]
            and Q(source["U"]) == geometry.U
            and Q(source["B"]) == geometry.B
            and source["guard_source"] in (None, {}),
            "center partition source frame or guard",
        )

    def ancestry(target: str) -> tuple[str, ...]:
        chain: list[str] = []
        while True:
            require(target in sources and target not in chain, "missing or cyclic ancestry")
            chain.append(target)
            parent = sources[target]["parent"]
            if parent is None:
                return tuple(reversed(chain))
            require(isinstance(parent, dict), "source parent grammar")
            target = parent["sha256"]

    nodes = tree["nodes"]
    roots = [key for key, node in nodes.items() if node["parent"] is None]
    require(len(roots) == 1 and len(nodes) == 3, "closed binary tree inventory")
    root_id = roots[0]
    root = nodes[root_id]
    split = root["split"]
    children = split["children"]
    require(
        root["receipt"]["sha256"] == tree["root_receipt"]["sha256"]
        and split["kind"] == "center"
        and type(split["axis"]) is int
        and split["axis"] in (0, 1)
        and type(split["owner"]) is int
        and split["owner"] in recipe["mask"]
        and set(children) == {"le", "ge"}
        and len(set(children.values())) == 2
        and set(children.values()) == set(nodes) - {root_id},
        "closed complementary split grammar",
    )
    common = ancestry(root["receipt"]["sha256"])
    require(
        all(sources[sha]["constraints"] == [] for sha in common), "common center assumptions"
    )
    owner, axis = split["owner"], split["axis"]
    centered = Q(split["bound_centered_unit"])
    upper = geometry.B * (geometry.U / 2 + centered)
    branches: list[Branch] = []
    used = set(common)
    for side, sign in (("le", 1), ("ge", -1)):
        child = nodes[children[side]]
        require(child["parent"] == root_id and child["side"] == side, "branch tree parent")
        chain = ancestry(child["receipt"]["sha256"])
        require(
            chain[: len(common)] == common and len(chain) > len(common),
            "branch common ancestry",
        )
        tail = chain[len(common) :]
        require(not used.intersection(tail), "branches share a constrained state")
        used.update(tail)
        normal = (Q(sign if axis == 0 else 0), Q(sign if axis == 1 else 0))
        plane = (*normal, sign * upper)
        for sha in tail:
            constraints = sources[sha]["constraints"]
            require(len(constraints) == 1, "branch constraint inventory")
            cut = constraints[0]
            require(
                cut["owner"] == owner
                and cut["axis"] == axis
                and cut["keep"] == side
                and Q(cut["bound_centered_unit"]) == centered
                and tuple(map(Q, cut["normal"])) == normal
                and Q(cut["upper_field"]) == plane[2],
                "branch is not the exact closed halfspace",
            )
        branches.append(Branch(side, tail, owner, plane))
    require(used == set(sources), "unaccounted partition source")
    return CenterPartition(common, (branches[0], branches[1]))
