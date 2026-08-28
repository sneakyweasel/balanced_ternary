import Problems.Juggler.Cycles
import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
# The two leftover length-six cycle orientations

`OOOEOE` and `OOOOEE` are the remaining legal `CycleMin` orientations
among the expanding length-six even-terminating words. Uniform extra
scale from `n = 3` fails. The argument here is a finite evaluation
below `256` plus the coarse comparison `n^81 > 2^130 (n+1)^64` for
`n ≥ 256`.

This is not a length-six census, not an exclusion of odd-terminating
cycle words, and not a halt theorem.
-/

theorem wordOOOEOE_eq_eval : wordOOOEOE = wordOOOEOE' :=
  rfl

theorem cycleWordB_iff {n : ℕ} {w : List Branch} :
    cycleWordB n w = true ↔ CycleWord n w := by
  simp [cycleWordB, CycleWord, followsB_iff, Bool.and_eq_true, beq_iff_eq]
  exact and_assoc

theorem no_cycle_word_oooeoe_of_lt {n : ℕ} (hn : n < 256) :
    ¬CycleWord n wordOOOEOE := by
  intro h
  have hfalse : cycleWordB n wordOOOEOE = false := by
    simpa [wordOOOEOE_eq_eval] using cycleWordB_oooeoe_lt256 ⟨n, hn⟩
  have htrue : cycleWordB n wordOOOEOE = true := cycleWordB_iff.mpr h
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_ooooee_of_lt {n : ℕ} (hn : n < 256) :
    ¬CycleWord n wordOOOOEE := by
  intro h
  have hfalse := cycleWordB_ooooee_lt256 ⟨n, hn⟩
  have htrue : cycleWordB n wordOOOOEE = true := cycleWordB_iff.mpr h
  rw [hfalse] at htrue
  exact Bool.false_ne_true htrue

theorem four_eq_two_pow : (4 : ℕ) = 2 ^ 2 := by
  decide

theorem lowerDenomFrom_odd_cons (k o D : ℕ) (w : List Branch) :
    lowerDenomFrom k o D (Branch.odd :: w) =
      lowerDenomFrom (k + 1) (o + 1) (D ^ 3 * 4 ^ (2 ^ k)) w :=
  rfl

theorem lowerDenomFrom_nil (k o D : ℕ) :
    lowerDenomFrom k o D [] = D :=
  rfl

theorem two_pow_mul (n m : ℕ) : (2 ^ n) ^ m = 2 ^ (n * m) :=
  (Nat.pow_mul 2 n m).symm

theorem four_pow_two_pow (k : ℕ) : (4 : ℕ) ^ (2 ^ k) = 2 ^ (2 * 2 ^ k) := by
  rw [four_eq_two_pow, ← Nat.pow_mul]

theorem lowerDenom_ooo :
    lowerDenom [Branch.odd, Branch.odd, Branch.odd] = 2 ^ 38 := by
  rw [lowerDenom, lowerDenomFrom_odd_cons]
  have s0 : (1 : ℕ) ^ 3 * 4 ^ (2 ^ 0) = 2 ^ 2 := by decide
  rw [s0, lowerDenomFrom_odd_cons]
  have s1 : (2 ^ 2) ^ 3 * 4 ^ (2 ^ 1) = 2 ^ 10 := by
    rw [two_pow_mul, four_pow_two_pow, ← Nat.pow_add]
    rfl
  rw [s1, lowerDenomFrom_odd_cons]
  have s2 : (2 ^ 10) ^ 3 * 4 ^ (2 ^ 2) = 2 ^ 38 := by
    rw [two_pow_mul, four_pow_two_pow, ← Nat.pow_add]
    rfl
  rw [s2, lowerDenomFrom_nil]

