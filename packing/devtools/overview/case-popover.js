// Every link to a case record (`a[data-case]`: an atlas-grid cell on the overview, an
// `n` in the frontier atlas) opens that record in the page's one case popover, framed
// narrow as a card's page popover is, with Expand going to the full record. Without
// this script the link goes to the record page itself.
//
// The frame is kept between cases: the second case opened only moves its fragment,
// which the record page answers without reloading (`case-view.js`).
//
// The popover's headline is the case, `n = 11`, as kpress's own math node, cloned from
// the template the popover carries and typeset by the site's math driver (`math.js`).
// It is mathematics standing alone, so its element is marked for the serif face.
(() => {
  const popover = document.querySelector("[data-case-popover]");
  const frame = popover?.querySelector("[data-case-frame]");
  const expand = popover?.querySelector("[data-case-expand]");
  const heading = popover?.querySelector("[data-case-title]");
  const mathTemplate = popover?.querySelector("template[data-case-math]");
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

  /**
   * Sets the headline to `text` as mathematics, or as plain text on a page whose
   * popover carries no math template.
   * @param {string} text
   */
  const title = (text) => {
    const node =
      mathTemplate instanceof HTMLTemplateElement
        ? mathTemplate.content.firstElementChild?.cloneNode(true)
        : undefined;
    const render = node instanceof HTMLElement ? node.querySelector(".kpress-math-render") : null;
    if (!(node instanceof HTMLElement) || !render) {
      heading.textContent = text;
      return;
    }
    render.textContent = `\\(${text}\\)`;
    const semantic = node.querySelector(".kpress-math-semantic");
    if (semantic) {
      semantic.textContent = text;
    }
    heading.replaceChildren(node);
    void globalThis.siteMath?.typeset(heading, true);
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
    title(`n = ${link.dataset.case ?? ""}`);
    popover.showPopover();
  });
})();
