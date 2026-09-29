#!/bin/sh
# build_lean.sh from point_n21_L5/lean at 39d8ecc, every step before 'lake' (no Lean toolchain here);
# the upstream clone is the 6e1223cf checkout verify.sh made, copied.
set -eu
HERE=/tmp/claude-0/-home-user-squares/b85b7ecf-955c-5223-9481-e5200885a948/scratchpad/lane3/src/point_n21_L5/lean
P=/tmp/claude-0/-home-user-squares/b85b7ecf-955c-5223-9481-e5200885a948/scratchpad/lane3/lean-check/lean
sha() { sha256sum "$1" | cut -d' ' -f1; }
[ "$(sha "$P/Sqpack.lean")" = 094c02f94b50aa123a2be8b61cf1655189f148b7f8f1ef2d6364dcf64b10ab6a ]
echo SQPACK_LEAN_SHA_OK
for f in N21Pts.lean N21PtsAxioms.lean N21PtsData.lean; do
  [ ! -e "$P/Sqpack/$f" ] || { echo "upstream already has $f" >&2; exit 1; }
  cp "$HERE/Sqpack/$f" "$P/Sqpack/$f"
done
cp "$HERE/scripts/gen_n21pts_data.py" "$P/scripts/gen_n21pts_data.py"
printf 'import Sqpack.N21Pts\nimport Sqpack.N21PtsAxioms\n' >> "$P/Sqpack.lean"
CAND="$HERE/../certificates/n21-original.txt"
[ "$(sha "$CAND")" = 84a7dae793f05ff72de52ddcd3058e8518c1f84c461f94d11305adefe6137679 ]
(cd "$P" && python3 scripts/gen_n21pts_data.py --source "$CAND" --check)
if grep -rn -e 'sorry' -e 'native_decide' -e '^axiom' "$P/Sqpack/N21Pts.lean" "$P/Sqpack/N21PtsData.lean"; then
  echo "forbidden construct in overlay" >&2; exit 1
fi
echo "N21PtsData.lean sha256 $(sha "$P/Sqpack/N21PtsData.lean")"
echo LEAN_OVERLAY_PREFIX_OK_LAKE_NOT_RUN
