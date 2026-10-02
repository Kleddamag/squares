"""Rescale evand's s(12) certificate and decide it with the source's own verifier.

Evan Daniel's certificate ``s12_lower_3.9686.txt`` proves ``s(12) >= 15680/3951`` with 1,736
weighted points. Scaling the picture by ``lambda`` keeps the integer coordinates and divides
the denominator by ``lambda``, so in the source's text format a scale ``m*3951/D'`` is the
file with every coordinate multiplied by ``m``, coordinate denominator ``D'``, and container
``15680*m/D'``. The weights, and so the total, do not change.

The scaled file still has to cover every closed unit square in the larger container, and
that is decided by the source's arrangement sweep, ``verify/`` in the retained packet, over
the net ``theta_k = 2 arctan(k/N)``. For bin ``k`` it tests the concentric square of side
``sigma_k = 1/(cos d + sin d)`` (``d`` the bin's gap, rounded down to ``10^-6``), which every
unit square at an angle of the bin contains. The net costs ``1 - sigma_k``, about ``2/N``,
of the certificate's slack: jlevy/squares#309 found the scale ``7902/7901`` refused at
``N = 6000`` and ``12000`` and verified at ``24000``. A finer net leaves more slack for the
scale, and this tool searches it.

It never edits the source. ``build`` copies the retained ``verify/`` crate into a scratch
directory and builds it with ``cargo build --release --locked``, once as the source ships it
and once with ``overflow-checks`` on, so an ``i128`` overflow at a fine net or a large
denominator would abort rather than wrap. The two binaries' digests go in every receipt.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.s12_angle_net_rescale \\
        build --work WORK
    ... write --multiplier 100 --denominator 395040 --output CERT.txt
    ... screen --work WORK --certificate CERT.txt --net 96000 --stride 16 --workers 4
    ... verify --work WORK --certificate CERT.txt --net 96000 --threads 4 --output R.json

``screen`` sweeps every ``stride``-th bin, one bin per process, and is only a filter: it
says where a scale fails, never that it holds. ``verify`` is the complete sweep, and its
receipt says ``VERIFIED`` only when the source's verifier printed its verdict for the whole
range with no ``PARTIAL`` marker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
SOURCE_CERTIFICATE = PACKET / "certificates/s12_lower_3.9686.txt"
SOURCE_SHA256 = "75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78"
SOURCE_URL = "https://github.com/evand/square-packing"
SOURCE_COMMIT = "167d842cd27ba1451cb2833773ea930c80b9e65b"
#: The bound #309 records, and the one a candidate here has to beat strictly.
RESCALED_309 = Fraction(31360, 7901)

_MIN_RE = re.compile(
    r"min covered weight over ALL placements = (-?\d+)/(\d+) = \S+\s+\(at angle k=(\d+)\)"
)
_ANGLES_RE = re.compile(r"angles: k=0\.\.(\d+) \(N=(\d+)\)")


@dataclass(frozen=True, slots=True)
class Certificate:
    """The source's text format: ``s_num s_den D W m`` and ``m`` lines ``X Y w``."""

    s_num: int
    s_den: int
    denominator: int
    weight_scale: int
    points: tuple[tuple[int, int, int], ...]

    @property
    def side(self) -> Fraction:
        return Fraction(self.s_num, self.s_den)

    @property
    def total_weight(self) -> Fraction:
        return Fraction(sum(w for _, _, w in self.points), self.weight_scale)

    def text(self) -> str:
        header = (
            (self.s_num, self.s_den),
            (self.denominator,),
            (self.weight_scale,),
            (len(self.points),),
        )
        head = "".join(" ".join(map(str, line)) + "\n" for line in header)
        return head + "".join(f"{x} {y} {w}\n" for x, y, w in self.points)


def parse_certificate(data: bytes) -> Certificate:
    tokens = data.split()
    if not tokens or not all(t.isdigit() for t in tokens):
        raise ValueError("the text format holds nonnegative integers only")
    values = [int(t) for t in tokens]
    if len(values) < 5:
        raise ValueError("truncated header")
    s_num, s_den, denominator, weight_scale, count = values[:5]
    if min(s_num, s_den, denominator, weight_scale, count) <= 0:
        raise ValueError("nonpositive header value")
    if len(values) != 5 + 3 * count:
        raise ValueError("point count does not match the file")
    points = tuple(
        (values[5 + 3 * i], values[6 + 3 * i], values[7 + 3 * i]) for i in range(count)
    )
    return Certificate(s_num, s_den, denominator, weight_scale, points)


def load_source() -> Certificate:
    """Daniel's shipped certificate, refusing any bytes but the reviewed release."""
    data = read_retained_bytes(SOURCE_CERTIFICATE)
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("certificate bytes differ from the reviewed evand release")
    return parse_certificate(data)


