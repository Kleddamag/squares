#!/usr/bin/env python3
r"""Acquire the Kingbird catalogue cases above `n = 100` once, and keep only the numbers.

This is the one-time fetch-and-derive pass that decision `D2` of the atlas expansion
plan authorises, and it is the only code path in this repository that can produce a new
Kingbird-derived witness. The 34 witnesses at `n <= 100` were made this way in August
2026 from SVGs that were never committed, so nothing since then has been able to add a
thirty-fifth; that is what this tool restores, for `n = 101..324`.

**What it retains, and what it refuses to.** Each catalogue SVG is fetched into memory,
parsed to normalized centre-and-angle facts, and dropped. No SVG is written anywhere,
no response is cached, and the tool refuses to start at all if a raw Kingbird directory
has appeared under the source inventory or if the output root is inside a directory
named `kingbird`. The retained artefact is a `Witness/v2` record carrying the numbers,
the attribution, the source URL, and its own finite-precision feasibility receipt --
exactly the shape `witnesses/known-best/n-071.yaml` already has. The reasoning is in
`resources/web/known-best-packings/README.md`; this file implements it rather than
restating it.

**The subpacking rule, and the evidence for it.** Thirteen catalogue pictures in
`101..324` serve two counts each. The picture holds the larger count, and the smaller
needs one square removed. Two facts decide how:

1. The catalogue states the rule itself, in the paragraph above its grid: *"If a
   pictured packing has multiple numbers in its label above, the picture represents the
   largest; each smaller is represented by removing any square."* The source therefore
   licenses removing **any** square, and the choice is free rather than guessed.
2. The picture marks nothing. Inspected on 2026-09-07, `square-148.svg` -- the
   `147, 148` entry -- contains `fill:none` only on the paths that draw the internal
   grid lines of its two blocks and on the closing `<use href="#outer">` frame. Every
   one of those is scenery the adapter already skips, and none of them is a square the
   source is offering up for removal. There is no dashed square, no differently filled
   square, and no annotated group.

So the rule is: **take the source's licence, and spend it deterministically.** The
squares are ordered by their normalized centre, descending, comparing exact decimals --
`x`, then `y`, then the angle -- and the first `source_n - n` of them are dropped. The
order is a property of the recovered geometry rather than of the document, so
reformatting the SVG upstream cannot change which square goes; and because it is
descending, what goes is a square at the far edge rather than one out of the middle.
Measured on the one shared entry below `n = 200`: deriving `n = 147` from the `147, 148`
picture drops the square centred at `(s - 1/2, s - 1/2)`, the container's top-right
corner, and the other three corners of the `s = 12.6568...` container keep theirs.
The licence sentence is re-read from the retained transcription every time a subpacking
is built, and its absence is a refusal: if the catalogue stops saying that, this rule
has lost its warrant and the case needs a person, not a default.

**What is skipped rather than derived.** A case whose catalogue side is a whole number
covering it -- `n = 119, 120, 142, 143, 167, 168, 194, 195, 223, 224, 254, 255, 287,
288, 322, 323` -- is a grid case in this atlas even though the catalogue pictures it,
exactly as `n = 47, 48, 62, 63, 79, 80, 98, 99` are at `n <= 100`. The builder generates
those exactly, and a derived witness for one would be overwritten on the next
`--update`, so this tool leaves them alone and says so.

Usage, from `packing/`::

    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --range 101 200 --dry-run
    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --n 147

**After the catalogue is captured again**, a count whose printed side moved keeps a
witness of the packing the page no longer shows. `--refresh` re-derives exactly those --
a retained witness whose side still agrees with the catalogue is left alone -- and
`--retrieved` dates what it writes::

    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --range 101 324 --refresh --retrieved 2026-09-30

The source is one person's personal site. Fetches are sequential by default, each
followed by a pause, and `--jobs` is capped low on purpose.

**A refresh reaches the hand-audited hundred too.** The 34 Kingbird witnesses at
`n <= 100` predate the source map, so a refresh plans one of them from the retained
catalogue itself (`_hand_audited_entry`): the picture that serves the count and the
counts it holds. Nothing at `n <= 100` is derived except to replace a retained witness.

**When the SVG cannot be fetched, a pinned parse of it can stand in**, and says so.
`--from-parse DIR --parse-revision REV` reads each picture from a third party's parse
instead of fetching it: Evan Daniel's `evand/square-packing` exports a parse of every
catalogue SVG (`site/www/data/p/square-<n>.json`, side as a decimal string, poses in
binary64), read by his own `site/tools/parse_svg.py` at 50 digits. `--compare-parse`
measures how far to trust it: on 2026-10-05, at commit `7ff3b21`, his parse agreed with
this repository's own at 90 of the 92 counts where a retained witness was read from the
picture -- the same side, and every pose to one binary64 ulp, square for square and in
the same order -- and the two that differed, `n = 83` and `87`, were counts whose
picture had changed since their witness was read. The parse must print a
side the catalogue's printed decimal truncates, digit for digit, and passes every check
a fetched picture does; the witness records `REV` and the file in `source.revision`,
and the SHA-256 of the file's bytes in `source.revision_sha256`, since the parse is not
retained here and a revision alone does not say which bytes were read. `REV` must be
`owner/name@<full commit>:<directory>`, and its limitations say the numbers are that
parse's and not the SVG's::

    uv run --frozen --all-extras --group dev python -m devtools.derive_kingbird_facts \
        --n 69 --refresh --retrieved 2026-10-05 --from-parse PATH/site/www/data/p \
        --parse-revision evand/square-packing@<commit>:site/www/data/p
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from strif import atomic_output_file

from devtools.build_known_best_atlas import (
    FRONTIER,
    KINGBIRD_RAW_ROOT,
    ROOT,
    SOURCE_MANIFEST,
    USER_AGENT,
    WITNESS_ROOT,
)
from sqpack import retained_json
from sqpack.kingbird_catalogue import CatalogueEntry, default_catalogue_path, parse_catalogue
from sqpack.known_best import (
    KINGBIRD_BASE_URL,
    KINGBIRD_TOLERANCE,
    KingbirdGeometry,
    SourceGeometryError,
    SquarePose,
    kingbird_derived_witness,
    parse_kingbird_svg,
)
from sqpack.witness import check_witness_semantics, witness_document
from sqpack.yamlio import safe_load

AVAILABILITY = ROOT / "atlas/prospective/source-availability-101-324.json"

#: What `--help` says. Written out rather than sliced off `__doc__`, which is stripped
#: under `-OO` and is longer than a usage screen wants anyway.
SUMMARY = (
    "Acquire the Kingbird catalogue cases above n = 100 once, keeping only the derived "
    "numerical facts. No source SVG is written to disk."
)

#: The source-availability key this tool acts on. Every other key in that map is served
#: by the grid rule or by a retained UnitSquare rendering, neither of which needs a
#: fetch.
CATALOGUE_SOURCE_KEY = "kingbird-current-catalogue"
#: How a frontier record names the catalogue as the source of its reported side.
CATALOGUE_RECORD_KEY = "[Kingbird]"
#: The hand-audited hundred, whose 34 Kingbird witnesses predate the source map. A count
#: here is planned from the catalogue itself, and only to refresh a retained witness.
HAND_AUDITED_MAX = 100
#: The one parse format `--from-parse` reads: Evan Daniel's per-picture export, whose
#: `site/tools/parse_svg.py` reads the catalogue SVG at 50 digits and whose
#: `site/tools/export.py` writes `{"s": ..., "n": ..., "squares": [[cx, cy, angle], ...]}`
#: with the side as a decimal string and each pose in binary64, angles in degrees modulo
#: 90, in the y-up frame of the container `[0, s]^2` -- this repository's own convention.
PARSE_FILE_SUFFIX = ".json"
#: A pinned parse: `owner/name@<full commit>:<directory>`, the directory the files are in.
PARSE_REVISION = re.compile(r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}:\S+$")

#: The date this acquisition pass read the catalogue, recorded in every witness it
#: writes. Not `sqpack.known_best.RETRIEVED_DATE`, which belongs to the 2026-08-26 pass
#: and must keep saying so for the 34 witnesses that carry it.
DERIVED_RETRIEVED_DATE = "2026-09-07"

#: The catalogue's own sentence licensing a subpacking. Checked against the retained
#: transcription before any square is dropped; see this module's docstring.
REMOVAL_LICENCE = "each smaller is represented by removing any square"

#: Politeness, matching `build_known_best_atlas._fetch_one`: one pause per fetch, taken
#: inside the worker that fetched, so `--jobs` raises the rate by at most its own factor.
FETCH_PAUSE_SECONDS = 0.15
FETCH_ATTEMPTS = 3
FETCH_TIMEOUT_SECONDS = 30
#: Low on purpose. The ceiling is not a resource limit on this machine; it is a limit on
#: what this tool can do to someone else's web server.
MAX_JOBS = 4


class DerivationRefusedError(RuntimeError):
    """A typed refusal to derive one case, carrying the reason a report can group on."""

    def __init__(self, kind: str, detail: str) -> None:
        super().__init__(f"{kind}: {detail}")
        self.kind: str = kind
        self.detail: str = detail


@dataclass(frozen=True)
class DerivationPlan:
    """One case this pass intends to acquire, with everything the fetch needs."""

    n: int
    source_n: int
    listed_n: tuple[int, ...]
    source_path: str
    url: str
    #: The catalogue's printed decimal side. This is the reported value the receipt is
    #: checked against, because a frontier record for `n > 100` may not exist yet.
    catalogue_side: str
    witness_path: Path

    @property
    def removals(self) -> int:
        """How many squares the subpacking rule drops; zero for a pictured count."""
        return self.source_n - self.n


@dataclass(frozen=True)
class SkippedCase:
    """One case this pass deliberately does not acquire, and why."""

    n: int
    reason: str
    detail: str


@dataclass(frozen=True)
class DerivedCase:
    """One acquired case: the witness, its serialization, and where it was written."""

    plan: DerivationPlan
    witness: dict[str, Any]
    text: str
    path: Path

    @property
    def receipt(self) -> dict[str, Any]:
        """The feasibility receipt `kingbird_derived_witness` wrote into the record."""
        return self.witness["certificate"]["result"]


def _relative(path: Path) -> str:
    """Repository-relative where it can be, absolute where the caller went elsewhere."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def availability_entries(path: Path | None = None) -> dict[int, dict[str, Any]]:
    """The prospective source map, keyed by `n`."""
    target = AVAILABILITY if path is None else path
    document = json.loads(target.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in document["availability"]["entries"]}


