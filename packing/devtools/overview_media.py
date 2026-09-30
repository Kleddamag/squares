#!/usr/bin/env python3
"""The files the site's pages serve beside them: previews, drawings and the favicon.

`devtools.render_overview` collects them from `assets()` and writes them into its output
directory; nothing here is committed, so no file under `DATA_PATHS` changes.

**Previews.** The committed atlas composites are too heavy to show as previews
(`known-best-1-324.png` is 4,224 by 4,912 pixels and 2.5 MB), so each is scaled with
Pillow to twice the width the overview draws it at, `PREVIEW_DISPLAY_WIDTH`, and reduced to
a 256-colour palette by median cut without dithering, which keeps the paper white and the
packing palette's fills exact. The bytes carry no metadata, so two renders are identical.
Each preview links to its composite's PDF, which the explainer's build already serves
beside the pages (`render_explainer.COMPOSITE_ASSETS`). The caption's edition is the
composite's own stamp, read from the SVG the PNG records it was rendered from.

**Drawings.** The hero, the favicon and the frontier thumbnails are drawn from the
rendering SVGs under `atlas/known-best/rendering/`, keeping only the container and the
squares: no ids, titles, descriptions, metadata, background or caption, and coordinates
rounded in the container's own units, for drawing only. The rendering SVGs are never
inlined: each carries ids such as `figure-title` and `panel-0` that the explainer's
inlined `n = 11` drawing also uses. Squares of one fill share one path, and every outline
is inherited from the root, so a thumbnail of 324 squares is 7 KB rather than 330.

- The hero is inlined, so its outlines are `currentColor` and follow the page's theme;
  its fills are the packing palette's, unchanged, and its stroke does not scale, as the
  rendering's does not.
- A thumbnail is loaded as an `<img>`, which inherits nothing from the page, so its
  outlines are black and turn light under `prefers-color-scheme: dark`, which a browser
  answers from the embedding element's `color-scheme`. Their stroke is a fixed fraction
  of the container, as on the atlas composite, so a dense case reads as a grid, not ink.
- The favicon is a tile of paper with the `n = 11` packing on it, so it reads on a light
  tab strip and a dark one alike.

**The film.** The overview embeds the `n = 1…324` ascent from the site's own copy under
`films/` (`devtools.published_media`), with a poster cut from its last frame and
committed beside the explainer's (`packages/workbench/assets/`). Its caption's edition is
the stamp its frames carry, from `sqpack.release.PUBLISHED_FILMS`, never
`PUBLICATION_EDITION`, which moves with every re-pin while the film does not.
"""

from __future__ import annotations

import hashlib
import io
import re
import zlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

from devtools import published_media
from devtools.site_kit import Asset
from sqpack import release
from sqpack.release import PUBLISHED_FILMS

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
ATLAS = PACKING / "atlas" / "known-best"
RENDERING = ATLAS / "rendering"
RELEASE_MODULE = Path(release.__file__)

#: The composites the overview previews, `n = 1…100` then `n = 1…324`. Each is a stem;
#: the PNG is scaled, the PDF is linked, and the SVG holds the stamp.
COMPOSITES: tuple[Path, ...] = (ATLAS / "known-best-1-100", ATLAS / "known-best-1-324")
#: What each preview is a picture of.
PREVIEW_ALTS = {
    "known-best-1-100": (
        "The best known packings of one through one hundred unit squares, in a ten-by-ten "
        "grid, each labelled with its bounds"
    ),
    "known-best-1-324": (
        "The best known packings of one through three hundred twenty-four unit squares, "
        "in an eighteen-by-eighteen grid, each labelled with its bounds"
    ),
}
#: The CSS width the overview draws each preview at, two side by side; the PNG is twice
#: that, so it is sharp on a high-density screen.
PREVIEW_DISPLAY_WIDTH = 560
PREVIEW_SCALE = 2
PREVIEW_COLOURS = 256

#: The `<text>` element each composite SVG stamps its edition in.
RELEASE_STAMP = re.compile(r'<text\b[^>]*\bdata-feature="release-stamp"[^>]*>([^<]+)</text>')
#: The PNG text chunk the atlas builder records its source SVG's hash in.
SOURCE_SVG_KEY = "sqpack-source-svg-sha256"

#: The film the overview embeds, and its poster, committed beside the `n = 1…100` one.
FILM = next(film for film in PUBLISHED_FILMS if film.name.startswith("ascent-n1-324-"))
#: H.264 High profile, level 4.0, as the receipt's `delivered` probe records it; the
#: explainer's `<source>` names the same codec. The value is the attribute's text, unescaped.
FILM_TYPE = 'video/mp4; codecs="avc1.640028"'
POSTER_SOURCE = REPO / "packages" / "workbench" / "assets" / "ascent-n1-324-poster.png"
POSTER = POSTER_SOURCE.name

