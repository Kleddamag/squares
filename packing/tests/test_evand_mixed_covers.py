"""Controls for Evan Daniel's mixed covers for ``s(21) = 5`` and ``s(45) = 7``.

The packet under ``resources/web/evand-square-packing-2026-09-28/`` holds the source's
covers, both of its checkers' run records, and this repository's replays of the ``zmx2``
checker. The sweeps that decide coverage take minutes (``zmx2``) to many CPU-hours
(``zm_mixed.py``) and leave receipts. These tests are the fast part that has to stay
true: the retained bytes are the pinned ones; each cover is well formed, weighs exactly
what the packet states and less than the count it excludes, and is invariant under the
square's symmetries; the shipped records cover their regions with no uncertified box;
and the replays' censuses equal the source's, root for root. The same commands audit a
replayer's own ``zmx2`` log of the ``s(32)`` point cover against the retained run, and
a mutated, dropped or differently configured root fails them.

Coverage itself, every closed unit square capturing mass at least one, is not decided
here. `devtools.audit_evand_mixed_covers` does the reading, with its own parser.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.audit_evand_mixed_covers import (
    CASES,
    PACKET,
    POINT_COVER_RUNS,
    POINT_COVERS,
    RECEIPTS,
    Case,
    PointCoverRun,
    audit_cover,
    audit_point_cover_run,
    audit_zm_mixed,
    audit_zmx2,
    check_point_cover_runs,
    compare_zm_mixed,
    compare_zmx2,
    comparison_clean,
    cover_clean,
    main,
    point_cover_clean,
    sample_records,
    zm_mixed_clean,
    zmx2_clean,
    zmx2_comparison_clean,
)
from devtools.retained_data import (
    candidates,
    check_packet,
    read_retained_bytes,
    read_retained_text,
)

BUNDLES = PACKET / "square-packing" / "s12" / "certificates"
MODES = ("d4", "full")


def test_retained_bytes_match_the_packet_manifest() -> None:
    lines = (PACKET / "retained-files.sha256").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 91
    for line in lines:
        digest, path = line.split("  ", 1)
        data = read_retained_bytes(PACKET / path)
        assert hashlib.sha256(data).hexdigest() == digest, path


def test_compressed_files_match_their_table_and_none_is_left_plain() -> None:
    assert check_packet(PACKET) == []
    assert candidates(PACKET) == []


@pytest.mark.parametrize("n", sorted(CASES))
def test_cover_is_well_formed_light_and_symmetric(n: int) -> None:
    case = CASES[n]
    result = audit_cover(case)
    assert cover_clean(result), result
    assert Fraction(result["total"]) == case.total < n
    # The segment mass lies on the interior grid lines and nowhere else.
    interior = [str(c) for c in range(1, case.side)]
    assert result["lines_carrying_segments"] == {"x": interior, "y": interior}


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("n", sorted(CASES))
def test_shipped_zmx2_log_covers_its_region(n: int, mode: str) -> None:
    result = audit_zmx2(CASES[n], BUNDLES / f"s{n}" / f"zmx2_{mode}" / "roots.log", mode)
    assert zmx2_clean(result), result


@pytest.mark.parametrize("n", sorted(CASES))
def test_shipped_zm_mixed_records_cover_the_d4_region(n: int) -> None:
    records = BUNDLES / f"s{n}" / "zm_mixed_d4" / "roots.jsonl"
    result = audit_zm_mixed(CASES[n], records)
    assert zm_mixed_clean(result), result
    manifest = json.loads((records.parent / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["result"]["verdict"] == "VERIFIED-D4"
    assert manifest["records"]["sha256"] == result["sha256"]
    shipped = {k: v for k, v in manifest["result"]["census"].items() if k != "cpu"}
    assert result["census"] == shipped


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("n", sorted(CASES))
def test_fresh_zmx2_run_matches_the_shipped_census(n: int, mode: str) -> None:
    fresh = RECEIPTS / f"s{n}_zmx2_{mode}_roots.log"
    assert zmx2_clean(audit_zmx2(CASES[n], fresh, mode))
    result = compare_zmx2(BUNDLES / f"s{n}" / f"zmx2_{mode}" / "roots.log", fresh)
    assert zmx2_comparison_clean(result), result
    assert result["shipped_roots_not_replayed"] == 0


@pytest.mark.parametrize("n", sorted(CASES))
def test_zm_mixed_sample_matches_the_shipped_census(n: int) -> None:
    samples = sample_records(n)
    assert len(samples) == 2
    result = compare_zm_mixed(BUNDLES / f"s{n}" / "zm_mixed_d4" / "roots.jsonl", samples)
    assert comparison_clean(result), result
    assert result["replay_roots"] == 32
    assert result["header_sha256_equal"]
    assert result["settings_equal_apart_from_region"]


@pytest.mark.parametrize("run", POINT_COVER_RUNS, ids=lambda run: f"s{run.n}")
def test_point_cover_zmx2_run_matches_the_source_report(run: PointCoverRun) -> None:
    result = audit_point_cover_run(run)
    assert point_cover_clean(result), result


def test_the_point_cover_logs_are_required() -> None:
    report, clean = check_point_cover_runs()
    assert clean, report
    assert set(report) == {f"s{run.n}_point_cover_zmx2_d4" for run in POINT_COVER_RUNS}
    absent = replace(POINT_COVERS[32], receipt="s32_no_such_run_roots.log")
    report, clean = check_point_cover_runs((POINT_COVERS[13], absent))
    assert not clean
    assert report["s32_point_cover_zmx2_d4"]["missing"]


# --- the audit fails closed ---------------------------------------------------------------

#: A symmetric toy cover of [0, 2]^2 (D = 10): four points off the lines, and the two
#: middle grid lines each carrying mass 1 as one segment. Total 4.
TOY = """mixed 1
2 1
10
100
4
5 5 50
15 5 50
5 15 50
15 15 50
2
10 0 10 20 100
0 10 20 10 100
0
"""


def _toy(tmp_path: Path, text: str) -> tuple[Case, Path]:
    path = tmp_path / "toy.txt"
    path.write_text(text, encoding="ascii")
    return Case(5, 2, "toy", "toy.txt", Fraction(4), 4, 2), path


def test_toy_cover_is_clean(tmp_path: Path) -> None:
    case, path = _toy(tmp_path, TOY)
    assert cover_clean(audit_cover(case, path))


def test_a_moved_point_breaks_the_symmetry(tmp_path: Path) -> None:
    case, path = _toy(tmp_path, TOY.replace("15 15 50", "15 14 50"))
    result = audit_cover(case, path)
    assert not result["d4_invariant_as_measure"]
    assert not cover_clean(result)


def test_a_split_segment_is_the_same_measure_but_not_the_same_entries(tmp_path: Path) -> None:
    text = TOY.replace("2\n10 0 10 20 100", "3\n10 0 10 10 50\n10 10 10 20 50")
    case, path = _toy(tmp_path, text)
    result = audit_cover(replace(case, segments=3), path)
    assert result["d4_invariant_as_measure"]
    assert not result["d4_invariant_entry_by_entry"]


def test_a_point_on_a_line_and_a_wrong_total_are_reported(tmp_path: Path) -> None:
    case, path = _toy(tmp_path, TOY.replace("15 15 50", "15 15 51"))
    assert not audit_cover(case, path)["total_equals_stated"]
    case, path = _toy(tmp_path, TOY.replace("\n5 5 50\n", "\n10 5 50\n", 1))
    assert audit_cover(case, path)["points_on_segment_lines"] == 1


def test_a_missing_or_uncertified_root_is_refused(tmp_path: Path) -> None:
    shipped = BUNDLES / "s21" / "zmx2_d4" / "roots.log"
    lines = read_retained_text(shipped, encoding="ascii").splitlines()
    missing = tmp_path / "missing.log"
    missing.write_text("\n".join(lines[:-1]) + "\n", encoding="ascii")
    assert audit_zmx2(CASES[21], missing, "d4")["roots_missing"] == 1
    assert not zmx2_clean(audit_zmx2(CASES[21], missing, "d4"))
    last = lines[-1].replace(" uncert 0 ", " uncert 1 ")
    assert last != lines[-1]
    uncertified = tmp_path / "uncertified.log"
    uncertified.write_text("\n".join([*lines[:-1], last]) + "\n", encoding="ascii")
    assert not zmx2_clean(audit_zmx2(CASES[21], uncertified, "d4"))
    compared = compare_zmx2(shipped, uncertified)
    assert compared["roots_whose_census_differs"]
    assert not comparison_clean(compared)


# --- a replayer's own s(32) log -----------------------------------------------------------

S32_LOG = RECEIPTS / POINT_COVERS[32].receipt


def _s32_replay(
    tmp_path: Path, name: str, edit: Callable[[list[str]], list[str]] | None = None
) -> Path:
    """The retained run as a replayer might write it: other timings, roots in another order.

    ``edit`` maps the list of ROOT lines to a changed list, for the negative controls.
    """
    lines = read_retained_text(S32_LOG, encoding="ascii").splitlines()
    header = [line for line in lines if not line.startswith("ROOT ")]
    roots = [re.sub(r" ms \d+$", " ms 7", line) for line in lines if line.startswith("ROOT ")]
    roots.reverse()
    if edit is not None:
        roots = edit(roots)
    path = tmp_path / name
    path.write_text("\n".join([*header, *roots]) + "\n", encoding="ascii")
    return path


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, dict[str, Any]]:
    code = main(list(argv))
    return code, json.loads(capsys.readouterr().out)


def test_a_fresh_s32_log_is_audited_root_for_root(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    fresh = str(_s32_replay(tmp_path, "fresh.log"))
    code, audited = _run(capsys, "zmx2", "--case", "32", "--mode", "d4", fresh)
    assert code == 0, audited
    assert audited["roots_present"] == 3600
    assert audited["totals_equal_source_report"]
    code, compared = _run(capsys, "compare-zmx2", "--case", "32", "--records", fresh)
    assert code == 0, compared
    assert compared["headers_equal"]
    assert compared["roots_identical"] == compared["roots_compared"] == 3600
    assert compared["shipped_roots_not_replayed"] == 0


def _deepen_one_root(roots: list[str]) -> list[str]:
    """One certified leaf split once more: two more boxes, one more certified leaf."""
    index = next(i for i, line in enumerate(roots) if " cert 1 " in line)
    fields = roots[index].split()
    boxes, cert = fields.index("boxes") + 1, fields.index("cert") + 1
    fields[boxes] = str(int(fields[boxes]) + 2)
    fields[cert] = str(int(fields[cert]) + 1)
    return [*roots[:index], " ".join(fields), *roots[index + 1 :]]


def test_a_mutated_s32_root_fails_the_audit_and_the_comparison(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    mutated = str(_s32_replay(tmp_path, "mutated.log", _deepen_one_root))
    code, audited = _run(capsys, "zmx2", "--case", "32", "--mode", "d4", mutated)
    assert code == 1
    assert audited["roots_present"] == 3600
    assert not audited["totals_equal_source_report"]
    code, compared = _run(capsys, "compare-zmx2", "--case", "32", "--records", mutated)
    assert code == 1
    assert len(compared["roots_whose_census_differs"]) == 1
    # A dropped root is caught by the audit; the comparison counts it and stays silent.
    dropped = str(_s32_replay(tmp_path, "dropped.log", lambda roots: roots[1:]))
    code, audited = _run(capsys, "zmx2", "--case", "32", "--mode", "d4", dropped)
    assert code == 1
    assert audited["roots_missing"] == 1


def test_an_s32_log_without_pair_points_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    fresh = _s32_replay(tmp_path, "fresh.log")
    grid = tmp_path / "grid.log"
    grid.write_text(
        fresh.read_text(encoding="ascii").replace("atoms=pairpts", "atoms=grid"),
        encoding="ascii",
    )
    code, compared = _run(capsys, "compare-zmx2", "--case", "32", "--records", str(grid))
    assert code == 1
    assert not compared["headers_equal"]
    assert comparison_clean(compared)
