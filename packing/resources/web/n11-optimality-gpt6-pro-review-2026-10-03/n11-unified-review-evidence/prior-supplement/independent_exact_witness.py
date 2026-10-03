#!/usr/bin/env python3
"""Independent witness reconstruction; uses only Python stdlib Fraction, no project code."""

if not __debug__:
    raise RuntimeError('This mathematical checker refuses optimized Python (-O/-OO).')

from fractions import Fraction as R
from decimal import Decimal, localcontext
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fresh-results"
OUTPUT.mkdir(parents=True, exist_ok=True)
from functools import cmp_to_key

# Polynomials ascending, over Q.
def trim(a):
    a=list(map(R,a))
    while len(a)>1 and not a[-1]:a.pop()
    return a

def add(a,b):
    r=[R(0)]*max(len(a),len(b))
    for i,x in enumerate(a):r[i]+=x
    for i,x in enumerate(b):r[i]+=x
    return trim(r)

def neg(a):return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    r=[R(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]+=x*y
    return trim(r)

def divmodp(a,b):
    a=trim(a);b=trim(b)
    if b==[0]:raise ZeroDivisionError
    q=[R(0)]*max(1,len(a)-len(b)+1)
    while a!=[0] and len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]/b[-1];q[k]=c
        for i,x in enumerate(b):a[i+k]-=c*x
        a=trim(a)
    return trim(q),a

P=list(map(R,[-1,2,2,-6,12,14,-2,-10,5]))

def rem(a):return divmodp(a,P)[1]
def inv(a):
    r0,r1=P,trim(a);s0,s1=[R(0)],[R(1)]
    while r1!=[0]:
        q,r2=divmodp(r0,r1);r0,r1=r1,r2;s0,s1=s1,sub(s0,mul(q,s1))
    assert len(r0)==1 and r0[0]
    return rem([x/r0[0] for x in s0])

def peval(a,x):
    r=R(0)
    for c in reversed(a):r=r*x+c
    return r

def ieval(a,I):
    z=(R(0),R(0))
    for c in reversed(a):
        prods=[x*y for x in z for y in I]
        z=(min(prods)+c,max(prods)+c)
    return z

lo,hi=R(9,25),R(37,100)
root_endpoints=[str(peval(P,lo)),str(peval(P,hi))]
assert peval(P,lo)<0<peval(P,hi)
DP=[i*P[i] for i in range(1,len(P))]
# A coarser termwise derivative interval is often clearer in a printed proof.
dp_lo=sum(c*(lo if c>=0 else hi)**i for i,c in enumerate(DP))
dp_hi=sum(c*(hi if c>=0 else lo)**i for i,c in enumerate(DP))
assert dp_lo>4
for _ in range(300):
    m=(lo+hi)/2
    if peval(P,m)<0:lo=m
    else:hi=m
I=(lo,hi)

class F:
    __slots__=('a',)
    def __init__(self,x=0):
        if isinstance(x,F):self.a=x.a
        else:self.a=tuple(rem(x if isinstance(x,(tuple,list)) else [R(x)]))
    def __add__(self,o):return F(add(self.a,F(o).a))
    __radd__=__add__
    def __neg__(self):return F(neg(self.a))
    def __sub__(self,o):return self+-F(o)
    def __rsub__(self,o):return F(o)+-self
    def __mul__(self,o):return F(mul(self.a,F(o).a))
    __rmul__=__mul__
    def __truediv__(self,o):return F(mul(self.a,inv(F(o).a)))
    def __rtruediv__(self,o):return F(o)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        v=F(1)
        for _ in range(n):v=v*self
        return v
    def sgn(self):
        if self.a==(0,):return 0
        L,H=ieval(self.a,I)
        if L>0:return 1
        if H<0:return -1
        raise ArithmeticError('Could not certify sign at fixed 300-step root bracket')
    def dec(self,n=70):
        with localcontext() as ctx:
            ctx.prec=n
            q=peval(self.a,(lo+hi)/2)
            return str(Decimal(q.numerator)/Decimal(q.denominator))
    def __bool__(self):return self.a!=(0,)

u=F([0,1]);T=(6*u+4)/(1+2*u-u*u);c=(1-u*u)/(1+u*u);s=2*u/(1+u*u)
rho=1-(T-3)*c;eta=((1+rho)*c-1)/s;v=c-s;zeta=(T-1)/s-rho-(3+eta)*c/s;x0=1+2/c-(T-2)*s/c
for x in [c,s,1+u*u,1+2*u-u*u]:assert x.sgn()>0
assert not c*c+s*s-1
SP=[-6865,12420,-6754,-496,1923,-842,178,-20,1]
polT=F(0)
for coeff in reversed(SP):polT=polT*T+coeff
assert not polT
assert not T-(2+(2+s)/(c+s))
U=F(R(387708359002281417731,10**20));assert (U-T).sgn()>0