def rescale(cert: Certificate, multiplier: int, denominator: int) -> Certificate:
    """Coordinates times ``multiplier`` over ``denominator``: the scale ``multiplier*D/D'``.

    The container keeps its coordinate count, ``side*D``, so it becomes
    ``side*D*multiplier/D'``, written in lowest terms the way the source writes its own.
    """
    if multiplier <= 0 or denominator <= 0:
        raise ValueError("multiplier and denominator must be positive")
    units = cert.side * cert.denominator
    if units.denominator != 1:
        raise ValueError("container is off the coordinate grid")
    side = Fraction(int(units) * multiplier, denominator)
    points = tuple((x * multiplier, y * multiplier, w) for x, y, w in cert.points)
    return Certificate(side.numerator, side.denominator, denominator, cert.weight_scale, points)


def scale_factor(cert: Certificate, multiplier: int, denominator: int) -> Fraction:
    return Fraction(multiplier * cert.denominator, denominator)


@dataclass(frozen=True, slots=True)
class Verdict:
    """What the source's verifier printed, parsed and nothing inferred."""

    verified: bool
    partial: bool
    least_weight: str | None
    least_bin: int | None
    last_bin: int | None
    net: int | None
    exit_code: int


def parse_output(stdout: str, exit_code: int) -> Verdict:
    found = _MIN_RE.search(stdout)
    angles = _ANGLES_RE.search(stdout)
    partial = "PARTIAL RUN" in stdout
    lines = stdout.splitlines()
    verified = (
        exit_code == 0
        and not partial
        and any(line.startswith("VERIFIED:") for line in lines)
        and not any(line.strip() == "NOT VERIFIED" for line in lines)
    )
    return Verdict(
        verified=verified,
        partial=partial,
        least_weight=None if found is None else f"{found.group(1)}/{found.group(2)}",
        least_bin=None if found is None else int(found.group(3)),
        last_bin=None if angles is None else int(angles.group(1)),
        net=None if angles is None else int(angles.group(2)),
        exit_code=exit_code,
    )


def bin_count(net: int) -> int:
    """Bins the source sweeps for a D4-symmetric set: ``k`` with ``(k+N)^2 < 2 N^2``."""
    k = 0
    while (k + net) * (k + net) < 2 * net * net:
        k += 1
    return k


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(work: Path) -> dict[str, str]:
    """Build the retained ``verify/`` crate twice, as shipped and with overflow checks."""
    crate = work / "verify"
    if crate.exists():
        shutil.rmtree(crate)
    shutil.copytree(PACKET / "verify", crate)
    binaries: dict[str, str] = {}
    for name, checks in (("shipped", "false"), ("overflow-checked", "true")):
        target = work / f"target-{name}"
        env = dict(os.environ, CARGO_PROFILE_RELEASE_OVERFLOW_CHECKS=checks)
        subprocess.run(
            ["cargo", "build", "--release", "--locked", "--target-dir", str(target)],
            cwd=crate,
            env=env,
            check=True,
            capture_output=True,
        )
        binary = target / "release/verify"
        binaries[name] = str(binary)
        binaries[f"{name}_sha256"] = _sha256(binary)
    return binaries


def binary_path(work: Path, *, overflow_checked: bool) -> Path:
    name = "overflow-checked" if overflow_checked else "shipped"
    path = work / f"target-{name}/release/verify"
    if not path.exists():
        raise FileNotFoundError(f"{path}: run `build --work {work}` first")
    return path


