#!/usr/bin/env python3

if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

import runpy,contextlib,io,math,json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fresh-results"
OUTPUT.mkdir(parents=True, exist_ok=True)
with contextlib.redirect_stdout(io.StringIO()): ns=runpy.run_path(str(ROOT / 'independent_exact_witness.py'))
R=ns['R'];trim=ns['trim'];add=ns['add'];sub=ns['sub'];mul=ns['mul'];divmodp=ns['divmodp'];P=ns['P']
def gcd(a,b):
 while b!=[0]:a,b=b,divmodp(a,b)[1]
 return [x/a[-1] for x in a]
class RF:
 def __init__(self,n=0,d=1):
  if isinstance(n,RF):self.n,self.d=n.n,n.d;return
  n=trim(n if isinstance(n,(tuple,list)) else [n]);d=trim(d if isinstance(d,(tuple,list)) else [d])
  g=gcd(n,d);n=divmodp(n,g)[0];d=divmodp(d,g)[0];L=d[-1]
  self.n=[x/L for x in n];self.d=[x/L for x in d]
 def __add__(self,o):
  o=RF(o);return RF(add(mul(self.n,o.d),mul(o.n,self.d)),mul(self.d,o.d))
 __radd__=__add__
 def __neg__(self):return RF([-x for x in self.n],self.d)
 def __sub__(self,o):return self+-RF(o)
 def __rsub__(self,o):return RF(o)+-self
 def __mul__(self,o):
  o=RF(o);return RF(mul(self.n,o.n),mul(self.d,o.d))
 __rmul__=__mul__
 def __truediv__(self,o):
  o=RF(o);return RF(mul(self.n,o.d),mul(self.d,o.n))
 def __rtruediv__(self,o):return RF(o)/self
 def __pow__(self,n):
  z=RF(1)
  for _ in range(n):z=z*self
  return z
 def __repr__(self):return f'{self.n} / {self.d}'
u=RF([0,1]);T=(6*u+4)/(1+2*u-u*u);c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
rho=1-(T-3)*c;eta=((1+rho)*c-1)/s;v=c-s;zeta=(T-1)/s-rho-(3+eta)*c/s;x0=1+2/c-(T-2)*s/c
# Oriented projection gap: square 10 to square 2 along (-s,c).
g=-s*x0+c*T-2*c+zeta+rho-1
expected_gap=RF(P)/(2*u*(1-u**4)*(1+2*u-u*u))
assert (g-expected_gap).n==[0], "contact closure rational-function identity failed"
print('gap numerator',g.n);print('gap denominator',g.d)
print('gap numerator divided by defining P:',divmodp(g.n,P))
print('den / (u*(u-1)*(u+1)*(u*u+1)*(u*u-2*u-1))',g/(RF(P)/(u*(u-1)*(u+1)*(u*u+1)*(u*u-2*u-1))))
# Other contact gaps indicated by exact check. Reconstruct all rational functions
# without imposing P, select projections using certified field specialization.
def A(a,b):return [(RF(a)+dx,RF(b)+dy) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
def F(pt):
 x,y=pt;return 1+c*x-s*(y-rho),1+s*x+c*(y-rho)
squares=[A(0,0),A(T-1,0),A(x0,T-1),A(0,T-1),A(1,T-1),A(0,T-2)]+[[F(pt) for pt in A(a,b)] for a,b in ((0,0),(eta,-1),(1,v),(eta+1,v-1),(eta+2,-zeta))]
axes=[(RF(1),RF(0)),(RF(0),RF(1)),(c,s),(-s,c)]
Field=ns['F']
def specialize(x):return Field(x.n)/Field(x.d)
def extrema(vs):
 lo=hi=vs[0]
 for z in vs[1:]:
  if specialize(z-lo).sgn()<0:lo=z
  if specialize(z-hi).sgn()>0:hi=z
 return lo,hi
pr=[[extrema([pt[0]*ax[0]+pt[1]*ax[1] for pt in pts]) for ax in axes] for pts in squares]
D=json.load(open(OUTPUT / 'independent-exact-witness-result.json'))
identities=[]
for z in D['pair_results']:
 if not z['contact']:continue
 i,j=z['pair']
 for cert in z['certificates']:
  k=cert['axis'];mi,Ma=pr[i][k];mj,Mb=pr[j][k]
  gap=mj-Ma if cert['order']==f'{i}<{j}' else mi-Mb
  rec={'pair':[i,j],'axis':k,'zero_identically_in_u':gap.n==[0],'numerator':list(map(str,gap.n)),'denominator':list(map(str,gap.d))}
  identities.append(rec);print(rec)
assert len(identities)==16
nonautomatic=[v for v in identities if not v['zero_identically_in_u']]
assert len(nonautomatic)==1 and nonautomatic[0]['pair']==[2,10] and nonautomatic[0]['axis']==3
with open(OUTPUT / 'independent-witness-symbolic-contacts.json','w') as f:json.dump(identities,f,indent=2)
print('ALL SYMBOLIC CONTACT IDENTITIES PASS')
