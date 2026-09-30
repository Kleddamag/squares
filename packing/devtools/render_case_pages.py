"""Render the case records: every case `n = 1…324` as one record, at one address each.

A case record is what a reader wants after pointing at a case anywhere on the site: the
known-best packing drawn large, every bound with its exact form or minimal polynomial as
math and its credit, the status and the gap, every registered result that concerns the
case with its rungs, the evidence and sources, and the case file's own prose. The atlas
grid on the overview and the `n` column of the frontier atlas both open it, in the same
framed popover (`overview/case-popover.js`), at the same address: `cases.html#n-11`.

The records are one page, not 324. A site page carries about 1.6 MB of inlined faces
and KaTeX, since every page is self-contained; 324 copies of that would be over 500 MB.
One page holds every record, and `overview/case-view.js` shows only the one its
fragment names, so a frame opened on `#n-11` shows case 11 alone and moving to `#n-12`
inside it reloads nothing. Without scripts the page lists every record and the fragment
scrolls to the one asked for.

Every value is read from the case's `SquarePackingCase/v2` record and from
`frontier/results.yaml`, as the frontier atlas reads them. The case files write their
mathematics in code spans; the prose here sets each span that is mathematics as `$…$`
(`code_tex`), and leaves identifiers, paths and commands as code.

The page is one of `render_overview.PAGES`; render it with the rest of the site:

    uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR
"""

from __future__ import annotations

import html
import re
from functools import cache
from pathlib import Path
from typing import Any

from devtools import render_frontier_page as frontier
from devtools import render_research_tables as tables

PACKING = Path(__file__).resolve().parents[1]
TEMPLATES = PACKING / "devtools" / "templates"
CASES_ARTICLE = TEMPLATES / "cases-article.md"
CASE_VIEW_SCRIPT = PACKING / "devtools" / "overview" / "case-view.js"
CASE_POPOVER_SCRIPT = PACKING / "devtools" / "overview" / "case-popover.js"

#: Where the records are served.
CASES_PAGE = "cases.html"
#: The one popover a page opens every case record in.
CASE_POPOVER_ID = "pop-case"

#: Every file this page reads beyond the frontier atlas's own inputs.
CASES_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    CASES_ARTICLE,
    CASE_VIEW_SCRIPT,
    CASE_POPOVER_SCRIPT,
)

#: A case file's minimal polynomial longer than this, in characters, opens on request.
POLYNOMIAL_OPEN = 400
#: A result about more cases than this is summarized in each of their records, with its
#: claim and records left to its row in the overview's results table.
BROAD_RESULT = 4


def case_url(n: int) -> str:
    """A case record's address, the same from every page that links it."""
    return f"{CASES_PAGE}#n-{n}"


def case_link(n: int, content: str, *, classes: str = "", label: str = "") -> str:
    """A link to case `n`'s record that `case-popover.js` opens in the shared popover.

    Without scripts it is an ordinary link to the record page.
    """
    attributes = f' class="{classes}"' if classes else ""
    if label:
        attributes += f' aria-label="{html.escape(label)}"'
    return f'<a{attributes} href="{case_url(n)}" data-case="{n}">{content}</a>'


def case_popover() -> str:
    """The one popover a page opens every case record in, framed as a card's page
    popover is. `case-popover.js` points its frame and its Expand button at the case
    that was pressed; the frame keeps its page between cases, so a second case only
    moves its fragment."""
    return (
        f'<div class="site-popover" id="{CASE_POPOVER_ID}" popover '
        'data-go="page" data-case-popover>'
        f'<button type="button" class="site-popover-close" popovertarget="{CASE_POPOVER_ID}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        '<span class="site-card-label">Case record</span>'
        '<p class="site-popover-value" data-math-face="serif" data-case-title>Case record</p>'
        '<iframe class="site-popover-frame" title="Case record" data-case-frame></iframe>'
        '<p class="site-popover-actions"><a class="site-popover-action" data-go="page" '
        f'data-case-expand href="{CASES_PAGE}">See All Cases</a></p>'
        "</div>"
    )


# ---------- Mathematics in the case files' code spans ----------

