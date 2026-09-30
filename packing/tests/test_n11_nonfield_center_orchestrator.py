"""The closed branches replay from separate copies of one accepted root state."""

from __future__ import annotations

import time
from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import n11_nonfield_center_orchestrator as orchestrator
from devtools import n11_nonfield_center_partition as partition


def _source(node: str, parent: str | None, reference: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": node,
        "parent": {"sha256": parent} if parent else None,
        "mask_index": 1383,
        "mask": [0],
        "source": {"sha256": "seed"},
        "U": str(orchestrator.geometry.U),
        "B": str(orchestrator.geometry.B),
        "guard_source": None,
        "constraints": [] if parent is None else [{"admitted": node}],
        "initial": {
            "groups": {"0": [["1", "0"]] if parent else [["0", "0"]]},
            "cell_references": {"0": [reference]},
        },
        "steps": [
            {
                "index": 0,
                "owner": 0,
                "allowed_half_angle": ["0", "1"],
                "prior_partner_pose_covers": {},
                "complete": True,
                "rows": [{"collision_regions": []}],
            }
        ],
    }


def _setup(monkeypatch: pytest.MonkeyPatch):
    seed_ref = {"kind": "seed"}
    root_ref = {"kind": "root"}
    sources = {
        "root": _source("root", None, seed_ref),
        "le": _source("le", "root", root_ref),
        "ge": _source("ge", "root", root_ref),
    }
    plan = partition.CenterPartition(
        ("root",),
        (
            partition.Branch("le", ("le",), 0, (Q(1), Q(0), Q(2))),
            partition.Branch("ge", ("ge",), 0, (Q(-1), Q(0), Q(-2))),
        ),
    )
    monkeypatch.setattr(partition, "admit_center_partition", lambda *_: plan)
    return sources, {0: [(Q(0), Q(0))]}, {0: [{"reference": seed_ref}]}


def test_both_closed_leaves_use_the_same_accepted_root_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, groups, rows = _setup(monkeypatch)
    seen: list[tuple[str, bool, str | None, dict[int, Any] | None]] = []

    def replay(
        source: dict[str, Any],
        current_groups: dict[int, Any],
        current_rows: dict[int, Any],
        **kwargs: Any,
    ):
        node = source["node_id"]
        seen.append(
            (node, kwargs["final_node"], kwargs["parent_sha"], kwargs.get("center_planes"))
        )
        if node == "root":
            assert current_groups[0] == [(Q(0), Q(0))]
            return {0: [(Q(1), Q(0))]}, {0: [{"reference": {"kind": "root"}}]}
        assert current_groups[0] == [(Q(1), Q(0))]
        assert current_rows[0] == [{"reference": {"kind": "root"}}]
        current_groups[0].append((Q(2 if node == "le" else 3), Q(0)))
        return current_groups, current_rows

    monkeypatch.setattr(orchestrator.generic, "replay_one_node", replay)
    result: dict[str, Any] = {"mask_index": 1383, "nodes_completed": 0}
    orchestrator.replay_center_partition(
        {"mask_index": 1383, "mask": [0], "seed_sha256": "seed"},
        {},
        sources,
        groups,
        rows,
        world=[],
        mask=(0,),
        result=result,
        budget=orchestrator.geometry.Budget(time.monotonic() + 10, 100),
        workers=1,
        cover_backend="reference",
        collision_backend="reference",
    )
    assert [item[0] for item in seen] == ["root", "le", "ge"]
    assert [item[1] for item in seen] == [False, True, True]
    assert [item[2] for item in seen] == [None, "root", "root"]
    assert seen[1][3] == {0: [(Q(1), Q(0), Q(2))]}
    assert seen[2][3] == {0: [(Q(-1), Q(0), Q(-2))]}
    assert result["nodes_completed"] == 3
    assert result["branches_completed"] == ["le", "ge"]


def test_branch_cannot_reseed_from_a_changed_parent_reference(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, groups, rows = _setup(monkeypatch)
    sources["ge"]["initial"]["cell_references"]["0"] = [{"kind": "other"}]

    def replay(
        source: dict[str, Any], _groups: dict[int, Any], _rows: dict[int, Any], **_kwargs: Any
    ):
        if source["node_id"] == "root":
            return {0: [(Q(1), Q(0))]}, {0: [{"reference": {"kind": "root"}}]}
        return _groups, _rows

    monkeypatch.setattr(orchestrator.generic, "replay_one_node", replay)
    with pytest.raises(ValueError, match="branch initial state"):
        orchestrator.replay_center_partition(
            {"mask_index": 1383, "mask": [0], "seed_sha256": "seed"},
            {},
            sources,
            groups,
            rows,
            world=[],
            mask=(0,),
            result={"mask_index": 1383, "nodes_completed": 0},
            budget=orchestrator.geometry.Budget(time.monotonic() + 10, 100),
            workers=1,
            cover_backend="reference",
            collision_backend="reference",
        )
