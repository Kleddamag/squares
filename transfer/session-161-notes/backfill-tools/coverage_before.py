import sys
from pathlib import Path
PACKING = Path("/home/user/squares-docs/packing")
sys.path.insert(0, str(PACKING)); sys.path.insert(0, str(PACKING / "src"))
from devtools import check_results as cr
from sqpack.yamlio import safe_load
reg = safe_load(cr.RESULTS.read_text())
draft = [d for d in safe_load((Path(__file__).resolve().parent.parent / "register" / "backfill.yaml").read_text()) if "claim" in d]
ev = {e["id"]: e for e in safe_load(cr.EVIDENCE.read_text())["evidence"]}
bib = {s["key"]: s for s in safe_load((PACKING/"resources/bibliography.yaml").read_text())["sources"]}
before = {e for r in reg["results"] for e in r["evidence"]}
draft_cites = {e: [d["id"] for d in draft if e in d["evidence"]] for d in draft for e in d["evidence"]}
gaps = {}
for p in sorted((PACKING/"frontier").glob("n-*.md")):
    t = p.read_text(); pk = safe_load(t[4:t.index("\n---",4)])["packing"]
    for f in ("reported_lower_bound","verified_lower_bound"):
        for ref in (pk.get(f) or {}).get("evidence") or []:
            k = ev[ref].get("source_key"); d = (bib.get(k) or {}).get("dated")
            if k and d and d >= "2026-08-22" and ref not in before:
                gaps.setdefault(ref, []).append(pk["n"])
for ref, ns in gaps.items():
    print(f"{ref}: n={ns} -> closed by {draft_cites.get(ref)}")
# evidence entries from recent sources that no entry (existing or draft) cites at all
allc = before | set(draft_cites)
print("--- recent-source evidence cited by no entry (not necessarily case-bound):")
for i,e in ev.items():
    k=e.get("source_key"); d=(bib.get(k) or {}).get("dated")
    if k and d and d>="2026-08-22" and i not in allc: print(" ", i, k, d)
print("--- evidence source keys absent from bibliography.yaml:")
for k in sorted({e.get("source_key") for e in ev.values() if e.get("source_key") and e.get("source_key") not in bib}): print(" ", k)
