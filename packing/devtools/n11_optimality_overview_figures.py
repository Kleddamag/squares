"""Static, source-bound diagrams for the T-060 proof route and exact endpoint."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from html import escape
from pathlib import Path
from typing import Any

PACKING = Path(__file__).resolve().parents[1]
RECEIPTS = PACKING / "resources/web/n11-optimality-2026-09-29/receipts"
COMPOSITION = RECEIPTS / "final-composition.json"
D4 = RECEIPTS / "d4-independent/result.json"
EXCLUSIONS = RECEIPTS / "exclusion-inventory.json"
LOCAL = RECEIPTS / "local-isolation/result.json"
POSE = RECEIPTS / "pose-inclusion/result.json"
RENDER_INPUTS = (Path(__file__), COMPOSITION, D4, EXCLUSIONS, LOCAL, POSE)

SVG_NS = "http://www.w3.org/2000/svg"
INK = "var(--kpress-doc-text)"
MUTED = "var(--kpress-doc-muted)"
ACCENT = "var(--kpress-doc-accent)"
BORDER = "var(--kpress-doc-border)"
BACKGROUND = "var(--kpress-doc-bg)"


def _load(path: Path, expected_sha: str | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    if expected_sha is not None and hashlib.sha256(data).hexdigest() != expected_sha:
        raise ValueError(f"retained receipt changed: {path}")
    value = json.loads(data)
    if not isinstance(value, dict):
        raise TypeError(f"expected an object in {path.name}")
    return value


def _sources() -> Fraction:
    composition = _load(COMPOSITION)
    accepted = composition["reviewed_receipt_sha256s"]
    d4 = _load(D4, accepted["d4-independent"])
    exclusions = _load(EXCLUSIONS, composition["exclusion_inventory_sha256"])
    local = _load(LOCAL, accepted["local-isolation"])
    pose = _load(POSE, accepted["pose-inclusion"])

    if (
        composition.get("status") != "PASS_REVIEWED_COMPONENT_COMPOSITION"
        or composition.get("global_optimality_proved") is not True
        or composition.get("geometry_rerun") is not False
        or composition.get("pending_obligations") != []
        or composition.get("accepted_exclusions") != 2180
        or composition.get("required_exclusions") != 2180
    ):
        raise ValueError("the accepted final composition changed")
    if (
        d4.get("status") != "PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE"
        or d4.get("raw_masks") != 4368
        or d4.get("canonical_masks") != 2184
        or [(row["source_canonical_index"], row["status"]) for row in d4["finite_search"]]
        != [(999, "UNSAT"), (1462, "UNSAT"), (1659, "UNSAT")]
    ):
        raise ValueError("the accepted case reduction changed")
    survivors = set(range(2184)) - set(exclusions.get("accepted_case_ids", []))
    if (
        exclusions.get("status") != "EXECUTION_RECORD_INVENTORY"
        or exclusions.get("accepted_case_count") != 2180
        or exclusions.get("required_case_count") != 2180
        or survivors != {438, 999, 1462, 1659}
    ):
        raise ValueError("the accepted exclusion inventory changed")
    ratio = Fraction(local["worst_dual_ratio"])
    if (
        local.get("status") != "PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION"
        or local.get("fixed_T_local_isolation_proved") is not True
        or local.get("required_branches") != 128
        or len(local.get("checked_branches", [])) != 128
        or local.get("signed_coordinate_margins_checked") != 8448
        or not 0 < ratio < 1
    ):
        raise ValueError("the accepted fixed-T local result changed")
    frame = pose.get("source_frame")
    if not isinstance(frame, dict):
        raise TypeError("the accepted field frame is missing")
    cap = Fraction(frame["U"])
    scale = Fraction(frame["B"])
    if (
        pose.get("status") != "PASS_POSE_INCLUSION"
        or pose.get("pose_inclusion_proved") is not True
        or pose.get("root_interval") != local.get("root_interval")
        or cap != Fraction(387708359002281417731, 10**20)
        or scale * cap != Fraction(191, 50)
        or frame.get("inverse") != "(yf/B-U/2,U/2-xf/B)"
    ):
        raise ValueError("the accepted fixed-T pose inclusion changed")
    return ratio


def _svg(
    identifier: str,
    title: str,
    description: str,
    *,
    width: int,
    top: int,
    bottom: int,
    body: str,
) -> str:
    """One diagram, its canvas from `top` to `bottom` of the coordinates its parts are
    drawn in. A diagram carries its labels and nothing else: its title and whatever a
    sentence says of it are the figure's caption, in the article."""
    title_id = f"n11-{identifier}-title"
    desc_id = f"n11-{identifier}-desc"
    height = bottom - top
    return (
        f'<svg xmlns="{SVG_NS}" class="n11-diagram n11-{identifier}" '
        f'width="{width}" height="{height}" viewBox="0 {top} {width} {height}" '
        f'role="img" aria-labelledby="{title_id} {desc_id}">'
        f'<title id="{title_id}">{escape(title)}</title>'
        f'<desc id="{desc_id}">{escape(description)}</desc>'
        f"{body}</svg>"
    )


