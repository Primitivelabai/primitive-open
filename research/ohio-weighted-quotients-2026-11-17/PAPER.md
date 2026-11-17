# Ohio: weighted quotients, exact evolution and coordinate transport

**Primitive Labs · Research note v1.0 · 17 November 2026 (Perth)**  
Prepared with ChatGPT/Codex from Josh's Ohio research direction.  
**Status: computational demonstration with 18 Lean-checked finite/algebraic theorems; not peer reviewed.**

## Abstract

We give a concrete mathematical bridge from a finite ternary state model to symmetry-reduced evolution and discrete coordinate transport. Permuting three ternary positions partitions 27 configurations into 10 occupancy classes. The class weights are essential: they preserve sums of all class-invariant complex observables, and their square roots normalize an amplitude basis. For the three-trit adjacency operator, an exact incidence-matrix intertwining identity and its Gram matrix are checked in Lean. Separate general Lean theorems establish preservation through arbitrary finite admissible control sequences, all natural matrix powers, Hermitian compression, Gram matrices, unitary restriction, rebasing, and cancellation of intermediate transport frames.

A reproducible NumPy experiment extends the construction to a permutation-symmetric interacting Hamiltonian. At ten trits, 59,049 amplitudes reduce to 66. A local warm RK4 kernel takes 455.815 ms versus 1.401 ms (325.33×), with a full-versus-lifted trajectory difference of 5.36e-16 in Euclidean norm. The comparison excludes setup and expansion, and is against a matrix-free tensor implementation, not an existing symmetry-reduced solver. An independent eigendecomposition path gives 972 three-trit comparisons with maximum state error 3.60e-14. A named-site perturbation produces error 0.3166 at time one, correctly rejecting exact symmetry reduction.

The contribution is a scoped implementation and verification package using established mathematics. It is not a new quantum theory, a universal compressor, or evidence of quantum computational advantage.

## 1. The core object

Let X_n={0,1,2}^n. The symmetric group S_n acts by permuting positions. Its orbits are the occupancy triples

```math
c=(n_0,n_1,n_2), \qquad n_0+n_1+n_2=n.
```

There are binomial(n+2,2) such triples, and each has weight

```math
w(c)=\frac{n!}{n_0!n_1!n_2!}.
```

The dimension formula and multinomial expression follow from standard counting. Their general-n derivations are given here mathematically; the Lean fixture enumerates n=3.

| n | Full configurations / amplitudes | Symmetric amplitude dimension | Status in this package |
|---:|---:|---:|---|
| 3 | 27 | 10 | Finite Lean fixture and numerical evolution |
| 6 | 729 | 28 | Numerical benchmark |
| 8 | 6,561 | 45 | Numerical benchmark |
| 10 | 59,049 | 66 | Numerical benchmark |
| 12 | 531,441 | 91 | Formula only |
| 20 | 3,486,784,401 | 231 | Formula only; no large full-state run |

These dimensions describe the permutation-invariant subspace, not every possible vector in the full Hilbert space. No claim is made that 231 arbitrary complex numbers losslessly encode 3.49 billion arbitrary complex numbers.

## 2. Measure: why the weights cannot disappear

Write pi:X_3→C for the orbit map. For any f:C→C (complex-valued),

```math
\sum_{x\in X_3} f(\pi(x))=\sum_{c\in C} w(c)f(c).
```

Proof: partition the left sum into its disjoint fibres; f is constant within each fibre, which contains w(c) elements. The implementation proves this for every complex function of the class code, not merely a sampled observable: **Ohio.weighted_sum**.

For n=3 there are three weight-one classes, six weight-three classes and one weight-six class. Their total weight is 27. For f(x)=(x_1+x_2+x_3)^2, full summation and weighted class summation both give 297; unweighted class summation gives 120. These values and the histogram are checked by Lean.

This is the discrete measure-preservation lesson suggested by the cylindrical-integration animation [1]. It is not an assertion that orbit multiplicity is literally a coordinate Jacobian.

## 3. From incidence to amplitudes

Let S be the 27-by-10 incidence matrix: S(x,c)=1 when pi(x)=c and zero otherwise. Let W=diag(w(c)). Then

