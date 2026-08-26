# Frozen Engine campaign: encoded binary-word rewrite

Status: **EXPLORATORY**

This is the ninth mathematical campaign on frozen Research Engine v2.3
and the last unrun board wildcard. It does **not** claim universality
and does not add a tag-system attack. The adapter is a thin one-variable
spec: a sentinel integer encoding of a `{0,1}`-word, successor the
rewrite that drops the first symbol and appends `0` or `11`, halt on
empty, observation word length, `affine_system=None`.

CLI is not required. Tests invoke `ResearchLoop` and
`StrategyPlanner` in-process.

## Problem

On the stored `0|->0`, `1|->11` rewrite with halt on empty, does frozen
v2.3 diagnose a representation mismatch for an integer encoding of
words, without a new rewrite attack and without a universality claim?

## Exact statement

On the stored packet `cyclic_tag_bit` (binary words encoded as integers,
dummy control, length observation, seed `101`), with

- empty has no successor;
- `0w \mapsto w0`;
- `1w \mapsto w11`;

does frozen v2.3 recover a class obstruction relevant to reaching empty,
or only a missing affine cover plus an expanding encoded prefix?

Computational budget (stored packet): 16 planner steps / 32 residual
states; successor undefined when the word length exceeds 64.

## Current literature

- Baader–Nipkow 1998 (`baader-nipkow-1998-term-rewriting`): term
  rewriting textbook. **KNOWN** method source. Not a tag-system
  completeness theorem for this production.

Project relationship: **engine diagnosis**. No new rewriting theorem is
claimed.

## Branch budget

```text
Mathematical target     On the stored 0|->0, 1|->11 rewrite (halt on empty),
                        does frozen v2.3 diagnose a representation mismatch
                        for word rewriting encoded as an integer, without a
                        tag-system attack and without a universality claim?
Novelty hypothesis      An exact halt obstruction that is not the definition
                        and not an encoding artefact.
Falsifier               Affine cover of the encoded map; adapter leak of
                        universality; seed-101 halt billed as a Z-theorem;
                        a new tag attack.
Existing machinery      One-variable dummy-control spec; ResearchLoop;
                        integer encoding of words.
Maximum Phase-0 scope   Thin packet seed 101; exact rewrite; probes; live
                        loop; smallest exact Lean (empty iff halt; length).
Promotion criterion     Exact obstruction that is not the definition.
Stop criterion          All KNOWN/REPARAMETERIZATION; new attack;
                        universality claims; folklore leak.
```

## Balanced-ternary formulation

None.

## Why BT may be relevant

It is not required. The encoding is ordinary binary.

## Candidate operations / invariants

- Empty has no successor. **EXACT — LEAN VERIFIED** (`tagStep_nil`).
  **KNOWN**.
- `[0]` is fixed. **EXACT — LEAN VERIFIED**. **KNOWN**.
- `101 \mapsto 0111`. **EXACT — LEAN VERIFIED**. **KNOWN**.
- Length never decreases when a successor exists.
  **EXACT — LEAN VERIFIED** (`tagStep_length_ge`). **KNOWN**. Immediate
  from the productions; nonempty words do not reach empty in one step.
- Seed `101` grows on the 16-step / 32-state horizon.
  **OBSERVATION**. Not an integer halt theorem.
- No complete piecewise-affine cover on the sample window.
  **OBSERVATION** (`INCONCLUSIVE`). **KNOWN** (word rewrite).
- Residual BFS hits the cap 32. **OBSERVATION** (`INCONCLUSIVE`).
  Horizon artefact.

## Experiments

- `tests/research/cyclic_tag_bit/test_cyclic_tag_bit.py`
- Runner: `research.cyclic_tag_bit.runner.run_campaign`
- Scout (never imported by spec/adapter/planner):
  `research.cyclic_tag_bit.scout`

## Conjectures

None opened.

## Counterexamples

- “The encoded map is residue-affine.” **REFUTED**: `affine_system is None`;
  census `INCONCLUSIVE`.
- “The frozen integer stack proves the seed reaches empty.” **REFUTED**.
- “The successor is an affine map of the encoded integer.” **REFUTED**.
- “A nonempty window word maps to empty in one step.” **REFUTED**:
  length nondecrease; `[0]` fixed.
- “Progress requires a new tag-system attack.” **REFUTED**: exact I/O
  is the definition; the frozen stack diagnoses the mismatch.

## Formalization

`formal/Problems/Engine/CyclicTag.lean`. Identities `tagStep_nil`,
`tagStep_zero_fixed`, `tagStep_seed_one_zero_one`, `tagStep_length_ge`.
No `sorry`. No ledger row (KNOWN).

## Results

See sections A–L below.

## Open questions

None on this production: nonempty length never drops, so empty is only
reached from empty. That is the rewrite, not a new theorem.

## Decision

