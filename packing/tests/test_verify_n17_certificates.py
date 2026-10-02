"""The standing certificate verifiers pass sound certificates and refuse doctored ones."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import math
import random
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from fractions import Fraction as Q
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import pilot_n17_subpattern_bb as bb
from devtools import verify_n17_bb_certificate as bb_verifier
from devtools import verify_n17_kernel_certificate as kernel_verifier
from devtools.check_n17_subpattern import save_certificate
from sqpack.hull_kernel import Budget, producer
from sqpack.hull_kernel.frame import make_frame

PACKING = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    "sqpack.hull_kernel",
    "devtools.check_n17_subpattern",
    "devtools.pilot_n17_subpattern_bb",
    "devtools.select_n17_sub_patterns",
    "scipy.optimize",
)


def canonical(document: Any) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def cells_file(directory: Path, cap: Q, names: list[str], polygons: list[Any]) -> Path:
    path = directory / "cells.json"
    document = {
        "U": str(cap),
        "order": names,
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in zip(names, polygons, strict=True)
        },
    }
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# The kernel verifier, on the blind pair of test_hull_kernel_sequential
# ---------------------------------------------------------------------------

TRIANGLE = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
SHIFTED = [(x + Q(1, 100), y) for x, y in TRIANGLE]


@cache
def blind_pair_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    """The two near-equilateral cells whose closure needs collision alone, produced once."""
    frame = make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[TRIANGLE, SHIFTED],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )
    budget = Budget(time.monotonic() + 60, 200_000)
    production = producer.produce(frame, [0, 1], bins=16, max_rounds=2, budget=budget)
    return production.seed, production.node


def blind_pair(tmp_path: Path, edit: Callable[[dict[str, Any]], None] | None = None) -> Path:
    """The saved closure under `tmp_path/cert`, its node edited and re-named if asked."""
    seed, node = blind_pair_objects()
    if edit is not None:
        node = copy.deepcopy(node)
        edit(node)
    save_certificate(tmp_path / "cert", seed, node)
    return tmp_path / "cert"


def blind_cells(tmp_path: Path) -> kernel_verifier.Cells:
    path = cells_file(tmp_path, Q(3), ["left", "right"], [TRIANGLE, SHIFTED])
    return kernel_verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


def test_the_kernel_verifier_passes_the_blind_pair(tmp_path: Path) -> None:
    receipt = kernel_verifier.verify(blind_pair(tmp_path), blind_cells(tmp_path))
    assert receipt["status"] == "PASS", receipt["failure"]
    assert receipt["mode"] == "full"
    assert receipt["closure"]["kind"] == "all_parent_poses_forbidden"
    assert receipt["counts"]["collision_regions"] > 0
    assert receipt["verifier_sha256"] == kernel_verifier.MODULE_SHA256
    seed, node = blind_pair_objects()
    assert receipt["certificate"] == {
        "seed_sha256": hashlib.sha256(canonical(seed)).hexdigest(),
        "node_sha256": hashlib.sha256(canonical(node)).hexdigest(),
    }
    sampled = kernel_verifier.verify(blind_pair(tmp_path), blind_cells(tmp_path), sample=1)
    assert sampled["status"] == "PASS"
    assert sampled["mode"] == "sample"


def collision_row(node: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in node["steps"][-1]["rows"] if row["collision_regions"])


def shift_region(node: dict[str, Any]) -> None:
    region = collision_row(node)["collision_regions"][0]
    region["vertices"] = [[str(Q(x) + Q(1, 2)), y] for x, y in region["vertices"]]


def shrink_partner_domain(node: dict[str, Any]) -> None:
    covers = node["steps"][-1]["prior_partner_pose_covers"]
    live = next(item for items in covers.values() for item in items if item["domain"])
    live["domain"] = live["domain"][:1]


def drop_residual_claim(node: dict[str, Any]) -> None:
    node["closed"] = False


def drop_collision_region(node: dict[str, Any]) -> None:
    collision_row(node)["collision_regions"] = []


@pytest.mark.parametrize(
    ("edit", "message"),
    [
        (shift_region, "escapes"),
        (shrink_partner_domain, "domain"),
        (drop_residual_claim, "closed flags"),
        (drop_collision_region, "NOT covered"),
    ],
)
def test_the_kernel_verifier_refuses_a_doctored_closure(
    tmp_path: Path, edit: Callable[[dict[str, Any]], None], message: str
) -> None:
    receipt = kernel_verifier.verify(blind_pair(tmp_path, edit), blind_cells(tmp_path))
    assert receipt["status"] == "FAIL"
    assert message in receipt["failure"]


def test_the_kernel_verifier_refuses_bytes_that_do_not_match_their_name(
    tmp_path: Path,
) -> None:
    directory = blind_pair(tmp_path)
    saved = next(directory.glob("node-*.json.gz"))
    raw = gzip.decompress(saved.read_bytes())
    saved.write_bytes(gzip.compress(raw.replace(b'"closed":true', b'"closed":false')))
    receipt = kernel_verifier.verify(directory, blind_cells(tmp_path))
    assert receipt["status"] == "FAIL"
    assert "digest" in receipt["failure"]
    with pytest.raises(kernel_verifier.VerificationError, match="digest"):
        _ = kernel_verifier.file_cells(tmp_path / "cells.json", "0" * 64)


# ---------------------------------------------------------------------------
# The kernel verifier's integer forms, against its Fraction forms
# ---------------------------------------------------------------------------

Point = tuple[Q, Q]


def convex_polygon(rng: random.Random, vertices: int) -> list[Point]:
    """A random convex polygon with at least three hull vertices, on a coarse grid."""
    while True:
        points = [
            (Q(rng.randint(-20, 20), 64), Q(rng.randint(-20, 20), 64)) for _ in range(vertices)
        ]
        found = kernel_verifier.hull(points)
        if len(found) >= 3:
            return found


def encode(polygon: list[Point]) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in polygon]


def homogeneous(polygon: list[Point]) -> tuple[kernel_verifier.HPoint, ...]:
    return tuple(kernel_verifier.homogeneous(v) for v in polygon)


def canonical_plane(a: Q, b: Q, c: Q) -> tuple[int, int, Q]:
    """`a x + b y <= c` with an integer normal in lowest terms, for comparing facet sets."""
    scale = math.lcm(a.denominator, b.denominator)
    ai, bi = int(a * scale), int(b * scale)
    g = math.gcd(ai, bi)
    return ai // g, bi // g, c * scale / g


SQUARE = [(Q(-1, 4), Q(-1, 4)), (Q(1, 4), Q(-1, 4)), (Q(1, 4), Q(1, 4)), (Q(-1, 4), Q(1, 4))]


def test_difference_facets_are_the_hull_facets() -> None:
    rng = random.Random(7)
    pairs = [(SQUARE, [(x / 2, y / 2) for x, y in SQUARE])]
    pairs.extend(
        (convex_polygon(rng, 3 + rng.randrange(5)), convex_polygon(rng, 3 + rng.randrange(4)))
        for _ in range(40)
    )
    for partner, core in pairs:
        difference = kernel_verifier.minkowski_diff(partner, core)
        reference = {
            canonical_plane(a, b, c) for a, b, c in kernel_verifier.planes_of(difference)
        }
        facets = kernel_verifier.difference_facets(homogeneous(partner), homogeneous(core))
        assert {(nx, ny, Q(hn, hd)) for nx, ny, hn, hd in facets} == reference
        assert len(facets) == len(reference)


def tiling(rng: random.Random, domain: list[Point], cuts: int) -> list[list[Point]]:
    """The domain cut by random lines into convex pieces that cover it exactly."""
    pieces = [domain]
    for _ in range(cuts):
        a, b = Q(rng.randint(-5, 5)), Q(rng.randint(-5, 5))
        if a == 0 and b == 0:
            continue
        inside = rng.choice(domain)
        c = a * inside[0] + b * inside[1] + Q(rng.randint(-3, 3), 128)
        out: list[list[Point]] = []
        for piece in pieces:
            for sign in (1, -1):
                part = kernel_verifier.clip_closed(piece, sign * a, sign * b, sign * c)
                if len(part) >= 3 and kernel_verifier.area2(part) > 0:
                    out.append(kernel_verifier.hull(part))
        pieces = out
    return pieces


def shifted(polygon: list[Point], dx: Q) -> list[Point]:
    return kernel_verifier.hull([(x + dx, y) for x, y in polygon])


def test_the_sweep_agrees_with_the_area_cover() -> None:
    rng = random.Random(11)
    verdicts: set[bool] = set()
    rectangle = [(Q(0), Q(0)), (Q(2), Q(0)), (Q(2), Q(1)), (Q(0), Q(1))]
    for trial in range(48):
        domain = rectangle if trial % 6 == 0 else convex_polygon(rng, 4 + rng.randrange(4))
        regions = tiling(rng, domain, 1 + rng.randrange(4))
        kind = trial % 4
        if kind == 1 and len(regions) > 1:
            regions.pop(rng.randrange(len(regions)))
        elif kind == 2:
            index = rng.randrange(len(regions))
            regions[index] = shifted(regions[index], Q(1, 2**30))
        elif kind == 3:
            regions.extend(convex_polygon(rng, 3 + rng.randrange(3)) for _ in range(2))
            regions.append([(Q(0), Q(0)), (Q(1), Q(0))])
        rng.shuffle(regions)
        by_area = kernel_verifier.covered_by_area(domain, regions)[0]
        by_sweep, probe = kernel_verifier.covered_by_sweep(domain, regions)
        assert by_sweep == by_area, (trial, probe)
        assert (probe is None) == by_sweep
        verdicts.add(by_area)
    assert verdicts == {True, False}


def test_between_lies_strictly_inside_with_small_terms() -> None:
    rng = random.Random(3)
    pairs: list[tuple[tuple[int, int], tuple[int, int]]] = [
        ((10**60, 3 * 10**60 + 1), (10**60 + 1, 3 * 10**60 + 1)),
        ((-7, 2), (-3, 1)),
        ((0, 1), (1, 10**9)),
    ]
    while len(pairs) < 200:
        a = (rng.randint(-(10**6), 10**6), rng.randint(1, 10**6))
        b = (rng.randint(-(10**6), 10**6), rng.randint(1, 10**6))
        if kernel_verifier.ratio_lt(a, b):
            pairs.append((a, b))
    for a, b in pairs:
        n, d = kernel_verifier.between(a, b)
        assert d > 0
        assert kernel_verifier.ratio_lt(a, (n, d))
        assert kernel_verifier.ratio_lt((n, d), b)
        assert d <= a[1] + b[1]


def unit_cell() -> list[Point]:
    return [(Q(1), Q(1)), (Q(2), Q(1)), (Q(2), Q(2)), (Q(1), Q(2))]


def cover_state() -> tuple[kernel_verifier.State, kernel_verifier.Row, dict[str, Any]]:
    """A state with one partner row whose published cover is sound."""
    state = kernel_verifier.State(
        cells=[unit_cell(), unit_cell()], cap=Q(3), bins=1, mask=[0, 1]
    )
    residual = kernel_verifier.hull(
        [(Q(1), Q(1)), (Q(3, 2), Q(1)), (Q(3, 2), Q(3, 2)), (Q(1), Q(3, 2))]
    )
    row = kernel_verifier.Row(
        (Q(0), Q(1)), {"kind": "wall_seed", "owner": 1, "row": 0}, residual, [residual]
    )
    state.rows[1] = [row]
    item = {
        "reference": row.reference,
        "interval": ["0", "1"],
        "domain": encode(residual),
        "core": encode(SQUARE),
    }
    return state, row, item


def step_with(item: dict[str, Any]) -> dict[str, Any]:
    return {"owner": 0, "prior_partner_pose_covers": {"1": [item]}}


def test_a_republished_partner_cover_is_reused_only_when_identical() -> None:
    state, row, item = cover_state()
    partners = kernel_verifier.check_partners(state, step_with(item), 0)
    admitted = partners[1][0]
    assert row.cover is admitted
    again = kernel_verifier.check_partners(state, step_with(copy.deepcopy(item)), 1)
    assert again[1][0] is admitted
    assert state.stats["partner_rows"] == 2
    shrunk = copy.deepcopy(item)
    shrunk["domain"] = shrunk["domain"][:3]
    with pytest.raises(kernel_verifier.VerificationError, match="domain"):
        _ = kernel_verifier.check_partners(state, step_with(shrunk), 2)
    wide = copy.deepcopy(item)
    wide["core"] = encode([(2 * x, 2 * y) for x, y in SQUARE])
    with pytest.raises(kernel_verifier.VerificationError, match="core not strict"):
        _ = kernel_verifier.check_partners(state, step_with(wide), 3)
    assert row.cover is admitted
    replaced = kernel_verifier.hull(
        [(Q(1), Q(1)), (Q(5, 4), Q(1)), (Q(5, 4), Q(5, 4)), (Q(1), Q(5, 4))]
    )
    state.rows[1] = [kernel_verifier.Row(row.interval, row.reference, replaced, [replaced])]
    with pytest.raises(kernel_verifier.VerificationError, match="domain"):
        _ = kernel_verifier.check_partners(state, step_with(item), 4)
    assert state.rows[1][0].cover is None


def test_the_facet_cache_keys_on_the_exact_cores() -> None:
    state = kernel_verifier.State(cells=[], cap=Q(3), bins=1, mask=[])
    partner = homogeneous(unit_cell())
    core = homogeneous(SQUARE)
    moved = homogeneous([(x + Q(1, 2**40), y) if x > 0 else (x, y) for x, y in SQUARE])
    first = state.difference(partner, core)
    second = state.difference(partner, moved)
    assert state.difference(partner, core) is first
    assert second == kernel_verifier.difference_facets(partner, moved)
    assert first != second
    assert len(state.facets) == 2


# ---------------------------------------------------------------------------
# The branch-and-bound verifier, on the three-in-a-row round trip of P2's tests
# ---------------------------------------------------------------------------


def rectangle(x0: str, x1: str) -> tuple[tuple[Q, Q], ...]:
    a, b, c, d = Q(x0), Q(x1), Q("2.00"), Q("2.05")
    return ((a, c), (b, c), (b, d), (a, d))


ROW = ("left", "middle", "right")
ROW_CELLS = (rectangle("1.00", "1.05"), rectangle("1.40", "2.40"), rectangle("2.80", "2.85"))


@pytest.fixture(scope="module")
def row_certificates(tmp_path_factory: pytest.TempPathFactory) -> dict[int, Path]:
    """The crowded row's certificates without and with bound tightening, made once."""
    made: dict[int, Path] = {}
    pattern = bb.Pattern(ROW, ROW_CELLS, bb.cover.U)
    for obbt_rounds in (0, 3):
        directory = tmp_path_factory.mktemp(f"row-obbt{obbt_rounds}")
        settings = bb.Settings(obbt_rounds=obbt_rounds)
        result = bb.search(pattern, settings, certificate=directory)
        assert result["verdict"] == "certified-infeasible"
        made[obbt_rounds] = directory
    return made


