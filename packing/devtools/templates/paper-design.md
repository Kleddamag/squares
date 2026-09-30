# Design System

This is the one description of how every page of the site looks: the explainer, the
overview, the frontier atlas and the tutorial.
Each stylesheet implements what is written here and points back to it; when a page needs
something new, it is added here first and then to the stylesheet that owns it.

Three layers carry it, from the bottom up:

| Layer | File | Owns |
| --- | --- | --- |
| KPress | `vendor/kpress` | Fonts, Markdown typography, math, themes, print |
| Paper | [explainer-shell.html](explainer-shell.html) | The explainer’s type proportions, reading measure and figures |
| Site | [site.css](site.css), [site-nav.css](site-nav.css) | Site pages and the navigation bar every page carries, the explainer included |

The paper and site layers use the same values under their own prefixes, `--paper-` and
`--site-`, so a site page and the explainer set a role at the same size and weight.
Every site value is a KPress token or derived from one, so it follows the theme and the
print rules.

The explainer uses serif prose for sustained reading and sans serif text for figures,
captions, notes, and controls.
The web page and PDF share this hierarchy, with sizes scaled for each medium.
[explainer-article.md](explainer-article.md) contains the explainer’s article.

## Typography Roles

Sizes below are the CSS values for each medium.
Compare the final PDF when absolute point sizes matter: browser print scaling can change
physical sizes.

| Role | Web | Print | Treatment |
| --- | --- | --- | --- |
| Prose | 18px | 12pt | Serif, with KPress prose emphasis |
| Sans base | 19px | 12⅔pt | A size ratio of 19/18 against prose |
| Main title | 28.5px | 19pt | Sans, 1.5 of the sans base |
| Subtitle | 23.75px | About 15.8333pt | Sans caps, 1.25 of the sans base |
| Title credits and date | 19px | 12⅔pt | Sans base size |
| Section headings | 21.6px | 14.4pt | Serif italic, 1.2 of the prose base |
| Figure labels and controls | 18.05px | About 12.0333pt | Sans, 0.95 of the sans base |
| Captions and end footnotes | 17.48px | About 11.6533pt | Shared sans size: 0.92 of the sans base; 1.4rem side inset |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
| Sans weights | 410 regular, 550 medium, 680 bold | Same | Preserve serif weight settings |
| Supporting text color | KPress gray text role | Solid black | Preserve semantic diagram and status colors |

Figure labels retain their readable size; captions and end footnotes use a slightly
smaller shared size and inset on both sides.
Screen theme colors still apply in both light and dark mode.
Print uses a white ground and black prose, labels, captions, and notes; semantic diagram
colors retain their meaning.
Links have no persistent underline on the web or in print.
Links within supporting text inherit its gray or black; links in the main prose retain
the accent color. Caption leads use bold weight to distinguish the figure number without
changing its size or color.

## Color

One accent, the teal `--kpress-doc-accent`, is the only link and emphasis color:
`oklch(51.09% 0.0861 186.4)` in the light theme and `oklch(76.68% 0.0861 186.4)` in the
dark. Both the paper and site layers alias KPress’s separate link blue to it.
Supporting text uses KPress’s gray (`--kpress-doc-muted`, carried as
`--site-support-color`) on the web and black in print.

The packing palette is the fixed set of square fills in `SQUARE_HUE_PALETTE`
(`packing/src/sqpack/render/style.py`), shaded by contact count in the figures.
Page colors that are not the accent are desaturated shades of it:

| Use | Hue | Chroma | Source in the palette |
| --- | --- | --- | --- |
| Verification rung (`V`) | 250 | 0.08 | The blue square, `#166eac` |
| Confirmation rung (`C`) | 158 | 0.08 | The green square, `#158655` |
| Significance rung (`S`) | 250 | 0.008 | Gray |

Every chip carries light text on a dark fill, and in dark mode dark text on a light
fill: its text is the page’s background colour.
A rung’s fill is `oklch(base + step × level, chroma, hue)` for levels 0 to 5, with base
50% and step −4% in light mode, so it darkens from 50% to 30% as the rung rises, and
base 75% and step +4% in dark mode, so it lightens from 75% to 95%. The two are
`--site-rung-base` and `--site-rung-step`. The recent-bound star is the one warm mark,
`oklch(52% 0.19 25)`.

