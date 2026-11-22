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
    check_second_batch()
    check_third_batch()
    print("OK: chapters 01–15 mathematical experiments; no third-party packages")

def second_derivatives(xs,ys,clamped=False):
    n=len(xs)
    assert n>=2 and len(ys)==n
    h=[xs[i+1]-xs[i] for i in range(n-1)]
    assert all(v>0 for v in h)
    lower=[0.0]*n;diag=[1.0]*n;upper=[0.0]*n;rhs=[0.0]*n
    if clamped:
        diag[0]=2*h[0]; upper[0]=h[0]; rhs[0]=6*(ys[1]-ys[0])/h[0]
        lower[-1]=h[-1];diag[-1]=2*h[-1];rhs[-1]=-6*(ys[-1]-ys[-2])/h[-1]
    for i in range(1,n-1):
        lower[i]=h[i-1];diag[i]=2*(h[i-1]+h[i]);upper[i]=h[i]
        rhs[i]=6*((ys[i+1]-ys[i])/h[i]-(ys[i]-ys[i-1])/h[i-1])
    for i in range(1,n):
        factor=lower[i]/diag[i-1]
        diag[i]-=factor*upper[i-1]
        rhs[i]-=factor*rhs[i-1]
    M=[0.0]*n
    for i in range(n-1,-1,-1):
        M[i]=(rhs[i]-upper[i]*(M[i+1] if i+1<n else 0.0))/diag[i]
    return M

def natural_value_half(xs,ys,M):
    h=xs[1]-xs[0];x=(xs[0]+xs[1])/2;left=xs[1]-x;right=x-xs[0]
    return (M[0]*left**3+M[1]*right**3)/(6*h)+(ys[0]-M[0]*h*h/6)*left/h+(ys[1]-M[1]*h*h/6)*right/h

def cheb_integral(m,n,N=1024):
    dt=math.pi/N
    return dt*sum(math.cos(m*(k+.5)*dt)*math.cos(n*(k+.5)*dt) for k in range(N))

def check_second_batch():
    from fractions import Fraction as Q
    # 06: explicit natural and zero-clamped systems
    x=[0,1,2,3]; y=[0,1,0,1]
    natural=second_derivatives(x,y)
    clamped=second_derivatives(x,y,True)
    for a,b in zip(natural,[0,-4,4,0]):approx(a,b)
    for a,b in zip(clamped,[6,-6,6,-6]):approx(a,b)
    approx(natural_value_half(x,y,natural),.75)
    # 07: Chebyshev orthogonality avoids w(x) singular endpoints
    approx(cheb_integral(2,3),0,tol=1e-12)
    approx(cheb_integral(2,2),math.pi/2,tol=1e-12)
    # 08: exact L2 projection of x² onto span(1,x)
    def squared_error(c):return Q(2,5)-Q(4,3)*c+2*c*c
    assert squared_error(Q(1,3))==Q(8,45)
    assert squared_error(Q(1,2))==Q(7,30)
    assert squared_error(Q(1,2))-squared_error(Q(1,3))==Q(1,18)
    # 09: discrete least squares residuals orthogonal to [1,x]
    xs=[-1,0,1]; y=[1,0,2]; slope=.5;intercept=1.0
    residual=[yi-intercept-slope*xi for xi,yi in zip(xs,y)]
    for a,b in zip(residual,[.5,-1,.5]):approx(a,b)
    approx(sum(residual),0)
    approx(sum(a*b for a,b in zip(xs,residual)),0)
    approx(sum(a*a for a in residual),1.5)
    # 10: trapezoid precision 1, Simpson precision 3
    for k in range(5):
        f=lambda z:z**k
        exact=1/(k+1)
        T=(f(0)+f(1))/2
        S=(f(0)+4*f(.5)+f(1))/6
        if k<=1:approx(T,exact)
        if k<=3:approx(S,exact)
        if k==4:
            approx(S,Q(5,24))
            approx(exact,Q(1,5))
            approx(S-exact,Q(1,120))
    print("OK: chapters 06–10, spline boundaries, Chebyshev, Gram projection, LS, quadrature")


