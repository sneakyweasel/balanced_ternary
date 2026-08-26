# Research Engine v2.2 research target board

Status: **EXPLORATORY**

This is laboratory intelligence for frozen Research Engine v2.2. It does
**not** add attacks, thaw the planner, or solve any open problem.
Machine-readable records live in `research_engine.memory`. The thin
descriptor is `research.target_board`.

## Problem

Can frozen v2.2 enter a campaign knowing what failed, why it failed,
what was salvaged, which failures recur, and which mathematical targets
are most likely to turn existing machinery into new mathematics?

## Exact statement

On the frozen 0.2.1 attack stack, do the persistent artifacts

1. represent every listed historical lesson as `GreyLoot`;
2. group recurring failures into named clusters by mathematical meaning;
3. separate representation novelty from mathematical novelty;
4. assemble at least 15 `ResearchTarget` records in three pools;
5. attach a prior-art dossier and a hint-free `BlindPacket` to each
   recommended target;
6. rank candidates with existing `ExpectedResearchValue`
   \((distance \times capability\_gap \times novelty \times failure\_learning)/cost\);
7. emit a protocol campaign order
   known → frontier → structurally distant → ResearchLoop choice
   without running any target?

## Current literature

The board is engine methodology. Mathematical prior art for frontier
targets is cited on each `PriorArtDossier` (`literature/` ids). Project
relationship: **engine diagnosis**. No new number-theory theorem is
claimed. Novelty is not inferred from keyword overlap.

## Branch budget

```text
Mathematical target     Can frozen v2.2 enter a campaign with persistent
                        research memory, grey loot, a ranked target
                        portfolio, and prior-art maps, without new attacks?
Novelty hypothesis      None mathematical. Past experiments → grey loot →
                        failure clusters → ranked next targets.
Falsifier               A new attack; adapter hints; invented EV scores;
                        novelty from keyword search; thawing the planner.
Existing machinery      research_engine.memory types, historical seed,
                        score_candidate, FailureLearningValue, ResearchLoop.
Maximum Phase-0 scope   Board types + seed JSON + grey-loot backfill +
                        named clusters + prior-art dossiers + blind packets
                        + campaign order + tests + this dossier.
Promotion criterion     The ten success criteria of the preparation prompt.
Stop criterion          Any new attack; adapters for unrun targets;
                        involution-census fix; v2.3 design.
```

## Balanced-ternary formulation

None required. The wildcard `reverse_and_add_base3` uses balanced-ternary
digit reverse as an exact transition, not as a solving coordinate.

## Why BT may be relevant

It is not required. Digit-fold saturation remains a comparison cluster.

## Candidate operations / invariants

None added. Labels below are **OBSERVATION** of engine history, not
theorems.

- Named failure clusters (global-reachability, branching/quantifier,
  non-affine arithmetic, census-domain, prior-art saturation) —
  **OBSERVATION**
- `ExpectedResearchValue` with `FailureLearningValue` — **OBSERVATION**
- Blind packets free of scout conclusions — **OBSERVATION** (hygiene)

## Experiments

- Historical seed: `src/research_engine/memory/seed/historical.json`
- Target board: `src/research_engine/memory/seed/target_board.json`
- Constructors: `research_engine.memory.seed_records`,
  `research_engine.memory.seed_targets`
- Assembly: `research_engine.memory.board.assemble_board`
- Tests: `tests/research_engine/memory/test_target_board.py`,
  `tests/research_engine/memory/test_research_memory.py`
- No target is executed in this phase.

## Conjectures

None opened.

## Counterexamples

Historical counterexamples remain grey loot (`u_11 < 0`; descent
refuted at aliquot seed 12; sign-first census misses \(y=-x\)). They
are not deleted.

## Formalization

None for the board. Historical records continue to point at existing
Lean modules. No `sorry`. No ledger row.

## Results

### A. Research Target Board

