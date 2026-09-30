#!/usr/bin/env python3
"""The site's own copies of its media, and the check that Pages serves each as what it is.

A release download is served as an `application/octet-stream` attachment and a
`github.com/…/blob/…` URL as GitHub's HTML viewer, so a link to either downloads the file
or opens a page about it. The site serves its media itself, and three things hold that:

- **`--fetch SITE --cache DIR`** copies the ascent films pinned in
  `sqpack.release.PUBLISHED_FILMS` from their release into `SITE/films/`, streaming each
  and checking its byte count and SHA-256 against the pin; any mismatch fails. The Pages
  workflow's `publish` job runs it on `main` only. `--cache` names a directory of copies
  already verified, reused when their size and hash still match, so a deploy downloads
  the films again only when the pin changes. `--cache-key` prints the key that directory
  is cached under, derived from the films' names and hashes alone, so re-pinning
  `DATA_REVISION` in the same file never invalidates it.
- **`--check-media SITE_URL [PATH ...]`** asks the deployed site for one byte of each
  media file and requires status 200 or 206, the exact media type for its extension, no
  `attachment` disposition, `accept-ranges: bytes` for a film, and a total length equal
  to the pinned byte count for a film. The decision (`media_problems`) is a pure function
  of the status and headers, apart from the request that obtains them.
- **`foreign_media(html)`** names every media link on a page that is not site-relative:
  a release download, a `raw.githubusercontent.com` file, a `/blob/` page, or any other
  absolute or root-relative URL to a PDF, MP4 or PNG. The overview's render test holds it
  empty.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.published_media --cache-key
    uv run --frozen --all-extras --group dev python -m devtools.published_media \
        --fetch site --cache ~/.cache/squares-films
    uv run --frozen --all-extras --group dev python -m devtools.published_media \
        --check-media https://jlevy.github.io/squares/
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import shutil
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import BinaryIO
from urllib.parse import urljoin, urlsplit

from devtools.site_kit import REPO_URL
from sqpack.release import PUBLISHED_FILMS, PublishedFilm

#: Where on the site the films are served, relative to its root.
FILMS_DIR = "films"

#: The media types Pages must serve, by extension. `image/svg+xml` is here so a check can
#: include the explainer's figure and the frontier thumbnails; the same-origin rule is
#: about the three heavy kinds a reader opens directly.
EXPECTED_TYPES: Mapping[str, str] = {
    ".pdf": "application/pdf",
    ".mp4": "video/mp4",
    ".png": "image/png",
    ".svg": "image/svg+xml",
}
#: What `foreign_media` holds to the site: files a reader opens or plays by following a
#: link, which a host serving the wrong type turns into a download or a viewer page.
SAME_ORIGIN_SUFFIXES = frozenset({".pdf", ".mp4", ".png"})

#: The media the overview and the explainer link, relative to the site root: the atlas
#: PDFs and their previews, both films and both posters. `--check-media` checks these
#: when it is given no paths.
SITE_MEDIA: tuple[str, ...] = (
    "known-best-1-100.pdf",
    "known-best-1-324.pdf",
    "known-best-1-100-preview.png",
    "known-best-1-324-preview.png",
    "ascent-n1-100-poster.png",
    "ascent-n1-324-poster.png",
    *(f"{FILMS_DIR}/{film.name}" for film in PUBLISHED_FILMS),
)

USER_AGENT = "squares-published-media/1"
CHUNK = 1 << 20
#: Pages can answer 404 or 5xx for a short while after a deploy reports success, as
#: `check_published_site` found; thirty seconds in all, the same schedule it uses.
RETRY_DELAYS = (2.0, 4.0, 8.0, 16.0)
TRANSIENT_STATUSES = frozenset({0, 404, 408, 429, 500, 502, 503, 504})
#: A film download interrupted in transit is started again after each of these pauses; a
#: complete download that does not match the pin is never retried.
DOWNLOAD_RETRY_DELAYS = (5.0, 20.0)


# --- The pin ------------------------------------------------------------------------


def release_url(film: PublishedFilm) -> str:
    """The film's release download, which serves it as an attachment."""
    return f"{REPO_URL}/releases/download/{film.tag}/{film.name}"


def release_page(tag: str) -> str:
    """The release's page, the archive of record with its receipts."""
    return f"{REPO_URL}/releases/tag/{tag}"


def site_path(film: PublishedFilm) -> str:
    """Where the site serves the film, relative to its root."""
    return f"{FILMS_DIR}/{film.name}"


