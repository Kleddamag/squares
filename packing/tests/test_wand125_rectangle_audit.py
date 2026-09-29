"""wand125's rectangle-density certificates: pins, input binding, and the bounds they carry."""

from __future__ import annotations

import json
import shutil
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import apply_wand125_rectangles as apply
from devtools import audit_tokoharu_density as tokoharu
from devtools.audit_wand125_rectangles import (
    CASES,
    CASES_2026_09_28,
    PACKETS,
    SEPTEMBER_27,
    SEPTEMBER_28,
    audit_case,
    materialize,
    monotone_bounds,
    read_tree_manifest,
    source_provenance,
    standing,
)
from devtools.retained_data import (
    candidates,
    check_packet,
    compressed_path,
    read_retained_bytes,
    read_retained_text,
)
from sqpack.yamlio import safe_load

FRONTIER = Path(__file__).resolve().parents[1] / "frontier"
#: The two smallest interval inputs, so regeneration stays well inside the test ceiling.
SMALL = (21, 32)
#: The standing certificates 39d8ecc left byte-identical to ad43d29's.
UNCHANGED = (18, 19, 20, 26, 27, 30, 32, 40, 45, 61, 75, 78)


def _payload(n: int, frontier: Path = FRONTIER) -> dict:
    text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n", 2)[1])["packing"]


def _value(field: dict) -> Fraction:
    return Fraction(Decimal(str(field["value"])))


@pytest.mark.parametrize(
    ("date", "upstream", "retained", "referenced"),
    [("2026-09-27", 1367, 184, None), ("2026-09-28", 2295, 153, 55)],
)
def test_retained_subset_matches_the_pinned_tree(
    date: str, upstream: int, retained: int, referenced: int | None
) -> None:
    packet = PACKETS[date]
    provenance = source_provenance(packet, packet.source)
    assert provenance["kind"] == "verified-retained-subset"
    assert provenance["upstream_files"] == upstream
    assert provenance["files_verified"] == retained
    assert provenance.get("files_referenced") == referenced


def test_the_later_pin_only_adds_files_except_its_readme() -> None:
    earlier = read_tree_manifest(SEPTEMBER_27.tree_manifest)
    later = read_tree_manifest(SEPTEMBER_28.tree_manifest)
    assert {path for path, digest in earlier.items() if later.get(path) != digest} == {
        Path("README.md")
    }


def test_unchanged_certificates_are_read_from_the_earlier_packet() -> None:
    same = {n for n, case in CASES_2026_09_28.items() if CASES.get(n) == case}
    assert same == set(UNCHANGED)
    for n, (name, side) in CASES_2026_09_28.items():
        assert n not in CASES or side >= CASES[n][1]
        here = SEPTEMBER_28.source / "certificates" / name
        assert here.is_dir() == (n not in same)
        expected = SEPTEMBER_27.source if n in same else SEPTEMBER_28.source
        assert SEPTEMBER_28.case_directory(SEPTEMBER_28.source, name) == (
            expected / "certificates" / name
        )


@pytest.mark.parametrize("date", tuple(PACKETS))
@pytest.mark.parametrize("n", SMALL)
def test_regenerated_input_is_the_published_input(date: str, n: int, tmp_path: Path) -> None:
    packet = PACKETS[date]
    name, side = packet.cases[n]
    case = packet.case_directory(packet.source, name)
    binding = materialize(case, tmp_path / name)
    assert (
        binding["input_sha256"]
        == tokoharu.load_json(case / "certificate_metadata.json")["input_sha256"]
    )
    report = tokoharu.preflight(tmp_path / name, n, side)
    assert report["status"] == "PASS"
    assert Fraction(report["mass_exact"]) == n - Fraction(1, 1000 if n in {21, 27} else 100)


def test_a_changed_weight_breaks_the_input_binding(tmp_path: Path) -> None:
    name, _side = CASES[32]
    case = tmp_path / "case"
    shutil.copytree(SEPTEMBER_27.source / "certificates" / name, case)
    path = case / "certified_candidate.json"
    data = json.loads(read_retained_bytes(path))
    compressed_path(path).unlink()
    index = next(i for i, weight in enumerate(data["weights"]) if Fraction(weight) > 0)
    data["weights"][index] = str(Fraction(data["weights"][index]) * 2)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="published SHA-256"):
        materialize(case, tmp_path / "scratch")