def _grid_covered(n: int, side: str) -> bool:
    """Whether the catalogue's own side is a whole number a plain grid already reaches."""
    value = Fraction(side)
    return value.denominator == 1 and value.numerator * value.numerator >= n


def _hand_audited_entry(n: int, catalogued: dict[int, CatalogueEntry]) -> dict[str, Any] | None:
    """A source-map entry for a count of the hand-audited hundred, read off the catalogue.

    The source map covers `101..324`; the 34 Kingbird witnesses at `n <= 100` were derived
    in August 2026 by a pass that left no map. A refresh of one of them -- the page was
    captured again and prints a new side -- needs the same four facts the map gives, and
    the retained catalogue states all of them: which picture serves the count, which
    counts that picture holds, and so where it lives. `None` where the page pictures no
    packing for the count, which the caller refuses like any count outside the map.
    """
    listed = catalogued.get(n)
    if listed is None or listed.svg_path is None:
        return None
    return {
        "n": n,
        "source_key": CATALOGUE_SOURCE_KEY,
        "source_n": listed.n,
        "listed_n": list(listed.listed_n),
        "source_path": listed.svg_path,
        "source_url": f"{KINGBIRD_BASE_URL}/{listed.svg_path}",
    }


def _cross_check(n: int, entry: dict[str, Any], catalogued: CatalogueEntry) -> None:
    """Refuse where the source map and the reparsed catalogue disagree about a case.

    Two independent readings of the same page: the 2026-08-26 audit that wrote the map,
    and `sqpack.kingbird_catalogue` reading the retained transcription today. A case is
    only acquired where they agree on which picture serves it and on which counts that
    picture holds.
    """
    if catalogued.svg_path != entry["source_path"]:
        raise DerivationRefusedError(
            "source-map-disagrees",
            f"n={n}: the map names {entry['source_path']!r} and the catalogue names "
            f"{catalogued.svg_path!r}",
        )
    listed = tuple(int(value) for value in entry["listed_n"])
    if catalogued.listed_n != listed or catalogued.n != int(entry["source_n"]):
        raise DerivationRefusedError(
            "source-map-disagrees",
            f"n={n}: the map lists {listed} under source_n={entry['source_n']} and the "
            f"catalogue lists {catalogued.listed_n} under n={catalogued.n}",
        )


