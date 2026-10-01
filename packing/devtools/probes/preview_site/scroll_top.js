// Return the page to its top at once and say whether it is there. A wheel scroll
// animates, so a full-page screenshot taken while one is still running draws the page
// offset by the distance left to go, blank at the top and cut off at the foot.
() => {
  window.scrollTo({ top: 0, left: 0, behavior: "instant" });
  return window.scrollY === 0;
};
