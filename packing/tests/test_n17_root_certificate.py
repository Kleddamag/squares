"""Synthetic exact controls; these never load or evaluate the retained target source."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_root_certificate as checker

SYSTEM: tuple[checker.Polynomial, checker.Polynomial] = (
    {(2, 0): 1, (0, 1): 2, (0, 0): -3},
    {(1, 0): 3, (0, 2): 1, (0, 0): -4},
)
MIDPOINT = Fraction(101, 100), Fraction(1)
RADIUS = Fraction(1, 50)


def hand_certificate() -> dict[str, Any]:
    """Every value follows from the hand-derived nonlinear H255 positive control."""
    return {
        "polynomials": [
            [[0, 0, "-3"], [0, 1, "2"], [2, 0, "1"]],
            [[0, 0, "-4"], [0, 2, "1"], [1, 0, "3"]],
        ],
        "F_mid": ["201/10000", "3/100"],
        "J_mid": [["101/50", "2"], ["3", "2"]],
        "C": [["-50/49", "50/49"], ["75/49", "-101/98"]],
        "J_box": [
            [["99/50", "103/50"], ["2", "2"]],
            [["3", "3"], ["49/25", "51/25"]],
        ],
        "M": [
            [["-2/49", "2/49"], ["-2/49", "2/49"]],
            [["-3/49", "3/49"], ["-101/2450", "101/2450"]],
        ],
        "row_norms": ["4/49", "251/2450"],
        "q": "251/2450",
        "correction": ["99/9800", "-3/19600"],
        "inclusion_bounds": ["23/1960", "1079/490000"],
    }


def test_hand_derived_nonlinear_certificate_and_signed_interval_product() -> None:
    document = hand_certificate()
    assert checker.check_quantities(document, SYSTEM, MIDPOINT, RADIUS) == document
    assert checker.multiply((Fraction(-2), Fraction(3)), (Fraction(-5), Fraction(-1))) == (
        -15,
        10,
    )
    assert checker.power((Fraction(-2), Fraction(3)), 2) == (0, 9)
    assert checker.power((Fraction(-2), Fraction(3)), 3) == (-8, 27)


def test_fixed_polynomials_match_independent_hand_expansion() -> None:
    first = {
        (1, 0): 1,
        (2, 0): -3,
        (3, 0): -1,
        (4, 0): -1,
        (0, 1): 1,
        (1, 1): -1,
        (4, 1): -1,
        (5, 1): 1,
        (1, 2): -3,
        (2, 2): 1,
        (3, 2): -1,
        (4, 2): -1,
    }
    second = {
        (3, 0): -2,
        (4, 0): -2,
        (0, 1): -1,
        (1, 1): 3,
        (2, 1): -4,
        (4, 1): 1,
        (5, 1): 1,
        (0, 2): 4,
        (1, 2): -2,
        (2, 2): -2,
        (3, 2): 2,
        (4, 2): -2,
        (0, 3): -1,
        (1, 3): -5,
        (2, 3): 4,
        (4, 3): 1,
        (5, 3): 1,
        (1, 4): 2,
        (2, 4): 2,
    }
    assert checker.n17_polynomials() == (first, second)


def test_mathematical_negative_controls() -> None:
    origin = Fraction(0), Fraction(0)
    for constant in (-2, -1):
        affine = ({(1, 0): 1, (0, 0): constant}, {(0, 1): 1})
        document = checker.quantities(affine, origin, Fraction(1))
        with pytest.raises(checker.CertificateError, match="strictly inside"):
            checker.check_quantities(document, affine, origin, Fraction(1))
    singular = ({(2, 0): 1}, {(0, 1): 1})
    with pytest.raises(checker.CertificateError, match="singular"):
        checker.quantities(singular, origin, Fraction(1))
    two_roots = ({(2, 0): 1, (0, 0): -1}, {(0, 1): 1})
    midpoint = Fraction(1, 2), Fraction(0)
    document = checker.quantities(two_roots, midpoint, Fraction(2))
    with pytest.raises(checker.CertificateError, match="contraction norm"):
        checker.check_quantities(document, two_roots, midpoint, Fraction(2))
    with pytest.raises(checker.CertificateError, match="strictly positive"):
        checker.quantities(SYSTEM, MIDPOINT, Fraction(0))


def test_all_derived_certificate_fields_are_checked() -> None:
    mutations: list[tuple[str, Any]] = [
        ("C", [["-50/49", "50/49"], ["75/49", "-50/49"]]),
        ("F_mid", ["1", "3/100"]),
        ("J_mid", [["101/50", "2"], ["3", "3"]]),
        ("J_box", [[["99/50", "103/50"], ["2", "2"]], [["3", "3"], ["49/25", "52/25"]]]),
        ("M", [[["0", "0"], ["0", "0"]], [["0", "0"], ["0", "0"]]]),
        ("row_norms", ["0", "0"]),
        ("q", "0"),
        ("correction", ["99/9800", "3/19600"]),
        ("inclusion_bounds", ["0", "0"]),
        (
            "polynomials",
            [
                [[0, 0, "-3"], [0, 1, "2"], [2, 0, "2"]],
                [[0, 0, "-4"], [0, 2, "1"], [1, 0, "3"]],
            ],
        ),
        ("q", 0.1),
        ("q", True),
        ("q", "2/4"),
        ("C", [["1"]]),
        ("J_box", [[["103/50", "99/50"], ["2", "2"]], [["3", "3"], ["49/25", "51/25"]]]),
    ]
    for field, changed in mutations:
        document = deepcopy(hand_certificate())
        document[field] = changed
        with pytest.raises(checker.CertificateError):
            checker.check_quantities(document, SYSTEM, MIDPOINT, RADIUS)


def target_envelope() -> dict[str, Any]:
    document = hand_certificate()
    document.update(
        {
            "schema": "n17-root-certificate/v1",
            "source": {
                "sha256": checker.SOURCE_SHA256,
                "path": checker.SOURCE_PATH,
                "row_to_label": checker.LABELS.copy(),
            },
            "box": {"midpoint": ["9/25", "33/100"], "radius": str(checker.RADIUS)},
            "domain": {},
            "provenance": {
                "git_commit": "0" * 40,
                "git_clean": True,
                "git_clean_scope": "tracked",
            },
            "criterion_passed": True,
            "failures": [],
        }
    )
    return document


def test_frozen_source_and_box_refusals_without_target_access() -> None:
    for field, value in (
        ("sha256", "0" * 64),
        ("path", "other.json"),
        ("row_to_label", list(range(1, 18))),
    ):
        document = target_envelope()
        document["source"][field] = value
        with pytest.raises(checker.CertificateError, match="source"):
            checker.check(document, b"not the retained source")
    for radius in ("0", "1/50", True, 0.01):
        document = target_envelope()
        document["box"]["radius"] = radius
        with pytest.raises(checker.CertificateError):
            checker.check(document, b"not the retained source")
    with pytest.raises(checker.CertificateError, match="source digest"):
        checker.check(target_envelope(), b"not the retained source")


def test_domain_guards_reject_wrong_side_reversed_and_outside_box() -> None:
    domain = {
        "t": ["9/25", "37/100"],
        "b": ["33/100", "17/50"],
        "D": ["1", "2"],
        "E": ["1", "2"],
        "L": ["1", "3"],
        "K": ["1", "2"],
        "side_guard_lower": ["0", "1"],
        "side_guard_upper": ["-1", "0"],
    }
    checker.check_domain(domain)
    for name, value in (
        ("K", ["0", "1"]),
        ("t", ["1/2", "1"]),
        ("b", ["1", "0"]),
        ("side_guard_lower", ["-1", "0"]),
        ("side_guard_upper", ["0", "1"]),
    ):
        changed = deepcopy(domain)
        changed[name] = value
        with pytest.raises(checker.CertificateError):
            checker.check_domain(changed)


def test_midpoint_and_provenance_guards_before_polynomial_evaluation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A synthetic source-reader result exercises identity guards without opening
    # or evaluating the target, whose first execution is preregistered separately.
    synthetic_midpoint = Fraction(9, 25), Fraction(33, 100)
    monkeypatch.setattr(checker, "source_midpoint", lambda _raw: synthetic_midpoint)
    document = target_envelope()
    document["box"]["midpoint"][0] = "1/3"
    with pytest.raises(checker.CertificateError, match="source midpoint"):
        checker.check(document, b"synthetic")
    for field, value in (
        ("git_commit", "no commit"),
        ("git_clean", False),
        ("git_clean", 1),
        ("git_clean_scope", "untracked"),
    ):
        document = target_envelope()
        document["provenance"][field] = value
        with pytest.raises(checker.CertificateError, match=r"Git|tracked-clean"):
            checker.check(document, b"synthetic")
    for field, value in (("criterion_passed", False), ("failures", ["failed"])):
        document = target_envelope()
        document[field] = value
        with pytest.raises(checker.CertificateError, match="producer"):
            checker.check(document, b"synthetic")


def test_cli_malformed_json_refuses_with_structured_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    certificate, source = tmp_path / "certificate.json", tmp_path / "source.json"
    source.write_text("{}", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check", str(certificate), "--source", str(source)])
    for payload in ('{"schema":1,"schema":2}', "[" * 2000 + "]" * 2000, "9" * 21000):
        certificate.write_text(payload, encoding="utf-8")
        assert checker.main() == 1
        receipt = json.loads(capsys.readouterr().out)
        assert receipt["verification_passed"] is False
        assert receipt["error"]
