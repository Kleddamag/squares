#!/usr/bin/env python3
"""The overview page, the site's front door, rendered into the shared site shell.

Its prose lives in `templates/overview-article.md`, reviewed as prose and formatted by
flowmark; every fact in it is a placeholder filled from the record, so no bound is ever a
literal in the template. `devtools.render_overview` collects the page from `pages()`.

**What the page is made of.** The record comes from three contracts, each owned by its
own module: `overview_data.load()` (the register, the case records, the credits and the
notable sources), `overview_media` (the atlas previews, the film and the hero drawing)
and `reader_documents.reader_documents()` (the documents the page lists as cards).
`render()` turns them into the page's HTML and never reads anything else, so a test can
hand it fixture instances of the same types.

**How the page is assembled.** The template is rendered by kpress like every site page,
with inline placeholders (dates, counts, links) filled before parsing. Block placeholders
(the cards, the table, the media) stand alone in a paragraph and are replaced after
parsing, so the generated HTML never passes through the Markdown parser. Each `h2` is
then given the stable id `SECTIONS` names, because the explainer uses the natural slug of
the first heading and the overview's ids and the explainer's must stay disjoint (the
fragment forwarder in `overview/forward.js` sends any fragment the overview lacks to the
explainer).

**The design system** these blocks are written in (cards, chips, rung badges, the
results table, the popover) is `templates/site-design.md`; `templates/site.css` is its
stylesheet and the scripts under `overview/` its behaviour. Every card is a link, and
the page works with JavaScript off.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

from latex2mathml.converter import convert as convert_latex_math

from devtools import (
    overview_data,
    overview_media,
    reader_documents,
    render_explainer,
    render_recent_results,
)
from devtools.overview_data import (
    AtlasTotals,
    Bound,
    ExplainerEdition,
    Link,
    NotableSource,
    OverviewData,
    Result,
    ResultGroup,
    RungCount,
)
from devtools.overview_media import Film, Preview
from devtools.reader_documents import ReaderDocument
from devtools.site_kit import REPO_URL, SITE_NAME, TEMPLATES, Page

TEMPLATE = TEMPLATES / "overview-article.md"
REPO = Path(__file__).resolve().parents[2]

#: The page's own classic scripts, inlined in this order after the math runtime. The
#: forwarder goes first, so an old deep link into the explainer leaves before anything
#: else runs.
SCRIPTS_DIR = Path(__file__).with_name("overview")
FORWARD_SCRIPT = SCRIPTS_DIR / "forward.js"
TABLE_SCRIPT = SCRIPTS_DIR / "table.js"
POPOVER_SCRIPT = SCRIPTS_DIR / "popover.js"
SCRIPTS: tuple[Path, ...] = (FORWARD_SCRIPT, TABLE_SCRIPT, POPOVER_SCRIPT)

#: The reader documents whose opening sections the document cards' popovers show,
#: rendered at build time. Declared as the files and trees they live in, because which
#: documents the map lists is decided at render time; `test_overview_page` holds every
#: document `reader_documents()` returns to one of these.
READER_SOURCES: tuple[Path, ...] = (
    REPO / "README.md",
    REPO / "TUTORIAL.md",
    REPO / "SYNOPSIS.md",
    REPO / "epistemics.md",
    REPO / "conventions.md",
    REPO / "packing" / "frontier" / "RESULTS.md",
    REPO / "packing" / "frontier" / "STATUS.md",
    REPO / "docs" / "project" / "research",
)

RENDER_INPUTS: tuple[Path, ...] = tuple(
    dict.fromkeys(
        (
            Path(__file__),
            TEMPLATE,
            *SCRIPTS,
            Path(render_recent_results.__file__),
            *READER_SOURCES,
            *overview_data.RENDER_INPUTS,
            *overview_media.RENDER_INPUTS,
            *reader_documents.RENDER_INPUTS,
        )
    )
)

DESCRIPTION = (
    "The square packing problem, and every current result on it, by this project and "
    "by others, with how far each has been verified."
)

#: The page's sections, in order: each `h2` in the template and the id it is given.
#: The ids are stable anchors other pages link to (the explainer's edition notice links
#: `#recent-results`), and none of them is an id on the explainer.
SECTIONS: tuple[tuple[str, str], ...] = (
    ("problem", "The Square Packing Problem"),
    ("recent-results", "Recent Results"),
    ("verification", "Verification at a Glance"),
    ("atlas", "The Atlas and Its Film"),
    ("results", "Results"),
    ("read-further", "Read Further"),
    ("other-projects", "Other Square Packing Projects"),
)

#: The id of the results table, which the result cards and the filters point at.
RESULTS_TABLE_ID = "results-table"
#: The data island listing every link on the page that names the default branch rather
#: than the build commit (the document cards), for the published-site ref rule.
DEFAULT_BRANCH_LINKS_ID = "site-default-branch-links"

#: The three classification axes, in the order the page shows them, with the words a
#: reader needs before the counts. The rung definitions themselves come from the record.
AXES: tuple[tuple[str, str, str], ...] = (
    ("V", "Verification", "How far the proof itself has been checked."),
    ("C", "Confirmation", "What this repository has itself replayed or read."),
    ("S", "Significance", "How much the result moves the problem."),
)

NOVELTY_LABELS = {
    "common-knowledge": "common knowledge",
    "previously-published": "previously published",
    "apparently-novel": "apparently novel",
    "confirmed-novel": "confirmed novel",
}

KIND_LABELS = {
    "website": "Website",
    "catalogue": "Catalogue",
    "release": "Release",
    "repository": "Repository",
}

READER_GROUPS: tuple[tuple[str, str], ...] = (
    ("start", "Start here"),
    ("results", "Results and policy"),
    ("reports", "Research reports"),
)

#: An exact form longer than this is shown on a card by its decimal, with the exact form
#: in the table's expanded row: a card is a third of the page wide on a desktop and the
#: whole phone, and a long radical does not wrap.
EXACT_ON_CARD = 24

RELATION_TEX = {"≥": r"\ge", ">": ">", "≤": r"\le", "<": "<", "=": "="}


@dataclass(frozen=True)
class PageCard:
    """A card for another page of the site, previewed in a same-origin frame."""

    title: str
    href: str
    summary: str


#: The site's other pages, in the navigation bar's order. What each page covers is
#: interface text, not a finding: no bound is stated here.
PAGE_CARDS: tuple[PageCard, ...] = (
    PageCard(
        "Frontier atlas",
        "frontier.html",
        "Every case from one to 324, with its best known packing, its reported and "
        "verified bounds and the records behind them.",
    ),
    PageCard(
        "Explainer",
        "explainer.html",
        "An illustrated, interactive walk through the certificates behind this "
        "project's lower bounds for eleven squares.",
    ),
    PageCard(
        "Tutorial",
        "tutorial.html",
        "How the problem is posed, how bounds are proved and checked, and how to run "
        "the tools in this repository.",
    ),
    PageCard(
        "Visualizer",
        "workbench/",
        "An interactive workbench for the known-best packings: browse, animate and "
        "compare them case by case.",
    ),
)


@dataclass(frozen=True)
class Media:
    """What `overview_media` provides the page: the previews, the film and the hero."""

    previews: tuple[Preview, ...]
    film: Film
    hero: str


def media() -> Media:
    return Media(
        previews=overview_media.atlas_previews(),
        film=overview_media.atlas_film(),
        hero=overview_media.hero_svg(),
    )


def pages() -> Iterable[Page]:
    yield Page(
        key="overview",
        path="index.html",
        title=SITE_NAME,
        description=DESCRIPTION,
        html=render(overview_data.load(), media(), reader_documents.reader_documents()),
        scripts=SCRIPTS,
    )


# ── Mathematics ─────────────────────────────────────────────────────────────────────


def math_html(tex: str, *, display: bool = False) -> str:
    """One formula in kpress's markup, as its Markdown renderer would write `$tex$`.

    The TeX source is what `overview/site-math.js` typesets through the explainer's
    runtime; the MathML beside it is the accessible reading and the no-JavaScript
    fallback. The one-mu spacing after a one-letter function name is the explainer's.
    """
    source = render_explainer.kerned_math(tex.strip())
    tag = "div" if display else "span"
    kind = "display" if display else "inline"
    open_delim, close_delim = (r"\[", r"\]") if display else (r"\(", r"\)")
    mathml = convert_latex_math(source, display="block" if display else "inline")
    return (
        f'<{tag} class="kpress-math kpress-math-{kind}" data-kpress-math="{kind}" '
        f'data-kpress-math-renderer="katex">'
        f'<{tag} class="kpress-math-render" aria-hidden="true">'
        f"{open_delim}{escape(source)}{close_delim}</{tag}>"
        f'<{tag} class="kpress-math-semantic">{mathml}</{tag}></{tag}>'
    )


_TEX_SYMBOLS = (
    ("≥", r"\ge "),
    ("≤", r"\le "),
    ("≠", r"\ne "),
    ("≈", r"\approx "),
    ("…", r"\ldots "),
    ("−", "-"),
    ("·", r"\cdot "),
    ("×", r"\times "),
    ("→", r"\to "),
    ("²", "^2"),
    ("³", "^3"),
    ("⌈", r"\lceil "),
    ("⌉", r"\rceil "),
    ("⌊", r"\lfloor "),
    ("⌋", r"\rfloor "),
    ("ρ", r"\rho "),
)
_FUNCTIONS = re.compile(r"(?<![A-Za-z\\])(min|max|log|sin|cos)(?=\()")
_GREEK_WORDS = re.compile(r"(?<![A-Za-z\\])(rho|theta|phi|alpha|beta|delta)(?![A-Za-z])")
_SUBSCRIPT_WORD = re.compile(r"_([A-Za-z]{2,})")
_ROOT_TOKEN = re.compile(r"√([0-9A-Za-z.]+)")
#: A register code span that names something rather than states it: a result, evidence
#: or session id, a rung. It stays code, as the math migration's rule has it.
_IDENTIFIER = re.compile(r"^(?:[A-Z]{1,3}-[\w.-]+|[VCS]\d|[a-z_]+\.[a-z_.]+)$")


def _root_groups(text: str) -> str:
    """`√(…)` with balanced parentheses as `\\sqrt{…}`."""
    out: list[str] = []
    index = 0
    while index < len(text):
        if text.startswith("√(", index):
            depth, cursor = 0, index + 1
            while cursor < len(text):
                if text[cursor] == "(":
                    depth += 1
                elif text[cursor] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                cursor += 1
            out.append(r"\sqrt{" + _root_groups(text[index + 2 : cursor]) + "}")
            index = cursor + 1
        else:
            out.append(text[index])
            index += 1
    return "".join(out)


def ascii_tex(text: str) -> str:
    """The register's plain mathematics (`s(11) ≥ 2 + 4/√5`) as TeX.

    The register and its headlines write mathematics as Unicode text in code spans;
    Phase 3 of the plan moves the prose to LaTeX, and until then the page converts the
    few symbols the register uses rather than showing them as code.
    """
    tex = _root_groups(text)
    tex = _ROOT_TOKEN.sub(r"\\sqrt{\1}", tex)
    for symbol, replacement in _TEX_SYMBOLS:
        tex = tex.replace(symbol, replacement)
    tex = _FUNCTIONS.sub(r"\\\1", tex)
    tex = _GREEK_WORDS.sub(r"\\\1", tex)
    tex = _SUBSCRIPT_WORD.sub(r"_{\\mathrm{\1}}", tex)
    return re.sub(r" +", " ", tex).strip()


_INLINE = re.compile(r"(?<!\\)\$(?P<tex>[^$\n]+?)(?<!\\)\$|`(?P<code>[^`\n]+)`")


def inline_html(text: str) -> str:
    """A line of record text as HTML: `$…$` and math-like code spans set as math."""
    out: list[str] = []
    cursor = 0
    for match in _INLINE.finditer(text):
        out.append(escape(text[cursor : match.start()]))
        cursor = match.end()
        if match["tex"] is not None:
            out.append(math_html(match["tex"]))
            continue
        code = match["code"]
        if _IDENTIFIER.match(code):
            out.append(f"<code>{escape(code)}</code>")
            continue
        try:
            out.append(math_html(ascii_tex(code)))
        except Exception:  # noqa: BLE001 -- latex2mathml raises bare parse errors
            out.append(f"<code>{escape(code)}</code>")
    out.append(escape(text[cursor:]))
    return "".join(out)


def plain_text(text: str) -> str:
    """Record text with its math markers dropped, for a sort key or an attribute."""
    return re.sub(r"[`$]", "", text)


def decimal_tex(decimal: str) -> str:
    return decimal.replace("…", r"\ldots")


def bound_tex(bound: Bound) -> str:
    """A bound as a card shows it: the exact form when it is short, and the decimal."""
    relation = RELATION_TEX.get(bound.relation, bound.relation)
    if len(bound.exact) > EXACT_ON_CARD:
        return f"s({bound.n}) {relation} {decimal_tex(bound.decimal)}"
    if bound.decimal and bound.decimal != bound.exact:
        return f"{bound.tex} = {decimal_tex(bound.decimal)}"
    return bound.tex


# ── Small components ────────────────────────────────────────────────────────────────


def goes(href: str) -> str:
    """Where a link takes the reader, for the card's hover icon: down, page or out."""
    if href.startswith("#"):
        return "down"
    if urlsplit(href).scheme in {"http", "https"}:
        return "out"
    return "page"


