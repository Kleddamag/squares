# Design System

This is the one description of how every page of the site looks: the explainer, the
overview, the frontier atlas, the papers page, the tutorial and the Visualize section.
Each stylesheet implements what is written here and points back to it; when a page needs
something new, it is added here first and then to the stylesheet that owns it.

Three layers carry it, from the bottom up, with the paper’s text tokens shared by all:

| Layer | File | Owns |
| --- | --- | --- |
| KPress | `vendor/kpress` | Fonts, Markdown typography, math, themes, print |
| Text | [paper-type.css](paper-type.css) | The type base, reading measure, heading scale, role scales and pinned faces every page shares |
| Paper | [explainer-shell.html](explainer-shell.html) | The explainer’s figures, panels and print rules |
| Site | [site.css](site.css), [site-nav.css](site-nav.css) | Site pages and the navigation bar every page carries, the explainer and the workbench included |

The paper and site layers read the same values from `paper-type.css`, under their own
prefixes, `--cert-` and `--site-`, so a site page and the explainer set a role at the
same size and weight.
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
| Heading leading | 1.15 | KPress’s 1.2 | `--paper-heading-leading`: every heading, a card’s and a popover’s headline, and a page’s subtitle; the explainer’s hero title keeps KPress’s 1.05 |
| Space above a section heading | 48.6px | 37.8pt | `--paper-section-space`: 2.7 of the prose base on screen, 2.8 in print |
| Space below a section heading | 27.2px | 15.6pt | `--paper-section-space-below`: 1.7rem on screen, 1.3rem in print |
| Figure labels and controls | 18.05px | About 12.0333pt | Sans, 0.95 of the sans base |
| Captions and end footnotes | 17.48px | About 11.6533pt | Shared sans size: 0.92 of the sans base; 1.4rem side inset |
| Colophon | 16.15px | About 10.7667pt | Sans, 0.85 of the sans base |
| Navigation links and section tabs | 17.48px | Not printed | Sans medium at the caption size, 0.92 of the sans base: one step under the prose |
| Site name in the bar | 19px | Not printed | Sans bold caps at the sans base |
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
Page colors that are not the accent take their hues from it:

| Use | Hue | Chroma | Source in the palette |
| --- | --- | --- | --- |
| Verification rung (`V`) | 250 | Rises with the level | The blue square, `#166eac` |
| Confirmation rung (`C`) | 158 | Rises with the level | The green square, `#158655` |
| Significance rung (`S`) | 250 | 0.008 at every level | Gray |

Every chip carries the page’s own text colour, black in light mode, on a light fill, and
in dark mode light text on a dark fill.
A plain chip is a 16% tint of the muted gray over the page background, and an accent
chip a 22% tint of the accent.

### The Rung Scale

A rung’s fill is one rule,
`oklch(base + step × level, chroma-base + chroma-step × level, hue)`, so its saturation
and its strength both rise with the level: level 0 is nearly the page background, and
the top rung is the most saturated and the furthest from it.
Four tokens set the scale in each theme, and the two ladders that carry a hue share
them:

| Token | Light | Dark |
| --- | --- | --- |
| `--site-rung-base`, the lightness at level 0 | 95% | 25% |
| `--site-rung-step`, what a level adds to it | −5.5% | +4.6% |
| `--site-rung-chroma-base`, the chroma at level 0 | 0.015 | 0.012 |
| `--site-rung-chroma-step`, what a level adds to it | 0.024 | 0.019 |

Significance is gray by design: it takes the lightness steps and no chroma step, so a
higher level is darker in light mode and lighter in dark, never coloured.
No chip has a value of its own; a level’s fill is always these tokens at that level.

The text is the page’s own at every step, with no switch to a second text colour: the
scale stops where that text still reads.
Every fill is inside sRGB, so a browser shows the chroma written here, and the text’s
contrast on it is 6.0:1 or better in light mode and 5.3:1 or better in dark, against the
4.5:1 that WCAG AA asks of body text.
The fills and ratios below are what `devtools.rung_scale` computes from the tokens in
`site.css` and KPress’s page colours; run it after changing a token.
`tests/test_rung_scale.py` holds this table to its output, the order to monotonic, and
every ratio to 4.5:1.

| Rung | Light fill | Text contrast | Dark fill | Text contrast |
| --- | --- | --- | --- | --- |
| `S1` | `oklch(89.5% 0.008 250)` `#d8dde2` | 13.0:1 | `oklch(29.6% 0.008 250)` `#2a2d31` | 11.7:1 |
| `S2` | `oklch(84.0% 0.008 250)` `#c7cbd0` | 10.9:1 | `oklch(34.2% 0.008 250)` `#35393d` | 9.9:1 |
| `S3` | `oklch(78.5% 0.008 250)` `#b5b9be` | 9.0:1 | `oklch(38.8% 0.008 250)` `#414549` | 8.2:1 |
| `S4` | `oklch(73.0% 0.008 250)` `#a4a8ad` | 7.4:1 | `oklch(43.4% 0.008 250)` `#4e5155` | 6.8:1 |
| `S5` | `oklch(67.5% 0.008 250)` `#93979c` | 6.0:1 | `oklch(48.0% 0.008 250)` `#5a5e62` | 5.5:1 |
| `V0` | `oklch(95.0% 0.015 250)` `#e7f0f8` | 15.4:1 | `oklch(25.0% 0.012 250)` `#1d2227` | 13.6:1 |
| `V1` | `oklch(89.5% 0.039 250)` `#cadff6` | 13.0:1 | `oklch(29.6% 0.031 250)` `#212e3c` | 11.7:1 |
| `V2` | `oklch(84.0% 0.063 250)` `#accef3` | 10.9:1 | `oklch(34.2% 0.050 250)` `#243a51` | 9.9:1 |
| `V3` | `oklch(78.5% 0.087 250)` `#8ebeef` | 9.1:1 | `oklch(38.8% 0.069 250)` `#264768` | 8.2:1 |
| `V4` | `oklch(73.0% 0.111 250)` `#70adeb` | 7.5:1 | `oklch(43.4% 0.088 250)` `#27537f` | 6.7:1 |
| `V5` | `oklch(67.5% 0.135 250)` `#4f9be6` | 6.1:1 | `oklch(48.0% 0.107 250)` `#266097` | 5.5:1 |
| `C0` | `oklch(95.0% 0.015 158)` `#e7f2eb` | 15.4:1 | `oklch(25.0% 0.012 158)` `#1d231f` | 13.5:1 |
| `C1` | `oklch(89.5% 0.039 158)` `#c8e5d3` | 13.2:1 | `oklch(29.6% 0.031 158)` `#1f3227` | 11.6:1 |
| `C2` | `oklch(84.0% 0.063 158)` `#a9d8bb` | 11.1:1 | `oklch(34.2% 0.050 158)` `#20402e` | 9.7:1 |
| `C3` | `oklch(78.5% 0.087 158)` `#88caa4` | 9.3:1 | `oklch(38.8% 0.069 158)` `#1f5036` | 7.9:1 |
| `C4` | `oklch(73.0% 0.111 158)` `#65bd8d` | 7.8:1 | `oklch(43.4% 0.088 158)` `#1a5f3e` | 6.5:1 |
| `C5` | `oklch(67.5% 0.135 158)` `#3aaf76` | 6.4:1 | `oklch(48.0% 0.107 158)` `#0f6f46` | 5.3:1 |

The recent-bound star is the one warm mark, `oklch(52% 0.19 25)`.

Every hover, a table’s group row and a targeted row take one gentle wash, `--site-wash`,
defined in `site-nav.css` because every page carries it: KPress’s hover surface in light
mode, and a 9% tint of the text in dark mode, where KPress’s own is a light gray that
light text cannot sit on.

## Text

Every page sets its reading text as the explainer does, from one file,
[paper-type.css](paper-type.css), which the explainer’s shell, every KPress page and the
Visualizer’s navigation shell inline right after KPress’s stylesheets.
No page declares these tokens itself; `tests/test_overview.py` fails a layer that does,
and `tests/test_site_text_tokens.py` pins what they resolve to in Chromium.

| Token | Value | Resolves to |
| --- | --- | --- |
| `--kpress-host-font-size-base` | `18px` | Every KPress size, from `--kpress-font-size-base` |
| `--kpress-measure` | 40 of the base | 720px, the width KPress’s default 45 gives at 16px |
| `--kpress-font-size-h2` | 1.2 of the base | 21.6px at every width; KPress steps it to 1.4 from a 64rem pane |
| `--paper-font-scale-sans` | 19/18 | The 19px sans base of captions, cards and notes |
| `--paper-font-weight-sans-medium`, `-bold` | 550, 680 | The sans medium and bold |
| `--paper-title-scale`, `-subtitle-`, `-support-`, `-note-`, `-colophon-` | 1.5, 1.25, 0.95, 0.92, 0.85 | The roles in the table above |

What a reader sees, measured with `devtools.measure_site_pages type` on the explainer,
the tutorial, the readme and the homepage, identical on all four where the role occurs:

