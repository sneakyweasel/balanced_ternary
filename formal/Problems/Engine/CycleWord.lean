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
A cycle minimum forbids an `OE` start: the first even residual is
below `n^2`. An internal `E` plus a next-square suffix then
contradicts the last-even cell.

The extrema of any nontrivial cycle are word-independent: the
minimum is odd, the maximum is even, and `M > m^2`. A realized path
from `m` to any even cycle state is therefore superquadratic. This is
not a halt theorem and not a claim that every cycle word is impossible.
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

/-- The start is a minimum of its realized cycle. Cycle-internal. -/
def CycleMin (n : ℕ) (w : List Branch) : Prop :=
  CycleWord n w ∧ ∀ j, j < w.length → n ≤ floorPower^[j] n

theorem cycleMin_cycleWord {n : ℕ} {w : List Branch} (h : CycleMin n w) :
    CycleWord n w :=
  h.1

theorem cycleMin_ge {n : ℕ} {w : List Branch} {j : ℕ}
    (h : CycleMin n w) (hj : j < w.length) : n ≤ floorPower^[j] n :=
  h.2 j hj

theorem cycle_iterate_mul_length {n : ℕ} {w : List Branch}
    (h : CycleWord n w) : ∀ q, floorPower^[q * w.length] n = n
  | 0 => by simp
  | q + 1 => by
      have hmul : (q + 1) * w.length = q * w.length + w.length :=
        Nat.succ_mul q w.length
      rw [hmul, Function.iterate_add_apply, cycle_iterate_period h,
        cycle_iterate_mul_length h q]

theorem cycle_iterate_mod {n : ℕ} {w : List Branch} {k : ℕ}
    (h : CycleWord n w) : floorPower^[k] n = floorPower^[k % w.length] n := by
  have hsum : k = k % w.length + k / w.length * w.length := by
    have hdiv := Nat.div_add_mod k w.length
    rw [Nat.mul_comm, Nat.add_comm] at hdiv
    exact hdiv.symm
  conv => lhs; rw [hsum]
  rw [Function.iterate_add_apply, cycle_iterate_mul_length h]

