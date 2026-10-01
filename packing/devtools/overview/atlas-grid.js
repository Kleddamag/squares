// The homepage's grid of every known-best packing. Its cells arrive in a <template>,
// which the browser parses but does not lay out, and are placed only when the grid
// comes near the viewport, so they cost the page's first paint nothing.
//
// Pressing a cell opens the page's one atlas popover on that case: what the ascent
// film's panel says about it (the gap bar, the bound as one statement, the badges, the
// citation and what is open), read from the grid's JSON facts, beside the drawing shown
// large, ending in the button to the case record. The arrows, and the arrow keys, step
// to the next or previous case. Without this script a cell is a link to the record.
//
// The grid shows the first hundred cases. The button under it places the rest, from a
// second template, the first time it is pressed, and after that shows or hides them;
// stepping the popover past the hundredth case expands the grid the same way.
//
// The tabs over the tiles choose between two views of the one set, the grid and the
// triangle, which `atlas-view.js` lays out and moves between (`SiteAtlasView.mount`).
// They ship `hidden` and show once the tiles are placed.
(() => {
  const grid = document.querySelector("[data-atlas-grid]");
  const template = grid?.querySelector("template[data-atlas-first]");
  const restTemplate = grid?.querySelector("template[data-atlas-rest]");
  const toggle = grid?.querySelector("[data-atlas-toggle]");
  const tabs = grid?.querySelector("[data-atlas-views]");
  if (
    !(grid instanceof HTMLElement) ||
    !(template instanceof HTMLTemplateElement) ||
    !(restTemplate instanceof HTMLTemplateElement) ||
    !(toggle instanceof HTMLButtonElement) ||
    !(tabs instanceof HTMLElement)
  ) {
    return;
  }
  const cells = document.createElement("div");
  cells.className = "site-atlas-cells";
  // The rest of the cases, in a box of their own that the grid lays out as if its
  // cells were the grid's own (`display: contents`), so hiding them is one attribute.
  const rest = document.createElement("div");
  rest.className = "site-atlas-rest";
  rest.hidden = true;

  // The view the address names is set here, before any tile is placed, so the page
  // never shows one view and then the other.
  const views = SiteAtlasView.mount({ block: grid, cells, tabs });

  const place = () => {
    cells.append(template.content.cloneNode(true), rest);
    tabs.after(cells);
    tabs.hidden = false;
    if (toggle.parentElement) {
      toggle.parentElement.hidden = false;
    }
    views.arrange();
  };

  // The button reads Show More with the double chevron down, and once the rest show,
  // Show Less with the chevron up; its name for assistive technology says what each
  // does and how many cases that is, from the names the page ships.
  const toggleLabel = toggle.querySelector("[data-atlas-label]");
  const toggleChevron = toggle.querySelector(".site-icon-arrow");
  /** @param {boolean} open */
  const relabel = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute(
      "aria-label",
      (open ? toggle.dataset.nameLess : toggle.dataset.nameMore) ?? "",
    );
    if (toggleLabel !== null) {
      toggleLabel.textContent = (open ? toggle.dataset.labelLess : toggle.dataset.labelMore) ?? "";
    }
    if (toggleChevron instanceof HTMLElement) {
      toggleChevron.dataset.arrow = open ? "double-up" : "double-down";
    }
  };

  // Showing or hiding the rest changes where the triangle's tiles stand, since its
  // longest row sets how many a line holds, so it is a change of layout like a change
  // of view: the tiles that stay move, and the ones that arrive fade in. Collapsing
  // takes away everything above the button but the first hundred, so the page would
  // land far below it: `settle` brings the button back to where the reader is, as part
  // of the same change.
  /**
   * @param {boolean} open
   * @param {() => void} [settle]
   */
  const expandGrid = (open, settle) => {
    if (open && rest.childElementCount === 0) {
      rest.append(restTemplate.content.cloneNode(true));
    }
    views.change(() => {
      rest.hidden = !open;
      relabel(open);
      settle?.();
    });
  };
  toggle.addEventListener("click", () => {
    const open = rest.hidden !== false;
    expandGrid(open, open ? undefined : () => toggle.scrollIntoView({ block: "nearest" }));
  });
  if ("IntersectionObserver" in window) {
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
  } else {
    place();
  }

  const popover = document.querySelector("[data-atlas-popover]");
  const source = grid.querySelector("script[data-atlas-facts]");
  const mathTemplate = popover?.querySelector("template[data-atlas-math]");
  if (
    !(popover instanceof HTMLElement) ||
    !(source instanceof HTMLScriptElement) ||
    !(mathTemplate instanceof HTMLTemplateElement) ||
    typeof popover.showPopover !== "function"
  ) {
    return;
  }

  /** @param {string} selector */
  const slot = (selector) => {
    const found = popover.querySelector(selector);
    if (!(found instanceof HTMLElement)) {
      throw new Error(`the atlas popover has no ${selector}`);
    }
    return found;
  };
  const title = slot("[data-atlas-title]");
  const figure = slot("[data-atlas-figure]");
  const bound = slot("[data-atlas-bound]");
  const badges = slot("[data-atlas-badges]");
  const citation = slot("[data-atlas-citation]");
  const record = slot("[data-atlas-record]");
  const openSection = slot("[data-atlas-open]");
  const openItems = slot("[data-atlas-open-items]");
  const expand = slot("[data-atlas-expand]");
  const gapValues = slot("[data-atlas-gap-values]");
  const gapRail = slot("[data-atlas-gap-rail]");
  const gapIntegers = slot("[data-atlas-gap-integers]");
  const gapRoots = slot("[data-atlas-gap-roots]");
  const areaFormula = slot('[data-atlas-formula="area"]');
  const gridFormula = slot('[data-atlas-formula="grid"]');
  const close = slot(".site-popover-close");
  /** @type {Record<"lower" | "upper", HTMLElement>} */
  const cites = {
    lower: slot('[data-atlas-cite="lower"]'),
    upper: slot('[data-atlas-cite="upper"]'),
  };

  /** @type {Map<number, AtlasFact> | null} */
  let facts = null;
  const factsFor = () => {
    if (facts === null) {
      /** @type {AtlasFact[]} */
      const list = JSON.parse(source.textContent ?? "[]");
      facts = new Map(list.map((fact) => [fact.n, fact]));
    }
    return facts;
  };

  /**
   * @param {string} tag
   * @param {string} [className]
   * @param {string} [text]
   */
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (text !== undefined) {
      node.textContent = text;
    }
    return node;
  };

  // A formula typeset as every other on the page: kpress's own math node, cloned from
  // the template the popover carries, with the TeX set as text and the words a screen
  // reader hears in place of its MathML.
  /**
   * @param {string} tex
   * @param {string} spoken
   */
  const math = (tex, spoken) => {
    const node = mathTemplate.content.firstElementChild?.cloneNode(true);
    if (!(node instanceof HTMLElement)) {
      return element("span", undefined, spoken);
    }
    const render = node.querySelector(".kpress-math-render");
    const semantic = node.querySelector(".kpress-math-semantic");
    if (render) {
      render.textContent = `\\(${tex}\\)`;
    }
    if (semantic) {
      semantic.textContent = spoken;
    }
    return node;
  };

  // ---- The gap bar, as the film draws it: a scale from one below the grid bound
  // `ceil(sqrt(n))` to two above that, so it changes only at a perfect square; the
  // integers and the two formulas `sqrt(n)` and `sqrt(n) + 1` marked on it; the proved
  // lower bound and the best known side as bold rules, their values above, and the
  // span between them shaded, the territory nobody has closed.
  const INSET = 5;
  /**
   * @param {number} value
   * @param {number} lo
   */
  const at = (value, lo) => INSET + Math.min(1, Math.max(0, (value - lo) / 2)) * (100 - 2 * INSET);
  /** @param {number} value */
  const barNumber = (value) => (Number.isInteger(value) ? String(value) : value.toFixed(3));
  /**
   * @param {HTMLElement} row
   * @param {string} className
   * @param {string} text
   * @param {number} percent
   */
  const label = (row, className, text, percent) => {
    const node = element("span", className, text);
    node.dataset.at = String(percent);
    node.style.left = `${percent}%`;
    row.append(node);
    return node;
  };
  /**
   * @param {string} className
   * @param {number} percent
   */
  const mark = (className, percent) => {
    const node = element("span", className);
    node.style.left = `${percent}%`;
    gapRail.append(node);
  };

  /** @param {AtlasFact} fact */
  const drawGap = (fact) => {
    const upper = Number(fact.upper);
    const lower = fact.lower === null ? upper : Number(fact.lower);
    const root = Math.sqrt(fact.n);
    const lo = Math.ceil(root) - 1;
    gapRail.replaceChildren(element("span", "site-atlas-gap-track"));
    gapValues.replaceChildren();
    gapIntegers.replaceChildren();
    gapRoots.replaceChildren();
    const open = element("span", "site-atlas-gap-open");
    open.style.left = `${at(lower, lo)}%`;
    open.style.width = `${Math.max(0, at(upper, lo) - at(lower, lo))}%`;
    gapRail.append(open);
    /** @type {number[]} */
    const marks = [];
    for (const value of [lo, lo + 1, lo + 2, root, root + 1]) {
      if (!marks.includes(value)) {
        marks.push(value);
      }
    }
    for (const value of marks) {
      const integer = Number.isInteger(value);
      mark(integer ? "site-atlas-gap-tick" : "site-atlas-gap-tick is-root", at(value, lo));
      label(integer ? gapIntegers : gapRoots, "", barNumber(value), at(value, lo));
    }
    if (fact.lower !== null) {
      mark("site-atlas-gap-rule", at(lower, lo));
      label(gapValues, "is-lower", barNumber(lower), at(lower, lo));
    }
    mark("site-atlas-gap-rule", at(upper, lo));
    label(gapValues, "is-upper", barNumber(upper), at(upper, lo));
    areaFormula.dataset.at = String(at(root, lo));
    gridFormula.dataset.at = String(at(root + 1, lo));
  };

  // Each label is centred on its mark, then kept inside the bar; the two values share
  // one line, so the lower, always the smaller, gives way to the left when they crowd.
  const fitGap = () => {
    for (const row of [gapValues, gapIntegers, gapRoots, areaFormula.parentElement]) {
      if (!(row instanceof HTMLElement)) {
        continue;
      }
      const width = row.clientWidth;
      /** @type {{node: HTMLElement, left: number, width: number}[]} */
      const placed = [];
      for (const node of row.children) {
        if (!(node instanceof HTMLElement) || node.dataset.at === undefined) {
          continue;
        }
        const own = node.offsetWidth;
        const centre = (Number(node.dataset.at) / 100) * width;
        placed.push({ node, left: centre - own / 2, width: own });
      }
      if (row === gapValues && placed.length === 2) {
        const [low, high] = placed;
        const overlap = low && high ? low.left + low.width + 10 - high.left : 0;
        if (low && high && overlap > 0) {
          low.left -= overlap / 2;
          high.left += overlap / 2;
        }
      }
      for (const item of placed) {
        const left = Math.max(0, Math.min(width - item.width, item.left));
        item.node.style.left = `${left}px`;
      }
    }
  };

  /** @param {AtlasFact} fact */
  const drawBound = (fact) => {
    const star = element("span", "site-atlas-pop-star", fact.star ? "★" : "");
    star.setAttribute("aria-hidden", "true");
    const n = fact.n;
    const parts = [star];
    if (fact.exact) {
      parts.push(math(`s(${n}) = ${fact.upper}`, `s(${n}) = ${fact.upper}`));
    } else {
      if (fact.lower !== null) {
        const lower = element("span", "is-lower");
        lower.append(math(fact.lower, fact.lower));
        parts.push(lower);
      }
      const middle = fact.lower === null ? `s(${n}) \\le{}` : `{}\\le s(${n}) \\le{}`;
      const spoken = fact.lower === null ? `s(${n}) ≤ ` : ` ≤ s(${n}) ≤ `;
      parts.push(math(middle, spoken));
      const upper = element("span", "is-upper");
      upper.append(math(fact.upper, fact.upper));
      parts.push(upper);
    }
    bound.replaceChildren(...parts);
  };

  /**
   * @param {string} glyph
   * @param {string} style
   * @param {string} text
   * @param {string} [className]
   */
  const badge = (glyph, style, text, className) => {
    const item = element(
      "li",
      className ? `site-atlas-pop-item ${className}` : "site-atlas-pop-item",
    );
    const box = element("span", "site-atlas-badge", glyph);
    box.dataset.style = style;
    box.setAttribute("aria-hidden", "true");
    item.append(box, text);
    return item;
  };

  /** @param {AtlasFact} fact */
  const drawFacts = (fact) => {
    const items = fact.star ? [badge("★", "star", "new result", "is-new-result")] : [];
    for (const [glyph, style, text] of fact.badges) {
      items.push(badge(glyph, style, text));
    }
    badges.replaceChildren(...items);
    const cited = fact.cite.lower !== null || fact.cite.upper !== null;
    citation.hidden = !cited;
    record.textContent = fact.record;
    for (const which of /** @type {const} */ (["lower", "upper"])) {
      const line = fact.cite[which];
      const node = cites[which];
      node.hidden = line === null;
      node.replaceChildren();
      if (line !== null) {
        node.append(element("span", `site-atlas-pop-which is-${which}`, which), line.text);
        if (line.note !== null) {
          node.append(" ", element("span", "site-atlas-pop-note", line.note));
        }
      }
    }
    openSection.hidden = fact.open.length === 0;
    openItems.replaceChildren(...fact.open.map((text) => badge("?", "query", text)));
  };

  /** @type {HTMLAnchorElement | null} */
  let current = null;

  // The site's math driver (overview/math.js) typesets the panel's fresh formulas.
  const typeset = () => {
    fitGap();
    const site = globalThis.siteMath;
    if (site !== undefined) {
      site.typeset(popover, true).then(fitGap, fitGap);
    }
  };

  /** @param {HTMLAnchorElement} cell */
  const show = (cell) => {
    const n = Number(cell.dataset.atlasN);
    const fact = factsFor().get(n);
    if (fact === undefined) {
      return false;
    }
    current = cell;
    title.replaceChildren(math(`n = ${n}`, `n = ${n}`));
    const drawing = cell.querySelector("svg")?.cloneNode(true);
    figure.replaceChildren(...(drawing ? [drawing] : []));
    drawGap(fact);
    drawBound(fact);
    drawFacts(fact);
    expand.setAttribute("href", cell.getAttribute("href") ?? "cases.html");
    expand.setAttribute("aria-label", `See all cases, opened at n = ${n}`);
    for (const step of popover.querySelectorAll("[data-atlas-step]")) {
      if (step instanceof HTMLButtonElement) {
        step.disabled = !factsFor().has(n + Number(step.dataset.atlasStep));
      }
    }
    if (!popover.matches(":popover-open")) {
      popover.showPopover();
      close.focus();
    }
    typeset();
    return true;
  };

  /** @param {number} offset */
  const step = (offset) => {
    if (current === null) {
      return;
    }
    const selector = `[data-atlas-n="${Number(current.dataset.atlasN) + offset}"]`;
    let next = cells.querySelector(selector);
    // A case the grid does not show yet: expand it, so the cell the popover now stands
    // for is there when it closes and focus returns to it.
    if (!(next instanceof HTMLAnchorElement) || next.closest("[hidden]")) {
      expandGrid(true);
      next = cells.querySelector(selector);
    }
    if (next instanceof HTMLAnchorElement) {
      show(next);
    }
  };

  cells.addEventListener("click", (event) => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    const cell = event.target instanceof Element ? event.target.closest(".site-atlas-cell") : null;
    if (cell instanceof HTMLAnchorElement && show(cell)) {
      event.preventDefault();
    }
  });
  for (const button of popover.querySelectorAll("[data-atlas-step]")) {
    if (button instanceof HTMLButtonElement) {
      button.addEventListener("click", () => step(Number(button.dataset.atlasStep)));
    }
  }
  popover.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      step(event.key === "ArrowLeft" ? -1 : 1);
    }
  });
  // Closing returns focus to the case's cell, which the arrows may have moved, so a
  // keyboard reader carries on in the grid from where the popover left them.
  popover.addEventListener("toggle", (event) => {
    if (!(event instanceof ToggleEvent) || event.newState !== "closed" || current === null) {
      return;
    }
    // The browser has already put focus back on the cell that opened the popover, which
    // is not the case shown once the arrows have moved.
    const focus = document.activeElement;
    if (
      focus === null ||
      focus === document.body ||
      popover.contains(focus) ||
      (cells.contains(focus) && focus !== current)
    ) {
      current.focus();
    }
  });
  window.addEventListener("resize", () => {
    if (popover.matches(":popover-open")) {
      fitGap();
    }
  });
})();
