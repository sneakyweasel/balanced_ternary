import Problems.Juggler.LeftoverTwoEven
import Problems.Juggler.FirstETransportEval

namespace Problems.Juggler

/-!
# First-E transport of the uniform two-even tail

On a `CycleMin` the remainder after the first even letter of a
gapped three-even leftover is a two-even leftover family, started
at `y ≥ n`. The leftover cell is measured against the cycle start
`n`, so `y ≥ n` tightens it against the shared two-even tail at
`y`. Large `y` is the uniform cutoff `y ≥ 256`. Below `256`, short
gaps are tables and long gaps are seven-odd.

This excludes gapped `CycleMin`s only. It is not a `CycleWord`
theorem at a non-minimum start, not a bunched-tail attack, not a
length-8 or length-9 census, and not a halt theorem. Paper A
records the transport as Theorem 3.13.
-/

theorem four_mul_two_pow (b : ℕ) : 4 * 2 ^ b = 2 ^ (b + 2) := by
  have h4 : (4 : ℕ) = 2 ^ 2 := rfl
  rw [h4, ← Nat.pow_add]
  congr 1
  omega

theorem gappedThreeEvenEE_eq_twoEven (a b : ℕ) :
    gappedThreeEvenEE a b = firstEPrefix a ++ twoEvenEE (b + 2) := by
  have hb : b + 2 - 2 = b := Nat.add_sub_cancel b 2
  simp [gappedThreeEvenEE, twoEvenEE, hb, List.append_assoc]

theorem gappedThreeEvenEOE_eq_twoEven (a b : ℕ) :
    gappedThreeEvenEOE a b = firstEPrefix a ++ twoEvenEOE (b + 3) := by
  have hb : b + 3 - 3 = b := Nat.add_sub_cancel b 3
  simp [gappedThreeEvenEOE, twoEvenEOE, hb, List.append_assoc]

theorem gappedThreeEvenEE_length (a b : ℕ) :
    (gappedThreeEvenEE a b).length = a + b + 3 := by
  simp [gappedThreeEvenEE, firstEPrefix, List.length_append, List.length_replicate]
  omega

theorem gappedThreeEvenEOE_length (a b : ℕ) :
    (gappedThreeEvenEOE a b).length = a + b + 4 := by
  simp [gappedThreeEvenEOE, firstEPrefix, List.length_append, List.length_replicate]
  omega

theorem firstEPrefix_length (a : ℕ) : (firstEPrefix a).length = a + 1 := by
  simp [firstEPrefix, List.length_append, List.length_replicate]

theorem firstEPrefix_image (n a : ℕ) :
    image n (firstEPrefix a) = floorPower^[a + 1] n := by
  simp [firstEPrefix, image_eq_iterate, List.length_append, List.length_replicate]

theorem cycleMin_gapped_ee_y_ge {n a b : ℕ}
    (h : CycleMin n (gappedThreeEvenEE a b)) :
    n ≤ image n (firstEPrefix a) := by
  have hlen := gappedThreeEvenEE_length a b
  have hj : a + 1 < (gappedThreeEvenEE a b).length := by omega
  have : n ≤ floorPower^[a + 1] n := cycleMin_ge h hj
  simpa [firstEPrefix_image] using this

theorem cycleMin_gapped_eoe_y_ge {n a b : ℕ}
    (h : CycleMin n (gappedThreeEvenEOE a b)) :
    n ≤ image n (firstEPrefix a) := by
  have hlen := gappedThreeEvenEOE_length a b
  have hj : a + 1 < (gappedThreeEvenEOE a b).length := by omega
  have : n ≤ floorPower^[a + 1] n := cycleMin_ge h hj
  simpa [firstEPrefix_image] using this

theorem follows_gapped_ee_prefix {n a b : ℕ}
    (h : follows n (gappedThreeEvenEE a b)) : follows n (firstEPrefix a) :=
  follows_of_append_left
    (v := List.replicate b Branch.odd ++ [Branch.even, Branch.even])
    (by simpa [gappedThreeEvenEE, List.append_assoc] using h)

