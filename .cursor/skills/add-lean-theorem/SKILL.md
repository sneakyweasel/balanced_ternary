---
name: add-lean-theorem
description: Add or package a Lean 4 theorem in formal/ without sorry. Use when formalizing a ledger row, writing NewtonStratum wrappers, or proving a Collatz/calculus claim in Lean.
---

# Add a Lean theorem

The project has no `sorry` or `admit`. If the proof is not short, leave the ledger tag as `EXACT — HUMAN PROOF` and record the deferral in `docs/research_journal.md`.

## Placement

| Content | Path |
|---------|------|
| Trit / residual / cubic fibre lemmas | `formal/BTCalculus/` |
| Packaging of existing cubic laws | `formal/BTCalculus/NewtonStratum.lean` |
| Collatz-only | `formal/Problems/Collatz/` plus a `CollatzDual.*` re-export |
| Automata | Do not invent proofs in `formal/Automata/` |

Do not rename the Lake package `collatz-dual-formal`.

Prefer wrapping a lemma that already compiles:

```lean
theorem newtonStratum_n2 {k r : Nat} (hr : r + 1 ≤ k) (p q : Int) :
    (3 : Int) ^ k ∣ n2Resid (k - 1 - r) p - n2Resid (k - 1 - r) q ↔
      (3 : Int) ^ r ∣ p - q :=
  depthDeficit_n2_visibility hr p q
```

Python faces in `research.residuals.stratum` must keep the same names (`newton_stratum_n2` ↔ `newtonStratum_n2`).

## Build

```powershell
$env:PATH = "$env:USERPROFILE\.elan\bin;$env:PATH"
cd formal
lake build BTCalculus
# or: lake build CollatzDual
```

Then update `docs/theory/theorem_ledger.json` (use the `add-ledger-row` skill) only if the Lean statement covers the English claim.
