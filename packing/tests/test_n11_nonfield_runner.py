"""A complete execution, identity and empty pending inventory are jointly required."""

from __future__ import annotations

from typing import Any

import pytest

from devtools.run_n11_nonfield_batch import complete_case


@pytest.mark.parametrize(
    "change",
    [
        {"status": "INCOMPLETE"},
        {"excluded_case_ids": [2095, 2096]},
        {"excluded_case_ids": []},
        {"geometry_verified": False},
        {"global_optimality_proved": True},
        {"current_row": 159},
        {"current_node": "unfinished"},
        {"current_step": 4},
        {"mask_index": 2096},
        {"source_sha256": {"checker": "wrong"}},
    ],
)
def test_partial_or_mismatched_receipt_never_credits_a_case(change: dict[str, Any]) -> None:
    record = {
        "status": "PASS_ONE_GENERIC_EXCLUSION",
        "geometry_verified": True,
        "global_optimality_proved": False,
        "excluded_case_ids": [2095],
        "mask_index": 2095,
        "current_node": None,
        "current_step": None,
        "current_row": None,
        "source_sha256": {"checker": "frozen"},
    }
    assert complete_case(record, 2095, "frozen", 0)
    assert not complete_case(record, 2095, "frozen", 2)
    assert not complete_case({**record, **change}, 2095, "frozen", 0)
