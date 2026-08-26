# Research Engine v2.3 Phase 1 research strategy

Status: **EXPLORATORY**

This is laboratory intelligence for Research Engine v2.3 Phase 1. It
does **not** add attacks, rewrite the census, synthesise ranking
functions, or introduce relation/quantifier semantics. Implementation
lives in `research_engine.strategy`. The thin descriptor is
`research.research_strategy`.

## Problem

Can frozen v2.2 turn attack artifacts and `ResearchMemory` into ranked
falsifiable hypotheses, explicit proof obligations, and opt-in attack
chains — without changing default `PlannerReport`s or contaminating
blind discovery?

## Exact statement

On the frozen 0.2.1 attack stack, with v2.2 memory unchanged as the
empirical base, does an opt-in strategy layer

1. represent persistent `ResearchHypothesis` records with proof
   obligations, prior-art matches, and a source target;
2. generate hypotheses only from evidence (grey loot, exact artifacts,
   named failure-cluster questions), never to fill a quota;
3. run counterexample-first falsification before any proof-search
   language;
4. declare existing attacks as a capability graph and seed the
   historically successful chain
   `piecewise_affine → parameter_domain → control_word → control_obstruction`;
5. select and execute one attack chain for a stated `ResearchGoal`
   rather than flooding `DEFAULT_ATTACK_ORDER`;
6. leave `AttackPlanner` and `ResearchLoop` flood behaviour identical
   when the strategy entry point is not used;
7. isolate hypotheses so a record born on target A cannot become a
   predicate for target B’s `BlindPacket` or adapter?

Phases 2–4 (global reasoning, law/domain separation, quantifiers) are
**gated**. They are not implemented here.

## Current literature

The strategy layer is engine methodology, not a number-theory result.
Historical campaigns remain **KNOWN** rediscoveries or **PARK**ed
limitations as recorded in their own dossiers. Project relationship:
**engine diagnosis**. No new mathematics is claimed.

v2.2 context: [engine_memory.md](engine_memory.md),
[research_target_board.md](research_target_board.md).

## Branch budget

```text
Mathematical target     Can frozen v2.2 turn attack artifacts + ResearchMemory
                        into ranked falsifiable hypotheses, proof obligations,
                        and opt-in attack chains — without new attacks or
                        changing default PlannerReports?
Novelty hypothesis      Engine methodology: attack collection → research
                        strategy. No number-theory theorem is claimed.
Falsifier               Default AttackPlanner outputs change; hypotheses
                        leak into blind adapters; fabricated hypotheses;
                        known rediscoveries billed as novel; Phase 2–4
                        machinery shipped in this phase.
Existing machinery      AttackPlanner flood order, _ensure_certificate_chain,
                        session Hypothesis + ResearchLedger, recommended_next_attacks
                        (unused), Counterexample/envelope attacks, ResearchMemory,
                        GreyLoot, FailureCluster, MathematicalYield, score_candidate.
Maximum Phase-0 scope   research_engine.strategy types + capability graph +
                        hypothesis generation/falsification/ranking + opt-in
                        StrategyPlanner + dossier + tests. No new attacks.
                        No census fix. No invariant synthesizer. No quantifiers.
Promotion criterion     Known statements regenerated as hypotheses without
                        false novelty; planner rediscovers census→domain→
                        control_word→obstruction; ≥1 surviving falsifiable
                        conjecture on a replayed target; default planner
                        unchanged.
Stop criterion          Any new attack; involution-census rewrite; ranking
                        synthesizer; relation semantics; thawing parked
                        branches; CLI/visualization.
```

## Balanced-ternary formulation

None. Strategy records are structured metadata about engine experiments
and attack capabilities.

## Why BT may be relevant

It is not required. Digit-fold saturation remains a comparison cluster
in the historical seed.

## Candidate operations / invariants

None added. Labels below are **OBSERVATION** of engine methodology, not
theorems.

