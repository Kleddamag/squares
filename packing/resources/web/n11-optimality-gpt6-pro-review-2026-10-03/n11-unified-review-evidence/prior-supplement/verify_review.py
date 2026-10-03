#!/usr/bin/env python3
"""Replay this review's portable component checks; this is not a global proof runner."""
if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "source-manifest.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest():
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    require(manifest["schema"] == "n11-review-supplement-source-manifest-v1", "Unsupported source manifest")
    rows = manifest["files"]
    require(type(rows) is list and bool(rows), "Empty source manifest")
    expected = set()
    for row in rows:
        relative = row["path"]
        require(type(relative) is str and "\\" not in relative, "Invalid manifest path")
        path = PurePosixPath(relative)
        require(not path.is_absolute() and ".." not in path.parts and path.parts and path.parts[0] != "fresh-results", "Manifest path is outside immutable bundle inputs")
        require(relative not in expected, "Duplicate manifest path")
        expected.add(relative)
        local = BASE / path
        require(local.is_file() and not local.is_symlink(), "Missing/nonregular declared file: " + relative)
        require(local.stat().st_size == row["bytes"], "Byte-count mismatch: " + relative)
        require(digest(local) == row["sha256"], "SHA-256 mismatch: " + relative)
    require("verify_review.py" in expected and "requirements.txt" in expected, "Driver/dependencies missing from manifest")
    actual = {
        p.relative_to(BASE).as_posix()
        for p in BASE.rglob("*")
        if p.is_file()
        and "fresh-results" not in p.relative_to(BASE).parts
        and "__pycache__" not in p.relative_to(BASE).parts
        and p.name != "source-manifest.json"
    }
    require(actual == expected, "Bundle inventory differs; missing=" + str(sorted(expected - actual)) + "; unexpected=" + str(sorted(actual - expected)))
    return manifest, hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hashes-only", action="store_true", help="Check identities only; performs no mathematical replay")
    args = parser.parse_args()
    os.chdir(BASE)
    start = time.monotonic()
    manifest, manifest_sha = check_manifest()
    print(f"Checked {len(manifest['files'])} supplied file identities.", flush=True)
    if args.hashes_only:
        print("PASS_HASHES_ONLY — no mathematical replay was performed.")
        return 0
    require(sys.version_info >= (3, 12), "Use Python 3.12 or newer; Python 3.12 was tested")
    packages = {}
    for name in ("numpy", "scipy", "sympy", "mpmath"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as error:
            raise ValueError("Missing dependency " + name + "; install requirements.txt") from error
    output = BASE / "fresh-results"
    logs = output / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    stages = [
        ("endpoint-root-and-cap", "independent_endpoint_check.py", []),
        ("short-rational-cap", "independent_cap_short_certificate.py", []),
        ("parameter-irreducibility", "independent_irreducibility.py", []),
        ("side-irreducibility", "independent_side_irreducibility.py", []),
        ("exact-witness", "independent_exact_witness.py", []),
        ("symbolic-closing-contact", "independent_witness_simplify.py", []),
        ("d4-read-only-incidence", "verify_d4_review.py", []),
        ("d4-independent-geometry", "d4_independent_geometry.py", []),
        ("simplified-local-first-implementation", "local-isolation-audit/verify_simplified_local.py", ["--output", "fresh-results/simplified-local-result.json"]),
        ("simplified-local-second-implementation", "second_review_simplified_local.py", []),
        ("field-subset-finite-check", "verify_field_subset.py", []),
    ]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
    outcomes = []
    for name, script, arguments in stages:
        script_path = BASE / script
        require(script_path.is_file(), "Missing stage entry point: " + script)
        print("Running " + name + " ...", flush=True)
        stage_start = time.monotonic()
        command = [sys.executable, "-B", str(script_path), *arguments]
        log = logs / (name + ".txt")
        with log.open("wb") as stream:
            result = subprocess.run(command, cwd=BASE, env=env, stdout=stream, stderr=subprocess.STDOUT)
        record = {"stage": name, "script": script, "exit_code": result.returncode, "seconds": time.monotonic() - stage_start, "log": log.relative_to(BASE).as_posix()}
        outcomes.append(record)
        if result.returncode:
            print(log.read_text(errors="replace")[-12000:])
            raise ValueError("Stage failed: " + name + "; see " + str(log))
        print("PASS " + name, flush=True)
    # Independently compare the newly produced scientific local results.
    first = json.loads((output / "simplified-local-result.json").read_bytes())
    second = json.loads((output / "second-review-simplified-local-result.json").read_bytes())
    require(first["status"] == "PASS_SIMPLIFIED_FIXED_T_LOCAL_BOX", "First local result status differs")
    require(second["status"] == "PASS_SECOND_REVIEW_SIMPLIFIED_LOCAL", "Second local result status differs")
    require(first["worst_dual_ratio"] == second["worst_ratio"], "Independent local maximum ratios differ")
    require(first["radii"] == second["radii"], "Independent local rectangles differ")
    require(first["fresh_signed_coordinate_residuals_checked"] == second["independent_residuals_and_dual_margins_checked"] == 8448, "Local obligation counts differ")
    require(first["negative_features_checked"] == second["negative_features_checked"] == 88, "Negative-feature counts differ")
    _, final_manifest_sha = check_manifest()
    require(final_manifest_sha == manifest_sha, "Source manifest changed during replay")
    summary = {
        "status": "PASS_REVIEW_SUPPLEMENT_COMPONENTS",
        "global_optimality_proved": False,
        "whole_global_proof_replayed": False,
        "d4_trace_regenerated": False,
        "field_geometry_rerun": False,
        "field_component": "Exact finite-set and 44-subset minimum verification from the 59 recorded fresh geometry receipts.",
        "local_component": "Both exact implementations rerun; all 8,448 residual margins and all 88 negative features checked in each.",
        "scope": "This is the review supplement, not an end-to-end replay of all 2,180 exclusions or the capture graph. It does not discharge those omitted global premises.",
        "source_manifest_sha256": manifest_sha,
        "python_version": sys.version,
        "dependency_versions": packages,
        "stages": outcomes,
        "seconds": time.monotonic() - start,
    }
    (output / "verification-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: summary[key] for key in ("status", "whole_global_proof_replayed", "field_geometry_rerun", "d4_trace_regenerated", "seconds")}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("REFUSED: " + str(error), file=sys.stderr)
        raise SystemExit(2)
