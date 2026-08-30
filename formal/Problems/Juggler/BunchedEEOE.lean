import Problems.Juggler.BunchedEOEE
import Problems.Juggler.BunchedEEOEEval

namespace Problems.Juggler

set_option exponentiation.threshold 2048
set_option maxRecDepth 2048
set_option maxHeartbeats 800000

/-!
# Uniform bunched leftovers `O^a EEOE`

`OOOOOEEOE` is the first expanding instance. The mixed cell is
`z < (n+1)^6` for `n ≥ 4`: the last-odd cube gives `y^3 < (n+1)^4`,
two leading evens give `z < (y+1)^4`, and `n ≥ 4` upgrades that to
`z < (n+1)^6`.

The comparison is then the same EOEE tail

`n^{3^a} > 2^{e_a} (n+1)^{6 · 2^a}`

already proved for `a ≥ 5`. Large `n` at `a = 5` is `n ≥ 314`.
At `a = 6` the same cell already fires at `n ≥ 16`. Below those
cutoffs, `a = 5` and `a = 6` are tables and `a ≥ 7` is seven
consecutive odds.

This excludes that one bunched family only. It is not the other
bunched tails, not a length-8 or length-9 census, and not a halt
theorem. Paper A records the family as Theorem 3.18.
-/

def threeEvenEEOE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.even, Branch.odd, Branch.even]

theorem threeEvenEEOE_of_five : threeEvenEEOE 5 = wordOOOOOEEOE :=
  rfl

theorem threeEvenEEOE_of_six : threeEvenEEOE 6 = wordOOOOOOEEOE :=
  rfl

theorem two_mul_succ_cube_lt_succ_pow6 {n y : ℕ} (hn : 4 ≤ n)
    (h : (y + 1) ^ 3 < 2 * (n + 1) ^ 4) :
    (y + 1) ^ 4 < (n + 1) ^ 6 := by
  have h8 : 8 * (y + 1) ^ 3 < 16 * (n + 1) ^ 4 := by
    have h' : 8 * (y + 1) ^ 3 < 8 * (2 * (n + 1) ^ 4) :=
      Nat.mul_lt_mul_of_pos_left h (by decide : (0 : ℕ) < 8)
    have hexp : 8 * (2 * (n + 1) ^ 4) = 16 * (n + 1) ^ 4 := by ring
    rwa [hexp] at h'
  have h16 : 16 * (n + 1) ^ 4 < (n + 1) ^ 6 := by
    have hsq : (16 : ℕ) < (n + 1) ^ 2 := by
      have : 5 ≤ n + 1 := by omega
      have h25 : (25 : ℕ) ≤ (n + 1) ^ 2 := Nat.pow_le_pow_left this 2
      exact lt_of_lt_of_le (by decide : (16 : ℕ) < 25) h25
    have hpos : 0 < (n + 1) ^ 4 := pow_pos (Nat.succ_pos n) 4
    have hr : (n + 1) ^ 6 = (n + 1) ^ 2 * (n + 1) ^ 4 := by
      rw [← Nat.pow_add]
    rw [hr]
    exact Nat.mul_lt_mul_of_pos_right hsq hpos
  have hcube : (2 * (y + 1)) ^ 3 < (n + 1) ^ 6 := by
    have hexp : (2 * (y + 1)) ^ 3 = 8 * (y + 1) ^ 3 := by ring
    exact hexp ▸ (h8.trans h16)
  have h6 : (n + 1) ^ 6 = ((n + 1) ^ 2) ^ 3 := by rw [← Nat.pow_mul]
  have hlin : 2 * (y + 1) < (n + 1) ^ 2 :=
    (Nat.pow_lt_pow_iff_left (by decide : (3 : ℕ) ≠ 0)).mp (h6 ▸ hcube)
  have h4 : (y + 1) ^ 4 = (y + 1) * (y + 1) ^ 3 :=
    (pow_succ (y + 1) 3).trans (mul_comm _ _)
  have hmid : (y + 1) * (y + 1) ^ 3 < (y + 1) * (2 * (n + 1) ^ 4) :=
    Nat.mul_lt_mul_of_pos_left h (Nat.succ_pos y)
  have hmid' : (y + 1) * (2 * (n + 1) ^ 4) = 2 * (y + 1) * (n + 1) ^ 4 := by
    ring
  have hfin : 2 * (y + 1) * (n + 1) ^ 4 < (n + 1) ^ 6 := by
    have hr : (n + 1) ^ 6 = (n + 1) ^ 2 * (n + 1) ^ 4 := by
      rw [← Nat.pow_add]
    rw [hr]
    exact Nat.mul_lt_mul_of_pos_right hlin (pow_pos (Nat.succ_pos n) 4)
  exact h4 ▸ (hmid.trans_eq hmid').trans hfin

theorem threeEvenEEOE_z_lt {n a : ℕ} (hn : 4 ≤ n)
    (h : CycleWord n (threeEvenEEOE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 6 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 4) hn
  set u := List.replicate a Branch.odd ++ [Branch.even]
  have hsplit : threeEvenEEOE a =
      u ++ [Branch.even, Branch.odd, Branch.even] := by
    simp [threeEvenEEOE, u]
  have hC : CycleWord n (u ++ [Branch.even, Branch.odd, Branch.even]) := by
    simpa [hsplit] using h
  have hy3 := cycle_eoe_suffix_y_cube_lt (u := u) hC
  set z := image n (List.replicate a Branch.odd)
  set s := image n (List.replicate a Branch.odd ++ [Branch.even])
  set y := image n (u ++ [Branch.even])
  have hy3' : y ^ 3 < (n + 1) ^ 4 := by
    simpa [y, u] using hy3
  have hf : follows z
      [Branch.even, Branch.even, Branch.odd, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEEOE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hseq : s = floorPower z := by
    simp [s, z, image_append, image]
  have hzlt : z < (s + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hseq.symm).2
  have hf2 : follows s [Branch.even, Branch.odd, Branch.even] := by
    simpa [s, hseq, image] using hf.2
  have he2 : s % 2 = 0 := hf2.1
  have hyeq : y = floorPower s := by
    simp [y, s, u, image_append, image]
  have hslt : s < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he2).mp hyeq.symm).2
  have hys : s + 1 ≤ (y + 1) ^ 2 := Nat.succ_le_of_lt hslt
  have hz4 : z < (y + 1) ^ 4 := by
    have : (s + 1) ^ 2 ≤ ((y + 1) ^ 2) ^ 2 := Nat.pow_le_pow_left hys 2
    have hexp : ((y + 1) ^ 2) ^ 2 = (y + 1) ^ 4 := by rw [← Nat.pow_mul]
    exact lt_of_lt_of_le hzlt (hexp ▸ this)
  have hA : 3 ≤ n + 1 := by omega
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA hy3'
  exact lt_of_lt_of_le hz4 (le_of_lt (two_mul_succ_cube_lt_succ_pow6 hn hysucc))

theorem no_cycle_word_three_even_eeoe_of_ge_five {n a : ℕ}
    (hn : 314 ≤ n) (ha : 5 ≤ a) (h : CycleWord n (threeEvenEEOE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 314) hn
  have hn4 : 4 ≤ n := le_trans (by decide : (4 : ℕ) ≤ 314) hn
  have hz := threeEvenEEOE_z_lt hn4 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.even, Branch.odd, Branch.even])
      (by simpa [threeEvenEEOE] using h.1)
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ a ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image n (List.replicate a Branch.odd) ^ (2 ^ a) <
        (n + 1) ^ (6 * 2 ^ a) :=
    pow_lt_of_lt_pow_mul (k := 6) (m := 2 ^ a) hz hm
  have hlt : n ^ (3 ^ a) <
      2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  exact (not_lt_of_gt (three_even_eoee_tail_of_five hn ha)) hlt

