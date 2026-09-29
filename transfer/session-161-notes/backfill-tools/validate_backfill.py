"""Throwaway: run check_results' per-result checks over results.yaml plus the draft backfill.

Run with the project interpreter:
    /home/user/squares-docs/packing/.venv/bin/python3 validate_backfill.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
from pathlib import Path

PACKING = Path("/home/user/squares-docs/packing")
sys.path.insert(0, str(PACKING))
sys.path.insert(0, str(PACKING / "src"))

import yaml  # noqa: E402

from devtools import check_results as cr  # noqa: E402
from sqpack.yamlio import safe_load  # noqa: E402

HERE = Path(__file__).resolve().parent
DRAFT = HERE.parent / "register" / "backfill.yaml"
RECENT_SINCE = "2026-08-22"

draft = safe_load(DRAFT.read_text(encoding="utf-8"))
new = [item for item in draft if "claim" in item]
retrofits = [item for item in draft if "claim" not in item]
register = safe_load(cr.RESULTS.read_text(encoding="utf-8"))
existing_ids = {r["id"] for r in register["results"]}

evidence_index = {
    e["id"]: e for e in safe_load(cr.EVIDENCE.read_text(encoding="utf-8"))["evidence"]
}
bibliography = safe_load(
    (PACKING / "resources" / "bibliography.yaml").read_text(encoding="utf-8")
)
bib = {s["key"]: s for s in bibliography["sources"]}

report: dict[str, list[str]] = {
    "checker": [],
    "schema": [],
    "attribution": [],
    "rungs": [],
    "coverage": [],
    "coverage_unknown_date": [],
}

# 1. v1 schema over the stripped draft entries.
schema = safe_load((PACKING / "frontier" / "results.schema.yaml").read_text(encoding="utf-8"))
try:
    import jsonschema

    validator = jsonschema.Draft202012Validator(schema["$defs"]["result"])
    resolver_schema = copy.deepcopy(schema)
    for item in new:
        stripped = {k: v for k, v in item.items() if k != "attribution"}
        wrapped = {"last_reviewed": "2026-09-29", "results": [stripped]}
        for err in jsonschema.Draft202012Validator(resolver_schema).iter_errors(wrapped):
            report["schema"].append(f"{item['id']}: {err.message} at {list(err.path)}")
except ImportError:
    report["schema"].append("jsonschema not importable; v1 schema not checked")

# 2. check_results.main over the combined register (attribution dropped).
combined = copy.deepcopy(register)
combined["results"].extend({k: v for k, v in item.items() if k != "attribution"} for item in new)
with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as fh:
    yaml.safe_dump(combined, fh, sort_keys=False, allow_unicode=True, width=100)
    combined_path = Path(fh.name)
cr.RESULTS = combined_path
import contextlib
import io

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    status = cr.main()
report["checker"] = [f"exit {status}"] + buffer.getvalue().rstrip().splitlines()

# 3. Derived versus declared rungs, per new entry and for the retrofitted ones.
document_map = safe_load(cr.DOCUMENT_MAP.read_text(encoding="utf-8"))
for item in new + [r for r in register["results"] if r["id"] in {x["id"] for x in retrofits}]:
    cited = [evidence_index[e] for e in item["evidence"] if e in evidence_index]
    review = item.get("review_artifact")
    ready = False
    if review:
        entry = cr._document_map_entry(review, document_map)
        ready = bool(entry and entry.get("role") == "review" and entry.get("lifecycle") != "superseded")
    dv = cr.derive_verification(cited)
    dc = cr.derive_confirmation(cited, review_ready=ready)
    flag = "" if (dv, dc) == (item["verification"], item["confirmation"]) else "  (declared differs; composition present: %s)" % bool(item.get("composition"))
    report["rungs"].append(
        f"{item['id']}: declared {item['verification']}/{item['confirmation']}, derived {dv}/{dc}{flag}"
    )

# 4. Attribution: keys resolve in bibliography.yaml; published is a date; retrofits exist.
for item in draft:
    att = item.get("attribution")
    rid = item["id"]
    if att is None:
        report["attribution"].append(f"{rid}: no attribution block")
        continue
    if "claim" not in item and rid not in existing_ids:
        report["attribution"].append(f"{rid}: retrofit names an id not in results.yaml")
    for key in att["source_keys"]:
        if key not in bib:
            report["attribution"].append(f"{rid}: source key {key} does not resolve in bibliography.yaml")
        else:
            dated = bib[key].get("dated")
            if dated and att.get("published") and att["published"] > dated:
                report["attribution"].append(
                    f"{rid}: published {att['published']} is after {key}'s bibliography date {dated}"
                )
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(att.get("published", ""))):
        report["attribution"].append(f"{rid}: published {att.get('published')!r} is not YYYY-MM-DD")
    # every cited source key of the entry's evidence should be among the attribution keys
    if "claim" in item:
        ev_keys = {evidence_index[e].get("source_key") for e in item["evidence"] if e in evidence_index}
        ev_keys.discard(None)
        missing = ev_keys - set(att["source_keys"])
        if missing:
            report["attribution"].append(f"{rid}: evidence source keys not in attribution: {sorted(missing)}")

# 5. Coverage gap: case reported/verified lower bounds citing evidence from a source dated
#    on or after RECENT_SINCE that no register entry (existing or draft) cites.
cited_anywhere = {e for r in combined["results"] for e in r["evidence"]}


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return safe_load(text[4 : text.index("\n---", 4)])


for path in sorted((PACKING / "frontier").glob("n-*.md")):
    packing = front_matter(path)["packing"]
    for field in ("reported_lower_bound", "verified_lower_bound"):
        for ref in (packing.get(field) or {}).get("evidence") or []:
            entry = evidence_index.get(ref)
            if entry is None:
                report["coverage"].append(f"n={packing['n']} {field}: {ref} is not in evidence.yaml")
                continue
            key = entry.get("source_key")
            if key is None or ref in cited_anywhere:
                continue
            dated = (bib.get(key) or {}).get("dated")
            if dated is None:
                report["coverage_unknown_date"].append(
                    f"n={packing['n']} {field}: {ref} (source {key}, no bibliography date)"
                )
            elif dated >= RECENT_SINCE:
                report["coverage"].append(
                    f"n={packing['n']} {field}: {ref} (source {key}, dated {dated}) is cited by no register entry"
                )

print(json.dumps(report, indent=2, ensure_ascii=False))
