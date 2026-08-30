import Problems.Juggler.FirstETransport

namespace Problems.Juggler

/-!
# Gapped three-even leftovers as `CycleWord`s

First-E transport excludes the gapped leftovers only as `CycleMin`s.
Every rotation is already an excluded `CycleMin` orientation, so
`exists_cycleMin` upgrades both families to `CycleWord`.

Not a length-8 or length-9 census and not a halt theorem. Paper A
records the families as Theorem 3.21.
-/

theorem gapped_rotateWord_eq_drop_append_take :
    ∀ (w : List Branch) (k : ℕ), k ≤ w.length →
      rotateWord w k = w.drop k ++ w.take k
  | _w, 0, _ => by simp [rotateWord]
  | [], k + 1, hk => by simp at hk
  | b :: rest, k + 1, hk => by
      have hkr : k ≤ rest.length := by
        simp only [List.length_cons] at hk
        omega
      have hk' : k ≤ (rest ++ [b]).length := by
        simp only [List.length_append, List.length_cons, List.length_nil]
        omega
      show rotateWord (rest ++ [b]) k =
        (b :: rest).drop (k + 1) ++ (b :: rest).take (k + 1)
      rw [gapped_rotateWord_eq_drop_append_take (rest ++ [b]) k hk']
      rw [List.drop_append_of_le_length hkr,
        List.take_append_of_le_length hkr]
      simp [List.append_assoc]

theorem rotateWord_cons {w : List Branch} {k : ℕ} (hk : k < w.length) :
    rotateWord w k = w[k] :: (w.drop (k + 1) ++ w.take k) := by
  rw [gapped_rotateWord_eq_drop_append_take w k (Nat.le_of_lt hk),
    List.drop_eq_getElem_cons hk, List.cons_append]

theorem rotateWord_cons_cons {w : List Branch} {k : ℕ}
    (hk : k + 1 < w.length) :
    rotateWord w k =
      w[k] :: w[k + 1] :: (w.drop (k + 2) ++ w.take k) := by
  have hk0 : k < w.length := Nat.lt_of_succ_lt hk
  rw [rotateWord_cons hk0, List.drop_eq_getElem_cons hk, List.cons_append]

theorem take_snoc {w : List Branch} {k : ℕ}
    (hk0 : 0 < k) (hk : k ≤ w.length) :
    w.take k = w.take (k - 1) ++
      [w[k - 1]'(Nat.lt_of_lt_of_le (Nat.sub_one_lt_of_lt hk0) hk)] := by
  have hi : k - 1 < w.length :=
    Nat.lt_of_lt_of_le (Nat.sub_one_lt_of_lt hk0) hk
  have h := List.take_succ_eq_append_getElem (l := w) (i := k - 1) hi
  have hsucc : k - 1 + 1 = k := Nat.sub_add_cancel (Nat.succ_le_of_lt hk0)
  rw [hsucc] at h
  exact h

theorem rotateWord_snoc {w : List Branch} {k : ℕ}
    (hk0 : 0 < k) (hk : k ≤ w.length) :
    rotateWord w k =
      (w.drop k ++ w.take (k - 1)) ++
        [w[k - 1]'(Nat.lt_of_lt_of_le (Nat.sub_one_lt_of_lt hk0) hk)] := by
  rw [gapped_rotateWord_eq_drop_append_take w k hk, take_snoc hk0 hk,
    List.append_assoc]

theorem cycleMin_of_rotate_ends_odd {n : ℕ} {w : List Branch} {k : ℕ}
    (hn : 2 ≤ n) (hk0 : 0 < k) (hk : k ≤ w.length)
    (hodd : w[k - 1]'(Nat.lt_of_lt_of_le (Nat.sub_one_lt_of_lt hk0) hk) =
      Branch.odd)
    (h : CycleMin n (rotateWord w k)) : False := by
  rw [rotateWord_snoc hk0 hk, hodd] at h
  exact cycleMin_not_end_odd hn h

theorem cycleMin_rotate_start_even {n : ℕ} {w : List Branch} {k : ℕ}
    (hn : 2 ≤ n) (hk : k < w.length)
    (he : w[k] = Branch.even)
    (h : CycleMin n (rotateWord w k)) : False := by
  rw [rotateWord_cons hk, he] at h
  exact cycleMin_not_start_even hn h

theorem cycleMin_rotate_start_OE {n : ℕ} {w : List Branch} {k : ℕ}
    (hn : 2 ≤ n) (hk : k + 1 < w.length)
    (ho : w[k] = Branch.odd) (he : w[k + 1] = Branch.even)
    (h : CycleMin n (rotateWord w k)) : False := by
  rw [rotateWord_cons_cons hk, ho, he] at h
  exact cycleMin_not_odd_even hn h

theorem getElem_of_list_eq {w w' : List Branch} (h : w = w') {i : ℕ}
    (hi : i < w.length) :
    w[i] = w'[i]'(by rw [← h]; exact hi) := by
  subst h; rfl

theorem getElem_nat_eq {w : List Branch} {i j : ℕ} (h : i = j)
    (hi : i < w.length) :
    w[i] = w[j]'(by rw [← h]; exact hi) := by
  subst h; rfl

theorem gapped_ee_as_prefix (a b : ℕ) :
    gappedThreeEvenEE a b =
      firstEPrefix a ++
        (List.replicate b Branch.odd ++ [Branch.even, Branch.even]) := by
  simp [gappedThreeEvenEE]

theorem gapped_eoe_as_prefix (a b : ℕ) :
    gappedThreeEvenEOE a b =
      firstEPrefix a ++
        (List.replicate b Branch.odd ++
          [Branch.even, Branch.odd, Branch.even]) := by
  simp [gappedThreeEvenEOE]

theorem gapped_ee_expanded (a b : ℕ) :
    gappedThreeEvenEE a b =
      List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++ [Branch.even, Branch.even] := by
  simp [gappedThreeEvenEE, firstEPrefix, List.append_assoc]

theorem gapped_eoe_expanded (a b : ℕ) :
    gappedThreeEvenEOE a b =
      List.replicate a Branch.odd ++ [Branch.even] ++
        List.replicate b Branch.odd ++
        [Branch.even, Branch.odd, Branch.even] := by
  simp [gappedThreeEvenEOE, firstEPrefix, List.append_assoc]

theorem firstEPrefix_get_lt {a i : ℕ} (hia : i < a) :
    (firstEPrefix a)[i]'(by simp [firstEPrefix_length]; omega) =
      Branch.odd := by
  have hiL : i < (List.replicate a Branch.odd).length := by
    simp [List.length_replicate]; exact hia
  simp [firstEPrefix, List.getElem_append_left hiL, List.getElem_replicate]

theorem firstEPrefix_get_last (a : ℕ) :
    (firstEPrefix a)[a]'(by simp [firstEPrefix_length]) = Branch.even := by
  have hge : (List.replicate a Branch.odd).length ≤ a := by
    simp [List.length_replicate]
  simp [firstEPrefix, List.getElem_append_right hge]

theorem gappedThreeEvenEE_get_lt_a {a b i : ℕ} (hia : i < a) :
    (gappedThreeEvenEE a b)[i]'(by
        have := gappedThreeEvenEE_length a b; omega) =
      Branch.odd := by
  have hi : i < (gappedThreeEvenEE a b).length := by
    have := gappedThreeEvenEE_length a b; omega
  have hiL : i < (firstEPrefix a).length := by
    simp [firstEPrefix_length]; omega
  rw [getElem_of_list_eq (gapped_ee_as_prefix a b) hi,
    List.getElem_append_left hiL]
  exact firstEPrefix_get_lt hia

theorem gappedThreeEvenEE_get_a {a b : ℕ} :
    (gappedThreeEvenEE a b)[a]'(by
        have := gappedThreeEvenEE_length a b; omega) =
      Branch.even := by
  have hi : a < (gappedThreeEvenEE a b).length := by
    have := gappedThreeEvenEE_length a b; omega
  have hiL : a < (firstEPrefix a).length := by
    simp [firstEPrefix_length]
  rw [getElem_of_list_eq (gapped_ee_as_prefix a b) hi,
    List.getElem_append_left hiL]
  exact firstEPrefix_get_last a

theorem gappedThreeEvenEE_get_mid {a b i : ℕ}
    (hgt : a < i) (hlt : i < a + b + 1) :
    (gappedThreeEvenEE a b)[i]'(by
        have := gappedThreeEvenEE_length a b; omega) =
      Branch.odd := by
  have hi : i < (gappedThreeEvenEE a b).length := by
    have := gappedThreeEvenEE_length a b; omega
  have hge : (firstEPrefix a).length ≤ i := by
    simp [firstEPrefix_length]; omega
  have hiL : i - (a + 1) < (List.replicate b Branch.odd).length := by
    simp [List.length_replicate]; omega
  rw [getElem_of_list_eq (gapped_ee_as_prefix a b) hi,
    List.getElem_append_right hge]
  simp [firstEPrefix_length, List.getElem_append_left hiL,
    List.getElem_replicate]

