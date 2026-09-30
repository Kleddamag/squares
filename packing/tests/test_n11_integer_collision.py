"""Integer collision predicates preserve exact hulls, equality and tiny gaps."""

from __future__ import annotations

import random
import time
from fractions import Fraction as Q

import pytest

from devtools import check_n11_capture_transition_pilot as reference
from devtools import n11_integer_collision as integer


def test_homogeneous_hulls_match_rational_hulls() -> None:
    rng = random.Random(391)
    for _ in range(40):
        points = [
            (
                Q(rng.randrange(-50, 51), rng.randrange(1, 20)),
                Q(rng.randrange(-50, 51), rng.randrange(1, 20)),
            )
            for _ in range(15)
        ]
        encoded = [integer.encode(point) for point in points]
        encoded += [(3 * x, 3 * y, 3 * z) for x, y, z in encoded[:3]]
        actual = [(Q(x, z), Q(y, z)) for x, y, z in integer.hull(encoded)]
        assert actual == reference.pilot.hull(points)


@pytest.mark.parametrize(
    ("delta", "accepted"), [(Q(), True), (Q(-1, 10**50), True), (Q(1, 10**50), False)]
)
def test_closed_collision_boundary_and_tiny_escape(delta: Q, *, accepted: bool) -> None:
    core = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    domain = [(Q(-3), Q(-3)), (Q(3), Q(-3)), (Q(3), Q(3)), (Q(-3), Q(3))]
    partners = [([(Q(), Q())], core)]
    region = [(Q(2) + delta, Q())]
    for checker in (reference.universal_collision, integer.universal_collision):
        budget = reference.geometry.Budget(time.monotonic() + 10, 20000)
        if accepted:
            assert checker(core, domain, partners, region, budget=budget) == 4
        else:
            with pytest.raises(ValueError, match="universal collision"):
                checker(core, domain, partners, region, budget=budget)


def test_every_partner_pose_is_required() -> None:
    core = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    domain = [(Q(-10), Q(-10)), (Q(10), Q(-10)), (Q(10), Q(10)), (Q(-10), Q(10))]
    partners = [([(Q(), Q())], core), ([(Q(5), Q())], core)]
    for checker in (reference.universal_collision, integer.universal_collision):
        with pytest.raises(ValueError, match="universal collision"):
            checker(
                core,
                domain,
                partners,
                [(Q(), Q())],
                budget=reference.geometry.Budget(time.monotonic() + 10, 20000),
            )


def test_rational_oblique_facets_preserve_signed_center_and_tiny_boundary() -> None:
    def linear(x: Q, y: Q) -> tuple[Q, Q]:
        return x / 3 + 2 * y / 7, x / 11 + 3 * y / 5

    center = (Q(5, 13), Q(-7, 17))

    def translated(x: Q, y: Q) -> tuple[Q, Q]:
        a, b = linear(x, y)
        return a + center[0], b + center[1]

    corners = [(Q(-1), Q(-1)), (Q(1), Q(-1)), (Q(1), Q(1)), (Q(-1), Q(1))]
    core = [linear(x, y) for x, y in corners]
    domain = [translated(3 * x, 3 * y) for x, y in corners]
    for delta in (Q(-1, 10**60), Q(), Q(1, 10**60)):
        region = [translated(2 + delta, Q())]
        for checker in (reference.universal_collision, integer.universal_collision):
            budget = reference.geometry.Budget(time.monotonic() + 10, 20_000)
            if delta <= 0:
                assert checker(core, domain, [([center], core)], region, budget=budget) == 4
            else:
                with pytest.raises(ValueError, match="universal collision"):
                    checker(core, domain, [([center], core)], region, budget=budget)
