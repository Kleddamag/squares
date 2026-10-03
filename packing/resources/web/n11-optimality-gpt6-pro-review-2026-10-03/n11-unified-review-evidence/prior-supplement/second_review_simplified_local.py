#!/usr/bin/env python3
"""Second-review independent arithmetic of simplified local rectangle.

Shares original branch inventory and proposal data, but reconstructs elementary
values/gradients with independent Fraction field code, coverage, alias maxima,
radii, coarse curvature constants, residuals, and every final inequality.
"""

if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

from pathlib import Path
import sys, json, runpy, contextlib, io, itertools, time
from fractions import Fraction as Q
START=time.monotonic()
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'fresh-results'
OUTPUT.mkdir(parents=True, exist_ok=True)
BASE=ROOT/'local-isolation-audit'
sys.path[:0]=[str(BASE/'sq/packing'),str(BASE/'sq/packing/src')]
from cases.trump11 import isolation_radius as ir
with contextlib.redirect_stdout(io.StringIO()): ns=runpy.run_path(str(ROOT / 'independent_exact_witness.py'))
F=ns['F'];I=ns['I'];ieval=ns['ieval'];squares=ns['squares'];dot=ns['dot'];minus=ns['minus'];side=ns['T']

def key(g):return tuple(tuple(x.a)+(Q(0),)*(8-len(x.a)) for x in g)
def project_key(g):return tuple(tuple(x.coeffs) for x in g)

def J(v):return (-v[1],v[0])
def addv(a,b):return (a[0]+b[0],a[1]+b[1])
centres=[(sum((p[0] for p in sq),F(0))/4,sum((p[1] for p in sq),F(0))/4) for sq in squares]
witness=ir.load_witness()
assert len(witness.branches)==128
for ours,theirs in zip(squares,witness.squares,strict=True):
 for p,q in zip(ours,theirs,strict=True):
  assert key(p)==project_key(q)
branches={b['branch']:[project_key(row.coefficients) for row in b['rows']] for b in witness.branches}
assert set(branches)==set(range(128))
assert all(len(keys)==42 for keys in branches.values())
used=set(k for keys in branches.values() for k in keys)

# Independent reconstruction of scalar corner gap values and exact analytic derivatives.
functions=[]
for i,sq in enumerate(squares):
 for m,(x,y) in enumerate(sq):
  rx,ry=minus((x,y),centres[i])
  for wall,dimension,sgn,gval,dtheta in [('left',0,1,x,-ry),('right',0,-1,side-x,ry),('bottom',1,1,y,rx),('top',1,-1,side-y,-rx)]:
   grad=[F(0)]*33;grad[3*i+dimension]=F(sgn);grad[3*i+2]=dtheta
   functions.append({'kind':'wall','subject':(i,wall,m),'value':gval,'gradient':grad,'key':key(grad)})
for i in range(11):
 for j in range(i+1,11):
  for owner in (i,j):
   other=j if owner==i else i
   axes=[J(minus(squares[owner][k+1],squares[owner][k])) for k in (0,1)]
   for axnum,n in enumerate(axes):
    for order,positive in [('first-before-second',j),('second-before-first',i)]:
     eps=1 if other==positive else -1
     d=minus(centres[other],centres[owner]);Jn=J(n)
     for corner,p in enumerate(squares[other]):
      r=minus(p,centres[other]);grad=[F(0)]*33
      for k in (0,1):grad[3*other+k]=eps*n[k];grad[3*owner+k]=-eps*n[k]
      grad[3*other+2]=eps*dot(n,J(r))
      grad[3*owner+2]=eps*dot(Jn,addv(d,r))
      value=eps*dot(n,minus(p,centres[owner]))-Q(1,2)
      functions.append({'kind':'pair','subject':(i,j,owner,axnum,order,corner),'value':value,'gradient':grad,'key':key(grad)})
assert len(functions)==1936
# Independent feature/branch cover at the exact endpoint.
contacts=set(map(tuple,ns['out']['contact_pairs']))
assert contacts=={c.pair for c in witness.contacts} and len(contacts)==14
features={}
for f in functions:
 if f['kind']=='pair' and f['subject'][:2] in contacts:features.setdefault(f['subject'][:5],[]).append(f)
