import Mathlib.Algebra.Order.BigOperators.GroupWithZero.Finset
import Mathlib.Tactic.Positivity
import Mathlib.Topology.MetricSpace.Lipschitz

/-!
# Information-field dynamics

An abstract dynamical system on an *information space*. The objects are

* information states `x : I`;
* perturbations `T : I → I` of the information field;
* physical (or computational) states `M`, reached through an
  interface `Φ : I → M`.

When `I` and `M` carry metrics the interesting quantity is the
*leverage* of a perturbation: the size of the downstream change
`dist (Φ x) (Φ (T x))` per unit of informational change
`dist x (T x)`. Everything below is a KNOWN consequence of the
definitions. The statements are:

* `leverage_mul_size` — effect = leverage × size, in every case;
* `leverage_le_of_lipschitz` — a `K`-Lipschitz interface has leverage
  at most `K` everywhere;
* `amplifies_iff_not_lipschitz` — the interface has unbounded
  leverage exactly when it is not Lipschitz for any constant;
* `step_amplifies` — a threshold interface `ℝ → ℝ` is a witness: the
  leverage of `x ↦ x + ε` at `0` is `1 / ε`;
* `leverage_compose_le` — the chain rule for composing perturbations
  (the effect of `T₁ ∘ T₂` is at most the sum of the two weighted
  leverages);
* `leverage_interface_comp` — the exact multiplicative chain rule for
  composing interfaces `Ψ ∘ Θ`;
* `dist_interface_trajectory_le_leverage` — along a trajectory
  `x_{n+1} = T_n x_n` the displacement of the physical state is at most
  the sum of the step-wise weighted leverages;
* `gainRatio_compose`, `gainRatio_trajectory` — the computational
  gain ratio `Λ(T; x) = C x / C (T x)` is multiplicative under
  composition and telescopes along a trajectory;
* `exists_optimal_perturbation` — a finite menu of perturbations has a
  most efficient member;
* `leverageBoundedOn_iff_lipschitzOnWith`, `originalLocus_inter_subset` —
  the landscape dichotomy: on a *normal* region the interface is
  Lipschitz and leverage is bounded, so a state of the *original* locus
  (leverage above the bound) inside a normal region can only be
  exploited by a perturbation that leaves the region;
* `pow_le_gainRatio_trajectory` — compounding: `n` steps of gain at
  least `g` give total gain at least `g ^ n`;
* `prod_le_prod_exchange`, `exists_optimal_menu` — mining order:
  swapping a candidate for one of larger gain never lowers the total
  gain, and among all `k`-element menus a best one exists.

The information space itself is left abstract; a *complexity* is any
real-valued function on it (see `informationCost`). Nothing here is
specific to balanced ternary or to the Juggler map.
-/

namespace Problems.Engine.InformationField

universe u v w

/-- A perturbation of the informational field. -/
abbrev Perturbation (I : Type u) := I → I

/-- A map through which information affects physical or computational
reality. -/
abbrev Interface (I : Type u) (M : Type v) := I → M

variable {I : Type u} {M : Type v}

/-- Applying an informational perturbation. -/
def perturb (T : Perturbation I) (x : I) : I :=
  T x

/-- Composition of perturbations: `compose T₁ T₂` applies `T₂` first,
then `T₁`. -/
def compose (T₁ T₂ : Perturbation I) : Perturbation I :=
  T₁ ∘ T₂

@[simp] theorem perturb_compose (T₁ T₂ : Perturbation I) (x : I) :
    perturb (compose T₁ T₂) x = perturb T₁ (perturb T₂ x) :=
  rfl

@[simp] theorem compose_apply (T₁ T₂ : Perturbation I) (x : I) :
    compose T₁ T₂ x = T₁ (T₂ x) :=
  rfl

theorem compose_assoc (T₁ T₂ T₃ : Perturbation I) :
    compose (compose T₁ T₂) T₃ = compose T₁ (compose T₂ T₃) :=
  rfl

@[simp] theorem compose_id_left (T : Perturbation I) : compose id T = T :=
  rfl

@[simp] theorem compose_id_right (T : Perturbation I) : compose T id = T :=
  rfl

