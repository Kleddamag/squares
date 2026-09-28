"""Compare a replay of evand's ``s(32)`` zeromargin.py sweep with the source's run record.

evand/square-packing ships the per-root records of its own ``zm_d4_sweep.py`` run of
``s32_closed_cover_6.txt`` (``certificates/s32/zeromargin_d4/roots.jsonl``): one line
per root box of the D4 region, with the checker's leaf census. A replay here runs the
same runner, frozen checker and settings, so every root it records at a depth the source
also ran should carry the same census, box for box and leaf for leaf. The runner's own
``summary`` decides whether the replay is clean; this compares it with the source.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.compare_evand_s32_sweep \\
        --records OUT/roots.jsonl --output COMPARISON.json

Exit status 0 when every replayed record's census equals the source's record of the
same root at the same depth, and 1 otherwise.

Both record files may be stored as deterministic gzip: the packet keeps the shipped
records and its own replay's as ``roots.jsonl.gz``. They are read through
`devtools.retained_data.read_retained_bytes`, which takes the plain path or the ``.gz``
one, and every digest reported is that of the decompressed bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/evand-square-packing-2026-09-26"
SHIPPED = PACKET / "square-packing/s12/certificates/s32/zeromargin_d4/roots.jsonl"
LEAVES = ("ADM", "CORE", "P1", "MIX", "CHAIN", "TRI", "EMPTY", "UNCERT")


def read_records(path: Path) -> list[dict[str, Any]]:
    """Every complete line; a torn last line from an interrupted run is skipped."""
    records = []
    for line in read_retained_bytes(path).decode("utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def _shown(records: list[dict[str, Any]]) -> dict[str, Any]:
    """The runner's summary rule: a certified record (least depth) if any, else the deepest."""
    certified = [r for r in records if r["stats"]["UNCERT"] == 0]
    if certified:
        return min(certified, key=lambda r: r["depth"])
    return max(records, key=lambda r: r["depth"])


def compare(shipped_path: Path, records_path: Path) -> dict[str, Any]:
    shipped: dict[tuple[str, int], dict[str, Any]] = {}
    for record in read_records(shipped_path):
        shipped.setdefault((record["root"], record["depth"]), record)
    region = sorted({root for root, _ in shipped})
    replay = read_records(records_path)
    by_root: dict[str, list[dict[str, Any]]] = {}
    for record in replay:
        by_root.setdefault(record["root"], []).append(record)
    matched = 0
    differs: list[str] = []
    unmatched: list[str] = []
    for record in replay:
        source = shipped.get((record["root"], record["depth"]))
        if source is None:
            unmatched.append(f"{record['root']} at depth {record['depth']}")
        elif source["stats"] == record["stats"]:
            matched += 1
        else:
            differs.append(f"{record['root']} at depth {record['depth']}")
    shown = {root: _shown(records) for root, records in by_root.items()}
    missing = [root for root in region if root not in shown]
    extra = sorted(set(shown) - set(region))
    uncertified = sorted(root for root, r in shown.items() if r["stats"]["UNCERT"])
    deepened = sorted(root for root, r in shown.items() if r["depth"] > 24)
    source_cpu = sum(r["cpu"] for r in shipped.values())
    return {
        "shipped_records": str(shipped_path.relative_to(REPO))
        if shipped_path.is_relative_to(REPO)
        else str(shipped_path),
        "shipped_records_sha256": hashlib.sha256(read_retained_bytes(shipped_path)).hexdigest(),
        "replay_records_sha256": hashlib.sha256(read_retained_bytes(records_path)).hexdigest(),
        "roots_in_region": len(region),
        "replay_records": len(replay),
        "replay_roots": len(shown),
        "missing_roots": len(missing),
        "extra_roots": extra,
        "records_with_census_identical_to_source": matched,
        "records_whose_census_differs": differs,
        "records_at_a_depth_the_source_did_not_run": unmatched,
        "roots_uncertified_in_every_replay_record": uncertified,
        "roots_certified_only_by_a_deeper_record": deepened,
        "replay_boxes_shown": sum(r["stats"]["boxes"] for r in shown.values()),
        "replay_max_depth_shown": max(
            (r["stats"]["maxdepth"] for r in shown.values()), default=0
        ),
        "replay_leaves_shown": {
            k: sum(r["stats"].get(k, 0) for r in shown.values()) for k in LEAVES
        },
        "checker_sha256": sorted({r["checker_sha"] for r in replay}),
        "certificate_sha256": sorted({r["cert_sha"] for r in replay}),
        "replay_cpu_seconds_all_records": round(sum(r["cpu"] for r in replay), 1),
        "source_cpu_seconds_all_records": round(source_cpu, 1),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, required=True, help="the replay's roots.jsonl")
    parser.add_argument("--shipped", type=Path, default=SHIPPED)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare(args.shipped, args.records)
    text = json.dumps(result, indent=1) + "\n"
    if args.output is not None:
        with atomic_output_file(args.output) as handle:
            handle.write_text(text)
    print(text, end="")
    return 0 if not result["records_whose_census_differs"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
