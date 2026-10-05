"""Source-bound explanatory SVGs for the n=11 optimality paper.

The pictures round exact coordinates only at the final pixel conversion. They
explain reviewed proof steps; rendering is not another geometry verifier.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction as Q
from html import escape
from pathlib import Path
from typing import Any

from devtools import check_n11_generic_fresh as fresh
from devtools import check_n11_optimality_d4 as d4
from devtools import check_n11_optimality_field_mask0 as field

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/n11-optimality-2026-09-29/receipts"
GENERIC = PACKET / "generic-mask2095-intake"
FIELD = PACKET / "field-mask0"
D4 = PACKET / "d4-independent"
SVG_NS = "http://www.w3.org/2000/svg"

GENERIC_DECODED_SHA = "68adba943c66ee60c65caf8094dfc18f68a622379acf506ed40558f87602f8aa"
GENERIC_PACKED_SHA = "800d8684bb856727acedbf438a27f57918c8ecd679c3df979e30ad826c590594"
GENERIC_RESULT_SHA = "2aa9c3819e4f39d9f4f489a25d1885b2a1c5a6f6c21099f42821d1165d608f88"
GENERIC_PROVENANCE_SHA = "81806b15f568ca6a3bd9843e0fa36387e8aa955c67071d278c47e1e50dd65b06"
GENERIC_CHECKER_SHA = "e8fcfd02560d09e7a2a5b2622976ab021ef15a4456a2824b37abae926f6ab7d3"
FIELD_AUDIT_SHA = "1a56056ad4d19786e41e248f0ef60866ad2021370e9ef809faa471fb679f8a54"
FIELD_RESULT_SHA = "821274111e6eb50d47e20882da083e3e23d25ee37e6725a18b18d133ab798663"
D4_COVER_SHA = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
D4_OVERLAY_SHA = "845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700"
D4_DISTANCE_SHA = "4f960f4001faa6c9c1e7521f3a2344f71e10b41cd38a6425f6821cc1fd2ccd47"
D4_RESULT_SHA = "c4aa4df460593abcb51cd4ebaaf916c78a6a718659bb6b7bf4245e3e67e6c00e"
D4_CHECKER_SHA = "19f4b0a47afd6acb327e85bd4a98ca2a43d2fdaa49aeb0edd30aa12d1b6aac1d"
FIELD_CHECKER_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"

RENDER_INPUTS = (
    Path(__file__),
    Path(fresh.__file__),
    Path(d4.__file__),
    Path(field.__file__),
    GENERIC / "provenance.json",
    GENERIC / "full-result.json",
    GENERIC / "objects" / f"{GENERIC_DECODED_SHA}.gz",
    FIELD / "result.json",
    FIELD / "objects" / f"{FIELD_AUDIT_SHA}.gz",
    D4 / "result.json",
    D4 / "objects" / f"{D4_COVER_SHA}.gz",
    D4 / "objects" / f"{D4_OVERLAY_SHA}.gz",
    D4 / "objects" / f"{D4_DISTANCE_SHA}.gz",
)

Point = tuple[Q, Q]
Polygon = list[Point]


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: Path, sha: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    if sha is not None and _hash(raw) != sha:
        raise ValueError(f"changed figure input: {path}")
    value: dict[str, Any] = json.loads(raw)
    return value


def _read_object(
    directory: Path, decoded_sha: str, *, packed_sha: str | None = None
) -> dict[str, Any]:
    packed = (directory / f"{decoded_sha}.gz").read_bytes()
    if packed_sha is not None and _hash(packed) != packed_sha:
        raise ValueError("changed compressed figure object")
    raw = gzip.decompress(packed)
    if _hash(raw) != decoded_sha:
        raise ValueError("changed exact figure object")
    value: dict[str, Any] = json.loads(raw)
    return value


def _pin_checker(path: Path, sha: str) -> None:
    if _hash(path.read_bytes()) != sha:
        raise ValueError(f"figure's accepted checker changed: {path}")


def _svg(
    name: str, title: str, description: str, *, width: int, height: int, body: str, top: int = 0
) -> str:
    """One diagram, its canvas from `top` down `height` of the coordinates its parts are
    drawn in. A diagram carries its labels and nothing else: its title and whatever a
    sentence says of it are the figure's caption, in the article."""
    title_id, desc_id = f"n11-mechanism-{name}-title", f"n11-mechanism-{name}-desc"
    return (
        f'<svg xmlns="{SVG_NS}" class="n11-diagram n11-mechanism-{name}" '
        f'width="{width}" height="{height}" viewBox="0 {top} {width} {height}" '
        f'role="img" aria-labelledby="{title_id} {desc_id}">'
        f'<title id="{title_id}">{escape(title)}</title>'
        f'<desc id="{desc_id}">{escape(description)}</desc>{body}</svg>'
    )


