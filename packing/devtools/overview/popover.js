/* The square popover. A card's link carries `data-popover`, and with JavaScript on a
   plain click opens the popover instead of following the link; a modified click (a new
   tab, a new window) and every card without the attribute still navigate. With
   JavaScript off every card is an ordinary link. `templates/site-design.md` describes
   the component ("The square popover").

   - `result`: the card again, with the full record from the results table's expanded
     row (the claim, the records, the next rung). The button shows the row in the table.
   - `page`: the site page the card links, rendered narrowly in a same-origin frame. The
     button opens it full size.
   - `document`: the card's summary and the document's opening section, which the page
     carries in a `<template class="site-card-preview">` rendered at build time. The
     button opens the document on GitHub.

   The popover is a modal `<dialog>`: Escape and a click outside it close it, and focus
   returns to the card. Its buttons draw kpress's own icons from the page's sprite. */
(() => {
  const SVG = "http://www.w3.org/2000/svg";

  /** @param {string} name a kpress sprite icon */
  const icon = (name) => {
    const svg = document.createElementNS(SVG, "svg");
    svg.setAttribute("aria-hidden", "true");
    const use = document.createElementNS(SVG, "use");
    use.setAttribute("href", `#kpress-icon-${name}`);
    svg.append(use);
    return svg;
  };

  const dialog = document.createElement("dialog");
  dialog.className = "kpress site-popover";
  const bar = document.createElement("div");
  bar.className = "site-popover-bar";
  const title = document.createElement("span");
  title.className = "site-popover-title";
  const expand = document.createElement("a");
  expand.className = "site-popover-button site-popover-expand";
  const expandLabel = document.createElement("span");
  const expandIcon = icon("maximize");
  expand.append(expandIcon, expandLabel);
  const close = document.createElement("button");
  close.type = "button";
  close.className = "site-popover-button site-popover-close";
  close.setAttribute("aria-label", "Close");
  close.append(icon("x"));
  bar.append(title, expand, close);
  const body = document.createElement("div");
  body.className = "site-popover-body";
  dialog.append(bar, body);

  /** @type {HTMLElement | null} */
  let opener = null;

  close.addEventListener("click", () => dialog.close());
  expand.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      dialog.close();
    }
  });
  dialog.addEventListener("close", () => {
    body.replaceChildren();
    opener?.focus();
    opener = null;
  });

  /**
   * The card without its stretched link, to show inside the popover.
   * @param {Element} card
   */
  const cardCopy = (card) => {
    const copy = /** @type {Element} */ (card.cloneNode(true));
    for (const link of copy.querySelectorAll(".site-card-link")) {
      const span = document.createElement("span");
      span.append(...link.childNodes);
      link.replaceWith(span);
    }
    for (const preview of copy.querySelectorAll("template")) {
      preview.remove();
    }
    return copy;
  };

  /**
   * What each kind of card shows, or null to let the link navigate.
   * @param {HTMLAnchorElement} link
   * @param {Element} card
   * @returns {{ label: string, icon: string, heading: string, nodes: Node[] } | null}
   */
  const content = (link, card) => {
    const kind = link.getAttribute("data-popover");
    const heading = (link.textContent ?? "").trim();
    if (kind === "result") {
      const row = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      const record = row?.querySelector(".site-details-body");
      if (!record) {
        return null;
      }
      const id = card.querySelector(".site-card-id")?.textContent ?? heading;
      return {
        label: "Show in the table",
        icon: "list",
        heading: id,
        nodes: [cardCopy(card), record.cloneNode(true)],
      };
    }
    if (kind === "page") {
      const frame = document.createElement("iframe");
      frame.className = "site-popover-frame";
      frame.src = link.href;
      frame.title = heading;
      return { label: "Open the page", icon: "maximize", heading, nodes: [frame] };
    }
    if (kind === "document") {
      const preview = card.querySelector("template.site-card-preview");
      if (!(preview instanceof HTMLTemplateElement)) {
        return null;
      }
      const prose = document.createElement("div");
      prose.className = "kpress kpress-prose site-popover-prose";
      prose.append(preview.content.cloneNode(true));
      return {
        label: "Open on GitHub",
        icon: "external-link",
        heading,
        nodes: [cardCopy(card), prose],
      };
    }
    return null;
  };

  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      !(event.target instanceof Element)
    ) {
      return;
    }
    const link = event.target.closest("a.site-card-link[data-popover]");
    const card = link?.closest(".site-card");
    if (!(link instanceof HTMLAnchorElement) || !card || dialog.contains(link)) {
      return;
    }
    const shown = content(link, card);
    if (!shown) {
      return;
    }
    event.preventDefault();
    if (!dialog.isConnected) {
      document.body.append(dialog);
    }
    opener = link;
    dialog.dataset.kind = link.getAttribute("data-popover") ?? "";
    dialog.setAttribute("aria-label", shown.heading);
    title.textContent = shown.heading;
    expand.href = link.href;
    expandLabel.textContent = shown.label;
    expandIcon.firstElementChild?.setAttribute("href", `#kpress-icon-${shown.icon}`);
    body.replaceChildren(...shown.nodes);
    body.scrollTop = 0;
    dialog.showModal();
    void window.siteMath?.typeset(body);
  });
})();
