import Problems.Juggler.LeftoverCycles

namespace Problems.Juggler

/-!
# Uniform two-even leftover families

`O^{k-2}EE` and `O^{k-3}EOE` are the leftover even-terminating
two-even words at every expanding length `k ≥ 6`. They share the
tail `n^{3^{k-2}} > 2^{e_{k-2}} (n+1)^{2^k}` with
`e_a = 2 (3^a - 2^a) = log2(lowerDenom(O^a))`.

Large `n` is the length-6 comparison at `n ≥ 256`, cubed in `k`.
Below `256` the longest odd run on `n ≥ 2` has length 6, so only
`k = 8` (EE) and `k = 8,9` (EOE) need tables; longer words require
seven consecutive odds.

This is not a length-8 census, not a three-even programme, and not
a halt theorem. Paper A records the families as Theorem 3.12.
-/

def denomBits (a : ℕ) : ℕ :=
  2 * (3 ^ a - 2 ^ a)

def twoEvenEE (k : ℕ) : List Branch :=
  List.replicate (k - 2) Branch.odd ++ List.replicate 2 Branch.even

def twoEvenEOE (k : ℕ) : List Branch :=
  List.replicate (k - 3) Branch.odd ++
    [Branch.even, Branch.odd, Branch.even]

theorem two_pow_le_three_pow (a : ℕ) : 2 ^ a ≤ 3 ^ a :=
  Nat.pow_le_pow_left (by decide : (2 : ℕ) ≤ 3) a

theorem nat_cast_eq_of_int {a b : ℕ} (h : (a : ℤ) = (b : ℤ)) : a = b :=
  Nat.cast_injective h

theorem denomBits_succ (a : ℕ) :
    denomBits (a + 1) = 3 * denomBits a + 2 ^ (a + 1) := by
  have ha : 2 ^ a ≤ 3 ^ a := two_pow_le_three_pow a
  have ha1 : 2 ^ (a + 1) ≤ 3 ^ (a + 1) := two_pow_le_three_pow (a + 1)
  apply nat_cast_eq_of_int
  simp only [denomBits, Nat.cast_add, Nat.cast_mul, Nat.cast_pow,
    Nat.cast_ofNat, Nat.cast_sub ha, Nat.cast_sub ha1]
  ring

theorem four_exp_odd_succ (k a : ℕ) :
    2 ^ k * 3 ^ a + 2 ^ (k + 1) * (3 ^ a - 2 ^ a) =
      2 ^ k * (3 ^ (a + 1) - 2 ^ (a + 1)) := by
  have ha : 2 ^ a ≤ 3 ^ a := two_pow_le_three_pow a
  have ha1 : 2 ^ (a + 1) ≤ 3 ^ (a + 1) := two_pow_le_three_pow (a + 1)
  apply nat_cast_eq_of_int
  simp only [Nat.cast_add, Nat.cast_mul, Nat.cast_pow, Nat.cast_ofNat,
    Nat.cast_sub ha, Nat.cast_sub ha1]
  ring

theorem four_mul_two_pow_sub {k : ℕ} (hk : 2 ≤ k) :
    4 * 2 ^ (k - 2) = 2 ^ k := by
  have h4 : (4 : ℕ) = 2 ^ 2 := rfl
  rw [h4, ← Nat.pow_add, Nat.add_sub_of_le hk]

theorem two_mul_two_pow (t : ℕ) : 2 * 2 ^ t = 2 ^ (t + 1) := by
  rw [pow_succ, mul_comm]

theorem two_mul_two_pow_pred {k : ℕ} (hk : 1 ≤ k) :
    2 * 2 ^ (k - 1) = 2 ^ k := by
  rw [two_mul_two_pow]
  congr 1
  omega

theorem two_mul_pow_cube (e y m : ℕ) :
    (2 ^ e * y ^ m) ^ 3 = 2 ^ (3 * e) * y ^ (3 * m) := by
  rw [mul_pow, two_pow_mul, ← Nat.pow_mul, Nat.mul_comm e 3, Nat.mul_comm m 3]

theorem three_mul_two_pow (k : ℕ) :
    3 * 2 ^ k = 2 ^ k + 2 ^ (k + 1) := by
  rw [pow_succ]
  ring

