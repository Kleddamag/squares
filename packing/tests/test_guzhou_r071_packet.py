"""The R070 and R071 packet holds the pinned bytes, and its pre-replay claims re-derive.

Both certificates are Guzhou0806's continuations of R068's charge (T-043) at smaller
parents. These tests read the retained files only: the acquisition record and every
package manifest, what each certificate changes relative to R068, R070's published
ledgers row by row and R071's completion summary; then stage 4's complete paired replay
of R071, whose fresh C++ and BigInt ledgers are compared row by row, and its two
mutated-certificate controls. No sweep runs here: the replay and the controls are the
packet's receipts, run by ``devtools.replay_guzhou_r071``.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_guzhou_r071 as audit
from devtools import replay_guzhou_r071 as driver
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
    assert result["consistent"]
    assert len(set(result["triples_sha256"].values())) == 1
    recorded = json.loads((RECEIPTS / "r070/published-ledgers.json").read_text())
    assert recorded == result


def test_a_theorem_that_disagrees_with_its_ledgers_fails_the_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Rows that agree are not enough: a THEOREM.json reporting another status fails."""
    release = audit.RELEASES["R070"]
    for stored in release.published.iterdir():
        (tmp_path / stored.name).write_bytes(stored.read_bytes())
    theorem = json.loads((tmp_path / "THEOREM.json").read_text(encoding="utf-8"))
    theorem["status"] = "FAIL"
    (tmp_path / "THEOREM.json").write_text(json.dumps(theorem), encoding="utf-8")
    moved = audit.Release(
        release.commit,
        release.package,
        release.certificate,
        release.sha256,
        tmp_path,
        release.target,
        release.intervals,
    )
    monkeypatch.setitem(audit.RELEASES, "R070", moved)
    assert audit.main(["ledgers"]) == 1
    printed = json.loads(capsys.readouterr().out)
    assert printed["mismatches"] == 0
    assert printed["theorem_agrees"]["status"] is False
    assert printed["consistent"] is False


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


# --------------------------------------------------------------- stage 4: the replay

REPLAY = RECEIPTS / "r071/replay"
CONTROLS = RECEIPTS / "r071/controls"
#: The executable R068's replay here built from the same ``verify.cpp``, Boost and g++.
R068_EXECUTABLE = "cf761bb5d19ba01be76853c7e6bd47648a8ff5c29624d02f9cc02d730cc719d5"
CONTROL_CWD = re.compile(
    r"^# cwd: .*; certificate (?P<mutated>[0-9a-f]{64}), the (?P<kind>\S+) mutation of "
    r"(?P<original>[0-9a-f]{64}) \(bounds/c027/certificate\.json\): (?P<change>.*); "
    r"intervals (?P<start>\d+) to (?P<end>\d+); C\+\+ executable (?P<exe>[0-9a-f]{64})$",
    re.MULTILINE,
)
FOOTER = re.compile(r"^# finished \S+; exit (?P<exit>\d+); ", re.MULTILINE)
#: What each checker prints when it refuses each mutation, and the exit it refuses with.
REFUSALS = {
    ("over-claim", "cpp"): ("REJECT: non-strict core", 1),
    ("over-claim", "bigint"): ("Error: strict core", 1),
    ("drop-rule", "cpp"): ("FAIL_INTERVAL_COVERAGE", 2),
    ("drop-rule", "bigint"): ('"status":"EXACT_INTERVAL_COVERAGE_FAILURE"', 2),
}


def test_the_driver_stages_every_file_the_bound_reads() -> None:
    """The packet holds the certificate and launchers, and names a copy of each checker."""
    digests = driver.subtree_digests()
    copies = driver.pinned_copies()
    assert len(digests) == 123
    for relative in (driver.CERTIFICATE, "run_public.js", "check_package.js"):
        retained = audit.SOURCE_ROOT / driver.PACKAGE / relative
        assert hashlib.sha256(read_retained_bytes(retained)).hexdigest() == digests[relative]
    for relative in (driver.VERIFY, driver.BIGINT, "project/base/upstream/cpp/replay.js"):
        data = read_retained_bytes(copies[relative])
        assert hashlib.sha256(data).hexdigest() == digests[relative]


