import Problems.Engine.MinimalNonTerm

namespace Problems.Engine

/-!
# Repeated `OE` scale budget

Exact power-envelope specializations of `OE` and `(OE)^r`, then the
minimal-counterexample scale barrier. Not a frequency theorem, not a
halt theorem, and not a new energy.
-/

def wordOE : List Branch := [.odd, .even]

def repeatedOE : ℕ → List Branch
  | 0 => []
  | r + 1 => wordOE ++ repeatedOE r

theorem wordOE_length : wordOE.length = 2 := rfl

theorem oddCount_wordOE : oddCount wordOE = 1 := rfl

theorem repeatedOE_zero : repeatedOE 0 = [] := rfl

theorem repeatedOE_succ (r : ℕ) : repeatedOE (r + 1) = wordOE ++ repeatedOE r :=
  rfl

theorem length_repeatedOE : ∀ r, (repeatedOE r).length = 2 * r
  | 0 => rfl
  | r + 1 => by
      rw [repeatedOE_succ, List.length_append, wordOE_length, length_repeatedOE]
      omega

theorem oddCount_repeatedOE : ∀ r, oddCount (repeatedOE r) = r
  | 0 => rfl
  | r + 1 => by
      rw [repeatedOE_succ, oddCount_append, oddCount_wordOE, oddCount_repeatedOE]
      omega

theorem four_pow_eq_two_pow_two_mul (r : ℕ) : 4 ^ r = 2 ^ (2 * r) := by
  rw [show (4 : ℕ) = 2 ^ 2 from rfl, Nat.pow_mul]

/-- One realized `OE` block: `T^2(x)^4 ≤ x^3`. -/
theorem oe_block_scale {x : ℕ} (hw : follows x wordOE) :
    image x wordOE ^ 4 ≤ x ^ 3 := by
  have h := power_bound_word hw
  simpa [wordOE, image_eq_iterate] using h

theorem oe_block_contracts {x : ℕ} (hx : 2 ≤ x) (hw : follows x wordOE) :
    image x wordOE < x := by
  have hgap : (3 : ℕ) ^ oddCount wordOE < 2 ^ wordOE.length := by
    simp [wordOE]
  have h := power_bound_contracts hx hw hgap
  simpa [wordOE, image_eq_iterate] using h

/-- Repeated realized `OE` blocks: `T^{2r}(x)^{4^r} ≤ x^{3^r}`. -/
theorem repeated_oe_scale {x r : ℕ} (hw : follows x (repeatedOE r)) :
    (floorPower^[2 * r] x) ^ (4 ^ r) ≤ x ^ (3 ^ r) := by
  have h := power_bound_word hw
  rw [length_repeatedOE, oddCount_repeatedOE] at h
  rw [← four_pow_eq_two_pow_two_mul] at h
  exact h

theorem follows_of_append_left {n : ℕ} :
    ∀ {u v : List Branch}, follows n (u ++ v) → follows n u
  | [], _, _ => trivial
  | .even :: _, _, h => ⟨h.1, follows_of_append_left h.2⟩
  | .odd :: _, _, h => ⟨h.1, follows_of_append_left h.2⟩

/-- A later `(OE)^r` segment on a minimal non-1 orbit requires
`n^{4^r} ≤ x^{3^r}`. -/
theorem repeated_oe_scale_barrier {n x k r : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = x) (hw : follows x (repeatedOE r)) :
    n ^ (4 ^ r) ≤ x ^ (3 ^ r) := by
  have hexit : floorPower^[k + 2 * r] n = floorPower^[2 * r] x := by
    rw [iterate_add_right, hk]
  have hge : n ≤ floorPower^[2 * r] x :=
    minimal_nonterm_ge_of_not_reachesOne h
      (by
        rw [← hexit]
        exact floorPower_iterate_pos h.pos (k + 2 * r))
      (orbit_not_reachesOne h hexit)
  exact le_trans (Nat.pow_le_pow_left hge (4 ^ r)) (repeated_oe_scale hw)

theorem repeated_oe_scale_barrier_of_image {n : ℕ} {u : List Branch} {r : ℕ}
    (h : MinimalNonTerm n) (_hu : follows n u)
    (hw : follows (image n u) (repeatedOE r)) :
    n ^ (4 ^ r) ≤ image n u ^ (3 ^ r) :=
  repeated_oe_scale_barrier h (image_eq_iterate n u).symm hw

theorem oe_requires_scale {n x k : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = x) (hw : follows x wordOE) : n ^ 4 ≤ x ^ 3 := by
  have hrep : follows x (repeatedOE 1) := by
    simpa [repeatedOE, wordOE] using hw
  simpa using repeated_oe_scale_barrier (r := 1) h hk hrep

/-- `(OE)^r` cannot start at the minimal state itself: the first image
is odd. Not a frequency theorem. -/
theorem minimal_nonterm_not_repeated_oe {n r : ℕ} (h : MinimalNonTerm n)
    (hr : 1 ≤ r) : ¬follows n (repeatedOE r) := by
  intro hw
  cases r with
  | zero => omega
  | succ r =>
      have hOE : follows n wordOE :=
        follows_of_append_left (u := wordOE) hw
      have heven : floorPower n % 2 = 0 := hOE.2.1
      have hodd := minimal_nonterm_odd_image_odd h
      omega

end Problems.Engine