def _text(x: float, y: float, value: str, *, note: bool = False, anchor: str = "start") -> str:
    cls = "n11-diagram-note" if note else "n11-diagram-label"
    return (
        f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" '
        f'text-anchor="{anchor}" fill="#172b3a">{escape(value)}</text>'
    )


def _polygon(
    points: Polygon,
    x: float,
    y: float,
    scale: float,
    origin: Point,
    *,
    fill: str,
    stroke: str = "#203b50",
    opacity: float = 1,
    tag: str = "",
) -> str:
    coords = " ".join(
        f"{x + scale * float(px - origin[0]):.3f},{y - scale * float(py - origin[1]):.3f}"
        for px, py in points
    )
    return (
        f'<polygon {tag} points="{coords}" fill="{fill}" fill-opacity="{opacity:.2f}" '
        f'stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
    )


def _pose_svg() -> str:
    # This is a lemma schematic: the upper possible-center region is an outer
    # enclosure; the lower Q polygon consists of offsets inside physical squares.
    body = [
        '<rect x="24" y="54" width="330" height="245" rx="8" fill="#f8fafc" stroke="#94a3b8"/>',
        (
            '<rect x="386" y="54" width="330" height="245" rx="8" '
            'fill="#f8fafc" stroke="#94a3b8"/>'
        ),
        _text(40, 42, "Candidate center positions"),
        _text(402, 42, "Offsets inside each physical square"),
        (
            '<path d="M65 220 L100 108 L278 105 L322 228 Z" '
            'fill="#dcebef" stroke="#1d7874" stroke-width="2"/>'
        ),
        (
            '<path d="M114 183 L155 135 L255 148 L274 212 L175 240 Z" '
            'fill="#f5bf65" fill-opacity=".65" stroke="#a15a00" stroke-width="2"/>'
        ),
        '<circle cx="210" cy="189" r="5" fill="#172b3a"/>',
        _text(71, 278, "D: possible centers", note=True),
        _text(139, 171, "K \N{MINUS SIGN} Q", note=True),
        (
            '<rect x="510" y="151" width="86" height="86" '
            'fill="#e2e8f0" stroke="#52667a" stroke-width="2"/>'
        ),
        (
            '<path d="M527 194 L553 168 L579 194 L553 220 Z" '
            'fill="#f5bf65" stroke="#a15a00" stroke-width="2"/>'
        ),
        _text(513, 279, "Q: strict core offsets", note=True),
    ]
    return _svg(
        "pose",
        "Possible centers and guaranteed strict cores",
        "Schematic of the ownership collision lemma. D and K minus Q are center-position "
        "regions; Q contains offsets relative to a square center. The implication concerns "
        "valid packings under accepted prior ownership and a whole-angle strict Q core.",
        width=740,
        height=312,
        body="".join(body),
    )


