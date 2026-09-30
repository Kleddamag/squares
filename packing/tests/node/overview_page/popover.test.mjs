// `overview/popover.js`: with JavaScript on, a plain click on a card whose link carries
// `data-popover` opens the square popover instead of navigating; a modified click, and a
// card without the attribute, still navigate. A result shows its card and the table row's
// record, a site page a same-origin frame, a GitHub document its build-time opening
// section; the expand button carries the link, and closing returns focus to the card.
import assert from "node:assert/strict";
import { test } from "node:test";
import { Element, event, HTMLIFrameElement, page, run } from "./dom.mjs";

const PAGE = `
<article class="site-card"><p class="site-card-meta"><span class="site-card-id">T-037</span></p>
<h3 class="site-card-title"><a class="site-card-link" href="#result-t-037" data-popover="result">s(11) &gt; 31/8</a></h3></article>
<article class="site-card"><h3 class="site-card-title"><a class="site-card-link" href="frontier.html" data-popover="page">Frontier atlas</a></h3></article>
<article class="site-card"><h3 class="site-card-title"><a class="site-card-link" href="https://github.com/jlevy/squares/blob/main/epistemics.md" data-popover="document">Epistemics</a></h3>
<p class="site-card-summary">How results are graded.</p><template class="site-card-preview"><p>The opening section.</p></template></article>
<article class="site-card"><h3 class="site-card-title"><a class="site-card-link" href="#results">Verification</a></h3></article>
<table><tbody><tr id="result-t-037"><td><details><summary>s(11)</summary><div class="site-details-body"><p>Claim.</p></div></details></td></tr></tbody></table>`;

const setUp = () => {
  const { document } = page(PAGE);
  run("devtools/overview/popover.js");
  /** @param {string} href */
  const link = (href) => {
    const found = document
      .querySelectorAll("a.site-card-link")
      .find((a) => a.getAttribute("href") === href);
    assert.ok(found, href);
    return found;
  };
  /** @param {Element} target @param {Partial<ReturnType<typeof event>>} [keys] */
  const click = (target, keys = {}) => {
    const clicked = Object.assign(event("click"), keys);
    target.dispatchEvent(clicked);
    return clicked;
  };
  const dialog = () => document.querySelector("dialog.site-popover");
  return { document, link, click, dialog };
};

await test("a result card opens its card and the table row's record, and does not navigate", () => {
  const { link, click, dialog, document } = setUp();
  const clicked = click(link("#result-t-037"));
  assert.equal(clicked.defaultPrevented, true);
  const shown = dialog();
  assert.ok(shown);
  assert.equal(shown.hasAttribute("open"), true);
  assert.equal(shown.getAttribute("data-kind"), "result");
  assert.equal(shown.querySelector(".site-popover-title")?.textContent, "T-037");
  const body = shown.querySelector(".site-popover-body");
  assert.ok(body?.querySelector(".site-details-body"), "the row's record is shown");
  assert.equal(body?.querySelector(".site-card-link"), null, "the copy is not a link");
  const expand = shown.querySelector("a.site-popover-expand");
  assert.equal(expand?.getAttribute("href"), "http://site.test/index.html#result-t-037");
  assert.equal(document.querySelectorAll("#result-t-037").length, 1, "no id is copied");
});

await test("a page card renders the page in a same-origin frame", () => {
  const { link, click, dialog } = setUp();
  click(link("frontier.html"));
  const frame = dialog()?.querySelector("iframe.site-popover-frame");
  assert.ok(frame instanceof HTMLIFrameElement);
  assert.equal(frame.src, "http://site.test/frontier.html");
  assert.equal(dialog()?.querySelector(".site-popover-expand span")?.textContent, "Open the page");
});

await test("a document card shows its summary and opening section, and opens GitHub", () => {
  const { link, click, dialog } = setUp();
  click(link("https://github.com/jlevy/squares/blob/main/epistemics.md"));
  const body = dialog()?.querySelector(".site-popover-body");
  assert.equal(body?.querySelector(".site-popover-prose p")?.textContent, "The opening section.");
  assert.equal(body?.querySelector(".site-card-summary")?.textContent, "How results are graded.");
  assert.equal(body?.querySelector("template"), null);
  assert.equal(
    dialog()?.querySelector("a.site-popover-expand")?.getAttribute("href"),
    "https://github.com/jlevy/squares/blob/main/epistemics.md",
  );
  assert.equal(
    dialog()?.querySelector("a.site-popover-expand use")?.getAttribute("href"),
    "#kpress-icon-external-link",
  );
});

await test("a modified click and a card without data-popover navigate as links", () => {
  const { link, click, dialog } = setUp();
  assert.equal(click(link("frontier.html"), { metaKey: true }).defaultPrevented, false);
  assert.equal(click(link("frontier.html"), { button: 1 }).defaultPrevented, false);
  assert.equal(click(link("#results")).defaultPrevented, false);
  assert.equal(dialog(), null);
});

await test("closing empties the popover and returns focus to the card's link", () => {
  const { link, click, dialog, document } = setUp();
  const opener = link("frontier.html");
  click(opener);
  const close = dialog()?.querySelector("button.site-popover-close");
  assert.ok(close instanceof Element);
  close.click();
  assert.equal(dialog()?.hasAttribute("open"), false);
  assert.equal(dialog()?.querySelector(".site-popover-body")?.childNodes.length, 0);
  assert.equal(document.activeElement, opener);
});
