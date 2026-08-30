import Problems.Juggler.CycleCore
import Problems.Juggler.FirstInternalOO

namespace Problems.Juggler

/-!
# Named CycleMin / CycleWord exclusions

Why particular trajectories cannot be cycles. Cycle foundations
(`CycleWord`, `CycleMin`, extrema, last-even cell) stay in
`CycleCore`. Isolated-prefix algebra stays in `FirstInternalOO`.
This file is not a halt theorem.
-/

def wordOOEOOE : List Branch :=
  [.odd, .odd, .even, .odd, .odd, .even]

def wordOEOOOE : List Branch :=
  [.odd, .even, .odd, .odd, .odd, .even]

theorem wordOOEOOE_split :
    wordOOEOOE = [.odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even] :=
  rfl

theorem wordOEOOOE_is_odd_even :
    wordOEOOOE = .odd :: .even :: [.odd, .odd, .odd, .even] :=
  rfl

theorem no_cycleMin_ooeooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOOEOOE) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  have hn5 : 5 ≤ n := by
    cases lt_or_ge n 5 with
    | inl hlt =>
        have hn3 : n = 3 := by omega
        subst hn3
        have hOOE : follows 3 ([.odd, .odd] ++ [.even]) :=
          follows_of_append_left (by simpa [wordOOEOOE] using h.1.1)
        have he : image 3 [.odd, .odd] % 2 = 0 :=
          (follows_of_append_right (u := [.odd, .odd]) hOOE).1
        have himg : image 3 [.odd, .odd] = 11 := by native_decide
        rw [himg] at he
        exact absurd he (by decide : ¬(11 : ℕ) % 2 = 0)
    | inr hge => exact hge
  have hsplit : CycleMin n ([.odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even]) := by
    simpa [wordOOEOOE] using h
  refine no_cycleMin_internal_even_threshold (N := 5) ?_ hn5 hsplit
  intro m hm hf
  simpa [image_eq_iterate] using oo_suffix_threshold hm hf

theorem no_cycleMin_oeoooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOEOOOE) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  have hn3 : 3 ≤ n := by omega
  have hsplit : CycleMin n ([.odd] ++ [.even] ++ [.odd, .odd, .odd] ++ [.even]) := by
    simpa [wordOEOOOE] using h
  refine no_cycleMin_internal_even_threshold (N := 3) ?_ hn3 hsplit
  intro m hm hf
  simpa [image_eq_iterate] using ooo_suffix_threshold hm hf

theorem rotate_ooeooe :
    ∀ k, k < 6 →
      rotateWord wordOOEOOE k = wordOOEOOE ∨
        rotateWord wordOOEOOE k = [.odd, .even, .odd, .odd, .even, .odd] ∨
          rotateWord wordOOEOOE k = [.even, .odd, .odd, .even, .odd, .odd] := by
  intro k hk
  interval_cases k <;> simp [wordOOEOOE, rotateWord]

theorem no_cycle_word_ooeooe {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n wordOOEOOE := by
  intro h
  have ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen : wordOOEOOE.length = 6 := rfl
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by omega)
  rcases rotate_ooeooe k hk with h0 | h1 | h2
  · exact no_cycleMin_ooeooe hnk (by simpa [h0] using hm)
  · exact cycleMin_not_odd_even hnk (by simpa [h1] using hm)
  · exact cycleMin_not_start_even hnk (by simpa [h2] using hm)

def wordOOEOOOE : List Branch :=
  [.odd, .odd, .even, .odd, .odd, .odd, .even]

def wordOOOEOOE : List Branch :=
  [.odd, .odd, .odd, .even, .odd, .odd, .even]

theorem wordOOEOOOE_split :
    wordOOEOOOE =
      [.odd, .odd] ++ [.even] ++ [.odd, .odd, .odd] ++ [.even] :=
  rfl

theorem wordOOOEOOE_split :
    wordOOOEOOE =
      [.odd, .odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even] :=
  rfl