HERO_N = 53
FAVICON_N = 11

#: Every drawing is in the container's units scaled to this, rounded to whole numbers:
#: a thousandth of the container, far below a pixel at any size the site draws them.
DRAWING_SCALE = 1000
#: The hero's outline, in CSS pixels whatever its size, as the rendering SVG draws it.
HERO_STROKE = 1.25
#: A thumbnail's outline, as a fraction of the container: the atlas composite's weight,
#: at which `n = 324`'s grid reads as lines on green rather than as a black square.
THUMBNAIL_STROKE = 6.5
#: What a thumbnail's outlines turn to on a dark page: kpress's dark text, near enough.
THUMBNAIL_DARK_STROKE = "#e3e7ec"
#: The favicon's grid: the container at 30 units on a 32-unit tile.
FAVICON_SIZE = 32
FAVICON_INSET = 1
FAVICON_STROKE = 0.7
FAVICON_INK = "#1b2631"

SVG_NS = "http://www.w3.org/2000/svg"

RENDER_INPUTS: tuple[Path, ...] = (
    Path(__file__),
    Path(published_media.__file__),
    RELEASE_MODULE,
    RENDERING,
    *(stem.with_suffix(suffix) for stem in COMPOSITES for suffix in (".png", ".pdf", ".svg")),
    POSTER_SOURCE,
)


@dataclass(frozen=True)
class Preview:
    """An atlas preview image and the PDF it links to, both site-relative.

    `image` is the preview PNG this module writes; `pdf` is the composite PDF served beside
    the pages. `width` and `height` are the CSS size to draw it at, half its pixels.
    `size` and `pages` are for the caption, for example `87 KB` and `25 by 30 in`.
    """

    image: str
    width: int
    height: int
    alt: str
    pdf: str
    size: str
    pages: str
    edition: str


@dataclass(frozen=True)
class Film:
    """The overview's one embedded film: the full `n = 1…324` ascent, never autoplayed.

    `src` and `poster` are site-relative; `type` is the `<source>` type attribute, whose
    quotes the page escapes. `release` is the release page, the archive of record with the
    film's receipt.
    """

    src: str
    type: str
    poster: str
    width: int
    height: int
    size: str
    duration: str
    edition: str
    release: str


# --- Captions -----------------------------------------------------------------------


def format_bytes(count: int) -> str:
    """A file size as a caption gives it, in decimal units: `87 KB`, `2.5 MB`, `216 MB`."""
    if count < 1000:
        return f"{count} bytes"
    if count < 1_000_000:
        return f"{round(count / 1000)} KB"
    megabytes = count / 1_000_000
    return f"{megabytes:.1f} MB" if megabytes < 10 else f"{round(megabytes)} MB"


def format_duration(seconds: float) -> str:
    """A running time as the explainer gives it: `8m 14s`."""
    minutes, rest = divmod(round(seconds), 60)
    return f"{minutes}m {rest}s" if minutes else f"{rest}s"


def pdf_media_box(data: bytes) -> tuple[float, float]:
    """The first page's size in points, from its `/MediaBox`, compressed or not.

    The composites are written by cairo, which keeps page objects in compressed object
    streams, so each Flate stream is inflated and searched as well as the plain bytes.
    Every page of a composite is one size, so a PDF declaring two sizes is refused.
    """
    box = re.compile(rb"/MediaBox\s*\[\s*([-\d.\s]+?)\s*\]")
    found = set(box.findall(data))
    for start in re.finditer(rb"stream\r?\n", data):
        try:
            found.update(box.findall(zlib.decompressobj().decompress(data[start.end() :])))
        except zlib.error:
            continue
    sizes = set()
    for entry in found:
        x0, y0, x1, y1 = (float(value) for value in entry.split())
        sizes.add((x1 - x0, y1 - y0))
    if len(sizes) != 1:
        raise SystemExit(f"expected one page size in the PDF, found {sorted(sizes)}")
    return sizes.pop()


def format_page_size(points: tuple[float, float]) -> str:
    """A page size in whole inches, as a caption gives it: `25 by 30 in`."""
    width, height = (round(value / 72) for value in points)
    return f"{width} by {height} in"


