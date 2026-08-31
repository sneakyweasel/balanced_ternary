import Problems.Juggler.CycleCore
import Problems.Juggler.LengthEightCensus
import Problems.Juggler.Termination
import Problems.Juggler.TerminationFloor257
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.Complex.ExponentialBounds

namespace Problems.Juggler

/-!
# Cycle finance inequality

A cycle word is formally expanding (`2^L < 3^o`) yet returns
exactly, so the multiplicative surplus must be financed by the
floor defects, which are relatively `O(1/x)` in logarithms. The
whole-cycle log unroll gives, for any `CycleMin` start `n`,

`n * log n * (3^o - 2^L) ≤ L * 3^o`.

Every cycle state is at least `261`
(`cycleWord_iterate_not_lt_two_hundred_sixty_one`) and the
rotated minimum is odd (`cycleMin_start_odd`), so the minimum is
at least `261` and `n * log n ≥ 261 * log 257 > 15921/11`.
This excludes cycle lengths wholesale. The residual floor `261`
(`reachesOne_of_lt_two_hundred_sixty_one`) kills the cheap
leftovers `57` and `76`. Together with
`no_cycle_word_length_le_eighteen` the census extends to
`no_cycle_word_length_le_nineteen`, lengths `20`–`83` die by the
same comparison, and any remaining cycle has period `84` or at
least `85`.

Eliahou packaging (`cycle_word_eliahou_leftover`) rewrites that
leftover plus the computational finance table as: period `84`, or
a listed near-convergent, or at least `10^5`. Not a new inequality.

Dossier: `docs/problems/juggler_cycle_finance.md`. Writeup:
`docs/theory/juggler_cycle_finance_note.md`, absorbed into
Paper A (`docs/theory/juggler_finite_dynamics_note.md`) as
Section 4. The paper theorems are `cycleMin_finance`
(Theorem 4.4, constant 1) and `cycleMin_finance_inv_sum`
(Corollary 4.4c). The leftover
`84` is an Appendix A companion, not the printed leftover.
The height leftover
(`cycle_word_length_eighty_four_m_ge_three_or_ge_eighty_five`)
lives in `CycleHeightFinance.lean` and is not imported by
`Problems.JugglerPaper`. This is not a halt theorem
and not a leftover-word census named
`no_cycle_word_length_eleven`. Length `84` is the next record
near-convergent leftover at the Lean floor.
-/

/-- The dyadic-cell logarithm bound: if `z < (y+1)^2` then
`log z ≤ 2 log y + 2/y`. The only analytic input of the finance
inequality (`log(1+u) ≤ u`). -/
theorem log_le_two_log_add {z y : ℕ} (hz : 1 ≤ z) (hy : 1 ≤ y)
    (hcell : z < (y + 1) ^ 2) :
    Real.log z ≤ 2 * Real.log y + 2 / y := by
  have hy0 : (0 : ℝ) < y := by exact_mod_cast hy
  have hz0 : (0 : ℝ) < z := by exact_mod_cast hz
  have hcast : (z : ℝ) ≤ ((y : ℝ) + 1) ^ 2 := by
    have hle : (z : ℕ) ≤ (y + 1) ^ 2 := hcell.le
    exact_mod_cast hle
  have h1 : Real.log z ≤ 2 * Real.log ((y : ℝ) + 1) := by
    have hmono : Real.log z ≤ Real.log (((y : ℝ) + 1) ^ 2) := by
      gcongr
    rw [Real.log_pow] at hmono
    simpa using hmono
  have hsplit : Real.log (((y : ℝ) + 1) / y) =
      Real.log ((y : ℝ) + 1) - Real.log y :=
    Real.log_div (by positivity) (ne_of_gt hy0)
  have hbound : Real.log (((y : ℝ) + 1) / y) ≤ ((y : ℝ) + 1) / y - 1 :=
    Real.log_le_sub_one_of_pos (by positivity)
  have hfrac : ((y : ℝ) + 1) / y - 1 = 1 / y := by
    field_simp
    ring
  have h2 : Real.log ((y : ℝ) + 1) ≤ Real.log y + 1 / y := by
    rw [hsplit] at hbound
    rw [hfrac] at hbound
    linarith
  have h3 : 2 * Real.log ((y : ℝ) + 1) ≤ 2 * Real.log y + 2 / y := by
    have := mul_le_mul_of_nonneg_left h2 (by norm_num : (0 : ℝ) ≤ 2)
    calc 2 * Real.log ((y : ℝ) + 1) ≤ 2 * (Real.log y + 1 / y) := this
      _ = 2 * Real.log y + 2 / y := by ring
  linarith

/-- Even step: `log x ≤ 2 log T(x) + 2/T(x)`. -/
theorem log_step_even {x : ℕ} (hx : 2 ≤ x) (he : x % 2 = 0) :
    Real.log x ≤ 2 * Real.log (floorPower x) + 2 / (floorPower x) := by
  have hy : 1 ≤ floorPower x := floorPower_pos (by omega)
  have hcell :=
    (floorPower_even_eq_iff_sq_interval (n := x) (M := floorPower x) he).mp rfl
  exact log_le_two_log_add (by omega) hy hcell.2

/-- Odd step: `3 log x ≤ 2 log T(x) + 2/T(x)`. -/
theorem log_step_odd {x : ℕ} (hx : 2 ≤ x) (ho : x % 2 = 1) :
    3 * Real.log x ≤ 2 * Real.log (floorPower x) + 2 / (floorPower x) := by
  have hy : 1 ≤ floorPower x := floorPower_pos (by omega)
  have hcell :=
    (floorPower_odd_eq_iff_cube_interval (n := x) (M := floorPower x) ho).mp rfl
  have hz : 1 ≤ x ^ 3 := Nat.one_le_pow _ _ (by omega)
  have h := log_le_two_log_add hz hy hcell.2
  have hcast : ((x ^ 3 : ℕ) : ℝ) = ((x : ℝ)) ^ 3 := by push_cast; ring
  rw [hcast, Real.log_pow] at h
  simpa using h

/-- On a `CycleMin`, every iterate through one period is at least
the start (the boundary `j = L` returns to the start exactly). -/
theorem cycleMin_iterate_ge {n : ℕ} {w : List Branch} (h : CycleMin n w) :
    ∀ j, j ≤ w.length → n ≤ floorPower^[j] n := by
  intro j hj
  rcases lt_or_eq_of_le hj with hlt | heq
  · exact h.2 j hlt
  · rw [heq, cycle_iterate_period h.1]

