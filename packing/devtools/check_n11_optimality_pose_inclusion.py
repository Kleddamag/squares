"""Check the conditional inclusion of the case-438 source poses in the fixed-T box.

The pinned source pose domains are premises. This checker validates their complete
closed-row inventory and their inclusion, without certifying their ancestry or the
global packing claim.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11 import packing

Q = Fraction
MASK = [0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15]
U = Q(387708359002281417731, 10**20)
B = Q(191, 50) / U
SOURCE_SHA = "491afdaaf411e7fdb4968bdcda7232ea517ead34739d0ae8c7d5570333a981cc"
GUARD_SHA = "0bc2edf59cbf620258719db7ba50cdf77af749d38dfbef76a131d32353443fb0"
FOCUSED_SHA = "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3"
LOCAL_RESULT_SHA = "a98623f57017b4f04c8d3a72083caa7d4a6fb5096a79ab1e4dbbf2cd9b35a29d"
LOCAL_CHECKER_SHA = "4e64b3de55e1dafec6f8f976aaa6395218801d6c7111f8f5e22cdf2bb99b6ccc"
SOURCE_SIZE = 185901535
GUARD_SIZE = 37904
LIVE_ROWS = 136
VERTICES = 1542

# jq parses the large pinned JSON and emits only the complete live-row inventory.
# Every omitted source row is counted; the full source digest is checked first.
EXTRACT = """
{
  mask_index, mask, U, B,
  constraints_match: (.constraints == .final_state.constraints),
  final_state: {
    mask: .final_state.mask,
    U: .final_state.U,
    B: .final_state.B,
    source: .final_state.source,
    guard_source: .final_state.guard_source,
    cells: (.final_state.cells | with_entries(
      .value |= {
        row_count: length,
        missing_polygon_fields: (map(select(has("residual_polygons") | not)) | length),
        live_rows: map(select(.residual_polygons | length > 0) | {interval, residual_polygons})
      }
    ))
  }
}
"""


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    hash_value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()


def root_interval() -> tuple[Q, Q, int]:
    def polynomial(value: Q) -> Q:
        result = Q(0)
        for coefficient in packing.U_MIN_POLY:
            result = result * value + coefficient
        return result

    lo, hi = Q(9, 25), Q(37, 100)
    require(polynomial(lo) < 0 < polynomial(hi), "Trump root bracket failed")
    derivative_lower = (
        40 * lo**7 + 70 * lo**4 + 48 * lo**3 + 4 * lo + 2 - 70 * hi**6 - 12 * hi**5 - 18 * hi**2
    )
    require(derivative_lower > 0, "Trump root uniqueness bound failed")
    count = 0
    while hi - lo > Q(1, 10**80):
        mid = (lo + hi) / 2
        if polynomial(mid) < 0:
            lo = mid
        else:
            hi = mid
        count += 1
    return lo, hi, count


def field_interval(value: Any, lo: Q, hi: Q) -> tuple[Q, Q]:
    lower = upper = Q(0)
    for degree, coefficient in enumerate(value.coeffs):
        first, second = coefficient * lo**degree, coefficient * hi**degree
        lower += min(first, second)
        upper += max(first, second)
    return lower, upper


def axis_angle_bound(lo: Q, hi: Q) -> Q:
    require(0 <= lo <= hi <= 1, "invalid closed half-angle interval")
    require(hi <= Q(1, 2) or lo >= Q(1, 2), "axis interval crosses remote chart")
    if hi <= Q(1, 2):
        return 2 * hi
    return 2 * (1 - lo) / (1 + lo)


def slanted_angle_bound(lo: Q, hi: Q, root_lo: Q, root_hi: Q) -> Q:
    require(0 <= lo <= hi < Q(2, 3), "slanted interval crosses quarter-turn cut")
    return 2 * max(abs(lo - root_hi), abs(hi - root_lo)) / (1 + min(lo, root_lo) ** 2)


def inverse_center(vertex: list[str], scale: Q, cap: Q) -> tuple[Q, Q]:
    require(len(vertex) == 2, "residual vertex must have two coordinates")
    x_field, y_field = map(Q, vertex)
    return y_field / scale - cap / 2, cap / 2 - x_field / scale


def required_center_radius(center: Q, witness_bound: tuple[Q, Q]) -> Q:
    return max(abs(center - witness_bound[0]), abs(center - witness_bound[1]))


def extract_source(path: Path, remaining_seconds: float) -> tuple[dict[str, Any], bytes]:
    require(
        path.stat().st_size == SOURCE_SIZE and digest(path) == SOURCE_SHA,
        "pose source identity mismatch",
    )
    require(remaining_seconds > 0, "pose extraction budget expired")
    process = subprocess.run(
        ["jq", "-c", EXTRACT, str(path)],
        capture_output=True,
        check=False,
        timeout=remaining_seconds,
    )
    require(
        process.returncode == 0, f"pose JSON extraction failed: {process.stderr.decode()[:200]}"
    )
    extracted = json.loads(process.stdout)
    return extracted, process.stdout


def check_inventory(
    data: dict[str, Any], guard_data: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = data["final_state"]
    require(data["mask_index"] == 438, "wrong source mask index")
    require(data["mask"] == state["mask"] == MASK, "source mask mismatch")
    require(data["constraints_match"] is True, "top and final constraints differ")
    require(Q(data["U"]) == Q(state["U"]) == U, "wrong source cap")
    require(Q(data["B"]) == Q(state["B"]) == B, "wrong source field scale")
    require(state["guard_source"]["sha256"] == GUARD_SHA, "source guard reference differs")
    guards = [entry for entry in guard_data["guards"] if entry["mask"] == MASK]
    require(len(guards) == 1, "mask 438 must have exactly one role guard")
    guard = guards[0]
    require(
        guard["symmetry"] == {"swap": True, "reflect_x": True, "reflect_y": False},
        "wrong quarter-turn symmetry",
    )
    roles = guard["roles"]
    require(len(roles) == 11, "role count mismatch")
    require(
        sorted(role["label"] for role in roles) == list(range(11)),
        "role labels are not bijective",
    )
    require(sorted(role["cell"] for role in roles) == MASK, "role owners are not bijective")
    require(
        guard["label_to_cell"]
        == [next(role["cell"] for role in roles if role["label"] == i) for i in range(11)],
        "role lookup disagrees with roles",
    )
    require(set(state["cells"]) == set(map(str, MASK)), "source owner inventory is incomplete")
    return roles, state["cells"]


def check_pose(
    data: dict[str, Any],
    guard_data: dict[str, Any],
    radii: list[Q],
    root_lo: Q,
    root_hi: Q,
) -> dict[str, Any]:
    roles, cells = check_inventory(data, guard_data)
    require(
        len(radii) == 33 and all(0 < radius <= Q(1, 64) for radius in radii),
        "invalid local radii",
    )
    squares, side, field = packing.build()
    require(len(squares) == 11, "witness square count mismatch")
    side_lo, side_hi = field_interval(side, root_lo, root_hi)
    require(0 < side_lo <= side_hi < U, "Trump side is not below source cap")
    alpha, one = field.alpha, field.one
    cosine = (one - alpha * alpha) / (one + alpha * alpha)
    sine = 2 * alpha / (one + alpha * alpha)
    per_owner: list[dict[str, Any]] = []
    rows_checked = vertices_checked = singleton_polygons = segment_polygons = 0
    saw_zero = saw_one = False
    for role in sorted(roles, key=lambda entry: entry["label"]):
        label, owner = role["label"], role["cell"]
        cell = cells[str(owner)]
        rows = cell["live_rows"]
        require(cell["row_count"] >= len(rows) > 0, "empty or impossible source owner")
        require(cell["missing_polygon_fields"] == 0, "source row lacks polygon field")
        edge = (
            squares[label][1][0] - squares[label][0][0],
            squares[label][1][1] - squares[label][0][1],
        )
        expected = (one, field.zero) if label < 6 else (cosine, sine)
        require(
            all(
                (actual - target).is_zero()
                for actual, target in zip(edge, expected, strict=True)
            ),
            "witness orientation mismatch",
        )
        center = tuple(
            (squares[label][0][k] + squares[label][2][k]) / 2 - side / 2 for k in (0, 1)
        )
        center_bounds = [field_interval(value, root_lo, root_hi) for value in center]
        required = [Q(0), Q(0), Q(0)]
        owner_vertices = 0
        for row in rows:
            require(len(row["interval"]) == 2, "row interval must have two endpoints")
            angle_lo, angle_hi = map(Q, row["interval"])
            required[2] = max(
                required[2],
                axis_angle_bound(angle_lo, angle_hi)
                if label < 6
                else slanted_angle_bound(angle_lo, angle_hi, root_lo, root_hi),
            )
            saw_zero |= angle_lo == 0
            saw_one |= angle_hi == 1
            for polygon in row["residual_polygons"]:
                require(polygon, "empty residual polygon")
                singleton_polygons += len(polygon) == 1
                segment_polygons += len(polygon) == 2
                for vertex in polygon:
                    transformed = inverse_center(vertex, B, U)
                    for coordinate in (0, 1):
                        required[coordinate] = max(
                            required[coordinate],
                            required_center_radius(
                                transformed[coordinate], center_bounds[coordinate]
                            ),
                        )
                    owner_vertices += 1
        require(
            all(required[k] <= radii[3 * label + k] for k in range(3)),
            "pose domain exceeds accepted rectangle",
        )
        rows_checked += len(rows)
        vertices_checked += owner_vertices
        per_owner.append(
            {
                "label": label,
                "owner": owner,
                "source_rows": cell["row_count"],
                "live_rows": len(rows),
                "vertices": owner_vertices,
                "required_radii": list(map(str, required)),
                "accepted_radii": list(map(str, radii[3 * label : 3 * label + 3])),
                "slack": [str(radii[3 * label + k] - required[k]) for k in range(3)],
            }
        )
    require(
        rows_checked == LIVE_ROWS and vertices_checked == VERTICES, "live pose census mismatch"
    )
    require(saw_zero and saw_one, "closed chart endpoint inventory incomplete")
    return {
        "owners": per_owner,
        "live_rows_checked": rows_checked,
        "vertices_checked": vertices_checked,
        "singleton_polygons_checked": singleton_polygons,
        "segment_polygons_checked": segment_polygons,
        "zero_endpoint_observed": saw_zero,
        "one_endpoint_observed": saw_one,
        "root_interval": [str(root_lo), str(root_hi)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, required=True, help="Decoded pinned near-refined1024-240 JSON"
    )
    parser.add_argument(
        "--guards", type=Path, required=True, help="Decoded pinned role-guard JSON"
    )
    parser.add_argument(
        "--focused", type=Path, required=True, help="Pinned focused local data JSON or .gz"
    )
    parser.add_argument(
        "--local-result", type=Path, required=True, help="Accepted fixed-T local result"
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--derived-output",
        type=Path,
        required=True,
        help="Complete compact live-row extraction (.gz)",
    )
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()
    require(0 < args.max_seconds <= 60, "bounded positive runtime ceiling required")
    start_wall, start_cpu = time.monotonic(), time.process_time()
    deadline = start_wall + args.max_seconds
    phases: dict[str, dict[str, float]] = {}

    def phase(name: str, started_wall: float, started_cpu: float) -> None:
        phases[name] = {
            "wall_seconds": time.monotonic() - started_wall,
            "process_cpu_seconds": time.process_time() - started_cpu,
        }
        require(time.monotonic() < deadline, f"runtime ceiling expired after {name}")

    tick_wall, tick_cpu = time.monotonic(), time.process_time()
    guard_bytes = args.guards.read_bytes()
    require(
        len(guard_bytes) == GUARD_SIZE and hashlib.sha256(guard_bytes).hexdigest() == GUARD_SHA,
        "guard identity mismatch",
    )
    guard_data = json.loads(guard_bytes)
    focused_bytes = (
        gzip.decompress(args.focused.read_bytes())
        if args.focused.suffix == ".gz"
        else args.focused.read_bytes()
    )
    require(
        hashlib.sha256(focused_bytes).hexdigest() == FOCUSED_SHA,
        "focused radii identity mismatch",
    )
    focused = json.loads(focused_bytes)
    radii = [Q(value) for value in focused["radii"]]
    local_bytes = args.local_result.read_bytes()
    require(
        hashlib.sha256(local_bytes).hexdigest() == LOCAL_RESULT_SHA,
        "accepted local result identity mismatch",
    )
    local = json.loads(local_bytes)
    require(
        local["status"] == "PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION"
        and local["fixed_T_local_isolation_proved"] is True,
        "local premise is not accepted",
    )
    require(
        local["checker_sha256"] == LOCAL_CHECKER_SHA
        and local["input_sha256"]["focused"] == FOCUSED_SHA,
        "local premise source mismatch",
    )
    require(
        local["pose_inclusion_proved"] is False and local["global_optimality_proved"] is False,
        "local result scope mismatch",
    )
    repo_packing = Path(__file__).resolve().parents[1]
    for relative, expected_sha in local["source_hashes"].items():
        require(
            digest(repo_packing / relative) == expected_sha,
            f"exact witness source changed: {relative}",
        )
    root_lo, root_hi, _ = root_interval()
    require(
        local["root_interval"] == [str(root_lo), str(root_hi)],
        "independent root enclosure differs from local premise",
    )
    phase("admission_and_root", tick_wall, tick_cpu)

    tick_wall, tick_cpu = time.monotonic(), time.process_time()
    data, extracted = extract_source(args.source, deadline - time.monotonic())
    phase("source_hash_and_extraction", tick_wall, tick_cpu)

    tick_wall, tick_cpu = time.monotonic(), time.process_time()
    checked = check_pose(data, guard_data, radii, root_lo, root_hi)
    phase("pose_inclusion", tick_wall, tick_cpu)

    require(time.monotonic() < deadline, "runtime ceiling expired before reporting")
    compressed = gzip.compress(extracted, mtime=0)
    result = {
        "status": "PASS_POSE_INCLUSION",
        "conditional_on_source_pose_domains": True,
        "pose_inclusion_proved": True,
        "source_geometry_ancestry_proved": False,
        "case_438_capture_proved": False,
        "global_optimality_proved": False,
        "scope": (
            "Every live closed pose domain in the pinned case-438 final state fits "
            "the independently accepted fixed-T local rectangle, conditional on "
            "those source domains."
        ),
        "source_pin": "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c",
        "source_sha256": SOURCE_SHA,
        "guard_sha256": GUARD_SHA,
        "focused_sha256": FOCUSED_SHA,
        "accepted_local_result_sha256": LOCAL_RESULT_SHA,
        "checker_sha256": digest(Path(__file__)),
        "derived_state_sha256": hashlib.sha256(extracted).hexdigest(),
        "derived_state_gzip_sha256": hashlib.sha256(compressed).hexdigest(),
        "derived_state_gzip_bytes": len(compressed),
        "source_frame": {"U": str(U), "B": str(B), "inverse": "(yf/B-U/2,U/2-xf/B)"},
        **checked,
        "phases": phases,
        "wall_seconds": time.monotonic() - start_wall,
        "process_cpu_seconds": time.process_time() - start_cpu,
        "max_seconds": args.max_seconds,
    }
    args.derived_output.write_bytes(compressed)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
