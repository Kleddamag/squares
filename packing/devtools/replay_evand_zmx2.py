"""Build Evan Daniel's ``zmx2`` from retained bytes and replay a mixed or point cover.

Stage 4 of the result import process replays the source's own checker on the retained
bytes (``campaign/result-import.md``). For the covers in Daniel's format that checker is
the Rust ``zmx2``, and every input it needs is retained here: its source at the version a
run's manifest names, the crate files it builds with, and the cover. This tool assembles
them in a scratch directory, refusing any file whose SHA-256 is not the one the record
states, builds the binary with ``cargo``, and runs ``zmx2 cert`` under
``devtools.replay_receipt``, so every run leaves a receipt in one shape.

``build --checker 6b7f0f79|92a4cfe8 --work DIR``
    Writes ``DIR/<checker>/verify2/`` and builds ``target/release/zmx2``; the receipt is
    ``DIR/<checker>/build.log``. Rebuilding an existing directory is a no-op apart from
    re-checking the digests.
``run --case N --mode d4|full --work DIR --out OUT [--threads T] [--x LO-HI] [--y LO-HI]``
    Runs the case's cover with the flags its source used (``CASES``), writing the
    receipt ``OUT/<name>.log`` and the root log ``OUT/<name>_roots.log``. ``--x`` and
    ``--y`` restrict the root region, so one sweep can be split across machines; the
    region is in the file name. Running the same command again resumes from the root log,
    which ``zmx2`` reads before it starts, so an interrupted run loses at most the roots
    in flight; the resumed run writes ``<name>_resume<k>.log`` beside the first receipt.

What a run decides is read afterwards by ``devtools.audit_evand_mixed_covers``. This
tool decides nothing about a cover: it only guarantees which bytes were run.

It imports only the standard library and ``devtools.replay_receipt``, so it runs under
any CPython from 3.11 and needs no project environment, which is what a fresh cloud
batch session has. From ``packing/``::

    python3 -m devtools.replay_evand_zmx2 build --checker 6b7f0f79 --work /tmp/zmx2
    python3 -m devtools.replay_evand_zmx2 run --case 77 --mode full --x 45-89 \\
        --work /tmp/zmx2 --out /tmp/zmx2/out --threads 4
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from devtools import replay_receipt

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
CRATE = WEB / "evand-square-packing-2026-09-26/square-packing/s12/verify2"
WAND125 = WEB / "wand125-point-and-mixed-2026-10-01/square-packing-bounds/certificates"

#: The crate files every checker version builds with: path in the crate, retained copy, SHA-256.
CRATE_FILES = (
    (
        "Cargo.toml",
        CRATE / "Cargo.toml",
        "4e0f078ea45b32802c21cb71413305e30cd062c3fa371c6ff6e62bda3d07a577",
    ),
    (
        "Cargo.lock",
        CRATE / "Cargo.lock",
        "e1daec4d9995e879ddbf4aa5fb89b6f03eaaa23157ef60feb72741e3a0ffa57e",
    ),
    (
        "src/main.rs",
        CRATE / "src/main.rs",
        "94b7d83ecf6aeea64c20aea9d4f5c210c28577fb3870581d79169204c980c12b",
    ),
)

#: ``zmx2.rs`` versions by the prefix of their SHA-256: the retained copy and the full digest.
CHECKERS = {
    "6b7f0f79": (
        WEB / "evand-square-packing-2026-09-28/square-packing/s12/verify2/src/bin/zmx2.rs",
        "6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed",
    ),
    "92a4cfe8": (
        WEB / "evand-zmx2-sym-atoms-2026-09-30/square-packing/s12/verify2/src/bin/zmx2.rs",
        "92a4cfe87b4e33d57ce132c9c517eded3fe62b4a5a2151b5ba250b8ee329fe64",
    ),
}


@dataclass(frozen=True, slots=True)
class Case:
    """One cover: where it is retained, its digest, and how its source ran ``zmx2``."""

    name: str
    cover: Path
    sha256: str
    checker: str
    flags: tuple[str, ...]
    #: Root cells per axis: the side over the centre pitch 1/10 (``full``); half in ``d4``.
    cells: int


CASES = {
    32: Case(
        "s32",
        WEB
        / "evand-square-packing-2026-09-26/square-packing/s12/certificates/s32"
        / "s32_closed_cover_6.txt.gz",
        "a0d2d38fc9a585a166b9e06c5069fdae9bdce44ca9fb64dda75abcc99e3c2144",
        "92a4cfe8",
        ("--pair-points", "--sym-atoms"),
        60,
    ),
    59: Case(
        "n59",
        WAND125 / "k2m5_n59_L8/n59_mixed_cover_8.txt.gz",
        "6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19",
        "6b7f0f79",
        (),
        80,
    ),
    60: Case(
        "s60",
        WEB
        / "evand-square-packing-2026-10-01/source/s12/certificates/s60"
        / "s60_mixed_cover_8.txt.gz",
        "2d0e456ea86cceeadc92d9f8fa7d468ba570a16d00d7343ebfbfb0b3b3b12a41",
        "6b7f0f79",
        (),
        80,
    ),
    77: Case(
        "n77",
        WAND125 / "k2m4_n77_L9/n77_mixed_cover_9.txt.gz",
        "47b57cfe38cbfdbcf5320e59caffe712f4ef32df8aad42b0d7f697de6d26cdd7",
        "6b7f0f79",
        ("--pair-points",),
        90,
    ),
}


class DigestError(RuntimeError):
    """A retained input does not have the SHA-256 the record states."""


def _checked(data: bytes, expected: str, what: str) -> bytes:
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise DigestError(f"{what}: SHA-256 {actual}, expected {expected}")
    return data


def _write_checked(target: Path, data: bytes) -> None:
    if target.exists() and target.read_bytes() == data:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def build(checker: str, work: Path) -> Path:
    """Assemble the crate for ``checker`` under ``work`` and build it; return the binary."""
    source, digest = CHECKERS[checker]
    crate = work / checker / "verify2"
    for relative, retained, expected in CRATE_FILES:
        _write_checked(
            crate / relative, _checked(retained.read_bytes(), expected, str(retained))
        )
    _write_checked(
        crate / "src/bin/zmx2.rs", _checked(source.read_bytes(), digest, str(source))
    )
    binary = crate / "target/release/zmx2"
    receipt = work / checker / "build.log"
    if binary.exists() and receipt.exists():
        return binary
    fields = replay_receipt.run(
        ["cargo", "build", "--release", "--bin", "zmx2"],
        receipt=receipt,
        cwd_label=(
            f"verify2/ assembled from retained bytes: zmx2.rs {digest} "
            f"({source.relative_to(REPO)}), Cargo.toml, Cargo.lock and src/main.rs "
            f"from {CRATE.relative_to(REPO)}"
        ),
        python_note="not used by this command",
        chdir=crate,
    )
    if fields["exit"] != 0:
        raise SystemExit(f"cargo build failed; see {receipt}")
    toolchain = subprocess.run(
        ["rustc", "--version"], capture_output=True, text=True, check=True
    ).stdout
    with receipt.open("a", encoding="utf-8") as out:
        out.write(f"# rustc: {toolchain.strip()}\n")
        out.write(f"# binary sha256: {hashlib.sha256(binary.read_bytes()).hexdigest()}\n")
    return binary


def root_span(text: str | None, cells: int) -> tuple[int, int]:
    if text is None:
        return 0, cells - 1
    low, _, high = text.partition("-")
    first, last = int(low), int(high)
    if not 0 <= first <= last < cells:
        raise SystemExit(f"region {text!r} is not within 0-{cells - 1}")
    return first, last


def run_case(
    n: int,
    mode: str,
    *,
    work: Path,
    out: Path,
    threads: int,
    x: str | None,
    y: str | None,
) -> int:
    """Run ``zmx2 cert`` on case ``n`` and return its exit status."""
    case = CASES[n]
    binary = build(case.checker, work)
    cells = case.cells if mode == "full" else case.cells // 2
    (x0, x1), (y0, y1) = root_span(x, cells), root_span(y, cells)
    stage = work / "s12"
    cover = stage / "certificates" / case.cover.name.removesuffix(".gz")
    data = gzip.decompress(case.cover.read_bytes())
    _write_checked(cover, _checked(data, case.sha256, f"{case.cover} (decompressed)"))
    link = stage / "verify2"
    if link.is_symlink() or link.exists():
        link.unlink() if link.is_symlink() else shutil.rmtree(link)
    link.symlink_to(binary.parents[2], target_is_directory=True)
    flags = "".join("_" + flag.strip("-").replace("-", "") for flag in case.flags)
    region = "" if (x is None and y is None) else f"_x{x0}-{x1}_y{y0}-{y1}"
    name = f"{case.name}_zmx2_{mode}{flags}{region}"
    roots = out / f"{name}_roots.log"
    receipt = out / f"{name}.log"
    resume = 0
    while receipt.exists():
        resume += 1
        receipt = out / f"{name}_resume{resume}.log"
    command = [
        "verify2/target/release/zmx2",
        "cert",
        f"certificates/{cover.name}",
        f"--{mode}",
        *case.flags,
        "--threads",
        str(threads),
        "--log",
        str(roots),
    ]
    if region:
        command += ["--xlo", str(x0), "--xhi", str(x1), "--ylo", str(y0), "--yhi", str(y1)]
    fields = replay_receipt.run(
        command,
        receipt=receipt,
        cwd_label=(
            f"s12/ staged by devtools.replay_evand_zmx2: zmx2.rs "
            f"{CHECKERS[case.checker][1]} built from retained bytes; cover {case.sha256} "
            f"decompressed from {case.cover.relative_to(REPO)}"
            + (f"; resumes the root log of {name}.log" if resume else "")
        ),
        python_note="not used by this command",
        chdir=stage,
    )
    return int(fields["exit"])  # type: ignore[call-overload]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="assemble and build one checker version")
    build_parser.add_argument("--checker", choices=sorted(CHECKERS), required=True)
    build_parser.add_argument("--work", type=Path, required=True)
    run_parser = commands.add_parser("run", help="replay one case's cover")
    run_parser.add_argument("--case", type=int, choices=sorted(CASES), required=True)
    run_parser.add_argument("--mode", choices=("d4", "full"), required=True)
    run_parser.add_argument("--work", type=Path, required=True)
    run_parser.add_argument("--out", type=Path, required=True)
    run_parser.add_argument("--threads", type=int, default=4)
    run_parser.add_argument("--x", help="root columns LO-HI (inclusive)")
    run_parser.add_argument("--y", help="root rows LO-HI (inclusive)")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            print(build(args.checker, args.work.resolve()))
            return 0
        return run_case(
            args.case,
            args.mode,
            work=args.work.resolve(),
            out=args.out.resolve(),
            threads=args.threads,
            x=args.x,
            y=args.y,
        )
    except DigestError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
