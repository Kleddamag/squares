"""How the results register's prose fields are read: their paragraphs and their links.

`frontier/results.yaml` writes `claim`, `composition`, `notes`, `next_rung` and
`significance.rationale` as folded YAML scalars. In a folded scalar a wrapped line loads
as a space and a blank line as one newline, so a newline in the loaded string divides
paragraphs. Every reader of those fields takes that reading from here: `render_results`
for `RESULTS.md`, `overview_data.prose_html` for the site, and
`check_prose_ceremony`, which holds a paragraph to a length. A reader that wants one
line, as a table's headline cell does, still collapses whitespace itself.

A field may cite its source as a Markdown link with an absolute `http` or `https`
target, `[evand/square-packing](https://github.com/evand/square-packing)`. Markdown
views print it as written; `LINK` is the pattern the site's HTML renderer reads it by.
"""

from __future__ import annotations

import re

#: A Markdown link with an absolute web target, the one link form register prose uses.
LINK = re.compile(r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)")


def paragraphs(text: object) -> list[str]:
    """A register prose field's paragraphs, each collapsed to one line."""
    return [" ".join(block.split()) for block in str(text).split("\n") if block.strip()]