def chip(label: str, *, title: str | None = None, tone: str | None = None) -> str:
    """One badge in the site's one chip component."""
    attributes = ['class="site-chip"']
    if tone:
        attributes.append(f'data-tone="{escape(tone)}"')
    if title:
        attributes.append(f'title="{escape(title)}"')
    return f"<span {' '.join(attributes)}>{escape(label)}</span>"


def rung_chip(axis: str, rung: int, *, title: str | None = None) -> str:
    """A rung badge: the chip, coloured by its axis and darkened by its rung."""
    label = f"{axis}{rung}"
    tooltip = f' title="{escape(title)}"' if title else ""
    return (
        f'<span class="site-chip site-rung" data-axis="{axis.lower()}" '
        f'data-rung="{rung}"{tooltip}>{label}</span>'
    )


def star_chip(title: str) -> str:
    return f'<span class="site-chip site-chip-star" title="{escape(title)}">recent</span>'


def link(item: Link) -> str:
    return f'<a href="{escape(item.url)}">{escape(item.label)}</a>'


def links(items: Sequence[Link], *, separator: str = " · ") -> str:
    return separator.join(link(item) for item in items)


def card_link(href: str, content: str, *, popover: str | None = None) -> str:
    """The card's one link, stretched over the whole card by `site.css`."""
    attributes = [
        'class="site-card-link"',
        f'href="{escape(href)}"',
        f'data-goes="{goes(href)}"',
    ]
    if popover:
        attributes.append(f'data-popover="{popover}"')
    return f"<a {' '.join(attributes)}>{content}</a>"


