# Verification receipt

Date: 17 November 2026, Australia/Perth.

## Exact proof check

- Interface: https://live.lean-lang.org/
- Successful fully inspected project: **Latest Mathlib with Lean v4.36.0** (MathlibDemo).
- Lean.versionString returned **4.36.0**.
- Final completed diagnostics: **19 informational messages**: 18 theorem axiom reports and the version string; no errors or warnings.
- Ohio.lean SHA-256: `c853e1e2298aa0196abffb004178469663416d263c7e1614fbfdd190f4931126`.
- Source was copied back from the editor and compared byte-for-byte as UTF-8 against the submitted source: matched. The browser-derived SHA-256 matched the local file hash.
- 18 named theorems; no sorryAx or Lean.ofReduceBool in the axiom reports; no sorry/admit/native_decide in the proof source.
- Proofs use ordinary Lean kernel checking, including finite decidable propositions. Standard foundations are listed below; this is not an axiom-free or independently audited development.
- This was a browser-hosted Lean check. The browser interaction's process exit status is not presented as a native Lean CLI exit status.
- A later switch to the release project displayed 19 messages, but its expanded diagnostic capture failed when the browser service returned HTTP 502. That incomplete capture is **not** used as an additional verification claim.
- No native local Lean build was run: Lean was unavailable locally and the shell could not resolve the download host. The supplied Lake configuration targets the official v4.36.0 release for reproduction; its dependency installation was not exercised here.

## Observed axiom reports

Reordered by theorem listing for readability; substantive diagnostic lines are unchanged.

```text
'Ohio.ten_classes' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.orbit_weights' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.orbit_histogram' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.representative_valid' depends on axioms: [propext]
'Ohio.equitable' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.weighted_balance' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.measure_example' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.named_position_breaks' depends on axioms: [propext]
'Ohio.weighted_sum' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.controlled_intertwining' does not depend on any axioms
'Ohio.powers_intertwine' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.rebasing' depends on axioms: [propext, Quot.sound]
'Ohio.transport_cancellation' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.hermitian_compression' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.isometry_gram' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.unitary_restriction' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.concrete_intertwining' depends on axioms: [propext, Classical.choice, Quot.sound]
'Ohio.concrete_gram' depends on axioms: [propext, Classical.choice, Quot.sound]
"4.36.0"
```

## Numerical execution

Command: `python experiment.py`

Observed process exit code: **0**. Final marker: **ALL_NUMERICAL_CHECKS_PASSED**.

The experiment uses NumPy 2.4.6, Python 3.14.6, Windows 11. Full environment and all samples are in results.json. It checks:
- class weights and symmetric reduced matrices;
- full-versus-reduced operator action at n=3,6,8,10;
- equal-step RK4 trajectories for those four models;
- 972 separate time/state eigendecomposition comparisons at n=3;
- rejection of a named-site symmetry-breaking perturbation;
- covariance of a discrete closed-loop transport example.

Numerical agreement is bounded floating-point evidence. It is not a Lean verification of NumPy, the Python implementation, general-n counting or matrix exponentials.

## Reproducibility boundary

The exact MathlibDemo backend commit was not exposed in the UI and is not claimed pinned by this receipt. The source, Lean version, axiom output and source hash are retained. The official mathlib v4.36.0 lean-toolchain file was separately read and specifies leanprover/lean4:v4.36.0.

