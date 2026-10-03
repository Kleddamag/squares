// Every word, in what the page has open, that is set across more than one line: a run of
// characters with no space in it whose glyphs sit in two or more line boxes. A browser
// breaks one after a hyphen or a slash and at other punctuation, which is ordinary, and,
// under `overflow-wrap` or `word-break`, anywhere at all, which is how "lower" comes out
// as "low" over "er" in a column squeezed to a few characters. The probe only reports;
// which breaks are faults is `preview_site.split_problem`'s to say.
//
// `root` names where to look, every open popover by default. A page framed inside a root
// (a card's popover frames its page) is looked at too, from its own `body`, since a
// local build's frames are the page's own origin. Typeset mathematics, drawings and
// anything not laid out are passed over: a formula's glyphs sit at many heights by design.
//
// Each word is reported with the pieces it was cut into, the element holding it and the
// nearest block around that, its own width in CSS pixels (with a chip's padding and
// border and whatever shares its inline box, which have to fit too), and the width of a
// line of that block, which is what it had to fit on. `code` says it is a name set as code or as a
// chip, and `prose` that it stands in a document's own running text, which KPress sets,
// rather than in a popover or a block the site builds (those are marked sans).
(/** @type {{root?: string} | undefined} */ options) => {
  const root = options?.root ?? ":popover-open";
  const passed = "script, style, template, noscript, svg, .katex, .kpress-math";
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const name = (el) =>
    [el.tagName.toLowerCase(), ...[...el.classList].filter((item) => !item.startsWith("kpress-"))]
      .join(".")
      .slice(0, 60);
  /**
   * The nearest box around `el` that lays its text out in lines of its own.
   * @param {Element} el
   * @param {Window} view
   */
  const block = (el, view) => {
    /** @type {Element | null} */
    let at = el;
    while (at?.parentElement && /^(inline|contents)$/.test(view.getComputedStyle(at).display)) {
      at = at.parentElement;
    }
    return at ?? el;
  };
  /** @type {{word: string, pieces: string[], host: string, block: string, code: boolean,
   *   prose: boolean, width: number, line: number, frame: string}[]} */
  const found = [];
  /**
   * @param {Element} within
   * @param {string} frame
   */
  const scan = (within, frame) => {
    const doc = within.ownerDocument;
    const view = doc.defaultView;
    if (!view) {
      return;
    }
    const walker = doc.createTreeWalker(within, NodeFilter.SHOW_TEXT);
    const range = doc.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const host = node.parentElement;
      const text = node.nodeValue ?? "";
      if (!host || host.closest(passed) || !text.trim()) {
        continue;
      }
      for (const match of text.matchAll(/\S+/g)) {
        const word = match[0];
        range.setStart(node, match.index);
        range.setEnd(node, match.index + word.length);
        const rects = [...range.getClientRects()].filter((rect) => rect.width > 0);
        if (rects.length < 2) {
          continue;
        }
        // The line each character sits on: a new one starts where a character's box
        // begins below the middle of the one before it.
        /** @type {string[]} */
        const pieces = [];
        let piece = "";
        /** @type {DOMRect | null} */
        let last = null;
        for (let index = 0; index < word.length; index += 1) {
          range.setStart(node, match.index + index);
          range.setEnd(node, match.index + index + 1);
          const box = range.getBoundingClientRect();
          if (last !== null && box.top > last.top + last.height / 2) {
            pieces.push(piece);
            piece = "";
          }
          piece += word.charAt(index);
          last = box;
        }
        pieces.push(piece);
        if (pieces.length < 2) {
          continue;
        }
        const around = block(host, view);
        const style = view.getComputedStyle(around);
        // What has to fit on the line is more than the letters: a chip's padding and
        // border, and, where the word sits in an inline box of its own (`.site-name`),
        // whatever shares the box, such as the comma after a name.
        const chip = host.closest("code, .site-chip");
        const box = chip ? view.getComputedStyle(chip) : null;
        const edges = box
          ? parseFloat(box.paddingLeft) +
            parseFloat(box.paddingRight) +
            parseFloat(box.borderLeftWidth) +
            parseFloat(box.borderRightWidth)
          : 0;
        if (style.display.startsWith("inline")) {
          rects.length = 0;
          const texts = doc.createTreeWalker(around, NodeFilter.SHOW_TEXT);
          for (let part = texts.nextNode(); part; part = texts.nextNode()) {
            range.selectNodeContents(part);
            rects.push(...[...range.getClientRects()].filter((rect) => rect.width > 0));
          }
        }
        found.push({
          word,
          pieces,
          host: name(host),
          block: name(around),
          code: chip !== null,
          prose:
            host.closest(".kpress-prose") !== null &&
            host.closest('[popover], [data-kpress-prose-font="sans"]') === null,
          width: round(rects.reduce((sum, rect) => sum + rect.width, edges)),
          line: round(
            around.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight),
          ),
          frame,
        });
      }
    }
    for (const inner of within.querySelectorAll("iframe")) {
      const body = inner.contentDocument?.body;
      if (body) {
        scan(body, name(inner));
      }
    }
  };
  for (const within of document.querySelectorAll(root)) {
    scan(within, "");
  }
  return found;
};
