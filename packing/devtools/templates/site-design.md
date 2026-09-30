# Site Design

The published site is one publication: the overview, the frontier atlas, the tutorial
and the explainer share KPress’s tokens, reading faces, math, tables, themes and print
rules, and a reader moving between them should not notice a seam.
The explainer’s typography is written down in [paper-design.md](paper-design.md); this
document covers what the site adds on top of KPress and the explainer, and nothing it
restates.

[site.css](site.css) is the stylesheet, the scripts are under
[`../overview/`](../overview/), and the page templates
([site-shell.html](site-shell.html), [site-nav.html](site-nav.html),
[overview-article.md](overview-article.md)) point here rather than repeating it.
Each addition is written so it could move upstream into KPress unchanged.

## Three Rules

- **Only KPress tokens.** Every colour, face, size, radius and transition in `site.css`
  is a `--kpress-*` token or a `--site-*` token derived from them at the top of the
  sheet. So the sheet follows the reader’s theme and KPress’s print reset without a rule
  of its own, and a token KPress retunes moves the site with it.
- **Scoped.** Every selector names a `site-` class or the `data-site-page` attribute the
  site shell stamps on `<html>`, so nothing in it can match the explainer’s article
  (`.cert-page`), its figures or its math.
  The explainer does not inline this sheet.
  The navigation bar’s rules are in their own file, [site-nav.css](site-nav.css), which
  every page with the bar inlines, the explainer included, so the bar cannot differ
  between pages; a page aligns it with its own track through `--site-nav-max-width`.
- **Square.** Cards, chips, controls and the popover have square corners
  (`--kpress-radius-none`), like the explainer’s figures.

## Tokens

| Token | Value | Used by |
| --- | --- | --- |
| `--site-track` | `--kpress-font-size-base` × 40 + 14rem | the wide blocks, the nav and the footer |
| `--site-table-width` | the pane less 2rem, at most 76rem | the results table and its filters |
| `--site-chip-ink` | `--kpress-doc-text`, 14% toward `--kpress-doc-muted` | every chip’s fill |
| `--site-rung-v` | `--kpress-doc-link`, 20% toward `--kpress-doc-muted` | `V` badges |
| `--site-rung-c` | `--kpress-doc-success`, 22% toward `--kpress-doc-muted` | `C` badges |
| `--site-rung-s` | `--kpress-doc-muted` | `S` badges |
| `--site-icon-down`, `-page`, `-out`, `-star` | Lucide glyphs as data URIs | hover icons and the recent star |

The site pages set `--kpress-host-font-size-base` to 18px, the explainer’s base, and the
reading measure to 40 of it, the explainer’s measure.
Everything else is KPress’s own.

## The Page Frame

A site page’s `<html>` carries `data-site-page="<key>"`, and its article is
`<div class="kpress kpress-doc kpress-prose site-page site-<key>">` inside KPress’s
`kpress-page-main`.

- The document scrolls, not KPress’s viewport pane, so the footer follows the article
  and the browser keeps the reading position, as on the explainer.
- The page is `--site-track` wide.
  Prose (paragraphs, headings, lists) keeps the reading measure; a block marked
  `site-wide` (card grids, media) takes the whole track; the results table takes
  `--site-table-width`, which on a desktop is wider than the track.
- The overview has no visible `h1`: the page’s name is in `<title>` and the navigation
  bar. Its sections are `h2`, centred and set as KPress sets them (serif italic), at 1.2
  of the base as on the explainer; each has a stable id from `overview_page.SECTIONS`,
  such as `#recent-results`, which other pages link to.
- The hero is one inlined drawing, centred, at most 21rem wide; its strokes take the
  text colour of the theme.

## Navigation Bar and Footer

The bar is [site-nav.html](site-nav.html), filled by `site_kit.nav_html` and included by
every page but the Visualizer, a full-viewport app that keeps its own `#site-note`.

- The logo reads “Square Packing” in the sans, bold, a step larger than the items.
- The items are Overview, Frontier, Explainer, Tutorial, Visualizer and GitHub, in the
  muted colour. The current page carries `aria-current="page"` and is marked with the
  selected surface and the text colour.
- Every link answers hover with a background (`--kpress-doc-surface-hover`) and never
  with an underline.
- There is no tagline and no version in the bar; the edition is in the footer.
- On a phone the items wrap under the logo.

The footer (`render_overview.footer_html`) carries the edition, the data revision, the
build commit and the licence, centred, in the muted tiny sans, over a hairline.
Both the bar and the footer are `display: none` in print, so a printed page, and the
explainer’s PDF, show neither.

## Cards

