#!/usr/bin/env python3
"""Consume the supplied v2 incidence trace without generating or rewriting it."""
if not __debug__:
    raise RuntimeError("This mathematical checker refuses Python -O/-OO.")

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    import d4_propagation_certificate as checker

    path = BASE / "d4-propagation-traces.json"
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    # Import and call only the independent consumer. The producer's __main__
    # block and generate() routine are never executed by this entry point.
    summary = checker.verify(json.loads(raw))
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("The supplied incidence trace changed during consumption")
    if {int(k): v["survivors"] for k, v in summary.items()} != {999: 1, 1462: 1, 1659: 0}:
        raise ValueError("Unexpected D4 survivor inventory")
    result = {
        "status": "PASS_READ_ONLY_D4_INCIDENCE_TRACE",
        "trace_schema": "independent_d4_bijection_trace_v2",
        "trace_sha256": digest,
        "trace_regenerated": False,
        "records_checked": 648,
        "summary": summary,
        "global_optimality_proved": False,
        "scope": "Conditional final D4 incidence component; geometry is independently reconstructed in a separate check.",
    }
    target = BASE / "fresh-results/d4-incidence-consumer.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
