import Problems.Juggler.LeftoverTwoEven

namespace Problems.Juggler

/-!
# Uniform three-trailing-even leftovers `O^a EEE`

`OOOOOOEEE` is the first expanding instance. The three-even cell
`z < (n+1)^8` against `C_{O^a}` is the comparison

`n^{3^a} > 2^{e_a} (n+1)^{2^{a+3}}`

with `e_a = denomBits a`. Large `n` is the `a = 6` comparison at
`n ≥ 128`, cubed in `a`. Below `128`, `a = 6` is the existing table
and `a ≥ 7` is seven consecutive odds.

This excludes that one bunched family only. It is not the other six
bunched tails, not a length-8 or length-9 census, and not a halt
theorem. Paper A is not edited.
-/

def threeEvenEEE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++ List.replicate 3 Branch.even

theorem eight_mul_two_pow (a : ℕ) : 8 * 2 ^ a = 2 ^ (a + 3) := by
  have h8 : (8 : ℕ) = 2 ^ 3 := rfl
  rw [h8, ← Nat.pow_add]
  congr 1
  omega

theorem four_mul_two_pow_succ (a : ℕ) : 4 * 2 ^ (a + 1) = 2 ^ (a + 3) := by
  have h4 : (4 : ℕ) = 2 ^ 2 := rfl
  rw [h4, ← Nat.pow_add]
  congr 1
  omega

theorem denomBits_six : denomBits 6 = 1330 := by
  native_decide

theorem three_pow_six : (3 : ℕ) ^ 6 = 729 := by
  decide

theorem two_pow_nine : (2 : ℕ) ^ 9 = 512 := by
  decide

theorem two_pow_six_add_three : (2 : ℕ) ^ (6 + 3) = 512 :=
  two_pow_nine

theorem threeEvenEEE_of_six : threeEvenEEE 6 = wordOOOOOOEEE :=
  rfl

theorem three_even_eee_tail_succ {n a : ℕ} (hn : 128 ≤ n)
    (ih : 2 ^ denomBits a * (n + 1) ^ (2 ^ (a + 3)) < n ^ (3 ^ a)) :
    2 ^ denomBits (a + 1) * (n + 1) ^ (2 ^ (a + 4)) <
      n ^ (3 ^ (a + 1)) := by
  have hcube :
      2 ^ (3 * denomBits a) * (n + 1) ^ (3 * 2 ^ (a + 3)) <
        n ^ (3 ^ (a + 1)) := by
    have hlt :
        (2 ^ denomBits a * (n + 1) ^ (2 ^ (a + 3))) ^ 3 <
          (n ^ (3 ^ a)) ^ 3 :=
      Nat.pow_lt_pow_left ih (by decide : (3 : ℕ) ≠ 0)
    have hL : (2 ^ denomBits a * (n + 1) ^ (2 ^ (a + 3))) ^ 3 =
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * 2 ^ (a + 3)) :=
      two_mul_pow_cube _ _ _
    have hR : (n ^ (3 ^ a)) ^ 3 = n ^ (3 ^ (a + 1)) := by
      rw [← Nat.pow_mul, ← Nat.pow_succ]
    rwa [hL, hR] at hlt
  have hsucc4 : 2 < (n + 1) ^ 4 := by
    have h16 : (16 : ℕ) ≤ (n + 1) ^ 4 := by
      have : 2 ≤ n + 1 := by omega
      simpa using Nat.pow_le_pow_left this 4
    exact lt_of_lt_of_le (by decide : (2 : ℕ) < 16) h16
  have hpow4 : 2 ^ (2 ^ (a + 1)) < (n + 1) ^ (2 ^ (a + 3)) := by
    have hm : 2 ^ (a + 1) ≠ 0 :=
      Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
    have : 2 ^ (2 ^ (a + 1)) < ((n + 1) ^ 4) ^ (2 ^ (a + 1)) :=
      Nat.pow_lt_pow_left hsucc4 hm
    rwa [← Nat.pow_mul, four_mul_two_pow_succ a] at this
  have he' : denomBits (a + 1) = 3 * denomBits a + 2 ^ (a + 1) :=
    denomBits_succ a
  have hfactor :
      2 ^ denomBits (a + 1) * (n + 1) ^ (2 ^ (a + 4)) <
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * 2 ^ (a + 3)) := by
    have hL :
        2 ^ denomBits (a + 1) * (n + 1) ^ (2 ^ (a + 4)) =
          2 ^ (3 * denomBits a) *
            (2 ^ (2 ^ (a + 1)) * (n + 1) ^ (2 ^ (a + 4))) := by
      rw [he', Nat.pow_add, mul_assoc]
    have hR :
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * 2 ^ (a + 3)) =
          2 ^ (3 * denomBits a) *
            ((n + 1) ^ (2 ^ (a + 3)) * (n + 1) ^ (2 ^ (a + 4))) := by
      congr 1
      rw [← Nat.pow_add, three_mul_two_pow]
    have hpos2 : 0 < 2 ^ (3 * denomBits a) :=
      pow_pos (by decide : (0 : ℕ) < 2) _
    have hposn : 0 < (n + 1) ^ (2 ^ (a + 4)) :=
      pow_pos (Nat.succ_pos n) _
    rw [hL, hR]
    exact Nat.mul_lt_mul_of_pos_left
      (Nat.mul_lt_mul_of_pos_right hpow4 hposn) hpos2
  exact hfactor.trans hcube

