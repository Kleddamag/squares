/** @param {{ readyOnly?: boolean } | null} [options] */
(options = null) => {
  const results = [];
  // Every diagram that carries a label. A drawing with no lettering, the construction
  // and the capacity cell, has no label whose size could be off.
  const diagrams = [...document.querySelectorAll(".n11-paper figure > svg, .n11-diagram")].filter(
    (diagram) => diagram.querySelector("text:not(.n11-diagram-note)"),
  );
  for (const diagram of diagrams) {
    const svg = /** @type {SVGSVGElement} */ (diagram);
    const parent = svg.parentElement;
    if (!parent) {
      throw new Error("diagram has no parent element");
    }
    const matrix = svg.getScreenCTM();
    const scale = matrix && Math.hypot(matrix.c, matrix.d);
    if (!scale) {
      throw new Error("diagram has no display transform");
    }
    const label = svg.querySelector("text:not(.n11-diagram-note)");
    if (!label) {
      throw new Error("diagram has no label");
    }
    const caption = svg.closest("figure")?.querySelector("figcaption");
    const note = svg.querySelector(".n11-diagram-note");
    const bounds = svg.getBoundingClientRect();
    const overflowingLabels = Array.from(svg.querySelectorAll("text"))
      .filter((text) => {
        const box = text.getBoundingClientRect();
        return (
          box.left < bounds.left - 1 ||
          box.right > bounds.right + 1 ||
          box.top < bounds.top - 1 ||
          box.bottom > bounds.bottom + 1
        );
      })
      .map((text) => text.textContent);
    results.push({
      overflowingLabels,
      name: svg.getAttribute("class") || "witness",
      label: Number.parseFloat(getComputedStyle(label).fontSize) * scale,
      support: Number.parseFloat(getComputedStyle(parent).fontSize),
      note: note ? Number.parseFloat(getComputedStyle(note).fontSize) * scale : null,
      caption: caption ? Number.parseFloat(getComputedStyle(caption).fontSize) : null,
      scrollWidth: parent.scrollWidth,
      clientWidth: parent.clientWidth,
    });
  }
  if (options?.readyOnly !== false) {
    return (
      results.length > 0 &&
      results.length === diagrams.length &&
      results.every(
        (role) =>
          Math.abs(role.label - role.support) < 0.1 &&
          (role.note === null ||
            (role.caption !== null && Math.abs(role.note - role.caption) < 0.1)),
      )
    );
  }
  return results;
};
