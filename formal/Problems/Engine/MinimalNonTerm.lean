import Problems.Engine.FloorPower

namespace Problems.Engine

/-!
# Minimal non-termination: even-run scale barriers

Conditional constraints on a hypothetical minimal `n` that never
reaches `1`. Not a halt theorem. Not an all-odd orbit claim: an even
state above `n` may still map to a non-terminating square root.

Positive integers only: `ReachesOne 0` is false, so minimality is
quantified over `m ≥ 1`.
-/

/-- A positive integer that never reaches `1`, and is minimal with
that property among positive integers. -/
def MinimalNonTerm (n : ℕ) : Prop :=
  1 ≤ n ∧ ¬ReachesOne n ∧ ∀ m, 1 ≤ m → m < n → ReachesOne m

theorem MinimalNonTerm.pos {n : ℕ} (h : MinimalNonTerm n) : 1 ≤ n :=
  h.1

theorem MinimalNonTerm.not_reachesOne {n : ℕ} (h : MinimalNonTerm n) :
    ¬ReachesOne n :=
  h.2.1

theorem MinimalNonTerm.below {n m : ℕ} (h : MinimalNonTerm n)
    (hm0 : 1 ≤ m) (hm : m < n) : ReachesOne m :=
  h.2.2 m hm0 hm

theorem minimal_nonterm_ge_of_not_reachesOne {n m : ℕ}
    (h : MinimalNonTerm n) (hm0 : 1 ≤ m) (hm : ¬ReachesOne m) : n ≤ m := by
  by_contra hlt
  exact hm (h.below hm0 (Nat.lt_of_not_ge hlt))

theorem minimal_nonterm_ge_twelve {n : ℕ} (h : MinimalNonTerm n) : 12 ≤ n :=
  non_reachesOne_ge_twelve h.pos h.not_reachesOne

theorem floorPower_iterate_pos {n : ℕ} (hn : 1 ≤ n) : ∀ k, 1 ≤ floorPower^[k] n
  | 0 => hn
  | k + 1 => by
      have ih := floorPower_iterate_pos (floorPower_pos hn) k
      simpa [iterate_cons] using ih

theorem orbit_not_reachesOne {n m k : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = m) : ¬ReachesOne m :=
  fun hm => h.not_reachesOne (reachesOne_of_iterate hk hm)

theorem image_not_reachesOne {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) : ¬ReachesOne (image n w) :=
  orbit_not_reachesOne h (image_eq_iterate n w).symm

theorem minimal_nonterm_no_capture {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) : ¬Capture n w :=
  fun hc => h.not_reachesOne (capture_reachesOne hc)

theorem minimal_nonterm_no_descent {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) : ¬Descent n w := by
  intro hd
  have hpos := image_pos h.pos w
  have hr := h.below hpos hd.2
  exact h.not_reachesOne (reachesOne_of_image hr)

theorem minimal_nonterm_image_ge {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) (hw : follows n w) : n ≤ image n w := by
  by_contra hlt
  exact minimal_nonterm_no_descent h ⟨hw, Nat.lt_of_not_ge hlt⟩

theorem iterate_add_right (n k r : ℕ) :
    floorPower^[k + r] n = floorPower^[r] (floorPower^[k] n) := by
  rw [Nat.add_comm, Function.iterate_add_apply]

theorem minimal_nonterm_odd {n : ℕ} (h : MinimalNonTerm n) : n % 2 = 1 := by
  by_cases heven : n % 2 = 0
  · have hw : follows n (List.replicate 1 Branch.even) := ⟨heven, trivial⟩
    have hlt : floorPower n < n :=
      even_word_contracts (by have := minimal_nonterm_ge_twelve h; omega)
        (by decide) hw
    have hr : ReachesOne (floorPower n) :=
      h.below (floorPower_pos h.pos) hlt
    exact (h.not_reachesOne (reachesOne_of_iterate (k := 1) rfl hr)).elim
  · omega

