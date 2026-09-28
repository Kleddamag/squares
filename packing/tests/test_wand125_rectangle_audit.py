"""wand125's rectangle-density certificates: pin, input binding, and the bounds they carry."""

from __future__ import annotations

import json
import shutil
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import apply_wand125_rectangles as apply
from devtools import audit_tokoharu_density as tokoharu
from devtools.audit_wand125_rectangles import (
    CASES,
    PACKET,
    SOURCE,
    materialize,
    monotone_bounds,
    source_provenance,
)
from devtools.retained_data import compressed_path, read_retained_bytes
from sqpack.yamlio import safe_load

FRONTIER = Path(__file__).resolve().parents[1] / "frontier"
#: The two smallest interval inputs, so regeneration stays well inside the test ceiling.
SMALL = (21, 32)


def _payload(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n", 2)[1])["packing"]


def test_retained_subset_matches_the_pinned_tree() -> None:
    provenance = source_provenance(SOURCE)
    assert provenance["kind"] == "verified-retained-subset"
    assert provenance["upstream_files"] == 1367
    assert provenance["files_verified"] == 184


@pytest.mark.parametrize("n", SMALL)
def test_regenerated_input_is_the_published_input(n: int, tmp_path: Path) -> None:
    name, side = CASES[n]
    binding = materialize(SOURCE / "certificates" / name, tmp_path / name)
    metadata = json.loads(
        (SOURCE / "certificates" / name / "certificate_metadata.json").read_text()
    )
    assert binding["input_sha256"] == metadata["input_sha256"]
    report = tokoharu.preflight(tmp_path / name, n, side)
    assert report["status"] == "PASS"
    assert Fraction(report["mass_exact"]) == n - Fraction(1, 1000 if n in {21, 27} else 100)


def test_a_changed_weight_breaks_the_input_binding(tmp_path: Path) -> None:
    name, _side = CASES[32]
    case = tmp_path / "case"
    shutil.copytree(SOURCE / "certificates" / name, case)
    path = case / "certified_candidate.json"
    data = json.loads(read_retained_bytes(path))
    compressed_path(path).unlink()
    index = next(i for i, weight in enumerate(data["weights"]) if Fraction(weight) > 0)
    data["weights"][index] = str(Fraction(data["weights"][index]) * 2)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="published SHA-256"):
        materialize(case, tmp_path / "scratch")


def test_a_side_other_than_the_pinned_one_is_refused(tmp_path: Path) -> None:
    name, side = CASES[21]
    materialize(SOURCE / "certificates" / name, tmp_path / name)
    with pytest.raises(ValueError, match="side mismatch"):
        tokoharu.preflight(tmp_path / name, 21, side + Fraction(1, 200))


def test_monotone_transfer_reaches_n77_from_n76() -> None:
    bounds = monotone_bounds({n: side for n, (_name, side) in CASES.items()})
    assert bounds[77] == (Fraction(89, 10), 76)
    assert bounds[76] == (Fraction(89, 10), 76)
    assert all(bounds[n][1] == n for n in CASES if n != 77)


def test_preflight_receipt_covers_every_standing_certificate() -> None:
    record = json.loads((PACKET / "receipts/preflight/audit.json").read_text())
    assert record["status"] == "PASS"
    assert record["provenance"]["kind"] == "verified-retained-subset"
    assert {case["n"]: Fraction(case["L"]) for case in record["cases"]} == {
        n: side for n, (_name, side) in CASES.items()
    }
    assert all(Fraction(case["mass_exact"]) < case["n"] for case in record["cases"])


def test_replay_receipt_records_complete_accepting_runs() -> None:
    record = json.loads((PACKET / "receipts/replay/audit.json").read_text())
    preflight = {
        case["n"]: case["input_sha256"]
        for case in json.loads((PACKET / "receipts/preflight/audit.json").read_text())["cases"]
    }
    assert record["cases"]
    for case in record["cases"]:
        summary = case["replay"]["summary"]
        assert case["status"] == "PASS"
        assert summary["status"] == "VERIFIED"
        assert summary["angle_cases"] == 201
        assert summary["input_sha256"] == case["input_sha256"] == preflight[case["n"]]
        assert (
            summary["verifier_source_sha256"]
            == tokoharu.load_json(
                PACKET / "receipts/replay" / case["certificate"] / "verification_summary.json"
            )["verifier_source_sha256"]
        )
        rows = (
            PACKET / "receipts/replay" / case["certificate"] / "verified_angles.jsonl"
        ).read_text()
        assert sorted(json.loads(line)["r"] for line in rows.splitlines()) == list(range(201))


def test_frontier_records_carry_exactly_the_certified_bounds() -> None:
    """Reported lane: every standing certificate; verified lane: only replayed ones."""
    reported = monotone_bounds({n: side for n, (_name, side) in CASES.items()})
    replayed = apply.replayed()
    verified = monotone_bounds(replayed) if replayed else {}
    for n, (side, source) in reported.items():
        payload = _payload(n)
        field = payload["reported_lower_bound"]
        if n in apply.SUPERSEDED_PRIORS:
            assert field["source_key"] != apply.SOURCE_KEY
            assert apply.REPLAY not in payload["verified_lower_bound"]["evidence"]
            continue
        if n not in CASES and n != 77:
            assert Fraction(str(field["value"])) >= side
            continue
        assert Fraction(field["exact_form"]) == side
        assert field["source_key"] == apply.SOURCE_KEY
        assert field["evidence"] == [apply.REPORT if source == n else apply.MONOTONE_REPORT]
        lower = payload["verified_lower_bound"]
        if apply.REPLAY in lower["evidence"]:
            assert Fraction(lower["exact_form"]) == verified[n][0]
        else:
            assert n not in verified or Fraction(str(lower["value"])) >= verified[n][0]


def test_records_are_what_the_apply_tool_writes() -> None:
    for plan in apply.plans():
        path = FRONTIER / f"n-{plan.n:03d}.md"
        assert apply.apply_case(plan) == path.read_text(encoding="utf-8"), path.name
