"""The overview page's generated blocks, as HTML, from `devtools.overview_data`.

The page's prose lives in `templates/overview-article.md`; every block that states a
fact is built here and substituted into it, so a bound or a count never appears in the
template as a literal. Values are set as `$…$` inline math for KaTeX, and every table
works without scripts: rows are all present, a row's detail opens in its popover from
the native trigger in the row (`row_detail`), and `overview/table.js` adds sorting and
filters on top while `overview/row-popover.js` makes the whole row the control.
"""

from __future__ import annotations

import base64
import html
import re
import textwrap
from collections import Counter
from collections.abc import Iterable, Sequence
from datetime import date, timedelta
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, NamedTuple, get_args
from urllib.parse import urlsplit

from devtools import repo_links
from devtools.build_bound_citations import RECENT_SINCE
from devtools.check_results import RESULTS as REGISTER
from devtools.overview_data import (
    APOSTROPHE,
    EN_DASH,
    REPO,
    Overview,
    Result,
    math_html,
    tex_bounds,
)
from devtools.render_overview import DOCUMENT_PAGES, RESULTS_PAGE
from devtools.render_recent_results import HOLDS, NOT_A_BOUND, STANDINGS, Lane, Row
from devtools.repo_links import branch_file
from sqpack.yamlio import safe_load


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
    """A standing as a row attribute and a filter value: `current best, reported`
    is `current-best-reported`."""
    return re.sub(r"[^a-z]+", "-", standing_label(standing)).strip("-")


def standing_chip(standing: str) -> str:
    """A result's standing as a chip: the accent where a case bound rests on it now,
    the plain gray otherwise, so a reader sees at a glance which results still hold."""
    tone = ' data-tone="accent"' if standing == HOLDS else ""
    return (
        f'<span class="site-chip" data-standing="{_esc(standing_key(standing))}"{tone}>'
        f"{_esc(standing_label(standing))}</span>"
    )


def result_url(result_id: str) -> str:
    """A result's row in the results table, on its own page."""
    return f"{RESULTS_PAGE}#{result_id.lower()}"


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


def card_hero(src: str) -> str:
    """A card's optional hero: a small picture at its head, in a fixed 16:9 box the
    picture covers from its top edge. It is decorative (`alt=""`), since the card's own
    label and value say what it shows, and loads lazily. `src` is a file served beside
    the page, never an address off the site."""
    if "://" in src or src.startswith("//"):
        raise SystemExit(f"{src}: a card's hero is served beside the page, never fetched")
    return (
        '<span class="site-card-hero">'
        f'<img src="{_esc(src)}" alt="" loading="lazy" decoding="async"></span>'
    )


#: A card's size, narrowest first. A card says which it is in `data-card-size`, and
#: `site.css` gives each its width: a column of the grid of that size's minimum column
#: the card section's frame fits (`paper-design.md`, Cards).
CardSize = Literal["small", "medium", "large"]
CARD_SIZES: tuple[CardSize, ...] = get_args(CardSize)

#: The default size's two thresholds, in characters of a card's own text, its headline
#: and its note together: fewer than the first is a small card, the second or more a
#: large one, and anything between a medium one.
CARD_SMALL_BELOW = 80
CARD_LARGE_FROM = 160

#: Each card section's size, declared here so its cards are one width and its lines one
#: grid. Each is the size its typical card's text asks for by `card_size` (a test holds
#: the two together): the documents' one-line notes are small; the rest carry a sentence
#: and are medium.
SECTION_CARD_SIZES: dict[str, CardSize] = {
    "pages": "medium",
    "atlas": "medium",
    "projects": "medium",
    "documents": "small",
}


#: Elements with no end tag, which open nothing a parser must later close.
_VOID_TAGS = frozenset({"br", "hr", "img", "input", "wbr"})


class _ReadingText(HTMLParser):
    """An HTML fragment's text as a reader sees it: a formula is its MathML's text, not
    also the TeX kpress carries beside it for KaTeX to set. `outside` is the text that
    is in no formula, and `formulas` counts them."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.outside: list[str] = []
        self.formulas = 0
        self._skipping = 0
        self._in_math = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _VOID_TAGS:
            return
        classes = (dict(attrs).get("class") or "").split()
        if self._in_math:
            self._in_math += 1
        elif "kpress-math" in classes:
            self._in_math = 1
            self.formulas += 1
        if self._skipping:
            self._skipping += 1
        elif "kpress-math-render" in classes:
            self._skipping = 1

    def handle_endtag(self, tag: str) -> None:
        if tag in _VOID_TAGS:
            return
        if self._skipping:
            self._skipping -= 1
        if self._in_math:
            self._in_math -= 1

    def handle_data(self, data: str) -> None:
        if not self._skipping:
            self.parts.append(data)
        if not self._in_math:
            self.outside.append(data)


def _read(fragment: str) -> _ReadingText:
    reader = _ReadingText()
    reader.feed(fragment)
    reader.close()
    return reader


def reading_text(fragment: str) -> str:
    """`fragment`'s text as it reads, with runs of white space as one space."""
    return " ".join("".join(_read(fragment).parts).split())


def formulas(fragment: str) -> int:
    """How many formulas `fragment` holds."""
    return _read(fragment).formulas


def words(fragment: str) -> str:
    """`fragment`'s text that is in no formula, with runs of white space as one space."""
    return " ".join("".join(_read(fragment).outside).split())


def is_all_math(fragment: str) -> bool:
    """Whether `fragment` is mathematics standing alone: at least one formula, and no
    word, digit or mark outside one. `$n = 11$` is; "Earlier $n = 11$ lower bounds" is
    not."""
    return formulas(fragment) > 0 and not words(fragment)


#: The mark that sets a block's mathematics in the serif face whatever the words around
#: it are set in; the host adapter's sans test (`host_math_init.js`) honours it.
SERIF_MATH = 'data-math-face="serif"'


def headline_math_face(headline: str) -> str:
    """The attribute, with its leading space, for a headline's element: `SERIF_MATH`
    when the headline is mathematics standing alone, such as `$n = 11$`, and nothing
    when it has words, whose math then follows them into the sans face."""
    return f" {SERIF_MATH}" if is_all_math(headline) else ""


def size_for_length(length: float) -> CardSize:
    """The size a card whose text runs to `length` characters takes by default: under
    `CARD_SMALL_BELOW` is small, `CARD_LARGE_FROM` or more is large, and between them
    medium."""
    if length < CARD_SMALL_BELOW:
        return "small"
    return "large" if length >= CARD_LARGE_FROM else "medium"


def card_size(*text: str) -> CardSize:
    """The size a card takes when its spec declares none, from how much text it carries:
    its headline and its note (and a direct card's address), as HTML, counted as they
    read (`reading_text`) and sized by `size_for_length`."""
    return size_for_length(sum(len(reading_text(part)) for part in text))


