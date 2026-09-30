/* Sorting and filtering for the site's tables: the overview's results table and the
   frontier atlas. Generic: it knows nothing about results or cases, only this contract,
   which `templates/site-design.md` documents ("Tables and table.js").

   - `<table class="kpress-table site-table" data-site-table id="…">`; every such table on
     the page is set up when this script runs.
   - A header `<th data-sort="number">` or `<th data-sort="text">` sorts by its column.
     Each click steps ascending, descending, then back to the page's own order; the
     header's `aria-sort` says which. A cell's sort value is its `data-value`, else its
     text. An empty value, or a non-number in a number column, sorts last either way.
   - Rows are the `tr` of every `tbody`. A row marked `data-site-table-group` heads the
     rows after it (until the next such row); it is hidden when all of them are, and
     while the table is sorted, when the rows are listed as one.
   - Filters live in `<div class="site-table-filters" data-filters-for="<table id>"
     hidden>`, shown by this script:
     `<select data-filter="attr">` keeps rows whose `data-attr` equals its value (the
     first option, value "", keeps all); `<input type="checkbox" data-filter-flag="f">`,
     when checked, keeps rows whose space-separated `data-flags` include `f`;
     `<input type="number" data-filter-min="attr">` and `data-filter-max="attr"` keep
     rows whose numeric `data-attr` is at least or at most the value, and drop a row
     without one. An `<output data-filter-count>` in the panel says how many rows show.
   - Expandable rows are `<details>` in a cell. A row the fragment targets has its
     details opened.

   With JavaScript off none of this runs: every row is in the page, in its order, and
   the filter panel stays hidden. */
