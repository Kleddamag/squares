"""Exact closed-partition, graph, and public-source refusal controls."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from devtools import check_n11_optimality_capture_ancestry as capture

RECEIPT = (
    Path(__file__).parents[1]
    / "resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry"
)


def packets() -> dict:
    return capture.load_packets(RECEIPT / "objects")


def test_reported_inventory_and_source_refusal_scope() -> None:
    checked = capture.check_reported(packets())
    result = json.loads((RECEIPT / "refusal-result.json").read_text())
    assert checked["reported_geometry_nodes"] == 10
    assert checked["reported_bound_premises"] == 24
    assert checked["reported_root_owner_rounds"] == 154
    assert checked["closed_leaves"] == ["far15", "far13", "far2", "near"]
    assert result["status"] == "REPORTED_CAPTURE_METADATA_CONSISTENT_SOURCE_BINDING_REFUSED"
    assert (
        result["near_final_state_actual_sha256"] != result["near_final_state_reported_sha256"]
    )
    assert result["near_source_binding_accepted"] is False
    assert result["complete_source_ancestry_proved"] is False
    assert result["geometric_capture_proved"] is False
    assert result["global_optimality_proved"] is False


def test_lost_closed_boundary_and_wrong_field_sign_refuse() -> None:
    source = packets()
    omitted_boundary = copy.deepcopy(source)
    omitted_boundary["B2"]["closed_leaves"][1]["predicates"][1][3] = "lt"
    with pytest.raises(ValueError, match="closed partition"):
        capture.check_reported(omitted_boundary)

    wrong_field_sign = copy.deepcopy(source)
    wrong_field_sign["B5"]["constraints"][0]["normal"] = [0, 1]
    with pytest.raises(ValueError, match="field or angle cut"):
        capture.check_reported(wrong_field_sign)


def test_missing_owner_round_or_geometry_node_refuses() -> None:
    source = packets()
    omitted_round = copy.deepcopy(source)
    omitted_round["B3"]["cells"].pop()
    with pytest.raises(ValueError, match="owner-round inventory"):
        capture.check_reported(omitted_round)

    omitted_node = copy.deepcopy(source)
    omitted_node["B7"]["nodes"].pop(0)
    with pytest.raises(ValueError, match="node count differs"):
        capture.check_reported(omitted_node)


def test_unbound_or_changed_cached_premise_refuses() -> None:
    source = packets()
    unbound = copy.deepcopy(source)
    unbound["B5"]["nodes"][0]["cached_from_audit_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="not earlier"):
        capture.check_reported(unbound)

    changed = copy.deepcopy(source)
    changed["B5"]["nodes"][0]["rows"] += 1
    with pytest.raises(ValueError, match="math fields changed"):
        capture.check_reported(changed)
