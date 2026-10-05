"""The retained answers of the valid7 fix probe: D-1 to D-3 at 38dd31b, none at da469ec."""

from __future__ import annotations

import copy
import json

from devtools import probe_valid7_fixes as probe


def test_the_retained_receipt_shows_each_defect_before_the_fix_and_none_after() -> None:
    receipt = json.loads(probe.RECEIPT.read_text(encoding="utf-8"))
    assert probe.problems(receipt) == []
    assert set(receipt["answers"]) == set(probe.TREES)
    assert receipt["interpreter"]["python_flint"] == "0.9.0"


def test_a_defect_still_present_after_the_fix_is_reported() -> None:
    receipt = json.loads(probe.RECEIPT.read_text(encoding="utf-8"))
    broken = copy.deepcopy(receipt)
    fixed = list(probe.TREES)[1]
    broken["answers"][fixed]["d1_nonneg_open_neg_square_at_sample"] = True
    assert probe.problems(broken) == [
        "d1_nonneg_open_neg_square_at_sample: True after the fix, expected False"
    ]
