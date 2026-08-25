import Mathlib.Data.Int.Basic
import Mathlib.Tactic

namespace Problems.Engine

/-!
Exact identities for the one-variable loop campaign. These statements
are the problem definitions and their immediate integer consequences.
They are KNOWN. They are not a decision procedure for SLC termination
and not a proof of the Reachability Conjecture.
-/

/-- Integer points of the strip ``4x-2 ≤ 3y ≤ 4x-1`` with ``x ≥ 3``. -/
def rplusRel (x y : ℤ) : Prop :=
  3 ≤ x ∧ 4 * x - 2 ≤ 3 * y ∧ 3 * y ≤ 4 * x - 1

/-- The integer graph is a partial function. -/
theorem rplusRel_unique {x y z : ℤ} (hy : rplusRel x y) (hz : rplusRel x z) : y = z := by
  have : 3 * y = 3 * z := by
    rcases hy with ⟨_, hy₁, hy₂⟩
    rcases hz with ⟨_, hz₁, hz₂⟩
    omega
  omega

/-- Every integer point of the strip lies on one of the two cleared lines. -/
theorem rplusRel_clear {x y : ℤ} (h : rplusRel x y) :
    3 * y = 4 * x - 1 ∨ 3 * y = 4 * x - 2 := by
  rcases h with ⟨_, hlo, hhi⟩
  omega

/-- On the defined locus the successor is Euclidean division ``(4x) / 3``. -/
theorem rplusRel_ediv {x y : ℤ} (h : rplusRel x y) : (4 * x) / 3 = y := by
  have hsum : 4 * x = 3 * y + 1 ∨ 4 * x = 3 * y + 2 := by
    have := rplusRel_clear h
    omega
  have hdecomp : 3 * ((4 * x) / 3) + (4 * x) % 3 = 4 * x := Int.ediv_add_emod (4 * x) 3
  have hmod_nonneg : 0 ≤ (4 * x) % 3 := Int.emod_nonneg _ (by decide)
  have hmod_lt : (4 * x) % 3 < 3 := Int.emod_lt_of_pos _ (by decide)
  cases hsum with
  | inl h1 =>
    have : 3 * ((4 * x) / 3 - y) = 1 - (4 * x) % 3 := by
      linarith
    have hr : (4 * x) % 3 = 0 ∨ (4 * x) % 3 = 1 ∨ (4 * x) % 3 = 2 := by omega
    rcases hr with hr | hr | hr
    · omega
    · omega
    · omega
  | inr h2 =>
    have : 3 * ((4 * x) / 3 - y) = 2 - (4 * x) % 3 := by
      linarith
    have hr : (4 * x) % 3 = 0 ∨ (4 * x) % 3 = 1 ∨ (4 * x) % 3 = 2 := by omega
    rcases hr with hr | hr | hr
    · omega
    · omega
    · omega

/-- Decrement loop: from ``n`` the iterate ``x ↦ x-1`` reaches ``0`` in ``n`` steps. -/
def decrementIter : ℕ → ℤ → ℤ
  | 0, x => x
  | n + 1, x => decrementIter n (x - 1)

theorem decrement_iter_eq (n : ℕ) (x : ℤ) : decrementIter n x = x - n := by
  induction n generalizing x with
  | zero => simp [decrementIter]
  | succ n ih =>
    simp [decrementIter, ih]
    ring

theorem decrement_reaches_zero (n : ℕ) : decrementIter n n = 0 := by
  simp [decrement_iter_eq]

/-- Sign flip. -/
def negationMap (x : ℤ) : ℤ := -x

theorem negation_period2 (x : ℤ) : negationMap (negationMap x) = x := by
  simp [negationMap]

theorem negation_fixed_iff_zero (x : ℤ) : negationMap x = x ↔ x = 0 := by
  simp [negationMap]
  omega

end Problems.Engine
