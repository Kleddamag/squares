// The site table script's pure functions, run in a context with no document, as the page
// script itself is: it publishes them on `globalThis.SiteTable` and skips the DOM wiring.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/table.js", import.meta.url),
  "utf8",
);

/** @returns {SiteTableApi} */
function load() {
  const context = vm.createContext({});
  vm.runInContext(SOURCE, context);
  return context.SiteTable;
}

const table = load();

void test("a numeric sort reads numbers, not text", () => {
  const keys = ["10", "9", "100", "3.875"];
  assert.deepEqual([...table.sortOrder(keys, "num", "ascending")], [3, 1, 0, 2]);
  assert.deepEqual([...table.sortOrder(keys, "num", "descending")], [2, 0, 1, 3]);
});

void test("a key that is not a number sorts after every number", () => {
  assert.ok(table.compareKeys("", "1", "num") > 0);
  assert.ok(table.compareKeys("1", "", "num") < 0);
  assert.equal(table.compareKeys("", "", "num"), 0);
});

void test("equal keys keep their order", () => {
  const keys = ["open", "proved", "open", "proved"];
  assert.deepEqual([...table.sortOrder(keys, "text", "ascending")], [0, 2, 1, 3]);
  assert.deepEqual([...table.sortOrder(keys, "text", "descending")], [1, 3, 0, 2]);
});

void test("a text sort puts n-9 before n-10", () => {
  assert.ok(table.compareKeys("n-9", "n-10", "text") < 0);
});

void test("filters: equals, flag and an n range", () => {
  const row = { n: "11", status: "open", open: "true", recent: "false" };
  assert.ok(table.rowMatches(row, []));
  assert.ok(table.rowMatches(row, [{ key: "status", kind: "equals", value: "" }]));
  assert.ok(table.rowMatches(row, [{ key: "status", kind: "equals", value: "open" }]));
  assert.ok(!table.rowMatches(row, [{ key: "status", kind: "equals", value: "proved" }]));
  assert.ok(table.rowMatches(row, [{ key: "open", kind: "flag", value: "true" }]));
  assert.ok(!table.rowMatches(row, [{ key: "recent", kind: "flag", value: "true" }]));
  assert.ok(table.rowMatches(row, [{ key: "recent", kind: "flag", value: "false" }]));
  assert.ok(table.rowMatches(row, [{ key: "n", kind: "min", value: "11" }]));
  assert.ok(!table.rowMatches(row, [{ key: "n", kind: "min", value: "12" }]));
  assert.ok(table.rowMatches(row, [{ key: "n", kind: "max", value: "11" }]));
  assert.ok(!table.rowMatches(row, [{ key: "n", kind: "max", value: "10" }]));
  assert.ok(table.rowMatches(row, [{ key: "n", kind: "max", value: "" }]));
});

void test("a significance floor keeps S3 and up, and an empty floor keeps all", () => {
  /** @param {string} value @returns {SiteTableFilter[]} */
  const floor = (value) => [{ key: "s", kind: "min", value }];
  assert.ok(table.rowMatches({ s: "3" }, floor("3")));
  assert.ok(table.rowMatches({ s: "5" }, floor("3")));
  assert.ok(!table.rowMatches({ s: "2" }, floor("3")));
  assert.ok(table.rowMatches({ s: "2" }, floor("")));
});

void test("the count names the total, and the share when filtered", () => {
  assert.equal(table.countText(324, 324, "cases"), "324 cases");
  assert.equal(table.countText(12, 324, "cases"), "12 of 324 cases");
});

void test("a query parameter names a filter by its key, and a bound by key and bound", () => {
  assert.equal(table.controlParam("recent", null), "recent");
  assert.equal(table.controlParam("n", "max"), "n-max");
});
