"""Audit wand125's mixed certificate on a declared net, and compare a replay of it.

wand125/square-packing-bounds at ``43050ed`` adds ``certificates/mixed_n18_L470``
(jlevy/squares#366), a rectangle density for ``s(18) >= 47/10`` whose candidate declares
its own half-angle net, ``"proof_net": {"step": "1/1001", "last": 415}``, at core side
``999/1000``. `devtools.audit_wand125_point_and_mixed` takes the standard net (step
``83/40000``, 201 nodes) and core ``9977/10000`` as fixed, so it cannot audit this one.
This tool is the first-party part of its import. It was written from the certificate
format, the bundle's data files and lemma N0 of ``sqverify_fast/SOUNDNESS.md``; it
imports no source code and opens no file of a ``code/`` folder, which it compares only
by digest.

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
    file is the retained ``mixed_n50_L740`` copy, and ``proof/verify.cpp`` is the
    checker ``89b674a6...``;
  - at every oblique node, the shipped record's net index, tangent, bin floor and
    per-bin centre domain are lemma N0's exactly, and its input's first lines enclose
    the side, core, domain half-width, cosine and sine exactly, with threshold one and
    eight images of every row;
  - the axis record is at threshold one, with no unresolved cell.

  This binds the source's own runs to the declared net. It decides no coverage either.
- ``compare`` reads a copy of the bundle after the bundle's own driver has replayed it,
  as its README says, and compares every regenerated record with the shipped one.

From ``packing/``::

    .venv/bin/python3 -m devtools.audit_wand125_declared_net audit --check
    .venv/bin/python3 -m devtools.audit_wand125_declared_net bundle --bundle DIR
    .venv/bin/python3 -m devtools.audit_wand125_declared_net compare \\
        --shipped DIR --fresh RUN_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.retained_data import read_retained_bytes
from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
PACKET = WEB / "wand125-mixed-bounds-finer-net-2026-10-05"
DIRECTORY = PACKET / "square-packing-bounds/certificates/mixed_n18_L470"
RECEIPTS = PACKET / "receipts/n18-L470"
N50 = WEB / "wand125-point-and-mixed-2026-09-28/square-packing-bounds/certificates"
N50_DIRECTORY = N50 / "mixed_n50_L740"
#: The source's checker, ``code/mixed_rotated_verify.cpp``, by SHA-256: every mixed
#: certificate of the source so far runs this one.
CHECKER_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
#: The budget gap every mixed certificate leaves below ``n``.
GAP = Fraction(1, 100000)
#: The claim, as the directory's README states it.
N = 18
SIDE = Fraction(47, 10)


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


def audit(directory: Path = DIRECTORY) -> dict[str, Any]:
    """Every exact premise of the certificate, from the retained files alone."""
    candidate, certificate, manifest = read_directory(directory)
    n = candidate["n"]
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    require((n, side) == (N, SIDE), f"the candidate is n = {n}, L = {side}")
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
        for key in (
            "step",
            "count",
            "endpoint",
            "endpoint_check",
            "rotated_side_upper",
            "side_margin",
            "per_edge_margin",
        ):
            require(
                Fraction(str(block[key])) == facts[key], f"{name} net {key} is {block[key]}"
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
        "certificate": "mixed_n18_L470",
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


def bundle(root: Path, directory: Path = DIRECTORY) -> dict[str, Any]:
    """Bind an unpacked proof bundle to the packet and its records to the declared net."""
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
        require(
            sha256((root / "code" / name).read_bytes())
            == sha256((N50_DIRECTORY / "code" / name).read_bytes()),
            f"code/{name} is not the retained mixed_n50_L740 copy",
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
        "certificate": "mixed_n18_L470",
        "status": "BUNDLE_BOUND_TO_PACKET_AND_NET",
        "listed_files": len(listed),
        "code_files": len(code),
        "oblique_inputs": count - 1,
        "rectangle_images": images,
        "upstream_oblique_seconds": seconds,
        "upstream_oblique_nodes": nodes,
        "axis": {
            "cells": axis["cells"],
            "integer_minimum": axis["integer_minimum"],
            "seconds": axis["seconds"],
        },
        "scope": (
            "The bundle's files against its own list and the packet, and every shipped"
            " record and input against the declared net's tangent, per-bin domain and"
            " threshold. No coverage is decided here."
        ),
    }


#: Files the bundle's driver writes in its copy of the bundle besides each node's record.
DRIVER_OUTPUTS = ("bundle.json", "files-sha256.json", "proof/replay-progress.json")


def compare(shipped: Path, fresh: Path, directory: Path = DIRECTORY) -> dict[str, Any]:
    """Every record the driver's replay regenerated, against the shipped one."""
    candidate, _certificate, _manifest = read_directory(directory)
    count = int(candidate["proof_net"]["last"]) + 1
    differing: list[str] = []
    matching = 0
    for r in range(count):
        name = "proof/axis/replayed.json" if r == 0 else f"proof/net{r:03d}/replayed.json"
        before, after = shipped / name, fresh / name
        if not after.is_file() or after.stat().st_mtime <= before.stat().st_mtime:
            differing.append(f"{name}: not regenerated")
        elif json.loads(after.read_text()) != json.loads(before.read_text()):
            differing.append(f"{name}: differs")
        else:
            matching += 1
    unchanged = []
    for path in sorted(shipped.rglob("*")):
        name = path.relative_to(shipped).as_posix()
        if path.is_file() and not name.endswith("replayed.json") and name not in DRIVER_OUTPUTS:
            other = fresh / name
            if not other.is_file() or other.read_bytes() != path.read_bytes():
                differing.append(f"{name}: changed by the replay")
            else:
                unchanged.append(name)
    fresh_bundle = json.loads((fresh / "bundle.json").read_text())
    return {
        "kind": "wand125-declared-net-compare/v1",
        "certificate": "mixed_n18_L470",
        "status": "FULL_REPLAY_MATCHES_SHIPPED" if not differing else "MISMATCH",
        "fresh_status": fresh_bundle.get("certificate"),
        "fresh_bundle_status": fresh_bundle.get("status"),
        "records_matching": matching,
        "records": count,
        "unchanged_shipped_files": len(unchanged),
        "differing": differing,
        "certificate_sha256": sha256(read_retained_bytes(directory / "certificate.json")),
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit", help="exact premises from the packet")
    audit_parser.add_argument("--out", type=Path, default=RECEIPTS / "audit.json")
    audit_parser.add_argument("--check", action="store_true")
    bundle_parser = commands.add_parser("bundle", help="bind an unpacked bundle")
    bundle_parser.add_argument("--bundle", type=Path, required=True)
    bundle_parser.add_argument("--out", type=Path, default=RECEIPTS / "bundle.json")
    compare_parser = commands.add_parser("compare", help="compare a replay with the shipped")
    compare_parser.add_argument("--shipped", type=Path, required=True)
    compare_parser.add_argument("--fresh", type=Path, required=True)
    compare_parser.add_argument("--out", type=Path, default=RECEIPTS / "full/compare.json")
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            return write_or_check(args.out, audit(), check=args.check)
        if args.command == "bundle":
            return write_or_check(args.out, bundle(args.bundle), check=False)
        result = compare(args.shipped, args.fresh)
        write_or_check(args.out, result, check=False)
        return 0 if result["status"] == "FULL_REPLAY_MATCHES_SHIPPED" else 1
    except AuditError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
