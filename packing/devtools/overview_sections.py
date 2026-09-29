"""The overview page's generated blocks, as HTML, from `devtools.overview_data`.

The page's prose lives in `templates/overview-article.md`; every block that states a
fact is built here and substituted into it, so a bound or a count never appears in the
template as a literal. Values are set as `$…$` inline math for KaTeX, and every table
works without scripts: rows are all present, details open with `<details>`, and
`overview/table.js` adds sorting and filters on top.
"""

from __future__ import annotations

import html

from devtools.overview_data import (
    APOSTROPHE,
    EN_DASH,
    REPO,
    Overview,
    Result,
    Stats,
    math_html,
    tex_bounds,
)
from devtools.render_overview import DOCUMENT_PAGES

#: Confirmation rungs from strongest to weakest.
C_RUNGS = ("C5", "C4", "C3", "C2", "C1", "C0")


def _esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def _fill(rung: str) -> str:
    """The attributes `site.css` colours a rung by: its scale, `V`, `C` or `S`, and its
    level, which darkens the fill. Badges, bar segments and legend swatches share them."""
    return f'data-rung="{_esc(rung[0])}" data-level="{_esc(rung[1:])}"'


def _rung(label: str) -> str:
    return f'<span class="site-chip site-rung-fill" {_fill(label)}>{_esc(label)}</span>'


def card_kind(href: str) -> str:
    """Where a card's popover leads, which its icons show: a row on this page, another
    site, or another page of this one."""
    if href.startswith("#"):
        return "scroll"
    if href.startswith("https://"):
        return "external"
    return "page"


def embed_url(href: str) -> str:
    """A site page's address framed in a popover: `view=embed`, which its `embed.js`
    reads to drop the site chrome, added before any fragment."""
    base, hash_mark, fragment = href.partition("#")
    joined = f"{base}{'&' if '?' in base else '?'}view=embed"
    return joined + hash_mark + fragment


def card(
    target: str,
    label: str,
    value: str,
    note: str,
    *,
    href: str,
    action: str,
    preview: str = "",
    also: tuple[str, str] | None = None,
) -> str:
    """A card and the popover it opens. The card is a caps label, the summary and a line
    under it; pressing it opens a popover that repeats the label and summary, shows
    where the card leads, and ends in a button that goes there.

    What the popover shows depends on the target. Another page of the site, a document
    among them, is rendered in the popover itself: framed narrow, without its site
    chrome, and the button expands it to the full page. A place on this page is
    previewed from `preview`, and the button scrolls there. `also` adds a second, quiet
    link, such as the document on GitHub.

    The popover is native (`popover`), so it opens, closes on Escape or a click outside,
    and follows its button with no script. It is set in sans, and its attribute tells
    kpress so, so its math is sans too. The label and action are escaped here; the value,
    note and preview are HTML, so they may carry math.
    """
    kind = card_kind(href)
    if kind == "page":
        body = (
            f'<iframe class="site-popover-frame" src="{_esc(embed_url(href))}" '
            f'loading="lazy" title="{_esc(label)}"></iframe>'
        )
    else:
        body = f'<div class="site-popover-preview">{preview}</div>'
    second = (
        f' <a class="site-popover-also" href="{_esc(also[0])}">{_esc(also[1])}</a>'
        if also
        else ""
    )
    return (
        f'<button type="button" class="site-card" popovertarget="{_esc(target)}" '
        f'data-go="{kind}">'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<span class="site-card-value">{value}</span>'
        f'<span class="site-card-note">{note}</span></button>'
        f'<div class="site-popover" id="{_esc(target)}" popover data-kpress-prose-font="sans" '
        f'data-go="{kind}">'
        f'<button type="button" class="site-popover-close" popovertarget="{_esc(target)}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<p class="site-popover-value">{value}</p>{body}'
        f'<p class="site-popover-actions"><a class="site-popover-action" href="{_esc(href)}" '
        f'data-go="{kind}">{_esc(action)}</a>{second}</p>'
        "</div>"
    )