```math
S^T S=W,\qquad Q=SW^{-1/2},\qquad Q^\dagger Q=I.
```

Thus Q is an isometric embedding. Its c-th column is the normalized orbit state

```math
|c\rangle=\frac{1}{\sqrt{w(c)}}\sum_{x\in c}|x\rangle.
```

The concrete natural-number identity S^T S=W is Lean theorem **Ohio.concrete_gram**. The square-root normalization argument is an explicit mathematical derivation here, also checked numerically, but is not instantiated as a concrete complex matrix in the Lean file. The general implication from Q†Q=I to Gram preservation is Lean theorem **Ohio.isometry_gram**.

This distinction matters. Classical probabilities aggregate by summing probability mass. Quantum amplitudes carry complex phase. Blindly summing amplitudes and treating the result as a classical probability loses interference information.

## 4. The exact evolution contract

Define A on X_3 by A(x,y)=1 if x and y differ in exactly one coordinate, otherwise zero. Define the unnormalized quotient B_0(c,d) to be the number of neighbours in class d of any representative of c. Equitability makes this independent of the chosen representative.

The Lean file checks, exactly over natural-number matrices,

```math
AS=SB_0,\qquad S^T S=W.
```

It also checks the classwise balance w(c)B_0(c,d)=w(d)B_0(d,c). After embedding the entries into the complex numbers and normalizing, define

```math
B=W^{1/2}B_0W^{-1/2}=Q^\dagger A Q.
```

The result is AQ=QB, with B Hermitian. Notice the normalization: B_0 need not be symmetric in the ordinary Euclidean inner product.

For a general H,Q,B, the operative admission condition is

```math
HQ=QB,\qquad Q^\dagger Q=I.
```

Lean theorem **Ohio.powers_intertwine** proves H^k Q=QB^k for every natural k under the first condition. Consequently every polynomial in H intertwines in the same way. In finite dimensions, the convergent exponential series gives

```math
e^{-itH}Q=Qe^{-itB}.
```

This final matrix-exponential step is a mathematical corollary, not a Lean-checked exponential theorem in this release. It is validated numerically using independently computed eigendecompositions.

For a discrete unitary step U with U†U=I and UQ=QB, the Lean theorem **Ohio.unitary_restriction** proves B†B=I. Thus exact restriction does preserve unitary evolution when its assumptions hold. **Ohio.hermitian_compression** separately proves that Q†HQ is Hermitian whenever H is Hermitian; Hermitian compression alone does not establish exact dynamics.

### Arbitrary admissible controls

Suppose each control c has a full update F_c, reduced update G_c and common lift L satisfying F_c(Ly)=L(G_c y). **Ohio.controlled_intertwining** proves the corresponding identity for every finite list of controls. There is no restriction to one repeated schedule or a bounded test horizon. However, every admitted control must satisfy the condition; one symmetry-breaking control invalidates the exact reduction.

This theorem is the formal contract for “reduce, evolve, expand.” It does not assert that an arbitrary application already satisfies that contract.

## 5. A reproducible interacting model

The numerical benchmark uses n ternary sites and

```math
H_n=\sum_{i=1}^{n}(X_i+X_i^\dagger)
 + \frac{0.37}{n}(N_2-N_0)^2,
```

where X cycles 0→1→2→0, and N_a counts sites in state a. The last term couples the occupancy counts and prevents this benchmark from being only independent one-site evolution. It remains permutation invariant.

In the normalized occupancy basis, moving one site from a to b has coefficient

```math
\sqrt{n_a(n_b+1)}.
```

The full implementation applies each single-site adjacency through tensor sums. It never constructs a dense 3^n-by-3^n matrix. The reduced implementation multiplies its small dense matrix. Both use complex128 and identical RK4 code: 40 steps, dt=0.002, a seeded normalized complex starting vector in the symmetric subspace. RK4 is an approximate integrator; agreement between representations is not a claim of exact numerical time integration.

### Measured results

Five timed repetitions per path after warmup; medians in milliseconds. Complete samples and environment are in results.json.

