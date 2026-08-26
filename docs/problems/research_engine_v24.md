# Research Engine v2.4 research-control layer

Status: **EXPLORATORY**

This is laboratory intelligence for Research Engine v2.4. It does
**not** add flood-order attacks, ranking synthesis, basin solvers,
symbolic composition, or a new Skolem procedure. Implementation lives
in `research_engine.control`. The thin descriptor is
`research.research_control`. Frozen v2.3 mathematical campaigns remain
unchanged.

## Problem

When frozen v2.3 reaches the edge of its executable attack vocabulary,
can the engine classify why it stopped, keep that frontier explicit,
and name the three strongest mathematically motivated next attacks
without executing them?

## Exact statement

On the frozen 0.2.1 attack stack, with v2.3 strategy/reasoning/law/
quantifier layers unchanged, a research-control layer

1. freezes an immutable baseline `RESEARCH_ENGINE_V2_3_BASELINE`;
2. assigns every CLOSE campaign exactly one primary close tag
   (`CLOSE_KNOWN` … `CLOSE_NO_PROMOTION`);
3. stores `execution_status` independently of `mathematical_status`
   (`RESOLVED | STRONG_NEGATIVE | FRONTIER | UNRESOLVED`);
4. loads historical v2.3 records without rewriting them, inferring new
   fields conservatively with provenance `INFERRED`;
5. emits an `AttackProposalDossier` of exactly three non-executable
   ranked proposals after mapping/discovery;
6. replays selected v2.2 targets under the current control layer with
   historical results excluded from the blind track;
7. extracts a v2.3 retrospective from the nine campaigns and their
   Top-3 dossiers, not by concatenating reports.

A proposal is not an attack. `run_named_attack` must reject every
proposal name.

## Current literature

The layer is engine methodology. Mathematical prior art for the nine
campaigns stays on those dossiers. Project relationship: **engine
diagnosis**. No new number-theory theorem is claimed.

## Branch budget

```text
Mathematical target     Can frozen v2.3 be wrapped in a control layer that
                        preserves an immutable baseline, classifies CLOSE
                        without implying resolution, emits exactly three
                        non-executable next-attack proposals, and replays
                        selected v2.2 targets in isolation?
Novelty hypothesis      None mathematical. The yield is a preserved
                        frontier: discover → classify → preserve → propose.
Falsifier               A new attack in DEFAULT_ATTACK_ORDER; mutating
                        historical.json / already_run; proposing a
                        registered attack as executable; inferring RESOLVED
                        from finite evidence; leaking v2.2 results into
                        the blind track.
Existing machinery      research_engine.memory, StrategyPlanner, AttackPlanner
                        freeze, nine v2.3 adapters, DecisionReason,
                        FailureClass, GreyLoot, BlindPacket hygiene,
                        GLOBAL_INDUCTIVE_CHAIN.attacks=().
Maximum Phase-0 scope   control package + baseline freeze + taxonomy adapter
                        + proposal generator + two v2.2 replays +
                        retrospective + tests. No new attacks.
Promotion criterion     All eight deliverables exist; historical seeds load
                        unchanged; proposals never enter the attack registry;
                        replay isolation holds.
Stop criterion          Any executable attack; rewriting the nine dossiers
                        to a new schema; ranking/basin/symbolic implementations.
```

## Balanced-ternary formulation

None required. The control layer does not change any map.

## Why BT may be relevant

It is not required.

## Candidate operations / invariants

None added. Labels below are **OBSERVATION** of engine control, not
theorems.

- Primary close tags independent of laboratory `PROMOTE|PARK|CLOSE` —
  **OBSERVATION**
- `CLOSE` execution does not imply `RESOLVED` — **OBSERVATION**
- Top-3 `AttackProposalDossier` is non-executable — **OBSERVATION**

## Experiments

- Baseline: `research_engine.control.baseline`
- Overlay: `research_engine.control.store` (never `historical.json`)
- Tests: `tests/research_engine/control/`,
  `tests/research/research_control/test_research_control.py`
- Phase-0 replays: `skolem_order2_known_zero`,
  `switching_affine_z2_origin`

## Conjectures

None opened.

## Counterexamples

Historical campaign counterexamples remain on the v2.3 dossiers. They
are not deleted. Finite prefixes are not upgraded to `RESOLVED`.

