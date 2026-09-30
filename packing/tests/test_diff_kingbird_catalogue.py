"""Two transcriptions of the catalogue compare count by count, not line by line."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools.diff_kingbird_catalogue import (
    compare,
    main,
    markdown_table,
    readings,
    record_standings,
    summary,
)

PREAMBLE = (
    "Squares in Squares\n\n"
    "If a pictured packing has multiple numbers in its label above, the picture "
    "represents the largest; each smaller is represented by removing any square. "
    "For the $n ≤ 12$ not pictured, the trivial packing (with no tilted squares) is "
    "the best known packing.\n\n"
)

BEFORE = PREAMBLE + (
    "5\n[](square-5.svg)\n\n"
    "$s = 2 + {1\\over 2}\\sqrt 2 = \\Nn{2.70710678118654}$  \n"
    "[Rigid.](squares_in_squares__rigid.html)  \n"
    "Proved by Frits Göbel  \nin early 1979.\n\n"
    "7, 8\n[](square-8.svg)\n\n$s = 3$  \nProved by Erich Friedman  \nin 1999.\n\n"
    "11\n[](square-11.svg)\n\n"
    "$s = \\Nn{3.87708359002281}$  \n"
    "Found by Walter Trump  \nin 1979.\n"
)

#: The same page after one improvement, one rewrap, one new picture, and one withdrawn
#: rigidity annotation: `n = 11` moves, `n = 5` only loses its annotation, `n = 7, 8`
#: rewraps a sentence without changing it, and `n = 10` gains its first picture.
AFTER = PREAMBLE + (
    "5\n[](square-5.svg)\n\n"
    "$s = 2 + {1\\over 2}\\sqrt 2 = \\Nn{2.70710678118654}$  \n"
    "Proved by Frits Göbel in early 1979.\n\n"
    "7, 8\n[](square-8.svg)\n\n$s = 3$  \nProved by Erich Friedman in 1999.\n\n"
    "10\n[](square-10.svg)\n\n"
    "$s = 3 + {1\\over 2}\\sqrt 2 = \\Nn{3.70710678118654}$  \n"
    "Found by Frits Göbel in early 1979.\n\n"
    "11\n[](square-11.svg)\n\n"
    "$s = 3.8770835900228$  \n"
    "Found by Walter Trump  \nin 1979.  \n"
    "Improved by Somebody Else in September 2026.  \n"
    "Not yet analytically optimized.\n"
)


def test_an_unpictured_count_reads_as_the_grid_the_page_promises() -> None:
    covered = readings(BEFORE)

    assert set(covered) == set(range(1, 13))
    assert covered[10].pictured is False
    assert covered[10].side == "4"
    assert covered[7].side == covered[8].side == "3"
    assert covered[7].listed_n == (7, 8)


def test_each_changed_count_is_reported_with_the_fields_that_moved() -> None:
    changes = {change.n: change for change in compare(BEFORE, AFTER)}

    assert sorted(changes) == [5, 10, 11]
    assert changes[5].fields == ("catalogue_rigid", "credits")
    assert changes[10].fields[0] == "side"
    assert changes[10].direction == "lower"
    assert changes[10].before is not None
    assert changes[10].before.pictured is False
    assert changes[11].direction == "lower"
    assert "side" in changes[11].fields


def test_a_rewrapped_sentence_is_not_a_change_and_an_added_one_is_verbatim() -> None:
    """The first sentence of `n = 11` loses its line break and keeps its words."""
    (change,) = [change for change in compare(BEFORE, AFTER) if change.n == 11]

    assert change.added_credits == (
        "Improved by Somebody Else in September 2026",
        "Not yet analytically optimized",
    )
    assert change.removed_credits == ()


def test_a_bare_printed_decimal_is_the_side_and_not_a_closed_form() -> None:
    (change,) = [change for change in compare(BEFORE, AFTER) if change.n == 11]

    assert change.after is not None
    assert change.after.side == "3.8770835900228"
    assert change.after.exact_form is None


def test_a_record_holding_a_better_side_is_set_apart_from_one_the_page_now_beats() -> None:
    changes = compare(BEFORE, AFTER)
    cases = {
        10: {"reported_upper_bound": {"value": "4", "source_key": "[Kingbird]"}},
        11: {"reported_upper_bound": {"value": "3.8", "source_key": "[Elsewhere]"}},
    }
    standings = record_standings(changes, cases)

    assert standings[10].relation == "below"
    assert standings[11].relation == "above"
    assert summary(changes, standings=standings)["side_against_record"] == {
        "below": [10],
        "above": [11],
    }
    table = markdown_table(changes, standings=standings)
    assert "| 11 | `3.87708359002281` | `3.8770835900228` |" in table
    assert "`3.8` [Elsewhere], catalogue above" in table


def test_the_cli_compares_two_files_and_prints_the_record(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    before, after, frontier = tmp_path / "before.md", tmp_path / "after.md", tmp_path / "f"
    before.write_text(BEFORE, encoding="utf-8")
    after.write_text(AFTER, encoding="utf-8")
    frontier.mkdir()

    status = main(
        [
            "--before-file",
            str(before),
            "--after-file",
            str(after),
            "--frontier",
            str(frontier),
            "--json",
        ]
    )

    assert status == 0
    document = json.loads(capsys.readouterr().out)
    assert document["summary"]["side_changed"] == 2
    assert [change["n"] for change in document["changes"]] == [5, 10, 11]
