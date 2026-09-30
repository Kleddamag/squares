/* Old deep links into the explainer keep working. The explainer was the site's root page
   until the overview took the root, and links into it carry their state in the fragment:
   section ids, footnotes (`#fn-3`) and the certificate picker (`#19-5`, `#381-100`). So
   any non-empty fragment that is not an id on this page goes to `explainer.html` with the
   same fragment and the same query string (`?review=fonts` must survive). The overview's
   ids and the explainer's are disjoint, which `test_overview_page.py` holds, so no old
   link is captured here. Inlined first among the page's scripts, so the reader leaves
   before anything else runs. */
(() => {
  const EXPLAINER = "explainer.html";
  const fragment = window.location.hash;
  if (fragment.length < 2) {
    return;
  }
  let id = fragment.slice(1);
  try {
    id = decodeURIComponent(id);
  } catch {
    // A malformed escape is not an id here either; forward it as written.
  }
  if (document.getElementById(id)) {
    return;
  }
  window.location.replace(`${EXPLAINER}${window.location.search}${fragment}`);
})();
