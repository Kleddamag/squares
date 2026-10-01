"""Rung labels in prose must name the rungs the register holds.

`epistemics.md` derives every rung, so a label written into a sentence is a second copy
of a derived fact, and it goes stale when the ladder or the evidence moves. On 2026-09-30
the ladder changed and the structured `verification` and `confirmation` fields moved with
it; the prose beside them kept saying `V4/C4` for results that stood at `V3/C3`.

This module reads one piece of prose and returns the labels it asserts that no result it
is about holds. It refuses two things:

- **rung 4 or 5 asserted** (`V4`, `C4`, `V5`, `C5`, alone or in a pair) where no result
  the clause is about declares that rung;
- **a rung or a pair below that** which is neither the declared nor the checker-derived
  rung of any result the clause is about.

A clause is about the results it names by id and, in a register field, about the entry
itself; a case-record clause that names no result is about every result scoped to that
`n`. A clause that names an evidence entry and no result describes a part, whose rung
this module does not derive, so only the first rule applies to it.

It does not refuse a statement of what a rung requires or of what a result once held.
A clause carrying a cue of that kind (`needs`, `would`, `requires`, `when`, `if`,
`until`, `once`, `held`, a negation, `V5 by …`) is passed whole. That is deliberate and
it is the limit of the check: it reads labels, not arguments, so a false sentence that
says `would` passes, and whether a requirement is stated correctly is a review
obligation. `check_results` applies this to `claim`, `composition` and `next_rung`, and
to the case records; `notes` is exempt, because the ladder change wrote what each result
held into it.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

#: The register fields held to the rule. `notes` is the dated record of what a result
#: held before the ladder change, so it names old rungs on purpose.
REGISTER_FIELDS = ("claim", "composition", "next_rung")

PAIR = re.compile(r"\b(V[0-5])/(C[0-5])\b")
LABEL = re.compile(r"\b([VC])([0-5])\b")
RESULT_ID = re.compile(r"\bT-\d{3}\b")
EVIDENCE_ID = re.compile(r"\bE-[a-z0-9][a-z0-9-]*")

#: Where one clause ends: a sentence end, a semicolon, a colon or a spaced dash. A cue
#: must sit in the clause of the label it excuses, so splitting more often is stricter.
_CLAUSE_END = re.compile(r"(?<=[.!?])\s+|;\s+|:\s+|\s+(?:--|—)\s+")

#: What marks a clause as a requirement, a hypothetical, a negation or history rather
#: than a statement of the rung a result holds now.
_CUE = re.compile(
    r"""
    \b(?:needs?|needed|requires?|required|would|could|should|must|asks?
       |when|if|unless|until|once|before
       |held|formerly|restores?|waits?\s+on|pending)\b
    | \b(?:not|nor|never|neither|no)\b(?:\W+\w+){0,4}?\W+[VC][0-5]\b   # "does not reach C4"
    | \b(?:above|below|beyond)\W+[VC][0-5]\b                          # "nothing above C2"
    | \b[VC][0-5]\s+by\b               # "V5 by a proof-assistant port", the old shorthand
    """,
    re.VERBOSE | re.IGNORECASE,
)

#: The lowest rung that needs a retained review record (epistemics.md, No Blind Trust).
REVIEWED_FROM = 4


@dataclass(frozen=True)
class Standing:
    """The rungs one result holds: what it declares and what the checker derives."""

    declared_v: str
    declared_c: str
    derived_v: str
    derived_c: str

    def declares(self, label: str) -> bool:
        return label in (self.declared_v, self.declared_c)

    def supports(self, label: str) -> bool:
        return label in (self.declared_v, self.declared_c, self.derived_v, self.derived_c)

    def pairs(self) -> set[tuple[str, str]]:
        return {(self.declared_v, self.declared_c), (self.derived_v, self.derived_c)}


def clauses(text: str) -> list[str]:
    """The clauses of `text` that carry a rung label, each on one line."""
    flat = " ".join(str(text).split())
    return [piece for piece in _CLAUSE_END.split(flat) if piece and LABEL.search(piece)]


def is_requirement(clause: str) -> bool:
    """Whether the clause says what a rung needs, or what was once held, not what is."""
    return bool(_CUE.search(clause))


def label_problems(
    text: str,
    standings: Mapping[str, Standing],
    *,
    own: str | None = None,
    fallback: Iterable[str] = (),
) -> list[str]:
    """The rung labels `text` asserts that no result it is about holds.

    `own` is the register entry the text belongs to; `fallback` is the results a clause
    that names none is about, which a case record sets to the results scoped to its `n`.
    """
    problems: list[str] = []
    for clause in clauses(text):
        if is_requirement(clause):
            continue
        named = [rid for rid in RESULT_ID.findall(clause) if rid in standings]
        subjects = set(named)
        if own is not None:
            subjects.add(own)
        if not subjects:
            subjects = set(fallback)
        about = [standings[rid] for rid in sorted(subjects) if rid in standings]
        # A clause naming an evidence entry and no result describes a part of the claim.
        part = bool(EVIDENCE_ID.search(clause)) and not named
        problems.extend(_clause_problems(clause, about, part=part))
    return problems


def _clause_problems(clause: str, about: list[Standing], *, part: bool) -> list[str]:
    problems: list[str] = []
    quoted = _shorten(clause)
    paired: set[int] = set()
    for match in PAIR.finditer(clause):
        paired.update(range(match.start(), match.end()))
        pair = (match.group(1), match.group(2))
        high = [label for label in pair if int(label[1]) >= REVIEWED_FROM]
        if high:
            problems.extend(
                f"asserts {label}, which no result it is about holds: {quoted}"
                for label in high
                if not any(standing.declares(label) for standing in about)
            )
        elif not part and not any(pair in standing.pairs() for standing in about):
            problems.append(
                f"asserts {pair[0]}/{pair[1]}, which is not the rung of any result it is "
                f"about: {quoted}"
            )
    for match in LABEL.finditer(clause):
        if match.start() in paired:
            continue
        label = match.group(0)
        if int(label[1]) >= REVIEWED_FROM:
            if not any(standing.declares(label) for standing in about):
                problems.append(f"asserts {label}, which no result it is about holds: {quoted}")
        elif not part and not any(standing.supports(label) for standing in about):
            problems.append(
                f"asserts {label}, which is not the rung of any result it is about: {quoted}"
            )
    return problems


def _shorten(clause: str, limit: int = 110) -> str:
    return clause if len(clause) <= limit else clause[: limit - 1].rstrip() + "…"
