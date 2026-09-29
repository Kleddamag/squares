"""Audit and replay wand125's point-only s(21) and s(45) and mixed-rectangle s(50) certificates.

wand125/square-packing-bounds at ``39d8ecc`` adds three certificate families that are not
in Tokoharu's rectangle format:

- ``point_n45_L7``: a point measure proving ``s(45) = 7``, whose capture condition is
  decided by Evan Daniel's unmodified ``zmx2`` checker (``--d4 --pair-points``);
- ``point_n21_L5``: a point measure proving ``s(21) = 5`` with capture threshold
  ``249987/250000``, decided by the source's own rational replay of a 463 MB bundle; and
- ``certificates/mixed_n50_*``: rectangle-density measures proving ``s(50) >= 37/5`` (and
  the superseded ``147/20`` and ``3659/500``), decided by a research copy of Tokoharu's
  ``verify.cpp`` that accepts coverage ``>= 1``.

This tool is the first-party part. ``exact`` recomputes, from the packet's retained bytes
and without importing any source code, every premise that is plain arithmetic: each
measure's digest, format, nonnegativity, exact total and strict budget, the point
measures' D4 invariance, the ``s(21)`` threshold algebra and its support's link to
Daniel's certificate, the ``s(50)`` angle-net containment and the exact comparison with
Green's reported ``2√2 + 101/25 + 3√14/25``. It decides no coverage.

The other commands work on the source's own runs. ``n45-compare``, ``n21-compare`` and
``n50-compare`` read a replay's outputs and compare them with the source's records (for
``s(21)``, output file by output file against the pinned M1 linkage, also for the
finished stages of a run in progress). ``n50-bundle-check`` checks an unpacked bundle
against its ``files-sha256.json``; ``n50-inputs`` binds all 200 oblique inputs to the
exact candidate by an independent enclosure check; and ``n50-replay`` re-executes chosen
per-angle proofs by calling the shipped Python driver functions and C++ checker
unchanged. ``acquire`` rebuilds the retained subset and its digest list from a checkout
at the pinned revision, and ``host`` records the toolchain.

Usage, from ``packing/`` with the project interpreter::

    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed exact --check
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed acquire CHECKOUT
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n45-compare RUN_DIR --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n21-compare OUT_DIR \\
        --m1-linkage M1 [--stage root --stage sieve | --collect RECEIPTS] --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-bundle-check BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-inputs BUNDLE --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-replay BUNDLE \\
        --index 0 --index 150 --workers 2 --out F
    .venv/bin/python3 -m devtools.audit_wand125_point_and_mixed n50-compare BUNDLE --out F

Retained data files over 1,000 lines are stored as deterministic gzip, so every read goes
through `devtools.retained_data.read_retained_bytes` and every digest is the upstream one.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import platform
import re
import resource
import shutil
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any, cast

from strif import atomic_write_text

from devtools.retained_data import (
    GZIP_SUFFIX,
    LINE_THRESHOLD,
    compress,
    describe,
    git_blob,
    read_retained_bytes,
)

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/wand125-point-and-mixed-2026-09-28"
SOURCE = PACKET / "square-packing-bounds"
MANIFEST = PACKET / "acquisition/sources.json"
SUBTREE = PACKET / "acquisition/upstream-subtree.sha256"
EXACT_RECEIPT = PACKET / "receipts/exact-audit.json"
REVISION = "39d8ecc74d651b54ec977c331c8f2015b442a6c4"
GIT_TREE = "936e2524c09ca137cf9e02dcd955d6737549253b"
SOURCE_URL = "https://github.com/wand125/square-packing-bounds"

#: The same repository's MIT licence, retained byte-identical with the rectangle packet.
RECTANGLE_LICENSE = (
    REPO / "packing/resources/web/wand125-rectangle-certificates-2026-09-27/wand125-rectangles"
) / "LICENSE"
#: Daniel's s(21) certificate, retained by the evand packet; the n21 support derives from it.
EVAND_S21 = (
    REPO / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
) / "certificates/s21/s21_lower_4.9950.txt"

N45 = Path("point_n45_L7")
N21 = Path("point_n21_L5")
N50 = {
    "L740": Path("certificates/mixed_n50_L740"),
    "L735": Path("certificates/mixed_n50_L735"),
    "L7318": Path("certificates/mixed_n50_L7318"),
}
CLAIM_DIRS = (N45, N21, *N50.values())
TOP_FILES = (Path("README.md"), Path("LICENSE"))

#: zmx2 as the n45 verify.sh pins it: evand/square-packing commit and source digest.
ZMX2_COMMIT = "6e1223cf7ef2be4c70baaa36c0e7e7197076735a"
ZMX2_SOURCE_SHA256 = "6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed"

N45_COVER_SHA256 = "f7d706aa07506c351d9c4b76082cc391ae3f1fd20f6759496bd7c601bb0ca192"
N45_TOTAL = Fraction(12666371418707823, 2**48)
N21_HASHES = {
    "n21-original.txt": "84a7dae793f05ff72de52ddcd3058e8518c1f84c461f94d11305adefe6137679",
    "n21-capture-one.txt": "9f631fbae420e0376ea636a232b7680e937deebe205dc035cfb9c43a3d74b456",
    "upstream-s21-lower-4.9950.txt": (
        "c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef"
    ),
}
N21_THRESHOLD = Fraction(249987, 250000)
N21_MASS = Fraction(2624862500021, 125000000000)
N21_GAP = Fraction(999979, 125000000000)

#: (side, rectangle count, manifest digest) the source states for each n = 50 rung.
N50_CLAIMS: dict[str, tuple[Fraction, int, str]] = {
    "L740": (
        Fraction(37, 5),
        553,
        "fdfaed937a788e0f2dcd45689927c59ffe62b1436aa06a4363a0ea6dd1a53fda",
    ),
    "L735": (
        Fraction(147, 20),
        499,
        "441c2612d81472a79f949f5cd453d2eb171c37faf0c34314ad309f77c0db0836",
    ),
    "L7318": (
        Fraction(3659, 500),
        355,
        "c0f46b688122f43b73e9ee63729900d6f2370b912452489ef2dd681ef9a67088",
    ),
}
N50_MASS = Fraction(4999999, 100000)
N50_STEP = Fraction(83, 40000)
N50_LAST = 200
#: ``code/mixed_rotated_verify.cpp``, the checker the L740 and L7318 manifests name.
N50_CHECKER_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
N50_TARBALLS = {
    "L740": "n50-L7.40-proof-bundle.tar.gz",
    "L735": "n50-L7.35-proof-bundle.tar.gz",
    "L7318": "n50-L7.318-proof-bundle.tar.gz",
}


def _pinned_only(path: Path) -> str | None:
    """Why an upstream file under the claim directories is pinned by digest and not copied."""
    parts = path.parts
    rules = (
        (
            path == Path("README.md"),
            "retained byte-identical by the 2026-09-28 rectangle packet",
        ),
        (
            path == Path("LICENSE"),
            "retained byte-identical by the 2026-09-27 rectangle packet",
        ),
        (
            parts[:2] == ("point_n21_L5", "data"),
            "n21 proof bundle archive part (463,568,316 bytes in 14 parts)",
        ),
        (
            parts[:2] == ("point_n21_L5", "verifier-source"),
            "readable copy of the bundle's Python, checked against it by unpack_bundle.py",
        ),
        (
            parts[:2] == ("point_n21_L5", "acceptance")
            and path.name.endswith("-linkage.json.gz"),
            "historical linkage record (about 5 MB compressed each)",
        ),
        (
            path == Path("point_n21_L5/lean/Sqpack/N21PtsData.lean"),
            "generated from n21-original.txt by the retained gen_n21pts_data.py",
        ),
        (
            parts[0] == "certificates" and path.name.endswith(".tar.gz"),
            "complete proof bundle (12.8 to 21.8 MB)",
        ),
        (
            parts[:3] == ("certificates", "mixed_n50_L7318", "code"),
            "byte-identical to certificates/mixed_n50_L740/code/",
        ),
    )
    return next((reason for matched, reason in rules if matched), None)


# --------------------------------------------------------------------------- helpers


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(relative: Path, source: Path = SOURCE) -> bytes:
    return read_retained_bytes(source / relative)


def _json(relative: Path, source: Path = SOURCE) -> Any:
    return json.loads(_read(relative, source))


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_subtree_manifest(path: Path = SUBTREE) -> dict[Path, str]:
    """Parse the ``sha256sum``-style list of ``./``-relative upstream paths."""
    expected: dict[Path, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, separator, name = line.partition("  ")
        relative = Path(name.removeprefix("./"))
        _require(
            bool(separator)
            and re.fullmatch(r"[0-9a-f]{64}", digest) is not None
            and name.startswith("./")
            and not relative.is_absolute()
            and ".." not in relative.parts
            and relative not in expected,
            f"invalid or duplicate subtree entry: {line!r}",
        )
        expected[relative] = digest
    _require(bool(expected), "empty subtree manifest")
    return expected


def retained_files(source: Path = SOURCE) -> dict[Path, bytes]:
    """Every retained upstream file, keyed by its upstream path, decompressed."""
    files: dict[Path, bytes] = {}
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        if relative.name.endswith(GZIP_SUFFIX):
            relative = relative.with_name(relative.name.removesuffix(GZIP_SUFFIX))
        _require(relative not in files, f"retained twice, plain and compressed: {relative}")
        files[relative] = read_retained_bytes(path)
    return files


# --------------------------------------------------------------------------- n = 45


def n45_cover(data: bytes, provenance: dict[str, Any]) -> dict[str, Any]:
    """Format, nonnegativity, D4 invariance and exact total of the n45 point cover."""
    _require(_sha256(data) == N45_COVER_SHA256, "cover.txt SHA-256 differs from the pin")
    _require(
        provenance.get("cover_sha256") == N45_COVER_SHA256, "provenance pins another cover"
    )
    values = [int(token) for token in data.split()]
    side_num, side_den, denominator, weight_den, count = values[:5]
    _require((side_num, side_den) == (7, 1), "container side is not 7")
    _require(denominator > 0 and weight_den > 0, "nonpositive denominator")
    _require(len(values) == 5 + 3 * count, "entry count disagrees with the header")
    span = 7 * denominator
    mass: Counter[tuple[int, int]] = Counter()
    for index in range(5, len(values), 3):
        x, y, w = values[index : index + 3]
        _require(0 <= x <= span and 0 <= y <= span, f"point outside [0,7]^2: {(x, y)}")
        _require(w >= 0, "negative weight")
        mass[x, y] += w
    for (x, y), w in mass.items():
        for image in ((span - x, y), (x, span - y), (y, x)):
            _require(mass.get(image, 0) == w, f"not D4-invariant at {(x, y)}")
    total = Fraction(sum(mass.values()), weight_den)
    _require(total == N45_TOTAL, "total differs from 12666371418707823/2^48")
    _require(str(total) == provenance.get("total"), "total differs from provenance.json")
    _require(total < 45, "total is not below 45")
    return {
        "sha256": N45_COVER_SHA256,
        "entries": count,
        "distinct_points": len(mass),
        "positive_points": sum(1 for w in mass.values() if w > 0),
        "coordinate_denominator": denominator,
        "weight_denominator": weight_den,
        "total": str(total),
        "total_float": float(total),
        "margin_below_45": str(45 - total),
        "d4_invariant": True,
        "coverage_decided_here": False,
    }


_ROOT_LINE = re.compile(
    r"ROOT (\d+) pass (\d+) root (\S+) boxes (\d+) cert (\d+) empty (\d+) uncert (\d+) "
    r"maxdepth (\d+) capped (\d+) ms (\d+)"
)


def n45_compare(run_dir: Path, provenance: dict[str, Any]) -> dict[str, Any]:
    """Compare a ``verify.sh`` run directory with the source's reference run."""
    roots_log = read_retained_bytes(run_dir / "roots.log")
    lines = roots_log.decode("ascii").splitlines()
    rows = [_ROOT_LINE.fullmatch(line) for line in lines if line.startswith("ROOT ")]
    _require(all(rows), "unparsed ROOT line")
    matches = [row for row in rows if row is not None]
    roots = {(m[2], m[3]) for m in matches}
    run_log = read_retained_bytes(run_dir / "run.log").decode("utf-8")
    verdicts = [line for line in run_log.splitlines() if line.startswith("VERIFIED-D4:")]
    reference = provenance["reference_run"]
    summary = {
        "root_lines": len(matches),
        "distinct_roots": len(roots),
        "boxes": sum(int(m[4]) for m in matches),
        "certified_leaves": sum(int(m[5]) for m in matches),
        "empty_leaves": sum(int(m[6]) for m in matches),
        "uncertified": sum(int(m[7]) for m in matches),
        "max_depth": max(int(m[8]) for m in matches),
        "capped": sum(int(m[9]) for m in matches),
        "root_ms_sum": sum(int(m[10]) for m in matches),
        "verdict_line": verdicts[-1] if verdicts else None,
        "not_verified_lines": run_log.count("NOT VERIFIED"),
        "roots_log_sha256": _sha256(roots_log),
    }
    agreement = {
        "roots": summary["distinct_roots"] == reference["roots"] == len(matches),
        "uncertified": summary["uncertified"] == reference["uncertified"] == 0,
        "capped": summary["capped"] == reference["capped"] == 0,
        "boxes": summary["boxes"] == reference["boxes"],
        "max_depth": summary["max_depth"] == reference["max_depth"],
        "verdict": bool(verdicts) and summary["not_verified_lines"] == 0,
    }
    return {
        "status": "MATCHES_SOURCE_REFERENCE" if all(agreement.values()) else "DIFFERS",
        "replay": summary,
        "reference": reference,
        "agreement": agreement,
        "note": (
            "The roots log carries per-root milliseconds, so its digest cannot equal the "
            "source's roots_sha256; the box and depth totals are compared instead."
        ),
    }


