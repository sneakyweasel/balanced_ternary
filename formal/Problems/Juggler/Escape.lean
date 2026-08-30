import Problems.Juggler.CycleCore

namespace Problems.Juggler

/-!
# Orbit split: cycle or escape

A Juggler orbit in `ℕ` is eventually periodic or unbounded. On a
`MinimalNonTerm` start the periodic case stays `≥ n`, so it is not
the `1`-cycle. The `OOEOOE` square-cell trap survives after dropping
the `CycleMin` return hypothesis: an even landing, or an even next
image below `n^2`, is descent and is impossible on a CE.

This is not a halt theorem. It does not prove
`∀ n, ¬EscapesToInfinity n`. It does not prove that every cycle is
impossible. `FiniteCoeffStopConjecture` remains a `def`.
-/

def EscapesToInfinity (n : ℕ) : Prop :=
  ∀ B, ∃ k, B < floorPower^[k] n

def EventuallyCycles (n : ℕ) : Prop :=
  ∃ i j, i < j ∧ floorPower^[i] n = floorPower^[j] n

def wordOOEOOEO : List Branch :=
  wordOOEOOE ++ [Branch.odd]

theorem not_escapes_iff_bounded {n : ℕ} :
    ¬EscapesToInfinity n ↔ ∃ M, ∀ k, floorPower^[k] n ≤ M := by
  constructor
  · intro h
    obtain ⟨B, hB⟩ := not_forall.mp h
    refine ⟨B, fun k => Nat.le_of_not_lt ?_⟩
    exact not_exists.mp hB k
  · intro ⟨M, hM⟩ hEsc
    obtain ⟨k, hk⟩ := hEsc M
    exact (not_lt_of_ge (hM k)) hk

/-- A uniformly bounded orbit repeats. Finite pigeonhole on the
prefix of length `M + 2`. -/
theorem bounded_orbit_eventually_cycles {n M : ℕ}
    (hbound : ∀ k, floorPower^[k] n ≤ M) :
    EventuallyCycles n := by
  by_contra hnone
  have hdistinct :
      ∀ i j, i < j → j < M + 2 → floorPower^[i] n ≠ floorPower^[j] n := by
    intro i j hij _hj heq
    exact hnone ⟨i, j, hij, heq⟩
  have hinj :
      Function.Injective fun i : Fin (M + 2) => floorPower^[i.val] n := by
    intro a b h
    apply Fin.ext
    rcases lt_trichotomy a.val b.val with hlt | heq | hgt
    · exact (hdistinct a.val b.val hlt (by omega) h).elim
    · exact heq
    · exact (hdistinct b.val a.val hgt (by omega) h.symm).elim
  have hsubset :
      (Finset.univ.image fun i : Fin (M + 2) => floorPower^[i.val] n) ⊆
        Finset.range (M + 1) := by
    intro x hx
    rcases Finset.mem_image.mp hx with ⟨i, _, rfl⟩
    exact Finset.mem_range.mpr (Nat.lt_succ_of_le (hbound i.val))
  have hcard := Finset.card_le_card hsubset
  have himg :=
    Finset.card_image_of_injective
      (f := fun i : Fin (M + 2) => floorPower^[i.val] n) Finset.univ hinj
  simp [himg, Fintype.card_fin, Finset.card_univ, Finset.card_range] at hcard

theorem cycles_or_escapes (n : ℕ) :
    EventuallyCycles n ∨ EscapesToInfinity n := by
  by_cases h : EscapesToInfinity n
  · exact Or.inr h
  · obtain ⟨M, hM⟩ := not_escapes_iff_bounded.mp h
    exact Or.inl (bounded_orbit_eventually_cycles hM)

