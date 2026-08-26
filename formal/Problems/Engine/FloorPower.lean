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
  have hodd0 : x % 2 ≠ 0 := by omega
  have hcube : x * x * x = x ^ 3 := by ring
  simp [localDefectOdd, floorPower, hodd0, hcube]

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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  rw [h2]
  exact lt_of_le_of_lt (pow_sq_le hsq) h

theorem strict_power_bound_append_odd {m n k o : ℕ}
    (h : StrictPowerBound m n k o) (hodd : m % 2 = 1) :
    StrictPowerBound (floorPower m) n (k + 1) (o + 1) := by
  have hsq : floorPower m ^ 2 ≤ m ^ 3 := floorPower_odd_sq_le_cube hodd
  unfold StrictPowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  rw [h2, Nat.pow_mul, ← h]
  exact Nat.pow_lt_pow_left hδ (pow_ne_zero_two_pow k)

theorem strict_power_bound_of_odd_defect {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) :
    StrictPowerBound (floorPower m) n (k + 1) (o + 1) := by
  unfold StrictPowerBound PowerBoundEq at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have hle : floorPower m ^ 2 ≤ m := le_of_lt hδ
  have hgap : m - floorPower m ^ 2 ≤ m ^ (2 ^ k) - (floorPower m ^ 2) ^ (2 ^ k) :=
    pow_sub_pow_ge_sub hle (Nat.one_le_pow _ _ (by decide : 0 < 2))
  unfold PowerBoundEq at h
  simpa [localDefectEven, h, h2, Nat.pow_mul] using hgap

theorem odd_defect_gap_ge_local {m n k o : ℕ}
    (h : PowerBoundEq m n k o) (_hodd : m % 2 = 1)
    (hδ : floorPower m ^ 2 < m ^ 3) :
    localDefectOdd m ≤ n ^ (3 ^ (o + 1)) - floorPower m ^ (2 ^ (k + 1)) := by
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have h3 : 3 ^ (o + 1) = 3 * 3 ^ o := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have hle : floorPower m ^ (2 ^ (k + 1)) ≤ m ^ (2 ^ k) := by
    rw [h2]
    exact pow_sq_le (floorPower_even_sq_le heven)
  exact Nat.sub_le_sub_left hle _

theorem power_deficit_append_odd {m n k o : ℕ}
    (h : PowerBound m n k o) (hodd : m % 2 = 1) :
    powerDeficit m n k o ≤ powerDeficit (floorPower m) n (k + 1) (o + 1) := by
  unfold powerDeficit PowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  cases le_or_lt d 1 with
  | inl hd1 =>
      have hd : d = 1 := le_antisymm hd1 hdpos
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
  | inr hlt =>
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
  have hT : floorPower m ^ (2 ^ (k + 1)) = m ^ (2 ^ k) := by
    rw [h2, Nat.pow_mul, htight]
  rw [hT]

theorem power_deficit_append_even_of_defect {m n k o : ℕ}
    (h : PowerBound m n k o) (_heven : m % 2 = 0)
    (hδ : floorPower m ^ 2 < m) :
    powerDeficit m n k o < powerDeficit (floorPower m) n (k + 1) o := by
  unfold powerDeficit PowerBound at *
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
  have h2 : 2 ^ (k + 1) = 2 * 2 ^ k := by rw [pow_succ, mul_comm]
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
Inverse-floor form of the odd Juggler step. This is the integer
interval for `T(n) = M`, not a termination theorem and not a
perfect-power height.
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

theorem floorPower_odd_eq_iff_cube_interval {n M : ℕ} (hodd : n % 2 = 1) :
    floorPower n = M ↔ M ^ 2 ≤ n ^ 3 ∧ n ^ 3 < (M + 1) ^ 2 := by
  have hodd0 : n % 2 ≠ 0 := by omega
  have hcube : n * n * n = n ^ 3 := by ring
  have step : floorPower n = (n ^ 3).sqrt := by
    simp [floorPower, hodd0, hcube]
  rw [step]
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

end Problems.Engine
