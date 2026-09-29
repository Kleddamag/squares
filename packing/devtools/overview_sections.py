"""The overview page's generated blocks, as HTML, from `devtools.overview_data`.

The page's prose lives in `templates/overview-article.md`; every block that states a
fact is built here and substituted into it, so a bound or a count never appears in the
template as a literal. Values are set as `$…$` inline math for KaTeX, and every table
works without scripts: rows are all present, details open with `<details>`, and
`overview/table.js` adds sorting and filters on top.
"""

from __future__ import annotations

import html
from decimal import Decimal
from fractions import Fraction

from devtools.overview_data import (
    APOSTROPHE,
    EN_DASH,
    Overview,
    Result,
    Stats,
    math_html,
    tex_bounds,
)

#: Confirmation rungs from strongest to weakest, with their bar colours (kpress-neutral
#: hues chosen to stay distinct in both themes).
C_RUNGS = ("C5", "C4", "C3", "C2", "C1", "C0")
C_COLOURS = {
    "C5": "oklch(45% 0.09 186)",
    "C4": "oklch(55% 0.09 186)",
    "C3": "oklch(66% 0.08 186)",
    "C2": "oklch(70% 0.10 70)",
    "C1": "oklch(66% 0.12 45)",
    "C0": "oklch(62% 0.02 260)",
}


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def _tex_value(exact: str | None, value: str | None) -> str:
    """A bound as inline TeX: a fraction as `a/b`, else its decimal."""
    if exact and "/" in exact and "root" not in exact and "sqrt" not in exact:
        return exact
    if value:
        return value
    return exact or ""


def bracket_11(overview: Overview) -> dict[str, str]:
    """The central case's bracket and gap, read from `n-011.md`."""
    case = overview.cases[11]
    lower = case["verified_lower_bound"]
    upper = case["verified_upper_bound"]
    lower_value = (
        Fraction(lower["exact_form"])
        if lower.get("exact_form")
        else Fraction(Decimal(lower["value"]))
    )
    upper_decimal = Decimal(upper["value"])
    gap = Decimal(
        float(upper_decimal - Decimal(lower_value.numerator) / lower_value.denominator)
    )
    upper_short = f"{upper_decimal:.7f}".rstrip("0")
    return {
        "S11_LOWER": _tex_value(lower.get("exact_form"), lower.get("value")),
        "S11_LOWER_DECIMAL": f"{float(lower_value):.3f}",
        "S11_UPPER": upper_short + r"\ldots",
        "S11_GAP": f"{gap:.4f}",
        "S11_UPPER_BY": _esc(", ".join(case["reported_upper_bound"].get("found_by") or [])),
        "S11_UPPER_YEAR": _esc(case["reported_upper_bound"].get("found_year") or ""),
    }


def _rung(label: str) -> str:
    return f'<span class="site-rung">{_esc(label)}</span>'


def headline_cards(overview: Overview) -> str:
    """One card per `S5` result, this project's and others' alike."""
    cards = []
    for result in overview.results:
        if result.record["significance"]["score"] < 5:
            continue
        record = result.record
        cards.append(
            '<div class="site-card">'
            f'<div class="site-card-label">{_esc(result.id)} · {_esc(result.credit)}</div>'
            f'<div class="site-card-value">{tex_bounds(result.summary)}</div>'
            '<div class="site-card-note">'
            f"{_rung(record['verification'])} {_rung(record['confirmation'])} "
            f"{_rung('S' + str(record['significance']['score']))} · "
            f'<a href="#{_esc(result.id.lower())}">in the table</a></div>'
            "</div>"
        )
    return '<div class="site-cards site-wide">' + "".join(cards) + "</div>"


def exact_value_cards(overview: Overview) -> str:
    """Cases now proved by a recent verified lower bound: the new exact values."""
    cards = []
    for n in sorted(overview.recent_lower):
        case = overview.cases[n]
        if case["status"] != "proved":
            continue
        lower = case["verified_lower_bound"]
        value = lower.get("exact_form") or lower.get("value")
        cards.append(
            '<div class="site-card">'
            f'<div class="site-card-label">n = {n} · exact value</div>'
            f'<div class="site-card-value">{math_html(f"s({n}) = {value}")}</div>'
            '<div class="site-card-note">'
            f'<a href="frontier.html#n-{n}">frontier record</a></div>'
            "</div>"
        )
    return '<div class="site-cards site-wide">' + "".join(cards) + "</div>"


def _detail(result: Result) -> str:
    record = result.record
    rows = [("Claim", tex_bounds(" ".join(str(record["claim"]).split())))]
    for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
        if record.get(key):
            rows.append((label, tex_bounds(" ".join(str(record[key]).split()))))
    rows.append(
        ("Significance", _esc(" ".join(str(record["significance"]["rationale"]).split())))
    )
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def _records(result: Result) -> str:
    return " · ".join(
        f'<a href="{_esc(link.url)}"'
        + (f' title="{_esc(link.title)}"' if link.title else "")
        + f">{_esc(link.label)}</a>"
        for link in result.records
    )


