"""The overview's media: previews, drawings, the film, and the same-origin render test.

What is held here: each atlas preview is a deterministic PNG at twice its drawn size, with
no metadata and under its byte ceiling, and its caption is read from the files it
describes; the film is the site's own copy with the committed poster and the stamp its
frames carry; the hero, the thumbnails and the favicon carry only the container and the
squares, with nothing that could collide with an id on a page, and within their ceilings;
there is a thumbnail for every case record; and the overview links no media file it does
not serve itself.
"""

from __future__ import annotations

import posixpath
import re
import struct
import zlib
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from devtools import overview_media, published_media, render_explainer, render_overview
from devtools.overview_media import (
    COMPOSITES,
    FILM,
    POSTER,
    POSTER_SOURCE,
    PREVIEW_DISPLAY_WIDTH,
    RENDER_INPUTS,
    atlas_film,
    atlas_previews,
    favicon_svg,
    hero_svg,
    preview_png,
    read_packing,
    rendering_path,
    thumbnail_path,
    thumbnail_svg,
)
from devtools.site_kit import Asset
from sqpack.release import PUBLISHED_FILMS

FRONTIER = overview_media.PACKING / "frontier"
SVG = "{http://www.w3.org/2000/svg}"

#: Measured on 2026-09-30 at 222,851 and 491,812 bytes; about a seventh of headroom.
PREVIEW_CEILINGS = {
    "known-best-1-100-preview.png": 256_000,
    "known-best-1-324-preview.png": 560_000,
}
#: All 324 thumbnails measured 1,294,409 bytes on 2026-09-30, the largest 8,590.
THUMBNAILS_CEILING = 1_450_000
THUMBNAIL_CEILING = 10_000
#: Measured at 2,028 and 584 bytes.
HERO_CEILING = 3_000
FAVICON_CEILING = 1_024


@pytest.fixture(scope="module")
def assets() -> dict[str, bytes]:
    found: dict[str, bytes] = {}
    for asset in overview_media.assets():
        assert isinstance(asset, Asset)
        assert asset.path not in found, asset.path
        found[asset.path] = asset.content
    return found


def _png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    chunks, offset = [], 8
    while offset < len(data):
        (length,) = struct.unpack(">I", data[offset : offset + 4])
        kind = data[offset + 4 : offset + 8]
        chunks.append((kind, data[offset + 8 : offset + 8 + length]))
        offset += 12 + length
    return chunks


def _png_size(data: bytes) -> tuple[int, int]:
    kind, header = _png_chunks(data)[0]
    assert kind == b"IHDR"
    width, height = struct.unpack(">II", header[:8])
    return width, height


# --- Previews -----------------------------------------------------------------------


def test_the_previews_are_the_two_atlases_linking_their_pdfs() -> None:
    previews = atlas_previews()
    assert [p.image for p in previews] == list(PREVIEW_CEILINGS)
    assert [p.pdf for p in previews] == ["known-best-1-100.pdf", "known-best-1-324.pdf"]
    served = {path.name for path in render_explainer.COMPOSITE_ASSETS}
    for preview in previews:
        assert preview.pdf in served, (
            "the PDF is served beside the pages by the explainer build"
        )
        assert published_media.is_site_relative(preview.image)
        assert preview.width == PREVIEW_DISPLAY_WIDTH
        assert preview.alt


def test_each_preview_is_twice_its_drawn_size_and_under_its_ceiling(
    assets: dict[str, bytes],
) -> None:
    for preview in atlas_previews():
        data = assets[preview.image]
        assert len(data) <= PREVIEW_CEILINGS[preview.image], (preview.image, len(data))
        assert _png_size(data) == (2 * preview.width, 2 * preview.height)
        kinds = {kind for kind, _ in _png_chunks(data)}
        assert not kinds & {b"tEXt", b"iTXt", b"zTXt", b"tIME", b"eXIf", b"iCCP", b"pHYs"}, (
            kinds
        )


@pytest.mark.parametrize("stem", COMPOSITES, ids=lambda stem: stem.name)
def test_a_preview_renders_to_the_same_bytes_twice(stem: Path) -> None:
    first = preview_png(stem.with_suffix(".png"), 400, 300)
    assert preview_png(stem.with_suffix(".png"), 400, 300) == first


