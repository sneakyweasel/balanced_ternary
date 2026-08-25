# D/Add residual completion

Status: **STRUCTURAL**

When the unary rewrite calculus reaches `Add`, `D(x+y)` is not a
function of `(D(x),D(y))`. This phase asks the research engine to
discover the smallest residual that restores locality, without
installing a carry table into the adapter.

The unary non-locality theorem remains `add_not_DLocal` in
[rewrite_calculus.md](rewrite_calculus.md). This dossier does not
reopen that paper branch.

## Problem

What is the smallest residual `R` such that

```text
D(x+y) = F(D(x), D(y), R(x,y))
```

exactly on `ℤ`, and is the same residual sufficient for LSD-first
streaming addition?

## Exact statement

Write `x = 3 D(x) + lsd(x)` and `y = 3 D(y) + lsd(y)`. Then

```text
x+y = 3(D(x)+D(y)) + (lsd(x)+lsd(y)).
```

The naive factorization fails exactly when `|lsd(x)+lsd(y)|=2`, because
that local sum is not a trit. The discovered residual-aware rule is

```text
D(x+y) = D(x) + D(y) + D(lsd(x)+lsd(y)).
```

On the slice `D(x)=D(y)=0`, the observable `D(x+y)` takes three values
`{0,1,-1}`, so no 1-state or 2-state residual can repair locality.
`R = lsd(x+y)` is not sufficient: `(1,1)` and `(0,-1)` share
`(D,D,lsd(x+y))=(0,0,-1)` but `D(2)=1 ≠ D(-1)=0`.

Streaming step, using existing `D`/`lsd` rather than a lookup table:

```text
s' = D(s+a+b),    out = lsd(s+a+b).
```

For trit inputs the reachable residual set is exactly `{-1,0,1}`.
The diagonal `a=b` is Phase-0 doubled-trit normalization.

## Current literature

- `D(x+y) ≠ D(x)+D(y)` and `add_not_DLocal` are already in the rewrite
  calculus. `KNOWN` as the obstruction, not the residual.
- `D_add` / `addDigit` already express the standard carry table.
  The new algebraic form is `D(lsd x + lsd y)`, not a second carry
  invention.
- Finite signed-digit adders are `KNOWN`. The contribution is engine
  discovery of the minimal residual and the exact obstruction to
  `lsd(x+y)`.

## Branch budget

- **Target:** smallest `R` restoring locality of `D(x+y)`, with exact
  streaming closure.
- **Novelty hypothesis:** a 3-state residual, discovered from `D`/`lsd`
  semantics, is both necessary and sufficient, and equals the Phase-0
  mechanism on the diagonal.
- **Falsifier:** every natural finite `R` still collides, or the
  streaming residual is not the static correction.
- **Existing machinery:** `D`, `lsd`, `ProblemSpec`, exhaustive closure,
  Mealy, Phase-0 doubled-trit spec, `add_not_DLocal`, `D_add`.
- **Maximum Phase-0 scope:** candidate-residual search; one streaming
  spec; trit closure; bound-2 perturbation; Lean of the repaired rule
  and the `lsd(x+y)` refutation.
- **Promotion criterion:** algebraic residual, engine `EXACT` closure,
  Lean without `sorry`.
- **Stop criterion:** finite completion proved, or an exact obstruction
  to finite local state.

## Balanced-ternary formulation

Digits are existing trits. The adapter never reimplements
`rewrite_sum`; the step is `D` and `lsd` of the integer `s+a+b`.

## Why BT may be relevant

The unary calculus already isolates `Add` as the locality boundary.
The question is whether the engine finds the missing finite interface.

## Candidate operations / invariants

- `R = (lsd x, lsd y)` sufficient (9 raw pairs). **EXACT — LEAN VERIFIED**
  via the repaired rule, which depends only on that pair through
  `D(lsd x + lsd y)`.
- `R = lsd(x+y)`. **REFUTED** (`(1,1)` vs `(0,-1)`).
- Correction values `D(x+y)-D(x)-D(y) ∈ {-1,0,1}`. **EXACT — LEAN VERIFIED**
- Streaming residual box for trit inputs. **EXACT — LEAN VERIFIED**
- Bound-2 input alphabet: reachable box `{-2,...,2}`. **COMPUTATIONALLY VERIFIED**

## Experiments

- `btlab research analyze|attack|reproduce|report d_add`
- Adapter tests in `tests/research/balanced_ternary/test_d_add.py`
- Records in `experiments/balanced_ternary/d_add/`

## Conjectures

None opened.

## Counterexamples

- Unary factorization: `(0,0)` vs `(1,1)`. Already `add_not_DLocal`.
- `R = lsd(x+y)`: `(1,1)` vs `(0,-1)`.
- Bound 2: residual `2` is reachable, so the 3-state trit box is
  alphabet-specific.

## Formalization

`formal/Problems/BalancedTernary/DAddResidual.lean`. Does not repeat
`add_not_DLocal` or `D_add`. No `sorry`.

## Results

- Raw static encoding `(lsd x, lsd y)`: 9 pairs.
- Algebraic residual `D(lsd x + lsd y)`: 3 values, and 3 is minimal
  on the `D=0` fiber.
- Streaming reachable states (trit alphabet): 3. Next-output Mealy: 3.
- Bound-2 reachable states: 5. Mealy: 5.
- Coefficient-word addition and the residual transducer compute the
  same integer; the transducer is the local interface, the word is the
  global coefficient vector.
- Phase 0 is the diagonal `a=b` of the same step.

## Open questions

None opened by this phase. Do not auto-start multiplication.

## Decision

`PROMOTE` the discovered residual `D(lsd x + lsd y)`, the `lsd(x+y)`
refutation, exact trit closure, and the bound-2 widening. The unary
paper is unchanged.

Best next question: does the same `D(s + raw)` residual classify every
bounded signed-digit normalizer, or only addition-like sums?

## Publication assessment

Status: `STRUCTURAL`. This is not a `PAPER_CANDIDATE`. Carry existence
is `KNOWN`. The engine-discovered minimal completion of the unary/`Add`
boundary is project-specific structure.
