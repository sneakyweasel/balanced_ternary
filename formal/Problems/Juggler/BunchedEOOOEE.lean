import Problems.Juggler.BunchedEOOEE
import Problems.Juggler.BunchedTight

namespace Problems.Juggler

/-!
# Uniform bunched leftovers `O^a EOOOEE`

`OOOEOOOEE` is the first expanding instance. For `a ≥ 4` the mixed
cell is `z < (n+1)^4`. At `a = 3` the coarse exponent is impossible,
so the argument uses the tight cell against `C_{O^3}`.

Large `n` is `n ≥ 256`. Below `256`, `3 ≤ a ≤ 6` is a table and
`a ≥ 7` is seven consecutive odds.

This excludes that one bunched family only. It is not a length-8
or length-9 census and not a halt theorem. Paper A records the
family as Theorem 3.17.
-/

set_option exponentiation.threshold 16
set_option maxRecDepth 512
set_option maxHeartbeats 400000

theorem denomBits_three : denomBits 3 = 38 := by
  decide

theorem three_pow_three : (3 : ℕ) ^ 3 = 27 := by
  decide

theorem threeEvenEOOOEE_z_lt {n a : ℕ} (hn : 3 ≤ n)
    (h : CycleWord n (threeEvenEOOOEE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 4 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 3) hn
  have hsplit : threeEvenEOOOEE a =
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even := by
    simp [threeEvenEOOOEE]
  have hC : CycleWord n
      ((List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even) := by
    simpa [hsplit] using h
  have hp := cycle_trailing_evens_lt (r := 2) (by decide) hC
  set z := image n (List.replicate a Branch.odd)
  set y := image n (List.replicate a Branch.odd ++ [Branch.even])
  have hyeq : y = floorPower z := by
    simp [y, z, image_append, image]
  have hf : follows z
      [Branch.even, Branch.odd, Branch.odd, Branch.odd,
        Branch.even, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEOOOEE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hzlt : z < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq.symm).2
  have hyO : follows y (List.replicate 3 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.even])
      (by simpa [y, hyeq, image, List.replicate] using hf.2)
  have hy1 : 1 ≤ y := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [y, hyeq] using floorPower_pos hz1
  have hpow := odd_run_lower_growth (n := y) (a := 3) hy1 hyO
  have hpimg :
      image n (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) =
        image y (List.replicate 3 Branch.odd) := by
    simp [y, image_append, image]
  have hle' : y ^ 27 ≤ 2 ^ 38 * image y (List.replicate 3 Branch.odd) ^ 8 := by
    simpa [denomBits_three, three_pow_three] using hpow
  have hp' : image y (List.replicate 3 Branch.odd) < (n + 1) ^ 4 := by
    rwa [← hpimg]
  have hplt : 2 ^ 38 * image y (List.replicate 3 Branch.odd) ^ 8 <
      2 ^ 38 * (n + 1) ^ 32 := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 8) hp' (by decide)
    exact Nat.mul_lt_mul_of_pos_left this
      (pow_pos (by decide : (0 : ℕ) < 2) 38)
  have hy27 : y ^ 27 < 2 ^ 38 * (n + 1) ^ 32 := lt_of_le_of_lt hle' hplt
  exact z_lt_succ_pow4_of_y hzlt (y_lt_succ_sq_of_odd27 hn hy27)

theorem no_cycle_word_three_even_eoooee_of_ge_four {n a : ℕ}
    (hn : 256 ≤ n) (ha : 4 ≤ a) (h : CycleWord n (threeEvenEOOOEE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn3 : 3 ≤ n := le_trans (by decide : (3 : ℕ) ≤ 256) hn
  have hz := threeEvenEOOOEE_z_lt hn3 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.odd,
        Branch.even, Branch.even])
      (by simpa [threeEvenEOOOEE] using h.1)
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ a ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image n (List.replicate a Branch.odd) ^ (2 ^ a) <
        (n + 1) ^ (4 * 2 ^ a) :=
    pow_lt_of_lt_pow_mul (k := 4) (m := 2 ^ a) hz hm
  have hlt : n ^ (3 ^ a) <
      2 ^ denomBits a * (n + 1) ^ (4 * 2 ^ a) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  exact (not_lt_of_gt (three_even_eooee_tail hn ha)) hlt

