/* Keep SVG labels at the publication support-text size through viewBox scaling. */
(() => {
  const diagrams = [
    ...document.querySelectorAll(
      ".line-fig svg, .chart svg, .n11-paper figure > svg, .n11-diagram",
    ),
  ].map((svg) => /** @type {SVGSVGElement} */ (svg));
  function sizeDiagramLabels() {
    for (const svg of diagrams) {
      if (!svg.getBoundingClientRect().width) {
        continue;
      }
      const matrix = svg.getScreenCTM();
      const scale = matrix && Math.hypot(matrix.c, matrix.d);
      if (!scale) {
        continue;
      }
      const size = parseFloat(getComputedStyle(svg.parentElement).fontSize) / scale;
      svg.style.setProperty("--paper-diagram-font-size", `${size}px`);
      const caption = svg.closest("figure")?.querySelector("figcaption");
      if (caption) {
        const noteSize = parseFloat(getComputedStyle(caption).fontSize) / scale;
        svg.style.setProperty("--paper-diagram-note-size", `${noteSize}px`);
      }
    }
  }
  const diagramObserver = new ResizeObserver(sizeDiagramLabels);
  diagrams.forEach((svg) => {
    diagramObserver.observe(svg);
  });
  window.addEventListener("beforeprint", sizeDiagramLabels);
  window.addEventListener("afterprint", sizeDiagramLabels);
  window.matchMedia("print").addEventListener("change", sizeDiagramLabels);
  void document.fonts.ready.then(sizeDiagramLabels);
  sizeDiagramLabels();
})();
