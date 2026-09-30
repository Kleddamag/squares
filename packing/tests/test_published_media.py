"""The site's films are the pinned ones, and the deployed site serves its media as media.

A release download is an `application/octet-stream` attachment, so the site serves its own
copies of the films. What is held here: the pin's shape and the cache key derived from it;
the fetch refuses any file that is not the pinned one and leaves nothing unchecked
behind; the post-deploy decision accepts what Pages serves for a PDF, a PNG and a film and
refuses an octet-stream, an attachment, a film that cannot seek, and a wrong length; and
the same-origin rule names every media link a page makes to somewhere other than itself.
No test here touches the network: the opener and the probe are passed in.
"""

from __future__ import annotations

import hashlib
import io
import re
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO

import pytest

from devtools import published_media
from devtools.published_media import (
    SITE_MEDIA,
    MediaResponse,
    cache_key,
    check_media,
    fetch_films,
    foreign_media,
    media_problems,
    media_references,
    release_page,
    release_url,
    site_path,
    total_length,
)
from sqpack.release import PUBLICATION_HISTORY, PUBLISHED_FILMS, PublishedFilm

STAMP = re.compile(r"v\d+\.\d+\.\d+-[0-9a-f]{6}")


# --- The pin ------------------------------------------------------------------------


def test_the_pin_names_both_ascent_films_of_a_published_edition() -> None:
    names = [film.name for film in PUBLISHED_FILMS]
    assert names == [
        "ascent-n1-100-1080p60-citations.mp4",
        "ascent-n1-324-1080p60-citations.mp4",
    ]
    versions = {entry.version for entry in PUBLICATION_HISTORY}
    for film in PUBLISHED_FILMS:
        assert film.tag in versions, film.name
        assert re.fullmatch(r"[0-9a-f]{64}", film.sha256), film.name
        assert film.byte_count > 1_000_000, film.name
        assert film.profile in {"social", "archive"}, film.name
        assert film.seconds > 0, film.name
        assert (film.width, film.height) == (1920, 1080), film.name
        # The frames' own stamp, which names the edition the release was cut for.
        assert STAMP.fullmatch(film.edition), film.name
        assert film.edition.startswith(film.tag + "-"), film.name
    assert len({film.sha256 for film in PUBLISHED_FILMS}) == len(PUBLISHED_FILMS)


def test_the_pin_is_the_one_the_plan_measured() -> None:
    pinned = {
        film.name: (film.profile, film.byte_count, film.sha256) for film in PUBLISHED_FILMS
    }
    assert pinned == {
        "ascent-n1-100-1080p60-citations.mp4": (
            "social",
            39_969_792,
            "6067ef13e9e9d9fa250f561ad71ecae21e9680e8c240f7e03e559d0050a854d7",
        ),
        "ascent-n1-324-1080p60-citations.mp4": (
            "archive",
            216_275_792,
            "91d9c52fd8afb588e3dce268728fe483a4bc0e0aab0811c0504913f0924f3e6a",
        ),
    }


def test_the_films_are_fetched_from_their_release_and_served_under_films() -> None:
    film = PUBLISHED_FILMS[1]
    assert release_url(film) == (
        "https://github.com/jlevy/squares/releases/download/v0.4.2/"
        "ascent-n1-324-1080p60-citations.mp4"
    )
    assert release_page(film.tag) == "https://github.com/jlevy/squares/releases/tag/v0.4.2"
    assert site_path(film) == "films/ascent-n1-324-1080p60-citations.mp4"
    assert {site_path(film) for film in PUBLISHED_FILMS} <= set(SITE_MEDIA)


def test_the_cache_key_moves_with_the_films_and_nothing_else() -> None:
    key = cache_key()
    assert re.fullmatch(r"films-[0-9a-f]{16}", key)
    assert cache_key() == key
    assert cache_key(reversed(PUBLISHED_FILMS)) == key
    # What the frames say or how long they run does not change which bytes are cached.
    restamped = [
        film._replace(edition="v9.9.9-000000", seconds=1.0, profile="web")
        for film in PUBLISHED_FILMS
    ]
    assert cache_key(restamped) == key
    first, second = PUBLISHED_FILMS
    assert cache_key([first._replace(sha256="0" * 64), second]) != key
    assert cache_key([first._replace(name="other.mp4"), second]) != key
    assert cache_key([first]) != key