| Trits | Full → reduced | Full kernel | Reduced kernel | Warm ratio | State difference (L2) |
|---:|---:|---:|---:|---:|---:|
| 3 | 27 → 10 | 2.070 ms | 0.551 ms | 3.76× | 3.92e-16 |
| 6 | 729 → 28 | 7.256 ms | 0.641 ms | 11.31× | 3.51e-16 |
| 8 | 6,561 → 45 | 38.521 ms | 0.760 ms | 50.66× | 3.48e-16 |
| 10 | 59,049 → 66 | 455.815 ms | 1.401 ms | 325.33× | 5.36e-16 |

The largest full-state RK4 norm drift was 5.12e-11. At n=10, one complex128 state vector occupies 944,784 bytes versus 1,056 bytes in the reduced representation. These are state-vector payloads only, excluding matrices, mapping tables, temporaries and source records.

**Timing boundary:** setup, source-state encoding, admission checks, expanding the output, I/O and persistence are excluded. Shared construction for the n=10 validation fixture took 4.202 ms, but that is not an independently benchmarked production setup path for either method. The 325× figure must not be advertised as end-to-end acceleration. The full samples ranged from 422.142 to 543.425 ms; no cross-host confidence interval is claimed.

**Comparator boundary:** the reduced method is established occupancy/symmetry reduction. This run does not demonstrate an advantage over an existing implementation of that same reduction, a specialized quantum simulator, GPU code or native compiled kernels. It demonstrates the value of recognizing a valid invariant subspace.

### Independent spectral cross-check

At n=3, the script constructs the full 27-by-27 matrix by applying the full operator to basis vectors, and independently diagonalizes that matrix and the reduced 10-by-10 matrix. Twelve seeded complex initial vectors are compared at 81 times from zero to ten:

- 972 state comparisons.
- Maximum lifted state difference: 3.6022e-14.
- Maximum full-state norm drift: 8.8818e-16.
- Matrix intertwining residual: 1.0878e-15.
- Isometry residual: 5.8747e-16.

These are floating-point measurements, not additional exact proofs.

## 6. A failure boundary that can be measured

Add 0.7 times the value of the first named site as a diagonal term. This distinguishes positions within an orbit. With the same Q and compressed B=Q†HQ:

- Leakage operator norm ||HQ-QB||_2 = 0.659966.
- At t=1, from the normalized (1,1,1) occupancy state, the full-versus-reduced state error is 0.316596.

The script asserts that this error is appreciable; it does not silently accept the reduced answer. The finite Lean theorem **Ohio.named_position_breaks** also exhibits two states in the same class with different first-coordinate values.

For production, exact admission requires an exact structural certificate. A small numerical residual is useful evidence but does not certify zero leakage. Approximate reduction needs a separate error budget.

## 7. Geometry: frames, transport and loops

The covariant-derivative animation [2] explains why coordinate components cannot be compared as though their bases were fixed. In a smooth coordinate chart,

```math
\nabla_\mu V^\alpha=\partial_\mu V^\alpha+
\Gamma^\alpha_{\mu\nu}V^\nu.
```

For the metric-compatible, torsion-free Levi–Civita connection,

```math
\Gamma^\alpha_{\mu\nu}
=\tfrac12 g^{\alpha\beta}
(\partial_\mu g_{\beta\nu}+\partial_\nu g_{\beta\mu}
-\partial_\beta g_{\mu\nu}).
```

A coordinate change can yield nonzero Christoffel symbols even when curvature is zero. An arbitrary finite ternary graph does not determine a smooth manifold, metric or connection. Those structures must be specified.

Our implemented bridge is deliberately discrete. For an edge p→q, let T_qp transport components between local frames. Under invertible frame changes G_p,

```math
T'_{qp}=G_qT_{qp}G_p^{-1}.
```

Adjacent G_p^{-1}G_p factors cancel. **Ohio.transport_cancellation** proves this matrix cancellation under the explicit inverse condition. **Ohio.rebasing** proves exact conjugation of arbitrary controlled function updates by an equivalence.

