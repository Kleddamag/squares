"""Audit wand125's rectangle-density certificates and replay the reviewed checker.

wand125/square-packing-bounds publishes certificates in Tokoharu's rectangle-density
format, checked by Tokoharu's unchanged ``verify.cpp``. This tool binds them to the
same first-party exact preflight as ``audit_tokoharu_density``: every interval in the
checker input encloses the exact rational datum, the axis-event partition is complete,
the orbit normalization preserves mass, and the total mass is strictly below ``n``.

The packet retains the exact candidates, not the tens of megabytes of derived interval
input. Each input is regenerated here from the candidate and must hash to the SHA-256
the upstream accepting run recorded, so the bytes replayed are the bytes published. The
checker source is the byte-identical copy already retained with Tokoharu's packet.

Each candidate is stored as deterministic gzip (``certified_candidate.json.gz``, listed in
the packet README's Compressed Files table). Every retained read here goes through
`devtools.retained_data.read_retained_bytes`, so the digests checked are those of the
upstream bytes, and a tree restored with ``gunzip -k`` reads the same.

Each retained pin of the source is one `Packet`: a directory under ``resources/web/``,
the revision, and the standing (highest) certificate for each count at that revision.
A packet with a ``base`` retains only the files that are new at its pin. A file its base
already retains byte for byte is read from the base packet, and the provenance check
requires the digest this pin's tree manifest records for it. ``--packet`` chooses the
packet by its date; the default is the first, so the commands its records give still
mean what they said.

Global rotated coverage is still decided by the external C++ checker, so a replay is
V4/C3 machine evidence, exactly as for Tokoharu's own certificates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import audit_tokoharu_density as tokoharu
from devtools.retained_data import (
    GZIP_SUFFIX,
    compress,
    compressed_path,
    read_retained_bytes,
    read_retained_text,
    retained_exists,
)

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
SOURCE_URL = "https://github.com/wand125/square-packing-bounds"
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
#: Top-level upstream files and directories every packet's evidence includes.
RETAINED_TOP = ("LICENSE", "README.md", "requirements.txt", "docs")
DEFAULT_TIMEOUT = 24 * 3600
_CERTIFICATE_NAME = re.compile(r"rect_n(\d+)_L\d+")

# The standing (highest) certificate for each n at ad43d29, and its exact side.
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

# The standing certificate for each n at 39d8ecc. Twelve are unchanged since ad43d29
# (n = 18, 19, 20, 26, 27, 30, 32, 40, 45, 61, 75, 78); the others are raised or new.
CASES_2026_09_28: dict[int, tuple[str, Fraction]] = {
    18: ("rect_n18_L4695", Fraction(939, 200)),
    19: ("rect_n19_L4815", Fraction(963, 200)),
    20: ("rect_n20_L4895", Fraction(979, 200)),
    21: ("rect_n21_L49875", Fraction(399, 80)),
    26: ("rect_n26_L553", Fraction(553, 100)),
    27: ("rect_n27_L56", Fraction(28, 5)),
    28: ("rect_n28_L572", Fraction(143, 25)),
    29: ("rect_n29_L579", Fraction(579, 100)),
    30: ("rect_n30_L5865", Fraction(1173, 200)),
    31: ("rect_n31_L5935", Fraction(1187, 200)),
    32: ("rect_n32_L595", Fraction(119, 20)),
    37: ("rect_n37_L6425", Fraction(257, 40)),
    38: ("rect_n38_L654", Fraction(327, 50)),
    39: ("rect_n39_L663", Fraction(663, 100)),
    40: ("rect_n40_L6695", Fraction(1339, 200)),
    41: ("rect_n41_L6755", Fraction(1351, 200)),
    42: ("rect_n42_L679", Fraction(679, 100)),
    43: ("rect_n43_L6865", Fraction(1373, 200)),
    44: ("rect_n44_L6935", Fraction(1387, 200)),
    45: ("rect_n45_L6955", Fraction(1391, 200)),
    51: ("rect_n51_L74425", Fraction(2977, 400)),
    52: ("rect_n52_L7535", Fraction(1507, 200)),
    53: ("rect_n53_L7595", Fraction(1519, 200)),
    54: ("rect_n54_L76675", Fraction(3067, 400)),
    55: ("rect_n55_L771", Fraction(771, 100)),
    56: ("rect_n56_L777", Fraction(777, 100)),
    57: ("rect_n57_L7835", Fraction(1567, 200)),
    58: ("rect_n58_L789", Fraction(789, 100)),
    59: ("rect_n59_L792", Fraction(198, 25)),
    60: ("rect_n60_L794", Fraction(397, 50)),
    61: ("rect_n61_L796", Fraction(199, 25)),
    66: ("rect_n66_L8375", Fraction(67, 8)),
    67: ("rect_n67_L8455", Fraction(1691, 200)),
    68: ("rect_n68_L8495", Fraction(1699, 200)),
    69: ("rect_n69_L8575", Fraction(343, 40)),
    70: ("rect_n70_L862", Fraction(431, 50)),
    71: ("rect_n71_L8685", Fraction(1737, 200)),
    72: ("rect_n72_L874", Fraction(437, 50)),
    73: ("rect_n73_L878", Fraction(439, 50)),
    74: ("rect_n74_L884", Fraction(221, 25)),
    75: ("rect_n75_L889", Fraction(889, 100)),
    76: ("rect_n76_L892", Fraction(223, 25)),
    77: ("rect_n77_L891", Fraction(891, 100)),
    78: ("rect_n78_L8955", Fraction(1791, 200)),
    86: ("rect_n86_L9355", Fraction(1871, 200)),
    88: ("rect_n88_L945", Fraction(189, 20)),
    89: ("rect_n89_L955", Fraction(191, 20)),
    91: ("rect_n91_L9645", Fraction(1929, 200)),
    94: ("rect_n94_L9795", Fraction(1959, 200)),
    95: ("rect_n95_L98418", Fraction(49209, 5000)),
}


@dataclass(frozen=True, slots=True)
class Packet:
    """One retained pin of the source, and the standing certificates at that pin."""

    date: str
    revision: str
    cases: Mapping[int, tuple[str, Fraction]]
    git_scope: str
    retention_notes: str
    #: The earlier packet whose retained files this one reads instead of copying.
    base: Packet | None = None
    #: The checkout the packet lives in; a scratch root rebuilds a packet elsewhere.
    root: Path = REPO

    @property
    def relative(self) -> Path:
        """The packet directory relative to the repository root, as its records name it."""
        return WEB.relative_to(REPO) / f"wand125-rectangle-certificates-{self.date}"

    @property
    def directory(self) -> Path:
        return self.root / self.relative

    @property
    def source(self) -> Path:
        return self.directory / "wand125-rectangles"

    @property
    def manifest(self) -> Path:
        return self.directory / "acquisition/sources.json"

    @property
    def tree_manifest(self) -> Path:
        return self.directory / "acquisition/upstream-tree.sha256"

    def required(self, tree: Iterable[Path]) -> set[Path]:
        """The pinned files this packet's evidence consists of, here or in its base."""
        names = {name for name, _side in self.cases.values()}
        return {
            path
            for path in tree
            if path.parts[0] in RETAINED_TOP
            or (
                path.parts[0] == "certificates"
                and len(path.parts) == 3
                and path.parts[1] in names
                and path.parts[2] in CASE_FILES
            )
        }

    def locate(self, relative: Path) -> Path | None:
        """The retained copy of an upstream path, in this packet or the nearest base."""
        if retained_exists(self.source / relative):
            return self.source / relative
        return None if self.base is None else self.base.locate(relative)

    def case_directory(self, source: Path, name: str) -> Path:
        """Where the audit reads a standing certificate from ``source``."""
        here = source / "certificates" / name
        if source.resolve() != self.source.resolve() or here.is_dir():
            return here
        found = self.locate(Path("certificates") / name / CASE_FILES[0])
        if found is None:
            raise ValueError(f"no packet retains {name}")
        return found.parent


