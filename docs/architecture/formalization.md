# Formalization architecture

Lean 4 + Mathlib lives under `formal/`. The Lake package name remains
`collatz-dual-formal` until the next Lean/Mathlib bump (renaming it
churns the lockfile and CI cache).

`formal/Automata/` is still a placeholder only; do not invent proofs there.

Build:

```powershell
cd formal
lake build
```

The project contains no `sorry` or `admit`.

## Namespace map

| Path | Role | Compatibility re-export |
|----------|------|-------------------------|
| `Core/Basic.lean` | eventually-constant / bounded | `CollatzDual.Basic` |
| `Representation/Words.lean` | BT digit-list algebra from Warp | used by `CollatzDual.Warp` |
| `Operators/Operators.lean` | `S`, `N`, `W∘S=W` | `CollatzDual.Operators` |
| `Operators/DigitDerivative.lean` | `D∘S=id` | `CollatzDual.DigitDerivative` |
| `Operators/Algebra.lean` | composed identities, `W(3)=1` | `CollatzDual.OperatorAlgebra` |
| `Operators/Polynomial.lean` | `P(3)=evalMSD` | `CollatzDual.Polynomial` |
| `Problems/Collatz/*` | lift, cylinders, endpoint, center, cycles, … | matching `CollatzDual.*` |
| `BTCalculus/` | trit algebra, `D`/`I_a`, product/sum rules, `cmp3`/`select3`, rewrite soundness, coefficient normalization, section derivative, jets, residual `≡_k`, cascade composition, polynomial function congruence modulo `3^k`, cubic residual Newton image, fibres, deepest-layer criteria, the first intermediate layer `m=k-2`, the depth-deficit `N2` visibility law, the general `N1` valuation stratification, the two-regime `N0` scaling, the mismatched-width cubic quotient, and the `Q` one-family obstruction | none |
| `Automata/` | placeholder only | no invented proofs |

[`formal/CollatzDual.lean`](../../formal/CollatzDual.lean) remains the
default Lake target and continues to import the compatibility modules.

Generic theorems stay out of problem namespaces. Collatz-only theorems
stay under `Problems/Collatz`.

See [formal/README.md](../../formal/README.md) for the theorem inventory.