theorem three_pow_succ_sub {k : ℕ} (hk : 3 ≤ k) :
    3 ^ (k - 3) * 3 = 3 ^ (k - 2) := by
  rw [← Nat.pow_succ]
  congr 1
  omega

theorem three_pow_succ_sub_two {k : ℕ} (hk : 2 ≤ k) :
    3 ^ (k - 2) * 3 = 3 ^ (k - 1) := by
  rw [← Nat.pow_succ]
  congr 1
  omega

theorem lowerDenomFrom_replicate_odd (k o D a : ℕ) :
    lowerDenomFrom k o D (List.replicate a Branch.odd) =
      D ^ (3 ^ a) * 4 ^ (2 ^ k * (3 ^ a - 2 ^ a)) := by
  induction a generalizing k o D with
  | zero =>
      rw [List.replicate_zero, lowerDenomFrom_nil]
      simp
  | succ a ih =>
      rw [List.replicate_succ, lowerDenomFrom_odd_cons, ih]
      have hD : (D ^ 3 * 4 ^ (2 ^ k)) ^ (3 ^ a) =
          D ^ (3 ^ (a + 1)) * 4 ^ (2 ^ k * 3 ^ a) := by
        rw [mul_pow, ← Nat.pow_mul, Nat.pow_mul 4 (2 ^ k) (3 ^ a)]
        congr 2
        rw [Nat.mul_comm, ← Nat.pow_succ]
      rw [hD, mul_assoc, ← Nat.pow_add, four_exp_odd_succ]

theorem lowerDenom_replicate_odd (a : ℕ) :
    lowerDenom (List.replicate a Branch.odd) = 2 ^ denomBits a := by
  rw [lowerDenom, lowerDenomFrom_replicate_odd, one_pow, pow_zero, one_mul]
  rw [four_eq_two_pow, ← Nat.pow_mul]
  unfold denomBits
  congr 1
  ring

theorem odd_run_lower_growth {n a : ℕ} (hn : 1 ≤ n)
    (hw : follows n (List.replicate a Branch.odd)) :
    n ^ (3 ^ a) ≤
      2 ^ denomBits a * image n (List.replicate a Branch.odd) ^ (2 ^ a) := by
  have hL := lower_growth_word hn hw
  simpa [LowerPowerBound, oddCount_replicate_odd, List.length_replicate,
    lowerDenom_replicate_odd] using hL

theorem denomBits_four : denomBits 4 = 130 := by
  native_decide

theorem three_pow_four : (3 : ℕ) ^ 4 = 81 := by
  decide

theorem two_pow_six : (2 : ℕ) ^ 6 = 64 := by
  decide

