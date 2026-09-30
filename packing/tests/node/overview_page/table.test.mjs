// `overview/table.js`, against its contract in `templates/site-design.md`: headers with
// `data-sort` sort by their column (a cell's `data-value`, else its text; ascending,
// descending, then the page's own order; missing values last), group rows stand aside
// while sorted and hide when all their rows do, and the filter panel's selects, flags and
// numeric bounds keep only the rows that pass every one.
import assert from "node:assert/strict";
import { test } from "node:test";
import { event, HTMLInputElement, HTMLSelectElement, page, run } from "./dom.mjs";

const TABLE = `
<div class="site-table-filters" data-filters-for="t" hidden>
<select data-filter="source"><option value="">All</option></select>
<input type="checkbox" data-filter-flag="recent">
<input type="number" data-filter-min="n-max">
<input type="number" data-filter-max="n-min">
<output data-filter-count></output>
</div>
<table class="kpress-table site-table" data-site-table id="t">
<thead><tr><th data-sort="number">ID</th><th data-sort="text">Credit</th><th>Records</th></tr></thead>
<tbody>
<tr data-site-table-group><th colspan="3">Ours</th></tr>
<tr id="r-2" data-source="ours" data-n-min="11" data-n-max="11" data-flags="ours recent"><td data-value="2">T-002</td><td>levy</td><td></td></tr>
<tr id="r-10" data-source="ours" data-n-min="17" data-n-max="19" data-flags="ours"><td data-value="10">T-010</td><td>Levy</td><td></td></tr>
</tbody>
<tbody>
<tr data-site-table-group><th colspan="3">Others</th></tr>
<tr id="r-1" data-source="others" data-n-min="18" data-n-max="95" data-flags="others recent"><td data-value="1">T-001</td><td>Daniel</td><td></td></tr>
<tr id="r-x" data-source="others" data-flags="others"><td data-value="">T-0xx</td><td>Burns</td><td><details><summary>more</summary><p>body</p></details></td></tr>
</tbody>
</table>`;

/** @param {string} [url] */
const setUp = (url) => {
  const { document, window } = page(TABLE, url);
  run("devtools/overview/table.js");
  const rows = () =>
    document
      .querySelectorAll("tbody > tr")
      .filter((row) => !row.hasAttribute("data-site-table-group"))
      .map((row) => row.id);
  const shown = () =>
    document
      .querySelectorAll("tbody > tr")
      .filter((row) => !row.hidden)
      .map((row) => row.id || `group:${row.textContent}`);
  /** @param {number} index */
  const header = (index) => {
    const th = document.querySelectorAll("thead th")[index];
    assert.ok(th);
    return th;
  };
  /** @param {number} index */
  const click = (index) => {
    const button = header(index).querySelector("button.site-sort");
    assert.ok(button, "a sortable header gains its button");
    button.click();
  };
  const panel = document.querySelector(".site-table-filters");
  assert.ok(panel);
  /** @param {string} selector @param {string | boolean} value */
  const set = (selector, value) => {
    const control = panel.querySelector(selector);
    if (control instanceof HTMLInputElement && typeof value === "boolean") {
      control.checked = value;
    } else if (control instanceof HTMLInputElement || control instanceof HTMLSelectElement) {
      control.value = String(value);
    } else {
      assert.fail(`no control ${selector}`);
    }
    control.dispatchEvent(event("change"));
  };
  const count = () => panel.querySelector("[data-filter-count]")?.textContent;
  return { document, window, rows, shown, header, click, panel, set, count };
};

await test("a number column sorts ascending, descending, then back to the page's order", () => {
  const table = setUp();
  assert.deepEqual(table.rows(), ["r-2", "r-10", "r-1", "r-x"]);
  assert.equal(table.header(2).querySelector("button"), null, "no data-sort, no button");
  table.click(0);
  assert.equal(table.header(0).getAttribute("aria-sort"), "ascending");
  assert.deepEqual(table.rows(), ["r-1", "r-2", "r-10", "r-x"], "missing value last");
  table.click(0);
  assert.equal(table.header(0).getAttribute("aria-sort"), "descending");
  assert.deepEqual(table.rows(), ["r-10", "r-2", "r-1", "r-x"], "missing value still last");
  table.click(0);
  assert.equal(table.header(0).getAttribute("aria-sort"), null);
  assert.deepEqual(table.rows(), ["r-2", "r-10", "r-1", "r-x"]);
  assert.deepEqual(table.shown(), ["group:Ours", "r-2", "r-10", "group:Others", "r-1", "r-x"]);
});

await test("a text column sorts by the cell's text, and the groups stand aside while sorted", () => {
  const table = setUp();
  table.click(1);
  assert.deepEqual(table.rows(), ["r-x", "r-1", "r-2", "r-10"]);
  assert.deepEqual(table.shown(), ["r-x", "r-1", "r-2", "r-10"]);
  table.click(0);
  assert.equal(table.header(1).getAttribute("aria-sort"), null, "one sorted column at a time");
  assert.equal(table.header(0).getAttribute("aria-sort"), "ascending");
});

await test("the filter panel is shown and counts the rows", () => {
  const table = setUp();
  assert.equal(table.panel.hidden, false);
  assert.equal(table.count(), "All 4 shown");
});

await test("a select keeps rows whose attribute equals its value, and a group hides when empty", () => {
  const table = setUp();
  table.set("select[data-filter]", "others");
  assert.deepEqual(table.shown(), ["group:Others", "r-1", "r-x"]);
  assert.equal(table.count(), "2 of 4 shown");
  table.set("select[data-filter]", "");
  assert.equal(table.count(), "All 4 shown");
});

await test("a checked flag keeps rows whose data-flags include it", () => {
  const table = setUp();
  table.set("input[data-filter-flag]", true);
  assert.deepEqual(table.shown(), ["group:Ours", "r-2", "group:Others", "r-1"]);
});

await test("numeric bounds compare the row's attribute and drop a row without one", () => {
  const table = setUp();
  table.set("input[data-filter-min]", "18");
  assert.deepEqual(table.shown(), ["group:Ours", "r-10", "group:Others", "r-1"]);
  table.set("input[data-filter-max]", "17");
  assert.deepEqual(table.shown(), ["group:Ours", "r-10"]);
  table.set("input[data-filter-min]", "");
  table.set("input[data-filter-max]", "");
  assert.equal(table.count(), "All 4 shown");
});

await test("a row the fragment names has its details opened", () => {
  const table = setUp("http://site.test/index.html#r-x");
  const details = table.document.querySelector("#r-x details");
  assert.ok(details);
  assert.equal(details.hasAttribute("open"), true);
});
