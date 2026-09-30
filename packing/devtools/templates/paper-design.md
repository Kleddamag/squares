# Design System

This is the one description of how every page of the site looks: the explainer, the
overview, the frontier atlas, the tutorial and the Visualize section.
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
| Space above a section heading | 32.4px | 37.8pt | `--paper-section-space`: 1.8 of the prose base on screen, 2.8 in print |
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
| Verification rung (`V`) | 250 | 0.06 | The blue square, `#166eac` |
| Confirmation rung (`C`) | 158 | 0.06 | The green square, `#158655` |
| Significance rung (`S`) | 250 | 0.008 | Gray |

Every chip carries the page’s own text colour, black in light mode, on a light fill, and
in dark mode light text on a dark fill.
A rung’s fill is `oklch(base + step × level, 0.06, hue)` for levels 0 to 5, with base
96% and step −3.5% in light mode, so level 0 sits close to the page background and it
darkens to 78.5% as the rung rises, and base 25% and step +4% in dark mode, so it
lightens from near the dark background at 25% to 45%. The two are `--site-rung-base` and
`--site-rung-step`. A plain chip is a 16% tint of the muted gray over the page
background, and an accent chip a 22% tint of the accent.
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

## Site Components

Each component is defined once in [site.css](site.css) and used on every page that needs
it.

- **Navigation bar.** One fixed-width row of sans links in the page’s header slot, the
  same on every page, the explainer and the workbench included, led by the site name,
  “Square Packing”, set in capitals by CSS (`text-transform`, lightly tracked) so its
  text is unchanged, and a step heavier.
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
  block starts one shared space under its rule, `--site-page-top` (2rem, in
  `site-nav.css`): KPress’s document padding above the column is dropped on screen, the
  column’s own top padding is the token, and the first block (a hero or a document’s
  title) adds no margin of its own.
  On the explainer the source chips sit in that space and the title starts the token
  below them. Print keeps KPress’s spacing, so the explainer’s PDF does not move.
  Its entries are Overview, Frontier, Results, Explainer, Tutorial, Visualize and
  GitHub. Visualize leads to the film (`visualize.html`) and is current on both pages of
  the Visualize section, the film and the workbench.
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
  border, a hairline between tabs, in the bar’s sans at 0.9rem and medium weight: a tab
  is gray, takes the nav items’ wash and accent on hover, and the current tab is filled
  with a 16% accent tint over the page background in the page’s own text colour.
  It is `.site-tabs`, rendered by `render_overview.visualize_tabs`, and defined in
  `site-nav.css` rather than `site.css` because the workbench carries only the bar’s
  stylesheet. On the film’s page it opens the document; on the workbench it sits in the
  application shell under the bar, above the application.
  It is hidden in print and in the embed view.

- **Theme control.** A small gray gear, an inline SVG, ends the navigation bar on every
  page, the explainer and the workbench included.
  From 80rem wide it leaves the links’ centred track for the bar’s far right, its edge
  over the right end of the rule under the bar; narrower, it ends the row of links.
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
  sections are `h2`s. A page that has a title (the frontier atlas, the case records)
  sets it in the hero, centred, with a subtitle under it such as “Every tracked case, n
  = 1 to 324”. The subtitle is the sans face at 1.1 times the sans base
  (`--site-subtitle-scale`, about 21px), in the page’s own text colour, never gray, with
  the same space above it and below it (`--site-subtitle-space`, 1.25rem). The page
  title style (every hero `h1`, and `.site-title`) is the sans face in upright caps (not
  KPress’s italic `h2`) at 1.5 times the sans base, centred.
  The homepage’s first section, The Square Packing Problem, takes it through
  `.site-title`, so it reads as the frontier atlas’s title does.

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
  a data URI on every page, the workbench included; the same drawing is the mark in the
  navigation bar, drawn there in the bar’s ink, so it is light in dark mode.
  In both, the container’s frame is exactly one pixel of the drawing at its size (16px
  in a tab, 18px in the bar; `packing_svg(frame_px=)`), its outer edge on the drawing’s
  edge and snapped to the pixel grid, so the container reads as a square: one crisp
  pixel on a 1x screen, two on a 2x screen.
  The homepage’s hero is case 53, centered under the title in the page’s ink and linked
  to its row in the frontier atlas.

- **Cards.** A card is a summary with square corners, a thin border, a caps label, a
  value and a supporting note.
  A card section is one grid in the wide track, in a `.site-cards-frame` the grid
  measures itself against.
  Four or more cards fill its columns from the left, as many 16rem columns as fit.
  Three or fewer centre as a group, each card as wide as it would be in a full row, so a
  short section lines up with a long one; below four columns the row holds them anyway.
  A card works one of two ways.
  Most cards open a popover that shows where they lead, and the popover ends in one
  button that goes there, centred at its foot.
  A direct card is instead itself the link (`link_card`), for a target whose address or
  picture is the whole of what a preview would say.
  **A direct card always opens its target in a new tab** (`target="_blank"`,
  `rel="noopener noreferrer"`), whether it is a page or file of this site or a place off
  it, so the page the reader chose it from stays where they left it.
  - When the card leads to another page of the site, the popover renders that page
    itself, narrow, in a frame: the page at the same address with `?view=embed` added
    before any fragment, so a filtered view such as `frontier.html?recent=true` or a
    case such as `frontier.html#n-11` arrives as it will be seen.
    The embed view drops the navigation bar and sends every link out of the frame to the
    full window. The button is **Expand**, which opens the page at full size; a
    repository document also offers its source “On GitHub”, which opens it on `main`.
    Every repository link on the site names `main`, never a commit, and is made by
    `devtools/repo_links.py`.
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
    A result’s row is on the results page, so its card is a page card, with `→` for its
    icon, that previews rather than frames: the button, **Open T-NNN in the results
    table**, goes to `all-results.html#t-nnn`. A row on the overview itself would
    scroll, with `↓`.

  The frame loads only when its popover first opens, so the overview stays light.
  The popover is a native `popover` panel with square corners over a faint scrim, set in
  sans, closed by its `×`, by Escape, or by a click outside, and it works without
  scripting. A card gains a gentle wash on hover.
  Its gray corner icon and the popover’s button both show where the button goes: `↓` to
  a row on this page, `↗` off the site, `→` to another page of the site.

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

