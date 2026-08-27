import Problems.Engine.ResidualPath

namespace Problems.Engine

/-!
# Fixed cycle words and lower-growth size bounds

`CycleWord n w` is a realized nonempty return `T_w(n) = n`. Cycle
return is not envelope equality: the defect stays positive. The
lower-growth theorem still gives `n^{3^o - 2^k} ≤ lowerDenom w`, hence
the crude bound `n ≤ lowerDenom w`. Contracting words, `O`, `OO`, and
`EOO` are excluded. This is not a halt theorem and not a claim that
every cycle word is impossible.
-/

def CycleWord (n : ℕ) (w : List Branch) : Prop :=
  follows n w ∧ image n w = n ∧ 1 ≤ w.length

theorem cycleWord_follows {n : ℕ} {w : List Branch} (h : CycleWord n w) :
    follows n w :=
  h.1

theorem cycleWord_image {n : ℕ} {w : List Branch} (h : CycleWord n w) :
    image n w = n :=
  h.2.1

theorem cycleWord_nonempty {n : ℕ} {w : List Branch} (h : CycleWord n w) :
    1 ≤ w.length :=
  h.2.2

theorem cycle_word_formally_expanding {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    2 ^ w.length < 3 ^ oddCount w :=
  cycle_strict_envelope hn h.1 h.2.1 h.2.2

theorem cycle_word_not_contracting {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    ¬3 ^ oddCount w < 2 ^ w.length :=
  cycle_not_contracting hn h.1 h.2.1

/-- Cycle return plus lower growth: `n^{3^o} ≤ D_w n^{2^k}`. -/
theorem cycle_lower_growth {n : ℕ} {w : List Branch}
    (hn : 1 ≤ n) (h : CycleWord n w) :
    n ^ (3 ^ oddCount w) ≤ lowerDenom w * n ^ (2 ^ w.length) := by
  have hL := lower_growth_word hn h.1
  have himg : image n w = n := h.2.1
  simpa [LowerPowerBound, himg] using hL

/-- The exact cycle size inequality. -/
theorem cycle_pow_le_lowerDenom {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    n ^ (3 ^ oddCount w - 2 ^ w.length) ≤ lowerDenom w := by
  have hexp := cycle_word_formally_expanding hn h
  have hle : 2 ^ w.length ≤ 3 ^ oddCount w := le_of_lt hexp
  have hL := cycle_lower_growth (le_trans (by decide : (1 : ℕ) ≤ 2) hn) h
  have hsplit :
      n ^ (3 ^ oddCount w) =
        n ^ (3 ^ oddCount w - 2 ^ w.length) * n ^ (2 ^ w.length) := by
    rw [← Nat.pow_add, Nat.sub_add_cancel hle]
  rw [hsplit] at hL
  have hpos : 0 < n ^ (2 ^ w.length) :=
    pow_pos (lt_of_lt_of_le (by decide : (0 : ℕ) < 1)
      (le_trans (by decide : (1 : ℕ) ≤ 2) hn)) _
  exact Nat.le_of_mul_le_mul_right hL hpos

/-- Crude explicit bound. Not optimized. -/
theorem cycle_le_lowerDenom {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    n ≤ lowerDenom w := by
  have hpow := cycle_pow_le_lowerDenom hn h
  have hexp := cycle_word_formally_expanding hn h
  have hge : 1 ≤ 3 ^ oddCount w - 2 ^ w.length :=
    Nat.succ_le_of_lt (Nat.sub_pos_of_lt hexp)
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 2) hn
  have hself : n ≤ n ^ (3 ^ oddCount w - 2 ^ w.length) :=
    le_trans (by simp : n ≤ n ^ 1) (Nat.pow_le_pow_right hn1 hge)
  exact le_trans hself hpow

theorem lowerDenom_odd : lowerDenom [.odd] = 4 := by native_decide

theorem lowerDenom_odd_odd : lowerDenom [.odd, .odd] = 1024 := by native_decide

theorem no_cycle_word_odd {n : ℕ} (hn : 2 ≤ n) : ¬CycleWord n [.odd] := by
  intro h
  have hle := cycle_le_lowerDenom hn h
  rw [lowerDenom_odd] at hle
  have hodd : n % 2 = 1 := h.1.1
  have himg : floorPower n = n := by simpa [image] using h.2.1
  have hn3 : n = 3 := by
    interval_cases n <;> omega
  subst hn3
  have : floorPower 3 = 5 := by native_decide
  exact (by decide : ¬(5 : ℕ) = 3) (this.symm.trans himg)

theorem cycle_oo_le_four {n : ℕ} (hn : 2 ≤ n)
    (h : CycleWord n [.odd, .odd]) : n ≤ 4 := by
  have hpow := cycle_pow_le_lowerDenom hn h
  have hlen : ([.odd, .odd] : List Branch).length = 2 := rfl
  have hodd : oddCount [.odd, .odd] = 2 := by simp
  have : n ^ 5 ≤ 1024 := by
    simpa [hlen, hodd, lowerDenom_odd_odd] using hpow
  refine Nat.lt_succ_iff.mp ?_
  have : ¬5 ≤ n := by
    intro hge
    have h5 : (5 : ℕ) ^ 5 ≤ n ^ 5 := Nat.pow_le_pow_left hge 5
    have : (3125 : ℕ) ≤ 1024 :=
      le_trans (by decide : (3125 : ℕ) ≤ 5 ^ 5) (le_trans h5 this)
    exact (by decide : ¬(3125 : ℕ) ≤ 1024) this
  omega

theorem no_cycle_word_oo {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n [.odd, .odd] := by
  intro h
  have hle := cycle_oo_le_four hn h
  have hodd : n % 2 = 1 := h.1.1
  have hn3 : n = 3 := by
    interval_cases n <;> omega
  subst hn3
  have himg : image 3 [.odd, .odd] = 3 := h.2.1
  have : image 3 [.odd, .odd] = 11 := by native_decide
  exact (by decide : ¬(11 : ℕ) = 3) (this.symm.trans himg)

theorem no_cycle_word_eoo {n : ℕ} (hn : 2 ≤ n) : ¬CycleWord n wordEOO := by
  intro h
  have hw := h.1
  have himg : floorPower^[3] n = n := by
    have : image n wordEOO = floorPower^[3] n := by
      simpa [length_wordEOO] using image_eq_iterate n wordEOO
    rw [← this, h.2.1]
  rcases eoo_sqrt_cases hw with h1 | h3 | h5
  · have hn2 : n = 2 := eoo_eq_two_of_sqrt_one hw h1
    subst hn2
    have : floorPower^[3] 2 = 1 := floorPower_eoo_two_eq
    exact (by decide : ¬(1 : ℕ) = 2) (this.symm.trans himg)
  · have hout : floorPower^[3] n = 11 :=
      floorPower_eoo_image_of_sqrt_three hw h3
    have hmem := eoo_of_sqrt_three hw h3
    rw [hout] at himg
    rcases hmem with hn10 | hn12 | hn14
    · subst hn10; exact (by decide : ¬(11 : ℕ) = 10) himg
    · subst hn12; exact (by decide : ¬(11 : ℕ) = 12) himg
    · subst hn14; exact (by decide : ¬(11 : ℕ) = 14) himg
  · exact (ne_of_gt (eoo_expands_of_sqrt_ge_five hw h5)) himg

theorem lowerDenom_wordOOE : lowerDenom wordOOE = 262144 := by native_decide

theorem cycle_ooe_le_lowerDenom {n : ℕ} (hn : 2 ≤ n)
    (h : CycleWord n wordOOE) : n ≤ 262144 := by
  have := cycle_le_lowerDenom hn h
  simpa [lowerDenom_wordOOE] using this

end Problems.Engine
