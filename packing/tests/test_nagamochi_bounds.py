#!/usr/bin/env python3
"""The register's most load-bearing citation is checked as arithmetic, not just as a link.

`E-nagamochi-lower` carries the verified lower bound for most of the hundred cases: 88
until 2026-08-31, when the first-party green17 certificate took over `n = 17` and
`n = 18`; 85 when the adopted 4.5058 bound took `n = 19` on 2026-09-03; 83 on
2026-09-04, when `T-020` took `n = 20` and `n = 21`. The next most-cited evidence
record carries two. `assurance.py` checks that such a bound cites verified evidence of
the right claim and scope, which is a statement about the citation. A transcription slip
in any one of the values would have passed every existing check.

Nothing below pins that count. Three tests here did, and each went stale the day a
result moved a case off the closed form -- one of them a poisoned-control test whose
target `n = 20` acquired, as a real result, the very value it was poisoning with, so the
control passed without biting for the second time in its life (`D-444`). What a test can
hold without going stale is the relation: a case cites the theorem only where its value
is the theorem's, and no case a retained certificate reaches still cites it.

Since 2026-10-02 no verified lower bound cites the record at all: Nagamochi's Lemma 1 was
found false (`T-085`), the record became `reported`, and its values moved to the reported
lane, where the same relation is held. The verified floors it carried are Karakuş's
(`E-karakus-strip-lower`) or the area bound, and the checker re-derives Karakuş's too.

"Is the theorem's value" means rounded down, since 2026-10-04: a floor rounded up above
what its source proves passed the two-sided tolerance that held until then, so the
rounded-up `n = 150` floor below is the control that the one-sided check bites.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

import devtools.check_nagamochi_bounds as nagamochi
from devtools.check_nagamochi_bounds import (
    RECORD,
    cases,
    disagreement,
    karakus_form,
    main,
    prose_counts,
    theorem_two,
    theorem_two_form,
)
from sqpack.fractional.certificate import least_size_certified
from sqpack.known_best import KNOWN_BEST_CORPUS

CASES_DIR = Path(__file__).parents[1] / "cases"


#: The verified floor that replaced the record's on 2026-10-02.
KARAKUS = nagamochi.KARAKUS


def citing(record: str = RECORD, lane: str = "verified_lower_bound") -> dict[int, dict]:
    return {
        n: case
        for n, case in cases().items()
        if record in ((case.get(lane) or {}).get("evidence") or [])
    }


def test_the_recorded_bounds_re_derive() -> None:
    assert main() == 0


def reached_by_retained_certificates() -> set[int]:
    """Every case a retained fractional certificate moves off the closed form.

    Read from the case packages, not from a list: a certificate of side `L` and
    total mass `M` certifies every `n` above `M`, and displaces Theorem 2 at each
    such `n` where the theorem's value is below `L`. The packages are the record.
    """
    reached: set[int] = set()
    for path in sorted(CASES_DIR.glob("n*_fractional_certificate/certificate.json")):
        record = json.loads(path.read_text())
        side = Fraction(record["outer_side"])
        mass = sum((Fraction(w) for _, _, w in record["atoms"]), Fraction(0))
        for n in range(least_size_certified(mass), 101):
            if theorem_two(n)[0] < Decimal(side.numerator) / Decimal(side.denominator):
                reached.add(n)
    return reached


def test_it_covers_the_cases_it_claims_to() -> None:
    """Every citing case sits in the theorem's scope, and none a certificate reaches cites it.

    The count is not pinned. It was 85 when this test was written and 83 by the
    evening of 2026-09-04; each time it moved, the literal here outlived the
    record it described (`D-444`). What holds is the relation.
    """
    # No verified lower bound has cited the record since 2026-10-02 (T-085); its values
    # sit in the reported lane, which is held to the same relation.
    assert not citing()
    covered = citing(lane="reported_lower_bound")
    assert covered
    assert min(covered) >= 4
    assert max(covered) <= KNOWN_BEST_CORPUS.last_n
    reached = reached_by_retained_certificates()
    # The retained packages today: n = 11, 12, 17 and 20, reaching 11, 12, 17-21.
    assert {11, 12, 17, 18, 19, 20, 21} <= reached
    assert not (reached & set(covered)), sorted(reached & set(covered))
    # Everything still citing the theorem carries the theorem's own value rounded down;
    # `main` re-derives each one, and this is the same statement from the other side.
    for n, case in covered.items():
        value = Decimal(str(case["reported_lower_bound"]["value"]))
        exponent = value.as_tuple().exponent
        places = max(0, -exponent) if isinstance(exponent, int) else 0
        exact = theorem_two_form(n)[0]
        assert not exact.below(Fraction(value)), n
        assert exact.below(Fraction(value) + Fraction(1, 10**places)), n


@pytest.mark.parametrize("n", [4, 7, 8, 9, 14, 15, 16, 99, 100])
def test_the_exact_cases_give_an_integer(n: int) -> None:
    """`N` in `{m^2, m^2-1, m^2-2}` is Theorem 2's own special case and gives `s(N) >= m`."""
    value, exact = theorem_two(n)
    assert exact, n
    assert value == value.to_integral_value(), n
    assert value == math.isqrt(n - 1) + 1


