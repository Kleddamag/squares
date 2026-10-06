"""`devtools.capture_web_source`: a deployed site and a Zenodo deposit, read and compared.

Before 2026-10-05 the sessions' egress policy refused `evand.github.io` and `zenodo.org`,
so packets said what they could not read. These pin what the tool records once it can,
with the network replaced: a page compared with a manifest and a checkout, a deposit
refused when its MD5 is not the record's, a GitHub release archive's top directory
removed so its members compare with a packet's manifest, and the retained packets'
receipts read back.
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile
from collections.abc import Mapping
from pathlib import Path

import pytest

from devtools import capture_web_source as capture

ROOT = Path(__file__).resolve().parent.parent
K2 = ROOT / "resources/web/squarepacker-k2-minus-c-2026-10-05"
EVAND = ROOT / "resources/web/evand-square-packing-2026-10-04"


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _server(answers: Mapping[str, bytes]) -> capture.Fetch:
    def get(url: str) -> capture.Response:
        if url not in answers:
            return capture.Response(404, b"", None, None)
        return capture.Response(200, answers[url], "Sun, 04 Oct 2026 20:18:03 GMT", '"e"')

    return get


def _zip(files: Mapping[str, bytes], top: str | None = "owner-repo-abc1234") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        if top is not None:
            bundle.writestr(f"{top}/", b"")
        for name, data in files.items():
            bundle.writestr(f"{top}/{name}" if top else name, data)
    return buffer.getvalue()


def test_pages_compare_with_a_manifest_and_a_checkout(tmp_path: Path) -> None:
    (tmp_path / "site").mkdir()
    (tmp_path / "site/index.html").write_bytes(b"<p>home</p>")
    (tmp_path / "site/problems.html").write_bytes(b"<p>old</p>")
    declaration = {
        "format": capture.DECLARATION_FORMAT,
        "base_url": "https://example.org/atlas/",
        "pages": [
            {"url": "index.html", "upstream": "site/index.html"},
            {"url": "problems.html", "upstream": "site/problems.html"},
            {"url": "gone.html", "upstream": "site/gone.html"},
        ],
    }
    served = {
        "https://example.org/atlas/index.html": b"<p>home</p>",
        "https://example.org/atlas/problems.html": b"<p>new</p>",
    }
    manifest = {"site/index.html": _digest(b"<p>home</p>")}
    receipt = capture.capture_pages(
        declaration, manifest=manifest, checkout=tmp_path, get=_server(served), pause=0
    )
    verdicts = [(row["status"], row["manifest"], row["checkout"]) for row in receipt["pages"]]
    assert verdicts == [
        (200, "same", "same"),
        (200, "absent", "differs"),
        (404, "absent", "absent"),
    ]
    assert receipt["summary"]["status_200"] == 2
    assert receipt["summary"]["checkout"] == {"same": 1, "differs": 1, "absent": 1}


def test_a_declaration_without_upstream_paths_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "pages.json"
    path.write_text(
        json.dumps(
            {
                "format": capture.DECLARATION_FORMAT,
                "base_url": "https://example.org/",
                "pages": [{"url": "a.html"}],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(capture.CaptureError, match="upstream"):
        capture.load_declaration(path)


def _deposit(archive: bytes, *, checksum: str | None = None) -> dict[str, bytes]:
    md5 = hashlib.md5(archive, usedforsecurity=False).hexdigest()
    entry = {
        "key": "owner/repo-v1.0.zip",
        "size": len(archive),
        "checksum": checksum or f"md5:{md5}",
        "links": {"self": "https://zenodo.org/api/records/7/files/repo-v1.0.zip/content"},
    }
    record = {
        "id": 7,
        "doi": "10.5281/zenodo.7",
        "conceptdoi": "10.5281/zenodo.6",
        "created": "2026-10-05T14:07:11+00:00",
        "updated": "2026-10-05T14:07:11+00:00",
        "metadata": {"title": "A preprint", "version": "1.0", "publication_date": "2026-10-05"},
        "files": [entry],
    }
    return {
        "https://zenodo.org/api/records/7": json.dumps(record).encode(),
        "https://zenodo.org/api/records/7/files": json.dumps({"entries": [entry]}).encode(),
        str(entry["links"]["self"]): archive,
    }


def test_a_deposit_is_written_with_its_digests_and_compared(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(capture, "FETCH_PAUSE_SECONDS", 0)
    archive = _zip({"paper/paper.pdf": b"%PDF v1.0", "code/run.py": b"print(1)\n"})
    packet = {
        "paper/paper.pdf": _digest(b"%PDF v1.1"),
        "code/run.py": _digest(b"print(1)\n"),
        "code/new.py": _digest(b""),
    }
    out = tmp_path / "zenodo"
    receipt = capture.capture_zenodo(
        "7",
        out=out,
        extract=["paper/paper.pdf"],
        comparisons=[("packet", packet)],
        get=_server(_deposit(archive)),
    )
    (row,) = receipt["files"]
    assert row["top_directory"] == "owner-repo-abc1234"
    assert row["members"] == 2
    assert row["sha256"] == _digest(archive)
    assert (out / "zenodo-7/paper/paper.pdf").read_bytes() == b"%PDF v1.0"
    assert (out / "zenodo-7.sha256").read_text(encoding="utf-8").splitlines() == [
        f"{_digest(b'print(1)' + bytes([10]))}  ./code/run.py",
        f"{_digest(b'%PDF v1.0')}  ./paper/paper.pdf",
    ]
    (comparison,) = receipt["comparisons"]
    assert comparison["same"] == 1
    assert comparison["differs"] == ["paper/paper.pdf"]
    assert comparison["only_in_manifest"] == ["code/new.py"]
    assert json.loads((out / "zenodo-7-receipt.json").read_text(encoding="utf-8")) == receipt
    assert not list(out.glob("*.zip"))


def test_a_deposit_whose_md5_is_not_the_records_is_refused(tmp_path: Path) -> None:
    archive = _zip({"a.txt": b"a"})
    with pytest.raises(capture.CaptureError, match="MD5"):
        capture.capture_zenodo(
            "7", out=tmp_path, get=_server(_deposit(archive, checksum="md5:" + "0" * 32))
        )


def test_an_archive_without_one_top_directory_keeps_its_paths() -> None:
    top, members = capture.archive_members(_zip({"a.txt": b"a", "b/c.txt": b"c"}, top=None))
    assert top is None
    assert sorted(members) == ["a.txt", "b/c.txt"]


def test_the_retained_v1_0_deposit_is_the_v1_0_tag_and_differs_from_the_pin_as_recorded() -> (
    None
):
    receipt = json.loads(
        (K2 / "zenodo/zenodo-23164302-receipt.json").read_text(encoding="utf-8")
    )
    (row,) = receipt["files"]
    assert row["md5"] == row["checksum_stated"].removeprefix("md5:")
    listing = capture.read_manifest(K2 / "zenodo/zenodo-23164302.sha256")
    assert len(listing) == row["members"] == 55
    paper = (K2 / "zenodo/zenodo-23164302/paper/paper.pdf").read_bytes()
    assert _digest(paper) == listing["paper/paper.pdf"]
    pin = capture.read_manifest(K2 / "acquisition/upstream-subtree.sha256")
    assert capture.compare_manifests(listing, pin)["differs"] == [
        ".zenodo.json",
        "README.md",
        "SHA256SUMS",
        "paper/paper.pdf",
        "paper/paper.tex",
        "reviews/REVIEWS.md",
    ]
    tag = next(c for c in receipt["comparisons"] if "tag v1.0" in c["against"])
    assert (tag["same"], tag["differs"], tag["only_in_archive"]) == (55, [], [])


def test_the_retained_v1_1_deposit_differs_from_the_pin_only_in_its_doi_line() -> None:
    listing = capture.read_manifest(K2 / "zenodo/zenodo-23165736.sha256")
    pin = capture.read_manifest(K2 / "acquisition/upstream-subtree.sha256")
    compared = capture.compare_manifests(listing, pin)
    assert (compared["differs"], compared["only_in_archive"], compared["only_in_manifest"]) == (
        ["README.md"],
        [],
        [],
    )


def test_the_deployed_atlas_was_the_pinned_build() -> None:
    receipt = json.loads(
        (EVAND / "receipts/deployed-site-2026-10-05.json").read_text(encoding="utf-8")
    )
    pin = capture.read_manifest(EVAND / "acquisition/upstream-subtree.sha256")
    for row in receipt["pages"]:
        assert row["status"] == 200
        assert row["checkout"] == "same"
        if row["upstream"] in pin:
            assert row["sha256"] == pin[row["upstream"]]
    parses = {
        row["upstream"].rsplit("/", 1)[-1]: row["sha256"]
        for row in receipt["pages"]
        if "/data/p/" in row["upstream"]
    }
    for n in (69, 83, 87):
        witness = (ROOT / f"witnesses/known-best/n-{n:03d}.yaml").read_text(encoding="utf-8")
        assert f"revision_sha256: {parses[f'square-{n}.json']}" in witness


def test_a_deposited_file_that_is_no_archive_is_matched_whole(tmp_path: Path) -> None:
    served = _deposit(b"%PDF v1.1")
    record = json.loads(served["https://zenodo.org/api/records/7"])
    record["files"][0]["key"] = "paper.pdf"
    served["https://zenodo.org/api/records/7"] = json.dumps(record).encode()
    packet = {"paper/paper.pdf": _digest(b"%PDF v1.1"), "code/run.py": _digest(b"")}
    receipt = capture.capture_zenodo(
        "7", out=tmp_path, comparisons=[("packet", packet)], get=_server(served)
    )
    (row,) = receipt["files"]
    assert row["same_bytes_as"] == {"packet": ["paper/paper.pdf"]}
    assert "comparisons" not in receipt
