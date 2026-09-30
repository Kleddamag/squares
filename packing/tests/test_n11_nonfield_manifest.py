"""Focused admission controls for proposal-only non-field recipes."""

from __future__ import annotations

import copy
import stat
from typing import Any

import pytest

from devtools.prepare_n11_nonfield_manifest import (
    COVER,
    canonical_masks,
    ordered_nodes,
    returned_transport,
)


def node(fingerprint: str) -> dict[str, Any]:
    return {
        "sha256": fingerprint,
        "node": fingerprint,
        "path": f"historical/{fingerprint}.json",
        "constraints": [],
        "complete_steps": 1,
        "rows": 8,
        "arrangement_slabs": 16,
    }


def transport_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    roles = {
        "ancestry_node": "terminal",
        "wall_seed": "seed",
        "cover": COVER,
        "saved_audit": "audit",
    }
    case: dict[str, Any] = {
        "archive": "bundle.zip",
        "saved_audit_sha256": "audit",
        "stream_extract_members": [],
    }
    archive: dict[str, Any] = {"kind": "zip", "members": []}
    index: dict[str, Any] = {
        "files": {"evidence/bundle.zip": "archive"},
        "objects": {"archive": archive},
    }
    for role, fingerprint in roles.items():
        name = f"certificates/{role}.json"
        archive["members"].append(
            {"name": name, "source": fingerprint, "mode": stat.S_IFREG | 0o600}
        )
        index["objects"][fingerprint] = {
            "kind": "blob",
            "sha256": fingerprint,
            "bytes": 20,
        }
        case["stream_extract_members"].append(
            {
                "member": name,
                "expected_sha256": fingerprint,
                "bytes": 20,
                "role": role,
                "destination_name": f"{role}.json",
            }
        )
    return case, index


def test_canonical_census_is_complete_and_half_turn_reduced() -> None:
    masks = canonical_masks()
    assert len(masks) == 2184
    assert len({tuple(mask) for mask in masks}) == 2184
    assert all(
        len(mask) == 11 and mask <= sorted(15 - owner for owner in mask) for mask in masks
    )


def test_declared_ancestry_rejects_missing_terminal_and_duplicates() -> None:
    audit = {"nodes": [node("first"), node("terminal")]}
    assert [item["source_sha256"] for item in ordered_nodes(audit, "terminal", tree=False)] == [
        "first",
        "terminal",
    ]
    with pytest.raises(ValueError, match="terminal is not last"):
        ordered_nodes(audit, "first", tree=False)
    with pytest.raises(ValueError, match="duplicate ancestry"):
        ordered_nodes({"nodes": [node("terminal"), node("terminal")]}, "terminal", tree=False)
    with pytest.raises(ValueError, match="missing node"):
        ordered_nodes({"nodes": []}, "terminal", tree=False)


@pytest.mark.parametrize("mode", [stat.S_IFREG | 0o600, 0o600])
def test_returned_members_bind_all_premises_without_extracting_zip(mode: int) -> None:
    case, index = transport_fixture()
    index["objects"]["archive"]["members"][0]["mode"] = mode
    assert len(returned_transport(case, index, {"terminal"}, "seed")) == 4


@pytest.mark.parametrize("mutation", ["omitted", "duplicate", "hash", "length", "symlink"])
def test_returned_member_mutations_refuse(mutation: str) -> None:
    case, index = transport_fixture()
    if mutation == "omitted":
        case["stream_extract_members"].pop(0)
    elif mutation == "duplicate":
        case["stream_extract_members"].append(copy.deepcopy(case["stream_extract_members"][0]))
    elif mutation == "hash":
        case["stream_extract_members"][0]["expected_sha256"] = "different"
    elif mutation == "length":
        case["stream_extract_members"][0]["bytes"] += 1
    else:
        index["objects"]["archive"]["members"][0]["mode"] = stat.S_IFLNK | 0o777
    with pytest.raises(ValueError, match=r"omits or adds|ambiguous|identity or byte length"):
        returned_transport(case, index, {"terminal"}, "seed")


def test_member_traversal_and_undeclared_ancestor_refuse() -> None:
    case, index = transport_fixture()
    with pytest.raises(ValueError, match="omits or adds"):
        returned_transport(case, index, {"terminal", "missing-parent"}, "seed")
    case["stream_extract_members"][0]["member"] = "../ancestry_node.json"
    with pytest.raises(ValueError, match="unsafe or ambiguous"):
        returned_transport(case, index, {"terminal"}, "seed")
