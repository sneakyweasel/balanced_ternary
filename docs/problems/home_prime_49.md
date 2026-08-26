# Frozen Engine campaign: factor-concatenation map

Status: **EXPLORATORY**

This is the eighth mathematical campaign on frozen Research Engine v2.3
and the last protocol wildcard after the frontier list. It does **not**
claim that seed 49 reaches a prime. The adapter is a thin one-variable
spec with `affine_system=None` and a factorization cap. There is no
concatenation attack and no unfinished-seed folklore on the adapter.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the stored factorization-concatenation map, does frozen v2.3
diagnose a regime that recurs the non-affine arithmetic cluster,
without a new concatenation attack and without claiming that seed 49
reaches a prime?

## Exact statement

On the stored packet `home_prime_49` (integers \(\ge 2\), dummy control,
identity observation, seed \(49\)), with \(T(n)\) the integer whose
decimal digits are the concatenation of the prime factors of \(n\) in
ascending order (with multiplicity), does frozen v2.3 recover a class
obstruction relevant to reaching a prime, or only a budget-truncated
prefix plus a missing affine cover?

Computational budget (stored packet): 16 planner steps / 32 residual
states; successor undefined when \(n<2\) or trial factorization exceeds
\(10^{12}\) / trial bound \(10^6\).

## Current literature

- OEIS A037274 (`oeis-A037274`): home primes obtained by iterating
  factor concatenation. Computational table. **COMPUTATIONAL**.
- Laboratory aliquot campaign: divisor-sum outside affine control with
  truncated factorization. **KNOWN**. Comparison cluster, not the same
  map.

Project relationship: **engine diagnosis**. No new number-theory
theorem is claimed. Published unfinished-seed folklore is not imported.

## Branch budget

```text
Mathematical target     On the stored factorization-concatenation map,
                        does frozen v2.3 diagnose a regime that recurs
                        the non-affine arithmetic cluster (distinct from
                        aliquot truncation and from reverse-add/juggler
                        closures), without a dedicated attack and without
                        claiming that seed 49 reaches a prime?
Novelty hypothesis      An exact prime-reachability obstruction that is
                        not the definition and not a budget truncation.
Falsifier               Affine cover; adapter leak of unfinished-seed
                        folklore; seed-49 prefix billed as a Z-theorem;
                        this is aliquot / reverse-add / juggler.
Existing machinery      Trial factorization (aliquot cap pattern);
                        one-variable dummy-control spec; ResearchLoop.
Maximum Phase-0 scope   Thin packet seed 49; factorization-capped concat;
                        prefix probes; live loop; smallest exact Lean.
Promotion criterion     An exact class obstruction to reaching a prime
                        that is not the definition.
Stop criterion          All KNOWN/REPARAMETERIZATION; new attack;
                        totality/unfinished-seed claims; folklore leak.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- \(T(7)=7\). **EXACT — LEAN VERIFIED** (`prime_seven_fixed`). **KNOWN**.
- \(49=7\cdot 7\) concatenates to \(77\). **EXACT — LEAN VERIFIED**.
  **KNOWN**.
- \(4\mapsto 22\mapsto 211\) with \(211\) prime.
  **EXACT — LEAN VERIFIED**. **KNOWN**. Not a theorem on all \(n\ge 2\).
- Seed 49 then grows until the factorization cap (14-digit successor).
  **OBSERVATION**. Not a prime-reachability theorem.
- \(T(49)=77\), not aliquot \(8\) and not floor-power \(343\).
  **OBSERVATION**. **REFUTED** as identity with those maps.
- \(T(8)=222\), not reverse-plus-add \(0\). **OBSERVATION**. **REFUTED**.
- No complete piecewise-affine cover on the sample window.
  **OBSERVATION** (`INCONCLUSIVE`). **KNOWN** (factor concatenation).
- Exact residual closure of the packet prefix has size 13.
  **EXACT** (engine `SUPPORTED`). Budget artefact: the last state has
  no legal successor.

## Experiments

- `tests/research/home_prime_49/test_home_prime_49.py`
- Runner: `research.home_prime_49.runner.run_campaign`
- Scout (never imported by spec/adapter/planner):
  `research.home_prime_49.scout`

## Conjectures

None opened. Whether seed 49 reaches a prime remains literature-open
and is not restated as a project conjecture.

## Counterexamples

- “The map is residue-affine.” **REFUTED**: `affine_system is None`;
  successor concatenates prime factors; census `INCONCLUSIVE`.
- “The seed-49 prefix is a theorem that every \(n\ge 2\) reaches a prime.”
  **REFUTED**.
- “The successor is \(\sigma(n)-n\).” **REFUTED**: \(T(49)=77\), not \(8\).
- “The successor is the even/odd floor-power map.” **REFUTED**:
  \(T(49)=77\), not \(343\).
- “The successor is balanced-ternary reverse-plus-add.” **REFUTED**:
  \(T(8)=222\), not \(0\).
- “Progress requires a new concatenation attack.” **REFUTED**: exact I/O
  is the definition; the frozen stack diagnoses the regime.

## Formalization

`formal/Problems/Engine/FactorConcat.lean`. Identities
`decimalConcat_seven_seven`, `factorConcat_forty_nine_step`,
`prime_seven_fixed`, `four_reaches_two_eleven`. No `sorry`. No ledger
row (KNOWN).

## Results

See sections A–L below.

## Open questions

Whether seed 49 reaches a prime. A budget-truncated prefix is not that
theorem.

## Decision

**CLOSE**. Frozen v2.3 recovered a finite residual prefix of seed 49
and refused a piecewise-affine cover. The identities are elementary.
The engine fingerprint is `FINITE_SEED_CLOSURE` of a truncated chain,
which is a budget artefact distinct from aliquot `UNBOUNDED_SAMPLE`
and from reverse-add/juggler attractor closures. That answers the
board's failure-learning question without a new attack. All surviving
statements are `KNOWN`. Laboratory decision `CLOSE`. Engine
`ResearchDecision` may still be `CONTINUE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks? Do not add a concatenation attack. Do not
start that leftover in this branch.

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`FactorConcatSpec` / `home_prime_49`):

