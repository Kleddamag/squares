"""Check sqsearch's declared Rust floor and prove its diagnostics reject bad code."""

from __future__ import annotations

import subprocess
import tomllib
from collections.abc import Sequence
from pathlib import Path

import pytest

from devtools import check_rust_floor
from sqpack.cli import validate

CRATE = Path(__file__).resolve().parents[1] / "sqsearch"


def test_rust_floor_and_gate_contract(monkeypatch: pytest.MonkeyPatch) -> None:
    """The fast gate executes tests and docs, not merely compilation of test code."""
    manifest = tomllib.loads((CRATE / "Cargo.toml").read_text())
    assert manifest["lints"]["rust"] == {
        "unsafe_code": "forbid",
        "missing_docs": "deny",
        "warnings": "deny",
    }
    assert manifest["lints"]["clippy"]["pedantic"] == {"level": "deny", "priority": -1}
    assert manifest["lints"]["clippy"]["unwrap_used"] == "deny"
    calls: list[tuple[str, ...]] = []

    def commands(
        context: validate.Context, commands: Sequence[Sequence[str]], *, cwd: Path
    ) -> str:
        assert cwd == CRATE
        assert context.environment["RUSTDOCFLAGS"].endswith("-D warnings")
        calls.extend(tuple(command) for command in commands)
        return "test result: ok. 5 passed; 0 failed"

    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", commands)
    environment = {"RUSTDOCFLAGS": "--document-private-items"}
    context = validate.Context(
        deep=False, strict=True, jobs=1, inner_jobs=1, environment=environment
    )
    step = next(step for step in validate.STEPS if step.name == "lint floor (rust)")
    step.action(context)
    assert environment == {"RUSTDOCFLAGS": "--document-private-items"}
    assert ("cargo", "test", "--locked", "--all-targets", "--quiet") in calls
    assert ("cargo", "doc", "--locked", "--no-deps", "--quiet") in calls
    assert ("cargo", "fmt", "--all", "--check") in calls
    assert any(call[-1].endswith("devtools/check_rust_floor.py") for call in calls)
    assert any(
        "clippy" in call and "--locked" in call and "--all-targets" in call for call in calls
    )
    assert step.fast


@pytest.mark.parametrize("failure", [None, "clean", "accepted", "wrong-diagnostic"])
def test_probe_outcomes(monkeypatch: pytest.MonkeyPatch, failure: str | None) -> None:
    """Tool absence and unrelated compiler errors cannot satisfy a negative probe."""
    monkeypatch.setattr(check_rust_floor.shutil, "which", lambda _: "cargo")
    calls: list[str] = []

    def compiler(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        root = Path(str(kwargs["cwd"]))
        source = (root / "src/lib.rs").read_text()
        calls.append(source)
        probe = next(item for item in check_rust_floor.PROBES if item[1] == source)
        assert command == ["cargo", "clippy", "--offline", "--quiet"]
        assert (root / "rust-toolchain.toml").read_bytes() == (
            CRATE / "rust-toolchain.toml"
        ).read_bytes()
        if probe[0] == "clean":
            return subprocess.CompletedProcess(
                command, int(failure == "clean"), "", "unavailable"
            )
        return subprocess.CompletedProcess(
            command,
            int(failure != "accepted"),
            "",
            "unrelated error" if failure == "wrong-diagnostic" else probe[2],
        )

    monkeypatch.setattr(check_rust_floor.subprocess, "run", compiler)
    if failure is None:
        check_rust_floor.check_probes()
        assert len(calls) == 5
    else:
        with pytest.raises(RuntimeError, match="Rust floor"):
            check_rust_floor.check_probes()


def test_missing_compiler_is_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(check_rust_floor.shutil, "which", lambda _: None)
    with pytest.raises(RuntimeError, match="require cargo"):
        check_rust_floor.check_probes()


def test_n17_native_declares_the_same_rust_floor() -> None:
    """The optional extension keeps the pinned compiler and enforced library lints."""
    native = CRATE.parent / "n17bb_native"
    manifest = tomllib.loads((native / "Cargo.toml").read_text())
    assert manifest["lints"]["rust"]["unsafe_code"] in {"deny", "forbid"}
    assert manifest["lints"]["rust"]["missing_docs"] == "deny"
    assert manifest["lints"]["rust"]["warnings"] == "deny"
    assert manifest["lints"]["clippy"]["pedantic"] == {"level": "deny", "priority": -1}
    assert manifest["lints"]["clippy"]["unwrap_used"] == "deny"
    assert tomllib.loads((native / "rust-toolchain.toml").read_text()) == tomllib.loads(
        (CRATE / "rust-toolchain.toml").read_text()
    )
    assert (native / "Cargo.lock").is_file()


@pytest.mark.parametrize("result", ["5 passed in 0.5s", "1 skipped", "no tests ran"])
def test_n17_gate_builds_then_requires_native_replay(
    monkeypatch: pytest.MonkeyPatch, result: str
) -> None:
    calls: list[tuple[str, ...]] = []

    def run(context: validate.Context, command: Sequence[str], **_: object) -> str:
        assert context.environment["N17BB_NATIVE_REQUIRED"] == "1"
        assert context.environment["N17BB_NATIVE_DIR"] == "/scratch/native/python"
        calls.append(tuple(command))
        if "devtools.build_n17_bb_native" in command:
            return "test result: ok. 3 passed; 0 failed"
        return result

    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_run", run)
    environment = {"CARGO_TARGET_DIR": "/scratch/native"}
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=environment
    )
    step = next(
        step for step in validate.STEPS if step.name == "n17 branch-and-bound native (Rust)"
    )
    assert step.fast
    assert step.broad
    assert "packing/n17bb_native/*" in step.touches
    if "passed" in result:
        assert result in step.action(context)
    else:
        with pytest.raises(validate.StepFailureError, match="unskipped"):
            step.action(context)
    assert "devtools.build_n17_bb_native" in calls[0]
    assert "tests/test_n17_bb_native.py" in calls[1]
    assert "tests/test_n17_bb_native_edges.py" in calls[1]
    assert environment == {"CARGO_TARGET_DIR": "/scratch/native"}


@pytest.mark.parametrize("output", ["", "test result: ok. 0 passed; 0 failed"])
def test_gate_refuses_empty_test_run(monkeypatch: pytest.MonkeyPatch, output: str) -> None:
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", lambda *_, **__: output)
    step = next(step for step in validate.STEPS if step.name == "lint floor (rust)")
    context = validate.Context(deep=False, strict=False, jobs=1, inner_jobs=1, environment={})
    with pytest.raises(validate.StepFailureError, match="no passing Rust tests"):
        step.action(context)


def test_gate_requires_compiler_even_without_strict(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: None)
    step = next(step for step in validate.STEPS if step.name == "lint floor (rust)")
    context = validate.Context(deep=False, strict=False, jobs=1, inner_jobs=1, environment={})
    with pytest.raises(validate.StepFailureError, match="requires cargo"):
        step.action(context)