SEPTEMBER_27 = Packet(
    date="2026-09-27",
    revision="ad43d29d96d0d9740b34643b5ac3fb960909cf9c",
    cases=CASES,
    git_scope=(
        "The single public branch was fetched; the repository has no tags, releases, "
        "submodules or Git LFS attributes."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, LICENSE, requirements and docs, "
        "and for each standing rectangle certificate its exact candidate, metadata, "
        "upstream verification summary and per-angle rows. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the earlier point certificates and src/ "
        "(the point-certificate search and checker code) are pinned by digest only."
    ),
)
SEPTEMBER_28 = Packet(
    date="2026-09-28",
    revision="39d8ecc74d651b54ec977c331c8f2015b442a6c4",
    cases=CASES_2026_09_28,
    git_scope=(
        "The single public branch was fetched; git ls-remote lists only refs/heads/main, "
        "so there are no tags, and the tree has no .gitmodules or .gitattributes. The "
        "GitHub releases page was not reachable from the retrieving session; the "
        "2026-09-27 retrieval found no releases, and none is recorded here."
    ),
    retention_notes=(
        "The whole tracked tree is pinned by per-file SHA-256 in the tree manifest. "
        "Retained bytes are the top-level README, which changed since ad43d29, and for "
        "each standing rectangle certificate new or raised since ad43d29 its exact "
        "candidate, metadata, upstream verification summary and per-angle rows. The "
        "LICENSE, requirements, docs and the twelve standing certificates unchanged "
        "since ad43d29 are byte-identical to files the 2026-09-27 packet retains, and "
        "are read from there against this tree's digests. Interval inputs are "
        "regenerated from the candidates and bound to the recorded input SHA-256; "
        "verify.cpp and run_verify.py are byte-identical to Tokoharu's retained copies. "
        "Lower rungs, matching certificates, the point certificates, the point_n21_L5 "
        "and point_n45_L7 bundles, the mixed_n50 certificates and src/ are pinned by "
        "digest only."
    ),
    base=SEPTEMBER_27,
)
#: Every packet by its date, oldest first.
PACKETS: dict[str, Packet] = {packet.date: packet for packet in (SEPTEMBER_27, SEPTEMBER_28)}
DEFAULT_PACKET = SEPTEMBER_27.date


