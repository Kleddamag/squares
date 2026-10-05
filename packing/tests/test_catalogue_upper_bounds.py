"""The exact certificates of the catalogue's packings at n = 69, 83 and 87 (T-088, T-089)."""

from __future__ import annotations

import json
from fractions import Fraction

from devtools import catalogue_upper_bounds as catalogue
from devtools import upper_bound_packets as packets
from sqpack.witness import load_witness


def test_the_certificates_and_receipts_agree() -> None:
    assert catalogue.fast_problems() == []


def test_each_certificate_is_its_witness_promoted_and_lies_above_the_printed_side() -> None:
    """The printed sides are truncated decimals, so every certificate is above its own."""
    for n, row in catalogue.certification().items():
        certificate = load_witness(
            catalogue.certificate_path(n), fallback_schema=catalogue.WITNESS_SCHEMA
        )
        assert certificate["id"] == f"W-known-best-n{n:03d}-rational", n
        assert certificate["certificate"]["derived_from"] == f"W-known-best-n{n:03d}", n
        assert certificate["source"]["path"] == f"witnesses/known-best/n-{n:03d}.yaml", n
        side = Fraction(row["certified_side"])
        assert Fraction(row["printed_side"]) < Fraction(row["witness_side"]) < side, n
        assert side - Fraction(row["printed_side"]) < Fraction(1, 10**12), n
        assert row["units_above_printed"] > 1, n
        assert row["witness_revision"].startswith("evand/square-packing@"), n


def test_both_negative_controls_are_refused_by_both_checkers() -> None:
    """Two mutations of the n = 69 certificate, decided again here rather than read back."""
    text = catalogue.certificate_path(catalogue.CONTROL_N).read_text(encoding="utf-8")
    assert packets.independent_check(text)["verification_passed"]
    shrunk = packets.shrink_side(text)
    moved = packets.shift_square(text, catalogue.CONTROL_SHIFT_SQUARE, Fraction(1, 10**6))
    for mutated, failure in ((shrunk, "container penetration"), (moved, "overlapping")):
        verdict = packets.independent_check(mutated)
        assert not verdict["verification_passed"]
        assert failure in verdict["failures"][0]
        assert not catalogue.exact_verify_passed(mutated)
    recorded = json.loads(catalogue.CONTROLS.read_text(encoding="utf-8"))["controls"]
    assert [row["control"] for row in recorded] == [
        "side-shrunk-1e-15",
        f"square-{catalogue.CONTROL_SHIFT_SQUARE}-shifted-1e-6",
    ]
