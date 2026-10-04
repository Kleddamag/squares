"""Run the native n=17 branch-and-bound search in resumable worker chunks.

This driver is for search and timing. It cannot write a certificate. The state file
contains the complete open queue at each checkpoint, so an interrupted invocation can
repeat work but cannot lose an open subtree.
"""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import os
import resource
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools import n17_bb_native
from devtools import pilot_n17_subpattern_bb as pilot

STATE_SCHEMA = "n17-bb-native-parallel-state/v1"
RECEIPT_SCHEMA = "n17-bb-native-parallel/v1"


@dataclass(frozen=True)
class WorkResult:
    """One bounded depth-first search chunk returned by a worker."""

    nodes: int
    closed_share: float
    queue: tuple[pilot.Node, ...]
    hit_floor: bool
    cpu_seconds: float


@dataclass
class WorkerContext:
    """Process-local native solver state."""

    solver: pilot.Solver | None = None
    pattern: pilot.Pattern | None = None
    settings: pilot.Settings | None = None
    chunk_nodes: int = 0


_worker_context = WorkerContext()


def _float(value: float) -> str:
    return value.hex()


def _node_record(node: pilot.Node) -> dict[str, Any]:
    return {
        "angles": [[_float(lo), _float(hi)] for lo, hi in node.angles],
        "boxes": [[_float(value) for value in box] for box in node.boxes],
        "windows": [
            None if window is None else [_float(window[0]), _float(window[1])]
            for window in node.windows
        ],
        "depth": node.depth,
        "share": _float(node.share),
    }


def _node_from_record(record: dict[str, Any], *, squares: int, pairs: int) -> pilot.Node:
    def pair(values: list[str]) -> tuple[float, float]:
        if not isinstance(values, list) or len(values) != 2:
            raise ValueError("node interval must contain two hexadecimal floats")
        result = float.fromhex(values[0]), float.fromhex(values[1])
        if not all(math.isfinite(value) for value in result) or result[0] > result[1]:
            raise ValueError("node interval must be finite and ordered")
        return result

    if not isinstance(record, dict):
        raise TypeError("parallel state node must be an object")
    if set(record) != {"angles", "boxes", "windows", "depth", "share"}:
        raise ValueError("parallel state node has unknown or missing fields")
    if (
        not isinstance(record["angles"], list)
        or len(record["angles"]) != squares
        or not isinstance(record["boxes"], list)
        or len(record["boxes"]) != squares
        or not isinstance(record["windows"], list)
        or len(record["windows"]) != pairs
    ):
        raise ValueError("parallel state node dimensions do not match the pattern")

    boxes: list[pilot.Box] = []
    for values in record["boxes"]:
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("node box must contain four hexadecimal floats")
        xl, xh, yl, yh = (float.fromhex(value) for value in values)
        if not all(math.isfinite(value) for value in (xl, xh, yl, yh)) or xl > xh or yl > yh:
            raise ValueError("node box must be finite and ordered")
        boxes.append((xl, xh, yl, yh))
    if type(record["depth"]) is not int or record["depth"] < 0:
        raise ValueError("node depth must be a nonnegative integer")
    share = float.fromhex(record["share"])
    if not math.isfinite(share) or not 0.0 <= share <= 1.0:
        raise ValueError("node share must be finite and between zero and one")
    return pilot.Node(
        angles=tuple(pair(values) for values in record["angles"]),
        boxes=tuple(boxes),
        windows=tuple(None if values is None else pair(values) for values in record["windows"]),
        depth=int(record["depth"]),
        share=share,
    )


