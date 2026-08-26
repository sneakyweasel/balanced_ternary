# Frozen Engine campaign: balanced-ternary reverse-plus-add

Status: **EXPLORATORY**

This is the seventh mathematical campaign on frozen Research Engine v2.3
and the second wildcard after the frontier list. It does **not** claim
that every seed reaches a reverse-fixed point. The adapter is a thin
one-variable spec with `affine_system=None`. There is no reverse-add
attack and no palindrome conjecture on the adapter.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the stored balanced-ternary reverse-plus-add map, does frozen v2.3
diagnose a regime distinct from digit-fold saturation and from
factorization or floor-power iteration, without a new reverse-add
attack and without claiming that every seed reaches a reverse-fixed
point?

## Exact statement

On the stored packet `reverse_add_bt` (integers, dummy control,
identity observation, seed \(196\)), with

\[
T(n)=n+W(n),\qquad W=\text{canonical balanced-ternary digit reverse},
\]

does frozen v2.3 recover a class obstruction relevant to reverse-fixed
reachability, or only a finite seed closure plus a missing affine cover?

Computational budget (stored packet): 16 planner steps / 32 residual
states; successor undefined when the bit length exceeds 512.

## Current literature

- OEIS A134028 (`oeis-A134028`): balanced-ternary reversal \(W\).
  **KNOWN** / **REPARAMETERIZATION** for the map \(W\) itself.
- Laboratory digit-sum / signed-fold campaigns: scalar digit-fold
  saturation. **KNOWN**. Comparison cluster, not the same map.
- Laboratory aliquot and floor-power campaigns: factorization
  truncation and even/odd floors. **KNOWN**. Comparison clusters.

Project relationship: **engine diagnosis**. No new number-theory
theorem is claimed. Base-10 reverse-and-add folklore is not imported.

## Branch budget

```text
Mathematical target     On the stored BT reverse-and-add map, does frozen
                        v2.3 diagnose a regime distinct from digit-fold
                        saturation and from factorization/aliquot/juggler
                        floors, without a palindrome theorem and without
                        importing base-10 Lychrel lore?
Novelty hypothesis      An exact palindrome/class obstruction that is not
                        the definition and not a finite seed closure.
Falsifier               Affine cover; palindrome-conjecture language on
                        the adapter; seed-196 halt billed as a Z-theorem;
                        this is digit-fold SignedP0 / aliquot / juggler.
Existing machinery      BT digit reverse already exists in the core;
                        one-variable dummy-control spec pattern;
                        unmodified ResearchLoop.
Maximum Phase-0 scope   Thin packet seed 196; exact reverse-plus-add;
                        prefix probes; live loop; smallest exact Lean.
Promotion criterion     An exact class obstruction that is not the
                        definition.
Stop criterion          All KNOWN/REPARAMETERIZATION; new attack;
                        palindrome totality; base-10 folklore leak.
```

## Balanced-ternary formulation

\(W\) is the existing core digit reverse (MSD reverse of the canonical
word). \(T(n)=n+W(n)\). A reverse-fixed point is an integer with
\(W(n)=n\); then \(T(n)=2n\). The map does not halt there.

## Why BT may be relevant

The transition *is* the core reverse. That is an exact encoding, not a
solving coordinate and not a claim that BT decides reverse-fixed
reachability.

## Candidate operations / invariants

- \(T(0)=0\). **EXACT — LEAN VERIFIED** (`reverseAdd_zero`). **KNOWN**.
- \(T(196)=392\). **EXACT — LEAN VERIFIED**. **KNOWN**. Also \(W(196)=196\).
- \(196\mapsto 392\mapsto -672\mapsto -448\mapsto -824\mapsto 192\mapsto 280\mapsto 560\mapsto 0\)
  in eight steps. **EXACT — LEAN VERIFIED**. **KNOWN**. Not a
  \(\mathbb Z\) theorem.
- \(T(8)=0\), not the floor-power image \(2\). **OBSERVATION**. **REFUTED**
  as identity with the juggler map.
- \(T(196)=392\), not digit-sum \(2\) and not \(\sigma(196)-196=203\).
  **OBSERVATION**. **REFUTED** as digit-fold or aliquot.
- \(W(2)=-2\). **OBSERVATION**. **REFUTED** as “every seed is reverse-fixed”.
- No complete piecewise-affine cover on the sample window.
  **OBSERVATION** (`INCONCLUSIVE`). **KNOWN** (digit reverse).
- Exact residual closure of the packet seed has size 9.
  **EXACT** (engine `SUPPORTED`). Horizon artefact of seed 196.

## Experiments

- `tests/research/reverse_and_add_base3/test_reverse_and_add_base3.py`
- Runner: `research.reverse_and_add_base3.runner.run_campaign`
- Scout (never imported by spec/adapter/planner):
  `research.reverse_and_add_base3.scout`

## Conjectures

None opened. Whether every integer seed eventually hits a reverse-fixed
point remains literature-open and is not restated as a project
conjecture.

## Counterexamples

- “The map is residue-affine.” **REFUTED**: `affine_system is None`;
  successor uses digit reverse; census `INCONCLUSIVE`.
