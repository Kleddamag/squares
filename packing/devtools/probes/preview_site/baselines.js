// The text baselines of the header's labels, from the top of the document in CSS
// pixels: the site's name, every link in the navigation bar, and every section tab. A
// baseline is measured, not inferred from a box's edge: a zero-size inline-block with
// nothing in it sits with its bottom edge on the baseline of the line it is in, so one
// is placed at the end of each label, read, and taken away again. The name's is null
// where its text is not shown, on a narrow window, where the mark alone leads home.
//
// With them: the mark's box and the name's text box, to see that the mark is centred on
// the name; the rule under the bar; and for the current link and the current tab how far
// the baseline stands above the rule (the bar's own, and the foot of the tab strip), which
// is where the current link's underline is drawn from.
// `preview_site.baseline_problems` holds the name and the links to one baseline with it.
() => {
  /** @param {number} value */
  const round = (value) => Math.round(value * 100) / 100;
  /** @param {Element} label */
  const baseline = (label) => {
    const mark = document.createElement("span");
    mark.style.cssText = "display:inline-block;inline-size:0;block-size:0;padding:0;margin:0";
    label.append(mark);
    const y = mark.getBoundingClientRect().bottom + window.scrollY;
    mark.remove();
    return round(y);
  };
  /** @param {Element} el */
  const span = (el) => {
    const rect = el.getBoundingClientRect();
    return { top: round(rect.top + window.scrollY), bottom: round(rect.bottom + window.scrollY) };
  };
  /** @param {Element} el */
  const shown = (el) => el.getClientRects().length > 0;
  /** @param {Element} el */
  const labelled = (el) => ({
    label: (el.textContent ?? "").trim(),
    baseline: baseline(el),
    top: Math.round(el.getBoundingClientRect().top + window.scrollY),
    current: el.getAttribute("aria-current") === "page",
  });
  const nav = document.querySelector(".site-nav");
  const header = document.querySelector(".kpress-site-header");
  const text = document.querySelector(".site-nav .site-name-text");
  const logo = document.querySelector(".site-nav .site-logo");
  const tabs = document.querySelector("nav.site-tabs");
  /** @param {Element | null} el */
  const ruled = (el) =>
    el !== null && Number.parseFloat(getComputedStyle(el).borderBottomWidth) > 0;
  const owner = [header, nav].find(ruled) ?? null;
  const rule = owner ? round(owner.getBoundingClientRect().bottom + window.scrollY) : null;
  const links = [...document.querySelectorAll(".site-nav a[data-page]")].map(labelled);
  const strip = tabs ? [...tabs.querySelectorAll("a")].map(labelled) : [];
  const current = links.find((link) => link.current) ?? null;
  const currentTab = strip.find((tab) => tab.current) ?? null;
  return {
    name: text && shown(text) ? baseline(text) : null,
    name_text: text && shown(text) ? span(text) : null,
    logo: logo && shown(logo) ? span(logo) : null,
    links,
    tabs: strip,
    rule,
    current_above_rule: current && rule !== null ? round(rule - current.baseline) : null,
    current_tab_above_foot:
      currentTab && tabs
        ? round(tabs.getBoundingClientRect().bottom + window.scrollY - currentTab.baseline)
        : null,
  };
};