/-- The evolution `x₀ → T 0 x₀ → T 1 (T 0 x₀) → ⋯` of the information
field under a sequence of perturbations. -/
def trajectory (T : ℕ → Perturbation I) (x₀ : I) : ℕ → I
  | 0 => x₀
  | n + 1 => T n (trajectory T x₀ n)

@[simp] theorem trajectory_zero (T : ℕ → Perturbation I) (x₀ : I) :
    trajectory T x₀ 0 = x₀ :=
  rfl

@[simp] theorem trajectory_succ (T : ℕ → Perturbation I) (x₀ : I) (n : ℕ) :
    trajectory T x₀ (n + 1) = T n (trajectory T x₀ n) :=
  rfl

/-! ## Size, effect, leverage -/

section Metric

variable [MetricSpace I] [PseudoMetricSpace M]

/-- Pointwise magnitude of an informational perturbation. -/
def perturbationSize (T : Perturbation I) (x : I) : ℝ :=
  dist x (T x)

/-- Downstream (physical or computational) effect of a perturbation
seen through the interface `Φ`. -/
def physicalEffect (Φ : Interface I M) (T : Perturbation I) (x : I) : ℝ :=
  dist (Φ x) (Φ (T x))

/-- Local informational leverage: downstream effect per unit of
informational change, with the convention `0` for a perturbation that
fixes `x`. -/
noncomputable def leverage (Φ : Interface I M) (T : Perturbation I) (x : I) : ℝ :=
  if dist x (T x) = 0 then 0 else physicalEffect Φ T x / dist x (T x)

variable (Φ : Interface I M) (T T₁ T₂ : Perturbation I) (x : I)

theorem perturbationSize_nonneg : 0 ≤ perturbationSize T x :=
  dist_nonneg

omit [MetricSpace I] in
theorem physicalEffect_nonneg : 0 ≤ physicalEffect Φ T x :=
  dist_nonneg

theorem leverage_nonneg : 0 ≤ leverage Φ T x := by
  unfold leverage
  split_ifs with h
  · exact le_rfl
  · exact div_nonneg dist_nonneg dist_nonneg

theorem perturbationSize_eq_zero_iff : perturbationSize T x = 0 ↔ T x = x := by
  unfold perturbationSize
  rw [dist_eq_zero, eq_comm]

@[simp] theorem perturbationSize_id : perturbationSize (id : Perturbation I) x = 0 :=
  dist_self x

omit [MetricSpace I] in
@[simp] theorem physicalEffect_id : physicalEffect Φ id x = 0 :=
  dist_self (Φ x)

@[simp] theorem leverage_id : leverage Φ id x = 0 := by
  simp [leverage]

theorem leverage_of_ne (h : dist x (T x) ≠ 0) :
    leverage Φ T x = physicalEffect Φ T x / dist x (T x) := by
  unfold leverage
  rw [if_neg h]

/-- The defining identity: effect equals leverage times size, including
the degenerate case of a perturbation that fixes `x`. -/
theorem leverage_mul_size :
    leverage Φ T x * perturbationSize T x = physicalEffect Φ T x := by
  unfold leverage perturbationSize physicalEffect
  split_ifs with h
  · have hx : x = T x := dist_eq_zero.mp h
    rw [← hx, dist_self, dist_self, mul_zero]
  · rw [div_mul_eq_mul_div, mul_div_assoc, div_self h, mul_one]

/-- A `K`-Lipschitz interface has leverage at most `K` everywhere. -/
theorem leverage_le_of_lipschitz {K : NNReal} (hΦ : LipschitzWith K Φ) :
    leverage Φ T x ≤ K := by
  unfold leverage physicalEffect
  split_ifs with h
  · exact K.coe_nonneg
  · rw [div_le_iff₀ (lt_of_le_of_ne dist_nonneg (Ne.symm h))]
    exact hΦ.dist_le_mul x (T x)

/-! ## Amplification -/

/-- An interface *amplifies* when its leverage is unbounded: an
arbitrarily small informational change can produce a downstream change
of any prescribed ratio. -/
def Amplifies (Φ : Interface I M) : Prop :=
  ∀ K : ℝ, ∃ (T : Perturbation I) (x : I), K < leverage Φ T x

theorem not_amplifies_of_lipschitz {K : NNReal} (hΦ : LipschitzWith K Φ) :
    ¬ Amplifies Φ := by
  intro h
  obtain ⟨T, x, hx⟩ := h K
  exact absurd (leverage_le_of_lipschitz Φ T x hΦ) (not_le.mpr hx)

