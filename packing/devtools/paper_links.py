"""Links from one paper to another, written once in the article as a placeholder.

A paper's renderer pins every relative link to a repository blob at the published
revision (`render_n11_optimality_review._repository_links`), so a sibling paper's page
cannot be written as a relative Markdown link: it would be pinned to a file that is not
in the repository. An article writes `{{PAPER:<slug>}}` or `{{PAPER:<slug>#<anchor>}}`
instead, and the renderer fills it before pinning: with the page-relative
`<slug>.html#anchor` on the page, which works on the site and in a local preview, and
with the absolute site address in the Markdown edition, which is read away from the
site. A slug that is not one of the site's papers is refused here; that every anchor
exists among the target paper's heading ids is checked against the built site, where
all papers are present.
"""

from __future__ import annotations

import re
from typing import Literal

from devtools import render_overview

#: One cross-paper link: a paper's slug and an optional heading anchor.
PAPER_LINK = re.compile(r"\{\{PAPER:(?P<slug>[a-z0-9-]+)(?:#(?P<anchor>[A-Za-z0-9_-]+))?\}\}")

#: The site's papers, by slug, from the one registry (`render_overview.PAPERS`). A
#: placeholder naming any other slug is refused.
PAPER_SLUGS: frozenset[str] = frozenset(paper.slug for paper in render_overview.PAPERS)

Edition = Literal["page", "markdown"]


def paper_link_targets(markdown: str) -> list[tuple[str, str | None]]:
    """Every cross-paper link in `markdown`, in order, as `(slug, anchor)`."""
    return [(match["slug"], match["anchor"]) for match in PAPER_LINK.finditer(markdown)]


def fill_paper_links(markdown: str, *, edition: Edition) -> str:
    """Replace each `{{PAPER:…}}` with the target paper's address for `edition`."""

    def address(match: re.Match[str]) -> str:
        slug, anchor = match["slug"], match["anchor"]
        if slug not in PAPER_SLUGS:
            raise ValueError(f"cross-paper link names no paper of the site: {slug!r}")
        if edition == "page":
            target = f"{slug}.html"
        else:
            target = render_overview.SITE_URL + render_overview.paper_path(slug)
        return target if anchor is None else f"{target}#{anchor}"

    return PAPER_LINK.sub(address, markdown)
