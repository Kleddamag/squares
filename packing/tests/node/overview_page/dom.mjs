// A small document for the site pages' scripts to run against in Node: enough of the DOM
// for `overview/table.js`, `forward.js`, `popover.js` and `site-math.js`, and no more.
// `page(html)` parses a fragment of the page's own markup into a document and installs it,
// with a `window` and the element classes the scripts test with `instanceof`, on
// `globalThis`; `run(path)` then runs one of the scripts in this realm, as the page's
// inlined `<script>` would.
//
// The parser reads the markup `overview_page` writes (elements, quoted attributes, text,
// the void elements, `<template>` content) and nothing more; the selector engine answers
// compound selectors of a tag, an id, classes and attributes (`[a]`, `[a="v"]`), joined by
// descendant and child combinators, in comma lists.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { runInThisContext } from "node:vm";

const PACKING = new URL("../../../", import.meta.url);
const VOID = new Set(["br", "img", "input", "meta", "link", "hr", "source", "wbr"]);

/** @typedef {{ type: string, target: Node | null, currentTarget: Node | null, defaultPrevented: boolean, button: number, metaKey: boolean, ctrlKey: boolean, shiftKey: boolean, altKey: boolean, preventDefault(): void }} DomEvent */
/** @typedef {{ fn: (event: DomEvent) => void, capture: boolean }} Listener */

export class Node {
  /** @param {Document | null} owner */
  constructor(owner) {
    /** @type {Document | null} */
    this.ownerDocument = owner;
    /** @type {Node | null} */
    this.parentNode = null;
    /** @type {Node[]} */
    this.childNodes = [];
    /** @type {Map<string, Listener[]>} */
    this.listeners = new Map();
  }

  /** @returns {Element | null} */
  get parentElement() {
    return this.parentNode instanceof Element ? this.parentNode : null;
  }

  get isConnected() {
    let at = /** @type {Node | null} */ (this);
    while (at?.parentNode) {
      at = at.parentNode;
    }
    return at instanceof Document;
  }

  /** @returns {string} */
  get textContent() {
    return this.childNodes.map((node) => /** @type {string} */ (node.textContent)).join("");
  }

  set textContent(value) {
    this.replaceChildren(new Text(this.ownerDocument, value));
  }

  /** @param {...(Node | string)} nodes */
  append(...nodes) {
    for (const item of nodes) {
      const node = typeof item === "string" ? new Text(this.ownerDocument, item) : item;
      if (node instanceof DocumentFragment) {
        this.append(...node.childNodes);
        continue;
      }
      node.remove();
      node.parentNode = this;
      this.childNodes.push(node);
    }
  }

  /** @param {...(Node | string)} nodes */
  replaceChildren(...nodes) {
    for (const child of [...this.childNodes]) {
      child.remove();
    }
    this.append(...nodes);
  }

  remove() {
    const parent = this.parentNode;
    if (parent) {
      parent.childNodes = parent.childNodes.filter((node) => node !== this);
      this.parentNode = null;
    }
  }

  /** @param {...Node} nodes */
  replaceWith(...nodes) {
    const parent = this.parentNode;
    if (!parent) {
      return;
    }
    const index = parent.childNodes.indexOf(this);
    this.remove();
    for (const node of nodes) {
      node.remove();
      node.parentNode = parent;
    }
    parent.childNodes.splice(index, 0, ...nodes);
  }

  /** @param {Node} node */
  contains(node) {
    for (let at = /** @type {Node | null} */ (node); at; at = at.parentNode) {
      if (at === this) {
        return true;
      }
    }
    return false;
  }

  /** @param {boolean} [deep] @returns {Node} */
  cloneNode(deep = false) {
    const copy = new Node(this.ownerDocument);
    if (deep) {
      copy.append(...this.childNodes.map((node) => node.cloneNode(true)));
    }
    return copy;
  }

