// The front of a paper as laid out: the formats row's chips, then each line of the
// credits, so the two papers can be held to one front in the browser, where the cascade
// decides what a reader sees. One row an item, in reading order.
//
// A chip's row carries its words, where it goes, its font size, its weight and its box's
// height. A credit line's row carries its words; the weight the line is set at; `bold`,
// the weights of the names set in `strong` in it, space-separated; `links`, the weight
// of each link's words in it (the name's where the link carries one, with `(name)` after
// it, so an address can be told from a name); `gap`, the space from the bottom of the
// line above to the top of
// this one, in the credits' line heights, which is the grid's own gap between most lines
// and a line's space more before a paper's own credits and before the dates; `lines`,
// how many lines its words take; and `width_share`, its box's width over the reading
// column's, which is one for a credits grid of one column the width of the page.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} el */
  const weight = (el) => getComputedStyle(el).fontWeight;
  const column = document.querySelector(".kpress-prose") ?? document.body;
  const columnWidth = column.getBoundingClientRect().width;
  /** @type {Record<string, unknown>[]} */
  const rows = [];
  let index = 0;
  for (const chip of document.querySelectorAll(".doc-links .chip")) {
    const style = getComputedStyle(chip);
    const box = chip.getBoundingClientRect();
    rows.push({
      part: "chip",
      index,
      text: (chip.textContent ?? "").trim(),
      href: chip.getAttribute("href") ?? "",
      font_size: round(Number.parseFloat(style.fontSize)),
      weight: style.fontWeight,
      block_size: round(box.height),
      gap: 0,
      lines: 1,
      bold: "",
      links: "",
      width_share: round(box.width / columnWidth),
    });
    index += 1;
  }
  const credits = document.querySelector(".credits");
  if (!credits) {
    return rows;
  }
  const lineHeight = Number.parseFloat(getComputedStyle(credits).lineHeight);
  /** @type {DOMRect | null} */
  let previous = null;
  index = 0;
  for (const line of credits.children) {
    const style = getComputedStyle(line);
    const box = line.getBoundingClientRect();
    rows.push({
      part: "credit",
      index,
      text: (line.textContent ?? "").trim(),
      href: "",
      font_size: round(Number.parseFloat(style.fontSize)),
      weight: style.fontWeight,
      block_size: round(box.height),
      gap: previous ? round((box.top - previous.bottom) / lineHeight) : 0,
      lines: Math.round(box.height / Number.parseFloat(style.lineHeight)),
      bold: [...line.querySelectorAll("strong")].map(weight).join(" "),
      links: [...line.querySelectorAll("a")]
        .map((anchor) => {
          const name = anchor.querySelector("strong");
          return name ? `${weight(name)} (name)` : weight(anchor);
        })
        .join(" "),
      width_share: round(box.width / columnWidth),
    });
    previous = box;
    index += 1;
  }
  return rows;
};
