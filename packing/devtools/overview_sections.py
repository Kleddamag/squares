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

from devtools import repo_links
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
from devtools.render_overview import DOCUMENT_PAGES
from devtools.render_recent_results import HOLDS, NOT_A_BOUND, STANDINGS, Lane
from devtools.repo_links import branch_file

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
    frame = '<div class="site-cards-frame site-wide"><div class="site-cards">'
    return frame + "".join(cards) + "</div></div>"


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
    text = (REPO / repo_links.EPISTEMICS).read_text(encoding="utf-8")
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
    text = (REPO / repo_links.EPISTEMICS).read_text(encoding="utf-8")
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
                also=(branch_file(repo_links.EPISTEMICS, f"#{section}"), "On GitHub"),
            )
        )
    return (
        '<div class="site-cards-frame site-wide"><div class="site-cards site-cards-dimensions">'
        f"{''.join(cards)}</div></div>"
    )


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
        repo_links.README,
        "The Squares Project",
        "What the project is, how it works, and where to start.",
    ),
    (
        repo_links.SYNOPSIS,
        "The synopsis",
        "The full research record: methods, claims and status.",
    ),
    (repo_links.RESULTS, "Results", "Every registered result with its rungs."),
    (repo_links.STATUS, "The frontier", "Every case to 324, with provenance."),
    (repo_links.EPISTEMICS, "Epistemics", "How each result is verified, confirmed and scored."),
    (repo_links.CONVENTIONS, "Conventions", "Record formats, identifiers and naming."),
    (repo_links.DEVELOPMENT, "Development", "Building, testing and validating the code."),
    (repo_links.DEFECTS, "Defect log", "Every defect found in the toolchain, one line each."),
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


#: The atlas grid's drawings, in units across the frame. One drawing serves the cell and
#: the popover, which shows it about four hundred pixels across: at 100 units the
#: rounding shows there as uneven gaps, and 400 costs about 26 kB more gzipped.
ATLAS_UNITS = 400

#: The film's panel labels, keyed by the composite record's badge (glyph, style): the
#: words `packages/workbench/src/view/facts.ts` draws under each badge (`BADGE_LABELS`).
FILM_BADGES: dict[tuple[str, str], str] = {
    ("O", "solid"): "optimal",
    ("=", "solid"): "exact",
    ("\u2248", "muted"): "numerical",
    ("R", "solid"): "rigid",
    ("R", "muted"): "rigid (catalogue)",
}

#: `side.display` and `lower.display` as the composite record writes them.
_FILM_DISPLAY = re.compile(r"^s\((\d+)\) ([=\u2264\u2265]) (.+)$")


def _film_value(display: str, n: int, relations: str) -> tuple[str, str]:
    match = _FILM_DISPLAY.match(display)
    if match is None or int(match[1]) != n or match[2] not in relations:
        raise SystemExit(f"n = {n}: the atlas figure's {display!r} is not s({n}) {relations}")
    return match[2], match[3]


def atlas_film_facts() -> list[dict[str, object]]:
    """What the ascent film's panel says about each case, n = 1 to 324, read as the film
    reads it (`packages/workbench/tools/workbench_tools/build_candidate.py`, `load_facts`
    and `load_citations`).

    From the atlas figure's record: the bound as one statement, its values as the record
    displays them, the badges, a star where the lower bound is a recent result, and what
    is open (rigidity never is, as in the film). From `bound-citations.json`: the frontier
    record and each bound's source with this project's note.
    """
    import json  # noqa: PLC0415

    from devtools.overview_data import CITATIONS, COMPOSITE  # noqa: PLC0415

    figure = json.loads(COMPOSITE.read_text(encoding="utf-8"))["figure"]["entries"]
    cited = {
        entry["n"]: entry
        for entry in json.loads(CITATIONS.read_text(encoding="utf-8"))["citations"]["entries"]
    }
    facts: list[dict[str, object]] = []
    for entry in figure:
        n = entry["n"]
        relation, upper = _film_value(entry["side"]["display"], n, "=\u2264")
        lower = (
            _film_value(entry["lower"]["display"], n, "\u2265")[1]
            if entry["lower"]["shown"]
            else None
        )
        badges: list[list[str]] = []
        for badge in entry["badges"]:
            key = (badge["glyph"], badge["style"])
            if key not in FILM_BADGES:
                raise SystemExit(f"n = {n}: badge {key} is not one the film draws")
            badges.append([badge["glyph"], badge["style"], FILM_BADGES[key]])
        open_items: list[str] = []
        if entry["optimality"]["status"] == "open":
            open_items.append("optimality")
        if entry["exactness"]["state"] not in ("closed-form", "minimal-polynomial"):
            open_items.append("exact value")
        record = cited[n]
        citations = {
            bound: None
            if record.get(bound) is None
            else {"text": record[bound]["text"], "note": record[bound]["note"]}
            for bound in ("lower", "upper")
        }
        facts.append(
            {
                "n": n,
                "exact": relation == "=",
                "upper": upper,
                "lower": lower,
                "star": bool(entry["lower"]["recent_result"]),
                "badges": badges,
                "open": open_items,
                "record": record["record"],
                "cite": citations,
            }
        )
    if [fact["n"] for fact in facts] != list(range(1, len(facts) + 1)):
        raise SystemExit("the atlas figure's entries are not n = 1, 2, 3 and on, in order")
    return facts