  /**
   * @param {string} type
   * @param {(event: DomEvent) => void} fn
   * @param {boolean | { capture?: boolean }} [options]
   */
  addEventListener(type, fn, options = false) {
    const capture = typeof options === "boolean" ? options : Boolean(options.capture);
    const list = this.listeners.get(type) ?? [];
    list.push({ fn, capture });
    this.listeners.set(type, list);
  }

  /** @param {DomEvent} event @param {boolean} capture */
  fire(event, capture) {
    for (const listener of this.listeners.get(event.type) ?? []) {
      if (listener.capture === capture) {
        event.currentTarget = this;
        listener.fn(event);
      }
    }
  }

  /** @param {DomEvent} event */
  dispatchEvent(event) {
    event.target = this;
    /** @type {Node[]} */
    const path = [];
    for (let at = /** @type {Node | null} */ (this); at; at = at.parentNode) {
      path.push(at);
    }
    const win = this.ownerDocument?.defaultView;
    const top = win ? [win] : [];
    for (const node of [...top, ...[...path].reverse()]) {
      node.fire(event, true);
    }
    for (const node of [...path, ...top]) {
      node.fire(event, false);
    }
    return !event.defaultPrevented;
  }
}

export class Text extends Node {
  /** @param {Document | null} owner @param {string} data */
  constructor(owner, data) {
    super(owner);
    this.data = data;
  }

  /**
   * @override
   * @returns {string}
   */
  get textContent() {
    return this.data;
  }

  /** @override */
  set textContent(value) {
    this.data = value;
  }

  /**
   * @override
   * @returns {Node}
   */
  cloneNode() {
    return new Text(this.ownerDocument, this.data);
  }
}

export class DocumentFragment extends Node {
  /**
   * @override
   * @param {boolean} [deep]
   * @returns {Node}
   */
  cloneNode(deep = false) {
    const copy = new DocumentFragment(this.ownerDocument);
    if (deep) {
      copy.append(...this.childNodes.map((node) => node.cloneNode(true)));
    }
    return copy;
  }

  /** @param {string} selector */
  querySelectorAll(selector) {
    return select(this, selector);
  }
}

/** @param {string} key */
const kebab = (key) => key.replace(/[A-Z]/g, (letter) => `-${letter.toLowerCase()}`);

export class Element extends Node {
  /** @param {Document | null} owner @param {string} tag */
  constructor(owner, tag) {
    super(owner);
    this.localName = tag.toLowerCase();
    this.tagName = tag.toUpperCase();
    /** @type {Map<string, string>} */
    this.attributes = new Map();
    const attributes = this.attributes;
    /** @type {Record<string, string | undefined>} */
    this.dataset = new Proxy(/** @type {Record<string, string | undefined>} */ ({}), {
      get: (_, key) => attributes.get(`data-${kebab(String(key))}`),
      set: (_, key, value) => {
        attributes.set(`data-${kebab(String(key))}`, String(value));
        return true;
      },
      deleteProperty: (_, key) => {
        attributes.delete(`data-${kebab(String(key))}`);
        return true;
      },
      has: (_, key) => attributes.has(`data-${kebab(String(key))}`),
    });
  }

  /** @param {string} name */
  getAttribute(name) {
    return this.attributes.get(name) ?? null;
  }

  /** @param {string} name @param {string} value */
  setAttribute(name, value) {
    this.attributes.set(name, String(value));
  }

  /** @param {string} name */
  hasAttribute(name) {
    return this.attributes.has(name);
  }

  /** @param {string} name */
  removeAttribute(name) {
    this.attributes.delete(name);
  }

  get id() {
    return this.getAttribute("id") ?? "";
  }

  set id(value) {
    this.setAttribute("id", value);
  }

  get className() {
    return this.getAttribute("class") ?? "";
  }

  set className(value) {
    this.setAttribute("class", value);
  }

  get classList() {
    const classes = this.className.split(/\s+/).filter(Boolean);
    return {
      contains: (/** @type {string} */ name) => classes.includes(name),
      add: (/** @type {string} */ name) => {
        if (!classes.includes(name)) {
          this.className = [...classes, name].join(" ");
        }
      },
    };
  }