def row_cells(tmp_path: Path) -> bb_verifier.Cells:
    path = cells_file(tmp_path, bb.cover.U, list(ROW), list(ROW_CELLS))
    return bb_verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


@pytest.mark.parametrize("obbt_rounds", [0, 3])
def test_the_bb_verifier_passes_the_round_trip_certificate(
    tmp_path: Path, row_certificates: dict[int, Path], obbt_rounds: int
) -> None:
    receipt = bb_verifier.verify_certificate(row_certificates[obbt_rounds], row_cells(tmp_path))
    assert receipt["status"] == "PASS", receipt["failures"]
    assert receipt["mode"] == "full"
    assert receipt["checked_nodes"] == receipt["nodes"] > 1
    assert receipt["pattern"] == list(ROW)
    assert receipt["verifier_sha256"] == bb_verifier.MODULE_SHA256


def read_named(directory: Path, name: str) -> Any:
    return json.loads(gzip.decompress((directory / f"{name}.json.gz").read_bytes()))


def write_named(directory: Path, document: Any) -> str:
    data = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    name = hashlib.sha256(data.encode()).hexdigest()
    (directory / f"{name}.json.gz").write_bytes(gzip.compress(data.encode(), mtime=0))
    return name


def rational(q: Q) -> str:
    return f"{q.numerator}/{q.denominator}"


