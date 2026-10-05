"""The n = 11 series' figure vocabulary: one role, one ink, one drawing per object.

Papers II and III draw the same object the same way (plan
`plan-2026-10-05-n11-explainer-series.md` §6.1):

- the *container*, a neutral outline;
- a *parent*, a filled square;
- a *core*, a dashed inner square;
- a *point charge*, a dot whose area is proportional to its weight (Paper I's rule);
- a *k-of-m charge*, a thin hull through its m sites with a `k/m` badge;
- a *centre domain*, hatched.

Every role is painted in fixed ink on a light ground, as Paper III's diagrams are, so a
page that carries the site's theme control keeps a light ground under each of these
diagrams on the dark theme (the paper's stylesheet lists them; see
`test_a_diagram_drawn_in_fixed_ink_keeps_a_light_ground_on_the_dark_theme`). The four
family inks are the reference categorical slots of the data-visualisation palette, in
order, validated for adjacent and colour-blind separation on the light ground; two of
them sit below 3:1 against it, so every use carries a direct label.

`svg`, `text` and `polygon` are the helpers Paper III's three figure modules each keep a
copy of; `bound_ladder` draws the series bound ladder from the register. Labels use
only glyphs the shipped sans face carries: Γ, L₀, ≤, ≥ and subscripts are a caption's.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from html import escape
from pathlib import Path
from typing import Any

from sqpack.yamlio import load_yaml

PACKING = Path(__file__).resolve().parents[1]
RESULTS = PACKING / "frontier/results.yaml"
SVG_NS = "http://www.w3.org/2000/svg"

#: The widest a series figure is drawn, in CSS pixels: a phone's column holds it whole.
PHONE_WIDTH = 390

#: Fixed inks. Text wears `INK` or `MUTED`, never a family colour.
INK = "#172b3a"
MUTED = "#52667a"
RULE = "#cbd5e1"
GROUND = "#ffffff"
#: A paid core, a highlighted rung, a minimiser: the one accent.
ACCENT = "#1d7874"
PARENT_FILL = "#dcebef"

#: One ink per charge family, in the palette's fixed categorical order.
FAMILY_INKS: dict[str, str] = {
    "point": "#2a78d6",
    "2-of-3": "#eb6834",
    "2-of-5": "#1baf7a",
    "3-of-5": "#eda100",
}


@dataclass(frozen=True, slots=True)
class Role:
    """How one object of the series vocabulary is painted."""

    fill: str
    stroke: str
    width: float
    dash: str = ""
    fill_opacity: float = 1.0

    def attributes(self) -> str:
        parts = [f'fill="{self.fill}"']
        if self.fill != "none" and self.fill_opacity != 1:
            parts.append(f'fill-opacity="{self.fill_opacity:g}"')
        parts.append(f'stroke="{self.stroke}"')
        if self.stroke != "none":
            parts.append(f'stroke-width="{self.width:g}"')
            parts.append('stroke-linejoin="round"')
        if self.dash:
            parts.append(f'stroke-dasharray="{self.dash}"')
        return " ".join(parts)


CONTAINER = Role("none", MUTED, 1.5)
PARENT = Role(PARENT_FILL, ACCENT, 1.25)
CORE = Role("none", INK, 1.5, dash="5 3")
PAID_CORE = Role(ACCENT, ACCENT, 1.75, dash="5 3", fill_opacity=0.08)
UNPAID_CORE = Role("none", MUTED, 1.5, dash="2 3")
POINT_CHARGE = Role(FAMILY_INKS["point"], "none", 0)
DOMAIN_STROKE = MUTED


def hull_role(family: str) -> Role:
    """A k-of-m charge's hull: a thin stroke in its family's ink over a faint wash."""
    ink = FAMILY_INKS[family]
    return Role(ink, ink, 1.25, fill_opacity=0.1)


def svg(
    identifier: str,
    title: str,
    description: str,
    *,
    width: float,
    height: float,
    body: str,
    origin: tuple[float, float] = (0, 0),
    defs: str = "",
) -> str:
    """One diagram, `width` by `height` from `origin` in the coordinates it is drawn in.

    A diagram carries its labels and nothing else: its title and what a sentence says of
    it are the figure's caption. The class `n11-<identifier>` names it to the paper's
    stylesheet, which gives each fixed-ink diagram its light ground."""
    if width > PHONE_WIDTH:
        raise ValueError(f"{identifier}: {width} px is wider than a phone's column")
    title_id = f"n11-{identifier}-title"
    desc_id = f"n11-{identifier}-desc"
    left, top = origin
    defs_block = f"<defs>{defs}</defs>" if defs else ""
    return (
        f'<svg xmlns="{SVG_NS}" class="n11-diagram n11-{identifier}" '
        f'width="{width:g}" height="{height:g}" '
        f'viewBox="{left:g} {top:g} {width:g} {height:g}" role="img" '
        f'aria-labelledby="{title_id} {desc_id}">'
        f'<title id="{title_id}">{escape(title)}</title>'
        f'<desc id="{desc_id}">{escape(description)}</desc>'
        f"{defs_block}{body}</svg>"
    )


def text(
    x: float,
    y: float,
    value: str,
    *,
    note: bool = False,
    anchor: str = "start",
    fill: str = INK,
    attributes: str = "",
    halo: bool = False,
) -> str:
    """A label (bold) or a note (light) at `x`, `y`; never a sentence. A `halo` keeps
    it legible over hatching or a raster."""
    role = "n11-diagram-note" if note else "n11-diagram-label"
    extra = f" {attributes}" if attributes else ""
    if halo:
        extra += (
            f' stroke="{GROUND}" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'
        )
    return (
        f'<text class="{role}" x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
        f'fill="{fill}"{extra}>{escape(value)}</text>'
    )


def polygon(points: Iterable[tuple[float, float]], role: Role, *, attributes: str = "") -> str:
    """A closed polygon through pixel `points`, painted in `role`."""
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    extra = f" {attributes}" if attributes else ""
    return f'<polygon points="{coords}" {role.attributes()}{extra}/>'


def line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    stroke: str = MUTED,
    width: float = 1,
    dash: str = "",
) -> str:
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{stroke}" stroke-width="{width:g}"{dashed}/>'
    )


def rect(
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    fill: str,
    stroke: str = "none",
    attributes: str = "",
) -> str:
    extra = f" {attributes}" if attributes else ""
    stroked = f' stroke="{stroke}"' if stroke != "none" else ""
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
        f'fill="{fill}"{stroked}{extra}/>'
    )


@dataclass(frozen=True, slots=True)
class Frame:
    """Exact plane coordinates to pixels: `(x0, y0)` lands at pixel `(left, bottom)`,
    `scale` pixels per unit, y up. Rationals become floats only here."""

    left: float
    bottom: float
    scale: float
    x0: Fraction | float = 0
    y0: Fraction | float = 0

    def __call__(self, point: Sequence[Fraction | float]) -> tuple[float, float]:
        x, y = point[0], point[1]
        return (
            self.left + self.scale * float(x - self.x0),
            self.bottom - self.scale * float(y - self.y0),
        )


def square_corners(
    centre: tuple[Fraction, Fraction], side: Fraction, cosine: Fraction, sine: Fraction
) -> list[tuple[Fraction, Fraction]]:
    """The four corners of a closed square of `side` about `centre`, turned by the
    rotation with exact `cosine` and `sine`."""
    half = side / 2
    cx, cy = centre
    return [
        (cx + cosine * u - sine * v, cy + sine * u + cosine * v)
        for u, v in ((-half, -half), (half, -half), (half, half), (-half, half))
    ]


def convex_hull(points: Sequence[tuple[float, float]]) -> list[tuple[float, float]]:
    """The convex hull of pixel points, counter-clockwise (monotone chain)."""
    ordered = sorted(set(points))
    if len(ordered) <= 2:
        return ordered

    def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[float, float]] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def point_charge(x: float, y: float, radius: float, *, attributes: str = "") -> str:
    """A point charge: a dot whose area the caller makes proportional to its weight."""
    extra = f" {attributes}" if attributes else ""
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" '
        f"{POINT_CHARGE.attributes()}{extra}/>"
    )


def site(x: float, y: float, family: str, *, attributes: str = "") -> str:
    """A site of a k-of-m charge: a small ring in its family's ink."""
    extra = f" {attributes}" if attributes else ""
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="{GROUND}" '
        f'stroke="{FAMILY_INKS[family]}" stroke-width="1.75"{extra}/>'
    )