def composite_stamp(stem: Path) -> str:
    """The edition the composite is stamped with, checked to be the PNG's too."""
    svg = stem.with_suffix(".svg").read_bytes()
    stamps = RELEASE_STAMP.findall(svg.decode("utf-8"))
    if len(stamps) != 1:
        raise SystemExit(f"{stem.name}.svg carries {len(stamps)} release stamps, not one")
    with Image.open(stem.with_suffix(".png")) as png:
        recorded = png.info.get(SOURCE_SVG_KEY)
    if recorded != hashlib.sha256(svg).hexdigest():
        raise SystemExit(
            f"{stem.name}.png was not rendered from {stem.name}.svg, so the stamp read "
            "there is not the preview's; rebuild the atlas"
        )
    return stamps[0].strip()


# --- Previews -----------------------------------------------------------------------


def preview_png(source: Path, width: int, height: int) -> bytes:
    """`source` scaled to `width` by `height`, as a palette PNG with no metadata."""
    with Image.open(source) as original:
        scaled = original.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    reduced = scaled.quantize(
        PREVIEW_COLOURS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
    )
    reduced.info.clear()
    buffer = io.BytesIO()
    reduced.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def preview_name(stem: Path) -> str:
    return f"{stem.name}-preview.png"


def _display_size(stem: Path) -> tuple[int, int]:
    with Image.open(stem.with_suffix(".png")) as original:
        width, height = original.size
    return PREVIEW_DISPLAY_WIDTH, round(PREVIEW_DISPLAY_WIDTH * height / width)


@cache
def _previews() -> tuple[tuple[Preview, bytes], ...]:
    built = []
    for stem in COMPOSITES:
        width, height = _display_size(stem)
        image = preview_png(
            stem.with_suffix(".png"), width * PREVIEW_SCALE, height * PREVIEW_SCALE
        )
        pdf = stem.with_suffix(".pdf")
        data = pdf.read_bytes()
        preview = Preview(
            image=preview_name(stem),
            width=width,
            height=height,
            alt=PREVIEW_ALTS[stem.name],
            pdf=pdf.name,
            size=format_bytes(len(data)),
            pages=format_page_size(pdf_media_box(data)),
            edition=composite_stamp(stem),
        )
        built.append((preview, image))
    return tuple(built)


def atlas_previews() -> tuple[Preview, ...]:
    """The `n = 1…100` and `n = 1…324` previews, in that order."""
    return tuple(preview for preview, _ in _previews())


# --- The film -----------------------------------------------------------------------


def atlas_film() -> Film:
    """The `n = 1…324` film as the overview embeds it."""
    return Film(
        src=published_media.site_path(FILM),
        type=FILM_TYPE,
        poster=POSTER,
        width=FILM.width,
        height=FILM.height,
        size=format_bytes(FILM.byte_count),
        duration=format_duration(FILM.seconds),
        edition=FILM.edition,
        release=published_media.release_page(FILM.tag),
    )


# --- Drawings -----------------------------------------------------------------------

Point = tuple[float, float]


@dataclass(frozen=True)
class Packing:
    """A case's squares as its rendering draws them, in container units, y down.

    The container runs from 0 to 1 on each axis; each square is its fill and its corners.
    """

    n: int
    squares: tuple[tuple[str, tuple[Point, ...]], ...]


def rendering_path(n: int) -> Path:
    return RENDERING / f"n-{n:03d}.svg"


def rendered_cases() -> list[int]:
    """Every `n` with a rendering, in order."""
    return sorted(int(path.stem.removeprefix("n-")) for path in RENDERING.glob("n-*.svg"))


def read_packing(n: int) -> Packing:
    """The container and the filled squares of case `n`'s rendering, and nothing else."""
    root = ET.parse(rendering_path(n)).getroot()
    features: dict[str, list[ET.Element]] = {}
    for element in root.iter():
        feature = element.get("data-feature")
        if feature is not None:
            features.setdefault(feature, []).append(element)
    containers = features.get("container-outline", [])
    if len(containers) != 1:
        raise SystemExit(
            f"{rendering_path(n).name}: expected one container, not {len(containers)}"
        )
    box = containers[0]
    left, top, width, height = (
        float(box.get(key, "")) for key in ("x", "y", "width", "height")
    )
    squares = []
    for polygon in features.get("square-fill", []):
        corners = tuple(
            ((float(x) - left) / width, (float(y) - top) / height)
            for x, y in (point.split(",") for point in polygon.get("points", "").split())
        )
        squares.append((polygon.get("fill", "#000000"), corners))
    if len(squares) != n:
        raise SystemExit(f"{rendering_path(n).name}: {len(squares)} squares, expected {n}")
    return Packing(n, tuple(squares))


