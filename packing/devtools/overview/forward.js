// Old links into pages that moved keep working.
//
// A page that moved whole, or was withdrawn, is still served at its old address, as a
// forwarder (`render_overview.forwarder_pages`): its root element names where a visit is
// sent now, in `data-moved-to`, and every visit is sent there with its query string and
// its fragment. Three repository documents left the site that way: `results.html` goes
// to the results table, `status.html` to the frontier atlas, and `defects.html` to the
// defect log on GitHub. The papers moved that way, to `papers/<slug>.html`: the explainer
// from `explainer.html` and the optimality paper from
// `n11-optimality/t-060-explainer.html`. Both keep their state in the fragment --
// section ids, footnotes (`#fn-3`) and the explainer's certificate picker (`#19-5`,
// `#381-100`) -- and `?review=fonts` must survive. A forwarder also carries a link and,
// for a reader without scripts, a refresh, neither of which can keep a fragment.
//
// The overview is not a forwarder, and forwards by fragment. The results table moved from
// it to `all-results.html`: its section, `#every-result`, and each result's row (`#t-018`)
// are sent there, fragment kept. The results page's title is "Every Result", so the
// section's old fragment lands on it. Verification Ladders moved there too, on
// 2026-10-02: its fragment, `#verification-ladders`, and the older
// `#verification-at-a-glance`, which an empty anchor in its heading keeps, are sent
// there the same way. The Frontier Survey section left the overview the same day, its
// account the Frontier page's own: its fragment, `#the-frontier-survey`, and the older
// `#the-survey` are sent to `frontier.html`, whose title carries the first. The explainer
// was once the site's root, so any other fragment that names nothing on the overview is
// sent to the explainer, query string and all. The overview's own ids, the explainer's
// and the results page's are kept disjoint by a test, so no old link is captured by the
// wrong page.
(() => {
  /** @param {string} target */
  const forward = (target) => {
    window.location.replace(`${target}${window.location.search}${window.location.hash}`);
  };
  const moved = document.documentElement.dataset.movedTo;
  if (moved) {
    forward(moved);
    return;
  }
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
  const result =
    id === "every-result" ||
    id === "verification-ladders" ||
    id === "verification-at-a-glance" ||
    /^t-\d+$/.test(id);
  if (result) {
    forward("all-results.html");
  } else if (id === "the-frontier-survey" || id === "the-survey") {
    forward("frontier.html");
  } else {
    forward("papers/n11-lower-bounds-explainer.html");
  }
})();
