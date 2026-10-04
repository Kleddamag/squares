"""The kernel verifier's node reader gives what `json.loads` gives or refuses, and its memo
bounds change no receipt (the streamed-verifier review of 2026-10-04).

`NodeStream` replaced `json.loads` of the whole decompressed node. These tests hold it to
the property the review established: for any bytes, it yields exactly what `json.loads`
of the decompressed file yields, member by member and step by step, with that document's
content id, or it refuses before setting a content id. Generated nodes are read at reads
of one byte and up, so that every number, string, escape and surrogate pair is split
between reads somewhere.
"""

from __future__ import annotations

import ast
import gzip
import hashlib
import inspect
import json
import random
from collections.abc import Callable
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import verify_n17_kernel_certificate as kernel_verifier
from tests.test_verify_n17_certificates import (
    W7_BINS8,
    blind_cells,
    blind_pair,
    canonical,
    pair_cells,
    split_certificate,
)

BLANKS = " \t\n\r"
CHARACTERS = 'aZ0 "\\/\b\f\n\r\t\x00\x1f\x7f\u00e9\u2028\ufeff\uffff\U0001f600\U0010ffff'
# Members that sort before `steps` must precede it; those after may go on either side.
BEFORE_STEPS = ("B", "U", "closed", "final_state", "mask", "s", "stepr")
AFTER_STEPS = ("st\u00e9", "steps0", "terminal", "z", "\U0001f600")
READS = (1, 2, 3, 7, 1 << 20)


def blank(rng: random.Random) -> str:
    return "".join(rng.choice(BLANKS) for _ in range(rng.choice((0, 0, 1, 3))))


def string(rng: random.Random, text: str, *, lone: bool = True) -> str:
    """`text` as a JSON string, each character written raw or escaped at random, astral
    characters sometimes as surrogate-pair escapes, and, if `lone`, sometimes after a lone
    surrogate."""
    out = ['"']
    if lone and rng.random() < 0.1:
        out.append(rng.choice(("\\ud83d", "\\uDC00", "\\udbff\\u0041")))
    for ch in text:
        code = ord(ch)
        if ch in '"\\' or code < 0x20:
            short = {'"': '\\"', "\\": "\\\\", "\n": "\\n", "\t": "\\t", "\b": "\\b"}
            out.append(short.get(ch) or f"\\u{code:04x}")
        elif code > 0xFFFF and rng.random() < 0.5:
            high, low = 0xD800 + ((code - 0x10000) >> 10), 0xDC00 + ((code - 0x10000) & 0x3FF)
            out.append(f"\\u{high:04x}\\u{low:04X}")
        elif rng.random() < 0.2:
            out.append(f"\\u{code:04x}" if code <= 0xFFFF else ch)
        else:
            out.append(ch)
    return "".join([*out, '"'])


def number(rng: random.Random) -> str:
    if rng.random() < 0.08:
        return rng.choice(("NaN", "Infinity", "-Infinity", "1e400", "-0", "0e-999"))
    whole = "0" if rng.random() < 0.2 else str(rng.randint(1, 10 ** rng.randint(1, 30)))
    fraction = "." + str(rng.randint(0, 10**12)) if rng.random() < 0.4 else ""
    exponent = rng.choice("eE") + rng.choice(("", "+", "-")) + str(rng.randint(0, 40))
    return (
        ("-" if rng.random() < 0.3 else "")
        + whole
        + fraction
        + (exponent if rng.random() < 0.3 else "")
    )


def value(rng: random.Random, depth: int) -> str:
    kind = rng.random()
    if depth <= 0 or kind < 0.4:
        scalar = rng.random()
        if scalar < 0.45:
            return number(rng)
        if scalar < 0.85:
            text = "".join(rng.choice(CHARACTERS) for _ in range(rng.randint(0, 6)))
            return string(rng, text)
        return rng.choice(("true", "false", "null"))
    if kind < 0.65:
        items = [value(rng, depth - 1) + blank(rng) for _ in range(rng.randint(0, 3))]
        return "[" + blank(rng) + ("," + blank(rng)).join(items) + "]"
    return obj(rng, depth)


