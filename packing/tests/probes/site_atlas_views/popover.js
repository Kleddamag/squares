// The atlas popover as it stands: whether it is open, the case its headline names, and
// what has the keyboard focus, a tile by its n or any other element by its id.
() => {
  const popover = document.querySelector("[data-atlas-popover]");
  const focus = document.activeElement;
  return {
    open: popover?.matches(":popover-open") === true,
    title: popover?.querySelector("[data-atlas-title] .kpress-math-semantic")?.textContent ?? null,
    focus: focus?.getAttribute("data-atlas-n") ?? focus?.id ?? focus?.className ?? null,
  };
};
