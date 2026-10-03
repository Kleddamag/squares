#!/usr/bin/env python3
"""Check exact field case sets and minimum-44 selection from recorded fresh replays.

This finite-set checker does not rerun the field ownership/coverage geometry.
"""
if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parent
A1_SHA = "04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57"
COVER_SHA = "df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e"
RUNNER_SHA = "84a65756676fb9b599294007e437ab8d5869acdef4312f64518a069de8bc12d8"
KERNEL_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
SOURCE_REVISION = "f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def ids(values, label):
    require(type(values) is list and all(type(v) is int and 0 <= v < 2184 for v in values), label + " case grammar")
    require(len(values) == len(set(values)), label + " duplicate case")
    return set(values)


def check_record(record, entry):
    require(record["status"] == "PASS_ONE_FIELD_GEOMETRY_AND_TRANSFER" and record["geometry_verified"] is True, "Receipt lacks complete recorded field result")
    require(record["global_optimality_proved"] is False, "Field receipt claims global optimality")
    require(record["packet_sha256"] == entry["source_sha256"] and record["audit_proposal_sha256"] == entry["fresh_audit_sha256"], "Field source binding differs")
    require(record["cover_sha256"] == COVER_SHA and record["upstream_source_revision"] == SOURCE_REVISION, "Field frame/source revision differs")
    require(record["checker_sha256"] == RUNNER_SHA and record["frozen_geometry_kernel_sha256"] == KERNEL_SHA, "Recorded checker source differs")
    require(record["ownership_pending"] == [] and record["rows_pending"] == [], "Recorded geometry has pending obligations")
    require(len(record["ownership_checked"]) == record["ownership_points"], "Ownership count differs")
    require(len(record["rows_checked"]) == record["positive_cell_rows"], "Angle row count differs")
    own = defaultdict(list)
    for row in record["ownership_checked"]:
        require(type(row["owner"]) is int and 0 <= row["owner"] < 16, "Owner label grammar")
        require(type(row["point_index"]) is int, "Ownership point index grammar")
        own[row["owner"]].append(row["point_index"])
    require(all(sorted(indices) == list(range(len(indices))) for indices in own.values()), "Ownership point inventory has a gap or duplicate")
    by_cell = defaultdict(list)
    for row in record["rows_checked"]:
        require(type(row["cell"]) is int and 0 <= row["cell"] < 16, "Row cell grammar")
        require(type(row["row_index"]) is int, "Row index grammar")
        a, b = map(Fraction, row["interval"])
        require(0 <= a < b <= 1, "Malformed recorded closed interval")
        by_cell[row["cell"]].append((row["row_index"], a, b))
    for rows in by_cell.values():
        rows.sort()
        require([r[0] for r in rows] == list(range(len(rows))), "Row inventory has a gap or duplicate")
        require(rows[0][1] == 0 and rows[-1][2] == 1, "Closed angular endpoint is missing")
        require(all(a[2] == b[1] for a, b in zip(rows, rows[1:])), "Recorded angle cover has a gap")
    cases = ids(record["transfer"]["transferred_case_ids"], "recorded transfer")
    require(cases == ids(entry["cases"], "pinned A1 field"), "Recorded transfer differs from pinned baseline")
    require(len(cases) == record["canonical_cases_excluded"], "Recorded exclusion count differs")
    return cases