def test_the_cache_key_command_prints_one_line(capsys: pytest.CaptureFixture[str]) -> None:
    assert published_media.main(["--cache-key"]) == 0
    assert capsys.readouterr().out == cache_key() + "\n"


def test_cache_goes_only_with_fetch() -> None:
    with pytest.raises(SystemExit):
        published_media.main(["--check-media", "https://example.org/", "--cache", "x"])


# --- Fetching -----------------------------------------------------------------------


def _film(name: str, content: bytes) -> PublishedFilm:
    return PublishedFilm(
        tag="v0.0.1",
        name=name,
        byte_count=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
        profile="social",
        seconds=1.0,
        width=1920,
        height=1080,
        edition="v0.0.1-000000",
    )


class Release:
    """A release that serves fixed bytes by file name, and counts what was asked of it."""

    def __init__(self, files: dict[str, bytes], failures: int = 0) -> None:
        self.files = files
        self.failures = failures
        self.requests: list[str] = []

    @contextmanager
    def open(self, url: str) -> Iterator[BinaryIO]:
        self.requests.append(url)
        if self.failures:
            self.failures -= 1
            raise ConnectionResetError("reset by peer")
        yield io.BytesIO(self.files[url.rsplit("/", 1)[1]])


FILMS = (_film("a.mp4", b"first film " * 1000), _film("b.mp4", b"second film " * 900))
CONTENT = {"a.mp4": b"first film " * 1000, "b.mp4": b"second film " * 900}


def _quiet(_: object) -> None:
    return None


def test_fetch_downloads_verifies_and_then_reuses_the_cache(tmp_path: Path) -> None:
    site, cache = tmp_path / "site", tmp_path / "cache"
    release = Release(CONTENT)
    paths = fetch_films(site, cache, films=FILMS, opener=release.open, sleep=_quiet, log=_quiet)
    assert [path.relative_to(site).as_posix() for path in paths] == [
        "films/a.mp4",
        "films/b.mp4",
    ]
    assert all(path.read_bytes() == CONTENT[path.name] for path in paths)
    assert sorted(path.name for path in cache.iterdir()) == ["a.mp4", "b.mp4"]
    assert len(release.requests) == 2

    fresh = tmp_path / "fresh-site"
    fetch_films(fresh, cache, films=FILMS, opener=release.open, sleep=_quiet, log=_quiet)
    assert len(release.requests) == 2, "a verified cache is not downloaded again"
    assert (fresh / "films" / "b.mp4").read_bytes() == CONTENT["b.mp4"]


def test_fetch_replaces_a_cached_copy_that_no_longer_matches(tmp_path: Path) -> None:
    site, cache = tmp_path / "site", tmp_path / "cache"
    cache.mkdir()
    (cache / "a.mp4").write_bytes(b"x" * len(CONTENT["a.mp4"]))
    release = Release(CONTENT)
    fetch_films(site, cache, films=FILMS[:1], opener=release.open, sleep=_quiet, log=_quiet)
    assert release.requests == [release_url(FILMS[0])]
    assert (cache / "a.mp4").read_bytes() == CONTENT["a.mp4"]


def test_fetch_refuses_a_file_that_is_not_the_pinned_one(tmp_path: Path) -> None:
    site, cache = tmp_path / "site", tmp_path / "cache"
    release = Release({"a.mp4": CONTENT["a.mp4"][:-1] + b"!"})
    with pytest.raises(SystemExit, match="is not the pinned film") as refused:
        fetch_films(site, cache, films=FILMS[:1], opener=release.open, sleep=_quiet, log=_quiet)
    assert "SHA-256" in str(refused.value)
    assert len(release.requests) == 1, "a complete download that does not match is not retried"
    assert not any(cache.iterdir())
    assert not (site / "films" / "a.mp4").exists()

    short = Release({"a.mp4": CONTENT["a.mp4"][:100]})
    with pytest.raises(SystemExit, match="100 bytes, pinned"):
        fetch_films(site, cache, films=FILMS[:1], opener=short.open, sleep=_quiet, log=_quiet)
    assert len(short.requests) == len(published_media.DOWNLOAD_RETRY_DELAYS) + 1
    assert not any(cache.iterdir())


