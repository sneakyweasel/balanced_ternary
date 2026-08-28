import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Tactic

namespace Problems.Juggler

/-!
# Gap cells: exact floor reductions for the parity-discrepancy program

The analytic discrepancy estimates of the finite-dynamics note
(Section 5) and of the two-step parity companion are human proofs.
They rest on three exact floor reductions, packaged here:

* `floor_add_eq_add_carry` — the floor of a sum splits into the two
  floors plus a 0/1 carry decided by the fractional parts;
* `floor_gap_eq_carry` / `seq_floor_gap` — the gap-cell identity
  (Lemmas B and N of the companion): the increment of `⌊Y⌋` along a
  step is the floor of the smooth increment plus a sawtooth carry;
* `floor_odd_iff_half_le_fract_half` — the parity of `⌊x⌋` is the
  event `{x/2} ≥ 1/2`, the exact fractional-part form that converts
  parity sums into interval discrepancies.

No analytic estimate is claimed here. These identities are exact and
unconditional; the van der Corput and Erdős–Turán stages of the
companion remain human proofs outside Lean.
-/

/-- The floor of a sum is the sum of floors plus a 0/1 carry, decided
by whether the fractional parts overflow. -/
theorem floor_add_eq_add_carry (x y : ℝ) :
    ⌊x + y⌋ = ⌊x⌋ + ⌊y⌋ +
      if 1 ≤ Int.fract x + Int.fract y then 1 else 0 := by
  have hxy : x + y = ((⌊x⌋ + ⌊y⌋ : ℤ) : ℝ) + (Int.fract x + Int.fract y) := by
    have hx := Int.floor_add_fract x
    have hy := Int.floor_add_fract y
    push_cast
    linarith
  rw [hxy, Int.floor_intCast_add]
  congr 1
  by_cases h : 1 ≤ Int.fract x + Int.fract y
  · rw [if_pos h]
    refine Int.floor_eq_iff.mpr ⟨by exact_mod_cast h, ?_⟩
    have hx1 := Int.fract_lt_one x
    have hy1 := Int.fract_lt_one y
    push_cast
    linarith
  · rw [if_neg h]
    have hlt : Int.fract x + Int.fract y < 1 := not_le.mp h
    refine Int.floor_eq_iff.mpr ⟨?_, by push_cast; linarith⟩
    have hx0 := Int.fract_nonneg x
    have hy0 := Int.fract_nonneg y
    push_cast
    linarith

/-- Gap-cell identity (Lemma B pattern): the increment of `⌊·⌋` across
a shift `δ` is `⌊δ⌋` plus the carry `𝟙[{x} ≥ 1 − {δ}]`. -/
theorem floor_gap_eq_carry (x δ : ℝ) :
    ⌊x + δ⌋ - ⌊x⌋ = ⌊δ⌋ +
      if 1 - Int.fract δ ≤ Int.fract x then 1 else 0 := by
  rw [floor_add_eq_add_carry x δ]
  by_cases h : 1 - Int.fract δ ≤ Int.fract x
  · rw [if_pos h, if_pos (by linarith)]
    ring
  · rw [if_neg h, if_neg (fun hc => h (by linarith))]
    ring

/-- Level-2 gap identity (Lemma N pattern): along any real-valued
sequence `Y`, the integer gap `⌊Y (n+h)⌋ − ⌊Y n⌋` is the floor of the
smooth increment plus a 0/1 carry read off the fractional parts. With
`Y = (m ∘ ·)^{3/2}` this is the companion's `g₂ = ⌊ΔY⌋ + κ₂`. -/
theorem seq_floor_gap (Y : ℕ → ℝ) (n h : ℕ) :
    ⌊Y (n + h)⌋ - ⌊Y n⌋ =
      ⌊Y (n + h) - Y n⌋ +
        if 1 - Int.fract (Y (n + h) - Y n) ≤ Int.fract (Y n) then 1
        else 0 := by
  have hgap := floor_gap_eq_carry (Y n) (Y (n + h) - Y n)
  rw [add_sub_cancel] at hgap
  exact hgap

/-- The carry of the gap identity is 0 or 1. -/
theorem gap_carry_mem (x δ : ℝ) :
    (if 1 - Int.fract δ ≤ Int.fract x then (1 : ℤ) else 0) = 0 ∨
      (if 1 - Int.fract δ ≤ Int.fract x then (1 : ℤ) else 0) = 1 := by
  by_cases h : 1 - Int.fract δ ≤ Int.fract x
  · exact Or.inr (if_pos h)
  · exact Or.inl (if_neg h)

/-- Parity bridge: `⌊x⌋` is odd exactly when `{x/2} ≥ 1/2`. This is
the exact fractional-part reduction that converts the parity sums of
the discrepancy program into interval discrepancies. -/
theorem floor_odd_iff_half_le_fract_half (x : ℝ) :
    ⌊x⌋ % 2 = 1 ↔ (1 / 2 : ℝ) ≤ Int.fract (x / 2) := by
  obtain ⟨t, ht0, ht1, hx⟩ : ∃ t : ℝ, 0 ≤ t ∧ t < 1 ∧ x = ⌊x⌋ + t :=
    ⟨Int.fract x, Int.fract_nonneg x, Int.fract_lt_one x,
      (Int.floor_add_fract x).symm⟩
  rcases Int.even_or_odd ⌊x⌋ with ⟨q, hq⟩ | ⟨q, hq⟩
  · have hfr : Int.fract (x / 2) = t / 2 := by
      have hx2 : x / 2 = (q : ℝ) + t / 2 := by
        rw [hx, hq]; push_cast; ring
      rw [hx2, Int.fract_intCast_add,
        Int.fract_eq_self.mpr ⟨by linarith, by linarith⟩]
    rw [hfr]
    constructor
    · intro h; exfalso; omega
    · intro h; exfalso; linarith
  · have hfr : Int.fract (x / 2) = (1 + t) / 2 := by
      have hx2 : x / 2 = (q : ℝ) + (1 + t) / 2 := by
        rw [hx, hq]; push_cast; ring
      rw [hx2, Int.fract_intCast_add,
        Int.fract_eq_self.mpr ⟨by linarith, by linarith⟩]
    rw [hfr]
    constructor
    · intro _; linarith
    · intro _; omega

end Problems.Juggler
