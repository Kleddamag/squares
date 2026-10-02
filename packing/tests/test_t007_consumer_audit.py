# ruff: noqa: RUF001 -- the record's typography (minus signs, superscripts) is matched as written.
"""The T-007 consumer audit: its exact arithmetic, the classes it assigns, and its record."""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_t007_consumers as audit
from devtools import check_nagamochi_bounds as nagamochi

REPO = Path(__file__).resolve().parents[2]


def rows() -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in audit.build_document()["rows"]}


def line_of(path: str, needle: str) -> int:
    """The line a needle is on, so a test survives edits elsewhere in the file."""
    lines = (REPO / path).read_text(encoding="utf-8").split("\n")
    return next(number for number, line in enumerate(lines, 1) if needle in line)


def test_the_retained_inventory_is_current() -> None:
    assert audit.OUTPUT.read_text(encoding="utf-8") == audit.render(audit.build_document())


def test_surd_arithmetic_is_exact() -> None:
    root2, root3 = audit.Surd.root(2), audit.Surd.root(3)
    assert audit.Surd.root(8) == audit.Surd.rational(2) * root2
    assert (root2 * root2).as_rational == 2
    assert audit.Surd.root(Fraction(1, 4)).as_rational == Fraction(1, 2)
    assert audit.Surd.rational(6) / root2 == audit.Surd.rational(3) * root2
    assert (root2 + audit.Surd.rational(Fraction(1, 10**50)) - root2).sign() == 1
    assert (root2 + root3 - audit.Surd.root(5)).sign() == 1
    assert (root2 + root3 - audit.Surd.root(10)).sign() == -1
    assert (root2 - root2).sign() == 0
    assert audit.Surd.root(150).floor() == 12
    assert root2.decimal() == "1.414213562373"
    assert audit.Surd.rational(Fraction(-1, 3)).decimal() == "-0.333333333334"
    with pytest.raises(ValueError, match="sum of radicals"):
        _ = audit.Surd.rational(1) / (audit.Surd.rational(1) + root2)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2 + (1/2)sqrt(2)", "2 + (1/2)*sqrt(2)"),
        ("sqrt(150 - 2*floor(sqrt(150)) + 1) + 1", "1 + sqrt(127)"),
        ("18*sqrt(5)/101 + 2*sqrt(2) + 709/101", "709/101 + 2*sqrt(2) + (18/101)*sqrt(5)"),
        ("94*sqrt(2)/41 + 247/41", "247/41 + (94/41)*sqrt(2)"),
        ("15680/3951", "15680/3951"),
        ("5.0", "5"),
    ],
)
def test_the_parser_reads_every_shape_the_register_uses(text: str, expected: str) -> None:
    assert audit.parse_exact(text).render() == expected


@pytest.mark.parametrize(
    "text",
    [
        "x+1",
        "sin(1)",
        "__import__('os')",
        "sqrt(sqrt(2))",
        "1/(1+sqrt(2))",
        "1/0",
        "True",
        "2**3",
    ],
)
def test_the_parser_refuses_what_its_arithmetic_cannot_hold(text: str) -> None:
    with pytest.raises(ValueError, match=r"expression|radical|division"):
        audit.parse_exact(text)


def test_display_slack_refuses_to_guess_a_close_comparison() -> None:
    def display(value: str, places: int) -> audit.Quantity:
        return audit.Quantity(
            audit.Surd.rational(Fraction(value)), "display", Fraction(1, 10**places)
        )

    assert audit.compare(display("3.877", 3), display("3.900", 3)) == -1
    with pytest.raises(ValueError, match="cannot separate"):
        audit.compare(display("3.877", 3), display("3.8775", 4))
    with pytest.raises(ValueError, match="cannot separate"):
        audit.compare(display("3.877", 3), display("3.9", 1))


def test_nagamochi_values_agree_with_the_gate_checker_at_every_case() -> None:
    for n in range(4, 325):
        value = audit.nagamochi_value(n)  # raises on any disagreement with theorem_two
        _, is_exact = nagamochi.theorem_two(n)
        assert (value.as_rational is not None) == is_exact
        assert audit.compare(
            audit.Quantity(value, "nagamochi"), audit.Quantity(audit.area_bound(n), "area")
        ) == (0 if math.isqrt(n) ** 2 == n else 1)


