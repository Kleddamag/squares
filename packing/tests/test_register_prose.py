"""A register prose field keeps its paragraphs and its links on every surface that prints it.

`frontier/results.yaml` writes its prose as folded YAML scalars, where a blank line is a
paragraph break. Until 2026-10-01 every renderer collapsed a field to one line, so a claim
of nine sentences reached `RESULTS.md` and the site as one block. `devtools.register_prose`
is the one reading of a field's paragraphs and of the link form it may carry.
"""

from __future__ import annotations

import yaml

from devtools import overview_data, register_prose, render_results

FOLDED = """claim: >-
  s(45) = 7: the lower half by Evan Daniel's mixed cover,
  the upper half by the 7 x 7 grid.

  Evan Daniel, [evand/square-packing](https://github.com/evand/square-packing),
  building on Burns's and Massaccesi's method.
"""


def test_a_blank_line_in_a_folded_scalar_is_a_paragraph_break_on_every_surface() -> None:
    record = yaml.safe_load(FOLDED)
    first, second = register_prose.paragraphs(record["claim"])
    assert first == (
        "s(45) = 7: the lower half by Evan Daniel's mixed cover, "
        "the upper half by the 7 x 7 grid."
    )
    assert second.startswith("Evan Daniel, [evand/square-packing](")

    # RESULTS.md keeps the break inside one table cell and the link as Markdown.
    cell = render_results.claim_cell(record)
    assert cell == f"{first}<br><br>{second}"

    # The site sets each paragraph, with its mathematics and its link.
    page = overview_data.prose_html(record["claim"], between="</p><p>")
    head, tail = page.split("</p><p>")
    assert "data-kpress-math" in head
    assert '<a href="https://github.com/evand/square-packing">evand/square-packing</a>' in tail
    assert "[evand/square-packing]" not in tail


def test_a_link_must_be_a_web_address_to_be_set_as_one() -> None:
    relative = overview_data.tex_bounds("see [the packet](../resources/web/README.md)")
    assert "<a " not in relative
    scripted = overview_data.tex_bounds('see [x](https://example.org/"onmouseover="x)')
    assert 'href="https://example.org/&quot;onmouseover=&quot;x"' in scripted