theorem shared_two_even_tail_succ {n k : ℕ} (hn : 256 ≤ n) (hk : 6 ≤ k)
    (ih : 2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k) < n ^ (3 ^ (k - 2))) :
    2 ^ denomBits (k - 1) * (n + 1) ^ (2 ^ (k + 1)) < n ^ (3 ^ (k - 1)) := by
  have hk1 : 1 ≤ k := le_trans (by decide : (1 : ℕ) ≤ 6) hk
  have hk2 : 2 ≤ k := le_trans (by decide : (2 : ℕ) ≤ 6) hk
  have hcube :
      2 ^ (3 * denomBits (k - 2)) * (n + 1) ^ (3 * 2 ^ k) <
        n ^ (3 ^ (k - 1)) := by
    have hlt :
        (2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k)) ^ 3 <
          (n ^ (3 ^ (k - 2))) ^ 3 :=
      Nat.pow_lt_pow_left ih (by decide : (3 : ℕ) ≠ 0)
    have hL : (2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k)) ^ 3 =
        2 ^ (3 * denomBits (k - 2)) * (n + 1) ^ (3 * 2 ^ k) :=
      two_mul_pow_cube _ _ _
    have hR : (n ^ (3 ^ (k - 2))) ^ 3 = n ^ (3 ^ (k - 1)) := by
      rw [← Nat.pow_mul, three_pow_succ_sub_two hk2]
    rwa [hL, hR] at hlt
  have hsucc2 : 2 < (n + 1) ^ 2 := by
    have h4 : (4 : ℕ) ≤ (n + 1) ^ 2 := by
      have : 2 ≤ n + 1 := by omega
      simpa using Nat.pow_le_pow_left this 2
    exact lt_of_lt_of_le (by decide : (2 : ℕ) < 4) h4
  have hpow2 : 2 ^ (2 ^ (k - 1)) < (n + 1) ^ (2 ^ k) := by
    have hm : 2 ^ (k - 1) ≠ 0 :=
      Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
    have : 2 ^ (2 ^ (k - 1)) < ((n + 1) ^ 2) ^ (2 ^ (k - 1)) :=
      Nat.pow_lt_pow_left hsucc2 hm
    rwa [← Nat.pow_mul, two_mul_two_pow_pred hk1] at this
  have he' : denomBits (k - 1) = 3 * denomBits (k - 2) + 2 ^ (k - 1) := by
    have hsub : k - 1 = (k - 2) + 1 := by omega
    rw [hsub, denomBits_succ]
  have hfactor :
      2 ^ denomBits (k - 1) * (n + 1) ^ (2 ^ (k + 1)) <
        2 ^ (3 * denomBits (k - 2)) * (n + 1) ^ (3 * 2 ^ k) := by
    have hL :
        2 ^ denomBits (k - 1) * (n + 1) ^ (2 ^ (k + 1)) =
          2 ^ (3 * denomBits (k - 2)) *
            (2 ^ (2 ^ (k - 1)) * (n + 1) ^ (2 ^ (k + 1))) := by
      rw [he', Nat.pow_add, mul_assoc]
    have hR :
        2 ^ (3 * denomBits (k - 2)) * (n + 1) ^ (3 * 2 ^ k) =
          2 ^ (3 * denomBits (k - 2)) *
            ((n + 1) ^ (2 ^ k) * (n + 1) ^ (2 ^ (k + 1))) := by
      congr 1
      rw [← Nat.pow_add, three_mul_two_pow]
    have hpos2 : 0 < 2 ^ (3 * denomBits (k - 2)) :=
      pow_pos (by decide : (0 : ℕ) < 2) _
    have hposn : 0 < (n + 1) ^ (2 ^ (k + 1)) :=
      pow_pos (Nat.succ_pos n) _
    rw [hL, hR]
    exact Nat.mul_lt_mul_of_pos_left
      (Nat.mul_lt_mul_of_pos_right hpow2 hposn) hpos2
  exact hfactor.trans hcube

theorem shared_two_even_tail {n k : ℕ} (hn : 256 ≤ n) (hk : 6 ≤ k) :
    2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k) < n ^ (3 ^ (k - 2)) := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le hk
  subst ht
  clear hk
  induction t with
  | zero =>
      simpa [denomBits_four, three_pow_four, two_pow_six] using
        pow81_gt_two_pow130_succ_pow64 hn
  | succ t ih =>
      have h :=
        shared_two_even_tail_succ (k := 6 + t) hn (Nat.le_add_right 6 t) ih
      have h1 : 6 + t - 1 = 6 + (t + 1) - 2 := by omega
      have h2 : 6 + t + 1 = 6 + (t + 1) := by omega
      simpa [h1, h2] using h

theorem twoEvenEE_of_six : twoEvenEE 6 = wordOOOOEE :=
  rfl

theorem twoEvenEE_of_seven : twoEvenEE 7 = wordOOOOOEE :=
  rfl

theorem twoEvenEE_of_eight : twoEvenEE 8 = wordTwoEvenEE8 :=
  rfl

theorem twoEvenEOE_of_six : twoEvenEOE 6 = wordOOOEOE :=
  rfl

theorem twoEvenEOE_of_seven : twoEvenEOE 7 = wordOOOOEOE :=
  rfl

theorem twoEvenEOE_of_eight : twoEvenEOE 8 = wordTwoEvenEOE8 :=
  rfl

theorem twoEvenEOE_of_nine : twoEvenEOE 9 = wordTwoEvenEOE9 :=
  rfl

theorem no_cycle_word_two_even_ee_of_ge {n k : ℕ}
    (hn : 256 ≤ n) (hk : 6 ≤ k) (h : CycleWord n (twoEvenEE k)) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hk2 : 2 ≤ k := le_trans (by decide : (2 : ℕ) ≤ 6) hk
  have hz := cycle_trailing_evens_lt (r := 2) (by decide) h
  have hO : follows n (List.replicate (k - 2) Branch.odd) :=
    follows_of_append_left (v := List.replicate 2 Branch.even) h.1
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ (k - 2) ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image n (List.replicate (k - 2) Branch.odd) ^ (2 ^ (k - 2)) <
        (n + 1) ^ (2 ^ k) := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 2 ^ (k - 2)) hz hm
    rwa [four_mul_two_pow_sub hk2] at this
  have hlt : n ^ (3 ^ (k - 2)) <
      2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  exact (not_lt_of_gt (shared_two_even_tail hn hk)) hlt

