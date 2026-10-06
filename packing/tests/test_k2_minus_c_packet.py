"""The import of jlevy/squares#368: Ryu's k^2 - M(k) >= 0.033 log k.

Sungjoon Ryu (squarepacker) reports a preprint whose constant 0.033 rests on Lemma 4.10,
a branch-and-bound cover of 78,673 boxes re-verified in Arb ball arithmetic. These tests
hold what was decided here, from the receipts of the
``squarepacker-k2-minus-c-2026-10-05`` packet:

- the source's own ``verify_leaves2.py`` re-verified every box, in four parts, with no
  failure and largest rigorous bound 9, and every part equals the author's output;
- the source's ``make_stats_v10.py`` and ``verify_v10.py`` pass on those outputs;
- the source's three coverage programs find no gap;
- two controls, regenerated here and pinned by digest, are refused: the box holding the
  nine-pair configuration at threshold 8, and the n = 2 list without that box; and
- the source's quick analytic checks and this repository's interval re-check of the
  constants pass.

They read receipts and retained files only; nothing here runs the source's programs.
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

from devtools import write_k2_minus_c_controls as controls

PACKET = controls.PACKET
RECEIPTS = PACKET / "receipts"
REPLAY = RECEIPTS / "verify-leaves2"
COVERAGE = RECEIPTS / "coverage"
CONTROLS = RECEIPTS / "controls"
BOXES = 78_673
_FOOTER = re.compile(
    r"^# finished \S+; exit (?P<exit>-?\d+); wall (?P<wall>[\d.]+) s; CPU (?P<cpu>[\d.]+) s"
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _body(path: Path) -> str:
    """A receipt's output, without its header and footer lines."""
    return "\n".join(line for line in _text(path).splitlines() if not line.startswith("# "))


def _exit(path: Path) -> int:
    match = _FOOTER.match(_text(path).splitlines()[-1])
    assert match, path
    return int(match["exit"])


def _json(path: Path) -> Any:
    return json.loads(_text(path))


def _archive() -> dict[str, bytes]:
    with zipfile.ZipFile(controls.ARCHIVE) as bundle:
        return {name: bundle.read(name) for name in bundle.namelist()}


def test_every_worker_exited_cleanly() -> None:
    for worker in range(4):
        assert _exit(REPLAY / f"verify-leaves2-worker{worker}.log") == 0
        assert _text(REPLAY / f"v2_worker{worker}.log").rstrip().endswith("### worker done")


def test_every_box_was_re_verified_with_no_failure() -> None:
    archive = _archive()
    leaves = {
        name: archive[name].decode("utf-8").count("\n")
        for name in archive
        if name.endswith("_final_leaves.jsonl")
    }
    assert len(leaves) == 13
    assert sum(leaves.values()) == BOXES
    for name, count in leaves.items():
        parts = [
            _json(REPLAY / "outputs" / name.replace(".jsonl", f"_verify2_{w}of4.json"))
            for w in range(4)
        ]
        assert all(part["finished"] and part["n_lines"] == count for part in parts), name
        assert sum(part["checked"] for part in parts) == count, name
        assert sum(part["ok"] for part in parts) == count, name
        assert all(part["fail"] == [] and part["maxU"] <= 9 for part in parts), name


def test_every_part_equals_the_authors_output() -> None:
    archive = _archive()
    outputs = sorted((REPLAY / "outputs").glob("*_verify2_*of4.json"))
    assert len(outputs) == 52
    for path in outputs:
        assert _json(path) == json.loads(archive[path.name]), path.name


def test_the_statistics_and_verify_v10_pass() -> None:
    stats = _json(REPLAY / "stats_v10.json")
    assert stats["complete"] is True
    assert (stats["fails"], stats["maxU"], stats["n_leaves"]) == (0, 9, BOXES)
    assert (stats["pieces"], stats["rig_pieces"]) == (59_238, 66_967)
    assert stats == json.loads(_archive()["stats_v10.json"])
    assert _exit(REPLAY / "make-stats-v10.log") == 0
    verify = _text(REPLAY / "verify-v10.log")
    assert _exit(REPLAY / "verify-v10.log") == 0
    assert "ALL OK" in verify
    assert not re.search(r"^FAIL", verify, re.MULTILINE)


#: Fields that time or measure a run rather than decide it.
_RUN_FIELDS = frozenset({"seconds", "sec", "mem", "min_avail"})


def _decided(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in _RUN_FIELDS}


def _slab(row: dict[str, Any]) -> tuple[bool, int, int]:
    return (row["wall"], row["n"], row["unit"])


