from pathlib import Path

p = Path("docs/research_journal.md")
add = r"""
## Nil-PET re-entry: the first difference re-expands \(A\{\Delta B\}\) (Phase 0; answers the characteristic-factor question the v94 CLOSE left external)

- **Date:** 2026-09-01
- **Objective:** The v94 rate-free door left characteristic factors external. Does the first Host–Kra / PET step on the Heisenberg lift keep the floor-removal correction as a Mal'cev coordinate, or does Mal'cev reduction re-expand it into an amplitude-product?
- **Hypotheses:** \(\chi_\Delta=\{-A(n+h)\lfloor\Delta B\rfloor-A(n)\{\Delta B\}\}\) with \(A\{\Delta B\}\) of GG species (\(A(n+2)-A(n)\asymp n^{1/8}\)); the second lift is the original algebra, not a published Hardy-nil orbit. Falsifier: the identity fails, or \(A\{\Delta B\}\) is \(o(1)\), or \(A'\to 0\), or \(\Delta B\) is \(o(1)\)-close to a Hardy-in-\(n\) increment.
- **Major results:**
  - **Identity (EXACT — HUMAN PROOF, `J-nil-pet-reentry`):** \(g(n)^{-1}g(n+h)=(\Delta A,\Delta B,-A\Delta B)\) and the reduced vertical is \(\{-A(n+h)\lfloor\Delta B\rfloor-A(n)\{\Delta B\}\}\). Fraction witnesses exact; one scaled tower pair exact. This is not the v94 abelian difference \(\{v(n+h)^{9/4}-v(n)^{9/4}\}\).
  - **Species (EXACT, leading ratio COMPUTATIONALLY VERIFIED):** \(A(n+2)-A(n)\sim\tfrac{27}{8}n^{1/8}\gg 1\) (GG); \(\{\Delta B\}\) is not concentrated at \(0\); leftover of \(\Delta B\) versus \((n+h)^{9/4}-n^{9/4}\) is \(\asymp n^{3/4}\), not \(o(1)\).
  - **Method claim REFUTED:** `juggler_nil_pet_stays_coordinate`. PET / characteristic-factor induction re-enters the amplitude-product class at step one. The second Heisenberg lift of \((A,\Delta B)\) is `J-tower-heisenberg-coordinate` applied to a new pair, not a degree drop to Richter / Frantzikinakis / Boshernitzan.
- **Refuted ideas:** that PET on the Heisenberg lift keeps the floor-correction as a coordinate without amplitude-product re-entry.
- **Literature:** `host-kra-2005-nilmanifolds` added to `literature/`.
- **Open:** the rate-free conjecture stays ACTIVE as Hardy-of-floor composition (Leibman on the horizontal, not PET). The \(\beta>0.369\) bias fallback is not opened. No PET².
- **Decision:** PROMOTE — dossier `docs/problems/juggler_nil_pet_reentry.md`, ledger row `J-nil-pet-reentry`. PET as a method is closed. No Lean, no Paper B edit, no K3/HH reopen.

```text
What was learned
- the first PET difference of the Heisenberg lift is
  (ΔA, ΔB, -A ΔB); after reduction the vertical is
  {-A(n+h) floor(ΔB) - A(n){ΔB}}
- A{ΔB} is GG: A(n+2)-A(n) ≍ n^{1/8} >> 1
- ΔB is not o(1)-close to a Hardy-in-n increment
  (leftover ≍ n^{3/4})
- re-lifting A{ΔB} is the original group law, not a
  published Hardy-nil orbit
- this is not the v94 abelian difference
Strongest theorem
- J-nil-pet-reentry (EXACT - HUMAN PROOF): PET
  re-enters the amplitude-product class at step one
Strongest refutation
- juggler_nil_pet_stays_coordinate
Reusable machinery
- nil_pet_reentry probe: Fraction Mal'cev difference
  and scaled-integer species (A-increment, {ΔB}, leftover)
Branch status
- PROMOTE
Why
- the identity is exact, distinct from the v94 abelian
  difference, and the predicted fourth layer fires
Best next question
- none from this door; the live target remains the
  rate-free conjecture as Hardy-of-floor composition
  (Leibman on the horizontal, not PET)
```
"""
text = p.read_text(encoding="utf-8")
if "J-nil-pet-reentry" not in text[-4000:]:
    p.write_text(text.rstrip() + "\n" + add, encoding="utf-8")
    print("appended")
else:
    print("already present")
