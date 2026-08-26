import Mathlib.Algebra.Group.Nat.Even
import Mathlib.Data.Nat.Sqrt
import Mathlib.Tactic

namespace Problems.Engine

/-!
Exact identities for the even/odd floor-power map.
These statements are the problem definition and a finite seed orbit.
They are KNOWN. They are not a halt theorem on all positive integers.
-/

/-- Even `n` maps to `Nat.sqrt n`; odd `n` maps to `Nat.sqrt (n^3)`. -/
def floorPower (n : ℕ) : ℕ :=
  if n % 2 = 0 then n.sqrt else (n * n * n).sqrt

/-- Integer obstruction: `k^4 ≤ n^3` and `n ≥ 2` forbid `k ≥ n`.
This is iterated `Nat.sqrt` of `n^3`, not `T^2` on the odd-to-odd branch. -/
theorem sqrt_sqrt_n_cubed_lt {n : ℕ} (hn : 2 ≤ n) :
    ((n * n * n).sqrt).sqrt < n := by
  set m := (n * n * n).sqrt
  set k := m.sqrt
  have hk : k * k ≤ m := Nat.sqrt_le m
  have hm : m * m ≤ n * n * n := Nat.sqrt_le (n * n * n)
  have hk4 : k * k * (k * k) ≤ m * m := Nat.mul_le_mul hk hk
  have hk4n : k * k * k * k ≤ n * n * n := by
    simpa [mul_assoc] using (le_trans hk4 hm)
  refine Nat.lt_of_not_ge fun hkn => ?_
  have hn4 : n * n * n * n ≤ k * k * k * k := by
    have h2 := Nat.mul_le_mul hkn hkn
    simpa [mul_assoc] using Nat.mul_le_mul h2 h2
  have hle : n * n * n * n ≤ n * n * n := le_trans hn4 hk4n
  have hn0 : 0 < n := lt_of_lt_of_le (by decide : 0 < 2) hn
  have hn3 : 0 < n * n * n := Nat.mul_pos (Nat.mul_pos hn0 hn0) hn0
  have hmul : n * (n * n * n) ≤ 1 * (n * n * n) := by
    simpa [mul_assoc, mul_comm, mul_left_comm] using hle
  have : n ≤ 1 := Nat.le_of_mul_le_mul_right hmul hn3
  omega

/-- On the odd-to-even branch, `T^2(n) < n`. Not a halt theorem for the full map. -/
theorem floorPower_odd_even_two_step_lt
    {n : ℕ} (hn : 2 ≤ n) (hodd : n % 2 = 1)
    (heven : (n * n * n).sqrt % 2 = 0) :
    floorPower (floorPower n) < n := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
  have step2 : floorPower (floorPower n) = ((n * n * n).sqrt).sqrt := by
    rw [step1]
    simp [floorPower, heven]
  rw [step2]
  exact sqrt_sqrt_n_cubed_lt hn

/-- Integer comparison: `(n+1)^2 ≤ n^3` for `n ≥ 3`. Threshold for odd-branch growth. -/
theorem succ_sq_le_cube {n : ℕ} (hn : 3 ≤ n) : (n + 1) ^ 2 ≤ n ^ 3 := by
  zify
  nlinarith

/-- On the odd branch, `n ≥ 3` implies `T(n) > n`. Independent of the parity of `T(n)`. -/
theorem floorPower_odd_gt {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1) :
    n < floorPower n := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
  rw [step1]
  have hsq : (n + 1) ^ 2 ≤ n ^ 3 := succ_sq_le_cube hn
  have hpow : n ^ 3 = n * n * n := by ring
  have : n + 1 ≤ (n * n * n).sqrt := by
    exact Nat.le_sqrt.mpr (by simpa [hpow, pow_two] using hsq)
  omega

/-- The odd branch is nondecreasing: `k ≤ T(k)` when `k` is odd and positive. -/
theorem floorPower_odd_nondecreasing {k : ℕ} (hk : 1 ≤ k) (hodd : k % 2 = 1) :
    k ≤ floorPower k := by
  have hodd0 : k % 2 ≠ 0 := by omega
  have step1 : floorPower k = (k * k * k).sqrt := by
    simp [floorPower, hodd0]
  rw [step1]
  have h1 : k * k ≤ k * k * k := by
    have : 1 ≤ k := hk
    simpa [Nat.mul_assoc] using Nat.mul_le_mul_left (k * k) this
  exact Nat.le_sqrt.mpr h1

