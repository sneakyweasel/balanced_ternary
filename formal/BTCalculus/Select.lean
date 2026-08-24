import BTCalculus.Comparison

namespace BTCalculus

open Representation.Words

def select3 (c : Trit) (xMinus xZero xPlus : ℤ) : ℤ :=
  match c with
  | .minus => xMinus
  | .zero => xZero
  | .plus => xPlus

theorem select3_minus (xm xz xp : ℤ) :
    select3 Trit.minus xm xz xp = xm := rfl

theorem select3_zero (xm xz xp : ℤ) :
    select3 Trit.zero xm xz xp = xz := rfl

theorem select3_plus (xm xz xp : ℤ) :
    select3 Trit.plus xm xz xp = xp := rfl

theorem select3_cases (c : Trit) (xm xz xp : ℤ) :
    select3 c xm xz xp = xm ∨
      select3 c xm xz xp = xz ∨
      select3 c xm xz xp = xp := by
  cases c <;> simp [select3]

/-- Every function ``Trit → ℤ`` is ``select3`` of its three values. -/
theorem select3_represents (f : Trit → ℤ) (c : Trit) :
    f c = select3 c (f Trit.minus) (f Trit.zero) (f Trit.plus) := by
  cases c <;> rfl

def absZ (n : ℤ) : ℤ :=
  select3 (cmp3 n 0) (-n) 0 n

theorem absZ_eq (n : ℤ) : absZ n = |n| := by
  rcases lt_trichotomy n 0 with h | h | h
  · rw [absZ, cmp3_lt h, select3, abs_of_neg h]
  · subst h
    simp [absZ, cmp3_eq, select3]
  · rw [absZ, cmp3_gt h, select3, abs_of_pos h]

def maxZ (x y : ℤ) : ℤ :=
  select3 (cmp3 x y) y x x

theorem maxZ_eq (x y : ℤ) : maxZ x y = max x y := by
  rcases lt_trichotomy x y with h | h | h
  · rw [maxZ, cmp3_lt h, select3, max_eq_right (le_of_lt h)]
  · subst h
    simp [maxZ, cmp3_eq, select3]
  · rw [maxZ, cmp3_gt h, select3, max_eq_left (le_of_lt h)]

def minZ (x y : ℤ) : ℤ :=
  select3 (cmp3 x y) x x y

theorem minZ_eq (x y : ℤ) : minZ x y = min x y := by
  rcases lt_trichotomy x y with h | h | h
  · rw [minZ, cmp3_lt h, select3, min_eq_left (le_of_lt h)]
  · subst h
    simp [minZ, cmp3_eq, select3]
  · rw [minZ, cmp3_gt h, select3, min_eq_right (le_of_lt h)]

end BTCalculus
