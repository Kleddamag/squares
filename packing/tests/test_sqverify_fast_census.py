"""The clean-room verifier's mixed census, and its controls on the certificates it decides.

`devtools.sqverify_fast_census --family mixed` keeps, per retained format M or L
certificate, `sqverify-fast`'s verdict at all 201 net directions, and for a certificate
whose verified lower bound rests on that verdict, a control receipt: the original
verified again at its least-bound direction, and two mutants refused there (every mass
scaled by 99/100, and every mass scaled so that the exact capture at the least-bound
leaf's centre is at most one part in a million below 1). `campaign/result-import.md`
asks that two mutated certificates be refused by every checker that accepted the
original, with a test holding them; this is that test for `V-sqverify-fast`.

These tests read the retained receipts, the retained candidates and the evidence
register only; nothing here builds or runs the verifier. Each mutant's capture at the
centre is recomputed here from the receipt's exact capture and factor, so each refusal
is the verifier's correct answer rather than a budget running out, and one receipt's
exact capture is recomputed from the candidate by the exact evaluator written apart
from the crate.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import mixed_exact, read_raw
from sqpack.yamlio import safe_load

FOLDER = census.CENSUS_ROOT / "census-mixed"
EVIDENCE = census.PROJECT / "frontier/evidence.yaml"
VERIFIER = "V-sqverify-fast"
#: The receipt whose exact capture is recomputed here from the candidate.
RECOMPUTED = "mixed_n67_L848"
#: The `source_sha256` of builds whose crate source is the one the two reviews of 3
#: October accepted at 4ddf37d9c: `src/`, `Cargo.lock` and `build.rs` unchanged, and
#: `Cargo.toml` changed only by the gate's test profile (IR-4 of the 5 October review).
REVIEWED_SOURCES = frozenset(
    {
        "9985c465116631570c873ecc33af126adc6f14c7429a5ed44d922254d3c7f8a7",
        "7c49cf79f2408e745d5a0759caf85768d92c502bb574b95dbc12b81a36e50300",
    }
)


@cache
def cases() -> dict[str, census.Case]:
    return {case.certificate: case for case in census.mixed_cases()}


@cache
def entries() -> dict[str, Any]:
    data = json.loads((FOLDER / "census.json").read_text(encoding="utf-8"))
    value: dict[str, Any] = data["cases"]
    return value


@cache
def controls() -> dict[str, dict[str, Any]]:
    return {
        path.name.removesuffix(".control.json"): json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(FOLDER.glob("*/*.control.json"))
    }


@cache
def cited() -> dict[str, str]:
    """Each evidence entry that `V-sqverify-fast` decides, by the certificate it names."""
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    by_path = {
        str(case.candidate.relative_to(census.PROJECT)): name for name, case in cases().items()
    }
    found: dict[str, str] = {}
    for entry in register["evidence"]:
        if VERIFIER in (entry.get("verifiers") or []):
            name = by_path.get(str(entry.get("certificate")))
            assert name is not None, f"{entry['id']}: no mixed census case for its certificate"
            found[entry["id"]] = name
    return found


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_every_mixed_census_case_is_verified_at_all_201_directions() -> None:
    assert entries()
    for name, entry in entries().items():
        least = entry["least_bound_leaf_exact"]
        assert entry["status"] == "VERIFIED", name
        assert entry["returncode"] == 0, name
        assert entry["directions_verified"] == 201, name
        assert least["clears_threshold"] is True, name
        assert Fraction(least["exact_coverage"]) >= Fraction(entry["threshold"]), name
        case = cases()[name]
        assert entry["candidate_sha256"] == sha256(case.candidate), name
        receipt = FOLDER / case.packet / f"{name}.jsonl.gz"
        rows = [json.loads(line) for line in gzip.decompress(receipt.read_bytes()).splitlines()]
        directions = [row for row in rows if "r" in row]
        assert sorted(int(row["r"]) for row in directions) == list(range(201)), name
        assert all(row["verdict"] == "verified" for row in directions), name
        summary = rows[-1]
        assert summary["kind"] == "sqverify-fast-summary/v1", name
        assert summary["status"] == "VERIFIED", name


def test_every_entry_the_verifier_decides_has_a_verified_case_and_a_refused_control() -> None:
    for evidence_id, name in cited().items():
        assert entries()[name]["status"] == "VERIFIED", evidence_id
        assert name in controls(), f"{evidence_id}: no control receipt for {name}"
        assert controls()[name]["status"] == "CONTROLS_REFUSED", evidence_id


def test_every_entry_the_verifier_decides_is_within_what_its_review_accepted() -> None:
    """The per-certificate conditions of the review of 5 October (Carrying the Route).

    A certificate outside them (points or segments, another core side, net, domain or
    threshold, a fault injected, or a crate source other than the reviewed one) needs
    another review before an evidence entry may rest on its census row.
    """
    for evidence_id, name in cited().items():
        entry = entries()[name]
        premises = entry["premises"]
        n = int(premises["n"])
        assert (n, premises["L"]) == (entry["n"], entry["L"]), evidence_id
        assert premises["format"] == "M", evidence_id
        assert premises["centre_domain"] == "per-bin", evidence_id
        assert (premises["angle_count"], premises["D"], premises["B"]) == (
            201,
            "83/40000",
            "9977/10000",
        ), evidence_id
        assert Fraction(premises["mass_exact"]) == n - Fraction(1, 100000), evidence_id
        assert premises["expanded_points"] == premises["expanded_segments"] == 0, evidence_id
        assert entry["threshold"] == "1", evidence_id
        assert entry["refused_directions"] == [], evidence_id
        assert entry["build"]["source_sha256"] in REVIEWED_SOURCES, evidence_id
        assert (entry["build"]["profile"], entry["build"]["rustc"].split()[1]) == (
            "release",
            "1.98.0",
        ), evidence_id
        receipt = FOLDER / entry["packet"] / f"{name}.jsonl.gz"
        summary = json.loads(gzip.decompress(receipt.read_bytes()).splitlines()[-1])
        assert summary["fault_injected_at_box"] is None, evidence_id


@pytest.mark.parametrize("name", sorted(controls()))
def test_each_control_refuses_both_mutants_where_the_original_verifies(name: str) -> None:
    receipt = controls()[name]
    entry = entries()[name]
    case = cases()[name]
    assert receipt["kind"] == "sqverify-fast-control/v1"
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["packet"], receipt["n"], receipt["L"]) == (case.packet, case.n, case.side)
    assert receipt["candidate_sha256"] == sha256(case.candidate) == entry["candidate_sha256"]
    least = entry["least_bound_leaf_exact"]
    assert receipt["index"] == least["r"]
    assert receipt["centre"] == least["centre"]
    exact = Fraction(receipt["exact_capture_independent"])
    assert receipt["captures_agree"] is True
    assert (
        exact == Fraction(receipt["exact_capture_crate"]) == Fraction(least["exact_coverage"])
    )
    runs = {run["name"]: run for run in receipt["runs"]}
    assert set(runs) == {"original", "scaled-99-100", "near-threshold"}
    original = runs["original"]
    assert (original["returncode"], original["verdict"]) == (0, "verified")
    for mutant in ("scaled-99-100", "near-threshold"):
        run = runs[mutant]
        mutation = run["mutation"]
        factor = Fraction(mutation["factor"])
        assert Fraction(mutation["capture_at_centre"]) == exact * factor, mutant
        witness = mutation["capture_at_witness"]
        # The mutant's capture is below the threshold at the least-bound leaf's centre or
        # at the refusal's witness, so the claim the mutant makes is false there and a
        # refusal is the only correct answer.
        assert exact * factor < 1 or (witness is not None and Fraction(witness) < 1), mutant
        assert run["returncode"] == 1, mutant
        assert run["verdict"] not in (None, "verified"), mutant
    assert Fraction(runs["scaled-99-100"]["mutation"]["factor"]) == census.CONTROL_SCALE
    near = runs["near-threshold"]["mutation"]
    assert exact * Fraction(near["factor"]) <= 1 - census.NEAR_THRESHOLD


def test_one_control_capture_is_recomputed_from_the_candidate() -> None:
    """The centre's capture, and the 99/100 mutant's at its witness, from the candidate."""
    receipt = controls()[RECOMPUTED]
    raw = read_raw(cases()[RECOMPUTED].candidate)
    index = int(receipt["index"])
    x, y = (Fraction(value) for value in receipt["centre"])
    assert mixed_exact(raw, x, y, index) == Fraction(receipt["exact_capture_independent"])
    (scaled,) = (run for run in receipt["runs"] if run["name"] == "scaled-99-100")
    px, py = (Fraction(value) for value in scaled["witness"]["exact_pose"])
    capture = census.CONTROL_SCALE * mixed_exact(raw, px, py, index)
    assert capture == Fraction(scaled["mutation"]["capture_at_witness"]) < 1
