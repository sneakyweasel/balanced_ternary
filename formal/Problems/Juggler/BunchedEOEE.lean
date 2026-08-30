import Problems.Juggler.BunchedEEE
import Problems.Juggler.BunchedEOEEEval

namespace Problems.Juggler

set_option exponentiation.threshold 2048
set_option maxRecDepth 2048
set_option maxHeartbeats 800000

/-!
# Uniform bunched leftovers `O^a EOEE`

`OOOOOEOEE` is the first expanding instance. The mixed cell is
`z < (n+1)^6` for `n ≥ 4`: two trailing evens give `p < (n+1)^4`,
the one-odd lower envelope gives `y^3 ≤ 4 p^2`, and `n ≥ 4`
upgrades that to `y < (n+1)^3`, hence `z < (y+1)^2 ≤ (n+1)^6`.

The comparison is

`n^{3^a} > 2^{e_a} (n+1)^{6 · 2^a}`

with `e_a = denomBits a`. Large `n` at `a = 5` is `n ≥ 314`,
cubed in `a`. At `a = 6` the same cell already fires at `n ≥ 16`.
Below those cutoffs, `a = 5` and `a = 6` are tables and `a ≥ 7`
is seven consecutive odds.

This excludes that one bunched family only. It is not the other
five bunched tails, not a length-8 or length-9 census, and not a
halt theorem. Paper A is not edited.
-/

def threeEvenEOEE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.even, Branch.even]

theorem denomBits_one : denomBits 1 = 2 := by
  decide

theorem denomBits_five : denomBits 5 = 422 := by
  native_decide

theorem three_pow_five : (3 : ℕ) ^ 5 = 243 := by
  decide

theorem six_mul_two_pow_five : 6 * 2 ^ 5 = 192 := by
  decide

theorem six_mul_two_pow_six : 6 * 2 ^ 6 = 384 := by
  decide

theorem threeEvenEOEE_of_five : threeEvenEOEE 5 = wordOOOOOEOEE :=
  rfl

theorem threeEvenEOEE_of_six : threeEvenEOEE 6 = wordOOOOOOEOEE :=
  rfl

theorem succ_sq_gt_mul_add_two {n : ℕ} (_hn : 1 ≤ n) :
    n * (n + 2) < (n + 1) ^ 2 := by
  have : n * (n + 2) + 1 = (n + 1) ^ 2 := by ring
  omega

theorem persist_succ_pow {n p q : ℕ} (hn : 1 ≤ n) (hq : 1 ≤ q)
    (hpq : q ≤ p) :
    n ^ p * (n + 2) ^ q < (n + 1) ^ (p + q) := by
  have hsq : n * (n + 2) < (n + 1) ^ 2 := succ_sq_gt_mul_add_two hn
  have hq0 : q ≠ 0 := Nat.pos_iff_ne_zero.mp hq
  have hpair : (n * (n + 2)) ^ q < ((n + 1) ^ 2) ^ q :=
    Nat.pow_lt_pow_left hsq hq0
  have hcore : n ^ q * (n + 2) ^ q < (n + 1) ^ (2 * q) := by
    rwa [mul_pow, ← Nat.pow_mul] at hpair
  have hrest : n ^ (p - q) ≤ (n + 1) ^ (p - q) :=
    Nat.pow_le_pow_left (Nat.le_succ n) _
  have hmid : n ^ (p - q) * (n ^ q * (n + 2) ^ q) <
      (n + 1) ^ (p - q) * (n + 1) ^ (2 * q) :=
    lt_of_le_of_lt (Nat.mul_le_mul_right _ hrest)
      (Nat.mul_lt_mul_of_pos_left hcore (pow_pos (Nat.succ_pos n) _))
  have hL : n ^ (p - q) * (n ^ q * (n + 2) ^ q) =
      n ^ p * (n + 2) ^ q := by
    rw [← mul_assoc, ← Nat.pow_add, Nat.sub_add_cancel hpq]
  have hR : (n + 1) ^ (p - q) * (n + 1) ^ (2 * q) =
      (n + 1) ^ (p + q) := by
    rw [← Nat.pow_add]
    congr 1
    omega
  rwa [hL, hR] at hmid

