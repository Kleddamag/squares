#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes register prose, whose typography uses curly
# apostrophes and the corpus's other non-ASCII marks.
"""Carry wand125's rectangle-density bounds into the Frontier records.

The reported lane takes every standing certificate at the pinned source revision, and
its monotone consequences, wherever it beats the case's current report. The verified
lane takes only certificates whose complete coverage replay is in the retained receipt
``receipts/replay/audit.json``, again with monotone consequences. Replays are expensive
(about a hundred CPU hours for all 44), so they arrive in batches: rerun this after each
batch and it promotes exactly what the receipt now covers. It is idempotent.

What it writes: each affected case's ``reported_lower_bound``, ``verified_lower_bound``,
top-level ``evidence`` and ``resources`` entries, ``source_reviewed``, and one intake
paragraph under the title; and the replay evidence entry's scope and command. Other
prose in a promoted case can still describe the superseded bound, which
``check_case_prose`` reports, and is edited by hand.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python -m devtools.apply_wand125_rectangles
    uv run --frozen --all-extras --group dev python -m devtools.apply_wand125_rectangles --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_write_text

from devtools.audit_wand125_rectangles import CASES, PACKET, REVISION, monotone_bounds
from devtools.generate_frontier_case import display_gap
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
EVIDENCE = FRONTIER / "evidence.yaml"
REPLAY_AUDIT = PACKET / "receipts/replay/audit.json"
PREFLIGHT_AUDIT = PACKET / "receipts/preflight/audit.json"
REVIEW_DATE = "2026-09-27"
SOURCE_KEY = "[wand125 rectangle bounds 2026]"
REPORT = "E-wand125-rectangle-report"
MONOTONE_REPORT = "E-wand125-rectangle-monotone-report"
REPLAY = "E-wand125-rectangle-source-replay"
OURS = {REPORT, MONOTONE_REPORT, REPLAY}
RESOURCE = {
    "key": SOURCE_KEY,
    "role": "lower-bound-proof",
    "local": str(PACKET.relative_to(ROOT / "resources")) + "/wand125-rectangles",
    "url": "https://github.com/wand125/square-packing-bounds",
    "retrieved": True,
}
PACKET_LINK = "../resources/web/" + PACKET.name + "/README.md"
INTAKE = "**External intake, 2026-09-27.**"
SCOPE = "Unrestricted square packing with independent rotations and disjoint interiors."
#: Counts where a stronger bound from another source is registered separately, so this
#: source's certificate is a superseded prior there and moves neither lane: evand's
#: reviewed s(21) >= 5000/1001 and s(32) = 6 (coordinator, 2026-09-27).
SUPERSEDED_PRIORS: dict[int, str] = {
    21: "evand/square-packing s(21) >= 5000/1001 supersedes 997/200",
    32: "evand/square-packing s(32) = 6 supersedes 119/20",
}


@dataclass(frozen=True)
class Plan:
    n: int
    reported: tuple[Fraction, int] | None
    verified: tuple[Fraction, int] | None


def _loose(phrase: str) -> str:
    """A regex for ``phrase`` however Flowmark wrapped it, and with its escaped ``)``."""
    return r"\s+".join(re.escape(word).replace(r"\)", r"\\?\)") for word in phrase.split())


#: The two sentences the Nagamochi-form bodies use to name their verified lower bound.
#: Once this source holds that field, both describe history, so they are rewritten.
_NAGAMOCHI_SUMMARY = re.compile(
    r"Open\. The best known packing gives `s\(\d+\) ≤ (?P<upper>[0-9.]+)`,\s+"
    + _loose("and the strongest lower bound independently verified here is")
    + r"\s+`[0-9.]+`\s+"
    + _loose("from Nagamochi’s general theorem, leaving a gap of")
    + r"\s+`[0-9.]+`\.\s+"
    + _loose(
        "General closed form: s(N) >= min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)."
    )
)
_NAGAMOCHI_SECTION = re.compile(
    _loose(
        "The strongest lower bound independently verified in this record is Nagamochi’s "
        "general closed form, which applies to every `N ≥ 4`:"
    )
)


def _decimal(side: Fraction) -> str:
    text = format(Decimal(side.numerator) / Decimal(side.denominator), "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def replayed() -> dict[int, Fraction]:
    """Cases whose complete coverage replay the retained receipt records as passed."""
    if not REPLAY_AUDIT.exists():
        return {}
    record = json.loads(REPLAY_AUDIT.read_text())
    result: dict[int, Fraction] = {}
    for case in record.get("cases", []):
        replay = case.get("replay") or {}
        summary = replay.get("summary") or {}
        n = case["n"]
        if (
            case.get("status") == "PASS"
            and replay.get("status") == "PASS"
            and summary.get("status") == "VERIFIED"
            and summary.get("angle_cases") == 201
            and Fraction(case["L"]) == CASES[n][1]
        ):
            result[n] = CASES[n][1]
    return result


def _front(n: int) -> tuple[str, dict[str, Any], str]:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    return front, safe_load(front)["packing"], body


def _held_by_us(field: dict[str, Any] | None) -> bool:
    return bool(field) and bool(set(field.get("evidence") or []) & OURS)


def _superseded_by_record(field: dict[str, Any] | None, candidate: Fraction) -> bool:
    """A field another source holds at least as high as ``candidate`` stays as it is."""
    if field is None or _held_by_us(field):
        return False
    return Fraction(Decimal(str(field["value"]))) >= candidate


def plans() -> list[Plan]:
    reported = monotone_bounds({n: side for n, (_name, side) in CASES.items()})
    passed = replayed()
    verified = monotone_bounds(passed) if passed else {}
    result = []
    for n in sorted(reported):
        if n in SUPERSEDED_PRIORS:
            continue
        _front_text, payload, _body = _front(n)
        report: tuple[Fraction, int] | None = reported[n]
        if _superseded_by_record(payload.get("reported_lower_bound"), reported[n][0]):
            report = None
        proof = verified.get(n)
        if proof is not None and _superseded_by_record(
            payload.get("verified_lower_bound"), proof[0]
        ):
            proof = None
        if report is not None or proof is not None:
            result.append(Plan(n, report, proof))
    return result


def _block(name: str, value: dict[str, Any]) -> str:
    dumped = yaml.safe_dump({name: value}, allow_unicode=True, sort_keys=False, width=100)
    return "".join("  " + line + "\n" for line in dumped.splitlines())


def _replace_block(front: str, name: str, block: str) -> str:
    pattern = re.compile(rf"^  {name}:\n(?:^    .*\n)*", re.MULTILINE)
    if not pattern.search(front):
        raise ValueError(f"no {name} block")
    return pattern.sub(lambda _match: block, front, count=1)


def _prepend_list(front: str, name: str, items: list[str]) -> str:
    """Insert raw list items at the head of a top-level ``packing`` list."""
    marker = f"\n  {name}:\n"
    index = front.index(marker) + len(marker)
    return front[:index] + "".join(items) + front[index:]


def reported_field(n: int, side: Fraction, source: int) -> dict[str, Any]:
    direct = source == n
    note = (
        "Rectangle-density certificate in Tokoharu's format, reported in the retained source "
        f"at {REVISION[:7]} and accepted there by Tokoharu's unchanged interval checker. The "
        "verified lane records the local replay separately."
        if direct
        else f"wand125's n={source} rectangle-density certificate has mass below {n}, so "
        f"monotonicity carries its bound to n={n}. The verified lane records the local "
        "replay separately."
    )
    return {
        "value": _decimal(side),
        "exact_form": str(side),
        "kind": "counting" if direct else "monotonicity",
        "proved_by": ["wand125"],
        "proved_year": 2026,
        "source_key": SOURCE_KEY,
        "note": note,
        "scope": SCOPE,
        "evidence": [REPORT if direct else MONOTONE_REPORT],
    }


def _mass(n: int) -> Fraction:
    record = json.loads(PREFLIGHT_AUDIT.read_text())
    return next(Fraction(case["mass_exact"]) for case in record["cases"] if case["n"] == n)


def intake(plan: Plan) -> str:
    n = plan.n
    link = f"[rectangle-density source]({PACKET_LINK})"
    sentences: list[str] = []
    if n in CASES:
        side = CASES[n][1]
        mass = _mass(n)
        claim = f"`s({n}) >= {side} = {_decimal(side)}`"
        if plan.reported is not None and plan.reported[1] != n:
            claim = f"a direct `{side} = {_decimal(side)}` certificate for this case"
        sentences.append(
            f"{INTAKE} wand125’s {link} at `{REVISION[:7]}` reports {claim}, with total "
            f"mass `{mass} = {_decimal(mass)} < {n}`, accepted by Tokoharu’s unchanged "
            "interval checker."
        )
    else:
        sentences.append(
            f"{INTAKE} wand125’s {link} at `{REVISION[:7]}` has no certificate at `n = {n}`."
        )
    if plan.reported is not None and plan.reported[1] != n:
        side, source = plan.reported
        sentences.append(
            f"Its n{source} certificate, of mass `{_mass(source)} < {n}`, gives the stronger "
            f"`s({n}) >= {side} = {_decimal(side)}` by monotonicity, the reported lower bound."
        )
    if plan.verified is not None:
        side, source = plan.verified
        if source == n:
            sentences.append(
                "The complete 201-direction coverage replay here accepted it again, after the "
                "first-party exact audit bound the regenerated checker input to the published "
                "digest and checked the mass and net premises, so it is also verified."
            )
        else:
            sentences.append(
                f"The replayed n{source} certificate carries "
                f"`s({n}) >= {side} = {_decimal(side)}` here by monotonicity, which is the "
                "verified lower bound."
            )
    elif n in CASES:
        sentences.append(
            "The first-party exact audit binds the regenerated checker input to the published "
            "digest and checks the mass and net premises; the complete coverage replay has not "
            "yet run here, so the verified lower bound is unchanged."
        )
    return " ".join(sentences)


_SELECTED_REPORT = re.compile(_loose("The selected external report, ["))
_REPORTED_ONLY = re.compile(
    _loose(
        "This changes the reported source field only; the independently verified lower "
        "bound remains"
    )
    + r"\s+`(?P<verified>[^`]+)`\."
)


def _retire_selected_report(rest: str, plan: Plan) -> str:
    """The generator's DS7 paragraph calls its report the selected one; it no longer is."""
    rest = _SELECTED_REPORT.sub("The earlier external report, [", rest, count=1)

    def reported_only(match: re.Match[str]) -> str:
        if plan.verified is not None:
            return (
                "wand125’s rectangle-density certificate above has since replaced it in both "
                "the reported and the verified field."
            )
        return (
            "wand125’s rectangle-density certificate above has since replaced it in the "
            "reported field; the independently verified lower bound remains "
            f"`{match['verified']}`."
        )

    return _REPORTED_ONLY.sub(reported_only, rest, count=1)


