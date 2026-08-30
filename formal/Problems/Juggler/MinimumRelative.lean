import Problems.Juggler.Scale

namespace Problems.Juggler

/-!
# Minimum-relative trajectory geometry

`AboveAnchor n w` is the shared finite-prefix hypothesis

```
follows n w  ∧  ∀ i ≤ |w|,  n ≤ T^i(n).
```

`CycleMin` and `MinimalNonTerm` are consumers: a cycle minimum
realizes it by the ge-filter plus return `T_w(n)=n`, and a
minimal non-1 start realizes it on every finite prefix because
the whole orbit stays `≥ n`. This file does not mention cycle
closure except as a hypothesis of `aboveAnchor_of_minimalNonTerm`
(which uses only the orbit lower bound). Cycle wrappers live in
`CycleCore` / `FirstInternalOO`.

Symbolic word envelopes stay in `Envelope` / `Scale`. The
semantic output of a drop is the existing `FiniteProgress`
certificate. This is not a halt theorem.
-/

/-- Every realized state along `w`, including the endpoint, is at
least the anchor `n`. -/
def AboveAnchor (n : ℕ) (w : List Branch) : Prop :=
  follows n w ∧ ∀ i, i ≤ w.length → n ≤ floorPower^[i] n

theorem aboveAnchor_follows {n : ℕ} {w : List Branch}
    (h : AboveAnchor n w) : follows n w :=
  h.1

theorem aboveAnchor_iterate_ge {n : ℕ} {w : List Branch} {i : ℕ}
    (h : AboveAnchor n w) (hi : i ≤ w.length) : n ≤ floorPower^[i] n :=
  h.2 i hi

theorem aboveAnchor_image_ge {n : ℕ} {w : List Branch}
    (h : AboveAnchor n w) : n ≤ image n w := by
  simpa [image_eq_iterate] using h.2 w.length le_rfl

/-- An anchor-relative prefix cannot drop. The image is at least `n`. -/
theorem aboveAnchor_not_lt {n : ℕ} {w : List Branch}
    (h : AboveAnchor n w) : ¬image n w < n :=
  fun hlt => (not_le_of_gt hlt) (aboveAnchor_image_ge h)

theorem aboveAnchor_of_prefix {n : ℕ} {u v : List Branch}
    (h : AboveAnchor n (u ++ v)) : AboveAnchor n u :=
  ⟨follows_of_append_left h.1, fun i hi =>
    h.2 i (by
      simp only [List.length_append]
      exact le_trans hi (Nat.le_add_right _ _))⟩

/-- A minimal non-1 orbit stays `≥ n` at every iterate, so every
realized finite prefix is minimum-relative. Not a cycle hypothesis. -/
theorem aboveAnchor_of_minimalNonTerm {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) (hw : follows n w) : AboveAnchor n w :=
  ⟨hw, fun i _ => minimal_nonterm_iterate_ge h i⟩

/-- Naming alias of `finiteProgress_of_imageLt`. A realized drop
below the start is the standard finite-progress certificate. -/
theorem finiteProgress_of_prefix_drop {n : ℕ} {w : List Branch}
    (hw : follows n w) (hlt : image n w < n) : FiniteProgress n :=
  finiteProgress_of_imageLt hw hlt

theorem follows_even_letter {m : ℕ} (he : m % 2 = 0) :
    follows m [Branch.even] :=
  ⟨he, trivial⟩

/-- Even cell: `T(x) < n ↔ x < n^2`. Shared square-trap primitive. -/
theorem even_below_square_iff {x n : ℕ} (he : x % 2 = 0) :
    floorPower x < n ↔ x < n ^ 2 := by
  rw [floorPower_even_eq he]
  simpa [pow_two] using (@Nat.sqrt_lt x n)

theorem even_below_square_drop {x n : ℕ} (he : x % 2 = 0)
    (hlt : x < n ^ 2) : floorPower x < n :=
  (even_below_square_iff he).mpr hlt

/-- Parameterized square trap: `x < n^{2k}` and `x` even give
`T(x) < n^k`. The `k = 1` case is `even_below_square_iff`. -/
theorem even_below_anchor_pow {x n k : ℕ} (he : x % 2 = 0) :
    floorPower x < n ^ k ↔ x < n ^ (2 * k) := by
  have h := even_below_square_iff (n := n ^ k) he
  have hsq : (n ^ k) ^ 2 = n ^ (2 * k) := by
    rw [pow_two, ← Nat.pow_add, Nat.two_mul]
  simpa [hsq] using h