def test_the_captions_are_read_from_the_files_they_describe() -> None:
    small, full = atlas_previews()
    assert (small.size, small.pages) == ("87 KB", "25 by 30 in")
    assert (full.size, full.pages) == ("517 KB", "44 by 51 in")
    for preview, stem in zip(atlas_previews(), COMPOSITES, strict=True):
        assert preview.size == overview_media.format_bytes(
            stem.with_suffix(".pdf").stat().st_size
        )
        stamp = re.search(
            r'data-feature="release-stamp"[^>]*>([^<]+)<',
            stem.with_suffix(".svg").read_text(encoding="utf-8"),
        )
        assert stamp is not None
        assert preview.edition == stamp.group(1)


def test_a_compressed_media_box_is_found() -> None:
    page = b"<< /Type /Page /MediaBox [ 0 0 1800 2172 ] >>"
    stream = b"%PDF-1.7\n1 0 obj\n<< /Filter /FlateDecode >>\nstream\n" + zlib.compress(page)
    assert overview_media.pdf_media_box(stream + b"\nendstream\nendobj\n") == (1800, 2172)
    with pytest.raises(SystemExit, match="one page size"):
        overview_media.pdf_media_box(b"%PDF-1.7\n")


@pytest.mark.parametrize(
    ("count", "text"),
    [(512, "512 bytes"), (86_697, "87 KB"), (2_487_506, "2.5 MB"), (216_275_792, "216 MB")],
)
def test_sizes_are_given_in_decimal_units(count: int, text: str) -> None:
    assert overview_media.format_bytes(count) == text


# --- The film -----------------------------------------------------------------------


def test_the_film_is_the_sites_copy_with_its_own_stamp(assets: dict[str, bytes]) -> None:
    film = atlas_film()
    assert FILM in PUBLISHED_FILMS
    assert film.src == f"films/{FILM.name}" == published_media.site_path(FILM)
    assert film.src.endswith("ascent-n1-324-1080p60-citations.mp4")
    assert film.type == 'video/mp4; codecs="avc1.640028"'
    assert (film.width, film.height) == (1920, 1080)
    assert (film.size, film.duration) == ("216 MB", "8m 14s")
    # The frames' stamp, not the edition every artifact prints now.
    assert film.edition == FILM.edition == "v0.4.2-d48006"
    assert film.release == "https://github.com/jlevy/squares/releases/tag/v0.4.2"
    assert film.poster == POSTER
    assert assets[POSTER] == POSTER_SOURCE.read_bytes()


def test_the_poster_is_a_frame_the_size_of_the_other_one() -> None:
    other = POSTER_SOURCE.with_name("ascent-n1-100-poster.png")
    assert _png_size(POSTER_SOURCE.read_bytes()) == _png_size(other.read_bytes()) == (1280, 720)


# --- Drawings -----------------------------------------------------------------------


def _parse(svg: str) -> ET.Element:
    root = ET.fromstring(svg)
    assert root.tag == f"{SVG}svg"
    return root


def _clean(root: ET.Element) -> None:
    for element in root.iter():
        assert element.tag not in {f"{SVG}title", f"{SVG}desc", f"{SVG}metadata", f"{SVG}text"}
        assert "id" not in element.attrib, element.attrib
        assert not any(name.startswith("data-") for name in element.attrib), element.attrib
        assert not any("href" in name for name in element.attrib), element.attrib


def _squares(root: ET.Element) -> list[str]:
    """The fill of each square drawn, one per `M` in a filled path's data."""
    return [
        path.get("fill", "")
        for path in root.iter(f"{SVG}path")
        if path.get("fill") not in (None, "none", "#fff")
        for _ in range(path.get("d", "").count("M"))
    ]


def _rendered_fills(n: int) -> list[str]:
    return sorted(fill for fill, _ in read_packing(n).squares)


