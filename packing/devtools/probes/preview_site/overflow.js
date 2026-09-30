// The page's widest content against its viewport. A page wider than its viewport scrolls
// sideways on a phone, which is the overflow `preview_site` refuses.
() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
});
