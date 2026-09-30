// `overview/forward.js`: an old deep link into the explainer, which was the site's root
// page, still reaches it. Any non-empty fragment that is not an id on the overview goes to
// `explainer.html` with the same fragment and query string; an id on the overview, or no
// fragment, stays.
import assert from "node:assert/strict";
import { test } from "node:test";
import { page, run } from "./dom.mjs";

const OVERVIEW = '<h2 id="recent-results">Recent Results</h2><tr id="result-t-037"></tr>';

/** @param {string} url */
const forwarded = (url) => {
  const { window } = page(OVERVIEW, url);
  run("devtools/overview/forward.js");
  return window.location.replaced;
};

await test("a fragment the overview lacks goes to the explainer, query string and all", () => {
  assert.equal(
    forwarded("http://site.test/?review=fonts#381-100"),
    "explainer.html?review=fonts#381-100",
  );
  assert.equal(forwarded("http://site.test/#fn-3"), "explainer.html#fn-3");
  assert.equal(
    forwarded("http://site.test/#proof-of-the-new-lower-bound"),
    "explainer.html#proof-of-the-new-lower-bound",
  );
});

await test("an id on the overview, or no fragment at all, stays on the overview", () => {
  assert.equal(forwarded("http://site.test/#recent-results"), null);
  assert.equal(forwarded("http://site.test/index.html#result-t-037"), null);
  assert.equal(forwarded("http://site.test/"), null);
  assert.equal(forwarded("http://site.test/#"), null);
});

await test("an escaped fragment is compared decoded and forwarded as written", () => {
  assert.equal(forwarded("http://site.test/#recent%2Dresults"), null);
  assert.equal(forwarded("http://site.test/#19%2D5"), "explainer.html#19%2D5");
  assert.equal(forwarded("http://site.test/#%E0%A4%A"), "explainer.html#%E0%A4%A");
});