Every highlighted box on a page is a card, and every card is a link: a page never mixes
plain boxes with clickable ones.

```html
<article class="site-card">
  <p class="site-card-meta">…</p>
  <h3 class="site-card-title"><a class="site-card-link" href="…" data-goes="page">…</a></h3>
  <p class="site-card-summary">One sentence.</p>
</article>
```

- **One link, stretched.** The card’s one `.site-card-link`, normally its title, covers
  the whole card through its `::after`, so the card is the link and the link’s text is
  the title. Secondary links inside a card (records, releases, cases) sit above the
  stretch and stay clickable.
  A preview card is a `<figure class="site-card">` whose caption holds the link.
- **One sentence of summary**, in `.site-card-summary`. The other parts are
  `.site-card-head` (the meta line and the chips, on one line where they fit),
  `.site-card-meta`, `.site-card-credit`, `.site-card-note` (small, muted) and
  `.site-card-foot` (the chips at the foot).
- **Hover** is gentle: the border darkens to the muted colour and the ground takes the
  code surface. Keyboard focus outlines the whole card.
- **The hover icon** says where the card goes, in the muted colour at the card’s bottom
  corner: `data-goes="down"` (an arrow down, a place on this page), `"page"` (an arrow
  right, another page of the site) or `"out"` (an arrow up and out, GitHub or another
  site). `overview_page.goes` sets it from the href.
- **Grids.** `.site-cards` fills the track with columns at least 17rem wide: three on a
  desktop, one on a phone.
  `.site-cards-axes` fits the three verification cards, `.site-cards-media` the two
  previews at 20rem, and `.site-cards-single` holds one card across the track.

## The Square Popover

With JavaScript on, a plain click on a card whose link carries `data-popover` opens a
square popover instead of navigating ([popover.js](../overview/popover.js)); a modified
click (a new tab or window) still navigates, and with JavaScript off every card is an
ordinary link.

| `data-popover` | The popover shows | Its button |
| --- | --- | --- |
| `result` | the card, and the record from the results table’s expanded row: the full claim, the records, the next rung | shows the row in the table |
| `page` | the site page, narrowly, in a same-origin frame | opens the page full size |
| `document` | the card’s summary and the document’s opening section, rendered at build time into the card’s `<template class="site-card-preview">` | opens the document on GitHub |

The popover is a modal `<dialog class="site-popover">`, at most 40rem wide, with the
card shadow and a hairline border.
Escape, the close button and a click outside close it, and focus returns to the card.
Its buttons draw KPress’s own `maximize` and `x` icons from the page’s sprite.
Formulas it shows are typeset through `siteMath.typeset`.

## Chips and Rung Badges

One component, `.site-chip`, is every small badge on every page: rungs, novelty,
standing, status and the recent star.

- A chip is a small sans label, medium weight, square, with a dark fill and light text
  in light mode and the reverse in dark mode: its fill is `--site-chip-ink` and its text
  `--kpress-doc-bg`, which swap with the theme.
- `data-tone="muted"` fills it with the muted colour instead, for what is secondary: a
  superseded standing, a novelty label, a dated record.
- `data-wrap` lets a chip whose label is a phrase (a novelty) wrap between its words; a
  chip never breaks inside a word.
- `.site-chip-star` draws the recent star; its word is kept for screen readers.

A rung badge is `<span class="site-chip site-rung" data-axis="v|c|s" data-rung="N">`:
`V` blue, `C` green, `S` grey, each hue pulled toward the muted grey to the chroma of
the packing palette’s blue and green (`sqpack.render.style.SQUARE_HUE_PALETTE`). The
fill moves toward the text colour as the rung rises, by 8% a rung: in light mode it
darkens with the rung, and in dark mode, where the text colour is light, it lightens,
away from the page either way.
Every badge carries the record’s own words for its rung as its tooltip.

## Tables and table.js

The site’s tables are KPress tables (`.kpress-table` in a `.kpress-table-wrap`), in the
table face, with the numeric alignment and the in-table code size KPress gives them.
[table.js](../overview/table.js) adds sorting and filtering to any table that asks, and
the frontier atlas uses it as the overview does.
Its contract:

- **The table** is `<table class="kpress-table site-table" data-site-table id="…">`.
  Every such table on the page is set up when the script runs.
- **Sorting.** A header `<th data-sort="number">` or `<th data-sort="text">` gains a
  button, and each click steps ascending, descending, then back to the page’s own order;
  the header’s `aria-sort` says which, and one column sorts at a time.
  A cell’s sort value is its `data-value`, else its text.
  Numbers compare as numbers and text by locale, digits numerically; an empty value, or
  a non-number in a number column, sorts last in both directions.
