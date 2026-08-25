# Frozen Engine campaign: switching affine Z^2 origin

Status: **EXPLORATORY**

This is an engine-capability campaign on the stored two-path integer
loop in \(\mathbb Z^2\). It does **not** claim a multi-path termination
decision procedure. Adapters live in `research.switching_affine_z2_origin`.
There is no `SwitchingAffineAttack`.

CLI is not required. Tests invoke `ResearchLoop` in-process.

## Problem

Can frozen Research Engine v2 derive a nontrivial exact obstruction,
invariant, quotient, or origin-avoidance result for the board target
`switching_affine_z2_origin` using only existing attacks?

## Exact statement

On the hint-free adapter whose transition is exactly the stored blind
packet

```text
if y >= 1 then (x,y):=(x+y, y-1)
else if x >= 1 then (x,y):=(x-1, x+y)
else halt
```

with seed \((3,2)\) and dummy control, does unmodified `ResearchLoop`
recover useful structure, and can exact post-run analysis certify a
class-level origin fact without new attacks?

Computational budget (stored packet): 16 planner steps / 32 residual
states.

## Current literature

- Ben-Amram–Genaim–Ouaknine–Worrell 2025 termination survey
  (`ben-amram-genaim-ouaknine-worrell-2025-termination-survey`). **KNOWN**.
- Hosseini–Ouaknine–Worrell 2019: affine integer-loop termination is
  decidable (`hosseini-ouaknine-worrell-2019-termination-linear-loops`).
  **THEOREM**.
- Multi-path integer loops remain open in general. **UNKNOWN**.

Project relationship: **engine diagnosis**. The class obstruction below
is an elementary consequence of this explicit map, not a new termination
theorem for the open multi-path class.

## Branch budget

```text
Mathematical target     Can frozen v2 cash out existing 2-D affine
                        machinery on the stored two-path loop?
Novelty hypothesis      A class origin-avoidance or finite quotient,
                        not mere rediscovery of the two branches.
Falsifier               Adapter leaks ranking/modulus; new attacks;
                        finite closure billed as a global basin.
Existing machinery      Unmodified ResearchLoop; vector_affine;
                        control-word; obstruction; closure; v2.2 memory.
Maximum Phase-0 scope   Blind spec = stored packet; one ResearchLoop;
                        post-run probes; Lean; dossier.
Promotion criterion     Exact class obstruction or basin theorem.
Stop criterion          New attack; 2-adic solver; census repair.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

- Unit 2-cycle \((1,0)\leftrightarrow(0,1)\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- Origin preimages \((-1,1)\) and \((1,-1)\). **EXACT — LEAN VERIFIED**. **KNOWN**.
- Nonnegative orthant is invariant. **EXACT — LEAN VERIFIED**. **KNOWN**.
- Nonnegative non-origin states never reach the origin.
  **EXACT — LEAN VERIFIED**. **KNOWN** (elementary).
- Seed \((3,2)\) does not reach the origin. **EXACT — LEAN VERIFIED** as
  an instance of the class fact. **KNOWN**.
- Two affine pieces recovered by `vector_affine`. **OBSERVATION**
  (FINITE_CENSUS; window agreement is not a \(\mathbb Z\)-theorem).
- Image-kernel matrix-word cycle obstruction on a 2-letter alphabet.
  **COMPUTATIONALLY VERIFIED** as a generic cycle constraint, not an
  origin-reachability theorem.

## Experiments

- `tests/research/switching_affine_z2_origin/test_switching_affine_z2_origin.py`
- Runner: `research.switching_affine_z2_origin.runner.run_campaign`
- Scout (never imported by the adapter): `research.switching_affine_z2_origin.scout`

## Conjectures

None opened.

## Counterexamples

- “\((3,2)\) reaches the origin on the search bound.” **REFUTED**.
- “Every small nonnegative seed reaches the origin.” **REFUTED**.
- “There is no period-2 orbit.” **REFUTED** at \((1,0)\leftrightarrow(0,1)\).
- “The start orbit is finite within the bound.” **REFUTED**.
- “Finite residual BFS is a global basin.” **REFUTED**: closure cap 32,
  `complete=false`, origin absent from the truncated union.

## Formalization

`formal/Problems/Engine/TwoPathZ2.lean`. KNOWN identities, including
`two_path_nonneg_never_origin`. No `sorry`. No ledger row.

## Results

See sections A–L below.

## Open questions

Does the loop terminate from every seed in \(\mathbb Z^2\)? Origin
reachability on \(\mathbb N_0^2\) is classified: only \((0,0)\) is
already at the origin; the unit pair cycles; the seed \((3,2)\) grows
on the window. Signed seeds can reach the origin in one step.

## Decision

**CLOSE**. The frozen stack recovered the two declared affine pieces
and a generic image-kernel cycle obstruction. The exact origin
statement is elementary from those pieces: \(\mathbb N_0^2\setminus\{(0,0)\}\)
never reaches the origin. All statements are `KNOWN`. Laboratory
decision `CLOSE`. Campaign label in section L is `CLOSE`.

Best next question: the unmodified leftover pick was `cyclic_tag_bit`.
What representation mismatch, if any, does that wildcard still teach?

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`TwoPathZ2Spec` / `two_path_z2`):

- state space \(\mathbb Z^2\);
- dummy singleton control;
- observation both coordinates;
- seed \((3,2)\);
- successor the stored two-path rule;
- halt when neither guard holds;
- accepting iff \((0,0)\);
- budget 16 planner steps / 32 residual states.

No ranking, modulus, literature name, or scout import in
`spec.py` / `adapter.py` / `planner.py`.

### B. Diagnosis

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_VECTOR`, `SINGLETON`, `FINITE`
  piecewise-affine structure, `VECTOR` affine control, `UNBOUNDED_SAMPLE`,
  orbit `INCOMPLETE`, certificate `BOUNDED`, latent control `FINITE`,
  algebra `EXPLOITABLE`, obstruction scope `CLASS`.