def _size_attribute(size: CardSize | None, *text: str) -> str:
    """A card's `data-card-size`: the size its spec declares, or `card_size`'s default."""
    chosen = size or card_size(*text)
    if chosen not in CARD_SIZES:
        raise SystemExit(f"{chosen!r} is not a card size: {', '.join(CARD_SIZES)}")
    return f'data-card-size="{chosen}"'


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
    hero: str = "",
    size: CardSize | None = None,
    links: Sequence[tuple[str, str]] = (),
) -> str:
    """A card and the popover it opens. The card is a caps label, the summary and a line
    under it; pressing it opens a popover that repeats the label and summary, shows
    where the card leads, and ends in a button that goes there.

    What the popover shows depends on the target. Another page of the site, a document
    among them, is rendered in the popover itself: framed narrow, without its site
    chrome, and the button expands it to the full page. A place on this page is
    previewed from `preview`, and the button scrolls there; so is a row on another page,
    such as a result's in the results table, and the button goes to that page. `also`
    adds a second, quiet link, such as the document on GitHub. `hero` heads the card
    with a picture (`card_hero`). `size` is the card's width, small, medium or large;
    left out, `card_size` chooses it from the length of the value and note. `links` are
    further quiet links beside the button, each its address and its words, for what a
    card's note names but cannot link: a card is a button.

    The popover is native (`popover`), so it opens, closes on Escape or a click outside,
    and follows its button with no script. It is set in sans, so its math is sans too,
    with one exception the card shares: a headline that is mathematics standing alone
    (`headline_math_face`) is set in the serif. The label and action are escaped here;
    the value, note and preview are HTML, so they may carry math.
    """
    face = headline_math_face(value)
    kind = card_kind(href)
    if kind == "page" and not preview:
        body = (
            f'<iframe class="site-popover-frame" src="{_esc(embed_url(href))}" '
            f'loading="lazy" title="{_esc(label)}"></iframe>'
        )
    else:
        body = f'<div class="site-popover-preview">{preview}</div>'
    second = "".join(
        f' <a class="site-popover-also" href="{_esc(url)}">{_esc(words)}</a>'
        for url, words in (*((also,) if also else ()), *links)
    )
    return (
        f'<button type="button" class="site-card" popovertarget="{_esc(target)}" '
        f'data-go="{kind}" {_size_attribute(size, value, note)}>'
        f"{card_hero(hero) if hero else ''}"
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<span class="site-card-value"{face}>{value}</span>'
        f'<span class="site-card-note">{note}</span></button>'
        f'<div class="site-popover" id="{_esc(target)}" popover '
        f'data-go="{kind}">'
        f'<button type="button" class="site-popover-close" popovertarget="{_esc(target)}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<p class="site-popover-value"{face}>{value}</p>{body}'
        f'<p class="site-popover-actions"><a class="site-popover-action" href="{_esc(href)}" '
        f'data-go="{kind}">{_esc(action)}</a>{second}</p>'
        "</div>"
    )


def _cards(cards: list[str]) -> str:
    frame = '<div class="site-cards-frame site-wide"><div class="site-cards">'
    return frame + "".join(cards) + "</div></div>"


# ---------- Row popovers: the one way a table row shows its detail ----------


class RowDetail(NamedTuple):
    """The three pieces that make a table row the unit (paper-design.md, Row popovers).

    The caller writes `attributes` into the row's `<tr>`, `trigger` into one of its
    cells, and `popover` after the table, outside every cell, so no cell expands and the
    panel takes no style from the table. The row finds its popover by id, so sorting and
    filtering, which move and hide rows, never part a row from its popover.
    """

    attributes: str
    """For the `<tr>`: `data-row-popover`, the id of the row's popover, and `aria-label`,
    the row's accessible name. It carries no `tabindex`: `overview/row-popover.js` makes
    the row focusable, so a row is never a stop that does nothing."""
    trigger: str
    """The row's one native trigger, a `<button popovertarget>` around the row's own key:
    without scripts it is what opens the popover; with them the whole row does, and the
    button leaves the tab order so each row is one stop."""
    popover: str
    """The panel: a card's popover in every way (`.site-popover`: the close cross, the caps
    label, the headline, Escape and a click outside), with the row's body and an optional
    action at its foot."""


def row_detail(
    target: str,
    *,
    name: str,
    trigger: str,
    label: str,
    title: str,
    body: str,
    action: tuple[str, str] | None = None,
    deferred: bool = False,
    fallback: str = "",
    source: str = "",
) -> RowDetail:
    """A table row's popover and the markup that ties its row to it.

    `target` is the popover's id, unique on the page; `name` the row's accessible name,
    plain text; `trigger` the HTML the native trigger wraps, the row's own key such as its
    id. The popover repeats `label` as its caps label and `title` as its headline, set as
    every headline is (`headline_math_face`: serif when it is mathematics standing alone,
    sans with its words otherwise), then `body`, the row's detail, and, when
    `action` is `(href, words)`, the one button that goes there. `name`, `label` and the
    action's words are escaped here; `trigger`, `title` and `body` are HTML.

    A `deferred` body is held in a `<template>`, which the browser parses but neither
    lays out nor typesets, and `overview/row-popover.js` places it the first time the
    popover opens: for a body too heavy to render once per row at load. It costs the
    same bytes. Without scripts a template stays inert, so `fallback`, HTML in a
    `<noscript>` beside it, is what such a reader's popover shows.

    `source` is for a body too heavy to carry in the page at all: the address, beside
    the page, of a fuller body that the script fetches when the popover is first opened
    and puts in place of `body`, which is then the short form the page itself holds and
    what a reader without scripts, or off the network, keeps. The page gains only the
    address.
    """
    if deferred and source:
        raise SystemExit(f"{target}: a row body waits in a template or is fetched, not both")
    if deferred:
        body = f"<template data-row-pop-body>{body}</template>" + (
            f"<noscript>{fallback}</noscript>" if fallback else ""
        )
    fetched = f' data-row-pop-src="{_esc(source)}"' if source else ""
    target = _esc(target)
    attributes = f'data-row-popover="{target}" aria-label="{_esc(name)}"'
    button = (
        f'<button type="button" class="site-row-open" popovertarget="{target}">'
        f"{trigger}</button>"
    )
    foot = ""
    if action:
        href, words = action
        kind = card_kind(href)
        foot = (
            f'<p class="site-popover-actions"><a class="site-popover-action" '
            f'href="{_esc(href)}" data-go="{kind}">{_esc(words)}</a></p>'
        )
    popover = (
        f'<div class="site-popover site-row-pop" id="{target}" popover role="dialog" '
        f'aria-labelledby="{target}-title">'
        f'<button type="button" class="site-popover-close" popovertarget="{target}" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<p class="site-popover-value"{headline_math_face(title)} id="{target}-title">'
        f"{title}</p>"
        f'<div class="site-row-pop-body"{fetched}>{body}</div>{foot}</div>'
    )
    return RowDetail(attributes, button, popover)


def plain_text(register: str) -> str:
    """Register prose as an accessible name: its code marks dropped, its spaces one."""
    return " ".join(register.replace("`", "").split())


def _dl(rows: list[tuple[str, str]]) -> str:
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in rows)
    return f'<dl class="site-detail">{body}</dl>'


