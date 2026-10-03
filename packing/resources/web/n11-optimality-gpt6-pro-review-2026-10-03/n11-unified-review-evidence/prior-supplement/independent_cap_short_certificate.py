#!/usr/bin/env python3
"""Reproduce the compact rational cap certificate originally checked interactively."""
if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')
from fractions import Fraction as F
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'fresh-results'
OUTPUT.mkdir(parents=True, exist_ok=True)
p=[-1,2,2,-6,12,14,-2,-10,5]
def ev(x):
    z=F(0)
    for a in reversed(p):
        z=z*x+a
    return z
lo=F(36576930760467729338,10**20)
hi=F(36576930760467729339,10**20)
cap=F(387708359002281417731,10**20)
Thi=(6*hi+4)/(1+2*hi-hi*hi)
assert ev(lo)<0<ev(hi)
# The broad-interval uniqueness proof is also repeated here, so the short
# bracket identifies the same root without reliance on a saved success flag.
a,b=F(9,25),F(37,100)
assert a<lo<hi<b and ev(a)<0<ev(b)
dp_lower=40*a**7-70*b**6-12*b**5+70*a**4+48*a**3-18*b**2+4*a+2
assert dp_lower>4
assert 1+2*a-b*b>0 and 6*a*a+8*a-2>0
assert cap-Thi>0
out={'u_lower':str(lo),'u_upper':str(hi),'P_lower':str(ev(lo)),'P_upper':str(ev(hi)),'U_minus_T_upper':str(cap-Thi)}
(OUTPUT/'independent-cap-short-certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
