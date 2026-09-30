"""Compare two exact Rust binaries on identical bounded verifier work.

This is a source-bound timing diagnostic. The capped external case remains
INCONCLUSIVE and no result here promotes a rectangle certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from statistics import median
from typing import Any

from benchmarks.bench_rectangle_verifier_parity import (
    ensure_external_scratch,
    run_command,
)
from sqpack import rectangle_density, rust_rectangle_geometry
from sqpack.rectangle_density import load_candidate, verify_candidate

PROJECT = Path(__file__).resolve().parents[1]
CRATE = PROJECT / "sqverify_exact"
ANALYTIC = PROJECT / "resources/web/wand125-tools-2026-09-29/native-analytic-control.json"
EXTERNAL = (
    PROJECT
    / "resources/web/external-square-certificates-2026-09-22/tokoharu-density"
    / "certificates/cert_n11_L381/certified_candidate.json"
)
EXPECTED_INPUT_SHA = {
    "analytic": "bfd6e4dea67a048321836c69c9c9fe782687ffc512ccb1afc43249212ba5f01e",
    "external": "8e3339eefb2fad81868f51e3f72cbc8487b40b66f9d8fbc711c1dbd5e5edeff4",
}
EXPECTED_REPORT_SHA = {
    "analytic": "bd878de9d1f469c749015aea091e96eceb98d8820db3fdc47f3e6562948117c8",
    "external": "68123cb6992b9971c370c1fd677985a1c6c5f31c74390e53c47303d5a5d49105",
}
EXPECTED_BINARY_SHA = {
    "coprime": "d25afa57a162cb821c5cae752209c77df7ff51715430b0d6ffd2f542f09e983b",
}
PAIRS = 3
INTERNAL_SECONDS = 30
INVOCATION_SECONDS = 40
TOTAL_SECONDS = 300
BUILD_SECONDS = 90


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_default(target: Path) -> tuple[Path, dict[str, object]]:
    """Execute the maintained default-feature release build before any paired timing."""
    if not all(os.environ.get(name) for name in ("TMPDIR", "UV_CACHE_DIR", "CARGO_TARGET_DIR")):
        raise ValueError("external TMPDIR, UV_CACHE_DIR and CARGO_TARGET_DIR are required")
    target = target.resolve()
    ensure_external_scratch(target)
    source_paths = (
        CRATE / "Cargo.toml",
        CRATE / "Cargo.lock",
        CRATE / "rust-toolchain.toml",
        CRATE / "src/lib.rs",
        CRATE / "src/main.rs",
    )
    sources = {str(path): _sha(path) for path in source_paths}
    rustc = subprocess.run(
        ["rustc", "-vV"],
        cwd=CRATE,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    cargo = subprocess.run(
        ["cargo", "--version"],
        cwd=CRATE,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()
    command = ["cargo", "build", "--offline", "--locked", "--release"]
    environment = dict(os.environ)
    environment["CARGO_TARGET_DIR"] = str(target)
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=CRATE,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=BUILD_SECONDS,
    )
    if completed.returncode != 0:
        raise ValueError(f"default release build failed: {completed.stderr[-500:]}")
    binary = target / "release/sqverify-exact"
    if sources != {str(path): _sha(path) for path in source_paths}:
        raise ValueError("Rust source changed during default release build")
    return binary, {
        "command": command,
        "cwd": str(CRATE),
        "wall_seconds": time.perf_counter() - started,
        "ceiling_seconds": BUILD_SECONDS,
        "source_sha256": sources,
        "rustc_version": rustc,
        "cargo_version": cargo,
        "rustflags": os.environ.get("RUSTFLAGS", ""),
        "cargo_encoded_rustflags": os.environ.get("CARGO_ENCODED_RUSTFLAGS", ""),
        "binary_sha256": _sha(binary),
    }


def _admit_coprime_build(
    binary: Path, receipt_path: Path, default_build: dict[str, object]
) -> str:
    """Bind the prior measured feature build to this default-source build."""
    prior: Any = json.loads(receipt_path.read_text())
    if not isinstance(prior, dict) or not isinstance(prior.get("arithmetic_ab"), dict):
        raise TypeError("prior coprime build receipt is missing")
    arithmetic: dict[str, Any] = prior["arithmetic_ab"]
    build: Any = arithmetic.get("build")
    if not isinstance(build, dict) or not isinstance(build.get("builds"), list):
        raise TypeError("prior feature build inventory is missing")
    matching = [
        item
        for item in build["builds"]
        if isinstance(item, dict) and item.get("feature") == "experimental-coprime-mul"
    ]
    if (
        len(matching) != 1
        or matching[0].get("binary_sha256") != _sha(binary)
        or build.get("rustc_version") != default_build["rustc_version"]
        or build.get("cargo_version") != default_build["cargo_version"]
        or build.get("rustflags") != default_build["rustflags"]
        or build.get("cargo_encoded_rustflags") != default_build["cargo_encoded_rustflags"]
    ):
        raise ValueError("coprime build differs from the default build environment")
    source_hashes: Any = prior.get("source_sha256")
    if not isinstance(source_hashes, dict):
        raise TypeError("prior feature source inventory is missing")
    default_sources = default_build["source_sha256"]
    assert isinstance(default_sources, dict)
    if any(source_hashes.get(path) != sha for path, sha in default_sources.items()):
        raise ValueError("coprime and default builds used different Rust source")
    return _sha(receipt_path)


def _normalized(report: dict[str, Any]) -> dict[str, Any]:
    expected_metadata = {
        "backend",
        "rust_binary_sha256",
        "rust_table_sha256",
        "backend_timeout",
    }
    if not expected_metadata <= report.keys():
        raise ValueError("Rust report is missing backend metadata")
    if report["backend"] != "rust" or report["backend_timeout"] is not False:
        raise ValueError("Rust report has an unadmitted backend state")
    return {key: value for key, value in report.items() if key not in expected_metadata}


def _report_sha(report: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _worker(dataset: str, binary: Path) -> int:
    source = ANALYTIC if dataset == "analytic" else EXTERNAL
    n = 3 if dataset == "analytic" else 11
    side = Fraction(3, 2) if dataset == "analytic" else Fraction(381, 100)
    candidate = load_candidate(source, n=n, expected_side=side)
    before_child = resource.getrusage(resource.RUSAGE_CHILDREN)
    parent_cpu = time.process_time()
    started = time.perf_counter()
    report = verify_candidate(
        candidate,
        angle_indices=tuple(range(201)) if dataset == "analytic" else (1,),
        max_nodes_per_angle=10_000 if dataset == "analytic" else 1_000,
        max_depth=20,
        max_seconds=INTERNAL_SECONDS,
        bound_mode="common-core",
        retain_pending_boxes=dataset == "external",
        backend="rust",
        rust_binary=binary,
    )
    verification_wall = time.perf_counter() - started
    coordinator_cpu = time.process_time() - parent_cpu
    after_child = resource.getrusage(resource.RUSAGE_CHILDREN)
    print(
        json.dumps(
            {
                "report": report.as_dict(),
                "verification_wall_seconds": verification_wall,
                "coordinator_cpu_seconds": coordinator_cpu,
                "rust_child_cpu_seconds": (
                    after_child.ru_utime
                    + after_child.ru_stime
                    - before_child.ru_utime
                    - before_child.ru_stime
                ),
            },
            sort_keys=True,
        )
    )
    return 0


def _assess(observations: list[dict[str, Any]]) -> dict[str, object]:
    metrics: dict[str, object] = {}
    for dataset in ("analytic", "external"):
        rows = [row for row in observations if row["dataset"] == dataset]
        if len(rows) != 2 * PAIRS:
            raise ValueError("paired verifier census is incomplete")
        if {(row["pair"], row["arm"]) for row in rows} != {
            (pair, arm) for pair in range(PAIRS) for arm in ("default", "coprime")
        }:
            raise ValueError("paired verifier identities are duplicated or missing")
        for field in ("rust_child_cpu_seconds", "invocation_wall_seconds"):
            baseline = [float(row[field]) for row in rows if row["arm"] == "default"]
            candidate = [float(row[field]) for row in rows if row["arm"] == "coprime"]
            if len(baseline) != PAIRS or len(candidate) != PAIRS:
                raise ValueError("paired verifier arms are incomplete")
            metrics[f"{dataset}_{field}"] = {
                "default_median": median(baseline),
                "default_range": [min(baseline), max(baseline)],
                "coprime_median": median(candidate),
                "coprime_range": [min(candidate), max(candidate)],
                "coprime_over_default_median": median(candidate) / median(baseline),
                "paired_coprime_over_default": [
                    float(
                        next(
                            row[field]
                            for row in rows
                            if row["pair"] == pair and row["arm"] == "coprime"
                        )
                    )
                    / float(
                        next(
                            row[field]
                            for row in rows
                            if row["pair"] == pair and row["arm"] == "default"
                        )
                    )
                    for pair in range(PAIRS)
                ],
            }
    external_cpu = metrics["external_rust_child_cpu_seconds"]
    external_wall = metrics["external_invocation_wall_seconds"]
    analytic_wall = metrics["analytic_invocation_wall_seconds"]
    assert isinstance(external_cpu, dict)
    assert isinstance(external_wall, dict)
    assert isinstance(analytic_wall, dict)
    metrics["material_bounded_verifier_improvement"] = (
        external_cpu["coprime_over_default_median"] <= 0.90
        and external_cpu["coprime_range"][1] < external_cpu["default_range"][0]
        and external_wall["coprime_over_default_median"] <= 1.05
        and analytic_wall["coprime_over_default_median"] <= 1.05
    )
    return metrics


def run(
    default_target: Path, coprime_binary: Path, prior_ab_receipt: Path, output: Path
) -> dict[str, object]:
    ensure_external_scratch(output.parent)
    if output.exists():
        raise ValueError("refusing to overwrite a prior verifier A/B receipt")
    default_binary, default_build = _build_default(default_target)
    print(
        "DEFAULT_BUILD_PREFLIGHT " + json.dumps(default_build, sort_keys=True),
        file=sys.stderr,
        flush=True,
    )
    binaries = {"default": default_binary, "coprime": coprime_binary.resolve(strict=True)}
    prior_receipt_sha = _admit_coprime_build(
        binaries["coprime"], prior_ab_receipt, default_build
    )
    source_paths = (
        Path(__file__),
        Path(rectangle_density.__file__),
        Path(rust_rectangle_geometry.__file__),
        PROJECT / "benchmarks/bench_rectangle_verifier_parity.py",
        PROJECT / "sqverify_exact/Cargo.toml",
        PROJECT / "sqverify_exact/Cargo.lock",
        PROJECT / "sqverify_exact/rust-toolchain.toml",
        PROJECT / "sqverify_exact/src/lib.rs",
        PROJECT / "sqverify_exact/src/main.rs",
        ANALYTIC,
        EXTERNAL,
        prior_ab_receipt,
        *binaries.values(),
    )
    before = {str(path): _sha(path) for path in source_paths}
    for dataset, source in (("analytic", ANALYTIC), ("external", EXTERNAL)):
        if before[str(source)] != EXPECTED_INPUT_SHA[dataset]:
            raise ValueError(f"{dataset} input differs from the retained workload")
    for arm, binary in binaries.items():
        expected_binary = (
            default_build["binary_sha256"]
            if arm == "default"
            else EXPECTED_BINARY_SHA["coprime"]
        )
        if before[str(binary)] != expected_binary:
            raise ValueError(f"{arm} binary differs from the retained build")
    started = time.monotonic()
    observations: list[dict[str, Any]] = []
    for dataset in ("analytic", "external"):
        for pair in range(PAIRS):
            order = ("default", "coprime") if pair % 2 == 0 else ("coprime", "default")
            for arm in order:
                if time.monotonic() - started >= TOTAL_SECONDS - INVOCATION_SECONDS:
                    raise TimeoutError("paired verifier benchmark reached its total ceiling")
                binary = binaries[arm]
                command = [
                    sys.executable,
                    "-m",
                    "benchmarks.bench_rectangle_rust_verifier_ab",
                    "--worker",
                    dataset,
                    "--binary",
                    str(binary),
                ]
                outer, stdout, stderr = run_command(
                    command, cwd=PROJECT, timeout=INVOCATION_SECONDS
                )
                if outer["timed_out"] or outer["exit_code"] != 0 or stderr:
                    raise ValueError(
                        f"{dataset}/{pair}/{arm} refused or timed out: {stderr[-500:]}"
                    )
                payload: Any = json.loads(stdout)
                if not isinstance(payload, dict) or not isinstance(payload.get("report"), dict):
                    raise TypeError("worker omitted its exact verifier report")
                report: dict[str, Any] = payload["report"]
                if report["rust_binary_sha256"] != before[str(binary)]:
                    raise ValueError("worker used a different Rust binary")
                normalized = _normalized(report)
                expected_status = "VERIFIED" if dataset == "analytic" else "INCONCLUSIVE"
                expected_nodes = 1781 if dataset == "analytic" else 1000
                if (
                    normalized["status"] != expected_status
                    or sum(angle["nodes"] for angle in normalized["angles"]) != expected_nodes
                    or _report_sha(normalized) != EXPECTED_REPORT_SHA[dataset]
                ):
                    raise ValueError(
                        f"{dataset}/{pair}/{arm} changed the retained exact census"
                    )
                observations.append(
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": arm,
                        "order": order,
                        "status": normalized["status"],
                        "nodes": expected_nodes,
                        "normalized_report_sha256": _report_sha(normalized),
                        "invocation_wall_seconds": outer["wall_seconds"],
                        "verification_wall_seconds": payload["verification_wall_seconds"],
                        "coordinator_cpu_seconds": payload["coordinator_cpu_seconds"],
                        "rust_child_cpu_seconds": payload["rust_child_cpu_seconds"],
                    }
                )
    if before != {str(path): _sha(path) for path in source_paths}:
        raise ValueError("verifier source, input, or binary changed during the benchmark")
    if time.monotonic() - started >= TOTAL_SECONDS:
        raise TimeoutError("paired verifier benchmark exceeded its total ceiling")
    result: dict[str, object] = {
        "status": "MATCHED_BOUNDED_VERIFIER_DIAGNOSTIC_ONLY",
        "created_utc": datetime.now(UTC).isoformat(),
        "source_sha256": before,
        "default_build": default_build,
        "coprime_build_receipt_sha256": prior_receipt_sha,
        "python_executable": sys.executable,
        "python_version": sys.version,
        "settings": {
            "pairs": PAIRS,
            "internal_seconds": INTERNAL_SECONDS,
            "per_invocation_ceiling_seconds": INVOCATION_SECONDS,
            "total_ceiling_seconds": TOTAL_SECONDS,
            "bound_mode": "common-core",
            "analytic": "all 201 angles, 10000 nodes/angle, depth 20, threshold 1",
            "external": "angle 1, 1000 nodes, depth 20, threshold 1, pending retained",
        },
        "observations": observations,
        "assessment": _assess(observations),
        "scope": (
            "Complete analytic control and capped external angle only; the latter remains "
            "INCONCLUSIVE. Invocation wall includes Python startup/admission/serialization "
            "and resident Rust startup/shutdown. Child CPU measures the Rust subprocess; "
            "coordinator CPU excludes it. This is no full certificate or proof claim."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=("analytic", "external"))
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--default-target", type=Path)
    parser.add_argument("--coprime-binary", type=Path)
    parser.add_argument("--prior-ab-receipt", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker is not None:
        if args.binary is None:
            parser.error("worker needs --binary")
        raise SystemExit(_worker(args.worker, args.binary))
    if any(
        item is None
        for item in (
            args.default_target,
            args.coprime_binary,
            args.prior_ab_receipt,
            args.output,
        )
    ):
        parser.error("paired run needs the default target, coprime binary/receipt and output")
    result = run(args.default_target, args.coprime_binary, args.prior_ab_receipt, args.output)
    print(json.dumps({"status": result["status"], "assessment": result["assessment"]}))


if __name__ == "__main__":
    main()
