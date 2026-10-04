"""Lazy raw-piece row supports, diagnostic only; never a geometric feasibility claim.

Each retained selection is a full solution of the frozen binary graph: its edges
mean only that universal collision was not proved. AC/PC preserve full solutions,
so a selection touching a row prevents deletion of that entire row in this graph.
The fresh --verify path reconstructs atoms and checks every edge without DFS/cache.
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from devtools.check_hull_kernel_mask0 import n17_unique_frame
from devtools.check_n17_subpattern import content_sha256, saved_files
from devtools.pilot_n17_capture import endpoint_holds, load_endpoint
from devtools.probe_n17_residual_graph import Atom, atomize, bounded_load, incompatible
from devtools.profile_n17_partner_memo import peak_memory_bytes
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, area2, require
from sqpack.hull_kernel.induction import encode

MAX_ATOMS = 4096
MAX_ROWS = 128
MAX_PAIRS = 50_000
MAX_NODES = 100_000
MAX_PEAK_BYTES = 512 * 1024 * 1024
MAX_PACKET_BYTES = 4 * 1024 * 1024
PREDICATE = "sorted-owner-universal-collision-v1"
SCHEMA = "n17.raw-row-support.v1"
type RowKey = tuple[int, int]
type Predicate = Callable[[Atom, Atom, Budget], bool]


def remaining(budget: Budget) -> None:
    if time.monotonic() >= budget.deadline:
        raise IncompleteError("raw row support wall ceiling")
    if peak_memory_bytes() > MAX_PEAK_BYTES:
        raise IncompleteError("actual worker peak exceeds 512 MiB")


def bounded_json(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        raw = stream.read(MAX_PACKET_BYTES + 1)
    require(len(raw) <= MAX_PACKET_BYTES, "packet/receipt exceeds 4 MiB")
    value = json.loads(raw)
    require(isinstance(value, dict), "packet/receipt must be a JSON object")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def checked_inputs(
    directory: Path, receipt_path: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    seed_path, node_path = saved_files(directory)
    seed, document = bounded_load(seed_path), bounded_load(node_path)
    receipt = bounded_json(receipt_path)
    require(receipt["status"] == "PASS_SAVED_STALL", "requires cold saved stalled receipt")
    require(receipt["seed_sha256"] == content_sha256(seed), "seed receipt differs")
    require(receipt["node_sha256"] == content_sha256(document), "node receipt differs")
    require(seed["mask"] == document["mask"] == document["final_state"]["mask"], "mask differs")
    return document, {
        "seed_sha256": receipt["seed_sha256"],
        "node_sha256": receipt["node_sha256"],
        "cold_receipt_sha256": content_sha256(receipt),
    }


def raw_atoms(frame: Frame, document: dict[str, Any]) -> list[Atom]:
    require(
        document["U"] == str(frame.cap) and document["B"] == str(frame.scale), "frame differs"
    )
    cells = document["final_state"]["cells"]
    owners = sorted(int(owner) for owner in cells)
    require(
        0 < len(owners) <= 6 and owners == sorted(document["mask"]), "owner inventory differs"
    )
    require(all(str(owner) in cells for owner in owners), "noncanonical owner key")
    for owner in owners:
        for row in cells[str(owner)]:
            if not row["residual_polygons"]:
                continue
            reference = row["reference"]
            require(reference["kind"] == "phase3", "unprocessed row")
            step_index, row_index = reference["step"], reference["row"]
            require(type(step_index) is int and step_index >= 0, "invalid source step")
            require(type(row_index) is int and row_index >= 0, "invalid source row")
            source = document["steps"][step_index]["rows"][row_index]
            require(source["reference"] == reference, "source reference differs")
            require(
                source["residual_polygons"] == row["residual_polygons"],
                "source residual differs",
            )
            require(
                source["outer_domain"] == row["outer_domain"], "source outer domain differs"
            )
    grouped = atomize(frame, document, "pieces")  # Rechecks every accepted strict core.
    require(all(grouped[owner] for owner in owners), "stalled input has empty owner domain")
    atoms = [atom for owner in owners for atom in grouped[owner]]
    require(len(atoms) <= MAX_ATOMS, "raw atom inventory ceiling")
    require(len({(a.owner, a.row) for a in atoms}) <= MAX_ROWS, "row inventory ceiling")
    return atoms


@dataclass
class LazySupports:
    atoms: list[Atom]
    budget: Budget
    predicate: Predicate = incompatible
    max_pairs: int = MAX_PAIRS
    max_nodes: int = MAX_NODES
    cache: dict[tuple[int, int], bool] = field(default_factory=dict)
    selections: list[list[int]] = field(default_factory=list)
    supported: dict[RowKey, int] = field(default_factory=dict)
    unsupported: list[RowKey] = field(default_factory=list)
    nodes: int = 0
    pair_tests: int = 0

    def compatible(self, left: int, right: int) -> bool:
        a, b = self.atoms[left], self.atoms[right]
        require(a.owner != b.owner, "same-owner pair")
        if a.owner > b.owner:
            left, right = right, left
        key = left, right
        if key not in self.cache:
            remaining(self.budget)
            if self.pair_tests >= self.max_pairs:
                raise IncompleteError("unique exact pair ceiling")
            self.pair_tests += 1
            # A timeout/refusal propagates; it must never become a compatible cache entry.
            self.cache[key] = not self.predicate(
                self.atoms[left], self.atoms[right], self.budget
            )
        return self.cache[key]

    def keep(self, selection: list[int]) -> None:
        index = len(self.selections)
        self.selections.append(selection)
        for value in selection:
            atom = self.atoms[value]
            self.supported.setdefault((atom.owner, atom.row), index)

    def snapshot(self, status: str, reason: str | None = None) -> dict[str, Any]:
        return {
            "status": status,
            "reason": reason,
            "search_nodes": self.nodes,
            "unique_pair_tests": self.pair_tests,
            "cache_entries": len(self.cache),
            "selections": self.selections,
            "row_support": [
                {"owner": owner, "row": row, "selection_index": index}
                for (owner, row), index in sorted(self.supported.items())
            ],
            "exhaustive_unsupported_rows": [list(row) for row in self.unsupported],
            "unsupported_rows_independently_verified": False,
        }

    def run(
        self,
        *,
        checkpoint: Callable[[dict[str, Any]], None] | None = None,
        initial_selection: list[int] | None = None,
    ) -> dict[str, Any]:
        owners = sorted({atom.owner for atom in self.atoms})
        choices = {
            owner: sorted(
                (i for i, atom in enumerate(self.atoms) if atom.owner == owner),
                key=lambda i: (
                    -area2(self.atoms[i].domain),
                    self.atoms[i].row,
                    self.atoms[i].pieces[0],
                ),
            )
            for owner in owners
        }
        rows = sorted({(atom.owner, atom.row) for atom in self.atoms})

        def search(order: list[int], selected: list[int], forced: RowKey) -> list[int] | None:
            remaining(self.budget)
            if self.nodes >= self.max_nodes:
                raise IncompleteError("DFS node ceiling")
            self.nodes += 1
            if not order:
                return sorted(selected, key=lambda i: self.atoms[i].owner)
            owner = order[0]
            for candidate in choices[owner]:
                if owner == forced[0] and self.atoms[candidate].row != forced[1]:
                    continue
                if all(self.compatible(candidate, other) for other in selected):
                    found = search(order[1:], [*selected, candidate], forced)
                    if found is not None:
                        return found
            return None

        try:
            if initial_selection is not None:
                require(
                    [self.atoms[i].owner for i in initial_selection] == owners,
                    "initial selection owners",
                )
                require(
                    all(
                        self.compatible(a, b)
                        for pos, a in enumerate(initial_selection)
                        for b in initial_selection[pos + 1 :]
                    ),
                    "endpoint selection collision",
                )
                self.keep(initial_selection)
            for forced in rows:
                if forced in self.supported:
                    continue
                order = [forced[0], *(owner for owner in owners if owner != forced[0])]
                selection = search(order, [], forced)
                if selection is None:
                    self.unsupported.append(forced)
                else:
                    self.keep(selection)
                if checkpoint is not None:
                    checkpoint(self.snapshot("RUNNING"))
        except IncompleteError as error:
            return self.snapshot("INCOMPLETE", str(error))
        status = "EXHAUSTIVE_UNSUPPORTED_ROWS" if self.unsupported else "ALL_ROWS_SUPPORTED"
        return self.snapshot(status)


def atom_reference(atom: Atom, document: dict[str, Any]) -> dict[str, Any]:
    row = document["final_state"]["cells"][str(atom.owner)][atom.row]
    return {
        "owner": atom.owner,
        "row": atom.row,
        "piece": atom.pieces[0],
        "source_reference": row["reference"],
        "interval": row["interval"],
        "domain_sha256": content_sha256(encode(atom.domain)),
        "core_sha256": content_sha256(encode(atom.core)),
    }


def packet(
    result: dict[str, Any],
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
) -> dict[str, Any]:
    return {
        **result,
        "schema": SCHEMA,
        "predicate": PREDICATE,
        "input_identity": identity,
        "diagnostic_only": True,
        "new_exclusions": 0,
        "raw_atoms": len(atoms),
        "live_rows": len({(a.owner, a.row) for a in atoms}),
        "limits": {
            "unique_pairs": MAX_PAIRS,
            "DFS_nodes": MAX_NODES,
            "wall_seconds": 180,
            "peak_bytes": MAX_PEAK_BYTES,
        },
        "selections": [
            [atom_reference(atoms[i], document) for i in values]
            for values in result["selections"]
        ],
    }


def direct_selection(
    references: list[dict[str, Any]],
    atoms: list[Atom],
    document: dict[str, Any],
    budget: Budget,
) -> tuple[list[RowKey], int]:
    lookup = {(atom.owner, atom.row, atom.pieces[0]): atom for atom in atoms}
    owners = sorted({atom.owner for atom in atoms})
    selected: list[Atom] = []
    for reference in references:
        key = reference["owner"], reference["row"], reference["piece"]
        require(all(type(index) is int and index >= 0 for index in key), "invalid atom key")
        atom = lookup[key]
        require(reference == atom_reference(atom, document), "atom provenance differs")
        selected.append(atom)
    require([atom.owner for atom in selected] == owners, "selection owner inventory differs")
    checks = 0
    for position, left in enumerate(selected):
        for right in selected[position + 1 :]:
            remaining(budget)
            require(not incompatible(left, right, budget), "selection contains collision")
            checks += 1
    return [(atom.owner, atom.row) for atom in selected], checks


def verify_packet(
    value: dict[str, Any],
    atoms: list[Atom],
    document: dict[str, Any],
    identity: dict[str, Any],
    budget: Budget,
) -> dict[str, Any]:
    require(
        value["schema"] == SCHEMA and value["predicate"] == PREDICATE, "packet grammar differs"
    )
    require(value["input_identity"] == identity, "packet input identity differs")
    require(
        value["status"]
        in {"ALL_ROWS_SUPPORTED", "EXHAUSTIVE_UNSUPPORTED_ROWS", "INCOMPLETE", "RUNNING"},
        "packet status differs",
    )
    require(
        value["diagnostic_only"] is True and value["new_exclusions"] == 0,
        "packet claims exclusion",
    )
    rows = {(a.owner, a.row) for a in atoms}
    require(
        value["raw_atoms"] == len(atoms) and value["live_rows"] == len(rows),
        "inventory differs",
    )
    selections = []
    checks = 0
    for references in value["selections"]:
        held, count = direct_selection(references, atoms, document, budget)
        selections.append(held)
        checks += count
    supported = set()
    for item in value["row_support"]:
        row = item["owner"], item["row"]
        require(all(type(part) is int and part >= 0 for part in row), "invalid supported row")
        index = item["selection_index"]
        require(type(index) is int and 0 <= index < len(selections), "invalid selection index")
        require(row in rows and row in selections[index], "claimed row absent from selection")
        require(row not in supported, "duplicate supported row")
        supported.add(row)
    if value["status"] == "ALL_ROWS_SUPPORTED":
        require(supported == rows, "all-row claim omits rows")
        require(not value["exhaustive_unsupported_rows"], "all-row claim has unsupported rows")
    return {
        "status": "PASS_REPLAYED_ALL_ROWS"
        if supported == rows
        else "PASS_REPLAYED_PARTIAL_SUPPORT",
        "supported_rows": len(supported),
        "live_rows": len(rows),
        "selections_checked": len(selections),
        "fresh_pair_checks": checks,
        "all_rows_supported": supported == rows,
        "unsupported_rows_independently_verified": False,
        "input_identity": identity,
        "packet_sha256": content_sha256(value),
    }


def endpoint_selection(frame: Frame, document: dict[str, Any], atoms: list[Atom]) -> list[int]:
    targets = load_endpoint(frame).by_owner()
    selected = []
    for owner in sorted({atom.owner for atom in atoms}):
        held = endpoint_holds(targets[owner], document["final_state"]["cells"][str(owner)])
        if held is None:
            raise RefusalError("endpoint absent from input")
        selected.append(
            next(
                i
                for i, a in enumerate(atoms)
                if a.owner == owner and a.row == held["row"] and a.pieces == (held["piece"],)
            )
        )
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--checked-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--endpoint", action="store_true")
    args = parser.parse_args()
    started, cpu = time.monotonic(), time.process_time()
    budget = Budget(started + (120 if args.verify else 180), MAX_NODES)
    result: dict[str, Any] = {"diagnostic_only": True, "new_exclusions": 0}
    try:
        document, identity = checked_inputs(args.directory, args.checked_receipt)
        frame = n17_unique_frame()
        atoms = raw_atoms(frame, document)
        remaining(budget)
        if args.verify:
            retained = bounded_json(args.verify)
            result.update(verify_packet(retained, atoms, document, identity, budget))
            if retained.get("endpoint_exact_presence") is True:
                expected = endpoint_selection(frame, document, atoms)
                require(retained["endpoint_selection_index"] == 0, "endpoint index differs")
                require(
                    retained["selections"][0]
                    == [atom_reference(atoms[i], document) for i in expected],
                    "endpoint selection differs",
                )
                result["endpoint_exact_presence_replayed"] = True
        else:
            search = LazySupports(atoms, budget)
            initial = endpoint_selection(frame, document, atoms) if args.endpoint else None

            def checkpoint(snapshot: dict[str, Any]) -> None:
                write_json(
                    args.output.with_suffix(".partial.json"),
                    packet(snapshot, atoms, document, identity),
                )

            result.update(
                packet(
                    search.run(checkpoint=checkpoint, initial_selection=initial),
                    atoms,
                    document,
                    identity,
                )
            )
            if (
                args.endpoint
                and initial is not None
                and search.selections
                and search.selections[0] == initial
            ):
                result["endpoint_selection_index"] = 0
                result["endpoint_exact_presence"] = True
    except IncompleteError as error:
        result.update(status="INCOMPLETE", reason=str(error))
    except (RefusalError, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        result.update(status="REFUSED", reason=f"{type(error).__name__}: {error}")
    result.update(
        wall_seconds=time.monotonic() - started,
        cpu_seconds=time.process_time() - cpu,
        worker_peak_bytes=peak_memory_bytes(),
    )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                key: item
                for key, item in result.items()
                if key not in {"selections", "row_support"}
            }
        )
    )
    return 2 if result["status"] == "REFUSED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
