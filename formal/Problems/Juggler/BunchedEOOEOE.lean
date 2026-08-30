import Problems.Juggler.BunchedEOOOEE
import Problems.Juggler.BunchedEOOEOEEval

namespace Problems.Juggler

/-!
# Uniform bunched leftovers `O^a EOOEOE`

`OOOEOOEOE` is the first expanding instance. For `a ≥ 4` the mixed
cell is `z < (n+1)^4`. At `a = 3` the two-odd plus last-odd geometry
recovers the same tight comparison already used for `O^3 EOOOEE`.

Large `n` is `n ≥ 256`. Below `256`, `3 ≤ a ≤ 6` is a table and
`a ≥ 7` is seven consecutive odds.

This excludes that one bunched family only. It is not a length-8
or length-9 census and not a halt theorem. Paper A records the
family as Theorem 3.20.
-/

set_option exponentiation.threshold 16
set_option maxRecDepth 512
set_option maxHeartbeats 400000

theorem threeEvenEOOEOE_z_lt {n a : ℕ} (hn : 4 ≤ n)
    (h : CycleWord n (threeEvenEOOEOE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 4 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 4) hn
  set pref :=
    List.replicate a Branch.odd ++ [Branch.even, Branch.odd, Branch.odd]
  have hsplit : threeEvenEOOEOE a =
      pref ++ [Branch.even, Branch.odd, Branch.even] := by
    simp [threeEvenEOOEOE, pref]
  have hC : CycleWord n
      (pref ++ [Branch.even, Branch.odd, Branch.even]) := by
    simpa [hsplit] using h
  have hy3 := cycle_eoe_suffix_y_cube_lt (u := pref) hC
  set z := image n (List.replicate a Branch.odd)
  set uimg := image n (List.replicate a Branch.odd ++ [Branch.even])
  set s := image n pref
  set y := image n (pref ++ [Branch.even])
  have hy3' : y ^ 3 < (n + 1) ^ 4 := by
    simpa [y, pref] using hy3
  have hf : follows z
      [Branch.even, Branch.odd, Branch.odd, Branch.even,
        Branch.odd, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEOOEOE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hueq : uimg = floorPower z := by
    simp [uimg, z, image_append, image]
  have hzlt : z < (uimg + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hueq.symm).2
  have huO : follows uimg (List.replicate 2 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even])
      (by simpa [uimg, hueq, image, List.replicate] using hf.2)
  have hu1 : 1 ≤ uimg := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [uimg, hueq] using floorPower_pos hz1
  have hpow := odd_run_lower_growth (n := uimg) (a := 2) hu1 huO
  have hseq : s = image uimg (List.replicate 2 Branch.odd) := by
    simp [s, uimg, pref, image_append, image]
  have hle' : uimg ^ 9 ≤ 1024 * s ^ 4 := by
    simpa [denomBits_two, three_pow_two, two_pow_ten, hseq] using hpow
  have hf1 : follows uimg
      [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.even] := by
    simpa [uimg, hueq, image] using hf.2
  have hf2 : follows s [Branch.even, Branch.odd, Branch.even] := by
    have := follows_of_append_right (u := List.replicate 2 Branch.odd) hf1
    simpa [s, hseq, image, List.replicate] using this
  have hes : s % 2 = 0 := hf2.1
  have hyeq : y = floorPower s := by
    simp [y, s, pref, image_append, image]
  have hslt : s < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval hes).mp hyeq.symm).2
  have hs4 : s ^ 4 < (y + 1) ^ 8 :=
    pow_lt_of_lt_pow_mul (k := 2) (m := 4) hslt (by decide)
  have hu9 : uimg ^ 9 < 1024 * (y + 1) ^ 8 :=
    lt_of_le_of_lt hle'
      (Nat.mul_lt_mul_of_pos_left hs4 (by decide : (0 : ℕ) < 1024))
  have hA : 3 ≤ n + 1 := by omega
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA hy3'
  exact z_lt_succ_pow4_of_y hzlt (eooeoe_u_lt_succ_sq hn hu9 hysucc)

theorem no_cycle_word_three_even_eooeoe_of_ge_four {n a : ℕ}
    (hn : 256 ≤ n) (ha : 4 ≤ a) (h : CycleWord n (threeEvenEOOEOE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn4 : 4 ≤ n := le_trans (by decide : (4 : ℕ) ≤ 256) hn
  have hz := threeEvenEOOEOE_z_lt hn4 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.even,
        Branch.odd, Branch.even])
      (by simpa [threeEvenEOOEOE] using h.1)
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