@pytest.mark.parametrize("n", [17, 29, 50, 77])
def test_the_general_cases_give_the_root_form(n: int) -> None:
    """Otherwise `s(N) >= sqrt(N - 2k + 1) + 1` with `k = floor(sqrt(N))`."""
    value, exact = theorem_two(n)
    assert not exact, n
    root = math.isqrt(n)
    # Pin the precision: `theorem_two` works at 80 digits and the ambient context is 28,
    # so recomputing the root outside a pinned block compares two different numbers.
    with localcontext() as context:
        context.prec = 80
        assert abs(value - (Decimal(n - 2 * root + 1).sqrt() + 1)) < Decimal("1e-70")


def test_no_recorded_lower_bound_exceeds_its_upper() -> None:
    """The inversion would be a soundness defect, not a bookkeeping one."""
    for record, lane in (
        (RECORD, "reported_lower_bound"),
        (KARAKUS, "verified_lower_bound"),
    ):
        for n, case in citing(record, lane).items():
            lower = Decimal(str(case[lane]["value"]))
            upper = (case.get("reported_upper_bound") or {}).get("value")
            if upper is not None:
                assert lower <= Decimal(str(upper)), n


def test_a_wrong_value_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """The guard has to bite; a checker that only ever passes is decoration."""
    real = nagamochi.cases

    def poisoned() -> dict[int, dict]:
        found = real()
        # Poison a case this record still carries -- chosen from the record, because
        # a fixed target goes blind. `n = 19` was the target until `T-016` took it
        # over on 2026-09-03; `n = 20` replaced it and was taken over by `T-020` on
        # 2026-09-04 with the very value this control poisoned it with, `4.8`, so
        # the poison became the truth and the control passed without biting (D-444).
        # The target is the largest citing case with at least 0.3 of room under its
        # reported upper bound, so the poison neither reads as an inversion nor
        # lands inside the checker's one-unit-in-the-last-place tolerance.
        # Since 2026-10-02 the verified floor the record carried is Karakuş's, so that is
        # what is poisoned.
        target = max(
            n
            for n, case in found.items()
            if KARAKUS in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
            and (case.get("reported_upper_bound") or {}).get("value") is not None
            and Decimal(str(case["reported_upper_bound"]["value"]))
            - Decimal(str(case["verified_lower_bound"]["value"]))
            >= Decimal("0.3")
        )
        value = Decimal(str(found[target]["verified_lower_bound"]["value"]))
        found[target]["verified_lower_bound"]["value"] = str(
            (value + Decimal("0.2")).quantize(Decimal("0.1"))
        )
        return found

    monkeypatch.setattr(nagamochi, "cases", poisoned)
    assert nagamochi.main() == 1


#: Karakuş's (6.1) at `n = 150` is 12.25797601630484..., recorded to ten places as
#: 12.2579760163. Rounded up in its last place, 12.2579760164 is within the two-sided
#: tolerance that held until 2026-10-04 and passed every gate but the generator's drift
#: check, though it claims more than the source proves.
N150_FLOOR = "12.2579760163"
N150_ROUNDED_UP = "12.2579760164"


def test_a_floor_rounded_up_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """The review's mutation: n = 150's verified floor rounded up in its last place."""
    real = nagamochi.cases

    def rounded_up() -> dict[int, dict]:
        found = real()
        lower = found[150]["verified_lower_bound"]
        # The control has to be about the record it names; if `n = 150` ever leaves
        # Karakuş's lane, this says so instead of passing on another case.
        assert lower["evidence"] == [KARAKUS]
        assert lower["value"] == N150_FLOOR
        lower["value"] = N150_ROUNDED_UP
        return found

    monkeypatch.setattr(nagamochi, "cases", rounded_up)
    assert nagamochi.main() == 1


