"""The two-radius rectangle is rebuilt exactly, compared exactly, and audited unchanged."""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n11_optimality_local_dual as dual
from devtools import check_n11_optimality_local_isolation as local
from devtools import check_n11_optimality_local_two_radius as two

RECEIPT = two.PACKET / "receipts/local-isolation-two-radius"
TIMING = {"phases", "wall_seconds", "process_cpu_seconds", "max_seconds"}


def accepted_focused() -> bytes:
    return two.decode(two.OBJECTS / f"{two.ACCEPTED_FOCUSED_SHA}.gz", two.ACCEPTED_FOCUSED_SHA)


def without_timing(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: without_timing(item) for key, item in value.items() if key not in TIMING}
    if isinstance(value, list):
        return [without_timing(item) for item in value]
    return value


def test_variant_reproduces_the_pinned_digest() -> None:
    raw = accepted_focused()
    variant = two.build_variant(raw, two.replacement_radii())
    assert hashlib.sha256(variant).hexdigest() == two.VARIANT_SHA
    original, rebuilt = json.loads(raw), json.loads(variant)
    changed = {key for key in original if original[key] != rebuilt[key]}
    assert changed == {"radii", "inclusion"}
    assert rebuilt["radii"].count("1/128") == 2
    assert [rebuilt["radii"][index] for index in two.WIDE_COORDINATES] == ["1/128"] * 2
    for before, after in zip(original["inclusion"], rebuilt["inclusion"], strict=True):
        assert {key for key in before if before[key] != after[key]} == {"radii"}


def test_a_changed_radius_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    changed = two.replacement_radii()
    changed[0] = Fraction(1, 255)
    variant = two.build_variant(accepted_focused(), changed)
    assert hashlib.sha256(variant).hexdigest() != two.VARIANT_SHA
    monkeypatch.setattr(two, "replacement_radii", lambda: changed)
    with pytest.raises(ValueError, match="variant digest differs"):
        two.check(max_seconds=30)
    focused = json.loads(accepted_focused())
    focused["radii"][5] = "1/1000"
    objects = tmp_path / "objects"
    objects.mkdir()
    weighted = f"{dual.WEIGHTED_SHA}.gz"
    (objects / weighted).symlink_to(two.OBJECTS / weighted)
    (objects / f"{two.ACCEPTED_FOCUSED_SHA}.gz").write_bytes(
        gzip.compress(two.serialize(focused), mtime=0)
    )
    with pytest.raises(ValueError, match="decoded object digest differs"):
        two.check(objects=objects, max_seconds=30)
    with pytest.raises(ValueError, match="inclusion radii differ"):
        two.build_variant(two.serialize(focused), two.replacement_radii())


def test_comparison_refuses_a_replacement_below_an_accepted_radius() -> None:
    accepted = [Fraction(value) for value in json.loads(accepted_focused())["radii"]]
    rows = two.radius_comparison(accepted, two.replacement_radii())
    assert len(rows) == 33
    assert all(Fraction(row["ratio"]) <= 1 for row in rows)
    assert max(Fraction(row["ratio"]) for row in rows) == Fraction(35312013, 39062500)
    shrunk = two.replacement_radii()
    shrunk[32] = Fraction(1, 256)
    with pytest.raises(ValueError, match="coordinate 32"):
        two.radius_comparison(accepted, shrunk)


def test_curvature_constants_are_the_reviews() -> None:
    constants = two.curvature_constants()
    assert [row["K_over_r_squared"] for row in constants["pair"]] == [
        "21/2",
        "57/4",
        "99/4",
        "30",
    ]
    assert [row["K_over_r_squared"] for row in constants["wall"]] == ["3/4", "3"]
    assert constants["premises"][0]["gap"] == "63/512"
    assert constants["used_by_audit"] is False


def test_focused_pin_is_restored_after_the_call(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str] = []

    def passing(*_args: object, **_kwargs: object) -> dict[str, Any]:
        seen.append(dual.FOCUSED_SHA)
        return {}

    def failing(*_args: object, **_kwargs: object) -> dict[str, Any]:
        seen.append(dual.FOCUSED_SHA)
        raise ValueError("audit refused")

    monkeypatch.setattr(local, "audit", passing)
    assert two.audited(Path("w"), Path("f"), max_seconds=1) == {}
    assert dual.FOCUSED_SHA == two.ACCEPTED_FOCUSED_SHA
    monkeypatch.setattr(local, "audit", failing)
    with pytest.raises(ValueError, match="audit refused"):
        two.audited(Path("w"), Path("f"), max_seconds=1)
    assert dual.FOCUSED_SHA == two.ACCEPTED_FOCUSED_SHA
    assert seen == [two.VARIANT_SHA, two.VARIANT_SHA]


def test_retained_receipt_binds_its_result_and_scope() -> None:
    raw = (RECEIPT / "result.json").read_bytes()
    result = json.loads(raw)
    provenance = json.loads((RECEIPT / "provenance.json").read_text())
    assert provenance["result_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["status"] == two.PASS
    assert result["replaces_accepted_component"] is False
    assert result["global_optimality_proved"] is False
    assert result["isolation_audit"]["status"] == "PASS_INDEPENDENT_FIXED_T_LOCAL_ISOLATION"
    assert result["isolation_audit"]["checker_sha256"] == provenance["isolation_checker_sha256"]
    assert result["isolation_audit"]["input_sha256"]["focused"] == two.VARIANT_SHA
    assert result["signed_coordinate_margins_checked"] == 8448
    assert result["unavailable_feature_margins_checked"] == 88
    assert Fraction(result["worst_dual_ratio"]) < 1
    assert result["two_radius_checker_sha256"] == provenance["checker_sha256"]


@pytest.mark.slow
def test_retained_result_matches_a_fresh_audit() -> None:
    fresh = two.check(max_seconds=90)
    retained = json.loads((RECEIPT / "result.json").read_text())
    assert without_timing(fresh) == without_timing(retained)
    assert dual.FOCUSED_SHA == two.ACCEPTED_FOCUSED_SHA
