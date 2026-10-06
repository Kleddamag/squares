"""Audit wand125's mixed certificates on a declared net, and replay and compare them.

wand125/square-packing-bounds declares its own half-angle net in three certificates
(jlevy/squares#366), each a rectangle density whose candidate carries a ``proof_net``
(`CERTIFICATES`):

- at ``43050ed``, ``mixed_n18_L470`` for ``s(18) >= 47/10``, core side ``999/1000`` and
  ``{"step": "1/1001", "last": 415}``, 416 nodes;
- at ``65e408c``, ``mixed_n18_L4704`` for ``s(18) >= 588/125``, core side ``1999/2000``
  and ``{"step": "1/2006", "last": 831}``, 832 nodes;
- at ``65e408c``, ``mixed_n19_L48229`` for ``s(19) >= 48229/10000``, on
  ``mixed_n18_L470``'s net.

`devtools.audit_wand125_point_and_mixed` takes the standard net (step ``83/40000``, 201
nodes) and core ``9977/10000`` as fixed, so it cannot audit these. This tool is the
first-party part of their import. It was written from the certificate format, the
bundles' data files and lemma N0 of ``sqverify_fast/SOUNDNESS.md``; ``audit``, ``bundle``
and ``compare`` import no source code and open no file of a ``code/`` folder, which they
compare only by digest. ``sample``, ``replay`` and ``control`` run the source's own
checker, from a bundle that ``bundle`` has first bound to the packet. Every command
takes ``--certificate``, ``n18-L470`` unless given.

- ``audit`` recomputes, from the packet's retained files alone, every premise that is
  plain arithmetic: the count, side and core the manifest states; nonnegative masses on
  nondegenerate rectangles inside the container, totalling exactly ``n - 1/100000``;
  lemma N0's five premises on the declared net; the net blocks of ``manifest.json`` and
  ``certificate.json`` equal to the facts recomputed here; one candidate digest
  throughout; and a replay record at threshold one at every node of the declared net.
  It decides no coverage.
- ``bundle`` checks an unpacked proof bundle against the packet:
  - every file its ``files-sha256.json`` lists has that digest, and nothing is
    unlisted;
  - the candidate, certificate and manifest are the retained files, every ``code/``
    file is the retained ``mixed_n50_L740`` copy or, where the certificate's directory
    retains its own (``mixed_n18_L4704``'s driver, whose one change raises the cap on
    its workers from 3 to 16), that copy, and ``proof/verify.cpp`` is the checker
    ``89b674a6...``;
  - at every oblique node, the shipped record's net index, tangent, bin floor and
    per-bin centre domain are lemma N0's exactly, and its input's first lines enclose
    the side, core, domain half-width, cosine and sine exactly, with threshold one; its
    rectangle lines enclose the eight images of every row of the candidate, with their
    densities, and list no point mass;
  - the axis record is at threshold one, with no unresolved cell.

  This binds the source's own runs to the declared net. It decides no coverage either.
- ``compare`` reads a copy of the bundle after the bundle's own driver has replayed it,
  as its README says, with the run's own record. It requires the run to have happened
  (exit zero, the driver's progress at every node, its binary in the copy, every record
  written after the start), and every regenerated record, and the rewritten certificate
  as a mapping, to equal the shipped and retained ones (finding DN-1 of the 5 October
  review, which found the first version matching a copy where nothing ran).
- ``sample`` unpacks the pinned tarball afresh, binds it, and replays a chosen set of
  net nodes with the source's per-node functions and its unchanged C++ checker, after
  the full driver's preconditions (`audit_wand125_point_and_mixed.n50_replay`): the CPU
  each node took against the bundle's own record of it, and the price of the rest. It
  decides only the nodes it ran.
- ``replay`` unpacks the pinned tarball twice, binds the first copy (``bundle``), runs
  the bundle's own driver in the second as its README says, recording the run's start,
  exit, end and the CPU of the driver and everything it waited for, and then compares
  the two (``compare``).
- ``control`` runs the source's checker on the original and two mutants at one oblique
  node, every mass scaled by 99/100 and every mass scaled so that an exact witness
  centre captures ``1 - 10^-6``, and runs the source's own net check on three corrupted
  net declarations. The original must return its shipped record and every other
  variant must be refused.

From ``packing/``::

    .venv/bin/python3 -m devtools.audit_wand125_declared_net audit --check
    .venv/bin/python3 -m devtools.audit_wand125_declared_net bundle --bundle DIR
    .venv/bin/python3 -m devtools.audit_wand125_declared_net compare \\
        --shipped DIR --fresh RUN_DIR --meta RUN_META
    .venv/bin/python3 -m devtools.audit_wand125_declared_net sample \\
        --certificate n19-L48229 --tarball TARBALL --work W --nodes 1,37,415 --workers 2
    .venv/bin/python3 -m devtools.audit_wand125_declared_net replay \\
        --certificate n19-L48229 --tarball TARBALL --work W --workers 2
    .venv/bin/python3 -m devtools.audit_wand125_declared_net control \\
        --certificate n19-L48229 --tarball TARBALL --work W
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.retained_data import read_retained_bytes
from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
N50 = WEB / "wand125-point-and-mixed-2026-09-28/square-packing-bounds/certificates"
N50_DIRECTORY = N50 / "mixed_n50_L740"
#: The source's checker, ``code/mixed_rotated_verify.cpp``, by SHA-256: every mixed
#: certificate of the source so far runs this one.
CHECKER_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
#: The budget gap every mixed certificate leaves below ``n``.
GAP = Fraction(1, 100000)


@dataclass(frozen=True, slots=True)
class Certificate:
    """One certificate directory of the source on a declared net, as the source states it.

    ``n`` and ``side`` are the claim the directory's README states. ``own_code`` names
    the ``code/`` files that are not byte-identical to the retained ``mixed_n50_L740``
    copies and that the packet retains in the certificate's own directory instead. The
    tarball's digest and size are read from the packet's acquisition record, so the pin
    has one home.
    """

    key: str
    packet: Path
    name: str
    n: int
    side: Fraction
    tarball: str
    own_code: frozenset[str] = frozenset()

    @property
    def directory(self) -> Path:
        return self.packet / "square-packing-bounds/certificates" / self.name

    @property
    def receipts(self) -> Path:
        return self.packet / "receipts" / self.key

    @property
    def bundle_name(self) -> str:
        """The one top-level directory of the tarball."""
        return self.tarball.removesuffix(".tar.gz")

    def code_reference(self, name: str) -> Path:
        """The retained file a bundle's ``code/<name>`` must equal."""
        return (self.directory if name in self.own_code else N50_DIRECTORY) / "code" / name

    def tarball_pin(self) -> tuple[str, int]:
        """The tarball's SHA-256 and size, from the packet's acquisition record."""
        record = json.loads((self.packet / "acquisition/sources.json").read_text())
        path = f"certificates/{self.name}/{self.tarball}"
        for source in record["sources"]:
            for item in source["pinned_only"]:
                if item["path"] == path:
                    return item["sha256"], int(item["bytes"])
        raise AuditError(f"the packet pins no {path}")


