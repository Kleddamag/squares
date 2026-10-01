"""Target-free controls for the deterministic n17 common-core stress."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path

import pytest

from devtools import check_n17_core_stress as stress
from devtools.check_n17_contact_chart import ANCHORS, CONTACTS
from devtools.check_n17_endpoint_feasibility import _layout


def test_complete_original_order_matrix_and_exact_unrelated_residuals() -> None:
    t, b, half = Q(1, 3), Q(1, 5), Q(1, 2)
    rows, weights, scales, residuals = stress.complete_stress(t, b, half)
    assert len(rows) == len(weights) == 58
    assert all(len(row) == 52 for row in rows.values())
    assert list(rows)[:2] == [("wall", *ANCHORS[0], 0), ("wall", *ANCHORS[0], 1)]
    assert list(rows)[-1] == ("pair", *CONTACTS[-1][:2], 0)
    assert residuals[51] == 0
    side, aux, _ = _layout(t, b, half)
    f2 = aux["d"] * (side - aux["X"] - Q(3, 2)) - aux["e"] * (aux["Y"] - side + Q(3, 2)) - 1
    expected = aux["gamma"] * scales["rho"] * f2 / scales["K"]
    assert residuals[stress._coordinate(12, "angle")] == expected
    assert residuals[stress._coordinate(16, "angle")] == -expected
    assert all(
        residual == 0
        for index, residual in enumerate(residuals)
        if index not in {stress._coordinate(12, "angle"), stress._coordinate(16, "angle")}
    )


def test_prescribed_zero_rows_and_mutated_moment_refusal() -> None:
    rows, weights, _, _ = stress.complete_stress(Q(1, 3), Q(1, 5), Q(1, 2))
    zero_keys = {
        ("wall", 5, "right", 0),
        ("wall", 5, "right", 1),
        ("wall", 6, "bottom", 0),
        ("wall", 6, "bottom", 1),
        ("pair", 9, 11, 0),
        ("pair", 9, 11, 1),
    }
    assert all(weights[key] == 0 for key in zero_keys)
    altered = weights.copy()
    altered["pair", 9, 10, 0] += Q(1, 100)
    assert any(
        sum(altered[key] * row[column] for key, row in rows.items())
        != sum(weights[key] * row[column] for key, row in rows.items())
        for column in range(52)
    )


def test_unready_cli_refuses_before_any_target_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    paths = [
        tmp_path / name for name in ("root.json", "endpoint.json", "feature.json", "source")
    ]
    for path in paths:
        path.write_bytes(b"{}")

    def refuse(_path: Path) -> bytes:
        raise AssertionError("unready CLI attempted target input read")

    monkeypatch.setattr(stress, "_read_limited", refuse)
    assert stress.main([*(str(path) for path in paths[:3]), "--source", str(paths[3])]) == 2
    output = capsys.readouterr().out
    assert '"criterion_passed": false' in output
    assert '"error": "instrument_unready"' in output