theorem lowerDenom_oooo :
    lowerDenom [Branch.odd, Branch.odd, Branch.odd, Branch.odd] = 2 ^ 130 := by
  rw [lowerDenom, lowerDenomFrom_odd_cons]
  have s0 : (1 : ℕ) ^ 3 * 4 ^ (2 ^ 0) = 2 ^ 2 := by decide
  rw [s0, lowerDenomFrom_odd_cons]
  have s1 : (2 ^ 2) ^ 3 * 4 ^ (2 ^ 1) = 2 ^ 10 := by
    rw [two_pow_mul, four_pow_two_pow, ← Nat.pow_add]
    rfl
  rw [s1, lowerDenomFrom_odd_cons]
  have s2 : (2 ^ 10) ^ 3 * 4 ^ (2 ^ 2) = 2 ^ 38 := by
    rw [two_pow_mul, four_pow_two_pow, ← Nat.pow_add]
    rfl
  rw [s2, lowerDenomFrom_odd_cons]
  have s3 : (2 ^ 38) ^ 3 * 4 ^ (2 ^ 3) = 2 ^ 130 := by
    rw [two_pow_mul, four_pow_two_pow, ← Nat.pow_add]
    rfl
  rw [s3, lowerDenomFrom_nil]

theorem oddCount_ooo :
    oddCount [Branch.odd, Branch.odd, Branch.odd] = 3 :=
  rfl

theorem oddCount_oooo :
    oddCount [Branch.odd, Branch.odd, Branch.odd, Branch.odd] = 4 :=
  rfl

theorem two_pow_256 : (256 : ℕ) = 2 ^ 8 := by
  decide

/-- For `n ≥ 256`, `(n+1)^64 < 2 n^64`. Uses the isolated `257^64` comparison. -/
theorem succ_pow64_lt {n : ℕ} (hn : 256 ≤ n) :
    (n + 1) ^ 64 < 2 * n ^ 64 := by
  have hlin : 256 * (n + 1) ≤ 257 * n := by omega
  have hpow : (256 * (n + 1)) ^ 64 ≤ (257 * n) ^ 64 :=
    Nat.pow_le_pow_left hlin 64
  rw [mul_pow, mul_pow] at hpow
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : (0 : ℕ) < 256) hn
  have hstrict : 257 ^ 64 * n ^ 64 < 2 * 256 ^ 64 * n ^ 64 :=
    Nat.mul_lt_mul_of_pos_right two_mul_pow256_gt_pow257 (pow_pos hn0 64)
  have hmid : 256 ^ 64 * (n + 1) ^ 64 < 2 * 256 ^ 64 * n ^ 64 :=
    lt_of_le_of_lt hpow hstrict
  have hRHS : 2 * 256 ^ 64 * n ^ 64 = 256 ^ 64 * (2 * n ^ 64) :=
    calc
      2 * 256 ^ 64 * n ^ 64 = 2 * (256 ^ 64 * n ^ 64) := by rw [mul_assoc]
      _ = (256 ^ 64 * n ^ 64) * 2 := by rw [mul_comm]
      _ = 256 ^ 64 * (n ^ 64 * 2) := by rw [mul_assoc]
      _ = 256 ^ 64 * (2 * n ^ 64) := by rw [mul_comm (n ^ 64)]
  have hpos : 0 < 256 ^ 64 := pow_pos (by decide : (0 : ℕ) < 256) 64
  exact (Nat.mul_lt_mul_left hpos).mp (hmid.trans_eq hRHS)

theorem pow81_gt_two_pow130_succ_pow64 {n : ℕ} (hn : 256 ≤ n) :
    2 ^ 130 * (n + 1) ^ 64 < n ^ 81 := by
  have hsucc := succ_pow64_lt hn
  have hmul : 2 ^ 130 * (n + 1) ^ 64 < 2 ^ 130 * (2 * n ^ 64) :=
    Nat.mul_lt_mul_of_pos_left hsucc (pow_pos (by decide : (0 : ℕ) < 2) 130)
  have hexp : 2 ^ 130 * (2 * n ^ 64) = 2 ^ 131 * n ^ 64 := by
    rw [← mul_assoc, ← pow_succ]
  have h131 : 2 ^ 130 * (n + 1) ^ 64 < 2 ^ 131 * n ^ 64 :=
    hmul.trans_eq hexp
  have hn17 : 2 ^ 136 ≤ n ^ 17 := by
    have hpow : (256 : ℕ) ^ 17 ≤ n ^ 17 := Nat.pow_le_pow_left hn 17
    have h256 : (256 : ℕ) ^ 17 = 2 ^ 136 := by
      rw [two_pow_256, ← Nat.pow_mul]
    exact h256 ▸ hpow
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : (0 : ℕ) < 256) hn
  have h136 : 2 ^ 131 * n ^ 64 < 2 ^ 136 * n ^ 64 :=
    Nat.mul_lt_mul_of_pos_right
      (Nat.pow_lt_pow_right (by decide : (1 : ℕ) < 2) (by decide : (131 : ℕ) < 136))
      (pow_pos hn0 64)
  have hle : 2 ^ 136 * n ^ 64 ≤ n ^ 17 * n ^ 64 :=
    Nat.mul_le_mul_right _ hn17
  have h81 : n ^ 17 * n ^ 64 = n ^ 81 := by
    rw [← Nat.pow_add]
  exact (h131.trans h136).trans_le (hle.trans_eq h81)

