"""Audit the re-weighted s(12) certificate exactly, sharing no code with the tools that made it.

Lane BB of 2 October 2026 claims ``s(12) >= 15680000/3949423`` from Evan Daniel's 1,736
points (``s12_lower_3.9686.txt``, T-049) scaled by ``3951000/3949423`` and re-weighted by
linear programming, and ``s(12) >= 1568000/395039`` from the same file scaled whole
(after jlevy/squares#309). Coverage is the verifier's business; this tool decides
everything else the claim rests on, in integers and `Fraction`:

- the decompressed bytes' SHA-256 against ``claim.json``;
- the source format: positive header, exactly ``m`` point lines, nonnegative integer
  weights, every point in the closed container, ``s_den`` dividing ``s_num * D``;
- the total weight strictly below 12, and equal to the recorded fraction;
- the container side, and that it is Daniel's side times the recorded scale;
- the geometry: each point is Daniel's point, in file order, with both coordinates times
  1000, so only the denominator and the weights differ from T-049;
- the D4 invariance of the weighted multiset, which the verifier's ``[0, 45]`` reduction
  needs, and the number of orbits;
- for Route A, that the weights are Daniel's unchanged;
- the two mutation controls, rebuilt here from their descriptions in
  ``receipts/controls.json`` and matched to the digests recorded there.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.audit_s12_reweighted \\
        --output cases/n12_beyond_rescaling/receipts/review-audit.json

The tool exits 1 if any check fails, and the receipt lists every check either way.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
CASE = REPO / "packing/cases/n12_beyond_rescaling"
DANIEL = (
    REPO
    / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
    / "certificates/s12_lower_3.9686.txt"
)
DANIEL_SHA256 = "75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78"
MULTIPLIER = 1000
N_SQUARES = 12
#: Control 1 lowers the orbit of this point by 100/10^7; control 2 regrids to 3949000.
LOWERED = (3948000, 3134000, 100)
REGRID = 3949000


@dataclass(frozen=True, slots=True)
class Cert:
    s_num: int
    s_den: int
    d: int
    w: int
    points: tuple[tuple[int, int, int], ...]

    @property
    def side(self) -> Fraction:
        return Fraction(self.s_num, self.s_den)

    @property
    def total(self) -> Fraction:
        return Fraction(sum(p[2] for p in self.points), self.w)

    def to_bytes(self) -> bytes:
        lines = [f"{self.s_num} {self.s_den}", str(self.d), str(self.w), str(len(self.points))]
        lines += [f"{x} {y} {w}" for x, y, w in self.points]
        return ("\n".join(lines) + "\n").encode()


def parse(data: bytes) -> Cert:
    """The source's format, refusing what its verifier refuses."""
    tokens = data.split()
    if not tokens or not all(t.isdigit() for t in tokens):
        raise ValueError("not a file of nonnegative integers")
    v = [int(t) for t in tokens]
    if len(v) < 5 or min(v[:5]) <= 0:
        raise ValueError("header must be five positive integers")
    s_num, s_den, d, w, m = v[:5]
    if len(v) != 5 + 3 * m:
        raise ValueError("point count does not match the file")
    if (s_num * d) % s_den:
        raise ValueError("s_den does not divide s_num * D")
    pts = tuple((v[5 + 3 * i], v[6 + 3 * i], v[7 + 3 * i]) for i in range(m))
    return Cert(s_num, s_den, d, w, pts)


def units(c: Cert) -> int:
    """The container side in coordinate units, an integer for a well-formed file."""
    return c.s_num * c.d // c.s_den


def d4_images(x: int, y: int, u: int) -> set[tuple[int, int]]:
    return {
        (x, y), (u - x, y), (x, u - y), (u - x, u - y),
        (y, x), (u - y, x), (y, u - x), (u - y, u - x),
    }  # fmt: skip


def d4_invariant(c: Cert) -> bool:
    """The weighted multiset is fixed by both reflections and the diagonal, hence by D4."""
    u = units(c)
    base = sorted(c.points)
    maps = ((lambda x, y: (u - x, y)), (lambda x, y: (x, u - y)), (lambda x, y: (y, x)))
    return all(sorted((*f(x, y), w) for x, y, w in c.points) == base for f in maps)


def orbit_count(c: Cert) -> int:
    u = units(c)
    return len({min(d4_images(x, y, u)) for x, y, _ in c.points})


def lowered(c: Cert, x: int, y: int, by: int) -> Cert:
    orbit = d4_images(x, y, units(c))
    pts = tuple((px, py, w - by if (px, py) in orbit else w) for px, py, w in c.points)
    return Cert(c.s_num, c.s_den, c.d, c.w, pts)


