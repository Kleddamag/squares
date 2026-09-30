"""Compare exact cover kernels on pinned generic mask-2095 rows.

This is a repeatable diagnostic benchmark. Every timed optimized result must
equal the frozen result and the accepted receipt's event/probe counts.
"""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import time
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_generic_fresh as generic
from devtools import check_n11_optimality_field_mask0 as frozen
from devtools import n11_fast_exact_cover as fast

ROWS = (0, 22, 31)
ROUNDS = 3


def _geometry(
    source: dict[str, Any], row_index: int
) -> tuple[frozen.Polygon, list[frozen.Polygon]]:
    step = source["steps"][0]
    row = step["rows"][row_index]
    domain = generic.convex(row["input_domain"])
    core = generic.convex(row["core_vertices"])
    prior = {
        int(owner): generic.hull(generic.points(group))
        for owner, group in step["prior_owned_hulls"].items()
    }
    forbidden = [
        generic.hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
        for owner, group in prior.items()
        if owner != step["owner"]
    ]
    residual = [generic.convex(value) for value in row["residual_polygons"]]
    return domain, forbidden + residual


def _timed(
    cover: Any, domain: frozen.Polygon, regions: list[frozen.Polygon]
) -> tuple[dict[str, int], float]:
    started = time.process_time()
    result = cover(domain, regions, budget=frozen.Budget(time.monotonic() + 20, 50_000))
    return result, time.process_time() - started


def run() -> dict[str, Any]:
    source_path = generic.OBJECTS / f"{generic.SOURCE_PIN[0]}.gz"
    source = generic._load_pin(source_path, generic.SOURCE_PIN)
    receipt_path = generic.PACKET / "receipts/generic-mask2095-intake/full-result.json"
    receipt = json.loads(receipt_path.read_text())
    if receipt["status"] != "PASS_ONE_GENERIC_EXCLUSION":
        raise ValueError("reference receipt is incomplete")
    findings = []
    for row_index in ROWS:
        domain, regions = _geometry(source, row_index)
        frozen_samples: list[float] = []
        fast_samples: list[float] = []
        results: dict[str, dict[str, int]] = {}
        for round_index in range(ROUNDS):
            methods = (
                (("frozen", frozen.exact_union_cover), ("fast", fast.exact_union_cover))
                if round_index % 2 == 0
                else (("fast", fast.exact_union_cover), ("frozen", frozen.exact_union_cover))
            )
            results = {}
            for name, cover in methods:
                result, elapsed = _timed(cover, domain, regions)
                results[name] = result
                (frozen_samples if name == "frozen" else fast_samples).append(elapsed)
            if results["frozen"] != results["fast"]:
                raise ValueError(f"row {row_index}: exact cover outputs differ")
        expected = receipt["step_timings"][0]["row_timings"][row_index]
        if (results["fast"]["events"], results["fast"]["probes"]) != (
            expected["events"],
            expected["probes"],
        ):
            raise ValueError(f"row {row_index}: accepted receipt counts differ")
        frozen_median = statistics.median(frozen_samples)
        fast_median = statistics.median(fast_samples)
        findings.append(
            {
                "row": row_index,
                "coverage": results["fast"],
                "frozen_cpu_seconds": frozen_samples,
                "fast_cpu_seconds": fast_samples,
                "frozen_median_cpu_seconds": frozen_median,
                "fast_median_cpu_seconds": fast_median,
                "median_speedup": frozen_median / fast_median,
            }
        )
    return {
        "schema": "n11_fast_exact_cover_benchmark_v1",
        "status": "DIAGNOSTIC_MATCHED_EXACT_RESULTS",
        "source_sha256": {
            "frozen": hashlib.sha256(Path(frozen.__file__).read_bytes()).hexdigest(),
            "fast": hashlib.sha256(Path(fast.__file__).read_bytes()).hexdigest(),
            "generic": hashlib.sha256(Path(generic.__file__).read_bytes()).hexdigest(),
            "pilot_source": generic.SOURCE_PIN[0],
            "pilot_receipt": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        },
        "rounds_per_row": ROUNDS,
        "rows": findings,
        "median_of_row_speedups": statistics.median(row["median_speedup"] for row in findings),
        "scope": "Three first-step rows of one accepted case; no corpus forecast.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "median_of_row_speedups": result["median_of_row_speedups"],
            }
        )
    )


if __name__ == "__main__":
    main()