def display_date(iso: str | None) -> str:
    if not iso:
        return ""
    day = date.fromisoformat(iso)
    return f"{day.day} {day:%B %Y}"


def rung_number(label: str) -> int:
    return int(label.lstrip("VCS"))


# ── Result cards and the results table ──────────────────────────────────────────────


def result_anchor(result: Result) -> str:
    return f"result-{result.id.lower()}"


def rung_titles(counts: Sequence[RungCount]) -> dict[str, str]:
    """Each rung's tooltip, `V4: Machine-verified`, from the record's definitions."""
    return {
        f"{count.axis}{count.rung}": f"{count.axis}{count.rung}: {count.label}"
        for count in counts
    }


def result_rungs(result: Result, titles: dict[str, str]) -> str:
    rungs = (
        ("V", rung_number(result.verification)),
        ("C", rung_number(result.confirmation)),
        ("S", result.significance),
    )
    return "".join(
        rung_chip(axis, rung, title=titles.get(f"{axis}{rung}")) for axis, rung in rungs
    )


def standing_chips(result: Result) -> list[str]:
    chips: list[str] = []
    if result.standing and result.standing != render_recent_results.NOT_A_BOUND:
        tone = "muted" if result.standing == render_recent_results.SUPERSEDED else None
        chips.append(chip(result.standing, tone=tone))
    if result.reported and "reported" not in result.standing:
        chips.append(chip("reported", title="Reported by its source; not yet verified here"))
    if result.exact_value:
        chips.append(chip("exact value", title="A new exact value, not only a bound"))
    return chips