# --------------------------------------------------------------------------- n = 21


def _points(data: bytes) -> tuple[Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    a, b, d, w, n, *values = (int(token) for token in data.split())
    _require(min(a, b, d, w) > 0 and n >= 0 and len(values) == 3 * n, "invalid point header")
    side = Fraction(a, b)
    points = [
        (Fraction(x, d), Fraction(y, d), Fraction(v, w))
        for x, y, v in zip(values[::3], values[1::3], values[2::3], strict=True)
    ]
    for x, y, v in points:
        _require(0 <= x <= side and 0 <= y <= side and v >= 0, "invalid point or weight")
    return side, points


def n21_certificates(source: Path = SOURCE) -> dict[str, Any]:
    """The n21 point measure's exact algebra, recomputed from the retained files."""
    raw = {name: _read(N21 / "certificates" / name, source) for name in N21_HASHES}
    for name, data in raw.items():
        _require(_sha256(data) == N21_HASHES[name], f"{name} SHA-256 differs from the pin")
    side, original = _points(raw["n21-original.txt"])
    normalized_side, normalized = _points(raw["n21-capture-one.txt"])
    upstream_side, upstream = _points(raw["upstream-s21-lower-4.9950.txt"])
    _require(side == normalized_side == 5, "container side is not 5")
    _require(upstream_side == Fraction(5000, 1001), "Daniel's side is not 5000/1001")
    _require(len(original) == len(normalized) == len(upstream) == 4604, "entry count")
    q = N21_THRESHOLD
    _require(
        normalized == [(x, y, v / q) for x, y, v in original], "normalized != original / q"
    )
    scale = Fraction(1001, 1000)
    _require(
        [(x, y) for x, y, _ in original] == [(x * scale, y * scale) for x, y, _ in upstream],
        "support is not Daniel's, scaled by 1001/1000 in the same order",
    )
    weights = {(x, y): v for x, y, v in original}
    _require(len(weights) == 4604, "coordinates are not distinct")
    for (x, y), v in weights.items():
        for image in ((5 - x, y), (x, 5 - y), (y, x)):
            _require(weights.get(image) == v, f"not D4-invariant at {(x, y)}")
    mass = sum(weights.values(), Fraction(0))
    _require(mass == N21_MASS, "mass differs from 2624862500021/125000000000")
    gap = 21 * q - mass
    _require(gap == N21_GAP and gap > 0, "21q - mass is not 999979/125000000000")
    evand = read_retained_bytes(EVAND_S21)
    _require(evand == raw["upstream-s21-lower-4.9950.txt"], "evand packet copy differs")
    check = _json(N21 / "certificate-data-check.json", source)
    _require(check["mass"] == str(mass) and check["strict_gap"] == str(gap), "data check")
    return {
        "hashes": N21_HASHES,
        "entries": len(original),
        "positive_entries": sum(1 for v in weights.values() if v > 0),
        "zero_entries": sum(1 for v in weights.values() if v == 0),
        "threshold": str(q),
        "mass": str(mass),
        "normalized_mass": str(mass / q),
        "strict_gap": str(gap),
        "strict_gap_float": float(gap),
        "d4_invariant": True,
        "support_is_evand_s21_scaled_by": str(scale),
        "evand_packet_copy_identical": True,
        "coverage_decided_here": False,
    }


#: The M1 run's complete linkage record, pinned by digest (compressed, decompressed).
M1_LINKAGE_SHA256 = (
    "0d93072b65c1b162e1cba99db64a14b7f85e21f50b98da720247d3234c665f02",
    "6efc5fe539db5a37ec1ac0851271cee4c51dc5912d886d059ef253769bf7e0dc",
)
_STAGE_DIR = re.compile(r"/(root|sieve|frontier-s\d+)/(.+)$")


def _stage_relative(bindings: dict[str, str]) -> dict[str, str]:
    """Output bindings keyed by the path below the stage directory, not the run root."""
    relative: dict[str, str] = {}
    for path, digest in bindings.items():
        match = _STAGE_DIR.search(path)
        _require(match is not None, f"output outside a stage directory: {path}")
        assert match is not None
        key = f"{match[1]}/{match[2]}"
        _require(key not in relative, f"output bound twice: {key}")
        relative[key] = digest
    return relative


def compare_outputs(linkage: Path, m1_linkage: Path) -> dict[str, Any]:
    """Every output file of a fresh run against the M1 run's, by stage-relative path."""
    packed = m1_linkage.read_bytes()
    raw = gzip.decompress(packed)
    _require((_sha256(packed), _sha256(raw)) == M1_LINKAGE_SHA256, "M1 linkage is not pinned")
    ours = _stage_relative(json.loads(linkage.read_text())["output_bindings"])
    theirs = _stage_relative(json.loads(raw)["output_bindings"])
    shared = set(ours) & set(theirs)
    differing = sorted(key for key in shared if ours[key] != theirs[key])
    return {
        "outputs_here": len(ours),
        "outputs_m1": len(theirs),
        "identical": len(shared) - len(differing),
        "differing": len(differing),
        "differing_names": sorted({Path(key).name for key in differing}),
        "differing_examples": differing[:12],
        "only_here": sorted(set(ours) - set(theirs))[:12],
        "only_m1": sorted(set(theirs) - set(ours))[:12],
    }


#: What a finished ``verify_portable.py`` output directory contributes to the receipts.
N21_RECEIPT_FILES = ("result.json", "run-inputs.json")


def n21_collect(out: Path, receipts: Path, m1_linkage: Path | None) -> dict[str, Any]:
    """Copy a finished run's summary, exit records and stage logs into ``receipts``.

    The comparison is written as ``comparison.json``; logs over the line threshold are
    stored as deterministic gzip. Proof objects and ``linkage.json`` stay in ``out``;
    the comparison records their digests.
    """
    result = n21_compare(out, m1_linkage=m1_linkage)
    receipts.mkdir(parents=True, exist_ok=True)
    names = [*N21_RECEIPT_FILES, *(p.name for p in sorted(out.glob("*-exit.json")))]
    names += [p.name for p in sorted(out.glob("*.log"))]
    stored: list[str] = []
    rows: list[str] = []
    for name in names:
        target = receipts / name
        shutil.copyfile(out / name, target)
        if (
            target.suffix in {".json", ".log"}
            and target.read_bytes().count(b"\n") > LINE_THRESHOLD
        ):
            target = compress(target)
            rows.append(describe(PACKET, target, "receipt").markdown())
        stored.append(target.name)
    atomic_write_text(
        receipts / "comparison.json", json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result | {"stored": stored, "compressed_file_rows": rows}


def compare_stage_files(out: Path, m1_linkage: Path, stages: list[str]) -> dict[str, Any]:
    """Hash the files a run has written so far under ``stages`` and compare with M1's.

    Works on an unfinished run: only the named, completed stage directories are read.
    """
    packed = m1_linkage.read_bytes()
    raw = gzip.decompress(packed)
    _require((_sha256(packed), _sha256(raw)) == M1_LINKAGE_SHA256, "M1 linkage is not pinned")
    theirs = _stage_relative(json.loads(raw)["output_bindings"])
    report: dict[str, Any] = {}
    for stage in stages:
        ours = {
            f"{stage}/{path.relative_to(out / stage).as_posix()}": _sha256(path.read_bytes())
            for path in sorted((out / stage).rglob("*"))
            if path.is_file()
        }
        expected = {key: value for key, value in theirs.items() if key.startswith(f"{stage}/")}
        shared = set(ours) & set(expected)
        differing = sorted(key for key in shared if ours[key] != expected[key])
        report[stage] = {
            "files_here": len(ours),
            "files_m1": len(expected),
            "identical": len(shared) - len(differing),
            "differing": differing[:12],
            "only_here": sorted(set(ours) - set(expected))[:12],
            "only_m1": sorted(set(expected) - set(ours))[:12],
        }
    return {"status": "STAGE_FILES_COMPARED", "stages": report}


def n21_compare(
    out: Path, source: Path = SOURCE, m1_linkage: Path | None = None
) -> dict[str, Any]:
    """Compare a fresh ``verify_portable.py`` run with the source's M1 record."""
    reference = _json(N21 / "acceptance/m1-full-replay.json", source)
    result = json.loads((out / "result.json").read_text())
    run_inputs = json.loads((out / "run-inputs.json").read_text())
    exits = [json.loads(path.read_text()) for path in sorted(out.glob("*-exit.json"))]
    keys = (
        "status",
        "candidate_sha256",
        "root_count",
        "sieve_count",
        "frontier_count",
        "excluded_count",
        "threshold",
        "mass",
        "strict_gap",
        "independent_external_review",
        "formal_verification",
    )
    agreement = {key: result.get(key) == reference.get(key) for key in keys}
    agreement["all_stages_exit_zero"] = bool(exits) and all(
        item["exit_code"] == 0 for item in exits
    )
    linkage = out / "linkage.json"
    stages = [
        {
            "stage": item["stage"],
            "shard": item["shard"],
            "exit_code": item["exit_code"],
            "seconds": item["seconds"],
        }
        for item in exits
    ]
    outputs = compare_outputs(linkage, m1_linkage) if m1_linkage else None
    return {
        "status": "MATCHES_SOURCE_M1_RECORD" if all(agreement.values()) else "DIFFERS",
        "agreement": agreement,
        "outputs_against_m1": outputs,
        "replay": {key: result.get(key) for key in keys}
        | {
            "seconds": result.get("seconds"),
            "workers": run_inputs.get("workers"),
            "python": run_inputs.get("python"),
            "platform": run_inputs.get("platform"),
            "bindings": run_inputs.get("bindings"),
            "stages": stages,
            "linkage_sha256": _sha256(linkage.read_bytes()) if linkage.exists() else None,
            "result_sha256": _sha256((out / "result.json").read_bytes()),
        },
        "reference": {key: reference.get(key) for key in (*keys, "seconds", "linkage_sha256")}
        | {
            "stages": [
                {key: item[key] for key in ("stage", "shard", "exit_code", "seconds")}
                for item in reference["worker_exits"]
            ]
        },
        "note": (
            "Linkage records embed absolute output paths and per-run output digests, so "
            "their SHA-256 differs between runs; the certified quantities are compared."
        ),
    }


# --------------------------------------------------------------------------- n = 50


def _n50_measure(data: dict[str, Any]) -> tuple[Fraction, Fraction, list[tuple[Any, ...]]]:
    """(L, B, [(x0, y0, x1, y1, mass)]) for either upstream candidate schema."""
    side, core = Fraction(data["L"]), Fraction(data["B"])
    if "rectangles" in data:
        _require(not data.get("points"), "unexpected point masses")
        records, key = data["rectangles"], "rectangle"
    else:
        _require(data.get("schema") == "point_line_rectangle_v1", "unknown candidate schema")
        records, key = data["primitives"], "geometry"
        _require(all(r["kind"] == "rectangle" for r in records), "non-rectangle primitive")
    items = [(*map(Fraction, r[key]), Fraction(r["mass"])) for r in records]
    return side, core, items


def _semantic_digest(data: dict[str, Any]) -> str:
    """The source's candidate digest (mixed_density_check.expand), recomputed."""
    keys = ["n", "L", "B", "rectangles", "points", "total_mass"]
    if "proof_net" in data:
        keys.append("proof_net")
    semantic = {key: data[key] for key in keys}
    text = json.dumps(semantic, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode()).hexdigest()


def exceeds_green(value: Fraction) -> bool:
    """Whether ``value > 2√2 + 101/25 + 3√14/25``, decided in exact rational arithmetic.

    With ``x = value - 101/25`` the claim is ``x > 2√2 + (3/25)√14``. Both sides are
    positive, so it is ``x > 0`` and ``x² - 8 - 126/625 > (12/25)√28``, and squaring once
    more removes the last root. Equality is impossible for a rational ``value``.
    """
    x = value - Fraction(101, 25)
    if x <= 0:
        return False
    y = x * x - 8 - Fraction(126, 625)
    return y > 0 and y * y > Fraction(144, 625) * 28


def green_bounds(digits: int = 30) -> tuple[Fraction, Fraction]:
    """Rational bounds on Green's value from integer square roots at ``digits`` places."""
    scale = 10**digits
    root2, root14 = isqrt(2 * scale * scale), isqrt(14 * scale * scale)
    low = Fraction(2 * root2, scale) + Fraction(101, 25) + Fraction(3 * root14, 25 * scale)
    high = low + Fraction(2, scale) + Fraction(3, 25 * scale)
    return low, high


def n50_net(core: Fraction) -> dict[str, str]:
    """The angle-net containment facts ``mixed_net_audit.net_certificate`` asserts."""
    end = N50_STEP * N50_LAST
    _require(0 < core < 1 and (1 + end) ** 2 >= 2, "net does not reach tan(pi/8)")
    _require((1 + (N50_LAST - Fraction(1, 2)) * N50_STEP) ** 2 < 2, "last node unassigned")
    bound = core * (1 + N50_STEP)
    _require(bound < 1, "core containment is not strict")
    return {
        "step": str(N50_STEP),
        "count": str(N50_LAST + 1),
        "endpoint_check": str((1 + end) ** 2 - 2),
        "rotated_side_upper": str(bound),
        "side_margin": str(1 - bound),
    }


def n50_centre_domains(side: Fraction, core: Fraction) -> dict[str, Any]:
    """How far the mixed checker's centre domain sits inside verify.cpp's, per net node.

    verify.cpp checks core centres in ``[L/2, L - a_core]`` with ``a_core = B(c+s)/2`` at
    the node. The mixed driver supplies ``E = L/2 - r`` instead, where ``r`` is the half
    axis extent of the containing unit square at the lower end of the node's bin, so it
    checks ``[L/2, L - r]``. Both are the quarter-turn reduction of the full domain.
    """
    widths: list[Fraction] = []
    for index in range(1, N50_LAST + 1):
        t = index * N50_STEP
        a = max(Fraction(0), t - N50_STEP / 2)
        radius = (1 + 2 * a - a * a) / (2 * (1 + a * a))
        core_radius = core * (1 + 2 * t - t * t) / (2 * (1 + t * t))
        _require(radius >= core_radius, f"unit-square radius below core radius at {index}")
        widths.append(radius - core_radius)
    return {
        "nodes": N50_LAST,
        "eliminated_width_min": str(min(widths)),
        "eliminated_width_min_float": float(min(widths)),
        "eliminated_width_max": str(max(widths)),
        "eliminated_width_max_float": float(max(widths)),
        "axis_domain": f"[{side / 2}, {side - Fraction(1, 2)}]^2",
    }


def _certificate_minimum(certificate: dict[str, Any]) -> tuple[float | None, str | None]:
    """The least per-angle lower bound the certificate records, if it records them."""
    records = certificate["results"]
    _require(len(records) == N50_LAST + 1, "certificate does not carry 201 records")
    lows = [
        (float(value), index)
        for index, record in records.items()
        if (value := record.get("lower", record.get("integer_minimum"))) is not None
    ]
    if not lows:
        return None, None
    _require(len(lows) == N50_LAST + 1, "some records carry no lower bound")
    return min(lows)


#: The source's own audit record for a rung, where it ships one.
N50_AUDITS = {"L740": "completion-audit.json", "L735": "final-audit.json"}


def _n50_source_audit(name: str, source: Path) -> dict[str, Any] | None:
    """Bind the source's audit record to the retained certificate and pinned tarball.

    Its Green upper bound must be a true upper bound (``exceeds_green``) and its
    improvement exactly ``L`` minus that bound.
    """
    if name not in N50_AUDITS:
        return None
    directory = N50[name]
    record = _json(directory / N50_AUDITS[name], source)
    side = N50_CLAIMS[name][0]
    upper = Fraction(record["green_upper"])
    certificate = _sha256(_read(directory / "certificate.json", source))
    tree = read_subtree_manifest()
    _require(record["certificate_sha256"] == certificate, "audit binds another certificate")
    _require(exceeds_green(upper), "the source's Green upper bound is not an upper bound")
    _require(Fraction(record["improvement_lower"]) == side - upper, "improvement differs")
    archive = record.get("archive_sha256")
    _require(
        archive is None or archive == tree[directory / N50_TARBALLS[name]],
        "audit binds another tarball",
    )
    return {
        "file": N50_AUDITS[name],
        "status": record["status"],
        "certificate_sha256_matches": True,
        "archive_sha256_checked": archive is not None,
        "green_upper_is_upper_bound": True,
        "improvement_lower_float": float(Fraction(record["improvement_lower"])),
    }


def n50_certificate(name: str, source: Path = SOURCE) -> dict[str, Any]:
    """Exact premises of one n50 rung; coverage is the source checker's."""
    side, count, digest = N50_CLAIMS[name]
    directory = N50[name]
    data = _json(directory / "candidate.json", source)
    manifest = _json(directory / "manifest.json", source)
    certificate = _json(directory / "certificate.json", source)
    candidate_side, core, items = _n50_measure(data)
    _require(candidate_side == side and core == Fraction(9977, 10000), "side or core differs")
    _require(len(items) == count, "rectangle count differs from the source's statement")
    for x0, y0, x1, y1, mass in items:
        _require(0 <= x0 < x1 <= side and 0 <= y0 < y1 <= side, "rectangle outside container")
        _require(mass >= 0, "negative mass")
    total = sum((item[4] for item in items), Fraction(0))
    _require(total == Fraction(data["total_mass"]) == N50_MASS, "total differs")
    _require(total < 50 and data["n"] == 50, "total is not below 50")
    _require(
        manifest["candidate_digest"] == certificate["candidate_digest"] == digest, "digest"
    )
    if "rectangles" in data:
        _require(_semantic_digest(data) == digest, "recomputed candidate digest differs")
        checker = N50["L740"] / "code/mixed_rotated_verify.cpp"
        _require(
            manifest["source_sha256"] == _sha256(_read(checker, source)) == N50_CHECKER_SHA256,
            "the manifest names another checker",
        )
    _require(exceeds_green(side), "side does not exceed Green's bound")
    low, high = green_bounds()
    minimum, at = _certificate_minimum(certificate)
    _require(minimum is None or minimum >= 1, "a recorded per-angle lower bound is below 1")
    audit_record = _n50_source_audit(name, source)
    return {
        "side": str(side),
        "side_float": float(side),
        "core": str(core),
        "rectangles": count,
        "total_mass": str(total),
        "budget_gap": str(50 - total),
        "candidate_digest": digest,
        "digest_recomputed": "rectangles" in data,
        "checker_sha256": manifest["source_sha256"],
        "exceeds_green": True,
        "excess_over_green_lower": str(side - high),
        "excess_over_green_lower_float": float(side - high),
        "green_interval_30_digits": [float(low), float(high)],
        "net": n50_net(core),
        "centre_domains": n50_centre_domains(side, core),
        "certificate_status": certificate["status"],
        "recorded_minimum_lower": minimum,
        "recorded_minimum_at": at,
        "source_audit": audit_record,
        "coverage_decided_here": False,
    }


def check_bundle_hashes(bundle: Path) -> dict[str, Any]:
    """Every entry of an n50 bundle's ``files-sha256.json`` against the unpacked files.

    Run it on a pristine unpacking: the shipped checker writes into ``proof/``.
    """
    listing = json.loads((bundle / "files-sha256.json").read_text())
    present = {
        str(path.relative_to(bundle)) for path in bundle.rglob("*") if path.is_file()
    } - {"files-sha256.json"}
    mismatched = sorted(
        name
        for name, digest in listing.items()
        if not (bundle / name).is_file() or _sha256((bundle / name).read_bytes()) != digest
    )
    unlisted = sorted(present - set(listing))
    return {
        "status": "BUNDLE_FILES_MATCH" if not mismatched and not unlisted else "DIFFERS",
        "listed": len(listing),
        "mismatched": mismatched[:20],
        "unlisted": unlisted[:20],
    }


def d4_images(side: Fraction, items: list[tuple[Any, ...]]) -> list[tuple[Fraction, ...]]:
    """Each rectangle's eight D4 images with density ``m/(8|R|)``, in the source's order.

    The order is the source's convention (``mixed_density_check.expand``); the values are
    computed here from the candidate.
    """
    images: list[tuple[Fraction, ...]] = []
    for x0, y0, x1, y1, mass in items:
        rho = mass / (8 * (x1 - x0) * (y1 - y0))
        for swap in (False, True):
            a, b, c, d = (y0, x0, y1, x1) if swap else (x0, y0, x1, y1)
            for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                u, v = (a, c) if sx == 1 else (side - c, side - a)
                w, z = (b, d) if sy == 1 else (side - d, side - b)
                images.append((u, w, v, z, rho))
    return images


def encloses(text: str, exact: Fraction) -> bool:
    low, high = (Fraction(float.fromhex(token)) for token in text.split())
    return low <= exact <= high


def n50_inputs(bundle: Path) -> dict[str, Any]:
    """Bind all 200 oblique inputs of an n50 bundle to the exact candidate, independently.

    For each net index the input file must hash to the digest its ``result.json`` records,
    and every interval in it must enclose the exact rational recomputed here: the side, the
    core, ``E = L/2 - rho(a_r)``, the rotation ``c`` and ``s`` at ``t_r``, ``gamma = 1``
    exactly, and every coordinate and density of the D4-expanded rectangles. No source code
    is imported.
    """
    root = bundle / "proof"
    candidate = (root / "candidate.json").read_bytes()
    tree = read_subtree_manifest()
    _require(
        _sha256(candidate) == tree[N50["L740"] / "candidate.json"], "bundle candidate differs"
    )
    side, core, items = _n50_measure(json.loads(candidate))
    images = d4_images(side, items)
    checked = 0
    for index in range(1, N50_LAST + 1):
        folder = root / f"net{index:03}"
        raw = (folder / "input.txt").read_bytes()
        spec = json.loads((folder / "result.json").read_text())["manifest"]
        _require(_sha256(raw) == spec["input_sha256"], f"input {index} is not the recorded one")
        t = index * N50_STEP
        a = max(Fraction(0), t - N50_STEP / 2)
        radius = (1 + 2 * a - a * a) / (2 * (1 + a * a))
        header = (
            side,
            core,
            side / 2 - radius,
            (1 - t * t) / (1 + t * t),
            2 * t / (1 + t * t),
            Fraction(1),
        )
        lines = raw.decode("ascii").splitlines()
        _require(len(lines) == 6 + 1 + len(images) + 1, f"input {index} line count")
        for line, exact in zip(lines[:6], header, strict=True):
            _require(encloses(line, exact), f"input {index} header does not enclose {exact}")
        _require(lines[5].split()[0] == lines[5].split()[1], "gamma is not a point interval")
        _require(Fraction(float.fromhex(lines[5].split()[0])) == 1, "gamma is not one")
        _require(int(lines[6]) == len(images) and int(lines[-1]) == 0, f"input {index} counts")
        for line, image in zip(lines[7:-1], images, strict=True):
            tokens = line.split()
            _require(len(tokens) == 10, f"input {index} rectangle line")
            for k, exact in enumerate(image):
                _require(
                    encloses(" ".join(tokens[2 * k : 2 * k + 2]), exact),
                    f"input {index} interval does not enclose its datum",
                )
        _require(
            spec["E"] == str(side / 2 - radius) and Fraction(spec["t"]) == t,
            f"angle {index} specification differs",
        )
        checked += 1
    return {
        "status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE",
        "inputs": checked,
        "rectangle_images": len(images),
        "gamma": "1",
        "scope": (
            "Each oblique input hashes to its recorded digest and every interval encloses "
            "the exact datum recomputed from the candidate; coverage is not decided here."
        ),
    }


def n50_compare(bundle: Path) -> dict[str, Any]:
    """Compare a complete run of the shipped L740 driver with the retained certificate.

    The run rewrites ``proof/certificate.json`` with ``results`` in completion order, so it
    is compared field by field; ``replay-progress.json`` and ``replay-verify``, which the
    shipped bundle lacks, show that the run happened. Every per-angle ``replayed.json``
    must carry the node count and lower bound of the shipped ``result.json``.
    """
    root = bundle / "proof"
    progress = json.loads((root / "replay-progress.json").read_text())
    _require((root / "replay-verify").is_file(), "no replay binary: the driver did not run")
    fresh = json.loads((root / "certificate.json").read_text())
    shipped = json.loads(_read(N50["L740"] / "certificate.json"))
    differing = sorted(
        key for key in set(fresh) | set(shipped) if fresh.get(key) != shipped.get(key)
    )
    angles_ok = 0
    for index in range(1, N50_LAST + 1):
        folder = root / f"net{index:03}"
        replayed = json.loads((folder / "replayed.json").read_text())
        saved = json.loads((folder / "result.json").read_text())
        if (
            replayed["status"] == "ANGLE_RESULT_REPLAYED"
            and replayed["nodes"] == saved["nodes"]
            and replayed["lower"] == saved["lower"]
        ):
            angles_ok += 1
    axis = json.loads((root / "axis" / "replayed.json").read_text())
    axis_ok = axis == shipped["results"]["0"]
    complete = (
        fresh.get("status") == "ALL_ANGLES_VERIFIED_AND_REPLAYED"
        and progress == {"done": N50_LAST + 1, "total": N50_LAST + 1}
        and not differing
        and angles_ok == N50_LAST
        and axis_ok
    )
    return {
        "status": "FULL_REPLAY_MATCHES_SHIPPED" if complete else "DIFFERS",
        "fresh_status": fresh.get("status"),
        "progress": progress,
        "differing_fields": differing,
        "oblique_angles_matching": angles_ok,
        "axis_matches": axis_ok,
        "certificate_sha256": _sha256((root / "certificate.json").read_bytes()),
    }


def _n50_angle(job: tuple[str, str, str, str]) -> dict[str, Any]:
    """Re-execute one oblique angle with the source's own replay function (worker)."""
    code, folder, binary, candidate = job
    if code not in sys.path:
        sys.path.insert(0, code)
    replay = importlib.import_module("verify_rotated_result").replay
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    report = cast(dict[str, Any], replay(Path(folder), Path(binary), Path(candidate)))
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return report | {
        "wall_seconds": time.monotonic() - start,
        "cpu_seconds": (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime),
    }


def survey_n50_bundle(root: Path, count: int) -> dict[str, Any]:
    """What every recorded angle of a bundle's ``proof/`` says, without re-running any."""
    records = [
        json.loads((root / f"net{index:03}" / "result.json").read_text())
        for index in range(1, count)
    ]
    axis = json.loads((root / "axis" / "result.json").read_text())
    return {
        "oblique_records": len(records),
        "gammas": sorted({record["manifest"]["gamma"] for record in records} | {axis["gamma"]}),
        "statuses": sorted({record["status"] for record in records}),
        "axis_status": axis["status"],
        "frontier_boxes": sum(len(record["frontier"]) for record in records),
        "nodes": sum(record["nodes"] for record in records),
        "least_lower": min(record["lower"] for record in records),
        "upstream_oblique_seconds": sum(record["seconds"] for record in records),
        "upstream_axis_seconds": axis["seconds"],
    }


def n50_replay(bundle: Path, indices: list[int], workers: int) -> dict[str, Any]:
    """Run the preconditions of ``verify_mixed_full_proof.verify`` and a chosen angle set.

    The shipped driver has no subset mode, so this repeats its assertions in order and
    then calls the same per-angle functions: ``verify_axis_certificate.replay`` for index
    0 and ``verify_rotated_result.replay`` for each oblique index, with the source's C++
    compiled by the source's ``compile_verifier``. Nothing of the source is modified.
    """
    root = (bundle / "proof").resolve()
    code = str((bundle / "code").resolve())
    if code not in sys.path:
        sys.path.insert(0, code)
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    rotated = importlib.import_module("mixed_rotated_verify")
    axis_module = importlib.import_module("verify_axis_certificate")
    summary = json.loads((root / "summary.json").read_text())
    data = json.loads((root / "candidate.json").read_text())
    model = density.expand(data)
    net_audit.symmetry(model)
    step, last = net_audit.candidate_net(data)
    count = last + 1
    net = net_audit.net_certificate(model[1], step, last)
    domains = net_audit.centre_domains(model[0], model[1], step, last)
    manifest = json.loads((root / "manifest.json").read_text())
    source_bytes = Path(rotated.SOURCE).read_bytes()
    _require(summary["verified_angles"] == count == summary["complete_angles"], "summary")
    _require(manifest["net"] == net, "manifest net differs")
    _require(set(map(int, summary["records"])) == set(range(count)), "summary records")
    _require(summary["candidate_digest"] == manifest["candidate_digest"] == model[-1], "digest")
    _require((root / "verify.cpp").read_bytes() == source_bytes, "verify.cpp differs")
    _require(_sha256(source_bytes) == manifest["source_sha256"], "checker source digest")
    certificate = json.loads((root / "certificate.json").read_text())
    started = time.monotonic()
    rows: list[dict[str, Any]] = []
    if 0 in indices:
        before = resource.getrusage(resource.RUSAGE_SELF)
        start = time.monotonic()
        axis = axis_module.replay(root / "axis", root / "candidate.json")
        after = resource.getrusage(resource.RUSAGE_SELF)
        _require(axis["digest"] == model[-1] and Fraction(axis["gamma"]) >= 1, "axis replay")
        rows.append(
            {
                "index": 0,
                "status": axis["status"],
                "cells": axis["cells"],
                "integer_minimum": axis["integer_minimum"],
                "upstream": certificate["results"]["0"],
                "matches_upstream": axis == certificate["results"]["0"],
                "wall_seconds": time.monotonic() - start,
                "cpu_seconds": (after.ru_utime - before.ru_utime)
                + (after.ru_stime - before.ru_stime),
            }
        )
    oblique = sorted(index for index in set(indices) if index != 0)
    binary = root / "replay-verify"
    rotated.compile_verifier(binary)
    jobs: list[tuple[str, str, str, str]] = []
    for index in oblique:
        _require(1 <= index < count, f"index outside the net: {index}")
        folder = root / f"net{index:03}"
        saved = json.loads((folder / "result.json").read_text())
        spec = saved["manifest"]
        _require(saved["status"] == "ANGLE_VERIFIED" and saved["frontier"] == [], "status")
        _require(
            spec["candidate_digest"] == model[-1]
            and spec["net_index"] == index
            and spec["domain"] == domains[index]
            and Fraction(spec["gamma"]) >= 1,
            f"angle {index} specification",
        )
        jobs.append((code, str(folder), str(binary), str(root / "candidate.json")))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for index, report in zip(oblique, pool.map(_n50_angle, jobs), strict=True):
            saved = json.loads((root / f"net{index:03}" / "result.json").read_text())
            rows.append(
                {
                    "index": index,
                    "status": report["status"],
                    "nodes": report["nodes"],
                    "lower": report["lower"],
                    "upstream_nodes": saved["nodes"],
                    "upstream_lower": saved["lower"],
                    "upstream_seconds": saved["seconds"],
                    "matches_upstream": report["nodes"] == saved["nodes"]
                    and report["lower"] == saved["lower"],
                    "wall_seconds": report["wall_seconds"],
                    "cpu_seconds": report["cpu_seconds"],
                }
            )
    survey = survey_n50_bundle(root, count)
    upstream_total = survey["upstream_oblique_seconds"]
    sampled_upstream = sum(row.get("upstream_seconds", 0.0) for row in rows)
    sampled_cpu = sum(row["cpu_seconds"] for row in rows if row["index"] != 0)
    ratio = sampled_cpu / sampled_upstream if sampled_upstream else None
    return {
        "status": "SAMPLE_REPLAYED" if all(r["matches_upstream"] for r in rows) else "DIFFERS",
        "candidate_digest": model[-1],
        "indices": sorted(set(indices)),
        "rows": sorted(rows, key=lambda row: row["index"]),
        "wall_seconds": time.monotonic() - started,
        "bundle_records": survey,
        "upstream_oblique_seconds_total": upstream_total,
        "sample_cpu_over_upstream_seconds": ratio,
        "estimated_full_oblique_cpu_hours": (upstream_total * ratio / 3600) if ratio else None,
        "scope": (
            "The source's per-angle replay functions and unchanged C++ checker on the "
            "listed indices, after the full driver's preconditions; not a complete replay."
        ),
    }


# --------------------------------------------------------------------------- the audit


def provenance(source: Path = SOURCE) -> dict[str, Any]:
    """Every retained file against the subtree manifest, through the decompressed bytes."""
    tree = read_subtree_manifest()
    files = retained_files(source)
    _require(
        set(files) <= set(tree), f"retained outside the manifest: {set(files) - set(tree)}"
    )
    for relative, data in files.items():
        _require(_sha256(data) == tree[relative], f"SHA-256 mismatch: {relative}")
        _require(_pinned_only(relative) is None, f"pinned-only file retained: {relative}")
    missing = sorted(
        str(path)
        for path in set(tree) - set(files)
        if _pinned_only(path) is None and path.parts[0] != ".git"
    )
    _require(not missing, f"retained files missing: {missing}")
    record = json.loads(MANIFEST.read_text())["sources"][0]
    _require(
        record["source_commit"] == REVISION and record["git_tree"] == GIT_TREE, "pin differs"
    )
    _require(record["retained_file_count"] == len(files), "retained file count differs")
    return {
        "revision": REVISION,
        "git_tree": GIT_TREE,
        "subtree_files": len(tree),
        "retained_files": len(files),
        "retained_bytes": sum(len(data) for data in files.values()),
        "pinned_only_files": len(tree) - len(files),
    }


def exact_audit(source: Path = SOURCE) -> dict[str, Any]:
    """The whole first-party exact audit; no source code is imported or run."""
    return {
        "kind": "wand125-point-and-mixed-exact-audit/v1",
        "source_revision": REVISION,
        "provenance": provenance(source),
        "n45": n45_cover(
            _read(N45 / "cover.txt", source), _json(N45 / "provenance.json", source)
        ),
        "n21": n21_certificates(source),
        "n50": {name: n50_certificate(name, source) for name in N50},
        "scope": (
            "Exact premises only: digests, formats, nonnegativity, totals and strict "
            "budgets, D4 invariance of the point measures, the n21 threshold algebra, the "
            "n50 net containment and Green comparison. Coverage is decided by the "
            "source checkers, whose replays are recorded separately."
        ),
    }


# --------------------------------------------------------------------------- acquisition


def _git(checkout: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout


def acquire(checkout: Path, retrieved_at: str) -> dict[str, Any]:
    """Pin the claim directories of a checkout at REVISION and retain the evidence subset.

    Only reads the checkout: the revision and tree come from ``rev-parse``, and each file's
    bytes are bound to the commit by comparing its Git blob with ``ls-tree``. A sparse
    checkout is enough; ``LICENSE`` is taken from the rectangle packet when its blob is
    the pinned one.
    """
    _require(
        _git(checkout, "rev-parse", "HEAD").strip() == REVISION, "checkout is not REVISION"
    )
    _require(_git(checkout, "rev-parse", "HEAD^{tree}").strip() == GIT_TREE, "tree differs")
    blobs: dict[Path, str] = {}
    for line in _git(checkout, "ls-tree", "-r", "HEAD").splitlines():
        meta, _, name = line.partition("\t")
        blobs[Path(name)] = meta.split()[2]
    wanted = sorted(
        path
        for path in blobs
        if path in TOP_FILES or any(path.is_relative_to(d) for d in CLAIM_DIRS)
    )
    contents: dict[Path, bytes] = {}
    for path in wanted:
        origin = RECTANGLE_LICENSE if path == Path("LICENSE") else checkout / path
        data = origin.read_bytes()
        _require(git_blob(data) == blobs[path], f"bytes are not the pinned blob: {path}")
        contents[path] = data
    code = sorted(
        p for p in wanted if p.parts[:3] == ("certificates", "mixed_n50_L7318", "code")
    )
    for path in code:
        twin = Path("certificates/mixed_n50_L740/code") / path.name
        _require(contents.get(twin) == contents[path], f"L7318 code differs from L740: {path}")
    atomic_write_text(
        SUBTREE, "".join(f"{_sha256(contents[p])}  ./{p}\n" for p in wanted), encoding="utf-8"
    )
    if SOURCE.exists():
        shutil.rmtree(SOURCE)
    retained = [path for path in wanted if _pinned_only(path) is None]
    compressed: list[str] = []
    for path in retained:
        target = SOURCE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents[path])
        if (
            path.suffix in {".json", ".jsonl", ".txt", ".log"}
            and contents[path].count(b"\n") > LINE_THRESHOLD
        ):
            compressed.append(str(compress(target).relative_to(PACKET)))
    pinned = [
        {
            "path": str(path),
            "bytes": len(contents[path]),
            "sha256": _sha256(contents[path]),
            "reason": _pinned_only(path),
        }
        for path in wanted
        if _pinned_only(path) is not None
        and not path.is_relative_to(N21 / "verifier-source")
        and not path.is_relative_to(N21 / "data")
    ]
    grouped = {
        str(directory): {
            "files": len(members),
            "bytes": sum(len(contents[p]) for p in members),
        }
        for directory in (N21 / "data", N21 / "verifier-source")
        for members in [[p for p in wanted if p.is_relative_to(directory)]]
    }
    entry = {
        "id": "wand125-point-and-mixed",
        "source_url": SOURCE_URL,
        "source_ref": "refs/heads/main",
        "source_commit": REVISION,
        "git_tree": GIT_TREE,
        "archived_path": str(SOURCE.relative_to(REPO)),
        "subtree_manifest": str(SUBTREE.relative_to(REPO)),
        "subtree_scope": [str(path) for path in (*TOP_FILES, *CLAIM_DIRS)],
        "subtree_file_count": len(wanted),
        "subtree_total_bytes": sum(len(data) for data in contents.values()),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum(len(contents[p]) for p in retained),
        "compressed": compressed,
        "pinned_only": pinned,
        "pinned_only_groups": grouped,
        "license": "MIT (wand125); point_n21_L5/UPSTREAM-LICENSE.txt is Evan Daniel's MIT",
        "claims": [
            "s(45) = 7 (point_n45_L7)",
            "s(21) = 5 (point_n21_L5)",
            "s(50) >= 37/5 (certificates/mixed_n50_L740)",
            "s(50) >= 147/20 (certificates/mixed_n50_L735, superseded)",
            "s(50) >= 3659/500 (certificates/mixed_n50_L7318, superseded)",
        ],
    }
    record = {
        "format": "external-source-acquisition-v1",
        "retrieved_at_utc": retrieved_at,
        "git_scope": (
            "A blob-filtered clone of the single public branch, sparse over README.md, "
            "docs/, src/ and the five claim directories; every file under the claim "
            "directories is digested, the rest of the tree is pinned by the commit."
        ),
        "sources": [entry],
    }
    atomic_write_text(MANIFEST, json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return entry


def host_facts() -> dict[str, Any]:
    """CPU, cores and the toolchain versions a replay ran under."""

    def first_line(*command: str) -> str | None:
        try:
            output = subprocess.run(command, capture_output=True, text=True, check=True)
        except OSError, subprocess.CalledProcessError:
            return None
        return output.stdout.splitlines()[0] if output.stdout else None

    cpu = None
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        for line in cpuinfo.read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    return {
        "platform": platform.platform(),
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "python": sys.version,
        "c++": first_line("c++", "--version"),
        "rustc": first_line("rustc", "--version"),
        "cargo": first_line("cargo", "--version"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    exact = commands.add_parser("exact", help="recompute the exact premises")
    exact.add_argument("--out", type=Path, default=EXACT_RECEIPT)
    exact.add_argument("--check", action="store_true", help="compare with --out, write nothing")
    getting = commands.add_parser("acquire", help="retain the subset from a pinned checkout")
    getting.add_argument("checkout", type=Path)
    getting.add_argument("--retrieved-at", default="")
    n45 = commands.add_parser("n45-compare", help="compare a verify.sh run directory")
    n45.add_argument("run_dir", type=Path)
    n45.add_argument("--out", type=Path, required=True)
    n21 = commands.add_parser("n21-compare", help="compare a verify_portable.py output")
    n21.add_argument("out_dir", type=Path)
    n21.add_argument("--out", type=Path, required=True)
    n21.add_argument("--m1-linkage", type=Path, help="the pinned m1-full-linkage.json.gz")
    n21.add_argument("--collect", type=Path, help="also copy the run's records here")
    n21.add_argument(
        "--stage", action="append", help="compare only these finished stage directories"
    )
    n50 = commands.add_parser("n50-replay", help="replay chosen angles of an n50 bundle")
    n50.add_argument("bundle", type=Path)
    n50.add_argument("--index", type=int, action="append", required=True)
    n50.add_argument("--workers", type=int, default=2)
    n50.add_argument("--out", type=Path, required=True)
    hashes = commands.add_parser("n50-bundle-check", help="check files-sha256.json")
    hashes.add_argument("bundle", type=Path)
    hashes.add_argument("--out", type=Path, required=True)
    inputs = commands.add_parser("n50-inputs", help="bind all 200 inputs to the candidate")
    inputs.add_argument("bundle", type=Path)
    inputs.add_argument("--out", type=Path, required=True)
    comparing = commands.add_parser("n50-compare", help="compare a complete L740 run")
    comparing.add_argument("bundle", type=Path)
    comparing.add_argument("--out", type=Path, required=True)
    hosting = commands.add_parser("host", help="print CPU, core and toolchain facts")
    hosting.add_argument("--out", type=Path)
    args = parser.parse_args()
    if args.command == "acquire":
        print(json.dumps(acquire(args.checkout.resolve(), args.retrieved_at), indent=2))
        return 0
    if args.command == "exact":
        text = json.dumps(exact_audit(), indent=2) + "\n"
        if args.check:
            same = args.out.read_text(encoding="utf-8") == text
            print("EXACT_AUDIT_MATCHES_RECEIPT" if same else "EXACT_AUDIT_DIFFERS")
            return 0 if same else 1
        atomic_write_text(args.out, text, encoding="utf-8")
        print(text, end="")
        return 0
    if args.command == "host":
        text = json.dumps(host_facts(), indent=2) + "\n"
        if args.out:
            atomic_write_text(args.out, text, encoding="utf-8")
        print(text, end="")
        return 0
    if args.command == "n45-compare":
        result = n45_compare(args.run_dir, _json(N45 / "provenance.json"))
    elif args.command == "n21-compare":
        if args.stage:
            _require(args.m1_linkage is not None, "--stage needs --m1-linkage")
            result = compare_stage_files(args.out_dir, args.m1_linkage, args.stage)
        elif args.collect:
            result = n21_collect(args.out_dir, args.collect, args.m1_linkage)
        else:
            result = n21_compare(args.out_dir, m1_linkage=args.m1_linkage)
    elif args.command == "n50-bundle-check":
        result = check_bundle_hashes(args.bundle)
    elif args.command == "n50-inputs":
        result = n50_inputs(args.bundle)
    elif args.command == "n50-compare":
        result = n50_compare(args.bundle)
    else:
        if args.workers < 1 or args.workers > 2:
            parser.error("--workers must be 1 or 2 on a shared host")
        result = n50_replay(args.bundle, args.index, args.workers)
    text = json.dumps(result, indent=2, default=str) + "\n"
    atomic_write_text(args.out, text, encoding="utf-8")
    print(text, end="")
    ok = result["status"] in {
        "MATCHES_SOURCE_REFERENCE",
        "MATCHES_SOURCE_M1_RECORD",
        "SAMPLE_REPLAYED",
        "BUNDLE_FILES_MATCH",
        "ALL_INPUTS_ENCLOSE_THE_CANDIDATE",
        "FULL_REPLAY_MATCHES_SHIPPED",
        "STAGE_FILES_COMPARED",
    }
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
