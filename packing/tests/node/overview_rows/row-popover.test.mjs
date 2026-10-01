// The row popover script, run against a stand-in document: a table of two rows, each
// naming its popover, with a link and the native trigger in its cells. The stand-ins do
// what the platform does for a popover (`showPopover`, `hidePopover`, the `toggle`
// event, `:popover-open`) and for focus, so the test reads the script's own part:
// which presses open a row's popover, where focus goes, and what the row is told.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(
  new URL("../../../devtools/overview/row-popover.js", import.meta.url),
  "utf8",
);

/** The script's own selectors, which is all the stand-in has to match. */
const COMPOUND = /^([a-z]+)?((?:\[[a-z-]+\]|\.[a-z-]+|:popover-open)*)$/;

/**
 * @typedef {object} Press what a test dispatches: a click or a key press
 * @property {number} [button]
 * @property {string} [key]
 * @property {boolean} [metaKey]
 * @property {boolean} [ctrlKey]
 * @property {boolean} [shiftKey]
 * @property {boolean} [altKey]
 * @property {string} [newState]
 */

/** One page's stand-in classes and document, in a context of its own. */
function page() {
  class StandInElement {
    /**
     * @param {string} tag
     * @param {Record<string, string>} [attributes]
     * @param {StandInElement[]} [children]
     */
    constructor(tag, attributes = {}, children = []) {
      this.tag = tag;
      /** @type {Map<string, string>} */
      this.attributes = new Map(Object.entries(attributes));
      /** @type {StandInElement[]} */
      this.children = [];
      /** @type {StandInElement | null} */
      this.parentElement = null;
      /** @type {Map<string, ((event: object) => void)[]>} */
      this.listeners = new Map();
      this.tabIndex = tag === "a" || tag === "button" ? 0 : -1;
      this.open = false;
      /** @type {StandInElement | null} what a `<template>` holds, as its fragment */
      this.content = null;
      this.append(...children);
    }

    get id() {
      return this.attributes.get("id") ?? "";
    }

    /** @param {StandInElement[]} children */
    append(...children) {
      for (const child of children) {
        child.parentElement?.remove(child);
        child.parentElement = this;
        this.children.push(child);
      }
    }

    /** @param {StandInElement} child */
    remove(child) {
      this.children = this.children.filter((other) => other !== child);
    }

    /** @param {string} name */
    getAttribute(name) {
      return this.attributes.get(name) ?? null;
    }

    /** @param {string} name @param {string} value */
    setAttribute(name, value) {
      this.attributes.set(name, value);
    }

    /** @param {string} name */
    hasAttribute(name) {
      return this.attributes.has(name);
    }

    /** @param {string} selector */
    matches(selector) {
      return selector.split(",").some((part) => {
        const found = COMPOUND.exec(part.trim());
        assert.ok(found, `the stand-in does not read the selector ${part}`);
        const [, tag, rest = ""] = found;
        const conditions = rest.match(/\[[a-z-]+\]|\.[a-z-]+|:popover-open/g) ?? [];
        return (
          (tag === undefined || tag === this.tag) &&
          conditions.every((condition) => {
            if (condition === ":popover-open") {
              return this.open;
            }
            if (condition.startsWith(".")) {
              return (this.attributes.get("class") ?? "").split(" ").includes(condition.slice(1));
            }
            return this.attributes.has(condition.slice(1, -1));
          })
        );
      });
    }

    /** @param {string} selector @returns {StandInElement | null} */
    closest(selector) {
      /** @type {StandInElement | null} */
      let element = this;
      while (element !== null && !element.matches(selector)) {
        element = element.parentElement;
      }
      return element;
    }

    /** @param {unknown} other @returns {boolean} */
    contains(other) {
      return other === this || this.children.some((child) => child.contains(other));
    }

    /** @param {string} selector @returns {StandInElement[]} */
    querySelectorAll(selector) {
      return this.children.flatMap((child) => [
        ...(child.matches(selector) ? [child] : []),
        ...child.querySelectorAll(selector),
      ]);
    }

    /** @param {string} selector */
    querySelector(selector) {
      return this.querySelectorAll(selector)[0] ?? null;
    }

    /** @param {string} type @param {(event: object) => void} listener */
    addEventListener(type, listener) {
      this.listeners.set(type, [...(this.listeners.get(type) ?? []), listener]);
    }

    focus() {
      document.activeElement = this;
    }

    /** @param {StandInElement | null} fragment whose children take this element's place */
    replaceWith(fragment) {
      const parent = this.parentElement;
      assert.ok(parent !== null && fragment !== null);
      const placed = fragment.children;
      parent.children.splice(parent.children.indexOf(this), 1, ...placed);
      for (const child of placed) {
        child.parentElement = parent;
      }
      fragment.children = [];
      this.parentElement = null;
    }

    showPopover() {
      assert.ok(!this.open, "showPopover on an open popover throws in a browser");
      fire(this, "beforetoggle", { newState: "open" });
      this.open = true;
      fire(this, "toggle", { newState: "open" });
    }

    hidePopover() {
      this.open = false;
      fire(this, "toggle", { newState: "closed" });
    }
  }

  class StandInToggleEvent {
    /** @param {string} newState */
    constructor(newState) {
      this.newState = newState;
    }
  }

  const body = new StandInElement("body");
  const document = {
    readyState: "complete",
    body,
    /** @type {StandInElement | null} */
    activeElement: body,
    /**
     * What the reader has selected; a collapsed selection is none.
     * @type {{ isCollapsed: boolean, anchorNode: StandInElement | null }}
     */
    selection: { isCollapsed: true, anchorNode: null },
    getSelection: () => document.selection,
    /** @param {string} id */
    getElementById: (id) =>
      [body, ...body.querySelectorAll("[id]")].find((element) => element.id === id) ?? null,
    /** @param {string} selector */
    querySelectorAll: (selector) => body.querySelectorAll(selector),
  };

  /**
   * Dispatch an event at `target`, bubbling to the body. Returns whether its default was
   * prevented, which for a click on a trigger is whether the platform's own opening ran.
   * @param {StandInElement} target
   * @param {string} type
   * @param {Press} [init]
   */
  function fire(target, type, init = {}) {
    const toggles = type === "toggle" || type === "beforetoggle";
    const kind = toggles ? new StandInToggleEvent(init.newState ?? "") : {};
    const event = Object.assign(kind, {
      button: 0,
      metaKey: false,
      ctrlKey: false,
      shiftKey: false,
      altKey: false,
      ...init,
      type,
      target,
      defaultPrevented: false,
      preventDefault() {
        this.defaultPrevented = true;
      },
    });
    // The toggle events do not bubble; a click and a key press do.
    /** @type {StandInElement[]} */
    const path = [];
    for (
      let element = /** @type {StandInElement | null} */ (target);
      element !== null;
      element = toggles ? null : element.parentElement
    ) {
      path.push(element);
    }
    for (const element of path) {
      for (const listener of element.listeners.get(type) ?? []) {
        listener(event);
      }
    }
    return event.defaultPrevented;
  }

  /**
   * A row with detail and its popover, as `overview_sections.row_detail` writes them.
   * @param {string} key
   * @param {Record<string, string>} [more] further attributes of the row, such as `hidden`
   * @param {boolean} [deferred] whether the popover's body waits in a template
   */
  function row(key, more = {}, deferred = false) {
    const target = `pop-${key}`;
    const trigger = new StandInElement("button", { class: "site-row-open", popovertarget: target });
    const link = new StandInElement("a", { href: `records/${key}` });
    const text = new StandInElement("td");
    const attributes = { id: key, "data-row-popover": target, ...more };
    const element = new StandInElement("tr", attributes, [
      new StandInElement("td", {}, [trigger]),
      text,
      new StandInElement("td", {}, [link]),
    ]);
    const close = new StandInElement("button", { class: "site-popover-close" });
    const detail = new StandInElement("a", { href: `detail/${key}` });
    const held = new StandInElement("template", { "data-row-pop-body": "" });
    held.content = new StandInElement("fragment", {}, [detail]);
    const body = new StandInElement("div", { class: "site-row-pop-body" }, [
      deferred ? held : detail,
    ]);
    const popover = new StandInElement("div", { id: target, class: "site-popover" }, [close, body]);
    return { element, trigger, link, text, popover, close, body, held, detail };
  }

  const first = row("t-001");
  // The second row is one the filters hide at load, as a results table writes it, and
  // its popover's body is deferred.
  const second = row("t-002", { hidden: "" }, true);
  // A row naming a popover the page does not carry: its popover is never appended.
  const orphan = row("t-003");
  const tbody = new StandInElement("tbody", {}, [first.element, second.element, orphan.element]);
  body.append(new StandInElement("table", {}, [tbody]), first.popover, second.popover);

  vm.runInContext(
    SOURCE,
    vm.createContext({
      document,
      Element: StandInElement,
      HTMLElement: StandInElement,
      HTMLTemplateElement: StandInElement,
      ToggleEvent: StandInToggleEvent,
    }),
  );
  return { document, fire, first, second, orphan, tbody };
}

