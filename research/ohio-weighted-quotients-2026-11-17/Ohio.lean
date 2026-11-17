import Mathlib

/- Ohio: weighted quotients, exact evolution, and rebasing.
   This file proves finite and algebraic claims; it does not formalise
   continuum manifolds, matrix exponentials, or physical experiments. -/
namespace Ohio
set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev State := Fin 27
def digit (s : State) (i : Nat) : Nat := s.val / 3^i % 3
def count (s : State) (a : Nat) : Nat :=
  (if digit s 0 = a then 1 else 0) +
  (if digit s 1 = a then 1 else 0) +
  (if digit s 2 = a then 1 else 0)
def cls (s : State) : Nat := 4 * count s 0 + count s 1
def classes : Finset Nat := Finset.univ.image cls
def weight (c : Nat) : Nat := (Finset.univ.filter fun s : State => cls s = c).card
def rep (c : Nat) : State := match c with
  | 0 => 26 | 1 => 17 | 2 => 14 | 3 => 13
  | 4 => 8 | 5 => 5 | 6 => 4 | 8 => 2 | 9 => 1 | 12 => 0
  | _ => 0
def hamming (s t : State) : Nat :=
  (if digit s 0 = digit t 0 then 0 else 1) +
  (if digit s 1 = digit t 1 then 0 else 1) +
  (if digit s 2 = digit t 2 then 0 else 1)
def adjacency (s t : State) : Nat := if hamming s t = 1 then 1 else 0
def row (s : State) (c : Nat) : Nat :=
  (Finset.univ.filter fun t : State => cls t = c && hamming s t = 1).card

theorem ten_classes : classes.card = 10 := by decide
theorem orbit_weights :
  classes.sum weight = 27 := by decide
theorem orbit_histogram :
  (classes.filter fun c => weight c = 1).card = 3 ∧
  (classes.filter fun c => weight c = 3).card = 6 ∧
  (classes.filter fun c => weight c = 6).card = 1 := by decide
theorem representative_valid : ∀ s : State, cls (rep (cls s)) = cls s := by decide
theorem equitable :
  ∀ s : State, ∀ c : Fin 13, row s c.val = row (rep (cls s)) c.val := by decide
theorem weighted_balance :
  ∀ c d : Fin 13,
  weight c.val * row (rep c.val) d.val =
  weight d.val * row (rep d.val) c.val := by decide

def obs (s : State) : Nat := (digit s 0 + digit s 1 + digit s 2)^2
theorem measure_example :
  (Finset.univ.sum obs = 297) ∧
  (classes.sum (fun c => weight c * obs (rep c)) = 297) ∧
  (classes.sum (fun c => obs (rep c)) = 120) := by decide
theorem named_position_breaks :
  cls (5 : State) = cls (11 : State) ∧
  digit (5 : State) 2 ≠ digit (11 : State) 2 := by decide

-- A concrete all-observables conservation theorem, not one test function.
theorem weighted_sum (f : Nat → ℂ) :
  (∑ s : State, f (cls s)) = ∑ c ∈ classes, (weight c : ℂ) * f c := by
  have regroup := Finset.sum_fiberwise_of_maps_to
    (s := (Finset.univ : Finset State)) (t := classes) (g := cls)
    (by intro s hs; exact Finset.mem_image.mpr ⟨s, hs, rfl⟩)
    (fun s => f (cls s))
  rw [← regroup]
  apply Finset.sum_congr rfl
  intro c hc
  calc
    (∑ s ∈ Finset.univ.filter (fun s : State => cls s = c), f (cls s)) =
        ∑ s ∈ Finset.univ.filter (fun s : State => cls s = c), f c := by
      apply Finset.sum_congr rfl
      intro s hs
      rw [(Finset.mem_filter.mp hs).2]
    _ = (weight c : ℂ) * f c := by simp [weight, nsmul_eq_mul]

-- Concrete natural-number matrices connecting the finite partition to evolution.
def code (c : Fin 10) : Nat := (![0,1,2,3,4,5,6,8,9,12] : Fin 10 → Nat) c
def fullMatrix : Matrix State State Nat := fun s t => (adjacency s t : Nat)
def incidence : Matrix State (Fin 10) Nat := fun s c => if cls s = code c then 1 else 0
def reducedMatrix : Matrix (Fin 10) (Fin 10) Nat :=
  fun c d => (row (rep (code c)) (code d) : Nat)
def weightMatrix : Matrix (Fin 10) (Fin 10) Nat :=
  fun c d => if c = d then weight (code c) else 0

theorem concrete_intertwining : fullMatrix * incidence = incidence * reducedMatrix := by
  have h : ∀ i j, (fullMatrix * incidence) i j = (incidence * reducedMatrix) i j := by decide
  exact Matrix.ext h
theorem concrete_gram : incidence.transpose * incidence = weightMatrix := by
  have h : ∀ (i j : Fin 10), (incidence.transpose * incidence) i j = weightMatrix i j := by
    change ∀ (i j : Fin 10), (∑ s : State, incidence s i * incidence s j) =
      (if i = j then weight (code i) else 0)
    decide
  exact Matrix.ext h

