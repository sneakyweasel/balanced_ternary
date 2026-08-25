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
After the piecewise-affine census, which sample-supported branch family
(if any) is recovered, and what remains uncertified?

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
- Sample-supported family \(2^k y = 3x+1\) with several observed \(k\).
  **OBSERVATION**. **KNOWN** as `acceleratedT_mul`.
- Maximal-divisibility conjunction for that family. **OBSERVATION** of
  the map on a window; the integer iff is **EXACT — LEAN VERIFIED** and
  **KNOWN** (`mul_pow_eq_iff_padicValInt`). Presentation \(k=v_2(3x+1)\)
  only after the conjunction is certified. Not a global map theorem.

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

See [research_engine_loop.md](../architecture/research_engine_loop.md)
and [piecewise_affine_census.md](piecewise_affine_census.md).
`PiecewiseAffineCensus` is appended after reconnaissance;
`parameter_domain` immediately after that. Fingerprint gains non-core
`piecewise_affine_structure` / `latent_control` / `parameter_domain`.
`ComplexityProfile` is still not forked. Weight-drift is not extended.

### B. Regime corpus

SignedP0, DigitSumDynamics, WeightDynamics share core
`INTEGER_1D | SINGLETON | FINITE_CONTRACTING | FINITE_SEED_CLOSURE`
with local differences. SignedP0 has a *secondary* finite residue census
that does not change the core family. Syracuse: `MIXED_MAGNITUDE`,
`UNBOUNDED_SAMPLE`, piecewise `PARAMETERIZED`, domain `EXACT`.

### C. Family analysis

The finite-contracting cluster with three closed members is
`SATURATED`. WeightDrift does not join. Syracuse does not join.

### D. Syracuse diagnosis

Still not a contracting digit-fold. Mixed magnitude, dummy singleton
control, truncated seed closure. The census recovers a sample-supported
parameterized family \(2^k y = 3x+1\). `parameter_domain` then certifies
the conjunction \(2^k\mid(3x+1)\land 2^{k+1}\nmid(3x+1)\) as `EXACT` for
the arithmetic relation (presentation \(k=v_2(3x+1)\) only after that).
Mere divisibility is `NECESSARY_ONLY`. Engine decision `CONTINUE`:
relation certified, map globality on \(\mathbb{Z}\) empirical. **KNOWN**
as `acceleratedT_mul`. Not a Collatz theorem.

### E. Structural delta

Nearest finite-contracting records: **HIGH** (core contraction, eventual
region, orbit, certificate strength all differ). Piecewise/latent fields
also differ (`PARAMETERIZED` vs `FINITE`/`UNCERTAIN`). Non-core
`parameter_domain` is `EXACT` on Syracuse.

### F. Capability coverage

Exercised: finite-closure attempt, numerical contraction, growth,
infinite reachable trajectories (cap), latent piecewise-affine control,
parameter-domain certification, valuation dynamics (parameterized family
plus exact maximal-divisibility conjunction). Inapplicable: branching
controls, affine modular/spectral/block, reverse. Not tested: cycle
obstruction, symbolic control, recursive digit semantics.

### G. Attack ledger

Reconnaissance: bounded observation. `piecewise_affine`: `OBSERVATION`,
`PARAMETERIZED_CENSUS`, family \(p=3,r=1\), \(q_{\mathrm{base}}=2\).
`parameter_domain`: `SUPPORTED` / `EXACT` on the arithmetic relation
(`EXACT_ARITHMETIC_IDENTITY`); map globality remains empirical. Closure:
INCONCLUSIVE. Functional \(|n|\): REFUTED. Modular/spectral/reverse/block/
factorization/symmetry: inapplicable in the same planner pass (no
`AffineSystem` injection). Separation: identity observation separates
distinct odds.

### H. Exact mathematical discoveries

Well-definedness and odd preservation (**KNOWN**, Lean). \(S(1)=1\)
(**KNOWN**). Sample-supported clearing family and its maximal domain
(**OBSERVATION**, engine rediscovery of `acceleratedT_mul`; generic Lean
iff `mul_pow_eq_iff_padicValInt` is **KNOWN** arithmetic). No new cycle
identity. Window agreement is not a map theorem on all odd positives.

### I. Falsification record

See Counterexamples. Naive claims (every step decreases; a small odd
interval is invariant; a finite sample implies bounded orbits; a finite
affine table exhausts \(S\); mere \(2^k\mid(3x+1)\) selects the exact
parameter) fail.

### J. Lean certification

`syracuseS_one`. Packaging of `acceleratedT`. Synthetic A identities are
in `Problems/Engine/PiecewiseCensus.lean`. The generic valuation iff is
`Problems/Engine/ParameterDomain.lean`. Neither is retagged as a Syracuse
theorem. The census is not `EXACT — LEAN VERIFIED`.

### K. Prior-art checkpoint

| Kind | Item |
|------|------|
| known theorem | `acceleratedT` / `acceleratedT_mul`; padic valuation iff; Tao logarithmic density; expanding-period exclusion in `Cycles.lean` |
| computationally verified range | large Collatz searches; this module's seed-27 prefix and odd census window |
| heuristic / probabilistic | Terras stopping times; stochastic \(3x+1\) models |
| working paper | cycle-sieve preprints in `literature/` |
| engine rediscovery | mixed magnitude; truncated residual; \(S(1)=1\); sample-supported \(2^k y=3x+1\) and maximal domain |
| new formalization | adapter alias `syracuseS`; synthetic A Lean; generic Engine valuation iff |
| potentially new result | none claimed |

### L. ComplexityProfile

Seed 27: controls 1; raw contribution unset; reachable count unset
(truncated); max separation depth 1 (identity); closure INCONCLUSIVE.
Census and domain metrics stay on attack evidence (`branch_count`,
`coverage`, `census_kind`, `predicate_count`, `queries`). Profile schema
not forked.

### M. Research decision

```text
CONTINUE
```

Branch mapping: `PARK`. The arithmetic domain of the reconstructed
relation is certified generically. That is still not a Collatz theorem,
not a \(\mathbb{Z}\)-wide map certificate, and not a reason to reopen
`research.collatz`.

## Open questions

Is there a generic certificate beyond KNOWN clearing that still does not
require map-specific hints and does not claim convergence?

## Decision

`PARK`. v2 now recovers a sample-supported parameterized family and
certifies its maximal-divisibility domain, matching the known clearing
identity. The old representation boundary moved again. That is still not
a Collatz theorem and not a reason to reopen `research.collatz`. Do not
auto-continue.

Best next question: is there a generic certificate beyond KNOWN clearing
that still does not require map-specific hints?

## Publication assessment

Status: `EXPLORATORY`. Not a `PAPER_CANDIDATE` as a Collatz contribution.
The value is the generic census/domain layer and the moved engine
boundary.

