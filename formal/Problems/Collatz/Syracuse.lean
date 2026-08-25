import Problems.Collatz.Accelerated

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

end Problems.Collatz