def _headline_rest(result: Result) -> str:
    """What a headline says beyond the bound a card already sets as its title."""
    match = re.match(r"^`[^`]+`[,;]?\s*", result.headline)
    if match is None:
        return result.headline
    return result.headline[match.end() :]


def result_card(result: Result, titles: dict[str, str]) -> str:
    if result.bound is not None:
        title = math_html(bound_tex(result.bound))
        rest = _headline_rest(result)
    else:
        title = inline_html(result.headline)
        rest = ""
    when = result.established if result.ours else result.published
    meta = [f'<span class="site-card-id">{escape(result.id)}</span>']
    meta.append(f"{math_html('n')} = {escape(result.cases)}")
    if when:
        meta.append(escape(display_date(when)))
    parts = [
        f'<article class="site-card site-card-result" data-source='
        f'"{"ours" if result.ours else "others"}">',
        '<div class="site-card-head">'
        f'<p class="site-card-meta">{" · ".join(meta)}</p>'
        f'<p class="site-chips">{result_rungs(result, titles)}</p></div>',
        '<h3 class="site-card-title">'
        f"{card_link('#' + result_anchor(result), title, popover='result')}</h3>",
    ]
    if rest:
        parts.append(f'<p class="site-card-summary">{inline_html(rest)}</p>')
    credit = escape(result.credit)
    if result.relation:
        credit += f' <span class="site-card-relation">({escape(result.relation)})</span>'
    parts.append(f'<p class="site-card-credit">{credit}</p>')
    if result.ai_assistance:
        parts.append(
            '<p class="site-card-note">AI assistance, in the source’s words: '
            f"{escape(result.ai_assistance)}</p>"
        )
    if result.superseded_by:
        parts.append(
            f'<p class="site-card-note">Superseded; the case is now held by '
            f"{inline_html(result.superseded_by)}.</p>"
        )
    chips = standing_chips(result)
    if chips:
        parts.append(f'<p class="site-chips site-card-foot">{"".join(chips)}</p>')
    parts.append("</article>")
    return "\n".join(parts)


def result_cards(results: Sequence[Result], titles: dict[str, str]) -> str:
    cards = "\n".join(result_card(result, titles) for result in results)
    return f'<div class="site-cards site-wide">\n{cards}\n</div>'


def n_bounds(result: Result) -> tuple[int, int]:
    return min(result.n_values), max(result.n_values)


def row_flags(result: Result) -> str:
    flags = ["ours" if result.ours else "others"]
    if result.recent:
        flags.append("recent")
    if result.reported:
        flags.append("reported")
    if result.exact_value:
        flags.append("exact")
    if result.standing.startswith(render_recent_results.HOLDS):
        flags.append("holds")
    if result.standing.startswith(render_recent_results.SUPERSEDED):
        flags.append("superseded")
    return " ".join(flags)


def details_body(result: Result) -> str:
    """The expanded row: the full claim, how it composes, and what would raise it."""
    parts = [f"<p><strong>Claim.</strong> {inline_html(result.claim)}</p>"]
    if result.bound is not None and len(result.bound.exact) > EXACT_ON_CARD:
        parts.append(f"<p><strong>Exact form.</strong> {math_html(result.bound.tex)}</p>")
    standing = result.standing
    if standing and standing != render_recent_results.NOT_A_BOUND:
        text = escape(standing)
        if result.superseded_by:
            text += f"; the case is now held by {inline_html(result.superseded_by)}"
        parts.append(f"<p><strong>Standing.</strong> {text}.</p>")
    if result.composition:
        parts.append(f"<p><strong>Composition.</strong> {inline_html(result.composition)}</p>")
    if result.next_rung:
        parts.append(f"<p><strong>Next rung.</strong> {inline_html(result.next_rung)}</p>")
    if result.records:
        parts.append(f"<p><strong>Records.</strong> {links(result.records)}</p>")
    if result.artifacts:
        parts.append(f"<p><strong>Artifacts.</strong> {links(result.artifacts)}</p>")
    return f'<div class="site-details-body">{"".join(parts)}</div>'


