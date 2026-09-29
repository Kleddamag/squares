"""README's recent-results table and the counts quoted above it cannot drift from the record.

The listing of recent lower bounds and its four counts were kept by hand and drifted
three times (`think-ti71`). `devtools.render_recent_results` now generates the table and
`devtools.check_readme` holds the counts; these are the properties that make both
checks mean something. The committed README passes, a mutated row or a mutated count
fails, and the rows are exactly the cases the record calls recent: the verified bounds
the atlas stars, and the reported bounds the register's coverage gate must hold.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from devtools import check_readme
from devtools import render_recent_results as view
from devtools.build_bound_citations import PROJECT_NAME, load_case, recent_lower_bounds
from devtools.check_results import recent_evidence

ELLIPSIS = "\u2026"


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


@pytest.fixture(scope="module")
def rows(records: view.Records) -> list[view.Row]:
    return view.recent_rows(records)


@pytest.fixture(scope="module")
def readme() -> str:
    return view.README.read_text(encoding="utf-8")


def table_rows(text: str) -> list[str]:
    """The block's data rows, as the document has them."""
    return [line for line in view.block(text).splitlines() if line.startswith("| [")]


def test_the_committed_table_is_current(readme: str, rows: list[view.Row]) -> None:
    assert not view.stale(readme, view.render_lines(rows))


def test_rendering_over_an_unchanged_tree_is_a_no_op(readme: str, rows: list[view.Row]) -> None:
    """The splice keeps the document's own bytes for every row whose content held."""
    assert view.spliced(readme, view.render_lines(rows)) == readme


def test_an_edited_row_is_stale(readme: str, rows: list[view.Row]) -> None:
    first = table_rows(readme)[0]
    edited = first.replace(" | ", " | 0", 1)
    assert edited != first
    assert view.stale(readme.replace(first, edited, 1), view.render_lines(rows))


def test_a_dropped_row_is_stale(readme: str, rows: list[view.Row]) -> None:
    last = table_rows(readme)[-1]
    assert view.stale(readme.replace(last + "\n", "", 1), view.render_lines(rows))


def test_a_document_without_one_marker_pair_is_refused(readme: str) -> None:
    with pytest.raises(ValueError, match="marker pair"):
        view.block(readme.replace(view.END, "", 1))
    with pytest.raises(ValueError, match="marker pair"):
        view.block(readme + view.BEGIN)


def test_the_committed_counts_agree(readme: str, rows: list[view.Row]) -> None:
    assert check_readme.recent_count_problems(readme, view.recent_counts(rows)) == []


@pytest.mark.parametrize("field", ["cases", "verified", "ours", "exact"])
def test_a_mutated_count_fails(readme: str, rows: list[view.Row], field: str) -> None:
    """Each of the four counts is checked, found wherever the formatter broke the line."""
    match = check_readme.RECENT_COUNT.search(readme)
    assert match is not None
    counts = view.recent_counts(rows)
    wrong = check_readme.spelled(getattr(counts, field) + 1)
    start, end = match.span(field)
    mutated = readme[:start] + wrong + readme[end:]
    problems = check_readme.recent_count_problems(mutated, counts)
    assert len(problems) == 1
    assert f"says {wrong} " in problems[0]


def test_a_deleted_count_sentence_fails(readme: str, rows: list[view.Row]) -> None:
    """A count deleted rather than corrected is a count nothing checks."""
    mutated = readme.replace("are new exact values", "are new values", 1)
    assert mutated != readme
    problems = check_readme.recent_count_problems(mutated, view.recent_counts(rows))
    assert problems
    assert "no 'N of its hundred cases" in problems[0]


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


@pytest.mark.parametrize(
    ("count", "word"),
    [(3, "three"), (20, "twenty"), (27, "twenty-seven"), (40, "forty"), (55, "fifty-five")],
)
def test_counts_are_spelled_as_the_readme_spells_them(count: int, word: str) -> None:
    assert check_readme.spelled(count) == word
