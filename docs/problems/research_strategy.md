# Research Engine v2.3 research strategy

Status: **EXPLORATORY**

This is laboratory intelligence for Research Engine v2.3 Phases 1–2.
It does **not** add flood-order attacks, rewrite the census, run an
LP/SMT ranking optimizer, or introduce relation/quantifier semantics.
Phase 1 lives in `research_engine.strategy`. Phase 2 lives in
`research_engine.reasoning`. The thin descriptor is
`research.research_strategy`.

## Problem

Can frozen v2.2 turn attack artifacts and `ResearchMemory` into ranked
falsifiable hypotheses and opt-in attack chains, and can a generic
inductive/ranking layer wrap existing envelope and leak attacks to
produce intermediate \(T(S)\subseteq S\) / \(V(T(x))<V(x)\) certificates
on the global-reachability cluster — without changing default
`PlannerReport`s, contaminating blind discovery, or becoming a Skolem,
Positivity, or Collatz solver?

## Exact statement

On the frozen 0.2.1 attack stack, with v2.2 memory unchanged as the
empirical base:

**Phase 1.** An opt-in strategy layer

1. represents persistent `ResearchHypothesis` records with proof
   obligations, prior-art matches, and a source target;
2. generates hypotheses only from evidence (grey loot, exact artifacts,
   named failure-cluster questions), never to fill a quota;
3. runs counterexample-first falsification before any proof-search
   language;
4. declares existing attacks as a capability graph and seeds
   `piecewise_affine → parameter_domain → control_word → control_obstruction`;
5. selects and executes one attack chain for a stated `ResearchGoal`
   rather than flooding `DEFAULT_ATTACK_ORDER`;
6. leaves `AttackPlanner` and `ResearchLoop` flood behaviour identical
   when the strategy entry point is not used;
7. isolates hypotheses so a record born on target A cannot become a
   predicate for target B’s `BlindPacket` or adapter.

**Phase 2.** A generic reasoning layer, not a flood attack,

1. certifies `InvariantCertificate` / `RankingCertificate` objects with
   explicit `EvidenceState` values;
2. tests true \(T(S)\subseteq S\) over `legal_controls` without the
   live-slice `is_terminal` filter;
3. runs bounded CEGIS over the catalog `FINITE_SET | INTERVAL |
   SIGN_ORTHANT | MODULAR_CLASS` (about four refinement rounds);
4. tries ranking from a fixed linear/norm/lex catalog wrapping
   `DescentLeakAttack`, with no optimizer;
5. never promotes complete finite closure or a probed orthant to
   `UNIVERSAL_THEOREM`;
6. is selected only by the opt-in chain `global_inductive` for
   `TERMINATION | BOUNDEDNESS | POSITIVITY | REACHABILITY`.

Phases 3–4 (law/domain separation, quantifiers) remain **gated**.

## Current literature

The strategy and reasoning layers are engine methodology, not a
number-theory result. Historical campaigns remain **KNOWN**
rediscoveries or **PARK**ed limitations as recorded in their own
dossiers. Project relationship: **engine diagnosis**. No new
mathematics is claimed.

v2.2 context: [engine_memory.md](engine_memory.md),
[research_target_board.md](research_target_board.md).

## Branch budget

```text
Mathematical target     Can a generic InvariantCertificate / ranking layer,
                        wrapping existing envelope and leak attacks, produce
                        intermediate inductive structure on the
                        GLOBAL_REASONING cluster without becoming a
                        Skolem, Positivity, or Collatz solver?
Novelty hypothesis      Engine methodology: finite exact structure →
                        certified T(S)⊆S or V(T(x))<V(x), with explicit
                        evidence states so finite closure is never a
                        universal theorem. No number-theory theorem claimed.
Falsifier               DEFAULT_ATTACK_ORDER changes; a cluster replay is
                        billed as UNIVERSAL_THEOREM; a target-specific
                        solver appears; finite BFS is promoted to LIVE
                        infinitude; Phase 3/4 census or quantifier work ships.
Existing machinery      envelope.find_invariant / compute_exact_reachable;
                        InvariantLeakAttack, ClosureLeakAttack, DescentLeakAttack;
                        LinearFunctional; AffineInvariantAttack (live-slice
                        filter — not true T(S)⊆S); Phase 1 ObligationKind
                        INDUCTIVE_INCLUSION / RANKING_DESCENT; StrategyPlanner;
                        TwoPathZ2 N^2 invariance; slc_decrement / Euclidean
                        ranking; GLOBAL_REASONING seed (Carelli, Skolem,
                        Positivity, BB-5).
Maximum Phase-0 scope   research_engine.reasoning types + bounded CEGIS +
                        ranking catalog + evidence discipline + opt-in
                        strategy chain + replay tests + dossier update.
                        No new flood-order attack. No Lean math. No CLI.
Promotion criterion     At least one real target yields a useful
                        INDUCTIVE_CERTIFIED or RANKING_CERTIFIED result
                        (calibration may be known); cluster replays stay
                        below UNIVERSAL_THEOREM; default planner unchanged.
Stop criterion          Target-specific solver; general SMT/CEGIS engine;
                        cones/polyhedra/lex synthesizer beyond the catalog;
                        involution-census rewrite; quantifier semantics;
                        thawing parked branches.
```

Phase 1 budget (implemented, not reopened) is recorded in the journal
entry for 2026-08-26.

## Balanced-ternary formulation

None. Strategy records and reasoning certificates are structured
metadata about engine experiments, regions, and ranking probes.