def test_fetch_retries_a_broken_connection_after_a_pause(tmp_path: Path) -> None:
    pauses: list[float] = []
    release = Release(CONTENT, failures=1)
    fetch_films(
        tmp_path, None, films=FILMS[:1], opener=release.open, sleep=pauses.append, log=_quiet
    )
    assert len(release.requests) == 2
    assert pauses == [published_media.DOWNLOAD_RETRY_DELAYS[0]]
    assert (tmp_path / "films" / "a.mp4").read_bytes() == CONTENT["a.mp4"]

    pauses.clear()
    broken = Release(CONTENT, failures=len(published_media.DOWNLOAD_RETRY_DELAYS) + 1)
    with pytest.raises(SystemExit, match="download failed"):
        fetch_films(
            tmp_path / "other", None, films=FILMS[:1], opener=broken.open, sleep=pauses.append
        )
    assert pauses == list(published_media.DOWNLOAD_RETRY_DELAYS)
    assert not (tmp_path / "other" / "films" / "a.mp4.partial").exists()


def test_fetch_without_a_cache_keeps_a_file_already_in_place(tmp_path: Path) -> None:
    (tmp_path / "films").mkdir()
    (tmp_path / "films" / "a.mp4").write_bytes(CONTENT["a.mp4"])
    release = Release(CONTENT)
    fetch_films(tmp_path, None, films=FILMS[:1], opener=release.open, sleep=_quiet, log=_quiet)
    assert release.requests == []


def test_the_release_opener_refuses_plain_http() -> None:
    with pytest.raises(ValueError, match="non-https"):
        published_media.open_release("http://example.org/a.mp4")
    with pytest.raises(ValueError, match="non-https"):
        published_media.probe_once("http://example.org/a.mp4")


# --- The deployed site's media ------------------------------------------------------

FILM = PUBLISHED_FILMS[1]
FILM_PATH = site_path(FILM)


def _answer(status: int = 206, **headers: str) -> MediaResponse:
    return MediaResponse.of(
        status, [(name.replace("_", "-"), value) for name, value in headers.items()]
    )


def _film_answer(**overrides: str) -> MediaResponse:
    headers = {
        "Content_Type": "video/mp4",
        "Accept_Ranges": "bytes",
        "Content_Range": f"bytes 0-0/{FILM.byte_count}",
        "Content_Length": "1",
    }
    headers.update(overrides)
    return _answer(206, **{name: value for name, value in headers.items() if value})


def test_what_pages_serves_passes() -> None:
    assert media_problems(FILM_PATH, _film_answer(), expected_length=FILM.byte_count) == []
    pdf = _answer(206, Content_Type="application/pdf", Content_Range="bytes 0-0/86697")
    assert media_problems("known-best-1-100.pdf", pdf) == []
    png = _answer(200, Content_Type="image/png", Content_Length="222851")
    assert media_problems("known-best-1-100-preview.png", png, expected_length=222851) == []
    assert media_problems("x.png", _answer(206, Content_Type="image/png; q=1")) == []


def test_a_release_style_answer_fails_every_way_it_can() -> None:
    download = _answer(
        200,
        Content_Type="application/octet-stream",
        Content_Disposition="attachment; filename=ascent-n1-324-1080p60-citations.mp4",
        Content_Length="12",
    )
    problems = media_problems(FILM_PATH, download, expected_length=FILM.byte_count)
    assert any("served as application/octet-stream, expected video/mp4" in p for p in problems)
    assert any("as an attachment" in p for p in problems)
    assert any("accept-ranges is absent" in p for p in problems)
    assert any("12 bytes served, pinned 216,275,792" in p for p in problems)


def test_each_requirement_is_checked_on_its_own() -> None:
    expected = FILM.byte_count

    def problems(answer: MediaResponse, path: str = FILM_PATH) -> list[str]:
        return media_problems(path, answer, expected_length=expected)

    assert problems(_film_answer(Content_Type="text/html; charset=utf-8"))
    assert problems(_film_answer(Content_Disposition="attachment"))
    assert problems(_film_answer(Content_Disposition="inline")) == []
    assert problems(_film_answer(Accept_Ranges="none"))
    assert problems(_film_answer(Content_Range=f"bytes 0-0/{expected - 1}"))
    assert problems(_film_answer(Content_Range="bytes 0-0/*"))
    assert problems(_answer(404)) == [f"{FILM_PATH}: status 404, expected 200 or 206"]
    assert "unreachable" in problems(_answer(0))[0]
    assert media_problems("known-best-1-324.pdf", _answer(206, Content_Type="text/html"))
    assert media_problems("notes.txt", _answer(206, Content_Type="text/plain"))


