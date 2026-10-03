"""Replay the proposed two-radius, six-curvature-constant local theorem.

Portable invocation (Python 3.10+, with numpy/scipy/sympy installed):

    python verify_simplified_local.py --output ../fresh-results/simplified-local-result.json

The --output option is the only bundle adaptation. Its default is the sibling
fresh-results/ directory, so a fresh run never overwrites a retained receipt.

This script uses paths relative to itself. It expects weighted.json, focused.json,
and the unchanged modules in sq/packing/ listed in SOURCE_SHA256 below, plus the
ordinary cases/trump11/__init__.py and src/sqpack/__init__.py package files.

All source modules are from jlevy/squares commit
ea0a3b19a70085683c3b65946cded03ffe4e2415. The published original proof repository
is Queuingtheorydotcom/11SquaresOptimal at
f9e0de713a0949d1bc6a0fa6b59d96edf6c3d65c. The two exact input SHA-256 hashes are
in INPUT_SHA256 below; their retained gzip objects are available under
packing/resources/web/n11-optimality-2026-09-29/receipts/local-dual-residual/objects/
in the pinned jlevy repository.

No optimization routine is called. This replays all 8,448 residual certificates,
all 88 negative-feature inequalities, and their nonlinear margins exactly. It
shares the original witness/field/gradient source and the feature-bridge helper;
it is not a formal proof assistant or a source-independent geometry library.

The proposed radii are 1/256 except angular coordinates 29 and 32, which use
1/128. Pair curvature K/r^2 is one of 21/2,57/4,99/4,30; wall curvature K/r^2
is 3/4 or 3. The code verifies the elementary rational geometric bounds used
to derive those six constants. The result is conditional on the separately
proved source pose inclusion and global capture.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import sys
import time

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'sq/packing'
INPUT_SHA256 = {
    'weighted.json': 'ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889',
    'focused.json': '9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3',
}
SOURCE_SHA256 = {
    'cases/trump11/packing.py': '3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9',
    'cases/trump11/tangent_cones.py': '17302de574d9f7bc377cbc1dc4c537dc60976d6a1e4e63432adb5fa184058765',
    'cases/trump11/isolation_radius.py': '3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4',
    'src/sqpack/field.py': '734a645d9b95bf43018b1d9662cf255fbf3b834b74ae5e1f10dcf2455a0e3de6',
    'src/sqpack/verify.py': '56bc5b9f690b054ba30e82547dea4aa9d0ccea0a2b1827fab28fcc4e98677337',
    'src/sqpack/exact_lp.py': 'c7e2b92116ae41a7e5e081736be14731553d31bdc85f3ef78c107151aac108ba',
    'devtools/check_n11_optimality_local_dual.py': '2078773593607d3da54f4d6fe7088c5fed224309837d712b030c75d9be04e1f1',
    'devtools/check_n11_optimality_local_isolation.py': '4e64b3de55e1dafec6f8f976aaa6395218801d6c7111f8f5e22cdf2bb99b6ccc',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes():
    for name, expected in INPUT_SHA256.items():
        need(digest(BASE / name) == expected, 'input hash mismatch: ' + name)
    for name, expected in SOURCE_SHA256.items():
        need(digest(SOURCE / name) == expected, 'source hash mismatch: ' + name)


def main():
    need(__debug__, 'Assertions must remain enabled in the imported source modules.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=BASE.parent / 'fresh-results/simplified-local-result.json')
    args = parser.parse_args()
    start = time.monotonic()
    check_hashes()
    sys.path[:0] = [str(SOURCE), str(SOURCE / 'src')]
    from cases.trump11 import isolation_radius as ir
    from devtools import check_n11_optimality_local_dual as dual
    from devtools import check_n11_optimality_local_isolation as local
    shared = dual.bound_sources()
    need(Path(local.__file__).resolve() == (SOURCE / 'devtools/check_n11_optimality_local_isolation.py').resolve(),
         'incorrect feature-bridge import')
    packet = json.loads((BASE / 'weighted.json').read_text())
    focused = json.loads((BASE / 'focused.json').read_text())
    denominator, scale = dual.validate_scales(packet)
    receipts = dual.validate_branch_inventory(packet)
    lo, hi, refinements = dual.root_interval()
    w = ir.load_witness()
    functions = ir.elementary_functions(w, Q(1, 64))
    unavailable, census = local.bridge_features(w, functions)

    r = Q(1, 256)
    radii = [r] * 33
    radii[29] = radii[32] = 2 * r
    old_radii = list(map(Q, focused['radii']))
    need(len(old_radii) == 33 and all(0 < old <= new <= Q(1, 64)
                                     for old, new in zip(old_radii, radii)),
         'new rectangle does not contain the declared old rectangle')
    contacts = {c.pair for c in w.contacts}
    need(len(contacts) == 14, 'wrong contact-pair count')
    # A touching pair has center distance at most sqrt(2). Check this particular
    # witness fact exactly as well, then use one constant over the working box.
    for i, j in contacts:
        dx = w.centres[i][0] - w.centres[j][0]
        dy = w.centres[i][1] - w.centres[j][1]
        need((dx * dx + dy * dy - w.field.rational(2)).sign() <= 0,
             'contact center distance exceeds sqrt(2)')
    need(2 * Q(33, 32)**2 < Q(3, 2)**2, 'working-box distance bound failed')
    need(2 * Q(1, 128)**2 < Q(3, 256)**2, 'translation velocity bound failed')
    need(Q(1, 2) < Q(3, 4)**2, 'corner radius bound failed')

    # Angular radii equal a_i*r with a_i=1 or 2. All translation radii equal r.
    angular = [1] * 9 + [2, 2]
    pair_constants = {(1, 1): Q(21, 2), (1, 2): Q(57, 4),
                      (2, 1): Q(99, 4), (2, 2): Q(30)}
    for (a, b), c in pair_constants.items():
        need(c == Q(3, 2)*a*a + 6*a + Q(3, 4)*(a+b)**2,
             'pair curvature table formula differs')

    def curvature(f):
        if f.kind == 'wall':
            return Q(3, 4) * angular[f.subject[0]]**2 * r*r
        i, j, owner = f.subject[:3]
        need((i, j) in contacts, 'a needed noncontact alias lacks a distance bound')
        other = j if owner == i else i
        return pair_constants[angular[owner], angular[other]] * r*r

    rowkeys = [[local.signature(row.coefficients) for row in branch['rows']]
               for branch in w.branches]
    neededkeys = {key for keys in rowkeys for key in keys}
    bounds = {}
    alias_pairs = set()
    for f in functions:
        if f.value.is_zero():
            key = local.signature(f.gradient)
            if key in neededkeys:
                bounds[key] = max(bounds.get(key, Q(0)), curvature(f))
                if f.kind == 'pair':
                    alias_pairs.add(f.subject[:2])
    need(set(bounds) == neededkeys and alias_pairs == contacts,
         'needed tied elementary-function alias coverage differs')

    intervals = {}

    def interval(value):
        key = tuple(value.coeffs)
        if key not in intervals:
            left = right = Q(0)
            for coefficient in reversed(key):
                products = (left*lo, left*hi, right*lo, right*hi)
                left, right = min(products)+coefficient, max(products)+coefficient
            intervals[key] = left, right
        return intervals[key]

    seen = set()
    minimum_gap = None
    worst_feature = None
    for record in packet['unavailable_feature_proofs']:
        key = tuple(record['feature'])
        need(key in unavailable and key not in seen, 'invalid or duplicate unavailable feature')
        seen.add(key)
        corner = record['negative_corner']
        need(type(corner) is int and 0 <= corner < 4, 'invalid corner index')
        f = next(f for f in unavailable[key] if f.subject[-1] == corner)
        upper = interval(f.value)[1]
        need(upper < 0, 'negative corner has no certified negative initial value')
        linear = sum(max(abs(a), abs(b))*radius
                     for (a, b), radius in zip(map(interval, f.gradient), radii, strict=True))
        gap = -(upper + linear + curvature(f)/2)
        need(gap > 0, 'a forbidden feature can activate in the larger rectangle')
        if minimum_gap is None or gap < minimum_gap:
            minimum_gap, worst_feature = gap, list(f.subject)
    need(seen == set(unavailable) and len(seen) == 88, 'incomplete forbidden-feature inventory')
    need(minimum_gap > Q(1, 200), 'simple printed lower feature margin was not verified')

    checked = 0
    maximum_ratio = Q(0)
    worst_coordinate = None
    for branch, keys in zip(w.branches, rowkeys, strict=True):
        branch_id = branch['branch']
        certs = receipts[branch_id]['certificates']
        matrix = dual.integer_matrix(branch['rows'], lo, hi, scale)
        count, _ = dual.check_residuals(matrix, certs, denominator, scale)
        checked += count
        row_bounds = [bounds[key] for key in keys]
        for certificate in certs:
            j, sign = certificate['coordinate'], certificate['sign']
            error = Q(certificate['residual_upper'])
            mass = sum(Q(v, denominator)*k
                       for v, k in zip(certificate['coefficients'], row_bounds, strict=True))
            right = 2*(radii[j] - error*max(radii))
            need(right > 0 and 0 < mass < right, 'strict local dual margin failed')
            ratio = mass / right
            if ratio > maximum_ratio:
                maximum_ratio = ratio
                worst_coordinate = [branch_id, j, sign]
    need(checked == 8448, 'not all signed coordinate residuals were checked')
    need(maximum_ratio < Q(20, 21), 'simple printed upper dual ratio was not verified')
    check_hashes()
    need(dual.bound_sources() == shared, 'shared imports changed during the check')
    output = {
        'status': 'PASS_SIMPLIFIED_FIXED_T_LOCAL_BOX',
        'scope': 'Local fixed-T labelled isolation only; capture and source-pose inclusion are separate premises.',
        'input_sha256': INPUT_SHA256, 'source_sha256': SOURCE_SHA256,
        'checker_sha256': digest(Path(__file__)),
        'root_refinements': refinements, 'features': census,
        'old_rectangle_contained_in_new': True, 'radii': list(map(str, radii)),
        'center_distance_bound': '3/2', 'translation_velocity_bound': '3/256',
        'corner_offset_bound': '3/4',
        'pair_curvature_coefficients_over_r_squared': {str(k): str(v) for k, v in pair_constants.items()},
        'wall_curvature_coefficients_over_r_squared': ['3/4', '3'],
        'all_tied_alias_pairs_are_contacts': True,
        'fresh_signed_coordinate_residuals_checked': checked,
        'negative_features_checked': len(seen), 'worst_dual_ratio': str(maximum_ratio),
        'worst_dual_ratio_float': float(maximum_ratio), 'worst_coordinate': worst_coordinate,
        'worst_dual_ratio_less_than': '20/21',
        'minimum_feature_margin': str(minimum_gap),
        'minimum_feature_margin_float': float(minimum_gap), 'worst_feature': worst_feature,
        'minimum_feature_margin_greater_than': '1/200',
        'seconds': time.monotonic()-start,
    }
    destination = args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ('status', 'fresh_signed_coordinate_residuals_checked',
          'negative_features_checked', 'worst_dual_ratio', 'worst_dual_ratio_float',
          'minimum_feature_margin_float', 'seconds')}, indent=2))


if __name__ == '__main__':
    main()