void test("a row with detail becomes one tab stop, collapsed, naming its popover", () => {
  const { first } = page();
  assert.equal(first.element.tabIndex, 0);
  assert.equal(first.trigger.tabIndex, -1);
  assert.equal(first.link.tabIndex, 0);
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
  assert.equal(first.element.getAttribute("aria-controls"), "pop-t-001");
});

void test("a click anywhere on the row opens its popover and moves focus to the cross", () => {
  const { document, fire, first, second } = page();
  fire(first.text, "click");
  assert.ok(first.popover.open);
  assert.ok(!second.popover.open);
  assert.equal(document.activeElement, first.close);
  assert.equal(first.element.getAttribute("aria-expanded"), "true");
  assert.equal(second.element.getAttribute("aria-expanded"), "false");
});

void test("Enter and Space on the focused row open it, and no other key does", () => {
  for (const key of ["Enter", " "]) {
    const { fire, first } = page();
    assert.ok(fire(first.element, "keydown", { key }), "the key's own action is prevented");
    assert.ok(first.popover.open, key);
  }
  const { fire, first } = page();
  assert.ok(!fire(first.element, "keydown", { key: "ArrowDown" }));
  assert.ok(!fire(first.element, "keydown", { key: "Enter", ctrlKey: true }));
  assert.ok(!first.popover.open);
});