  focus() {
    if (this.ownerDocument) {
      this.ownerDocument.activeElement = this;
    }
  }

  get hidden() {
    return this.hasAttribute("hidden");
  }

  set hidden(value) {
    if (value) {
      this.setAttribute("hidden", "");
    } else {
      this.removeAttribute("hidden");
    }
  }

  get children() {
    return /** @type {Element[]} */ (this.childNodes.filter((node) => node instanceof Element));
  }

  /** @returns {Element | null} */
  get firstElementChild() {
    return this.children[0] ?? null;
  }

  /** @returns {Element | null} */
  get nextElementSibling() {
    const siblings = this.parentNode?.childNodes ?? [];
    for (const node of /** @type {Node[]} */ (siblings.slice(siblings.indexOf(this) + 1))) {
      if (node instanceof Element) {
        return node;
      }
    }
    return null;
  }

  /**
   * @override
   * @param {boolean} [deep]
   * @returns {Node}
   */
  cloneNode(deep = false) {
    const copy = this.ownerDocument
      ? this.ownerDocument.createElement(this.localName)
      : new Element(null, this.localName);
    for (const [name, value] of this.attributes) {
      copy.setAttribute(name, value);
    }
    if (deep) {
      copy.append(...this.childNodes.map((node) => node.cloneNode(true)));
      if (this instanceof HTMLTemplateElement && copy instanceof HTMLTemplateElement) {
        copy.content = /** @type {DocumentFragment} */ (this.content.cloneNode(true));
      }
    }
    return copy;
  }

  /** @param {string} selector */
  matches(selector) {
    return selector.split(",").some((part) => matchesChain(this, parseChain(part.trim())));
  }

  /** @param {string} selector */
  closest(selector) {
    for (let at = /** @type {Element | null} */ (this); at; at = at.parentElement) {
      if (at.matches(selector)) {
        return at;
      }
    }
    return null;
  }

  /** @param {string} selector */
  querySelectorAll(selector) {
    return select(this, selector);
  }

  /** @param {string} selector */
  querySelector(selector) {
    return this.querySelectorAll(selector)[0] ?? null;
  }

  click() {
    this.dispatchEvent(event("click"));
  }
}

export class HTMLAnchorElement extends Element {
  get href() {
    const base = this.ownerDocument?.defaultView?.location.href ?? "http://site.test/";
    return new URL(this.getAttribute("href") ?? "", base).href;
  }

  set href(value) {
    this.setAttribute("href", value);
  }

  get hash() {
    return new URL(this.href).hash;
  }
}

export class HTMLInputElement extends Element {
  /** @type {string} */
  value = "";
  checked = false;
}

export class HTMLSelectElement extends Element {
  /** @type {string} */
  value = "";
}

export class HTMLButtonElement extends Element {
  type = "submit";
}

export class HTMLIFrameElement extends Element {
  src = "";
  title = "";
}

export class HTMLDetailsElement extends Element {
  get open() {
    return this.hasAttribute("open");
  }

  set open(value) {
    if (value) {
      this.setAttribute("open", "");
    } else {
      this.removeAttribute("open");
    }
  }
}

export class HTMLDialogElement extends Element {
  get open() {
    return this.hasAttribute("open");
  }

  set open(value) {
    if (value) {
      this.setAttribute("open", "");
    } else {
      this.removeAttribute("open");
    }
  }

  showModal() {
    this.open = true;
  }

  close() {
    this.open = false;
    this.dispatchEvent(event("close"));
  }
}

export class HTMLTemplateElement extends Element {
  /** @param {Document | null} owner @param {string} tag */
  constructor(owner, tag) {
    super(owner, tag);
    this.content = new DocumentFragment(owner);
  }
}

const CLASSES = {
  a: HTMLAnchorElement,
  input: HTMLInputElement,
  select: HTMLSelectElement,
  button: HTMLButtonElement,
  iframe: HTMLIFrameElement,
  details: HTMLDetailsElement,
  dialog: HTMLDialogElement,
  template: HTMLTemplateElement,
};

