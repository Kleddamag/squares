"""Pinned A2 assignment controls; no case geometry is accepted here."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from devtools import check_n11_generic_sequential as generic
from devtools import n11_nonfield_assignment as assignment


def _case() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    manifest = generic.load_manifest(generic.MANIFEST)
    recipe = next(row for row in manifest["cases"] if row["mask_index"] == 221)
    baseline_sha = manifest["input_sha256s"]["A1"]
    baseline = generic.load_object(baseline_sha, manifest, generic.METADATA_OBJECTS)
    extension = generic.load_object(
        manifest["input_sha256s"]["A2"], manifest, generic.METADATA_OBJECTS
    )
    return recipe, baseline, extension, baseline_sha


def test_pinned_a2_single_case_assignment() -> None:
    recipe, baseline, extension, baseline_sha = _case()
    assignment.admit_a2_extension(
        221, recipe, baseline, extension, baseline_object_sha256=baseline_sha
    )


@pytest.mark.parametrize(
    ("mutator", "message"),
    [
        (lambda recipe, _baseline, _extension: recipe.update(source_sha256="0" * 64), "recipe"),
        (
            lambda _recipe, _baseline, extension: extension["extension_entries"].append(
                extension["extension_entries"][0]
            ),
            "inventory",
        ),
        (
            lambda _recipe, _baseline, extension: extension["extension_entries"][0].update(
                mask=True
            ),
            "case ID",
        ),
        (
            lambda _recipe, baseline, _extension: baseline.update(
                authoritative_snapshot_sha256="0" * 64
            ),
            "baseline binding",
        ),
        (
            lambda _recipe, _baseline, extension: extension["per_case_evidence"].update(
                {"221": []}
            ),
            "per-case evidence",
        ),
    ],
)
def test_near_miss_a2_assignments_refuse(mutator: Any, message: str) -> None:
    recipe, baseline, extension, baseline_sha = _case()
    recipe, baseline, extension = copy.deepcopy((recipe, baseline, extension))
    mutator(recipe, baseline, extension)
    with pytest.raises(ValueError, match=message):
        assignment.admit_a2_extension(
            221, recipe, baseline, extension, baseline_object_sha256=baseline_sha
        )
