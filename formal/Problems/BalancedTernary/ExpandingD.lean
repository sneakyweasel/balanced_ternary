import BTCalculus.Integral
import BTCalculus.Normalization

namespace Problems.BalancedTernary

open BTCalculus
open Representation.Words

/-!
Expanding map ``T(n) = 3n - lsd(n)``. This is not laboratory ``DZ``.
Canonical ``T`` is the section ``n ↦ -lsd(n) + 3n``. The LSD
observable of the ``T``-orbit is exactly the current LSD.
-/

def expandingD (n : ℤ) : ℤ :=
  3 * n - lsdZ n

def expandingDGain (gain n : ℤ) : ℤ :=
  3 * n - gain * lsdZ n

theorem expandingD_eq_IZ_shape (n : ℤ) :
    expandingD n = -lsdZ n + 3 * n := by
  unfold expandingD
  ring

theorem expandingD_mod (n : ℤ) : expandingD n ≡ -lsdZ n [ZMOD 3] := by
  unfold expandingD
  refine Int.modEq_iff_dvd.mpr ⟨-n, by ring⟩

theorem neg_lsdZ_is_trit (n : ℤ) :
    -lsdZ n = -1 ∨ -lsdZ n = 0 ∨ -lsdZ n = 1 := by
  rcases lsdZ_is_trit n with h | h | h <;> simp [h]

theorem lsdZ_expandingD (n : ℤ) : lsdZ (expandingD n) = -lsdZ n :=
  lsdZ_unique (neg_lsdZ_is_trit n) (expandingD_mod n)

theorem expandingD_decomp (n : ℤ) :
    expandingD n = 9 * DZ n + 2 * lsdZ n := by
  unfold expandingD
  have h := decomp n
  linarith

theorem DZ_expandingD (n : ℤ) : DZ (expandingD n) = n := by
  have hdecomp := decomp (expandingD n)
  have hlsd := lsdZ_expandingD n
  have hexpr : expandingD n = 3 * n - lsdZ n := rfl
  linarith

theorem expandingD_IZ (a : Representation.Words.Trit) (x : ℤ) :
    expandingD (IZ a x) = 9 * x + 2 * a.toInt := by
  unfold expandingD
  rw [lsdZ_IZ]
  unfold IZ
  ring

theorem lsdZ_expandingD_IZ (a : Representation.Words.Trit) (x : ℤ) :
    lsdZ (expandingD (IZ a x)) = -a.toInt := by
  rw [lsdZ_expandingD, lsdZ_IZ]

theorem lsdZ_iterate_expandingD (k : ℕ) (n : ℤ) :
    lsdZ (expandingD^[k] n) = (-1 : ℤ) ^ k * lsdZ n := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply', lsdZ_expandingD, ih]
    ring

theorem expandingD_gt_of_pos {n : ℤ} (hn : 0 < n) : n < expandingD n := by
  have hr := lsdZ_is_trit n
  unfold expandingD
  rcases hr with h | h | h <;> nlinarith

theorem expandingD_lt_of_neg {n : ℤ} (hn : n < 0) : expandingD n < n := by
  have hr := lsdZ_is_trit n
  unfold expandingD
  rcases hr with h | h | h <;> nlinarith

theorem expandingD_abs_lt {n : ℤ} (hn : n ≠ 0) :
    |n| < |expandingD n| := by
  rcases lt_trichotomy n 0 with hneg | h0 | hpos
  · have ht := expandingD_lt_of_neg hneg
    have hT : expandingD n < 0 := lt_trans ht hneg
    rw [abs_of_neg hneg, abs_of_neg hT]
    omega
  · exact (hn h0).elim
  · have ht := expandingD_gt_of_pos hpos
    have hT : 0 < expandingD n := lt_trans hpos ht
    rw [abs_of_pos hpos, abs_of_pos hT]
    exact ht

theorem expandingD_expands {n : ℤ} (hn : n ≠ 0) :
    n.natAbs < (expandingD n).natAbs := by
  have h := expandingD_abs_lt hn
  have : (n.natAbs : ℤ) < ((expandingD n).natAbs : ℤ) := by
    simpa [Int.natCast_natAbs] using h
  exact Int.ofNat_lt.mp this

theorem expandingD_one : expandingD 1 = 2 := by native_decide

theorem magnitude_contraction_false :
    ¬ ∀ n : ℤ, (expandingD n).natAbs ≤ n.natAbs := by
  intro h
  have := h 1
  rw [expandingD_one] at this
  exact (by native_decide : ¬ (2 : ℕ) ≤ 1) this

theorem expandingDGain_one (n : ℤ) : expandingDGain 1 n = expandingD n := by
  unfold expandingDGain expandingD
  ring

theorem expandingDGain_two_mod (n : ℤ) :
    expandingDGain 2 n ≡ lsdZ n [ZMOD 3] := by
  unfold expandingDGain
  refine Int.modEq_iff_dvd.mpr ⟨lsdZ n - n, by ring⟩

