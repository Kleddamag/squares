"""Green's DS7 Theorem 9 pattern: its identities, its empty squares, and its controls.

`devtools.check_green_ds7` reconstructs the ``k^2`` points behind DS7's
``s(k^2 + 1) >= G_k`` and decides, in exact arithmetic over ``Q(sqrt 2, sqrt k)``,
whether a given closed unit square fits in ``[0, G_k]^2`` and misses every point.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from devtools import check_green_ds7 as green
from devtools.check_green_ds7 import SQRT2, Square, Surd


def test_square_roots_normalise_and_multiply_exactly() -> None:
    assert Surd.sqrt(8) == 2 * SQRT2
    assert Surd.sqrt(36) == Surd.of(6)
    assert SQRT2 * Surd.sqrt(6) == 2 * Surd.sqrt(3)
    assert Surd.of(2) == SQRT2 * SQRT2
    assert (SQRT2 - SQRT2).terms == ()
    assert green.squarefree_split(72) == (6, 2)


def test_signs_are_decided_however_close_to_zero() -> None:
    # 239/169 and 577/408 are consecutive convergents of sqrt 2, on either side of it.
    assert (SQRT2 - Fraction(239, 169)).sign() == 1
    assert (Fraction(577, 408) - SQRT2).sign() == 1
    # sqrt 2 + sqrt 3 = 3.14626436994197234...
    assert (SQRT2 + Surd.sqrt(3) - Fraction(314626436994197234, 10**17)).sign() == 1
    assert (SQRT2 + Surd.sqrt(3) - Fraction(314626436994197235, 10**17)).sign() == -1
    assert (SQRT2 + Surd.sqrt(3) - Surd.sqrt(10)).sign() == -1
    assert Surd().sign() == 0


@pytest.mark.parametrize(
    ("k", "expected"),
    [
        (4, (40 * SQRT2 + 19) / 17),
        (5, 2 * SQRT2 + (27 + 2 * Surd.sqrt(10)) / 13),
        (9, (247 + 94 * SQRT2) / 41),
    ],
)
def test_green_bound_matches_the_specializations_ds7_prints(k: int, expected: Surd) -> None:
    assert green.green_bound(k) == expected


@pytest.mark.parametrize("k", range(2, 13))
def test_the_pattern_reproduces_g_k_exactly(k: int) -> None:
    p = green.pattern(k)
    assert all(green.identities(p).values()), green.identities(p)
    assert len(green.long_edges(p)) == (k - 1) * (k - 2)
    assert green.long_edge_exceeds_one(p) is (k >= 4)
    assert green.side_margin_exceeds_one(p) is (k == 2)


def test_k18_is_rational_in_t_and_u_and_has_slack_one_tenth() -> None:
    """The write-up's check case: ``t = 24/25``, ``u = 7/25``, ``d = 6/5``."""
    p = green.pattern(18)
    assert p.t == Surd.of(Fraction(24, 25))
    assert p.u == Surd.of(Fraction(7, 25))
    result = green.check_square(p, green.writeup_square(p))
    assert result.escapes
    assert Fraction(99999, 1000000) < result.slack_lower <= Fraction(1, 10)


@pytest.mark.parametrize("k", range(4, 13))
def test_the_writeup_square_is_empty_and_fits_for_every_k_from_four(k: int) -> None:
    p = green.pattern(k)
    result = green.check_square(p, green.writeup_square(p))
    assert result.fits
    assert result.empty
    d = float(2 - 2 * p.u) ** 0.5
    assert abs(float(result.slack_lower) - (d - 1) / 2) < 1e-9


def test_the_square_the_writeup_publishes_for_k4_is_empty_and_fits() -> None:
    p = green.pattern(4)
    result = green.check_square(p, green.published_square(p))
    assert result.escapes
    assert Fraction(5449, 1000000) < result.slack_lower < Fraction(5450, 1000000)