theorem cycleMin_succ_ge {n : ℕ} {w : List Branch} {i : ℕ}
    (h : CycleMin n w) (hi : i < w.length) :
    n ≤ floorPower (floorPower^[i] n) := by
  have hnext : floorPower (floorPower^[i] n) = floorPower^[i + 1] n :=
    (Function.iterate_succ_apply' floorPower i n).symm
  rw [hnext]
  cases lt_or_eq_of_le (Nat.succ_le_of_lt hi) with
  | inl hlt =>
      exact cycleMin_ge h hlt
  | inr heq =>
      rw [← Nat.succ_eq_add_one, heq, cycle_iterate_period h.1]

/-- Even cycle states sit at or above `n^2`. Parity on the realized cycle. -/
theorem cycleMin_even_ge_sq {n : ℕ} {w : List Branch} {i : ℕ}
    (_hn : 2 ≤ n) (h : CycleMin n w) (hi : i < w.length)
    (he : floorPower^[i] n % 2 = 0) :
    n ^ 2 ≤ floorPower^[i] n := by
  have hy := cycleMin_succ_ge h hi
  have hz : floorPower (floorPower^[i] n) = (floorPower^[i] n).sqrt :=
    floorPower_even_eq he
  rw [hz] at hy
  exact (by simpa [pow_two] using Nat.le_sqrt.mp hy)

theorem floorPower_odd_lt_sq {n : ℕ} (hn : 2 ≤ n) (hodd : n % 2 = 1) :
    floorPower n < n ^ 2 := by
  rw [floorPower_odd_eq hodd]
  refine Nat.sqrt_lt.mpr ?_
  have hn1 : 1 < n := lt_of_lt_of_le (by decide : (1 : ℕ) < 2) hn
  have hpow : n ^ 3 < n ^ 4 :=
    Nat.pow_lt_pow_right hn1 (by decide : (3 : ℕ) < 4)
  have h4 : n ^ 4 = n ^ 2 * n ^ 2 := Nat.pow_add n 2 2
  simpa [h4] using hpow

theorem cycleMin_start_odd {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) : n % 2 = 1 := by
  rcases Nat.mod_two_eq_zero_or_one n with he | ho
  · exfalso
    have hlt : floorPower n < n := floorPower_even_lt hn he
    cases Nat.eq_or_lt_of_le h.1.2.2 with
    | inl h1 =>
        have hper := cycle_iterate_period h.1
        have hlen1 : w.length = 1 := by omega
        rw [hlen1] at hper
        change floorPower n = n at hper
        omega
    | inr hgt =>
        have hge : n ≤ floorPower^[1] n := cycleMin_ge h hgt
        exact (not_le_of_gt hlt) hge
  · exact ho

theorem cycleMin_not_start_even {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (.even :: v)) : False := by
  have he : n % 2 = 0 := h.1.1.1
  have ho := cycleMin_start_odd hn h
  omega

/-- A cycle minimum cannot start `OE`: the first even residual is `< n^2`. -/
theorem cycleMin_not_odd_even {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (.odd :: .even :: v)) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  have he : floorPower n % 2 = 0 := h.1.1.2.1
  have hlt := floorPower_odd_lt_sq hn hodd
  have hlen : (1 : ℕ) < (.odd :: .even :: v).length := by simp
  have hsq := cycleMin_even_ge_sq hn h hlen (by simpa using he)
  have : floorPower^[1] n = floorPower n := by simp
  rw [this] at hsq
  exact (not_le_of_gt hlt) hsq

def rotateWord : List Branch → ℕ → List Branch
  | w, 0 => w
  | [], _k + 1 => []
  | b :: rest, k + 1 => rotateWord (rest ++ [b]) k

theorem rotateWord_length : ∀ w k, (rotateWord w k).length = w.length
  | w, 0 => rfl
  | [], _k + 1 => rfl
  | b :: rest, k + 1 => by
      have := rotateWord_length (rest ++ [b]) k
      simpa [rotateWord, List.length_append] using this

theorem cycleWord_rotateWord {n : ℕ} {w : List Branch}
    (h : CycleWord n w) : ∀ k, CycleWord (floorPower^[k] n) (rotateWord w k)
  | 0 => by simpa [rotateWord] using h
  | k + 1 => by
      match w with
      | [] =>
          exact (Nat.not_succ_le_zero 0 h.2.2).elim
      | b :: rest =>
          have hrot := cycleWord_rotate_cons (by simpa using h)
          have ih := cycleWord_rotateWord hrot k
          have : floorPower^[k + 1] n = floorPower^[k] (floorPower n) :=
            Function.iterate_succ_apply floorPower k n
          simpa [rotateWord, this] using ih

theorem exists_cycleMin {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    ∃ k < w.length, CycleMin (floorPower^[k] n) (rotateWord w k) := by
  have ⟨i, hi, hle, _hodd⟩ := exists_cycle_min_odd hn h
  refine ⟨i, hi, cycleWord_rotateWord h i, ?_⟩
  intro j hj
  have hlen : (rotateWord w i).length = w.length := rotateWord_length w i
  rw [hlen] at hj
  have himg : floorPower^[j] (floorPower^[i] n) = floorPower^[i + j] n := by
    simpa [Nat.add_comm] using
      (Function.iterate_add_apply floorPower j i n).symm
  rw [himg, cycle_iterate_mod (k := i + j) h]
  exact hle _ (Nat.mod_lt _ (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2))

/-- Internal `E` plus a next-square suffix contradicts the last-even cell
on a cycle minimum. `y ≥ n` is enough; `y > n` is not required. -/
theorem no_cycleMin_internal_even_threshold {u v : List Branch} {N : ℕ}
    (hth : ∀ m, N ≤ m → follows m v → (m + 1) ^ 2 ≤ image m v)
    {n : ℕ} (hn : N ≤ n)
    (h : CycleMin n (u ++ [.even] ++ v ++ [.even])) : False := by
  have hw : CycleWord n (u ++ [.even] ++ v ++ [.even]) := h.1
  have hcell : CycleWord n ((u ++ [.even] ++ v) ++ [.even]) := by
    simpa [List.append_assoc] using hw
  have hI := cycle_last_even_interval hcell
  have himg_y := image_eq_iterate n (u ++ [.even])
  have hlen :
      (u ++ [Branch.even]).length <
        (u ++ [Branch.even] ++ v ++ [Branch.even]).length := by
    simp [List.length_append]
  have hy_ge : n ≤ image n (u ++ [.even]) := by
    simpa [himg_y] using cycleMin_ge h hlen
  have hf_tail : follows (image n (u ++ [.even])) (v ++ [.even]) :=
    follows_of_append_right (u := u ++ [.even])
      (by simpa [List.append_assoc] using hw.1)
  have hf_v : follows (image n (u ++ [.even])) v :=
    follows_of_append_left (v := [.even]) hf_tail
  have hth' := hth _ (le_trans hn hy_ge) hf_v
  have himg : image n (u ++ [.even] ++ v) = image (image n (u ++ [.even])) v :=
    image_append n (u ++ [.even]) v
  rw [himg] at hI
  have hy2 : (n + 1) ^ 2 ≤ image (image n (u ++ [.even])) v :=
    le_trans (Nat.pow_le_pow_left (Nat.succ_le_succ hy_ge) 2) hth'
  exact (not_le_of_gt hI.2) hy2

def wordOOEOOE : List Branch :=
  [.odd, .odd, .even, .odd, .odd, .even]

def wordOEOOOE : List Branch :=
  [.odd, .even, .odd, .odd, .odd, .even]

theorem wordOOEOOE_split :
    wordOOEOOE = [.odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even] :=
  rfl

theorem wordOEOOOE_is_odd_even :
    wordOEOOOE = .odd :: .even :: [.odd, .odd, .odd, .even] :=
  rfl

theorem no_cycleMin_ooeooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOOEOOE) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  have hn5 : 5 ≤ n := by
    cases lt_or_ge n 5 with
    | inl hlt =>
        have hn3 : n = 3 := by omega
        subst hn3
        have hOOE : follows 3 ([.odd, .odd] ++ [.even]) :=
          follows_of_append_left (by simpa [wordOOEOOE] using h.1.1)
        have he : image 3 [.odd, .odd] % 2 = 0 :=
          (follows_of_append_right (u := [.odd, .odd]) hOOE).1
        have himg : image 3 [.odd, .odd] = 11 := by native_decide
        rw [himg] at he
        exact absurd he (by decide : ¬(11 : ℕ) % 2 = 0)
    | inr hge => exact hge
  have hsplit : CycleMin n ([.odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even]) := by
    simpa [wordOOEOOE] using h
  refine no_cycleMin_internal_even_threshold (N := 5) ?_ hn5 hsplit
  intro m hm hf
  simpa [image_eq_iterate] using oo_suffix_threshold hm hf

theorem no_cycleMin_oeoooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOEOOOE) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  have hn3 : 3 ≤ n := by omega
  have hsplit : CycleMin n ([.odd] ++ [.even] ++ [.odd, .odd, .odd] ++ [.even]) := by
    simpa [wordOEOOOE] using h
  refine no_cycleMin_internal_even_threshold (N := 3) ?_ hn3 hsplit
  intro m hm hf
  simpa [image_eq_iterate] using ooo_suffix_threshold hm hf

