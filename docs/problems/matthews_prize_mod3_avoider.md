# Frozen Engine campaign: three-branch mod-3 avoider class

Status: **EXPLORATORY**

This is the third mathematical campaign on frozen Research Engine v2.3.
It does **not** claim that every orbit enters a cycle, a prize result,
or a Collatz theorem. The adapter reuses `OneVariableLoopSpec`. There is
no new attack.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the stored three-branch map, does frozen v2.3 recover a class
obstruction that forces \(\pm 1\pmod 3\) avoiders into the known
cycles, without taking branch reconstruction or \(0\pmod 3\)
divergence as the yield?

## Exact statement

On the stored packet `mod3_three_branch` (seeds \(x=1\) and \(x=5\),
dummy control, identity observation), does frozen v2.3 recover a
restriction that prevents, constrains, or forces access to the cycles
at \(-1\) and \(\{-2,-4\}\) for orbits that stay in \(\{1,2\}\pmod 3\),
without billing totality?

Computational budget (stored packet): 16 planner steps / 32 residual
states.

## Current literature

- Matthews–Watts 1984 (`matthews-watts-1984-generalization-hasse`).
  Generalized Syracuse maps; Uniform Distribution Conjecture. **KNOWN**.
- Laboratory BB-5 / \(R^+\) residue-affine reconstruction. **KNOWN**.

Project relationship: **engine diagnosis / elementary arithmetic**.
The \(0\pmod 3\) invariant and the two named cycles are immediate from
the definition.

## Branch budget

```text
Mathematical target     Does frozen v2.3 recover a class obstruction
                        that forces ±1 (mod 3) avoiders into the known
                        cycles?
Novelty hypothesis      An avoider-class restriction that is not the
                        three given branches, not the 0 (mod 3)
                        invariant, and not a finite-horizon cycle visit.
Falsifier               Stored seeds enter 0 (mod 3); yield is only
                        residue-affine rediscovery; cycles are
                        elementary from the definition.
Existing machinery      OneVariableLoopSpec; StrategyPlanner
                        census_obstruction; ResearchMemory.
Maximum Phase-0 scope   Thin packet, seeds 1 and 5, horizon≤16,
                        residual≤32; falsify; smallest exact Lean.
Promotion criterion     Exact avoider-class obstruction that is not
                        the definition and is not a totality claim.
Stop criterion          All surviving statements KNOWN or
                        REPARAMETERIZATION; new attack; prize/totality
                        billed as a Z-theorem.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Three residue-affine branches. **OBSERVATION** on the sample window;
  **DISCOVERED** (not a new formula). Mathematics **KNOWN** (problem
  definition).
- If \(3\mid x\) then \(T(x)=2x\) and \(3\mid T(x)\); \(\lvert T(x)\rvert=2\lvert x\rvert\).
  **EXACT — LEAN VERIFIED** (`matthews_zero_class_dvd`,
  `matthews_zero_class_expands`). **KNOWN**.
- \(T(-1)=-1\); \(T(-2)=-4\), \(T(-4)=-2\). **EXACT — LEAN VERIFIED**.
  **KNOWN**.
- Seeds \(1\) and \(5\) enter \(0\pmod 3\). **EXACT** on the relation.
  **KNOWN**.
- Window avoiders in \([-40,40]\) at 16 steps:
  \(\{-28,-10,-4,-2,-1\}\). Preimages of the known cycles.
  **OBSERVATION**; not a \(\mathbb Z\)-theorem.

## Experiments

- `tests/research/matthews_prize_mod3_avoider/test_matthews_prize_mod3_avoider.py`
- Runner: `research.matthews_prize_mod3_avoider.runner.run_campaign`
- Scout (never imported by the adapter):
  `research.matthews_prize_mod3_avoider.scout`

## Conjectures

None opened. The literature claim that every avoider enters \(-1\) or
\(\{-2,-4\}\) remains literature-open and is not restated as a project
conjecture.

## Counterexamples

- “Rediscovering the three formulas is the yield.” **REFUTED** as a
  campaign success criterion: they are the problem definition.
- “Seeds 1 and 5 are avoiders.” **REFUTED**: \(1\mapsto 3\), \(5\mapsto 1\mapsto 3\).
- “\(\{1,2\}\pmod 3\) is a basin / cannot reach \(0\pmod 3\).” **REFUTED**
  at seed 1.
- “Finite visit of \(-1\) or \(\{-2,-4\}\) is a map theorem on \(\mathbb Z\).”
  **REFUTED**.
- “This is the 4/3 strip or the BB5 partial map.” **REFUTED**:
  \(T(1)=3\), \(T(5)=1\), \(T(0)=0\).
- “Every 16-step window avoider is a cycle point.” **REFUTED**:
  \(-28\) and \(-10\) are strict preimages of \(\{-2,-4\}\).

## Formalization

`formal/Problems/Engine/MatthewsMod3.lean`. Identities
`matthews_zero_class_dvd`, `matthews_zero_class_expands`,
`matthews_fixed_neg_one`, `matthews_cycle_neg_two`. No `sorry`. No
ledger row (KNOWN).

## Results

See sections A–L below.

## Open questions

Whether every integer orbit that stays in \(\{1,2\}\pmod 3\) for all
time enters \(-1\) or \(\{-2,-4\}\). Finite-window preimages are not
that theorem.

## Decision

**CLOSE**. Frozen v2.3 recovered the three given branches as a
`FINITE_CENSUS`. The exact statements are elementary: \(0\pmod 3\) is
invariant and expanding; cycles at \(-1\) and \(\{-2,-4\}\) sit in the
definition. Packet seeds are not avoiders. \(\{1,2\}\pmod 3\) is not a
basin. No class obstruction forces all avoiders into those cycles.
All surviving statements are `KNOWN`. Laboratory decision `CLOSE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks?

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`OneVariableLoopSpec` / `mod3_three_branch`):