theorem cube_succ (y : ℕ) :
    (y + 1) ^ 3 = y ^ 3 + 3 * y ^ 2 + 3 * y + 1 := by
  ring

theorem succ_cube_lt_two_mul_pow4 {A : ℕ} (hA : 2 ≤ A) :
    (A + 1) ^ 3 < 2 * A ^ 4 := by
  have hL : (A + 1) ^ 3 = A ^ 3 + 3 * A ^ 2 + 3 * A + 1 := cube_succ A
  rw [hL]
  have hle : A ^ 2 + A + 1 ≤ A ^ 3 := by
    cases lt_or_ge A 3 with
    | inl hlt =>
        have : A = 2 := by omega
        subst this
        decide
    | inr hge =>
        have hmul : 3 * A ^ 2 ≤ A * A ^ 2 :=
          Nat.mul_le_mul_right (A ^ 2) hge
        have hA3 : A * A ^ 2 = A ^ 3 := by
          ring
        have hsmall : A ^ 2 + A + 1 ≤ 3 * A ^ 2 := by
          have hA1 : 1 ≤ A := by omega
          have hself : A ≤ A ^ 2 := by
            simpa [pow_two] using Nat.le_mul_of_pos_right A hA1
          have : A + 1 ≤ 2 * A ^ 2 :=
            calc
              A + 1 ≤ A + A := Nat.add_le_add_left hA1 A
              _ = 2 * A := by ring
              _ ≤ 2 * A ^ 2 := Nat.mul_le_mul_left 2 hself
          have : A ^ 2 + (A + 1) ≤ A ^ 2 + 2 * A ^ 2 := Nat.add_le_add_left this _
          have h3A : A ^ 2 + 2 * A ^ 2 = 3 * A ^ 2 := by ring
          simpa [Nat.add_assoc, h3A] using this
        exact le_trans hsmall (by simpa [hA3] using hmul)
  have h3 : 3 * A ^ 2 + 3 * A + 1 < 3 * A ^ 3 := by
    have hmul : 3 * (A ^ 2 + A + 1) ≤ 3 * A ^ 3 := Nat.mul_le_mul_left 3 hle
    have hlt : 3 * A ^ 2 + 3 * A + 1 < 3 * (A ^ 2 + A + 1) := by omega
    exact lt_of_lt_of_le hlt hmul
  have hge : 3 * A ^ 3 ≤ (2 * A - 1) * A ^ 3 := by
    have : 3 ≤ 2 * A - 1 := by omega
    exact Nat.mul_le_mul_right (A ^ 3) this
  have hge' : 3 * A ^ 3 ≤ A ^ 3 * (2 * A - 1) := by
    simpa [mul_comm] using hge
  have hsum :
      A ^ 3 + (3 * A ^ 2 + 3 * A + 1) < A ^ 3 + A ^ 3 * (2 * A - 1) :=
    Nat.add_lt_add_left (lt_of_lt_of_le h3 hge') _
  have hsum' :
      A ^ 3 + 3 * A ^ 2 + 3 * A + 1 < A ^ 3 + A ^ 3 * (2 * A - 1) := by
    simpa [Nat.add_assoc] using hsum
  have hadd : A ^ 3 + A ^ 3 * (2 * A - 1) = A ^ 3 * (2 * A) := by
    have hk : 1 + (2 * A - 1) = 2 * A := by omega
    calc
      A ^ 3 + A ^ 3 * (2 * A - 1)
          = A ^ 3 * 1 + A ^ 3 * (2 * A - 1) := by ring
      _ = A ^ 3 * (1 + (2 * A - 1)) := (Nat.mul_add (A ^ 3) 1 (2 * A - 1)).symm
      _ = A ^ 3 * (2 * A) := by rw [hk]
  have h2 : A ^ 3 * (2 * A) = 2 * A ^ 4 := by ring
  exact hsum'.trans_eq (hadd.trans h2)

theorem cube_succ_lt_two_mul_of_cube_lt_pow4 {y A : ℕ}
    (hA : 3 ≤ A) (h : y ^ 3 < A ^ 4) :
    (y + 1) ^ 3 < 2 * A ^ 4 := by
  cases le_or_gt y A with
  | inl hle =>
      have : (y + 1) ^ 3 ≤ (A + 1) ^ 3 :=
        Nat.pow_le_pow_left (Nat.succ_le_succ hle) 3
      exact lt_of_le_of_lt this (succ_cube_lt_two_mul_pow4 (by omega))
  | inr hgt =>
      have hyA : A + 1 ≤ y := Nat.succ_le_of_lt hgt
      have hy4 : 4 ≤ y := le_trans (by omega : (4 : ℕ) ≤ A + 1) hyA
      have hy0 : 0 < y := lt_of_lt_of_le (by decide : (0 : ℕ) < 4) hy4
      have hlin : 3 * y + 1 < y ^ 2 := by
        have h4 : 4 * y ≤ y * y := Nat.mul_le_mul_right y hy4
        have h3 : 3 * y + 1 < 4 * y := by omega
        exact lt_of_lt_of_le h3 (by simpa [pow_two] using h4)
      have h4y' : 3 * y ^ 2 + 3 * y + 1 < 4 * y ^ 2 := by
        have : 3 * y ^ 2 + y ^ 2 = 4 * y ^ 2 := by ring
        have h' : 3 * y ^ 2 + (3 * y + 1) < 3 * y ^ 2 + y ^ 2 :=
          Nat.add_lt_add_left hlin (3 * y ^ 2)
        simpa [Nat.add_assoc, this] using h'
      have h4cube : 4 * y ^ 3 < 4 * A ^ 4 :=
        Nat.mul_lt_mul_of_pos_left h (by decide : (0 : ℕ) < 4)
      have h4A : 4 * A ^ 4 ≤ y * A ^ 4 :=
        Nat.mul_le_mul_right (A ^ 4) hy4
      have hy3 : 4 * y ^ 2 * y = 4 * y ^ 3 := by ring
      have h4sq : 4 * y ^ 2 < A ^ 4 := by
        have : 4 * y ^ 2 * y < A ^ 4 * y := by
          have hlt : 4 * y ^ 3 < y * A ^ 4 := lt_of_lt_of_le h4cube h4A
          rw [hy3, mul_comm (A ^ 4)]
          exact hlt
        exact (Nat.mul_lt_mul_right hy0).mp this
      have hsum : (y + 1) ^ 3 < A ^ 4 + 4 * y ^ 2 := by
        rw [cube_succ]
        have hleft :
            y ^ 3 + (3 * y ^ 2 + 3 * y + 1) <
              A ^ 4 + (3 * y ^ 2 + 3 * y + 1) :=
          Nat.add_lt_add_right h _
        have hleft' : y ^ 3 + 3 * y ^ 2 + 3 * y + 1 <
            A ^ 4 + (3 * y ^ 2 + 3 * y + 1) := by
          simpa [Nat.add_assoc] using hleft
        exact lt_of_lt_of_le hleft' (Nat.add_le_add_left (le_of_lt h4y') _)
      have htwo : A ^ 4 + 4 * y ^ 2 < 2 * A ^ 4 := by
        have : A ^ 4 + 4 * y ^ 2 < A ^ 4 + A ^ 4 := Nat.add_lt_add_left h4sq _
        have hexp : A ^ 4 + A ^ 4 = 2 * A ^ 4 := by ring
        simpa [hexp] using this
      exact hsum.trans htwo