theorem follows_gapped_eoe_prefix {n a b : ℕ}
    (h : follows n (gappedThreeEvenEOE a b)) : follows n (firstEPrefix a) :=
  follows_of_append_left
    (v := List.replicate b Branch.odd ++
      [Branch.even, Branch.odd, Branch.even])
    (by simpa [gappedThreeEvenEOE, List.append_assoc] using h)

theorem follows_gapped_ee_remaining_odds {n a b : ℕ}
    (h : follows n (gappedThreeEvenEE a b)) :
    follows (image n (firstEPrefix a)) (List.replicate b Branch.odd) :=
  follows_of_append_left (v := [Branch.even, Branch.even])
    (follows_of_append_right (u := firstEPrefix a)
      (by simpa [gappedThreeEvenEE, List.append_assoc] using h))

theorem follows_gapped_eoe_remaining_odds {n a b : ℕ}
    (h : follows n (gappedThreeEvenEOE a b)) :
    follows (image n (firstEPrefix a)) (List.replicate b Branch.odd) :=
  follows_of_append_left (v := [Branch.even, Branch.odd, Branch.even])
    (follows_of_append_right (u := firstEPrefix a)
      (by simpa [gappedThreeEvenEOE, List.append_assoc] using h))

theorem firstEPrefix_image_ge_two {n a : ℕ}
    (hn : 2 ≤ n) (ha : 1 ≤ a) (h : follows n (firstEPrefix a)) :
    2 ≤ image n (firstEPrefix a) := by
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left (v := [Branch.even]) (by simpa [firstEPrefix] using h)
  have hcons : List.replicate a Branch.odd =
      Branch.odd :: List.replicate (a - 1) Branch.odd := by
    cases a with
    | zero => exact (Nat.not_succ_le_zero 0 ha).elim
    | succ a => rfl
  have hnOdd : n % 2 = 1 := by
    have : follows n (Branch.odd :: List.replicate (a - 1) Branch.odd) := by
      simpa [hcons] using hO
    exact this.1
  have hn3 : 3 ≤ n := by omega
  have hz : n < image n (List.replicate a Branch.odd) := by
    simpa [image_eq_iterate, List.length_replicate] using
      odd_word_expands hn3 ha hO
  have hz4 : 4 ≤ image n (List.replicate a Branch.odd) := by omega
  have he : image n (List.replicate a Branch.odd) % 2 = 0 := by
    have hf : follows (image n (List.replicate a Branch.odd)) [Branch.even] :=
      follows_of_append_right (u := List.replicate a Branch.odd)
        (by simpa [firstEPrefix] using h)
    change _ % 2 = 0 ∧ follows (floorPower _) [] at hf
    exact hf.1
  have hy : image n (firstEPrefix a) =
      (image n (List.replicate a Branch.odd)).sqrt := by
    simp [firstEPrefix, image_append, image, floorPower_even_eq he]
  have : 2 ≤ (image n (List.replicate a Branch.odd)).sqrt :=
    Nat.le_sqrt.mpr (by simpa [pow_two] using hz4)
  simpa [hy] using this