def badge(x: float, y: float, threshold: int, size: int) -> str:
    """The `k/m` badge of a k-of-m charge, centred at `x`, `y`."""
    label = f"{threshold}/{size}"
    family = f"{threshold}-of-{size}"
    return (
        f'<rect x="{x - 17:.2f}" y="{y - 11:.2f}" width="34" height="20" rx="10" '
        f'fill="{GROUND}" stroke="{FAMILY_INKS[family]}" stroke-width="1.5"/>'
        + text(x, y + 4.5, label, note=True, anchor="middle", attributes='data-badge="1"')
    )


def hull(
    points: Sequence[tuple[float, float]],
    threshold: int,
    *,
    badge_at: tuple[float, float],
    attributes: str = "",
) -> str:
    """A k-of-m charge: a thin hull through its sites, the sites, and its `k/m` badge."""
    size = len(points)
    family = f"{threshold}-of-{size}"
    outline = convex_hull(points)
    drawn = (
        polygon(outline, hull_role(family), attributes=attributes)
        if len(outline) > 2
        else line(*outline[0], *outline[-1], stroke=FAMILY_INKS[family], width=1.25)
    )
    return (
        drawn
        + "".join(site(x, y, family) for x, y in points)
        + badge(*badge_at, threshold, size)
    )