/-- Even-run envelope: `r` even steps give `T^r(m)^{2^r} ≤ m`. -/
theorem even_run_pow_le {m : ℕ} :
    ∀ {r : ℕ}, follows m (List.replicate r Branch.even) →
      (floorPower^[r] m) ^ (2 ^ r) ≤ m := by
  intro r
  induction r generalizing m with
  | zero =>
      intro _
      simp
  | succ r ih =>
      intro hw
      rw [List.replicate_succ] at hw
      have ih' := ih hw.2
      have hstep := floorPower_even_sq_le hw.1
      have hexp :
          (floorPower^[r] (floorPower m)) ^ (2 ^ (r + 1)) =
            ((floorPower^[r] (floorPower m)) ^ (2 ^ r)) ^ 2 := by
        have hr2 : 2 ^ (r + 1) = 2 ^ r * 2 := by
          rw [two_pow_succ, mul_comm]
        rw [hr2, Nat.pow_mul]
      rw [iterate_cons m r, hexp]
      exact le_trans (Nat.pow_le_pow_left ih' 2) hstep

theorem even_run_exit_ge {n m k r : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = m)
    (_hw : follows m (List.replicate r Branch.even)) :
    n ≤ floorPower^[r] m := by
  have hexit : floorPower^[k + r] n = floorPower^[r] m := by
    rw [iterate_add_right, hk]
  exact minimal_nonterm_ge_of_not_reachesOne h
    (by rw [← hexit]; exact floorPower_iterate_pos h.pos (k + r))
    (orbit_not_reachesOne h hexit)

/-- Scale barrier: an `E^r` run on a minimal non-1 orbit has
entry at least `n ^ (2 ^ r)`. Not an all-odd claim. -/
theorem even_run_scale_barrier {n m k r : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = m)
    (hw : follows m (List.replicate r Branch.even)) :
    n ^ (2 ^ r) ≤ m := by
  have hexit := even_run_exit_ge h hk hw
  have hpow := even_run_pow_le hw
  exact le_trans (Nat.pow_le_pow_left hexit (2 ^ r)) hpow

theorem even_run_scale_barrier_of_image {n : ℕ} {u : List Branch} {r : ℕ}
    (h : MinimalNonTerm n) (_hu : follows n u)
    (hw : follows (image n u) (List.replicate r Branch.even)) :
    n ^ (2 ^ r) ≤ image n u :=
  even_run_scale_barrier h (image_eq_iterate n u).symm hw

theorem minimal_nonterm_even_ge_sq {n m k : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = m) (heven : m % 2 = 0) : n ^ 2 ≤ m :=
  even_run_scale_barrier (r := 1) h hk ⟨heven, trivial⟩

theorem minimal_nonterm_first_even_ge_sq {n : ℕ} {u : List Branch}
    (h : MinimalNonTerm n) (_hu : follows n u)
    (heven : image n u % 2 = 0) : n ^ 2 ≤ image n u :=
  minimal_nonterm_even_ge_sq h (image_eq_iterate n u).symm heven

theorem minimal_nonterm_avoid_even_lt_sq_twelve {n m k : ℕ}
    (h : MinimalNonTerm n) (hk : floorPower^[k] n = m)
    (heven : m % 2 = 0) : 144 ≤ m := by
  have hm0 : 1 ≤ m := by
    rw [← hk]
    exact floorPower_iterate_pos h.pos k
  by_contra hlt
  exact orbit_not_reachesOne h hk
    (even_lt_sq_twelve_reachesOne heven hm0 (Nat.lt_of_not_ge hlt))

theorem even_tower_not_on_minimal {n k j : ℕ} (h : MinimalNonTerm n)
    (hk : 1 ≤ k) : floorPower^[j] n ≠ 2 ^ (2 ^ (k - 1)) :=
  fun heq =>
    orbit_not_reachesOne h heq (capture_reachesOne (even_tower_capture hk))

theorem minimal_nonterm_oe_descent {n : ℕ} (h : MinimalNonTerm n)
    (heven : floorPower n % 2 = 0) :
    Descent n [.odd, .even] := by
  have hodd := minimal_nonterm_odd h
  have hw : follows n [.odd, .even] := ⟨hodd, heven, trivial⟩
  have hT : floorPower n = (n ^ 3).sqrt := floorPower_odd_eq hodd
  have hlt :=
    floorPower_odd_even_two_step_lt
      (by have := minimal_nonterm_ge_twelve h; omega) hodd
      (by simpa [hT] using heven)
  exact ⟨hw, by simpa [image] using hlt⟩

/-- The first image is odd. Later even states are still allowed if they
stay at scale `≥ n^2`. -/
theorem minimal_nonterm_odd_image_odd {n : ℕ} (h : MinimalNonTerm n) :
    floorPower n % 2 = 1 := by
  by_cases heven : floorPower n % 2 = 0
  · exact (minimal_nonterm_no_descent h (minimal_nonterm_oe_descent h heven)).elim
  · omega

/-- Finite-prefix normal form. Not a totality proof and not an all-odd
orbit theorem. -/
theorem minimal_counterexample_normal_form {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) (hw : follows n w) :
    12 ≤ n ∧
      n % 2 = 1 ∧
      n ≤ image n w ∧
      ¬ReachesOne (image n w) ∧
      ¬Descent n w ∧
      ¬Capture n w ∧
      (image n w % 2 = 0 → n ^ 2 ≤ image n w) :=
  ⟨minimal_nonterm_ge_twelve h,
    minimal_nonterm_odd h,
    minimal_nonterm_image_ge h hw,
    image_not_reachesOne h,
    minimal_nonterm_no_descent h,
    minimal_nonterm_no_capture h,
    fun heven =>
      minimal_nonterm_even_ge_sq h (image_eq_iterate n w).symm heven⟩

end Problems.Engine
