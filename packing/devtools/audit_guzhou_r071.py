"""Audit Guzhou0806's R070 and R071 lower bounds for s(17) against R068, before a replay.

Two commits of github.com/Guzhou0806/n17-square-packing follow R068 (T-043): R070 at
``8988d933`` claims ``s(17) > 46604427/10000000`` and R071 at ``8c11f696`` claims
``s(17) > 18641771/4000000``. Both packages are retained in
``resources/web/n17-guzhou-r071-2026-09-30/`` as of ``8c11f696``, their large files as
deterministic gzip, and are read here through `read_retained_bytes`; R068's certificate
and its checker bytes are read from the R068 packet (`devtools.audit_guzhou_r068`).

``structure`` measures what a certificate changes relative to R068's: whether its point
orbits, rule orbits, budget and requested minimum are R068's, its parent side and
target, and how its angle chain refines R068's and the previous release's, with how
many shared intervals keep their core's angle and how many keep the whole core.

``ledgers`` reads R070's published C++ and BigInt partition records and compares them
row by row with `audit_guzhou_r068.compare`, holding the published ``THEOREM.json`` to
the result. R071 publishes no partition records.

``summary`` holds R071's retained completion summary, ``C027_GLOBAL_THEOREM.json``, to
its certificate: the digest, the interval count, the budget, the minimum and surplus it
reports, and the digests it gives for the checker, the launcher and the executable,
against the bytes R068's packet retains and the executable R068's and R070's own runs
record.

``compare RELEASE FRESH`` is the stage 4 instrument: a paired replay's partitions against
the published ones. R071 has none, so its replay passes ``--published FRESH`` and the
fresh C++ and BigInt ledgers are compared with each other.

None of these decides a certificate. The exact sweep is the source's own two checkers,
run by its own launcher; this tool checks what the packet README says about the
certificates and their records, before that replay is priced and run.

Usage (from ``packing/``)::

    .venv/bin/python3 -m devtools.audit_guzhou_r071 structure R071
    .venv/bin/python3 -m devtools.audit_guzhou_r071 ledgers --output OUT.json
    .venv/bin/python3 -m devtools.audit_guzhou_r071 summary
    .venv/bin/python3 -m devtools.audit_guzhou_r071 compare R071 FRESH --published FRESH
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import audit_guzhou_r068 as r068
from devtools.audit_guzhou_r068 import Release, angle_chain, load_json, refinement
from devtools.retained_data import read_retained_bytes

PACKET = r068.WEB / "n17-guzhou-r071-2026-09-30"
SOURCE_ROOT = PACKET / "n17-square-packing"
R070_PACKAGE = SOURCE_ROOT / "certificates/R070-4.6604427"
R071_PACKAGE = SOURCE_ROOT / "certificates/R071-C029"
R070_RESULTS = R070_PACKAGE / "project/followup_c016/results/target_4.6604427"
N = r068.N

RELEASES = {
    "R070": Release(
        "8988d933e10fe89709a01d98b602396c29dd7bd1",
        R070_PACKAGE,
        R070_RESULTS / "certificate.json",
        "8438cae4da93c98a92b0b96560f95d9da8d0ef47287783f3b18a9cb8208167b9",
        R070_RESULTS / "paired_replay",
        Fraction(46604427, 10000000),
        5107,
    ),
    "R071": Release(
        "8c11f6962506940c5de67a9fa73b3d1e2e151196",
        R071_PACKAGE,
        R071_PACKAGE / "bounds/c027/certificate.json",
        "15b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469",
        R071_PACKAGE / "history/c027",
        Fraction(18641771, 4000000),
        5114,
    ),
}
R068 = r068.RELEASES["R068"]
#: The release whose angle chain each certificate refines, by its own lineage.
PREVIOUS = {"R070": R068, "R071": RELEASES["R070"]}
PREVIOUS_NAME = {"R070": "R068", "R071": "R070"}
#: R068's bundled checker, launcher and published paired run, as its packet retains them.
R068_CPP = R068.package / "upstream/cpp"
R068_THEOREM = R068.published / "THEOREM.json"
#: The fields every certificate must share with R068's, the charge it reuses.
SHARED_FIELDS = (
    "L",
    "coordinate_denominator",
    "weight_denominator",
    "budget_units",
    "minimum_units",
    "point_orbits",
    "threshold_orbits",
)


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _carry_over(previous: list[list[str]], current: list[list[str]]) -> dict[str, int]:
    """How many intervals ``current`` shares with ``previous``, and what each keeps."""
    before = {(entry[0], entry[1]): entry for entry in previous}
    shared = [entry for entry in current if (entry[0], entry[1]) in before]
    return {
        "shared_intervals": len(shared),
        "shared_same_core_angle": sum(before[(e[0], e[1])][2] == e[2] for e in shared),
        "shared_same_core": sum(before[(e[0], e[1])] == e for e in shared),
    }


def structure(name: str) -> dict[str, Any]:
    """What the release's certificate changes relative to R068's, and to its predecessor."""
    release = RELEASES[name]
    base = load_json(R068.certificate, R068.sha256)
    cert = load_json(release.certificate, release.sha256)
    previous = PREVIOUS[name]
    before = load_json(previous.certificate, previous.sha256)
    parent = Fraction(cert["A"])
    target = Fraction(cert["normalized_target"])
    _require(target == release.target, "normalized_target is not the release's claim")
    _require(Fraction(cert["L"]) / parent == target, "L / A is not the normalized target")
    chain = angle_chain(cert["entries"])
    _require(len(chain) == release.intervals, "the interval count is not the claim")
    shared = {field: cert[field] == base[field] for field in SHARED_FIELDS}
    return {
        "schema": "GuzhouR071PacketStructure/v1",
        "release": name,
        "source_commit": release.commit,
        "certificate_sha256": release.sha256,
        "r068_certificate_sha256": R068.sha256,
        "target": str(target),
        "parent_side": str(parent),
        "r068_parent_side": base["A"],
        "advance_over_r068": str(target - R068.target),
        "previous_release": PREVIOUS_NAME[name],
        "advance_over_previous": str(target - previous.target),
        "same_as_r068": shared,
        "charge_is_r068s": all(shared.values()),
        "point_orbits": len(cert["point_orbits"]),
        "rule_orbits": len(cert["threshold_orbits"]),
        "budget_units": cert["budget_units"],
        "requested_minimum_units": cert["minimum_units"],
        "requested_surplus_units": N * cert["minimum_units"] - cert["budget_units"],
        "declared_base_sha256": cert.get("research_change", {}).get("base_sha256"),
        "source_note": cert.get("source"),
        "angle_chain_over_r068": refinement(angle_chain(base["entries"]), chain),
        "angle_chain_over_previous": refinement(angle_chain(before["entries"]), chain),
        "cores_over_previous": _carry_over(before["entries"], cert["entries"]),
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(read_retained_bytes(path)).hexdigest()


def ledgers() -> dict[str, Any]:
    """R070's published C++ and BigInt ledgers row by row, and its THEOREM.json against them."""
    release = RELEASES["R070"]
    result = r068.compare("R070", release.published, release.published, release=release)
    theorem = load_json(release.published / "THEOREM.json")
    inputs = load_json(release.published / "INPUTS.json")
    checks = {
        "status": theorem["status"] == "PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION",
        "target": theorem["target"] == str(release.target),
        "intervals": theorem["intervals"] == release.intervals,
        "certificate": theorem["certificate_sha256"] == release.sha256,
        "minimum": int(theorem["minimum_units"]) == result["minimum_units"],
        "budget": int(theorem["budget_units"]) == result["budget_units"],
        "surplus": int(theorem["surplus"]) == result["surplus_units"],
        "inputs": all(theorem[key] == value for key, value in inputs.items()),
    }
    published = {key: value for key, value in result.items() if not isinstance(value, dict)}
    for key in ("canonical_rows_sha256", "triples_sha256"):
        published[key] = {k: v for k, v in result[key].items() if k.startswith("published-")}
    return {
        **published,
        "schema": "GuzhouR070PublishedLedgers/v1",
        "partitions": result["partitions"]["published"],
        "ledgers_compared": 2,
        "cpp_header": result["cpp_headers"]["published"],
        "theorem_agrees": checks,
        "consistent": all(checks.values()),
        "theorem_seconds": theorem["seconds"],
        "theorem_processes": len(theorem["processes"]),
    }


