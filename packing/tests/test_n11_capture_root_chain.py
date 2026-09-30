"""Focused refusal controls for the fourteen-round receipt-chain admission."""

from __future__ import annotations

from fractions import Fraction as Q
from typing import Any

import pytest

from devtools import check_n11_capture_root_chain as chain
from devtools import check_n11_capture_root_continue as continuation
from devtools import check_n11_capture_root_round1 as first


def test_checker_revision_boundaries_are_explicit() -> None:
    assert chain.expected_checker(1) == continuation.FIRST_SHA
    assert chain.expected_checker(7) == continuation.LEGACY_SHA
    assert chain.expected_checker(8) == chain.MODERN_SHA
    assert chain.expected_checker(12) == chain.FINAL_SHA
    with pytest.raises(ValueError, match="round index"):
        chain.expected_checker(15)


def test_worker_requires_full_rows_output_and_prior_hash() -> None:
    cell = {
        "rows": [{}, {}],
        "inner_grid_compression": {"vertices": [["0", "0"]]},
    }
    worker = {
        "status": "PASS_CONDITIONAL_OWNER_UPDATE",
        "owner": 2,
        "round": 12,
        "rows_checked": 2,
        "round_sha256": "selected",
        "prior_sha256": "prior",
        "previous_result_sha256": "previous",
        "checker_sha256": chain.FINAL_SHA,
        "pilot_sha256": first.PILOT_SHA,
        "geometry_sha256": continuation.pilot.GEOMETRY_SHA,
        "degenerate_sha256": continuation.DEGENERATE_SHA,
        "new_points": [["0", "0"]],
    }

    def admit(candidate: dict[str, Any]) -> list[tuple[Q, Q]]:
        return chain.admit_worker(
            candidate,
            owner=2,
            round_index=12,
            selected_sha="selected",
            prior_sha="prior",
            previous_result_sha="previous",
            checker_sha=chain.FINAL_SHA,
            source_cell=cell,
        )

    assert admit(worker) == [(Q(), Q())]
    with pytest.raises(ValueError, match="binding differs"):
        admit({**worker, "rows_checked": 1})
    with pytest.raises(ValueError, match="previous binding"):
        admit({**worker, "previous_result_sha256": "stale"})
    with pytest.raises(ValueError, match="output differs"):
        admit({**worker, "new_points": [["1", "0"]]})
