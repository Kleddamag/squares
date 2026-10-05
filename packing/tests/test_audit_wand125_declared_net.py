"""The first-party audit of wand125's mixed certificate on a declared net (jlevy/squares#366).

`devtools.audit_wand125_declared_net` recomputes `mixed_n18_L470`'s exact premises from
the retained files, lemma N0's five among them, and refuses a copy whose net, mass or
stated facts are changed. Its bundle receipt binds the source's own runs to the declared
net, and its comparison passes a replay only when every regenerated record is the
shipped one.
"""

from __future__ import annotations

import json
import math
import os
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_wand125_declared_net as declared
from devtools.retained_data import read_retained_bytes


def test_the_audit_recomputes_to_its_receipt() -> None:
    assert declared.main(["audit", "--check"]) == 0


def test_the_audit_holds_lemma_n0_on_the_declared_net() -> None:
    facts = declared.audit()
    assert facts["status"] == "EXACT_PREMISES_HOLD"
    assert all(facts["premises"].values())
    assert facts["net"]["step"] == "1/1001"
    assert facts["net"]["count"] == "416"
    assert facts["net"]["rotated_side_upper"] == "500499/500500"
    assert facts["net"]["endpoint_check"] == "1054/1002001"
    assert facts["mass"] == "1799999/100000"
    assert facts["oblique_records"] == 415


def test_the_bundle_receipt_binds_every_oblique_input_to_the_declared_net() -> None:
    record = json.loads((declared.RECEIPTS / "bundle.json").read_text(encoding="utf-8"))
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert (record["listed_files"], record["code_files"]) == (1266, 10)
    assert record["oblique_inputs"] == 415
    assert record["rectangle_images"] == 8 * 136
    assert record["upstream_oblique_nodes"] == declared.audit()["oblique_nodes"]


def copy_directory(tmp_path: Path) -> Path:
    """The retained files as plain JSON in a scratch directory."""
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        (tmp_path / name).write_bytes(read_retained_bytes(declared.DIRECTORY / name))
    return tmp_path


def edit(directory: Path, name: str, change: Any) -> None:
    path = directory / name
    value = json.loads(path.read_text(encoding="utf-8"), parse_float=str)
    change(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def coarser_step(value: dict[str, Any]) -> None:
    # B (1 + 1/999) = 1 exactly: the core need not fit inside the unit square.
    value["proof_net"]["step"] = "1/999"


def short_net(value: dict[str, Any]) -> None:
    # t = 414/1001 < tan(pi/8): the net stops short of pi/4.
    value["proof_net"]["last"] = 414


def offset_field(value: dict[str, Any]) -> None:
    value["proof_net"]["offset"] = "1/2002"


def heavier_row(value: dict[str, Any]) -> None:
    row = value["rectangles"][0]
    row["mass"] = str(Fraction(row["mass"]) + Fraction(1, 10**9))


def stated_endpoint(value: dict[str, Any]) -> None:
    value["net"]["endpoint"] = "414/1001"


def missing_record(value: dict[str, Any]) -> None:
    del value["results"]["207"]


@pytest.mark.parametrize(
    ("name", "change", "message"),
    [
        ("candidate.json", coarser_step, "lemma N0"),
        ("candidate.json", short_net, "lemma N0"),
        ("candidate.json", offset_field, "proof_net has fields"),
        ("candidate.json", heavier_row, "total_mass"),
        ("manifest.json", stated_endpoint, "manifest net endpoint"),
        ("certificate.json", missing_record, "no record"),
    ],
)
def test_a_changed_copy_is_refused(
    tmp_path: Path, name: str, change: Any, message: str
) -> None:
    directory = copy_directory(tmp_path)
    assert declared.audit(directory)["status"] == "EXACT_PREMISES_HOLD"
    edit(directory, name, change)
    with pytest.raises(declared.AuditError, match=message):
        declared.audit(directory)


def shipped_tree(root: Path) -> dict[str, Any]:
    """A bundle tree holding what ``compare`` reads, the records being the retained
    certificate's; file times are a day before any run."""
    certificate = json.loads(read_retained_bytes(declared.DIRECTORY / "certificate.json"))
    for r in range(416):
        path = root / declared.record_name(r)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(certificate["results"][str(r)]), encoding="utf-8")
    (root / "proof/certificate.json").write_bytes(
        read_retained_bytes(declared.DIRECTORY / "certificate.json")
    )
    (root / "proof/net001/input.txt").write_text("unchanged", encoding="utf-8")
    (root / "bundle.json").write_text(
        json.dumps(
            {
                "status": "REPLAYED_PROOF_BUNDLE",
                "certificate": "ALL_ANGLES_VERIFIED_AND_REPLAYED",
            }
        ),
        encoding="utf-8",
    )
    for path in root.rglob("*"):
        os.utime(path, (1_790_000_000, 1_790_000_000))
    return certificate