_TOKEN = re.compile(
    r"(?P<space>\s+)"
    r"|(?P<sci>\d+(?:\.\d+)?[eE][-+]?\d+)"
    r"|(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
    r"|(?P<ellipsis>\.\.\.|\u2026)"
    r"|(?P<word>[A-Za-z]+(?:_\d+)?)"
    r"|(?P<greek>[\u03b1-\u03c9\u0391-\u03a9])"
    r"|(?P<sup>[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207b]+)"
    r"|(?P<sub>[\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089]+)"
    r"|(?P<rel><=|>=|[=<>\u2264\u2265\u2248\u2260\u2208\u2209\u2282\u2286\u2192])"
    r"|(?P<op>[-+\u2212\u00b1*\u00b7\u00d7/,|'\u2032\u00b0%!^])"
    r"|(?P<vulgar>[\u00bd\u00bc\u00be\u2153\u2154])"
    r"|(?P<open>[(\[{\u2308\u230a])"
    r"|(?P<close>[)\]}\u2309\u230b])"
    r"|(?P<root>\u221a)"
    r"|(?P<set>[\u211a\u211d\u2124\u2115\u221e])"
    r"|(?P<dot>\.)"
)
_FUNCTIONS = {
    "sqrt": r"\sqrt",
    "floor": r"\lfloor",
    "ceil": r"\lceil",
    "min": r"\min",
    "max": r"\max",
    "cos": r"\cos",
    "sin": r"\sin",
    "tan": r"\tan",
    "log": r"\log",
    "arcsin": r"\arcsin",
    "arccos": r"\arccos",
    "arctan": r"\arctan",
    "epsilon": r"\varepsilon",
    "delta": r"\delta",
    "pi": r"\pi",
}
_GREEK = dict(
    zip(
        "\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc"
        "\u03bd\u03be\u03bf\u03c0\u03c1\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8\u03c9",
        [
            *(r"\alpha", r"\beta", r"\gamma", r"\delta", r"\varepsilon", r"\zeta"),
            *(r"\eta", r"\theta", r"\iota", r"\kappa", r"\lambda", r"\mu"),
            *(r"\nu", r"\xi", "o", r"\pi", r"\rho", r"\sigma"),
            *(r"\tau", r"\upsilon", r"\varphi", r"\chi", r"\psi", r"\omega"),
        ],
        strict=True,
    )
) | {
    "\u0394": r"\Delta",
    "\u0398": r"\Theta",
    "\u03a3": r"\Sigma",
    "\u03a0": r"\Pi",
    "\u03a9": r"\Omega",
}
_SYMBOLS = {
    "<=": r"\le",
    ">=": r"\ge",
    "\u2264": r"\le",
    "\u2265": r"\ge",
    "\u2248": r"\approx",
    "\u2260": r"\ne",
    "\u2212": "-",
    "*": r"\cdot",
    "\u00b7": r"\cdot",
    "\u00d7": r"\times",
    "\u00b0": r"^\circ",
    "\u2032": "'",
    "%": r"\%",
    "{": r"\{",
    "}": r"\}",
    "\u2308": r"\lceil",
    "\u2309": r"\rceil",
    "\u230a": r"\lfloor",
    "\u230b": r"\rfloor",
    "\u211a": r"\mathbb{Q}",
    "\u211d": r"\mathbb{R}",
    "\u2124": r"\mathbb{Z}",
    "\u2115": r"\mathbb{N}",
    "\u221e": r"\infty",
    "\u00b1": r"\pm",
    "\u2208": r"\in",
    "\u2209": r"\notin",
    "\u2282": r"\subset",
    "\u2286": r"\subseteq",
    "\u2192": r"\to",
    "\u00bd": r"\tfrac{1}{2}",
    "\u00bc": r"\tfrac{1}{4}",
    "\u00be": r"\tfrac{3}{4}",
    "\u2153": r"\tfrac{1}{3}",
    "\u2154": r"\tfrac{2}{3}",
}
_SUPERSCRIPT = str.maketrans(
    "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u207b", "0123456789-"
)
_SUBSCRIPT = str.maketrans(
    "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089", "0123456789"
)
_ROOT_NEXT = ([("word", "sqrt")], [("root", "\u221a")])
_PAIRS = {"(": ")", "[": "]", "{": "}", "\u2308": "\u2309", "\u230a": "\u230b"}
#: What marks a code span as a name rather than mathematics: a letter run straight into
#: a digit (`V4`, `n011`), or a hyphenated identifier (`T-026`, `n-012`).
_SCIENTIFIC = re.compile(r"\d+(?:\.\d+)?[eE][-+]?\d+")
_IDENTIFIER = re.compile(r"[A-Za-z]\d|[A-Za-z]-[A-Za-z0-9]")


