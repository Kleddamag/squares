"""Audit all fourteen source-bound mask-438 root-induction run receipts.

The audit checks an unbroken receipt and state chain rooted in the fixed first
round. It does not rerun the geometry, prove that a receipt was produced by an
actual execution, or establish candidate capture/global optimality.
"""

from __future__ import annotations

import argparse
import gzip
import json
import time
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import check_n11_capture_root_continue as continuation
from devtools import check_n11_capture_root_pilot as pilot
from devtools import check_n11_capture_root_round1 as first
from devtools import check_n11_optimality_field_mask0 as geometry

FIRST_RESULT_SHA = "488f26c0effe528f29d2cc06f60766e2c1f845f2aac93f65b18c0c4d3b5e76a4"
MODERN_SHA = "17fc81b2b08a80456325b347b3effa25050e4e233d9a984292e0d6339bb64e73"
FINAL_SHA = "3eca359a215cde005b79fbd9f7866000f75b48bb3f50ce0b3a3d9b2d9db83b34"
LEGACY_SHA = continuation.LEGACY_SHA
SEED_GZIP_SHA = "ad9c0c9c00c54301dd49b1fcd771d7a9a3a14e894fe904b949fe415dceddf7f2"
SEED_GZIP_BYTES = 3407
ROWS_TOTAL = 16551
ADDITIONS_TOTAL = 1060


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return continuation.digest(data)


def expected_checker(round_index: int) -> str:
    require(1 <= round_index <= 14, "round index")
    if round_index == 1:
        return continuation.FIRST_SHA
    return LEGACY_SHA if round_index <= 7 else MODERN_SHA if round_index <= 11 else FINAL_SHA