theorem eoee_tail_five_succ {n : ℕ} (hn : 1 ≤ n)
    (ih : 2 ^ 422 * (n + 1) ^ 192 < n ^ 243) :
    2 ^ 422 * (n + 2) ^ 192 < (n + 1) ^ 243 := by
  have hpq := persist_succ_pow (p := 243) (q := 192) hn
    (by decide) (by decide)
  have hpos2 : 0 < 2 ^ 422 := pow_pos (by decide : (0 : ℕ) < 2) _
  have hposn : 0 < n ^ 243 :=
    pow_pos (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) hn) _
  have hmid : (2 ^ 422 * (n + 2) ^ 192) * n ^ 243 <
      (n + 1) ^ 243 * n ^ 243 :=
    calc
      (2 ^ 422 * (n + 2) ^ 192) * n ^ 243 =
          2 ^ 422 * ((n + 2) ^ 192 * n ^ 243) := by
        rw [mul_assoc]
      _ = 2 ^ 422 * (n ^ 243 * (n + 2) ^ 192) := by
        rw [mul_comm ((n + 2) ^ 192)]
      _ < 2 ^ 422 * (n + 1) ^ (243 + 192) :=
        Nat.mul_lt_mul_of_pos_left hpq hpos2
      _ = 2 ^ 422 * ((n + 1) ^ 243 * (n + 1) ^ 192) := by
        rw [Nat.pow_add]
      _ = 2 ^ 422 * ((n + 1) ^ 192 * (n + 1) ^ 243) := by
        rw [mul_comm ((n + 1) ^ 243)]
      _ = (2 ^ 422 * (n + 1) ^ 192) * (n + 1) ^ 243 := by
        rw [mul_assoc]
      _ < n ^ 243 * (n + 1) ^ 243 :=
        Nat.mul_lt_mul_of_pos_right ih (pow_pos (Nat.succ_pos n) _)
      _ = (n + 1) ^ 243 * n ^ 243 := mul_comm _ _
  exact (Nat.mul_lt_mul_right hposn).mp hmid

theorem eoee_tail_six_succ {n : ℕ} (hn : 1 ≤ n)
    (ih : 2 ^ 1330 * (n + 1) ^ 384 < n ^ 729) :
    2 ^ 1330 * (n + 2) ^ 384 < (n + 1) ^ 729 := by
  have hpq := persist_succ_pow (p := 729) (q := 384) hn
    (by decide) (by decide)
  have hpos2 : 0 < 2 ^ 1330 := pow_pos (by decide : (0 : ℕ) < 2) _
  have hposn : 0 < n ^ 729 :=
    pow_pos (lt_of_lt_of_le (by decide : (0 : ℕ) < 1) hn) _
  have hmid : (2 ^ 1330 * (n + 2) ^ 384) * n ^ 729 <
      (n + 1) ^ 729 * n ^ 729 :=
    calc
      (2 ^ 1330 * (n + 2) ^ 384) * n ^ 729 =
          2 ^ 1330 * ((n + 2) ^ 384 * n ^ 729) := by
        rw [mul_assoc]
      _ = 2 ^ 1330 * (n ^ 729 * (n + 2) ^ 384) := by
        rw [mul_comm ((n + 2) ^ 384)]
      _ < 2 ^ 1330 * (n + 1) ^ (729 + 384) :=
        Nat.mul_lt_mul_of_pos_left hpq hpos2
      _ = 2 ^ 1330 * ((n + 1) ^ 729 * (n + 1) ^ 384) := by
        rw [Nat.pow_add]
      _ = 2 ^ 1330 * ((n + 1) ^ 384 * (n + 1) ^ 729) := by
        rw [mul_comm ((n + 1) ^ 729)]
      _ = (2 ^ 1330 * (n + 1) ^ 384) * (n + 1) ^ 729 := by
        rw [mul_assoc]
      _ < n ^ 729 * (n + 1) ^ 729 :=
        Nat.mul_lt_mul_of_pos_right ih (pow_pos (Nat.succ_pos n) _)
      _ = (n + 1) ^ 729 * n ^ 729 := mul_comm _ _
  exact (Nat.mul_lt_mul_right hposn).mp hmid

theorem eoee_tail_five_at {n : ℕ} (hn : 314 ≤ n) :
    2 ^ 422 * (n + 1) ^ 192 < n ^ 243 := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le hn
  subst ht
  clear hn
  induction t with
  | zero => exact pow314_243_gt_two_pow422_succ_pow192
  | succ t ih =>
      have h1 : 1 ≤ 314 + t := by omega
      exact eoee_tail_five_succ h1 ih

