# Frozen Engine campaign: order-2 companion known zero

Status: **EXPLORATORY**

This is an engine competence check on the stored order-2 companion
window. It does **not** claim a Skolem decision procedure. Adapters
live in `research.skolem_order2_known_zero`. There is no `SkolemAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Does frozen Research Engine v2 certify the declared order-2
first-coordinate zero and recover the 2-D companion, without a new
attack?

## Exact statement

On the hint-free adapter whose transition is the stored blind packet

```text
window (u, v) maps to (v, a v + b u)
```

with declared coefficients \(a=3\), \(b=-2\) and start \((-7,-6)\), does
unmodified `ResearchLoop` recover the companion and certify a finite
first-coordinate zero?

Computational budget (stored packet): 16 planner steps / 32 residual
states.

## Current literature

- Kenison–Nieuwveld–Ouaknine–Worrell 2025: order-4 Skolem complete
  (`kenison-et-al-2025-order-4-skolem`). **THEOREM**.
- Bacik et al. 2026 Skolem/Positivity survey
  (`bacik-et-al-2026-skolem-positivity-survey`). **KNOWN**.

Project relationship: **engine diagnosis**. This window is a known
finite zero, not the open order-6 instance.

## Branch budget

```text
Mathematical target     Does frozen v2 certify the declared order-2
                        first-coordinate zero and recover the companion?
Novelty hypothesis      None expected. Memory/hygiene distinction vs
                        the order-6 GLOBAL_REASONING cluster.
Falsifier               Re-running order-6; leaking Skolem into the
                        adapter; tagging a ZERO_WITNESS as infinite-time
                        failure.
Existing machinery      CompanionShiftSpec; unmodified ResearchLoop;
                        v2.2 memory.
Maximum Phase-0 scope   One blind spec; one ResearchLoop; post-run zero
                        index; reuse existing Lean; dossier.
Promotion criterion     A new exact obstruction beyond the index-3 zero.
Stop criterion          New Skolem/p-adic attack; claiming a Skolem
                        decision.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Companion matrix \(\bigl((0,1),(-2,3)\bigr)\). **OBSERVATION**
  (`FINITE_CENSUS`). **KNOWN**.
- First coordinate vanishes at index 3.
  **EXACT — LEAN VERIFIED** (`companion_shift_zero_small_third`). **KNOWN**.
- Exact residual closure of size 4. **EXACT** (engine `SUPPORTED`).
  **KNOWN**.

## Experiments

- `tests/research/skolem_order2_known_zero/test_skolem_order2_known_zero.py`
- Runner: `research.skolem_order2_known_zero.runner.run_campaign`
- Scout (never imported by the adapter): `research.skolem_order2_known_zero.scout`

## Conjectures

None opened.

## Counterexamples

- “The first coordinate never vanishes on the search bound.” **REFUTED**
  at index 3.

## Formalization

`formal/Problems/Engine/CompanionShift.lean`, theorem
`companion_shift_zero_small_third`. No new Lean. No `sorry`. No ledger
row.

## Results

See sections A–L below.

## Open questions

None for this calibration window. Order-6 vanishing remains a separate
parked campaign.

## Decision

**CLOSE**. The board pick was a leftover competence check. Frozen v2
recovered the declared companion, certified the index-3 zero, and
closed a 4-state residual set. All statements are `KNOWN`. Do not
re-open the order-6 `GLOBAL_REASONING` cluster. Do not add a Skolem
attack.

Best next question: the unmodified leftover pick was `cyclic_tag_bit`.
What representation mismatch, if any, does that wildcard still teach?

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`CompanionShiftSpec` / `companion_shift_order2`):

- state \(\mathbb Z^2\); dummy singleton control;
- observation first coordinate;
- start \((-7,-6)\);
- last row \((-2,3)\), i.e. \((u,v)\mapsto(v,-2u+3v)\);
- accepting iff the first coordinate is \(0\);
- budget 16 / 32.

No ranking, p-adic, literature name, or scout import in `spec.py` /
`adapter.py` / `planner.py`.

### B. Diagnosis

Live `ResearchLoop` after `assemble_board` confirmed
`research_loop_pick = skolem_order2_known_zero` (not overridden):

- `RegimeFingerprint`: `INTEGER_VECTOR`, `SINGLETON`, `FINITE_CONTRACTING`,
  `FINITE_SEED_CLOSURE`, piecewise-affine `FINITE`, affine control `VECTOR`,
  certificate `EXACT_CLOSURE`.
- `StructuralDelta`: `MEDIUM` vs nearest `balanced_ternary_digit_sum_dynamics`.
- `FamilyStatus`: `ACTIVE`; family id
  `INTEGER_VECTOR|SINGLETON|FINITE_CONTRACTING|FINITE_SEED_CLOSURE|FINITE|EXACT_CLOSURE`.
- `ResearchDecision`: **CONTINUE** — finite piecewise-affine census;
  window agreement is not a \(\mathbb Z\)-theorem.

Planner output with `memory=ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| vector_affine | OBSERVATION; `FINITE_CENSUS`; 1 branch \(M=((0,1),(-2,3))\), offset \(0\) |
| matrix_word_invariant | INCONCLUSIVE |
| closure | SUPPORTED; complete; union size 4 |
| functional | OBSERVATION |
| separation | SUPPORTED |
| quotient | SUPPORTED |
| piecewise_affine, control_word, control_obstruction, modular, block, … | INAPPLICABLE |
| symbolic | SKIPPED |

### D. Origin analysis

First-coordinate zero at index 3 (`ZERO_WITNESS`). Exact finite
closure of size 4. Not a global Skolem theorem and not an infinite-time
non-vanishing claim.

### E. Control analysis

Singleton dummy control. Scalar word/obstruction inapplicable.

### F. Invariants and quotients

Quotient `SUPPORTED` on the exact 4-state closure. No new invariant
beyond the companion definition and the index-3 zero.

### G. Mathematical yield

```text
known_rediscoveries:     companion ((0,1),(-2,3)); zero at index 3; closure size 4
new_exact_results:       none beyond companion_shift_zero_small_third
new_invariants:          none promoted
new_obstructions:        none beyond the known finite zero
new_conjectures:         none
new_formalizations:      Problems.Engine.CompanionShift (existing)
potentially_new_mathematics: none
engineering_changes:     0
representation_novelty:  LOW
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY`. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

No `GLOBAL_REASONING` record. A `ZERO_WITNESS` on an order-2 companion
is a competence check; order-6 vanishing remains the global cluster.

### I. Prior-art reconciliation

Order \(\le 4\) Skolem is decidable. This instance is the catalogued
finite zero already used as Skolem campaign calibration A. Independently
rediscovered: no. Notation change to `companion_shift_order2` is not
novelty.

### J. Lean

Existing `companion_shift_zero_small_third`. No new theorem. No `sorry`.

### K. ResearchLoop

Board pick `skolem_order2_known_zero` was executed without override.
Memory ingest did not change planner output. Next leftover pick:
`cyclic_tag_bit`.

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE` (finite census). Laboratory
and campaign close because every statement is `KNOWN`. Do not add a
Skolem attack. Do not treat this as the open order-6 cluster.
