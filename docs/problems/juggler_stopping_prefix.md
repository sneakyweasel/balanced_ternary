# Juggler stopping-time prefix

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment and not a claim that
every positive integer reaches 1. It does not reopen the closed
windowed inverse-basin census
([juggler_minimal_counterexample.md](juggler_minimal_counterexample.md)).

## Problem

Does the unbounded stopping-time prefix

\[
F_\tau(r)=\max\{N:\max_{n\le N}\tau(n)\le r\}
\]

admit an interval amplification lemma, or does it only invert the
running maximum of \(\tau\)?

## Exact statement

Let \(T\) be `floorPower`: even \(n\mapsto\lfloor\sqrt{n}\rfloor\), odd
\(n\mapsto\lfloor n^{3/2}\rfloor\). Write \(\tau(1)=0\) and
\(\tau(n)=\min\{k:T^k(n)=1\}\) when the minimum exists. Decide whether
there exist an explicit \(f\) with \(f(N)>N\) and a controlled \(k\)
such that

\[
[1,N]\subseteq\{\tau\le r\}
\implies
[1,f(N)]\subseteq\{\tau\le r+k\},
\]

or whether every prefix jump is the definitional event “the current
first gap \(b_r=F_\tau(r)+1\) finally satisfies \(\tau(b_r)=r+1\)”.

## Current literature

- OEIS A007320 (`oeis-A007320`): step counts to 1. **known**. Totality
  is not claimed.
- Windowed inverse-basin \(F(r)\) and \(G_r\) —
  **COMPUTATIONALLY VERIFIED**, branch **CLOSE**
  (`juggler_minimal_counterexample`).
- `PredClosure ↔ ReachesOne` — **EXACT — LEAN VERIFIED**.
  **REPARAMETERIZATION**.
- `even_good_of_sqrt_le`, `odd_not_pred_of_le` —
  **EXACT — LEAN VERIFIED**. One-step closure of \([1,B]\) adds no
  odd \(n>B\).
- Even cells are intervals \([m^2,(m+1)^2)\), not singletons on
  squares. The informal rule \(T(2k)=k^2\) is a forward/inverse swap
  and is not used.

Project relationship: **independent** of the windowed \(G_r\) census;
the object is the unbounded \(\tau\)-prefix. Totality remains
unclaimed.

## Branch budget

```text
Mathematical target     Does F_τ(r)=max{N : max_{n≤N} τ(n) ≤ r} admit
                        an interval amplification [1,N] ⊆ {τ≤r} ⇒
                        [1,f(N)] ⊆ {τ≤r+k} with explicit f(N)>N, or
                        does it only invert the running-max of τ?
Novelty hypothesis      The closed branch measured windowed inverse-basin
                        F(r) (frozen at 24). Unbounded F_τ is a different
                        sequence; a reusable odd-gap mechanism would be new.
Falsifier               F_τ is the definitional inverse of running-max τ;
                        first gaps are odd expanders with no bounded-k
                        route into [1,N]; plateaus dominate; no f besides
                        “wait until τ(b)”.
Existing machinery      floor_power; stopping_times; even_good_of_sqrt_le;
                        odd_not_pred_of_le; U(B) density 1/2; windowed
                        F(r) in good_closure.csv
Maximum Phase-0 scope   N=4000, existing horizon 10000; one F_τ table;
                        first-gap orbits; growth/plateau tests; decide
Promotion criterion     A candidate lemma that predicts the next prefix
                        jump without computing τ of that gap
Stop criterion          Definitional reparameterization of τ; stall /
                        linear envelope; no reusable odd mechanism
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

A first-gap cylinder in least significant trits, or a boundary of the
form \((3^k\pm 1)/2\), would have been a BT observation. Phase-0 does
not hunt a BT law.

## Candidate operations / invariants

- \(F_\tau(r)=\max\{N:M(N)\le r\}\) with \(M(N)=\max_{n\le N}\tau(n)\)
  — **REPARAMETERIZATION** of the running-max of \(\tau\) once
  computed
- finite-depth even cell: even \(n<(F+1)^2\) satisfies
  \(\tau(n)\le r+1\) when \([1,F]\subseteq\{\tau\le r\}\) —
  **OBSERVATION** (Lean unbounded form is `even_good_of_sqrt_le`)
- one-step odd coverage of \(n>F\) — **REFUTED** in the closed
  branch (`odd_not_pred_of_le`)
- interval amplification with explicit \(f(N)>N\) — **REFUTED**
  on the Phase-0 window
- \(F_\tau(r)\to\infty\) on a finite window — not a totality theorem
- global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.stopping_prefix`
- Records: [juggler_stopping_prefix.md](../research/juggler_stopping_prefix.md),
  [juggler_stopping_prefix.json](../research/juggler_stopping_prefix.json)
- Data: `data/research/juggler/stopping_prefix/`
- Tests: `tests/research/juggler_sequence/test_stopping_prefix.py`
- The Research Engine control layer is not modified.

## Conjectures

None opened.

## Counterexamples

- “\(F_\tau\) is a new inductive coverage law.” **REFUTED**: it is
  the inverse of the running-max of \(\tau\).
- “Unbounded and windowed prefixes coincide.” **REFUTED**: windowed
  `F(12)=24` while `F_τ(12)` is larger because `τ(25)` is finite.
- “A bounded number of predecessor layers covers the next interval.”
  **REFUTED**: odd first gaps have `T(b)` outside the previous prefix
  and no uniform `k≤8` entry. First-gap oddness
  `True`; plateau fraction
  `0.863`.

## Formalization

None added. Existing `even_good_of_sqrt_le` and `odd_not_pred_of_le`
in `formal/Problems/Juggler/MinimalClosure.lean` are cited, not
restated. No `GoodAt` / `GoodSet` module.

## Results

See [juggler_stopping_prefix.md](../research/juggler_stopping_prefix.md).
Classification **STOPPING_PREFIX_COMPLEX**.

## Open questions

Whether every positive integer reaches 1. A finite-window prefix
table does not answer it.

## Decision

**CLOSE**. F_τ is the definitional inverse of the running-max of τ. First gaps are odd expanders whose images leave the previous prefix; no uniform k≤4 entry exists. Plateaus cover 0.863 of depth steps. Window totality F_τ(max τ)=N is the already-recorded fact that every n≤4000 reaches 1, not a coverage theorem. A branch whose surviving statements
are `KNOWN` or `REPARAMETERIZATION` is a `CLOSE`.

Best next question: none from this branch. Do not launch Phase 1.

## Publication assessment

Status: `ARCHIVED`.

The prefix table inverts recorded stopping times on `n ≤ 4000`.
There is no new theorem beyond the already-packaged even-cell lemma,
and no paper distinction.