def obj(rng: random.Random, depth: int) -> str:
    """An object, sometimes repeating a name: `json` keeps the last, and so must a step."""
    names = [rng.choice(("a", "index", "rows", "\u00e9", "")) for _ in range(rng.randint(0, 4))]
    members = [
        string(rng, name) + blank(rng) + ":" + blank(rng) + value(rng, depth - 1) + blank(rng)
        for name in names
    ]
    return "{" + blank(rng) + ("," + blank(rng)).join(members) + "}"


def node_text(rng: random.Random) -> str:
    early: list[str] = list(rng.sample(BEFORE_STEPS, rng.randint(0, 3)))
    late: list[str] = []
    for name in rng.sample(AFTER_STEPS, rng.randint(0, 3)):
        (early if rng.random() < 0.5 else late).append(name)
    rng.shuffle(early)
    steps = [
        obj(rng, 3) if rng.random() < 0.9 else value(rng, 2) for _ in range(rng.randint(0, 4))
    ]
    array = "[" + blank(rng) + ("," + blank(rng)).join(s + blank(rng) for s in steps) + "]"

    def member(name: str, text: str) -> str:
        return string(rng, name) + blank(rng) + ":" + blank(rng) + text + blank(rng)

    members = [member(name, value(rng, 2)) for name in early]
    members.append(string(rng, "steps", lone=False) + blank(rng) + ":" + blank(rng) + array)
    members.extend(member(name, value(rng, 2)) for name in late)
    return blank(rng) + "{" + blank(rng) + ("," + blank(rng)).join(members) + "}" + blank(rng)


def read(path: Path) -> tuple[dict[str, Any], list[Any], str] | None:
    """What the stream yields, read to its end, or None when it refuses."""
    try:
        stream = kernel_verifier.NodeStream(path)
        steps = list(stream.steps())
    except kernel_verifier.VerificationError, ValueError, EOFError, OSError:
        return None
    assert stream.sha256 is not None
    return stream.header, steps, stream.sha256


def loads(data: bytes) -> Any:
    """`json.loads` of the decompressed bytes, as the verifier read a node before, or None."""
    try:
        return json.loads(gzip.decompress(data))
    except ValueError, EOFError, OSError:
        return None


def assert_same(got: tuple[dict[str, Any], list[Any], str], document: Any) -> None:
    """The stream gave exactly the document: its steps in order, its other members, and
    the SHA-256 of its canonical JSON. NaN is compared by its canonical spelling."""
    header, steps, sha256 = got
    assert isinstance(document, dict)
    assert "steps" in document
    assert canonical(steps) == canonical(document["steps"])
    assert set(header) == set(document) - {"steps"}
    assert canonical({**header, "steps": steps}) == canonical(document)
    assert sha256 == hashlib.sha256(canonical(document)).hexdigest()
    if b"NaN" not in canonical(document):
        assert {**header, "steps": steps} == document


def agrees_or_refuses(path: Path, data: bytes) -> bool:
    """The property: the stream refuses, or gives exactly what `json.loads` gives. Returns
    whether it accepted."""
    _ = path.write_bytes(data)
    got = read(path)
    if got is None:
        return False
    document = loads(data)
    assert document is not None, "the stream accepted bytes json.loads refuses"
    assert_same(got, document)
    return True


