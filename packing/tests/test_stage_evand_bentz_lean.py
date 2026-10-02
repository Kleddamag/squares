"""Staging Evan Daniel's Lean reduction for T-064 from retained bytes.

``devtools.stage_evand_bentz_lean`` assembles the import closure of ``bentz_of_valid7``
from the September 26 and October 1 evand packets, regenerates the two data files with
the source's own scripts, and refuses any file whose Git blob is not the upstream one.
It builds nothing; the build needs a Lean toolchain and the Mathlib cache.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools import stage_evand_bentz_lean as stage

RECEIPT = stage.OCT01.parent.parent / "receipts/lean/bentz_stage.json"


def test_comments_are_stripped_before_the_escape_scan() -> None:
    text = "/- a /- nested native_decide -/ sorry -/\ntheorem t : True := trivial -- sorry\n"
    assert "sorry" not in stage.strip_comments(text)
    assert "native_decide" not in stage.strip_comments(text)
    assert "theorem t : True := trivial" in stage.strip_comments(text)


def test_the_closure_stages_with_every_upstream_blob(tmp_path: Path) -> None:
    receipt = stage.stage(tmp_path)
    assert receipt["ok"], receipt["problems"]
    assert receipt["toolchain"] == "leanprover/lean4:v4.33.1"
    found = receipt["kernel_escapes"]
    assert isinstance(found, dict)
    assert set(found.values()) == {0}
    probe = (tmp_path / "s12/lean/AxiomsBentz.lean").read_text(encoding="utf-8")
    assert f"#print axioms {stage.THEOREM}" in probe
    lean = sorted(p.name for p in (tmp_path / "s12/lean/Sqpack").glob("*.lean"))
    assert lean == sorted(Path(n).name for n in stage.UPSTREAM if n.startswith("lean/Sqpack/"))


def test_a_changed_input_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    changed = tmp_path / "Bentz.lean"
    original = stage.RETAINED["lean/Sqpack/Bentz.lean"].read_text(encoding="utf-8")
    changed.write_text(original + "theorem x : False := by sorry\n", encoding="utf-8")
    monkeypatch.setitem(stage.RETAINED, "lean/Sqpack/Bentz.lean", changed)
    receipt = stage.stage(tmp_path / "out")
    assert not receipt["ok"]
    problems = receipt["problems"]
    assert isinstance(problems, list)
    assert any(str(x).startswith("lean/Sqpack/Bentz.lean is blob") for x in problems)
    assert "1 x \\bsorry\\b in the staged sources" in problems


def test_the_committed_receipt_is_the_tool_output(tmp_path: Path) -> None:
    committed = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert committed == stage.stage(tmp_path)
