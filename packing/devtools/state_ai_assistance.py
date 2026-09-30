#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes case-record prose, whose typography uses curly
# apostrophes and quotation marks.
"""Find, and write, the sentence each case record owes a source that says AI assisted it.

epistemics.md, Results by Others: "Where a source states that AI assisted its work, its
case record and the README say so in the source's own terms." The bibliography notes
record each source's statement, but a case record is hand-written prose, and on
2026-09-29 some fifty of them cited wand125's or Tokoharu's releases in their front
matter without saying so in their bodies. Writing one sentence into each by hand is the
one-off edit `OR-1` asks to be a tool, and checking that none is missing afterwards is
the measurement that should outlive it.

**The statements live in the bibliography.** Each source's `ai_assistance` in
`resources/bibliography.yaml` holds the sentence in the source's own terms (`statement`),
the source's own words that sentence quotes (`quote`), and the retained file that says so
(`where`); the overview reads the same field, so the page, the register and the case
records cannot word a source's statement differently. This tool adds only what is about
case records: where in one the sentence belongs.

Each `Statement` names the bibliography keys whose citation calls for it (every key that
carries the same statement), the paragraph that describes that source's result
(`anchor`, from `ANCHORS`), the sentence to write there, and the words that show the
paragraph already says so (`marker`, the statement's quote). A record owes the statement
when its front matter cites one of the keys and a body paragraph matches the anchor; it
has it when such a paragraph contains the marker. `--apply` appends the sentence to the
first anchored paragraph of every record that owes one; the Markdown formatter then
reflows it. A statement in the bibliography with no anchor here fails on import rather
than going unsaid.

Records whose body never describes the source owe nothing and are listed by `--check`
as such, since where the sentence belongs is then a question for the record rather than
this tool. Statements that differ release by release, as `n-017`'s five successive
external bounds do, are written by hand and are not in `STATEMENTS`.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.state_ai_assistance --check
    uv run --frozen --all-extras --group dev python -m devtools.state_ai_assistance --apply
    ... --below 68    only the records n < 68
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"
RECORD = re.compile(r"^n-(\d{3})\.md$")


@dataclass(frozen=True, slots=True)
class Statement:
    """What one source says of AI assistance, and where a case record says it."""

    keys: frozenset[str]
    anchor: re.Pattern[str]
    sentence: str
    marker: str


#: Where a case record describes each source's result: the paragraph its statement joins.
#: Keyed by one bibliography key of each statement; every key whose `ai_assistance`
#: carries the same statement shares the anchor. In this order, which `STATEMENTS` keeps.
ANCHORS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("[wand125 point bounds 2026]", re.compile(r"wand125")),
    (
        "[Tokoharu density 2026]",
        # Tokoharu's own result, not Tokoharu's checker running someone else's certificate.
        re.compile(r"\[Tokoharu density source\]|Tokoharu’s (?:retained|separately|n\d)"),
    ),
    ("[Kleddamag n11 2026]", re.compile(r"Kleddamag")),
    ("[Guzhou0806 n17 R052]", re.compile(r"\bR0[56]\d\b")),
    ("[n17 weighted certificates 2026-09-20]", re.compile(r"\bR012\b")),
    ("[evand square-packing 2026]", re.compile(r"Evan Daniel")),
)


def said(source: Mapping[str, Any]) -> tuple[str, str] | None:
    """A bibliography entry's statement of AI assistance and its quote, on one line each."""
    statement = source.get("ai_assistance")
    if not statement:
        return None
    sentence = " ".join(str(statement["statement"]).split())
    return sentence, " ".join(str(statement["quote"]).split())


def load_statements(sources: Iterable[Mapping[str, Any]]) -> tuple[Statement, ...]:
    """The bibliography's statements, one per distinct sentence, each with its anchor."""
    carried: dict[tuple[str, str], set[str]] = {}
    for source in sources:
        if (statement := said(source)) is not None:
            carried.setdefault(statement, set()).add(str(source["key"]))
    statements: list[Statement] = []
    for key, anchor in ANCHORS:
        found = [(statement, keys) for statement, keys in carried.items() if key in keys]
        if not found:
            raise ValueError(f"{BIBLIOGRAPHY.name}: {key} states no AI assistance")
        (sentence, marker), keys = found[0]
        if marker not in sentence:
            raise ValueError(f"{key}: its statement does not contain its quote {marker!r}")
        statements.append(Statement(frozenset(keys), anchor, sentence, marker))
    placed = {key for statement in statements for key in statement.keys}
    unplaced = sorted(key for keys in carried.values() for key in keys if key not in placed)
    if unplaced:
        raise ValueError(
            f"{', '.join(unplaced)}: AI assistance stated in {BIBLIOGRAPHY.name} with no "
            "anchor in devtools.state_ai_assistance.ANCHORS"
        )
    return tuple(statements)


