#!/usr/bin/env python3
"""The data the overview shows, as one typed model read from the record.

Nothing here is typed by hand: every result comes from `frontier/results.yaml`, every
case bound from `frontier/n-NNN.md`, every credit from `resources/bibliography.yaml`,
and every notable source from `resources/notable-sources.yaml`. What is recent, how a
result relates to this project, and whether it still holds a case bound are decided by
`devtools.render_recent_results`, the functions README's generated blocks use, so the
overview and README cannot disagree.

The types below are the contract the overview page renders from; the functions that
fill them are this module's to implement.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Literal

RENDER_INPUTS: tuple[Path, ...] = (Path(__file__),)

Lineage = Literal["this-project", "builds-on-project", "credits-project", "independent"]


@dataclass(frozen=True)
class Link:
    """A labelled link: a record permalink, a case file, a source."""

    label: str
    url: str


@dataclass(frozen=True)
class Bound:
    """One bound as the page prints it, with the relation its claim states.

    `relation` is `≥`, `>`, `≤`, `<` or `=`. `tex` is the bound as LaTeX, for example
    `s(11) > \\frac{31}{8}`; `decimal` is the value cut, never rounded, to the places the
    record states, ending in `…` when it does not terminate.
    """

    n: int
    relation: str
    exact: str
    decimal: str
    tex: str
    value: Fraction | None


@dataclass(frozen=True)
class Result:
    """One register entry, with everything a card or a table row shows."""

    id: str
    n_values: tuple[int, ...]
    cases: str
    headline: str
    claim: str
    bound: Bound | None
    verification: str
    confirmation: str
    significance: int
    novelty: str
    ours: bool
    credit: str
    ai_assistance: str | None
    lineage: Lineage
    relation: str | None
    standing: str
    superseded_by: str | None
    reported: bool
    exact_value: bool
    recent: bool
    established: str | None
    published: str | None
    registered: str
    next_rung: str
    composition: str | None
    records: tuple[Link, ...]
    artifacts: tuple[Link, ...]


@dataclass(frozen=True)
class ResultGroup:
    """A heading and its results, in the order `RESULTS.md` gives them."""

    key: str
    title: str
    results: tuple[Result, ...]


@dataclass(frozen=True)
class RungCount:
    """How many results stand at one rung of one axis, this project's and others'."""

    axis: Literal["V", "C", "S"]
    rung: int
    label: str
    definition: str
    ours: int
    others: int


@dataclass(frozen=True)
class AtlasTotals:
    """The hundred-case atlas's totals, read from `composite-figure.json`."""

    cases: int
    proved: int
    open: int
    recent_verified_lower: int


@dataclass(frozen=True)
class SourceRelease:
    """One reviewed release of a notable source."""

    title: str
    url: str
    reviewed: str
    superseded: bool


@dataclass(frozen=True)
class NotableSource:
    """One card of Other Square Packing Projects."""

    id: str
    title: str
    kind: Literal["website", "catalogue", "release", "repository"]
    url: str
    credit: str
    summary: str
    archive: Link | None
    releases: tuple[SourceRelease, ...]
    cases: tuple[Link, ...]


@dataclass(frozen=True)
class ExplainerEdition:
    """How the explainer's lead result compares with the case record now."""

    lead_result: str
    lead_bound: Bound
    current_bound: Bound
    current_credit: str
    current_results: tuple[str, ...]
    is_current: bool
    first_published: str
    edition: str
    edition_first_published: str

    @property
    def note(self) -> str:
        """The generated line, as plain text with LaTeX math in `$…$`."""
        raise NotImplementedError


@dataclass(frozen=True)
class OverviewData:
    """Everything the overview page renders from, at one commit."""

    edition: str
    data_revision: str
    recent_ours: tuple[Result, ...]
    recent_others: tuple[Result, ...]
    groups: tuple[ResultGroup, ...]
    rung_counts: tuple[RungCount, ...]
    atlas: AtlasTotals
    sources: tuple[NotableSource, ...]
    explainer: ExplainerEdition


def load() -> OverviewData:
    """Read the record once and return the model; cached per process."""
    raise NotImplementedError


def explainer_edition() -> ExplainerEdition:
    """The explainer's lead result against the case record, for its card and its notice."""
    raise NotImplementedError
