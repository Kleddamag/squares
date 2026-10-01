#!/usr/bin/env python3
"""Render the frontier atlas page: one table row for every case `n = 1…324`.

Every row is read from the case's softschema record, the `packing:` envelope of
`frontier/n-NNN.md` under the enforced `packing.squares:SquarePackingCase/v2` contract,
and each file is validated against its declared schema before a cell is written, so an
invalid record fails the render rather than rendering a blank. Nothing is read from
`STATUS.md` and nothing is typed by hand: the formatting is `render_research_tables`'s
(`latex`, `compact_bound`'s exact-form rule, `case_disposition`,
`verification_origins`), and "shown once" is `bounds_agree_at_declared_precision`, the
test `STATUS.md` applies.

The page is one of `render_overview.PAGES`; render it with the rest of the site:

    uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable, Iterable
from decimal import Decimal
from functools import cache
from pathlib import Path
from typing import Any, cast

from devtools import render_research_tables as tables
from devtools.build_bound_citations import RECENT_SINCE
from devtools.build_bound_citations import RECORD as BOUND_CITATIONS
from devtools.repo_links import repo_url
from devtools.validate_schemas import check as check_record
from sqpack.assurance import bounds_agree_at_declared_precision

PACKING = Path(__file__).resolve().parents[1]
TEMPLATES = PACKING / "devtools" / "templates"
FRONTIER_ARTICLE = TEMPLATES / "frontier-article.md"
RENDERINGS = PACKING / "atlas" / "known-best" / "rendering"
TABLE_SCRIPT = PACKING / "devtools" / "overview" / "table.js"

#: Every file this page reads beyond the site shell's own inputs.
FRONTIER_INPUTS: tuple[Path, ...] = (
    Path(__file__).resolve(),
    FRONTIER_ARTICLE,
    TABLE_SCRIPT,
    PACKING / "frontier",
    RENDERINGS,
    BOUND_CITATIONS,
    PACKING / "devtools" / "render_research_tables.py",
    PACKING / "devtools" / "build_bound_citations.py",
    PACKING / "devtools" / "validate_schemas.py",
    PACKING / "src" / "sqpack" / "assurance.py",
)

#: The digits a decimal cell shows before it is cut, with an ellipsis rather than rounded:
#: a rounded bound can read as a different bound.
DECIMAL_PLACES = 8
#: A minimal polynomial longer than this is linked rather than typeset; the longest in the
#: record runs to 18,000 characters.
POLYNOMIAL_SHOWN = 160
#: An exact gap longer than this, in TeX, is shown as its decimal: a difference of two
#: long closed forms is exact and unreadable.
GAP_SHOWN = 44
#: A closed form longer than this, in TeX, is shown as its decimal. The longest structured
#: form runs to 45 characters; a 30-digit rational certificate value does not read as one.
VALUE_SHOWN = 56


def math_html(tex: str) -> str:
    """Inline math in kpress's own markup, which the page's KaTeX scripts enhance.

    kpress turns `$…$` into math only in Markdown text, and a table here is an HTML
    block, so the cell asks kpress's renderer for the same span it would have written:
    the TeX for KaTeX and server MathML as the no-script fallback.
    """
    from kpress.format.markdown import (  # noqa: PLC0415
        _render_math,  # pyright: ignore[reportPrivateUsage]
    )

    return _render_math(tex, display="inline", math="auto", env={})


def decimal_text(value: object) -> str:
    """A record's decimal, cut rather than rounded after `DECIMAL_PLACES`.

    A whole number the record writes as `3.0` prints as `3`, as the best-known side
    beside it does.
    """
    text = str(value)
    whole, _, fraction = text.partition(".")
    if fraction and not fraction.strip("0"):
        return whole
    if len(fraction) <= DECIMAL_PLACES:
        return text
    return f"{whole}.{fraction[:DECIMAL_PLACES]}…"


def is_integer(text: str) -> bool:
    return re.fullmatch(r"\d+", text) is not None


def cell_tex(tex: str) -> str:
    """A value's TeX as a table cell sets it: a lone fraction at full size.

    Inline math sets `\\frac` in text style, where `31/8` reads at a subscript's size;
    a fraction that is the whole value is the one a reader is looking for, so it gets
    `\\dfrac`. A fraction inside a sum keeps text style and the row its height.
    """
    if re.fullmatch(r"\\frac\{\d+\}\{\d+\}", tex):
        return "\\dfrac" + tex.removeprefix("\\frac")
    return tex


def exact_decimal(value: Any) -> tuple[str, bool]:
    """An exact value's decimal as a cell prints it, and whether that is the whole of it.

    The digits come from the exact value and from nothing looser. A rational is divided
    in whole numbers, so its decimal either ends within `DECIMAL_PLACES` and is printed
    in full, or is cut there. Anything else is evaluated by sympy to 30 significant
    digits and cut by `decimal_text`, the rule every decimal on the page follows. A cut
    drops digits and never rounds, so the digits dropped must not be all nines or all
    zeros as far as they are known: there the last digit kept would depend on digits
    that were never computed, and the render stops instead of printing a guess.
    """
    import sympy  # noqa: PLC0415

    if value.is_Rational:
        scaled, left = divmod(abs(int(value.p)) * 10**DECIMAL_PLACES, int(value.q))
        whole, fraction = divmod(scaled, 10**DECIMAL_PLACES)
        sign = "-" if value.p < 0 else ""
        digits = f"{fraction:0{DECIMAL_PLACES}d}"
        if left:
            return f"{sign}{whole}.{digits}…", False
        return f"{sign}{whole}.{digits}".rstrip("0").rstrip("."), True
    numeric = f"{Decimal(str(sympy.N(value, 30))):f}"
    dropped = numeric.partition(".")[2][DECIMAL_PLACES:-2]
    if not dropped.strip("9") or not dropped.strip("0"):
        raise SystemExit(f"{value} is too close to a {DECIMAL_PLACES}-place decimal to cut")
    return decimal_text(numeric), False


def approx_html(value: Any) -> str:
    """The decimal a closed form is set over, quiet, on a line of its own under it:
    `= 4.695` where the decimal is the value, `≈ 3.96861554…` where it is cut."""
    text, whole = exact_decimal(value)
    return f'<span class="site-approx">{"=" if whole else "≈"} {text}</span>'


def value_html(bound: dict[str, Any]) -> str:
    """A bound as a reader should see it: integers plain, closed forms as math."""
    exact = bound.get("exact_form")
    if isinstance(exact, str) and exact and not tables.ROOT_FORM.fullmatch(exact):
        if is_integer(exact):
            return html.escape(exact)
        tex = tables.latex(exact)
        if len(tex) <= VALUE_SHOWN:
            return math_html(cell_tex(tex))
    return f'<span class="site-decimal">{html.escape(decimal_text(bound["value"]))}</span>'


def bound_approx_html(bound: dict[str, Any]) -> str:
    """The decimal under a bound the table sets as a closed form, and nothing under a
    whole number or a bound already set as a decimal. It is read from the closed form,
    never from the record's own decimal, which a lower bound may hold to fewer places
    (`15680/3951` is recorded as `3.968615`)."""
    exact = bound.get("exact_form")
    if (
        not isinstance(exact, str)
        or not exact
        or tables.ROOT_FORM.fullmatch(exact)
        or is_integer(exact)
        or len(tables.latex(exact)) > VALUE_SHOWN
    ):
        return ""
    value = exact_value(exact)
    return "" if value.is_Integer else approx_html(value)


def polynomial_html(case: dict[str, Any], case_url: str) -> str:
    """The minimal polynomial behind a decimal, where the record gives one."""
    upper = case["reported_upper_bound"]
    polynomial = upper.get("minimal_polynomial")
    if not polynomial:
        return ""
    degree = upper.get("algebraic_degree")
    if len(polynomial) > POLYNOMIAL_SHOWN:
        return (
            f'<dt>Minimal polynomial</dt><dd>degree {degree}, <a href="{case_url}">'
            "in the case record</a></dd>"
        )
    shown = tables.polynomial_latex(polynomial)
    return f"<dt>Minimal polynomial</dt><dd>{math_html(shown)}</dd>"


def credit(names: Iterable[str] | None, year: object) -> str:
    who = ", ".join(names or [])
    when = str(year) if year else ""
    return html.escape(" ".join(part for part in (who, when) if part))


@cache
def exact_value(form: str) -> Any:
    """A sympy value for an exact form, or `None` for a polynomial root."""
    import sympy  # noqa: PLC0415
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    if tables.ROOT_FORM.fullmatch(form):
        return None
    return parse_expr(
        form,
        transformations=(*standard_transformations, implicit_multiplication_application),
        local_dict={"sqrt": sympy.sqrt, "floor": sympy.floor},
    )


def gap(case: dict[str, Any]) -> tuple[str, str]:
    """Verified upper minus verified lower: `(cell HTML, decimal for sorting)`.

    Exact where both bounds are closed forms and the difference is short enough to read
    in a cell, with its decimal beneath unless it is a whole number; otherwise the
    decimal difference, cut like every other decimal here. Both bounds written as the
    same exact form -- one polynomial root, as for n = 11 since T-060 -- are one number,
    so the gap is zero without evaluating the root.
    """
    import sympy  # noqa: PLC0415

    upper, lower = case["verified_upper_bound"], case["verified_lower_bound"]
    if upper.get("exact_form") and upper["exact_form"] == lower.get("exact_form"):
        return "0", "0"
    upper_exact = exact_value(upper["exact_form"]) if upper.get("exact_form") else None
    lower_exact = exact_value(lower["exact_form"]) if lower.get("exact_form") else None
    if upper_exact is not None and lower_exact is not None:
        difference = cast("Any", sympy.radsimp(sympy.expand(upper_exact - lower_exact)))
        numeric = Decimal(str(sympy.N(difference, 30)))
        sort_value = "0" if numeric == 0 else f"{numeric:.30f}"
        tex = sympy.latex(difference, order="rev-lex")
        if difference.is_Integer:
            return html.escape(str(difference)), sort_value
        if len(tex) <= GAP_SHOWN:
            return math_html(cell_tex(tex)) + approx_html(difference), sort_value
        return f'<span class="site-decimal">{decimal_text(numeric)}</span>', sort_value
    numeric = Decimal(str(upper["value"])) - Decimal(str(lower["value"]))
    return (
        f'<span class="site-decimal">{html.escape(decimal_text(numeric))}</span>',
        str(numeric),
    )


@cache
def evidence_lines() -> dict[str, int]:
    """Each evidence id's line in `evidence.yaml`, for a link to the entry itself."""
    lines = (tables.FRONTIER / "evidence.yaml").read_text(encoding="utf-8").splitlines()
    found = {}
    for number, line in enumerate(lines, start=1):
        match = re.fullmatch(r"\s*- id: (\S+)", line)
        if match:
            found[match.group(1)] = number
    return found


