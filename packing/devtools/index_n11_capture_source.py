"""Index a pinned capture source in one jq parse without trusting its proof claims.

The JSONL and offset index are disposable derived data. A consumer must pin the
original source SHA and call ``IndexedSource.verify_binding`` before and after
using records. Every source field is retained in the header, ordered steps, or
final-state record; this module grants no geometric or ancestry acceptance.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from strif import atomic_write_text

QUERY = (
    ". as $source | "
    '({kind:"header",value:($source | del(.steps,.final_state))}, '
    '($source.steps | to_entries[] | {kind:"step",index:.key,value:.value}), '
    '{kind:"final",value:$source.final_state})'
)
SCHEMA = "capture_source_index_v1"


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def strict_json(data: bytes) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, "duplicate indexed JSON key")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=pairs)


def _entry(offset: int, raw: bytes) -> dict[str, Any]:
    return {"offset": offset, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def _scan(stream_path: Path, expected_steps: int) -> tuple[dict[str, Any], str]:
    hasher = hashlib.sha256()
    entries: list[dict[str, Any]] = []
    with stream_path.open("rb") as stream:
        while raw := stream.readline():
            offset = stream.tell() - len(raw)
            require(raw.endswith(b"\n"), "unterminated indexed record")
            record = strict_json(raw)
            require(isinstance(record, dict), "indexed record must be an object")
            position = len(entries)
            if position == 0:
                require(
                    record.get("kind") == "header"
                    and set(record) == {"kind", "value"}
                    and isinstance(record["value"], dict)
                    and "steps" not in record["value"]
                    and "final_state" not in record["value"],
                    "indexed header differs",
                )
            elif position <= expected_steps:
                require(
                    record.get("kind") == "step"
                    and set(record) == {"kind", "index", "value"}
                    and type(record["index"]) is int
                    and record["index"] == position - 1
                    and isinstance(record["value"], dict),
                    "indexed step order or content differs",
                )
            else:
                require(
                    position == expected_steps + 1
                    and record.get("kind") == "final"
                    and set(record) == {"kind", "value"}
                    and isinstance(record["value"], dict),
                    "indexed final record differs",
                )
            hasher.update(raw)
            entries.append(_entry(offset, raw))
    require(len(entries) == expected_steps + 2, "indexed source record count differs")
    require(stream_path.stat().st_size == sum(item["bytes"] for item in entries), "index gaps")
    return {
        "header": entries[0],
        "steps": entries[1:-1],
        "final": entries[-1],
    }, hasher.hexdigest()


def build_index(
    source: Path,
    directory: Path,
    *,
    expected_sha256: str,
    expected_steps: int,
    max_seconds: float = 60,
) -> dict[str, Any]:
    """Create a disposable complete index only from the exact pinned source."""

    require(
        expected_steps >= 1 and math.isfinite(max_seconds) and max_seconds > 0,
        "positive bounded index parameters",
    )
    require(source.is_file(), "capture source missing")
    require(
        source.resolve()
        not in {(directory / "source.jsonl").resolve(), (directory / "index.json").resolve()},
        "index output would overwrite source",
    )
    started = time.monotonic()
    require(digest(source) == expected_sha256, "capture source SHA differs before indexing")
    directory.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix="capture-index-", suffix=".jsonl", dir=directory)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as output:
            jq_started = time.monotonic()
            completed = subprocess.run(
                ["jq", "-c", QUERY, str(source)],
                stdout=output,
                stderr=subprocess.PIPE,
                check=False,
                timeout=max_seconds,
            )
            jq_seconds = time.monotonic() - jq_started
        require(completed.returncode == 0, "jq index extraction failed")
        scan_started = time.monotonic()
        entries, stream_sha256 = _scan(temporary_path, expected_steps)
        scan_seconds = time.monotonic() - scan_started
        require(digest(source) == expected_sha256, "capture source changed during indexing")
        require(time.monotonic() - started <= max_seconds, "index deadline exceeded")
        stream_path = directory / "source.jsonl"
        temporary_path.replace(stream_path)
        index = {
            "schema": SCHEMA,
            "source_sha256": expected_sha256,
            "source_bytes": source.stat().st_size,
            "stream_sha256": stream_sha256,
            "stream_bytes": stream_path.stat().st_size,
            "expected_steps": expected_steps,
            **entries,
            "timing": {
                "jq_wall_seconds": jq_seconds,
                "scan_wall_seconds": scan_seconds,
                "total_wall_seconds": time.monotonic() - started,
            },
            "proof_accepted": False,
        }
        atomic_write_text(directory / "index.json", json.dumps(index, indent=2) + "\n")
        return index
    finally:
        temporary_path.unlink(missing_ok=True)


class IndexedSource:
    """Read records only against an index returned by a fresh build_index call."""

    def __init__(
        self,
        source: Path,
        directory: Path,
        *,
        expected_sha256: str,
        expected_steps: int,
        expected_index: dict[str, Any],
    ) -> None:
        self.source = source
        self.stream = directory / "source.jsonl"
        self.index_path = directory / "index.json"
        self.trusted_index = copy.deepcopy(expected_index)
        self.index = strict_json((directory / "index.json").read_bytes())
        require(isinstance(self.index, dict), "capture index metadata must be an object")
        require(
            self.index == self.trusted_index
            and self.index.get("schema") == SCHEMA
            and self.index.get("source_sha256") == expected_sha256
            and self.index.get("expected_steps") == expected_steps
            and len(self.index.get("steps", [])) == expected_steps
            and self.index.get("source_bytes") == source.stat().st_size
            and self.index.get("stream_bytes") == self.stream.stat().st_size,
            "capture index identity differs",
        )
        self.verify_binding()
        entries = [self.index["header"], *self.index["steps"], self.index["final"]]
        cursor = 0
        for entry in entries:
            require(entry["offset"] == cursor and entry["bytes"] > 0, "capture index gap")
            cursor += entry["bytes"]
        require(cursor == self.index["stream_bytes"], "capture index trailing data")

    def verify_binding(self) -> None:
        require(
            strict_json(self.index_path.read_bytes()) == self.trusted_index
            and digest(self.source) == self.trusted_index["source_sha256"]
            and digest(self.stream) == self.trusted_index["stream_sha256"],
            "indexed source or derived stream changed",
        )

    def _read(self, entry: dict[str, Any], kind: str, index: int | None = None) -> Any:
        with self.stream.open("rb") as stream:
            stream.seek(entry["offset"])
            raw = stream.read(entry["bytes"])
        require(hashlib.sha256(raw).hexdigest() == entry["sha256"], "indexed record changed")
        record = strict_json(raw)
        require(
            isinstance(record, dict)
            and record.get("kind") == kind
            and (index is None or record.get("index") == index),
            "indexed record identity differs",
        )
        return record["value"]

    def header(self) -> dict[str, Any]:
        return self._read(self.index["header"], "header")

    def step(self, index: int) -> dict[str, Any]:
        require(0 <= index < self.index["expected_steps"], "indexed step out of range")
        return self._read(self.index["steps"][index], "step", index)

    def final_state(self) -> dict[str, Any]:
        return self._read(self.index["final"], "final")


def build_and_open(
    source: Path,
    directory: Path,
    *,
    expected_sha256: str,
    expected_steps: int,
    max_seconds: float = 60,
) -> IndexedSource:
    """Freshly derive and bind an index in the same process that will consume it."""

    trusted = build_index(
        source,
        directory,
        expected_sha256=expected_sha256,
        expected_steps=expected_steps,
        max_seconds=max_seconds,
    )
    return IndexedSource(
        source,
        directory,
        expected_sha256=expected_sha256,
        expected_steps=expected_steps,
        expected_index=trusted,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--expected-steps", type=int, required=True)
    parser.add_argument("--max-seconds", type=float, default=60)
    args = parser.parse_args()
    index = build_index(
        args.source,
        args.directory,
        expected_sha256=args.expected_sha256,
        expected_steps=args.expected_steps,
        max_seconds=args.max_seconds,
    )
    print(
        json.dumps(
            {
                key: index[key]
                for key in (
                    "schema",
                    "source_sha256",
                    "stream_sha256",
                    "expected_steps",
                    "timing",
                    "proof_accepted",
                )
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
