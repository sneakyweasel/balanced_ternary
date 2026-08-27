import Problems.Engine.ResidualPath

namespace Problems.Engine

/-!
# Fixed cycle words and lower-growth size bounds

`CycleWord n w` is a realized nonempty return `T_w(n) = n`. Cycle
return is not envelope equality: the defect stays positive. The
lower-growth theorem still gives `n^{3^o - 2^k} ≤ lowerDenom w`.

A last even letter is the square *cell* `n^2 ≤ z < (n+1)^2`, not an
exact-square identity. If a suffix `v` sits at or above the next
square, `vE` cannot be a cycle.

Existing next-square inventory, not a new engine:

* exact `OO` at `N = 5` (`oo_suffix_threshold`)
* exact `OOO` at `N = 3` (`ooo_suffix_threshold`)
* inherited `O^a` for `a ≥ 3` at `N = 3` (odd-append)
* eventual every superquadratic `v` at a huge `Q0(v)`
  (`eventually_no_first_even_contraction`)
* cell-specific `EOO` uses `(√n+1)^2`, not `(n+1)^2`

Every length-5 E-terminating word is either contracting or `OOOOE`.
This is not a halt theorem and not a claim that every cycle word is
impossible.
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

theorem cycle_iterate_period {n : ℕ} {w : List Branch} (h : CycleWord n w) :
    floorPower^[w.length] n = n := by
  simpa [image_eq_iterate] using h.2.1

theorem cycle_iterate_one_tail {n k : ℕ} (h : floorPower^[k] n = 1) :
    ∀ j, floorPower^[k + j] n = 1
  | 0 => by simpa using h
  | j + 1 => by
      rw [Nat.add_succ, Function.iterate_succ_apply']
      simpa [cycle_iterate_one_tail h j] using floorPower_one

theorem cycleWord_iterate_ge_two {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 2 ≤ n) (h : CycleWord n w) (hi : i < w.length) :
    2 ≤ floorPower^[i] n := by
  have hpos : 1 ≤ floorPower^[i] n :=
    floorPower_iterate_pos (le_trans (by decide : (1 : ℕ) ≤ 2) hn) i
  refine Nat.succ_le_of_lt (lt_of_le_of_ne hpos ?_)
  intro heq
  have htail := cycle_iterate_one_tail heq.symm (w.length - i)
  have hsum : i + (w.length - i) = w.length := Nat.add_sub_of_le (Nat.le_of_lt hi)
  have hone : floorPower^[w.length] n = 1 := by simpa [hsum] using htail
  have : n = 1 := (cycle_iterate_period h).symm.trans hone
  omega

/-- Even states strictly descend. Last-even cycle return is therefore
never a fixed point of `T`. -/
theorem floorPower_even_lt {n : ℕ} (hn : 2 ≤ n) (he : n % 2 = 0) :
    floorPower n < n := by
  have hsq : floorPower n ^ 2 ≤ n := floorPower_even_sq_le he
  refine Nat.lt_of_not_ge fun hge => ?_
  have : n ^ 2 ≤ n := le_trans (Nat.pow_le_pow_left hge 2) hsq
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : (0 : ℕ) < 2) hn
  have : n ≤ 1 :=
    Nat.le_of_mul_le_mul_right (by simpa [pow_two] using this) hn0
  omega

/-- Last even letter: the inverse cell, not an exact-square identity. -/
theorem cycle_last_even_interval {n : ℕ} {u : List Branch}
    (h : CycleWord n (u ++ [.even])) :
    n ^ 2 ≤ image n u ∧ image n u < (n + 1) ^ 2 := by
  have hf := follows_of_append_right (u := u) h.1
  have he : image n u % 2 = 0 := hf.1
  have hz : floorPower (image n u) = n := by
    have : image (image n u) [.even] = n := by
      simpa [image_append] using h.2.1
    simpa [image] using this
  exact (floorPower_even_eq_iff_sq_interval he).mp hz

