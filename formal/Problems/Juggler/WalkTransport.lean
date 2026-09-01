import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic
import Problems.Juggler.CycleFinance

namespace Problems.Juggler

/-!
# Transport to a reduced base (Paper A Theorem 5.3)

On a minimum-based cycle with minimum `n ≥ 400`, every state
satisfies, in log form,

`walkWeight w k * (log n − D) ≤ log x_k`,

where `walkWeight w k = 3^(a_k)/2^k` is the walk weight
`w_k = 2^(u_k)` (rational — no real exponentiation is needed),
`a_k` is the odd count of the length-`k` prefix, and
`D = 1.05·e/n + 0.7·o/(n·√n)` is the transport deficit over the
full word. Exponentiating gives the paper's
`x_k ≥ (n e^{−D})^{w_k}`.

The proof is the paper's: per-step floor losses
`log T(x) ≥ (3/2)·log x − 1.05/(x√x)` (odd) and
`log T(x) ≥ (1/2)·log x − 1.05/√x` (even), from the floor cells
and `−log(1−t) ≤ 1.05·t` on `t ≤ 1/21`; the amplification is the
exact weight recursion `w_{k+1} = (3/2)·w_k` (odd), `w_k/2`
(even); odd injections are priced at `x_j ≥ n`
(`cycleMin_iterate_ge`) against `w_{j+1} ≥ 3/2`, even injections
at `x_j ≥ n²` (`cycleMin_even_ge_sq`) against `w_{j+1} ≥ 1`
(`cycleMin_prefix_pow_le`).

This certifies the transport inequality itself. The walk-charge
consequence (the DP over nonnegative closed walks at the reduced
base) and the Denjoy–Koksma envelope stay human proofs. Not a
cycle obstruction and not a halt theorem.
-/

/-!
## The elementary log inequality
-/

/-- `−log(1−t) ≤ 1.05·t` for `0 ≤ t ≤ 1/21`. -/
theorem neg_log_one_sub_le {t : ℝ} (h0 : 0 ≤ t) (h1 : t ≤ 1 / 21) :
    -Real.log (1 - t) ≤ 1.05 * t := by
  have hpos : 0 < 1 - t := by linarith
  have h2 : Real.log (1 - t)⁻¹ ≤ (1 - t)⁻¹ - 1 :=
    Real.log_le_sub_one_of_pos (by positivity)
  rw [Real.log_inv] at h2
  have h3 : (1 - t)⁻¹ - 1 = t / (1 - t) := by field_simp; ring
  have h4 : t / (1 - t) ≤ 1.05 * t := by
    rw [div_le_iff₀ hpos]
    nlinarith
  linarith

/-!
## Per-step floor losses
-/