def main():
    raw = (BASE / "fields/A1-baseline.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == A1_SHA, "Pinned A1 baseline bytes changed")
    baseline = strict_json(raw)
    fields = [e for e in baseline["certificates"] if e["family"] == "field"]
    require(len(fields) == 59 and len({e["source_sha256"] for e in fields}) == 59, "Original field inventory differs")
    expected_files = {e["source_sha256"] + ".json" for e in fields}
    require({p.name for p in (BASE / "fields/receipts").glob("*.json")} == expected_files, "Fresh-review receipt inventory differs")
    records, sets = {}, {}
    for entry in fields:
        sha = entry["source_sha256"]
        record = strict_json((BASE / "fields/receipts" / (sha + ".json")).read_bytes())
        sets[sha] = check_record(record, entry)
        records[sha] = record
    universe = set.union(*sets.values())
    require(len(universe) == 1904, "Field case union differs")
    coverers = {case: {sha for sha, values in sets.items() if case in values} for case in universe}
    mandatory = {next(iter(owners)) for owners in coverers.values() if len(owners) == 1}
    mandatory_union = set.union(*(sets[sha] for sha in mandatory))
    require(len(mandatory) == 43 and len(mandatory_union) == 1903 and universe - mandatory_union == {1456}, "Minimum-selection witness differs")
    proposal = strict_json((BASE / "fields/minimal-44-field-manifest.json").read_bytes())
    proposed = proposal["certificates"]
    require(len(proposed) == 59 and {r["source_sha256"] for r in proposed} == set(sets), "Subset manifest inventory differs")
    selected = set()
    for row in proposed:
        sha = row["source_sha256"]
        require(type(row["selected"]) is bool and type(row["mandatory"]) is bool, "Subset flags must be boolean")
        require(row["mandatory"] == (sha in mandatory), "Mandatory flag differs")
        require(ids(row["case_ids"], "subset entry") == sets[sha], "Subset transfer set differs")
        unique = {case for case, owners in coverers.items() if owners == {sha}}
        require(ids(row["all_uniquely_covered_case_ids"], "uniqueness witness") == unique, "Uniqueness case list differs")
        require(row["unique_case_witness"] == (min(unique) if unique else None), "Unique-case witness differs")
        require(row["angle_rows"] == records[sha]["positive_cell_rows"] and row["ownership_points"] == records[sha]["ownership_points"], "Subset work counts differ")
        if row["selected"]:
            selected.add(sha)
    selected_union = set.union(*(sets[sha] for sha in selected))
    require(len(selected) == 44 and mandatory <= selected and selected_union == universe, "Selected 44 do not give the required union")
    all_rows = sum(r["positive_cell_rows"] for r in records.values())
    all_points = sum(r["ownership_points"] for r in records.values())
    selected_rows = sum(records[sha]["positive_cell_rows"] for sha in selected)
    selected_points = sum(records[sha]["ownership_points"] for sha in selected)
    require((all_rows, all_points, selected_rows, selected_points) == (24373, 5877, 17963, 4233), "Aggregate row/ownership counts differ")
    generics = [e for e in baseline["certificates"] if e["family"] == "generic"]
    require(len(generics) == 34 and all(len(e["cases"]) == 1 for e in generics), "Generic baseline inventory differs")
    generic_cases = set.union(*(ids(e["cases"], "generic entry") for e in generics))
    require(len(generic_cases) == 34 and len(generic_cases - universe) == 27 and len(generic_cases | universe) == 1931, "93-to-71 top-level inventory arithmetic differs")
    result = {
        "status": "PASS_RECORDED_FIELD_SETS_AND_MINIMUM_44",
        "recorded_complete_field_replays": 59,
        "recorded_field_case_union": 1904,
        "mandatory_certificates": 43,
        "mandatory_union": 1903,
        "residual_case": 1456,
        "minimum_sufficient_field_certificates": 44,
        "original_angle_rows": all_rows,
        "selected_angle_rows": selected_rows,
        "original_ownership_points": all_points,
        "selected_ownership_points": selected_points,
        "redundant_generic_case_ids": sorted(generic_cases & universe),
        "sufficient_top_level_baseline_certificates": 71,
        "geometry_rerun": False,
        "global_optimality_proved": False,
        "scope": "Finite sets and minimality checked against recorded fresh field results. Geometry is not reexecuted. The 71 count is a top-level certificate count, not a 71-file source closure; shared ancestry and downstream bindings remain separate obligations.",
    }
    target = BASE / "fresh-results/field-subset-verification.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
