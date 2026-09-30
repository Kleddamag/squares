/* The site pages' math. Every kpress formula is typeset through the explainer's own
   runtime (`squaresMath`, installed by the inlined KaTeX bundle), so a formula here is
   set exactly as it is in the explainer. The explainer's `page.js` does the same for its
   article, with its certificate figures besides, and keeps its own timing.

   **Lazily.** A formula costs the runtime a dozen milliseconds or more, and the frontier
   atlas carries hundreds, most of them far down the page or inside a closed row. So a
   formula is set when it comes within `NEAR` of the viewport (an IntersectionObserver),
   and a formula inside a closed `<details>` when the reader opens it (its `toggle`, and
   the observer, which sees the formula only once it has a box). Until then the reader
   has kpress's MathML, which is what a page without JavaScript shows.

   **`math-ready`** is added to <html> once every formula that has a box within `NEAR` of
   the viewport when the page opens has been set: what the reader can see, and a screen
   or two beyond it, is typeset. Formulas further down are set as they approach, and a
   print sets every formula first (`beforeprint`). `site-design.md` states the same
   contract for the preview and layout checks that wait for the class.

   `siteMath.typeset(root)` sets every formula under one element at once: the popover
   calls it for content it has just shown. */
(() => {
  const math = squaresMath;
  const runtime = kpressMathText;
  if (!math || !runtime) {
    return;
  }
  /** How far beyond the viewport a formula is set ahead of the reader. */
  const NEAR = "1200px 0px";
  /** @type {WeakSet<Element>} */
  const queued = new WeakSet();

  /** @param {HTMLElement} el */
  const job = (el) => {
    return async () => {
      const box = /** @type {HTMLElement | null} */ (el.querySelector(".kpress-math-render"));
      if (!box || box.dataset.done) {
        return;
      }
      const source =
        box.dataset.kpressMathSource ??
        (box.textContent ?? "")
          .trim()
          .replace(/^\\[([]/, "")
          .replace(/\\[)\]]$/, "");
      const rendered = await math.render(box, source, el.dataset.kpressMath === "display");
      box.dataset.done = "1";
      if (rendered) {
        el.dataset.kpressMathRendered = "true";
      } else {
        delete el.dataset.kpressMathRendered;
      }
    };
  };

  /** @param {Iterable<Element>} nodes */
  const setAll = async (nodes) => {
    const fresh = [...nodes].filter((node) => !queued.has(node));
    for (const node of fresh) {
      queued.add(node);
    }
    await math.batch(fresh.map((node) => job(/** @type {HTMLElement} */ (node))));
    await math.settled();
  };

  /** @param {ParentNode} root */
  const typesetIn = (root) => setAll(root.querySelectorAll(".kpress-math"));
  window.siteMath = { typeset: typesetIn };

  const finish = () => {
    runtime.complete();
    document.documentElement.classList.add("math-ready");
    window.kpressInitTooltips?.(document, { only: "footnote" });
    window.kpressInitCodeCopy?.(document);
  };

  const formulas = [...document.querySelectorAll(".kpress-math")];
  /* `?typeset=all` sets every formula before `math-ready`, closed rows included: the
     math-face check (`devtools.preview_site`) reads every formula on the page, which lazy
     setting would leave as MathML. */
  if (new URLSearchParams(globalThis.location?.search ?? "").get("typeset") === "all") {
    void setAll(formulas).then(finish);
    return;
  }
  let opening = true;
  const observer = new IntersectionObserver(
    (entries) => {
      const near = entries.filter((entry) => entry.isIntersecting).map((entry) => entry.target);
      for (const node of near) {
        observer.unobserve(node);
      }
      const set = setAll(near);
      if (opening) {
        opening = false;
        void set.then(finish);
      } else {
        void set;
      }
    },
    { rootMargin: NEAR },
  );
  for (const node of formulas) {
    observer.observe(node);
  }
  if (!formulas.length) {
    void setAll([]).then(finish);
  }

  document.addEventListener(
    "toggle",
    (event) => {
      const details = event.target;
      if (details instanceof HTMLDetailsElement && details.open) {
        void typesetIn(details);
      }
    },
    true,
  );
  window.addEventListener("beforeprint", () => {
    void setAll(formulas);
  });
})();
