import Problems.Juggler.CycleFinance
import Mathlib.Algebra.BigOperators.Group.Finset.Basic

namespace Problems.Juggler

/-!
# Odd-run height law and leftover 84 with m ≥ 3

After `j` consecutive odd steps from a `CycleMin` valley the state
is at least the odd-run height `oddRunHeight n j`. Combined with
the inv-sum form of `cycleMin_finance` this excludes every length-84
cycle with at most two odd-runs at the residual floor 261.

Not a halt theorem. Paper A is unchanged.
-/

open Finset

/-- Drop a leading odd-run. -/
def dropOddRun : List Branch → List Branch
  | .odd :: w => dropOddRun w
  | w => w

theorem dropOddRun_length_le : ∀ w : List Branch, (dropOddRun w).length ≤ w.length
  | [] => le_rfl
  | .odd :: w =>
      le_trans (dropOddRun_length_le w) (Nat.le_succ _)
  | .even :: _ => le_rfl

/-- Trailing odd-run length of a prefix. -/
def trailingOdds (w : List Branch) : ℕ :=
  (w.reverse.takeWhile (fun b => decide (b = Branch.odd))).length

theorem trailingOdds_nil : trailingOdds [] = 0 := rfl

theorem trailingOdds_append_odd (w : List Branch) :
    trailingOdds (w ++ [Branch.odd]) = trailingOdds w + 1 := by
  simp [trailingOdds, List.reverse_append]

theorem trailingOdds_append_even (w : List Branch) :
    trailingOdds (w ++ [Branch.even]) = 0 := by
  simp [trailingOdds, List.reverse_append]

/-- Depth of the odd-run containing index `i` (0 if `w[i]` is even). -/
def oddRunDepth (w : List Branch) (i : ℕ) : ℕ :=
  if h : i < w.length then
    match w[i] with
    | .even => 0
    | .odd => trailingOdds (w.take i) + 1
  else 0

/-- Number of odd-runs: indices of odd-run starts (`oddRunDepth = 1`). -/
def cycleCircuitCount (w : List Branch) : ℕ :=
  (List.range w.length).filter (fun i => oddRunDepth w i = 1) |>.length

theorem dropOddRun_even_cons (w : List Branch) :
    dropOddRun (.even :: w) = .even :: w := rfl

theorem dropOddRun_nil : dropOddRun [] = [] := rfl

theorem cycleCircuitCount_nil : cycleCircuitCount [] = 0 := rfl

theorem cycleMin_iterate_ge_two {n : ℕ} {w : List Branch} {k : ℕ}
    (hn : 2 ≤ n) (h : CycleMin n w) (hk : k ≤ w.length) :
    2 ≤ floorPower^[k] n := by
  rcases lt_or_eq_of_le hk with hlt | rfl
  · exact cycleWord_iterate_ge_two hn h.1 hlt
  · rw [cycle_iterate_period h.1]
    exact hn

/-- Inv-sum envelope: each dyadic-cell defect is kept as `1/x_{i+1}`
instead of being replaced by `1/n`. At `k = L` this is
`(3^o - 2^L) log n ≤ 3^o ∑ 1/x_i`. -/
theorem cycleMin_log_envelope_inv {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∀ k, k ≤ w.length →
      (3 : ℝ) ^ oddCount (w.take k) * Real.log n ≤
        (2 : ℝ) ^ k * Real.log (floorPower^[k] n) +
          (3 : ℝ) ^ oddCount (w.take k) *
            ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
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
    have hsum : ∑ i ∈ range (k + 1), (1 : ℝ) / (floorPower^[i + 1] n) =
        (∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
          1 / (floorPower^[k + 1] n) :=
      sum_range_succ (fun i => (1 : ℝ) / (floorPower^[i + 1] n)) k
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
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) := ihk
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (3 : ℝ) ^ oddCount (List.take k w) /
                (floorPower^[k + 1] n : ℝ)) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (3 : ℝ) ^ oddCount (List.take k w) *
                ((∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
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
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n)) := ihk3
        _ = (2 : ℝ) ^ k * (3 * Real.log (floorPower^[k] n)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            ring
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              (2 : ℝ) ^ (k + 1) / (floorPower^[k + 1] n : ℝ)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) :=
            add_le_add_left hs2 _
        _ ≤ ((2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) /
                (floorPower^[k + 1] n : ℝ)) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n) := by
            gcongr
        _ = (2 : ℝ) ^ (k + 1) * Real.log (floorPower^[k + 1] n) +
              3 * (3 : ℝ) ^ oddCount (List.take k w) *
                ((∑ i ∈ range k, (1 : ℝ) / (floorPower^[i + 1] n)) +
                  1 / (floorPower^[k + 1] n)) := by
            ring