def result_row(result: Result, titles: dict[str, str]) -> str:
    low, high = n_bounds(result)
    verification = rung_number(result.verification)
    confirmation = rung_number(result.confirmation)
    when = result.established if result.ours else result.published
    when_label = "established" if result.ours else "published"
    credit = escape(result.credit)
    if result.ai_assistance:
        credit += (
            f'<span class="site-cell-note">AI assistance, in the source’s words: '
            f"{escape(result.ai_assistance)}</span>"
        )
    recent = star_chip("Recent: dated on or after the recent-results cut") if result.recent else ""
    novelty = NOVELTY_LABELS.get(result.novelty, result.novelty)
    cells = [
        f'<td data-value="{escape(result.id[2:])}"><a class="site-row-id" '
        f'href="#{result_anchor(result)}">{escape(result.id)}</a>{recent}</td>',
        f'<td data-value="{low}">{escape(result.cases)}</td>',
        f'<td class="site-col-result" data-value="{escape(plain_text(result.headline))}">'
        f"<details><summary>{inline_html(result.headline)}</summary>"
        f"{details_body(result)}</details></td>",
        f'<td data-value="{escape(result.credit)}">{credit}</td>',
        f'<td class="site-col-rung" data-value="{verification}">'
        f"{rung_chip('V', verification, title=titles.get(f'V{verification}'))}</td>",
        f'<td class="site-col-rung" data-value="{confirmation}">'
        f"{rung_chip('C', confirmation, title=titles.get(f'C{confirmation}'))}</td>",
        f'<td class="site-col-rung" data-value="{result.significance}">'
        f"{rung_chip('S', result.significance, title=titles.get(f'S{result.significance}'))}"
        "</td>",
        f'<td data-value="{escape(novelty)}">{chip(novelty, tone="muted")}</td>',
        f'<td class="site-col-date" data-value="{escape(when or "")}">'
        f"{escape(when or '—')}"
        f'<span class="site-cell-note">{when_label}</span></td>',
        f'<td class="site-col-date" data-value="{escape(result.registered)}">'
        f"{escape(result.registered)}</td>",
        f'<td class="site-col-records">{links(result.records, separator="<br>")}</td>',
    ]
    attributes = (
        f'id="{result_anchor(result)}" data-source="{"ours" if result.ours else "others"}" '
        f'data-v="{verification}" data-c="{confirmation}" data-s="{result.significance}" '
        f'data-n-min="{low}" data-n-max="{high}" data-flags="{row_flags(result)}"'
    )
    return f"<tr {attributes}>{''.join(cells)}</tr>"


TABLE_HEADER = (
    ("number", "site-col-id", "ID"),
    ("number", "site-col-n", "{n}"),
    ("text", "site-col-result", "Result"),
    ("text", "site-col-credit", "Credit"),
    ("number", "site-col-rung", "V"),
    ("number", "site-col-rung", "C"),
    ("number", "site-col-rung", "S"),
    ("text", "site-col-novelty", "Novelty"),
    ("text", "site-col-date", "Established or published"),
    ("text", "site-col-date", "Registered"),
    ("", "site-col-records", "Records"),
)


def table_filters() -> str:
    """The filters above the table, hidden until `table.js` makes them work."""
    c_options = "".join(f'<option value="{rung}">C{rung}</option>' for rung in range(6))
    return (
        f'<div class="site-table-filters site-wide" data-filters-for="{RESULTS_TABLE_ID}" '
        'hidden>'
        '<label>Source <select data-filter="source"><option value="">All</option>'
        '<option value="ours">This project</option><option value="others">Others</option>'
        "</select></label>"
        f'<label>Confirmation <select data-filter="c"><option value="">Any</option>'
        f"{c_options}</select></label>"
        f"<label>{math_html('n')} from "
        '<input type="number" min="1" inputmode="numeric" data-filter-min="n-max"></label>'
        '<label>to <input type="number" min="1" inputmode="numeric" '
        'data-filter-max="n-min"></label>'
        '<label><input type="checkbox" data-filter-flag="recent"> Recent only</label>'
        '<output class="site-table-count" data-filter-count></output>'
        "</div>"
    )


def results_table(groups: Sequence[ResultGroup], titles: dict[str, str]) -> str:
    header = "".join(
        f'<th scope="col" class="{css}"'
        + (f' data-sort="{kind}"' if kind else "")
        + f">{math_html('n') if label == '{n}' else escape(label)}</th>"
        for kind, css, label in TABLE_HEADER
    )
    bodies = []
    for group in groups:
        rows = "\n".join(result_row(result, titles) for result in group.results)
        bodies.append(
            f'<tbody data-group="{escape(group.key)}">'
            f'<tr class="site-table-group" data-site-table-group>'
            f'<th scope="colgroup" colspan="{len(TABLE_HEADER)}">{escape(group.title)}</th>'
            f"</tr>\n{rows}\n</tbody>"
        )
    return (
        f"{table_filters()}\n"
        '<div class="kpress-table-wrap site-table-wrap site-wide" '
        'data-kpress-table-scale="wide">'
        f'<table class="kpress-table site-table" data-site-table id="{RESULTS_TABLE_ID}">'
        f"<thead><tr>{header}</tr></thead>\n" + "\n".join(bodies) + "</table></div>"
    )


# ── Verification at a glance ────────────────────────────────────────────────────────


