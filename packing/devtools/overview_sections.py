"""The overview page's generated blocks, as HTML, from `devtools.overview_data`.

The page's prose lives in `templates/overview-article.md`; every block that states a
fact is built here and substituted into it, so a bound or a count never appears in the
template as a literal. Values are set as `$…$` inline math for KaTeX, and every table
works without scripts: rows are all present, details open with `<details>`, and
`overview/table.js` adds sorting and filters on top.
"""

from __future__ import annotations

import html
import re

from devtools.overview_data import (
    EN_DASH,
    REPO,
    Overview,
    Result,
    math_html,
    tex_bounds,
)
from devtools.render_overview import DOCUMENT_PAGES, branch_file

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


#: The rubric's three scored dimensions, in the homepage's order: the scale, its name,
#: the `epistemics.md` section that defines it, and the question it answers.
DIMENSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("V", "Verification", "verification", "How strongly is the claim checked, by anyone?"),
    ("C", "Confirmation", "confirmation", "What has this repository checked itself?"),
    ("S", "Significance", "significance-and-novelty", "How much does the result matter?"),
)

_LEVEL_ROW = re.compile(r"^\| `([VCS])(\d)` \| ([^|]+?) \|", re.MULTILINE)


def rubric_levels() -> dict[str, list[tuple[int, str]]]:
    """Each dimension's levels and their one-line meanings, read from the tables in
    `epistemics.md`, so a card cannot drift from the rubric it summarizes."""
    text = (REPO / "epistemics.md").read_text(encoding="utf-8")
    levels: dict[str, list[tuple[int, str]]] = {}
    for scale, level, meaning in _LEVEL_ROW.findall(text):
        levels.setdefault(scale, []).append((int(level), meaning.strip()))
    for scale, *_ in DIMENSIONS:
        if not levels.get(scale):
            raise SystemExit(f"epistemics.md defines no {scale} levels")
    return levels


def verification_block() -> str:
    """One card per dimension of the rubric: its question and every level, as the chip
    the tables use and the rubric's meaning. Each card's popover renders that section of
    `epistemics.md`."""

    levels = rubric_levels()
    cards = []
    for scale, name, section, question in DIMENSIONS:
        ladder = "".join(
            f'<span class="site-level"><span class="site-chip site-rung-fill" '
            f'data-rung="{scale}" data-level="{level}">{scale}{level}</span> '
            f"{_esc(meaning)}</span>"
            for level, meaning in sorted(levels[scale], reverse=True)
        )
        cards.append(
            card(
                f"pop-dimension-{scale.lower()}",
                f"{scale}{levels[scale][0][0]}{EN_DASH}{scale}{levels[scale][-1][0]}",
                _esc(name),
                f'<span class="site-level-question">{_esc(question)}</span>{ladder}',
                href=f"epistemics.html#{section}",
                action=f"Expand {name} in epistemics.md",
                also=(f"{branch_file('epistemics.md')}#{section}", "On GitHub"),
            )
        )
    return f'<div class="site-cards site-cards-dimensions site-wide">{"".join(cards)}</div>'


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
    of the site, and expands to it, with its latest version on GitHub beside."""
    return _cards(
        [
            card(
                f"pop-doc-{page.removesuffix('.html')}",
                path.rsplit("/", 1)[-1],
                _esc(label),
                _esc(note),
                href=page,
                action=f"Expand {path.rsplit('/', 1)[-1]}",
                also=(branch_file(path), "On GitHub"),
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


#: The other public square-packing projects on GitHub that the research frontier cites:
#: each repository's home, its author as the record credits them (the GitHub handle
#: where the record names no one), and what it holds. A test holds this list to cover
#: every source repository in the source-coverage register.
OTHER_PROJECTS: tuple[tuple[str, str, str], ...] = (
    (
        "https://github.com/evand/square-packing",
        "Evan Daniel",
        "Exact weighted certificates and zero-margin closed covers, closing n = 21, 32 and 45.",
    ),
    (
        "https://github.com/wand125/square-packing-bounds",
        "wand125",
        "Weighted point and rectangle-density lower-bound certificates across many n.",
    ),
    (
        "https://github.com/tokoharu/square-packing-density-bounds",
        "Tokoharu",
        "Rectangle-density lower-bound certificates.",
    ),
    (
        "https://github.com/franciscouzo/square-packing",
        "Francisco Couzo",
        "Improved packings for dozens of n between 68 and 300.",
    ),
    (
        "https://github.com/griffcass/square-packing",
        "Griffin Casson",
        "Improved packings for n = 103, 105 and other cases.",
    ),
    (
        "https://github.com/JoostdeWinter/square-packing-211",
        "Joost de Winter",
        "A packing of 211 squares in a square of side under 15.",
    ),
    (
        "https://github.com/Kleddamag/11-squares-certified-bound",
        "Kleddamag",
        "A certified lower bound for eleven squares.",
    ),
    (
        "https://github.com/Kleddamag/17-squares-certified-bound",
        "Kleddamag",
        "Certified lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/Guzhou0806/n17-square-packing",
        "Guzhou0806",
        "Strict lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/DRMacIver/square-packing-research",
        "David R. MacIver",
        "A lower bound for seventeen squares, with its paper and a Lean check.",
    ),
    (
        "https://github.com/ahyangyi/17squares",
        "ahyangyi",
        "A lower-bound proof for seventeen squares.",
    ),
    (
        "https://github.com/anabologyco-maker/square17-lower-bound",
        "anabologyco-maker",
        "A weighted fractional lower bound for seventeen squares.",
    ),
    (
        "https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record",
        "Thomas Schadt",
        "A record packing of 29 squares.",
    ),
)


def other_project_cards() -> str:
    """One card per other project: its repository's name and owner, its author, and what
    it holds. Each leads off the site, so its popover previews it and its button opens
    the repository's home page."""
    cards = []
    for url, author, note in OTHER_PROJECTS:
        owner, name = url.removeprefix("https://github.com/").split("/")
        slug = re.sub(r"[^a-z0-9]+", "-", f"{owner}-{name}".lower()).strip("-")
        cards.append(
            card(
                f"pop-project-{slug}",
                f"By {author}",
                _esc(name),
                _esc(note),
                preview=_dl(
                    [("Repository", _esc(f"{owner}/{name}")), ("Author", _esc(author))]
                ),
                href=url,
                action=f"Open {owner}/{name} on GitHub",
            )
        )
    return _cards(cards)