def derivation_plans(
    numbers: Sequence[int],
    *,
    out_root: Path,
    availability: dict[int, dict[str, Any]] | None = None,
    catalogue: dict[int, CatalogueEntry] | None = None,
    refresh: bool = False,
) -> tuple[list[DerivationPlan], list[SkippedCase], list[tuple[int, DerivationRefusedError]]]:
    """Split the requested counts into what this pass acquires, leaves, and refuses.

    Nothing raises: one unreadable case in a hundred-case range is that case's refusal,
    reported with the rest, rather than an abort that loses the other ninety-nine. A
    skip and a refusal differ in kind -- a skip is a case this tool was never going to
    touch (a grid case, a UnitSquare case, one already retained), a refusal is one it
    should have been able to touch and could not.
    """
    entries = availability_entries() if availability is None else availability
    catalogued = parse_catalogue() if catalogue is None else catalogue
    plans: list[DerivationPlan] = []
    skipped: list[SkippedCase] = []
    refusals: list[tuple[int, DerivationRefusedError]] = []
    for n in numbers:
        try:
            plan = _plan_one(n, entries, catalogued, out_root=out_root, refresh=refresh)
        except DerivationRefusedError as error:
            refusals.append((n, error))
            continue
        if isinstance(plan, SkippedCase):
            skipped.append(plan)
        else:
            plans.append(plan)
    return plans, skipped, refusals


def _plan_one(
    n: int,
    entries: dict[int, dict[str, Any]],
    catalogued: dict[int, CatalogueEntry],
    *,
    out_root: Path,
    refresh: bool = False,
) -> DerivationPlan | SkippedCase:
    """Decide one count: acquire it, skip it, or refuse it.

    A retained witness is skipped, since this pass never refetches what it already
    holds -- unless `refresh` is set and the witness's side is no longer the catalogue's.
    That is the one reason to replace one: the page was captured again and prints a new
    side for the count, so the retained numbers describe a packing it no longer shows.
    """
    entry = entries.get(n)
    if entry is None and n <= HAND_AUDITED_MAX and refresh:
        entry = _hand_audited_entry(n, catalogued)
    if entry is None:
        raise DerivationRefusedError(
            "no-availability-entry", f"n={n}: outside the audited 101..324 source map"
        )
    source_key = str(entry["source_key"])
    if source_key != CATALOGUE_SOURCE_KEY:
        return SkippedCase(n, "other-source", f"served by {source_key}")
    listed = catalogued.get(n)
    if listed is None:
        raise DerivationRefusedError(
            "not-in-catalogue",
            f"n={n}: the source map says catalogue, the catalogue is silent",
        )
    _cross_check(n, entry, listed)
    if _grid_covered(n, listed.side_decimal):
        return SkippedCase(n, "grid-covered", f"catalogue side {listed.side_decimal} is a grid")
    witness_path = out_root / f"n-{n:03d}.yaml"
    if witness_path.is_file():
        if not refresh:
            return SkippedCase(n, "existing", _relative(witness_path))
        reported_by = frontier_source_key(n)
        if reported_by not in {None, CATALOGUE_RECORD_KEY}:
            # The record's upper lane is another source's packing, and so is the witness
            # the builder wrote for it; the catalogue's picture is not this count's.
            return SkippedCase(n, "other-source", f"the frontier record reports {reported_by}")
        retained = retained_side(witness_path)
        if _sides_agree(listed.side_decimal, retained):
            return SkippedCase(
                n, "current", f"{_relative(witness_path)} agrees with the catalogue"
            )
    return DerivationPlan(
        n=n,
        source_n=int(entry["source_n"]),
        listed_n=listed.listed_n,
        source_path=str(entry["source_path"]),
        url=str(entry["source_url"]),
        catalogue_side=listed.side_decimal,
        witness_path=witness_path,
    )


def fetch_picture(url: str) -> tuple[bytes, str | None]:
    """Fetch one catalogue SVG into memory, with the builder's retries and politeness.

    Returns the bytes and the server's `Last-Modified`. Nothing here writes, and no
    caller is given a path: the bytes exist only for as long as the derivation or the
    comparison that parses them.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(FETCH_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
                content = response.read()
                modified = response.headers.get("Last-Modified")
        except (OSError, urllib.error.HTTPError, urllib.error.URLError) as error:
            last_error = error
            if attempt < FETCH_ATTEMPTS - 1:
                time.sleep(2**attempt)
        else:
            # The whole response, not a prefix: `square-179.svg` of 2026-09-30 opens with a
            # 166,839-byte comment carrying its degree-158 polynomial before `<svg`.
            if b"<svg" not in content:
                raise DerivationRefusedError("not-svg", f"upstream response is not SVG: {url}")
            time.sleep(FETCH_PAUSE_SECONDS)
            return content, modified
    raise DerivationRefusedError("fetch-failed", f"{url}: {last_error}")


def fetch_svg(url: str) -> str:
    """One catalogue SVG's text, fetched as `fetch_picture` fetches it."""
    return fetch_picture(url)[0].decode("utf-8")


def _pose_key(pose: SquarePose) -> tuple[Decimal, Decimal, Decimal]:
    """A pose's exact decimal ordering key. `Decimal` because these strings are exact."""
    return (
        Decimal(pose.center_x),
        Decimal(pose.center_y),
        Decimal(pose.angle_degrees),
    )


def assert_removal_licence(catalogue_text: str) -> None:
    """Refuse to build a subpacking unless the catalogue still licenses one."""
    if REMOVAL_LICENCE not in catalogue_text:
        raise DerivationRefusedError(
            "removal-licence-absent",
            "the retained catalogue no longer states that a smaller listed count is the "
            "pictured packing with any square removed; a subpacking has lost its warrant",
        )


