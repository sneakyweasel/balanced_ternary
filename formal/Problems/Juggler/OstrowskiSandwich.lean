import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

namespace Problems.Juggler

/-!
# Ostrowski sandwich for θ = log(3/2)/log 3

Paper A Section 5.5 decomposes hug-word prefixes into blocks of
convergent denominators of `θ = log(3/2)/log 3` and applies
Denjoy–Koksma per block. The convergent data are certified there by
an interval continued fraction on a big-integer sandwich.

This file certifies that arithmetic:

* the two big-integer power inequalities
  `3^10781274 < 2^17087915` and `2^16785921 < 3^10590737`
  (`theta_sandwich_upper`, `theta_sandwich_lower`);
* the resulting real sandwich
  `6195184/16785921 < θ < 6306641/17087915`
  (`lower_lt_walkTheta`, `walkTheta_lt_upper`);
* both rational endpoints have continued-fraction quotients starting
  `[2, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1]`, with further quotients
  remaining (`cf_lower_prefix`, `cf_upper_prefix`,
  `cf_lower_continues`, `cf_upper_continues`);
* the standard convergent recurrence on those quotients produces the
  denominator list
  `1, 2, 3, 8, 19, 65, 84, 485, 1054, 24727, 50508, 125743, 176251`
  (`theta_convergent_denominators`);
* the greedy Ostrowski digit scan of Paper A Theorem 5.8: every
  window length `50508 ≤ L < 301994` decomposes into certified
  blocks with digit sum at most `37` (`window_digit_scan`,
  `window_digit_cap`), attained at `L = 275632`
  (`window_digit_max`).

The bridge from the shared endpoint prefix to the continued fraction
of `θ` itself is the classical cylinder-interval fact (KNOWN); it is
used as prose in Paper A and is not re-proved here. Denjoy–Koksma is
likewise KNOWN. Not a cycle obstruction and not a halt theorem.
-/

/-- Upper side of the sandwich: `3^10781274 < 2^17087915`,
hence `log 2 / log 3 > 10781274 / 17087915`. -/
theorem theta_sandwich_upper : (3 : ℕ) ^ 10781274 < 2 ^ 17087915 := by
  native_decide

/-- Lower side of the sandwich: `2^16785921 < 3^10590737`,
hence `log 2 / log 3 < 10590737 / 16785921`. -/
theorem theta_sandwich_lower : (2 : ℕ) ^ 16785921 < 3 ^ 10590737 := by
  native_decide

/-- The rotation number of the hug walk in Paper A Section 5:
`θ = log(3/2)/log 3`. -/
noncomputable def walkTheta : ℝ := Real.log (3 / 2) / Real.log 3

/-- Real form of the lower sandwich: `6195184/16785921 < θ`. -/
theorem lower_lt_walkTheta : (6195184 : ℝ) / 16785921 < walkTheta := by
  have hlog3 : 0 < Real.log 3 := Real.log_pos (by norm_num)
  have key : (16785921 : ℝ) * Real.log 2 < 10590737 * Real.log 3 := by
    have hc : ((2 : ℝ)) ^ (16785921 : ℕ) < (3 : ℝ) ^ (10590737 : ℕ) := by
      exact_mod_cast theta_sandwich_lower
    have hlt := Real.log_lt_log (by positivity) hc
    simpa [Real.log_pow] using hlt
  rw [walkTheta, Real.log_div (by norm_num) (by norm_num),
    div_lt_div_iff₀ (by norm_num) hlog3]
  nlinarith [key]

/-- Real form of the upper sandwich: `θ < 6306641/17087915`. -/
theorem walkTheta_lt_upper : walkTheta < (6306641 : ℝ) / 17087915 := by
  have hlog3 : 0 < Real.log 3 := Real.log_pos (by norm_num)
  have key : (10781274 : ℝ) * Real.log 3 < 17087915 * Real.log 2 := by
    have hc : ((3 : ℝ)) ^ (10781274 : ℕ) < (2 : ℝ) ^ (17087915 : ℕ) := by
      exact_mod_cast theta_sandwich_upper
    have hlt := Real.log_lt_log (by positivity) hc
    simpa [Real.log_pow] using hlt
  rw [walkTheta, Real.log_div (by norm_num) (by norm_num),
    div_lt_div_iff₀ hlog3 (by norm_num)]
  nlinarith [key]

/-- Continued-fraction quotients of the fraction `p/q ∈ (0,1)` by
Euclid, most significant first, fuel-bounded: the first quotient of
`p/q` is `⌊q/p⌋` and the tail is the expansion of `(q mod p)/p`. -/
def cfQuotients : ℕ → ℕ → ℕ → List ℕ
  | 0, _, _ => []
  | _ + 1, _, 0 => []
  | fuel + 1, q, p + 1 => (q / (p + 1)) :: cfQuotients fuel (p + 1) (q % (p + 1))