theorem no_cycleMin_ooeoooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOOEOOOE) : False := by
  have hn3 : 3 ≤ n := by
    have : n % 2 = 1 := h.1.1.1
    omega
  have hsplit :
      CycleMin n ([.odd, .odd] ++ [.even] ++ [.odd, .odd, .odd] ++ [.even]) := by
    simpa [wordOOEOOOE] using h
  refine no_cycleMin_internal_even_threshold (N := 3) ?_ hn3 hsplit
  intro m hm hf
  simpa [image_eq_iterate] using ooo_suffix_threshold hm hf

theorem no_followsB_3_oooeooe : followsB 3 wordOOOEOOE = false := by
  native_decide

theorem no_follows_3_oooeooe : ¬follows 3 wordOOOEOOE := by
  intro hf
  have htrue : followsB 3 wordOOOEOOE = true := (followsB_iff 3 _).mpr hf
  rw [no_followsB_3_oooeooe] at htrue
  exact Bool.false_ne_true htrue

theorem no_cycleMin_oooeooe {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOOOEOOE) : False := by
  have hodd : n % 2 = 1 := h.1.1.1
  cases lt_or_ge n 5 with
  | inl hlt =>
      have hn3 : n = 3 := by omega
      subst hn3
      exact no_follows_3_oooeooe h.1.1
  | inr hge =>
      have hsplit :
          CycleMin n
            ([.odd, .odd, .odd] ++ [.even] ++ [.odd, .odd] ++ [.even]) := by
        simpa [wordOOOEOOE] using h
      refine no_cycleMin_internal_even_threshold (N := 5) ?_ hge hsplit
      intro m hm hf
      simpa [image_eq_iterate] using oo_suffix_threshold hm hf

theorem rotate_ooeoooe :
    ∀ k, k < 7 →
      rotateWord wordOOEOOOE k = wordOOEOOOE ∨
        rotateWord wordOOEOOOE k = wordOOOEOOE ∨
          rotateWord wordOOEOOOE k =
              [.odd, .even, .odd, .odd, .odd, .even, .odd] ∨
            rotateWord wordOOEOOOE k =
                [.even, .odd, .odd, .odd, .even, .odd, .odd] ∨
              rotateWord wordOOEOOOE k =
                  [.odd, .odd, .even, .odd, .odd, .even, .odd] ∨
                rotateWord wordOOEOOOE k =
                    [.odd, .even, .odd, .odd, .even, .odd, .odd] ∨
                  rotateWord wordOOEOOOE k =
                    [.even, .odd, .odd, .even, .odd, .odd, .odd] := by
  intro k hk
  interval_cases k <;> simp [wordOOEOOOE, wordOOOEOOE, rotateWord]

theorem rotate_oooeooe :
    ∀ k, k < 7 →
      rotateWord wordOOOEOOE k = wordOOOEOOE ∨
        rotateWord wordOOOEOOE k = wordOOEOOOE ∨
          rotateWord wordOOOEOOE k =
              [.odd, .odd, .even, .odd, .odd, .even, .odd] ∨
            rotateWord wordOOOEOOE k =
                [.odd, .even, .odd, .odd, .even, .odd, .odd] ∨
              rotateWord wordOOOEOOE k =
                  [.even, .odd, .odd, .even, .odd, .odd, .odd] ∨
                rotateWord wordOOOEOOE k =
                    [.odd, .even, .odd, .odd, .odd, .even, .odd] ∨
                  rotateWord wordOOOEOOE k =
                    [.even, .odd, .odd, .odd, .even, .odd, .odd] := by
  intro k hk
  interval_cases k <;> simp [wordOOOEOOE, wordOOEOOOE, rotateWord]

