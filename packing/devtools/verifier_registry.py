"""The verifier registry: which verification programs stand behind each evidence entry.

`frontier/verifiers.yaml` holds one entry per verification program the evidence register
names, external or first-party, with the digests or revisions that ran and the paths that
hold its source. Each evidence entry names its programs in `verifiers`, and its existing
`relationship_to_generator` says how the code that verified it stands to the code its
result's producer used (epistemics.md, Confirmation):

- `same-implementation`, or `generator`: the producer's own code, re-run. A replay of it
  establishes reproducibility, not independence.
- `shared-components`: separately written code that reuses named parts of it, listed in
  the entry's `shared_components`.
- `independent-implementation`: code that shares none of it, written from the
  mathematics and the certificate format.

This module loads the registry, holds the cross-record rules the JSON Schema cannot state
(`problems`, run by `devtools.validate_schemas`), and gives the views one reading of an
entry's and a result's verification code.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
REGISTRY = ROOT / "frontier" / "verifiers.yaml"

GENERATOR = "generator"
SAME = "same-implementation"
SHARED = "shared-components"
INDEPENDENT = "independent-implementation"
NOT_APPLICABLE = "not-applicable"
UNKNOWN = "unknown-historical"
#: The relations a run of code can hold to its producer's code, from closest to
#: furthest. `generator` and `same-implementation` both mean the producer's own code ran.
RANK = {GENERATOR: 0, SAME: 0, SHARED: 1, INDEPENDENT: 2}
#: The typographic apostrophe the register's prose uses, written as an escape.
APOSTROPHE = "\u2019"
#: How each relation is read beside a rung and after the word "confirmed": the legend the
#: register's views print, and the phrases the prose rule accepts.
LABELS = {
    GENERATOR: f"reproduced with the producer{APOSTROPHE}s code",
    SAME: f"reproduced with the producer{APOSTROPHE}s code",
    SHARED: f"re-implemented, sharing the producer{APOSTROPHE}s components",
    INDEPENDENT: "independently re-implemented",
    NOT_APPLICABLE: "no relation: a proof, a derivation or a report",
    UNKNOWN: "relation not recorded",
}
#: The labels in rank order, once each, for a legend.
LEGEND = tuple(dict.fromkeys(LABELS[relation] for relation in (SAME, SHARED, INDEPENDENT)))
DECIDES = "decides"
EXTERNAL = "external"
FIRST_PARTY = "first-party"
CONFIRMING_ORIGINS = frozenset({"audited-here", "replayed-here", "independently-external"})

#: The independent-implementation entries recorded before 2026-10-02, when the record of
#: what a verifying program's authors read became required, that name no program whose
#: registry entry carries one and carry none of their own. They are exempt by name: the
#: list only shrinks, as each gains a record, and a new entry is never added to it.
GRANDFATHERED_INDEPENDENCE = frozenset(
    {
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-n005-gobel-upper",
        "E-n010-gobel-upper",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-trump-upper",
        "E-n011-wang-li-native-parent-core",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-monotonicity-lower",
        "E-n017-burns-control-decision",
        "E-n017-certified-endpoint",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n040-gobel-upper",
        "E-n061-wand125-point-cover-evand-replay-report",
        "E-n082-gobel-l-upper",
        "E-wand125-tools-n11-row-report",
    }
)


@dataclass(frozen=True)
class Verifier:
    """One registry entry, as the views read it."""

    id: str
    program: str
    author: str
    provenance: str
    role: str
    record: Mapping[str, Any]

    @property
    def decides(self) -> bool:
        return self.role == DECIDES


def load(path: Path = REGISTRY) -> dict[str, Verifier]:
    """The registry's verifiers by id, in file order."""
    document = safe_load(path.read_text(encoding="utf-8"))
    return {
        entry["id"]: Verifier(
            id=entry["id"],
            program=entry["program"],
            author=entry["author"],
            provenance=entry["provenance"],
            role=entry["role"],
            record=entry,
        )
        for entry in document["verifiers"]
    }


def _path_problem(path: str) -> str | None:
    pure = PurePosixPath(path)
    if pure.is_absolute() or pure.as_posix() != path or ".." in pure.parts:
        return "is not a normalized repository-relative path"
    if not (REPO / pure).exists():
        return "does not exist"
    return None