def atlas_grid() -> str:
    """Every tracked case's known-best packing, n = 1 to 324, as a grid of small
    drawings, each linking to its row in the frontier atlas and carrying its details for
    the hover card `overview/atlas-grid.js` shows.

    The cells, about a megabyte of SVG, sit in a `<template>`, which the browser parses
    but does not render; the script places them when the grid nears the viewport, so
    the page opens as fast as it did without them.
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from sqpack.assurance import bounds_agree_at_declared_precision  # noqa: PLC0415

    recent = frontier.recent_lower_bounds()
    cells = []
    for case in frontier.frontier_cases():
        n = case["n"]
        upper = case["reported_upper_bound"]
        reported_lower, verified_lower = (
            case["reported_lower_bound"],
            case["verified_lower_bound"],
        )
        status = case["status"]
        tone = ' data-tone="accent"' if status == "proved" else ""
        star = (
            '<span class="site-star" title="Recent lower bound">\u2605</span>'
            if recent.get(n)
            else ""
        )
        lower_by = (
            frontier.credit(reported_lower.get("proved_by"), reported_lower.get("proved_year"))
            if bounds_agree_at_declared_precision(reported_lower, verified_lower)
            else "verified here"
        )
        detail = (
            f'<span class="site-atlas-head"><b>n = {n}</b> '
            f'<span class="site-chip"{tone}>{_esc(status)}</span> {star}</span>'
            f'<span class="site-atlas-row"><span>Best known</span> '
            f"<b>{_esc(frontier.decimal_text(upper['value']))}</b> "
            f"<i>{frontier.credit(upper.get('found_by'), upper.get('found_year'))}</i></span>"
            f'<span class="site-atlas-row"><span>Lower bound</span> '
            f"<b>{_esc(frontier.decimal_text(verified_lower['value']))}</b> "
            f"<i>{lower_by}</i></span>"
        )
        cells.append(
            f'<a class="site-atlas-cell" href="frontier.html#n-{n}" '
            f'data-status="{_esc(status)}" '
            f'aria-label="n = {n}, {_esc(status)}">{frontier.packing_svg(n)}'
            f'<span class="site-atlas-n">{n}</span>'
            f'<span class="site-atlas-detail" hidden>{detail}</span></a>'
        )
    return (
        '<div class="site-wide site-atlas-grid" data-atlas-grid>'
        f"<template>{''.join(cells)}</template>"
        '<p class="site-atlas-note">Every case from n = 1 to 324 is also in the '
        '<a href="frontier.html">frontier atlas</a>.</p>'
        '<div class="site-atlas-tip" role="tooltip" hidden></div></div>'
    )