/-- Prefix non-contraction on a `CycleMin`: an exponent-gap prefix
would contract strictly below the cycle minimum. -/
theorem cycleMin_prefix_pow_le {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∀ k, k ≤ w.length → 2 ^ k ≤ 3 ^ oddCount (w.take k) := by
  intro k hk
  by_contra hc
  push Not at hc
  have hf : follows n (w.take k) := follows_take w k h.1.1
  have hlen : (w.take k).length = k := by
    simp [List.length_take, Nat.min_eq_left hk]
  have hgap : 3 ^ oddCount (w.take k) < 2 ^ (w.take k).length := by
    rw [hlen]; exact hc
  have hcontr := power_bound_contracts hn hf hgap
  rw [hlen] at hcontr
  exact absurd hcontr (not_lt.mpr (cycleMin_iterate_ge h k hk))

/-- The unrolled financing envelope along a `CycleMin` prefix:
`3^{o_k} log n ≤ 2^k log x_k + k 3^{o_k} / n`. Division-free
induction; each step spends one dyadic-cell logarithm bound and one
prefix non-contraction fact. -/
theorem cycleMin_log_envelope {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∀ k, k ≤ w.length →
      (3 : ℝ) ^ oddCount (w.take k) * Real.log n ≤
        (2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
          (k : ℝ) * (3 : ℝ) ^ oddCount (w.take k) / n := by
  intro k
  induction k with
  | zero => intro _; simp
  | succ k ih =>
    intro hk1
    have hk : k < w.length := Nat.lt_of_succ_le hk1
    have ihk := ih (Nat.le_of_lt hk)
    have htake : w.take (k + 1) = w.take k ++ [w[k]] := by
      rw [List.take_add_one, List.getElem?_eq_getElem hk]
      rfl
    have hx2 : 2 ≤ floorPower^[k] n := cycleWord_iterate_ge_two hn h.1 hk
    have hiter : floorPower^[k + 1] n = floorPower (floorPower^[k] n) :=
      Function.iterate_succ_apply' floorPower k n
    have hxk1 : n ≤ floorPower^[k + 1] n := cycleMin_iterate_ge h (k + 1) hk1
    have hpow : 2 ^ (k + 1) ≤ 3 ^ oddCount (w.take (k + 1)) :=
      cycleMin_prefix_pow_le hn h (k + 1) hk1
    have hn0 : (0 : ℝ) < n := by
      have : 0 < n := by omega
      exact_mod_cast this
    have hx1pos : (0 : ℝ) < (floorPower^[k + 1] n : ℝ) := by
      have : 0 < floorPower^[k + 1] n := by omega
      exact_mod_cast this
    have hdiv : (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) ≤
        (3 : ℝ) ^ oddCount (w.take (k + 1)) / n := by
      rw [div_le_div_iff₀ hx1pos hn0]
      have hmul : (2 : ℕ) ^ (k + 1) * n ≤
          3 ^ oddCount (w.take (k + 1)) * floorPower^[k + 1] n :=
        Nat.mul_le_mul hpow hxk1
      exact_mod_cast hmul
    have h2k : (0 : ℝ) ≤ (2 : ℝ) ^ k := by positivity
    cases hb : w[k] with
    | even =>
      have hpar : (floorPower^[k] n) % 2 = 0 :=
        follows_get_even w h.1.1 k hk hb
      have hstep := log_step_even hx2 hpar
      rw [← hiter] at hstep
      have hodd : oddCount (w.take (k + 1)) = oddCount (w.take k) := by
        rw [htake, hb, oddCount_append]
        simp
      rw [hodd] at hdiv ⊢
      have hs2 := mul_le_mul_of_nonneg_left hstep h2k
      have hexpand : (2 : ℝ) ^ k *
          (2 * Real.log (floorPower^[k + 1] n) +
            2 / (floorPower^[k + 1] n : ℝ)) =
          (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
            (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) := by
        rw [pow_succ]; ring
      rw [hexpand] at hs2
      push_cast
      calc (3 : ℝ) ^ oddCount (List.take k w) * Real.log n
          ≤ (2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
              (k : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) / n := ihk
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              (k : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) / n :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (3 : ℝ) ^ oddCount (List.take k w) / n) +
              (k : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) / n := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              ((k : ℝ) + 1) * (3 : ℝ) ^ oddCount (List.take k w) / n := by
            ring
    | odd =>
      have hpar : (floorPower^[k] n) % 2 = 1 :=
        follows_get_odd w h.1.1 k hk hb
      have hstep := log_step_odd hx2 hpar
      rw [← hiter] at hstep
      have hodd : oddCount (w.take (k + 1)) = oddCount (w.take k) + 1 := by
        rw [htake, hb, oddCount_append]
        simp
      rw [hodd] at hdiv ⊢
      have hs2 := mul_le_mul_of_nonneg_left hstep h2k
      have hexpand : (2 : ℝ) ^ k *
          (2 * Real.log (floorPower^[k + 1] n) +
            2 / (floorPower^[k + 1] n : ℝ)) =
          (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
            (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) := by
        rw [pow_succ]; ring
      rw [hexpand] at hs2
      have ihk3 := mul_le_mul_of_nonneg_left ihk (by norm_num : (0 : ℝ) ≤ 3)
      have hpow_succ : (3 : ℝ) ^ (oddCount (w.take k) + 1) =
          3 * (3 : ℝ) ^ oddCount (w.take k) := by
        rw [pow_succ]; ring
      rw [hpow_succ] at hdiv ⊢
      push_cast
      calc (3 : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) * Real.log n
          = 3 * ((3 : ℝ) ^ oddCount (List.take k w) * Real.log n) := by ring
        _ ≤ 3 * ((2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
              (k : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) / n) := ihk3
        _ = (2 : ℝ) ^ k * (3 * Real.log (floorPower^[k] n)) +
              (k : ℝ) * (3 * (3 : ℝ) ^ oddCount (List.take k w)) / n := by
            ring
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              (k : ℝ) * (3 * (3 : ℝ) ^ oddCount (List.take k w)) / n :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) / n) +
              (k : ℝ) * (3 * (3 : ℝ) ^ oddCount (List.take k w)) / n := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              ((k : ℝ) + 1) * (3 * (3 : ℝ) ^ oddCount (List.take k w)) / n := by
            ring

/-- **Cycle finance inequality.** For any cycle taken at its
minimum: `n log n (3^o - 2^L) ≤ L 3^o`. -/
theorem cycleMin_finance {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    (n : ℝ) * Real.log n *
        ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
  have henv := cycleMin_log_envelope hn h w.length le_rfl
  rw [List.take_length, cycle_iterate_period h.1] at henv
  have hn0 : (0 : ℝ) < n := by
    have : 0 < n := by omega
    exact_mod_cast this
  have hstep : ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) * Real.log n ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w / n := by linarith
  have hmul := mul_le_mul_of_nonneg_left hstep hn0.le
  calc (n : ℝ) * Real.log n *
      ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length)
      = (n : ℝ) * (((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) *
          Real.log n) := by ring
    _ ≤ (n : ℝ) * ((w.length : ℝ) * (3 : ℝ) ^ oddCount w / n) := hmul
    _ = (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
        field_simp

/-- On a `CycleMin`, every iterate through one period is at least
two (the start is, and later states are at least the start). -/
theorem cycleMin_iterate_ge_two {n : ℕ} {w : List Branch} {k : ℕ}
    (hn : 2 ≤ n) (h : CycleMin n w) (hk : k ≤ w.length) :
    2 ≤ floorPower^[k] n := by
  rcases lt_or_eq_of_le hk with hlt | rfl
  · exact cycleWord_iterate_ge_two hn h.1 hlt
  · rw [cycle_iterate_period h.1]
    exact hn

/-- Inv-sum envelope: each dyadic-cell defect is kept as `1/x_{i+1}`
instead of being replaced by `1/n`. At `k = L` this is
`(3^o - 2^L) log n ≤ 3^o ∑ 1/x_i`. Paper A Corollary 4.4c. -/
theorem cycleMin_log_envelope_inv {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∀ k, k ≤ w.length →
      (3 : ℝ) ^ oddCount (w.take k) * Real.log n ≤
        (2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
          (3 : ℝ) ^ oddCount (w.take k) *
            ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
  intro k
  induction k with
  | zero => intro _; simp
  | succ k ih =>
    intro hk1
    have hk : k < w.length := Nat.lt_of_succ_le hk1
    have ihk := ih (Nat.le_of_lt hk)
    have htake : w.take (k + 1) = w.take k ++ [w[k]] := by
      rw [List.take_add_one, List.getElem?_eq_getElem hk]
      rfl
    have hx2 : 2 ≤ floorPower^[k] n := cycleMin_iterate_ge_two hn h (Nat.le_of_lt hk)
    have hx21 : 2 ≤ floorPower^[k + 1] n := cycleMin_iterate_ge_two hn h hk1
    have hiter : floorPower^[k + 1] n = floorPower (floorPower^[k] n) :=
      Function.iterate_succ_apply' floorPower k n
    have hpow : 2 ^ (k + 1) ≤ 3 ^ oddCount (w.take (k + 1)) :=
      cycleMin_prefix_pow_le hn h (k + 1) hk1
    have hx1pos : (0 : ℝ) < (floorPower^[k + 1] n : ℝ) := by
      have : 0 < floorPower^[k + 1] n := by omega
      exact_mod_cast this
    have h2le3 : (2 : ℝ) ^ (k + 1) ≤ (3 : ℝ) ^ oddCount (w.take (k + 1)) := by
      exact_mod_cast hpow
    have hsum : ∑ i ∈ Finset.range (k + 1), (1 : ℝ) / (floorPower^[i + 1] n) =
        (∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
          1 / (floorPower^[k + 1] n) :=
      Finset.sum_range_succ (fun i => (1 : ℝ) / (floorPower^[i + 1] n)) k
    have h2k : (0 : ℝ) ≤ (2 : ℝ) ^ k := by positivity
    cases hb : w[k] with
    | even =>
      have hpar : (floorPower^[k] n) % 2 = 0 :=
        follows_get_even w h.1.1 k hk hb
      have hstep := log_step_even hx2 hpar
      rw [← hiter] at hstep
      have hodd : oddCount (w.take (k + 1)) = oddCount (w.take k) := by
        rw [htake, hb, oddCount_append]
        simp
      rw [hodd] at h2le3 ⊢
      have hs2 := mul_le_mul_of_nonneg_left hstep h2k
      have hexpand : (2 : ℝ) ^ k *
          (2 * Real.log (floorPower^[k + 1] n) +
            2 / (floorPower^[k + 1] n : ℝ)) =
          (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
            (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) := by
        rw [pow_succ]; ring
      rw [hexpand] at hs2
      have hdef :
          (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) ≤
            (3 : ℝ) ^ oddCount (w.take k) / (floorPower^[k + 1] n : ℝ) := by
        exact div_le_div_of_nonneg_right h2le3 hx1pos.le
      rw [hsum]
      push_cast
      calc (3 : ℝ) ^ oddCount (List.take k w) * Real.log n
          ≤ (2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) := ihk
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (3 : ℝ) ^ oddCount (List.take k w) /
                (floorPower^[k + 1] n : ℝ)) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ((∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
                  1 / (floorPower^[k + 1] n)) := by
            ring
    | odd =>
      have hpar : (floorPower^[k] n) % 2 = 1 :=
        follows_get_odd w h.1.1 k hk hb
      have hstep := log_step_odd hx2 hpar
      rw [← hiter] at hstep
      have hodd : oddCount (w.take (k + 1)) = oddCount (w.take k) + 1 := by
        rw [htake, hb, oddCount_append]
        simp
      rw [hodd] at h2le3 ⊢
      have hs2 := mul_le_mul_of_nonneg_left hstep h2k
      have hexpand : (2 : ℝ) ^ k *
          (2 * Real.log (floorPower^[k + 1] n) +
            2 / (floorPower^[k + 1] n : ℝ)) =
          (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
            (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) := by
        rw [pow_succ]; ring
      rw [hexpand] at hs2
      have ihk3 := mul_le_mul_of_nonneg_left ihk (by norm_num : (0 : ℝ) ≤ 3)
      have hpow_succ : (3 : ℝ) ^ (oddCount (w.take k) + 1) =
          3 * (3 : ℝ) ^ oddCount (w.take k) := by
        rw [pow_succ]; ring
      rw [hpow_succ] at h2le3 ⊢
      have hdef :
          (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ) ≤
            3 * (3 : ℝ) ^ oddCount (w.take k) /
              (floorPower^[k + 1] n : ℝ) :=
        div_le_div_of_nonneg_right h2le3 hx1pos.le
      rw [hsum]
      push_cast
      calc (3 : ℝ) * (3 : ℝ) ^ oddCount (List.take k w) * Real.log n
          = 3 * ((3 : ℝ) ^ oddCount (List.take k w) * Real.log n) := by ring
        _ ≤ 3 * ((2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n)) := ihk3
        _ = (2 : ℝ) ^ k * (3 * Real.log (floorPower^[k] n)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            ring
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) /
                (floorPower^[k + 1] n : ℝ)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ((∑ i ∈ Finset.range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
                  1 / (floorPower^[k + 1] n)) := by
            ring

/-- **Inv-sum finance inequality.** Same cell-log defects as
`cycleMin_finance`, remainders kept as `1/x_{i+1}`.
`(3^o - 2^L) log n ≤ 3^o ∑ 1/x_i`. -/
theorem cycleMin_finance_inv_sum {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) * Real.log n ≤
      (3 : ℝ) ^ oddCount w *
        ∑ i ∈ Finset.range w.length, (1 : ℝ) / (floorPower^[i + 1] n) := by
  have henv := cycleMin_log_envelope_inv hn h w.length le_rfl
  rw [List.take_length, cycle_iterate_period h.1] at henv
  linarith

/-- Rotation preserves the odd count. -/
theorem oddCount_rotateWord : ∀ (k : ℕ) (w : List Branch),
    oddCount (rotateWord w k) = oddCount w := by
  intro k
  induction k with
  | zero => intro w; rfl
  | succ k ih =>
    intro w
    cases w with
    | nil => rfl
    | cons b rest =>
      have hrot : rotateWord (b :: rest) (k + 1) =
          rotateWord (rest ++ [b]) k := rfl
      rw [hrot, ih, oddCount_append]
      cases b <;> simp [oddCount]

/-- Numeric certificate `log 13 > 5/2`, via `e^5 < 169`. -/
theorem log_thirteen_gt : (5 / 2 : ℝ) < Real.log 13 := by
  rw [Real.lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 13)]
  have hsq : Real.exp (5 / 2) ^ 2 = Real.exp 5 := by
    rw [sq, ← Real.exp_add]
    norm_num
  have hpow : Real.exp 1 ^ (5 : ℕ) = Real.exp 5 := by
    rw [← Real.exp_nat_mul]
    norm_num
  have hlt : Real.exp 1 ^ (5 : ℕ) < (2.7182818286 : ℝ) ^ (5 : ℕ) := by
    gcongr
    exact Real.exp_one_lt_d9
  have hnum : (2.7182818286 : ℝ) ^ (5 : ℕ) < 169 := by norm_num
  have h169 : Real.exp (5 / 2) ^ 2 < 169 := by
    rw [hsq, ← hpow]
    linarith
  nlinarith [Real.exp_pos (5 / 2 : ℝ), h169,
    sq_nonneg (Real.exp (5 / 2) - 13)]

/-- Finance at the rotated odd minimum: every cycle word satisfies
`(65/2)(3^o - 2^L) ≤ L 3^o`, because the minimum is at least `13`
and `13 log 13 > 65/2`. -/
theorem cycle_finance_min_thirteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    (65 / 2 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
  obtain ⟨k, hkL, hmin⟩ := exists_cycleMin hn h
  have hm12 : 12 ≤ floorPower^[k] n := cycleWord_iterate_not_lt_twelve hn h
  have hm2 : 2 ≤ floorPower^[k] n := by omega
  have hmodd : (floorPower^[k] n) % 2 = 1 := cycleMin_start_odd hm2 hmin
  have hm13 : 13 ≤ floorPower^[k] n := by omega
  have hfin := cycleMin_finance hm2 hmin
  rw [rotateWord_length, oddCount_rotateWord] at hfin
  have hexpand : (2 : ℝ) ^ w.length < (3 : ℝ) ^ oddCount w := by
    exact_mod_cast cycle_word_formally_expanding hn h
  have hm13R : (13 : ℝ) ≤ (floorPower^[k] n : ℝ) := by exact_mod_cast hm13
  have hlog : (5 / 2 : ℝ) ≤ Real.log (floorPower^[k] n) := by
    have hmono : Real.log (13 : ℝ) ≤ Real.log (floorPower^[k] n) := by
      gcongr
    linarith [log_thirteen_gt]
  have hmlog : (65 / 2 : ℝ) ≤
      (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) := by
    have h1 : (13 : ℝ) * (5 / 2) ≤
        (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) :=
      mul_le_mul hm13R hlog (by norm_num) (by linarith)
    linarith
  calc (65 / 2 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length)
      ≤ (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) *
          ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) :=
        mul_le_mul_of_nonneg_right hmlog (by linarith)
    _ ≤ (w.length : ℝ) * (3 : ℝ) ^ oddCount w := hfin

/-- No cycle word of length `9`: `o ≥ 6` forces
`(65/2)(3^o - 512) > 9 · 3^o`. -/
theorem no_cycle_word_length_nine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 9) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_thirteen hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 6 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 5 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 9 < 3 ^ 5 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (729 : ℕ) ≤ 3 ^ oddCount w := by
    calc (729 : ℕ) = 3 ^ 6 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (729 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- No cycle word of length `10`: `o ≥ 7` forces
`(65/2)(3^o - 1024) > 10 · 3^o`. -/
theorem no_cycle_word_length_ten {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 10) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_thirteen hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 7 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 6 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 10 < 3 ^ 6 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (2187 : ℕ) ≤ 3 ^ oddCount w := by
    calc (2187 : ℕ) = 3 ^ 7 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (2187 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- No cycle word of length `12`: `o ≥ 8` forces
`(65/2)(3^o - 4096) > 12 · 3^o` (margin `6561 > 6494`). -/
theorem no_cycle_word_length_twelve {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 12) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_thirteen hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 8 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 7 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 12 < 3 ^ 7 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (6561 : ℕ) ≤ 3 ^ oddCount w := by
    calc (6561 : ℕ) = 3 ^ 8 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (6561 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- No cycle word of length `13`: `o ≥ 9` forces
`(65/2)(3^o - 8192) > 13 · 3^o`. -/
theorem no_cycle_word_length_thirteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 13) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_thirteen hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 9 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 8 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 13 < 3 ^ 8 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (19683 : ℕ) ≤ 3 ^ oddCount w := by
    calc (19683 : ℕ) = 3 ^ 9 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (19683 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- No cycle word of length `16`: `o ≥ 11` forces
`(65/2)(3^o - 65536) > 16 · 3^o`. -/
theorem no_cycle_word_length_sixteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 16) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_thirteen hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 11 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 10 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 16 < 3 ^ 10 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (177147 : ℕ) ≤ 3 ^ oddCount w := by
    calc (177147 : ℕ) = 3 ^ 11 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (177147 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- Census extension: no cycle word of length at most `10`.
Lengths `≤ 8` are the Lean census; `9` and `10` are the finance
inequality. -/
theorem no_cycle_word_length_le_ten {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length ≤ 10) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 9 with h9 | h9
  · exact no_cycle_word_length_le_eight hn (by omega) h
  · rcases Nat.lt_or_ge w.length 10 with h10 | h10
    · exact no_cycle_word_length_nine hn (by omega) h
    · exact no_cycle_word_length_ten hn (by omega) h

/-- If a nontrivial cycle exists, its period is `11` or at least
`14`: lengths `≤ 10`, `12`, and `13` are impossible. -/
theorem cycle_word_length_eleven_or_ge_fourteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 11 ∨ 14 ≤ w.length := by
  by_contra hc
  push Not at hc
  obtain ⟨h11, h14⟩ := hc
  have hsplit : w.length ≤ 10 ∨ w.length = 12 ∨ w.length = 13 := by omega
  rcases hsplit with hle | h12 | h13
  · exact no_cycle_word_length_le_ten hn hle h
  · exact no_cycle_word_length_twelve hn h12 h
  · exact no_cycle_word_length_thirteen hn h13 h

/-- Residual class `{1,…,52}` is disjoint from a nontrivial cycle. -/
theorem cycleWord_iterate_not_lt_fifty_three {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    53 ≤ floorPower^[i] n := by
  by_contra h53
  have hmod : floorPower^[i] n = floorPower^[i % w.length] n :=
    cycle_iterate_mod h
  have hlenpos : 0 < w.length :=
    lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2
  have hlt : i % w.length < w.length := Nat.mod_lt i hlenpos
  have hge := cycleWord_iterate_ge_two hn h hlt
  have hpos : 1 ≤ floorPower^[i] n := by
    have : 2 ≤ floorPower^[i % w.length] n := hge
    exact le_trans (by decide : (1 : ℕ) ≤ 2) (by simpa [hmod] using this)
  have hy : floorPower^[i] n < 53 := Nat.lt_of_not_ge h53
  have hR : ReachesOne (floorPower^[i] n) :=
    reachesOne_of_lt_fifty_three hpos hy
  exact cycleWord_not_reachesOne hn h (reachesOne_of_iterate rfl hR)

/-- Numeric certificate `log 53 > 7/2`, via `e < 3` and `3^7 < 53^2`. -/
theorem log_fifty_three_gt : (7 / 2 : ℝ) < Real.log 53 := by
  rw [Real.lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 53)]
  have hsq : Real.exp (7 / 2) ^ 2 = Real.exp 7 := by
    rw [sq, ← Real.exp_add]
    norm_num
  have hpow : Real.exp 1 ^ (7 : ℕ) = Real.exp 7 := by
    rw [← Real.exp_nat_mul]
    norm_num
  have hlt : Real.exp 1 ^ (7 : ℕ) < (3 : ℝ) ^ (7 : ℕ) := by
    gcongr
    exact Real.exp_one_lt_three
  have hnum : (3 : ℝ) ^ (7 : ℕ) < (53 : ℝ) ^ 2 := by norm_num
  have h2809 : Real.exp (7 / 2) ^ 2 < (53 : ℝ) ^ 2 := by
    rw [hsq, ← hpow]
    linarith
  nlinarith [Real.exp_pos (7 / 2 : ℝ), h2809,
    sq_nonneg (Real.exp (7 / 2) - 53)]

/-- Finance at the rotated odd minimum after the residual floor `53`:
`(371/2)(3^o - 2^L) ≤ L 3^o`, because the minimum is at least `53`
and `53 log 53 > 371/2`. -/
theorem cycle_finance_min_fifty_three {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    (371 / 2 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
  obtain ⟨k, hkL, hmin⟩ := exists_cycleMin hn h
  have hm53 : 53 ≤ floorPower^[k] n :=
    cycleWord_iterate_not_lt_fifty_three hn h
  have hm2 : 2 ≤ floorPower^[k] n := by omega
  have hfin := cycleMin_finance hm2 hmin
  rw [rotateWord_length, oddCount_rotateWord] at hfin
  have hexpand : (2 : ℝ) ^ w.length < (3 : ℝ) ^ oddCount w := by
    exact_mod_cast cycle_word_formally_expanding hn h
  have hm53R : (53 : ℝ) ≤ (floorPower^[k] n : ℝ) := by exact_mod_cast hm53
  have hlog : (7 / 2 : ℝ) ≤ Real.log (floorPower^[k] n) := by
    have hmono : Real.log (53 : ℝ) ≤ Real.log (floorPower^[k] n) := by
      gcongr
    linarith [log_fifty_three_gt]
  have hmlog : (371 / 2 : ℝ) ≤
      (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) := by
    have h1 : (53 : ℝ) * (7 / 2) ≤
        (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) :=
      mul_le_mul hm53R hlog (by norm_num) (by linarith)
    linarith
  calc (371 / 2 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length)
      ≤ (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) *
          ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) :=
        mul_le_mul_of_nonneg_right hmlog (by linarith)
    _ ≤ (w.length : ℝ) * (3 : ℝ) ^ oddCount w := hfin

/-- Finance excludes length `11`: `o ≥ 7` forces
`(371/2)(3^o - 2048) > 11 · 3^o`. Not a leftover-word census. -/
theorem finance_excludes_length_eleven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 11) : ¬CycleWord n w := by
  intro h
  have hfin := cycle_finance_min_fifty_three hn h
  have hexp := cycle_word_formally_expanding hn h
  rw [hlen] at hfin hexp
  have ho : 7 ≤ oddCount w := by
    by_contra hc
    push Not at hc
    have hle : (3 : ℕ) ^ oddCount w ≤ 3 ^ 6 :=
      Nat.pow_le_pow_right (by norm_num) (by omega)
    have : (2 : ℕ) ^ 11 < 3 ^ 6 := lt_of_lt_of_le hexp hle
    norm_num at this
  have hA : (2187 : ℕ) ≤ 3 ^ oddCount w := by
    calc (2187 : ℕ) = 3 ^ 7 := by norm_num
      _ ≤ 3 ^ oddCount w := Nat.pow_le_pow_right (by norm_num) ho
  have hAR : (2187 : ℝ) ≤ (3 : ℝ) ^ oddCount w := by exact_mod_cast hA
  norm_num at hfin
  linarith

/-- Census extension: no cycle word of length at most `11`.
Lengths `≤ 10` are the prior census; `11` is finance at the
residual floor `53`. -/
theorem no_cycle_word_length_le_eleven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length ≤ 11) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 11 with h11 | h11
  · exact no_cycle_word_length_le_ten hn (by omega) h
  · exact finance_excludes_length_eleven hn (by omega) h

/-- If a nontrivial cycle exists, its period is at least `14`.
Corollary of the floor-`53` leftover; lengths `14`–`18` and
`20`–`29` are excluded separately. -/
theorem cycle_word_length_ge_fourteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) : 14 ≤ w.length := by
  rcases cycle_word_length_eleven_or_ge_fourteen hn h with h11 | h14
  · exact absurd h (finance_excludes_length_eleven hn h11)
  · exact h14

/-- Formal expansion forces more odds than any `o0` with `3^{o0} ≤ 2^L`. -/
theorem cycle_oddCount_gt_of_three_pow_le {n : ℕ} {w : List Branch} {o0 : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w)
    (hle : 3 ^ o0 ≤ 2 ^ w.length) : o0 < oddCount w := by
  have hexp := cycle_word_formally_expanding hn h
  have : 3 ^ o0 < 3 ^ oddCount w := lt_of_le_of_lt hle hexp
  exact (Nat.pow_lt_pow_iff_right (by norm_num : (1 : ℕ) < 3)).mp this

/-- If the floor-`53` comparison already fails at the minimal
admissible `3^{o0}`, it fails for every larger odd count. Requires
`L < 371/2` so the comparison is increasing in `3^o`. -/
theorem finance_contradicts_min_fifty_three {n : ℕ} {w : List Branch}
    {L o0 : ℕ} (hn : 2 ≤ n) (h : CycleWord n w)
    (hlen : w.length = L) (hL : (L : ℝ) < 371 / 2)
    (ho : o0 ≤ oddCount w)
    (hnum : (371 / 2 : ℝ) * ((3 : ℝ) ^ o0 - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ o0) : False := by
  have hfin := cycle_finance_min_fifty_three hn h
  rw [hlen] at hfin
  have hA : (3 : ℝ) ^ o0 ≤ (3 : ℝ) ^ oddCount w := by
    have : (3 : ℕ) ^ o0 ≤ 3 ^ oddCount w :=
      Nat.pow_le_pow_right (by norm_num) ho
    exact_mod_cast this
  have hc : (0 : ℝ) < 371 / 2 - L := sub_pos.mpr hL
  have hnum' : (371 / 2 - (L : ℝ)) * (3 : ℝ) ^ o0 >
      (371 / 2) * (2 : ℝ) ^ L := by nlinarith
  have hfin' : (371 / 2 - (L : ℝ)) * (3 : ℝ) ^ oddCount w ≤
      (371 / 2) * (2 : ℝ) ^ L := by nlinarith
  have hleA : (3 : ℝ) ^ oddCount w ≤ (3 : ℝ) ^ o0 :=
    le_of_mul_le_mul_left (le_trans hfin' hnum'.le) hc
  have heq : (3 : ℝ) ^ oddCount w = (3 : ℝ) ^ o0 := le_antisymm hleA hA
  rw [heq] at hfin'
  exact not_le_of_gt hnum' hfin'

/-- Instantiate the floor-`53` comparison at a concrete length. -/
theorem finance_excludes_at {n : ℕ} {w : List Branch} {L oPred : ℕ}
    (hn : 2 ≤ n) (hlen : w.length = L)
    (hL : (L : ℝ) < 371 / 2)
    (hpred : 3 ^ oPred ≤ 2 ^ L)
    (hnum : (371 / 2 : ℝ) * ((3 : ℝ) ^ (oPred + 1) - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ (oPred + 1)) :
    ¬CycleWord n w := by
  intro h
  have hpred' : 3 ^ oPred ≤ 2 ^ w.length := by simpa [hlen] using hpred
  have ho : oPred + 1 ≤ oddCount w :=
    Nat.succ_le_of_lt (cycle_oddCount_gt_of_three_pow_le hn h hpred')
  exact finance_contradicts_min_fifty_three hn h hlen hL ho hnum

theorem finance_excludes_length_fourteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 14) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 8 ≤ 2 ^ 14) (by norm_num)

theorem finance_excludes_length_fifteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 15) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 9 ≤ 2 ^ 15) (by norm_num)

theorem finance_excludes_length_seventeen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 17) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 10 ≤ 2 ^ 17) (by norm_num)

theorem finance_excludes_length_eighteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 18) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 11 ≤ 2 ^ 18) (by norm_num)

theorem finance_excludes_length_twenty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 20) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 12 ≤ 2 ^ 20) (by norm_num)

theorem finance_excludes_length_twentyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 21) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 13 ≤ 2 ^ 21) (by norm_num)

theorem finance_excludes_length_twentytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 22) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 13 ≤ 2 ^ 22) (by norm_num)

