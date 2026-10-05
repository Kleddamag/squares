// The transition the browser computes for the first element `selector` names: the
// properties it lists, their durations and their easings, or null where the page has no
// such element.
(/** @type {{selector: string}} */ { selector }) => {
  const found = document.querySelector(selector);
  if (!found) {
    return null;
  }
  const style = getComputedStyle(found);
  return {
    property: style.transitionProperty,
    duration: style.transitionDuration,
    easing: style.transitionTimingFunction,
  };
};
