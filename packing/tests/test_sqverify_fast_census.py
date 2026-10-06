"""The clean-room verifier's mixed census, and its controls on the certificates it decides.

`devtools.sqverify_fast_census --family mixed` keeps, per retained format M or L
certificate, `sqverify-fast`'s verdict at all 201 net directions, and for a certificate
whose verified lower bound rests on that verdict, a control receipt: the original
verified again at its least-bound direction, and two mutants refused there (every mass
scaled by 99/100, and every mass scaled so that the exact capture at the least-bound
leaf's centre is at most one part in a million below 1). `campaign/result-import.md`
asks that two mutated certificates be refused by every checker that accepted the
original, with a test holding them; this is that test for `V-sqverify-fast`.

These tests read the retained receipts, the retained candidates and the evidence
register only; nothing here builds or runs the verifier. Each mutant's capture at the
centre is recomputed here from the receipt's exact capture and factor, so each refusal
is the verifier's correct answer rather than a budget running out, and one receipt's
exact capture is recomputed from the candidate by the exact evaluator written apart
from the crate.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import mixed_exact, net_step, read_raw
from sqpack.yamlio import safe_load

FOLDER = census.CENSUS_ROOT / "census-mixed"
EVIDENCE = census.PROJECT / "frontier/evidence.yaml"
RESULTS = census.PROJECT / "frontier/results.yaml"
VERIFIER = "V-sqverify-fast"
#: How far below lemma F3's cap on an expanded rectangle's density, 2^96, a certificate
#: on the reviewed route stays: eight coinciding images of its densest row at most 2^32.
#: The retained ones are near 2^19, so none is near the cap.
DENSITY_CEILING = 2**32
#: The receipt whose exact capture is recomputed here from the candidate.
RECOMPUTED = "mixed_n67_L848"
#: The retained format M certificate on a declared net (step 1/1001, 416 directions).
DECLARED = "mixed_n18_L470"
#: Lemma N0's cap on a declared net's direction count, its condition (a).
MAX_ANGLE_COUNT = 2**16
#: The `source_sha256` of builds whose crate source a soundness review accepted.
#: `census.REVIEWED_SOURCES` holds the same digests with each one's commit, review and
#: scope, which `--evidence` states; widening the route takes an edit to both.
REVIEWED_SOURCES = frozenset(
    {
        # The source the two reviews of 3 October accepted at 4ddf37d9c.
        "9985c465116631570c873ecc33af126adc6f14c7429a5ed44d922254d3c7f8a7",
        # The same `src/`, `Cargo.lock` and `build.rs`, with `Cargo.toml` changed only by
        # the gate's test profile (IR-4 of the 5 October route review); through e020eb1e2.
        "7c49cf79f2408e745d5a0759caf85768d92c502bb574b95dbc12b81a36e50300",
        # main's crate at 910b6b12c: the declared net of format M (`proof_net`, lemma N0,
        # f007d7afd) with the fixes of the 5 October declared-net review's DN-2, DN-4 to
        # DN-6 and DN-9 (910b6b12c). The soundness review of 6 October
        # (review-2026-10-06-sqverify-fast-declared-net-soundness.md) read the whole diff
        # from e020eb1e2 and accepted it, for standard-net certificates at once; a row on
        # a declared net needs `declared_nets` in `census.REVIEWED_SOURCES` too.
        "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88",
    }
)


@cache
def cases() -> dict[str, census.Case]:
    return {case.certificate: case for case in census.mixed_cases()}


@cache
def entries() -> dict[str, Any]:
    data = json.loads((FOLDER / "census.json").read_text(encoding="utf-8"))
    value: dict[str, Any] = data["cases"]
    return value


@cache
def controls() -> dict[str, dict[str, Any]]:
    return {
        path.name.removesuffix(".control.json"): json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(FOLDER.glob("*/*.control.json"))
    }


@cache
def decided() -> dict[str, dict[str, Any]]:
    """Each evidence entry that `V-sqverify-fast` decides, by its id."""
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    return {
        entry["id"]: entry
        for entry in register["evidence"]
        if VERIFIER in (entry.get("verifiers") or [])
    }


@cache
def cited() -> dict[str, str]:
    """Each evidence entry that `V-sqverify-fast` decides, by the certificate it names."""
    by_path = {
        str(case.candidate.relative_to(census.PROJECT)): name for name, case in cases().items()
    }
    found: dict[str, str] = {}
    for ident, entry in decided().items():
        name = by_path.get(str(entry.get("certificate")))
        assert name is not None, f"{ident}: no mixed census case for its certificate"
        found[ident] = name
    return found


@cache
def citing() -> dict[str, list[dict[str, Any]]]:
    """The register results that cite each evidence id."""
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    found: dict[str, list[dict[str, Any]]] = {}
    for record in register["results"]:
        for ident in record.get("evidence") or []:
            found.setdefault(ident, []).append(record)
    return found


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_every_mixed_census_case_is_verified_at_every_direction_of_its_net() -> None:
    """All 201 directions of the standard net, or every node of the net a certificate
    declares (`mixed_n18_L470`'s 416)."""
    assert entries()
    for name, entry in entries().items():
        least = entry["least_bound_leaf_exact"]
        case = cases()[name]
        total = census.net_directions(case)
        assert entry["status"] == "VERIFIED", name
        assert entry["returncode"] == 0, name
        assert entry["directions_verified"] == total, name
        assert least["clears_threshold"] is True, name
        assert Fraction(least["exact_coverage"]) >= Fraction(entry["threshold"]), name
        assert entry["candidate_sha256"] == sha256(case.candidate), name
        receipt = FOLDER / case.packet / f"{name}.jsonl.gz"
        rows = [json.loads(line) for line in gzip.decompress(receipt.read_bytes()).splitlines()]
        directions = [row for row in rows if "r" in row]
        assert sorted(int(row["r"]) for row in directions) == list(range(total)), name
        assert all(row["verdict"] == "verified" for row in directions), name
        summary = rows[-1]
        assert summary["kind"] == "sqverify-fast-summary/v1", name
        assert summary["status"] == "VERIFIED", name


def test_every_entry_the_verifier_decides_has_a_verified_case_and_a_refused_control() -> None:
    for evidence_id, name in cited().items():
        assert entries()[name]["status"] == "VERIFIED", evidence_id
        assert name in controls(), f"{evidence_id}: no control receipt for {name}"
        assert controls()[name]["status"] == "CONTROLS_REFUSED", evidence_id


def net_problems(
    raw: dict[str, Any], premises: dict[str, Any], source: census.ReviewedSource | None
) -> list[str]:
    """Where a census row's net is outside what its crate source's review accepted.

    Without a declaration, the standard net and core of the 5 October route review
    (Carrying the Route): 201 half-angles of step 83/40000 at core side 9977/10000. A
    format M file that declares its own net (`proof_net`) needs a source whose review
    read the declared-net path, and the checklist (b) of the 6 October soundness review:
    the declaration exactly `step` and `last` (with `count = last + 1` if given), metadata
    that only restates it, the premises the net the file declares, and lemma N0's (a) to
    (e) recomputed here in exact rationals, apart from the crate.
    """
    problems = ["a format L net block in a format M file"] if "net" in raw else []
    net = raw.get("proof_net")
    if net is None:
        if (premises["angle_count"], premises["D"], premises["B"]) != (
            201,
            "83/40000",
            "9977/10000",
        ):
            problems.append("not the standard net and core")
        return problems
    if source is None or not source.declared_nets:
        problems.append("a declared net, built from a source no declared-net review read")
    if (
        not isinstance(net, dict)
        or not {"step", "last"} <= set(net) <= {"step", "last", "count"}
        or type(net["last"]) is not int
        or ("count" in net and net["count"] != net["last"] + 1)
    ):
        return [*problems, "proof_net is not exactly step and an integer last"]
    step, count, core = Fraction(str(net["step"])), int(net["last"]) + 1, Fraction(raw["B"])
    top = step * (count - 1)
    metadata = raw.get("certificate") or {}
    holds = {
        "net_origin proof_net": premises.get("net_origin") == "proof_net",
        "D is the declared step": Fraction(str(premises["D"])) == step,
        "angle_count is last + 1": premises["angle_count"] == count,
        "net_last_tangent": Fraction(str(premises.get("net_last_tangent", -1))) == top,
        "B is the file's": Fraction(str(premises["B"])) == core,
        "shrink_bound is B (1 + D)": (
            Fraction(str(premises.get("shrink_bound", 2))) == core * (1 + step)
        ),
        "metadata only restates the net": (
            Fraction(str(metadata.get("D", step))) == step
            and metadata.get("angle_count", count) == count
        ),
        "(a) D > 0 and 2 <= N <= 2^16": step > 0 and 2 <= count <= MAX_ANGLE_COUNT,
        "(b) B (1 + D) < 1": core * (1 + step) < 1,
        "(c) the last tangent past tan(pi/8)": top * top + 2 * top - 1 > 0,
        "(d) the last tangent at most 1/2": top <= Fraction(1, 2),
        "(e) B (1 + D / (1 - D^2/4)) < 1": core * (1 + step / (1 - step * step / 4)) < 1,
    }
    return [*problems, *(name for name, ok in holds.items() if not ok)]


def test_every_entry_the_verifier_decides_is_within_what_its_review_accepted() -> None:
    """The per-certificate conditions of the review of 5 October (Carrying the Route),
    and for a declared net those of the soundness review of 6 October (`net_problems`).

    A certificate outside them (points or segments, another core side, net, domain or
    threshold, a declared net outside lemma N0 or on a source whose review did not read
    it, a scaling factor, densities near lemma F3's caps, a fault injected, or a crate
    source no review accepted) needs another review before an evidence entry may rest on
    its census row.
    """
    for evidence_id, name in cited().items():
        raw = read_raw(cases()[name].candidate)
        assert raw["points"] == [], evidence_id
        assert raw.get("scaling_factor", "1") == "1", evidence_id
        densest = max(
            Fraction(row["mass"])
            / ((Fraction(x2) - Fraction(x1)) * (Fraction(y2) - Fraction(y1)))
            for row in raw["rectangles"]
            for x1, y1, x2, y2 in [row["rectangle"]]
        )
        assert 8 * densest <= DENSITY_CEILING, evidence_id
        entry = entries()[name]
        premises = entry["premises"]
        n = int(premises["n"])
        assert (n, premises["L"]) == (entry["n"], entry["L"]), evidence_id
        assert premises["format"] == "M", evidence_id
        assert premises["centre_domain"] == "per-bin", evidence_id
        source = census.REVIEWED_SOURCES.get(entry["build"]["source_sha256"])
        assert net_problems(raw, premises, source) == [], evidence_id
        assert Fraction(premises["mass_exact"]) == n - Fraction(1, 100000), evidence_id
        assert premises["expanded_points"] == premises["expanded_segments"] == 0, evidence_id
        assert entry["threshold"] == "1", evidence_id
        assert entry["refused_directions"] == [], evidence_id
        assert entry["build"]["source_sha256"] in REVIEWED_SOURCES, evidence_id
        assert (entry["build"]["profile"], entry["build"]["rustc"].split()[1]) == (
            "release",
            "1.98.0",
        ), evidence_id
        receipt = FOLDER / entry["packet"] / f"{name}.jsonl.gz"
        summary = json.loads(gzip.decompress(receipt.read_bytes()).splitlines()[-1])
        assert summary["fault_injected_at_box"] is None, evidence_id


def test_every_entry_the_verifier_decides_rests_on_a_review_of_its_certificate() -> None:
    """The route carries only to a certificate whose mathematics a review read.

    Each replay entry names, as its `audit_record`, the review that read its
    certificate, and every result citing the entry lists that review, accepting and
    covering the result: the 5 October review of the route for T-094's two, and for
    T-097's mixed_n66_L843 the review of the same day that read it before its replay.
    """
    for evidence_id in cited():
        record = decided()[evidence_id]["proof"]["audit_record"]
        results = citing().get(evidence_id) or []
        assert results, f"{evidence_id}: no result cites it"
        for result in results:
            reviews = [
                review for review in result.get("reviews") or [] if review["path"] == record
            ]
            assert reviews, f"{evidence_id}: {result['id']} does not list {record}"
            for review in reviews:
                assert review["verdict"] == "accepted", evidence_id
                assert result["id"] in (review.get("covers") or [result["id"]]), evidence_id


@pytest.mark.parametrize("name", sorted(controls()))
def test_each_control_refuses_both_mutants_where_the_original_verifies(name: str) -> None:
    receipt = controls()[name]
    entry = entries()[name]
    case = cases()[name]
    assert receipt["kind"] == "sqverify-fast-control/v1"
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["packet"], receipt["n"], receipt["L"]) == (case.packet, case.n, case.side)
    assert receipt["candidate_sha256"] == sha256(case.candidate) == entry["candidate_sha256"]
    least = entry["least_bound_leaf_exact"]
    assert receipt["index"] == least["r"]
    assert receipt["centre"] == least["centre"]
    exact = Fraction(receipt["exact_capture_independent"])
    assert receipt["captures_agree"] is True
    assert (
        exact == Fraction(receipt["exact_capture_crate"]) == Fraction(least["exact_coverage"])
    )
    runs = {run["name"]: run for run in receipt["runs"]}
    assert set(runs) == {"original", "scaled-99-100", "near-threshold"}
    original = runs["original"]
    assert (original["returncode"], original["verdict"]) == (0, "verified")
    for mutant in ("scaled-99-100", "near-threshold"):
        run = runs[mutant]
        mutation = run["mutation"]
        factor = Fraction(mutation["factor"])
        assert Fraction(mutation["capture_at_centre"]) == exact * factor, mutant
        witness = mutation["capture_at_witness"]
        # The mutant's capture is below the threshold at the least-bound leaf's centre or
        # at the refusal's witness, so the claim the mutant makes is false there and a
        # refusal is the only correct answer.
        assert exact * factor < 1 or (witness is not None and Fraction(witness) < 1), mutant
        assert run["returncode"] == 1, mutant
        assert run["verdict"] not in (None, "verified"), mutant
    assert Fraction(runs["scaled-99-100"]["mutation"]["factor"]) == census.CONTROL_SCALE
    near = runs["near-threshold"]["mutation"]
    assert exact * Fraction(near["factor"]) <= 1 - census.NEAR_THRESHOLD