def _detail(result: Result) -> str:
    """A result's claim, composition, next rung, why it matters and novelty label: the
    short form of what its row opens to, which the page itself carries (`result_row`)."""
    record = result.record
    rows = [("Claim", tex_bounds(" ".join(str(record["claim"]).split())))]
    for key, label in (("composition", "Composition"), ("next_rung", "Next rung")):
        if record.get(key):
            rows.append((label, tex_bounds(" ".join(str(record[key]).split()))))
    rows.append(
        ("Significance", tex_bounds(" ".join(str(record["significance"]["rationale"]).split())))
    )
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


def result_row_popover_body(result: Result, overview: Overview) -> str:
    """The body of a result row's popover, the one source of it for every table that
    lists results: the recent table on the overview and the results page's table. It is
    the result's whole overview (`result_overview.result_popover_html`): its case drawn,
    the chain of results on that case, and every link.

    The overviews run to 2.8 MB between them, and two pages list the results, so no page
    carries one. Each is written once, beside the pages (`result_fragment`,
    `render_overview.result_fragments`), and a row's popover fetches its own when it
    first opens (`result_row`).
    """
    # `result_overview` reads this module for the chips and the film's facts.
    from devtools import result_overview  # noqa: PLC0415

    return result_overview.result_popover_html(result, overview)


#: Where the result overviews are served, under the site's root: a directory of
#: fragments, one a result, which are not pages. Not `results/`: `results.html` is
#: `RESULTS.md`, and a host may serve either at `/results`.
RESULT_FRAGMENTS = "result"


def result_fragment(result_id: str) -> str:
    """The address of a result's overview, from a page at the site's root. Its links
    are written from the root too, so only a page there may place it."""
    return f"{RESULT_FRAGMENTS}/{result_id.lower()}.html"


def result_row(result: Result, *, trigger: str, here: bool) -> RowDetail:
    """A result's row popover, the same on every page: its id as the caps label, its
    summary as the headline, then the result's short detail (`_detail`), which the
    script replaces with the whole overview, fetched from `result_fragment` when the
    popover first opens. A row on the results page (`here`) is the result's own row, so
    its popover has no button; anywhere else it ends in the button to that row."""
    action = None if here else (result_url(result.id), f"Open {result.id} in the results table")
    return row_detail(
        f"pop-result-{result.id.lower()}",
        name=f"{result.id}: {plain_text(result.summary)}",
        trigger=trigger,
        label=result.id,
        title=tex_bounds(result.summary),
        body=_detail(result),
        action=action,
        source=result_fragment(result.id),
    )


# ---------- Result filters: one tools bar for every table of results ----------


class FilterDefaults(NamedTuple):
    """Where a table's bar starts, which is all that differs between the two tables of
    results: the lowest significance shown and the greatest age in days, each `None`
    for no limit. Every other control starts at all on both."""

    significance: int | None = None
    max_age: int | None = None


#: The overview's Recent Results: what matters most, from the last half year.
RECENT_DEFAULTS = FilterDefaults(significance=4, max_age=180)

#: The results page: every result, of any significance and any age.
RESULTS_DEFAULTS = FilterDefaults()

#: The rung filters, in the bar's order: the scale, which names the row's attribute
#: (`data-s`), and the select's label.
RUNG_FILTERS: tuple[tuple[str, str], ...] = (
    ("S", "Significance"),
    ("V", "Verification"),
    ("C", "Confirmation"),
)

#: What every select of the bar offers first: no filter on that facet.
ALL = "All"


def result_cases(result: Result) -> str:
    """A result's cases as its row's `data-n`, which the Case filter reads: each count,
    and a run of counts as a range, `18-21 26`."""
    return result.scope.replace(EN_DASH, "-").replace(",", "")


def result_facets(result: Result) -> str:
    """A result row's facets as attributes, the same on every table of results, each one
    a filter of `result_filters`: whose result it is, its V, C and S rungs as numbers,
    its standing, its cases and the date the table shows."""
    record = result.record
    return (
        f'data-source="{"ours" if result.ours else "others"}" '
        f'data-v="{_esc(record["verification"][1:])}" '
        f'data-c="{_esc(record["confirmation"][1:])}" '
        f'data-s="{significance(result)}" '
        f'data-standing="{_esc(standing_key(result.standing))}" '
        f'data-n="{_esc(result_cases(result))}" '
        f'data-date="{_esc(first_day(result.dated[1]))}"'
    )


def reference_date(overview: Overview) -> date:
    """The day a render measures a result's age from: the newest `registered` date in
    the register. It is the register's own and never the clock's, so two renders of one
    tree are the same bytes. It decides only what the HTML starts with: on the page,
    `overview/table.js` measures every age again from the reader's own day."""
    return max(date.fromisoformat(str(r.record["registered"])) for r in overview.results)


def age_cutoff(reference: date, days: int) -> str:
    """The first day a row may be dated to be no older than `days` on `reference`, as
    `overview/table.js` reckons it (`ageCutoff`): 180 days on 2026-09-30 is 2026-04-03."""
    return (reference - timedelta(days=days)).isoformat()


def shown_by_default(result: Result, defaults: FilterDefaults, reference: date) -> bool:
    """Whether a result's row shows before the reader touches the filters, a table's
    `defaults`, with its age measured from `reference`."""
    if defaults.significance is not None and significance(result) < defaults.significance:
        return False
    return defaults.max_age is None or first_day(result.dated[1]) >= age_cutoff(
        reference, defaults.max_age
    )


def rung_options(scale: str) -> list[tuple[str, str]]:
    """A rung filter's choices: all, then each level above the scale's lowest as a
    floor, `S4 and up`, the top one bare. The levels are the rubric's own."""
    levels = sorted(level for level, _ in rubric_levels()[scale])
    return [
        ("", ALL),
        *(
            (str(level), f"{scale}{level}" + ("" if level == levels[-1] else " and up"))
            for level in levels[1:]
        ),
    ]


def _options(options: Iterable[tuple[str, str]], selected: str = "") -> str:
    return "".join(
        f'<option value="{_esc(value)}"{" selected" if value == selected else ""}>'
        f"{_esc(label)}</option>"
        for value, label in options
    )


def first_day(dated: str) -> str:
    """A date the register gives only to its year or its month, as the first day of it,
    so every row's `data-date` is a whole date and orders as text: `1979` is
    `1979-01-01`, and `2005-03` is `2005-03-01`."""
    missing = "-01-01"[max(len(dated) - 4, 0) :]
    return dated + missing if len(dated) < len("2026-01-01") else dated


def count_text(shown: int, total: int, noun: str = "results") -> str:
    """A tools bar's count, as `overview/table.js` writes it (`countText`)."""
    return f"{total} {noun}" if shown == total else f"{shown} of {total} {noun}"