def _admitted_row() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _pin_checker(Path(fresh.__file__), GENERIC_CHECKER_SHA)
    _pin_checker(Path(field.__file__), FIELD_CHECKER_SHA)
    provenance = _read_json(GENERIC / "provenance.json", GENERIC_PROVENANCE_SHA)
    result = _read_json(GENERIC / "full-result.json", GENERIC_RESULT_SHA)
    source = _read_object(
        GENERIC / "objects", GENERIC_DECODED_SHA, packed_sha=GENERIC_PACKED_SHA
    )
    if (
        provenance.get("result_sha256") != GENERIC_RESULT_SHA
        or provenance.get("checker_sha256") != GENERIC_CHECKER_SHA
        or result.get("status") != "PASS_ONE_GENERIC_EXCLUSION"
        or result.get("geometry_verified") is not True
        or result.get("rows_checked") != 160
        or result.get("steps_completed") != 5
        or result.get("source_sha256", {}).get("source") != GENERIC_PACKED_SHA
        or source.get("mask_index") != 2095
        or len(source.get("steps", [])) != 5
    ):
        raise ValueError("accepted case-2095 row binding changed")
    step = source["steps"][1]
    row = step["rows"][17]
    if (
        step["owner"] != 10
        or step["complete"] is not True
        or len(step["rows"]) != 32
        or row["interval"] != ["17/32", "9/16"]
        or row["prior_reference"] != {"kind": "wall_seed", "owner": 10, "row": 17}
        or row["reference"]
        != {
            "kind": "phase3",
            "node": "mask2095-hull-first-v5",
            "step": 1,
            "row": 17,
        }
        or row["collision_regions"] != []
    ):
        raise ValueError("case-2095 selected row changed")
    return source, step, row


def complete_obstacles_for_display(clipped: dict[int, d4.Polygon]) -> dict[int, d4.Polygon]:
    """Retain every closed obstacle contact or refuse a shape this SVG cannot depict."""
    if any(0 < len(poly) < 3 for poly in clipped.values()):
        raise ValueError("worked row has a closed lower-dimensional obstacle contact")
    return {owner: poly for owner, poly in clipped.items() if poly}