- “Seed 196 reaching 0 is a theorem on all integers.” **REFUTED**.
- “The successor is signed digit-sum.” **REFUTED**: \(T(196)=392\), not \(2\).
- “The successor is \(\sigma(n)-n\).” **REFUTED**: \(T(196)=392\), not \(203\).
- “The successor is the even/odd floor-power map.” **REFUTED**:
  \(T(8)=0\), not \(2\).
- “Every positive seed is reverse-fixed.” **REFUTED** at \(n=2\).
- “Progress requires a new reverse-add attack.” **REFUTED**: exact I/O
  is the definition; the frozen stack diagnoses the regime.

## Formalization

`formal/Problems/Engine/ReverseAdd.lean`. Identities
`reverseAdd_zero`, `reverseAdd_one_ninety_six_step`,
`reverseAdd_one_ninety_six_reaches_zero`. No `sorry`. No ledger row
(KNOWN).

## Results

See sections A–L below.

## Open questions

Whether every integer seed eventually hits a reverse-fixed point. An
eight-step orbit of seed 196 is not that theorem.

## Decision

**CLOSE**. Frozen v2.3 recovered the packet-seed finite closure and
refused a piecewise-affine cover. The identities are elementary. The
fingerprint (`FINITE_SEED_CLOSURE`) is distinct from digit-fold
saturation, aliquot factorization truncation, and floor-power closure,
which answers the board's failure-learning question without a new
attack. All surviving statements are `KNOWN`. Laboratory decision
`CLOSE`. Engine `ResearchDecision` may still be `CONTINUE`.

Best next question: the unmodified leftover pick on the board after
this ingest. What exact obstruction, if any, can frozen v2.3 produce
there without new attacks? Do not add a reverse-add attack. Do not
start that leftover in this branch.

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`ReverseAddSpec` / `reverse_add_bt`):

- state space integers;
- dummy singleton control;
- identity observation;
- seed \(196\);
- successor \(n\mapsto n+W(n)\) with core \(W\);
- budget 16 planner steps / 32 residual states.

No named conjecture, palindrome language, or open-problem status in
`spec.py` / `adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `TERMINATION` selected
`global_inductive` and returned no attack results (no ranking-function
attack on the frozen stack).

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`,
  `FINITE_CONTRACTING`, `FINITE_SEED_CLOSURE`, `EXACT_CLOSURE`,
  piecewise-affine `UNCERTAIN`, affine control `UNOBSERVED`.
- `ResearchDecision`: **CONTINUE** — new structural regime with an
  exact certificate (the seed-196 closure). That certificate is not a
  map theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | INCONCLUSIVE; no complete cover |
| closure | SUPPORTED; size 9 |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | SUPPORTED |
| parameter_domain / control_word / vector_affine / matrix_word | INAPPLICABLE |

### D. Class analysis

Reverse-fixed integers satisfy \(T(n)=2n\) and are not fixed points
unless \(n=0\). Seed 196 is reverse-fixed and then leaves that class.
The orbit enters the fixed point \(0\) in eight steps. No residue
class was found that forces all orbits to a reverse-fixed point.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| seed 196 reaches 0 | yes | independently | **KNOWN** |
| \(T(0)=0\) | yes | independently | **KNOWN** |
| no affine cover | yes | independently | **KNOWN** |
| universal reverse-fixed reachability | open | not obtained | not yield |
| distinct from digit-fold / aliquot / floors | hypothesized | yes on this seed | **OBSERVATION** |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| \(T(0)=0\) | **EXACT — LEAN VERIFIED** |
| seed-196 eight-step orbit | **EXACT — LEAN VERIFIED** |
| residue-affine cover | **not obtained** |
| reverse-fixed reachability on all integers | **not obtained** |

### G. Mathematical yield

```text
known_rediscoveries:     seed-196 orbit; missing affine cover
new_exact_results:       reverseAdd_zero / one_ninety_six_step / reaches_zero
new_invariants:          none
new_obstructions:        none
new_counterexamples:     T(196)=392 vs digit-sum/aliquot; T(8)=0 vs floor-power; W(2)=-2
new_conjectures:         none
new_formalizations:      Problems.Engine.ReverseAdd
potentially_new_mathematics: none
unresolved_questions:    whether every integer seed hits a reverse-fixed point
engineering_changes:     0
representation_novelty:  MEDIUM
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` plus a `DISTINCT_REGIME`
fingerprint versus digit-fold / aliquot / floor-power. Not
`POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

`REPRESENTATION` (no affine cover). Not `GLOBAL_REASONING`: reverse-fixed
reachability on \(\mathbb Z\) is out of scope. Grey loot ids
`reverse_add_bt:loot:mismatch`, `:seed196`, `:cluster`. Juggler loot
that listed this target as transfer is `REUSED`.

### I. Prior-art reconciliation

OEIS A134028 records \(W\). It does not supply a class obstruction this
campaign missed. The laboratory identities are the packet-seed orbit.
Base-10 reverse-and-add status is not a theorem here.

### J. Lean

`Problems.Engine.ReverseAdd`. Strongest exact theorem:
`reverseAdd_one_ninety_six_reaches_zero`. No `sorry`.

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
close because the finite orbit is KNOWN, there is no affine cover,
and no class forces all seeds to a reverse-fixed point. Do not add a
reverse-add attack. Do not claim totality. Do not import base-10
folklore. Do not start the next target automatically.
