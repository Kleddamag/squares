"""Credit and lineage for a result by others, read from the bibliography.

`frontier/RESULTS.md` (`devtools.render_results`) and the site's overview
(`devtools.overview_data`) print the same credit cell and group by the same
lineage, so both read them here and cannot credit a result differently. The credit
text itself has one home, `resources/bibliography.yaml`; nothing here restates it.
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


def credit_line(record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> str:
    """The sources' credit lines, each once, in the order the attribution names them.

    `RESULTS.md` and the site's overview print this same cell.
    """
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
