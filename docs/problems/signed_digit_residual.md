# Signed-digit residual phase transitions

Status: **STRUCTURAL**

Classification of the residual map `F_{λ,U}(s,u)=λ·D(s+u)` by gain and
raw-contribution alphabet. Finite signed-digit adders remain `KNOWN`.
The laboratory object is the exact finite/infinite law for this
dynamical system, not the existence of a carry transducer.

CLI `btlab research analyze signed_digit_residual` (alias `sdr`).
It does not reopen Collatz, primes, T/jets, Ostrowski, or a general
multiplication project.

## Problem

For residual systems `F_{λ,U}(s,u)=λ·D(s+u)` with finite raw alphabet
`U`, when is the origin-reachable residual finite, what is the exact
closure, and what is the minimal state count?

## Exact statement

Write `D(n)=(n-lsd(n))/3` with `lsd(n)∈{-1,0,+1}`. For integer `λ≥1`
and finite `U⊂ℤ`, start at `s=0`. The origin-reachable set is finite
if and only if

```text
λ ≤ 2  or  max_{u∈U} |u| ≤ 1.
```

For the symmetric family `U_m={-m,...,m}` this is `λ≤2` or `m≤1`.
At `λ=3` the step is `s'=s+u-lsd(s+u)`, so any constant `|u|≥2`
escapes by at least 1 per iterate. At `λ≥4` the same constant control
is strictly expanding on the matching ray. For `λ=1` the sharp
invariant/reachable radius is `⌊m/2⌋`. For `λ=2` it is `2(m-1)_+`,
and origin-reachable states lie on `2ℤ`. r-way trit addition
`s'=D(s+a_1+⋯+a_r)` is the same map on `U_r`, with
`M(r)=2⌊r/2⌋+1`.

## Current literature

- Finite signed-digit adders and LSD-first conversion transducers are
  `KNOWN` (`avizienis-1961-signed-digit`; standard radix conversion
  FSTs with bounded carry states). Parallel addition in redundant
  numeration is `KNOWN`.
- Anashin's automata-finiteness criterion
  (`anashin-2012-automata-finiteness`) characterises 1-Lipschitz
  p-adic maps; it does not classify the synthetic-gain family
  `s↦λ D(s+u)`.
- Doubled-trit closure, `D(x+y)` residual, and `λ=3` escape on `u=2`
  are already in this laboratory (`BTN-doubled-*`, `BTN-dadd-*`,
  `BTN-carry-gain-3`).
- Product controls factor through raw `h` (`BTN-mr-factor-through-raw`).
- This branch `extended` those cases to one `DZ`-family and `refuted`
  the scalar test “`λ=3` iff infinite” and the claim that geometry of
  `U` controls the phase. Carry existence is not new. The
  finite/infinite law for all `λ≥1` is `PROJECT-SPECIFIC`
  (`NEW FORMULATION` of residual dynamics, not a new adder).

## Branch budget

Written before the first implementation. Theorem-phase budget follows.
See [methodology.md](../methodology.md).

- **Target:** exact finite/infinite classification of
  `F_{λ,U}(s,u)=λ·D(s+u)` from `(λ,U)`, including invariant radius,
  origin-reachable closure, and when geometry of `U` matters.
- **Novelty hypothesis:** the phase is a control-theoretic condition
  on `(λ, max|u|)`, not the scalar `λ/3` and not operator syntax.
- **Falsifier:** some `U` with `max|u|≥2` finite at `λ≥3`; or trit
  forcing infinite; or holes change the phase; or every exact
  statement is an Avizienis reparameterization.
- **Existing machinery:** `D`/`lsd`, `signed_step`,
  `SignedDigitResidualSpec`, exhaustive closure, Mealy,
  `origin_trit_forcing`, `carryGain3`.
- **Maximum Phase-0 / theorem-phase scope:** symmetric `U_m` for
  general `λ`; one sparse and one asymmetric alphabet; explicit
  escape; Lean of the iff; literature audit. No parameter grid.
- **Promotion criterion:** necessary-and-sufficient `C(λ,U)` with Lean
  of the finite box and an explicit unbounded family.
- **Stop criterion:** empirical phase diagram; or the result is only
  “signed-digit arithmetic is finite-state”; or machinery gravity.

## Balanced-ternary formulation

The step is existing `D` and `lsd` of the integer `s+u`. Controls are
letters of a finite raw alphabet. Gain `λ` is a synthetic multiplier
on `D`, not a second digit model.

## Why BT may be relevant

Radix-3 balanced division is the laboratory's carry. The question is
whether a single residual map classifies finite versus unbounded
normalization dynamics.

## Candidate operations / invariants

- `V(s)=|s|` for `λ=1` outside `|s|>⌊m/2⌋`. **EXACT — LEAN VERIFIED**
- Origin-reachable radius `⌊m/2⌋` at `λ=1`. **EXACT — LEAN VERIFIED**
- Sharp `λ=2` radius `2(m-1)_+`. **EXACT — LEAN VERIFIED**
- Loose box `⌈(m+1)/2⌉` from `3|D n|≤|n|+1`. Not sharp; **REFUTED** as
  the optimal `λ=1` radius (`m=2` closes at `1`, not `2`).
- Scalar test: finite iff `λ<3`. **REFUTED** (`F_{3,U_1}` stays at `0`).
- Geometry of `U` (holes, asymmetry) changes the finite/infinite
  phase at fixed `(λ, max|u|)`. **REFUTED**