theorem finance_excludes_length_twentythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 23) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 14 ≤ 2 ^ 23) (by norm_num)

theorem finance_excludes_length_twentyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 24) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 15 ≤ 2 ^ 24) (by norm_num)

theorem finance_excludes_length_twentyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 25) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 15 ≤ 2 ^ 25) (by norm_num)

theorem finance_excludes_length_twentysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 26) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 16 ≤ 2 ^ 26) (by norm_num)

theorem finance_excludes_length_twentyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 27) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 17 ≤ 2 ^ 27) (by norm_num)

theorem finance_excludes_length_twentyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 28) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 17 ≤ 2 ^ 28) (by norm_num)

theorem finance_excludes_length_twentynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 29) : ¬CycleWord n w :=
  finance_excludes_at hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 18 ≤ 2 ^ 29) (by norm_num)

/-- Census extension: no cycle word of length at most `18`.
Length `11` is the near-convergent killed by the floor `53`;
`14`–`18` die by the same comparison. -/
theorem no_cycle_word_length_le_eighteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length ≤ 18) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 12 with h11 | h12
  · exact no_cycle_word_length_le_eleven hn (Nat.lt_succ_iff.mp h11) h
  · have hsplit : w.length = 12 ∨ w.length = 13 ∨ w.length = 14 ∨
        w.length = 15 ∨ w.length = 16 ∨ w.length = 17 ∨ w.length = 18 := by
      omega
    rcases hsplit with hL | hL | hL | hL | hL | hL | hL
    · exact no_cycle_word_length_twelve hn hL h
    · exact no_cycle_word_length_thirteen hn hL h
    · exact finance_excludes_length_fourteen hn hL h
    · exact finance_excludes_length_fifteen hn hL h
    · exact no_cycle_word_length_sixteen hn hL h
    · exact finance_excludes_length_seventeen hn hL h
    · exact finance_excludes_length_eighteen hn hL h