def cache_key(films: Iterable[PublishedFilm] = PUBLISHED_FILMS) -> str:
    """A cache key that changes exactly when a pinned film's name or hash does.

    `films-` and sixteen hex characters of a SHA-256 over the sorted `name sha256` lines,
    so neither the order of the pin nor anything else in `sqpack.release` moves it.
    """
    lines = sorted(f"{film.name} {film.sha256}\n" for film in films)
    return "films-" + hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()[:16]


def file_digest(path: Path) -> tuple[int, str]:
    """The byte count and SHA-256 of a file, read in chunks."""
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
            size += len(block)
    return size, digest.hexdigest()


def pin_problems(film: PublishedFilm, size: int, sha256: str) -> list[str]:
    """How a file of `size` bytes and hash `sha256` differs from the film's pin."""
    problems = []
    if size != film.byte_count:
        problems.append(f"{film.name}: {size:,} bytes, pinned {film.byte_count:,}")
    if sha256 != film.sha256:
        problems.append(f"{film.name}: SHA-256 {sha256}, pinned {film.sha256}")
    return problems


def matches_pin(path: Path, film: PublishedFilm) -> bool:
    """Whether `path` is the pinned film, checked by size first and then by hash."""
    if not path.is_file() or path.stat().st_size != film.byte_count:
        return False
    return not pin_problems(film, *file_digest(path))


# --- Fetching the films -------------------------------------------------------------

#: Opens a URL for reading; the default is an HTTPS GET that follows GitHub's redirect to
#: its asset store. Tests pass one that returns bytes from memory.
Opener = Callable[[str], AbstractContextManager[BinaryIO]]