theorem cycle_eoe_suffix_y_cube_lt {n : ℕ} {u : List Branch}
    (h : CycleWord n (u ++ [Branch.even, Branch.odd, Branch.even])) :
    image n (u ++ [Branch.even]) ^ 3 < (n + 1) ^ 4 := by
  have hcell : CycleWord n
      ((u ++ [Branch.even, Branch.odd]) ++ [Branch.even]) := by
    simpa [List.append_assoc] using h
  have hI := cycle_last_even_interval hcell
  have hyO :
      follows (image n (u ++ [Branch.even])) [Branch.odd, Branch.even] :=
    follows_of_append_right (u := u ++ [Branch.even])
      (by simpa [List.append_assoc] using h.1)
  have hyodd : image n (u ++ [Branch.even]) % 2 = 1 := hyO.1
  have hz : image n (u ++ [Branch.even, Branch.odd]) =
      floorPower (image n (u ++ [Branch.even])) := by
    simp [image_append, image]
  have hcube := (floorPower_odd_eq_iff_cube_interval hyodd).mp rfl
  have hylt :
      image n (u ++ [Branch.even]) ^ 3 <
        (floorPower (image n (u ++ [Branch.even])) + 1) ^ 2 :=
    hcube.2
  have hflt :
      floorPower (image n (u ++ [Branch.even])) < (n + 1) ^ 2 := by
    simpa [hz] using hI.2
  have hsucc :
      floorPower (image n (u ++ [Branch.even])) + 1 ≤ (n + 1) ^ 2 :=
    Nat.succ_le_of_lt hflt
  have hsq :
      (floorPower (image n (u ++ [Branch.even])) + 1) ^ 2 ≤
        ((n + 1) ^ 2) ^ 2 :=
    Nat.pow_le_pow_left hsucc 2
  have hexp : ((n + 1) ^ 2) ^ 2 = (n + 1) ^ 4 :=
    (Nat.pow_mul (n + 1) 2 2).symm
  exact lt_of_lt_of_le hylt (hexp ▸ hsq)

