// Every open popover as laid out: its box, the window it is in, the margin the window
// keeps above and below it and at its sides, and how much of what it holds it shows
// without scrolling. A popover that frames a page (the case popover frames `cases.html`)
// scrolls inside its frame, not itself, so its share is the frame's: the frame's height
// over the height of the page in it. Lengths are CSS pixels and a share is from 0 to 1.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 10) / 10;
  /** @param {Element} el */
  const name = (el) =>
    [el.tagName.toLowerCase(), ...[...el.classList].filter((item) => !item.startsWith("kpress-"))]
      .join(".")
      .slice(0, 60);
  return [...document.querySelectorAll(":popover-open")].map((popover) => {
    const box = popover.getBoundingClientRect();
    const frame = popover.querySelector("iframe");
    const page = frame?.contentDocument?.scrollingElement ?? null;
    const shown = frame && page ? frame.clientHeight : popover.clientHeight;
    const content = page ? page.scrollHeight : popover.scrollHeight;
    return {
      popover: popover.id ? `#${popover.id}` : name(popover),
      window_height: window.innerHeight,
      inline: round(box.width),
      block: round(box.height),
      above: round(box.top),
      below: round(window.innerHeight - box.bottom),
      beside: round(Math.min(box.left, window.innerWidth - box.right)),
      scrolls: frame ? "its frame" : "itself",
      shown,
      content,
      share: content > 0 ? Math.min(1, Math.round((shown / content) * 100) / 100) : 1,
    };
  });
};
