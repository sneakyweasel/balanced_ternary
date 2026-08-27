import Problems.Engine.ResidualChain
import Problems.Engine.RepeatedBlock

namespace Problems.Engine

/-!
# Residual path regimes: repeats, cycles, envelopes

A residual step is already `ResidualStep`. This module records the
finite bounded-path consequence (a repeated orbit state is a cycle)
and the cycle-word envelope `2^r < 3^o`. A residual return
`ResidualStep x x` therefore needs `a ≥ 2`. This is not a halt
theorem, not a cycle-impossibility theorem, and not an infinite-path
type.
-/

def ResidualDescent (x y : ℕ) : Prop :=
  ResidualStep x y ∧ y < x

def ResidualReturn (x y : ℕ) : Prop :=
  ResidualStep x y ∧ y = x

def ResidualOvershoot (x y : ℕ) : Prop :=
  ResidualStep x y ∧ x < y

theorem two_pow_ne_three_pow {k o : ℕ} (hk : 1 ≤ k) : 2 ^ k ≠ 3 ^ o := by
  intro h
  have heven := two_pow_even_of_pos hk
  have hodd := three_pow_odd o
  rw [h] at heven
  omega

/-- A realized return to `x ≥ 2` forces `2^r ≤ 3^o`. -/
theorem cycle_envelope {x : ℕ} {w : List Branch}
    (hx : 2 ≤ x) (hw : follows x w) (hret : image x w = x) :
    2 ^ w.length ≤ 3 ^ oddCount w := by
  have hpow := power_bound_word hw
  have himg : floorPower^[w.length] x = x := by
    rw [← image_eq_iterate, hret]
  rw [himg] at hpow
  exact (Nat.pow_le_pow_iff_right (show 1 < x by omega)).mp hpow

/-- Equality `2^r = 3^o` is impossible for a nonempty word, so every
nontrivial cycle is strictly expanding in the exponent. -/
theorem cycle_strict_envelope {x : ℕ} {w : List Branch}
    (hx : 2 ≤ x) (hw : follows x w) (hret : image x w = x)
    (hlen : 1 ≤ w.length) :
    2 ^ w.length < 3 ^ oddCount w :=
  lt_of_le_of_ne (cycle_envelope hx hw hret) (two_pow_ne_three_pow hlen)

/-- Contracting words cannot close a cycle. -/
theorem cycle_not_contracting {x : ℕ} {w : List Branch}
    (hx : 2 ≤ x) (hw : follows x w) (hret : image x w = x) :
    ¬3 ^ oddCount w < 2 ^ w.length := by
  intro hgap
  have hlt := power_bound_contracts hx hw hgap
  have himg : floorPower^[w.length] x = x := by
    rw [← image_eq_iterate, hret]
  rw [himg] at hlt
  exact (lt_irrefl x) hlt

/-- A repeated iterate is a finite Juggler cycle at that state. -/
theorem orbit_repeat_cycle {n i j : ℕ} (hij : i ≤ j)
    (h : floorPower^[i] n = floorPower^[j] n) :
    floorPower^[j - i] (floorPower^[i] n) = floorPower^[i] n := by
  have hsum : i + (j - i) = j := Nat.add_sub_cancel' hij
  calc
    floorPower^[j - i] (floorPower^[i] n)
        = floorPower^[i + (j - i)] n := (iterate_add_right n i (j - i)).symm
    _ = floorPower^[j] n := by rw [hsum]
    _ = floorPower^[i] n := h.symm

/-- A residual return is an actual cycle of length `a + b`. -/
theorem residual_return_cycle {x a b : ℕ}
    (_hw : follows x (oddEvenBlock a b))
    (hret : image x (oddEvenBlock a b) = x) :
    floorPower^[a + b] x = x := by
  rw [← image_oddEvenBlock_iterate, hret]

