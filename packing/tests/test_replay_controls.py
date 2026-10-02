"""Stage 4's negative controls for the ``zmx2`` replays: mutated covers it refuses.

``campaign/result-import.md`` asks that two mutated certificates be refused by every
checker that accepted the original, with a test holding them. For each cover that
``devtools.replay_evand_zmx2`` replays, ``CONTROLS`` names two mutations and the root
region where ``zmx2`` refuses each, and the receipts are retained in
``receipts/controls/`` of the packet holding that case's replay. These tests read the
retained receipts and the retained covers only; nothing here runs ``cargo`` or ``zmx2``.
"""

from __future__ import annotations

import gzip
import hashlib
import re
import shlex
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path

import pytest

from devtools import replay_evand_zmx2 as driver
from devtools.audit_evand_mixed_covers import MixedCover, parse_cover

WEB = driver.WEB

#: Where each case's controls are retained: the packet that holds its replay.
PACKETS = {
    32: WEB / "evand-zmx2-sym-atoms-2026-09-30",
    59: WEB / "wand125-point-and-mixed-2026-10-01",
    60: WEB / "evand-square-packing-2026-10-01",
    77: WEB / "wand125-point-and-mixed-2026-10-01",
}

#: The checker build receipt each packet's controls ran with.
BUILDS = {
    WEB / "evand-zmx2-sym-atoms-2026-09-30": "92a4cfe8",
    WEB / "wand125-point-and-mixed-2026-10-01": "6b7f0f79",
    WEB / "evand-square-packing-2026-10-01": "6b7f0f79",
}

CWD = re.compile(
    r"^# cwd: .* zmx2\.rs (?P<checker>[0-9a-f]{64}) built from retained bytes; "
    r"cover (?P<mutated>[0-9a-f]{64}), the (?P<kind>\S+) mutation of "
    r"(?P<original>[0-9a-f]{64}) decompressed from (?P<path>\S+): .*, removing mass "
    r"(?P<removed>\S+)$",
    re.MULTILINE,
)
HEADER = re.compile(
    r"^# zmx2 cert hash=\S+ mode=(?P<mode>\S+) .* "
    r"region=x(?P<x>\d+-\d+),y(?P<y>\d+-\d+),bins0-3$",
    re.MULTILINE,
)
DONE = re.compile(
    r"^done in \S+ wall: roots (?P<roots>\d+) \(missing 0\), .* uncertified (?P<unc>\d+),",
    re.MULTILINE,
)
VERDICT = re.compile(r"^NOT VERIFIED: (?P<unc>\d+) uncertified boxes$", re.MULTILINE)
FOOTER = re.compile(r"^# finished \S+; exit (?P<exit>\d+); ", re.MULTILINE)


@cache
def cover_text(n: int) -> str:
    return gzip.decompress(driver.CASES[n].cover.read_bytes()).decode("ascii")


def as_mixed(text: str) -> MixedCover:
    """Parse with the audit's own reader; a plain point cover is mixed with no segments."""
    if text.split("#", 1)[0].split()[:2] == ["mixed", "1"]:
        return parse_cover(text)
    return parse_cover("mixed 1\n" + text + "0\n0\n")


def total(cover: MixedCover) -> Fraction:
    mass = sum(w for *_, w in cover.points) + sum(s[4] for s in cover.segments)
    return Fraction(mass, cover.mass_denominator)


def edge(cover: MixedCover) -> int:
    scaled = cover.side * cover.denominator
    assert scaled.denominator == 1
    return scaled.numerator


def images(point: tuple[int, int], side: int) -> set[tuple[int, int]]:
    x, y = point
    out: set[tuple[int, int]] = set()
    for a, b in ((x, y), (y, x)):
        out |= {(a, b), (side - a, b), (a, side - b), (side - a, side - b)}
    return out


def point_weights(cover: MixedCover) -> Counter[tuple[int, int]]:
    weights: Counter[tuple[int, int]] = Counter()
    for x, y, w in cover.points:
        weights[(x, y)] += w
    return weights