def _tokens(code: str) -> list[tuple[str, str]] | None:
    """The span's tokens, spaces dropped; `None` when any character is not mathematics."""
    found: list[tuple[str, str]] = []
    position = 0
    while position < len(code):
        match = _TOKEN.match(code, position)
        if match is None or match.lastgroup is None:
            return None
        if match.lastgroup != "space":
            found.append((match.lastgroup, match.group(0)))
        position = match.end()
    return found


class _RefusedError(ValueError):
    """The span is not mathematics this reader can set."""


def _group(tokens: list[tuple[str, str]], start: int) -> tuple[str, int]:
    """The TeX of the bracketed group opening at `start`, without its brackets, and the
    index after its closing bracket."""
    closer = _PAIRS[tokens[start][1]]
    inner, index = _sequence(tokens, start + 1, closer)
    return inner, index + 1


def _atom(tokens: list[tuple[str, str]], index: int) -> tuple[str, int]:
    """One operand, for a root or an exponent: a number, a letter or a bracketed group."""
    if index >= len(tokens):
        raise _RefusedError
    kind, text = tokens[index]
    if kind == "open":
        inner, after = _group(tokens, index)
        return (
            inner
            if text == "("
            else f"{_SYMBOLS.get(text, text)} {inner} "
            f"{_SYMBOLS.get(_PAIRS[text], _PAIRS[text])}"
        ), after
    if kind == "op" and text in "-\u2212":
        rest, after = _atom(tokens, index + 1)
        return f"-{rest}", after
    if kind in {"num", "sci", "word", "greek", "vulgar", "set"}:
        return _piece(kind, text), index + 1
    raise _RefusedError


def _piece(kind: str, text: str) -> str:  # noqa: PLR0911 -- one return per token kind
    if kind == "num":
        return text.replace(",", "{,}")
    if kind == "sci":
        mantissa, _, exponent = text.lower().partition("e")
        return rf"{mantissa} \times 10^{{{int(exponent)}}}"
    if kind == "word":
        if len(text) == 1 or re.fullmatch(r"[A-Za-z]_\d+", text):
            letter, _, subscript = text.partition("_")
            return f"{letter}_{{{subscript}}}" if subscript else letter
        if text in _FUNCTIONS:
            return _FUNCTIONS[text]
        raise _RefusedError
    if kind == "greek":
        return _GREEK[text] if text in _GREEK else _SYMBOLS[text]
    if kind == "ellipsis":
        return r"\ldots"
    return _SYMBOLS.get(text, text)


def _sequence(tokens: list[tuple[str, str]], index: int, closer: str | None) -> tuple[str, int]:
    """TeX for the tokens from `index` up to `closer` (or the end); the index it stopped at."""
    out: list[str] = []
    while index < len(tokens):
        kind, text = tokens[index]
        if kind == "close":
            if text != closer:
                raise _RefusedError
            return " ".join(out), index
        if kind == "word" and text in {"sqrt", "floor", "ceil"}:
            if index + 1 >= len(tokens) or tokens[index + 1][1] != "(":
                raise _RefusedError
            inner, index = _group(tokens, index + 1)
            if text == "sqrt":
                out.append(rf"\sqrt{{{inner}}}")
            else:
                close = r"\rfloor" if text == "floor" else r"\rceil"
                out.append(rf"{_FUNCTIONS[text]} {inner} {close}")
            continue
        if kind == "root":
            inner, index = _atom(tokens, index + 1)
            out.append(rf"\sqrt{{{inner}}}")
            continue
        if kind == "op" and text == "*" and tokens[index + 1 : index + 2] in _ROOT_NEXT:
            # `18*sqrt(5)` reads as the record's exact forms set it, `18\sqrt{5}`.
            index += 1
            continue
        if kind == "op" and text == "^":
            inner, index = _atom(tokens, index + 1)
            out.append(f"^{{{inner}}}")
            continue
        if kind == "open":
            inner, index = _group(tokens, index)
            left, right = _SYMBOLS.get(text, text), _SYMBOLS.get(_PAIRS[text], _PAIRS[text])
            out.append(f"{left}{inner}{right}")
            continue
        if kind == "sup":
            out.append(f"^{{{text.translate(_SUPERSCRIPT)}}}")
        elif kind == "sub":
            out.append(f"_{{{text.translate(_SUBSCRIPT)}}}")
        elif kind == "dot":
            if index != len(tokens) - 1:
                raise _RefusedError
            out.append(".")
        else:
            out.append(_piece(kind, text))
        index += 1
    if closer is not None:
        raise _RefusedError
    return " ".join(out), index