export class Document extends Node {
  constructor() {
    super(null);
    this.ownerDocument = this;
    /** @type {{ location: { href: string, hash: string, search: string, replace(url: string): void, replaced: string | null }, fire(event: DomEvent, capture: boolean): void } | null} */
    this.defaultView = null;
    /** @type {Element | null} */
    this.activeElement = null;
    this.documentElement = this.createElement("html");
    this.body = this.createElement("body");
    this.documentElement.append(this.body);
    this.append(this.documentElement);
  }

  /** @param {string} tag @returns {Element} */
  createElement(tag) {
    const name = tag.toLowerCase();
    const Kind = CLASSES[/** @type {keyof typeof CLASSES} */ (name)] ?? Element;
    return new Kind(this, name);
  }

  /** @param {string} _namespace @param {string} tag */
  createElementNS(_namespace, tag) {
    return new Element(this, tag);
  }

  /** @param {string} id */
  getElementById(id) {
    return select(this, "*").find((element) => element.id === id) ?? null;
  }

  /** @param {string} selector */
  querySelectorAll(selector) {
    return select(this, selector);
  }

  /** @param {string} selector */
  querySelector(selector) {
    return this.querySelectorAll(selector)[0] ?? null;
  }
}

/** @param {string} type @returns {DomEvent} */
export function event(type) {
  return {
    type,
    target: null,
    currentTarget: null,
    defaultPrevented: false,
    button: 0,
    metaKey: false,
    ctrlKey: false,
    shiftKey: false,
    altKey: false,
    preventDefault() {
      this.defaultPrevented = true;
    },
  };
}

// ── Selectors ────────────────────────────────────────────────────────────────────────

/** @typedef {{ tag: string | null, id: string | null, classes: string[], attributes: [string, string | null][] }} Compound */
/** @typedef {{ compound: Compound, combinator: " " | ">" | null }[]} Chain */

/** @param {string} text @returns {Compound} */
function parseCompound(text) {
  /** @type {Compound} */
  const compound = { tag: null, id: null, classes: [], attributes: [] };
  const pattern = /([a-zA-Z][\w-]*|\*)|#([\w-]+)|\.([\w-]+)|\[([\w-]+)(?:="([^"]*)")?\]/g;
  for (const match of text.matchAll(pattern)) {
    if (match[1]) {
      compound.tag = match[1] === "*" ? null : match[1].toLowerCase();
    } else if (match[2]) {
      compound.id = match[2];
    } else if (match[3]) {
      compound.classes.push(match[3]);
    } else if (match[4]) {
      compound.attributes.push([match[4], match[5] ?? null]);
    }
  }
  return compound;
}

/** @param {string} text @returns {Chain} */
function parseChain(text) {
  const tokens = text
    .replace(/\s*>\s*/g, " > ")
    .trim()
    .split(/\s+/);
  /** @type {Chain} */
  const chain = [];
  /** @type {" " | ">" | null} */
  let combinator = null;
  for (const token of tokens) {
    if (token === ">") {
      combinator = ">";
      continue;
    }
    chain.push({ compound: parseCompound(token), combinator });
    combinator = " ";
  }
  return chain;
}

/** @param {Element} element @param {Compound} compound */
function matchesCompound(element, compound) {
  return (
    (compound.tag === null || element.localName === compound.tag) &&
    (compound.id === null || element.id === compound.id) &&
    compound.classes.every((name) => element.classList.contains(name)) &&
    compound.attributes.every(([name, value]) =>
      value === null ? element.hasAttribute(name) : element.getAttribute(name) === value,
    )
  );
}

/**
 * @param {Element} element
 * @param {Chain} chain
 * @returns {boolean}
 */