def test_a_side_other_than_the_pinned_one_is_refused(tmp_path: Path) -> None:
    name, side = CASES[21]
    materialize(SEPTEMBER_27.source / "certificates" / name, tmp_path / name)
    with pytest.raises(ValueError, match="side mismatch"):
        tokoharu.preflight(tmp_path / name, 21, side + Fraction(1, 200))


def test_a_candidate_naming_another_count_is_refused(tmp_path: Path) -> None:
    name, _side = CASES_2026_09_28[21]
    case = tmp_path / "certificates" / name
    shutil.copytree(SEPTEMBER_28.source / "certificates" / name, case)
    path = case / "certified_candidate.json"
    data = json.loads(read_retained_bytes(path))
    compressed_path(path).unlink()
    path.write_text(json.dumps(data | {"n": 22}))
    with pytest.raises(ValueError, match="does not declare n = 21"):
        audit_case(
            SEPTEMBER_28, tmp_path, 21, tmp_path / "out", run_replay=False, workers=1, timeout=1
        )


def test_the_standing_certificate_is_the_highest_and_unambiguous(tmp_path: Path) -> None:
    for name, n, side in (("rect_n5_L2", 5, "2.0"), ("rect_n5_L21", 5, "2.1")):
        (tmp_path / "certificates" / name).mkdir(parents=True)
        (tmp_path / "certificates" / name / "certified_candidate.json").write_text(
            f'{{"n": {n}, "L": {side}}}'
        )
    assert standing(tmp_path) == {5: ("rect_n5_L21", Fraction(21, 10))}
    (tmp_path / "certificates" / "rect_n5_L210").mkdir()
    (tmp_path / "certificates" / "rect_n5_L210" / "certified_candidate.json").write_text(
        '{"n": 5, "L": 2.10}'
    )
    with pytest.raises(ValueError, match="share the standing side"):
        standing(tmp_path)


def test_monotone_transfers_follow_the_mass() -> None:
    earlier = monotone_bounds({n: side for n, (_name, side) in CASES.items()})
    assert earlier[77] == (Fraction(89, 10), 76)
    assert all(earlier[n][1] == n for n in CASES if n != 77)
    later = monotone_bounds({n: side for n, (_name, side) in CASES_2026_09_28.items()})
    assert all(later[n][1] == n for n in CASES_2026_09_28 if n != 77)
    inherited = {n: later[n][1] for n in later if later[n][1] != n}
    assert inherited == {
        **dict.fromkeys(range(22, 26), 21),
        **dict.fromkeys(range(33, 37), 32),
        **dict.fromkeys(range(46, 51), 45),
        **dict.fromkeys(range(62, 66), 61),
        77: 76,
        **dict.fromkeys(range(79, 86), 78),
        87: 86,
        90: 89,
        92: 91,
        93: 91,
    }
    assert monotone_bounds({27: Fraction(28, 5)}, upto=29)[29] == (Fraction(28, 5), 27)


@pytest.mark.parametrize("date", tuple(PACKETS))
def test_preflight_receipt_covers_every_standing_certificate(date: str) -> None:
    packet = PACKETS[date]
    record = json.loads(read_retained_text(packet.directory / "receipts/preflight/audit.json"))
    assert record["status"] == "PASS"
    assert record["source_revision"] == packet.revision
    assert record["provenance"]["kind"] == "verified-retained-subset"
    assert {
        case["n"]: (case["certificate"], Fraction(case["L"])) for case in record["cases"]
    } == (dict(packet.cases))
    for case in record["cases"]:
        assert Fraction(case["mass_exact"]) < case["n"]
        directory = packet.case_directory(packet.source, case["certificate"])
        metadata = tokoharu.load_json(directory / "certificate_metadata.json")
        assert case["input_sha256"] == metadata["input_sha256"]


@pytest.mark.parametrize("date", tuple(PACKETS))
def test_every_compressed_file_matches_its_table_row(date: str) -> None:
    assert check_packet(PACKETS[date].directory) == []
    assert candidates(PACKETS[date].directory) == []