/-- No cycle word of length below `30` except possibly `19`. -/
theorem no_cycle_word_length_lt_thirty_ne_nineteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hLt : w.length < 30) (hne : w.length ≠ 19) :
    ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 19 with h18 | h19
  · exact no_cycle_word_length_le_eighteen hn (Nat.le_of_lt_succ h18) h
  · have hge : 20 ≤ w.length :=
      Nat.succ_le_of_lt (lt_of_le_of_ne h19 hne.symm)
    have hsplit : w.length = 20 ∨ w.length = 21 ∨ w.length = 22 ∨
        w.length = 23 ∨ w.length = 24 ∨ w.length = 25 ∨ w.length = 26 ∨
        w.length = 27 ∨ w.length = 28 ∨ w.length = 29 := by
      omega
    rcases hsplit with hL | hL | hL | hL | hL | hL | hL | hL | hL | hL
    · exact finance_excludes_length_twenty hn hL h
    · exact finance_excludes_length_twentyone hn hL h
    · exact finance_excludes_length_twentytwo hn hL h
    · exact finance_excludes_length_twentythree hn hL h
    · exact finance_excludes_length_twentyfour hn hL h
    · exact finance_excludes_length_twentyfive hn hL h
    · exact finance_excludes_length_twentysix hn hL h
    · exact finance_excludes_length_twentyseven hn hL h
    · exact finance_excludes_length_twentyeight hn hL h
    · exact finance_excludes_length_twentynine hn hL h

