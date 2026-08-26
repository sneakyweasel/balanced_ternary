# Research Engine v2.4 research-control layer

Status: **EXPLORATORY**

This is laboratory intelligence for Research Engine v2.4. It does
**not** add flood-order attacks, ranking synthesis, basin solvers,
a general symbolic-composition engine, or a new Skolem procedure.
A gated experimental attack `odd_even_two_step_decrease` may be opted
into; it is not in `DEFAULT_ATTACK_ORDER`. Implementation lives in
`research_engine.control` and `research_engine.attacks.restricted_symbolic_composition`.
The thin descriptor is `research.research_control`. Frozen v2.3
mathematical campaigns remain unchanged.

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
  `tests/research/research_control/test_research_control.py`,
  `tests/research/research_control/test_ranking_phase0.py`,
  `tests/research/research_control/test_ranking_phase1.py`,
  `tests/research/research_control/test_symbolic_composition_phase2.py`,
  `tests/research/research_control/test_symbolic_composition_phase3.py`,
  `tests/research/research_control/test_reverse_add_composition_phase4.py`,
  `tests/research/research_control/test_reverse_add_carry_phase5.py`,
  `tests/research/research_control/test_reverse_add_pair_interaction_phase6.py`,
  `tests/research/research_control/test_reverse_add_weighted_pair_phase7.py`,
  `tests/research/research_control/test_reverse_add_involution_phase8.py`,
  `tests/research/research_control/test_phase9_frontier_ranking.py`,
  `tests/research/research_control/test_juggler_odd_odd_phase10.py`,
  `tests/research/research_control/test_juggler_macro_phase11.py`
- Phase-0 replays: `skolem_order2_known_zero`,
  `switching_affine_z2_origin`
- Ranking Phase-0 falsifier: `research_engine.control.ranking`,
  `docs/research/ranking_phase0.md`
- Ranking Phase-1 falsifier: `research_engine.control.ranking_phase1`,
  `docs/research/ranking_phase1.md`
- Symbolic-composition Phase-2 falsifier:
  `research_engine.control.symbolic_composition`,
  `docs/research/symbolic_composition_phase2.md`
- Restricted symbolic-composition Phase-3 attack:
  `research_engine.attacks.restricted_symbolic_composition`,
  `docs/research/symbolic_composition_phase3.md`
- Reverse-add composition Phase-4 falsifier:
  `research_engine.control.reverse_add_composition`,
  `docs/research/reverse_add_composition_phase4.md`
- Reverse-add carry Phase-5 falsifier:
  `research_engine.control.reverse_add_carry`,
  `docs/research/reverse_add_carry_phase5.md`
- Reverse-add pair-interaction Phase-6 falsifier:
  `research_engine.control.reverse_add_pair_interaction`,
  `docs/research/reverse_add_pair_interaction_phase6.md`
- Reverse-add weighted-pair Phase-7 falsifier:
  `research_engine.control.reverse_add_weighted_pair`,
  `docs/research/reverse_add_weighted_pair_phase7.md`
- Reverse-add involution Phase-8 falsifier:
  `research_engine.control.reverse_add_involution`,
  `docs/research/reverse_add_involution_phase8.md`
- Frontier re-ranking Phase-9 selection:
  `research_engine.control.frontier_ranking`,
  `docs/research/phase9_frontier_ranking.md`
- Juggler odd-odd Phase-10 falsifier:
  `research_engine.control.juggler_odd_odd`,
  `docs/research/juggler_odd_odd_phase10.md`
- Juggler macro-grammar Phase-11 falsifier:
  `research_engine.control.juggler_macro`,
  `docs/research/juggler_macro_phase11.md`

## Conjectures

None opened.

## Counterexamples

Historical campaign counterexamples remain on the v2.3 dossiers. They
are not deleted. Finite prefixes are not upgraded to `RESOLVED`.

## Formalization

The control layer itself has no new ledger row. Phase-3 reuses
`Problems.Engine.FloorPower.floorPower_odd_even_two_step_lt`.
Phase-10 adds `floorPower_odd_odd_two_step_gt`. Phase-11 adds
`floorPower_odd_macro_direction` as `COMPOSITION_OF_KNOWN_FACTS`.
No `sorry`.

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

A Phase-0 ranking-function falsifier later tested that specification
on four frozen campaigns; see Results F and
[ranking_phase0.md](../research/ranking_phase0.md). It did not add an
attack.

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