FINER_NET_05 = WEB / "wand125-mixed-bounds-finer-net-2026-10-05"
FINER_NET_06 = WEB / "wand125-mixed-bounds-finer-net-2026-10-06"
#: Every certificate of the source on a declared net, by the key a command takes.
CERTIFICATES = {
    certificate.key: certificate
    for certificate in (
        Certificate(
            "n18-L470",
            FINER_NET_05,
            "mixed_n18_L470",
            18,
            Fraction(47, 10),
            "n18-L4.7-proof-bundle.tar.gz",
        ),
        Certificate(
            "n18-L4704",
            FINER_NET_06,
            "mixed_n18_L4704",
            18,
            Fraction(588, 125),
            "n18-L4.704-proof-bundle.tar.gz",
            frozenset({"verify_mixed_full_proof.py"}),
        ),
        Certificate(
            "n19-L48229",
            FINER_NET_06,
            "mixed_n19_L48229",
            19,
            Fraction(48229, 10000),
            "n19-L4.8229-proof-bundle.tar.gz",
        ),
    )
}
#: The certificate a command reads when none is given: the first, T-096's.
DEFAULT = "n18-L470"
PACKET = CERTIFICATES[DEFAULT].packet
DIRECTORY = CERTIFICATES[DEFAULT].directory
RECEIPTS = CERTIFICATES[DEFAULT].receipts
N = CERTIFICATES[DEFAULT].n
SIDE = CERTIFICATES[DEFAULT].side


class AuditError(Exception):
    """A premise or a binding that does not hold."""


def require(condition: bool, message: str, /) -> None:  # noqa: FBT001
    """Raise `AuditError` with ``message`` unless ``condition`` holds."""
    if not condition:
        raise AuditError(message)


def load_json(data: bytes) -> Any:
    """JSON with every decimal kept as its text, so that it reads as an exact rational."""
    return json.loads(data, parse_float=str)


def rho(a: Fraction) -> Fraction:
    """Half the width ``(cos phi + sin phi) / 2`` of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def net_facts(core: Fraction, step: Fraction, count: int) -> dict[str, Fraction]:
    """The containment facts of a declared net (lemma N0), exactly."""
    last = step * (count - 1)
    shrink = core * (1 + step)
    return {
        "step": step,
        "count": Fraction(count),
        "endpoint": last,
        "endpoint_check": last * last + 2 * last - 1,
        "rotated_side_upper": shrink,
        "side_margin": 1 - shrink,
        "per_edge_margin": (1 - shrink) / 2,
        "tangent_form": core * (1 + step / (1 - step * step / 4)),
    }


def premises(facts: dict[str, Fraction], count: int) -> dict[str, bool]:
    """Lemma N0's premises (a) to (e) on the declared net."""
    return {
        "a_positive_step_and_count": facts["step"] > 0 and 2 <= count <= 1 << 16,
        "b_core_fits": facts["rotated_side_upper"] < 1,
        "c_reaches_past_pi_over_4": facts["endpoint_check"] > 0,
        "d_last_tangent_at_most_half": facts["endpoint"] <= Fraction(1, 2),
        "e_tangent_form": facts["tangent_form"] < 1,
    }