- `StructuralDelta`: `HIGH` vs nearest `syracuse`.
- `FamilyStatus`: `ACTIVE`; family id `unclassified`.
- `CapabilityCoverage`: `latent_vector_affine_control` and
  `matrix_word_recursive_invariant` exercised; scalar piecewise /
  parameter-domain / modular / block / reverse inapplicable.
- `ExpectedResearchValue`: memory-aware leftover scores collapsed to
  \(0\) among remaining unrun targets after this ingest.
- `ResearchDecision`: **CONTINUE** — “finite piecewise-affine census on
  a structurally distant regime; window agreement is not a Z-theorem.”

Comparison: this is not saturated digit-fold, not scalar \(mx+r\), not
Carelli \(R^+\), not BB-5, not companion-window Skolem/Positivity. It is
a distinct low-dimensional deterministic switching-affine regime whose
two pieces the existing vector census can see.

Planner output with `memory=ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | INAPPLICABLE |
| parameter_domain | INAPPLICABLE |
| control_word | INAPPLICABLE |
| control_obstruction | INAPPLICABLE |
| vector_affine | OBSERVATION; `FINITE_CENSUS`; 2 branches |
| matrix_word_invariant | SUPPORTED; CLASS image-kernel |
| closure | INCONCLUSIVE; cap 32; union 33; not complete |
| modular | INAPPLICABLE |
| functional | INAPPLICABLE |
| affine | INAPPLICABLE |
| reverse | INAPPLICABLE |
| block | INAPPLICABLE |
| spectral | INAPPLICABLE |
| factorization | INAPPLICABLE |
| separation | SUPPORTED; \((3,2)\) vs \((5,1)\) by a word of length 1 |
| quotient | INCONCLUSIVE; needs an exact finite reachable set |
| symmetry | INAPPLICABLE |
| symbolic | SKIPPED |

Recovered branches (sample-supported, not billed as a \(\mathbb Z\)-theorem):

\[
(x,y)\mapsto (x+y,\,y-1)
\qquad
(x,y)\mapsto (x-1,\,x+y).
\]

Strongest engine exact claim: “matrix-word class obstruction with a
preserved arithmetic predicate” (`c \notin \operatorname{im}_{\mathbb Z}(M-I)`
on the 2-letter alphabet). That is a cycle obstruction, not an
origin-reachability obstruction.

### D. Origin analysis

- Exact witness of origin from \((3,2)\): none.
- Exact non-reachability: \(\mathbb N_0^2\setminus\{(0,0)\}\) never
  reaches \((0,0)\). **EXACT — LEAN VERIFIED**.
- Certified finite basin: none global. Closure on the seed is
  `COMPUTATION_EXHAUSTED` / incomplete (`CERTIFIED_ON_WINDOW` only as
  “origin absent from a 32-state BFS”).
- Empirical basin: small nonnegative seeds \(\{0,\ldots,8\}^2\) do not
  hit the origin except the origin itself.
- Global basin theorem: not claimed. Finite non-visit is not a basin.
- Cycles: \((1,0)\leftrightarrow(0,1)\), disjoint from the origin.

### E. Control analysis

Singleton dummy control in the blind packet. Scalar `control_word` /
`control_obstruction` inapplicable. Vector census supplies a 2-letter
latent alphabet for `matrix_word_invariant` only. No origin-specific
impossible-word family was emitted.

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| nonnegative orthant | **PROVED** / **LEAN_CERTIFIED** |
| origin preimage restriction | **PROVED** / **LEAN_CERTIFIED** |
| unit 2-cycle | **PROVED** / **LEAN_CERTIFIED** |
| image-kernel cycle predicate | **FINITE_RANGE_SUPPORTED** / engine **PROVED** as CLASS |
| finite origin-reachability quotient | not obtained; quotient attack inconclusive |

### G. Mathematical yield

```text
known_rediscoveries:     two affine branches; image-kernel cycle obstruction
new_exact_results:       two_path_nonneg_never_origin and supporting identities
new_invariants:          nonnegative orthant
new_obstructions:        N^2 \ {(0,0)} never reaches (0,0)
new_origin_reachability_results: none; (3,2) does not reach (0,0)
new_nonreachability_results:     N^2 class obstruction
new_quotients:           none promoted
new_control_constraints: singleton dummy; 2-letter latent alphabet only
new_counterexamples:     (3,2) origin; universal small-seed origin; no 2-cycle
new_conjectures:         none
new_formalizations:      Problems.Engine.TwoPathZ2
potentially_new_mathematics: none
unresolved_questions:    termination on all of Z^2
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
failure_learning_value:  this is not GLOBAL_REASONING
```

Classification: `KNOWN_REDISCOVERY` of the local map, plus
`NEW_FORMALIZATION` of an elementary class fact. Not
`POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