def run_verifier(
    binary: Path,
    certificate: Path,
    net: int,
    *,
    threads: int,
    bins: tuple[int, int] | None = None,
    n: int = 12,
    extra_env: dict[str, str] | None = None,
) -> tuple[Verdict, str]:
    env = dict(os.environ)
    for name in ("VERIFY_BINS", "TIGHT_DUMP", "TIGHT_THRESH", "TIGHT_MAX", "VERIFY_FULLSWEEP"):
        env.pop(name, None)
    env.update(extra_env or {})
    if bins is not None:
        env["VERIFY_BINS"] = f"{bins[0]}:{bins[1]}"
    done = subprocess.run(
        [str(binary), str(certificate), str(n), str(net), str(threads)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    return parse_output(done.stdout, done.returncode), done.stdout + done.stderr


def screen(
    binary: Path, certificate: Path, net: int, *, stride: int, workers: int, offset: int = 0
) -> dict[str, Any]:
    """Every ``stride``-th bin, one per process: a filter that can refuse, never accept."""
    last = bin_count(net)
    chosen = list(range(offset, last, stride))

    def one(k: int) -> tuple[int, Verdict]:
        verdict, _ = run_verifier(binary, certificate, net, threads=1, bins=(k, k))
        return k, verdict

    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, chosen))
    failing = [
        (k, v.least_weight)
        for k, v in results
        if v.least_weight is None or Fraction(v.least_weight) < 1
    ]
    least = min(results, key=lambda kv: Fraction(kv[1].least_weight or "-1"))
    return {
        "net": net,
        "stride": stride,
        "offset": offset,
        "bins_screened": len(chosen),
        "failing_bins": len(failing),
        "first_failures": failing[:20],
        "least": {"bin": least[0], "weight": least[1].least_weight},
        "seconds": time.monotonic() - started,
    }


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def verify(
    work: Path, certificate: Path, net: int, *, threads: int, overflow_checked: bool
) -> dict[str, Any]:
    cert = parse_certificate(certificate.read_bytes())
    binary = binary_path(work, overflow_checked=overflow_checked)
    started = time.monotonic()
    verdict, output = run_verifier(binary, certificate, net, threads=threads)
    seconds = time.monotonic() - started
    margin = None if verdict.least_weight is None else str(Fraction(verdict.least_weight) - 1)
    return {
        "schema": "S12AngleNetRescaleReceipt/v1",
        "status": "VERIFIED" if verdict.verified else "NOT_VERIFIED",
        "verifier": "evand/square-packing s12/verify (the producer's arrangement sweep), "
        "built from the retained source",
        "binary": "overflow-checked" if overflow_checked else "shipped",
        "binary_sha256": _sha256(binary),
        "certificate_sha256": _sha256(certificate),
        "container": str(cert.side),
        "total_weight": str(cert.total_weight),
        "points": len(cert.points),
        "net": net,
        "bins": verdict.last_bin,
        "least_weight": verdict.least_weight,
        "least_bin": verdict.least_bin,
        "margin": margin,
        "verdict": asdict(verdict),
        "stdout_tail": output.strip().splitlines()[-6:],
        "threads": threads,
        "wall_seconds": round(seconds, 1),
        "provenance": {
            "git_commit": _git("rev-parse", "HEAD"),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "cpus": os.cpu_count(),
            "source_url": SOURCE_URL,
            "source_commit": SOURCE_COMMIT,
            "command": sys.argv,
        },
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as handle:
        handle.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build", help="build the source verifier, shipped and overflow-checked")
    b.add_argument("--work", type=Path, required=True)
    w = sub.add_parser("write", help="write the source certificate rescaled")
    w.add_argument("--multiplier", type=int, required=True)
    w.add_argument("--denominator", type=int, required=True)
    w.add_argument("--output", type=Path, required=True)
    s = sub.add_parser("screen", help="sweep every stride-th bin; can only refuse")
    s.add_argument("--work", type=Path, required=True)
    s.add_argument("--certificate", type=Path, required=True)
    s.add_argument("--net", type=int, required=True)
    s.add_argument("--stride", type=int, default=16)
    s.add_argument("--offset", type=int, default=0)
    s.add_argument("--workers", type=int, default=4)
    v = sub.add_parser("verify", help="the complete sweep, with a receipt")
    v.add_argument("--work", type=Path, required=True)
    v.add_argument("--certificate", type=Path, required=True)
    v.add_argument("--net", type=int, required=True)
    v.add_argument("--threads", type=int, default=4)
    v.add_argument("--overflow-checked", action="store_true")
    v.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "build":
        args.work.mkdir(parents=True, exist_ok=True)
        print(json.dumps(build(args.work), indent=2))
    elif args.command == "write":
        source = load_source()
        scaled = rescale(source, args.multiplier, args.denominator)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(scaled.text(), encoding="ascii")
        factor = scale_factor(source, args.multiplier, args.denominator)
        print(
            f"scale {factor} -> container {scaled.side} = {float(scaled.side):.9f}; "
            f"above #309's {RESCALED_309}: {scaled.side > RESCALED_309}"
        )
    elif args.command == "screen":
        binary = binary_path(args.work, overflow_checked=False)
        result = screen(
            binary,
            args.certificate,
            args.net,
            stride=args.stride,
            workers=args.workers,
            offset=args.offset,
        )
        print(json.dumps(result, indent=2))
    else:
        receipt = verify(
            args.work,
            args.certificate,
            args.net,
            threads=args.threads,
            overflow_checked=args.overflow_checked,
        )
        _write_json(args.output, receipt)
        least = f"least {receipt['least_weight']} at bin {receipt['least_bin']}"
        print(f"{receipt['status']}: {least}")
        return 0 if receipt["status"] == "VERIFIED" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