| Role | Face | Size / line height at 1280px | At 390px |
| --- | --- | --- | --- |
| Paragraph and list item | PT Serif | 18 / 27px | Same |
| h1 (a report’s title) | PT Serif | 30.6 / 36.72px (1.7 of the base) | Same |
| h2 | PT Serif italic | 21.6 / 25.92px | Same |
| h3 | Source Sans 3, 550 | 21.6px | 20.7px |
| h4 | Source Sans 3 italic, 540 | 21.6px | 20.16px |
| Table cell | Source Sans 3, 410 | 17.1px | 16.2px |
| Inline code | Planetaire Mono Text | 14.76 / 22.14px | Same |
| Inline math | KPress Math Text (serif) | 18px, the text’s own em | Same |
| Text line | — | 800px: the measure and both 2.5rem insets | The column less the page margin |

h3 and h4 keep KPress’s own step up at a 64rem pane.
The explainer’s title is its own role (sans caps, 28.5px); a report’s h1 is the Markdown
title and keeps KPress’s ratio of the same base.
The homepage sets its summary lists and tables a step smaller, in `site.css`.

**Faces.** Every page inlines byte-identical `@font-face` blocks (PT Serif and its
punctuation face, Source Sans 3, Planetaire Mono Text, the KaTeX faces and KPress’s math
composites), because every page takes them from the same functions,
`render_explainer.kpress_css`, `katex_css` and `relation_face_css`;
`devtools.measure_site_pages faces` compares them block by block.
KPress leads each family token with an embedding host’s hook, `--kpress-host-font-sans`
and its siblings, so an application embedding a KPress fragment can supply its own face.
The site does not honor those hooks: a viewer that injects one would draw the page in a
face it does not ship, which is the rule every text run here is held to.
`paper-type.css` sets each hook to `initial`, important, on KPress’s own scopes, so
KPress’s stack, led by the inlined face, always applies.
A reader’s own choice of system fonts still works: KPress’s `data-kpress-font-set`
switch sets the family tokens themselves, not the hooks.
Its system stack (`style-tokens.css`, the block for `[data-kpress-font-set="system"]`)
applies only under that attribute, which only a saved reader preference stamps.

## Math

Math takes the face of the text around it: serif math in serif prose, sans math in sans
text.
KPress chooses the face from a fixed list of sans contexts (a table, a `<details>`,
a caption, a footnote), so a site style must not set text inside one of those contexts
in the serif face, or the other way round; set the text in the face KPress will pick for
its math. The outer math em follows the surrounding text in inline and display formulas;
KaTeX still controls the internal sizes of scripts and nested expressions.
One exception: a headline that is mathematics standing alone, such as $n = 11$, is set
in the serif face, on a card, in a popover and in any heading, though the headline’s own
face is sans. A headline with words in it, such as “Earlier $n = 11$ lower bounds”, is
not one: its math follows the words into the sans.
The exception’s element is marked `data-math-face="serif"`, which the host adapter’s
sans test (`host_math_init.js`) honours before it reads the surrounding face.
`overview_sections.headline_math_face` marks a card’s headline and its popover’s when
the value is all math, and the two headlines a script fills with $n = N$, the atlas
popover’s and the case popover’s, carry the mark in their markup.
Popovers carry no `data-kpress-prose-font` mark, so every other formula in them follows
its own text. The rule holds on every surface, walked formula by formula on the built
site: a card’s headline and note, a popover and the atlas popover, a table’s cells,
heads, summaries and disclosures, a caption, a footnote, a case record’s head, panels
and detail, a page’s subtitle, and a sans heading are sans text with sans math; prose
and its lists are serif with serif math.
A card’s headline and note are prose whose mathematical runs are set as math, so a case
a note names, such as $n = 21$, is sans math too, never upright words.
Documents write math as LaTeX (`$…$`) rather than in code spans;
`devtools.check_math_markup` holds the documents already migrated to it.
Code uses Planetaire Mono Text at KPress’s calibrated monospace size.

## Math Loading

Every page loads its mathematics through the explainer’s pipeline, from the same code:

- **Faces and styles.** KaTeX’s faces pruned to those a page can reach, inlined as data
  URIs and switched from `font-display: swap` to `block`, so no formula is drawn in a
  host face and redrawn; KPress’s math composites; the three relation glyphs
  (`relation_face_css`).
- **Scripts.** `render_explainer.katex_js`: KaTeX, KPress’s metric tables and shared
  runtime, and the explainer’s host adapter, `squaresMath`
  (`probes/render_explainer/host_math_init.js`). KPress’s own entry points,
  `auto-render.min.js` and `katex-init.js`, are left out: `katex-init.js` typesets every
  formula on the page in one task at DOMContentLoaded.
- **Per-formula readiness.** The runtime lays a formula out hidden, waits for the faces
  its glyphs need, and reveals that formula alone; a formula whose faces fail keeps its
  readable fallback.
- **Batching.** `squaresMath.batch` submits sixteen formulas per task, so a formula that
  is ready shows while later ones are still being submitted.

The explainer adds what only a single published page can: its formulas are typeset,
measured and written into the HTML at publication (`render_explainer --prepare-math`),
so the client hydrates rather than lays out, and its queue puts the interactive panels
first. The KPress pages are rendered without a browser, so they typeset in the client,
driven by `overview/math.js`: the formulas within two screens of the viewport first, the
rest as the reader scrolls toward them or opens what hides them, and, once the page has
loaded, one at a time in the browser’s idle time.
A formula whose faces missed the runtime’s wait is retried twice after the page and its
fonts load, which a long page needed when every face decoded at once.
Both mark the end of their load-time work with `math-ready`.

Each client layout costs a style pass over the whole document, 6ms a formula on the
synopsis against 0.9ms with KPress’s `:has(.kpress-toc)` layout rules removed: those
selectors make every change inside the column re-match the page’s grid.
The rules are KPress’s, so the fix belongs upstream (a class stamped by the renderer,
which KPress already accepts as `.has-toc`, tracked as think-csiv); until then the
synopsis’s 1,357 formulas cost about eight seconds of idle time in all.

`devtools.measure_site_pages load` measures a built site in cold Chromium contexts
(median of three loads, milliseconds from navigation start; “visible math” is the first
frame at which every formula in the first viewport is typeset and showing, “blocking”
the long tasks’ time over 50ms). Before is the site at `3e8274909`, after is this
pipeline:

| Page | Width | DOMContentLoaded | Visible math | Load-time math done | Longest task | Blocking |
| --- | --- | --- | --- | --- | --- | --- |
| `explainer.html` | 1280 | 712 → 993 | 727 → 1,008 | 947 → 1,238 | 132 → 128 | 211 → 263 |
| `tutorial.html` | 1280 | 2,233 → 594 | 2,235 → 595 | 2,458 → 741 | 1,875 → 198 | 2,101 → 182 |
| `synopsis.html` | 1280 | 14,040 → 1,089 | 14,704 → 1,668 | 14,704 → 1,758 | 13,002 → 847 | 16,123 → 1,179 |
| `results.html` | 1280 | 568 → 236 | 600 → 387 | 600 → 387 | 82 → 75 | 32 → 25 |
| `readme.html` | 1280 | 608 → 233 | 642 → 297 | 642 → 322 | 74 → 98 | 28 → 48 |
| `index.html` | 1280 | 3,331 → 686 | 3,595 → 811 | 3,595 → 903 | 2,152 → 152 | 2,507 → 219 |
| `cases.html#n-11` | 1280 | 7,958 → 5,362 | 8,106 → 5,386 | 8,106 → 5,509 | 3,773 → 2,399 | 7,247 → 4,130 |
| `explainer.html` | 390 | 696 → 1,156 | 710 → 1,171 | 932 → 1,421 | 121 → 128 | 205 → 263 |
| `tutorial.html` | 390 | 2,336 → 651 | 2,338 → 652 | 2,541 → 743 | 1,924 → 191 | 2,163 → 175 |
| `synopsis.html` | 390 | 14,969 → 1,361 | 15,657 → 1,363 | 15,657 → 1,525 | 13,922 → 326 | 17,132 → 880 |
| `results.html` | 390 | 166 → 190 | 214 → 240 | 214 → 240 | 79 → 87 | 29 → 37 |
| `readme.html` | 390 | 213 → 202 | 278 → 276 | 278 → 285 | 75 → 79 | 29 → 29 |
| `index.html` | 390 | 2,455 → 775 | 2,687 → 855 | 2,687 → 897 | 1,940 → 236 | 2,198 → 248 |
| `cases.html#n-11` | 390 | 8,118 → 5,100 | 8,266 → 5,190 | 8,266 → 5,275 | 3,925 → 2,566 | 7,416 → 3,810 |

“Load-time math done” is the frame at which every displayed formula is typeset or, on a
page that defers the rest, the frame that page marks `math-ready`. The explainer’s own
output changed only by its stylesheet, so its row is the run-to-run noise of the shared
host the two runs were measured on, a few hundred milliseconds; an earlier run of the
same after-build measured it at 705 to 743ms.

The case records page (`cases.html`) is still slow before any math runs: it carries
every case’s record in one 9MB document, and parsing and styling that takes several
seconds on its own (think-cy3a). Publication-time preparation for the KPress pages,
which would remove the client layout and the fallback-to-KaTeX reflow as it did for the
explainer, is not done: it needs a browser in the pages’ build (think-89lw).

## Spacing

The vertical space between a page’s blocks is set on screen by a few tokens, each
declared once and read wherever that space occurs.
Print keeps KPress’s spacing and the paper’s, so the explainer’s PDF does not move when
one of them changes.

