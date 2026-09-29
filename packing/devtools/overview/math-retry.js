// kpress typesets each formula once, as soon as the page is parsed, and gives up on one
// whose faces are not ready within its wait: that formula keeps its MathML fallback,
// drawn in whatever sans face the browser picks. A long page with every face inlined can
// take longer to decode them all than that wait, and on the synopsis about a third of
// the formulas were left behind. Once the page and its fonts have loaded, ask kpress
// again for whatever is still untypeset; it skips what it has already done. Three
// rounds bound the work if a formula can never be typeset.
(() => {
  const ROUNDS = 3;
  let rounds = 0;
  const untypeset = () =>
    document.querySelector(".kpress-math:not([data-kpress-math-rendered])") !== null;
  const retry = () => {
    const enhance = globalThis.enhanceMath;
    if (rounds >= ROUNDS || typeof enhance !== "function" || !untypeset()) {
      return;
    }
    rounds += 1;
    Promise.resolve(enhance()).then(retry, retry);
  };
  window.addEventListener("load", () => {
    document.fonts.ready.then(retry, retry);
  });
})();
