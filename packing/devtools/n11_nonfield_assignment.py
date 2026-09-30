"""Bind one A2 extension recipe to the pinned census metadata.

This checks case/source bookkeeping only. It does not validate the proposed
geometry or promote an excluded case.
"""

from __future__ import annotations

import re
from typing import Any


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _ids(value: object, count: int, label: str) -> set[int]:
    if not isinstance(value, list) or len(value) != count:
        raise ValueError(f"{label} inventory")
    require(
        all(type(item) is int and 0 <= item < 2184 for item in value),
        f"{label} case ID",
    )
    result = set(value)
    require(len(result) == count, f"{label} duplicate case ID")
    return result


def admit_a2_extension(
    case_id: int,
    recipe: dict[str, Any],
    baseline: dict[str, Any],
    extension: dict[str, Any],
    *,
    baseline_object_sha256: str,
) -> None:
    """Require exact census ancestry and a unique source/audit for one A2 case."""
    require(type(case_id) is int and 0 <= case_id < 2184, "A2 case ID")
    require(recipe.get("family") == "A2" and recipe.get("mask_index") == case_id, "A2 recipe")
    require(_sha(baseline_object_sha256), "A2 baseline object SHA")
    prior = _ids(baseline.get("excluded_canonical_mask_indices"), 1931, "A1 baseline")
    require(
        _sha(baseline.get("authoritative_snapshot_sha256"))
        and extension.get("status") == "PASS_STRICT_PRIOR_76_EXTENSION_INTEGRATION"
        and extension.get("baseline_sha256") == baseline["authoritative_snapshot_sha256"]
        and extension.get("baseline_excluded") == 1931
        and extension.get("fresh_baseline_replay", {}).get("sha256") == baseline_object_sha256,
        "A2 baseline binding",
    )
    entries = extension.get("extension_entries")
    if not isinstance(entries, list) or len(entries) != 76:
        raise ValueError("A2 extension inventory")
    seen: set[int] = set()
    matched: dict[str, Any] | None = None
    for entry in entries:
        require(isinstance(entry, dict), "A2 extension entry")
        mask = entry.get("mask")
        require(type(mask) is int and 0 <= mask < 2184, "A2 extension case ID")
        require(mask not in prior and mask not in seen, "A2 extension duplicate or overlap")
        require(
            entry.get("cases") == [mask] and entry.get("new_cases") == [mask], "A2 singleton"
        )
        require(
            _sha(entry.get("source_sha256")) and _sha(entry.get("audit_sha256")),
            "A2 extension source SHA",
        )
        require(
            isinstance(entry.get("kind"), str)
            and type(entry.get("nodes")) is int
            and entry["nodes"] > 0,
            "A2 extension shape",
        )
        seen.add(mask)
        if mask == case_id:
            matched = entry
    if matched is None:
        raise ValueError("A2 case not in extension")
    require(
        extension.get("extension_receipts") == 76
        and extension.get("distinct_extension_cases") == 76
        and _ids(extension.get("excluded_canonical_mask_indices"), 2007, "A2 prior")
        == prior | seen,
        "A2 union binding",
    )
    evidence = extension.get("per_case_evidence")
    require(
        isinstance(evidence, dict)
        and isinstance(evidence.get(str(case_id)), list)
        and matched["audit_sha256"] in evidence[str(case_id)],
        "A2 per-case evidence binding",
    )
    require(
        matched["source_sha256"] == recipe.get("source_sha256")
        and matched["audit_sha256"] == recipe.get("audit_sha256")
        and matched["kind"] == recipe.get("source_profile")
        and matched["nodes"] == len(recipe.get("ordered_ancestry_proposal", [])),
        "A2 extension differs from pinned recipe",
    )