theorem gappedThreeEvenEE_get_last {a b : ℕ} :
    (gappedThreeEvenEE a b)[a + b + 2]'(by
        have := gappedThreeEvenEE_length a b; omega) =
      Branch.even := by
  have hi : a + b + 2 < (gappedThreeEvenEE a b).length := by
    have := gappedThreeEvenEE_length a b; omega
  have hge : (firstEPrefix a).length ≤ a + b + 2 := by
    simp [firstEPrefix_length]; omega
  have hge2 : (List.replicate b Branch.odd).length ≤ b + 1 := by
    simp [List.length_replicate]
  have hidx : a + b + 2 - (firstEPrefix a).length = b + 1 := by
    rw [firstEPrefix_length]; omega
  have hiR : a + b + 2 - (firstEPrefix a).length <
      (List.replicate b Branch.odd ++ [Branch.even, Branch.even]).length := by
    simp [List.length_replicate]; omega
  rw [getElem_of_list_eq (gapped_ee_as_prefix a b) hi,
    List.getElem_append_right hge, getElem_nat_eq hidx hiR,
    List.getElem_append_right hge2]
  simp [List.length_replicate]

theorem gappedThreeEvenEE_pred_odd {a b k : ℕ}
    (hk0 : 0 < k) (hk : k < a + b + 3) (hne1 : k ≠ a + 1)
    (hne2 : k ≠ a + b + 2) :
    (gappedThreeEvenEE a b)[k - 1]'(by
        have := gappedThreeEvenEE_length a b; omega) =
      Branch.odd := by
  cases lt_or_ge (k - 1) a with
  | inl hlt => exact gappedThreeEvenEE_get_lt_a hlt
  | inr hge =>
      have hgt : a < k - 1 := lt_of_le_of_ne hge (by omega)
      exact gappedThreeEvenEE_get_mid hgt (by omega)

