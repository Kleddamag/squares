// Whether the atlas has tiles placed and none of them is in a move.
() =>
  document.querySelector(".site-atlas-cells .site-atlas-cell") !== null &&
  document
    .getAnimations()
    .every(
      (animation) =>
        animation instanceof CSSTransition ||
        !(animation.effect instanceof KeyframeEffect) ||
        animation.effect.target?.matches(".site-atlas-cell") !== true ||
        animation.playState === "finished",
    );
