"""The import of jlevy/squares#309: squarepacker's rescaled ``s(12)`` certificate.

squarepacker (Ryu Sungjoon) reports ``s(12) >= 31360/7901`` from Evan Daniel's
1,736-point certificate (``T-049``) with every coordinate and the container multiplied by
``7902/7901``. These tests hold what was decided here:

- the exact preflight, re-run from the retained bytes, passes every check and equals its
  retained receipt;
- three checkers accepted the certificate at ``N = 24000``: Daniel's ``verify`` and the
  reporter's ``indep_check.cpp`` (both the producer's code, run here) and this
  repository's native parent-core branch and bound (first party), every row of it;
- two mutated certificates, regenerated here and pinned by digest, were refused by each
  of the three; and
- the native reader still decides Daniel's own case at ``N = 6000`` row for row as before.

They read receipts and retained files only; nothing here compiles or runs a checker.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_s12_rescaled_certificate as preflight
from devtools import verify_evand_angle_net_native as native
from devtools.retained_data import read_retained_text

RECEIPTS = preflight.PACKET / "receipts"
CONTROLS = RECEIPTS / "controls"
W = 10_000_000


@cache
def audit() -> dict[str, Any]:
    return preflight.audit()


def _body(path: Path) -> str:
    return "\n".join(
        line for line in read_retained_text(path).splitlines() if not line.startswith("# ")
    )


def _footer(path: Path) -> str:
    return read_retained_text(path).splitlines()[-1]


def _command(path: Path) -> str:
    return read_retained_text(path).splitlines()[0]


def test_preflight_passes_every_exact_check_and_equals_its_receipt() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert all(result["checks"].values()), result["checks"]
    retained = json.loads((RECEIPTS / "preflight.json").read_text(encoding="utf-8"))
    assert retained == result
    assert result["side"] == "31360/7901"
    assert result["factor"] == "7902/7901"
    assert result["advance"] == "15680/31216851"
    assert result["total_weight"] == "119738036/10000000"


def test_the_certificate_is_the_one_the_issue_names() -> None:
    assert preflight.CERTIFICATE_SHA256 == (
        "6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578"
    )
    assert native.CASES["s12-rescaled"].sha256 == preflight.CERTIFICATE_SHA256
    assert native.CASES["s12"].sha256 == preflight.DANIEL_SHA256


@pytest.mark.parametrize("name", preflight.CONTROLS)
def test_each_control_is_regenerated_with_the_digest_its_receipts_name(name: str) -> None:
    _, cert = preflight.read(preflight.CERTIFICATE, preflight.CERTIFICATE_SHA256)
    data = preflight.controls(cert)[name].render()
    digest = hashlib.sha256(data).hexdigest()
    assert audit()["controls"][name]["sha256"] == digest
    assert preflight.d4_invariant(preflight.parse(data))
    receipt = json.loads((CONTROLS / f"native-{name}.json").read_text(encoding="utf-8"))
    assert receipt["provenance"]["certificate_sha256"] == digest
    for checker in ("indep-check-N24000", "daniel-verify-N24000"):
        (path,) = CONTROLS.glob(f"{checker}-{name}*.log")
        assert digest[:8] in _command(path) + read_retained_text(path).splitlines()[1]


def test_the_lowered_weights_control_must_be_refused() -> None:
    """Every weight down 57/10^7 puts the reported least pose at most 9999999/10^7."""
    assert preflight.WEIGHT_STEP == 57
    assert preflight.REPORTED_MINIMUM - preflight.WEIGHT_STEP < W


def test_daniels_verifier_accepts_at_24000_with_the_reported_minimum() -> None:
    path = RECEIPTS / "daniel-verify-N24000.log"
    body = _body(path)
    assert "D4-symmetric atom set: true" in body
    assert "angles: k=0..9942 (N=24000)" in body
    assert "min covered weight over ALL placements = 10000056/10000000" in body
    assert "(at angle k=0)" in body
    assert "VERIFIED: every CLOSED unit square inside C covers weight >= 1" in body
    assert "FAIL" not in body
    assert "NOT VERIFIED" not in body
    assert "VERIFY_" not in read_retained_text(path).splitlines()[1]
    assert "exit 0" in _footer(path)


def test_the_reporters_checker_accepts_at_24000_and_matches_its_log() -> None:
    path = RECEIPTS / "indep-check-N24000.log"
    body = _body(path)
    assert "min captured weight over all bins = 10000056/10000000" in body
    assert body.splitlines()[-1].startswith("VERIFIED")
    assert "exit 0" in _footer(path)
    log = read_retained_text(preflight.SOURCE / "logs/indep_check_N24000.log")
    assert body.strip() == log.strip()


@cache
def native_receipt() -> dict[str, Any]:
    return json.loads(read_retained_text(RECEIPTS / "native-parent-core-N24000.json"))


def test_the_native_decision_is_complete_and_clean() -> None:
    receipt = native_receipt()
    assert receipt["status"] == "PASS_COMPLETE"
    assert receipt["case"] == "s12-rescaled"
    assert receipt["net"] == 24000
    assert receipt["complete"] is True
    assert receipt["refutations"] == []
    assert receipt["provenance"]["dirty"] is False
    assert receipt["provenance"]["certificate_sha256"] == preflight.CERTIFICATE_SHA256
    assert receipt["catalogue_rows"] == len(native.net_rows(24000)) == 9942
    lines = read_retained_text(RECEIPTS / "native-parent-core-N24000.rows.jsonl").splitlines()
    rows = [json.loads(line) for line in lines[1:]]
    assert sorted(r["index"] for r in rows) == list(range(receipt["catalogue_rows"]))
    for row in rows:
        assert row["status"] == "certified"
        assert row["stalled"] == 0
        assert not row["budget_exhausted"]
        assert int(row["lower"]) >= receipt["threshold_units"]


@pytest.mark.parametrize("name", preflight.CONTROLS)
def test_every_checker_refuses_each_control(name: str) -> None:
    (indep,) = CONTROLS.glob(f"indep-check-N24000-{name}.log")
    body = _body(indep)
    assert body.splitlines()[-1] == "NOT VERIFIED"
    least = re.search(r"min captured weight over all bins = (\d+)/10000000", body)
    assert least is not None
    assert int(least.group(1)) < W
    assert "exit 1" in _footer(indep)

    (daniel,) = CONTROLS.glob(f"daniel-verify-N24000-{name}-bins-*.log")
    body = _body(daniel)
    fails = [int(v) for v in re.findall(r"FAIL at angle k=\d+: covered (\d+)/10000000", body)]
    assert fails
    assert all(v < W for v in fails)
    assert "NOT VERIFIED" in body
    assert "\nVERIFIED" not in body

    receipt = json.loads((CONTROLS / f"native-{name}.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "UNRESOLVED"
    assert receipt["case"] == "s12-rescaled"
    assert receipt["net"] == 24000
    assert receipt["provenance"]["certificate_sha256"] != preflight.CERTIFICATE_SHA256
    assert all(row["status"] == "refuted" for row in receipt["rows"])
    witnesses = receipt["refutations"]
    assert len(witnesses) == len(receipt["rows"])
    assert all(w["admissible"] and Fraction(w["charge"]) < 1 for w in witnesses)


def test_the_native_reader_still_decides_daniels_case_at_6000() -> None:
    case = native.CASES["s12"]
    assert (case.net, case.source_commit) == (6000, native.SOURCE_COMMIT)
    assert len(native.net_rows(case.net)) == 2486
    certificate = native.load_case(case)
    assert len(certificate.rows) == 2486
    assert certificate.outer_side == preflight.DANIEL_SIDE
    assert certificate.rows[0].core_side == native.sigma(0, 6000)
