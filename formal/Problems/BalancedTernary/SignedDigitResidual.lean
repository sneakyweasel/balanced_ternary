import BTCalculus.Normalization
import Problems.BalancedTernary.FiniteStateDynamics

namespace Problems.BalancedTernary

open BTCalculus

/-!
Residual dynamics ``F_{λ,U}(s,u) = λ · DZ(s+u)`` for a bounded raw
alphabet. Doubled-trit normalization and streaming ``D(x+y)`` are
special alphabets of this map. This file does not repeat
``doubledTrit_*`` or ``dAdd_*``.
-/

def signedNext (gain s u : ℤ) : ℤ :=
  gain * DZ (s + u)

def signedOut (s u : ℤ) : ℤ :=
  lsdZ (s + u)

theorem isTrit_of_natAbs_le_one {u : ℤ} (h : u.natAbs ≤ 1) : isTrit u :=
  natAbs_le_one_iff.mp h

theorem DZ_of_trit {u : ℤ} (h : isTrit u) : DZ u = 0 := by
  rcases h with h | h | h <;> simp [h, DZ, lsdZ]

/-- Trit forcing: from residual ``0``, any ``|u|≤1`` stays at ``0`` for every gain. -/
theorem origin_trit_forcing {gain u : ℤ} (hu : u.natAbs ≤ 1) :
    signedNext gain 0 u = 0 := by
  have htrit := isTrit_of_natAbs_le_one hu
  simp [signedNext, DZ_of_trit htrit]

theorem gain3_m1_origin {u : ℤ} (hu : u.natAbs ≤ 1) :
    signedNext 3 0 u = 0 :=
  origin_trit_forcing hu

/-- Sharp ``λ=1`` reachable/invariant radius ``⌊m/2⌋``. The looser
``⌈(m+1)/2⌉`` from ``3|DZ n|≤|n|+1`` is not required. -/
theorem lambda1_radius_div (m : ℕ) :
    (m / 2 + m + 1) / 3 ≤ m / 2 := by
  omega

theorem lambda1_reachable_box {s u : ℤ} {m : ℕ}
    (hs : s.natAbs ≤ m / 2) (hu : u.natAbs ≤ m) :
    (DZ (s + u)).natAbs ≤ m / 2 := by
  have hsum : (s + u).natAbs ≤ s.natAbs + u.natAbs := Int.natAbs_add_le s u
  have hB : (s + u).natAbs ≤ m / 2 + m := by omega
  have hdz := DZ_le_of_abs_le (B := m / 2 + m) hB
  have : (m / 2 + m + 1) / 3 ≤ m / 2 := lambda1_radius_div m
  omega

theorem lambda1_u2_residual_closure {s u : ℤ}
    (hs : s.natAbs ≤ 1) (hu : u.natAbs ≤ 2) :
    (DZ (s + u)).natAbs ≤ 1 :=
  lambda1_reachable_box (m := 2) hs hu

/-- Strict decrease of ``|s|`` outside the sharp ``λ=1`` box. -/
theorem lambda1_lyapunov {s u : ℤ} {m : ℕ}
    (hs : m + 2 ≤ 2 * s.natAbs) (hu : u.natAbs ≤ m) :
    (DZ (s + u)).natAbs < s.natAbs := by
  have hsum : (s + u).natAbs ≤ s.natAbs + u.natAbs := Int.natAbs_add_le s u
  have hB : (s + u).natAbs ≤ s.natAbs + m := by omega
  have hb := DZ_carry_bound (s + u)
  have : 3 * (DZ (s + u)).natAbs ≤ s.natAbs + m + 1 := by omega
  have hpos : 0 < s.natAbs := by omega
  omega