/-- `k = 2`: even `x < n^4` gives `T(x) < n^2`. -/
theorem even_below_fourth {x n : ℕ} (he : x % 2 = 0) :
    floorPower x < n ^ 2 ↔ x < n ^ 4 :=
  even_below_anchor_pow (k := 2) he

/-- `k = 3`: even `x < n^6` gives `T(x) < n^3`. -/
theorem even_below_cube {x n : ℕ} (he : x % 2 = 0) :
    floorPower x < n ^ 3 ↔ x < n ^ 6 := by
  simpa [show (2 : ℕ) * 3 = 6 from rfl] using even_below_anchor_pow (k := 3) he

/-- If an even image sits below `n^2`, one more even letter is a
descent certificate. -/
theorem finiteProgress_of_even_below_square {n : ℕ} {w : List Branch}
    (hw : follows n w) (he : image n w % 2 = 0)
    (hlt : image n w < n ^ 2) : FiniteProgress n :=
  finiteProgress_of_prefix_drop
    (follows_append hw (follows_even_letter he))
    (by
      have hdrop := even_below_square_drop he hlt
      simpa [image_append, image] using hdrop)

/-- `k = 1` envelope gap is a descent certificate. -/
theorem finiteProgress_of_power_bound_lt_pow {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w)
    (hgap : 3 ^ oddCount w < 2 ^ w.length) : FiniteProgress n :=
  finiteProgress_of_prefix_drop hw (by
    have hlt := power_bound_lt_pow (k := 1) hn hw (by simpa using hgap)
    simpa [image_eq_iterate] using hlt)

/-- Square-cell pipeline: `power_bound_lt_pow (k := 2)` plus an even
image is `FiniteProgress`. -/
theorem finiteProgress_of_even_power_bound_square {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w) (he : image n w % 2 = 0)
    (hgap : 3 ^ oddCount w < 2 * 2 ^ w.length) : FiniteProgress n :=
  finiteProgress_of_even_below_square hw he
    (power_bound_lt_pow (k := 2) hn hw hgap)

/-- Cube cell plus even is a square cell for the next state:
`x < n^3 < n^4` and `even_below_fourth`. -/
theorem even_below_cube_cell {x n : ℕ} (hn : 2 ≤ n) (he : x % 2 = 0)
    (hlt : x < n ^ 3) : floorPower x < n ^ 2 :=
  (even_below_fourth he).mpr
    (lt_trans hlt (pow_lt_of_two_le hn (by decide : (3 : ℕ) < 4)))

/-- Even cube-not-square landing resets into the square cell. -/
theorem even_cube_not_square {x n : ℕ} (hn : 2 ≤ n) (he : x % 2 = 0)
    (hge : n ^ 2 ≤ x) (hlt : x < n ^ 3) :
    n ≤ floorPower x ∧ floorPower x < n ^ 2 :=
  ⟨by
      have hnot : ¬floorPower x < n := by
        intro hdrop
        exact (not_le_of_gt ((even_below_square_iff he).mp hdrop)) hge
      exact Nat.le_of_not_gt hnot,
    even_below_cube_cell hn he hlt⟩

/-- Odd cube-not-square landing lifts to at least `n^3`.
Companion of `odd_ge_succ_sq_floorPower_ge_cube`, with floor `n^2`. -/
theorem odd_ge_sq_floor_ge_cube {x n : ℕ} (hodd : x % 2 = 1)
    (hge : n ^ 2 ≤ x) : n ^ 3 ≤ floorPower x := by
  rw [floorPower_odd_eq hodd]
  refine Nat.le_sqrt.mpr ?_
  have hpow : (n ^ 2) ^ 3 ≤ x ^ 3 := Nat.pow_le_pow_left hge 3
  have hexp : (n ^ 3) ^ 2 = (n ^ 2) ^ 3 := by simp [← Nat.pow_mul]
  have : (n ^ 3) ^ 2 ≤ x ^ 3 := by rwa [hexp]
  simpa [pow_two] using this

