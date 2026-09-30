// Every link and embedded resource the page names, as written, so `preview_site` can
// resolve the relative ones against the assembled site and report any that are missing.
() => ({
  hrefs: [...document.querySelectorAll("a[href]")].map((a) => a.getAttribute("href") ?? ""),
  sources: [...document.querySelectorAll("img[src], source[src], video[src], iframe[src]")].map(
    (el) => el.getAttribute("src") ?? "",
  ),
  posters: [...document.querySelectorAll("video[poster]")].map(
    (el) => el.getAttribute("poster") ?? "",
  ),
});