@pytest.mark.parametrize(
    ("n", "form", "recorded", "refused"),
    [
        (150, "karakus", N150_FLOOR, None),
        (150, "karakus", "12.257976016", None),
        (150, "karakus", N150_ROUNDED_UP, "never up"),
        (150, "karakus", "12.2579760162", "rounded down at the record's places"),
        # Theorem 2 at n = 106 is 10.32737905308881...: the reported value the generator
        # wrote, rounded to nearest, until 2026-10-04, and the floor it writes now.
        (106, "nagamochi", "10.32737905309", "never up"),
        (106, "nagamochi", "10.32737905308", None),
        # An exact case is the integer itself, and nothing a unit below it.
        (99, "nagamochi", "10", None),
        (99, "nagamochi", "9.9", "rounded down at the record's places"),
        (99, "karakus", "10", None),
        (99, "karakus", "10.0000000001", "never up"),
    ],
)
def test_a_record_is_its_theorem_rounded_down(
    n: int, form: str, recorded: str, refused: str | None
) -> None:
    exact = (karakus_form if form == "karakus" else theorem_two_form)(n)[0]
    problem = disagreement(n, Decimal(recorded), exact, name=form)
    if refused is None:
        assert problem is None, problem
    else:
        assert problem is not None
        assert refused in problem, problem


def test_the_comparison_is_exact_not_rounded() -> None:
    """Values within 1e-90 of the root are told apart, past any decimal context here."""
    exact = karakus_form(150)[0]
    assert exact.radicand == Fraction(4 * (150 - 12) + 1, 4)
    root = math.isqrt(int(exact.radicand * 4 * 10**180))
    # `root / (2 * 10^90)` is sqrt(radicand) rounded down at 90 places; one unit above it
    # is strictly above the true root.
    just_above = exact.rational + Fraction(root + 1, 2 * 10**90)
    just_below = exact.rational + Fraction(root, 2 * 10**90)
    assert exact.below(just_above)
    assert not exact.below(just_below)


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ((1, 4), (3, 0)),
        ((1, 4), (0, 9)),
        ((Fraction(1, 2), 1), (0, Fraction(9, 4))),
        ((0, 2), (0, 2)),
        ((0, 0), (0, 0)),
    ],
)
def test_compare_finds_equal_values_equal(
    left: tuple[Fraction | int, Fraction | int], right: tuple[Fraction | int, Fraction | int]
) -> None:
    one = nagamochi.RootForm(Fraction(left[0]), Fraction(left[1]))
    other = nagamochi.RootForm(Fraction(right[0]), Fraction(right[1]))
    assert one.compare(other) == 0
    assert other.compare(one) == 0


def test_compare_agrees_with_high_precision_decimals() -> None:
    """Every branch of the sign rule, against 100-digit decimals on a grid of forms."""
    values = [Fraction(numerator, 4) for numerator in range(0, 41, 3)]
    forms = [nagamochi.RootForm(a - 3, r) for a in values for r in values]
    with localcontext() as context:
        context.prec = 100
        decimals = {
            form: Decimal(form.rational.numerator) / form.rational.denominator
            + (Decimal(form.radicand.numerator) / form.radicand.denominator).sqrt()
            for form in forms
        }
        for one in forms:
            for other in forms:
                difference = decimals[one] - decimals[other]
                if abs(difference) < Decimal("1e-80"):
                    # A tie, which only an exact rule can call; it must call it a tie.
                    assert one.compare(other) == 0, (one, other)
                else:
                    assert one.compare(other) == (1 if difference > 0 else -1), (one, other)


def test_a_negative_radicand_is_refused() -> None:
    with pytest.raises(ValueError, match="negative"):
        nagamochi.RootForm(Fraction(0), Fraction(-1))


def test_the_prose_counts_agree_with_the_records() -> None:
    """The README and the case bodies quote the corpus, not a memory of it (D-430)."""
    assert prose_counts(cases()) == []


def test_a_stale_readme_count_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pytest.TempPathFactory
) -> None:
    """The figure that outlived the 4.5058 adoption by a day would now fail the gate."""
    stale = tmp_path / "README.md"  # type: ignore[operator]
    found = cases()
    open_cases = [case for case in found.values() if case.get("status") == "open"]
    governed = sum(
        RECORD in ((case.get("verified_lower_bound") or {}).get("evidence") or [])
        for case in open_cases
    )
    # Five more than the record says, whatever the corpus says today.
    stale_count = governed + 5
    stale.write_text(
        f"Of the {len(open_cases)} open cases, **{stale_count}** have\nNagamochi\u2019s "
        "general closed form.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(nagamochi, "README", stale)
    problems = prose_counts(found)
    assert len(problems) == 1
    assert f"{stale_count} of {len(open_cases)}" in problems[0]
    # The corpus figure is read from the record here, as the checker reads it: it
    # was 60 when this test was written and 58 a day later (D-444).
    assert f"{governed} of {len(open_cases)}" in problems[0]
    assert governed < stale_count
