#!/usr/bin/env bash
# Replay the n=11 D4 incidence bridge (review S3) from the retained cover and overlay
# objects of ../d4-independent. Every path is relative to the repository root. The
# checker verifies the stored and decoded SHA-256 of both objects itself, and exits
# nonzero with status REFUSED_D4_INCIDENCE_BRIDGE on any mismatch or failed step.
#
# Usage: replay.sh [OUTPUT_JSON]   (default: $TMPDIR/n11-d4-incidence-result.json)
set -euo pipefail

receipt_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$receipt_dir/../../../../../.." && pwd)"
output="${1:-${TMPDIR:-/tmp}/n11-d4-incidence-result.json}"
output="$(cd "$(dirname "$output")" && pwd)/$(basename "$output")"

cd "$repo_root/packing"
exec .venv/bin/python3 -B -m devtools.check_n11_optimality_d4_incidence \
    --objects resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects \
    --max-seconds 45 \
    --output "$output"
