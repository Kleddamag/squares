// Where a page's header stands, from the top of the document in CSS pixels: the
// navigation bar, the rule under it, the section tabs a page of a section carries (the
// Visualize section's Film and Workbench) and the first block of the page's content.
// The rule is the lower border of the header slot, or of the bar where the slot hands
// its rule to the bar; the first block is an application's viewport, or whatever opens
// a page's column, a title, a picture or a table, passing over what is out of the flow.
// `preview_site.tabs_problems` holds the tabs to their place below the rule with it.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} el */
  const box = (el) => {
    const rect = el.getBoundingClientRect();
    return {
      top: round(rect.top + window.scrollY),
      bottom: round(rect.bottom + window.scrollY),
      left: round(rect.left),
      right: round(rect.right),
    };
  };
  /** @param {Element} el */
  const name = (el) =>
    [
      el.tagName.toLowerCase() + (el.id ? `#${el.id}` : ""),
      ...[...el.classList].filter((item) => !item.startsWith("kpress-")),
    ]
      .join(".")
      .slice(0, 60);
  /** @param {Element} el */
  const inFlow = (el) => {
    if (el.getClientRects().length === 0 || el.matches("script, style, template")) {
      return false;
    }
    const position = getComputedStyle(el).position;
    return position !== "absolute" && position !== "fixed" && el.getBoundingClientRect().height > 0;
  };
  const nav = document.querySelector(".site-nav");
  const header = document.querySelector(".kpress-site-header");
  const tabs = document.querySelector(".site-tabs");
  /** @param {Element | null} el */
  const ruled = (el) =>
    el !== null && Number.parseFloat(getComputedStyle(el).borderBottomWidth) > 0;
  const owner = [header, nav].find(ruled) ?? null;
  let rule = null;
  if (owner) {
    const edge = box(owner);
    const width = Number.parseFloat(getComputedStyle(owner).borderBottomWidth);
    rule = { ...edge, top: round(edge.bottom - width), on: name(owner) };
  }
  /** @type {Element | null} */
  let first = document.querySelector("#viewport, .kpress-long-text, .cert-page");
  while (first && !first.matches("#viewport") && first.matches("div, header, section, article")) {
    const child = [...first.children].find(inFlow);
    if (!child) {
      break;
    }
    first = child;
  }
  return {
    nav: nav && box(nav),
    rule,
    tabs: tabs && {
      ...box(tabs),
      current: tabs.querySelector('[aria-current="page"]')?.textContent ?? null,
    },
    first: first && { ...box(first), block: name(first) },
  };
};
