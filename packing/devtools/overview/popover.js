// The overview's card popovers. They open and close natively (`popovertarget`), so the
// page works without this script; it adds two things the platform does not:
//   - a formula inside a popover is typeset when the popover opens, since kpress may
//     pass over math that was hidden when it ran;
//   - a link in a popover to a place on this page closes the popover first, so the
//     reader lands on the row rather than behind the panel.
(() => {
  for (const popover of document.querySelectorAll(".site-popover[popover]")) {
    if (!(popover instanceof HTMLElement)) {
      continue;
    }
    popover.addEventListener("toggle", (event) => {
      const enhance = globalThis.enhanceMath;
      if (
        event instanceof ToggleEvent &&
        event.newState === "open" &&
        typeof enhance === "function"
      ) {
        void enhance();
      }
    });
    for (const link of popover.querySelectorAll('a[href^="#"]')) {
      link.addEventListener("click", () => {
        popover.hidePopover();
      });
    }
  }
})();
