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

end Problems.Engine
