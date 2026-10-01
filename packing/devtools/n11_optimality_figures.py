"""Render source-bound SVG illustrations for the n=11 optimality explainer.

These drawings are not proof computations. The cell vertices, case mask, witness,
and capture ancestry come from retained inputs and reviewed receipts; rational
coordinates are converted to pixels only after their source identities are checked.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from fractions import Fraction
from html import escape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from devtools.check_n11_optimality_d4 import EXPECTED_MASKS
from devtools.packing_render_adapters import frame_from_trump11
from sqpack.render import render_packing_svg

PACKING = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/n11-optimality-2026-09-29/receipts"
WITNESS = PACKING / "atlas/rendering/trump11-overview.svg"
COMPOSITION = PACKET / "final-composition.json"
D4_RECEIPT = PACKET / "d4-independent/result.json"
SOURCE_GRAPH = PACKET / "source-graph/result.json"
CASE_MASK = EXPECTED_MASKS[438]
CELL_COUNT = 16
CAPTURE_NODE_COUNT = 10
SVG_NS = "http://www.w3.org/2000/svg"

# Canvas dimensions are display choices, not geometric inputs to the proof.
CELL_CANVAS = 640
CELL_MARGIN = 36
TREE_WIDTH = 840
TREE_TOP = 70
TREE_LEVEL_GAP = 100
TREE_LEAF_X = (100, 310, 520, 730)

NODE_NAMES = {
    "research/candidate-capture/root-self-240.json": "root",
    "research/candidate-capture/far15y-self-300.json": "far15",
    "research/candidate-capture/tree438-rebuilt/r1.json": "r1",
    "research/candidate-capture/tree438-rebuilt/r10.json": "r10",
    "research/candidate-capture/far13-collision-180.json": "far13",
    "research/candidate-capture/near13-self-180.json": "near13",
    "research/candidate-capture/tree438-facet/r11.json": "r11",
    "research/candidate-capture/tree438-facet/r110.json": "far2",
    "research/candidate-capture/tree438-facet/r111.json": "r111",
    "research/candidate-capture/near-refined1024-240.json": "near",
}
LEAF_OUTCOMES = {
    "far15": "contradiction",
    "far13": "contradiction",
    "far2": "contradiction",
    "near": "local enclosure",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(path: Path, expected_sha: str) -> dict[str, Any]:
    data = path.read_bytes()
    if _sha256(data) != expected_sha:
        raise ValueError(f"retained receipt changed: {path}")
    value: dict[str, Any] = json.loads(data)
    return value


def _admitted_sources() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    composition: dict[str, Any] = json.loads(COMPOSITION.read_bytes())
    if composition.get("status") != "PASS_REVIEWED_COMPONENT_COMPOSITION":
        raise ValueError("the retained final composition is not accepted")
    if composition.get("global_optimality_proved") is not True:
        raise ValueError("the retained final composition does not prove T-060")
    accepted = composition["reviewed_receipt_sha256s"]
    d4 = _json_bytes(D4_RECEIPT, accepted["d4-independent"])
    graph = _json_bytes(SOURCE_GRAPH, accepted["source-graph"])
    if d4.get("status") != "PASS_INDEPENDENT_CONDITIONAL_D4_BRIDGE":
        raise ValueError("the retained D4 bridge is not accepted")
    if graph.get("actual_source_parent_graph_checked") is not True:
        raise ValueError("the retained capture source graph is not checked")

    cover_sha = d4["input_sha256"]["cover"]
    cover_path = PACKET / f"d4-independent/objects/{cover_sha}.gz"
    cover_data = gzip.decompress(cover_path.read_bytes())
    if _sha256(cover_data) != cover_sha:
        raise ValueError("the retained rational cell data changed")
    cover: dict[str, Any] = json.loads(cover_data)
    cells: list[dict[str, Any]] = cover["cells"]
    if len(cells) != CELL_COUNT or [row["index"] for row in cells] != list(range(CELL_COUNT)):
        raise ValueError("the retained cover lacks the indexed sixteen cells")
    if tuple(CASE_MASK) != (0, 1, 2, 3, 4, 8, 9, 10, 11, 13, 15):
        raise ValueError("the retained case-438 mask changed")
    if graph["source_nodes_checked"] != CAPTURE_NODE_COUNT:
        raise ValueError("the retained capture graph lacks ten nodes")
    return cells, graph


def _svg(
    identifier: str,
    title: str,
    description: str,
    *,
    width: int,
    height: int,
    content: str,
) -> str:
    title_id = f"n11-{identifier}-title"
    desc_id = f"n11-{identifier}-desc"
    return (
        f'<svg xmlns="{SVG_NS}" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="{title_id} {desc_id}">'
        f'<title id="{title_id}">{escape(title)}</title>'
        f'<desc id="{desc_id}">{escape(description)}</desc>'
        f"{content}</svg>"
    )


def _pixel(point: list[str]) -> tuple[float, float]:
    span = CELL_CANVAS - 2 * CELL_MARGIN
    x, y = (Fraction(value) for value in point)
    return CELL_MARGIN + span * float(x), CELL_MARGIN + span * float(1 - y)


def _cell_svg(cells: list[dict[str, Any]], *, mask: bool) -> str:
    selected = set(CASE_MASK)
    parts = []
    outlines: list[str] = []
    for row in cells:
        index = row["index"]
        vertices = [_pixel(point) for point in row["vertices"]]
        points = " ".join(f"{x:.4f},{y:.4f}" for x, y in vertices)
        fill = "#1d7874" if mask and index in selected else "#e2e8f0" if mask else "#dcebef"
        parts.append(
            f'<polygon data-cell="{index}" data-selected="{str(index in selected).lower()}" '
            f'points="{points}" fill="{fill}"/>'
        )
        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1], strict=True):
            outlines.append(
                f'<line x1="{x1:.4f}" y1="{y1:.4f}" x2="{x2:.4f}" y2="{y2:.4f}" '
                'stroke="#52667a" stroke-width="1.2"/>'
            )
        x, y = _pixel(row["center"])
        label_color = "#fff" if mask and index in selected else "#172b3a"
        outlines.append(
            f'<text x="{x:.4f}" y="{y:.4f}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="sans-serif" font-size="18" font-weight="700" fill="{label_color}">'
            f"{index}</text>"
        )
    parts.extend(outlines)
    low, high = CELL_MARGIN, CELL_CANVAS - CELL_MARGIN
    for x1, y1, x2, y2 in (
        (low, low, high, low),
        (high, low, high, high),
        (high, high, low, high),
        (low, high, low, low),
    ):
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="2"/>'
        )
    if mask:
        title = "Case 438 selects eleven of the sixteen center cells"
        description = (
            "The eleven selected Voronoi cells of case 438 are teal; the other five are gray. "
            "Cell vertices are exact rational proof input, converted to SVG pixels "
            "for illustration. "
            "Selection is cell membership, not an owned-hull diagram."
        )
    else:
        title = "Sixteen exact center-cover Voronoi cells"
        description = (
            "Sixteen closed rational Voronoi cells partition the normalized square. "
            "Their retained exact vertices are converted to SVG pixels only for illustration."
        )
    return _svg(
        "mask" if mask else "cover",
        title,
        description,
        width=CELL_CANVAS,
        height=CELL_CANVAS,
        content="".join(parts),
    )


def _capture_svg(graph: dict[str, Any]) -> str:
    parent_edges: dict[str, str] = graph["source_parent_edges"]
    if set(parent_edges) != set(NODE_NAMES) - {"research/candidate-capture/root-self-240.json"}:
        raise ValueError("capture graph nodes differ from the retained ten-node tree")
    roots = set(NODE_NAMES) - set(parent_edges)
    if len(roots) != 1:
        raise ValueError("capture graph has no unique root")
    root = roots.pop()
    source_hashes = {
        path: details["decoded_sha256"] for path, details in graph["source_provenance"].items()
    }
    if (
        set(source_hashes) != set(NODE_NAMES)
        or len(set(source_hashes.values())) != CAPTURE_NODE_COUNT
    ):
        raise ValueError("capture graph source identities are incomplete or duplicate")
    children: dict[str, list[str]] = {path: [] for path in NODE_NAMES}
    hash_to_path = {digest: path for path, digest in source_hashes.items()}
    for child, parent_hash in parent_edges.items():
        if parent_hash not in hash_to_path:
            raise ValueError("capture graph contains an unknown parent hash")
        children[hash_to_path[parent_hash]].append(child)
    leaves = [path for path in NODE_NAMES if not children[path]]
    if {NODE_NAMES[path] for path in leaves} != set(LEAF_OUTCOMES):
        raise ValueError("capture graph leaves differ from the four accepted outcomes")
    leaves.sort(key=lambda path: ("far15", "far13", "far2", "near").index(NODE_NAMES[path]))
    leaf_x = dict(zip(leaves, TREE_LEAF_X, strict=True))
    positions: dict[str, tuple[float, int]] = {}

    def position(path: str, depth: int) -> float:
        if path in positions:
            raise ValueError("capture graph has a cycle or joined child")
        x = (
            sum(position(child, depth + 1) for child in children[path]) / len(children[path])
            if children[path]
            else leaf_x[path]
        )
        positions[path] = (x, depth)
        return x

    position(root, 0)
    if len(positions) != CAPTURE_NODE_COUNT:
        raise ValueError("capture graph has unreachable nodes")
    height = TREE_TOP * 2 + TREE_LEVEL_GAP * max(depth for _, depth in positions.values())
    parts: list[str] = []
    for child, parent_hash in parent_edges.items():
        parent = hash_to_path[parent_hash]
        x1, d1 = positions[parent]
        x2, d2 = positions[child]
        parts.append(
            f'<line x1="{x1:.1f}" y1="{TREE_TOP + d1 * TREE_LEVEL_GAP}" '
            f'x2="{x2:.1f}" y2="{TREE_TOP + d2 * TREE_LEVEL_GAP}" '
            'stroke="#94a3b8" stroke-width="2.5"/>'
        )
    for path, (x, depth) in positions.items():
        label = NODE_NAMES[path]
        leaf = label in LEAF_OUTCOMES
        fill = "#e4f3ee" if label == "near" else "#fce9e7" if leaf else "#e9eff7"
        y = TREE_TOP + depth * TREE_LEVEL_GAP
        parts.append(
            f'<rect x="{x - 56:.1f}" y="{y - 24:.1f}" width="112" height="48" rx="12" '
            f'fill="{fill}" stroke="#52667a" stroke-width="1.5"/>'
            f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" '
            f'font-family="sans-serif" font-size="17" font-weight="700" fill="#17324a">'
            f"{escape(label)}</text>"
        )
        if leaf:
            parts.append(
                f'<text x="{x:.1f}" y="{y + 43:.1f}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="13" fill="#34465a">'
                f"{escape(LEAF_OUTCOMES[label])}</text>"
            )
    return _svg(
        "capture",
        "The closed case-438 capture tree",
        "The accepted ten-node source-parent tree ends at three contradiction leaves and one "
        "near leaf discharged by pose inclusion and local isolation. This is a dependency "
        "diagram, not a drawing of the geometric search domains.",
        width=TREE_WIDTH,
        height=height + 36,
        content="".join(parts),
    )


def _witness_svg() -> str:
    text = render_packing_svg(frame_from_trump11())
    if text != WITNESS.read_text(encoding="utf-8"):
        raise ValueError("the retained exact-construction witness SVG is stale")
    root = ET.fromstring(text)
    outlines = root.findall(f'.//{{{SVG_NS}}}polygon[@data-feature="square-outline"]')
    container = root.findall(f'.//{{{SVG_NS}}}rect[@data-feature="container-outline"]')
    if len(outlines) != 11 or len(container) != 1:
        raise ValueError("retained exact witness SVG lacks its eleven squares or container")
    text = re.sub(r"<\?xml[^>]*\?>\s*", "", text, count=1)
    text = re.sub(r"<metadata>.*?</metadata>\s*", "", text, count=1, flags=re.DOTALL)
    text = re.sub(
        r'<title id="figure-title">.*?</title>',
        '<title id="figure-title">Trump construction of eleven unit squares</title>',
        text,
        count=1,
    )
    return re.sub(
        r'<desc id="figure-description">.*?</desc>',
        '<desc id="figure-description">An SVG illustration rendered from the exact '
        "Trump construction. Pixel coordinates are rounded for display; exact algebraic "
        "checks establish the witness separately.</desc>",
        text,
        count=1,
    )


def render_figures() -> dict[str, str]:
    """Return four self-contained SVG illustrations from reviewed retained inputs."""
    cells, graph = _admitted_sources()
    return {
        "WITNESS_SVG": _witness_svg(),
        "COVER_SVG": _cell_svg(cells, mask=False),
        "CAPTURE_SVG": _capture_svg(graph),
        "MASK_SVG": _cell_svg(cells, mask=True),
    }
