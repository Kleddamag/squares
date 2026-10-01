"""The reader documents as site pages, with every link made to work off GitHub.

The tutorial is a page in the navigation; the README, the synopsis, the result and
frontier registers and the reference documents are pages the navigation does not list,
reached from the overview's cards, whose popovers frame them. Each is written to be
read on GitHub, where a relative link to `conventions.md` or to a directory under
`packing/` opens that file. Served as pages, the same links would point at pages that
do not exist, so each one is rewritten in the rendered HTML, never in the Markdown,
where a pattern would also match `](` inside a code span:

- a link to another rendered document becomes its page, anchor kept;
- any other relative link becomes the file's link on `main`, `blob/` for a file and
  `tree/` for a directory, and an image becomes its raw file on `main`, all through
  `repo_links`, the one place the site's repository links are made.

A relative link is resolved against the document's own directory, as GitHub resolves
it. Every rewritten repository target is checked against the tree being rendered, which
is the tree `main` holds when the site deploys, read once from git, and every anchor
into a page against the ids the target page actually has. A target that does not
resolve fails the render with the whole list, so a broken link is found when the page is
built rather than by a reader.

One document is also read in part. README's introduction, the block between its
`project-intro` markers, is the overview's first section: the overview's template holds a
placeholder where the prose would be, `overview_intro` fills it with the block, and
`rewrite_overview_intro` makes the block's links work on the site, as a document's are
made to. The project is introduced in one text, on GitHub and on the site.
"""

from __future__ import annotations

import html
import posixpath
import re
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from urllib.parse import quote, unquote

from devtools import render_overview, repo_links
from devtools.render_overview import REPO, Page
from devtools.repo_links import RepositoryTree, repo_url, repository_tree

TUTORIAL = REPO / repo_links.TUTORIAL
README = REPO / repo_links.README

#: The block of README that is also the overview's first section. It is hand-written in
#: README, between these two lines, and read from there; nothing writes it.
INTRO_BEGIN = "<!-- BEGIN SHARED: project-intro (devtools.site_documents) -->"
INTRO_END = "<!-- END SHARED: project-intro -->"
#: The same block in the overview, as Markdown and then as rendered HTML: kpress passes a
#: comment through, so these two mark the run whose links `rewrite_overview_intro`
#: rewrites, and nothing else on the overview is touched.
OVERVIEW_INTRO_OPEN = "<!-- README project-intro -->"
OVERVIEW_INTRO_CLOSE = "<!-- /README project-intro -->"


@dataclass(frozen=True)
class SiteDocument:
    """One reader document served as a page."""

    source: Path
    name: str
    current: str
    title: str
    description: str


def _document(path: str, name: str, title: str, description: str) -> SiteDocument:
    """A repository document served as a page that the navigation does not list: it is
    reached from its card's popover, which frames it, and from links in the others."""
    return SiteDocument(REPO / path, name, "github", f"{title} · Square Packing", description)


DOCUMENTS: tuple[SiteDocument, ...] = (
    SiteDocument(
        TUTORIAL,
        "tutorial.html",
        "tutorial",
        "Tutorial · Square Packing",
        "A guided walk through square packing: the problem, the bounds and how each "
        "result here is checked.",
    ),
    _document(
        repo_links.README,
        "readme.html",
        "The Squares Project",
        "What the project is, how it works, and where to start.",
    ),
    _document(
        repo_links.SYNOPSIS,
        "synopsis.html",
        "Synopsis",
        "The full research record: methods, claims and status.",
    ),
    _document(
        repo_links.RESULTS,
        "results.html",
        "Results",
        "Every registered result with its rungs.",
    ),
    _document(
        repo_links.STATUS,
        "status.html",
        "The Frontier",
        "Every case to 324, with provenance.",
    ),
    _document(
        repo_links.EPISTEMICS,
        "epistemics.html",
        "Epistemics",
        "How each result is verified, confirmed and scored.",
    ),
    _document(
        repo_links.CONVENTIONS,
        "conventions.html",
        "Conventions",
        "Record formats, identifiers and naming.",
    ),
    _document(
        repo_links.DEVELOPMENT,
        "development.html",
        "Development",
        "Building, testing and validating the code.",
    ),
    _document(
        repo_links.DEFECTS,
        "defects.html",
        "Defect Log",
        "Every defect found in the toolchain, one line each.",
    ),
)

#: The rendered documents by repository path, which is how the Markdown links them.
_BY_SOURCE = {doc.source.relative_to(REPO).as_posix(): doc for doc in DOCUMENTS}

