"""The document map's summaries: required where the overview shows a card, and bound-free.

`check_documentation` holds every summary to one sentence of at most `SUMMARY_LIMIT`
characters that states no bound. What stating a bound means is `states_a_bound`'s, and
the cases below are its definition by example: a value of `s` related to a number, a
number related to `s`, an inequality beside a number, and the forms a side length takes
(a decimal, a fraction, a radical). A case named by an integer is not a bound.
"""

from __future__ import annotations

from typing import Any

import pytest

from devtools.check_documentation import (
    SUMMARY_LIMIT,
    states_a_bound,
    summary_faults,
    summary_problems,
)
from devtools.reader_documents import REPO, RESULTS, START, load_map
from sqpack.yamlio import safe_load

SCHEMA = REPO / "docs" / "project" / "document-map.schema.yaml"


@pytest.mark.parametrize(
    ("text", "shape"),
    [
        ("proves s(11) ≥ 3", "a relation of s(…) to a number"),
        ("shows s(32) = 6 by a second method", "a relation of s(…) to a number"),
        ("s(21) is 5 and s(45) is 7", "a relation of s(…) to a number"),
        ("s(11) is at least four", None),
        ("s(11) is at least 4", "a relation of s(…) to a number"),
        (r"raises $s(11) \ge 4$", "a relation of s(…) to a number"),
        (r"$s(11) \;\ge\; \frac{31}{8}$", "a relation of s(…) to a number"),
        ("s (17) > 4", "a relation of s(…) to a number"),
        ("4 < s(11)", "a number in relation to s(…)"),
        ("where 5 = s(21)", "a number in relation to s(…)"),
        ("a container side ≥ 4", "an inequality with a number"),
        ("the case n = 11 > 3", "an inequality with a number"),
        (r"a side \approx 4", "an inequality with a number"),
        ("a side <= 4", "an inequality with a number"),
        ("the bound 3.8269975…", "a decimal"),
        ("a side of 31/8", "a fraction"),
        (r"a side of \frac{31}{8}", "a fraction"),
        ("a side of 2 + √2", "a radical"),
        (r"a side of 2 + \sqrt{2}", "a radical"),
        ("a side of 2 + sqrt(2)", "a radical"),
    ],
)
def test_a_statement_of_a_bound_is_found_and_named(text: str, shape: str | None) -> None:
    found = states_a_bound(text)
    assert (found[0] if found else None) == shape, found


@pytest.mark.parametrize(
    "text",
    [
        "what s(n) means and how the problem is posed",
        "every tracked case through n = 324",
        "the cases n = 1…100 and n = 101…324",
        "the v0.4 proof edition and its v0.4.2 successor",
        "results T-026 and T-037, and hypothesis H-161",
        "the BC303 T2 charge bridge and the X027 helpers",
        "packing twenty-six unit squares, and the case of 11 squares",
        "the V4/C5 rungs and the S5 score",
        "from s(1) to s(100)",
        "the 1984 memoranda and their 66 checkpoint steps",
    ],
)
def test_a_summary_that_names_cases_and_identifiers_states_no_bound(text: str) -> None:
    assert states_a_bound(text) is None


@pytest.mark.parametrize(
    ("summary", "fault"),
    [
        ("A survey of annealing for square packing." * 5, "characters, over"),
        ("A survey of annealing. It covers engines.", "one sentence"),
        ("A survey of annealing without a full stop", "one sentence"),
        ("A survey of annealing\nover two lines.", "one sentence"),
        ("A survey that proves s(11) ≥ 3.8.", "states a bound"),
    ],
)
def test_a_summary_is_one_short_sentence_and_states_no_bound(summary: str, fault: str) -> None:
    faults = summary_faults(summary)
    assert any(fault in text for text in faults), faults


def test_a_well_formed_summary_has_no_fault() -> None:
    assert summary_faults("A survey of annealing for square packing, n = 1…100.") == []


def _map(**summaries: Any) -> dict[str, Any]:
    documents = []
    for path in (*START, *RESULTS):
        entry = {"path": path, "role": "orientation", "authority": "current"}
        entry["lifecycle"] = "maintained"
        summary = summaries.get(path, "Covers the document.")
        if summary is not None:
            entry["summary"] = summary
        documents.append(entry)
    return {"documents": documents}


def test_a_shown_document_needs_a_summary_and_an_unshown_one_does_not() -> None:
    document_map = _map(**{"README.md": None})
    document_map["documents"].append(
        {"path": "notes.md", "role": "plan", "authority": "current", "lifecycle": "transient"}
    )
    assert summary_problems(document_map) == [
        "README.md: the overview lists it, so its map entry needs a summary"
    ]


def test_a_shown_document_the_map_does_not_record_is_a_problem() -> None:
    document_map = _map()
    document_map["documents"] = document_map["documents"][1:]
    assert summary_problems(document_map) == [
        "README.md: the overview lists it, but the document map does not"
    ]


def test_a_bound_in_any_summary_is_a_problem_shown_or_not() -> None:
    document_map = _map(**{"epistemics.md": "How s(11) ≥ 3.8 is classified."})
    document_map["documents"].append(
        {
            "path": "notes.md",
            "role": "plan",
            "authority": "current",
            "lifecycle": "transient",
            "summary": "A plan for the case at 31/8.",
        }
    )
    problems = summary_problems(document_map)
    assert [problem.split(":")[0] for problem in problems] == ["epistemics.md", "notes.md"]
    assert all("states a bound" in problem for problem in problems)


def test_the_maps_summaries_pass_and_the_schema_agrees_on_the_limit() -> None:
    assert summary_problems(load_map()) == []
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    summary = schema["$defs"]["document"]["properties"]["summary"]
    assert summary["maxLength"] == SUMMARY_LIMIT
    assert "summary" not in schema["$defs"]["document"]["required"]