def _row_svg() -> str:
    _, step, row = _admitted_row()
    domain = fresh.convex(row["input_domain"])
    core = fresh.convex(row["core_vertices"])
    residual = [fresh.convex(item) for item in row["residual_polygons"]]
    if len(domain) != 6 or len(core) != 8 or len(residual) != 1 or len(residual[0]) != 3:
        raise ValueError("case-2095 worked-row polygon census changed")
    prior = {int(k): fresh.convex(v) for k, v in step["prior_owned_hulls"].items()}
    if set(prior) != set(fresh.MASK):
        raise ValueError("worked-row predecessor hull inventory changed")
    forbidden = {
        owner: fresh.hull([(px - qx, py - qy) for px, py in group for qx, qy in core])
        for owner, group in prior.items()
        if owner != 10
    }
    clipped = {
        owner: d4.intersection(tuple(poly), tuple(domain)) for owner, poly in forbidden.items()
    }
    active = complete_obstacles_for_display(clipped)
    if set(active) != {6, 11, 14}:
        raise ValueError("worked-row obstacle intersection changed")
    # All positions use the same exact-coordinate affine display map.
    low_x = min(p[0] for p in domain)
    high_x = max(p[0] for p in domain)
    low_y = min(p[1] for p in domain)
    high_y = max(p[1] for p in domain)
    mid = ((low_x + high_x) / 2, (low_y + high_y) / 2)
    scale = 178 / max(float(high_x - low_x), float(high_y - low_y))
    panels = [(20, 58), (380, 58), (20, 348), (380, 348)]
    body: list[str] = []
    for x, y in panels:
        body.append(
            f'<rect x="{x}" y="{y}" width="330" height="252" rx="8" '
            'fill="#f8fafc" stroke="#94a3b8"/>'
        )
    body += [
        _text(34, 42, "1 · Possible centers"),
        _text(394, 42, "2 · Core and owned hull"),
        _text(34, 332, "3 · Forbidden centers"),
        _text(394, 332, "4 · Retained triangle"),
    ]
    # Panel 1 and 3: center-position coordinates, never Q-offset coordinates.
    body.append(
        _polygon(
            domain, 185, 195, scale, mid, fill="#dcebef", tag='data-row-domain="2095-1-10-17"'
        )
    )
    body.append(_polygon(domain, 185, 485, scale, mid, fill="#f8fafc"))
    colors = {6: "#db7458", 11: "#c98e33", 14: "#b35f8d"}
    for owner, poly in active.items():
        body.append(
            _polygon(
                list(poly),
                185,
                485,
                scale,
                mid,
                fill=colors[owner],
                opacity=0.45,
                tag=f'data-obstacle-owner="{owner}"',
            )
        )
    body.append(
        _polygon(
            residual[0], 185, 485, scale, mid, fill="#1d7874", tag='data-residual-vertices="3"'
        )
    )
    # Panel 2 intentionally uses different origins: Q is an offset; K is owned interior.
    offset_scale = 70
    body.append(
        _polygon(
            core,
            545,
            175,
            offset_scale,
            (Q(), Q()),
            fill="#f5bf65",
            tag='data-core-vertices="8"',
        )
    )
    body.append(
        _polygon(
            prior[11],
            545,
            255,
            380,
            (Q(147, 50), Q(11, 5)),
            fill="#dcebef",
            tag='data-prior-owner="11"',
        )
    )
    body.append(_text(393, 295, "Q offsets; K₁₁ interior (zoom)", note=True))
    # The residual is tiny at the domain scale; zoom its actual three vertices.
    triangle = residual[0]
    tx = (min(p[0] for p in triangle) + max(p[0] for p in triangle)) / 2
    ty = (min(p[1] for p in triangle) + max(p[1] for p in triangle)) / 2
    extent = max(
        max(p[0] for p in triangle) - min(p[0] for p in triangle),
        max(p[1] for p in triangle) - min(p[1] for p in triangle),
    )
    body.append(
        _polygon(
            triangle,
            545,
            478,
            145 / float(extent),
            (tx, ty),
            fill="#1d7874",
            tag='data-residual-zoom="true"',
        )
    )
    body += [
        _text(35, 295, "D: file center region", note=True),
        _text(35, 585, "3 obstacles; 7 miss D", note=True),
        _text(395, 585, "Triangle magnified", note=True),
    ]
    return _svg(
        "row",
        "A source-bound owner-update row in case 2095",
        "Accepted case 2095, step 1, owner 10, row 17, closed half-angle interval 17/32 "
        "through 9/16. Field-scaled coordinates are used throughout. The legal center domain "
        "has six vertices, strict square-relative "
        "core has eight, and one tiny triangular residual remains. Three of ten reconstructed "
        "owned-hull Minkowski obstacles overlap this domain. Ownership promotion requires "
        "the complete angular cover, common-core and compression checks; "
        "this one row is an illustration.",
        width=740,
        height=614,
        body="".join(body),
    )


#: How far the charge figure's lower panel is raised into the room two sentences left.
CHARGE_LIFT = 52