theorem ooooee_prefix_lt_succ_pow4 {n : ℕ}
    (h : CycleWord n wordOOOOEE) :
    image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] < (n + 1) ^ 4 := by
  have hcell :
      CycleWord n
        ([Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.even] ++
          [Branch.even]) := by
    simpa [wordOOOOEE] using h
  have hI := cycle_last_even_interval hcell
  have hf4 :
      follows (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd])
        [Branch.even, Branch.even] :=
    follows_of_append_right
      (u := [Branch.odd, Branch.odd, Branch.odd, Branch.odd])
      (by simpa [wordOOOOEE] using h.1)
  have he4 :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] % 2 = 0 :=
    hf4.1
  have hz5 :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.even] =
        floorPower
          (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) := by
    simp [image]
  have hz4lt :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] <
        (floorPower
            (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he4).mp rfl).2
  have hz5lt :
      floorPower (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) <
        (n + 1) ^ 2 := by
    simpa [hz5] using hI.2
  have hsucc :
      floorPower (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) + 1 ≤
        (n + 1) ^ 2 :=
    Nat.succ_le_of_lt hz5lt
  have hsq :
      (floorPower
            (image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) + 1) ^ 2 ≤
        ((n + 1) ^ 2) ^ 2 :=
    Nat.pow_le_pow_left hsucc 2
  have hexp : ((n + 1) ^ 2) ^ 2 = (n + 1) ^ 4 :=
    (Nat.pow_mul (n + 1) 2 2).symm
  exact lt_of_lt_of_le hz4lt (hexp ▸ hsq)

