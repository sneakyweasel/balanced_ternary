# Juggler survival-set inverse mass

Status: **EXPLORATORY**

Standalone application phase on the Juggler floor-power map. It is
**not** a Research Engine control-layer experiment, not a reopen of
survivor-phase histograms, prefix cylinders, excursion transfer,
backward-geometry rank, preimage cylinders, or the Terras program,
not a new atlas language tag, not an ergodic theorem, not Paper A,
and not a claim that every positive integer reaches 1.

Individual long survivors look generic. This phase measures a
different object: the population \(B_k(N;X)\) of all integers in
a window that stay at least \(N\) for \(k\) steps, and whether
that set contracts under inverse iteration in a way that is not
already even-step `FiniteProgress`.

## Problem

For a fixed anchor \(N\), does the set of integers whose first
\(k\) iterates remain at least \(N\) undergo a genuine global
contraction under repeated Juggler preimages, and can that
contraction be strengthened from a density statement to an
arithmetic statement that excludes a single infinite survivor?

## Exact statement

\[
B_k(N)=\{n\ge N:T^j(n)\ge N\text{ for all }0\le j\le k\},
\qquad
B_k(N;X)=B_k(N)\cap[N,X].
\]

The recursion \(B_{k+1}(N)=[N,\infty)\cap T^{-1}(B_k(N))\) is
exact on unbounded sets. Windowed counts use a forward
\(\tau_N\) census, because \(T(n)\) may leave \([N,X]\).

Phase 0 computes \(S_k=|B_k(N;X)|\), ratios
\(R_k=S_{k+1}/S_k\), densities \(S_k/(X-N+1)\), even/odd
inverse mass, and a few weights \(x^{-\theta}\) on several
anchors and scaled windows.

A density decay is not emptiness. \(\mu(B_\infty)=0\) does not
imply \(B_\infty=\varnothing\). Absence under a bound is
`NOT OBSERVED WITHIN SEARCH BOUND`. This is not a halt theorem.

## Current literature

- Even starts contract —
  **EXACT — LEAN VERIFIED** (`even_word_contracts`)
- Odd-to-even two-step descent —
  **EXACT — LEAN VERIFIED**
- Progress coverage leftover is odd-to-odd —
  **PROMOTE**
  ([juggler_progress_coverage.md](juggler_progress_coverage.md))
- Repeated inversion adds no extra rank —
  **CLOSE**
  ([juggler_backward_geometry.md](juggler_backward_geometry.md))
- One-word cylinders —
  **CLOSE** as `ANCHOR_CYLINDER_CLOSED`
- Survivor rounding phase —
  **CLOSE** as `SURVIVOR_PHASE_CLOSED`
- Excursion transfer —
  **CLOSE** as `EXCURSION_TRANSFER_CLOSED`
- Stopping-time prefix / OEIS A007320 — **known**; totality
  is not claimed
- Cube cell without a square cell — a **separate** leftover
- Every start reaches 1 — not claimed

Project relationship: **extended**. The designated
population-level diagnostic after the local/mesoscopic closes.

## Branch budget

```text
Mathematical target     For several N and scaled X, does
                        S_{k+1}/S_k admit a stable rho<1
                        (or a weighted mu) that is not the
                        even leak, and that can become an
                        arithmetic emptiness statement?
Novelty hypothesis      The survivor population cannot
                        sustain itself under T^{-1} even
                        though individuals look generic.
Falsifier               R_k -> 1 or exceeds 1 after scaling;
                        density grows with X; only even
                        FiniteProgress leaks; weights fail;
                        core stays macroscopic.
Existing machinery      floor_power; even_cell; pred_odd;
                        even_word_contracts; progress
                        coverage; stopping_times
Maximum Phase-0 scope   Forward tau_N census; several N;
                        X,2X,4X; even/odd inverse mass;
                        three weights; no Lean, no invariant
                        measure, no Terras reopen.
Promotion criterion     Uniform rho<1, or a finite core,
                        not equivalent to even contraction.
Stop criterion          Scale artefact; only density; only
                        the even leak; no route to emptiness.
```

## Balanced-ternary formulation

None required. The map is on ordinary positive integers.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(B_{k+1}=[N,\infty)\cap T^{-1}(B_k)\) —
  **KNOWN** as set algebra
- Even leak \(n<N^2\Rightarrow T(n)<N\) —
  **EXACT — LEAN VERIFIED** (`even_word_contracts`)
- \(S_k\), \(R_k\), densities, weights —
  **COMPUTATIONALLY VERIFIED** as a bounded observation
- Uniform \(\rho<1\) inverse contraction — tested in Phase 0
- Finite survivor core — tested in Phase 0
- Global halt — not claimed

## Experiments

- Probe: `research.juggler_sequence.survival_set`
- Records: [juggler_survival_set.md](../research/juggler_survival_set.md),
  [juggler_survival_set.json](../research/juggler_survival_set.json)
- Dataset: `data/research/juggler/survival_sets/`
- Tests: `tests/research/juggler_sequence/test_survival_set.py`

Science window: anchors \(2,3,5,10,50,100,1000\); windows
up to a few million; \(k\le 40\). Tests use \(X\le 200\),
\(k\le 12\). No CLI. No Lean.

## Conjectures

None opened.

## Counterexamples

Recorded after the science window.

## Formalization

None added. Existing `even_word_contracts` and even/odd
cells already contain the identities. No `SurvivalSet.lean`.
No `sorry`. Paper A is unchanged.

## Results

Recorded after the science window. Classification is produced
by `survival_set.classify`.

## Open questions

Whether a population inverse-mass contraction exists that
can be upgraded from density to arithmetic emptiness.

## Decision

Pending the Phase-0 science window. The branch will end in
exactly one of PROMOTE, PARK, or CLOSE after the multi-anchor
survival-set census.

## Publication assessment

Status: `EXPLORATORY`. A bounded population census, not a paper
candidate and not a Juggler totality result.
