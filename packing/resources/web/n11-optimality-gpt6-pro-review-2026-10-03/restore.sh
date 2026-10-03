#!/usr/bin/env bash
# Rebuild all 202 members of n11-optimality-unified-review-evidence.zip, byte for byte, from
# this packet and the objects the 2026-09-29 packet already retains.
#
#   bash restore.sh OUT        # OUT is a new directory outside the repository
#
# Then run the archive's own drivers from OUT as its README.txt describes. PYTHON selects the
# interpreter for the final identity check (default python3; standard library only).
set -euo pipefail

packet="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
objects="$packet/../n11-optimality-2026-09-29/receipts"
out="${1:?usage: bash restore.sh OUT, where OUT is a new directory outside the repository}"
test ! -e "$out"

cp -R "$packet/n11-unified-review-evidence" "$out"
find "$out" -name '*.gz' -exec gunzip {} +

restore() { # restore OBJECT MEMBER: decompress a retained repository object to an archive path
    mkdir -p "$(dirname "$out/$2")"
    gzip -dc "$objects/$1" > "$out/$2"
}
cover=df7938d9ba27095a38fabe45f8b26b259a2cc896c2ae4aac6bae874f417adc4e
overlay=845b5f748843dd60fa7e290a5ea1a304da4e439ae229bd73a841aec816f4e700
mirror=prior-supplement/squares/packing/resources/web/n11-optimality-2026-09-29/receipts/d4-independent/objects
restore local-dual-residual/objects/ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889.gz \
    prior-supplement/local-isolation-audit/weighted.json
restore local-dual-residual/objects/9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3.gz \
    prior-supplement/local-isolation-audit/focused.json
restore case-census/objects/04fa1ebb37f5dace29946224fe8c7c5d8a1bedb4fa860c65b359f4200415de57.gz \
    prior-supplement/fields/A1-baseline.json
restore "d4-independent/objects/$cover.gz" "geometry-audit/$cover.json"
restore "d4-independent/objects/$cover.gz" "$mirror/$cover.json"
restore "d4-independent/objects/$overlay.gz" "$mirror/$overlay.json"

# Every member against provenance.json: a missing, extra or changed file fails.
"${PYTHON:-python3}" - "$packet/provenance.json" "$out" <<'CHECK'
import hashlib, json, pathlib, sys

files = json.loads(pathlib.Path(sys.argv[1]).read_text())["files"]
root = pathlib.Path(sys.argv[2])
present = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
if present != set(files):
    sys.exit(f"member set differs: {sorted(present ^ set(files))}")
for name, row in sorted(files.items()):
    data = (root / name).read_bytes()
    if len(data) != row["size_bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
        sys.exit(f"member differs: {name}")
print(f"restored {len(files)} archive members byte for byte in {root}")
CHECK
