# Frozen Engine campaign: order-5 companion vanishing

Status: **EXPLORATORY**

This is the fifth mathematical campaign on frozen Research Engine v2.3.
It is the last unrun frontier target on the board protocol. It does
**not** claim an unconditional order-5 Skolem decision, uniqueness of
zeros, or interpolant methods. The adapter reuses
`CompanionShiftSpec`. There is no new attack. Matrix-word is not
un-skipped.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On a declared order-5 companion window, can frozen v2.3 do more than
exhaust a finite prefix, without interpolants and without claiming an
unconditional decision procedure?

## Exact statement

On the stored packet `companion_shift_order5` (dimension 5, dummy
control, first-coordinate observation, start window
\((-30,-27,0,469,1762)\), last row
\((4225,-4745,522,-10,9)\)), does frozen v2.3 recover anything beyond
a finite prefix search and the frozen \(25^d\) skip?

Computational budget (stored packet): 16 planner steps / 32 residual
states; discovery prefix max index 64; skip \(25^d\) cubes above 50000
cells. Frozen skip:
`skip_attacks_for_dimension(5) = ("vector_affine", "matrix_word_invariant")`,
identical to dimension 6.

## Current literature

- Lipton et al. 2022 (`lipton-et-al-2022-skolem-conjecture`),
  Example 2.4: this window; unique zero at index 2 in the literature.
  Conditional order-5 procedure under the Skolem Conjecture.
  **KNOWN** / **THEOREM** (conditional, not used here).
- Kenison–Nieuwveld–Ouaknine–Worrell 2025
  (`kenison-et-al-2025-order-4-skolem`). Unconditional vanishing
  through order 4. **THEOREM**. Not this window.
- Bacik et al. 2026 (`bacik-et-al-2026-skolem-positivity-survey`).
  Survey of the open regime from order 5. **KNOWN**.

Project relationship: **engine diagnosis**. The campaign asks whether
dimension 5 is a new computational cluster and whether a finite zero
is billed as an unconditional procedure. It does not restate the
Skolem Problem.

## Branch budget

