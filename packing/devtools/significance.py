#!/usr/bin/env python3
"""One place that knows how a result's significance is read and ranked.

`results.yaml` is the record, `epistemics.md` owns the vocabulary, and
`devtools/check_results.py` grants the rungs. Two surfaces now display them --
the synopsis headline block and the pull-request description -- and before this
module existed neither did. Agenda 016 registered `T-014`, `T-015` and `T-016`,
scored all three at `S3`, rendered them into `RESULTS.md`, and then published a
synopsis whose first mention of a significance score was 400 lines in and a
pull request that carried no score for two of the three at all. The record was
complete and the presentation was not, which is the failure this module is here
to make structurally impossible: both surfaces read their rows and their rubric
wording from here, so a result cannot be registered and go unpresented.

The anchors are parsed from `epistemics.md` rather than copied, because a rubric
restated in code is a rubric that drifts from the policy it claims to quote --
the same shape as `D-010`, `D-017` and `D-022`, three hand-maintained views that
drifted from their sources in one week.

The same holds for the verification and confirmation ladders, which the overview's
counts label: `rungs` reads any of the three tables, the two-column `S` rubric and the
three-column `V` and `C` ladders, whose third column is the structural support the
checker derives the rung from.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import NamedTuple

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
#: The reader-facing policy lives at the repository root, not under `packing/`.
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
EPISTEMICS = REPO / "epistemics.md"

#: The three axes `epistemics.md` tabulates rung by rung, and what each is called.
AXES = {"V": "verification", "C": "confirmation", "S": "significance"}

#: The head of one rung's row, `| `S3` |` or `| `V4` |`, in any of the three tables. The
#: cells after it are split on the pipe: `| `S3` | anchor |` for the significance rubric,
#: `| `V4` | meaning | structural support |` for the two ladders.
_RUNG_ROW = re.compile(r"^\|\s*`([VCS])(\d)`\s*\|")


class Rung(NamedTuple):
    """One rung as `epistemics.md` defines it."""

    meaning: str
    """The rung's own words: `Machine-verified`, or the rubric anchor for a score."""
    support: str | None
    """What the checker derives the rung from, for `V` and `C`; None for `S`."""


def rungs(axis: str) -> dict[int, Rung]:
    """One axis's rungs, read from `epistemics.md` at the moment of use."""
    if axis not in AXES:
        raise ValueError(f"no rung table for axis {axis!r}; expected one of {sorted(AXES)}")
    found: dict[int, Rung] = {}
    for line in EPISTEMICS.read_text(encoding="utf-8").splitlines():
        match = _RUNG_ROW.match(line)
        if match is None or match.group(1) != axis:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")][1:]
        rung = int(match.group(2))
        if rung in found or not 1 <= len(cells) <= 2 or not cells[0]:
            raise SystemExit(f"{EPISTEMICS}: the {AXES[axis]} row {axis}{rung} is malformed")
        found[rung] = Rung(cells[0], cells[1] if len(cells) == 2 else None)
    if not found:
        raise SystemExit(f"{EPISTEMICS}: no {AXES[axis]} anchors found; the table moved")
    return found


def anchors(axis: str = "S") -> dict[int, str]:
    """One axis's rungs in their own words; the significance rubric by default."""
    return {rung: row.meaning for rung, row in rungs(axis).items()}


def anchor_for(score: int, axis: str = "S") -> str:
    """The rubric's own words for one rung, or a refusal naming the gap."""
    found = anchors(axis)
    if score not in found:
        raise SystemExit(f"epistemics.md defines no anchor for {axis}{score}")
    return found[score]


def load() -> list[dict]:
    """Every registered result, as recorded."""
    return safe_load(RESULTS.read_text(encoding="utf-8"))["results"]


def scope_label(record: dict) -> str:
    """The `n` a result speaks about, in the register's own two shapes."""
    scope = record["scope"]
    if "n_values" in scope:
        return ", ".join(str(n) for n in scope["n_values"])
    return f"{scope['n_min']}-{scope['n_max']}"


def by_significance(results: list[dict]) -> list[dict]:
    """Significance descending, then confirmation, then id.

    The same order `RESULTS.md` uses. Reading order is the whole purpose of the
    score, so the two prioritized surfaces must not disagree about it.
    """
    return sorted(
        results,
        key=lambda record: (
            -record["significance"]["score"],
            -int(record["confirmation"][1:]),
            record["id"],
        ),
    )


def scored_within(results: list[dict], start: date, end: date) -> list[dict]:
    """Results whose current significance assessment was made in `[start, end]`.

    `scored` dates the assessment rather than the registration, which is the
    field that answers "what did this run establish": a result re-scored inside
    the window is news to the reader even when its id is older, and one
    registered earlier and untouched is not.
    """
    inside = []
    for record in results:
        scored = record["significance"].get("scored")
        if scored is None:
            continue
        when = scored if isinstance(scored, date) else date.fromisoformat(str(scored))
        if start <= when <= end:
            inside.append(record)
    return by_significance(inside)


def headline(record: dict) -> str:
    """The first sentence of a claim, for a table cell that must stay one line."""
    claim = " ".join(record["claim"].split())
    sentence, _, _ = claim.partition(". ")
    return sentence.rstrip(".") + "."
