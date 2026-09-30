"""Exact closed-angle predecessor refinement controls."""

from __future__ import annotations

import copy

import pytest

from devtools import n11_nonfield_refinement as refinement


def _fixture():
    left = {"reference": {"row": 0}, "interval": ["0", "1/2"]}
    right = {"reference": {"row": 1}, "interval": ["1/2", "1"]}
    proposed = [
        {"interval": ["0", "1/4"], "prior_reference": {"row": 0}},
        {"interval": ["1/4", "1/2"], "prior_reference": {"row": 0}},
        {"interval": ["1/2", "1"], "prior_reference": {"row": 1}},
    ]
    return proposed, [left, right]


def test_refinement_is_complete_and_resolves_exact_predecessors() -> None:
    proposed, accepted = _fixture()
    prior = refinement.complete_refinement(proposed, accepted, max_rows=3)
    assert prior == [accepted[0], accepted[0], accepted[1]]


@pytest.mark.parametrize(
    ("index", "interval", "message"),
    [
        (1, ["3/8", "1/2"], "gap"),
        (1, ["1/8", "1/2"], "overlap"),
        (1, ["1/4", "5/8"], "crossed predecessor"),
        (2, ["1/2", "7/8"], "incomplete"),
    ],
)
def test_refinement_refuses_gaps_overlap_crossing_and_missing_tail(
    index: int, interval: list[str], message: str
) -> None:
    proposed, accepted = _fixture()
    changed = copy.deepcopy(proposed)
    changed[index]["interval"] = interval
    with pytest.raises(ValueError, match=message):
        refinement.complete_refinement(changed, accepted, max_rows=3)


def test_refinement_refuses_wrong_reference_and_row_ceiling() -> None:
    proposed, accepted = _fixture()
    proposed[0]["prior_reference"] = {"row": 2}
    with pytest.raises(ValueError, match="not accepted"):
        refinement.complete_refinement(proposed, accepted, max_rows=3)
    proposed, accepted = _fixture()
    with pytest.raises(ValueError, match="row inventory"):
        refinement.complete_refinement(proposed, accepted, max_rows=2)
