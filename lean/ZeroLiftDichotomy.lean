/-!
Milestone 5 Lean 4 target: the abstract zero-lift dichotomy.

`R m` is the minimum realizer of the prefix of length `m`, and `J m`
is its lift coefficient.  The concrete cylinder development must supply:

* `realizer_iff_stabilizes`: a positive integer realizes every prefix
  exactly when `R` stabilizes;
* `step_iff_zero`: one step of `R` is unchanged exactly when `J = 0`.

The theorem below proves that these two exact bridge lemmas imply the
three-way Milestone 5 equivalence.  It uses only Lean's standard library.
-/

import Std

namespace ZeroLift

def EventuallyConstant (R : Nat → Nat) : Prop :=
  ∃ N, ∀ m, N ≤ m → R m = R N

def EventuallyZero (J : Nat → Nat) : Prop :=
  ∃ N, ∀ m, N ≤ m → J m = 0

theorem eventuallyConstant_iff_eventuallyZero
    (R J : Nat → Nat)
    (step_iff_zero : ∀ m, R (m + 1) = R m ↔ J m = 0) :
    EventuallyConstant R ↔ EventuallyZero J := by
  constructor
  · rintro ⟨N, hR⟩
    refine ⟨N, ?_⟩
    intro m hm
    apply (step_iff_zero m).mp
    rw [hR m hm, hR (m + 1) (Nat.le_trans hm (Nat.le_add_right m 1))]
  · rintro ⟨N, hJ⟩
    refine ⟨N, ?_⟩
    intro m hm
    obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hm
    induction d with
    | zero =>
        simp
    | succ d ih =>
        rw [Nat.add_succ]
        calc
          R (N + d + 1) = R (N + d) :=
            (step_iff_zero (N + d)).mpr
              (hJ (N + d) (Nat.le_add_right N d))
          _ = R N := ih

theorem zeroLiftDichotomy
    (R J : Nat → Nat)
    (HasPositiveIntegerRealizer : Prop)
    (realizer_iff_stabilizes :
      HasPositiveIntegerRealizer ↔ EventuallyConstant R)
    (step_iff_zero : ∀ m, R (m + 1) = R m ↔ J m = 0) :
    HasPositiveIntegerRealizer ↔
      EventuallyConstant R ∧ EventuallyZero J := by
  rw [realizer_iff_stabilizes]
  constructor
  · intro hR
    exact ⟨hR, (eventuallyConstant_iff_eventuallyZero R J step_iff_zero).mp hR⟩
  · exact fun h => h.1

end ZeroLift