function matchesChain(element, chain) {
  const last = chain.at(-1);
  if (!last || !matchesCompound(element, last.compound)) {
    return false;
  }
  if (chain.length === 1) {
    return true;
  }
  const rest = chain.slice(0, -1);
  if (last.combinator === ">") {
    return element.parentElement !== null && matchesChain(element.parentElement, rest);
  }
  for (let at = element.parentElement; at; at = at.parentElement) {
    if (matchesChain(at, rest)) {
      return true;
    }
  }
  return false;
}

/** @param {Node} root @param {string} selector @returns {Element[]} */
function select(root, selector) {
  /** @type {Element[]} */
  const found = [];
  /** @param {Node} node */
  const walk = (node) => {
    for (const child of node.childNodes) {
      if (child instanceof Element) {
        if (child.matches(selector)) {
          found.push(child);
        }
        walk(child);
      }
    }
  };
  walk(root);
  return found;
}

// ── Parsing and running ──────────────────────────────────────────────────────────────

/** @param {string} text */
const decode = (text) =>
  text
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#8288;/g, "⁠")
    .replace(/&amp;/g, "&");

/** @param {Document} document @param {Node} into @param {string} html */
export function parseInto(document, into, html) {
  const pattern =
    /<!--[\s\S]*?-->|<\/([\w-]+)\s*>|<([\w-]+)((?:\s+[\w-]+(?:="[^"]*")?)*)\s*\/?>|([^<]+)/g;
  /** @type {Node[]} */
  const stack = [into];
  for (const match of html.matchAll(pattern)) {
    const top = /** @type {Node} */ (stack.at(-1));
    const [, closing, opening, attributes, text] = match;
    if (text !== undefined) {
      top.append(new Text(document, decode(text)));
    } else if (closing !== undefined) {
      while (stack.length > 1) {
        const node = stack.pop();
        if (node instanceof Element && node.localName === closing.toLowerCase()) {
          break;
        }
        if (node instanceof DocumentFragment) {
          stack.pop();
          break;
        }
      }
    } else if (opening !== undefined) {
      const element = document.createElement(opening);
      for (const attribute of (attributes ?? "").matchAll(/([\w-]+)(?:="([^"]*)")?/g)) {
        element.setAttribute(String(attribute[1]), decode(attribute[2] ?? ""));
      }
      top.append(element);
      if (element instanceof HTMLTemplateElement) {
        stack.push(element, element.content);
      } else if (!VOID.has(element.localName)) {
        stack.push(element);
      }
    }
  }
}

/**
 * A document holding `html` in its body, installed on `globalThis` with a window whose
 * location is `url`.
 * @param {string} html
 * @param {string} [url]
 */
export function page(html, url = "http://site.test/index.html") {
  const document = new Document();
  parseInto(document, document.body, html);
  const where = new URL(url);
  const window = {
    location: {
      href: where.href,
      hash: where.hash,
      search: where.search,
      /** @type {string | null} */
      replaced: null,
      /** @param {string} target */
      replace(target) {
        this.replaced = target;
      },
    },
    /** @type {Map<string, Listener[]>} */
    listeners: new Map(),
    /**
     * @param {string} type
     * @param {(event: DomEvent) => void} fn
     */
    addEventListener(type, fn) {
      const list = this.listeners.get(type) ?? [];
      list.push({ fn, capture: false });
      this.listeners.set(type, list);
    },
    /** @param {DomEvent} event @param {boolean} capture */
    fire(event, capture) {
      if (capture) {
        return;
      }
      for (const listener of this.listeners.get(event.type) ?? []) {
        listener.fn(event);
      }
    },
  };
  document.defaultView = window;
  Object.assign(globalThis, {
    document,
    window,
    Element,
    HTMLAnchorElement,
    HTMLDetailsElement,
    HTMLTemplateElement,
  });
  return { document, window };
}

/**
 * Run a script of the site pages, at `packing/<path>`, in this realm.
 * @param {string} path
 */
export function run(path) {
  const file = fileURLToPath(new URL(path, PACKING));
  runInThisContext(readFileSync(file, "utf8"), { filename: file });
}