def axis_card(axis: str, name: str, summary: str, counts: Sequence[RungCount]) -> str:
    rows = "".join(
        f"<tr><th scope=\"row\">{rung_chip(axis, count.rung, title=count.definition)}"
        f"<span>{escape(count.label)}</span></th>"
        f'<td data-count="{count.ours}">{count.ours}</td>'
        f'<td data-count="{count.others}">{count.others}</td></tr>'
        for count in sorted(counts, key=lambda count: count.rung, reverse=True)
    )
    return (
        f'<article class="site-card site-card-axis" data-axis="{axis.lower()}">'
        f'<h3 class="site-card-title">{card_link("#results", escape(name))}</h3>'
        f'<p class="site-card-summary">{escape(summary)}</p>'
        '<table class="site-rung-table"><thead><tr><th scope="col">Rung</th>'
        '<th scope="col">This project</th><th scope="col">Others</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></article>"
    )


def atlas_card(atlas: AtlasTotals) -> str:
    figures = (
        (atlas.proved, "proved"),
        (atlas.open, "open"),
        (atlas.recent_verified_lower, "with a recent verified lower bound"),
    )
    items = "".join(
        f'<li><span class="site-figure">{value}</span> {escape(label)}</li>'
        for value, label in figures
    )
    return (
        '<article class="site-card site-card-atlas">'
        '<h3 class="site-card-title">'
        f"{card_link('frontier.html', f'The atlas of {atlas.cases} cases', popover='page')}"
        "</h3>"
        '<p class="site-card-summary">How many of the atlas’s cases are settled, and how '
        "many carry a verified lower bound dated in the recent-results window.</p>"
        f'<ul class="site-figures">{items}</ul></article>'
    )


def verification_cards(counts: Sequence[RungCount], atlas: AtlasTotals) -> str:
    cards = [
        axis_card(axis, name, summary, [c for c in counts if c.axis == axis])
        for axis, name, summary in AXES
    ]
    return (
        f'<div class="site-cards site-cards-axes site-wide">{"".join(cards)}</div>\n'
        f'<div class="site-cards site-cards-single site-wide">{atlas_card(atlas)}</div>'
    )


# ── The atlas and its film ──────────────────────────────────────────────────────────


def preview_card(preview: Preview) -> str:
    caption = (
        f"{escape(preview.alt)}"
        f'<span class="site-card-note">PDF, {escape(preview.pages)}, '
        f"{escape(preview.size)}; edition {escape(preview.edition)}</span>"
    )
    return (
        '<figure class="site-card site-card-preview">'
        f'<img src="{escape(preview.image)}" width="{preview.width}" '
        f'height="{preview.height}" alt="{escape(preview.alt)}" loading="lazy" '
        'decoding="async">'
        f'<figcaption>{card_link(preview.pdf, caption)}</figcaption></figure>'
    )


def film_figure(film: Film) -> str:
    return (
        '<figure class="site-film site-wide">'
        f'<video controls preload="none" playsinline poster="{escape(film.poster)}" '
        f'width="{film.width}" height="{film.height}">'
        f'<source src="{escape(film.src)}" type="{escape(film.type)}"></video>'
        '<figcaption>The ascent from one square to 324, one case at a time: '
        f"{escape(film.duration)}, {escape(film.size)}, edition {escape(film.edition)}, "
        f"as released in {escape(film.release)}. "
        f'<a href="{escape(film.src)}">Open the MP4</a>.</figcaption></figure>'
    )


def atlas_media(previews: Sequence[Preview], film: Film) -> str:
    """The previews and the film, inside the element the same-origin media rule reads.

    `data-site-media` marks where every `href` and `src` must be site-relative: the
    published-site media check applies the rule inside it and nowhere else, since the
    record links elsewhere on the page are permalinks by design.
    """
    cards = "".join(preview_card(preview) for preview in previews)
    return (
        '<div class="site-media site-wide" data-site-media>'
        f'<div class="site-cards site-cards-media">{cards}</div>\n'
        f"{film_figure(film)}</div>"
    )


# ── Read further ────────────────────────────────────────────────────────────────────


def page_card(card: PageCard, explainer: ExplainerEdition) -> str:
    parts = [
        '<article class="site-card site-card-page">',
        f'<h3 class="site-card-title">{card_link(card.href, escape(card.title), popover="page")}'
        "</h3>",
        f'<p class="site-card-summary">{escape(card.summary)}</p>',
    ]
    if card.href == "explainer.html":
        parts.append(
            f'<p class="site-card-note">The {escape(explainer.edition)} proof edition, '
            f"first published {escape(display_date(explainer.edition_first_published))}; "
            f"the page first appeared {escape(display_date(explainer.first_published))}.</p>"
        )
        tone = None if explainer.is_current else "muted"
        label = "current" if explainer.is_current else "earlier edition"
        parts.append(
            f'<p class="site-card-note site-edition-note">{chip(label, tone=tone)} '
            f"{inline_html(explainer.note)}</p>"
        )
    parts.append("</article>")
    return "".join(parts)


_OPENING_LIMIT = 2400