theorem no_cycle_word_three_even_eooeoe_of_ge_three {n : ℕ}
    (hn : 256 ≤ n) (h : CycleWord n (threeEvenEOOEOE 3)) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn197 : 197 ≤ n := le_trans (by decide : (197 : ℕ) ≤ 256) hn
  have hn24 : 24 ≤ n := le_trans (by decide : (24 : ℕ) ≤ 256) hn
  set z := image n (List.replicate 3 Branch.odd)
  set uimg := image n (List.replicate 3 Branch.odd ++ [Branch.even])
  set pref :=
    List.replicate 3 Branch.odd ++ [Branch.even, Branch.odd, Branch.odd]
  set s := image n pref
  set y := image n (pref ++ [Branch.even])
  have hueq : uimg = floorPower z := by
    simp [uimg, z, image_append, image]
  have hf : follows z
      [Branch.even, Branch.odd, Branch.odd, Branch.even,
        Branch.odd, Branch.even] :=
    follows_of_append_right (u := List.replicate 3 Branch.odd)
      (by simpa [threeEvenEOOEOE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hzlt : z < (uimg + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hueq.symm).2
  have hO : follows n (List.replicate 3 Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.even,
        Branch.odd, Branch.even])
      (by simpa [threeEvenEOOEOE] using h.1)
  have hpow := odd_run_lower_growth hn1 hO
  have hz8 : z ^ 8 < (uimg + 1) ^ 16 :=
    pow_lt_of_lt_pow_mul (k := 2) (m := 8) hzlt (by decide)
  have h27 : n ^ 27 < 2 ^ 38 * (uimg + 1) ^ 16 := by
    have hle : n ^ 27 ≤ 2 ^ 38 * z ^ 8 := by
      simpa [denomBits_three, three_pow_three, z] using hpow
    exact lt_of_le_of_lt hle
      (Nat.mul_lt_mul_of_pos_left hz8
        (pow_pos (by decide : (0 : ℕ) < 2) 38))
  have hC : CycleWord n
      (pref ++ [Branch.even, Branch.odd, Branch.even]) := by
    simpa [threeEvenEOOEOE, pref] using h
  have hy3 := cycle_eoe_suffix_y_cube_lt (u := pref) hC
  have hy3' : y ^ 3 < (n + 1) ^ 4 := by
    simpa [y, pref] using hy3
  have huO : follows uimg (List.replicate 2 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even])
      (by simpa [uimg, hueq, image, List.replicate] using hf.2)
  have hu1 : 1 ≤ uimg := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [uimg, hueq] using floorPower_pos hz1
  have hpowu := odd_run_lower_growth (n := uimg) (a := 2) hu1 huO
  have hseq : s = image uimg (List.replicate 2 Branch.odd) := by
    simp [s, uimg, pref, image_append, image]
  have hle' : uimg ^ 9 ≤ 1024 * s ^ 4 := by
    simpa [denomBits_two, three_pow_two, two_pow_ten, hseq] using hpowu
  have hf1 : follows uimg
      [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.even] := by
    simpa [uimg, hueq, image] using hf.2
  have hf2 : follows s [Branch.even, Branch.odd, Branch.even] := by
    have := follows_of_append_right (u := List.replicate 2 Branch.odd) hf1
    simpa [s, hseq, image, List.replicate] using this
  have hes : s % 2 = 0 := hf2.1
  have hyeq : y = floorPower s := by
    simp [y, s, pref, image_append, image]
  have hslt : s < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval hes).mp hyeq.symm).2
  have hs4 : s ^ 4 < (y + 1) ^ 8 :=
    pow_lt_of_lt_pow_mul (k := 2) (m := 4) hslt (by decide)
  have hu9 : uimg ^ 9 < 1024 * (y + 1) ^ 8 :=
    lt_of_le_of_lt hle'
      (Nat.mul_lt_mul_of_pos_left hs4 (by decide : (0 : ℕ) < 1024))
  have hA : 3 ≤ n + 1 := by omega
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA hy3'
  have hu27 : uimg ^ 27 < 2 ^ 38 * (n + 1) ^ 32 :=
    eooeoe_u_pow27 hu9 hysucc
  cases lt_or_ge uimg 39 with
  | inl hlt => exact eoooee_small_y_false hn24 hlt h27
  | inr hge => exact eoooee_large_y_false hn197 hge hu27 h27

theorem threeEvenEOOEOE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEOOEOE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.even,
        Branch.odd, Branch.even])
      (by simpa [threeEvenEOOEOE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eooeoe_of_lt {n a : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha3 : 3 ≤ a) (ha6 : a ≤ 6)
    (h : CycleWord n (threeEvenEOOEOE a)) : False := by
  have hA : a - 3 < 4 := by omega
  have hfalse :
      cycleWordB n (threeEvenEOOEOE (a - 3 + 3)) = false :=
    cycleWordB_eooeoe_prefix_lt256 ⟨n, hn⟩ ⟨a - 3, hA⟩ hn2
  have ha : a - 3 + 3 = a := by omega
  have hfalse' : cycleWordB n (threeEvenEOOEOE a) = false := by
    simpa [ha] using hfalse
  have htrue : cycleWordB n (threeEvenEOOEOE a) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eooeoe {n a : ℕ} (hn : 2 ≤ n) (ha : 3 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.even,
          Branch.odd, Branch.even]) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt =>
      have hcases : a ≤ 6 ∨ 7 ≤ a := by omega
      rcases hcases with hle | hge
      · exact no_cycle_word_three_even_eooeoe_of_lt hn hlt ha hle h
      · exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEOOEOE_follows_seven_odds hge h)
  | inr hge =>
      have hcases : a = 3 ∨ 4 ≤ a := by omega
      rcases hcases with h3 | h4
      · subst h3
        exact no_cycle_word_three_even_eooeoe_of_ge_three hge h
      · exact no_cycle_word_three_even_eooeoe_of_ge_four hge h4 h

end Problems.Juggler