- state space integers \(\ge 2\);
- dummy singleton control;
- identity observation;
- seed \(49\);
- successor the stored factor concatenation;
- budget 16 planner steps / 32 residual states;
- factorization cap \(10^{12}\) / trial \(10^6\).

No named conjecture, unfinished-seed language, or open-problem status
in `spec.py` / `adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `TERMINATION` selected
`global_inductive` and returned no attack results (no ranking-function
attack on the frozen stack).

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`,
  `FINITE_CONTRACTING`, `FINITE_SEED_CLOSURE`, `EXACT_CLOSURE`,
  piecewise-affine `UNCERTAIN`, affine control `UNOBSERVED`.
- `ResearchDecision`: **CONTINUE** — new structural regime with an
  exact certificate (the truncated seed-49 prefix). That certificate
  is not a map theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | INCONCLUSIVE; no complete cover |
| closure | SUPPORTED; size 13 |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | SUPPORTED |
| factorization (existing) | INAPPLICABLE; not a new attack |
| parameter_domain / control_word / vector_affine / matrix_word | INAPPLICABLE |

### D. Class analysis

Primes inside the budget are fixed points. Seed 4 enters a prime in
two steps. Seed 49 grows until the successor exceeds the factorization
cap. No residue class was found that forces all orbits to a prime.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| \(T(7)=7\) | yes | independently | **KNOWN** |
| seed 4 reaches 211 | yes | independently | **KNOWN** |
| seed 49 maps to 77 then truncates | yes | independently | **KNOWN** |
| no affine cover | yes | independently | **KNOWN** |
| seed 49 reaches a prime | open | not obtained | not yield |
| distinct from aliquot UNBOUNDED_SAMPLE | hypothesized | yes on this seed | **OBSERVATION** |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| \(T(7)=7\) | **EXACT — LEAN VERIFIED** |
| \(49\to 77\) | **EXACT — LEAN VERIFIED** |
| \(4\to 22\to 211\) | **EXACT — LEAN VERIFIED** |
| residue-affine cover | **not obtained** |
| prime reachability of 49 | **not obtained** |

### G. Mathematical yield

```text
known_rediscoveries:     seed-49 prefix; missing affine cover
new_exact_results:       decimalConcat / forty_nine_step / prime 7 / 4 reaches 211
new_invariants:          none
new_obstructions:        none
new_counterexamples:     T(49)=77 vs aliquot/floor-power; T(8)=222 vs reverse-add
new_conjectures:         none
new_formalizations:      Problems.Engine.FactorConcat
potentially_new_mathematics: none
unresolved_questions:    whether seed 49 reaches a prime
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` plus a `DISTINCT_REGIME`
fingerprint versus aliquot unbounded truncation and versus attractor
closures. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

`REPRESENTATION` (no affine cover). Not `GLOBAL_REASONING`: prime
reachability of 49 is out of scope. Grey loot ids
`home_prime:loot:mismatch`, `:seed49`, `:cluster`. Loot that listed
this target as transfer is `REUSED`.

### I. Prior-art reconciliation

OEIS A037274 records home-prime iteration. It does not supply a class
obstruction this campaign missed. The laboratory identities are the
packet first step and the finite seed-4 orbit.

### J. Lean

`Problems.Engine.FactorConcat`. Strongest exact theorem:
`four_reaches_two_eleven`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(TERMINATION)` selected `global_inductive` with
empty results. Next leftover target is selected automatically (no
override). Do not start that leftover in this branch.

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE`. Laboratory and campaign
close because the finite prefix is KNOWN, there is no affine cover,
and no class forces seed 49 to a prime. Do not add a concatenation
attack. Do not claim totality. Do not import unfinished-seed folklore.
Do not start the next target automatically.