def test_the_fresh_replay_passes_with_the_claimed_values() -> None:
    theorem = json.loads((REPLAY / "THEOREM.json").read_text(encoding="utf-8"))
    assert theorem["status"] == "PASS_COMPLETE_CPP_AND_BIGINT_EXCLUSION"
    assert theorem["target"] == "18641771/4000000"
    assert theorem["intervals"] == 5114
    assert (theorem["minimum_units"], theorem["budget_units"]) == ("1000026844", "17000448944")
    assert theorem["surplus"] == "7404"
    assert theorem["certificate_sha256"] == audit.RELEASES["R071"].sha256
    assert all(p["exit"] == 0 and not p["expired"] for p in theorem["processes"])
    inputs = json.loads((REPLAY / "INPUTS.json").read_text(encoding="utf-8"))
    assert inputs["executable_sha256"] == R068_EXECUTABLE
    cpp = audit.R068_CPP
    assert (
        inputs["reference_sha256"]
        == hashlib.sha256(
            read_retained_bytes(cpp / "reference/verify_global_variable.js")
        ).hexdigest()
    )
    assert (
        inputs["launcher_sha256"]
        == hashlib.sha256(read_retained_bytes(cpp / "replay.js")).hexdigest()
    )
    replay = json.loads((REPLAY / "REPLAY.json").read_text(encoding="utf-8"))
    assert replay["status"] == "PASS_R071_C027_GLOBAL_REPLAY"
    assert [r["exit"] for r in replay["records"]] == [0, 0]


def test_the_fresh_cpp_and_bigint_ledgers_agree_row_by_row() -> None:
    result = audit.r068.compare("R071", REPLAY, REPLAY, release=audit.RELEASES["R071"])
    assert result["mismatches"] == 0
    assert result["ledgers_compared"] == 4
    assert result["minimum_units"] == 1000026844
    assert result["surplus_units"] == 7404
    assert len(set(result["triples_sha256"].values())) == 1
    header = result["cpp_headers"]["fresh"]
    assert (header["sites"], header["signed_terms"]) == (20860, 49208)
    recorded = json.loads((RECEIPTS / "r071/compare.json").read_text(encoding="utf-8"))
    assert recorded == result


@pytest.mark.parametrize("kind", sorted(driver.MUTATIONS))
def test_each_checker_refuses_each_mutated_certificate(kind: str) -> None:
    """Stage 4's two negative controls: what changed, and that both checkers refuse it."""
    original = read_retained_bytes(audit.RELEASES["R071"].certificate)
    data, change = driver.mutate(kind, original)
    for checker in ("cpp", "bigint"):
        text = (CONTROLS / f"control-{kind}-{checker}.log").read_text(encoding="utf-8")
        found = CONTROL_CWD.search(text)
        assert found is not None
        assert found["kind"] == kind
        assert found["original"] == audit.RELEASES["R071"].sha256
        assert found["mutated"] == hashlib.sha256(data).hexdigest()
        assert found["change"] == change
        assert found["exe"] == R068_EXECUTABLE
        message, code = REFUSALS[kind, checker]
        assert message in text
        footer = FOOTER.search(text)
        assert footer is not None
        assert int(footer["exit"]) == code


def test_the_over_claim_moves_only_the_parent_side() -> None:
    retained = read_retained_bytes(audit.RELEASES["R071"].certificate)
    original = json.loads(retained)
    mutated = json.loads(driver.mutate("over-claim", retained)[0])
    assert Fraction(mutated["normalized_target"]) == Fraction(9321, 2000)
    assert Fraction(mutated["A"]) < Fraction(original["A"])
    assert mutated["entries"] == original["entries"]
    assert mutated["budget_units"] == original["budget_units"]


def test_the_dropped_rule_is_refused_by_the_sweep_not_the_count() -> None:
    """The mutated budget still passes the counting check, so the refusal is the sweep's."""
    mutated = json.loads(
        driver.mutate("drop-rule", read_retained_bytes(audit.RELEASES["R071"].certificate))[0]
    )
    assert 17 * mutated["minimum_units"] > mutated["budget_units"]
    for checker in ("cpp", "bigint"):
        record = json.loads((CONTROLS / f"control-drop-rule-{checker}.json").read_text())
        refused = [
            r for r in record["rows"] if int(r["minimum_units"]) < mutated["minimum_units"]
        ]
        assert refused
        assert refused[0]["interval"] == 0