def replay(shipped: Path, fresh: Path, certificate: dict[str, Any]) -> Path:
    """A copy of ``shipped`` after a complete run: every record written again, the
    certificate rewritten in another order, the progress record, the driver's binary and
    the runner's record. Returns the runner's record."""
    shutil.copytree(shipped, fresh)
    for r in range(416):
        (fresh / declared.record_name(r)).write_text(
            json.dumps(certificate["results"][str(r)]), encoding="utf-8"
        )
    reordered = {**certificate, "results": dict(reversed(certificate["results"].items()))}
    (fresh / "proof/certificate.json").write_text(json.dumps(reordered), encoding="utf-8")
    (fresh / "proof/replay-progress.json").write_text('{"done": 416, "total": 416}')
    (fresh / declared.DRIVER_BINARY).write_bytes(b"binary")
    meta = fresh.parent / "run.meta"
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 0\nend: 2026-10-05T22:00:00Z\n")
    return meta


def test_a_complete_replay_matches_whatever_order_it_rewrites_the_certificate_in(
    tmp_path: Path,
) -> None:
    """Finding DN-1's second probe: the driver rewrites the certificate with its records
    in another order, which is the same certificate."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    result = declared.compare(shipped, fresh, meta)
    assert result["status"] == "FULL_REPLAY_MATCHES_SHIPPED", result["differing"]
    assert result["records_matching"] == 416
    assert result["certificate_rewritten"]


def test_a_copy_on_which_nothing_ran_does_not_match(tmp_path: Path) -> None:
    """Finding DN-1's first probe: a copy made without keeping file times, on which no
    replay ran, has every record newer than the shipped one and equal to it."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    shipped_tree(shipped)
    shutil.copytree(shipped, fresh, copy_function=shutil.copy)
    meta = tmp_path / "run.meta"
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 0\n")
    result = declared.compare(shipped, fresh, meta)
    assert result["status"] == "MISMATCH"
    assert any("progress record" in line for line in result["differing"])
    assert any("binary" in line for line in result["differing"])


def test_a_replay_with_a_changed_or_stale_record_does_not_match(tmp_path: Path) -> None:
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    changed = fresh / declared.record_name(207)
    changed.write_text(json.dumps({**certificate["results"]["207"], "nodes": 1}))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/net207/replayed.json: differs from the shipped record"
    ]
    os.utime(changed, (1_790_000_000, 1_790_000_000))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/net207/replayed.json: not written by this run"
    ]
    (fresh / "proof/net001/input.txt").write_text("changed", encoding="utf-8")
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 1\n")
    differing = declared.compare(shipped, fresh, meta)["differing"]
    assert "the run did not exit zero: 1" in differing
    assert "proof/net001/input.txt: changed by the replay" in differing


def enclosing_lines(candidate: dict[str, Any]) -> list[str]:
    """Rectangle lines in the input's layout that enclose the expanded candidate."""
    side = Fraction(candidate["L"])
    lines = []
    for row in candidate["rectangles"]:
        corners = [Fraction(value) for value in row["rectangle"]]
        area = (corners[2] - corners[0]) * (corners[3] - corners[1])
        density = Fraction(row["mass"]) / 8 / area
        for image in declared.orbit(side, corners):
            fields = []
            for exact in (*image, density):
                value = float(exact)
                fields += [
                    math.nextafter(value, -math.inf).hex(),
                    math.nextafter(value, math.inf).hex(),
                ]
            lines.append(" ".join(fields))
    return [*lines, "0"]


def test_rectangle_lines_must_enclose_every_image_of_every_row() -> None:
    candidate = json.loads(read_retained_bytes(declared.DIRECTORY / "candidate.json"))
    lines = enclosing_lines(candidate)
    declared.rectangle_block(candidate, lines)
    record = json.loads((declared.RECEIPTS / "bundle.json").read_text(encoding="utf-8"))
    assert record["rectangle_lines"] == "ENCLOSE_THE_EXPANDED_CANDIDATE"
    heavier = list(lines)
    fields = heavier[0].split()
    fields[8:10] = [(float.fromhex(fields[9]) * 2).hex(), (float.fromhex(fields[9]) * 3).hex()]
    heavier[0] = " ".join(fields)
    with pytest.raises(declared.AuditError, match="encloses none of its images"):
        declared.rectangle_block(candidate, heavier)
    with pytest.raises(declared.AuditError, match="point count"):
        declared.rectangle_block(candidate, [*lines[:-1], "1"])
    twice = [lines[0], *lines[0:7], *lines[8:]]
    with pytest.raises(declared.AuditError, match="encloses none of its images"):
        declared.rectangle_block(candidate, twice)
