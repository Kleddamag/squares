"""The September 2026 parallel upper-bound packets, their certificates and their records."""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest

from devtools import apply_upper_bound_packets as apply
from devtools import upper_bound_packets as packets
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.witness import witness_document
from sqpack.yamlio import safe_load

#: Where the certified ceiling sits above the printed side, measured on 2026-09-29.
TRAILING = {206, 259, 305}


def test_the_verified_value_is_the_larger_of_the_printed_and_certified_sides() -> None:
    assert packets.verified_value("1.25", Fraction(5, 4)) == "1.25"
    assert packets.verified_value("1.25", Fraction(124, 100)) == "1.25"
    assert packets.verified_value("1.25", Fraction(1250000001, 10**9)) == "1.26"
    assert packets.units_above("1.25", Fraction(1250000001, 10**9)) == 1
    assert packets.units_above("1.25", Fraction(124, 100)) == -1
    assert packets.exact_form("1.26") == "63/50"


def test_a_franciscouzo_file_is_read_by_its_header_and_rows() -> None:
    text = "# n = 2\n# s = 2.0\n# x y theta(rad)\n0.5 0.5 0\n1.5 0.5 0\n"
    assert packets.parse_couzo(text) == (2, "2.0", [("0.5", "0.5", "0"), ("1.5", "0.5", "0")])
    with pytest.raises(ValueError, match="rows"):
        packets.parse_couzo(text + "1.5 1.5 0\n")
    with pytest.raises(ValueError, match="franciscouzo"):
        packets.parse_couzo("# n = 2\n" + text)


def _two_squares() -> str:
    """Two unit squares side by side in a 2 x 1 box, as an exact rational witness."""
    squares = [
        {"id": 1, "corners": [["0", "0"], ["1", "0"], ["1", "1"], ["0", "1"]]},
        {"id": 2, "corners": [["1", "0"], ["2", "0"], ["2", "1"], ["1", "1"]]},
    ]
    witness = {
        "id": "W-control",
        "n": 2,
        "side": "2",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "control",
        },
        "source": {"path": "control"},
    }
    return witness_document(witness)


def test_the_negative_controls_fail_both_ways_on_a_packing_that_passes() -> None:
    text = _two_squares()
    assert packets.independent_check(text)["verification_passed"]
    shrunk = packets.independent_check(packets.shrink_side(text))
    assert not shrunk["verification_passed"]
    assert "container penetration" in shrunk["failures"][0]
    moved = packets.independent_check(packets.shift_square(text, 1, Fraction(1, 10**6)))
    assert not moved["verification_passed"]
    assert "overlapping" in moved["failures"][0]


@pytest.mark.parametrize("source", packets.SOURCES, ids=lambda source: source.id)
def test_each_retained_packet_is_consistent_with_its_receipts(source: packets.Source) -> None:
    assert packets.fast_problems(source) == []


def test_every_certificate_verifies_and_the_trailing_cases_are_the_measured_three() -> None:
    trailing = set()
    for source in packets.CERTIFIED:
        for n, row in packets.certification(source).items():
            assert row["independent"]["verification_passed"], n
            assert row["center_dilation"] == "1", n
            increase = Fraction(row["certified_side"]) - Fraction(row["printed_side"])
            assert abs(increase) < Fraction(22, 10**16) or source is packets.DE_WINTER, n
            if row["units_above_printed"] > 1:
                trailing.add(n)
    assert trailing == TRAILING


def test_the_casson_packings_are_each_larger_than_couzos() -> None:
    couzo = packets.cases(packets.FRANCISCOUZO)
    casson = packets.cases(packets.CASSON)
    assert len(casson) == 39
    assert set(casson) <= set(couzo)
    for n, case in casson.items():
        assert Decimal(case["side"]) > Decimal(couzo[n]["side"]), n


def test_the_records_are_what_the_apply_tool_writes() -> None:
    assert apply.main(["--check"]) == 0


def test_a_case_trails_its_report_exactly_where_the_certificate_does() -> None:
    for plan in apply.plans():
        case = safe_load(
            (apply.FRONTIER / f"n-{plan.n:03d}.md")
            .read_text(encoding="utf-8")
            .split("---\n")[1]
        )["packing"]
        agrees = bounds_agree_at_declared_precision(
            case["reported_upper_bound"], case["verified_upper_bound"]
        )
        assert agrees == (plan.n not in TRAILING), plan.n
        assert case["verified_upper_bound"]["evidence"] == [plan.registration.replay]
        kinds = {conflict["kind"] for conflict in case["conflicts"]}
        assert ("replay-failure" in kinds) == (plan.n in TRAILING), plan.n


def test_shared_counts_state_both_sources_dates_and_values() -> None:
    for plan in apply.plans():
        if plan.casson is None:
            continue
        body = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        flat = " ".join(body.split())
        assert f"`{plan.casson['side']}`" in flat, plan.n
        assert f"`{plan.case['history'][0]['side']}`" in flat, plan.n
        assert "22:45 UTC\u22126" in flat, plan.n
        assert "infers nothing about whether either packing derives" in flat, plan.n


def test_issue_227_dates_a_claim_only_at_the_shared_count_it_names() -> None:
    """The issue names 102 and 103; Casson reports only 103, so only 103 cites its date."""
    for plan in apply.plans():
        body = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        flat = " ".join(body.split())
        cited = "opened on 23 September 2026 at 02:48 UTC" in flat
        assert cited == (plan.n == 103), plan.n


def test_couzos_ai_statement_is_quoted_for_the_counts_it_names() -> None:
    """Issue #227 speaks of the 102 and 103 packings, never of all 49."""
    for plan in apply.plans():
        if plan.registration.source is not packets.FRANCISCOUZO:
            continue
        body = (apply.FRONTIER / f"n-{plan.n:03d}.md").read_text(encoding="utf-8")
        flat = " ".join(body.split())
        quoted = "found the 102 and 103 packings \u201cwith the help of Claude\u201d"
        assert quoted in flat, plan.n
        assert "itself states no AI assistance" in flat, plan.n
        assert "found the packings" not in flat, plan.n