def read_directory(directory: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """The retained candidate, certificate and manifest."""
    return (
        load_json(read_retained_bytes(directory / "candidate.json")),
        load_json(read_retained_bytes(directory / "certificate.json")),
        load_json(read_retained_bytes(directory / "manifest.json")),
    )


def audit(directory: Path | None = None, *, key: str = DEFAULT) -> dict[str, Any]:
    """Every exact premise of the certificate, from the retained files alone."""
    stated = CERTIFICATES[key]
    candidate, certificate, manifest = read_directory(directory or stated.directory)
    n = candidate["n"]
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    require((n, side) == (stated.n, stated.side), f"the candidate is n = {n}, L = {side}")
    require(candidate["points"] == [], "the candidate has point masses")
    require(candidate["scaling_factor"] == "1", "the candidate is scaled")
    total = Fraction(0)
    positive = 0
    for index, row in enumerate(candidate["rectangles"]):
        x1, y1, x2, y2 = (Fraction(value) for value in row["rectangle"])
        mass = Fraction(row["mass"])
        require(mass >= 0, f"row {index} has a negative mass")
        if mass > 0:
            positive += 1
            require(
                0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side,
                f"row {index} is degenerate or outside [0, L]^2",
            )
        total += mass
    require(total == Fraction(candidate["total_mass"]), "total_mass is not the sum")
    require(total == n - GAP, f"the mass {total} is not n - 1/100000")
    net = candidate["proof_net"]
    require(set(net) == {"step", "last"}, f"proof_net has fields {sorted(net)}")
    require(isinstance(net["last"], int), "proof_net.last is not an integer")
    step, count = Fraction(net["step"]), int(net["last"]) + 1
    facts = net_facts(core, step, count)
    checks = premises(facts, count)
    require(all(checks.values()), f"a premise of lemma N0 fails: {checks}")
    for name, block in (("manifest", manifest["net"]), ("certificate", certificate["net"])):
        for field in (
            "step",
            "count",
            "endpoint",
            "endpoint_check",
            "rotated_side_upper",
            "side_margin",
            "per_edge_margin",
        ):
            require(
                Fraction(str(block[field])) == facts[field],
                f"{name} net {field} is {block[field]}",
            )
    digest = candidate["scaling_source_digest"]
    require(
        manifest["candidate_digest"] == certificate["candidate_digest"] == digest,
        "the candidate digest differs between files",
    )
    require(
        (manifest["n"], Fraction(manifest["L"]), Fraction(manifest["B"])) == (n, side, core),
        "the manifest states another count, side or core",
    )
    require(Fraction(manifest["budget"]) == total, "the manifest's budget is not the mass")
    require(manifest["source_sha256"] == CHECKER_SHA256, "the manifest names another checker")
    require(certificate["status"] == "ALL_ANGLES_VERIFIED_AND_REPLAYED", "not all verified")
    require(
        (certificate["n"], Fraction(certificate["L"]), Fraction(certificate["B"]))
        == (n, side, core)
        and Fraction(certificate["total_mass"]) == total
        and Fraction(certificate["budget_gap"]) == GAP
        and certificate["point_mass"] == "0"
        and certificate["angle_count"] == count,
        "the certificate states another measure or net",
    )
    results = certificate["results"]
    require(set(results) == {str(r) for r in range(count)}, "a net node has no record")
    axis = results["0"]
    require(
        axis["status"] == "AXIS_CERTIFICATE_REPLAYED"
        and axis["gamma"] == "1"
        and axis["digest"] == digest,
        "the axis record is not a replay at threshold one",
    )
    least: tuple[float, int] | None = None
    nodes = 0
    for r in range(1, count):
        record = results[str(r)]
        require(
            record["status"] == "ANGLE_RESULT_REPLAYED"
            and record["index"] == r
            and record["candidate_digest"] == digest,
            f"node {r} has no replay record of this candidate",
        )
        lower = float(record["lower"])
        require(lower >= 1, f"node {r} records a lower bound below one")
        nodes += int(record["nodes"])
        if least is None or lower < least[0]:
            least = (lower, r)
    assert least is not None
    return {
        "kind": "wand125-declared-net-audit/v1",
        "certificate": stated.name,
        "claim": f"s({n}) >= {side.numerator}/{side.denominator}",
        "rectangles": len(candidate["rectangles"]),
        "positive_rectangles": positive,
        "mass": str(total),
        "core": str(core),
        "net": {key: str(value) for key, value in facts.items()},
        "premises": checks,
        "candidate_digest": digest,
        "checker_sha256": CHECKER_SHA256,
        "oblique_records": count - 1,
        "oblique_nodes": nodes,
        "least_oblique_lower": {"lower": least[0], "index": least[1]},
        "axis": {"cells": axis["cells"], "integer_minimum": axis["integer_minimum"]},
        "status": "EXACT_PREMISES_HOLD",
        "scope": (
            "Exact premises only, from the retained files: the measure, lemma N0's premises"
            " on the declared net, the net blocks the manifest and certificate state, one"
            " candidate digest, and a replay record at threshold one at every node. No"
            " coverage is decided here."
        ),
    }


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def enclosure(line: str) -> tuple[Fraction, Fraction]:
    """An input line's two hexadecimal binary64 ends, as exact rationals."""
    low, high = line.split()
    return Fraction(float.fromhex(low)), Fraction(float.fromhex(high))


def orbit(side: Fraction, row: list[Fraction]) -> list[tuple[Fraction, ...]]:
    """The eight images of ``[x1, y1, x2, y2]`` under the container's symmetries."""
    x1, y1, x2, y2 = row
    return [
        (left, bottom, right, top)
        for a1, b1, a2, b2 in ((x1, y1, x2, y2), (y1, x1, y2, x2))
        for left, right in ((a1, a2), (side - a2, side - a1))
        for bottom, top in ((b1, b2), (side - b2, side - b1))
    ]


def rectangle_block(candidate: dict[str, Any], lines: list[str]) -> None:
    """An input's rectangle lines enclose the expanded candidate, row by row.

    After the header, an input lists eight lines per candidate row, each the enclosures
    of an image's ``x1, y1, x2, y2`` and density, then the count of point masses. Each
    row's eight lines must enclose its eight images, matched as a multiset, with
    density ``mass / 8 / area``; no point mass is listed.
    """
    side = Fraction(candidate["L"])
    rows = candidate["rectangles"]
    require(len(lines) == 8 * len(rows) + 1 and lines[-1].strip() == "0", "the point count")
    for index, row in enumerate(rows):
        corners = [Fraction(value) for value in row["rectangle"]]
        area = (corners[2] - corners[0]) * (corners[3] - corners[1])
        density = Fraction(row["mass"]) / 8 / area
        expected = [(*image, density) for image in orbit(side, corners)]
        for line in lines[8 * index : 8 * index + 8]:
            tokens = line.split()
            require(
                len(tokens) == 10, f"row {index}: a rectangle line has {len(tokens)} fields"
            )
            bounds = [
                (Fraction(float.fromhex(tokens[k])), Fraction(float.fromhex(tokens[k + 1])))
                for k in range(0, 10, 2)
            ]
            match = next(
                (
                    image
                    for image in expected
                    if all(
                        low <= exact <= high
                        for (low, high), exact in zip(bounds, image, strict=True)
                    )
                ),
                None,
            )
            if match is None:
                raise AuditError(f"row {index}: a line encloses none of its images")
            expected.remove(match)


def bundle(root: Path, directory: Path | None = None, *, key: str = DEFAULT) -> dict[str, Any]:
    """Bind an unpacked proof bundle to the packet and its records to the declared net."""
    stated = CERTIFICATES[key]
    directory = directory or stated.directory
    listed: dict[str, str] = json.loads((root / "files-sha256.json").read_text())
    present = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "files-sha256.json"
    }
    require(present == set(listed), f"unlisted or missing: {sorted(present ^ set(listed))[:5]}")
    for name, digest in listed.items():
        require(sha256((root / name).read_bytes()) == digest, f"{name} differs from its list")
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        require(
            (root / "proof" / name).read_bytes() == read_retained_bytes(directory / name),
            f"proof/{name} is not the retained file",
        )
    code = sorted(path.name for path in (root / "code").iterdir())
    require(
        code == sorted(path.name for path in N50_DIRECTORY.joinpath("code").iterdir()), "code/"
    )
    for name in code:
        reference = stated.code_reference(name)
        require(
            sha256((root / "code" / name).read_bytes())
            == sha256(read_retained_bytes(reference)),
            f"code/{name} is not the retained copy {reference.relative_to(WEB)}",
        )
    require(
        sha256((root / "requirements.txt").read_bytes())
        == sha256((N50_DIRECTORY / "requirements.txt").read_bytes()),
        "requirements.txt is not the retained copy",
    )
    require(sha256((root / "proof/verify.cpp").read_bytes()) == CHECKER_SHA256, "verify.cpp")
    candidate, certificate, _manifest = read_directory(directory)
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    step = Fraction(candidate["proof_net"]["step"])
    count = int(candidate["proof_net"]["last"]) + 1
    digest = candidate["scaling_source_digest"]
    images = 8 * len(candidate["rectangles"])
    block: list[str] | None = None
    seconds = 0.0
    nodes = 0
    for r in range(1, count):
        folder = root / "proof" / f"net{r:03d}"
        result = json.loads((folder / "result.json").read_text())
        manifest = result["manifest"]
        domain = manifest["domain"]
        t = step * r
        floor = max(Fraction(0), t - step / 2)
        low = rho(floor)
        half_width = side / 2 - low
        require(
            result["status"] == "ANGLE_VERIFIED"
            and result["frontier"] == []
            and result["exact_witnesses"] == []
            and float(result["lower"]) >= 1,
            f"node {r}: the shipped run did not verify it",
        )
        require(
            manifest["candidate_digest"] == digest
            and manifest["net_index"] == r
            and Fraction(manifest["t"]) == t
            and manifest["gamma"] == "1"
            and manifest["source_sha256"] == CHECKER_SHA256,
            f"node {r}: the record is not this candidate's at t = {t}",
        )
        require(
            domain["index"] == r
            and Fraction(domain["t"]) == t
            and Fraction(domain["original_t_lower"]) == floor
            and Fraction(domain["centre_low"]) == low
            and Fraction(domain["centre_high"]) == side - low
            and Fraction(manifest["E"]) == half_width,
            f"node {r}: the centre domain is not the per-bin domain at step {step}",
        )
        text = (folder / "input.txt").read_bytes()
        require(sha256(text) == manifest["input_sha256"], f"node {r}: the input's digest")
        lines = text.decode().splitlines()
        cosine = (1 - t * t) / (1 + t * t)
        sine = 2 * t / (1 + t * t)
        for position, exact in enumerate((side, core, half_width, cosine, sine, Fraction(1))):
            low_end, high_end = enclosure(lines[position])
            require(low_end <= exact <= high_end, f"node {r}: input line {position + 1}")
        require(int(lines[6]) == images, f"node {r}: the input lists {lines[6]} rectangles")
        # The rectangle lines are the same at every node: checked against the expanded
        # candidate once, and held byte for byte to that at every other node.
        if block is None:
            rectangle_block(candidate, lines[7:])
            block = lines[7:]
        require(lines[7:] == block, f"node {r}: the rectangle lines differ from node 1's")
        record = certificate["results"][str(r)]
        require(
            (int(record["nodes"]), float(record["lower"]))
            == (int(result["nodes"]), float(result["lower"])),
            f"node {r}: the certificate's record is not the run's",
        )
        seconds += float(result["seconds"])
        nodes += int(result["nodes"])
    axis = json.loads((root / "proof/axis/result.json").read_text())
    require(
        axis["status"] == "AXIS_VERIFIED"
        and axis["net_index"] == 0
        and axis["gamma"] == "1"
        and axis["digest"] == digest
        and Fraction(axis["mass"]) == Fraction(candidate["total_mass"])
        and axis["integer_unresolved"] == 0
        and axis["witness"] is None
        and Fraction(axis["integer_minimum"]) >= 1,
        "the axis record is not a complete run at threshold one",
    )
    return {
        "kind": "wand125-declared-net-bundle/v1",
        "certificate": stated.name,
        "status": "BUNDLE_BOUND_TO_PACKET_AND_NET",
        "listed_files": len(listed),
        "code_files": len(code),
        "oblique_inputs": count - 1,
        "rectangle_images": images,
        "rectangle_lines": "ENCLOSE_THE_EXPANDED_CANDIDATE",
        "upstream_oblique_seconds": seconds,
        "upstream_oblique_nodes": nodes,
        "axis": {
            "cells": axis["cells"],
            "integer_minimum": axis["integer_minimum"],
            "seconds": axis["seconds"],
        },
        "scope": (
            "The bundle's files against its own list and the packet, every shipped record"
            " and input header against the declared net's tangent, per-bin domain and"
            " threshold, and every input's rectangle lines against the expanded candidate."
            " No coverage is decided here."
        ),
    }


