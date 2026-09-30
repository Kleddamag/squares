#!/usr/bin/env bash
set -euo pipefail

: "${TMPDIR:?set external scratch TMPDIR}"
: "${CARGO_TARGET_DIR:?set external scratch CARGO_TARGET_DIR}"
: "${UV_CACHE_DIR:?set external scratch UV_CACHE_DIR}"

receipt_dir=$(cd "$(dirname "$0")" && pwd)
repo_root=$(cd "$receipt_dir/../../../../../.." && pwd)
cd "$repo_root"

args=(
  --objects "$receipt_dir/objects"
  --cover "packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e.gz"
  --all
  --max-seconds 30
  --max-nodes 100000
)
if [[ $# -gt 0 ]]; then
  args+=(--output "$1")
fi
exec packing/.venv/bin/python3 packing/devtools/check_n11_optimality_field_mask0.py "${args[@]}"