Every hover, a table’s group row and a targeted row take one gentle wash, `--site-wash`,
defined in `site-nav.css` because every page carries it: KPress’s hover surface in light
mode, and a 9% tint of the text in dark mode, where KPress’s own is a light gray that
light text cannot sit on.

## Math

Math takes the face of the text around it: serif math in serif prose, sans math in sans
text.
KPress chooses the face from a fixed list of sans contexts (a table, a `<details>`,
a caption, a footnote), so a site style must not set text inside one of those contexts
in the serif face, or the other way round; set the text in the face KPress will pick for
its math. The outer math em follows the surrounding text in inline and display formulas;
KaTeX still controls the internal sizes of scripts and nested expressions.
Documents write math as LaTeX (`$…$`) rather than in code spans;
`devtools.check_math_markup` holds the documents already migrated to it.
Code uses Planetaire Mono Text at KPress’s calibrated monospace size.

## Site Components

Each component is defined once in [site.css](site.css) and used on every page that needs
it.

- **Navigation bar.** One fixed-width row of sans links in the page’s header slot, the
  same on every page, led by the site name, “Square Packing”, set in capitals by CSS
  (`text-transform`, lightly tracked) so its text is unchanged, and a step heavier.
  Every item takes the cards’ gentle wash on hover and nothing underlines on hover; the
  current page alone is underlined in the accent.
  The edition appears only in the closing line.

- **Theme control.** A small gray gear, an inline SVG, ends the navigation bar on every
  page, the explainer included.
  It takes the nav items’ wash on hover and while its menu is open, and never
  underlines. Pressing it opens a compact menu, a native popover under the gear with
  square corners and the cards’ border and shadow, of three choices, each an icon and a
  word: System, Light and Dark.
  The current choice is in the accent with a check at its end.
  Choosing applies at once, closes the menu and keeps the choice across pages and
  visits; the menu also closes on Escape, an outside click or tabbing away.
  The gear is a button named “Color theme” with `aria-haspopup="menu"` and
  `aria-expanded`; the menu is a `role="menu"` of `menuitemradio` items carrying
  `aria-checked`, and the arrow keys, Home and End move between them.
  On a phone the whole bar wraps onto centred lines, so every link stays in view, and
  the gear ends the last line.
  The choice is KPress’s own reader preference, the `kpress.theme` key its head
  bootstrap applies before first paint, so no page flashes the wrong theme and every
  stylesheet keys only on `data-kpress-resolved-theme`, never on `prefers-color-scheme`.
  System follows the operating system as it changes.
  The embed view has no navigation bar and so no gear, and a framed page follows the
  choice its parent makes, live.
  `overview/theme.js` is the script, and it announces a change as `squares:themechange`
  for anything drawn on a canvas.
  Adapted from metabrowser’s settings gear, reduced to one chooser with words beside its
  icons.

- **Page headings.** The homepage has no title heading: its hero picture leads, and its
  sections are `h2`s.

- **Report layout.** Every report page (the tutorial, the synopsis and the other
  documents) has one layout.
  A long report gets a contents rail and a short one does not, by kpress’s own rule
  (seven headings and 800 words), so the choice is never made per page.
  Either way the reading column is centred.

- **Document pages with contents.** On a wide screen the contents rail stays at the left
  edge and the reading column is centred on the page, under the centred navigation.
  Where the pane is too narrow to centre, the column sits as near centre as the 15rem
  rail allows. The rail is plain text: no frame, only the underlined Contents label, and
  entries that change colour on hover or when current, with no fill or side bar.

- **Site icon and hero.** Both are atlas drawings, reduced to each square’s outline and
  fill. The icon is case 11, the central open case, in the atlas ink on white, inlined as
  a data URI on every page.
  The homepage’s hero is case 53, centered under the title in the page’s ink and linked
  to its row in the frontier atlas.

