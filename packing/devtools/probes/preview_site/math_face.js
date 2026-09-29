// Every typeset formula whose face disagrees with the text around it: sans math in
// serif prose, or serif math in sans prose. kpress picks the face from a fixed list of
// sans contexts, so a site style that sets a block in the other face goes unnoticed.
// Formulas kpress leaves in the stock KaTeX face are neither, and are not reported.
() => {
  /** @param {string} family */
  const first = (family) => (family.split(",")[0] ?? "").trim().replace(/^["']|["']$/g, "");
  const sans = first(
    getComputedStyle(document.documentElement).getPropertyValue("--kpress-font-sans"),
  );
  /** @type {Record<string, boolean>} */
  const faces = { "KPress Math Text": false, "KPress Math Text Sans": true };
  const found = [];
  for (const math of document.querySelectorAll(".kpress-math[data-kpress-math-rendered]")) {
    const host = math.parentElement;
    const katex = math.querySelector(".katex");
    if (!(host && katex)) {
      continue;
    }
    const mathSans = faces[first(getComputedStyle(katex).fontFamily)];
    if (mathSans === undefined) {
      continue;
    }
    const textSans = first(getComputedStyle(host).fontFamily) === sans;
    if (mathSans !== textSans) {
      const where = host.closest("[id]")?.id ?? "";
      const tag = `${host.tagName.toLowerCase()}.${host.className || "-"}`;
      const tex = math.querySelector("annotation")?.textContent ?? "";
      found.push(
        `${mathSans ? "sans" : "serif"} math in ${textSans ? "sans" : "serif"} text: ` +
          `${tag} in #${where}: ${tex.slice(0, 40)}`,
      );
    }
  }
  return found;
};
