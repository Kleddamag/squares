"""Audit Evan Daniel's mixed covers for ``s(21) = 5`` and ``s(45) = 7`` independently.

evand/square-packing at ``6aa82ba4`` proves both values with a *mixed cover*: point
masses plus mass spread uniformly along axis-parallel segments of the interior grid
lines, of total below ``n``, such that every closed unit square in ``[0, s]^2`` captures
mass at least one. Its two checkers, ``zm_mixed.py`` and ``zmx2``, decide that coverage
by subdividing pose space. The packet ``resources/web/evand-square-packing-2026-09-28/``
keeps the covers, both checkers' run records and this repository's replays.

This tool decides, with its own parser and exact integer arithmetic, the facts that do
not need a sweep, and re-reads the sweeps' records without the source's summarisers:

``cover``
    The file is mixed format v1 with no polygons. Every coordinate lies in ``[0, s]``,
    every mass is nonnegative, every segment is axis-parallel with positive length, and
    the total is the stated fraction and below ``n``. The measure is invariant under
    ``x -> s - x`` and ``x <-> y`` in two senses, both decided: entry by entry (points as
    a weighted multiset, segments as unordered endpoint pairs), which is the hypothesis
    of the source's Lean lemma ``MixedCover.d4InvM``, and as a measure (point masses by
    position, segment mass as a piecewise-constant density on each line). It also counts
    the points lying on a line that carries segment mass, which the source says is none.
``zmx2``
    A ``zmx2 cert`` log covers exactly the region its mode names, once per root, with no
    uncertified and no capped box. ``d4``: centre cells of pitch 1/10 over
    ``[0, s/2]^2`` by four ``u`` bins of width 1/8 over ``[0, 1/2]``; ``full``: the same
    over ``[0, s]^2``, for pass 0 (the cover) and pass 1 (its mirror ``y -> s - y``).
``zm-mixed``
    A ``zm_mixed.py --resume`` record file names the retained checker files and cover by
    SHA-256, carries the certificate-mode D4 settings, covers exactly the root grid of
    pitch 1/20 over ``[0, s/2]^2`` by sixteen ``u`` bins of width 1/32, once per root,
    and has no uncertified box.
``compare-zmx2``, ``compare-zm-mixed``
    Root for root, a replay's census equals the source's record of the same root, timing
    fields excepted. Source roots the replay did not run are counted, not failed, so a
    sample or a partial re-sweep compares as cleanly as a complete one.
``check``
    All of the above on the packet's retained files and receipts, and the fresh ``zmx2``
    runs on the source's ``s(13)`` and ``s(32)`` point covers, whose totals must equal
    the ones ``search/ZMX2.md`` reports; the source ships no log for those.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.audit_evand_mixed_covers check
    ... audit_evand_mixed_covers cover --case 45 [PATH]
    ... audit_evand_mixed_covers compare-zm-mixed --case 21 --records OUT/roots.jsonl

Every command prints JSON and exits 0 when the audit is clean, 1 otherwise. Files stored
as deterministic gzip are read through `devtools.retained_data.read_retained_bytes`, so a
path may name ``X`` or ``X.gz`` and every digest is that of the decompressed bytes.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import compressed_path, read_retained_bytes, retained_exists

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/evand-square-packing-2026-09-28"
UPSTREAM = PACKET / "square-packing/s12"
RECEIPTS = PACKET / "receipts"
CHECKER_FILES = ("zm_mixed.py", "mixed_cover.py", "zeromargin.py")
#: zmx2 census fields compared root for root; ``ms`` is timing and is left out.
ZMX2_CENSUS = ("boxes", "cert", "empty", "uncert", "maxdepth", "capped")
#: The zm_mixed.py settings every certificate-mode D4 record file must carry.
ZM_MIXED_SETTINGS = {
    "mode": "D4",
    "depth": 24,
    "pitch": "1/20",
    "ubins": 16,
    "chain": True,
    "chain_from": 0,
    "cert_mode": True,
    "split": True,
}


@dataclass(frozen=True, slots=True)
class Case:
    """One claim: the cover, the total the packet states, and where the records live."""

    n: int
    side: int
    bundle: str
    cover: str
    total: Fraction
    points: int
    segments: int

    @property
    def cover_path(self) -> Path:
        return UPSTREAM / "certificates" / self.bundle / self.cover


#: The two claims, with the totals and counts the source's READMEs state.
CASES = {
    21: Case(
        n=21,
        side=5,
        bundle="s21",
        cover="s21_mixed_cover_5.txt",
        total=Fraction(522368729933, 25 * 10**9),
        points=7536,
        segments=1872,
    ),
    45: Case(
        n=45,
        side=7,
        bundle="s45",
        cover="s45_mixed_cover_7.txt",
        total=Fraction(2238676387, 5 * 10**7),
        points=19989,
        segments=3912,
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(read_retained_bytes(path)).hexdigest()


def _display(path: Path) -> str:
    return str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path)


# --- the cover -------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MixedCover:
    """A mixed format v1 file as integers: side, denominators, points and segments."""

    side: Fraction
    denominator: int
    mass_denominator: int
    points: tuple[tuple[int, int, int], ...]
    segments: tuple[tuple[int, int, int, int, int], ...]
    polygons: int


def parse_cover(text: str) -> MixedCover:
    """Parse the format line by line; ``#`` starts a comment; every count must match."""
    rows = [line.split("#", 1)[0].split() for line in text.splitlines()]
    rows = [row for row in rows if row]
    if rows[0] != ["mixed", "1"]:
        raise ValueError(f"not mixed format v1: {rows[0]}")
    values = [[int(token) for token in row] for row in rows[1:]]

    def take(count: int, width: int) -> list[list[int]]:
        nonlocal values
        block, values = values[:count], values[count:]
        if len(block) != count or any(len(row) != width for row in block):
            raise ValueError(f"expected {count} rows of {width} integers")
        return block

    (side_num, side_den), (denominator,), (mass_denominator,) = take(1, 2)[0], *take(2, 1)
    (point_count,) = take(1, 1)[0]
    points = tuple((x, y, w) for x, y, w in take(point_count, 3))
    (segment_count,) = take(1, 1)[0]
    segments = tuple((a, b, c, d, w) for a, b, c, d, w in take(segment_count, 5))
    (polygon_count,) = take(1, 1)[0]
    if values[polygon_count:]:
        raise ValueError("trailing rows after the polygons")
    if side_den <= 0 or denominator <= 0 or mass_denominator <= 0:
        raise ValueError("denominators must be positive")
    return MixedCover(
        Fraction(side_num, side_den),
        denominator,
        mass_denominator,
        points,
        segments,
        polygon_count,
    )


