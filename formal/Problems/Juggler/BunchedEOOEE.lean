import Problems.Juggler.LeftoverTwoEven
import Problems.Juggler.BunchedEOOEEEval

namespace Problems.Juggler

/-!
# Uniform bunched leftovers `O^a EOOEE`

`OOOOEOOEE` is the first expanding instance. The mixed cell is
`z < (n+1)^4` for `n ≥ 32`: two trailing evens give `p < (n+1)^4`,
the two-odd lower envelope gives `y^9 ≤ 1024 p^4`, and `n ≥ 32`
upgrades that to `y < (n+1)^2`, hence `z < (y+1)^2 ≤ (n+1)^4`.

The comparison is then exactly the shared two-even tail

`n^{3^a} > 2^{e_a} (n+1)^{2^{a+2}}`

with `e_a = denomBits a`. Large `n` is `n ≥ 256`, already proved
for every `a ≥ 4`. Below `256`, `4 ≤ a ≤ 6` is a table and
`a ≥ 7` is seven consecutive odds.

This excludes that one bunched family only. It is not the other
four bunched tails, not a length-8 or length-10 census, and not a
halt theorem. Paper A records the family as Theorem 3.16.
-/

set_option exponentiation.threshold 2048
set_option maxRecDepth 2048

theorem four_mul_two_pow_a (a : ℕ) : 4 * 2 ^ a = 2 ^ (a + 2) := by
  have h4 : (4 : ℕ) = 2 ^ 2 := rfl
  rw [h4, ← Nat.pow_add]
  congr 1
  omega

theorem denomBits_two : denomBits 2 = 10 := by
  decide

theorem three_pow_two : (3 : ℕ) ^ 2 = 9 := by
  decide

theorem two_pow_ten : (2 : ℕ) ^ 10 = 1024 := by
  decide

theorem two_pow10_lt_succ_sq {n : ℕ} (hn : 32 ≤ n) :
    1024 < (n + 1) ^ 2 := by
  have : 33 ≤ n + 1 := by omega
  have h : (33 : ℕ) ^ 2 ≤ (n + 1) ^ 2 := Nat.pow_le_pow_left this 2
  exact lt_of_lt_of_le (by decide : (1024 : ℕ) < 1089) h

theorem two_pow10_succ_pow16_lt_succ_pow18 {n : ℕ} (hn : 32 ≤ n) :
    1024 * (n + 1) ^ 16 < (n + 1) ^ 18 := by
  have hpos : 0 < (n + 1) ^ 16 := pow_pos (Nat.succ_pos n) 16
  have hr : (n + 1) ^ 18 = (n + 1) ^ 2 * (n + 1) ^ 16 := by
    rw [← Nat.pow_add]
  rw [hr]
  exact Nat.mul_lt_mul_of_pos_right (two_pow10_lt_succ_sq hn) hpos

theorem three_even_eooee_tail {n a : ℕ} (hn : 256 ≤ n) (ha : 4 ≤ a) :
    2 ^ denomBits a * (n + 1) ^ (4 * 2 ^ a) < n ^ (3 ^ a) := by
  have hk : 6 ≤ a + 2 := by omega
  have h := shared_two_even_tail (k := a + 2) hn hk
  have hsub : a + 2 - 2 = a := by omega
  simpa [hsub, four_mul_two_pow_a a] using h