/-- Leverage is unbounded exactly when the interface is not Lipschitz
for any constant. The perturbation `fun _ => y` at `x` realizes every
Lipschitz quotient `dist (Φ x) (Φ y) / dist x y`. -/
theorem amplifies_iff_not_lipschitz :
    Amplifies Φ ↔ ¬ ∃ K : NNReal, LipschitzWith K Φ := by
  constructor
  · rintro h ⟨K, hK⟩
    exact not_amplifies_of_lipschitz Φ hK h
  · intro h K
    by_contra hK
    simp only [not_exists, not_lt] at hK
    apply h
    refine ⟨Real.toNNReal K, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
    by_cases hxy : dist x y = 0
    · rw [dist_eq_zero] at hxy
      subst hxy
      simp
    · have hpos : 0 < dist x y := lt_of_le_of_ne dist_nonneg (Ne.symm hxy)
      have hL := hK (fun _ => y) x
      simp only [leverage, physicalEffect, hxy, ↓reduceIte] at hL
      rw [div_le_iff₀ hpos] at hL
      calc dist (Φ x) (Φ y) ≤ K * dist x y := hL
        _ ≤ (Real.toNNReal K : ℝ) * dist x y :=
          mul_le_mul_of_nonneg_right (Real.le_coe_toNNReal K) dist_nonneg

/-! ## Chain rules -/

omit [MetricSpace I] in
/-- Triangle inequality for the effect of a composite perturbation. -/
theorem physicalEffect_compose_le :
    physicalEffect Φ (compose T₁ T₂) x ≤
      physicalEffect Φ T₂ x + physicalEffect Φ T₁ (T₂ x) :=
  dist_triangle _ _ _

theorem perturbationSize_compose_le :
    perturbationSize (compose T₁ T₂) x ≤
      perturbationSize T₂ x + perturbationSize T₁ (T₂ x) :=
  dist_triangle _ _ _

/-- Chain rule for leverage under composition of perturbations: the
weighted leverage of `T₁ ∘ T₂` is at most the sum of the weighted
leverages of the two steps. -/
theorem leverage_compose_le :
    leverage Φ (compose T₁ T₂) x * perturbationSize (compose T₁ T₂) x ≤
      leverage Φ T₂ x * perturbationSize T₂ x +
        leverage Φ T₁ (T₂ x) * perturbationSize T₁ (T₂ x) := by
  rw [leverage_mul_size, leverage_mul_size, leverage_mul_size]
  exact physicalEffect_compose_le Φ T₁ T₂ x

