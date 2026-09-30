// Every link to a case record (`a[data-case]`: an atlas-grid cell on the overview, an
// `n` in the frontier atlas) opens that record in the page's one case popover, framed
// narrow as a card's page popover is, with Expand going to the full record. Without
// this script the link goes to the record page itself.
//
// The frame is kept between cases: the second case opened only moves its fragment,
// which the record page answers without reloading (`case-view.js`).
(() => {
  const popover = document.querySelector("[data-case-popover]");
  const frame = popover?.querySelector("[data-case-frame]");
  const expand = popover?.querySelector("[data-case-expand]");
  const heading = popover?.querySelector("[data-case-title]");
  if (
    !(popover instanceof HTMLElement) ||
    !(frame instanceof HTMLIFrameElement) ||
    !(expand instanceof HTMLAnchorElement) ||
    !(heading instanceof HTMLElement) ||
    typeof popover.showPopover !== "function"
  ) {
    return;
  }

  /** @param {string} href */
  const embedded = (href) => {
    const url = new URL(href, location.href);
    url.searchParams.set("view", "embed");
    return url.href;
  };

  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    const link = event.target instanceof Element ? event.target.closest("a[data-case]") : null;
    const href = link instanceof HTMLAnchorElement ? link.getAttribute("href") : null;
    if (!(link instanceof HTMLAnchorElement) || !href) {
      return;
    }
    event.preventDefault();
    const target = embedded(href);
    if (frame.src !== target) {
      frame.src = target;
    }
    expand.href = href;
    heading.textContent = `n = ${link.dataset.case ?? ""}`;
    popover.showPopover();
  });
})();
