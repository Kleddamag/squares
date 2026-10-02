"""Controls for the mixed rectangle-measure certificates of wand125/square-packing-bounds.

`devtools.audit_wand125_point_and_mixed` audits and replays eight of them: n = 50 (T-048),
the five of jlevy/squares#282 (T-069) and the two of its comment of 2 October. Three
families of check stand between a certificate and a recorded replay, and each is held
here to its positive case and to two or more mutated controls that it must refuse:

- **the retained files**: the exact premises the source's statements rest on, from the
  packet's bytes alone;
- **the tarball and its bundle**: the pinned digest before use, whichever route delivered
  the file or whoever supplied it, a safe unpacking, and the bundle's binding to the
  packet before any of its code is imported;
- **the replay receipts**: the per-range records a split replay writes, their merge, and
  the audit's reading of whatever receipts a packet holds.

The range driver is held to its promises with a stand-in for the shipped per-angle
function: each angle recorded as it finishes, an interrupted range resumed where it
stopped, a deadline honoured, a torn last line cut, a finished range not fetched again.
The price is held to its samples. No checker is run here. Coverage is the source
checker's, replayed by `mixed-replay`.
"""

from __future__ import annotations

import concurrent.futures
import dataclasses
import hashlib
import io
import itertools
import json
import shutil
import tarfile
import urllib.error
from email.message import Message
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_wand125_point_and_mixed as audit

G_PACKET = audit.G_PACKET
NAMES = sorted(audit.MIXED, key=lambda name: int(name[1:]))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _repinned(certificate: audit.MixedCertificate, files: dict[str, bytes]) -> dict[Path, str]:
    """The packet's digest list with these files' digests in place of the pinned ones.

    A control built this way passes the pin check, so what refuses it is the content.
    """
    tree = dict(audit.read_subtree_manifest(certificate.subtree))
    for name, data in files.items():
        tree[certificate.directory / name] = _sha256(data)
    return tree


# --------------------------------------------------------------------------- retained files


@pytest.fixture(scope="module")
def audits() -> dict[str, dict[str, Any]]:
    return {name: audit.mixed_certificate(audit.MIXED[name]) for name in NAMES}


@pytest.mark.parametrize("name", NAMES)
def test_each_certificate_has_its_stated_exact_premises(
    audits: dict[str, dict[str, Any]], name: str
) -> None:
    certificate = audit.MIXED[name]
    facts = audits[name]
    assert facts["rectangles"] == certificate.rectangles
    assert Fraction(facts["total_mass"]) == certificate.n - Fraction(1, 100000)
    assert facts["candidate_digest"] == certificate.candidate_digest
    assert facts["checker_sha256"] == audit.N50_CHECKER_SHA256
    assert facts["code_identical_to_n50"]
    assert facts["least_lower"] >= 1
    assert facts["axis_integer_minimum"] >= 1
    assert facts["comparison"]["side_exceeds_green"]


def test_the_least_bounds_are_the_ones_the_sources_state(
    audits: dict[str, dict[str, Any]],
) -> None:
    least = {
        name: (facts["least_lower"], facts["least_lower_at"]) for name, facts in audits.items()
    }
    assert least["n50"] == (1.0000000004625813, 150)
    assert least["n84"] == (1.0000000008975796, 175)
    assert least["n85"] == (1.0000000017271347, 44)
    assert least["n90"] == (1.000000000041986, 122)


def test_n50_agrees_with_its_own_exact_audit(audits: dict[str, dict[str, Any]]) -> None:
    earlier = audit.n50_certificate("L740")
    facts = audits["n50"]
    assert facts["side"] == earlier["side"]
    assert facts["candidate_digest"] == earlier["candidate_digest"]
    assert facts["least_lower"] == earlier["recorded_minimum_lower"]
    assert facts["centre_domains"] == earlier["centre_domains"]


def test_the_g_comparison_value_is_below_greens_bound(
    audits: dict[str, dict[str, Any]],
) -> None:
    """The n = 84 and 85 audits compare with 92667/10000, which is below Green's value."""
    for name in ("n84", "n85"):
        comparison = audits[name]["comparison"]
        assert audits[name]["source_audit"]["compared_with"] == "92667/10000"
        assert comparison["green"] == "Theorem 9, k=9, from n = 82"
        assert not comparison["source_value_exceeds_green"]
        assert comparison["side_exceeds_green"]