_ARTICLE = re.compile(r"<article\b.*?</article>", re.DOTALL)
_TAG = re.compile(r"<(?!/)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
_LINK_ATTR = re.compile(r'\s(href|src)="([^"]*)"')
_ID_ATTR = re.compile(r'\s(?:id|name)="([^"]*)"')
_EXTERNAL = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")
# A document's own contents list, written for GitHub, which draws no contents rail: a
# `## Contents` heading over nothing but a list of links to the document's headings.
_MANUAL_CONTENTS = re.compile(
    r"^## Contents\n\n(?:[ \t]*(?:\d+\.|[-*])[ \t]+\[[^\]]+\]\(#[^)]+\)[ \t]*\n)+\n?",
    re.MULTILINE,
)


def without_manual_contents(markdown: str) -> str:
    """The document without its hand-written contents list. On the site the contents
    rail lists the headings, and the list would repeat as the rail's first entry."""
    return _MANUAL_CONTENTS.sub("", markdown, count=1)


@dataclass
class LinkReport:
    """What the rewrite found: targets missing from the tree and anchors with no id."""

    missing: list[str] = field(default_factory=list)
    #: (target page, anchor, as written): checked once every page is rendered.
    anchors: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkContext:
    """What a rewrite needs: the page's own name, the tree its links must exist in, and
    where the document sits."""

    page: str
    tree: RepositoryTree
    #: The document's directory in the repository, `""` at the root: what its relative
    #: links are relative to.
    base: str = ""
    #: Served pages a link may already name, such as `frontier.html#n-11` in a page
    #: built from the record rather than from a document: kept as written.
    served: frozenset[str] = frozenset()
    #: Repository files the page itself serves, and where: a case file linked from a
    #: case record is that case's record on the same page.
    aliases: dict[str, str] = field(default_factory=dict)


def _repository_link(path: str, fragment: str, *, tag: str, context: LinkContext) -> str | None:
    """A file's or directory's link on `main`; `None` if the tree has neither."""
    if path in context.tree.files:
        if tag == "img":
            return repo_url(path, kind="raw")
        return repo_url(path, fragment, kind="blob")
    if path in context.tree.directories:
        return repo_url(path, fragment, kind="tree")
    for root, (url, commit) in context.tree.submodules.items():
        if path.startswith(root + "/"):
            # Inside a submodule: its own repository at the commit this one pins, since a
            # vendored file is only known to exist at the pin. That is another
            # repository's permalink, not one of this repository's.
            inner = quote(path.removeprefix(root + "/"), safe="/")
            return f"{url}/blob/{commit}/{inner}{fragment}"
    return None


def rewrite_link(url: str, *, tag: str, context: LinkContext, report: LinkReport) -> str:
    """The served URL for one `href` or `src` found in a rendered reader document.

    A relative link is relative to the document's own directory, as GitHub reads it.
    """
    target, _, anchor = url.partition("#")
    if not url or url.startswith("#") or _EXTERNAL.match(url) or target in context.served:
        return url
    target, _, query = target.partition("?")
    relative = unquote(target) if target else "."
    path = posixpath.normpath(posixpath.join(context.base, relative))
    path = "" if path == "." else path
    fragment = f"#{anchor}" if anchor else ""
    document = _BY_SOURCE.get(path)
    if path in context.aliases:
        link = context.aliases[path]
    elif document is not None:
        if anchor:
            report.anchors.append((document.name, unquote(anchor), url))
        if document.name == context.page:
            return fragment or document.name
        link = document.name + fragment
    else:
        link = (
            None
            if path.startswith("../") or path == ".."
            # A query is GitHub's (`?plain=1` before a `#L12` line anchor), so it is kept.
            else _repository_link(
                path, (f"?{query}" if query else "") + fragment, tag=tag, context=context
            )
        )
    if link is None:
        report.missing.append(url)
        return url
    return link


def rewrite_links(markup: str, *, context: LinkContext, report: LinkReport) -> str:
    """Rewrite every `href` and `src` in a run of rendered HTML."""

    def attribute(match: re.Match[str], tag: str) -> str:
        url = html.unescape(match.group(2))
        new = rewrite_link(url, tag=tag, context=context, report=report)
        if new == url:
            return match.group(0)
        return f' {match.group(1)}="{html.escape(new, quote=True)}"'

    def element(match: re.Match[str]) -> str:
        tag = match.group(1).lower()
        return _LINK_ATTR.sub(lambda m: attribute(m, tag), match.group(0))

    return _TAG.sub(element, markup)


def rewrite_article(page: str, *, context: LinkContext, report: LinkReport) -> str:
    """Rewrite the links inside the page's article, leaving the nav and scripts alone."""
    article = _ARTICLE.search(page)
    if article is None:
        raise SystemExit(f"{context.page}: the rendered page has no <article>")
    body = rewrite_links(article.group(0), context=context, report=report)
    return page[: article.start()] + body + page[article.end() :]


def element_ids(page: str) -> frozenset[str]:
    """Every `id` and `name` in the page's article: the anchors a link can land on."""
    article = _ARTICLE.search(page)
    return frozenset(
        html.unescape(m) for m in _ID_ATTR.findall(article.group(0) if article else "")
    )


def render_document(
    document: SiteDocument, *, tree: RepositoryTree, report: LinkReport
) -> Page:
    """One reader document as a kpress page with its links rewritten."""
    base = posixpath.dirname(document.source.relative_to(REPO).as_posix())
    context = LinkContext(document.name, tree, base)
    return render_overview.kpress_page(
        without_manual_contents(document.source.read_text(encoding="utf-8")),
        name=document.name,
        current=document.current,
        title=document.title,
        description=document.description,
        # A long report gets the contents rail and a short one does not, by kpress's
        # own length rule, so every report keeps one layout either way.
        toc="auto",
        trust_mode="sanitized",
        strict_anchors=True,
        rewrite_body=lambda page: rewrite_article(page, context=context, report=report),
    )


def unresolved(pages: dict[str, Page], report: LinkReport) -> list[str]:
    """Every link the render could not resolve, missing files and anchors together."""
    ids = {name: element_ids(page.html) for name, page in pages.items()}
    problems = [f"no such path in the tree: {url}" for url in report.missing]
    problems += [
        f"no heading #{anchor} in {name}: {url}"
        for name, anchor, url in report.anchors
        if anchor not in ids[name]
    ]
    return sorted(set(problems))


def intro_block(readme: str) -> str:
    """README's introduction: the Markdown between its `project-intro` markers.

    Raises `ValueError` unless each marker appears once, in order, around prose alone. A
    heading or a comment inside the block would land in the middle of the overview's
    first section, and a link to the site would point the overview at itself.
    """
    if readme.count(INTRO_BEGIN) != 1 or readme.count(INTRO_END) != 1:
        raise ValueError("the project-intro markers must each appear exactly once")
    begin, end = readme.index(INTRO_BEGIN), readme.index(INTRO_END)
    if end < begin:
        raise ValueError("the project-intro block ends before it begins")
    block = readme[begin + len(INTRO_BEGIN) : end].strip()
    if not block:
        raise ValueError("the project-intro block is empty")
    if "<!--" in block or re.search(r"^#", block, re.MULTILINE):
        raise ValueError("the project-intro block holds a heading or a comment")
    if render_overview.SITE_URL in block:
        raise ValueError("the project-intro block links the site it is rendered on")
    return block


def overview_intro() -> str:
    """README's introduction as the overview's Markdown, between the two comments
    `rewrite_overview_intro` finds it by once the page is rendered."""
    try:
        block = intro_block(README.read_text(encoding="utf-8"))
    except ValueError as error:
        raise SystemExit(f"{repo_links.README}: {error}") from None
    return f"{OVERVIEW_INTRO_OPEN}\n\n{block}\n\n{OVERVIEW_INTRO_CLOSE}"


_CASE_FILE = re.compile(r"packing/frontier/n-(\d{3})\.md")
_RESULT_LINK = re.compile(r'<a href="([^"]*)">(T-\d{3})</a>')


def _result_rows(markup: str) -> str:
    """A link to the results register whose text is a result's id, as README writes
    `[T-060](packing/frontier/RESULTS.md)`, goes to that result's row in the table."""

    def row(match: re.Match[str]) -> str:
        if html.unescape(match.group(1)) != repo_links.RESULTS:
            return match.group(0)
        result = match.group(2)
        return f'<a href="{render_overview.RESULTS_PAGE}#{result.lower()}">{result}</a>'

    return _RESULT_LINK.sub(row, markup)


def rewrite_overview_intro(page: str) -> str:
    """The rendered overview with the links of README's introduction made to work there.

    The block is written for GitHub, so its links are repository paths. Each becomes the
    site's own page for what it names where the site has one: a result's row in the
    results table, the results table for the register, the frontier atlas for the status
    table, a case's record for its case file, and a reader document's page. Any other
    path becomes its link on `main`, checked against the tree, as on a document's page.
    Nothing outside the block is rewritten.
    """
    if page.count(OVERVIEW_INTRO_OPEN) != 1 or page.count(OVERVIEW_INTRO_CLOSE) != 1:
        raise SystemExit("index.html: README's introduction is not marked in the page")
    head, _, rest = page.partition(OVERVIEW_INTRO_OPEN)
    body, _, tail = rest.partition(OVERVIEW_INTRO_CLOSE)
    tree = repository_tree()
    cases = {
        path: f"cases.html#n-{int(match.group(1))}"
        for path in tree.files
        if (match := _CASE_FILE.fullmatch(path))
    }
    context = LinkContext(
        "index.html",
        tree,
        served=frozenset(render_overview.SITE_PAGES),
        aliases={
            repo_links.RESULTS: render_overview.RESULTS_PAGE,
            repo_links.STATUS: "frontier.html",
            **cases,
        },
    )
    report = LinkReport()
    body = rewrite_links(_result_rows(body), context=context, report=report)
    # An anchor into a reader document is checked against that document's page, which
    # is rendered only when the block has such a link.
    problems = unresolved(site_documents() if report.anchors else {}, report)
    if problems:
        listing = "\n  ".join(problems)
        raise SystemExit(
            f"{len(problems)} unresolved links in README's introduction:\n  {listing}"
        )
    return head + OVERVIEW_INTRO_OPEN + body + OVERVIEW_INTRO_CLOSE + tail


@cache
def site_documents() -> dict[str, Page]:
    """Every reader document, rendered once and checked together."""
    tree = repository_tree()
    report = LinkReport()
    pages = {doc.name: render_document(doc, tree=tree, report=report) for doc in DOCUMENTS}
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


def document_page(name: str) -> Page:
    """One repository document as its page, by served name."""
    return site_documents()[name]