def evidence_links(refs: Iterable[str]) -> str:
    """Each evidence id once, as code linking to its entry in `evidence.yaml`, with commas
    between. A name and the comma after it are one `.site-name` box, so a line breaks
    between names and never on a hyphen inside one (`site.css`, Words stay whole)."""
    base = repo_url(tables.FRONTIER / "evidence.yaml")
    lines = evidence_lines()
    links = []
    for ref in dict.fromkeys(refs):
        if ref not in lines:
            raise SystemExit(f"evidence id {ref} is not in evidence.yaml")
        links.append(f'<a href="{base}#L{lines[ref]}"><code>{html.escape(ref)}</code></a>')
    return " ".join(
        f'<span class="site-name">{link}{"," if index < len(links) else ""}</span>'
        for index, link in enumerate(links, start=1)
    )


def thumbnail_svg(n: int) -> str:
    """The atlas drawing of case `n`, reduced to its squares for a table cell.

    The full drawing carries exact coordinates to 28 digits and a metadata block, about
    51 MB over the corpus; a cell 50 pixels across needs the outline of each square at
    whole units of a 100-unit frame, half a pixel at
    that size, one path per fill colour, and nothing else. The cell that holds it is
    the `.site-thumb` and sizes it, so the drawing has no wrapper of its own.
    """
    return packing_svg(n)