def opening_markdown(text: str) -> str:
    """A document's opening section: what follows its title, up to its first `##`."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        text = text[end + 5 :] if end != -1 else text
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = text.splitlines()
    body: list[str] = []
    in_fence = False
    for line in lines:
        if line.startswith(("```", "~~~")):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{1,2}\s", line):
            if line.startswith("# ") and not body:
                continue
            if body and line.startswith("## "):
                break
            continue
        body.append(line)
    opening = "\n".join(body).strip()
    if len(opening) > _OPENING_LIMIT:
        cut = opening.rfind("\n\n", 0, _OPENING_LIMIT)
        opening = opening[: cut if cut > 0 else _OPENING_LIMIT].rstrip()
    return opening


_ANCHOR_OPEN = re.compile(r"<a\b[^>]*>")
_IMAGE = re.compile(r"<img\b[^>]*>")
_ID_ATTRIBUTE = re.compile(r'\s(?:id|name)="[^"]*"')


def opening_html(path: str) -> str:
    """The opening section of a reader document, rendered by kpress for its popover.

    Links and images are dropped (the popover is a preview; its button opens the whole
    document on GitHub) and so are ids, which would enter the page's id space.
    """
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    source = (REPO / path).read_text(encoding="utf-8")
    document = parse_markdown(
        render_explainer.kerned_math_spans(opening_markdown(source)),
        title=path,
        trust_mode="sanitized",
        math="auto",
    )
    errors = [d for d in document.diagnostics if d.severity == "error"]
    if errors:
        raise SystemExit(f"{path}: its opening section did not render: {errors[0].message}")
    html = _ANCHOR_OPEN.sub("", document.html).replace("</a>", "")
    html = _IMAGE.sub("", html)
    return _ID_ATTRIBUTE.sub("", html)


def document_card(document: ReaderDocument) -> str:
    meta: list[str] = [f"<code>{escape(document.path)}</code>"]
    if document.date:
        meta.append(escape(display_date(document.date)))
    chips = chip("dated record", tone="muted", title="Kept as a record of its date") if (
        document.dated
    ) else ""
    external = goes(document.url) == "out"
    preview = (
        f'<template class="site-card-preview">{opening_html(document.path)}</template>'
        if external
        else ""
    )
    popover = "document" if external else "page"
    return (
        f'<article class="site-card site-card-document" data-group="{document.group}">'
        f'<p class="site-card-meta">{" · ".join(meta)} {chips}</p>'
        '<h3 class="site-card-title">'
        f"{card_link(document.url, escape(document.title), popover=popover)}</h3>"
        f'<p class="site-card-summary">{escape(document.summary)}</p>'
        f"{preview}</article>"
    )


def read_further(explainer: ExplainerEdition, documents: Sequence[ReaderDocument]) -> str:
    page_hrefs = {card.href for card in PAGE_CARDS}
    parts = [
        '<h3 class="site-group-title">On this site</h3>',
        '<div class="site-cards site-wide">'
        + "".join(page_card(card, explainer) for card in PAGE_CARDS)
        + "</div>",
    ]
    for key, title in READER_GROUPS:
        group = [d for d in documents if d.group == key and d.url not in page_hrefs]
        if not group:
            continue
        parts.append(f'<h3 class="site-group-title">{escape(title)}</h3>')
        parts.append(
            '<div class="site-cards site-wide">'
            + "".join(document_card(document) for document in group)
            + "</div>"
        )
    return "\n".join(parts)


# ── Other square packing projects ───────────────────────────────────────────────────


def source_card(source: NotableSource) -> str:
    parts = [
        f'<article class="site-card site-card-source" data-kind="{source.kind}">',
        f'<p class="site-card-meta">{escape(KIND_LABELS.get(source.kind, source.kind))}</p>',
        f'<h3 class="site-card-title">{card_link(source.url, escape(source.title))}</h3>',
        f'<p class="site-card-credit">{escape(source.credit)}</p>',
        f'<p class="site-card-summary">{escape(source.summary)}</p>',
    ]
    if source.releases:
        items = "".join(
            f'<li><a href="{escape(release.url)}">{escape(release.title)}</a>, reviewed '
            f"{escape(release.reviewed)}"
            + (
                " " + chip("superseded", tone="muted", title="Covered by a later release")
                if release.superseded
                else ""
            )
            + "</li>"
            for release in source.releases
        )
        parts.append(f'<ul class="site-card-list">{items}</ul>')
    extras: list[str] = []
    if source.archive is not None:
        extras.append(f'<a href="{escape(source.archive.url)}">retained copy</a>')
    if source.cases:
        extras.append("cited by " + links(source.cases, separator=", "))
    if extras:
        parts.append(f'<p class="site-card-note">{"; ".join(extras)}</p>')
    parts.append("</article>")
    return "".join(parts)


def project_cards(sources: Sequence[NotableSource]) -> str:
    groups = (
        ("Websites and catalogues", ("website", "catalogue")),
        ("Repositories and releases", ("repository", "release")),
    )
    parts: list[str] = []
    for title, kinds in groups:
        members = [source for source in sources if source.kind in kinds]
        if not members:
            continue
        parts.append(f'<h3 class="site-group-title">{escape(title)}</h3>')
        parts.append(
            '<div class="site-cards site-wide">'
            + "".join(source_card(source) for source in members)
            + "</div>"
        )
    return "\n".join(parts)


# ── The page ────────────────────────────────────────────────────────────────────────


def default_branch_links(documents: Sequence[ReaderDocument]) -> str:
    """The data island naming every link that names the default branch, not the commit."""
    urls = sorted({d.url for d in documents if goes(d.url) == "out"})
    return (
        f'<script type="application/json" id="{DEFAULT_BRANCH_LINKS_ID}">'
        f"{json.dumps(urls).replace('</', '<\\/')}</script>"
    )


def hero(svg: str) -> str:
    return (
        '<figure class="site-hero" role="img" aria-label="The best known packing of '
        f'fifty-three unit squares">{svg}</figure>'
    )


def inline_values(data: OverviewData, documents: Sequence[ReaderDocument]) -> dict[str, str]:
    """The facts the template's prose names, filled before the Markdown is parsed."""
    epistemics = next((d.url for d in documents if d.path == "epistemics.md"), None)
    if epistemics is None:
        raise SystemExit("the document map lists no epistemics.md; the overview links it")
    total = sum(len(group.results) for group in data.groups)
    return {
        "RECENT_SINCE": display_date(render_recent_results.RECENT_SINCE.isoformat()),
        "RECENT_OURS": str(len(data.recent_ours)),
        "RECENT_OTHERS": str(len(data.recent_others)),
        "RESULT_COUNT": str(total),
        "ATLAS_CASES": str(data.atlas.cases),
        "EPISTEMICS_URL": epistemics,
    }


