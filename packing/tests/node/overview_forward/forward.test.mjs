// The site's forwarder, run against a stand-in location and document. On the overview, an
// old link to the results table or to one of its rows goes to the results page, and any
// other fragment the overview lacks goes to the explainer, query string and fragment kept.
// On a page that moved whole, whose root element names where it is now, every visit goes
// there, query string and fragment kept.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/forward.js", import.meta.url),
  "utf8",
);

/** Where the explainer is served, from the site's root. */
const EXPLAINER = "papers/n11-lower-bounds-explainer.html";

/**
 * Where the forwarder sends a reader arriving with `search` and `hash`, or null when it
 * leaves them where they are. `ids` are the elements the page has; `movedTo` is what a
 * forwarder page's root element says, absent on the overview.
 * @param {string} hash
 * @param {{ search?: string, ids?: readonly string[], movedTo?: string }} [options]
 * @returns {string | null}
 */
function forwarded(hash, { search = "", ids = [], movedTo } = {}) {
  /** @type {string | null} */
  let target = null;
  const context = vm.createContext({
    decodeURIComponent,
    document: {
      documentElement: { dataset: movedTo === undefined ? {} : { movedTo } },
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

void test("any other missing fragment goes to the explainer where it is served now", () => {
  assert.equal(forwarded("#fn-3"), `${EXPLAINER}#fn-3`);
  assert.equal(
    forwarded("#381-100", { search: "?review=fonts" }),
    `${EXPLAINER}?review=fonts#381-100`,
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
  assert.equal(forwarded(old, { ids: ["verification-ladders"] }), `${EXPLAINER}${old}`);
});

void test("a page that moved sends every visit on, fragment and query string kept", () => {
  // `explainer.html`, from the site's root.
  assert.equal(forwarded("", { movedTo: EXPLAINER }), EXPLAINER);
  assert.equal(forwarded("#fn-3", { movedTo: EXPLAINER }), `${EXPLAINER}#fn-3`);
  assert.equal(
    forwarded("#381-100", { movedTo: EXPLAINER, search: "?review=fonts" }),
    `${EXPLAINER}?review=fonts#381-100`,
  );
  // `n11-optimality/t-060-explainer.html` and its directory's index, a level down.
  const review = "../papers/n11-optimality-review.html";
  assert.equal(forwarded("#the-capture-graph", { movedTo: review }), `${review}#the-capture-graph`);
  assert.equal(forwarded("", { movedTo: review, search: "?view=embed" }), `${review}?view=embed`);
});

void test("a page that moved forwards a results fragment to its own page, not the table", () => {
  // Only the overview owned the results table: a moved paper's `#t-018` is the paper's.
  assert.equal(forwarded("#t-018", { movedTo: EXPLAINER }), `${EXPLAINER}#t-018`);
  // And a fragment that happens to name something on the forwarder still goes on.
  assert.equal(forwarded("#x", { movedTo: EXPLAINER, ids: ["x"] }), `${EXPLAINER}#x`);
});
