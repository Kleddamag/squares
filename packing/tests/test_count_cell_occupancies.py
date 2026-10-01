"""Synthetic controls for exact bounded occupancy-vector counts."""

from __future__ import annotations

import json
from itertools import product
from typing import cast

import pytest

from devtools.count_cell_occupancies import count_cell_occupancies, main


def test_known_small_counts_and_capacity_order() -> None:
    expected = count_cell_occupancies([1, 1, 2], 2)
    assert expected["coefficients_through_target"] == [1, 3, 4]
    assert expected["target_assignments"] == 4
    assert expected["total_assignments"] == 12
    assert expected["capacities"] == [1, 1, 2]
    assert count_cell_occupancies([2, 1, 1], 2)["coefficients_through_target"] == [
        1,
        3,
        4,
    ]


@pytest.mark.parametrize(
    ("capacities", "target", "coefficient", "total"),
    [([], 0, 1, 1), ([], 2, 0, 1), ([0, 0], 0, 1, 1), ([1, 2], 0, 1, 6), ([1], 2, 0, 2)],
)
def test_empty_zero_and_impossible_counts(
    capacities: list[int], target: int, coefficient: int, total: int
) -> None:
    result = count_cell_occupancies(capacities, target)
    assert result["target_assignments"] == coefficient
    assert result["total_assignments"] == total
    assert len(result["coefficients_through_target"]) == target + 1


def test_small_brute_force_enumeration() -> None:
    for cell_count in range(4):
        for capacities_tuple in product(range(3), repeat=cell_count):
            capacities = list(capacities_tuple)
            target = 6
            brute = [0] * (target + 1)
            for assignment in product(*(range(capacity + 1) for capacity in capacities)):
                brute[sum(assignment)] += 1
            result = count_cell_occupancies(capacities, target)
            assert result["coefficients_through_target"] == brute
            assert result["total_assignments"] == sum(brute)


@pytest.mark.parametrize(
    ("capacities", "target"),
    [
        ([True], 1),
        ([1.0], 1),
        (["1"], 1),
        ([-1], 1),
        ([65], 1),
        ([0] * 65, 1),
        ((1, 2), 1),
        ([1], True),
        ([1], 1.0),
        ([1], -1),
        ([1], 4097),
    ],
)
def test_malformed_and_excessive_inputs_refused(capacities: object, target: object) -> None:
    with pytest.raises(ValueError, match="must be"):
        _ = count_cell_occupancies(cast("list[int]", capacities), cast("int", target))


def test_cli_success_and_structured_refusal(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--capacities", "[1,1,2]", "--target", "2"]) == 0
    success = json.loads(capsys.readouterr().out)
    assert success["schema"] == "cell-occupancy-count/v1"
    assert success["target_assignments"] == 4
    assert success["coefficients_through_target"] == [1, 3, 4]
    assert main(["--capacities", "[1,true]", "--target", "1"]) == 2
    refused = json.loads(capsys.readouterr().out)
    assert refused["count_completed"] is False
    assert refused["schema"] == "cell-occupancy-count/v1"


def test_cli_input_size_cap(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--capacities", "[" + " " * 4096 + "]", "--target", "1"]) == 2
    assert "exceeds" in json.loads(capsys.readouterr().out)["error"]


def test_cli_deep_json_refuses_without_traceback(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--capacities", "[" * 1100 + "0" + "]" * 1100, "--target", "1"]) == 2
    assert json.loads(capsys.readouterr().out)["count_completed"] is False
