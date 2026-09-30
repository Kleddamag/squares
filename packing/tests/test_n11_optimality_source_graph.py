"""Actual parent-edge, assumption, and closure controls for the ten source nodes."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from devtools import check_n11_optimality_capture_ancestry as capture
from devtools import check_n11_optimality_source_graph as graph

RECEIPT = (
    Path(__file__).parents[1] / "resources/web/n11-optimality-2026-09-29/receipts/source-graph"
)
PACKETS = (
    Path(__file__).parents[1]
    / "resources/web/n11-optimality-2026-09-29/receipts/capture-ancestry/objects"
)
ROOT = "research/candidate-capture/root-self-240.json"
FAR15 = "research/candidate-capture/far15y-self-300.json"
R1 = "research/candidate-capture/tree438-rebuilt/r1.json"
R11 = "research/candidate-capture/tree438-facet/r11.json"
R110 = "research/candidate-capture/tree438-facet/r110.json"
R111 = "research/candidate-capture/tree438-facet/r111.json"
NEAR13 = "research/candidate-capture/near13-self-180.json"
NEAR = "research/candidate-capture/near-refined1024-240.json"


def inputs() -> tuple[dict, dict]:
    result = json.loads((RECEIPT / "result.json").read_text())
    pins = capture.load_packets(PACKETS)["B1"]["geometry_nodes"]
    return result["source_headers"], pins


def test_actual_source_graph_and_scope() -> None:
    headers, pins = inputs()
    checked = graph.check_source_graph(headers, pins)
    result = json.loads((RECEIPT / "result.json").read_text())
    assert checked["source_nodes_checked"] == 10
    assert checked["actual_parent_edges_checked"] == 9
    assert checked["far_leaf_contradiction_markers"] == ["far15", "far13", "far2"]
    assert result["status"] == "ACTUAL_SOURCE_PARENT_GRAPH_CHECKED_PUBLIC_AUDIT_BINDING_REFUSED"
    assert set(result["leaf_final_state_digests"]) == {"far15", "far13", "far2", "near"}
    assert all(
        pair["claimed"] != pair["actual"]
        for pair in result["leaf_final_state_digests"].values()
    )
    assert result["root_induction_geometry_proved"] is False
    assert result["geometric_capture_proved"] is False
    assert result["global_optimality_proved"] is False


def test_wrong_parent_and_lost_assumption_refuse() -> None:
    headers, pins = inputs()
    wrong_parent = copy.deepcopy(headers)
    wrong_parent[NEAR]["parent"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="missing or changed parent"):
        graph.check_source_graph(wrong_parent, pins)

    lost_cut = copy.deepcopy(headers)
    lost_cut[R111]["constraints"].pop(0)
    with pytest.raises(ValueError, match="inherited branch assumption"):
        graph.check_source_graph(lost_cut, pins)


def test_hidden_root_cycle_and_contradictory_parent_refuse() -> None:
    headers, pins = inputs()
    hidden_root = copy.deepcopy(headers)
    hidden_root[ROOT]["constraints"] = [capture.center_cut("le")]
    with pytest.raises(ValueError, match="hidden parent or assumption"):
        graph.check_source_graph(hidden_root, pins)

    cycle = copy.deepcopy(headers)
    cycle[NEAR13]["parent"] = {
        "path": graph.SOURCE_PREFIX + R11,
        "sha256": pins[R11],
    }
    with pytest.raises(ValueError, match="disconnected from root"):
        graph.check_source_graph(cycle, pins)

    after_contradiction = copy.deepcopy(headers)
    after_contradiction[R1]["parent"] = {
        "path": graph.SOURCE_PREFIX + FAR15,
        "sha256": pins[FAR15],
    }
    with pytest.raises(ValueError, match="continuation after contradiction"):
        graph.check_source_graph(after_contradiction, pins)


def test_missing_far_closure_refuses() -> None:
    headers, pins = inputs()
    unclosed = copy.deepcopy(headers)
    unclosed[R110]["closed"] = False
    unclosed[R110]["contradiction"] = None
    with pytest.raises(ValueError, match="whole-branch contradiction"):
        graph.check_source_graph(unclosed, pins)
