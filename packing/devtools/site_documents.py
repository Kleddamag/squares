"""The tutorial and the synopsis as site pages, with every link made to work off GitHub.

`TUTORIAL.md` and `SYNOPSIS.md` are written to be read on GitHub, where a relative link
to `conventions.md` or to a directory under `packing/` opens that file. Served as
`tutorial.html` and `synopsis.html`, the same links would point at pages that do not
exist, so each one is rewritten in the rendered HTML, never in the Markdown, where a
pattern would also match `](` inside a code span:

- `README.md` becomes the overview, `./`, with the anchor kept when the overview has a
  heading of that id and the repository's README named otherwise;
- `TUTORIAL.md#…` and `SYNOPSIS.md#…` become `tutorial.html#…` and `synopsis.html#…`;
- any other relative link becomes a permalink at the build commit, `blob/` for a file
  and `tree/` for a directory, and an image becomes its raw-file permalink.

Every rewritten repository target is checked against the build commit's tree, read
once with `git ls-tree`, and every anchor into the two pages against the ids the target
page actually has. A target that does not resolve fails the render with the whole list,
so a broken link is found when the page is built rather than by a reader.

The build commit is `render_explainer.link_revision()`, the same commit the explainer's
repository links name.
"""

from __future__ import annotations

import html
import posixpath
import re
import subprocess
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from urllib.parse import quote, unquote

from devtools import render_overview
from devtools.render_overview import REPO, REPO_URL, Page

TUTORIAL = REPO / "TUTORIAL.md"
SYNOPSIS = REPO / "SYNOPSIS.md"

RAW_URL = "https://raw.githubusercontent.com/jlevy/squares"


@dataclass(frozen=True)
class SiteDocument:
    """One reader document served as a page."""

    source: Path
    name: str
    current: str
    title: str
    description: str


DOCUMENTS: tuple[SiteDocument, ...] = (
    SiteDocument(
        TUTORIAL,
        "tutorial.html",
        "tutorial",
        "Tutorial · The Squares Project",
        "A guided walk through square packing: the problem, the bounds and how each "
        "result here is checked.",
    ),
    SiteDocument(
        SYNOPSIS,
        "synopsis.html",
        "synopsis",
        "Synopsis · The Squares Project",
        "The project's synopsis: every method, claim, tool and record, with links into "
        "the repository.",
    ),
)

#: The rendered documents by repository path, which is how the Markdown links them.
_BY_SOURCE = {doc.source.relative_to(REPO).as_posix(): doc for doc in DOCUMENTS}

