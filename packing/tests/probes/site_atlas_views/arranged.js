// Whether the triangle is now arranged for `per_line` tiles to a line, which a resize
// settles a frame after the window changes.
(/** @type {{per_line: number}} */ { per_line }) =>
  document
    .querySelector(".site-atlas-cells")
    ?.getAttribute("style")
    ?.includes(`--site-atlas-per-line: ${per_line};`) === true;
