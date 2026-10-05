// The case popover's drawing as the browser lays it out now: the width of the popover's
// body, inside its padding; the drawing's width and height; the stroke width the browser
// computes for the frame and for the squares' outlines, and whether each is drawn in the
// page's own units; the height of each `svg` the caption's typeset math draws, such as a
// radical; the root's font size; and how wide the page and the popover reach against the
// window. Null until the popover shows a record with a drawing.
() => {
  const popover = document.querySelector("[data-case-popover]");
  const body = popover?.querySelector("[data-case-body]");
  const drawing = body?.querySelector(".site-case-figure > svg");
  const frame = drawing?.querySelector(":scope > rect");
  const outline = drawing?.querySelector("path");
  if (!popover || !body || !drawing || !frame || !outline) {
    return null;
  }
  const box = drawing.getBoundingClientRect();
  const framed = getComputedStyle(frame);
  const outlined = getComputedStyle(outline);
  return {
    body: body.clientWidth,
    width: box.width,
    height: box.height,
    frame: Number.parseFloat(framed.strokeWidth),
    frame_effect: framed.vectorEffect,
    outline: Number.parseFloat(outlined.strokeWidth),
    outline_effect: outlined.vectorEffect,
    caption_math: [...body.querySelectorAll(".site-case-figure > figcaption svg")].map(
      (drawn) => drawn.getBoundingClientRect().height,
    ),
    rem: Number.parseFloat(getComputedStyle(document.documentElement).fontSize),
    page_width: document.documentElement.scrollWidth,
    popover_right: popover.getBoundingClientRect().right,
    window_width: window.innerWidth,
  };
};
