"""The review's exact audit of the re-weighted s(12) certificate, and controls on the audit.

The audit itself must pass on the retained case, and each of its load-bearing checks must
refuse a certificate that breaks it: a weight moved off its orbit, a negative weight, a
point outside the container, a total of 12.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from devtools.audit_s12_reweighted import (
    CASE,
    Cert,
    audit,
    d4_invariant,
    lowered,
    parse,
    regridded,
    sha,
)


def _case() -> Cert:
    return parse(gzip.decompress((CASE / "certificate.txt.gz").read_bytes()))


def test_audit_passes_on_the_retained_case() -> None:
    checks, facts = audit()
    assert [c["check"] for c in checks if not c["pass"]] == []
    assert facts["points"] == 1736
    assert facts["total"] == "14970347/1250000"


def test_committed_receipt_matches_a_fresh_audit() -> None:
    receipt = json.loads((CASE / "receipts/review-audit.json").read_text(encoding="utf-8"))
    checks, facts = audit()
    assert receipt["status"] == "PASS"
    assert receipt["checks"] == checks
    assert receipt["facts"] == facts


def test_moving_weight_off_an_orbit_breaks_d4() -> None:
    cert = _case()
    x, y, w = cert.points[0]
    moved = Cert(cert.s_num, cert.s_den, cert.d, cert.w, ((x, y, w + 1), *cert.points[1:]))
    assert d4_invariant(cert)
    assert not d4_invariant(moved)


def test_controls_keep_d4_and_change_what_they_say() -> None:
    cert = _case()
    one = lowered(cert, 3948000, 3134000, 100)
    assert d4_invariant(one)
    assert sum(1 for p, q in zip(one.points, cert.points, strict=True) if p != q) == 8
    assert cert.total - one.total == pytest.approx(800 / 10**7)
    two = regridded(cert, 3949000)
    assert str(two.side) == "15680/3949"
    assert two.points == cert.points
    assert sha(one.to_bytes()) != sha(two.to_bytes())


@pytest.mark.parametrize(
    "text",
    [
        b"15680000 3949423\n3949423\n10000000\n1\n0 0 -1\n",  # a negative weight
        b"15680000 3949423\n3949423\n10000000\n2\n0 0 1\n",  # a missing point line
        b"15680000 3949422\n3949423\n10000000\n1\n0 0 1\n",  # side off the grid
        b"0 1\n1\n1\n1\n0 0 1\n",  # a zero header value
    ],
)
def test_parse_refuses_malformed_files(text: bytes) -> None:
    with pytest.raises(ValueError, match=r"integers|header|count|divide"):
        parse(text)


def test_a_point_outside_the_container_is_visible() -> None:
    cert = parse(b"4 1\n1\n1\n1\n5 0 1\n")
    assert cert.points[0][0] > cert.s_num * cert.d // cert.s_den


def test_case_directory_is_where_the_audit_reads() -> None:
    assert Path(CASE / "claim.json").is_file()