def hatch(pattern_id: str) -> str:
    """The centre domain's hatching, as a pattern its diagram declares once."""
    return (
        f'<pattern id="{pattern_id}" width="6" height="6" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">'
        f'<rect width="6" height="6" fill="{GROUND}"/>'
        f'<line x1="0" y1="0" x2="0" y2="6" stroke="{DOMAIN_STROKE}" stroke-width="1"/>'
        "</pattern>"
    )


def domain(
    points: Iterable[tuple[float, float]], pattern_id: str, *, attributes: str = ""
) -> str:
    """A centre domain, hatched with the pattern `pattern_id`."""
    return polygon(
        points,
        Role(f"url(#{pattern_id})", DOMAIN_STROKE, 1.25),
        attributes=attributes,
    )


def count(value: int) -> str:
    """An integer as the papers print one: 12,028."""
    return f"{value:,}"


def decimal(value: Fraction, places: int) -> str:
    """`value` rounded half away from zero to `places` decimals, exactly."""
    scale = 10**places
    scaled = abs(value) * scale
    whole = int(scaled)
    if scaled - whole >= Fraction(1, 2):
        whole += 1
    sign = "-" if value < 0 and whole else ""
    digits = str(whole).rjust(places + 1, "0")
    if not places:
        return f"{sign}{digits}"
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def exact_decimal(value: Fraction) -> str:
    """A rational with a terminating decimal expansion, written out in full."""
    places = 0
    while (value * 10**places).denominator != 1:
        places += 1
        if places > 40:
            raise ValueError(f"{value} has no short terminating decimal")
    return decimal(value, places)


def percent(value: Fraction) -> str:
    return f"{decimal(100 * value, 0)}%"


def power_of_ten(value: Fraction) -> str:
    """`10⁻¹²` for 1/10¹²: only an exact power of ten is written this way."""
    superscript = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    exponent = 0
    probe = value
    while probe < 1:
        probe *= 10
        exponent -= 1
    while probe > 1:
        probe /= 10
        exponent += 1
    if probe != 1:
        raise ValueError(f"{value} is not a power of ten")
    return f"10{str(exponent).translate(superscript)}"


def scientific(value: Fraction, digits: int = 2) -> str:
    """`3.6 x 10⁻⁹`, with a multiplication sign: `value` to `digits` significant
    figures, exactly rounded."""
    if value <= 0:
        raise ValueError("scientific notation here is for positive values")
    exponent = 0
    mantissa = value
    while mantissa >= 10:
        mantissa /= 10
        exponent += 1
    while mantissa < 1:
        mantissa *= 10
        exponent -= 1
    written = decimal(mantissa, digits - 1)
    if written.startswith("10"):
        written = decimal(Fraction(1), digits - 1)
        exponent += 1
    superscript = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{written} \N{MULTIPLICATION SIGN} 10{str(exponent).translate(superscript)}"


# The series bound ladder ------------------------------------------------------------

#: The ladder's rungs in order, bottom to top. A rung may carry a second result that
#: stands at the same place in the order: T-061 is T-037's certificate reweighted, about
#: 3.9e-9 above it.
LADDER_RUNGS: tuple[tuple[str, *tuple[str, ...]], ...] = (
    ("T-010",),
    ("T-018",),
    ("T-025",),
    ("T-026",),
    ("T-033",),
    ("T-037", "T-061"),
    ("T-060",),
)
#: The register records the ladder reads, pinned: every rung's headline, and the claim of
#: one whose headline states no value (T-060's names the packing).
#: A changed headline must be read before the ladder redraws it. Recompute with
#: `ladder_digest(ladder_records())` after reviewing the change.
LADDER_DIGEST = "cac7d8e21c3078d49dc46daa73a9766547505bbf102cfb2351b7909ee9e704c1"
#: Decimals a rung shows: a long expansion is cut, a short one is kept as written, so
#: T-061's 3.875000003875… stays apart from 31/8.
LADDER_CUT = 7
LADDER_KEEP = 12


_DECIMAL = re.compile(r"= (\d+\.\d+)(…|\.\.\.)?")
_SURD = re.compile(r"`s\(11\) ≥ (\d+) \+ (\d+)/√(\d+)`")


