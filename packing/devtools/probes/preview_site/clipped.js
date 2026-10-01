// Every wide block, table, filter bar and count whose box runs past the nearest ancestor
// that clips or scrolls sideways, with how far it runs past each side. Such a block is
// either cut off, as a table sized from the window is under a narrow page's clip, or
// spilling over its panel's margin, as a grid wider than its popover does. A table inside
// its own scrolling wrap is not looked at, since scrolling there is the wrap's job; the
// wrap is. `scrollbar` first narrows the page by that many pixels, as a classic scrollbar
// does: the window (`100vw`, a media query) keeps its width and the layout loses the
// scrollbar's, which is the difference a block sized from the window gets wrong.
(/** @type {{scrollbar?: number} | undefined} */ options) => {
  const scrollbar = options?.scrollbar ?? 0;
  if (scrollbar > 0) {
    document.documentElement.style.inlineSize = `calc(100vw - ${scrollbar}px)`;
  }
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const name = (el) =>
    [el.tagName.toLowerCase(), ...[...el.classList].filter((item) => !item.startsWith("kpress-"))]
      .join(".")
      .slice(0, 60);
  const blocks =
    ".site-wide, .site-table-tools, .site-count, .site-table-wrap, .kpress-table-wrap, " +
    ".site-result-bounds, .site-result-case-list, .site-film-frame";
  const found = [];
  for (const el of document.querySelectorAll(blocks)) {
    if (el.getClientRects().length === 0) {
      continue;
    }
    const box = el.getBoundingClientRect();
    for (let frame = el.parentElement; frame; frame = frame.parentElement) {
      if (getComputedStyle(frame).overflowX === "visible") {
        continue;
      }
      const left = frame.getBoundingClientRect().left + frame.clientLeft;
      const before = left - box.left;
      const after = box.right - (left + frame.clientWidth);
      if (before > 0.5 || after > 0.5) {
        found.push({
          block: name(el),
          frame: name(frame),
          left: round(Math.max(0, before)),
          right: round(Math.max(0, after)),
        });
      }
      break;
    }
  }
  if (scrollbar > 0) {
    document.documentElement.style.inlineSize = "";
  }
  return found;
};