- state space \(\mathbb Z\);
- dummy singleton control;
- identity observation;
- seed \(1\) (packet also lists \(5\), probed post-run);
- successor the three stored formulas;
- budget 16 planner steps / 32 residual states.

No named conjecture, cycle theorem, or prize claim in `spec.py` /
`adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `CYCLE_EXCLUSION` selected
`census_obstruction`. Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`, `FINITE` piecewise-affine
  / latent control, `SCALAR` affine control, `MIXED_MAGNITUDE`,
  `UNBOUNDED_SAMPLE`, obstruction `WORD`.
- `ResearchDecision`: **CONTINUE** — finite census on a structurally
  distant regime; window agreement is not a \(\mathbb Z\)-theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | OBSERVATION; `FINITE_CENSUS`; 3 branches |
| parameter_domain | OBSERVATION |
| control_word | SUPPORTED |
| control_obstruction | OBSERVATION |
| closure | INCONCLUSIVE |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | INCONCLUSIVE |

### D. Class analysis

Let \(C_0=\{n: n\equiv 0\pmod 3\}\) and \(C_{\pm}=\{n: n\equiv\pm 1\pmod 3\}\).

- \(T(C_0)\subseteq C_0\) and \(\lvert T(x)\rvert=2\lvert x\rvert\) on \(C_0\). **EXACT**.
- \(C_{\pm}\) is **not** forward-invariant: \(T(1)=3\in C_0\).
- Known cycles lie in \(C_{\pm}\). Window preimages \(-28,-10\) enter
  \(\{-2,-4\}\). That is not an infinite-family obstruction.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| three residue-affine branches | yes | yes | common; **KNOWN** definition |
| \(0\pmod 3\) invariant | yes | independently | **KNOWN** |
| cycles at \(-1\), \(\{-2,-4\}\) | yes | independently from I/O | **KNOWN** |
| seeds 1, 5 are avoiders | — | refuted | false lead |
| \(C_{\pm}\) is a basin | hypothesized | refuted | false lead |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| \(0\pmod 3\) invariant / expanding | **PROVED** / **LEAN_CERTIFIED** |
| cycles at \(-1\) and \(\{-2,-4\}\) | **PROVED** / **LEAN_CERTIFIED** |
| avoider class forced into cycles | **not obtained** |
| \(C_{\pm}\) closed | **REFUTED** |

### G. Mathematical yield

```text
known_rediscoveries:     three given branches; generic cycle words
new_exact_results:       matthews_zero_class_dvd / expands; named cycles
new_invariants:          0 (mod 3) class
new_obstructions:        none
new_counterexamples:     T(1)=3; T(5)=1; window avoiders -28, -10
new_conjectures:         none
new_formalizations:      Problems.Engine.MatthewsMod3
potentially_new_mathematics: none
unresolved_questions:    whether every Z-avoider enters the known cycles
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` of the given map, plus
`NEW_FORMALIZATION` of elementary identities. Not
`POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

No `GLOBAL_REASONING` record. The avoider-to-cycle claim remains open
as a map theorem; window preimages are finite facts.

### I. Prior-art reconciliation

Matthews–Watts discuss generalized Syracuse maps and distribution
heuristics. They do not supply an avoider-class obstruction that this
campaign missed. The identities \(3\mid x\Rightarrow T(x)=2x\) and the
two cycles are immediate.

### J. Lean

`Problems.Engine.MatthewsMod3`. Strongest exact theorem:
`matthews_zero_class_dvd`. Cycle identities
`matthews_fixed_neg_one` and `matthews_cycle_neg_two`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction`.
Next leftover target is selected automatically (no override).

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE`. Laboratory and campaign close
because no class forces avoiders into the known cycles, and the
surviving statements are `KNOWN` elementary arithmetic. Do not add a
Matthews attack. Do not expand the census. Do not claim totality. Do
not start the next target automatically.