def admit_worker(
    worker: dict[str, Any],
    *,
    owner: int,
    round_index: int,
    selected_sha: str,
    prior_sha: str,
    previous_result_sha: str | None,
    checker_sha: str,
    source_cell: dict[str, Any],
) -> pilot.Polygon:
    require(
        worker["status"] == "PASS_CONDITIONAL_OWNER_UPDATE"
        and worker["owner"] == owner
        and worker["rows_checked"] == len(source_cell["rows"])
        and worker["round_sha256"] == selected_sha
        and worker["prior_sha256"] == prior_sha
        and worker["checker_sha256"] == checker_sha
        and worker["pilot_sha256"] == first.PILOT_SHA
        and worker["geometry_sha256"] == pilot.GEOMETRY_SHA,
        f"round {round_index} owner {owner} binding differs",
    )
    if round_index >= 2:
        require(
            worker["round"] == round_index
            and worker["previous_result_sha256"] == previous_result_sha,
            f"round {round_index} owner {owner} previous binding differs",
        )
        if round_index >= 8:
            require(
                worker["degenerate_sha256"] == continuation.DEGENERATE_SHA,
                f"round {round_index} owner {owner} helper differs",
            )
    proposed = pilot.points(source_cell["inner_grid_compression"]["vertices"])
    accepted = pilot.points(worker["new_points"])
    require(accepted == proposed, f"round {round_index} owner {owner} output differs")
    return accepted


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    result: dict[str, Any] = {
        "status": "REFUSED",
        "root_receipt_chain_verified": False,
        "conditional_root_induction_proved": False,
        "candidate_capture_proved": False,
        "global_optimality_proved": False,
        "checker_sha256": pilot.digest(Path(__file__)),
        "source_revision": continuation.SOURCE_REVISION,
        "premise": (
            "All fourteen local geometric receipt results must have come from actual "
            "accepted executions; this receipt-only audit cannot establish that occurrence."
        ),
    }
    try:
        require(
            pilot.digest(Path(first.__file__)) == continuation.FIRST_SHA
            and pilot.digest(Path(continuation.__file__)) == FINAL_SHA
            and pilot.digest(Path(pilot.__file__)) == first.PILOT_SHA
            and pilot.digest(Path(geometry.__file__)) == pilot.GEOMETRY_SHA
            and pilot.digest(Path(continuation.degenerate.__file__))
            == continuation.DEGENERATE_SHA,
            "first-party source identity differs",
        )
        require(pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive source changed")
        require(
            args.seed_gzip.is_file()
            and args.seed_gzip.stat().st_size == SEED_GZIP_BYTES
            and pilot.digest(args.seed_gzip) == SEED_GZIP_SHA,
            "retained seed object changed",
        )
        seed_bytes = gzip.decompress(args.seed_gzip.read_bytes())
        require(len(seed_bytes) == 27029 and sha(seed_bytes) == pilot.SEED_SHA, "seed decode")
        seed = geometry.strict_json(seed_bytes)
        require(
            seed["mask_index"] == 438 and tuple(seed["mask"]) == pilot.MASK, "seed mask differs"
        )
        require(seed["cover_sha256"] == geometry.COVER_SHA, "seed cover differs")
        groups = {owner: pilot.points(seed["owned_points"][owner]) for owner in range(16)}
        require(sum(len(groups[owner]) for owner in pilot.MASK) == 130, "seed census")
        previous_result_sha: str | None = None
        previous_selected_sha: str | None = None
        rows_total = additions_total = 0
        record: list[dict[str, Any]] = []
        file_hashes: dict[str, str] = {}
        for round_index in range(1, 15):
            selected, selected_bytes = continuation.extract(args.adaptive, round_index)
            selected_sha = sha(selected_bytes)
            rnd = selected["round"]
            require(
                selected["mask_index"] == 438
                and tuple(selected["mask"]) == pilot.MASK
                and selected["cover_sha256"] == geometry.COVER_SHA
                and selected["seed_sha256"] == pilot.SEED_SHA
                and selected.get("branch") is None
                and rnd["index"] == round_index
                and rnd["complete"] is True,
                f"round {round_index} source premises differ",
            )
            prior = first.canonical_groups(groups)
            prior_sha = sha(json.dumps(prior, separators=(",", ":")).encode())
            require(rnd["prior_owned_points"] == prior, f"round {round_index} prior differs")
            directory = args.receipts / f"capture-root-round{round_index}-final"
            result_path = directory / "result.json"
            result_bytes = result_path.read_bytes()
            result_sha = sha(result_bytes)
            file_hashes[str(result_path.relative_to(args.receipts))] = result_sha
            if round_index == 1:
                require(result_sha == FIRST_RESULT_SHA, "first result is not pinned")
            receipt = geometry.strict_json(result_bytes)
            checker_sha = expected_checker(round_index)
            require(
                receipt["status"]
                == (
                    "PASS_ONE_ROOT_ROUND" if round_index == 1 else "PASS_CONDITIONAL_ROOT_ROUND"
                )
                and receipt["round"] == round_index
                and receipt["owners_completed"] == list(pilot.MASK)
                and receipt["checker_sha256"] == checker_sha
                and receipt["pilot_sha256"] == first.PILOT_SHA
                and receipt["geometry_sha256"] == pilot.GEOMETRY_SHA
                and receipt["adaptive_sha256"] == pilot.ADAPTIVE_SHA
                and receipt["seed_sha256"] == pilot.SEED_SHA
                and receipt["cover_sha256"] == geometry.COVER_SHA
                and receipt["selected_round_sha256"] == selected_sha
                and receipt["accepted_prior_sha256"] == prior_sha
                and receipt["root_induction_proved"] is False
                and receipt["candidate_capture_proved"] is False
                and receipt["global_optimality_proved"] is False,
                f"round {round_index} aggregate receipt differs",
            )
            if round_index >= 2:
                require(
                    receipt["previous_result_sha256"] == previous_result_sha
                    and receipt["previous_selected_sha256"] == previous_selected_sha
                    and (
                        round_index <= 7
                        or receipt["degenerate_sha256"] == continuation.DEGENERATE_SHA
                    ),
                    f"round {round_index} previous aggregate binding differs",
                )
            cells = {cell["owner"]: cell for cell in rnd["cells"]}
            require(
                len(rnd["cells"]) == 11 and sorted(cells) == list(pilot.MASK),
                f"round {round_index} owner inventory differs",
            )
            additions = 0
            rows = 0
            for owner in pilot.MASK:
                worker_path = directory / f"owner-{owner:02d}.json"
                worker_bytes = worker_path.read_bytes()
                file_hashes[str(worker_path.relative_to(args.receipts))] = sha(worker_bytes)
                worker = geometry.strict_json(worker_bytes)
                accepted = admit_worker(
                    worker,
                    owner=owner,
                    round_index=round_index,
                    selected_sha=selected_sha,
                    prior_sha=prior_sha,
                    previous_result_sha=previous_result_sha,
                    checker_sha=checker_sha,
                    source_cell=cells[owner],
                )
                rows += len(cells[owner]["rows"])
                for point in accepted:
                    if point not in groups[owner]:
                        groups[owner].append(point)
                        additions += 1
            next_state = first.canonical_groups(groups)
            next_sha = sha(json.dumps(next_state, separators=(",", ":")).encode())
            require(
                additions == rnd["added_owned_vertices"] == receipt["new_owned_points"]
                and receipt["next_state_sha256"] == next_sha
                and selected["next_prior"] == next_state
                and (round_index == 1 or receipt["rows_checked"] == rows),
                f"round {round_index} joined state differs",
            )
            rows_total += rows
            additions_total += additions
            record.append(
                {
                    "round": round_index,
                    "rows": rows,
                    "additions": additions,
                    "result_sha256": result_sha,
                    "selected_sha256": selected_sha,
                    "next_state_sha256": next_sha,
                }
            )
            previous_result_sha = result_sha
            previous_selected_sha = selected_sha
        require(
            rows_total == ROWS_TOTAL and additions_total == ADDITIONS_TOTAL,
            "full root census differs",
        )
        require(
            pilot.digest(args.adaptive) == pilot.ADAPTIVE_SHA, "adaptive changed during audit"
        )
        for name, expected in file_hashes.items():
            require(pilot.digest(args.receipts / name) == expected, f"receipt changed: {name}")
        require(pilot.digest(Path(__file__)) == result["checker_sha256"], "audit code changed")
        result.update(
            status="PASS_ROOT_RECEIPT_CHAIN",
            root_receipt_chain_verified=True,
            rounds=record,
            owner_updates=154,
            rows_checked=rows_total,
            additions=additions_total,
            final_state_sha256=record[-1]["next_state_sha256"],
            receipt_file_sha256=file_hashes,
        )
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result["error"] = str(error)
    result["wall_seconds"] = time.monotonic() - started
    atomic_write_text(args.out, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adaptive", type=Path, required=True)
    parser.add_argument("--seed-gzip", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "owner_updates",
                    "rows_checked",
                    "additions",
                    "wall_seconds",
                    "error",
                )
            }
        )
    )
    return 0 if result["status"] == "PASS_ROOT_RECEIPT_CHAIN" else 2


if __name__ == "__main__":
    raise SystemExit(main())
