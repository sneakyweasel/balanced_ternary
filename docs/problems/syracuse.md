# Accelerated odd-only map (Syracuse engine stress test)

Status: **EXPLORATORY**

This module does **not** claim a proof or disproof of the Collatz conjecture.
It is a Research Engine v2 diagnosis benchmark. It does not reopen the parked
application [collatz.md](collatz.md) or the archived shortcut test
[collatz_finite_descent.md](collatz_finite_descent.md).

CLI `btlab research analyze|attack|reproduce|report syracuse`.

## Problem

Can v2 diagnose the structural language of the accelerated odd-only map

\[
S(n)=\frac{3n+1}{2^{v_2(3n+1)}}
\]

on positive odd integers without being told 2-adic structure, and without
claiming a Collatz solution?

## Exact statement

On \(\mathbb{Z}_{>0}^{\mathrm{odd}}\), with dummy control and identity
observation, does the generic diagnosis layer classify \(S\) as another
finite-contracting digit-fold regime, or as a different dynamical class?
Which exact constraints (if any) do generic attacks certify?

## Current literature

- Accelerated \(T\) well-defined on positive odds: ledger `C-T-welldefined`,
  Lean `acceleratedT`. **KNOWN** (engine rediscovery of the definition).
- Parked four-coordinate dictionary: [collatz.md](collatz.md),
  [collatz_mathematics.md](../collatz_mathematics.md). **KNOWN**. The
  novelty hypothesis that BT observables of the realizer \(R\) are
  independent of \(R\) is **REFUTED** (`H_BT_independence`). Do not re-test.
- Shortcut map engine test: [collatz_finite_descent.md](collatz_finite_descent.md)
  **CLOSE**. Different map (parity controls, even states).
- `lagarias-2010-3x+1-survey`: survey of the \(3x+1\) problem. **KNOWN**.
- `terras-1976-stopping-time`: stopping-time density. **KNOWN** heuristic /
  density, not a global proof.
- `tao-2019-almost-all-collatz`: almost all orbits attain almost bounded
  values (logarithmic density). **KNOWN** theorem; not global convergence.
- Cycle-exclusion preprints in `literature/` (`lebel-2026` and related):
  **working paper / unverified claim** unless independently Lean-checked
  here. Not treated as established mathematics.
- Computational verification of the conjecture on large finite ranges is
  **computationally verified range**, never a proof.

Project relationship: engine diagnosis / **engine rediscovery** of
well-definedness and \(S(1)=1\). No new Collatz theorem is claimed.

## Branch budget

```text
Mathematical target     Can v2 diagnose S without Collatz hints, and
                        certify an exact constraint or a precise engine
                        boundary?
Novelty hypothesis      A noncontracting / mixed-magnitude regime with
                        hidden branching, or ENGINE_LIMITATION if v2
                        cannot name the partition.
Falsifier               Adapter seeds v2, residues, cycles, or Lyapunov;
                        imports research.collatz; or a census is billed
                        as a Collatz proof.
Existing machinery      Diagnosis loop; AttackPlanner; Accelerated.lean.
Maximum Phase-0 scope   One integer adapter; generic attacks; Lean of an
                        exact identity the loop actually has.
Promotion criterion     A new reusable exact control language, or a
                        precise engine boundary that justifies later work.
Stop criterion          Machinery gravity; Collatz-solution language;
                        only KNOWN reparameterizations.
```

## Balanced-ternary formulation

None. The adapter uses ordinary integer arithmetic.

## Why BT may be relevant

It is not required. The laboratory question is whether the upgraded
engine loop, which saturated the scalar digit-fold family, recognizes a
genuinely different integer map.

## Candidate operations / invariants

- \(S\) well-defined on positive odds. **EXACT — LEAN VERIFIED**
  (`acceleratedT` / `syracuseS`). **KNOWN**.
- \(S\) preserves oddness. **EXACT — LEAN VERIFIED** (`syracuseS_odd`).
  **KNOWN**.
- \(S(1)=1\). **EXACT — LEAN VERIFIED** (`syracuseS_one`). **KNOWN**
  elementary.
- \(V(n)=n\) strictly decreases. **REFUTED** (\(S(1)=1\), \(S(3)=5\)).
- Odd box \([1,15]\) invariant. **REFUTED** (\(S(11)=17\)).
- \(S(n)<n\) for odd \(n\ge 3\). **REFUTED** (\(S(3)=5\)).
- \(S^2=S\). **REFUTED**.
- Integer \(n\) is a finite residual. **PARKED** (BFS hits the cap).
  Bounded census, not infinitude.

Do not re-test REFUTED ids `W_commutes_T`, `H_BT_independence`,
`n_star_le_n`, `C-shortcut-one-step-lyapunov`.

## Experiments

- `btlab research analyze|attack|reproduce|report syracuse`
- Adapter tests: `tests/research/syracuse/test_syracuse.py`
- Records: `experiments/syracuse/`
- Seed 27, state cap 16: closure **INCONCLUSIVE** by design (the seed
  trajectory is longer than the cap). Seed 1 is a finite fixed point and
  is not the benchmark seed.