### F. Ranking-function Phase-0 falsifier

Record: [ranking_phase0.md](../research/ranking_phase0.md),
[ranking_phase0.json](../research/ranking_phase0.json).
`engine_control_version = 0.2.7`. Not an attack.

Tiny integer templates `V = a·log_bit + b·digit + c·residue` on the
three `TERMINATION → global_inductive` campaigns plus cyclic-tag
negative control. Exact integer comparison; exceptional cores of size
`K ≤ 8`; no grid enlargement.

| Target | Classification |
| --- | --- |
| `juggler_sequence` | `RANKING_NEEDS_RICHER_STATE` (odd-to-odd floor-power growth) |
| `reverse_and_add_base3` | `RANKING_NEEDS_RICHER_STATE` (reverse-plus-add expansion) |
| `home_prime_49` | `RANKING_NEEDS_RICHER_STATE` (factor-concat length growth) |
| `cyclic_tag_bit` | `RANKING_IMPLAUSIBLE` (length nondecrease; sanity check) |

Family decision: **REFINE**. Formalization: `not_yet_formalization_ready`.
Updated Top-3 names live only in the Phase-0 record. Frozen v2.3 files
and `DEFAULT_ATTACK_ORDER` are unchanged.

### G. Ranking-function Phase-1 enriched falsifier

Record: [ranking_phase1.md](../research/ranking_phase1.md),
[ranking_phase1.json](../research/ranking_phase1.json).
`experimental_status = PHASE_1_ENRICHED_RANKING_FALSIFIER`. Not an attack.

| Target | Hypothesis | Classification |
| --- | --- | --- |
| Juggler | odd-even `T^2` | `COMPOSED_RANKING_PROMISING` (`BOUNDED_SURVIVOR` on 11 macros; 9 odd-to-odd steps remain outside) |
| Reverse-add | reverse_gap L1 | `REVERSE_GAP_IMPLAUSIBLE` (`1→2`: palindromes are not an attractor) |
| Home Prime 49 | piecewise `V_C` | `PIECEWISE_RANKING_NEEDS_RICHER_STATE` (`4→22` concat growth; `10→25` factor_count nondecrease) |

Family decision: **MIXED**. Formalization: `not_yet_formalization_ready`.
`DEFAULT_ATTACK_ORDER` unchanged.

### H. Symbolic-composition Phase-2 falsifier

Record: [symbolic_composition_phase2.md](../research/symbolic_composition_phase2.md),
[symbolic_composition_phase2.json](../research/symbolic_composition_phase2.json).
`experimental_status = PHASE_2_SYMBOLIC_COMPOSITION_FALSIFIER`. Not an attack.

k=2 only. No composition engine. No termination claim.

| Target | Classification | Lean |
| --- | --- | --- |
| Juggler | `SYMBOLIC_COMPOSITION_PROMISING`: `T^2(n) < n` on odd `n` with `T(n)` even | `PROVED` (`floorPower_odd_even_two_step_lt`) |
| Reverse-add | `REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE`: collapse `1→2→0`, growth `3→4→8` | `NOT_YET_FORMALIZATION_READY` |
| Home Prime 49 | `HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE`: `10→25` keeps decimal length; `16→2222→211101` drops `Ω` | `NOT_YET_FORMALIZATION_READY` |

Family decision: **MIXED**. Promoted concept (not executable):
`odd_even_symbolic_composition`. Not a universal composition engine.
`DEFAULT_ATTACK_ORDER` unchanged.

The Phase-1 juggler ranking survivor is a downstream size consequence of
the exact two-step inequality, not a new ranking template.

### I. Restricted symbolic-composition Phase-3 attack

Record: [symbolic_composition_phase3.md](../research/symbolic_composition_phase3.md),
[symbolic_composition_phase3.json](../research/symbolic_composition_phase3.json).
`experimental_status = PHASE_3_RESTRICTED_SYMBOLIC_ATTACK`.

First executable v2.4 mathematical attack. Gated:
`enable_restricted_symbolic_composition`. Not in `DEFAULT_ATTACK_ORDER`.
Family `restricted_symbolic_composition`, rule `odd_even_two_step_decrease`.
Depth frozen at 2. `global_consequence = NONE`.

