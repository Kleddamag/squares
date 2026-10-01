// Installed before any page script runs: records the page's long tasks and, on every
// animation frame, how much of its mathematics is typeset and showing -- the formulas in
// the first viewport and every displayed formula on the page. A formula is readable when
// its KaTeX HTML is present and no render of it is pending; a hidden record, an inactive
// variant or a collapsed certificate is not displayed and is not counted.
// `measure_site_pages` reads the result through `report.js`.
() => {
  const MATH = ".kpress-math, .tex, .tex-d";
  const LIMIT_MS = 30_000;
  const state = {
    /** @type {number[][]} */
    longTasks: [],
    frames: 0,
    /** @type {number | null} */
    visibleMathMs: null,
    /** @type {number | null} */
    allMathMs: null,
    /** @type {number | null} */
    mathReadyMs: null,
    visibleMath: 0,
    displayedMath: 0,
    readableMath: 0,
    done: false,
  };
  Object.assign(window, { siteLoadMeasure: state });
  try {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        state.longTasks.push([entry.startTime, entry.duration]);
      }
    }).observe({ type: "longtask", buffered: true });
  } catch {
    // A browser without long-task timing reports none.
  }
  /** @param {Element} el */
  const readable = (el) => {
    if (
      el.matches("[data-kpress-math-pending]") ||
      el.querySelector("[data-kpress-math-pending]")
    ) {
      return false;
    }
    const html = el.querySelector(".katex-html");
    if (!html) {
      return false;
    }
    return getComputedStyle(html).visibility !== "hidden";
  };
  const tick = () => {
    state.frames += 1;
    const now = performance.now();
    if (document.body) {
      const nodes = [...document.querySelectorAll(MATH)].filter(
        (el) => !el.parentElement?.closest(MATH),
      );
      const height = window.innerHeight;
      let visible = 0;
      let visibleReady = 0;
      let displayed = 0;
      let ready = 0;
      for (const el of nodes) {
        const rects = el.getClientRects();
        const first = rects[0];
        if (!first) {
          continue;
        }
        displayed += 1;
        const ok = readable(el);
        if (ok) {
          ready += 1;
        }
        if (first.top < height && first.bottom > 0) {
          visible += 1;
          if (ok) {
            visibleReady += 1;
          }
        }
      }
      state.visibleMath = visible;
      state.displayedMath = displayed;
      state.readableMath = ready;
      const parsed = document.readyState !== "loading";
      if (parsed && state.visibleMathMs === null && visibleReady === visible) {
        state.visibleMathMs = now;
      }
      if (parsed && state.allMathMs === null && ready === displayed) {
        state.allMathMs = now;
      }
      // A page that typesets its off-screen math only as it nears the viewport marks the
      // end of its load-time work with `math-ready`, as the explainer does.
      if (state.mathReadyMs === null && document.documentElement.classList.contains("math-ready")) {
        state.mathReadyMs = now;
      }
      if (
        state.visibleMathMs !== null &&
        (state.allMathMs !== null || state.mathReadyMs !== null)
      ) {
        state.done = true;
      }
    }
    if (now > LIMIT_MS) {
      state.done = true;
    }
    if (!state.done) {
      requestAnimationFrame(tick);
    }
  };
  requestAnimationFrame(tick);
};
