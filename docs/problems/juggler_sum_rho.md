# Juggler global sum-\(\rho\) / word-statistics

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1.

## Problem

After the residual-future CLOSE, the leftover object C is a global
bound on accumulated local floor remainders in
\((n,\text{word statistics})\). Does the *naive* path sum of the
existing \(\rho\) admit such a bound, or is it irreducibly
state-dependent?

Do not invent a new \(\rho\). Do not reopen residual quotients or
PE-factor grammar.

## Exact statement

The existing local remainder is

\[
\rho(x)=
\begin{cases}
x-T(x)^2 & x\text{ even},\\
x^3-T(x)^2 & x\text{ odd}.
\end{cases}
\]

This is `local_defect` / Lean `branchDefect`. For a realized word
\(w\) of length \(k\),

\[
\mathrm{Rho}(w,n)=\sum_{i=0}^{k-1}\rho(x_i)
\]

is Lean `pathDefectSum`. It is **not** the weighted global defect

\[
\Delta_w(n)=n^{3^{\#O(w)}}-T_w(n)^{2^k}.
\]

Phase-0 asks whether any of H1–H4 holds on a stated window, whether
the known path identity is the only telescope, and whether every
useful comparison reduces to \(\Delta\) or \(T_w(n)<n\).

This says nothing about totality.

## Current literature

- Local remainders — **EXACT — LEAN VERIFIED** (`localDefectEven` /
  `Odd`, `branchDefect`).
- Naive path sum `pathDefectSum` and
  `pathPows = pathNextSquares + pathDefectSum` —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.Cycles`.
- Weighted \(\Delta\) recurrence, composition, \(\Delta=0\) rigidity —
  **EXACT — LEAN VERIFIED** in `Problems.Juggler.GlobalDefect`.
  Promoted; not reopened as a new object.
- First-defect Amplify — **EXACT — LEAN VERIFIED**. Does not beat
  surplus on expanding `OOE`.
- \(R=\Delta/S\) and forced residual drift —
  **CLOSE** / **REFUTED** as an independent attack
  (`juggler_normalized_defect.md`).
- \(\Delta>\) surplus on expanding mixed prefixes —
  **REFUTED** (equivalent to \(T_w(n)<n\)).
- Residual future-quotient — **CLOSE** as `FUTURE_QUOTIENT_REPACK`.
- PE-factor / word language — **CLOSE** as
  `JUGGLER_LANGUAGE_IS_KNOWN_GRAMMAR`.

Project relationship: **extended** (object C after the residual-state
CLOSE). Totality remains unclaimed.

## Branch budget

```text
Mathematical target     Does pathDefectSum admit a word-statistics
                        bound in (n, k, o, runs) that is not a
                        rewrite of Δ or T_w(n)<n?
Novelty hypothesis      H1–H3 survive, or a new telescope A(x)-A(T(x))
                        controls the sum, or Δ vs Rho is a useful
                        non-circular contraction law.
Falsifier               H1–H3 fail by small exact pairs; the only
                        telescope is the known pathPows identity;
                        H4 reduces to T<n; same (k,o) Rho is
                        state-dependent.
Existing machinery      local_defect, pathDefectSum, globalDefect,
                        powGap, envelope slack, itinerary_word
Maximum Phase-0 scope   n<=4000 itineraries, k<=20 with a bit cap;
                        HARD_PROBES + known PE starts; H1–H4;
                        no GPU, no new atlas table, no Lean, no
                        first-return induction.
Promotion criterion     A bound that is not Δ, not T<n, not 2^k>3^o,
                        and not the known path identity.
Stop criterion          RHO_COMPLEX; another scalar; residual
                        quotient; PE-factor; halt; GPU census.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(\rho=\) `local_defect` — **EXACT — LEAN VERIFIED** (existing)
- \(\mathrm{Rho}=\) `pathDefectSum` — **EXACT — LEAN VERIFIED**
  (existing; not a new \(\rho\))
- \(\mathrm{Rho}(uv,n)=\mathrm{Rho}(u,n)+\mathrm{Rho}(v,T_u(n))\) —
  definition / existing additivity
- \(\mathrm{Rho}=\sum x_i^{e_i}-\sum T(x_i)^2\) —
  **EXACT — LEAN VERIFIED**
- H1–H4 — Phase-0 tests
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.sum_rho`
- Records: [juggler_sum_rho.md](../research/juggler_sum_rho.md),
  [juggler_sum_rho.json](../research/juggler_sum_rho.json)
- Dataset: `data/research/juggler/sum_rho/`
- Tests: `tests/research/juggler_sequence/test_sum_rho.py`

No new census. No `RHO_RECORD` atlas table in Phase-0.

## Conjectures

None opened.

## Counterexamples

Filled after the Phase-0 run.

## Formalization

None added. Existing `pathDefectSum` / `globalDefect` stay unchanged.
No `sorry`.

## Results

Filled after the Phase-0 run.

## Open questions

Filled after the Phase-0 run.

## Decision

Filled after the Phase-0 run.

## Publication assessment

Status: `EXPLORATORY`.
