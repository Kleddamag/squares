// The Visualize page's film starts when the page is visited.
//
// A browser starts a film unasked only when it is muted, so the film's markup mutes it,
// and it keeps its controls: a reader can pause it, seek, or turn it full screen. The
// markup does not carry `autoplay` itself. Markup cannot make that depend on what the
// reader asked of motion, and a film marked `preload="none"` that nothing starts fetches
// nothing. So the film is marked `data-autoplay`, and this starts it: it sets `autoplay`
// and plays, unless the reader asks for reduced motion, or the page is framed in a
// card's popover (`embed.js`), where looking at a preview should not start a download.
// A browser that will not start it rejects `play()`; the rejection is dropped and the
// film is paused, so it stays as it is for everyone else: its poster, with the play
// control. A film that cannot be fetched keeps its poster and controls too, as the
// browser leaves any film it cannot load.
(() => {
  const film = document.querySelector("video[data-autoplay]");
  if (!(film instanceof HTMLVideoElement)) {
    return;
  }
  const framed = document.documentElement.getAttribute("data-site-view") === "embed";
  if (framed || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  film.autoplay = true;
  film.play().catch(() => {
    // Refused: back to the poster and the play control.
    film.pause();
  });
})();
