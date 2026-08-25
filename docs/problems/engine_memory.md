# Research Engine v2.2 research memory

Status: **EXPLORATORY**

This is an engine-infrastructure campaign. It does **not** add attacks,
claim a new number-theory theorem, or define Research Engine v2.3.
Implementation lives in `research_engine.memory`. The thin descriptor
is `research.engine_memory`.

## Problem

Can frozen Research Engine v2 turn accumulated successes, failures,
counterexamples, limitations, and prior-art findings into persistent
research knowledge that improves target selection and engineering
decisions without contaminating blind mathematical discovery?

## Exact statement

On the frozen attack stack (package 0.2.1 order unchanged), does a
post-run memory layer

1. represent the historical campaign corpus as immutable
   `MemoryExperiment` records;
2. classify failures by a reusable taxonomy rather than `attack=FAIL`;
3. preserve grey loot with evidence status;
4. cluster recurring failures by mathematical signature, not target
   name;
5. separate representation novelty from mathematical novelty;
6. record `MathematicalYield` per experiment;
7. keep scout, attack, grey-loot, and certified machinery on isolated
   lanes;
8. multiply `ExpectedResearchValue` by `FailureLearningValue` only when
   a memory store is supplied?

A failed attack is evidence about the boundary of the current
mathematical language. It is not an instruction to implement a new
attack.

## Current literature

The memory layer is engine methodology, not a number-theory result.
Historical campaigns remain **KNOWN** rediscoveries or **PARK**ed
limitations as recorded in their own dossiers:

- digit-fold saturation: [operator_dynamics_benchmark.md](operator_dynamics_benchmark.md),
  [balanced_ternary_digit_sum_dynamics.md](balanced_ternary_digit_sum_dynamics.md),
  [balanced_ternary_weight_dynamics.md](balanced_ternary_weight_dynamics.md)
- Syracuse / latent control: [syracuse.md](syracuse.md)
- Euclidean / vector affine: [engine_campaign.md](engine_campaign.md)
- Carelli / BB-5: [linear_constraint_loops.md](linear_constraint_loops.md),
  [bb5_map.md](bb5_map.md)
- aliquot: [aliquot_dynamics.md](aliquot_dynamics.md)
- Skolem order 6: [skolem_lrs.md](skolem_lrs.md)

Project relationship: **engine diagnosis**. No new mathematics is
claimed.

## Branch budget

```text
Mathematical target     Can frozen v2 persist experiment history as
                        classified research knowledge without changing
                        attack outputs or leaking scout/grey loot into
                        blind adapters?
Novelty hypothesis      Failure taxonomy + grey loot + novelty split +
                        failure-aware EV is a research-intelligence
                        layer, not new mathematics.
Falsifier               Attack outputs change; grey loot enters a blind
                        adapter; known rediscoveries marked novel;
                        clusters form by target name; a single failure
                        auto-promotes machinery.
Existing machinery      ExperimentRecord, ResearchCorpus,
                        ResearchDecision, score_candidate,
                        NegativeKnowledge, PriorArtStatus, scout/adapter
                        split, seed_baseline_corpus().
Maximum Phase-0 scope   research_engine.memory types + classifier +
                        JSON seed + optional ResearchLoop ingest +
                        tests. No new attacks. No Lean math. No CLI.
Promotion criterion     The twelve v2.2 success criteria.
Stop criterion          Any new attack; involution-census fix; v2.3
                        design; hint injection.
```

## Balanced-ternary formulation

None. Memory records are structured metadata about engine experiments.

## Why BT may be relevant

It is not required. Digit-fold campaigns remain a comparison cluster in
the historical seed.

## Candidate operations / invariants

None. The layer classifies existing evidence. Labels below are
**OBSERVATION** of engine history, not theorems.

- Failure taxonomy (`REPRESENTATION`, `QUANTIFIER`, `GLOBAL_REASONING`,
  `COMPUTATIONAL`, `EXPERIMENT_HYGIENE`, …) — **OBSERVATION**
- Grey loot with evidence status (`OBSERVED` … `CONJECTURAL`) —
  **OBSERVATION**
- Machinery-inflation guard: a single failure does not justify a new
  attack — **OBSERVATION** (policy)

## Experiments

- Seed: `src/research_engine/memory/seed/historical.json` (also
  `research_engine.memory.seed_records.historical_experiments`).
- Tests: `tests/research_engine/memory/test_research_memory.py`.
- Live ingest: `ResearchLoop.run(..., memory=ResearchMemory())` is
  post-run only.

## Conjectures

None. Computational observations are not conjectures.

## Counterexamples

Historical counterexamples are preserved as grey loot (for example
`u_11 < 0` on the order-6 companion shift; descent refuted at aliquot
seed 12). They are not deleted when an invariant fails.

## Formalization

None for the memory layer. Historical records point at existing Lean
modules (`Problems.Engine.CompanionShift`, `Problems.Engine.Syracuse`,
`Problems.Engine.AliquotDynamics`, …). No `sorry`.

## Results

- Historical corpus is loadable and classifies aliquot as
  `REPRESENTATION`, nondeterministic SLC as `QUANTIFIER`, Skolem order 6
  as `GLOBAL_REASONING` plus `COMPUTATIONAL`, and the `skolem_lrs`
  identifier false positive as resolved `EXPERIMENT_HYGIENE`.
- Syracuse / Carelli \(R^+\) / BB-5: representation novelty `HIGH`,
  mathematical novelty `NONE`, status `KNOWN_REDISCOVERY`.
- Global-reachability failures of Skolem, \(R^+\), and BB-5 cluster
  together; the policy emits `PROMOTE_TO_NEXT_VERSION` as **guidance
  only**.
- `score_candidate` without memory is numerically unchanged.
- `ResearchLoop` attack results and `ResearchDecision` are identical
  with and without `memory=`.

## Open questions

Which high-value failure cluster, if any, later justifies a v2.3
abstraction — to be answered by further experiments, not by this
milestone.

## Decision

`PROMOTE` the memory layer into `research_engine` as frozen v2.2
platform machinery. Do not add attacks. Do not implement the involution
census. Do not define v2.3.

Best next question: which frozen-engine target still teaches something
new about an unresolved high-value failure cluster?

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