theorem gapped_ee_cell {n a b : ℕ}
    (hy : 1 ≤ image n (firstEPrefix a))
    (h : CycleWord n (gappedThreeEvenEE a b)) :
    image n (firstEPrefix a) ^ (3 ^ b) <
      2 ^ denomBits b * (n + 1) ^ (2 ^ (b + 2)) := by
  set y := image n (firstEPrefix a)
  set v := firstEPrefix a ++ List.replicate b Branch.odd
  have hsplit : gappedThreeEvenEE a b =
      v ++ List.replicate 2 Branch.even := by
    simp [gappedThreeEvenEE, v, List.append_assoc]
  have hC : CycleWord n (v ++ List.replicate 2 Branch.even) := by
    simpa [hsplit] using h
  have hz := cycle_trailing_evens_lt (r := 2) (by decide) hC
  have hO : follows y (List.replicate b Branch.odd) :=
    follows_gapped_ee_remaining_odds h.1
  have hpow := odd_run_lower_growth hy hO
  have himg : image y (List.replicate b Branch.odd) = image n v := by
    simp [y, v, image_append]
  have hz' : image y (List.replicate b Branch.odd) < (n + 1) ^ 4 := by
    simpa [himg] using hz
  have hm : 2 ^ b ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow :
      image y (List.replicate b Branch.odd) ^ (2 ^ b) <
        (n + 1) ^ (2 ^ (b + 2)) := by
    have := pow_lt_of_lt_pow_mul (k := 4) (m := 2 ^ b) hz' hm
    rwa [four_mul_two_pow b] at this
  exact lt_of_le_of_lt hpow
    (Nat.mul_lt_mul_of_pos_left hzpow
      (pow_pos (by decide : (0 : ℕ) < 2) _))

