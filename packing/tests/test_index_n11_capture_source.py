"""Source identity, complete order, and corruption controls for capture indexing."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import pytest

from devtools import index_n11_capture_source as indexed


def source_data() -> dict[str, Any]:
    return {
        "schema": "exact_branch_owned_hull_v1",
        "node_id": "tiny",
        "mask": [0, 1],
        "extra_unselected_field": {"retained": ["a", "b"]},
        "steps": [
            {"index": 0, "owner": 0, "rows": [{"reference": 0}]},
            {"index": 1, "owner": 1, "rows": [{"reference": 1}]},
            {"index": 2, "owner": 0, "rows": [{"reference": 2}]},
        ],
        "final_state": {"cells": {"0": [], "1": []}, "groups": {"0": [], "1": []}},
    }


def write_source(path: Path, data: dict[str, Any]) -> str:
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_complete_index_reconstructs_every_source_field(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    data = source_data()
    sha = write_source(source, data)
    directory = tmp_path / "index"
    reader = indexed.build_and_open(source, directory, expected_sha256=sha, expected_steps=3)
    record = reader.trusted_index
    assert record["proof_accepted"] is False
    assert len(record["steps"]) == 3
    rebuilt = {**reader.header(), "steps": [reader.step(i) for i in range(3)]}
    rebuilt["final_state"] = reader.final_state()
    assert rebuilt == data
    reader.verify_binding()


def test_index_refuses_omission_and_mutated_source_or_stream(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    data = source_data()
    sha = write_source(source, data)
    with pytest.raises(ValueError, match="indexed step order or content differs"):
        indexed.build_index(
            source, tmp_path / "wrong-count", expected_sha256=sha, expected_steps=4
        )
    directory = tmp_path / "index"
    record = indexed.build_index(source, directory, expected_sha256=sha, expected_steps=3)
    stream = directory / "source.jsonl"
    original = stream.read_bytes()
    stream.write_bytes(original.replace(b'"reference":1', b'"reference":9', 1))
    with pytest.raises(ValueError, match="indexed source or derived stream changed"):
        indexed.IndexedSource(
            source, directory, expected_sha256=sha, expected_steps=3, expected_index=record
        )
    stream.write_bytes(original)
    data["extra_unselected_field"]["retained"].append("c")
    write_source(source, data)
    with pytest.raises(ValueError, match="capture index identity differs"):
        indexed.IndexedSource(
            source, directory, expected_sha256=sha, expected_steps=3, expected_index=record
        )


def test_index_refuses_changed_offsets_and_record_sha(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    sha = write_source(source, source_data())
    directory = tmp_path / "index"
    trusted = indexed.build_index(source, directory, expected_sha256=sha, expected_steps=3)
    metadata = directory / "index.json"
    record = json.loads(metadata.read_text())
    record["steps"][1]["offset"] += 1
    metadata.write_text(json.dumps(record))
    with pytest.raises(ValueError, match="capture index identity differs"):
        indexed.IndexedSource(
            source, directory, expected_sha256=sha, expected_steps=3, expected_index=trusted
        )
    metadata.write_text(json.dumps(trusted))
    reader = indexed.IndexedSource(
        source, directory, expected_sha256=sha, expected_steps=3, expected_index=trusted
    )
    stream = directory / "source.jsonl"
    stream.write_bytes(stream.read_bytes().replace(b'"reference":1', b'"reference":9', 1))
    with pytest.raises(ValueError, match="indexed record changed"):
        reader.step(1)


def test_rewritten_stream_and_self_described_index_cannot_rebind_source(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    sha = write_source(source, source_data())
    directory = tmp_path / "index"
    trusted = indexed.build_index(source, directory, expected_sha256=sha, expected_steps=3)
    stream = directory / "source.jsonl"
    lines = stream.read_bytes().splitlines(keepends=True)
    lines[2] = lines[2].replace(b'"reference":1', b'"reference":9', 1)
    stream.write_bytes(b"".join(lines))
    forged = json.loads(json.dumps(trusted))
    forged["steps"][1]["sha256"] = hashlib.sha256(lines[2]).hexdigest()
    forged["stream_sha256"] = indexed.digest(stream)
    (directory / "index.json").write_text(json.dumps(forged))
    with pytest.raises(ValueError, match="capture index identity differs"):
        indexed.IndexedSource(
            source, directory, expected_sha256=sha, expected_steps=3, expected_index=trusted
        )


def test_index_refuses_unbounded_or_overwriting_output(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    sha = write_source(source, source_data())
    with pytest.raises(ValueError, match="positive bounded"):
        indexed.build_index(
            source,
            tmp_path / "index",
            expected_sha256=sha,
            expected_steps=3,
            max_seconds=math.inf,
        )
    colliding = tmp_path / "source.jsonl"
    colliding_sha = write_source(colliding, source_data())
    with pytest.raises(ValueError, match="overwrite source"):
        indexed.build_index(
            colliding, tmp_path, expected_sha256=colliding_sha, expected_steps=3
        )
