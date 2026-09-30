// Every formula whose face disagrees with the words around it, for `preview_site`.
//
// kpress draws a formula's letters and digits from the sans composite only where the
// page stamped `data-kpress-math-face="sans"` on it, so the mark is the whole decision
// and it can be wrong both ways: an unmarked formula in a sans caption or table cell is
// set in PT Serif, and a marked one in a serif paragraph is set in Source Sans.
//
// The words' face is read off the nearest ancestor that is not math markup (`wrappers`,
// the renderer's selector list), because the wrappers declare a face of their own. Sans
// or prose is decided by comparing that container's computed `font-family` with both of
// the tokens in scope on it, so a container matching neither is reported, not guessed.
// This is the face walk of `check_math_faces` alone, without that check's assertions
// about the explainer's own init, tables and first paint.
/** @param {{ wrappers: string }} o */
({ wrappers }) => {
  /** @param {string | null | undefined} value */
  const first = (value) =>
    /** @type {string} */ ((value || "").split(",")[0]).trim().replace(/^["']|["']$/g, "");
  /** @param {Element} el */
  const where = (el) => {
    const parts = [];
    for (
      let e = /** @type {Element | null} */ (el);
      e && e !== document.body && parts.length < 4;
      e = e.parentElement
    ) {
      const id = e.id ? `#${e.id}` : "";
      parts.unshift(e.tagName.toLowerCase() + id);
    }
    return parts.join(" > ");
  };
  /** @type {string[]} */
  const findings = [];
  const nodes = [...document.querySelectorAll(".katex")];
  for (const node of nodes) {
    let words = node.parentElement;
    while (words?.matches(wrappers)) {
      words = words.parentElement;
    }
    if (!words) {
      continue;
    }
    const style = getComputedStyle(words);
    const drawn = first(style.fontFamily);
    const isSans = drawn === first(style.getPropertyValue("--kpress-font-sans"));
    const isProse = drawn === first(style.getPropertyValue("--kpress-font-prose"));
    const marked = !!node.closest('[data-kpress-math-face="sans"]');
    const at = `${where(node)} [${drawn}]`;
    if (!isSans && !isProse) {
      findings.push(`mathematics in words set in neither the sans nor the prose: ${at}`);
    } else if (isSans && !marked) {
      findings.push(`sans words, serif mathematics: ${at}`);
    } else if (isProse && !isSans && marked) {
      findings.push(`serif words, sans mathematics: ${at}`);
    }
  }
  return { nodes: nodes.length, findings };
};
