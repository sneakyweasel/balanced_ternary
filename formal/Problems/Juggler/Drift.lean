import Problems.Juggler.WordStats

namespace Problems.Juggler

/-!
# Orbit drift

`G` along an actual itinerary is the combinatorial drift of `word n k`.
This file does not mention stopping times or certificates.
-/

def orbitDrift (n k : ℕ) : ℤ :=
  driftG (word n k)

def orbitExponentGap (n k : ℕ) : Prop :=
  exponentGap (word n k)

theorem orbitExponentGap_iff {n k : ℕ} :
    orbitExponentGap n k ↔ 3 ^ oddCount (word n k) < 2 ^ k := by
  simp [orbitExponentGap, exponentGap, word_length]

theorem follows_word_self (n k : ℕ) : follows n (word n k) :=
  (follows_iff_word n (word n k)).mpr (by simp [word_length])

end Problems.Juggler
