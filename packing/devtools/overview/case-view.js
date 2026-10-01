// The case records page shows one record at a time: the one its fragment names
// (`cases.html#n-11`), or, with no fragment, the index of every case. Without this
// script every record is listed and the fragment scrolls to the one asked for.
//
// A record's formulas are typeset only when it is shown. The site's math driver
// (`math.js`) typesets every formula on the page once the document is parsed, and there
// are thousands here; this script runs first, marks the formulas of every record not
// shown as done, and hands them back to the driver when their record is shown.
(() => {
  const root = document.querySelector("[data-case-records]");
  if (!(root instanceof HTMLElement)) {
    return;
  }
  /** @type {Map<string, HTMLElement>} */
  const records = new Map();
  for (const record of root.querySelectorAll(".site-case[id]")) {
    if (record instanceof HTMLElement) {
      records.set(record.id, record);
    }
  }
  const page = document.documentElement;
  const title = document.title;

  /** @param {HTMLElement} record */
  const defer = (record) => {
    for (const host of record.querySelectorAll(".kpress-math:not([data-kpress-math-rendered])")) {
      if (host instanceof HTMLElement) {
        host.dataset.kpressMathRendered = "true";
        host.dataset.siteMathDeferred = "";
      }
    }
  };
  /** @param {HTMLElement} record */
  const release = (record) => {
    const deferred = record.querySelectorAll("[data-site-math-deferred]");
    if (deferred.length === 0) {
      return;
    }
    for (const host of deferred) {
      if (host instanceof HTMLElement) {
        delete host.dataset.kpressMathRendered;
        delete host.dataset.siteMathDeferred;
      }
    }
    void globalThis.siteMath?.typeset(record);
  };

  // A record opens at the top of the page with the navigation in view. KPress scrolls
  // its viewport pane rather than the window, so both are reset.
  const toTop = () => {
    document.querySelector(".kpress-viewport")?.scrollTo(0, 0);
    window.scrollTo(0, 0);
  };

  const show = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const current = records.get(id);
    if (!current) {
      page.removeAttribute("data-case-current");
      document.title = title;
      return;
    }
    page.setAttribute("data-case-current", id);
    for (const record of records.values()) {
      record.toggleAttribute("data-current", record === current);
    }
    release(current);
    const label = current.dataset.n ? `n = ${current.dataset.n}` : id;
    document.title = `${label} · ${title}`;
    toTop();
    // The browser's own jump to the fragment can land after this runs, so settle once more.
    requestAnimationFrame(toTop);
  };

  page.setAttribute("data-case-view", "");
  for (const record of records.values()) {
    defer(record);
  }
  show();
  window.addEventListener("hashchange", show);
  window.addEventListener("load", () => {
    if (records.has(decodeURIComponent(location.hash.slice(1)))) {
      toTop();
    }
  });
})();
