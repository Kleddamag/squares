"""The recent rows, their counts and each entry's standing are what the record says.

`devtools.render_recent_results` reads them for the site's overview and `RESULTS.md`
(README's three generated results tables moved to the site). These are the properties
that make them mean something: the rows are exactly the cases the record calls recent,
the verified bounds the atlas stars and the reported bounds the register's coverage gate
must hold; the counts are the rows; and standing is derived from the case records.
"""

from __future__ import annotations

import re
from fractions import Fraction

import pytest

from devtools import render_recent_results as view
from devtools.build_bound_citations import PROJECT_NAME, load_case, recent_lower_bounds
from devtools.check_results import recent_evidence

ELLIPSIS = "…"


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


@pytest.fixture(scope="module")
def rows(records: view.Records) -> list[view.Row]:
    return view.recent_rows(records)


def test_the_rows_are_the_recent_cases(records: view.Records, rows: list[view.Row]) -> None:
    """The row set is the atlas's stars plus the reported bounds the register must hold."""
    starred = {n for n in recent_lower_bounds() if n <= view.HUNDRED}
    reported = {
        n
        for n in range(1, view.HUNDRED + 1)
        if any(
            recent_evidence(records.register.evidence[item], records.sources)
            for item in load_case(n)["reported_lower_bound"]["evidence"]
        )
    }
    assert {row.n for row in rows} == starred | reported
    assert {row.n for row in rows if row.verified.recent} == starred
    assert [row.n for row in rows] == sorted(row.n for row in rows)


def test_every_recent_lane_names_its_holder_entry_lineage_and_date(
    records: view.Records, rows: list[view.Row]
) -> None:
    """Credit is the bibliography's, and the coverage gate gives each a register entry."""
    credited = {source.credited for source in records.register.sources.values()}
    for row in rows:
        for lane in (row.verified, row.reported):
            if not lane.recent:
                continue
            assert lane.holder in credited | {PROJECT_NAME}, (row.n, lane.holder)
            assert lane.results.startswith("T-"), (row.n, lane.results)
            assert lane.lineage, row.n
            assert lane.published, row.n


def test_the_counts_are_the_rows(rows: list[view.Row]) -> None:
    counts = view.recent_counts(rows)
    verified = [row for row in rows if row.verified.recent]
    assert counts.cases == len(rows)
    assert counts.verified == len(verified)
    assert counts.ours == sum(row.verified.holder == PROJECT_NAME for row in verified)
    assert counts.exact == sum(row.exact for row in verified)


@pytest.mark.parametrize(
    ("value", "shown"),
    [
        (Fraction(31, 8), "3.875"),
        (Fraction(15680, 3951), f"3.9686{ELLIPSIS}"),
        (Fraction(116511, 25000), "4.66044"),
        (Fraction(5), "5"),
        (Fraction(2, 3), f"0.6666{ELLIPSIS}"),
    ],
)
def test_decimals_are_exact_or_cut_never_rounded_up(value: Fraction, shown: str) -> None:
    assert view.digits(value) == shown


def test_standing_is_one_of_the_derived_words(records: view.Records) -> None:
    for record in records.register.results:
        assert view.standing(record, records) in view.STANDINGS, record["id"]


def test_standing_agrees_with_the_recent_rows(
    records: view.Records, rows: list[view.Row]
) -> None:
    """An entry a recent row names as a bound's holder holds a bound by `standing` too."""
    for row in rows:
        for entry in re.findall(r"T-\d{3}", row.verified.results):
            assert view.standing(records.results[entry], records) == view.HOLDS, (row.n, entry)
        if row.shows_reported and row.reported.recent:
            for entry in re.findall(r"T-\d{3}", row.reported.results):
                assert view.standing(records.results[entry], records) in {
                    view.HOLDS,
                    view.HOLDS_REPORTED,
                }, (row.n, entry)


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        # A rung of the n = 18 ladder shares its interval decision with the rung that
        # holds the bound; a shared checker does not make it hold.
        ("T-027", view.SUPERSEDED),
        # A rigidity theorem claims no bound on s(n).
        ("T-014", view.NOT_A_BOUND),
        # A second proof of s(45) = 7, whose bound Evan Daniel's cover holds.
        ("T-054", view.SECOND_CERTIFICATE),
        # A second route to s(21) = 5 that is reported and not yet replayed here.
        ("T-055", view.SECOND_CERTIFICATE_REPORTED),
    ],
)
def test_standing_is_read_from_the_case_records(
    records: view.Records, entry: str, expected: str
) -> None:
    assert view.standing(records.results[entry], records) == expected


def test_the_recent_rows_date_this_projects_bounds_by_establishment(
    records: view.Records, rows: list[view.Row]
) -> None:
    for row in rows:
        if row.verified.ours:
            entry = re.findall(r"T-\d{3}", row.verified.results)[0]
            assert row.verified.published == records.results[entry]["established"], row.n


def test_every_recent_result_by_others_has_a_relation(records: view.Records) -> None:
    for record in records.register.results:
        if view.is_recent_by_others(record):
            assert view.relation(record, records) in view.LINEAGES.values(), record["id"]
