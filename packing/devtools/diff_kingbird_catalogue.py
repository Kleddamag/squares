#!/usr/bin/env python3
"""Compare two retained transcriptions of the Kingbird catalogue, count by count.

Refreshing the retained catalogue is a dated survey rather than a routine fetch, and a
line diff of two transcriptions is the wrong instrument for it: a page that gains one
preamble paragraph shifts every block below it, a credit sentence rewrapped by the page
reads as removed and re-added, and a count that leaves or joins a shared picture is
invisible. This reads both transcriptions through `sqpack.kingbird_catalogue`, resolves
every count the page covers to what the page says about it, and reports each count
whose reading changed, field by field.

**What a count reads as.** A pictured count takes its block: the printed side, closed
form, degree lock, polynomial, rigidity annotation, first credit, and the credit lines
verbatim. A count at or below the page's completeness bound that no block pictures
takes the trivial grid, side `ceil(sqrt(n))`, because the page says so in its own
preamble; so a count that gains its first picture is reported as a side change from the
grid, not as a new entry with no predecessor.

**What counts as a change.** Sides compare as decimals, so `12.83095954472600` and
`12.830959544726` are one value. Credit lines compare sentence by sentence after
whitespace is collapsed, so a sentence the page rewraps across two lines is unchanged
and a sentence it adds is reported verbatim, which is the attribution text a refresh
has to classify.

Usage, from `packing/`, after refreshing the retained capture in place::

    uv run --frozen --all-extras --group dev python -m devtools.diff_kingbird_catalogue \\
        --before 886b1783a

compares the working tree's transcription with the one at that revision. `--before-file`
and `--after-file` compare two files instead, and `--json` prints the complete record.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path

from devtools.audit_kingbird_catalogue import FRONTIER, load_frontier_cases
from sqpack.kingbird_catalogue import (
    CATALOGUE_MARKDOWN,
    NOT_STATED,
    CatalogueEntry,
    completeness_bound_from_text,
    default_catalogue_path,
    index_entries,
    parse_entries,
    split_credit_sentences,
)

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
#: The transcription's path from the repository root, which is what `git show` takes.
REPOSITORY_PATH = f"{ROOT.name}/{CATALOGUE_MARKDOWN}"

#: The fields a count's reading carries, in the order a report lists them.
FIELDS = (
    "side",
    "exact_form",
    "algebraic_degree",
    "minimal_polynomial",
    "catalogue_rigid",
    "found_by",
    "found_year",
    "credits",
    "pictured",
    "svg_path",
    "listed_n",
)


@dataclass(frozen=True)
class CountReading:
    """What one transcription says about one count."""

    n: int
    pictured: bool
    side: str
    exact_form: str | None
    algebraic_degree: int | None
    minimal_polynomial: str | None
    catalogue_rigid: str
    found_by: tuple[str, ...]
    found_year: int | None
    credits: tuple[str, ...]
    """The block's annotation sentences, whitespace collapsed, in page order."""
    svg_path: str | None
    listed_n: tuple[int, ...]
    source_line: int | None


@dataclass(frozen=True)
class CountChange:
    """One count whose reading differs between the two transcriptions."""

    n: int
    before: CountReading | None
    after: CountReading | None
    fields: tuple[str, ...]

    @property
    def added_credits(self) -> tuple[str, ...]:
        """Sentences the later transcription prints for this count and the earlier did not."""
        earlier = set(self.before.credits) if self.before else set()
        return tuple(s for s in (self.after.credits if self.after else ()) if s not in earlier)

    @property
    def removed_credits(self) -> tuple[str, ...]:
        """Sentences the earlier transcription printed for this count and the later does not."""
        later = set(self.after.credits) if self.after else set()
        return tuple(s for s in (self.before.credits if self.before else ()) if s not in later)

    @property
    def direction(self) -> str:
        """`lower`, `higher` or `same`: how the printed side moved; `listed` or `unlisted`."""
        if self.before is None:
            return "listed"
        if self.after is None:
            return "unlisted"
        before, after = Decimal(self.before.side), Decimal(self.after.side)
        if after < before:
            return "lower"
        if after > before:
            return "higher"
        return "same"