_ARTICLE = re.compile(r"<article\b.*?</article>", re.DOTALL)
_TAG = re.compile(r"<(?!/)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
_LINK_ATTR = re.compile(r'\s(href|src)="([^"]*)"')
_ID_ATTR = re.compile(r'\s(?:id|name)="([^"]*)"')
_EXTERNAL = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")


@dataclass(frozen=True)
class RepositoryTree:
    """The build commit's tracked files and directories, the root as `""`."""

    files: frozenset[str]
    directories: frozenset[str]


def _ls_tree(revision: str, *flags: str) -> frozenset[str]:
    found = subprocess.run(
        ("git", "ls-tree", "-r", *flags, "--name-only", "-z", revision),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise SystemExit(f"git ls-tree {revision} failed: {found.stderr.strip()}")
    return frozenset(name for name in found.stdout.split("\0") if name)


@cache
def repository_tree(revision: str) -> RepositoryTree:
    """Every file and directory at `revision`, in two `git ls-tree` calls."""
    return RepositoryTree(_ls_tree(revision), _ls_tree(revision, "-d") | {""})


@dataclass
class LinkReport:
    """What the rewrite found: targets missing at the commit and anchors with no id."""

    missing: list[str] = field(default_factory=list)
    #: (target page, anchor, as written): checked once every page is rendered.
    anchors: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkContext:
    """What a rewrite needs: the page's own name, the commit, and the overview's ids."""

    page: str
    revision: str
    tree: RepositoryTree
    overview_ids: frozenset[str]


def _readme_link(anchor: str, context: LinkContext) -> str:
    """The overview for `README.md`, or the repository's README for an anchor only it has."""
    if not anchor:
        return "./"
    if unquote(anchor) in context.overview_ids:
        return f"./#{anchor}"
    return f"{REPO_URL}/blob/{context.revision}/README.md#{anchor}"


def _permalink(path: str, fragment: str, *, tag: str, context: LinkContext) -> str | None:
    """A file's or directory's permalink at the build commit; `None` if it has neither."""
    quoted = quote(path, safe="/")
    if path in context.tree.files:
        if tag == "img":
            return f"{RAW_URL}/{context.revision}/{quoted}"
        return f"{REPO_URL}/blob/{context.revision}/{quoted}{fragment}"
    if path in context.tree.directories:
        suffix = f"/{quoted}" if quoted else ""
        return f"{REPO_URL}/tree/{context.revision}{suffix}{fragment}"
    return None


def rewrite_link(url: str, *, tag: str, context: LinkContext, report: LinkReport) -> str:
    """The served URL for one `href` or `src` found in a rendered reader document.

    Both documents sit at the repository root, so a relative link is a repository path.
    """
    if not url or url.startswith("#") or _EXTERNAL.match(url):
        return url
    target, _, anchor = url.partition("#")
    path = posixpath.normpath(unquote(target.split("?", 1)[0])) if target else "."
    path = "" if path == "." else path
    fragment = f"#{anchor}" if anchor else ""
    if path == "README.md":
        return _readme_link(anchor, context)
    document = _BY_SOURCE.get(path)
    if document is not None:
        if anchor:
            report.anchors.append((document.name, unquote(anchor), url))
        if document.name == context.page:
            return fragment or document.name
        return document.name + fragment
    link = (
        None
        if path.startswith("../") or path == ".."
        else _permalink(path, fragment, tag=tag, context=context)
    )
    if link is None:
        report.missing.append(url)
        return url
    return link


def rewrite_article(page: str, *, context: LinkContext, report: LinkReport) -> str:
    """Rewrite the links inside the page's article, leaving the nav and scripts alone."""
    article = _ARTICLE.search(page)
    if article is None:
        raise SystemExit(f"{context.page}: the rendered page has no <article>")

    def attribute(match: re.Match[str], tag: str) -> str:
        url = html.unescape(match.group(2))
        new = rewrite_link(url, tag=tag, context=context, report=report)
        if new == url:
            return match.group(0)
        return f' {match.group(1)}="{html.escape(new, quote=True)}"'

    def element(match: re.Match[str]) -> str:
        tag = match.group(1).lower()
        return _LINK_ATTR.sub(lambda m: attribute(m, tag), match.group(0))

    body = _TAG.sub(element, article.group(0))
    return page[: article.start()] + body + page[article.end() :]


def element_ids(page: str) -> frozenset[str]:
    """Every `id` and `name` in the page's article: the anchors a link can land on."""
    article = _ARTICLE.search(page)
    return frozenset(
        html.unescape(m) for m in _ID_ATTR.findall(article.group(0) if article else "")
    )


@cache
def overview_ids() -> frozenset[str]:
    """The overview's heading ids, so a README anchor it also has stays on the site."""
    return element_ids(render_overview.PAGES["index.html"]().html)


def render_document(
    document: SiteDocument, *, revision: str, tree: RepositoryTree, report: LinkReport
) -> Page:
    """One reader document as a kpress page with its links rewritten."""
    context = LinkContext(document.name, revision, tree, overview_ids())
    return render_overview.kpress_page(
        document.source.read_text(encoding="utf-8"),
        name=document.name,
        current=document.current,
        title=document.title,
        description=document.description,
        toc=True,
        trust_mode="sanitized",
        strict_anchors=True,
        rewrite_body=lambda page: rewrite_article(page, context=context, report=report),
    )


def unresolved(pages: dict[str, Page], report: LinkReport) -> list[str]:
    """Every link the render could not resolve, missing files and anchors together."""
    ids = {name: element_ids(page.html) for name, page in pages.items()}
    problems = [f"no such path at the build commit: {url}" for url in report.missing]
    problems += [
        f"no heading #{anchor} in {name}: {url}"
        for name, anchor, url in report.anchors
        if anchor not in ids[name]
    ]
    return sorted(set(problems))


@cache
def site_documents() -> dict[str, Page]:
    """Both pages, rendered once and checked together, since each links into the other."""
    from devtools.render_explainer import link_revision  # noqa: PLC0415

    revision = link_revision()
    tree = repository_tree(revision)
    report = LinkReport()
    pages = {
        doc.name: render_document(doc, revision=revision, tree=tree, report=report)
        for doc in DOCUMENTS
    }
    problems = unresolved(pages, report)
    if problems:
        listing = "\n  ".join(problems)
        raise SystemExit(
            f"{len(problems)} unresolved links in the reader documents:\n  {listing}"
        )
    return pages


def tutorial_page() -> Page:
    """`TUTORIAL.md` as `tutorial.html`."""
    return site_documents()["tutorial.html"]


def synopsis_page() -> Page:
    """`SYNOPSIS.md` as `synopsis.html`."""
    return site_documents()["synopsis.html"]