def result_filters(
    overview: Overview, listed: Sequence[Result], defaults: FilterDefaults
) -> str:
    """The one tools bar every table of results carries: the overview's recent table and
    the results page's table. `overview/table.js` drives it.

    One control per facet a row carries (`result_facets`), and they compose: Significance,
    Verification and Confirmation as floors (`data-bound="min"`), Standing and Source as
    equalities, Case as a number the row's cases must hold (`covers`), and Max age as the
    most days the row's date may lie behind the reader's day (`age`), empty for no limit.

    A table's `defaults` are where Significance and Max age start; every other control
    starts at all. The tables write the rows outside those defaults `hidden` and the bar
    writes the count of the rows left, so the first paint is the filtered table. An age
    is measured there from `reference_date`, and by the script from the reader's day.
    Without scripts nothing stays filtered: `site.css` shows every row and drops the bar.

    The choices come from the whole register, never from `listed`, the rows of the table
    the bar sits over, so the bar is the same on both pages but for where it starts and
    its count.
    """
    present = {result.standing for result in overview.results}
    last = f' max="{max(overview.cases)}"' if overview.cases else ""
    floor = "" if defaults.significance is None else str(defaults.significance)
    age = "" if defaults.max_age is None else f' value="{defaults.max_age}"'
    reference = reference_date(overview)
    rungs = "".join(
        f'<label>{label} <select data-filter="{scale.lower()}" data-bound="min">'
        f"{_options(rung_options(scale), floor if scale == 'S' else '')}"
        "</select></label>"
        for scale, label in RUNG_FILTERS
    )
    standings = [
        ("", ALL),
        *(
            (standing_key(standing), standing_label(standing))
            for standing in STANDINGS
            if standing in present
        ),
    ]
    sources = [("", ALL), ("ours", "This project"), ("others", "Others")]
    shown = sum(shown_by_default(result, defaults, reference) for result in listed)
    return (
        '<div class="site-table-tools site-result-filters">'
        f"{rungs}"
        f'<label>Standing <select data-filter="standing">{_options(standings)}</select></label>'
        f'<label>Source <select data-filter="source">{_options(sources)}</select></label>'
        '<label>Case <var>n</var> <input type="number" data-filter="n" data-bound="covers" '
        f'min="1"{last} placeholder="any"></label>'
        '<label>Max age <input type="number" data-filter="date" data-bound="age" '
        f'min="0" placeholder="any"{age}> days</label>'
        '<span class="site-count" data-count data-noun="results" aria-live="polite">'
        f"{count_text(shown, len(listed))}</span></div>"
    )


def results_table(overview: Overview, defaults: FilterDefaults = RESULTS_DEFAULTS) -> str:
    """Every registered result, grouped as `RESULTS.md` groups them, which is by the
    relation `RESULTS.md` prints (`result_credit.source_lineage`), with its
    standing and, for a result by others, the date it was published. Each row opens its
    result's popover (`result_row`), placed after the table; its id is the trigger.
    The bar above it is `result_filters`, starting at `defaults`, which on the results
    page hide nothing; a row outside them is `hidden` in the HTML, and so is a group
    heading with no row left under it."""
    reference = reference_date(overview)
    head = (
        "<thead><tr>"
        '<th data-sort="text" class="site-col-id">ID</th>'
        '<th data-sort="num" class="num site-col-n">n</th>'
        '<th class="site-col-result">Result</th>'
        '<th data-sort="text">Credit</th>'
        '<th data-sort="text" title="Significance, verification and confirmation, then '
        'whether a case bound rests on the result now">Rungs</th>'
        '<th data-sort="text" title="Published, for a result by others; established, for '
        f'this project{APOSTROPHE}s">Date</th>'
        "<th>Records</th>"
        "</tr></thead>"
    )
    body = []
    popovers = []
    for title, members in overview.groups:
        shown = {result.id: shown_by_default(result, defaults, reference) for result in members}
        hidden = "" if any(shown.values()) else " hidden"
        body.append(
            f'<tr class="site-group-row" data-group="{_esc(title)}"{hidden}>'
            f'<th colspan="7" scope="colgroup">{_esc(title)}</th></tr>'
        )
        for result in members:
            record = result.record
            kind, date = result.dated
            detail = result_row(result, trigger=_esc(result.id), here=True)
            popovers.append(detail.popover)
            body.append(
                f'<tr id="{_esc(result.id.lower())}" {result_facets(result)} '
                f"{detail.attributes}{'' if shown[result.id] else ' hidden'}>"
                f'<td class="site-col-id" data-value="{_esc(result.id)}">{detail.trigger}</td>'
                f'<td class="num site-col-n" data-value="{result.first_n}">'
                f"{_esc(result.scope)}</td>"
                f'<td class="site-col-result">{tex_bounds(result.summary)}</td>'
                '<td class="site-col-credit site-cell-quiet" '
                f'data-value="{_esc(result.credit)}">'
                f"{_esc(result.credit)}</td>"
                f'<td class="site-rungs" '
                f'data-value="{_esc(record["confirmation"] + record["verification"])}">'
                f"{rung_chips(result)}"
                f'<span class="site-standing">{standing_chip(result.standing)}</span></td>'
                f'<td class="site-col-date" data-value="{_esc(date)}">'
                f'<span class="site-date-kind">{_esc(kind)}</span> {_esc(date)}</td>'
                f'<td class="site-records">{_records(result)}</td>'
                "</tr>"
            )
    return (
        f'<div class="site-wide">{result_filters(overview, overview.results, defaults)}'
        '<div class="site-table-wrap">'
        f'<table class="kpress-table site-table site-results" data-site-table>{head}'
        f"<tbody>{''.join(body)}</tbody></table></div>{''.join(popovers)}</div>"
    )


#: The rubric's three scored dimensions, in the site's order, significance first: the
#: scale, its name, the `epistemics.md` section that defines it, and the question it
#: answers.
DIMENSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("S", "Significance", "significance-and-novelty", "How much does the result matter?"),
    ("V", "Verification", "verification", "How strongly is the claim checked, by anyone?"),
    ("C", "Confirmation", "confirmation", "What has this repository checked itself?"),
)

_LEVEL_ROW = re.compile(r"^\| `([VCS])(\d)` \| ([^|]+?) \|", re.MULTILINE)


def rubric_levels() -> dict[str, list[tuple[int, str]]]:
    """Each dimension's levels and their one-line meanings, read from the tables in
    `epistemics.md`, so the ladder diagram cannot drift from the rubric it summarizes."""
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


#: The short form the ladder diagram prints for a rung whose meaning in `epistemics.md`
#: does not fit a cell's two lines. This is the one place a short form is written; a rung
#: not named here prints its meaning whole. The chip's `title` carries the full meaning
#: either way.
RUNG_SHORT_MEANINGS: dict[str, str] = {
    "S4": "Reusable technique, bound family, or settled value",
    "S5": "Moves a central open case, or broad adoption",
}

#: How many characters one line of a ladder cell's description holds where the cell is
#: narrowest, 13.5rem or 216px (`--site-ladders-meaning-min` in `site.css`): the note
#: size sets a line of prose at 7.3 to 8.4px a character, so 25 characters are at most
#: 210px. A description fits its two lines when it wraps to two lines of this many
#: characters; `tests/test_site_ladders.py` measures the same in a browser, in pixels.
SHORT_MEANING_LINE = 25


@cache
def rung_meanings() -> dict[str, str]:
    """Every rung chip's label (`V3`, `C5`, `S2`) and its one-line meaning, from the
    tables in `epistemics.md`, so a chip's `title` says what the rubric says."""
    return {
        f"{scale}{level}": meaning
        for scale, levels in rubric_levels().items()
        for level, meaning in levels
    }


