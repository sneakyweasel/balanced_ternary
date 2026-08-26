# Phase-9 mathematical frontier re-ranking

Status: **PHASE_9_FRONTIER_RERANKING**

This is a target × attack selection experiment. It does not implement a
new attack, does not modify `DEFAULT_ATTACK_ORDER`, does not open a new
board, and does not reopen reverse-and-add.

## Branch budget

```text
Mathematical target     Among remaining frontiers, which (target, attack)
                        pair has the highest expected new mathematics per
                        unit of attack effort?
Novelty hypothesis      Accumulated v2.4 evidence can rank existing pairs
                        without inventing a new attack family.
Falsifier               Reverse-add reopened; flood order thawed; a new
                        target created; the winner executed in this phase.
Existing machinery      ResearchMemory, GreyLoot, Top-3 dossiers, Phase 0-8
                        records, v2.2 replays, CLOSE/math-status taxonomy.
Maximum Phase-9 scope   Frozen candidate pool, qualitative score, Top-3,
                        artifacts, tests. No execution.
Promotion criterion     A selected frontier with a cheap falsifier and
                        visible evidence, not a new campaign.
Stop criterion          New attack family; reverse-add reopening; ranking
                        synthesizer; digit-language engine.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_9_FRONTIER_RERANKING`
- decision: **SELECTED_FRONTIER**
- executed: `False`
- green loot: `NO_NEW_LOOT`

Reverse-and-add is excluded. `DEFAULT_ATTACK_ORDER` is unchanged.
No production attack is registered.

## Scoring basis

S = P(new mathematics) * frontier_strength * formalization_value / (implementation_cost * novelty_risk)

The score is a prioritization aid, not a calibrated probability.
Objective: new mathematics per unit of attack effort.

## Comparison table

| Rank | Target | Attack | Frontier | Cheapest falsifier | Expected loot | Scope | Lean |
| ---- | ------ | ------ | -------- | ------------------ | ------------- | ----- | ---- |
| 1 | `juggler_sequence` | `odd_odd_branch_composition` | Unexplained nonlinear branch interaction on the complementary odd-to-odd floor-power cylinder | On the frozen odd-to-odd pairs, test any k=2 size law T^2(n)<n (fails at 3->5->11) or a single exact parity-cylinder predicate; do not enlarge depth to hide 3->5. | GREEN | MEDIUM | PLAUSIBLE |
| 2 | `mx_plus_r_7x1_class_obstruction` | `basin_preimage_grammar` | Local image-class invariant without a basin consequence | Propose one finite residue/valuation quotient of predecessors of 1 and exhibit two states in the same class with different reachability of 1 on the stored window. | GREY | MEDIUM | PLAUSIBLE |
| 3 | `matthews_prize_mod3_avoider` | `basin_preimage_grammar` | Whether every integer orbit that stays in {1,2} mod 3 for all time enters -1 or {-2,-4}. Finite-window preimages and the fact that packet seeds are not avoiders do not decide that. | Propose one residue quotient of bounded preimages of {-1} union {-2,-4} and split two states with identical class but different avoider behavior. | GREY | MEDIUM | PLAUSIBLE |

## Rank 1 — SELECTED_FRONTIER

- Rank: `1`
- Target: `juggler_sequence`
- Attack: `odd_odd_branch_composition`
- Mathematical frontier: Unexplained nonlinear branch interaction on the complementary odd-to-odd floor-power cylinder: odd-even T^2(n)<n is proved, but odd-to-odd steps such as 3->5 remain outside the lemma and are not a halt theorem.
- Why now: v2.4's only green-loot trajectory left an explicit complementary branch unimplemented. Reverse-add showed the same idea does not transfer; the remaining Juggler cylinder is still local, exact, and Lean-adjacent.
- Cheapest falsifier: On the frozen odd-to-odd pairs, test any k=2 size law T^2(n)<n (fails at 3->5->11) or a single exact parity-cylinder predicate; do not enlarge depth to hide 3->5.
- Expected loot: `GREEN`
- Novelty risk: `MEDIUM`
- Implementation scope: `MEDIUM`
- Lean path: `PLAUSIBLE`
- Recommendation: Run a k=2 odd-odd composition falsifier on the existing frozen odd-to-odd transitions; do not claim termination and do not generalize the gated odd-even primitive.

