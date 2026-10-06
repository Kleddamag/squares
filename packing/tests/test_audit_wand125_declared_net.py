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


@pytest.mark.parametrize("key", sorted(declared.CERTIFICATES))
def test_every_certificate_recomputes_to_its_receipt(key: str) -> None:
    assert declared.main(["audit", "--certificate", key, "--check"]) == 0


def test_the_finer_net_of_6_october_holds_lemma_n0() -> None:
    """mixed_n18_L4704 (T-099): core 1999/2000 on 832 tangents of step 1/2006."""
    facts = declared.audit(key="n18-L4704")
    assert facts["status"] == "EXACT_PREMISES_HOLD"
    assert all(facts["premises"].values())
    assert facts["net"]["step"] == "1/2006"
    assert facts["net"]["count"] == "832"
    assert facts["net"]["rotated_side_upper"] == "4011993/4012000"
    assert facts["net"]["endpoint_check"] == "497/4024036"
    assert (facts["mass"], facts["rectangles"]) == ("1799999/100000", 209)
    assert facts["oblique_records"] == 831
    n19 = declared.audit(key="n19-L48229")
    assert (n19["mass"], n19["rectangles"], n19["oblique_records"]) == (
        "1899999/100000",
        313,
        415,
    )
    assert n19["net"] == declared.audit()["net"]


@pytest.mark.parametrize(
    ("key", "listed", "rows"), [("n18-L4704", 2515, 209), ("n19-L48229", 1267, 313)]
)
def test_each_bundle_of_6_october_is_bound_to_its_net(key: str, listed: int, rows: int) -> None:
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "bundle.json").read_text(encoding="utf-8"))
    facts = declared.audit(key=key)
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert record["certificate"] == stated.name
    assert (record["listed_files"], record["code_files"]) == (listed, 10)
    assert record["oblique_inputs"] == facts["oblique_records"]
    assert record["rectangle_images"] == 8 * rows
    assert record["upstream_oblique_nodes"] == facts["oblique_nodes"]


def test_the_one_retained_driver_differs_from_the_n50_copy_only_in_its_worker_cap() -> None:
    """mixed_n18_L4704's code/verify_mixed_full_proof.py is retained because one line
    differs from the mixed_n50_L740 copy: the bound on --workers, 16 where it was 3."""
    stated = declared.CERTIFICATES["n18-L4704"]
    assert stated.own_code == {"verify_mixed_full_proof.py"}
    own = stated.code_reference("verify_mixed_full_proof.py").read_text().splitlines()
    n50 = (declared.N50_DIRECTORY / "code/verify_mixed_full_proof.py").read_text().splitlines()
    assert len(own) == len(n50)
    changed = [(a, b) for a, b in zip(n50, own, strict=True) if a != b]
    assert len(changed) == 1
    before, after = changed[0]
    assert "assert 1<=a.workers<=3;" in before
    assert after == before.replace("a.workers<=3", "a.workers<=16")


