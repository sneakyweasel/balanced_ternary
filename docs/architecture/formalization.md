# Formalization architecture

Lean 4 + Mathlib lives under `formal/`. The Lake package name is
`balanced-ternary-formal`.

`formal/Automata/` is still a placeholder only; do not invent proofs there.

Build:

```powershell
cd formal
lake build
```

The project contains no `sorry` or `admit`.

## Namespace map

| Path | Role | Lean namespace |
|----------|------|----------------|
| `Core/Basic.lean` | eventually-constant / bounded | `Core.Basic` |
| `Representation/Words.lean` | BT digit-list algebra | `Representation.Words` |
| `Operators/Shift.lean` | `S`, `N`, `W∘S=W` | `Operators.Shift` |
| `Operators/DigitDerivative.lean` | `D∘S=id` | `Operators.DigitDerivative` |
| `Operators/Algebra.lean` | composed identities, `W(3)=1` | `Operators.Algebra` |
| `Operators/Polynomial.lean` | `P(3)=evalMSD` | `Operators.Polynomial` |
| `Problems/Engine/PiecewiseCensus.lean` | hidden congruence identities | `Problems.Engine` |
| `Problems/Engine/ParameterDomain.lean` | padic valuation iff | `Problems.Engine` |
| `Problems/Engine/ControlWord.lean` | cleared affine composition / cycle constraint | `Problems.Engine` |
| `Problems/Engine/ControlObstruction.lean` | integer cycle-constraint obstructions | `Problems.Engine` |
| `Problems/Collatz/*` | lift, cylinders, endpoint, center, cycles, … | `Problems.Collatz` |
| `Problems/Juggler/*` | one-way Juggler layers: dynamics, words, first-passage, certificates, leaves | `Problems.Juggler` |
| `BTCalculus/` | trit algebra, `D`/`I_a`, product/sum rules, `cmp3`/`select3`, rewrite soundness, coefficient normalization, section derivative, jets, residual `≡_k`, cascade composition, polynomial function congruence modulo `3^k`, cubic residual Newton image, fibres, deepest-layer criteria, the first intermediate layer `m=k-2`, the depth-deficit `N2` visibility law, the general `N1` valuation stratification, the two-regime `N0` scaling, the mismatched-width cubic quotient, and the `Q` one-family obstruction | `BTCalculus` |
| `Automata/` | placeholder only | no invented proofs |

Default Lake targets are `BTCalculus` and `Problems`. Namespaces match their modules.

Generic theorems stay out of problem namespaces. Collatz-only theorems
stay under `Problems/Collatz`.

See [formal/README.md](../../formal/README.md) for the theorem inventory.