theorem eoee_tail_six_at {n : ℕ} (hn : 16 ≤ n) :
    2 ^ 1330 * (n + 1) ^ 384 < n ^ 729 := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le hn
  subst ht
  clear hn
  induction t with
  | zero => exact pow16_729_gt_two_pow1330_succ_pow384
  | succ t ih =>
      have h1 : 1 ≤ 16 + t := by omega
      exact eoee_tail_six_succ h1 ih

theorem three_even_eoee_tail_succ {n a : ℕ} (hn : 1 ≤ n)
    (ih : 2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a) < n ^ (3 ^ a)) :
    2 ^ denomBits (a + 1) * (n + 1) ^ (6 * 2 ^ (a + 1)) <
      n ^ (3 ^ (a + 1)) := by
  have hcube :
      2 ^ (3 * denomBits a) * (n + 1) ^ (3 * (6 * 2 ^ a)) <
        n ^ (3 ^ (a + 1)) := by
    have hlt :
        (2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a)) ^ 3 <
          (n ^ (3 ^ a)) ^ 3 :=
      Nat.pow_lt_pow_left ih (by decide : (3 : ℕ) ≠ 0)
    have hL : (2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a)) ^ 3 =
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * (6 * 2 ^ a)) :=
      two_mul_pow_cube _ _ _
    have hR : (n ^ (3 ^ a)) ^ 3 = n ^ (3 ^ (a + 1)) := by
      rw [← Nat.pow_mul, ← Nat.pow_succ]
    rwa [hL, hR] at hlt
  have hsucc6 : 4 < (n + 1) ^ 6 := by
    have h64 : (64 : ℕ) ≤ (n + 1) ^ 6 := by
      have : 2 ≤ n + 1 := by omega
      simpa using Nat.pow_le_pow_left this 6
    exact lt_of_lt_of_le (by decide : (4 : ℕ) < 64) h64
  have hpow4 : 2 ^ (2 ^ (a + 1)) < (n + 1) ^ (6 * 2 ^ a) := by
    have hm : 2 ^ a ≠ 0 :=
      Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
    have : 4 ^ (2 ^ a) < ((n + 1) ^ 6) ^ (2 ^ a) :=
      Nat.pow_lt_pow_left hsucc6 hm
    have h4 : (4 : ℕ) ^ (2 ^ a) = 2 ^ (2 ^ (a + 1)) := by
      have : (4 : ℕ) = 2 ^ 2 := rfl
      rw [this, ← Nat.pow_mul, Nat.mul_comm, ← Nat.pow_succ]
    rwa [h4, ← Nat.pow_mul] at this
  have he' : denomBits (a + 1) = 3 * denomBits a + 2 ^ (a + 1) :=
    denomBits_succ a
  have hfactor :
      2 ^ denomBits (a + 1) * (n + 1) ^ (6 * 2 ^ (a + 1)) <
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * (6 * 2 ^ a)) := by
    have hexp : 3 * (6 * 2 ^ a) = 6 * 2 ^ a + 6 * 2 ^ (a + 1) := by
      have : 6 * 2 ^ (a + 1) = 12 * 2 ^ a := by
        rw [pow_succ]
        ring
      rw [this]
      ring
    have hL :
        2 ^ denomBits (a + 1) * (n + 1) ^ (6 * 2 ^ (a + 1)) =
          2 ^ (3 * denomBits a) *
            (2 ^ (2 ^ (a + 1)) * (n + 1) ^ (6 * 2 ^ (a + 1))) := by
      rw [he', Nat.pow_add, mul_assoc]
    have hR :
        2 ^ (3 * denomBits a) * (n + 1) ^ (3 * (6 * 2 ^ a)) =
          2 ^ (3 * denomBits a) *
            ((n + 1) ^ (6 * 2 ^ a) * (n + 1) ^ (6 * 2 ^ (a + 1))) := by
      congr 1
      rw [hexp, Nat.pow_add]
    have hpos2 : 0 < 2 ^ (3 * denomBits a) :=
      pow_pos (by decide : (0 : ℕ) < 2) _
    have hposn : 0 < (n + 1) ^ (6 * 2 ^ (a + 1)) :=
      pow_pos (Nat.succ_pos n) _
    rw [hL, hR]
    exact Nat.mul_lt_mul_of_pos_left
      (Nat.mul_lt_mul_of_pos_right hpow4 hposn) hpos2
  exact hfactor.trans hcube

theorem three_even_eoee_tail_of_five {n a : ℕ} (hn : 314 ≤ n)
    (ha : 5 ≤ a) :
    2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a) < n ^ (3 ^ a) := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le ha
  subst ht
  clear ha
  induction t with
  | zero =>
      rw [denomBits_five, three_pow_five, six_mul_two_pow_five]
      exact eoee_tail_five_at hn
  | succ t ih =>
      exact three_even_eoee_tail_succ
        (le_trans (by decide : (1 : ℕ) ≤ 314) hn) ih