- **Cards.** A card is a summary with square corners, a thin border, a caps label, a
  value and a supporting note.
  Every card works the same way: pressing it opens a popover that shows where it leads,
  and the popover ends in one button that goes there.
  - When the card leads to another page of the site, the popover renders that page
    itself, narrow, in a frame: the page at the same address with `?view=embed` added
    before any fragment, so a filtered view such as `frontier.html?recent=true` or a
    case such as `frontier.html#n-11` arrives as it will be seen.
    The embed view drops the navigation bar and sends every link out of the frame to the
    full window. The button is **Expand**, which opens the page at full size; a
    repository document also offers its source “On GitHub”, which opens it on `main`.
    Every repository link on the site names `main`, never a commit, and is made by
    `devtools/repo_links.py`.
  - When the card leads off the site, as an other project’s card does, the popover
    previews the repository and its author, and the button opens it.
  - When the card leads to a row on this page, the popover previews the row, read from
    the same record: a result’s claim, why it matters, its rungs and records.
    The button shows the row in the table.

  The frame loads only when its popover first opens, so the overview stays light.
  The popover is a native `popover` panel with square corners over a faint scrim, set in
  sans, closed by its `×`, by Escape, or by a click outside, and it works without
  scripting. A card gains a gentle wash on hover.
  Its gray corner icon and the popover’s button both show where the button goes: `↓` to
  a row on this page, `↗` off the site, `→` to another page of the site.

- **Chips.** Every small label is one `.site-chip`: square corners, the sans face at the
  note size, a solid fill and no border, lettered in the page’s background colour.
  A plain chip is the muted gray; `data-tone="accent"` is the accent, for a settled
  state such as a proved case.
  A rung chip adds `.site-rung-fill` with `data-rung` and `data-level`. A standing chip
  carries `data-standing` and adds no style of its own: `holds` takes the accent, as a
  settled state, and every other standing (`holds, reported`, `second certificate`,
  `superseded`, `not a bound`) the plain gray, so a reader sees which results still hold
  without the others shouting.
  A novelty chip (`data-novelty`) is always plain gray.

- **Dimension cards.** Verification at a Glance is one card per scored dimension of the
  rubric, Verification, Confirmation and Significance: the question it answers, then
  every level as its chip and the rubric’s meaning, read from the tables in
  `epistemics.md`. Each opens that section of `epistemics.md`.

- **Atlas grid.** The atlas opens with every tracked case, n = 1 to 324, as a small
  square drawing in the page’s ink with its n beneath, in as many columns as fit.
  A cell washes on hover and opens its case record.
  Pointing at or focusing a cell shows one hover card below it, kept inside the window:
  the status chip, the best-known side and the lower bound, each with its credit.
  The cells ship in a `<template>` and are placed only as the grid nears the viewport
  (`overview/atlas-grid.js`), so they add nothing to the first paint.

- **Case records.** Every case has one record at one address, `cases.html#n-11`, and
  every place that names a case by its n opens it the same way: a cell of the atlas grid
  and the n of a frontier-atlas row.
  A press opens the one case popover the page carries, a page-kind popover framing the
  record in its embed view, with **Expand** to the full record
  (`overview/case-popover.js`); without scripting the link goes to the record itself.
  A record leads with a caps label, the n, its status chip and recent star, and the
  verified interval as display-size math; then the known-best packing drawn large beside
  a grid of bordered sans panels, one per bound (best known, verified upper, reported
  lower, verified lower) and the gap.
  Each panel shows its value as math when it has a closed form (a lone fraction at full
  size) and as figures when it is a decimal, the recorded decimal in full beneath, then
  its credit, source, minimal polynomial as math and evidence.
  Below come the register’s results for the case, each a line with its rungs as chips,
  then rigidity, open questions, evidence and sources, the links to the frontier row and
  to the case file “On GitHub”, and the case file’s own prose, whose formulas are set as
  LaTeX. The records share one page, since every page inlines the shell: the page shows
  only the record its fragment names (`overview/case-view.js`) and typesets that
  record’s math when it is shown; without scripting it lists every record.

- **Atlas posters.** The n = 1 to 100 and n = 1 to 324 posters sit side by side, stacked
  on a phone. Each image and its caption link to that poster’s PDF, marked
  `type="application/pdf"` and never `download`, so the browser opens it in place.
  Under them, across both columns, the n = 1 to 324 film plays by itself: muted,
  looping, inline and with its controls, held still on its first frame for a reader who
  asks for reduced motion (`overview/film.js`).