@cache
def rung_short_meanings() -> dict[str, str]:
    """Every rung's description in a ladder cell: its short form in `RUNG_SHORT_MEANINGS`,
    or the rubric's own meaning where that fits. One that does not fit two lines of the
    narrowest cell fails the build, since the fix is a shorter text, never a clipped one."""
    meanings = rung_meanings()
    unknown = sorted(set(RUNG_SHORT_MEANINGS) - set(meanings))
    if unknown:
        raise SystemExit(f"a short form names no rung of epistemics.md: {', '.join(unknown)}")
    short = {
        label: RUNG_SHORT_MEANINGS.get(label, meaning) for label, meaning in meanings.items()
    }
    for label, text in short.items():
        if len(textwrap.wrap(text, SHORT_MEANING_LINE)) > 2:
            raise SystemExit(
                f"{label}'s description, {text!r}, does not fit two lines of "
                f"{SHORT_MEANING_LINE} characters: give it a short form in RUNG_SHORT_MEANINGS"
            )
    return short


def rung_counts() -> dict[str, Counter[int]]:
    """How many registered results stand at each level of each dimension, read from the
    register, so the diagram shows an empty rung as empty rather than omitting it."""
    results = safe_load(REGISTER.read_text(encoding="utf-8"))["results"]
    counts: dict[str, Counter[int]] = {scale: Counter() for scale, *_ in DIMENSIONS}
    for record in results:
        counts["V"][int(record["verification"][1])] += 1
        counts["C"][int(record["confirmation"][1])] += 1
        counts["S"][int(record["significance"]["score"])] += 1
    return counts


def count_label(count: int) -> str:
    """How the diagram says how many results stand at a level; an empty rung says so."""
    if count == 0:
        return "no result yet"
    return f"{count} result" + ("" if count == 1 else "s")


def _ladder_cell(scale: str, level: int, count: int) -> str:
    """One rung of the ladder diagram: the chip the tables use, titled with the rubric's
    full meaning, the two-line description, and how many results stand there."""
    label = f"{scale}{level}"
    return (
        f'<div class="site-ladders-cell" role="cell" data-ladder="{scale}">'
        '<div class="site-ladders-rung">'
        f'<span class="site-chip site-rung-fill" title="{_esc(rung_meanings()[label])}" '
        f"{_fill(label)}>{label}</span>"
        f'<span class="site-ladders-meaning">{_esc(rung_short_meanings()[label])}</span>'
        f'<span class="site-ladders-count">{_esc(count_label(count))}</span>'
        "</div></div>"
    )


def verification_block() -> str:
    """The rating ladders as one diagram: a column per dimension of the rubric,
    Significance, Verification, Confirmation, headed by its name and the question it
    answers, and a row per level, the highest at the top, so the rungs of the three
    ladders line up. A cell is the rung's chip, its description on two lines and the
    count of results at that level; a ladder with no rung at a level leaves its cell
    empty, as Significance does at level 0.

    It is a grid marked with table roles, not a `<table>`: kpress wraps every table on a
    page in its own scroller and restyles it as `.kpress-table`, which this diagram is
    not. Each name links to that section of `epistemics.md`.
    """
    levels = {scale: {level for level, _ in rungs} for scale, rungs in rubric_levels().items()}
    counts = rung_counts()
    heads = "".join(
        f'<div class="site-ladders-head" role="columnheader" data-ladder="{scale}">'
        f'<a class="site-ladders-name" href="epistemics.html#{section}">{_esc(name)}</a> '
        f'<span class="site-ladders-question">{_esc(question)}</span></div>'
        for scale, name, section, question in DIMENSIONS
    )
    rows = [
        (
            '<div class="site-ladders-row" role="row">'
            f'<span class="site-ladders-level" role="columnheader">Level</span>{heads}</div>'
        )
    ]
    every = sorted({level for scale, *_ in DIMENSIONS for level in levels[scale]}, reverse=True)
    for level in every:
        cells = "".join(
            _ladder_cell(scale, level, counts[scale][level])
            if level in levels[scale]
            else f'<div class="site-ladders-cell site-ladders-empty" role="cell" '
            f'data-ladder="{scale}"></div>'
            for scale, *_ in DIMENSIONS
        )
        rows.append(
            f'<div class="site-ladders-row" role="row" data-level="{level}">'
            f'<span class="site-ladders-level" role="rowheader">Level {level}</span>'
            f"{cells}</div>"
        )
    names = ", ".join(name.lower() for _, name, _, _ in DIMENSIONS)
    return (
        '<div class="site-ladders-frame site-wide">'
        f'<div class="site-ladders" role="table" aria-label="Rating ladders by level: {names}">'
        f"{''.join(rows)}</div></div>"
    )


#: A summary that leads with its formula: the formula, then the method after "by", then
#: a trailing ", reported" that the standing chips already say.
_LEADING_FORMULA = re.compile(r"(`[^`]+`)(?:,? by (?:an? )?(?P<method>.+?))?(?:, reported)?")

#: How many names of a credit's "after …" list show before the rest is cut to its title.
CREDIT_AFTER_SHOWN = 3


def recent_results(overview: Overview) -> list[Result]:
    """Every result, newest first: by the date the table shows, then by id. What makes
    the table recent is its bar's defaults (`RECENT_DEFAULTS`), which a reader can
    change, and never a cut the page makes for them."""
    return sorted(overview.results, key=lambda r: (first_day(r.dated[1]), r.id), reverse=True)


def significance(result: Result) -> int:
    """A result's S rung, the level its S chip shows."""
    return int(result.record["significance"]["score"])


def result_rungs(result: Result) -> tuple[str, str, str]:
    """A result's three rungs in the order the site lists them wherever it shows them:
    significance first, then verification and confirmation (`S4`, `V4`, `C3`). The
    register's own documents keep theirs, verification first."""
    record = result.record
    return (f"S{significance(result)}", record["verification"], record["confirmation"])


def rung_chips(result: Result) -> str:
    """A result's rung chips, S, V and C, a space apart: the one place their order is
    set, for a table's row, a popover, a result's overview and a case record."""
    return " ".join(_rung(rung) for rung in result_rungs(result))


def split_summary(summary: str) -> tuple[str, str]:
    """A summary as its result and its method: `` `s(21) = 5` by a point-only route ``
    is the formula and "point-only route". A summary that does not lead with one
    formula, such as a batch of counts, is all result and no method."""
    match = _LEADING_FORMULA.fullmatch(summary)
    if not match:
        return summary, ""
    return match.group(1), match.group("method") or ""


def credit_cell(credit: str) -> str:
    """A credit with its finder first and "after …" quiet, the list cut after
    `CREDIT_AFTER_SHOWN` names; the cell's title keeps the whole credit."""
    finder, _, after = credit.partition(" after ")
    if not after:
        return _esc(finder)
    names = after.split(", ")
    shown = ", ".join(names[:CREDIT_AFTER_SHOWN])
    if len(names) > CREDIT_AFTER_SHOWN:
        shown += ", …"
    return f'{_esc(finder)} <span class="site-cell-quiet">after {_esc(shown)}</span>'


