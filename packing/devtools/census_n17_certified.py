"""The n17 census under certified sub-patterns (H-267): what the admitted certificates exclude.

What it counts. On the unique-state cover `ring-3-voronoi-8-tabbed-unique` at cap
1169/250 there are 346,104 closed capacity-one states in 43,593 D4 orbits (H-266). A
sub-pattern proved infeasible excludes every state that contains it in any D4 image. This
tool counts, exactly, the states and orbits that survive every sub-pattern its ledger
*admits*, with the selector's consumer (`select_n17_sub_patterns.consume`), and nothing
else enters that count.

The ledger. A YAML file declares one entry per certified class:

- `name`, and `cells`: the pattern's cell names on the cover.
- `certifier`: `kernel` (the ownership-induction kernel, `check_n17_subpattern`) or
  `branch-and-bound` (the interval branch and bound, `pilot_n17_subpattern_bb`).
- `receipt` and `receipt_sha256`: the certifier's receipt and its digest. A `pending`
  entry may leave both null while its receipt is being produced.
- `certificate`: the saved proof objects, or null where the certifier keeps none.
- `status`: `admitted` or `pending`, and `evidence`: the review document that admits the
  entry, required once it is admitted.
- `verification`, required once admitted: the standing verifier's receipt and its SHA-256
  (`verify_n17_kernel_certificate` or `verify_n17_bb_certificate`, written separately
  from the producers). The ledger's header lists, under `verifiers`, the reviewed digests
  of each verifier; a receipt from any other bytes does not count.

Every path is repository-relative.

The checks. An entry is refused, and no count is reported at all, unless:

- its receipt exists and has the declared digest;
- the receipt states a certified closure: `PASS_SAVED_CLOSED` or `PASS_CERTIFIED_CLOSED`
  from the kernel, on this cover's frame; `certified-infeasible` from the branch and
  bound, on this design, with no control flag and no soundness failure;
- the receipt's cells are the declared cells as a D4 class: their canonical masks agree;
- no D4 image of the pattern lies in the endpoint's state, which must survive;
- a declared certificate exists, and for the kernel holds the seed and node the receipt
  names;
- an admitted entry names review evidence that exists, and no class is declared twice;
- an admitted entry names a saved certificate and a verification receipt that exists, has
  its declared digest, PASSes in full mode, comes from a verifier of the entry's kind
  whose digest the header allows, names the certificate's own digests (the kernel's seed
  and node, the branch and bound's manifest), and checked the declared class.

The report. The certified line counts admitted entries only. Pending entries with a
verified receipt are a separate projection, and pending entries still awaiting a receipt a
third. Each entry's exclusion is given alone, from the full census, and at the margin: for
an admitted entry, the survivors its removal from the ledger would restore; for a pending
one, what it would remove from the certified survivors. Last, every class the float
selector flagged in the given receipts and the ledger does not admit is listed with the
states and orbits it would remove from the certified survivors, and the survivors if all
of them were certified. Those are heuristic projections and never enter the certified
count.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from devtools import select_n17_sub_patterns as selector
from sqpack.yamlio import load_yaml

SCHEMA = "n17-certified-census/v1"
LEDGER_SCHEMA = "n17-certified-sub-patterns/v1"
STATUS = (
    "exact census under admitted sub-pattern certificates; the pending and flagged lines "
    "are projections and never enter the certified count"
)
REPO = Path(__file__).resolve().parents[2]
PILOTS = "packing/campaign/explorations/X048-session-168-pilots"
DEFAULT_LEDGER = f"{PILOTS}/certified-sub-patterns.yaml"
DEFAULT_SELECTOR_RECEIPTS = (
    f"{PILOTS}/receipts/selector-arity7-seed1.json",
    f"{PILOTS}/receipts/selector-arity8-seed1-restricted.json",
)
DESIGN = selector.DEFAULT_DESIGN
CENSUS = {"states": 346104, "orbits": 43593}
CERTIFIERS = ("kernel", "branch-and-bound")
STATUSES = ("admitted", "pending")
KERNEL_CLOSED = ("PASS_SAVED_CLOSED", "PASS_CERTIFIED_CLOSED")
KERNEL_FRAME = f"n17-{DESIGN}"
BB_SCHEMA = "n17-subpattern-bb-pilot/v1"
BB_CERTIFIED = "certified-infeasible"
VERIFICATION_SCHEMA = "n17-certificate-verification/v1"
FIELDS = (
    "name",
    "cells",
    "certifier",
    "receipt",
    "receipt_sha256",
    "certificate",
    "status",
    "evidence",
)
MODULE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

States = NDArray[np.int64]


class RefusedError(ValueError):
    """A ledger entry or its evidence fails a check; the census reports no count."""


@dataclass(frozen=True)
class Cover:
    """The cover's cells and D4 group, the endpoint's state, and every state."""

    geometry: selector.Geometry
    endpoint_state: int
    states: States


@functools.cache
def cover_context() -> Cover:
    geometry = selector.cover_geometry(DESIGN)
    endpoint = selector.endpoint_pose(DESIGN)
    states = selector.all_states(len(geometry.names), selector.TARGET)
    return Cover(geometry, selector.mask_of(endpoint["cells"]), states)


@dataclass(frozen=True)
class Entry:
    """A ledger entry that passed every check."""

    name: str
    mask: int
    status: str
    certifier: str
    record: dict[str, Any]


def class_mask(cover: Cover, names: Any, where: str) -> int:
    """The canonical D4 mask of a list of cell names, refusing anything else."""
    known = cover.geometry.names
    if not isinstance(names, list) or not names:
        raise RefusedError(f"{where}: cells must be a non-empty list of cell names")
    cells: list[int] = []
    for name in names:
        if name not in known:
            raise RefusedError(f"{where}: {name!r} is not a cell of {DESIGN}")
        cells.append(known.index(name))
    if len(set(cells)) != len(cells):
        raise RefusedError(f"{where}: a cell is repeated")
    return selector.canonical(selector.mask_of(cells), cover.geometry.group)


def resolve(root: Path, declared: Any, where: str) -> Path:
    if not isinstance(declared, str) or not declared or Path(declared).is_absolute():
        raise RefusedError(f"{where}: {declared!r} is not a repository-relative path")
    path = root / declared
    if not path.exists():
        raise RefusedError(f"{where}: {declared} does not exist")
    return path


def receipt_cells(
    cover: Cover, entry: dict[str, Any], receipt: dict[str, Any], where: str
) -> Any:
    """The receipt's cells, once its status is checked to be a certified closure."""
    if entry["certifier"] == "kernel":
        status = receipt.get("status")
        if status not in KERNEL_CLOSED:
            raise RefusedError(f"{where}: kernel status {status!r} is not a closure")
        if receipt.get("frame", KERNEL_FRAME) != KERNEL_FRAME:
            raise RefusedError(f"{where}: kernel frame {receipt.get('frame')!r}")
        cells, mask = receipt.get("cells"), receipt.get("mask")
        names = cover.geometry.names
        indices = sorted(names.index(c) for c in cells if c in names) if cells else []
        if mask is not None and indices != sorted(mask):
            raise RefusedError(f"{where}: the receipt's cells and mask disagree")
        return cells
    if receipt.get("schema") != BB_SCHEMA or receipt.get("verdict") != BB_CERTIFIED:
        raise RefusedError(
            f"{where}: branch-and-bound verdict {receipt.get('verdict')!r} is not certified"
        )
    if receipt.get("design") != DESIGN:
        raise RefusedError(f"{where}: branch-and-bound design {receipt.get('design')!r}")
    if receipt.get("control") is not False or "soundness_failure" in receipt:
        raise RefusedError(f"{where}: a control run or a soundness failure certifies nothing")
    return receipt.get("pattern")


