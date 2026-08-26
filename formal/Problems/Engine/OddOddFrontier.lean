import Problems.Engine.OddRunFinancing
import Problems.Engine.Progress

namespace Problems.Engine

/-!
# First even residual of an odd-to-odd start

An even residual `z` falls into one of three square cells relative to
an odd `n`: below `n^2`, the return cell `n^2 < z < (n+1)^2`, or
overshoot `(n+1)^2 ≤ z`. Under `MinimalNonTerm`, the first cell is
impossible and the first `O^a E` block is not `Descent` or `Capture`.
The leftover is a return-to-start cycle candidate or strict overshoot.
Not a halt theorem.
-/

theorem image_oddEvenBlock (x a b : ℕ) :
    image x (oddEvenBlock a b) =
      image (image x (List.replicate a Branch.odd))
        (List.replicate b Branch.even) :=
  image_append x (List.replicate a Branch.odd) (List.replicate b Branch.even)

theorem first_even_return {x a : ℕ} (hw : follows x (oddEvenBlock a 1)) :
    image x (List.replicate a Branch.odd) % 2 = 0 :=
  odd_run_even_residual hw

theorem image_odd_run (n a : ℕ) :
    image n (List.replicate a Branch.odd) = floorPower^[a] n := by
  simpa [List.length_replicate] using image_eq_iterate n (List.replicate a Branch.odd)

theorem even_floorPower_lt_iff {z n : ℕ} (heven : z % 2 = 0) :
    floorPower z < n ↔ z < n ^ 2 := by
  rw [floorPower_even_eq heven]
  simpa [pow_two] using (@Nat.sqrt_lt z n)

theorem even_floorPower_eq_iff {z n : ℕ} (heven : z % 2 = 0) :
    floorPower z = n ↔ n ^ 2 ≤ z ∧ z < (n + 1) ^ 2 :=
  floorPower_even_eq_iff_sq_interval heven

theorem even_floorPower_gt_iff {z n : ℕ} (heven : z % 2 = 0) :
    n < floorPower z ↔ (n + 1) ^ 2 ≤ z := by
  have hiff : floorPower z < n + 1 ↔ z < (n + 1) ^ 2 :=
    even_floorPower_lt_iff (n := n + 1) heven
  constructor
  · intro h
    have : ¬floorPower z < n + 1 := Nat.not_lt.mpr (Nat.succ_le_of_lt h)
    exact Nat.le_of_not_lt (hiff.not.mp this)
  · intro h
    have : ¬floorPower z < n + 1 := hiff.not.mpr (Nat.not_lt.mpr h)
    exact Nat.lt_of_succ_le (Nat.le_of_not_lt this)

theorem odd_sq_odd {n : ℕ} (hodd : n % 2 = 1) : n ^ 2 % 2 = 1 := by
  have : n * n % 2 = 1 := by simp [Nat.mul_mod, hodd]
  simpa [pow_two] using this

theorem even_ne_odd_square {z n : ℕ} (heven : z % 2 = 0)
    (hodd : n % 2 = 1) : z ≠ n ^ 2 := by
  intro h
  have : z % 2 = 1 := by simpa [h] using odd_sq_odd hodd
  omega

theorem even_ge_sq_image_ge {z n : ℕ} (heven : z % 2 = 0)
    (h : n ^ 2 ≤ z) : n ≤ floorPower z := by
  rw [floorPower_even_eq heven]
  exact Nat.le_sqrt.mpr (by simpa [pow_two] using h)

/-- An even residual versus an odd start sits in exactly one cell. -/
theorem odd_even_residual_trichotomy {z n : ℕ}
    (hodd : n % 2 = 1) (heven : z % 2 = 0) :
    z < n ^ 2 ∨ (n ^ 2 < z ∧ z < (n + 1) ^ 2) ∨ (n + 1) ^ 2 ≤ z := by
  rcases lt_or_ge z (n ^ 2) with hlt | hge
  · exact Or.inl hlt
  · have hne : z ≠ n ^ 2 := even_ne_odd_square heven hodd
    have hgt : n ^ 2 < z := lt_of_le_of_ne hge hne.symm
    rcases lt_or_ge z ((n + 1) ^ 2) with hcell | hover
    · exact Or.inr (Or.inl ⟨hgt, hcell⟩)
    · exact Or.inr (Or.inr hover)

/-- Image of an even residual in each cell. -/
theorem odd_even_residual_image {z n : ℕ}
    (hodd : n % 2 = 1) (heven : z % 2 = 0) :
    (z < n ^ 2 ∧ floorPower z < n) ∨
      (n ^ 2 < z ∧ z < (n + 1) ^ 2 ∧ floorPower z = n) ∨
        ((n + 1) ^ 2 ≤ z ∧ n < floorPower z) := by
  rcases odd_even_residual_trichotomy hodd heven with hlt | hmid | hover
  · exact Or.inl ⟨hlt, (even_floorPower_lt_iff heven).mpr hlt⟩
  · refine Or.inr (Or.inl ⟨hmid.1, hmid.2, ?_⟩)
    exact (even_floorPower_eq_iff heven).mpr ⟨le_of_lt hmid.1, hmid.2⟩
  · exact Or.inr (Or.inr ⟨hover, (even_floorPower_gt_iff heven).mpr hover⟩)