| Target | Result |
| --- | --- |
| Juggler | `APPLICABLE`; `T^2(x) < x`; Lean `PROVED`; `NEW_STRUCTURAL_LEMMA` |
| Reverse-add | `NOT_APPLICABLE` / `MAP_MISMATCH` |
| Home Prime 49 | `NOT_APPLICABLE` / `MAP_MISMATCH` |
| Cyclic tag | `NOT_APPLICABLE` / `MAP_MISMATCH` |

Family decision: **PROMOTE_RESTRICTED**. Matching is by floor-power successor
identity, not campaign name. StrategyPlanner does not execute the attack.
Phase-0/1/2 records and the v2.3 freeze are unchanged.

### J. Reverse-add two-step composition Phase-4 falsifier

Record: [reverse_add_composition_phase4.md](../research/reverse_add_composition_phase4.md),
[reverse_add_composition_phase4.json](../research/reverse_add_composition_phase4.json).
`experimental_status = PHASE_4_REVERSE_ADD_COMPOSITION_FALSIFIER`. Not an attack.

k=2 only. Three pre-ranked candidates. Frozen window `1..40` plus seed `196`.
`reverse_gap` not reopened. `DEFAULT_ATTACK_ORDER` unchanged.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `W(x)+W(T(x))=0` | `CANCELLATION_FAILURE` at `1→2→0` (`W(1)=1`, `W(2)=-2`) |
| 2 | `sign(T^2(x))=sign(x)` | `SIGN_REVERSAL` at `1→2→0` |
| 3 | `bt_length(T^2) ≤ bt_length+1` | bounded survivor on 49 samples; not a theorem |

Classification: **REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE**.
Green loot: `NO_NEW_LOOT`. Lean: `NOT_YET_FORMALIZATION_READY`.
Top-3 #1 remains `symbolic_nonlinear_composition`. The specific reverse-add
composition branch is closed. Missing coordinate: carry of `x+W(x)`.

### K. Reverse-add carry Phase-5 falsifier

Record: [reverse_add_carry_phase5.md](../research/reverse_add_carry_phase5.md),
[reverse_add_carry_phase5.json](../research/reverse_add_carry_phase5.json).
`experimental_status = PHASE_5_REVERSE_ADD_CARRY_FALSIFIER`. Not an attack.

k=1 only. Statistic A: carry-chain length from `add_with_trace`.
Three pre-ranked candidates. Frozen window `1..40` plus seed `196`.
`reverse_gap` not reopened. `DEFAULT_ATTACK_ORDER` unchanged.
The Phase-4 two-step length bound is not proved here.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `C(x) ≥ max(0, ΔL)` | survived on 49 one-step samples; near-definitional, not loot |
| 2 | `C(x)=0 ⇒ ΔL=0` | `REVERSAL_DEPENDENCE` at `2→0` (`W(2)=-2`, length 2→1) |
| 3 | `C(x)>0 ⇒ ΔL=1` | `LENGTH_DECOUPLING` at `5→-6` (`C=2`, length 3→3) |

Classification: **CARRY_NEEDS_RICHER_STATE**.
Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_BLOCKED`.
Top-3 #1 remains `symbolic_nonlinear_composition`. Carry is a supporting
coordinate of the addition, not a sufficient one-dimensional successor law.
`carry_structure_analysis` is not registered. `balanced_ternary_carry_attack`
is not registered.

### L. Reverse-add pair-interaction Phase-6 falsifier

Record: [reverse_add_pair_interaction_phase6.md](../research/reverse_add_pair_interaction_phase6.md),
[reverse_add_pair_interaction_phase6.json](../research/reverse_add_pair_interaction_phase6.json).
`experimental_status = PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER`. Not an attack.

k=1 only. Pre-normalization pair sums \(s_i=d_i(x)+d_i(W(x))\) from
LSD-aligned `encode`. Three pre-ranked candidates. Frozen window `1..40`
plus seed `196`. `reverse_gap` not reopened. `DEFAULT_ATTACK_ORDER`
unchanged. Phase-4/5 observations are not proved here.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `P0>P2 ⇒ ΔL ≤ 0` | survived on 19 domain samples; finite, not loot |
| 2 | `P+≠P- ⇒ sign(T)=sign(P+-P-)` | `SIGN_IMBALANCE_MISMATCH` at `-672→-448` |
| 3 | `ΔL≥1 ⇒ s_{n-1}≠0` | survived on 17 growth samples; near-positional, not loot |

Classification: **REVERSE_PAIR_NEEDS_RICHER_STRUCTURE**.
Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_BLOCKED`.
Top-3 #1 remains `symbolic_nonlinear_composition`. Pair interaction is a
supporting coordinate, not a sufficient count/position successor law.
`reverse_pair_interaction` is not registered.

