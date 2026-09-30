#!/usr/bin/env bash
set -euo pipefail

: "${TMPDIR:?set external scratch TMPDIR}"
: "${CARGO_TARGET_DIR:?set external scratch CARGO_TARGET_DIR}"
: "${UV_CACHE_DIR:?set external scratch UV_CACHE_DIR}"
output=${1:?pass a new output JSON path outside the repository source tree}
receipt_dir=$(cd "$(dirname "$0")" && pwd)
repo_root=$(cd "$receipt_dir/../../../../../.." && pwd)
cd "$repo_root/packing"

PYTHONDONTWRITEBYTECODE=1 gtimeout 35 .venv/bin/python3 \
  -m devtools.check_n11_optimality_field_runner \
  --mask-index 202 \
  --objects resources/web/n11-optimality-2026-09-29/receipts/field-mask202/objects \
  --cover resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects/df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e.gz \
  --all --max-seconds 30 --max-work 100000 --output "$output" > /dev/null
