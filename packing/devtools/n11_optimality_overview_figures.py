"""Static, source-bound diagrams for the T-060 proof route and exact endpoint, and the
exact tables of the interface the proof composes through: the local radii, the local
labels' squares and capture owners, and the center-cover sites."""

from __future__ import annotations

import gzip
import hashlib
import json
from collections.abc import Iterable, Sequence
from fractions import Fraction
from html import escape
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_d4 as d4_checker

PACKING = Path(__file__).resolve().parents[1]
RECEIPTS = PACKING / "resources/web/n11-optimality-2026-09-29/receipts"
COMPOSITION = RECEIPTS / "final-composition.json"
D4 = RECEIPTS / "d4-independent/result.json"
EXCLUSIONS = RECEIPTS / "exclusion-inventory.json"
LOCAL = RECEIPTS / "local-isolation/result.json"
POSE = RECEIPTS / "pose-inclusion/result.json"
#: The focused rectangle's decoded identity, which both the local and the pose-inclusion
#: receipts name as their input, and the cover's, which the D4 receipt names.
FOCUSED_SHA = "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3"
COVER_SHA = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
FOCUSED = RECEIPTS / f"local-dual-residual/objects/{FOCUSED_SHA}.gz"
GUARDS = RECEIPTS / "pose-inclusion/guard.json"
COVER = RECEIPTS / f"d4-independent/objects/{COVER_SHA}.gz"
#: The construction whose square order is the local witness labels' order; the local
#: receipt records the hash of the copy it numbered.
WITNESS_SOURCE = PACKING / "cases/trump11/packing.py"
WITNESS_SOURCE_KEY = "cases/trump11/packing.py"
CASE_MASK = d4_checker.EXPECTED_MASKS[438]
RENDER_INPUTS = (
    Path(__file__),
    COMPOSITION,
    D4,
    EXCLUSIONS,
    LOCAL,
    POSE,
    FOCUSED,
    GUARDS,
    COVER,
    WITNESS_SOURCE,
    Path(d4_checker.__file__),
)

#: Local witness label k's square in the paper's Appendix A, in the order
#: `cases/trump11/packing.py` builds them: six axis-aligned squares, then the images
#: under the rigid map F of five more.
SQUARES = (
    "$A(0,0)$",
    "$A(T-1,0)$",
    "$A(x_0,T-1)$",
    "$A(0,T-1)$",
    "$A(1,T-1)$",
    "$A(0,T-2)$",
    "$F(A(0,0))$",
    r"$F(A(\eta,-1))$",
    "$F(A(1,v))$",
    r"$F(A(\eta+1,v-1))$",
    r"$F(A(\eta+2,-\zeta))$",
)
#: The cover's sites are integers over this denominator, in normalized coordinates.
SITE_DENOMINATOR = 2_000_000
CELL_COUNT = 16

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


def _object(path: Path, decoded_sha: str) -> dict[str, Any]:
    """A retained gzip object, refused unless its decoded bytes are the named ones."""
    data = gzip.decompress(path.read_bytes())
    if hashlib.sha256(data).hexdigest() != decoded_sha:
        raise ValueError(f"retained receipt changed: {path}")
    value = json.loads(data)
    if not isinstance(value, dict):
        raise TypeError(f"expected an object in {path.name}")
    return value


def _accepted() -> dict[str, dict[str, Any]]:
    """The accepted D4, local and pose-inclusion receipts, each at the hash the final
    composition accepted it at, once every premise the diagrams and tables use matches."""
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
        or pose.get("accepted_local_result_sha256") != accepted["local-isolation"]
    ):
        raise ValueError("the accepted fixed-T pose inclusion changed")
    return {"d4": d4, "local": local, "pose": pose}


def _sources() -> Fraction:
    return Fraction(_accepted()["local"]["worst_dual_ratio"])


