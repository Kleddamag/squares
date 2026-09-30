"""Compare the preserved walker rule with its conditional-transform optimization.

This measures selection only; it never runs the selected tests. Both modes use
the same checkout and cold selector caches. The control retains the original
unconditional AST transformation, including conservative parse-error handling.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import time
from dataclasses import asdict
from functools import cache
from pathlib import Path

from strif import atomic_write_text

from devtools import reachable_tests as selector


@cache
def control(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        source = ast.unparse(selector._WithoutBenignMetadataVersion().visit(tree))  # noqa: SLF001
    except OSError, SyntaxError, UnicodeDecodeError, RecursionError, ValueError:
        return True
    return any(marker in source for marker in selector.WALKER_MARKERS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error("retain prior evidence: choose a new output path")
    candidate = selector._walker_evidence  # noqa: SLF001
    source_before = Path(selector.__file__).read_bytes()
    records = []
    try:
        for changed in (
            "packing/frontier/n-011.md",
            "packing/src/sqpack/cli/validate.py",
            "packing/devtools/run_negative_controls.py",
        ):
            pair = {}
            for name, implementation in (("control", control), ("candidate", candidate)):
                selector._walker_evidence = implementation  # noqa: SLF001
                selector._imports_of.cache_clear()  # noqa: SLF001
                selector._mapped_files.cache_clear()  # noqa: SLF001
                implementation.cache_clear()
                started, cpu = time.monotonic(), time.process_time()
                selection = selector.select_tests([changed])
                pair[name] = {
                    "wall_seconds": time.monotonic() - started,
                    "cpu_seconds": time.process_time() - cpu,
                    "selection": asdict(selection),
                }
            records.append(
                {
                    "changed": changed,
                    "equivalent": (
                        pair["control"]["selection"] == pair["candidate"]["selection"]
                    ),
                    **pair,
                }
            )
    finally:
        selector._walker_evidence = candidate  # noqa: SLF001
    if Path(selector.__file__).read_bytes() != source_before:
        raise RuntimeError("selector changed during comparison")
    report = {
        "selector_sha256": hashlib.sha256(source_before).hexdigest(),
        "benchmark_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_selections_equal": all(record["equivalent"] for record in records),
        "records": records,
        "scope": "Three cold selector calls per mode on one checkout; no test execution.",
    }
    atomic_write_text(args.out, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "records"}))
    if not report["all_selections_equal"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
