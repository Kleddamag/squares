"""Evan Daniel's exact certificates (T-098): the reader, the conversion and the receipts.

`devtools.evand_exact_certificates` reads a certificate format no checker here read
before, converts it without rounding and hands it to this repository's two exact
checkers. These tests hold the reader to the format, the conversion to the meaning the
source's own checkers give it, the deciders to refusing what must be refused, and the
committed receipts and records to the retained certificates.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from devtools import apply_exact_optima, apply_upper_bound_packets
from devtools import check_rational_witness_independent as independent
from devtools import evand_exact_certificates as certificates
from devtools.check_source_coverage import load_claims
from sqpack.witness import exact_verify

#: Two axis-parallel unit squares side by side, 1e-20 apart, in a box 1e-20 wider than
#: they need, and a third rotated by t = 1/3 well clear of both.
SMALL = (
    "# a test certificate\n"
    "3 400000000000000000001/100000000000000000000\n"
    "1/2 1/2 0\n"
    "150000000000000000001/100000000000000000000 1/2 0\n"
    "2 5/2 1/3\n"
)


def _small() -> certificates.Certificate:
    return certificates.parse(SMALL)


def _verdicts(certificate: certificates.Certificate) -> tuple[bool, bool]:
    first, _ = exact_verify(certificates.basis_witness(certificate))
    second = independent.check_squares(
        certificates.corner_squares(certificate), certificate.side
    )
    return bool(first["verification_passed"]), bool(second["verification_passed"])


def test_the_reader_takes_the_format_and_ignores_comments() -> None:
    certificate = _small()
    assert certificate.n == 3
    assert certificate.side == Fraction(400000000000000000001, 100000000000000000000)
    assert certificate.poses[2].t == Fraction(1, 3)


@pytest.mark.parametrize(
    "text",
    [
        "2 4\n1/2 1/2 0\n",  # a row missing
        "1 4\n1/2 1/2 0\n3 3 0\n",  # a row the source's checkers would ignore
        "1 4\n1/2 1e0 0\n",  # an exponent, which Fraction reads and the format does not name
        "1 4\n1/2 1_0 0\n",  # an underscore, likewise
        "1.0 4\n1/2 1/2 0\n",  # a count that is not an integer
        "1 -4\n1/2 1/2 0\n",  # a side that is not positive
        "1 4\n1/2 1/2\n",  # a row without its tangent
    ],
)
def test_the_reader_refuses_what_the_format_does_not_state(text: str) -> None:
    with pytest.raises(certificates.CertificateError):
        certificates.parse(text)


def test_the_header_must_name_the_count_the_file_is_for() -> None:
    with pytest.raises(certificates.CertificateError, match="file name"):
        certificates.parse(SMALL, expected_n=4)


@pytest.mark.parametrize(
    "t", [Fraction(0), Fraction(1, 3), Fraction(-7, 5), Fraction(10**30, 3)]
)
def test_the_tangent_gives_a_unit_basis_exactly(t: Fraction) -> None:
    c, s = certificates.Pose(Fraction(0), Fraction(0), t).basis
    assert c * c + s * s == 1


def test_the_corners_are_the_rotation_the_source_checkers_use() -> None:
    """``(x + c a - s b, y + s a + c b)`` for ``a, b = ±1/2``, as both of the source's
    checkers build them: at t = 1, a quarter turn, the square maps onto itself."""
    pose = certificates.Pose(Fraction(3), Fraction(5), Fraction(1, 3))
    c, s = pose.basis
    assert (c, s) == (Fraction(4, 5), Fraction(3, 5))
    half = Fraction(1, 2)
    assert pose.corners()[0] == (3 + c * half - s * half, 5 + s * half + c * half)
    quarter = certificates.Pose(Fraction(0), Fraction(0), Fraction(1))
    assert sorted(quarter.corners()) == sorted(
        certificates.Pose(Fraction(0), Fraction(0), Fraction(0)).corners()
    )


def test_both_deciders_accept_a_valid_certificate() -> None:
    assert _verdicts(_small()) == (True, True)


def test_both_deciders_refuse_each_control() -> None:
    certificate = _small()
    overlapped, row = certificates.overlap_control(certificate)
    assert row["squares"] == [0, 1]
    assert _verdicts(overlapped) == (False, False)
    (past, past_row), (one, one_row) = certificates.shrink_controls(certificate)
    assert past_row["expect"] == "refused"
    assert _verdicts(past) == (False, False)
    # The box has 1e-20 to spare, far more than one unit of its denominator.
    assert one_row["expect"] == "accepted"
    assert _verdicts(one) == (True, True)


def test_the_serialized_certificate_reads_back_as_itself() -> None:
    certificate = _small()
    assert certificates.parse(certificates.serialize(certificate)) == certificate


def test_the_held_count_is_never_read(tmp_path: Path) -> None:
    (tmp_path / "n-17.cert").write_text("this is never parsed\n", encoding="utf-8")
    (tmp_path / "n-3.cert").write_text(SMALL, encoding="utf-8")
    assert certificates.certificate_counts(tmp_path) == [3]
    with pytest.raises(certificates.CertificateError, match="held"):
        certificates.check_one(str(tmp_path / "n-17.cert"))


def test_a_side_that_terminates_is_written_out_in_full() -> None:
    assert certificates.terminating_decimal(Fraction(1, 8)) == "0.125"
    assert certificates.terminating_decimal(Fraction(1, 3)) is None


def test_the_committed_receipts_agree_with_the_packet() -> None:
    assert certificates.receipt_problems() == []


def test_the_smallest_retained_certificate_is_decided_exactly() -> None:
    path = certificates.certificate_path(certificates.CERTS, 68)
    row = certificates.decide(
        certificates.parse(path.read_text(encoding="utf-8"), expected_n=68)
    )
    assert row["exact_verify"]["passed"]
    assert row["independent"]["passed"]


def test_the_claims_record_is_the_retained_certificates() -> None:
    """`check_source_coverage` reads the packet's certificate directory as its claims:
    the 48 improving counts, each at the side its header gives, written out in full."""
    claims = load_claims(certificates.CERTS)
    assert sorted(claims) == sorted(certificates.IMPROVING)
    assert claims[211] == apply_exact_optima.side_text(211)


def test_the_earlier_evidence_is_the_packets_and_the_catalogues() -> None:
    packets = {
        identifier
        for registration in apply_upper_bound_packets.REGISTRATIONS
        for identifier in (
            registration.report,
            registration.replay,
            registration.interval_replay,
        )
    }
    assert (
        packets
        | {
            "E-kingbird-upper-register",
            "E-kingbird-grid-completeness",
        }
        == apply_exact_optima.EARLIER_UPPER
    )


@pytest.mark.parametrize("n", [68, 126, 206, 211])
def test_the_records_are_the_layer_applied_to_themselves(n: int) -> None:
    path = apply_exact_optima.FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    normalized = apply_upper_bound_packets.normalized
    assert normalized(apply_exact_optima.apply_case(n, text)) == normalized(text)


def test_the_coverage_record_is_the_layer_applied_to_itself() -> None:
    text = apply_exact_optima.COVERAGE.read_text(encoding="utf-8")
    assert apply_exact_optima.coverage_text(text) == text
