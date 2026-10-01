/** @param {{ readyOnly?: boolean } | null} [options] */
(options = null) => {
  const results = [];
  const diagrams = document.querySelectorAll(".n11-paper figure > svg, .n11-diagram");
  for (const diagram of diagrams) {
    const svg = /** @type {SVGSVGElement} */ (diagram);
    const matrix = svg.getScreenCTM();
    const scale = matrix && Math.hypot(matrix.c, matrix.d);
    if (!scale) {
      throw new Error("diagram has no display transform");
    }
    const label = svg.querySelector("text:not(.n11-diagram-note)");
    if (!label) {
      continue;
    }
    const caption = svg.closest("figure")?.querySelector("figcaption");
    const note = svg.querySelector(".n11-diagram-note");
    results.push({
      name: svg.getAttribute("class") || "witness",
      label: Number.parseFloat(getComputedStyle(label).fontSize) * scale,
      support: Number.parseFloat(getComputedStyle(svg.parentElement).fontSize),
      note: note ? Number.parseFloat(getComputedStyle(note).fontSize) * scale : null,
      caption: caption ? Number.parseFloat(getComputedStyle(caption).fontSize) : null,
      scrollWidth: svg.parentElement?.scrollWidth ?? 0,
      clientWidth: svg.parentElement?.clientWidth ?? 0,
    });
  }
  if (options?.readyOnly !== false) {
    return (
      results.length === 4 &&
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