theorem three_even_eee_tail {n a : ℕ} (hn : 128 ≤ n) (ha : 6 ≤ a) :
    2 ^ denomBits a * (n + 1) ^ (2 ^ (a + 3)) < n ^ (3 ^ a) := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le ha
  subst ht
  clear ha
  induction t with
  | zero =>
      rw [denomBits_six, three_pow_six, two_pow_six_add_three]
      exact pow729_gt_two_pow1330_succ_pow512 hn
  | succ t ih =>
      exact three_even_eee_tail_succ hn ih

theorem no_cycle_word_three_even_eee_of_ge {n a : ℕ}
    (hn : 128 ≤ n) (ha : 6 ≤ a) (h : CycleWord n (threeEvenEEE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 128) hn
  have hz := cycle_trailing_evens_lt (r := 3) (by decide) h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left (v := List.replicate 3 Branch.even) h.1
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ a ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image n (List.replicate a Branch.odd) ^ (2 ^ a) <
        (n + 1) ^ (2 ^ (a + 3)) := by
    have := pow_lt_of_lt_pow_mul (k := 8) (m := 2 ^ a) hz hm
    rwa [eight_mul_two_pow a] at this
  have hlt : n ^ (3 ^ a) <
      2 ^ denomBits a * (n + 1) ^ (2 ^ (a + 3)) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  exact (not_lt_of_gt (three_even_eee_tail hn ha)) hlt

theorem threeEvenEEE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEEE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left (v := List.replicate 3 Branch.even) h.1
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eee_of_lt {n a : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 128) (ha : 6 ≤ a)
    (h : CycleWord n (threeEvenEEE a)) : False := by
  have hcases : a = 6 ∨ 7 ≤ a := by omega
  rcases hcases with h6 | hge
  · subst h6
    exact no_cycle_word_ooooooeee hn2 (by simpa [threeEvenEEE_of_six] using h)
  · exact no_follows_seven_odds_of_lt256 hn2
      (lt_trans hn (by decide : (128 : ℕ) < 256))
      (threeEvenEEE_follows_seven_odds hge h)

theorem no_cycle_word_three_even_eee {n a : ℕ} (hn : 2 ≤ n) (ha : 6 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++ List.replicate 3 Branch.even) := by
  intro h
  cases lt_or_ge n 128 with
  | inl hlt => exact no_cycle_word_three_even_eee_of_lt hn hlt ha h
  | inr hge => exact no_cycle_word_three_even_eee_of_ge hge ha h

end Problems.Juggler