def _number(value: float, digits: int) -> str:
    text = f"{value:.{digits}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def square_path(corners: Sequence[Point], *, scale: float, offset: float, digits: int) -> str:
    """One square as path data, with `H` and `V` for the edges rounding leaves axis-aligned."""
    points = [
        (_number(x * scale + offset, digits), _number(y * scale + offset, digits))
        for x, y in corners
    ]
    (x0, y0), *rest = points
    data = [f"M{x0} {y0}"]
    previous = (x0, y0)
    for x, y in rest:
        if y == previous[1]:
            data.append(f"H{x}")
        elif x == previous[0]:
            data.append(f"V{y}")
        else:
            data.append(f"L{x} {y}")
        previous = (x, y)
    data.append("Z")
    return "".join(data)


def fill_paths(
    packing: Packing, *, scale: float, offset: float = 0, digits: int = 0, extra: str = ""
) -> str:
    """One `<path>` per fill colour, in the order the colours first appear."""
    groups: dict[str, list[str]] = {}
    for fill, corners in packing.squares:
        groups.setdefault(fill, []).append(
            square_path(corners, scale=scale, offset=offset, digits=digits)
        )
    return "".join(
        f'<path fill="{fill}"{extra} d="{"".join(paths)}"/>' for fill, paths in groups.items()
    )


def _box(low: float, high: float, digits: int = 0) -> str:
    a, b = _number(low, digits), _number(high, digits)
    return f"M{a} {a}H{b}V{b}H{a}Z"


def hero_svg() -> str:
    """The `n = 53` packing, stripped of ids, titles and descriptions, to inline.

    It has a `viewBox` and no size, so CSS sizes it; its outlines are `currentColor`.
    """
    packing = read_packing(HERO_N)
    scale = DRAWING_SCALE
    pad = scale // 100
    keep = ' vector-effect="non-scaling-stroke"'
    return (
        f'<svg xmlns="{SVG_NS}" viewBox="{-pad} {-pad} {scale + 2 * pad} {scale + 2 * pad}"'
        f' role="img" aria-label="The best known packing of {HERO_N} unit squares"'
        f' fill="none" stroke="currentColor" stroke-width="{HERO_STROKE:g}"'
        ' stroke-linejoin="round">'
        f"{fill_paths(packing, scale=scale, extra=keep)}"
        f'<path{keep} d="{_box(0, scale)}"/></svg>'
    )


def thumbnail_path(n: int) -> str:
    """The site-relative path of case `n`'s thumbnail, for the frontier atlas page."""
    return f"thumbs/n-{n:03d}.svg"


def thumbnail_svg(n: int) -> str:
    """Case `n` as a small standalone drawing, for an `<img loading="lazy">`."""
    packing = read_packing(n)
    scale = DRAWING_SCALE
    pad = int(THUMBNAIL_STROKE // 2 + 1)
    return (
        f'<svg xmlns="{SVG_NS}" viewBox="{-pad} {-pad} {scale + 2 * pad} {scale + 2 * pad}"'
        f' stroke="#000" stroke-width="{THUMBNAIL_STROKE:g}" stroke-linejoin="round">'
        "<style>@media (prefers-color-scheme:dark){svg{stroke:"
        f"{THUMBNAIL_DARK_STROKE}}}}}</style>"
        f"{fill_paths(packing, scale=scale)}"
        f'<path fill="none" d="{_box(0, scale)}"/></svg>'
    )


@cache
def favicon_svg() -> str:
    """The site's favicon, inlined into every page as a data URI: `n = 11` on paper."""
    packing = read_packing(FAVICON_N)
    inner = FAVICON_SIZE - 2 * FAVICON_INSET
    return (
        f'<svg xmlns="{SVG_NS}" viewBox="0 0 {FAVICON_SIZE} {FAVICON_SIZE}"'
        f' stroke="{FAVICON_INK}" stroke-width="{FAVICON_STROKE:g}" stroke-linejoin="round">'
        f'<path fill="#fff" d="{_box(FAVICON_INSET, FAVICON_INSET + inner)}"/>'
        f"{fill_paths(packing, scale=inner, offset=FAVICON_INSET, digits=1)}</svg>"
    )


@cache
def _thumbnails() -> tuple[Asset, ...]:
    return tuple(
        Asset(thumbnail_path(n), thumbnail_svg(n).encode("utf-8")) for n in rendered_cases()
    )


def assets() -> Iterable[Asset]:
    """The preview PNGs, the film's poster, and a thumbnail for every case."""
    yield from (Asset(preview.image, image) for preview, image in _previews())
    yield Asset(POSTER, POSTER_SOURCE.read_bytes())
    yield from _thumbnails()
