# Frozen Engine campaign: 5x-4 one-variable strip

Status: **EXPLORATORY**

This is the second mathematical campaign on frozen Research Engine v2.3.
It does **not** claim termination of \(\lfloor 5x/4\rfloor\), a proof or
refutation of the Reachability Conjecture, or a Collatz theorem. The
adapter reuses `OneVariableLoopSpec`. There is no new attack.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the hint-free strip \(5x-4\le 4x'\le 5x-1\) with \(x\ge 2\), does
frozen v2.3 recover a class or branch obstruction relevant to losing
the successor, without rediscovering the 4/3 SLC language as the yield?

## Exact statement

On the stored packet `floor_5x4_strip` (seed \(x=5\), dummy control,
identity observation), does frozen v2.3 recover a restriction that
prevents, constrains, or forces loss of the successor, without billing
a universal halt and without taking the 4/3 reconstruction as success?

Computational budget (stored packet): 16 planner steps / 32 residual
states.

## Current literature

- Carelli, *Loop Termination and Generalized Collatz Sequences*, ICALP
  2026 (`carelli-2026-loop-termination`). One-variable integer SLCs;
  cyclic traces of length at most two. **KNOWN**.
- Matthews–Watts 1984 (`matthews-watts-1984-generalization-hasse`).
  Generalized Collatz maps; Uniform Distribution / Reachability.
  **KNOWN**.
- Ben-Amram–Genaim–Ouaknine–Worrell 2025 termination survey
  (`ben-amram-genaim-ouaknine-worrell-2025-termination-survey`).
  **KNOWN**.
- Laboratory 4/3 strip \(R^+\): unique successor on a length-2 interval
  over modulus 3; successor can be undefined. **KNOWN**
  (`rplusRel_unique`).

Project relationship: **engine diagnosis / elementary arithmetic**.
Unique successor on a length-4 interval over modulus 4 is not a new
number-theory theorem.

## Branch budget

```text
Mathematical target     On 5x-4 ≤ 4x' ≤ 5x-1 (x≥2), does frozen v2.3
                        recover a class/branch obstruction relevant to
                        losing the successor?
Novelty hypothesis      A 5/4-specific obstruction, not the Carelli R+
                        reparameterization, not a finite-window halt.
Falsifier               Unique successor always exists and never drops;
                        yield is only residue-affine reconstruction;
                        halt is a horizon artefact; image class ≠ basin.
Existing machinery      OneVariableLoopSpec; integer_images;
                        StrategyPlanner census_obstruction;
                        LinearConstraintLoops.lean; ResearchMemory.
Maximum Phase-0 scope   Scout+blind at seed 5, horizon≤16, residual≤32;
                        falsify; smallest exact statement; Lean.
Promotion criterion     Exact obstruction that is not the 4/3 analogue
                        and is not a universal-halt claim.
Stop criterion          Candidates fail structurally, or yield is only
                        KNOWN / REPARAMETERIZATION.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Unique successor for every \(x\ge 2\). **EXACT — LEAN VERIFIED**
  (`floor54Rel_unique`, `floor54Rel_exists`). **KNOWN**.
- Cleared lines \(4y\in\{5x-1,5x-2,5x-3,5x-4\}\). **EXACT — LEAN VERIFIED**
  (`floor54Rel_clear`). **KNOWN**.
- A defined successor stays in \(x\ge 2\). **EXACT — LEAN VERIFIED**
  (`floor54Rel_stays`). **KNOWN**.
- Engine census: four residue-affine branches \(4y=5x-r\).
  **OBSERVATION** on the sample window; **DISCOVERED** (not
  adapter-given). Mathematics **REPARAMETERIZATION** of the 4/3 SLC
  language.
- Fixed points \(2,3,4\). **EXACT** on the relation. **KNOWN**.
- Seed \(5\) grows on horizons \(16\) and \(32\). **OBSERVATION**; not
  a halt theorem and not divergence.

## Experiments

- `tests/research/weak_collatz_floor_5x4_rplus/test_weak_collatz_floor_5x4_rplus.py`
- Runner: `research.weak_collatz_floor_5x4_rplus.runner.run_campaign`
- Scout (never imported by the adapter):
  `research.weak_collatz_floor_5x4_rplus.scout`

## Conjectures

None opened. The Reachability Conjecture for the weak map
\(T(x)=\lfloor 5x/4\rfloor\) remains literature-open and is **not**
this closed-strip spec.

## Counterexamples

- “Rediscovering the 4/3 SLC language is the yield.” **REFUTED** as a
  campaign success criterion: that language is KNOWN infrastructure.
- “This strip is the 4/3 loop.” **REFUTED**: the inequality map sends
  \(8\mapsto 9\); \(R^+\) sends \(8\mapsto 10\).
- “Every orbit loses its successor.” **REFUTED**: unique successor on
  \(x\ge 2\); fixed points \(2,3,4\); seed \(5\) grows.
- “Finite seed halt on the budget is a map theorem on \(\mathbb Z\).”
  **REFUTED**: seed \(5\) does not halt on horizons \(16\) or \(32\).
- “A residue image class excludes a basin of losing the successor.”
  **REFUTED**: every residue class modulo \(4\) still has a successor.
- “The 4/3 strip is likewise total on its domain.” **REFUTED**: \(R^+\)
  is undefined at \(x\equiv 0\pmod 3\) (e.g. \(x=3\)).
- “Widening the window inside the budget changes uniqueness.”
  **REFUTED**.

## Formalization

`formal/Problems/Engine/LinearConstraintLoops.lean`. Identities
`floor54Rel_unique`, `floor54Rel_clear`, `floor54Rel_exists`,
`floor54Rel_stays`. No `sorry`. No ledger row (KNOWN).

## Results

See sections A–L below.

## Open questions

The board’s weak-map question (halt when hitting a multiple of \(4\))
is a **different spec**. On this closed strip the successor is total
and stays in the domain. Do not restate the Reachability Conjecture as
a project conjecture.

## Decision

**CLOSE**. Frozen v2.3 recovered four residue-affine branches
\(4y=5x-r\), a `FINITE_CENSUS` reparameterization of the 4/3 SLC
language. The exact 5/4-specific statements are elementary: the
interval length equals the modulus, so a unique successor exists for
every \(x\ge 2\) and stays in the domain. Losing the successor is
false. All surviving statements are `KNOWN` or `REPARAMETERIZATION`.
Laboratory decision `CLOSE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks?

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`OneVariableLoopSpec` / `floor_5x4_strip`):