def test_karakus_bound_sits_between_area_and_nagamochi_touching_it_at_k2_minus_1() -> None:
    for n in range(1, 325):
        bound = audit.karakus_bound(n)
        if n < 8 or math.isqrt(n) ** 2 == n:
            assert bound is None
            continue
        assert bound is not None
        area = audit.Quantity(audit.area_bound(n), "area")
        karakus = audit.Quantity(bound, "karakus")
        target = audit.Quantity(audit.nagamochi_value(n), "nagamochi")
        assert audit.compare(karakus, area) == 1
        k2_minus_1 = math.isqrt(n + 1) ** 2 == n + 1
        assert audit.compare(karakus, target) == (0 if k2_minus_1 else -1)
        if k2_minus_1:
            assert bound.as_rational == math.isqrt(n + 1)


def classify(**overrides: Any) -> dict[str, Any]:
    def quantity(value: int | str) -> audit.Quantity:
        return audit.Quantity(audit.Surd.rational(Fraction(value)), "test")

    arguments: dict[str, Any] = {
        "cites_t007": True,
        "target": quantity(8),
        "area": quantity("7.8"),
        "registered": None,
        "shape": None,
        "karakus": None,
    }
    numeric = {"target", "area", "registered", "karakus"}
    arguments.update(
        {key: quantity(value) if key in numeric else value for key, value in overrides.items()}
    )
    return audit.classify(**arguments)


def test_classification_follows_its_declared_order() -> None:
    assert classify(cites_t007=False)["reason"] == "operative-bound-independent"
    assert classify(area=8)["reason"] == "area-bound"
    assert classify(registered=8)["reason"] == "registered-verified-bound"
    assert classify(registered=8, shape=("k^2-1", 9))["class"] == audit.UNAFFECTED
    assert classify(shape=("k^2-1", 9))["class"] == audit.REPROVED
    assert classify()["class"] == audit.ONLY
    assert classify(registered="7.5")["class"] == audit.ONLY
    weakened = classify(registered="7.9")
    assert weakened["class"] == audit.WEAKENED
    assert weakened["weakened_to"]["exact"] == "79/10"
    assert classify(registered="7.9", karakus="7.95")["reason"] == "karakus-6.1"
    assert classify(registered="7.95", karakus="7.9")["reason"] == "registered-verified-bound"
    with pytest.raises(ValueError, match="Nagamochi value"):
        audit.classify(
            cites_t007=True,
            target=None,
            area=audit.Quantity(audit.Surd.rational(1), "area"),
            registered=None,
            shape=None,
            karakus=None,
        )


def test_the_register_counts_match_the_frontier_readme() -> None:
    summary = audit.build_document()["summary"]
    operative = summary["operative_cites_t007"]
    assert (operative["all"], operative["open"], summary["open_cases"]) == (287, 238, 261)
    assert operative["outside_t007_registered_scope_n"] == "101-324"
    assert sum(summary["classes"].values()) == 324


def test_the_k2_minus_2_exact_values_from_k8_rest_on_t007_alone() -> None:
    summary = audit.build_document()["summary"]
    k2_minus_2 = [k * k - 2 for k in range(8, 19)]
    assert summary["exact_value_claims_on_t007_alone"] == k2_minus_2
    assert summary["exact_value_claims_on_t007_alone_without_karakus"] == sorted(
        [*k2_minus_2, *(k * k - 1 for k in range(8, 19))]
    )