/-- On the odd-to-odd branch with `n ≥ 3`, `T^2(n) > n`. Dual of
`floorPower_odd_even_two_step_lt`. Not a divergence theorem. -/
theorem floorPower_odd_odd_two_step_gt
    {n : ℕ} (hn : 3 ≤ n) (hodd : n % 2 = 1)
    (hodd1 : (n * n * n).sqrt % 2 = 1) :
    n < floorPower (floorPower n) := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step1 : floorPower n = (n * n * n).sqrt := by
    simp [floorPower, hodd0]
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
    ((n * n * n).sqrt % 2 = 0 → floorPower (floorPower n) < n) ∧
    ((n * n * n).sqrt % 2 = 1 → n < floorPower (floorPower n)) := by
  refine ⟨?he, ?ho⟩
  · intro heven
    have hn2 : 2 ≤ n := le_trans (by decide : 2 ≤ 3) hn
    exact floorPower_odd_even_two_step_lt hn2 hodd heven
  · intro hodd1
    exact floorPower_odd_odd_two_step_gt hn hodd hodd1

/-- Power comparison for the OOOEE floor-power block: three odd steps
(`x^2 ≤ y^3`) and two even steps (`x^2 ≤ y`) give `n5 ^ 32 ≤ n ^ 27`.
This is the exact surrogate of negative log-log drift on that word. -/
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

/-- On the OOOEE branch word, `T^5(n) < n` for `n ≥ 2`. Conditional block
contraction; not a halt theorem and not a parity-frequency theorem. -/
theorem floorPower_oooee_five_step_lt
    {n : ℕ} (hn : 2 ≤ n) (h0 : n % 2 = 1)
    (h1 : floorPower n % 2 = 1)
    (h2 : floorPower (floorPower n) % 2 = 1)
    (h3 : floorPower (floorPower (floorPower n)) % 2 = 0)
    (h4 : floorPower (floorPower (floorPower (floorPower n))) % 2 = 0) :
    floorPower (floorPower (floorPower (floorPower (floorPower n)))) < n := by
  set n1 := floorPower n
  set n2 := floorPower n1
  set n3 := floorPower n2
  set n4 := floorPower n3
  set n5 := floorPower n4
  have n0ne : n % 2 ≠ 0 := by omega
  have n1ne : n1 % 2 ≠ 0 := by
    have : n1 % 2 = 1 := h1
    omega
  have n2ne : n2 % 2 ≠ 0 := by
    have : n2 % 2 = 1 := h2
    omega
  have n1eq : n1 = (n * n * n).sqrt := by
    simp [n1, floorPower, n0ne]
  have n2eq : n2 = (n1 * n1 * n1).sqrt := by
    simp [n2, floorPower, n1ne]
  have n3eq : n3 = (n2 * n2 * n2).sqrt := by
    simp [n3, floorPower, n2ne]
  have n3even : n3 % 2 = 0 := h3
  have n4eq : n4 = n3.sqrt := by
    simp [n4, floorPower, n3even]
  have n4even : n4 % 2 = 0 := h4
  have n5eq : n5 = n4.sqrt := by
    simp [n5, floorPower, n4even]
  have hn1 : n1 ^ 2 ≤ n ^ 3 := by
    have : n1 * n1 ≤ n * n * n := by simpa [n1eq] using Nat.sqrt_le (n * n * n)
    simpa [pow_two, pow_three, mul_assoc] using this
  have hn2 : n2 ^ 2 ≤ n1 ^ 3 := by
    have : n2 * n2 ≤ n1 * n1 * n1 := by simpa [n2eq] using Nat.sqrt_le (n1 * n1 * n1)
    simpa [pow_two, pow_three, mul_assoc] using this
  have hn3 : n3 ^ 2 ≤ n2 ^ 3 := by
    have : n3 * n3 ≤ n2 * n2 * n2 := by simpa [n3eq] using Nat.sqrt_le (n2 * n2 * n2)
    simpa [pow_two, pow_three, mul_assoc] using this
  have hn4 : n4 ^ 2 ≤ n3 := by
    have : n4 * n4 ≤ n3 := by simpa [n4eq] using Nat.sqrt_le n3
    simpa [pow_two] using this
  have hn5 : n5 ^ 2 ≤ n4 := by
    have : n5 * n5 ≤ n4 := by simpa [n5eq] using Nat.sqrt_le n4
    simpa [pow_two] using this
  have hpow : n5 ^ 32 ≤ n ^ 27 :=
    floorPower_oooee_pow_chain hn1 hn2 hn3 hn4 hn5
  refine Nat.lt_of_not_ge fun hge => ?_
  have hn32 : n ^ 32 ≤ n5 ^ 32 := Nat.pow_le_pow_left hge 32
  have hle : n ^ 32 ≤ n ^ 27 := le_trans hn32 hpow
  have hpos : 0 < n := lt_of_lt_of_le (by decide : 0 < 2) hn
  have h27pos : 0 < n ^ 27 := pow_pos hpos 27
  have hle' : n ^ 27 * n ^ 5 ≤ n ^ 27 * 1 := by
    have heq : n ^ 27 * n ^ 5 = n ^ 32 := (Nat.pow_add n 27 5).symm
    rw [heq, mul_one]
    exact hle
  have hpow5 : n ^ 5 ≤ 1 := Nat.le_of_mul_le_mul_left hle' h27pos
  have hbig : (2 : ℕ) ^ 5 ≤ n ^ 5 := Nat.pow_le_pow_left hn 5
  exact (by decide : ¬(2 : ℕ) ^ 5 ≤ 1) (le_trans hbig hpow5)