/-- If a nontrivial cycle exists, its period is `19` or at least `30`.
The gap `20..29` dies by finance at the residual floor `53`; `19` is
the next near-convergent (`2^19 < 3^12`). -/
theorem cycle_word_length_nineteen_or_ge_thirty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 19 ∨ 30 ≤ w.length := by
  by_contra hc
  push Not at hc
  obtain ⟨h19, h30⟩ := hc
  exact no_cycle_word_length_lt_thirty_ne_nineteen hn (by omega) h19 h

/-- Weaker leftover: period is `19` or at least `20`. -/
theorem cycle_word_length_nineteen_or_ge_twenty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 19 ∨ 20 ≤ w.length := by
  rcases cycle_word_length_nineteen_or_ge_thirty hn h with h19 | h30
  · exact Or.inl h19
  · exact Or.inr (le_trans (by decide : (20 : ℕ) ≤ 30) h30)

/-- Residual class `{1,…,256}` is disjoint from a nontrivial cycle. -/
theorem cycleWord_iterate_not_lt_two_hundred_fifty_seven
    {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    257 ≤ floorPower^[i] n := by
  by_contra h257
  have hmod : floorPower^[i] n = floorPower^[i % w.length] n :=
    cycle_iterate_mod h
  have hlenpos : 0 < w.length :=
    lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2
  have hlt : i % w.length < w.length := Nat.mod_lt i hlenpos
  have hge := cycleWord_iterate_ge_two hn h hlt
  have hpos : 1 ≤ floorPower^[i] n := by
    have : 2 ≤ floorPower^[i % w.length] n := hge
    exact le_trans (by decide : (1 : ℕ) ≤ 2) (by simpa [hmod] using this)
  have hy : floorPower^[i] n < 257 := Nat.lt_of_not_ge h257
  have hR : ReachesOne (floorPower^[i] n) :=
    reachesOne_of_lt_two_hundred_fifty_seven hpos hy
  exact cycleWord_not_reachesOne hn h (reachesOne_of_iterate rfl hR)

/-- Residual class `{1,…,260}` is disjoint from a nontrivial cycle. -/
theorem cycleWord_iterate_not_lt_two_hundred_sixty_one
    {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    261 ≤ floorPower^[i] n := by
  by_contra h261
  have hmod : floorPower^[i] n = floorPower^[i % w.length] n :=
    cycle_iterate_mod h
  have hlenpos : 0 < w.length :=
    lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2
  have hlt : i % w.length < w.length := Nat.mod_lt i hlenpos
  have hge := cycleWord_iterate_ge_two hn h hlt
  have hpos : 1 ≤ floorPower^[i] n := by
    have : 2 ≤ floorPower^[i % w.length] n := hge
    exact le_trans (by decide : (1 : ℕ) ≤ 2) (by simpa [hmod] using this)
  have hy : floorPower^[i] n < 261 := Nat.lt_of_not_ge h261
  have hR : ReachesOne (floorPower^[i] n) :=
    reachesOne_of_lt_two_hundred_sixty_one hpos hy
  exact cycleWord_not_reachesOne hn h (reachesOne_of_iterate rfl hR)

/-- Numeric certificate `log 257 > 61/11`, via `e < 2.7182818286`
and `e^61 < 257^11`. -/
theorem log_two_hundred_fifty_seven_gt : (61 / 11 : ℝ) < Real.log 257 := by
  rw [Real.lt_log_iff_exp_lt (by norm_num : (0 : ℝ) < 257)]
  have hpow : Real.exp (61 / 11) ^ (11 : ℕ) = Real.exp 61 := by
    rw [← Real.exp_nat_mul]
    norm_num
  have he : Real.exp 1 ^ (61 : ℕ) = Real.exp 61 := by
    rw [← Real.exp_nat_mul]
    norm_num
  have hlt : Real.exp 1 ^ (61 : ℕ) < (2.7182818286 : ℝ) ^ (61 : ℕ) := by
    gcongr
    exact Real.exp_one_lt_d9
  have hnum : (2.7182818286 : ℝ) ^ (61 : ℕ) < (257 : ℝ) ^ (11 : ℕ) := by
    norm_num
  have h11 : Real.exp (61 / 11) ^ (11 : ℕ) < (257 : ℝ) ^ (11 : ℕ) := by
    rw [hpow, ← he]
    linarith
  refine (pow_lt_pow_iff_left₀ ?_ ?_ (by norm_num : (11 : ℕ) ≠ 0)).1 h11
  · exact (Real.exp_pos _).le
  · norm_num

/-- Finance at the rotated odd minimum after the residual floor `257`:
`(15677/11)(3^o - 2^L) ≤ L 3^o`, because the minimum is at least `257`
and `257 log 257 > 15677/11`. -/
theorem cycle_finance_min_two_hundred_fifty_seven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    (15677 / 11 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
  obtain ⟨k, hkL, hmin⟩ := exists_cycleMin hn h
  have hm257 : 257 ≤ floorPower^[k] n :=
    cycleWord_iterate_not_lt_two_hundred_fifty_seven hn h
  have hm2 : 2 ≤ floorPower^[k] n := by omega
  have hfin := cycleMin_finance hm2 hmin
  rw [rotateWord_length, oddCount_rotateWord] at hfin
  have hexpand : (2 : ℝ) ^ w.length < (3 : ℝ) ^ oddCount w := by
    exact_mod_cast cycle_word_formally_expanding hn h
  have hm257R : (257 : ℝ) ≤ (floorPower^[k] n : ℝ) := by exact_mod_cast hm257
  have hlog : (61 / 11 : ℝ) ≤ Real.log (floorPower^[k] n) := by
    have hmono : Real.log (257 : ℝ) ≤ Real.log (floorPower^[k] n) := by
      gcongr
    linarith [log_two_hundred_fifty_seven_gt]
  have hmlog : (15677 / 11 : ℝ) ≤
      (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) := by
    have h1 : (257 : ℝ) * (61 / 11) ≤
        (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) :=
      mul_le_mul hm257R hlog (by norm_num) (by linarith)
    linarith
  calc (15677 / 11 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length)
      ≤ (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) *
          ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) :=
        mul_le_mul_of_nonneg_right hmlog (by linarith)
    _ ≤ (w.length : ℝ) * (3 : ℝ) ^ oddCount w := hfin

/-- If the floor-`257` comparison already fails at the minimal
admissible `3^{o0}`, it fails for every larger odd count. Requires
`L < 15677/11` so the comparison is increasing in `3^o`. -/
theorem finance_contradicts_min_two_hundred_fifty_seven
    {n : ℕ} {w : List Branch} {L o0 : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w)
    (hlen : w.length = L) (hL : (L : ℝ) < 15677 / 11)
    (ho : o0 ≤ oddCount w)
    (hnum : (15677 / 11 : ℝ) * ((3 : ℝ) ^ o0 - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ o0) : False := by
  have hfin := cycle_finance_min_two_hundred_fifty_seven hn h
  rw [hlen] at hfin
  have hA : (3 : ℝ) ^ o0 ≤ (3 : ℝ) ^ oddCount w := by
    have : (3 : ℕ) ^ o0 ≤ 3 ^ oddCount w :=
      Nat.pow_le_pow_right (by norm_num) ho
    exact_mod_cast this
  have hc : (0 : ℝ) < 15677 / 11 - L := sub_pos.mpr hL
  have hnum' : (15677 / 11 - (L : ℝ)) * (3 : ℝ) ^ o0 >
      (15677 / 11) * (2 : ℝ) ^ L := by nlinarith
  have hfin' : (15677 / 11 - (L : ℝ)) * (3 : ℝ) ^ oddCount w ≤
      (15677 / 11) * (2 : ℝ) ^ L := by nlinarith
  have hleA : (3 : ℝ) ^ oddCount w ≤ (3 : ℝ) ^ o0 :=
    le_of_mul_le_mul_left (le_trans hfin' hnum'.le) hc
  have heq : (3 : ℝ) ^ oddCount w = (3 : ℝ) ^ o0 := le_antisymm hleA hA
  rw [heq] at hfin'
  exact not_le_of_gt hnum' hfin'

/-- Instantiate the floor-`257` comparison at a concrete length. -/
theorem finance_excludes_at_two_hundred_fifty_seven
    {n : ℕ} {w : List Branch} {L oPred : ℕ}
    (hn : 2 ≤ n) (hlen : w.length = L)
    (hL : (L : ℝ) < 15677 / 11)
    (hpred : 3 ^ oPred ≤ 2 ^ L)
    (hnum : (15677 / 11 : ℝ) * ((3 : ℝ) ^ (oPred + 1) - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ (oPred + 1)) :
    ¬CycleWord n w := by
  intro h
  have hpred' : 3 ^ oPred ≤ 2 ^ w.length := by simpa [hlen] using hpred
  have ho : oPred + 1 ≤ oddCount w :=
    Nat.succ_le_of_lt (cycle_oddCount_gt_of_three_pow_le hn h hpred')
  exact finance_contradicts_min_two_hundred_fifty_seven hn h hlen hL ho hnum

/-- Finance excludes length `19`: `2^19 < 3^12` and
`(15677/11)(3^{12} - 2^{19}) > 19 · 3^{12}`. -/
theorem finance_excludes_length_nineteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 19) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 11 ≤ 2 ^ 19) (by norm_num)

/-- Census extension: no cycle word of length at most `19`. -/
theorem no_cycle_word_length_le_nineteen {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length ≤ 19) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 19 with h19 | h19
  · exact no_cycle_word_length_le_eighteen hn (by omega) h
  · exact finance_excludes_length_nineteen hn (by omega) h

theorem finance_excludes_length_thirty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 30) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 18 ≤ 2 ^ 30) (by norm_num)

theorem finance_excludes_length_thirtyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 31) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 19 ≤ 2 ^ 31) (by norm_num)

