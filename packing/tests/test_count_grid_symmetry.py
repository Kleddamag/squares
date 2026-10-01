"""Small exact controls for D4 occupancy orbit counting."""

from __future__ import annotations

import json
from itertools import combinations

import pytest

from devtools.count_grid_symmetry import count_grid_symmetry, grid_action_permutation, main


def test_one_cell_and_empty_occupancy() -> None:
    result = count_grid_symmetry(1, [2], 1)
    assert result["orbit_assignments"] == 1
    assert result["fixed_sum"] == 8
    assert [action["fixed_assignments"] for action in result["actions"]] == [1] * 8
    assert count_grid_symmetry(2, [0] * 4, 0)["orbit_assignments"] == 1
    assert count_grid_symmetry(2, [0] * 4, 1)["orbit_assignments"] == 0


def test_binary_two_by_two_has_adjacent_and_opposite_orbits() -> None:
    result = count_grid_symmetry(2, [1] * 4, 2)
    assert result["orbit_assignments"] == 2
    assert result["actions"][0]["fixed_assignments"] == 6
    assert [action["name"] for action in result["actions"]] == [
        "r0",
        "r1",
        "r2",
        "r3",
        "f0",
        "f1",
        "f2",
        "f3",
    ]
    assert result["actions"][0]["cycle_profile"] == [[1, 1]] * 4
    assert result["actions"][1]["cycle_profile"] == [[4, 1]]
    assert result["actions"][2]["cycle_profile"] == [[2, 1]] * 2
    assert result["fixed_sum"] == 16


def test_d4_actions_are_distinct_bijections_and_form_a_group() -> None:
    actions = [
        tuple(grid_action_permutation(3, turns, reflected=reflected))
        for reflected in (False, True)
        for turns in range(4)
    ]
    action_set = set(actions)
    assert len(action_set) == 8
    assert tuple(range(9)) in action_set
    capacities = [1, 1, 1, 1, 2, 1, 1, 1, 1]
    for action in actions:
        assert sorted(action) == list(range(9))
        assert all(capacities[index] == capacities[action[index]] for index in range(9))
        assert any(
            tuple(action[inverse[index]] for index in range(9)) == tuple(range(9))
            for inverse in actions
        )
        for other in actions:
            assert tuple(action[other[index]] for index in range(9)) in action_set


def test_binary_two_by_two_orbits_by_direct_action_enumeration() -> None:
    actions = [
        grid_action_permutation(2, turns, reflected=reflected)
        for reflected in (False, True)
        for turns in range(4)
    ]
    states = {
        tuple(1 if index in pair else 0 for index in range(4))
        for pair in combinations(range(4), 2)
    }
    orbits: set[frozenset[tuple[int, ...]]] = set()
    for state in states:
        orbits.add(
            frozenset(tuple(state[action[index]] for index in range(4)) for action in actions)
        )
    assert len(orbits) == count_grid_symmetry(2, [1] * 4, 2)["orbit_assignments"]


@pytest.mark.parametrize(
    ("size", "capacities", "target"),
    [
        (0, [0], 0),
        (True, [0], 0),
        (9, [0], 0),
        (2, [1, 1, 1], 1),
        (2, [1, 0, 0, 0], 1),
        (1, [True], 0),
        (1, [1.0], 0),
        (1, [-1], 0),
        (1, [3], 0),
        (1, [1], True),
        (1, [1], -1),
        (1, [1], 129),
    ],
)
def test_invalid_or_asymmetric_input_refused(
    size: object, capacities: object, target: object
) -> None:
    with pytest.raises(ValueError, match="must be"):
        _ = count_grid_symmetry(size, capacities, target)  # type: ignore[arg-type]


def test_cli_and_resource_refusals(capsys: pytest.CaptureFixture[str]) -> None:
    request = '{"grid_size":2,"capacities":[1,1,1,1],"target":2}'
    assert main(["--input", request]) == 0
    success = json.loads(capsys.readouterr().out)
    assert success["orbit_assignments"] == 2
    assert main(["--input", '{"grid_size":2,"capacities":[1,0,0,0],"target":1}']) == 2
    assert json.loads(capsys.readouterr().out)["count_completed"] is False
    assert main(["--input", "[" + " " * 4096 + "]"]) == 2
    assert "exceeds" in json.loads(capsys.readouterr().out)["error"]
    duplicate = '{"grid_size":1,"grid_size":1,"capacities":[1],"target":0}'
    assert main(["--input", duplicate]) == 2
    assert "duplicate" in json.loads(capsys.readouterr().out)["error"]
    assert main(["--input", "[" * 1100 + "]" * 1100]) == 2
    assert json.loads(capsys.readouterr().out)["count_completed"] is False
