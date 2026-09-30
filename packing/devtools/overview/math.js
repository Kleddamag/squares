// Typesets a kpress page's formulas the way the explainer typesets its own: through the
// explainer's host adapter, `squaresMath` (`probes/render_explainer/host_math_init.js`,
// inlined after KPress's shared runtime by `render_explainer.katex_js`), in batches of
// sixteen per task so no formula holds the main thread for the rest. The formulas within
// two screens of the viewport go first; the rest wait until the reader scrolls toward
// them, what hides them opens, or the browser is idle after the page has loaded. Each
// formula shows as soon as its own faces have loaded; until then its MathML fallback
// keeps its place. A formula whose faces missed
// the runtime's wait is asked for again once the page and its fonts have loaded, twice
// at most, and keeps its MathML if it still cannot be typeset. When the load-time work
// is done the page gains `math-ready`, the explainer's signal.
//
// `siteMath.typeset(root)` queues what is still untypeset under `root`; the case records
// (`case-view.js`) call it when a record is shown, and the popovers when one opens.
(() => {
  const math = globalThis.squaresMath;
  if (!math) {
    return;
  }
  const UNTYPESET =
    ".kpress-math:not([data-kpress-math-rendered]):not([data-kpress-math-error]):not([data-site-math-queued])";
  const RETRIES = 2;
  /** @type {Set<HTMLElement>} */
  const failed = new Set();

  /** @param {HTMLElement} box */
  const source = (box) =>
    (box.textContent ?? "")
      .trim()
      .replace(/^\\[([]/, "")
      .replace(/\\[)\]]$/, "");

  /** @param {HTMLElement} host */
  const job = (host) => async () => {
    const box = host.querySelector(".kpress-math-render");
    if (!(box instanceof HTMLElement)) {
      delete host.dataset.siteMathQueued;
      return;
    }
    try {
      const rendered = await math.render(box, source(box), host.dataset.kpressMath === "display");
      if (rendered) {
        host.dataset.kpressMathRendered = "true";
        failed.delete(host);
      } else {
        failed.add(host);
      }
    } finally {
      delete host.dataset.siteMathQueued;
    }
  };

  /** @param {HTMLElement[]} hosts */
  const queue = (hosts) => {
    for (const host of hosts) {
      host.dataset.siteMathQueued = "";
    }
    return hosts.length ? math.batch(hosts.map(job)) : Promise.resolve();
  };

  // A formula more than two screens away waits until the reader scrolls toward it, or
  // until what hides it opens: typesetting costs a style pass over the whole document
  // per formula, and a long report has more than a thousand of them.
  /** @type {Set<HTMLElement>} */
  const waiting = new Set();
  /** @type {HTMLElement[]} */
  let arriving = [];
  const nearing = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting && entry.target instanceof HTMLElement) {
          nearing.unobserve(entry.target);
          waiting.delete(entry.target);
          arriving.push(entry.target);
        }
      }
      const hosts = arriving.filter((host) => host.matches(UNTYPESET));
      arriving = [];
      void queue(hosts);
    },
    { rootMargin: "200% 0px" },
  );

  /**
   * Typesets the formulas under `root` that are near the viewport now, and watches the
   * rest. `all` typesets every one at once, for a panel that has just opened.
   * @param {ParentNode} root
   * @param {boolean} [all]
   */
  const typeset = (root, all = false) => {
    const height = window.innerHeight;
    /** @type {HTMLElement[]} */
    const near = [];
    for (const host of root.querySelectorAll(UNTYPESET)) {
      if (!(host instanceof HTMLElement)) {
        continue;
      }
      const box = host.getBoundingClientRect();
      const shown = host.getClientRects().length > 0;
      if (all || (shown && box.bottom > -2 * height && box.top < 3 * height)) {
        near.push(host);
      } else {
        nearing.observe(host);
        waiting.add(host);
      }
    }
    return queue(near);
  };

  const retry = async () => {
    for (let round = 0; round < RETRIES && failed.size; round += 1) {
      const again = [...failed];
      failed.clear();
      for (const host of again) {
        host.dataset.siteMathQueued = "";
      }
      await math.batch(again.map(job));
      await math.settled();
    }
  };

  // Once the load-time work is done, the formulas still waiting are typeset one at a time
  // in the browser's idle time, so a reader who jumps or scrolls fast finds them set, and
  // no task grows long: each takes a few milliseconds, and one is started only while the
  // idle period has room for it.
  const IDLE_ROOM_MS = 12;
  /** @param {{timeRemaining(): number}} deadline */
  const idle = (deadline) => {
    for (const host of waiting) {
      if (deadline.timeRemaining() < IDLE_ROOM_MS) {
        break;
      }
      waiting.delete(host);
      nearing.unobserve(host);
      if (host.matches(UNTYPESET)) {
        host.dataset.siteMathQueued = "";
        void job(host)();
      }
    }
    if (waiting.size) {
      whenIdle();
    }
  };
  const whenIdle = () => {
    if (typeof globalThis.requestIdleCallback === "function") {
      requestIdleCallback(idle);
      return;
    }
    setTimeout(() => {
      const start = performance.now();
      idle({ timeRemaining: () => 40 - (performance.now() - start) });
    }, 100);
  };

  globalThis.siteMath = { typeset };

  const start = async () => {
    await typeset(document);
    await math.settled();
    await new Promise((resolve) => {
      if (document.readyState === "complete") {
        resolve(undefined);
      } else {
        window.addEventListener("load", () => resolve(undefined), { once: true });
      }
    });
    await document.fonts.ready;
    await retry();
    globalThis.kpressMathText?.complete();
    document.documentElement.classList.add("math-ready");
    whenIdle();
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => void start(), { once: true });
  } else {
    void start();
  }
})();
