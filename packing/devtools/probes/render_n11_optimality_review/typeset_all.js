// Has the paper typeset every formula now, wherever it stands on the page. The site's
// math driver (`overview/math.js`) typesets the formulas near the window at once and
// leaves the rest to the browser's idle time, which a print must not wait on: asked for
// all of them, it queues every formula still untypeset and resolves when they are done.
// A page without the driver answers nothing, and the caller's own wait reports it.
() =>
  /** @type {{siteMath?: {typeset(root: ParentNode, all?: boolean): Promise<void>}}} */ (
    globalThis
  ).siteMath?.typeset(document, true);
