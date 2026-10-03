// The record page, `cases/` (`cases/index.html`), is the index of every case
// (`nav[data-case-index]`) and the reader that shows one record in its place
// (`[data-case-reader]`). Without this script the page is the index, each of whose links
// goes to a record file, which a reader without scripts reads plain.
//
// `cases/?n=11` and `cases/#n-11` show case 11: the record file sends a reader with
// scripts here that way (`case-forward.js`), with the fragment they came with. The record
// is fetched from its file beside this page, `11.html`, parsed in a `<template>` so the
// file's script never runs, and its article (`article.site-case`) placed in the reader;
// the page takes the file's title, the index steps aside, and the address bar then reads
// the file's own address (`history.replaceState`), with any other fragment kept. A
// record's steps (`a[data-case-step]`), a link in it to another case, and the index's
// links (`a[data-case]`) load that case in place and push its address
// (`history.pushState`); the record's link to every case (`a[data-case-index]`) pushes
// `./` and shows the index again. Back and Forward show what the address then names,
// read from its file, `…/cases/12.html`, or from the directory alone for the index.
//
// Each change lands at the top of the page, or at the element in the record a kept
// fragment names; Back and Forward land where the reader was, as kpress's history noted
// it on that entry. A press that takes away what had focus, a step or a link in the
// index, gives it to the same step in the record that replaces it, or to the record or
// the index now shown. The record's math is typeset as the site's math driver typesets
// a page (`math.js`): what is near the viewport now, the rest as the reader nears it.
//
// A record that cannot be fetched, as none can on a page read from a file, leaves what
// is shown as it is and sends the reader to the file itself, `11.html?raw`, which the
// file's own script does not send back here.
(() => {
  const reader = document.querySelector("[data-case-reader]");
  if (!(reader instanceof HTMLElement)) {
    return;
  }
  const found = document.querySelector("nav[data-case-index]");
  const index = found instanceof HTMLElement ? found : null;
  const pageTitle = document.title;

  /** @param {string} digits */
  const caseNumber = (digits) => String(Number(digits));

  /**
   * The case an address names, and the fragment it keeps: its file, `…/12.html`, which
   * the address bar reads once a record is shown; failing that `?n=12`, or `#n-12`. A
   * case named in any form but the file's is written back as the file's (`rewrite`).
   * @param {URL} url
   * @returns {{ n: string, hash: string, rewrite: boolean } | null}
   */
  const named = (url) => {
    const fragment = /^#n-(\d+)$/.exec(url.hash)?.[1];
    const hash = fragment === undefined ? url.hash : "";
    const file = /\/(\d+)\.html$/.exec(url.pathname)?.[1];
    if (file !== undefined) {
      return { n: caseNumber(file), hash, rewrite: false };
    }
    const query = url.searchParams.get("n");
    if (query !== null && /^\d+$/.test(query)) {
      return { n: caseNumber(query), hash, rewrite: true };
    }
    if (fragment !== undefined) {
      return { n: caseNumber(fragment), hash, rewrite: true };
    }
    return null;
  };

  /**
   * One case's record and its file's title.
   * @param {string} url
   * @returns {Promise<{ article: HTMLElement, title: string }>}
   */
  const fetchRecord = async (url) => {
    if (location.protocol === "file:") {
      throw new Error("a page read from a file cannot fetch a record");
    }
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`${url}: ${response.status}`);
    }
    const parsed = document.createElement("template");
    parsed.innerHTML = await response.text();
    const article = parsed.content.querySelector("article.site-case");
    if (!(article instanceof HTMLElement)) {
      throw new Error(`${url} holds no case record`);
    }
    const heading = parsed.content.querySelector("title")?.textContent ?? "";
    return { article, title: heading.replace(/\s+/g, " ").trim() };
  };

  /**
   * Each record asked for, by case. The article itself is kept, so a record shown again
   * keeps its typeset math; a failure is dropped, so the next press asks again.
   * @type {Map<string, Promise<{ article: HTMLElement, title: string }>>}
   */
  const records = new Map();
  /** @param {string} n */
  const record = (n) => {
    let held = records.get(n);
    if (held === undefined) {
      held = fetchRecord(new URL(`${n}.html`, location.href).href);
      records.set(n, held);
      void held.catch(() => {
        records.delete(n);
      });
    }
    return held;
  };

  /**
   * The case the reader shows, or null while the page is the index.
   * @type {string | null}
   */
  let shown = null;
  /**
   * The case on its way.
   * @type {string | null}
   */
  let wanted = null;
  /** The number of the latest change asked for: only it may show its record, or navigate. */
  let latest = 0;

  /**
   * The element in the record shown that a fragment names.
   * @param {string} hash
   */
  const spot = (hash) => {
    let id = hash.slice(1);
    try {
      id = decodeURIComponent(id);
    } catch {
      // A malformed escape is looked for as it was written.
    }
    return id ? reader.querySelector(`#${CSS.escape(id)}`) : null;
  };

  /**
   * Where the page stands after a change. kpress's history notes on each entry where the
   * reader was (`kpressScroll` in its state); a record that Back or Forward returns to
   * may arrive after the browser has restored the scroll, so the note is applied here.
   * @param {string} hash
   * @param {boolean} returning
   */
  const land = (hash, returning) => {
    /** @type {unknown} */
    const state = history.state;
    const noted =
      returning && typeof state === "object" && state !== null && "kpressScroll" in state
        ? state.kpressScroll
        : undefined;
    if (typeof noted === "number" && Number.isFinite(noted)) {
      window.scrollTo({ top: noted, behavior: "instant" });
      return;
    }
    const place = hash ? spot(hash) : null;
    if (place !== null) {
      place.scrollIntoView({ behavior: "instant", block: "start" });
      return;
    }
    window.scrollTo({ top: 0, behavior: "instant" });
  };

  /** Whether focus is on what a change takes away: the record shown, or the index. */
  const losing = () => {
    const focus = document.activeElement;
    return (
      focus === null ||
      focus === document.body ||
      reader.contains(focus) ||
      (index?.contains(focus) ?? false)
    );
  };

  /**
   * Give `target` focus where it stands. An element that takes no focus of its own holds
   * `tabindex="-1"` until it loses it again.
   * @param {Element} target
   */
  const focusOn = (target) => {
    if (!(target instanceof HTMLElement)) {
      return;
    }
    if (target.tabIndex < 0 && !target.hasAttribute("tabindex")) {
      target.setAttribute("tabindex", "-1");
      target.addEventListener("blur", () => target.removeAttribute("tabindex"), { once: true });
    }
    target.focus({ preventScroll: true });
  };

  /**
   * Show case `n`'s record, and write its address as `how` says: pushed for a press,
   * written over the current entry for an address that named the case another way, and
   * left alone on Back and Forward. `rel` is the step pressed, if one was.
   * @param {string} n
   * @param {{ article: HTMLElement, title: string }} shownRecord
   * @param {"push" | "replace" | "none"} how
   * @param {string} hash
   * @param {string | undefined} rel
   */
  const place = (n, shownRecord, how, hash, rel) => {
    const { article, title } = shownRecord;
    const moveFocus = how === "push" && losing();
    shown = n;
    reader.replaceChildren(article);
    reader.hidden = false;
    if (index !== null) {
      index.hidden = true;
    }
    document.title = title || pageTitle;
    const address = `${n}.html${hash}`;
    if (how === "push") {
      history.pushState(null, "", address);
    } else if (how === "replace") {
      history.replaceState(history.state, "", address);
    }
    if (moveFocus) {
      const step = rel ? article.querySelector(`a[data-case-step][rel~="${rel}"]`) : null;
      focusOn(step ?? article);
    }
    land(hash, how === "none");
    void globalThis.siteMath?.typeset(reader);
  };

  /**
   * Fetch case `n`'s record and show it (`place`), or go to its file.
   * @param {string} n
   * @param {"push" | "replace" | "none"} how
   * @param {string} hash
   * @param {string | undefined} rel
   */
  const open = (n, how, hash, rel) => {
    latest += 1;
    const request = latest;
    wanted = n;
    void record(n).then(
      (fetched) => {
        if (request === latest) {
          wanted = null;
          place(n, fetched, how, hash, rel);
        }
      },
      () => {
        if (request === latest) {
          wanted = null;
          location.href = `${n}.html?raw${hash}`;
        }
      },
    );
  };

  /**
   * Show the index again, with the address `./` pushed for a press.
   * @param {"push" | "none"} how
   */
  const showIndex = (how) => {
    latest += 1;
    wanted = null;
    if (shown === null) {
      return;
    }
    const moveFocus = how === "push" && losing();
    shown = null;
    reader.hidden = true;
    reader.replaceChildren();
    if (index !== null) {
      index.hidden = false;
    }
    document.title = pageTitle;
    if (how === "push") {
      history.pushState(null, "", "./");
    }
    if (moveFocus && index !== null) {
      focusOn(index);
    }
    land("", how === "none");
  };

  /** Show what the address names: on arrival, and on Back and Forward. */
  const follow = () => {
    const target = named(new URL(location.href));
    if (target === null) {
      showIndex("none");
    } else if (target.n !== wanted && target.n !== shown) {
      open(target.n, target.rewrite ? "replace" : "none", target.hash, undefined);
    }
  };

  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      !(event.target instanceof Element)
    ) {
      return;
    }
    const link = event.target.closest("a[href]");
    if (
      !(link instanceof HTMLAnchorElement) ||
      (link.target !== "" && link.target !== "_self") ||
      link.hasAttribute("download")
    ) {
      return;
    }
    const inRecord = reader.contains(link);
    if (inRecord && link.hasAttribute("data-case-index")) {
      event.preventDefault();
      showIndex("push");
      return;
    }
    const listed = index?.contains(link) === true && link.hasAttribute("data-case");
    const stepped =
      inRecord && (link.hasAttribute("data-case-step") || link.hasAttribute("data-case"));
    if (!listed && !stepped) {
      return;
    }
    // Only a record file beside this page loads in place; any other address is followed.
    const url = new URL(link.href);
    const file = /\/(\d+)\.html$/.exec(url.pathname)?.[1];
    if (file === undefined || new URL("./", url).href !== new URL("./", location.href).href) {
      return;
    }
    event.preventDefault();
    const n = caseNumber(file);
    if (n !== wanted) {
      const rel = ["prev", "next"].find((token) => link.relList.contains(token));
      open(n, "push", url.hash, rel);
    }
  });

  window.addEventListener("popstate", follow);
  follow();
})();
