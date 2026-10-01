// The overview's fragment forwarder, run against a stand-in location and document: an
// old link to the results table or to one of its rows goes to the results page, and any
// other fragment the overview lacks goes to the explainer, query string and fragment kept.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/forward.js", import.meta.url),
  "utf8",
);

/**
 * Where the forwarder sends a reader arriving with `search` and `hash`, or null when it
 * leaves them on the overview.
 * @param {string} hash
 * @param {{ search?: string, ids?: readonly string[] }} [options]
 * @returns {string | null}
 */
function forwarded(hash, { search = "", ids = [] } = {}) {
  /** @type {string | null} */
  let target = null;
  const context = vm.createContext({
    decodeURIComponent,
    document: {
      /** @param {string} id */
      getElementById: (id) => (ids.includes(id) ? {} : null),
    },
    window: {
      location: {
        hash,
        search,
        /** @param {string} url */
        replace: (url) => {
          target = url;
        },
      },
    },
  });
  vm.runInContext(SOURCE, context);
  return target;
}

void test("the old results section goes to the results page", () => {
  assert.equal(forwarded("#every-result"), "all-results.html#every-result");
});

void test("a result's row goes to its row on the results page", () => {
  assert.equal(forwarded("#t-018"), "all-results.html#t-018");
  assert.equal(forwarded("#t-037", { search: "?x=1" }), "all-results.html?x=1#t-037");
});

void test("any other missing fragment still goes to the explainer", () => {
  assert.equal(forwarded("#fn-3"), "explainer.html#fn-3");
  assert.equal(
    forwarded("#381-100", { search: "?review=fonts" }),
    "explainer.html?review=fonts#381-100",
  );
});

void test("a fragment the overview has, or none, stays", () => {
  assert.equal(forwarded("#recent-results", { ids: ["recent-results"] }), null);
  assert.equal(forwarded(""), null);
});

void test("a renamed section's old fragment stays while an anchor keeps its id", () => {
  // Verification Ladders was `#verification-at-a-glance`; its heading keeps an empty
  // anchor of that id, without which the old link would be sent to the explainer.
  const old = "#verification-at-a-glance";
  const kept = ["verification-ladders", "verification-at-a-glance"];
  assert.equal(forwarded(old, { ids: kept }), null);
  assert.equal(forwarded(old, { ids: ["verification-ladders"] }), `explainer.html${old}`);
});
