"""The independent corner checker must honor its Witness/v2 geometry contract."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from devtools.check_rational_witness_independent import check, parse
from sqpack.witness import WitnessError, exact_verify, load_witness

WITNESSES = Path(__file__).resolve().parent.parent / "witnesses"


def _grid_document() -> dict:
    return yaml.safe_load((WITNESSES / "grid-n004.yaml").read_text(encoding="utf-8"))


def _write(path: Path, document: dict) -> Path:
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


def test_centered_corners_do_not_pass_as_lower_left_geometry(tmp_path: Path) -> None:
    document = _grid_document()
    witness = document["witness"]
    witness["id"] = "W-centered-control"
    witness["n"] = 1
    witness["squares"] = [deepcopy(witness["squares"][1])]
    lower_left = _write(tmp_path / "lower-left.yaml", document)
    assert check(lower_left)["verification_passed"]

    witness["coordinates"]["origin"] = "container-center"
    centered = _write(tmp_path / "centered.yaml", document)
    with pytest.raises(ValueError, match="lower-left"):
        parse(centered)
    main_witness = load_witness(centered, fallback_schema=WITNESSES / "witness.schema.yaml")
    assert not exact_verify(main_witness)[1].valid


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("square_size", "2", "unit squares"),
        (
            "coordinates",
            {"origin": "lower-left", "axes": "x-left-y-up", "angle_unit": "not-applicable"},
            "x-right-y-up",
        ),
        (
            "coordinates",
            {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "radians"},
            "x-right-y-up",
        ),
    ],
)
def test_unsupported_geometry_metadata_rejects(
    tmp_path: Path, field: str, value: object, message: str
) -> None:
    document = _grid_document()
    document["witness"][field] = value
    path = _write(tmp_path / "bad-metadata.yaml", document)
    with pytest.raises(ValueError, match=message):
        parse(path)
    with pytest.raises(WitnessError):
        load_witness(path, fallback_schema=WITNESSES / "witness.schema.yaml")


def test_complete_positive_integer_count_is_required(tmp_path: Path) -> None:
    document = _grid_document()
    document["witness"]["n"] = 3
    path = _write(tmp_path / "incomplete.yaml", document)
    with pytest.raises(ValueError, match="complete square list"):
        parse(path)

    document["witness"]["squares"] = document["witness"]["squares"][:1]
    document["witness"]["n"] = True
    path = _write(tmp_path / "boolean-count.yaml", document)
    with pytest.raises(ValueError, match="complete square list"):
        parse(path)


def test_non_contract_and_non_rational_corners_reject(tmp_path: Path) -> None:
    document = _grid_document()
    document["softschema"]["contract"] = "other:Witness/v2"
    path = _write(tmp_path / "wrong-contract.yaml", document)
    with pytest.raises(ValueError, match="Witness/v2 contract"):
        parse(path)

    document["softschema"]["contract"] = "packing.squares:Witness/v2"
    document["witness"]["squares"][0]["corners"][0][0] = 0.0
    path = _write(tmp_path / "float-corner.yaml", document)
    with pytest.raises(ValueError, match="rational strings"):
        parse(path)