@pytest.mark.parametrize(
    "date",
    [
        date
        for date, packet in PACKETS.items()
        if (packet.directory / "receipts/replay").is_dir()
    ],
)
def test_replay_receipt_records_complete_accepting_runs(date: str) -> None:
    packet = PACKETS[date]
    replays = packet.directory / "receipts/replay"
    record = json.loads(read_retained_text(replays / "audit.json"))
    preflight = {
        case["n"]: case["input_sha256"]
        for case in json.loads(
            read_retained_text(packet.directory / "receipts/preflight/audit.json")
        )["cases"]
    }
    assert record["cases"]
    for case in record["cases"]:
        summary = case["replay"]["summary"]
        assert case["status"] == "PASS"
        assert summary["status"] == "VERIFIED"
        assert summary["angle_cases"] == 201
        assert summary["input_sha256"] == case["input_sha256"] == preflight[case["n"]]
        assert (
            summary["verifier_source_sha256"]
            == tokoharu.load_json(replays / case["certificate"] / "verification_summary.json")[
                "verifier_source_sha256"
            ]
        )
        rows = (replays / case["certificate"] / "verified_angles.jsonl").read_text()
        assert sorted(json.loads(line)["r"] for line in rows.splitlines()) == list(range(201))


def test_frontier_records_carry_exactly_the_certified_bounds() -> None:
    """Reported lane: every standing certificate; verified lane: only replayed ones."""
    registration = apply.registered()
    cases = registration.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    proofs = apply.replays(registration)
    verified = (
        monotone_bounds({n: side for n, (side, _) in proofs.items()}, upto=max(cases))
        if proofs
        else {}
    )
    for n, (side, source) in reported.items():
        payload = _payload(n)
        field = payload["reported_lower_bound"]
        if not set(field["evidence"]) & apply.OURS:
            # Another source's report holds here, at least as strong.
            assert n in registration.superseded_priors or _value(field) >= side
        else:
            holder = apply.owner(cases[source][0])
            assert Fraction(field["exact_form"]) == side
            assert field["source_key"] == holder.source_key
            assert field["evidence"] == [
                holder.report if source == n else holder.monotone_report
            ]
        lower = payload["verified_lower_bound"]
        if set(lower["evidence"]) & apply.OURS:
            proof, origin = verified[n]
            assert Fraction(lower["exact_form"]) == proof
            assert lower["evidence"] == [proofs[origin][1].replay]
        else:
            assert n not in verified or _value(lower) >= verified[n][0]


def test_records_are_what_the_apply_tool_writes() -> None:
    registration = apply.registered()
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in FRONTIER.glob("n-*.md")
    }
    for plan in apply.plans(registration):
        assert apply.apply_case(plan, registration) == texts[plan.n], plan.n
    evidence = (FRONTIER / "evidence.yaml").read_text(encoding="utf-8")
    assert apply.update_evidence(evidence, registration, texts) == evidence


def test_an_older_registration_is_refused_once_a_newer_one_holds(tmp_path: Path) -> None:
    newest = apply.REGISTRATIONS[-1]
    (tmp_path / "n-001.md").write_text(f"---\n  evidence:\n  - {newest.report}\n---\n")
    assert apply.registered(tmp_path) is newest
    with pytest.raises(ValueError, match="older"):
        apply.plans(apply.REGISTRATIONS[0], tmp_path)


def _register(registration: apply.Registration, frontier: Path) -> list[int]:
    written = []
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in frontier.glob("n-*.md")
    }
    for plan in apply.plans(registration, frontier):
        rendered = apply.apply_case(plan, registration, frontier)
        if rendered != texts[plan.n]:
            written.append(plan.n)
            texts[plan.n] = rendered
            (frontier / f"n-{plan.n:03d}.md").write_text(rendered, encoding="utf-8")
    evidence = frontier / "evidence.yaml"
    evidence.write_text(
        apply.update_evidence(evidence.read_text(encoding="utf-8"), registration, texts),
        encoding="utf-8",
    )
    return written


def test_registering_the_newest_packet_is_idempotent_and_never_lowers(tmp_path: Path) -> None:
    """A dry run of the newest registration on a copy of the records.

    Before the real registration it moves the raised and new counts; after it, it is a
    no-op. Either way a second pass writes nothing, and no lower bound falls.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.REGISTRATIONS[-1]
    counts = range(min(newest.packet.cases), max(newest.packet.cases) + 1)
    before = {n: _payload(n, frontier) for n in counts}
    written = _register(newest, frontier)
    for n in counts:
        payload = _payload(n, frontier)
        for field in ("reported_lower_bound", "verified_lower_bound"):
            assert _value(payload[field]) >= _value(before[n][field]), (n, field)
    for n in written:
        body = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8").split("---\n", 2)[2]
        assert newest.intake in body
    assert _register(newest, frontier) == []