def subpacking_poses(
    poses: Sequence[SquarePose], *, n: int, source_n: int, catalogue_text: str
) -> tuple[SquarePose, ...]:
    """The `n` squares this repository keeps from a picture holding `source_n` of them.

    Identity where the picture is the case. Otherwise the catalogue's own licence is
    checked and then spent deterministically: drop the `source_n - n` squares whose
    normalized centres sort last, exact decimals, `x` then `y` then angle. Survivors keep
    the order they were recovered in, which is the order every retained witness is in.
    """
    if len(poses) != source_n:
        raise DerivationRefusedError(
            "square-count-mismatch",
            f"the picture for n={source_n} yielded {len(poses)} squares",
        )
    if n == source_n:
        return tuple(poses)
    if not 1 <= n < source_n:
        raise DerivationRefusedError(
            "subpacking-out-of-range", f"n={n} is not a subpacking of n={source_n}"
        )
    assert_removal_licence(catalogue_text)
    order = sorted(range(source_n), key=lambda index: _pose_key(poses[index]), reverse=True)
    dropped = set(order[: source_n - n])
    return tuple(pose for index, pose in enumerate(poses) if index not in dropped)


def _sides_agree(reported: str, actual: str) -> bool:
    """The builder's side agreement, at the tolerance the Kingbird facts are checked at."""
    with mp.workdps(120):
        difference = abs(mp.mpf(reported) - mp.mpf(actual))
        tolerance = max(mp.mpf("1e-8"), abs(mp.mpf(reported)) * mp.mpf("1e-12"))
        return bool(difference <= tolerance)


def retained_side(path: Path) -> str:
    """The side a retained witness records, read without loading its geometry."""
    document = safe_load(path.read_text(encoding="utf-8"))
    witness = document.get("witness") if isinstance(document, dict) else None
    if not isinstance(witness, dict) or "side" not in witness:
        raise DerivationRefusedError(
            "witness-unreadable", f"{_relative(path)} records no witness side"
        )
    return str(witness["side"])


def _assert_side_matches(reported: str, actual: str, *, what: str, n: int) -> None:
    """Refuse where `_sides_agree` does not hold."""
    if not _sides_agree(reported, actual):
        raise DerivationRefusedError(
            "side-mismatch", f"n={n}: source side {actual} disagrees with {what} {reported}"
        )


def _frontier_upper(n: int, frontier_root: Path | None) -> dict[str, Any] | None:
    root = FRONTIER if frontier_root is None else frontier_root
    path = root / f"n-{n:03d}.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise DerivationRefusedError("frontier-malformed", f"{path.name}: missing frontmatter")
    return safe_load(text.split("---\n", 2)[1])["packing"]["reported_upper_bound"]


def frontier_source_key(n: int, *, frontier_root: Path | None = None) -> str | None:
    """Whose side `frontier/n-NNN.md` reports, or None where no record is."""
    upper = _frontier_upper(n, frontier_root)
    return None if upper is None else str(upper.get("source_key"))


def frontier_reported_side(n: int, *, frontier_root: Path | None = None) -> str | None:
    """What `frontier/n-NNN.md` reports as the upper bound, or None where no record is."""
    upper = _frontier_upper(n, frontier_root)
    return None if upper is None else str(upper["value"])


def _float_text(value: object) -> str:
    """One binary64 coordinate as the shortest decimal that reads back to it.

    Written the way the SVG adapter writes a number (`sqpack.known_best._format`): fixed
    notation, `0` for zero and `2.0` for two, so a witness read from a parse differs from
    one read from the picture only in the digits the parse does not carry.
    """
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise DerivationRefusedError("parse-unreadable", f"{value!r} is not a number")
    number = Decimal(repr(float(value)))
    if not number.is_finite():
        raise DerivationRefusedError("parse-unreadable", f"{value!r} is not finite")
    return "0" if number.is_zero() else format(number, "f")


def _positive_decimal(text: str) -> bool:
    """Whether `text` is a finite decimal above zero; text that is no decimal is not."""
    try:
        value = Decimal(text)
    except InvalidOperation:
        return False
    return value.is_finite() and value > 0


def parse_record_name(plan: DerivationPlan) -> str:
    """The parse file that holds this plan's picture: `square-69.svg` is `square-69.json`."""
    return Path(plan.source_path).stem + PARSE_FILE_SUFFIX


def geometry_from_parse(text: str, *, expected_n: int, where: str) -> KingbirdGeometry:
    """Read one picture's parse (`PARSE_FILE_SUFFIX`) as the geometry an SVG parse gives.

    The parse is a third party's reading of the same SVG, so it is held to the same
    checks a fetched picture is: the side and the square count, here, and the catalogue's
    printed side and the frontier record's, in `derive_witness`. Each pose is kept at the
    binary64 precision the parse publishes, never padded with digits it does not carry.
    """
    try:
        record = json.loads(text)
    except json.JSONDecodeError as error:
        raise DerivationRefusedError("parse-unreadable", f"{where}: {error}") from error
    if not isinstance(record, dict) or not isinstance(record.get("squares"), list):
        raise DerivationRefusedError("parse-unreadable", f"{where}: no squares list")
    side = record.get("s")
    if not isinstance(side, str) or not _positive_decimal(side):
        raise DerivationRefusedError("parse-unreadable", f"{where}: side {side!r}")
    squares = record["squares"]
    if record.get("n") != expected_n or len(squares) != expected_n:
        raise DerivationRefusedError(
            "square-count-mismatch",
            f"{where} holds {len(squares)} squares under n={record.get('n')}, not {expected_n}",
        )
    poses: list[SquarePose] = []
    for index, square in enumerate(squares, start=1):
        if not isinstance(square, list) or len(square) != 3:
            raise DerivationRefusedError(
                "parse-unreadable", f"{where}: square {index} is not [cx, cy, angle]"
            )
        center_x, center_y, angle = (_float_text(value) for value in square)
        if not Decimal(0) <= Decimal(angle) < Decimal(90):
            raise DerivationRefusedError(
                "parse-unreadable", f"{where}: square {index} angle {angle} is not in [0, 90)"
            )
        poses.append(SquarePose(center_x, center_y, angle))
    return KingbirdGeometry(side=side, poses=tuple(poses))