theorem finance_excludes_length_thirtytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 32) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 20 ≤ 2 ^ 32) (by norm_num)

theorem finance_excludes_length_thirtythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 33) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 20 ≤ 2 ^ 33) (by norm_num)

theorem finance_excludes_length_thirtyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 34) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 21 ≤ 2 ^ 34) (by norm_num)

theorem finance_excludes_length_thirtyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 35) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 22 ≤ 2 ^ 35) (by norm_num)

theorem finance_excludes_length_thirtysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 36) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 22 ≤ 2 ^ 36) (by norm_num)

theorem finance_excludes_length_thirtyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 37) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 23 ≤ 2 ^ 37) (by norm_num)

/-- No cycle word of length below `38` except possibly `38`. -/
theorem no_cycle_word_length_lt_thirty_eight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hLt : w.length < 38) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 19 with h18 | h19
  · exact no_cycle_word_length_le_eighteen hn (Nat.le_of_lt_succ h18) h
  · rcases Nat.eq_or_lt_of_le h19 with _ | hlt19
    · exact finance_excludes_length_nineteen hn (by omega) h
    · have hge : 20 ≤ w.length := Nat.succ_le_of_lt hlt19
      rcases Nat.lt_or_ge w.length 30 with h29 | h30
      · exact no_cycle_word_length_lt_thirty_ne_nineteen hn h29
          (ne_of_gt (lt_of_lt_of_le (by decide : (19 : ℕ) < 20) hge)) h
      · have hsplit : w.length = 30 ∨ w.length = 31 ∨ w.length = 32 ∨
            w.length = 33 ∨ w.length = 34 ∨ w.length = 35 ∨
            w.length = 36 ∨ w.length = 37 := by
          omega
        rcases hsplit with hL | hL | hL | hL | hL | hL | hL | hL
        · exact finance_excludes_length_thirty hn hL h
        · exact finance_excludes_length_thirtyone hn hL h
        · exact finance_excludes_length_thirtytwo hn hL h
        · exact finance_excludes_length_thirtythree hn hL h
        · exact finance_excludes_length_thirtyfour hn hL h
        · exact finance_excludes_length_thirtyfive hn hL h
        · exact finance_excludes_length_thirtysix hn hL h
        · exact finance_excludes_length_thirtyseven hn hL h

/-- If a nontrivial cycle exists, its period is at least `30`. -/
theorem cycle_word_length_ge_thirty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) : 30 ≤ w.length := by
  rcases cycle_word_length_nineteen_or_ge_thirty hn h with h19 | h30
  · exact absurd h (finance_excludes_length_nineteen hn h19)
  · exact h30

/-- If a nontrivial cycle exists, its period is `38` or at least `39`.
Weaker leftover: `log 257 > 61/11` also kills `38`. -/
theorem cycle_word_length_thirty_eight_or_ge_thirty_nine
    {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 38 ∨ 39 ≤ w.length := by
  by_contra hc
  push Not at hc
  obtain ⟨h38, h39⟩ := hc
  exact no_cycle_word_length_lt_thirty_eight hn (by omega) h

/-- Finance excludes length `38`: `2^38 < 3^24` and
`(15677/11)(3^{24} - 2^{38}) > 38 · 3^{24}`. -/
theorem finance_excludes_length_thirtyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 38) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 23 ≤ 2 ^ 38) (by norm_num)

