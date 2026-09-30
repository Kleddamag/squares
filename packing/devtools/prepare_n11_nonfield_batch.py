"""Acquire a bounded selection of pinned non-field proof proposals.

This does not execute upstream code or accept geometry. Every retained compressed
object is checked against the immutable Git index, LFS pointer and decoded hash.
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from strif import atomic_write_bytes, atomic_write_text

from devtools import prepare_n11_nonfield_manifest as manifest_tools
from devtools.prepare_n11_nonfield_manifest import (
    PACKET,
    REPO,
    REVISION,
    Catalog,
    digest,
    require,
    strict_json,
)

INPUT_ARCHIVE = REPO / "attic/n11-proof-inputs" / REVISION


def object_directory_allowed(path: Path) -> bool:
    """Keep bulk reproducible inputs in the ignored, durable source archive."""
    resolved = path.resolve()
    return resolved.is_relative_to(PACKET) or resolved.is_relative_to(INPUT_ARCHIVE)


def checked_bytes(path: Path, pin: dict[str, Any]) -> bytes:
    """Bound both compressed and decoded input before checking its identity."""
    require(path.stat().st_size == pin["compressed_bytes"], "compressed length differs")
    packed = path.read_bytes()
    require(digest(packed) == pin["compressed_sha256"], "compressed hash differs")
    with gzip.GzipFile(fileobj=io.BytesIO(packed)) as source:
        raw = source.read(pin["decoded_bytes"] + 1)
        require(len(raw) == pin["decoded_bytes"], "decoded length differs")
        require(not source.read(1), "decoded input exceeds its declared size")
    require(digest(raw) == pin["decoded_sha256"], "decoded hash differs")
    return packed


def acquire(
    pin: dict[str, Any], *, objects: Path, candidates: dict[str, Path], deadline: float
) -> dict[str, Any]:
    fingerprint = pin["decoded_sha256"]
    target = objects / f"{fingerprint}.gz"
    require(time.monotonic() < deadline, "acquisition deadline expired")
    downloaded = 0
    if target.exists():
        checked_bytes(target, pin)
    elif fingerprint in candidates:
        atomic_write_bytes(target, checked_bytes(candidates[fingerprint], pin))
    else:
        url = (
            "https://media.githubusercontent.com/media/Queuingtheorydotcom/"
            f"11SquaresOptimal/{REVISION}/{pin['object_path']}"
        )
        with urllib.request.urlopen(
            url, timeout=min(20, deadline - time.monotonic())
        ) as source:
            packed = source.read(pin["compressed_bytes"] + 1)
        require(
            len(packed) == pin["compressed_bytes"]
            and digest(packed) == pin["compressed_sha256"],
            "download identity differs",
        )
        # Publication follows both checks; an invalid decoded object is not retained.
        with gzip.GzipFile(fileobj=io.BytesIO(packed)) as source:
            raw = source.read(pin["decoded_bytes"] + 1)
            require(len(raw) == pin["decoded_bytes"] and not source.read(1), "decoded size")
        require(digest(raw) == fingerprint, "download decoded hash differs")
        atomic_write_bytes(target, packed)
        downloaded = len(packed)
    require(time.monotonic() < deadline, "acquisition deadline expired after identity check")
    return {"sha256": fingerprint, "downloaded_bytes": downloaded}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="reviewed manifest.json.gz")
    parser.add_argument("--checkout", type=Path, default=REPO / "attic/11SquaresOptimal")
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit", type=int, choices=range(1, 277), default=4)
    parser.add_argument("--cases", type=int, nargs="+")
    parser.add_argument(
        "--adapter",
        choices=("sequential_wall_seed", "closed_center_partition", "baseline_necessary_d4"),
        default="sequential_wall_seed",
        help="Source recipe to acquire; this never admits its mathematical premises.",
    )
    parser.add_argument("--max-compressed-bytes", type=int, default=20_000_000)
    parser.add_argument("--max-decoded-bytes", type=int, default=150_000_000)
    parser.add_argument("--max-seconds", type=float, default=55)
    args = parser.parse_args()
    require(0 < args.max_seconds <= 120, "acquisition wall limit outside (0,120]")
    require(
        0 < args.max_compressed_bytes <= 150_000_000
        and 0 < args.max_decoded_bytes <= 600_000_000,
        "acquisition byte budget outside allowed range",
    )
    require(not args.out.exists(), "use a new receipt path")
    require(
        object_directory_allowed(args.objects),
        "source objects require packet or pinned archive",
    )
    require(args.out.resolve().is_relative_to(PACKET), "retain intake receipt in packet")
    started = time.monotonic()
    deadline = started + args.max_seconds
    before = Path(__file__).read_bytes()
    helper_before = Path(manifest_tools.__file__).read_bytes()
    packed = args.manifest.read_bytes()
    summary = strict_json(args.manifest.with_name("summary.json").read_bytes())
    require(digest(packed) == summary["manifest_gzip_sha256"], "manifest compressed binding")
    with gzip.GzipFile(fileobj=io.BytesIO(packed)) as source:
        raw = source.read(10_000_001)
        require(len(raw) <= 10_000_000 and not source.read(1), "manifest size ceiling")
    require(digest(raw) == summary["manifest_sha256"], "manifest decoded binding")
    manifest = strict_json(raw)
    require(manifest["source_revision"] == REVISION, "manifest source differs")
    cases = [
        case
        for case in manifest["cases"]
        if case["adapter"] == args.adapter
        and (args.cases is None or case["mask_index"] in args.cases)
    ]
    cases.sort(key=lambda case: (case["reported_rows"], case["declared_decoded_bytes"]))
    cases = cases[: args.limit]
    require(bool(cases), "no selected cases")
    if args.cases is not None:
        require(
            {case["mask_index"] for case in cases} == set(args.cases), "requested cases omitted"
        )
    required = sorted({sha for case in cases for sha in case["required_object_sha256s"]})
    pins = [manifest["objects"][sha] for sha in required]
    require(
        sum(pin["compressed_bytes"] for pin in pins) <= args.max_compressed_bytes
        and sum(pin["decoded_bytes"] for pin in pins) <= args.max_decoded_bytes,
        "selected source closure exceeds byte budget",
    )
    catalog = Catalog(args.checkout, args.objects, fetch=False, deadline=deadline)
    require(digest(catalog.index_raw) == manifest["index_sha256"], "manifest index differs")
    require(
        all(catalog.pin(sha) == manifest["objects"][sha] for sha in required),
        "object pins differ",
    )
    candidates = {
        path.stem: path
        for path in sorted((PACKET / "receipts").glob("**/*.gz"))
        if path.stem in required
    }
    args.objects.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(
            pool.map(
                lambda pin: acquire(
                    pin, objects=args.objects, candidates=candidates, deadline=deadline
                ),
                pins,
            )
        )
    require(Path(__file__).read_bytes() == before, "intake tool changed during acquisition")
    require(
        Path(manifest_tools.__file__).read_bytes() == helper_before,
        "manifest helper changed during acquisition",
    )
    require(time.monotonic() < deadline, "acquisition deadline expired before receipt")
    report = {
        "status": "PINNED_PROPOSALS_ACQUIRED",
        "geometry_verified": False,
        "excluded_case_ids": [],
        "global_optimality_proved": False,
        "source_revision": REVISION,
        "manifest_sha256": digest(raw),
        "intake_tool_sha256": digest(before),
        "manifest_helper_sha256": digest(helper_before),
        "selected_case_ids": [case["mask_index"] for case in cases],
        "selected_adapter": args.adapter,
        "objects_directory": args.objects.resolve().relative_to(REPO).as_posix(),
        "objects": results,
        "compressed_bytes": sum(pin["compressed_bytes"] for pin in pins),
        "decoded_bytes": sum(pin["decoded_bytes"] for pin in pins),
        "wall_seconds": time.monotonic() - started,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(args.out, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "objects"}))


if __name__ == "__main__":
    main()