theorem no_cycle_word_two_even_eoe_of_ge {n k : ℕ}
    (hn : 256 ≤ n) (hk : 6 ≤ k) (h : CycleWord n (twoEvenEOE k)) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hk2 : 2 ≤ k := le_trans (by decide : (2 : ℕ) ≤ 6) hk
  have hk3 : 3 ≤ k := le_trans (by decide : (3 : ℕ) ≤ 6) hk
  set u := List.replicate (k - 3) Branch.odd
  set z := image n u
  set y := image n (u ++ [Branch.even])
  have hC : CycleWord n (u ++ [Branch.even, Branch.odd, Branch.even]) := h
  have hO : follows n u :=
    follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even]) h.1
  have he : z % 2 = 0 := by
    have hf : follows z [Branch.even, Branch.odd, Branch.even] :=
      follows_of_append_right (u := u) h.1
    exact hf.1
  have hyeq : floorPower z = y := by
    simp [z, y, u, image_append, image]
  have hzlt : z < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq).2
  have hpow := odd_run_lower_growth hn1 hO
  have hm : 2 ^ (k - 3) ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow : z ^ (2 ^ (k - 3)) < (y + 1) ^ (2 ^ (k - 2)) := by
    have := pow_lt_of_lt_pow_mul (k := 2) (m := 2 ^ (k - 3)) hzlt hm
    have hexp : 2 * 2 ^ (k - 3) = 2 ^ (k - 2) := by
      rw [two_mul_two_pow]
      congr 1
      omega
    rwa [hexp] at this
  have hmid : n ^ (3 ^ (k - 3)) <
      2 ^ denomBits (k - 3) * (y + 1) ^ (2 ^ (k - 2)) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  have hcube : n ^ (3 ^ (k - 2)) <
      2 ^ (3 * denomBits (k - 3)) * (y + 1) ^ (3 * 2 ^ (k - 2)) := by
    have hlt : (n ^ (3 ^ (k - 3))) ^ 3 <
        (2 ^ denomBits (k - 3) * (y + 1) ^ (2 ^ (k - 2))) ^ 3 :=
      Nat.pow_lt_pow_left hmid (by decide : (3 : ℕ) ≠ 0)
    have hL : (n ^ (3 ^ (k - 3))) ^ 3 = n ^ (3 ^ (k - 2)) := by
      rw [← Nat.pow_mul, three_pow_succ_sub hk3]
    have hR : (2 ^ denomBits (k - 3) * (y + 1) ^ (2 ^ (k - 2))) ^ 3 =
        2 ^ (3 * denomBits (k - 3)) * (y + 1) ^ (3 * 2 ^ (k - 2)) :=
      two_mul_pow_cube _ _ _
    rwa [hL, hR] at hlt
  have hy3 := cycle_eoe_suffix_y_cube_lt (u := u) hC
  have hA : 3 ≤ n + 1 :=
    le_trans (by decide : (3 : ℕ) ≤ 257) (Nat.succ_le_succ hn)
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA (by simpa [y, u] using hy3)
  have hyraise : (y + 1) ^ (3 * 2 ^ (k - 2)) <
      2 ^ (2 ^ (k - 2)) * (n + 1) ^ (2 ^ k) := by
    have hm' : 2 ^ (k - 2) ≠ 0 :=
      Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
    have hlt : ((y + 1) ^ 3) ^ (2 ^ (k - 2)) <
        (2 * (n + 1) ^ 4) ^ (2 ^ (k - 2)) :=
      Nat.pow_lt_pow_left hysucc hm'
    have hL : ((y + 1) ^ 3) ^ (2 ^ (k - 2)) =
        (y + 1) ^ (3 * 2 ^ (k - 2)) :=
      (Nat.pow_mul (y + 1) 3 (2 ^ (k - 2))).symm
    have hR : (2 * (n + 1) ^ 4) ^ (2 ^ (k - 2)) =
        2 ^ (2 ^ (k - 2)) * (n + 1) ^ (4 * 2 ^ (k - 2)) := by
      rw [mul_pow, Nat.pow_mul]
    rw [hL, hR, four_mul_two_pow_sub hk2] at hlt
    exact hlt
  have hlt : n ^ (3 ^ (k - 2)) <
      2 ^ denomBits (k - 2) * (n + 1) ^ (2 ^ k) := by
    have hmid' : n ^ (3 ^ (k - 2)) <
        2 ^ (3 * denomBits (k - 3)) *
          (2 ^ (2 ^ (k - 2)) * (n + 1) ^ (2 ^ k)) :=
      lt_trans hcube
        (Nat.mul_lt_mul_of_pos_left hyraise
          (pow_pos (by decide : (0 : ℕ) < 2) _))
    have hexp :
        2 ^ (3 * denomBits (k - 3)) *
            (2 ^ (2 ^ (k - 2)) * (n + 1) ^ (2 ^ k)) =
          2 ^ (3 * denomBits (k - 3) + 2 ^ (k - 2)) * (n + 1) ^ (2 ^ k) := by
      rw [← mul_assoc, ← Nat.pow_add]
    have hbits : 3 * denomBits (k - 3) + 2 ^ (k - 2) = denomBits (k - 2) := by
      have : k - 2 = (k - 3) + 1 := by omega
      rw [this, denomBits_succ]
    rwa [hexp, hbits] at hmid'
  exact (not_lt_of_gt (shared_two_even_tail hn hk)) hlt

theorem no_follows_seven_odds_of_lt256 {n : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) : ¬follows n sevenOdds := by
  intro hf
  have hfalse : followsB n sevenOdds = false :=
    followsB_seven_odds_of_lt256 ⟨n, hn⟩ hn2
  have htrue : followsB n sevenOdds = true := (followsB_iff n sevenOdds).mpr hf
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem twoEvenEE_follows_seven_odds {n k : ℕ}
    (hk : 9 ≤ k) (h : CycleWord n (twoEvenEE k)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate (k - 2) Branch.odd) :=
    follows_of_append_left (v := List.replicate 2 Branch.even) h.1
  have hsplit : List.replicate (k - 2) Branch.odd =
      sevenOdds ++ List.replicate (k - 9) Branch.odd := by
    have hsum : 7 + (k - 9) = k - 2 := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  have hO' : follows n (sevenOdds ++ List.replicate (k - 9) Branch.odd) := by
    simpa [hsplit] using hO
  exact follows_of_append_left (v := List.replicate (k - 9) Branch.odd) hO'

