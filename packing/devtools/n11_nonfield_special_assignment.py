"""Bind special A2 audit metadata without importing its geometric assertions.

The ordinary A2 assignment checker still binds the exact census and source
recipe. This additional check handles the two special audit formats; their
claimed success, cached geometry, and purported baseline replay are not premises.
"""

from __future__ import annotations

from fractions import Fraction as Q
from typing import Any

from devtools import check_n11_optimality_field_mask0 as geometry


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def admit_special_audit(
    recipe: dict[str, Any], audit: dict[str, Any], baseline: dict[str, Any]
) -> None:
    """Check case/frame/source identities only; return no geometric conclusion."""
    case = recipe["mask_index"]
    require(
        type(case) is int
        and recipe["family"] == "A2"
        and audit["mask_index"] == case
        and audit["mask"] == recipe["mask"]
        and Q(audit["parent_Uplus"]) == geometry.U
        and Q(audit["parent_side"]) == geometry.B
        and audit["global_optimality_proved"] is False,
        "special audit case or frame identity",
    )
    nodes = recipe["ordered_ancestry_proposal"]
    if recipe["adapter"] == "baseline_necessary_d4":
        require(
            case in (2175, 2176)
            and recipe["source_profile"] == "necessary_D4_cuts_and_independent_geometry"
            and len(nodes) == 1
            and audit["source_sha256"] == recipe["source_sha256"]
            and audit["baseline_sha256"] == baseline["authoritative_snapshot_sha256"]
            and [node["sha256"] for node in audit["checked_ancestry"]]
            == [nodes[0]["source_sha256"]]
            and audit["necessary_halfplanes_checked"] == len(nodes[0]["constraints_proposal"]),
            "special D4 audit source or baseline identity",
        )
    elif recipe["adapter"] == "closed_center_partition":
        require(
            case == 1383
            and recipe["source_profile"] == "native_cached_v4_center_partition"
            and audit["tree_sha256"] == recipe["source_sha256"]
            and audit["root_sha256"] == recipe["seed_sha256"]
            and audit["cover_sha256"] == geometry.COVER_SHA
            and audit["required_antecedent_mask"] == recipe["mask"]
            and audit["transferred_canonical_mask_indices"] == [case]
            and [(node["node"], node["sha256"]) for node in audit["nodes"]]
            == [(node["node_id"], node["source_sha256"]) for node in nodes],
            "special center-partition audit source identity",
        )
    else:
        raise ValueError("unsupported special audit adapter")