def packing_svg(
    n: int,
    *,
    units: int = 100,
    ink: str = "currentColor",
    paper: str = "none",
    frame_px: int | None = None,
) -> str:
    """Case `n`'s atlas drawing as a bare `<svg>`: the frame and each square's outline at
    whole units of a `units`-wide frame, drawn in `ink` on `paper`.

    A table cell needs 100 units; a drawing shown large needs more, or the rounding shows
    as uneven gaps. A drawing used outside the page, where `currentColor` means nothing,
    names its ink. An icon drawn `frame_px` pixels square (the site's logo and favicon)
    gets a frame exactly one of those pixels wide, its outer edge on the drawing's edge,
    so the container reads as a square at icon size and lands on the pixel grid, and
    its squares' outlines half a pixel, so each square stays distinct.
    """
    source = (RENDERINGS / f"n-{n:03d}.svg").read_text(encoding="utf-8")
    frame = re.search(
        r'<rect data-feature="container-outline" x="([\d.]+)" y="([\d.]+)" '
        r'width="([\d.]+)" height="([\d.]+)"',
        source,
    )
    if frame is None:
        raise SystemExit(f"n-{n:03d}.svg has no container outline")
    x0, y0, width, _ = (Decimal(part) for part in frame.groups())
    scale = Decimal(units) / width
    paths: dict[str, list[str]] = {}
    squares = re.findall(
        r'<polygon data-feature="square-fill"[^>]*? points="([^"]+)" fill="(#[0-9a-f]{6})"',
        source,
    )
    if len(squares) != n:
        raise SystemExit(f"n-{n:03d}.svg draws {len(squares)} squares, not {n}")
    for points, fill in squares:
        corners = [
            (round((Decimal(x) - x0) * scale), round((Decimal(y) - y0) * scale))
            for x, y in (pair.split(",") for pair in points.split())
        ]
        paths.setdefault(fill, []).append(_square_path(corners))
    body = "".join(
        f'<path fill="{fill}" d="{"".join(parts)}"/>' for fill, parts in sorted(paths.items())
    )
    unit = Decimal(units) / 100
    box = f"{-unit:g} {-unit:g} {units + 2 * unit:g} {units + 2 * unit:g}"
    frame_width = (Decimal("1.2") * unit).normalize()
    crisp = ""
    line_width = (Decimal("0.6") * unit).normalize()
    if frame_px is not None:
        # One pixel of a `frame_px`-pixel drawing whose box is the frame plus half its
        # stroke on each side: (units + w) / frame_px = w.
        pixel = Decimal(units) / (frame_px - 1)
        half = pixel / 2
        box = f"{-half:.4f} {-half:.4f} {units + pixel:.4f} {units + pixel:.4f}"
        frame_width = pixel.quantize(Decimal("0.0001"))
        crisp = ' shape-rendering="crispEdges"'
        # At icon size the page's hairline all but vanishes, so the squares' outlines
        # take half a pixel: one device pixel on a 2x screen, and still lighter than
        # the frame.
        line_width = (pixel / 2).quantize(Decimal("0.0001"))
    return (
        f'<svg viewBox="{box}" aria-hidden="true" focusable="false">'
        f'<rect x="0" y="0" width="{units}" height="{units}" fill="{paper}" '
        f'stroke="{ink}" stroke-width="{frame_width:f}"{crisp}/><g stroke="{ink}" '
        f'stroke-width="{line_width:f}" stroke-linejoin="round">{body}</g></svg>'
    )


