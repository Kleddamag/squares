// The forwarder, run against a stand-in location and document. On the overview an old
// link to the results table or to one of its rows goes to the results page, and any
// other fragment the overview lacks goes to the explainer where it is served now, query
// string and fragment kept. On a forwarder page, which names where it sends a reader in
// `data-moved-to`, every visit goes there, query string and fragment kept.
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
 * leaves them where they are. `moved` is the page's `data-moved-to`, which only a
 * forwarder page has.
 * @param {string} hash
 * @param {{ search?: string, ids?: readonly string[], moved?: string }} [options]
 * @returns {string | null}
 */
function forwarded(hash, { search = "", ids = [], moved } = {}) {
  /** @type {string | null} */
  let target = null;
  const context = vm.createContext({
    decodeURIComponent,
    document: {
      documentElement: { dataset: moved === undefined ? {} : { movedTo: moved } },
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
  // The Frontier Survey was `#the-survey`, kept the same way.
  const survey = "#the-survey";
  assert.equal(forwarded(survey, { ids: ["the-frontier-survey", "the-survey"] }), null);
  assert.equal(forwarded(survey, { ids: ["the-frontier-survey"] }), `${EXPLAINER}${survey}`);
});

void test("a forwarder page sends every visit where it names", () => {
  assert.equal(forwarded("", { moved: "all-results.html" }), "all-results.html");
  assert.equal(forwarded("", { moved: "frontier.html" }), "frontier.html");
  const defects = "https://github.com/jlevy/squares/blob/main/defects.md";
  assert.equal(forwarded("", { moved: defects }), defects);
  // `explainer.html`, from the site's root.
  assert.equal(forwarded("", { moved: EXPLAINER }), EXPLAINER);
});

void test("a forwarder page keeps the query string and the fragment", () => {
  assert.equal(
    forwarded("#next-actions", { moved: "all-results.html", search: "?x=1" }),
    "all-results.html?x=1#next-actions",
  );
  // A fragment the old page had is not looked up: a forwarder has no content of its own.
  assert.equal(forwarded("#n-11", { moved: "frontier.html", ids: ["n-11"] }), "frontier.html#n-11");
});

void test("a paper's old address sends every visit on to the paper", () => {
  assert.equal(forwarded("#fn-3", { moved: EXPLAINER }), `${EXPLAINER}#fn-3`);
  assert.equal(
    forwarded("#381-100", { moved: EXPLAINER, search: "?review=fonts" }),
    `${EXPLAINER}?review=fonts#381-100`,
  );
  // `n11-optimality/t-060-explainer.html` and its directory's index, a level down.
  const review = "../papers/n11-optimality-review.html";
  assert.equal(forwarded("#the-capture-graph", { moved: review }), `${review}#the-capture-graph`);
  assert.equal(forwarded("", { moved: review, search: "?view=embed" }), `${review}?view=embed`);
  // Only the overview owned the results table: a moved paper's `#t-018` is the paper's.
  assert.equal(forwarded("#t-018", { moved: EXPLAINER }), `${EXPLAINER}#t-018`);
});