def markdown_table(header: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    """One Markdown table in the project's style: a `---` rule per column and no
    trailing space, without a final newline, so a placeholder on its own line takes it."""
    lines = [tuple(header), tuple("---" for _ in header), *(tuple(row) for row in rows)]
    if any(len(line) != len(header) for line in lines):
        raise ValueError("a table row has the wrong number of cells")
    return "\n".join("| " + " | ".join(line) + " |" for line in lines)


def _exact(value: str) -> str:
    """An exact positive rational as the paper prints it, `$p/q$` in lowest terms."""
    number = Fraction(value)
    if number <= 0 or str(number) != value:
        raise ValueError(f"not a positive rational in lowest terms: {value}")
    return f"${number}$"


def local_radii_table(focused: dict[str, Any]) -> str:
    """The focused rectangle's 33 radii, label k's at coordinates 3k, 3k+1 and 3k+2:
    two physical center radii and one angular radius in radians."""
    radii = focused.get("radii", [])
    inclusion = focused.get("inclusion", [])
    if (
        focused.get("status") != "PASS_INDEPENDENT_FOCUSED_RECTANGLE_LOCAL_ISOLATION"
        or focused.get("local_rectangle_isolation_proved") is not True
        or len(radii) != 3 * len(SQUARES)
        or [entry["label"] for entry in inclusion] != list(range(len(SQUARES)))
        or any(entry["radii"] != radii[3 * k : 3 * k + 3] for k, entry in enumerate(inclusion))
    ):
        raise ValueError("the accepted focused local rectangle changed")
    return markdown_table(
        ("Label", "$r_x$", "$r_y$", r"$r_\theta$"),
        (
            (str(k), *(_exact(value) for value in radii[3 * k : 3 * k + 3]))
            for k in range(len(SQUARES))
        ),
    )


def capture_owners(
    focused: dict[str, Any], guards: dict[str, Any], pose: dict[str, Any]
) -> list[int]:
    """Each local label's capture owner cell, which the role guard for case 438, the
    pose-inclusion result and the focused rectangle must all state alike."""
    entries = [entry for entry in guards.get("guards", []) if entry["mask"] == list(CASE_MASK)]
    if len(entries) != 1:
        raise ValueError("the retained role guard lacks one entry for case 438")
    guard = entries[0]
    owners: list[int] = guard["label_to_cell"]
    by_role = {role["label"]: role["cell"] for role in guard["roles"]}
    if (
        sorted(owners) != list(CASE_MASK)
        or [by_role.get(k) for k in range(len(SQUARES))] != owners
        or [(row["label"], row["owner"]) for row in pose["owners"]] != list(enumerate(owners))
        or [(row["label"], row["owner"]) for row in focused["inclusion"]]
        != list(enumerate(owners))
        or any(
            row["accepted_radii"] != focused["radii"][3 * k : 3 * k + 3]
            for k, row in enumerate(pose["owners"])
        )
    ):
        raise ValueError("the accepted local-to-owner map changed")
    return owners


def role_map_table(owners: Sequence[int]) -> str:
    """Local label, its square in Appendix A's notation, and its capture owner cell."""
    if len(owners) != len(SQUARES):
        raise ValueError("the role map does not name eleven owners")
    return markdown_table(
        ("Local label", "Square", "Capture owner cell"),
        (
            (str(k), square, str(owner))
            for k, (square, owner) in enumerate(zip(SQUARES, owners, strict=True))
        ),
    )


def cover_sites_table(cover: dict[str, Any]) -> str:
    """Sites 0-7 of the sixteen-cell cover as integers over 2,000,000, each with the
    site the half-turn sends it to, once every site 15-i is exactly (1,1) minus site i."""
    cells = cover.get("cells", [])
    if (
        cover.get("status") != "PASS_EXACT_HALF_TURN_16_CELL_COVER"
        or cover.get("centers_denominator") != SITE_DENOMINATOR
        or cover.get("number_of_cells") != CELL_COUNT
        or [cell["index"] for cell in cells] != list(range(CELL_COUNT))
        or cover.get("symmetry_cell_involution") != list(range(CELL_COUNT))[::-1]
    ):
        raise ValueError("the accepted center cover changed")
    sites = [tuple(Fraction(value) for value in cell["center"]) for cell in cells]
    half = CELL_COUNT // 2
    for index, (x, y) in enumerate(sites[:half]):
        if sites[CELL_COUNT - 1 - index] != (1 - x, 1 - y):
            raise ValueError(
                f"cover site {CELL_COUNT - 1 - index} is not site {index} reflected"
            )
    scaled = [tuple(value * SITE_DENOMINATOR for value in site) for site in sites[:half]]
    if any(
        value.denominator != 1 or not 0 < value < SITE_DENOMINATOR
        for site in scaled
        for value in site
    ):
        raise ValueError("a cover site is not an interior integer point over 2,000,000")
    return markdown_table(
        ("Site", "First coordinate", "Second coordinate", "Reflected site"),
        (
            (str(index), str(x.numerator), str(y.numerator), str(CELL_COUNT - 1 - index))
            for index, (x, y) in enumerate(scaled)
        ),
    )


def _tables(accepted: dict[str, dict[str, Any]]) -> dict[str, str]:
    """The three exact tables, each from the retained object its accepted receipt names."""
    local, pose, d4 = accepted["local"], accepted["pose"], accepted["d4"]
    if (
        local.get("input_sha256", {}).get("focused") != FOCUSED_SHA
        or pose.get("focused_sha256") != FOCUSED_SHA
        or d4.get("input_sha256", {}).get("cover") != COVER_SHA
    ):
        raise ValueError("an accepted receipt names a different table input")
    if (
        hashlib.sha256(WITNESS_SOURCE.read_bytes()).hexdigest()
        != local["source_hashes"][WITNESS_SOURCE_KEY]
    ):
        raise ValueError(f"retained receipt changed: {WITNESS_SOURCE}")
    focused = _object(FOCUSED, FOCUSED_SHA)
    guards = _load(GUARDS, pose["guard_sha256"])
    cover = _object(COVER, COVER_SHA)
    return {
        "LOCAL_RADII_TABLE": local_radii_table(focused),
        "ROLE_MAP_TABLE": role_map_table(capture_owners(focused, guards, pose)),
        "COVER_SITES_TABLE": cover_sites_table(cover),
    }


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
            "For the lower bound, assume L₀ < T",
            note=True,
            anchor="middle",
        )
        + _card(170, "Assume L₀ < T", "The same packing sits inside cap U > T")
        + _down_arrow(240)
        + _card(263, "Classify center patterns", "16 closed cells; 2,184 case classes")
        + _down_arrow(333)
        + _card(356, "Exclude, then use symmetry", "2,180 excluded; D₄ leaves case 438")
        + _down_arrow(426)
        + _card(449, "Capture, align, include", "Packing enters fixed-T rectangle")
        + _down_arrow(519)
        + _card(
            542,
            "Apply fixed-T local isolation",
            "Only the witness remains; span T > L₀",
            accent=True,
        )
        + _text(450, 642, "No packing has L₀ < T; hence s(11) = T", anchor="middle")
    )
    return _svg(
        "roadmap",
        "Two routes to the exact eleven-square optimum",
        "The exact Trump witness gives the upper bound. For the lower bound, assume a "
        "packing with side L₀ smaller than T. Exact case classification, exclusion, "
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
        + _text(195, 256, "packing in L₀ < T", anchor="middle")
        + f'<path d="M345 243h185" fill="none" stroke="{MUTED}" stroke-width="2"/>'
        + f'<path d="M520 235l12 8-12 8" fill="none" stroke="{MUTED}" '
        'stroke-width="2"/>'
        + _text(437, 187, "Undo file scale", note=True, anchor="middle")
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
        + _text(450, 538, "Witness spans T > L₀: contradiction", anchor="middle")
    )
    return _svg(
        "endpoint",
        "Why a smaller container contradicts the exact witness span",
        "A hypothetical packing P in side L₀ less than T is centered inside the "
        "larger rational cap U. Undoing the file-coordinate scale and then "
        "rigidly aligning it places the same physical unit squares inside the "
        "fixed-T container. Checked capture and pose inclusion put P in the local "
        "rectangle, where the fixed-T local theorem forces the exact Trump witness. "
        "That witness spans T in both directions, so it cannot fit inside side L₀. "
        "The drawn container gaps are schematic and not to scale; no claim of "
        "uniqueness for all optimal packings is made.",
        width=900,
        top=78,
        bottom=560,
        body=body,
    )


def caption_facts() -> dict[str, str]:
    """What the article says of these diagrams that is data: the fixed-T local check's
    census, from the receipt the diagram itself is drawn from, and the exact tables of
    the local radii, the local-to-owner map and the cover's sites, from the objects the
    accepted receipts name, and only once every accepted premise matches. The article
    names these and never types them."""
    accepted = _accepted()
    local = accepted["local"]
    return {
        "LOCAL_BRANCHES": f"{local['required_branches']:,}",
        "LOCAL_MARGINS": f"{local['signed_coordinate_margins_checked']:,}",
        **_tables(accepted),
    }


def render_overview_figures() -> dict[str, str]:
    """Render explanatory SVGs only after their accepted source premises match."""
    ratio = _sources()
    return {
        "ROADMAP_SVG": _roadmap(),
        "LOCAL_SVG": _local(ratio),
        "ENDPOINT_SVG": _endpoint(),
    }