### M. Reverse-add weighted-pair Phase-7 falsifier

Record: [reverse_add_weighted_pair_phase7.md](../research/reverse_add_weighted_pair_phase7.md),
[reverse_add_weighted_pair_phase7.json](../research/reverse_add_weighted_pair_phase7.json).
`experimental_status = PHASE_7_WEIGHTED_REVERSE_PAIR_FALSIFIER`. Not an attack.

k=1 only. Positional summaries of raw pair sums, strictly coarser than
\(T=\sum s_i 3^i\). Frozen window `1..40` plus seed `196`. `reverse_gap`
not reopened. `DEFAULT_ATTACK_ORDER` unchanged.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `sign(T)=sign(s_h)` | survived on 42 nonzero-pair samples; repairs `-672` |
| 2 | `m+>m- ⇒ T>0` (and symmetric) | survived on the same 42; equivalent unpacking of Candidate 1 |
| 3 | `sign(T)=sign(s_{h_2})` | `MULTI_POSITION_INTERFERENCE` at `6→4` (`s=(1,-2,1)`, `h=2`, `h2=1`) |

Classification: **WEIGHTED_PAIR_PROMISING**.
Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_READY` (place-value bound
\(|\sum_{i<h}s_i 3^i|\le 3^h-1\); not proved in this phase).
Top-3 #1 remains `symbolic_nonlinear_composition`. Highest-pair sign is a
supporting coordinate, not a reverse-add-specific identity.
`weighted_reverse_pair_interaction` is not registered.

### N. Reverse-add involution Phase-8 falsifier

Record: [reverse_add_involution_phase8.md](../research/reverse_add_involution_phase8.md),
[reverse_add_involution_phase8.json](../research/reverse_add_involution_phase8.json).
`experimental_status = PHASE_8_REVERSE_INVOLUTION_FALSIFIER`. Not an attack.

k=1 only. Objects `x`, `W(x)`, `T(x)`, `W(T(x))`. Not `T^2`. Frozen window
`1..40` plus seed `196`. `reverse_gap` not reopened as ranking.
`DEFAULT_ATTACK_ORDER` unchanged. Canonical `W` is involutive iff `x=0`
or `3` does not divide `x`.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `|W(T)-W(x)| ≤ |W(x)|` | `INVOLUTION_RESIDUAL_MISMATCH` at `1→2` (`R=-3`) |
| 2 | `gap(T) ≤ gap(x)+L(x)` | `SUCCESSOR_REVERSAL_UNCONTROLLED` at `1→2` (`0→4`) |
| 3 | MSD(T) in operand MSD set | survived 42 samples; assessed `GENERAL_ARITHMETIC` |

Classification: **REVERSE_INVOLUTION_REFUTED**.
Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_BLOCKED`.
Top-3 #1 remains `symbolic_nonlinear_composition`.
`reverse_involution_not_sufficient_at_this_level`.
`reverse_involution_structure` is not registered.

### O. Frontier re-ranking Phase-9 selection

Record: [phase9_frontier_ranking.md](../research/phase9_frontier_ranking.md),
[phase9_frontier_ranking.json](../research/phase9_frontier_ranking.json).
`experimental_status = PHASE_9_FRONTIER_RERANKING`. Not an attack.
Not executed. Reverse-add remains CLOSED.

The unit is `(target, attack family)`. Score is a qualitative
prioritization aid
\(S = P(\text{new math})\times\text{frontier}\times\text{Lean}/(\text{cost}\times\text{novelty})\),
not a calibrated probability.

| Rank | Target | Attack | Loot | Scope | Lean |
| --- | --- | --- | --- | --- | --- |
| 1 | `juggler_sequence` | `odd_odd_branch_composition` | `GREEN` | `MEDIUM` | `PLAUSIBLE` |
| 2 | `mx_plus_r_7x1_class_obstruction` | `basin_preimage_grammar` | `GREY` | `MEDIUM` | `PLAUSIBLE` |
| 3 | `matthews_prize_mod3_avoider` | `basin_preimage_grammar` | `GREY` | `MEDIUM` | `PLAUSIBLE` |

