import Mathlib.Algebra.Polynomial.Basic
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Algebra.Polynomial.Roots
import BTCalculus.Derivative

noncomputable section

namespace BTCalculus

open Polynomial

def powShift (a : ℤ) : ℕ → ℤ[X]
  | 0 => 0
  | n + 1 => C a * powShift a n + C (a ^ n) * X + 3 * X * powShift a n

theorem powShift_spec (a : ℤ) :
    ∀ n : ℕ, (C a + 3 * (X : ℤ[X])) ^ n = C (a ^ n) + 3 * powShift a n
  | 0 => by
    simp [powShift]
  | n + 1 => by
    rw [pow_succ, powShift_spec a n, powShift]
    simp [map_mul]
    ring

theorem powShift_eval (a x : ℤ) (n : ℕ) :
    (a + 3 * x) ^ n = a ^ n + 3 * eval x (powShift a n) := by
  have h := congrArg (eval x) (powShift_spec a n)
  simpa [eval_add, eval_C, eval_mul, eval_X, eval_pow] using h

def sectionDeriv (a : ℤ) (f : ℤ[X]) : ℤ[X] :=
  C (DZ (eval a f)) + ∑ n ∈ f.support, C (f.coeff n) * powShift a n

theorem eval_sectionDeriv (f : ℤ[X]) (a x : ℤ) :
    eval x (sectionDeriv a f) =
      DZ (eval a f) + ∑ n ∈ f.support, f.coeff n * eval x (powShift a n) := by
  simp [sectionDeriv, eval_add, eval_C, eval_finset_sum, eval_mul]

theorem section_reconstruction_eval (f : ℤ[X]) (a x : ℤ) :
    eval (a + 3 * x) f =
      lsdZ (eval a f) + 3 * eval x (sectionDeriv a f) := by
  have hpow := powShift_eval a x
  have lhs :
      eval (a + 3 * x) f = ∑ n ∈ f.support, f.coeff n * (a + 3 * x) ^ n := by
    simp [eval_eq_sum, Polynomial.sum]
  have ha : eval a f = ∑ n ∈ f.support, f.coeff n * a ^ n := by
    simp [eval_eq_sum, Polynomial.sum]
  have hterms :
      ∑ n ∈ f.support, f.coeff n * (a + 3 * x) ^ n =
        ∑ n ∈ f.support, (f.coeff n * a ^ n + 3 * f.coeff n * eval x (powShift a n)) := by
    refine Finset.sum_congr rfl ?_
    intro n _hn
    rw [hpow n]
    ring
  have hsplit :
      ∑ n ∈ f.support, f.coeff n * (a + 3 * x) ^ n =
        (∑ n ∈ f.support, f.coeff n * a ^ n) +
          3 * ∑ n ∈ f.support, f.coeff n * eval x (powShift a n) := by
    rw [hterms, Finset.sum_add_distrib, Finset.mul_sum]
    simp [mul_left_comm, mul_assoc, mul_comm]
  have hde : eval a f = lsdZ (eval a f) + 3 * DZ (eval a f) := decomp (eval a f)
  have hsd := eval_sectionDeriv f a x
  calc
    eval (a + 3 * x) f
        = ∑ n ∈ f.support, f.coeff n * (a + 3 * x) ^ n := lhs
    _ = (∑ n ∈ f.support, f.coeff n * a ^ n) +
          3 * ∑ n ∈ f.support, f.coeff n * eval x (powShift a n) := hsplit
    _ = eval a f + 3 * ∑ n ∈ f.support, f.coeff n * eval x (powShift a n) := by
        rw [ha]
    _ = lsdZ (eval a f) + 3 * DZ (eval a f) +
          3 * ∑ n ∈ f.support, f.coeff n * eval x (powShift a n) := by
        conv_lhs => rw [hde]
    _ = lsdZ (eval a f) + 3 * eval x (sectionDeriv a f) := by
        conv_rhs => rw [hsd]
        ring

/-- Polynomial (not merely pointwise) reconstruction. -/
theorem section_reconstruction (f : ℤ[X]) (a : ℤ) :
    f.comp (C a + 3 * X) = C (lsdZ (eval a f)) + 3 * sectionDeriv a f := by
  refine Polynomial.funext (fun x => ?_)
  have h := section_reconstruction_eval f a x
  simpa [eval_comp, eval_add, eval_C, eval_mul, eval_X] using h

end BTCalculus
