// Sorting and filtering for the site's tables: the frontier atlas and the results table.
//
// A classic script, inlined into each page by `devtools.render_overview`. It enhances
// every `table.site-table` whose wrapper follows a `.site-table-tools` bar; the table is
// complete in the HTML, so with scripting off every row is present and nothing is lost.
//
// Headings with `data-sort="num"` or `data-sort="text"` sort on click (a numeric sort
// reads each cell's `data-value`, else its text). Filters are the bar's controls, each
// naming a row attribute with `data-filter`:
//   <select data-filter="status">                 row's data-status equals the value
//   <input type="checkbox" data-filter="open">     row's data-open is "true"
//   <input type="number" data-filter="n" data-bound="min|max">  row's data-n in range
// The bar's `.site-count` shows how many rows remain. The pure functions are published
// on `globalThis.SiteTable` for the Node tests; nothing else leaves this file.

(() => {
  /**
   * The sort key of a cell: its `data-value`, else its visible text.
   * @param {Element | undefined} cell
   * @returns {string}
   */
  function cellKey(cell) {
    if (!cell) {
      return "";
    }
    const value = cell.getAttribute("data-value");
    return value ?? (cell.textContent ?? "").trim();
  }

  /**
   * Compare two sort keys; a key that is not a number sorts after every number.
   * @param {string} left
   * @param {string} right
   * @param {SiteTableSortType} type
   * @returns {number}
   */
  function compareKeys(left, right, type) {
    if (type === "num") {
      const a = Number.parseFloat(left);
      const b = Number.parseFloat(right);
      const aMissing = Number.isNaN(a);
      const bMissing = Number.isNaN(b);
      if (aMissing || bMissing) {
        return Number(aMissing) - Number(bMissing);
      }
      return a - b;
    }
    return left.localeCompare(right, undefined, { numeric: true, sensitivity: "base" });
  }

  /**
   * The order that sorts `keys`, stable, as indices into `keys`.
   * @param {readonly string[]} keys
   * @param {SiteTableSortType} type
   * @param {"ascending" | "descending"} direction
   * @returns {number[]}
   */
  function sortOrder(keys, type, direction) {
    const sign = direction === "ascending" ? 1 : -1;
    return keys
      .map((key, index) => ({ key, index }))
      .sort((a, b) => sign * compareKeys(a.key, b.key, type) || a.index - b.index)
      .map((entry) => entry.index);
  }

  /**
   * Whether a row with these attributes passes every active filter.
   * @param {Readonly<Record<string, string | undefined>>} row
   * @param {readonly SiteTableFilter[]} filters
   * @returns {boolean}
   */
  function rowMatches(row, filters) {
    return filters.every((filter) => {
      const actual = row[filter.key];
      switch (filter.kind) {
        case "equals":
          return filter.value === "" || actual === filter.value;
        case "flag":
          return filter.value !== "true" || actual === "true";
        case "min":
        case "max": {
          const bound = Number.parseFloat(filter.value);
          if (Number.isNaN(bound)) {
            return true;
          }
          const value = Number.parseFloat(actual ?? "");
          return filter.kind === "min" ? value >= bound : value <= bound;
        }
        default:
          return true;
      }
    });
  }

  /**
   * The live count's words.
   * @param {number} shown
   * @param {number} total
   * @param {string} noun
   * @returns {string}
   */
  function countText(shown, total, noun) {
    return shown === total ? `${total} ${noun}` : `${shown} of ${total} ${noun}`;
  }

  /**
   * The filters a tools bar's controls currently express.
   * @param {Element} tools
   * @returns {SiteTableFilter[]}
   */
  function readFilters(tools) {
    /** @type {SiteTableFilter[]} */
    const filters = [];
    for (const control of tools.querySelectorAll("[data-filter]")) {
      const key = control.getAttribute("data-filter") ?? "";
      if (control instanceof HTMLSelectElement) {
        filters.push({ key, kind: "equals", value: control.value });
      } else if (control instanceof HTMLInputElement && control.type === "checkbox") {
        filters.push({ key, kind: "flag", value: control.checked ? "true" : "false" });
      } else if (control instanceof HTMLInputElement) {
        const kind = control.getAttribute("data-bound") === "max" ? "max" : "min";
        filters.push({ key, kind, value: control.value });
      }
    }
    return filters;
  }

  /**
   * A row's `data-*` attributes, by name without the prefix.
   * @param {HTMLTableRowElement} row
   * @returns {Record<string, string | undefined>}
   */
  function rowData(row) {
    return { ...row.dataset };
  }

  /**
   * Wire one table to its tools bar. Safe to call twice: a wired table is skipped.
   * @param {HTMLTableElement} table
   * @param {Element | null} tools
   */
  function enhance(table, tools) {
    if (table.hasAttribute("data-site-table-ready")) {
      return;
    }
    table.setAttribute("data-site-table-ready", "");
    const body = table.tBodies[0];
    if (!body) {
      return;
    }
    const rows = Array.from(body.rows);
    const count = tools?.querySelector(".site-count") ?? null;
    const noun = count?.getAttribute("data-noun") ?? "rows";

    const applyFilters = () => {
      if (!tools) {
        return;
      }
      const filters = readFilters(tools);
      let shown = 0;
      for (const row of rows) {
        const visible = rowMatches(rowData(row), filters);
        row.hidden = !visible;
        shown += Number(visible);
      }
      if (count) {
        count.textContent = countText(shown, rows.length, noun);
      }
    };

    const headings = Array.from(table.tHead?.rows[0]?.cells ?? []);
    headings.forEach((heading, column) => {
      const type = heading.getAttribute("data-sort");
      if (type !== "num" && type !== "text") {
        return;
      }
      heading.tabIndex = 0;
      heading.setAttribute("aria-sort", "none");
      const sort = () => {
        const direction =
          heading.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        for (const other of headings) {
          if (other.hasAttribute("aria-sort")) {
            other.setAttribute("aria-sort", "none");
          }
        }
        heading.setAttribute("aria-sort", direction);
        const current = Array.from(body.rows);
        const keys = current.map((row) => cellKey(row.cells[column]));
        const order = sortOrder(keys, type, direction);
        body.append(...order.flatMap((index) => current[index] ?? []));
      };
      heading.addEventListener("click", sort);
      heading.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          sort();
        }
      });
    });

    if (tools) {
      tools.removeAttribute("hidden");
      tools.addEventListener("input", applyFilters);
      tools.addEventListener("change", applyFilters);
      applyFilters();
    }
  }

  /** Enhance every site table on the page. */
  function init() {
    for (const table of document.querySelectorAll("table.site-table")) {
      if (!(table instanceof HTMLTableElement)) {
        continue;
      }
      const wrap = table.closest(".site-table-wrap");
      const before = wrap?.previousElementSibling;
      const tools = before?.classList.contains("site-table-tools") ? before : null;
      enhance(table, tools);
    }
  }

  globalThis.SiteTable = { compareKeys, sortOrder, rowMatches, countText, init };

  if (typeof document === "undefined") {
    return;
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
