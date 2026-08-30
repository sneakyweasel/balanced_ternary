import Problems.Juggler.CycleCore

namespace Problems.Juggler

/-!
# First internal `OO` after isolated `OE` transport

A CycleMin-shaped word that stays in the isolated-`OE` corridor after
the first even letter, then meets a later odd run of length at least
two, is

```
O^{a} E (OE)^{r} O^{b} v
```

with `a ≥ 2`, `b ≥ 2`, and `v` not beginning with `O`. The displayed
`O^{b}` is the first internal `OO`. This file packages that
decomposition and the isolated-`OE` exponent comparison

```
n ≤ T_{O^{a}E(OE)^{r}}(n)  →  2^{a+2r+1} ≤ 3^{a+r}.
```

In particular `R(2) = 0`: a CycleMin cannot complete one isolated
`OE` after `OOE` while staying at least `n`. The suffix after the
first `OO` is not classified. Not a halt theorem, not a four-even
assembler, and not a length-11 census.
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

/-- If the isolated prefix stays at least `n`, the two existing scale
envelopes force `2^{a+2r+1} ≤ 3^{a+r}`. -/
theorem isolated_oe_ge_implies_exponent {n a r : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix a r))
    (hge : n ≤ image n (isolatedPrefix a r)) :
    2 ^ (a + 2 * r + 1) ≤ 3 ^ (a + r) := by
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
  simpa [four_pow_mul_two_pow] using hexp

/-- Contrapositive: a scale gap forces the isolated prefix below `n`. -/
theorem isolated_oe_lt_of_scale_gap {n a r : ℕ} (hn : 2 ≤ n)
    (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (hw : follows n (isolatedPrefix a r)) :
    image n (isolatedPrefix a r) < n := by
  refine lt_of_not_ge fun hge => ?_
  exact (not_lt_of_ge (isolated_oe_ge_implies_exponent hn hw hge)) hgap

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

theorem image_ooe_oe_lt {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n (isolatedPrefix 2 1)) :
    image n (isolatedPrefix 2 1) < n :=
  isolated_oe_lt_of_scale_gap hn two_one_isolated_scale_gap hw

theorem no_cycleMin_isolated_prefix_of_gap {n a r : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (hgap : 3 ^ (a + r) < 2 ^ (a + 2 * r + 1))
    (h : CycleMin n (isolatedPrefix a r ++ v)) : False := by
  have hw : follows n (isolatedPrefix a r) := follows_of_append_left h.1.1
  have hlt := isolated_oe_lt_of_scale_gap hn hgap hw
  cases v with
  | nil =>
      have himg : image n (isolatedPrefix a r) = n := by
        simpa using h.1.2.1
      rw [himg] at hlt
      exact (lt_irrefl n) hlt
  | cons b t =>
      have hlen :
          (isolatedPrefix a r).length <
            (isolatedPrefix a r ++ b :: t).length := by
        simp [List.length_append]
      have hge : n ≤ image n (isolatedPrefix a r) := by
        have := cycleMin_ge (j := (isolatedPrefix a r).length) h hlen
        simpa [image_eq_iterate] using this
      exact (not_lt_of_ge hge) hlt

/-- An `a₀ = 2` CycleMin cannot complete one isolated `OE` after the
first even letter. The first internal `OO`, if it exists on this
corridor, is immediate (`r = 0`). -/
theorem no_cycleMin_prefix_ooe_oe {n : ℕ} {v : List Branch}
    (hn : 2 ≤ n) (h : CycleMin n (isolatedPrefix 2 1 ++ v)) : False :=
  no_cycleMin_isolated_prefix_of_gap hn two_one_isolated_scale_gap h

/-- The first-internal-`OO` predicate is exactly the isolated-prefix
writing `O^{a}E(OE)^{r}O^{b}v` with a maximal displayed odd run. -/
theorem firstInternalOO_decomp {w : List Branch} (h : FirstInternalOO w) :
    ∃ a r b v,
      2 ≤ a ∧ 2 ≤ b ∧
        w = firstInternalOOWord a r b v ∧
          v.head? ≠ some Branch.odd :=
  h

end Problems.Juggler
