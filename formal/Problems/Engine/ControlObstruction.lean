import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import Problems.Engine.ControlWord

namespace Problems.Engine

/-!
Generic integer obstructions for a cleared cycle constraint
``(A - B) x = C``. This is not a Collatz theorem.
-/

theorem exists_mul_eq_iff_dvd (a b : ℤ) :
    (∃ x : ℤ, a * x = b) ↔ a ∣ b := by
  constructor
  · rintro ⟨x, hx⟩
    exact ⟨x, hx.symm⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, hx.symm⟩

theorem cycle_constraint_dvd {A B C x : ℤ}
    (h : A * x = B * x + C) :
    (A - B) ∣ C := by
  exact (exists_mul_eq_iff_dvd (A - B) C).1 ⟨x, cycle_of_composed h⟩

theorem not_dvd_of_abs_gt {a b : ℤ} (hb : b ≠ 0) (h : |b| < |a|) :
    ¬ a ∣ b := by
  rintro ⟨k, rfl⟩
  have hk0 : k ≠ 0 := by
    rintro rfl
    simp at hb
  have hge : (1 : ℤ) ≤ |k| := by
    have := abs_pos.mpr hk0
    omega
  have : |a| ≤ |a * k| := by
    calc
      |a| = |a| * 1 := by ring
      _ ≤ |a| * |k| := by nlinarith [abs_nonneg a]
      _ = |a * k| := (abs_mul a k).symm
  exact (not_le_of_lt h) this

end Problems.Engine