def test_k2_fails_at_the_wall_not_in_the_mesh() -> None:
    """``m_x = sqrt 2 - 2/5 > 1``: a whole unit strip along each side wall is empty."""
    p = green.pattern(2)
    result = green.check_square(p, green.strip_square(p))
    assert result.escapes
    assert result.slack_lower > Fraction(7, 1000)


def test_a_grown_square_past_its_slack_is_refused() -> None:
    """Negative control: the check must see a point that a larger square catches."""
    p = green.pattern(4)
    square = green.writeup_square(p)
    slack = green.check_square(p, square).slack_lower
    grown = square.grown(square.half + slack + Fraction(1, 10**6))
    result = green.check_square(p, grown)
    assert not result.empty
    assert len(result.covered_by) == 2


def test_a_square_outside_the_container_is_refused() -> None:
    p = green.pattern(4)
    corner = Square.from_tangent(Fraction(1, 2), Fraction(1, 2), Fraction(1, 10))
    result = green.check_square(p, corner)
    assert not result.fits
    assert not result.escapes


def test_lemma_three_holds_in_a_mesh_triangle_where_every_side_is_at_most_one() -> None:
    """Negative control at ``k = 3``: a square centred in a mesh triangle covers a vertex."""
    p = green.pattern(3)
    a, b, c = (p.points[i] for i in (0, 1, 3))
    x = ((a[0] + b[0] + c[0]) / 3).midpoint()
    y = ((a[1] + b[1] + c[1]) / 3).midpoint()
    for tau in (Fraction(0), Fraction(1, 7), Fraction(1, 3), Fraction(2, 5)):
        assert not green.check_square(p, Square.from_tangent(x, y, tau)).empty


def test_the_search_finds_an_empty_square_as_wide_as_q4() -> None:
    p = green.pattern(4)
    found = green.search_empty_square(p)
    assert abs(found.best - 0.0054494651) < 1e-7
    assert green.check_square(p, green.square_from_pose(*found.pose)).escapes


def test_the_search_finds_nothing_at_k3() -> None:
    assert green.search_empty_square(green.pattern(3)).best < 0


def test_figure_34_is_ds7s_own_gif_and_matches_the_k4_pattern() -> None:
    p = green.pattern(4)
    gif = green.figure_gif(green.FIGURE.read_text(encoding="utf-8"))
    match = green.match_figure(p, gif)
    assert match.gif_sha256 == green.DS7_L17_GIF_SHA256
    assert match.dots == 16
    assert match.row_zero == "top"
    assert match.max_residual < 1.5
    assert match.other_residual > 10


def test_the_scaled_k3_pattern_is_certified() -> None:
    three = green.certify_scaled(green.pattern(3), Fraction(1, 20))
    assert three.certified, three.detail


def test_the_k2_pattern_is_refused_a_thousandth_below_g2() -> None:
    """Its side margin is still above one there, so no branch-and-bound may close it."""
    assert not green.certify_scaled(green.pattern(2), Fraction(1, 1000)).certified


def test_ceiling_is_below_g4_and_comes_from_a_checked_square() -> None:
    record = green.check(4, search=False)
    assert record["verdict"] == "fails"
    assert record["ceiling_square"]["empty"]
    assert record["ceiling_square"]["fits"]
    assert Fraction(record["ceiling"]) < Fraction(4398, 1000)
    assert record["figure"]["is_ds7_l17_gif"]


def test_the_retained_receipt_holds_the_verdict_for_every_k_it_ran() -> None:
    """The packet's receipt is this tool's run for k = 2..17; spot-check it against a rerun."""
    receipt = green.PACKET / "receipts/check_green_ds7.json"
    records = json.loads(receipt.read_text(encoding="utf-8"))
    verdicts = {record["k"]: record["verdict"] for record in records}
    expected = {2: "fails", 3: "unavoidable-below-G_k"} | dict.fromkeys(range(4, 18), "fails")
    assert verdicts == expected
    for record in records:
        if record["k"] in (4, 9, 17):
            p = green.pattern(record["k"])
            result = green.check_square(p, green.writeup_square(p))
            assert str(result.slack_lower) == record["writeup_square"]["point_slack_at_least"]
