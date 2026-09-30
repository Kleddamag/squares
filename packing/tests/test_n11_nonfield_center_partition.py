"""The special center split covers equality and cannot reuse one branch twice."""

from __future__ import annotations

import copy
import gzip
import json
from fractions import Fraction as Q

import pytest

from devtools import n11_nonfield_center_partition as partition


def fixture():
    manifest = json.loads(
        gzip.decompress(
            (
                partition.geometry.PACKET / "receipts/nonfield-manifest/manifest.json.gz"
            ).read_bytes()
        )
    )
    recipe = next(item for item in manifest["cases"] if item["mask_index"] == 1383)
    declarations = recipe["ordered_ancestry_proposal"]
    sources = {}
    for index, node in enumerate(declarations):
        parent_index = 4 if index == 7 else index - 1
        sources[node["source_sha256"]] = {
            "node_id": node["node_id"],
            "mask_index": 1383,
            "mask": recipe["mask"],
            "source": {"sha256": recipe["seed_sha256"]},
            "U": str(partition.geometry.U),
            "B": str(partition.geometry.B),
            "guard_source": None,
            "parent": {"sha256": declarations[parent_index]["source_sha256"]}
            if index
            else None,
            "constraints": copy.deepcopy(node["constraints_proposal"]),
        }
    return recipe, copy.deepcopy(recipe["partition_proposal"]), sources


def test_two_closed_halves_share_only_the_accepted_unconstrained_ancestry() -> None:
    recipe, tree, sources = fixture()
    plan = partition.admit_center_partition(recipe, tree, sources)
    assert len(plan.common_sources) == 5
    le, ge = plan.branches
    assert (len(le.sources), len(ge.sources)) == (2, 1)
    assert le.owner == ge.owner == 13
    assert le.plane == tuple(-value for value in ge.plane)
    boundary = le.plane[2]
    for y in (boundary - Q(1, 10**80), boundary, boundary + Q(1, 10**80)):
        assert any(branch.plane[1] * y <= branch.plane[2] for branch in plan.branches)
    assert all(branch.plane[1] * boundary == branch.plane[2] for branch in plan.branches)


def test_changed_halfspace_cannot_leave_an_unchecked_gap() -> None:
    recipe, tree, sources = fixture()
    leaf = sources[tree["nodes"]["r.ge"]["receipt"]["sha256"]]
    cut = leaf["constraints"][0]
    cut["upper_field"] = str(Q(cut["upper_field"]) - Q(1, 10**80))
    with pytest.raises(ValueError, match="exact closed halfspace"):
        partition.admit_center_partition(recipe, tree, sources)


def test_branch_cannot_inherit_the_other_halfspace_state() -> None:
    recipe, tree, sources = fixture()
    sources[tree["nodes"]["r.ge"]["receipt"]["sha256"]]["parent"] = {
        "sha256": tree["nodes"]["r.le"]["receipt"]["sha256"]
    }
    with pytest.raises(ValueError, match="share a constrained state"):
        partition.admit_center_partition(recipe, tree, sources)


def test_cycles_and_unproved_guards_are_refused() -> None:
    recipe, tree, sources = fixture()
    first = next(iter(sources))
    sources[first]["parent"] = {"sha256": first}
    with pytest.raises(ValueError, match="cyclic"):
        partition.admit_center_partition(recipe, tree, sources)
    recipe, tree, sources = fixture()
    sources[next(iter(sources))]["guard_source"] = {"assume": "producer guard"}
    with pytest.raises(ValueError, match="guard"):
        partition.admit_center_partition(recipe, tree, sources)


def test_one_leaf_cannot_stand_for_both_sides() -> None:
    recipe, tree, sources = fixture()
    tree["nodes"]["r"]["split"]["children"]["ge"] = "r.le"
    with pytest.raises(ValueError, match="split grammar"):
        partition.admit_center_partition(recipe, tree, sources)