theorem finance_excludes_length_thirtynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 39) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 24 ≤ 2 ^ 39) (by norm_num)

theorem finance_excludes_length_forty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 40) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 25 ≤ 2 ^ 40) (by norm_num)

theorem finance_excludes_length_fortyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 41) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 25 ≤ 2 ^ 41) (by norm_num)

theorem finance_excludes_length_fortytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 42) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 26 ≤ 2 ^ 42) (by norm_num)

theorem finance_excludes_length_fortythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 43) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 27 ≤ 2 ^ 43) (by norm_num)

theorem finance_excludes_length_fortyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 44) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 27 ≤ 2 ^ 44) (by norm_num)

theorem finance_excludes_length_fortyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 45) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 28 ≤ 2 ^ 45) (by norm_num)

theorem finance_excludes_length_fortysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 46) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 29 ≤ 2 ^ 46) (by norm_num)

theorem finance_excludes_length_fortyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 47) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 29 ≤ 2 ^ 47) (by norm_num)

theorem finance_excludes_length_fortyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 48) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 30 ≤ 2 ^ 48) (by norm_num)

theorem finance_excludes_length_fortynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 49) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 30 ≤ 2 ^ 49) (by norm_num)

theorem finance_excludes_length_fifty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 50) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 31 ≤ 2 ^ 50) (by norm_num)

theorem finance_excludes_length_fiftyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 51) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 32 ≤ 2 ^ 51) (by norm_num)

theorem finance_excludes_length_fiftytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 52) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 32 ≤ 2 ^ 52) (by norm_num)

theorem finance_excludes_length_fiftythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 53) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 33 ≤ 2 ^ 53) (by norm_num)

theorem finance_excludes_length_fiftyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 54) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 34 ≤ 2 ^ 54) (by norm_num)

theorem finance_excludes_length_fiftyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 55) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 34 ≤ 2 ^ 55) (by norm_num)

theorem finance_excludes_length_fiftysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 56) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_fifty_seven hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 35 ≤ 2 ^ 56) (by norm_num)

/-- No cycle word of length below `57`. -/
theorem no_cycle_word_length_lt_fifty_seven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hLt : w.length < 57) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 38 with h37 | h38
  · exact no_cycle_word_length_lt_thirty_eight hn h37 h
  · have hsplit : w.length = 38 ∨ w.length = 39 ∨ w.length = 40 ∨
        w.length = 41 ∨ w.length = 42 ∨ w.length = 43 ∨
        w.length = 44 ∨ w.length = 45 ∨ w.length = 46 ∨
        w.length = 47 ∨ w.length = 48 ∨ w.length = 49 ∨
        w.length = 50 ∨ w.length = 51 ∨ w.length = 52 ∨
        w.length = 53 ∨ w.length = 54 ∨ w.length = 55 ∨
        w.length = 56 := by
      omega
    rcases hsplit with
      hL | hL | hL | hL | hL | hL | hL | hL | hL |
      hL | hL | hL | hL | hL | hL | hL | hL | hL | hL
    · exact finance_excludes_length_thirtyeight hn hL h
    · exact finance_excludes_length_thirtynine hn hL h
    · exact finance_excludes_length_forty hn hL h
    · exact finance_excludes_length_fortyone hn hL h
    · exact finance_excludes_length_fortytwo hn hL h
    · exact finance_excludes_length_fortythree hn hL h
    · exact finance_excludes_length_fortyfour hn hL h
    · exact finance_excludes_length_fortyfive hn hL h
    · exact finance_excludes_length_fortysix hn hL h
    · exact finance_excludes_length_fortyseven hn hL h
    · exact finance_excludes_length_fortyeight hn hL h
    · exact finance_excludes_length_fortynine hn hL h
    · exact finance_excludes_length_fifty hn hL h
    · exact finance_excludes_length_fiftyone hn hL h
    · exact finance_excludes_length_fiftytwo hn hL h
    · exact finance_excludes_length_fiftythree hn hL h
    · exact finance_excludes_length_fiftyfour hn hL h
    · exact finance_excludes_length_fiftyfive hn hL h
    · exact finance_excludes_length_fiftysix hn hL h

/-- If a nontrivial cycle exists, its period is `57` or at least `58`.
Weaker leftover: the floor `261` also kills `57` and `76`. -/
theorem cycle_word_length_fifty_seven_or_ge_fifty_eight
    {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 57 ∨ 58 ≤ w.length := by
  by_contra hc
  push Not at hc
  obtain ⟨h57, h58⟩ := hc
  exact no_cycle_word_length_lt_fifty_seven hn (by omega) h

/-- Finance at the rotated odd minimum after the residual floor `261`:
`(15921/11)(3^o - 2^L) ≤ L 3^o`, because the minimum is at least `261`
and `261 log 257 > 15921/11`. -/
theorem cycle_finance_min_two_hundred_sixty_one {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    (15921 / 11 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) ≤
      (w.length : ℝ) * (3 : ℝ) ^ oddCount w := by
  obtain ⟨k, hkL, hmin⟩ := exists_cycleMin hn h
  have hm261 : 261 ≤ floorPower^[k] n :=
    cycleWord_iterate_not_lt_two_hundred_sixty_one hn h
  have hm2 : 2 ≤ floorPower^[k] n := by omega
  have hfin := cycleMin_finance hm2 hmin
  rw [rotateWord_length, oddCount_rotateWord] at hfin
  have hexpand : (2 : ℝ) ^ w.length < (3 : ℝ) ^ oddCount w := by
    exact_mod_cast cycle_word_formally_expanding hn h
  have hm261R : (261 : ℝ) ≤ (floorPower^[k] n : ℝ) := by exact_mod_cast hm261
  have hlog : (61 / 11 : ℝ) ≤ Real.log (floorPower^[k] n) := by
    have hmono : Real.log (257 : ℝ) ≤ Real.log (floorPower^[k] n) := by
      have : (257 : ℝ) ≤ (floorPower^[k] n : ℝ) := by
        exact_mod_cast (le_trans (by decide : (257 : ℕ) ≤ 261) hm261)
      gcongr
    linarith [log_two_hundred_fifty_seven_gt]
  have hmlog : (15921 / 11 : ℝ) ≤
      (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) := by
    have h1 : (261 : ℝ) * (61 / 11) ≤
        (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) :=
      mul_le_mul hm261R hlog (by norm_num) (by linarith)
    linarith
  calc (15921 / 11 : ℝ) * ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length)
      ≤ (floorPower^[k] n : ℝ) * Real.log (floorPower^[k] n) *
          ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) :=
        mul_le_mul_of_nonneg_right hmlog (by linarith)
    _ ≤ (w.length : ℝ) * (3 : ℝ) ^ oddCount w := hfin

theorem finance_contradicts_min_two_hundred_sixty_one
    {n : ℕ} {w : List Branch} {L o0 : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w)
    (hlen : w.length = L) (hL : (L : ℝ) < 15921 / 11)
    (ho : o0 ≤ oddCount w)
    (hnum : (15921 / 11 : ℝ) * ((3 : ℝ) ^ o0 - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ o0) : False := by
  have hfin := cycle_finance_min_two_hundred_sixty_one hn h
  rw [hlen] at hfin
  have hA : (3 : ℝ) ^ o0 ≤ (3 : ℝ) ^ oddCount w := by
    have : (3 : ℕ) ^ o0 ≤ 3 ^ oddCount w :=
      Nat.pow_le_pow_right (by norm_num) ho
    exact_mod_cast this
  have hc : (0 : ℝ) < 15921 / 11 - L := sub_pos.mpr hL
  have hnum' : (15921 / 11 - (L : ℝ)) * (3 : ℝ) ^ o0 >
      (15921 / 11) * (2 : ℝ) ^ L := by nlinarith
  have hfin' : (15921 / 11 - (L : ℝ)) * (3 : ℝ) ^ oddCount w ≤
      (15921 / 11) * (2 : ℝ) ^ L := by nlinarith
  have hleA : (3 : ℝ) ^ oddCount w ≤ (3 : ℝ) ^ o0 :=
    le_of_mul_le_mul_left (le_trans hfin' hnum'.le) hc
  have heq : (3 : ℝ) ^ oddCount w = (3 : ℝ) ^ o0 := le_antisymm hleA hA
  rw [heq] at hfin'
  exact not_le_of_gt hnum' hfin'

theorem finance_excludes_at_two_hundred_sixty_one
    {n : ℕ} {w : List Branch} {L oPred : ℕ}
    (hn : 2 ≤ n) (hlen : w.length = L)
    (hL : (L : ℝ) < 15921 / 11)
    (hpred : 3 ^ oPred ≤ 2 ^ L)
    (hnum : (15921 / 11 : ℝ) * ((3 : ℝ) ^ (oPred + 1) - (2 : ℝ) ^ L) >
      (L : ℝ) * (3 : ℝ) ^ (oPred + 1)) :
    ¬CycleWord n w := by
  intro h
  have hpred' : 3 ^ oPred ≤ 2 ^ w.length := by simpa [hlen] using hpred
  have ho : oPred + 1 ≤ oddCount w :=
    Nat.succ_le_of_lt (cycle_oddCount_gt_of_three_pow_le hn h hpred')
  exact finance_contradicts_min_two_hundred_sixty_one hn h hlen hL ho hnum

theorem finance_excludes_length_fiftyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 57) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 35 ≤ 2 ^ 57) (by norm_num)