def standing_chips(standing: str) -> str:
    """A standing as one chip per part: `second certificate, reported` is two chips."""
    if standing == NOT_A_BOUND:
        return standing_chip(standing)
    return " ".join(standing_chip(part) for part in standing.split(", "))


def status_chips(result: Result) -> str:
    """A result's rung chips, S, V and C, then its standing chips, side by side."""
    return rung_chips(result) + " " + standing_chips(result.standing)


def recent_table(overview: Overview, defaults: FilterDefaults = RECENT_DEFAULTS) -> str:
    """Every result as one table, newest first: the date, the result linking to its row
    on the results page with its id quiet beside it, the method, the credit and the
    status chips. A result by others is dated by its publication, as `RESULTS.md` dates
    it, and this project's by the day it was established; the cell says which. The bar
    above it is `result_filters`, the results page's, starting at `defaults`: a row
    outside them is `hidden` in the HTML, so the first paint is already filtered. Each
    row opens its result's popover (`result_row`), the results page's, ending in the
    button to that page's row; the quiet id is its trigger."""
    results = recent_results(overview)
    reference = reference_date(overview)
    head = (
        "<thead><tr>"
        '<th class="site-col-date">Date</th>'
        '<th class="site-col-result">Result</th>'
        '<th class="site-col-method">Method</th>'
        '<th class="site-col-credit">Credit</th>'
        '<th class="site-col-status" title="Significance, verification and confirmation, '
        'then whether a case bound rests on the result now">Status</th>'
        "</tr></thead>"
    )
    rows = []
    popovers = []
    for result in results:
        kind, dated = result.dated
        formula, method = split_summary(result.summary)
        detail = result_row(result, trigger=_esc(result.id), here=False)
        popovers.append(detail.popover)
        rows.append(
            f'<tr data-result="{_esc(result.id.lower())}" {result_facets(result)} '
            f"{detail.attributes}"
            f"{'' if shown_by_default(result, defaults, reference) else ' hidden'}>"
            f'<td class="site-col-date"><span class="site-date-kind">{_esc(kind)}</span> '
            f"{_esc(dated)}</td>"
            f'<td class="site-col-result"><a href="{_esc(result_url(result.id))}">'
            f"{tex_bounds(formula)}</a> "
            f'<span class="site-cell-quiet">{detail.trigger}</span></td>'
            f'<td class="site-col-method">{tex_bounds(method)}</td>'
            f'<td class="site-col-credit" title="{_esc(result.credit)}">'
            f"{credit_cell(result.credit)}</td>"
            f'<td class="site-col-status">{status_chips(result)}</td>'
            "</tr>"
        )
    return (
        f'<div class="site-wide">{result_filters(overview, results, defaults)}'
        '<div class="site-table-wrap">'
        '<table class="kpress-table site-table site-results site-recent-table">'
        f"{head}<tbody>{''.join(rows)}</tbody></table></div>{''.join(popovers)}</div>"
    )


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
        f'<a href="{_esc(result_url(entry))}">{_esc(entry)}</a> {_rung(v)} {_rung(c)}'
        for entry, v, c in _LANE_RESULT.findall(results)
    )


def _lane_detail(lane: Lane) -> str:
    """One lane in a replay row's popover: its value, who holds it and when it was
    published, and the register entries that carry it with their rungs."""
    held = _esc(lane.holder) + (f", published {_esc(lane.published)}" if lane.published else "")
    entries = _lane_results(lane.results)
    return f'{_lane_math(lane)} <span class="site-cell-quiet">{held}</span>' + (
        f"<br>{entries}" if entries else ""
    )


def replay_row_popover_body(row: Row) -> str:
    """The body of an awaiting-replay row's popover: the bound a source reports and the
    one verified here, each with its holder, date and the entries that carry it."""
    return (
        '<dl class="site-detail">'
        f"<dt>Reported</dt><dd>{_lane_detail(row.reported)}</dd>"
        f"<dt>Verified here</dt><dd>{_lane_detail(row.verified)}</dd></dl>"
    )


def awaiting_replay(overview: Overview) -> str:
    """The recent cases whose reported lower bound differs from the verified one: a
    source's bound waiting on a replay here. One row per case, grouped by holder and the
    entries that carry the claim, each case linked to its row in the frontier atlas.
    Each row opens its popover (`replay_row_popover_body`), its reported value the
    trigger, ending in the button to the frontier row; the popovers follow the
    disclosure, so none takes its compact table's style."""
    rows = overview.awaiting_replay
    if not rows:
        return ""
    groups: dict[tuple[str, str], list[str]] = {}
    popovers = []
    for row in rows:
        reported = row.reported
        detail = row_detail(
            f"pop-replay-n-{row.n}",
            name=f"n = {row.n}, reported {plain_text(reported.shown)}",
            trigger=_lane_math(reported),
            label="Awaiting replay",
            title=math_html(f"n = {row.n}"),
            body=replay_row_popover_body(row),
            action=(f"frontier.html#n-{row.n}", f"Open n = {row.n} in the frontier atlas"),
        )
        popovers.append(detail.popover)
        groups.setdefault((reported.holder, reported.results), []).append(
            f'<tr id="replay-n-{row.n}" data-n="{row.n}" {detail.attributes}>'
            f'<td class="num"><a href="frontier.html#n-{row.n}">{row.n}</a></td>'
            f"<td>{detail.trigger}</td>"
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
        f"</tr></thead><tbody>{body}</tbody></table></div></details>{''.join(popovers)}"
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
                size=SECTION_CARD_SIZES["documents"],
            )
            for (path, label, note), page in zip(DOCUMENTS, DOCUMENT_PAGES, strict=True)
        ]
    )


#: When the explainer's proofs are from, as its cards say it: T-018 was established on
#: 4 September 2026 and T-025 and T-026 on 9 September (`results.yaml`), first published
#: on 5 and 13 September (`sqpack.release.PUBLICATION_HISTORY`). A test holds this phrase
#: to those dates.
EXPLAINER_AS_OF = "early September"


class Paper(NamedTuple):
    """One of the site's papers, as its card says what it is: where it is served, a caps
    label naming its kind, its title, one or two sentences on what it is, the size of
    its card on the Papers page, and the quiet links its card's popover carries for
    what the description names. The title and description are register prose, so
    `n = 11` in either is set as math."""

    href: str
    label: str
    title: str
    description: str
    size: CardSize = "large"
    links: tuple[tuple[str, str], ...] = ()


#: Where the optimality paper is served, which `render_n11_optimality_explainer` builds
#: (its `SITE_PATH`; a test holds the two together). Named here rather than read from
#: that module, which loads the explainer's renderer and so this one's.
OPTIMALITY_PAPER = "n11-optimality/t-060-explainer.html"

#: Where the explainer's card sends a reader for the newer optimality proofs it names:
#: the paper that explains the proof, and T-060's row in the results table. Both of the
#: explainer's cards carry them. A card is a button and holds no link, so its popover
#: does.
OPTIMALITY_LINKS: tuple[tuple[str, str], ...] = (
    (OPTIMALITY_PAPER, "The optimality paper"),
    (result_url("T-060"), "The optimality proof, T-060"),
)

