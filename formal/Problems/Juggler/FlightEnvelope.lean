import Problems.Juggler.WalkTransport
import Problems.Juggler.AboveAnchorWalk

namespace Problems.Juggler

/-!
# Flight envelope: transport on open descent-free prefixes

Ports the transport theorem (Paper A Theorem 5.3, `WalkTransport.lean`)
from minimum-based cycles to open trajectory prefixes, and packages the
two-sided fly-height sandwich

`w_k · (log n − D) ≤ log x_k ≤ w_k · log n`

on `AboveAnchor n w` with `n ≥ 400`, where `w_k = 3^{a_k}/2^k` is the
walk weight and `D = 1.05·e/n + 0.7·o/(n·√n)` is the transport deficit
over the full word.

The upper side is unconditional (floors only lose): it is the log form
of `power_bound_word` and needs only `follows n w` with `n ≥ 1`. The
lower side is the `cycleMin_transport_prefix` induction verbatim with
the cycle hypothesis replaced by the anchor hypothesis: odd injections
are priced at `x_j ≥ n` (`aboveAnchor_iterate_ge`), even injections at
`x_j ≥ n²` (`even_ge_sq_of_aboveAnchor`), and walk nonnegativity comes
from `aboveAnchor_prefix_pow_le`.

Consequence at the prefix peak: `log H ≥ W·(log n − D)` with
`W = max_k w_k`, so the fly exponent `log H / log n` of a descent-free
prefix equals its peak walk weight up to `O(D·W/log n)`.

This constrains hypothetical never-descending orbit segments and
measures realized ascent prefixes only. It is not a halt theorem, not
a divergence theorem, not a cycle obstruction, and it does not modify
Paper A. Above-anchor alone does not force height explosion: the hug
adversary keeps `w_k` pinned near `1`.
-/

/-!
## The defect-free upper envelope, log form
-/

/-- Upper envelope on any realized prefix (floors only lose):
`log x_k ≤ w_k · log n`. Log form of `power_bound_word`; no anchor
hypothesis. -/
theorem follows_log_le_walkWeight {n : ℕ} {w : List Branch}
    (hn : 1 ≤ n) (hf : follows n w) {k : ℕ} (hk : k ≤ w.length) :
    Real.log (floorPower^[k] n) ≤ walkWeight w k * Real.log n := by
  have hfk : follows n (w.take k) := follows_take w k hf
  have hlen : (w.take k).length = k := by
    simp [List.length_take, Nat.min_eq_left hk]
  have hpb := power_bound_word hfk
  rw [hlen] at hpb
  set x := floorPower^[k] n with hxdef
  set a := oddCount (w.take k) with hadef
  have hxpos : 1 ≤ x := floorPower_iterate_pos hn k
  have hxR : (0 : ℝ) < x := by exact_mod_cast hxpos
  have hnR : (1 : ℝ) ≤ n := by exact_mod_cast hn
  have hcast : ((x : ℝ)) ^ (2 ^ k) ≤ ((n : ℝ)) ^ (3 ^ a) := by
    exact_mod_cast hpb
  have hlog : Real.log ((x : ℝ) ^ (2 ^ k)) ≤
      Real.log ((n : ℝ) ^ (3 ^ a)) :=
    Real.log_le_log (by positivity) hcast
  rw [Real.log_pow, Real.log_pow] at hlog
  push_cast at hlog
  rw [walkWeight, ← hadef, div_mul_eq_mul_div,
    le_div_iff₀ (by positivity : (0 : ℝ) < 2 ^ k)]
  linarith

/-!
## Walk nonnegativity in weight form
-/

