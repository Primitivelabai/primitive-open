# Ohio: fewer amplitudes, preserved evolution

A reproducible symmetry-reduction experiment, an explicit failure case, and **18 Lean-checked finite/algebraic theorems**.

**Read [the research note](PAPER.md).** Check [the verification receipt](VERIFICATION.md), [Lean source](Ohio.lean), [experiment](experiment.py), and [raw results](results.json).

## The measured result

On one synthetic symmetric 10-trit Hamiltonian:

- **59,049 → 66 amplitudes.**
- **455.815 ms → 1.401 ms**, a **325.33× warm kernel ratio**, against a full tensor implementation.
- Full-versus-lifted RK4 trajectory difference: **5.36e-16** (L2).
- **972** three-trit spectral comparisons, maximum error **3.60e-14**.
- A named-site perturbation breaks the symmetry and produces **0.3166** state error at time one.

This is established symmetry reduction implemented and tested for a scoped model. Timing excludes setup, encoding, expansion and I/O. It is not a measured advantage over another symmetry-reduced solver, a quantum hardware result or a universal speedup.

## Reproduce the numerical run

Python 3 and NumPy are required. The recorded run used Python 3.14.6 and NumPy 2.4.6.

```bash
python -m pip install -r requirements.txt
python experiment.py
```

This writes fresh measurements to results.json. Preserve the original file first if comparing timings. The seed is fixed; floating-point and timing results can vary by host and library.

## Recheck Lean

Fast route: open https://live.lean-lang.org/, select a Mathlib project using Lean 4.36.0, paste the complete Ohio.lean file and expand All Messages. Every named theorem has a final axiom report.

Native reproduction configuration (provided, not executed locally in this run):

```bash
lake update
lake exe cache get
lake env lean Ohio.lean
```

The lakefile pins mathlib's v4.36.0 release tag and lean-toolchain pins Lean 4.36.0. The browser verification used the MathlibDemo backend; its exact commit was not exposed. See VERIFICATION.md for the complete boundary.

## Files

| File | Purpose |
|---|---|
| PAPER.md | Definitions, proofs, interpretation, measured results, references and limits |
| Ohio.lean | Exact finite fixture and general algebraic contracts |
| VERIFICATION.md | Observed proof diagnostics, source hash and execution scope |
| experiment.py | Seeded numerical reproduction and negative controls |
| results.json | Raw measurements and host information |
| lean-toolchain / lakefile.toml | Native reproduction configuration |
| requirements.txt | Recorded numerical dependency version |
| SHA256SUMS | Integrity hashes of the release files |

Prepared with ChatGPT/Codex from Josh's Ohio research direction. Research note, not peer reviewed. Repository licence applies.