def summary() -> dict[str, Any]:
    """R071's completion summary against its certificate and the checker bytes it names."""
    release = RELEASES["R071"]
    cert = load_json(release.certificate, release.sha256)
    record = load_json(release.published / "C027_GLOBAL_THEOREM.json")
    r068_run = load_json(R068_THEOREM)
    r070_run = load_json(RELEASES["R070"].published / "THEOREM.json")
    minimum = int(record["minimum_units"])
    checks = {
        "status": record["status"] == "PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION",
        "certificate": record["certificate_sha256"] == release.sha256,
        "target": record["target"] == cert["normalized_target"] == str(release.target),
        "intervals": record["intervals"] == len(cert["entries"]) == release.intervals,
        "budget": int(record["budget_units"]) == cert["budget_units"],
        "surplus": int(record["surplus"]) == N * minimum - cert["budget_units"] > 0,
        "minimum_reaches_request": minimum >= cert["minimum_units"],
        "reference_is_r068s": record["reference_sha256"]
        == _sha256(R068_CPP / "reference/verify_global_variable.js"),
        "launcher_is_r068s": record["launcher_sha256"] == _sha256(R068_CPP / "replay.js"),
        "executable_is_r068_and_r070_runs": record["executable_sha256"]
        == r068_run["executable_sha256"]
        == r070_run["executable_sha256"],
        "every_process_exited_zero": all(
            p["exit"] == 0 and p["signal"] is None and not p["expired"]
            for p in record["processes"]
        ),
    }
    return {
        "schema": "GuzhouR071CompletionSummary/v1",
        "release": "R071",
        "certificate_sha256": release.sha256,
        "minimum_units": minimum,
        "surplus_units": N * minimum - cert["budget_units"],
        "partitions": len(record["processes"]) // 2,
        "seconds": record["seconds"],
        "verified_utc": record["verified_utc"],
        "checks": checks,
        "consistent": all(checks.values()),
        "partition_records_published": False,
    }