def _assert_printed_truncation(printed: str, actual: str, *, n: int) -> None:
    """Refuse a parse whose side the catalogue's printed decimal does not truncate.

    The page prints its side cut short, never rounded, so a parse of the picture it
    shows must begin with exactly those digits. The `_sides_agree` tolerance alone would
    accept another version of the picture within 1e-8; this does not.
    """
    lower = Decimal(printed)
    exponent = lower.as_tuple().exponent
    if not isinstance(exponent, int):
        raise DerivationRefusedError("side-mismatch", f"n={n}: {printed} is not a decimal")
    step = Decimal(1).scaleb(exponent)
    if not lower <= Decimal(actual) < lower + step:
        raise DerivationRefusedError(
            "side-mismatch",
            f"n={n}: the parse's side {actual} does not begin with the catalogue's {printed}",
        )


@dataclass(frozen=True)
class ParseAgreement:
    """How one parse compares with the witness this repository read from the same SVG."""

    n: int
    same_side: bool
    #: The largest difference of a centre coordinate or an angle, square for square, in
    #: units in the last place of binary64 at the larger of the two values and 1. At most
    #: one is the parse being this repository's own numbers, rounded to the parse.
    worst: float


def compare_parse(n: int, parse_text: str, witness_path: Path) -> ParseAgreement:
    """Compare a parse with a retained witness read from the SVG, at binary64.

    The measurement behind trusting `--from-parse`: where this repository read the
    picture itself, the third party's parse should be the same numbers rounded to the
    parse's precision, in the same order. Retained facts read from a parse are not a
    comparison and are refused.
    """
    witness = safe_load(witness_path.read_text(encoding="utf-8"))["witness"]
    if (witness.get("source") or {}).get("revision"):
        raise DerivationRefusedError(
            "not-independent", f"{_relative(witness_path)} was itself read from a parse"
        )
    geometry = geometry_from_parse(parse_text, expected_n=n, where=f"n={n}")
    ours = [
        (float(square["center"][0]), float(square["center"][1]), float(square["angle"]))
        for square in witness["squares"]
    ]
    theirs = [
        (float(pose.center_x), float(pose.center_y), float(pose.angle_degrees))
        for pose in geometry.poses
    ]
    worst = max(
        abs(left - right) / math.ulp(max(abs(left), abs(right), 1.0))
        for mine, other in zip(ours, theirs, strict=True)
        for left, right in zip(mine, other, strict=True)
    )
    return ParseAgreement(
        n=n,
        same_side=float(witness["side"]) == float(geometry.side),
        worst=worst,
    )


def compare_parses(numbers: Sequence[int], root: Path, *, out_root: Path) -> int:
    """`--compare-parse`: report how a parse directory agrees with the retained corpus.

    Counts are compared where the retained witness was read from the catalogue's own
    picture of that count -- center-angle, not a subpacking, not itself read from a parse
    -- and the parse holds the picture. Exit 0 only where every compared count agrees,
    side exactly at binary64 and every pose to one unit in its last place; anything else
    is printed with its difference.
    """
    catalogued = parse_catalogue()
    compared = disagreeing = 0
    for n in numbers:
        listed = catalogued.get(n)
        witness_path = out_root / f"n-{n:03d}.yaml"
        if listed is None or listed.svg_path is None or listed.n != n:
            continue
        if not witness_path.is_file():
            continue
        witness = safe_load(witness_path.read_text(encoding="utf-8"))["witness"]
        from_parse = bool((witness.get("source") or {}).get("revision"))
        if witness.get("representation") != "center-angle" or from_parse:
            continue
        if not str((witness.get("source") or {}).get("url", "")).endswith(listed.svg_path):
            continue
        parse = root / (Path(listed.svg_path).stem + PARSE_FILE_SUFFIX)
        if not parse.is_file():
            continue
        agreement = compare_parse(n, parse.read_text(encoding="utf-8"), witness_path)
        compared += 1
        if not agreement.same_side or agreement.worst > 1:
            disagreeing += 1
            print(
                f"  n={n:<3} differs  side {'agrees' if agreement.same_side else 'differs'}, "
                f"largest pose difference {agreement.worst:.3g} ulp"
            )
    print(
        f"compared {compared} count{'' if compared == 1 else 's'}: "
        f"{compared - disagreeing} agree to one binary64 ulp, {disagreeing} differ"
    )
    return 1 if disagreeing or not compared else 0


@dataclass(frozen=True)
class PictureReading:
    """One catalogue picture fetched again and compared with the witness retained for it.

    `identical` is the strongest agreement: the side and every centre and angle the same
    decimal text, square for square. Otherwise `same_side` and `worst` measure it at
    binary64, as `compare_parse` does, which is how a witness read from a parse compares
    with the picture it was a parse of.
    """

    n: int
    url: str
    bytes: int
    sha256: str
    last_modified: str | None
    #: The witness was read from a third party's parse (`source.revision`), not the SVG.
    from_parse: bool
    identical: bool
    same_side: bool
    worst: float
    #: The picture's attribution: the first paragraph of the comment before `<svg`.
    credits: tuple[str, ...]


def picture_credits(text: str) -> tuple[str, ...]:
    """The first paragraph of the comment a catalogue SVG opens with, line by line.

    The catalogue writes its attribution there, with the dates its page abbreviates to
    a month, and below a blank line whatever derivation or polynomial the picture
    carries. Only the attribution is returned.
    """
    head = text.split("<svg", 1)[0]
    start = head.find("<!--")
    if start < 0:
        return ()
    comment = head[start + 4 :].split("-->", 1)[0]
    lines: list[str] = []
    for line in comment.splitlines():
        if not line.strip():
            if lines:
                break
            continue
        lines.append(line.strip())
    return tuple(lines)


def _poses_text(witness: dict[str, Any]) -> list[tuple[str, str, str]]:
    return [
        (str(square["center"][0]), str(square["center"][1]), str(square["angle"]))
        for square in witness["squares"]
    ]


