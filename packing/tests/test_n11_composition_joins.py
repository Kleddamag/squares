"""Reject gaps in capture conditions and mismatched local component scopes."""

import copy

import pytest

from devtools import check_n11_final_composition as final
from devtools.inventory_n11_completion import CAPTURE, FIXED, RECEIPTS, bound
from devtools.n11_composition_joins import (
    capture_conditions,
    local_joins,
    reviewed_capture_states,
)


def records():
    return {name: bound(RECEIPTS / name / "result.json", sha) for name, sha in FIXED.items()}


def test_changed_closed_split_or_inherited_condition_is_refused() -> None:
    graph = records()["source-graph"]
    capture_conditions(graph)
    changed = copy.deepcopy(graph)
    key = "research/candidate-capture/tree438-rebuilt/r1.json"
    changed["source_headers"][key]["constraints"][0]["normal"] = [0, 1]
    with pytest.raises(ValueError, match="closed capture conditions"):
        capture_conditions(changed)
    changed = copy.deepcopy(graph)
    key = "research/candidate-capture/tree438-facet/r111.json"
    changed["source_headers"][key]["constraints"].pop(0)
    with pytest.raises(ValueError, match="closed capture conditions"):
        capture_conditions(changed)


def test_wrong_final_state_and_missing_contradiction_are_refused() -> None:
    data = records()
    assert reviewed_capture_states(data["source-graph"], data, CAPTURE)
    changed = copy.deepcopy(data)
    changed["capture-child-far15"]["final_state_canonical_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="final state"):
        reviewed_capture_states(changed["source-graph"], changed, CAPTURE)
    changed = copy.deepcopy(data)
    changed["capture-child-far15"]["terminal_empty_pose_checked"] = False
    with pytest.raises(ValueError, match="empty-pose contradiction"):
        reviewed_capture_states(changed["source-graph"], changed, CAPTURE)


def test_missing_local_branch_or_changed_frame_is_refused() -> None:
    data = records()
    local_joins(data, RECEIPTS)
    changed = copy.deepcopy(data)
    changed["local-isolation"]["branch_results"].pop()
    with pytest.raises(ValueError, match="local endpoint computation scope"):
        local_joins(changed, RECEIPTS)
    changed = copy.deepcopy(data)
    changed["pose-inclusion"]["source_frame"]["inverse"] = "identity"
    with pytest.raises(ValueError, match="inverse frame"):
        local_joins(changed, RECEIPTS)


def test_final_composition_cannot_promote_unreviewed_union(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = final.compose()
    assert result["status"] == "INCOMPLETE_COMPOSITION"
    assert result["geometry_rerun"] is False
    assert result["global_optimality_proved"] is False
    assert result["missing_exclusion_ids"]
    monkeypatch.setattr(final, "REVIEWED_COMPLETE_EXCLUSION_INVENTORY", "0" * 64)
    with pytest.raises(ValueError, match="reviewed complete exclusion inventory changed"):
        final.compose()


def test_final_composition_refuses_source_change_during_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identities = iter([{"checker": "before"}, {"checker": "after"}])
    monkeypatch.setattr(final, "source_closure", lambda: next(identities))
    with pytest.raises(ValueError, match="composition source changed during execution"):
        final.compose()
