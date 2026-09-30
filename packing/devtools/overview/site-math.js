/* The site pages' math. Every kpress formula is typeset through the explainer's own
   runtime (`squaresMath`, installed by the inlined KaTeX bundle), so a formula here is
   set exactly as it is in the explainer. The page is then marked `math-ready`, which the
   preview and layout checks wait for, and kpress's footnote previews are booted, so their
   clones carry rendered formulas. The explainer's `page.js` does the same for its article,
   with its certificate figures besides.

   `siteMath.typeset(root)` sets the formulas under one element later on: the popover
   calls it for the opening section of a document, which the page carries in a
   `<template>` and so is not in the document when the page first typesets. */
(() => {
  const math = squaresMath;
  const runtime = kpressMathText;
  if (!math || !runtime) {
    return;
  }
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
  /** @param {ParentNode} root */
  const typesetIn = async (root) => {
    const nodes = [...root.querySelectorAll(".kpress-math")].map(
      (node) => /** @type {HTMLElement} */ (node),
    );
    await math.batch(nodes.map(job));
    await math.settled();
  };
  window.siteMath = { typeset: typesetIn };
  const typeset = async () => {
    await typesetIn(document);
    runtime.complete();
    document.documentElement.classList.add("math-ready");
    window.kpressInitTooltips?.(document, { only: "footnote" });
    window.kpressInitCodeCopy?.(document);
  };
  void typeset();
})();
