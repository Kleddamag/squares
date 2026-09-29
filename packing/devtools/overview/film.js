// The atlas film plays by itself, muted and looping, as the page's moving picture
// (`autoplay muted loop playsinline` in the markup, which browsers allow without a
// gesture). A reader who has asked for reduced motion gets it paused on its first frame
// with its controls, to start when they choose.
(() => {
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  for (const film of document.querySelectorAll("video.site-film")) {
    if (film instanceof HTMLVideoElement) {
      film.autoplay = false;
      film.pause();
    }
  }
})();