theorem gappedThreeEvenEOE_get_lt_a {a b i : ℕ} (hia : i < a) :
    (gappedThreeEvenEOE a b)[i]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.odd := by
  have hi : i < (gappedThreeEvenEOE a b).length := by
    have := gappedThreeEvenEOE_length a b; omega
  have hiL : i < (firstEPrefix a).length := by
    simp [firstEPrefix_length]; omega
  rw [getElem_of_list_eq (gapped_eoe_as_prefix a b) hi,
    List.getElem_append_left hiL]
  exact firstEPrefix_get_lt hia

theorem gappedThreeEvenEOE_get_a {a b : ℕ} :
    (gappedThreeEvenEOE a b)[a]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.even := by
  have hi : a < (gappedThreeEvenEOE a b).length := by
    have := gappedThreeEvenEOE_length a b; omega
  have hiL : a < (firstEPrefix a).length := by
    simp [firstEPrefix_length]
  rw [getElem_of_list_eq (gapped_eoe_as_prefix a b) hi,
    List.getElem_append_left hiL]
  exact firstEPrefix_get_last a

theorem gappedThreeEvenEOE_get_mid {a b i : ℕ}
    (hgt : a < i) (hlt : i < a + b + 1) :
    (gappedThreeEvenEOE a b)[i]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.odd := by
  have hi : i < (gappedThreeEvenEOE a b).length := by
    have := gappedThreeEvenEOE_length a b; omega
  have hge : (firstEPrefix a).length ≤ i := by
    simp [firstEPrefix_length]; omega
  have hiL : i - (a + 1) < (List.replicate b Branch.odd).length := by
    simp [List.length_replicate]; omega
  rw [getElem_of_list_eq (gapped_eoe_as_prefix a b) hi,
    List.getElem_append_right hge]
  simp [firstEPrefix_length, List.getElem_append_left hiL,
    List.getElem_replicate]

theorem gappedThreeEvenEOE_get_o {a b : ℕ} :
    (gappedThreeEvenEOE a b)[a + b + 2]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.odd := by
  have hi : a + b + 2 < (gappedThreeEvenEOE a b).length := by
    have := gappedThreeEvenEOE_length a b; omega
  have hge : (firstEPrefix a).length ≤ a + b + 2 := by
    simp [firstEPrefix_length]; omega
  have hge2 : (List.replicate b Branch.odd).length ≤ b + 1 := by
    simp [List.length_replicate]
  have hidx : a + b + 2 - (firstEPrefix a).length = b + 1 := by
    rw [firstEPrefix_length]; omega
  have hiR : a + b + 2 - (firstEPrefix a).length <
      (List.replicate b Branch.odd ++
        [Branch.even, Branch.odd, Branch.even]).length := by
    simp [List.length_replicate]; omega
  rw [getElem_of_list_eq (gapped_eoe_as_prefix a b) hi,
    List.getElem_append_right hge, getElem_nat_eq hidx hiR,
    List.getElem_append_right hge2]
  simp [List.length_replicate]

