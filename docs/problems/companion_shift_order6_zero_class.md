# Frozen Engine campaign: order-6 vanishing class constraint

Status: **EXPLORATORY**

This is the fourth mathematical campaign on frozen Research Engine v2.3.
It is a sharper intermediate on the stored order-6 companion window,
not a second Skolem decision and not a non-existence claim. The adapter
reuses `CompanionShiftSpec`. There is no new attack. Matrix-word is
not un-skipped.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the declared order-6 companion window, can frozen v2.3 recover a
lattice/gcd or matrix-word congruence on vanishing indices, without
interpolants and without claiming that a zero does not exist?

## Exact statement

On the stored packet `companion_shift_order6` (dimension 6, dummy
control, first-coordinate observation, start window
\((12, 49, 374, 6003, 21520, 150773)\), last row
\((-4225, 8970, -5267, 532, -19, 10)\)), does frozen v2.3 recover a
class constraint on indices where the first coordinate vanishes that
is not the companion definition itself?

Computational budget (stored packet): 16 planner steps / 32 residual
states; discovery prefix max index 64; skip \(25^d\) cubes above 50000
cells. Frozen skip:
`skip_attacks_for_dimension(6) = ("vector_affine", "matrix_word_invariant")`.

## Current literature

- Bacik et al. 2026 (`bacik-et-al-2026-skolem-positivity-survey`).
  Order-6 survey instance; companion reconstruction is laboratory
  infrastructure. **KNOWN**.
- Kenison–Nieuwveld–Ouaknine–Worrell 2025
  (`kenison-et-al-2025-order-4-skolem`). Unconditional vanishing
  through order 4. **THEOREM**. Not this window.
- Lipton et al. 2022 (`lipton-et-al-2022-skolem-conjecture`).
  Conditional methods; interpolants forbidden here. **KNOWN**.

Project relationship: **engine diagnosis**. The campaign asks only for
an intermediate vanishing-index class constraint. It does not restate
the Skolem Problem and does not claim a zero-free theorem.

## Branch budget

```text
Mathematical target     On the declared order-6 companion window, can
                        frozen v2.3 recover a lattice/gcd or
                        matrix-word congruence on vanishing indices,
                        without interpolants and without claiming
                        non-existence?
Novelty hypothesis      An intermediate vanishing-index class
                        constraint that is not the companion
                        definition.
Falsifier               Companion rediscovery; 25^6 skip; prefix gaps
                        billed as modular exclusion; “no zero on
                        0..64 ⇒ no zero”.
Existing machinery      CompanionShiftSpec / order6_spec;
                        skip_attacks_for_dimension(6);
                        research.skolem_lrs.discovery;
                        CompanionShift.lean.
Maximum Phase-0 scope   Thin packet wrapping the existing spec;
                        prefix/modulus probes; memory-free
                        StrategyPlanner; live ResearchLoop; reuse
                        existing Lean.
Promotion criterion     Exact vanishing congruence that is not the
                        definition.
Stop criterion          All KNOWN/REPARAMETERIZATION; new attack;
                        Skolem decision; interpolants.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Order-6 companion window and last row. **OBSERVATION**;
  **DISCOVERED** (not a new formula). Mathematics **KNOWN**
  (problem definition / prior `skolem_lrs` run).
- First coordinate has no integer zero on indices \(0,\ldots,64\).
  **COMPUTATIONALLY VERIFIED** on that prefix (`FINITE_ZERO_FREE`).
  Not a \(\mathbb Z\)-theorem. `universal_zero_free=False`.
- \(u_{11}<0\). **EXACT — LEAN VERIFIED**
  (`companion_shift_order6_eleventh_negative`). **KNOWN**.
- Every modulus \(m\in\{2,\ldots,32\}\) hits a \(0\) residue on the
  prefix (`moduli_without_zero=()`, `NO_PREFIX_EXCLUSION`).
  **OBSERVATION**. That is not integer vanishing.
- `vector_affine` and `matrix_word_invariant` skipped by adapter at
  dimension 6. **OBSERVATION** (`COMPUTATION_EXHAUSTED`). Not a
  lattice/gcd congruence.

## Experiments

- `tests/research/companion_shift_order6_zero_class/test_companion_shift_order6_zero_class.py`
- Runner: `research.companion_shift_order6_zero_class.runner.run_campaign`
- Scout (never imported by spec/adapter/planner):
  `research.companion_shift_order6_zero_class.scout`

## Conjectures

None opened. Whether the first coordinate vanishes on \(\mathbb Z\)
remains the literature-open instance and is not restated as a project
conjecture.

## Counterexamples

- “Rediscovering the companion is the yield.” **REFUTED** as a
  campaign success criterion: it is KNOWN infrastructure.
- “No zero on indices \(0..64\) means no zero exists.” **REFUTED**.
- “Matrix-word / lattice-gcd recovers a vanishing congruence.”
  **REFUTED**: the attack is skipped at dimension 6.
- “This is the order-2 competence check.” **REFUTED**: dimension 6,
  `zero_at=None`.
- “The first coordinate has fixed sign.” **REFUTED** at \(n=11\).
- “A modulus in \(2..32\) with no \(0\) residue on the prefix is
  modular exclusion of integer zeros.” **REFUTED**: every such
  modulus hits a \(0\) residue, and a prefix gap would still not be
  exclusion.

## Formalization

`formal/Problems/Engine/CompanionShift.lean`. Existing identities
`companion_shift_order6_step` and
`companion_shift_order6_eleventh_negative`. No new theorem. No
`sorry`. No ledger row (KNOWN).

## Results

See sections A–L below.

## Open questions

Whether the first coordinate vanishes on \(\mathbb Z\). A length-65
zero-free prefix is not that theorem. A skipped matrix-word attack is
not a class constraint.

## Decision

**CLOSE**. Frozen v2.3 did not recover a lattice/gcd or matrix-word
congruence on vanishing indices. The companion window is KNOWN. The
\(25^6\) census and matrix-word attacks are skipped by the frozen
cell budget. The prefix is zero-free and every small modulus hits a
\(0\) residue; neither is a vanishing congruence or a non-existence
claim. All surviving statements are `KNOWN`. Laboratory decision
`CLOSE`. Engine `ResearchDecision` may still be `CONTINUE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks? Do not start a Skolem decision procedure
and do not un-skip matrix-word.

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`CompanionShiftSpec` / `companion_shift_order6`):

