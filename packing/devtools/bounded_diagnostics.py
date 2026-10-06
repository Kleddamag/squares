"""Shared resource guards, retained JSON IO and diagnostic input provenance.

Lifetime peak is a reporting statistic; only current RSS enforces the live worker
limit. Committed evidence is located by Git revision/path and compared as JSON,
while external saved objects retain their semantic seed/node digests.
"""

from __future__ import annotations

import gzip
import json
import time
from pathlib import Path
from typing import Any

from devtools.process_memory import current_memory_bytes
from sqpack.hull_kernel.geometry import Budget, IncompleteError, require
from sqpack.retained_json import dumps

MAX_PACKET_BYTES = 4 * 1024**2
MAX_MEMORY_BYTES = 512 * 1024**2
REPO_ROOT = Path(__file__).resolve().parents[2]
BOOKKEEPING_FIELDS = {
    "packet_sha256",
    "profile_packet_sha256",
    "seed_packet_sha256",
    "source_packet_sha256",
    "baseline_replay_sha256",
    "H_packet_sha256",
    "E_packet_sha256",
    "J_certificate_sha256",
    "A_packet_sha256",
    "A_replay_sha256",
    "B_packet_sha256",
    "D_packet_sha256",
    "D_replay_sha256",
    "artifact_provenance",
    "baseline_revision",
    "baseline_repository_revision",
    "derived_inventory_sha256",
    "full_inventory_sha256",
    "mixed_inventory_sha256",
}


def check_budget(budget: Budget, *, wall_message: str) -> None:
    """Fail before or after work without using a process's historical high-water mark."""
    if time.monotonic() >= budget.deadline:
        raise IncompleteError(wall_message)
    if current_memory_bytes() > MAX_MEMORY_BYTES:
        raise IncompleteError("actual worker current RSS exceeds 512 MiB")


def read_json(
    path: Path, *, limit: int = MAX_PACKET_BYTES, compressed: bool = False
) -> dict[str, Any]:
    opener = gzip.open if compressed else Path.open
    with opener(path, "rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, f"JSON input exceeds {limit // 1024**2} MiB byte limit")
    value = json.loads(raw)
    require(isinstance(value, dict), "packet/receipt must be a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    """Write exactly the bounded LF bytes, keeping an existing destination on refusal."""
    serialized = dumps(value).encode("utf-8")
    require(len(serialized) <= MAX_PACKET_BYTES, "output packet exceeds 4 MiB")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(serialized)
    temporary.replace(path)


def input_identity(value: Any) -> dict[str, str]:
    """Project legacy receipt bookkeeping away without weakening object identity."""
    require(isinstance(value, dict), "input identity must be an object")
    result = {}
    for key in ("seed_sha256", "node_sha256"):
        digest = value.get(key)
        require(
            isinstance(digest, str) and bool(digest), f"input identity differs: missing {key}"
        )
        result[key] = digest
    return result


def same_inputs(left: Any, right: Any) -> bool:
    return input_identity(left) == input_identity(right)


def scientific_view(value: dict[str, Any]) -> dict[str, Any]:
    """Normalize only legacy input receipt metadata, preserving the original packet."""
    return {**value, "input_identity": input_identity(value["input_identity"])}


def same_header(value: dict[str, Any], expected: dict[str, Any]) -> bool:
    for key, item in expected.items():
        if key in BOOKKEEPING_FIELDS:
            continue
        if key == "input_identity":
            if not same_inputs(value.get(key), item):
                return False
        elif key == "limits":
            if not same_content(resource_limits(value.get(key)), resource_limits(item)):
                return False
        elif not same_content(value.get(key), item):
            return False
    return True


def resource_limits(value: Any) -> dict[str, Any]:
    """Read the old limit label without relabelling retained peak measurements."""
    require(isinstance(value, dict), "resource limits must be an object")
    result = dict(value)
    if "worker_peak_bytes" in result:
        result.setdefault("worker_current_rss_bytes", result.pop("worker_peak_bytes"))
    return result


def retained_json(path: str) -> dict[str, Any]:
    """Read the committed fixture path; historical Git objects are not a runtime dependency."""
    target = (REPO_ROOT / path).resolve()
    require(
        path.startswith("packing/") and target.is_relative_to(REPO_ROOT),
        "invalid artifact path",
    )
    return read_json(target)


def same_content(left: Any, right: Any) -> bool:
    """Type-aware JSON equality, excluding only historical provenance bookkeeping."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        left_keys = left.keys() - BOOKKEEPING_FIELDS
        right_keys = right.keys() - BOOKKEEPING_FIELDS
        return left_keys == right_keys and all(
            same_inputs(left[key], right[key])
            if key == "input_identity"
            else same_content(resource_limits(left[key]), resource_limits(right[key]))
            if key == "limits"
            else same_content(left[key], right[key])
            for key in left_keys
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            same_content(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def retained_matches(value: dict[str, Any], revision: str, path: str) -> bool:
    """Compare fixture content; the revision is informational provenance, never a pin."""
    del revision
    return same_content(value, retained_json(path))