def ladder_records(path: Path = RESULTS) -> dict[str, dict[str, str]]:
    """The headline and claim of every rung's result, from the register."""
    register: dict[str, Any] = load_yaml(path.read_text(encoding="utf-8"))
    wanted = {identifier for rung in LADDER_RUNGS for identifier in rung}
    records: dict[str, dict[str, str]] = {}
    for row in register["results"]:
        if row.get("id") not in wanted:
            continue
        record = {"headline": str(row["headline"])}
        # Where the headline states no value, the claim's first decimal is read, and only
        # it is pinned: the rest of a claim is prose the register may reword.
        if _DECIMAL.search(record["headline"]) is None and not _SURD.search(record["headline"]):
            found = _DECIMAL.search(str(row["claim"]))
            if found is None:
                raise ValueError(f"{row['id']} states no value for the ladder")
            record["claim"] = found.group(0)
        records[str(row["id"])] = record
    missing = wanted - set(records)
    if missing:
        raise ValueError(f"the register lacks ladder results {sorted(missing)}")
    return records


def ladder_digest(records: dict[str, dict[str, str]]) -> str:
    canonical = json.dumps(records, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()


def ladder_value(record: dict[str, str]) -> str:
    """The value a rung shows, read from its headline, or from its claim when the
    headline states none (T-060's names the packing; T-010's is a surd)."""
    for source in (record["headline"], record.get("claim", "")):
        found = _DECIMAL.search(source)
        if found is not None:
            digits, cut = found.group(1), found.group(2)
            whole, places = digits.split(".")
            if len(places) > LADDER_KEEP:
                return f"{whole}.{places[:LADDER_CUT]}…"
            return digits + ("…" if cut else "")
    surd = _SURD.search(record["headline"])
    if surd is None:
        raise ValueError(f"no value in ladder headline {record['headline']!r}")
    whole, numerator, radicand = (int(group) for group in surd.groups())
    with localcontext() as context:
        context.prec = 40
        value = Decimal(whole) + Decimal(numerator) / Decimal(radicand).sqrt()
    places = str(value).split(".")[1]
    return f"{whole + int(value - whole)}.{places[:LADDER_CUT]}…"


def bound_ladder(highlight: str, *, identifier: str = "ladder", path: Path = RESULTS) -> str:
    """The series bound ladder: the n = 11 lower bounds and T, evenly spaced, with no
    linear axis (on one, T-037 to T is 0.0021 of the range and T-037 to T-061 is
    3.9e-9), each rung labelled with its register id and headline value. The rung
    holding `highlight` is drawn in the accent."""
    records = ladder_records(path)
    if ladder_digest(records) != LADDER_DIGEST:
        raise ValueError("changed figure input: the ladder's register records changed")
    if not any(highlight in rung for rung in LADDER_RUNGS):
        raise ValueError(f"{highlight} is not on the ladder")
    width, gap, top = 360, 50, 34
    rail = 46
    bottom = top + gap * (len(LADDER_RUNGS) - 1)
    parts = [line(rail, top, rail, bottom, stroke=RULE, width=3)]
    for level, rung in enumerate(LADDER_RUNGS):
        y = bottom - gap * level
        lit = highlight in rung
        ink = ACCENT if lit else MUTED
        if lit:
            parts.append(
                rect(
                    rail + 10,
                    y - 21,
                    width - rail - 18,
                    42 if len(rung) > 1 else 30,
                    fill=ACCENT,
                    attributes='fill-opacity="0.08" rx="8"',
                )
            )
        parts.append(
            f'<circle cx="{rail}" cy="{y:.2f}" r="{7 if lit else 5}" fill="{ink}" '
            f'data-rung="{rung[0]}"/>'
        )
        for offset, identifier_ in enumerate(rung):
            value = ladder_value(records[identifier_])
            row = y + 5 + 18 * offset
            parts.append(
                text(
                    rail + 20,
                    row,
                    identifier_,
                    note=offset > 0,
                    attributes=f'data-result="{identifier_}"',
                )
                + text(
                    rail + 92,
                    row,
                    value,
                    note=offset > 0,
                    attributes=f'data-value="{identifier_}"',
                )
            )
    return svg(
        identifier,
        "The n = 11 bound ladder",
        "The verified lower bounds for eleven squares and the optimum T, bottom to top: "
        + ", ".join(
            f"{rid} {ladder_value(records[rid])}" for rung in LADDER_RUNGS for rid in rung
        )
        + f". Rungs are evenly spaced, not to scale; {highlight} is highlighted.",
        width=width,
        height=bottom + 34,
        body="".join(parts),
    )
