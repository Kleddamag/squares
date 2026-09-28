"""Audit wand125's rectangle-density certificates and replay the reviewed checker.

wand125/square-packing-bounds publishes certificates in Tokoharu's rectangle-density
format, checked by Tokoharu's unchanged ``verify.cpp``. This tool binds them to the
same first-party exact preflight as ``audit_tokoharu_density``: every interval in the
checker input encloses the exact rational datum, the axis-event partition is complete,
the orbit normalization preserves mass, and the total mass is strictly below ``n``.

The packet retains the exact candidates, not the 35 MB of derived interval input.
Each input is regenerated here from the candidate and must hash to the SHA-256 the
upstream accepting run recorded, so the bytes replayed are the bytes published. The
checker source is the byte-identical copy already retained with Tokoharu's packet.

Each candidate is stored as deterministic gzip (``certified_candidate.json.gz``, listed in
the packet README's Compressed Files table). Every retained read here goes through
`devtools.retained_data.read_retained_bytes`, so the digests checked are those of the
upstream bytes, and a tree restored with ``gunzip -k`` reads the same.

Global rotated coverage is still decided by the external C++ checker, so a replay is
V4/C3 machine evidence, exactly as for Tokoharu's own certificates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import audit_tokoharu_density as tokoharu
from devtools.retained_data import GZIP_SUFFIX, compress, read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/wand125-rectangle-certificates-2026-09-27"
SOURCE = PACKET / "wand125-rectangles"
MANIFEST = PACKET / "acquisition/sources.json"
TREE_MANIFEST = PACKET / "acquisition/upstream-tree.sha256"
REVISION = "ad43d29d96d0d9740b34643b5ac3fb960909cf9c"
CHECKER = tokoharu.SOURCE / "certificates" / tokoharu.CASES[29]
VERIFY_SHA256 = "a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602"
RUNNER_SHA256 = "7bce246763cac8a2bda9aa4cfd9944aa5e14cde9ac965e00686c25f21ae78261"
CASE_FILES = (
    "certified_candidate.json",
    "certificate_metadata.json",
    "verification_summary.json",
    "verified_angles.jsonl",
)
#: Case files retained as deterministic gzip: every standing candidate is over 1,000 lines.
COMPRESSED_CASE_FILES = frozenset({"certified_candidate.json"})
DEFAULT_TIMEOUT = 24 * 3600

# The standing (highest) certificate for each n at REVISION, and its exact side.
CASES: dict[int, tuple[str, Fraction]] = {
    18: ("rect_n18_L4695", Fraction(939, 200)),
    19: ("rect_n19_L4815", Fraction(963, 200)),
    20: ("rect_n20_L4895", Fraction(979, 200)),
    21: ("rect_n21_L4985", Fraction(997, 200)),
    26: ("rect_n26_L553", Fraction(553, 100)),
    27: ("rect_n27_L56", Fraction(28, 5)),
    28: ("rect_n28_L5695", Fraction(1139, 200)),
    29: ("rect_n29_L5785", Fraction(1157, 200)),
    30: ("rect_n30_L5865", Fraction(1173, 200)),
    31: ("rect_n31_L592", Fraction(148, 25)),
    32: ("rect_n32_L595", Fraction(119, 20)),
    37: ("rect_n37_L64", Fraction(32, 5)),
    38: ("rect_n38_L652", Fraction(163, 25)),
    39: ("rect_n39_L662", Fraction(331, 50)),
    40: ("rect_n40_L6695", Fraction(1339, 200)),
    41: ("rect_n41_L6745", Fraction(1349, 200)),
    42: ("rect_n42_L676", Fraction(169, 25)),
    43: ("rect_n43_L6855", Fraction(1371, 200)),
    44: ("rect_n44_L6925", Fraction(277, 40)),
    45: ("rect_n45_L6955", Fraction(1391, 200)),
    51: ("rect_n51_L743", Fraction(743, 100)),
    52: ("rect_n52_L7505", Fraction(1501, 200)),
    53: ("rect_n53_L758", Fraction(379, 50)),
    54: ("rect_n54_L7665", Fraction(1533, 200)),
    55: ("rect_n55_L77", Fraction(77, 10)),
    56: ("rect_n56_L776", Fraction(194, 25)),
    57: ("rect_n57_L78", Fraction(39, 5)),
    58: ("rect_n58_L788", Fraction(197, 25)),
    59: ("rect_n59_L7905", Fraction(1581, 200)),
    60: ("rect_n60_L792", Fraction(198, 25)),
    61: ("rect_n61_L796", Fraction(199, 25)),
    66: ("rect_n66_L8345", Fraction(1669, 200)),
    67: ("rect_n67_L844", Fraction(211, 25)),
    68: ("rect_n68_L846", Fraction(423, 50)),
    69: ("rect_n69_L8545", Fraction(1709, 200)),
    70: ("rect_n70_L861", Fraction(861, 100)),
    71: ("rect_n71_L8645", Fraction(1729, 200)),
    72: ("rect_n72_L8705", Fraction(1741, 200)),
    73: ("rect_n73_L874", Fraction(437, 50)),
    74: ("rect_n74_L8815", Fraction(1763, 200)),
    75: ("rect_n75_L889", Fraction(889, 100)),
    76: ("rect_n76_L89", Fraction(89, 10)),
    77: ("rect_n77_L888", Fraction(222, 25)),
    78: ("rect_n78_L8955", Fraction(1791, 200)),
}


def monotone_bounds(cases: dict[int, Fraction]) -> dict[int, tuple[Fraction, int]]:
    """Best side and its source count for every n from the least case to the largest.

    Deleting squares from a packing proves s(m) <= s(n) for m <= n, and a certificate
    of total mass below k already refutes k squares, so each direct bound carries to
    every larger count.
    """
    result: dict[int, tuple[Fraction, int]] = {}
    best: tuple[Fraction, int] | None = None
    for n in range(min(cases), max(cases) + 1):
        if n in cases and (best is None or cases[n] > best[0]):
            best = (cases[n], n)
        if best is not None:
            result[n] = best
    return result


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _upstream_path(relative: Path, tree: dict[Path, str]) -> Path:
    """The pinned-tree path a retained file stands for: ``X.gz`` stores ``X``."""
    if relative.name.endswith(GZIP_SUFFIX) and relative not in tree:
        stored = relative.with_name(relative.name.removesuffix(GZIP_SUFFIX))
        if stored in tree:
            return stored
    return relative


def read_tree_manifest(path: Path) -> dict[Path, str]:
    """Parse a sorted ``sha256sum``-style list of ``./``-relative paths."""
    expected: dict[Path, str] = {}
    for line in path.read_text().splitlines():
        digest, separator, name = line.partition("  ")
        relative = Path(name)
        if (
            not separator
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
            or not name.startswith("./")
            or relative.is_absolute()
            or ".." in relative.parts
            or relative in expected
        ):
            raise ValueError(f"invalid or duplicate tree checksum entry: {line!r}")
        expected[relative] = digest
    if not expected:
        raise ValueError("empty tree checksum manifest")
    return expected


def source_provenance(source: Path) -> dict[str, Any]:
    """Bind the source to a clean pinned checkout or to the retained, digest-checked subset."""
    tree = read_tree_manifest(TREE_MANIFEST)
    if (source / ".git").exists():
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True, text=True, check=True
        ).stdout.strip()
        changed = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=source,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if revision != REVISION or changed:
            raise ValueError("source checkout is dirty or differs from the pinned revision")
        kind = "clean-git-checkout"
    elif source.resolve() != SOURCE.resolve():
        raise ValueError("non-checkout source must be the retained acquisition subset")
    else:
        kind = "verified-retained-subset"
    entries = [
        entry
        for entry in tokoharu.load_json(MANIFEST).get("sources", [])
        if isinstance(entry, dict) and entry.get("id") == "wand125-rectangles"
    ]
    if len(entries) != 1:
        raise ValueError("acquisition manifest must identify exactly one wand125 source")
    entry = entries[0]
    if (
        entry.get("source_commit") != REVISION
        or entry.get("archived_path") != str(SOURCE.relative_to(REPO))
        or entry.get("tree_manifest") != str(TREE_MANIFEST.relative_to(REPO))
        or entry.get("upstream_file_count") != len(tree)
    ):
        raise ValueError("acquisition manifest does not bind the pinned revision and tree")
    actual: set[Path] = set()
    for path in source.rglob("*"):
        if ".git" in path.relative_to(source).parts:
            continue
        if path.is_symlink():
            raise ValueError(f"source contains an unexpected symlink: {path}")
        if path.is_file():
            actual.add(_upstream_path(path.relative_to(source), tree))
    if kind == "clean-git-checkout" and actual != set(tree):
        raise ValueError("checkout file set differs from the pinned tree manifest")
    if not actual <= set(tree):
        raise ValueError(
            f"retained files outside the pinned tree: {sorted(actual - set(tree))}"
        )
    required = {
        Path("certificates") / name / file for name, _ in CASES.values() for file in CASE_FILES
    }
    if not required <= actual:
        raise ValueError(f"missing retained case files: {sorted(map(str, required - actual))}")
    total_bytes = 0
    for relative in sorted(actual):
        data = read_retained_bytes(source / relative)
        if hashlib.sha256(data).hexdigest() != tree[relative]:
            raise ValueError(f"SHA-256 mismatch against the pinned tree: {relative}")
        total_bytes += len(data)
    if kind == "verified-retained-subset" and (
        len(actual) != entry.get("retained_file_count")
        or total_bytes != entry.get("retained_total_bytes")
    ):
        raise ValueError("retained file count or bytes differ from the acquisition manifest")
    for name, _ in CASES.values():
        for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
            if tree.get(Path("certificates") / name / file) != digest:
                raise ValueError(f"{name}/{file} is not the reviewed Tokoharu checker")
    for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
        if _sha256(CHECKER / file) != digest:
            raise ValueError(f"retained Tokoharu {file} differs from the reviewed checker")
    return {
        "kind": kind,
        "revision": REVISION,
        "tree_manifest": str(TREE_MANIFEST.relative_to(REPO)),
        "upstream_files": len(tree),
        "files_verified": len(actual),
        "bytes_verified": total_bytes,
        "checker": str(CHECKER.relative_to(REPO)),
    }


def input_text(candidate: dict[str, Any]) -> str:
    """Regenerate the checker's interval input from the exact candidate."""
    side, shrink, _total, rectangles = tokoharu.density(candidate)
    centers = {side / 2, side - shrink / 2}
    for a, _b, d, _e, _rho in rectangles:
        for edge in (a, d):
            for center in (edge - shrink / 2, edge + shrink / 2):
                if side / 2 <= center <= side - shrink / 2:
                    centers.add(center)
    lines = [tokoharu.enclose(side), tokoharu.enclose(shrink), str(len(rectangles))]
    lines.extend(" ".join(tokoharu.enclose(value) for value in rect) for rect in rectangles)
    lines.append(str(len(centers)))
    lines.extend(tokoharu.enclose(center) for center in sorted(centers))
    return "\n".join(lines) + "\n"