def _square_path(corners: list[tuple[int, int]]) -> str:
    """One square as a closed path in whole units, relative after its first corner."""
    (x, y), *rest = corners
    steps = [f"M{x} {y}"]
    for next_x, next_y in rest:
        dx, dy = next_x - x, next_y - y
        if dy == 0:
            steps.append(f"h{dx}")
        elif dx == 0:
            steps.append(f"v{dy}")
        else:
            steps.append(f"l{dx}{'' if dy < 0 else ' '}{dy}")
        x, y = next_x, next_y
    return "".join(steps) + "z"


def frontier_cases() -> list[dict[str, Any]]:
    """Every case, each validated against its declared contract before it is read."""
    paths = sorted(tables.FRONTIER.glob("n-*.md"))
    for path in paths:
        errors = check_record(path)
        if errors:
            raise SystemExit(f"{path.name} is not a valid case record: {'; '.join(errors[:3])}")
    cases = tables.load_cases()
    names = [f"n-{case['n']:03d}.md" for case in cases]
    if names != [path.name for path in paths]:
        raise SystemExit("frontier case numbers do not match their file names")
    return cases


def recent_lower_bounds() -> dict[int, bool]:
    """Whether each case's verified lower bound is recent, as the atlas figure stars it."""
    import json  # noqa: PLC0415

    entries = json.loads(BOUND_CITATIONS.read_text(encoding="utf-8"))["citations"]["entries"]
    return {entry["n"]: bool(entry["lower"] and entry["lower"]["recent"]) for entry in entries}


