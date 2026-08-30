import Problems.Juggler.CycleCore

namespace Problems.Juggler

/-!
# First internal `OO`: CycleMin wrappers

The isolated-`OE` survival bound, the `R(2)=0` corollary, and the
`AboveAnchor` form live in `MinimumRelative`. This file keeps the
CycleMin consumers: a scale-gap isolated prefix cannot occur on a
cycle minimum, so an `a₀ = 2` CycleMin cannot complete one `OE`
after `OOE`.

The suffix after the first `OO` is not classified. Not a halt
theorem, not a four-even assembler, and not a length-11 census.
-/

theorem no_cycleMin_isolated_prefix_of_gap {n a r : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (h : CycleMin n (isolatedPrefix a r ++ v)) : False :=
  forbidden_isolated_under_anchor hn (Nat.not_le.mpr hgap)
    (aboveAnchor_of_prefix (aboveAnchor_of_cycleMin h))

/-- An `a₀ = 2` CycleMin cannot complete one isolated `OE` after the
first even letter. The first internal `OO`, if it exists on this
corridor, is immediate (`r = 0`). -/
theorem no_cycleMin_prefix_ooe_oe {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (isolatedPrefix 2 1 ++ v)) : False :=
  no_cycleMin_isolated_prefix_of_gap hn two_one_isolated_scale_gap h

/-- Cycle application of the shared `r ≤ R(2)` bound. -/
theorem cycleMin_isolated_two {n r : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (isolatedPrefix 2 r ++ v)) : r = 0 :=
  aboveAnchor_isolated_two hn
    (aboveAnchor_of_prefix (aboveAnchor_of_cycleMin h))

/-- Termination application: a CE-realized isolated prefix with
`a₀ = 2` forces `r = 0`. -/
theorem minimal_isolated_two {n r : ℕ} (h : MinimalNonTerm n)
    (hw : follows n (isolatedPrefix 2 r)) : r = 0 :=
  aboveAnchor_isolated_two
    (le_trans (by decide : (2 : ℕ) ≤ 12) (minimal_nonterm_ge_twelve h))
    (aboveAnchor_of_minimalNonTerm h hw)

end Problems.Juggler
