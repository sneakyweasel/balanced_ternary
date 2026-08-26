import Mathlib.Algebra.Group.Nat.Even
import Mathlib.Data.Nat.Sqrt
import Mathlib.Tactic

namespace Problems.Engine

/-!
# Finite-word floor-power envelope

The Juggler map on `ℕ` is

```
T(n) = Nat.sqrt n          if n is even
T(n) = Nat.sqrt (n ^ 3)    if n is odd
```

This file packages the local exact theory of realized finite parity words.
It is not a halt theorem on all positive integers.

Headline theorems:

* `power_bound_follows` — every realized word obeys
  `T_w(n) ^ (2 ^ |w|) ≤ n ^ (3 ^ #O(w))`.
* `power_bound_eq_iff_extremal` — envelope equality is exactly the two
  monochrome towers `a^(2^k)`.
* `power_deficit_eq_local_even_iff` / `power_deficit_eq_local_odd_iff` —
  first-defect sharpness: `Δ = δ` iff the suffix is an exact even tower.
* `floorPower_odd_eq_iff_cube_interval` — inverse-floor form of an odd step.
* `power_bound_compensated_contracts` — a certified deficit larger than
  the formal exponent gap implies block contraction.
* `floorPower_eoo_contracts_iff` — the shortest mixed positive-drift
  word `EOO` contracts if and only if `n ∈ {2, 12, 14}`.
* `eoo_contracts_on_cell` — that classification is the square-root
  cell threshold `n > eooCellOutput ⌊√n⌋`.
* `first_even_freeze` — every first-even word satisfies
  `T_{Ev}(n) = T_v(⌊√n⌋)` on the square-root cell.
* `odd_cell_unique` — every odd floor cell contains at most one `n`.
* `oo_suffix_threshold` / `ooo_suffix_threshold` — the positive-drift
  suffixes `OO` and `OOO` eventually sit at or above `(q+1)^2`.
* `eventually_no_first_even_contraction` — every fixed suffix with
  `3^#O(v) > 2^(|v|+1)` has only finitely many first-even contraction
  cells.
-/

/-!
## One-step map
-/

/-- Even `n` maps to `Nat.sqrt n`; odd `n` maps to `Nat.sqrt (n^3)`. -/
def floorPower (n : ℕ) : ℕ :=
  if n % 2 = 0 then n.sqrt else (n ^ 3).sqrt

theorem floorPower_even_eq {n : ℕ} (heven : n % 2 = 0) :
    floorPower n = n.sqrt :=
  if_pos heven

theorem floorPower_odd_eq {n : ℕ} (hodd : n % 2 = 1) :
    floorPower n = (n ^ 3).sqrt := by
  have hodd0 : n % 2 ≠ 0 := by omega
  simp [floorPower, hodd0]

/-- Integer obstruction: `k^4 ≤ n^3` and `n ≥ 2` forbid `k ≥ n`.
This is iterated `Nat.sqrt` of `n^3`, not `T^2` on the odd-to-odd branch. -/
theorem sqrt_sqrt_n_cubed_lt {n : ℕ} (hn : 2 ≤ n) :
    ((n ^ 3).sqrt).sqrt < n := by
  set m := (n ^ 3).sqrt
  set k := m.sqrt
  have hk : k * k ≤ m := Nat.sqrt_le m
  have hm : m * m ≤ n ^ 3 := Nat.sqrt_le (n ^ 3)
  have hk4 : k * k * (k * k) ≤ m * m := Nat.mul_le_mul hk hk
  have hk4n : k ^ 4 ≤ n ^ 3 := by
    have : k * k * k * k ≤ n ^ 3 := by
      simpa [mul_assoc] using (le_trans hk4 hm)
    simpa [pow_succ, pow_zero, mul_assoc] using this
  refine Nat.lt_of_not_ge fun hkn => ?_
  have hn4 : n ^ 4 ≤ k ^ 4 := by
    have h2 := Nat.mul_le_mul hkn hkn
    have h4 := Nat.mul_le_mul h2 h2
    simpa [pow_succ, pow_zero, mul_assoc] using h4
  have hle : n ^ 4 ≤ n ^ 3 := le_trans hn4 hk4n
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : 0 < 2) hn
  have hn3 : 0 < n ^ 3 := pow_pos hn0 3
  have hmul : n * n ^ 3 ≤ 1 * n ^ 3 := by
    simpa [pow_succ, pow_zero, mul_assoc] using hle
  have : n ≤ 1 := Nat.le_of_mul_le_mul_right hmul hn3
  omega

/-- On the odd-to-even branch, `T^2(n) < n`. Not a halt theorem for the full map. -/
theorem floorPower_odd_even_two_step_lt
    {n : ℕ} (hn : 2 ≤ n) (hodd : n % 2 = 1)
    (heven : (n ^ 3).sqrt % 2 = 0) :
    floorPower (floorPower n) < n := by
  have step1 : floorPower n = (n ^ 3).sqrt := floorPower_odd_eq hodd
  have step2 : floorPower (floorPower n) = ((n ^ 3).sqrt).sqrt := by
    rw [step1]
    exact floorPower_even_eq heven
  rw [step2]
  exact sqrt_sqrt_n_cubed_lt hn

/-- Integer comparison: `(n+1)^2 ≤ n^3` for `n ≥ 3`. Threshold for odd-branch growth. -/
theorem succ_sq_le_cube {n : ℕ} (hn : 3 ≤ n) : (n + 1) ^ 2 ≤ n ^ 3 := by
  zify
  nlinarith

/-- On the odd branch, `n ≥ 3` implies `T(n) > n`. Independent of the parity of `T(n)`. -/
theorem floorPower_odd_gt {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1) :
    n < floorPower n := by
  rw [floorPower_odd_eq hodd]
  have hsq : (n + 1) ^ 2 ≤ n ^ 3 := succ_sq_le_cube hn
  have : n + 1 ≤ (n ^ 3).sqrt := Nat.le_sqrt.mpr (by simpa [pow_two] using hsq)
  omega

/-- The odd branch is nondecreasing: `k ≤ T(k)` when `k` is odd and positive. -/
theorem floorPower_odd_nondecreasing {k : ℕ} (hk : 1 ≤ k) (hodd : k % 2 = 1) :
    k ≤ floorPower k := by
  rw [floorPower_odd_eq hodd]
  have h1 : k ^ 2 ≤ k ^ 3 := by
    have : 1 ≤ k := hk
    simpa [pow_succ, pow_two, pow_zero, mul_assoc] using
      Nat.mul_le_mul_left (k * k) this
  exact Nat.le_sqrt.mpr (by simpa [pow_two] using h1)

/-- On the odd-to-odd branch with `n ≥ 3`, `T^2(n) > n`. Dual of
`floorPower_odd_even_two_step_lt`. Not a divergence theorem. -/
theorem floorPower_odd_odd_two_step_gt
    {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1)
    (hodd1 : (n ^ 3).sqrt % 2 = 1) :
    n < floorPower (floorPower n) := by
  have step1 : floorPower n = (n ^ 3).sqrt := floorPower_odd_eq hodd
  have hkpos : 1 ≤ floorPower n := by
    have : n < floorPower n := floorPower_odd_gt hn hodd
    omega
  have hoddT : floorPower n % 2 = 1 := by
    simpa [step1] using hodd1
  have hmono : floorPower n ≤ floorPower (floorPower n) :=
    floorPower_odd_nondecreasing hkpos hoddT
  have hgt : n < floorPower n := floorPower_odd_gt hn hodd
  omega

/-- Combined odd-state two-step direction for `n ≥ 3`. This is the
conjunction of `floorPower_odd_even_two_step_lt` and
`floorPower_odd_odd_two_step_gt` on a common domain. It is not a
macro-transition law, not a halt theorem, and not a divergence theorem.
The case `n = 1` is excluded: `floorPower 1 = 1`. -/
theorem floorPower_odd_macro_direction
    {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1) :
    ((n ^ 3).sqrt % 2 = 0 → floorPower (floorPower n) < n) ∧
    ((n ^ 3).sqrt % 2 = 1 → n < floorPower (floorPower n)) := by
  refine ⟨?he, ?ho⟩
  · intro heven
    have hn2 : 2 ≤ n := le_trans (by decide : 2 ≤ 3) hn
    exact floorPower_odd_even_two_step_lt hn2 hodd heven
  · intro hodd1
    exact floorPower_odd_odd_two_step_gt hn hodd hodd1

/-- Named expansion of the OOOEE envelope `n5 ^ 32 ≤ n ^ 27`. -/
theorem floorPower_oooee_pow_chain
    {n n1 n2 n3 n4 n5 : ℕ}
    (h1 : n1 ^ 2 ≤ n ^ 3)
    (h2 : n2 ^ 2 ≤ n1 ^ 3)
    (h3 : n3 ^ 2 ≤ n2 ^ 3)
    (h4 : n4 ^ 2 ≤ n3)
    (h5 : n5 ^ 2 ≤ n4) :
    n5 ^ 32 ≤ n ^ 27 := by
  have h32 : n5 ^ 32 = (n5 ^ 2) ^ 16 := by
    calc
      n5 ^ 32 = n5 ^ (2 * 16) := by norm_num
      _ = (n5 ^ 2) ^ 16 := Nat.pow_mul n5 2 16
  have h16 : n4 ^ 16 = (n4 ^ 2) ^ 8 := by
    calc
      n4 ^ 16 = n4 ^ (2 * 8) := by norm_num
      _ = (n4 ^ 2) ^ 8 := Nat.pow_mul n4 2 8
  have h8 : n3 ^ 8 = (n3 ^ 2) ^ 4 := by
    calc
      n3 ^ 8 = n3 ^ (2 * 4) := by norm_num
      _ = (n3 ^ 2) ^ 4 := Nat.pow_mul n3 2 4
  have h12 : (n2 ^ 3) ^ 4 = n2 ^ 12 := by
    calc
      (n2 ^ 3) ^ 4 = n2 ^ (3 * 4) := (Nat.pow_mul n2 3 4).symm
      _ = n2 ^ 12 := by norm_num
  have h12' : n2 ^ 12 = (n2 ^ 2) ^ 6 := by
    calc
      n2 ^ 12 = n2 ^ (2 * 6) := by norm_num
      _ = (n2 ^ 2) ^ 6 := Nat.pow_mul n2 2 6
  have h18 : (n1 ^ 3) ^ 6 = n1 ^ 18 := by
    calc
      (n1 ^ 3) ^ 6 = n1 ^ (3 * 6) := (Nat.pow_mul n1 3 6).symm
      _ = n1 ^ 18 := by norm_num
  have h18' : n1 ^ 18 = (n1 ^ 2) ^ 9 := by
    calc
      n1 ^ 18 = n1 ^ (2 * 9) := by norm_num
      _ = (n1 ^ 2) ^ 9 := Nat.pow_mul n1 2 9
  have h27 : (n ^ 3) ^ 9 = n ^ 27 := by
    calc
      (n ^ 3) ^ 9 = n ^ (3 * 9) := (Nat.pow_mul n 3 9).symm
      _ = n ^ 27 := by norm_num
  calc
    n5 ^ 32 = (n5 ^ 2) ^ 16 := h32
    _ ≤ n4 ^ 16 := Nat.pow_le_pow_left h5 16
    _ = (n4 ^ 2) ^ 8 := h16
    _ ≤ n3 ^ 8 := Nat.pow_le_pow_left h4 8
    _ = (n3 ^ 2) ^ 4 := h8
    _ ≤ (n2 ^ 3) ^ 4 := Nat.pow_le_pow_left h3 4
    _ = n2 ^ 12 := h12
    _ = (n2 ^ 2) ^ 6 := h12'
    _ ≤ (n1 ^ 3) ^ 6 := Nat.pow_le_pow_left h2 6
    _ = n1 ^ 18 := h18
    _ = (n1 ^ 2) ^ 9 := h18'
    _ ≤ (n ^ 3) ^ 9 := Nat.pow_le_pow_left h1 9
    _ = n ^ 27 := h27

/-- Even branch: `T(n)^2 ≤ n`. Exact floor bound, not a real square root. -/
theorem floorPower_even_sq_le {n : ℕ} (heven : n % 2 = 0) :
    floorPower n ^ 2 ≤ n := by
  rw [floorPower_even_eq heven]
  simpa [pow_two] using Nat.sqrt_le n

/-- Odd branch: `T(n)^2 ≤ n^3`. Exact floor bound, not a real 3/2-power. -/
theorem floorPower_odd_sq_le_cube {n : ℕ} (hodd : n % 2 = 1) :
    floorPower n ^ 2 ≤ n ^ 3 := by
  rw [floorPower_odd_eq hodd]
  have hle : (n ^ 3).sqrt * (n ^ 3).sqrt ≤ n ^ 3 := Nat.sqrt_le (n ^ 3)
  simpa [pow_two] using hle

/-- Odd squares attain the one-step envelope: odd `m` implies `T(m^2)^2 = (m^2)^3`.
So `n^{3/2}` can be an integer for odd `n≥3`. Mixed-word equality is possible.
This kills any universal lemma `T(n)^2 < n^3` for all odd `n≥3`. -/
theorem floorPower_odd_sq_eq_cube_of_sq {m : ℕ} (hodd : m % 2 = 1) :
    floorPower (m ^ 2) ^ 2 = (m ^ 2) ^ 3 := by
  have nne : (m ^ 2) % 2 = 1 := by
    rw [Nat.pow_two, Nat.mul_mod, hodd]
  rw [floorPower_odd_eq nne]
  have hcube : (m ^ 2) ^ 3 = (m ^ 3) ^ 2 := by ring
  rw [hcube, Nat.sqrt_eq']

/-- Smallest mixed-equality witness: word `O` at `n=9`. -/
theorem floorPower_nine_odd_eq : floorPower 9 ^ 2 = 9 ^ 3 := by
  have h : floorPower ((3 : ℕ) ^ 2) ^ 2 = ((3 : ℕ) ^ 2) ^ 3 :=
    floorPower_odd_sq_eq_cube_of_sq (by decide)
  simpa using h

/-- Even-step composition of a square upper bound. -/
theorem pow_sq_le {a b e : ℕ} (h : a ^ 2 ≤ b) :
    a ^ (2 * e) ≤ b ^ e := by
  calc
    a ^ (2 * e) = (a ^ 2) ^ e := Nat.pow_mul a 2 e
    _ ≤ b ^ e := Nat.pow_le_pow_left h e

/-- Odd-step composition of a square-vs-cube upper bound. -/
theorem pow_sq_le_cube {a b e : ℕ} (h : a ^ 2 ≤ b ^ 3) :
    a ^ (2 * e) ≤ b ^ (3 * e) := by
  calc
    a ^ (2 * e) = (a ^ 2) ^ e := Nat.pow_mul a 2 e
    _ ≤ (b ^ 3) ^ e := Nat.pow_le_pow_left h e
    _ = b ^ (3 * e) := (Nat.pow_mul b 3 e).symm

/-- For `n ≥ 2`, a strictly larger exponent yields a strictly larger power. -/
theorem pow_lt_of_two_le {n a b : ℕ} (hn : 2 ≤ n) (hba : b < a) :
    n ^ b < n ^ a :=
  Nat.pow_lt_pow_right (lt_of_lt_of_le (by decide : 1 < 2) hn) hba

theorem two_pow_succ (k : ℕ) : 2 ^ (k + 1) = 2 * 2 ^ k := by
  rw [pow_succ, mul_comm]

theorem three_pow_succ (o : ℕ) : 3 ^ (o + 1) = 3 * 3 ^ o := by
  rw [pow_succ, mul_comm]

theorem pow_three_succ_right (n o : ℕ) :
    (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ (o + 1)) := by
  calc
    (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
    _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
    _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']

/-!
## Finite words and the weak envelope

One-sided floor-power composition on realized finite words.
Not a tactic, not a termination theorem, and not a parity-frequency theorem.
The invariant is `PowerBound m n k o`, i.e. `m^{2^k} ≤ n^{3^o}`.
-/

inductive Branch where
  | even
  | odd
  deriving DecidableEq, Repr

def oddCount : List Branch → ℕ
  | [] => 0
  | .odd :: w => oddCount w + 1
  | .even :: w => oddCount w

/-- The orbit of `n` realizes the finite parity word `w`. -/
def follows : ℕ → List Branch → Prop
  | _, [] => True
  | n, .even :: w => n % 2 = 0 ∧ follows (floorPower n) w
  | n, .odd :: w => n % 2 = 1 ∧ follows (floorPower n) w

/-- Weak one-sided bound `m^{2^k} ≤ n^{3^o}`. Equality is allowed. -/
def PowerBound (m n k o : ℕ) : Prop := m ^ (2 ^ k) ≤ n ^ (3 ^ o)

@[simp] theorem oddCount_nil : oddCount [] = 0 := rfl

@[simp] theorem oddCount_even_cons (w : List Branch) :
    oddCount (.even :: w) = oddCount w := rfl

@[simp] theorem oddCount_odd_cons (w : List Branch) :
    oddCount (.odd :: w) = oddCount w + 1 := rfl

theorem power_bound_empty (n : ℕ) : PowerBound n n 0 0 := by
  simp [PowerBound]

theorem power_bound_append_even {m n k o : ℕ}
    (h : PowerBound m n k o) (heven : m % 2 = 0) :
    PowerBound (floorPower m) n (k + 1) o := by
  have hsq : floorPower m ^ 2 ≤ m := floorPower_even_sq_le heven
  unfold PowerBound at *
  rw [two_pow_succ]
  exact le_trans (pow_sq_le hsq) h

theorem power_bound_append_odd {m n k o : ℕ}
    (h : PowerBound m n k o) (hodd : m % 2 = 1) :
    PowerBound (floorPower m) n (k + 1) (o + 1) := by
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  unfold PowerBound at *
  rw [two_pow_succ, three_pow_succ]
  calc
    floorPower m ^ (2 * 2 ^ k) ≤ m ^ (3 * 2 ^ k) := pow_sq_le_cube hsq
    _ = (m ^ (2 ^ k)) ^ 3 := by rw [mul_comm, Nat.pow_mul]
    _ ≤ (n ^ (3 ^ o)) ^ 3 := Nat.pow_le_pow_left h 3
    _ = n ^ ((3 ^ o) * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
    _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]

/-- Image of `n` after the realized word `w`. Definitional on `cons`. -/
def image : ℕ → List Branch → ℕ
  | n, [] => n
  | n, _ :: w => image (floorPower n) w

@[simp] theorem image_nil (n : ℕ) : image n [] = n := rfl

@[simp] theorem image_cons (n : ℕ) (b : Branch) (w : List Branch) :
    image n (b :: w) = image (floorPower n) w := rfl

theorem iterate_cons (n : ℕ) (k : ℕ) :
    floorPower^[k + 1] n = floorPower^[k] (floorPower n) := by
  induction k generalizing n with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply, ih, ← Function.iterate_succ_apply]

theorem image_eq_iterate (n : ℕ) : ∀ w, image n w = floorPower^[w.length] n := by
  intro w
  induction w generalizing n with
  | nil => simp
  | cons _b w ih =>
      simp [List.length_cons, ih, iterate_cons]

theorem power_bound_from {start current k o : ℕ}
    (hbound : PowerBound current start k o) :
    ∀ w, follows current w →
      PowerBound (image current w) start (k + w.length)
        (o + oddCount w) := by
  intro w
  induction w generalizing current k o with
  | nil =>
      intro _
      simpa using hbound
  | cons b rest ih =>
      intro hw
      cases b with
      | even =>
          have heven : current % 2 = 0 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o)
              (power_bound_append_even hbound heven) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          simp [List.length_cons]
          rw [hk]
          exact hih
      | odd =>
          have hodd : current % 2 = 1 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o + 1)
              (power_bound_append_odd hbound hodd) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have ho : o + (oddCount rest + 1) = o + 1 + oddCount rest := by omega
          simp [List.length_cons]
          rw [hk, ho]
          exact hih

/-- Weak composition: every realized finite word obeys the one-sided bound. -/
theorem power_bound_follows {n : ℕ} {w : List Branch} (hw : follows n w) :
    PowerBound (floorPower^[w.length] n) n w.length (oddCount w) := by
  have h := power_bound_from (power_bound_empty n) w hw
  simpa [image_eq_iterate] using h

/-- Unfolded form of `power_bound_follows`. Naming alias only. -/
theorem power_bound_word {n : ℕ} {w : List Branch} (hw : follows n w) :
    (floorPower^[w.length] n) ^ (2 ^ w.length) ≤ n ^ (3 ^ oddCount w) :=
  power_bound_follows hw

/-- Strict block contraction from the exponent gap. Domain `n ≥ 2`.
Not a claim that every trajectory meets a negative-drift word. -/
theorem power_bound_contracts {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w)
    (hgap : 3 ^ oddCount w < 2 ^ w.length) :
    floorPower^[w.length] n < n := by
  have hpow := power_bound_follows hw
  unfold PowerBound at hpow
  refine Nat.lt_of_not_ge fun hge => ?_
  have hleft : n ^ (2 ^ w.length) ≤ (floorPower^[w.length] n) ^ (2 ^ w.length) :=
    Nat.pow_le_pow_left hge _
  have hle : n ^ (2 ^ w.length) ≤ n ^ (3 ^ oddCount w) := le_trans hleft hpow
  have hlt : n ^ (3 ^ oddCount w) < n ^ (2 ^ w.length) := pow_lt_of_two_le hn hgap
  exact (not_le_of_gt hlt) hle

def wordOOOEE : List Branch := [.odd, .odd, .odd, .even, .even]

def wordOOOEEEOO : List Branch :=
  [.odd, .odd, .odd, .even, .even, .even, .odd, .odd]

theorem follows_wordOOOEE_iff {n : ℕ} :
    follows n wordOOOEE ↔
      n % 2 = 1 ∧
      floorPower n % 2 = 1 ∧
      floorPower (floorPower n) % 2 = 1 ∧
      floorPower (floorPower (floorPower n)) % 2 = 0 ∧
      floorPower (floorPower (floorPower (floorPower n))) % 2 = 0 := by
  simp [follows, wordOOOEE]