theorem cycleMin_finance_inv_sum {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ((3 : ℝ) ^ oddCount w - (2 : ℝ) ^ w.length) * Real.log n ≤
      (3 : ℝ) ^ oddCount w *
        ∑ i ∈ range w.length, (1 : ℝ) / (floorPower^[i + 1] n) := by
  have henv := cycleMin_log_envelope_inv hn h w.length le_rfl
  rw [List.take_length, cycle_iterate_period h.1] at henv
  linarith

theorem floorPower_two_hundred_sixty_one :
    floorPower 261 = 4216 := by
  native_decide

theorem floorPower_four_thousand_two_hundred_seventeen :
    floorPower 4217 = 273845 := by
  native_decide

theorem odd_two_hundred_sixty_one : (261 : ℕ) % 2 = 1 := by decide

theorem odd_four_thousand_two_hundred_seventeen : (4217 : ℕ) % 2 = 1 := by
  decide

/-- Least odd integer `≥ T(n)`. -/
def nextOddHeight (x : ℕ) : ℕ :=
  let t := floorPower x
  if t % 2 = 0 then t + 1 else t

/-- Odd-run height `τ_j`. `τ_0 = n`, `τ_{j+1}` is the least odd
integer `≥ T(τ_j)`. -/
def oddRunHeight (n : ℕ) : ℕ → ℕ
  | 0 => n
  | j + 1 => nextOddHeight (oddRunHeight n j)

theorem oddRunHeight_zero (n : ℕ) : oddRunHeight n 0 = n := rfl

theorem oddRunHeight_succ (n j : ℕ) :
    oddRunHeight n (j + 1) = nextOddHeight (oddRunHeight n j) :=
  rfl

theorem nextOddHeight_two_hundred_sixty_one :
    nextOddHeight 261 = 4217 := by
  simp [nextOddHeight, floorPower_two_hundred_sixty_one]

theorem oddRunHeight_one_two_hundred_sixty_one :
    oddRunHeight 261 1 = 4217 := by
  simp [oddRunHeight, nextOddHeight_two_hundred_sixty_one]

theorem oddRunHeight_two_two_hundred_sixty_one :
    oddRunHeight 261 2 = 273845 := by
  have h1 : oddRunHeight 261 1 = 4217 :=
    oddRunHeight_one_two_hundred_sixty_one
  unfold oddRunHeight nextOddHeight
  rw [h1, floorPower_four_thousand_two_hundred_seventeen]
  native_decide

theorem floorPower_odd_ge_of_ge_two_hundred_sixty_one
    {n : ℕ} (hn : 261 ≤ n) (ho : n % 2 = 1) :
    4216 ≤ floorPower n := by
  have hmono :=
    floorPower_odd_mono odd_two_hundred_sixty_one ho hn
  simpa [floorPower_two_hundred_sixty_one] using hmono

theorem floorPower_odd_ge_four_thousand_two_hundred_seventeen
    {x : ℕ} (hx : 4217 ≤ x) (ho : x % 2 = 1) :
    273845 ≤ floorPower x := by
  have hmono :=
    floorPower_odd_mono odd_four_thousand_two_hundred_seventeen ho hx
  simpa [floorPower_four_thousand_two_hundred_seventeen] using hmono

theorem cycleMin_start_odd_run {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) : 1 ≤ cycleCircuitCount w := by
  have h0 : 0 < w.length := h.1.2.2
  have hfirst : w[0] = Branch.odd := by
    cases hb : w[0] with
    | odd => rfl
    | even =>
        have he := follows_get_even w h.1.1 0 h0 hb
        have ho := cycleMin_start_odd hn h
        simp at he
        omega
  have hd : oddRunDepth w 0 = 1 := by
    unfold oddRunDepth
    simp [h0, hfirst, trailingOdds_nil]
  have hmem : 0 ∈ (List.range w.length).filter (fun i => oddRunDepth w i = 1) := by
    simp [List.mem_filter, hd, h0]
  exact List.length_pos_of_mem hmem

theorem cycleMin_end_even {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∃ u, w = u ++ [.even] := by
  induction w using List.reverseRecOn with
  | nil =>
      have := h.1.2.2
      simp at this
  | append_singleton u b =>
      cases b with
      | even => exact ⟨u, rfl⟩
      | odd => exact (cycleMin_not_end_odd hn h).elim

/-- After one odd letter from a `CycleMin` valley, the image is at
least `T(261) = 4216`. -/
theorem cycleMin_first_odd_image_ge {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 261 ≤ n) (h : CycleMin n w) (hi : i < w.length)
    (hd : oddRunDepth w i = 1) :
    4216 ≤ floorPower^[i + 1] n := by
  have hn2 : 2 ≤ n := le_trans (by decide : (2 : ℕ) ≤ 261) hn
  have hletter : w[i] = Branch.odd := by
    unfold oddRunDepth at hd
    rw [dif_pos hi] at hd
    cases hb : w[i] with
    | even => simp [hb] at hd
    | odd => rfl
  have hpar : (floorPower^[i] n) % 2 = 1 :=
    follows_get_odd w h.1.1 i hi hletter
  have hval : n ≤ floorPower^[i] n := cycleMin_iterate_ge h i (Nat.le_of_lt hi)
  have hiter : floorPower^[i + 1] n = floorPower (floorPower^[i] n) :=
    Function.iterate_succ_apply' floorPower i n
  have hT : 4216 ≤ floorPower (floorPower^[i] n) :=
    floorPower_odd_ge_of_ge_two_hundred_sixty_one
      (le_trans hn hval) hpar
  simpa [hiter] using hT

theorem oddRunDepth_even {w : List Branch} {i : ℕ}
    (hi : i < w.length) (he : w[i] = Branch.even) : oddRunDepth w i = 0 := by
  unfold oddRunDepth
  simp [hi, he]

theorem oddRunDepth_odd {w : List Branch} {i : ℕ}
    (hi : i < w.length) (ho : w[i] = Branch.odd) :
    oddRunDepth w i = trailingOdds (w.take i) + 1 := by
  unfold oddRunDepth
  simp [hi, ho]

theorem oddRunDepth_le_of_odd {w : List Branch} {i : ℕ}
    (hi : i < w.length) (ho : w[i] = Branch.odd) : 1 ≤ oddRunDepth w i := by
  rw [oddRunDepth_odd hi ho]
  omega

/-- After two or more consecutive odds from a `CycleMin` valley,
the image is at least `T(4217) = 273845`. The intermediate state is
odd (the next letter is odd). -/
theorem cycleMin_later_odd_image_ge {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 261 ≤ n) (h : CycleMin n w) (hi : i < w.length)
    (hd : 2 ≤ oddRunDepth w i) :
    273845 ≤ floorPower^[i + 1] n := by
  have hn2 : 2 ≤ n := le_trans (by decide : (2 : ℕ) ≤ 261) hn
  have hletter : w[i] = Branch.odd := by
    unfold oddRunDepth at hd
    rw [dif_pos hi] at hd
    cases hb : w[i] with
    | even => simp [hb] at hd
    | odd => rfl
  have hpar : (floorPower^[i] n) % 2 = 1 :=
    follows_get_odd w h.1.1 i hi hletter
  have hd' : oddRunDepth w i = trailingOdds (w.take i) + 1 :=
    oddRunDepth_odd hi hletter
  have htr : 1 ≤ trailingOdds (w.take i) := by omega
  have hi0 : 1 ≤ i := by
    have hne : w.take i ≠ [] := by
      intro he
      rw [he, trailingOdds_nil] at htr
      omega
    have hlen : (w.take i).length = i := by
      simp [List.length_take, Nat.min_eq_left (Nat.le_of_lt hi)]
    have : 0 < i := by
      rw [← hlen]
      exact List.length_pos_iff.mpr hne
    exact Nat.succ_le_of_lt this
  have hi1 : i - 1 < w.length := Nat.lt_of_le_of_lt (Nat.sub_le i 1) hi
  have htake : w.take i = w.take (i - 1) ++ [w[i - 1]] := by
    have h1 : w.take (i - 1 + 1) = w.take (i - 1) ++ [w[i - 1]] := by
      rw [List.take_add_one, List.getElem?_eq_getElem hi1]
      rfl
    simpa [Nat.sub_add_cancel hi0] using h1
  have hprev : w[i - 1] = Branch.odd := by
    cases hb : w[i - 1] with
    | even =>
        have : trailingOdds (w.take i) = 0 := by
          rw [htake, hb, trailingOdds_append_even]
        omega
    | odd => rfl
  have hpari : (floorPower^[i - 1] n) % 2 = 1 :=
    follows_get_odd w h.1.1 (i - 1) hi1 hprev
  have hval : n ≤ floorPower^[i - 1] n :=
    cycleMin_iterate_ge h (i - 1) (Nat.le_of_lt hi1)
  have hx : floorPower^[i] n = floorPower (floorPower^[i - 1] n) := by
    conv_lhs => rw [show i = (i - 1) + 1 from (Nat.sub_add_cancel hi0).symm]
    exact Function.iterate_succ_apply' floorPower (i - 1) n
  have hxi : 4217 ≤ floorPower^[i] n := by
    have hT0 : 4216 ≤ floorPower (floorPower^[i - 1] n) :=
      floorPower_odd_ge_of_ge_two_hundred_sixty_one (le_trans hn hval) hpari
    rw [hx]
    rcases Nat.mod_two_eq_zero_or_one (floorPower (floorPower^[i - 1] n)) with he | ho'
    · have : (floorPower^[i] n) % 2 = 0 := by simpa [hx] using he
      omega
    · omega
  have hiter : floorPower^[i + 1] n = floorPower (floorPower^[i] n) :=
    Function.iterate_succ_apply' floorPower i n
  have hT : 273845 ≤ floorPower (floorPower^[i] n) :=
    floorPower_odd_ge_four_thousand_two_hundred_seventeen hxi hpar
  simpa [hiter] using hT

/-- Inv-sum terms are classified by the producing letter. -/
theorem cycleMin_inv_term_le {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 261 ≤ n) (h : CycleMin n w) (hi : i < w.length) :
    (1 : ℝ) / (floorPower^[i + 1] n) ≤
      if w[i] = .even then
        if (floorPower^[i + 1] n) % 2 = 1 then (1 : ℝ) / n
        else (1 : ℝ) / (n * n)
      else if oddRunDepth w i = 1 then (1 : ℝ) / 4217
      else (1 : ℝ) / 273845 := by
  have hn2 : 2 ≤ n := le_trans (by decide : (2 : ℕ) ≤ 261) hn
  have hx : 2 ≤ floorPower^[i + 1] n :=
    cycleMin_iterate_ge_two hn2 h (Nat.succ_le_of_lt hi)
  have hx0 : (0 : ℝ) < (floorPower^[i + 1] n : ℝ) := by
    have : 0 < floorPower^[i + 1] n := by omega
    exact_mod_cast this
  have hn0 : (0 : ℝ) < n := by
    have : 0 < n := by omega
    exact_mod_cast this
  by_cases hev : w[i] = Branch.even
  · rw [if_pos hev]
    by_cases hodd : (floorPower^[i + 1] n) % 2 = 1
    · rw [if_pos hodd]
      have hge : n ≤ floorPower^[i + 1] n :=
        cycleMin_iterate_ge h (i + 1) (Nat.succ_le_of_lt hi)
      have hgeR : (n : ℝ) ≤ (floorPower^[i + 1] n : ℝ) := by exact_mod_cast hge
      simpa [one_div] using one_div_le_one_div_of_le hn0 hgeR
    · rw [if_neg hodd]
      have hsq : n ^ 2 ≤ floorPower^[i + 1] n := by
        have hi1 : i + 1 ≤ w.length := Nat.succ_le_of_lt hi
        have himg_even : (floorPower^[i + 1] n) % 2 = 0 := by omega
        rcases lt_or_eq_of_le hi1 with hlt | heq
        · exact cycleMin_even_ge_sq hn2 h hlt himg_even
        · have hper : floorPower^[i + 1] n = n := by
            rw [heq, cycle_iterate_period h.1]
          have : n % 2 = 0 := by simpa [hper] using himg_even
          have : n % 2 = 1 := cycleMin_start_odd hn2 h
          omega
      have hsqR : (n * n : ℝ) ≤ (floorPower^[i + 1] n : ℝ) := by
        have : (n ^ 2 : ℕ) ≤ floorPower^[i + 1] n := hsq
        exact_mod_cast (by simpa [pow_two] using this)
      simpa [one_div, mul_inv] using
        (one_div_le_one_div_of_le (by positivity : (0 : ℝ) < n * n) hsqR)
  · rw [if_neg hev]
    have hb : w[i] = Branch.odd := by
      cases hbr : w[i] with
      | even => exact (hev hbr).elim
      | odd => rfl
    by_cases h1 : oddRunDepth w i = 1
    · rw [if_pos h1]
      have hge : (4217 : ℕ) ≤ floorPower^[i + 1] n := by
        rcases Nat.mod_two_eq_zero_or_one (floorPower^[i + 1] n) with he | ho
        · have hsq : n ^ 2 ≤ floorPower^[i + 1] n := by
            have hi1 : i + 1 ≤ w.length := Nat.succ_le_of_lt hi
            rcases lt_or_eq_of_le hi1 with hlt | heq
            · exact cycleMin_even_ge_sq hn2 h hlt he
            · have hper : floorPower^[i + 1] n = n := by
                rw [heq, cycle_iterate_period h.1]
              have : n % 2 = 0 := by simpa [hper] using he
              have : n % 2 = 1 := cycleMin_start_odd hn2 h
              omega
          have h4217 : (4217 : ℕ) ≤ 261 ^ 2 := by decide
          have hsqn : 261 ^ 2 ≤ n ^ 2 := Nat.pow_le_pow_left hn 2
          exact le_trans h4217 (le_trans hsqn hsq)
        · have hT := cycleMin_first_odd_image_ge hn h hi (by omega)
          omega
      have hgeR : (4217 : ℝ) ≤ (floorPower^[i + 1] n : ℝ) := by
        exact_mod_cast hge
      simpa [one_div] using
        (one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 4217) hgeR)
    · rw [if_neg h1]
      have h2 : 2 ≤ oddRunDepth w i := by
        have := oddRunDepth_le_of_odd hi hb
        omega
      have hT := cycleMin_later_odd_image_ge hn h hi h2
      have hgeR : (273845 : ℝ) ≤ (floorPower^[i + 1] n : ℝ) := by
        exact_mod_cast hT
      simpa [one_div] using
        (one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 273845) hgeR)

end Problems.Juggler