def code_tex(code: str) -> str | None:
    """A case file's code span as TeX when it is mathematics, else `None`.

    Mathematics here is what the case files write: `s(11) > 31/8 = 3.875`,
    `2 + 4/sqrt(5)`, `⌈√112⌉ = 11`, `q^2 B^2(1 + D)^2 < 1 + D^2`, `cos θ₁`, `n ≤ 100`,
    a bare number or a single letter. A span is left as code when it has a word that is
    not a known function (`minSide`, `reported_lower_bound`), a character no formula
    uses (a path's `/x` is fine, its `.json` is not), or the shape of an identifier
    (`T-026`, `V4/C5`, `n-012.md`).
    """
    if not code.strip() or _IDENTIFIER.search(_SCIENTIFIC.sub("0", code)):
        return None
    tokens = _tokens(code)
    if not tokens:
        return None
    kinds = {kind for kind, _ in tokens}
    if not kinds & {"num", "sci", "rel", "word", "greek", "root", "set", "vulgar"}:
        return None
    try:
        tex, _ = _sequence(tokens, 0, None)
    except _RefusedError:
        return None
    return tex


_FENCE = re.compile(r"^```[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL)
_FENCED = re.compile(r"(^```.*?^```[ \t]*$)", re.MULTILINE | re.DOTALL)
#: A code span, unless it opens a link's text: ``[`T-018`](RESULTS.md)`` names a record.
_CODE_SPAN = re.compile(r"(?<![`\\\[])`([^`\n]+)`(?!`)")
_HEADING = re.compile(r"^(#{1,4}) ", re.MULTILINE)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def prose_markdown(body: str) -> str:
    """A case file's prose as this page sets it.

    A fenced block that is one formula becomes display math; a code span that is
    mathematics becomes inline math, except one that is a link's text. Headings drop
    two levels, under the record's own, and the guideline footer comment goes.
    """
    body = _COMMENT.sub("", body).strip()

    def fence(match: re.Match[str]) -> str:
        tex = code_tex(" ".join(match.group(1).split()))
        return f"$$\n{tex}\n$$" if tex is not None else match.group(0)

    def span(match: re.Match[str]) -> str:
        tex = code_tex(match.group(1))
        return f"${tex}$" if tex is not None else match.group(0)

    parts = _FENCED.split(_FENCE.sub(fence, body))

    def demote(match: re.Match[str]) -> str:
        return "#" * (len(match.group(1)) + 2) + " "

    return "".join(
        part if number % 2 else _HEADING.sub(demote, _CODE_SPAN.sub(span, part))
        for number, part in enumerate(parts)
    )


# ---------- The record ----------


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def bound_tex(bound: dict[str, Any]) -> str:
    """A bound as TeX: its closed form, or its decimal cut as the atlas cuts it."""
    exact = bound.get("exact_form")
    if isinstance(exact, str) and exact and not tables.ROOT_FORM.fullmatch(exact):
        tex = tables.latex(exact)
        if len(tex) <= frontier.VALUE_SHOWN:
            return frontier.cell_tex(tex)
    text = frontier.decimal_text(bound["value"])
    return text.replace("\u2026", "\\text{\u2026}")


def _closed_form(bound: dict[str, Any]) -> bool:
    exact = bound.get("exact_form")
    return (
        isinstance(exact, str)
        and bool(exact)
        and not tables.ROOT_FORM.fullmatch(exact)
        and len(tables.latex(exact)) <= frontier.VALUE_SHOWN
    )


def _math(tex: str, *, display: bool = False) -> str:
    from devtools.overview_data import math_html  # noqa: PLC0415

    return math_html(tex, display=display)


def interval_tex(case: dict[str, Any]) -> str:
    """The verified interval: `s(n) = v` when it is closed, `L ≤ s(n) ≤ U` otherwise."""
    n = case["n"]
    upper, lower = case["verified_upper_bound"], case["verified_lower_bound"]
    if frontier.Decimal(str(upper["value"])) == frontier.Decimal(str(lower["value"])):
        return f"s({n}) = {bound_tex(upper)}"
    return rf"{bound_tex(lower)} \le s({n}) \le {bound_tex(upper)}"


def _full_decimal(bound: dict[str, Any]) -> str:
    value = str(bound["value"])
    return f'<span class="site-case-decimal">{_esc(value)}</span>'


def _value_block(bound: dict[str, Any]) -> str:
    """A bound's value, a closed form as math and a decimal as figures, with the recorded
    decimal in full under it where the two differ."""
    shown = (
        _math(bound_tex(bound))
        if _closed_form(bound)
        else '<span class="site-case-figures">'
        f"{_esc(frontier.decimal_text(bound['value']))}</span>"
    )
    exact = bound.get("exact_form")
    exact_text = str(exact) if exact else ""
    if frontier.is_integer(exact_text) or str(bound["value"]).rstrip("0").rstrip(".") in {
        exact_text,
        frontier.decimal_text(bound["value"]),
    }:
        return f'<p class="site-case-value">{shown}</p>'
    return f'<p class="site-case-value">{shown}</p>{_full_decimal(bound)}'


def polynomial_block(upper: dict[str, Any]) -> str:
    """The minimal polynomial, typeset whatever its length; a long one opens on request."""
    polynomial = upper.get("minimal_polynomial")
    if not polynomial:
        return ""
    degree = upper.get("algebraic_degree")
    shown = _math(tables.polynomial_latex(polynomial))
    label = f"Minimal polynomial, degree {degree}" if degree else "Minimal polynomial"
    if len(polynomial) > POLYNOMIAL_OPEN:
        return (
            f'<details class="site-case-polynomial"><summary>{_esc(label)}</summary>'
            f"<p>{shown}</p></details>"
        )
    return f"<dt>{_esc(label)}</dt><dd>{shown}</dd>"


def _row(label: str, value: str) -> str:
    return f"<dt>{_esc(label)}</dt><dd>{value}</dd>" if value else ""


def _upper_panel(case: dict[str, Any]) -> str:
    upper = case["reported_upper_bound"]
    method = upper.get("construction_method")
    construction = _esc(tables.UB_LABEL.get(method, method or "\u2014"))
    if upper.get("catalogue_rigid") == "rigid":
        construction += ", catalogue rigid"
    angles = upper.get("tilt_angles_deg") or []
    tilts = ", ".join(
        _math(frontier.decimal_text(a).replace("\u2026", "\\text{\u2026}") + r"^\circ")
        for a in angles
    )
    polynomial = polynomial_block(upper)
    inline_polynomial = polynomial if polynomial.startswith("<dt>") else ""
    rows = (
        _row("Found by", frontier.credit(upper.get("found_by"), upper.get("found_year")))
        + _row("Improved by", _esc(", ".join(upper.get("improved_by") or [])))
        + _row("Construction", construction)
        + _row("Tilt angles", tilts)
        + inline_polynomial
        + _row("Source", _esc(upper.get("source_key") or ""))
        + _row("Evidence", frontier.evidence_links(upper["evidence"]))
    )
    long_polynomial = "" if inline_polynomial else polynomial
    return _panel("Best known packing", _value_block(upper), rows, long_polynomial)


def _verified_panel(label: str, verified: dict[str, Any], reported: dict[str, Any]) -> str:
    from sqpack.assurance import bounds_agree_at_declared_precision  # noqa: PLC0415

    same = bounds_agree_at_declared_precision(reported, verified)
    note = '<p class="site-case-same">The reported value, verified here.</p>' if same else ""
    rows = _row("Evidence", frontier.evidence_links(verified["evidence"]))
    return _panel(label, _value_block(verified) + note, rows)


def _lower_panel(case: dict[str, Any]) -> str:
    from devtools.overview_data import tex_bounds  # noqa: PLC0415

    lower = case["reported_lower_bound"]
    kind = str(tables.LB_LABEL.get(lower["kind"], lower["kind"])).replace("`", "")
    rows = (
        _row("Proved by", frontier.credit(lower.get("proved_by"), lower.get("proved_year")))
        + _row("Kind", _esc(kind))
        + _row("Scope", tex_bounds(lower.get("scope") or ""))
        + _row("Note", tex_bounds(" ".join(str(lower.get("note") or "").split())))
        + _row("Source", _esc(lower.get("source_key") or ""))
        + _row("Evidence", frontier.evidence_links(lower["evidence"]))
    )
    return _panel("Reported lower bound", _value_block(lower), rows)


def _panel(label: str, value: str, rows: str, extra: str = "") -> str:
    listing = f'<dl class="site-detail">{rows}</dl>' if rows else ""
    return (
        f'<div class="site-case-bound"><span class="site-card-label">{_esc(label)}</span>'
        f"{value}{listing}{extra}</div>"
    )


def _gap_panel(case: dict[str, Any]) -> str:
    gap_html, _ = frontier.gap(case)
    closed = case["status"] == "proved"
    note = (
        "Solved: the verified bounds meet."
        if closed
        else "Verified upper minus verified lower."
    )
    return _panel(
        "Gap",
        f'<p class="site-case-value">{gap_html}</p><p class="site-case-same">{note}</p>',
        "",
    )


def _rigidity(case: dict[str, Any]) -> str:
    rigidity = case.get("rigidity") or {}
    if not rigidity:
        return ""
    words = [
        str(rigidity.get(key, "")).replace("-", " ")
        for key in ("property", "assurance", "method")
        if rigidity.get(key)
    ]
    scope = rigidity.get("scope")
    detail = (
        f"<details><summary>Scope</summary><p>{_esc(' '.join(str(scope).split()))}</p>"
        "</details>"
        if scope
        else ""
    )
    evidence = rigidity.get("evidence") or []
    links = f"<p>Evidence: {frontier.evidence_links(evidence)}</p>" if evidence else ""
    return (
        '<div class="site-case-note"><span class="site-card-label">Rigidity</span>'
        f"<p>{_esc(', '.join(words))}</p>{links}{detail}</div>"
    )


def _open_questions(case: dict[str, Any]) -> str:
    items = []
    for label, entries in (("Conflict", case["conflicts"]), ("Blocker", case["blockers"])):
        for entry in entries:
            kind = str(entry.get("kind", "")).replace("-", " ")
            items.append(
                f"<li><b>{label}</b> ({_esc(kind)}): {_esc(entry.get('detail', ''))} "
                f"{frontier.evidence_links(entry.get('evidence') or [])}</li>"
            )
    for note in case.get("priority_notes") or []:
        who = ", ".join(note.get("claimed_by") or [])
        items.append(
            f"<li><b>Priority</b>: {_esc(note.get('claim', ''))}"
            + (f" ({_esc(who)})" if who else "")
            + "</li>"
        )
    if not items:
        return ""
    return (
        '<div class="site-case-note"><span class="site-card-label">Open questions</span>'
        f'<ul class="site-case-list">{"".join(items)}</ul></div>'
    )


@cache
def _results_by_case() -> dict[int, list[Any]]:
    """Every registered result, filed under each case it concerns."""
    from devtools import overview_data  # noqa: PLC0415

    found: dict[int, list[Any]] = {}
    for result in overview_data.load().results:
        scope = result.record["scope"]
        members = (
            scope["n_values"]
            if "n_values" in scope
            else range(scope["n_min"], scope["n_max"] + 1)
        )
        for n in members:
            found.setdefault(n, []).append(result)
    return found


def results_block(n: int) -> str:
    """Every result in the register that concerns case `n`: its rungs, summary, claim
    and records, and a link to its row in the results table."""
    from devtools.overview_data import tex_bounds  # noqa: PLC0415
    from devtools.overview_sections import (  # noqa: PLC0415
        _detail,  # pyright: ignore[reportPrivateUsage]
        _records,  # pyright: ignore[reportPrivateUsage]
        _rung,  # pyright: ignore[reportPrivateUsage]
        result_url,
    )

    results = sorted(_results_by_case().get(n, []), key=lambda r: r.id)
    if not results:
        return (
            '<p class="site-case-empty">No result in the register concerns this case; '
            "its bounds are the sources\u2019 and the record\u2019s.</p>"
        )
    items = []
    for result in results:
        record = result.record
        rungs = " ".join(
            _rung(rung)
            for rung in (
                record["verification"],
                record["confirmation"],
                "S" + str(record["significance"]["score"]),
            )
        )
        scope = record["scope"]
        count = (
            len(scope["n_values"])
            if "n_values" in scope
            else scope["n_max"] - scope["n_min"] + 1
        )
        # A result about many cases is repeated in each of their records, so it is
        # summarized there; its claim and records are one click away, in its row.
        broad = count > BROAD_RESULT
        where = f"{count} cases" if broad else f"n = {_esc(result.scope)}"
        detail = (
            ""
            if broad
            else f"<details><summary>Claim and records</summary>{_detail(result)}"
            f'<p class="site-records">{_records(result)}</p></details>'
        )
        items.append(
            f'<li class="site-case-result" data-result="{_esc(result.id)}">'
            f'<p class="site-case-result-head"><a href="{_esc(result_url(result.id))}">'
            f"{_esc(result.id)}</a> {rungs} "
            f'<span class="site-credit">{_esc(result.credit)} · {_esc(result.date)} · '
            f"{where}</span></p>"
            f'<p class="site-case-result-summary">{tex_bounds(result.summary)}</p>'
            f"{detail}</li>"
        )
    return f'<ul class="site-case-results">{"".join(items)}</ul>'


def _sources(case: dict[str, Any]) -> str:
    items = []
    for resource in case.get("resources") or []:
        role = str(resource.get("role", "")).replace("-", " ")
        url = resource.get("url")
        key = _esc(resource.get("key", ""))
        name = f'<a href="{_esc(url)}">{key}</a>' if url else key
        items.append(f'<li>{name} <span class="site-credit">{_esc(role)}</span></li>')
    if not items:
        return ""
    return f'<ul class="site-case-list site-case-sources">{"".join(items)}</ul>'


def record_head(case: dict[str, Any], *, recent: bool, first: int, last: int) -> str:
    """The record's head and its structured part, as one HTML block."""
    from devtools.overview_sections import arrow_icon  # noqa: PLC0415
    from devtools.repo_links import branch_file  # noqa: PLC0415

    n = case["n"]
    status = case["status"]
    tone = ' data-tone="accent"' if status == "proved" else ""
    chip = f'<span class="site-chip"{tone}>{_esc(status)}</span>'
    if case["reported_status"] != status:
        chip += f' <span class="site-credit">reported {_esc(case["reported_status"])}</span>'
    star = ' <span class="site-star" title="Recent lower bound">\u2605</span>' if recent else ""
    previous = (
        f'<a href="#n-{n - 1}" rel="prev">{arrow_icon("left")}n = {n - 1}</a>'
        if n > first
        else ""
    )
    following = (
        f'<a href="#n-{n + 1}" rel="next">n = {n + 1}{arrow_icon("right")}</a>'
        if n < last
        else ""
    )
    upper, lower = case["reported_upper_bound"], case["reported_lower_bound"]
    evidence = list(dict.fromkeys(case["evidence"]))
    source = f"packing/frontier/n-{n:03d}.md"
    return (
        f'<header class="site-case-head" data-kpress-prose-font="sans">'
        f'<nav class="site-case-steps" aria-label="Cases">{previous}'
        f'<a href="#cases">All cases</a>{following}</nav>'
        '<span class="site-card-label">Case record</span>'
        f'<p class="site-case-title"><b>n = {n}</b> {chip}{star}</p>'
        f'<p class="site-case-interval">{_math(interval_tex(case))}</p></header>'
        '<div class="site-case-top site-wide">'
        f'<figure class="site-case-figure">{frontier.packing_svg(n, units=1000)}'
        f"<figcaption>The best packing known for {n} square{'s' if n != 1 else ''}, side "
        f"{_math(bound_tex(upper))}, "
        f"{frontier.credit(upper.get('found_by'), upper.get('found_year'))}"
        "</figcaption></figure>"
        f'<div class="site-case-bounds" data-kpress-prose-font="sans">'
        f"{_upper_panel(case)}"
        f"{_verified_panel('Verified upper bound', case['verified_upper_bound'], upper)}"
        f"{_lower_panel(case)}"
        f"{_verified_panel('Verified lower bound', case['verified_lower_bound'], lower)}"
        f"{_gap_panel(case)}</div></div>"
        f'<div class="site-case-more" data-kpress-prose-font="sans">'
        f'<h3 class="site-case-heading">Results in the register</h3>{results_block(n)}'
        f"{_rigidity(case)}{_open_questions(case)}"
        '<div class="site-case-note"><span class="site-card-label">Evidence and sources</span>'
        f"<details><summary>{len(evidence)} evidence entries</summary>"
        f"<p>{frontier.evidence_links(evidence)}</p></details>{_sources(case)}</div>"
        f'<p class="site-case-links"><a href="frontier.html#n-{n}">In the frontier atlas</a>'
        f' <a class="site-case-github" href="{branch_file(source)}">On GitHub</a></p></div>'
    )


def _body(n: int) -> tuple[str, str]:
    """The case file's title line and its prose, as this page sets them."""
    text = (tables.FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    body = text.split("---\n", 2)[2]
    title, _, rest = body.strip().partition("\n")
    if not title.startswith("# "):
        title, rest = "", body
    heading = title.removeprefix("# ").strip()
    return heading, rest


def record_markdown(case: dict[str, Any], *, recent: bool, first: int, last: int) -> str:
    """One case's record: its head and structured part, then the case file's prose."""
    n = case["n"]
    heading, prose = _body(n)
    shown = prose_markdown(f"# {heading}\n") if heading else ""
    return (
        f'<section class="site-case" id="n-{n}" data-n="{n}" '
        f'data-status="{_esc(case["status"])}">\n'
        f"{record_head(case, recent=recent, first=first, last=last)}\n\n"
        f"{shown.strip()}\n\n{prose_markdown(prose)}\n\n</section>"
    )


def index_html(cases: list[dict[str, Any]]) -> str:
    """Every case as a link to its record, marked solved or open."""
    links = "".join(
        f'<a href="#n-{case["n"]}" data-status="{_esc(case["status"])}">{case["n"]}</a>'
        for case in cases
    )
    return (
        '<nav class="site-case-index site-wide" id="cases" aria-label="Every case" '
        f'data-kpress-prose-font="sans">{links}</nav>'
    )


def cases_markdown(fill: Any) -> str:
    """The article: its prose from the template, the index and every record."""
    cases = frontier.frontier_cases()
    recent = frontier.recent_lower_bounds()
    first, last = min(c["n"] for c in cases), max(c["n"] for c in cases)
    records = "\n\n".join(
        record_markdown(case, recent=recent.get(case["n"], False), first=first, last=last)
        for case in cases
    )
    values = {
        "COUNT": str(len(cases)),
        "LAST_N": str(last),
        "INDEX": index_html(cases),
        "RECORDS": f'<div class="site-case-records" data-case-records>\n\n{records}\n\n</div>',
    }
    template = CASES_ARTICLE.read_text(encoding="utf-8")
    return fill(template, values, where=CASES_ARTICLE.name)


CASES_DESCRIPTION = (
    "Every tracked case of packing n unit squares in the smallest square, one record "
    "each: the best packing known, every bound with its exact form and credit, and every "
    "result that concerns it."
)


def cases_page() -> Any:
    """The records as one kpress page, with the case files' links made to work here.

    The prose's links are rewritten as a reader document's are (`site_documents`): a
    link to another case file becomes that case's record on this page, a link to a
    rendered document its page, and anything else its link on `main`; a
    link the record itself writes to a served page is kept.
    """
    from devtools import render_overview, site_documents  # noqa: PLC0415
    from devtools.repo_links import repository_tree  # noqa: PLC0415

    numbers = [int(path.stem.split("-")[1]) for path in tables.FRONTIER.glob("n-*.md")]
    context = site_documents.LinkContext(
        CASES_PAGE,
        repository_tree(),
        "packing/frontier",
        served=frozenset({*render_overview.SITE_PAGES, "./"}),
        aliases={f"packing/frontier/n-{n:03d}.md": f"#n-{n}" for n in numbers},
    )
    report = site_documents.LinkReport()
    page = render_overview.kpress_page(
        cases_markdown(render_overview.fill),
        name=CASES_PAGE,
        current="frontier",
        title=f"Case Records · {render_overview.SITE_NAME}",
        description=CASES_DESCRIPTION,
        toc=False,
        rewrite_body=lambda text: site_documents.rewrite_article(
            text, context=context, report=report
        ),
        page_scripts=(CASE_VIEW_SCRIPT,),
    )
    problems = site_documents.unresolved(
        {**site_documents.site_documents(), CASES_PAGE: page}, report
    )
    if problems:
        listing = "\n  ".join(problems)
        raise SystemExit(f"{len(problems)} unresolved links in the case records:\n  {listing}")
    return page