theorem cycle_last_even_ne_odd_sq {n : ℕ} {u : List Branch}
    (hodd : n % 2 = 1) (h : CycleWord n (u ++ [.even])) :
    image n u ≠ n ^ 2 :=
  even_ne_odd_square (follows_of_append_right (u := u) h.1).1 hodd

theorem cycle_last_odd_interval {n : ℕ} {u : List Branch}
    (h : CycleWord n (u ++ [.odd])) :
    n ^ 2 ≤ image n u ^ 3 ∧ image n u ^ 3 < (n + 1) ^ 2 := by
  have hf := follows_of_append_right (u := u) h.1
  have ho : image n u % 2 = 1 := hf.1
  have hz : floorPower (image n u) = n := by
    have : image (image n u) [.odd] = n := by
      simpa [image_append] using h.2.1
    simpa [image] using this
  exact (floorPower_odd_eq_iff_cube_interval ho).mp hz

theorem cycleWord_rotate_cons {n : ℕ} {b : Branch} {w : List Branch}
    (h : CycleWord n (b :: w)) :
    CycleWord (floorPower n) (w ++ [b]) := by
  have hf0 : follows (floorPower n) w := by
    cases b <;> exact h.1.2
  have hb : follows n [b] := by
    cases b <;> exact ⟨h.1.1, trivial⟩
  have himg_w : image (floorPower n) w = n := by
    simpa [image] using h.2.1
  refine ⟨follows_append hf0 (by simpa [himg_w] using hb), ?_, by simp⟩
  rw [image_append, himg_w]
  cases b <;> simp [image]