theorem gappedThreeEvenEOE_get_last {a b : ℕ} :
    (gappedThreeEvenEOE a b)[a + b + 3]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.even := by
  have hi : a + b + 3 < (gappedThreeEvenEOE a b).length := by
    have := gappedThreeEvenEOE_length a b; omega
  have hge : (firstEPrefix a).length ≤ a + b + 3 := by
    simp [firstEPrefix_length]; omega
  have hge2 : (List.replicate b Branch.odd).length ≤ b + 2 := by
    simp [List.length_replicate]
  have hidx : a + b + 3 - (firstEPrefix a).length = b + 2 := by
    rw [firstEPrefix_length]; omega
  have hiR : a + b + 3 - (firstEPrefix a).length <
      (List.replicate b Branch.odd ++
        [Branch.even, Branch.odd, Branch.even]).length := by
    simp [List.length_replicate]; omega
  rw [getElem_of_list_eq (gapped_eoe_as_prefix a b) hi,
    List.getElem_append_right hge, getElem_nat_eq hidx hiR,
    List.getElem_append_right hge2]
  simp [List.length_replicate]

theorem gappedThreeEvenEOE_pred_odd {a b k : ℕ}
    (hk0 : 0 < k) (hk : k < a + b + 4) (hne1 : k ≠ a + 1)
    (hne2 : k ≠ a + b + 2) :
    (gappedThreeEvenEOE a b)[k - 1]'(by
        have := gappedThreeEvenEOE_length a b; omega) =
      Branch.odd := by
  cases lt_or_ge (k - 1) a with
  | inl hlt => exact gappedThreeEvenEOE_get_lt_a hlt
  | inr hge =>
      have hgt : a < k - 1 := lt_of_le_of_ne hge (by omega)
      cases lt_or_ge (k - 1) (a + b + 1) with
      | inl hlt => exact gappedThreeEvenEOE_get_mid hgt hlt
      | inr hge2 =>
          have : k - 1 = a + b + 2 := by omega
          simpa [this] using gappedThreeEvenEOE_get_o (a := a) (b := b)

def gappedEEBootstrap (a b : ℕ) : List Branch :=
  List.replicate b Branch.odd ++ [Branch.even, Branch.even] ++
    List.replicate a Branch.odd ++ [Branch.even]

def gappedEOEBootstrap (a b : ℕ) : List Branch :=
  List.replicate b Branch.odd ++ [Branch.even, Branch.odd, Branch.even] ++
    List.replicate a Branch.odd ++ [Branch.even]

theorem gappedEEBootstrap_split (a b : ℕ) :
    gappedEEBootstrap a b =
      (List.replicate b Branch.odd ++ [Branch.even]) ++ [Branch.even] ++
        List.replicate a Branch.odd ++ [Branch.even] := by
  simp [gappedEEBootstrap, List.append_assoc]

theorem gappedEOEBootstrap_split (a b : ℕ) :
    gappedEOEBootstrap a b =
      (List.replicate b Branch.odd ++ [Branch.even, Branch.odd]) ++
        [Branch.even] ++ List.replicate a Branch.odd ++ [Branch.even] := by
  simp [gappedEOEBootstrap, List.append_assoc]

theorem gapped_ee_rotate_succ_a {a b : ℕ} :
    rotateWord (gappedThreeEvenEE a b) (a + 1) = gappedEEBootstrap a b := by
  have hlen := gappedThreeEvenEE_length a b
  have hk : a + 1 ≤ (gappedThreeEvenEE a b).length := by rw [hlen]; omega
  have hpre := firstEPrefix_length a
  have hle : a + 1 ≤ (firstEPrefix a).length := Nat.le_of_eq hpre.symm
  have hword := gapped_ee_as_prefix a b
  have hdrop : (firstEPrefix a).drop (a + 1) = [] :=
    List.drop_eq_nil_of_le (Nat.le_of_eq hpre)
  have htake : (firstEPrefix a).take (a + 1) = firstEPrefix a :=
    List.take_of_length_le (Nat.le_of_eq hpre)
  rw [gapped_rotateWord_eq_drop_append_take _ _ hk, hword,
    List.drop_append_of_le_length hle, List.take_append_of_le_length hle,
    hdrop, htake]
  simp [gappedEEBootstrap, firstEPrefix]