/-- Exact chain rule for composing interfaces. If `Θ : I → J` and
`Ψ : J → M`, and `T'` is any perturbation of `J` that moves `Θ x` to
`Θ (T x)`, then the leverage of `Ψ ∘ Θ` factors as the leverage of `Ψ`
at `Θ x` times the leverage of `Θ` at `x`. -/
theorem leverage_interface_comp {J : Type w} [MetricSpace J]
    (Θ : Interface I J) (Ψ : Interface J M) (T' : Perturbation J)
    (hT' : T' (Θ x) = Θ (T x)) :
    leverage (Ψ ∘ Θ) T x = leverage Ψ T' (Θ x) * leverage Θ T x := by
  by_cases h₁ : dist x (T x) = 0
  · simp [leverage, h₁]
  · by_cases h₂ : dist (Θ x) (Θ (T x)) = 0
    · have hΘ : Θ x = Θ (T x) := dist_eq_zero.mp h₂
      have h₂' : dist (Θ x) (T' (Θ x)) = 0 := by rw [hT']; exact h₂
      unfold leverage
      rw [if_neg h₁, if_pos h₂', zero_mul, div_eq_zero_iff]
      left
      show dist (Ψ (Θ x)) (Ψ (Θ (T x))) = 0
      rw [← hΘ, dist_self]
    · unfold leverage physicalEffect
      simp only [h₁, h₂, ↓reduceIte, Function.comp_apply, hT']
      rw [div_mul_div_comm, mul_comm (dist (Ψ (Θ x)) (Ψ (Θ (T x)))),
        mul_div_mul_left _ _ h₂]

/-! ## Trajectories -/

variable (Tseq : ℕ → Perturbation I) (x₀ : I) (n : ℕ)

/-- The information field moves at most the sum of the step sizes. -/
theorem dist_trajectory_le :
    dist x₀ (trajectory Tseq x₀ n) ≤
      ∑ k ∈ Finset.range n, perturbationSize (Tseq k) (trajectory Tseq x₀ k) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ]
    calc dist x₀ (trajectory Tseq x₀ (n + 1))
        ≤ dist x₀ (trajectory Tseq x₀ n) +
            dist (trajectory Tseq x₀ n) (trajectory Tseq x₀ (n + 1)) :=
          dist_triangle _ _ _
      _ ≤ _ := add_le_add ih le_rfl

omit [MetricSpace I] in
/-- The physical state moves at most the sum of the step effects. -/
theorem dist_interface_trajectory_le :
    dist (Φ x₀) (Φ (trajectory Tseq x₀ n)) ≤
      ∑ k ∈ Finset.range n, physicalEffect Φ (Tseq k) (trajectory Tseq x₀ k) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ]
    calc dist (Φ x₀) (Φ (trajectory Tseq x₀ (n + 1)))
        ≤ dist (Φ x₀) (Φ (trajectory Tseq x₀ n)) +
            dist (Φ (trajectory Tseq x₀ n)) (Φ (trajectory Tseq x₀ (n + 1))) :=
          dist_triangle _ _ _
      _ ≤ _ := add_le_add ih le_rfl

/-- Cumulative chain rule: the physical displacement along a trajectory
is bounded by the sum of the step-wise weighted leverages. -/
theorem dist_interface_trajectory_le_leverage :
    dist (Φ x₀) (Φ (trajectory Tseq x₀ n)) ≤
      ∑ k ∈ Finset.range n,
        leverage Φ (Tseq k) (trajectory Tseq x₀ k) *
          perturbationSize (Tseq k) (trajectory Tseq x₀ k) := by
  simpa only [leverage_mul_size] using dist_interface_trajectory_le Φ Tseq x₀ n

/-- Through a `K`-Lipschitz interface, a trajectory can move the
physical state at most `K` times the total information moved. -/
theorem dist_interface_trajectory_le_of_lipschitz {K : NNReal}
    (hΦ : LipschitzWith K Φ) :
    dist (Φ x₀) (Φ (trajectory Tseq x₀ n)) ≤
      K * ∑ k ∈ Finset.range n, perturbationSize (Tseq k) (trajectory Tseq x₀ k) :=
  calc dist (Φ x₀) (Φ (trajectory Tseq x₀ n))
      ≤ K * dist x₀ (trajectory Tseq x₀ n) := hΦ.dist_le_mul _ _
    _ ≤ _ := mul_le_mul_of_nonneg_left (dist_trajectory_le Tseq x₀ n) K.coe_nonneg

end Metric

/-! ## Computational leverage and gain -/

section Computational

variable [MetricSpace I] (C : I → ℝ) (T T₁ T₂ : Perturbation I) (x : I)

/-- Computational leverage of `T` at `x` for a capability functional
`C : I → ℝ`: the leverage of `C` viewed as an interface into `ℝ`. -/
noncomputable def computationalLeverage : ℝ :=
  leverage C T x

theorem computationalLeverage_eq (h : dist x (T x) ≠ 0) :
    computationalLeverage C T x = |C (T x) - C x| / dist x (T x) := by
  unfold computationalLeverage leverage physicalEffect
  rw [if_neg h, Real.dist_eq, abs_sub_comm]

/-- The change in capability is exactly leverage times informational
size. -/
theorem abs_sub_eq_computationalLeverage_mul :
    |C (T x) - C x| = computationalLeverage C T x * perturbationSize T x := by
  rw [computationalLeverage, leverage_mul_size, physicalEffect, Real.dist_eq, abs_sub_comm]

end Computational

/-! ## Gain ratios -/

section Gain

variable (C : I → ℝ) (T T₁ T₂ : Perturbation I) (x : I)

/-- Capability cannot change without an informational change. -/
theorem capability_eq_of_fixed (h : T x = x) : C (T x) = C x := by
  rw [h]

/-- The gain ratio `Λ(T; x) = C x / C (T x)` of a perturbation for a
cost functional `C` (resources needed before over resources needed
after). -/
noncomputable def gainRatio : ℝ :=
  C x / C (T x)

/-- `T` improves the cost at `x`. -/
def Improves : Prop :=
  C (T x) < C x

theorem one_lt_gainRatio_iff (hpos : 0 < C (T x)) :
    1 < gainRatio C T x ↔ Improves C T x :=
  one_lt_div hpos

theorem gainRatio_id (h : C x ≠ 0) : gainRatio C id x = 1 :=
  div_self h

/-- Multiplicative chain rule for the gain ratio:
`Λ(T₁ ∘ T₂; x) = Λ(T₂; x) · Λ(T₁; T₂ x)`. -/
theorem gainRatio_compose (h : C (T₂ x) ≠ 0) :
    gainRatio C (compose T₁ T₂) x = gainRatio C T₂ x * gainRatio C T₁ (T₂ x) := by
  unfold gainRatio
  rw [compose_apply, div_mul_div_comm, mul_comm (C x), mul_div_mul_left _ _ h]

/-- Along a trajectory the total gain telescopes into the product of the
step gains. -/
theorem gainRatio_trajectory (Tseq : ℕ → Perturbation I) (x₀ : I) (n : ℕ)
    (h : ∀ k, k ≤ n → C (trajectory Tseq x₀ k) ≠ 0) :
    C x₀ / C (trajectory Tseq x₀ n) =
      ∏ k ∈ Finset.range n, gainRatio C (Tseq k) (trajectory Tseq x₀ k) := by
  induction n with
  | zero =>
    have h0 : C x₀ ≠ 0 := h 0 le_rfl
    simp [div_self h0]
  | succ n ih =>
    rw [Finset.prod_range_succ, ← ih (fun k hk => h k (Nat.le_succ_of_le hk))]
    unfold gainRatio
    rw [trajectory_succ, div_mul_div_comm, mul_comm (C x₀),
      mul_div_mul_left _ _ (h n (Nat.le_succ n))]

end Gain

/-! ## Information cost -/

section Cost

variable (κ : I → ℝ) (T T₁ T₂ : Perturbation I) (x : I)

/-- Cost of a perturbation measured by a complexity functional
`κ : I → ℝ` (description length, entropy, …): the absolute change in
complexity. -/
def informationCost : ℝ :=
  |κ (T x) - κ x|

theorem informationCost_nonneg : 0 ≤ informationCost κ T x :=
  abs_nonneg _

@[simp] theorem informationCost_id : informationCost κ id x = 0 := by
  simp [informationCost]

/-- Subadditivity of cost under composition. -/
theorem informationCost_compose_le :
    informationCost κ (compose T₁ T₂) x ≤
      informationCost κ T₂ x + informationCost κ T₁ (T₂ x) := by
  unfold informationCost
  rw [compose_apply, abs_sub_comm (κ (T₁ (T₂ x))), abs_sub_comm (κ (T₂ x)),
    abs_sub_comm (κ (T₁ (T₂ x)))]
  exact abs_sub_le _ _ _

/-- Efficiency of a perturbation: downstream gain per unit of cost. -/
noncomputable def efficiency (gain cost : Perturbation I → ℝ) (T : Perturbation I) : ℝ :=
  gain T / cost T

/-- A finite menu of candidate perturbations has a most efficient
member: the optimal perturbation `argmax_T gain T / cost T` exists. -/
theorem exists_optimal_perturbation (gain cost : Perturbation I → ℝ)
    (S : Finset (Perturbation I)) (hS : S.Nonempty) :
    ∃ T ∈ S, ∀ T' ∈ S, efficiency gain cost T' ≤ efficiency gain cost T :=
  S.exists_max_image (efficiency gain cost) hS

end Cost

/-! ## A witness of amplification -/

section Threshold

/-- A threshold interface `ℝ → ℝ`: one bit of output that flips at `0`. -/
noncomputable def step (x : ℝ) : ℝ :=
  if 0 < x then 1 else 0

/-- Leverage of the shift `x ↦ x + ε` at the threshold is `1 / ε`. -/
theorem leverage_step (ε : ℝ) (hε : 0 < ε) :
    leverage step (fun x => x + ε) 0 = 1 / ε := by
  have hd : dist (0 : ℝ) ((fun x : ℝ => x + ε) 0) = ε := by
    simp [Real.dist_eq, abs_of_pos hε]
  have hne : dist (0 : ℝ) ((fun x : ℝ => x + ε) 0) ≠ 0 := by
    rw [hd]; exact hε.ne'
  unfold leverage physicalEffect
  rw [if_neg hne, hd]
  congr 1
  simp [step, hε, Real.dist_eq]

/-- The threshold interface amplifies: leverage `1 / ε` is unbounded as
`ε → 0`. -/
theorem step_amplifies : Amplifies step := by
  intro K
  refine ⟨fun x => x + 1 / (|K| + 1), 0, ?_⟩
  have hpos : 0 < 1 / (|K| + 1) := by positivity
  rw [leverage_step _ hpos, one_div_one_div]
  exact lt_of_le_of_lt (le_abs_self K) (lt_add_one _)

/-- Consequently the threshold interface is not Lipschitz for any
constant. -/
theorem step_not_lipschitz : ¬ ∃ K : NNReal, LipschitzWith K step :=
  (amplifies_iff_not_lipschitz step).mp step_amplifies

end Threshold

/-! ## The landscape: normal versus original regions

The information landscape is not homogeneous. On a *normal* region the
interface is Lipschitz, so leverage is bounded and no small change has
a large consequence. The *original* locus at level `K` is the set of
states from which some perturbation has leverage above `K`. Inside a
normal region such a perturbation must leave the region: high-leverage
content lives at the frontier of what the ambient bound controls. -/

section Landscape

variable [MetricSpace I] [PseudoMetricSpace M] (Φ : Interface I M)

/-- Leverage of perturbations that stay inside `A` is bounded by `K`. -/
def LeverageBoundedOn (A : Set I) (K : ℝ) : Prop :=
  ∀ (T : Perturbation I) (x : I), x ∈ A → T x ∈ A → leverage Φ T x ≤ K

/-- The original locus at level `K`: states from which some
perturbation has leverage above `K`. -/
def originalLocus (K : ℝ) : Set I :=
  {x | ∃ T : Perturbation I, K < leverage Φ T x}

theorem amplifies_iff_originalLocus_nonempty :
    Amplifies Φ ↔ ∀ K : ℝ, (originalLocus Φ K).Nonempty :=
  forall_congr' fun _ => exists_comm

theorem leverageBoundedOn_of_lipschitzOnWith {A : Set I} {K : NNReal}
    (hΦ : LipschitzOnWith K Φ A) : LeverageBoundedOn Φ A K := by
  intro T x hx hTx
  unfold leverage physicalEffect
  split_ifs with h
  · exact K.coe_nonneg
  · rw [div_le_iff₀ (lt_of_le_of_ne dist_nonneg (Ne.symm h))]
    exact hΦ.dist_le_mul x hx (T x) hTx

theorem lipschitzOnWith_of_leverageBoundedOn {A : Set I} {K : ℝ}
    (h : LeverageBoundedOn Φ A K) : LipschitzOnWith (Real.toNNReal K) Φ A := by
  refine LipschitzOnWith.of_dist_le_mul fun x hx y hy => ?_
  by_cases hxy : dist x y = 0
  · rw [dist_eq_zero] at hxy
    subst hxy
    simp
  · have hpos : 0 < dist x y := lt_of_le_of_ne dist_nonneg (Ne.symm hxy)
    have hL := h (fun _ => y) x hx hy
    simp only [leverage, physicalEffect, hxy, ↓reduceIte] at hL
    rw [div_le_iff₀ hpos] at hL
    calc dist (Φ x) (Φ y) ≤ K * dist x y := hL
      _ ≤ (Real.toNNReal K : ℝ) * dist x y :=
        mul_le_mul_of_nonneg_right (Real.le_coe_toNNReal K) dist_nonneg

/-- A region is normal (bounded leverage for some constant) exactly when
the interface is Lipschitz on it. -/
theorem leverageBoundedOn_iff_lipschitzOnWith (A : Set I) :
    (∃ K : ℝ, LeverageBoundedOn Φ A K) ↔ ∃ K : NNReal, LipschitzOnWith K Φ A :=
  ⟨fun ⟨_, hK⟩ => ⟨_, lipschitzOnWith_of_leverageBoundedOn Φ hK⟩,
    fun ⟨K, hK⟩ => ⟨K, leverageBoundedOn_of_lipschitzOnWith Φ hK⟩⟩

/-- A perturbation whose leverage exceeds the Lipschitz constant of a
region starts or lands outside that region. -/
theorem exit_of_lt_leverage {A : Set I} {K : NNReal} (hΦ : LipschitzOnWith K Φ A)
    (T : Perturbation I) (x : I) (hK : (K : ℝ) < leverage Φ T x) :
    x ∉ A ∨ T x ∉ A := by
  by_cases hx : x ∈ A
  · by_cases hTx : T x ∈ A
    · exact absurd (leverageBoundedOn_of_lipschitzOnWith Φ hΦ T x hx hTx) (not_le.mpr hK)
    · exact Or.inr hTx
  · exact Or.inl hx

/-- Original content inside a normal region is reached only by
perturbations that leave the region. -/
theorem originalLocus_inter_subset {A : Set I} {K : NNReal}
    (hΦ : LipschitzOnWith K Φ A) :
    originalLocus Φ K ∩ A ⊆
      {x | ∃ T : Perturbation I, T x ∉ A ∧ (K : ℝ) < leverage Φ T x} := by
  rintro x ⟨⟨T, hT⟩, hx⟩
  show ∃ T : Perturbation I, T x ∉ A ∧ (K : ℝ) < leverage Φ T x
  refine ⟨T, ?_, hT⟩
  rcases exit_of_lt_leverage Φ hΦ T x hT with h | h
  · exact absurd hx h
  · exact h

end Landscape

/-! ## Compounding and mining order -/

section Mining

/-- Compounding: if every step of a trajectory has gain ratio at least
`g ≥ 0`, the total gain is at least `g ^ n`. One high-leverage lemma
multiplies everything downstream of it. -/
theorem pow_le_gainRatio_trajectory (C : I → ℝ) (Tseq : ℕ → Perturbation I) (x₀ : I)
    (n : ℕ) (h : ∀ k, k ≤ n → C (trajectory Tseq x₀ k) ≠ 0) {g : ℝ} (hg : 0 ≤ g)
    (hstep : ∀ k, k < n → g ≤ gainRatio C (Tseq k) (trajectory Tseq x₀ k)) :
    g ^ n ≤ C x₀ / C (trajectory Tseq x₀ n) := by
  rw [gainRatio_trajectory C Tseq x₀ n h]
  calc g ^ n = ∏ _k ∈ Finset.range n, g := by
        rw [Finset.prod_const, Finset.card_range]
    _ ≤ _ := Finset.prod_le_prod (fun _ _ => hg)
        (fun k hk => hstep k (Finset.mem_range.mp hk))

/-- Exchange principle for mining order: in a menu with nonnegative
gains, replacing a candidate by one of larger gain never lowers the
total (multiplicative) gain. -/
theorem prod_le_prod_exchange {α : Type w} [DecidableEq α] (gain : α → ℝ)
    (S : Finset α) (hS : ∀ a ∈ S, 0 ≤ gain a) {a b : α} (hb : b ∈ S) (ha : a ∉ S)
    (hab : gain b ≤ gain a) :
    ∏ c ∈ S, gain c ≤ ∏ c ∈ insert a (S.erase b), gain c := by
  rw [Finset.prod_insert (fun h => ha (Finset.mem_of_mem_erase h)),
    ← Finset.mul_prod_erase S gain hb]
  exact mul_le_mul_of_nonneg_right hab
    (Finset.prod_nonneg fun c hc => hS c (Finset.mem_of_mem_erase hc))

/-- Among all `k`-element sub-menus of a finite menu there is one of
maximal total gain: the `k` lemmas to mine first exist. -/
theorem exists_optimal_menu (gain : Perturbation I → ℝ) (S : Finset (Perturbation I))
    (k : ℕ) (hk : k ≤ S.card) :
    ∃ B ∈ S.powersetCard k, ∀ B' ∈ S.powersetCard k,
      ∏ T ∈ B', gain T ≤ ∏ T ∈ B, gain T :=
  Finset.exists_max_image (S.powersetCard k) (fun B => ∏ T ∈ B, gain T)
    (Finset.powersetCard_nonempty.mpr hk)

end Mining

end Problems.Engine.InformationField
