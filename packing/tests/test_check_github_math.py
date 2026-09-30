"""`devtools.check_github_math` without the network: reading GitHub's page and comparing.

The fetch is `curl` against github.com and is exercised only by running the tool. What is
pinned here is everything after it: where the rendered Markdown sits in the page, how the
TeX comes out of GitHub's twice-escaped `<math-renderer>` elements, and that a formula
GitHub split, dropped or rewrote is reported on both sides of the comparison.
"""

from __future__ import annotations

import html
import json

import pytest

from devtools.check_github_math import (
    ShownAsSourceError,
    compare,
    rendered_html,
    rendered_math,
)


def page(blob: dict[str, object]) -> str:
    island = json.dumps({"payload": {"codeViewBlobRoute": blob}})
    script = '<script type="application/json" data-target="react-app.embeddedData">'
    return f"<html><body>{script}{island}</script></body></html>"


def formula(tex: str, *, display: bool = False) -> str:
    """One formula as GitHub writes it: delimited, then escaped twice."""
    delimited = f"$${tex}$$" if display else f"${tex}$"
    escaped = html.escape(html.escape(delimited))
    return f'<math-renderer class="js-inline-math">{escaped}</math-renderer>'


def test_the_rendered_markdown_is_read_from_the_pages_data_island() -> None:
    assert rendered_html(page({"richText": "<p>hello</p>"})) == "<p>hello</p>"


def test_a_file_github_will_not_render_is_skipped_not_failed() -> None:
    with pytest.raises(ShownAsSourceError):
        rendered_html(page({"richText": None, "richTextTruncated": True}))


def test_a_page_this_cannot_read_is_an_error() -> None:
    with pytest.raises(ValueError, match="layout has changed"):
        rendered_html("<html></html>")
    with pytest.raises(ValueError, match="no rendered Markdown"):
        rendered_html(page({"richText": None, "richTextTruncated": False}))


def test_tex_comes_back_unescaped_and_undelimited() -> None:
    rich = f"<p>{formula('s(11) < 4')} and {formula(r'\frac{a}{b} \ge 0', display=True)}</p>"
    assert rendered_math(rich) == ["s(11) < 4", r"\frac{a}{b} \ge 0"]


def test_every_span_rendered_once_and_unchanged_passes() -> None:
    source = "Bounds $s(11) < 4$ and $n \\ge 1$, and `$not math$` in code.\n"
    rich = f"<p>{formula('s(11) < 4')} {formula(r'n \ge 1')}</p>"
    result = compare("x.md", source, rich)
    assert result.ok
    assert (result.expected, result.rendered) == (2, 2)


def test_a_rewritten_formula_is_missing_on_one_side_and_extra_on_the_other() -> None:
    """GitHub read `\\{` as a Markdown escape: the braces are gone from what it drew."""
    source = "Here $\\max\\{0,a\\}$ is it.\n"
    rich = f"<p>Here {formula(r'\max{0,a}')} is it.</p>"
    result = compare("x.md", source, rich)
    assert not result.ok
    assert result.missing == (r"\max\{0,a\}",)
    assert result.extra == (r"\max{0,a}",)


def test_a_formula_left_as_dollars_is_missing() -> None:
    source = "The $B$ and the $Q$.\n"
    rich = f"<p>The $B$ and the {formula('Q')}.</p>"
    result = compare("x.md", source, rich)
    assert result.missing == ("B",)
    assert result.extra == ()
