import Problems.Engine.ControlObstruction
import Problems.Engine.ControlWord
import Problems.Engine.ParameterDomain

namespace Problems.Engine

/-!
Generic accelerated (mx+r) identities. These are KNOWN integer
arithmetic specializations of the Engine lemmas. They are not map
theorems on the odd positives and not Collatz convergence results.
-/

/-- Exact exponent selection for the cleared relation ``2^k y = m x + r``. -/
theorem mxPlusR_parameter_iff
    {m r x : ℤ} {k : ℕ} (hq : m * x + r ≠ 0) :
    (∃ y : ℤ, (2 : ℤ) ^ k * y = m * x + r ∧ ¬ (2 : ℤ) ∣ y) ↔
      padicValInt 2 (m * x + r) = k :=
  mul_pow_eq_iff_padicValInt (b := 2) hq

/-- Two certified one-step clearing relations compose. -/
theorem mxPlusR_compose_two
    {m r : ℤ} {k0 k1 : ℕ} {x0 x1 x2 : ℤ}
    (h0 : (2 : ℤ) ^ k0 * x1 = m * x0 + r)
    (h1 : (2 : ℤ) ^ k1 * x2 = m * x1 + r) :
    (2 : ℤ) ^ k0 * (2 : ℤ) ^ k1 * x2 =
      m * m * x0 + (m * r + (2 : ℤ) ^ k0 * r) :=
  compose_two_affine h0 h1

/-- Length-one cycle constraint implies a divisibility condition. -/
theorem mxPlusR_len_one_cycle_dvd {m r : ℤ} {k : ℕ} {x : ℤ}
    (h : (2 : ℤ) ^ k * x = m * x + r) :
    ((2 : ℤ) ^ k - m) ∣ r :=
  cycle_constraint_dvd h

end Problems.Engine
