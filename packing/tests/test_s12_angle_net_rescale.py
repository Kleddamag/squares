"""Controls for the s(12) rescale and re-weight tools.

The verifier runs that decide coverage take minutes to an hour and leave receipts under
``cases/n12_beyond_rescaling/``. These are the fast parts that must stay true: the
rescaling arithmetic, the reading of the source verifier's verdict, the D4 orbits, the
exact cell membership, and the retained candidate's well-formedness and total.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from devtools.retained_data import read_retained_bytes
from devtools.s12_angle_net_rescale import (
    RESCALED_309,
    Certificate,
    bin_count,
    load_source,
    parse_certificate,
    parse_output,
    rescale,
    scale_factor,
)
from devtools.s12_reweight import BinFrame, Rows, cell_members, d4_orbits, parse_dump

CASE = Path(__file__).resolve().parents[1] / "cases" / "n12_beyond_rescaling"


def test_source_is_the_reviewed_release() -> None:
    source = load_source()
    assert source.side == Fraction(15680, 3951)
    assert len(source.points) == 1736
    assert source.total_weight == Fraction(119738036, 10**7)


def test_rescale_reproduces_309() -> None:
    source = load_source()
    scaled = rescale(source, 2, 7901)
    assert scaled.side == RESCALED_309
    assert scale_factor(source, 2, 7901) == Fraction(7902, 7901)
    assert scaled.total_weight == source.total_weight
    assert scaled.points[0][:2] == (2 * source.points[0][0], 2 * source.points[0][1])
    # the format's grid condition: s_den divides s_num * D
    assert (scaled.s_num * scaled.denominator) % scaled.s_den == 0


def test_rescale_refuses_nonpositive() -> None:
    with pytest.raises(ValueError, match="positive"):
        rescale(load_source(), 0, 10)


def test_text_round_trip() -> None:
    cert = Certificate(4, 1, 2, 10, ((1, 1, 3), (7, 1, 3)))
    assert parse_certificate(cert.text().encode()) == cert
    with pytest.raises(ValueError, match="count"):
        parse_certificate(b"4 1 2 10 2 1 1 3")


def test_bin_count_matches_source() -> None:
    # verify/ at N = 6000 sweeps k = 0..2486, as its log and xcheck.py's 2486 bins say
    assert bin_count(6000) == 2486


VERIFIED = """D4-symmetric atom set: true  -> angles cover [0,45] deg
angles: k=0..2486 (N=6000), covering [0,45deg]
min covered weight over ALL placements = 10000056/10000000 = 1.000006  (at angle k=0)
VERIFIED: every CLOSED unit square inside C covers weight >= 1, and total weight < 12.
"""


def test_parse_output_verdicts() -> None:
    good = parse_output(VERIFIED, 0)
    assert good.verified
    assert (good.least_weight, good.least_bin) == ("10000056/10000000", 0)
    assert (good.net, good.last_bin) == (6000, 2486)
    partial = parse_output(
        "PARTIAL RUN: VERIFY_BINS=0:3\n"
        + VERIFIED.replace("VERIFIED:", "NOT VERIFIED (PARTIAL"),
        0,
    )
    assert not partial.verified
    assert partial.partial
    refused = parse_output(VERIFIED.replace("VERIFIED:", "x") + "NOT VERIFIED\n", 0)
    assert not refused.verified
    assert not parse_output(VERIFIED, 2).verified


def test_source_orbits_are_d4() -> None:
    source = load_source()
    orbits = d4_orbits(source)
    assert sum(len(o) for o in orbits) == 1736
    assert {len(o) for o in orbits} <= {1, 4, 8}
    for orbit in orbits:
        assert len({source.points[i][2] for i in orbit}) == 1


def test_orbits_refuse_an_asymmetric_set() -> None:
    with pytest.raises(ValueError, match="D4"):
        d4_orbits(Certificate(4, 1, 1, 1, ((1, 2, 1), (2, 1, 1))))


def test_cell_members_is_the_closed_square() -> None:
    # axis-parallel bin (cn = g, sn = 0), unit over DEN = 2 sg_d wm_d D g with all ones:
    # points at (0,0), (1,0), (3,0); centre cell around u = (1, 0), half-side 1
    cert = Certificate(4, 1, 1, 1, ((0, 0, 1), (1, 0, 1), (3, 0, 1)))
    frame = BinFrame(k=0, den=2, cn=1, sn=0, g=1, hh=2, sg_n=1, sg_d=1, wm_d=1)
    # q = 2 * x * k1 with k1 = 2: points at 0, 4, 12 over DEN; reach 2 * hh = 4 around 2 * mid
    assert cell_members(cert, frame, (1, 3, -1, 1)) == frozenset({0, 1})
    assert cell_members(cert, frame, (4, 6, -1, 1)) == frozenset({2})


def test_parse_dump_reads_cells() -> None:
    text = (
        "# header\nbin 3 6000 0.1 100 5 6 7 8 9 10 11 12 0 0 0 1\n"
        "c 3 1 2 3 4 999 0.5 0.5 1e-9\n"
    )
    ((frame, cell, captured),) = parse_dump(text)
    assert (frame.k, frame.cn, frame.sn, frame.g, frame.hh) == (3, 5, 6, 7, 8)
    assert cell == (1, 2, 3, 4)
    assert captured == 999


def test_rows_deduplicate_by_orbit_counts() -> None:
    rows = Rows(np.array([0, 0, 1]), 2)
    assert rows.add(frozenset({0, 2}))
    assert not rows.add(frozenset({1, 2}))
    assert rows.add(frozenset({0, 1}))
    assert len(rows.rows) == 2


@pytest.mark.skipif(not (CASE / "certificate.txt.gz").exists(), reason="no candidate retained")
def test_retained_candidate_is_well_formed() -> None:
    cert = parse_certificate(read_retained_bytes(CASE / "certificate.txt"))
    claim = json.loads((CASE / "claim.json").read_text(encoding="utf-8"))
    assert cert.side == Fraction(claim["container"]) > RESCALED_309
    assert cert.total_weight == Fraction(claim["total_weight"]) < 12
    assert all(w >= 0 for _, _, w in cert.points)
    assert all(0 <= x <= cert.side * cert.denominator for x, _, _ in cert.points)
    d4_orbits(cert)  # D4-symmetric, so the source's [0, 45] reduction applies