Line = tuple[str, int]  # ("x", c): the vertical line x = c; ("y", c): the horizontal y = c.
Density = tuple[tuple[int, Fraction], ...]  # breakpoints along the line and density jumps


def _segment_line(segment: tuple[int, int, int, int, int]) -> tuple[Line, int, int]:
    x0, y0, x1, y1, _ = segment
    if x0 == x1 and y0 != y1:
        return ("x", x0), min(y0, y1), max(y0, y1)
    if y0 == y1 and x0 != x1:
        return ("y", y0), min(x0, x1), max(x0, x1)
    raise ValueError(f"segment is not axis-parallel with positive length: {segment}")


def line_densities(segments: tuple[tuple[int, int, int, int, int], ...]) -> dict[Line, Density]:
    """Each line's segment measure as a canonical piecewise-constant density.

    A segment of mass ``w`` and length ``L`` has density ``w / L`` on its extent; the
    measure on a line is the sum, recorded as sorted breakpoints with nonzero jumps, so
    two segment families define the same measure exactly when these agree.
    """
    jumps: dict[Line, defaultdict[int, Fraction]] = defaultdict(lambda: defaultdict(Fraction))
    for segment in segments:
        line, lo, hi = _segment_line(segment)
        rate = Fraction(segment[4], hi - lo)
        jumps[line][lo] += rate
        jumps[line][hi] -= rate
    out: dict[Line, Density] = {}
    for line, table in jumps.items():
        canonical = tuple((t, v) for t, v in sorted(table.items()) if v)
        if canonical:
            out[line] = canonical
    return out


def _reflect_density(density: Density, edge: int) -> Density:
    return tuple(sorted((edge - t, -v) for t, v in density))