| Space | Token | Screen value | Declared in |
| --- | --- | --- | --- |
| From the bar’s rule to a page’s first block, or from the section tabs where a page has them | `--site-page-top` | 4rem, 64px | `site-nav.css` |
| From the bar’s rule to the section tabs, and from them to an application | `--site-tabs-space` | 0.7rem, 11.2px | `site-nav.css` |
| How much nearer the bar an opening picture starts | `--site-hero-lift` | 0.5rem, 8px | `site.css` |
| Above a section heading (`h2`) | `--paper-section-space` | 2.7 of the prose base, 48.6px | `paper-type.css` |
| Below a section heading (`h2`) | `--paper-section-space-below` | 1.7rem, 27.2px | `paper-type.css` |
| Below a page’s title, and below its subtitle | `--site-subtitle-space` | 1.5rem, 24px | `site.css` |
| Above and below a table | `--site-table-space` | 2rem, 32px | `site.css` |
| Between a wide block and the edge of the page’s content area | `--site-wide-gutter` | 0.5rem, 8px | `site.css` |

A page’s title, or the picture that opens the homepage, starts `--site-page-top` under
the bar’s rule on every page, the explainer and the optimality paper included.
The film’s page has section tabs under that rule, and its film starts the same space
under the tabs. Every section heading on the site pages and the explainer takes the two
section tokens; print reads its own values of both (2.8 of the base and 1.3rem), which
are the paper’s. On the explainer the credits start 2.25rem under the title on screen
and 2rem in print.

`--site-table-space` is the space above and below every table, and above and below the
rating ladders. A site table (`.site-table`) takes it above its filter bar, which keeps
its own 0.5rem to the table, and below its wrap; the awaiting-replay disclosure takes it
above and below itself, its table flush under the summary when open; and a document’s
own table, which KPress wraps and already sets 2rem from the text, reads the same token,
so one value moves every table on the site.
Where a larger margin meets it, as a section heading’s does below the disclosure, the
larger one stands.

`--site-wide-gutter` is the least space between a wide block and the edge of the page’s
content area: a table with its filter bar, a row of cards, the atlas grid, the film.
The content area is the page inside its margin, which is where KPress clips a narrow
page, and its width is KPress’s page container’s, `100cqw`. A wide block’s room is that
width less the gutter on either side (`--site-wide-room`), and the wide track, a table’s
bleed and the film all stop there.
The gutter is KPress’s own document gutter, so a wide block with no room to spare is
exactly as wide as the text: 40 pixels from either edge of the window between 768 and
about 1180 pixels wide (1456 for the frontier atlas), and 16 on a phone.
The room is never measured from the window.
`100vw` counts a scrollbar that the layout does not, so a block sized from it ran 16
pixels under the document’s clip at 768 pixels, and 7.5 more with a scrollbar, cutting
the first letters of the filter labels and the end of the count.
Nothing that scrolls sideways gives the gutter up either: in KPress’s narrow band a
document’s own table keeps to its column and scrolls inside its wrap, where KPress would
run it under the clip, and a result overview’s bounds scroll inside their own box rather
than past the popover’s margin.
On a phone a results table’s row cards are padded 0.5rem at the sides.
`devtools.preview_site` fails a build on any wide block that runs past an ancestor which
clips or scrolls sideways (`--clips`, and with `--shots`), at 1024, 768 and 390 pixels,
as laid out and again with a scrollbar’s 15 pixels taken from the layout;
`tests/test_site_wide_blocks.py` holds the pages to none.

`devtools.measure_site_pages space` measures these on a built site: the white space
above and below every table and heading, in pixels between boxes, at each width asked
for, with each heading’s size and line height, and each table’s distance from the
window’s edges or its popover’s. `tests/test_overview.py` pins each token’s value and
the rule that reads it.

## Site Components

Each component is defined once in [site.css](site.css) and used on every page that needs
it.

- **Navigation bar.** One fixed-width row of sans links in the page’s header slot, the
  same on every page, the explainer and the workbench included, led by the site name,
  “Square Packing”, set in capitals by CSS (`text-transform`, lightly tracked) so its
  text is unchanged, and a step heavier.
  The bar’s type is tied to the body’s on the scale above (Typography Roles), never set
  in pixels or rem. A link, and a section tab, is one step under the 18px prose and no
  more: the caption size, 0.92 of the sans base, 17.48px, which is the first size of the
  scale under 18px (`--site-nav-font-size`; the step between, 0.95, is 18.05px, not
  under the prose). The site’s name is the sans base, 19px (`--site-nav-name-size`), the
  size sans text takes beside the prose, so with its weight and capitals it reads as the
  name. Both tokens are in `site-nav.css` and are computed from the host base
  (`--kpress-host-font-size-base`), which is the same on every page, so the bar is one
  size on every page and at every width.
  `devtools.measure_site_pages header` reports the four sizes, `preview_site` fails a
  page whose bar is not one step under its body (`type_problems`), and
  `tests/test_site_wide_blocks.py` holds the relation in a browser at 1280, 768 and 390
  pixels, where the links keep one line, one line and two lines.
  Case 11, the site’s icon, sits before the name as its mark, 18px square, inside the
  same link, so it takes the same hover.
  Narrower than 56rem, where the bar with the name would wrap, the name gives way and
  the mark alone leads home, labelled “Square Packing home” for a screen reader.
  Every item takes the cards’ gentle wash on hover and nothing underlines on hover; the
  current page alone is underlined in the accent.
  The edition appears only in the closing line.
  Every page renders it from the one partial, `site-nav.html`, and it has the same box
  on every page at every width.
  It sits 1rem below the top of the window on every page, the explainer and the
  workbench included: `site-nav.css` narrows KPress’s page top margin
  (`--kpress-page-margin-block-start`) from 2.5rem. Below the bar, every page’s first
  block starts one shared space under its rule, `--site-page-top` (4rem, in
  `site-nav.css`): KPress’s document padding above the column is dropped on screen, the
  column’s own top padding is the token, and the first block (a hero or a document’s
  title) adds no margin of its own.
  A page that opens on a picture, the homepage’s packing, starts it `--site-hero-lift`
  (0.5rem) nearer the bar, since a drawing has no line spacing above its edge.
  On the explainer the source chips sit in that space and the title starts the token
  below them. Print keeps KPress’s spacing, so the explainer’s PDF does not move.
  Its entries are Overview, Frontier, Results, Papers, Visualize and GitHub.
  Papers leads to the papers page (`papers.html`) and is current on it and on both
  papers, the explainer and the tutorial, which keep their own addresses.
  Visualize leads to the film (`visualize.html`) and is current on both pages of the
  Visualize section, the film and the workbench.
  The workbench is an application rather than a KPress page, so its build
  (`workbench_tools.build_site`) takes the bar, its stylesheet, the theme bootstrap and
  the gear’s script from `render_overview.nav_shell`, in a shell that gives it the page
  margins and header rule KPress gives the others; the application fills the window
  below it. Only the bar and the section tabs follow the theme there: the workbench
  itself has no dark mode yet.

- **Section tabs.** A section that spans pages carries one small tab bar under the
  navigation bar; the Visualize section is the one that does, with two tabs, **Film**
  (`visualize.html`, the section’s first page) and **Workbench** (`workbench/`). Each
  tab is a real link to its own page, so the bar needs no script, and a tab can be
  opened, bookmarked and shared; every existing `workbench/` address lands on the
  Workbench tab. The bar is a centred strip with square corners and the cards’ thin
  border, a hairline between tabs, in the bar’s sans at the links’ own size
  (`--site-nav-font-size`) and medium weight: a tab is gray, takes the nav items’ wash
  and accent on hover, and the current tab is filled with a 16% accent tint over the
  page background in the page’s own text colour.
  It is `.site-tabs`, rendered by `render_overview.visualize_tabs`, and defined in
  `site-nav.css` rather than `site.css` because the workbench carries only the bar’s
  stylesheet. On the film’s page it opens the document; on the workbench it sits in the
  application shell under the bar, above the application.
  From the top, both pages read bar, rule, tabs, content: the tabs stand under the rule
  that runs under the bar, never over it.
  They are in the header slot, whose lower border is that rule, so a header that holds
  tabs gives up its border and the bar draws the rule at its own foot (`:has()`, in
  `site-nav.css`), where it is on every other page and as long.
  The tabs start `--site-tabs-space` (0.7rem, 11.2px) under the rule.
  On the film’s page the first block starts `--site-page-top` under the tabs; on the
  workbench, where the application starts at the shell’s lower edge, the tabs keep the
  same 0.7rem below them.
  Measured at 1280px, on both pages: the bar from 16 to 72.1px with the rule its last
  pixel, the tabs from 83.3 to 119.9px, then the film at 183.9px and the application at
  131.1px; at 390px, where the bar wraps to two lines, the rule ends at 84.8px, the tabs
  run from 96.0 to 132.6px, the film starts at 196.6px and the application at 143.8px.
  `devtools.measure_site_pages header` reports these, `preview_site` fails a built page
  whose tabs start over the rule (`tabs_problems`), and `tests/test_site_wide_blocks.py`
  holds both pages to it in a browser.
  It is hidden in print and in the embed view.