theorem no_cycle_word_ooeoooe {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n wordOOEOOOE := by
  intro h
  have ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen : wordOOEOOOE.length = 7 := rfl
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by omega)
  rcases rotate_ooeoooe k hk with h0 | h1 | h2 | h3 | h4 | h5 | h6
  · exact no_cycleMin_ooeoooe hnk (by simpa [h0] using hm)
  · exact no_cycleMin_oooeooe hnk (by simpa [h1] using hm)
  · have heq :
        [Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd] =
          [Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.odd, Branch.even] ++
            [Branch.odd] :=
      rfl
    rw [h2, heq] at hm
    exact cycleMin_not_end_odd hnk hm
  · exact cycleMin_not_start_even hnk (by simpa [h3] using hm)
  · have heq :
        [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.odd] =
          [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.even] ++
            [Branch.odd] :=
      rfl
    rw [h4, heq] at hm
    exact cycleMin_not_end_odd hnk hm
  · exact cycleMin_not_odd_even hnk (by simpa [h5] using hm)
  · exact cycleMin_not_start_even hnk (by simpa [h6] using hm)

theorem no_cycle_word_oooeooe {n : ℕ} (hn : 2 ≤ n) :
    ¬CycleWord n wordOOOEOOE := by
  intro h
  have ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen : wordOOOEOOE.length = 7 := rfl
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by omega)
  rcases rotate_oooeooe k hk with h0 | h1 | h2 | h3 | h4 | h5 | h6
  · exact no_cycleMin_oooeooe hnk (by simpa [h0] using hm)
  · exact no_cycleMin_ooeoooe hnk (by simpa [h1] using hm)
  · have heq :
        [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.odd] =
          [Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.even] ++
            [Branch.odd] :=
      rfl
    rw [h2, heq] at hm
    exact cycleMin_not_end_odd hnk hm
  · exact cycleMin_not_odd_even hnk (by simpa [h3] using hm)
  · exact cycleMin_not_start_even hnk (by simpa [h4] using hm)
  · have heq :
        [Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd] =
          [Branch.odd, Branch.even, Branch.odd, Branch.odd, Branch.odd, Branch.even] ++
            [Branch.odd] :=
      rfl
    rw [h5, heq] at hm
    exact cycleMin_not_end_odd hnk hm
  · exact cycleMin_not_start_even hnk (by simpa [h6] using hm)

def wordOOOEOE : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.even]

theorem wordOOOEOE_split :
    wordOOOEOE =
      [Branch.odd, Branch.odd, Branch.odd] ++ [Branch.even] ++
        [Branch.odd] ++ [Branch.even] :=
  rfl

theorem no_cycleMin_ooooeoe_of_sqrt_eq {n : ℕ} (hn : 2 ≤ n)
    (h : CycleMin n wordOOOEOE)
    (hy : image n ([Branch.odd, Branch.odd, Branch.odd] ++ [Branch.even]) = n) :
    False := by
  have hsplit : CycleMin n
      ([Branch.odd, Branch.odd, Branch.odd] ++ [Branch.even] ++
        [Branch.odd] ++ [Branch.even]) := by
    simpa [wordOOOEOE] using h
  exact cycleMin_prefix_ooo_even_sqrt_ne hn hsplit hy

theorem no_cycleMin_isolated_prefix_of_gap {n a r : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (h : CycleMin n (isolatedPrefix a r ++ v)) : False :=
  forbidden_isolated_under_anchor hn (Nat.not_le.mpr hgap)
    (aboveAnchor_of_prefix (aboveAnchor_of_cycleMin h))

/-- An `a₀ = 2` CycleMin cannot complete one isolated `OE` after the
first even letter. The first internal `OO`, if it exists on this
corridor, is immediate (`r = 0`). -/
theorem no_cycleMin_prefix_ooe_oe {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (isolatedPrefix 2 1 ++ v)) : False :=
  no_cycleMin_isolated_prefix_of_gap hn two_one_isolated_scale_gap h

/-- Cycle application of the shared `r ≤ R(2)` bound. -/
theorem cycleMin_isolated_two {n r : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (isolatedPrefix 2 r ++ v)) : r = 0 :=
  aboveAnchor_isolated_two hn
    (aboveAnchor_of_prefix (aboveAnchor_of_cycleMin h))

end Problems.Juggler