def audit_cover(case: Case, path: Path | None = None) -> dict[str, Any]:
    """Everything about the cover that is decided without a sweep."""
    path = path or case.cover_path
    data = read_retained_bytes(path)
    cover = parse_cover(data.decode("ascii"))
    edge_fraction = cover.side * cover.denominator
    if edge_fraction.denominator != 1:
        raise ValueError("the side is not a multiple of 1/D")
    edge = edge_fraction.numerator
    problems: list[str] = []
    for x, y, w in cover.points:
        if not (0 <= x <= edge and 0 <= y <= edge and w >= 0):
            problems.append(f"point out of range or negative: {(x, y, w)}")
    for segment in cover.segments:
        x0, y0, x1, y1, w = segment
        if not all(0 <= v <= edge for v in (x0, y0, x1, y1)) or w < 0:
            problems.append(f"segment out of range or negative: {segment}")
        _segment_line(segment)
    point_mass = Fraction(sum(w for _, _, w in cover.points), cover.mass_denominator)
    segment_mass = Fraction(sum(s[4] for s in cover.segments), cover.mass_denominator)
    total = point_mass + segment_mass

    weights: Counter[tuple[int, int]] = Counter()
    for x, y, w in cover.points:
        weights[(x, y)] += w
    entries: Counter[tuple[tuple[int, int], tuple[int, int], int]] = Counter()
    for x0, y0, x1, y1, w in cover.segments:
        a, b = sorted(((x0, y0), (x1, y1)))
        entries[(a, b, w)] += 1

    def reflect(p: tuple[int, int]) -> tuple[int, int]:
        return (edge - p[0], p[1])

    def swap(p: tuple[int, int]) -> tuple[int, int]:
        return (p[1], p[0])

    def mapped_entries(g: Any) -> Counter[tuple[tuple[int, int], tuple[int, int], int]]:
        image: Counter[tuple[tuple[int, int], tuple[int, int], int]] = Counter()
        for (a, b, w), count in entries.items():
            ga, gb = sorted((g(a), g(b)))
            image[(ga, gb, w)] += count
        return image

    points_invariant = weights == Counter({reflect(p): w for p, w in weights.items()}) and (
        weights == Counter({swap(p): w for p, w in weights.items()})
    )
    entries_invariant = entries == mapped_entries(reflect) and entries == mapped_entries(swap)
    density = line_densities(cover.segments)
    reflected: dict[Line, Density] = {}
    swapped: dict[Line, Density] = {}
    for (axis, c), d in density.items():
        # x -> edge - x moves the vertical line x = c to x = edge - c and reverses the
        # horizontal lines' parameter; x <-> y exchanges the two families.
        reflected[("x", edge - c) if axis == "x" else ("y", c)] = (
            d if axis == "x" else _reflect_density(d, edge)
        )
        swapped[("y" if axis == "x" else "x", c)] = d
    measure_invariant = points_invariant and density == reflected and density == swapped

    vertical = {c for axis, c in density if axis == "x"}
    horizontal = {c for axis, c in density if axis == "y"}
    on_lines = sum(1 for x, y, _ in cover.points if x in vertical or y in horizontal)
    return {
        "cover": _display(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "side": str(cover.side),
        "coordinate_denominator": cover.denominator,
        "mass_denominator": cover.mass_denominator,
        "points": len(cover.points),
        "segments": len(cover.segments),
        "polygons": cover.polygons,
        "lines_carrying_segments": {
            "x": sorted(Fraction(c, cover.denominator).__str__() for c in vertical),
            "y": sorted(Fraction(c, cover.denominator).__str__() for c in horizontal),
        },
        "point_mass": str(point_mass),
        "segment_mass": str(segment_mass),
        "total": str(total),
        "total_decimal": f"{float(total):.9f}",
        "total_equals_stated": total == case.total,
        "total_below_n": total < case.n,
        "counts_as_stated": (len(cover.points), len(cover.segments))
        == (case.points, case.segments),
        "d4_invariant_entry_by_entry": points_invariant and entries_invariant,
        "d4_invariant_as_measure": measure_invariant,
        "points_on_segment_lines": on_lines,
        "problems": problems,
    }


def cover_clean(result: dict[str, Any]) -> bool:
    return (
        not result["problems"]
        and result["polygons"] == 0
        and result["total_equals_stated"]
        and result["total_below_n"]
        and result["counts_as_stated"]
        and result["d4_invariant_entry_by_entry"]
        and result["d4_invariant_as_measure"]
        and result["points_on_segment_lines"] == 0
    )


# --- zmx2 logs ---------------------------------------------------------------------------


def _stamp(path: Path) -> tuple[int, int]:
    """Size and mtime of the stored file, so a cached parse is dropped when it changes."""
    stored = path if path.is_file() else compressed_path(path)
    status = stored.stat()
    return status.st_size, status.st_mtime_ns


def read_zmx2(path: Path) -> tuple[str, dict[tuple[int, str], tuple[int, ...]], int]:
    """The header, each ROOT line's census keyed by (pass, root), and the UNCERT lines."""
    return _read_zmx2(path, _stamp(path))


@functools.lru_cache(maxsize=16)
def _read_zmx2(
    path: Path, stamp: tuple[int, int]
) -> tuple[str, dict[tuple[int, str], tuple[int, ...]], int]:
    del stamp
    header = ""
    census: dict[tuple[int, str], tuple[int, ...]] = {}
    uncert_lines = 0
    for line in read_retained_bytes(path).decode("ascii").splitlines():
        if line.startswith("# zmx2 cert"):
            header = header or line
        elif line.startswith("UNCERT "):
            uncert_lines += 1
        elif line.startswith("ROOT "):
            fields = line.split()
            record = dict(zip(fields[2::2], fields[3::2], strict=False))
            key = (int(record["pass"]), record["root"])
            if key in census:
                raise ValueError(f"{path}: root {key} recorded twice")
            census[key] = tuple(int(record[name]) for name in ZMX2_CENSUS)
    return header, census, uncert_lines


def zmx2_region(side: int, mode: str) -> set[tuple[int, str]]:
    cells = 5 * side if mode == "d4" else 10 * side
    passes = (0,) if mode == "d4" else (0, 1)
    return {
        (p, f"{i}/10,{i + 1}/10,{j}/10,{j + 1}/10,{k}/8,{k + 1}/8")
        for p in passes
        for i in range(cells)
        for j in range(cells)
        for k in range(4)
    }


def audit_zmx2(case: Case, path: Path, mode: str) -> dict[str, Any]:
    header, census, uncert_lines = read_zmx2(path)
    region = zmx2_region(case.side, mode)
    present = region & census.keys()
    fields = dict(zip(ZMX2_CENSUS, zip(*census.values(), strict=True), strict=True))
    return {
        "log": _display(path),
        "sha256": _sha256(path),
        "header": header,
        "mode": mode,
        "roots_in_region": len(region),
        "roots_present": len(present),
        "roots_missing": len(region - census.keys()),
        "roots_outside_region": len(census.keys() - region),
        "mode_in_header": f"mode={mode}" in header.split(),
        "boxes": sum(fields["boxes"]),
        "certified_leaves": sum(fields["cert"]),
        "empty_leaves": sum(fields["empty"]),
        "uncertified_boxes": sum(fields["uncert"]),
        "uncert_lines": uncert_lines,
        "capped_roots": sum(fields["capped"]),
        "max_depth": max(fields["maxdepth"]),
    }


def zmx2_clean(result: dict[str, Any]) -> bool:
    return (
        result["mode_in_header"]
        and result["roots_present"] == result["roots_in_region"]
        and result["roots_outside_region"] == 0
        and result["uncertified_boxes"] == 0
        and result["uncert_lines"] == 0
        and result["capped_roots"] == 0
    )


def compare_zmx2(shipped: Path, replay: Path) -> dict[str, Any]:
    source_header, source, _ = read_zmx2(shipped)
    replay_header, fresh, _ = read_zmx2(replay)
    common = fresh.keys() & source.keys()
    differ = sorted(key for key in common if fresh[key] != source[key])
    return {
        "shipped": _display(shipped),
        "shipped_sha256": _sha256(shipped),
        "replay": _display(replay),
        "replay_sha256": _sha256(replay),
        "headers_equal": source_header == replay_header,
        "shipped_roots": len(source),
        "replay_roots": len(fresh),
        "roots_compared": len(common),
        "roots_identical": len(common) - len(differ),
        "roots_whose_census_differs": [f"pass {p} root {r}" for p, r in differ[:50]],
        "replay_roots_not_in_shipped": len(fresh.keys() - source.keys()),
        "shipped_roots_not_replayed": len(source.keys() - fresh.keys()),
    }


# --- zm_mixed.py records -----------------------------------------------------------------


def read_zm_mixed(path: Path) -> tuple[dict[str, Any], dict[tuple[str, ...], dict[str, Any]]]:
    """The header line and each root's record; a torn last line is skipped.

    Parses are cached per file state; callers treat the returned mappings as read-only.
    """
    return _read_zm_mixed(path, _stamp(path))


@functools.lru_cache(maxsize=16)
def _read_zm_mixed(
    path: Path, stamp: tuple[int, int]
) -> tuple[dict[str, Any], dict[tuple[str, ...], dict[str, Any]]]:
    del stamp
    lines = [line for line in read_retained_bytes(path).decode("utf-8").splitlines() if line]
    header = json.loads(lines[0])
    if header.get("kind") != "zm_mixed cert header":
        raise ValueError(f"{path}: the first line is not a zm_mixed header")
    records: dict[tuple[str, ...], dict[str, Any]] = {}
    for index, line in enumerate(lines[1:], start=2):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            if index == len(lines):
                continue
            raise
        key = tuple(record["root"])
        if key in records:
            raise ValueError(f"{path}: root {key} recorded twice")
        records[key] = record
    return header, records


def zm_mixed_region(side: int) -> set[tuple[str, ...]]:
    cells = 10 * side  # pitch 1/20 over [0, side/2]
    return {
        (
            str(Fraction(i, 20)),
            str(Fraction(i + 1, 20)),
            str(Fraction(j, 20)),
            str(Fraction(j + 1, 20)),
            str(Fraction(k, 32)),
            str(Fraction(k + 1, 32)),
        )
        for i in range(cells)
        for j in range(cells)
        for k in range(16)
    }


def _census(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record["st"].items() if key != "cpu"}


def _differs(replay: dict[str, Any], source: dict[str, Any]) -> bool:
    """A root's leaf census or its uncertified boxes differ; CPU time is not compared."""
    return _census(replay) != _census(source) or replay["unc"] != source["unc"]


def audit_zm_mixed(case: Case, path: Path, checker_dir: Path | None = None) -> dict[str, Any]:
    header, records = read_zm_mixed(path)
    checker_dir = checker_dir or path.parent / "checker"
    expected = {name: _sha256(checker_dir / name) for name in CHECKER_FILES}
    expected["input"] = _sha256(case.cover_path)
    settings = header["settings"]
    region = zm_mixed_region(case.side)
    leaves: Counter[str] = Counter()
    max_depth = 0
    uncertified_roots = []
    cpu: list[float] = []
    for key, record in records.items():
        census = _census(record)
        max_depth = max(max_depth, census.pop("maxdepth"))
        leaves.update(census)
        cpu.append(float(record["st"]["cpu"]))
        if record["st"]["UNCERT"] or record["unc"]:
            uncertified_roots.append(",".join(key))
    cpu.sort()
    return {
        "records": _display(path),
        "sha256": _sha256(path),
        "header_sha256_match_retained_files": header["sha256"] == expected,
        "header_total": header["total"],
        "header_total_equals_stated": Fraction(header["total"]) == case.total,
        "settings_as_required": all(settings.get(k) == v for k, v in ZM_MIXED_SETTINGS.items()),
        "region_unrestricted": not any(settings.get("region", {}).values()),
        "roots_in_region": len(region),
        "roots_present": len(region & records.keys()),
        "roots_missing": len(region - records.keys()),
        "roots_outside_region": len(records.keys() - region),
        "uncertified_roots": uncertified_roots[:50],
        "census": dict(sorted({**leaves, "maxdepth": max_depth}.items())),
        "cpu_seconds": round(sum(cpu), 1),
        "cpu_seconds_per_root_quantiles": {
            q: round(cpu[min(len(cpu) - 1, int(q * len(cpu)))], 3)
            for q in (0.5, 0.9, 0.99, 1.0)
        }
        if cpu
        else {},
    }


def zm_mixed_clean(result: dict[str, Any]) -> bool:
    return (
        result["header_sha256_match_retained_files"]
        and result["header_total_equals_stated"]
        and result["settings_as_required"]
        and result["region_unrestricted"]
        and result["roots_present"] == result["roots_in_region"]
        and result["roots_outside_region"] == 0
        and not result["uncertified_roots"]
        and result["census"].get("UNCERT", 0) == 0
    )


def compare_zm_mixed(shipped: Path, replays: Sequence[Path]) -> dict[str, Any]:
    """Root for root against the source; ``replays`` may be several partial runs."""
    source_header, source = read_zm_mixed(shipped)
    fresh: dict[tuple[str, ...], dict[str, Any]] = {}
    headers_equal = settings_equal = True
    regions = []
    for replay in replays:
        replay_header, records = read_zm_mixed(replay)
        headers_equal &= source_header["sha256"] == replay_header["sha256"]
        settings_equal &= _settings_apart_from_region(replay_header) == (
            _settings_apart_from_region(source_header)
        )
        regions.append(replay_header["settings"].get("region"))
        if fresh.keys() & records.keys():
            raise ValueError(f"{replay}: a root is recorded in two replay files")
        fresh.update(records)
    common = fresh.keys() & source.keys()
    differ = sorted(key for key in common if _differs(fresh[key], source[key]))
    replay_cpu = sum(float(fresh[key]["st"]["cpu"]) for key in common)
    source_cpu = sum(float(source[key]["st"]["cpu"]) for key in common)
    return {
        "shipped": _display(shipped),
        "shipped_sha256": _sha256(shipped),
        "replays": [{"path": _display(r), "sha256": _sha256(r)} for r in replays],
        "header_sha256_equal": headers_equal,
        "settings_equal_apart_from_region": settings_equal,
        "replay_regions": regions,
        "shipped_roots": len(source),
        "replay_roots": len(fresh),
        "roots_compared": len(common),
        "roots_identical": len(common) - len(differ),
        "roots_whose_census_differs": [",".join(key) for key in differ[:50]],
        "replay_roots_not_in_shipped": len(fresh.keys() - source.keys()),
        "shipped_roots_not_replayed": len(source.keys() - fresh.keys()),
        "replay_cpu_seconds_on_compared_roots": round(replay_cpu, 1),
        "shipped_cpu_seconds_on_compared_roots": round(source_cpu, 1),
        "shipped_cpu_seconds_all_roots": round(
            sum(float(r["st"]["cpu"]) for r in source.values()), 1
        ),
    }


def _settings_apart_from_region(header: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in header["settings"].items() if k != "region"}


def comparison_clean(result: dict[str, Any]) -> bool:
    return (
        result["roots_compared"] > 0
        and result["roots_identical"] == result["roots_compared"]
        and result["replay_roots_not_in_shipped"] == 0
    )


# --- the packet --------------------------------------------------------------------------


def _bundle(case: Case) -> Path:
    return UPSTREAM / "certificates" / case.bundle


def sample_records(n: int) -> list[Path]:
    """The packet's sampled zm_mixed.py replays for ``s(n)``, one file per centre cell."""
    return sorted(RECEIPTS.glob(f"s{n}_zm_mixed_sample_*.jsonl"))


@dataclass(frozen=True, slots=True)
class PointCoverRun:
    """A fresh ``zmx2 --d4`` run on one of the source's plain point covers."""

    n: int
    side: int
    receipt: str
    #: Totals ``search/ZMX2.md`` section 9 reports for the source's run; it ships no log.
    boxes: int
    certified_leaves: int
    empty_leaves: int
    max_depth: int


#: The source's ``s(13)`` and ``s(32)`` point covers, which the previous packet retains.
POINT_COVER_RUNS = (
    PointCoverRun(13, 4, "s13_zmx2_d4_roots.log", 47162, 22136, 2245, 20),
    PointCoverRun(32, 6, "s32_zmx2_d4_pairpoints_roots.log", 1405342, 686886, 17585, 29),
)


def audit_point_cover_run(run: PointCoverRun) -> dict[str, Any]:
    """Region completeness, and the census totals against the ones the source reports."""
    case = Case(run.n, run.side, "", "", Fraction(0), 0, 0)
    result = audit_zmx2(case, RECEIPTS / run.receipt, "d4")
    result["totals_equal_source_report"] = (
        result["boxes"],
        result["certified_leaves"],
        result["empty_leaves"],
        result["max_depth"],
    ) == (run.boxes, run.certified_leaves, run.empty_leaves, run.max_depth)
    return result


def check_packet() -> dict[str, Any]:
    """The cover, shipped-record and receipt audits over the packet's retained files."""
    report: dict[str, Any] = {}
    clean = True
    for n, case in CASES.items():
        bundle = _bundle(case)
        entry: dict[str, Any] = {"cover": audit_cover(case)}
        clean &= cover_clean(entry["cover"])
        entry["shipped_zm_mixed"] = audit_zm_mixed(case, bundle / "zm_mixed_d4/roots.jsonl")
        clean &= zm_mixed_clean(entry["shipped_zm_mixed"])
        for mode in ("d4", "full"):
            shipped = bundle / f"zmx2_{mode}/roots.log"
            entry[f"shipped_zmx2_{mode}"] = audit_zmx2(case, shipped, mode)
            clean &= zmx2_clean(entry[f"shipped_zmx2_{mode}"])
            fresh = RECEIPTS / f"s{n}_zmx2_{mode}_roots.log"
            if retained_exists(fresh):
                entry[f"fresh_zmx2_{mode}"] = audit_zmx2(case, fresh, mode)
                compared = compare_zmx2(shipped, fresh)
                entry[f"fresh_zmx2_{mode}_vs_shipped"] = compared
                clean &= zmx2_clean(entry[f"fresh_zmx2_{mode}"])
                clean &= comparison_clean(compared)
                clean &= compared["shipped_roots_not_replayed"] == 0
        samples = sample_records(n)
        if samples:
            entry["zm_mixed_sample_vs_shipped"] = compare_zm_mixed(
                bundle / "zm_mixed_d4/roots.jsonl", samples
            )
            clean &= comparison_clean(entry["zm_mixed_sample_vs_shipped"])
        report[f"s{n}"] = entry
    for run in POINT_COVER_RUNS:
        if retained_exists(RECEIPTS / run.receipt):
            result = audit_point_cover_run(run)
            report[f"s{run.n}_point_cover_zmx2_d4"] = result
            clean &= zmx2_clean(result) and result["totals_equal_source_report"]
    report["clean"] = clean
    return report


def _emit(result: dict[str, Any], output: Path | None) -> None:
    text = json.dumps(result, indent=1) + "\n"
    if output is not None:
        with atomic_output_file(output) as handle:
            handle.write_text(text)
    print(text, end="")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--output", type=Path, help="also write the JSON here")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "check", parents=[common], help="audit the packet's retained files and receipts"
    )
    cover = commands.add_parser("cover", parents=[common], help="audit one mixed cover")
    cover.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    cover.add_argument("path", type=Path, nargs="?")
    zmx2 = commands.add_parser("zmx2", parents=[common], help="audit one zmx2 cert log")
    zmx2.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    zmx2.add_argument("--mode", choices=("d4", "full"), required=True)
    zmx2.add_argument("log", type=Path)
    zm = commands.add_parser(
        "zm-mixed", parents=[common], help="audit one zm_mixed.py record file"
    )
    zm.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    zm.add_argument("records", type=Path)
    zm.add_argument("--checker-dir", type=Path, help="default: checker/ beside the records")
    for name in ("compare-zmx2", "compare-zm-mixed"):
        compare = commands.add_parser(
            name, parents=[common], help="root-for-root census against the source"
        )
        compare.add_argument("--case", type=int, choices=sorted(CASES), required=True)
        compare.add_argument("--mode", choices=("d4", "full"), default="d4")
        compare.add_argument(
            "--records", type=Path, nargs="+", required=True, help="the replay's file(s)"
        )
        compare.add_argument("--shipped", type=Path, help="default: the packet's record")
    args = parser.parse_args()
    if args.command == "check":
        result = check_packet()
        _emit(result, args.output)
        return 0 if result["clean"] else 1
    case = CASES[args.case]
    if args.command == "cover":
        result = audit_cover(case, args.path)
        ok = cover_clean(result)
    elif args.command == "zmx2":
        result = audit_zmx2(case, args.log, args.mode)
        ok = zmx2_clean(result)
    elif args.command == "zm-mixed":
        result = audit_zm_mixed(case, args.records, args.checker_dir)
        ok = zm_mixed_clean(result)
    elif args.command == "compare-zmx2":
        shipped = args.shipped or _bundle(case) / f"zmx2_{args.mode}/roots.log"
        (records,) = args.records
        result = compare_zmx2(shipped, records)
        ok = comparison_clean(result)
    else:
        shipped = args.shipped or _bundle(case) / "zm_mixed_d4/roots.jsonl"
        result = compare_zm_mixed(shipped, args.records)
        ok = comparison_clean(result)
    _emit(result, args.output)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
