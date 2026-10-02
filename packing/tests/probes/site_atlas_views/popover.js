// The atlas popover as it stands: whether it is open, the case its headline names, what
// has the keyboard focus, a tile by its n or any other element by its id, and whether the
// note that says a drawing is regularized shows under the drawing.
() => {
  const popover = document.querySelector("[data-atlas-popover]");
  const focus = document.activeElement;
  const note = popover?.querySelector("[data-atlas-layer-note]");
  return {
    open: popover?.matches(":popover-open") === true,
    title: popover?.querySelector("[data-atlas-title] .kpress-math-semantic")?.textContent ?? null,
    focus: focus?.getAttribute("data-atlas-n") ?? focus?.id ?? focus?.className ?? null,
    note: note instanceof HTMLElement ? note.getClientRects().length > 0 : null,
  };
};
