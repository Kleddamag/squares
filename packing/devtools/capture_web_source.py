#!/usr/bin/env python3
"""Fetch a web source the record cites, and compare what it serves with what is retained.

Most sources reach this record through Git, and `devtools.acquire_source` retains them.
Two kinds arrive over plain HTTPS instead, and before 2026-10-05 the agent sessions'
egress policy refused both hosts, so several packets say a source "was not fetched":

- **A deployed site.** GitHub Pages serves a build of a repository, and a packet retains
  the repository at a pinned commit. Whether the pages a reader sees are those files is
  a question only a fetch of the site answers.
- **A Zenodo deposit.** A DOI names a record whose files Zenodo checksums. An issue may
  cite the DOI of one version while the packet pins the repository at another.

This tool fetches either, records what was served, and says how it compares. It decides
nothing about what the source claims.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`::

    python -m devtools.capture_web_source pages DECLARATION \\
        [--compare-manifest FILE] [--compare-dir DIR] [--receipt PATH]
    python -m devtools.capture_web_source zenodo RECORD --out DIR \\
        [--extract MEMBER ...] [--compare-manifest FILE]

**`pages`** reads DECLARATION, a JSON object with `format` `web-pages-declaration-v1`, a
`base_url`, and `pages`: a list of `{"url": ..., "upstream": ...}`, each page's address
relative to the base and the source file a build copies to it. It fetches every page in
order, one at a time with a pause, and records each one's status, size, SHA-256,
`Last-Modified` and `ETag`. `--compare-manifest` compares each page with its upstream
path's digest in a `sha256sum`-style list of `./`-relative paths, the form
`devtools.acquire_source` writes; `--compare-dir` compares it with the file at its
upstream path under a directory, such as a checkout at the pinned commit. The receipt
says, page by page, `same`, `differs` or `absent` for each comparison asked for. Nothing
fetched is written.

**`zenodo`** reads one record from Zenodo's REST API, `/api/records/RECORD` and its
`/files` listing, downloads every file into memory, and refuses one whose size or MD5 is
not the record's. It writes into `--out`, in Zenodo's own bytes where Zenodo wrote them:

- `zenodo-RECORD.json` and `zenodo-RECORD-files.json`, the record and its files listing
  as served;
- `zenodo-RECORD.sha256`, for each zip archive, the SHA-256 of every member with the
  archive's single top directory removed, in `sha256sum` form, so it compares line for
  line with a packet's manifest; a file that is not an archive is compared whole, by
  the paths in each manifest that hold the same bytes;
- each `--extract` member, at its archive path under `zenodo-RECORD/`; and
- `zenodo-RECORD-receipt.json`: the record's identity, each file's stated and computed
  digests, the members, and the comparison with `--compare-manifest`.

The archive itself is not written. It is pinned by the MD5 Zenodo states and the SHA-256
computed here (`OR-18`), and a later reader re-fetches it from the DOI.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import time
import urllib.request
import zipfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, cast

from strif import atomic_output_file

from sqpack import retained_json

REPO = Path(__file__).resolve().parents[2]
#: Names this repository to the servers it reads, as the catalogue tools do.
USER_AGENT = "sqpack-source-capture/1 (+https://github.com/jlevy/squares)"
DECLARATION_FORMAT = "web-pages-declaration-v1"
PAGES_FORMAT = "web-pages-capture-v1"
ZENODO_FORMAT = "zenodo-capture-v1"
ZENODO_API = "https://zenodo.org/api/records"
FETCH_TIMEOUT_SECONDS = 60
#: One page at a time, with this pause after each: these are people's own sites.
FETCH_PAUSE_SECONDS = 0.3


@dataclass(frozen=True)
class Response:
    """What one fetch returned: the final status, the body and the headers this tool keeps."""

    status: int
    body: bytes
    last_modified: str | None
    etag: str | None


Fetch = Callable[[str], Response]


class CaptureError(RuntimeError):
    """A source served something this tool will not record as the source."""


def fetch(url: str) -> Response:
    """GET one address, following redirects, through the environment's proxy."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
        return Response(
            status=response.status,
            body=response.read(),
            last_modified=response.headers.get("Last-Modified"),
            etag=response.headers.get("ETag"),
        )


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_manifest(path: Path) -> dict[str, str]:
    """A `sha256sum`-style list of `./`-relative paths, as path to digest."""
    digests: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        if len(digest) != 64 or not name:
            message = f"{path}: not a sha256sum line: {line!r}"
            raise CaptureError(message)
        digests[name.removeprefix("./")] = digest
    return digests