def monotone_bounds(
    cases: Mapping[int, Fraction], upto: int | None = None
) -> dict[int, tuple[Fraction, int]]:
    """Best side and its source count for every n from the least case to ``upto``.

    ``upto`` defaults to the largest case. Deleting squares from a packing proves
    s(m) <= s(n) for m <= n, and a certificate of total mass below k already refutes k
    squares, so each direct bound carries to every larger count.
    """
    result: dict[int, tuple[Fraction, int]] = {}
    best: tuple[Fraction, int] | None = None
    last = max(cases) if upto is None else max(*cases, upto)
    for n in range(min(cases), last + 1):
        if n in cases and (best is None or cases[n] > best[0]):
            best = (cases[n], n)
        if best is not None:
            result[n] = best
    return result


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _upstream_path(relative: Path, tree: Mapping[Path, str]) -> Path:
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


def _git(checkout: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=checkout, capture_output=True, text=True, check=True
    ).stdout.strip()


def _manifest_entry(packet: Packet) -> dict[str, Any]:
    entries = [
        entry
        for entry in tokoharu.load_json(packet.manifest).get("sources", [])
        if isinstance(entry, dict) and entry.get("id") == "wand125-rectangles"
    ]
    if len(entries) != 1:
        raise ValueError("acquisition manifest must identify exactly one wand125 source")
    return entries[0]


def _referenced(
    packet: Packet, missing: set[Path], tree: Mapping[Path, str]
) -> tuple[int, int]:
    """Check the files a packet reads from its base against this pin's digests."""
    total = 0
    for relative in sorted(missing):
        found = None if packet.base is None else packet.base.locate(relative)
        if found is None:
            raise ValueError(f"missing retained file: {relative}")
        data = read_retained_bytes(found)
        if hashlib.sha256(data).hexdigest() != tree[relative]:
            raise ValueError(f"referenced file differs from the pinned tree: {relative}")
        total += len(data)
    return len(missing), total


