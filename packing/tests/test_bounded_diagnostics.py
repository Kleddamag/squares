"""Resource and provenance controls shared by the retained diagnostic tools."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

from devtools import bounded_diagnostics as bounded
from devtools import probe_n17_raw_row_support as raw
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError


def test_cold_receipt_metadata_does_not_change_objects(monkeypatch: pytest.MonkeyPatch) -> None:
    seed = {"mask": [8]}
    node = {"mask": [8], "final_state": {"mask": [8]}}
    receipt = {
        "status": "PASS_SAVED_STALL",
        "seed_sha256": raw.content_sha256(seed),
        "node_sha256": raw.content_sha256(node),
        "wall_seconds": 1,
    }
    monkeypatch.setattr(raw, "saved_files", lambda _: (Path("seed"), Path("node")))
    monkeypatch.setattr(raw, "bounded_load", lambda p: seed if p.name == "seed" else node)
    monkeypatch.setattr(raw, "bounded_json", lambda _: receipt)
    _, identity = raw.checked_inputs(Path("saved"), Path("receipt"))
    legacy = {**identity, "cold_receipt_sha256": "historical receipt metadata"}
    receipt.update(wall_seconds=99, host="different")
    assert raw.checked_inputs(Path("saved"), Path("receipt"))[1] == identity
    assert bounded.same_inputs(legacy, identity)
    seed["extra"] = [99]
    with pytest.raises(RefusalError, match="seed receipt differs"):
        raw.checked_inputs(Path("saved"), Path("receipt"))
    seed.pop("extra")
    node["extra"] = "changed node"
    with pytest.raises(RefusalError, match="node receipt differs"):
        raw.checked_inputs(Path("saved"), Path("receipt"))


def test_historical_header_metadata_and_exact_json_types() -> None:
    identity = {"seed_sha256": "seed", "node_sha256": "node"}
    expected = {"input_identity": identity, "diagnostic_only": True}
    old = {**expected, "input_identity": {**identity, "cold_receipt_sha256": "old"}}
    assert bounded.same_header(old, expected)
    assert "cold_receipt_sha256" in old["input_identity"]
    assert not bounded.same_header({**old, "diagnostic_only": 1}, expected)
    with pytest.raises(RefusalError, match="missing seed_sha256"):
        bounded.same_inputs({"node_sha256": "node"}, identity)


def test_legacy_resource_limit_label_is_reusable_without_relabelling_peak() -> None:
    old = {"limits": {"worker_peak_bytes": 512}, "worker_peak_bytes": 1000}
    new = {"limits": {"worker_current_rss_bytes": 512}, "worker_peak_bytes": 1000}
    assert bounded.same_header(old, new)
    assert bounded.same_content(old, new)
    assert old["worker_peak_bytes"] == 1000
    assert not bounded.same_header(old, {**new, "limits": {"worker_current_rss_bytes": 513}})


def test_retained_semantics_need_no_historical_git_object(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    revision = "historical revision is informational, even in a shallow clone"
    path = (
        "packing/campaign/explorations/X048-session-172-capacity-support/receipts/"
        "endpoint-support-packet.json"
    )
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_k: pytest.fail("Git unavailable"))
    value = bounded.retained_json(path)
    assert bounded.retained_matches(json.loads(json.dumps(value, indent=3)), revision, path)
    value["source_packet_sha256"] = "obsolete bookkeeping"
    assert bounded.retained_matches(value, revision, path)
    changed = copy.deepcopy(value)
    changed["diagnostic_only"] = 1
    assert not bounded.retained_matches(changed, revision, path)


@pytest.mark.parametrize("path", ["../x", "packing/../../x"])
def test_retained_locator_refuses_escaping_paths(path: str) -> None:
    with pytest.raises(RefusalError):
        bounded.retained_json(path)


def test_atomic_json_format_and_exact_byte_ceiling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "packet.json"
    value = {"rows": [{"owner": 8, "row": 1}], "supported": False}
    bounded.write_json(path, value)
    before = path.read_bytes()
    assert b"\r" not in before
    assert json.loads(before) == value
    monkeypatch.setattr(bounded, "MAX_PACKET_BYTES", len(before) - 1)
    with pytest.raises(RefusalError, match="output packet exceeds"):
        bounded.write_json(path, value)
    assert path.read_bytes() == before


def test_current_rss_guard_does_not_use_historical_peak(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    budget = Budget(time.monotonic() + 10, 1)
    monkeypatch.setattr(bounded, "current_memory_bytes", lambda: bounded.MAX_MEMORY_BYTES)
    bounded.check_budget(budget, wall_message="wall")
    monkeypatch.setattr(bounded, "current_memory_bytes", lambda: bounded.MAX_MEMORY_BYTES + 1)
    with pytest.raises(IncompleteError, match="current RSS"):
        bounded.check_budget(budget, wall_message="wall")


@pytest.mark.skipif(
    sys.platform not in {"win32", "linux"}, reason="current RSS is Windows/Linux"
)
def test_reusable_worker_after_release_passes_current_guard() -> None:
    # A fresh worker avoids attributing this pytest process's historic allocations.
    source = """
import gc, time
from devtools import bounded_diagnostics as b
from devtools.process_memory import current_memory_bytes, peak_memory_bytes
from sqpack.hull_kernel.geometry import Budget
baseline=current_memory_bytes()
held=bytearray(96*1024**2)
for i in range(0,len(held),4096): held[i]=1
assert current_memory_bytes() > baseline+64*1024**2
del held
gc.collect()
b.MAX_MEMORY_BYTES=baseline+48*1024**2
assert peak_memory_bytes() > b.MAX_MEMORY_BYTES
b.check_budget(Budget(time.monotonic()+5,1),wall_message='wall')
"""
    subprocess.run([sys.executable, "-c", source], check=True, timeout=10)
