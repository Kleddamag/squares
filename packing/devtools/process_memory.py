"""Process memory measurements shared by bounded diagnostic tools."""

from __future__ import annotations

import ctypes
import importlib
import os
import sys
from ctypes import wintypes
from pathlib import Path


def peak_memory_bytes() -> int:
    """Lifetime peak working set on Windows, or lifetime peak RSS on Unix."""
    if sys.platform != "win32":
        resource = importlib.import_module("resource")
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform == "darwin" else peak * 1024)

    return _windows_memory()[0]


def _windows_memory() -> tuple[int, int]:
    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("faults", wintypes.DWORD)] + [
            (name, ctypes.c_size_t)
            for name in ("peak", "working", "pp", "p", "pnp", "np", "page", "peakpage")
        ]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    value = Counters()
    value.cb = ctypes.sizeof(value)
    if not psapi.GetProcessMemoryInfo(
        kernel.GetCurrentProcess(), ctypes.byref(value), value.cb
    ):
        raise ctypes.WinError(ctypes.get_last_error())
    return int(value.peak), int(value.working)


def current_memory_bytes() -> int:
    """Current resident bytes on Windows/Linux; unsupported hosts fail explicitly.

    Lifetime peaks are separate reporting evidence, never this guard's input. macOS
    current RSS is deliberately ungated until a native implementation is validated.
    """
    if sys.platform == "win32":
        return _windows_memory()[1]
    if sys.platform.startswith("linux"):
        resident_pages = int(Path("/proc/self/statm").read_text(encoding="ascii").split()[1])
        return resident_pages * os.sysconf("SC_PAGE_SIZE")
    raise OSError(f"Current resident memory is unavailable on {sys.platform}")