/-- `O^a E` descends iff the even residual lies below `n^2`. -/
theorem first_even_descent_iff {n a : ℕ} (hw : follows n (oddEvenBlock a 1)) :
    Descent n (oddEvenBlock a 1) ↔
      image n (List.replicate a Branch.odd) < n ^ 2 := by
  have hz := odd_run_even_residual hw
  have himg : image n (oddEvenBlock a 1) =
      floorPower (image n (List.replicate a Branch.odd)) := by
    simp [image_oddEvenBlock, image]
  constructor
  · intro hd
    have : floorPower (image n (List.replicate a Branch.odd)) < n := by
      simpa [himg] using hd.2
    exact (even_floorPower_lt_iff hz).mp this
  · intro hlt
    refine ⟨hw, ?_⟩
    have : floorPower (image n (List.replicate a Branch.odd)) < n :=
      (even_floorPower_lt_iff hz).mpr hlt
    simpa [himg] using this

/-- Below-`n^2` first residual is `FiniteProgress` via `O^a E`. -/
theorem finiteProgress_of_first_even_below {n a : ℕ}
    (hw : follows n (oddEvenBlock a 1))
    (hlt : image n (List.replicate a Branch.odd) < n ^ 2) :
    FiniteProgress n :=
  finiteProgress_of_descent ((first_even_descent_iff hw).mpr hlt)

theorem minimal_even_residual_gt_sq {n z k : ℕ} (h : MinimalNonTerm n)
    (hk : floorPower^[k] n = z) (heven : z % 2 = 0) : n ^ 2 < z := by
  have hle := minimal_nonterm_even_ge_sq h hk heven
  have hne := even_ne_odd_square heven (minimal_nonterm_odd h)
  exact lt_of_le_of_ne hle hne.symm

/-- A `MinimalNonTerm` start cannot descend on its first `O^a E`. -/
theorem minimal_nonterm_not_first_even_descent {n a : ℕ}
    (h : MinimalNonTerm n) (hw : follows n (oddEvenBlock a 1)) :
    ¬Descent n (oddEvenBlock a 1) := by
  intro hd
  have hz := odd_run_even_residual hw
  have hlt := (first_even_descent_iff hw).mp hd
  have hbar :=
    minimal_nonterm_even_ge_sq (k := a) h (image_odd_run n a).symm hz
  exact (not_lt_of_ge hbar) hlt

/-- Nor can the first `O^a E` capture `{1}`: the image stays `≥ n ≥ 12`. -/
theorem minimal_nonterm_not_first_even_capture {n a : ℕ}
    (h : MinimalNonTerm n) (hw : follows n (oddEvenBlock a 1)) :
    ¬Capture n (oddEvenBlock a 1) := by
  intro hc
  have hz := odd_run_even_residual hw
  have himg : image n (oddEvenBlock a 1) =
      floorPower (image n (List.replicate a Branch.odd)) := by
    simp [image_oddEvenBlock, image]
  have hge : n ≤ image n (oddEvenBlock a 1) := by
    have hbar :=
      minimal_nonterm_even_ge_sq (k := a) h (image_odd_run n a).symm hz
    have : n ≤ floorPower (image n (List.replicate a Branch.odd)) :=
      even_ge_sq_image_ge hz hbar
    simpa [himg] using this
  have hn : 12 ≤ n := minimal_nonterm_ge_twelve h
  have : 12 ≤ 1 := le_trans hn (by simpa [hc.2] using hge)
  exact (by decide : ¬(12 : ℕ) ≤ 1) this

/-- First `O^a E` is not `FiniteProgress` on a minimal non-1 start. -/
theorem minimal_nonterm_not_first_even_finiteProgress {n a : ℕ}
    (h : MinimalNonTerm n) (hw : follows n (oddEvenBlock a 1)) :
    ¬(Descent n (oddEvenBlock a 1) ∨ Capture n (oddEvenBlock a 1)) :=
  fun hfp =>
    hfp.elim (minimal_nonterm_not_first_even_descent h hw)
      (minimal_nonterm_not_first_even_capture h hw)

/-- Return to `n` on `O^a E` is a directed cycle. Not a cycle-impossibility
theorem. -/
theorem first_even_return_cycle {n a : ℕ}
    (_hw : follows n (oddEvenBlock a 1))
    (hret : image n (oddEvenBlock a 1) = n) :
    floorPower^[a + 1] n = n := by
  have hlen : (oddEvenBlock a 1).length = a + 1 := by
    simp [oddEvenBlock, List.length_append, List.length_replicate]
  have : image n (oddEvenBlock a 1) = floorPower^[a + 1] n := by
    rw [image_eq_iterate, hlen]
  simpa [this] using hret

/-- On a `MinimalNonTerm` start the first even residual is a return
cell (`T(z)=n`) or a strict overshoot (`T(z)>n`). -/
theorem minimal_first_even_dichotomy {n a : ℕ} (h : MinimalNonTerm n)
    (hw : follows n (oddEvenBlock a 1)) :
    (image n (oddEvenBlock a 1) = n ∧
        image n (List.replicate a Branch.odd) < (n + 1) ^ 2) ∨
      ((n + 1) ^ 2 ≤ image n (List.replicate a Branch.odd) ∧
        n < image n (oddEvenBlock a 1)) := by
  have hodd := minimal_nonterm_odd h
  have hz := odd_run_even_residual hw
  set z := image n (List.replicate a Branch.odd)
  have himg : image n (oddEvenBlock a 1) = floorPower z := by
    simp [image_oddEvenBlock, image, z]
  have hgt :=
    minimal_even_residual_gt_sq (k := a) h (image_odd_run n a).symm hz
  rcases odd_even_residual_image (z := z) hodd hz with hlt | hmid | hover
  · exact (lt_asymm hgt hlt.1).elim
  · refine Or.inl ⟨?_, hmid.2.1⟩
    simpa [himg] using hmid.2.2
  · refine Or.inr ⟨hover.1, ?_⟩
    simpa [himg] using hover.2

end Problems.Engine