void test("a link in the row stays a link: neither a click nor Enter on it opens the popover", () => {
  const { fire, first } = page();
  assert.ok(!fire(first.link, "click"), "the link's own navigation is left alone");
  assert.ok(!fire(first.link, "keydown", { key: "Enter" }));
  assert.ok(!first.popover.open);
});

void test("the native trigger opens through the row's one path, not twice", () => {
  const { document, fire, first } = page();
  // Left alone, the platform would toggle the popover after this click; preventing it
  // leaves the script's own opening, which also moves focus.
  assert.ok(fire(first.trigger, "click"));
  assert.ok(first.popover.open);
  assert.equal(document.activeElement, first.close);
});

void test("a modified click, another button, or a click ending a selection does not open", () => {
  const { document, fire, first } = page();
  fire(first.text, "click", { metaKey: true });
  fire(first.text, "click", { shiftKey: true });
  fire(first.text, "click", { button: 1 });
  document.selection = { isCollapsed: false, anchorNode: first.text };
  fire(first.text, "click");
  assert.ok(!first.popover.open);
  document.selection = { isCollapsed: true, anchorNode: null };
  fire(first.text, "click");
  assert.ok(first.popover.open);
});

void test("closing, as the cross and Escape do, collapses the row and returns focus to it", () => {
  const { document, fire, first } = page();
  fire(first.text, "click");
  first.popover.hidePopover();
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
  assert.equal(document.activeElement, first.element);
});

void test("closing leaves focus where the reader has already moved it", () => {
  const { document, fire, first, second } = page();
  fire(first.text, "click");
  // A press on another row closes this popover by light dismiss, focus already there.
  second.element.focus();
  first.popover.hidePopover();
  assert.equal(document.activeElement, second.element);
  assert.equal(first.element.getAttribute("aria-expanded"), "false");
});

void test("a row moved by a sort still opens its own popover", () => {
  const { fire, first, second, tbody } = page();
  tbody.append(first.element);
  assert.deepEqual(
    tbody.children.map((element) => element.id),
    ["t-002", "t-003", "t-001"],
  );
  fire(second.text, "click");
  assert.ok(second.popover.open);
  assert.ok(!first.popover.open);
  second.popover.hidePopover();
  fire(first.text, "click");
  assert.ok(first.popover.open);
});

void test("pressing a row whose popover is open does not open it again", () => {
  const { fire, first } = page();
  fire(first.text, "click");
  // `showPopover` on an open popover throws in a browser, and in the stand-in.
  fire(first.element, "keydown", { key: "Enter" });
  assert.ok(first.popover.open);
});

void test("a row whose popover is not on the page is left as the HTML has it", () => {
  const { document, fire, first, orphan } = page();
  assert.equal(document.getElementById("pop-t-001"), first.popover);
  assert.equal(document.getElementById("pop-t-003"), null);
  assert.ok(first.element.hasAttribute("data-row-ready"));
  assert.ok(!orphan.element.hasAttribute("data-row-ready"));
  assert.equal(orphan.element.tabIndex, -1);
  assert.equal(orphan.trigger.tabIndex, 0);
  assert.ok(!orphan.element.hasAttribute("aria-expanded"));
  assert.ok(!fire(orphan.text, "click"));
});

void test("a row the filters hide at load is wired all the same, for when they show it", () => {
  const { document, fire, second } = page();
  assert.ok(second.element.hasAttribute("hidden"));
  assert.equal(second.element.tabIndex, 0);
  assert.equal(second.trigger.tabIndex, -1);
  fire(second.text, "click");
  assert.ok(second.popover.open);
  assert.equal(document.activeElement, second.close);
});

void test("a body held in a template is placed when its popover first opens, and once", () => {
  const { fire, first, second } = page();
  assert.deepEqual(second.body.children, [second.held]);
  fire(second.text, "click");
  assert.deepEqual(second.body.children, [second.detail]);
  assert.equal(second.detail.parentElement, second.body);
  second.popover.hidePopover();
  fire(second.element, "keydown", { key: "Enter" });
  assert.deepEqual(second.body.children, [second.detail]);
  // A body written in place is left as it is.
  fire(first.text, "click");
  assert.deepEqual(first.body.children, [first.detail]);
});

void test("the platform's own opening places a deferred body too", () => {
  const { second } = page();
  // What the native trigger does when the script has not taken the click.
  second.popover.showPopover();
  assert.deepEqual(second.body.children, [second.detail]);
});