def exit_code(receipt: dict[str, Any]) -> int:
    """1 when a receipt reports a differing row or a record inconsistent with its rows."""
    failed = receipt.get("mismatches") or receipt.get("consistent") is False
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    shape = commands.add_parser("structure", help="a certificate against R068's")
    shape.add_argument("release", choices=sorted(RELEASES))
    shape.add_argument("--output", type=Path)
    rows = commands.add_parser("ledgers", help="R070's published ledgers row by row")
    rows.add_argument("--output", type=Path)
    record = commands.add_parser("summary", help="R071's completion summary")
    record.add_argument("--output", type=Path)
    replay = commands.add_parser("compare", help="a paired replay against published rows")
    replay.add_argument("release", choices=sorted(RELEASES))
    replay.add_argument("fresh", type=Path)
    replay.add_argument("--published", type=Path)
    replay.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.command == "structure":
        receipt = structure(args.release)
    elif args.command == "ledgers":
        receipt = ledgers()
    elif args.command == "summary":
        receipt = summary()
    else:
        release = RELEASES[args.release]
        receipt = r068.compare(args.release, args.fresh, args.published, release=release)
    text = json.dumps(receipt, indent=2) + "\n"
    if args.output is not None:
        with atomic_output_file(args.output) as temporary:
            Path(temporary).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return exit_code(receipt)


if __name__ == "__main__":
    raise SystemExit(main())
