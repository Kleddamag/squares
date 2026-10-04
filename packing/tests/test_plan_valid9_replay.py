"""The ValidTilt9 replay planner, and the plan and calibration receipts it wrote.

``devtools.plan_valid9_replay`` prices a full replay of Daniel's ``qx2_zm.py`` run
``qx2_k4x_k008`` from its retained record, splits it into shards, stages the checker and
cover, and compares a sharded replay with the published record. The record is retained,
so every test here reads the real file.
"""

from __future__ import annotations

import gzip
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from devtools import plan_valid9_replay as p9

RECEIPTS = p9.PACKET / "receipts/valid9"
CALIBRATION = ("x23-24_y16-17", "x33-34_y22-23")
F = Fraction


def _rect_cells(rect: p9.Rect) -> set[p9.Cell]:
    x0, x1, y0, y1 = rect
    return {
        (x0 + p9.PITCH * i, y0 + p9.PITCH * j)
        for i in range(int((x1 - x0) / p9.PITCH))
        for j in range(int((y1 - y0) / p9.PITCH))
    }


def test_the_plan_covers_the_d4_region_once_in_balanced_shards() -> None:
    result = p9.plan(12)
    assert result["roots"] == p9.ROOTS
    assert result["recorded_cpu_hours"] == pytest.approx(815_343 / 3600, abs=0.01)
    shards = cast("list[dict[str, object]]", result["shards"])
    assert len(shards) == 12
    cells: list[p9.Cell] = []
    for shard in shards:
        runs = cast("list[dict[str, object]]", shard["runs"])
        assert len(runs) <= 3
        for run in runs:
            rect = cast("p9.Rect", tuple(F(v) for v in cast("list[str]", run["rectangle"])))
            cells += _rect_cells(rect)
            command = cast("list[str]", run["command"])
            assert command[1:3] == ["checker/qx2_zm.py", "K4_k008_box9.txt"]
            assert command[command.index("--resume") + 1] == run["record"]
            assert not p9.argv_problems("plan", {"argv": command[1:]})
    assert len(cells) == len(set(cells)) == p9.GRID**2
    priced = [cast("float", s["priced_cpu_hours"]) for s in shards]
    assert sum(priced) == pytest.approx(cast("float", result["recorded_cpu_hours"]), abs=0.1)
    assert max(priced) <= 1.05 * sum(priced) / len(priced)


def _published_lines() -> list[dict[str, object]]:
    with gzip.open(p9.RECORD, "rt", encoding="utf-8") as handle:
        return [cast("dict[str, object]", json.loads(raw)) for raw in handle][1:]


ARGV = [
    "checker/qx2_zm.py", "K4_k008_box9.txt", "--depth", "18", "--nproc", "4",
    "--exact-umax", "1/2", "--exact-from", "3", "--progress", "200",
    "--cx-lo", "0", "--cx-hi", "3/2", "--resume", "runs/x.jsonl", "--dump-leaves",
]  # fmt: skip


def _shards(tmp_path: Path, lines: list[dict[str, object]], argv: list[str]) -> list[Path]:
    """``lines`` split into three records, the last gzipped as a runner would leave it."""
    header = {"kind": "header", "sha256": {**p9.FILES, "input": p9.COVER_SHA256}, "argv": argv}
    third = len(lines) // 3 + 1
    paths: list[Path] = []
    for k in range(3):
        text = "".join(
            json.dumps(x) + "\n" for x in [header, *lines[k * third : (k + 1) * third]]
        )
        path = tmp_path / f"shard{k}.jsonl"
        if k == 2:
            path = path.with_suffix(".jsonl.gz")
            path.write_bytes(gzip.compress(text.encode(), mtime=0))
        else:
            path.write_text(text, encoding="utf-8")
        paths.append(path)
    return paths


