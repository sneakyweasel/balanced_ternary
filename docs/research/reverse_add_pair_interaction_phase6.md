# Reverse-add pairwise word-interaction Phase-6 falsifier

Status: **PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER**

This is not a reverse-and-add solver, not a ranking synthesizer, and not a
digit-language engine. It tests whether the pre-normalization alignment of
`encode(x)` with `encode(W(x))` exposes an exact successor coordinate that
magnitude, length, reverse-gap, two-step composition, and carry-chain
length could not see.

## Branch budget

```text
Mathematical target     Do aligned pair sums of encode(x) and encode(W(x))
                        yield an exact successor law invisible to C, length,
                        reverse_gap, and T^2?
Novelty hypothesis      Pre-normalization reverse pairing, not the carry
                        scalar, is the missing one-step coordinate.
Falsifier               An exact one-step sample violating each candidate, or
                        a survivor that is only the definition of s_i.
Existing machinery      ReverseAddSpec, encode, bt_reverse, bt_length,
                        add_with_trace, WINDOW, seed-196 orbit.
Maximum Phase-6 scope   k=1; three pre-ranked pair candidates; frozen
                        window+orbit.
Promotion criterion     Exact nontrivial pair/successor law, Lean path.
Stop criterion          digit-language engine, k>1, census growth, ranking,
                        coefficient search.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_6_REVERSE_PAIR_INTERACTION_FALSIFIER`
- target: `reverse_and_add_base3`
- composition depth: 1
- classification: **REVERSE_PAIR_NEEDS_RICHER_STRUCTURE**
- lean: `FORMALIZATION_BLOCKED`
- green loot: `NO_NEW_LOOT`
- decision reason: pairwise reverse interaction is visible but no simple count or top-position aggregate determines the successor

Candidate list frozen at three. reverse_gap is not reopened.
`DEFAULT_ATTACK_ORDER` is unchanged. No production pair attack.
Phase-4/5 observations are not proved here.

## Pair convention

- Digit index: LSD-first: index i is the coefficient of 3^i
- Alignment: LSD-align encode(x) with encode(W(x)); pad the shorter word with 0 on the MSD side, matching addition
- Equal-length case: when bt_length(x)=bt_length(W(x)), s_i = d_i + d_{L-1-i} on the canonical word of x
- Pair sum: left_i + right_i, the raw aligned trit sum before rewrite_sum
- Range: s_i in {-2,-1,0,+1,+2}
- Not carry: s_i does not include incoming carry and is not a carry statistic

## Candidate 1: `cancellation_majority_blocks_growth` (survived)

- Statement: P0(x) > P2(x) implies bt_length(T(x)) - bt_length(x) <= 0 for the one-step addition T(x)=x+W(x)
- Motivation: A reverse pairing with more cancelling positions (s_i=0) than constructive collisions (|s_i|=2) should not grow canonical length. K is not fitted: the relation is the direct P0/P2 comparison with ΔL.
- Domain: one-step reverse-plus-add states with P0(x) > P2(x)
- Expected yield: an exact cancellation-versus-construction law for length change
- Cheapest falsifier: the first frozen seed with P0>P2 whose canonical length grows
- Checked: 19

## Candidate 2: `pair_sign_imbalance_matches_successor_sign` (failed)

- Statement: If P+(x) != P-(x) then sign(T(x)) = sign(P+(x)-P-(x)) for the one-step addition T(x)=x+W(x)
- Motivation: Reversal preserves the trit multiset, so any sign of T must come from aligned constructive versus destructive pair sums, not from the digit inventory of x alone.
- Domain: one-step reverse-plus-add states with P+ != P-
- Expected yield: an exact pair-majority rule for sign(T)
- Cheapest falsifier: the first frozen seed whose pair-sign majority disagrees with sign(T)
- Checked: 32

- Counterexample: `-672 -> -448` (P0=0, P2=1, P+=4, P-=3, R=6, length 7->7)
- Failure class: `SIGN_IMBALANCE_MISMATCH`
- Mechanism: Pair-sign majority disagrees with sign(T): P+=4, P-=3, sign(T(-672))=-1 for -672->-448. Equal-weight pair counts ignore place value 3^i.

## Candidate 3: `length_growth_requires_top_pair` (survived)

- Statement: bt_length(T(x)) - bt_length(x) >= 1 implies s_{n-1} != 0, where n is the LSD-aligned pair length and s_{n-1} is the highest aligned pair sum
- Motivation: If where the interaction occurs matters more than how often, length growth should require a nonzero pair at the MSD-aligned position rather than a count of |s_i|=2 anywhere.
- Domain: one-step reverse-plus-add states with ΔL >= 1
- Expected yield: an exact positional obstruction for length growth
- Cheapest falsifier: the first frozen seed whose length grows while the highest pair is 0
- Checked: 17

## Special probes

- `positive palindrome`: x=1 -> T=2, W=1, s=[2], P0=0, P2=1, P+=1, P-=0, R=0, length 1->2
- `reverse-as-negation`: x=2 -> T=0, W=-2, s=[0, 0], P0=2, P2=0, P+=0, P-=0, R=-1, length 2->1
- `sign-changing successor`: x=5 -> T=-6, W=-11, s=[0, -2, 0], P0=2, P2=1, P+=0, P-=1, R=1, length 3->3
- `successor 0`: x=8 -> T=0, W=-8, s=[0, 0, 0], P0=3, P2=0, P+=0, P-=0, R=-1, length 3->1
- `packet seed`: x=196 -> T=392, W=196, s=[2, -2, 2, 2, -2, 2], P0=0, P2=6, P+=4, P-=2, R=5, length 6->7

## Transition window

- Frozen discovery window: range(1, 41)
- Packet orbit seed: 196
- One-step samples: 49

## Decision

**REVERSE_PAIR_NEEDS_RICHER_STRUCTURE**

pairwise reverse interaction is visible but no simple count or top-position aggregate determines the successor.

Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_BLOCKED`.
Not a halt theorem. Not a production attack.

## Best next question

If simple pair counts and the top aligned position do not determine T, what exact remaining interaction of `x` and `W(x)` is still not a digit-language engine?