Entry = tuple[tuple[int, int], tuple[int, int], int]


def segment_entries(cover: MixedCover) -> Counter[Entry]:
    entries: Counter[Entry] = Counter()
    for x0, y0, x1, y1, w in cover.segments:
        a, b = sorted(((x0, y0), (x1, y1)))
        entries[(a, b, w)] += 1
    return entries


def entry_images(entry: Entry, side: int) -> set[Entry]:
    """The images of a segment under the symmetries, by mapping both endpoints alike."""
    (ax, ay), (bx, by), w = entry
    maps = [
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    ]
    out: set[Entry] = set()
    for g in maps:
        a, b = sorted((g(ax, ay), g(bx, by)))
        out.add((a, b, w))
    return out


def d4_invariant(cover: MixedCover) -> bool:
    """Points and segment entries are each mapped onto themselves by the symmetries."""
    side = edge(cover)
    weights = point_weights(cover)
    entries = segment_entries(cover)
    for g in (lambda x, y: (side - x, y), lambda x, y: (y, x)):
        if Counter({g(*p): w for p, w in weights.items()}) != weights:
            return False
        image: Counter[Entry] = Counter()
        for (a, b, w), count in entries.items():
            ga, gb = sorted((g(*a), g(*b)))
            image[(ga, gb, w)] += count
        if image != entries:
            return False
    return True


def expected_orbit_mass(cover: MixedCover, kind: str) -> Fraction:
    """The mass of the orbit ``kind`` names, found from the original cover alone."""
    side = edge(cover)
    if kind == "drop-heaviest-segment":
        entries = segment_entries(cover)
        heaviest = min(entries, key=lambda e: (-e[2], e[0], e[1]))
        orbit = entry_images(heaviest, side)
        mass = sum(e[2] * count for e, count in entries.items() if e in orbit)
        return Fraction(mass, cover.mass_denominator)
    weights = point_weights(cover)
    ranked = sorted(weights, key=lambda p: (-weights[p], p))
    orbit = images(ranked[0], side)
    if kind == "drop-second-heaviest-point":
        orbit = images(next(p for p in ranked if p not in orbit), side)
    return Fraction(sum(weights[p] for p in orbit), cover.mass_denominator)


def applicable(n: int) -> list[str]:
    has_segments = bool(as_mixed(cover_text(n)).segments)
    return [k for k in driver.MUTATIONS if has_segments or k != "drop-heaviest-segment"]


@pytest.mark.parametrize("n", sorted(driver.CASES))
def test_every_mutation_keeps_d4_and_removes_exactly_its_orbit(n: int) -> None:
    text = cover_text(n)
    original = as_mixed(text)
    assert d4_invariant(original)
    for kind in applicable(n):
        mutation = driver.mutate(text, kind)
        mutated = as_mixed(mutation.text)
        assert d4_invariant(mutated), kind
        removed = expected_orbit_mass(original, kind)
        assert removed > 0
        assert mutation.removed == removed == total(original) - total(mutated), kind
        assert mutated.mass_denominator == original.mass_denominator
        dropped = len(original.points) + len(original.segments)
        dropped -= len(mutated.points) + len(mutated.segments)
        assert dropped == mutation.rows > 0
        assert len(text.splitlines()) - len(mutation.text.splitlines()) == mutation.rows
        assert hashlib.sha256(mutation.text.encode()).hexdigest() != driver.CASES[n].sha256


def test_a_point_cover_has_no_segment_mutation() -> None:
    with pytest.raises(ValueError, match="no segments"):
        driver.mutate(cover_text(32), "drop-heaviest-segment")


def test_every_case_has_two_retained_controls() -> None:
    by_case = Counter(n for n, _ in driver.CONTROLS)
    assert by_case == dict.fromkeys(driver.CASES, 2)
    for (n, kind), control in driver.CONTROLS.items():
        assert kind in applicable(n)
        assert control.mode in {"d4", "full"}