```text
Mathematical target     On a declared order-5 companion window, can
                        frozen v2.3 do more than exhaust a finite
                        prefix, without interpolants and without an
                        unconditional decision claim?
Novelty hypothesis      A dim-5 obstruction distinct from the order-6
                        skip cluster, or a uniqueness certificate that
                        is not the definition.
Falsifier               Census runs at d=5; skip is billed as a new
                        cluster; ZERO_WITNESS billed as an order-5
                        procedure; this is the order-6 flagship or the
                        order-2 window.
Existing machinery      CompanionShiftSpec;
                        skip_attacks_for_dimension(5);
                        research.skolem_lrs.discovery;
                        CompanionShift.lean.
Maximum Phase-0 scope   Thin packet; prefix/skip probes; memory-free
                        StrategyPlanner; live ResearchLoop; smallest
                        exact Lean zero identity.
Promotion criterion     Exact uniqueness or a class constraint that is
                        not the definition and not the frozen skip.
Stop criterion          All KNOWN/REPARAMETERIZATION; new attack;
                        interpolants; Skolem decision.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Order-5 companion window and last row. **OBSERVATION**.
  Mathematics **KNOWN** (Lipton et al. 2022, Example 2.4).
- First coordinate vanishes at index 2. **EXACT — LEAN VERIFIED**
  (`companion_shift_order5_zero_second`). **KNOWN**.
- `vector_affine` and `matrix_word_invariant` skipped at dimension 5,
  same pair as dimension 6. **OBSERVATION**
  (`COMPUTATION_EXHAUSTED`). Not a new cluster.
- Uniqueness of the zero. **not obtained** from frozen moduli
  \(2,\ldots,32\). Literature uniqueness is out of scope.

## Experiments

- `tests/research/skolem_order5_unconditional/test_skolem_order5_unconditional.py`
- Runner: `research.skolem_order5_unconditional.runner.run_campaign`
- Scout (never imported by spec/adapter/planner):
  `research.skolem_order5_unconditional.scout`

## Conjectures

None opened. Unconditional vanishing for general order-5 LRS remains
literature-open and is not restated as a project conjecture.

## Counterexamples

- “Census and matrix-word run at dimension 5.” **REFUTED**:
  \(25^5=9765625>50000\).
- “Dimension-5 skip is a new computational cluster.” **REFUTED**:
  same skip pair as dimension 6.
- “A ZERO_WITNESS decides vanishing for all order-5 LRS.” **REFUTED**.
- “The frozen prefix recovers uniqueness.” **REFUTED**.
- “This is the order-6 survey instance.” **REFUTED**: dimension 5,
  `zero_at=2`.
- “This is the order-2 competence window.” **REFUTED**: dimension 5,
  `zero_at=2` (order 2 vanishes at 3).
- “Companion reconstruction is the yield.” **REFUTED** as a success
  criterion.

## Formalization

`formal/Problems/Engine/CompanionShift.lean`. Identity
`companion_shift_order5_zero_second`. No `sorry`. No ledger row
(KNOWN).

## Results

See sections A–L below.

## Open questions

Unconditional vanishing for general order-5 integer LRS. A finite
zero on one declared window is not that theorem.

## Decision

**CLOSE**. Frozen v2.3 found the first-coordinate zero at index 2 and
skipped the \(25^5\) census with the same skip pair as dimension 6.
No uniqueness certificate and no unconditional procedure. All
surviving statements are `KNOWN`. Laboratory decision `CLOSE`. Engine
`ResearchDecision` may still be `CONTINUE`.

Best next question: the unmodified leftover pick on the board after
this ingest (first wildcard in the protocol order). What exact
obstruction, if any, can frozen v2.3 produce there without new
attacks? Do not start a Skolem decision procedure.

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`CompanionShiftSpec` / `companion_shift_order5`):

- state space \(\mathbb Z^5\);
- dummy singleton control;
- observation the first coordinate;
- start the declared window;
- last row the declared companion coefficients;
- budget 16 planner steps / 32 residual states;
- skip `vector_affine` and `matrix_word_invariant` at dimension 5.

No named conjecture, known congruence of zeros, interpolant method,
or open-problem status in `spec.py` / `adapter.py` / `planner.py`.
Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `ORIGIN_AVOIDANCE` selected
`vector_matrix`. Live results of that chain are empty because both
attacks are skipped.

Live `ResearchLoop` on the stored packet reports a structurally
distant companion regime. A finite zero does not thaw the census.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| vector_affine | COMPUTATION_EXHAUSTED (skipped by adapter) |
| matrix_word_invariant | COMPUTATION_EXHAUSTED (skipped by adapter) |
| reconnaissance / closure / functional / separation / quotient | as in the live session |

### D. Class analysis

Let \(u_n\) be the first coordinate of the companion window at index
\(n\).

- \(u_2=0\). **EXACT**. Not \(\forall\) order-5 LRS.
- Skip pair at \(d=5\) equals skip pair at \(d=6\). **EXACT** on the
  frozen cell budget. Not a uniqueness theorem.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| order-5 companion window | yes | yes | common; **KNOWN** definition |
| \(u_2=0\) | yes | independently | **KNOWN** |
| uniqueness of the zero | yes (literature) | not obtained | out of frozen probe |
| \(25^5\) skip = \(25^6\) skip | yes | independently | **KNOWN** cluster |
| unconditional order-5 procedure | forbidden | not obtained | not yield |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| companion matrix / window | **KNOWN** definition |
| \(u_2=0\) | **PROVED** / **LEAN_CERTIFIED** |
| uniqueness | **not obtained** |
| unconditional order-5 decision | **not obtained** |
| new skip cluster | **REFUTED** |

### G. Mathematical yield

```text
known_rediscoveries:     order-5 companion; 25^5 / matrix-word skip
new_exact_results:       companion_shift_order5_zero_second
new_invariants:          none
new_obstructions:        none
new_counterexamples:     d=5 skip is the same cluster as d=6
new_conjectures:         none
new_formalizations:      Problems.Engine.CompanionShift (order-5 identity)
potentially_new_mathematics: none
unresolved_questions:    unconditional vanishing for general order-5 LRS
engineering_changes:     0
representation_novelty:  LOW
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY`. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

`COMPUTATIONAL` only (skipped lattice/census). Not `GLOBAL_REASONING`:
this instance has a `ZERO_WITNESS`. Grey loot ids `order5:loot:zero`,
`:skip`, `:uniqueness`.

### I. Prior-art reconciliation

Lipton et al. already record the zero at index 2. The laboratory
identity is that finite fact, not their conditional procedure and not
their uniqueness modulus. Kenison et al. decide order \(\le 4\), not
this window.

### J. Lean

`Problems.Engine.CompanionShift`. Strongest exact theorem:
`companion_shift_order5_zero_second`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(ORIGIN_AVOIDANCE)` selected `vector_matrix` and
returned no attack results. Next leftover target is selected
automatically (no override). Do not start that leftover in this
branch.

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` may be `CONTINUE`. Laboratory and campaign
close because the finite zero is KNOWN, the skip is the same cluster
as dimension 6, and no uniqueness or unconditional procedure was
recovered. Do not add a Skolem attack. Do not un-skip matrix-word.
Do not start the next target automatically.