- **Atlas grid.** The atlas opens with every tracked case, n = 1 to 324, as a square
  drawing in the page’s ink with its n beneath.
  The grid bleeds past the wide track as the window grows, to 140rem less the page
  gutters, and its cells keep a readable size (at least 6.4rem, 4.6rem on a phone), so a
  wider screen shows more cases per row: 4 at 390 pixels, 11 at 1280, 17 at 1920 and 20
  at 2560. A cell washes on hover and is a link to its case record.
  The cells ship in a `<template>` and are placed only as the grid nears the viewport
  (`overview/atlas-grid.js`), so they add nothing to the first paint; each drawing is
  400 units across, fine enough to show large.

- **Atlas popover.** Pressing a cell opens the page’s one atlas popover on that case, a
  card popover in every other way (square corners, the scrim, the caps label, the close
  cross, Escape and a click outside).
  It shows what the ascent film’s panel shows for the case, beside the drawing large:
  the gap bar (a number line from one below $\lceil\sqrt{n}\,\rceil$ to two above it,
  the integers and the values of $\sqrt{n}$ and $\sqrt{n} + 1$ marked, the two bounds as
  bold rules with their values above and the open span between them shaded); under
  PROVEN the bound as one statement, the proved lower bound in scarlet and the best
  known side in green, with the star for a recent lower bound; the badges; the citation,
  one line per bound with this project’s note; and what is OPEN. The facts are the
  film’s own, read from the atlas figure and `bound-citations.json` into one JSON
  element (`atlas_film_facts`), and the script fills the popover from them with kpress’s
  math nodes, never HTML strings.
  It ends in **See All Cases**, which goes to `cases.html#n-N` at full size, and arrows,
  and the arrow keys, step to the neighbouring case.
  The two arrows are one drawn SVG arrow (`step_arrow`), the back one mirrored, never
  the `←` and `→` characters: the site’s text face has no arrow glyphs, so browsers drew
  the two from different fallback fonts.
  Opening moves focus to the close cross; closing returns it to the case’s cell.
  On a phone the panel takes the width less half a rem each side, scrolls inside, keeps
  its button in a sticky foot, and has a 2.75rem close target.

- **Case records.** Every case has one record at one address, `cases.html#n-11`. The n
  of a frontier-atlas row opens it in the one case popover that page carries, a
  page-kind popover framing the record in its embed view, with **Expand** to the full
  record (`overview/case-popover.js`); an atlas-grid cell reaches it through the atlas
  popover’s button. Without scripting either link goes to the record itself.
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
  film at full size under the section tabs and a page title, “Visualize”, with the
  subtitle “The ascent, n = 1 to 324”. It is as wide as the window allows less the page
  gutters, up to 120rem, but never so tall that it will not fit the window whole
  (`.site-film-frame`), and embedded as the explainer embeds its film: inline, with its
  controls, fetching nothing until a reader presses play (`preload="none"`), and showing
  its poster until then, `ascent-n1-324-poster.png`, published beside the explainer’s
  assets, at the video’s own 16:9, so starting playback moves nothing.
  A caption and a note in the support colour follow at the reading measure: what the
  film shows, its length, the shorter 1 to 100 film, the release both are on, and the
  Workbench.

- **Tables.** KPress tables in the sans face, with sortable headers, filters above,
  group rows, and an expandable row whose summary stays sans so its math does.
  On a phone, the results table becomes one card per row.
  In the results table a result’s standing chip sits under its rungs, and a Standing
  filter selects by it; a date cell says what it dates, `published` or `established`, in
  the support colour.

- **Results page.** Every registered result is one row of the results table on its own
  page, `all-results.html`, “Results” in the navigation bar after Frontier.
  (`results.html` is `RESULTS.md` rendered as a reader document, so the table’s page
  takes the other name.)
  The page has the frontier atlas’s shape: a hero title, “Every Result”, whose id is
  `every-result`, a subtitle with the count, the prose that defines the ratings and
  standings, and the table with its filters.
  Each row keeps its id, the result’s own (`#t-018`), which is where the overview’s
  cards, its recent list and replay table, and each case record’s results link.
  The overview keeps the newest results and ends that list with a “See all results →”
  line in the sans face at the note size.
  The table used to be the overview’s Every Result section, and its old addresses still
  arrive: the overview’s `overview/forward.js` sends `#every-result` and any `#t-nnn` to
  the results page with the fragment kept, and every other fragment the overview lacks
  to the explainer, as before.
  `tests/node/overview_forward/` runs the forwarder, and `tests/test_overview.py` holds
  every row id to the form it recognises.

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

`paper-type.css` owns the type base, the reading measure, the h2 scale, the sans/prose
size ratio, the paper’s medium and bold weights and the role scales; the explainer’s
shell and `site.css` alias them and never restate them.
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

It fails on console errors, a page wider than its viewport, math left untypeset, and any
formula whose face disagrees with the text around it.
`tests/test_overview.py` holds the cards and chips to the rules above.

The linear-program display is reflowed within the print column.
`check_print_layout` guards its width so an overflowing equation cannot silently shrink
the whole PDF page.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