def test_the_total_length_comes_from_the_range_or_the_whole_body() -> None:
    assert total_length(_answer(206, Content_Range="bytes 0-0/1234")) == 1234
    assert total_length(_answer(206, Content_Length="1")) is None
    assert total_length(_answer(200, Content_Length="1234")) == 1234
    assert total_length(_answer(200)) is None


def test_check_media_asks_for_each_file_under_the_site_and_holds_films_to_the_pin() -> None:
    asked: list[str] = []

    def ask(url: str) -> MediaResponse:
        asked.append(url)
        if url.endswith(".mp4"):
            return _film_answer(Content_Range="bytes 0-0/1")
        return _answer(206, Content_Type="application/pdf", Content_Range="bytes 0-0/5")

    problems = check_media(
        "https://jlevy.github.io/squares",
        ["known-best-1-100.pdf", FILM_PATH, FILM_PATH],
        ask=ask,
    )
    assert asked == [
        "https://jlevy.github.io/squares/known-best-1-100.pdf",
        f"https://jlevy.github.io/squares/{FILM_PATH}",
    ]
    assert problems == [f"{FILM_PATH}: 1 bytes served, pinned {FILM.byte_count:,}"]


# --- The same-origin rule -----------------------------------------------------------

PAGE = """<!doctype html><html><head>
<link rel="canonical" href="https://jlevy.github.io/squares/">
<meta property="og:image" content="https://jlevy.github.io/squares/known-best-1-100-card.png">
<link rel="icon" href="data:image/svg+xml;base64,AAAA">
</head><body>
<a href="known-best-1-100.pdf"><img src="known-best-1-100-preview.png" alt=""></a>
<a href="./known-best-1-324.pdf"><img srcset="a.png 1x, b.png 2x" alt=""></a>
<video poster="ascent-n1-324-poster.png">
<source src="films/ascent-n1-324-1080p60-citations.mp4"></video>
<img src="thumbs/n-011.svg" alt="">
<a href="https://github.com/jlevy/squares/releases/tag/v0.4.2">the release</a>
<a href="https://github.com/jlevy/squares/blob/abc/packing/frontier/n-011.md">n = 11</a>
</body></html>"""

FOREIGN = [
    "https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-324-1080p60-citations.mp4",
    "https://raw.githubusercontent.com/jlevy/squares/abc/packing/atlas/known-best/known-best-1-324.png",
    "https://github.com/jlevy/squares/blob/abc/packing/atlas/known-best/known-best-1-324.pdf",
    "https://github.com/jlevy/squares/blob/abc/x.pdf?raw=true",
    "https://jlevy.github.io/squares/known-best-1-100.pdf",
    "//jlevy.github.io/squares/films/x.mp4",
    "/squares/known-best-1-100-preview.png",
]


def test_site_relative_media_and_non_media_links_pass() -> None:
    assert foreign_media(PAGE) == []
    assert media_references(PAGE) == [
        "known-best-1-100.pdf",
        "known-best-1-100-preview.png",
        "./known-best-1-324.pdf",
        "a.png",
        "b.png",
        "ascent-n1-324-poster.png",
        "films/ascent-n1-324-1080p60-citations.mp4",
        "thumbs/n-011.svg",
    ]


@pytest.mark.parametrize("url", FOREIGN)
def test_release_raw_blob_and_absolute_media_links_are_foreign(url: str) -> None:
    for markup in (
        f'<a href="{url}">x</a>',
        f'<video><source src="{url}"></video>',
        f'<video poster="{url}"></video>',
        f'<img srcset="ok.png 1x, {url} 2x" alt="">',
    ):
        assert foreign_media(PAGE.replace("</body>", markup + "</body>")) == [url], markup


def test_the_media_the_check_asks_for_by_default_is_what_the_site_serves() -> None:
    assert len(set(SITE_MEDIA)) == len(SITE_MEDIA)
    assert all(published_media.expected_type(path) for path in SITE_MEDIA)
    assert all(published_media.is_site_relative(path) for path in SITE_MEDIA)
