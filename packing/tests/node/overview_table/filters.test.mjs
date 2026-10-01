// The table script wired to a stand-in results table and its tools bar: two groups of
// rows carrying the facets `overview_sections.result_facets` writes, under the controls
// `overview_sections.result_filters` writes, Significance starting at S4 and up. The
// stand-ins are only what the script reads; the test reads what it then shows.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/table.js", import.meta.url),
  "utf8",
);

/** A control of the tools bar: what `data-filter` names, its `data-bound`, its value. */
class Control {
  /** @param {string} key @param {string | null} bound @param {string} value */
  constructor(key, bound, value) {
    this.key = key;
    this.bound = bound;
    this.value = value;
    this.type = "number";
  }

  /** @param {string} name */
  getAttribute(name) {
    return name === "data-filter" ? this.key : name === "data-bound" ? this.bound : null;
  }
}
class Select extends Control {}
class Input extends Control {}
class Table {}

/**
 * A stand-in row: a result's, with its facets, or a group heading's.
 * @param {string} id
 * @param {Record<string, string> | null} facets null for a group heading
 * @param {boolean} [hidden] as the page writes it
 */
function row(id, facets, hidden = false) {
  return {
    id,
    hidden,
    dataset: facets ?? {},
    classList: {
      /** @param {string} name */
      contains: (name) => name === "site-group-row" && facets === null,
    },
    cells: [{ getAttribute: () => id }],
  };
}

/**
 * A page with the results table, as the HTML has it: Significance at S4 and up, the
 * rows below it and the heading of the group they leave empty already hidden.
 * @param {{ search?: string, hash?: string }} [address]
 */
function page({ search = "", hash = "" } = {}) {
  const ours = { source: "ours", standing: "current-best" };
  const others = { source: "others", standing: "superseded" };
  const rows = [
    row("", null),
    row("t-001", { ...ours, v: "4", c: "5", s: "5", n: "11", date: "2026-09-04" }),
    row("t-002", { ...ours, v: "3", c: "2", s: "3", n: "17 18", date: "2026-08-31" }, true),
    row("", null, true),
    row("t-003", { ...others, v: "0", c: "0", s: "2", n: "18-21 26", date: "1979-01-01" }, true),
    row("t-004", { ...others, v: "4", c: "3", s: "3", n: "1-100", date: "2026-09-27" }, true),
    row("", null),
    row("t-005", { ...others, v: "4", c: "4", s: "4", n: "45", date: "2026-09-27" }),
  ];
  const controls = {
    s: new Select("s", "min", "4"),
    v: new Select("v", "min", ""),
    c: new Select("c", "min", ""),
    standing: new Select("standing", null, ""),
    source: new Select("source", null, ""),
    n: new Input("n", "covers", ""),
    from: new Input("date", "from", ""),
    to: new Input("date", "to", ""),
  };
  const count = { textContent: "2 of 5 results", getAttribute: () => "results" };
  /** @type {Record<string, (() => void)[]>} */
  const listeners = { change: [], hashchange: [], click: [] };
  const tools = {
    classList: {
      /** @param {string} name */
      contains: (name) => name === "site-table-tools",
    },
    querySelectorAll: () => Object.values(controls),
    querySelector: () => count,
    removeAttribute: () => undefined,
    /** @param {string} type @param {() => void} listener */
    addEventListener: (type, listener) => listeners[type]?.push(listener),
  };
  /** @type {Record<string, string>} */
  const sortable = { "data-sort": "text" };
  const heading = {
    tabIndex: -1,
    /** @param {string} name */
    getAttribute: (name) => sortable[name] ?? null,
    /** @param {string} name @param {string} value */
    setAttribute: (name, value) => {
      sortable[name] = value;
    },
    /** @param {string} name */
    hasAttribute: (name) => name in sortable,
    /** @param {string} type @param {() => void} listener */
    addEventListener: (type, listener) => listeners[type]?.push(listener),
  };
  const body = {
    rows,
    /** @param {ReturnType<typeof row>[]} sorted */
    append(...sorted) {
      this.rows = sorted;
    },
  };
  const table = Object.assign(new Table(), {
    tBodies: [body],
    tHead: { rows: [{ cells: [heading] }] },
    hasAttribute: () => false,
    setAttribute: () => undefined,
    closest: () => ({ previousElementSibling: tools }),
  });
  const location = { search, hash };
  vm.runInContext(
    SOURCE,
    vm.createContext({
      URLSearchParams,
      decodeURIComponent,
      location,
      document: { readyState: "complete", querySelectorAll: () => [table] },
      window: {
        /** @param {string} type @param {() => void} listener */
        addEventListener: (type, listener) => listeners[type]?.push(listener),
      },
      HTMLSelectElement: Select,
      HTMLInputElement: Input,
      HTMLTableElement: Table,
    }),
  );
  /** @param {keyof typeof listeners} type */
  const fire = (type) => {
    for (const listener of listeners[type] ?? []) {
      listener();
    }
  };
  return {
    controls,
    count,
    location,
    /** The ids of the result rows showing, and how many group headings show. */
    shown: () => ({
      rows: body.rows.filter((entry) => entry.id !== "" && !entry.hidden).map((entry) => entry.id),
      headings: body.rows.filter((entry) => entry.id === "" && !entry.hidden).length,
    }),
    /**
     * Change the controls, then tell the bar, as a reader's choice does.
     * @param {Partial<Record<keyof typeof controls, string>>} values
     */
    choose(values) {
      for (const [name, value] of Object.entries(values)) {
        controls[/** @type {keyof typeof controls} */ (name)].value = value;
      }
      fire("change");
    },
    fire,
  };
}

