// `overview/site-math.js`: formulas are typeset lazily. At opening only those the observer
// reports near the viewport are set, and `math-ready` follows them; a formula is set when
// it later comes near, when the `<details>` holding it opens, or when the page prints; and
// `siteMath.typeset(root)` sets everything under one element. None is set twice.
import assert from "node:assert/strict";
import { test } from "node:test";
import { Element, event, page, run } from "./dom.mjs";

/** @param {string} tex */
const formula = (tex) =>
  `<span class="kpress-math kpress-math-inline" data-kpress-math="inline"><span class="kpress-math-render">\\(${tex}\\)</span></span>`;

const PAGE = `<p>${formula("a")} ${formula("b")}</p><p>${formula("c")}</p>
<details><summary>more</summary>${formula("d")}</details>`;

/** @typedef {{ callback: (entries: { target: Element, isIntersecting: boolean }[]) => void, targets: Element[], options: unknown }} Observer */

const setUp = () => {
  const { document, window } = page(PAGE);
  /** @type {string[]} */
  const rendered = [];
  /** @type {Observer[]} */
  const observers = [];
  let completed = 0;
  Object.assign(globalThis, {
    squaresMath: {
      /** @param {Element} _box @param {string} source */
      render: async (_box, source) => {
        rendered.push(source);
        return true;
      },
      /** @param {ReadonlyArray<() => unknown>} jobs */
      batch: async (jobs) => {
        for (const job of jobs) {
          await job();
        }
      },
      settled: async () => {},
    },
    kpressMathText: {
      complete: () => {
        completed += 1;
      },
    },
    IntersectionObserver: class {
      /** @param {Observer["callback"]} callback @param {unknown} options */
      constructor(callback, options) {
        /** @type {Observer} */
        this.state = { callback, targets: [], options };
        observers.push(this.state);
      }

      /** @param {Element} target */
      observe(target) {
        this.state.targets.push(target);
      }

      /** @param {Element} target */
      unobserve(target) {
        this.state.targets = this.state.targets.filter((node) => node !== target);
      }
    },
  });
  run("devtools/overview/site-math.js");
  const observer = observers[0];
  assert.ok(observer, "the formulas are observed");
  const formulas = document.querySelectorAll(".kpress-math");
  /** @param {number[]} near */
  const report = (near) =>
    observer.callback(
      formulas.map((target, index) => ({ target, isIntersecting: near.includes(index) })),
    );
  const ready = () => document.documentElement.classList.contains("math-ready");
  const settle = () => new Promise((resolve) => setTimeout(resolve, 0));
  return {
    document,
    window,
    rendered,
    report,
    ready,
    settle,
    observer,
    completed: () => completed,
  };
};

await test("at opening only the formulas near the viewport are set, then math-ready", async () => {
  const math = setUp();
  assert.equal(math.observer.targets.length, 4);
  assert.equal(math.ready(), false);
  math.report([0, 1]);
  await math.settle();
  assert.deepEqual(math.rendered, ["a", "b"]);
  assert.equal(math.ready(), true);
  assert.equal(math.completed(), 1);
  assert.equal(math.observer.targets.length, 2, "a set formula is no longer observed");
});

await test("a formula is set as it comes near, and never twice", async () => {
  const math = setUp();
  math.report([0]);
  await math.settle();
  math.report([0, 2]);
  await math.settle();
  assert.deepEqual(math.rendered, ["a", "c"]);
});

await test("opening a details sets the formulas inside it", async () => {
  const math = setUp();
  math.report([]);
  await math.settle();
  const details = math.document.querySelector("details");
  assert.ok(details instanceof Element);
  details.setAttribute("open", "");
  details.dispatchEvent(event("toggle"));
  await math.settle();
  assert.deepEqual(math.rendered, ["d"]);
});

await test("printing sets every formula, and siteMath.typeset sets a subtree", async () => {
  const math = setUp();
  math.report([0]);
  await math.settle();
  const typeset = /** @type {{ siteMath?: { typeset(root: unknown): Promise<void> } }} */ (
    math.window
  ).siteMath;
  assert.ok(typeset);
  const second = math.document.querySelectorAll("p")[1];
  await typeset.typeset(second);
  assert.deepEqual(math.rendered, ["a", "c"]);
  math.window.fire(event("beforeprint"), false);
  await math.settle();
  assert.deepEqual(math.rendered, ["a", "c", "b", "d"]);
});
