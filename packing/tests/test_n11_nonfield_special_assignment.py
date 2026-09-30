"""Special audit metadata carries source identities, never geometry authority."""

from __future__ import annotations

import copy
import gzip
import json

import pytest

from devtools import n11_nonfield_special_assignment as assignment


def fixture(case):
    manifest = json.loads(
        gzip.decompress(
            (
                assignment.geometry.PACKET / "receipts/nonfield-manifest/manifest.json.gz"
            ).read_bytes()
        )
    )
    recipe = next(item for item in manifest["cases"] if item["mask_index"] == case)
    baseline = {"authoritative_snapshot_sha256": "a" * 64}
    audit = {
        "status": "UNTRUSTED_ASSERTION",
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
        "mask_index": case,
        "mask": recipe["mask"],
        "parent_Uplus": str(assignment.geometry.U),
        "parent_side": str(assignment.geometry.B),
    }
    nodes = recipe["ordered_ancestry_proposal"]
    if case == 1383:
        audit.update(
            tree_sha256=recipe["source_sha256"],
            root_sha256=recipe["seed_sha256"],
            cover_sha256=assignment.geometry.COVER_SHA,
            required_antecedent_mask=recipe["mask"],
            transferred_canonical_mask_indices=[case],
            nodes=[
                {"node": node["node_id"], "sha256": node["source_sha256"]} for node in nodes
            ],
        )
    else:
        audit.update(
            source_sha256=recipe["source_sha256"],
            baseline_sha256=baseline["authoritative_snapshot_sha256"],
            checked_ancestry=[{"sha256": nodes[0]["source_sha256"]}],
            necessary_halfplanes_checked=len(nodes[0]["constraints_proposal"]),
        )
    return recipe, audit, baseline


@pytest.mark.parametrize("case", [1383, 2175, 2176])
def test_metadata_binding_does_not_import_reported_success(case) -> None:
    recipe, audit, baseline = fixture(case)
    assignment.admit_special_audit(recipe, audit, baseline)
    changed = copy.deepcopy(audit)
    changed["status"] = "PASS"
    changed["mask_exclusion_proved"] = True
    assignment.admit_special_audit(recipe, changed, baseline)
    changed["mask_index"] = case + 1
    with pytest.raises(ValueError, match="case or frame"):
        assignment.admit_special_audit(recipe, changed, baseline)


@pytest.mark.parametrize("case", [1383, 2175, 2176])
def test_different_source_cannot_reuse_special_audit(case) -> None:
    recipe, audit, baseline = fixture(case)
    audit["tree_sha256" if case == 1383 else "source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="source"):
        assignment.admit_special_audit(recipe, audit, baseline)


def test_center_partition_cannot_omit_an_ancestry_node() -> None:
    recipe, audit, baseline = fixture(1383)
    audit["nodes"].pop()
    with pytest.raises(ValueError, match="source"):
        assignment.admit_special_audit(recipe, audit, baseline)