theorem rotate_ooeooe :
    ∀ k, k < 6 →
      rotateWord wordOOEOOE k = wordOOEOOE ∨
        rotateWord wordOOEOOE k = [.odd, .even, .odd, .odd, .even, .odd] ∨
          rotateWord wordOOEOOE k = [.even, .odd, .odd, .even, .odd, .odd] := by
  intro k hk
  interval_cases k <;> simp [wordOOEOOE, rotateWord]

theorem no_cycle_word_ooeooe {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n wordOOEOOE := by
  intro h
  have ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen : wordOOEOOE.length = 6 := rfl
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by omega)
  rcases rotate_ooeooe k hk with h0 | h1 | h2
  · exact no_cycleMin_ooeooe hnk (by simpa [h0] using hm)
  · exact cycleMin_not_odd_even hnk (by simpa [h1] using hm)
  · exact cycleMin_not_start_even hnk (by simpa [h2] using hm)

/-- Dual of `CycleMin`: the start is a maximum of its realized cycle. -/
def CycleMax (n : ℕ) (w : List Branch) : Prop :=
  CycleWord n w ∧ ∀ j, j < w.length → floorPower^[j] n ≤ n

theorem cycleMax_cycleWord {n : ℕ} {w : List Branch} (h : CycleMax n w) :
    CycleWord n w :=
  h.1

theorem cycleMax_le {n : ℕ} {w : List Branch} {j : ℕ}
    (h : CycleMax n w) (hj : j < w.length) : floorPower^[j] n ≤ n :=
  h.2 j hj

