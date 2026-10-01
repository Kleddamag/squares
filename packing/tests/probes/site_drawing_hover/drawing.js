// One packing drawing and the element that holds it, as the browser paints them now: the
// states the holder is in, its background and text colour, the stroke of the drawing's
// frame and of its squares' outlines, and where a screenshot finds the frame's left edge
// and the holder's own top left corner. `holder` is a selector for the link, or the table
// row, that takes the hover.
(/** @type {{holder: string}} */ { holder }) => {
  const held = document.querySelector(holder);
  const frame = held?.querySelector("svg > rect");
  const outlines = held?.querySelector("svg > g");
  if (!held || !frame || !outlines) {
    return null;
  }
  const box = held.getBoundingClientRect();
  const edge = frame.getBoundingClientRect();
  const style = getComputedStyle(held);
  return {
    hover: held.matches(":hover"),
    focus_visible: held.matches(":focus-visible"),
    active: held.matches(":active"),
    background: style.backgroundColor,
    color: style.color,
    frame_stroke: getComputedStyle(frame).stroke,
    outline_stroke: getComputedStyle(outlines).stroke,
    box: { x: box.left, y: box.top, width: box.width, height: box.height },
    edge: { x: edge.left, y: edge.top + edge.height / 2 },
  };
};
