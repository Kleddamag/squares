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

void test("a first day reads ISO dates as text, and an empty one is no limit", () => {
  /** @param {string} value @returns {SiteTableFilter[]} */
  const since = (value) => [{ key: "date", kind: "since", value }];
  const row = { date: "2026-09-04" };
  assert.ok(table.rowMatches(row, since("2026-09-04")));
  assert.ok(table.rowMatches(row, since("2026-08-31")));
  assert.ok(!table.rowMatches(row, since("2026-09-05")));
  assert.ok(table.rowMatches(row, since("")));
  // A row with no date is older than every limit.
  assert.ok(!table.rowMatches({}, since("2026-01-01")));
  assert.ok(table.rowMatches({}, since("")));
});

void test("a maximum age in days is the first day a row may be dated, from a given day", () => {
  // The same reckoning as `overview_sections.age_cutoff`, which writes the HTML's default.
  assert.equal(table.ageCutoff("2026-09-30", "180"), "2026-04-03");
  assert.equal(table.ageCutoff("2026-10-01", "0"), "2026-10-01");
  assert.equal(table.ageCutoff("2026-10-01", "1"), "2026-09-30");
  assert.equal(table.ageCutoff("2026-03-01", "1"), "2026-02-28");
  assert.equal(table.ageCutoff("2024-03-01", "1"), "2024-02-29");
  assert.equal(table.ageCutoff("2026-01-01", "1"), "2025-12-31");
  assert.equal(table.ageCutoff("2026-10-01", "365"), "2025-10-01");
  // Part of a day is not counted, and an age below none is none.
  assert.equal(table.ageCutoff("2026-10-01", "1.9"), "2026-09-30");
  assert.equal(table.ageCutoff("2026-10-01", "-5"), "2026-10-01");
  // Empty is no limit, and so is an age that is no number or is past the calendar.
  assert.equal(table.ageCutoff("2026-10-01", ""), "");
  assert.equal(table.ageCutoff("2026-10-01", "old"), "");
  assert.equal(table.ageCutoff("2026-10-01", "1e12"), "");
  assert.equal(table.ageCutoff("2026-10-01", "999999"), "");
  assert.equal(table.ageCutoff("", "180"), "");
});

void test("the reader's day is the local one, as an ISO date", () => {
  assert.equal(table.localDay(new Date(2026, 0, 5, 23, 59)), "2026-01-05");
  assert.equal(table.localDay(new Date(2026, 9, 1, 0, 0)), "2026-10-01");
  assert.equal(table.localDay(new Date(2026, 11, 31, 12)), "2026-12-31");
});

void test("a case filter finds its number in a row's list of cases and ranges", () => {
  assert.ok(table.covers("11", 11));
  assert.ok(!table.covers("11", 1));
  assert.ok(table.covers("27 28 31-32", 28));
  assert.ok(table.covers("27 28 31-32", 31));
  assert.ok(table.covers("27 28 31-32", 32));
  assert.ok(!table.covers("27 28 31-32", 29));
  assert.ok(table.covers("1-324", 200));
  assert.ok(!table.covers("", 1));
  /** @param {string} value @returns {SiteTableFilter[]} */
  const wanted = (value) => [{ key: "n", kind: "covers", value }];
  assert.ok(table.rowMatches({ n: "18-21 26" }, wanted("20")));
  assert.ok(!table.rowMatches({ n: "18-21 26" }, wanted("22")));
  assert.ok(table.rowMatches({ n: "18-21 26" }, wanted("")));
  assert.ok(!table.rowMatches({}, wanted("20")));
});

/** A value each kind of filter refuses the row below with. */
const FAILING = {
  equals: { value: "nothing-of-the-kind" },
  flag: { value: "true" },
  min: { value: "6" },
  max: { value: "0" },
  since: { value: "2026-10-01" },
  covers: { value: "44" },
};

void test("filters compose: a row shows only when it passes every one", () => {
  const row = {
    source: "others",
    v: "4",
    c: "3",
    s: "4",
    standing: "current-best",
    n: "45",
    date: "2026-09-27",
  };
  /** @type {SiteTableFilter[]} */
  const all = [
    { key: "s", kind: "min", value: "4" },
    { key: "v", kind: "min", value: "4" },
    { key: "c", kind: "min", value: "3" },
    { key: "standing", kind: "equals", value: "current-best" },
    { key: "source", kind: "equals", value: "others" },
    { key: "n", kind: "covers", value: "45" },
    { key: "date", kind: "since", value: "2026-09-01" },
  ];
  assert.ok(table.rowMatches(row, all));
  all.forEach((filter, index) => {
    const narrowed = all.map((other, at) =>
      at === index ? { ...filter, ...FAILING[filter.kind] } : other,
    );
    assert.ok(!table.rowMatches(row, narrowed), `${filter.key} ${filter.kind}`);
  });
});

void test("a group heading shows while a row under it does, until the table is sorted", () => {
  // Two groups: the first has one row showing, the second none.
  const headings = [true, false, false, true, false];
  const passes = [false, false, true, false, false];
  assert.deepEqual([...table.rowsShown(headings, passes, true)], [true, false, true, false, false]);
  assert.deepEqual(
    [...table.rowsShown(headings, passes, false)],
    [false, false, true, false, false],
  );
  // A heading never shows on its own account, and a row before any heading needs none.
  assert.deepEqual([...table.rowsShown([true, false], [true, false], true)], [false, false]);
  assert.deepEqual(
    [...table.rowsShown([false, true, false], [true, false, true], true)],
    [true, true, true],
  );
});

void test("a covers control takes the plain key as its query parameter, and an age `age`", () => {
  assert.equal(table.controlParam("n", "covers"), "n");
  assert.equal(table.controlParam("date", "age"), "age");
  assert.equal(table.controlParam("s", "min"), "s-min");
});
