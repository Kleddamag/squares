"""README's three results tables and the counts quoted above them cannot drift from the record.

The listing of recent lower bounds and its four counts were kept by hand and drifted
three times (`think-ti71`), and New Results and Results by Others were a paragraph of
prose per result. `devtools.render_recent_results` now generates all three tables and
`devtools.check_readme` holds the counts; these are the properties that make both
checks mean something. The committed README passes, a mutated row, a dropped row or a
mutated count fails, and the rows are exactly what the record says they are: every
result of this project, every recent result by others, and the cases the record calls
recent, the verified bounds the atlas stars and the reported bounds the register's
coverage gate must hold.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from fractions import Fraction
from typing import Any

import pytest

from devtools import check_readme
from devtools import render_recent_results as view
from devtools.build_bound_citations import (
    NOVEL,
    PROJECT_NAME,
    RECENT_SINCE,
    load_case,
    recent_lower_bounds,
)
from devtools.check_results import recent_evidence
from devtools.render_results import OUTPUT as RESULTS_VIEW
from devtools.render_results import credit_line

ELLIPSIS = "\u2026"
DASH = "\u2013"
REGISTER_TABLES = (view.NEW, view.OTHERS)


@pytest.fixture(scope="module")
def records() -> view.Records:
    return view.load_records()


@pytest.fixture(scope="module")
def rows(records: view.Records) -> list[view.Row]:
    return view.recent_rows(records)


@pytest.fixture(scope="module")
def readme() -> str:
    return view.README.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def blocks(records: view.Records) -> dict[view.Block, list[str]]:
    return view.rendered(records)


def table_rows(text: str, which: view.Block = view.RECENT) -> list[str]:
    """A block's data rows, as the document has them: every table line after the rule."""
    lines = [line for line in view.block(text, which).splitlines() if line.startswith("|")]
    return lines[2:]


def row_id(row: str) -> str:
    """The `T-NNN` a register table row is about."""
    match = re.search(r"\[(T-\d{3})\]\(", row)
    assert match is not None, row
    return match.group(1)


def cells(row: str) -> list[str]:
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", row)[1:-1]]


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


# --- the register tables: New Results and Results by Others ---


def test_every_committed_block_is_current(
    readme: str, blocks: dict[view.Block, list[str]]
) -> None:
    for which in view.BLOCKS:
        assert not view.stale(readme, blocks[which], which), which.name


def test_rendering_every_block_over_an_unchanged_tree_is_a_no_op(
    readme: str, blocks: dict[view.Block, list[str]]
) -> None:
    """The formatter curls quotes inside the rows; the splice keeps the document's bytes."""
    text = readme
    for which in view.BLOCKS:
        text = view.spliced(text, blocks[which], which)
    assert text == readme


@pytest.mark.parametrize("which", REGISTER_TABLES, ids=lambda which: which.name)
def test_a_hand_edited_register_row_is_stale(
    readme: str, blocks: dict[view.Block, list[str]], which: view.Block
) -> None:
    first = table_rows(readme, which)[0]
    edited = first.replace(" | ", " | 0", 1)
    assert edited != first
    assert view.stale(readme.replace(first, edited, 1), blocks[which], which)


@pytest.mark.parametrize("which", REGISTER_TABLES, ids=lambda which: which.name)
def test_a_register_entry_missing_from_its_table_is_stale(
    readme: str, blocks: dict[view.Block, list[str]], which: view.Block
) -> None:
    last = table_rows(readme, which)[-1]
    assert view.stale(readme.replace(last + "\n", "", 1), blocks[which], which)


@pytest.mark.parametrize("which", REGISTER_TABLES, ids=lambda which: which.name)
def test_a_register_table_without_its_marker_pair_is_refused(
    readme: str, which: view.Block
) -> None:
    with pytest.raises(ValueError, match=f"{which.name} marker pair"):
        view.block(readme.replace(which.end, "", 1), which)


def test_a_novel_result_dropped_from_new_results_fails_the_readme_check(
    readme: str, records: view.Records
) -> None:
    """Rule 6 of `check_readme` holds the generated table too, not only the prose."""
    section = readme[readme.index("## New Results") : readme.index("## Results by Others")]
    row = next(
        row
        for row in table_rows(readme, view.NEW)
        if len(re.findall(rf"\b{row_id(row)}\b", section)) == 1
    )
    problems = check_readme.result_coverage_problems(
        readme.replace(row + "\n", "", 1), [dict(item) for item in records.register.results]
    )
    assert problems == [f"README.md: New Results does not name novel result {row_id(row)}"]


def test_new_results_carry_every_result_of_this_project_once(
    readme: str, records: view.Records
) -> None:
    ids = [row_id(row) for row in table_rows(readme, view.NEW)]
    novel = {str(r["id"]) for r in records.register.results if r["novelty"] in NOVEL}
    assert sorted(ids) == sorted(novel)
    assert len(ids) == len(set(ids))