theorem twoEvenEOE_follows_seven_odds {n k : ℕ}
    (hk : 10 ≤ k) (h : CycleWord n (twoEvenEOE k)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate (k - 3) Branch.odd) :=
    follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even]) h.1
  have hsplit : List.replicate (k - 3) Branch.odd =
      sevenOdds ++ List.replicate (k - 10) Branch.odd := by
    have hsum : 7 + (k - 10) = k - 3 := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  have hO' : follows n (sevenOdds ++ List.replicate (k - 10) Branch.odd) := by
    simpa [hsplit] using hO
  exact follows_of_append_left (v := List.replicate (k - 10) Branch.odd) hO'

theorem no_cycle_word_two_even_ee_of_lt {n k : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (hk : 6 ≤ k)
    (h : CycleWord n (twoEvenEE k)) : False := by
  have hcases : k = 6 ∨ k = 7 ∨ k = 8 ∨ 9 ≤ k := by omega
  rcases hcases with h6 | h7 | h8 | hge
  · subst h6
    exact no_cycle_word_ooooee hn2 (by simpa [twoEvenEE_of_six] using h)
  · subst h7
    exact no_cycle_word_oooooee hn2 (by simpa [twoEvenEE_of_seven] using h)
  · subst h8
    have hfalse := cycleWordB_two_even_ee8_lt256 ⟨n, hn⟩
    have htrue : cycleWordB n wordTwoEvenEE8 = true :=
      cycleWordB_iff.mpr (by simpa [twoEvenEE_of_eight] using h)
    rw [hfalse] at htrue
    exact Bool.false_ne_true htrue
  · exact no_follows_seven_odds_of_lt256 hn2 hn
      (twoEvenEE_follows_seven_odds hge h)

theorem no_cycle_word_two_even_eoe_of_lt {n k : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (hk : 6 ≤ k)
    (h : CycleWord n (twoEvenEOE k)) : False := by
  have hcases : k = 6 ∨ k = 7 ∨ k = 8 ∨ k = 9 ∨ 10 ≤ k := by omega
  rcases hcases with h6 | h7 | h8 | h9 | hge
  · subst h6
    exact no_cycle_word_oooeoe hn2 (by simpa [twoEvenEOE_of_six] using h)
  · subst h7
    exact no_cycle_word_ooooeoe hn2 (by simpa [twoEvenEOE_of_seven] using h)
  · subst h8
    have hfalse := cycleWordB_two_even_eoe8_lt256 ⟨n, hn⟩
    have htrue : cycleWordB n wordTwoEvenEOE8 = true :=
      cycleWordB_iff.mpr (by simpa [twoEvenEOE_of_eight] using h)
    rw [hfalse] at htrue
    exact Bool.false_ne_true htrue
  · subst h9
    have hfalse := cycleWordB_two_even_eoe9_lt256 ⟨n, hn⟩
    have htrue : cycleWordB n wordTwoEvenEOE9 = true :=
      cycleWordB_iff.mpr (by simpa [twoEvenEOE_of_nine] using h)
    rw [hfalse] at htrue
    exact Bool.false_ne_true htrue
  · exact no_follows_seven_odds_of_lt256 hn2 hn
      (twoEvenEOE_follows_seven_odds hge h)

theorem no_cycle_word_two_even_ee {n k : ℕ} (hn : 2 ≤ n) (hk : 6 ≤ k) :
    ¬CycleWord n
      (List.replicate (k - 2) Branch.odd ++ List.replicate 2 Branch.even) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycle_word_two_even_ee_of_lt hn hlt hk h
  | inr hge => exact no_cycle_word_two_even_ee_of_ge hge hk h

theorem no_cycle_word_two_even_eoe {n k : ℕ} (hn : 2 ≤ n) (hk : 6 ≤ k) :
    ¬CycleWord n
      (List.replicate (k - 3) Branch.odd ++
        [Branch.even, Branch.odd, Branch.even]) := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycle_word_two_even_eoe_of_lt hn hlt hk h
  | inr hge => exact no_cycle_word_two_even_eoe_of_ge hge hk h

end Problems.Juggler