theorem three_even_eoee_tail_of_six {n a : ℕ} (hn : 16 ≤ n)
    (ha : 6 ≤ a) :
    2 ^ denomBits a * (n + 1) ^ (6 * 2 ^ a) < n ^ (3 ^ a) := by
  obtain ⟨t, ht⟩ := Nat.exists_eq_add_of_le ha
  subst ht
  clear ha
  induction t with
  | zero =>
      rw [denomBits_six, three_pow_six, six_mul_two_pow_six]
      exact eoee_tail_six_at hn
  | succ t ih =>
      exact three_even_eoee_tail_succ
        (le_trans (by decide : (1 : ℕ) ≤ 16) hn) ih

theorem four_mul_succ_pow8_lt_succ_pow9 {n : ℕ} (hn : 4 ≤ n) :
    4 * (n + 1) ^ 8 < (n + 1) ^ 9 := by
  have : (4 : ℕ) < n + 1 := by omega
  have hpos : 0 < (n + 1) ^ 8 := pow_pos (Nat.succ_pos n) 8
  have hr : (n + 1) ^ 9 = (n + 1) * (n + 1) ^ 8 :=
    (pow_succ (n + 1) 8).trans (mul_comm _ _)
  rw [hr]
  exact Nat.mul_lt_mul_of_pos_right this hpos

theorem threeEvenEOEE_z_lt {n a : ℕ} (hn : 4 ≤ n)
    (h : CycleWord n (threeEvenEOEE a)) :
    image n (List.replicate a Branch.odd) < (n + 1) ^ 6 := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 4) hn
  have hsplit : threeEvenEOEE a =
      (List.replicate a Branch.odd ++ [Branch.even, Branch.odd]) ++
        List.replicate 2 Branch.even := by
    simp [threeEvenEOEE]
  have hC : CycleWord n
      ((List.replicate a Branch.odd ++ [Branch.even, Branch.odd]) ++
        List.replicate 2 Branch.even) := by
    simpa [hsplit] using h
  have hp := cycle_trailing_evens_lt (r := 2) (by decide) hC
  set z := image n (List.replicate a Branch.odd)
  set y := image n (List.replicate a Branch.odd ++ [Branch.even])
  have hyeq : y = floorPower z := by
    simp [y, z, image_append, image]
  have hf : follows z
      [Branch.even, Branch.odd, Branch.even, Branch.even] :=
    follows_of_append_right (u := List.replicate a Branch.odd)
      (by simpa [threeEvenEOEE] using h.1)
  have he : z % 2 = 0 := hf.1
  have hzlt : z < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq.symm).2
  have hyO : follows y [Branch.odd] :=
    follows_of_append_left (v := [Branch.even, Branch.even])
      (by simpa [y, hyeq, image] using hf.2)
  have hy1 : 1 ≤ y := by
    have hz1 : 1 ≤ z := image_pos hn1 _
    simpa [y, hyeq] using floorPower_pos hz1
  have hpow := odd_run_lower_growth (n := y) (a := 1) hy1 hyO
  have hpimg :
      image n (List.replicate a Branch.odd ++ [Branch.even, Branch.odd]) =
        floorPower y := by
    simp [y, image_append, image]
  have hle' : y ^ 3 ≤ 4 * floorPower y ^ 2 := by
    simpa [denomBits_one] using hpow
  have hp' : floorPower y < (n + 1) ^ 4 := by
    rwa [hpimg] at hp
  have hplt : 4 * floorPower y ^ 2 < 4 * (n + 1) ^ 8 := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 2) hp' (by decide)
    exact Nat.mul_lt_mul_of_pos_left this (by decide : (0 : ℕ) < 4)
  have hy3 : y ^ 3 < (n + 1) ^ 9 :=
    lt_of_le_of_lt hle' (hplt.trans (four_mul_succ_pow8_lt_succ_pow9 hn))
  have h9 : (n + 1) ^ 9 = ((n + 1) ^ 3) ^ 3 := by
    rw [← Nat.pow_mul]
  have hylt : y < (n + 1) ^ 3 :=
    (Nat.pow_lt_pow_iff_left (by decide : (3 : ℕ) ≠ 0)).mp (h9 ▸ hy3)
  have hys : y + 1 ≤ (n + 1) ^ 3 := Nat.succ_le_of_lt hylt
  have hz6 : z < (n + 1) ^ 6 := by
    have : (y + 1) ^ 2 ≤ ((n + 1) ^ 3) ^ 2 := Nat.pow_le_pow_left hys 2
    have hexp : ((n + 1) ^ 3) ^ 2 = (n + 1) ^ 6 := by rw [← Nat.pow_mul]
    exact lt_of_lt_of_le hzlt (hexp ▸ this)
  exact hz6

