"""Bounded source intake refuses identity and length changes before reuse."""

from __future__ import annotations

import gzip
from pathlib import Path
from typing import Any

import pytest

from devtools.prepare_n11_nonfield_batch import checked_bytes, digest


def test_reused_object_requires_both_byte_identities(tmp_path: Path) -> None:
    raw = b'{"source":"proposal"}\n'
    packed = gzip.compress(raw, mtime=0)
    path = tmp_path / "source.gz"
    path.write_bytes(packed)
    pin: dict[str, Any] = {
        "compressed_bytes": len(packed),
        "compressed_sha256": digest(packed),
        "decoded_bytes": len(raw),
        "decoded_sha256": digest(raw),
    }
    assert checked_bytes(path, pin) == packed
    for key, replacement in (
        ("compressed_bytes", len(packed) - 1),
        ("compressed_sha256", "0" * 64),
        ("decoded_bytes", len(raw) - 1),
        ("decoded_bytes", len(raw) + 1),
        ("decoded_sha256", "0" * 64),
    ):
        with pytest.raises(ValueError, match="differs"):
            checked_bytes(path, {**pin, key: replacement})


def test_concatenated_gzip_cannot_hide_trailing_decoded_data(tmp_path: Path) -> None:
    first, second = b"first", b"second"
    packed = gzip.compress(first, mtime=0) + gzip.compress(second, mtime=0)
    path = tmp_path / "source.gz"
    path.write_bytes(packed)
    with pytest.raises(ValueError, match="decoded length differs"):
        checked_bytes(
            path,
            {
                "compressed_bytes": len(packed),
                "compressed_sha256": digest(packed),
                "decoded_bytes": len(first),
                "decoded_sha256": digest(first),
            },
        )
