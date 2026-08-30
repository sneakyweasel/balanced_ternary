import Problems.Juggler.CycleCore
import Problems.Juggler.LengthEightCensus
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

Every cycle state is at least `12` (`cycleWord_iterate_not_lt_twelve`)
and the rotated minimum is odd (`cycleMin_start_odd`), so the
minimum is at least `13` and `n * log n ≥ 13 * log 13 > 65/2`.
This excludes cycle lengths wholesale: lengths `9`, `10`, `12`,
`13`, and `16` die here without any word census, and together with
`no_cycle_word_length_le_eight` the census extends to
`no_cycle_word_length_le_ten`.

Dossier: `docs/problems/juggler_cycle_finance.md`. This is not a
halt theorem and not a claim that every cycle length is excluded:
lengths `11`, `14`, `15` and the near-convergent lengths require a
larger verified floor than `12`.
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

end Problems.Juggler