def test_the_g_packet_audit_recomputes_to_its_receipt() -> None:
    receipt = G_PACKET / "receipts/mixed-audit.json"
    expected = json.dumps(audit.mixed_audit(G_PACKET), indent=2, default=str) + "\n"
    assert receipt.read_text(encoding="utf-8") == expected


def test_the_g_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(G_PACKET, acquire_source.REPO) == []


def _with_heavier_rectangle(data: bytes) -> bytes:
    candidate = json.loads(data)
    rectangle = candidate["rectangles"][0]
    rectangle["mass"] = str(Fraction(rectangle["mass"]) + Fraction(1, 10**9))
    return json.dumps(candidate).encode()


def test_a_heavier_rectangle_is_refused_even_when_repinned() -> None:
    certificate = audit.MIXED["n84"]
    files = audit.mixed_retained(certificate)
    files["candidate.json"] = _with_heavier_rectangle(files["candidate.json"])
    with pytest.raises(ValueError, match="total mass differs"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))
    with pytest.raises(ValueError, match="not the pinned file"):
        audit.mixed_certificate(certificate, files)


def test_a_changed_angle_record_is_refused_by_the_source_audit() -> None:
    certificate = audit.MIXED["n85"]
    files = audit.mixed_retained(certificate)
    replay = json.loads(files["certificate.json"])
    replay["results"]["44"]["nodes"] += 1
    files["certificate.json"] = json.dumps(replay).encode()
    with pytest.raises(ValueError, match="binds another certificate"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_an_angle_below_one_is_refused_even_with_a_matching_audit() -> None:
    """A forged certificate whose source audit is re-bound to it still fails at the angle."""
    certificate = audit.MIXED["n85"]
    files = audit.mixed_retained(certificate)
    replay = json.loads(files["certificate.json"])
    replay["results"]["44"]["lower"] = 0.9999999999
    files["certificate.json"] = json.dumps(replay).encode()
    source_audit = json.loads(files["completion-audit.json"])
    source_audit["certificate_sha256"] = _sha256(files["certificate.json"])
    files["completion-audit.json"] = json.dumps(source_audit).encode()
    with pytest.raises(ValueError, match="angle 44 is not a replayed record"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_an_audit_naming_another_tarball_is_refused() -> None:
    certificate = audit.MIXED["n37"]
    files = audit.mixed_retained(certificate)
    source_audit = json.loads(files["completion-audit.json"])
    source_audit["archive_sha256"] = "0" * 64
    files["completion-audit.json"] = json.dumps(source_audit).encode()
    with pytest.raises(ValueError, match="binds another tarball"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


# --------------------------------------------------------------------------- tarball, bundle


def _bundle_files(certificate: audit.MixedCertificate) -> dict[str, bytes]:
    """A bundle with the shape of the source's, from the retained bytes, without angles."""
    retained = audit.mixed_retained(certificate)
    files = {f"proof/{name}": retained[name] for name in audit.MIXED_FILES[:3]}
    for path in sorted(audit.MIXED_CODE.iterdir()):
        if path.is_file():
            files[f"code/{path.name}"] = path.read_bytes()
    files["proof/verify.cpp"] = files["code/mixed_rotated_verify.cpp"]
    files["requirements.txt"] = audit.MIXED_REQUIREMENTS.read_bytes()
    return files


def _listed(files: dict[str, bytes]) -> dict[str, bytes]:
    listing = {name: _sha256(data) for name, data in sorted(files.items())}
    return files | {"files-sha256.json": json.dumps(listing, indent=2).encode()}


def _write_bundle(root: Path, files: dict[str, bytes]) -> Path:
    for name, data in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return root


def _tarball(prefix: str, files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in sorted(files.items()):
            member = tarfile.TarInfo(f"{prefix}/{name}")
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    return stream.getvalue()


def _pinned_to(tmp_path: Path, archive: bytes) -> audit.MixedCertificate:
    """n = 84 with a scratch packet whose acquisition files pin ``archive``."""
    real = audit.MIXED["n84"]
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    path = real.upstream_tarball.as_posix()
    digest = _sha256(archive)
    (packet / "acquisition/upstream-subtree.sha256").write_text(f"{digest}  ./{path}\n")
    entry = {"path": path, "bytes": len(archive), "sha256": digest}
    record = {"sources": [{"pinned_only": [entry]}]}
    (packet / "acquisition/sources.json").write_text(json.dumps(record))
    return dataclasses.replace(real, packet=packet)


def test_the_pinned_tarball_unpacks_into_a_bound_bundle(tmp_path: Path) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, _listed(_bundle_files(real)))
    certificate = _pinned_to(tmp_path, archive)
    supplied = tmp_path / "supplied.tar.gz"
    supplied.write_bytes(archive)
    fetched = audit.fetch_tarball(certificate, tmp_path / "work", supplied)
    assert fetched["status"] == "TARBALL_MATCHES_PIN"
    bundle = audit.unpack_bundle(certificate, tmp_path / "work" / real.tarball, tmp_path / "u")
    tree = audit.read_subtree_manifest(real.subtree)
    assert audit.bundle_bindings(real, bundle, tree)["status"] == "BUNDLE_BOUND_TO_PACKET"


@pytest.mark.parametrize("damage", ["flipped", "truncated"])
def test_a_tarball_that_is_not_the_pinned_bytes_is_refused(tmp_path: Path, damage: str) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, _listed(_bundle_files(real)))
    certificate = _pinned_to(tmp_path, archive)
    changed = bytearray(archive)
    if damage == "flipped":
        changed[len(changed) // 2] ^= 1
    else:
        del changed[-10:]
    supplied = tmp_path / "supplied.tar.gz"
    supplied.write_bytes(bytes(changed))
    with pytest.raises(ValueError, match="the pin is"):
        audit.fetch_tarball(certificate, tmp_path / "work", supplied)
    assert not (tmp_path / "work" / real.tarball).exists()
    assert (tmp_path / "work" / f"{real.tarball}.rejected").is_file()


def test_an_archive_member_outside_the_bundle_is_refused(tmp_path: Path) -> None:
    real = audit.MIXED["n84"]
    archive = tmp_path / "escape.tar.gz"
    archive.write_bytes(_tarball("elsewhere", {"README.md": b"not the bundle\n"}))
    with pytest.raises(ValueError, match="unexpected archive member"):
        audit.unpack_bundle(real, archive, tmp_path / "u")


def test_a_bundle_with_other_code_is_refused_even_when_listed(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    files = _bundle_files(real)
    files["code/mixed_net_audit.py"] += b"\n# changed\n"
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match="code/ is not the retained"):
        audit.bundle_bindings(real, bundle)


def test_a_bundle_with_an_unlisted_file_is_refused(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    bundle = _write_bundle(tmp_path / real.bundle, _listed(_bundle_files(real)))
    (bundle / "proof/extra.json").write_text("{}")
    with pytest.raises(ValueError, match="file list fails"):
        audit.bundle_bindings(real, bundle)


def test_a_bundle_with_another_candidate_is_refused_even_when_listed(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    files = _bundle_files(real)
    files["proof/candidate.json"] = _with_heavier_rectangle(files["proof/candidate.json"])
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match=r"proof/candidate\.json is not the retained"):
        audit.bundle_bindings(real, bundle)


# --------------------------------------------------------------------------- replay receipts


def _run(certificate: audit.MixedCertificate, run: str, **changes: Any) -> dict[str, Any]:
    digest, _ = audit.tarball_pin(certificate)
    record: dict[str, Any] = {
        "run": run,
        "certificate": certificate.name,
        "tarball": {"sha256": digest},
        "bindings": {"status": "BUNDLE_BOUND_TO_PACKET"},
        "preconditions": {
            "status": "DRIVER_PRECONDITIONS_HOLD",
            "candidate_digest": certificate.candidate_digest,
        },
        "inputs": {"status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"},
        "environment": {"PYTHONOPTIMIZE": None},
        "host": {"cpu": "test host"},
    }
    return record | changes


def _receipts(
    tmp_path: Path, certificate: audit.MixedCertificate, ranges: list[tuple[int, int]]
) -> Path:
    """Receipts as a faithful split replay writes them: each angle returns its record."""
    shipped = json.loads(audit.mixed_retained(certificate)["certificate.json"])["results"]
    receipts = tmp_path / "receipts"
    for first, last in ranges:
        folder = receipts / audit.range_name(first, last)
        folder.mkdir(parents=True)
        run = f"run-{first}"
        (folder / "runs.jsonl").write_text(json.dumps(_run(certificate, run)) + "\n")
        rows = [
            {
                "run": run,
                "index": index,
                "status": "REPLAYED",
                "report": shipped[str(index)],
                "replayed_sha256": _sha256(json.dumps(shipped[str(index)], indent=2).encode()),
                "cpu_seconds": 1.5,
            }
            for index in range(first, last + 1)
        ]
        (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return receipts


def _rewrite_rows(folder: Path, change: Any) -> None:
    rows = [json.loads(line) for line in (folder / "directions.jsonl").read_text().splitlines()]
    kept = [row for row in map(change, rows) if row is not None]
    (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in kept))


def test_complete_range_receipts_merge_into_a_full_replay(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 99), (100, 150), (151, 200)])
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert merged["angles_replayed"] == 201
    assert merged["cpu_hours"] == pytest.approx(201 * 1.5 / 3600, abs=1e-3)
    summary = audit.range_summary(certificate, receipts / "range-100-150", 100, 150)
    assert summary["status"] == "RANGE_REPLAYED"


def test_an_angle_with_another_node_count_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 175:
            row["report"] = row["report"] | {"nodes": row["report"]["nodes"] + 1}
        return row

    _rewrite_rows(receipts / "range-101-200", change)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "DIFFERS"
    assert merged["refused"] == ["range-101-200: angle 175 REPLAYED"]
    summary = audit.range_summary(certificate, receipts / "range-101-200", 101, 200)
    assert summary["status"] == "DIFFERS"


def test_an_angle_whose_written_record_is_another_is_refused(tmp_path: Path) -> None:
    """The row must carry the digest of the replayed.json the shipped function wrote."""
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 3:
            row["replayed_sha256"] = "2" * 64
        return row

    _rewrite_rows(receipts / "range-000-200", change)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "DIFFERS"
    assert merged["refused"] == ["range-000-200: angle 3 REPLAYED"]


def test_a_missing_angle_leaves_the_replay_incomplete(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])
    _rewrite_rows(receipts / "range-000-100", lambda row: None if row["index"] == 0 else row)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "INCOMPLETE"
    assert merged["missing"] == [0]


def test_a_failed_angle_is_refused_even_when_another_run_passed_it(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    folder = receipts / "range-000-200"
    failed = {"run": "run-0", "index": 7, "status": "FAILED", "report": None, "cpu_seconds": 2}
    with (folder / "directions.jsonl").open("a") as out:
        out.write(json.dumps(failed) + "\n")
    assert audit.mixed_merge(certificate, receipts)["status"] == "DIFFERS"


def test_a_run_on_another_tarball_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    other = _run(certificate, "run-0", tarball={"sha256": "1" * 64})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.mixed_merge(certificate, receipts)


def test_a_row_without_its_run_record_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    (receipts / "range-000-200/runs.jsonl").write_text("")
    with pytest.raises(ValueError, match="has no run record"):
        audit.mixed_merge(certificate, receipts)


def test_a_replay_with_asserts_off_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PYTHONOPTIMIZE", "1")
    with pytest.raises(ValueError, match="assertions are off"):
        audit.replay_runtime()


# --------------------------------------------------------------------------- the plan


@pytest.mark.parametrize("parts", [1, 3, 5])
def test_a_plan_splits_every_angle_into_contiguous_ranges(parts: int) -> None:
    plan = audit.mixed_plan(audit.MIXED["n65"], parts)
    ranges = [tuple(part["range"]) for part in plan["parts"]]
    assert len(ranges) == parts
    assert ranges[0][0] == 0
    assert ranges[-1][1] == audit.N50_LAST
    assert all(left[1] + 1 == right[0] for left, right in itertools.pairwise(ranges))
    shares = [part["share"] for part in plan["parts"]]
    assert sum(shares) == pytest.approx(1, abs=1e-3)
    assert max(shares) <= 1.1 / parts + 0.01


def test_unpacking_replaces_only_the_work_directory(tmp_path: Path) -> None:
    """The replay unpacks into its work directory and replaces only that directory."""
    real = audit.MIXED["n84"]
    archive = tmp_path / "bundle.tar.gz"
    archive.write_bytes(_tarball(real.bundle, {"README.md": b"bundle\n"}))
    into = tmp_path / "work/unpacked"
    stale = into / "stale.txt"
    stale.parent.mkdir(parents=True)
    stale.write_text("left by an earlier run")
    bundle = audit.unpack_bundle(real, archive, into)
    assert bundle == into / real.bundle
    assert not stale.exists()
    shutil.rmtree(into)


# --------------------------------------------------------------------------- transport


def _downloads(
    monkeypatch: pytest.MonkeyPatch, deliveries: dict[str, bytes | None]
) -> list[str]:
    """Stand in for the network: each route either writes its bytes or is refused."""
    tried: list[str] = []

    def deliver(route: str, partial: Path) -> None:
        tried.append(route)
        data = deliveries.get(route)
        if data is None:
            raise urllib.error.HTTPError(route, 403, "Forbidden", Message(), None)
        partial.write_bytes(data)

    def git(_: audit.MixedCertificate, partial: Path) -> str:
        deliver("git", partial)
        return "git"

    monkeypatch.setattr(audit, "_fetch_url", deliver)
    monkeypatch.setattr(audit, "_fetch_git", git)
    return tried


def test_auto_tries_each_address_and_keeps_the_pinned_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    first, second = certificate.urls
    assert first == (
        "https://github.com/wand125/square-packing-bounds/raw/"
        f"{audit.G_REVISION}/certificates/mixed_n84_L940/n84-L9.40-proof-bundle.tar.gz"
    )
    tried = _downloads(monkeypatch, {second: archive})
    fetched = audit.fetch_tarball(certificate, tmp_path / "work")
    assert tried == [first, second]
    assert fetched["origin"] == second
    assert fetched["status"] == "TARBALL_MATCHES_PIN"
    assert len(fetched["refused_routes"]) == 1


@pytest.mark.parametrize("via", ["auto", "url", "git"])
def test_a_route_delivering_other_bytes_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, via: str
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    other = _tarball(real.bundle, {"README.md": b"another bundle\n"})
    _downloads(monkeypatch, dict.fromkeys([*certificate.urls, "git"], other))
    with pytest.raises(ValueError, match="the pin is"):
        audit.fetch_tarball(certificate, tmp_path / "work", via=via)
    assert (tmp_path / "work" / f"{real.tarball}.rejected").is_file()


def test_when_no_route_delivers_the_fetch_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = _pinned_to(tmp_path, b"pinned")
    tried = _downloads(monkeypatch, {})
    with pytest.raises(ValueError, match="no route delivered"):
        audit.fetch_tarball(certificate, tmp_path / "work", via="auto")
    assert tried == [*certificate.urls, "git"]
    assert not (tmp_path / "work" / certificate.tarball).exists()


# --------------------------------------------------------------------------- audit supplements


def test_a_supplied_tarball_is_checked_against_the_pin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    monkeypatch.setitem(audit.MIXED, "n84", certificate)
    supplied = tmp_path / real.tarball
    supplied.write_bytes(archive)
    found = audit.mixed_audit_supplements(certificate.packet, [supplied])
    assert found["tarballs"]["n84"]["status"] == "TARBALL_MATCHES_PIN"
    supplied.write_bytes(archive[:-1])
    with pytest.raises(ValueError, match="the pin is"):
        audit.mixed_audit_supplements(certificate.packet, [supplied])
    elsewhere = tmp_path / "n85-L9.42-proof-bundle.tar.gz"
    elsewhere.write_bytes(archive)
    with pytest.raises(ValueError, match="is not a tarball"):
        audit.mixed_audit_supplements(certificate.packet, [elsewhere])


def test_present_replay_receipts_are_merged_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    assert audit.replay_receipts(certificate, tmp_path / "none") is None
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])
    state = audit.replay_receipts(certificate, receipts)
    assert state is not None
    assert state["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    shutil.rmtree(receipts / "range-101-200")
    partial = audit.replay_receipts(certificate, receipts)
    assert partial is not None
    assert (partial["status"], partial["angles_missing"]) == ("INCOMPLETE", 100)


def test_replay_receipts_with_another_angle_are_refused_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 44:
            row["report"] = row["report"] | {"lower": 0.99}
        return row

    _rewrite_rows(receipts / "range-000-200", change)
    with pytest.raises(ValueError, match="the replay receipts differ"):
        audit.replay_receipts(certificate, receipts)


def test_replay_receipts_from_an_unbound_run_are_refused_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    other = _run(certificate, "run-0", environment={"PYTHONOPTIMIZE": "1"})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.replay_receipts(certificate, receipts)
    other = _run(certificate, "run-0", tarball={"sha256": "1" * 64})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.replay_receipts(certificate, receipts)


def test_each_packets_committed_replay_receipts_merge_without_a_refusal() -> None:
    for name in NAMES:
        state = audit.replay_receipts(audit.MIXED[name])
        assert state is None or state["status"] != "DIFFERS"


# --------------------------------------------------------------------------- the range driver


def _faithful(shipped: dict[str, Any], fail_at: int | None = None) -> Any:
    """A stand-in for the shipped per-angle function, returning the certificate's record."""

    def replay(index: int) -> dict[str, Any]:
        if index == fail_at:
            raise RuntimeError("the session was interrupted")
        record = shipped[str(index)]
        return {
            "index": index,
            "status": "REPLAYED",
            "report": record,
            "replayed_sha256": _sha256(json.dumps(record, indent=2).encode()),
            "cpu_seconds": 2.0,
        }

    return replay


def _drive(
    folder: Path,
    certificate: audit.MixedCertificate,
    span: tuple[int, int],
    replay: Any,
    run: str,
    *,
    deadline: float | None = None,
) -> dict[str, Any]:
    shipped = audit.shipped_results(certificate)
    todo = audit.pending_directions(folder, shipped, *span)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return audit.replay_directions(
            certificate,
            folder,
            span,
            todo,
            lambda index: pool.submit(replay, index),
            workers=1,
            run=run,
            shipped=shipped,
            deadline=deadline,
        )


def test_an_interrupted_range_keeps_each_finished_angle_and_resumes(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    shipped = audit.shipped_results(certificate)
    receipts = tmp_path / "receipts"
    folder = receipts / audit.range_name(0, 12)
    folder.mkdir(parents=True)
    order = audit.pending_directions(folder, shipped, 0, 12)
    assert order[0] == 0
    (folder / "runs.jsonl").write_text(
        json.dumps(_run(certificate, "first"))
        + "\n"
        + json.dumps(_run(certificate, "second"))
        + "\n"
    )
    with pytest.raises(RuntimeError, match="interrupted"):
        _drive(folder, certificate, (0, 12), _faithful(shipped, fail_at=order[4]), "first")
    summary = json.loads((folder / "summary.json").read_text())
    assert (summary["status"], summary["replayed"]) == ("INCOMPLETE", 4)
    assert audit.pending_directions(folder, shipped, 0, 12) == order[4:]
    done = _drive(folder, certificate, (0, 12), _faithful(shipped), "second")
    assert done["status"] == "RANGE_REPLAYED"
    rows = audit.read_jsonl(folder / "directions.jsonl")
    assert sorted(row["index"] for row in rows) == list(range(13))
    assert audit.mixed_merge(certificate, receipts)["missing"] == list(range(13, 201))


def test_a_passed_deadline_starts_no_angle(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    shipped = audit.shipped_results(certificate)
    folder = tmp_path / audit.range_name(5, 9)
    folder.mkdir()
    summary = _drive(folder, certificate, (5, 9), _faithful(shipped), "late", deadline=0.0)
    assert (summary["status"], summary["missing"]) == ("INCOMPLETE", [5, 6, 7, 8, 9])
    assert not (folder / "directions.jsonl").exists()


def test_a_torn_last_line_is_cut_and_its_angle_replayed(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    shipped = audit.shipped_results(certificate)
    receipts = _receipts(tmp_path, certificate, [(10, 14)])
    rows = receipts / "range-010-014/directions.jsonl"
    whole = rows.read_text().splitlines(keepends=True)
    rows.write_text("".join(whole[:3]) + whole[3][:40])
    with pytest.raises(json.JSONDecodeError):
        audit.pending_directions(rows.parent, shipped, 10, 14)
    assert audit.drop_torn_line(rows) == 40
    assert audit.drop_torn_line(rows) == 0
    assert sorted(audit.pending_directions(rows.parent, shipped, 10, 14)) == [13, 14]


def test_a_finished_range_is_not_fetched_again(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"):
        monkeypatch.setenv(name, "1")
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(20, 30)])

    def refuse(*_: Any, **__: Any) -> None:
        raise AssertionError("a finished range fetched its tarball")

    monkeypatch.setattr(audit, "fetch_tarball", refuse)
    summary = audit.mixed_replay(
        certificate, tmp_path / "work", 20, 30, workers=1, receipts=receipts
    )
    assert summary["status"] == "RANGE_REPLAYED"
    assert (receipts / "range-020-030/summary.json").is_file()


# --------------------------------------------------------------------------- the price


def test_the_price_samples_agree_once_scaled_by_rectangles() -> None:
    rate, samples = audit.price_rate()
    for sample in samples:
        assert sample["rate"] == pytest.approx(rate, rel=0.03)
    per_node = [
        sample["rate"] * audit.MIXED[sample["certificate"]].rectangles for sample in samples
    ]
    assert max(per_node) / min(per_node) > 1.3
    price = audit.mixed_price()["certificates"]
    assert set(price) == set(audit.MIXED)
    assert all(row["axis_share"] < 0.01 for row in price.values())
    assert price["n65"]["cpu_hours"] > price["n84"]["cpu_hours"] > price["n37"]["cpu_hours"]