Decision: **SELECTED_FRONTIER**
`(juggler_sequence, odd_odd_branch_composition)`.
Backups: 7x+1 basin/preimage, Matthews basin/preimage.
`DEFAULT_ATTACK_ORDER` unchanged. No new board. No production attack.

### P. Juggler odd-odd composition Phase-10 falsifier

Record: [juggler_odd_odd_phase10.md](../research/juggler_odd_odd_phase10.md),
[juggler_odd_odd_phase10.json](../research/juggler_odd_odd_phase10.json).
`experimental_status = PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER`.
Not an attack. `k=2` only. Frozen window `1..40` plus seed `13`.
`odd_even_two_step_decrease` unchanged. `DEFAULT_ATTACK_ORDER` unchanged.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | `T^2(x)>x` on all `D_OO` | `THRESHOLD_FAILURE` at `1→1→1` |
| 2 | `T^2(n)>n` on `D_OO`, `n≥3` | survived 8 samples; Lean **PROVED** |
| 3 | `T^2(x)` odd on `D_OO` | `PARITY_DOMAIN_LEAK` at `5→11→36` |

Classification: **JUGGLER_ODD_ODD_GREEN_LOOT**.
Green loot: `JUGGLER_ODD_ODD_GREEN_LOOT`. Lean: `PROVED`
(`floorPower_odd_odd_two_step_gt`). Scope: `LOCAL_BRANCH_LAW`,
not `GLOBAL_TERMINATION`. Top-3 #1 is `odd_odd_symbolic_composition`
(proposed, not registered).

### Q. Juggler macro-dynamics Phase-11 falsifier

Record: [juggler_macro_phase11.md](../research/juggler_macro_phase11.md),
[juggler_macro_phase11.json](../research/juggler_macro_phase11.json).
`experimental_status = PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER`.
Not an attack. `k=2` only. Frozen window `1..40` plus seed `13`.
`odd_even_two_step_decrease` unchanged. `DEFAULT_ATTACK_ORDER` unchanged.
Gated name `juggler_macro_phase11` is not in `EXPERIMENTAL_ATTACKS`.

| Rank | Candidate | Result |
| --- | --- | --- |
| 1 | Combined direction on odd `n≥3` | survived; `COMPOSITION_OF_KNOWN_FACTS` |
| 2 | `B` determines `parity(T^2)` | `MACRO_PARITY_NOT_DETERMINISTIC` at `5→11→36` |
| 3 | `B=E` exits the odd macro | `DIRECTION_SURVIVAL_DECOUPLING` at `15→58→7` |

Classification: **MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE**.
Loot: `NO_NEW_LOOT`. Lean: `COMPOSITION_OF_KNOWN_FACTS`
(`floorPower_odd_macro_direction`). Macro-state
`M(n)=(parity(n), B(n), parity(T^2(n)))` is `MACRO_STATE_INSUFFICIENT`.
Top-3 #1 is `basin_preimage_grammar` on `mx_plus_r_7x1_class_obstruction`.
Keep `odd_odd_symbolic_composition`. Do not register
`juggler_macro_grammar`.

## Open questions

`B(n)` does not determine `parity(T^2(n))` or odd-macro survival.
The next cheap frontier is basin/preimage on 7x+1, not another
Juggler micro-attack.

## Decision

`PROMOTE` the gated Juggler `odd_even_two_step_decrease` primitive.
`PROMOTE` the Phase-9 frontier map. `PROMOTE` the odd-odd two-step
growth lemma as local branch loot. `PARK` the Juggler macro-grammar
branch: the paired lemmas do not induce a next-bit transition law.
`CLOSE` reverse-add compressed involution summaries. Do not claim
Juggler termination or divergence. Do not thaw `DEFAULT_ATTACK_ORDER`.
Do not register `odd_odd_symbolic_composition` or
`juggler_macro_grammar`.

Best next question: a finite residue/valuation quotient of predecessors
of 1 for `mx_plus_r_7x1_class_obstruction`. Still no new attack in
`DEFAULT_ATTACK_ORDER`.

## Publication assessment

Status: `EXPLORATORY`. Engine methodology, not a paper candidate.
