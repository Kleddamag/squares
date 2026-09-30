"""Profile prerequisites for an independent n=11 local-isolation consumer.

The current profile stops before reading coordinate-dual proposals. Its status is
always incomplete: the shared exact-geometry source does not prove a local theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

from cases.trump11 import isolation_radius, packing, tangent_cones
from sqpack import exact_lp, field, verify

PACKING = Path(__file__).resolve().parents[1]
SHARED_PUBLISHED_SOURCE_HASHES = {
    "cases/trump11/packing.py": (
        "3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9"
    ),
    "cases/trump11/tangent_cones.py": (
        "17302de574d9f7bc377cbc1dc4c537dc60976d6a1e4e63432adb5fa184058765"
    ),
    "cases/trump11/isolation_radius.py": (
        "3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4"
    ),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def profile_geometry(*, max_seconds: float) -> dict[str, object]:
    if not math.isfinite(max_seconds) or max_seconds <= 0:
        raise ValueError("wall ceiling must be finite and positive")
    started = time.monotonic()
    deadline = started + max_seconds
    source_hashes = {
        name: sha(PACKING / name)
        for name in (
            *SHARED_PUBLISHED_SOURCE_HASHES,
            "src/sqpack/field.py",
            "src/sqpack/verify.py",
            "src/sqpack/exact_lp.py",
        )
    }
    if any(
        source_hashes[name] != expected
        for name, expected in SHARED_PUBLISHED_SOURCE_HASHES.items()
    ):
        raise ValueError("shared exact-geometry source differs from published pin")
    if not all(
        module.__file__ is not None and sha(Path(module.__file__)) == source_hashes[name]
        for name, module in (
            ("cases/trump11/packing.py", packing),
            ("cases/trump11/tangent_cones.py", tangent_cones),
            ("cases/trump11/isolation_radius.py", isolation_radius),
            ("src/sqpack/field.py", field),
            ("src/sqpack/verify.py", verify),
            ("src/sqpack/exact_lp.py", exact_lp),
        )
    ):
        raise ValueError("imported geometry source differs from bound files")
    phases: dict[str, dict[str, float]] = {}

    def phase(name: str, action: object) -> object:
        if not callable(action):
            raise TypeError("phase action must be callable")
        wall_start = time.monotonic()
        cpu_start = time.process_time()
        value = action()
        phases[name] = {
            "wall_seconds": time.monotonic() - wall_start,
            "process_cpu_seconds": time.process_time() - cpu_start,
        }
        if time.monotonic() > deadline:
            raise TimeoutError(f"local profile exceeded wall ceiling in {name}")
        return value

    witness = phase("exact_witness_and_branches", isolation_radius.load_witness)
    assert isinstance(witness, isolation_radius.Witness)
    if len(witness.contacts) != 14 or len(witness.branches) != 128:
        raise ValueError("witness contact or branch inventory differs")
    functions = phase(
        "elementary_value_gradient_generation",
        lambda: isolation_radius.elementary_functions(witness, isolation_radius.DEFAULT_BOX),
    )
    assert isinstance(functions, list)
    if len(functions) != 1936:
        raise ValueError("elementary function count differs")
    contact_pairs = {contact.pair for contact in witness.contacts}
    feature_groups: dict[tuple[object, ...], list[isolation_radius.Elementary]] = {}
    for item in functions:
        if item.kind == "pair" and item.subject[:2] in contact_pairs:
            feature_groups.setdefault(item.subject[:5], []).append(item)
    if len(feature_groups) != 112 or any(
        len(members) != 4 for members in feature_groups.values()
    ):
        raise ValueError("contact-feature inventory differs")
    if time.monotonic() > deadline:
        raise TimeoutError("local profile exceeded wall ceiling in feature inventory")
    return {
        "status": "INCOMPLETE_LOCAL_GEOMETRY_PROFILE",
        "scope": (
            "Exact shared witness/branch and elementary-feature generation only; "
            "no proposal, dual, negative margin, rectangle inclusion, capture, "
            "or global proof checked."
        ),
        "source_shared_with_published_checker": True,
        "source_hashes": source_hashes,
        "checker_sha256": sha(Path(__file__)),
        "contacts": len(witness.contacts),
        "branches": len(witness.branches),
        "elementary_functions": len(functions),
        "contact_features": len(feature_groups),
        "phases": phases,
        "wall_seconds": time.monotonic() - started,
        "max_seconds": max_seconds,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--max-seconds", type=float, default=25.0)
    _ = parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = profile_geometry(max_seconds=args.max_seconds)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
