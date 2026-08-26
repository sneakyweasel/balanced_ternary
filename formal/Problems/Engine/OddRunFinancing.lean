import Problems.Engine.RepeatedOE

namespace Problems.Engine

/-!
# Odd-run financing of the first legal even residual

If a later state `x` realizes `O^a E^b` on a `MinimalNonTerm` orbit,
then `n ^ (2 ^ (a + b)) ≤ x ^ (3 ^ a)`. The start itself cannot meet
an even residual before `OOE`. Not a frequency theorem and not a halt
theorem.
-/

def oddEvenBlock (a b : ℕ) : List Branch :=
  List.replicate a Branch.odd ++ List.replicate b Branch.even

theorem follows_of_append_right {n : ℕ} :
    ∀ {u v : List Branch}, follows n (u ++ v) → follows (image n u) v
  | [], _, h => by simpa [image] using h
  | .even :: u, v, h => by
      simpa [image] using follows_of_append_right (u := u) h.2
  | .odd :: u, v, h => by
      simpa [image] using follows_of_append_right (u := u) h.2

theorem odd_run_even_residual {x a : ℕ}
    (hw : follows x (oddEvenBlock a 1)) :
    image x (List.replicate a Branch.odd) % 2 = 0 :=
  (follows_of_append_right (u := List.replicate a Branch.odd) hw).1

theorem two_pow_succ_le_three_of_two_le :
    ∀ {a : ℕ}, 2 ≤ a → 2 ^ (a + 1) ≤ 3 ^ a
  | 0, h => by omega
  | 1, h => by omega
  | 2, _ => by decide
  | a + 3, _ => by
      have ih : 2 ^ (a + 3) ≤ 3 ^ (a + 2) :=
        two_pow_succ_le_three_of_two_le (a := a + 2) (by omega)
      have h2 : 2 * 2 ^ (a + 3) ≤ 2 * 3 ^ (a + 2) :=
        Nat.mul_le_mul_left 2 ih
      have h3 : 2 * 3 ^ (a + 2) ≤ 3 * 3 ^ (a + 2) :=
        Nat.mul_le_mul_right _ (by decide : (2 : ℕ) ≤ 3)
      have hL : 2 ^ (a + 4) = 2 * 2 ^ (a + 3) := by
        rw [two_pow_succ]
      have hR : 3 ^ (a + 3) = 3 * 3 ^ (a + 2) := by
        rw [pow_succ, mul_comm]
      rw [hL, hR]
      exact le_trans h2 h3

theorem two_pow_succ_le_three_pow_iff {a : ℕ} :
    2 ^ (a + 1) ≤ 3 ^ a ↔ 2 ≤ a := by
  constructor
  · intro h
    cases a with
    | zero =>
        have : ¬(2 : ℕ) ^ 1 ≤ 3 ^ 0 := by decide
        exact (this h).elim
    | succ a =>
        cases a with
        | zero =>
            have : ¬(2 : ℕ) ^ 2 ≤ 3 ^ 1 := by decide
            exact (this h).elim
        | succ _ => omega
  · exact two_pow_succ_le_three_of_two_le

theorem pow_add_two (a b : ℕ) : 2 ^ (a + b) = 2 ^ b * 2 ^ a := by
  rw [Nat.pow_add, mul_comm]

/-- Isolated odd prefix envelope: `T^a(x)^{2^a} ≤ x^{3^a}`. -/
theorem odd_run_power_bound {x a : ℕ}
    (hw : follows x (List.replicate a Branch.odd)) :
    (floorPower^[a] x) ^ (2 ^ a) ≤ x ^ (3 ^ a) := by
  have h := power_bound_word hw
  simpa [List.length_replicate, oddCount_replicate_odd] using h

/-- Growth pays for collapse: `O^a E^b` on a minimal non-1 orbit
requires `n ^ (2 ^ (a + b)) ≤ x ^ (3 ^ a)`. -/
theorem odd_even_block_scale_barrier {n x k a b : ℕ}
    (h : MinimalNonTerm n) (hk : floorPower^[k] n = x)
    (hw : follows x (oddEvenBlock a b)) :
    n ^ (2 ^ (a + b)) ≤ x ^ (3 ^ a) := by
  have hodd := follows_of_append_left (u := List.replicate a Branch.odd) hw
  have heven := follows_of_append_right (u := List.replicate a Branch.odd) hw
  have hxa : floorPower^[k + a] n = image x (List.replicate a Branch.odd) := by
    rw [iterate_add_right, hk, image_eq_iterate, List.length_replicate]
  have hbar := even_run_scale_barrier h hxa heven
  have hpow := odd_run_power_bound hodd
  have hexp : n ^ (2 ^ (a + b)) = (n ^ (2 ^ b)) ^ (2 ^ a) := by
    rw [pow_add_two, Nat.pow_mul]
  rw [hexp]
  have hmid :
      (n ^ (2 ^ b)) ^ (2 ^ a) ≤
        (floorPower^[a] x) ^ (2 ^ a) :=
    Nat.pow_le_pow_left (by
      simpa [image_eq_iterate, List.length_replicate] using hbar) _
  exact le_trans hmid hpow

/-- First legal even residual after an odd run: `n ^ (2 ^ (a + 1)) ≤ x ^ (3 ^ a)`. -/
theorem odd_run_financing_scale_barrier {n x k a : ℕ}
    (h : MinimalNonTerm n) (hk : floorPower^[k] n = x)
    (hw : follows x (oddEvenBlock a 1)) :
    n ^ (2 ^ (a + 1)) ≤ x ^ (3 ^ a) :=
  odd_even_block_scale_barrier (b := 1) h hk hw

theorem odd_run_financing_scale_barrier_of_image {n : ℕ} {u : List Branch} {a : ℕ}
    (h : MinimalNonTerm n) (_hu : follows n u)
    (hw : follows (image n u) (oddEvenBlock a 1)) :
    n ^ (2 ^ (a + 1)) ≤ image n u ^ (3 ^ a) :=
  odd_run_financing_scale_barrier h (image_eq_iterate n u).symm hw

/-- At the minimal start, an even residual cannot occur before `OOE`.
Later odd runs may be shorter if the entry is already large. -/
theorem initial_even_not_before_ooe {n a : ℕ} (h : MinimalNonTerm n)
    (hw : follows n (oddEvenBlock a 1)) : 2 ≤ a := by
  have hfin := odd_run_financing_scale_barrier (k := 0) h rfl hw
  have hn : 1 < n := lt_of_lt_of_le (by decide : (1 : ℕ) < 12)
    (minimal_nonterm_ge_twelve h)
  have hexp : 2 ^ (a + 1) ≤ 3 ^ a :=
    (Nat.pow_le_pow_iff_right hn).mp hfin
  exact two_pow_succ_le_three_pow_iff.mp hexp

end Problems.Engine