assert len(features)==112
available={};unavailable={}
for k,fs in features.items():
 assert len(fs)==4 and {f['subject'][-1] for f in fs}==set(range(4))
 signs=[f['value'].sgn() for f in fs]
 if min(signs)<0:unavailable[k]=fs
 else:
  assert min(signs)==0
  available[k]=tuple(sorted({f['key'] for f in fs if not f['value']}))
assert len(available)==24 and len(unavailable)==88
walls=tuple(sorted(f['key'] for f in functions if f['kind']=='wall' and not f['value']))
choices=[[rows for k,rows in available.items() if k[:2]==pair] for pair in sorted(contacts)]
matrices=set();raw=0
for selection in itertools.product(*choices):
 raw+=1;matrices.add(tuple(sorted(walls+tuple(row for choice in selection for row in choice))))
assert raw==512 and len(matrices)==128
assert matrices=={tuple(sorted(rows)) for rows in branches.values()}

proposal=json.load(open(BASE/'weighted.json'));focused=json.load(open(BASE/'focused.json'))
r=Q(1,256);radii=[r]*33;radii[29]=radii[32]=2*r
radii0=list(map(Q,focused['radii']))
assert len(radii0)==33 and all(0<a<=b<=Q(1,64) for a,b in zip(radii0,radii,strict=True))
assert {i for i,x in enumerate(radii) if x==2*r}=={29,32}
assert all(radii[3*i+k]==r for i in range(11) for k in (0,1))
# D = 3/2 is certified geometrically on the old analytic working box:
# true contact implies original centre distance <= sqrt2; displacements add <=sqrt2/32.
assert Q(33,32)**2*2 < Q(3,2)**2
for i,j in contacts:
 d=minus(centres[i],centres[j]);assert (F(2)-dot(d,d)).sgn()>=0
# Uniform translation speed ||v_other-v_owner|| <=2sqrt2*r <=3r.
assert Q(3,2)**2>=2 and Q(3,4)**2>=Q(1,2)
Ktable={(a,b):Q(3,2)*a*a+6*a+Q(3,4)*(a+b)**2 for a in (1,2) for b in (1,2)}
assert Ktable=={(1,1):Q(21,2),(1,2):Q(57,4),(2,1):Q(99,4),(2,2):Q(30)}

def curvature(f):
 if f['kind']=='wall':
  a=radii[3*f['subject'][0]+2]/r;return r*r*Q(3,4)*a*a
 i,j,owner=f['subject'][:3];other=j if owner==i else i
 a=radii[3*owner+2]/r;b=radii[3*other+2]/r
 return r*r*Ktable[a,b]

aliases={}
for f in functions:
 if not f['value'] and f['key'] in used:aliases.setdefault(f['key'],[]).append(f)
assert set(aliases)==used
rowK={k:max(map(curvature,fs)) for k,fs in aliases.items()}
neededpairs={f['subject'][:2] for fs in aliases.values() for f in fs if f['kind']=='pair'}
# Audit an identity of translation support: pair aliases never introduce a new pair.
for k,fs in aliases.items():
 p={f['subject'][:2] for f in fs if f['kind']=='pair'}
 if p:
  assert len(p)==1 and all(f['kind']=='pair' for f in fs)

intervals={}
def interval_poly(coeffs):
 if coeffs not in intervals:intervals[coeffs]=ieval(coeffs,I)
 return intervals[coeffs]
def interval(f):return interval_poly(tuple(f.a))

negative=[];seen=set();minmargin=None;minfeature=None
for record in proposal['unavailable_feature_proofs']:
 k=tuple(record['feature']);corner=record['negative_corner']
 assert k in unavailable and k not in seen;seen.add(k)
 assert type(corner) is int and corner in range(4)
 f=next(v for v in unavailable[k] if v['subject'][-1]==corner)
 neededpairs.add(f['subject'][:2])
 v=interval(f['value'])[1];assert v<0
 linear=sum(max(abs(l),abs(h))*rad for (l,h),rad in zip(map(interval,f['gradient']),radii,strict=True))
 margin=-v-linear-curvature(f)/2
 assert margin>0
 if minmargin is None or margin<minmargin:minmargin,minfeature=margin,f['subject']
 negative.append(margin)