def _verdict(digest: str, expected: str | None) -> str:
    if expected is None:
        return "absent"
    return "same" if digest == expected else "differs"


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def write_json(path: Path, document: object) -> None:
    _write_bytes(path, retained_json.dumps(document, ensure_ascii=False).encode("utf-8"))


# --------------------------------------------------------------------------- pages


def load_declaration(path: Path) -> dict[str, Any]:
    """The pages to fetch, refused unless every page names its address and its source."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        message = f"{path}: not a JSON object"
        raise CaptureError(message)
    declaration = cast("dict[str, Any]", document)
    if declaration.get("format") != DECLARATION_FORMAT:
        message = f"{path}: format is not {DECLARATION_FORMAT}"
        raise CaptureError(message)
    base = declaration.get("base_url")
    pages = declaration.get("pages")
    if not isinstance(base, str) or not base.endswith("/") or not isinstance(pages, list):
        message = f"{path}: needs a base_url ending in '/' and a list of pages"
        raise CaptureError(message)
    for page in cast("list[object]", pages):
        entry = cast("dict[str, object]", page) if isinstance(page, dict) else {}
        if not isinstance(entry.get("url"), str) or not isinstance(entry.get("upstream"), str):
            message = f"{path}: every page needs a url and an upstream path: {page!r}"
            raise CaptureError(message)
    return declaration


def capture_pages(
    declaration: Mapping[str, Any],
    *,
    manifest: Mapping[str, str] | None = None,
    checkout: Path | None = None,
    get: Fetch = fetch,
    pause: float = FETCH_PAUSE_SECONDS,
) -> dict[str, Any]:
    """Fetch every declared page and compare it as asked; the receipt, as a document."""
    retrieved = now_utc()
    base = str(declaration["base_url"])
    rows: list[dict[str, Any]] = []
    for page in declaration["pages"]:
        url = base + str(page["url"])
        upstream = str(page["upstream"])
        response = get(url)
        digest = sha256(response.body)
        row: dict[str, Any] = {
            "url": url,
            "upstream": upstream,
            "status": response.status,
            "bytes": len(response.body),
            "sha256": digest,
            "last_modified": response.last_modified,
            "etag": response.etag,
        }
        if manifest is not None:
            row["manifest"] = _verdict(digest, manifest.get(upstream))
        if checkout is not None:
            source = checkout / upstream
            row["checkout"] = _verdict(
                digest, sha256(source.read_bytes()) if source.is_file() else None
            )
        rows.append(row)
        time.sleep(pause)
    summary: dict[str, Any] = {
        "pages": len(rows),
        "status_200": sum(r["status"] == 200 for r in rows),
    }
    for comparison in ("manifest", "checkout"):
        verdicts = [row[comparison] for row in rows if comparison in row]
        if verdicts:
            summary[comparison] = {v: verdicts.count(v) for v in ("same", "differs", "absent")}
    return {
        "format": PAGES_FORMAT,
        "base_url": base,
        "retrieved_utc": retrieved,
        "summary": summary,
        "pages": rows,
    }


# --------------------------------------------------------------------------- zenodo


def archive_members(data: bytes) -> tuple[str | None, dict[str, bytes]]:
    """A zip's files by path, with its single top directory removed when it has one.

    GitHub's release archives, which Zenodo's GitHub integration deposits, hold the tree
    under one directory named for the repository and commit; removing it makes the paths
    the tree's own, as a packet's manifest gives them.
    """
    with zipfile.ZipFile(io.BytesIO(data)) as bundle:
        files = {
            info.filename: bundle.read(info) for info in bundle.infolist() if not info.is_dir()
        }
    tops = {PurePosixPath(name).parts[0] for name in files}
    if len(tops) == 1 and all(len(PurePosixPath(name).parts) > 1 for name in files):
        (top,) = tops
        return top, {name.removeprefix(top + "/"): body for name, body in files.items()}
    return None, files


def directory_manifest(root: Path) -> dict[str, str]:
    """Every file under `root` by its relative path, as a manifest, Git's own files aside."""
    return {
        path.relative_to(root).as_posix(): sha256(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def manifest_text(members: Mapping[str, bytes]) -> str:
    return "".join(f"{sha256(members[name])}  ./{name}\n" for name in sorted(members))


def compare_manifests(ours: Mapping[str, str], theirs: Mapping[str, str]) -> dict[str, Any]:
    """Member by member: the same digest, a different one, or present on one side only."""
    shared = sorted(set(ours) & set(theirs))
    return {
        "same": sum(ours[name] == theirs[name] for name in shared),
        "differs": [name for name in shared if ours[name] != theirs[name]],
        "only_in_archive": sorted(set(ours) - set(theirs)),
        "only_in_manifest": sorted(set(theirs) - set(ours)),
    }


def _json_body(response: Response, url: str) -> dict[str, Any]:
    if response.status != 200:
        message = f"{url} answered {response.status}"
        raise CaptureError(message)
    document = json.loads(response.body)
    if not isinstance(document, dict):
        message = f"{url} did not answer with a JSON object"
        raise CaptureError(message)
    return cast("dict[str, Any]", document)


def _checked_file(entry: Mapping[str, Any], get: Fetch) -> tuple[bytes, str]:
    """One deposited file, refused unless its size and MD5 are the record's."""
    url = str(entry["links"]["self"])
    response = get(url)
    stated = str(entry["checksum"])
    algorithm, _, expected = stated.partition(":")
    md5 = hashlib.md5(response.body, usedforsecurity=False).hexdigest()
    if response.status != 200 or algorithm != "md5" or md5 != expected:
        message = f"{url}: status {response.status}, MD5 {md5}, the record states {stated}"
        raise CaptureError(message)
    if len(response.body) != int(entry["size"]):
        message = f"{url}: {len(response.body)} bytes, the record states {entry['size']}"
        raise CaptureError(message)
    return response.body, md5


def capture_zenodo(
    record_id: str,
    *,
    out: Path,
    extract: Sequence[str] = (),
    comparisons: Sequence[tuple[str, Mapping[str, str]]] = (),
    get: Fetch = fetch,
) -> dict[str, Any]:
    """Fetch one record and its files, write what `zenodo` writes, return the receipt."""
    retrieved = now_utc()
    record_url = f"{ZENODO_API}/{record_id}"
    record_response = get(record_url)
    record = _json_body(record_response, record_url)
    files_response = get(f"{record_url}/files")
    _json_body(files_response, f"{record_url}/files")
    stem = f"zenodo-{record_id}"
    _write_bytes(out / f"{stem}.json", record_response.body)
    _write_bytes(out / f"{stem}-files.json", files_response.body)
    metadata = cast("dict[str, Any]", record.get("metadata") or {})
    files: list[dict[str, Any]] = []
    extracted: list[dict[str, Any]] = []
    compared: list[dict[str, Any]] = []
    wanted = set(extract)
    for entry in cast("list[dict[str, Any]]", record.get("files") or []):
        body, md5 = _checked_file(entry, get)
        row: dict[str, Any] = {
            "key": entry["key"],
            "bytes": len(body),
            "checksum_stated": entry["checksum"],
            "md5": md5,
            "sha256": sha256(body),
        }
        if str(entry["key"]).endswith(".zip"):
            top, members = archive_members(body)
            listing = manifest_text(members)
            _write_bytes(out / f"{stem}.sha256", listing.encode("utf-8"))
            row |= {
                "top_directory": top,
                "members": len(members),
                "member_bytes": sum(len(member) for member in members.values()),
                "member_manifest": f"{stem}.sha256",
            }
            for name in sorted(wanted & set(members)):
                target = out / stem / name
                _write_bytes(target, members[name])
                extracted.append(
                    {
                        "member": name,
                        "path": f"{stem}/{name}",
                        "bytes": len(members[name]),
                        "sha256": sha256(members[name]),
                    }
                )
            wanted -= set(members)
            ours = {name: sha256(data) for name, data in members.items()}
            compared.extend(
                {"archive": entry["key"], "against": label} | compare_manifests(ours, theirs)
                for label, theirs in comparisons
            )
        else:
            digest = row["sha256"]
            row["same_bytes_as"] = {
                label: sorted(name for name, other in theirs.items() if other == digest)
                for label, theirs in comparisons
            }
        files.append(row)
        time.sleep(FETCH_PAUSE_SECONDS)
    if wanted:
        message = f"record {record_id} holds no member {sorted(wanted)}"
        raise CaptureError(message)
    receipt: dict[str, Any] = {
        "format": ZENODO_FORMAT,
        "record": record.get("id"),
        "doi": record.get("doi"),
        "conceptdoi": record.get("conceptdoi"),
        "title": metadata.get("title"),
        "version": metadata.get("version"),
        "publication_date": metadata.get("publication_date"),
        "created": record.get("created"),
        "updated": record.get("updated"),
        "api": record_url,
        "retrieved_utc": retrieved,
        "files": files,
        "extracted": extracted,
    }
    if compared:
        receipt["comparisons"] = compared
    write_json(out / f"{stem}-receipt.json", receipt)
    return receipt


# --------------------------------------------------------------------------- the command


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = command.add_subparsers(dest="kind", required=True)
    pages = sub.add_parser("pages", help="fetch a declared list of pages and compare them")
    pages.add_argument("declaration", type=Path)
    pages.add_argument(
        "--compare-manifest", type=Path, help="a sha256sum list of upstream paths"
    )
    pages.add_argument(
        "--compare-dir", type=Path, help="a directory holding the upstream files"
    )
    pages.add_argument("--receipt", type=Path, help="write the receipt here")
    zenodo = sub.add_parser("zenodo", help="fetch one Zenodo record, its files and digests")
    zenodo.add_argument("record", help="the record id, as in 10.5281/zenodo.RECORD")
    zenodo.add_argument("--out", type=Path, required=True, help="where the record is written")
    zenodo.add_argument(
        "--extract", action="append", default=[], help="an archive member to keep; repeatable"
    )
    zenodo.add_argument(
        "--compare-manifest",
        type=Path,
        action="append",
        default=[],
        help="compare each archive with this sha256sum list; repeatable",
    )
    zenodo.add_argument(
        "--compare-dir",
        action="append",
        default=[],
        metavar="LABEL=DIR",
        help="compare each archive with the files under DIR, named LABEL; repeatable",
    )
    return command


def _shown(path: Path) -> str:
    """A path as the record writes one: from the repository root where it is inside it."""
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


def _report_pages(receipt: Mapping[str, Any]) -> None:
    for row in receipt["pages"]:
        compared = ", ".join(
            f"{name} {row[name]}" for name in ("manifest", "checkout") if name in row
        )
        print(
            f"  {row['status']} {row['bytes']:>8} {row['sha256'][:12]} {row['url']}  {compared}"
        )
    print(json.dumps(receipt["summary"]))


def _report_zenodo(receipt: Mapping[str, Any]) -> None:
    print(f"record {receipt['record']} {receipt['doi']} version {receipt['version']}")
    for row in receipt["files"]:
        print(
            f"  {row['key']}: {row['bytes']} bytes, MD5 {row['md5']}, SHA-256 {row['sha256']}"
        )
        if "members" in row:
            print(f"    {row['members']} members, {row['member_bytes']} bytes unpacked")
        for label, paths in row.get("same_bytes_as", {}).items():
            print(f"    the same bytes as {paths or 'nothing'} in {label}")
    for row in receipt["extracted"]:
        print(f"  kept {row['path']}: {row['bytes']} bytes, SHA-256 {row['sha256']}")
    for comparison in receipt.get("comparisons", ()):
        print(
            f"  {comparison['archive']} against {comparison['against']}: "
            f"{comparison['same']} same, differs {comparison['differs']}, only in the "
            f"archive {comparison['only_in_archive']}, only in the other "
            f"{comparison['only_in_manifest']}"
        )


def _zenodo_comparisons(
    manifests: Sequence[Path], directories: Sequence[str]
) -> list[tuple[str, dict[str, str]]]:
    """The `--compare-manifest` and `--compare-dir` arguments, read."""
    comparisons = [(_shown(path), read_manifest(path)) for path in manifests]
    for argument in directories:
        label, separator, directory = argument.partition("=")
        if not separator or not label or not Path(directory).is_dir():
            message = f"--compare-dir takes LABEL=DIR with DIR a directory: {argument!r}"
            raise CaptureError(message)
        comparisons.append((label, directory_manifest(Path(directory))))
    return comparisons


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.kind == "pages":
            manifest = (
                None if args.compare_manifest is None else read_manifest(args.compare_manifest)
            )
            receipt = capture_pages(
                load_declaration(args.declaration), manifest=manifest, checkout=args.compare_dir
            )
            if args.receipt is not None:
                write_json(args.receipt, receipt)
            _report_pages(receipt)
            return 0 if receipt["summary"]["status_200"] == receipt["summary"]["pages"] else 1
        receipt = capture_zenodo(
            args.record,
            out=args.out,
            extract=args.extract,
            comparisons=_zenodo_comparisons(args.compare_manifest, args.compare_dir),
        )
    except (CaptureError, OSError, ValueError) as error:
        print(f"capture failed: {error}", file=sys.stderr)
        return 1
    _report_zenodo(receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