def _retire_nagamochi_prose(rest: str, plan: Plan, upper: str) -> str:
    """Point a Nagamochi-form body's summary at the promoted verified lower bound."""
    assert plan.verified is not None
    side, source = plan.verified
    origin = (
        "wand125’s rectangle-density certificate"
        if source == plan.n
        else f"wand125’s n{source} rectangle-density certificate by monotonicity"
    )

    def summary(match: re.Match[str]) -> str:
        return (
            f"Open. The best known packing gives `s({plan.n}) ≤ {match['upper']}`, and the "
            f"verified lower bound is `s({plan.n}) ≥ {side} = {_decimal(side)}`, "
            f"from {origin}, "
            f"leaving a gap of `{display_gap(upper, _decimal(side))}`."
        )

    rest = _NAGAMOCHI_SUMMARY.sub(summary, rest, count=1)
    return _NAGAMOCHI_SECTION.sub(
        "Nagamochi’s general closed form, the verified lower bound before this certificate, "
        "applies to every `N ≥ 4`:",
        rest,
        count=1,
    )


def apply_case(plan: Plan) -> str:
    front, payload, body = _front(plan.n)
    if plan.reported is not None:
        front = _replace_block(
            front,
            "reported_lower_bound",
            _block("reported_lower_bound", reported_field(plan.n, *plan.reported)),
        )
    if plan.verified is not None:
        side = plan.verified[0]
        front = _replace_block(
            front,
            "verified_lower_bound",
            _block(
                "verified_lower_bound",
                {"value": _decimal(side), "exact_form": str(side), "evidence": [REPLAY]},
            ),
        )
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{REVIEW_DATE}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    wanted = []
    if plan.reported is not None:
        wanted.append(REPORT if plan.reported[1] == plan.n else MONOTONE_REPORT)
        if plan.reported[1] != plan.n and plan.n in CASES:
            wanted.append(REPORT)
    if plan.verified is not None:
        wanted.append(REPLAY)
    existing = payload.get("evidence") or []
    front = _prepend_list(
        front, "evidence", [f"  - {item}\n" for item in wanted if item not in existing]
    )
    if not any(
        resource.get("key") == SOURCE_KEY for resource in payload.get("resources") or []
    ):
        dumped = yaml.safe_dump([RESOURCE], allow_unicode=True, sort_keys=False, width=100)
        front = _prepend_list(
            front, "resources", ["".join("  " + line + "\n" for line in dumped.splitlines())]
        )
    paragraph = intake(plan)
    title, _, rest = body.partition("\n\n")
    if rest.startswith(INTAKE):
        existing, _, rest = rest.partition("\n\n")
        # Flowmark rewraps the paragraph at commit; the same words are the same paragraph.
        if " ".join(existing.split()) == paragraph:
            paragraph = existing
    if plan.reported is not None:
        rest = _retire_selected_report(rest, plan)
    if plan.verified is not None:
        rest = _retire_nagamochi_prose(
            rest, plan, str(payload["reported_upper_bound"]["value"])
        )
    body = f"{title}\n\n{paragraph}\n\n{rest}"
    return f"---\n{front}---\n{body}"