def read_picture_again(
    n: int,
    witness: dict[str, Any],
    picture: bytes,
    *,
    source_n: int,
    catalogue_text: str,
    last_modified: str | None = None,
) -> PictureReading:
    """Compare one retained Kingbird witness with its picture, fetched again."""
    url = str(witness["source"]["url"])
    text = picture.decode("utf-8")
    try:
        geometry = parse_kingbird_svg(text, expected_n=source_n)
    except SourceGeometryError as error:
        raise DerivationRefusedError(error.kind, f"n={n} from {url}: {error}") from error
    poses = subpacking_poses(
        geometry.poses, n=n, source_n=source_n, catalogue_text=catalogue_text
    )
    theirs = [(pose.center_x, pose.center_y, pose.angle_degrees) for pose in poses]
    ours = _poses_text(witness)
    if len(ours) != len(theirs):
        raise DerivationRefusedError(
            "square-count-mismatch", f"n={n}: {len(ours)} retained, {len(theirs)} in {url}"
        )
    worst = max(
        abs(float(left) - float(right))
        / math.ulp(max(abs(float(left)), abs(float(right)), 1.0))
        for mine, other in zip(ours, theirs, strict=True)
        for left, right in zip(mine, other, strict=True)
    )
    return PictureReading(
        n=n,
        url=url,
        bytes=len(picture),
        sha256=hashlib.sha256(picture).hexdigest(),
        last_modified=last_modified,
        from_parse=bool(witness["source"].get("revision")),
        identical=str(witness["side"]) == geometry.side and ours == theirs,
        same_side=float(witness["side"]) == float(geometry.side),
        worst=worst,
        credits=picture_credits(text),
    )


def compare_pictures(
    numbers: Sequence[int],
    *,
    out_root: Path,
    fetch: Callable[[str], tuple[bytes, str | None]] = fetch_picture,
) -> tuple[list[PictureReading], list[tuple[int, DerivationRefusedError]]]:
    """`--compare-pictures`: fetch the picture behind each retained Kingbird witness again.

    Every center-angle witness under `out_root` whose source is a catalogue SVG is
    compared with that SVG as the catalogue serves it now, read by this repository's own
    adapter: pictured counts and subpackings, and witnesses read from a third party's
    parse, which is the one comparison `--compare-parse` cannot make. A picture serving
    two counts is fetched once. Nothing fetched is written.
    """
    catalogued = parse_catalogue()
    catalogue_text = default_catalogue_path().read_text(encoding="utf-8")
    fetched: dict[str, tuple[bytes, str | None]] = {}
    readings: list[PictureReading] = []
    refusals: list[tuple[int, DerivationRefusedError]] = []
    for n in numbers:
        path = out_root / f"n-{n:03d}.yaml"
        if not path.is_file():
            continue
        witness = safe_load(path.read_text(encoding="utf-8"))["witness"]
        url = str((witness.get("source") or {}).get("url", ""))
        if not url.startswith(KINGBIRD_BASE_URL) or witness.get("representation") != (
            "center-angle"
        ):
            continue
        listed = catalogued.get(n)
        if listed is None or listed.svg_path is None or not url.endswith(listed.svg_path):
            refusals.append(
                (
                    n,
                    DerivationRefusedError(
                        "source-map-disagrees",
                        f"n={n}: the witness names {url}, the catalogue "
                        f"{None if listed is None else listed.svg_path}",
                    ),
                )
            )
            continue
        try:
            if url not in fetched:
                fetched[url] = fetch(url)
            picture, modified = fetched[url]
            readings.append(
                read_picture_again(
                    n,
                    witness,
                    picture,
                    source_n=listed.n,
                    catalogue_text=catalogue_text,
                    last_modified=modified,
                )
            )
        except DerivationRefusedError as error:
            refusals.append((n, error))
    return readings, refusals


def picture_receipt(
    readings: Sequence[PictureReading],
    refusals: Sequence[tuple[int, DerivationRefusedError]],
    *,
    retrieved_utc: str,
) -> dict[str, Any]:
    """What `--compare-pictures --receipt` writes: one row per count, and the tally."""
    agree = [r for r in readings if r.identical or (r.same_side and r.worst <= 1)]
    return {
        "format": "kingbird-picture-reading-v1",
        "retrieved_utc": retrieved_utc,
        "compared": len(readings),
        "identical": sum(r.identical for r in readings),
        "agree_to_one_ulp": len(agree),
        "refused": [{"n": n, "kind": e.kind, "detail": e.detail} for n, e in refusals],
        "readings": [
            {
                "n": r.n,
                "url": r.url,
                "bytes": r.bytes,
                "sha256": r.sha256,
                "last_modified": r.last_modified,
                "from_parse": r.from_parse,
                "identical": r.identical,
                "same_side": r.same_side,
                "worst_ulp": r.worst,
                "credits": list(r.credits),
            }
            for r in readings
        ],
    }


def report_pictures(
    readings: Sequence[PictureReading], refusals: Sequence[tuple[int, DerivationRefusedError]]
) -> int:
    """Print `--compare-pictures`'s findings; exit 0 only where every picture agrees."""
    disagreeing = 0
    for reading in readings:
        agrees = reading.identical or (reading.same_side and reading.worst <= 1)
        disagreeing += not agrees
        if reading.from_parse or not reading.identical:
            print(
                f"  n={reading.n:<3} {'agrees' if agrees else 'differs'}  "
                f"{'parse-read, ' if reading.from_parse else ''}"
                f"{'identical' if reading.identical else f'worst {reading.worst:.3g} ulp'}"
                f", {reading.bytes} bytes, Last-Modified {reading.last_modified}"
            )
    for n, refusal in refusals:
        print(f"  n={n:<3} refused  {refusal}")
    identical = sum(reading.identical for reading in readings)
    print(
        f"read {len(readings)} witness{'' if len(readings) == 1 else 'es'} against the "
        f"catalogue's pictures: {identical} identical, "
        f"{len(readings) - identical - disagreeing} to one binary64 ulp, "
        f"{disagreeing} differ, {len(refusals)} refused"
    )
    return 1 if disagreeing or refusals or not readings else 0