def _charge_svg() -> str:
    _pin_checker(Path(field.__file__), FIELD_CHECKER_SHA)
    receipt = _read_json(FIELD / "result.json", FIELD_RESULT_SHA)
    audit = _read_object(FIELD / "objects", FIELD_AUDIT_SHA)
    if (
        receipt.get("audit_proposal_sha256") != FIELD_AUDIT_SHA
        or receipt.get("geometry_verified") is not True
        or audit.get("canonical_mask_index") != 0
        or audit.get("mask") != list(range(11))
        or audit.get("conditional_owner_support") != [0, 1, 2, 3, 6]
        or audit.get("proved_positive_cells") != [1, 2]
        or audit.get("proved_cell_thresholds") != {"1": 1, "2": 1}
        or audit.get("budget_units") != 1
        or audit.get("threshold_sum_units") != 2
        or 0 not in audit.get("transferred_canonical_mask_indices", [])
    ):
        raise ValueError("source-bound field-charge example changed")
    body = [
        _text(28, 38, "A separating projection · capacity-one lemma"),
        '<line x1="78" y1="150" x2="650" y2="150" stroke="#52667a" stroke-width="2"/>',
        (
            '<rect x="104" y="112" width="165" height="76" rx="8" '
            'fill="#dcebef" stroke="#1d7874" stroke-width="2"/>'
        ),
        (
            '<rect x="368" y="112" width="174" height="76" rx="8" '
            'fill="#f5dfb8" stroke="#a15a00" stroke-width="2"/>'
        ),
        '<line x1="328" y1="92" x2="328" y2="217" stroke="#172b3a" stroke-width="2"/>',
        _text(186, 139, "core A", anchor="middle"),
        _text(455, 139, "core B", anchor="middle"),
        _text(328, 239, "median m", anchor="middle", note=True),
        # The lower panel stands where it did under two lines of prose, less their room.
        f'<g transform="translate(0 {-CHARGE_LIFT})">',
        '<line x1="28" y1="322" x2="705" y2="322" stroke="#cbd5e1"/>',
        _text(28, 358, "Accepted field example · canonical mask 0"),
        _text(28, 393, "Required owners O = {0,1,2,3,6}"),
        _text(28, 422, "Mask J = {0,…,10}; O ⊆ J"),
        _text(28, 451, "Charged cells P ∩ J = {1,2}"),
        _text(28, 480, "Γ₁ = Γ₂ = 1; budget b = 1"),
        (
            '<rect x="450" y="385" width="240" height="113" rx="9" '
            'fill="#dcebef" stroke="#1d7874" stroke-width="2"/>'
        ),
        _text(570, 440, "Γ₁ + Γ₂ = 2 > 1 = b", anchor="middle"),
        "</g>",
    ]
    return _svg(
        "charge",
        "A median projection capacity and a strict field budget",
        "Upper panel is a schematic one-direction median projection. Lower panel quotes "
        "accepted canonical-mask-zero field data: required owners 0,1,2,3,6 are present "
        "in mask 0 through 10; charged cells 1 and 2 each carry charge one, "
        "exceeding budget one. The exact checker "
        "establishes the required all-direction statements.",
        width=740,
        height=518 - CHARGE_LIFT,
        body="".join(body),
    )


def _point_in_cell(point: Point, cell: tuple[Point, ...]) -> bool:
    return d4.intersection((point,), cell) == (point,)


def _d4_example() -> tuple[
    list[tuple[Point, ...]], dict[str, Any], list[Point], dict[str, str]
]:
    """The accepted D4 example the symmetry figure draws, checked against its receipt:
    the cover's cells, the overlay region whose point is shown, that point in its four
    views, and what the caption says of the example and of the search it stands for."""
    _pin_checker(Path(d4.__file__), D4_CHECKER_SHA)
    receipt = _read_json(D4 / "result.json", D4_RESULT_SHA)
    inputs = receipt.get("input_sha256", {})
    if (
        receipt.get("status") != "PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE"
        or inputs
        != {"cover": D4_COVER_SHA, "overlay": D4_OVERLAY_SHA, "distance": D4_DISTANCE_SHA}
        or receipt.get("strict_distance_bans") != 1572
    ):
        raise ValueError("accepted D4 illustration premise changed")
    objects = D4 / "objects"
    cover = _read_object(objects, D4_COVER_SHA)
    overlay = _read_object(objects, D4_OVERLAY_SHA)
    distances = _read_object(objects, D4_DISTANCE_SHA)
    if len(cover.get("cells", [])) != 16 or len(overlay.get("regions", [])) != 220:
        raise ValueError("D4 cover or overlay census changed")
    cells = [d4.points(cell["vertices"]) for cell in cover["cells"]]
    region = overlay["regions"][9]
    other = overlay["regions"][12]
    pair = distances["pairs"][0]
    if (
        region["index"] != 9
        or region["labels"] != [0, 7, 3, 5]
        or other["index"] != 12
        or pair["regions"] != [9, 12]
        or len(distances["pairs"]) != 1572
        or tuple(tuple(view) for view in overlay["symmetries"]) != d4.VIEWS
    ):
        raise ValueError("selected D4 example changed")
    first = d4.points(region["vertices"])
    second = d4.points(other["vertices"])
    banned, maximum = d4.strict_distance_ban(first, second)
    if not banned or maximum != Q(pair["maximum_squared_center_distance"]):
        raise ValueError("illustrative D4 strict ban changed")
    point: Point = (
        Q(sum(p[0] for p in first) / len(first)),
        Q(sum(p[1] for p in first) / len(first)),
    )
    x, y = point
    shown = [(x, y), (1 - x, y), (1 - y, x), (y, x)]
    if any(
        not _point_in_cell(q, cells[label])
        for q, label in zip(shown, region["labels"], strict=True)
    ):
        raise ValueError("selected D4 point does not have its retained labels")
    facts = {
        "D4_BAN_REGIONS": " and ".join(str(index) for index in pair["regions"]),
        "D4_REGIONS": f"{len(overlay['regions']):,}",
        "D4_BANS": f"{receipt['strict_distance_bans']:,}",
    }
    return cells, region, shown, facts


