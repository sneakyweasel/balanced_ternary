import Mathlib.Data.Nat.Sqrt
import Mathlib.Tactic

namespace Problems.Engine

/-!
Exact identities for the even/odd floor-power map.
These statements are the problem definition and a finite seed orbit.
They are KNOWN. They are not a halt theorem on all positive integers.
-/

/-- Even `n` maps to `Nat.sqrt n`; odd `n` maps to `Nat.sqrt (n^3)`. -/
def floorPower (n : ℕ) : ℕ :=
  if n % 2 = 0 then n.sqrt else (n * n * n).sqrt

/-- Integer obstruction: `k^4 ≤ n^3` and `n ≥ 2` forbid `k ≥ n`.
This is iterated `Nat.sqrt` of `n^3`, not `T^2` on the odd-to-odd branch. -/
theorem sqrt_sqrt_n_cubed_lt {n : ℕ} (hn : 2 ≤ n) :
    ((n * n * n).sqrt).sqrt < n := by
  set m := (n * n * n).sqrt
  set k := m.sqrt
  have hk : k * k ≤ m := Nat.sqrt_le m
  have hm : m * m ≤ n * n * n := Nat.sqrt_le (n * n * n)
  have hk4 : k * k * (k * k) ≤ m * m := Nat.mul_le_mul hk hk
  have hk4n : k * k * k * k ≤ n * n * n := by
    simpa [mul_assoc] using (le_trans hk4 hm)
  refine Nat.lt_of_not_ge fun hkn => ?_
  have hn4 : n * n * n * n ≤ k * k * k * k := by
    have h2 := Nat.mul_le_mul hkn hkn
    simpa [mul_assoc] using Nat.mul_le_mul h2 h2
  have hle : n * n * n * n ≤ n * n * n := le_trans hn4 hk4n
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : 0 < 2) hn
  have hn3 : 0 < n * n * n := Nat.mul_pos (Nat.mul_pos hn0 hn0) hn0
  have hmul : n * (n * n * n) ≤ 1 * (n * n * n) := by
    simpa [mul_assoc, mul_comm, mul_left_comm] using hle
  have : n ≤ 1 := Nat.le_of_mul_le_mul_right hmul hn3
  omega

/-- On the odd-to-even branch, `T^2(n) < n`. Not a halt theorem for the full map. -/
theorem floorPower_odd_even_two_step_lt
    {n : ℕ} (hn : 2 ≤ n) (hodd : n % 2 = 1)
    (heven : (n * n * n).sqrt % 2 = 0) :
    floorPower (floorPower n) < n := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
  have step2 : floorPower (floorPower n) = ((n * n * n).sqrt).sqrt := by
    rw [step1]
    simp [floorPower, heven]
  rw [step2]
  exact sqrt_sqrt_n_cubed_lt hn

/-- Integer comparison: `(n+1)^2 ≤ n^3` for `n ≥ 3`. Threshold for odd-branch growth. -/
theorem succ_sq_le_cube {n : ℕ} (hn : 3 ≤ n) : (n + 1) ^ 2 ≤ n ^ 3 := by
  zify
  nlinarith

/-- On the odd branch, `n ≥ 3` implies `T(n) > n`. Independent of the parity of `T(n)`. -/
theorem floorPower_odd_gt {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1) :
    n < floorPower n := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
  rw [step1]
  have hsq : (n + 1) ^ 2 ≤ n ^ 3 := succ_sq_le_cube hn
  have hpow : n ^ 3 = n * n * n := by ring
  have : n + 1 ≤ (n * n * n).sqrt := by
    exact Nat.le_sqrt.mpr (by simpa [hpow, pow_two] using hsq)
  omega

/-- The odd branch is nondecreasing: `k ≤ T(k)` when `k` is odd and positive. -/
theorem floorPower_odd_nondecreasing {k : ℕ} (hk : 1 ≤ k) (hodd : k % 2 = 1) :
    k ≤ floorPower k := by
  have hodd0 : k % 2 ≠ 0 := by omega
  have step1 : floorPower k = (k * k * k).sqrt := by
    simp [floorPower, hodd0]
  rw [step1]
  have h1 : k * k ≤ k * k * k := by
    have : 1 ≤ k := hk
    simpa [Nat.mul_assoc] using Nat.mul_le_mul_left (k * k) this
  exact Nat.le_sqrt.mpr h1

/-- On the odd-to-odd branch with `n ≥ 3`, `T^2(n) > n`. Dual of
`floorPower_odd_even_two_step_lt`. Not a divergence theorem. -/
theorem floorPower_odd_odd_two_step_gt
    {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1)
    (hodd1 : (n * n * n).sqrt % 2 = 1) :
    n < floorPower (floorPower n) := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
  have hkpos : 1 ≤ floorPower n := by
    have : n < floorPower n := floorPower_odd_gt hn hodd
    omega
  have hoddT : floorPower n % 2 = 1 := by
    simpa [step1] using hodd1
  have hmono : floorPower n ≤ floorPower (floorPower n) :=
    floorPower_odd_nondecreasing hkpos hoddT
  have hgt : n < floorPower n := floorPower_odd_gt hn hodd
  omega

/-- Combined odd-state two-step direction for `n ≥ 3`. This is the
conjunction of `floorPower_odd_even_two_step_lt` and
`floorPower_odd_odd_two_step_gt` on a common domain. It is not a
macro-transition law, not a halt theorem, and not a divergence theorem.
The case `n = 1` is excluded: `floorPower 1 = 1`. -/
theorem floorPower_odd_macro_direction
    {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1) :
    ((n * n * n).sqrt % 2 = 0 → floorPower (floorPower n) < n) ∧
    ((n * n * n).sqrt % 2 = 1 → n < floorPower (floorPower n)) := by
  refine ⟨?he, ?ho⟩
  · intro heven
    have hn2 : 2 ≤ n := le_trans (by decide : 2 ≤ 3) hn
    exact floorPower_odd_even_two_step_lt hn2 hodd heven
  · intro hodd1
    exact floorPower_odd_odd_two_step_gt hn hodd hodd1


theorem floorPower_one : floorPower 1 = 1 := by
  native_decide

theorem floorPower_thirteen_step : floorPower 13 = 46 := by
  native_decide

/-- Packet seed `13` reaches `1` in four steps. Not a map theorem. -/
theorem floorPower_thirteen_reaches_one :
    (floorPower^[4] 13) = 1 := by
  native_decide

end Problems.Engine