def derive_witness(
    plan: DerivationPlan,
    source_text: str,
    *,
    catalogue_text: str,
    retrieved: str = DERIVED_RETRIEVED_DATE,
    frontier_root: Path | None = None,
    parse_revision: str | None = None,
) -> dict[str, Any]:
    """Parse one fetched SVG and return the checked `Witness/v2` record for one `n`.

    The retained shape is assembled here; every claim, source and certificate field is
    written by `kingbird_derived_witness`, which is the same code that rechecks the 34
    existing rows on every build.

    With `parse_revision`, `source_text` is not an SVG but a third party's parse of it
    (`geometry_from_parse`), pinned at that revision; the witness names it and the
    SHA-256 of the parse's bytes, which this repository does not retain, and says its
    numbers are that parse's, and the parse must reproduce the page's printed side digit
    for digit.
    """
    if parse_revision is None:
        try:
            geometry = parse_kingbird_svg(source_text, expected_n=plan.source_n)
        except SourceGeometryError as error:
            raise DerivationRefusedError(
                error.kind, f"n={plan.n} from {plan.source_path}: {error}"
            ) from error
        revision = digest = None
    else:
        revision = f"{pinned_parse_revision(parse_revision)}/{parse_record_name(plan)}"
        digest = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
        geometry = geometry_from_parse(source_text, expected_n=plan.source_n, where=revision)
        _assert_printed_truncation(plan.catalogue_side, geometry.side, n=plan.n)
    _assert_side_matches(plan.catalogue_side, geometry.side, what="the catalogue", n=plan.n)
    recorded = frontier_reported_side(plan.n, frontier_root=frontier_root)
    if recorded is not None:
        _assert_side_matches(recorded, geometry.side, what="the frontier record", n=plan.n)
    poses = subpacking_poses(
        geometry.poses, n=plan.n, source_n=plan.source_n, catalogue_text=catalogue_text
    )
    retained = {
        "id": f"W-known-best-n{plan.n:03d}",
        "n": plan.n,
        "side": geometry.side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "degrees",
        },
        "squares": [
            {
                "id": index,
                "center": [pose.center_x, pose.center_y],
                "angle": pose.angle_degrees,
            }
            for index, pose in enumerate(poses, start=1)
        ],
    }
    try:
        witness = kingbird_derived_witness(
            plan.n,
            retained,
            source_n=plan.source_n,
            source_path=_relative(SOURCE_MANIFEST),
            source_url=plan.url,
            retrieved=retrieved,
            revision=revision,
            revision_sha256=digest,
        )
    except (SourceGeometryError, ValueError) as error:
        raise DerivationRefusedError("witness-rejected", f"n={plan.n}: {error}") from error
    problems = check_witness_semantics(witness)
    if problems:
        raise DerivationRefusedError("witness-rejected", f"n={plan.n}: {problems[0]}")
    return witness


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")


def _parts_below_checkout(path: Path) -> tuple[str, ...]:
    """The path's parts below the checkout's root, or all of them for a path outside it.

    Where the checkout itself lives is the person's choice and says nothing about what the
    repository retains: a worktree named `kingbird` holds no Kingbird asset by being so
    named.
    """
    resolved = path.resolve()
    checkout = ROOT.resolve().parent
    try:
        return resolved.relative_to(checkout).parts
    except ValueError:
        return resolved.parts


def assert_no_raw_retention(out_root: Path) -> None:
    """The two ways this pass could start leaving source bytes behind, refused up front."""
    if KINGBIRD_RAW_ROOT.exists():
        raise DerivationRefusedError(
            "raw-kingbird-retained",
            f"{_relative(KINGBIRD_RAW_ROOT)} exists; the retention policy keeps no raw "
            "Kingbird asset, so this pass will not add derived facts beside one",
        )
    if any(part.lower() == "kingbird" for part in _parts_below_checkout(out_root)):
        raise DerivationRefusedError(
            "output-under-kingbird-directory",
            f"{out_root} is inside a directory named kingbird; witnesses are derived "
            "facts and do not live with source assets",
        )


