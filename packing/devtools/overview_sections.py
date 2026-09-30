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

from devtools.build_bound_citations import RECENT_SINCE
from devtools.overview_data import (
    APOSTROPHE,
    EN_DASH,
    REPO,
    Overview,
    Result,
    math_html,
    tex_bounds,
)
from devtools.render_overview import DOCUMENT_PAGES, branch_file
from devtools.render_recent_results import HOLDS, NOT_A_BOUND, STANDINGS, Lane

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


#: What the table and its filter call an entry that is no bound on `s(n)`:
#: `render_recent_results` spells that standing as a dash, which a filter cannot name.
NOT_A_BOUND_LABEL = "not a bound"


def standing_label(standing: str) -> str:
    """The words a standing chip shows: `render_recent_results`'s own, the dash spelled."""
    return NOT_A_BOUND_LABEL if standing == NOT_A_BOUND else standing


def standing_key(standing: str) -> str:
    """A standing as a row attribute and a filter value: `holds, reported` is
    `holds-reported`."""
    return re.sub(r"[^a-z]+", "-", standing_label(standing)).strip("-")


def standing_chip(standing: str) -> str:
    """A result's standing as a chip: the accent where a case bound rests on it now,
    the plain gray otherwise, so a reader sees at a glance which results still hold."""
    tone = ' data-tone="accent"' if standing == HOLDS else ""
    return (
        f'<span class="site-chip" data-standing="{_esc(standing_key(standing))}"{tone}>'
        f"{_esc(standing_label(standing))}</span>"
    )


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
    """One card per `S5` result, this project's and others' alike, with its rungs and its
    standing. Its popover previews the result, its claim, rationale, rungs, standing and
    records, and goes to its table row."""
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
        rungs += " " + standing_chip(result.standing)
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
    """A result's claim and why it matters; `full` adds its composition, next rung and
    novelty label, which the table row carries and a card's popover leaves to the row."""
    record = result.record
    rows = [("Claim", tex_bounds(" ".join(str(record["claim"]).split())))]
    for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
        if full and record.get(key):
            rows.append((label, tex_bounds(" ".join(str(record[key]).split()))))
    rows.append(
        ("Significance", tex_bounds(" ".join(str(record["significance"]["rationale"]).split())))
    )
    if full:
        meaning = novelty_labels().get(result.novelty, "")
        rows.append(
            (
                "Novelty",
                (
                    f'<span class="site-chip" data-novelty="{_esc(result.novelty)}">'
                    f"{_esc(result.novelty)}</span> {_esc(meaning)}"
                ),
            )
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
    """Every registered result, grouped as `RESULTS.md` groups them, which is by the
    relation `RESULTS.md` prints (`result_credit.source_lineage`), with its
    standing and, for a result by others, the date it was published."""
    present = {result.standing for result in overview.results}
    head = (
        "<thead><tr>"
        '<th data-sort="text">ID</th>'
        '<th data-sort="num">n</th>'
        '<th class="site-col-result">Result</th>'
        '<th data-sort="text">Credit</th>'
        '<th data-sort="text" title="Verification, confirmation and significance, then '
        'whether a case bound rests on the result now">Rungs</th>'
        '<th data-sort="text" title="Published, for a result by others; established, for '
        f'this project{APOSTROPHE}s">Date</th>'
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
            kind, date = result.dated
            body.append(
                f'<tr id="{_esc(result.id.lower())}" '
                f'data-source="{"ours" if result.ours else "others"}" '
                f'data-c="{_esc(record["confirmation"])}" '
                f'data-standing="{_esc(standing_key(result.standing))}">'
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
                f"{_rung('S' + str(record['significance']['score']))}"
                f'<span class="site-standing">{standing_chip(result.standing)}</span></td>'
                f'<td class="site-col-date" data-value="{_esc(date)}">'
                f'<span class="site-date-kind">{_esc(kind)}</span> {_esc(date)}</td>'
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
        '<label>Standing <select data-filter="standing">'
        '<option value="">all</option>'
        + "".join(
            f'<option value="{_esc(standing_key(standing))}">'
            f"{_esc(standing_label(standing))}</option>"
            for standing in STANDINGS
            if standing in present
        )
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


_NOVELTY_ROW = re.compile(r"^\| `([a-z]+(?:-[a-z]+)+)` \| ([^|]+?) \|$", re.MULTILINE)


def novelty_labels() -> dict[str, str]:
    """Each novelty label and its one-line meaning, read from the table in
    `epistemics.md` as `rubric_levels` reads the scored dimensions."""
    text = (REPO / "epistemics.md").read_text(encoding="utf-8")
    section = text.split("Novelty uses four labels", 1)[-1]
    labels = {label: meaning.strip() for label, meaning in _NOVELTY_ROW.findall(section)}
    for label in ("apparently-novel", "confirmed-novel", "previously-published"):
        if label not in labels:
            raise SystemExit(f"epistemics.md defines no novelty label {label}")
    return labels


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
    """The newest results, newest first, each with its standing. A result by others is
    dated by its publication, as `RESULTS.md` dates it, and this project's
    by the day it was established; the label says which."""
    newest = sorted(overview.results, key=lambda r: (r.dated[1], r.id), reverse=True)[:count]
    items = "".join(
        f'<li><span class="site-date">{_esc(r.dated[0])} {_esc(r.dated[1])}</span> · '
        f'<a href="#{_esc(r.id.lower())}">{_esc(r.id)}</a> · {tex_bounds(r.summary)} '
        f'<span class="site-credit">({_esc(r.credit)})</span> {standing_chip(r.standing)}</li>'
        for r in newest
    )
    return f'<ul class="site-recent">{items}</ul>'


def _since() -> str:
    """`RECENT_SINCE` as prose: 22 August 2026."""
    return f"{RECENT_SINCE.day} {RECENT_SINCE:%B %Y}"


def survey_counts(overview: Overview) -> str:
    """The survey's four counts as one Markdown sentence, from
    `render_recent_results.recent_counts`."""
    counts = overview.counts
    return (
        f"Of the hundred cases $n \\le 100$, {counts.cases} have a lower bound published or "
        f"proved since {_since()}, reported or verified; {counts.verified} of those have "
        f"a recent verified lower bound, the cases the atlas stars; {counts.ours} of the "
        f"{counts.verified} are this project{APOSTROPHE}s, and {counts.exact} are new "
        "exact values."
    )


_LANE_RESULT = re.compile(r"(T-\d{3}) `(V\d)/(C\d)`")


def _lane_math(lane: Lane) -> str:
    """A lane's value, as `render_recent_results.shown` writes it, set as math."""
    return math_html(lane.shown.replace("`", "").replace("\u2026", r"\ldots"))


def _lane_results(results: str) -> str:
    """A lane's results cell, the register entries carrying its bound as
    `render_recent_results.rungs` writes them, each linked to its row with its rungs."""
    return " ".join(
        f'<a href="#{_esc(entry.lower())}">{_esc(entry)}</a> {_rung(v)} {_rung(c)}'
        for entry, v, c in _LANE_RESULT.findall(results)
    )


def awaiting_replay(overview: Overview) -> str:
    """The recent cases whose reported lower bound differs from the verified one: a
    source's bound waiting on a replay here. One row per case, grouped by holder and the
    entries that carry the claim, each case linked to its row in the frontier atlas."""
    rows = overview.awaiting_replay
    if not rows:
        return ""
    groups: dict[tuple[str, str], list[str]] = {}
    for row in rows:
        reported = row.reported
        groups.setdefault((reported.holder, reported.results), []).append(
            f'<tr id="replay-n-{row.n}" data-n="{row.n}">'
            f'<td class="num"><a href="frontier.html#n-{row.n}">{row.n}</a></td>'
            f"<td>{_lane_math(reported)}</td>"
            f"<td>{_lane_math(row.verified)}</td>"
            f'<td class="site-col-date">{_esc(reported.published or "")}</td></tr>'
        )
    body = "".join(
        f'<tr class="site-group-row"><th colspan="4" scope="colgroup">{_esc(holder)} · '
        f"{_lane_results(results)}</th></tr>{''.join(members)}"
        for (holder, results), members in groups.items()
    )
    first, last = rows[0].n, rows[-1].n
    return (
        '<details class="site-wide site-replay">'
        f"<summary>Reported, awaiting replay: {len(rows)} cases, "
        f"{math_html(f'n = {first}')} to {last}</summary>"
        '<div class="site-table-wrap">'
        '<table class="kpress-table site-table site-replay-table">'
        "<thead><tr><th>n</th><th>Reported</th><th>Verified here</th><th>Published</th>"
        f"</tr></thead><tbody>{body}</tbody></table></div></details>"
    )


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
        "Improved packings for 49 counts from n = 68 to 307.",
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
    drawings, each linking to its case record, which `overview/case-popover.js` opens in
    the case popover beside the grid, and carrying its details for the hover card
    `overview/atlas-grid.js` shows.

    The cells, about a megabyte of SVG, sit in a `<template>`, which the browser parses
    but does not render; the script places them when the grid nears the viewport, so
    the page opens as fast as it did without them.
    """
    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import CASES_PAGE, case_popover, case_url  # noqa: PLC0415
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
            f'<a class="site-atlas-cell" href="{case_url(n)}" data-case="{n}" '
            f'data-status="{_esc(status)}" '
            f'aria-label="n = {n}, {_esc(status)}">{frontier.packing_svg(n)}'
            f'<span class="site-atlas-n">{n}</span>'
            f'<span class="site-atlas-detail" hidden>{detail}</span></a>'
        )
    return (
        '<div class="site-wide site-atlas-grid" data-atlas-grid>'
        f"<template>{''.join(cells)}</template>"
        '<p class="site-atlas-note">Every case from n = 1 to 324 is also in the '
        '<a href="frontier.html">frontier atlas</a>, and each has a '
        f'<a href="{CASES_PAGE}">case record</a>.</p>'
        f'<div class="site-atlas-tip" role="tooltip" hidden></div></div>{case_popover()}'
    )
