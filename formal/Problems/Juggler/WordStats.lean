import Problems.Juggler.Itinerary

namespace Problems.Juggler

/-!
# Word statistics

Length, odd count, and the combinatorial drift of a finite word.
This file does not know how a word was obtained.
-/

def oddCount : List Branch → ℕ
  | [] => 0
  | .odd :: w => oddCount w + 1
  | .even :: w => oddCount w

@[simp] theorem oddCount_nil : oddCount [] = 0 := rfl

@[simp] theorem oddCount_even_cons (w : List Branch) :
    oddCount (.even :: w) = oddCount w := rfl

@[simp] theorem oddCount_odd_cons (w : List Branch) :
    oddCount (.odd :: w) = oddCount w + 1 := rfl

theorem oddCount_replicate_even (k : ℕ) :
    oddCount (List.replicate k Branch.even) = 0 := by
  induction k with
  | zero => simp
  | succ k ih => simp [List.replicate_succ, ih]

theorem oddCount_replicate_odd (k : ℕ) :
    oddCount (List.replicate k Branch.odd) = k := by
  induction k with
  | zero => simp
  | succ k ih => simp [List.replicate_succ, ih]

theorem oddCount_le_length : ∀ w : List Branch, oddCount w ≤ w.length
  | [] => by simp
  | .even :: w => by
      simpa [List.length_cons] using
        (le_trans (oddCount_le_length w) (Nat.le_succ _))
  | .odd :: w => by
      exact Nat.succ_le_succ (oddCount_le_length w)

theorem oddCount_append : ∀ u v, oddCount (u ++ v) = oddCount u + oddCount v
  | [], _ => by simp
  | .even :: u, v => by simp [oddCount_append u v]
  | .odd :: u, v => by
      simp [oddCount_append u v, Nat.add_assoc, Nat.add_comm]

theorem eq_replicate_even_of_oddCount_zero {w : List Branch}
    (h : oddCount w = 0) : w = List.replicate w.length Branch.even := by
  induction w with
  | nil => simp
  | cons b rest ih =>
      cases b with
      | even =>
          have hrest : oddCount rest = 0 := by simpa using h
          have hk : (Branch.even :: rest).length = rest.length + 1 := rfl
          rw [hk, List.replicate_succ]
          exact congrArg (List.cons Branch.even) (ih hrest)
      | odd =>
          simp at h

theorem eq_replicate_odd_of_oddCount_eq_length {v : List Branch}
    (h : oddCount v = v.length) : v = List.replicate v.length Branch.odd := by
  induction v with
  | nil => simp
  | cons b v ih =>
      cases b with
      | odd =>
          have hv : oddCount v = v.length := by
            simp [List.length_cons] at h
            omega
          simpa [List.replicate_succ] using
            congrArg (List.cons Branch.odd) (ih hv)
      | even =>
          have : oddCount v ≤ v.length := oddCount_le_length v
          simp [List.length_cons] at h
          omega

/-- Combinatorial drift of a finite word. Positive means the formal
even exponent strictly dominates the odd exponent. -/
def driftG (w : List Branch) : ℤ :=
  (2 : ℤ) ^ w.length - (3 : ℤ) ^ oddCount w

def exponentGap (w : List Branch) : Prop :=
  3 ^ oddCount w < 2 ^ w.length

/-- Formal surplus is strictly positive: the odd exponent dominates. -/
def exponentExpanding (w : List Branch) : Prop :=
  2 ^ w.length < 3 ^ oddCount w

theorem exponentGap_iff_posDrift (w : List Branch) :
    exponentGap w ↔ 0 < driftG w := by
  unfold exponentGap driftG
  constructor
  · intro h
    exact Int.sub_pos_of_lt (Int.ofNat_lt.mpr h)
  · intro h
    have hlt : ((3 : ℕ) : ℤ) ^ oddCount w < ((2 : ℕ) : ℤ) ^ w.length :=
      lt_of_sub_pos h
    exact Int.ofNat_lt.mp hlt

theorem exponentExpanding_not_gap {w : List Branch}
    (h : exponentExpanding w) : ¬ exponentGap w :=
  fun hg => (lt_asymm h) hg

/-- Prefix-noncontracting: no prefix has positive combinatorial drift. -/
def prefixNoncontracting (w : List Branch) : Prop :=
  ∀ k, k ≤ w.length → ¬exponentGap (w.take k)

end Problems.Juggler
