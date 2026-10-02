// Scroll the page so The Atlas, its heading, starts at the window's top edge, and say
// where the heading then stands.
() => {
  const heading = document.getElementById("the-atlas");
  heading?.scrollIntoView({ block: "start" });
  return heading ? Math.round(heading.getBoundingClientRect().top) : null;
};