def _symmetry_svg() -> str:
    cells, region, shown, _ = _d4_example()
    body: list[str] = []
    for index, (q, label) in enumerate(zip(shown, region["labels"], strict=True)):
        left = 28 + index * 174
        body.append(
            f'<rect x="{left}" y="66" width="156" height="156" '
            'fill="#f8fafc" stroke="#94a3b8"/>'
        )
        for cell_index, cell in enumerate(cells):
            body.append(
                _polygon(
                    list(cell),
                    left + 8,
                    214,
                    140,
                    (Q(), Q()),
                    fill="#dcebef" if cell_index == label else "#f8fafc",
                    stroke="#cbd5e1" if cell_index != label else "#1d7874",
                    tag=f'data-view="{index}" data-cell="{cell_index}"',
                )
            )
        px, py = left + 8 + 140 * float(q[0]), 214 - 140 * float(q[1])
        body.append(
            f'<circle data-view-point="{index}" cx="{px:.3f}" cy="{py:.3f}" '
            'r="5" fill="#a15a00"/>'
        )
        body.append(_text(left + 78, 247, f"view {index + 1}: cell {label}", anchor="middle"))
    return _svg(
        "symmetry",
        "Four point views on a fixed irregular cell cover",
        "The same exact rational point from retained D4 overlay region 9 has fixed-cover "
        "cell labels 0,7,3,5 under four coordinate views.",
        width=740,
        top=50,
        height=216,
        body="".join(body),
    )


def caption_facts() -> dict[str, str]:
    """What the article's captions say of these diagrams that is data, each from the
    receipt its diagram is drawn from and only once that receipt checks: how many rows
    the worked row's update has and how many complete updates exclude its case, and the
    D4 search's census with the one ban the caption cites. A caption names these and
    never types them."""
    source, step, _ = _admitted_row()
    return {
        "ROW_UPDATE_ROWS": str(len(step["rows"])),
        "ROW_CASE_UPDATES": str(len(source["steps"])),
        **_d4_example()[3],
    }


def render_mechanism_figures() -> dict[str, str]:
    """Return four standalone illustrations with source-bound concrete examples."""
    result = {
        "POSE_SVG": _pose_svg(),
        "ROW_SVG": _row_svg(),
        "CHARGE_SVG": _charge_svg(),
        "SYMMETRY_SVG": _symmetry_svg(),
    }
    # Refuse source drift that occurs while rendering any of the examples.
    _pin_checker(Path(fresh.__file__), GENERIC_CHECKER_SHA)
    _pin_checker(Path(field.__file__), FIELD_CHECKER_SHA)
    _pin_checker(Path(d4.__file__), D4_CHECKER_SHA)
    return result