def source_provenance(packet: Packet, source: Path) -> dict[str, Any]:
    """Bind the source to a clean pinned checkout or to the retained, digest-checked subset."""
    tree = read_tree_manifest(packet.tree_manifest)
    if (source / ".git").exists():
        if _git(source, "rev-parse", "HEAD") != packet.revision or _git(
            source, "status", "--porcelain"
        ):
            raise ValueError("source checkout is dirty or differs from the pinned revision")
        kind = "clean-git-checkout"
    elif source.resolve() != packet.source.resolve():
        raise ValueError("non-checkout source must be the retained acquisition subset")
    else:
        kind = "verified-retained-subset"
    entry = _manifest_entry(packet)
    if (
        entry.get("source_commit") != packet.revision
        or entry.get("archived_path") != str(packet.source.relative_to(packet.root))
        or entry.get("tree_manifest") != str(packet.tree_manifest.relative_to(packet.root))
        or entry.get("upstream_file_count") != len(tree)
    ):
        raise ValueError("acquisition manifest does not bind the pinned revision and tree")
    # Each file on disk and the pinned path it stands for. A stored ``X.gz`` stands for
    # ``X`` and is decompressed; an upstream file that is itself gzip (the mixed_n50
    # bundles) is pinned, and read, as the bytes it is.
    stored: dict[Path, Path] = {}
    for path in source.rglob("*"):
        if ".git" in path.relative_to(source).parts:
            continue
        if path.is_symlink():
            raise ValueError(f"source contains an unexpected symlink: {path}")
        if path.is_file():
            stored[path.relative_to(source)] = _upstream_path(path.relative_to(source), tree)
    actual = set(stored.values())
    if kind == "clean-git-checkout" and actual != set(tree):
        raise ValueError("checkout file set differs from the pinned tree manifest")
    if not actual <= set(tree):
        raise ValueError(
            f"retained files outside the pinned tree: {sorted(actual - set(tree))}"
        )
    missing = packet.required(tree) - actual
    if missing and (kind == "clean-git-checkout" or packet.base is None):
        raise ValueError(f"missing retained case files: {sorted(map(str, missing))}")
    sizes: dict[Path, int] = {}
    for on_disk, relative in sorted(stored.items()):
        path = source / on_disk
        data = path.read_bytes() if on_disk == relative else read_retained_bytes(path)
        if hashlib.sha256(data).hexdigest() != tree[relative]:
            raise ValueError(f"SHA-256 mismatch against the pinned tree: {relative}")
        sizes[relative] = len(data)
    total_bytes = sum(sizes.values())
    referenced = _referenced(packet, missing, tree)
    if kind == "verified-retained-subset" and (
        len(actual) != entry.get("retained_file_count")
        or total_bytes != entry.get("retained_total_bytes")
    ):
        raise ValueError("retained file count or bytes differ from the acquisition manifest")
    if (
        packet.base is not None
        and kind == "verified-retained-subset"
        and (
            entry.get("referenced_path")
            != str(packet.base.source.relative_to(packet.base.root))
            or referenced
            != (entry.get("referenced_file_count"), entry.get("referenced_total_bytes"))
        )
    ):
        raise ValueError("referenced files differ from the acquisition manifest")
    for name, _ in packet.cases.values():
        for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
            if tree.get(Path("certificates") / name / file) != digest:
                raise ValueError(f"{name}/{file} is not the reviewed Tokoharu checker")
    for file, digest in (("verify.cpp", VERIFY_SHA256), ("run_verify.py", RUNNER_SHA256)):
        if _sha256(CHECKER / file) != digest:
            raise ValueError(f"retained Tokoharu {file} differs from the reviewed checker")
    result: dict[str, Any] = {
        "kind": kind,
        "revision": packet.revision,
        "tree_manifest": str(packet.tree_manifest.relative_to(packet.root)),
        "upstream_files": len(tree),
        "files_verified": len(actual),
        "bytes_verified": total_bytes,
        "checker": str(CHECKER.relative_to(REPO)),
    }
    if packet.base is not None:
        result |= {
            "referenced_path": str(packet.base.source.relative_to(packet.base.root)),
            "files_referenced": referenced[0],
            "bytes_referenced": referenced[1],
        }
    return result


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
    packet: Packet,
    source: Path,
    n: int,
    out: Path,
    *,
    run_replay: bool,
    workers: int,
    timeout: int,
) -> dict[str, Any]:
    name, side = packet.cases[n]
    case = packet.case_directory(source, name)
    # The count the candidate names must be the pinned one (review WSC-1); the mass
    # check against the pinned n is what the bound rests on, and this is identity.
    if tokoharu.load_json(case / "certified_candidate.json").get("n") != n:
        raise ValueError(f"{name} does not declare n = {n}")
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


