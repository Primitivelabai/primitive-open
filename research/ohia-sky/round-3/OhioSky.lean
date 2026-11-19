import Lean

namespace OhioSky

/-- Exact sums in an ordered cadence list. Inputs have already been folded,
    sorted, and quantized. -/
def sumTo : Nat → List Int → Int
  | 0, _ => 0
  | _ + 1, [] => 0
  | n + 1, x :: xs => x + sumTo n xs

theorem prefix_window (xs : List Int) (lo width : Nat) :
    sumTo (lo + width) xs - sumTo lo xs = sumTo width (xs.drop lo) := by
  induction lo generalizing xs with
  | zero => simp [sumTo]
  | succ lo ih =>
      cases xs with
      | nil =>
          cases width <;> simp [Nat.succ_add, sumTo]
      | cons x xs =>
          simp only [Nat.succ_add, sumTo, List.drop_succ_cons]
          have h := ih xs
          omega

/-- A wrapped interval consists of the tail followed by an initial segment. -/
theorem wrapped_window (xs : List Int) (lo width : Nat) (h : lo ≤ xs.length) :
    sumTo xs.length xs - sumTo lo xs + sumTo width xs =
      sumTo (xs.length - lo) (xs.drop lo) + sumTo width xs := by
  have hs : lo + (xs.length - lo) = xs.length := by omega
  have hp := prefix_window xs lo (xs.length - lo)
  rw [hs] at hp
  rw [hp]

def signedSquare (x : Int) : Int := x * (Int.natAbs x : Int)

/-- Integer comparison used by the two exact rank implementations. -/
def atLeast (total trial : Int) (count trialCount : Nat) : Bool :=
  decide (signedSquare trial * (count : Int) ≤ signedSquare total * (trialCount : Int))

theorem window_vote (xs : List Int) (lo width count trialCount : Nat) (trial : Int) :
    atLeast (sumTo (lo + width) xs - sumTo lo xs) trial count trialCount =
      atLeast (sumTo width (xs.drop lo)) trial count trialCount := by
  rw [prefix_window]

theorem rank_votes (xs : List Int) (windows : List (Nat × Nat)) (trialCount : Nat) (trial : Int) :
    (windows.filter fun w => atLeast (sumTo (w.1 + w.2) xs - sumTo w.1 xs) trial w.2 trialCount).length =
      (windows.filter fun w => atLeast (sumTo w.2 (xs.drop w.1)) trial w.2 trialCount).length := by
  induction windows with
  | nil => rfl
  | cons w ws ih =>
    simp only [List.filter_cons, window_vote]

def signal (period : Nat) (wave : Nat → Int) (t : Nat) : Int := wave (t % period)

/-- Folding a periodic source at an integer multiple preserves its inner phase. -/
theorem multiple_fold (period repeats t : Nat) (wave : Nat → Int) :
    signal period wave (t % (period * repeats)) = signal period wave t := by
  unfold signal
  rw [Nat.mod_mod_of_dvd t (show period ∣ period * repeats from ⟨repeats, rfl⟩)]

/-- A constant baseline and linear leakage preserve the alias in an aperture. -/
theorem mixed_aperture (period repeats t : Nat) (wave : Nat → Int) (baseline leakage : Int) :
    baseline + leakage * signal period wave (t % (period * repeats)) =
      baseline + leakage * signal period wave t := by
  rw [multiple_fold]

def dip (period t : Nat) : Int := if t % period = 0 then -1 else 0

/-- One dip per long cycle and a repeated short-cycle dip agree at the main
    anchor but disagree at the first internal crossing. -/
theorem internal_witness (period : Nat) (pos : 0 < period) :
    dip period 0 = dip (3 * period) 0 ∧
    dip period (3 * period) = dip (3 * period) (3 * period) ∧
    dip period period ≠ dip (3 * period) period := by
  have lt : period < 3 * period := by omega
  have ne : period ≠ 0 := by omega
  simp [dip, Nat.mod_eq_of_lt lt, ne]

/-- Arithmetic check on the two measured periods rounded to nanodays. -/
theorem rounded_clock_residual :
    ((1114597980 : Int) - 3 * 371540278).natAbs * 86400 < 2 * 1000000000 := by
  decide

end OhioSky

#print axioms OhioSky.prefix_window
#print axioms OhioSky.wrapped_window
#print axioms OhioSky.window_vote
#print axioms OhioSky.rank_votes
#print axioms OhioSky.multiple_fold
#print axioms OhioSky.mixed_aperture
#print axioms OhioSky.internal_witness
#print axioms OhioSky.rounded_clock_residual