@pytest.mark.parametrize("key", ["n18-L4704", "n19-L48229"])
def test_each_sample_of_the_source_checker_returned_the_shipped_records(key: str) -> None:
    stated = declared.CERTIFICATES[key]
    receipts = sorted((stated.receipts / "sample").glob("nodes-*.json"))
    assert receipts
    for path in receipts:
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["status"] == "SAMPLE_REPLAYED", path.name
        assert record["certificate"] == stated.name
        assert record["binding"]["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
        assert record["candidate_digest"] == declared.audit(key=key)["candidate_digest"]
        assert record["tarball"]["sha256"] == stated.tarball_pin()[0]
        assert [row["index"] for row in record["rows"]] == record["nodes"]
        assert all(row["matches_upstream"] for row in record["rows"]), path.name


@pytest.mark.parametrize("key", ["n18-L4704", "n19-L48229"])
def test_each_corrupted_net_fails_lemma_n0_or_the_format(key: str) -> None:
    """The three corrupted declarations `control` runs the source's net check on."""
    candidate = json.loads(
        read_retained_bytes(declared.CERTIFICATES[key].directory / "candidate.json")
    )
    for label, variant in declared.corrupted_nets(candidate).items():
        net = variant["proof_net"]
        if label == "extra-field":
            assert set(net) == {"step", "last", "offset"}
            continue
        step, count = Fraction(net["step"]), int(net["last"]) + 1
        checks = declared.premises(
            declared.net_facts(Fraction(candidate["B"]), step, count), count
        )
        failing = {name for name, held in checks.items() if not held}
        assert failing == (
            {"b_core_fits", "e_tangent_form"}
            if label == "coarser-step"
            else {"c_reaches_past_pi_over_4"}
        ), (key, label)


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
    meta.write_text(
        "asserts: on\nstart: 2026-10-05T17:16:28Z\nexit: 0\nend: 2026-10-05T22:00:00Z\n"
    )
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


@pytest.mark.parametrize("core", [Fraction(1999, 2000), Fraction(999, 1000)])
def test_the_coarser_net_breaks_the_cores_fit_and_nothing_else(core: Fraction) -> None:
    net = declared.coarser_net(core)
    step, last = Fraction(net["step"]), int(net["last"])
    assert core * (1 + step) >= 1
    # The sharp extent, not only the sufficient test: a core at a bin's edge does not fit
    # strictly inside its unit square (FN-3). At D = (1 - B)/B it still would.
    assert declared.sharp_extent(core, step) >= 1
    assert declared.sharp_extent(core, (1 - core) / core) < 1
    assert declared.reaches_past_pi_over_8(last * step)
    assert not declared.reaches_past_pi_over_8((last - Fraction(1, 2)) * step)


@pytest.mark.parametrize(("key", "index"), [("n18-L4704", 797), ("n19-L48229", 37)])
def test_each_control_is_refused_for_its_own_premise(key: str, index: int) -> None:
    """The source's checker accepts the original at its least recorded bound and refuses
    two mass mutants there, each provably uncovered at an exact witness; the source's net
    check and sqverify-fast refuse each corrupted net for the premise it breaks; and
    sqverify-fast verifies the original and refuses the same two mutants."""
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "control.json").read_text(encoding="utf-8"))
    assert record["status"] == "CONTROLS_REFUSED"
    assert (record["certificate"], record["index"]) == (stated.name, index)
    assert record["checker"]["source_sha256"] == declared.CHECKER_SHA256
    original, *mutants = record["runs"]
    assert original["run"]["verdict"] == "ACCEPTED"
    assert original["run"]["output"]["lower"] == record["shipped_record"]["lower"]
    assert [run["name"] for run in mutants] == ["scale-masses", "near-threshold"]
    for run in mutants:
        assert Fraction(run["witness_coverage_exact"]) < 1, run["name"]
        assert run["run"]["verdict"] == "REFUSED", run["name"]
        assert run["run"]["output"]["status"] == "ANGLE_UNRESOLVED", run["name"]
    assert Fraction(mutants[1]["witness_coverage_exact"]) == 1 - declared.NEAR_THRESHOLD
    assert [item["name"] for item in record["nets"]] == list(declared.NET_REFUSALS)
    candidate = json.loads(read_retained_bytes(stated.directory / "candidate.json"))
    assert record["nets"][0]["proof_net"] == declared.coarser_net(Fraction(candidate["B"]))
    for item in record["nets"]:
        source_rule, admission_rule = declared.NET_REFUSALS[item["name"]]
        assert item["source"]["verdict"] == "REFUSED", item["name"]
        assert source_rule in item["source"]["message"], item["name"]
        assert item["sqverify_fast"]["verdict"] == "REFUSED", item["name"]
        assert admission_rule in item["sqverify_fast"]["stderr"], item["name"]
    fast = json.loads(
        (stated.receipts / "control-sqverify-fast.json").read_text(encoding="utf-8")
    )
    assert fast["status"] == "CONTROLS_REFUSED"
    assert fast["binary_sha256"] == record["sqverify_fast"]
    assert [(run["name"], run["held"]) for run in fast["runs"]] == [
        ("original", True),
        ("scale-masses", True),
        ("near-threshold", True),
    ]


def test_a_run_with_nothing_showing_its_assertions_were_on_does_not_match(
    tmp_path: Path,
) -> None:
    """Finding FN-1 of the 6 October review: the source's checks are asserts, so a run
    whose record and snapshot do not show them on proves nothing."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 0\nend: 2026-10-05T22:00:00Z\n")
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "nothing shows the driver's assertions were on during the run"
    ]
    snapshot = {
        "status": "ASSERTS_ON",
        "taken": "2026-10-05T18:00:00Z",
        "processes": [{"pid": 1}, {"pid": 2}],
    }
    (meta.parent / declared.PROCESSES).write_text(json.dumps(snapshot))
    assert declared.compare(shipped, fresh, meta)["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    # A snapshot taken outside the run, or one that does not show the assertions on,
    # shows nothing about it.
    for changed in ({"taken": "2026-10-05T23:00:00Z"}, {"status": "NOT_SHOWN"}):
        (meta.parent / declared.PROCESSES).write_text(json.dumps(snapshot | changed))
        assert declared.compare(shipped, fresh, meta)["status"] == "MISMATCH"


def test_a_certificate_the_run_did_not_rewrite_does_not_match(tmp_path: Path) -> None:
    """Finding FN-2: the shipped certificate equals the retained one, so an unrewritten
    copy must not count as the driver's output."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    os.utime(fresh / "proof/certificate.json", (1_790_000_000, 1_790_000_000))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/certificate.json: not rewritten by this run"
    ]


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["python3", "code/verify_mixed_full_proof.py", "proof"], "runs asserts"),
        (["python3", "-B", "-c", "import sys"], "runs asserts"),
        (["python3", "-O", "code/verify_mixed_full_proof.py"], "optimizes"),
        (["python3", "-BO", "-c", "x"], "optimizes"),
        (["python3", "-OO", "-m", "x"], "optimizes"),
        (["python3", "-m", "x", "-O"], "runs asserts"),
    ],
)
def test_an_optimizing_command_line_is_recognised(argv: list[str], expected: str) -> None:
    assert declared.optimizing(argv) is (expected == "optimizes")


def test_replay_refuses_to_run_with_assertions_off(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PYTHONOPTIMIZE", "1")
    with pytest.raises(declared.AuditError, match="assertions are off"):
        declared.replay("n18-L4704", tmp_path / "absent.tar.gz", tmp_path, 1, tmp_path)
