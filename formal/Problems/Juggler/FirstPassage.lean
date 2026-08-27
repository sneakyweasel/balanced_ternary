import Problems.Juggler.Drift
import Problems.Juggler.Envelope

namespace Problems.Juggler

/-!
# First-passage times

Ordinary stopping time versus coefficient / drift stopping time.
Neither is assumed finite. The already-known arrow is

```
HasFiniteCoeffStop n  →  HasFiniteStop n
```

The statement `∀ n ≥ 2, HasFiniteCoeffStop n` is not proved here.
-/

def HasFiniteStop (n : ℕ) : Prop :=
  ∃ k > 0, floorPower^[k] n < n

def HasFiniteCoeffStop (n : ℕ) : Prop :=
  ∃ k > 0, orbitExponentGap n k

/-- Isolated research target. Not a theorem. -/
def FiniteCoeffStopConjecture : Prop :=
  ∀ n, 2 ≤ n → HasFiniteCoeffStop n

theorem hasFiniteStop_of_contracts {n k : ℕ}
    (hk : 0 < k) (hlt : floorPower^[k] n < n) :
    HasFiniteStop n :=
  ⟨k, hk, hlt⟩

theorem hasFiniteCoeffStop_of_gap {n k : ℕ}
    (hk : 0 < k) (hgap : orbitExponentGap n k) :
    HasFiniteCoeffStop n :=
  ⟨k, hk, hgap⟩

/-- Already known: a positive combinatorial drift on the actual
itinerary forces a strict descent. Wraps `power_bound_contracts`. -/
theorem coeffStop_implies_stop {n : ℕ} (hn : 2 ≤ n)
    (h : HasFiniteCoeffStop n) : HasFiniteStop n := by
  obtain ⟨k, hk, hgap⟩ := h
  have hw : follows n (word n k) := follows_word_self n k
  have hlt : floorPower^[k] n < n := by
    have hgap' : 3 ^ oddCount (word n k) < 2 ^ (word n k).length := by
      simpa [word_length] using orbitExponentGap_iff.mp hgap
    have := power_bound_contracts hn hw hgap'
    simpa [word_length] using this
  exact ⟨k, hk, hlt⟩

end Problems.Juggler