(() => {
  /** @typedef {"ascending" | "descending"} Direction */
  /** @typedef {{ row: HTMLElement, body: HTMLElement }} Entry */

  const GROUP = "data-site-table-group";

  /** @param {Element | undefined} cell */
  const cellValue = (cell) => {
    if (!cell) {
      return "";
    }
    return cell.getAttribute("data-value") ?? (cell.textContent ?? "").trim();
  };

  /**
   * @param {string} value
   * @param {string} kind
   */
  const missing = (value, kind) =>
    value === "" || (kind === "number" && Number.isNaN(Number.parseFloat(value)));

  /**
   * The order of two sort values: missing values last in both directions.
   * @param {string} a
   * @param {string} b
   * @param {string} kind
   * @param {Direction} direction
   */
  const compare = (a, b, kind, direction) => {
    const aMissing = missing(a, kind);
    const bMissing = missing(b, kind);
    if (aMissing || bMissing) {
      return Number(aMissing) - Number(bMissing);
    }
    const order =
      kind === "number"
        ? Number.parseFloat(a) - Number.parseFloat(b)
        : a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
    return direction === "descending" ? -order : order;
  };

  /**
   * @param {HTMLElement} row
   * @param {string} attribute
   */
  const numberOf = (row, attribute) => {
    const text = row.getAttribute(`data-${attribute}`);
    return text === null || text === "" ? Number.NaN : Number(text);
  };

  /**
   * Whether a row passes every filter in the given panels.
   * @param {HTMLElement} row
   * @param {HTMLElement[]} panels
   */
  const passes = (row, panels) => {
    for (const panel of panels) {
      for (const select of panel.querySelectorAll("select[data-filter]")) {
        const want = /** @type {HTMLSelectElement} */ (select).value;
        const attribute = select.getAttribute("data-filter");
        if (want !== "" && row.getAttribute(`data-${attribute}`) !== want) {
          return false;
        }
      }
      for (const box of panel.querySelectorAll("input[data-filter-flag]")) {
        const flag = box.getAttribute("data-filter-flag") ?? "";
        const flags = (row.getAttribute("data-flags") ?? "").split(/\s+/);
        if (/** @type {HTMLInputElement} */ (box).checked && !flags.includes(flag)) {
          return false;
        }
      }
      for (const [selector, atLeast] of /** @type {const} */ ([
        ["data-filter-min", true],
        ["data-filter-max", false],
      ])) {
        for (const input of panel.querySelectorAll(`input[${selector}]`)) {
          const limit = /** @type {HTMLInputElement} */ (input).value;
          if (limit === "" || Number.isNaN(Number(limit))) {
            continue;
          }
          const value = numberOf(row, input.getAttribute(selector) ?? "");
          if (Number.isNaN(value) || (atLeast ? value < Number(limit) : value > Number(limit))) {
            return false;
          }
        }
      }
    }
    return true;
  };

  /** @param {HTMLElement} table */
  const setUp = (table) => {
    const bodies = /** @type {HTMLElement[]} */ ([...table.querySelectorAll("tbody")]);
    /** The page's own order, group rows included, which a third click restores. */
    /** @type {Entry[]} */
    const original = [];
    for (const body of bodies) {
      for (const child of body.children) {
        original.push({ row: /** @type {HTMLElement} */ (child), body });
      }
    }
    const entries = original.filter(({ row }) => !row.hasAttribute(GROUP));
    const groups = original.filter(({ row }) => row.hasAttribute(GROUP)).map(({ row }) => row);
    const panels = table.id
      ? /** @type {HTMLElement[]} */ ([
          ...document.querySelectorAll(`[data-filters-for="${table.id}"]`),
        ])
      : [];
    let sorted = false;

    const showGroups = () => {
      for (const group of groups) {
        let shown = false;
        for (
          let next = group.nextElementSibling;
          next && !next.hasAttribute(GROUP);
          next = next.nextElementSibling
        ) {
          if (!(/** @type {HTMLElement} */ (next).hidden)) {
            shown = true;
            break;
          }
        }
        group.hidden = sorted || !shown;
      }
    };

    const filter = () => {
      let shown = 0;
      for (const { row } of entries) {
        row.hidden = !passes(row, panels);
        shown += row.hidden ? 0 : 1;
      }
      showGroups();
      const total = entries.length;
      for (const panel of panels) {
        for (const output of panel.querySelectorAll("[data-filter-count]")) {
          output.textContent =
            shown === total ? `All ${total} shown` : `${shown} of ${total} shown`;
        }
      }
    };

    /** @param {number} column @param {string} kind @param {Direction | null} direction */
    const sort = (column, kind, direction) => {
      const first = bodies[0];
      if (!first) {
        return;
      }
      if (direction === null) {
        sorted = false;
        for (const { row, body } of original) {
          body.append(row);
        }
      } else {
        sorted = true;
        const keyed = entries.map(({ row }, index) => ({
          row,
          index,
          value: cellValue(row.children[column]),
        }));
        keyed.sort((a, b) => compare(a.value, b.value, kind, direction) || a.index - b.index);
        for (const { row } of keyed) {
          first.append(row);
        }
      }
      showGroups();
    };

    for (const head of table.querySelectorAll("thead th[data-sort]")) {
      const header = /** @type {HTMLElement} */ (head);
      const kind = header.getAttribute("data-sort") ?? "text";
      const column = header.parentElement ? [...header.parentElement.children].indexOf(header) : -1;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "site-sort";
      button.append(...header.childNodes);
      header.append(button);
      button.addEventListener("click", () => {
        const now = header.getAttribute("aria-sort");
        /** @type {Direction | null} */
        const next = now === "ascending" ? "descending" : now === "descending" ? null : "ascending";
        for (const other of table.querySelectorAll("thead th[aria-sort]")) {
          other.removeAttribute("aria-sort");
        }
        if (next) {
          header.setAttribute("aria-sort", next);
        }
        sort(column, kind, next);
      });
    }

    for (const panel of panels) {
      panel.hidden = false;
      panel.addEventListener("input", filter);
      panel.addEventListener("change", filter);
    }
    if (panels.length) {
      filter();
    }
  };

  /** Open the details of a table row the fragment names. */
  const openTarget = () => {
    let id = window.location.hash.slice(1);
    try {
      id = decodeURIComponent(id);
    } catch {
      return;
    }
    const row = id ? document.getElementById(id) : null;
    if (!row?.closest("table[data-site-table]")) {
      return;
    }
    const details = row.querySelector("details");
    if (details) {
      details.open = true;
    }
  };

  for (const table of document.querySelectorAll("table[data-site-table]")) {
    setUp(/** @type {HTMLElement} */ (table));
  }
  window.addEventListener("hashchange", openTarget);
  openTarget();
})();
