"""Credit and lineage for a registered result, read from the record.

`frontier/RESULTS.md` (`devtools.render_results`) and the site's overview
(`devtools.overview_data`) print the same credit cell and group by the same
lineage, so both read them here and cannot credit a result differently.

Every credit names people, in one form (epistemics.md, Parallel Projects and Their
Credit): `X`, or `X after Y, Z` where X's result rests directly on Y's and Z's proof,
method or tool. A result by others takes its line from its sources in
`resources/bibliography.yaml`, the one home of that text. A result of this project is
credited to `PROJECT_AUTHOR`, and its `after` is the result's own `builds_on.credit`
in `frontier/results.yaml`, which `devtools.check_results` holds to the sources the
result's evidence cites. Nothing here restates either.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from devtools.build_bound_citations import RECENT_SINCE

#: The groups results by others fall into, in reading order, by the lineage their
#: sources carry in the bibliography.
OTHERS = (
    ("builds-on-project", "Building on this project"),
    ("credits-project", "Crediting this project second-hand"),
    ("independent", "Independent of this project"),
    (None, "Published before this project began"),
)


#: The name this project's own results are credited under, the same surname form every
#: other author gets (the owner, 2026-10-01). It is also how other sources' credit lines
#: name this project: `Kleddamag after Levy, Guzhou0806, Mira`.
PROJECT_AUTHOR = "Levy"


def credit_line(record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> str:
    """Who a result is credited to. `RESULTS.md` and the site's overview print this cell.

    For a result by others: its sources' credit lines, each once, in the order the
    attribution names them. For a result of this project: `Levy`, or `Levy after …` with
    the names its `builds_on.credit` lists, in that order.
    """
    if not record.get("attribution"):
        after = (record.get("builds_on") or {}).get("credit") or []
        return PROJECT_AUTHOR + (f" after {', '.join(after)}" if after else "")
    lines = [
        sources[key].get("credit") or ", ".join(sources[key]["authors"])
        for key in record["attribution"]["source_keys"]
    ]
    return "; ".join(dict.fromkeys(lines)).replace("|", r"\|")


def source_lineage(
    record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]
) -> str | None:
    """The group an attributed result reads under: its sources' lineage, if recent.

    Also the relation `render_recent_results.relation` names, read through this function.
    """
    attribution = record["attribution"]
    if attribution["published"] < RECENT_SINCE.isoformat():
        return None
    lineages = {sources[key].get("lineage") for key in attribution["source_keys"]}
    for lineage, _ in OTHERS:
        if lineage in lineages:
            return lineage
    return None
