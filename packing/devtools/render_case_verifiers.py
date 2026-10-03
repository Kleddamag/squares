#!/usr/bin/env python3
"""Write each case record's Verification Code section: the programs behind its verified bounds.

A case record, `frontier/n-NNN.md`, is hand-written prose over a machine front matter whose
`verified_lower_bound` and `verified_upper_bound` name the evidence each verified bound
rests on. This writes one section into the prose, kept between two markers, that names
for each of those evidence entries who ran it, how the code that ran stands to the code
the result's producer used (`relationship_to_generator`, epistemics.md, Confirmation),
and the programs themselves, each external or first-party (`frontier/verifiers.yaml`).
A reader of the case then sees which programs stand behind its verified lane, and
whether they were the producer's own or a re-implementation.

The section sits just before the record's closing guideline comment, or at its end when
it has none. Everything outside the markers is the record's own and is left as it was;
the section is rewritten from the records on every `--update`, and `--check` fails when
any case's section differs from what the records say. The section is plain Markdown the
formatter leaves alone: sentences on lines of their own and a table.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_case_verifiers --update
    uv run --frozen --all-extras --group dev python -m devtools.render_case_verifiers --check
"""

from __future__ import annotations

import argparse
import functools
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from devtools.verifier_registry import (
    SHORT_LABELS,
    Verifier,
    load,
    programs_text,
    run_label,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
EVIDENCE = FRONTIER / "evidence.yaml"

BEGIN = "<!-- BEGIN verification code: written by devtools.render_case_verifiers -->"
END = "<!-- END verification code -->"
FOOTER = "<!-- This document follows common-doc-guidelines.md."
#: The verified lane's two fields, and how the table names each.
FIELDS = (
    ("verified_lower_bound", "verified lower"),
    ("verified_upper_bound", "verified upper"),
)
APOSTROPHE = chr(0x2019)


def _front_matter(text: str) -> Mapping[str, Any]:
    return safe_load(text.split("---\n")[1])["packing"]


def section(
    case: Mapping[str, Any],
    evidence: Mapping[str, Mapping[str, Any]],
    verifiers: Mapping[str, Verifier],
) -> list[str]:
    """The section's lines for one case, markers included."""
    rows = []
    for field, label in FIELDS:
        for ref in (case.get(field) or {}).get("evidence") or []:
            entry = evidence.get(ref)
            if entry is None:
                continue
            code = SHORT_LABELS.get(str(entry.get("relationship_to_generator")), "-")
            rows.append(
                f"| {label} | `{ref}` | {run_label(entry)} | {code} "
                f"| {programs_text(entry, verifiers)} |"
            )
    return [
        BEGIN,
        "",
        "## Verification Code",
        "",
        f"The programs behind this case{APOSTROPHE}s verified bounds, by their evidence.",
        "The code column says how the code that ran stands to the code its producer used.",
        "[`VERIFIERS.md`](VERIFIERS.md) says what each program is and whose it is.",
        "",
        "| bound | evidence | run | code | programs |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
        END,
    ]


@functools.cache
def _records() -> tuple[dict[str, Mapping[str, Any]], dict[str, Verifier]]:
    evidence = {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    return evidence, load()


def section_for(case: Mapping[str, Any]) -> list[str]:
    """One case's section from the committed records, for a generator drafting a record."""
    evidence, verifiers = _records()
    return section(case, evidence, verifiers)


def refresh(text: str) -> str:
    """A whole case record with its section rewritten from its own front matter, for a
    tool that has just changed the evidence a verified bound cites."""
    return place(text, section_for(_front_matter(text)))


def place(text: str, lines: Sequence[str]) -> str:
    """The case text with its section replaced, or placed before the footer comment."""
    block = "\n".join(lines)
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        end = text.index(END) + len(END)
        return text[:start] + block + text[end:]
    if FOOTER in text:
        at = text.index(FOOTER)
        return text[:at] + block + "\n\n" + text[at:]
    return text.rstrip("\n") + "\n\n" + block + "\n"


def render_all(frontier: Path = FRONTIER) -> dict[Path, tuple[str, str]]:
    """Every case record's current text and the text it should have, by path."""
    evidence = {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    verifiers = load()
    out: dict[Path, tuple[str, str]] = {}
    for path in sorted(frontier.glob("n-*.md")):
        text = path.read_text(encoding="utf-8")
        out[path] = (text, place(text, section(_front_matter(text), evidence, verifiers)))
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true")
    group.add_argument("--check", action="store_true")
    options = parser.parse_args(argv)
    rendered = render_all()
    stale = [path for path, (current, wanted) in rendered.items() if current != wanted]
    if options.update:
        for path in stale:
            path.write_text(rendered[path][1], encoding="utf-8")
        print(f"wrote the verification-code section of {len(stale)} case records")
        return 0
    if stale:
        names = ", ".join(path.name for path in stale[:8])
        more = f" and {len(stale) - 8} more" if len(stale) > 8 else ""
        print(
            f"{len(stale)} case records' verification-code sections are stale ({names}{more}); "
            "run devtools.render_case_verifiers --update"
        )
        return 1
    print(f"{len(rendered)} case records' verification-code sections agree with the records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