def certificate_digests(entry: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    """The digests that name the entry's saved objects, as its producer receipt gives them."""
    if entry["certifier"] == "kernel":
        return {
            "seed_sha256": receipt.get("seed_sha256"),
            "node_sha256": receipt.get("node_sha256"),
        }
    return {"manifest_sha256": receipt.get("certificate_manifest")}


def check_certificate(
    entry: dict[str, Any], receipt: dict[str, Any], root: Path, where: str
) -> dict[str, Any]:
    """The declared certificate directory holds the objects the producer receipt names."""
    saved = resolve(root, entry["certificate"], f"{where}: certificate")
    digests = certificate_digests(entry, receipt)
    if entry["certifier"] == "kernel":
        names = [f"{kind}-{digests[f'{kind}_sha256']}.json.gz" for kind in ("seed", "node")]
    else:
        names = [f"{digests['manifest_sha256']}.json.gz"]
    for name in names:
        if not (saved / name).is_file():
            raise RefusedError(f"{where}: the certificate holds no {name}")
    return digests


def check_verification(
    cover: Cover,
    entry: dict[str, Any],
    context: tuple[Path, dict[str, list[str]], int, dict[str, Any]],
    where: str,
) -> dict[str, Any]:
    """The standing verifier's receipt: full, passing, allowed, and about this certificate."""
    root, allowed, mask, digests = context
    declared = entry.get("verification")
    if not isinstance(declared, dict) or set(declared) != {"receipt", "sha256"}:
        raise RefusedError(f"{where}: verification must name a receipt and its sha256")
    path = resolve(root, declared["receipt"], f"{where}: verification")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != declared["sha256"]:
        raise RefusedError(f"{where}: verification digest {digest} is not the declared one")
    verification = json.loads(path.read_text(encoding="utf-8"))
    certifier = entry["certifier"]
    if not isinstance(verification, dict) or (
        verification.get("schema") != VERIFICATION_SCHEMA
        or verification.get("verifier") != certifier
    ):
        raise RefusedError(f"{where}: not a {certifier} verification receipt")
    if verification.get("status") != "PASS":
        raise RefusedError(f"{where}: the verification did not pass")
    if verification.get("mode") != "full":
        raise RefusedError(f"{where}: the verification is a sample, not a full check")
    if verification.get("verifier_sha256") not in allowed.get(certifier, []):
        raise RefusedError(
            f"{where}: verifier {verification.get('verifier_sha256')} is not on the allowlist"
        )
    checked = verification.get("certificate") or {}
    if any(checked.get(key) != value for key, value in digests.items()):
        raise RefusedError(f"{where}: the verification names a different certificate")
    names = verification.get("cells" if certifier == "kernel" else "pattern")
    if class_mask(cover, names, f"{where}: verification") != mask:
        raise RefusedError(f"{where}: the verification checked another class")
    return {
        "receipt": declared["receipt"],
        "verifier_sha256": verification["verifier_sha256"],
        "mode": "full",
        "status": "PASS",
        "certificate": digests,
    }


def check_entry(
    cover: Cover, entry: Any, root: Path, index: int, allowed: dict[str, list[str]]
) -> Entry:
    """Every check on one ledger entry; refuses on the first that fails."""
    if not isinstance(entry, dict) or not set(FIELDS) <= set(entry) <= {
        *FIELDS,
        "verification",
    }:
        raise RefusedError(
            f"entry {index}: fields must be {', '.join(FIELDS)}, and optionally verification"
        )
    where = f"entry {entry['name']!r}"
    if entry["certifier"] not in CERTIFIERS:
        raise RefusedError(f"{where}: certifier {entry['certifier']!r}")
    if entry["status"] not in STATUSES:
        raise RefusedError(f"{where}: status {entry['status']!r}")
    mask = class_mask(cover, entry["cells"], where)
    group = cover.geometry.group
    if any(image & cover.endpoint_state == image for image in selector.orbit(mask, group)):
        raise RefusedError(f"{where}: the pattern lies in the endpoint's feasible state")
    if entry["status"] == "admitted" or entry["evidence"] is not None:
        _ = resolve(root, entry["evidence"], f"{where}: evidence")
    record: dict[str, Any] = {
        "name": entry["name"],
        "status": entry["status"],
        "certifier": entry["certifier"],
        "cells": list(entry["cells"]),
        "receipt": entry["receipt"],
        "evidence": entry["evidence"],
    }
    if entry["receipt"] is None:
        if entry["status"] == "admitted" or entry["receipt_sha256"] is not None:
            raise RefusedError(f"{where}: only a pending entry may await its receipt")
        if entry.get("verification") is not None:
            raise RefusedError(f"{where}: a verification needs the producer receipt")
        record["verified"] = False
        return Entry(entry["name"], mask, entry["status"], entry["certifier"], record)
    path = resolve(root, entry["receipt"], f"{where}: receipt")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != entry["receipt_sha256"]:
        raise RefusedError(f"{where}: receipt digest {digest} is not the declared one")
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict):
        raise RefusedError(f"{where}: the receipt is not a JSON object")
    certified = class_mask(
        cover, receipt_cells(cover, entry, receipt, where), f"{where}: receipt"
    )
    if certified != mask:
        raise RefusedError(f"{where}: the receipt certifies another class")
    admitted = entry["status"] == "admitted"
    if admitted and entry["certificate"] is None:
        raise RefusedError(f"{where}: an admitted entry names its saved certificate")
    if entry["certificate"] is not None:
        digests = check_certificate(entry, receipt, root, where)
        if admitted or entry.get("verification") is not None:
            context = (root, allowed, mask, digests)
            record["verification"] = check_verification(cover, entry, context, where)
    elif entry.get("verification") is not None:
        raise RefusedError(f"{where}: a verification needs the saved certificate")
    kernel = entry["certifier"] == "kernel"
    record["verified"] = True
    record["receipt_status"] = receipt.get("status") if kernel else receipt.get("verdict")
    record["certifier_sha256"] = receipt.get("tool_sha256" if kernel else "module_sha256")
    return Entry(entry["name"], mask, entry["status"], entry["certifier"], record)


