import Problems.BalancedTernary.SignedDigitConstrainedControls

namespace Problems.BalancedTernary

open BTCalculus

/-!
Traces of length at most ``L`` agree whenever ``3^L ∣ s-t``. Combined with
``any_word_separation``, a remaining-horizon ``L`` controller makes
``(s,q_L)`` and ``(t,q_L)`` equivalent iff that congruence holds, for
gains not divisible by 3. This file does not reopen the phase law.
-/

theorem signedTrace_take (gain s : ℤ) :
    ∀ w n, (signedTrace gain s w).take n = signedTrace gain s (w.take n)
  | [], n => by simp [signedTrace]
  | u :: rest, 0 => by simp [signedTrace]
  | u :: rest, n + 1 => by
    simp [signedTrace_cons, List.take_cons]
    exact signedTrace_take gain (signedNext gain s u) rest n

theorem pow_three_succ (L : ℕ) :
    (3 : ℤ) ^ (L + 1) = (3 : ℤ) ^ L * 3 :=
  pow_succ _ _

theorem truncated_3adic_agree {gain s t : ℤ} {L : ℕ} {w : List ℤ}
    (hdvd : (3 : ℤ) ^ L ∣ s - t) (hw : w.length ≤ L) :
    signedTrace gain s w = signedTrace gain t w := by
  induction w generalizing s t L with
  | nil =>
    simp [signedTrace]
  | cons u rest ih =>
    have hpos : 1 ≤ L := by
      have : rest.length + 1 ≤ L := by simpa [List.length_cons] using hw
      omega
    have hdecomp : (3 : ℤ) ^ L = (3 : ℤ) ^ (L - 1) * 3 := by
      calc (3 : ℤ) ^ L
          = (3 : ℤ) ^ (L - 1 + 1) := by rw [Nat.sub_add_cancel hpos]
        _ = (3 : ℤ) ^ (L - 1) * 3 := pow_three_succ (L - 1)
    have hdvd3 : (3 : ℤ) ∣ s - t := by
      have hself : (3 : ℤ) ∣ (3 : ℤ) ^ L := by
        rw [hdecomp]
        exact dvd_mul_left _ _
      exact dvd_trans hself hdvd
    have hc : s ≡ t [ZMOD 3] := (cong_iff_dvd_sub s t).mpr hdvd3
    have hout : signedOut s u = signedOut t u :=
      (signedOut_eq_iff_cong s t u).mpr hc
    obtain ⟨k, hk⟩ := hdvd
    have hne3 : (3 : ℤ) ≠ 0 := by decide
    have hdiv : (s - t) / 3 = (3 : ℤ) ^ (L - 1) * k := by
      have hre : (3 : ℤ) ^ L * k = (3 : ℤ) ^ (L - 1) * k * 3 := by
        rw [hdecomp]
        ring
      rw [hk, hre, Int.mul_ediv_cancel _ hne3]
    have hsucc : (3 : ℤ) ^ (L - 1) ∣ signedNext gain s u - signedNext gain t u := by
      have hst' : signedNext gain s u - signedNext gain t u =
          gain * ((s - t) / 3) := by
        linarith [signedNext_diff_of_cong hc gain u]
      have hpart : (3 : ℤ) ^ (L - 1) ∣ (3 : ℤ) ^ (L - 1) * k :=
        dvd_mul_right _ _
      rw [hst', hdiv]
      exact dvd_mul_of_dvd_right hpart gain
    have hrest : rest.length ≤ L - 1 := by
      have : rest.length + 1 ≤ L := by simpa [List.length_cons] using hw
      omega
    rw [signedTrace_cons, signedTrace_cons, hout]
    exact congrArg (List.cons (signedOut t u)) (ih hsucc hrest)

theorem truncated_3adic_equiv {gain s t : ℤ} {L : ℕ} {w : List ℤ}
    (hdvd : (3 : ℤ) ^ L ∣ s - t) (hw : w.length ≤ L) :
    signedTrace gain s w = signedTrace gain t w :=
  truncated_3adic_agree hdvd hw

theorem short_horizon_equiv {gain s t : ℤ} {L : ℕ} {w : List ℤ}
    (hdvd : (3 : ℤ) ^ L ∣ s - t) (hw : w.length ≤ L) :
    signedTrace gain s w = signedTrace gain t w :=
  truncated_3adic_equiv hdvd hw

theorem short_horizon_separation {gain s t : ℤ} {w : List ℤ}
    (hgain : ¬ (3 : ℤ) ∣ gain) (hne : s ≠ t)
    (hw : intVal3 (s - t) + 1 ≤ w.length) :
    signedTrace gain s w ≠ signedTrace gain t w := by
  set n := intVal3 (s - t) + 1
  have htake : (w.take n).length = n := by
    simp [List.length_take]
    omega
  have hsep := any_word_separation (w := w.take n) hgain hne htake
  intro heq
  have hpref :
      (signedTrace gain s w).take n = (signedTrace gain t w).take n := by
    simp [heq]
  exact hsep ((signedTrace_take gain s w n).symm.trans
    (hpref.trans (signedTrace_take gain t w n)))

theorem control_language_separation {gain s t : ℤ} {w : List ℤ}
    (hgain : ¬ (3 : ℤ) ∣ gain) (hne : s ≠ t)
    (hw : intVal3 (s - t) + 1 ≤ w.length) :
    signedTrace gain s w ≠ signedTrace gain t w :=
  short_horizon_separation hgain hne hw

theorem lambda3_short_horizon_symmetry (s k : ℤ) (w : List ℤ) :
    signedTrace 3 (s + 3 * k) w = signedTrace 3 s w :=
  lambda3_trace_translate s k w

end Problems.BalancedTernary
