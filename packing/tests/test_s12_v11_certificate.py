"""The import of jlevy/squares#363: squarepacker's v1.1 ``s(12) >= 7943/2000`` certificate.

squarepacker (Ryu Sungjoon) reports ``s(12) >= 7943/2000`` from Evan Daniel's 1,736
points dilated to the container ``7943/2000`` and re-weighted by linear programming.
These tests hold what was decided here:

- the exact preflight, re-run from the retained bytes, passes every check and equals its
  retained receipt;
- three checkers accepted the certificate at ``N = 96000``: Daniel's ``verify`` built with
  overflow checks and the reporter's ``indep_check.cpp`` (both the producer's code, run
  here) and this repository's native parent-core branch and bound (first party), every
  row of it;
- the reporter's two controls, regenerated here and pinned by digest, were refused by
  each of the three; and
- the native case is pinned to the certificate the issue names.

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

from devtools import audit_s12_v11_certificate as preflight
from devtools import verify_evand_angle_net_native as native
from devtools.retained_data import read_retained_text

RECEIPTS = preflight.PACKET / "receipts"
CONTROLS = RECEIPTS / "controls"
W = 10_000_000


@cache
def audit() -> dict[str, Any]:
    return preflight.audit()


def _lines(path: Path) -> list[str]:
    return read_retained_text(path).splitlines()


def _body(path: Path) -> str:
    return "\n".join(line for line in _lines(path) if not line.startswith("# "))


def _footer(path: Path) -> str:
    return _lines(path)[-1]


def test_preflight_passes_every_exact_check_and_equals_its_receipt() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert all(result["checks"].values()), result["checks"]
    retained = json.loads((RECEIPTS / "preflight.json").read_text(encoding="utf-8"))
    assert retained == result
    assert result["side"] == "7943/2000"
    assert result["dilation"] == "31382793/31360000"
    assert result["advance_over_route_b"] == "10266889/7898846000"
    assert result["total_weight"] == "119974808/10000000"
    assert result["orbits"] == 223
    assert Fraction(result["max_coordinate_deviation"]) <= Fraction(11, 39200000)


def test_the_certificate_is_the_one_the_issue_names() -> None:
    assert preflight.CERTIFICATE_SHA256 == (
        "e2f326b28142cf22402f88357f4c7fe4680a08a32ae785b493adac335bcc2685"
    )
    case = native.CASES["s12-v11"]
    assert case.sha256 == preflight.CERTIFICATE_SHA256
    assert case.path == preflight.CERTIFICATE
    assert (case.n, case.net, case.source_bin) == (12, 96000, 0)
    assert case.source_minimum == f"{preflight.REPORTED_MINIMUM}/{W}"
    assert case.source_commit == "7a96bec36bc6811c3715ef581598f22ff9b7ba3a"


@pytest.mark.parametrize("name", preflight.CONTROLS)
def test_each_control_is_regenerated_with_the_digest_its_receipts_name(name: str) -> None:
    _, cert = preflight.read(preflight.CERTIFICATE, preflight.CERTIFICATE_SHA256)
    data = preflight.controls(cert)[name].render()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == preflight.REPORTER_CONTROLS[name][1]
    assert audit()["controls"][name]["sha256"] == digest
    receipt = json.loads((CONTROLS / f"native-{name}.json").read_text(encoding="utf-8"))
    assert receipt["provenance"]["certificate_sha256"] == digest
    paths = [
        *CONTROLS.glob(f"daniel-verify-N96000-{name}-*.log"),
        CONTROLS / f"indep-check-N96000-{name}.log",
    ]
    for path in paths:
        assert digest[:8] in _lines(path)[1], path


def test_the_lowered_orbit_control_must_be_refused() -> None:
    """The corner square's 58 points include two of the lowered orbit."""
    assert preflight.REPORTED_MINIMUM - 2 * preflight.ORBIT_STEP < W