Around a closed path, the transport product transforms by conjugation at the starting point. Returning to the starting address does not force the internal frame to return unchanged. The numerical demonstration uses the path 0→1→2→0, with two identity edges and a 60-degree rotation on the third. Its holonomy differs from identity by Frobenius norm sqrt(2), while a non-orthogonal frame change preserves the expected conjugation relation to 4.44e-16.

This is a constructed discrete transport example, not evidence of physical curvature or a claim that an existing Ohio cycle has this holonomy.

For an actual Riemannian manifold the integration measure is sqrt(det g) dx; cylindrical coordinates give diag(1,r²,1) and hence r dr dtheta dz for r>0. These smooth formulas are established background from [3], not Lean-checked continuum results in this package.

## 8. Verification inventory

All 18 named theorem declarations were accepted by Lean Web with Lean 4.36.0. The receipt records the selected project, source hash, diagnostics and per-theorem axiom reports. The file uses no sorry placeholders, admitted axioms or native_decide.

| Lean theorem | Exact scope |
|---|---|
| ten_classes | n=3 orbit count is 10 |
| orbit_weights | Class weights sum to 27 |
| orbit_histogram | Three weights 1, six weights 3, one weight 6 |
| representative_valid | Chosen representative preserves class code |
| equitable | Neighbour counts agree with the representative |
| weighted_balance | Finite class sizes balance edge counts |
| measure_example | The 297 / 297 / 120 example |
| named_position_breaks | Named-position information is not class invariant |
| weighted_sum | All complex class observables preserve weighted sums |
| concrete_intertwining | The actual natural-number fixture satisfies AS=SB_0 |
| concrete_gram | The actual incidence fixture satisfies S^T S=W |
| controlled_intertwining | Every finite admissible control sequence preserves lifting |
| powers_intertwine | Every natural complex matrix power preserves intertwining |
| rebasing | Conjugating controlled dynamics by an equivalence preserves trajectories |
| transport_cancellation | Intermediate inverse frames cancel |
| hermitian_compression | Compression preserves Hermiticity |
| isometry_gram | Isometric lifting preserves Gram matrices |
| unitary_restriction | An invariant isometric restriction preserves U†U=I |

Standard Lean foundations appearing in the reports are propext, Classical.choice and Quot.sound. The controlled-sequence theorem depends on no axioms. “No sorryAx” is not a claim of an axiom-free development or an independent audit.

**Not formalised in Lean here:** general-n orbit counting; the concrete square-root normalization into complex matrices; the infinite exponential-series corollary; the interacting benchmark implementation; numerical error bounds; smooth Jacobian/Christoffel formulas; a physical model or continuum limit. The paper and code label these boundaries explicitly.

## 9. Practical use and research boundary

The useful implementation is an admission-gated representation choice: retain the full state when identity matters, choose a weighted quotient when the observable and dynamics admit it, and keep the lift, measure and proof obligations with the reduced representation. This connects the Ohio naming and workflow to established group actions, equitable partitions and invariant subspaces.

Today this package provides a reproducible simulation example and formal contracts. A next engineering step is to expose the admission test and backend selector in a real application and compare against a tuned symmetry-aware baseline. A commercial offering would still require a buyer-owned workload and end-to-end measurements. No production or customer performance is claimed here.

## References

1. Matheorems, cylindrical integration animation, 16 November 2026. https://x.com/matheorems/status/2122432771234877824
2. Matheorems, covariant derivative explanation, 17 November 2026. https://x.com/matheorems/status/2122489394431140230
3. David Tong, General Relativity, section 3: Introducing Riemannian Geometry. https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S3.html
4. Hari Krovi and Todd A. Brun, Quantum walks on quotient graphs, Physical Review A 75, 062332 (2007). https://arxiv.org/abs/quant-ph/0701173 ; https://doi.org/10.1103/PhysRevA.75.062332
5. Lean Web, actual proof-checking interface used for this release. https://live.lean-lang.org/
6. Mathlib release toolchain. https://github.com/leanprover-community/mathlib4/blob/v4.36.0/lean-toolchain

References establish mathematical context, not endorsement of Ohio or replication of this benchmark.

