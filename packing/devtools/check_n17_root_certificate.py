"""Independently check the fixed H255 rational contraction certificate.

Only the standard library is used. Polynomial construction, differentiation, interval
arithmetic, inversion and acceptance are independent of the certificate producer.
Importing this module neither reads nor evaluates the target source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

Polynomial = dict[tuple[int, int], int]
Interval = tuple[Fraction, Fraction]
REPO = Path(__file__).resolve().parents[2]
SOURCE_PATH = (
    "packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/"
    "kleddamag-17-squares-certified-bound/upper-packing-certificate.json"
)
SOURCE_SHA256 = "24e296f5995abc9424e2d8d39ea0a8e44953b919430a04f006fa84c56fef45f7"
LABELS = [1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
RADIUS = Fraction(1, 10**12)
MAX_BYTES = 10 * 1024 * 1024
MAX_LITERAL = 20000
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
CORE_FIELDS = {
    "polynomials",
    "F_mid",
    "J_mid",
    "C",
    "J_box",
    "M",
    "row_norms",
    "q",
    "correction",
    "inclusion_bounds",
}


class CertificateError(ValueError):
    """The claimed certificate does not prove the frozen H255 proposition."""


def rational(value: Any) -> Fraction:
    if type(value) is not str or len(value) > MAX_LITERAL or not RATIONAL.fullmatch(value):
        raise CertificateError("expected a bounded canonical rational string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CertificateError("invalid rational literal") from error
    if str(result) != value:
        raise CertificateError("noncanonical rational string")
    return result


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != keys:
        raise CertificateError(f"wrong {label} fields")
    return value


def _pair(value: Any) -> tuple[Fraction, Fraction]:
    if type(value) is not list or len(value) != 2:
        raise CertificateError("expected two rational components")
    return rational(value[0]), rational(value[1])


def _same(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise CertificateError(f"recomputed {label} differs from certificate")


def add(left: Interval, right: Interval) -> Interval:
    return left[0] + right[0], left[1] + right[1]


def multiply(left: Interval, right: Interval) -> Interval:
    products = [a * b for a in left for b in right]
    return min(products), max(products)


def point(value: int | Fraction) -> Interval:
    return Fraction(value), Fraction(value)


def power(value: Interval, exponent: int) -> Interval:
    if exponent < 0 or value[0] > value[1]:
        raise CertificateError("invalid interval power")
    if exponent == 0:
        return point(1)
    endpoints = value[0] ** exponent, value[1] ** exponent
    lower = 0 if exponent % 2 == 0 and value[0] <= 0 <= value[1] else min(endpoints)
    return Fraction(lower), max(endpoints)


def _sum(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, 0) + coefficient
    return {key: value for key, value in result.items() if value}


def _scale(polynomial: Polynomial, coefficient: int) -> Polynomial:
    return {
        key: value * coefficient for key, value in polynomial.items() if value * coefficient
    }


def _product(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {(0, 0): 1}
    for polynomial in polynomials:
        terms: Polynomial = {}
        for (i, j), coefficient in result.items():
            for (k, ell), other in polynomial.items():
                exponent = i + k, j + ell
                terms[exponent] = terms.get(exponent, 0) + coefficient * other
        result = {key: value for key, value in terms.items() if value}
    return result


def n17_polynomials() -> tuple[Polynomial, Polynomial]:
    """Expand the two independently derived positive-normalization formulas."""
    one, t, b = {(0, 0): 1}, {(1, 0): 1}, {(0, 1): 1}
    t2, b2 = _product(t, t), _product(b, b)
    d, e = _sum(one, t2), _sum(one, b2)
    plus_t, minus_t = _sum(one, t), _sum(one, _scale(t, -1))
    minus_t2, minus_b2 = _sum(one, _scale(t2, -1)), _sum(one, _scale(b2, -1))
    ell = _product(plus_t, d)
    first = _sum(
        _scale(_product(t, minus_t, minus_b2), 2),
        _product(minus_t, minus_t, ell, b),
        _scale(_product(t, ell, e), -1),
    )
    alpha_numerator = _sum(_product(minus_t2, minus_b2), _scale(_product(t, b), -4))
    second = _sum(
        _product(minus_t2, d, e, e),
        _scale(_product(plus_t, d, e, _sum(_product(b, minus_t2), _product(t, minus_b2))), -1),
        _scale(_product(minus_t, minus_b2, alpha_numerator), -1),
    )
    return first, second


def derivative(polynomial: Polynomial, coordinate: int) -> Polynomial:
    if coordinate not in (0, 1):
        raise CertificateError("invalid derivative coordinate")
    result: Polynomial = {}
    for (i, j), coefficient in polynomial.items():
        exponent = (i, j)[coordinate]
        if exponent:
            result[i - (coordinate == 0), j - (coordinate == 1)] = coefficient * exponent
    return result


def evaluate(polynomial: Polynomial, box: tuple[Interval, Interval]) -> Interval:
    """Natural interval evaluation of the expanded sparse monomial polynomial."""
    result = point(0)
    for (i, j), coefficient in sorted(polynomial.items()):
        term = multiply(power(box[0], i), power(box[1], j))
        result = add(result, multiply(point(coefficient), term))
    return result


def _encode(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [_encode(item) for item in value]
    return value


def _terms(polynomial: Polynomial) -> list[list[int | str]]:
    return [[i, j, str(coefficient)] for (i, j), coefficient in sorted(polynomial.items())]


def quantities(
    polynomials: tuple[Polynomial, Polynomial],
    midpoint: tuple[Fraction, Fraction],
    radius: Fraction,
) -> dict[str, Any]:
    """Recompute a complete exact certificate, without deciding target identity."""
    if radius <= 0:
        raise CertificateError("radius must be strictly positive")
    box = tuple((value - radius, value + radius) for value in midpoint)
    at_midpoint = point(midpoint[0]), point(midpoint[1])
    derivatives = [[derivative(polynomial, j) for j in range(2)] for polynomial in polynomials]
    values = [evaluate(polynomial, at_midpoint)[0] for polynomial in polynomials]
    jacobian = [[evaluate(entry, at_midpoint)[0] for entry in row] for row in derivatives]
    a, b = jacobian[0]
    c, d = jacobian[1]
    determinant = a * d - b * c
    if determinant == 0:
        raise CertificateError("singular midpoint Jacobian")
    inverse = [[d / determinant, -b / determinant], [-c / determinant, a / determinant]]
    for left, right in ((inverse, jacobian), (jacobian, inverse)):
        product = [
            [sum(left[i][k] * right[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)
        ]
        if product != [[1, 0], [0, 1]]:
            raise CertificateError("inverse identity failure")
    jbox = [[evaluate(entry, (box[0], box[1])) for entry in row] for row in derivatives]
    residual: list[list[Interval]] = []
    for i in range(2):
        row: list[Interval] = []
        for j in range(2):
            entry = point(int(i == j))
            for k in range(2):
                entry = add(entry, multiply(point(-inverse[i][k]), jbox[k][j]))
            row.append(entry)
        residual.append(row)
    norms = [sum((max(abs(lo), abs(hi)) for lo, hi in row), Fraction(0)) for row in residual]
    correction = [
        sum((inverse[i][j] * values[j] for j in range(2)), Fraction(0)) for i in range(2)
    ]
    inclusion = [abs(correction[i]) + radius * norms[i] for i in range(2)]
    return {
        "polynomials": [_terms(polynomial) for polynomial in polynomials],
        "F_mid": _encode(values),
        "J_mid": _encode(jacobian),
        "C": _encode(inverse),
        "J_box": _encode(jbox),
        "M": _encode(residual),
        "row_norms": _encode(norms),
        "q": str(max(norms)),
        "correction": _encode(correction),
        "inclusion_bounds": _encode(inclusion),
    }


def _validate_scalars(value: Any) -> None:
    if type(value) is list:
        for entry in value:
            _validate_scalars(entry)
    else:
        rational(value)


def check_quantities(
    document: dict[str, Any],
    polynomials: tuple[Polynomial, Polynomial],
    midpoint: tuple[Fraction, Fraction],
    radius: Fraction,
) -> dict[str, Any]:
    """Reject altered claims and enforce both strict contraction inequalities."""
    expected = quantities(polynomials, midpoint, radius)
    for field in CORE_FIELDS - {"polynomials"}:
        _validate_scalars(document.get(field))
        _same(document[field], expected[field], field)
    supplied = document.get("polynomials")
    if type(supplied) is not list or len(supplied) != 2:
        raise CertificateError("expected two sparse polynomials")
    for polynomial in supplied:
        if type(polynomial) is not list:
            raise CertificateError("expected sparse monomial lists")
        for term in polynomial:
            if (
                type(term) is not list
                or len(term) != 3
                or any(type(x) is not int for x in term[:2])
            ):
                raise CertificateError("invalid monomial exponents")
            rational(term[2])
    _same(supplied, expected["polynomials"], "polynomials")
    if rational(expected["q"]) >= 1:
        raise CertificateError("contraction norm is not strictly below one")
    if any(rational(bound) >= radius for bound in expected["inclusion_bounds"]):
        raise CertificateError("inclusion is not strictly inside the box")
    return expected


def domain_intervals(midpoint: tuple[Fraction, Fraction], radius: Fraction) -> dict[str, Any]:
    t, b = [(value - radius, value + radius) for value in midpoint]
    d, e = add(point(1), power(t, 2)), add(point(1), power(b, 2))
    ell = multiply(add(point(1), t), d)
    k = add(add(point(1), multiply(point(2), t)), multiply(point(-1), power(t, 2)))
    lower = add(add(multiply(point(187), power(t, 2)), multiply(point(-214), t)), point(53))
    upper = add(add(multiply(point(1169), power(t, 2)), multiply(point(-1338), t)), point(331))
    return {
        name: _encode(value)
        for name, value in {
            "t": t,
            "b": b,
            "D": d,
            "E": e,
            "L": ell,
            "K": k,
            "side_guard_lower": lower,
            "side_guard_upper": upper,
        }.items()
    }


def check_domain(domain: dict[str, Any]) -> None:
    values = {name: _pair(value) for name, value in domain.items()}
    if any(lo > hi for lo, hi in values.values()):
        raise CertificateError("reversed domain interval")
    for name, lo, hi in (
        ("t", Fraction(36, 100), Fraction(37, 100)),
        ("b", Fraction(33, 100), Fraction(34, 100)),
    ):
        if values[name][0] < lo or values[name][1] > hi:
            raise CertificateError(f"{name} box is outside frozen domain")
    if any(values[name][0] <= 0 for name in ("t", "L", "D", "E", "K")):
        raise CertificateError("positive denominator guard failed")
    if values["side_guard_lower"][0] < 0 or values["side_guard_upper"][1] > 0:
        raise CertificateError("side-domain guard failed")


def source_midpoint(raw: bytes) -> tuple[Fraction, Fraction]:
    """Bind midpoint selection to the already admitted source bytes and label map."""
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise CertificateError("source digest differs from H253")
    source = json.loads(raw, object_pairs_hook=_object)
    if type(source) is not dict or _source_fraction(source.get("side")) != Fraction(
        4675530093604551, 10**15
    ):
        raise CertificateError("wrong source side")
    squares = source.get("squares")
    if type(squares) is not list or len(squares) != 17:
        raise CertificateError("wrong source count")
    for square in squares:
        _keys(square, {"x", "y", "t"}, "source square")
        for value in square.values():
            _source_fraction(value)
    return _source_fraction(squares[LABELS.index(9)]["t"]), -_source_fraction(
        squares[LABELS.index(16)]["t"]
    )


def _source_fraction(value: Any) -> Fraction:
    # Source bytes were fixed before this schema; reduced spelling is not required.
    if type(value) is not str or len(value) > MAX_LITERAL or not RATIONAL.fullmatch(value):
        raise CertificateError("invalid exact source scalar")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise CertificateError("invalid exact source scalar") from error


def check(document: Any, source: bytes) -> dict[str, Any]:
    """Check the frozen target contract; no alternative polynomial or box is admitted."""
    _keys(
        document,
        CORE_FIELDS
        | {"schema", "source", "box", "domain", "provenance", "criterion_passed", "failures"},
        "certificate",
    )
    _same(document["schema"], "n17-root-certificate/v1", "schema")
    metadata = _keys(document["source"], {"sha256", "path", "row_to_label"}, "source")
    _same(metadata["sha256"], SOURCE_SHA256, "source digest")
    _same(metadata["path"], SOURCE_PATH, "source path")
    labels = metadata["row_to_label"]
    if type(labels) is not list or any(type(label) is not int for label in labels):
        raise CertificateError("invalid source label map")
    _same(labels, LABELS, "source label map")
    box = _keys(document["box"], {"midpoint", "radius"}, "box")
    midpoint, radius = _pair(box["midpoint"]), rational(box["radius"])
    _same(radius, RADIUS, "frozen radius")
    _same(midpoint, source_midpoint(source), "source midpoint")
    provenance = _keys(
        document["provenance"], {"git_commit", "git_clean", "git_clean_scope"}, "provenance"
    )
    if (
        type(provenance["git_commit"]) is not str
        or re.fullmatch(r"[0-9a-f]{40}", provenance["git_commit"]) is None
        or type(provenance["git_clean"]) is not bool
    ):
        raise CertificateError("malformed Git provenance")
    _same(provenance["git_clean_scope"], "tracked", "Git cleanliness scope")
    if provenance["git_clean"] is not True:
        raise CertificateError("producer implementation was not tracked-clean")
    if document["criterion_passed"] is not True:
        raise CertificateError("producer did not claim acceptance")
    _same(document["failures"], [], "producer failures")
    expected = check_quantities(document, n17_polynomials(), midpoint, radius)
    domain = domain_intervals(midpoint, radius)
    _same(document["domain"], domain, "domain intervals")
    check_domain(domain)
    return {
        "verification_passed": True,
        "schema": "n17-root-check/v1",
        "source_sha256": SOURCE_SHA256,
        "q": expected["q"],
        "inclusion_bounds": expected["inclusion_bounds"],
        "limitations": (
            "Same contraction method; root existence only, "
            "not endpoint packing feasibility or optimality."
        ),
    }


def _read(path: Path) -> bytes:
    with path.open("rb") as stream:
        result = stream.read(MAX_BYTES + 1)
    if len(result) > MAX_BYTES:
        raise CertificateError("input exceeds 10 MiB")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--source", type=Path, default=REPO / SOURCE_PATH)
    args = parser.parse_args()
    try:
        document = json.loads(_read(args.certificate), object_pairs_hook=_object)
        receipt = check(document, _read(args.source))
    except (ValueError, OSError, RecursionError) as error:
        print(json.dumps({"verification_passed": False, "error": str(error)}, sort_keys=True))
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
