"""Check, build, and stage the native n=17 branch-and-bound extension."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
import tomllib
from pathlib import Path

from devtools import check_rust_floor

ROOT = Path(__file__).resolve().parent.parent
CRATE = ROOT / "n17bb_native"
TOOLCHAIN = CRATE / "rust-toolchain.toml"


def _python_target() -> str:
    """Return the Rust target triple matching the running Python interpreter."""
    machine = platform.machine().lower()
    system = platform.system()
    if machine in {"arm64", "aarch64"}:
        architecture = "aarch64"
    elif machine in {"amd64", "x86_64"}:
        architecture = "x86_64"
    else:
        raise RuntimeError(f"unsupported Python architecture: {machine}")
    if system == "Darwin":
        return f"{architecture}-apple-darwin"
    if system == "Linux":
        return f"{architecture}-unknown-linux-gnu"
    if system == "Windows" and architecture == "x86_64":
        return "x86_64-pc-windows-msvc"
    raise RuntimeError(f"unsupported Python platform: {system} {machine}")


def _rust_host(rustc: str, environment: dict[str, str]) -> str:
    """Read rustc's host triple without assuming the shell's architecture."""
    result = subprocess.run(
        (rustc, "-vV"),
        cwd=CRATE,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if line.startswith("host: "):
            return line.removeprefix("host: ").strip()
    raise RuntimeError("rustc -vV did not report a host triple")


def _toolchain_channel() -> str:
    """Return the exact toolchain channel pinned by this crate."""
    with TOOLCHAIN.open("rb") as stream:
        channel = tomllib.load(stream).get("toolchain", {}).get("channel")
    if not isinstance(channel, str) or not channel:
        raise RuntimeError("rust-toolchain.toml has no toolchain.channel")
    return channel


def _install_target(target: str, environment: dict[str, str]) -> None:
    """Install a cross target for the pinned toolchain when it is absent."""
    rustup = shutil.which("rustup", path=environment.get("PATH"))
    if rustup is None:
        raise RuntimeError(f"rustup is required to install Rust target {target}")
    toolchain = _toolchain_channel()
    listed = subprocess.run(
        (rustup, "target", "list", "--installed", "--toolchain", toolchain),
        cwd=CRATE,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    if target not in listed.stdout.splitlines():
        subprocess.run(
            (rustup, "target", "add", "--toolchain", toolchain, target),
            cwd=CRATE,
            env=environment,
            check=True,
        )


def _target_directory(environment: dict[str, str]) -> Path:
    """Resolve Cargo's target directory using Cargo's crate-relative semantics."""
    configured = Path(environment.get("CARGO_TARGET_DIR", "target"))
    return configured if configured.is_absolute() else CRATE / configured


def _artifact(target_directory: Path, target: str | None) -> Path:
    """Locate the cdylib produced by Cargo for this platform and target."""
    release = target_directory / "release"
    if target is not None:
        release = target_directory / target / "release"
    if sys.platform == "win32":
        return release / "n17bb_native.dll"
    if sys.platform == "darwin":
        return release / "libn17bb_native.dylib"
    return release / "libn17bb_native.so"


def _extension_name() -> str:
    """Return an importable stable-ABI module name for this platform."""
    return "n17bb_native.pyd" if sys.platform == "win32" else "n17bb_native.abi3.so"


def _run(command: tuple[str, ...], environment: dict[str, str]) -> None:
    """Run one visible Cargo gate and fail immediately when it fails."""
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=CRATE, env=environment, check=True)


def build(output_dir: Path | None = None) -> Path:
    """Run every crate gate, stage the extension, and return its directory."""
    environment = dict(os.environ)
    cargo = shutil.which("cargo", path=environment.get("PATH"))
    rustc = shutil.which("rustc", path=environment.get("PATH"))
    if cargo is None or rustc is None:
        raise RuntimeError("building n17bb-native requires cargo and rustc")
    environment["PYO3_PYTHON"] = sys.executable

    python_target = _python_target()
    host = _rust_host(rustc, environment)
    cross_target = python_target if python_target != host else None
    target_args: tuple[str, ...] = ()
    if cross_target is not None:
        _install_target(cross_target, environment)
        target_args = ("--target", cross_target)
        environment["PYO3_CROSS"] = "1"
        environment["PYO3_CROSS_PYTHON_VERSION"] = "3.14"

    rustdoc_flags = environment.get("RUSTDOCFLAGS", "")
    environment["RUSTDOCFLAGS"] = f"{rustdoc_flags} -D warnings".strip()
    check_rust_floor.check_probes(CRATE)
    print("Rust floor positive control and 4 negative probes passed", flush=True)
    _run((cargo, "fmt", "--all", "--check"), environment)
    test_environment = dict(environment)
    if platform.system() == "Darwin":
        library_directory = sysconfig.get_config_var("LIBDIR")
        if isinstance(library_directory, str) and library_directory:
            rust_flags = test_environment.get("RUSTFLAGS", "")
            test_environment["RUSTFLAGS"] = (
                f"{rust_flags} -L native={library_directory}"
            ).strip()
    _run(
        (
            cargo,
            "clippy",
            "--locked",
            "--release",
            "--all-targets",
            *target_args,
            "--",
            "-D",
            "warnings",
        ),
        environment,
    )
    _run(
        (
            cargo,
            "test",
            "--locked",
            "--all-targets",
            "--no-default-features",
            *target_args,
            "--quiet",
        ),
        test_environment,
    )
    _run(
        (cargo, "doc", "--locked", "--no-deps", *target_args, "--quiet"),
        environment,
    )
    _run(
        (cargo, "build", "--locked", "--release", *target_args, "--quiet"),
        environment,
    )

    target_directory = _target_directory(environment)
    source = _artifact(target_directory, cross_target)
    if not source.is_file():
        raise RuntimeError(f"Cargo did not produce the expected extension: {source}")
    destination = (
        output_dir.resolve()
        if output_dir is not None
        else (target_directory / "python").resolve()
    )
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination / _extension_name())
    return destination


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, build the extension, and print its import directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="directory that receives the importable stable-ABI extension",
    )
    args = parser.parse_args(argv)
    destination = build(args.output_dir)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