def first_round(nodes: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
    return next((r for n in nodes for r in n["rounds"] if r.get(key)), None)


def corrupt(directory: Path, kind: str) -> str | None:
    """R4's corruptions (`audit-A/corrupt_cert.py.txt`): one change, re-hashed; the manifest.

    None when the certificate has no record of the kind.
    """
    manifest = read_named(directory, bb_verifier.manifest_from_readme(directory))
    chunks = [read_named(directory, c)["nodes"] for c in manifest["chunks"]]
    nodes = [n for chunk in chunks for n in chunk]
    nudge = Q(1, 10**9)
    if kind == "cut_v":
        record = next(
            (
                r
                for n in nodes
                for r in n["rounds"]
                if any(f[0][0] == "u" for f in r.get("farkas", []))
            ),
            None,
        )
        if record is None:
            return None
        ref = next(f[0] for f in record["farkas"] if f[0][0] == "u")
        cut = record["cuts"][ref[1]]
        cut[3] = rational(Q(cut[3]) + nudge)
    elif kind == "farkas_y":
        record = first_round(nodes, "farkas")
        if record is None:
            return None
        record["farkas"][0][1] = rational(-Q(record["farkas"][0][1]))
    elif kind == "bound":
        record = first_round(nodes, "bounds")
        if record is None:
            return None
        record["bounds"][0][2] = rational(Q(record["bounds"][0][2]) + nudge)
    elif kind == "box":
        node = next(n for n in nodes if n["rounds"])
        node["rounds"][0]["boxes"][0][0] = rational(Q(node["rounds"][0]["boxes"][0][0]) + nudge)
    elif kind == "lost_child":
        leaf = next(n for n in nodes if n["closed"] is not None and n["parent"] is not None)
        for chunk in chunks:
            if leaf in chunk:
                chunk.remove(leaf)
    elif kind == "disc":
        node = next((n for n in nodes if n["closed"] == "disc"), None)
        if node is None:
            return None
        record = node["rounds"][-1]
        _, j = manifest["header"]["pairs"][record["closed_pair"][0]]
        record["boxes"][j][1] = rational(Q(record["boxes"][j][1]) + 1)
    elif kind == "split_point":
        node = next(n for n in nodes if n.get("split") and "angle" in n["split"])
        s, _ = node["split"]["angle"]
        node["split"]["angle"][1] = rational(Q(node["angles"][s][1]) + Q(1, 10**6))
    elif kind == "piece":
        found = False
        for record in (r for n in nodes for r in n["rounds"]):
            for pieces in record.get("pairs", {}).values():
                lows = sorted(Q(piece[0]) for piece in pieces)
                if len(lows) >= 2 and lows[0] < lows[1]:
                    piece = min(pieces, key=lambda p: Q(p[0]))
                    if Q(piece[0]) + nudge <= Q(piece[2]):
                        piece[0] = rational(Q(piece[0]) + nudge)
                        found = True
                        break
            if found:
                break
        if not found:
            return None
    else:
        raise ValueError(kind)
    manifest["chunks"] = [write_named(directory, {"nodes": chunk}) for chunk in chunks]
    return write_named(directory, manifest)


KINDS = ("cut_v", "farkas_y", "bound", "box", "lost_child", "disc", "split_point", "piece")


@pytest.mark.parametrize("kind", KINDS)
def test_the_bb_verifier_refuses_each_doctored_kind(
    tmp_path: Path, row_certificates: dict[int, Path], kind: str
) -> None:
    refused = 0
    for obbt_rounds, certificate in row_certificates.items():
        directory = tmp_path / f"obbt{obbt_rounds}"
        _ = shutil.copytree(certificate, directory)
        manifest = corrupt(directory, kind)
        if manifest is None:
            continue
        receipt = bb_verifier.verify_certificate(
            directory, row_cells(tmp_path), manifest=manifest
        )
        assert receipt["status"] == "FAIL", (kind, obbt_rounds)
        refused += 1
    assert refused > 0, f"no certificate carries a {kind} record"


# ---------------------------------------------------------------------------
# Independence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module", ["devtools.verify_n17_kernel_certificate", "devtools.verify_n17_bb_certificate"]
)
def test_a_verifier_imports_no_producer_checker_or_solver(module: str) -> None:
    code = (
        "import sys, importlib\n"
        f"verifier = importlib.import_module({module!r})\n"
        "verifier.cover_cells()\n"
        f"forbidden = {FORBIDDEN!r}\n"
        "loaded = [m for m in sys.modules if m.startswith(forbidden) or 'highs' in m.lower()]\n"
        "assert not loaded, loaded\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PACKING,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