#: Files the bundle's driver writes in its copy of the bundle, besides each node's
#: record: compared by their content, never by their bytes.
DRIVER_OUTPUTS = frozenset(
    {"bundle.json", "files-sha256.json", "proof/replay-progress.json", "proof/certificate.json"}
)
#: What the driver builds and leaves in its copy: present only where it ran.
DRIVER_BINARY = "proof/replay-verify"


def read_meta(path: Path) -> dict[str, str]:
    """The run's own record (`key: value` lines, as the replay's runner writes them)."""
    meta: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition(": ")
        if separator and key and not key.startswith(" "):
            meta.setdefault(key, value)
    return meta


def record_name(r: int) -> str:
    return "proof/axis/replayed.json" if r == 0 else f"proof/net{r:03d}/replayed.json"


def compare(
    shipped: Path,
    fresh: Path,
    meta: Path,
    directory: Path | None = None,
    *,
    key: str = DEFAULT,
) -> dict[str, Any]:
    """A replay by the bundle's own driver, in a copy of the bundle, against the shipped
    run: that the run happened, and that every record it regenerated is the shipped one.

    The run happened when its runner's record says it started and exited zero, the
    driver's progress record counts every node done, the driver's binary is in the copy,
    and every node's record was written after the run started. Every regenerated record
    equals the shipped one and the retained certificate's, field by field; the copy's
    certificate, if the driver rewrote it, equals the retained one as a mapping, whatever
    its order; the copy's `bundle.json` reports the replay; and every other shipped file
    is unchanged.
    """
    stated = CERTIFICATES[key]
    directory = directory or stated.directory
    candidate, certificate, _manifest = read_directory(directory)
    count = int(candidate["proof_net"]["last"]) + 1
    run = read_meta(meta)
    differing: list[str] = []
    if run.get("exit") != "0":
        differing.append(f"the run did not exit zero: {run.get('exit')}")
    started = run.get("start", "")
    start_time = datetime.fromisoformat(started).timestamp() if started else None
    progress_path = fresh / "proof/replay-progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.is_file() else {}
    if progress != {"done": count, "total": count}:
        differing.append(f"the driver's progress record is {progress or 'missing'}")
    if not (fresh / DRIVER_BINARY).is_file() or (shipped / DRIVER_BINARY).exists():
        differing.append("the driver's binary is not in the copy alone")
    matching = 0
    for r in range(count):
        name = record_name(r)
        after = fresh / name
        if not after.is_file():
            differing.append(f"{name}: missing")
            continue
        if start_time is None or after.stat().st_mtime < start_time:
            differing.append(f"{name}: not written by this run")
            continue
        regenerated = load_json(after.read_bytes())
        if regenerated != load_json((shipped / name).read_bytes()):
            differing.append(f"{name}: differs from the shipped record")
        elif regenerated != certificate["results"][str(r)]:
            differing.append(f"{name}: differs from the retained certificate's record")
        else:
            matching += 1
    rewritten = fresh / "proof/certificate.json"
    if rewritten.is_file() and load_json(rewritten.read_bytes()) != certificate:
        differing.append("proof/certificate.json: differs from the retained certificate")
    fresh_bundle = json.loads((fresh / "bundle.json").read_text())
    if (fresh_bundle.get("status"), fresh_bundle.get("certificate")) != (
        "REPLAYED_PROOF_BUNDLE",
        "ALL_ANGLES_VERIFIED_AND_REPLAYED",
    ):
        differing.append(f"bundle.json reports {fresh_bundle}")
    unchanged = 0
    for path in sorted(shipped.rglob("*")):
        name = path.relative_to(shipped).as_posix()
        if not path.is_file() or name.endswith("replayed.json") or name in DRIVER_OUTPUTS:
            continue
        other = fresh / name
        if not other.is_file() or other.read_bytes() != path.read_bytes():
            differing.append(f"{name}: changed by the replay")
        else:
            unchanged += 1
    return {
        "kind": "wand125-declared-net-compare/v2",
        "certificate": stated.name,
        "status": "FULL_REPLAY_MATCHES_SHIPPED" if not differing else "MISMATCH",
        "run": {key: run.get(key) for key in ("start", "end", "exit")},
        "progress": progress,
        "fresh_status": fresh_bundle.get("certificate"),
        "fresh_bundle_status": fresh_bundle.get("status"),
        "certificate_rewritten": rewritten.is_file()
        and rewritten.read_bytes() != (shipped / "proof/certificate.json").read_bytes(),
        "records_matching": matching,
        "records": count,
        "unchanged_shipped_files": unchanged,
        "differing": differing,
        "certificate_sha256": sha256(read_retained_bytes(directory / "certificate.json")),
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def unpack(stated: Certificate, tarball: Path, into: Path) -> tuple[Path, dict[str, Any]]:
    """The pinned tarball, unpacked afresh under ``into``.

    Refused unless its size and SHA-256 are the packet's pin, or if any member lies
    outside its one top-level directory or is not a plain file or directory. The members'
    file times are the archive's, so a record a later run writes is newer than every
    shipped one.
    """
    digest, size = stated.tarball_pin()
    require(
        tarball.stat().st_size == size and file_sha256(tarball) == digest,
        f"{tarball} is not the pinned {stated.tarball}",
    )
    if into.exists():
        shutil.rmtree(into)
    into.mkdir(parents=True)
    with tarfile.open(tarball, "r:gz") as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            require(
                name.parts[0] == stated.bundle_name
                and ".." not in name.parts
                and not name.is_absolute()
                and (member.isfile() or member.isdir()),
                f"unexpected archive member: {member.name}",
            )
        archive.extractall(into, filter="data")
    return into / stated.bundle_name, {"name": stated.tarball, "sha256": digest, "bytes": size}


def shipped_modules() -> Any:
    """`devtools.audit_wand125_point_and_mixed`, whose replay functions run the source's
    per-node checks on any mixed bundle, its declared net included."""
    return importlib.import_module("devtools.audit_wand125_point_and_mixed")


def sample(
    key: str, tarball: Path, work: Path, nodes: list[int], workers: int
) -> dict[str, Any]:
    """Replay ``nodes`` of the net with the source's checker, after binding the bundle.

    The bundle is unpacked afresh and bound by `bundle`; then
    `audit_wand125_point_and_mixed.n50_replay` repeats the full driver's preconditions in
    its order and calls the source's per-node functions, unchanged, on each node, with
    the checker the source's ``compile_verifier`` builds. Each node passes only if it
    returns the shipped record. The price of the rest is the sample's CPU over the
    bundle's own seconds on the same nodes, times the bundle's seconds on every node.
    """
    stated = CERTIFICATES[key]
    mixed = shipped_modules()
    root, pin = unpack(stated, tarball, work / "sample")
    binding = bundle(root, key=key)
    runtime = mixed.replay_runtime()
    started = utc_now()
    report = mixed.n50_replay(root, nodes, workers)
    rows = report.pop("rows")
    return {
        "kind": "wand125-declared-net-sample/v1",
        "certificate": stated.name,
        "status": report.pop("status"),
        "nodes": report.pop("indices"),
        "workers": workers,
        "started": started,
        "ended": utc_now(),
        "rows": rows,
        "sample_cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 1),
        **report,
        "tarball": pin,
        "binding": {
            field: binding[field] for field in ("status", "listed_files", "code_files")
        },
        "environment": runtime,
        "host": mixed.host_facts(),
        "loadavg_end": list(os.getloadavg()),
    }


def numpy_version() -> str:
    try:
        return importlib.import_module("numpy").__version__
    except ImportError:
        return "absent"


def compiler_version() -> str:
    try:
        output = subprocess.run(
            ["c++", "--version"], capture_output=True, text=True, check=True
        )
    except OSError, subprocess.CalledProcessError:
        return "absent"
    return output.stdout.splitlines()[0]


def replay(
    key: str, tarball: Path, work: Path, workers: int, out: Path | None = None
) -> dict[str, Any]:
    """The bundle's own driver over every node, as its README says, then `compare`.

    The pinned tarball is unpacked twice. The first copy is bound by `bundle`, whose
    receipt is written beside the run's; the driver runs in the second,
    ``OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/verify_mixed_full_proof.py
    proof --workers W`` with this interpreter as ``python3``. The run's record,
    ``run.meta``, holds its start, exit and end, and the CPU of the driver and of every
    process it waited for, its pooled workers and their checker runs among them, read
    from ``wait4``; ``run.stdout`` is what it printed.
    """
    stated = CERTIFICATES[key]
    out = out or stated.receipts / "full"
    out.mkdir(parents=True, exist_ok=True)
    shipped, pin = unpack(stated, tarball, work / "shipped")
    write_or_check(stated.receipts / "bundle.json", bundle(shipped, key=key), check=False)
    fresh, _pin = unpack(stated, tarball, work / "run")
    command = [sys.executable, "code/verify_mixed_full_proof.py", "proof"]
    command += ["--workers", str(workers)]
    environment = os.environ | {
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    lines = [
        "command: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 " + " ".join(command),
        f"cwd: {fresh}",
        f"tarball: {pin['name']} sha256 {pin['sha256']} bytes {pin['bytes']}",
        f"python: {platform.python_version()} numpy {numpy_version()}",
        f"cxx: {compiler_version()}",
        (
            f"host: {platform.system()} {platform.release()} {platform.machine()},"
            f" {os.cpu_count()} cpus"
        ),
        f"niceness: {os.nice(0)}",
        f"start: {utc_now()}",
        "loadavg_start: " + " ".join(f"{value:.2f}" for value in os.getloadavg()),
    ]
    clock = time.monotonic()
    with (out / "run.stdout").open("wb") as stdout:
        process = subprocess.Popen(
            command, cwd=fresh, env=environment, stdout=stdout, stderr=subprocess.STDOUT
        )
        _pid, status, usage = os.wait4(process.pid, 0)
        process.returncode = os.waitstatus_to_exitcode(status)
    lines += [
        f"exit: {process.returncode}",
        f"end: {utc_now()}",
        "loadavg_end: " + " ".join(f"{value:.2f}" for value in os.getloadavg()),
        f"wall_seconds: {time.monotonic() - clock:.1f}",
        f"cpu_user_seconds: {usage.ru_utime:.1f}",
        f"cpu_system_seconds: {usage.ru_stime:.1f}",
        f"cpu_seconds: {usage.ru_utime + usage.ru_stime:.1f}",
        f"max_rss_kb: {usage.ru_maxrss}",
    ]
    (out / "run.meta").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return compare(shipped, fresh, out / "run.meta", key=key)


#: The factor ``control``'s first mutant scales every mass by.
CONTROL_FACTOR = Fraction(99, 100)
#: How far below 1 the second mutant's capture at the exact witness centre is.
NEAR_THRESHOLD = Fraction(1, 10**6)
#: How long one control run of the source's checker may take.
CONTROL_TIMEOUT = 3600


def scaled(data: dict[str, Any], factor: Fraction) -> dict[str, Any]:
    """A copy of a candidate with every mass, and the total, multiplied by ``factor``."""
    mutated = dict(data)
    mutated["rectangles"] = [
        row | {"mass": str(Fraction(row["mass"]) * factor)} for row in data["rectangles"]
    ]
    mutated["total_mass"] = str(
        sum((Fraction(row["mass"]) for row in mutated["rectangles"]), Fraction())
    )
    return mutated


def corrupted_nets(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Three corrupted net declarations, each a copy of the candidate.

    ``coarser-step`` sets the step to ``(1 - B) / B``, where ``B (1 + step) = 1`` and the
    core need not fit inside the unit square; ``short-net`` drops the last node, so the
    net stops before ``tan(pi/8)``; ``extra-field`` adds a field the format does not
    have.
    """
    core = Fraction(data["B"])
    net = data["proof_net"]
    return {
        "coarser-step": data | {"proof_net": net | {"step": str((1 - core) / core)}},
        "short-net": data | {"proof_net": net | {"last": int(net["last"]) - 1}},
        "extra-field": data | {"proof_net": net | {"offset": str(Fraction(net["step"]) / 2)}},
    }


def sqverify_fast_refusal(binary: Path, path: Path, n: int) -> dict[str, Any]:
    """A corrupted net under ``sqverify-fast``: admission must refuse it."""
    argv = [str(binary.resolve()), "--candidate", str(path), "--n", str(n), "--directions"]
    result = subprocess.run(
        [*argv, "0"], capture_output=True, text=True, check=False, timeout=600
    )
    refused = result.returncode != 0 and not any(
        '"verified"' in line for line in result.stdout.splitlines()
    )
    return {
        "returncode": result.returncode,
        "stderr": result.stderr.strip()[-400:],
        "verdict": "REFUSED" if refused else "ACCEPTED",
    }


def control(
    key: str,
    tarball: Path,
    work: Path,
    index: int | None = None,
    sqverify_fast: Path | None = None,
) -> dict[str, Any]:
    """The source's checker on the certificate and its mutants: the stage-4 controls.

    The bundle is unpacked afresh and bound, and the full driver's preconditions run. At
    one oblique node, the least recorded lower bound unless given, a centre of low
    capture is found (`audit_wand125_rectangles.least_covered`) and evaluated exactly.
    ``scale-masses`` multiplies every mass by 99/100 and ``near-threshold`` by the factor
    that leaves that centre's exact capture at ``1 - 10^-6``; each must leave it below 1,
    so each mutant is provably invalid at that node. Each variant is exported by the
    source's ``export`` and run by the checker its ``compile_verifier`` builds, with the
    shipped record's node count as the limit; the original must return the shipped
    record, and both mutants must stop unresolved. Each corrupted net declaration
    (`corrupted_nets`) must be refused by the source's ``candidate_net``, which the
    driver and every export read the net through, and by ``sqverify-fast`` when a binary
    is given.
    """
    stated = CERTIFICATES[key]
    mixed = shipped_modules()
    rectangles = importlib.import_module("devtools.audit_wand125_rectangles")
    root, pin = unpack(stated, tarball, work / "control-bundle")
    bundle(root, key=key)
    runtime = mixed.replay_runtime()
    driver = mixed.driver_preconditions(root)
    certificate = load_json(read_retained_bytes(stated.directory / "certificate.json"))
    oblique = {r: certificate["results"][str(r)] for r in range(1, driver.count)}
    chosen = (
        min(oblique, key=lambda r: (float(oblique[r]["lower"]), r)) if index is None else index
    )
    require(chosen in oblique, "a control runs one oblique net node")
    saved = mixed.check_angle_record(driver.root, chosen, driver.model[-1], driver.domains)
    spec = saved["manifest"]
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    side, core, rects, points = driver.model[:4]
    data = json.loads((driver.root / "candidate.json").read_text())
    require(not points, "the witness search reads rectangle measures only")
    c, s = rectangles.net_rotation(Fraction(spec["t"]))
    domain = (side / 2, Fraction(spec["domain"]["centre_high"]))
    centre = rectangles.least_covered(rects, (c, s), core, domain)
    at_centre = rectangles.coverage_exact(rects, centre, c, s, core)
    near = (1 - NEAR_THRESHOLD) / at_centre
    variants = {
        "original": data,
        "scale-masses": scaled(data, CONTROL_FACTOR),
        "near-threshold": scaled(data, near),
    }
    gamma = Fraction(spec["gamma"])
    binary = work / "control-verify"
    driver.rotated.compile_verifier(binary)
    shipped_input = (driver.root / f"net{chosen:03}" / "input.txt").read_bytes()
    runs: list[dict[str, Any]] = []
    for label, variant in variants.items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        (folder / "candidate.json").write_text(json.dumps(variant, indent=2) + "\n")
        model = density.expand(variant)
        manifest = driver.rotated.export(
            model, chosen, folder / "input.txt", gamma, net_audit.candidate_net(variant)
        )
        at_witness = rectangles.coverage_exact(model[2], centre, c, s, core)
        item: dict[str, Any] = {
            "name": label,
            "candidate_digest": model[-1],
            "input_sha256": manifest["input_sha256"],
            "total_mass": str(model[-2]),
            "witness_coverage_exact": str(at_witness),
            "witness_coverage": float(at_witness),
        }
        if label == "original":
            require(
                manifest == spec and (folder / "input.txt").read_bytes() == shipped_input,
                "the original's export is not the shipped proof's",
            )
        else:
            require(at_witness < 1, f"{label} leaves the witness covered")
            item["factor"] = str(CONTROL_FACTOR if label == "scale-masses" else near)
        run = mixed.control_direction(binary, folder, saved["nodes"], CONTROL_TIMEOUT)
        output = run.get("output") or {}
        if label == "original":
            matches = run.get("returncode") == 0 and run.get("frontier_boxes") == 0
            matches = matches and all(
                output.get(field) == saved[field]
                for field in ("status", "nodes", "leaves", "lower")
            )
            run["verdict"] = "ACCEPTED" if matches else "NOT_ACCEPTED"
        elif "verdict" not in run:
            unresolved = output.get("status") == "ANGLE_UNRESOLVED" and run["frontier_boxes"]
            run["verdict"] = "REFUSED" if unresolved else "ACCEPTED"
        runs.append(item | {"run": run})
        print(json.dumps({"name": label, "verdict": run["verdict"]}), flush=True)
    nets: list[dict[str, Any]] = []
    for label, variant in corrupted_nets(data).items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        path = folder / "candidate.json"
        path.write_text(json.dumps(variant, indent=2) + "\n")
        try:
            net_audit.candidate_net(variant)
        except ValueError as error:
            source = {"verdict": "REFUSED", "message": str(error)}
        else:
            source = {"verdict": "ACCEPTED"}
        item = {"name": label, "proof_net": variant["proof_net"], "source": source}
        if sqverify_fast is not None:
            item["sqverify_fast"] = sqverify_fast_refusal(sqverify_fast, path, stated.n)
        nets.append(item)
        print(json.dumps({"name": label, "verdict": source["verdict"]}), flush=True)
    original, *mutants = runs
    refused = all(item["run"]["verdict"] == "REFUSED" for item in mutants) and all(
        item["source"]["verdict"] == "REFUSED"
        and item.get("sqverify_fast", {"verdict": "REFUSED"})["verdict"] == "REFUSED"
        for item in nets
    )
    passed = original["run"]["verdict"] == "ACCEPTED"
    return {
        "kind": "wand125-declared-net-control/v1",
        "status": "CONTROLS_REFUSED" if passed and refused else "CONTROL_FAILED",
        "certificate": stated.name,
        "n": stated.n,
        "side": str(stated.side),
        "index": chosen,
        "index_choice": "the least lower bound of the certificate's oblique records"
        if index is None
        else "given",
        "shipped_record": {
            field: saved[field] for field in ("status", "nodes", "leaves", "lower")
        },
        "gamma": str(gamma),
        "checker": {
            "source_sha256": spec["source_sha256"],
            "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
            "-fno-fast-math",
            "binary_sha256": file_sha256(binary),
            "argv": ["verify", "input.txt", str(saved["nodes"])],
        },
        "witness": {
            "centre": [str(value) for value in centre],
            "t": spec["t"],
            "domain": [str(value) for value in domain],
            "coverage_exact": str(at_centre),
            "coverage": float(at_centre),
        },
        "runs": runs,
        "nets": nets,
        "sqverify_fast": None if sqverify_fast is None else file_sha256(sqverify_fast),
        "tarball": pin,
        "environment": runtime,
        "host": mixed.host_facts(),
        "scope": (
            "Stage-4 negative controls on the certificate itself: the source's export and"
            " the C++ checker its compile_verifier builds, at one net node with the shipped"
            " record's node limit, on the original and two mutants that leave an exact"
            " witness centre covered below 1 there; and three corrupted net declarations"
            " under the source's net check and, where given, sqverify-fast's admission."
        ),
    }


def write_or_check(path: Path, value: dict[str, Any], *, check: bool) -> int:
    text = retained_json.dumps(value)
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            print(f"{path} differs from a fresh run")
            return 1
        print("RECEIPT_MATCHES")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


def parse_nodes(text: str) -> list[int]:
    """``1,37,100-102`` as a sorted list of node indices."""
    nodes: set[int] = set()
    for part in text.split(","):
        first, _, last = part.partition("-")
        nodes.update(range(int(first), int(last or first) + 1))
    return sorted(nodes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit", help="exact premises from the packet")
    audit_parser.add_argument("--check", action="store_true")
    bundle_parser = commands.add_parser("bundle", help="bind an unpacked bundle")
    bundle_parser.add_argument("--bundle", type=Path, required=True)
    compare_parser = commands.add_parser("compare", help="compare a replay with the shipped")
    compare_parser.add_argument("--shipped", type=Path, required=True)
    compare_parser.add_argument("--fresh", type=Path, required=True)
    compare_parser.add_argument(
        "--meta", type=Path, required=True, help="the run's own record: start, exit, end"
    )
    sample_parser = commands.add_parser("sample", help="replay chosen nodes, and price")
    sample_parser.add_argument("--nodes", type=parse_nodes, required=True, help="1,37,100-102")
    replay_parser = commands.add_parser("replay", help="the bundle's driver over every node")
    control_parser = commands.add_parser("control", help="the original and its mutants")
    control_parser.add_argument("--index", type=int, help="the oblique node; least by default")
    control_parser.add_argument(
        "--sqverify-fast", type=Path, help="a binary to run the corrupted nets through too"
    )
    for running in (sample_parser, replay_parser, control_parser):
        running.add_argument("--tarball", type=Path, required=True)
        running.add_argument("--work", type=Path, required=True)
    for running in (sample_parser, replay_parser):
        running.add_argument("--workers", type=int, default=1)
    for each in (
        audit_parser,
        bundle_parser,
        compare_parser,
        sample_parser,
        replay_parser,
        control_parser,
    ):
        each.add_argument("--certificate", choices=sorted(CERTIFICATES), default=DEFAULT)
        each.add_argument("--out", type=Path, help="the receipt; the packet's by default")
    args = parser.parse_args(argv)
    receipts = CERTIFICATES[args.certificate].receipts
    key = args.certificate
    try:
        if args.command == "audit":
            out = args.out or receipts / "audit.json"
            return write_or_check(out, audit(key=key), check=args.check)
        if args.command == "bundle":
            out = args.out or receipts / "bundle.json"
            return write_or_check(out, bundle(args.bundle, key=key), check=False)
        if args.command == "sample":
            result = sample(key, args.tarball, args.work, args.nodes, args.workers)
            first, last = args.nodes[0], args.nodes[-1]
            out = args.out or receipts / f"sample/nodes-{first:03d}-{last:03d}.json"
            write_or_check(out, result, check=False)
            return 0 if result["status"] == "SAMPLE_REPLAYED" else 1
        if args.command == "control":
            result = control(key, args.tarball, args.work, args.index, args.sqverify_fast)
            write_or_check(args.out or receipts / "control.json", result, check=False)
            return 0 if result["status"] == "CONTROLS_REFUSED" else 1
        if args.command == "replay":
            full = args.out or receipts / "full"
            result = replay(key, args.tarball, args.work, args.workers, full)
            out = full / "compare.json"
        else:
            result = compare(args.shipped, args.fresh, args.meta, key=key)
            out = args.out or receipts / "full/compare.json"
        write_or_check(out, result, check=False)
        return 0 if result["status"] == "FULL_REPLAY_MATCHES_SHIPPED" else 1
    except AuditError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