def test_the_hero_is_n_53_stripped_and_sized_by_css() -> None:
    svg = hero_svg()
    assert len(svg.encode("utf-8")) <= HERO_CEILING
    root = _parse(svg)
    _clean(root)
    assert root.get("viewBox")
    assert "width" not in root.attrib
    assert "height" not in root.attrib
    assert root.get("stroke") == "currentColor"
    assert root.get("role") == "img"
    assert sorted(_squares(root)) == _rendered_fills(53)
    assert "<?xml" not in svg


def test_the_rendering_svgs_carry_ids_the_drawings_drop() -> None:
    source = rendering_path(53).read_text(encoding="utf-8")
    assert 'id="figure-title"' in source
    assert 'id="panel-0"' in source
    assert " id=" not in hero_svg()


def test_there_is_a_small_clean_thumbnail_for_every_case(assets: dict[str, bytes]) -> None:
    cases = sorted(int(path.stem.removeprefix("n-")) for path in FRONTIER.glob("n-[0-9]*.md"))
    assert len(cases) == 324
    thumbnails = {path: data for path, data in assets.items() if path.startswith("thumbs/")}
    assert set(thumbnails) == {thumbnail_path(n) for n in cases}
    assert sum(len(data) for data in thumbnails.values()) <= THUMBNAILS_CEILING
    assert max(len(data) for data in thumbnails.values()) <= THUMBNAIL_CEILING
    for n in cases:
        root = _parse(thumbnails[thumbnail_path(n)].decode("utf-8"))
        _clean(root)
        assert "width" not in root.attrib
        assert len(_squares(root)) == n, n


@pytest.mark.parametrize("n", [1, 11, 53, 68, 324])
def test_a_thumbnail_keeps_the_rendering_s_fills(n: int) -> None:
    assert sorted(_squares(_parse(thumbnail_svg(n)))) == _rendered_fills(n)


def test_a_thumbnail_turns_its_outlines_light_on_a_dark_page() -> None:
    svg = thumbnail_svg(11)
    assert 'stroke="#000"' in svg
    assert "@media (prefers-color-scheme:dark){svg{stroke:#e3e7ec}}" in svg


def test_the_favicon_is_n_11_and_small() -> None:
    svg = favicon_svg()
    assert len(svg.encode("utf-8")) <= FAVICON_CEILING
    root = _parse(svg)
    _clean(root)
    assert root.get("viewBox") == "0 0 32 32"
    assert sorted(_squares(root)) == _rendered_fills(11)


def test_rounding_keeps_axis_aligned_edges_as_h_and_v() -> None:
    corners = ((0.0, 0.5), (0.25, 0.5), (0.25, 0.25), (0.0, 0.25))
    assert overview_media.square_path(corners, scale=1000, offset=0, digits=0) == (
        "M0 500H250V250H0Z"
    )
    tilted = ((0.1, 0.2), (0.3, 0.1), (0.4, 0.3), (0.2, 0.4))
    assert overview_media.square_path(tilted, scale=10, offset=1, digits=1) == (
        "M2 3L4 2L5 4L3 5Z"
    )


# --- Inputs and the same-origin rule ------------------------------------------------


def test_every_input_is_declared_and_exists() -> None:
    assert all(path.exists() for path in RENDER_INPUTS)
    assert set(RENDER_INPUTS) <= set(render_overview.RENDER_INPUTS)
    assert overview_media.RENDERING in RENDER_INPUTS
    assert POSTER_SOURCE in RENDER_INPUTS


def test_the_overview_links_only_media_the_site_serves() -> None:
    """No release download, raw file or `/blob/` page, and nothing the site does not hold."""
    served = (
        {asset.path for asset in render_overview.site_assets_of()}
        | {path.name for path in render_explainer.COMPOSITE_ASSETS}
        | {published_media.site_path(film) for film in PUBLISHED_FILMS}
    )
    pages = [page for page in render_overview.site_pages_of() if page.key == "overview"]
    assert pages, "the overview is one of the site's pages"
    for page in pages:
        html = render_overview.page_html(page, commit="0" * 40)
        assert published_media.foreign_media(html) == [], page.path
        for url in published_media.media_references(html):
            if url.startswith("data:"):
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(page.path), url))
            assert resolved in served, (page.path, url)
