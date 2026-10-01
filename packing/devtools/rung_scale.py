#!/usr/bin/env python3
"""The rung chips' colour scale as the stylesheet makes it: every fill, and the contrast
of the chip's text on it.

A rung chip's fill is one rule in `templates/site.css`,
`oklch(base + level * step, chroma-base + level * chroma-step, hue)`, from four tokens a
theme sets and a hue (and, for significance, a flat chroma) a ladder sets. This reads
those tokens from the stylesheet, the page's text and background colours from kpress's
own, and the levels of each ladder from `epistemics.md`, and reports each rung in each
theme: the fill in OkLCh and as sRGB hex, whether sRGB holds it, and the WCAG contrast
ratio of the page's text on it.

It needs no browser. `tests/test_rung_scale.py` holds the scale to what the design
system says of it (`templates/paper-design.md`, Color): saturation and strength rise
with the level, every fill is in gamut, and the text keeps 4.5:1 on every one. The same
test holds the table in that document to this tool's output.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.rung_scale
"""

from __future__ import annotations

import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from devtools.overview_sections import rubric_levels
from devtools.render_explainer import kpress_static
from devtools.render_overview import SITE_CSS
from sqpack.render.color import (
    _linear_to_srgb,  # pyright: ignore[reportPrivateUsage]
    _maximum_chroma,  # pyright: ignore[reportPrivateUsage]
    _oklch_linear_rgb,  # pyright: ignore[reportPrivateUsage]
)

#: The ladders in the order the site lists them, significance first.
LADDERS = ("S", "V", "C")
THEMES = ("light", "dark")
#: WCAG 2 AA for body text, which a chip's label is.
MINIMUM_CONTRAST = 4.5

_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
_BLOCK = re.compile(r"([^{}]+)\{([^{}]*)\}")
_DECLARATION = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")
_OKLCH = re.compile(r"oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*\)")
_VAR = re.compile(r"var\((--[\w-]+)\)")

Oklch = tuple[float, float, float]


@dataclass(frozen=True)
class Fill:
    """One rung's chip in one theme."""

    theme: str
    rung: str
    lightness: float
    chroma: float
    hue: float
    hex: str
    in_gamut: bool
    contrast: float

    @property
    def level(self) -> int:
        return int(self.rung[1:])

    @property
    def scale(self) -> str:
        return self.rung[0]

    @property
    def oklch(self) -> str:
        return f"oklch({self.lightness * 100:.1f}% {self.chroma:.3f} {self.hue:g})"


def _blocks(css: Path) -> list[tuple[str, dict[str, str]]]:
    """A stylesheet's rules as (selector, custom properties), comments dropped."""
    text = _COMMENT.sub("", css.read_text(encoding="utf-8"))
    return [
        (" ".join(selector.split()), dict(_DECLARATION.findall(body)))
        for selector, body in _BLOCK.findall(text)
    ]


def _is_dark(selector: str) -> bool:
    return 'data-kpress-resolved-theme="dark"' in selector


def _number(value: str) -> float:
    value = value.strip()
    return float(value[:-1]) / 100 if value.endswith("%") else float(value)


def theme_tokens() -> dict[str, dict[str, str]]:
    """Each theme's `--site-rung-*` tokens, from the rule that sets the scale."""
    themes: dict[str, dict[str, str]] = {}
    for selector, declared in _blocks(SITE_CSS):
        if "--site-rung-base" not in declared:
            continue
        theme = "dark" if _is_dark(selector) else "light"
        if theme in themes:
            raise SystemExit(f"site.css sets the {theme} rung scale twice")
        themes[theme] = {
            name: value for name, value in declared.items() if name.startswith("--site-rung-")
        }
    if set(themes) != set(THEMES):
        raise SystemExit(f"site.css sets the rung scale for {sorted(themes)}, not both themes")
    return themes


def ladder_tokens() -> dict[str, dict[str, str]]:
    """Each ladder's `--rung-*` properties: the rule's own, then the ladder's."""
    rules = dict(_blocks(SITE_CSS))
    shared = rules.get(".site-rung-fill")
    if not shared:
        raise SystemExit("site.css has no .site-rung-fill rule")
    return {
        scale: shared | rules.get(f'.site-rung-fill[data-rung="{scale}"]', {})
        for scale in LADDERS
    }


def styled_levels() -> set[int]:
    """The levels `site.css` gives a fill of their own: 0, and each `data-level` rule."""
    levels = {0}
    for selector, declared in _blocks(SITE_CSS):
        match = re.fullmatch(r'\.site-rung-fill\[data-level="(\d+)"\]', selector)
        if match and declared.get("--rung-level") == match.group(1):
            levels.add(int(match.group(1)))
    return levels