def _cell(content: str, *, value: str | None = None, classes: str = "") -> str:
    attributes = f' class="{classes}"' if classes else ""
    if value is not None:
        attributes += f' data-value="{html.escape(value)}"'
    return f"<td{attributes}>{content}</td>"


def _bound_cell(bound: dict[str, Any], note: str = "") -> str:
    parts = [value_html(bound), bound_approx_html(bound)]
    if note:
        parts.append(f'<span class="site-frontier-note site-cell-quiet">{note}</span>')
    return _cell("".join(parts), value=str(bound["value"]), classes="num")


def _verified_cell(verified: dict[str, Any], reported: dict[str, Any]) -> str:
    """A verified bound, or the mark that it is the reported one, shown once."""
    if bounds_agree_at_declared_precision(reported, verified):
        return _cell(
            '<span class="site-frontier-same" title="Verified here at the reported value">'
            "✓ same</span>",
            value=str(verified["value"]),
            classes="num",
        )
    return _cell(
        value_html(verified) + bound_approx_html(verified),
        value=str(verified["value"]),
        classes="num",
    )


def _upper_details(case: dict[str, Any], case_url: str) -> str:
    upper = case["reported_upper_bound"]
    construction = html.escape(tables.UB_LABEL[upper["construction_method"]])
    if upper.get("catalogue_rigid") == "rigid":
        construction += ", catalogue rigid"
    return (
        f"<dt>Construction</dt><dd>{construction}</dd>"
        f"{polynomial_html(case, case_url)}"
        f"<dt>Source</dt><dd>{html.escape(upper.get('source_key') or '—')}</dd>"
    )


def _lower_details(lower: dict[str, Any]) -> str:
    kind = html.escape(tables.LB_LABEL[lower["kind"]].replace("`", ""))
    return (
        f"<dt>Kind</dt><dd>{kind}</dd>"
        f"<dt>Source</dt><dd>{html.escape(lower.get('source_key') or '—')}</dd>"
    )


def _evidence_refs(case: dict[str, Any]) -> list[str]:
    """The evidence behind a case's four bounds, each once, in the order they are cited."""
    return list(
        dict.fromkeys(
            [
                *case["reported_upper_bound"]["evidence"],
                *case["verified_upper_bound"]["evidence"],
                *case["reported_lower_bound"]["evidence"],
                *case["verified_lower_bound"]["evidence"],
            ]
        )
    )