def _atlas_formula(key: str, tex: str) -> str:
    return (
        f'<span class="site-atlas-gap-formula" data-atlas-formula="{key}">'
        f"{math_html(tex)}</span>"
    )


def atlas_popover() -> str:
    """The one popover every atlas cell opens, filled by `overview/atlas-grid.js` from
    the page's film facts. Its slots are empty here but for what is the same at every n:
    the gap bar's two formulas, and the template each value's math is typeset from."""
    return (
        '<div class="site-popover site-atlas-pop" id="pop-atlas" popover '
        'data-kpress-prose-font="sans" data-go="atlas" data-atlas-popover '
        'role="dialog" aria-labelledby="pop-atlas-title">'
        '<button type="button" class="site-popover-close" popovertarget="pop-atlas" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        '<span class="site-card-label">Best known packing</span>'
        '<p class="site-popover-value site-atlas-pop-title" id="pop-atlas-title" '
        "data-atlas-title></p>"
        '<div class="site-atlas-pop-body">'
        '<div class="site-atlas-pop-figure" data-atlas-figure></div>'
        '<div class="site-atlas-pop-facts">'
        '<div class="site-atlas-gap" data-atlas-gap>'
        '<div class="site-atlas-gap-values" data-atlas-gap-values></div>'
        '<div class="site-atlas-gap-rail" data-atlas-gap-rail></div>'
        '<div class="site-atlas-gap-row" data-atlas-gap-integers></div>'
        '<div class="site-atlas-gap-row" data-atlas-gap-roots></div>'
        '<div class="site-atlas-gap-row site-atlas-gap-formulas">'
        + _atlas_formula("area", r"\sqrt{n}")
        + _atlas_formula("grid", r"\sqrt{n} + 1")
        + "</div></div>"
        '<p class="site-atlas-pop-head">Proven</p>'
        '<p class="site-atlas-pop-bound" data-atlas-bound></p>'
        '<ul class="site-atlas-pop-badges" data-atlas-badges></ul>'
        "<div data-atlas-citation>"
        '<p class="site-atlas-pop-head">Citation '
        '<span class="site-atlas-pop-record">record <span data-atlas-record></span></span></p>'
        '<p class="site-atlas-pop-cite" data-atlas-cite="lower"></p>'
        '<p class="site-atlas-pop-cite" data-atlas-cite="upper"></p></div>'
        '<div data-atlas-open><p class="site-atlas-pop-head">Open</p>'
        '<ul class="site-atlas-pop-badges" data-atlas-open-items></ul></div>'
        "</div></div>"
        '<p class="site-popover-actions">'
        '<a class="site-popover-action" data-go="page" data-atlas-expand href="cases.html">'
        "Open the case record</a>"
        '<span class="site-atlas-pop-step">'
        '<button type="button" data-atlas-step="-1" aria-label="Previous case">\u2190</button>'
        '<button type="button" data-atlas-step="1" aria-label="Next case">\u2192</button>'
        "</span></p>"
        f"<template data-atlas-math>{math_html('n')}</template>"
        "</div>"
    )


def atlas_grid() -> str:
    """Every tracked case's known-best packing, n = 1 to 324, as a grid of drawings,
    each a link to its case record. With scripts, `overview/atlas-grid.js` opens a cell
    in the one atlas popover instead: what the ascent film's panel says about that n,
    from `atlas_film_facts`, beside the drawing shown large, with a button to the record.

    The cells, about a megabyte of SVG, sit in a `<template>`, which the browser parses
    but does not render; the script places them when the grid nears the viewport, so
    the page opens as fast as it did without them. The facts are one JSON element, a
    tenth the size the same facts would take as markup in every cell.
    """
    import json  # noqa: PLC0415

    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import CASES_PAGE, case_url  # noqa: PLC0415

    cells = []
    for case in frontier.frontier_cases():
        n = case["n"]
        status = case["status"]
        cells.append(
            f'<a class="site-atlas-cell" href="{case_url(n)}" data-atlas-n="{n}" '
            f'data-status="{_esc(status)}" aria-label="n = {n}, {_esc(status)}">'
            f"{frontier.packing_svg(n, units=ATLAS_UNITS)}"
            f'<span class="site-atlas-n">{n}</span></a>'
        )
    facts = json.dumps(atlas_film_facts(), ensure_ascii=False, separators=(",", ":"))
    return (
        '<div class="site-wide site-atlas-grid" data-atlas-grid>'
        f"<template>{''.join(cells)}</template>"
        '<script type="application/json" data-atlas-facts>'
        + facts.replace("</", "<\\/")
        + "</script>"
        '<p class="site-atlas-note">Every case from n = 1 to 324 is also in the '
        '<a href="frontier.html">frontier atlas</a>, and each has a '
        f'<a href="{CASES_PAGE}">case record</a>.</p></div>{atlas_popover()}'
    )