def open_release(url: str) -> AbstractContextManager[BinaryIO]:
    if not url.startswith("https://"):
        raise ValueError(f"refusing to fetch a non-https URL: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(request, timeout=60.0)


def download(url: str, destination: Path, *, opener: Opener = open_release) -> tuple[int, str]:
    """Stream `url` into `destination`, returning the byte count and SHA-256 written."""
    digest = hashlib.sha256()
    size = 0
    with opener(url) as response, destination.open("wb") as handle:
        for block in iter(lambda: response.read(CHUNK), b""):
            handle.write(block)
            digest.update(block)
            size += len(block)
    return size, digest.hexdigest()


def _download_whole(
    film: PublishedFilm,
    partial: Path,
    *,
    opener: Opener,
    delays: Sequence[float],
    sleep: Callable[[float], object],
    log: Callable[[str], object],
) -> tuple[int, str]:
    """Download the film to `partial`, again after a transport error or a short read.

    A complete download is returned whatever its hash, for the caller to refuse: a file
    of the pinned length that does not match is not a network fault, so it is not retried.
    """
    for attempt, delay in enumerate((*delays, None), start=1):
        try:
            size, sha256 = download(release_url(film), partial, opener=opener)
        except (OSError, http.client.HTTPException) as error:
            partial.unlink(missing_ok=True)
            if delay is None:
                raise SystemExit(f"{film.name}: download failed: {error}") from error
            log(f"{film.name}: attempt {attempt} failed ({error}); again in {delay:g} s")
        else:
            if size >= film.byte_count or delay is None:
                return size, sha256
            partial.unlink(missing_ok=True)
            log(f"{film.name}: attempt {attempt} ended at {size:,} bytes; again in {delay:g} s")
        sleep(delay)
    raise AssertionError("unreachable: the last attempt returns or raises")


def fetch_film(
    film: PublishedFilm,
    site: Path,
    cache: Path | None = None,
    *,
    opener: Opener = open_release,
    delays: Sequence[float] = DOWNLOAD_RETRY_DELAYS,
    sleep: Callable[[float], object] = time.sleep,
    log: Callable[[str], object] = print,
) -> Path:
    """Put the pinned film at `site/films/<name>`, from the cache or the release.

    A cached copy is used only when its size and hash match the pin; otherwise the film
    is downloaded to a partial file beside where it will live, checked, and only then
    moved into place, so neither the cache nor the site ever holds an unchecked file.
    Raises `SystemExit` naming the mismatch when the release's file is not the pinned one.
    """
    target = site / site_path(film)
    target.parent.mkdir(parents=True, exist_ok=True)
    stored = cache / film.name if cache is not None else target
    if cache is not None:
        cache.mkdir(parents=True, exist_ok=True)
    if matches_pin(stored, film):
        log(f"{film.name}: {'cached' if cache is not None else 'present'}, matches the pin")
    else:
        partial = stored.with_name(f"{film.name}.partial")
        url = release_url(film)
        size, sha256 = _download_whole(
            film, partial, opener=opener, delays=delays, sleep=sleep, log=log
        )
        problems = pin_problems(film, size, sha256)
        if problems:
            partial.unlink(missing_ok=True)
            raise SystemExit(f"{url} is not the pinned film:\n  " + "\n  ".join(problems))
        partial.replace(stored)
        log(f"{film.name}: downloaded {size:,} bytes, matches the pin")
    if stored != target:
        partial = target.with_name(f"{film.name}.partial")
        shutil.copyfile(stored, partial)
        if not matches_pin(partial, film):
            partial.unlink(missing_ok=True)
            raise SystemExit(f"{film.name}: the copy into the site does not match the pin")
        partial.replace(target)
    return target


def fetch_films(
    site: Path,
    cache: Path | None = None,
    *,
    films: Sequence[PublishedFilm] = PUBLISHED_FILMS,
    opener: Opener = open_release,
    sleep: Callable[[float], object] = time.sleep,
    log: Callable[[str], object] = print,
) -> list[Path]:
    """Every pinned film into `site/films/`, each checked against the pin."""
    return [
        fetch_film(film, site, cache, opener=opener, sleep=sleep, log=log) for film in films
    ]


# --- The deployed site's media ------------------------------------------------------


@dataclass(frozen=True)
class MediaResponse:
    """What a one-byte range request returned: its status and headers, names lower-cased.

    Status 0 means the site could not be reached.
    """

    status: int
    headers: Mapping[str, str]

    @staticmethod
    def of(status: int, headers: Iterable[tuple[str, str]]) -> MediaResponse:
        return MediaResponse(status, {name.lower(): value for name, value in headers})


def expected_type(path: str) -> str | None:
    """The media type Pages must serve `path` as, by its extension."""
    return EXPECTED_TYPES.get(PurePosixPath(urlsplit(path).path).suffix.lower())


def media_type(value: str) -> str:
    """A `Content-Type` value's essence: its type and subtype, lower-cased."""
    return value.split(";", 1)[0].strip().lower()


def total_length(response: MediaResponse) -> int | None:
    """The whole file's length: from `Content-Range` on a 206, `Content-Length` on a 200."""
    if response.status == 206:
        content_range = response.headers.get("content-range", "")
        _, _, total = content_range.rpartition("/")
        return int(total) if total.strip().isdigit() else None
    length = response.headers.get("content-length", "").strip()
    return int(length) if length.isdigit() else None


def film_lengths(films: Iterable[PublishedFilm] = PUBLISHED_FILMS) -> dict[str, int]:
    """Each pinned film's byte count, by file name."""
    return {film.name: film.byte_count for film in films}


def media_problems(
    path: str, response: MediaResponse, *, expected_length: int | None = None
) -> list[str]:
    """Why the site's answer for `path` would not open or play in a browser, one line each."""
    if response.status not in (200, 206):
        return [f"{path}: status {response.status or 'unreachable'}, expected 200 or 206"]
    problems = []
    wanted = expected_type(path)
    served = response.headers.get("content-type", "")
    if wanted is None:
        problems.append(f"{path}: no media type is expected for this extension")
    elif media_type(served) != wanted:
        problems.append(f"{path}: served as {served or 'no Content-Type'}, expected {wanted}")
    disposition = response.headers.get("content-disposition", "")
    if "attachment" in disposition.lower():
        problems.append(f"{path}: served as an attachment ({disposition}), so it downloads")
    if path.lower().endswith(".mp4"):
        ranges = response.headers.get("accept-ranges", "")
        if ranges.strip().lower() != "bytes":
            problems.append(
                f"{path}: accept-ranges is {ranges or 'absent'}, so the player cannot seek"
            )
    if expected_length is not None:
        total = total_length(response)
        if total is None:
            problems.append(f"{path}: the response states no total length")
        elif total != expected_length:
            problems.append(f"{path}: {total:,} bytes served, pinned {expected_length:,}")
    return problems


def probe_once(url: str, *, timeout: float = 30.0) -> MediaResponse:
    """GET the first byte of `url` and return the status and headers, reading no body.

    The body is never read, so a server that ignores the range and answers 200 with the
    whole film costs one connection, not 216 MB.
    """
    if not url.startswith("https://"):
        raise ValueError(f"refusing to fetch a non-https URL: {url}")
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Range": "bytes=0-0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return MediaResponse.of(response.status, response.headers.items())
    except urllib.error.HTTPError as error:
        return MediaResponse.of(error.code, error.headers.items())
    except urllib.error.URLError:
        return MediaResponse(0, {})


def probe(
    url: str,
    *,
    delays: Sequence[float] = RETRY_DELAYS,
    sleep: Callable[[float], object] = time.sleep,
) -> MediaResponse:
    """`probe_once`, asked again after each delay while the answer is transient."""
    answer = probe_once(url)
    for delay in delays:
        if answer.status not in TRANSIENT_STATUSES:
            break
        sleep(delay)
        answer = probe_once(url)
    return answer


def check_media(
    site_url: str,
    paths: Iterable[str] = SITE_MEDIA,
    *,
    lengths: Mapping[str, int] | None = None,
    ask: Callable[[str], MediaResponse] = probe,
) -> list[str]:
    """Every problem with the deployed site's media, one line each; empty when all pass.

    `lengths` maps a file name to the byte count its total length must equal; the default
    is the pinned films'. `ask` returns the answer to a one-byte request for a URL.
    """
    lengths = film_lengths() if lengths is None else lengths
    base = site_url if site_url.endswith("/") else site_url + "/"
    problems = []
    for path in dict.fromkeys(paths):
        response = ask(urljoin(base, path))
        expected = lengths.get(PurePosixPath(urlsplit(path).path).name)
        problems.extend(media_problems(path, response, expected_length=expected))
    return problems


# --- The same-origin rule -----------------------------------------------------------


class _References(HTMLParser):
    """Every URL a page's elements name in `href`, `src`, `poster` or `srcset`."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for name, value in attrs:
            if value is None:
                continue
            if name in ("href", "src", "poster"):
                self.urls.append(value.strip())
            elif name == "srcset":
                self.urls.extend(part.split()[0] for part in value.split(",") if part.split())

    handle_startendtag = handle_starttag


def references(html: str) -> list[str]:
    """Every `href`, `src`, `poster` and `srcset` URL in `html`, in document order."""
    parser = _References()
    parser.feed(html)
    parser.close()
    return parser.urls


def _suffix(url: str) -> str:
    return PurePosixPath(urlsplit(url).path).suffix.lower()


def is_site_relative(url: str) -> bool:
    """Whether `url` resolves against the page it is on: no scheme, host or leading `/`."""
    parts = urlsplit(url)
    return not parts.scheme and not parts.netloc and not url.startswith("/")


def media_references(html: str, suffixes: Iterable[str] = EXPECTED_TYPES) -> list[str]:
    """The distinct media URLs `html` links or embeds, by extension, in document order."""
    wanted = frozenset(suffixes)
    return list(dict.fromkeys(url for url in references(html) if _suffix(url) in wanted))


def foreign_media(html: str) -> list[str]:
    """The media links in `html` that are not site-relative, and so not served by the site.

    A release download (served as an `application/octet-stream` attachment), a
    `raw.githubusercontent.com` file (octet-stream, `nosniff`), a `/blob/` URL (GitHub's
    HTML viewer), or any other absolute or root-relative URL to a PDF, MP4 or PNG.
    """
    return [
        url for url in media_references(html, SAME_ORIGIN_SUFFIXES) if not is_site_relative(url)
    ]


# --- Command line -------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--cache-key",
        action="store_true",
        help="print the key the verified films are cached under, derived from the pin alone",
    )
    mode.add_argument(
        "--fetch",
        type=Path,
        metavar="SITE",
        help="download the pinned films into SITE/films/, verifying each against the pin",
    )
    mode.add_argument(
        "--check-media",
        metavar="SITE_URL",
        help="check that the deployed site serves each media file as its type",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        metavar="DIR",
        help="with --fetch: verified copies to reuse, and where new downloads are kept",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=f"with --check-media: site-relative paths (default: {len(SITE_MEDIA)} files)",
    )
    args = parser.parse_args(argv)

    if args.cache_key:
        print(cache_key())
        return 0
    if args.fetch is not None:
        if args.paths:
            parser.error("--fetch takes no paths")
        fetch_films(args.fetch, args.cache)
        return 0
    if args.cache is not None:
        parser.error("--cache goes with --fetch")
    site_url = args.check_media
    paths = args.paths or list(SITE_MEDIA)
    problems = check_media(site_url, paths)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print(f"{len(paths)} media files at {site_url} serve as their types")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