def results_table(overview: Overview) -> str:
    """Every registered result, grouped as `RESULTS.md` groups them."""
    head = (
        "<thead><tr>"
        '<th data-sort="text">ID</th>'
        '<th data-sort="num">n</th>'
        '<th class="site-col-result">Result</th>'
        '<th data-sort="text">Credit</th>'
        '<th data-sort="text" title="Verification, confirmation and significance">Rungs</th>'
        '<th data-sort="text">Date</th>'
        "<th>Records</th>"
        "</tr></thead>"
    )
    body = []
    for title, members in overview.groups:
        body.append(
            f'<tr class="site-group-row" data-group="{_esc(title)}">'
            f'<th colspan="7" scope="colgroup">{_esc(title)}</th></tr>'
        )
        for result in members:
            record = result.record
            body.append(
                f'<tr id="{_esc(result.id.lower())}" '
                f'data-source="{"ours" if result.ours else "others"}" '
                f'data-c="{_esc(record["confirmation"])}">'
                f'<td class="site-col-id" data-value="{_esc(result.id)}">{_esc(result.id)}</td>'
                f'<td class="num site-col-n" data-value="{result.first_n}">'
                f"{_esc(result.scope)}</td>"
                f'<td class="site-col-result"><details><summary>'
                f"{tex_bounds(result.summary)}</summary>"
                f"{_detail(result)}</details></td>"
                f'<td class="site-col-credit" data-value="{_esc(result.credit)}">'
                f"{_esc(result.credit)}</td>"
                f'<td class="site-rungs" '
                f'data-value="{_esc(record["confirmation"] + record["verification"])}">'
                f"{_rung(record['verification'])} {_rung(record['confirmation'])} "
                f"{_rung('S' + str(record['significance']['score']))}</td>"
                f'<td class="site-col-date" data-value="{_esc(result.date)}">'
                f"{_esc(result.date)}</td>"
                f'<td class="site-records">{_records(result)}</td>'
                "</tr>"
            )
    tools = (
        '<div class="site-table-tools">'
        '<label>Source <select data-filter="source">'
        '<option value="">all</option><option value="ours">this project</option>'
        '<option value="others">others</option></select></label>'
        '<label>Confirmation <select data-filter="c">'
        '<option value="">all</option>'
        + "".join(f'<option value="{c}">{c}</option>' for c in C_RUNGS)
        + "</select></label>"
        '<span class="site-count" data-count></span>'
        "</div>"
    )
    return (
        f'<div class="site-wide">{tools}<div class="site-table-wrap">'
        f'<table class="kpress-table site-table site-results" data-site-table>{head}'
        f"<tbody>{''.join(body)}</tbody></table></div></div>"
    )


def _bar(label: str, counts: dict[str, int]) -> str:
    total = sum(counts.values()) or 1
    segments = "".join(
        f'<span class="site-bar-seg" style="flex:{counts[c]};background:{C_COLOURS[c]}"'
        f' title="{c}: {counts[c]}">{counts[c]}</span>'
        for c in C_RUNGS
        if counts.get(c)
    )
    return (
        f'<div class="site-bar-row"><span>{_esc(label)} ({sum(counts.values())})</span>'
        f'<span class="site-bar-track" aria-label="{_esc(label)}: '
        + ", ".join(f"{c} {counts[c]}" for c in C_RUNGS if counts.get(c))
        + f'" data-total="{total}">{segments}</span></div>'
    )


def verification_block(stats: Stats) -> str:
    """Counts of results and cases, and the confirmation bar by source."""
    cards = [
        (
            "Registered results",
            str(stats.total),
            f"{stats.ours} this project{APOSTROPHE}s, {stats.others} by others",
        ),
        (
            f"Cases n = 1{EN_DASH}100",
            f"{stats.cases_1_100_proved} proved",
            f"{stats.cases_1_100_open} still open",
        ),
        (
            "Recent lower bounds",
            str(stats.recent_lower_total),
            "verified lower bounds proved since 22 August 2026",
        ),
        (
            "Verification",
            f"{stats.verification.get('V4', 0)} at V4",
            ", ".join(f"{v} {k}" for k, v in sorted(stats.verification.items(), reverse=True)),
        ),
    ]
    grid = "".join(
        '<div class="site-card">'
        f'<div class="site-card-label">{_esc(label)}</div>'
        f'<div class="site-card-value">{_esc(value)}</div>'
        f'<div class="site-card-note">{_esc(note)}</div></div>'
        for label, value, note in cards
    )
    legend = "".join(
        f'<span><i style="background:{C_COLOURS[c]}"></i>{c}</span>' for c in C_RUNGS
    )
    bars = _bar("This project", dict(stats.confirmation_ours)) + _bar(
        "By others", dict(stats.confirmation_others)
    )
    return (
        f'<div class="site-cards site-wide">{grid}</div>'
        f'<div class="site-bar">{bars}</div><div class="site-legend">{legend}</div>'
    )


def recent_list(overview: Overview, count: int = 8) -> str:
    """The newest results by date, newest first."""
    newest = sorted(overview.results, key=lambda r: (r.date, r.id), reverse=True)[:count]
    items = "".join(
        f'<li><span class="site-date">{_esc(r.date)}</span> · '
        f'<a href="#{_esc(r.id.lower())}">{_esc(r.id)}</a> · {tex_bounds(r.summary)} '
        f'<span class="site-credit">({_esc(r.credit)})</span></li>'
        for r in newest
    )
    return f'<ul class="site-recent">{items}</ul>'