- **Theme control.** A small gray gear, an inline SVG, ends the navigation bar on every
  page, the explainer and the workbench included.
  From 80rem wide it leaves the links’ centred track for the bar’s far right, its edge
  over the right end of the rule under the bar; narrower, it ends the row of links.
  At every width its centre is level with the middle of the tab text’s capitals, which
  sits lower than the middle of the row, so it drops by `--site-gear-drop` (0.11em). It
  takes the nav items’ wash on hover and while its menu is open, and never underlines.
  Pressing it opens a compact menu, a native popover under the gear with square corners
  and the cards’ border and shadow, of three choices, each an icon and a word: System,
  Light and Dark. The current choice is in the accent with a check at its end.
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
  sections are `h2`s. The Visualize page shows none either: the bar, the section tabs
  and the film are the page, and its `h1`, “Visualize”, is for a screen reader alone
  (`.site-visually-hidden`, in `site.css`: out of the flow, one pixel, clipped, the
  class for any block a reader does not see and a screen reader should).
  The film after the hidden title is the page’s first block, so on screen it brings no
  margin above and starts `--site-page-top` under the header.
  A page that has a title (the frontier atlas, the case records) sets it in the hero,
  centred, with a subtitle under it.
  The frontier atlas’s is “A survey of everything known for cases $n = 1, \ldots, 324$”,
  the results page’s “A survey of all reviewed results” and the Papers page’s “Papers
  and interactive explanations for specific results”.
  The subtitle is the sans face at 1.1 times the sans base (`--site-subtitle-scale`,
  about 21px), in the page’s own text colour, never gray, with the same space above it
  and below it (`--site-subtitle-space`, 1.5rem). A formula in a subtitle is math, not
  `<var>` and digits: the subtitle is an HTML block, where KPress leaves `$…$` literal,
  so the renderer fills it with KPress’s own math markup
  (`render_frontier_page.math_html`), and it is set sans as the subtitle’s text is.
  The atlas’s range is read from the case records, first and last, never typed.
  A title with no subtitle, a document’s own `h1` among them, stands that space above
  its first paragraph.
  The page title style (every hero `h1`, and `.site-title`) is the sans face in upright
  caps (not KPress’s italic `h2`) at 1.5 times the sans base, centred.
  The homepage’s first section, The Square Packing Problem, takes it through
  `.site-title`, so it reads as the frontier atlas’s title does.
  That section opens with README’s first paragraph: the block between README’s
  `project-intro` markers, read at render time and its links rewritten for the site
  (`site_documents.overview_intro`), so it is edited in `README.md` and nowhere else.
  The site’s own statement follows it and is the only prose the template holds there.
  README’s next two paragraphs, what the project covers and its newest major result, are
  a second shared block, `recent-progress`, which opens Recent Results
  (`site_documents.overview_progress`); README keeps all three paragraphs together and
  in order, parted only by the markers.
  `devtools.check_readme` holds both blocks: each marked once, the second directly after
  the first, prose alone with no heading or comment, and no case called the central one.

- **Heading leading.** Every heading is set at one line height, 1.15
  (`--paper-heading-leading`, in `paper-type.css`), on screen: a page’s title (an `h1`,
  or the homepage’s `.site-title`), its subtitle, every section heading (`h2` to `h6`)
  on the site pages, the explainer and the optimality paper, a card’s headline
  (`.site-card-value`), a popover’s (`.site-popover-value`, which a row’s popover, the
  atlas popover and a result overview’s case all use), a case record’s title and a
  column’s name in the rating ladders.
  Body text, table cells, notes and the small caps labels (a card’s label, a result
  overview’s section label) keep their own line heights.
  The explainer’s hero title keeps KPress’s 1.05, which its prepared math is fitted to,
  and print keeps KPress’s leading, so the explainer’s PDF does not move.
  A formula in a heading or headline takes no line of its own: KPress’s inline math box
  (line height 1.4) and KaTeX’s (1.2) are both set to zero there, so a formula is as
  tall as KaTeX’s struts make it and the line that holds one is no taller than its
  neighbours. A headline’s box carries the room the looser line used to give it as margin
  (0.2rem above and 0.3rem below a card’s, 0.5rem and 1rem a popover’s).

- **Report layout.** Every report page (the tutorial, the synopsis and the other
  documents) has one layout.
  A long report gets a contents rail and a short one does not, by kpress’s own rule
  (seven headings and 800 words), so the choice is never made per page.
  Either way the reading column is centred.
  A document’s own hand-written contents list, which GitHub needs and the site does not,
  is dropped from its page, so the rail never repeats it as an entry.

- **Document pages with contents.** On a wide screen the contents rail stays at the left
  edge and the reading column is centred on the page, under the centred navigation.
  Where the pane is too narrow to centre, the column sits as near centre as the 15rem
  rail allows. The rail is plain text: no frame, only the underlined Contents label, and
  entries that change colour on hover or when current, with no fill or side bar.

- **Site icon and hero.** Both are atlas drawings, reduced to each square’s outline and
  fill. The icon is case 11, Trump’s packing of eleven squares, in the atlas ink on
  white, inlined as a data URI on every page, the workbench included; the same drawing
  is the mark in the navigation bar, drawn there in the bar’s ink, so it is light in
  dark mode. In both, the container’s frame is exactly one pixel of the drawing at its
  size (16px in a tab, 18px in the bar; `packing_svg(frame_px=)`), its outer edge on the
  drawing’s edge and snapped to the pixel grid, so the container reads as a square: one
  crisp pixel on a 1x screen, two on a 2x screen.
  Its squares’ outlines are half that pixel, one device pixel on a 2x screen, so each
  square stays distinct at icon size; the page’s drawings keep their hairline.
  The homepage’s hero is case 53, centered under the title in the page’s ink and linked
  to its row in the frontier atlas.

- **Cards.** A card is a summary with square corners, a thin border, a caps label, a
  value and a supporting note.
  A card section is one wrapping row in the wide track, in a `.site-cards-frame` the row
  measures itself against.
  Any line the cards do not fill centres on it, at every width: four cards on a wide
  screen, a section of three, and the last line of a long section alike.
  A card’s popover is its sibling in the row’s markup but never in the row, since a
  closed popover is not displayed and an open one is in the top layer.
  Print keeps the plain grid of medium columns, filled from the left.
  Cards come in three sizes (Card sizes, below).
  The value is the card’s headline: the sans face at the medium weight
  (`--site-font-weight-sans-medium`, 550), the face and weight of the page title and of
  the sans section headings (`h3`), at 1.15 of the text size (20.7px) and at the
  headings’ leading (**Heading leading**, below), so a headline of two or three lines
  reads as one block. The popover repeats the headline in the same face, weight and
  leading. A card works one of two ways.
  A popover card (`card`) is a button that opens a popover showing where it leads, and
  the popover ends in one button that goes there, centred at its foot.
  A direct card is instead itself the link (`link_card`), an `<a>` with no popover.
  **A page card navigates.** The overview’s four page cards, the explainer, the
  tutorial, the workbench and the frontier atlas, lead to full pages the site serves, so
  each is a direct card that goes to its page in the same tab (`new_tab=False`), with
  the right arrow for its icon (`data-go="page"`) and nothing framed (`think-bc5d`).
  Popovers are for targets that are not site pages of their own: a result’s row, a
  repository document rendered for its card’s popover, a case.
  **Every other direct card opens its target in a new tab** (`target="_blank"`,
  `rel="noopener noreferrer"`), so the page the reader chose it from stays where they
  left it: a poster’s PDF, the Visualize page, another project.
  `link_card` refuses `new_tab=False` for an address off the site.
  - When a popover card leads to a document or paper the site renders, the popover
    renders that page itself, narrow, in a frame: the page at the same address with
    `?view=embed` added before any fragment, so a filtered view such as
    `frontier.html?recent=true` or a case such as `frontier.html#n-11` arrives as it
    will be seen. The embed view drops the navigation bar and sends every link out of the
    frame to the full window.
    The button is **Expand**, which opens the page at full size; a repository document
    also offers its source “On GitHub”, which opens it on `main`. Every repository link
    on the site names `main`, never a commit, and is made by `devtools/repo_links.py`.
  - When the card leads to another project off the site, it is a direct card.
    It shows the address under the note beside the host’s mark (GitHub’s for a GitHub
    URL, otherwise the site’s favicon, saved under `devtools/overview/favicons/` by host
    and inlined, since the page fetches nothing), and opens it in a new tab.
  - When the card leads to a poster’s PDF or to the Visualize page, it is a direct card
    headed by the picture it opens (below).
    A PDF card is typed `application/pdf` and never marked `download`, so the browser
    opens it in place.
  - When the card leads to a row, the popover previews the row, read from the same
    record: a result’s claim, why it matters, its rungs and records.
    A result’s row is on the results page, so its card is a page card, with the right
    arrow for its icon, that previews rather than frames: the button, **Open T-NNN in
    the results table**, goes to `all-results.html#t-nnn`. A row on the overview itself
    would scroll, with the down arrow.

  The frame loads only when its popover first opens, so the overview stays light.
  The popover is a native `popover` panel with square corners over a faint scrim, set in
  sans, closed by its `×`, by Escape, or by a click outside, and it works without
  scripting. A card, popover or direct, gains a gentle wash on hover.
  Every popover has the same margin on all four sides, `--site-popover-pad` (1.75rem;
  1.1rem on a phone). Its `×` is a 2.75rem square tap target (`--site-popover-close`) set
  0.6rem in from the corner (0.25rem on a phone), washed on hover.
  Only the first block after it keeps clear of it, so the margins stay even everywhere
  else. Its gray corner icon and the popover’s button both show where the button goes:
  down to a row on this page, external off the site, right to another page of the site
  (Arrows, below).