def test_compare_accepts_the_published_record_in_pieces_and_names_each_fault(
    tmp_path: Path,
) -> None:
    lines = _published_lines()
    ok = p9.compare(_shards(tmp_path, lines, ARGV))
    assert ok["ok"], ok["problems"]
    assert ok["roots"] == ok["roots_matching_published_leaves"] == p9.ROOTS
    assert ok["leaves_matching"] == 115_268
    dropped = p9.compare(_shards(tmp_path, lines[:-1], ARGV))
    assert dropped["problems"] == ["1 published roots are missing"]
    # Every other fault on a partial slice, which keeps the test to seconds.
    some = lines[:600]
    assert p9.compare(_shards(tmp_path, some, ARGV), partial=True)["ok"]
    twice = p9.compare(_shards(tmp_path, [*some, some[0]], ARGV), partial=True)
    assert twice["problems"] == ["1 roots recorded more than once"]
    tampered = json.loads(json.dumps(some))
    leaves = cast("list[list[object]]", tampered[0]["leaves"])
    leaves[0][1] = "CAP" if leaves[0][1] != "CAP" else "EMPTY"
    changed = p9.compare(_shards(tmp_path, tampered, ARGV), partial=True)
    assert changed["problems"] == ["1 roots have leaves other than the published ones"]
    shallow = [v if v != "18" else "12" for v in ARGV]
    assert p9.compare(_shards(tmp_path, some, shallow), partial=True)["problems"] == [
        f"shard{k}.{ext}: argv does not set --depth 18"
        for k, ext in ((0, "jsonl"), (1, "jsonl"), (2, "jsonl.gz"))
    ]
    one_bin = [*ARGV, "--u-lo", "1/4"]
    assert "shard0.jsonl: argv changes a setting with --u-lo" in cast(
        "list[str]", p9.compare(_shards(tmp_path, some, one_bin), partial=True)["problems"]
    )
    uncertified = json.loads(json.dumps(some))
    cast("dict[str, int]", uncertified[0]["st"])["UNCERT"] = 1
    bad = p9.compare(_shards(tmp_path, uncertified, ARGV), partial=True)
    assert bad["problems"] == [f"shard0.jsonl: root {some[0]['root']} has 1 uncertified"]


def test_stage_writes_the_retained_files_and_refuses_a_wrong_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    staged = p9.stage(tmp_path / "work", s12=True)
    assert staged == {
        **{f"checker/{n}": d for n, d in p9.FILES.items()},
        "K4_k008_box9.txt": p9.COVER_SHA256,
        "s12_files": 53,
    }
    upstream = tmp_path / "work" / p9.RECORD_UPSTREAM
    assert upstream.read_bytes() == p9.RECORD.read_bytes()
    assert (tmp_path / "work/s12/search/qx2_data/K4_k008_box9.txt").read_bytes() == (
        tmp_path / "work/K4_k008_box9.txt"
    ).read_bytes()
    fake = tmp_path / "checker"
    fake.mkdir()
    for name in p9.FILES:
        (fake / name).write_bytes((p9.CHECKER / name).read_bytes())
    (fake / "zm_mixed.py").write_text("# not the retained file\n", encoding="utf-8")
    monkeypatch.setattr(p9, "CHECKER", fake)
    with pytest.raises(SystemExit, match="the record names 1fd203469bb43a55"):
        p9.stage(tmp_path / "bad")
    monkeypatch.setattr(p9, "CHECKER", p9.K2M4 / "qx2_zm/checker")
    wrong = tmp_path / "cover.gz"
    wrong.write_bytes(gzip.compress(b"9 1 5 1 0\n", mtime=0))
    monkeypatch.setattr(p9, "COVER_GZ", wrong)
    with pytest.raises(SystemExit, match="not 4151d7c4"):
        p9.stage(tmp_path / "bad")


def test_the_committed_plan_is_what_the_tool_writes() -> None:
    receipt = json.loads((RECEIPTS / "qx2_replay_plan.json").read_text(encoding="utf-8"))
    fresh = p9.plan(
        len(receipt["shards"]), speed=receipt["speed"], cores=receipt["cores_per_shard"]
    )
    assert fresh == receipt


def _footer(log: Path) -> tuple[float, str]:
    text = log.read_text(encoding="utf-8")
    cpu = re.search(r"exit 0; wall [\d.]+ s; CPU ([\d.]+) s", text)
    assert cpu is not None, log
    return float(cpu.group(1)), text


def test_the_calibration_reproduces_published_leaves_and_bounds_the_speed() -> None:
    here = recorded = 0.0
    for cell in CALIBRATION:
        cpu, log = _footer(RECEIPTS / f"qx2_calibration_{cell}.log")
        assert "VERIFIED-D4" in log
        assert (
            "sha256 4151d7c4059d5dcf56130c9373e6b5b60635e1a4250f46562d7ecc4d64a27801  input"
            in log
        )
        x0, x1, y0, y1 = (F(int(v), 10) for v in re.findall(r"\d+", cell))
        here += cpu
        recorded += cast("float", p9.region((x0, x1), (y0, y1))["recorded_cpu_seconds"])
    plan = json.loads((RECEIPTS / "qx2_replay_plan.json").read_text(encoding="utf-8"))
    assert here / recorded <= plan["speed"]
    compare = json.loads((RECEIPTS / "qx2_calibration_compare.json").read_text("utf-8"))
    assert (compare["ok"], compare["partial"]) == (True, True)
    assert compare["roots"] == compare["roots_matching_published_leaves"] == 16
