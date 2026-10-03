#!/usr/bin/env python3

if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fresh-results"
OUTPUT.mkdir(parents=True, exist_ok=True)
prime=29
P=[-6865,12420,-6754,-496,1923,-842,178,-20,1]
def trim(a):
 a=[x%prime for x in a]
 while len(a)>1 and a[-1]==0:a.pop()
 return a
P=trim(P)
def sub(a,b):
 c=[0]*max(len(a),len(b))
 for i,x in enumerate(a):c[i]+=x
 for i,x in enumerate(b):c[i]-=x
 return trim(c)
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def div(a,b):
 a=trim(a);b=trim(b);q=[0]*max(1,len(a)-len(b)+1)
 while a!=[0] and len(a)>=len(b):
  d=len(a)-len(b);z=(a[-1]*pow(b[-1],-1,prime))%prime;q[d]=z
  a=sub(a,[0]*d+[(z*x)%prime for x in b])
 return trim(q),a
def mod(a):return div(a,P)[1]
def power(a,n):
 z=[1]
 while n:
  if n&1:z=mod(mul(z,a))
  a=mod(mul(a,a));n>>=1
 return z
def gcd(a,b):
 while b!=[0]:a,b=b,div(a,b)[1]
 return trim([x*pow(a[-1],-1,prime) for x in a])
x=[0,1]
f4=power(x,prime**4);f8=power(x,prime**8)
g=gcd(P,sub(f4,x))
assert g==[1] and f8==x
out={'prime':prime,'degree':8,'x_to_p4_mod_P':f4,'gcd_P_x_to_p4_minus_x':g,'x_to_p8_mod_P':f8,'irreducible_mod_29':True,'irreducible_over_Q':True}
with open(OUTPUT / 'independent-side-irreducibility-result.json','w') as f:json.dump(out,f,indent=2)
print(out)