def materialize(case: Path, scratch: Path) -> dict[str, Any]:
    """Write a replayable case directory whose input matches the published digest."""
    metadata = tokoharu.load_json(case / "certificate_metadata.json")
    summary = tokoharu.load_json(case / "verification_summary.json")
    text = input_text(tokoharu.load_json(case / "certified_candidate.json"))
    digest = hashlib.sha256(text.encode()).hexdigest()
    if digest != metadata.get("input_sha256") or digest != summary.get("input_sha256"):
        raise ValueError(f"regenerated input does not match the published SHA-256: {case.name}")
    if (case / "certificate_input.txt").exists() and _sha256(
        case / "certificate_input.txt"
    ) != digest:
        raise ValueError(f"published input differs from its own recorded SHA-256: {case.name}")
    if (
        summary.get("verifier_source_sha256") != VERIFY_SHA256
        or summary.get("status") != "VERIFIED"
    ):
        raise ValueError(f"upstream accepting run is not the reviewed checker: {case.name}")
    scratch.mkdir(parents=True)
    atomic_write_text(scratch / "certificate_input.txt", text)
    for name in ("certified_candidate.json", "certificate_metadata.json"):
        (scratch / name).write_bytes(read_retained_bytes(case / name))
    for name in ("verify.cpp", "run_verify.py"):
        shutil.copyfile(CHECKER / name, scratch / name)
    return {
        "input_sha256": digest,
        "input_bytes": len(text.encode()),
        "upstream_nodes": summary.get("nodes"),
        "upstream_wall_seconds": summary.get("wall_seconds"),
    }


