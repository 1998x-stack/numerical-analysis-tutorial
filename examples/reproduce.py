#!/usr/bin/env python3
"""Five deterministic mathematical checks for the first chapter batch. Python >=3.9, standard library only."""
import math
import sys

def approx(a,b,tol=1e-11):
    assert math.isclose(a,b,rel_tol=tol,abs_tol=tol),(a,b)

def lagrange(xs,ys,x):
    assert len(xs)==len(ys)>0 and len(set(xs))==len(xs)
    total=0.0
    for i,xi in enumerate(xs):
        t=ys[i]
        for j,xj in enumerate(xs):
            if j!=i:t*=(x-xj)/(xi-xj)
        total+=t
    return total

def divided_differences(xs,ys):
    assert len(xs)==len(ys)>0 and len(set(xs))==len(xs)
    a=list(map(float,ys)); n=len(xs); cs=[a[0]]
    for j in range(1,n):
        for i in range(n-j):
            a[i]=(a[i+1]-a[i])/(xs[i+j]-xs[i])
        cs.append(a[0])
    return cs

def newton_eval(xs,cs,x):
    r=cs[-1]
    for i in range(len(cs)-2,-1,-1):
        r=cs[i]+(x-xs[i])*r
    return r

def newton_append(xs,cs,xnew,ynew):
    assert xnew not in xs
    prod=1.0
    for x in xs:prod*=xnew-x
    return cs+[(ynew-newton_eval(xs,cs,xnew))/prod]

def hermite_segment(x0,x1,y0,y1,m0,m1,x):
    h=x1-x0; assert h>0
    t=(x-x0)/h
    return (2*t**3-3*t**2+1)*y0+(t**3-2*t**2+t)*h*m0+(-2*t**3+3*t**2)*y1+(t**3-t**2)*h*m1

def pchip_internal(hleft,hright,dleft,dright):
    if dleft*dright<=0:return 0.0
    w1=2*hright+hleft;w2=hright+2*hleft
    return (w1+w2)/(w1/dleft+w2/dright)

def main():
    # 01: absolute vs relative scale
    approx(abs(100.01-100.0)/100.0,0.0001)
    approx(abs(0.03-0.02)/0.02,0.5)
    # 02: rationalized small root avoids catastrophic cancellation
    a=1e9
    unstable=(a-math.sqrt(a*a-4))/2
    stable=2/(a+math.sqrt(a*a-4))
    assert unstable==0.0
    approx(stable,1e-9)
    # 03: polynomial x²+1 in barycentric basis
    xs=[-1.0,0.0,1.0]; ys=[2.0,1.0,2.0]
    for x in [-1.,-.5,0.,.5,1.]:
        approx(lagrange(xs,ys,x),x*x+1)
    # 04: Newton coefficients [1,1,1] for f(x)=x²+1 at 0,1,2
    xs=[0.,1.,2.]; ys=[1.,2.,5.]
    cs=divided_differences(xs,ys)
    assert cs==[1.0,1.0,1.0],cs
    for x in [0.,.4,1.5,2.,3.]:approx(newton_eval(xs,cs,x),x*x+1)
    updated=newton_append(xs,cs,3.,10.)
    approx(updated[-1],0.0)
    # 05: Hermite endpoint values and slopes
    approx(hermite_segment(0,1,0,1,2,0,0),0)
    approx(hermite_segment(0,1,0,1,2,0,1),1)
    h=1e-6
    approx((hermite_segment(0,1,0,1,2,0,h)-hermite_segment(0,1,0,1,2,0,-h))/(2*h),2,tol=1e-9)
    approx((hermite_segment(0,1,0,1,2,0,1+h)-hermite_segment(0,1,0,1,2,0,1-h))/(2*h),0,tol=1e-9)
    m=pchip_internal(1,1,1,.4)
    assert 0<m<1
    print("OK: 5 chapter experiments; no third-party packages")
if __name__=="__main__":main()