def page_colours() -> dict[str, dict[str, Oklch]]:
    """The page's text and background in each theme, from kpress's neutral palette."""
    found: dict[str, dict[str, Oklch]] = {}
    for selector, declared in _blocks(kpress_static() / "css" / "style-tokens.css"):
        if "--kpress-doc-text" not in declared or "data-kpress-palette" in selector:
            continue
        theme = "dark" if _is_dark(selector) else "light"
        colours: dict[str, Oklch] = {}
        for role in ("text", "bg"):
            match = _OKLCH.fullmatch(declared[f"--kpress-doc-{role}"].strip())
            if not match:
                raise SystemExit(f"kpress's {theme} {role} colour is not an oklch() value")
            lightness, chroma, hue = (float(part) for part in match.groups())
            colours[role] = (lightness / 100, chroma, hue)
        found.setdefault(theme, colours)
    if set(found) != set(THEMES):
        raise SystemExit("kpress's style tokens do not state both themes' page colours")
    return found


def luminance(colour: Oklch) -> float:
    """WCAG relative luminance of an OkLCh colour, clipped to sRGB as a browser shows it."""
    red, green, blue = (min(1.0, max(0.0, channel)) for channel in _oklch_linear_rgb(*colour))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first: Oklch, second: Oklch) -> float:
    """The WCAG 2 contrast ratio of two colours."""
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def hex_colour(colour: Oklch) -> str:
    """An OkLCh colour as the sRGB hex a browser shows it as, clipped to the gamut."""
    channels = (
        round(_linear_to_srgb(min(1.0, max(0.0, channel))) * 255)
        for channel in _oklch_linear_rgb(*colour)
    )
    return "#" + "".join(f"{channel:02x}" for channel in channels)


def fills() -> list[Fill]:
    """Every rung of every ladder in each theme, in the site's order, lowest level first."""
    themes = theme_tokens()
    ladders = ladder_tokens()
    pages = page_colours()
    levels = rubric_levels()
    report = []
    for theme in THEMES:
        tokens = themes[theme]

        def value(declared: str, tokens: dict[str, str] = tokens) -> float:
            reference = _VAR.fullmatch(declared.strip())
            return _number(tokens[reference.group(1)] if reference else declared)

        for scale in LADDERS:
            ladder = ladders[scale]
            hue = _number(ladder["--rung-hue"])
            for level, _meaning in sorted(levels[scale]):
                colour = (
                    value("var(--site-rung-base)") + level * value("var(--site-rung-step)"),
                    value(ladder["--rung-chroma-base"])
                    + level * value(ladder["--rung-chroma-step"]),
                    hue,
                )
                report.append(
                    Fill(
                        theme=theme,
                        rung=f"{scale}{level}",
                        lightness=colour[0],
                        chroma=colour[1],
                        hue=hue,
                        hex=hex_colour(colour),
                        in_gamut=colour[1] <= _maximum_chroma(colour[0], hue),
                        contrast=contrast(pages[theme]["text"], colour),
                    )
                )
    return report


def markdown_table(report: Sequence[Fill]) -> str:
    """The scale as the design document carries it: one row a rung, a theme a pair of
    columns, the fill in OkLCh with its hex and the text's contrast on it."""
    by_rung: dict[str, dict[str, Fill]] = {}
    for fill in report:
        by_rung.setdefault(fill.rung, {})[fill.theme] = fill
    lines = [
        "| Rung | Light fill | Text contrast | Dark fill | Text contrast |",
        "| --- | --- | --- | --- | --- |",
    ]
    for rung, themed in by_rung.items():
        cells = [f"`{rung}`"]
        for theme in THEMES:
            fill = themed[theme]
            cells += [f"`{fill.oklch}` `{fill.hex}`", f"{fill.contrast:.1f}:1"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        raise SystemExit(__doc__)
    report = fills()
    print(markdown_table(report))
    pages = page_colours()
    for theme in THEMES:
        print(f"{theme}: text on the page background {contrast(*pages[theme].values()):.1f}:1")
    failed = [fill for fill in report if not fill.in_gamut or fill.contrast < MINIMUM_CONTRAST]
    for fill in failed:
        print(
            f"{fill.theme} {fill.rung}: {fill.oklch} "
            f"{'in' if fill.in_gamut else 'out of'} gamut, {fill.contrast:.2f}:1",
            file=sys.stderr,
        )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
