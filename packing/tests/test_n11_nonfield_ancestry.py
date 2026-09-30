"""The child-node bridge accepts only an independently retained parent state."""

from __future__ import annotations

import copy
from fractions import Fraction as Q

import pytest

from devtools import check_n11_optimality_field_mask0 as geometry
from devtools import n11_nonfield_ancestry as ancestry


def _fixture():
    parent_sha = "a" * 64
    seed_sha = "b" * 64
    reference = {"kind": "phase3", "node": "root", "step": 0, "row": 0}
    groups = {0: [(Q(), Q()), (Q(1), Q())]}
    rows = {0: [{"reference": reference, "interval": ["0", "1"], "outer_domain": []}]}
    child = {
        "parent": {"sha256": parent_sha, "path": "/untrusted/parent.json"},
        "mask_index": 7,
        "mask": [0],
        "U": str(geometry.U),
        "B": str(geometry.B),
        "source": {"sha256": seed_sha},
        "constraints": [],
        "guard_source": None,
        "initial": {
            "groups": {"0": [["0", "0"], ["1", "0"]]},
            "cell_references": {"0": [reference]},
        },
    }
    return child, groups, rows, parent_sha, seed_sha


def _admit(child, groups, rows, parent_sha, seed_sha):
    return ancestry.admit_child_state(
        child,
        parent_source_sha256=parent_sha,
        seed_sha256=seed_sha,
        case_id=7,
        mask=(0,),
        accepted_groups=groups,
        accepted_rows=rows,
    )


def test_child_inherits_exact_accepted_parent_state_as_isolated_snapshot() -> None:
    child, groups, rows, parent_sha, seed_sha = _fixture()
    next_groups, next_rows = _admit(child, groups, rows, parent_sha, seed_sha)
    assert next_groups == groups
    assert next_rows == rows
    next_rows[0][0]["outer_domain"].append(["2", "2"])
    assert rows[0][0]["outer_domain"] == []


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda child: child["parent"].update(sha256="0" * 64), "parent source hash"),
        (lambda child: child["source"].update(sha256="0" * 64), "case/seed"),
        (
            lambda child: child["initial"]["groups"]["0"].append(["2", "0"]),
            "owned group",
        ),
        (
            lambda child: child["initial"]["cell_references"]["0"][0].update(row=1),
            "pose references",
        ),
    ],
)
def test_child_must_bind_parent_hash_seed_groups_and_references(mutation, message) -> None:
    child, groups, rows, parent_sha, seed_sha = _fixture()
    changed = copy.deepcopy(child)
    mutation(changed)
    with pytest.raises(ValueError, match=message):
        _admit(changed, groups, rows, parent_sha, seed_sha)