def regridded(c: Cert, d: int) -> Cert:
    side = Fraction(units(c), d)
    return Cert(side.numerator, side.denominator, d, c.w, c.points)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def audit() -> tuple[list[dict[str, object]], dict[str, object]]:
    claim = json.loads((CASE / "claim.json").read_text(encoding="utf-8"))
    controls = json.loads((CASE / "receipts/controls.json").read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: object, *, ok: bool) -> None:
        checks.append({"check": name, "pass": bool(ok), "value": value})

    daniel_bytes = read_retained_bytes(DANIEL)
    digest = sha(daniel_bytes)
    check("Daniel's file is the reviewed T-049 release", digest, ok=digest == DANIEL_SHA256)
    daniel = parse(daniel_bytes)

    # Route B: the re-weighted certificate.
    data = gzip.decompress((CASE / "certificate.txt.gz").read_bytes())
    check("Route B digest", sha(data), ok=sha(data) == claim["certificate_sha256"])
    cert = parse(data)
    header = {"s": f"{cert.s_num}/{cert.s_den}", "D": cert.d, "W": cert.w}
    check("Route B parses: positive header, m lines, s_den | s_num*D", header, ok=True)
    check("Route B bytes are the canonical rendering", len(data), ok=cert.to_bytes() == data)
    weights = [w for *_, w in cert.points]
    zero = sum(1 for w in weights if w == 0)
    check("weights are nonnegative integers over W", {"zero": zero}, ok=min(weights) >= 0)
    u = units(cert)
    inside = all(0 <= x <= u and 0 <= y <= u for x, y, _ in cert.points)
    check("every point in the closed container", {"side_units": u}, ok=inside)
    total = cert.total
    check("total is the recorded fraction", str(total), ok=str(total) == claim["total_weight"])
    gap = {"total": str(total), "gap": str(N_SQUARES - total)}
    check("total weight < 12", gap, ok=total < N_SQUARES)
    check(
        "container is the claimed side", str(cert.side), ok=str(cert.side) == claim["container"]
    )
    scale = Fraction(MULTIPLIER * daniel.d, cert.d)
    check(
        "container is Daniel's side times the scale",
        str(scale),
        ok=cert.side == daniel.side * scale,
    )
    check(
        "points are Daniel's, in order, times 1000",
        len(cert.points),
        ok=_same_points(cert, daniel),
    )
    check("weighted multiset is D4-invariant", orbit_count(cert), ok=d4_invariant(cert))
    changed = sum(1 for p, q in zip(cert.points, daniel.points, strict=True) if p[2] != q[2])
    facts: dict[str, object] = {
        "points": len(cert.points),
        "orbits": orbit_count(cert),
        "zero_weight_points": zero,
        "weights_changed_from_daniel": changed,
        "daniel_total": str(daniel.total),
        "total": str(total),
        "side": str(cert.side),
        "side_decimal": f"{float(cert.side):.10f}",
        "daniel_side_decimal": f"{float(daniel.side):.10f}",
    }

    # Route A: the whole-certificate rescaling.
    route_a = claim["route_a"]
    adata = gzip.decompress((CASE / "rescaled-certificate.txt.gz").read_bytes())
    check("Route A digest", sha(adata), ok=sha(adata) == route_a["certificate_sha256"])
    acert = parse(adata)
    claimed = f"s(12) >= {acert.side}" == route_a["claim"]
    check("Route A container is the claimed side", str(acert.side), ok=claimed)
    unchanged = acert.w == daniel.w and all(
        p[2] == q[2] for p, q in zip(acert.points, daniel.points, strict=True)
    )
    check(
        "Route A is Daniel's file, times 1000, weights unchanged",
        str(acert.total),
        ok=_same_points(acert, daniel) and unchanged,
    )
    ua = units(acert)
    a_inside = all(0 <= x <= ua and 0 <= y <= ua for x, y, _ in acert.points)
    check(
        "Route A is D4-invariant and in the container", ua, ok=d4_invariant(acert) and a_inside
    )

    # The controls, rebuilt here and matched to the recorded digests.
    ctl = {c["name"]: c["certificate_sha256"] for c in controls["controls"]}
    one = lowered(cert, *LOWERED)
    moved = sum(1 for p, q in zip(one.points, cert.points, strict=True) if p != q)
    one_facts = {
        "sha256": sha(one.to_bytes()),
        "total": str(one.total),
        "points_lowered": moved,
    }
    check(
        "control 1 (lowered orbit) rebuilt here matches the recorded digest",
        one_facts,
        ok=sha(one.to_bytes()) == ctl["lowered orbit"] and d4_invariant(one),
    )
    two = regridded(cert, REGRID)
    two_facts = {"sha256": sha(two.to_bytes()), "side": str(two.side)}
    check(
        "control 2 (one step larger) rebuilt here matches the recorded digest",
        two_facts,
        ok=sha(two.to_bytes()) == ctl["one step larger"],
    )
    return checks, facts


def _same_points(cert: Cert, daniel: Cert) -> bool:
    return len(cert.points) == len(daniel.points) and all(
        (x, y) == (MULTIPLIER * dx, MULTIPLIER * dy)
        for (x, y, _), (dx, dy, _) in zip(cert.points, daniel.points, strict=True)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--control-dir", type=Path, help="also write both controls here")
    args = parser.parse_args()
    checks, facts = audit()
    if args.control_dir is not None:
        args.control_dir.mkdir(parents=True, exist_ok=True)
        cert = parse(gzip.decompress((CASE / "certificate.txt.gz").read_bytes()))
        (args.control_dir / "ctl1.txt").write_bytes(lowered(cert, *LOWERED).to_bytes())
        (args.control_dir / "ctl2.txt").write_bytes(regridded(cert, REGRID).to_bytes())
    ok = all(c["pass"] for c in checks)
    receipt = {
        "schema": "S12ReweightedAudit/v1",
        "status": "PASS" if ok else "FAIL",
        "tool": "devtools.audit_s12_reweighted",
        "relationship_to_generator": "independent-implementation",
        "facts": facts,
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    for c in checks:
        print(("PASS " if c["pass"] else "FAIL ") + str(c["check"]))
    print(receipt["status"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