/-- Two evens after a cube-cell even landing drop below `n`. -/
theorem finiteProgress_of_cube_even_even {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w)
    (he : image n w % 2 = 0) (hlt : image n w < n ^ 3)
    (he2 : floorPower (image n w) % 2 = 0) : FiniteProgress n :=
  finiteProgress_of_even_below_square
    (follows_append hw (follows_even_letter he))
    (by simpa [image_append, image] using he2)
    (by simpa [image_append, image] using even_below_cube_cell hn he hlt)

/-- On a CE, a cube-cell even landing is followed by an odd image. -/
theorem minimal_cube_even_forces_odd_image {n : ℕ} {w : List Branch}
    (h : MinimalNonTerm n) (hw : follows n w)
    (he : image n w % 2 = 0) (hlt : image n w < n ^ 3) :
    floorPower (image n w) % 2 = 1 := by
  have hn : 2 ≤ n :=
    le_trans (by decide : (2 : ℕ) ≤ 12) (minimal_nonterm_ge_twelve h)
  by_contra heven
  have he2 : floorPower (image n w) % 2 = 0 := by omega
  exact minimal_nonterm_not_finiteProgress h
    (finiteProgress_of_cube_even_even hn hw he hlt he2)

theorem even_ge_sq_of_succ_ge {x n : ℕ} (he : x % 2 = 0)
    (hge : n ≤ floorPower x) : n ^ 2 ≤ x := by
  rw [floorPower_even_eq he] at hge
  exact (by simpa [pow_two] using Nat.le_sqrt.mp hge)