/-- Even step, lower side: for even `x ≥ 441`,
`log T(x) ≥ (1/2)·log x − 1.05/√x`. -/
theorem log_floorPower_even_ge {x : ℕ} (hx : 441 ≤ x) (he : x % 2 = 0) :
    Real.log x / 2 - 1.05 / Real.sqrt x ≤ Real.log (floorPower x) := by
  have hcell :=
    (floorPower_even_eq_iff_sq_interval (n := x) (M := floorPower x) he).mp rfl
  have hxpos : (0 : ℝ) < x := by positivity
  have hs21 : (21 : ℝ) ≤ Real.sqrt x := by
    rw [show (21 : ℝ) = Real.sqrt 441 by
      rw [show (441 : ℝ) = 21 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_le_sqrt (by exact_mod_cast hx)
  have hspos : (0 : ℝ) < Real.sqrt x := by linarith
  -- the cell gives `√x < M + 1`
  have hlt : Real.sqrt x < (floorPower x : ℝ) + 1 := by
    rw [Real.sqrt_lt' (by positivity)]
    exact_mod_cast hcell.2
  -- so `M ≥ √x − 1 = √x·(1 − 1/√x)`
  set t : ℝ := 1 / Real.sqrt x with ht
  have ht0 : 0 ≤ t := by positivity
  have ht21 : t ≤ 1 / 21 := by
    rw [ht, div_le_div_iff₀ hspos (by norm_num)]
    linarith
  have hfac : Real.sqrt x * (1 - t) = Real.sqrt x - 1 := by
    rw [ht]; field_simp
  have hM : Real.sqrt x * (1 - t) ≤ (floorPower x : ℝ) := by
    rw [hfac]; linarith
  have h1t : (0 : ℝ) < 1 - t := by
    have : t ≤ 1 / 21 := ht21
    linarith
  have hlog : Real.log (Real.sqrt x * (1 - t)) ≤ Real.log (floorPower x) :=
    Real.log_le_log (by positivity) hM
  rw [Real.log_mul (by positivity) (by linarith), Real.log_sqrt (le_of_lt hxpos)]
    at hlog
  have hbound := neg_log_one_sub_le ht0 ht21
  have : -(1.05 * t) ≤ Real.log (1 - t) := by linarith
  rw [ht] at this
  have h105 : 1.05 * (1 / Real.sqrt x) = 1.05 / Real.sqrt x := by ring
  rw [h105] at this
  linarith

/-- Odd step, lower side: for odd `x ≥ 9`,
`log T(x) ≥ (3/2)·log x − 1.05/(x·√x)`. -/
theorem log_floorPower_odd_ge {x : ℕ} (hx : 9 ≤ x) (ho : x % 2 = 1) :
    3 * Real.log x / 2 - 1.05 / (x * Real.sqrt x) ≤
      Real.log (floorPower x) := by
  have hcell :=
    (floorPower_odd_eq_iff_cube_interval (n := x) (M := floorPower x) ho).mp rfl
  have hxpos : (0 : ℝ) < x := by positivity
  have hx9 : (9 : ℝ) ≤ x := by exact_mod_cast hx
  have hs3 : (3 : ℝ) ≤ Real.sqrt x := by
    rw [show (3 : ℝ) = Real.sqrt 9 by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]]
    exact Real.sqrt_le_sqrt hx9
  have hspos : (0 : ℝ) < Real.sqrt x := by linarith
  have hxs : (27 : ℝ) ≤ x * Real.sqrt x := by nlinarith
  have hxspos : (0 : ℝ) < x * Real.sqrt x := by positivity
  -- `√(x³) = x·√x`
  have hcube : Real.sqrt ((x : ℝ) ^ 3) = x * Real.sqrt x := by
    rw [show ((x : ℝ)) ^ 3 = (x : ℝ) ^ 2 * x by ring,
      Real.sqrt_mul (by positivity), Real.sqrt_sq (le_of_lt hxpos)]
  -- the cell gives `√(x³) < M + 1`
  have hlt : x * Real.sqrt x < (floorPower x : ℝ) + 1 := by
    rw [← hcube, Real.sqrt_lt' (by positivity)]
    exact_mod_cast hcell.2
  set t : ℝ := 1 / (x * Real.sqrt x) with ht
  have ht0 : 0 ≤ t := by positivity
  have ht21 : t ≤ 1 / 21 := by
    rw [ht, div_le_div_iff₀ hxspos (by norm_num)]
    linarith
  have hfac : (x * Real.sqrt x) * (1 - t) = x * Real.sqrt x - 1 := by
    rw [ht]; field_simp
  have hM : (x * Real.sqrt x) * (1 - t) ≤ (floorPower x : ℝ) := by
    rw [hfac]; linarith
  have h1t : (0 : ℝ) < 1 - t := by linarith
  have hlog : Real.log ((x * Real.sqrt x) * (1 - t)) ≤
      Real.log (floorPower x) :=
    Real.log_le_log (by positivity) hM
  rw [Real.log_mul (by positivity) (by linarith),
    Real.log_mul (ne_of_gt hxpos) (ne_of_gt hspos),
    Real.log_sqrt (le_of_lt hxpos)] at hlog
  have hbound := neg_log_one_sub_le ht0 ht21
  have hlow : -(1.05 * t) ≤ Real.log (1 - t) := by linarith
  rw [ht] at hlow
  have h105 : 1.05 * (1 / (x * Real.sqrt x)) = 1.05 / (x * Real.sqrt x) := by
    ring
  rw [h105] at hlow
  linarith

/-!
## Walk weight and transport deficit
-/

/-- The walk weight `w_k = 2^(u_k) = 3^(a_k)/2^k` — rational. -/
noncomputable def walkWeight (w : List Branch) (k : ℕ) : ℝ :=
  3 ^ oddCount (w.take k) / 2 ^ k

@[simp] theorem walkWeight_zero (w : List Branch) : walkWeight w 0 = 1 := by
  simp [walkWeight]

theorem oddCount_take_succ {w : List Branch} {k : ℕ} (hk : k < w.length) :
    oddCount (w.take (k + 1)) =
      oddCount (w.take k) + if w[k] = .odd then 1 else 0 := by
  rw [List.take_add_one, List.getElem?_eq_getElem hk]
  cases h : w[k] <;> simp [oddCount_append]

theorem walkWeight_succ_odd {w : List Branch} {k : ℕ} (hk : k < w.length)
    (h : w[k] = .odd) :
    walkWeight w (k + 1) = 3 / 2 * walkWeight w k := by
  rw [walkWeight, walkWeight, oddCount_take_succ hk, h]
  simp [pow_succ]
  ring

theorem walkWeight_succ_even {w : List Branch} {k : ℕ} (hk : k < w.length)
    (h : w[k] = .even) :
    walkWeight w (k + 1) = walkWeight w k / 2 := by
  rw [walkWeight, walkWeight, oddCount_take_succ hk, h]
  simp [pow_succ]
  ring

/-- Cycle minimality forces `u_k ≥ 0`, that is `w_k ≥ 1`
(`cycleMin_prefix_pow_le` in weight form). -/
theorem one_le_walkWeight {n : ℕ} {w : List Branch} (hn : 2 ≤ n)
    (h : CycleMin n w) {k : ℕ} (hk : k ≤ w.length) :
    1 ≤ walkWeight w k := by
  have hpow := cycleMin_prefix_pow_le hn h k hk
  rw [walkWeight, le_div_iff₀ (by positivity), one_mul]
  exact_mod_cast hpow

theorem walkWeight_nonneg (w : List Branch) (k : ℕ) :
    0 ≤ walkWeight w k := by
  rw [walkWeight]; positivity

/-- Accumulated transport deficit along the first `k` letters:
`0.7/(n√n)` per odd letter, `1.05/n` per even letter. -/
noncomputable def prefixDeficit (n : ℕ) (w : List Branch) : ℕ → ℝ
  | 0 => 0
  | k + 1 => prefixDeficit n w k +
      if w[k]? = some .odd then 0.7 / (n * Real.sqrt n) else 1.05 / n

theorem prefixDeficit_succ (n : ℕ) (w : List Branch) (k : ℕ) :
    prefixDeficit n w (k + 1) = prefixDeficit n w k +
      if w[k]? = some .odd then 0.7 / (n * Real.sqrt n) else 1.05 / n :=
  rfl

theorem prefixDeficit_mono (n : ℕ) (w : List Branch) {j k : ℕ}
    (h : j ≤ k) : prefixDeficit n w j ≤ prefixDeficit n w k := by
  induction k with
  | zero => simp [Nat.le_zero.mp h]
  | succ k ih =>
    rcases Nat.lt_or_ge j (k + 1) with hlt | hge
    · have h1 := ih (Nat.lt_succ_iff.mp hlt)
      have h2 : (0 : ℝ) ≤
          if w[k]? = some .odd then 0.7 / (n * Real.sqrt n) else 1.05 / n := by
        split <;> positivity
      rw [prefixDeficit_succ]
      linarith
    · have hj : j = k + 1 := Nat.le_antisymm h hge
      simp [hj]

/-- The transport deficit over the full word:
`D = 1.05·e/n + 0.7·o/(n·√n)`. -/
noncomputable def transportDeficit (n : ℕ) (w : List Branch) : ℝ :=
  1.05 * ((w.length : ℝ) - oddCount w) / n +
    0.7 * oddCount w / (n * Real.sqrt n)

/-- The prefix deficit in closed count form. -/
theorem prefixDeficit_eq (n : ℕ) (w : List Branch) :
    ∀ {k : ℕ}, k ≤ w.length →
      prefixDeficit n w k =
        1.05 * ((k : ℝ) - oddCount (w.take k)) / n +
          0.7 * oddCount (w.take k) / (n * Real.sqrt n) := by
  intro k
  induction k with
  | zero => intro _; simp [prefixDeficit]
  | succ k ih =>
    intro hk1
    have hk : k < w.length := hk1
    rw [prefixDeficit_succ, ih (le_of_lt hk), List.getElem?_eq_getElem hk,
      oddCount_take_succ hk]
    cases h : w[k] <;> · simp; ring

/-- The full-word prefix deficit is the transport deficit. -/
theorem prefixDeficit_length (n : ℕ) (w : List Branch) :
    prefixDeficit n w w.length = transportDeficit n w := by
  rw [prefixDeficit_eq n w le_rfl, List.take_length, transportDeficit]

/-!
## The transport induction
-/

/-- Transport invariant along the cycle:
`w_k·(log n − D_k) ≤ log x_k` with the running prefix deficit. -/
theorem cycleMin_transport_prefix {n : ℕ} {w : List Branch}
    (hn : 400 ≤ n) (h : CycleMin n w) :
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
    have hxge : n ≤ x := cycleMin_iterate_ge h k (le_of_lt hk)
    set W := walkWeight w k with hWdef
    set A := Real.log n - prefixDeficit n w k with hAdef
    have hW1 : 1 ≤ W := one_le_walkWeight hn2 h (le_of_lt hk)
    cases hlet : w[k] with
    | odd =>
      have hxodd : x % 2 = 1 := follows_get_odd w h.1.1 k hk hlet
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
      have hxeven : x % 2 = 0 := follows_get_even w h.1.1 k hk hlet
      have hxsq : n ^ 2 ≤ x := cycleMin_even_ge_sq hn2 h hk hxeven
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
        one_le_walkWeight hn2 h hk1
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

/-- **Transport to a reduced base** (Paper A Theorem 5.3, log
form): on a minimum-based cycle with minimum `n ≥ 400`, every
state satisfies `w_k·(log n − D) ≤ log x_k` with
`D = 1.05·e/n + 0.7·o/(n·√n)`. Exponentiating gives
`x_k ≥ (n e^{−D})^{w_k}`. -/
theorem cycleMin_transport {n : ℕ} {w : List Branch}
    (hn : 400 ≤ n) (h : CycleMin n w) {k : ℕ} (hk : k ≤ w.length) :
    walkWeight w k * (Real.log n - transportDeficit n w) ≤
      Real.log (floorPower^[k] n) := by
  have hle : prefixDeficit n w k ≤ transportDeficit n w := by
    rw [← prefixDeficit_length n w]
    exact prefixDeficit_mono n w hk
  calc walkWeight w k * (Real.log n - transportDeficit n w)
      ≤ walkWeight w k * (Real.log n - prefixDeficit n w k) :=
        mul_le_mul_of_nonneg_left (by linarith) (walkWeight_nonneg w k)
    _ ≤ Real.log (floorPower^[k] n) :=
        cycleMin_transport_prefix hn h k hk

end Problems.Juggler
