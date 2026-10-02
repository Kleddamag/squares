"""Stage 4's negative controls for the rectangle-density checkers: mutations they refuse.

``campaign/result-import.md`` asks that two mutated certificates be refused by every
checker that accepted the original, with a test holding them. Tokoharu's ``verify.cpp``
(the rectangle replays of ``devtools.audit_wand125_rectangles``) and wand125's
``mixed_rotated_verify.cpp`` (the mixed replays of
``devtools.audit_wand125_point_and_mixed``) each have one retained control: a standing
certificate and two mutations of it run on one net direction, the original accepted
again there and both mutations refused. These tests read the retained receipts and the
retained certificates only; nothing here compiles or runs a checker.

Each mutation is regenerated here from the retained certificate, its digest checked
against the receipt's, and the witness centre evaluated in exact arithmetic: every
mutation leaves it covered below 1 at the control's angle, so the refusal is the
checker's correct answer rather than a budget running out.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import cache
from typing import Any

import pytest

from devtools import audit_tokoharu_density as tokoharu
from devtools import audit_wand125_point_and_mixed as mixed
from devtools import audit_wand125_rectangles as rect
from devtools.retained_data import read_retained_text

#: The first-party readers of a mixed candidate, which the audit keeps private.
semantic_digest = mixed._semantic_digest  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
measure = mixed._n50_measure  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

RECTANGLE_N = 41
MIXED_NAME = "n37"


@cache
def rectangle_receipt() -> dict[str, Any]:
    name, _side = rect.OCTOBER_1.cases[RECTANGLE_N]
    path = rect.OCTOBER_1.directory / "receipts/controls" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


@cache
def mixed_receipt() -> dict[str, Any]:
    path = mixed.MIXED[MIXED_NAME].receipts / "control.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _centre(receipt: dict[str, Any]) -> tuple[Fraction, Fraction]:
    x, y = (Fraction(value) for value in receipt["witness"]["centre"])
    return x, y


def _runs(receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["name"]: item for item in receipt["runs"]}


# --------------------------------------------------------------------------- rectangles


def test_the_rectangle_control_runs_the_least_bound_direction_under_the_shipped_flags() -> None:
    receipt = rectangle_receipt()
    packet = rect.OCTOBER_1
    name, side = packet.cases[RECTANGLE_N]
    case = packet.case_directory(packet.source, name)
    rows = [
        json.loads(line)
        for line in read_retained_text(case / "verified_angles.jsonl").splitlines()
    ]
    least = min(rows, key=lambda row: (row["lower_bound"], row["r"]))
    assert receipt["kind"] == rect.CONTROL_KIND
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["packet"], receipt["source_revision"]) == (packet.date, packet.revision)
    assert (receipt["certificate"], receipt["n"], Fraction(receipt["L"])) == (
        name,
        RECTANGLE_N,
        side,
    )
    assert receipt["direction"] == least["r"]
    assert receipt["upstream_row"] == least
    checker = receipt["checker"]
    assert checker["verify_cpp_sha256"] == rect.VERIFY_SHA256
    assert checker["runner_sha256"] == rect.RUNNER_SHA256
    assert checker["compile"] == list(rect.RUNNER_COMPILE)
    runner = (rect.CHECKER / "run_verify.py").read_text()
    assert repr(checker["compile"]).replace(", ", ",") in runner
    assert checker["argv"] == ["./verify", str(least["r"]), str(least["r"])]
    assert "subprocess.run(['./verify',str(r),str(r)]" in runner


def test_the_rectangle_original_is_accepted_with_the_upstream_results() -> None:
    receipt = rectangle_receipt()
    original = _runs(receipt)["original"]
    name, _side = rect.OCTOBER_1.cases[RECTANGLE_N]
    case = rect.OCTOBER_1.case_directory(rect.OCTOBER_1.source, name)
    published = tokoharu.load_json(case / "certificate_metadata.json")["input_sha256"]
    assert original["input_sha256"] == published
    run = original["run"]
    assert run["verdict"] == "ACCEPTED"
    assert run["matches_upstream"]
    assert run["returncode"] == 0
    assert run["command"] == receipt["checker"]["argv"]
    (row,) = run["rows"]
    assert row == json.loads(run["stdout"])
    upstream = receipt["upstream_row"]
    assert row["status"] == "verified"
    assert all(row[key] == upstream[key] for key in ("r", "nodes", "leaves", "lower_bound"))
    assert Fraction(row["lower_bound"]) >= tokoharu.TARGET


@pytest.mark.parametrize("kind", rect.MUTATIONS)
def test_each_rectangle_mutation_is_refused(kind: str) -> None:
    receipt = rectangle_receipt()
    run = _runs(receipt)[kind]["run"]
    assert run["verdict"] == "REFUSED"
    assert run["returncode"] != 0
    assert run["rows"] == []
    assert run["stderr"].startswith(f"UNRESOLVED {receipt['direction']} ")
    assert run["command"] == receipt["checker"]["argv"]


def test_the_rectangle_mutations_are_regenerated_and_provably_uncovered() -> None:
    """Each mutation's input digest, and its exact coverage at the witness, recomputed."""
    receipt = rectangle_receipt()
    runs = _runs(receipt)
    name, side = rect.OCTOBER_1.cases[RECTANGLE_N]
    case = rect.OCTOBER_1.case_directory(rect.OCTOBER_1.source, name)
    candidate = tokoharu.load_json(case / "certified_candidate.json")
    _side, shrink, _total, rects = tokoharu.density(candidate)
    r = receipt["direction"]
    c, s = rect.net_rotation(r * tokoharu.GAP)
    witness = receipt["witness"]
    assert (Fraction(witness["cos"]), Fraction(witness["sin"])) == (c, s)
    assert Fraction(witness["side"]) == shrink
    low, high = side / 2, side - shrink * (c + s) / 2
    assert [Fraction(v) for v in witness["domain"]] == [low, high]
    centre = _centre(receipt)
    assert all(low <= v <= high for v in centre)
    contributions = rect.orbit_contributions(
        rect.candidate_orbits(candidate, rects), centre, c, s, shrink
    )
    covered = sum(contributions.values(), Fraction())
    assert Fraction(witness["coverage_exact"]) == covered >= 1
    top = rect.heaviest(contributions)
    assert runs["drop-top-contributor"]["mutation"]["row"] == top
    assert (
        Fraction(runs["drop-top-contributor"]["mutation"]["contribution_at_witness_exact"])
        == (contributions[top])
    )
    upstream = receipt["upstream_row"]["lower_bound"]
    assert rect.CONTROL_FACTOR * Fraction(upstream) < 1
    assert Fraction(runs["scale-weights"]["mutation"]["factor"]) == rect.CONTROL_FACTOR
    digests = {"original": runs["original"]["input_sha256"]}
    for kind in rect.MUTATIONS:
        mutated = rect.mutate_candidate(candidate, kind, top)
        digest = hashlib.sha256(rect.input_text(mutated).encode()).hexdigest()
        assert digest == runs[kind]["input_sha256"], kind
        digests[kind] = digest
        _s, _b, mass, images = tokoharu.density(mutated)
        assert Fraction(runs[kind]["mass_exact"]) == mass < RECTANGLE_N
        at_witness = rect.coverage_exact(images, centre, c, s, shrink)
        assert Fraction(runs[kind]["witness_coverage_exact"]) == at_witness < 1, kind
    assert len(set(digests.values())) == 3