def test_daniels_verifier_with_overflow_checks_accepts_at_96000() -> None:
    path = RECEIPTS / "daniel-verify-ovf-N96000.log"
    header = _lines(path)[1]
    assert "CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=true" in header
    assert "VERIFY_" not in header
    body = _body(path)
    assert "D4-symmetric atom set: true" in body
    assert "angles: k=0..39765 (N=96000)" in body
    assert "min covered weight over ALL placements = 10000050/10000000" in body
    assert "(at angle k=0)" in body
    assert "VERIFIED: every CLOSED unit square inside C covers weight >= 1" in body
    assert "FAIL" not in body
    assert "NOT VERIFIED" not in body
    assert "PARTIAL" not in body
    assert "exit 0" in _footer(path)
    log = read_retained_text(preflight.SOURCE / "logs/3.9715/daniel_verify_ovf_N96000.log")
    assert body.strip() == log.strip()


@pytest.mark.parametrize("net", [96000, 192000])
def test_the_reporters_checker_accepts_and_matches_its_log(net: int) -> None:
    path = RECEIPTS / f"indep-check-N{net}.log"
    body = _body(path)
    assert f"min captured weight over all bins = {preflight.REPORTED_MINIMUM}/{W}" in body
    assert body.splitlines()[-1].startswith("VERIFIED")
    assert "exit 0" in _footer(path)
    log = read_retained_text(preflight.SOURCE / f"logs/3.9715/indep_check_N{net}.log")
    assert body.strip() == log.strip()


@cache
def native_receipt() -> dict[str, Any]:
    return json.loads(read_retained_text(RECEIPTS / "native-parent-core-N96000.json"))


def test_the_native_decision_is_complete_and_its_tree_is_recorded() -> None:
    """The run's tree was its commit plus untracked paths, which the receipt flags as
    dirty; the status captured at launch names them, and no tracked file differed."""
    receipt = native_receipt()
    assert receipt["status"] == "PASS_COMPLETE"
    assert receipt["case"] == "s12-v11"
    assert receipt["net"] == 96000
    assert receipt["points"] == 1736
    assert receipt["complete"] is True
    assert receipt["refutations"] == []
    status = _lines(RECEIPTS / "native-parent-core-N96000.git-status.txt")
    assert status[0] == f"# HEAD {receipt['provenance']['git_commit']}"
    assert all(line.startswith("?? ") for line in status[1:]), status
    assert receipt["provenance"]["dirty"] is (len(status) > 1)
    assert receipt["provenance"]["certificate_sha256"] == preflight.CERTIFICATE_SHA256
    assert receipt["catalogue_rows"] == len(native.net_rows(96000)) == 39765
    lines = read_retained_text(RECEIPTS / "native-parent-core-N96000.rows.jsonl").splitlines()
    rows = [json.loads(line) for line in lines[1:]]
    assert sorted(r["index"] for r in rows) == list(range(receipt["catalogue_rows"]))
    for row in rows:
        assert row["status"] == "certified"
        assert row["stalled"] == 0
        assert not row["budget_exhausted"]
        assert int(row["lower"]) >= receipt["threshold_units"]


@pytest.mark.parametrize("name", preflight.CONTROLS)
def test_every_checker_refuses_each_control(name: str) -> None:
    indep = CONTROLS / f"indep-check-N96000-{name}.log"
    body = _body(indep)
    assert body.splitlines()[-1] == "NOT VERIFIED"
    least = re.search(r"min captured weight over all bins = (\d+)/10000000", body)
    assert least is not None
    assert int(least.group(1)) < W
    assert "exit 1" in _footer(indep)

    daniel = CONTROLS / f"daniel-verify-N96000-{name}-bin-0.log"
    body = _body(daniel)
    fails = [int(v) for v in re.findall(r"FAIL at angle k=0: covered (\d+)/10000000", body)]
    assert fails
    assert all(v < W for v in fails)
    assert "NOT VERIFIED" in body
    assert "\nVERIFIED" not in body

    receipt = json.loads((CONTROLS / f"native-{name}.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "UNRESOLVED"
    assert receipt["case"] == "s12-v11"
    assert receipt["net"] == 96000
    assert receipt["provenance"]["certificate_sha256"] != preflight.CERTIFICATE_SHA256
    row0 = next(row for row in receipt["rows"] if row["index"] == 0)
    assert row0["status"] == "refuted"
    witnesses = receipt["refutations"]
    assert witnesses
    assert all(w["admissible"] and Fraction(w["charge"]) < 1 for w in witnesses)
