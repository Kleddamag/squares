"""Synthetic algebra and refusal controls for the H-254 exact chart screen."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path

import pytest

from devtools.check_n17_contact_chart import (
    ANCHORS,
    CONTACTS,
    Pose,
    audit,
    canonical_axis,
    chart,
    directed_gap,
    distinct_axes,
    load_frozen_source,
    main,
    orientation,
    reconstruct,
    undirected_gap,
)


def synthetic(*, lambda6: Q = Q(3, 2)) -> tuple[tuple[Pose, ...], Q]:
    """Exact contact-table input, without any feasibility or root assertion."""
    side, t, b = Q(33, 7), Q(1, 3), Q(1, 5)
    centres = reconstruct(side, t, b, lambda6, Q(1))
    angles = (Q(0),) * 8 + (t,) * 6 + (Q(0), -b, Q(0))
    return tuple(
        Pose(*centre, angle) for centre, angle in zip(centres, angles, strict=True)
    ), side


def by_name(result: dict, name: str) -> dict:
    return next(check for check in result["checks"] if check["name"] == name)


def test_frozen_reconstruction_satisfies_defining_equalities() -> None:
    poses, side = synthetic()
    result = audit(poses, side)
    for label, wall in ANCHORS:
        assert by_name(result, f"anchor.{label}.{wall}")["value"] == "0"
    for left, right, axis, _ in CONTACTS:
        assert by_name(result, f"contact.{left}.{right}.{axis}.support")["value"] == "0"
        assert by_name(result, f"contact.{left}.{right}.{axis}.selected_axis")["passed"]
    for left, right, axis, _ in CONTACTS[:17]:
        assert by_name(result, f"contact.{left}.{right}.{axis}.gap")["value"] == "0"
    for key in ("F1", "F2", "F3"):
        assert by_name(result, f"identity.{key}")["value"] == "0"
    assert result["counts"]["anchors"] == 15
    assert result["counts"]["selected_contacts"] == 20
    assert result["counts"]["centres"] == 34
    assert result["counts"]["pairs"] == 136
    assert sum(".alternative." in check["name"] for check in result["checks"]) == 42
    assert all(
        by_name(result, f"centre.{label}.{axis}")["value"] == "0"
        for label in range(1, 18)
        for axis in ("x", "y")
    )


def test_square_11_tangential_contact_is_independently_checked() -> None:
    poses, side = synthetic()
    v = orientation(poses[10].t)[1]
    moved = list(poses)
    original = moved[10]
    moved[10] = Pose(original.x + v[0] / 100, original.y + v[1] / 100, original.t)
    result = audit(tuple(moved), side)
    assert by_name(result, "contact.9.11.w.gap")["passed"] is False
    assert by_name(result, "contact.3.11.u.gap")["value"] == "0"
    assert by_name(result, "centre.11.x")["passed"] is False


def test_axis_dedup_and_opposite_axis_gap() -> None:
    first = Pose(Q(1), Q(1), Q(0))
    second = Pose(Q(2), Q(1), Q(0))
    assert len(distinct_axes(first, second)) == 2
    assert canonical_axis((Q(-1), Q(0))) == (Q(1), Q(0))
    assert undirected_gap(first, second, (Q(1), Q(0))) == undirected_gap(
        first, second, (Q(-1), Q(0))
    )
    assert directed_gap(first, second, (Q(1), Q(0))) == 0


def test_alternative_axis_ambiguity_is_reported() -> None:
    poses, side = synthetic()
    changed = list(poses)
    second = changed[1]
    changed[1] = Pose(second.x, second.y + 1, second.t)
    result = audit(tuple(changed), side)
    assert by_name(result, "contact.1.2.ex.gap")["value"] == "0"
    assert by_name(result, "contact.1.2.ex.alternative.0.1")["passed"] is False


def test_displaced_contact_and_domain_sign_refusal() -> None:
    poses, side = synthetic()
    shifted = list(poses)
    original = shifted[1]
    shifted[1] = Pose(original.x + Q(1, 10**9), original.y, original.t)
    result = audit(tuple(shifted), side)
    assert by_name(result, "contact.1.2.ex.gap")["passed"] is False
    assert by_name(result, "contact.1.2.ex.gap")["value"] == "1/1000000000"
    assert by_name(audit(poses, side), "domain.S")["passed"] is False
    with pytest.raises(ValueError, match="denominator"):
        chart(side, Q(0), Q(1, 5))
    # A source outside the branch-sign regime is rejected, even if algebra is defined.
    bad = list(poses)
    bad[15] = bad[15]._replace(t=Q(2))
    assert by_name(audit(tuple(bad), side), "sign.alpha")["passed"] is False


def test_slider_overlap_is_detected_by_full_pair_check() -> None:
    poses, side = synthetic(lambda6=Q(1, 2))
    result = audit(poses, side)
    assert by_name(result, "separation.1.6")["passed"] is False
    assert by_name(result, "separation.1.6")["value"] == "-1"
    assert result["criterion_passed"] is False


def test_incomplete_roster_and_wrong_source_hash_refused(tmp_path: Path, capsys) -> None:
    poses, side = synthetic()
    with pytest.raises(ValueError, match="exactly 17"):
        audit(poses[:-1], side)
    wrong_source = tmp_path / "wrong-source.json"
    wrong_source.write_text('{"side":"4675530093604551/1000000000000000"}')
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        load_frozen_source(wrong_source)
    assert main(["--source", str(wrong_source)]) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["criterion_passed"] is False
    assert "SHA-256 mismatch" in output["refused"]
