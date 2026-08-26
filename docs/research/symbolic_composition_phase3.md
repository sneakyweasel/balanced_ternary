# Restricted symbolic-composition Phase-3 attack

Status: **PHASE_3_RESTRICTED_SYMBOLIC_ATTACK**

This is the first executable v2.4 mathematical attack. It is gated.
It is not a general composition engine and not a halt theorem.

## Branch budget

```text
Mathematical target     Can the proved odd-even T^2 < n lemma become a gated
                        executable primitive that recovers Juggler and rejects
                        unrelated maps, without a general composition engine?
Novelty hypothesis      Map-identity matching plus a two-candidate vocabulary
                        plus Lean association is enough; campaign names are not.
Falsifier               Juggler not recovered, negatives accepted, flood-order
                        thawed, or the attack only hard-codes the theorem.
Existing machinery      FloorPowerSpec.successors; floorPower_odd_even_two_step_lt;
                        Attack / run_named_attack.
Maximum Phase-3 scope   One rule, depth 2, four targets, gated registration.
Promotion criterion     Juggler APPLICABLE+PROVED; negatives NOT_APPLICABLE;
                        freeze intact.
Stop criterion          Arbitrary k, CAS/SMT, ranking synthesis, termination claim.
```

## Metadata

- engine_control_version: `0.2.7`
- experimental_status: `PHASE_3_RESTRICTED_SYMBOLIC_ATTACK`
- family: `restricted_symbolic_composition`
- attack: `odd_even_two_step_decrease`
- depth: 2
- gated: `enable_restricted_symbolic_composition`
- decision: **PROMOTE_RESTRICTED**
- decision reason: Juggler odd-even T^2 < x is recovered and Lean-certified; unrelated maps are rejected

`DEFAULT_ATTACK_ORDER` is unchanged. StrategyPlanner does not execute this attack.

## Target `juggler_sequence`

- Applicability: **APPLICABLE**
- Attack: `odd_even_two_step_decrease`
- Depth: 2
- Domain: odd n >= 2 with T(n) even (equivalently isqrt(n^3) even on the floor-power map)
- Candidate: T^2(x) < x
- Bounded: SURVIVES
- Exact: VERIFIED
- Lean: `PROVED`
- Mathematical status: `NEW_STRUCTURAL_LEMMA`
- Global consequence: `NONE`
- Failure reason: `none`

## Target `reverse_and_add_base3`

- Applicability: **NOT_APPLICABLE**
- Attack: `odd_even_two_step_decrease`
- Depth: 2
- Domain: —
- Candidate: —
- Bounded: —
- Exact: —
- Lean: `NOT_YET_FORMALIZATION_READY`
- Mathematical status: `—`
- Global consequence: `NONE`
- Failure reason: `MAP_MISMATCH`

## Target `home_prime_49`

- Applicability: **NOT_APPLICABLE**
- Attack: `odd_even_two_step_decrease`
- Depth: 2
- Domain: —
- Candidate: —
- Bounded: —
- Exact: —
- Lean: `NOT_YET_FORMALIZATION_READY`
- Mathematical status: `—`
- Global consequence: `NONE`
- Failure reason: `MAP_MISMATCH`

## Target `cyclic_tag_bit`

- Applicability: **NOT_APPLICABLE**
- Attack: `odd_even_two_step_decrease`
- Depth: 2
- Domain: —
- Candidate: —
- Bounded: —
- Exact: —
- Lean: `NOT_YET_FORMALIZATION_READY`
- Mathematical status: `—`
- Global consequence: `NONE`
- Failure reason: `MAP_MISMATCH`

## Grey loot

- Why Juggler: Phase-1 bounded T^2 ranking survived; Phase-2 explained it by the exact odd-even two-step inequality; Lean proved floorPower_odd_even_two_step_lt.
- Path: finite survivor -> symbolic explanation -> Lean theorem -> gated executable rule
- Compositional vs target-specific: matching is by successor identity with the floor-power map, not by campaign name. The rule is compositional (odd-even T^2 decrease) and does not cover reverse-add or factor-concatenation.
- Global consequence: `NONE`

Reusable:

- fixed composition depth 2
- exact odd-to-even domain predicate
- map-identity probe against even/odd floor-power
- named candidate T^2(x) < x
- association with an existing Lean theorem

Hard-coded before any later generalization:

- finite map-identity probe
- single rule, depth frozen at 2
- two-candidate vocabulary T^2 < x and T^2 <= x-1
- Lean theorem name association (no proof search)

## Decision

**PROMOTE_RESTRICTED**

Juggler odd-even T^2 < x is recovered and Lean-certified; unrelated maps are rejected.

Ready for controlled research use. Not added to `DEFAULT_ATTACK_ORDER`.
Not a universal symbolic-composition engine.

## Best next question

Does any other stored map have a natural depth-2 branch with an exact
inequality that would justify a Phase-4 falsifier, rather than widening
this primitive now?
