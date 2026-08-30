import Problems.Juggler.BunchedEOOEE
import Problems.Juggler.BunchedEOEE
import Problems.Juggler.BunchedEOEOEEval

namespace Problems.Juggler

/-!
# Uniform bunched leftovers `O^a EOEOE`

`OOOOEOEOE` is the first expanding instance. The mixed cell is
`z < (n+1)^4` for `n ≥ 32`: the last-odd cube gives `y^3 < (n+1)^4`,
the one-odd envelope on the first gap gives `w^3 ≤ 4 s^2`, and
`n ≥ 32` upgrades that to `w < (n+1)^2`, hence `z < (w+1)^2 ≤ (n+1)^4`.

The comparison is then exactly the shared two-even tail already
proved for `O^a EOOEE`. Large `n` is `n ≥ 256`. Below `256`,
`4 ≤ a ≤ 6` is a table and `a ≥ 7` is seven consecutive odds.

This excludes that one bunched family only. It is not the other
bunched tails, not a length-8 or length-9 census, and not a halt
theorem. Paper A records the family as Theorem 3.19.
-/

set_option exponentiation.threshold 2048
set_option maxRecDepth 2048

theorem eight_mul_succ_lt_succ_sq {n y : ℕ} (hn : 32 ≤ n)
    (h : (y + 1) ^ 3 < 2 * (n + 1) ^ 4) :
    8 * (y + 1) < (n + 1) ^ 2 := by
  have h512 : 512 * (y + 1) ^ 3 < 1024 * (n + 1) ^ 4 := by
    have h' : 512 * (y + 1) ^ 3 < 512 * (2 * (n + 1) ^ 4) :=
      Nat.mul_lt_mul_of_pos_left h (by decide : (0 : ℕ) < 512)
    have hexp : 512 * (2 * (n + 1) ^ 4) = 1024 * (n + 1) ^ 4 := by ring
    rwa [hexp] at h'
  have h1024 : 1024 * (n + 1) ^ 4 < (n + 1) ^ 6 := by
    have hsq : (1024 : ℕ) < (n + 1) ^ 2 := by
      have : 33 ≤ n + 1 := by omega
      have h : (33 : ℕ) ^ 2 ≤ (n + 1) ^ 2 := Nat.pow_le_pow_left this 2
      exact lt_of_lt_of_le (by decide : (1024 : ℕ) < 1089) h
    have hpos : 0 < (n + 1) ^ 4 := pow_pos (Nat.succ_pos n) 4
    have hr : (n + 1) ^ 6 = (n + 1) ^ 2 * (n + 1) ^ 4 := by
      rw [← Nat.pow_add]
    rw [hr]
    exact Nat.mul_lt_mul_of_pos_right hsq hpos
  have hcube : (8 * (y + 1)) ^ 3 < (n + 1) ^ 6 := by
    have hexp : (8 * (y + 1)) ^ 3 = 512 * (y + 1) ^ 3 := by ring
    exact hexp ▸ (h512.trans h1024)
  have h6 : (n + 1) ^ 6 = ((n + 1) ^ 2) ^ 3 := by rw [← Nat.pow_mul]
  exact (Nat.pow_lt_pow_iff_left (by decide : (3 : ℕ) ≠ 0)).mp (h6 ▸ hcube)

