"""The first-party audit of wand125's mixed certificate on a declared net (jlevy/squares#366).

`devtools.audit_wand125_declared_net` recomputes `mixed_n18_L470`'s exact premises from
the retained files, lemma N0's five among them, and refuses a copy whose net, mass or
stated facts are changed. Its bundle receipt binds the source's own runs to the declared
net, and its comparison passes a replay only when every regenerated record is the
shipped one.
"""

from __future__ import annotations

import json
import os
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


def fake_replay(root: Path, *, regenerated: bool, record: dict[str, Any]) -> None:
    """A bundle tree holding only the records ``compare`` reads."""
    for r in range(416):
        name = "proof/axis/replayed.json" if r == 0 else f"proof/net{r:03d}/replayed.json"
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({**record, "index": r}), encoding="utf-8")
        if not regenerated:
            os.utime(path, (1_000_000_000, 1_000_000_000))
    (root / "proof/input-like.txt").write_text("unchanged", encoding="utf-8")
    (root / "bundle.json").write_text(
        json.dumps({"status": "REPLAYED_PROOF_BUNDLE", "certificate": "ALL"}), encoding="utf-8"
    )


def test_a_replay_matches_only_when_every_record_is_regenerated_and_equal(
    tmp_path: Path,
) -> None:
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    fake_replay(shipped, regenerated=False, record={"status": "ANGLE_RESULT_REPLAYED"})
    fake_replay(fresh, regenerated=True, record={"status": "ANGLE_RESULT_REPLAYED"})
    result = declared.compare(shipped, fresh)
    assert result["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert result["records_matching"] == 416
    changed = fresh / "proof/net207/replayed.json"
    changed.write_text(json.dumps({"status": "ANGLE_RESULT_REPLAYED", "index": 0}))
    result = declared.compare(shipped, fresh)
    assert result["status"] == "MISMATCH"
    assert result["differing"] == ["proof/net207/replayed.json: differs"]
    os.utime(changed, (1_000_000_000, 1_000_000_000))
    assert declared.compare(shipped, fresh)["differing"] == [
        "proof/net207/replayed.json: not regenerated"
    ]


def test_a_replay_that_changes_a_shipped_file_does_not_match(tmp_path: Path) -> None:
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    fake_replay(shipped, regenerated=False, record={"status": "ANGLE_RESULT_REPLAYED"})
    fake_replay(fresh, regenerated=True, record={"status": "ANGLE_RESULT_REPLAYED"})
    (fresh / "proof/input-like.txt").write_text("changed", encoding="utf-8")
    result = declared.compare(shipped, fresh)
    assert result["differing"] == ["proof/input-like.txt: changed by the replay"]
