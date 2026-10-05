"""Opt-in bounded Windows subprocess supervisor, standard library only.

Usage: python -m devtools.supervise_windows --cwd DIR --output-dir NEW_DIR
--timeout 600 -- EXE ARG...
The child is created suspended, assigned to a kill-on-close Job, then resumed.
stdout.log and stderr.log receive child output directly and remain readable live.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import math
import os
import signal
import subprocess
import sys
import time
from ctypes import wintypes
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, NoReturn

GIB = 1024**3
MEASUREMENT_FAILURE_LIMIT = 3


def gib_bytes(value: float) -> int:
    """Convert finite configured GiB without overflowing a floating-point product."""
    numerator, denominator = value.as_integer_ratio()
    return numerator * GIB // denominator


def utc_now():
    return datetime.now(UTC).isoformat()


def durable_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def process_handle(process: subprocess.Popen[bytes]) -> int:
    """The Windows Popen owns this handle; callers never close it directly."""
    return int(process.__dict__["_handle"])


def refuse(message: str) -> NoReturn:
    raise RuntimeError(message)


def windows_ctypes(name: str) -> Any:
    """Resolve the native ABI only inside the platform-guarded execution path."""
    return getattr(ctypes, name)


def win_error(code: int) -> NoReturn:
    raise windows_ctypes("WinError")(code)


class WindowsJob:
    # Dynamic DLLs/Structure subclasses exist only after the Windows platform gate.
    # Declared ABI boundaries keep non-Windows import/type checking independent.
    kernel: Any
    psapi: Any
    ntdll: Any
    handle: Any
    ExtendedLimit: Any
    Accounting: Any
    ProcessMemory: Any
    MemoryStatus: Any

    def __init__(self):
        if os.name != "nt":
            raise RuntimeError("Windows is required; no unmonitored fallback")
        self.kernel = windows_ctypes("WinDLL")("kernel32", use_last_error=True)
        self.psapi = windows_ctypes("WinDLL")("psapi", use_last_error=True)
        self.ntdll = windows_ctypes("WinDLL")("ntdll", use_last_error=True)
        size_t = ctypes.c_size_t

        class BasicLimit(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", size_t),
                ("MaximumWorkingSetSize", size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class IOCounters(ctypes.Structure):
            _fields_ = [
                (name, ctypes.c_ulonglong)
                for name in (
                    "ReadOperationCount",
                    "WriteOperationCount",
                    "OtherOperationCount",
                    "ReadTransferCount",
                    "WriteTransferCount",
                    "OtherTransferCount",
                )
            ]

        class ExtendedLimit(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BasicLimit),
                ("IoInfo", IOCounters),
                ("ProcessMemoryLimit", size_t),
                ("JobMemoryLimit", size_t),
                ("PeakProcessMemoryUsed", size_t),
                ("PeakJobMemoryUsed", size_t),
            ]

        class Accounting(ctypes.Structure):
            _fields_ = [
                ("TotalUserTime", ctypes.c_longlong),
                ("TotalKernelTime", ctypes.c_longlong),
                ("ThisPeriodTotalUserTime", ctypes.c_longlong),
                ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
                ("TotalPageFaultCount", wintypes.DWORD),
                ("TotalProcesses", wintypes.DWORD),
                ("ActiveProcesses", wintypes.DWORD),
                ("TotalTerminatedProcesses", wintypes.DWORD),
            ]

        class ProcessMemory(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
                (name, size_t)
                for name in (
                    "PeakWorkingSetSize",
                    "WorkingSetSize",
                    "QuotaPeakPagedPoolUsage",
                    "QuotaPagedPoolUsage",
                    "QuotaPeakNonPagedPoolUsage",
                    "QuotaNonPagedPoolUsage",
                    "PagefileUsage",
                    "PeakPagefileUsage",
                    "PrivateUsage",
                )
            ]

        class MemoryStatus(ctypes.Structure):
            _fields_ = [("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD)] + [
                (name, ctypes.c_ulonglong)
                for name in (
                    "ullTotalPhys",
                    "ullAvailPhys",
                    "ullTotalPageFile",
                    "ullAvailPageFile",
                    "ullTotalVirtual",
                    "ullAvailVirtual",
                    "ullAvailExtendedVirtual",
                )
            ]

        self.ExtendedLimit = ExtendedLimit
        self.Accounting = Accounting
        self.ProcessMemory = ProcessMemory
        self.MemoryStatus = MemoryStatus
        declarations = [
            (
                self.kernel,
                "CreateJobObjectW",
                [ctypes.c_void_p, wintypes.LPCWSTR],
                wintypes.HANDLE,
            ),
            (
                self.kernel,
                "SetInformationJobObject",
                [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD],
                wintypes.BOOL,
            ),
            (
                self.kernel,
                "QueryInformationJobObject",
                [
                    wintypes.HANDLE,
                    ctypes.c_int,
                    ctypes.c_void_p,
                    wintypes.DWORD,
                    ctypes.c_void_p,
                ],
                wintypes.BOOL,
            ),
            (
                self.kernel,
                "AssignProcessToJobObject",
                [wintypes.HANDLE, wintypes.HANDLE],
                wintypes.BOOL,
            ),
            (
                self.kernel,
                "TerminateJobObject",
                [wintypes.HANDLE, wintypes.UINT],
                wintypes.BOOL,
            ),
            (self.kernel, "CloseHandle", [wintypes.HANDLE], wintypes.BOOL),
            (
                self.kernel,
                "OpenProcess",
                [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD],
                wintypes.HANDLE,
            ),
            (
                self.kernel,
                "IsProcessInJob",
                [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)],
                wintypes.BOOL,
            ),
            (
                self.kernel,
                "WaitForSingleObject",
                [wintypes.HANDLE, wintypes.DWORD],
                wintypes.DWORD,
            ),
            (
                self.kernel,
                "GetProcessTimes",
                [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4,
                wintypes.BOOL,
            ),
            (
                self.kernel,
                "GlobalMemoryStatusEx",
                [ctypes.POINTER(MemoryStatus)],
                wintypes.BOOL,
            ),
            (
                self.psapi,
                "GetProcessMemoryInfo",
                [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD],
                wintypes.BOOL,
            ),
            (self.ntdll, "NtResumeProcess", [wintypes.HANDLE], ctypes.c_long),
        ]
        for library, name, arguments, result in declarations:
            function = getattr(library, name)  # Missing API raises before launch.
            function.argtypes = arguments
            function.restype = result
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise windows_ctypes("WinError")(windows_ctypes("get_last_error")())
        try:
            limits = ExtendedLimit()
            limits.BasicLimitInformation.LimitFlags = 0x2000  # KILL_ON_JOB_CLOSE.
            self.require(
                self.kernel.SetInformationJobObject(
                    self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)
                )
            )
            self.accounting()
            self.process_ids()
            self.memory_available()
        except BaseException:
            self.close()
            raise

    @staticmethod
    def require(ok):
        if not ok:
            raise windows_ctypes("WinError")(windows_ctypes("get_last_error")())

    def accounting(self):
        value = self.Accounting()
        self.require(
            self.kernel.QueryInformationJobObject(
                self.handle, 1, ctypes.byref(value), ctypes.sizeof(value), None
            )
        )
        return {
            "tree_cpu_seconds": (value.TotalUserTime + value.TotalKernelTime) / 10_000_000,
            "job_active_processes": value.ActiveProcesses,
            "job_total_processes": value.TotalProcesses,
        }

    def memory_available(self):
        value = self.MemoryStatus()
        value.dwLength = ctypes.sizeof(value)
        self.require(self.kernel.GlobalMemoryStatusEx(ctypes.byref(value)))
        return int(value.ullAvailPhys)

    def process_times(self, handle):
        times = [wintypes.FILETIME() for _ in range(4)]
        self.require(
            self.kernel.GetProcessTimes(handle, *(ctypes.byref(item) for item in times))
        )

        def ticks(value: wintypes.FILETIME) -> int:
            return (value.dwHighDateTime << 32) + value.dwLowDateTime

        return ticks(times[0]), (ticks(times[2]) + ticks(times[3])) / 10_000_000

    def process_cpu(self, process):
        return self.process_times(process_handle(process))[1]

    def process_ids(self):
        """Query only this Job's PID list, retrying boundedly if it grows mid-query."""
        capacity = 16
        for _ in range(8):

            class ProcessIds(ctypes.Structure):
                _fields_ = [
                    ("assigned", wintypes.DWORD),
                    ("listed", wintypes.DWORD),
                    ("pids", ctypes.c_size_t * capacity),
                ]

            value = ProcessIds()
            ok = self.kernel.QueryInformationJobObject(
                self.handle, 3, ctypes.byref(value), ctypes.sizeof(value), None
            )
            code = windows_ctypes("get_last_error")() if not ok else 0
            if not ok and code != 234:  # ERROR_MORE_DATA.
                raise windows_ctypes("WinError")(code)
            if ok and value.listed <= capacity and value.assigned <= value.listed:
                return [int(pid) for pid in value.pids[: value.listed]]
            capacity = max(capacity * 2, int(value.assigned))
            if capacity > 65_536:
                raise RuntimeError("Job PID-list capacity guard exceeded")
        raise RuntimeError("Job PID list did not stabilize in eight bounded queries")

    def handle_exited(self, handle):
        value = self.kernel.WaitForSingleObject(handle, 0)
        if value == 0:
            return True
        if value == 258:  # WAIT_TIMEOUT: the process is still running.
            return False
        if value == 0xFFFFFFFF:
            raise windows_ctypes("WinError")(windows_ctypes("get_last_error")())
        raise RuntimeError(f"Unexpected process wait result {value}")

    def cleanup_handles(self):
        """Retain owned identities across termination, since zero Job count can precede
        the process-handle exit signal. Never retain an unrelated reused PID's handle.
        """
        handles = []
        try:
            for pid in self.process_ids():
                handle = self.kernel.OpenProcess(0x1000 | 0x100000, 0, pid)
                if not handle:
                    code = windows_ctypes("get_last_error")()
                    if pid not in self.process_ids():
                        continue
                    win_error(code)
                try:
                    member = wintypes.BOOL()
                    self.require(
                        self.kernel.IsProcessInJob(handle, self.handle, ctypes.byref(member))
                    )
                    if not member.value:
                        continue
                    created, _ = self.process_times(handle)
                    handles.append((pid, created, handle))
                    handle = None  # Ownership transferred to the returned list.
                finally:
                    if handle:
                        self.require(self.kernel.CloseHandle(handle))
        except BaseException:
            for _, _, handle in handles:
                self.kernel.CloseHandle(handle)
            raise
        return handles

    def worker_sample(self):
        """Measure live owned handles; PID reuse cannot substitute an unrelated worker.

        Creation time identifies successive processes that reuse a PID. Every opened
        handle is closed here. An exited process may disappear between any two calls;
        non-race failures are retained for the supervisor's consecutive-failure guard.
        """
        pids = self.process_ids()
        workers, failures, races = [], [], []
        for pid in pids:
            # QUERY_INFORMATION | VM_READ | SYNCHRONIZE; no mutation access.
            handle = self.kernel.OpenProcess(0x0400 | 0x0010 | 0x100000, 0, pid)
            if not handle:
                code = windows_ctypes("get_last_error")()
                if pid not in self.process_ids():
                    races.append({"pid": pid, "reason": "exited-before-open"})
                else:
                    failures.append({"pid": pid, "stage": "open", "winerror": code})
                continue
            try:
                member = wintypes.BOOL()
                self.require(
                    self.kernel.IsProcessInJob(handle, self.handle, ctypes.byref(member))
                )
                if not member.value:
                    races.append({"pid": pid, "reason": "PID-reused-outside-owned-job"})
                    continue
                if self.handle_exited(handle):
                    races.append({"pid": pid, "reason": "exited-before-measurement"})
                    continue
                created, cpu = self.process_times(handle)
                memory = self.ProcessMemory()
                memory.cb = ctypes.sizeof(memory)
                self.require(
                    self.psapi.GetProcessMemoryInfo(
                        handle, ctypes.byref(memory), ctypes.sizeof(memory)
                    )
                )
                workers.append(
                    {
                        "pid": pid,
                        "creation_filetime_ticks": created,
                        "working_set_bytes": int(memory.WorkingSetSize),
                        "peak_working_set_bytes": int(memory.PeakWorkingSetSize),
                        "private_committed_bytes": int(memory.PrivateUsage),
                        "cpu_seconds": cpu,
                    }
                )
            except OSError as exc:
                if self.handle_exited(handle):
                    races.append({"pid": pid, "reason": "exited-during-measurement"})
                else:
                    failures.append({"pid": pid, "stage": "measurement", "error": str(exc)})
            finally:
                self.require(self.kernel.CloseHandle(handle))
        return {
            "workers": workers,
            "enumerated_job_pids": pids,
            "worker_measurement_failures": failures,
            "worker_exit_races": races,
            "worker_count_measured": len(workers),
            "max_worker_working_set_bytes": max(
                (w["working_set_bytes"] for w in workers), default=0
            ),
            "max_worker_peak_working_set_bytes": max(
                (w["peak_working_set_bytes"] for w in workers), default=0
            ),
            # Shared pages can occur in several working sets. This is not physical use.
            "sum_worker_working_sets_overcount_bytes": sum(
                w["working_set_bytes"] for w in workers
            ),
        }

    def job_peak_committed(self):
        limits = self.ExtendedLimit()
        self.require(
            self.kernel.QueryInformationJobObject(
                self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits), None
            )
        )
        return int(limits.PeakJobMemoryUsed)

    def root_sample(self, process):
        memory = self.ProcessMemory()
        memory.cb = ctypes.sizeof(memory)
        self.require(
            self.psapi.GetProcessMemoryInfo(
                process_handle(process), ctypes.byref(memory), ctypes.sizeof(memory)
            )
        )
        return {
            "root_working_set_bytes": int(memory.WorkingSetSize),
            "root_peak_working_set_bytes": int(memory.PeakWorkingSetSize),
            "root_private_committed_bytes": int(memory.PrivateUsage),
            "root_cpu_seconds": self.process_cpu(process),
        }

    def sample(self, process):
        root = {}
        if process.poll() is None:
            try:
                root = self.root_sample(process)
            except OSError:
                if process.poll() is None:
                    raise
        return {
            **root,
            **self.worker_sample(),
            **self.accounting(),
            "job_peak_committed_bytes": self.job_peak_committed(),
            "root_cpu_seconds": self.process_cpu(process),
            "system_available_memory_bytes": self.memory_available(),
        }

    def assign(self, process):
        self.require(self.kernel.AssignProcessToJobObject(self.handle, process_handle(process)))

    def resume(self, process):
        status = self.ntdll.NtResumeProcess(process_handle(process))
        if status < 0:
            raise RuntimeError(f"NtResumeProcess failed, NTSTATUS 0x{status & 0xFFFFFFFF:08x}")

    def terminate(self):
        self.require(self.kernel.TerminateJobObject(self.handle, 137))

    def close(self):
        if self.handle:
            handle, self.handle = self.handle, None
            self.require(self.kernel.CloseHandle(handle))