theorem no_cycle_word_three_even_eoooee_of_ge_three {n : ℕ}
    (hn : 256 ≤ n) (h : CycleWord n (threeEvenEOOOEE 3)) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn197 : 197 ≤ n := le_trans (by decide : (197 : ℕ) ≤ 256) hn
  have hn24 : 24 ≤ n := le_trans (by decide : (24 : ℕ) ≤ 256) hn
  set z := image n (List.replicate 3 Branch.odd)
  set y := image n (List.replicate 3 Branch.odd ++ [Branch.even])
  have hyeq : y = floorPower z := by
    simp [y, z, image_append, image]
  have hf : follows z
      [Branch.even, Branch.odd, Branch.odd, Branch.odd,
        Branch.even, Branch.even] :=
    follows_of_append_right (u := List.replicate 3 Branch.odd)
      (by simpa [threeEvenEOOOEE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hzlt : z < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq.symm).2
  have hO : follows n (List.replicate 3 Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.odd,
        Branch.even, Branch.even])
      (by simpa [threeEvenEOOOEE] using h.1)
  have hpow := odd_run_lower_growth hn1 hO
  have hz8 : z ^ 8 < (y + 1) ^ 16 :=
    pow_lt_of_lt_pow_mul (k := 2) (m := 8) hzlt (by decide)
  have h27 : n ^ 27 < 2 ^ 38 * (y + 1) ^ 16 := by
    have hle : n ^ 27 ≤ 2 ^ 38 * z ^ 8 := by
      simpa [denomBits_three, three_pow_three, z] using hpow
    exact lt_of_le_of_lt hle
      (Nat.mul_lt_mul_of_pos_left hz8
        (pow_pos (by decide : (0 : ℕ) < 2) 38))
  have hsplit : threeEvenEOOOEE 3 =
      (List.replicate 3 Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even := by
    simp [threeEvenEOOOEE]
  have hC : CycleWord n
      ((List.replicate 3 Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even) := by
    simpa [hsplit] using h
  have hp := cycle_trailing_evens_lt (r := 2) (by decide) hC
  have hyO : follows y (List.replicate 3 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.even])
      (by simpa [y, hyeq, image, List.replicate] using hf.2)
  have hy1 : 1 ≤ y := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [y, hyeq] using floorPower_pos hz1
  have hpowy := odd_run_lower_growth (n := y) (a := 3) hy1 hyO
  have hpimg :
      image n (List.replicate 3 Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd]) =
        image y (List.replicate 3 Branch.odd) := by
    simp [y, image_append, image]
  have hle' : y ^ 27 ≤ 2 ^ 38 * image y (List.replicate 3 Branch.odd) ^ 8 := by
    simpa [denomBits_three, three_pow_three] using hpowy
  have hp' : image y (List.replicate 3 Branch.odd) < (n + 1) ^ 4 := by
    rwa [← hpimg]
  have hplt : 2 ^ 38 * image y (List.replicate 3 Branch.odd) ^ 8 <
      2 ^ 38 * (n + 1) ^ 32 := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 8) hp' (by decide)
    exact Nat.mul_lt_mul_of_pos_left this
      (pow_pos (by decide : (0 : ℕ) < 2) 38)
  have hy27 : y ^ 27 < 2 ^ 38 * (n + 1) ^ 32 := lt_of_le_of_lt hle' hplt
  cases lt_or_ge y 39 with
  | inl hlt => exact eoooee_small_y_false hn24 hlt h27
  | inr hge => exact eoooee_large_y_false hn197 hge hy27 h27

theorem threeEvenEOOOEE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEOOOEE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.odd,
        Branch.even, Branch.even])
      (by simpa [threeEvenEOOOEE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eoooee_of_lt {n a : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha3 : 3 ≤ a) (ha6 : a ≤ 6)
    (h : CycleWord n (threeEvenEOOOEE a)) : False := by
  have hA : a - 3 < 4 := by omega
  have hfalse :
      cycleWordB n (threeEvenEOOOEE (a - 3 + 3)) = false :=
    cycleWordB_eoooee_prefix_lt256 ⟨n, hn⟩ ⟨a - 3, hA⟩ hn2
  have ha : a - 3 + 3 = a := by omega
  have hfalse' : cycleWordB n (threeEvenEOOOEE a) = false := by
    simpa [ha] using hfalse
  have htrue : cycleWordB n (threeEvenEOOOEE a) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eoooee {n a : ℕ} (hn : 2 ≤ n) (ha : 3 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.odd,
          Branch.even, Branch.even]) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt =>
      have hcases : a ≤ 6 ∨ 7 ≤ a := by omega
      rcases hcases with hle | hge
      · exact no_cycle_word_three_even_eoooee_of_lt hn hlt ha hle h
      · exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEOOOEE_follows_seven_odds hge h)
  | inr hge =>
      have hcases : a = 3 ∨ 4 ≤ a := by omega
      rcases hcases with h3 | h4
      · subst h3
        exact no_cycle_word_three_even_eoooee_of_ge_three hge h
      · exact no_cycle_word_three_even_eoooee_of_ge_four hge h4 h

end Problems.Juggler