- **Groups.** Rows are the `tr` of every `tbody`. A row marked `data-site-table-group`
  heads the rows after it, until the next such row.
  It is hidden when every row it heads is hidden, and while the table is sorted, when
  the rows are listed as one.
- **Filters** live in `<div class="site-table-filters" data-filters-for="<table id>"
  hidden>`, which the script shows.
  A row stays when it passes every control:
  - `<select data-filter="attr">` keeps rows whose `data-attr` equals its value; the
    first option, with the value `""`, keeps all.
  - `<input type="checkbox" data-filter-flag="f">`, when checked, keeps rows whose
    space-separated `data-flags` include `f`.
  - `<input type="number" data-filter-min="attr">` and `data-filter-max="attr"` keep
    rows whose numeric `data-attr` is at least, or at most, the value; a row without the
    attribute is dropped while a bound is set.
    The results table filters on `n` with `data-filter-min="n-max"` and
    `data-filter-max="n-min"`, so a row is kept when its range of cases meets the one
    asked for.
  - An `<output data-filter-count>` in the panel says how many rows show.
- **Expandable rows** are a `<details>` in a cell; its summary is set in the table’s own
  sans, never as KPress’s caps disclosure label.
  A row the fragment names has its details opened.
- **With JavaScript off** every row is in the page in its order, every details element
  opens, and the filter panel stays hidden.

The rest is presentation:

- `.site-table-fixed` lays a table out by its header, every column but one at a set
  width (`th.site-col-*`), so a long formula wraps in its own column rather than
  widening the table; below its minimum the wrap scrolls.
- `.site-table-scroll`, on the wrap, caps it at 85% of the viewport’s height and keeps
  the header row in view, for a long table.
- A code span in a table (an evidence id, a file name) never breaks at its hyphens.
- `.site-thumb` marks a drawing loaded as an `<img>` (the frontier thumbnails); under
  the dark theme it is given `color-scheme: dark`, which is what switches its outlines
  to the light ink, since an image does not inherit the page’s theme.
- The row a fragment targets is marked with the selected surface.

## Mathematics

**Math matches its text.** Serif prose sets its formulas in the serif math face and sans
text in the sans one.
The runtime decides from the formula’s surroundings: KPress sets every formula inside a
`<details>`, a `.kpress-table` or a `.sans-text` block in the sans face, and the
explainer’s host adapter (`squaresMath`) does the same wherever the surrounding text’s
computed face is the sans.
So every site component whose text is sans (cards, tables and their summaries, chips,
the popover) sets its formulas in the sans face, and a table summary is sans throughout.
Formulas in generated blocks are written in KPress’s own markup by
`overview_page.math_html`, the TeX for KaTeX beside MathML for readers without
JavaScript.

**Punctuation keeps its line.** A formula is an inline box, and a line may break between
it and a colon or comma after it.
The overview puts a word joiner there (`overview_page.keep_punctuation`), which forbids
that break without stopping the formula breaking at its relations as
`white-space: nowrap` would; `.site-nowrap` and `.frontier-decimal` are for text that
must not wrap at all.

**Typesetting is lazy** ([site-math.js](../overview/site-math.js)). A formula costs the
runtime a dozen milliseconds or more, and the frontier atlas has hundreds, so a formula
is set when it comes within 1,200 pixels of the viewport, and a formula inside a closed
`<details>` when the reader opens it.
Until then the reader has KPress’s MathML. A print sets every formula first, and
`siteMath.typeset(root)` sets every formula under one element at once.

**`math-ready`** is added to `<html>` once every formula that has a box within 1,200
pixels of the viewport when the page opens has been set: what the reader can see, and a
screen or two beyond it, is typeset.
It does not mean every formula on the page is set.
A check that reads every formula’s face calls `siteMath.typeset(document)` after
`math-ready` and waits for it, which sets the rest, closed rows included;
`devtools.preview_site` does this before its face walk and its screenshots.
The explainer keeps its own `page.js` and its own meaning of the class.

## Media

The atlas previews, the film and its links sit inside one element marked
`data-site-media`, and every `href`, `src` and `poster` inside it is site-relative: the
published-site media check requires it there, since the files are served by Pages with
the right media types and a release download or a GitHub page is not.
The film is one `<video>` with native controls, `preload="none"`, its poster frame and
no autoplay, so nothing is downloaded until a reader presses play; its caption links the
MP4 itself.

## Print

The navigation bar, the footer, the popover and the filter panel are hidden.
Cards do not break across pages and lose their hover icons, a chip prints as an outlined
label rather than a filled one, and the film is left out.
KPress’s own print reset takes the colours to black on white.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