theorem gapped_eoe_cell {n a b : ℕ}
    (hn : 2 ≤ n) (hy : 1 ≤ image n (firstEPrefix a))
    (h : CycleWord n (gappedThreeEvenEOE a b)) :
    image n (firstEPrefix a) ^ (3 ^ (b + 1)) <
      2 ^ denomBits (b + 1) * (n + 1) ^ (2 ^ (b + 3)) := by
  set y := image n (firstEPrefix a)
  set u := List.replicate b Branch.odd
  set z := image y u
  set w := image y (u ++ [Branch.even])
  have hC' : CycleWord n
      ((firstEPrefix a ++ u) ++ [Branch.even, Branch.odd, Branch.even]) := by
    simpa [gappedThreeEvenEOE, List.append_assoc] using h
  have hO : follows y u := follows_gapped_eoe_remaining_odds h.1
  have he : z % 2 = 0 := by
    have hf : follows y (u ++ [Branch.even, Branch.odd, Branch.even]) :=
      follows_of_append_right (u := firstEPrefix a)
        (by simpa [gappedThreeEvenEOE, List.append_assoc] using h.1)
    have hfE : follows z [Branch.even, Branch.odd, Branch.even] :=
      follows_of_append_right (u := u) hf
    change z % 2 = 0 ∧ follows (floorPower z) [Branch.odd, Branch.even] at hfE
    exact hfE.1
  have hyeq : floorPower z = w := by
    simp [z, w, u, image_append, image]
  have hzlt : z < (w + 1) ^ 2 :=
    ((floorPower_even_eq_iff_sq_interval he).mp hyeq).2
  have hpow := odd_run_lower_growth hy hO
  have hm : 2 ^ b ≠ 0 :=
    Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
  have hzpow : z ^ (2 ^ b) < (w + 1) ^ (2 ^ (b + 1)) := by
    have := pow_lt_of_lt_pow_mul (k := 2) (m := 2 ^ b) hzlt hm
    rwa [two_mul_two_pow b] at this
  have hmid : y ^ (3 ^ b) <
      2 ^ denomBits b * (w + 1) ^ (2 ^ (b + 1)) :=
    lt_of_le_of_lt hpow
      (Nat.mul_lt_mul_of_pos_left hzpow
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  have hcube : y ^ (3 ^ (b + 1)) <
      2 ^ (3 * denomBits b) * (w + 1) ^ (3 * 2 ^ (b + 1)) := by
    have hlt : (y ^ (3 ^ b)) ^ 3 <
        (2 ^ denomBits b * (w + 1) ^ (2 ^ (b + 1))) ^ 3 :=
      Nat.pow_lt_pow_left hmid (by decide : (3 : ℕ) ≠ 0)
    have hL : (y ^ (3 ^ b)) ^ 3 = y ^ (3 ^ (b + 1)) := by
      rw [← Nat.pow_mul, ← Nat.pow_succ]
    have hR : (2 ^ denomBits b * (w + 1) ^ (2 ^ (b + 1))) ^ 3 =
        2 ^ (3 * denomBits b) * (w + 1) ^ (3 * 2 ^ (b + 1)) :=
      two_mul_pow_cube _ _ _
    rwa [hL, hR] at hlt
  have hw3 : w ^ 3 < (n + 1) ^ 4 := by
    have hcube' := cycle_eoe_suffix_y_cube_lt (u := firstEPrefix a ++ u) hC'
    simpa [w, y, u, image_append, List.append_assoc] using hcube'
  have hA : 3 ≤ n + 1 := by omega
  have hwsucc : (w + 1) ^ 3 < 2 * (n + 1) ^ 4 :=
    cube_succ_lt_two_mul_of_cube_lt_pow4 hA hw3
  have hwraise : (w + 1) ^ (3 * 2 ^ (b + 1)) <
      2 ^ (2 ^ (b + 1)) * (n + 1) ^ (2 ^ (b + 3)) := by
    have hm' : 2 ^ (b + 1) ≠ 0 :=
      Nat.pos_iff_ne_zero.mp (pow_pos (by decide : (0 : ℕ) < 2) _)
    have hlt : ((w + 1) ^ 3) ^ (2 ^ (b + 1)) <
        (2 * (n + 1) ^ 4) ^ (2 ^ (b + 1)) :=
      Nat.pow_lt_pow_left hwsucc hm'
    have hL : ((w + 1) ^ 3) ^ (2 ^ (b + 1)) =
        (w + 1) ^ (3 * 2 ^ (b + 1)) :=
      (Nat.pow_mul (w + 1) 3 (2 ^ (b + 1))).symm
    have hR : (2 * (n + 1) ^ 4) ^ (2 ^ (b + 1)) =
        2 ^ (2 ^ (b + 1)) * (n + 1) ^ (4 * 2 ^ (b + 1)) := by
      rw [mul_pow, Nat.pow_mul]
    have hexp : 4 * 2 ^ (b + 1) = 2 ^ (b + 3) := by
      have h4 : (4 : ℕ) = 2 ^ 2 := rfl
      rw [h4, ← Nat.pow_add]
      congr 1
      omega
    rw [hL, hR, hexp] at hlt
    exact hlt
  have hmid' : y ^ (3 ^ (b + 1)) <
      2 ^ (3 * denomBits b) *
        (2 ^ (2 ^ (b + 1)) * (n + 1) ^ (2 ^ (b + 3))) :=
    lt_trans hcube
      (Nat.mul_lt_mul_of_pos_left hwraise
        (pow_pos (by decide : (0 : ℕ) < 2) _))
  have hexp :
      2 ^ (3 * denomBits b) *
          (2 ^ (2 ^ (b + 1)) * (n + 1) ^ (2 ^ (b + 3))) =
        2 ^ (3 * denomBits b + 2 ^ (b + 1)) * (n + 1) ^ (2 ^ (b + 3)) := by
    rw [← mul_assoc, ← Nat.pow_add]
  have hbits : 3 * denomBits b + 2 ^ (b + 1) = denomBits (b + 1) :=
    (denomBits_succ b).symm
  rwa [hexp, hbits] at hmid'

theorem no_cycleMin_gapped_three_even_ee_of_y {n a b : ℕ}
    (hb : 4 ≤ b) (h : CycleMin n (gappedThreeEvenEE a b))
    (hy : 256 ≤ image n (firstEPrefix a)) : False := by
  set y := image n (firstEPrefix a)
  have hC : CycleWord n (gappedThreeEvenEE a b) := cycleMin_cycleWord h
  have hyn : n ≤ y := cycleMin_gapped_ee_y_ge h
  have hy1 : 1 ≤ y := le_trans (by decide : (1 : ℕ) ≤ 256) hy
  have hcell := gapped_ee_cell (n := n) (a := a) (b := b) hy1 hC
  have hk : 6 ≤ b + 2 := by omega
  have htail := shared_two_even_tail (n := y) hy hk
  have hle : (n + 1) ^ (2 ^ (b + 2)) ≤ (y + 1) ^ (2 ^ (b + 2)) :=
    Nat.pow_le_pow_left (Nat.succ_le_succ hyn) _
  have hlt : y ^ (3 ^ b) <
      2 ^ denomBits b * (y + 1) ^ (2 ^ (b + 2)) :=
    lt_of_lt_of_le hcell (Nat.mul_le_mul_left _ hle)
  have hbits : b + 2 - 2 = b := Nat.add_sub_cancel b 2
  have htail' : 2 ^ denomBits b * (y + 1) ^ (2 ^ (b + 2)) < y ^ (3 ^ b) := by
    simpa [hbits] using htail
  exact (not_lt_of_gt htail') hlt

theorem no_cycleMin_gapped_three_even_eoe_of_y {n a b : ℕ}
    (hn : 2 ≤ n) (hb : 3 ≤ b) (h : CycleMin n (gappedThreeEvenEOE a b))
    (hy : 256 ≤ image n (firstEPrefix a)) : False := by
  set y := image n (firstEPrefix a)
  have hC : CycleWord n (gappedThreeEvenEOE a b) := cycleMin_cycleWord h
  have hyn : n ≤ y := cycleMin_gapped_eoe_y_ge h
  have hy1 : 1 ≤ y := le_trans (by decide : (1 : ℕ) ≤ 256) hy
  have hcell := gapped_eoe_cell hn hy1 hC
  have hk : 6 ≤ b + 3 := by omega
  have htail := shared_two_even_tail (n := y) hy hk
  have hle : (n + 1) ^ (2 ^ (b + 3)) ≤ (y + 1) ^ (2 ^ (b + 3)) :=
    Nat.pow_le_pow_left (Nat.succ_le_succ hyn) _
  have hlt : y ^ (3 ^ (b + 1)) <
      2 ^ denomBits (b + 1) * (y + 1) ^ (2 ^ (b + 3)) :=
    lt_of_lt_of_le hcell (Nat.mul_le_mul_left _ hle)
  have hbits : b + 3 - 2 = b + 1 := by omega
  have htail' :
      2 ^ denomBits (b + 1) * (y + 1) ^ (2 ^ (b + 3)) <
        y ^ (3 ^ (b + 1)) := by
    simpa [hbits] using htail
  exact (not_lt_of_gt htail') hlt

theorem gapped_ee_prefix_seven_odds {n a b : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (gappedThreeEvenEE a b)) :
    follows n sevenOdds := by
  have hP := follows_gapped_ee_prefix h.1
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left (v := [Branch.even])
      (by simpa [firstEPrefix] using hP)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem gapped_eoe_prefix_seven_odds {n a b : ℕ}
    (ha : 7 ≤ a) (h : CycleWord n (gappedThreeEvenEOE a b)) :
    follows n sevenOdds := by
  have hP := follows_gapped_eoe_prefix h.1
  have hO : follows n (List.replicate a Branch.odd) :=
    follows_of_append_left (v := [Branch.even])
      (by simpa [firstEPrefix] using hP)
  have hsplit : List.replicate a Branch.odd =
      sevenOdds ++ List.replicate (a - 7) Branch.odd := by
    have hsum : 7 + (a - 7) = a := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (a - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem gapped_ee_remaining_seven_odds {n a b : ℕ}
    (hb : 7 ≤ b) (h : CycleWord n (gappedThreeEvenEE a b)) :
    follows (image n (firstEPrefix a)) sevenOdds := by
  have hO := follows_gapped_ee_remaining_odds h.1
  have hsplit : List.replicate b Branch.odd =
      sevenOdds ++ List.replicate (b - 7) Branch.odd := by
    have hsum : 7 + (b - 7) = b := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (b - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem gapped_eoe_remaining_seven_odds {n a b : ℕ}
    (hb : 7 ≤ b) (h : CycleWord n (gappedThreeEvenEOE a b)) :
    follows (image n (firstEPrefix a)) sevenOdds := by
  have hO := follows_gapped_eoe_remaining_odds h.1
  have hsplit : List.replicate b Branch.odd =
      sevenOdds ++ List.replicate (b - 7) Branch.odd := by
    have hsum : 7 + (b - 7) = b := by omega
    rw [sevenOdds, ← List.replicate_add, hsum]
  exact follows_of_append_left (v := List.replicate (b - 7) Branch.odd)
    (by simpa [hsplit] using hO)

theorem no_cycle_word_gapped_ee_short_of_lt {n a b : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha2 : 2 ≤ a) (ha6 : a ≤ 6)
    (hb4 : 4 ≤ b) (hb6 : b ≤ 6)
    (h : CycleWord n (gappedThreeEvenEE a b)) : False := by
  have hA : a - 2 < 5 := by omega
  have hB : b - 4 < 3 := by omega
  have hfalse :
      cycleWordB n (gappedThreeEvenEE (a - 2 + 2) (b - 4 + 4)) = false :=
    cycleWordB_gapped_ee_short_lt256 ⟨n, hn⟩ ⟨a - 2, hA⟩ ⟨b - 4, hB⟩ hn2
  have ha : a - 2 + 2 = a := by omega
  have hb : b - 4 + 4 = b := by omega
  have hfalse' : cycleWordB n (gappedThreeEvenEE a b) = false := by
    simpa [ha, hb] using hfalse
  have htrue : cycleWordB n (gappedThreeEvenEE a b) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycle_word_gapped_eoe_short_of_lt {n a b : ℕ}
    (hn2 : 2 ≤ n) (hn : n < 256) (ha2 : 2 ≤ a) (ha6 : a ≤ 6)
    (hb3 : 3 ≤ b) (hb6 : b ≤ 6)
    (h : CycleWord n (gappedThreeEvenEOE a b)) : False := by
  have hA : a - 2 < 5 := by omega
  have hB : b - 3 < 4 := by omega
  have hfalse :
      cycleWordB n (gappedThreeEvenEOE (a - 2 + 2) (b - 3 + 3)) = false :=
    cycleWordB_gapped_eoe_short_lt256 ⟨n, hn⟩ ⟨a - 2, hA⟩ ⟨b - 3, hB⟩ hn2
  have ha : a - 2 + 2 = a := by omega
  have hb : b - 3 + 3 = b := by omega
  have hfalse' : cycleWordB n (gappedThreeEvenEOE a b) = false := by
    simpa [ha, hb] using hfalse
  have htrue : cycleWordB n (gappedThreeEvenEOE a b) = true :=
    cycleWordB_iff.mpr h
  rw [hfalse'] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycleMin_gapped_three_even_ee_of_lt {n a b : ℕ}
    (hn : 2 ≤ n) (hnlt : n < 256) (ha : 2 ≤ a) (hb : 4 ≤ b)
    (h : CycleMin n (gappedThreeEvenEE a b)) : False := by
  have hC : CycleWord n (gappedThreeEvenEE a b) := cycleMin_cycleWord h
  cases lt_or_ge a 7 with
  | inr ha7 =>
      exact no_follows_seven_odds_of_lt256 hn hnlt
        (gapped_ee_prefix_seven_odds ha7 hC)
  | inl ha6 =>
      have hP := follows_gapped_ee_prefix hC.1
      have ha1 : 1 ≤ a := le_trans (by decide : (1 : ℕ) ≤ 2) ha
      set y := image n (firstEPrefix a)
      cases lt_or_ge y 256 with
      | inr hyge =>
          exact no_cycleMin_gapped_three_even_ee_of_y hb h hyge
      | inl hylt =>
          have hy2 : 2 ≤ y := firstEPrefix_image_ge_two hn ha1 hP
          cases lt_or_ge b 7 with
          | inr hb7 =>
              exact no_follows_seven_odds_of_lt256 hy2 hylt
                (gapped_ee_remaining_seven_odds hb7 hC)
          | inl hb6 =>
              exact no_cycle_word_gapped_ee_short_of_lt hn hnlt ha
                (Nat.le_of_lt_succ ha6) hb (Nat.le_of_lt_succ hb6) hC

theorem no_cycleMin_gapped_three_even_eoe_of_lt {n a b : ℕ}
    (hn : 2 ≤ n) (hnlt : n < 256) (ha : 2 ≤ a) (hb : 3 ≤ b)
    (h : CycleMin n (gappedThreeEvenEOE a b)) : False := by
  have hC : CycleWord n (gappedThreeEvenEOE a b) := cycleMin_cycleWord h
  cases lt_or_ge a 7 with
  | inr ha7 =>
      exact no_follows_seven_odds_of_lt256 hn hnlt
        (gapped_eoe_prefix_seven_odds ha7 hC)
  | inl ha6 =>
      have hP := follows_gapped_eoe_prefix hC.1
      have ha1 : 1 ≤ a := le_trans (by decide : (1 : ℕ) ≤ 2) ha
      set y := image n (firstEPrefix a)
      cases lt_or_ge y 256 with
      | inr hyge =>
          exact no_cycleMin_gapped_three_even_eoe_of_y hn hb h hyge
      | inl hylt =>
          have hy2 : 2 ≤ y := firstEPrefix_image_ge_two hn ha1 hP
          cases lt_or_ge b 7 with
          | inr hb7 =>
              exact no_follows_seven_odds_of_lt256 hy2 hylt
                (gapped_eoe_remaining_seven_odds hb7 hC)
          | inl hb6 =>
              exact no_cycle_word_gapped_eoe_short_of_lt hn hnlt ha
                (Nat.le_of_lt_succ ha6) hb (Nat.le_of_lt_succ hb6) hC

theorem no_cycleMin_gapped_three_even_ee {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 4 ≤ b) :
    ¬CycleMin n
      (List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++ [Branch.even, Branch.even]) := by
  intro h
  have hw : gappedThreeEvenEE a b =
      List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++ [Branch.even, Branch.even] := by
    simp [gappedThreeEvenEE, firstEPrefix, List.append_assoc]
  have h' : CycleMin n (gappedThreeEvenEE a b) := by
    simpa [hw] using h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycleMin_gapped_three_even_ee_of_lt hn hlt ha hb h'
  | inr hge =>
      have hy : 256 ≤ image n (firstEPrefix a) :=
        le_trans hge (cycleMin_gapped_ee_y_ge h')
      exact no_cycleMin_gapped_three_even_ee_of_y hb h' hy

theorem no_cycleMin_gapped_three_even_eoe {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 3 ≤ b) :
    ¬CycleMin n
      (List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++
        [Branch.even, Branch.odd, Branch.even]) := by
  intro h
  have hw : gappedThreeEvenEOE a b =
      List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++
        [Branch.even, Branch.odd, Branch.even] := by
    simp [gappedThreeEvenEOE, firstEPrefix, List.append_assoc]
  have h' : CycleMin n (gappedThreeEvenEOE a b) := by
    simpa [hw] using h
  cases lt_or_ge n 256 with
  | inl hlt => exact no_cycleMin_gapped_three_even_eoe_of_lt hn hlt ha hb h'
  | inr hge =>
      have hy : 256 ≤ image n (firstEPrefix a) :=
        le_trans hge (cycleMin_gapped_eoe_y_ge h')
      exact no_cycleMin_gapped_three_even_eoe_of_y hn hb h' hy

end Problems.Juggler
