// Whether the page has finished typesetting: `math-ready` is set by the site pages'
// `site-math.js` and the explainer's `page.js` once every formula is drawn. A page with no
// formulas has nothing to wait for.
() =>
  document.documentElement.classList.contains("math-ready") ||
  document.querySelector(".kpress-math, .tex, .tex-d") === null;
