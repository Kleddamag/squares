"""Reproduce the pinned tools' missing mass-budget admission check.

This runs upstream code only in explicitly supplied scratch. The retained output is
a negative control, never a packing certificate: s(1)=1, whereas the upstream driver
announces s(1)>=3/2 after verifying a density of mass 289/10.

From packing/:
    python -m devtools.audit_wand125_tools CHECKOUT --scratch EMPTY_DIR --out RECEIPTS
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from strif import atomic_output_file

REVISION = "0d33ab61726c2ab03e3eb8f457dabaf22db8571f"


def reproduce(checkout: Path, scratch: Path, out: Path, timeout: float) -> dict:
    """Require the pinned clean source and retain the actual coverage-only acceptance."""
    revision = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    if revision != REVISION or dirty:
        raise ValueError("negative control requires the pinned, unmodified source")
    if scratch.exists() and any(scratch.iterdir()):
        raise ValueError("scratch must be new or empty")
    scratch.mkdir(parents=True, exist_ok=True)
    search = scratch / "search"
    search.mkdir()
    candidate = {
        "n": 1,
        "L": "3/2",
        "B": "9977/10000",
        "rectangles": [["1/1000", "1/1000", "1499/1000", "1499/1000"]],
        "weights": ["1/2"],
    }
    # L is a decimal so the driver's human-readable false claim is unambiguous.
    candidate["L"] = "1.5"
    candidate_text = json.dumps(candidate, indent=2) + "\n"
    (search / "candidate.json").write_text(candidate_text)
    proof = scratch / "proof"
    command = [
        sys.executable,
        str(checkout / "transfer/scale_and_verify.py"),
        str(search),
        str(proof),
        "--workers",
        "2",
        "--solver-dir",
        str(checkout / "solver"),
    ]
    run = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    out.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(out / "admission-control.log") as temporary:
        temporary.write_text(run.stdout + run.stderr)
    with atomic_output_file(out / "admission-input.json") as temporary:
        temporary.write_text(candidate_text)
    if run.returncode != 0:
        raise ValueError(f"upstream run failed with exit {run.returncode}; see retained log")
    summary = json.loads((proof / "verification_summary.json").read_text())
    metadata = json.loads((proof / "certificate_metadata.json").read_text())
    scaled = json.loads((scratch / "proof.candidate.json").read_text())
    with atomic_output_file(out / "admission-scaled.json") as temporary:
        temporary.write_text(json.dumps(scaled, indent=2) + "\n")
    mass = sum((Fraction(w) for w in scaled["weights"]), Fraction())
    reproduced = (
        summary["status"] == "VERIFIED"
        and summary["angle_cases"] == 201
        and summary["input_sha256"] == metadata["input_sha256"]
        and mass == Fraction(289, 10)
        and Fraction(metadata["mass_exact"]) == mass
        and mass >= 1
        and "certificate for s(1) >= 1.5" in run.stdout
    )
    report = {
        "status": "ADMISSION_DEFECT_REPRODUCED" if reproduced else "NOT_REPRODUCED",
        "source_revision": revision,
        "python": sys.version,
        "command": command,
        "target_n": 1,
        "claimed_side": "3/2",
        "true_side": "1",
        "scaled_mass": str(mass),
        "mass_budget_passed": mass < 1,
        "coverage_summary": summary,
        "certificate_metadata": metadata,
        "meaning": "Negative control: coverage acceptance cannot establish the printed bound.",
    }
    with atomic_output_file(out / "admission-control.json") as temporary:
        temporary.write_text(json.dumps(report, indent=2) + "\n")
    if not reproduced:
        raise ValueError("upstream output did not reproduce the declared admission defect")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=60)
    args = parser.parse_args()
    report = reproduce(
        args.checkout.resolve(), args.scratch.resolve(), args.out.resolve(), args.timeout
    )
    print(report["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