def A(a,b):
    return [(F(a)+dx,F(b)+dy) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
def transform(pt):
    x,y=pt
    return (1+c*x-s*(y-rho),1+s*x+c*(y-rho))

squares=[A(0,0),A(T-1,0),A(x0,T-1),A(0,T-1),A(1,T-1),A(0,T-2)]
squares += [[transform(pt) for pt in A(a,b)] for a,b in ((0,0),(eta,-1),(1,v),(eta+1,v-1),(eta+2,-zeta))]
assert len(squares)==11
names=['A(0,0)','A(T-1,0)','A(x0,T-1)','A(0,T-1)','A(1,T-1)','A(0,T-2)','F A(0,0)','F A(eta,-1)','F A(1,v)','F A(eta+1,v-1)','F A(eta+2,-zeta)']

def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def minus(a,b):return (a[0]-b[0],a[1]-b[1])
def extrema(vs):
    M=m=vs[0]
    for z in vs[1:]:
        if (z-m).sgn()<0:m=z
        if (z-M).sgn()>0:M=z
    return m,M

# Verify unit geometry without assuming that construction routine did it right.
unit_checks=0
for pts in squares:
    edges=[minus(pts[(i+1)%4],pts[i]) for i in range(4)]
    for i in range(4):
        assert not dot(edges[i],edges[i])-1;unit_checks+=1
        assert not dot(edges[i],edges[(i+1)%4]);unit_checks+=1
    assert all(not x for x in (edges[0][0]+edges[2][0],edges[0][1]+edges[2][1],edges[1][0]+edges[3][0],edges[1][1]+edges[3][1]))

wall_contacts=[];margins=[]
for i,pts in enumerate(squares):
    for j,(x,y) in enumerate(pts):
        for wall,gap in [('L',x),('R',T-x),('B',y),('T',T-y)]:
            sig=gap.sgn();assert sig>=0
            if not sig:wall_contacts.append([i,j,wall])
            else:margins.append(gap)

# Exhaust all pair relations in axes e_x,e_y,(c,s),(-s,c), valid separating axes
# independently of which are edge normals; at least the appropriate normals occur.
axes=[(F(1),F(0)),(F(0),F(1)),(c,s),(-s,c)]
projections=[[extrema([dot(pt,ax) for pt in pts]) for ax in axes] for pts in squares]
pair_results=[]
for i in range(11):
    for j in range(i+1,11):
        certs=[]
        for k in range(4):
            mi,Ma=projections[i][k];mj,Mb=projections[j][k]
            for order,gap in [(f'{i}<{j}',mj-Ma),(f'{j}<{i}',mi-Mb)]:
                sig=gap.sgn()
                if sig>=0:certs.append({'axis':k,'order':order,'gap_sign':sig,'gap':gap.dec(35)})
        assert certs,(i,j)
        pair_results.append({'pair':[i,j],'contact':not any(z['gap_sign'] for z in certs),'certificates':certs})
assert len(pair_results)==55
xmin,xmax=extrema([p[0] for pts in squares for p in pts]);ymin,ymax=extrema([p[1] for pts in squares for p in pts])
assert not xmin and not ymin and not xmax-T and not ymax-T

out={
 'method':'independent stdlib Fraction quotient ring and rational interval signs; no imported project code',
 'root_polynomial_ascending':list(map(str,P)),
 'root_interval_start':['9/25','37/100'],
 'root_polynomial_at_endpoints':root_endpoints,
 'derivative_termwise_lower':str(dp_lo),'derivative_termwise_upper':str(dp_hi),
 'root_bisections':300,'root_bracket':list(map(str,I)),
 'constants':{k:x.dec() for k,x in [('u',u),('T',T),('c',c),('s',s),('rho',rho),('eta',eta),('v',v),('zeta',zeta),('x0',x0),('U-T',U-T)]},
 'side_polynomial_zero':True,'rotation_identity_zero':True,
 'unit_geometry_checks':unit_checks,
 'vertex_count':44,'containment_scalar_inequalities':176,
 'nonzero_wall_margin_min':extrema(margins)[0].dec(40),
 'wall_contacts_zero_indexed':wall_contacts,
 'pair_count':55,
 'contact_pair_count':sum(z['contact'] for z in pair_results),
 'contact_pairs':[z['pair'] for z in pair_results if z['contact']],
 'pair_results':pair_results,
 'span_x_equals_T':True,'span_y_equals_T':True,
 'squares':[{'index':i,'name':names[i],'vertices':[[x.dec(30),y.dec(30)] for x,y in pts]} for i,pts in enumerate(squares)]
}
with open(OUTPUT / 'independent-exact-witness-result.json','w') as f:json.dump(out,f,indent=2)
for key in ['constants','derivative_termwise_lower','unit_geometry_checks','vertex_count','containment_scalar_inequalities','nonzero_wall_margin_min','wall_contacts_zero_indexed','pair_count','contact_pair_count','contact_pairs','span_x_equals_T','span_y_equals_T']:print(key,out[key])
print('ALL INDEPENDENT EXACT CHECKS PASS')