def test_three_coverage_programs_find_no_gap() -> None:
    archive = _archive()
    checks = sorted((COVERAGE / "coverage-check").glob("*_coverage.json"))
    assert len(checks) == 13
    for path in checks:
        assert _json(path)["ok"] is True, path.name
        assert _json(path) == json.loads(archive[path.name]), path.name
    assert "FAILED" not in _body(COVERAGE / "coverage-check.log")
    retained = PACKET / "k2-minus-c/code/coverage_independent"
    volumes = sorted((COVERAGE / "indep-cover").glob("*.json"))
    assert len(volumes) == 13
    for path in volumes:
        report = _json(path)
        assert report["methodA_pass"] is True, path.name
        assert report["volume_exact_equal"] is True, path.name
        assert report["methodB_uncovered"] == [], path.name
        author = _json(retained / "exact_volume/results" / path.name)
        assert _decided(report) == _decided(author), path.name
    rows = [json.loads(line) for line in _text(COVERAGE / "results-replay.jsonl").splitlines()]
    assert len(rows) == 258
    assert sum(row["gaps"] for row in rows) == 0
    assert sum(row["leaves_total"] for row in rows if row["unit"] == 0) == BOXES
    authors = [
        json.loads(line)
        for line in _text(retained / "recursive_cover/results.jsonl").splitlines()
    ]
    assert sorted(map(_decided, rows), key=_slab) == sorted(map(_decided, authors), key=_slab)


def test_the_controls_regenerate_byte_for_byte(tmp_path: Path) -> None:
    assert controls.write_controls(tmp_path) == _json(CONTROLS / "controls.json")


def test_the_sharp_box_passes_at_nine_and_is_refused_at_eight() -> None:
    nine = _json(CONTROLS / "verify2-sharp-leaf-T9.json")
    assert (nine["checked"], nine["ok"], nine["fail"], nine["maxU"]) == (1, 1, [], 9)
    eight = _json(CONTROLS / "verify2-sharp-leaf-T8.json")
    assert (eight["checked"], eight["ok"], len(eight["fail"])) == (1, 0, 1)
    assert eight["pieces"] == 4097
    assert (
        "verify_leaves2.py bnb_n2_T9_0of1_final_leaves.jsonl 8 0 1"
        in _text(CONTROLS / "verify-leaves2-sharp-leaf-T8.log").splitlines()[0]
    )


def test_every_coverage_program_refuses_the_dropped_box() -> None:
    assert '"ok": true' in _text(CONTROLS / "coverage-check-n2-base.log")
    assert "FAIL: reached a tiny unmatched box" in _text(
        CONTROLS / "coverage-check-n2-drop.log"
    )
    assert _exit(CONTROLS / "coverage-check-n2-drop.log") == 1
    assert '"methodA_pass": true' in _text(CONTROLS / "indep-cover-n2-base.log")
    assert '"methodA_pass": false' in _text(CONTROLS / "indep-cover-n2-drop.log")
    assert "TOTAL {'gaps': 0," in _text(CONTROLS / "coverage-lowmem-n2-base-summary.log")
    assert "TOTAL {'gaps': 2," in _text(CONTROLS / "coverage-lowmem-n2-drop-summary.log")


def test_the_constants_hold() -> None:
    for overlap, count in ((9, 31), (13, 28)):
        record = _json(RECEIPTS / "constants" / f"ryu-constants-overlap-{overlap}.json")
        assert record["passed"] is True
        assert len(record["checks"]) == count
    sources = RECEIPTS / "source-checks"
    assert "ALL OK" in _text(sources / "consts_v10-9.log")
    assert "ALL OK (lem:Kw refinement)" in _text(sources / "kw13_check.log")
    hand9 = re.findall(r"count=(\d+)", _text(sources / "check_hand9_indep.log"))
    assert len(hand9) == 5
    assert set(hand9) == {"9"}


def test_the_replay_ran_the_retained_bytes() -> None:
    archive = _archive()
    code = PACKET / "k2-minus-c/code"
    ran: dict[str, str] = {}
    for line in _text(REPLAY / "inputs.sha256").splitlines():
        digest, name = line.split(maxsplit=1)
        ran[name] = digest
    leaves = {name: digest for name, digest in ran.items() if name.endswith(".jsonl")}
    assert len(leaves) == 13
    for name, digest in leaves.items():
        assert hashlib.sha256(archive[name]).hexdigest() == digest, name
    programs = {name: digest for name, digest in ran.items() if name.endswith(".py")}
    assert "verify_leaves2.py" in programs
    for name, digest in programs.items():
        assert hashlib.sha256((code / name).read_bytes()).hexdigest() == digest, name
