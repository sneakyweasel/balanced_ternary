/-
Unread-tail energy of Γ_NP and the constructional step identity.

    E_i(s) = s₁ q_{i-2} + s₂ q_{i-1} + s₃ q_i

with `q_j = 0` for underflow, and

    E_{i-1}(T_w s) = E_i(s) - w q_{i-1}.

This is the covariance of the place-value recurrence with the residual
matrix `A`, not a bound on the live set `L₀`.
-/

import Problems.Ostrowski.NP.Recurrence
import Problems.Ostrowski.NP.Residual

namespace Ostrowski.NP

/-- `q_{n-k}` with value `0` when `k > n`. -/
def qShift (n k : ℕ) : ℤ :=
  if k ≤ n then q (n - k) else 0

theorem qShift_zero (n : ℕ) : qShift n 0 = q n := by
  simp [qShift]

theorem qShift_of_le {n k : ℕ} (h : k ≤ n) : qShift n k = q (n - k) := by
  simp [qShift, h]

theorem qShift_of_not_le {n k : ℕ} (h : ¬ k ≤ n) : qShift n k = 0 := by
  simp [qShift, h]

theorem qShift_one_of_pos {i : ℕ} (hi : 0 < i) : qShift i 1 = q (i - 1) := by
  have : 1 ≤ i := Nat.succ_le_of_lt hi
  simp [qShift, this]

/-- `E_i(s) = s₁ q_{i-2} + s₂ q_{i-1} + s₃ q_i`. -/
def energy (i : ℕ) : State → ℤ
  | (s1, s2, s3) => qShift i 2 * s1 + qShift i 1 * s2 + q i * s3

theorem energy_zero (s1 s2 s3 : ℤ) : energy 0 (s1, s2, s3) = s3 := by
  simp [energy, qShift, q]

/-- Coefficient row `u_i = (q_{i-2}, q_{i-1}, q_i)`. -/
def adjointU (i : ℕ) : ℤ × ℤ × ℤ :=
  (qShift i 2, qShift i 1, q i)

/-- Left action of
`A = [[0, 0, 3], [1, 0, 1], [0, 1, 2]]` on a row vector. -/
def mulRowA (u : ℤ × ℤ × ℤ) : ℤ × ℤ × ℤ :=
  (u.2.1, u.2.2, 3 * u.1 + u.2.1 + 2 * u.2.2)

theorem energy_eq_dot (i : ℕ) (s1 s2 s3 : ℤ) :
    energy i (s1, s2, s3) =
      (adjointU i).1 * s1 + (adjointU i).2.1 * s2 + (adjointU i).2.2 * s3 :=
  rfl

private theorem adjoint_covariance_succ_succ (n : ℕ) :
    mulRowA (adjointU (n + 2)) = adjointU (n + 3) := by
  have h2 : 2 ≤ n + 2 := Nat.le_add_left 2 n
  have h2' : 2 ≤ n + 3 := Nat.le_add_left 2 (n + 1)
  have h1 : 1 ≤ n + 2 := Nat.le_add_left 1 (n + 1)
  have h1' : 1 ≤ n + 3 := Nat.le_add_left 1 (n + 2)
  simp [mulRowA, adjointU, qShift, h2, h2', h1, h1', q_rec n]
  ring

/-- `u_{i-1} A = u_i` for `i ≥ 1`. -/
theorem adjoint_covariance (i : ℕ) (hi : 0 < i) :
    mulRowA (adjointU (i - 1)) = adjointU i := by
  match i with
  | 0 => cases hi
  | 1 => simp [mulRowA, adjointU, qShift, q]
  | 2 => simp [mulRowA, adjointU, qShift, q]
  | n + 3 =>
    simpa using adjoint_covariance_succ_succ n

private theorem adjoint_components (i : ℕ) (hi : 0 < i) :
    qShift (i - 1) 1 = qShift i 2 ∧
      q (i - 1) = qShift i 1 ∧
        3 * qShift (i - 1) 2 + qShift (i - 1) 1 + 2 * q (i - 1) = q i := by
  have h := adjoint_covariance i hi
  simp [mulRowA, adjointU] at h
  exact h

/-- Constructional identity: `E_{i-1}(T_w s) = E_i(s) - w q_{i-1}`. -/
theorem energy_step (i : ℕ) (hi : 0 < i) (w s1 s2 s3 : ℤ) :
    energy (i - 1) (step w (s1, s2, s3)) =
      energy i (s1, s2, s3) - w * q (i - 1) := by
  obtain ⟨h1, h2, h3⟩ := adjoint_components i hi
  simp only [energy, step]
  rw [← h1, ← h2, ← h3]
  ring

end Ostrowski.NP