def test_one_control_capture_is_recomputed_from_the_candidate() -> None:
    """The centre's capture, and the 99/100 mutant's at its witness, from the candidate."""
    receipt = controls()[RECOMPUTED]
    raw = read_raw(cases()[RECOMPUTED].candidate)
    index = int(receipt["index"])
    x, y = (Fraction(value) for value in receipt["centre"])
    assert mixed_exact(raw, x, y, index) == Fraction(receipt["exact_capture_independent"])
    (scaled,) = (run for run in receipt["runs"] if run["name"] == "scaled-99-100")
    px, py = (Fraction(value) for value in scaled["witness"]["exact_pose"])
    capture = census.CONTROL_SCALE * mixed_exact(raw, px, py, index)
    assert capture == Fraction(scaled["mutation"]["capture_at_witness"]) < 1


def test_each_reviewed_source_names_the_review_that_accepted_it() -> None:
    """The gate's digests are the driver's, each with a retained review, and only a review
    that read the declared-net path admits a row on a declared net."""
    assert set(census.REVIEWED_SOURCES) == REVIEWED_SOURCES
    for digest, source in census.REVIEWED_SOURCES.items():
        assert len(digest) == 64, digest
        assert (census.PROJECT.parent / source.review).is_file(), digest
    # The only source whose review read the declared-net path is main's at 910b6b12c.
    assert {
        digest for digest, source in census.REVIEWED_SOURCES.items() if source.declared_nets
    } <= {"d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"}