- **Card sizes.** A card is sized by its text, in three sizes it names in
  `data-card-size`; a card that names none is medium.
  Each size is as wide as a column of the grid of its own minimum column the frame fits,
  with 1rem gaps, so cards of one size line up as a grid at every width:
  - `small`, 12rem columns, for a headline and one line, under 80 characters: five to a
    line at 1280 pixels (208px each), four at 1024 (236px) and three at 768 (235px).
  - `medium`, 16rem columns, for a headline and a sentence, 80 to 159 characters: four
    to a line at 1280 pixels (264px), three at 1024 (320px) and two at 768 (360px).
  - `large`, 21rem columns, for a paragraph or a list, 160 characters or more: three to
    a line at 1280 pixels (357px), two at 1024 (488px) and two at 768 (360px).

  On a phone every card takes the whole line.
  The count to a line is `--site-cards-small`, `-medium` or `-large`, each stepped by
  its own container queries: n columns of minimum m and n − 1 gaps need (m + 1)n − 1
  rem, so medium steps at 33, 50, 67 and 84rem, as the grid did.
  A section declares one size for all its cards, in `SECTION_CARD_SIZES`
  (`overview_sections.py`), so its lines are one grid; the size is the one its typical
  card’s text asks for, and `tests/test_overview.py` holds the two together.
  The page cards, the atlas cards and the other projects are medium; the documents,
  whose notes are a line, are small.
  A card built without a size (`card()` or `link_card()` with no `size=`) takes the
  default for its own text: its headline and note, and a direct card’s address, counted
  as they read, a formula once.

- **Card heroes.** Any card, popover or direct, may be headed by a small picture
  (`hero=` on `card()` and `link_card()`, drawn by `card_hero`). The hero runs edge to
  edge above the caps label in a fixed 16:9 box, covering it from the picture’s top
  edge, so pictures of any shape line up across a row; a hairline parts it from the
  text. It is a file served beside the page, never an address off the site, loads lazily,
  and is decorative (`alt=""`), since the card’s label and value already say what it
  shows. Dark mode dims it slightly (`--site-hero-filter`), since the pictures are prints
  on white. On a hero card the corner icon sits over the picture on a small chip of the
  page background, so it reads on any image.

- **Chips.** Every small label is one `.site-chip`: square corners, the sans face at the
  note size, a solid light fill and no border, lettered in the page’s own text colour.
  A plain chip is a light gray tint; `data-tone="accent"` is an accent tint, for a
  settled state such as a proved case.
  Chips sit inline and wrap like words, a space apart, with a small block margin
  (0.15rem) so a wrapped row never touches the row above, on any page or at any width.
  A rung chip adds `.site-rung-fill` with `data-rung` and `data-level`, and its fill
  strengthens and saturates with the level (Color, The Rung Scale).
  Significance is listed first: wherever a result’s rungs are shown together, in a table
  row, a popover, a result’s overview or a case record, they run S, V, C, from the one
  function that sets the order, `overview_sections.rung_chips`. The generated register
  documents keep their own order, verification first.
  A standing chip carries `data-standing` and adds no style of its own: `current best`
  takes the accent, as a settled state, and every other standing
  (`current best, reported`, `second certificate`, `superseded`, `not a bound`) the
  plain gray, so a reader sees which results still hold without the others shouting.
  A novelty chip (`data-novelty`) is always plain gray.

- **Arrows.** Every arrow on the site is one drawing, never a typed character: the
  site’s text face has glyphs for `↑` and `↓` only, so `←`, `→` and `↗` came from a
  different fallback font in each browser and no two arrows matched.
  The drawing is `--site-arrow` in [site.css](site.css), a shaft and an open head in a
  16-unit box, stroke 1.6 with round caps and joins, held as an SVG data URI and painted
  as a mask over `currentColor`, so it takes the colour of the text around it in both
  themes. Each direction is that one drawing turned: **right** as drawn, **left** its
  mirror, **down** a quarter turn clockwise, **up** a quarter turn back, and
  **external** an eighth turn back, pointing up and to the right.
  The one other shape is the sort pair, `--site-arrow-sort`, two small arrows up and
  down in the same stroke.
  - Inline markup carries `<span class="site-icon-arrow" data-arrow="right">`, written
    only by `overview_sections.arrow_icon(direction)`: the atlas popover’s stepper (left
    and right), a case record’s steps to its neighbours (left before the previous case,
    right after the next) and the overview’s “See all results” line (right).
  - The icons CSS draws are pseudo-elements painted from the same token: a card’s corner
    icon and its popover’s button, chosen by `data-go` (down to a row on this page,
    external off the site, right to another page of the site, such as **See All
    Cases**), and a sortable header’s indicator (the sort pair while unsorted, in the
    muted gray; up or down in the accent once sorted).
  - The arrow is decorative, `aria-hidden` or generated content, so a link or button
    keeps its own text or `aria-label` as its name.
  - **Hover.** On hover or keyboard focus, the arrow in a link or button moves 2px the
    way it points (external 1.5px up and 1.5px right) on the Motion timing and keeps the
    element’s colour. A card’s corner icon does not move: it fades in with the card’s
    wash. A disabled button’s arrow stays still, and under reduced motion no arrow moves.
  - Sort indicators do not move: a header is a control whose arrow reports a state.

- **Motion.** Every hover and focus change on the site runs on one timing, a fast,
  smooth ease: `--site-hover-duration` (140ms) and `--site-hover-easing` (`ease-out`),
  declared in [site-nav.css](site-nav.css) so every page carries them, the explainer and
  the workbench included, and fed to KPress’s own `--kpress-transition-fast` so its
  contents rail and footnote links match.
  A rule transitions only the properties its hover changes (`background-color`, `color`,
  `border-color`, `opacity`, `translate`), never `all`, and never with a literal
  duration: `tests/test_overview.py` fails a `transition` in `site.css`, `site-nav.css`
  or `explainer-shell.html` that names a time instead of the token.
  Under `prefers-reduced-motion: reduce` the duration is 0ms, so colours change at once
  and no arrow moves.

- **Rating ladders.** Verification at a Glance is one diagram, `.site-ladders`, which is
  neither a set of cards nor the shared data table: a column for each scored dimension
  of the rubric, in the order Significance, Verification, Confirmation, and a row for
  each level, the highest at the top, so the rungs of the three ladders line up across a
  row. A column is headed by the dimension’s name, which links to its section of
  `epistemics.md`, and the question it answers, with no caps label.
  A cell holds the rung’s chip, a description of exactly two lines, and the count of
  register entries at that level, “7 results” or “no result yet” (`rung_counts`,
  `count_label`). A ladder with no rung at a level leaves its cell empty, as
  Significance does at level 0.
  - **Wording.** The chip’s `title` is the rubric’s full meaning, read from the tables
    in `epistemics.md` (`rung_meanings`). The description is that meaning, or a short
    form where the meaning does not fit two lines of the narrowest cell
    (`rung_short_meanings`); `RUNG_SHORT_MEANINGS` in `overview_sections.py` is the one
    place a short form is written.
    A description is never clipped and never cut with an ellipsis: one that does not
    wrap to two lines of 25 characters (`SHORT_MEANING_LINE`) stops the build until it
    is given a shorter form.
  - **Rows.** Every rung is the same height at any one width, since each is a chip, a
    count and a two-line box.
    A cell arranges the three by its own width.
    With 20.5rem or more it sets the chip over its count in a 6.5rem rail and the
    description beside them, 74.8px a row, at 1280 pixels and on a phone.
    Narrower, it sets the chip and its count on one line and the description under them
    across the cell, 99.3px a row, at 1024 and 768 pixels.
    A description is never set narrower than 13.5rem (`--site-ladders-meaning-min`).
  - **Columns.** The three columns are equal, and each keeps 0.75rem
    (`--site-ladders-inset`) clear after its words, before the next column’s chip.
    Three columns therefore need 42.75rem: three times the least description and its
    inset.
  - **Phone.** Below 42.75rem of its own width the diagram stacks: one block a ladder,
    in the same order, each under its own head with its rungs from the top.
    Three columns there would set a description narrower than its least.
    The missing rung takes no room.
    The diagram’s width is the wide track’s, which is sized from the page and not the
    window (**Wide bleed**): 1104px at a 1280-pixel window, 944px at 1024, 688px (43rem)
    at 768, where the page’s margin widens, 684px at 716 and 358px at 390. So three
    columns hold from a 716-pixel window up, with a description 217.3px wide at 768 and
    216px at 716, and the ladders stack at 715 and below.
    The inset is what fits them at 768: at 1rem three columns need 43.5rem, more than
    that window’s wide track, and the ladders would stack from 768 to 775 pixels between
    two bands of three columns.
  - **Markup.** A grid with table roles (`role="table"`, a row a level, column headers,
    a visually hidden row header naming the level, cells), not a `<table>`: KPress wraps
    every table in its own scroller and restyles it as `.kpress-table`. Stacking changes
    only the grid’s order, so a screen reader reads the same table, level by level, at
    every width.
  - **Space.** It sits in the wide track and stands `--site-table-space` clear of the
    text above and below it, as a table does.
    Either side it keeps the wide track’s gutter and is never under the page’s clip:
    40px from the window at 1024 and 768 pixels and 16px at 390, which is 8px
    (`--site-wide-gutter`) inside the page’s content area wherever the page clips.

