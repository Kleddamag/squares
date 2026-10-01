// The site's one way to show a table row's detail: the row is the unit
// (paper-design.md, Row popovers). A row with detail names its popover,
// `<tr data-row-popover="ID">`, and carries one native trigger in a cell,
// `<button class="site-row-open" popovertarget="ID">`; the popover is a card's
// (`.site-popover`), placed after the table. Without this script the trigger opens it and
// nothing else is needed. This script makes the whole row the control:
//   - the row takes focus and the trigger leaves the tab order, so each row is one stop;
//   - a click anywhere on the row, or Enter or Space while the row has focus, opens its
//     popover; a link, button or form control of the row's own keeps its own behaviour,
//     and a click that ends a text selection selects rather than opens;
//   - opening moves focus to the popover's close cross and marks the row expanded;
//     closing, by the cross, Escape or a click outside, marks it collapsed and returns
//     focus to the row.
// Sorting and filtering (`table.js`) move and hide rows; a row finds its popover by id,
// so the popover follows its row.
//
// A popover's body may wait in a `<template data-row-pop-body>`, which the browser
// parses but neither lays out nor typesets: it is placed just before the popover first
// opens, however it is opened, and `popover.js` then typesets its math. A page whose
// every row carries a long body pays for a body only when a reader asks for it.
(() => {
  /** What a click on a row leaves alone: the row's own links and controls. */
  const CONTROLS = "a[href], button, input, select, textarea, label, summary";

  /**
   * The popover a row names, if it is on the page and the browser has popovers.
   * @param {HTMLElement} row
   * @returns {HTMLElement | null}
   */
  function popoverOf(row) {
    const id = row.getAttribute("data-row-popover");
    const popover = id ? document.getElementById(id) : null;
    return popover instanceof HTMLElement && typeof popover.showPopover === "function"
      ? popover
      : null;
  }

  /**
   * Whether the reader has just selected text in the row, which a click ends.
   * @param {HTMLElement} row
   * @returns {boolean}
   */
  function selecting(row) {
    const selection = document.getSelection();
    return (
      selection !== null &&
      !selection.isCollapsed &&
      selection.anchorNode !== null &&
      row.contains(selection.anchorNode)
    );
  }

  /**
   * Make one row the control for its popover. Safe to call twice.
   * @param {HTMLElement} row
   */
  function wire(row) {
    const popover = popoverOf(row);
    if (popover === null || row.hasAttribute("data-row-ready")) {
      return;
    }
    row.setAttribute("data-row-ready", "");
    row.tabIndex = 0;
    row.setAttribute("aria-expanded", "false");
    row.setAttribute("aria-controls", popover.id);
    for (const trigger of row.querySelectorAll("[popovertarget]")) {
      if (trigger instanceof HTMLElement) {
        trigger.tabIndex = -1;
      }
    }

    const open = () => {
      if (popover.matches(":popover-open")) {
        return;
      }
      popover.showPopover();
      // The toggle event below says the same a task later; the row's wash should not wait.
      row.setAttribute("aria-expanded", "true");
      const close = popover.querySelector(".site-popover-close");
      if (close instanceof HTMLElement) {
        close.focus();
      }
    };

    row.addEventListener("click", (event) => {
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey ||
        !(event.target instanceof Element)
      ) {
        return;
      }
      const control = event.target.closest(CONTROLS);
      const trigger = control?.getAttribute("popovertarget") === popover.id;
      if ((control !== null && row.contains(control) && !trigger) || selecting(row)) {
        return;
      }
      // The trigger opens its popover natively too; cancelling the click leaves one
      // path, this one, so focus moves the same way however the row was pressed.
      event.preventDefault();
      open();
    });

    row.addEventListener("keydown", (event) => {
      if (
        event.target !== row ||
        (event.key !== "Enter" && event.key !== " ") ||
        event.altKey ||
        event.ctrlKey ||
        event.metaKey
      ) {
        return;
      }
      event.preventDefault();
      open();
    });

    // A body held in a template is placed before the popover shows, so it is there for
    // the first paint and for the math pass the open popover gets.
    popover.addEventListener("beforetoggle", (event) => {
      if (!(event instanceof ToggleEvent) || event.newState !== "open") {
        return;
      }
      for (const held of popover.querySelectorAll("template[data-row-pop-body]")) {
        if (held instanceof HTMLTemplateElement) {
          held.replaceWith(held.content);
        }
      }
    });

    popover.addEventListener("toggle", (event) => {
      if (!(event instanceof ToggleEvent)) {
        return;
      }
      const opened = event.newState === "open";
      row.setAttribute("aria-expanded", String(opened));
      if (opened) {
        return;
      }
      // Back to the row, unless the reader has already moved on to something else, such
      // as another row whose press closed this popover.
      const focus = document.activeElement;
      if (
        focus === null ||
        focus === document.body ||
        popover.contains(focus) ||
        (row.contains(focus) && focus !== row)
      ) {
        row.focus();
      }
    });
  }

  /** Wire every row with detail on the page. */
  function init() {
    for (const row of document.querySelectorAll("tr[data-row-popover]")) {
      if (row instanceof HTMLElement) {
        wire(row);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
