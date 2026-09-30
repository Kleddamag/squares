"""Measure spawn transfer of the pinned 1383 source node without proof replay.

This isolates process start and source-object transfer. It does not include
partner-cover admission, row geometry, or the per-step worker task queue.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import pickle
import resource
import time
from pathlib import Path
from queue import Empty
from typing import Any

from strif import atomic_write_text

from benchmarks.bench_n11_indexed_cover import SOURCE_1383, SOURCE_1383_SHA
from devtools import check_n11_generic_sequential as sequential


def _worker(source: dict[str, Any], started: float, output: Any) -> None:
    output.put(
        {
            "ready_after_seconds": time.monotonic() - started,
            "steps": len(source["steps"]),
            "maxrss_platform_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        }
    )


def _require_time(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise TimeoutError("spawn ceiling expired before starting all workers")


def _require_exit(process: Any) -> None:
    if process.exitcode != 0:
        raise RuntimeError(f"spawn worker ended with exit code {process.exitcode}")


def run(*, workers: int, payload_kind: str, max_seconds: float) -> dict[str, Any]:
    if (
        workers not in (1, 3)
        or payload_kind not in ("whole_node", "one_step")
        or not 0 < max_seconds <= 30
    ):
        raise ValueError("admit only one or three workers and a 30-second ceiling")
    manifest = sequential.load_manifest(sequential.MANIFEST)
    source = sequential.load_object(SOURCE_1383_SHA, manifest, SOURCE_1383.parent)
    payload = (
        source
        if payload_kind == "whole_node"
        else {"node_id": source["node_id"], "steps": {1: source["steps"][1]}}
    )
    pickle_bytes = len(pickle.dumps(payload, protocol=pickle.HIGHEST_PROTOCOL))
    context = multiprocessing.get_context("spawn")
    output = context.Queue()
    processes: list[Any] = []
    started = time.monotonic()
    deadline = started + max_seconds
    measurements: list[dict[str, Any]] = []
    reason = ""
    try:
        for _ in range(workers):
            _require_time(deadline)
            process = context.Process(target=_worker, args=(payload, started, output))
            process.start()
            processes.append(process)
        measurements = [
            output.get(timeout=max(0, deadline - time.monotonic())) for _ in processes
        ]
        for process in processes:
            process.join(timeout=max(0, deadline - time.monotonic()))
            _require_exit(process)
        status = "COMPLETE_DIAGNOSTIC"
    except (TimeoutError, RuntimeError, Empty) as error:
        status = "INCOMPLETE_DIAGNOSTIC"
        reason = str(error)
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=2)
                if process.is_alive():
                    process.kill()
                    process.join(timeout=2)
        output.close()
    result: dict[str, Any] = {
        "schema": "n11_spawn_cost_diagnostic_v1",
        "status": status,
        "workers": workers,
        "payload_kind": payload_kind,
        "payload_pickle_bytes": pickle_bytes,
        "max_seconds": max_seconds,
        "spawn_wall_seconds": time.monotonic() - started,
        "worker_measurements": measurements,
        "source_sha256": {
            "benchmark": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "manifest": hashlib.sha256(sequential.MANIFEST.read_bytes()).hexdigest(),
            "source_node": SOURCE_1383_SHA,
        },
        "scope": "Node-object spawn/transfer only; no row geometry or proof credit.",
    }
    if status != "COMPLETE_DIAGNOSTIC":
        result["reason"] = reason
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, choices=(1, 3), required=True)
    parser.add_argument("--payload", choices=("whole_node", "one_step"), required=True)
    parser.add_argument("--max-seconds", type=float, default=20)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(workers=args.workers, payload_kind=args.payload, max_seconds=args.max_seconds)
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {"status": result["status"], "spawn_wall_seconds": result["spawn_wall_seconds"]}
        )
    )


if __name__ == "__main__":
    main()