theorem finance_excludes_length_fiftyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 58) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 36 ≤ 2 ^ 58) (by norm_num)

theorem finance_excludes_length_fiftynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 59) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 37 ≤ 2 ^ 59) (by norm_num)

theorem finance_excludes_length_sixty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 60) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 37 ≤ 2 ^ 60) (by norm_num)

theorem finance_excludes_length_sixtyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 61) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 38 ≤ 2 ^ 61) (by norm_num)

theorem finance_excludes_length_sixtytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 62) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 39 ≤ 2 ^ 62) (by norm_num)

theorem finance_excludes_length_sixtythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 63) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 39 ≤ 2 ^ 63) (by norm_num)

theorem finance_excludes_length_sixtyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 64) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 40 ≤ 2 ^ 64) (by norm_num)

theorem finance_excludes_length_sixtyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 65) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 41 ≤ 2 ^ 65) (by norm_num)

theorem finance_excludes_length_sixtysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 66) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 41 ≤ 2 ^ 66) (by norm_num)

theorem finance_excludes_length_sixtyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 67) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 42 ≤ 2 ^ 67) (by norm_num)

theorem finance_excludes_length_sixtyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 68) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 42 ≤ 2 ^ 68) (by norm_num)

theorem finance_excludes_length_sixtynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 69) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 43 ≤ 2 ^ 69) (by norm_num)

theorem finance_excludes_length_seventy {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 70) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 44 ≤ 2 ^ 70) (by norm_num)

theorem finance_excludes_length_seventyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 71) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 44 ≤ 2 ^ 71) (by norm_num)

theorem finance_excludes_length_seventytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 72) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 45 ≤ 2 ^ 72) (by norm_num)

theorem finance_excludes_length_seventythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 73) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 46 ≤ 2 ^ 73) (by norm_num)

theorem finance_excludes_length_seventyfour {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 74) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 46 ≤ 2 ^ 74) (by norm_num)

theorem finance_excludes_length_seventyfive {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 75) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 47 ≤ 2 ^ 75) (by norm_num)

theorem finance_excludes_length_seventysix {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 76) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 47 ≤ 2 ^ 76) (by norm_num)

theorem finance_excludes_length_seventyseven {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 77) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 48 ≤ 2 ^ 77) (by norm_num)

theorem finance_excludes_length_seventyeight {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 78) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 49 ≤ 2 ^ 78) (by norm_num)

theorem finance_excludes_length_seventynine {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 79) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 49 ≤ 2 ^ 79) (by norm_num)

theorem finance_excludes_length_eighty {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 80) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 50 ≤ 2 ^ 80) (by norm_num)

theorem finance_excludes_length_eightyone {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 81) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 51 ≤ 2 ^ 81) (by norm_num)

theorem finance_excludes_length_eightytwo {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 82) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 51 ≤ 2 ^ 82) (by norm_num)

theorem finance_excludes_length_eightythree {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hlen : w.length = 83) : ¬CycleWord n w :=
  finance_excludes_at_two_hundred_sixty_one hn hlen (by norm_num)
    (by norm_num : (3 : ℕ) ^ 52 ≤ 2 ^ 83) (by norm_num)

/-- No cycle word of length below `84`. -/
theorem no_cycle_word_length_lt_eighty_four {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hLt : w.length < 84) : ¬CycleWord n w := by
  intro h
  rcases Nat.lt_or_ge w.length 57 with h56 | h57
  · exact no_cycle_word_length_lt_fifty_seven hn h56 h
  · have hsplit : w.length = 57 ∨ w.length = 58 ∨ w.length = 59 ∨
        w.length = 60 ∨ w.length = 61 ∨ w.length = 62 ∨
        w.length = 63 ∨ w.length = 64 ∨ w.length = 65 ∨
        w.length = 66 ∨ w.length = 67 ∨ w.length = 68 ∨
        w.length = 69 ∨ w.length = 70 ∨ w.length = 71 ∨
        w.length = 72 ∨ w.length = 73 ∨ w.length = 74 ∨
        w.length = 75 ∨ w.length = 76 ∨ w.length = 77 ∨
        w.length = 78 ∨ w.length = 79 ∨ w.length = 80 ∨
        w.length = 81 ∨ w.length = 82 ∨ w.length = 83 := by
      omega
    rcases hsplit with
      hL | hL | hL | hL | hL | hL | hL | hL | hL |
      hL | hL | hL | hL | hL | hL | hL | hL | hL |
      hL | hL | hL | hL | hL | hL | hL | hL | hL
    · exact finance_excludes_length_fiftyseven hn hL h
    · exact finance_excludes_length_fiftyeight hn hL h
    · exact finance_excludes_length_fiftynine hn hL h
    · exact finance_excludes_length_sixty hn hL h
    · exact finance_excludes_length_sixtyone hn hL h
    · exact finance_excludes_length_sixtytwo hn hL h
    · exact finance_excludes_length_sixtythree hn hL h
    · exact finance_excludes_length_sixtyfour hn hL h
    · exact finance_excludes_length_sixtyfive hn hL h
    · exact finance_excludes_length_sixtysix hn hL h
    · exact finance_excludes_length_sixtyseven hn hL h
    · exact finance_excludes_length_sixtyeight hn hL h
    · exact finance_excludes_length_sixtynine hn hL h
    · exact finance_excludes_length_seventy hn hL h
    · exact finance_excludes_length_seventyone hn hL h
    · exact finance_excludes_length_seventytwo hn hL h
    · exact finance_excludes_length_seventythree hn hL h
    · exact finance_excludes_length_seventyfour hn hL h
    · exact finance_excludes_length_seventyfive hn hL h
    · exact finance_excludes_length_seventysix hn hL h
    · exact finance_excludes_length_seventyseven hn hL h
    · exact finance_excludes_length_seventyeight hn hL h
    · exact finance_excludes_length_seventynine hn hL h
    · exact finance_excludes_length_eighty hn hL h
    · exact finance_excludes_length_eightyone hn hL h
    · exact finance_excludes_length_eightytwo hn hL h
    · exact finance_excludes_length_eightythree hn hL h

/-- If a nontrivial cycle exists, its period is `84` or at least `85`.
The cheap leftovers `57` and `76` die at the residual floor `261`;
`58`–`75` and `77`–`83` die by the same comparison. `L=84` is the
next record near-convergent. -/
theorem cycle_word_length_eighty_four_or_ge_eighty_five
    {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    w.length = 84 ∨ 85 ≤ w.length := by
  by_contra hc
  push Not at hc
  obtain ⟨h84, h85⟩ := hc
  exact no_cycle_word_length_lt_eighty_four hn (by omega) h

/-- Finance table cutoff used by the Eliahou leftover. -/
def eliahouTableCutoff : ℕ := 10 ^ 5

/-- Eliahou leftover: period `84`, a listed near-convergent, or at
least the finance table cutoff. -/
def EliahouLeftover (L : ℕ) (exceptions : List ℕ) : Prop :=
  L = 84 ∨ L ∈ exceptions ∨ eliahouTableCutoff ≤ L

/-- Every length in `[30, cutoff)` outside the named family is
already excluded. Instantiated by the computational gap table. -/
def EliahouTable (exceptions : List ℕ) : Prop :=
  ∀ (n : ℕ) (w : List Branch),
    2 ≤ n → 30 ≤ w.length → w.length < eliahouTableCutoff →
      w.length ∉ exceptions → ¬CycleWord n w

/-- Bookkeeping: the Lean leftover `84` or `≥ 85`, plus the finance
table, is the Eliahou leftover. Not a new inequality. -/
theorem cycle_word_eliahou_leftover {n : ℕ} {w : List Branch}
    {exceptions : List ℕ} (hn : 2 ≤ n) (h : CycleWord n w)
    (hTable : EliahouTable exceptions) :
    EliahouLeftover w.length exceptions := by
  rcases cycle_word_length_eighty_four_or_ge_eighty_five hn h with h84 | h85
  · exact Or.inl h84
  · rcases Nat.lt_or_ge w.length eliahouTableCutoff with hlt | hge
    · have hmem : w.length ∈ exceptions := by
        by_contra hne
        have h30 : 30 ≤ w.length :=
          le_trans (by decide : (30 : ℕ) ≤ 85) h85
        exact hTable n w hn h30 hlt hne h
      exact Or.inr (Or.inl hmem)
    · exact Or.inr (Or.inr hge)

end Problems.Juggler