- state space integers with guard \(x\ge 2\);
- dummy singleton control;
- identity observation;
- seed \(5\);
- successor the unique integer \(x'\) with \(5x-4\le 4x'\le 5x-1\) when
  it exists;
- budget 16 planner steps / 32 residual states.

No named conjecture, residue partition, or cycle theorem in
`spec.py` / `adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `CYCLE_EXCLUSION` selected
`census_obstruction`. Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`, `FINITE` piecewise-affine
  / latent control, `SCALAR` affine control, `EXPANDING`,
  `UNBOUNDED_SAMPLE`, obstruction `CLASS`.
- `ResearchDecision`: **CONTINUE** — finite census on a structurally
  distant regime; window agreement is not a \(\mathbb Z\)-theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | OBSERVATION; `FINITE_CENSUS`; 4 branches \(p=5,q=4\) |
| parameter_domain | OBSERVATION; window-exact residues mod 4 |
| control_word | SUPPORTED; 36 words |
| control_obstruction | SUPPORTED; class-level cycle words |
| closure | INCONCLUSIVE |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | INCONCLUSIVE |

The class-level engine obstructions are generic cycle constraints.
They classify words, they do not force loss of the successor.

### D. Class analysis

On the closed strip, four consecutive integers always contain exactly
one multiple of \(4\). Hence the graph is a total function for
\(x\ge 2\). The successor stays \(\ge 2\) (`floor54Rel_stays`). Fixed
points: \(2,3,4\). Seed \(5\) is expanding on the budget.

The board question “hit a multiple of \(4\)” is the **weak-map**
formulation, which makes the successor undefined when \(4\mid x\).
That is not the stored inequality.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| residue-affine branches \(4y=5x-r\) | yes | yes | common; **REPARAMETERIZATION** of 4/3 |
| generic cycle-word obstructions | yes | yes | common; **KNOWN** |
| unique successor / never drops | after contrast with \(R^+\) | independently from I/O | independently rediscovered; **KNOWN** |
| every orbit loses successor | hypothesized | refuted | false lead |
| this is the 4/3 loop | — | refuted at \(8\) | false lead |
| finite halt is a \(\mathbb Z\)-theorem | forbidden | refuted | false lead |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| unique successor on \(x\ge 2\) | **PROVED** / **LEAN_CERTIFIED** |
| successor stays in the domain | **PROVED** / **LEAN_CERTIFIED** |
| \(4y=5x-r\) on residues mod 4 | **OBSERVATION** on the window; relation exactness as in ParameterDomain |
| losing-successor basin | **REFUTED** |
| finite origin-reachability quotient | not obtained |

### G. Mathematical yield

```text
known_rediscoveries:     4y=5x-r branches; generic cycle-word obstructions
new_exact_results:       floor54Rel_exists / unique / stays
new_invariants:          total successor on x>=2
new_obstructions:        none
new_counterexamples:     2,3,4 fixed; seed 5 grows; strip(8)=9 vs R+(8)=10
new_conjectures:         none
new_formalizations:      Problems.Engine.LinearConstraintLoops floor54Rel
potentially_new_mathematics: none
unresolved_questions:    weak-map halt is a different spec
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` / `REPARAMETERIZATION` of the 4/3
SLC language, plus `NEW_FORMALIZATION` of an elementary definedness
fact. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

No `GLOBAL_REASONING` record. Definedness is a finite-modulus fact, not
an infinite-time certificate. Grey loot stored: unique successor;
never-drops counterexamples; 4-branch census is not a halt obstruction.

### I. Prior-art reconciliation

Carelli Example 4.26 is the 4/3 strip, not this inequality. Matthews–
Watts discuss weak maps that become undefined on a residue class. The
identity “four consecutive integers contain one multiple of 4” is
immediate. The 5/4-specific comparison with \(R^+\) is that interval
length equals the modulus here and does not there. That comparison is
elementary, not new.

### J. Lean

`Problems.Engine.LinearConstraintLoops`. Strongest exact theorem:
`floor54Rel_exists`. Supporting `floor54Rel_unique`, `floor54Rel_clear`,
`floor54Rel_stays`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction`.
Next leftover target is selected automatically (no override).

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE` (finite census on an unbounded
sample). Laboratory and campaign close because losing the successor is
false on this spec, and the surviving statements are `KNOWN` elementary
arithmetic or a `REPARAMETERIZATION` of the 4/3 campaign. Do not add a
5/4 attack. Do not expand the census. Do not claim halt or divergence.
Do not start the next target automatically.