def test_the_controls_directories_hold_only_the_controls() -> None:
    expected: dict[Path, set[str]] = {}
    for packet, checker in BUILDS.items():
        expected[packet] = {f"zmx2_{checker}_build.log"}
    for n, kind in driver.CONTROLS:
        receipt = control_receipt(n, kind)
        expected[PACKETS[n]] |= {receipt.name, receipt.name.removesuffix(".log") + "_roots.log"}
    for packet, names in expected.items():
        assert {p.name for p in (packet / "receipts/controls").iterdir()} == names


def control_receipt(n: int, kind: str) -> Path:
    name = driver.CASES[n].name
    found = [
        p
        for p in (PACKETS[n] / "receipts/controls").glob(f"{name}_control_{kind}_zmx2_*.log")
        if not p.name.endswith("_roots.log")
    ]
    assert len(found) == 1, found
    return found[0]


@pytest.mark.parametrize("key", sorted(driver.CONTROLS), ids=lambda k: f"{k[0]}-{k[1]}")
def test_the_retained_control_is_refused_where_recorded(key: tuple[int, str]) -> None:
    n, kind = key
    case, control = driver.CASES[n], driver.CONTROLS[key]
    receipt = control_receipt(n, kind)
    text = receipt.read_text(encoding="utf-8")

    cwd = CWD.search(text)
    assert cwd is not None
    assert cwd["kind"] == kind
    assert cwd["checker"] == driver.CHECKERS[case.checker][1]
    assert cwd["original"] == case.sha256
    assert cwd["path"] == str(case.cover.relative_to(driver.REPO))
    mutation = driver.mutate(cover_text(n), kind)
    assert cwd["mutated"] == hashlib.sha256(mutation.text.encode()).hexdigest()
    assert cwd["mutated"] != cwd["original"]
    assert Fraction(cwd["removed"]) == mutation.removed

    command = shlex.split(text.splitlines()[0].removeprefix("# command: "))
    assert command[:2] == ["verify2/target/release/zmx2", "cert"]
    assert f"--{control.mode}" in command
    assert all(flag in command for flag in case.flags)
    region = {
        flag: command[command.index(flag) + 1] for flag in ("--xlo", "--xhi", "--ylo", "--yhi")
    }
    assert f"{region['--xlo']}-{region['--xhi']}" == control.x
    assert f"{region['--ylo']}-{region['--yhi']}" == control.y

    header = HEADER.search(text)
    assert header is not None
    assert (header["mode"], header["x"], header["y"]) == (control.mode, control.x, control.y)
    verdict, done, footer = VERDICT.search(text), DONE.search(text), FOOTER.search(text)
    assert verdict is not None
    assert done is not None
    assert footer is not None
    assert int(verdict["unc"]) == int(done["unc"]) > 0
    assert int(footer["exit"]) == 0

    (x0, x1), (y0, y1) = (tuple(map(int, v.split("-"))) for v in (control.x, control.y))
    roots = (x1 - x0 + 1) * (y1 - y0 + 1) * 4 * (2 if control.mode == "full" else 1)
    assert int(done["roots"]) == roots
    log = receipt.with_name(receipt.name.removesuffix(".log") + "_roots.log")
    lines = log.read_text(encoding="utf-8").splitlines()
    assert lines[0] == header[0]
    root_lines = [line.split() for line in lines if line.startswith("ROOT ")]
    assert len(root_lines) == roots
    assert sum(int(f[f.index("uncert") + 1]) for f in root_lines) == int(verdict["unc"])


@pytest.mark.parametrize("packet", sorted(BUILDS))
def test_the_build_receipt_names_the_checker_it_built(packet: Path) -> None:
    checker = BUILDS[packet]
    text = (packet / f"receipts/controls/zmx2_{checker}_build.log").read_text(encoding="utf-8")
    assert f"zmx2.rs {driver.CHECKERS[checker][1]} " in text
    assert re.search(r"^# finished \S+; exit 0; ", text, re.MULTILINE)
    assert re.search(r"^# binary sha256: [0-9a-f]{64}$", text, re.MULTILINE)