- `M(λ,U)` is determined by `(λ, max|u|)` alone. **REFUTED**
  (`U={2}` at `λ=2` has Mealy 2; `U_2` has Mealy 3).
- `(3,2)` constant `u=2` gives `s_n=3n`. **EXACT — LEAN VERIFIED**
  (existing `carryGain3`; now any `|u|≥2`).
- `(2,2)` reachable `{-2,0,2}` versus invariant interval `[-2,2]`.
  **COMPUTATIONALLY VERIFIED**
- r-way `M(r)=2⌊r/2⌋+1`. **EXACT — LEAN VERIFIED** for the box;
  Mealy count **COMPUTATIONALLY VERIFIED** for `r=1..4`.
- Asymmetric `U={0,1,2}` at `λ=1`: reachable `{0,1}`. **COMPUTATIONALLY
  VERIFIED**
- Factorization `F(s,c)=λ·D(s+h(c))` when output is `lsd(s+h(c))`.
  **EXACT — LEAN VERIFIED** (`same_raw_same_residual`; product case
  already `product_factor_through_raw`).

## Experiments

- `btlab research analyze|attack|reproduce|report signed_digit_residual`
  (alias `sdr`)
- Adapter tests in
  `tests/research/signed_digit_residual/test_signed_digit_residual.py`
- Records in `experiments/balanced_ternary/signed_digit_residual/`

Default planner system is `λ=1`, `U_2`. Distinguishing pairs are not a
parameter sweep. Geometry check uses `{-2,0,2}`, `{0,1,2}`, and `{2}`.

## Conjectures

None opened.

## Counterexamples

- Scalar `λ=3` threshold: `F_{3,U_1}` has origin-reachable `{0}`.
- Loose invariant radius `⌈(m+1)/2⌉`: for `m=2` the box `[-1,1]` is
  already closed.
- Identifying the invariant interval with the reachable set: `(2,2)`
  reachable `{-2,0,2}` inside `[-2,2]`.
- Geometry controls the phase: `U={-2,0,2}` and `U={0,1,2}` have the
  same finite/infinite law as `U_2`.
- Max-abs determines Mealy size: `U={2}` versus `U_2` at `λ=2`.

## Formalization

`formal/Problems/BalancedTernary/SignedDigitResidual.lean`. Wraps
`carryGain3_unbounded`; does not repeat `doubledTrit_*` or `dAdd_*`.
No `sorry`. Named theorems: `origin_residual_box_iff`,
`signedIterate_unbounded_of_ge_three`, `lambda2_sharp_box`,
`same_raw_same_residual`.

## Results

Phase classification (origin-reachable, exact) for `U_m`:

| `(λ,m)` | status | reachable / witness | notes |
|---------|--------|---------------------|-------|
| `λ≤2` | EXACT FINITE | `λ=1`: `[-⌊m/2⌋,⌊m/2⌋]`; `λ=2`: `2ℤ∩[-2(m-1)_+, 2(m-1)_+]` | Level A box exists |
| `m≤1`, any `λ` | EXACT FINITE | `{0}` | trit forcing |
| `λ≥3`, `m≥2` | EXACT INFINITE | constant `u=m` | `λ=3`: increment; `λ≥4`: expansion |

Levels stay distinct:

- **A.** A finite invariant interval exists iff `λ≤2` or `m≤1`
  (`origin_residual_box_iff`).
- **B.** Origin-reachable is finite under the same condition, because
  `0` lies in the box, and is unbounded on the complementary side by
  an explicit constant word.
- **C.** Minimal Mealy size is not a function of `(λ, max|u|)` alone.

r-way trit addition: `M(1)=1`, `M(2)=3`, `M(3)=3`, `M(4)=5`. Bound-2
two-stream D-add is raw `U_4`, hence five states. Sparse `U={-2,0,2}`
matches `U_2` on the phase and, at `λ=1,2`, on the origin-reachable
set. Asymmetric `U={0,1,2}` remains finite at `λ=1,2` with a different
reachable set, and escapes at `λ=3`.

Universality of raw contribution: residual and `lsd` output factor
through `u=h(c)` whenever legality does not depend on the
decomposition. That fails if the output includes the raw control pair
or if future letters are constrained by previous ones.

## Open questions

None opened as conjectures. Best next question is recorded under
Decision. Do not auto-start a general-radix theorem.

## Decision

`PROMOTE` the exact condition `C(λ,U)`: origin-reachable residual of
`λ·D(s+u)` is finite iff `λ≤2` or `max|u|≤1`, with Lean of the
invariant-box iff for `U_m` and explicit constant-control escape for
every `λ≥3` and `|u|≥2`. The `λ=1` radius `⌊m/2⌋`, the sharp `λ=2`
radius `2(m-1)_+`, the `(3,1)` refutation of a scalar gain threshold,
the geometry/Mealy refutations, and `M(r)=2⌊r/2⌋+1` remain. Avizienis
stays `KNOWN` for finite signed-digit adders. The promoted content is
the residual-dynamics classification, not another carry automaton.

Best next question: can `M(λ,U)` be read as the origin-reachable
subset of `λℤ` inside the sharp invariant interval?

## Publication assessment

Status: `STRUCTURAL`. Exact theorems exist. This is not a
`PAPER_CANDIDATE`: carry-bounded signed-digit addition is `KNOWN`, and
the new finite/infinite law is a laboratory classification of a
synthetic-gain residual map rather than a literature-facing arithmetic
algorithm.
