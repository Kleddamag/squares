// The columns of every shared data table (`.site-table`) as laid out, and what makes its
// rows tall. For each table that is showing: its classes, the heading above it, its
// width and the width of what scrolls it sideways (`frame_width`, the nearest ancestor
// that clips or scrolls, with `scrolls` how far the table runs past it, 0 when it
// fits), how many rows show, and `layout`, `table` or, on a phone, where a row is a
// card, `cards`. `top` and `height` place the component, the table with its filter bar,
// on the page, to find it in a full-page screenshot.
//
// In the `table` layout each column is reported under its header's words with its width
// and what its cells hold: `lines`, the most lines any cell of it takes, and `tallest`,
// the tallest row whose height this column's cell sets, with that row's key, its height
// and the lines the cell takes. A row's height is set by the cell whose content is
// tallest, so a column that never sets one reports no `tallest`. A cell's content is
// measured as the box around what it holds, and its lines as that height over the
// cell's own line height: exact for a cell of words, and a count of line boxes at the
// cell's line height for one of chips or math, whose lines are taller. `broken` lists the
// words of the column that a line break splits, which a cell too narrow for its longest
// word does to it ("Queuingthe" over "orydotcom"); a break after a hyphen or a slash is
// a word's own and is not counted, and typeset math is passed over.
//
// In the `cards` layout no column has a width and none sets a row's height alone; the
// table reports its tallest card (`tallest_row`, as it does in either layout) and each
// cell's class with the most lines it takes, so a cell that wraps badly on a phone shows
// there.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  /** @param {Element} el */
  const words = (el) => (el.textContent ?? "").replace(/\s+/g, " ").trim();
  /** The height of what a cell holds, and the lines that is at the cell's line height.
   * @param {Element} cell */
  const content = (cell) => {
    const range = document.createRange();
    range.selectNodeContents(cell);
    const height = range.getBoundingClientRect().height;
    const style = getComputedStyle(cell);
    const line = Number.parseFloat(style.lineHeight) || Number.parseFloat(style.fontSize) * 1.2;
    return {
      height: round(height),
      lines: height > 0 ? Math.max(1, Math.round(height / line)) : 0,
    };
  };
  /** The words of a cell that a line break splits, outside its typeset math: each run
   * of characters up to a space, a hyphen or a slash that sits on more than one line.
   * @param {Element} cell */
  const broken = (cell) => {
    /** @type {string[]} */
    const found = [];
    const walker = document.createTreeWalker(cell, NodeFilter.SHOW_TEXT);
    const range = document.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (node.parentElement?.closest(".katex")) {
        continue;
      }
      for (const word of (node.textContent ?? "").matchAll(/[^\s\-\u2010-\u2014/]+/g)) {
        range.setStart(node, word.index);
        range.setEnd(node, word.index + word[0].length);
        const tops = new Set([...range.getClientRects()].map((rect) => Math.round(rect.top)));
        if (tops.size > 1) {
          found.push(word[0]);
        }
      }
    }
    return found;
  };
  /** A row's key: its id, the result it names, or its first cell's words.
   * @param {HTMLTableRowElement} row */
  const key = (row) =>
    row.id || row.getAttribute("data-result") || words(row.cells[0] ?? row).slice(0, 24);
  /** The width inside the nearest ancestor that clips or scrolls `element` sideways,
   * or the page's own layout width where none does.
   * @param {Element} element */
  const frameWidth = (element) => {
    for (let frame = element.parentElement; frame; frame = frame.parentElement) {
      if (getComputedStyle(frame).overflowX !== "visible") {
        return frame.clientWidth;
      }
    }
    return document.documentElement.clientWidth;
  };
  /** The heading a table sits under.
   * @param {Element} table */
  const section = (table) => {
    for (let at = /** @type {Element | null} */ (table); at; at = at.parentElement) {
      for (let before = at.previousElementSibling; before; before = before.previousElementSibling) {
        if (before.matches("h1, h2, h3")) {
          return words(before);
        }
      }
    }
    return "";
  };
  return [...document.querySelectorAll("table.site-table")]
    .filter((table) => table instanceof HTMLTableElement && shown(table))
    .map((found) => {
      const table = /** @type {HTMLTableElement} */ (found);
      const wrap = table.closest(".site-table-wrap") ?? table;
      const bar = wrap.previousElementSibling;
      const tools = bar?.classList.contains("site-table-tools") && shown(bar) ? bar : wrap;
      const top = tools.getBoundingClientRect().top;
      const box = table.getBoundingClientRect();
      const frame = frameWidth(table);
      const rows = [...(table.tBodies[0]?.rows ?? [])].filter(
        (row) => shown(row) && !row.classList.contains("site-group-row"),
      );
      const heads = [...(table.tHead?.rows[0]?.cells ?? [])];
      const cards = !heads.some(shown);
      const base = {
        table: [...table.classList].filter((item) => !item.startsWith("kpress-")).join("."),
        section: section(table),
        layout: cards ? "cards" : "table",
        table_width: round(box.width),
        frame_width: round(frame),
        scrolls: Math.max(0, round(box.width - frame)),
        shown_rows: rows.length,
        top: Math.round(top + window.scrollY),
        height: Math.round(wrap.getBoundingClientRect().bottom - top),
      };
      const measured = rows.map((row) => ({
        key: key(row),
        height: round(row.getBoundingClientRect().height),
        cells: [...row.cells].map((cell) => ({
          ...content(cell),
          name: cell.className,
          broken: broken(cell),
        })),
      }));
      const tallestRow = measured.reduce(
        (best, row) => (best && best.height >= row.height ? best : row),
        /** @type {(typeof measured)[number] | null} */ (null),
      );
      const names = cards
        ? [...new Set(measured.flatMap((row) => row.cells.map((cell) => cell.name)))]
        : heads.map(words);
      const columns = names.map((name, index) => {
        const cellsOf = measured.flatMap((row) => {
          const cell = cards ? row.cells.find((item) => item.name === name) : row.cells[index];
          return cell ? [{ row, cell }] : [];
        });
        // The rows this column's cell sets the height of: none of the row's other cells
        // holds more.
        const sets = cards
          ? []
          : cellsOf.filter(({ row, cell }) =>
              row.cells.every((other) => other.height <= cell.height),
            );
        const tallest = sets.reduce(
          (best, item) => (best && best.row.height >= item.row.height ? best : item),
          /** @type {(typeof sets)[number] | null} */ (null),
        );
        const head = heads[index];
        return {
          column: name,
          width: cards || !head ? null : round(head.getBoundingClientRect().width),
          lines: Math.max(0, ...cellsOf.map(({ cell }) => cell.lines)),
          broken: [...new Set(cellsOf.flatMap(({ cell }) => cell.broken))],
          tallest: tallest
            ? { row: tallest.row.key, height: tallest.row.height, lines: tallest.cell.lines }
            : null,
        };
      });
      return {
        ...base,
        tallest_row: tallestRow ? { row: tallestRow.key, height: tallestRow.height } : null,
        columns,
      };
    });
};
