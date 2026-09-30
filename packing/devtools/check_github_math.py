#!/usr/bin/env python3
"""Check that GitHub renders every math span of a pushed Markdown file as mathematics.

`devtools.migrate_math` proves each rewrite against kpress's parser, the pinned KaTeX and
the pinned flowmark, which is what the site and the formatter need. GitHub is the third
reader of the same file and the one most readers meet first, and it parses math its own
way: a span it does not recognise is shown as literal dollars, and one it splits is shown
as two formulas and the text between them. Nothing local can answer for it, so this asks
GitHub itself.

For each file it fetches the file's page on github.com at a pushed ref, takes the rendered
Markdown GitHub embeds in it, and compares the TeX of every `<math-renderer>` element with
the math spans `devtools.check_math_spans` reads from the file at that ref. Every span has
to come back exactly once, with its TeX unchanged, and GitHub may render nothing the file
does not hold. The file is read with `git show REF:PATH`, so the comparison is between
the same bytes on both sides.

A file GitHub declines to render, as it does past a size, is reported and skipped: its
readers there see the source, formulas and all, whatever the markup.

It needs the network and a pushed ref, so it is a verification a migration runs after
pushing, not a gate. It exits 1 when any file disagrees. Pages are fetched with `curl`.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_github_math \\
        [--ref REF] PATH...

PATH is repository-relative (`README.md`, `docs/project/...`). REF defaults to the
checked-out commit, which has to be on GitHub already.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from devtools.check_math_spans import math_spans

REPO = Path(__file__).resolve().parents[2]
#: The repository on GitHub whose rendering is asked for.
GITHUB_REPOSITORY = "jlevy/squares"
#: Where a blob's page carries its rendered Markdown: the page's embedded data island.
_EMBEDDED = re.compile(
    r'<script type="application/json" data-target="react-app\.embeddedData">(.*?)</script>',
    re.DOTALL,
)
#: One formula as GitHub renders it: the TeX, dollars included, inside the element.
_RENDERED = re.compile(r"<math-renderer\b[^>]*>(.*?)</math-renderer>", re.DOTALL)
#: The delimiters GitHub leaves around the TeX inside the element, inline and display.
_DELIMITED = re.compile(
    r"\A(?:\$\$(?P<display>.*)\$\$|\$`(?P<code>.*)`\$|\$(?P<inline>.*)\$)\Z", re.DOTALL
)
TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class Comparison:
    """One file's math spans against GitHub's rendering of them."""

    path: str
    expected: int
    rendered: int
    missing: tuple[str, ...]
    extra: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.missing and not self.extra


class ShownAsSourceError(Exception):
    """GitHub does not render this file at all, so it shows no formula either way."""


def rendered_html(page: str) -> str:
    """The rendered Markdown a github.com blob page embeds.

    `ShownAsSourceError` when GitHub declines to render the file -- it does past a size it does
    not publish, and `SYNOPSIS.md` is past it -- and `ValueError` when the page is not
    one this reads, which means GitHub's page layout has changed.
    """
    island = _EMBEDDED.search(page)
    if island is None:
        raise ValueError("the page embeds no data island; GitHub's page layout has changed")
    blob = json.loads(island.group(1)).get("payload", {}).get("codeViewBlobRoute", {})
    rich = blob.get("richText")
    if isinstance(rich, str):
        return rich
    if blob.get("richTextTruncated"):
        raise ShownAsSourceError
    raise ValueError("the page carries no rendered Markdown; is the file Markdown?")


def rendered_math(rich: str) -> list[str]:
    """The TeX of every formula GitHub rendered, delimiters removed, in page order."""
    out = []
    for element in _RENDERED.finditer(rich):
        # GitHub escapes the TeX twice: once as the element's text, and once more inside it.
        text = html.unescape(html.unescape(element.group(1))).strip()
        delimited = _DELIMITED.match(text)
        if delimited is None:
            out.append(text)
            continue
        out.append(next(group for group in delimited.groups() if group is not None))
    return out


def compare(path: str, source: str, rich: str) -> Comparison:
    """Every span of `source` against the formulas in `rich`, as multisets of TeX."""
    expected = Counter(span.strip() for span in math_spans(source))
    rendered = Counter(span.strip() for span in rendered_math(rich))
    return Comparison(
        path=path,
        expected=sum(expected.values()),
        rendered=sum(rendered.values()),
        missing=tuple(sorted((expected - rendered).elements())),
        extra=tuple(sorted((rendered - expected).elements())),
    )


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=REPO, check=True, capture_output=True, text=True
    ).stdout


def fetch(url: str) -> str:
    """The page at `url`, by `curl`, which honours the machine's proxy and CA settings
    the way the shell does; a sandbox proxy's CA fails Python's strict X.509 check."""
    return subprocess.run(
        ("curl", "--fail", "--silent", "--show-error", "--location", "--max-time",
         str(TIMEOUT_SECONDS), url),
        check=True, capture_output=True, text=True,
    ).stdout  # fmt: skip


def check(path: str, ref: str) -> Comparison:
    source = _git("show", f"{ref}:{path}")
    page = fetch(f"https://github.com/{GITHUB_REPOSITORY}/blob/{ref}/{path}")
    return compare(path, source, rendered_html(page))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("paths", nargs="+", help="repository-relative Markdown files")
    parser.add_argument("--ref", help="a pushed commit, branch or tag (default: HEAD's commit)")
    args = parser.parse_args(argv)
    ref = args.ref or _git("rev-parse", "HEAD").strip()

    failed = 0
    for path in args.paths:
        try:
            result = check(path, ref)
        except ShownAsSourceError:
            print(f"skip {path}: GitHub shows it as source, too large to render")
            continue
        except (ValueError, OSError, subprocess.CalledProcessError) as error:
            print(f"FAIL {path}: {error}", file=sys.stderr)
            failed += 1
            continue
        print(
            f"{'ok  ' if result.ok else 'FAIL'} {path}: {result.expected} spans, "
            f"{result.rendered} rendered"
        )
        for span in result.missing:
            print(f"  not rendered as math: ${span}$", file=sys.stderr)
        for span in result.extra:
            print(f"  rendered, not in the file: ${span}$", file=sys.stderr)
        failed += not result.ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
