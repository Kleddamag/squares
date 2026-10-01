// Tells a page which platform it runs on, before any of its scripts ask: an init script
// that answers `navigator.platform` with the name it is applied to. The publication
// layer's head script reads the platform to choose how formulas are rasterised
// (`explainer/native-math-metrics.js`), so this is how the branch a machine would not
// take is exercised on it. Only the answer changes; the glyphs are still drawn by the
// machine the browser runs on.
(/** @type {string} */ platform) => {
  Object.defineProperty(Navigator.prototype, "platform", {
    configurable: true,
    get: () => platform,
  });
};