Seventeen candidates in three pools. Structure is in the record fields,
not in the names.

Pool A (calibration / known): `slc_decrement`, `euclidean_remainder`,
`aliquot_seed_12`, `aliquot_amicable_220`, `skolem_order2_known_zero`,
`mx_plus_r_3x1`.

Pool B (frontier / open): `companion_shift_order6_zero_class`,
`weak_collatz_floor_5x4_rplus`, `matthews_prize_mod3_avoider`,
`switching_affine_z2_origin`, `mx_plus_r_7x1_class_obstruction`,
`skolem_order5_unconditional`.

Pool C (wildcards): `aliquot_276`, `home_prime_49`, `juggler_sequence`,
`reverse_and_add_base3`, `cyclic_tag_bit`.

Numeric `ExpectedResearchValue` is computed by `score_candidate` against
the historical corpus and memory. Qualitative reasons are stored on each
axis. Already-run targets stay on the board with honest low novelty.

### B. Grey-Loot Corpus

Every listed historical lesson is a `GreyLoot` with evidence status,
reusable lesson, transfer targets, and
`ACTIVE|PARKED|REFUTED|REUSED|SATURATED|SUPERSEDED`.

### C. Failure Clusters

Named overlays, not target-name clustering:

- global-reachability — Skolem, \(R^+\), BB-5; HIGH; `WATCH`;
  `PROMOTE_TO_NEXT_VERSION` remains guidance only
- branching/quantifier — sum-strip, two-affine SLC; `PARK`
- non-affine arithmetic — aliquot; home-prime as transfer; `PARK`
- census-domain — negation / involution; `PARK`
- prior-art saturation — Syracuse, \(R^+\), BB-5; `RECORD`

### D. Engineering Candidates

Wrapped named clusters. A single failure never auto-promotes. No
involution-census fix. No aliquot/Skolem/nondeterministic attack.

### E. Mathematical Yield Corpus

Per-experiment `MathematicalYield` plus independent
`representation_novelty` / `mathematical_novelty`. BB-5 remains
representation `HIGH`, mathematical `NONE`.

### F–G. Prior-art map and blind packets

Every Pool B target and the recommended wildcards have a
`PriorArtDossier` (scout lane) and a `BlindPacket` whose
`attack_payload` excludes literature names, known invariants, residue
partitions, and open-problem status. `forbidden_hints` is metadata for
future adapters, not I/O.

### H. Recommended campaign order

Protocol, computed by `recommend_campaign_order` against the historical
corpus and memory (2026-08-25 dump):

1. Calibration: `slc_decrement`, `euclidean_remainder`, `aliquot_seed_12`
2. Frontier (memory-aware EV): `switching_affine_z2_origin`,
   `mx_plus_r_7x1_class_obstruction`, `weak_collatz_floor_5x4_rplus`,
   `matthews_prize_mod3_avoider`, `companion_shift_order6_zero_class`,
   `skolem_order5_unconditional`
3. Wildcards: `juggler_sequence`, `reverse_and_add_base3`,
   `home_prime_49` (`aliquot_276` is baseline history;
   `cyclic_tag_bit` dropped for low failure-learning)
4. ResearchLoop pick (max EV among leftovers):
   `skolem_order2_known_zero`

No target is run. Recompute with `assemble_board` after new experiments.

## Open questions

The first frontier in the computed campaign order — what exact
intermediate theorem or obstruction can frozen v2 produce there?

v2.3 Phases 1–3 (hypotheses, inductive/ranking certificates, law/domain
split; no new flood attacks; involution census still unimplemented) is
[research_strategy.md](research_strategy.md).

## Decision

`PROMOTE` the target board and grey-loot corpus as v2.2 laboratory
intelligence. Do not add attacks. Do not write adapters in this phase.
Do not implement the involution census. Do not define v2.3.

Best next question: the first frontier name in
`RecommendedCampaignOrder.sequence` after the three calibration
targets.

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