def supervise(args):
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise RuntimeError("Output directory must be empty; receipts are never overwritten")
    started = time.monotonic()
    receipt = {
        "schema": "packing.windows-supervisor.v1",
        "started_at": utc_now(),
        "command": args.command,
        "cwd": str(args.cwd.resolve()),
        "timeout_seconds": args.timeout,
        "sample_interval_seconds": args.interval,
        "worker_memory_stop_bytes": gib_bytes(args.worker_memory_gib),
        "worker_memory_review_stop_bytes": gib_bytes(args.review_memory_gib),
        "worker_measurement_failure_limit": MEASUREMENT_FAILURE_LIMIT,
        "system_available_stop_bytes": gib_bytes(args.min_available_gib),
        "supervisor_pid": os.getpid(),
        "pid": None,
        "status": "starting",
        "root_status": "not-started",
        "root_exited_before_cleanup": None,
        "live_descendants_before_cleanup": None,
        "descendants_termination_requested": None,
        "assigned_to_job": False,
        "termination_scope": "owned Windows Job Object including descendants",
        "memory_scope": (
            "per-live-owned-process current and peak working sets; "
            "shared-page overcounting sum "
            "and Job committed memory separately labelled"
        ),
        "memory_sampling_limit": (
            "Processes that start and exit between samples can be missed; observed per-process "
            "OS peaks are not a perfect tree RSS maximum"
        ),
    }
    durable_json(output / "start.json", receipt)
    job = None
    process = None
    last_sample = {}
    error = None
    cleanup_errors = []
    reason = "technical-failure"
    peak_root = 0
    peak_job = 0
    peak_worker = 0
    observed_workers = {}
    measurement_failures = 0
    total_measurement_failures = 0
    min_available = None
    stream = None
    try:
        job = WindowsJob()
        available = job.memory_available()
        min_available = available
        if available < receipt["system_available_stop_bytes"]:
            reason = "guard-refused-system-memory"
            refuse("Available physical memory is below the configured start guard")
        stream = (output / "samples.jsonl").open("a", encoding="utf-8", newline="\n")
        with (
            (output / "stdout.log").open("wb", buffering=0) as stdout,
            (output / "stderr.log").open("wb", buffering=0) as stderr,
        ):
            process = subprocess.Popen(
                args.command,
                cwd=args.cwd,
                stdin=subprocess.DEVNULL,
                stdout=stdout,
                stderr=stderr,
                shell=False,
                creationflags=0x00000004 | 0x08000000 | 0x00000200,
            )
            receipt.update(pid=process.pid, status="suspended")
            durable_json(output / "start.json", receipt)
            # Assignment occurs while suspended. Verify owned-process monitor APIs
            # before allowing the root to execute any user code.
            job.assign(process)
            receipt["assigned_to_job"] = True
            last_sample = job.sample(process)
            if last_sample["worker_measurement_failures"] or not last_sample["workers"]:
                refuse("Suspended owned root could not be measured before resume")
            job.resume(process)
            receipt.update(status="running", assigned_to_job=True, resumed_at=utc_now())
            durable_json(output / "start.json", receipt)
            while True:
                exited = process.poll() is not None
                # Descendants are measured even if the launcher has just exited.
                last_sample = job.sample(process)
                wall = time.monotonic() - started
                peak_root = max(peak_root, last_sample.get("root_peak_working_set_bytes", 0))
                peak_job = max(peak_job, last_sample.get("job_peak_committed_bytes", 0))
                peak_worker = max(peak_worker, last_sample["max_worker_peak_working_set_bytes"])
                for worker in last_sample["workers"]:
                    key = (worker["pid"], worker["creation_filetime_ticks"])
                    prior = observed_workers.get(key, {})
                    observed_workers[key] = {
                        **worker,
                        "max_sampled_working_set_bytes": max(
                            prior.get("max_sampled_working_set_bytes", 0),
                            worker["working_set_bytes"],
                        ),
                        "peak_working_set_bytes": max(
                            prior.get("peak_working_set_bytes", 0),
                            worker["peak_working_set_bytes"],
                        ),
                    }
                failed = bool(last_sample["worker_measurement_failures"]) or (
                    last_sample["job_active_processes"] > 0 and not last_sample["workers"]
                )
                measurement_failures = measurement_failures + 1 if failed else 0
                total_measurement_failures += int(failed)
                last_sample["consecutive_worker_measurement_failures"] = measurement_failures
                min_available = min(min_available, last_sample["system_available_memory_bytes"])
                sample = {
                    "at": utc_now(),
                    "wall_seconds": wall,
                    "pid": process.pid,
                    "root_exited": exited,
                    **last_sample,
                }
                stream.write(json.dumps(sample, sort_keys=True) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
                durable_json(output / "heartbeat.json", sample)
                over_stop = [
                    w
                    for w in last_sample["workers"]
                    if max(w["working_set_bytes"], w["peak_working_set_bytes"])
                    >= receipt["worker_memory_stop_bytes"]
                ]
                over_review = [
                    w
                    for w in last_sample["workers"]
                    if max(w["working_set_bytes"], w["peak_working_set_bytes"])
                    >= receipt["worker_memory_review_stop_bytes"]
                ]
                if over_stop or over_review:
                    reason = "worker-memory-stop" if over_stop else "worker-memory-review"
                    receipt["worker_memory_trigger"] = over_stop or over_review
                    break
                if measurement_failures >= MEASUREMENT_FAILURE_LIMIT:
                    reason = "worker-measurement-failed"
                    error = (
                        "Owned-worker measurements unavailable for three consecutive samples"
                    )
                    break
                if (
                    last_sample["system_available_memory_bytes"]
                    < receipt["system_available_stop_bytes"]
                ):
                    reason = "system-memory-stop"
                    break
                if exited:
                    reason = "success" if process.returncode == 0 else "command-failed"
                    break
                if wall >= args.timeout:
                    reason = "timeout"
                    break
                time.sleep(min(args.interval, max(0.01, args.timeout - wall)))
    except KeyboardInterrupt:
        reason = "interrupted"
    except BaseException as exc:  # noqa: BLE001 -- record failure after mandatory tree cleanup
        error = f"{type(exc).__name__}: {exc}"
    finally:
        if job is not None:
            cleanup_handles = []
            try:
                cleanup_handles = job.cleanup_handles()
                before = job.accounting()
                receipt["active_processes_before_cleanup"] = before["job_active_processes"]
                receipt["root_exited_before_cleanup"] = (
                    process is not None and process.poll() is not None
                )
                root_pid = None if process is None else process.pid
                receipt["live_descendants_before_cleanup"] = sum(
                    pid != root_pid and not job.handle_exited(handle)
                    for pid, _, handle in cleanup_handles
                )
                receipt["descendants_termination_requested"] = bool(
                    before["job_active_processes"]
                    and receipt["live_descendants_before_cleanup"]
                )
                if before["job_active_processes"]:
                    job.terminate()
                cleanup_deadline = time.monotonic() + 10
                while (
                    job.accounting()["job_active_processes"]
                    or any(not job.handle_exited(handle) for _, _, handle in cleanup_handles)
                ) and time.monotonic() < cleanup_deadline:
                    time.sleep(0.05)
                receipt.update(job.accounting())
                peak_job = max(peak_job, job.job_peak_committed())
                receipt["cleanup_process_identity_checks"] = [
                    {
                        "pid": pid,
                        "creation_filetime_ticks": created,
                        "exit_signalled": job.handle_exited(handle),
                    }
                    for pid, created, handle in cleanup_handles
                ]
                receipt["tree_cleanup_confirmed"] = receipt[
                    "job_active_processes"
                ] == 0 and all(
                    item["exit_signalled"]
                    for item in receipt["cleanup_process_identity_checks"]
                )
                if not receipt["tree_cleanup_confirmed"]:
                    cleanup_errors.append(
                        "Job or retained owned process handles did not finish "
                        "after cleanup wait"
                    )
            except BaseException as exc:  # noqa: BLE001 -- cleanup must attempt every handle
                cleanup_errors.append(f"Job cleanup: {exc}")
            finally:
                for _, _, handle in cleanup_handles:
                    try:
                        job.require(job.kernel.CloseHandle(handle))
                    except BaseException as exc:  # noqa: BLE001 -- close remaining handles
                        cleanup_errors.append(f"Cleanup process handle close: {exc}")
                try:
                    job.close()  # Last-resort whole-tree kill, also on monitor failure.
                except BaseException as exc:  # noqa: BLE001 -- retain final kill/close failure
                    cleanup_errors.append(f"Job close: {exc}")
        if process is not None:
            try:
                if process.poll() is None:
                    # Assignment can fail before the suspended root joins the job.
                    # That root has never run, so it cannot yet have descendants.
                    process.kill()
                process.wait(timeout=10)
                if job is not None:
                    last_sample["root_cpu_seconds"] = job.process_cpu(process)
            except BaseException as exc:  # noqa: BLE001 -- retain root reap failure in receipt
                cleanup_errors.append(f"Root cleanup: {exc}")
        if stream is not None:
            stream.close()
        receipt.update(
            status=reason,
            ended_at=utc_now(),
            wall_seconds=time.monotonic() - started,
            returncode=None if process is None else process.returncode,
            root_status=(
                "not-started"
                if process is None
                else "exit-unconfirmed"
                if process.returncode is None
                else "exited-zero"
                if process.returncode == 0
                else "exited-nonzero"
            ),
            peak_root_working_set_bytes=peak_root,
            peak_job_committed_bytes=peak_job,
            peak_observed_worker_working_set_bytes=peak_worker,
            observed_workers=list(observed_workers.values()),
            worker_measurement_failure_samples=total_measurement_failures,
            minimum_system_available_memory_bytes=min_available,
            root_cpu_seconds=last_sample.get("root_cpu_seconds"),
            error=error,
            cleanup_errors=cleanup_errors,
        )
        if cleanup_errors:
            receipt["status"] = "cleanup-failed"
        durable_json(output / "final.json", receipt)
    print(json.dumps(receipt, sort_keys=True), flush=True)
    return (
        0
        if receipt["status"] == "success"
        else 124
        if receipt["status"] == "timeout"
        else 130
        if receipt["status"] == "interrupted"
        else 2
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, required=True)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument(
        "--worker-memory-gib",
        type=float,
        default=16.0,
        help="Stop when an owned process current or observed OS peak reaches this value",
    )
    parser.add_argument(
        "--review-memory-gib",
        type=float,
        default=12.0,
        help="Early review stop; hard-stop label wins if one sample crosses both limits",
    )
    parser.add_argument(
        "--min-available-gib",
        type=float,
        default=8.0,
        help="Available physical-memory floor (>=0); default 8 GiB is conservative",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def validated_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(arguments)
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.command or not args.cwd.is_dir():
        parser.error("a command argument list and an existing cwd are required")
    if not Path(args.command[0]).is_absolute() or not Path(args.command[0]).is_file():
        parser.error("the command executable must be an existing absolute file path")
    guards = (
        args.timeout,
        args.interval,
        args.worker_memory_gib,
        args.review_memory_gib,
        args.min_available_gib,
    )
    if not all(math.isfinite(value) for value in guards):
        parser.error("all numeric guards must be finite")
    if not 0 < args.timeout <= 1800 or not 0.1 <= args.interval <= 5:
        parser.error("timeout must be in (0,1800] and interval in [0.1,5]")
    if args.worker_memory_gib <= 0 or args.review_memory_gib <= 0 or args.min_available_gib < 0:
        parser.error(
            "worker/review limits must be positive; available-memory floor must be >=0"
        )
    return args


def install_interrupt_handlers() -> None:
    def interrupt(_signum: int, _frame: object) -> None:
        raise KeyboardInterrupt

    for name in ("SIGTERM", "SIGBREAK"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), interrupt)


def main(arguments: list[str] | None = None) -> int:
    args = validated_arguments(arguments)
    if os.name != "nt":
        print("Windows is required; no child launched or unmonitored fallback", file=sys.stderr)
        return 2
    install_interrupt_handlers()
    return supervise(args)


if __name__ == "__main__":
    raise SystemExit(main())
