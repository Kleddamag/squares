"""Completion bookkeeping cannot convert metadata or cycles into proof credit."""

import hashlib
from pathlib import Path

import pytest

from devtools.inventory_n11_completion import acyclic, bound, completion, pending_joins


def test_changed_success_receipt_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "result.json"
    path.write_text('{"status":"PASS"}')
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert bound(path, sha)["status"] == "PASS"
    path.write_text('{"status":"PASS","global_optimality_proved":true}')
    with pytest.raises(ValueError, match="changed receipt"):
        bound(path, sha)


def test_missing_and_circular_premises_are_refused() -> None:
    acyclic({"root": None, "child": "root"})
    with pytest.raises(ValueError, match="cyclic"):
        acyclic({"cut": "exclusion", "exclusion": "cut"})
    with pytest.raises(ValueError, match="missing dependency"):
        acyclic({"child": "missing"})


def test_current_inventory_preserves_open_mathematical_obligations() -> None:
    result = completion()
    assert result["global_optimality_proved"] is False
    assert result["geometry_rerun"] is False
    assert result["missing_capture_source_sha256s"]
    assert result["final_composition_review_required"] is True
    assert "All three far-leaf contradictions" not in result["pending_joins"]


def test_pending_join_text_follows_actual_missing_components() -> None:
    final = "Final consumer join to the reviewed endpoint/witness argument"
    assert pending_joins([], [], []) == [final]
    assert pending_joins([1383], [], []) == [
        "1 required exclusion executions remain",
        "Both center-partition branches for case 1383",
        final,
    ]
    assert pending_joins([], [{"source_path": "near"}], ["r110"]) == [
        "1 capture node executions remain",
        "Capture leaf executions remain: r110",
        final,
    ]
