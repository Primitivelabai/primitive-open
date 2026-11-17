"""Reproduce the Ohio weighted-quotient demonstration. Python 3 + NumPy.

Exact claims are checked in Ohio.lean. This is floating-point validation and
local timing, not a physical experiment or a quantum advantage claim.
"""
import os
for name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(name, "1")
import json
import math
import platform
import sys
import time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent

def model(n, coupling=0.37):
    start = time.perf_counter()
    states = np.arange(3**n, dtype=np.int64)
    n0 = np.zeros(len(states), dtype=np.int64)
    n1 = n0.copy()
    for i in range(n):
        d = states // (3**i) % 3
        n0 += d == 0
        n1 += d == 1
    cells = [(a,b,n-a-b) for a in range(n+1) for b in range(n-a+1)]
    lookup = {c:i for i,c in enumerate(cells)}
    table = np.zeros((n+1,n+1), dtype=np.int64)
    for j,(a,b,c) in enumerate(cells):
        table[a,b] = j
    labels = table[n0,n1]
    weights = np.array([math.factorial(n)//(math.factorial(a)*math.factorial(b)*math.factorial(c)) for a,b,c in cells])
    B = np.zeros((len(cells),len(cells)))
    for j,occ in enumerate(cells):
        B[j,j] = coupling*(occ[2]-occ[0])**2/n
        for a in range(3):
            if occ[a] == 0:
                continue
            for b in range(3):
                if a == b:
                    continue
                nxt = list(occ); nxt[a] -= 1; nxt[b] += 1
                B[lookup[tuple(nxt)],j] = math.sqrt(occ[a]*(occ[b]+1))
    diag = coupling*(n-n0-n1-n0)**2/n
    def full(v):
        t = v.reshape((3,)*n)
        out = diag*v
        for axis in range(n):
            # K3 adjacency, applied with tensor structure; no dense 3^n matrix.
            out += (np.sum(t,axis=axis,keepdims=True)-t).reshape(-1)
        return out
    def lift(y):
        return y[labels]/np.sqrt(weights[labels])
    def project(v):
        w = v/np.sqrt(weights[labels])
        return (np.bincount(labels,weights=w.real,minlength=len(cells)) +
                1j*np.bincount(labels,weights=w.imag,minlength=len(cells)))
    return cells, weights, labels, B, full, lift, project, (time.perf_counter()-start)*1000

def rk4(action, v, dt=0.002, steps=40):
    v = v.copy()
    for _ in range(steps):
        k1 = -1j*action(v)
        k2 = -1j*action(v+dt*k1/2)
        k3 = -1j*action(v+dt*k2/2)
        k4 = -1j*action(v+dt*k3)
        v += dt*(k1+2*k2+2*k3+k4)/6
    return v

def timed(fn,repeats=5):
    samples=[]
    for _ in range(repeats):
        t=time.perf_counter(); result=fn(); samples.append((time.perf_counter()-t)*1000)
    return result, samples, float(np.median(samples))

def main():
    rng=np.random.default_rng(20261117)
    result={"title":"Ohio weighted quotient and quantum evolution", "seed":20261117,
      "environment":{"python":sys.version,"numpy":np.__version__,"platform":platform.platform(),
      "processor":platform.processor(),"threads":{k:os.environ.get(k) for k in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS")}},
      "scope":"Synthetic symmetric Hamiltonian; timings are local warm kernel medians. RK4 is approximate; no hardware quantum run.",
      "benchmarks":[]}
    for n in [3,6,8,10]:
        cells,w,labels,B,H,lift,project,setup=model(n)
        y=rng.normal(size=len(cells))+1j*rng.normal(size=len(cells)); y/=np.linalg.norm(y)
        x=lift(y)
        assert sum(int(v) for v in w)==3**n
        assert np.allclose(B,B.T,atol=1e-14,rtol=0)
        residual=float(np.linalg.norm(H(x)-lift(B@y)))
        assert residual<1e-11
        # Warm each path once; same RK4 algorithm, dt, steps and initial state.
        rk4(H,x);rk4(lambda v:B@v,y)
        xf,tf,mf=timed(lambda:rk4(H,x))
        yr,tr,mr=timed(lambda:rk4(lambda v:B@v,y))
        err=float(np.linalg.norm(xf-lift(yr)))
        assert err<1e-10
        row={"n_trits":n,"full_dimension":3**n,"reduced_dimension":len(cells),
          "dimension_ratio":3**n/len(cells),"full_complex128_state_bytes":16*3**n,
          "reduced_complex128_state_bytes":16*len(cells),"shared_validation_setup_ms":setup,
          "intertwining_residual_l2":residual,"trajectory_difference_l2":err,
          "norm_drift_full":float(abs(np.linalg.norm(xf)-1)),
          "full_samples_ms":tf,"reduced_samples_ms":tr,"full_median_ms":mf,
          "reduced_median_ms":mr,"warm_kernel_ratio":mf/mr}
        result["benchmarks"].append(row)
        print(json.dumps(row),flush=True)
    # Dense, independent spectral solution at n=3 and multiple complex starts.
    cells,w,labels,B,H,lift,project,_=model(3)
    eye=np.eye(27,dtype=complex)
    A=np.column_stack([H(eye[:,i]) for i in range(27)])
    Q=np.column_stack([lift(np.eye(10)[:,i]) for i in range(10)])
    lam,V=np.linalg.eigh(A); mu,W=np.linalg.eigh(B)
    maxerr=0.; maxnorm=0.
    for _ in range(12):
        y=rng.normal(size=10)+1j*rng.normal(size=10); y/=np.linalg.norm(y)
        for t in np.linspace(0,10,81):
            x=V@(np.exp(-1j*t*lam)*(V.conj().T@lift(y)))
            z=W@(np.exp(-1j*t*mu)*(W.conj().T@y))
            maxerr=max(maxerr,float(np.linalg.norm(x-lift(z))))
            maxnorm=max(maxnorm,float(abs(np.linalg.norm(x)-1)))
    assert maxerr<1e-11
    result["spectral_validation"]={"initial_states":12,"times_per_state":81,"comparisons":972,
      "max_state_error_l2":maxerr,"max_norm_drift":maxnorm,
      "isometry_error":float(np.linalg.norm(Q.T@Q-np.eye(10))),
      "matrix_intertwining_error":float(np.linalg.norm(A@Q-Q@B))}
    # Symmetry-breaking diagonal that names the most significant trit.
    D=np.diag(np.arange(27)//9)
    Ab=A+0.7*D; Bb=Q.T@Ab@Q
    leakage=float(np.linalg.norm(Ab@Q-Q@Bb,ord=2))
    v=np.zeros(10,dtype=complex); v[cells.index((1,1,1))]=1
    la,va=np.linalg.eigh(Ab); lb,vb=np.linalg.eigh(Bb)
    t=1.0
    actual=va@(np.exp(-1j*t*la)*(va.conj().T@lift(v)))
    reduced=lift(vb@(np.exp(-1j*t*lb)*(vb.conj().T@v)))
    broken_error=float(np.linalg.norm(actual-reduced))
    assert leakage>0.1 and broken_error>0.1
    result["negative_control"]={"site_term_strength":0.7,"leakage_operator_norm":leakage,
      "time":t,"state_error_l2":broken_error,
      "meaning":"Reject exact reduction when the Hamiltonian distinguishes site identity."}
    # Nontrivial internal transport around a triangle: return of address != return of frame.
    theta=math.pi/3
    R=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    frames=[np.diag([2.,0.5]),np.array([[1.,1.],[0.,1.]]),np.diag([0.5,2.])]
    edges=[np.eye(2),np.eye(2),R]
    changed=[frames[(i+1)%3]@edges[i]@np.linalg.inv(frames[i]) for i in range(3)]
    loop=edges[2]@edges[1]@edges[0]
    loop_changed=changed[2]@changed[1]@changed[0]
    gauge_error=float(np.linalg.norm(loop_changed-frames[0]@loop@np.linalg.inv(frames[0])))
    assert gauge_error<1e-12
    result["transport"]={"closed_address_path":[0,1,2,0],"rotation_degrees":60,
      "frame_return_error":float(np.linalg.norm(loop-np.eye(2))),"gauge_covariance_error":gauge_error,
      "meaning":"Discrete transport example; no continuum manifold or measured physical curvature asserted."}
    result["scaling_formula"]=[{"n":n,"full":3**n,"symmetric":math.comb(n+2,2)} for n in [3,10,12,20]]
    (ROOT/"results.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("ALL_NUMERICAL_CHECKS_PASSED",flush=True)

if __name__=="__main__": main()
