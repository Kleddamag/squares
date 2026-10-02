"""Exact first-order parts of the n17 local-minimum checker (H-261, BC-407)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

import pytest

from devtools import check_n17_local_minimum as local


@cache
def _target() -> local.Model:
    midpoint, _ = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    return local.build_model(*midpoint)


@cache
def _space() -> local.Quotient:
    return local.quotient(_target())


@cache
def _solved(name: str, sign: int) -> local.DirectionSolution:
    return local.solve_direction(_target(), _space(), name, sign)


def test_six_prescribed_zero_weights_and_52_positive_rows() -> None:
    audit = local.weight_audit(_target())
    assert audit["passed"]
    assert audit["zero_weight_rows"] == sorted(map(local.row_label, local.ZERO_WEIGHT_KEYS))
    assert audit["positive_weight_rows"] == 52
    # The midpoint is not the root: only the two prescribed F2 columns are off zero.
    omega12, omega16 = local.column(12, "angle"), local.column(16, "angle")
    assert set(audit["stress_residual_columns_at_point"]) == {str(omega12), str(omega16)}


def test_coordinates_annihilate_the_sliders_and_number_ninety_directions() -> None:
    model = _target()
    covectors = local.coordinates(model)
    assert len(covectors) == 45
    assert len(local.directions(model)) == 90
    assert model.u[0] ** 2 + model.u[1] ** 2 == 1
    for vector in local.slider_generators(model).values():
        for covector in covectors.values():
            assert sum((covector.get(i, Q(0)) * v for i, v in vector.items()), Q(0)) == 0


def test_kernel_is_exactly_the_slider_span_with_two_lineality_directions() -> None:
    audit = local.kernel_audit(_target())
    assert audit["passed"]
    assert (audit["rank_positive"], audit["kernel_dimension"], audit["rank_all"]) == (46, 6, 50)
    assert (audit["rank_positive_mod_p"], audit["rank_all_mod_p"]) == (46, 50)
    assert audit["lineality_generators"] == ["v13", "xi6"]
    zero_rows = audit["generator_values_on_zero_weight_rows"]
    assert zero_rows["xi5"] == {"wall:5:right:0": "-1", "wall:5:right:1": "-1"}
    assert zero_rows["v11"] == {"pair:9:11:0": "-1", "pair:9:11:1": "-1"}
    assert zero_rows["omega6"] == {"wall:6:bottom:0": "-1/2", "wall:6:bottom:1": "1/2"}


def test_rank_helpers_on_a_known_deficient_matrix() -> None:
    rows = [[Q(1), Q(2), Q(3)], [Q(2), Q(4), Q(6)], [Q(0), Q(1), Q(1, 2)]]
    assert local.exact_rank(rows) == 2
    assert local.modular_rank(rows) == 2


@pytest.mark.parametrize(
    ("name", "sign", "prefix"),
    [
        ("omega11", -1, "175.848328842"),
        ("omega16", -1, "74.1727814434"),
        ("eta16", 1, "12.0116678565"),
        ("xi17", 1, "1"),
        ("xi1", -1, "0"),
    ],
)
def test_selected_coordinate_duals_are_exact_optima(name: str, sign: int, prefix: str) -> None:
    solution = _solved(name, sign)
    assert solution.status == "certified_optimal"
    assert solution.a is not None
    assert local.decimal(solution.a).startswith(prefix)
    assert all(value > 0 for value in solution.lam.values())
    assert set(solution.lam) <= set(_target().positive_keys)
    assert local.verify_solution(_target(), _space(), solution)


def test_tampered_certificates_are_rejected() -> None:
    solution = _solved("omega11", -1)
    assert solution.a is not None
    key = next(iter(solution.lam))
    bumped = {**solution.lam, key: solution.lam[key] + Q(1, 10**9)}
    negated = {**solution.lam, key: -solution.lam[key]}
    for tampered in (
        replace(solution, lam=bumped),
        replace(solution, lam=negated),
        replace(solution, a=solution.a - Q(1, 10**9)),
        replace(solution, sign=1),
        replace(solution, status="undecided"),
    ):
        assert not local.verify_solution(_target(), _space(), tampered)


def test_unavailable_owner_alternatives_are_strictly_negative() -> None:
    audit = local.owner_alternative_audit(_target())
    assert audit["passed"]
    assert audit["unavailable"] == audit["strictly_negative"] == 135
    assert audit["identity_options"] == 33
    assert audit["identity_exact_zero"] == 31
    leading = [row["margin_decimal"][:7] for row in audit["least_negative"][:4]]
    assert leading == ["-0.0557", "-0.0557", "-0.0707", "-0.1474"]
    assert {tuple(row["pair"]) for row in audit["least_negative"][:2]} == {(7, 14), (14, 17)}


def test_kernel_row_control_is_refused() -> None:
    result = local.run_control(_target(), "kernel-row")
    assert result["refused"]
    assert "kernel.kernel_equals_slider_span" in result["failed_checks"]


def test_infeasible_dual_control_keeps_the_kernel_and_loses_the_dual() -> None:
    result = local.run_control(_target(), "infeasible-dual")
    assert result["refused"]
    assert all(result["kernel_checks"].values())
    assert result["direction"]["status"] == "no_nonnegative_dual"
    assert result["failed_checks"] == ["duals.-omega11"]


@pytest.mark.parametrize(
    ("control", "failed"), [("kernel-row", "kernel"), ("infeasible-dual", "duals")]
)
def test_cli_refuses_each_control(
    control: str,
    failed: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    seen: list[bytes] = []
    monkeypatch.setattr(local, "_check_frozen_root_bytes", seen.append)
    output = tmp_path / "receipt.json"
    assert local.main(["--control", control, "--output", str(output)]) == 1
    receipt = json.loads(output.read_text())
    raw = local.ROOT_CERTIFICATE.read_bytes()
    assert seen == [raw]
    assert receipt["passed"] is False
    assert receipt["checks"][failed] is False
    assert receipt["inputs"]["root_certificate_sha256"] == hashlib.sha256(raw).hexdigest()
    assert json.loads(capsys.readouterr().out)["passed"] is False


def test_cli_rejects_unbound_or_malformed_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def reject(_raw: bytes) -> None:
        raise ValueError("root certificate differs from frozen exp-237 Git blob")

    monkeypatch.setattr(local, "_check_frozen_root_bytes", reject)
    assert local.main([]) == 2
    assert "frozen" in json.loads(capsys.readouterr().out)["error"]
    malformed = tmp_path / "root.json"
    malformed.write_text("{}")
    monkeypatch.setattr(local, "_check_frozen_root_bytes", lambda _raw: None)
    assert local.main([str(malformed)]) == 2
    assert json.loads(capsys.readouterr().out)["passed"] is False


# The ratio test over the slider box (recipe C3, C4, C6, C7, C8, C9, C12).


@cache
def _family() -> local.Family:
    midpoint, _ = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    return local.build_family(*midpoint)


@cache
def _affine() -> tuple[local.AffineMatrix, dict[str, object]]:
    return local.affine_audit(_family(), local.DECLARED_BOX)


@cache
def _curvature() -> tuple[Q, ...]:
    radii = dict.fromkeys(_family().names, local.DECLARED_RADIUS)
    return local.curvature_audit(_family(), local.DECLARED_BOX, radii)[0]


@cache
def _outcome(name: str, sign: int) -> local.CoordinateOutcome:
    matrix, _ = _affine()
    family = _family()
    return local.certify_coordinate(
        matrix,
        local.float_system(matrix, 45),
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        names=family.names,
        name=name,
        sign=sign,
        box=local.DECLARED_BOX,
    )


def test_family_rows_at_the_origin_are_the_frozen_h258_rows_and_affine_in_the_sliders() -> None:
    matrix, audit = _affine()
    assert audit["passed"]
    assert audit["checks"] == {
        "identity_at_eleven_points": True,
        "support_as_stated": True,
        "rows_at_origin_equal_frozen_h258_rows": True,
        "rank_at_origin_45": True,
    }
    family = _family()
    omega5, omega7 = family.names.index("omega5"), family.names.index("omega7")
    rows = {key: index for index, key in enumerate(family.keys)}
    # Only the (5,7) moment arm k = (1 - a)/2 moves with a: d/da of tau/2 + k is -1.
    assert matrix.slopes[0][rows["pair", 5, 7, 0]] == {omega5: Q(-1)}
    assert matrix.slopes[0][rows["pair", 5, 7, 1]] == {omega7: Q(-1)}
    assert len(family.keys) == 52
    assert not set(family.keys) & local.ZERO_WEIGHT_KEYS


def test_perturbed_slope_control_is_refused() -> None:
    _, audit = local.affine_audit(_family(), local.DECLARED_BOX, perturb=True)
    assert not audit["passed"]
    assert not audit["checks"]["identity_at_eleven_points"]
    assert not audit["checks"]["support_as_stated"]


def test_sign_branches_hold_on_the_declared_box_and_a_flipped_branch_is_refused() -> None:
    audit = local.sign_branch_audit(_family(), local.DECLARED_BOX)
    assert audit["passed"]
    assert audit["faces"]["5/7"]["min_decimal"] == "-0.25"
    crossing = Q(audit["tau_13_14_zero_at_z"])
    assert Q(1, 16) < crossing < Q(81, 1000)
    assert audit["tau_13_14_slope_in_z"] == "-1"
    flipped = local.build_family(
        _family().t, _family().beta, branches={**local.FACE_BRANCHES, (5, 7): 1}
    )
    refused = local.sign_branch_audit(flipped, local.DECLARED_BOX)
    assert refused["failures"] == ["5/7"]
    wide = ((Q(0), Q(1, 4)), (Q(0), Q(1, 12)), (Q(-1, 8), Q(1, 10)))
    assert local.sign_branch_audit(_family(), wide)["failures"] == ["13/14"]


def test_curvature_constants_follow_the_n11_formula() -> None:
    radius = local.DECLARED_RADIUS
    curvature = _curvature()
    family = _family()
    walls = {curvature[i] for i, key in enumerate(family.keys) if key[0] == "wall"}
    assert walls == {local.INVERSE_ROOT2_UPPER * radius * radius}
    assert 2 * local.INVERSE_ROOT2_UPPER**2 > 1
    assert all(
        8 * radius**2 < value < 10 * radius**2 for value in curvature if value not in walls
    )
    assert local.pair_curvature(Q(2), Q(3), Q(5), Q(7), Q(1, 2)) == 50 + 30 + 72
    for value in (Q(0), Q(2), Q(1, 3), Q(10**6 + 1, 7)):
        upper = local.sqrt_upper(value)
        assert upper**2 >= value
        assert (
            upper - Q(1, local.SQRT_SCALE) < 0 or (upper - Q(1, local.SQRT_SCALE)) ** 2 < value
        )
    with pytest.raises(ValueError, match="nonnegative"):
        local.sqrt_upper(Q(-1))


def test_ratio_test_is_strict_and_agrees_with_the_n11_consumer() -> None:
    from devtools import check_n11_optimality_local_isolation as n11  # noqa: PLC0415

    assert local.ratio_test(Q(2), Q(1, 4), Q(2), Q(1)) == (True, Q(1, 3))
    assert local.ratio_test(Q(2), Q(1, 4), Q(2), Q(3)) == (False, Q(1))
    assert local.ratio_test(Q(1), Q(1), Q(1), Q(1)) == (False, None)
    for case in ((Q(2), Q(1, 4), Q(2), Q(1)), (Q(3, 7), Q(1, 9), Q(1, 2), Q(1, 5))):
        assert local.ratio_test(*case)[1] == n11.strict_dual_margin(*case)


def test_minus_omega11_passes_on_tiling_cells_with_its_worst_ratio_below_one() -> None:
    outcome = _outcome("omega11", -1)
    assert outcome.passed
    cells = [dual.cell for dual, _ in outcome.certificates]
    assert local.tiling_audit(cells, local.DECLARED_BOX)
    record = local.outcome_record(outcome)
    assert record["cells"] == len(cells) <= 16
    assert Q(9, 10) < Q(record["worst_ratio"]) < 1
    assert all(
        verdict["nonnegative"] and verdict["epsilon"] < Q(1, 10)
        for _, verdict in outcome.certificates
    )


def test_single_cell_directions_pass_with_small_ratios() -> None:
    for name, sign in (("u11", -1), ("xi1", 1), ("omega16", -1)):
        record = local.outcome_record(_outcome(name, sign))
        assert record["passed"]
        assert record["cells"] == 1
        assert Q(record["worst_ratio"]) < Q(1, 2)


def test_negative_vertex_dual_and_wider_radius_are_refused() -> None:
    outcome = _outcome("omega11", -1)
    matrix, _ = _affine()
    coordinate = _family().names.index("omega11")
    dual = outcome.certificates[0][0]
    negative = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=local.negative_vertex_control(dual),
    )
    assert negative["vertex_min"] == Q(-1, 10**6)
    assert not negative["nonnegative"]
    assert not negative["passed"]
    radii = dict.fromkeys(_family().names, 2 * local.DECLARED_RADIUS)
    wide, _ = local.curvature_audit(_family(), local.DECLARED_BOX, radii)
    verdicts = [
        local.evaluate_dual(
            matrix,
            wide,
            [2 * local.DECLARED_RADIUS] * 45,
            coordinate=coordinate,
            sign=-1,
            dual=item,
        )
        for item, _ in outcome.certificates
    ]
    assert not any(verdict["passed"] for verdict in verdicts)


def test_certificates_replay_from_json_and_tampering_is_refused() -> None:
    outcome = _outcome("omega11", -1)
    matrix, _ = _affine()
    documents = [
        {
            "direction": "-omega11",
            "cells": [local.dual_document(dual) for dual, _ in outcome.certificates],
        }
    ]
    stored = json.loads(json.dumps(documents))
    replay = local.replay_certificates(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        names=_family().names,
        documents=stored,
        box=local.DECLARED_BOX,
    )
    assert replay["failures"] == []
    assert not replay["complete"]
    assert replay["worst_ratio"] == local.outcome_record(outcome)["worst_ratio"]
    scaled = json.loads(json.dumps(stored))
    scaled[0]["cells"][0]["lambda"] = [2 * value for value in scaled[0]["cells"][0]["lambda"]]
    missing = json.loads(json.dumps(stored))
    missing[0]["cells"].pop()
    for tampered in (scaled, missing):
        result = local.replay_certificates(
            matrix,
            _curvature(),
            [local.DECLARED_RADIUS] * 45,
            names=_family().names,
            documents=tampered,
            box=local.DECLARED_BOX,
        )
        assert result["failures"] == ["-omega11"]


def test_tiling_audit_rejects_gaps_and_overlaps() -> None:
    whole = local.Cell((Q(0), Q(0), Q(-1, 8)), (Q(1, 4), Q(1, 12), Q(1, 16)))
    left, right = whole.split(1)
    assert local.tiling_audit([left, right], local.DECLARED_BOX)
    assert not local.tiling_audit([left], local.DECLARED_BOX)
    assert not local.tiling_audit([whole, left], local.DECLARED_BOX)


def test_unavailable_options_stay_negative_and_the_largest_corner_is_refused() -> None:
    family = _family()
    radii = dict.fromkeys(family.names, local.DECLARED_RADIUS)
    audit = local.unavailable_option_audit(family, local.DECLARED_BOX, radii)
    assert audit["passed"]
    assert audit["options"] == audit["strictly_negative"] == 125
    leading = audit["least_negative"][0]
    assert leading["base_gap_decimal"].startswith("-0.0557998")
    assert leading["worst_margin_decimal"].startswith("-0.05527")
    # The chosen corner gap at the origin is the point checker's support margin.
    point = {
        (tuple(row["pair"]), row["owner"], row["axis"], row["sign"]): row["margin_decimal"]
        for row in local.owner_alternative_audit(_target())["margins"]
    }
    for row in audit["least_negative"]:
        key = (tuple(row["pair"]), row["owner"], row["axis"], row["sign"])
        assert point[key] == row["base_gap_decimal"]
    control = local.unavailable_option_audit(
        family, local.DECLARED_BOX, radii, largest_corner=True
    )
    assert not control["passed"]


def test_cli_ratio_mode_without_the_n11_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local, "_check_frozen_root_bytes", lambda _raw: None)
    # C11 has its own test; a stub keeps this wiring test fast and shows it is load-bearing.
    monkeypatch.setattr(local, "stress_audit", lambda _family, _box: {"passed": False})
    output = tmp_path / "ratio.json"
    partial = ["--direction", "omega11:-1", "--direction", "u11:1"]
    command = ["--ratio", "--no-n11", "--midpoint-only", *partial, "--output", str(output)]
    assert local.main(command) == 1
    receipt = json.loads(output.read_text())
    assert receipt["schema"] == local.RATIO_SCHEMA
    assert receipt["inputs"]["core_stress_commit"] == "2fbf8d29"
    assert receipt["checks"]["c8_c9_every_direction"]
    assert receipt["checks"]["c12_controls"]
    # A partial run cannot pass: two of 90 directions, and no root-box items.
    assert not receipt["checks"]["c8_c9_replayed_from_certificates"]
    assert not receipt["checks"]["c8i_root_box"]
    assert not receipt["checks"]["c11_stress_on_the_box"]
    assert receipt["checks"]["c1_roster_binding"]
    assert json.loads(capsys.readouterr().out)["passed"] is False
    assert local.main(["--ratio", "--radius", "1/10"]) == 2
    assert "radius" in json.loads(capsys.readouterr().out)["error"]


def test_affine_structure_holds_at_symbolic_root_parameters() -> None:
    matrix, _ = _affine()
    audit = local.symbolic_affine_audit(_family(), matrix)
    assert audit["passed"]
    assert audit["entries"] == 52 * 45
    assert audit["offsets"] == {"1/2": True, "1/3": True, "5/7": True}


def test_root_box_deviation_is_tiny_and_folds_into_the_residual() -> None:
    matrix, _ = _affine()
    family = _family()
    _, radii = local.read_point(local.ROOT_CERTIFICATE.read_bytes())
    enclosure = local.root_enclosure(family, radii)
    deviation, audit = local.root_box_audit(family, enclosure, local.DECLARED_BOX, matrix)
    assert audit["passed"]
    assert audit["midpoint_entries_contained"]
    assert 0 < max(deviation) < Q(1, 10**18)
    outcome = _outcome("omega11", -1)
    coordinate = family.names.index("omega11")
    dual, plain = outcome.certificates[0]
    folded = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=dual,
        deviation=deviation,
    )
    assert folded["root_box_residual"] > 0
    assert folded["epsilon"] == plain["epsilon"] + folded["root_box_residual"]
    assert folded["passed"]
    widened = [value * 10**19 for value in deviation]
    refused = local.evaluate_dual(
        matrix,
        _curvature(),
        [local.DECLARED_RADIUS] * 45,
        coordinate=coordinate,
        sign=-1,
        dual=dual,
        deviation=widened,
    )
    assert not refused["passed"]


def test_slides_leave_every_retained_contact_and_anchor_unchanged() -> None:
    slides = local.slide_invariance_audit(_family())
    assert slides["passed"]
    assert slides["identity_options"] == slides["slide_invariant"] == 27
    # Only the two closing contacts carry the midpoint's residual, far below any margin.
    assert set(slides["nonzero_at_midpoint"]) == {"12/16:12:u:1", "16/17:16:p:1"}
    spanning = local.spanning_audit()
    assert spanning["passed"]
    assert spanning["walls"] == {
        "left": [1, 3, 4, 9],
        "right": [7, 8, 17],
        "bottom": [1, 2, 5],
        "top": [4, 8, 15],
    }


def test_recomputed_stress_is_a_nonnegative_stress_on_the_whole_box() -> None:
    audit = local.stress_audit(_family(), local.DECLARED_BOX)
    assert audit["passed"]
    assert all(audit["checks"].values())
    assert audit["rows_reaching_zero"] == []
    assert audit["vertex_ranks_mod_p"] == [46] * 8
    assert audit["least_weight"]["row"] == "pair:11:12:1"
    assert audit["least_weight"]["vertex"] == ["0", "1/12", "-1/8"]
    assert Q(1, 250) < Q(audit["least_weight"]["value_decimal"]) < Q(1, 200)
    # Only the midpoint's two F2 columns (omega12, omega16) are off zero, as in H-258.
    assert set(audit["origin_residual_columns"]) == {
        str(local.column(12, "angle")),
        str(local.column(16, "angle")),
    }


def test_family_stress_needs_the_wall_rebalancing_when_square_5_slides() -> None:
    family = _family()
    origin = (Q(0), Q(0), Q(0))
    _, reference = local.family_stress(family, origin)
    corner = (Q(1, 4), Q(0), Q(0))
    _, unbalanced = local.family_stress(family, corner)
    moved = {c for c, (x, y) in enumerate(zip(unbalanced, reference, strict=True)) if x != y}
    assert moved == {local.column(5, "angle"), local.column(7, "angle")}
    stress, balanced = local.family_stress(family, corner, reference)
    assert balanced == reference
    assert all(stress[key] == 0 for key in local.ZERO_WEIGHT_KEYS)


def test_roster_is_bound_to_the_accepted_h257_inventory() -> None:
    audit = local.roster_binding_audit(_family())
    assert audit["passed"]
    assert (audit["retained_pairs"], audit["retained_walls"]) == (19, 13)
    assert audit["retained_identity_options"] == 27
    raw = local.FEATURE_CERTIFICATE.read_bytes()
    tampered = local.roster_binding_audit(
        _family(), raw.replace(b'"pairs": 21', b'"pairs": 22')
    )
    assert not tampered["checks"]["certificate_blob_is_frozen"]
    assert not tampered["checks"]["manifest_reproduces_counts"]
    assert not tampered["passed"]


def test_restoring_the_non_tight_9_11_row_fails_slide_invariance() -> None:
    audit = local.slide_invariance_audit(_family(), restore=frozenset({(9, 11)}))
    assert not audit["passed"]
    assert audit["identity_options"] == 29
    assert audit["not_invariant"] == ["9/11:11:v:-1", "9/11:9:v:-1"]
