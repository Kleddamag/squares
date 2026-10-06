"""Current guards and historical peak reporting remain distinct in a reused process."""

from __future__ import annotations

import json
import subprocess
import sys
from textwrap import dedent

import pytest

from devtools.process_memory import current_memory_bytes, peak_memory_bytes

CURRENT_RSS_HOSTS = {"linux", "win32"}
requires_current_rss = pytest.mark.skipif(
    sys.platform not in CURRENT_RSS_HOSTS,
    reason="current RSS is measured on Linux and Windows only; other hosts refuse by design",
)


def test_ungated_platform_refuses_current_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "platform", "darwin")
    with pytest.raises(OSError, match="unavailable on darwin"):
        current_memory_bytes()


@requires_current_rss
def test_live_memory_sample_is_positive() -> None:
    assert current_memory_bytes() > 0
    assert peak_memory_bytes() > 0


@requires_current_rss
def test_released_allocation_does_not_leave_current_memory_above_guard() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            dedent("""
            import gc
            import json
            from devtools.process_memory import current_memory_bytes, peak_memory_bytes
            baseline = current_memory_bytes()
            threshold = baseline + 48 * 1024**2
            allocation = bytearray(96 * 1024**2)
            for i in range(0, len(allocation), 4096):
                allocation[i] = 1
            live = current_memory_bytes()
            del allocation
            gc.collect()
            print(json.dumps(dict(threshold=threshold, live=live,
                                  current=current_memory_bytes(), peak=peak_memory_bytes())))
        """),
        ],
        text=True,
        capture_output=True,
        check=True,
        timeout=15,
    )
    sample = json.loads(result.stdout)
    assert sample["live"] > sample["threshold"]
    assert sample["peak"] > sample["threshold"]
    assert sample["current"] < sample["threshold"]