assert len(negative)==88 and seen==set(unavailable) and neededpairs==contacts

# Reconstruct coefficient approximations and every residual, independently of
# check_coarse_radii.py or the dual checker's integer/residual routines.
den=proposal['coefficient_denominator'];scale=proposal['matrix_approximation_denominator']
assert type(den) is int and den>0 and type(scale) is int and scale>0
matrixrowcache={}
for k in used:
 row=[]
 for coeffs in k:
  l,h=interval_poly(coeffs);q=round((l+h)*scale/2)
  assert Q(q-1,scale)<=l<=h<=Q(q+1,scale)
  row.append(q)
 matrixrowcache[k]=row
certbranches={b['branch']:b for b in proposal['branches']}
assert len(certbranches)==128 and set(certbranches)==set(range(128))
count=0;worst=Q(0);worst_at=None;maxres=Q(0)
for b,keys in branches.items():
 A=[matrixrowcache[k] for k in keys];ks=[rowK[k] for k in keys];seen=set()
 certs=certbranches[b]['certificates'];assert len(certs)==66
 for cert in certs:
  j,sign=cert['coordinate'],cert['sign'];assert type(j) is int and 0<=j<33 and type(sign) is int and sign in (-1,1)
  assert (j,sign) not in seen;seen.add((j,sign))
  ws=cert['coefficients'];assert len(ws)==42 and all(type(w) is int and w>=0 for w in ws) and sum(ws)>0
  nz=[(i,w) for i,w in enumerate(ws) if w]
  residual=sum(abs(sum(w*A[i][column] for i,w in nz)-(sign*den*scale if column==j else 0)) for column in range(33))
  err=Q(residual,den*scale)+Q(33*sum(ws),den*scale)
  assert 0<=err<1 and err==Q(cert['residual_upper'])
  mass=sum(Q(w,den)*ks[i] for i,w in nz)
  threshold=2*(radii[j]-err*max(radii));assert 0<mass<threshold
  ratio=mass/threshold
  if ratio>worst:worst,worst_at=ratio,(b,j,sign)
  maxres=max(maxres,err);count+=1
 assert seen==set(itertools.product(range(33),(-1,1)))
assert count==8448
recorded=json.load(open(ROOT/'recorded-results/simplified-local-result.json'))
assert Q(recorded['worst_dual_ratio'])==worst
result={'status':'PASS_SECOND_REVIEW_SIMPLIFIED_LOCAL','scope':'New simplified local box/constants only; original shared branch inventory retained','original_rectangle_nested':True,'enlarged_angle_coordinates':[29,32],'enlarged_square_indices':[9,10],'working_box':'1/64','radii':list(map(str,radii)),'pair_K_over_r2':{str(k):str(v) for k,v in Ktable.items()},'wall_K_over_r2':['3/4','3'],'all_elementary_functions_reconstructed':len(functions),'available_features':len(available),'unavailable_features':len(unavailable),'raw_branch_selections':raw,'distinct_branches':len(matrices),'distinct_row_gradients':len(used),'matched_tied_elementary_functions':sum(map(len,aliases.values())),'row_alias_groups_with_multiple_functions':sum(len(fs)>1 for fs in aliases.values()),'needed_pairs':sorted(neededpairs),'negative_features_checked':len(negative),'smallest_negative_margin':str(minmargin),'smallest_negative_margin_float':float(minmargin),'smallest_negative_feature':minfeature,'independent_residuals_and_dual_margins_checked':count,'maximum_residual':str(maxres),'worst_ratio':str(worst),'worst_ratio_float':float(worst),'worst_at':worst_at,'seconds':time.monotonic()-START}
(OUTPUT / 'second-review-simplified-local-result.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ('smallest_negative_margin','radii')},indent=2))