void test("the bar's state in the HTML is the default: S4 and up, already filtered", () => {
  const results = page();
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-005"], headings: 2 });
  assert.equal(results.count.textContent, "2 of 5 results");
});

void test("All shows every row and every group heading", () => {
  const results = page();
  results.choose({ s: "" });
  assert.deepEqual(results.shown(), {
    rows: ["t-001", "t-002", "t-003", "t-004", "t-005"],
    headings: 3,
  });
  assert.equal(results.count.textContent, "5 results");
});

void test("each facet filters, and the filters compose", () => {
  const results = page();
  /** @param {Parameters<typeof results.choose>[0]} values */
  const rows = (values) => {
    results.choose({
      ...{ s: "", v: "", c: "", standing: "", source: "", n: "", from: "", to: "" },
      ...values,
    });
    return results.shown().rows;
  };
  assert.deepEqual(rows({ s: "3" }), ["t-001", "t-002", "t-004", "t-005"]);
  assert.deepEqual(rows({ v: "4" }), ["t-001", "t-004", "t-005"]);
  assert.deepEqual(rows({ c: "4" }), ["t-001", "t-005"]);
  assert.deepEqual(rows({ standing: "superseded" }), ["t-003", "t-004", "t-005"]);
  assert.deepEqual(rows({ source: "ours" }), ["t-001", "t-002"]);
  assert.deepEqual(rows({ n: "18" }), ["t-002", "t-003", "t-004"]);
  assert.deepEqual(rows({ from: "2026-09-01" }), ["t-001", "t-004", "t-005"]);
  assert.deepEqual(rows({ to: "2026-08-31" }), ["t-002", "t-003"]);
  assert.deepEqual(rows({ from: "2026-08-01", to: "2026-09-10" }), ["t-001", "t-002"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4" }), ["t-004", "t-005"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4", n: "45" }), ["t-004", "t-005"]);
  assert.deepEqual(rows({ s: "3", source: "others", v: "4", n: "45", c: "4" }), ["t-005"]);
  assert.equal(results.count.textContent, "1 of 5 results");
  assert.deepEqual(rows({ s: "5", source: "others" }), []);
  assert.equal(results.shown().headings, 0);
  assert.equal(results.count.textContent, "0 of 5 results");
});

void test("the row the address names shows whatever the filters hide", () => {
  const results = page({ hash: "#t-003" });
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-003", "t-005"], headings: 3 });
  assert.equal(results.count.textContent, "3 of 5 results");
  results.location.hash = "#t-002";
  results.fire("hashchange");
  assert.deepEqual(results.shown().rows, ["t-001", "t-002", "t-005"]);
  results.location.hash = "#%E0%A4%A";
  results.fire("hashchange");
  assert.deepEqual(results.shown().rows, ["t-001", "t-005"]);
});

void test("a link can open the table filtered, by each control's parameter", () => {
  const results = page({ search: "?s-min=3&n=17&date-from=2026-08-01" });
  assert.equal(results.controls.s.value, "3");
  assert.equal(results.controls.n.value, "17");
  assert.equal(results.controls.from.value, "2026-08-01");
  assert.deepEqual(results.shown().rows, ["t-002", "t-004"]);
  assert.deepEqual(page({ search: "?s-min=" }).shown().rows.length, 5);
});

void test("a sort keeps the filters and hides the group headings", () => {
  const results = page();
  results.fire("click");
  assert.deepEqual(results.shown(), { rows: ["t-001", "t-005"], headings: 0 });
  results.fire("click");
  assert.deepEqual(results.shown(), { rows: ["t-005", "t-001"], headings: 0 });
  results.choose({ s: "" });
  assert.deepEqual(results.shown(), {
    rows: ["t-005", "t-004", "t-003", "t-002", "t-001"],
    headings: 0,
  });
});