/-- On an anchor prefix the next state is still `≥ n`, so an even
current state sits at or above `n^2`. -/
theorem even_ge_sq_of_aboveAnchor {n : ℕ} {w : List Branch} {i : ℕ}
    (h : AboveAnchor n w) (hi : i + 1 ≤ w.length)
    (he : floorPower^[i] n % 2 = 0) :
    n ^ 2 ≤ floorPower^[i] n :=
  even_ge_sq_of_succ_ge he (by
    have := aboveAnchor_iterate_ge h hi
    simpa [Function.iterate_succ_apply'] using this)

theorem odd_floor_lt_sq {n : ℕ} (hn : 2 ≤ n) (hodd : n % 2 = 1) :
    floorPower n < n ^ 2 := by
  rw [floorPower_odd_eq hodd]
  refine Nat.sqrt_lt.mpr ?_
  have hn1 : 1 < n := lt_of_lt_of_le (by decide : (1 : ℕ) < 2) hn
  have hpow : n ^ 3 < n ^ 4 :=
    Nat.pow_lt_pow_right hn1 (by decide : (3 : ℕ) < 4)
  have h4 : n ^ 4 = n ^ 2 * n ^ 2 := Nat.pow_add n 2 2
  simpa [h4] using hpow

/-- An `OE` start cannot stay at or above the anchor: the first even
residual is below `n^2`. -/
theorem aboveAnchor_not_odd_even {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : AboveAnchor n (.odd :: .even :: v)) : False := by
  have hodd : n % 2 = 1 := h.1.1
  have he : floorPower n % 2 = 0 := h.1.2.1
  have hlt := odd_floor_lt_sq hn hodd
  have hlen : (1 : ℕ) + 1 ≤ (.odd :: .even :: v).length := by simp
  have hsq := even_ge_sq_of_aboveAnchor (i := 1) h hlen (by simpa using he)
  have : floorPower^[1] n = floorPower n := by simp
  rw [this] at hsq
  exact (not_le_of_gt hlt) hsq

theorem minimal_nonterm_not_follow_odd_even {n : ℕ} {v : List Branch}
    (h : MinimalNonTerm n) (hw : follows n (.odd :: .even :: v)) : False :=
  aboveAnchor_not_odd_even
    (le_trans (by decide : (2 : ℕ) ≤ 12) (minimal_nonterm_ge_twelve h))
    (aboveAnchor_of_minimalNonTerm h hw)

/-!
## First internal `OO`

A. Syntax: `isolatedPrefix` / `firstOOState` / `FirstInternalOO`.
B. Algebra: `isolated_oe_ge_implies_exponent` / `isolated_oe_r_bound`.
C. Semantics: CycleMin / MinimalNonTerm consumers stay in
`FirstInternalOO.lean`.

The comparison `2^{a+2r+1} ≤ 3^{a+r}` is a survival bound for
`O^a E (OE)^r`. It does not use cycle return.
-/

def isolatedPrefix (a r : ℕ) : List Branch :=
  oddEvenBlock a 1 ++ repeatedOE r

def firstOOState (n a r : ℕ) : ℕ :=
  image n (isolatedPrefix a r)

def firstInternalOOWord (a r b : ℕ) (v : List Branch) : List Branch :=
  isolatedPrefix a r ++ List.replicate b Branch.odd ++ v

/-- Canonical first-internal-`OO` shape: the displayed `O^b` is a
maximal odd run. -/
def FirstInternalOO (w : List Branch) : Prop :=
  ∃ a r b v,
    2 ≤ a ∧ 2 ≤ b ∧
      w = firstInternalOOWord a r b v ∧
        v.head? ≠ some Branch.odd

def isolatedOESurvives (a r : ℕ) : Prop :=
  2 ^ (a + 2 * r + 1) ≤ 3 ^ (a + r)

theorem isolatedPrefix_zero (a : ℕ) :
    isolatedPrefix a 0 = oddEvenBlock a 1 := by
  simp [isolatedPrefix, repeatedOE]

theorem isolatedPrefix_succ (a r : ℕ) :
    isolatedPrefix a (r + 1) =
      oddEvenBlock a 1 ++ wordOE ++ repeatedOE r := by
  simp [isolatedPrefix, repeatedOE_succ]

theorem isolatedPrefix_two_one :
    isolatedPrefix 2 1 = oddEvenBlock 2 1 ++ wordOE := by
  simp [isolatedPrefix, repeatedOE]

theorem oddEvenBlock_one_append (a : ℕ) (w : List Branch) :
    oddEvenBlock a 1 ++ w =
      List.replicate a Branch.odd ++ Branch.even :: w := by
  simp [oddEvenBlock]

theorem four_pow_mul_two_pow (r a : ℕ) :
    4 ^ r * 2 ^ (a + 1) = 2 ^ (a + 2 * r + 1) := by
  rw [four_pow_eq_two_pow_two_mul, ← Nat.pow_add]
  congr 1
  ring

theorem length_isolatedPrefix (a r : ℕ) :
    (isolatedPrefix a r).length = a + 1 + 2 * r := by
  simp [isolatedPrefix, length_oddEvenBlock, length_repeatedOE, Nat.mul_comm]

theorem oddCount_isolatedPrefix (a r : ℕ) :
    oddCount (isolatedPrefix a r) = a + r := by
  simp [isolatedPrefix, oddCount_append, oddCount_oddEvenBlock,
    oddCount_repeatedOE]

/-- Isolated-odd survival bound: staying at least `n` forces
`2^{a+2r+1} ≤ 3^{a+r}`. -/
theorem isolatedOddSurvival_bound {n a r : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix a r))
    (hge : n ≤ image n (isolatedPrefix a r)) :
    isolatedOESurvives a r := by
  set y := image n (oddEvenBlock a 1)
  set z := image n (isolatedPrefix a r)
  have hy : follows n (oddEvenBlock a 1) :=
    follows_of_append_left (v := repeatedOE r) hw
  have hz : follows y (repeatedOE r) := by
    simpa [y, isolatedPrefix] using follows_of_append_right hw
  have henv : y ^ (2 ^ (a + 1)) ≤ n ^ (3 ^ a) := by
    have h := power_bound_word hy
    simpa [y, image_eq_iterate, length_oddEvenBlock, oddCount_oddEvenBlock]
      using h
  have hoe : z ^ (4 ^ r) ≤ y ^ (3 ^ r) := by
    have h := repeated_oe_scale hz
    have hz' : z = floorPower^[2 * r] y := by
      calc z
          = image y (repeatedOE r) := by
              simp [z, y, isolatedPrefix, image_append]
          _ = floorPower^[(repeatedOE r).length] y := image_eq_iterate y _
          _ = floorPower^[2 * r] y := by rw [length_repeatedOE]
    simpa [hz'] using h
  have hn1 : 1 < n := lt_of_lt_of_le (by decide : (1 : ℕ) < 2) hn
  have hnpow : n ^ (4 ^ r) ≤ y ^ (3 ^ r) :=
    le_trans (Nat.pow_le_pow_left hge _) hoe
  have hraise :
      (n ^ (4 ^ r)) ^ (2 ^ (a + 1)) ≤ (y ^ (3 ^ r)) ^ (2 ^ (a + 1)) :=
    Nat.pow_le_pow_left hnpow _
  have hL : (n ^ (4 ^ r)) ^ (2 ^ (a + 1)) = n ^ (4 ^ r * 2 ^ (a + 1)) :=
    (Nat.pow_mul n (4 ^ r) (2 ^ (a + 1))).symm
  have hR : (y ^ (3 ^ r)) ^ (2 ^ (a + 1)) = (y ^ (2 ^ (a + 1))) ^ (3 ^ r) := by
    rw [← Nat.pow_mul y (3 ^ r), ← Nat.pow_mul y (2 ^ (a + 1))]
    rw [Nat.mul_comm (3 ^ r)]
  have hmid : (y ^ (2 ^ (a + 1))) ^ (3 ^ r) ≤ (n ^ (3 ^ a)) ^ (3 ^ r) :=
    Nat.pow_le_pow_left henv _
  have hN : (n ^ (3 ^ a)) ^ (3 ^ r) = n ^ (3 ^ (a + r)) := by
    rw [← Nat.pow_mul, ← Nat.pow_add]
  have hchain : n ^ (4 ^ r * 2 ^ (a + 1)) ≤ n ^ (3 ^ (a + r)) := by
    calc
      n ^ (4 ^ r * 2 ^ (a + 1)) = (n ^ (4 ^ r)) ^ (2 ^ (a + 1)) := hL.symm
      _ ≤ (y ^ (3 ^ r)) ^ (2 ^ (a + 1)) := hraise
      _ = (y ^ (2 ^ (a + 1))) ^ (3 ^ r) := hR
      _ ≤ (n ^ (3 ^ a)) ^ (3 ^ r) := hmid
      _ = n ^ (3 ^ (a + r)) := hN
  have hexp : 4 ^ r * 2 ^ (a + 1) ≤ 3 ^ (a + r) :=
    (Nat.pow_le_pow_iff_right hn1).mp hchain
  simpa [isolatedOESurvives, four_pow_mul_two_pow] using hexp

/-- Compatibility name of `isolatedOddSurvival_bound`. -/
theorem isolated_oe_ge_implies_exponent {n a r : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix a r))
    (hge : n ≤ image n (isolatedPrefix a r)) :
    2 ^ (a + 2 * r + 1) ≤ 3 ^ (a + r) :=
  isolatedOddSurvival_bound hn hw hge

theorem aboveAnchor_isolatedOddSurvival {n a r : ℕ}
    (hn : 2 ≤ n) (h : AboveAnchor n (isolatedPrefix a r)) :
    isolatedOESurvives a r :=
  isolatedOddSurvival_bound hn h.1 (aboveAnchor_image_ge h)

/-- Contrapositive: a scale gap forces the isolated prefix below `n`. -/
theorem isolated_oe_lt_of_scale_gap {n a r : ℕ} (hn : 2 ≤ n)
    (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (hw : follows n (isolatedPrefix a r)) :
    image n (isolatedPrefix a r) < n := by
  refine lt_of_not_ge fun hge => ?_
  exact (not_lt_of_ge (isolatedOddSurvival_bound hn hw hge)) hgap

theorem forbidden_isolated_under_anchor {n a r : ℕ}
    (hn : 2 ≤ n) (hgap : ¬isolatedOESurvives a r)
    (h : AboveAnchor n (isolatedPrefix a r)) : False :=
  hgap (aboveAnchor_isolatedOddSurvival hn h)

/-- A scale-gap isolated prefix is a finite-progress certificate. -/
theorem finiteProgress_of_isolated_scale_gap {n a r : ℕ}
    (hn : 2 ≤ n) (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (hw : follows n (isolatedPrefix a r)) : FiniteProgress n :=
  finiteProgress_of_prefix_drop hw (isolated_oe_lt_of_scale_gap hn hgap hw)

theorem two_one_isolated_scale_gap :
    3 ^ (2 + 1) < 2 ^ (2 + 2 * 1 + 1) := by
  decide

theorem isolated_oe_exponent_two_zero :
    2 ^ (2 + 2 * 0 + 1) ≤ 3 ^ (2 + 0) := by
  decide

theorem not_isolated_oe_exponent_two_one :
    ¬2 ^ (2 + 2 * 1 + 1) ≤ 3 ^ (2 + 1) := by
  decide

/-- `R(2) = 0`: the comparison permits `r = 0` and forbids `r = 1`. -/
theorem isolated_oe_r_max_two :
    2 ^ (2 + 2 * 0 + 1) ≤ 3 ^ (2 + 0) ∧
      ¬2 ^ (2 + 2 * 1 + 1) ≤ 3 ^ (2 + 1) :=
  ⟨isolated_oe_exponent_two_zero, not_isolated_oe_exponent_two_one⟩

theorem three_pow_lt_two_pow_isolated_two :
    ∀ r : ℕ, 3 ^ (r + 3) < 2 ^ (2 * r + 5)
  | 0 => by decide
  | r + 1 => by
      have ih := three_pow_lt_two_pow_isolated_two r
      have hpos : 0 < 2 ^ (2 * r + 5) :=
        pow_pos (by decide : (0 : ℕ) < 2) _
      have h3 : r + 1 + 3 = (r + 3) + 1 := by omega
      have h2 : 2 * (r + 1) + 5 = (2 * r + 5) + 2 := by omega
      calc
        3 ^ (r + 1 + 3)
            = 3 ^ (r + 3) * 3 := by rw [h3, pow_succ]
        _ = 3 * 3 ^ (r + 3) := mul_comm _ _
        _ < 3 * 2 ^ (2 * r + 5) :=
            Nat.mul_lt_mul_of_pos_left ih (by decide)
        _ < 4 * 2 ^ (2 * r + 5) :=
            Nat.mul_lt_mul_of_pos_right (by decide : (3 : ℕ) < 4) hpos
        _ = 2 ^ 2 * 2 ^ (2 * r + 5) := by norm_num
        _ = 2 ^ (2 * r + 5) * 2 ^ 2 := mul_comm _ _
        _ = 2 ^ ((2 * r + 5) + 2) := (Nat.pow_add 2 (2 * r + 5) 2).symm
        _ = 2 ^ (2 * (r + 1) + 5) := by rw [h2]

theorem not_isolatedOESurvives_two_succ (r : ℕ) :
    ¬isolatedOESurvives 2 (r + 1) := by
  unfold isolatedOESurvives
  have hL : 2 + 2 * (r + 1) + 1 = 2 * r + 5 := by omega
  have hR : 2 + (r + 1) = r + 3 := by omega
  simpa [hL, hR] using
    (Nat.not_le.mpr (three_pow_lt_two_pow_isolated_two r))

/-- Corollary `a = 2 → r = 0` of the isolated survival bound. -/
theorem isolatedOESurvives_two {r : ℕ} (h : isolatedOESurvives 2 r) : r = 0 := by
  cases r with
  | zero => rfl
  | succ r => exact (not_isolatedOESurvives_two_succ r h).elim

theorem aboveAnchor_isolated_two {n r : ℕ} (hn : 2 ≤ n)
    (h : AboveAnchor n (isolatedPrefix 2 r)) : r = 0 :=
  isolatedOESurvives_two (aboveAnchor_isolatedOddSurvival hn h)

theorem image_ooe_oe_lt {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix 2 1)) :
    image n (isolatedPrefix 2 1) < n :=
  isolated_oe_lt_of_scale_gap hn two_one_isolated_scale_gap hw

/-- `OOE OE` is a finite-progress word: the isolated scale gap. -/
theorem finiteProgress_of_ooe_oe {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix 2 1)) : FiniteProgress n :=
  finiteProgress_of_isolated_scale_gap hn two_one_isolated_scale_gap hw

theorem firstInternalOO_decomp {w : List Branch} (h : FirstInternalOO w) :
    ∃ a r b v,
      2 ≤ a ∧ 2 ≤ b ∧
        w = firstInternalOOWord a r b v ∧
          v.head? ≠ some Branch.odd :=
  h

end Problems.Juggler