def _cards(cards: list[str]) -> str:
    return '<div class="site-cards site-wide">' + "".join(cards) + "</div>"


def _dl(rows: list[tuple[str, str]]) -> str:
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def headline_cards(overview: Overview) -> str:
    """One card per `S5` result, this project's and others' alike. Its popover previews
    the result, its claim, rationale, rungs and records, and goes to its table row."""
    cards = []
    for result in overview.results:
        if result.record["significance"]["score"] < 5:
            continue
        record = result.record
        rungs = " ".join(
            _rung(rung)
            for rung in (
                record["verification"],
                record["confirmation"],
                "S" + str(record["significance"]["score"]),
            )
        )
        preview = (
            f"{_detail(result, full=False)}"
            f'<p class="site-popover-links">{rungs}</p>'
            f'<p class="site-popover-links">{_records(result)}</p>'
        )
        cards.append(
            card(
                f"pop-{result.id.lower()}",
                f"{result.id} · {result.credit}",
                tex_bounds(result.summary),
                rungs,
                preview=preview,
                href=f"#{result.id.lower()}",
                action=f"Show {result.id} in the table",
            )
        )
    return _cards(cards)


def exact_value_cards(overview: Overview) -> str:
    """Cases now proved by a recent verified lower bound: the new exact values. Each
    popover frames the case's row in the frontier atlas."""
    cards = []
    for n in sorted(overview.recent_lower):
        case = overview.cases[n]
        if case["status"] != "proved":
            continue
        lower = case["verified_lower_bound"]
        value = lower.get("exact_form") or lower.get("value")
        cards.append(
            card(
                f"pop-n-{n}",
                f"n = {n} · exact value",
                math_html(f"s({n}) = {value}"),
                "Proved by a recent lower bound.",
                href=f"frontier.html#n-{n}",
                action=f"Expand n = {n} in the frontier atlas",
            )
        )
    return _cards(cards)


