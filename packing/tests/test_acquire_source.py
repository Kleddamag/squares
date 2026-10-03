"""`devtools.acquire_source` retains a pinned subtree and checks the packet it wrote."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools.acquire_source import (
    DECLARATION,
    MANIFEST,
    RECORD,
    Declaration,
    PinnedOnly,
    Record,
    Rule,
    Source,
    acquire,
    check,
    read_manifest,
)
from devtools.retained_data import describe, is_deterministic_gzip, read_retained_bytes

#: Committed on 2 January by the author's clock and on 1 January in UTC, which is the
#: date a packet is named for.
WHEN = "2026-01-02T03:04:05+09:00"
NAME = "example-source-2026-01-01"
REAL = "wand125-point-and-mixed-2026-10-01"

LARGE = "".join(f"{index} {index * index}\n" for index in range(1500)).encode()
FILES: dict[str, bytes] = {
    "README.md": b"# Example source\n",
    "LICENSE": b"MIT License\n\nCopyright (c) 2026 Example\n",
    "cert/README.md": b"A cover.\n",
    "cert/cover.txt": LARGE,
    "cert/manifest.json": b'{"roots": 4}\n',
    "cert/code/check.py": b"print('checked')\n",
    "cert/bundle.tar.gz": b"\x1f\x8b not really an archive \x00\x01\x02",
    "elsewhere/notes.txt": b"outside the scope\n",
}
RETAINED = ("README.md", "cert/README.md", "cert/cover.txt", "cert/manifest.json")
PINNED = ("LICENSE", "cert/bundle.tar.gz", "cert/code/check.py")

SCRATCH_GIT = (
    "-c",
    "user.name=acquire test",
    "-c",
    "user.email=acquire-test@example.invalid",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "core.hooksPath=/dev/null",
)


def _git(checkout: Path, *arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(checkout), *SCRATCH_GIT, *arguments),
        capture_output=True,
        text=True,
        check=True,
        env={"GIT_AUTHOR_DATE": WHEN, "GIT_COMMITTER_DATE": WHEN, "PATH": "/usr/bin:/bin"},
    )
    return done.stdout.strip()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Scratch:
    """A synthetic upstream checkout, and a repository root holding one packet of it."""

    def __init__(self, base: Path) -> None:
        self.root = base / "repository"
        self.checkout = base / "checkout"
        self.packet = self.root / "packing/resources/web" / NAME
        self.checkout.mkdir()
        _git(self.checkout, "init", "-q")
        for name, data in FILES.items():
            target = self.checkout / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        _git(self.checkout, "add", "--all")
        _git(self.checkout, "commit", "-q", "-m", "publish")
        # Copies an earlier packet already retains: a file, and a directory of files.
        self.earlier = "packing/resources/web/earlier-packet"
        (self.root / self.earlier / "code").mkdir(parents=True)
        (self.root / self.earlier / "LICENSE").write_bytes(FILES["LICENSE"])
        (self.root / self.earlier / "code/check.py").write_bytes(FILES["cert/code/check.py"])
        self.declare()

    def declaration(self) -> Declaration:
        rules: list[Rule] = [
            {
                "match": "LICENSE",
                "reason": "retained by the earlier packet",
                "identical_to": f"{self.earlier}/LICENSE",
            },
            {"match": "cert/*.tar.gz", "reason": "the proof bundle"},
            {
                "match": "cert/code/*",
                "reason": "retained by the earlier packet",
                "identical_to": f"{self.earlier}/code",
            },
        ]
        return {
            "format": acquire_source.DECLARATION_FORMAT,
            "id": "example-source",
            "source_url": "https://example.invalid/author/source",
            "source_ref": "refs/heads/main",
            "source_commit": _git(self.checkout, "rev-parse", "HEAD"),
            "retrieved_at_utc": "2026-01-03T04:05Z",
            "git_scope": "A whole clone; the certificate directory is digested.",
            "archived_dir": "source",
            "license": "MIT (LICENSE)",
            "claims": ["s(1) = 1 (cert)"],
            "scope": ["README.md", "LICENSE", "cert"],
            "pinned_only": rules,
        }

    def declare(self, **changes: object) -> None:
        self.write(DECLARATION, {**self.declaration(), **changes})

    def write(self, relative: Path, value: object) -> None:
        target = self.packet / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def record(self) -> Any:
        return json.loads((self.packet / RECORD).read_text(encoding="utf-8"))

    def acquire(self) -> Source:
        """Write the packet, then the README table that only a person writes."""
        entry = acquire(self.packet, self.checkout, self.root)
        rows = [
            describe(self.packet, self.packet / stored, "upstream").markdown()
            for stored in entry["compressed"]
        ]
        lines = [
            "# Example",
            "",
            "## Compressed Files",
            "",
            "| Stored file | Origin | Git blob | SHA-256, decompressed |",
            "| --- | --- | --- | --- |",
            *rows,
            "",
        ]
        (self.packet / "README.md").write_text("\n".join(lines), encoding="utf-8")
        return entry

    def problems(self) -> list[str]:
        return check(self.packet, self.root)


@pytest.fixture
def scratch(tmp_path: Path) -> Scratch:
    return Scratch(tmp_path)


def test_acquire_retains_the_declared_files_and_pins_the_rest(scratch: Scratch) -> None:
    entry = scratch.acquire()
    source = scratch.packet / "source"

    for name in RETAINED:
        assert read_retained_bytes(source / name) == FILES[name]
    assert not (source / "cert/cover.txt").exists()
    assert is_deterministic_gzip((source / "cert/cover.txt.gz").read_bytes())
    assert (source / "cert/manifest.json").read_bytes() == FILES["cert/manifest.json"]
    for name in (*PINNED, "elsewhere/notes.txt"):
        assert not (source / name).exists()

    scoped = sorted((*RETAINED, *PINNED))
    assert read_manifest(scratch.packet / MANIFEST) == {
        name: _sha256(FILES[name]) for name in scoped
    }
    assert (scratch.packet / MANIFEST).read_text(encoding="utf-8").splitlines() == [
        f"{_sha256(FILES[name])}  ./{name}" for name in scoped
    ]

    assert entry == scratch.record()["sources"][0]
    assert scratch.record()["format"] == "external-source-acquisition-v1"
    assert entry["source_commit"] == _git(scratch.checkout, "rev-parse", "HEAD")
    assert entry["git_tree"] == _git(scratch.checkout, "rev-parse", "HEAD^{tree}")
    assert entry["committed_utc"] == "2026-01-01T18:04:05Z"
    assert entry["archived_path"] == f"packing/resources/web/{NAME}/source"
    assert entry["subtree_manifest"] == f"packing/resources/web/{NAME}/{MANIFEST.as_posix()}"
    assert entry["subtree_file_count"] == 7
    assert entry["subtree_total_bytes"] == sum(len(FILES[name]) for name in scoped)
    assert entry["retained_file_count"] == 4
    assert entry["retained_total_bytes"] == sum(len(FILES[name]) for name in RETAINED)
    assert entry["compressed"] == ["source/cert/cover.txt.gz"]
    assert entry["pinned_only"] == [
        {
            "path": "LICENSE",
            "bytes": len(FILES["LICENSE"]),
            "sha256": _sha256(FILES["LICENSE"]),
            "reason": "retained by the earlier packet",
            "identical_to": f"{scratch.earlier}/LICENSE",
        },
        {
            "path": "cert/bundle.tar.gz",
            "bytes": len(FILES["cert/bundle.tar.gz"]),
            "sha256": _sha256(FILES["cert/bundle.tar.gz"]),
            "reason": "the proof bundle",
        },
        {
            "path": "cert/code/check.py",
            "bytes": len(FILES["cert/code/check.py"]),
            "sha256": _sha256(FILES["cert/code/check.py"]),
            "reason": "retained by the earlier packet",
            "identical_to": f"{scratch.earlier}/code/check.py",
        },
    ]
    assert scratch.problems() == []


def test_the_same_command_reproduces_the_packet(scratch: Scratch) -> None:
    def snapshot() -> dict[str, bytes]:
        return {
            path.relative_to(scratch.packet).as_posix(): path.read_bytes()
            for path in sorted(scratch.packet.rglob("*"))
            if path.is_file()
        }

    scratch.acquire()
    first = snapshot()
    (scratch.packet / "source/stale.txt").write_text("left by an earlier declaration\n")
    scratch.acquire()
    assert snapshot() == first


def _wrong_commit(scratch: Scratch) -> None:
    scratch.declare(source_commit="0" * 40)


def _modified_file(scratch: Scratch) -> None:
    (scratch.checkout / "cert/manifest.json").write_bytes(b'{"roots": 5}\n')


def _idle_rule(scratch: Scratch) -> None:
    rules = [*scratch.declaration()["pinned_only"], {"match": "cert/*.log", "reason": "logs"}]
    scratch.declare(pinned_only=rules)


def _empty_scope_entry(scratch: Scratch) -> None:
    scratch.declare(scope=["README.md", "LICENSE", "cert", "absent"])


def _different_twin(scratch: Scratch) -> None:
    (scratch.root / scratch.earlier / "LICENSE").write_bytes(b"another licence\n")


def _retained_gzip(scratch: Scratch) -> None:
    licence, _, code = scratch.declaration()["pinned_only"]
    scratch.declare(pinned_only=[licence, code])


def _missing_declared_field(scratch: Scratch) -> None:
    declaration: dict[str, object] = {**scratch.declaration()}
    del declaration["license"]
    scratch.write(DECLARATION, declaration)


def _unsafe_directory(scratch: Scratch) -> None:
    scratch.declare(archived_dir="../elsewhere")


@pytest.mark.parametrize(
    ("spoil", "message"),
    [
        (_wrong_commit, "not the declared"),
        (_modified_file, "bytes are not the pinned blob: cert/manifest.json"),
        (_idle_rule, r"pinned_only rule decides no file: cert/\*\.log"),
        (_empty_scope_entry, "scope entry is not in the tree: absent"),
        (_different_twin, "LICENSE is not the bytes of"),
        (_retained_gzip, "can be pinned but not retained: cert/bundle.tar.gz"),
        (_missing_declared_field, "lacks the required field license"),
        (_unsafe_directory, "archived_dir must be one plain directory name"),
    ],
)
def test_acquire_refuses(
    scratch: Scratch, spoil: Callable[[Scratch], None], message: str
) -> None:
    spoil(scratch)
    with pytest.raises(ValueError, match=message):
        acquire(scratch.packet, scratch.checkout, scratch.root)
    assert not (scratch.packet / RECORD).exists()
    assert not (scratch.packet / "source").exists()


def test_a_packet_is_named_for_the_utc_date_of_its_pin(tmp_path: Path) -> None:
    scratch = Scratch(tmp_path)
    misnamed = scratch.packet.with_name("example-source-2026-01-02")
    scratch.packet.rename(misnamed)
    with pytest.raises(ValueError, match="named for the UTC date of its pin, 2026-01-01"):
        acquire(misnamed, scratch.checkout, scratch.root)


def _edit_record(change: Callable[[Any], None]) -> Callable[[Scratch], None]:
    def spoil(scratch: Scratch) -> None:
        record = scratch.record()
        change(record)
        scratch.write(RECORD, record)

    return spoil


def _change_plain_byte(scratch: Scratch) -> None:
    (scratch.packet / "source/cert/manifest.json").write_bytes(b'{"roots": 5}\n')


def _change_compressed_byte(scratch: Scratch) -> None:
    changed = LARGE.replace(b"7 49\n", b"7 50\n", 1)
    (scratch.packet / "source/cert/cover.txt.gz").write_bytes(gzip.compress(changed, mtime=0))


def _drop_retained_file(scratch: Scratch) -> None:
    (scratch.packet / "source/cert/README.md").unlink()


def _add_stray_file(scratch: Scratch) -> None:
    (scratch.packet / "source/cert/extra.md").write_text("not upstream\n")


def _restore_plain_copy(scratch: Scratch) -> None:
    (scratch.packet / "source/cert/cover.txt").write_bytes(LARGE)


def _edit_manifest_digest(scratch: Scratch) -> None:
    listing = scratch.packet / MANIFEST
    old = _sha256(FILES["cert/bundle.tar.gz"])
    listing.write_text(listing.read_text().replace(old, "0" * 64))


def _change_the_named_copy(scratch: Scratch) -> None:
    (scratch.root / scratch.earlier / "code/check.py").write_bytes(b"print('changed')\n")


def _edit_declared_rule(scratch: Scratch) -> None:
    scratch.declare(pinned_only=scratch.declaration()["pinned_only"][:2])


def _drop_readme(scratch: Scratch) -> None:
    (scratch.packet / "README.md").unlink()


def _drop_table_row(scratch: Scratch) -> None:
    readme = scratch.packet / "README.md"
    kept = [line for line in readme.read_text().splitlines() if "cover.txt.gz" not in line]
    readme.write_text("\n".join(kept) + "\n")


def _drop(field: str) -> Callable[[Any], None]:
    def change(record: Any) -> None:
        del record["sources"][0][field]

    return change


def _set(field: str, value: object) -> Callable[[Any], None]:
    def change(record: Any) -> None:
        record["sources"][0][field] = value

    return change


@pytest.mark.parametrize(
    ("spoil", "message"),
    [
        (
            _change_plain_byte,
            "cert/manifest.json does not have the digest its manifest records",
        ),
        (_change_compressed_byte, "cert/cover.txt.gz does not have the digest its manifest"),
        (_drop_retained_file, "cert/README.md is in the subtree manifest but neither retained"),
        (_add_stray_file, "cert/extra.md is retained but is not in the subtree manifest"),
        (_restore_plain_copy, "cert/cover.txt is retained twice, plain and compressed"),
        (_edit_manifest_digest, "pinned-only cert/bundle.tar.gz does not have its manifest"),
        (_change_the_named_copy, "pinned-only cert/code/check.py is not the bytes of"),
        (_edit_declared_rule, "rules no longer decide cert/code/check.py as recorded"),
        (_drop_readme, "the packet has no README.md"),
        (_drop_table_row, "cover.txt.gz is not in the table"),
        (_edit_record(_drop("license")), "sources[0] lacks the required field license"),
        (_edit_record(_drop("source_commit")), "lacks the required field source_commit"),
        (_edit_record(_drop("pinned_only")), "lacks the required field pinned_only"),
        (
            _edit_record(lambda record: record.pop("retrieved_at_utc")),
            "sources.json lacks the required field retrieved_at_utc",
        ),
        (
            _edit_record(lambda record: record["sources"][0]["pinned_only"][1].pop("reason")),
            "pinned_only[1] lacks the required field reason",
        ),
        (_edit_record(_set("license", "")), "sources[0].license is empty"),
        (
            _edit_record(_set("retained_file_count", "4")),
            "retained_file_count is not an integer",
        ),
        (
            _edit_record(_set("retained_file_count", 5)),
            "retained_file_count is 5, and the packet",
        ),
        (
            _edit_record(_set("subtree_total_bytes", 1)),
            "subtree_total_bytes is 1, and the packet",
        ),
        (_edit_record(_set("compressed", [])), "compressed is [], and the packet's files give"),
        (_edit_record(_set("source_commit", "main")), "the declaration's source_commit is not"),
        (_edit_record(_set("git_tree", "abc")), "git_tree is malformed"),
        (_edit_record(_set("committed_utc", "2026-01-02T03:04:05Z")), "not named for the UTC"),
        (
            _edit_record(_set("subtree_scope", ["cert"])),
            "LICENSE is in the manifest but outside",
        ),
        (
            _edit_record(_set("archived_path", "packing/resources/web/earlier-packet/code")),
            "archived_path is not a directory of this packet",
        ),
        (
            _edit_record(lambda record: record.update(format="external-source-acquisition-v0")),
            "format is not external-source-acquisition-v1",
        ),
    ],
)
def test_check_names_what_is_wrong(
    scratch: Scratch, spoil: Callable[[Scratch], None], message: str
) -> None:
    scratch.acquire()
    assert scratch.problems() == []
    spoil(scratch)
    problems = scratch.problems()
    assert any(message in problem for problem in problems), problems
    assert all(problem.startswith(f"{NAME}: ") for problem in problems)


def test_the_command_writes_and_checks_a_packet(
    scratch: Scratch, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(acquire_source, "REPO", scratch.root)
    monkeypatch.setattr(acquire_source, "WEB", scratch.root / "packing/resources/web")

    assert acquire_source.main([NAME, "--checkout", str(scratch.checkout)]) == 0
    printed = capsys.readouterr().out.splitlines()
    retained = sum(len(FILES[name]) for name in RETAINED)
    pinned = sum(len(FILES[name]) for name in PINNED)
    assert printed[0].endswith(
        f"retained 4 files, {retained} bytes; pinned only 3 files, {pinned} bytes"
    )
    row = describe(scratch.packet, scratch.packet / "source/cert/cover.txt.gz", "upstream")
    assert printed[1:] == [row.markdown()]

    assert acquire_source.main([NAME, "--check"]) == 1
    assert "the packet has no README.md" in capsys.readouterr().err
    scratch.acquire()
    assert acquire_source.main([NAME, "--check"]) == 0
    assert capsys.readouterr().out == "PACKET_MATCHES_ITS_CONTRACT\n"

    _change_plain_byte(scratch)
    assert acquire_source.main([NAME, "--check"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "PACKET_DIFFERS_FROM_ITS_CONTRACT\n"
    assert "does not have the digest its manifest records" in captured.err

    with pytest.raises(SystemExit):
        acquire_source.main(["../outside", "--check"])


@pytest.mark.parametrize("shape", [Record, Source, PinnedOnly, Declaration, Rule])
def test_the_contract_says_what_every_field_means(shape: type) -> None:
    documented = shape.__doc__ or ""
    assert [name for name in shape.__annotations__ if f"``{name}``" not in documented] == []


def test_the_retained_wand125_packet_matches_its_contract(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert check(acquire_source.WEB / REAL, acquire_source.REPO) == []
    assert acquire_source.main([REAL, "--check"]) == 0
    assert capsys.readouterr().out == "PACKET_MATCHES_ITS_CONTRACT\n"


def test_the_checkers_the_two_covers_pin_are_already_retained() -> None:
    """Each cover's `verify.sh` requires four checker digests; earlier packets hold them."""
    web = acquire_source.WEB
    evand = "square-packing/s12"
    retained = {
        "ZMX2_RS": f"evand-square-packing-2026-09-28/{evand}/verify2/src/bin/zmx2.rs",
        "ZM_MIXED": f"evand-square-packing-2026-09-28/{evand}/search/zm_mixed.py",
        "MIXED_COVER": f"evand-square-packing-2026-09-28/{evand}/search/mixed_cover.py",
        "ZEROMARGIN": f"evand-square-packing-2026-09-26/{evand}/search/zeromargin.py",
    }
    for directory in ("k2m5_n59_L8", "k2m4_n77_L9"):
        script = web / REAL / "square-packing-bounds/certificates" / directory / "verify.sh"
        lines = script.read_text(encoding="utf-8").splitlines()
        assert "UPSTREAM_COMMIT=b91d70b6ed314624c1434b628a9c7bf9a132c743" in lines
        for name, path in retained.items():
            assert f"{name}={_sha256(read_retained_bytes(web / path))}" in lines
