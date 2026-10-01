// Every card section as laid out: for each `.site-cards` block on the page, the section
// heading it follows, its width, and its cards grouped into rows by their top edge, each
// row with its cards' widths and sizes and the slack left at its start and at its end.
// A row is centred when the two slacks agree. Each card also reports its label and its
// headline's face, weight and size. Popovers are the cards' siblings but never cards.
() => {
  /** @param {string} family */
  const first = (family) => (family.split(",")[0] ?? "").trim().replace(/^["']|["']$/g, "");
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  const headings = [...document.querySelectorAll("h2")];
  /** @param {Element} block */
  const section = (block) => {
    const before = headings.filter(
      (heading) => heading.compareDocumentPosition(block) & Node.DOCUMENT_POSITION_FOLLOWING,
    );
    return before.at(-1)?.textContent?.trim() ?? "";
  };
  return [...document.querySelectorAll(".site-cards")]
    .filter((block) => block.getClientRects().length > 0)
    .map((block) => {
      const box = block.getBoundingClientRect();
      const cards = [...block.children].filter((child) => child.classList.contains("site-card"));
      /** @type {Map<number, Element[]>} */
      const rows = new Map();
      for (const card of cards) {
        const top = Math.round(card.getBoundingClientRect().top);
        rows.set(top, [...(rows.get(top) ?? []), card]);
      }
      return {
        section: section(block),
        block_width: round(box.width),
        rows: [...rows.values()].map((row) => {
          const boxes = row.map((card) => card.getBoundingClientRect());
          return {
            cards: row.length,
            sizes: row.map((card) => card.getAttribute("data-card-size") ?? ""),
            widths: boxes.map((rect) => round(rect.width)),
            start: round((boxes[0]?.left ?? box.left) - box.left),
            end: round(box.right - (boxes.at(-1)?.right ?? box.right)),
          };
        }),
        headlines: cards.map((card) => {
          const value = card.querySelector(".site-card-value");
          if (!value) {
            return null;
          }
          const style = getComputedStyle(value);
          return {
            label: (card.querySelector(".site-card-label")?.textContent ?? "").trim(),
            family: first(style.fontFamily),
            weight: style.fontWeight,
            size: style.fontSize,
          };
        }),
      };
    });
};