def load_ledger(cover: Cover, ledger: Path, root: Path) -> list[Entry]:
    document = load_yaml(ledger.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema") != LEDGER_SCHEMA:
        raise RefusedError(f"{ledger}: not a {LEDGER_SCHEMA} ledger")
    if document.get("design") != DESIGN:
        raise RefusedError(f"{ledger}: design {document.get('design')!r}, not {DESIGN}")
    raw = document.get("entries") or []
    if not isinstance(raw, list):
        raise RefusedError(f"{ledger}: entries must be a list")
    allowed = document.get("verifiers") or {}
    if not isinstance(allowed, dict) or not all(
        isinstance(digests, list) for digests in allowed.values()
    ):
        raise RefusedError(f"{ledger}: verifiers must map a certifier to a list of digests")
    entries = [
        check_entry(cover, entry, root, index, allowed) for index, entry in enumerate(raw)
    ]
    names = [entry.name for entry in entries]
    if len(set(names)) != len(names):
        raise RefusedError(f"{ledger}: entry names repeat")
    seen: dict[int, str] = {}
    for entry in entries:
        if entry.mask in seen:
            raise RefusedError(f"entries {seen[entry.mask]!r} and {entry.name!r} are one class")
        seen[entry.mask] = entry.name
    return entries


def count(cover: Cover, masks: list[int]) -> dict[str, Any]:
    record = selector.consume(
        len(cover.geometry.names),
        cover.geometry.group,
        masks,
        endpoint_state=cover.endpoint_state,
        states=cover.states,
    )
    return {key: record[key] for key in ("surviving_states", "orbits", "endpoint_survives")}


def removal(cover: Cover, alive: States, mask: int) -> dict[str, int]:
    """States and orbits of `alive` that hold some D4 image of the class."""
    hit = np.zeros(alive.size, dtype=np.bool_)
    for image in selector.orbit(mask, cover.geometry.group):
        hit |= (alive & image) == image
    removed = alive[hit]
    orbits = selector.count_orbits(removed, cover.geometry.group)["orbits"]
    return {"states": int(removed.size), "orbits": orbits}


def flagged_classes(
    cover: Cover, root: Path, receipts: Sequence[str]
) -> dict[int, dict[str, Any]]:
    """Every class the selector flagged in the receipts, with its latest record."""
    flags: dict[int, dict[str, Any]] = {}
    for declared in receipts:
        path = resolve(root, declared, "selector receipt")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("schema") != selector.SCHEMA or receipt.get("design") != DESIGN:
            raise RefusedError(f"{declared}: not a selector receipt on {DESIGN}")
        for flag in receipt["flagged"]:
            mask = selector.canonical(selector.mask_of(flag["indices"]), cover.geometry.group)
            flags[mask] = {
                "cells": flag["cells"],
                "arity": flag["arity"],
                "best_penetration": flag["best_penetration"],
                "selector_receipt": declared,
            }
    return flags


def census(
    ledger: Path,
    *,
    root: Path = REPO,
    selector_receipts: Sequence[str] = DEFAULT_SELECTOR_RECEIPTS,
) -> dict[str, Any]:
    """The certified census, its projections, and every entry's exclusion."""
    clock = time.perf_counter()
    cover = cover_context()
    entries = load_ledger(cover, ledger, root)
    full = count(cover, [])
    if {"states": full["surviving_states"], "orbits": full["orbits"]} != CENSUS:
        raise RefusedError(f"the empty census is {full}, not H-266's {CENSUS}")
    admitted = [entry.mask for entry in entries if entry.status == "admitted"]
    verified = [e.mask for e in entries if e.status == "pending" and e.record["verified"]]
    pending = [entry.mask for entry in entries if entry.status == "pending"]
    certified = count(cover, admitted)
    if not certified["endpoint_survives"]:
        raise RefusedError("the admitted entries exclude the endpoint's state")
    alive = selector.survivors(
        cover.states,
        sorted({i for m in admitted for i in selector.orbit(m, cover.geometry.group)}),
    )
    rows: list[dict[str, Any]] = []
    for entry in entries:
        alone = removal(cover, cover.states, entry.mask)
        if entry.status == "admitted":
            without = count(cover, [m for m in admitted if m != entry.mask])
            margin = {
                "states": without["surviving_states"] - certified["surviving_states"],
                "orbits": without["orbits"] - certified["orbits"],
            }
        else:
            margin = removal(cover, alive, entry.mask)
        rows.append({**entry.record, "alone": alone, "marginal": margin})
    flags = flagged_classes(cover, root, selector_receipts)
    ledger_status = {entry.mask: entry.status for entry in entries}
    remaining = [
        {
            **flags[mask],
            "in_ledger": ledger_status.get(mask),
            "projected_gain": removal(cover, alive, mask),
        }
        for mask in sorted(flags)
        if ledger_status.get(mask) != "admitted"
    ]
    remaining.sort(key=lambda row: (-row["projected_gain"]["states"], row["cells"]))
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "design": DESIGN,
        "ledger": str(ledger.relative_to(root)) if ledger.is_relative_to(root) else str(ledger),
        "ledger_sha256": hashlib.sha256(ledger.read_bytes()).hexdigest(),
        "census": full,
        "entries": rows,
        "certified": {"admitted": len(admitted), **certified},
        "pending_verified_projection": {
            "entries": len(verified),
            **count(cover, admitted + verified),
        },
        "pending_all_projection": {"entries": len(pending), **count(cover, admitted + pending)},
        "flagged_uncertified": {
            "selector_receipts": list(selector_receipts),
            "classes": remaining,
            "all_certified_projection": count(cover, admitted + sorted(flags)),
        },
        "module_sha256": MODULE_SHA256,
        "seconds": round(time.perf_counter() - clock, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--ledger", default=DEFAULT_LEDGER, help="repository-relative")
    _ = parser.add_argument(
        "--selector-receipt",
        action="append",
        default=None,
        help="a selector receipt whose flags are projected (repeatable)",
    )
    _ = parser.add_argument(
        "--root", type=Path, default=REPO, help="what the ledger's paths are relative to"
    )
    _ = parser.add_argument("--output", type=Path, help="write the census here")
    arguments = parser.parse_args(argv)
    root: Path = arguments.root
    receipts = arguments.selector_receipt or list(DEFAULT_SELECTOR_RECEIPTS)
    try:
        record = census(root / arguments.ledger, root=root, selector_receipts=receipts)
    except RefusedError as refusal:
        print(json.dumps({"refused": str(refusal)}))
        return 2
    text = json.dumps(record, indent=1, sort_keys=True)
    if arguments.output is not None:
        _ = arguments.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