/-- Even branch: `T(n)^2 ≤ n`. Exact floor bound, not a real square root. -/
theorem floorPower_even_sq_le {n : ℕ} (heven : n % 2 = 0) :
    floorPower n ^ 2 ≤ n := by
  have step : floorPower n = n.sqrt := by simp [floorPower, heven]
  rw [step]
  simpa [pow_two] using Nat.sqrt_le n

/-- Odd branch: `T(n)^2 ≤ n^3`. Exact floor bound, not a real 3/2-power. -/
theorem floorPower_odd_sq_le_cube {n : ℕ} (hodd : n % 2 = 1) :
    floorPower n ^ 2 ≤ n ^ 3 := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have step : floorPower n = (n * n * n).sqrt := by simp [floorPower, hodd0]
  rw [step]
  have hle : (n * n * n).sqrt * (n * n * n).sqrt ≤ n * n * n := Nat.sqrt_le (n * n * n)
  simpa [pow_two, pow_three, mul_assoc] using hle

/-- Odd squares attain the one-step envelope: odd `m` implies `T(m^2)^2 = (m^2)^3`.
So `n^{3/2}` can be an integer for odd `n≥3`. Mixed-word equality is possible.
This kills any universal lemma `T(n)^2 < n^3` for all odd `n≥3`. -/
theorem floorPower_odd_sq_eq_cube_of_sq {m : ℕ} (hodd : m % 2 = 1) :
    floorPower (m ^ 2) ^ 2 = (m ^ 2) ^ 3 := by
  have nne : (m ^ 2) % 2 ≠ 0 := by
    have : (m ^ 2) % 2 = 1 := by
      rw [Nat.pow_two, Nat.mul_mod, hodd]
    omega
  have step : floorPower (m ^ 2) = ((m ^ 2) * (m ^ 2) * (m ^ 2)).sqrt := by
    simp [floorPower, nne]
  have hcube : (m ^ 2) * (m ^ 2) * (m ^ 2) = (m ^ 3) * (m ^ 3) := by ring
  rw [step, hcube, Nat.sqrt_eq]
  ring

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

/-!
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
  have hmul : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  rw [hmul]
  exact le_trans (pow_sq_le hsq) h

theorem power_bound_append_odd {m n k o : ℕ}
    (h : PowerBound m n k o) (hodd : m % 2 = 1) :
    PowerBound (floorPower m) n (k + 1) (o + 1) := by
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  unfold PowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have h3 : 3 ^ (o + 1) = 3 * 3 ^ o := by rw [pow_succ, mul_comm]
  rw [h2, h3]
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

