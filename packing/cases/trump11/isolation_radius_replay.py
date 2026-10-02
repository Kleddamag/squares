#!/usr/bin/env python3
"""Replay a retained isolation-radius record from its own declared inputs and compare it.

The retained BC-199 record names its box and symmetry threshold.  The replay runs the
generator that produced it, ``cases.trump11.isolation_radius``, on the repository's
retained exp-013 branch matrices and certificates with those parameters, and compares
every non-timing leaf of the recomputation with the record.  It is a same-implementation
replay: it shows the record is reproducible, not that a second implementation agrees.
Four perturbed copies of the retained record are compared with the same recomputation,
and each must be refused.

The replay lives beside the generator rather than in it because the generator is one of
the eight inputs the BC-241 checker (``devtools.review_trump_local_theorem``) binds byte
for byte to its review revision; a mode added to the generator would break that binding.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

from cases.trump11.isolation_radius import ROOT, VARIABLES, build_result, sha256

TIMING_KEYS = frozenset({"seconds", "elapsed_seconds"})
# The recorded input digests are provenance, not computed values: the replay reports where
# the current files differ from them, and compares every computed leaf.
PROVENANCE_KEYS = frozenset({"inputs"})
ROW_RADIUS_PATH = ("rho_0_weighted", "rational_lower_bound_short")


def differences(retained: object, recomputed: object, path: str = "") -> list[str]:
    """Every computed leaf at which two records disagree; timing and provenance aside."""
    if isinstance(retained, dict) and isinstance(recomputed, dict):
        found: list[str] = []
        for key in sorted(set(retained) | set(recomputed)):
            if key in TIMING_KEYS or (not path and key in PROVENANCE_KEYS):
                continue
            where = f"{path}.{key}" if path else str(key)
            if key not in retained:
                found.append(f"{where}: absent from the retained record")
            elif key not in recomputed:
                found.append(f"{where}: absent from the recomputation")
            else:
                found.extend(differences(retained[key], recomputed[key], where))
        return found
    if isinstance(retained, list) and isinstance(recomputed, list):
        if len(retained) != len(recomputed):
            return [f"{path}: length {len(retained)} retained, {len(recomputed)} recomputed"]
        found = []
        for index, (left, right) in enumerate(zip(retained, recomputed, strict=True)):
            found.extend(differences(left, right, f"{path}[{index}]"))
        return found
    if retained != recomputed or type(retained) is not type(recomputed):
        return [f"{path}: retained {str(retained)[:60]!r}, recomputed {str(recomputed)[:60]!r}"]
    return []


def leaf_count(value: object) -> int:
    if isinstance(value, dict):
        return sum(
            leaf_count(item)
            for key, item in value.items()
            if key not in TIMING_KEYS and key not in PROVENANCE_KEYS
        )
    if isinstance(value, list):
        return sum(leaf_count(item) for item in value)
    return 1


def row_radius(record: dict) -> str:
    value: object = record
    for key in ROW_RADIUS_PATH:
        value = value[key]  # type: ignore[index]
    return str(value)


def perturbations(retained: dict) -> dict[str, dict]:
    """Copies of the retained record with one declared quantity wrong."""
    radius = json.loads(json.dumps(retained))
    radius["rho_0_weighted"]["rational_lower_bound_short"] = "808514698/200000000000"
    witness = json.loads(json.dumps(retained))
    face = witness["branches"][0]["kappa_argmin_face"]
    face["coordinate"] = (face["coordinate"] + 1) % VARIABLES
    modulus = json.loads(json.dumps(retained))
    numerator, denominator = modulus["branches"][0]["kappa_lower"][0].split("/")
    modulus["branches"][0]["kappa_lower"][0] = f"{int(numerator) + 1}/{denominator}"
    box = json.loads(json.dumps(retained))
    box["box_sup_radius"] = "1/65"
    return {
        "radius_off_in_last_digit": radius,
        "argmin_face_witness_moved": witness,
        "exact_kappa_coefficient_off_by_one": modulus,
        "declared_box_changed": box,
    }


def replay(record_path: Path, *, log: Callable[[str], None] | None = None) -> dict:
    """Recompute ``record_path`` from its own declared parameters and compare it."""
    retained = json.loads(record_path.read_text())
    input_digests = {
        path: {
            "recorded": recorded,
            "current": sha256(ROOT / path),
            "unchanged": recorded == sha256(ROOT / path),
        }
        for path, recorded in retained["inputs"].items()
    }
    recomputed = build_result(
        box=Fraction(retained["box_sup_radius"]),
        threshold=Fraction(retained["symmetry"]["threshold"]),
        log=log,
    )
    # Canonicalise through JSON so that tuples and floats compare as the file does.
    recomputed = json.loads(json.dumps(recomputed))
    found = differences(retained, recomputed)
    controls = {
        name: differences(copy, recomputed) for name, copy in perturbations(retained).items()
    }
    return {
        "schema_version": 1,
        "kind": "isolation-radius-replay",
        "record": str(record_path.relative_to(ROOT.parent)),
        "relationship_to_generator": "same-implementation",
        "retained_row_radius": row_radius(retained),
        "recomputed_row_radius": row_radius(recomputed),
        "retained_leaves_compared": leaf_count(retained),
        "recomputed_leaves": leaf_count(recomputed),
        "mismatches": found,
        "status": "passed" if not found else "failed",
        "inputs": input_digests,
        "inputs_drifted": sorted(
            path for path, item in input_digests.items() if not item["unchanged"]
        ),
        "controls": {
            name: {"refused": bool(items), "first_difference": items[0] if items else None}
            for name, items in controls.items()
        },
        "controls_all_refused": all(controls.values()),
        "recomputation_seconds": recomputed["elapsed_seconds"],
    }


def write_atomically(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "record",
        type=Path,
        metavar="RECORD",
        help="recompute RECORD from its declared inputs and compare it leaf by leaf",
    )
    parser.add_argument("--receipt", type=Path, help="write the receipt here")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = replay(args.record.resolve(), log=lambda line: print(line, flush=True))
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        write_atomically(args.receipt, rendered)
    print(rendered, end="")
    return 0 if receipt["status"] == "passed" and receipt["controls_all_refused"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