theorem exists_iterate_min (n k : ℕ) (hk : 1 ≤ k) :
    ∃ i < k, ∀ j < k, floorPower^[i] n ≤ floorPower^[j] n := by
  induction k with
  | zero => omega
  | succ k ih =>
      match k with
      | 0 =>
          refine ⟨0, by omega, ?_⟩
          intro j hj
          have : j = 0 := by omega
          subst this
          exact le_rfl
      | k' + 1 =>
          have ⟨i, hi, hmin⟩ := ih (by omega : 1 ≤ k' + 1)
          cases le_or_gt (floorPower^[i] n) (floorPower^[k' + 1] n) with
          | inl hle =>
              refine ⟨i, Nat.lt_trans hi (by omega), ?_⟩
              intro j hj
              rcases Nat.lt_or_eq_of_le (Nat.lt_succ_iff.mp hj) with hlt | heq
              · exact hmin j hlt
              · simpa [heq] using hle
          | inr hgt =>
              refine ⟨k' + 1, by omega, ?_⟩
              intro j hj
              rcases Nat.lt_or_eq_of_le (Nat.lt_succ_iff.mp hj) with hjt | heq
              · exact (le_of_lt hgt).trans (hmin j hjt)
              · subst heq
                exact le_rfl

/-- The minimum state of a nontrivial cycle is odd, because an even
state strictly descends. -/
theorem exists_cycle_min_odd {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    ∃ i < w.length,
      (∀ j < w.length, floorPower^[i] n ≤ floorPower^[j] n) ∧
        floorPower^[i] n % 2 = 1 := by
  have ⟨i, hi, hmin⟩ := exists_iterate_min n w.length h.2.2
  refine ⟨i, hi, hmin, ?_⟩
  have hge := cycleWord_iterate_ge_two hn h hi
  rcases Nat.mod_two_eq_zero_or_one (floorPower^[i] n) with he | ho
  · exfalso
    have hlt : floorPower^[i + 1] n < floorPower^[i] n := by
      simpa [Function.iterate_succ_apply'] using floorPower_even_lt hge he
    cases lt_or_eq_of_le (Nat.succ_le_of_lt hi) with
    | inl hlen =>
        exact (not_le_of_gt hlt) (hmin (i + 1) hlen)
    | inr heq =>
        have hper := cycle_iterate_period h
        have hlt' : floorPower^[w.length] n < floorPower^[i] n := by
          convert hlt
          exact heq.symm
        rw [hper] at hlt'
        exact (not_le_of_gt hlt') (hmin 0 (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2))
  · exact ho

theorem no_cycle_word_ooe {n : ℕ} (hn : 2 ≤ n) : ¬CycleWord n wordOOE := by
  intro h
  have hw := follows_wordOOE_iff.mp h.1
  have hOO : follows n [.odd, .odd] := ⟨hw.1, hw.2.1, trivial⟩
  have hcell : CycleWord n ([.odd, .odd] ++ [.even]) := by
    simpa [wordOOE] using h
  have hI := cycle_last_even_interval hcell
  have hb : image n [.odd, .odd] = floorPower^[2] n :=
    image_eq_iterate n [.odd, .odd]
  rw [hb] at hI
  cases lt_or_ge n 5 with
  | inl hlt =>
      have hn3 : n = 3 := by
        have : n % 2 = 1 := hw.1
        omega
      subst hn3
      have himg : floorPower^[2] 3 = 11 := by
        simpa [eooCellOutput_eq_iterate hOO] using eoo_cell_output_three
      have he : floorPower^[2] 3 % 2 = 0 := by
        have := (follows_of_append_right (u := [.odd, .odd]) hcell.1).1
        simpa [hb] using this
      have : (11 : ℕ) % 2 = 1 := by decide
      omega
  | inr hge =>
      exact (not_le_of_gt hI.2) (oo_suffix_threshold hge hOO)

theorem no_cycle_word_oeo {n : ℕ} (hn : 2 ≤ n) : ¬CycleWord n wordOEO := by
  intro h
  have hw := follows_wordOEO_iff.mp h.1
  have hn3 : 3 ≤ n := by
    have : n % 2 = 1 := hw.1
    omega
  have ha : 2 ≤ floorPower n :=
    le_trans hn (le_of_lt (floorPower_odd_gt hn3 hw.1))
  have hrot : CycleWord (floorPower n) wordEOO := by
    have hcons : CycleWord n (.odd :: [.even, .odd]) := by
      simpa [wordOEO] using h
    simpa [wordEOO] using cycleWord_rotate_cons hcons
  exact no_cycle_word_eoo ha hrot

theorem cycle_last_even_cell {n : ℕ} {v : List Branch}
    (h : CycleWord n (v ++ [.even])) :
    n ^ 2 ≤ image n v ∧ image n v < (n + 1) ^ 2 :=
  cycle_last_even_interval h

theorem cycle_last_even_cell_odd {n : ℕ} {v : List Branch}
    (hodd : n % 2 = 1) (h : CycleWord n (v ++ [.even])) :
    n ^ 2 < image n v ∧ image n v < (n + 1) ^ 2 :=
  ⟨lt_of_le_of_ne (cycle_last_even_interval h).1
      (cycle_last_even_ne_odd_sq hodd h).symm,
    (cycle_last_even_interval h).2⟩

/-- If a suffix sits at or above the next square, it cannot be the
pre-final state of an E-terminating cycle. -/
theorem no_cycle_append_even_of_suffix_threshold {v : List Branch} {N : ℕ}
    (hth : ∀ m, N ≤ m → follows m v → (m + 1) ^ 2 ≤ image m v)
    {n : ℕ} (hn : N ≤ n) (h : CycleWord n (v ++ [.even])) : False :=
  (not_le_of_gt (cycle_last_even_interval h).2)
    (hth n hn (follows_of_append_left h.1))

def wordOOOE : List Branch := [.odd, .odd, .odd, .even]

theorem wordOOOE_eq_append :
    wordOOOE = [.odd, .odd, .odd] ++ [.even] :=
  rfl

theorem no_cycle_word_oooe {n : ℕ} (hn : 2 ≤ n) : ¬CycleWord n wordOOOE := by
  intro h
  have hcell : CycleWord n ([.odd, .odd, .odd] ++ [.even]) := by
    simpa [wordOOOE] using h
  have hw := follows_of_append_left hcell.1
  have hn3 : 3 ≤ n := by
    have : n % 2 = 1 := hw.1
    omega
  refine no_cycle_append_even_of_suffix_threshold (N := 3) ?_ hn3 hcell
  intro m hm hf
  simpa [image_eq_iterate] using ooo_suffix_threshold hm hf

theorem oddCount_le_length : ∀ w : List Branch, oddCount w ≤ w.length
  | [] => by simp
  | .odd :: w => Nat.succ_le_succ (oddCount_le_length w)
  | .even :: w => le_trans (oddCount_le_length w) (Nat.le_succ _)

theorem eq_replicate_odd_of_oddCount_eq_length {v : List Branch}
    (h : oddCount v = v.length) : v = List.replicate v.length Branch.odd := by
  induction v with
  | nil => simp
  | cons b rest ih =>
      cases b with
      | odd =>
          have hrest : oddCount rest = rest.length := by
            have : oddCount rest + 1 = rest.length + 1 := by
              simpa [oddCount, List.length_cons] using h
            omega
          have hk : (Branch.odd :: rest).length = rest.length + 1 := rfl
          rw [hk, List.replicate_succ]
          exact congrArg (List.cons Branch.odd) (ih hrest)
      | even =>
          have : oddCount rest ≤ rest.length := oddCount_le_length rest
          have : oddCount rest + 0 = rest.length + 1 := by
            simpa [oddCount, List.length_cons] using h
          omega

/-- Every length-4 E-terminating cycle word is impossible: it is either
formally contracting, or it is `OOOE` and hits the `OOO` threshold. -/
theorem no_cycle_word_length_four_ends_even {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (hv : v.length = 3)
    (h : CycleWord n (v ++ [Branch.even])) : False := by
  have hexp := cycle_word_formally_expanding hn h
  have hlen : (v ++ [Branch.even]).length = 4 := by simp [hv]
  have ho : oddCount (v ++ [Branch.even]) = oddCount v := by
    simp [oddCount_append]
  rw [hlen, ho] at hexp
  have hge : 3 ≤ oddCount v := by
    refine Nat.succ_le_of_lt (lt_of_not_ge fun hle => ?_)
    have hpow : 3 ^ oddCount v ≤ 9 := by
      interval_cases oddCount v <;> decide
    exact (not_le_of_gt hexp) (le_trans hpow (by decide : (9 : ℕ) ≤ 16))
  have hle : oddCount v ≤ 3 := by
    simpa [hv] using oddCount_le_length v
  have hodd : oddCount v = 3 := le_antisymm hle hge
  have hvOOO : v = [.odd, .odd, .odd] := by
    have := eq_replicate_odd_of_oddCount_eq_length (hodd.trans hv.symm)
    simpa [hv] using this
  have hOOOE : CycleWord n wordOOOE := by
    simpa [wordOOOE, hvOOO] using h
  exact no_cycle_word_oooe hn hOOOE

theorem threshold_inherits_odd_append {v : List Branch} {N : ℕ}
    (hth : ∀ m, N ≤ m → follows m v → (m + 1) ^ 2 ≤ image m v)
    {n : ℕ} (hn : N ≤ n) (hw : follows n (v ++ [Branch.odd])) :
    (n + 1) ^ 2 ≤ image n (v ++ [Branch.odd]) := by
  have hv := follows_of_append_left hw
  have hodd : image n v % 2 = 1 := (follows_of_append_right hw).1
  have hge := hth n hn hv
  have himg : image n (v ++ [Branch.odd]) = floorPower (image n v) := by
    rw [image_append]
    simp [image]
  exact le_trans hge (by simpa [himg] using floorPower_odd_ge hodd)

theorem replicate_odd_concat (a : ℕ) :
    List.replicate a Branch.odd ++ [Branch.odd] =
      List.replicate (a + 1) Branch.odd := by
  induction a with
  | zero => simp
  | succ a ih =>
      rw [List.replicate_succ, List.cons_append, ih]
      rfl

theorem follows_replicate_odd_head {n a : ℕ} (ha : 1 ≤ a)
    (hw : follows n (List.replicate a Branch.odd)) : n % 2 = 1 := by
  cases a with
  | zero => omega
  | succ a =>
      simpa [List.replicate_succ] using hw.1

theorem odd_run_suffix_threshold_add :
    ∀ k m, 3 ≤ m → follows m (List.replicate (3 + k) Branch.odd) →
      (m + 1) ^ 2 ≤ image m (List.replicate (3 + k) Branch.odd)
  | 0, m, hm, hf => by
      simpa [image_eq_iterate] using ooo_suffix_threshold hm hf
  | k + 1, m, hm, hf => by
      have hrep :
          List.replicate (3 + (k + 1)) Branch.odd =
            List.replicate (3 + k) Branch.odd ++ [Branch.odd] := by
        have : 3 + (k + 1) = (3 + k) + 1 := Nat.add_assoc 3 k 1
        rw [this, replicate_odd_concat]
      have hf' :
          follows m (List.replicate (3 + k) Branch.odd ++ [Branch.odd]) := by
        simpa [hrep] using hf
      have hle :=
        threshold_inherits_odd_append (N := 3)
          (odd_run_suffix_threshold_add k) hm hf'
      simpa [hrep] using hle

theorem odd_run_suffix_threshold {a : ℕ} (ha : 3 ≤ a) :
    ∀ m, 3 ≤ m → follows m (List.replicate a Branch.odd) →
      (m + 1) ^ 2 ≤ image m (List.replicate a Branch.odd) := by
  have hlen : a = 3 + (a - 3) := (Nat.add_sub_of_le ha).symm
  rw [hlen]
  exact odd_run_suffix_threshold_add (a - 3)

theorem no_cycle_odd_run_append_even {a : ℕ} (ha : 3 ≤ a)
    {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n (List.replicate a Branch.odd ++ [Branch.even]) := by
  intro h
  have hw := follows_of_append_left h.1
  have hodd :=
    follows_replicate_odd_head (le_trans (by decide : (1 : ℕ) ≤ 3) ha) hw
  have hn3 : 3 ≤ n := by omega
  exact no_cycle_append_even_of_suffix_threshold
    (odd_run_suffix_threshold ha) hn3 h

/-- Coarse coverage: every expanding `vE` is excluded above a huge `Q0`. -/
theorem eventually_no_cycle_append_even {v : List Branch}
    (hα : 2 ^ (v.length + 1) < 3 ^ oddCount v) :
    ∃ Q0, ∀ n, Q0 ≤ n → ¬CycleWord n (v ++ [Branch.even]) := by
  rcases eventually_no_first_even_contraction hα with ⟨Q0, hth⟩
  exact ⟨Q0, fun n hn h => no_cycle_append_even_of_suffix_threshold hth hn h⟩

/-- Every length-5 E-terminating cycle word is impossible: it is either
formally contracting, or it is `OOOOE` and inherits the `OOO` threshold. -/
theorem no_cycle_word_length_five_ends_even {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (hv : v.length = 4)
    (h : CycleWord n (v ++ [Branch.even])) : False := by
  have hexp := cycle_word_formally_expanding hn h
  have hlen : (v ++ [Branch.even]).length = 5 := by simp [hv]
  have ho : oddCount (v ++ [Branch.even]) = oddCount v := by
    simp [oddCount_append]
  rw [hlen, ho] at hexp
  have hge : 4 ≤ oddCount v := by
    refine Nat.succ_le_of_lt (lt_of_not_ge fun hle => ?_)
    have hpow : 3 ^ oddCount v ≤ 27 := by
      interval_cases oddCount v <;> decide
    exact (not_le_of_gt hexp) (le_trans hpow (by decide : (27 : ℕ) ≤ 32))
  have hle : oddCount v ≤ 4 := by
    simpa [hv] using oddCount_le_length v
  have hodd : oddCount v = 4 := le_antisymm hle hge
  have hvO : v = List.replicate 4 Branch.odd := by
    have := eq_replicate_odd_of_oddCount_eq_length (hodd.trans hv.symm)
    simpa [hv] using this
  have hC : CycleWord n (List.replicate 4 Branch.odd ++ [Branch.even]) := by
    simpa [hvO] using h
  exact no_cycle_odd_run_append_even (by decide : (3 : ℕ) ≤ 4) hn hC

end Problems.Engine