/-- Sufficient invariant interval for gain ``2``: radius ``2(m+1)``. -/
theorem lambda2_box_invariant {s u : ℤ} {m : ℕ}
    (hs : s.natAbs ≤ 2 * (m + 1)) (hu : u.natAbs ≤ m) :
    (2 * DZ (s + u)).natAbs ≤ 2 * (m + 1) := by
  have hsum : (s + u).natAbs ≤ s.natAbs + u.natAbs := Int.natAbs_add_le s u
  have hB : (s + u).natAbs ≤ 2 * (m + 1) + m := by omega
  have hb := DZ_carry_bound (s + u)
  have : 3 * (DZ (s + u)).natAbs ≤ 2 * (m + 1) + m + 1 := by omega
  have hmul : (2 * DZ (s + u)).natAbs = 2 * (DZ (s + u)).natAbs := by
    simp [Int.natAbs_mul]
  omega

theorem signedNext_gain3_control2 (n : ℤ) :
    signedNext 3 (3 * n) 2 = 3 * (n + 1) := by
  simp [signedNext, DZ_three_mul_add_two]

theorem gain3_control2_eq (n : ℕ) : carryGain3 n = 3 * (n : ℤ) :=
  carryGain3_eq n

theorem gain3_control2_unbounded (B : ℕ) :
    ∃ n : ℕ, B < (carryGain3 n).natAbs :=
  carryGain3_unbounded B

/-- Finite residual closure of ``F_{λ,U_m}`` for ``λ∈{1,2}`` or trit forcing
``m≤1``. The matching infinite witness at ``λ=3``, ``m≥2`` is
``gain3_control2_unbounded``. -/
theorem finite_residual_condition {gain m : ℕ}
    (h : gain = 1 ∨ gain = 2 ∨ m ≤ 1) :
    ∃ R : ℕ, ∀ s u : ℤ, s.natAbs ≤ R → u.natAbs ≤ m →
      ((gain : ℤ) * DZ (s + u)).natAbs ≤ R := by
  rcases h with hgain | hgain | hm
  · refine ⟨m / 2, ?_⟩
    intro s u hs hu
    simp [hgain, lambda1_reachable_box hs hu]
  · refine ⟨2 * (m + 1), ?_⟩
    intro s u hs hu
    simpa [hgain] using lambda2_box_invariant (s := s) (u := u) (m := m) hs hu
  · refine ⟨0, ?_⟩
    intro s u hs hu
    have hs0 : s = 0 := Int.natAbs_eq_zero.mp (by omega)
    have hstep := origin_trit_forcing (gain := (gain : ℤ)) (u := u) (by omega)
    simp [signedNext] at hstep
    simpa [hs0] using hstep

theorem sum_trits_bound (inputs : List ℤ)
    (h : ∀ a ∈ inputs, isTrit a) :
    inputs.sum.natAbs ≤ inputs.length := by
  induction inputs with
  | nil => simp
  | cons a rest ih =>
    have ha := h a (by simp)
    have hr : ∀ b ∈ rest, isTrit b := fun b hb =>
      h b (by simp [hb])
    have ih' := ih hr
    have habs : a.natAbs ≤ 1 := isTrit_natAbs ha
    have hadd : (a + rest.sum).natAbs ≤ a.natAbs + rest.sum.natAbs :=
      Int.natAbs_add_le a rest.sum
    simp [List.sum_cons]
    omega

/-- r-way trit addition is the ``λ=1`` family on ``U_r``. -/
theorem multi_trit_carry_bound {s : ℤ} {inputs : List ℤ}
    (hs : s.natAbs ≤ inputs.length / 2)
    (htrits : ∀ a ∈ inputs, isTrit a) :
    (DZ (s + inputs.sum)).natAbs ≤ inputs.length / 2 := by
  have hu := sum_trits_bound inputs htrits
  exact lambda1_reachable_box (m := inputs.length) hs hu

theorem multi_trit_carry_minimal :
    2 * (1 / 2) + 1 = 1 ∧
      2 * (2 / 2) + 1 = 3 ∧
      2 * (3 / 2) + 1 = 3 ∧
      2 * (4 / 2) + 1 = 5 := by
  native_decide

end Problems.BalancedTernary