def update_evidence_scope(text: str, verified: dict[int, tuple[Fraction, int]]) -> str:
    start = text.index(f"  - id: {REPLAY}\n")
    end = text.find("\n  - id: ", start + 1)
    entry = text[start:end]
    scope = ", ".join(str(n) for n in sorted(verified))
    entry = re.sub(
        r"^    scope: .*$",
        f"    scope: {{n_values: [{scope}]}}",
        entry,
        count=1,
        flags=re.MULTILINE,
    )
    direct = " ".join(
        f"--n {n}" for n in sorted({source for _side, source in verified.values()})
    )
    command = (
        "    replay: >-\n"
        '      wand125_replay_output="$(mktemp -d '
        '"${TMPDIR:-/tmp}/wand125-rectangle-replay.XXXXXX")" &&\n'
        "      .venv/bin/python3 -m devtools.audit_wand125_rectangles "
        '--out "$wand125_replay_output"\n'
        f"      --replay --workers 2 {direct}\n"
    )
    entry = re.sub(
        r"^    replay: >-\n(?:^      .*\n)+", command, entry, count=1, flags=re.MULTILINE
    )
    return text[:start] + entry + text[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args()
    drift: list[str] = []
    selected = plans()
    for plan in selected:
        path = FRONTIER / f"n-{plan.n:03d}.md"
        rendered = apply_case(plan)
        if rendered != path.read_text(encoding="utf-8"):
            drift.append(str(path.relative_to(ROOT)))
            if not args.check:
                atomic_write_text(path, rendered)
    verified = {plan.n: plan.verified for plan in selected if plan.verified is not None}
    text = EVIDENCE.read_text(encoding="utf-8")
    if f"  - id: {REPLAY}\n" in text and verified:
        updated = update_evidence_scope(text, verified)
        if updated != text:
            drift.append(str(EVIDENCE.relative_to(ROOT)))
            if not args.check:
                atomic_write_text(EVIDENCE, updated)
    for item in drift:
        print(("drift: " if args.check else "wrote: ") + item)
    return 1 if args.check and drift else 0


if __name__ == "__main__":
    sys.exit(main())