def frontier_row_popover_body(case: dict[str, Any], evidence: dict[str, dict[str, Any]]) -> str:
    """The body of a frontier row's popover, the one source of it: how the best known
    packing was built, the minimal polynomial behind a decimal and its source; the
    reported lower bound's kind and source; then how the bounds were verified, the case's
    notes and the evidence entries behind them. The row's cells used to open these one at
    a time in place."""
    case_url = repo_url(tables.FRONTIER / f"n-{case['n']:03d}.md")
    origins = html.escape(tables.verification_origins(case, evidence))
    notes = html.escape(tables.case_disposition(case))
    return (
        '<div class="site-pairs">'
        '<p class="site-popover-heading">Best known packing</p>'
        f'<dl class="site-detail">{_upper_details(case, case_url)}</dl>'
        '<p class="site-popover-heading">Reported lower bound</p>'
        f'<dl class="site-detail">{_lower_details(case["reported_lower_bound"])}</dl>'
        '<p class="site-popover-heading">Verification and evidence</p>'
        f'<dl class="site-detail"><dt>Verification</dt><dd>{origins}</dd>'
        f"<dt>Notes</dt><dd>{notes}</dd>"
        f"<dt>Evidence</dt><dd>{evidence_links(_evidence_refs(case))}</dd></dl>"
        "</div>"
    )


def case_row(
    case: dict[str, Any], evidence: dict[str, dict[str, Any]], *, recent: bool
) -> tuple[str, str]:
    """One table row, every cell from the record, and the popover it opens. Its `n`
    opens the case's record; anywhere else on the row, the drawing included, opens the
    popover, whose body is `frontier_row_popover_body` and whose button opens the record
    too. The cells are in `HEADERS`' order: the drawing, `n`, the star, and then what is
    known."""
    from devtools.overview_sections import row_detail  # noqa: PLC0415
    from devtools.render_case_pages import case_link  # noqa: PLC0415
    from devtools.render_case_pages import case_url as record_url  # noqa: PLC0415

    n = case["n"]
    case_url = repo_url(tables.FRONTIER / f"n-{n:03d}.md")
    upper, lower = case["reported_upper_bound"], case["reported_lower_bound"]
    status = case["status"]
    tone = ' data-tone="accent"' if status == "proved" else ""
    shown_status = f'<span class="site-chip"{tone}>{html.escape(status)}</span>'
    if case["reported_status"] != status:
        shown_status += f" (reported {html.escape(case['reported_status'])})"
    gap_html, gap_value = gap(case)
    star = '<span class="site-star" title="Recent lower bound">★</span>' if recent else ""
    detail = row_detail(
        f"pop-frontier-n-{n}",
        name=f"n = {n}, {status}",
        trigger="Details",
        label="Frontier survey",
        title=f"<var>n</var> = {n}",
        body=frontier_row_popover_body(case, evidence),
        action=(record_url(n), f"Open the case record for n = {n}"),
    )
    cells = [
        _cell(thumbnail_svg(n), classes="site-thumb"),
        _cell(
            case_link(n, str(n), label=f"n = {n}: open its case record"),
            value=str(n),
            classes="num site-col-n",
        ),
        _cell(star, value="1" if recent else "0"),
        _cell(shown_status, value=status),
        _bound_cell(upper, credit(upper.get("found_by"), upper.get("found_year"))),
        _verified_cell(case["verified_upper_bound"], upper),
        _bound_cell(lower, credit(lower.get("proved_by"), lower.get("proved_year"))),
        _verified_cell(case["verified_lower_bound"], lower),
        _cell(gap_html, value=gap_value, classes="num"),
        _cell(
            f'<a href="{case_url}">n-{n:03d}.md</a> '
            f'<span class="site-cell-quiet">{detail.trigger}</span>',
            classes="site-records",
        ),
    ]
    flag = {True: "true", False: "false"}
    attributes = (
        f'id="n-{n}" data-n="{n}" data-status="{html.escape(status)}" '
        f'data-open="{flag[status == "open"]}" data-recent="{flag[recent]}" '
        f"{detail.attributes}"
    )
    return f"<tr {attributes}>{''.join(cells)}</tr>", detail.popover