- **Atlas grid.** The atlas grid holds every tracked case, n = 1 to 324, as a square
  drawing in the page’s ink with its n beneath.
  The grid bleeds past the wide track as the window grows, to 140rem less the page
  gutters, and its cells keep a readable size (at least 6.4rem, 4.6rem on a phone), so a
  wider screen shows more cases per row: 4 at 390 pixels, 11 at 1280, 17 at 1920 and 20
  at 2560. A cell washes on hover and is a link to its case record.
  The cells ship in a `<template>` and are placed only as the grid nears the viewport
  (`overview/atlas-grid.js`), so they add nothing to the first paint; each drawing is
  400 units across, fine enough to show large.

- **Atlas expander.** The grid shows n = 1 to 100 at first (`ATLAS_FIRST`). One button,
  centred under it, reads **Show all 324** and expands the grid in place; it then reads
  **Show 1 to 100** and collapses it, and carries `aria-expanded`. It is the site’s
  action button, `.site-popover-action`, the same accent fill a popover’s button has,
  set `--site-atlas-toggle-space` below the grid.
  Cases 101 to 324 ship in a second `<template>` and are placed only the first time the
  grid expands, into one box the grid lays out as its own cells (`display: contents`),
  so collapsing is that box’s `hidden`. Collapsing keeps the button in view.
  The atlas popover’s arrows still step through all 324 cases: stepping past the last
  case shown expands the grid first, so the cell focus returns to is there.
  Without scripting the button’s row stays `hidden`, since it would do nothing.

- **Wide bleed.** A wide block (`.site-wide`) takes the wide track, `--site-wide`, less
  the page gutters (`--site-wide-gutter` on either side; **Spacing**, above).
  Two kinds bleed past it.
  The atlas grid bleeds at every width, up to `--site-bleed-max` (140rem). A data table
  bleeds only above `--site-table-bleed-from` (80rem, 1280 pixels): from there it grows
  one pixel for each pixel of window, `--site-table-wide`, until it reaches the page
  gutters or `--site-table-max` (100rem, 1600 pixels), past which its columns would only
  spread apart and a row would be harder to follow.
  So nothing changes at 1280 pixels or narrower, and on a large screen a table’s text
  columns wrap less. The Every Result table is 1104 pixels wide up to 1280, 1424 at 1600
  and 1600 from about 1780 up; the frontier table, whose own track is 86rem, is the
  page’s content area less its gutters up to 1456 pixels and goes from 1376 to 1600
  above that. The rule takes any `.site-wide` that is or holds a `.site-table-wrap`, so a
  new table bleeds with no rule of its own.
  The replay table is the exception because it keeps to its content.

- **Atlas popover.** Pressing a cell opens the page’s one atlas popover on that case, a
  card popover in every other way (square corners, the scrim, the caps label, the close
  cross, Escape and a click outside), and a little larger: up to 62rem wide and 58rem
  tall. It shows what the ascent film’s panel shows for the case, beside the drawing
  large: the gap bar (a number line from one below $\lceil\sqrt{n}\,\rceil$ to two above
  it, the integers and the values of $\sqrt{n}$ and $\sqrt{n} + 1$ marked, the two
  bounds as bold rules with their values above and the open span between them shaded);
  under PROVEN the bound as one statement, the proved lower bound in scarlet and the
  best known side in green, with the star for a recent lower bound; the badges; the
  citation, one line per bound with this project’s note; and what is OPEN. The facts are
  the film’s own, read from the atlas figure and `bound-citations.json` into one JSON
  element (`atlas_film_facts`), and the script fills the popover from them with kpress’s
  math nodes, never HTML strings.
  It ends in **See All Cases**, which goes to `cases.html#n-N` at full size, and arrows,
  and the arrow keys, step to the neighbouring case.
  The two arrows are the site’s arrow, right and left (Arrows, above).
  Opening moves focus to the close cross; closing returns it to the case’s cell.
  On a phone the panel takes the width less half a rem each side, scrolls inside, keeps
  its button in a sticky foot, and has a 2.75rem close target.

- **Case records.** Every case has one record at one address, `cases.html#n-11`. The n
  of a frontier-atlas row opens it in the one case popover that page carries, a
  page-kind popover framing the record in its embed view, with **Expand** to the full
  record (`overview/case-popover.js`); an atlas-grid cell reaches it through the atlas
  popover’s button. Without scripting either link goes to the record itself.
  The rest of a frontier-atlas row opens the row’s own popover (**Row popovers**,
  below): how the best known packing was built, the minimal polynomial behind a decimal,
  the sources, the verification, the notes and the evidence entries, with “Details” in
  the Records cell as the trigger.
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

- **Atlas cards.** Under the grid, the atlas’s posters and film are three direct hero
  cards side by side, one card section (`atlas_cards`): the n = 1 to 100 poster, headed
  by its landscape card image, opens its PDF; the n = 1 to 324 poster, headed by the top
  of the poster itself, opens its PDF; and **Visualize**, headed by a frame of the n = 1
  to 324 film at n = 290 (`ascent-n1-324-poster.png`), opens `visualize.html`, the film
  alone at full size. The overview embeds no video, so nothing on it moves or fetches a
  film.

- **The film.** The Visualize section’s Film tab, `visualize.html`, is the n = 1 to 324
  film at full size directly under the section tabs, with no page title and no subtitle
  (**Page headings**, above).
  It is as wide as the window allows less the page gutters, up to 120rem, but never so
  tall that it will not fit the window whole (`.site-film-frame`), and embedded inline,
  with its controls. Its poster, `ascent-n1-324-poster.png`, published beside the
  explainer’s assets, shows until playback starts, at the video’s own 16:9, so starting
  moves nothing. The film starts when the page is visited.
  Its markup mutes it (`muted`, which a browser requires of a film it starts unasked)
  and marks it `data-autoplay`, and `overview/film.js`, which only this page carries,
  sets `autoplay` and plays it.
  It does not loop. **Visiting the page therefore starts the film’s download**, a 216 MB
  file on the release, which the browser fetches as it plays.
  A reader who asks for reduced motion (`prefers-reduced-motion: reduce`) keeps the
  poster and the play control, and so does a reader without scripts, the page framed in
  a card’s popover, and a browser that refuses to start the film.
  For them nothing is fetched until they press play: the markup keeps `preload="none"`
  and has no `autoplay` of its own, since markup cannot make that depend on the motion
  preference. No other film on the site starts unasked: the explainer’s stays as it was,
  fetching nothing until a reader presses play, and the overview embeds no video.
  The tools that open the site’s pages in a browser (`preview_site`,
  `measure_site_pages header`, the browser tests) open them under reduced motion
  (`preview_site.REDUCED_MOTION`), so none of them starts the download.
  `tests/node/overview_film/` runs the script against a stand-in film.
  A caption and a note in the support colour follow at the reading measure: what the
  film shows, its length, the shorter 1 to 100 film, the release both are on, and the
  Workbench.

- **Tables.** Every data table is one component, `.site-table` on a KPress table, in a
  `.site-table-wrap` that scrolls sideways if the table cannot fit.
  It is set in the sans face at the note size, with sortable headers, filters above and
  group rows. A row with detail opens its popover, and no cell expands on its own (**Row
  popovers**, below). Rows are separated by a light rule, not zebra stripes, and a row
  takes the wash on hover.
  Cells are padded 0.55rem by 0.5rem, top-aligned, at line height 1.4. Headers sit at
  the bottom of their cell, aligned as their column is: text columns to the start,
  number columns (`.num`, tabular figures) to the end.
  The short columns (the id, n and date, `.site-col-id`, `.site-col-n` and
  `.site-col-date`) stay on one line and as narrow as their content, which leaves the
  spare width to the long text column.
  Secondary content in a cell, such as a result’s id, a credit or an “after …” list,
  takes `.site-cell-quiet`, which sets it in the support colour and the sans face.
  It keeps the table’s size, so the quiet text does not become harder to read.
  Every table stands `--site-table-space` clear of the text above and below it
  (**Spacing**, above).
  Wide tables bleed on large screens, as **Wide bleed** above describes.
  On a phone, the results table becomes one card per row.
  In the results table a result’s standing chip sits under its rungs; a date cell says
  what it dates, `published` or `established`, in the support colour.
  A superseded result’s row reads quieter, its text in the support colour, in every site
  table, by one rule on `tr[data-standing="superseded"]`; its chips keep their fills.
  A row reached by its address (`frontier.html#n-11`, `all-results.html#t-018`) takes
  the wash, in every site table.