/-- The certified quotient prefix of `θ` after the leading zero:
`θ = [0; 2, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, …]`. -/
def thetaQuotients : List ℕ := [2, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1]

/-- The lower endpoint opens with the certified quotients. -/
theorem cf_lower_prefix :
    (cfQuotients 64 16785921 6195184).take 12 = thetaQuotients := by
  native_decide

/-- The upper endpoint opens with the certified quotients. -/
theorem cf_upper_prefix :
    (cfQuotients 64 17087915 6306641).take 12 = thetaQuotients := by
  native_decide

/-- The lower endpoint's expansion continues past the shared prefix. -/
theorem cf_lower_continues :
    12 < (cfQuotients 64 16785921 6195184).length := by
  native_decide

/-- The upper endpoint's expansion continues past the shared prefix. -/
theorem cf_upper_continues :
    12 < (cfQuotients 64 17087915 6306641).length := by
  native_decide

/-- Convergent denominators from a quotient list by the standard
recurrence `q_n = a_n q_{n-1} + q_{n-2}`, with `q_{-1} = 0` and
`q_0 = 1` prepended to the output. -/
def convergentDenoms (as : List ℕ) : List ℕ :=
  (as.foldl
    (fun (st : ℕ × ℕ × List ℕ) a =>
      let next := a * st.2.1 + st.1
      (st.2.1, next, st.2.2 ++ [next]))
    (0, 1, [1])).2.2

/-- The certified quotients produce exactly the block-denominator
list used by Paper A Theorem 5.7 and the window digit caps of
Theorem 5.8. -/
theorem theta_convergent_denominators :
    convergentDenoms thetaQuotients =
      [1, 2, 3, 8, 19, 65, 84, 485, 1054, 24727, 50508, 125743, 176251] := by
  native_decide

/-- The window endpoint `q₁₃ = 301994 = 1·176251 + 125743`, the next
denominator after the certified list. -/
theorem theta_window_endpoint : 176251 + 125743 = 301994 := by norm_num

/-!
## The window digit scan (Paper A Theorem 5.8, arithmetic core)

Theorem 5.8 controls the Denjoy–Koksma budget on the window
`50508 ≤ L < 301994` by the greedy Ostrowski digit sum `s(L)` over
the certified denominators. The scan below certifies both the
decomposition identity `L = Σ bⱼ qⱼ` and the exact cap
`s(L) ≤ 37` for every length in the window, replacing the
previously computational scan. The Denjoy–Koksma comparison that
turns `s(L)` into a charge bound stays analytic (KNOWN, prose).
-/

/-- The certified denominators, largest block first, ending in `1`
so the greedy remainder is always exhausted. -/
def thetaDenomsDesc : List ℕ :=
  [176251, 125743, 50508, 24727, 1054, 485, 84, 65, 19, 8, 3, 2, 1]

/-- Greedy Ostrowski digits of `L`: peel the largest certified
denominator repeatedly, most significant digit first. -/
def greedyDigits (L : ℕ) : List ℕ :=
  (thetaDenomsDesc.foldl
    (fun (st : ℕ × List ℕ) q => (st.1 % q, st.2 ++ [st.1 / q]))
    (L, [])).2

/-- The greedy digit sum `s(L) = Σ bⱼ`. -/
def greedyDigitSum (L : ℕ) : ℕ := (greedyDigits L).sum

/-- Reconstruction `Σ bⱼ qⱼ` of the greedy decomposition. -/
def greedyReconstruct (L : ℕ) : ℕ :=
  (((greedyDigits L).zip thetaDenomsDesc).map fun p => p.1 * p.2).sum

/-- **Window digit scan**: for every `L` in the window
`[50508, 301994)`, the greedy digits reconstruct `L` and their sum
is at most `37`. -/
theorem window_digit_scan :
    ((List.range' 50508 251486).all fun L =>
      decide (greedyReconstruct L = L ∧ greedyDigitSum L ≤ 37)) = true := by
  native_decide

/-- The cap `37` is attained, at `L = 275632`. -/
theorem window_digit_max : greedyDigitSum 275632 = 37 := by native_decide

/-- Pointwise form of the scan: any window length decomposes
greedily into certified blocks with digit sum at most `37`. -/
theorem window_digit_cap {L : ℕ} (h1 : 50508 ≤ L) (h2 : L < 301994) :
    greedyReconstruct L = L ∧ greedyDigitSum L ≤ 37 := by
  have hall := List.all_eq_true.mp window_digit_scan L
    (List.mem_range'_1.mpr ⟨h1, by omega⟩)
  exact of_decide_eq_true hall

end Problems.Juggler
