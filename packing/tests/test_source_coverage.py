"""Selected overrides may come from any retained source, and every reparsed claim is held."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from devtools import check_source_coverage as coverage_check


def _coverage() -> dict[str, Any]:
    def source(identifier: str, values: list[int]) -> dict[str, Any]:
        return {
            "id": identifier,
            "scope": {"n_values": values},
            "evidence": [f"E-{identifier}-report"],
        }

    return {
        "case_corpus": {"n_min": 1, "n_max": 10},
        "sources": [
            source("release", [5, 6]),
            source("repository", [5, 7]),
            source("superseded", [7]),
        ],
        "selected_overrides": [
            {"n": 6, "source_id": "release", "value": "2.9", "evidence": "E-release-report"},
            {
                "n": 5,
                "source_id": "repository",
                "value": "2.8",
                "evidence": "E-repository-report",
            },
            {
                "n": 7,
                "source_id": "repository",
                "value": "2.95",
                "evidence": "E-repository-report",
            },
        ],
        "superseded_reports": [
            {"n": 5, "source_id": "release", "value": "2.85", "superseded_by": "repository"},
            {"n": 7, "source_id": "superseded", "value": "2.97", "superseded_by": "repository"},
        ],
        "beyond_horizon_claims": [],
    }


KINGBIRD = {5: "2.9", 6: "3", 7: "3"}
CLAIMS = {
    "release": {5: "2.85", 6: "2.9"},
    "repository": {5: "2.8", 7: "2.95"},
    "superseded": {7: "2.97"},
}


def _errors(coverage: dict[str, Any], claims: dict[str, dict[int, str]] = CLAIMS) -> list[str]:
    return coverage_check.selection_errors(coverage, KINGBIRD, claims)


def test_overrides_from_several_sources_reconcile() -> None:
    assert _errors(_coverage()) == []


def test_an_override_must_print_what_its_source_prints() -> None:
    coverage = _coverage()
    coverage["selected_overrides"][1]["value"] = "2.81"
    assert any("repository prints 2.8" in error for error in _errors(coverage))


def test_an_override_must_beat_the_catalogue_baseline() -> None:
    coverage = _coverage()
    claims = copy.deepcopy(CLAIMS)
    claims["release"][6] = "3"
    coverage["selected_overrides"][0]["value"] = "3"
    assert any("does not beat the catalogue" in error for error in _errors(coverage, claims))


def test_a_superseded_report_must_lose_to_the_selected_source() -> None:
    coverage = _coverage()
    coverage["superseded_reports"][0]["value"] = "2.75"
    claims = copy.deepcopy(CLAIMS)
    claims["release"][5] = "2.75"
    assert any("is not beaten" in error for error in _errors(coverage, claims))
    coverage = _coverage()
    coverage["superseded_reports"][0]["superseded_by"] = "superseded"
    assert any("not the selected source" in error for error in _errors(coverage))


def test_every_reparsed_claim_is_accounted_for() -> None:
    coverage = _coverage()
    del coverage["superseded_reports"][1]
    assert any("unaccounted [7]" in error for error in _errors(coverage))


def test_an_override_outside_its_sources_scope_is_refused() -> None:
    coverage = _coverage()
    coverage["selected_overrides"][2]["n"] = 8
    assert any("outside repository's scope" in error for error in _errors(coverage))


def test_both_claims_record_shapes_are_reparsed(tmp_path: Path) -> None:
    release = tmp_path / "results.json"
    release.write_text(json.dumps({"results": [{"n": 5, "offered_side": "2.85"}]}))
    assert coverage_check.load_claims(release) == {5: "2.85"}
    acquisition = tmp_path / "sources.json"
    acquisition.write_text(
        json.dumps(
            {
                "format": coverage_check.ACQUISITION_FORMAT,
                "sources": [{"cases": [{"n": 7, "side": "2.95"}]}],
            }
        )
    )
    assert coverage_check.load_claims(acquisition) == {7: "2.95"}


def test_the_recorded_coverage_reconciles() -> None:
    assert coverage_check.main() == 0