theorem oooo_lower_growth {n : ℕ} (hn : 1 ≤ n)
    (hw : follows n [Branch.odd, Branch.odd, Branch.odd, Branch.odd]) :
    n ^ 81 ≤ 2 ^ 130 *
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] ^ 16 := by
  have hL := lower_growth_word hn hw
  rw [LowerPowerBound, oddCount_oooo, lowerDenom_oooo] at hL
  have hlen :
      ([Branch.odd, Branch.odd, Branch.odd, Branch.odd] : List Branch).length = 4 :=
    rfl
  rw [hlen] at hL
  have h3 : (3 : ℕ) ^ 4 = 81 := by decide
  have h2 : (2 : ℕ) ^ 4 = 16 := by decide
  rw [h3, h2] at hL
  exact hL

theorem ooo_lower_growth {n : ℕ} (hn : 1 ≤ n)
    (hw : follows n [Branch.odd, Branch.odd, Branch.odd]) :
    n ^ 27 ≤ 2 ^ 38 * image n [Branch.odd, Branch.odd, Branch.odd] ^ 8 := by
  have hL := lower_growth_word hn hw
  rw [LowerPowerBound, oddCount_ooo, lowerDenom_ooo] at hL
  have hlen :
      ([Branch.odd, Branch.odd, Branch.odd] : List Branch).length = 3 :=
    rfl
  rw [hlen] at hL
  have h3 : (3 : ℕ) ^ 3 = 27 := by decide
  have h2 : (2 : ℕ) ^ 3 = 8 := by decide
  rw [h3, h2] at hL
  exact hL

theorem pow_lt_of_lt_pow_mul {a b k m : ℕ} (h : a < b ^ k) (hm : m ≠ 0) :
    a ^ m < b ^ (k * m) := by
  have := Nat.pow_lt_pow_left h hm
  rwa [← Nat.pow_mul] at this

theorem no_cycle_word_ooooee_of_ge {n : ℕ} (hn : 256 ≤ n)
    (h : CycleWord n wordOOOOEE) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hOOOO :
      follows n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] :=
    follows_of_append_left (v := [Branch.even, Branch.even])
      (by simpa [wordOOOOEE] using h.1)
  have hz := ooooee_prefix_lt_succ_pow4 h
  have hpow := oooo_lower_growth hn1 hOOOO
  have hz16 : image n [Branch.odd, Branch.odd, Branch.odd, Branch.odd] ^ 16 <
      (n + 1) ^ 64 := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 16) hz (by decide)
    simpa using this
  have hlt : n ^ 81 < 2 ^ 130 * (n + 1) ^ 64 :=
    lt_of_le_of_lt hpow (Nat.mul_lt_mul_of_pos_left hz16
      (pow_pos (by decide : (0 : ℕ) < 2) 130))
  exact (not_lt_of_gt (pow81_gt_two_pow130_succ_pow64 hn)) hlt

