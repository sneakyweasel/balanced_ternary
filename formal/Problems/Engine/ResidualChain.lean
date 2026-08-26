import Problems.Engine.OddOddFrontier

namespace Problems.Engine

/-!
# Residual steps and certificate propagation

A residual step is one realized `O^a E^b` excursion with `b ≥ 1`.
`ReachesOne` and `Capture` propagate backward along a residual word.
A later `ReturnBelow` the original start is `FiniteProgress` there.
A `Descent` at the residual that stays `≥` the original start is not
`Descent` at the start. Persistent odd-to-odd residuals remain on the
same unresolved frontier. This is not a halt theorem and not a claim
that `FiniteProgress` at the residual implies `FiniteProgress` at the
start.
-/

/-- One realized excursion through a later even residual. Not an
infinite transition system. -/
def ResidualStep (x y : ℕ) : Prop :=
  ∃ a b, 1 ≤ b ∧ follows x (oddEvenBlock a b) ∧
    image x (oddEvenBlock a b) = y

/-- Another odd-to-odd frontier state, strictly above the current one.
Recursion, not progress. -/
def PersistentOddResidual (x y : ℕ) : Prop :=
  ResidualStep x y ∧ x < y ∧ y % 2 = 1 ∧ floorPower y % 2 = 1

theorem residualStep_word {x y : ℕ} (h : ResidualStep x y) :
    ∃ w, follows x w ∧ image x w = y := by
  obtain ⟨_a, _b, _hb, hw, himg⟩ := h
  exact ⟨_, hw, himg⟩

/-- Any certified residual closes `ReachesOne` at the source. Stronger
than requiring `Capture` of the residual word itself. -/
theorem reachesOne_of_residualStep {x y : ℕ}
    (h : ResidualStep x y) (hy : ReachesOne y) : ReachesOne x := by
  obtain ⟨w, _hw, himg⟩ := residualStep_word h
  rw [← himg] at hy
  exact reachesOne_of_image hy

theorem finiteProgress_of_residual_capture {x y : ℕ} {v : List Branch}
    (h : ResidualStep x y) (hc : Capture y v) : FiniteProgress x := by
  obtain ⟨w, hw, himg⟩ := residualStep_word h
  rw [← himg] at hc
  exact finiteProgress_of_capture (capture_of_suffix hw hc)

theorem finiteProgress_of_residual_returnBelow {x y : ℕ}
    (h : ResidualStep x y) (hr : ReturnBelow x y) : FiniteProgress x := by
  obtain ⟨w, hw, himg⟩ := residualStep_word h
  rw [← himg] at hr
  exact finiteProgress_of_returnBelow hw hr

/-- Concatenating a residual descent that stays at or above `x` is not
`Descent` at `x`. Distinguishes `T_v(y) < y` from `T_v(y) < x`. -/
theorem residual_descent_not_below {x y : ℕ} {u v : List Branch}
    (_hu : follows x u) (hy : image x u = y)
    (_hd : Descent y v) (hge : x ≤ image y v) :
    ¬Descent x (u ++ v) := by
  intro hD
  have himg : image x (u ++ v) = image y v := by
    rw [image_append, hy]
  have : image y v < x := by
    simpa [himg] using hD.2
  exact Nat.not_lt.mpr hge this

theorem persistent_odd_odd {x y : ℕ} (h : PersistentOddResidual x y) :
    y % 2 = 1 ∧ floorPower y % 2 = 1 :=
  ⟨h.2.2.1, h.2.2.2⟩

theorem persistent_residual_gt {x y : ℕ} (h : PersistentOddResidual x y) :
    x < y :=
  h.2.1

/-- The same frontier analysis applies to a persistent residual.
This is recursion, not a progress certificate. -/
theorem persistent_residual_preserves_frontier {x y : ℕ}
    (h : PersistentOddResidual x y) :
    y % 2 = 1 ∧ floorPower y % 2 = 1 :=
  persistent_odd_odd h

theorem minimal_residual_image_ge {n y : ℕ}
    (h : MinimalNonTerm n) (hs : ResidualStep n y) : n ≤ y := by
  obtain ⟨w, hw, himg⟩ := residualStep_word hs
  simpa [himg] using minimal_nonterm_image_ge h hw

/-- Combined residual scale on a CE: odd exits stay `≥ n`, even exits
stay `≥ n^2`. -/
theorem minimal_residual_scale {n y : ℕ}
    (h : MinimalNonTerm n) (hs : ResidualStep n y) :
    n ≤ y ∧ (y % 2 = 0 → n ^ 2 ≤ y) := by
  refine ⟨minimal_residual_image_ge h hs, ?_⟩
  intro hy
  obtain ⟨w, hw, himg⟩ := residualStep_word hs
  rw [← himg] at hy
  have := minimal_nonterm_first_even_ge_sq h hw hy
  rwa [himg] at this

/-- Finite residual chains. Not an infinite-path type. -/
inductive ResidualChain : ℕ → ℕ → Prop where
  | refl (x : ℕ) : ResidualChain x x
  | step {x y z : ℕ} : ResidualStep x y → ResidualChain y z → ResidualChain x z

theorem residualChain_word {x y : ℕ} (h : ResidualChain x y) :
    ∃ w, follows x w ∧ image x w = y := by
  induction h with
  | refl x => exact ⟨[], trivial, rfl⟩
  | step hs _ ih =>
      obtain ⟨u, hu, hul⟩ := residualStep_word hs
      obtain ⟨v, hv, hvl⟩ := ih
      refine ⟨u ++ v, follows_append hu (by simpa [hul] using hv), ?_⟩
      rw [image_append, hul, hvl]

theorem reachesOne_of_residualChain {x y : ℕ}
    (h : ResidualChain x y) (hy : ReachesOne y) : ReachesOne x := by
  obtain ⟨w, _hw, himg⟩ := residualChain_word h
  rw [← himg] at hy
  exact reachesOne_of_image hy

theorem finiteProgress_of_residualChain_returnBelow {x y : ℕ}
    (h : ResidualChain x y) (hr : ReturnBelow x y) : FiniteProgress x := by
  obtain ⟨w, hw, himg⟩ := residualChain_word h
  rw [← himg] at hr
  exact finiteProgress_of_returnBelow hw hr

theorem finiteProgress_of_residualChain_capture {x y : ℕ} {v : List Branch}
    (h : ResidualChain x y) (hc : Capture y v) : FiniteProgress x := by
  obtain ⟨w, hw, himg⟩ := residualChain_word h
  rw [← himg] at hc
  exact finiteProgress_of_capture (capture_of_suffix hw hc)

end Problems.Engine
