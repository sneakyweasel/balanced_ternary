# Signed-digit residual phase transitions

Status: **STRUCTURAL**

This phase asks whether doubled-trit normalization, streaming
`D(x+y)`, bound-2 widening, and the synthetic `λ=3` escape are one
residual family, and what exact condition separates finite from
unbounded origin-reachable dynamics.

CLI `btlab research analyze signed_digit_residual` (alias `sdr`) is
this adapter. It does not reopen Collatz, primes, T/jets, or Ostrowski.

## Problem

For residual systems `F_{λ,U}(s,u)=λ·D(s+u)` with finite raw alphabet
`U`, when is the origin-reachable residual finite, what is the exact
closure, and what is the minimal state count?

## Exact statement

Write `D(n)=(n-lsd(n))/3` with `lsd(n)∈{-1,0,+1}`. For
`U_m={-m,...,m}` and gain `λ∈{1,2,3}`, start at `s=0`. The
origin-reachable set is finite if and only if `λ≤2` or `m≤1`. For
`λ=1` it equals `[-⌊m/2⌋,⌊m/2⌋]`. r-way trit addition
`s'=D(s+a_1+⋯+a_r)` is the same map on `U_r`, with
`M(r)=2⌊r/2⌋+1`.

## Current literature

- Finite signed-digit adders are `KNOWN` (`avizienis-1961-signed-digit`).
- Doubled-trit closure, `D(x+y)` residual, and `λ=3` escape on `u=2d`
  are already in this laboratory (`BTN-doubled-*`, `BTN-dadd-*`,
  `BTN-carry-gain-3`).
- This branch `extended` those cases to one `DZ`-family and `refuted`
  the scalar test “`λ=3` iff infinite”. The finite/infinite law for
  `λ·D(s+u)` is `PROJECT-SPECIFIC`. Carry existence is not new.

## Branch budget

Written before substantial implementation. See
[methodology.md](../methodology.md).

- **Target:** for radix-3 maps `F_{λ,U}(s,u)=λ·D(s+u)` with finite `U`,
  when is the residual dynamics finite, what is the exact reachable
  closure, and what is the minimal state count?
- **Novelty hypothesis:** doubled-trit, D-add, bound-2 widening, and
  `λ=3` escape are one family. Finiteness is not a scalar `λ/3` test.
  Reachable set, invariant box, and Mealy size can differ. r-way trit
  addition has an exact `M(r)`.
- **Falsifier:** every natural `C(λ,U)` fails on a small witness; or
  all exact statements are Avizienis/KNOWN reparameterizations with no
  new finite/infinite law.
- **Existing machinery:** `D`/`lsd`, `DZ_carry_bound`, doubled-trit and
  D-add specs, `ExhaustiveClosureAttack`, Mealy minimization.
- **Maximum Phase-0 scope:** `F_{1,U_m}` for `m=1,2,3`; distinguishing
  pairs `(1,1),(1,2),(1,3),(2,1),(2,2),(3,1)` plus infinite companion
  `(3,2)`; r-way for `r=1..4`; one perturbation; Lean of the strongest
  statement.
- **Promotion criterion:** exact `C(λ,U)` or exact `M(r)` with Lean of
  the strongest piece and an explicit infinite witness.
- **Stop criterion:** all statements `KNOWN`/`REPARAMETERIZATION`; or
  the boundary is real but no short `C` appears; or machinery gravity.

## Balanced-ternary formulation

The step is existing `D` and `lsd` of the integer `s+u`. Controls are
`U_m` or r-tuples of trits. Gain `λ` is a synthetic multiplier on `D`,
not a second digit model.

## Why BT may be relevant

Radix-3 balanced division is the laboratory's carry. The question is
whether a single residual map classifies the earlier finite-state
discoveries.

## Candidate operations / invariants

- `V(s)=|s|` for `λ=1` outside `|s|>⌊m/2⌋`. **EXACT — LEAN VERIFIED**
- Origin-reachable radius `⌊m/2⌋` at `λ=1`. **EXACT — LEAN VERIFIED**
- Loose box `⌈(m+1)/2⌉` from `3|D n|≤|n|+1`. Not sharp; **REFUTED** as
  the optimal radius (`m=2` closes at `1`, not `2`).