def standing(checkout: Path) -> dict[int, tuple[str, Fraction]]:
    """The highest rectangle certificate for each count in a checkout, read from the data.

    The count is the directory's; ten early n29 rungs carry no ``n`` of their own, and a
    candidate that does must agree. A tie at the top would leave the standing
    certificate ambiguous, so it is refused.
    """
    found: dict[int, list[tuple[Fraction, str]]] = {}
    for directory in sorted((checkout / "certificates").glob("rect_n*")):
        match = _CERTIFICATE_NAME.fullmatch(directory.name)
        if match is None or not directory.is_dir():
            raise ValueError(f"unexpected rectangle certificate entry: {directory.name}")
        n = int(match[1])
        candidate = tokoharu.load_json(directory / "certified_candidate.json")
        side = candidate.get("L")
        if candidate.get("n", n) != n or not isinstance(side, int | Fraction):
            raise ValueError(f"{directory.name} does not declare n = {n} and an exact side")
        found.setdefault(n, []).append((Fraction(side), directory.name))
    result: dict[int, tuple[str, Fraction]] = {}
    for n, rungs in sorted(found.items()):
        rungs.sort()
        if len(rungs) > 1 and rungs[-1][0] == rungs[-2][0]:
            raise ValueError(f"two certificates share the standing side at n = {n}")
        result[n] = (rungs[-1][1], rungs[-1][0])
    return result


