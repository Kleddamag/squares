"""Controls for `devtools.compare_site_floors`, on tables small enough to read.

The comparison reports, for each n, how a published floor stands to the record's
verified and reported lower bounds, and whether a ``register: verified`` mark names a
value the verified lane holds. These tests hold the three relations, the exact
comparison of rationals, the tolerance for the rest, the mark check and the family
rings, and that the retained receipt is what the command writes today.
"""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from devtools.compare_site_floors import (
    ABOVE,
    ABSENT,
    BELOW,
    SAME,
    Bound,
    compare,
    family_rows,
    read_table,
    relation,
    summary,
)

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/evand-square-packing-2026-10-04"


def _case(verified: str | None, reported: str | None = None) -> dict[str, object]:
    def bound(text: str | None) -> dict[str, str] | None:
        if text is None:
            return None
        if "/" in text:
            num, den = text.split("/")
            return {"value": str(Decimal(num) / Decimal(den)), "exact_form": text}
        return {"value": text, "exact_form": text}

    return {"verified_lower_bound": bound(verified), "reported_lower_bound": bound(reported)}


def test_rationals_compare_exactly_and_other_forms_to_the_tolerance() -> None:
    verified = Bound(Decimal("4.8975"), "1959/400")
    reported = Bound(Decimal("4.9"), "49/10")
    assert relation(verified, Bound(Decimal("4.8975"), "1959/400")) == SAME
    assert relation(reported, verified) == ABOVE
    assert relation(verified, reported) == BELOW
    root = Bound(Decimal("4.47213595499958"), "sqrt(20)")
    assert relation(root, Bound(Decimal("4.4721359549"), None)) == SAME
    assert relation(root, Bound(Decimal("4.4721"), None)) == ABOVE
    assert relation(root, None) == ABSENT


def test_a_verified_mark_on_a_value_the_verified_lane_lacks_is_reported() -> None:
    table = {
        "20": {"best": {"value": 4.8975, "exact_form": "1959/400", "register": "verified"}},
        "96": {"best": {"value": 10.0, "exact_form": "10", "register": "verified"}},
        "97": {"best": {"value": 10.0, "exact_form": "10"}},
        "meta": {"description": "not a count"},
    }
    cases = {20: _case("1959/400", "49/10"), 96: _case("249/25", "10"), 97: _case("10", "10")}
    rows = compare(table, cases)
    assert [row["n"] for row in rows] == [20, 96, 97]
    totals = summary(rows)
    assert totals["mark_not_held"] == [96]
    assert totals["above_verified"] == [96]
    assert totals["above_both_lanes"] == []
    assert totals["verified_reported"] == {"above/same": 1, "same/below": 1, "same/same": 1}


def test_a_family_count_is_held_only_when_its_verified_floor_is_k() -> None:
    cases = {78: _case("9"), 96: _case("249/25"), 97: _case("10"), 99: _case("10")}
    rows = family_rows({3: 9, 4: 10}, cases, above=77)
    assert [(row["n"], row["held"]) for row in rows] == [(78, True), (97, True), (96, False)]


def test_the_retained_receipt_reads_the_retained_table() -> None:
    """The receipt is dated: it names the table it read, and a later record may differ."""
    receipt = json.loads((PACKET / "receipts/site_floors_compare.json").read_text("utf-8"))
    table, digest = read_table(PACKET / "square-packing/site/www/data/lower_bounds.json")
    assert receipt["format"] == "site-floor-comparison-v1"
    assert receipt["table_sha256"] == digest
    assert len(receipt["rows"]) == sum(key.isdigit() for key in table) == 100
