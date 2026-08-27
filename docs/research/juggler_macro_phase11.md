# Juggler macro-dynamics Phase-11 falsifier

Status: **PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER**

This is not a termination attack, not a divergence theorem, and not a
parity automaton. Depth is frozen at `k=2`. It asks whether the paired
odd-even contraction and odd-odd expansion lemmas induce an exact
macro-transition grammar.

## Branch budget

```text
Mathematical target     Do the paired OE/OO two-step laws imply an exact
                        macro-transition grammar for odd Juggler states?
Novelty hypothesis      Direction may determine whether the odd macro-state
                        survives after T^2.
Falsifier               Frozen odd n>=3 whose T^2 parity or survival is not
                        a function of B(n).
Existing machinery      FloorPower, two proved lemmas, WINDOW+orbit 13.
Maximum Phase-11 scope  Combined direction + two pre-ranked macro implications.
Promotion criterion     Nontrivial B-to-next-bit law with a Lean path.
Stop criterion          k>2, automaton, census growth, restatement billed as loot.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_11_JUGGLER_MACRO_GRAMMAR_FALSIFIER`
- target: `juggler_sequence`
- composition depth: `2`
- classification: **MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE**
- lean: `COMPOSITION_OF_KNOWN_FACTS`
- loot: `NO_NEW_LOOT`
- macro-state: `MACRO_STATE_INSUFFICIENT`
- decision reason: paired direction is known; B does not determine T^2 parity or odd-macro survival

Candidate 1 survival is `COMPOSITION_OF_KNOWN_FACTS`, not new loot.
`DEFAULT_ATTACK_ORDER` is unchanged. No production macro attack.

## Branch definition

- B: E if T(n) even, O if T(n) odd, on odd n
- Complementary on odd n>=3: `True`

Macro-state `M(n)=(parity(n), B(n), parity(T^2(n)))`. Status: `MACRO_STATE_INSUFFICIENT`.

## Existing lemmas

- `Problems.Juggler.Dynamics.floorPower_odd_even_two_step_lt`
- `Problems.Juggler.Dynamics.floorPower_odd_odd_two_step_gt`
- combined: `Problems.Juggler.Dynamics.floorPower_odd_macro_direction`

## Exceptional state

1->1->1 is why T^2(n)>n cannot hold on all of D_OO. The combined direction lemma uses n>=3. This is not a termination result.

## Candidate 1: `combined_direction_law` (survived)

- Statement: For odd n>=3, B(n)=E => T^2(n)<n and B(n)=O => T^2(n)>n. Domains D_OE and D_OO are complementary on odd n>=3; n=1 is excluded.
- Domain: odd n>=3 with T and T^2 defined
- Motivation: Canonical pairing of the two proved lemmas on a common domain. Survival here is COMPOSITION_OF_KNOWN_FACTS, not new loot.
- Checked: 19

## Candidate 2: `branch_determines_t2_parity` (failed)

- Statement: For odd n>=3, B(n)=E => T^2(n) even and B(n)=O => T^2(n) odd. The pair (P_E, P_O)=(even, odd) is the first-observation pair on the frozen mapping (n=7 even, n=3 odd), not a residue sweep.
- Domain: odd n>=3 with T and T^2 defined
- Motivation: Does the contracting/expanding branch also determine whether the odd macro-state survives? Depth remains 2.
- Checked: 2

- Counterexample: `5 -> 11 -> 36` (B=O)
- Failure class: `MACRO_PARITY_NOT_DETERMINISTIC`
- Mechanism: T^2 parity is not a function of B: B(5)=O but T^2(5)=36 has parity 0. Macro-state (1, 'O', 0) is not determined by (parity, B).

## Candidate 3: `contraction_exits_odd_macro` (failed)

- Statement: For odd n>=3, B(n)=E => T^2(n) is even, i.e. the contracting branch leaves the odd macro domain. One-sided coupling; the expanding branch is not assumed to continue.
- Domain: odd n>=3 with B(n)=E
- Motivation: The first frozen E-state n=7 has T^2=4 even. Ask whether contraction is coupled to exit from the odd macro description.
- Checked: 4

- Counterexample: `15 -> 58 -> 7` (B=E)
- Failure class: `DIRECTION_SURVIVAL_DECOUPLING`
- Mechanism: Contraction does not exit the odd macro: B(15)=E and T^2(15)=7 is odd, so the odd label sequence continues.

## Decision

**MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE**

paired direction is known; B does not determine T^2 parity or odd-macro survival.

Loot: `NO_NEW_LOOT`. Lean: `COMPOSITION_OF_KNOWN_FACTS`.
Scope: `LOCAL_BRANCH_LAW`. Not `GLOBAL_TERMINATION`.
`juggler_macro_grammar` is not registered.
`macro_state_needs_richer_information`.

## Best next question

Promote the Phase-9 backup `basin_preimage_grammar` on 7x+1. Do not invent another Juggler micro-attack.
