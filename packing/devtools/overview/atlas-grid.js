// The homepage's grid of every known-best packing. Its cells arrive in a <template>,
// which the browser parses but does not lay out, and are placed only when the grid
// comes near the viewport, so they cost the page's first paint nothing. Pointing at a
// cell, or focusing it, shows its details in one hover card kept inside the window.
(() => {
  for (const grid of document.querySelectorAll("[data-atlas-grid]")) {
    const template = grid.querySelector("template");
    const tip = grid.querySelector(".site-atlas-tip");
    if (!(template instanceof HTMLTemplateElement) || !(tip instanceof HTMLElement)) {
      continue;
    }
    const cells = document.createElement("div");
    cells.className = "site-atlas-cells";

    /** @param {Element} cell */
    const show = (cell) => {
      const detail = cell.querySelector(".site-atlas-detail");
      if (!detail) {
        return;
      }
      tip.replaceChildren(...detail.cloneNode(true).childNodes);
      tip.hidden = false;
      const box = cell.getBoundingClientRect();
      const frame = grid.getBoundingClientRect();
      const width = tip.offsetWidth;
      const left = Math.min(
        Math.max(box.left + box.width / 2 - width / 2, 8),
        window.innerWidth - width - 8,
      );
      tip.style.left = `${left - frame.left}px`;
      tip.style.top = `${box.bottom - frame.top + 6}px`;
    };
    const hide = () => {
      tip.hidden = true;
    };
    cells.addEventListener("pointerover", (event) => {
      const cell =
        event.target instanceof Element ? event.target.closest(".site-atlas-cell") : null;
      if (cell) {
        show(cell);
      }
    });
    cells.addEventListener("pointerleave", hide);
    cells.addEventListener("focusin", (event) => {
      if (event.target instanceof Element) {
        show(event.target);
      }
    });
    cells.addEventListener("focusout", hide);

    const place = () => {
      cells.append(template.content.cloneNode(true));
      grid.prepend(cells);
    };
    if (!("IntersectionObserver" in window)) {
      place();
      continue;
    }
    const watch = new IntersectionObserver(
      (entries) => {
        if (entries.some((entry) => entry.isIntersecting)) {
          watch.disconnect();
          place();
        }
      },
      { rootMargin: "800px 0px" },
    );
    watch.observe(grid);
  }
})();