#: The site's papers, in the order the Papers page shows them, one large card each
#: (`paper_cards`). A new paper is one entry here. The optimality paper is first: it
#: explains the result that stands, T-060, where the explainer proves the lower bounds
#: T-060 superseded and the tutorial is the background to both. Its title is its
#: renderer's (`render_n11_optimality_explainer.TITLE`) in sentence case, and its
#: description says what T-060's rungs allow: a proof, machine-verified and reviewed
#: here. The explainer's title is the owner's (2026-09-30), as `render_explainer.TITLE`
#: has it in title case; the tutorial's description is `TUTORIAL.md`'s own opening, its
#: audience and what it owns.
PAPERS: tuple[Paper, ...] = (
    Paper(
        href=OPTIMALITY_PAPER,
        label="Optimality paper",
        title="Why eleven squares need this much room",
        description=(
            "Explains the accepted proof that Trump\u2019s 1979 packing of eleven squares "
            "is optimal, s(11) = 3.8770835\u2026 (T-060): the exact construction, the "
            "exhaustive case exclusions, the geometric capture and the local-isolation "
            "argument, with figures drawn from the retained proof data."
        ),
        links=((result_url("T-060"), "The optimality proof, T-060"),),
    ),
    Paper(
        href="explainer.html",
        label="Explainer",
        title="New lower bounds for square packing for n = 11",
        description=(
            "An explainer and proof of certain lower bounds for n = 11. It explains the "
            f"earlier, simpler proofs as of {EXPLAINER_AS_OF}; newer optimality proofs now "
            "exist (T-060)."
        ),
        links=OPTIMALITY_LINKS,
    ),
    Paper(
        href="tutorial.html",
        label="Tutorial",
        title="Square packing from first principles",
        description=(
            "An introduction for anyone new to the problem: what the objects are, why the "
            "approach is shaped the way it is, and what the research has and has not "
            "established. Each outside idea it uses, from linear programming to algebraic "
            "number fields, is introduced where it is first needed."
        ),
    ),
)
#: The explainer, whose card is the same on the overview as on the Papers page.
EXPLAINER = next(paper for paper in PAPERS if paper.href == "explainer.html")


def paper_cards() -> str:
    """One card per paper, the overview's page cards in kind: the whole card is a button
    that opens a popover framing the paper, which expands to it."""
    return _cards(
        [
            card(
                "pop-paper-" + re.sub(r"[^a-z0-9]+", "-", paper.href.removesuffix(".html")),
                paper.label,
                tex_bounds(paper.title),
                tex_bounds(paper.description),
                href=paper.href,
                action=f"Expand the {paper.label.lower()}",
                size=paper.size,
                links=paper.links,
            )
            for paper in PAPERS
        ]
    )


#: The site's other pages, as the overview's cards show them: the page, a label, its
#: title, and one line on what a reader finds there. Both are register prose, so a
#: bound in either is written in ASCII (`s(11) >= 3.8264…`) and set as math. The
#: explainer's card is its paper's; the tutorial's keeps a shorter line here.
PAGES: tuple[tuple[str, str, str, str], ...] = (
    (EXPLAINER.href, EXPLAINER.label, EXPLAINER.title, EXPLAINER.description),
    (
        "tutorial.html",
        "Tutorial",
        "Square packing from first principles",
        "The problem, its configuration space, exact algebra and the search.",
    ),
    (
        "workbench/",
        "Workbench",
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
                tex_bounds(note),
                href=href,
                action=f"Expand the {label.lower()}",
                size=SECTION_CARD_SIZES["pages"],
                links=EXPLAINER.links if href == EXPLAINER.href else (),
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
        "https://github.com/Queuingtheorydotcom/11SquaresOptimal",
        "Queuingtheorydotcom",
        "A computer-assisted proof that Trump's packing of eleven squares is optimal.",
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


#: Favicons for other projects hosted off GitHub, saved here by host name
#: (`example.org.png`, `.svg` or `.ico`) and inlined, so the page fetches nothing.
PROJECT_FAVICONS = Path(__file__).resolve().parent / "overview" / "favicons"

#: GitHub's mark (Octicons `mark-github`, 16 units), drawn in the text colour.
GITHUB_MARK = (
    '<svg class="site-link-icon" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
    '<path fill="currentColor" d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08'
    "-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 "
    "0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27"
    "-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28"
    "-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15"
    "-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67"
    '.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"/></svg>'
)

_FAVICON_TYPES = {".png": "image/png", ".svg": "image/svg+xml", ".ico": "image/x-icon"}


def link_icon(url: str) -> str:
    """The mark beside a project's address: GitHub's for a GitHub URL, otherwise the
    site's own favicon from `PROJECT_FAVICONS`, which a build without one refuses."""
    host = (urlsplit(url).hostname or "").removeprefix("www.")
    if host == "github.com":
        return GITHUB_MARK
    for suffix, mime in _FAVICON_TYPES.items():
        path = PROJECT_FAVICONS / f"{host}{suffix}"
        if path.is_file():
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            return (
                f'<img class="site-link-icon" src="data:{mime};base64,{data}" alt="" '
                'width="16" height="16">'
            )
    raise SystemExit(
        f"{url}: save {host}'s favicon as {PROJECT_FAVICONS.name}/{host}.png (or .svg, .ico)"
    )


def _breakable(address: str) -> str:
    """An address that may wrap after each slash rather than inside a name."""
    return "/<wbr>".join(_esc(part) for part in address.split("/"))


def link_card(
    url: str,
    label: str,
    value: str,
    note: str,
    *,
    hero: str = "",
    size: CardSize | None = None,
) -> str:
    """A card that is itself the link, with no popover: for a place whose address, or
    whose picture, is the whole of what a preview would say. It carries the label, the
    value and note, and `hero` heads it with a picture (`card_hero`). `size` is its
    width, as `card` takes it; left out, `card_size` chooses it from the value, the note
    and the address shown.

    Every card that navigates directly opens its target in a new tab, whether that is a
    page or file of this site or a place off it, so the page the reader chose it from
    stays where they left it. An address off the site is shown under the note beside
    the host's mark; a PDF is typed as one, so the browser opens it in place.
    """
    kind = card_kind(url)
    typed = ' type="application/pdf"' if url.endswith(".pdf") else ""
    address = ""
    if kind == "external":
        shown = url.removeprefix("https://").rstrip("/")
        address = (
            f'<span class="site-card-url">{link_icon(url)}'
            f"<span>{_breakable(shown)}</span></span>"
        )
    return (
        f'<a class="site-card site-card-link" href="{_esc(url)}"{typed} data-go="{kind}" '
        f"{_size_attribute(size, value, note, address)} "
        'target="_blank" rel="noopener noreferrer">'
        f"{card_hero(hero) if hero else ''}"
        f'<span class="site-card-label">{_esc(label)}</span>'
        f'<span class="site-card-value"{headline_math_face(value)}>{value}</span>'
        f'<span class="site-card-note">{note}</span>'
        f"{address}"
        "</a>"
    )


def other_project_cards() -> str:
    """One card per other project: its repository's name, its author, what it holds and
    its address. Each card is the link itself, opening the project in a new tab. The note
    is prose like a page card's, so a case it names (`n = 21`) is set as math."""
    cards = []
    for url, author, note in OTHER_PROJECTS:
        name = urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
        cards.append(
            link_card(
                url,
                f"By {author}",
                _esc(name),
                tex_bounds(note),
                size=SECTION_CARD_SIZES["projects"],
            )
        )
    return _cards(cards)


#: The page the atlas's film card opens: the film alone, at full size.
VISUALIZE_PAGE = "visualize.html"

#: The atlas's three direct cards: where each goes, the picture heading it (a file
#: served beside the page), its label, value and note.
ATLAS_CARDS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "known-best-1-100.pdf",
        "known-best-1-100-card.png",
        "Poster \u00b7 PDF",
        "n = 1 to 100",
        (
            "The first hundred, each labelled with its best-known side and, where the case is "
            "open, its strongest verified lower bound."
        ),
    ),
    (
        "known-best-1-324.pdf",
        "known-best-1-324.png",
        "Poster \u00b7 PDF",
        "n = 1 to 324",
        (
            "Every tracked case as its best-known packing, on one sheet that prints at 44 by "
            "51 inches."
        ),
    ),
    (
        VISUALIZE_PAGE,
        "ascent-n1-324-poster.png",
        "Visualize",
        "The ascent to n = 324",
        (
            "The atlas built one square at a time, each step naming the bound it reaches and "
            "its source. 8\u00a0m\u00a014\u00a0s."
        ),
    ),
)