## Formalization

None for the control layer. Historical Lean modules are unchanged. No
`sorry`. No ledger row.

## Results

### A. Immutable v2.3 baseline

Identifier `RESEARCH_ENGINE_V2_3_BASELINE`. SHA-256 freeze of
`historical.json` and `target_board.json`, plus campaign order, attack
registry, engine versions 0.2.2–0.2.6, and the empty
`global_inductive` / `law_domain` / `quantifier_probe` attack tuples.
`FrozenResearchMemory.add` / `to_json` raise. v2.4 writes only to
`ControlStore`.

The nine campaign dossiers are not rewritten.

### B. CLOSE taxonomy and mathematical status

Inferred conservatively (provenance `INFERRED`; never `RESOLVED`):

- `mx_plus_r_7x1_class_obstruction` — `CLOSE_FALSE_OBSTRUCTION` /
  `STRONG_NEGATIVE`
- `weak_collatz_floor_5x4_rplus` — `CLOSE_REPARAMETERIZATION` /
  `UNRESOLVED`
- `matthews_prize_mod3_avoider` — `CLOSE_FALSE_OBSTRUCTION` /
  `STRONG_NEGATIVE`
- `companion_shift_order6_zero_class` — `CLOSE_SKIP_BOUNDARY` /
  `FRONTIER`
- `skolem_order5_unconditional` — `CLOSE_SKIP_BOUNDARY` / `FRONTIER`
- `juggler_sequence` — `CLOSE_FINITE_CENSUS` / `FRONTIER`
- `reverse_and_add_base3` — `CLOSE_FINITE_CENSUS` / `FRONTIER`
- `home_prime_49` — `CLOSE_FINITE_CENSUS` / `FRONTIER`
- `cyclic_tag_bit` — `CLOSE_SPEC_MISMATCH` / `UNRESOLVED`

Engine `ResearchDecision` on those records remains `CONTINUE`.
`CLOSE_SKIP_BOUNDARY + FRONTIER` is valid.
`CLOSE_FINITE_CENSUS + RESOLVED` is rejected.

### C. AttackProposalDossier

Every campaign emits ranks `{1,2,3}`. Names are absent from
`DEFAULT_ATTACK_ORDER`. Recurring required capabilities (union of the
nine Top-3 dossiers):

- ranking-function synthesis (9)
- symbolic nonlinear branch composition (6)
- proof-guided hypothesis refinement (5)
- symbolic predecessor construction (3)
- residue × valuation class algebra (2)
- symbolic matrix-word / lattice congruence outside the cell budget (2)

These are specifications for a later stage, not implementations.

### D. v2.2 replay

Protocol `campaign_type=REPLAY`, `source_engine=v2.2`,
`execution_engine=v2.4_control_v2.3`. Distinct ids
`replay_v22_<target>`. Historical `already_run` stays true. Historical
GreyLoot / yield does not enter `BlindPacket.attack_payload`. Phase-0
targets: `skolem_order2_known_zero`, `switching_affine_z2_origin`.
Added information is the close tag, mathematical status, and three
proposals — not a reformulation billed as a theorem.

### E. v2.3 retrospective

Successful capabilities actually exercised: problem normalization;
fingerprinting; finite exact exploration; candidate falsification;
Lean identities; scout/blind isolation; post-attack close taxonomy and
Top-3 preservation.

Recurring failure modes: image class mistaken for a basin; representation
mistaken for yield; skip-boundary at unimplemented global-inductive /
matrix-word; finite census mistaken for a global theorem; integer
encoding mistaken for a word/rewrite spec.

## Open questions

Which missing-capability family from the retrospective should be the
first executable v2.4 attack — ranking synthesis, basin/preimage
grammar, or symbolic nonlinear composition — and what is the cheapest
falsifier for that family?

## Decision

`PROMOTE` the research-control layer as v2.4 laboratory intelligence.
Do not add attacks. Do not thaw `DEFAULT_ATTACK_ORDER`. Do not rewrite
the nine v2.3 dossiers. Do not implement ranking, basin, or symbolic
composition in this branch.

Best next question: the highest-frequency missing capability in the
retrospective (ranking-function synthesis) — specify its Phase-0
falsifier before writing an attack.

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