def test_case_rows_carry_each_kind_of_support_separately() -> None:
    by_n = rows()
    n62 = by_n[62]
    assert (n62["exposure_class"], n62["exposure_reason"]) == (audit.WEAKENED, "karakus-6.1")
    assert n62["exposure_class_without_karakus"] == audit.ONLY
    assert n62["support"]["registered_reported"]["reaches_nagamochi"] is True
    assert [s["results"] for s in n62["support"]["registered_reported"]["sources"]] == [
        ["T-062"],
        ["T-063"],
    ]
    assert n62["support"]["chelokot_lean_reported"]["status"] == "reported-unchecked"
    assert by_n[63]["exposure_class"] == audit.REPROVED
    assert by_n[63]["support"]["karakus_k2_minus_1"]["value"] == 8
    assert by_n[16]["exposure_reason"] == "area-bound"
    assert by_n[12]["exposure_reason"] == "operative-bound-independent"
    assert by_n[73]["weakened_to_without_karakus"]["exact"] == "861/100"
    assert by_n[150]["operative_lower_bound"]["t007_scope_covers_n"] is False


def test_an_independent_route_through_a_nagamochi_lemma_says_so() -> None:
    sources = rows()[47]["support"]["registered_verified"]["sources"]
    assert [(source["n"], source["results"]) for source in sources] == [
        (45, ["T-053"]),
        (46, ["T-004", "T-008"]),
    ]
    assert "shares_a_nagamochi_lemma" not in sources[0]
    caveat = sources[1]["shares_a_nagamochi_lemma"]
    for key, needle in (("cited_at", "Nagamochi [7]"), ("nagamochi_lemma_at", "Lemma 7")):
        path, line = caveat[key].rsplit(":", 1)
        assert needle in (REPO / path).read_text(encoding="utf-8").split("\n")[int(line) - 1]


def test_case_prose_proofs_and_their_defects_are_carried() -> None:
    by_n = rows()
    n7 = by_n[7]["support"]["case_prose_published_proofs"]
    assert n7["defects"] == ["D-344–D-347"]
    assert n7["proofs"][0]["label"] == "El Moumni’s Theorem 1"
    assert by_n[150]["support"]["case_prose_published_proofs"] is None


def test_the_scan_sorts_lines_into_tiers() -> None:
    lines = (
        "Nagamochi proved s(k^2 - 2) = k.",
        "",
        "| T-044 | lower bound | wand125 after Stromquist, Nagamochi, Burns |",
        "| 92 | 10 | Nagamochi | 0.34 |",
        "",
        "The floor here is Nagamochi’s closed form.",
        "",
        "Karakuş showed the scoring lemma fails; s(n^2-2) = n is open.",
        "",
        "the loop stalls at the 1e-12 floor, and E-nagamochi-lower is an identifier",
        "since n^2-2n < (n-1)^2",
    )
    hits = {hit["line"]: hit for hit in audit.scan_text("\n".join(lines))}
    assert {line: hit["tier"] for line, hit in hits.items()} == {
        1: "states",
        3: "mentions",
        4: "relies",
        6: "relies",
        8: "states",
    }
    assert [line for line, hit in hits.items() if hit["qualified"]] == [8]


def test_the_inventory_finds_the_statements_a_correction_must_reach() -> None:
    files = {entry["path"]: entry for entry in audit.build_document()["documents"]["files"]}
    expected = (
        ("packing/frontier/RESULTS.md", "| T-007 |"),
        ("packing/frontier/evidence.yaml", "exact values for N in {m^2, m^2-1, m^2-2}"),
        ("packing/frontier/README.md", "have Nagamochi’s formula as their verified"),
        ("packing/devtools/generate_frontier_case.py", "Established by Nagamochi’s general"),
        ("packing/frontier/n-322.md", "Established by Nagamochi’s general theorem"),
        (
            "docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md",
            "Nagamochi’s $s(n^2 - 1) = s(n^2 - 2) = n$",
        ),
    )
    for path, needle in expected:
        assert line_of(path, needle) in files[path]["unqualified_states_lines"], path


def test_check_reports_a_stale_record(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "audit.json"
    monkeypatch.setattr(audit, "OUTPUT", target)
    assert audit.main(["--check"]) == 1
    assert audit.main(["--update"]) == 0
    assert audit.main(["--check"]) == 0
    target.write_text(target.read_text(encoding="utf-8") + " ", encoding="utf-8")
    assert audit.main(["--check"]) == 1