def fetch_pictures(
    plans: Sequence[DerivationPlan], *, jobs: int, fetch: Callable[[str], str] = fetch_svg
) -> tuple[dict[str, str], dict[str, DerivationRefusedError]]:
    """Fetch each distinct picture once, however many counts it serves."""
    urls = sorted({plan.url for plan in plans})
    fetched: dict[str, str] = {}
    failures: dict[str, DerivationRefusedError] = {}
    if not urls:
        return fetched, failures
    with ThreadPoolExecutor(max_workers=min(jobs, len(urls))) as executor:
        futures = {executor.submit(fetch, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                fetched[url] = future.result()
            except DerivationRefusedError as error:
                failures[url] = error
    return fetched, failures


def read_parses(
    plans: Sequence[DerivationPlan], root: Path
) -> tuple[dict[str, str], dict[str, DerivationRefusedError]]:
    """Read each distinct picture's parse from `root`, keyed by the picture's URL as
    `fetch_pictures` keys what it fetches, so the rest of a pass is the same either way.

    Each is decoded from its bytes with no newline translation, so the text encodes back
    to exactly the file and the digest `derive_witness` records is the file's.
    """
    read: dict[str, str] = {}
    failures: dict[str, DerivationRefusedError] = {}
    for plan in plans:
        path = root / parse_record_name(plan)
        if not path.is_file():
            failures[plan.url] = DerivationRefusedError(
                "parse-missing", f"{path} holds no parse of {plan.source_path}"
            )
            continue
        try:
            read[plan.url] = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as error:
            failures[plan.url] = DerivationRefusedError(
                "parse-unreadable", f"{path}: not UTF-8: {error}"
            )
    return read, failures


def pinned_parse_revision(revision: str) -> str:
    """`revision` without a trailing slash, or a refusal unless it pins a commit and a
    directory: it is written into every witness read from the parse, so a branch, a
    short id or a sentence would be a provenance nobody can resolve."""
    if not PARSE_REVISION.fullmatch(revision):
        raise DerivationRefusedError(
            "parse-unpinned",
            f"--parse-revision {revision!r} is not owner/name@<40-hex commit>:<directory>",
        )
    return revision.rstrip("/")


def derive(
    numbers: Sequence[int],
    *,
    out_root: Path,
    jobs: int = 1,
    dry_run: bool = False,
    retrieved: str = DERIVED_RETRIEVED_DATE,
    fetch: Callable[[str], str] = fetch_svg,
    refresh: bool = False,
    from_parse: Path | None = None,
    parse_revision: str | None = None,
) -> int:
    """Run one acquisition pass and report it. Returns the process exit status.

    With `from_parse`, nothing is fetched: each picture's numbers are read from a third
    party's parse of it in that directory, pinned at `parse_revision`, which every
    witness written names. That is for a count whose SVG this session cannot reach; the
    checks a fetched picture passes are the same.
    """
    if (from_parse is None) != (parse_revision is None):
        raise DerivationRefusedError(
            "parse-unpinned", "a parse directory and its pinned revision go together"
        )
    if parse_revision is not None:
        parse_revision = pinned_parse_revision(parse_revision)
    assert_no_raw_retention(out_root)
    plans, skipped, refusals = derivation_plans(numbers, out_root=out_root, refresh=refresh)
    for case in skipped:
        print(f"  n={case.n:<3} skipped  {case.reason}: {case.detail}")
    for n, refusal in refusals:
        print(f"  n={n:<3} refused  {refusal}")
    if dry_run:
        for plan in plans:
            print(
                f"  n={plan.n:<3} planned  {plan.source_path} "
                f"(source_n={plan.source_n}, drop={plan.removals}, "
                f"side={plan.catalogue_side}) -> {_relative(plan.witness_path)}"
            )
        pictures = len({plan.url for plan in plans})
        print(
            f"dry run: {len(plans)} to derive from {pictures} picture"
            f"{'' if pictures == 1 else 's'}, {len(skipped)} skipped, "
            f"{len(refusals)} refused, 0 fetched"
        )
        return 1 if refusals else 0

    catalogue_text = default_catalogue_path().read_text(encoding="utf-8")
    if from_parse is None:
        sources, failures = fetch_pictures(plans, jobs=jobs, fetch=fetch)
    else:
        sources, failures = read_parses(plans, from_parse)
    derived: list[DerivedCase] = []
    for index, plan in enumerate(plans, start=1):
        source_text = sources.get(plan.url)
        if source_text is None:
            refusal = failures.get(plan.url) or DerivationRefusedError(
                "fetch-failed", f"{plan.url}: no response retained"
            )
            refusals.append((plan.n, refusal))
            print(f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} refused  {refusal}")
            continue
        try:
            witness = derive_witness(
                plan,
                source_text,
                catalogue_text=catalogue_text,
                retrieved=retrieved,
                parse_revision=parse_revision,
            )
        except DerivationRefusedError as error:
            refusals.append((plan.n, error))
            print(f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} refused  {error}")
            continue
        text = witness_document(witness, schema="../witness.schema.yaml")
        _write(plan.witness_path, text)
        case = DerivedCase(plan, witness, text, plan.witness_path)
        derived.append(case)
        receipt = case.receipt
        print(
            f"  [{index:03d}/{len(plans):03d}] n={plan.n:<3} derived  "
            f"side={str(witness['side'])[:18]} squares={plan.n} drop={plan.removals} "
            f"tolerance={KINGBIRD_TOLERANCE} "
            f"check={'passed' if receipt['check_passed'] else 'failed'} "
            f"-> {_relative(case.path)}"
        )
    existing = sum(1 for case in skipped if case.reason in {"existing", "current"})
    print(
        f"derived {len(derived)}, {'fetched' if from_parse is None else 'read the parse of'} "
        f"{len(sources)} picture{'' if len(sources) == 1 else 's'}, skipped {len(skipped)} "
        f"({existing} already retained), refused {len(refusals)}"
    )
    for n, refusal in refusals:
        print(f"  refused n={n}: {refusal.kind}: {refusal.detail}")
    return 1 if refusals else 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=SUMMARY)
    selection = command.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--range",
        nargs=2,
        type=int,
        metavar=("FIRST", "LAST"),
        help="derive every eligible case in this closed range",
    )
    selection.add_argument("--n", type=int, help="derive one case")
    command.add_argument(
        "--out",
        type=Path,
        default=WITNESS_ROOT,
        help="where witnesses are written (default: the known-best witness root)",
    )
    command.add_argument(
        "--dry-run", action="store_true", help="report the plan without fetching or writing"
    )
    command.add_argument(
        "--jobs",
        type=int,
        default=1,
        help=f"concurrent fetches, 1..{MAX_JOBS} (default: 1)",
    )
    command.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "re-derive a retained witness whose side the catalogue no longer prints, "
            "instead of skipping it; one that still agrees is left alone"
        ),
    )
    command.add_argument(
        "--retrieved",
        default=DERIVED_RETRIEVED_DATE,
        help=f"the retrieval date written witnesses record (default: {DERIVED_RETRIEVED_DATE})",
    )
    command.add_argument(
        "--from-parse",
        type=Path,
        default=None,
        help=(
            "read each picture from a third party's parse of it in this directory "
            "(square-<n>.json, Evan Daniel's export format) instead of fetching the SVG"
        ),
    )
    command.add_argument(
        "--parse-revision",
        default=None,
        help=(
            "where --from-parse's files live upstream, pinned: repository, commit and "
            "directory, e.g. evand/square-packing@<commit>:site/www/data/p"
        ),
    )
    command.add_argument(
        "--compare-pictures",
        action="store_true",
        help=(
            "derive nothing: fetch the picture behind each retained Kingbird witness "
            "again and compare the two, count by count"
        ),
    )
    command.add_argument(
        "--receipt",
        type=Path,
        default=None,
        help="with --compare-pictures, write the comparison here as JSON",
    )
    command.add_argument(
        "--compare-parse",
        type=Path,
        default=None,
        help=(
            "derive nothing: compare a parse directory with the retained witnesses this "
            "repository read from the SVGs themselves, count by count"
        ),
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    command = parser()
    args = command.parse_args(argv)
    if not 1 <= args.jobs <= MAX_JOBS:
        command.error(f"--jobs takes 1 to {MAX_JOBS}, to stay gentle with one small site")
    if args.range is not None:
        first, last = args.range
        if first < 1 or last < first:
            command.error("--range takes a nonempty positive range")
        numbers = list(range(first, last + 1))
    else:
        if args.n < 1:
            command.error("--n takes a positive count")
        numbers = [args.n]
    try:
        if args.compare_parse is not None:
            return compare_parses(numbers, args.compare_parse, out_root=args.out)
        if args.compare_pictures:
            retrieved = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
            readings, refusals = compare_pictures(numbers, out_root=args.out)
            if args.receipt is not None:
                receipt = picture_receipt(readings, refusals, retrieved_utc=retrieved)
                _write(args.receipt, retained_json.dumps(receipt, ensure_ascii=False))
            return report_pictures(readings, refusals)
        return derive(
            numbers,
            out_root=args.out,
            jobs=args.jobs,
            dry_run=args.dry_run,
            retrieved=args.retrieved,
            refresh=args.refresh,
            from_parse=args.from_parse,
            parse_revision=args.parse_revision,
        )
    except DerivationRefusedError as error:
        print(f"refused: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