def _text(x: int, y: int, value: str, *, note: bool = False, anchor: str = "start") -> str:
    role = "n11-diagram-note" if note else "n11-diagram-label"
    return (
        f'<text class="{role}" x="{x}" y="{y}" text-anchor="{anchor}" '
        f'fill="{INK}">{escape(value)}</text>'
    )


def _card(y: int, label: str, detail: str, *, accent: bool = False) -> str:
    stroke = ACCENT if accent else BORDER
    return (
        f'<rect x="36" y="{y}" width="828" height="70" rx="10" '
        f'fill="{BACKGROUND}" stroke="{stroke}" stroke-width="2"/>'
        + _text(58, y + 29, label)
        + _text(58, y + 55, detail, note=True)
    )


def _down_arrow(y: int) -> str:
    return (
        f'<path d="M450 {y}v20" fill="none" stroke="{MUTED}" stroke-width="2"/>'
        f'<path d="M443 {y + 14}l7 8 7-8" fill="none" stroke="{MUTED}" '
        'stroke-width="2"/>'
    )


def _roadmap() -> str:
    body = (
        _card(48, "Exact construction at T", "Eleven unit squares fit: s(11) ≤ T", accent=True)
        + _text(
            450,
            151,
            "For the lower bound, assume S < T",
            note=True,
            anchor="middle",
        )
        + _card(170, "Assume S < T", "The same packing sits inside cap U > T")
        + _down_arrow(240)
        + _card(263, "Classify center patterns", "16 closed cells; 2,184 case classes")
        + _down_arrow(333)
        + _card(356, "Exclude, then use symmetry", "2,180 excluded; D4 leaves case 438")
        + _down_arrow(426)
        + _card(449, "Capture, align, include", "Packing enters fixed-T rectangle")
        + _down_arrow(519)
        + _card(
            542,
            "Apply fixed-T local isolation",
            "Only the witness remains; span T > S",
            accent=True,
        )
        + _text(450, 642, "No packing has S < T; hence s(11) = T", anchor="middle")
    )
    return _svg(
        "roadmap",
        "Two routes to the exact eleven-square optimum",
        "The exact Trump witness gives the upper bound. For the lower bound, assume a "
        "packing with side S smaller than T. Exact case classification, exclusion, "
        "symmetry, capture, fixed-T pose inclusion and local isolation force the same "
        "packing to be the witness of span T, a contradiction. Counts are case "
        "classes, not numbers of packings. The diagram summarizes accepted premises "
        "and does not rerun their geometry.",
        width=900,
        top=36,
        bottom=665,
        body=body,
    )


