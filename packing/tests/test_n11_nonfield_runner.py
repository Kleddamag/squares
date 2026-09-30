"""A complete execution, identity and empty pending inventory are jointly required."""

from __future__ import annotations

import gzip
import hashlib
from pathlib import Path
from typing import Any

import pytest

from devtools.run_n11_nonfield_batch import complete_case, retain_receipt


def test_large_receipt_retains_exact_bytes_in_deterministic_compression(tmp_path: Path) -> None:
    raw = b'{"rows": [' + b"0," * 20_000 + b"0]}\n"
    source = tmp_path / "case.json"
    source.write_bytes(raw)
    retained, fingerprint = retain_receipt(source, raw)
    assert not source.exists()
    packed = retained.read_bytes()
    assert gzip.decompress(packed) == raw
    assert fingerprint == hashlib.sha256(packed).hexdigest()
    assert packed == gzip.compress(raw, mtime=0)


def test_retention_refuses_changed_input_and_existing_destination(tmp_path: Path) -> None:
    source = tmp_path / "case.json"
    raw = b" " * 20_000
    source.write_bytes(raw + b"changed")
    with pytest.raises(ValueError, match="changed before"):
        retain_receipt(source, raw)
    source.write_bytes(raw)
    source.with_suffix(".json.gz").write_bytes(b"prior evidence")
    with pytest.raises(ValueError, match="already exists"):
        retain_receipt(source, raw)
    assert source.read_bytes() == raw


@pytest.mark.parametrize(
    "change",
    [
        {"status": "INCOMPLETE"},
        {"excluded_case_ids": [2095, 2096]},
        {"excluded_case_ids": []},
        {"geometry_verified": False},
        {"global_optimality_proved": True},
        {"current_row": 159},
        {"current_node": "unfinished"},
        {"current_step": 4},
        {"mask_index": 2096},
        {"source_sha256": {"checker": "wrong"}},
    ],
)
def test_partial_or_mismatched_receipt_never_credits_a_case(change: dict[str, Any]) -> None:
    record = {
        "status": "PASS_ONE_GENERIC_EXCLUSION",
        "geometry_verified": True,
        "global_optimality_proved": False,
        "excluded_case_ids": [2095],
        "mask_index": 2095,
        "current_node": None,
        "current_step": None,
        "current_row": None,
        "source_sha256": {"checker": "frozen"},
    }
    assert complete_case(record, 2095, "frozen", 0)
    assert not complete_case(record, 2095, "frozen", 2)
    assert not complete_case({**record, **change}, 2095, "frozen", 0)