def registry_problems(verifiers: Mapping[str, Verifier], ids: Sequence[str]) -> list[str]:
    """What is wrong with the registry by itself: duplicate ids, and source, version and
    independence-record paths that do not resolve."""
    problems = [
        f"verifiers: duplicate id {verifier_id}"
        for verifier_id in sorted({i for i in ids if ids.count(i) > 1})
    ]
    for verifier in verifiers.values():
        record = verifier.record
        paths = [
            *record.get("source", []),
            *(version["path"] for version in record.get("versions", []) if "path" in version),
        ]
        if "independence_record" in record:
            paths.append(record["independence_record"])
        problems.extend(
            f"verifiers: {verifier.id} names {path}, which {problem}"
            for path in paths
            if (problem := _path_problem(path))
        )
    return problems


def independence_recorded(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> bool:
    """Whether an independent implementation names the record of what its authors read:
    its own `independence_record`, or a deciding program's in the registry."""
    if entry.get("independence_record"):
        return True
    return any(
        verifiers[v].decides and "independence_record" in verifiers[v].record
        for v in entry.get("verifiers") or []
        if v in verifiers
    )


def evidence_problems(
    evidence: Iterable[Mapping[str, Any]], verifiers: Mapping[str, Verifier]
) -> list[str]:
    """What is wrong with the evidence entries' verifier fields, given the registry: every
    id resolves; a replay names a program that decides, since a premise check never
    decides alone, unless the entry claims no relation to the producer's decision
    (`not-applicable`), which is what a premise check recorded on its own is; an
    independent implementation names the record of what its authors
    read, unless it is grandfathered; an entry's own independence record resolves."""
    problems: list[str] = []
    for entry in evidence:
        eid = str(entry.get("id", "<unknown evidence>"))
        named = list(entry.get("verifiers") or [])
        unknown = [verifier_id for verifier_id in named if verifier_id not in verifiers]
        problems.extend(f"{eid}: names unknown verifier {v}" for v in unknown)
        record = entry.get("independence_record")
        if record and (problem := _path_problem(str(record))):
            problems.append(f"{eid}: independence_record {record} {problem}")
        if unknown:
            continue
        if (
            entry.get("replay")
            and named
            and entry.get("relationship_to_generator") != NOT_APPLICABLE
            and not any(verifiers[v].decides for v in named)
        ):
            problems.append(
                f"{eid}: its replay names no program that decides; a premise check never "
                "decides a claim alone"
            )
        if (
            entry.get("relationship_to_generator") == INDEPENDENT
            and eid not in GRANDFATHERED_INDEPENDENCE
            and not independence_recorded(entry, verifiers)
        ):
            problems.append(
                f"{eid}: an independent implementation names the record of what its "
                "authors read: an independence_record, or a deciding program whose "
                "registry entry carries one"
            )
    return problems


def problems(evidence: Sequence[Mapping[str, Any]], path: Path = REGISTRY) -> list[str]:
    """Every cross-record problem of the registry and the evidence's verifier fields."""
    document = safe_load(path.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in document["verifiers"]]
    verifiers = load(path)
    stale = sorted(
        eid
        for eid in GRANDFATHERED_INDEPENDENCE
        if not any(
            entry.get("id") == eid and entry.get("relationship_to_generator") == INDEPENDENT
            for entry in evidence
        )
    )
    return [
        *registry_problems(verifiers, ids),
        *evidence_problems(evidence, verifiers),
        *(
            f"{eid}: grandfathered for its independence record, but no longer an "
            "independent-implementation entry; remove it from GRANDFATHERED_INDEPENDENCE"
            for eid in stale
        ),
    ]


def confirming_runs(entries: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """The entries that confirm by running code: a confirming origin and a passing replay,
    with a relation to the producer's code recorded."""
    return [
        entry
        for entry in entries
        if entry.get("origin") in CONFIRMING_ORIGINS
        and entry.get("replay")
        and entry.get("replay_status") == "passed"
        and entry.get("relationship_to_generator") in RANK
    ]


def strongest(entries: Iterable[Mapping[str, Any]]) -> str | None:
    """The relation furthest from the producer's code among `entries`, or none."""
    relations = [str(entry["relationship_to_generator"]) for entry in entries]
    return max(relations, key=RANK.__getitem__, default=None)


def provenance_label(verifier: Verifier) -> str:
    """A program's provenance as a view prints it, with its role where it only checks
    premises: `external`, `first-party`, `first-party, premises`."""
    return verifier.provenance if verifier.decides else f"{verifier.provenance}, premises"


def result_programs(
    cited: Iterable[Mapping[str, Any]], verifiers: Mapping[str, Verifier]
) -> list[Verifier]:
    """Every program behind a result's cited evidence, each once: deciders first, external
    before first-party, then in registry order."""
    named = {v for entry in cited for v in entry.get("verifiers") or [] if v in verifiers}
    order = {verifier_id: index for index, verifier_id in enumerate(verifiers)}
    return sorted(
        (verifiers[v] for v in named),
        key=lambda verifier: (
            not verifier.decides,
            verifier.provenance != EXTERNAL,
            order[verifier.id],
        ),
    )


#: The relations as a narrow table cell prints them.
SHORT_LABELS = {
    GENERATOR: f"producer{APOSTROPHE}s code",
    SAME: f"producer{APOSTROPHE}s code",
    SHARED: "shared components",
    INDEPENDENT: "independent",
    NOT_APPLICABLE: "no code",
    UNKNOWN: "unknown",
}
#: The order a list of programs is grouped in: deciders before premise checks, external
#: before first-party.
_GROUPS = ((EXTERNAL, True), (FIRST_PARTY, True), (EXTERNAL, False), (FIRST_PARTY, False))
_CODE_METHODS = frozenset(
    {
        "numerical-f64",
        "numerical-multiprecision",
        "interval-certified",
        "exact-algebraic",
        "proof-assistant-checked",
    }
)
_PROOFS = frozenset({"published-proof", "proof-audited"})


def runs_code(entry: Mapping[str, Any]) -> bool:
    """Whether an entry's verification is a program run: a computational method, as
    performed or as reported, or a replay."""
    method = entry.get("method") or entry.get("reported_method")
    return method in _CODE_METHODS or bool(entry.get("replay"))


#: Who ran a third party's check that this repository holds only as their report: its
#: origin is `external`, not `independently-external`, so it confirms nothing here. Until
#: 2026-10-06 it read "a third party's run", and the line in `RESULTS.md` went on to say
#: how the third party's code stood to the producer's, "independently re-implemented",
#: the words a confirmed result's mark uses (`E-k2m4-wand125-validtilt9-report`, T-081).
THIRD_PARTY_REPORT = "reported by a third party, not replayed here"


def run_label(entry: Mapping[str, Any]) -> str:
    """Who ran an entry's verification, in a few words."""
    labels = {
        "replayed-here": "replayed here",
        "audited-here": "audited here",
        "independently-external": "replayed by a third party",
    }
    if (origin := entry.get("origin")) in labels:
        return labels[str(origin)]
    if entry.get("performed_by") == "independent-external":
        return THIRD_PARTY_REPORT
    if (entry.get("method") or entry.get("reported_method")) in _PROOFS:
        return "a published proof"
    return f"the source{APOSTROPHE}s own run"


def programs_text(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str:
    """An entry's programs, grouped by provenance and role:
    `` `V-a`, `V-b` (external); `V-c` (first-party, premises) ``, or why it names none."""
    named = [verifiers[v] for v in entry.get("verifiers") or [] if v in verifiers]
    if not named:
        return "no program held" if runs_code(entry) else "no verification code"
    parts = []
    for provenance, decides in _GROUPS:
        group = [v for v in named if v.provenance == provenance and v.decides == decides]
        if group:
            label = provenance if decides else f"{provenance}, premises"
            parts.append(", ".join(f"`{v.id}`" for v in group) + f" ({label})")
    return "; ".join(parts)


def entry_line(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str:
    """One evidence entry's verification code in a line: who ran it, how its code stands
    to the producer's where a confirming run went beyond the source's own, and its
    programs. A third party's run held only as their report confirms nothing here, so
    its line names no relation, whose labels are the words a confirmation is read in
    (`THIRD_PARTY_REPORT`); `VERIFIERS.md` keeps its code relation in a column of its own."""
    relation = entry.get("relationship_to_generator")
    beyond = entry.get("origin") in CONFIRMING_ORIGINS
    how = f", {LABELS[str(relation)]}" if beyond and relation in RANK else ""
    return f"`{entry['id']}`, {run_label(entry)}{how}: {programs_text(entry, verifiers)}"