def _credits(entry: CatalogueEntry) -> tuple[str, ...]:
    """The block's sentences, each without its closing period.

    The sentence split consumes a period only where whitespace follows it, so a block's
    last sentence would otherwise keep its period and a sentence that stops being last
    -- because the page appended another after it -- would read as removed and re-added.
    """
    text = " ".join((entry.credit_line or "").split())
    return tuple(sentence.removesuffix(".") for sentence in split_credit_sentences(text))


def _sentences(sentences: Sequence[str]) -> str:
    return " ".join(f"{sentence}." for sentence in sentences)


def _pictured(n: int, entry: CatalogueEntry) -> CountReading:
    return CountReading(
        n=n,
        pictured=True,
        side=entry.side_decimal,
        exact_form=entry.exact_form,
        algebraic_degree=entry.algebraic_degree,
        minimal_polynomial=entry.minimal_polynomial,
        catalogue_rigid=entry.catalogue_rigid,
        found_by=entry.found_by,
        found_year=entry.found_year,
        credits=_credits(entry),
        svg_path=entry.svg_path,
        listed_n=entry.listed_n,
        source_line=entry.source_line,
    )


def _grid(n: int) -> CountReading:
    side = str(math.isqrt(n - 1) + 1)
    return CountReading(
        n=n,
        pictured=False,
        side=side,
        exact_form=side,
        algebraic_degree=None,
        minimal_polynomial=None,
        catalogue_rigid=NOT_STATED,
        found_by=(),
        found_year=None,
        credits=(),
        svg_path=None,
        listed_n=(),
        source_line=None,
    )


def readings(text: str) -> dict[int, CountReading]:
    """Every count one transcription covers: its pictured counts and its grid fallback."""
    by_n = index_entries(parse_entries(text))
    bound = completeness_bound_from_text(text)
    covered = {n: _pictured(n, entry) for n, entry in by_n.items()}
    for n in range(1, bound + 1):
        covered.setdefault(n, _grid(n))
    return dict(sorted(covered.items()))


def _differs(field: str, before: CountReading, after: CountReading) -> bool:
    if field == "side":
        return Decimal(before.side) != Decimal(after.side)
    return getattr(before, field) != getattr(after, field)


def compare(before_text: str, after_text: str) -> list[CountChange]:
    """Every count whose reading differs, in count order."""
    earlier, later = readings(before_text), readings(after_text)
    changes: list[CountChange] = []
    for n in sorted(set(earlier) | set(later)):
        before, after = earlier.get(n), later.get(n)
        if before is None or after is None:
            changes.append(CountChange(n, before, after, FIELDS))
            continue
        fields = tuple(field for field in FIELDS if _differs(field, before, after))
        if fields:
            changes.append(CountChange(n, before, after, fields))
    return changes


@dataclass(frozen=True)
class RecordStanding:
    """Where one changed count's new catalogue side stands against its frontier record."""

    n: int
    source_key: str
    value: str
    relation: str
    """`below`, `equal` or `above`: the later catalogue side against the record's value."""


def record_standings(
    changes: Sequence[CountChange], cases: Mapping[int, Mapping[str, object]]
) -> dict[int, RecordStanding]:
    """For each changed count with a frontier record, how its new side compares.

    `below` is the case a refresh has to act on: the catalogue now prints a side smaller
    than the one the record reports. `above` means the record already holds something
    better -- a certified packing from another source -- and the catalogue change moves
    only the baseline that source is measured against.
    """
    standings: dict[int, RecordStanding] = {}
    for change in changes:
        case = cases.get(change.n)
        if case is None or change.after is None:
            continue
        bound = case.get("reported_upper_bound")
        if not isinstance(bound, Mapping):
            continue
        value = str(bound.get("value"))
        after, recorded = Decimal(change.after.side), Decimal(value)
        relation = "below" if after < recorded else "above" if after > recorded else "equal"
        standings[change.n] = RecordStanding(
            change.n, str(bound.get("source_key")), value, relation
        )
    return standings


def read_revision(revision: str, path: str = REPOSITORY_PATH) -> str:
    """The transcription as Git holds it at one revision."""
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _side_cell(reading: CountReading | None) -> str:
    if reading is None:
        return "—"
    side = f"`{reading.side}`" + ("" if reading.pictured else " (grid)")
    if reading.algebraic_degree is not None:
        side += f", degree {reading.algebraic_degree}"
    return side