def _atomic_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(document, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _git_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


def _binding(pattern: pilot.Pattern, settings: pilot.Settings) -> dict[str, Any]:
    return {
        "pattern": list(pattern.names),
        "design": pilot.DEFAULT_DESIGN,
        "parameters": {
            "theta0": settings.theta0,
            "floor": settings.floor,
            "merge_gap": settings.merge_gap,
            "split_ratio": settings.split_ratio,
            "obbt_rounds": settings.obbt_rounds,
            "taylor": settings.taylor,
        },
    }


def _state_document(
    *,
    binding: dict[str, Any],
    queue: list[pilot.Node],
    nodes: int,
    closed_share: float,
    cpu_seconds: float,
    search_cpu_seconds: float,
    cpu_seconds_complete: bool,
    wall_seconds: float,
    hit_floor: bool,
    provenance: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema": STATE_SCHEMA,
        "binding": binding,
        "queue": [_node_record(node) for node in queue],
        "nodes": nodes,
        "closed_tree_share": _float(closed_share),
        "cpu_seconds": cpu_seconds,
        "search_cpu_seconds": search_cpu_seconds,
        "cpu_seconds_complete": cpu_seconds_complete,
        "wall_seconds": wall_seconds,
        "hit_floor": hit_floor,
        "provenance": provenance,
    }


def _load_state(
    path: Path, binding: dict[str, Any]
) -> tuple[
    list[pilot.Node],
    int,
    float,
    float,
    float,
    float,
    bool,
    bool,
    list[dict[str, str]],
]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema") != STATE_SCHEMA:
        raise ValueError(f"unsupported parallel state schema in {path}")
    if document.get("binding") != binding:
        raise ValueError("parallel state belongs to different pattern or search settings")
    provenance = document.get("provenance", [])
    if not isinstance(provenance, list) or any(
        not isinstance(item, dict)
        or set(item) != {"git_revision"}
        or not isinstance(item["git_revision"], str)
        or not item["git_revision"]
        for item in provenance
    ):
        raise TypeError("parallel state provenance entries must name a Git revision")
    pattern = binding.get("pattern")
    if not isinstance(pattern, list) or not all(isinstance(name, str) for name in pattern):
        raise TypeError("parallel state binding pattern must be a list of cell names")
    squares = len(pattern)
    pair_count = squares * (squares - 1) // 2
    raw_queue = document.get("queue")
    if not isinstance(raw_queue, list):
        raise TypeError("parallel state queue must be a list")
    queue = [
        _node_from_record(record, squares=squares, pairs=pair_count) for record in raw_queue
    ]
    nodes = document.get("nodes")
    hit_floor = document.get("hit_floor")
    cpu_seconds_complete = document.get("cpu_seconds_complete")
    if type(nodes) is not int or nodes < 0:
        raise ValueError("parallel state nodes must be a nonnegative integer")
    if type(hit_floor) is not bool:
        raise TypeError("parallel state hit_floor must be Boolean")
    if type(cpu_seconds_complete) is not bool:
        raise TypeError("parallel state cpu_seconds_complete must be Boolean")
    closed_share = float.fromhex(document["closed_tree_share"])
    cpu_seconds = float(document["cpu_seconds"])
    search_cpu_seconds = float(document["search_cpu_seconds"])
    wall_seconds = float(document["wall_seconds"])
    if (
        not math.isfinite(closed_share)
        or not -1e-12 <= closed_share <= 1.0 + 1e-9
        or not all(
            math.isfinite(value) and value >= 0.0
            for value in (cpu_seconds, search_cpu_seconds, wall_seconds)
        )
    ):
        raise ValueError("parallel state totals are outside their admitted ranges")
    accounted_share = closed_share + sum(node.share for node in queue)
    if not hit_floor and not math.isclose(accounted_share, 1.0, abs_tol=1e-9):
        raise ValueError("parallel state queue and closed share do not account for the root")
    if not queue and not hit_floor and not math.isclose(closed_share, 1.0, abs_tol=1e-9):
        raise ValueError("empty parallel state is not a complete exhaustion")
    return (
        queue,
        nodes,
        closed_share,
        cpu_seconds,
        search_cpu_seconds,
        wall_seconds,
        cpu_seconds_complete,
        hit_floor,
        provenance,
    )


def _worker_init(
    native_dir: str,
    cells: tuple[str, ...],
    settings: pilot.Settings,
    chunk_nodes: int,
) -> None:
    n17_bb_native.install(Path(native_dir))
    _worker_context.pattern = pilot.cover_pattern(cells)
    _worker_context.settings = settings
    _worker_context.chunk_nodes = chunk_nodes
    _worker_context.solver = None


def _work(node: pilot.Node) -> WorkResult:
    if (
        _worker_context.pattern is None
        or _worker_context.settings is None
        or _worker_context.chunk_nodes <= 0
    ):
        raise RuntimeError("parallel worker was not initialized")
    if _worker_context.solver is None:
        _worker_context.solver = pilot.Solver(_worker_context.pattern, _worker_context.settings)
    started = time.process_time()
    queue = [node]
    nodes = 0
    closed_share = 0.0
    hit_floor = False
    while queue and nodes < _worker_context.chunk_nodes:
        current = queue.pop()
        nodes += 1
        evaluation = _worker_context.solver.assess(current)
        if evaluation.pruned is not None:
            closed_share += current.share
            continue
        outcome = _worker_context.solver.children(current, evaluation)
        if outcome is None:
            hit_floor = True
            break
        queue.extend(reversed(outcome[1]))
    return WorkResult(
        nodes=nodes,
        closed_share=closed_share,
        queue=tuple(queue),
        hit_floor=hit_floor,
        cpu_seconds=time.process_time() - started,
    )


def _settings_from_args(args: argparse.Namespace) -> pilot.Settings:
    return pilot.Settings(
        theta0=args.theta0,
        floor=args.floor,
        merge_gap=args.merge_gap,
        max_seconds=args.max_seconds,
        split_ratio=args.split_ratio,
        obbt_rounds=args.obbt_rounds,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native-dir", type=Path, required=True)
    parser.add_argument("--cells", required=True, help="comma-separated cell names")
    parser.add_argument("--label", default="")
    parser.add_argument("--control", action="store_true", help="must never certify")
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--max-seconds", type=float, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chunk-nodes", type=int, default=3_000)
    parser.add_argument("--checkpoint-seconds", type=float, default=30.0)
    parser.add_argument("--theta0", type=float, default=pilot.DEFAULT_THETA0)
    parser.add_argument("--floor", type=float, default=pilot.DEFAULT_FLOOR)
    parser.add_argument("--merge-gap", type=float, default=0.0)
    parser.add_argument("--split-ratio", type=float, default=pilot.DEFAULT_SPLIT_RATIO)
    parser.add_argument("--obbt-rounds", type=int, default=3)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument(
        "--certificate",
        "--save-certificate",
        nargs="?",
        const=True,
        help=argparse.SUPPRESS,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.certificate:
        raise SystemExit("parallel native search is benchmark-only and refuses certificates")
    if args.workers <= 0 or args.chunk_nodes <= 0:
        raise SystemExit("--workers and --chunk-nodes must be positive")
    if (
        not math.isfinite(args.max_seconds)
        or not math.isfinite(args.checkpoint_seconds)
        or args.max_seconds <= 0
        or args.checkpoint_seconds <= 0
    ):
        raise SystemExit("--max-seconds and --checkpoint-seconds must be positive")
    if not all(
        math.isfinite(value)
        for value in (args.theta0, args.floor, args.merge_gap, args.split_ratio)
    ):
        raise SystemExit("search settings must be finite")
    if args.floor <= 0 or args.split_ratio <= 0 or args.obbt_rounds < 0:
        raise SystemExit(
            "--floor and --split-ratio must be positive; --obbt-rounds cannot be negative"
        )
    if args.merge_gap != 0.0:
        raise SystemExit("the native parallel search requires --merge-gap 0")
    cells = tuple(part for part in args.cells.split(",") if part)
    if not 1 <= len(cells) <= 7 or len(set(cells)) != len(cells):
        raise SystemExit("--cells must contain one to seven distinct cell names")
    settings = _settings_from_args(args)
    pattern = pilot.cover_pattern(cells)
    binding = _binding(pattern, settings)
    revision = _git_revision()
    invocation_provenance = {
        "git_revision": revision,
    }
    resumed = args.state.is_file()
    if resumed:
        (
            queue,
            nodes,
            closed,
            cpu,
            search_cpu,
            prior_wall,
            prior_cpu_complete,
            hit_floor,
            provenance,
        ) = _load_state(args.state, binding)
    else:
        queue = [pilot.Solver(pattern, settings).root()]
        (
            nodes,
            closed,
            cpu,
            search_cpu,
            prior_wall,
            prior_cpu_complete,
            hit_floor,
            provenance,
        ) = (
            0,
            0.0,
            0.0,
            0.0,
            0.0,
            True,
            False,
            [],
        )
    provenance.append(invocation_provenance)
    started = time.perf_counter()
    self_cpu_started = time.process_time()
    children_started = resource.getrusage(resource.RUSAGE_CHILDREN)

    def save(
        extra_queue: list[pilot.Node],
        *,
        wall_seconds: float | None = None,
        cpu_seconds_complete: bool = False,
    ) -> None:
        _atomic_json(
            args.state,
            _state_document(
                binding=binding,
                queue=[*queue, *extra_queue],
                nodes=nodes,
                closed_share=closed,
                cpu_seconds=cpu,
                search_cpu_seconds=search_cpu,
                cpu_seconds_complete=cpu_seconds_complete,
                wall_seconds=(
                    prior_wall + (time.perf_counter() - started)
                    if wall_seconds is None
                    else wall_seconds
                ),
                hit_floor=hit_floor,
                provenance=provenance,
            ),
        )

    save([])
    n17_bb_native.install(args.native_dir)
    context = mp.get_context("spawn")
    pool = context.Pool(
        args.workers,
        initializer=_worker_init,
        initargs=(str(args.native_dir.resolve()), pattern.names, settings, args.chunk_nodes),
    )
    pending: list[tuple[Any, pilot.Node]] = []
    last_checkpoint = started
    try:
        while (queue or pending) and not hit_floor:
            elapsed = time.perf_counter() - started
            while queue and len(pending) < 2 * args.workers and elapsed < args.max_seconds:
                node = queue.pop()
                pending.append((pool.apply_async(_work, (node,)), node))
                elapsed = time.perf_counter() - started
            completed: list[tuple[Any, pilot.Node]] = []
            for result, original in pending:
                if result.ready():
                    chunk = result.get()
                    nodes += chunk.nodes
                    closed += chunk.closed_share
                    search_cpu += chunk.cpu_seconds
                    hit_floor = hit_floor or chunk.hit_floor
                    queue.extend(chunk.queue)
                    completed.append((result, original))
            if completed:
                completed_ids = {id(result) for result, _ in completed}
                pending = [item for item in pending if id(item[0]) not in completed_ids]
            now = time.perf_counter()
            if now - last_checkpoint >= args.checkpoint_seconds:
                save([original for _, original in pending])
                last_checkpoint = now
                if args.progress:
                    print(
                        json.dumps(
                            {
                                "nodes": nodes,
                                "closed_tree_share": closed,
                                "search_cpu_seconds": round(search_cpu, 3),
                                "wall_seconds": round(prior_wall + now - started, 3),
                                "open": len(queue) + len(pending),
                            },
                            sort_keys=True,
                        ),
                        flush=True,
                    )
            if elapsed >= args.max_seconds and not pending:
                break
            if not completed:
                time.sleep(0.01)
        for result, _original in pending:
            chunk = result.get()
            nodes += chunk.nodes
            closed += chunk.closed_share
            search_cpu += chunk.cpu_seconds
            hit_floor = hit_floor or chunk.hit_floor
            queue.extend(chunk.queue)
        pending.clear()
    except BaseException:
        pool.terminate()
        pool.join()
        raise
    else:
        pool.close()
        pool.join()

    invocation_wall = time.perf_counter() - started
    children_finished = resource.getrusage(resource.RUSAGE_CHILDREN)
    invocation_cpu = (
        time.process_time()
        - self_cpu_started
        + (
            children_finished.ru_utime
            + children_finished.ru_stime
            - children_started.ru_utime
            - children_started.ru_stime
        )
    )
    cpu += invocation_cpu
    total_wall = prior_wall + invocation_wall
    save(
        [],
        wall_seconds=total_wall,
        cpu_seconds_complete=prior_cpu_complete,
    )
    if hit_floor:
        verdict = "unresolved-at-resolution-floor"
    elif queue:
        verdict = "unresolved-at-budget"
    elif math.isclose(closed, 1.0, abs_tol=1e-9):
        verdict = "certified-infeasible"
    else:
        raise RuntimeError("exhausted queue does not account for the complete root")
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "label": args.label,
        "control": args.control,
        "pattern": list(pattern.names),
        "parameters": binding["parameters"],
        "verdict": verdict,
        "nodes": nodes,
        "closed_tree_share": closed,
        "open_at_stop": len(queue),
        "cpu_seconds": round(cpu, 3),
        "search_cpu_seconds": round(search_cpu, 3),
        "cpu_seconds_complete": prior_cpu_complete,
        "wall_seconds": round(total_wall, 3),
        "wall_this_invocation_seconds": round(invocation_wall, 3),
        "workers": args.workers,
        "resumed": resumed,
        "git_revision": revision,
        "git_revisions": list(dict.fromkeys(item["git_revision"] for item in provenance)),
    }
    receipt["mixed_revision_resume"] = len(receipt["git_revisions"]) > 1
    if args.control and verdict == "certified-infeasible":
        receipt["soundness_failure"] = "a control pattern was certified"
    _atomic_json(args.output, receipt)
    print(json.dumps(receipt, sort_keys=True), flush=True)
    return int("soundness_failure" in receipt)


if __name__ == "__main__":
    raise SystemExit(main())