- `ResearchHypothesis` life-cycle (`CANDIDATE` … `LEAN_CERTIFIED`) —
  **OBSERVATION** (engine status, not a theorem-ledger tag)
- Capability graph over the frozen 0.2.1 attacks — **OBSERVATION**
- Opt-in chain selection vs flood order — **OBSERVATION**
- Blindness: hypotheses do not cross target adapters — **OBSERVATION**
  (hygiene)

## Experiments

- Types and planner: `research_engine.strategy`
- Historical generation: `generate_from_memory(ResearchMemory.load_historical())`
- Live chain selection: `StrategyPlanner.run(spec, context, goal=...)`
- Tests: `tests/research_engine/strategy/test_strategy.py`,
  `tests/research/research_strategy/test_research_strategy.py`
- No new adapters. No unrun board targets are executed.

## Conjectures

None opened. Engine hypotheses are not conjecture-registry rows.

## Counterexamples

Historical counterexamples remain grey loot. A planted false invariant
is refuted by the existing leak attacks; that is a regression of the
falsifier, not a new mathematical counterexample ledger row.

## Formalization

None for the strategy layer. Session `ResearchLedger` promotion
discipline is unchanged. No `sorry`. No theorem-ledger row.

## Results

### A. Research hypotheses

Historical memory regenerates known statements as `ResearchHypothesis`
records without novelty inflation:

- Syracuse: parameterized family \(2^k y = 3x+1\); class obstruction
  without enumeration — `KNOWN_REDISCOVERY`
- Carelli \(R^+\): residue family \(3y=4x-1\) / \(3y=4x-2\) —
  `KNOWN_REDISCOVERY`; global-reachability remainder tagged to the
  existing cluster, not billed as a theorem
- Switching affine \(\mathbb Z^2\): nonnegative origin-avoidance /
  \(\mathbb N^2\) invariance — `KNOWN_REDISCOVERY`
- Matrix-word: lattice/gcd class obstruction — `KNOWN_REDISCOVERY`

A planted false invariant is `REFUTED` with a witness. A known exact
identity may become `SEARCH_SUPPORTED` without a ledger `PROMOTE`.

### B. Strategy planner

On a census-friendly hidden piecewise target, `StrategyPlanner`
rediscovers

```text
piecewise_affine → parameter_domain → control_word → control_obstruction
```

and executes fewer attacks than flood order with the obstruction still
`SUPPORTED`. `AttackPlanner` / `ResearchLoop` without the strategy
entry point remain flood-order.

### C. Blindness

A hypothesis born on target A does not enter target B’s
`BlindPacket.attack_payload`. Scout and prior-art stay on the scout
lane. Known theorem status is not adapter I/O.

### D. Gated later phases (not implemented)

**Phase 2 — Global reasoning.** Generic inductive/ranking certificates
wrapping existing envelope and leak attacks. Gate: Phase 1 produces a
`PROOF_READY` obligation \(T(S)\subseteq S\) or \(V(T(x))<V(x)\) on a
real target.

**Phase 3 — Law ⊥ domain.** Census law candidates before region
partition. Gate: the parked involution regression; this phase does not
touch `infer_region`.

**Phase 4 — Quantifiers.** \(R\subseteq X\times X\) and
\(\exists\neq\forall\). Gate: a second independent branching target
besides parked nondeterministic SLC.

## Open questions

Does a replayed real target produce a `PROOF_READY` inductive or
ranking obligation that would justify opening Phase 2?

## Decision

`PROMOTE` Phase 1 as v2.3 laboratory intelligence: hypotheses, proof
obligations, and opt-in chain selection on the frozen attack stack. Do
not add attacks. Do not implement the involution census. Do not open
Phases 2–4.

Best next question: does a replayed real target produce a
`PROOF_READY` obligation of the form \(T(S)\subseteq S\) or
\(V(T(x))<V(x)\)?

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