def _detail(result: Result, *, full: bool = True) -> str:
    """A result's claim and why it matters; `full` adds its composition and next rung,
    which the table row carries and a card's popover leaves to the row."""
    record = result.record
    rows = [("Claim", tex_bounds(" ".join(str(record["claim"]).split())))]
    for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
        if full and record.get(key):
            rows.append((label, tex_bounds(" ".join(str(record[key]).split()))))
    rows.append(
        ("Significance", tex_bounds(" ".join(str(record["significance"]["rationale"]).split())))
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
        f'<span class="site-bar-seg site-rung-fill" {_fill(c)} style="flex:{counts[c]}"'
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


def verification_block(overview: Overview, stats: Stats) -> str:
    """Counts of results and cases, and the confirmation bar by source. Each count's
    popover shows what it counts: the result groups, above a button to the table here;
    the frontier atlas filtered to the cases it names; or the definition of the rungs."""
    from devtools.render_explainer import repo_file  # noqa: PLC0415

    groups = _dl(
        [(_esc(name), _esc(f"{len(results)} results")) for name, results in overview.groups]
    )
    cards = [
        card(
            "pop-count-results",
            "Registered results",
            _esc(stats.total),
            _esc(f"{stats.ours} this project{APOSTROPHE}s, {stats.others} by others"),
            preview=groups,
            href="#every-result",
            action="Show every result",
        ),
        card(
            "pop-count-cases",
            f"Cases n = 1{EN_DASH}100",
            _esc(f"{stats.cases_1_100_proved} proved"),
            _esc(f"{stats.cases_1_100_open} still open"),
            href="frontier.html?n-max=100",
            action="Expand these cases in the frontier atlas",
        ),
        card(
            "pop-count-recent",
            "Recent lower bounds",
            _esc(stats.recent_lower_total),
            "verified lower bounds proved since 22 August 2026",
            href="frontier.html?recent=true",
            action="Expand these cases in the frontier atlas",
        ),
        card(
            "pop-count-verification",
            "Verification",
            _esc(f"{stats.verification.get('V4', 0)} at V4"),
            _esc(
                ", ".join(
                    f"{v} {k}" for k, v in sorted(stats.verification.items(), reverse=True)
                )
            ),
            href="epistemics.html#verification",
            action="Expand epistemics.md",
            also=(repo_file(REPO / "epistemics.md"), "On GitHub"),
        ),
    ]
    grid = "".join(cards)
    legend = "".join(
        f'<span><i class="site-rung-fill" {_fill(c)}></i>{c}</span>' for c in C_RUNGS
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


#: The repository's reader documents, as the overview's cards show them: the file, a
#: label, and one line on what a reader finds there. README and the synopsis lead.
DOCUMENTS: tuple[tuple[str, str, str], ...] = (
    (
        "README.md",
        "The Squares Project",
        "What the project is, how it works, and where to start.",
    ),
    ("SYNOPSIS.md", "The synopsis", "The full research record: methods, claims and status."),
    ("packing/frontier/RESULTS.md", "Results", "Every registered result with its rungs."),
    ("packing/frontier/STATUS.md", "The frontier", "Every case to 324, with provenance."),
    ("epistemics.md", "Epistemics", "How each result is verified, confirmed and scored."),
    ("conventions.md", "Conventions", "Record formats, identifiers and naming."),
    ("development.md", "Development", "Building, testing and validating the code."),
    ("defects.md", "Defect log", "Every defect found in the toolchain, one line each."),
)


def document_cards() -> str:
    """One card per reader document; its popover renders the document, served as a page
    of the site, and expands to it, with the file on GitHub beside."""
    from devtools.render_explainer import repo_file  # noqa: PLC0415

    return _cards(
        [
            card(
                f"pop-doc-{page.removesuffix('.html')}",
                path.rsplit("/", 1)[-1],
                _esc(label),
                _esc(note),
                href=page,
                action=f"Expand {path.rsplit('/', 1)[-1]}",
                also=(repo_file(REPO / path), "On GitHub"),
            )
            for (path, label, note), page in zip(DOCUMENTS, DOCUMENT_PAGES, strict=True)
        ]
    )


#: The site's other pages, as the overview's cards show them: the page, a label, its
#: title, and one line on what a reader finds there.
PAGES: tuple[tuple[str, str, str, str], ...] = (
    (
        "explainer.html",
        "Explainer",
        "The n = 11 lower bound",
        "The proof, with the certificate drawn and checkable in the page.",
    ),
    (
        "tutorial.html",
        "Tutorial",
        "Square packing from first principles",
        "The problem, its configuration space, exact algebra and the search.",
    ),
    (
        "workbench/",
        "Visualizer",
        "Pack squares by hand",
        "Move squares yourself and watch the known packings.",
    ),
    (
        "frontier.html",
        "Frontier atlas",
        "Every case from n = 1 to 324",
        "Reported and verified bounds side by side, with their sources.",
    ),
)


def page_cards() -> str:
    """One card per page of the site other than this one; its popover renders the page
    and expands to it."""
    return _cards(
        [
            card(
                f"pop-page-{label.split()[0].lower()}",
                label,
                tex_bounds(title),
                _esc(note),
                href=href,
                action=f"Expand the {label.lower()}",
            )
            for href, label, title, note in PAGES
        ]
    )


#: The case drawn large under the homepage's title.
HERO_CASE = 53


def hero() -> str:
    """The homepage's picture: one known-best packing, drawn from its atlas rendering
    and linked to its row in the frontier atlas."""
    from devtools.render_frontier_page import packing_svg  # noqa: PLC0415

    n = HERO_CASE
    return (
        f'<figure class="site-hero-figure"><a href="frontier.html#n-{n}" '
        f'aria-label="The best packing known for {n} squares, in the frontier atlas">'
        f"{packing_svg(n, units=1000)}</a>"
        f"<figcaption>The best packing known for {n} squares</figcaption></figure>"
    )