def atlas_cards() -> str:
    """The atlas's posters and film as three cards side by side, each headed by its
    picture and itself the link: a poster opens its PDF, the film its own page."""
    return _cards(
        [
            link_card(
                href,
                label,
                tex_bounds(value),
                tex_bounds(note),
                hero=hero,
                size=SECTION_CARD_SIZES["atlas"],
            )
            for href, hero, label, value, note in ATLAS_CARDS
        ]
    )


#: The atlas grid's drawings, in units across the frame. One drawing serves the cell and
#: the popover, which shows it about four hundred pixels across: at 100 units the
#: rounding shows there as uneven gaps, and 400 costs about 26 kB more gzipped.
ATLAS_UNITS = 400

#: How many cases the atlas grid shows until the reader asks for the rest: the first
#: hundred, the cases of the smaller poster.
ATLAS_FIRST = 100

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
        'data-go="atlas" data-atlas-popover '
        'role="dialog" aria-labelledby="pop-atlas-title">'
        '<button type="button" class="site-popover-close" popovertarget="pop-atlas" '
        'popovertargetaction="hide" aria-label="Close">\u00d7</button>'
        '<span class="site-card-label">Best known packing</span>'
        f'<p class="site-popover-value site-atlas-pop-title" {SERIF_MATH} '
        'id="pop-atlas-title" data-atlas-title></p>'
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
        "See All Cases</a>"
        '<span class="site-atlas-pop-step">'
        '<button type="button" data-atlas-step="-1" aria-label="Previous case">'
        f"{step_arrow(back=True)}</button>"
        '<button type="button" data-atlas-step="1" aria-label="Next case">'
        f"{step_arrow()}</button>"
        "</span></p>"
        f"<template data-atlas-math>{math_html('n')}</template>"
        "</div>"
    )


#: The directions of the site's one arrow (paper-design.md, Arrows): each is the one
#: drawing, `--site-arrow` in site.css, turned or mirrored by `data-arrow`.
ARROW_DIRECTIONS = ("right", "left", "down", "up", "external")


def arrow_icon(direction: str = "right") -> str:
    """The site's arrow pointing `direction`, as inline markup: an empty, hidden span that
    site.css paints with the one arrow drawing in the text colour. It is never a typed
    `→`: the site's text face has no arrow glyphs, and each browser fell back to a
    different font for them, so no two arrows matched."""
    if direction not in ARROW_DIRECTIONS:
        raise ValueError(f"unknown arrow direction {direction!r}")
    return f'<span class="site-icon-arrow" data-arrow="{direction}" aria-hidden="true"></span>'


def step_arrow(*, back: bool = False) -> str:
    """The atlas stepper's arrow: the site's arrow, left for the previous case."""
    return arrow_icon("left" if back else "right")


def atlas_grid() -> str:
    """Every tracked case's known-best packing, n = 1 to 324, as a grid of drawings,
    each a link to its case record. With scripts, `overview/atlas-grid.js` opens a cell
    in the one atlas popover instead: what the ascent film's panel says about that n,
    from `atlas_film_facts`, beside the drawing shown large, with a button to the record.

    The cells, about a megabyte of SVG, sit in two `<template>`s, which the browser
    parses but does not render. The script places the first `ATLAS_FIRST` when the grid
    nears the viewport, so the page opens as fast as it did without them, and the rest
    only when the reader presses the button under the grid, "Show all 324", or steps the
    popover past the last case shown. The button then reads "Show 1 to 100" and collapses
    the grid again. Its row ships `hidden`, since without the script it would do
    nothing. The facts are one JSON element, a tenth the size the same facts would take
    as markup in every cell.
    """
    import json  # noqa: PLC0415

    from devtools import render_frontier_page as frontier  # noqa: PLC0415
    from devtools.render_case_pages import CASES_PAGE, case_url  # noqa: PLC0415

    cases = frontier.frontier_cases()
    cells = []
    for case in cases:
        n = case["n"]
        status = case["status"]
        cells.append(
            f'<a class="site-atlas-cell" href="{case_url(n)}" data-atlas-n="{n}" '
            f'data-status="{_esc(status)}" aria-label="n = {n}, {_esc(status)}">'
            f"{frontier.packing_svg(n, units=ATLAS_UNITS)}"
            f'<span class="site-atlas-n">{n}</span></a>'
        )
    facts = json.dumps(atlas_film_facts(), ensure_ascii=False, separators=(",", ":"))
    more, less = f"Show all {len(cases)}", f"Show 1 to {ATLAS_FIRST}"
    return (
        '<div class="site-wide site-atlas-grid" data-atlas-grid>'
        f"<template data-atlas-first>{''.join(cells[:ATLAS_FIRST])}</template>"
        f"<template data-atlas-rest>{''.join(cells[ATLAS_FIRST:])}</template>"
        '<script type="application/json" data-atlas-facts>'
        + facts.replace("</", "<\\/")
        + "</script>"
        '<p class="site-atlas-toggle-row" hidden>'
        '<button type="button" class="site-popover-action site-atlas-toggle" '
        'data-atlas-toggle aria-expanded="false" '
        f'data-label-more="{more}" data-label-less="{less}">{more}</button></p>'
        '<p class="site-atlas-note">Every case from n = 1 to 324 is also in the '
        '<a href="frontier.html">frontier atlas</a>, and each has a '
        f'<a href="{CASES_PAGE}">case record</a>.</p></div>{atlas_popover()}'
    )
