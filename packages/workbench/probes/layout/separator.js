// The stage separator's layout now: the stage's drawn height, whether the controls end inside
// the window, whether the page is marked as resizing, the share stored under o.key, the
// separator's ARIA range, the window's height, and the height the stage and the controls share:
// `#viewport`'s, the window's less the site's navigation bar above it on the published page.
/** @param {{key: string}} o */
(o) => {
  /** @param {string} id */
  const element = (id) => {
    const found = document.getElementById(id);
    if (found == null) {
      throw new Error(`probe requires #${id}`);
    }
    return found;
  };
  const handle = element("stage-resize");
  /** @type {string | null} */
  let stored = null;
  try {
    stored = window.localStorage.getItem(o.key);
  } catch {
    stored = null;
  }
  return {
    stageHeight: element("stage-wrap").offsetHeight,
    controlsFit: element("controls").getBoundingClientRect().bottom <= window.innerHeight + 1,
    resizing: document.body.classList.contains("resizing"),
    stored,
    valueMin: Number(handle.getAttribute("aria-valuemin")),
    valueMax: Number(handle.getAttribute("aria-valuemax")),
    valueNow: Number(handle.getAttribute("aria-valuenow")),
    innerHeight: window.innerHeight,
    viewportHeight: element("viewport").clientHeight,
  };
};
