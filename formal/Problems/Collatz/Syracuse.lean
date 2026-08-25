import Problems.Collatz.Accelerated
import Problems.Engine.ParameterDomain

namespace Problems.Collatz

/-- Adapter name for the accelerated odd-only map. Same definition as ``acceleratedT``. -/
abbrev syracuseS : ℕ → ℕ := acceleratedT

theorem syracuseS_mul (n : ℕ) :
    syracuseS n * 2 ^ padicValNat 2 (3 * n + 1) = 3 * n + 1 :=
  acceleratedT_mul n

theorem syracuseS_odd {n : ℕ} (hn : Odd n) (hpos : 0 < n) :
    Odd (syracuseS n) :=
  acceleratedT_odd hn hpos

/-- Exact one-point identity. Not a Collatz convergence theorem. -/
theorem syracuseS_one : syracuseS 1 = 1 := by
  have hmul := acceleratedT_mul 1
  have hval : padicValNat 2 (3 * 1 + 1) = 2 := by native_decide
  have : syracuseS 1 * 2 ^ 2 = 4 := by
    simpa [hval] using hmul
  omega

/-- Generic Engine iff specialized to ``q = 3x+1``. KNOWN arithmetic;
not a theorem that ``syracuseS`` equals the closed form on all odd
positives, and not a Collatz convergence result. -/
theorem syracuseS_parameter_iff
    {x : ℤ} {k : ℕ} (hq : (3 : ℤ) * x + 1 ≠ 0) :
    (∃ y : ℤ, (2 : ℤ) ^ k * y = 3 * x + 1 ∧ ¬ (2 : ℤ) ∣ y) ↔
      padicValInt 2 (3 * x + 1) = k :=
  Problems.Engine.mul_pow_eq_iff_padicValInt (b := 2) hq

end Problems.Collatz