theorem residual_return_envelope {x a b : ℕ}
    (hx : 2 ≤ x) (hb : 1 ≤ b) (hw : follows x (oddEvenBlock a b))
    (hret : image x (oddEvenBlock a b) = x) :
    2 ^ (a + b) ≤ 3 ^ a ∧ 2 ^ (a + b) < 3 ^ a := by
  have hlen := length_oddEvenBlock a b
  have hodd := oddCount_oddEvenBlock a b
  have hle : 2 ^ (oddEvenBlock a b).length ≤ 3 ^ oddCount (oddEvenBlock a b) :=
    cycle_envelope hx hw hret
  have hlt : 2 ^ (oddEvenBlock a b).length < 3 ^ oddCount (oddEvenBlock a b) :=
    cycle_strict_envelope hx hw hret (by
      rw [hlen]
      omega)
  constructor
  · simpa [hlen, hodd] using hle
  · simpa [hlen, hodd] using hlt

/-- Residual period-1 on `x ≥ 2` cannot start with `a ≤ 1`. -/
theorem residual_return_a_ge_two {x a b : ℕ}
    (hx : 2 ≤ x) (hb : 1 ≤ b) (hw : follows x (oddEvenBlock a b))
    (hret : image x (oddEvenBlock a b) = x) : 2 ≤ a := by
  have hle := (residual_return_envelope hx hb hw hret).1
  have hmon : 2 ^ (a + 1) ≤ 2 ^ (a + b) :=
    Nat.pow_le_pow_right (by decide : (1 : ℕ) ≤ 2) (Nat.add_le_add_left hb a)
  have : 2 ^ (a + 1) ≤ 3 ^ a := le_trans hmon hle
  exact two_pow_succ_le_three_pow_iff.mp this

/-- A residual chain from a CE stays at or above the start. -/
theorem minimal_residual_chain_ge {n y : ℕ}
    (h : MinimalNonTerm n) (hc : ResidualChain n y) : n ≤ y := by
  obtain ⟨w, hw, himg⟩ := residualChain_word hc
  simpa [himg] using minimal_nonterm_image_ge h hw

/-- Finite pigeonhole: a prefix valued in `[lo, hi]` that is longer
than the interval cannot be nodup. This is the finite form of
“bounded residual path ⇒ repeat”. -/
theorem bounded_prefix_not_nodup {lo hi : ℕ} (hle : lo ≤ hi)
    (xs : List ℕ) (hmem : ∀ x ∈ xs, lo ≤ x ∧ x ≤ hi)
    (hlen : hi + 1 - lo < xs.length) : ¬xs.Nodup := by
  intro hn
  have hsubset : xs.toFinset ⊆ Finset.Icc lo hi := by
    intro x hx
    exact Finset.mem_Icc.mpr (hmem x (List.mem_toFinset.mp hx))
  have hcard := Finset.card_le_card hsubset
  have hIcc : (Finset.Icc lo hi).card = hi + 1 - lo := by
    let emb : ℕ ↪ ℕ := ⟨fun i => i + lo, add_left_injective lo⟩
    have hmap : Finset.Icc lo hi = (Finset.range (hi + 1 - lo)).map emb := by
      ext x
      constructor
      · intro hx
        rcases Finset.mem_Icc.mp hx with ⟨hlo, hhi⟩
        refine Finset.mem_map.mpr ⟨x - lo, ?_, ?_⟩
        · exact Finset.mem_range.mpr (by omega)
        · change x - lo + lo = x
          exact Nat.sub_add_cancel hlo
      · intro hx
        rcases Finset.mem_map.mp hx with ⟨i, himem, heq⟩
        have hi' : i < hi + 1 - lo := Finset.mem_range.mp himem
        have hsum : i + lo = x := by
          simpa [emb] using heq
        have hlo : lo ≤ x := by
          rw [← hsum]
          exact Nat.le_add_left lo i
        have hhi : x ≤ hi := by
          rw [← hsum]
          have : i + lo < hi + 1 - lo + lo := Nat.add_lt_add_right hi' lo
          have hcancel : hi + 1 - lo + lo = hi + 1 :=
            Nat.sub_add_cancel (Nat.le_succ_of_le hle)
          rw [hcancel] at this
          exact Nat.lt_succ_iff.mp this
        exact Finset.mem_Icc.mpr ⟨hlo, hhi⟩
    rw [hmap, Finset.card_map, Finset.card_range]
  have hlen' : xs.toFinset.card = xs.length := List.toFinset_card_of_nodup hn
  omega

end Problems.Engine