def test_an_evidence_entry_names_the_reviewed_build_its_row_was_made_from() -> None:
    entry = entries()[RECOMPUTED]
    text = census.evidence_entry(
        cases()[RECOMPUTED], FOLDER, entry, audit_record=census.ROUTE_REVIEW, date="2026-10-05"
    )
    (record,) = safe_load(text)
    source = census.REVIEWED_SOURCES[entry["build"]["source_sha256"]]
    built = entry["build"]["source_sha256"][:8]
    assert f"these receipts' build is {built}..., the source at {source.commit}" in " ".join(
        record["replay"].split()
    )
    assert "at all 201 directions of the standard net" in " ".join(record["replay"].split())
    assert source.statement in " ".join(record["limitations"].split())


def test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source() -> None:
    """mixed_n18_L470's row was built at f007d7afd, a source no review accepted."""
    name = DECLARED
    assert entries()[name]["build"]["source_sha256"] not in REVIEWED_SOURCES
    with pytest.raises(SystemExit, match="no review accepted"):
        census.evidence_entry(
            cases()[name], FOLDER, entries()[name], audit_record="x", date="2026-10-05"
        )


#: A stand-in digest for the declared-net row's build in the two tests below.
STAND_IN = "0" * 64


@pytest.mark.parametrize("scope", ["declared nets", "standard net only"])
def test_an_evidence_entry_on_a_declared_net_states_the_net_and_its_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, scope: str
) -> None:
    """The declared-net row as if built from a reviewed source, with a stand-in control:
    stated with its own net if that source's review read the declared-net path, and
    refused if it did not."""
    declared_nets = scope == "declared nets"
    source = census.ReviewedSource("910b6b12c", census.DECLARED_NET_REVIEW, "-", declared_nets)
    monkeypatch.setitem(census.REVIEWED_SOURCES, STAND_IN, source)
    name = DECLARED
    case = cases()[name]
    packet = tmp_path / case.packet
    packet.mkdir()
    receipt = FOLDER / case.packet / f"{name}.jsonl.gz"
    (packet / receipt.name).write_bytes(receipt.read_bytes())
    refused = {"verdict": "counterexample-candidate", "mutation": {"capture_at_centre": "0"}}
    control = {
        "status": "CONTROLS_REFUSED",
        "index": 408,
        "runs": [
            {"name": "original", "verdict": "verified"},
            {"name": "scaled-99-100", **refused},
            {"name": "near-threshold", **refused},
        ],
    }
    (packet / f"{name}.control.json").write_text(json.dumps(control), encoding="utf-8")
    entry = entries()[name]
    reviewed = {**entry, "build": {**entry["build"], "source_sha256": STAND_IN}}
    if not declared_nets:
        with pytest.raises(SystemExit, match="no review of the declared net accepted"):
            census.evidence_entry(case, tmp_path, reviewed, audit_record="x", date="2026-10-06")
        return
    text = census.evidence_entry(case, tmp_path, reviewed, audit_record="x", date="2026-10-06")
    (record,) = safe_load(text)
    replay = " ".join(record["replay"].split())
    limitations = " ".join(record["limitations"].split())
    assert "at all 416 directions of the net it declares" in replay
    assert "the source at 910b6b12c" in replay
    assert "at all 416 net directions" in limitations
    assert "of 416 half-angles of step 1/1001, with B(1 + D) = 500499/500500 < 1" in limitations
    assert "the other 415 by interval branch and bound" in limitations
    assert census.DECLARED_NET_REVIEW in " ".join(record["proof"]["pinpoints"].split())
    assert "the net its candidate declares (proof_net)" in record["proof"]["assumptions"][1]


