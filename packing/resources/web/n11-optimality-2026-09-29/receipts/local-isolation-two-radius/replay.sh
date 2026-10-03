#!/usr/bin/env bash
# Replay review S2's two-radius local rectangle from the accepted weighted and focused
# objects of ../local-dual-residual. Every path is relative to the repository root. The
# checker verifies the decoded SHA-256 of both objects and of the rebuilt two-radius
# rectangle itself, and exits nonzero with status
# REFUSED_TWO_RADIUS_FIXED_T_LOCAL_ISOLATION on any mismatch or failed step.
#
# Usage: replay.sh [OUTPUT_JSON]   (default: $TMPDIR/n11-local-two-radius-result.json)
set -euo pipefail

receipt_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$receipt_dir/../../../../../.." && pwd)"
output="${1:-${TMPDIR:-/tmp}/n11-local-two-radius-result.json}"
output="$(cd "$(dirname "$output")" && pwd)/$(basename "$output")"

cd "$repo_root/packing"
exec timeout 120s .venv/bin/python3 -B -m devtools.check_n11_optimality_local_two_radius \
    --objects resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/objects \
    --max-seconds 90 \
    --output "$output"
