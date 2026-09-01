import Problems.Juggler.WalkChargeWords
import Problems.Juggler.MinimumRelative

namespace Problems.Juggler

/-!
# Above-anchor walk: hug domination for open trajectories

Ports the discrete walk layer of Paper A Section 5 from minimum-based
cycles to open (non-closing) trajectory prefixes. The hypothesis is
`AboveAnchor n w` — every realized state along `w` stays at or above
the anchor `n` — with no cycle assumption.

The content is the composition of two existing facts:

* the defect-free upper envelope (`power_bound_contracts`) makes a
  walk-negative prefix (`3^{a_k} < 2^k`) contract strictly below `n`,
  so an above-anchor prefix keeps the exponent walk nonnegative
  (`aboveAnchor_prefix_pow_le`), exactly the `CycleMin` hypothesis of
  `cycleMin_prefix_pow_le` without the cycle;
* hug minimality (`hugOdds_least`) then forces every above-anchor
  prefix to dominate the exact hug word in odd count
  (`aboveAnchor_prefix_odds_ge_hug`).

This constrains *hypothetical* never-descending orbit segments only.
It is not a halt theorem, not a descent-certificate existence claim,
and not a cycle obstruction; it does not modify Paper A.
-/

/-- Prefix non-contraction on an `AboveAnchor` prefix: a
walk-negative prefix would contract strictly below the anchor. This
is `cycleMin_prefix_pow_le` with the cycle hypothesis replaced by
the open above-anchor hypothesis — a never-descending orbit segment
keeps `u_k ≥ 0` at every prefix length. -/
theorem aboveAnchor_prefix_pow_le {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : AboveAnchor n w) :
    ∀ k, k ≤ w.length → 2 ^ k ≤ 3 ^ oddCount (w.take k) := by
  intro k hk
  by_contra hc
  have hf : follows n (w.take k) := follows_take w k h.1
  have hlen : (w.take k).length = k := by
    simp [List.length_take, Nat.min_eq_left hk]
  have hgap : 3 ^ oddCount (w.take k) < 2 ^ (w.take k).length := by
    rw [hlen]; exact Nat.lt_of_not_le hc
  have hcontr := power_bound_contracts hn hf hgap
  rw [hlen] at hcontr
  exact absurd hcontr (not_lt.mpr (h.2 k hk))

/-- **Open trajectories dominate the hug word.** Every prefix of a
never-descending orbit segment carries at least as many odd letters
as the exact hug word of the same length. The open-trajectory form
of `cycleMin_prefix_odds_ge_hug`: the hug adversary prices not only
hypothetical cycles but every hypothetical descent-free flight. -/
theorem aboveAnchor_prefix_odds_ge_hug {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : AboveAnchor n w) :
    ∀ k, k ≤ w.length → hugOdds k ≤ oddCount (w.take k) :=
  fun k hk => hugOdds_least (aboveAnchor_prefix_pow_le hn h k hk)

/-- Full-word instance: an above-anchor word of length `L` has at
least `hugOdds L` odd letters. -/
theorem aboveAnchor_odds_ge_hug {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : AboveAnchor n w) :
    hugOdds w.length ≤ oddCount w := by
  simpa using aboveAnchor_prefix_odds_ge_hug hn h w.length le_rfl

end Problems.Juggler