- **Result filters.** Every table of results sits under one tools bar, the same on the
  overview’s recent table and on the results page: the same controls, the same choices
  and the same order. Only where Significance and Max age start, and the count at its
  end, are the table’s own.
  `overview_sections.result_filters` writes it and `overview/table.js` drives it.
  - **Facets.** A result’s row carries each facet as an attribute
    (`overview_sections.result_facets`), and the bar has one control for each:

| Control | Row attribute | Reads as |
| --- | --- | --- |
| Significance | `data-s`, the S level | a floor: S4 and up |
| Verification | `data-v`, the V level | a floor: V4 and up |
| Confirmation | `data-c`, the C level | a floor: C3 and up |
| Standing | `data-standing` | equal to the standing chosen |
| Source | `data-source`, `ours` or `others` | this project’s, or others’ |
| Case n | `data-n`, counts and ranges (`18-21 26`) | the result covers that n |
| Max age | `data-date`, a whole ISO date | dated at most that many days ago |

```
A rung select offers All, then each level of the rubric above its lowest as a floor,
the top level bare (S5). Standing offers the standings the register holds.
A date the register gives only to the year is the first day of it (`1979-01-01`).
Max age is a number of days, and empty is no limit. There is no date range.
```

- **Composition.** The filters compose: a row shows when it passes every one, and an
  empty control passes every row.

- **Defaults.** The caller passes them (`FilterDefaults`), and they are the one thing
  that differs between the two bars.
  Recent Results on the overview starts at significance S4 and up and a maximum age of
  180 days (`RECENT_DEFAULTS`); the results page starts at All and no maximum age
  (`RESULTS_DEFAULTS`), so every result shows.
  Every other control starts at All on both.
  A row outside its table’s defaults is `hidden` in the HTML, never left out of it, and
  the count is written there too, so the first paint is already the filtered table and
  never flashes every row.
  A control’s state in the HTML is its default, which is all the script knows of it.

- **Age.** On the page an age is measured from the reader’s own day, which the script
  reads when it loads and at every change, so a default of 180 days moves with the
  calendar and needs no rebuild.
  The HTML cannot know that day, and must not read the clock, since two renders of one
  tree are compared byte for byte.
  It measures from the newest `registered` date in the register (`reference_date`),
  which decides only which rows start `hidden` and the count written beside them; the
  script settles both again on load.

- **Group headings.** A group heading shows while a row under it does: one with no row
  left is hidden with them, in the HTML for the default.
  A sort hides the group headings, since the rows are then no longer in their groups.

- **A row named by the address** (`all-results.html#t-048`) shows whatever the filters
  hide, so a link to a result never lands on nothing.
  The script keeps it, and without scripts one rule, `.site-table tr[hidden]:target`,
  shows it.

- **Links.** A link can open either table filtered: each query parameter presets the
  control it names, `s-min=3`, `source=ours`, `n=17`, `age=30`; an empty value,
  `s-min=&age=`, clears a default.

- **A row’s popover** follows it through filtering and sorting, since the row finds it
  by id (**Row popovers**, below).

The bar wraps onto further lines as the page narrows; on a phone each control takes
about a line. Without scripts a filter cannot be changed, so nothing stays filtered:
under `@media (scripting: none)` every row shows, each group under its heading, and the
bar, which would do nothing, does not.
`tests/node/overview_table/` runs the script’s filters, alone and wired to a stand-in
table, and `tests/test_overview.py` holds both pages to the identical bar and each to
its defaults.

- **Row popovers.** The row is the unit: a table row with detail opens one popover for
  the whole row. This is the site’s one way to show detail on a table row, and no cell
  holds a `<details>` or expands on its own.
  Four tables use it: the recent table and the awaiting-replay table on the overview,
  the results table, and the frontier atlas.
  - **Pressing.** A click anywhere on the row opens its popover, and so does Enter or
    Space while the row has keyboard focus.
    A link, button or form control inside the row keeps its own behaviour, so the
    frontier’s n still opens the case record and a record link still leaves the page.
    A click that ends a text selection selects rather than opens.
  - **Look.** The whole row takes the wash on hover, from the shared table rule.
    A row with detail keeps the wash on keyboard focus, with a 2px accent ring inside
    its edge, and while its popover is open (`aria-expanded="true"`), and shows the
    pointer anywhere on it.
  - **The popover** is a card’s popover (`.site-popover`, with `.site-row-pop`): the
    caps label, the headline (its math serif only where the headline is mathematics
    standing alone, as on a card), the close cross, Escape and a click outside, and one
    button at its foot when the row leads somewhere else.
    Opening moves focus to the close cross.
    Closing returns focus to the row, unless the reader has already moved it, as a press
    on another row does.
  - **Markup** is written only by `overview_sections.row_detail`, in three pieces.
    The row is `<tr data-row-popover="ID" aria-label="…">`, the label its accessible
    name. One cell holds the row’s native trigger,
    `<button class="site-row-open" popovertarget="ID">`, around the row’s own key, such
    as a result’s id, and styled as that text.
    The popover follows the table, outside every cell, so it takes no style from the
    table: `<div class="site-popover site-row-pop" id="ID" popover role="dialog"
    aria-labelledby="ID-title">`, holding the close cross, the `.site-card-label`, the
    headline `.site-popover-value` with the id `ID-title`, the body in
    `.site-row-pop-body`, and the optional `.site-popover-actions`. The ids are
    `pop-result-t-nnn`, `pop-replay-n-N` and `pop-frontier-n-N`.
  - **Without scripting** the trigger opens the popover, as a card’s button does, and is
    the row’s one tab stop.
    `overview/row-popover.js` makes the row the control: it gives the row
    `tabindex="0"`, `aria-expanded` and `aria-controls`, and takes the trigger out of
    the tab order, so each row stays one stop.
    The row carries no `tabindex` in the HTML, since a focusable row that did nothing
    would be a dead stop for a reader without scripts.
  - **Sorting and filtering** (`overview/table.js`) move and hide rows.
    A row finds its popover by id, so the popover follows its row.
  - **Content.** Each kind of row has one function that writes its popover’s body:
    `overview_sections.result_row_popover_body` for a result, on the overview and the
    results page alike; `overview_sections.replay_row_popover_body` for a case awaiting
    replay; and `render_frontier_page.frontier_row_popover_body` for a frontier row.
    A result’s popover ends in **Open T-NNN in the results table** on the overview and
    has no button on the results page, where the row pressed is that row.
    A replay row’s ends in the button to its case in the frontier atlas, and a frontier
    row’s in the button to its case record.
  - **Deferred bodies.** A body too heavy to render once per row when the page loads can
    wait in a template: `row_detail(deferred=True)` writes it as
    `<template data-row-pop-body>` inside `.site-row-pop-body`, which the browser parses
    but neither lays out nor typesets, and the script places it just before the popover
    first opens, however it is opened.
    Its math is typeset then, as any popover’s is.
    A deferred body costs the same bytes; what it saves is the work of rendering every
    row’s body at load. Without scripts a template stays inert, so `fallback` is written
    beside it in a `<noscript>`, and is what that reader’s popover shows.
    No table uses it at present.
  - **Fetched bodies.** A body too heavy to carry in the page at all is written once, as
    a file beside the pages, and fetched: `row_detail(source="…")` writes the file’s
    address as `data-row-pop-src` on `.site-row-pop-body`, whose content in the page is
    then a short form of the body.
    The script fetches the file when the row is first pressed or its popover first
    opens, puts it in place of the short form, and has its math typeset.
    The page gains only the address.
    Where the file cannot be had, without scripts, on a page read from a file or off the
    network, the short form stays, and the next opening asks again.
    A result’s row does this: its short form is the result’s claim, significance and
    novelty, and its file is the result’s whole overview (**Result Overview**, below).
    This is the one fetch a page makes besides a page a card’s popover frames.

  `tests/node/overview_rows/` runs the script against a stand-in document, and
  `tests/test_overview.py` holds every row of the three pages to this markup and every
  cell free of `<details>`.

- **Recent results.** The overview’s Recent Results section opens with README’s
  `recent-progress` block (**Page headings**, above), then its own short prose on what
  the table lists, and then one table, not cards or a list: every result, by the date
  the table shows, newest first, one row each, the same `.site-table` in the sans face
  as the results page, without sorting (`recent_table`). The results page’s tools bar
  sits above it (**Result filters**, above), starting at significance S4 and up and a
  maximum age of 180 days, with the count of rows shown out of the total at the bar’s
  end. Those two defaults are all that make the table recent: no result is left out of it
  by a date the page fixes.
  Its five columns are the date, which says what it dates (`published` or
  `established`); the result, its math linking to its row on the results page, with the
  id beside it quiet, which is the row’s trigger; the method, the phrase the summary
  gives after the formula (“by a point-only route” reads “point-only route”), empty when
  there is none; the credit, the finder first and “after …” quiet, the list cut after
  three names with the whole of it in the cell’s `title`; and the status, every chip in
  one cell side by side.
  The status cell holds the S, V and C rung chips and then one chip per part of the
  standing (`second certificate, reported` is two chips), left to right a space apart,
  wrapping only where the cell is too narrow, with the chips’ own block margin between
  wrapped rows; it never stacks one chip per line.
  On a phone it takes the results table’s card-per-row form: the result and the date on
  the first line, then the method, the credit and the chips each across the card.
  A row opens its result’s popover (**Row popovers**, above), the same panel the results
  page opens for that result.
  The section holds no card or bulleted list, and the “See all results” line, with the
  right arrow, follows the table.