theorem reachesOne_implies_eventually_cycles {n : ℕ}
    (h : ReachesOne n) : EventuallyCycles n := by
  obtain ⟨k, hk⟩ := h
  refine ⟨k, k + 1, Nat.lt_succ_self k, ?_⟩
  calc
    floorPower^[k] n = 1 := hk
    _ = floorPower 1 := floorPower_one.symm
    _ = floorPower^[k + 1] n := by
        rw [Function.iterate_succ_apply', hk]

theorem minimal_nonterm_cycles_or_escapes {n : ℕ}
    (_h : MinimalNonTerm n) :
    EventuallyCycles n ∨ EscapesToInfinity n :=
  cycles_or_escapes n

theorem minimal_nonterm_cycle_values_ge {n i : ℕ}
    (h : MinimalNonTerm n) : n ≤ floorPower^[i] n :=
  minimal_nonterm_iterate_ge h i

theorem wordOOEOOE_length : wordOOEOOE.length = 6 := rfl

theorem wordOOEOOE_oddCount : oddCount wordOOEOOE = 4 := by
  simp [wordOOEOOE]

theorem wordOOEOOEO_length : wordOOEOOEO.length = 7 := by
  simp [wordOOEOOEO, wordOOEOOE]

theorem wordOOEOOEO_oddCount : oddCount wordOOEOOEO = 5 := by
  simp [wordOOEOOEO, wordOOEOOE]

theorem follows_ooeooe_pow {n : ℕ} (hw : follows n wordOOEOOE) :
    (image n wordOOEOOE) ^ 64 ≤ n ^ 81 := by
  have h := power_bound_word hw
  rw [wordOOEOOE_length, wordOOEOOE_oddCount] at h
  rw [image_eq_iterate, wordOOEOOE_length]
  convert h <;> norm_num

/-- Same square-cell comparison as the human `OOEOOE` corridor, with
no `CycleMin` return hypothesis. -/
theorem follows_ooeooe_image_lt_sq {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOEOOE) :
    image n wordOOEOOE < n ^ 2 := by
  have hpow := follows_ooeooe_pow hw
  refine Nat.lt_of_not_ge fun hge => ?_
  have hleft : n ^ 128 ≤ (image n wordOOEOOE) ^ 64 := by
    calc
      n ^ 128 = n ^ (2 * 64) := by norm_num
      _ = (n ^ 2) ^ 64 := Nat.pow_mul n 2 64
      _ ≤ (image n wordOOEOOE) ^ 64 := Nat.pow_le_pow_left hge 64
  have hle : n ^ 128 ≤ n ^ 81 := le_trans hleft hpow
  have hlt : n ^ 81 < n ^ 128 := pow_lt_of_two_le hn (by decide : 81 < 128)
  exact (not_le_of_gt hlt) hle

theorem follows_ooeooeo_pow {n : ℕ} (hw : follows n wordOOEOOEO) :
    (image n wordOOEOOEO) ^ 128 ≤ n ^ 243 := by
  have h := power_bound_word hw
  rw [wordOOEOOEO_length, wordOOEOOEO_oddCount] at h
  rw [image_eq_iterate, wordOOEOOEO_length]
  convert h <;> norm_num

/-- The word `OOEOOEO` has the square-cell gap `256 > 243`. -/
theorem follows_ooeooeo_image_lt_sq {n : ℕ} (hn : 2 ≤ n)
    (hw : follows n wordOOEOOEO) :
    image n wordOOEOOEO < n ^ 2 := by
  have hpow := follows_ooeooeo_pow hw
  refine Nat.lt_of_not_ge fun hge => ?_
  have hleft : n ^ 256 ≤ (image n wordOOEOOEO) ^ 128 := by
    calc
      n ^ 256 = n ^ (2 * 128) := by norm_num
      _ = (n ^ 2) ^ 128 := Nat.pow_mul n 2 128
      _ ≤ (image n wordOOEOOEO) ^ 128 := Nat.pow_le_pow_left hge 128
  have hle : n ^ 256 ≤ n ^ 243 := le_trans hleft hpow
  have hlt : n ^ 243 < n ^ 256 := pow_lt_of_two_le hn (by decide : 243 < 256)
  exact (not_le_of_gt hlt) hle

theorem follows_singleton_even {m : ℕ} (he : m % 2 = 0) :
    follows m [Branch.even] :=
  ⟨he, trivial⟩

theorem follows_singleton_odd {m : ℕ} (hodd : m % 2 = 1) :
    follows m [Branch.odd] :=
  ⟨hodd, trivial⟩

theorem follows_ooeooe_even {n : ℕ} (hw : follows n wordOOEOOE)
    (he : image n wordOOEOOE % 2 = 0) :
    follows n (wordOOEOOE ++ [Branch.even]) :=
  follows_append hw (follows_singleton_even he)

theorem image_ooeooe_even (n : ℕ) :
    image n (wordOOEOOE ++ [Branch.even]) =
      floorPower (image n wordOOEOOE) := by
  rw [image_append]
  rfl

/-- Even `OOEOOE` landing is descent, hence impossible on a CE. -/
theorem minimal_ooeooe_not_even_landing {n : ℕ}
    (h : MinimalNonTerm n) (hw : follows n wordOOEOOE) :
    image n wordOOEOOE % 2 = 1 := by
  have hn2 : 2 ≤ n :=
    le_trans (by decide : (2 : ℕ) ≤ 12) (minimal_nonterm_ge_twelve h)
  have hlt := follows_ooeooe_image_lt_sq hn2 hw
  by_contra heven
  have he : image n wordOOEOOE % 2 = 0 := by omega
  have hdrop : floorPower (image n wordOOEOOE) < n :=
    (even_floorPower_lt_iff he).mpr hlt
  exact minimal_nonterm_no_descent h
    ⟨follows_ooeooe_even hw he, by simpa [image_ooeooe_even] using hdrop⟩

theorem follows_wordOOEOOEO_of_odd_landing {n : ℕ}
    (hw : follows n wordOOEOOE) (hodd : image n wordOOEOOE % 2 = 1) :
    follows n wordOOEOOEO := by
  simpa [wordOOEOOEO] using follows_append hw (follows_singleton_odd hodd)

theorem follows_ooeooeo_even {n : ℕ} (hw : follows n wordOOEOOEO)
    (he : image n wordOOEOOEO % 2 = 0) :
    follows n (wordOOEOOEO ++ [Branch.even]) :=
  follows_append hw (follows_singleton_even he)

theorem image_ooeooeo_even (n : ℕ) :
    image n (wordOOEOOEO ++ [Branch.even]) =
      floorPower (image n wordOOEOOEO) := by
  rw [image_append]
  rfl

/-- On a CE, `OOEOOE` forces another `OO`. The next completed letter
after the forced `O` cannot be `E`. -/
theorem minimal_ooeooe_forces_oo {n : ℕ}
    (h : MinimalNonTerm n) (hw : follows n wordOOEOOE) :
    follows n wordOOEOOEO ∧ image n wordOOEOOEO % 2 = 1 := by
  have hodd := minimal_ooeooe_not_even_landing h hw
  have hf := follows_wordOOEOOEO_of_odd_landing hw hodd
  refine ⟨hf, ?_⟩
  have hn2 : 2 ≤ n :=
    le_trans (by decide : (2 : ℕ) ≤ 12) (minimal_nonterm_ge_twelve h)
  have hzlt := follows_ooeooeo_image_lt_sq hn2 hf
  by_contra heven
  have he : image n wordOOEOOEO % 2 = 0 := by omega
  have hdrop : floorPower (image n wordOOEOOEO) < n :=
    (even_floorPower_lt_iff he).mpr hzlt
  exact minimal_nonterm_no_descent h
    ⟨follows_ooeooeo_even hf he, by simpa [image_ooeooeo_even] using hdrop⟩

end Problems.Juggler