def test_new_results_read_highest_significance_first_then_newest(
    readme: str, records: view.Records
) -> None:
    keys = [
        (
            records.results[row_id(row)]["significance"]["score"],
            str(records.results[row_id(row)]["established"]),
        )
        for row in table_rows(readme, view.NEW)
    ]
    assert keys == sorted(keys, reverse=True)


def test_results_by_others_carry_every_recent_entry_by_others_once(
    readme: str, records: view.Records
) -> None:
    ids = [row_id(row) for row in table_rows(readme, view.OTHERS)]
    recent = {
        str(record["id"])
        for record in records.register.results
        if record.get("attribution")
        and str(record["attribution"]["published"]) >= RECENT_SINCE.isoformat()
    }
    assert sorted(ids) == sorted(recent)
    assert len(ids) == len(set(ids))
    dates = [str(records.results[item]["attribution"]["published"]) for item in ids]
    assert dates == sorted(dates, reverse=True)


def _results_view_credits() -> dict[str, str]:
    """The credit column of every attributed row in `RESULTS.md`, by id."""
    printed: dict[str, str] = {}
    for line in RESULTS_VIEW.read_text(encoding="utf-8").splitlines():
        row = cells(line) if line.startswith("| T-") else []
        if len(row) == 9:
            printed[row[0]] = row[2]
    return printed


def test_results_by_others_credit_as_the_register_view_credits(
    readme: str, records: view.Records
) -> None:
    """One credit line per result in README and `RESULTS.md`, read from the bibliography."""
    printed = _results_view_credits()
    for row in table_rows(readme, view.OTHERS):
        entry = row_id(row)
        credit, relation = cells(row)[4:6]
        assert credit == credit_line(records.results[entry], records.sources), entry
        assert credit == printed[entry], entry
        assert relation in view.LINEAGES.values(), entry


def _standings(text: str) -> dict[str, str]:
    """Each register table row's standing cell, by id: the eighth column of both."""
    return {
        row_id(row): cells(row)[7]
        for which in REGISTER_TABLES
        for row in table_rows(text, which)
    }


def test_standing_is_one_of_the_derived_words(readme: str) -> None:
    assert set(_standings(readme).values()) <= set(view.STANDINGS)


def test_standing_agrees_with_the_per_case_table(readme: str, rows: list[view.Row]) -> None:
    """An entry the per-case table names as a bound's holder holds a bound here too."""
    standings = _standings(readme)
    for row in rows:
        for entry in re.findall(r"T-\d{3}", row.verified.results):
            if entry in standings:
                assert standings[entry] == view.HOLDS, (row.n, entry)
        if row.shows_reported and row.reported.recent:
            for entry in re.findall(r"T-\d{3}", row.reported.results):
                if entry in standings:
                    assert standings[entry] in {view.HOLDS, view.HOLDS_REPORTED}, (row.n, entry)


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


def test_the_per_case_table_dates_this_projects_bounds_by_establishment(
    records: view.Records, rows: list[view.Row]
) -> None:
    for row in rows:
        if row.verified.ours:
            entry = re.findall(r"T-\d{3}", row.verified.results)[0]
            assert row.verified.published == records.results[entry]["established"], row.n


@pytest.mark.parametrize(
    ("values", "cell"),
    [
        ([11], "[11](packing/frontier/n-011.md)"),
        ([20, 21], "20, 21"),
        ([17, 18, 19], f"17{DASH}19"),
        ([11, 26, 27, 28, 29, 30, 31], f"11, 26{DASH}31"),
        ([27, 28, 31, 32], "27, 28, 31, 32"),
        ([26, 29, 39, 40, 41, 52, 53, 55, 56, 68, 69, 70, 71, 72], f"14 in 26{DASH}72"),
    ],
)
def test_an_n_cell_links_one_case_and_shortens_many(values: list[int], cell: str) -> None:
    assert view.cases_cell(values) == cell


def test_a_records_cell_numbers_its_links_only_where_there_are_several() -> None:
    record: Mapping[str, Any] = {
        "artifacts": [
            "packing/resources/web/a-2026-09-22/README.md",
            "packing/resources/web/a-2026-09-22/sub/README.md",
            "docs/project/reviews/review-one.md",
            "packing/devtools/tool.py",
        ],
        "review_artifact": "docs/project/reviews/review-two.md",
    }
    assert view.records_cell(record) == (
        "[packet](packing/resources/web/a-2026-09-22/README.md) \u00b7 "
        "[review 1](docs/project/reviews/review-one.md) \u00b7 "
        "[review 2](docs/project/reviews/review-two.md)"
    )
