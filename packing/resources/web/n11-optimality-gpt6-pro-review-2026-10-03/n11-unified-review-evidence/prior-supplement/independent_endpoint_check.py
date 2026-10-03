if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

from fractions import Fraction as F
from decimal import Decimal,getcontext
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fresh-results"
OUTPUT.mkdir(parents=True, exist_ok=True)
co=[5,-10,-2,14,12,-6,2,2,-1]
def value(co,x):
 v=F(0)
 for c in co:v=v*x+c
 return v
def interval(co,l,r):
 lo=hi=F(0)
 for c in co:
  ps=[lo*l,lo*r,hi*l,hi*r];lo=min(ps)+c;hi=max(ps)+c
 return lo,hi
l,r=F(9,25),F(37,100)
assert value(co,l)<0<value(co,r)
dco=[c*(len(co)-1-i) for i,c in enumerate(co[:-1])]
dlo,dhi=interval(dco,l,r);assert dlo>0
# T(u) increasing because derivative numerator 6u²+8u−2>0 in this interval.
assert 6*l*l+8*l-2>0 and 1+2*l-r*r>0
for _ in range(160):
 m=(l+r)/2
 if value(co,m)<0:l=m
 else:r=m
T=lambda u:(6*u+4)/(1+2*u-u*u)
U=F(387708359002281417731,10**20)
tl,tr=T(l),T(r);assert tr<U
getcontext().prec=70
fmt=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
report={'polynomial_derivative_bound_over_initial_interval':[str(dlo),str(dhi)],'unique_u_interval_decimal':[fmt(l),fmt(r)],'T_interval_decimal':[fmt(tl),fmt(tr)],'U_minus_T_interval_decimal':[fmt(U-tr),fmt(U-tl)],'verified_T_lt_U':True}
(OUTPUT / 'independent-endpoint-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