- state space \(\mathbb Z^6\);
- dummy singleton control;
- observation the first coordinate;
- start the declared window;
- last row the declared companion coefficients;
- budget 16 planner steps / 32 residual states;
- skip `vector_affine` and `matrix_word_invariant` at dimension 6.

No named conjecture, known congruence of zeros, interpolant method,
or open-problem status in `spec.py` / `adapter.py` / `planner.py`.
Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `ORIGIN_AVOIDANCE` selected
`vector_matrix`. Live results of that chain are empty because both
attacks are skipped.

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_VECTOR`, `SINGLETON`,
  `MIXED_MAGNITUDE`, `UNBOUNDED_SAMPLE`.
- `ResearchDecision`: **CONTINUE** — structurally distant non-finite
  regime; finite prefix is not a vanishing theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| vector_affine | COMPUTATION_EXHAUSTED (skipped by adapter) |
| matrix_word_invariant | COMPUTATION_EXHAUSTED (skipped by adapter) |
| reconnaissance | OBSERVATION |
| closure | INCONCLUSIVE |
| functional | typically REFUTED |
| separation | typically SUPPORTED |
| quotient | INCONCLUSIVE |
| affine control | UNOBSERVED as a recovered census |

### D. Class analysis

Let \(u_n\) be the first coordinate of the companion window at index
\(n\).

- No \(n\in\{0,\ldots,64\}\) with \(u_n=0\). **COMPUTATIONALLY VERIFIED**
  on the prefix. Not \(\forall n\in\mathbb Z_{\ge 0},\; u_n\neq 0\).
- For every \(m\in\{2,\ldots,32\}\) there is some prefix index with
  \(u_n\equiv 0\pmod m\). That does not force some integer \(n\) with
  \(u_n=0\).
- Lattice/gcd word invariants were not computed: the attack is skipped.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| order-6 companion window | yes | yes | common; **KNOWN** definition |
| \(u_{11}<0\) | yes | independently | **KNOWN** |
| no zero on \(0..64\) | yes | independently | **KNOWN** prefix fact |
| lattice/gcd vanishing congruence | hypothesized | not obtained | skip |
| prefix \(\Rightarrow\) non-existence | forbidden | refuted | false lead |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| companion matrix / window | **KNOWN** definition |
| \(u_{11}<0\) | **PROVED** / **LEAN_CERTIFIED** |
| vanishing-index congruence | **not obtained** |
| universal zero-free | **not claimed** |
| modular exclusion on \(2..32\) | **REFUTED** as prefix exclusion |

### G. Mathematical yield

```text
known_rediscoveries:     order-6 companion window; 25^6 / matrix-word skip
new_exact_results:       u_11 < 0 (already Lean); FINITE_ZERO_FREE on 0..64
new_invariants:          none
new_obstructions:        none; prefix modular hits are not a vanishing congruence
new_counterexamples:     fixed sign at n=11; prefix is not non-existence
new_conjectures:         none
new_formalizations:      none; reuse Problems.Engine.CompanionShift
potentially_new_mathematics: none
unresolved_questions:    whether the first coordinate vanishes on Z
engineering_changes:     0
representation_novelty:  LOW
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` of the companion instance plus
the frozen computational skip. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

`COMPUTATIONAL` (skipped lattice/census) and `GLOBAL_REASONING`
(finite prefix is not vanishing on \(\mathbb Z\)). Grey loot ids
`order6_zero:loot:prefix`, `:matrix`, `:modulus`. Do not bill the
skip as a theorem.

### I. Prior-art reconciliation

Bacik et al. supply the survey instance. Kenison et al. decide
vanishing through order 4, not this window. Lipton et al. use methods
this campaign forbids. None of them supply a lattice/gcd vanishing
congruence that frozen v2.3 missed by skipping interpolants.

### J. Lean

`Problems.Engine.CompanionShift`. Strongest exact theorem reused:
`companion_shift_order6_eleventh_negative`. Step identity
`companion_shift_order6_step`. No new lemma. No `sorry`.

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

Engine `ResearchDecision` was `CONTINUE`. Laboratory and campaign
close because no vanishing-index class constraint was recovered, and
the surviving statements are `KNOWN`. Do not add a Skolem attack. Do
not un-skip matrix-word. Do not claim non-existence. Do not start the
next target automatically.