- **Results page.** Every registered result is one row of the results table on its own
  page, `all-results.html`, “Results” in the navigation bar after Frontier.
  (`results.html` is `RESULTS.md` rendered as a reader document, so the table’s page
  takes the other name.)
  The page has the frontier atlas’s shape: a hero title, “Every Result”, whose id is
  `every-result`, a subtitle, the prose that defines the ratings and standings, and the
  table under its filters (**Result filters**, above), which start with significance at
  All and no maximum age, so every result shows.
  Each row keeps its id, the result’s own (`#t-018`), which is where the overview’s
  recent table and replay table, and each case record’s results link.
  A row opens its result’s popover, the full claim and its novelty label, with the id in
  its first cell as the trigger (**Row popovers**, above).
  The overview keeps the newest results and ends that table with a “See all results”
  line and the right arrow, in the sans face at the note size.
  The table used to be the overview’s Every Result section, and its old addresses still
  arrive: the overview’s `overview/forward.js` sends `#every-result` and any `#t-nnn` to
  the results page with the fragment kept, and every other fragment the overview lacks
  to the explainer, as before.
  `tests/node/overview_forward/` runs the forwarder, and `tests/test_overview.py` holds
  every row id to the form it recognises.

- **Papers page.** The site’s papers, the optimality paper, the explainer and the
  tutorial, share one entry in the navigation bar, “Papers”, after Results.
  It leads to `papers.html`: a hero title, “Papers”, a subtitle, a short introduction
  and one large card for each paper (`data-card-size="large"`), saying what the paper
  is. The cards come from one ordered list, `overview_sections.PAPERS`, each entry a
  paper’s address, label, title, description and card size, so a new paper is one entry.
  Each is a popover card: pressing it opens a popover that frames the paper and expands
  to it. (The overview’s page cards are direct links instead; see Cards.)
  A popover card is a button and holds no link of its own, so what its description names
  is linked from its popover, beside the button.
  The optimality paper is first: it explains the result that stands, T-060, where the
  explainer proves the lower bounds T-060 superseded and the tutorial is the background
  to both. The explainer’s card names the newer optimality proofs and links the
  optimality paper and T-060 from its popover, from the one list that holds them
  (`OPTIMALITY_LINKS`). Its card on the overview reads the same but is the link to the
  explainer itself, so it carries no other link.
  The papers keep their addresses, `explainer.html`, `tutorial.html` and
  `n11-optimality/t-060-explainer.html`, and Papers is the current entry on the papers
  page and on each of them.
  The optimality paper has its own renderer, shell and Pages job
  (`render_n11_optimality_explainer`); it carries the bar as the explainer does, through
  `render_overview.nav_html`, with the links climbing one level to the site’s root, and
  without `paper-type.css`, so its typography and its sixteen-page PDF are its own.
  Its citations name the commit it was built from, where every other page links `main`.

- **Awaiting replay.** Under the recent table, a closed disclosure in the sans face at
  the note size: its summary names how many cases and the range, and it opens a compact
  table grouped by holder and the entries carrying the claim, each case linking to its
  row in the frontier atlas.
  A row opens its popover (**Row popovers**, above): the reported and the verified
  bound, each with its holder, date and entries.
  The reported value is the trigger, and the popovers follow the disclosure rather than
  sit in it, so none takes the compact table’s size.

## Result Overview

A result’s row, in Recent Results and in the results table, opens a popover with the
full overview of that result.
`devtools/result_overview.py` writes the popover’s body, `result_popover_html`, and
[site-result.css](site-result.css) holds its styles, apart from `site.css` and inlined
after it on every page.
The body is one `.site-result` block with no ids, no script and no `<table>`, so it does
not depend on the popover around it.
Its popover takes the atlas popover’s size, up to 62rem wide and 58rem tall, and scrolls
as one panel.

No page carries an overview.
Between them they run to about 2.8 MB (`result_overview --audit`) and two pages list the
results, so each is written once, as `result/t-nnn.html` beside the pages
(`render_overview.result_fragments`), and a row’s popover fetches its own when it first
opens (**Row popovers**, Fetched bodies).
A fragment is the one block and nothing else: it has no shell, and its links are written
from the site’s root, so only a page there may place it.
The directory is `result/`, not `results/`, since `results.html` is `RESULTS.md`.
`tests/test_overview.py` holds the two pages under a size ceiling each, and
`check_published_site` asks the deployed site for every overview the results table
names.

- **Head.** The popover’s own caps label, the result’s id, and its headline, the
  result’s summary, stand above the body and are in the page, so they do not change when
  the overview lands. The body opens with the S, V and C rung chips and the standing
  chips, as the tables show them; then the date with what it dates, the credit and the
  cases, in the support colour; the claim at the note size; and a closed disclosure with
  the significance, composition, next rung and novelty.
- **The case.** A result about one case, or up to four, shows the atlas popover’s panel
  for each: the gap bar, the bound as one statement with the lower bound in scarlet and
  the best known side in green, the badges, the citation and what is open, beside the
  packing drawn from the atlas.
  The block carries `site-atlas-pop`, so the panel takes the rules `site.css` already
  gives it, and its facts are the film’s own (`atlas_film_facts`). It is filled when the
  page is rendered, on the scale `overview/atlas-grid.js` uses; two values too close to
  sit side by side go either side of their marks.
  Under the panel, the case record’s verified and reported bounds and the gap form a
  small grid, each value linking to its field in the case file.
- **Many cases.** A result about more than four cases says so and lists them in a box
  that scrolls, one row each: the n linking to the case record, the two bounds in the
  film’s colours, the gap, the status chip, the frontier row and the case file.
- **The chain.** Every register result on the same case, oldest first, down one rule:
  the date, the id linking to its row, what it established, its chips, and its credit,
  bibliography entry, source packet and register entry.
  The rule beside the result the overview is about is the accent, and a superseded step
  reads quieter, as a superseded row does.
  Where a result stands differently on this case than across its whole scope, the step
  says both. A broad result’s chain opens on request.
- **Links.** One list for this site (the case record, the frontier row, the result’s
  row, the explainer for $n = 11$) and one for GitHub, every link on `main` through
  `devtools/repo_links.py`: the register entry, each evidence entry and each cited
  source’s bibliography entry at its line, the source packet, the artifacts, the review,
  and the case file with its four frontmatter bounds.
  A repository path is set as code.
  Rendering fails on a link whose target is not in the tree, on a page the site does not
  serve and on a fragment no row or record carries.

A section heading in the overview is a caps label, so it holds no formula: capitals
would change the formula’s letters.
`tests/test_result_overview.py` holds every part and every link.

## Token Ownership

KPress owns the regular sans weight in `--kpress-font-weight-sans-regular`. Its font
generators read that token to produce matching math metrics and print faces; the paper’s
CSS and print instancer use the same source.
Change that token and regenerate the fonts, metrics, and prepared page together.
The loading and generation contract is documented in the
[KPress font and math architecture](../../../vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md).

`paper-type.css` owns the type base, the reading measure, the h2 scale, the heading
leading, the space around a section heading, the sans/prose size ratio, the paper’s
medium and bold weights and the role scales; the explainer’s shell and `site.css` alias
them and never restate them.
`--paper-font-size-support` sizes figure labels; `--paper-font-size-note` and
`--paper-note-inset` size and inset captions and endnotes.
They share `--paper-support-color` and `--paper-support-leading`. Resolve the sans base
once in the prose scope: nested sans components must inherit the resolved size without
multiplying the ratio again.
Apply print overrides at the same scopes as KPress theme declarations, including
footnote popovers.

The paper’s role sizes, heading scale, and reading measure are explicit choices, made
once for every page.
Certificate selection, interactive panels, and diagram geometry stay with the explainer.

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

It scrolls each page to its foot first, so what a page places or loads lazily is in the
shot, and fails on console errors, a page wider than its viewport, math left untypeset,
any formula set in the wrong face (the Math rule above, its headline exception
included), and a row of cards off the centre of its line (more than a pixel between its
two slacks). `--page cases.html#n-11` walks one page at a fragment, and
`--press SELECTOR` presses a card or an atlas cell on each page that has one, then walks
and shoots what it opened, since a popover a script fills has no math until it opens.
`devtools.measure_site_pages cards` reports the rows the preview reads: each card
section’s lines, their cards’ widths and the slack at either end.
`devtools.measure_site_pages ladders` reports the rating ladders as laid out: every
rung’s height, each description’s box and the lines its words take, the room between the
diagram and whatever clips it sideways, and with `--shots DIR` a picture of the diagram
at each width, light and dark.
`tests/test_site_ladders.py` holds those rows and that room in a browser at nine widths,
the narrowest of each layout among them.
`devtools.measure_site_pages math` reports every formula’s face beside its text’s,
counted by surface. `devtools.measure_site_pages space` reports the space around every
table and heading (**Spacing**, above).
`tests/test_site_math_faces.py` runs the same walk wherever a browser is installed, over
the overview and its atlas popover, the results table, the frontier atlas and its case
popover, and two case records, with a control that marks a worded headline for serif
math and requires the walk to name it.
`tests/test_overview.py` holds the cards and chips to the rules above.

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
