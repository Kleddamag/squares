// Set every formula on a site page now, closed rows and far-down sections included, so a
// full-page screenshot and the math-face walk see KaTeX rather than the MathML fallback
// lazy setting leaves below the fold. `site-math.js` installs `siteMath`; the explainer
// sets its whole article itself and has none, so there this does nothing.
async () => {
  await window.siteMath?.typeset(document);
};