def romberg(f,a,b,levels=6):
    h=b-a
    row=[0.5*h*(f(a)+f(b))]
    table=[row[:]]
    for k in range(1,levels):
        n=2**(k-1)
        midpoint_sum=sum(f(a+(j+0.5)*h) for j in range(n))
        new=[0.5*row[0]+0.5*h*midpoint_sum]
        for j in range(1,k+1):
            new.append((4**j*new[j-1]-row[j-1])/(4**j-1))
        table.append(new[:])
        row=new
        h*=0.5
    return table

def gauss2(f):
    r=1/math.sqrt(3)
    return f(-r)+f(r)

def gauss3(f):
    r=math.sqrt(3/5)
    return (5/9)*f(-r)+(8/9)*f(0)+(5/9)*f(r)

def lu_factor_pp(A):
    n=len(A)
    U=[list(map(float,row)) for row in A]
    L=[[0.0]*n for _ in range(n)]
    P=[[float(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):L[i][i]=1.0
    for k in range(n):
        pivot=max(range(k,n),key=lambda i:abs(U[i][k]))
        if U[pivot][k]==0.0:raise ValueError("singular matrix")
        if pivot!=k:
            U[k],U[pivot]=U[pivot],U[k]
            P[k],P[pivot]=P[pivot],P[k]
            for j in range(k):
                L[k][j],L[pivot][j]=L[pivot][j],L[k][j]
        for i in range(k+1,n):
            m=U[i][k]/U[k][k]
            L[i][k]=m
            for j in range(k,n):U[i][j]-=m*U[k][j]
            U[i][k]=0.0
    return P,L,U

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def check_third_batch():
    import cmath
    # 11: composite trapezoid refinement and Romberg extrapolation
    table=romberg(math.exp,0.0,1.0,levels=6)
    exact=math.expm1(1.0)
    assert abs(table[-1][-1]-exact)<1e-12
    assert abs(table[1][1]-exact)<abs(table[1][0]-exact)
    # 12: n-point Gauss-Legendre exact through degree 2n-1
    for degree in range(4):
        f=lambda x,d=degree:x**d
        exact_poly=0.0 if degree%2 else 2/(degree+1)
        approx(gauss2(f),exact_poly,tol=1e-12)
    for degree in range(6):
        f=lambda x,d=degree:x**d
        exact_poly=0.0 if degree%2 else 2/(degree+1)
        approx(gauss3(f),exact_poly,tol=1e-12)
    # 13: central, Richardson and complex-step derivatives
    x=.7; h=1e-3; truth=math.cos(x)
    D=lambda step:(math.sin(x+step)-math.sin(x-step))/(2*step)
    approx(D(h),truth,tol=1e-6)
    rich=(4*D(h/2)-D(h))/3
    approx(rich,truth,tol=1e-10)
    cs=cmath.sin(x+1e-20j).imag/1e-20
    approx(cs,truth,tol=1e-14)
    five=(math.sin(x-2*h)-8*math.sin(x-h)+8*math.sin(x+h)-math.sin(x+2*h))/(12*h)
    approx(five,truth,tol=1e-10)
    # 14: Legendre P3 roots and the 3x3 Jacobi matrix spectrum
    def legendre(x,n):
        p0,p1=1.0,x
        if n==0:return p0
        for k in range(1,n):
            p0,p1=p1,((2*k+1)*x*p1-k*p0)/(k+1)
        return p1
    r=math.sqrt(3/5)
    for node in [-r,0.0,r]:approx(legendre(node,3),0,tol=1e-12)
    a1,a2=1/math.sqrt(3),2/math.sqrt(15)
    approx(math.sqrt(a1*a1+a2*a2),r)
    approx(5/9+8/9+5/9,2)
    # 15: partial-pivot LU convention P A = L U
    A=[[1e-20,1.0],[1.0,1.0]]
    P,L,U=lu_factor_pp(A)
    PA,LU=matmul(P,A),matmul(L,U)
    for i in range(2):
        for j in range(2):approx(PA[i][j],LU[i][j],tol=1e-12)
    assert abs(L[1][0])<=1.0 and abs(L[1][0])<1e-18
    assert abs(1.0/1e-20-1e20)<1e5
    try:lu_factor_pp([[1.0,2.0],[2.0,4.0]])
    except ValueError:pass
    else:raise AssertionError("singular pivot was not detected")
    print("OK: chapters 11–15, Romberg, Gauss rules, differentiation, Jacobi nodes, pivoted LU")

if __name__=="__main__":main()