# --------------------------------------------------------------------------- mixed


@cache
def mixed_candidate() -> dict[str, Any]:
    return json.loads(mixed.mixed_retained(mixed.MIXED[MIXED_NAME])["candidate.json"])


def test_the_mixed_control_runs_the_least_bound_direction_under_the_shipped_flags() -> None:
    receipt = mixed_receipt()
    certificate = mixed.MIXED[MIXED_NAME]
    shipped = mixed.shipped_results(certificate)
    oblique = {int(key): row for key, row in shipped.items() if int(key)}
    least = min(oblique, key=lambda index: (oblique[index]["lower"], index))
    assert receipt["kind"] == mixed.MIXED_CONTROL_KIND
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["certificate"], receipt["revision"], receipt["n"]) == (
        certificate.name,
        certificate.revision,
        certificate.n,
    )
    assert receipt["directory"] == certificate.directory.as_posix()
    assert receipt["index"] == least
    record = receipt["shipped_record"]
    assert (record["nodes"], record["lower"]) == (
        oblique[least]["nodes"],
        oblique[least]["lower"],
    )
    assert record["status"] == "ANGLE_VERIFIED"
    checker = receipt["checker"]
    source = (mixed.MIXED_CODE / "mixed_rotated_verify.cpp").read_bytes()
    assert checker["source_sha256"] == hashlib.sha256(source).hexdigest()
    assert checker["argv"] == ["verify", "input.txt", str(record["nodes"])]
    shipped_compile = (mixed.MIXED_CODE / "mixed_rotated_verify.py").read_text()
    assert "['c++','-O2','-std=c++17','-ffp-contract=off','-fno-fast-math'" in shipped_compile
    assert checker["compile"].endswith("c++ -O2 -std=c++17 -ffp-contract=off -fno-fast-math")
    assert receipt["tarball"]["status"] == "TARBALL_MATCHES_PIN"
    assert receipt["tarball"]["sha256"] == mixed.tarball_pin(certificate)[0]
    assert receipt["bindings"]["status"] == "BUNDLE_BOUND_TO_PACKET"
    assert receipt["preconditions"]["status"] == "DRIVER_PRECONDITIONS_HOLD"
    assert receipt["environment"]["PYTHONOPTIMIZE"] is None


