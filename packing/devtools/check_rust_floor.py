"""Exercise the pinned sqsearch lint floor with disposable offline compiler probes."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

CRATE = Path(__file__).resolve().parents[1] / "sqsearch"
PROBES = (
    ("clean", "//! Probe.\n", None),
    ("missing-docs", "//! Probe.\npub fn undocumented() {}\n", "missing documentation"),
    ("warnings", "//! Probe.\nfn unused() {}\n", "never used"),
    (
        "pedantic",
        "//! Probe.\n/// Return the answer.\npub fn answer() -> u32 { 42 }\n",
        "must_use_candidate",
    ),
    (
        "unwrap",
        (
            "//! Probe.\n/// Probe.\npub fn unwrap_probe(value: Option<u32>) -> u32 "
            "{ value.unwrap() }\n"
        ),
        "used `unwrap()`",
    ),
)


def check_probes(crate: Path = CRATE) -> None:
    """Require a working positive control and each independently rejected defect."""
    cargo = shutil.which("cargo")
    if cargo is None:
        raise RuntimeError("Rust floor probes require cargo")
    lint_table = (crate / "Cargo.toml").read_text().split("[lints.rust]", 1)[1]
    # tempfile honors the task's TMPDIR; isolate targets from the engine and all
    # concurrent workers. Nothing is downloaded: the tiny crate has no dependencies.
    with tempfile.TemporaryDirectory(prefix="rust-floor-") as directory:
        root = Path(directory)
        (root / "Cargo.toml").write_text(
            '[package]\nname="rust-floor-probe"\nversion="0.0.0"\nedition="2021"\n'
            "[lints.rust]" + lint_table
        )
        shutil.copyfile(crate / "rust-toolchain.toml", root / "rust-toolchain.toml")
        (root / "src").mkdir()
        environment = dict(os.environ)
        environment["CARGO_TARGET_DIR"] = str(root / "target")
        for name, source, diagnostic in PROBES:
            (root / "src" / "lib.rs").write_text(source)
            result = subprocess.run(
                [cargo, "clippy", "--offline", "--quiet"],
                cwd=root,
                env=environment,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            if diagnostic is None:
                if result.returncode != 0:
                    raise RuntimeError(f"Rust floor positive control failed: {result.stderr}")
            elif result.returncode == 0 or diagnostic not in result.stderr:
                raise RuntimeError(
                    f"Rust floor probe {name} did not reject its defect: {result.stderr}"
                )


def main() -> None:
    """Run only in the Rust gate, where the pinned compiler is required."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crate", type=Path, default=CRATE)
    check_probes(parser.parse_args().crate)
    print("Rust floor positive control and 4 negative probes passed")


if __name__ == "__main__":
    main()