theorem threeEvenEOEOE_z_lt {n a : ℕ} (hn : 32 ≤ n)
    (h : CycleWord n (threeEvenEOEOE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 4 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 32) hn
  set pref := List.replicate a Branch.odd ++ [Branch.even, Branch.odd]
  have hsplit : threeEvenEOEOE a =
      pref ++ [Branch.even, Branch.odd, Branch.even] := by
    simp [threeEvenEOEOE, pref]
  have hC : CycleWord n
      (pref ++ [Branch.even, Branch.odd, Branch.even]) := by
    simpa [hsplit] using h
  have hy3 := cycle_eoe_suffix_y_cube_lt (u := pref) hC
  set z := image n (List.replicate a Branch.odd)
  set w := image n (List.replicate a Branch.odd ++ [Branch.even])
  set s := image n (List.replicate a Branch.odd ++ [Branch.even, Branch.odd])
  set y := image n (pref ++ [Branch.even])
  have hy3' : y ^ 3 < (n + 1) ^ 4 := by
    simpa [y, pref] using hy3
  have hf : follows z
      [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEOEOE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hweq : w = floorPower z := by
    simp [w, z, image_append, image]
  have hzlt : z < (w + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hweq.symm).2
  have hwO : follows w (List.replicate 1 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even])
      (by simpa [w, hweq, image, List.replicate] using hf.2)
  have hw1 : 1 ≤ w := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [w, hweq] using floorPower_pos hz1
  have hpow := odd_run_lower_growth (n := w) (a := 1) hw1 hwO
  have hseq : s = image w (List.replicate 1 Branch.odd) := by
    simp [s, w, image_append, image]
  have hle' : w ^ 3 ≤ 4 * s ^ 2 := by
    simpa [denomBits_one, hseq] using hpow
  have hf2 : follows s [Branch.even, Branch.odd, Branch.even] := by
    have hf1 : follows w
        [Branch.odd, Branch.even, Branch.odd, Branch.even] := by
      simpa [w, hweq, image] using hf.2
    simpa [s, hseq, image, List.replicate] using hf1.2
  have hes : s % 2 = 0 := hf2.1
  have hyeq : y = floorPower s := by
    simp [y, s, pref, image_append, image]
  have hslt : s < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval hes).mp hyeq.symm).2
  have hss : s + 1 ≤ (y + 1) ^ 2 := Nat.succ_le_of_lt hslt
  have hs4 : s ^ 2 < (y + 1) ^ 4 := by
    have : s < (y + 1) ^ 2 := hslt
    exact pow_lt_of_lt_pow_mul (k := 2) (m := 2) this (by decide)
  have hplt : 4 * s ^ 2 < 4 * (y + 1) ^ 4 :=
    Nat.mul_lt_mul_of_pos_left hs4 (by decide : (0 : ℕ) < 4)
  have hw3 : w ^ 3 < 4 * (y + 1) ^ 4 := lt_of_le_of_lt hle' hplt
  have hA : 3 ≤ n + 1 := by omega
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA hy3'
  have h8 : 8 * (y + 1) < (n + 1) ^ 2 := eight_mul_succ_lt_succ_sq hn hysucc
  have hy4 : (y + 1) ^ 4 = (y + 1) * (y + 1) ^ 3 :=
    (pow_succ (y + 1) 3).trans (mul_comm _ _)
  have h4y : 4 * (y + 1) ^ 4 < (n + 1) ^ 6 := by
    have hmid : 4 * (y + 1) * (y + 1) ^ 3 <
        4 * (y + 1) * (2 * (n + 1) ^ 4) :=
      Nat.mul_lt_mul_of_pos_left hysucc
        (Nat.mul_pos (by decide : (0 : ℕ) < 4) (Nat.succ_pos y))
    have hexp : 4 * (y + 1) * (2 * (n + 1) ^ 4) =
        8 * (y + 1) * (n + 1) ^ 4 := by ring
    have hfin : 8 * (y + 1) * (n + 1) ^ 4 < (n + 1) ^ 6 := by
      have hr : (n + 1) ^ 6 = (n + 1) ^ 2 * (n + 1) ^ 4 := by
        rw [← Nat.pow_add]
      rw [hr]
      exact Nat.mul_lt_mul_of_pos_right h8 (pow_pos (Nat.succ_pos n) 4)
    have h4y' : 4 * (y + 1) ^ 4 = 4 * (y + 1) * (y + 1) ^ 3 := by
      rw [hy4, mul_assoc]
    exact h4y' ▸ (hmid.trans_eq hexp).trans hfin
  have hw6 : w ^ 3 < (n + 1) ^ 6 := hw3.trans h4y
  have h6 : (n + 1) ^ 6 = ((n + 1) ^ 2) ^ 3 := by rw [← Nat.pow_mul]
  have hwlt : w < (n + 1) ^ 2 :=
    (Nat.pow_lt_pow_iff_left (by decide : (3 : ℕ) ≠ 0)).mp (h6 ▸ hw6)
  have hws : w + 1 ≤ (n + 1) ^ 2 := Nat.succ_le_of_lt hwlt
  have : (w + 1) ^ 2 ≤ ((n + 1) ^ 2) ^ 2 := Nat.pow_le_pow_left hws 2
  have hexp : ((n + 1) ^ 2) ^ 2 = (n + 1) ^ 4 := by rw [← Nat.pow_mul]
  exact lt_of_lt_of_le hzlt (hexp ▸ this)

theorem no_cycle_word_three_even_eoeoe_of_ge {n a : ℕ}
    (hn : 256 ≤ n) (ha : 4 ≤ a) (h : CycleWord n (threeEvenEOEOE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn32 : 32 ≤ n := le_trans (by decide : (32 : ℕ) ≤ 256) hn
  have hz := threeEvenEOEOE_z_lt hn32 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even])
      (by simpa [threeEvenEOEOE] using h.1)
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

theorem threeEvenEOEOE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEOEOE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even])
      (by simpa [threeEvenEOEOE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eoeoe_of_lt {n a : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha4 : 4 ≤ a) (ha6 : a ≤ 6)
    (h : CycleWord n (threeEvenEOEOE a)) : False := by
  have hA : a - 4 < 3 := by omega
  have hfalse :
      cycleWordB n (threeEvenEOEOE (a - 4 + 4)) = false :=
    cycleWordB_eoeoe_prefix_lt256 ⟨n, hn⟩ ⟨a - 4, hA⟩ hn2
  have ha : a - 4 + 4 = a := by omega
  have hfalse' : cycleWordB n (threeEvenEOEOE a) = false := by
    simpa [ha] using hfalse
  have htrue : cycleWordB n (threeEvenEOEOE a) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eoeoe {n a : ℕ} (hn : 2 ≤ n) (ha : 4 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even]) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt =>
      have hcases : a ≤ 6 ∨ 7 ≤ a := by omega
      rcases hcases with hle | hge
      · exact no_cycle_word_three_even_eoeoe_of_lt hn hlt ha hle h
      · exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEOEOE_follows_seven_odds hge h)
  | inr hge => exact no_cycle_word_three_even_eoeoe_of_ge hge ha h

end Problems.Juggler