theorem exists_iterate_max (n k : ℕ) (hk : 1 ≤ k) :
    ∃ i < k, ∀ j < k, floorPower^[j] n ≤ floorPower^[i] n := by
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
          have ⟨i, hi, hmax⟩ := ih (by omega : 1 ≤ k' + 1)
          cases le_or_gt (floorPower^[k' + 1] n) (floorPower^[i] n) with
          | inl hle =>
              refine ⟨i, Nat.lt_trans hi (by omega), ?_⟩
              intro j hj
              rcases Nat.lt_or_eq_of_le (Nat.lt_succ_iff.mp hj) with hlt | heq
              · exact hmax j hlt
              · simpa [heq] using hle
          | inr hgt =>
              refine ⟨k' + 1, by omega, ?_⟩
              intro j hj
              rcases Nat.lt_or_eq_of_le (Nat.lt_succ_iff.mp hj) with hjt | heq
              · exact (hmax j hjt).trans (le_of_lt hgt)
              · subst heq
                exact le_rfl

/-- The maximum state of a nontrivial cycle is even, because an odd
state strictly ascends. -/
theorem exists_cycle_max_even {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    ∃ i < w.length,
      (∀ j < w.length, floorPower^[j] n ≤ floorPower^[i] n) ∧
        floorPower^[i] n % 2 = 0 := by
  have ⟨i, hi, hmax⟩ := exists_iterate_max n w.length h.2.2
  refine ⟨i, hi, hmax, ?_⟩
  have hge := cycleWord_iterate_ge_two hn h hi
  rcases Nat.mod_two_eq_zero_or_one (floorPower^[i] n) with he | ho
  · exact he
  · exfalso
    have hn3 : 3 ≤ floorPower^[i] n := by omega
    have hlt : floorPower^[i] n < floorPower^[i + 1] n := by
      simpa [Function.iterate_succ_apply'] using floorPower_odd_gt hn3 ho
    cases lt_or_eq_of_le (Nat.succ_le_of_lt hi) with
    | inl hlen =>
        exact (not_le_of_gt hlt) (hmax (i + 1) hlen)
    | inr heq =>
        have hper := cycle_iterate_period h
        have hlt' : floorPower^[i] n < floorPower^[w.length] n := by
          convert hlt
          exact heq.symm
        rw [hper] at hlt'
        exact (not_le_of_gt hlt') (hmax 0 (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2))

theorem cycleMax_start_even {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMax n w) : n % 2 = 0 := by
  rcases Nat.mod_two_eq_zero_or_one n with he | ho
  · exact he
  · exfalso
    have hn3 : 3 ≤ n := by omega
    have hgt : n < floorPower n := floorPower_odd_gt hn3 ho
    cases Nat.eq_or_lt_of_le h.1.2.2 with
    | inl h1 =>
        have hper := cycle_iterate_period h.1
        have hlen1 : w.length = 1 := by omega
        rw [hlen1] at hper
        change floorPower n = n at hper
        omega
    | inr hgt1 =>
        have hle : floorPower^[1] n ≤ n := cycleMax_le h hgt1
        exact (not_le_of_gt hgt) hle

theorem exists_cycleMax {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleWord n w) :
    ∃ k < w.length, CycleMax (floorPower^[k] n) (rotateWord w k) := by
  have ⟨i, hi, hge, _heven⟩ := exists_cycle_max_even hn h
  refine ⟨i, hi, cycleWord_rotateWord h i, ?_⟩
  intro j hj
  have hlen : (rotateWord w i).length = w.length := rotateWord_length w i
  rw [hlen] at hj
  have himg : floorPower^[j] (floorPower^[i] n) = floorPower^[i + j] n := by
    simpa [Nat.add_comm] using
      (Function.iterate_add_apply floorPower j i n).symm
  rw [himg, cycle_iterate_mod (k := i + j) h]
  exact hge _ (Nat.mod_lt _ (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) h.2.2))

/-- On a cycle minimum the maximum is even and strictly above `n^2`. -/
theorem cycleMin_max_gt_sq {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∃ i < w.length,
      (∀ j < w.length, floorPower^[j] n ≤ floorPower^[i] n) ∧
        floorPower^[i] n % 2 = 0 ∧ n ^ 2 < floorPower^[i] n := by
  have ⟨i, hi, hmax, heven⟩ := exists_cycle_max_even hn h.1
  refine ⟨i, hi, hmax, heven, ?_⟩
  have hsq := cycleMin_even_ge_sq hn h hi heven
  have hodd := cycleMin_start_odd hn h
  exact lt_of_le_of_ne hsq (even_ne_odd_square heven hodd).symm

theorem cycleMin_max_sqrt_ge {n : ℕ} {w : List Branch} {i : ℕ}
    (_hn : 2 ≤ n) (h : CycleMin n w) (hi : i < w.length)
    (he : floorPower^[i] n % 2 = 0) :
    n ≤ (floorPower^[i] n).sqrt := by
  have hy := cycleMin_succ_ge h hi
  have hz : floorPower (floorPower^[i] n) = (floorPower^[i] n).sqrt :=
    floorPower_even_eq he
  simpa [hz] using hy

theorem cycleMax_return_cell {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMax n w) :
    n % 2 = 0 ∧ n.sqrt ^ 2 ≤ n ∧ n < (n.sqrt + 1) ^ 2 := by
  have he := cycleMax_start_even hn h
  have hfp : floorPower n = n.sqrt := floorPower_even_eq he
  have hI := (floorPower_even_eq_iff_sq_interval he).mp hfp
  exact ⟨he, hI.1, hI.2⟩

theorem follows_take {n : ℕ} :
    ∀ (w : List Branch) (i : ℕ), follows n w → follows n (w.take i)
  | _, 0, _ => trivial
  | [], _i + 1, _ => trivial
  | .even :: rest, i + 1, h =>
      ⟨h.1, follows_take rest i h.2⟩
  | .odd :: rest, i + 1, h =>
      ⟨h.1, follows_take rest i h.2⟩

theorem image_take_of_le {n : ℕ} {w : List Branch} {i : ℕ}
    (hi : i ≤ w.length) :
    image n (w.take i) = floorPower^[i] n := by
  rw [image_eq_iterate, List.length_take, Nat.min_eq_left hi]

/-- Any realized path from `n ≥ 2` to a state at least `n^2` is
superquadratic: `3^o ≥ 2^{k+1}`. Cycle-independent. -/
theorem square_scale_superquadratic {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w) (himg : n ^ 2 ≤ image n w) :
    2 ^ (w.length + 1) ≤ 3 ^ oddCount w := by
  have hpow : (image n w) ^ (2 ^ w.length) ≤ n ^ (3 ^ oddCount w) := by
    simpa [image_eq_iterate] using power_bound_word hw
  have hleft :
      (n ^ 2) ^ (2 ^ w.length) ≤ (image n w) ^ (2 ^ w.length) :=
    Nat.pow_le_pow_left himg _
  have hmul : (n ^ 2) ^ (2 ^ w.length) = n ^ (2 * 2 ^ w.length) :=
    (Nat.pow_mul n 2 (2 ^ w.length)).symm
  have h2 : 2 * 2 ^ w.length = 2 ^ (w.length + 1) :=
    (two_pow_succ w.length).symm
  have hle : n ^ (2 ^ (w.length + 1)) ≤ n ^ (3 ^ oddCount w) := by
    rw [← h2, ← hmul]
    exact le_trans hleft hpow
  exact
    (Nat.pow_le_pow_iff_right
        (lt_of_lt_of_le (by decide : (1 : ℕ) < 2) hn)).mp
      hle

/-- The path from a cycle minimum to any later even state — in
particular to the maximum — is superquadratic. -/
theorem cycleMin_to_even_superquadratic {n : ℕ} {w : List Branch} {i : ℕ}
    (hn : 2 ≤ n) (h : CycleMin n w) (hi : i < w.length)
    (he : floorPower^[i] n % 2 = 0) :
    2 ^ (i + 1) ≤ 3 ^ oddCount (w.take i) := by
  have hw : follows n (w.take i) := follows_take w i h.1.1
  have hlen : (w.take i).length = i := by
    rw [List.length_take, Nat.min_eq_left (Nat.le_of_lt hi)]
  have himg : image n (w.take i) = floorPower^[i] n :=
    image_take_of_le (Nat.le_of_lt hi)
  have hsq : n ^ 2 ≤ floorPower^[i] n := cycleMin_even_ge_sq hn h hi he
  have hsq' : n ^ 2 ≤ image n (w.take i) := by simpa [himg] using hsq
  have hα := square_scale_superquadratic hn hw hsq'
  simpa [hlen] using hα

theorem cycleMin_to_max_superquadratic {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n w) :
    ∃ i < w.length,
      floorPower^[i] n % 2 = 0 ∧ n ^ 2 < floorPower^[i] n ∧
        2 ^ (i + 1) ≤ 3 ^ oddCount (w.take i) := by
  have ⟨i, hi, _hmax, heven, hgt⟩ := cycleMin_max_gt_sq hn h
  exact ⟨i, hi, heven, hgt, cycleMin_to_even_superquadratic hn h hi heven⟩

end Problems.Engine