STATEMENTS: tuple[Statement, ...] = load_statements(
    safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
)

#: wand125's statement, which `devtools.apply_wand125_rectangles` also writes into the
#: intake paragraph it owns, so that regenerating a record keeps the sentence this tool added.
WAND125 = STATEMENTS[0]


@dataclass(frozen=True, slots=True)
class Paragraph:
    """A run of prose lines in a record's body, by its first and last line index."""

    first: int
    last: int
    text: str


def split_record(text: str) -> tuple[str, list[str]]:
    """The front matter and the body's lines of a case record."""
    _, front, body = text.split("---\n", 2)
    return front, body.split("\n")


def paragraphs(lines: Sequence[str]) -> list[Paragraph]:
    """The body's prose paragraphs: not headings, tables, comments or fenced code."""
    found: list[Paragraph] = []
    fenced = False
    start: int | None = None
    for index, line in enumerate([*lines, ""]):
        if line.startswith("```"):
            fenced = not fenced
        if fenced or line.startswith("```") or not line.strip():
            if start is not None:
                found.append(Paragraph(start, index - 1, " ".join(lines[start:index])))
                start = None
            continue
        if start is None:
            start = index
    return [
        paragraph
        for paragraph in found
        if not lines[paragraph.first].startswith(("#", "|", "<!--"))
    ]


def owed(front: str, lines: Sequence[str]) -> list[tuple[Statement, Paragraph | None, bool]]:
    """Each statement the record's citations call for: its anchor paragraph, and whether said.

    The anchor is the first paragraph describing the source, or None where the body never
    does. A statement is said where any anchored paragraph carries its marker.
    """
    prose = paragraphs(lines)
    result: list[tuple[Statement, Paragraph | None, bool]] = []
    for statement in STATEMENTS:
        if not any(key in front for key in statement.keys):
            continue
        anchored = [paragraph for paragraph in prose if statement.anchor.search(paragraph.text)]
        said = any(statement.marker in paragraph.text for paragraph in anchored)
        result.append((statement, anchored[0] if anchored else None, said))
    return result


def state(text: str) -> str:
    """The record with every owed, unsaid statement appended to its anchor paragraph."""
    front, lines = split_record(text)
    insertions = sorted(
        (
            (paragraph.last, statement.sentence)
            for statement, paragraph, said in owed(front, lines)
            if paragraph is not None and not said
        ),
        reverse=True,
    )
    for last, sentence in insertions:
        lines.insert(last + 1, sentence)
    return text.split("---\n", 2)[0] + "---\n" + front + "---\n" + "\n".join(lines)


def records(below: int | None) -> list[Path]:
    """The case records, in `n` order, those under `below` where it is given."""
    found = []
    for path in sorted(FRONTIER.glob("n-*.md")):
        match = RECORD.match(path.name)
        if match and (below is None or int(match.group(1)) < below):
            found.append(path)
    return found


def report(paths: Iterable[Path]) -> tuple[list[str], list[str]]:
    """The statements still missing, and the ones no paragraph gives a place to."""
    missing: list[str] = []
    unanchored: list[str] = []
    for path in paths:
        front, lines = split_record(path.read_text(encoding="utf-8"))
        for statement, paragraph, said in owed(front, lines):
            cited = ", ".join(sorted(key for key in statement.keys if key in front))
            label = f"{path.name}: {cited}"
            if paragraph is None:
                unanchored.append(label)
            elif not said:
                missing.append(label)
    return missing, unanchored


def apply(paths: Iterable[Path]) -> list[str]:
    changed = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        stated = state(text)
        if stated != text:
            with atomic_output_file(path) as temporary:
                temporary.write_text(stated, encoding="utf-8")
            changed.append(path.name)
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="fail on a missing statement")
    group.add_argument("--apply", action="store_true", help="write the missing statements")
    parser.add_argument("--below", type=int, help="only the records n < BELOW")
    arguments = parser.parse_args(argv)
    paths = records(arguments.below)
    if arguments.apply:
        changed = apply(paths)
        print(f"stated AI assistance in {len(changed)} records: {', '.join(changed)}")
    missing, unanchored = report(paths)
    for label in unanchored:
        print(f"no paragraph describes the source, so nothing is owed: {label}")
    for label in missing:
        print(f"MISSING: {label}", file=sys.stderr)
    if missing:
        return 1
    print(f"every statement owed by {len(paths)} records is made")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