def block_values(
    data: OverviewData, media_: Media, documents: Sequence[ReaderDocument]
) -> dict[str, str]:
    """The generated blocks, each standing alone in a paragraph of the template."""
    titles = rung_titles(data.rung_counts)
    return {
        "HERO": hero(media_.hero),
        "RECENT_OURS_CARDS": result_cards(data.recent_ours, titles),
        "RECENT_OTHERS_CARDS": result_cards(data.recent_others, titles),
        "VERIFICATION_CARDS": verification_cards(data.rung_counts, data.atlas),
        "ATLAS_MEDIA": atlas_media(media_.previews, media_.film),
        "RESULTS_TABLE": results_table(data.groups, titles),
        "READ_FURTHER": read_further(data.explainer, documents),
        "PROJECT_CARDS": project_cards(data.sources),
        "DEFAULT_BRANCH_LINKS": default_branch_links(documents),
    }


_PLACEHOLDER = re.compile(r"\{\{([A-Z_]+)\}\}")


def template_text(template: str) -> str:
    """The template without its leading comment, which is for its editors."""
    return re.sub(r"\A\s*<!--.*?-->\s*", "", template, flags=re.DOTALL)


def markdown_html(source: str, *, where: str) -> str:
    """The template through kpress, as `render_overview.markdown_html` renders a page."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    document = parse_markdown(
        render_explainer.kerned_math_spans(source),
        title=SITE_NAME,
        trust_mode="trusted",
        math="auto",
    )
    for diagnostic in document.diagnostics:
        print(f"{where}: {diagnostic.severity}: {diagnostic.message}", file=sys.stderr)
    if any(d.severity == "error" for d in document.diagnostics):
        raise SystemExit(f"{where} did not render cleanly; refusing to write the page")
    return document.html


def _sections(html: str) -> Iterator[tuple[str, str]]:
    for match in re.finditer(r'<h2 id="([^"]*)">(.*?)</h2>', html):
        yield match[1], match[2]


def with_section_ids(html: str) -> str:
    """Give each `h2` its id from `SECTIONS`, refusing a template whose headings differ."""
    found = [heading for _, heading in _sections(html)]
    expected = [heading for _, heading in SECTIONS]
    if found != expected:
        raise SystemExit(f"{TEMPLATE.name}: sections {found} are not the page's {expected}")
    for (slug, heading), (anchor, _) in zip(_sections(html), SECTIONS, strict=True):
        html = html.replace(f'<h2 id="{slug}">{heading}</h2>', f'<h2 id="{anchor}">{heading}</h2>')
    return html


def render(
    data: OverviewData,
    media_: Media,
    documents: Sequence[ReaderDocument],
    *,
    template: str | None = None,
) -> str:
    """The overview's body HTML, from the record and nothing else."""
    source = template_text(template if template is not None else TEMPLATE.read_text("utf-8"))
    inline = inline_values(data, documents)
    blocks = block_values(data, media_, documents)
    names = set(_PLACEHOLDER.findall(source))
    unknown = names - inline.keys() - blocks.keys()
    if unknown:
        raise SystemExit(f"{TEMPLATE.name}: placeholders with no value: {sorted(unknown)}")
    missing = blocks.keys() - names
    if missing:
        raise SystemExit(f"{TEMPLATE.name}: the page's blocks {sorted(missing)} have no place")
    for key, value in inline.items():
        source = source.replace(f"{{{{{key}}}}}", value)
    html = markdown_html(source, where=TEMPLATE.name)
    for key, value in blocks.items():
        paragraph = f"<p>{{{{{key}}}}}</p>"
        if html.count(paragraph) != 1:
            raise SystemExit(f"{TEMPLATE.name}: {{{{{key}}}}} must stand alone in a paragraph")
        html = html.replace(paragraph, value)
    left = _PLACEHOLDER.findall(html)
    if left:
        raise SystemExit(f"{TEMPLATE.name}: placeholders left in the page: {sorted(left)}")
    return with_section_ids(html)