theorem oooeoe_y_cube_lt {n : ℕ} (h : CycleWord n wordOOOEOE) :
    image n [Branch.odd, Branch.odd, Branch.odd, Branch.even] ^ 3 <
      (n + 1) ^ 4 := by
  have hcell :
      CycleWord n
        ([Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd] ++
          [Branch.even]) := by
    simpa [wordOOOEOE] using h
  have hI := cycle_last_even_interval hcell
  have hyO :
      follows (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even])
        [Branch.odd, Branch.even] :=
    follows_of_append_right
      (u := [Branch.odd, Branch.odd, Branch.odd, Branch.even])
      (by simpa [wordOOOEOE] using h.1)
  have hyodd :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.even] % 2 = 1 :=
    hyO.1
  have hz5 :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd] =
        floorPower
          (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]) := by
    simp [image]
  have hcube := (floorPower_odd_eq_iff_cube_interval hyodd).mp rfl
  have hylt :
      image n [Branch.odd, Branch.odd, Branch.odd, Branch.even] ^ 3 <
        (floorPower
            (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]) + 1) ^ 2 :=
    hcube.2
  have hz5lt :
      floorPower (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]) <
        (n + 1) ^ 2 := by
    simpa [hz5] using hI.2
  have hsucc :
      floorPower (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]) + 1 ≤
        (n + 1) ^ 2 :=
    Nat.succ_le_of_lt hz5lt
  have hsq :
      (floorPower
            (image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]) + 1) ^ 2 ≤
        ((n + 1) ^ 2) ^ 2 :=
    Nat.pow_le_pow_left hsucc 2
  have hexp : ((n + 1) ^ 2) ^ 2 = (n + 1) ^ 4 :=
    (Nat.pow_mul (n + 1) 2 2).symm
  exact lt_of_lt_of_le hylt (hexp ▸ hsq)

theorem no_cycle_word_oooeoe_of_ge {n : ℕ} (hn : 256 ≤ n)
    (h : CycleWord n wordOOOEOE) : False := by
  have hn1 : 1 ≤ n := le_trans (by decide : (1 : ℕ) ≤ 256) hn
  have hOOO : follows n [Branch.odd, Branch.odd, Branch.odd] :=
    follows_of_append_left
      (v := [Branch.even, Branch.odd, Branch.even])
      (by simpa [wordOOOEOE] using h.1)
  set z3 := image n [Branch.odd, Branch.odd, Branch.odd]
  set y := image n [Branch.odd, Branch.odd, Branch.odd, Branch.even]
  have he3 : z3 % 2 = 0 := by
    have hf : follows z3 [Branch.even, Branch.odd, Branch.even] :=
      follows_of_append_right (u := [Branch.odd, Branch.odd, Branch.odd])
        (by simpa [wordOOOEOE] using h.1)
    exact hf.1
  have hyeq : floorPower z3 = y := by
    simp [z3, y, image]
  have hz3lt : z3 < (y + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he3).mp hyeq).2
  have hpow := ooo_lower_growth hn1 hOOO
  have hz8 : z3 ^ 8 < (y + 1) ^ 16 := by
    have := pow_lt_of_lt_pow_mul (k := 2) (m := 8) hz3lt (by decide)
    simpa using this
  have h27 : n ^ 27 < 2 ^ 38 * (y + 1) ^ 16 :=
    lt_of_le_of_lt hpow (Nat.mul_lt_mul_of_pos_left hz8
      (pow_pos (by decide : (0 : ℕ) < 2) 38))
  have h81 := cube_ooo_lower h27
  have hy3 := oooeoe_y_cube_lt h
  have hA : 3 ≤ n + 1 :=
    le_trans (by decide : (3 : ℕ) ≤ 257)
      (Nat.succ_le_succ (le_trans (by decide : (1 : ℕ) ≤ 256) hn))
  have hysucc : (y + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA (by simpa [y] using hy3)
  have hy48 := y_succ_pow48 hysucc
  have hlt := combine_ooo_tail h81 hy48
  exact (not_lt_of_gt (pow81_gt_two_pow130_succ_pow64 hn)) hlt

theorem no_cycle_word_oooeoe {n : ℕ} (_hn : 2 ≤ n) :
    ¬CycleWord n wordOOOEOE := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycle_word_oooeoe_of_lt hlt h
  | inr hge => exact no_cycle_word_oooeoe_of_ge hge h

theorem no_cycle_word_ooooee {n : ℕ} (_hn : 2 ≤ n) :
    ¬CycleWord n wordOOOOEE := by
  intro h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycle_word_ooooee_of_lt hlt h
  | inr hge => exact no_cycle_word_ooooee_of_ge hge h

end Problems.Juggler
