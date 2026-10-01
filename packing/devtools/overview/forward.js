// Old links into pages that moved keep working.
//
// The results table moved from the overview to `all-results.html`: its section,
// `#every-result`, and each result's row (`#t-018`) are sent there, fragment kept. The
// results page's title is "Every Result", so the section's old fragment lands on it.
//
// The explainer moved from the site root to `explainer.html`. It keeps its state in the
// fragment -- section ids, footnotes (`#fn-3`) and the certificate picker (`#19-5`,
// `#381-100`) -- so any other fragment that names nothing on the overview is sent there,
// query string and all (`?review=fonts` must survive). The overview's own ids, the
// explainer's and the results page's are kept disjoint by a test, so no old link is
// captured by the wrong page.
(() => {
  const fragment = window.location.hash.slice(1);
  if (!fragment) {
    return;
  }
  let id = fragment;
  try {
    id = decodeURIComponent(fragment);
  } catch {
    // A malformed escape cannot name an element here either.
  }
  if (document.getElementById(id)) {
    return;
  }
  const moved = id === "every-result" || /^t-\d+$/.test(id);
  const target = moved ? "all-results.html" : "explainer.html";
  window.location.replace(`${target}${window.location.search}${window.location.hash}`);
})();