theorem lsdZ_expandingDGain_two (n : ℤ) :
    lsdZ (expandingDGain 2 n) = lsdZ n :=
  lsdZ_unique (lsdZ_is_trit n) (expandingDGain_two_mod n)

theorem expandingDGain_three_eq (n : ℤ) : expandingDGain 3 n = 9 * DZ n := by
  unfold expandingDGain
  have h := decomp n
  linarith

theorem lsdZ_expandingDGain_three (n : ℤ) :
    lsdZ (expandingDGain 3 n) = 0 := by
  rw [expandingDGain_three_eq]
  apply lsdZ_unique (Or.inr (Or.inl rfl))
  refine Int.modEq_iff_dvd.mpr ⟨-3 * DZ n, by ring⟩

theorem expandingD_three_signatures :
    lsdZ (expandingD 0) = 0 ∧
      lsdZ (expandingD 1) = -1 ∧
      lsdZ (expandingD (-1)) = 1 := by
  rw [lsdZ_expandingD, lsdZ_expandingD, lsdZ_expandingD]
  native_decide

theorem lsdZ_of_isTrit {a : ℤ} (ha : isTrit a) : lsdZ a = a :=
  lsdZ_unique ha (Int.ModEq.refl a)

theorem neg_isTrit {r : ℤ} (hr : isTrit r) : isTrit (-r) := by
  rcases hr with h | h | h <;> simp [isTrit, h]

theorem expandingD_residue_T {r : ℤ} (hr : isTrit r) :
    isTrit (lsdZ (expandingD r)) := by
  rw [lsdZ_expandingD, lsdZ_of_isTrit hr]
  exact neg_isTrit hr

theorem expandingD_residue_I (a : Representation.Words.Trit) :
    isTrit a.toInt :=
  trit_toInt_is_trit a

theorem expandingD_residue_closure :
    (∀ r : ℤ, isTrit r → isTrit (lsdZ (expandingD r))) ∧
      (∀ a : Representation.Words.Trit, isTrit a.toInt) :=
  ⟨fun _ hr => expandingD_residue_T hr, expandingD_residue_I⟩

def jet2 (n : ℤ) : ℤ × ℤ :=
  (lsdZ n, lsdZ (DZ n))

theorem jet2_expandingD (n : ℤ) :
    jet2 (expandingD n) = (-lsdZ n, lsdZ n) := by
  unfold jet2
  rw [lsdZ_expandingD, DZ_expandingD]

theorem jet2_IZ (a : Representation.Words.Trit) (x : ℤ) :
    jet2 (IZ a x) = (a.toInt, lsdZ x) := by
  unfold jet2
  rw [lsdZ_IZ, D_after_I]

theorem jet2_of_window {a b : ℤ} (ha : isTrit a) (hb : isTrit b) :
    jet2 (a + 3 * b) = (a, b) := by
  unfold jet2
  have hlsd : lsdZ (a + 3 * b) = a :=
    lsdZ_unique ha (Int.modEq_iff_dvd.mpr ⟨-b, by ring⟩)
  have hdz : DZ (a + 3 * b) = b := by
    have hde := decomp (a + 3 * b)
    rw [hlsd] at hde
    linarith
  rw [hlsd, hdz, lsdZ_of_isTrit hb]

theorem jet2_residue_closure {a b : ℤ} (ha : isTrit a) (hb : isTrit b) :
    jet2 (expandingD (a + 3 * b)) = (-a, a) := by
  have hn := jet2_of_window ha hb
  have hlsd : lsdZ (a + 3 * b) = a := by
    have := congrArg Prod.fst hn
    simpa [jet2] using this
  rw [jet2_expandingD, hlsd]

theorem lsdZ_mul3 (m : ℤ) : lsdZ (3 * m) = 0 :=
  lsdZ_unique (Or.inr (Or.inl rfl)) (Int.modEq_iff_dvd.mpr ⟨-m, by ring⟩)

theorem DZ_expandingDGain_two (n : ℤ) :
    DZ (expandingDGain 2 n) = 3 * DZ n := by
  have hde := decomp (expandingDGain 2 n)
  rw [lsdZ_expandingDGain_two] at hde
  have hn := decomp n
  unfold expandingDGain at *
  linarith

theorem jet2_expandingDGain_two (n : ℤ) :
    jet2 (expandingDGain 2 n) = (lsdZ n, 0) := by
  unfold jet2
  rw [lsdZ_expandingDGain_two, DZ_expandingDGain_two, lsdZ_mul3]

theorem DZ_expandingDGain_three (n : ℤ) :
    DZ (expandingDGain 3 n) = 3 * DZ n := by
  rw [expandingDGain_three_eq]
  have hde := decomp (9 * DZ n)
  have hlsd : lsdZ (9 * DZ n) = 0 := by
    simpa [expandingDGain_three_eq] using lsdZ_expandingDGain_three n
  rw [hlsd] at hde
  linarith

theorem jet2_expandingDGain_three (n : ℤ) :
    jet2 (expandingDGain 3 n) = (0, 0) := by
  unfold jet2
  rw [lsdZ_expandingDGain_three, DZ_expandingDGain_three, lsdZ_mul3]

end Problems.BalancedTernary
