"""A rung label in prose names a rung the result holds, or says what a rung needs.

`devtools/rung_prose.py` is the rule and `devtools/check_results.py` applies it to the
register's `claim`, `composition` and `next_rung` and to the case records. These tests
pin both directions: the stale assertion the ladder change of 2026-09-30 left behind is
refused, and a statement of what a rung requires, or of what a result once held, is not.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_results
from devtools.rung_prose import Standing, clauses, is_requirement, label_problems

#: A machine-checked result with its review record pending, and one a prose step holds
#: a rung lower than the checker derives from its strongest entry.
STANDINGS = {
    "T-001": Standing("V3", "C3", "V3", "C3"),
    "T-002": Standing("V3", "C2", "V3", "C3"),
    "T-003": Standing("V4", "C4", "V4", "C4"),
    "T-004": Standing("V0", "C0", "V3", "C3"),
}


def problems(text: str, own: str = "T-001") -> list[str]:
    return label_problems(text, STANDINGS, own=own)


@pytest.mark.parametrize(
    "text",
    [
        "Two methods decide it, so the bound stands at V4/C4.",
        "C4 is earned by two evidence entries whose method values differ.",
        "C5 is reached; V5 would need a proof-assistant port.",
        "All premises have completed exact executions, supporting V4/C5.",
        "The Lean kernel checked the theorem, so the claim is V5.",
        "The source certificate reaches C4 because two methods decide its bytes.",
    ],
)
def test_a_rung_four_or_five_the_result_does_not_hold_is_refused(text: str) -> None:
    found = problems(text)
    assert found
    assert all("which no result it is about holds" in problem for problem in found)


@pytest.mark.parametrize(
    "text",
    [
        "The result reaches V4 when the oversight record is retained.",
        (
            "V4 and C4 need two adversarial AI reviews by distinct reviewers and a human "
            "oversight record, and none is retained."
        ),
        "Rung 5 is formal: V5 requires a human expert's review of the formalization.",
        "A complete replay recorded as an interval-certified entry would derive V4/C4.",
        "It stands at V3/C3 (it held V4/C5 until 2026-09-30).",
        "One method decides the derivation, so the result is C3 and not C4.",
        "A proof-audited entry does not derive above C2, and nothing here is above C4.",
        "V5 by a proof-assistant port of the reduction.",
        "One named human expert's review of the formalization restores V5.",
    ],
)
def test_a_requirement_or_a_history_is_not_refused(text: str) -> None:
    assert problems(text) == []


def test_the_cue_must_sit_in_the_clause_of_the_label_it_excuses() -> None:
    found = problems("C5 is reached; V5 would need a proof-assistant port.")
    assert len(found) == 1
    assert found[0].startswith("asserts C5,")
    # A colon ends a clause too, so a requirement after it excuses nothing before it.
    assert problems("The claim is V5: C5 needs two experts.") != []


def test_a_result_that_holds_the_rung_may_say_so() -> None:
    assert problems("Two reviews and the oversight record are retained: V4/C4.", "T-003") == []
    assert problems("T-003 stands at V4/C4, and this corollary inherits its certificate.") == []


def test_a_lower_rung_must_be_one_the_result_declares_or_the_checker_derives() -> None:
    assert problems("Every part is machine-replayed here, so the claim is V3/C3.") == []
    found = problems("The replay yields no certificate, so the claim is V3/C2.")
    assert found == [
        (
            "asserts V3/C2, which is not the rung of any result it is about: The replay "
            "yields no certificate, so the claim is V3/C2."
        )
    ]
    assert problems("The proof itself is C1.") != []
    # The derived rung is allowed: a composition note says why the declared one is lower.
    assert problems("The checker derives C3 from the reduction's entry.", "T-002") == []
    assert problems("Confirmation is C2 by the C table.", "T-002") == []
    assert problems("The checker derives V3 and C3 from the grid's entry.", "T-004") == []


def test_a_clause_is_about_the_results_it_names() -> None:
    assert problems("The reduction, T-001, is V3/C3.", "T-002") == []
    found = problems("The reduction, T-001, is V4/C5.", "T-002")
    assert [problem.split(",")[0] for problem in found] == ["asserts V4", "asserts C5"]


def test_a_part_named_by_its_evidence_entry_is_held_only_to_the_review_rungs() -> None:
    part = "The upper half is the grid, E-basic-grid-upper, at V3/C3."
    assert label_problems(part, STANDINGS, own="T-004") == []
    assert label_problems(part.replace("V3/C3", "V1/C2"), STANDINGS, own="T-004") == []
    assert label_problems(part.replace("V3/C3", "V4/C3"), STANDINGS, own="T-004") != []


def test_a_case_clause_naming_no_result_is_about_the_results_of_its_case() -> None:
    text = "This supports `V4/C3`: the two sweeps are one event-cell method."
    assert label_problems(text, STANDINGS, fallback=["T-001"]) != []
    assert label_problems(text, STANDINGS, fallback=["T-003"]) == []
    assert label_problems(text.replace("V4", "V3"), STANDINGS, fallback=["T-001"]) == []


def test_clauses_keep_only_those_with_a_label_and_join_wrapped_lines() -> None:
    text = "The bound is exact.\nIt stands at\n`V3/C3`; C4 needs a\nhuman oversight record."
    assert clauses(text) == ["It stands at `V3/C3`", "C4 needs a human oversight record."]
    assert not is_requirement("It stands at `V3/C3`")
    assert is_requirement("C4 needs a human oversight record.")


def test_notes_are_exempt_and_the_three_fields_are_checked(tmp_path: Path) -> None:
    record = {
        "id": "T-001",
        "scope": {"n_values": [7]},
        "claim": "s(7) = 3.",
        "composition": "C4 is earned by two methods.",
        "next_rung": "C5 is reached.",
        "notes": "2026-09-30: held V4/C4 under the ladder then in force.",
    }
    case = tmp_path / "n-007.md"
    case.write_text("---\nn: 7\n---\nThe bound stands at `V4/C4`.\n", encoding="utf-8")
    found = check_results.rung_label_problems([record], STANDINGS, cases=[case])
    assert [problem.split(", which")[0] for problem in found] == [
        "T-001: composition asserts C4",
        "T-001: next_rung asserts C5",
        "n-007.md: asserts V4",
        "n-007.md: asserts C4",
    ]
    record["claim"] = "s(7) = 3, at V5."
    record["composition"] = "Both parts are machine-replayed here: C3."
    record["next_rung"] = "V4 and C4 need two adversarial AI reviews and an oversight record."
    case.write_text("---\nn: 7\n---\nThe bound stands at `V3/C3`.\n", encoding="utf-8")
    found = check_results.rung_label_problems([record], STANDINGS, cases=[case])
    assert [problem.split(", which")[0] for problem in found] == ["T-001: claim asserts V5"]


def test_the_live_register_and_case_records_assert_no_stale_rung() -> None:
    register = check_results.safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    evidence = {
        entry["id"]: entry
        for entry in check_results.safe_load(
            check_results.EVIDENCE.read_text(encoding="utf-8")
        )["evidence"]
    }
    standings = {}
    for record in register["results"]:
        cited = [evidence[ref] for ref in record["evidence"]]
        reviews = list(record.get("reviews") or [])
        standings[record["id"]] = Standing(
            record["verification"],
            record["confirmation"],
            check_results.derive_verification(cited, reviews),
            check_results.derive_confirmation(
                cited, reviews, open_review=bool(record.get("open_review"))
            ),
        )
    assert check_results.rung_label_problems(register["results"], standings) == []
