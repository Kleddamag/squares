// `preview_site/math_face.js` over a stand-in page: a formula in each face inside serif
// prose, sans text, and a popover headline marked `data-math-face="serif"`, whose words
// are sans and whose math is serif by design (paper-design.md, Math).
import assert from "node:assert/strict";
import { afterEach, test } from "node:test";
import { probe } from "../probe.mjs";

const SANS = '"Source Sans 3 Variable", sans-serif';
const SERIF = '"Source Serif 4 Variable", serif';
const FACE = { serif: '"KPress Math Text", serif', sans: '"KPress Math Text Sans", sans-serif' };

/**
 * A typeset formula in `face` whose host is set in `family`, marked for serif math or not.
 * @param {keyof typeof FACE | "stock"} face
 * @param {string} family
 * @param {{ marked?: boolean, id?: string }} [options]
 */
function formula(face, family, { marked = false, id = "host" } = {}) {
  const katex = { fontFamily: face === "stock" ? "KaTeX_Main" : FACE[face] };
  const host = {
    fontFamily: family,
    tagName: "P",
    className: "site-popover-value",
    /** @param {string} selector */
    closest: (selector) => {
      if (selector === "[id]") {
        return { id };
      }
      assert.equal(selector, '[data-math-face="serif"]');
      return marked ? host : null;
    },
  };
  return {
    parentElement: host,
    /** @param {string} selector */
    querySelector: (selector) => (selector === ".katex" ? katex : { textContent: `tex of ${id}` }),
  };
}

/**
 * What the probe reports for a page of these formulas.
 * @param {ReturnType<typeof formula>[]} formulas
 * @returns {string[]}
 */
function report(formulas) {
  const root = {};
  Object.assign(globalThis, {
    document: { documentElement: root, querySelectorAll: () => formulas },
    /** @param {{ fontFamily?: string }} element */
    getComputedStyle: (element) => ({
      fontFamily: element.fontFamily ?? "",
      getPropertyValue: () => (element === root ? SANS : ""),
    }),
  });
  return /** @type {() => string[]} */ (probe("devtools/probes/preview_site/math_face.js"))();
}

afterEach(() => {
  Reflect.deleteProperty(globalThis, "document");
  Reflect.deleteProperty(globalThis, "getComputedStyle");
});

void test("math in the face of its text is not reported, nor is stock KaTeX", () => {
  assert.deepEqual(
    report([formula("serif", SERIF), formula("sans", SANS), formula("stock", SANS)]),
    [],
  );
});

void test("math in the other face from its text is reported", () => {
  assert.deepEqual(report([formula("serif", SANS, { id: "a" }), formula("sans", SERIF)]), [
    "serif math in sans text: p.site-popover-value in #a: tex of a",
    "sans math in serif text: p.site-popover-value in #host: tex of host",
  ]);
});

void test("a headline marked for serif math expects serif math in its sans words", () => {
  assert.deepEqual(report([formula("serif", SANS, { marked: true })]), []);
  assert.deepEqual(report([formula("sans", SANS, { marked: true, id: "pop" })]), [
    "sans math in text marked for serif math: p.site-popover-value in #pop: tex of pop",
  ]);
});
