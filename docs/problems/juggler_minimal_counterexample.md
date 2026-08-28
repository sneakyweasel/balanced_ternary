# Juggler minimal counterexample and well-ordering

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1.

## Problem

If a bad Juggler state existed, what would the smallest such state be
forced to look like, and can exact predecessor closure or trajectory
barriers make that state impossible?

## Exact statement

Let `Bad(n)` mean `¬ReachesOne n`. Assume a bad state exists and let
`n*` be least. Then every positive `m < n*` is `Good`, the orbit of
`n*` never enters `[1, n*-1]`, and `n*` lies outside the predecessor
closure of every finite good set generated from states `< n*`. Decide
whether this well-ordering constraint plus exact inverse cells yields
a new reduction, or only the tautology that a minimal bad orbit cannot
visit a smaller bad state.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Existing `MinimalNonTerm` normal form — **EXACT — LEAN VERIFIED**.
- Even-run scale barrier `n^{2^r} ≤ m` —
  **EXACT — LEAN VERIFIED** (`juggler_even_scale_barrier`).
- `ReachesOne` closure along images —
  **EXACT — LEAN VERIFIED**.

Project relationship: **independent** as a well-ordering question;
the closure experiment is a **REPARAMETERIZATION** of `ReachesOne`.
Totality remains unclaimed.

## Branch budget

```text
Mathematical target     Does minimality plus predecessor closure give
                        a new reduction, or only the barrier tautology?
Novelty hypothesis      Well-ordering plus inverse cells yields an
                        inductive coverage law or a forbidden block family
Falsifier               PredClosure ↔ ReachesOne; U(B) not sparse;
                        no F(r) recurrence
Existing machinery      ReachesOne, MinimalNonTerm, even/odd cells,
                        floor_power, even_run_scale_barrier
Maximum Phase-0 scope   N≤4000, depth≤12, two-step barriers,
                        Lean PredClosure ↔ ReachesOne
Promotion criterion     A new exclusion theorem or a proved coverage law
Stop criterion          MINIMALITY_COMPLEX; tautology only
```

## Balanced-ternary formulation

Optional coordinate on uncovered minima. No forced BT law.

## Why BT may be relevant

A closure boundary of the form `(3^k ± 1)/2`, or an lsd cylinder of
uncovered states, would have been a BT observation. Neither appeared.

## Candidate operations / invariants

- `Good` / `Bad` as `ReachesOne` / its negation —
  **EXACT — LEAN VERIFIED**
- `good_of_good_successor` —
  **EXACT — LEAN VERIFIED**
- `PredClosure ↔ ReachesOne` —
  **EXACT — LEAN VERIFIED**. **REPARAMETERIZATION**
- `U(B)` = odds `> B` plus evens `≥ (B+1)^2` —
  **EXACT — LEAN VERIFIED**
- two-step barrier identities —
  **EXACT — LEAN VERIFIED**
- window-restricted `G_r` equals the inverse basin of `1` in
  `[1, 4000]` — **COMPUTATIONALLY VERIFIED**
- `G_r = {n : τ(n) ≤ r}` on `n ≤ 4000` —
  **REFUTED** (`25`, `9` at small `N`)
- interval closure / sparse `U(B)` / new induction —
  **REFUTED**
- `Bad_H = Bad` —
  **REFUTED**
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.minimal_counterexample`
- Records: [juggler_minimal_counterexample.md](../research/juggler_minimal_counterexample.md),
  [juggler_minimal_counterexample.json](../research/juggler_minimal_counterexample.json)
- Data: `data/research/juggler/minimal_counterexample/`
- Tests: `tests/research/juggler_sequence/test_minimal_counterexample.py`
- The Research Engine control layer is not modified.

## Conjectures

None opened.

## Counterexamples

- “Predecessor closure from `{1}` is a new induction.” **REFUTED**:
  `PredClosure ↔ ReachesOne`.
- “`U(B)` is arithmetically sparse.” **REFUTED**: density tends to
  `1/2`.
- “`G_r` is a single interval.” **REFUTED**: at depth
  `12` there are `1540` components.
- “A visit `≥ n*` is automatically good.” **REFUTED**: only a visit
  `< n*` reduces.
- “`Bad_H` is `Bad`.” **REFUTED** by definition.
- “Finite-`N` closure is the stopping-time filtration.” **REFUTED**:
  `25 → 125 → 1397 → 52214` leaves `[1, 4000]`.

## Formalization

`formal/Problems/Juggler/MinimalClosure.lean`. No `sorry`. Existing
`Minimal.lean` lemmas are reused, not restated as new obstructions.

## Results

See [juggler_minimal_counterexample.md](../research/juggler_minimal_counterexample.md).
Classification **MINIMALITY_COMPLEX**.

## Open questions

Whether every positive integer reaches 1. Well-ordering alone does not
answer it.

## Decision

**CLOSE**. Unbounded predecessor closure from {1} is ReachesOne. The finite-N experiment is the inverse basin of 1 inside [1, N], which is strictly smaller than {n : τ(n) ≤ r} because high-peak orbits leave the window. U(B) is all odds > B together with evens >= (B+1)^2, so it is not sparse. Two-step barriers are floor-sqrt identities. No interval-growth recurrence and no contradiction to a minimal bad state appear. All promoted-looking identities are
either already in `Minimal.lean` or a reparameterization of
`ReachesOne`. A branch whose surviving statements are `KNOWN` or
`REPARAMETERIZATION` is a `CLOSE`.

Best next question: none from this branch. Do not launch Phase 1.

## Publication assessment

Status: `ARCHIVED`.

The well-ordering reduction is the classical minimal-counterexample
setup. The predecessor-closure experiment identifies that construction
with the existing `ReachesOne` predicate. There is no new theorem
beyond packaging, and no paper distinction.