def test_the_node_stream_reads_what_json_reads(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Generated nodes, re-spaced at random, with escapes, surrogates split by reads,
    numbers in every form, `NaN` and infinities, names repeated inside steps, and members
    that sort after `steps` on both sides of it: the stream gives `json.loads`'s document
    at every read size."""
    path = tmp_path / "node.json.gz"
    rng = random.Random(20261004)
    for _ in range(120):
        data = gzip.compress(node_text(rng).encode(), mtime=0)
        for size in READS:
            monkeypatch.setattr(kernel_verifier, "READ_BYTES", size)
            assert agrees_or_refuses(path, data)


def test_a_cut_or_damaged_node_is_refused_or_read_exactly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every prefix of some generated nodes, single bytes changed, data appended: whatever
    the stream accepts is exactly what `json.loads` accepts, and a proper prefix of a node
    is never read to its end unless all it lost was trailing blanks."""
    path = tmp_path / "node.json.gz"
    rng = random.Random(7)
    accepted = refused = 0
    for case in range(24):
        raw = node_text(rng).encode()
        monkeypatch.setattr(kernel_verifier, "READ_BYTES", (1, 3, 1 << 20)[case % 3])
        cuts = (
            range(len(raw))
            if case in {2, 5}
            else rng.sample(range(len(raw)), min(len(raw), 12))
        )
        for cut in cuts:
            took = agrees_or_refuses(path, gzip.compress(raw[:cut], mtime=0))
            assert not took or raw[cut:].strip(BLANKS.encode()) == b""
        for _ in range(12):
            changed = bytearray(raw)
            changed[rng.randrange(len(raw))] = rng.choice(b'{}[],:"\\0-.eE \x00\xff')
            took = agrees_or_refuses(path, gzip.compress(bytes(changed), mtime=0))
            accepted, refused = accepted + took, refused + (not took)
        for tail in (b"{}", b"x", b"0", b",", b"]"):
            assert not agrees_or_refuses(path, gzip.compress(raw + tail, mtime=0))
    assert accepted
    assert refused


def one_step_node() -> dict[str, Any]:
    return {"mask": [0, 1], "schema": "s", "steps": [{"index": 0}], "terminal": True}


def raw_gzip(text: str) -> bytes:
    return gzip.compress(text.encode(), mtime=0)


ACCEPTED = {
    "NaN and the infinities, as json.loads reads them": raw_gzip(
        '{"U":NaN,"steps":[{"a":Infinity,"b":-Infinity,"c":1e400}],"z":-0}'
    ),
    "a name repeated inside a step: the last one, as json.loads keeps": raw_gzip(
        '{"steps":[{"index":0,"index":1,"rows":[{"a":1,"a":2}]}]}'
    ),
    "a member sorting after steps placed before it": raw_gzip(
        '{"terminal":true,"mask":[0],"steps":[{"index":0}],"z":1}'
    ),
    "the steps member's name written with an escape": raw_gzip('{"st\\u0065ps":[{}]}'),
    "a surrogate pair written as escapes, and a lone surrogate": raw_gzip(
        '{"steps":[{"\\ud83d\\ude00":"\\udc00x"}]}'
    ),
    "blanks everywhere JSON allows them": raw_gzip(' \r\n{ "steps" :\t[ { } , [ ] ] } \n'),
    "two gzip members": raw_gzip('{"mask":[0],"st') + raw_gzip('eps":[{"index":0}]}'),
    "gzip padding of zero bytes": raw_gzip(canonical(one_step_node()).decode()) + bytes(8),
}


def bad_checksum(packed: bytes) -> bytes:
    """The gzip stream with the first byte of its CRC-32 trailer changed."""
    return packed[:-8] + bytes([packed[-8] ^ 1]) + packed[-7:]


REFUSED = {
    "a top-level member repeated, which json.loads would read as the last": raw_gzip(
        '{"mask":[0],"mask":[1],"steps":[]}'
    ),
    "a member sorting before steps placed after it": raw_gzip('{"steps":[],"mask":[0]}'),
    "steps repeated after the array": raw_gzip('{"steps":[],"steps":[{}]}'),
    "a UTF-8 byte-order mark, which json.loads of the bytes skips": gzip.compress(
        b"\xef\xbb\xbf" + canonical(one_step_node()), mtime=0
    ),
    "UTF-16, which json.loads of the bytes detects": gzip.compress(
        json.dumps(one_step_node()).encode("utf-16"), mtime=0
    ),
    "a surrogate encoded in UTF-8, which json.loads of the bytes lets pass": gzip.compress(
        b'{"steps":[{"a":"\xed\xa0\x80"}]}', mtime=0
    ),
    "data after the node": raw_gzip('{"steps":[]} {}'),
    "a node with no steps": raw_gzip('{"mask":[0]}'),
    "steps that are not an array": raw_gzip('{"steps":{"0":{}}}'),
    "a trailing comma among the steps": raw_gzip('{"steps":[{},]}'),
    "a trailing comma among the members": raw_gzip('{"steps":[],"z":1,}'),
    "gzip trailing garbage": raw_gzip('{"steps":[]}') + b"garbage",
    "a gzip checksum that does not match": bad_checksum(raw_gzip('{"steps":[{"index":0}]}')),
    "a cut gzip stream": raw_gzip(canonical(one_step_node()).decode())[:-9],
}


@pytest.mark.parametrize("name", sorted(ACCEPTED))
def test_the_node_stream_reads_what_json_reads_at_the_edges(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    for size in READS:
        monkeypatch.setattr(kernel_verifier, "READ_BYTES", size)
        assert agrees_or_refuses(tmp_path / "node.json.gz", ACCEPTED[name]), name


@pytest.mark.parametrize("name", sorted(REFUSED))
def test_the_node_stream_refuses_input_json_would_read_otherwise_or_not_at_all(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    for size in READS:
        monkeypatch.setattr(kernel_verifier, "READ_BYTES", size)
        assert not agrees_or_refuses(tmp_path / "node.json.gz", REFUSED[name]), name


def outcome(directory: Path, cells: kernel_verifier.Cells) -> str:
    """The receipt's status, or the exception that escaped `verify`: anything but PASS."""
    try:
        return kernel_verifier.verify(directory, cells)["status"]
    except Exception as failure:  # noqa: BLE001 - an escape is also not a PASS
        return type(failure).__name__


def test_a_closure_whose_node_is_cut_after_its_last_step_never_passes(tmp_path: Path) -> None:
    """The closure is derived at the node's last step, so every check passes before the
    file runs out. Cut anywhere in the tail (inside the last step, before the array's
    end, inside `terminal`), or with its gzip stream cut, or with data appended, the
    certificate does not pass: the verifier must read the node to its end."""
    directory = blind_pair(tmp_path)
    cells = blind_cells(tmp_path)
    saved = next(directory.glob("node-*.json.gz"))
    packed = saved.read_bytes()
    raw = gzip.decompress(packed)
    tail = raw.rindex(b"]")
    assert raw[tail:] == b'],"terminal":true}'
    cuts = [tail - 40, tail - 1, tail, tail + 1, tail + 2, tail + 7, tail + 13, tail + 15]
    cuts.append(len(raw) - 1)
    for cut in cuts:
        _ = saved.write_bytes(gzip.compress(raw[:cut], mtime=0))
        assert outcome(directory, cells) != "PASS", cut
    for damaged in (packed[:-9], packed[:-1], gzip.compress(raw + b"{}", mtime=0)):
        _ = saved.write_bytes(damaged)
        assert outcome(directory, cells) != "PASS"
    _ = saved.write_bytes(packed)
    assert outcome(directory, cells) == "PASS"


# ---------------------------------------------------------------------------
# The memo bounds
# ---------------------------------------------------------------------------


def memo_readers() -> dict[str, set[str]]:
    """Each function of the verifier that touches `.facets` or `.forbidden`, by name."""
    tree = ast.parse(inspect.getsource(kernel_verifier))
    found: dict[str, set[str]] = {"facets": set(), "forbidden": set()}
    for function in ast.walk(tree):
        if isinstance(function, ast.FunctionDef):
            for node in ast.walk(function):
                if isinstance(node, ast.Attribute) and node.attr in found:
                    found[node.attr].add(function.name)
    return found


def test_the_memos_are_reached_only_through_their_accessors() -> None:
    """A memo entry is read only by the accessor that computes it when it is missing, so
    no code can take a dropped entry for an absent obligation. `bound_memos` is the only
    other function that touches them, and it only removes."""
    assert memo_readers() == {
        "facets": {"difference", "bound_memos"},
        "forbidden": {"forbidden_region", "bound_memos"},
    }


SQUARE_A = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
SQUARE_B = [(Q(2), Q(0)), (Q(3), Q(0)), (Q(3), Q(1)), (Q(2), Q(1))]
CORE = [(Q(-1, 4), Q(-1, 4)), (Q(1, 4), Q(-1, 4)), (Q(0), Q(1, 4))]


def test_a_replaced_hull_loses_only_its_own_regions_and_recomputes_them() -> None:
    """`bound_memos` drops the regions of the hull the step replaced and nothing else; a
    hull that comes back (here the owner's own, as replace mode may give) is computed
    again, equal to the exact Minkowski difference; an unchanged hull drops nothing."""
    state = kernel_verifier.State(cells=[], cap=Q(4), bins=1, mask=[0, 1])
    state.groups = {0: list(SQUARE_A), 1: list(SQUARE_B)}
    first = state.forbidden_region(state.groups[0], CORE)
    _ = state.forbidden_region(state.groups[1], CORE)
    kernel_verifier.bound_memos(state, 0, state.groups[0])
    assert len(state.forbidden) == 2
    before = state.groups[0]
    state.groups[0] = [(x + 1, y) for x, y in SQUARE_A]
    kernel_verifier.bound_memos(state, 0, before)
    assert set(state.forbidden) == {(tuple(SQUARE_B), tuple(CORE))}
    state.groups[0] = list(SQUARE_A)
    again = state.forbidden_region(state.groups[0], CORE)
    assert again == first == kernel_verifier.minkowski_diff(SQUARE_A, CORE)
    assert again is not first


def test_the_facet_memo_is_cleared_only_past_its_bound(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(kernel_verifier, "MEMO_PAIRS", 2)
    state = kernel_verifier.State(cells=[], cap=Q(4), bins=1, mask=[0])
    state.groups = {0: list(SQUARE_A)}
    cores = [
        tuple(kernel_verifier.homogeneous((x + Q(k, 8), y)) for x, y in SQUARE_A)
        for k in range(3)
    ]
    partner = tuple(kernel_verifier.homogeneous(v) for v in SQUARE_B)
    for core in cores[:2]:
        _ = state.difference(partner, core)
    kernel_verifier.bound_memos(state, 0, state.groups[0])
    assert len(state.facets) == 2
    _ = state.difference(partner, cores[2])
    kernel_verifier.bound_memos(state, 0, state.groups[0])
    assert state.facets == {}
    assert state.difference(partner, cores[0]) == kernel_verifier.difference_facets(
        partner, cores[0]
    )


def no_memo(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every facet set and forbidden region computed afresh at every use."""
    monkeypatch.setattr(
        kernel_verifier.State,
        "difference",
        lambda _, partner, core: kernel_verifier.difference_facets(partner, core),
    )
    monkeypatch.setattr(
        kernel_verifier.State,
        "forbidden_region",
        lambda _, group, core: kernel_verifier.minkowski_diff(group, core),
    )


def empty_after_every_step(monkeypatch: pytest.MonkeyPatch) -> None:
    def empty(state: kernel_verifier.State, owner: int, before: list[Any]) -> None:
        del owner, before
        state.facets.clear()
        state.forbidden.clear()

    monkeypatch.setattr(kernel_verifier, "bound_memos", empty)


def same_receipt(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return {**first, "seconds": None} == {**second, "seconds": None}


@pytest.mark.parametrize("variant", [no_memo, empty_after_every_step])
@pytest.mark.parametrize("pair", ["blind", "wall"])
def test_no_memo_and_an_emptied_memo_give_the_same_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    pair: str,
    variant: Callable[[pytest.MonkeyPatch], None],
) -> None:
    cells = pair_cells(tmp_path, pair)
    bounded = kernel_verifier.verify(split_certificate(tmp_path, pair), cells)
    assert bounded["status"] == "PASS", bounded["failure"]
    variant(monkeypatch)
    assert same_receipt(
        kernel_verifier.verify(split_certificate(tmp_path, pair), cells), bounded
    )


@pytest.mark.slow
def test_the_w7_fixture_replaces_a_hull_and_its_receipt_needs_no_memo(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The blind and wall pairs never replace an owned hull, so the drop of a replaced
    hull's regions is exercised by the W7 8-bin fixture, where one step replaces one: the
    receipt with the bounded memos equals the receipt with none."""
    cells = kernel_verifier.cover_cells()
    replaced: list[int] = []
    bound = kernel_verifier.bound_memos

    def counting(state: kernel_verifier.State, owner: int, before: list[Any]) -> None:
        replaced.append(int(state.groups[owner] != before))
        bound(state, owner, before)

    monkeypatch.setattr(kernel_verifier, "bound_memos", counting)
    bounded = kernel_verifier.verify(W7_BINS8, cells)
    assert sum(replaced) >= 1
    assert bounded["failure"] == "the node is a stall, not a closure"
    no_memo(monkeypatch)
    assert same_receipt(kernel_verifier.verify(W7_BINS8, cells), bounded)