def acquire(packet: Packet, checkout: Path, retrieved_at: str) -> dict[str, Any]:
    """Pin a clean checkout: digest the whole tree, retain the evidence subset."""
    if _git(checkout, "rev-parse", "HEAD") != packet.revision or _git(
        checkout, "status", "--porcelain"
    ):
        raise ValueError("checkout is dirty or differs from the packet's revision")
    if standing(checkout) != dict(packet.cases):
        raise ValueError("the packet's case table is not the checkout's standing set")
    listing = _git(checkout, "ls-files", "-z").split("\0")
    files = sorted(Path(name) for name in listing if name)
    tree = {path: _sha256(checkout / path) for path in files}
    packet.tree_manifest.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(
        packet.tree_manifest, "".join(f"{tree[path]}  ./{path}\n" for path in files)
    )
    required = sorted(packet.required(files))
    referenced = [
        path
        for path in required
        if packet.base is not None
        and (found := packet.base.locate(path)) is not None
        and hashlib.sha256(read_retained_bytes(found)).hexdigest() == tree[path]
    ]
    for name, _side in packet.cases.values():
        shared = {path.parts[2] for path in referenced if path.parts[1:2] == (name,)}
        if shared and shared != set(CASE_FILES):
            raise ValueError(f"{name} is only partly byte-identical to the base packet")
    retained = [path for path in required if path not in referenced]
    if packet.source.exists():
        shutil.rmtree(packet.source)
    for path in retained:
        (packet.source / path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(checkout / path, packet.source / path)
        if path.name in COMPRESSED_CASE_FILES:
            compress(packet.source / path)
    entry: dict[str, Any] = {
        "id": "wand125-rectangles",
        "source_url": SOURCE_URL,
        "source_ref": "refs/heads/main",
        "source_commit": packet.revision,
        "git_tree": _git(checkout, "rev-parse", "HEAD^{tree}"),
        "archived_path": str(packet.source.relative_to(packet.root)),
        "tree_manifest": str(packet.tree_manifest.relative_to(packet.root)),
        "upstream_file_count": len(files),
        "upstream_total_bytes": sum((checkout / path).stat().st_size for path in files),
        "retained_file_count": len(retained),
        "retained_total_bytes": sum((checkout / path).stat().st_size for path in retained),
    }
    if packet.base is not None:
        entry |= {
            "referenced_path": str(packet.base.source.relative_to(packet.base.root)),
            "referenced_file_count": len(referenced),
            "referenced_total_bytes": sum(
                (checkout / path).stat().st_size for path in referenced
            ),
        }
    entry |= {
        "license": "MIT",
        "branches": {"main": packet.revision},
        "tags": [],
        "releases": [],
        "submodules": [],
        "claims": [f"s({n}) >= {side}" for n, (_name, side) in sorted(packet.cases.items())],
        "retention_notes": packet.retention_notes,
    }
    record = {
        "format": "external-source-acquisition-v1",
        "retrieved_at_utc": retrieved_at,
        "git_scope": packet.git_scope,
        "sources": [entry],
    }
    atomic_write_text(packet.manifest, json.dumps(record, indent=2) + "\n")
    return entry


def _load(out: Path) -> dict[str, Any] | None:
    path = out / "audit.json"
    return json.loads(read_retained_text(path)) if retained_exists(path) else None


def _write(out: Path, record: dict[str, Any]) -> None:
    """Write the receipt plain; a stale compressed copy would disagree with it, so it goes.

    A receipt past 1,000 lines is stored as deterministic gzip once the run ends
    (``python -m devtools.retained_data compress --origin receipt PACKET FILE``).
    """
    atomic_write_text(out / "audit.json", json.dumps(record, indent=2, default=str) + "\n")
    compressed_path(out / "audit.json").unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", choices=tuple(PACKETS), default=DEFAULT_PACKET)
    parser.add_argument("--source", type=Path, help="default: the packet's retained subset")
    parser.add_argument(
        "--acquire", type=Path, help="clean pinned checkout to digest and retain"
    )
    parser.add_argument("--retrieved-at", default="")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--n", type=int, action="append")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument(
        "--resume", action="store_true", help="keep PASS cases already in --out"
    )
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()
    packet = PACKETS[args.packet]
    source = packet.source if args.source is None else args.source
    if unknown := sorted(set(args.n or ()) - set(packet.cases)):
        parser.error(f"no standing certificate in the {packet.date} packet at n = {unknown}")
    if args.acquire:
        print(json.dumps(acquire(packet, args.acquire, args.retrieved_at), indent=2))
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
        "source_revision": packet.revision,
        "source": str(source.resolve()),
        "python": sys.version,
        "scope": (
            "Independent exact preconditions and input binding; "
            "optional upstream global interval replay"
        ),
        "cases": [done[n] for n in sorted(done)],
    }
    try:
        record["provenance"] = source_provenance(packet, source)
        record["platform"] = platform.platform()
        if args.replay:
            compiler = subprocess.run(
                ["g++", "--version"], capture_output=True, text=True, check=True
            )
            record["compiler"] = compiler.stdout
        for n in args.n or sorted(packet.cases):
            if n in done:
                continue
            item = audit_case(
                packet,
                source,
                n,
                args.out,
                run_replay=args.replay,
                workers=args.workers,
                timeout=args.timeout,
            )
            record["cases"] = sorted([*record["cases"], item], key=lambda case: case["n"])
            _write(args.out, record)
            print(
                json.dumps({"n": n, "status": item["status"], "replay": "replay" in item}),
                flush=True,
            )
        record["status"] = "PASS"
    except (OSError, TypeError, ValueError, subprocess.SubprocessError) as error:
        record["status"] = "FAIL"
        record["error"] = str(error)
        print(str(error), file=sys.stderr)
    _write(args.out, record)
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