**CLOSE**. Frozen v2.3 recovered an expanding encoded prefix, refused a
piecewise-affine cover, and hit the residual cap. The Lean identities
are the problem definition. The fingerprint (`EXPANDING`,
`UNBOUNDED_SAMPLE`, `COARSE_OBSERVATION`) is the board's predicted
word/integer mismatch. Failure-learning is low-value obvious
incompatibility, as the protocol already said. All surviving statements
are `KNOWN`. Laboratory decision `CLOSE`. Engine `ResearchDecision` may
still be `CONTINUE`.

Best next question: none on the stored board; every named target is
now run. Do not add a tag-system attack. Do not open a new board.

## Publication assessment

Status: `EXPLORATORY`. No paper candidate.

---

### A. Blind target specification

What the engine received (`WordRewriteSpec` / `cyclic_tag_bit`):

- state a sentinel encoding of a `{0,1}`-word;
- dummy singleton control;
- observation word length;
- seed `101`;
- successor the stored rewrite;
- budget 16 planner steps / 32 residual states.

No named conjecture, universality language, or open-problem status in
`spec.py` / `adapter.py` / `planner.py`. Scout is not imported there.

### B. Diagnosis

Memory-free `StrategyPlanner` with goal `TERMINATION` selected
`global_inductive` and returned no attack results.

Live `ResearchLoop` on the stored packet:

- `RegimeFingerprint`: `INTEGER_1D`, `SINGLETON`, `EXPANDING`,
  `UNBOUNDED_SAMPLE`, `INCOMPLETE`, `BOUNDED`, piecewise-affine
  `UNCERTAIN`, affine control `UNOBSERVED`, compression
  `COARSE_OBSERVATION`.
- `ResearchDecision`: **CONTINUE** — structurally distant non-finite
  regime with a bounded certificate. That certificate is not a halt
  theorem.

Planner output with empty `ResearchMemory()` was identical to the
memory-free run.

### C. Existing attack results

| Attack | Status |
|--------|--------|
| reconnaissance | OBSERVATION |
| piecewise_affine | INCONCLUSIVE; no complete cover |
| closure | INCONCLUSIVE; cap 32 |
| functional | REFUTED |
| separation | SUPPORTED |
| quotient | INCONCLUSIVE |
| parameter_domain / control_word / vector_affine / matrix_word | INAPPLICABLE |

### D. Class analysis

Empty is the unique word with no successor. All-zero words are fixed.
Length is nondecreasing, so nonempty words do not reach empty. Seed
`101` grows. No residue class of the encoding was found that forces
empty.

### E. Scout / blind comparison

| Candidate | Scout | Blind | Classification |
|-----------|-------|-------|----------------|
| empty has no successor | yes | independently | **KNOWN** |
| `101 \mapsto 0111` | yes | independently | **KNOWN** |
| no affine cover | yes | independently | **KNOWN** |
| integer encoding mismatch | hypothesized | yes | **KNOWN** |
| seed reaches empty | no | not obtained | not yield |

### F. Invariants and quotients

| Candidate | Status |
|-----------|--------|
| empty has no successor | **EXACT — LEAN VERIFIED** |
| length nondecrease | **EXACT — LEAN VERIFIED** |
| residue-affine cover | **not obtained** |
| finite residual closure | **not obtained** |

### G. Mathematical yield

```text
known_rediscoveries:     empty halt; length nondecrease; missing affine cover
new_exact_results:       tagStep_nil / zero_fixed / seed 101 / length_ge
new_invariants:          none
new_obstructions:        none beyond the definition
new_counterexamples:     nonempty window words do not drop length
new_conjectures:         none
new_formalizations:      Problems.Engine.CyclicTag
potentially_new_mathematics: none
unresolved_questions:    none on this production
engineering_changes:     0
representation_novelty:  HIGH
mathematical_novelty:    NONE
```

Classification: `KNOWN_REDISCOVERY` plus the predicted
`REPRESENTATION_MISMATCH`. Not `POTENTIALLY_NEW_THEOREM`.

### H. Failure-memory update

`REPRESENTATION` (no affine cover; word vs integer). Not
`GLOBAL_REASONING`: halt of nonempty words is settled by the length
lemma and is out of engine scope. Grey loot ids
`cyclic_tag:loot:mismatch`, `:seed101`, `:cluster`.

### I. Prior-art reconciliation

Baader–Nipkow is a rewriting textbook. It does not supply a class
obstruction this campaign missed. The laboratory identities are the
productions.

### J. Lean

`Problems.Engine.CyclicTag`. Strongest exact theorem:
`tagStep_length_ge`. No `sorry`.

### K. ResearchLoop / StrategyPlanner

Memory ingest did not change flood-planner output. Blind
`StrategyPlanner(TERMINATION)` selected `global_inductive` with empty
results. After this ingest the board has no unrun leftover.

### L. Final decision

```text
CLOSE
```

Engine `ResearchDecision` was `CONTINUE`. Laboratory and campaign close
because the identities are KNOWN, the mismatch was predicted, and no
tag-system attack is allowed. Do not claim universality. Do not start
a new target automatically.
