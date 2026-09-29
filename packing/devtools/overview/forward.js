// Old links into the explainer keep working after it moved from the site root to
// `explainer.html`. The explainer keeps its state in the fragment -- section ids,
// footnotes (`#fn-3`) and the certificate picker (`#19-5`, `#381-100`) -- so any
// fragment that names nothing on the overview is sent there, query string and all
// (`?review=fonts` must survive). The overview's own ids and the explainer's are kept
// disjoint by a test, so no old link is captured here.
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
  window.location.replace(`explainer.html${window.location.search}${window.location.hash}`);
})();