theorem floorPower_oooee_of_follows {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOOEE) :
    floorPower^[5] n < n := by
  have h := power_bound_contracts (w := wordOOOEE) hn hw
  have hgap : 3 ^ oddCount wordOOOEE < 2 ^ wordOOOEE.length := by
    native_decide
  simpa [wordOOOEE] using h hgap

theorem floorPower_oooeeeoo_of_follows {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOOEEEOO) :
    floorPower^[8] n < n := by
  have h := power_bound_contracts (w := wordOOOEEEOO) hn hw
  have hgap : 3 ^ oddCount wordOOOEEEOO < 2 ^ wordOOOEEEOO.length := by
    native_decide
  simpa [wordOOOEEEOO] using h hgap

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

/-- On the OOOEEEOO branch word, `T^8(n) < n` for `n ≥ 2`. Conditional
block contraction; not a halt theorem and not a parity-frequency theorem. -/
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
  set n1 := floorPower n
  set n2 := floorPower n1
  set n3 := floorPower n2
  set n4 := floorPower n3
  set n5 := floorPower n4
  set n6 := floorPower n5
  set n7 := floorPower n6
  set n8 := floorPower n7
  have hn1 : n1 ^ 2 ≤ n ^ 3 := floorPower_odd_sq_le_cube h0
  have hn2 : n2 ^ 2 ≤ n1 ^ 3 := floorPower_odd_sq_le_cube h1
  have hn3 : n3 ^ 2 ≤ n2 ^ 3 := floorPower_odd_sq_le_cube h2
  have hn4 : n4 ^ 2 ≤ n3 := floorPower_even_sq_le h3
  have hn5 : n5 ^ 2 ≤ n4 := floorPower_even_sq_le h4
  have hn6 : n6 ^ 2 ≤ n5 := floorPower_even_sq_le h5
  have hn7 : n7 ^ 2 ≤ n6 ^ 3 := floorPower_odd_sq_le_cube h6
  have hn8 : n8 ^ 2 ≤ n7 ^ 3 := floorPower_odd_sq_le_cube h7
  have hpow : n8 ^ 256 ≤ n ^ 243 :=
    floorPower_oooeeeoo_pow_chain hn1 hn2 hn3 hn4 hn5 hn6 hn7 hn8
  refine Nat.lt_of_not_ge fun hge => ?_
  have hn256 : n ^ 256 ≤ n8 ^ 256 := Nat.pow_le_pow_left hge 256
  have hle : n ^ 256 ≤ n ^ 243 := le_trans hn256 hpow
  have hlt : n ^ 243 < n ^ 256 := pow_lt_of_two_le hn (by decide : 243 < 256)
  exact (not_le_of_gt hlt) hle

theorem floorPower_one : floorPower 1 = 1 := by
  native_decide

theorem floorPower_thirteen_step : floorPower 13 = 46 := by
  native_decide

/-- Packet seed `13` reaches `1` in four steps. Not a map theorem. -/
theorem floorPower_thirteen_reaches_one :
    (floorPower^[4] 13) = 1 := by
  native_decide

/-!
Local branch equality, composite equality, and square rigidity.
Not a termination theorem, not an equality-word classifier, and not a
`PowerBound` certificate datatype. `PowerBound` remains the weak bound.
-/

/-- Even branch: `T(n)^2 = n` iff `n` is a perfect square. -/
theorem floorPower_even_sq_eq_iff_square {n : ℕ} (heven : n % 2 = 0) :
    floorPower n ^ 2 = n ↔ n.sqrt ^ 2 = n := by
  have step : floorPower n = n.sqrt := by simp [floorPower, heven]
  rw [step]

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
      exact hn (pow_eq_zero this)
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
  have hodd0 : n % 2 ≠ 0 := by omega
  have step : floorPower n = (n * n * n).sqrt := by simp [floorPower, hodd0]
  have hcube : n * n * n = n ^ 3 := by ring
  rw [step, hcube]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have h3 : 3 ^ (o + 1) = 3 * 3 ^ o := by rw [pow_succ, mul_comm]
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

end Problems.Engine
