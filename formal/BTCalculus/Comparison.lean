import BTCalculus.Derivative

namespace BTCalculus

open Representation.Words

def cmp3 (x y : ℤ) : Trit :=
  if x < y then Trit.minus
  else if x = y then Trit.zero
  else Trit.plus

theorem cmp3_lt {x y : ℤ} (h : x < y) : cmp3 x y = Trit.minus := by
  simp [cmp3, h]

theorem cmp3_eq (x : ℤ) : cmp3 x x = Trit.zero := by
  simp [cmp3]

theorem cmp3_gt {x y : ℤ} (h : y < x) : cmp3 x y = Trit.plus := by
  have hne : ¬ x = y := ne_of_gt h
  have hnlt : ¬ x < y := not_lt.mpr (le_of_lt h)
  simp [cmp3, hnlt, hne]

theorem cmp3_antisym (x y : ℤ) : (cmp3 x y).negate = cmp3 y x := by
  rcases lt_trichotomy x y with h | h | h
  · simp [cmp3_lt h, cmp3_gt h, Trit.negate]
  · subst h
    simp [cmp3_eq, Trit.negate]
  · simp [cmp3_gt h, cmp3_lt h, Trit.negate]

theorem cmp3_translate (x y z : ℤ) : cmp3 (x + z) (y + z) = cmp3 x y := by
  rcases lt_trichotomy x y with h | h | h
  · have : x + z < y + z := add_lt_add_right h z
    simp [cmp3_lt h, cmp3_lt this]
  · subst h
    simp [cmp3_eq]
  · have : y + z < x + z := add_lt_add_right h z
    simp [cmp3_gt h, cmp3_gt this]

theorem cmp3_neg (x y : ℤ) : cmp3 (-x) (-y) = (cmp3 x y).negate := by
  rcases lt_trichotomy x y with h | h | h
  · have : -y < -x := neg_lt_neg h
    simp [cmp3_lt h, cmp3_gt this, Trit.negate]
  · subst h
    simp [cmp3_eq, Trit.negate]
  · have : -x < -y := neg_lt_neg h
    simp [cmp3_gt h, cmp3_lt this, Trit.negate]

theorem cmp3_mul_pos {x y c : ℤ} (hc : 0 < c) :
    cmp3 (c * x) (c * y) = cmp3 x y := by
  rcases lt_trichotomy x y with h | h | h
  · have : c * x < c * y := mul_lt_mul_of_pos_left h hc
    simp [cmp3_lt h, cmp3_lt this]
  · subst h
    simp [cmp3_eq]
  · have : c * y < c * x := mul_lt_mul_of_pos_left h hc
    simp [cmp3_gt h, cmp3_gt this]

theorem cmp3_mul_neg {x y c : ℤ} (hc : c < 0) :
    cmp3 (c * x) (c * y) = (cmp3 x y).negate := by
  rcases lt_trichotomy x y with h | h | h
  · have : c * y < c * x := mul_lt_mul_of_neg_left h hc
    simp [cmp3_lt h, cmp3_gt this, Trit.negate]
  · subst h
    simp [cmp3_eq, Trit.negate]
  · have : c * x < c * y := mul_lt_mul_of_neg_left h hc
    simp [cmp3_gt h, cmp3_lt this, Trit.negate]

end BTCalculus