def test_the_mixed_original_is_accepted_with_the_shipped_record() -> None:
    receipt = mixed_receipt()
    original = _runs(receipt)["original"]
    assert original["candidate_digest"] == mixed.MIXED[MIXED_NAME].candidate_digest
    assert original["candidate_digest"] == semantic_digest(mixed_candidate())
    run = original["run"]
    assert run["verdict"] == "ACCEPTED"
    assert (run["returncode"], run["frontier_boxes"]) == (0, 0)
    record = receipt["shipped_record"]
    assert all(
        run["output"][key] == record[key] for key in ("status", "nodes", "leaves", "lower")
    )


@pytest.mark.parametrize("kind", mixed.MIXED_MUTATIONS)
def test_each_mixed_mutation_is_refused(kind: str) -> None:
    receipt = mixed_receipt()
    run = _runs(receipt)[kind]["run"]
    assert run["verdict"] == "REFUSED"
    assert run["returncode"] == 0
    assert run["output"]["status"] == "ANGLE_UNRESOLVED"
    assert run["frontier_boxes"] > 0
    assert run["output"]["nodes"] <= receipt["shipped_record"]["nodes"]
    # The checker stops on the first box it cannot resolve at its depth floor, which is
    # where the coverage crosses gamma at the edge of the deficit the witness proves, so
    # the exact coverage there is gamma to within the checker's own slack.
    assert run["stopped_at"] == "depth floor"
    gap = Fraction(run["stop_centre_coverage_exact"]) - Fraction(receipt["gamma"])
    assert abs(gap) < Fraction(1, 10**6)


def test_the_mixed_mutations_are_regenerated_and_provably_uncovered() -> None:
    """Each mutation's candidate digest, and its exact coverage at the witness, recomputed
    with this repository's own expansion of the measure, not the source's."""
    receipt = mixed_receipt()
    runs = _runs(receipt)
    data = mixed_candidate()
    side, core, items = measure(data)
    witness = receipt["witness"]
    c, s = rect.net_rotation(Fraction(witness["t"]))
    assert (Fraction(witness["cos"]), Fraction(witness["sin"])) == (c, s)
    assert Fraction(witness["side"]) == core
    low, high = (Fraction(v) for v in witness["domain"])
    assert low == side / 2
    centre = _centre(receipt)
    assert all(low <= v <= high for v in centre)
    images = mixed.d4_images(side, items)
    orbits = {row: images[8 * row : 8 * row + 8] for row in range(len(items))}
    contributions = rect.orbit_contributions(orbits, centre, c, s, core)  # pyright: ignore[reportArgumentType]
    covered = sum(contributions.values(), Fraction())
    assert Fraction(witness["coverage_exact"]) == covered >= Fraction(receipt["gamma"])
    top = rect.heaviest(contributions)
    assert runs["drop-top-contributor"]["mutation"]["row"] == top
    assert Fraction(runs["scale-masses"]["mutation"]["factor"]) == rect.CONTROL_FACTOR
    assert rect.CONTROL_FACTOR * Fraction(receipt["shipped_record"]["lower"]) < 1
    digests = {runs["original"]["candidate_digest"]}
    inputs = {runs["original"]["input_sha256"]}
    for kind in mixed.MIXED_MUTATIONS:
        mutated = mixed.mutate_mixed(data, kind, top)
        assert semantic_digest(mutated) == runs[kind]["candidate_digest"], kind
        digests.add(runs[kind]["candidate_digest"])
        inputs.add(runs[kind]["input_sha256"])
        _side, _core, changed = measure(mutated)
        assert sum(item[4] for item in changed) == Fraction(mutated["total_mass"])
        assert Fraction(runs[kind]["total_mass"]) == Fraction(mutated["total_mass"])
        at_witness = rect.coverage_exact(
            mixed.d4_images(side, changed),  # pyright: ignore[reportArgumentType]
            centre,
            c,
            s,
            core,
        )
        assert Fraction(runs[kind]["witness_coverage_exact"]) == at_witness < 1, kind
    assert len(digests) == len(inputs) == 3
