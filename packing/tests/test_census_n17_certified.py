"""Controls for the n17 certified census: what it refuses and what it counts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools.census_n17_certified import (
    BB_CERTIFIED,
    BB_SCHEMA,
    CENSUS,
    DESIGN,
    KERNEL_FRAME,
    LEDGER_SCHEMA,
    RefusedError,
    census,
    cover_context,
)

W7 = ["corner-SW", "side-N0", "side-W0", "side-W1", "side-W2", "interior-SW", "interior-W"]
A = ["interior-SW", "interior-NW", "interior-W", "interior-S", "interior-N", "interior-SE"]


def write_json(root: Path, name: str, document: dict[str, Any]) -> tuple[str, str]:
    """A fabricated receipt under the root: its relative path and its digest."""
    path = root / "receipts" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return f"receipts/{name}", hashlib.sha256(path.read_bytes()).hexdigest()


def kernel_receipt(cells: list[str]) -> dict[str, Any]:
    return {"status": "PASS_SAVED_CLOSED", "cells": cells, "frame": KERNEL_FRAME}


def bb_receipt(cells: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "schema": BB_SCHEMA,
        "design": DESIGN,
        "pattern": cells,
        "verdict": BB_CERTIFIED,
        "control": False,
        **extra,
    }


def entry(
    name: str, cells: list[str], receipt: tuple[str, str], **fields: Any
) -> dict[str, Any]:
    return {
        "name": name,
        "cells": cells,
        "certifier": "kernel",
        "receipt": receipt[0],
        "receipt_sha256": receipt[1],
        "certificate": None,
        "status": "pending",
        "evidence": None,
        **fields,
    }


def run_census(root: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    ledger = root / "ledger.yaml"
    document = {"schema": LEDGER_SCHEMA, "design": DESIGN, "entries": entries}
    _ = ledger.write_text(json.dumps(document), encoding="utf-8")  # JSON is YAML
    return census(ledger, root=root, selector_receipts=())


def image_names(cells: list[str], element: int) -> list[str]:
    """The cell names of one D4 image of a pattern."""
    geometry = cover_context().geometry
    permutation = geometry.group[element]
    return [geometry.names[permutation[geometry.names.index(name)]] for name in cells]


def test_an_empty_ledger_reproduces_the_h266_census(tmp_path: Path) -> None:
    record = run_census(tmp_path, [])
    assert record["census"]["surviving_states"] == CENSUS["states"] == 346104
    assert record["census"]["orbits"] == CENSUS["orbits"] == 43593
    for line in ("certified", "pending_verified_projection", "pending_all_projection"):
        assert record[line]["surviving_states"] == 346104
        assert record[line]["orbits"] == 43593
        assert record[line]["endpoint_survives"]


def test_a_receipt_with_the_wrong_digest_is_refused(tmp_path: Path) -> None:
    path, _ = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    with pytest.raises(RefusedError, match="digest"):
        _ = run_census(tmp_path, [entry("W7", W7, (path, "0" * 64))])


def test_cells_that_disagree_with_the_receipt_are_refused(tmp_path: Path) -> None:
    receipt = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    other = [*W7[:-1], "interior-NW"]
    with pytest.raises(RefusedError, match="another class"):
        _ = run_census(tmp_path, [entry("W7", other, receipt)])
    # The comparison is by D4 class: an image of the receipt's cells is the same claim.
    turned = run_census(tmp_path, [entry("W7", image_names(W7, 1), receipt)])
    assert turned["entries"][0]["verified"]


def test_an_entry_excluding_the_endpoint_state_is_refused(tmp_path: Path) -> None:
    context = cover_context()
    inside = [
        name for k, name in enumerate(context.geometry.names) if context.endpoint_state >> k & 1
    ]
    cells = inside[:3]
    receipt = write_json(tmp_path, "endpoint.json", kernel_receipt(cells))
    with pytest.raises(RefusedError, match="endpoint"):
        _ = run_census(tmp_path, [entry("E", cells, receipt)])


def test_only_admitted_entries_are_counted(tmp_path: Path) -> None:
    w7 = write_json(tmp_path, "w7.json", kernel_receipt(W7))
    a = write_json(tmp_path, "a.json", bb_receipt(A))
    review = tmp_path / "review.md"
    _ = review.write_text("admits W7\n", encoding="utf-8")
    entries = [
        entry("W7", W7, w7, status="admitted", evidence="review.md"),
        entry("A", A, a, certifier="branch-and-bound"),
    ]
    record = run_census(tmp_path, entries)
    # W7 excludes 133,152 states in 16,701 orbits, as its kernel receipt says.
    assert record["certified"]["surviving_states"] == 346104 - 133152
    assert record["certified"]["orbits"] == 43593 - 16701
    assert record["entries"][0]["marginal"] == record["entries"][0]["alone"]
    both = record["pending_verified_projection"]
    assert both["surviving_states"] < record["certified"]["surviving_states"]
    assert both["surviving_states"] == (
        record["certified"]["surviving_states"] - record["entries"][1]["marginal"]["states"]
    )
    with pytest.raises(RefusedError, match="evidence"):
        _ = run_census(tmp_path, [entry("W7", W7, w7, status="admitted")])


def test_uncertified_or_control_receipts_are_refused(tmp_path: Path) -> None:
    stall = write_json(
        tmp_path, "stall.json", {**kernel_receipt(W7), "status": "PASS_SAVED_STALL"}
    )
    with pytest.raises(RefusedError, match="closure"):
        _ = run_census(tmp_path, [entry("W7", W7, stall)])
    control = write_json(tmp_path, "control.json", bb_receipt(A, control=True))
    with pytest.raises(RefusedError, match="control"):
        _ = run_census(tmp_path, [entry("A", A, control, certifier="branch-and-bound")])
    budget = write_json(tmp_path, "budget.json", bb_receipt(A, verdict="unresolved-at-budget"))
    with pytest.raises(RefusedError, match="not certified"):
        _ = run_census(tmp_path, [entry("A", A, budget, certifier="branch-and-bound")])