#: The drawing's column has no heading to read; this is its name for a screen reader.
THUMB_LABEL = "Packing"
#: The columns: heading, sort type (none for a column that does not sort), classes. The
#: drawing comes first, under no heading, then `n`, then the star, so the left edge of the
#: table says which case a row is and whether its bound is new; what is known follows.
HEADERS: tuple[tuple[str, str, str], ...] = (
    ("", "", "site-thumb"),
    ("n", "num", "num site-col-n"),
    ("Recent", "num", "site-col-recent"),
    ("Status", "text", ""),
    ("Best known packing", "num", "num"),
    ("Verified upper", "num", "num"),
    ("Reported lower", "num", "num"),
    ("Verified lower", "num", "num"),
    ("Gap", "num", "num"),
    ("Records", "", ""),
)


def _heading(label: str, kind: str, classes: str) -> str:
    """A column's header cell. One with no words is named for a screen reader."""
    sort = f' data-sort="{kind}"' if kind else ""
    named = f' class="{classes}"' if classes else ""
    if not label:
        named += f' aria-label="{THUMB_LABEL}"'
    return f'<th scope="col"{sort}{named}>{html.escape(label)}</th>'


def _tools(count: int, last: int) -> str:
    """The filter bar, hidden until the table script wires it up."""
    number = f'type="number" data-filter="n" min="1" max="{last}" size="4"'
    return (
        '<div class="site-table-tools" data-table="frontier" hidden>'
        '<label>Status <select data-filter="status"><option value="">all</option>'
        '<option value="open">open</option><option value="proved">proved</option>'
        "</select></label>"
        '<label><input type="checkbox" data-filter="open"> open only</label>'
        '<label><input type="checkbox" data-filter="recent"> recent only</label>'
        f'<label><var>n</var> from <input {number} data-bound="min" placeholder="1"></label>'
        f'<label>to <input {number} data-bound="max" placeholder="{last}"></label>'
        f'<span class="site-count" aria-live="polite" data-noun="cases">{count} cases</span>'
        "</div>"
    )


def table_html(cases: list[dict[str, Any]]) -> str:
    """The controls, the table, each row's popover and the popover its cases open in, as
    one HTML block with no blank line inside it."""
    from devtools.render_case_pages import case_popover  # noqa: PLC0415

    evidence = tables.load_evidence()
    recent = recent_lower_bounds()
    head = "".join(_heading(*column) for column in HEADERS)
    built = [case_row(case, evidence, recent=recent.get(case["n"], False)) for case in cases]
    rows = "\n".join(row for row, _ in built)
    popovers = "\n".join(popover for _, popover in built)
    return (
        f"{_tools(len(cases), max(case['n'] for case in cases))}\n"
        '<div class="site-table-wrap site-wide site-frontier" id="frontier-table">\n'
        '<table class="kpress-table site-table">\n'
        f"<thead><tr>{head}</tr></thead>\n<tbody>\n{rows}\n</tbody>\n</table>\n</div>\n"
        f"{popovers}\n{case_popover()}"
    )


def frontier_markdown(fill: Callable[..., str]) -> str:
    """The article with every count and link filled from the record."""
    cases = frontier_cases()
    recent = recent_lower_bounds()
    first, last = min(case["n"] for case in cases), max(case["n"] for case in cases)
    values = {
        "COUNT": str(len(cases)),
        # The subtitle's range, as math: the subtitle is an HTML block, where kpress
        # leaves `$…$` literal, and it is sans text, so the formula is set sans.
        "CASE_RANGE": math_html(rf"n = {first}, \ldots, {last}"),
        "PROVED": str(sum(case["status"] == "proved" for case in cases)),
        "OPEN": str(sum(case["status"] == "open" for case in cases)),
        "RECENT": str(sum(recent.values())),
        "RECENT_SINCE": f"{RECENT_SINCE:%B %Y}",
        "TABLE": table_html(cases),
    }
    template = FRONTIER_ARTICLE.read_text(encoding="utf-8")
    return fill(template, values, where=FRONTIER_ARTICLE.name)