theorem no_cycle_word_three_even_eeoe_of_ge_six {n a : ℕ}
    (hn : 16 ≤ n) (ha : 6 ≤ a) (h : CycleWord n (threeEvenEEOE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 16) hn
  have hn4 : 4 ≤ n := le_trans (by decide : (4 : ℕ) ≤ 16) hn
  have hz := threeEvenEEOE_z_lt hn4 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.even, Branch.odd, Branch.even])
      (by simpa [threeEvenEEOE] using h.1)
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ a ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image n (List.replicate a Branch.odd) ^ (2 ^ a) <
        (n + 1) ^ (6 * 2 ^ a) :=
    pow_lt_of_lt_pow_mul (k := 6) (m := 2 ^ a) hz hm
  have hlt : n ^ (3 ^ a) <
      2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  exact (not_lt_of_gt (three_even_eoee_tail_of_six hn ha)) hlt

theorem threeEvenEEOE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEEOE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.even, Branch.odd, Branch.even])
      (by simpa [threeEvenEEOE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eeoe_of_lt_five {n : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 314) (h : CycleWord n (threeEvenEEOE 5)) :
    False := by
  have hfalse : cycleWordB n wordOOOOOEEOE = false :=
    cycleWordB_ooooo_eeoe_lt314 ⟨n, hn⟩ hn2
  have htrue : cycleWordB n wordOOOOOEEOE = true :=
    cycleWordB_iff.mpr (by simpa [threeEvenEEOE_of_five] using h)
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eeoe_of_lt_six {n : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 16) (h : CycleWord n (threeEvenEEOE 6)) :
    False := by
  have hfalse : cycleWordB n wordOOOOOOEEOE = false :=
    cycleWordB_oooooo_eeoe_lt16 ⟨n, hn⟩ hn2
  have htrue : cycleWordB n wordOOOOOOEEOE = true :=
    cycleWordB_iff.mpr (by simpa [threeEvenEEOE_of_six] using h)
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eeoe {n a : ℕ} (hn : 2 ≤ n) (ha : 5 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.even, Branch.odd, Branch.even]) := by
  intro h
  have hcases : a = 5 ∨ a = 6 ∨ 7 ≤ a := by omega
  rcases hcases with h5 | hrest
  · subst h5
    cases lt_or_ge n 314 with
    | inl hlt => exact no_cycle_word_three_even_eeoe_of_lt_five hn hlt h
    | inr hge => exact no_cycle_word_three_even_eeoe_of_ge_five hge (by decide) h
  rcases hrest with h6 | hge
  · subst h6
    cases lt_or_ge n 16 with
    | inl hlt => exact no_cycle_word_three_even_eeoe_of_lt_six hn hlt h
    | inr hge => exact no_cycle_word_three_even_eeoe_of_ge_six hge (by decide) h
  · cases lt_or_ge n 256 with
    | inl hlt =>
        exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEEOE_follows_seven_odds hge h)
    | inr hge' =>
        exact no_cycle_word_three_even_eeoe_of_ge_six
          (le_trans (by decide : (16 : ℕ) ≤ 256) hge')
          (le_trans (by decide : (6 : ℕ) ≤ 7) hge) h

end Problems.Juggler