## Rank 2 — BACKUP_FRONTIER_1

- Rank: `2`
- Target: `mx_plus_r_7x1_class_obstruction`
- Attack: `basin_preimage_grammar`
- Mathematical frontier: Local image-class invariant without a basin consequence: after one step, odd images lie in <2> inside (Z/7Z)*, but complementary classes still reach 1. Which odd positives reach 1 remains open.
- Why now: The v2.3 retrospective named image-as-basin as a recurring failure. This target already has Lean-certified counterexamples, so a basin/preimage falsifier can run without a new map engine.
- Cheapest falsifier: Propose one finite residue/valuation quotient of predecessors of 1 and exhibit two states in the same class with different reachability of 1 on the stored window.
- Expected loot: `GREY`
- Novelty risk: `MEDIUM`
- Implementation scope: `MEDIUM`
- Lean path: `PLAUSIBLE`
- Recommendation: Test one predecessor quotient against the known hits 73 and 299593 versus a stored non-hit such as seed 3; do not rerun the false class obstruction.

## Rank 3 — BACKUP_FRONTIER_2

- Rank: `3`
- Target: `matthews_prize_mod3_avoider`
- Attack: `basin_preimage_grammar`
- Mathematical frontier: Whether every integer orbit that stays in {1,2} mod 3 for all time enters -1 or {-2,-4}. Finite-window preimages and the fact that packet seeds are not avoiders do not decide that.
- Why now: Same recurring image/basin limitation as 7x+1, with a second Lean module and named cycles already in hand. Cheaper than a Skolem vanishing procedure.
- Cheapest falsifier: Propose one residue quotient of bounded preimages of {-1} union {-2,-4} and split two states with identical class but different avoider behavior.
- Expected loot: `GREY`
- Novelty risk: `MEDIUM`
- Implementation scope: `MEDIUM`
- Lean path: `PLAUSIBLE`
- Recommendation: Test one bounded preimage quotient for the known cycles; do not claim the Matthews prize and do not rerun the false avoider obstruction.

## Exclusions

- `reverse_and_add_base3`: Phase-8 CLOSED the reverse-add branch: involution summaries are generic arithmetic or counterexample-killed. Reopening would be machinery gravity.
- `weak_collatz_floor_5x4_rplus`: CLOSE_REPARAMETERIZATION of the 4/3 SLC language; a new restricted-composition pass would upgrade a known representation.
- `skolem_order2_known_zero`: v2.2 calibration replay of a known zero; historical reproduction without a new attack hypothesis.
- `cyclic_tag_bit`: CLOSE_SPEC_MISMATCH and RANKING_IMPLAUSIBLE; length nondecrease is the production, and a native word engine is machinery gravity.
- `juggler_sequence × odd_even_two_step_decrease`: Already converted to a gated attack and Lean-proved as floorPower_odd_even_two_step_lt. Do not rerun the exhausted lemma.
- `home_prime_49 × concat_word_composition`: Dossier forbids a concatenation attack; a general digit-language engine is machinery gravity. Phase-2 two-step length already failed.
- `* × ranking_function_synthesis`: Unrestricted ranking synthesizer is machinery gravity.
- `* × symbolic_nonlinear_composition`: Generic symbolic algebra engine is machinery gravity.

## Decision

**SELECTED_FRONTIER**

juggler_sequence x odd_odd_branch_composition: mathematically interesting, cheap to falsify, exact, Lean-adjacent, and not exhausted.

Do not execute the winner in this phase.

## Best next question

Run a k=2 odd-odd composition falsifier on the existing frozen odd-to-odd transitions; do not claim termination and do not generalize the gated odd-even primitive.