theorem gapped_eoe_rotate_succ_a {a b : ℕ} :
    rotateWord (gappedThreeEvenEOE a b) (a + 1) = gappedEOEBootstrap a b := by
  have hlen := gappedThreeEvenEOE_length a b
  have hk : a + 1 ≤ (gappedThreeEvenEOE a b).length := by rw [hlen]; omega
  have hpre := firstEPrefix_length a
  have hle : a + 1 ≤ (firstEPrefix a).length := Nat.le_of_eq hpre.symm
  have hword := gapped_eoe_as_prefix a b
  have hdrop : (firstEPrefix a).drop (a + 1) = [] :=
    List.drop_eq_nil_of_le (Nat.le_of_eq hpre)
  have htake : (firstEPrefix a).take (a + 1) = firstEPrefix a :=
    List.take_of_length_le (Nat.le_of_eq hpre)
  rw [gapped_rotateWord_eq_drop_append_take _ _ hk, hword,
    List.drop_append_of_le_length hle, List.take_append_of_le_length hle,
    hdrop, htake]
  simp [gappedEOEBootstrap, firstEPrefix]

theorem no_followsB_3_four_odds :
    followsB 3 (List.replicate 4 Branch.odd) = false := by
  native_decide

theorem no_follows_three_four_odds :
    ¬follows 3 (List.replicate 4 Branch.odd) := by
  intro hf
  have htrue : followsB 3 (List.replicate 4 Branch.odd) = true :=
    (followsB_iff 3 _).mpr hf
  rw [no_followsB_3_four_odds] at htrue
  exact Bool.false_ne_true htrue

theorem no_follows_three_long_odds {b : ℕ} (hb : 4 ≤ b) :
    ¬follows 3 (List.replicate b Branch.odd) := by
  intro hf
  have hsplit : List.replicate b Branch.odd =
      List.replicate 4 Branch.odd ++ List.replicate (b - 4) Branch.odd := by
    have : 4 + (b - 4) = b := by omega
    rw [← List.replicate_add, this]
  exact no_follows_three_four_odds
    (follows_of_append_left (v := List.replicate (b - 4) Branch.odd)
      (by simpa [hsplit] using hf))

theorem no_followsB_3_eoe_boot3 :
    followsB 3 (gappedEOEBootstrap 2 3) = false := by
  native_decide

theorem no_follows_three_eoe_bootstrap {b : ℕ} (hb : 3 ≤ b) :
    ¬follows 3 (gappedEOEBootstrap 2 b) := by
  intro hf
  cases lt_or_ge b 4 with
  | inr hb4 =>
      exact no_follows_three_long_odds hb4
        (follows_of_append_left
          (v := [Branch.even, Branch.odd, Branch.even] ++
            List.replicate 2 Branch.odd ++ [Branch.even])
          (by simpa [gappedEOEBootstrap] using hf))
  | inl hb3 =>
      have : b = 3 := by omega
      subst this
      have htrue : followsB 3 (gappedEOEBootstrap 2 3) = true :=
        (followsB_iff 3 _).mpr hf
      rw [no_followsB_3_eoe_boot3] at htrue
      exact Bool.false_ne_true htrue

theorem oo_run_suffix_threshold :
    ∀ m, 5 ≤ m → follows m (List.replicate 2 Branch.odd) →
      (m + 1) ^ 2 ≤ image m (List.replicate 2 Branch.odd) := by
  intro m hm hf
  have hlist : List.replicate 2 Branch.odd = [.odd, .odd] := rfl
  rw [hlist] at hf ⊢
  simpa [image_eq_iterate] using oo_suffix_threshold hm hf

theorem no_cycleMin_gapped_ee_bootstrap {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 4 ≤ b)
    (h : CycleMin n (gappedEEBootstrap a b)) : False := by
  have hodd : n % 2 = 1 := cycleMin_start_odd hn h
  have hn3 : 3 ≤ n := by omega
  rw [gappedEEBootstrap_split] at h
  cases lt_or_ge a 3 with
  | inr ha3 =>
      exact no_cycleMin_internal_even_threshold
        (odd_run_suffix_threshold ha3) hn3 h
  | inl ha2 =>
      have : a = 2 := by omega
      subst this
      cases lt_or_ge n 5 with
      | inr hge =>
          exact no_cycleMin_internal_even_threshold
            oo_run_suffix_threshold hge h
      | inl hlt =>
          have : n = 3 := by omega
          subst this
          exact no_follows_three_long_odds hb
            (follows_of_append_left
              (v := [Branch.even, Branch.even] ++
                List.replicate 2 Branch.odd ++ [Branch.even])
              (by simpa [gappedEEBootstrap] using h.1.1))