## Why BT may be relevant

It is not required. Digit-fold saturation remains a comparison cluster
in the historical seed.

## Candidate operations / invariants

None added as theorems. Labels below are **OBSERVATION** of engine
methodology.

- `ResearchHypothesis` life-cycle (`CANDIDATE` … `LEAN_CERTIFIED`) —
  **OBSERVATION** (engine status, not a theorem-ledger tag)
- Capability graph over the frozen 0.2.1 attacks — **OBSERVATION**
- Opt-in chain selection vs flood order — **OBSERVATION**
- Blindness: hypotheses and certificates do not cross target adapters —
  **OBSERVATION** (hygiene)
- `EvidenceState` ladder (`FINITE_OBSERVATION` … `UNIVERSAL_THEOREM`) —
  **OBSERVATION**
- Bounded region CEGIS over the four-form catalog — **OBSERVATION**
- Ranking reconnaissance from a fixed catalog wrapping
  `DescentLeakAttack` — **OBSERVATION** (not a Lyapunov theorem)

## Experiments

- Types and planner: `research_engine.strategy`
- Reasoning: `research_engine.reasoning.analyze`
- Historical generation: `generate_from_memory(ResearchMemory.load_historical())`
- Live chain selection: `StrategyPlanner.run(spec, context, goal=...)`
- Tests: `tests/research_engine/strategy/test_strategy.py`,
  `tests/research_engine/reasoning/test_reasoning.py`,
  `tests/research/research_strategy/test_research_strategy.py`
- Existing specs only. No new adapters. No order-6 census cubes.
  No unrun board targets are executed as solvers.

## Conjectures

None opened. Engine hypotheses are not conjecture-registry rows.

## Counterexamples

Historical counterexamples remain grey loot. A planted false invariant
is refuted by the existing leak attacks; that is a regression of the
falsifier, not a new mathematical counterexample ledger row. Carelli
\(R^+\), Skolem order-2 calibration, and a small positivity companion
are recorded as **non-theorems**: evidence stays below
`UNIVERSAL_THEOREM`.

## Formalization

None for the strategy or reasoning layers. Session `ResearchLedger`
promotion discipline is unchanged. No `sorry`. No theorem-ledger row.
No Lean mathematics in this phase.

## Results

### A. Research hypotheses (Phase 1)

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

### B. Strategy planner (Phase 1)

On a census-friendly hidden piecewise target, `StrategyPlanner`
rediscovers

```text
piecewise_affine → parameter_domain → control_word → control_obstruction
```

and executes fewer attacks than flood order with the obstruction still
`SUPPORTED`. `AttackPlanner` / `ResearchLoop` without the strategy
entry point remain flood-order. `CYCLE_EXCLUSION` still selects
`census_obstruction`; it does not select `global_inductive`.

### C. Blindness

A hypothesis or certificate born on target A does not enter target B’s
`BlindPacket.attack_payload`. Scout and prior-art stay on the scout
lane. Known theorem status is not adapter I/O.

### D. Phase 2 global reasoning

`ENGINE_REASONING_VERSION = 0.2.4`. `ENGINE_STRATEGY_VERSION` stays
`0.2.3`. Package version stays `0.2.2`. `DEFAULT_ATTACK_ORDER` is
unchanged; `global_inductive` is not a flood attack.

Replay (existing specs, calibration tagged known):

- Two-path \(\mathbb Z^2\): nonnegative orthant is
  `INDUCTIVE_CERTIFIED` (`KNOWN_REDISCOVERY`). This is a probed
  one-step inclusion, not a theorem on all of \(\mathbb Z^2\).
- Decrement loop: ranking `RANKING_CERTIFIED` on the certified
  inductive region (`KNOWN_REDISCOVERY`). Not a Lyapunov theorem on
  \(\mathbb Z\).
- Hidden involution (period 2): complete finite closure is
  `FINITE_EXACT` on the enumerated pair; never `UNIVERSAL_THEOREM`.
- Carelli \(R^+\), Skolem order-2 small companion, positivity early
  negative: evidence in `{FINITE_*, INDUCTIVE_CANDIDATE,
  INDUCTIVE_CERTIFIED, RANKING_CANDIDATE, UNKNOWN}` —
  **never** `UNIVERSAL_THEOREM`.

`StrategyPlanner` with goal `TERMINATION` on the decrement spec selects
`global_inductive` and maps the ranking certificate to a
`PROOF_READY` hypothesis. Session `LIVE` hypotheses remain `OPEN`.
Finite complete closure is not promoted to live infinitude.

### E. Gated later phases (not implemented)

**Phase 3 — Law ⊥ domain.** Census law candidates before region
partition. Gate: the parked involution regression; this phase does not
touch `infer_region`.

**Phase 4 — Quantifiers.** \(R\subseteq X\times X\) and
\(\exists\neq\forall\). Gate: a second independent branching target
besides parked nondeterministic SLC.

## Open questions

Can law candidates be separated from domain partition without touching
`infer_region` (Phase 3 gate)?

## Decision

`PROMOTE` Phase 2 as v2.3 laboratory intelligence: generic inductive
and ranking certificates with evidence discipline, on top of the Phase 1
strategy layer, wrapping the frozen attack stack. Do not add flood
attacks. Do not implement the involution census. Do not open Phases 3–4.
Do not bill cluster replays as universal theorems.

Best next question: can law candidates be separated from domain
partition without touching `infer_region`?

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