theorem threeEvenEOOEE_z_lt {n a : ℕ} (hn : 32 ≤ n)
    (h : CycleWord n (threeEvenEOOEE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 4 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 32) hn
  have hsplit : threeEvenEOOEE a =
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even := by
    simp [threeEvenEOOEE]
  have hC : CycleWord n
      ((List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd]) ++
        List.replicate 2 Branch.even) := by
    simpa [hsplit] using h
  have hp := cycle_trailing_evens_lt (r := 2) (by decide) hC
  set z := image n (List.replicate a Branch.odd)
  set y := image n (List.replicate a Branch.odd ++ [Branch.even])
  have hyeq : y = floorPower z := by
    simp [y, z, image_append, image]
  have hf : follows z
      [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEOOEE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hzlt : z < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq.symm).2
  have hyO : follows y (List.replicate 2 Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.even])
      (by simpa [y, hyeq, image, List.replicate] using hf.2)
  have hy1 : 1 ≤ y := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [y, hyeq] using floorPower_pos hz1
  have hpow := odd_run_lower_growth (n := y) (a := 2) hy1 hyO
  have hpimg :
      image n (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd]) =
        image y (List.replicate 2 Branch.odd) := by
    simp [y, image_append, image]
  have hle' : y ^ 9 ≤ 1024 * image y (List.replicate 2 Branch.odd) ^ 4 := by
    simpa [denomBits_two, three_pow_two, two_pow_ten] using hpow
  have hp' : image y (List.replicate 2 Branch.odd) < (n + 1) ^ 4 := by
    rwa [← hpimg]
  have hplt : 1024 * image y (List.replicate 2 Branch.odd) ^ 4 <
      1024 * (n + 1) ^ 16 := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 4) hp' (by decide)
    exact Nat.mul_lt_mul_of_pos_left this
      (by decide : (0 : ℕ) < 1024)
  have hy9 : y ^ 9 < (n + 1) ^ 18 :=
    lt_of_le_of_lt hle' (hplt.trans (two_pow10_succ_pow16_lt_succ_pow18 hn))
  have h18 : (n + 1) ^ 18 = ((n + 1) ^ 2) ^ 9 := by
    rw [← Nat.pow_mul]
  have hylt : y < (n + 1) ^ 2 :=
    (Nat.pow_lt_pow_iff_left (by decide : (9 : ℕ) ≠ 0)).mp (h18 ▸ hy9)
  have hys : y + 1 ≤ (n + 1) ^ 2 := Nat.succ_le_of_lt hylt
  have : (y + 1) ^ 2 ≤ ((n + 1) ^ 2) ^ 2 := Nat.pow_le_pow_left hys 2
  have hexp : ((n + 1) ^ 2) ^ 2 = (n + 1) ^ 4 := by rw [← Nat.pow_mul]
  exact lt_of_lt_of_le hzlt (hexp ▸ this)

theorem no_cycle_word_three_even_eooee_of_ge {n a : ℕ}
    (hn : 256 ≤ n) (ha : 4 ≤ a) (h : CycleWord n (threeEvenEOOEE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hn32 : 32 ≤ n := le_trans (by decide : (32 : ℕ) ≤ 256) hn
  have hz := threeEvenEOOEE_z_lt hn32 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even])
      (by simpa [threeEvenEOOEE] using h.1)
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

theorem threeEvenEOOEE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEOOEE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even])
      (by simpa [threeEvenEOOEE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eooee_of_lt {n a : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha4 : 4 ≤ a) (ha6 : a ≤ 6)
    (h : CycleWord n (threeEvenEOOEE a)) : False := by
  have hA : a - 4 < 3 := by omega
  have hfalse :
      cycleWordB n (threeEvenEOOEE (a - 4 + 4)) = false :=
    cycleWordB_eooee_prefix_lt256 ⟨n, hn⟩ ⟨a - 4, hA⟩ hn2
  have ha : a - 4 + 4 = a := by omega
  have hfalse' : cycleWordB n (threeEvenEOOEE a) = false := by
    simpa [ha] using hfalse
  have htrue : cycleWordB n (threeEvenEOOEE a) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eooee {n a : ℕ} (hn : 2 ≤ n) (ha : 4 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even]) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt =>
      have hcases : a ≤ 6 ∨ 7 ≤ a := by omega
      rcases hcases with hle | hge
      · exact no_cycle_word_three_even_eooee_of_lt hn hlt ha hle h
      · exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEOOEE_follows_seven_odds hge h)
  | inr hge => exact no_cycle_word_three_even_eooee_of_ge hge ha h

end Problems.Juggler