def _standing_cell(standing: RecordStanding | None) -> str:
    if standing is None:
        return "—"
    return f"`{standing.value}` {standing.source_key}, catalogue {standing.relation}"


def _kept(changes: Sequence[CountChange], max_n: int | None) -> list[CountChange]:
    return [change for change in changes if max_n is None or change.n <= max_n]


def markdown_table(
    changes: Sequence[CountChange],
    *,
    standings: Mapping[int, RecordStanding] | None = None,
    max_n: int | None = None,
) -> str:
    """One row per changed count: sides, fields, the record, and the sentences."""
    lines = [
        "| n | Side before | Side after | Fields | Record | Added | Removed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    known = standings or {}
    for change in _kept(changes, max_n):
        fields = ", ".join(field for field in change.fields if field != "credits")
        lines.append(
            f"| {change.n} | {_side_cell(change.before)} | {_side_cell(change.after)} | "
            f"{fields or 'credits only'} | {_standing_cell(known.get(change.n))} | "
            f"{_sentences(change.added_credits) or '—'} | "
            f"{_sentences(change.removed_credits) or '—'} |"
        )
    return "\n".join(lines)


def summary(
    changes: Sequence[CountChange],
    *,
    standings: Mapping[int, RecordStanding] | None = None,
    max_n: int | None = None,
) -> dict[str, object]:
    """How many counts changed, by field, and where each moved side stands."""
    kept = _kept(changes, max_n)
    known = standings or {}
    by_field = {
        field: [change.n for change in kept if field in change.fields] for field in FIELDS
    }
    by_direction: dict[str, list[int]] = {}
    by_standing: dict[str, list[int]] = {}
    for change in kept:
        if "side" not in change.fields:
            continue
        by_direction.setdefault(change.direction, []).append(change.n)
        standing = known.get(change.n)
        if standing is not None:
            by_standing.setdefault(standing.relation, []).append(change.n)
    return {
        "changed_counts": len(kept),
        "side_changed": len(by_field["side"]),
        "by_field": {field: counts for field, counts in by_field.items() if counts},
        "side_by_direction": by_direction,
        "side_against_record": by_standing,
    }


def record(
    changes: Sequence[CountChange],
    *,
    standings: Mapping[int, RecordStanding] | None = None,
    max_n: int | None = None,
) -> dict[str, object]:
    """The complete comparison as plain data."""
    kept = _kept(changes, max_n)
    known = standings or {}
    return {
        "summary": summary(kept, standings=known),
        "changes": [
            {
                "n": change.n,
                "fields": list(change.fields),
                "direction": change.direction,
                "added_credits": list(change.added_credits),
                "removed_credits": list(change.removed_credits),
                "record": asdict(known[change.n]) if change.n in known else None,
                "before": None if change.before is None else asdict(change.before),
                "after": None if change.after is None else asdict(change.after),
            }
            for change in kept
        ],
    }


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    earlier = command.add_mutually_exclusive_group(required=True)
    earlier.add_argument("--before", metavar="REV", help="the transcription at this revision")
    earlier.add_argument("--before-file", type=Path, help="the earlier transcription")
    command.add_argument(
        "--after-file",
        type=Path,
        default=None,
        help="the later transcription (default: the retained one in the working tree)",
    )
    command.add_argument(
        "--frontier",
        type=Path,
        default=FRONTIER,
        help="the case records each change is set against (default: frontier/)",
    )
    command.add_argument(
        "--max-n", type=int, default=None, help="report only counts at or below this"
    )
    command.add_argument("--json", action="store_true", help="print the complete record")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    before_text = (
        read_revision(args.before)
        if args.before is not None
        else Path(args.before_file).read_text(encoding="utf-8")
    )
    after_path = default_catalogue_path() if args.after_file is None else args.after_file
    changes = compare(before_text, after_path.read_text(encoding="utf-8"))
    standings = record_standings(changes, load_frontier_cases(args.frontier))
    if args.json:
        document = record(changes, standings=standings, max_n=args.max_n)
        json.dump(document, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    print(markdown_table(changes, standings=standings, max_n=args.max_n))
    print()
    print(json.dumps(summary(changes, standings=standings, max_n=args.max_n), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