def _local(ratio: Fraction) -> str:
    left, top, right, bottom = 104, 100, 660, 350
    width = right - left
    height = bottom - top
    curve = " ".join(
        f"{left + round(width * step / 32)},"
        f"{bottom - round(height * float(ratio) * (step / 32) ** 2)}"
        for step in range(33)
    )
    body = (
        f'<path d="M{left} {top}V{bottom}H{right}" fill="none" stroke="{MUTED}" '
        'stroke-width="2"/>'
        f'<path d="M{left} {bottom}L{right} {top}" fill="none" stroke="{INK}" '
        'stroke-width="3"/>' + f'<polyline points="{curve}" fill="none" stroke="{ACCENT}" '
        f'data-accepted-ratio="{ratio}" stroke-width="3" stroke-dasharray="8 5"/>'
        + _text(539, 113, "τ", anchor="middle")
        + _text(556, 246, "cτ²", anchor="middle")
        + _text(left, 385, "0", note=True, anchor="middle")
        + _text(right, 385, "1", note=True, anchor="middle")
    )
    return _svg(
        "local",
        "A nonzero displacement cannot satisfy the fixed-T local inequality",
        "Algebraic schematic of y equal to tau and y equal to c tau squared on zero "
        "to one. The latter stays strictly below the former because the accepted "
        "fixed-T local checker proves c is below one for every signed-coordinate "
        "branch. The drawn curve uses the largest exact accepted ratio only for "
        "display; the complete 8,448 exact margins prove the result. This is not "
        "a projection of the 33-dimensional pose space or a global uniqueness claim.",
        width=760,
        top=80,
        bottom=404,
        body=body,
    )


def _endpoint() -> str:
    body = (
        f'<rect x="65" y="118" width="260" height="260" fill="none" '
        f'stroke="{MUTED}" stroke-width="2"/>'
        f'<rect x="105" y="158" width="180" height="180" fill="none" '
        f'stroke="{ACCENT}" stroke-width="3" stroke-dasharray="8 5"/>'
        + _text(195, 109, "Rational cap U > T", anchor="middle")
        + _text(195, 256, "packing in S < T", anchor="middle")
        + f'<path d="M345 243h185" fill="none" stroke="{MUTED}" stroke-width="2"/>'
        + f'<path d="M520 235l12 8-12 8" fill="none" stroke="{MUTED}" '
        'stroke-width="2"/>'
        + _text(437, 187, "Undo field frame B", note=True, anchor="middle")
        + _text(437, 216, "rigidly align", note=True, anchor="middle")
        + _text(437, 286, "No physical shrinking", note=True, anchor="middle")
        + f'<rect x="575" y="118" width="260" height="260" fill="none" '
        f'stroke="{INK}" stroke-width="2"/>'
        + f'<rect x="615" y="158" width="180" height="180" fill="none" '
        f'stroke="{ACCENT}" stroke-width="3" stroke-dasharray="8 5"/>'
        + _text(705, 109, "Fixed-T container", anchor="middle")
        + _text(705, 256, "same packing", anchor="middle")
        + _text(
            450,
            419,
            "Capture + inclusion locate packing",
            note=True,
            anchor="middle",
        )
        + _down_arrow(430)
        + _text(450, 477, "Fixed-T local theorem forces witness", anchor="middle")
        + _down_arrow(488)
        + _text(450, 538, "Witness spans T > S: contradiction", anchor="middle")
    )
    return _svg(
        "endpoint",
        "Why a smaller container contradicts the exact witness span",
        "A hypothetical packing P in side S less than T is centered inside the "
        "larger rational cap U. Undoing the field coordinate conversion and then "
        "rigidly aligning it places the same physical unit squares inside the "
        "fixed-T container. Checked capture and pose inclusion put P in the local "
        "rectangle, where the fixed-T local theorem forces the exact Trump witness. "
        "That witness spans T in both directions, so it cannot fit inside side S. "
        "The drawn container gaps are schematic and not to scale; no claim of "
        "uniqueness for all optimal packings is made.",
        width=900,
        top=78,
        bottom=560,
        body=body,
    )


def caption_facts() -> dict[str, str]:
    """What the article's captions say of these diagrams that is data: the fixed-T local
    check's census, from the receipt the diagram itself is drawn from, and only once
    every accepted premise matches. A caption names these and never types them."""
    _sources()
    local = _load(LOCAL)
    return {
        "LOCAL_BRANCHES": f"{local['required_branches']:,}",
        "LOCAL_MARGINS": f"{local['signed_coordinate_margins_checked']:,}",
    }


def render_overview_figures() -> dict[str, str]:
    """Render explanatory SVGs only after their accepted source premises match."""
    ratio = _sources()
    return {
        "ROADMAP_SVG": _roadmap(),
        "LOCAL_SVG": _local(ratio),
        "ENDPOINT_SVG": _endpoint(),
    }
