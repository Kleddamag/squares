"""Focused refusal and input-binding controls for the paired verifier benchmark."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

from benchmarks.bench_rectangle_verifier_parity import (
    EFFECTIVE_THRESHOLD,
    check_interval_adapter,
    checked_rows,
    classify,
)


def _decision(
    cpp_rows: list[dict[str, object]],
    native: dict[str, object],
    *,
    first: int = 0,
    last: int = 200,
    cpp_exit: int = 0,
    native_exit: int = 0,
    cpp_timeout: bool = False,
) -> str:
    return classify(
        first=first,
        last=last,
        cpp_exit=cpp_exit,
        cpp_timeout=cpp_timeout,
        cpp_rows=cpp_rows,
        native_exit=native_exit,
        native_report=native,
        native_timeout=False,
    )


def test_complete_scope_requires_both_full_angle_censuses() -> None:
    cpp_rows = [
        {
            "r": index,
            "status": "verified",
            "lower_bound": format(float(EFFECTIVE_THRESHOLD), ".17g"),
            "nodes": 1,
            "leaves": 1,
        }
        for index in range(201)
    ]
    native_rows = [
        {
            "index": index,
            "status": "VERIFIED",
            "lower_bound": str(EFFECTIVE_THRESHOLD),
            "unresolved_leaves": 0,
            "nodes": 1,
        }
        for index in range(201)
    ]
    native = {
        "status": "VERIFIED",
        "angles": native_rows,
    }
    assert _decision(cpp_rows, native) == "MATCHED_COMPLETE_VERIFIED"
    missing = {**native, "angles": native_rows[:-1]}
    assert _decision(cpp_rows, missing) != "MATCHED_COMPLETE_VERIFIED"
    below = [*cpp_rows]
    below[1] = {
        **below[1],
        "lower_bound": format(math.nextafter(float(EFFECTIVE_THRESHOLD), -math.inf), ".17g"),
    }
    assert _decision(below, native) != "MATCHED_COMPLETE_VERIFIED"
    assert _decision([*cpp_rows, cpp_rows[0]], native) != "MATCHED_COMPLETE_VERIFIED"
    assert (
        _decision(cpp_rows, {**native, "angles": [*native_rows, native_rows[0]]})
        != "MATCHED_COMPLETE_VERIFIED"
    )
    unresolved = [*native_rows]
    unresolved[1] = {**unresolved[1], "unresolved_leaves": 1}
    assert _decision(cpp_rows, {**native, "angles": unresolved}) != "MATCHED_COMPLETE_VERIFIED"
    missing_lower = [*cpp_rows]
    missing_lower[2] = {
        key: value for key, value in cpp_rows[2].items() if key != "lower_bound"
    }
    assert _decision(missing_lower, native) != "MATCHED_COMPLETE_VERIFIED"
    assert _decision(cpp_rows, native, cpp_timeout=True) == "INCOMPLETE_NO_PARITY_CLAIM"


def test_subset_or_unresolved_cannot_be_full_parity() -> None:
    cpp = [
        {
            "r": 1,
            "status": "verified",
            "lower_bound": format(float(EFFECTIVE_THRESHOLD), ".17g"),
            "nodes": 1,
            "leaves": 1,
        }
    ]
    native = {
        "status": "PARTIAL",
        "angles": [
            {
                "index": 1,
                "status": "VERIFIED",
                "lower_bound": str(EFFECTIVE_THRESHOLD),
                "unresolved_leaves": 0,
                "nodes": 1,
            }
        ],
    }
    assert _decision(cpp, native, first=1, last=1, native_exit=2) == "MATCHED_SUBSET_ONLY"
    assert (
        _decision(cpp, native, first=1, last=1, cpp_exit=3, native_exit=2)
        == "INCOMPLETE_NO_PARITY_CLAIM"
    )
    assert checked_rows('{"r":1,"status":"verified"}\nUNRESOLVED 1 10\n', 1, 1) == [
        {"r": 1, "status": "verified"}
    ]


def test_exact_adapter_binding_refuses_changed_interval() -> None:
    source = (
        Path(__file__).parents[1]
        / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
    )
    raw = source.read_bytes()

    def enclosed(value: Fraction) -> str:
        nearest = float(value)
        converted = Fraction(nearest)
        low = nearest if converted <= value else math.nextafter(nearest, -math.inf)
        high = nearest if converted >= value else math.nextafter(nearest, math.inf)
        return f"{low.hex()} {high.hex()}"

    side, core = Fraction(3, 2), Fraction(9977, 10000)
    left, right = Fraction(1, 1000), Fraction(1499, 1000)
    mass = Fraction(1683003, 625000)
    rho = mass / (8 * (right - left) ** 2)
    rectangle = " ".join(enclosed(value) for value in (left, left, right, right, rho))
    centers = (Fraction(3, 4), Fraction(20003, 20000), Fraction(20023, 20000))
    encoded = "\n".join(
        [enclosed(side), enclosed(core), "8", *([rectangle] * 8), "3"]
        + [enclosed(value) for value in centers]
    )
    assert check_interval_adapter(raw, encoded) == {"expanded_rectangles": 8, "axis_centers": 3}
    lines = encoded.splitlines()
    lines[0] = "0x1p+0 0x1p+0"
    try:
        check_interval_adapter(raw, "\n".join(lines))
    except ValueError as error:
        assert "side/core" in str(error)
    else:
        raise AssertionError("changed adapter interval was accepted")