theorem follows_wordOOOEEEOO_iff {n : ℕ} :
    follows n wordOOOEEEOO ↔
      n % 2 = 1 ∧
      floorPower n % 2 = 1 ∧
      floorPower (floorPower n) % 2 = 1 ∧
      floorPower (floorPower (floorPower n)) % 2 = 0 ∧
      floorPower (floorPower (floorPower (floorPower n))) % 2 = 0 ∧
      floorPower (floorPower (floorPower (floorPower (floorPower n)))) % 2 = 0 ∧
      floorPower (floorPower (floorPower (floorPower (floorPower
          (floorPower n))))) % 2 = 1 ∧
      floorPower (floorPower (floorPower (floorPower (floorPower
          (floorPower (floorPower n)))))) % 2 = 1 := by
  simp [follows, wordOOOEEEOO]

theorem floorPower_oooee_of_follows {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOOEE) :
    floorPower^[5] n < n := by
  have h := power_bound_contracts (w := wordOOOEE) hn hw
  have hgap : 3 ^ oddCount wordOOOEE < 2 ^ wordOOOEE.length := by
    simp [wordOOOEE]
  simpa [wordOOOEE] using h hgap

theorem floorPower_oooeeeoo_of_follows {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOOEEEOO) :
    floorPower^[8] n < n := by
  have h := power_bound_contracts (w := wordOOOEEEOO) hn hw
  have hgap : 3 ^ oddCount wordOOOEEEOO < 2 ^ wordOOOEEEOO.length := by
    simp [wordOOOEEEOO]
  simpa [wordOOOEEEOO] using h hgap

/-- On the OOOEE branch word, `T^5(n) < n` for `n ≥ 2`. Wrapper of
`floorPower_oooee_of_follows`. Not a halt theorem. -/
theorem floorPower_oooee_five_step_lt
    {n : ℕ} (hn : 2 ≤ n) (h0 : n % 2 = 1)
    (h1 : floorPower n % 2 = 1)
    (h2 : floorPower (floorPower n) % 2 = 1)
    (h3 : floorPower (floorPower (floorPower n)) % 2 = 0)
    (h4 : floorPower (floorPower (floorPower (floorPower n))) % 2 = 0) :
    floorPower (floorPower (floorPower (floorPower (floorPower n)))) < n := by
  have hw : follows n wordOOOEE :=
    (follows_wordOOOEE_iff (n := n)).mpr ⟨h0, h1, h2, h3, h4⟩
  simpa [wordOOOEE] using floorPower_oooee_of_follows hn hw

/-- Power comparison for the OOOEEEOO floor-power block: five odd steps
and three even steps give `n8 ^ 256 ≤ n ^ 243`. Canonical exponents of
the word exponent `243/256`. -/
theorem floorPower_oooeeeoo_pow_chain
    {n n1 n2 n3 n4 n5 n6 n7 n8 : ℕ}
    (h1 : n1 ^ 2 ≤ n ^ 3)
    (h2 : n2 ^ 2 ≤ n1 ^ 3)
    (h3 : n3 ^ 2 ≤ n2 ^ 3)
    (h4 : n4 ^ 2 ≤ n3)
    (h5 : n5 ^ 2 ≤ n4)
    (h6 : n6 ^ 2 ≤ n5)
    (h7 : n7 ^ 2 ≤ n6 ^ 3)
    (h8 : n8 ^ 2 ≤ n7 ^ 3) :
    n8 ^ 256 ≤ n ^ 243 := by
  calc
    n8 ^ 256 = n8 ^ (2 * 128) := by norm_num
    _ ≤ n7 ^ (3 * 128) := pow_sq_le_cube h8
    _ = n7 ^ 384 := by norm_num
    _ = n7 ^ (2 * 192) := by norm_num
    _ ≤ n6 ^ (3 * 192) := pow_sq_le_cube h7
    _ = n6 ^ 576 := by norm_num
    _ = n6 ^ (2 * 288) := by norm_num
    _ ≤ n5 ^ 288 := pow_sq_le h6
    _ = n5 ^ (2 * 144) := by norm_num
    _ ≤ n4 ^ 144 := pow_sq_le h5
    _ = n4 ^ (2 * 72) := by norm_num
    _ ≤ n3 ^ 72 := pow_sq_le h4
    _ = n3 ^ (2 * 36) := by norm_num
    _ ≤ n2 ^ (3 * 36) := pow_sq_le_cube h3
    _ = n2 ^ 108 := by norm_num
    _ = n2 ^ (2 * 54) := by norm_num
    _ ≤ n1 ^ (3 * 54) := pow_sq_le_cube h2
    _ = n1 ^ 162 := by norm_num
    _ = n1 ^ (2 * 81) := by norm_num
    _ ≤ n ^ (3 * 81) := pow_sq_le_cube h1
    _ = n ^ 243 := by norm_num

/-- On the OOOEEEOO branch word, `T^8(n) < n` for `n ≥ 2`. Wrapper of
`floorPower_oooeeeoo_of_follows`. Not a halt theorem. -/
theorem floorPower_oooeeeoo_eight_step_lt
    {n : ℕ} (hn : 2 ≤ n) (h0 : n % 2 = 1)
    (h1 : floorPower n % 2 = 1)
    (h2 : floorPower (floorPower n) % 2 = 1)
    (h3 : floorPower (floorPower (floorPower n)) % 2 = 0)
    (h4 : floorPower (floorPower (floorPower (floorPower n))) % 2 = 0)
    (h5 : floorPower (floorPower (floorPower (floorPower (floorPower n)))) % 2 = 0)
    (h6 : floorPower (floorPower (floorPower (floorPower (floorPower
        (floorPower n))))) % 2 = 1)
    (h7 : floorPower (floorPower (floorPower (floorPower (floorPower
        (floorPower (floorPower n)))))) % 2 = 1) :
    floorPower (floorPower (floorPower (floorPower (floorPower (floorPower
        (floorPower (floorPower n))))))) < n := by
  have hw : follows n wordOOOEEEOO :=
    (follows_wordOOOEEEOO_iff (n := n)).mpr ⟨h0, h1, h2, h3, h4, h5, h6, h7⟩
  simpa [wordOOOEEEOO] using floorPower_oooeeeoo_of_follows hn hw

/-!
## Seed identities
-/

theorem floorPower_one : floorPower 1 = 1 := by
  native_decide

theorem floorPower_thirteen_step : floorPower 13 = 46 := by
  native_decide

/-- Packet seed `13` reaches `1` in four steps. Not a map theorem. -/
theorem floorPower_thirteen_reaches_one :
    (floorPower^[4] 13) = 1 := by
  native_decide

/-!
## Equality rigidity and saturation

Local branch equality, composite equality, and square rigidity.
Not a termination theorem, not an equality-word classifier, and not a
`PowerBound` certificate datatype. `PowerBound` remains the weak bound.
-/

/-- Even branch: `T(n)^2 = n` iff `n` is a perfect square. -/
theorem floorPower_even_sq_eq_iff_square {n : ℕ} (heven : n % 2 = 0) :
    floorPower n ^ 2 = n ↔ n.sqrt ^ 2 = n := by
  rw [floorPower_even_eq heven]

