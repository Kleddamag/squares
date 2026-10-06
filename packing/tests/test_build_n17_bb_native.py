"""Hold the optional extension's build target to the interpreter that imports it."""

# The helper's command construction is its tested external-tool boundary.
# pyright: reportPrivateUsage=false

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import build_n17_bb_native as builder


@pytest.mark.parametrize(
    ("machine", "system", "target"),
    [
        ("arm64", "Darwin", "aarch64-apple-darwin"),
        ("x86_64", "Darwin", "x86_64-apple-darwin"),
        ("aarch64", "Linux", "aarch64-unknown-linux-gnu"),
        ("AMD64", "Windows", "x86_64-pc-windows-msvc"),
    ],
)
def test_target_follows_python(
    monkeypatch: pytest.MonkeyPatch, machine: str, system: str, target: str
) -> None:
    monkeypatch.setattr(builder.platform, "machine", lambda: machine)
    monkeypatch.setattr(builder.platform, "system", lambda: system)
    assert builder._python_target() == target  # noqa: SLF001


def test_rosetta_build_checks_every_gate_and_stages_arm64(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A host compiler must not silently produce an unimportable x86 extension."""
    target = tmp_path / "build"
    artifact = target / "aarch64-apple-darwin/release/libn17bb_native.dylib"
    artifact.parent.mkdir(parents=True)
    artifact.write_bytes(b"native extension fixture")
    monkeypatch.setenv("CARGO_TARGET_DIR", str(target))
    monkeypatch.setattr(builder, "_python_target", lambda: "aarch64-apple-darwin")
    monkeypatch.setattr(builder, "_rust_host", lambda *_: "x86_64-apple-darwin")
    monkeypatch.setattr(builder.sys, "platform", "darwin")
    monkeypatch.setattr(builder.shutil, "which", lambda name, **_: name)
    probed: list[Path] = []
    monkeypatch.setattr(builder.check_rust_floor, "check_probes", probed.append)
    installed: list[str] = []
    monkeypatch.setattr(builder, "_install_target", lambda name, _: installed.append(name))
    commands: list[tuple[str, ...]] = []

    def run(command: tuple[str, ...], environment: dict[str, str]) -> None:
        assert environment["RUSTDOCFLAGS"].endswith("-D warnings")
        commands.append(command)

    monkeypatch.setattr(builder, "_run", run)
    destination = builder.build(tmp_path / "importable")
    assert installed == ["aarch64-apple-darwin"]
    assert probed == [builder.CRATE]
    assert (destination / "n17bb_native.abi3.so").read_bytes() == artifact.read_bytes()
    cargo_commands = [command for command in commands if command[0] == "cargo"]
    assert [command[1] for command in cargo_commands] == [
        "fmt",
        "clippy",
        "test",
        "doc",
        "build",
    ]
    for command in cargo_commands[1:]:
        assert "--locked" in command
        assert command[command.index("--target") + 1] == "aarch64-apple-darwin"
    assert "--release" in cargo_commands[-1]