/-- Above-anchor prefixes keep `w_k ≥ 1`
(`aboveAnchor_prefix_pow_le` in weight form). -/
theorem one_le_walkWeight_aboveAnchor {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (h : AboveAnchor n w) {k : ℕ} (hk : k ≤ w.length) :
    1 ≤ walkWeight w k := by
  have hpow := aboveAnchor_prefix_pow_le hn h k hk
  rw [walkWeight, le_div_iff₀ (by positivity), one_mul]
  exact_mod_cast hpow

/-!
## The transport induction, anchor form
-/

/-- Transport invariant along an open descent-free prefix:
`w_k·(log n − D_k) ≤ log x_k` with the running prefix deficit. The
`cycleMin_transport_prefix` induction with the cycle hypothesis
replaced by the anchor hypothesis. -/
theorem aboveAnchor_transport_prefix {n : ℕ} {w : List Branch}
    (hn : 400 ≤ n) (h : AboveAnchor n w) :
    ∀ k, k ≤ w.length →
      walkWeight w k * (Real.log n - prefixDeficit n w k) ≤
        Real.log (floorPower^[k] n) := by
  have hn2 : 2 ≤ n := by omega
  have hnR : (400 : ℝ) ≤ n := by exact_mod_cast hn
  have hnpos : (0 : ℝ) < n := by linarith
  have hsn : (0 : ℝ) < Real.sqrt n := Real.sqrt_pos.mpr hnpos
  intro k
  induction k with
  | zero =>
    intro _
    simp [prefixDeficit]
  | succ k ih =>
    intro hk1
    have hk : k < w.length := hk1
    have hIH := ih (le_of_lt hk)
    have hiter : floorPower^[k + 1] n = floorPower (floorPower^[k] n) :=
      Function.iterate_succ_apply' floorPower k n
    set x := floorPower^[k] n with hxdef
    have hxge : n ≤ x := aboveAnchor_iterate_ge h (le_of_lt hk)
    set W := walkWeight w k with hWdef
    set A := Real.log n - prefixDeficit n w k with hAdef
    have hW1 : 1 ≤ W := one_le_walkWeight_aboveAnchor hn2 h (le_of_lt hk)
    cases hlet : w[k] with
    | odd =>
      have hxodd : x % 2 = 1 := follows_get_odd w h.1 k hk hlet
      have hstep := log_floorPower_odd_ge (x := x) (by omega) hxodd
      -- loss comparison: `1.05/(x√x) ≤ 1.05/(n√n)`
      have hxR : (n : ℝ) ≤ x := by exact_mod_cast hxge
      have hsx : Real.sqrt n ≤ Real.sqrt x := Real.sqrt_le_sqrt hxR
      have hns : (0 : ℝ) < n * Real.sqrt n := by positivity
      have hxs : (0 : ℝ) < (x : ℝ) * Real.sqrt x := by
        have : (0 : ℝ) < x := by linarith
        have : (0 : ℝ) < Real.sqrt x := Real.sqrt_pos.mpr this
        positivity
      have hloss : 1.05 / ((x : ℝ) * Real.sqrt x) ≤
          1.05 / (n * Real.sqrt n) := by
        apply div_le_div_of_nonneg_left (by norm_num) hns
        exact mul_le_mul hxR hsx (le_of_lt hsn) (by linarith)
      -- weight and deficit steps
      have hWs : walkWeight w (k + 1) = 3 / 2 * W :=
        walkWeight_succ_odd hk hlet
      have hDs : prefixDeficit n w (k + 1) =
          prefixDeficit n w k + 0.7 / (n * Real.sqrt n) := by
        rw [prefixDeficit_succ, List.getElem?_eq_getElem hk, hlet]
        simp
      have hWc : 1.05 / (n * Real.sqrt n) ≤ W * (1.05 / (n * Real.sqrt n)) :=
        le_mul_of_one_le_left (by positivity) hW1
      rw [hiter, hWs, hDs]
      calc 3 / 2 * W * (Real.log n - (prefixDeficit n w k +
              0.7 / (n * Real.sqrt n)))
          = 3 / 2 * (W * A) - W * (1.05 / (n * Real.sqrt n)) := by
            rw [hAdef]; ring
        _ ≤ 3 / 2 * Real.log x - 1.05 / (n * Real.sqrt n) := by
            have := mul_le_mul_of_nonneg_left hIH
              (by norm_num : (0 : ℝ) ≤ 3 / 2)
            linarith
        _ ≤ 3 / 2 * Real.log x - 1.05 / ((x : ℝ) * Real.sqrt x) := by
            linarith
        _ ≤ Real.log (floorPower x) := by linarith
    | even =>
      have hxeven : x % 2 = 0 := follows_get_even w h.1 k hk hlet
      have hxsq : n ^ 2 ≤ x := even_ge_sq_of_aboveAnchor h hk1 hxeven
      have hx441 : 441 ≤ x := by nlinarith
      have hstep := log_floorPower_even_ge (x := x) hx441 hxeven
      -- loss comparison: `1.05/√x ≤ 1.05/n` from `√x ≥ n`
      have hsx : (n : ℝ) ≤ Real.sqrt x := by
        rw [show ((n : ℝ)) = Real.sqrt ((n : ℝ) ^ 2) by
          rw [Real.sqrt_sq (by linarith)]]
        exact Real.sqrt_le_sqrt (by exact_mod_cast hxsq)
      have hloss : 1.05 / Real.sqrt x ≤ 1.05 / n :=
        div_le_div_of_nonneg_left (by norm_num) hnpos hsx
      -- weight and deficit steps
      have hWs : walkWeight w (k + 1) = W / 2 :=
        walkWeight_succ_even hk hlet
      have hDs : prefixDeficit n w (k + 1) =
          prefixDeficit n w k + 1.05 / n := by
        rw [prefixDeficit_succ, List.getElem?_eq_getElem hk, hlet]
        simp
      have hW1' : 1 ≤ walkWeight w (k + 1) :=
        one_le_walkWeight_aboveAnchor hn2 h hk1
      rw [hWs] at hW1'
      have hWc : 1.05 / (n : ℝ) ≤ W / 2 * (1.05 / n) :=
        le_mul_of_one_le_left (by positivity) hW1'
      rw [hiter, hWs, hDs]
      calc W / 2 * (Real.log n - (prefixDeficit n w k + 1.05 / n))
          = 1 / 2 * (W * A) - W / 2 * (1.05 / n) := by
            rw [hAdef]; ring
        _ ≤ Real.log x / 2 - 1.05 / n := by
            have := mul_le_mul_of_nonneg_left hIH
              (by norm_num : (0 : ℝ) ≤ 1 / 2)
            linarith
        _ ≤ Real.log x / 2 - 1.05 / Real.sqrt x := by linarith
        _ ≤ Real.log (floorPower x) := by linarith

/-- **Transport on open descent-free prefixes** (log form): on
`AboveAnchor n w` with `n ≥ 400`, every state satisfies
`w_k·(log n − D) ≤ log x_k` with `D = 1.05·e/n + 0.7·o/(n·√n)`.
The open-trajectory form of `cycleMin_transport`. -/
theorem aboveAnchor_transport {n : ℕ} {w : List Branch}
    (hn : 400 ≤ n) (h : AboveAnchor n w) {k : ℕ} (hk : k ≤ w.length) :
    walkWeight w k * (Real.log n - transportDeficit n w) ≤
      Real.log (floorPower^[k] n) := by
  have hle : prefixDeficit n w k ≤ transportDeficit n w := by
    rw [← prefixDeficit_length n w]
    exact prefixDeficit_mono n w hk
  calc walkWeight w k * (Real.log n - transportDeficit n w)
      ≤ walkWeight w k * (Real.log n - prefixDeficit n w k) :=
        mul_le_mul_of_nonneg_left (by linarith) (walkWeight_nonneg w k)
    _ ≤ Real.log (floorPower^[k] n) :=
        aboveAnchor_transport_prefix hn h k hk

/-- **Flight envelope** (fly-height sandwich): on an open descent-free
prefix with anchor `n ≥ 400`,

`w_k·(log n − D) ≤ log x_k ≤ w_k·log n`.

At the prefix peak `H` with `W = max_k w_k` this gives
`W·(log n − D) ≤ log H ≤ W·log n`: the fly exponent
`log H / log n` equals the peak walk weight up to `O(D·W/log n)`.
Not a halt theorem and not a divergence theorem. -/
theorem aboveAnchor_flight_envelope {n : ℕ} {w : List Branch}
    (hn : 400 ≤ n) (h : AboveAnchor n w) {k : ℕ} (hk : k ≤ w.length) :
    walkWeight w k * (Real.log n - transportDeficit n w) ≤
        Real.log (floorPower^[k] n) ∧
      Real.log (floorPower^[k] n) ≤ walkWeight w k * Real.log n :=
  ⟨aboveAnchor_transport hn h hk,
    follows_log_le_walkWeight (by omega) h.1 hk⟩

end Problems.Juggler
