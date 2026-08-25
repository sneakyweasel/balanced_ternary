# Multiplicative residual universality

Status: **STRUCTURAL**

A single controlled extension of the signed-digit residual family.
The question is whether residual dynamics depend on the algebraic
source of a raw contribution, or only on the attainable raw alphabet.

CLI `btlab research analyze multiplicative_residual` (aliases `mr`,
`mul_residual`). It does not reopen Collatz, primes, T/jets, Ostrowski,
or a general multiplication project.

## Problem

For `s'=λ·D(s+d_1 d_2)` with trit pairs as controls, does the
control-level system factor exactly through the raw product map
`h(d_1,d_2)=d_1 d_2`, and is it dynamically the same as `F_{λ,U_1}`?

## Exact statement

Let `h:C→U` be a raw-contribution map on a finite control alphabet.
If the transition is `F(s,c)=λ·D(s+h(c))` and the output is
`lsd(s+h(c))`, then `F(s,c)=\bar F(s,h(c))` with
`\bar F(s,u)=λ·D(s+u)`. For trit product, `h(Trit²)⊆ Trit={-1,0,1}`,
so origin-reachable residual equals `F_{λ,U_1}={0}` for `λ∈{1,2,3}`.

## Current literature

- Trits are closed under multiplication: `KNOWN`.
- `lsd(xy)=lsd(x)lsd(y)` is already `EXACT — LEAN VERIFIED` (`lsdZ_mul`).
- Signed-digit residual `C(λ,U_m)` is the previous laboratory theorem.
- This branch extends that law from additive `h` to product `h`.
  Avizienis remains `KNOWN` and is not restated.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** does residual dynamics of `λ·D(s+u)` depend on how `u` is
  generated, or only on the attainable raw set `U`?
- **Novelty hypothesis:** control syntax is redundant after the raw
  contribution quotient; product of trits matches `U_1`, not addition.
- **Falsifier:** equal raw products with different residual/output
  behaviour; or 2-factor vs 3-factor residuals differ; or a 3-state
  origin residual for trit product.
- **Existing machinery:** `signed_step`, `D`/`lsd`, `lsdZ_mul`,
  `SignedDigitResidualSpec` pair-control pattern from D-add, Mealy.
- **Maximum Phase-0 scope:** 2-trit product at `λ∈{1,2,3}`; 3-trit
  product; one richer product `u=2 d_1 d_2` (existing doubled-trit
  coefficient); exact quotient; Lean of the factor theorem.
- **Promotion criterion:** exact factor-through-`h` theorem with
  matching/refuting witnesses, not merely equal state counts.
- **Stop criterion:** tautological restatement of `u=d_1 d_2` with no
  quotient analysis; or a general multiplication project.

## Balanced-ternary formulation

Controls are trit pairs. Raw contribution is ordinary integer
multiplication, the same local factor as `lsd(xy)`. The residual step
is existing `signed_step(s, scale·∏d_i, λ)`. Scale `2` is the doubled
trit coefficient, not a new digit.

## Why BT may be relevant

Addition of trits enlarges `U`. Multiplication of trits does not.
That contrast tests whether residual complexity follows operator
syntax or only `U`.

## Candidate operations / invariants

- `h(d_1,d_2)=d_1 d_2` with 9 pairs and image `{-1,0,1}`. **EXACT —
  LEAN VERIFIED**
- `F(s,(d_1,d_2))=F_{λ,U}(s,h(d_1,d_2))`. **EXACT — LEAN VERIFIED**
- Origin residual of 2-trit product is `{0}` for `λ∈{1,2,3}`. **EXACT
  — LEAN VERIFIED**
- 3-trit product has a different residual. **REFUTED**
- 3 origin-reachable residual states. **REFUTED** (size 1, matching
  `U_1`)
- Equal-raw separator. **REFUTED** (no witness on `s∈[-8,8]`; the
  identity `F(s,c)=\bar F(s,h(c))` forbids one)
- Doubled product `u=2 d_1 d_2` has image `{-2,0,2}` and follows that
  alphabet, including `λ=3` escape `s_n=3n`. **EXACT — LEAN VERIFIED**
  for the factor; unbounded witness **EXACT — LEAN VERIFIED** via
  existing `carryGain3`.

## Experiments

- `btlab research analyze|attack|reproduce|report multiplicative_residual`
  (aliases `mr`, `mul_residual`)
- Tests in
  `tests/research/multiplicative_residual/test_multiplicative_residual.py`
- Records in `experiments/balanced_ternary/multiplicative_residual/`

Default planner: 2-trit product, `λ=1`, `scale=1`.

## Conjectures

None opened.

## Counterexamples

- “Three residual states at the origin”: reachable `{0}`, Mealy 1.
- “Number of multiplicative factors changes residual”: 2-trit and
  3-trit both `{0}`.
- “Product syntax determines the phase independently of `U`”:
  `2 d_1 d_2` at `λ=3` is unbounded, matching `U={-2,0,2}` not
  “product of two trits”.

## Formalization

`formal/Problems/BalancedTernary/MultiplicativeResidual.lean`. Reuses
`signedNext` and `origin_trit_forcing`. Does not repeat `D_mul`. No
`sorry`.

## Results

Quotient stack for 2-trit product, `λ∈{1,2,3}`:

```text
9 product controls
→ 3 raw contributions {-1,0,1}
→ 1 origin-reachable residual {0}
→ 1 Mealy state
→ 3 control-output classes at 0 (the fibers of h)
```

| Source | Raw `U` | Origin residual |
|--------|---------|-----------------|
| one trit | `{-1,0,1}` | `{0}` |
| product of 2 trits | `{-1,0,1}` | `{0}` |
| product of 3 trits | `{-1,0,1}` | `{0}` |
| sum of 2 trits | `{-2,…,2}` | `{-1,0,1}` |
| `2 d_1 d_2` | `{-2,0,2}` | `{-1,0,1}` at `λ=1`; unbounded at `λ=3` |

Universality holds under the stated hypotheses: single integer residual,
output `lsd(s+h(c))`, independently legal controls. It would fail if
control identity were an extra output or if legality depended on the
decomposition.

## Open questions

None opened. Do not auto-start a general balanced-ternary multiplication
project.

## Decision

`PROMOTE` the exact factor-through-raw theorem: residual dynamics of
this family depend on `h(C)`, not on the expression that generates
`u`. Trit products add control redundancy but no residual complexity.
The doubled-product perturbation shows that a larger raw alphabet, not
the product shape, restores the signed-digit phase transition. Trit
closure under multiplication is `KNOWN`; the promoted content is the
quotient analysis against addition.

Best next question: does universality survive when the output includes
the raw control pair, not only `lsd(s+h(c))`?

## Publication assessment

Status: `STRUCTURAL`. Exact factorisation is a laboratory classification
lemma, not a `PAPER_CANDIDATE`. The arithmetic of trit products is
`KNOWN`.