lemma sqrt_sq_iff_isSquare (n : ℕ) : n.sqrt ^ 2 = n ↔ IsSquare n := by
  rw [isSquare_iff_exists_sq]
  constructor
  · intro h
    exact ⟨n.sqrt, h.symm⟩
  · rintro ⟨r, hr⟩
    simp [hr, Nat.sqrt_eq']

lemma isSquare_pow_three_iff {n : ℕ} : IsSquare (n ^ 3) ↔ IsSquare n := by
  simp_rw [isSquare_iff_exists_sq]
  constructor
  · rintro ⟨k, hk⟩
    rcases eq_or_ne n 0 with rfl | hn
    · exact ⟨0, by simp⟩
    have hk0 : k ≠ 0 := by
      rintro rfl
      have : n ^ 3 = 0 := by simpa using hk
      exact hn ((Nat.pow_eq_zero.mp this).1)
    set d := Nat.gcd k n
    have hd_dvd_k : d ∣ k := Nat.gcd_dvd_left k n
    have hd_dvd_n : d ∣ n := Nat.gcd_dvd_right k n
    obtain ⟨a, ha⟩ := hd_dvd_k
    obtain ⟨b, hb⟩ := hd_dvd_n
    have hdpos : 0 < d := Nat.gcd_pos_of_pos_right k (Nat.pos_of_ne_zero hn)
    have hab : Nat.Coprime a b := by
      have hmul : Nat.gcd (d * a) (d * b) = d * Nat.gcd a b := Nat.gcd_mul_left d a b
      have : d * Nat.gcd a b = d := by
        rw [← hmul, ← ha, ← hb]
      have h1 : d * Nat.gcd a b = d * 1 := by
        rw [this, mul_one]
      exact Nat.mul_left_cancel hdpos h1
    have hpow : (d * a) ^ 2 = (d * b) ^ 3 := by
      rw [← ha, ← hb, hk]
    have hexp : d ^ 2 * a ^ 2 = d ^ 3 * b ^ 3 := by
      simpa [mul_pow] using hpow
    have hcancel : a ^ 2 = d * b ^ 3 := by
      have : d ^ 2 * a ^ 2 = d ^ 2 * (d * b ^ 3) := by
        have hre : d ^ 3 * b ^ 3 = d ^ 2 * (d * b ^ 3) := by ring
        rw [hexp, hre]
      exact Nat.mul_left_cancel (pow_pos hdpos 2) this
    have hb3 : b ^ 3 ∣ a ^ 2 := ⟨d, by rw [hcancel, mul_comm]⟩
    have hcop : Nat.Coprime (b ^ 3) (a ^ 2) := hab.symm.pow 3 2
    have hb1 : b = 1 := by
      have : b ^ 3 = 1 := hcop.eq_one_of_dvd hb3
      exact (Nat.pow_eq_one.mp this).resolve_right (by decide)
    refine ⟨a, ?_⟩
    rw [hb, hb1, mul_one, hcancel, hb1]
    ring
  · rintro ⟨s, hs⟩
    exact ⟨s ^ 3, by rw [hs]; ring⟩

lemma cube_sqrt_sq_iff (n : ℕ) :
    (n ^ 3).sqrt ^ 2 = n ^ 3 ↔ n.sqrt ^ 2 = n := by
  rw [sqrt_sq_iff_isSquare, sqrt_sq_iff_isSquare, isSquare_pow_three_iff]

/-- Odd branch: `T(n)^2 = n^3` iff `n` is a perfect square. -/
theorem floorPower_odd_sq_eq_cube_iff_square {n : ℕ} (hodd : n % 2 = 1) :
    floorPower n ^ 2 = n ^ 3 ↔ n.sqrt ^ 2 = n := by
  rw [floorPower_odd_eq hodd]
  exact cube_sqrt_sq_iff n

/-- Equality form of the one-sided envelope. Independent of `PowerBound`. -/
def PowerBoundEq (m n k o : ℕ) : Prop := m ^ (2 ^ k) = n ^ (3 ^ o)

theorem pow_eq_of_pow_sq_eq {a b e : ℕ} (he : e ≠ 0)
    (h : (a ^ 2) ^ e = b ^ e) : a ^ 2 = b :=
  Nat.pow_left_injective he h

theorem pow_ne_zero_two_pow (k : ℕ) : 2 ^ k ≠ 0 :=
  (Nat.pow_pos (by decide : (0 : ℕ) < 2)).ne'

/-- Even append: composite equality forces the previous equality and local tightness. -/
theorem power_bound_eq_of_append_even {m n k o : ℕ}
    (heven : m % 2 = 0) (hprev : PowerBound m n k o)
    (heq : PowerBoundEq (floorPower m) n (k + 1) o) :
    PowerBoundEq m n k o ∧ floorPower m ^ 2 = m := by
  have hlocal : floorPower m ^ 2 ≤ m := floorPower_even_sq_le heven
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hA : (floorPower m ^ 2) ^ (2 ^ k) ≤ m ^ (2 ^ k) :=
    Nat.pow_le_pow_left hlocal _
  have hA' : floorPower m ^ (2 ^ (k + 1)) ≤ m ^ (2 ^ k) := by
    rw [h2, Nat.pow_mul]
    exact hA
  have hB : m ^ (2 ^ k) ≤ n ^ (3 ^ o) := hprev
  have hends : floorPower m ^ (2 ^ (k + 1)) = n ^ (3 ^ o) := heq
  have hmid : floorPower m ^ (2 ^ (k + 1)) = m ^ (2 ^ k) :=
    le_antisymm hA' (hB.trans_eq hends.symm)
  have hprevEq : PowerBoundEq m n k o := le_antisymm hB (hends.symm.trans_le hA')
  refine ⟨hprevEq, ?_⟩
  have hpow : (floorPower m ^ 2) ^ (2 ^ k) = m ^ (2 ^ k) := by
    rw [← Nat.pow_mul, ← h2, hmid]
  have hk : 2 ^ k ≠ 0 := pow_ne_zero_two_pow k
  exact pow_eq_of_pow_sq_eq hk hpow

/-- Odd append: composite equality forces the previous equality and local tightness. -/
theorem power_bound_eq_of_append_odd {m n k o : ℕ}
    (hodd : m % 2 = 1) (hprev : PowerBound m n k o)
    (heq : PowerBoundEq (floorPower m) n (k + 1) (o + 1)) :
    PowerBoundEq m n k o ∧ floorPower m ^ 2 = m ^ 3 := by
  have hlocal : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have h3 : 3 ^ (o + 1) = 3 * 3 ^ o := three_pow_succ o
  have hA : (floorPower m ^ 2) ^ (2 ^ k) ≤ (m ^ 3) ^ (2 ^ k) :=
    Nat.pow_le_pow_left hlocal _
  have hA' : floorPower m ^ (2 ^ (k + 1)) ≤ m ^ (3 * 2 ^ k) := by
    rw [h2, Nat.pow_mul]
    simpa [Nat.pow_mul] using hA
  have hmid : m ^ (3 * 2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
    rw [mul_comm, Nat.pow_mul]
  have hB : (m ^ (2 ^ k)) ^ 3 ≤ (n ^ (3 ^ o)) ^ 3 :=
    Nat.pow_le_pow_left hprev 3
  have hB' : m ^ (3 * 2 ^ k) ≤ n ^ (3 ^ (o + 1)) := by
    rw [hmid, h3, mul_comm, Nat.pow_mul]
    exact hB
  have hends : floorPower m ^ (2 ^ (k + 1)) = n ^ (3 ^ (o + 1)) := heq
  have hchain1 : floorPower m ^ (2 ^ (k + 1)) = m ^ (3 * 2 ^ k) :=
    le_antisymm hA' (hB'.trans_eq hends.symm)
  have hchain2 : m ^ (3 * 2 ^ k) = n ^ (3 ^ (o + 1)) :=
    le_antisymm hB' (hends.symm.trans_le hA')
  have hprevEq : PowerBoundEq m n k o := by
    have : (m ^ (2 ^ k)) ^ 3 = (n ^ (3 ^ o)) ^ 3 := by
      rw [← hmid, hchain2, h3, mul_comm, Nat.pow_mul]
    exact Nat.pow_left_injective (by decide : (3 : ℕ) ≠ 0) this
  refine ⟨hprevEq, ?_⟩
  have hpow : (floorPower m ^ 2) ^ (2 ^ k) = (m ^ 3) ^ (2 ^ k) := by
    have : floorPower m ^ (2 * 2 ^ k) = m ^ (3 * 2 ^ k) := by
      simpa [h2] using hchain1
    simpa [Nat.pow_mul] using this
  have hk : 2 ^ k ≠ 0 := pow_ne_zero_two_pow k
  exact pow_eq_of_pow_sq_eq hk hpow

/-- Local tightness of one realized letter. -/
def localTight : ℕ → Branch → Prop
  | x, .even => floorPower x ^ 2 = x
  | x, .odd => floorPower x ^ 2 = x ^ 3

/-- Every local branch inequality along a realized word is tight. -/
def localsTight (n : ℕ) : List Branch → Prop
  | [] => True
  | b :: w => localTight n b ∧ localsTight (floorPower n) w

theorem localTight_even_iff_square {n : ℕ} (heven : n % 2 = 0) :
    localTight n .even ↔ n.sqrt ^ 2 = n :=
  floorPower_even_sq_eq_iff_square heven

theorem localTight_odd_iff_square {n : ℕ} (hodd : n % 2 = 1) :
    localTight n .odd ↔ n.sqrt ^ 2 = n :=
  floorPower_odd_sq_eq_cube_iff_square hodd

theorem power_bound_eq_from {start current k o : ℕ} :
    ∀ w, PowerBound current start k o → follows current w →
      PowerBoundEq (image current w) start (k + w.length) (o + oddCount w) →
        PowerBoundEq current start k o ∧ localsTight current w := by
  intro w
  induction w generalizing current k o with
  | nil =>
      intro hbound _ heq
      exact ⟨heq, trivial⟩
  | cons b rest ih =>
      intro hbound hw heq
      cases b with
      | even =>
          have heven : current % 2 = 0 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hbound' : PowerBound (floorPower current) start (k + 1) o :=
            power_bound_append_even hbound heven
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have heq' :
              PowerBoundEq (image (floorPower current) rest) start
                (k + 1 + rest.length) (o + oddCount rest) := by
            simpa [List.length_cons, hk] using heq
          have hih := ih hbound' hrest heq'
          have hstep := power_bound_eq_of_append_even heven hbound hih.1
          exact ⟨hstep.1, ⟨hstep.2, hih.2⟩⟩
      | odd =>
          have hodd : current % 2 = 1 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hbound' : PowerBound (floorPower current) start (k + 1) (o + 1) :=
            power_bound_append_odd hbound hodd
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have ho : o + (oddCount rest + 1) = o + 1 + oddCount rest := by omega
          have heq' :
              PowerBoundEq (image (floorPower current) rest) start
                (k + 1 + rest.length) (o + 1 + oddCount rest) := by
            simpa [List.length_cons, hk, ho] using heq
          have hih := ih hbound' hrest heq'
          have hstep := power_bound_eq_of_append_odd hodd hbound hih.1
          exact ⟨hstep.1, ⟨hstep.2, hih.2⟩⟩

theorem localsTight_get {n : ℕ} :
    ∀ w, localsTight n w →
      ∀ i, (hi : i < w.length) →
        localTight (floorPower^[i] n) w[i] := by
  intro w
  induction w generalizing n with
  | nil =>
      intro _ i hi
      cases hi
  | cons b rest ih =>
      intro h i hi
      cases i with
      | zero =>
          simpa [localTight] using h.1
      | succ j =>
          have hj : j < rest.length := by
            simpa [List.length_cons] using Nat.succ_lt_succ_iff.mp hi
          have hget : (b :: rest)[j + 1] = rest[j] := rfl
          have hiter : floorPower^[j + 1] n = floorPower^[j] (floorPower n) :=
            iterate_cons n j
          simpa [hget, hiter] using ih h.2 j hj

/-- Global envelope equality forces every local branch inequality to be tight. -/
theorem power_bound_eq_implies_local_eq {n : ℕ} {w : List Branch}
    (hw : follows n w)
    (heq : PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) :
    ∀ i, (hi : i < w.length) → localTight (floorPower^[i] n) w[i] := by
  have h :=
    power_bound_eq_from (w := w) (power_bound_empty n) hw
      (by simpa [image_eq_iterate] using heq)
  exact localsTight_get w h.2

theorem follows_get_even {n : ℕ} :
    ∀ w, follows n w →
      ∀ i, (hi : i < w.length) → w[i] = .even → (floorPower^[i] n) % 2 = 0 := by
  intro w
  induction w generalizing n with
  | nil =>
      intro _ i hi
      cases hi
  | cons b rest ih =>
      intro hw i hi he
      cases b with
      | even =>
          cases i with
          | zero => exact hw.1
          | succ j =>
              have hj : j < rest.length := by
                simpa [List.length_cons] using Nat.succ_lt_succ_iff.mp hi
              have hget : (Branch.even :: rest)[j + 1] = rest[j] := rfl
              have hiter : floorPower^[j + 1] n = floorPower^[j] (floorPower n) :=
                iterate_cons n j
              have hrest : follows (floorPower n) rest := hw.2
              simpa [hget, hiter] using ih hrest j hj (hget ▸ he)
      | odd =>
          cases i with
          | zero => cases he
          | succ j =>
              have hj : j < rest.length := by
                simpa [List.length_cons] using Nat.succ_lt_succ_iff.mp hi
              have hget : (Branch.odd :: rest)[j + 1] = rest[j] := rfl
              have hiter : floorPower^[j + 1] n = floorPower^[j] (floorPower n) :=
                iterate_cons n j
              have hrest : follows (floorPower n) rest := hw.2
              simpa [hget, hiter] using ih hrest j hj (hget ▸ he)

theorem follows_get_odd {n : ℕ} :
    ∀ w, follows n w →
      ∀ i, (hi : i < w.length) → w[i] = .odd → (floorPower^[i] n) % 2 = 1 := by
  intro w
  induction w generalizing n with
  | nil =>
      intro _ i hi
      cases hi
  | cons b rest ih =>
      intro hw i hi ho
      cases b with
      | even =>
          cases i with
          | zero => cases ho
          | succ j =>
              have hj : j < rest.length := by
                simpa [List.length_cons] using Nat.succ_lt_succ_iff.mp hi
              have hget : (Branch.even :: rest)[j + 1] = rest[j] := rfl
              have hiter : floorPower^[j + 1] n = floorPower^[j] (floorPower n) :=
                iterate_cons n j
              have hrest : follows (floorPower n) rest := hw.2
              simpa [hget, hiter] using ih hrest j hj (hget ▸ ho)
      | odd =>
          cases i with
          | zero => exact hw.1
          | succ j =>
              have hj : j < rest.length := by
                simpa [List.length_cons] using Nat.succ_lt_succ_iff.mp hi
              have hget : (Branch.odd :: rest)[j + 1] = rest[j] := rfl
              have hiter : floorPower^[j + 1] n = floorPower^[j] (floorPower n) :=
                iterate_cons n j
              have hrest : follows (floorPower n) rest := hw.2
              simpa [hget, hiter] using ih hrest j hj (hget ▸ ho)

theorem follows_get {n : ℕ} {w : List Branch} (hw : follows n w)
    (i : ℕ) (hi : i < w.length) :
    (w[i] = .even → (floorPower^[i] n) % 2 = 0) ∧
    (w[i] = .odd → (floorPower^[i] n) % 2 = 1) :=
  ⟨follows_get_even w hw i hi, follows_get_odd w hw i hi⟩

/-- Global envelope equality forces every relevant itinerary state to be a square. -/
theorem power_bound_eq_implies_square {n : ℕ} {w : List Branch}
    (hw : follows n w)
    (heq : PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) :
    ∀ i, i < w.length → (floorPower^[i] n).sqrt ^ 2 = floorPower^[i] n := by
  intro i hi
  have hloc := power_bound_eq_implies_local_eq hw heq i hi
  rcases hbranch : w[i] with _ | _
  · have heven := follows_get_even w hw i hi hbranch
    have : floorPower (floorPower^[i] n) ^ 2 = floorPower^[i] n := by
      simpa [localTight, hbranch] using hloc
    exact (floorPower_even_sq_eq_iff_square heven).mp this
  · have hodd := follows_get_odd w hw i hi hbranch
    have : floorPower (floorPower^[i] n) ^ 2 = (floorPower^[i] n) ^ 3 := by
      simpa [localTight, hbranch] using hloc
    exact (floorPower_odd_sq_eq_cube_iff_square hodd).mp this

/-- Even square: the even branch is exact as an image, not only as a power. -/
theorem floorPower_of_even_sq {s : ℕ} (heven : (s ^ 2) % 2 = 0) :
    floorPower (s ^ 2) = s := by
  have step : floorPower (s ^ 2) = (s ^ 2).sqrt := by simp [floorPower, heven]
  rw [step, Nat.sqrt_eq']

/-- Odd square: the odd branch maps `s^2` to `s^3`. -/
theorem floorPower_of_odd_sq {s : ℕ} (hodd : s % 2 = 1) :
    floorPower (s ^ 2) = s ^ 3 := by
  have hpow := floorPower_odd_sq_eq_cube_of_sq hodd
  have : floorPower (s ^ 2) ^ 2 = (s ^ 3) ^ 2 := by
    have hcube : (s ^ 2) ^ 3 = (s ^ 3) ^ 2 := by ring
    exact hpow.trans hcube
  exact Nat.pow_left_injective (by decide : (2 : ℕ) ≠ 0) this

theorem floorPower_even_sq_image_even {s : ℕ} (heven : (s ^ 2) % 2 = 0) :
    floorPower (s ^ 2) % 2 = 0 := by
  rw [floorPower_of_even_sq heven]
  have : Even (s ^ 2) := Nat.even_iff.2 heven
  have hs : Even s := (Nat.even_pow' (by decide : (2 : ℕ) ≠ 0)).1 this
  exact Nat.even_iff.1 hs

theorem floorPower_odd_sq_image_odd {s : ℕ} (hodd : s % 2 = 1) :
    floorPower (s ^ 2) % 2 = 1 := by
  rw [floorPower_of_odd_sq hodd]
  have : (s ^ 3) % 2 = 1 := by
    have hodd0 : s % 2 ≠ 0 := by omega
    simp [Nat.pow_mod, hodd]
  exact this

/-!
2-adic perfect-power depth of equality-saturating states.
Not a reusable height abstraction and not a termination theorem.
`HasPowTwoDepth n r` means `n` is a `2^r`-th power.
-/

def HasPowTwoDepth (n r : ℕ) : Prop := ∃ a, n = a ^ (2 ^ r)

theorem hasPowTwoDepth_zero (n : ℕ) : HasPowTwoDepth n 0 :=
  ⟨n, by simp⟩

theorem two_pow_pred {r : ℕ} (hr : 1 ≤ r) : 2 ^ r = 2 * 2 ^ (r - 1) := by
  cases r with
  | zero => exact (Nat.not_succ_le_zero 0 hr).elim
  | succ r => rw [Nat.add_sub_cancel, Nat.pow_succ']

theorem pow_two_succ_sq (a r : ℕ) :
    a ^ (2 ^ (r + 1)) = (a ^ (2 ^ r)) ^ 2 := by
  rw [pow_succ (2 : ℕ), Nat.pow_mul]

theorem pow_two_pred_sq {a r : ℕ} (hr : 1 ≤ r) :
    a ^ (2 ^ r) = (a ^ (2 ^ (r - 1))) ^ 2 := by
  rw [two_pow_pred hr, mul_comm, Nat.pow_mul]

/-- Exact even branch on a `2^r`-th power, `r ≥ 1`. -/
theorem floorPower_of_pow_two_depth_even {a r : ℕ} (hr : 1 ≤ r)
    (heven : (a ^ (2 ^ r)) % 2 = 0) :
    floorPower (a ^ (2 ^ r)) = a ^ (2 ^ (r - 1)) := by
  have hrep := pow_two_pred_sq (a := a) hr
  rw [hrep] at heven ⊢
  exact floorPower_of_even_sq heven

theorem pow_mod_two_of_odd {a e : ℕ} (hodd : a % 2 = 1) :
    (a ^ e) % 2 = 1 := by
  simp [Nat.pow_mod, hodd]

theorem odd_of_pow_odd {a e : ℕ} (he : 1 ≤ e) (h : (a ^ e) % 2 = 1) :
    a % 2 = 1 := by
  by_contra hne
  have heven : a % 2 = 0 := by omega
  have : Even (a ^ e) := by
    rw [Nat.even_pow]
    exact ⟨Nat.even_iff.2 heven, Nat.pos_iff_ne_zero.mp he⟩
  have : (a ^ e) % 2 = 0 := Nat.even_iff.1 this
  omega

/-- Exact odd branch on a `2^r`-th power, `r ≥ 1`. -/
theorem floorPower_of_pow_two_depth_odd {a r : ℕ} (hr : 1 ≤ r)
    (hodd : a % 2 = 1) :
    floorPower (a ^ (2 ^ r)) = a ^ (3 * 2 ^ (r - 1)) := by
  have hs : (a ^ (2 ^ (r - 1))) % 2 = 1 := pow_mod_two_of_odd hodd
  have hrep := pow_two_pred_sq (a := a) hr
  rw [hrep]
  have himg : floorPower ((a ^ (2 ^ (r - 1))) ^ 2) = (a ^ (2 ^ (r - 1))) ^ 3 :=
    floorPower_of_odd_sq hs
  rw [himg, ← pow_mul, mul_comm]

theorem hasPowTwoDepth_sq {s r : ℕ} (h : HasPowTwoDepth s r) :
    HasPowTwoDepth (s ^ 2) (r + 1) := by
  obtain ⟨a, ha⟩ := h
  refine ⟨a, ?_⟩
  rw [ha, pow_two_succ_sq]

theorem hasPowTwoDepth_one_iff (n : ℕ) :
    HasPowTwoDepth n 1 ↔ n.sqrt ^ 2 = n := by
  constructor
  · rintro ⟨a, ha⟩
    have : n = a ^ 2 := by simpa using ha
    simp [this, Nat.sqrt_eq']
  · intro h
    exact ⟨n.sqrt, h.symm⟩

/-- A cube that is a `2^m`-th power is the cube of a `2^m`-th power's base. -/
theorem hasPowTwoDepth_of_cube {s m : ℕ}
    (h : HasPowTwoDepth (s ^ 3) m) : HasPowTwoDepth s m := by
  induction m generalizing s with
  | zero => exact ⟨s, by simp⟩
  | succ m ih =>
      obtain ⟨a, ha⟩ := h
      have hsq : IsSquare (s ^ 3) := by
        refine ⟨a ^ (2 ^ m), ?_⟩
        have : a ^ (2 ^ (m + 1)) = (a ^ (2 ^ m)) ^ 2 := pow_two_succ_sq a m
        rw [ha, this, pow_two]
      have hs : IsSquare s := (isSquare_pow_three_iff (n := s)).mp hsq
      obtain ⟨t, ht⟩ := (isSquare_iff_exists_sq s).1 hs
      have ht3 : t ^ 3 = a ^ (2 ^ m) := by
        have hpow : (t ^ 3) ^ 2 = (a ^ (2 ^ m)) ^ 2 := by
          calc
            (t ^ 3) ^ 2 = t ^ 6 := by ring
            _ = (t ^ 2) ^ 3 := by ring
            _ = s ^ 3 := by rw [ht]
            _ = a ^ (2 ^ (m + 1)) := ha
            _ = (a ^ (2 ^ m)) ^ 2 := pow_two_succ_sq a m
        exact Nat.pow_left_injective (by decide : (2 : ℕ) ≠ 0) hpow
      obtain ⟨b, hb⟩ := ih ⟨a, ht3⟩
      refine ⟨b, ?_⟩
      rw [ht, hb, pow_two_succ_sq]

/-- Even exact step drops 2-adic depth by one. -/
theorem hasPowTwoDepth_even_exact {n r : ℕ} (hr : 1 ≤ r)
    (h : HasPowTwoDepth n r) (heven : n % 2 = 0) :
    HasPowTwoDepth (floorPower n) (r - 1) := by
  obtain ⟨a, ha⟩ := h
  rw [ha, floorPower_of_pow_two_depth_even hr (by simpa [ha] using heven)]
  exact ⟨a, rfl⟩

/-- Odd exact step drops 2-adic depth by one (`a^{3·2^{r-1}} = (a^3)^{2^{r-1}}`). -/
theorem hasPowTwoDepth_odd_exact {n r : ℕ} (hr : 1 ≤ r)
    (h : HasPowTwoDepth n r) (hodd : n % 2 = 1) :
    HasPowTwoDepth (floorPower n) (r - 1) := by
  obtain ⟨a, ha⟩ := h
  have haodd : a % 2 = 1 :=
    odd_of_pow_odd (Nat.one_le_pow _ _ (by decide : 0 < 2)) (by simpa [ha] using hodd)
  rw [ha, floorPower_of_pow_two_depth_odd hr haodd]
  refine ⟨a ^ 3, ?_⟩
  rw [← pow_mul, mul_comm]

/-- Depth at least 2 forces the exact image to remain a square. -/
theorem hasPowTwoDepth_ge_two_image_square {n r : ℕ} (hr : 2 ≤ r)
    (h : HasPowTwoDepth n r) :
    (floorPower n).sqrt ^ 2 = floorPower n := by
  have hr1 : 1 ≤ r := le_trans (by decide : 1 ≤ 2) hr
  have himg : HasPowTwoDepth (floorPower n) (r - 1) := by
    rcases Nat.mod_two_eq_zero_or_one n with heven | hodd
    · exact hasPowTwoDepth_even_exact hr1 h heven
    · exact hasPowTwoDepth_odd_exact hr1 h hodd
  have : 1 ≤ r - 1 := by omega
  have : HasPowTwoDepth (floorPower n) 1 := by
    obtain ⟨a, ha⟩ := himg
    refine ⟨a ^ (2 ^ (r - 1 - 1)), ?_⟩
    have hpow : 2 ^ (r - 1) = 2 * 2 ^ (r - 1 - 1) := two_pow_pred this
    have : floorPower n = (a ^ (2 ^ (r - 1 - 1))) ^ 2 := by
      rw [ha, hpow, mul_comm, Nat.pow_mul]
    simpa [HasPowTwoDepth, pow_one] using this
  exact (hasPowTwoDepth_one_iff _).1 this

/-- Depth exactly one: the exact image need not be a square. -/
theorem hasPowTwoDepth_one_image_sq_iff {a : ℕ}
    (heven : (a ^ 2) % 2 = 0) :
    (floorPower (a ^ 2)).sqrt ^ 2 = floorPower (a ^ 2) ↔ a.sqrt ^ 2 = a := by
  rw [floorPower_of_even_sq heven]

theorem hasPowTwoDepth_one_odd_image_sq_iff {a : ℕ} (hodd : a % 2 = 1) :
    (floorPower (a ^ 2)).sqrt ^ 2 = floorPower (a ^ 2) ↔ a.sqrt ^ 2 = a := by
  rw [floorPower_of_odd_sq hodd]
  exact cube_sqrt_sq_iff a

theorem localsTight_implies_power_bound_eq {n : ℕ} :
    ∀ w, follows n w → localsTight n w →
      PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w) := by
  intro w
  induction w generalizing n with
  | nil =>
      intro _ _
      simp [PowerBoundEq]
  | cons b rest ih =>
      intro hw hloc
      cases b with
      | even =>
          have heven : n % 2 = 0 := hw.1
          have hrest : follows (floorPower n) rest := hw.2
          have htail := ih hrest hloc.2
          have hlocal : floorPower n ^ 2 = n := by
            simpa [localTight] using hloc.1
          have hlen : (Branch.even :: rest).length = rest.length + 1 :=
            List.length_cons
          have ho : oddCount (Branch.even :: rest) = oddCount rest := rfl
          unfold PowerBoundEq at htail ⊢
          have h2 : 2 ^ (rest.length + 1) = 2 * 2 ^ rest.length := by
            rw [pow_succ, mul_comm]
          rw [hlen, ho, iterate_cons, h2]
          calc
            (floorPower^[rest.length] (floorPower n)) ^ (2 * 2 ^ rest.length)
              = ((floorPower^[rest.length] (floorPower n)) ^ (2 ^ rest.length)) ^ 2 := by
                rw [mul_comm, Nat.pow_mul]
            _ = (floorPower n ^ (3 ^ oddCount rest)) ^ 2 := by rw [htail]
            _ = (floorPower n ^ 2) ^ (3 ^ oddCount rest) := by
              rw [← Nat.pow_mul, mul_comm, Nat.pow_mul]
            _ = n ^ (3 ^ oddCount rest) := by rw [hlocal]
      | odd =>
          have hodd : n % 2 = 1 := hw.1
          have hrest : follows (floorPower n) rest := hw.2
          have htail := ih hrest hloc.2
          have hlocal : floorPower n ^ 2 = n ^ 3 := by
            simpa [localTight] using hloc.1
          have hlen : (Branch.odd :: rest).length = rest.length + 1 :=
            List.length_cons
          have ho : oddCount (Branch.odd :: rest) = oddCount rest + 1 := rfl
          unfold PowerBoundEq at htail ⊢
          have h2 : 2 ^ (rest.length + 1) = 2 * 2 ^ rest.length := by
            rw [pow_succ, mul_comm]
          rw [hlen, ho, iterate_cons, h2]
          have h3 : 3 ^ (oddCount rest + 1) = 3 * 3 ^ oddCount rest := by
            rw [pow_succ, mul_comm]
          rw [h3]
          calc
            (floorPower^[rest.length] (floorPower n)) ^ (2 * 2 ^ rest.length)
              = ((floorPower^[rest.length] (floorPower n)) ^ (2 ^ rest.length)) ^ 2 := by
                rw [mul_comm, Nat.pow_mul]
            _ = (floorPower n ^ (3 ^ oddCount rest)) ^ 2 := by rw [htail]
            _ = (floorPower n ^ 2) ^ (3 ^ oddCount rest) := by
              rw [← Nat.pow_mul, mul_comm, Nat.pow_mul]
            _ = (n ^ 3) ^ (3 ^ oddCount rest) := by rw [hlocal]
            _ = n ^ (3 * 3 ^ oddCount rest) := (Nat.pow_mul n 3 _).symm

/-- Envelope equality of length `k` forces the start to be a `2^k`-th power. -/
theorem power_bound_eq_implies_pow_two_depth {n : ℕ} {w : List Branch}
    (hw : follows n w)
    (heq : PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) :
    HasPowTwoDepth n w.length := by
  induction w generalizing n with
  | nil => exact hasPowTwoDepth_zero n
  | cons b rest ih =>
      have hfrom :=
        power_bound_eq_from (w := b :: rest) (power_bound_empty n) hw
          (by simpa [image_eq_iterate] using heq)
      have hloc : localsTight n (b :: rest) := hfrom.2
      have hsq : n.sqrt ^ 2 = n :=
        power_bound_eq_implies_square hw heq 0 (Nat.succ_pos _)
      set s := n.sqrt
      have hn : n = s ^ 2 := hsq.symm
      have hrest : follows (floorPower n) rest := by
        cases b with
        | even => exact hw.2
        | odd => exact hw.2
      have htailEq :
          PowerBoundEq (floorPower^[rest.length] (floorPower n)) (floorPower n)
            rest.length (oddCount rest) :=
        localsTight_implies_power_bound_eq rest hrest hloc.2
      have hdepth : HasPowTwoDepth (floorPower n) rest.length :=
        ih hrest htailEq
      have hr : 1 ≤ (b :: rest).length := Nat.succ_pos _
      cases b with
      | even =>
          have heven : n % 2 = 0 := hw.1
          have himg : floorPower n = s := by
            have : floorPower (s ^ 2) = s := floorPower_of_even_sq (by simpa [hn] using heven)
            simpa [hn] using this
          have : HasPowTwoDepth s rest.length := by simpa [himg] using hdepth
          simpa [hn, List.length_cons] using hasPowTwoDepth_sq this
      | odd =>
          have hodd : n % 2 = 1 := hw.1
          have hsodd : s % 2 = 1 :=
            odd_of_pow_odd (by decide : 1 ≤ 2) (by simpa [hn] using hodd)
          have himg : floorPower n = s ^ 3 := by
            have : floorPower (s ^ 2) = s ^ 3 := floorPower_of_odd_sq hsodd
            simpa [hn] using this
          have : HasPowTwoDepth (s ^ 3) rest.length := by simpa [himg] using hdepth
          have hs : HasPowTwoDepth s rest.length := hasPowTwoDepth_of_cube this
          simpa [hn, List.length_cons] using hasPowTwoDepth_sq hs

theorem hasPowTwoDepth_two_le {n r : ℕ} (hn : 2 ≤ n) (h : HasPowTwoDepth n r) :
    2 ^ (2 ^ r) ≤ n := by
  obtain ⟨a, ha⟩ := h
  have ha2 : 2 ≤ a := by
    by_contra hlt
    have : a ≤ 1 := Nat.lt_succ_iff.mp (lt_of_not_ge hlt)
    interval_cases a
    · have : n = 0 := by simp [ha]
      omega
    · have : n = 1 := by simp [ha]
      omega
  have : 2 ^ (2 ^ r) ≤ a ^ (2 ^ r) := Nat.pow_le_pow_left ha2 _
  simpa [ha] using this

/-- A contracting equality word of length `k` at `n ≥ 2` is at least `2^{2^k}`. -/
theorem power_bound_eq_contracts_pow_two_lb {n : ℕ} {w : List Branch}
    (hn : 2 ≤ n) (hw : follows n w)
    (heq : PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) :
    2 ^ (2 ^ w.length) ≤ n :=
  hasPowTwoDepth_two_le hn (power_bound_eq_implies_pow_two_depth hw heq)

/-!
## Extremal equality language

Parity rigidity of exact perfect-power states, and the monochrome
equality-word language. Not an equality-word census and not a
termination theorem.
-/

theorem even_iff_pow_even {a e : ℕ} (he : 1 ≤ e) :
    a % 2 = 0 ↔ (a ^ e) % 2 = 0 := by
  constructor
  · intro ha
    have : Even (a ^ e) := by
      rw [Nat.even_pow]
      exact ⟨Nat.even_iff.2 ha, Nat.pos_iff_ne_zero.mp he⟩
    exact Nat.even_iff.1 this
  · intro h
    by_contra hne
    have ha : a % 2 = 1 := by omega
    have : (a ^ e) % 2 = 1 := pow_mod_two_of_odd ha
    omega

theorem odd_iff_pow_odd {a e : ℕ} (he : 1 ≤ e) :
    a % 2 = 1 ↔ (a ^ e) % 2 = 1 := by
  constructor
  · exact pow_mod_two_of_odd
  · exact odd_of_pow_odd he

theorem even_iff_pow_two_depth_even {a r : ℕ} :
    a % 2 = 0 ↔ (a ^ (2 ^ r)) % 2 = 0 :=
  even_iff_pow_even (Nat.one_le_pow r 2 (by decide : 0 < 2))

theorem odd_iff_pow_two_depth_odd {a r : ℕ} :
    a % 2 = 1 ↔ (a ^ (2 ^ r)) % 2 = 1 :=
  odd_iff_pow_odd (Nat.one_le_pow r 2 (by decide : 0 < 2))

/-- An exact step on a square keeps the parity of the state. -/
theorem floorPower_sq_preserves_parity {n : ℕ} (hsq : n.sqrt ^ 2 = n) :
    floorPower n % 2 = n % 2 := by
  set s := n.sqrt
  have hn : n = s ^ 2 := hsq.symm
  rcases Nat.mod_two_eq_zero_or_one n with heven | hodd
  · have himg : floorPower n = s := by
      have : floorPower (s ^ 2) = s :=
        floorPower_of_even_sq (by simpa [hn] using heven)
      simpa [hn] using this
    have hs : s % 2 = 0 :=
      (even_iff_pow_even (by decide : 1 ≤ 2)).2 (by simpa [hn] using heven)
    omega
  · have hs : s % 2 = 1 :=
      odd_of_pow_odd (by decide : 1 ≤ 2) (by simpa [hn] using hodd)
    have himg : floorPower n = s ^ 3 := by
      have : floorPower (s ^ 2) = s ^ 3 := floorPower_of_odd_sq hs
      simpa [hn] using this
    have : (s ^ 3) % 2 = 1 := pow_mod_two_of_odd hs
    omega

theorem floorPower_of_pow_two_depth_even_base {a r : ℕ} (hr : 1 ≤ r)
    (ha : a % 2 = 0) :
    floorPower (a ^ (2 ^ r)) = a ^ (2 ^ (r - 1)) ∧
      (a ^ (2 ^ (r - 1))) % 2 = 0 := by
  have hn : (a ^ (2 ^ r)) % 2 = 0 := even_iff_pow_two_depth_even.1 ha
  refine ⟨floorPower_of_pow_two_depth_even hr hn, ?_⟩
  exact even_iff_pow_two_depth_even.1 ha

theorem floorPower_of_pow_two_depth_odd_base {a r : ℕ} (hr : 1 ≤ r)
    (ha : a % 2 = 1) :
    floorPower (a ^ (2 ^ r)) = a ^ (3 * 2 ^ (r - 1)) ∧
      (a ^ (3 * 2 ^ (r - 1))) % 2 = 1 :=
  ⟨floorPower_of_pow_two_depth_odd hr ha, pow_mod_two_of_odd ha⟩

/-- Exact even or odd branch on `a^{2^r}` keeps the parity of `a`. -/
theorem floorPower_pow_two_depth_preserves_parity {a r : ℕ} (hr : 1 ≤ r) :
    floorPower (a ^ (2 ^ r)) % 2 = a % 2 := by
  rcases Nat.mod_two_eq_zero_or_one a with ha | ha
  · have h := floorPower_of_pow_two_depth_even_base hr ha
    omega
  · have h := floorPower_of_pow_two_depth_odd_base hr ha
    omega

theorem oddCount_replicate_even (k : ℕ) :
    oddCount (List.replicate k Branch.even) = 0 := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [List.replicate_succ, oddCount_even_cons, ih]

theorem oddCount_replicate_odd (k : ℕ) :
    oddCount (List.replicate k Branch.odd) = k := by
  induction k with
  | zero => simp
  | succ k ih =>
      rw [List.replicate_succ, oddCount_odd_cons, ih]

/-- An all-even realized word of length `k ≥ 1` contracts for `n ≥ 2`. -/
theorem even_word_contracts {n k : ℕ} (hn : 2 ≤ n) (hk : 1 ≤ k)
    (hw : follows n (List.replicate k Branch.even)) :
    floorPower^[k] n < n := by
  have h := power_bound_contracts (w := List.replicate k Branch.even) hn hw
  have hgap :
      3 ^ oddCount (List.replicate k Branch.even) <
        2 ^ (List.replicate k Branch.even).length := by
    simp [oddCount_replicate_even, List.length_replicate]
    exact Nat.pos_iff_ne_zero.mp hk
  simpa [List.length_replicate] using h hgap

theorem floorPower_iterate_odd_nondecreasing {m k : ℕ} (hm : 1 ≤ m)
    (hw : follows m (List.replicate k Branch.odd)) :
    m ≤ floorPower^[k] m := by
  induction k generalizing m with
  | zero => simp
  | succ k ih =>
      rw [List.replicate_succ] at hw
      have hodd : m % 2 = 1 := hw.1
      have hstep : m ≤ floorPower m := floorPower_odd_nondecreasing hm hodd
      have hrest := ih (le_trans hm hstep) hw.2
      rw [iterate_cons]
      exact le_trans hstep hrest

/-- An all-odd realized word of length `k ≥ 1` expands for `n ≥ 3`. -/
theorem odd_word_expands {n k : ℕ} (hn : 3 ≤ n) (hk : 1 ≤ k)
    (hw : follows n (List.replicate k Branch.odd)) :
    n < floorPower^[k] n := by
  cases k with
  | zero => exact (Nat.not_succ_le_zero 0 hk).elim
  | succ k =>
      rw [List.replicate_succ] at hw
      have hodd : n % 2 = 1 := hw.1
      have hgt : n < floorPower n := floorPower_odd_gt hn hodd
      have himgpos : 1 ≤ floorPower n := by omega
      have hrest : floorPower n ≤ floorPower^[k] (floorPower n) :=
        floorPower_iterate_odd_nondecreasing himgpos hw.2
      rw [iterate_cons]
      exact lt_of_lt_of_le hgt hrest

/-- Envelope equality forces a monochrome word. -/
theorem power_bound_eq_implies_monochrome {n : ℕ} {w : List Branch}
    (hw : follows n w)
    (heq : PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) :
    w = List.replicate w.length Branch.even ∨
      w = List.replicate w.length Branch.odd := by
  induction w generalizing n with
  | nil => exact Or.inl rfl
  | cons b rest ih =>
      have hsq : n.sqrt ^ 2 = n :=
        power_bound_eq_implies_square hw heq 0 (Nat.succ_pos _)
      have hpar : floorPower n % 2 = n % 2 :=
        floorPower_sq_preserves_parity hsq
      have hfrom :=
        power_bound_eq_from (w := b :: rest) (power_bound_empty n) hw
          (by simpa [image_eq_iterate] using heq)
      have hloc : localsTight n (b :: rest) := hfrom.2
      have hrest : follows (floorPower n) rest := by
        cases b with
        | even => exact hw.2
        | odd => exact hw.2
      have htailEq :
          PowerBoundEq (floorPower^[rest.length] (floorPower n)) (floorPower n)
            rest.length (oddCount rest) :=
        localsTight_implies_power_bound_eq rest hrest hloc.2
      have hmono := ih hrest htailEq
      cases b with
      | even =>
          have heven : n % 2 = 0 := hw.1
          have himg : floorPower n % 2 = 0 := by omega
          have hrestEven : rest = List.replicate rest.length Branch.even := by
            cases hmono with
            | inl h => exact h
            | inr h =>
                cases rest with
                | nil => rfl
                | cons b' rest' =>
                    rw [List.length_cons, List.replicate_succ] at h
                    have hb' : b' = Branch.odd := (List.cons_eq_cons.mp h).1
                    have : floorPower n % 2 = 1 := by
                      rw [hb'] at hrest
                      exact hrest.1
                    omega
          refine Or.inl ?_
          rw [List.length_cons, List.replicate_succ]
          exact congrArg (List.cons Branch.even) hrestEven
      | odd =>
          have hodd : n % 2 = 1 := hw.1
          have himg : floorPower n % 2 = 1 := by omega
          have hrestOdd : rest = List.replicate rest.length Branch.odd := by
            cases hmono with
            | inr h => exact h
            | inl h =>
                cases rest with
                | nil => rfl
                | cons b' rest' =>
                    rw [List.length_cons, List.replicate_succ] at h
                    have hb' : b' = Branch.even := (List.cons_eq_cons.mp h).1
                    have : floorPower n % 2 = 0 := by
                      rw [hb'] at hrest
                      exact hrest.1
                    omega
          refine Or.inr ?_
          rw [List.length_cons, List.replicate_succ]
          exact congrArg (List.cons Branch.odd) hrestOdd

theorem floorPower_iterate_even_pow_two {a : ℕ} (ha : a % 2 = 0) :
    ∀ {k j : ℕ}, j ≤ k →
      floorPower^[j] (a ^ (2 ^ k)) = a ^ (2 ^ (k - j)) := by
  intro k j
  induction j generalizing k with
  | zero =>
      intro _
      simp
  | succ j ih =>
      intro hle
      have hk : 1 ≤ k := by omega
      rw [iterate_cons]
      have hstep : floorPower (a ^ (2 ^ k)) = a ^ (2 ^ (k - 1)) :=
        (floorPower_of_pow_two_depth_even_base hk ha).1
      rw [hstep]
      have hj : j ≤ k - 1 := by omega
      have hkj : k - 1 - j = k - (j + 1) := by
        rw [Nat.sub_right_comm, ← Nat.sub_add_eq]
      rw [ih (k := k - 1) hj, hkj]

theorem floorPower_iterate_odd_pow_two {a : ℕ} (ha : a % 2 = 1) :
    ∀ {k j : ℕ}, j ≤ k →
      floorPower^[j] (a ^ (2 ^ k)) = a ^ (3 ^ j * 2 ^ (k - j)) := by
  intro k j
  induction j generalizing a k with
  | zero =>
      intro _
      simp
  | succ j ih =>
      intro hle
      have hk : 1 ≤ k := by omega
      rw [iterate_cons]
      have hstep : floorPower (a ^ (2 ^ k)) = a ^ (3 * 2 ^ (k - 1)) :=
        (floorPower_of_pow_two_depth_odd_base hk ha).1
      rw [hstep]
      have ha3 : (a ^ 3) % 2 = 1 := pow_mod_two_of_odd ha
      have hform : a ^ (3 * 2 ^ (k - 1)) = (a ^ 3) ^ (2 ^ (k - 1)) := by
        rw [← pow_mul, mul_comm]
      rw [hform]
      have hj : j ≤ k - 1 := by omega
      have hih := ih (a := a ^ 3) (k := k - 1) ha3 hj
      have hkj : k - 1 - j = k - (j + 1) := by
        rw [Nat.sub_right_comm, ← Nat.sub_add_eq]
      rw [hih, ← pow_mul, ← mul_assoc, ← pow_succ', hkj]

theorem floorPower_iterate_even_pow_two_eq {a k : ℕ} (ha : a % 2 = 0) :
    floorPower^[k] (a ^ (2 ^ k)) = a := by
  simpa [pow_one] using floorPower_iterate_even_pow_two ha (j := k) le_rfl

theorem floorPower_iterate_odd_pow_two_eq {a k : ℕ} (ha : a % 2 = 1) :
    floorPower^[k] (a ^ (2 ^ k)) = a ^ (3 ^ k) := by
  simpa [mul_one] using floorPower_iterate_odd_pow_two ha (j := k) le_rfl

theorem follows_replicate_even_pow_two {a : ℕ} (ha : a % 2 = 0) :
    ∀ k, follows (a ^ (2 ^ k)) (List.replicate k Branch.even) := by
  intro k
  induction k with
  | zero => simp [follows]
  | succ k ih =>
      rw [List.replicate_succ]
      refine ⟨even_iff_pow_two_depth_even.1 ha, ?_⟩
      have himg : floorPower (a ^ (2 ^ (k + 1))) = a ^ (2 ^ k) := by
        simpa [Nat.add_sub_cancel] using
          (floorPower_of_pow_two_depth_even_base (Nat.succ_pos k) ha).1
      rw [himg]
      exact ih

theorem follows_replicate_odd_pow_two {a : ℕ} (ha : a % 2 = 1) :
    ∀ k, follows (a ^ (2 ^ k)) (List.replicate k Branch.odd) := by
  intro k
  induction k generalizing a ha with
  | zero => simp [follows]
  | succ k ih =>
      rw [List.replicate_succ]
      refine ⟨odd_iff_pow_two_depth_odd.1 ha, ?_⟩
      have himg : floorPower (a ^ (2 ^ (k + 1))) = (a ^ 3) ^ (2 ^ k) := by
        have h := (floorPower_of_pow_two_depth_odd_base (Nat.succ_pos k) ha).1
        rw [h, Nat.succ_sub_one, ← pow_mul, mul_comm]
      rw [himg]
      exact ih (pow_mod_two_of_odd ha)

theorem power_bound_eq_replicate_even {a k : ℕ} (ha : a % 2 = 0) :
    PowerBoundEq (floorPower^[k] (a ^ (2 ^ k))) (a ^ (2 ^ k)) k 0 := by
  unfold PowerBoundEq
  rw [floorPower_iterate_even_pow_two_eq ha, pow_zero, pow_one]

theorem power_bound_eq_replicate_odd {a k : ℕ} (ha : a % 2 = 1) :
    PowerBoundEq (floorPower^[k] (a ^ (2 ^ k))) (a ^ (2 ^ k)) k k := by
  unfold PowerBoundEq
  rw [floorPower_iterate_odd_pow_two_eq ha, ← Nat.pow_mul, ← Nat.pow_mul, mul_comm]

/-- Equality saturates iff the word is an exact even or odd tower. -/
theorem power_bound_eq_iff_extremal {n : ℕ} {w : List Branch} :
    (follows n w ∧
        PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w)) ↔
      (w = List.replicate w.length Branch.even ∧
          ∃ a, a % 2 = 0 ∧ n = a ^ (2 ^ w.length)) ∨
      (w = List.replicate w.length Branch.odd ∧
          ∃ a, a % 2 = 1 ∧ n = a ^ (2 ^ w.length)) := by
  constructor
  · rintro ⟨hw, heq⟩
    have ⟨a, ha⟩ := power_bound_eq_implies_pow_two_depth hw heq
    rcases Nat.mod_two_eq_zero_or_one n with hn | hn
    · refine Or.inl ?_
      have hwE : w = List.replicate w.length Branch.even := by
        have hmono := power_bound_eq_implies_monochrome hw heq
        cases hmono with
        | inl h => exact h
        | inr h =>
            cases w with
            | nil => rfl
            | cons b rest =>
                rw [List.length_cons, List.replicate_succ] at h
                have hb : b = Branch.odd := (List.cons_eq_cons.mp h).1
                have : n % 2 = 1 := by
                  rw [hb] at hw
                  exact hw.1
                omega
      refine ⟨hwE, a, even_iff_pow_two_depth_even.2 (by simpa [ha] using hn), ha⟩
    · refine Or.inr ?_
      have hwO : w = List.replicate w.length Branch.odd := by
        have hmono := power_bound_eq_implies_monochrome hw heq
        cases hmono with
        | inr h => exact h
        | inl h =>
            cases w with
            | nil => rfl
            | cons b rest =>
                rw [List.length_cons, List.replicate_succ] at h
                have hb : b = Branch.even := (List.cons_eq_cons.mp h).1
                have : n % 2 = 0 := by
                  rw [hb] at hw
                  exact hw.1
                omega
      refine ⟨hwO, a, odd_iff_pow_two_depth_odd.2 (by simpa [ha] using hn), ha⟩
  · rintro (⟨hwE, a, ha, hn⟩ | ⟨hwO, a, ha, hn⟩)
    · set k := w.length
      have hwE' : w = List.replicate k Branch.even := hwE
      rw [hn, hwE']
      refine ⟨follows_replicate_even_pow_two ha k, ?_⟩
      simpa [oddCount_replicate_even] using power_bound_eq_replicate_even (k := k) ha
    · set k := w.length
      have hwO' : w = List.replicate k Branch.odd := hwO
      rw [hn, hwO']
      refine ⟨follows_replicate_odd_pow_two ha k, ?_⟩
      simpa [oddCount_replicate_odd] using power_bound_eq_replicate_odd (k := k) ha

theorem two_pow_two_pow_extremal_even (k : ℕ) :
    follows (2 ^ (2 ^ k)) (List.replicate k Branch.even) ∧
      PowerBoundEq (floorPower^[k] (2 ^ (2 ^ k))) (2 ^ (2 ^ k)) k 0 :=
  ⟨follows_replicate_even_pow_two (by decide : (2 : ℕ) % 2 = 0) k,
    power_bound_eq_replicate_even (by decide : (2 : ℕ) % 2 = 0)⟩

theorem three_pow_two_pow_extremal_odd (k : ℕ) :
    follows (3 ^ (2 ^ k)) (List.replicate k Branch.odd) ∧
      PowerBoundEq (floorPower^[k] (3 ^ (2 ^ k))) (3 ^ (2 ^ k)) k k :=
  ⟨follows_replicate_odd_pow_two (by decide : (3 : ℕ) % 2 = 1) k,
    power_bound_eq_replicate_odd (by decide : (3 : ℕ) % 2 = 1)⟩

/-- Among \(n\ge 3\), an all-odd equality of length `k` is at least `3^{2^k}`. -/
theorem odd_equality_three_pow_le {n k : ℕ} (hn : 3 ≤ n)
    (hw : follows n (List.replicate k Branch.odd))
    (heq : PowerBoundEq (floorPower^[k] n) n k k) :
    3 ^ (2 ^ k) ≤ n := by
  cases k with
  | zero =>
      exact hn
  | succ k =>
      have heq' :
          PowerBoundEq (floorPower^[(List.replicate (k + 1) Branch.odd).length] n) n
            (List.replicate (k + 1) Branch.odd).length
            (oddCount (List.replicate (k + 1) Branch.odd)) := by
        simpa [List.length_replicate, oddCount_replicate_odd] using heq
      have ⟨a, ha⟩ :=
        power_bound_eq_implies_pow_two_depth
          (w := List.replicate (k + 1) Branch.odd) hw heq'
      have hodd : n % 2 = 1 := by
        rw [List.replicate_succ] at hw
        exact hw.1
      have haodd : a % 2 = 1 :=
        odd_iff_pow_two_depth_odd.2 (by simpa [ha] using hodd)
      have ha3 : 3 ≤ a := by
        by_contra hlt
        have : a ≤ 2 := by omega
        interval_cases a
        · have : n = 0 := by simp [ha]
          omega
        · have : n = 1 := by simp [ha]
          omega
        · have : n % 2 = 0 := by
            rw [ha]
            exact even_iff_pow_two_depth_even.1 rfl
          omega
      have : 3 ^ (2 ^ (k + 1)) ≤ a ^ (2 ^ (k + 1)) :=
        Nat.pow_le_pow_left ha3 _
      simpa [ha] using this

/-!
## Defect and sharpness

Composite envelope defect. This is not the refuted local claim
`T(n)^2 < n^3` for every odd `n`, and not a termination theorem.
`StrictPowerBound` is the strict companion of `PowerBound`.
-/

def localDefectEven (x : ℕ) : ℕ := x - floorPower x ^ 2

def localDefectOdd (x : ℕ) : ℕ := x ^ 3 - floorPower x ^ 2

def StrictPowerBound (m n k o : ℕ) : Prop := m ^ (2 ^ k) < n ^ (3 ^ o)

def isMonochrome (w : List Branch) : Prop :=
  w = List.replicate w.length Branch.even ∨
    w = List.replicate w.length Branch.odd

theorem localDefectEven_eq {x : ℕ} (heven : x % 2 = 0) :
    localDefectEven x = x - x.sqrt ^ 2 := by
  simp [localDefectEven, floorPower, heven]

theorem localDefectOdd_eq {x : ℕ} (hodd : x % 2 = 1) :
    localDefectOdd x = x ^ 3 - (x ^ 3).sqrt ^ 2 := by
  simp [localDefectOdd, floorPower_odd_eq hodd]

theorem localDefectEven_add {x : ℕ} (heven : x % 2 = 0) :
    floorPower x ^ 2 + localDefectEven x = x :=
  Nat.add_sub_of_le (floorPower_even_sq_le heven)

theorem localDefectOdd_add {x : ℕ} (hodd : x % 2 = 1) :
    floorPower x ^ 2 + localDefectOdd x = x ^ 3 :=
  Nat.add_sub_of_le (floorPower_odd_sq_le_cube hodd)

theorem localDefectEven_eq_zero_iff {x : ℕ} (heven : x % 2 = 0) :
    localDefectEven x = 0 ↔ x.sqrt ^ 2 = x := by
  rw [localDefectEven_eq heven, Nat.sub_eq_zero_iff_le]
  constructor
  · intro h
    exact le_antisymm (by simpa [pow_two] using Nat.sqrt_le x) h
  · intro h
    exact h.ge

theorem localDefectOdd_eq_zero_iff {x : ℕ} (hodd : x % 2 = 1) :
    localDefectOdd x = 0 ↔ x.sqrt ^ 2 = x := by
  constructor
  · intro h
    have hadd := localDefectOdd_add hodd
    rw [h, Nat.add_zero] at hadd
    exact (floorPower_odd_sq_eq_cube_iff_square hodd).mp hadd
  · intro hsq
    have : floorPower x ^ 2 = x ^ 3 :=
      (floorPower_odd_sq_eq_cube_iff_square hodd).mpr hsq
    simp [localDefectOdd, this]

theorem localDefectEven_lt_succ_sqrt {x : ℕ} (heven : x % 2 = 0) :
    localDefectEven x < 2 * x.sqrt + 1 := by
  rw [localDefectEven_eq heven]
  have hle : x.sqrt * x.sqrt ≤ x := Nat.sqrt_le x
  have hlt : x < (x.sqrt + 1) * (x.sqrt + 1) := by
    simpa [Nat.succ_eq_add_one] using Nat.lt_succ_sqrt x
  have hbin : (x.sqrt + 1) * (x.sqrt + 1) = x.sqrt ^ 2 + 2 * x.sqrt + 1 := by ring
  have hsq : x.sqrt ^ 2 = x.sqrt * x.sqrt := pow_two _
  omega

theorem pow_sq_lt {a b e : ℕ} (h : a ^ 2 < b) (he : e ≠ 0) :
    a ^ (2 * e) < b ^ e := by
  have : (a ^ 2) ^ e < b ^ e := Nat.pow_lt_pow_left h he
  rwa [← Nat.pow_mul] at this

theorem pow_add_pow_le_add_pow {b d e : ℕ} (he : 1 ≤ e) :
    b ^ e + d ^ e ≤ (b + d) ^ e := by
  cases e with
  | zero => exact (Nat.not_succ_le_zero 0 he).elim
  | succ e =>
      have hb : b ^ e ≤ (b + d) ^ e := Nat.pow_le_pow_left (Nat.le_add_right b d) _
      have hd : d ^ e ≤ (b + d) ^ e := Nat.pow_le_pow_left (Nat.le_add_left d b) _
      calc
        b ^ (e + 1) + d ^ (e + 1)
          = b * b ^ e + d * d ^ e := by
            rw [pow_succ, pow_succ, mul_comm (b ^ e), mul_comm (d ^ e)]
        _ ≤ b * (b + d) ^ e + d * (b + d) ^ e :=
            add_le_add (Nat.mul_le_mul_left b hb) (Nat.mul_le_mul_left d hd)
        _ = (b + d) * (b + d) ^ e := by ring
        _ = (b + d) ^ (e + 1) := by rw [pow_succ, mul_comm]

theorem pow_sub_pow_ge_sub {a b e : ℕ} (hba : b ≤ a) (he : 1 ≤ e) :
    a - b ≤ a ^ e - b ^ e := by
  set d := a - b
  have ha : b + d = a := Nat.add_sub_of_le hba
  have hsum : b ^ e + d ^ e ≤ a ^ e := by
    simpa [ha] using pow_add_pow_le_add_pow (b := b) (d := d) he
  have hd : d ≤ d ^ e := Nat.le_self_pow (Nat.pos_iff_ne_zero.mp he) d
  have : d ^ e ≤ a ^ e - b ^ e :=
    Nat.le_sub_of_add_le (add_comm (b ^ e) _ ▸ hsum)
  exact le_trans hd this

theorem strict_power_bound_append_even {m n k o : ℕ}
    (h : StrictPowerBound m n k o) (heven : m % 2 = 0) :
    StrictPowerBound (floorPower m) n (k + 1) o := by
  have hsq : floorPower m ^ 2 ≤ m := floorPower_even_sq_le heven
  unfold StrictPowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  rw [h2]
  exact lt_of_le_of_lt (pow_sq_le hsq) h

theorem strict_power_bound_append_odd {m n k o : ℕ}
    (h : StrictPowerBound m n k o) (hodd : m % 2 = 1) :
    StrictPowerBound (floorPower m) n (k + 1) (o + 1) := by
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  unfold StrictPowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hmid : m ^ (3 * 2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
    rw [mul_comm, Nat.pow_mul]
  have hle : floorPower m ^ (2 ^ (k + 1)) ≤ (m ^ (2 ^ k)) ^ 3 := by
    rw [h2]
    exact (pow_sq_le_cube hsq).trans_eq hmid
  have hlt : (m ^ (2 ^ k)) ^ 3 < (n ^ (3 ^ o)) ^ 3 :=
    Nat.pow_lt_pow_left h (by decide : (3 : ℕ) ≠ 0)
  have hright : (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ (o + 1)) := by
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  exact lt_of_le_of_lt hle (hlt.trans_eq hright)

theorem strict_power_bound_of_even_defect {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) :
    StrictPowerBound (floorPower m) n (k + 1) o := by
  unfold StrictPowerBound PowerBoundEq at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  rw [h2, Nat.pow_mul, ← h]
  exact Nat.pow_lt_pow_left hδ (pow_ne_zero_two_pow k)

theorem strict_power_bound_of_odd_defect {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) :
    StrictPowerBound (floorPower m) n (k + 1) (o + 1) := by
  unfold StrictPowerBound PowerBoundEq at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  rw [h2, Nat.pow_mul]
  have : (floorPower m ^ 2) ^ (2 ^ k) < (m ^ 3) ^ (2 ^ k) :=
    Nat.pow_lt_pow_left hδ (pow_ne_zero_two_pow k)
  have hmid : (m ^ 3) ^ (2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
    rw [← Nat.pow_mul, mul_comm, Nat.pow_mul]
  have hends : (m ^ (2 ^ k)) ^ 3 = n ^ (3 ^ (o + 1)) := by
    rw [h]
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  exact this.trans_eq (hmid.trans hends)

theorem even_defect_gap_ge_local {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) :
    localDefectEven m ≤ n ^ (3 ^ o) - floorPower m ^ (2 ^ (k + 1)) := by
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hle : floorPower m ^ 2 ≤ m := le_of_lt hδ
  have hgap : m - floorPower m ^ 2 ≤ m ^ (2 ^ k) - (floorPower m ^ 2) ^ (2 ^ k) :=
    pow_sub_pow_ge_sub hle (Nat.one_le_pow _ _ (by decide : 0 < 2))
  unfold PowerBoundEq at h
  simpa [localDefectEven, h, h2, Nat.pow_mul] using hgap

theorem odd_defect_gap_ge_local {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) :
    localDefectOdd m ≤ n ^ (3 ^ (o + 1)) - floorPower m ^ (2 ^ (k + 1)) := by
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have h3 : 3 ^ (o + 1) = 3 * 3 ^ o := three_pow_succ o
  have hle : floorPower m ^ 2 ≤ m ^ 3 := le_of_lt hδ
  have hgap :
      (m ^ 3) ^ (2 ^ k) - (floorPower m ^ 2) ^ (2 ^ k) ≥ m ^ 3 - floorPower m ^ 2 :=
    pow_sub_pow_ge_sub hle (Nat.one_le_pow _ _ (by decide : 0 < 2))
  have hmid : (m ^ 3) ^ (2 ^ k) = n ^ (3 ^ (o + 1)) := by
    have : (m ^ 3) ^ (2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
      rw [← Nat.pow_mul, mul_comm, Nat.pow_mul]
    rw [this, h]
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  simpa [localDefectOdd, h2, Nat.pow_mul, hmid] using hgap

theorem strict_power_bound_from {start current k o : ℕ}
    (hbound : StrictPowerBound current start k o) :
    ∀ w, follows current w →
      StrictPowerBound (image current w) start (k + w.length)
        (o + oddCount w) := by
  intro w
  induction w generalizing current k o with
  | nil =>
      intro _
      simpa using hbound
  | cons b rest ih =>
      intro hw
      cases b with
      | even =>
          have heven : current % 2 = 0 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o)
              (strict_power_bound_append_even hbound heven) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          simp [List.length_cons]
          rw [hk]
          exact hih
      | odd =>
          have hodd : current % 2 = 1 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o + 1)
              (strict_power_bound_append_odd hbound hodd) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have ho : o + (oddCount rest + 1) = o + 1 + oddCount rest := by omega
          simp [List.length_cons]
          rw [hk, ho]
          exact hih

theorem power_bound_word_strict {n : ℕ} {w : List Branch}
    (hw : follows n w) (hmix : ¬ isMonochrome w) :
    StrictPowerBound (floorPower^[w.length] n) n w.length (oddCount w) := by
  have hle : PowerBound (floorPower^[w.length] n) n w.length (oddCount w) :=
    power_bound_follows hw
  have hne : ¬ PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w) := by
    intro heq
    exact hmix (power_bound_eq_implies_monochrome hw heq)
  exact lt_of_le_of_ne hle hne

theorem strict_power_bound_of_not_extremal {n : ℕ} {w : List Branch}
    (hw : follows n w)
    (hnot :
      ¬ ((w = List.replicate w.length Branch.even ∧
            ∃ a, a % 2 = 0 ∧ n = a ^ (2 ^ w.length)) ∨
          (w = List.replicate w.length Branch.odd ∧
            ∃ a, a % 2 = 1 ∧ n = a ^ (2 ^ w.length)))) :
    StrictPowerBound (floorPower^[w.length] n) n w.length (oddCount w) := by
  have hle := power_bound_follows hw
  have hne : ¬ PowerBoundEq (floorPower^[w.length] n) n w.length (oddCount w) := by
    intro heq
    exact hnot (power_bound_eq_iff_extremal.mp ⟨hw, heq⟩)
  exact lt_of_le_of_ne hle hne

theorem power_bound_defect_ge_one {n : ℕ} {w : List Branch}
    (hw : follows n w) (hmix : ¬ isMonochrome w) :
    1 ≤ n ^ (3 ^ oddCount w) - (floorPower^[w.length] n) ^ (2 ^ w.length) := by
  have hlt := power_bound_word_strict hw hmix
  have hle : (floorPower^[w.length] n) ^ (2 ^ w.length) + 1 ≤
      n ^ (3 ^ oddCount w) := Nat.succ_le_of_lt hlt
  exact Nat.le_sub_of_add_le (add_comm _ 1 ▸ hle)

theorem not_localsTight_of_nonmonochrome {n : ℕ} {w : List Branch}
    (hw : follows n w) (hmix : ¬ isMonochrome w) :
    ¬ localsTight n w := by
  intro htight
  have heq := localsTight_implies_power_bound_eq w hw htight
  exact hmix (power_bound_eq_implies_monochrome hw heq)

/-- Numeric companion of `PowerBound`. Nonnegative once the weak bound holds. -/
def powerDeficit (m n k o : ℕ) : ℕ := n ^ (3 ^ o) - m ^ (2 ^ k)

theorem powerBound_of_eq {m n k o : ℕ} (h : PowerBoundEq m n k o) :
    PowerBound m n k o :=
  le_of_eq h

theorem power_bound_eq_empty (n : ℕ) : PowerBoundEq n n 0 0 := by
  simp [PowerBoundEq]

theorem power_deficit_append_even {m n k o : ℕ}
    (_h : PowerBound m n k o) (heven : m % 2 = 0) :
    powerDeficit m n k o ≤ powerDeficit (floorPower m) n (k + 1) o := by
  unfold powerDeficit
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hle : floorPower m ^ (2 ^ (k + 1)) ≤ m ^ (2 ^ k) := by
    rw [h2]
    exact pow_sq_le (floorPower_even_sq_le heven)
  exact Nat.sub_le_sub_left hle _

theorem power_deficit_append_odd {m n k o : ℕ}
    (h : PowerBound m n k o) (hodd : m % 2 = 1) :
    powerDeficit m n k o ≤ powerDeficit (floorPower m) n (k + 1) (o + 1) := by
  unfold powerDeficit PowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  have hmid : m ^ (3 * 2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
    rw [mul_comm, Nat.pow_mul]
  have hT : floorPower m ^ (2 ^ (k + 1)) ≤ (m ^ (2 ^ k)) ^ 3 := by
    rw [h2]
    exact (pow_sq_le_cube hsq).trans_eq hmid
  have hright : (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ (o + 1)) := by
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  have hcube :
      n ^ (3 ^ o) - m ^ (2 ^ k) ≤
        (n ^ (3 ^ o)) ^ 3 - (m ^ (2 ^ k)) ^ 3 :=
    pow_sub_pow_ge_sub h (by decide : (1 : ℕ) ≤ 3)
  have hdrop :
      (n ^ (3 ^ o)) ^ 3 - (m ^ (2 ^ k)) ^ 3 ≤
        (n ^ (3 ^ o)) ^ 3 - floorPower m ^ (2 ^ (k + 1)) :=
    Nat.sub_le_sub_left hT _
  have : n ^ (3 ^ o) - m ^ (2 ^ k) ≤
      (n ^ (3 ^ o)) ^ 3 - floorPower m ^ (2 ^ (k + 1)) :=
    le_trans hcube hdrop
  rwa [hright] at this

theorem power_deficit_from {start current k o : ℕ}
    (hbound : PowerBound current start k o) :
    ∀ w, follows current w →
      powerDeficit current start k o ≤
        powerDeficit (image current w) start (k + w.length)
          (o + oddCount w) := by
  intro w
  induction w generalizing current k o with
  | nil =>
      intro _
      exact le_rfl
  | cons b rest ih =>
      intro hw
      cases b with
      | even =>
          have heven : current % 2 = 0 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hstep := power_deficit_append_even hbound heven
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o)
              (power_bound_append_even hbound heven) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          simp [List.length_cons]
          rw [hk]
          exact le_trans hstep hih
      | odd =>
          have hodd : current % 2 = 1 := hw.1
          have hrest : follows (floorPower current) rest := hw.2
          have hstep := power_deficit_append_odd hbound hodd
          have hih :=
            ih (current := floorPower current) (k := k + 1) (o := o + 1)
              (power_bound_append_odd hbound hodd) hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have ho : o + (oddCount rest + 1) = o + 1 + oddCount rest := by omega
          simp [List.length_cons]
          rw [hk, ho]
          exact le_trans hstep hih

theorem local_defect_even_le_suffix_deficit {m n k o : ℕ} {v : List Branch}
    (h : PowerBoundEq m n k o) (heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) (hv : follows (floorPower m) v) :
    localDefectEven m ≤
      powerDeficit (image (floorPower m) v) n
        (k + 1 + v.length) (o + oddCount v) := by
  have hgap : localDefectEven m ≤ powerDeficit (floorPower m) n (k + 1) o :=
    even_defect_gap_ge_local h heven hδ
  have hbound : PowerBound (floorPower m) n (k + 1) o :=
    power_bound_append_even (powerBound_of_eq h) heven
  exact hgap.trans (power_deficit_from hbound v hv)

theorem local_defect_odd_le_suffix_deficit {m n k o : ℕ} {v : List Branch}
    (h : PowerBoundEq m n k o) (hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) (hv : follows (floorPower m) v) :
    localDefectOdd m ≤
      powerDeficit (image (floorPower m) v) n
        (k + 1 + v.length) (o + 1 + oddCount v) := by
  have hgap : localDefectOdd m ≤ powerDeficit (floorPower m) n (k + 1) (o + 1) :=
    odd_defect_gap_ge_local h hodd hδ
  have hbound : PowerBound (floorPower m) n (k + 1) (o + 1) :=
    power_bound_append_odd (powerBound_of_eq h) hodd
  exact hgap.trans (power_deficit_from hbound v hv)

theorem powerDeficit_even_first {n : ℕ} (_heven : n % 2 = 0) :
    powerDeficit (floorPower n) n 1 0 = localDefectEven n := by
  simp [powerDeficit, localDefectEven]

theorem powerDeficit_odd_first {n : ℕ} (_hodd : n % 2 = 1) :
    powerDeficit (floorPower n) n 1 1 = localDefectOdd n := by
  simp [powerDeficit, localDefectOdd]

theorem eq_replicate_even_of_oddCount_zero {w : List Branch}
    (h : oddCount w = 0) : w = List.replicate w.length Branch.even := by
  induction w with
  | nil => simp
  | cons b rest ih =>
      cases b with
      | even =>
          have hrest : oddCount rest = 0 := by simpa using h
          have hk : (Branch.even :: rest).length = rest.length + 1 := rfl
          rw [hk, List.replicate_succ]
          exact congrArg (List.cons Branch.even) (ih hrest)
      | odd =>
          simp at h

theorem pow_sub_pow_gt_sub {a b e : ℕ} (hba : b < a) (he : 2 ≤ e) (ha : 2 ≤ a) :
    a - b < a ^ e - b ^ e := by
  set d := a - b
  have hba' : b ≤ a := le_of_lt hba
  have hdpos : 1 ≤ d := Nat.succ_le_of_lt (Nat.sub_pos_of_lt hba)
  have ha' : b + d = a := Nat.add_sub_of_le hba'
  have hsum : b ^ e + d ^ e ≤ a ^ e := by
    simpa [ha'] using
      pow_add_pow_le_add_pow (b := b) (d := d)
        (le_trans (by decide : (1 : ℕ) ≤ 2) he)
  have hge : d ^ e ≤ a ^ e - b ^ e :=
    Nat.le_sub_of_add_le (add_comm (b ^ e) _ ▸ hsum)
  by_cases hd1 : d ≤ 1
  · have hd : d = 1 := le_antisymm hd1 hdpos
    have hb : 1 ≤ b := by
      have : 2 ≤ b + d := by simpa [ha'] using ha
      omega
    have he1 : 1 ≤ e - 1 := by omega
    have htail : b ^ (e - 1) + 1 ≤ (b + 1) ^ (e - 1) := by
      simpa using pow_add_pow_le_add_pow (b := b) (d := 1) he1
    have ha1 : a = b + 1 := by omega
    have hpow : (b + 1) ^ e = (b + 1) ^ (e - 1) * (b + 1) := by
      rw [← pow_succ, Nat.sub_add_cancel (by omega)]
    have hmul : (b ^ (e - 1) + 1) * (b + 1) ≤ (b + 1) ^ e := by
      rw [hpow]
      exact Nat.mul_le_mul_right _ htail
    have hexp : b ^ e + b ^ (e - 1) + b + 1 ≤ (b + 1) ^ e := by
      have hexpand :
          (b ^ (e - 1) + 1) * (b + 1) = b ^ e + b ^ (e - 1) + b + 1 := by
        calc
          (b ^ (e - 1) + 1) * (b + 1)
            = b ^ (e - 1) * (b + 1) + (b + 1) := by
              rw [add_mul, one_mul]
          _ = b ^ (e - 1) * b + b ^ (e - 1) + (b + 1) := by
              rw [mul_add, mul_one]
          _ = b ^ e + b ^ (e - 1) + (b + 1) := by
              rw [← pow_succ, Nat.sub_add_cancel (by omega)]
          _ = b ^ e + b ^ (e - 1) + b + 1 :=
            (add_assoc (b ^ e + b ^ (e - 1)) b (1 : ℕ)).symm
      exact hexpand ▸ hmul
    have hgap3 : 3 ≤ a ^ e - b ^ e := by
      have hb1 : 1 ≤ b ^ (e - 1) := by
        simpa using Nat.pow_le_pow_left hb (e - 1)
      have h3 : b ^ e + 3 ≤ (b + 1) ^ e := by
        have : 3 ≤ b ^ (e - 1) + b + 1 := by omega
        omega
      simpa [ha1] using Nat.le_sub_of_add_le (add_comm (b ^ e) (3 : ℕ) ▸ h3)
    rw [hd]
    exact Nat.lt_of_lt_of_le (by decide : (1 : ℕ) < 3) hgap3
  · have hlt : 1 < d := Nat.not_le.mp hd1
    have hd2 : 2 ≤ d := Nat.succ_le_of_lt hlt
    have hsq : d < d ^ 2 := by
      have : d * 1 < d * d :=
        Nat.mul_lt_mul_of_pos_left (by omega : 1 < d) (by omega : 0 < d)
      simpa [pow_two] using this
    have hde : d ^ 2 ≤ d ^ e := Nat.pow_le_pow_right hdpos he
    exact lt_of_lt_of_le (lt_of_lt_of_le hsq hde) hge

theorem two_le_two_pow_of_pos {k : ℕ} (hk : 1 ≤ k) : 2 ≤ 2 ^ k :=
  Nat.pow_le_pow_right (by decide : (1 : ℕ) ≤ 2) hk

theorem even_defect_gap_gt_of_pos_prefix {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) (hk : 1 ≤ k) (hm : 2 ≤ m) :
    localDefectEven m < powerDeficit (floorPower m) n (k + 1) o := by
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have he : 2 ≤ 2 ^ k := two_le_two_pow_of_pos hk
  have hgap :
      m - floorPower m ^ 2 < m ^ (2 ^ k) - (floorPower m ^ 2) ^ (2 ^ k) :=
    pow_sub_pow_gt_sub hδ he hm
  unfold PowerBoundEq at h
  simpa [localDefectEven, powerDeficit, h, h2, Nat.pow_mul] using hgap

theorem odd_defect_gap_gt_of_pos_prefix {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) (hk : 1 ≤ k) (hm : 2 ≤ m) :
    localDefectOdd m < powerDeficit (floorPower m) n (k + 1) (o + 1) := by
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have he : 2 ≤ 2 ^ k := two_le_two_pow_of_pos hk
  have hm3 : 2 ≤ m ^ 3 := by
    have : 8 ≤ m ^ 3 := Nat.pow_le_pow_left hm 3
    exact le_trans (by decide : (2 : ℕ) ≤ 8) this
  have hgap :
      m ^ 3 - floorPower m ^ 2 < (m ^ 3) ^ (2 ^ k) - (floorPower m ^ 2) ^ (2 ^ k) :=
    pow_sub_pow_gt_sub hδ he hm3
  have hmid : (m ^ 3) ^ (2 ^ k) = n ^ (3 ^ (o + 1)) := by
    have : (m ^ 3) ^ (2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
      rw [← Nat.pow_mul, mul_comm, Nat.pow_mul]
    rw [this, h]
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  simpa [localDefectOdd, powerDeficit, h2, Nat.pow_mul, hmid] using hgap

theorem power_deficit_append_even_eq {m n k o : ℕ}
    (_h : PowerBound m n k o) (_heven : m % 2 = 0)
    (htight : floorPower m ^ 2 = m) :
    powerDeficit (floorPower m) n (k + 1) o = powerDeficit m n k o := by
  unfold powerDeficit
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hT : floorPower m ^ (2 ^ (k + 1)) = m ^ (2 ^ k) := by
    rw [h2, Nat.pow_mul, htight]
  rw [hT]

theorem power_deficit_append_even_of_defect {m n k o : ℕ}
    (h : PowerBound m n k o) (_heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) :
    powerDeficit m n k o < powerDeficit (floorPower m) n (k + 1) o := by
  unfold powerDeficit PowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hT : floorPower m ^ (2 ^ (k + 1)) = (floorPower m ^ 2) ^ (2 ^ k) := by
    rw [h2, Nat.pow_mul]
  have hlt : (floorPower m ^ 2) ^ (2 ^ k) < m ^ (2 ^ k) :=
    Nat.pow_lt_pow_left hδ (pow_ne_zero_two_pow k)
  rw [hT]
  have hleft :
      n ^ (3 ^ o) - m ^ (2 ^ k) + (floorPower m ^ 2) ^ (2 ^ k) < n ^ (3 ^ o) := by
    have :
        n ^ (3 ^ o) - m ^ (2 ^ k) + (floorPower m ^ 2) ^ (2 ^ k) <
          n ^ (3 ^ o) - m ^ (2 ^ k) + m ^ (2 ^ k) :=
      Nat.add_lt_add_left hlt _
    rwa [Nat.sub_add_cancel h] at this
  have hA :
      n ^ (3 ^ o) - (floorPower m ^ 2) ^ (2 ^ k) + (floorPower m ^ 2) ^ (2 ^ k) =
        n ^ (3 ^ o) :=
    Nat.sub_add_cancel (le_of_lt (lt_of_lt_of_le hlt h))
  have hcmp :
      n ^ (3 ^ o) - m ^ (2 ^ k) + (floorPower m ^ 2) ^ (2 ^ k) <
        n ^ (3 ^ o) - (floorPower m ^ 2) ^ (2 ^ k) + (floorPower m ^ 2) ^ (2 ^ k) := by
    rwa [hA]
  exact Nat.lt_of_add_lt_add_right hcmp

theorem power_deficit_append_odd_of_strict {m n k o : ℕ}
    (h : StrictPowerBound m n k o) (hodd : m % 2 = 1) :
    powerDeficit m n k o < powerDeficit (floorPower m) n (k + 1) (o + 1) := by
  unfold powerDeficit StrictPowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := two_pow_succ k
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  have hmid : m ^ (3 * 2 ^ k) = (m ^ (2 ^ k)) ^ 3 := by
    rw [mul_comm, Nat.pow_mul]
  have hT : floorPower m ^ (2 ^ (k + 1)) ≤ (m ^ (2 ^ k)) ^ 3 := by
    rw [h2]
    exact (pow_sq_le_cube hsq).trans_eq hmid
  have hright : (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ (o + 1)) := by
    calc
      (n ^ (3 ^ o)) ^ 3 = n ^ (3 ^ o * 3) := (Nat.pow_mul n (3 ^ o) 3).symm
      _ = n ^ (3 * 3 ^ o) := by rw [mul_comm]
      _ = n ^ (3 ^ (o + 1)) := by rw [← pow_succ']
  have hmpos : 1 ≤ m := by
    have : m % 2 = 1 := hodd
    omega
  have ha : 2 ≤ n ^ (3 ^ o) := by
    have hb : 1 ≤ m ^ (2 ^ k) := by
      simpa using Nat.pow_le_pow_left hmpos (2 ^ k)
    have : m ^ (2 ^ k) + 1 ≤ n ^ (3 ^ o) := Nat.succ_le_of_lt h
    omega
  have hcube :
      n ^ (3 ^ o) - m ^ (2 ^ k) <
        (n ^ (3 ^ o)) ^ 3 - (m ^ (2 ^ k)) ^ 3 :=
    pow_sub_pow_gt_sub h (by decide : (2 : ℕ) ≤ 3) ha
  have hdrop :
      (n ^ (3 ^ o)) ^ 3 - (m ^ (2 ^ k)) ^ 3 ≤
        (n ^ (3 ^ o)) ^ 3 - floorPower m ^ (2 ^ (k + 1)) :=
    Nat.sub_le_sub_left hT _
  have : n ^ (3 ^ o) - m ^ (2 ^ k) <
      (n ^ (3 ^ o)) ^ 3 - floorPower m ^ (2 ^ (k + 1)) :=
    lt_of_lt_of_le hcube hdrop
  rwa [hright] at this

theorem suffix_deficit_eq_of_exact_even {current start k o : ℕ} {v : List Branch}
    (hbound : PowerBound current start k o)
    (hv : follows current v)
    (hevenV : v = List.replicate v.length Branch.even)
    (htight : localsTight current v) :
    powerDeficit (image current v) start (k + v.length) o
      = powerDeficit current start k o := by
  induction v generalizing current k with
  | nil => simp
  | cons b rest ih =>
      have hklen : (b :: rest).length = rest.length + 1 := rfl
      have hb : b = Branch.even := by
        have hrep : b :: rest = List.replicate (rest.length + 1) Branch.even := by
          simpa [hklen] using hevenV
        rw [List.replicate_succ] at hrep
        exact List.cons.inj hrep |>.1
      cases b with
      | odd => cases hb
      | even =>
          have heven : current % 2 = 0 := hv.1
          have hloc : floorPower current ^ 2 = current := by
            simpa [localTight] using htight.1
          have hstep := power_deficit_append_even_eq hbound heven hloc
          have hrestV : rest = List.replicate rest.length Branch.even := by
            have hrep : Branch.even :: rest =
                List.replicate (rest.length + 1) Branch.even := by
              simpa [hklen] using hevenV
            rw [List.replicate_succ] at hrep
            exact List.cons.inj hrep |>.2
          have hih :=
            ih (power_bound_append_even hbound heven) hv.2 hrestV htight.2
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          simp [List.length_cons]
          rw [hk, hih, hstep]

theorem suffix_eq_of_deficit_eq {current start k o : ℕ} {v : List Branch}
    (hbound : PowerBound current start k o)
    (hstrict : StrictPowerBound current start k o)
    (hv : follows current v)
    (heq : powerDeficit (image current v) start (k + v.length) (o + oddCount v)
            = powerDeficit current start k o) :
    v = List.replicate v.length Branch.even ∧ localsTight current v := by
  induction v generalizing current k o with
  | nil =>
      exact ⟨rfl, trivial⟩
  | cons b rest ih =>
      cases b with
      | even =>
          have heven : current % 2 = 0 := hv.1
          have hrest : follows (floorPower current) rest := hv.2
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          by_cases htight : floorPower current ^ 2 = current
          · have hstep := power_deficit_append_even_eq hbound heven htight
            have hbound' := power_bound_append_even hbound heven
            have hstrict' := strict_power_bound_append_even hstrict heven
            have heq' :
                powerDeficit (image (floorPower current) rest) start
                  (k + 1 + rest.length) (o + oddCount rest) =
                  powerDeficit (floorPower current) start (k + 1) o := by
              simp [List.length_cons] at heq
              rw [hk] at heq
              exact heq.trans hstep.symm
            have ih' := ih hbound' hstrict' hrest heq'
            have hklen : (Branch.even :: rest).length = rest.length + 1 := rfl
            refine ⟨?_, ⟨by simpa [localTight] using htight, ih'.2⟩⟩
            rw [hklen]
            conv => lhs; rw [ih'.1]
            rw [← List.replicate_succ]
          · have hδ : floorPower current ^ 2 < current :=
              lt_of_le_of_ne (floorPower_even_sq_le heven) htight
            have hlt := power_deficit_append_even_of_defect hbound heven hδ
            have hmono :=
              power_deficit_from (power_bound_append_even hbound heven) rest hrest
            have hlt' :
                powerDeficit current start k o <
                  powerDeficit (image (floorPower current) rest) start
                    (k + 1 + rest.length) (o + oddCount rest) :=
              hlt.trans_le hmono
            simp [List.length_cons] at heq
            rw [hk] at heq
            rw [heq] at hlt'
            exact (lt_irrefl _ hlt').elim
      | odd =>
          have hodd : current % 2 = 1 := hv.1
          have hrest : follows (floorPower current) rest := hv.2
          have hlt := power_deficit_append_odd_of_strict hstrict hodd
          have hmono :=
            power_deficit_from
              (power_bound_append_odd (le_of_lt hstrict) hodd) rest hrest
          have hk : k + (rest.length + 1) = k + 1 + rest.length := by omega
          have ho : o + (oddCount rest + 1) = o + 1 + oddCount rest := by omega
          have hlt' :
              powerDeficit current start k o <
                powerDeficit (image (floorPower current) rest) start
                  (k + 1 + rest.length) (o + 1 + oddCount rest) :=
            hlt.trans_le hmono
          simp [List.length_cons] at heq
          rw [hk, ho] at heq
          rw [heq] at hlt'
          exact (lt_irrefl _ hlt').elim

theorem power_deficit_eq_local_even_iff {n : ℕ} {v : List Branch}
    (heven : n % 2 = 0) (hδ : floorPower n ^ 2 < n)
    (hv : follows (floorPower n) v) :
    powerDeficit (image (floorPower n) v) n (v.length + 1) (oddCount v)
      = localDefectEven n ↔
      v = List.replicate v.length Branch.even ∧
        localsTight (floorPower n) v := by
  have hfirst : powerDeficit (floorPower n) n 1 0 = localDefectEven n :=
    powerDeficit_even_first heven
  have hstrict : StrictPowerBound (floorPower n) n 1 0 := by
    simpa [StrictPowerBound] using hδ
  have hbound : PowerBound (floorPower n) n 1 0 := le_of_lt hstrict
  constructor
  · intro heq
    have heq' :
        powerDeficit (image (floorPower n) v) n (1 + v.length) (0 + oddCount v)
          = powerDeficit (floorPower n) n 1 0 := by
      simpa [hfirst, add_comm v.length] using heq
    exact suffix_eq_of_deficit_eq hbound hstrict hv heq'
  · intro ⟨hevenV, htight⟩
    have ho : oddCount v = 0 := by
      rw [hevenV, oddCount_replicate_even]
    have heq := suffix_deficit_eq_of_exact_even hbound hv hevenV htight
    simpa [hfirst, ho, add_comm v.length] using heq

theorem power_deficit_eq_local_odd_iff {n : ℕ} {v : List Branch}
    (hodd : n % 2 = 1) (hδ : floorPower n ^ 2 < n ^ 3)
    (hv : follows (floorPower n) v) :
    powerDeficit (image (floorPower n) v) n (v.length + 1) (oddCount v + 1)
      = localDefectOdd n ↔
      v = List.replicate v.length Branch.even ∧
        localsTight (floorPower n) v := by
  have hfirst : powerDeficit (floorPower n) n 1 1 = localDefectOdd n :=
    powerDeficit_odd_first hodd
  have hstrict : StrictPowerBound (floorPower n) n 1 1 := by
    simpa [StrictPowerBound] using hδ
  have hbound : PowerBound (floorPower n) n 1 1 := le_of_lt hstrict
  constructor
  · intro heq
    have heq' :
        powerDeficit (image (floorPower n) v) n (1 + v.length) (1 + oddCount v)
          = powerDeficit (floorPower n) n 1 1 := by
      simpa [hfirst, add_comm v.length, add_comm (oddCount v)] using heq
    exact suffix_eq_of_deficit_eq hbound hstrict hv heq'
  · intro ⟨hevenV, htight⟩
    have ho : oddCount v = 0 := by
      rw [hevenV, oddCount_replicate_even]
    have heq := suffix_deficit_eq_of_exact_even hbound hv hevenV htight
    simpa [hfirst, ho, add_comm v.length] using heq

/-!
## Inverse floor

Inverse-floor form of a Juggler step. This is the integer interval
for `T(n) = M`, not a termination theorem and not a perfect-power
height.

The remaining Diophantine question — whether an odd first defect can
satisfy `HasPowTwoDepth (floorPower n) s` for some `s ≥ 2` — is not
claimed here. Finite search is not an impossibility theorem.
-/

theorem floor_sqrt_eq_iff_sq_interval {n M : ℕ} :
    n.sqrt = M ↔ M ^ 2 ≤ n ∧ n < (M + 1) ^ 2 := by
  constructor
  · intro h
    subst h
    exact ⟨by simpa [pow_two] using Nat.sqrt_le n,
      by simpa [pow_two, Nat.succ_eq_add_one] using Nat.lt_succ_sqrt n⟩
  · intro ⟨hle, hlt⟩
    apply Nat.eq_of_le_of_lt_succ
    · exact Nat.le_sqrt.mpr (by simpa [pow_two] using hle)
    · exact Nat.sqrt_lt.mpr (by simpa [pow_two] using hlt)

theorem floorPower_even_eq_iff_sq_interval {n M : ℕ} (heven : n % 2 = 0) :
    floorPower n = M ↔ M ^ 2 ≤ n ∧ n < (M + 1) ^ 2 := by
  rw [floorPower_even_eq heven]
  exact floor_sqrt_eq_iff_sq_interval

theorem floorPower_odd_eq_iff_cube_interval {n M : ℕ} (hodd : n % 2 = 1) :
    floorPower n = M ↔ M ^ 2 ≤ n ^ 3 ∧ n ^ 3 < (M + 1) ^ 2 := by
  rw [floorPower_odd_eq hodd]
  exact floor_sqrt_eq_iff_sq_interval

theorem floorPower_odd_eq_pow_two_depth_iff {n a s : ℕ} (hodd : n % 2 = 1) :
    floorPower n = a ^ (2 ^ s) ↔
      a ^ (2 ^ (s + 1)) ≤ n ^ 3 ∧ n ^ 3 < (a ^ (2 ^ s) + 1) ^ 2 := by
  have hsq : (a ^ (2 ^ s)) ^ 2 = a ^ (2 ^ (s + 1)) := (pow_two_succ_sq a s).symm
  constructor
  · intro h
    have hI := (floorPower_odd_eq_iff_cube_interval hodd).mp h
    exact ⟨hsq ▸ hI.1, hI.2⟩
  · intro h
    exact (floorPower_odd_eq_iff_cube_interval hodd).mpr ⟨hsq ▸ h.1, h.2⟩

/-!
## Defect-compensated contraction

Formal drift `3^o > 2^k` does not by itself decide the block direction.
If the envelope deficit exceeds the formal gap `n^{3^o} - n^{2^k}`, the
image still contracts. This is not a halt theorem, not a first-defect
certificate, and not a lower-envelope theory.
-/

/-- Reusable certificate: a deficit larger than the formal exponent gap
forces `m < n` for `n ≥ 2`. -/
theorem power_bound_compensated_contracts
    {m n k o D : ℕ} (_hn : 2 ≤ n)
    (_hpow : PowerBound m n k o)
    (hD : D ≤ powerDeficit m n k o)
    (hgap : n ^ (3 ^ o) - n ^ (2 ^ k) < D) :
    m < n := by
  refine Nat.lt_of_not_ge fun hge => ?_
  have hleft : n ^ (2 ^ k) ≤ m ^ (2 ^ k) := Nat.pow_le_pow_left hge _
  have hΔ : n ^ (3 ^ o) - m ^ (2 ^ k) ≤ n ^ (3 ^ o) - n ^ (2 ^ k) :=
    Nat.sub_le_sub_left hleft _
  unfold powerDeficit at hD
  exact (lt_irrefl D) (lt_of_le_of_lt (le_trans hD hΔ) hgap)

theorem power_bound_compensated_contracts_follows
    {n : ℕ} {w : List Branch} {D : ℕ}
    (hn : 2 ≤ n) (hw : follows n w)
    (hD : D ≤ powerDeficit (floorPower^[w.length] n) n w.length (oddCount w))
    (hgap : n ^ (3 ^ oddCount w) - n ^ (2 ^ w.length) < D) :
    floorPower^[w.length] n < n :=
  power_bound_compensated_contracts hn (power_bound_follows hw) hD hgap

def wordEOO : List Branch := [.even, .odd, .odd]
def wordOOE : List Branch := [.odd, .odd, .even]
def wordOEO : List Branch := [.odd, .even, .odd]

theorem follows_wordEOO_iff {n : ℕ} :
    follows n wordEOO ↔
      n % 2 = 0 ∧
        floorPower n % 2 = 1 ∧
          floorPower (floorPower n) % 2 = 1 := by
  simp [follows, wordEOO]

theorem follows_wordOOE_iff {n : ℕ} :
    follows n wordOOE ↔
      n % 2 = 1 ∧
        floorPower n % 2 = 1 ∧
          floorPower (floorPower n) % 2 = 0 := by
  simp [follows, wordOOE]

theorem follows_wordOEO_iff {n : ℕ} :
    follows n wordOEO ↔
      n % 2 = 1 ∧
        floorPower n % 2 = 0 ∧
          floorPower (floorPower n) % 2 = 1 := by
  simp [follows, wordOEO]

theorem oddCount_wordEOO : oddCount wordEOO = 2 := by simp [wordEOO]
theorem oddCount_wordOOE : oddCount wordOOE = 2 := by simp [wordOOE]
theorem oddCount_wordOEO : oddCount wordOEO = 2 := by simp [wordOEO]
theorem length_wordEOO : wordEOO.length = 3 := by simp [wordEOO]
theorem length_wordOOE : wordOOE.length = 3 := by simp [wordOOE]
theorem length_wordOEO : wordOEO.length = 3 := by simp [wordOEO]

theorem follows_eoo_two : follows 2 wordEOO := by
  rw [follows_wordEOO_iff]; native_decide

theorem follows_eoo_twelve : follows 12 wordEOO := by
  rw [follows_wordEOO_iff]; native_decide

theorem follows_eoo_fourteen : follows 14 wordEOO := by
  rw [follows_wordEOO_iff]; native_decide

theorem floorPower_eoo_two_contracts : floorPower^[3] 2 < 2 := by
  native_decide

theorem floorPower_eoo_twelve_contracts : floorPower^[3] 12 < 12 := by
  native_decide

theorem floorPower_eoo_fourteen_contracts : floorPower^[3] 14 < 14 := by
  native_decide

theorem floorPower_eoo_two_eq : floorPower^[3] 2 = 1 := by
  native_decide

theorem floorPower_eoo_twelve_eq : floorPower^[3] 12 = 11 := by
  native_decide

theorem floorPower_eoo_fourteen_eq : floorPower^[3] 14 = 11 := by
  native_decide

theorem n_lt_formal_gap_three_two {n : ℕ} (hn : 2 ≤ n) :
    n < n ^ 9 - n ^ 8 := by
  have hfact : n ^ 9 - n ^ 8 = n ^ 8 * (n - 1) := by
    rw [pow_succ, Nat.mul_sub_left_distrib, mul_one]
  rw [hfact]
  cases eq_or_lt_of_le hn with
  | inl h2 =>
      subst h2
      native_decide
  | inr hlt =>
      have hn3 : 3 ≤ n := Nat.succ_le_of_lt hlt
      have hself : n ≤ n ^ 8 := Nat.le_self_pow (by decide : 8 ≠ 0) n
      have hmul : n * (n - 1) ≤ n ^ 8 * (n - 1) :=
        Nat.mul_le_mul_right (n - 1) hself
      have hn0 : 0 < n := lt_of_lt_of_le (by decide : 0 < 3) hn3
      have hpred : 1 < n - 1 := by omega
      have hstrict : n * 1 < n * (n - 1) :=
        Nat.mul_lt_mul_of_pos_left hpred hn0
      exact lt_of_lt_of_le (by simpa using hstrict) hmul

theorem localDefectEven_lt_formal_gap_three_two {n : ℕ} (hn : 2 ≤ n) :
    localDefectEven n < n ^ 9 - n ^ 8 :=
  lt_of_le_of_lt (Nat.sub_le _ _) (n_lt_formal_gap_three_two hn)

theorem eoo_first_defect_lt_formal_gap {n : ℕ} (hn : 2 ≤ n)
    (_hw : follows n wordEOO) :
    localDefectEven n < n ^ (3 ^ oddCount wordEOO) - n ^ (2 ^ wordEOO.length) := by
  simpa [oddCount_wordEOO, length_wordEOO] using
    localDefectEven_lt_formal_gap_three_two hn

theorem floorPower_eoo_two_deficit_gt_gap :
    2 ^ (3 ^ 2) - 2 ^ (2 ^ 3) <
      powerDeficit (floorPower^[3] 2) 2 3 2 := by
  native_decide

theorem floorPower_eoo_of_follows {n : ℕ} (hw : follows n wordEOO) :
    floorPower^[3] n = (((n.sqrt ^ 3).sqrt ^ 3).sqrt) := by
  have heven : n % 2 = 0 := (follows_wordEOO_iff.mp hw).1
  have hodd1 : floorPower n % 2 = 1 := (follows_wordEOO_iff.mp hw).2.1
  have h1 : floorPower n = n.sqrt := floorPower_even_eq heven
  have h2 : floorPower (floorPower n) = (n.sqrt ^ 3).sqrt := by
    rw [h1, floorPower_odd_eq (by simpa [h1] using hodd1)]
  have hodd2 : floorPower (floorPower n) % 2 = 1 :=
    (follows_wordEOO_iff.mp hw).2.2
  have h3 : floorPower (floorPower (floorPower n)) =
      ((n.sqrt ^ 3).sqrt ^ 3).sqrt := by
    rw [h2, floorPower_odd_eq (by simpa [h2] using hodd2)]
  simpa [Function.iterate_succ_apply] using h3

theorem eoo_sqrt_odd {n : ℕ} (hw : follows n wordEOO) :
    n.sqrt % 2 = 1 := by
  have h := (follows_wordEOO_iff.mp hw).2.1
  simpa [floorPower_even_eq (follows_wordEOO_iff.mp hw).1] using h

theorem eoo_n_ge_two {n : ℕ} (hw : follows n wordEOO) : 2 ≤ n := by
  have heven : n % 2 = 0 := (follows_wordEOO_iff.mp hw).1
  have hn0 : n ≠ 0 := by
    intro h
    subst h
    simp [follows, wordEOO, floorPower] at hw
  omega

theorem eoo_sqrt_cube_pow_of_small {q : ℕ} (hlo : 5 ≤ q) (hhi : q ≤ 24) :
    ((q ^ 3).sqrt) ^ 3 ≥ (q + 1) ^ 4 := by
  interval_cases q <;> first | omega | native_decide

theorem succ_pow_eight_le_five_mul {s : ℕ} (hs : 5 ≤ s) :
    (s + 1) ^ 8 ≤ 5 * s ^ 8 := by
  have h56 : 5 * (s + 1) ≤ 6 * s := by omega
  have hpow : (5 * (s + 1)) ^ 8 ≤ (6 * s) ^ 8 :=
    Nat.pow_le_pow_left h56 8
  have hmul : 5 ^ 8 * (s + 1) ^ 8 ≤ 6 ^ 8 * s ^ 8 := by
    simpa [mul_pow] using hpow
  have h69 : (6 : ℕ) ^ 8 ≤ 5 ^ 9 := by native_decide
  have hR : 6 ^ 8 * s ^ 8 ≤ 5 ^ 9 * s ^ 8 :=
    Nat.mul_le_mul_right (s ^ 8) h69
  have hchain : 5 ^ 8 * (s + 1) ^ 8 ≤ 5 ^ 9 * s ^ 8 := le_trans hmul hR
  have hrew : 5 ^ 9 * s ^ 8 = 5 ^ 8 * (5 * s ^ 8) := by
    rw [pow_succ']
    ring
  rw [hrew] at hchain
  exact Nat.le_of_mul_le_mul_left hchain (pow_pos (by decide : 0 < 5) 8)

theorem succ_pow_eight_le_pow_nine {s : ℕ} (hs : 5 ≤ s) :
    (s + 1) ^ 8 ≤ s ^ 9 := by
  have h5 := succ_pow_eight_le_five_mul hs
  have hmul : 5 * s ^ 8 ≤ s * s ^ 8 := Nat.mul_le_mul_right (s ^ 8) hs
  have hrew : s * s ^ 8 = s ^ 9 := by
    calc
      s * s ^ 8 = s ^ 8 * s := mul_comm _ _
      _ = s ^ 9 := (pow_succ s 8).symm
  exact le_trans h5 (hrew ▸ hmul)

theorem eoo_qs_le_cbrt {q : ℕ} : q * q.sqrt ≤ (q ^ 3).sqrt := by
  refine Nat.le_sqrt.mpr ?_
  have hs : q.sqrt * q.sqrt ≤ q := Nat.sqrt_le q
  have hleft : (q * q.sqrt) * (q * q.sqrt) = (q * q) * (q.sqrt * q.sqrt) := by
    ring
  have hmid : (q * q) * (q.sqrt * q.sqrt) ≤ (q * q) * q :=
    Nat.mul_le_mul_left (q * q) hs
  have : (q * q.sqrt) * (q * q.sqrt) ≤ q * q * q := by
    simpa [hleft] using hmid
  have : q * q * q = q ^ 3 := by simp [pow_three, mul_assoc]
  simpa [this] using ‹(q * q.sqrt) * (q * q.sqrt) ≤ q * q * q›

theorem eoo_qs_cube_ge_of_ge_twenty_five {q : ℕ} (hq : 25 ≤ q) :
    (q * q.sqrt) ^ 3 ≥ (q + 1) ^ 4 := by
  set s := q.sqrt
  have hs : 5 ≤ s := Nat.le_sqrt.mpr (show 5 * 5 ≤ q from hq)
  have hsq : s * s ≤ q := Nat.sqrt_le q
  have hup : q + 1 ≤ (s + 1) * (s + 1) :=
    Nat.succ_le_of_lt (Nat.lt_succ_sqrt q)
  have hqs : s * s * s ≤ q * s := Nat.mul_le_mul_right s hsq
  have hleft : (s * s * s) ^ 3 ≤ (q * s) ^ 3 := Nat.pow_le_pow_left hqs 3
  have hright : (q + 1) ^ 4 ≤ ((s + 1) * (s + 1)) ^ 4 :=
    Nat.pow_le_pow_left hup 4
  have hs3 : s * s * s = s ^ 3 := by
    simp [pow_three, mul_assoc]
  have hs9 : (s * s * s) ^ 3 = s ^ 9 := by
    rw [hs3]
    calc
      (s ^ 3) ^ 3 = s ^ (3 * 3) := (Nat.pow_mul s 3 3).symm
      _ = s ^ 9 := by norm_num
  have h8 : ((s + 1) * (s + 1)) ^ 4 = (s + 1) ^ 8 := by
    have hexp : (s + 1) * (s + 1) = (s + 1) ^ 2 := (pow_two (s + 1)).symm
    rw [hexp]
    calc
      ((s + 1) ^ 2) ^ 4 = (s + 1) ^ (2 * 4) := (Nat.pow_mul (s + 1) 2 4).symm
      _ = (s + 1) ^ 8 := by norm_num
  have hcmp : (s + 1) ^ 8 ≤ s ^ 9 := succ_pow_eight_le_pow_nine hs
  have hmid : ((s + 1) * (s + 1)) ^ 4 ≤ (s * s * s) ^ 3 := by
    simpa [h8, hs9] using hcmp
  exact le_trans hright (le_trans hmid hleft)

theorem eoo_sqrt_cube_pow_ge {q : ℕ} (hq : 5 ≤ q) :
    ((q ^ 3).sqrt) ^ 3 ≥ (q + 1) ^ 4 := by
  cases lt_or_ge q 25 with
  | inl hlt =>
      have : q ≤ 24 := Nat.lt_succ_iff.mp hlt
      exact eoo_sqrt_cube_pow_of_small hq this
  | inr hge =>
      exact le_trans (eoo_qs_cube_ge_of_ge_twenty_five hge)
        (Nat.pow_le_pow_left eoo_qs_le_cbrt 3)

theorem eoo_image_ge_succ_sq {n : ℕ} (hw : follows n wordEOO)
    (hq : 5 ≤ n.sqrt) :
    (n.sqrt + 1) ^ 2 ≤ floorPower^[3] n := by
  have himg := floorPower_eoo_of_follows hw
  have hpow := eoo_sqrt_cube_pow_ge hq
  have hle : (n.sqrt + 1) ^ 2 ≤ ((n.sqrt ^ 3).sqrt ^ 3).sqrt := by
    refine Nat.le_sqrt.mpr ?_
    have hexp : (n.sqrt + 1) ^ 2 * (n.sqrt + 1) ^ 2 = (n.sqrt + 1) ^ 4 := by
      ring
    simpa [hexp] using hpow
  simpa [himg] using hle

theorem eoo_expands_of_sqrt_ge_five {n : ℕ} (hw : follows n wordEOO)
    (hq : 5 ≤ n.sqrt) :
    n < floorPower^[3] n := by
  have hsucc : n < (n.sqrt + 1) * (n.sqrt + 1) := Nat.lt_succ_sqrt n
  have hsq : (n.sqrt + 1) * (n.sqrt + 1) = (n.sqrt + 1) ^ 2 := by
    simp [pow_two]
  have : n < (n.sqrt + 1) ^ 2 := by simpa [hsq] using hsucc
  exact lt_of_lt_of_le this (eoo_image_ge_succ_sq hw hq)

theorem eoo_sqrt_cases {n : ℕ} (hw : follows n wordEOO) :
    n.sqrt = 1 ∨ n.sqrt = 3 ∨ 5 ≤ n.sqrt := by
  have hodd : n.sqrt % 2 = 1 := eoo_sqrt_odd hw
  have hn : 2 ≤ n := eoo_n_ge_two hw
  have hpos : 1 ≤ n.sqrt := Nat.le_sqrt.mpr (by
    have : 1 ≤ n := le_trans (by decide : 1 ≤ 2) hn
    simpa using this)
  cases lt_or_ge n.sqrt 5 with
  | inr h5 => exact Or.inr (Or.inr h5)
  | inl hlt =>
      have : n.sqrt = 1 ∨ n.sqrt = 3 := by
        interval_cases n.sqrt <;> omega
      exact this.imp_right Or.inl

theorem eoo_eq_two_of_sqrt_one {n : ℕ} (hw : follows n wordEOO)
    (h1 : n.sqrt = 1) : n = 2 := by
  have heven : n % 2 = 0 := (follows_wordEOO_iff.mp hw).1
  have hge : 1 ≤ n := by
    have : 1 * 1 ≤ n := by simpa [h1] using Nat.sqrt_le n
    omega
  have hlt : n < 4 := by
    have : n < (n.sqrt + 1) * (n.sqrt + 1) := Nat.lt_succ_sqrt n
    simpa [h1] using this
  interval_cases n <;> omega

theorem eoo_of_sqrt_three {n : ℕ} (hw : follows n wordEOO)
    (h3 : n.sqrt = 3) : n = 10 ∨ n = 12 ∨ n = 14 := by
  have heven : n % 2 = 0 := (follows_wordEOO_iff.mp hw).1
  have hge : 9 ≤ n := by simpa [h3] using Nat.sqrt_le n
  have hlt : n < 16 := by
    have : n < (n.sqrt + 1) * (n.sqrt + 1) := Nat.lt_succ_sqrt n
    simpa [h3] using this
  interval_cases n <;> omega

theorem floorPower_eoo_image_of_sqrt_three {n : ℕ} (hw : follows n wordEOO)
    (h3 : n.sqrt = 3) : floorPower^[3] n = 11 := by
  have himg := floorPower_eoo_of_follows hw
  have : ((((3 : ℕ) ^ 3).sqrt) ^ 3).sqrt = 11 := by native_decide
  simpa [himg, h3] using this

/-- `EOO` contracts if and only if `n ∈ {2, 12, 14}`. Not a halt theorem. -/
theorem floorPower_eoo_contracts_iff {n : ℕ} (hw : follows n wordEOO) :
    floorPower^[3] n < n ↔ n = 2 ∨ n = 12 ∨ n = 14 := by
  constructor
  · intro hlt
    rcases eoo_sqrt_cases hw with h1 | h3 | h5
    · exact Or.inl (eoo_eq_two_of_sqrt_one hw h1)
    · have hmem := eoo_of_sqrt_three hw h3
      have himg : floorPower^[3] n = 11 :=
        floorPower_eoo_image_of_sqrt_three hw h3
      rcases hmem with rfl | rfl | rfl
      · simp [himg] at hlt
      · exact Or.inr (Or.inl rfl)
      · exact Or.inr (Or.inr rfl)
    · exact (lt_asymm hlt (eoo_expands_of_sqrt_ge_five hw h5)).elim
  · rintro (rfl | rfl | rfl)
    · exact floorPower_eoo_two_contracts
    · exact floorPower_eoo_twelve_contracts
    · exact floorPower_eoo_fourteen_contracts

/-!
## EOO square-root cells

The first even step freezes the remaining `OO` computation on the
square-root cell `[q^2, (q+1)^2)`. Contraction is the threshold
`n > eooCellOutput q`. This explains the enumerated set `{2, 12, 14}`
and is not a halt theorem.
-/

theorem sqrt_cell_iff {n q : ℕ} :
    n.sqrt = q ↔ q ^ 2 ≤ n ∧ n < (q + 1) ^ 2 :=
  floor_sqrt_eq_iff_sq_interval

def eooCellOutput (q : ℕ) : ℕ := (((q ^ 3).sqrt) ^ 3).sqrt

theorem follows_eoo_sqrt_iff {n : ℕ} :
    follows n wordEOO ↔
      n % 2 = 0 ∧ n.sqrt % 2 = 1 ∧ (n.sqrt ^ 3).sqrt % 2 = 1 := by
  constructor
  · intro hw
    have h := follows_wordEOO_iff.mp hw
    refine ⟨h.1, eoo_sqrt_odd hw, ?_⟩
    have h1 : floorPower n = n.sqrt := floorPower_even_eq h.1
    have h2 : floorPower (floorPower n) = (n.sqrt ^ 3).sqrt := by
      rw [h1, floorPower_odd_eq (by simpa [h1] using h.2.1)]
    simpa [h2] using h.2.2
  · intro ⟨heven, hoddq, hoddb⟩
    refine follows_wordEOO_iff.mpr ⟨heven, ?_, ?_⟩
    · simpa [floorPower_even_eq heven] using hoddq
    · have h1 : floorPower n = n.sqrt := floorPower_even_eq heven
      have h2 : floorPower (floorPower n) = (n.sqrt ^ 3).sqrt := by
        rw [h1, floorPower_odd_eq (by simpa [h1] using hoddq)]
      simpa [h2] using hoddb

theorem eoo_output_eq_cell {n : ℕ} (hw : follows n wordEOO) :
    floorPower^[3] n = eooCellOutput n.sqrt :=
  floorPower_eoo_of_follows hw

theorem eoo_output_constant_on_sqrt_cell {n m : ℕ}
    (hn : follows n wordEOO) (hm : follows m wordEOO)
    (hq : n.sqrt = m.sqrt) :
    floorPower^[3] n = floorPower^[3] m := by
  rw [eoo_output_eq_cell hn, eoo_output_eq_cell hm, hq]

/-- On a realized `EOO` start, contraction is the cell threshold
`n > eooCellOutput ⌊√n⌋`. -/
theorem eoo_contracts_on_cell {n : ℕ} (hw : follows n wordEOO) :
    floorPower^[3] n < n ↔ eooCellOutput n.sqrt < n := by
  simp [eoo_output_eq_cell hw]

theorem eoo_cell_output_one : eooCellOutput 1 = 1 := by
  native_decide

theorem eoo_cell_output_three : eooCellOutput 3 = 11 := by
  native_decide

theorem eoo_cell_output_ge_succ_sq {q : ℕ} (hq : 5 ≤ q) :
    (q + 1) ^ 2 ≤ eooCellOutput q := by
  have hpow := eoo_sqrt_cube_pow_ge hq
  refine Nat.le_sqrt.mpr ?_
  have hexp : (q + 1) ^ 2 * (q + 1) ^ 2 = (q + 1) ^ 4 := by ring
  simpa [eooCellOutput, hexp] using hpow

theorem eoo_residue {n : ℕ} (hw : follows n wordEOO) :
    localDefectEven n = n - n.sqrt ^ 2 :=
  localDefectEven_eq (follows_wordEOO_iff.mp hw).1

/-!
## Primitive floor cells and the first-even freeze

Even and odd branches have exact inverse-floor cells. The first even
letter freezes every suffix on the square-root cell. Odd cells contain
at most one integer, so an initial odd letter does not freeze a useful
range. This is not a halt theorem and not a cell-tree calculus.
-/

theorem even_cell_iff {n q : ℕ} (heven : n % 2 = 0) :
    floorPower n = q ↔ q ^ 2 ≤ n ∧ n < (q + 1) ^ 2 :=
  floorPower_even_eq_iff_sq_interval heven

theorem odd_cell_iff {n m : ℕ} (hodd : n % 2 = 1) :
    floorPower n = m ↔ m ^ 2 ≤ n ^ 3 ∧ n ^ 3 < (m + 1) ^ 2 :=
  floorPower_odd_eq_iff_cube_interval hodd

theorem cell_same_next_state {n q : ℕ} (heven : n % 2 = 0)
    (hcell : q ^ 2 ≤ n ∧ n < (q + 1) ^ 2) :
    floorPower n = q :=
  (even_cell_iff heven).mpr hcell

theorem iterate_cons_even {n k : ℕ} (heven : n % 2 = 0) :
    floorPower^[k + 1] n = floorPower^[k] n.sqrt := by
  rw [iterate_cons, floorPower_even_eq heven]

theorem iterate_cons_odd {n k : ℕ} (hodd : n % 2 = 1) :
    floorPower^[k + 1] n = floorPower^[k] (n ^ 3).sqrt := by
  rw [iterate_cons, floorPower_odd_eq hodd]

/-- On a realized first-even word, the suffix is evaluated at `⌊√n⌋`. -/
theorem first_even_freeze {n : ℕ} {v : List Branch}
    (hw : follows n (.even :: v)) :
    floorPower^[v.length + 1] n = floorPower^[v.length] n.sqrt :=
  iterate_cons_even hw.1

theorem first_odd_freeze {n : ℕ} {v : List Branch}
    (hw : follows n (.odd :: v)) :
    floorPower^[v.length + 1] n = floorPower^[v.length] (n ^ 3).sqrt :=
  iterate_cons_odd hw.1

theorem suffix_same_output_on_cell {n₁ n₂ : ℕ} {v : List Branch}
    (h1 : follows n₁ (.even :: v)) (h2 : follows n₂ (.even :: v))
    (hq : n₁.sqrt = n₂.sqrt) :
    floorPower^[v.length + 1] n₁ = floorPower^[v.length + 1] n₂ := by
  rw [first_even_freeze h1, first_even_freeze h2, hq]

/-- First-even contraction is the cell threshold `T_v(⌊√n⌋) < n`. -/
theorem first_even_contracts_iff {n : ℕ} {v : List Branch}
    (hw : follows n (.even :: v)) :
    floorPower^[v.length + 1] n < n ↔
      floorPower^[v.length] n.sqrt < n := by
  simp [first_even_freeze hw]

theorem eoo_from_first_even {n : ℕ} (hw : follows n wordEOO) :
    floorPower^[3] n < n ↔ floorPower^[2] n.sqrt < n :=
  first_even_contracts_iff (v := [.odd, .odd]) (by simpa [wordEOO] using hw)

theorem constant_cell_trichotomy {c lo hi : ℕ} (_h : lo < hi) :
    c < lo ∨ hi ≤ c ∨ (lo ≤ c ∧ c < hi) := by
  omega

theorem constant_cell_all_contract {c lo n : ℕ}
    (hc : c < lo) (hn : lo ≤ n) : c < n :=
  lt_of_lt_of_le hc hn

theorem constant_cell_all_expand {c hi n : ℕ}
    (hc : hi ≤ c) (hn : n < hi) : ¬c < n :=
  fun h => (lt_asymm h) (lt_of_lt_of_le hn hc)

theorem cube_succ_diff (n : ℕ) :
    (n + 1) ^ 3 - n ^ 3 = 3 * n ^ 2 + 3 * n + 1 := by
  have h : (n + 1) ^ 3 = n ^ 3 + (3 * n ^ 2 + 3 * n + 1) := by ring
  omega

theorem sq_succ_diff (m : ℕ) :
    (m + 1) ^ 2 - m ^ 2 = 2 * m + 1 := by
  have h : (m + 1) ^ 2 = m ^ 2 + 2 * m + 1 := by ring
  omega

/-- An odd floor cell `{n : m^2 ≤ n^3 < (m+1)^2}` has at most one point. -/
theorem odd_cell_unique {m a b : ℕ}
    (ha : m ^ 2 ≤ a ^ 3 ∧ a ^ 3 < (m + 1) ^ 2)
    (hb : m ^ 2 ≤ b ^ 3 ∧ b ^ 3 < (m + 1) ^ 2) :
    a = b := by
  wlog hle : a ≤ b generalizing a b
  · exact (this hb ha (le_of_not_ge hle)).symm
  refine eq_of_le_of_not_lt hle fun hlt => ?_
  have hsucc : a + 1 ≤ b := Nat.succ_le_of_lt hlt
  have hcube : (a + 1) ^ 3 ≤ b ^ 3 := Nat.pow_le_pow_left hsucc 3
  have hlt2 : (a + 1) ^ 3 < (m + 1) ^ 2 := lt_of_le_of_lt hcube hb.2
  have hge : m ^ 2 ≤ a ^ 3 := ha.1
  have hgap : (a + 1) ^ 3 - a ^ 3 < (m + 1) ^ 2 - m ^ 2 := by
    have h1 : (a + 1) ^ 3 - a ^ 3 ≤ (a + 1) ^ 3 - m ^ 2 :=
      Nat.sub_le_sub_left hge _
    have h2 : (a + 1) ^ 3 - m ^ 2 < (m + 1) ^ 2 - m ^ 2 :=
      Nat.sub_lt_sub_right
        (le_trans hge (Nat.pow_le_pow_left (Nat.le_succ a) 3)) hlt2
    exact lt_of_le_of_lt h1 h2
  have hlin : 3 * a ^ 2 + 3 * a + 1 < 2 * m + 1 := by
    simpa [cube_succ_diff a, sq_succ_diff m] using hgap
  have h2m : 3 * a ^ 2 + 3 * a + 1 ≤ 2 * m := by omega
  cases Nat.eq_zero_or_pos a with
  | inl ha0 =>
      subst ha0
      have hm0 : m = 0 := Nat.eq_zero_of_le_zero (by simpa using hge)
      subst hm0
      exact (lt_irrefl (1 : ℕ)) hlin
  | inr hap =>
      have hsq : 3 * a ^ 2 ≤ 2 * m :=
        le_trans (Nat.le_add_right _ _) (le_trans (Nat.le_add_right _ _) h2m)
      have h4 : (3 * a ^ 2) ^ 2 ≤ (2 * m) ^ 2 := Nat.pow_le_pow_left hsq 2
      have h9 : 9 * a ^ 4 ≤ 4 * m ^ 2 := by
        simpa [pow_two, pow_succ, pow_zero, mul_assoc, mul_left_comm, mul_comm] using h4
      have hstrict : 4 * a ^ 3 < 9 * a ^ 4 := by
        have hmul : 4 < 9 * a := by omega
        have hpos : 0 < a ^ 3 := pow_pos hap 3
        simpa [mul_assoc, pow_succ, pow_zero] using
          Nat.mul_lt_mul_of_pos_right hmul hpos
      have : 4 * a ^ 3 < 4 * m ^ 2 := lt_of_lt_of_le hstrict h9
      have habs : a ^ 3 < m ^ 2 := (Nat.mul_lt_mul_left (by decide : 0 < 4)).mp this
      exact (lt_irrefl _) (lt_of_lt_of_le habs hge)

/-!
## First-even cell thresholds

On a square-root cell the contracting inputs are the integers
`n ∈ [q^2, (q+1)^2) ∩ (c, ∞)`. Any contraction requires
`c + 1 < (q+1)^2`; the whole cell contracts iff `c < q^2`.
The one-sided power envelope does not prove these lower bounds.
This is not a halt theorem.
-/

theorem sq_lt_succ_sq (q : ℕ) : q ^ 2 < (q + 1) ^ 2 := by
  have h : (q + 1) ^ 2 = q ^ 2 + 2 * q + 1 := by ring
  omega

theorem cell_any_contracts_iff {c lo hi : ℕ} :
    (∃ n, lo ≤ n ∧ n < hi ∧ c < n) ↔ lo < hi ∧ c + 1 < hi := by
  constructor
  · rintro ⟨n, hlo, hhi, hc⟩
    exact ⟨lt_of_le_of_lt hlo hhi, lt_of_le_of_lt (Nat.succ_le_of_lt hc) hhi⟩
  · intro ⟨hcell, hc⟩
    refine ⟨max lo (c + 1), Nat.le_max_left _ _, ?_, ?_⟩
    · exact max_lt_iff.mpr ⟨hcell, hc⟩
    · exact Nat.lt_of_succ_le (Nat.le_max_right _ _)

theorem cell_all_contracts_iff {c lo hi : ℕ} :
    (∀ n, lo ≤ n → n < hi → c < n) ↔ hi ≤ lo ∨ c < lo := by
  constructor
  · intro h
    cases Nat.lt_or_ge lo hi with
    | inl hlt => exact Or.inr (h lo le_rfl hlt)
    | inr hle => exact Or.inl hle
  · rintro (hle | hc) n hlo hhi
    · exact (not_lt_of_ge (le_trans hle hlo) hhi).elim
    · exact lt_of_lt_of_le hc hlo

theorem first_even_any_contracts_iff {c q : ℕ} :
    (∃ n, q ^ 2 ≤ n ∧ n < (q + 1) ^ 2 ∧ c < n) ↔ c + 1 < (q + 1) ^ 2 := by
  constructor
  · intro h
    exact (cell_any_contracts_iff.mp h).2
  · intro h
    exact cell_any_contracts_iff.mpr ⟨sq_lt_succ_sq q, h⟩

theorem first_even_all_contracts_iff {c q : ℕ} :
    (∀ n, q ^ 2 ≤ n → n < (q + 1) ^ 2 → c < n) ↔ c < q ^ 2 := by
  have h := cell_all_contracts_iff (c := c) (lo := q ^ 2) (hi := (q + 1) ^ 2)
  have hne : ¬(q + 1) ^ 2 ≤ q ^ 2 := not_le_of_gt (sq_lt_succ_sq q)
  simp [h, hne]

theorem floorPower_odd_ge {n : ℕ} (hodd : n % 2 = 1) :
    n ≤ floorPower n := by
  rw [floorPower_odd_eq hodd]
  refine Nat.le_sqrt.mpr ?_
  have hn : 1 ≤ n := Nat.one_le_iff_ne_zero.mpr (fun h => by
    subst h
    simp at hodd)
  have : n * n ≤ n * n * n :=
    Nat.le_mul_of_pos_right (n * n) hn
  simpa [pow_two, pow_three, mul_assoc] using this

theorem eooCellOutput_eq_iterate {q : ℕ}
    (hw : follows q [.odd, .odd]) :
    eooCellOutput q = floorPower^[2] q := by
  have hodd : q % 2 = 1 := hw.1
  have h1 : floorPower q = (q ^ 3).sqrt := floorPower_odd_eq hodd
  have hodd2 : floorPower q % 2 = 1 := hw.2.1
  have h2 : floorPower (floorPower q) = ((q ^ 3).sqrt ^ 3).sqrt := by
    rw [h1, floorPower_odd_eq (by simpa [h1] using hodd2)]
  simpa [eooCellOutput, Function.iterate_succ_apply, h1] using h2.symm

/-- For the suffix `OO`, every `q ≥ 5` that realizes the word sits at or
above the next square. So `Q_{OO}` is finite. -/
theorem oo_suffix_threshold {q : ℕ} (hq : 5 ≤ q)
    (hw : follows q [.odd, .odd]) :
    (q + 1) ^ 2 ≤ floorPower^[2] q := by
  simpa [eooCellOutput_eq_iterate hw] using eoo_cell_output_ge_succ_sq hq

theorem follows_oo_of_ooo {q : ℕ}
    (hw : follows q [.odd, .odd, .odd]) :
    follows q [.odd, .odd] :=
  ⟨hw.1, hw.2.1, trivial⟩

theorem ooo_three : floorPower^[3] 3 = 36 := by
  native_decide

/-- For the suffix `OOO`, every `q ≥ 3` that realizes the word sits at or
above the next square. So `Q_{OOO}` is finite. -/
theorem ooo_suffix_threshold {q : ℕ} (hq : 3 ≤ q)
    (hw : follows q [.odd, .odd, .odd]) :
    (q + 1) ^ 2 ≤ floorPower^[3] q := by
  cases lt_or_ge q 5 with
  | inl hlt =>
      have hq3 : q = 3 := by
        have hodd : q % 2 = 1 := hw.1
        omega
      subst hq3
      rw [ooo_three]
      omega
  | inr h5 =>
      have hoo := follows_oo_of_ooo hw
      have h2 := oo_suffix_threshold h5 hoo
      have hodd2 : floorPower^[2] q % 2 = 1 := by
        simpa [Function.iterate_succ_apply] using hw.2.2.1
      have hge : floorPower^[2] q ≤ floorPower^[3] q := by
        simpa [Function.iterate_succ_apply] using floorPower_odd_ge hodd2
      exact le_trans h2 hge

/-!
## Coarse lower growth

The one-sided envelope is an upper bound and cannot prove eventual
non-contraction. For `n ≥ 1` the elementary comparison
`n < 4 · n.sqrt^2` gives a multiplicative lower bound on each branch.
These compose along a fixed word to
`q^{3^o} ≤ D_v · T_v(q)^{2^r}`. If `3^o > 2^{r+1}`, the exponent gap
beats `(q+1)^2` for all sufficiently large `q`. The threshold depends
on `v`. This is not a halt theorem and not a lower-envelope theory.
-/

/-- Weak lower bound `n^{3^o} ≤ D · m^{2^k}`. Separate from `PowerBound`. -/
def LowerPowerBound (m n k o D : ℕ) : Prop :=
  n ^ (3 ^ o) ≤ D * m ^ (2 ^ k)

def lowerDenomFrom (k o D : ℕ) : List Branch → ℕ
  | [] => D
  | .even :: w => lowerDenomFrom (k + 1) o (D * 4 ^ (2 ^ k)) w
  | .odd :: w => lowerDenomFrom (k + 1) (o + 1) (D ^ 3 * 4 ^ (2 ^ k)) w

def lowerDenom (w : List Branch) : ℕ := lowerDenomFrom 0 0 1 w

theorem three_pow_odd (o : ℕ) : 3 ^ o % 2 = 1 := by
  induction o with
  | zero => simp
  | succ o ih =>
      simp [pow_succ, Nat.mul_mod, ih]

theorem two_pow_even_of_pos {k : ℕ} (hk : 1 ≤ k) : 2 ^ k % 2 = 0 := by
  cases k with
  | zero => omega
  | succ k => simp [pow_succ]

/-- No finite word has formal exponent exactly `2`. -/
theorem alpha_ne_two (v : List Branch) :
    3 ^ oddCount v ≠ 2 ^ (v.length + 1) := by
  intro h
  have hodd : 3 ^ oddCount v % 2 = 1 := three_pow_odd _
  have heven : 2 ^ (v.length + 1) % 2 = 0 :=
    two_pow_even_of_pos (Nat.succ_le_succ (Nat.zero_le _))
  rw [h] at hodd
  omega

theorem floorPower_pos {n : ℕ} (hn : 1 ≤ n) : 1 ≤ floorPower n := by
  cases Nat.mod_two_eq_zero_or_one n with
  | inl heven =>
      rw [floorPower_even_eq heven]
      exact Nat.le_sqrt.mpr (by simpa [pow_two] using hn)
  | inr hodd =>
      rw [floorPower_odd_eq hodd]
      have h3 : 1 ≤ n ^ 3 :=
        Nat.succ_le_of_lt (pow_pos (lt_of_lt_of_le (by decide : 0 < 1) hn) 3)
      exact Nat.le_sqrt.mpr (by simpa [pow_two] using h3)

theorem four_mul_sqrt_sq_gt {n : ℕ} (hn : 1 ≤ n) :
    n < 4 * n.sqrt ^ 2 := by
  have hs : 1 ≤ n.sqrt := Nat.le_sqrt.mpr (by simpa [pow_two] using hn)
  have hsucc : n < (n.sqrt + 1) ^ 2 := by
    simpa [pow_two, Nat.succ_eq_add_one] using Nat.lt_succ_sqrt n
  have h2 : n.sqrt + 1 ≤ 2 * n.sqrt := by omega
  have hsq : (n.sqrt + 1) ^ 2 ≤ (2 * n.sqrt) ^ 2 :=
    Nat.pow_le_pow_left h2 2
  have : n < (2 * n.sqrt) ^ 2 := lt_of_lt_of_le hsucc hsq
  have hexp : (2 * n.sqrt) ^ 2 = 4 * n.sqrt ^ 2 := by ring
  simpa [hexp] using this

theorem four_mul_floorPower_even_sq {n : ℕ} (heven : n % 2 = 0)
    (hn : 1 ≤ n) : n ≤ 4 * floorPower n ^ 2 := by
  rw [floorPower_even_eq heven]
  exact Nat.le_of_lt (four_mul_sqrt_sq_gt hn)

theorem four_mul_floorPower_odd_sq {n : ℕ} (hodd : n % 2 = 1)
    (hn : 1 ≤ n) : n ^ 3 ≤ 4 * floorPower n ^ 2 := by
  rw [floorPower_odd_eq hodd]
  have h3 : 1 ≤ n ^ 3 :=
    Nat.succ_le_of_lt (pow_pos (lt_of_lt_of_le (by decide : 0 < 1) hn) 3)
  exact Nat.le_of_lt (four_mul_sqrt_sq_gt h3)

theorem lower_power_empty (n : ℕ) : LowerPowerBound n n 0 0 1 := by
  simp [LowerPowerBound]

theorem lower_power_append_even {m n k o D : ℕ}
    (h : LowerPowerBound m n k o D) (heven : m % 2 = 0) (hm : 1 ≤ m) :
    LowerPowerBound (floorPower m) n (k + 1) o (D * 4 ^ (2 ^ k)) := by
  have h4 := four_mul_floorPower_even_sq heven hm
  unfold LowerPowerBound at *
  have hpow : m ^ (2 ^ k) ≤ (4 * floorPower m ^ 2) ^ (2 ^ k) :=
    Nat.pow_le_pow_left h4 _
  have hle : n ^ (3 ^ o) ≤ D * (4 * floorPower m ^ 2) ^ (2 ^ k) :=
    le_trans h (Nat.mul_le_mul_left D hpow)
  have hexp : (4 * floorPower m ^ 2) ^ (2 ^ k) =
      4 ^ (2 ^ k) * (floorPower m ^ 2) ^ (2 ^ k) := mul_pow 4 _ _
  have hT : (floorPower m ^ 2) ^ (2 ^ k) = floorPower m ^ (2 * 2 ^ k) :=
    (Nat.pow_mul (floorPower m) 2 (2 ^ k)).symm
  calc
    n ^ (3 ^ o)
        ≤ D * (4 * floorPower m ^ 2) ^ (2 ^ k) := hle
    _ = D * (4 ^ (2 ^ k) * (floorPower m ^ 2) ^ (2 ^ k)) := by rw [hexp]
    _ = D * 4 ^ (2 ^ k) * floorPower m ^ (2 * 2 ^ k) := by
        rw [hT, mul_assoc]
    _ = (D * 4 ^ (2 ^ k)) * floorPower m ^ (2 ^ (k + 1)) := by
        rw [two_pow_succ, mul_assoc]

theorem lower_power_append_odd {m n k o D : ℕ}
    (h : LowerPowerBound m n k o D) (hodd : m % 2 = 1) (hm : 1 ≤ m) :
    LowerPowerBound (floorPower m) n (k + 1) (o + 1)
      (D ^ 3 * 4 ^ (2 ^ k)) := by
  have h4 := four_mul_floorPower_odd_sq hodd hm
  unfold LowerPowerBound at *
  have hcube : n ^ (3 ^ (o + 1)) = (n ^ (3 ^ o)) ^ 3 :=
    (pow_three_succ_right n o).symm
  have hD : (n ^ (3 ^ o)) ^ 3 ≤ (D * m ^ (2 ^ k)) ^ 3 :=
    Nat.pow_le_pow_left h 3
  have hexpD : (D * m ^ (2 ^ k)) ^ 3 = D ^ 3 * (m ^ (2 ^ k)) ^ 3 :=
    mul_pow D _ 3
  have h4pow : (m ^ 3) ^ (2 ^ k) ≤ (4 * floorPower m ^ 2) ^ (2 ^ k) :=
    Nat.pow_le_pow_left h4 _
  have hm3 : (m ^ (2 ^ k)) ^ 3 = (m ^ 3) ^ (2 ^ k) := by
    rw [← Nat.pow_mul, ← Nat.pow_mul, mul_comm]
  have hexp : (4 * floorPower m ^ 2) ^ (2 ^ k) =
      4 ^ (2 ^ k) * (floorPower m ^ 2) ^ (2 ^ k) := mul_pow 4 _ _
  have hT : (floorPower m ^ 2) ^ (2 ^ k) = floorPower m ^ (2 * 2 ^ k) :=
    (Nat.pow_mul (floorPower m) 2 (2 ^ k)).symm
  calc
    n ^ (3 ^ (o + 1))
        = (n ^ (3 ^ o)) ^ 3 := hcube
    _ ≤ (D * m ^ (2 ^ k)) ^ 3 := hD
    _ = D ^ 3 * (m ^ (2 ^ k)) ^ 3 := hexpD
    _ = D ^ 3 * (m ^ 3) ^ (2 ^ k) := by rw [hm3]
    _ ≤ D ^ 3 * (4 * floorPower m ^ 2) ^ (2 ^ k) :=
        Nat.mul_le_mul_left _ h4pow
    _ = D ^ 3 * (4 ^ (2 ^ k) * (floorPower m ^ 2) ^ (2 ^ k)) := by rw [hexp]
    _ = D ^ 3 * 4 ^ (2 ^ k) * floorPower m ^ (2 * 2 ^ k) := by
        rw [hT, mul_assoc]
    _ = (D ^ 3 * 4 ^ (2 ^ k)) * floorPower m ^ (2 ^ (k + 1)) := by
        rw [two_pow_succ, mul_assoc]

theorem lower_power_from {start current k o D : ℕ}
    (h : LowerPowerBound current start k o D) (hpos : 1 ≤ current) :
    ∀ v, follows current v →
      LowerPowerBound (image current v) start (k + v.length)
        (o + oddCount v) (lowerDenomFrom k o D v) := by
  intro v
  induction v generalizing current k o D with
  | nil =>
      intro _
      simpa [image, lowerDenomFrom] using h
  | cons b w ih =>
      intro hw
      cases b with
      | even =>
          have heven : current % 2 = 0 := hw.1
          have hrest : follows (floorPower current) w := hw.2
          have hnext := lower_power_append_even h heven hpos
          have hpos' : 1 ≤ floorPower current := floorPower_pos hpos
          have hih := ih hnext hpos' hrest
          simpa [image, lowerDenomFrom, List.length_cons, Nat.add_comm,
            Nat.add_left_comm, Nat.add_assoc] using hih
      | odd =>
          have hodd : current % 2 = 1 := hw.1
          have hrest : follows (floorPower current) w := hw.2
          have hnext := lower_power_append_odd h hodd hpos
          have hpos' : 1 ≤ floorPower current := floorPower_pos hpos
          have hih := ih hnext hpos' hrest
          simpa [image, lowerDenomFrom, List.length_cons, oddCount,
            Nat.add_comm, Nat.add_left_comm, Nat.add_assoc] using hih

theorem lower_growth_word {q : ℕ} {v : List Branch}
    (hq : 1 ≤ q) (hw : follows q v) :
    LowerPowerBound (image q v) q v.length (oddCount v) (lowerDenom v) := by
  simpa [lowerDenom] using lower_power_from (lower_power_empty q) hq v hw

theorem succ_sq_le_four_sq {q : ℕ} (hq : 1 ≤ q) :
    (q + 1) ^ 2 ≤ 4 * q ^ 2 := by
  cases q with
  | zero => omega
  | succ t =>
      have : (t + 2) ^ 2 ≤ 4 * (t + 1) ^ 2 := by
        have hL : (t + 2) ^ 2 = t ^ 2 + 4 * t + 4 := by ring
        have hR : 4 * (t + 1) ^ 2 = 4 * t ^ 2 + 8 * t + 4 := by ring
        have : t ^ 2 + 4 * t + 4 ≤ 4 * t ^ 2 + 8 * t + 4 := by
          exact Nat.add_le_add (Nat.add_le_add (Nat.le_mul_of_pos_left (t ^ 2) (by decide : 1 ≤ 4))
            (Nat.mul_le_mul_right t (by decide : 4 ≤ 8))) le_rfl
        simpa [hL, hR] using this
      simpa [Nat.succ_eq_add_one] using this

theorem superquadratic_gap {v : List Branch}
    (hα : 2 ^ (v.length + 1) < 3 ^ oddCount v) :
    1 ≤ 3 ^ oddCount v - 2 ^ (v.length + 1) :=
  Nat.succ_le_of_lt (Nat.sub_pos_of_lt hα)

theorem lowerDenomFrom_pos (k o D : ℕ) (hD : 1 ≤ D) :
    ∀ w, 1 ≤ lowerDenomFrom k o D w := by
  intro w
  induction w generalizing k o D with
  | nil => simpa [lowerDenomFrom] using hD
  | cons b w ih =>
      cases b with
      | even =>
          have h4 : 1 ≤ (4 : ℕ) ^ (2 ^ k) :=
            Nat.succ_le_of_lt (pow_pos (by decide : 0 < 4) _)
          have hD' : 1 ≤ D * 4 ^ (2 ^ k) := by
            simpa using Nat.mul_le_mul hD h4
          exact ih (k + 1) o _ hD'
      | odd =>
          have h3 : 1 ≤ D ^ 3 := Nat.succ_le_of_lt (pow_pos (lt_of_lt_of_le (by decide : 0 < 1) hD) 3)
          have h4 : 1 ≤ (4 : ℕ) ^ (2 ^ k) :=
            Nat.succ_le_of_lt (pow_pos (by decide : 0 < 4) _)
          have hD' : 1 ≤ D ^ 3 * 4 ^ (2 ^ k) := by
            simpa using Nat.mul_le_mul h3 h4
          exact ih (k + 1) (o + 1) _ hD'

theorem lowerDenom_pos (w : List Branch) : 1 ≤ lowerDenom w :=
  lowerDenomFrom_pos 0 0 1 (by decide) w

theorem pow_le_pow_left_cancel {a b k : ℕ} (hk : 1 ≤ k)
    (h : a ^ k ≤ b ^ k) : a ≤ b := by
  refine le_of_not_gt fun hlt => ?_
  have hlt' : b ^ k < a ^ k :=
    Nat.pow_lt_pow_left hlt (Nat.one_le_iff_ne_zero.mp hk)
  exact (not_le_of_gt hlt') h

/-- Every fixed superquadratic suffix is eventually above the next square.
The threshold `Q0` depends on `v`. -/
theorem eventually_no_first_even_contraction {v : List Branch}
    (hα : 2 ^ (v.length + 1) < 3 ^ oddCount v) :
    ∃ Q0, ∀ q, Q0 ≤ q → follows q v → (q + 1) ^ 2 ≤ image q v := by
  set D := lowerDenom v
  set r := v.length
  set Q0 := D * 4 ^ (2 ^ r)
  refine ⟨Q0, fun q hq hw => ?_⟩
  have hD : 1 ≤ D := lowerDenom_pos v
  have h4p : 1 ≤ (4 : ℕ) ^ (2 ^ r) :=
    Nat.succ_le_of_lt (pow_pos (by decide : 0 < 4) _)
  have hQpos : 1 ≤ Q0 := by
    simpa [Q0] using Nat.mul_le_mul hD h4p
  have hq1 : 1 ≤ q := le_trans hQpos hq
  have hL : LowerPowerBound (image q v) q r (oddCount v) D := by
    simpa [D, r] using lower_growth_word hq1 hw
  have hgap : 1 ≤ 3 ^ oddCount v - 2 ^ (r + 1) := superquadratic_gap (by simpa [r] using hα)
  have hqg : q ≤ q ^ (3 ^ oddCount v - 2 ^ (r + 1)) :=
    le_trans (by simp : q ≤ q ^ 1)
      (Nat.pow_le_pow_right hq1 hgap)
  have hleft : Q0 * q ^ (2 ^ (r + 1)) ≤ q ^ (3 ^ oddCount v) := by
    have hmul : Q0 * q ^ (2 ^ (r + 1)) ≤
        q ^ (3 ^ oddCount v - 2 ^ (r + 1)) * q ^ (2 ^ (r + 1)) :=
      Nat.mul_le_mul_right _ (le_trans hq hqg)
    have hadd : q ^ (3 ^ oddCount v - 2 ^ (r + 1)) * q ^ (2 ^ (r + 1)) =
        q ^ (3 ^ oddCount v) := by
      rw [← Nat.pow_add, Nat.sub_add_cancel (Nat.le_of_lt (by simpa [r] using hα))]
    simpa [hadd] using hmul
  have hsucc : (q + 1) ^ (2 ^ (r + 1)) ≤ 4 ^ (2 ^ r) * q ^ (2 ^ (r + 1)) := by
    have hsq := succ_sq_le_four_sq hq1
    have hpow : ((q + 1) ^ 2) ^ (2 ^ r) ≤ (4 * q ^ 2) ^ (2 ^ r) :=
      Nat.pow_le_pow_left hsq _
    have hLexp : ((q + 1) ^ 2) ^ (2 ^ r) = (q + 1) ^ (2 ^ (r + 1)) := by
      rw [← Nat.pow_mul, two_pow_succ, mul_comm]
    have hRexp : (4 * q ^ 2) ^ (2 ^ r) = 4 ^ (2 ^ r) * q ^ (2 ^ (r + 1)) := by
      rw [mul_pow, ← Nat.pow_mul, two_pow_succ, mul_comm]
    simpa [hLexp, hRexp] using hpow
  have hDsucc : D * (q + 1) ^ (2 ^ (r + 1)) ≤ q ^ (3 ^ oddCount v) :=
    calc
      D * (q + 1) ^ (2 ^ (r + 1))
          ≤ D * (4 ^ (2 ^ r) * q ^ (2 ^ (r + 1))) :=
            Nat.mul_le_mul_left D hsucc
      _ = Q0 * q ^ (2 ^ (r + 1)) := by
            simp [Q0, mul_assoc]
      _ ≤ q ^ (3 ^ oddCount v) := hleft
  have hT : (q + 1) ^ (2 ^ (r + 1)) ≤ image q v ^ (2 ^ r) := by
    have hbound : q ^ (3 ^ oddCount v) ≤ D * image q v ^ (2 ^ r) := hL
    have : D * (q + 1) ^ (2 ^ (r + 1)) ≤ D * image q v ^ (2 ^ r) :=
      le_trans hDsucc hbound
    exact Nat.le_of_mul_le_mul_left this (lt_of_lt_of_le (by decide : 0 < 1) hD)
  have hT' : ((q + 1) ^ 2) ^ (2 ^ r) ≤ image q v ^ (2 ^ r) := by
    have hexp : (q + 1) ^ (2 ^ (r + 1)) = ((q + 1) ^ 2) ^ (2 ^ r) := by
      rw [← Nat.pow_mul, two_pow_succ, mul_comm]
    simpa [hexp] using hT
  exact pow_le_pow_left_cancel
    (Nat.succ_le_of_lt (pow_pos (by decide : 0 < 2) r)) hT'

theorem oo_lower_growth_eventual :
    ∃ Q0, ∀ q, Q0 ≤ q → follows q [.odd, .odd] →
      (q + 1) ^ 2 ≤ image q [.odd, .odd] :=
  eventually_no_first_even_contraction
    (by native_decide : 2 ^ (([.odd, .odd] : List Branch).length + 1) <
      3 ^ oddCount [.odd, .odd])

end Problems.Engine



