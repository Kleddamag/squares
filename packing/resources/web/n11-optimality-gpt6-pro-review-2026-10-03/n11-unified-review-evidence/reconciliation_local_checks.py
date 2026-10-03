"""Exact reconciliation of A's local claims against B's pinned certificate data.

No new LP certificates are generated. B's 8,448 retained certificates are replayed;
their algebraic residuals are directly enclosed coordinatewise for weighted norms.

Portable use with the previously delivered B supplement (Python 3.10+, with its
numpy/scipy/sympy dependencies installed):

    python -B reconciliation_local_checks.py --bundle /path/to/n11-review-supplement

Optionally pass --review-a /path/to/report-A.md to compare its printed radii with
B's pinned focused.json. This is a text-input comparison, not verification of A's
unavailable new dual vectors. The old supplement's local-isolation-audit/ subtree
must contain weighted.json, focused.json, and its ten-module sq/packing closure;
its recorded-results/ contains published-local-replay-result.json and
simplified-local-result.json. The original audit-tree layout is also accepted.

Outputs are written to --output-dir, defaulting to fresh-results/ beside this
script. No existing supplement source or retained receipt is changed.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, math, sys, time

ROOT = Path(__file__).resolve().parent
EXPECTED_SOURCE_SHA256 = {
    'cases/trump11/packing.py': '3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9',
    'cases/trump11/tangent_cones.py': '17302de574d9f7bc377cbc1dc4c537dc60976d6a1e4e63432adb5fa184058765',
    'cases/trump11/isolation_radius.py': '3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4',
    'src/sqpack/field.py': '734a645d9b95bf43018b1d9662cf255fbf3b834b74ae5e1f10dcf2455a0e3de6',
    'src/sqpack/verify.py': '56bc5b9f690b054ba30e82547dea4aa9d0ccea0a2b1827fab28fcc4e98677337',
    'src/sqpack/exact_lp.py': 'c7e2b92116ae41a7e5e081736be14731553d31bdc85f3ef78c107151aac108ba',
    'devtools/check_n11_optimality_local_dual.py': '2078773593607d3da54f4d6fe7088c5fed224309837d712b030c75d9be04e1f1',
    'devtools/check_n11_optimality_local_isolation.py': '4e64b3de55e1dafec6f8f976aaa6395218801d6c7111f8f5e22cdf2bb99b6ccc',
}


def key(row):
    return tuple(tuple(v.coeffs) for v in row)


def sparse_record(row):
    return {str(j): list(map(str, v.coeffs)) for j, v in enumerate(row) if not v.is_zero()}


def main():
    if not __debug__:
        raise SystemExit('Assertions must remain enabled.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,default=ROOT)
    parser.add_argument('--review-a',type=Path)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'fresh-results')
    args=parser.parse_args()
    bundle=args.bundle.expanduser().resolve()
    BASE=bundle/'local-isolation-audit'
    SOURCE=BASE/'sq/packing'
    sys.dont_write_bytecode=True
    sys.path[:0]=[str(SOURCE),str(SOURCE/'src')]
    from cases.trump11 import isolation_radius as ir
    from devtools import check_n11_optimality_local_dual as dual
    from devtools import check_n11_optimality_local_isolation as local
    start = time.monotonic()
    assert all(dual.digest(SOURCE/name)==sha for name,sha in EXPECTED_SOURCE_SHA256.items())
    assert Path(dual.__file__).resolve()==(SOURCE/'devtools/check_n11_optimality_local_dual.py').resolve()
    assert Path(local.__file__).resolve()==(SOURCE/'devtools/check_n11_optimality_local_isolation.py').resolve()
    assert dual.digest(BASE/'weighted.json') == dual.WEIGHTED_SHA
    assert dual.digest(BASE/'focused.json') == dual.FOCUSED_SHA
    sources = dual.bound_sources()
    packet = json.loads((BASE/'weighted.json').read_text())
    focused = json.loads((BASE/'focused.json').read_text())
    weight_den, matrix_scale = dual.validate_scales(packet)
    receipts = dual.validate_branch_inventory(packet)
    lo, hi, _ = dual.root_interval()
    w = ir.load_witness()
    functions = ir.elementary_functions(w, Q(1, 64))
    unavailable, census = local.bridge_features(w, functions)
    branches = [[key(row.coefficients) for row in b['rows']] for b in w.branches]
    row_by_key = {key(row.coefficients): row.coefficients for b in w.branches for row in b['rows']}
    keys = sorted(row_by_key)
    identifiers = {k: j for j, k in enumerate(keys)}
    common = set.intersection(*(set(b) for b in branches))
    assert len(keys) == 56 and len(common) == 30
    assert len(branches) == 128 and all(len(b) == len(set(b)) == 42 for b in branches)

    # Exact row reduction and a fully checked nullspace basis over Q(alpha).
    cm = [list(row_by_key[k]) for k in sorted(common)]
    original_common = [list(row) for row in cm]
    pivots = []
    pivot_row = 0
    for column in range(33):
        pivot = next((i for i in range(pivot_row, len(cm)) if not cm[i][column].is_zero()), None)
        if pivot is None:
            continue
        cm[pivot_row], cm[pivot] = cm[pivot], cm[pivot_row]
        inverse = cm[pivot_row][column].inverse()
        cm[pivot_row] = [v*inverse if not v.is_zero() else v for v in cm[pivot_row]]
        for i in range(len(cm)):
            factor = cm[i][column]
            if i != pivot_row and not factor.is_zero():
                cm[i] = [v-factor*u if not u.is_zero() else v
                         for v, u in zip(cm[i], cm[pivot_row], strict=True)]
        pivots.append(column)
        pivot_row += 1
    free = sorted(set(range(33))-set(pivots))
    kernel = []
    for column in free:
        vector = [w.field.zero]*33
        vector[column] = w.field.one
        for i, p in enumerate(pivots):
            vector[p] = -cm[i][column]
        assert all(sum((a*b for a, b in zip(row, vector, strict=True)), w.field.zero).is_zero()
                   for row in original_common)
        kernel.append(vector)
    assert all(cm[i][p] == (1 if i == j else 0)
               for j, p in enumerate(pivots) for i in range(len(cm)))
    assert all(all(v.is_zero() for v in cm[i]) for i in range(len(pivots), len(cm)))
    print('common rows', len(common), 'exact rank', len(pivots), 'nullity', len(kernel), flush=True)

    radii0 = list(map(Q, focused['radii']))
    radii1 = [Q(1,256)]*33
    radii1[29] = radii1[32] = Q(1,128)
    a_radii_match=None
    a_sha256=None
    if args.review_a is not None:
        arows = []
        review_text=args.review_a.read_text()
        for line in review_text.splitlines():
            fields = [s.strip() for s in line.split('|')]
            if len(fields) == 6 and fields[1].isdigit() and '/' in fields[2]:
                arows.append((int(fields[1]), [Q(s) for s in fields[2:5]]))
        assert [i for i, _ in arows] == list(range(11))
        assert [v for _, row in arows for v in row] == radii0
        a_radii_match=True
        a_sha256=dual.digest(args.review_a)

    # Curvature configuration 1 matches B's published-checker replay exactly.
    interval_cache = {}
    def interval(v):
        k = tuple(v.coeffs)
        if k not in interval_cache:
            interval_cache[k] = dual.field_interval(v, lo, hi)
        return interval_cache[k]
    root2, invroot2 = Q(packet['sqrt2_upper']), Q(packet['inverse_sqrt2_upper'])
    tightroot2 = local.radical_upper(Q(2))
    tightinvroot2 = local.radical_upper(Q(1,2))
    distances, velocities, tightdistances = {}, {}, {}
    for i in range(11):
        for j in range(i+1,11):
            dx, dy = w.centres[i][0]-w.centres[j][0], w.centres[i][1]-w.centres[j][1]
            d0 = local.radical_upper(interval(dx*dx+dy*dy)[1])
            distances[i,j] = d0 + 2*root2/64
            tightdistances[i,j] = d0 + 2*tightroot2/64
            velocities[i,j] = local.radical_upper((radii0[3*i]+radii0[3*j])**2 +
                                                   (radii0[3*i+1]+radii0[3*j+1])**2)
    def curvature(f, configuration):
        if configuration == 'simple':
            angular = [1]*9+[2,2]
            if f.kind == 'wall':
                return Q(3,4)*angular[f.subject[0]]**2*Q(1,256)**2
            i,j,o = f.subject[:3]
            p = j if o == i else i
            a,b = angular[o],angular[p]
            return (Q(3,2)*a*a+6*a+Q(3,4)*(a+b)**2)*Q(1,256)**2
        iq = tightinvroot2 if configuration == 'tight' else invroot2
        if f.kind == 'wall':
            return iq*radii0[3*f.subject[0]+2]**2
        i,j,o = f.subject[:3]
        p = j if o == i else i
        a,b = radii0[3*o+2],radii0[3*p+2]
        d = tightdistances[i,j] if configuration == 'tight' else distances[i,j]
        return d*a*a+2*velocities[i,j]*a+iq*(a+b)**2
    aliases = {k: [] for k in keys}
    for f in functions:
        if f.value.is_zero() and key(f.gradient) in aliases:
            aliases[key(f.gradient)].append(f)
    bounds = {configuration: {k:max(curvature(f,configuration) for f in fs)
                               for k,fs in aliases.items()}
              for configuration in ('published','tight','simple')}

    # Integer encoding of every exact field coefficient in the 56 canonical rows.
    poly_den = math.lcm(*(c.denominator for k in keys for scalar in k for c in scalar))
    rows_int = {}
    for k in keys:
        rows_int[k] = [(j, [int(c*poly_den) for c in scalar])
                       for j,scalar in enumerate(k) if any(scalar)]
    # Fixed-scale outward Horner arithmetic directly encloses the residual polynomial.
    # All arithmetic is integer/Fraction. This avoids subtracting coarse independent
    # matrix-entry enclosures after cancellation.
    root_scale = 10**80
    lower_root = lo.numerator*root_scale//lo.denominator
    upper_root = -((-hi.numerator*root_scale)//hi.denominator)
    assert Q(lower_root,root_scale) <= lo <= hi <= Q(upper_root,root_scale)
    residual_den = poly_den*weight_den*root_scale
    residual_cache = {}
    def abs_residual_upper(coeffs):
        ck=tuple(coeffs)
        if ck not in residual_cache:
            lower=upper=0
            for c in reversed(coeffs):
                products=(lower*lower_root,lower*upper_root,upper*lower_root,upper*upper_root)
                lower=min(products)//root_scale+c*root_scale
                upper=-((-max(products))//root_scale)+c*root_scale
            residual_cache[ck]=Q(max(abs(lower),abs(upper)),residual_den)
        return residual_cache[ck]

    outcomes = {c: {'unweighted': (Q(0),None), 'weighted': (Q(0),None),
                    'normalized_sum': (Q(0),None)} for c in ('published','tight','simple')}
    check_count=0
    maximum_eta = [Q(0),Q(0)]
    maximum_l1=Q(0)
    for branch,branchkeys in zip(w.branches,branches,strict=True):
        branch_id=branch['branch']
        certificates=receipts[branch_id]['certificates']
        matrix=dual.integer_matrix(branch['rows'],lo,hi,matrix_scale)
        count,_=dual.check_residuals(matrix,certificates,weight_den,matrix_scale)
        check_count+=count
        for cert in certificates:
            coordinate,sign=cert['coordinate'],cert['sign']
            epsilon=Q(cert['residual_upper'])
            accum=[[0]*w.field.degree for _ in range(33)]
            accum[coordinate][0]=-sign*poly_den*weight_den
            nonzero_weights=[]
            for rowindex,weight in enumerate(cert['coefficients']):
                if weight:
                    nonzero_weights.append((branchkeys[rowindex],Q(weight,weight_den)))
                    for j,scalar in rows_int[branchkeys[rowindex]]:
                        for d,c in enumerate(scalar):
                            accum[j][d]+=weight*c
            residuals=list(map(abs_residual_upper,accum))
            assert sum(residuals)<=epsilon
            maximum_l1=max(maximum_l1,sum(residuals))
            etas=[sum(r*x for r,x in zip(radii,residuals,strict=True)) for radii in (radii0,radii1)]
            maximum_eta=[max(a,b) for a,b in zip(maximum_eta,etas,strict=True)]
            location=[branch_id,coordinate,sign]
            for configuration in ('published','tight','simple'):
                radii=radii1 if configuration=='simple' else radii0
                eta=etas[1 if configuration=='simple' else 0]
                mass=sum(weight*bounds[configuration][k] for k,weight in nonzero_weights)
                assert eta <= epsilon*max(radii)
                assert eta+mass/2 < radii[coordinate]
                metrics={'unweighted': mass/(2*(radii[coordinate]-epsilon*max(radii))),
                         'weighted': mass/(2*(radii[coordinate]-eta)),
                         'normalized_sum':(eta+mass/2)/radii[coordinate]}
                for metric,value in metrics.items():
                    if value>outcomes[configuration][metric][0]:
                        outcomes[configuration][metric]=(value,location)
        if branch_id%32==31:
            print('processed branches',branch_id+1,flush=True)
    assert check_count==8448
    baseline_path=bundle/'recorded-results/published-local-replay-result.json'
    if not baseline_path.exists():baseline_path=BASE/'replay-result.json'
    simple_path=bundle/'recorded-results/simplified-local-result.json'
    if not simple_path.exists():simple_path=BASE/'simplified-local-result.json'
    baseline=json.loads(baseline_path.read_text())
    simple=json.loads(simple_path.read_text())
    assert outcomes['published']['unweighted'][0]==Q(baseline['worst_dual_ratio'])
    assert outcomes['simple']['unweighted'][0]==Q(simple['worst_dual_ratio'])
    output={'status':'PASS_B_LOCAL_RECONCILIATION','scope':'Checks B retained weights only; A newly generated weights were not supplied and are not replayed.',
            'census':census,'branches':len(branches),'rows_in_every_branch':42,'distinct_row_keys':len(keys),
            'common_rows':len(common),'common_exact_rank':len(pivots),'common_nullity':len(kernel),
            'common_free_coordinates':free,'a_published_radii_equal_b':a_radii_match,
            'a_markdown_sha256':a_sha256,
            'fresh_b_signed_residuals_checked':check_count,
            'maximum_direct_residual_l1_upper':str(maximum_l1),
            'maximum_weighted_residual_eta_upper':list(map(str,maximum_eta)),
            'residual_polynomial_common_denominator':str(poly_den),'root_scale':str(root_scale),
            'configurations':{c:{m:{'value':str(v),'float':float(v),'at':at} for m,(v,at) in metrics.items()}
                              for c,metrics in outcomes.items()},
            'source_hashes':EXPECTED_SOURCE_SHA256,'weighted_sha256':dual.WEIGHTED_SHA,'focused_sha256':dual.FOCUSED_SHA,
            'checker_sha256':dual.digest(Path(__file__)),
            'seconds':time.monotonic()-start}
    output_dir=args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True,exist_ok=True)
    (output_dir/'reconciliation-local-check-results.json').write_text(json.dumps(output,indent=2)+'\n')
    dictionary={'field_polynomial':list(ir.trump11.U_MIN_POLY),
                'rows':[{ 'id':identifiers[k], 'coefficients':sparse_record(row_by_key[k]),
                         'common_to_all_branches':k in common,
                         'elementary_aliases':[list(f.subject) for f in aliases[k]],
                         'curvature':{c:str(bounds[c][k]) for c in bounds}}
                        for k in keys],
                'branches':[[identifiers[k] for k in b] for b in branches],
                'common_row_ids':[identifiers[k] for k in sorted(common)],
                'common_pivot_columns':pivots,'common_free_columns':free,
                'common_nullspace_basis':[sparse_record(v) for v in kernel]}
    (output_dir/'reconciliation-local-canonical-rows.json').write_text(json.dumps(dictionary,indent=2)+'\n')
    assert all(dual.digest(SOURCE/name)==sha for name,sha in EXPECTED_SOURCE_SHA256.items())
    assert dual.bound_sources()==sources
    assert dual.digest(BASE/'weighted.json')==dual.WEIGHTED_SHA
    assert dual.digest(BASE/'focused.json')==dual.FOCUSED_SHA
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
