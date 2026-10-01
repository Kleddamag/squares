// How many math spans kpress has not yet typeset. It renders them progressively, near
// the viewport first, so a screenshot taken at load shows the untypeset fallback below.
() => document.querySelectorAll(".kpress-math:not([data-kpress-math-rendered])").length;
