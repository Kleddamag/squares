"""The R070 and R071 packet holds the pinned bytes, and its pre-replay claims re-derive.

Both certificates are Guzhou0806's continuations of R068's charge (T-043) at smaller
parents. These tests read the retained files only: the acquisition record and every
package manifest, what each certificate changes relative to R068, R070's published
ledgers row by row and R071's completion summary. No sweep runs here; the full paired
replay of R071 is stage 4 of its import.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_guzhou_r071 as audit
from devtools.retained_data import candidates, check_packet, read_retained_bytes

RECEIPTS = audit.PACKET / "receipts"
#: Root files R071's commit edited after R070's publication record described them.
EDITED_BY_R071 = frozenset(
    {
        "CHANGELOG.md",
        "CITATION.cff",
        "NOTICE.md",
        "README.md",
        "RESULTS.md",
        "docs/EVIDENCE_MAP.md",
        "docs/RELEASE_NOTES.md",
        "docs/REPRODUCIBILITY.md",
        "scripts/check_release_hashes.py",
    }
)


def _pinned() -> dict[str, dict[str, Any]]:
    record = json.loads((audit.PACKET / acquire_source.RECORD).read_text(encoding="utf-8"))
    return {item["path"]: item for item in record["sources"][0]["pinned_only"]}


def _bytes(upstream: str) -> bytes | None:
    """An upstream file's bytes from the packet, or from the copy it names, or None."""
    retained = audit.SOURCE_ROOT / upstream
    if retained.exists() or retained.with_name(retained.name + ".gz").exists():
        return read_retained_bytes(retained)
    twin = _pinned()[upstream].get("identical_to")
    return None if twin is None else read_retained_bytes(acquire_source.REPO / twin)


def _matches(upstream: str, item: dict[str, Any]) -> bool:
    data = _bytes(upstream)
    if data is None:
        return _pinned()[upstream]["sha256"] == item["sha256"]
    return len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"]


@pytest.fixture(scope="module")
def structures() -> dict[str, dict[str, Any]]:
    return {name: audit.structure(name) for name in audit.RELEASES}


def test_the_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(audit.PACKET, acquire_source.REPO) == []
    assert check_packet(audit.PACKET) == []
    assert candidates(audit.PACKET) == []


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_each_package_matches_its_manifest(name: str) -> None:
    package = audit.RELEASES[name].package
    prefix = package.relative_to(audit.SOURCE_ROOT).as_posix()
    files = json.loads(read_retained_bytes(package / "MANIFEST.json"))["files"]
    assert all(_matches(f"{prefix}/{entry}", item) for entry, item in files.items())


def test_publication_records_describe_the_pinned_bytes() -> None:
    root = audit.SOURCE_ROOT
    r071 = json.loads((root / "R071_PUBLICATION.json").read_text(encoding="utf-8"))["files"]
    assert all(_matches(name, item) for name, item in r071.items())
    r070 = json.loads((root / "R070_PUBLICATION.json").read_text(encoding="utf-8"))["files"]
    stale = {name for name, item in r070.items() if not _matches(name, item)}
    assert stale == EDITED_BY_R071


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_each_certificate_keeps_r068s_charge(
    name: str, structures: dict[str, dict[str, Any]]
) -> None:
    shape = structures[name]
    assert shape["charge_is_r068s"]
    assert shape["budget_units"] == 17000448944
    assert (shape["point_orbits"], shape["rule_orbits"]) == (2621, 889)
    assert shape["cores_over_previous"]["shared_same_core"] == 0
    assert (
        shape["cores_over_previous"]["shared_same_core_angle"]
        == shape["cores_over_previous"]["shared_intervals"]
    )


def test_r071_refines_r070_by_seven_bisections(structures: dict[str, dict[str, Any]]) -> None:
    shape = structures["R071"]
    assert shape["advance_over_r068"] == "11/4000000"
    assert shape["advance_over_previous"] == "1/20000000"
    assert shape["declared_base_sha256"] == audit.RELEASES["R070"].sha256
    assert shape["angle_chain_over_previous"]["pieces_per_original"] == {"1": 5100, "2": 7}
    assert shape["angle_chain_over_r068"]["original_intervals"] == 4991


@pytest.mark.parametrize("name", sorted(audit.RELEASES))
def test_structure_receipts_are_current(
    name: str, structures: dict[str, dict[str, Any]]
) -> None:
    recorded = json.loads((RECEIPTS / name.lower() / "structure.json").read_text())
    assert recorded == structures[name]


def test_r070_published_ledgers_agree_row_by_row() -> None:
    result = audit.ledgers()
    assert result["mismatches"] == 0
    assert result["minimum_units"] == 1000026844
    assert result["intervals_at_minimum"] == 5107
    assert result["surplus_units"] == 7404
    assert all(result["theorem_agrees"].values())
    assert len(set(result["triples_sha256"].values())) == 1
    recorded = json.loads((RECEIPTS / "r070/published-ledgers.json").read_text())
    assert recorded == result


def test_r071_summary_names_r068s_checkers() -> None:
    result = audit.summary()
    assert result["consistent"]
    assert result["surplus_units"] == 7404
    recorded = json.loads((RECEIPTS / "r071/summary.json").read_text())
    assert recorded == result


def test_a_changed_published_row_is_reported(tmp_path: Path) -> None:
    release = audit.RELEASES["R070"]
    for kind in ("cpp", "node"):
        for index in range(4):
            name = f"{kind}-{index}.json"
            (tmp_path / name).write_bytes(read_retained_bytes(release.published / name))
    record = json.loads((tmp_path / "node-2.json").read_text())
    record["rows"][5]["minimum_units"] = str(int(record["rows"][5]["minimum_units"]) - 1)
    (tmp_path / "node-2.json").write_text(json.dumps(record))
    result = audit.r068.compare("R070", tmp_path, release.published, release=release)
    assert result["mismatches"] == 1
    assert result["first_mismatches"][0]["interval"] == record["rows"][5]["interval"]


def test_a_summary_for_another_certificate_is_inconsistent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    history = tmp_path / "history"
    history.mkdir()
    source = audit.RELEASES["R071"].published / "C027_GLOBAL_THEOREM.json"
    record = json.loads(read_retained_bytes(source))
    record["certificate_sha256"] = audit.RELEASES["R070"].sha256
    (history / "C027_GLOBAL_THEOREM.json").write_text(json.dumps(record))
    release = audit.RELEASES["R071"]
    moved = audit.Release(
        release.commit,
        release.package,
        release.certificate,
        release.sha256,
        history,
        release.target,
        release.intervals,
    )
    monkeypatch.setitem(audit.RELEASES, "R071", moved)
    result = audit.summary()
    assert not result["consistent"]
    assert not result["checks"]["certificate"]
