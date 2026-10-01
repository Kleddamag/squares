// `preview_site/math_face.js` over a stand-in page: a formula in each face inside serif
// prose, sans text, and a headline. A headline's words are sans, and its math follows
// them unless the headline is mathematics standing alone, which is serif by design
// (paper-design.md, Math).
import assert from "node:assert/strict";
import { afterEach, test } from "node:test";
import { probe } from "../probe.mjs";

const SANS = '"Source Sans 3 Variable", sans-serif';
const SERIF = '"Source Serif 4 Variable", serif';
const FACE = { serif: '"KPress Math Text", serif', sans: '"KPress Math Text Sans", sans-serif' };

/** The stand-in for the page's `Element`, which the probe tests child nodes against. */
class Element {
  /** @param {string} classes */
  constructor(classes) {
    this.classes = classes.split(" ");
    this.textContent = "";
  }

  /** @param {string} selector */
  matches(selector) {
    return selector.split(",").some((one) => this.classes.includes(one.trim().slice(1)));
  }
}

/**
 * A typeset formula in `face` whose host is set in `family`: a paragraph of prose, or a
 * popover's headline holding the formula alone or after `words`.
 * @param {keyof typeof FACE | "stock"} face
 * @param {string} family
 * @param {{ headline?: boolean, words?: string, id?: string }} [options]
 */
function formula(face, family, { headline = false, words = "", id = "host" } = {}) {
  const katex = { fontFamily: face === "stock" ? "KaTeX_Main" : FACE[face] };
  const math = new Element("kpress-math");
  const className = headline ? "site-popover-value" : "prose";
  const host = Object.assign(new Element(className), {
    fontFamily: family,
    tagName: "P",
    className,
    childNodes: words ? [{ textContent: words }, math] : [math],
    /** @param {string} selector */
    closest: (selector) => {
      assert.equal(selector, "[id]");
      return { id };
    },
  });
  return Object.assign(math, {
    parentElement: host,
    /** @param {string} selector */
    querySelector: (selector) => (selector === ".katex" ? katex : { textContent: `tex of ${id}` }),
  });
}

/**
 * What the probe reports for a page of these formulas.
 * @param {ReturnType<typeof formula>[]} formulas
 * @returns {string[]}
 */
function report(formulas) {
  const root = {};
  Object.assign(globalThis, {
    Element,
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
  Reflect.deleteProperty(globalThis, "Element");
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
    "serif math in sans text: p.prose in #a: tex of a",
    "sans math in serif text: p.prose in #host: tex of host",
  ]);
});

void test("a headline that is all math expects serif math though its own face is sans", () => {
  assert.deepEqual(report([formula("serif", SANS, { headline: true })]), []);
  assert.deepEqual(report([formula("sans", SANS, { headline: true, id: "pop" })]), [
    "sans math in a headline that is all math: p.site-popover-value in #pop: tex of pop",
  ]);
});

void test("a headline with words expects its math in their sans face", () => {
  assert.deepEqual(report([formula("sans", SANS, { headline: true, words: "Earlier " })]), []);
  assert.deepEqual(
    report([formula("serif", SANS, { headline: true, words: "Earlier ", id: "pop" })]),
    ["serif math in sans text: p.site-popover-value in #pop: tex of pop"],
  );
});