theorem no_cycleMin_gapped_eoe_bootstrap {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 3 ≤ b)
    (h : CycleMin n (gappedEOEBootstrap a b)) : False := by
  have hodd : n % 2 = 1 := cycleMin_start_odd hn h
  have hn3 : 3 ≤ n := by omega
  rw [gappedEOEBootstrap_split] at h
  cases lt_or_ge a 3 with
  | inr ha3 =>
      exact no_cycleMin_internal_even_threshold
        (odd_run_suffix_threshold ha3) hn3 h
  | inl ha2 =>
      have : a = 2 := by omega
      subst this
      cases lt_or_ge n 5 with
      | inr hge =>
          exact no_cycleMin_internal_even_threshold
            oo_run_suffix_threshold hge h
      | inl hlt =>
          have : n = 3 := by omega
          subst this
          exact no_follows_three_eoe_bootstrap hb
            (by simpa [gappedEOEBootstrap_split] using h.1.1)

theorem no_cycle_word_gapped_three_even_ee {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 4 ≤ b) :
    ¬CycleWord n (gappedThreeEvenEE a b) := by
  intro h
  obtain ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen := gappedThreeEvenEE_length a b
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by simpa [hlen] using hk)
  have hcases :
      k = 0 ∨ k = a + 1 ∨ k = a + b + 2 ∨
        (0 < k ∧ k ≠ a + 1 ∧ k ≠ a + b + 2) := by omega
  rcases hcases with h0 | hsucc | hlast | hmid
  · subst h0
    exact no_cycleMin_gapped_three_even_ee hnk ha hb
      (by simpa [rotateWord, gapped_ee_expanded] using hm)
  · subst hsucc
    exact no_cycleMin_gapped_ee_bootstrap hnk ha hb
      (by simpa [gapped_ee_rotate_succ_a] using hm)
  · subst hlast
    exact cycleMin_rotate_start_even hnk (by simpa [hlen] using hk)
      (gappedThreeEvenEE_get_last (a := a) (b := b)) hm
  · exact cycleMin_of_rotate_ends_odd hnk hmid.1
      (by simpa [hlen] using Nat.le_of_lt hk)
      (gappedThreeEvenEE_pred_odd hmid.1 hk hmid.2.1 hmid.2.2) hm

theorem no_cycle_word_gapped_three_even_eoe {n a b : ℕ}
    (hn : 2 ≤ n) (ha : 2 ≤ a) (hb : 3 ≤ b) :
    ¬CycleWord n (gappedThreeEvenEOE a b) := by
  intro h
  obtain ⟨k, hk, hm⟩ := exists_cycleMin hn h
  have hlen := gappedThreeEvenEOE_length a b
  rw [hlen] at hk
  have hnk : 2 ≤ floorPower^[k] n :=
    cycleWord_iterate_ge_two hn h (by simpa [hlen] using hk)
  have hcases :
      k = 0 ∨ k = a + 1 ∨ k = a + b + 2 ∨
        (0 < k ∧ k ≠ a + 1 ∧ k ≠ a + b + 2) := by omega
  rcases hcases with h0 | hsucc | hO | hmid
  · subst h0
    exact no_cycleMin_gapped_three_even_eoe hnk ha hb
      (by simpa [rotateWord, gapped_eoe_expanded] using hm)
  · subst hsucc
    exact no_cycleMin_gapped_eoe_bootstrap hnk ha hb
      (by simpa [gapped_eoe_rotate_succ_a] using hm)
  · subst hO
    exact cycleMin_rotate_start_OE hnk (by
        have := hlen; omega)
      (gappedThreeEvenEOE_get_o (a := a) (b := b))
      (gappedThreeEvenEOE_get_last (a := a) (b := b)) hm
  · exact cycleMin_of_rotate_ends_odd hnk hmid.1
      (by simpa [hlen] using Nat.le_of_lt hk)
      (gappedThreeEvenEOE_pred_odd hmid.1 hk hmid.2.1 hmid.2.2) hm

end Problems.Juggler
