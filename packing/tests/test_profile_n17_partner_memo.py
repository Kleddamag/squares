"""Exercise the observer against the real producer frame on the small W7 fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from devtools import profile_n17_partner_memo as profile


def test_w7_profile_observes_live_producer_locals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "profile"
    monkeypatch.setattr(sys, "argv", ["profile", str(output), "--fixture", "W7"])
    assert profile.main() == 0
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["fixture"] == "W7"
    assert summary["steps"] > 0
    assert len(summary["memo_trace"]) == summary["steps"]
    assert all(sample["memo_entries"] > 0 for sample in summary["memo_trace"])
    assert all(sample["obsolete_entries"] == 0 for sample in summary["memo_trace"])
    assert summary["pipeline_peak_working_set_bytes"] > 0