theorem no_cycle_word_three_even_eoee_of_ge_five {n a : ℕ}
    (hn : 314 ≤ n) (ha : 5 ≤ a) (h : CycleWord n (threeEvenEOEE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 314) hn
  have hn4 : 4 ≤ n := le_trans (by decide : (4 : ℕ) ≤ 314) hn
  have hz := threeEvenEOEE_z_lt hn4 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even, Branch.even])
      (by simpa [threeEvenEOEE] using h.1)
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

theorem no_cycle_word_three_even_eoee_of_ge_six {n a : ℕ}
    (hn : 16 ≤ n) (ha : 6 ≤ a) (h : CycleWord n (threeEvenEOEE a)) :
    False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 16) hn
  have hn4 : 4 ≤ n := le_trans (by decide : (4 : ℕ) ≤ 16) hn
  have hz := threeEvenEOEE_z_lt hn4 h
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even, Branch.even])
      (by simpa [threeEvenEOEE] using h.1)
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

theorem threeEvenEOEE_follows_seven_odds {n a : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (threeEvenEOEE a)) :
    follows n sevenOdds := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even, Branch.even])
      (by simpa [threeEvenEOEE] using h.1)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_three_even_eoee_of_lt_five {n : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 314) (h : CycleWord n (threeEvenEOEE 5)) :
    False := by
  have hfalse : cycleWordB n wordOOOOOEOEE = false :=
    cycleWordB_ooooo_eoee_lt314 ⟨n, hn⟩ hn2
  have htrue : cycleWordB n wordOOOOOEOEE = true :=
    cycleWordB_iff.mpr (by simpa [threeEvenEOEE_of_five] using h)
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eoee_of_lt_six {n : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 16) (h : CycleWord n (threeEvenEOEE 6)) :
    False := by
  have hfalse : cycleWordB n wordOOOOOOEOEE = false :=
    cycleWordB_oooooo_eoee_lt16 ⟨n, hn⟩ hn2
  have htrue : cycleWordB n wordOOOOOOEOEE = true :=
    cycleWordB_iff.mpr (by simpa [threeEvenEOEE_of_six] using h)
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_three_even_eoee {n a : ℕ} (hn : 2 ≤ n) (ha : 5 ≤ a) :
    ¬CycleWord n
      (List.replicate a Branch.odd ++
        [Branch.even, Branch.odd, Branch.even, Branch.even]) := by
  intro h
  have hcases : a = 5 ∨ a = 6 ∨ 7 ≤ a := by omega
  rcases hcases with h5 | hrest
  · subst h5
    cases lt_or_ge n 314 with
    | inl hlt => exact no_cycle_word_three_even_eoee_of_lt_five hn hlt h
    | inr hge => exact no_cycle_word_three_even_eoee_of_ge_five hge (by decide) h
  rcases hrest with h6 | hge
  · subst h6
    cases lt_or_ge n 16 with
    | inl hlt => exact no_cycle_word_three_even_eoee_of_lt_six hn hlt h
    | inr hge => exact no_cycle_word_three_even_eoee_of_ge_six hge (by decide) h
  · cases lt_or_ge n 256 with
    | inl hlt =>
        exact no_follows_seven_odds_of_lt256 hn hlt
          (threeEvenEOEE_follows_seven_odds hge h)
    | inr hge' =>
        exact no_cycle_word_three_even_eoee_of_ge_six
          (le_trans (by decide : (16 : ℕ) ≤ 256) hge')
          (le_trans (by decide : (6 : ℕ) ≤ 7) hge) h

end Problems.Juggler
