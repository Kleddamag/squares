"""The frontend runner preserves every contract under bounded concurrency."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Barrier, Lock

import pytest

from workbench_tools import check_frontend
from workbench_tools.check_frontend import run_checks


def test_browser_checks_overlap_without_losing_order_or_coverage(tmp_path: Path) -> None:
    barrier = Barrier(2, timeout=5)
    lock = Lock()
    active = 0
    peak = 0
    called: list[int] = []

    def check(index: int):
        def run(page: Path) -> str:
            nonlocal active, peak
            assert page == tmp_path
            with lock:
                called.append(index)
                active += 1
                peak = max(peak, active)
            barrier.wait()
            with lock:
                active -= 1
            return str(index)

        return run

    results, timings = run_checks(
        tmp_path, [(str(index), check(index)) for index in range(4)], workers=2
    )
    assert results == ["0", "1", "2", "3"]
    assert sorted(called) == [0, 1, 2, 3]
    assert peak == 2
    assert list(timings) == results
    assert all(elapsed >= 0 for elapsed in timings.values())


@pytest.mark.parametrize("workers", [1, 2])
def test_browser_failure_is_never_converted_to_success(tmp_path: Path, workers: int) -> None:
    def reject(_: Path) -> str:
        raise ValueError("browser contract failed")

    with pytest.raises(ValueError, match="browser contract failed"):
        run_checks(tmp_path, [("reject", reject)], workers=workers)


@pytest.mark.parametrize("workers", [0, 3, -1])
def test_worker_count_is_bounded(tmp_path: Path, workers: int) -> None:
    with pytest.raises(ValueError, match="one or two"):
        run_checks(tmp_path, [], workers=workers)


def test_timing_receipt_is_complete_and_refuses_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_frontend, "build", lambda _: None)
    monkeypatch.setattr(check_frontend, "source_revision", lambda: "a" * 40)
    monkeypatch.setattr(check_frontend, "source_dirty", lambda: True)
    monkeypatch.setattr(
        check_frontend, "run_checks", lambda *_, **__: (["passed"], {"check": 0.1})
    )
    receipt = tmp_path / "timings.json"
    assert check_frontend.main(["--workers", "2", "--timings", str(receipt)]) == 0
    result = json.loads(receipt.read_text())
    assert result["status"] == "passed"
    assert result["source_commit"] == "a" * 40
    assert result["source_dirty"] is True
    assert result["workers"] == 2
    assert result["checks"] == {"check": 0.1}
    before = receipt.read_bytes()
    with pytest.raises(SystemExit):
        check_frontend.main(["--timings", str(receipt)])
    assert receipt.read_bytes() == before
