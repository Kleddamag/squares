#!/usr/bin/env python3
"""The small shared kit of the published site: its name, its navigation, and page types.

The site's own pages (the overview, the frontier atlas and the tutorial) are rendered by
`devtools.render_overview`, which collects them from one module per part of the site; the
explainer is rendered by `devtools.render_explainer`. All of them carry the same
navigation bar, and the Visualizer, a full-viewport app, keeps its own `#site-note`
instead. This module is what they share, and it imports nothing heavier than the standard
library, so any renderer can use it without importing another renderer.

Every href the bar writes is relative to the page, so the site opens the same way from
Pages, from a local preview server, and from an artifact host. `base` is the path from the
page back to the site root: empty for a page at the root, `../` for one a directory down.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import NamedTuple

TEMPLATES = Path(__file__).with_name("templates")
NAV_TEMPLATE = TEMPLATES / "site-nav.html"

#: The site's name on every page. The project on GitHub keeps its own name, the Squares
#: Project; the site is named for its subject.
SITE_NAME = "Square Packing"
REPO_URL = "https://github.com/jlevy/squares"
SITE_URL = "https://jlevy.github.io/squares/"


class NavItem(NamedTuple):
    """One item in the bar: the key a page marks itself current with, its label, its href."""

    key: str
    label: str
    href: str
    external: bool = False


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("overview", "Overview", "./"),
    NavItem("frontier", "Frontier", "frontier.html"),
    NavItem("explainer", "Explainer", "explainer.html"),
    NavItem("tutorial", "Tutorial", "tutorial.html"),
    NavItem("visualizer", "Visualizer", "workbench/"),
    NavItem("github", "GitHub", REPO_URL, external=True),
)

PAGE_KEYS = frozenset(item.key for item in NAV_ITEMS if not item.external)


@dataclass(frozen=True)
class Page:
    """One site page, as a part of the site hands it to `render_overview`.

    Exactly one of `markdown` and `html` is set. Markdown is rendered by kpress in trusted
    mode, placeholders already filled; HTML is used as it is. `scripts` are first-party
    classic scripts inlined after the page's math runtime, each a file the browser floor
    checks, never a string written from Python.
    """

    key: str
    path: str
    title: str
    description: str
    markdown: str | None = None
    html: str | None = None
    scripts: tuple[Path, ...] = ()
    prose_font: str = "serif"

    def __post_init__(self) -> None:
        if self.key not in PAGE_KEYS:
            raise ValueError(
                f"unknown site page {self.key!r}; expected one of {sorted(PAGE_KEYS)}"
            )
        if (self.markdown is None) == (self.html is None):
            raise ValueError(f"page {self.path}: set exactly one of markdown and html")
        if self.path.startswith("/") or ".." in Path(self.path).parts:
            raise ValueError(f"page path {self.path!r} must be relative to the site root")


@dataclass(frozen=True)
class Asset:
    """A file the site serves beside its pages, at `path` relative to the site root."""

    path: str
    content: bytes

    def __post_init__(self) -> None:
        if self.path.startswith("/") or ".." in Path(self.path).parts:
            raise ValueError(f"asset path {self.path!r} must be relative to the site root")


def base_for(path: str) -> str:
    """The relative path from a file at `path` back to the site root."""
    return "../" * (len(Path(path).parts) - 1)


def _href(item: NavItem, base: str) -> str:
    if item.external:
        return item.href
    if item.href == "./":
        return base or "./"
    return base + item.href


def nav_html(current: str, *, base: str = "") -> str:
    """The bar for the page whose key is `current`, with hrefs relative to that page."""
    if current not in PAGE_KEYS:
        raise ValueError(f"unknown site page {current!r}; expected one of {sorted(PAGE_KEYS)}")
    items = []
    for item in NAV_ITEMS:
        attributes = [f'href="{escape(_href(item, base))}"']
        if item.key == current:
            attributes.append('aria-current="page"')
        if item.external:
            attributes.append('rel="noopener"')
        items.append(
            f'<li class="site-nav-item site-nav-{item.key}">'
            f"<a {' '.join(attributes)}>{escape(item.label)}</a></li>"
        )
    template = NAV_TEMPLATE.read_text(encoding="utf-8")
    return (
        template.replace("{{NAV_HOME}}", escape(base or "./"))
        .replace("{{SITE_NAME}}", escape(SITE_NAME))
        .replace("{{NAV_ITEMS}}", "\n".join(items))
        .strip()
    )