No `GLOBAL_REASONING` record. The structural distinction vs Skolem /
Positivity:

> Skolem and Positivity failed because infinite-time zero / half-space
> certificates were inaccessible. This target yields an exact finite
> preimage obstruction on \(\mathbb N_0^2\) before that barrier.

Grey loot stored: unit 2-cycle; \(\mathbb N_0^2\) invariance and origin
preimages; “not the global-reasoning cluster.”

### I. Prior-art reconciliation

Affine SLC decidability does not decide this two-path instance as a
class. The origin fact here does not resolve multi-path termination.
The two recovered matrices are the problem definition. The image-kernel
predicate is the existing matrix-word method. The \(\mathbb N_0^2\)
avoidance argument is elementary arithmetic, independently of the
termination surveys.

### J. Lean

`Problems.Engine.TwoPathZ2`. Strongest exact theorem:
`two_path_nonneg_never_origin`. No `sorry`.

### K. ResearchLoop

Memory ingest did not change planner output. Next leftover target
selected automatically (no override): `cyclic_tag_bit`. Remaining
unrun EV scores were \(0\) under the post-run memory-aware formula;
the pick is alphabetical among those leftovers. The candidate is on
the board and is not the current target, so it was not overridden.

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE` (finite census on a distant
regime). Laboratory and campaign close because the mathematical
statements are all `KNOWN` elementary consequences of the stored map.
Do not add a switching-affine attack. Do not repair the census. Do
not treat truncated closure as a basin.
