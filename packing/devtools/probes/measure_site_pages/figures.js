// Every figure a page shows, as laid out: where its drawing stands in the column and what
// is lettered into it.
//
// A figure's drawing is what it holds besides its caption: its SVGs, canvases, pictures
// and films, taken together, so a pair set side by side is one drawing. `offset` is how
// far the drawing's centre stands from the centre of the reading column, in CSS pixels;
// `scrolls` says the drawing is wider than what holds it and scrolls sideways there, as a
// wide diagram does on a phone, where being centred means nothing. `beside` says the
// figure sets something else beside the drawing, a panel of controls, so the drawing is
// one part of a row and not what the figure centres.
//
// The box of a drawing can be centred while what is drawn in it is not: a packing set at
// the left of a wide canvas. `ink_offset` is how far the centre of what an SVG paints
// (its shapes and labels, less any ground that fills its canvas) stands from the centre
// of the column, as a share of the drawing's width.
//
// A drawing's own lettering is its labels. `texts` counts the text elements of its SVGs,
// and `longest` is the widest of them with its `share` of the drawing's width: a caption
// or a title lettered into a drawing is a run most of the drawing wide, where a label is
// a few words beside what it names. `sentences` are the labels that end as a sentence
// does, which is what a caption lettered into a drawing reads as. `caption` is the
// figure's `figcaption`, the first words of it, or empty where it has none.
//
// The first drawing of each figure is marked with `mark`, so the caller can shoot it.
(/** @type {{mark: string}} */ options) => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  const column =
    document.querySelector(".kpress-prose") ?? document.querySelector(".kpress") ?? document.body;
  const columnBox = column.getBoundingClientRect();
  const centre = columnBox.left + columnBox.width / 2;
  const rows = [];
  let index = 0;
  for (const figure of document.querySelectorAll("figure")) {
    if (!shown(figure)) {
      continue;
    }
    const drawings = [...figure.querySelectorAll("svg, canvas, img, video")].filter(
      (el) => shown(el) && !el.closest("figcaption") && !el.parentElement?.closest("svg"),
    );
    if (!drawings.length) {
      continue;
    }
    index += 1;
    const boxes = drawings.map((el) => el.getBoundingClientRect());
    const left = Math.min(...boxes.map((box) => box.left));
    const right = Math.max(...boxes.map((box) => box.right));
    const first = /** @type {Element} */ (drawings[0]);
    let holder = first.parentElement;
    while (holder && holder !== figure && holder.scrollWidth <= holder.clientWidth + 1) {
      holder = holder.parentElement;
    }
    const scrolls = !!holder && holder.scrollWidth > holder.clientWidth + 1;
    const beside = [...figure.querySelectorAll(".panel, .tip-panel, .ctl, button")].some(shown);
    /** @type {{text: string, share: number} | null} */
    let longest = null;
    let texts = 0;
    /** @type {string[]} */
    const sentences = [];
    let inkLeft = Number.POSITIVE_INFINITY;
    let inkRight = Number.NEGATIVE_INFINITY;
    for (const svg of drawings) {
      if (!(svg instanceof SVGSVGElement)) {
        continue;
      }
      const canvas = svg.getBoundingClientRect();
      const width = canvas.width;
      for (const part of svg.querySelectorAll("*")) {
        if (
          !(part instanceof SVGGeometryElement || part instanceof SVGTextElement) ||
          part.closest("defs, clipPath") ||
          !shown(part)
        ) {
          continue;
        }
        const box = part.getBoundingClientRect();
        if (box.width >= canvas.width - 1 && box.height >= canvas.height - 1) {
          continue;
        }
        inkLeft = Math.min(inkLeft, Math.max(box.left, canvas.left));
        inkRight = Math.max(inkRight, Math.min(box.right, canvas.right));
      }
      for (const text of svg.querySelectorAll("text")) {
        if (!shown(text) || getComputedStyle(text).display === "none") {
          continue;
        }
        texts += 1;
        const words = (text.textContent ?? "").trim().replace(/\s+/g, " ");
        if (/[.!?]$/.test(words) && words.split(" ").length >= 3) {
          sentences.push(words);
        }
        const share = width ? text.getBoundingClientRect().width / width : 0;
        if (!longest || share > longest.share) {
          longest = {
            text: (text.textContent ?? "").trim().replace(/\s+/g, " "),
            share: Math.round(share * 1000) / 1000,
          };
        }
      }
    }
    first.setAttribute(options.mark, `f${index}`);
    rows.push({
      figure: index,
      mark: `f${index}`,
      drawing: [...new Set(drawings.map((el) => el.tagName.toLowerCase()))].join(" "),
      named: (first.getAttribute("class") ?? "").split(" ")[0] || figure.className || "",
      drawings: drawings.length,
      drawing_width: round(right - left),
      column: round(columnBox.width),
      offset: round((left + right) / 2 - centre),
      ink_offset:
        inkRight > inkLeft
          ? Math.round((((inkLeft + inkRight) / 2 - centre) / (right - left)) * 1000) / 1000
          : 0,
      scrolls,
      beside,
      texts,
      longest: longest?.text ?? "",
      share: longest?.share ?? 0,
      sentences: sentences.join(" | "),
      caption: (figure.querySelector("figcaption")?.textContent ?? "")
        .trim()
        .replace(/\s+/g, " ")
        .slice(0, 60),
    });
  }
  return rows;
};