## Conjectures

None opened. The Collatz conjecture is not a conjecture of this branch.

## Counterexamples

- One-step Lyapunov \(V(n)=n\): \(n=1\) (\(S(1)=1\)).
- Universal contraction for odd \(n\ge 3\): \(n=3\) (\(S(3)=5\)).
- Interval \([1,15]\cap 2\mathbb{Z}+1\): \(S(11)=17\).
- Idempotence: \(S(S(3))=1\neq 5\).

## Formalization

`formal/Problems/Collatz/Syracuse.lean` aliases `acceleratedT` and proves
`syracuseS_one`. No `sorry`. `Accelerated.lean` is imported from
`Problems.lean`. Cycle algebra from `Cycles.lean` is not copied.

## Results

### A. Upgrade report

See [research_engine_loop.md](../architecture/research_engine_loop.md).
New abstractions: `RegimeFingerprint`, `StructuralDelta`, `FamilyStatus`,
`CapabilityCoverage`, `ResearchDecision`, `ResearchCorpus`,
`ExpectedResearchValue`, `ResearchLoop`. Attack planner unchanged.
`ComplexityProfile` schema not forked. Weight-drift not extended.

### B. Regime corpus

SignedP0, DigitSumDynamics, WeightDynamics share core
`INTEGER_1D | SINGLETON | FINITE_CONTRACTING | FINITE_SEED_CLOSURE | FINITE | EXACT_CLOSURE`
with local differences (sign vs identity observation; reverse present
only on SignedP0). Syracuse: `MIXED_MAGNITUDE`, `UNBOUNDED_SAMPLE`,
`INCOMPLETE`, `BOUNDED`.

### C. Family analysis

The finite-contracting cluster with three closed members is
`SATURATED`. A mechanically similar contracting sketch scores low.
WeightDrift (`n+W(n)`) does not join that cluster (expanding,
truncated). Syracuse does not join it either.

### D. Syracuse diagnosis

Not a contracting digit-like regime. Mixed one-step growth and
contraction under a dummy singleton control; seed closure truncated.

### E. Structural delta

Nearest finite-contracting records: **HIGH** (core contraction, eventual
region, orbit, certificate strength all differ).

### F. Capability coverage

Exercised: finite-closure attempt, numerical contraction test, growth,
infinite reachable trajectories (cap), identity observation / separation.
Inapplicable: branching controls, affine modular/spectral/block, reverse
(no preimage callback). Not tested: valuation-as-control, cycle
obstruction language, symbolic control, recursive digit semantics.

### G. Attack ledger

Reconnaissance: bounded observation. Closure: INCONCLUSIVE. Functional
\(|n|\): REFUTED. Modular/spectral/reverse/block/factorization/symmetry:
inapplicable. Separation: identity observation separates distinct odds.
Quotient: inapplicable or identity on an incomplete set.

### H. Exact mathematical discoveries

Well-definedness and odd preservation (**KNOWN**, Lean). \(S(1)=1\)
(**KNOWN**). No new cycle identity was derived: the engine has no
generic affine word for hidden \(2^k\)-clearing.

### I. Falsification record

See Counterexamples. Naive claims (every step decreases; a small odd
interval is invariant; a finite sample implies bounded orbits) fail.

### J. Lean certification

`syracuseS_one`. Packaging of `acceleratedT`. Not a census-as-theorem.

### K. Prior-art checkpoint

| Kind | Item |
|------|------|
| known theorem | `acceleratedT`; Tao logarithmic density; expanding-period exclusion in `Cycles.lean` |
| computationally verified range | large Collatz searches; this module's seed-27 prefix |
| heuristic / probabilistic | Terras stopping times; stochastic \(3x+1\) models |
| working paper | cycle-sieve preprints in `literature/` |
| engine rediscovery | mixed magnitude; truncated residual; \(S(1)=1\) |
| new formalization | adapter alias `syracuseS` |
| potentially new result | none claimed |

### L. ComplexityProfile

Seed 27: controls 1; raw contribution unset; reachable count unset
(truncated); max separation depth 1 (identity); closure INCONCLUSIVE.
Growth/valuation complexity were **not** added to the profile schema.

### M. Research decision

```text
ENGINE_LIMITATION
```

Branch mapping: `PARK`.

## Open questions

Is there a reusable generic language for implicit prime-power clearing
(piecewise affine maps with dummy control) that is not Syracuse-specific?

## Decision

`PARK`. v2 left the finite-contracting digit-fold family and diagnosed a
mixed-magnitude non-finite integer regime, but it cannot represent the
hidden \(2\)-adic partition as a control alphabet without being handed
that structure. That is an engine boundary, not a Collatz theorem, and
not a reason to reopen `research.collatz`. Do not auto-continue.

Best next question: can a generic piecewise-affine census, driven by I/O
samples rather than a named valuation, become a reusable v2 attack?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as a Collatz contribution.
The value is the diagnosis loop and the engine-limitation statement.