def test_the_net_conditions_admit_the_declared_net_only_on_a_source_that_read_it() -> None:
    """`net_problems` on the retained declared-net row, as if its build were of a source
    whose review read the declared-net path, and of one whose review did not."""
    raw = read_raw(cases()[DECLARED].candidate)
    premises = entries()[DECLARED]["premises"]
    read_it = census.ReviewedSource("-", "-", "-", declared_nets=True)
    standard_only = census.ReviewedSource("-", "-", "-", declared_nets=False)
    assert net_problems(raw, premises, read_it) == []
    assert net_problems(raw, premises, standard_only) == [
        "a declared net, built from a source no declared-net review read"
    ]
    net = raw["proof_net"]
    assert net_problems({**raw, "proof_net": {**net, "step": "1/999"}}, premises, read_it) == [
        "D is the declared step",
        "net_last_tangent",
        "shrink_bound is B (1 + D)",
        "(b) B (1 + D) < 1",
        "(e) B (1 + D / (1 - D^2/4)) < 1",
    ]
    assert "(c) the last tangent past tan(pi/8)" in net_problems(
        {**raw, "proof_net": {**net, "last": 414}}, premises, read_it
    )
    assert net_problems({**raw, "proof_net": {**net, "last": "415"}}, premises, read_it) == [
        "proof_net is not exactly step and an integer last"
    ]
    assert net_problems({**raw, "net": {}}, premises, read_it) == [
        "a format L net block in a format M file"
    ]
    assert net_problems(raw, {**premises, "D": "83/40000"}, read_it) == [
        "D is the declared step",
    ]


def test_the_exact_evaluator_reads_a_declared_net() -> None:
    """Finding DR-1 of the 6 October review: on mixed_n18_L470's net (step 1/1001) the
    control's evaluator gives the crate's exact capture at the least-bound leaf's centre,
    where the standard step scored another angle (1.2947 against 1.0703)."""
    raw = read_raw(cases()[DECLARED].candidate)
    entry = entries()[DECLARED]
    least = entry["least_bound_leaf_exact"]
    x, y = (Fraction(value) for value in least["centre"])
    assert net_step(raw) == Fraction(1, 1001) == Fraction(entry["premises"]["D"])
    assert mixed_exact(raw, x, y, int(least["r"])) == Fraction(least["exact_coverage"])


def test_a_control_refuses_a_row_decided_on_another_net() -> None:
    """The census control evaluates on the file's net and refuses a row whose net differs."""
    entry = entries()[DECLARED]
    other = {**entry, "premises": {**entry["premises"], "D": "83/40000"}}
    with pytest.raises(SystemExit, match="not the file's"):
        census.control(Path("/nonexistent"), cases()[DECLARED], other)