- Scalar test: finite iff `λ<3`. **REFUTED** (`F_{3,U_1}` stays at `0`).
- `(3,2)` constant `u=2` gives `s_n=3n`. **EXACT — LEAN VERIFIED**
  (existing `carryGain3`).
- `(2,2)` reachable `{-2,0,2}` versus invariant interval `[-2,2]`.
  **COMPUTATIONALLY VERIFIED**
- r-way `M(r)=2⌊r/2⌋+1`. **EXACT — LEAN VERIFIED** for the box;
  Mealy count **COMPUTATIONALLY VERIFIED** for `r=1..4`.
- Asymmetric `U={0,1,2}` at `λ=1`: reachable `{0,1}`. **COMPUTATIONALLY
  VERIFIED**

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_residual`
  (alias `sdr`)
- Adapter tests in
  `tests/research/signed_digit_residual/test_signed_digit_residual.py`
- Records in `experiments/balanced_ternary/signed_digit_residual/`

Default planner system is `λ=1`, `U_2`. Distinguishing pairs are not a
parameter sweep.

## Conjectures

None opened.

## Counterexamples

- Scalar `λ=3` threshold: `F_{3,U_1}` has origin-reachable `{0}`.
- Loose invariant radius `⌈(m+1)/2⌉`: for `m=2` the box `[-1,1]` is
  already closed.
- Identifying the invariant interval with the reachable set: `(2,2)`
  reachable `{-2,0,2}` inside `[-2,2]`.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitResidual.lean`. Wraps
`carryGain3_unbounded`; does not repeat `doubledTrit_*` or `dAdd_*`.
No `sorry`.

## Results

Phase classification (origin-reachable, exact):

| `(λ,m)` | status | reachable | Mealy | notes |
|---------|--------|-----------|-------|-------|
| `(1,1)` | EXACT FINITE | `{0}` | 1 | trit alphabet |
| `(1,2)` | EXACT FINITE | `{-1,0,1}` | 3 | doubled-trit ⊂ `U_2`; binary addition |
| `(1,3)` | EXACT FINITE | `{-1,0,1}` | 3 | same box as `m=2` |
| `(2,1)` | EXACT FINITE | `{0}` | 1 | |
| `(2,2)` | EXACT FINITE | `{-2,0,2}` | 3 | interval `[-2,2]` is strictly larger |
| `(3,1)` | EXACT FINITE | `{0}` | 1 | kills scalar `λ=3` |
| `(3,2)` | EXACT INFINITE | — | — | `s_n=3n` on constant `u=2` |

r-way trit addition: `M(1)=1`, `M(2)=3`, `M(3)=3`, `M(4)=5`. Bound-2
two-stream D-add is raw `U_4`, hence five states. Asymmetric
`U={0,1,2}` at `λ=1` remains finite; symmetry of `U_m` is not
load-bearing.

`C(λ,U_m)` for `λ∈{1,2,3}`: origin-reachable residual is finite iff
`λ≤2` or `m≤1`.

## Open questions

None opened by this phase. Do not auto-start a general-radix theorem.

## Decision

`PROMOTE` the exact condition `C(λ,U_m)` for `λ∈{1,2,3}`, the sharp
`λ=1` radius `⌊m/2⌋`, the `(3,1)` refutation of a scalar gain
threshold, the `(2,2)` box/reachable distinction, and `M(r)=2⌊r/2⌋+1`
for r-way trit addition. Doubled-trit, binary addition, bound-2
widening, and the `λ=3` escape are special alphabets of one residual
map. Avizienis remains `KNOWN` for finite signed-digit adders; the
promoted content is the `D`-dynamics law.

Best next question: does the same threshold survive when the raw
contribution is a product of trits rather than a sum?

## Publication assessment

Status: `STRUCTURAL`. Exact theorems exist and unify prior laboratory
cases. This is not a `PAPER_CANDIDATE`: carry-bounded signed-digit
addition is `KNOWN`, and the new finite/infinite law is a laboratory
classification rather than a literature-facing arithmetic theorem.
