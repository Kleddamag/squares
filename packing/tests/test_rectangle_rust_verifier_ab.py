"""Fast admission controls for the paired exact verifier diagnostic."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from benchmarks import bench_rectangle_rust_verifier_ab as benchmark


def test_normalization_drops_only_binary_metadata() -> None:
    normalize = benchmark._normalized  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    report: dict[str, Any] = {
        "status": "INCONCLUSIVE",
        "angles": [{"index": 1, "nodes": 1000, "unresolved_leaves": 1}],
        "backend": "rust",
        "rust_binary_sha256": "binary",
        "rust_table_sha256": "table",
        "backend_timeout": False,
    }
    normalized = normalize(report)
    assert normalized == {"status": report["status"], "angles": report["angles"]}
    with pytest.raises(ValueError, match="unadmitted backend"):
        normalize({**report, "backend_timeout": True})
    with pytest.raises(ValueError, match="missing backend metadata"):
        normalize({key: value for key, value in report.items() if key != "rust_table_sha256"})


def test_material_rule_requires_complete_pairs_and_separated_cpu_ranges() -> None:
    assess = benchmark._assess  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    rows: list[dict[str, Any]] = []
    for dataset in ("analytic", "external"):
        for pair in range(3):
            rows.extend(
                (
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": "default",
                        "rust_child_cpu_seconds": 10.0 + pair / 100,
                        "invocation_wall_seconds": 20.0 + pair / 100,
                    },
                    {
                        "dataset": dataset,
                        "pair": pair,
                        "arm": "coprime",
                        "rust_child_cpu_seconds": 8.0 + pair / 100,
                        "invocation_wall_seconds": 19.0 + pair / 100,
                    },
                )
            )
    assert assess(rows)["material_bounded_verifier_improvement"] is True
    with pytest.raises(ValueError, match="census is incomplete"):
        assess(rows[:-1])
    duplicated = [dict(row) for row in rows]
    duplicated[-1]["pair"] = 1
    with pytest.raises(ValueError, match="identities are duplicated"):
        assess(duplicated)
    overlapping = [dict(row) for row in rows]
    for row in overlapping:
        if row["dataset"] == "external" and row["arm"] == "coprime":
            row["rust_child_cpu_seconds"] = 9.9 + row["pair"] / 10
    assert assess(overlapping)["material_bounded_verifier_improvement"] is False


def test_prior_coprime_build_must_match_source_toolchain_and_binary(tmp_path: Path) -> None:
    admit = benchmark._admit_coprime_build  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    binary = tmp_path / "coprime"
    binary.write_bytes(b"exact candidate")
    source = str(tmp_path / "source.rs")
    default = {
        "source_sha256": {source: "source-digest"},
        "rustc_version": "same rustc",
        "cargo_version": "same cargo",
        "rustflags": "",
        "cargo_encoded_rustflags": "",
    }
    prior = {
        "source_sha256": {source: "source-digest"},
        "arithmetic_ab": {
            "build": {
                "rustc_version": "same rustc",
                "cargo_version": "same cargo",
                "rustflags": "",
                "cargo_encoded_rustflags": "",
                "builds": [
                    {
                        "feature": "experimental-coprime-mul",
                        "binary_sha256": benchmark._sha(binary),  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
                    }
                ],
            }
        },
    }
    receipt = tmp_path / "prior.json"
    receipt.write_text(json.dumps(prior))
    assert admit(binary, receipt, default) == benchmark._sha(receipt)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    prior["source_sha256"][source] = "wrong-source"
    receipt.write_text(json.dumps(prior))
    with pytest.raises(ValueError, match="different Rust source"):
        admit(binary, receipt, default)