- **Tables.** KPress tables in the sans face, with sortable headers, filters above,
  group rows, and an expandable row whose summary stays sans so its math does.
  On a phone, the results table becomes one card per row.
  In the results table a result’s standing chip sits under its rungs, and a Standing
  filter selects by it; a date cell says what it dates, `published` or `established`, in
  the support colour.

- **Awaiting replay.** Under the recent list, a closed disclosure in the sans face at
  the note size: its summary names how many cases and the range, and it opens a compact
  table grouped by holder and the entries carrying the claim, each case linking to its
  row in the frontier atlas.

## Token Ownership

KPress owns the regular sans weight in `--kpress-font-weight-sans-regular`. Its font
generators read that token to produce matching math metrics and print faces; the paper’s
CSS and print instancer use the same source.
Change that token and regenerate the fonts, metrics, and prepared page together.
The loading and generation contract is documented in the
[KPress font and math architecture](../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md).

The local typography block owns the sans/prose size ratio and the paper’s medium and
bold weights. `--paper-font-size-support` sizes figure labels; `--paper-font-size-note`
and `--paper-note-inset` size and inset captions and endnotes.
They share `--paper-support-color` and `--paper-support-leading`. Resolve the sans base
once in the prose scope: nested sans components must inherit the resolved size without
multiplying the ratio again.
Apply print overrides at the same scopes as KPress theme declarations, including
footnote popovers.

The paper’s role sizes, heading scale, and reading measure remain explicit local
choices. Certificate selection, interactive panels, and diagram geometry stay with the
explainer.

An SVG’s declared font size is in its own coordinate system.
Audit the effective size after its `viewBox` and rendered dimensions scale the drawing;
matching a CSS number alone does not match the intended label size.
The shared script compensates font sizes using the SVG transform and updates them on
resize and when entering or leaving print.
Label rows leave room for the resulting text size.
On narrow screens, diagrams scroll horizontally rather than shrinking their labels.
Long figure notes remain HTML so they can wrap.

The 100-packing atlas is an explicit exception: it is a standalone SVG with its own
dense grid, title, and labels.
Enlarging every internal label to the figure-label size would obscure its cells.
Its caption uses the shared role; the linked full-size PDF provides the detailed view.

## Print and Verification

Print uses Letter paper with 1.25-inch side margins and 0.75-inch top and bottom
margins, ragged-right prose, embedded reading fonts, and fractional glyph advances.
The title has extra top padding; page numbers sit inside the bottom margin and are
omitted on the first page.
Supporting text uses 1.4 line-height on the web and 1.32 in print.
Print source notes use compact list spacing and a 1.5rem gap before the colophon to keep
the closing credit on the same page.
Set the print SVG width before pagination so its font measurements match the exported
page. Interactive controls disappear, the default certificate determines the printed
figures, and the atlas occupies its own page.
Preserve the hierarchy when adjusting page breaks or figure dimensions.

From `packing/`, render and check the result:

```shell
uv run --frozen --all-extras --group dev python -m devtools.render_explainer --prepare-math
uv run --frozen --all-extras --group dev pytest tests/test_explainer.py -q
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --check-math --theme light
uv run --frozen --all-extras --group dev python -m devtools.inspect_explainer_typography --check-supporting --check-math --theme dark --width 390
uv run --frozen --all-extras --group dev python -m devtools.check_print_layout
uv run --frozen --all-extras --group dev python -m devtools.render_explainer_pdf --update
```

The typography check compares ordinary captions and endnotes with their shared role, and
figure labels with theirs, including effective SVG sizes.
It reports overlapping SVG label boxes and persistent link underlining.
Math and code have separate context and baseline inventories; semantic status labels
retain their distinct treatment.
Inspect the rendered page in both themes and the exported PDF, and check page breaks
after changing type size.
The generated editions live in `packing/site/`; publication and broader validation
requirements are in [development.md](../../../development.md).

The site pages are checked together by building the whole site and screenshotting every
page at a desktop and a phone width:

```shell
uv run --frozen --all-extras --group dev python -m devtools.preview_site --shots /tmp/shots
```

It fails on console errors, a page wider than its viewport, math left untypeset, and any
formula whose face disagrees with the text around it.
`tests/test_overview.py` holds the cards and chips to the rules above.

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