def audit_case(
    source: Path, n: int, out: Path, *, run_replay: bool, workers: int, timeout: int
) -> dict[str, Any]:
    name, side = CASES[n]
    case = source / "certificates" / name
    with tempfile.TemporaryDirectory(prefix="wand125-rect-") as directory:
        scratch = Path(directory) / name
        binding = materialize(case, scratch)
        item = tokoharu.preflight(scratch, n, side)
        item |= {"certificate": name, **binding}
        if run_replay:
            if (out / name).exists():
                # Only accepted cases are kept on --resume; this is an interrupted run.
                shutil.rmtree(out / name)
            item["replay"] = tokoharu.replay(scratch, out / name, workers, timeout)
    return item


RETAINED_TOP = ("LICENSE", "README.md", "requirements.txt", "docs")


def acquire(checkout: Path, retrieved_at: str) -> dict[str, Any]:
    """Pin a clean checkout: digest the whole tree, retain the evidence subset."""
    listing = subprocess.run(
        ["git", "ls-files", "-z"], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout.split("\0")
    files = sorted(Path(name) for name in listing if name)
    git_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=checkout,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    tree_lines = [f"{_sha256(checkout / path)}  ./{path}" for path in files]
    atomic_write_text(TREE_MANIFEST, "\n".join(tree_lines) + "\n")
    retained = [
        path
        for path in files
        if path.parts[0] in RETAINED_TOP
        or (
            path.parts[0] == "certificates"
            and len(path.parts) == 3
            and path.parts[1] in {name for name, _ in CASES.values()}
            and path.parts[2] in CASE_FILES
        )
    ]
    if SOURCE.exists():
        shutil.rmtree(SOURCE)
    for path in retained:
        (SOURCE / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(checkout / path, SOURCE / path)
        if path.name in COMPRESSED_CASE_FILES:
            compress(SOURCE / path)
    claims = [f"s({n}) >= {side}" for n, (_name, side) in sorted(CASES.items())]
    entry = {
        "id": "wand125-rectangles",
        "source_url": "https://github.com/wand125/square-packing-bounds",
        "source_ref": "refs/heads/main",
        "source_commit": REVISION,
        "git_tree": git_tree,
        "archived_path": str(SOURCE.relative_to(REPO)),
        "tree_manifest": str(TREE_MANIFEST.relative_to(REPO)),
        "upstream_file_count": len(files),
        "upstream_total_bytes": sum((checkout / path).stat().st_size for path in files),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum((checkout / path).stat().st_size for path in retained),
        "license": "MIT",
        "branches": {"main": REVISION},
        "tags": [],
        "releases": [],
        "submodules": [],
        "claims": claims,
        "retention_notes": (
            "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
            "Retained bytes are the top-level README, LICENSE, requirements and docs, "
            "and for each standing rectangle certificate its exact candidate, metadata, "
            "upstream verification summary and per-angle rows. Interval inputs are "
            "regenerated from the candidates and bound to the recorded input SHA-256; "
            "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
            "Lower rungs, matching certificates, the earlier point certificates and src/ "
            "(the point-certificate search and checker code) are pinned by digest only."
        ),
    }
    record = {
        "format": "external-source-acquisition-v1",
        "retrieved_at_utc": retrieved_at,
        "git_scope": (
            "The single public branch was fetched; the repository has no tags, releases, "
            "submodules or Git LFS attributes."
        ),
        "sources": [entry],
    }
    atomic_write_text(MANIFEST, json.dumps(record, indent=2) + "\n")
    return entry


def _load(out: Path) -> dict[str, Any] | None:
    path = out / "audit.json"
    return json.loads(path.read_text()) if path.exists() else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument(
        "--acquire", type=Path, help="clean pinned checkout to digest and retain"
    )
    parser.add_argument("--retrieved-at", default="")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--n", type=int, choices=tuple(CASES), action="append")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument(
        "--resume", action="store_true", help="keep PASS cases already in --out"
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    if args.acquire:
        TREE_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        print(json.dumps(acquire(args.acquire, args.retrieved_at), indent=2))
        return 0
    if args.out is None:
        parser.error("--out is required unless --acquire is given")
    args.out.mkdir(parents=True, exist_ok=True)
    previous = _load(args.out) if args.resume else None
    done = {
        case["n"]: case
        for case in (previous or {}).get("cases", [])
        if case.get("status") == "PASS" and (case.get("replay") or not args.replay)
    }
    record: dict[str, Any] = {
        "kind": "wand125-rectangle-audit/v1",
        "source_revision": REVISION,
        "source": str(args.source.resolve()),
        "python": sys.version,
        "scope": (
            "Independent exact preconditions and input binding; "
            "optional upstream global interval replay"
        ),
        "cases": [done[n] for n in sorted(done)],
    }
    try:
        record["provenance"] = source_provenance(args.source)
        record["platform"] = platform.platform()
        if args.replay:
            compiler = subprocess.run(
                ["g++", "--version"], capture_output=True, text=True, check=True
            )
            record["compiler"] = compiler.stdout
        for n in args.n or sorted(CASES):
            if n in done:
                continue
            item = audit_case(
                args.source,
                n,
                args.out,
                run_replay=args.replay,
                workers=args.workers,
                timeout=args.timeout,
            )
            record["cases"] = sorted([*record["cases"], item], key=lambda case: case["n"])
            atomic_write_text(
                args.out / "audit.json", json.dumps(record, indent=2, default=str) + "\n"
            )
            print(
                json.dumps({"n": n, "status": item["status"], "replay": "replay" in item}),
                flush=True,
            )
        record["status"] = "PASS"
    except (OSError, TypeError, ValueError, subprocess.SubprocessError) as error:
        record["status"] = "FAIL"
        record["error"] = str(error)
        print(str(error), file=sys.stderr)
    atomic_write_text(args.out / "audit.json", json.dumps(record, indent=2, default=str) + "\n")
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