-- Exact evolution through any finite sequence of admissible controls.
def run {C X : Type*} (F : C → X → X) : List C → X → X
  | [], x => x
  | c :: cs, x => run F cs (F c x)
theorem controlled_intertwining {C X Y : Type*}
  (F : C → X → X) (G : C → Y → Y) (L : Y → X)
  (h : ∀ c y, F c (L y) = L (G c y)) :
  ∀ cs y, run F cs (L y) = L (run G cs y) := by
  intro cs
  induction cs with
  | nil => intro y; rfl
  | cons c cs ih =>
    intro y
    simp only [run, h]
    exact ih (G c y)

-- Rectangular intertwining propagates to every natural matrix power.
theorem powers_intertwine {m n : Type*} [Fintype m] [Fintype n]
  [DecidableEq m] [DecidableEq n]
  (H : Matrix m m ℂ) (Q : Matrix m n ℂ) (B : Matrix n n ℂ)
  (h : H * Q = Q * B) : ∀ k : Nat, H^k * Q = Q * B^k := by
  intro k
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, Matrix.mul_assoc, h, ← Matrix.mul_assoc, ih,
        Matrix.mul_assoc, ← pow_succ]

-- Exact coordinate rebasing for arbitrary nonlinear controlled dynamics.
theorem rebasing {C X Y : Type*} (e : X ≃ Y) (F : C → X → X) :
  ∀ cs x,
    run (fun c y => e (F c (e.symm y))) cs (e x) = e (run F cs x) := by
  apply controlled_intertwining
  intro c x
  simp

-- Adjacent frame changes cancel in transported matrix products.
theorem transport_cancellation {n : Type*} [Fintype n] [DecidableEq n]
  (A B B_inv T S : Matrix n n ℂ) (h : B_inv * B = 1) :
  (A * T * B_inv) * (B * S) = A * (T * S) := by
  calc
    (A * T * B_inv) * (B * S) = (A * T) * ((B_inv * B) * S) := by
      simp only [Matrix.mul_assoc]
    _ = A * (T * S) := by rw [h]; simp [Matrix.mul_assoc]

-- Compression of a Hermitian operator remains Hermitian.
theorem hermitian_compression {m n : Type*} [Fintype m] [Fintype n]
  (H : Matrix m m ℂ) (Q : Matrix m n ℂ) (h : H.conjTranspose = H) :
  (Q.conjTranspose * H * Q).conjTranspose = Q.conjTranspose * H * Q := by
  simp [Matrix.conjTranspose_mul, h, Matrix.mul_assoc]

-- An isometric lift preserves every Gram matrix.
theorem isometry_gram {m n k : Type*} [Fintype m] [Fintype n]
  [DecidableEq n] (Q : Matrix m n ℂ) (V : Matrix n k ℂ)
  (h : Q.conjTranspose * Q = 1) :
  (Q * V).conjTranspose * (Q * V) = V.conjTranspose * V := by
  rw [Matrix.conjTranspose_mul]
  calc
    (V.conjTranspose * Q.conjTranspose) * (Q * V) =
      V.conjTranspose * ((Q.conjTranspose * Q) * V) := by
        simp only [Matrix.mul_assoc]
    _ = V.conjTranspose * V := by rw [h]; simp

-- Exact restriction of a unitary step to an invariant isometric subspace.
theorem unitary_restriction {m n : Type*} [Fintype m] [Fintype n]
  [DecidableEq m] [DecidableEq n]
  (U : Matrix m m ℂ) (Q : Matrix m n ℂ) (B : Matrix n n ℂ)
  (hU : U.conjTranspose * U = 1) (hQ : Q.conjTranspose * Q = 1)
  (h : U * Q = Q * B) : B.conjTranspose * B = 1 := by
  calc
    B.conjTranspose * B = (Q * B).conjTranspose * (Q * B) :=
      (isometry_gram Q B hQ).symm
    _ = (U * Q).conjTranspose * (U * Q) := by rw [← h]
    _ = Q.conjTranspose * Q := isometry_gram U Q hU
    _ = 1 := hQ

end Ohio
#print axioms Ohio.ten_classes
#print axioms Ohio.orbit_weights
#print axioms Ohio.orbit_histogram
#print axioms Ohio.representative_valid
#print axioms Ohio.equitable
#print axioms Ohio.weighted_balance
#print axioms Ohio.measure_example
#print axioms Ohio.named_position_breaks
#print axioms Ohio.weighted_sum
#print axioms Ohio.controlled_intertwining
#print axioms Ohio.powers_intertwine
#print axioms Ohio.rebasing
#print axioms Ohio.transport_cancellation
#print axioms Ohio.hermitian_compression
#print axioms Ohio.isometry_gram
#print axioms Ohio.unitary_restriction
#print axioms Ohio.concrete_intertwining
#print axioms Ohio.concrete_gram
#eval Lean.versionString
