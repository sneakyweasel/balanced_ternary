# Juggler odd-odd composition Phase-10 falsifier

Status: **PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER**

This is not a termination attack, not a ranking synthesizer, and not a
generalization of `odd_even_two_step_decrease`. Depth is frozen at `k=2`.
It asks what exact two-step law, if any, replaces descent on the odd→odd
floor-power cylinder.

## Branch budget

```text
Mathematical target     On D_OO, does T^2 satisfy a simple exact k=2 law
                        that is not definitional floor-power restatement?
Novelty hypothesis      The complementary cylinder has a dual growth law
                        to the proved odd-even descent.
Falsifier               An exact two-step sample violating each frozen
                        candidate, or a definitional restatement billed as loot.
Existing machinery      FloorPowerSpec, WINDOW+orbit 13, FloorPower.lean.
Maximum Phase-10 scope  Three pre-ranked k=2 candidates on frozen D_OO.
Promotion criterion     Exact non-definitional branch law with Lean path.
Stop criterion          k>2, ranking, census growth, generic engine,
                        termination/divergence claim.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_10_JUGGLER_ODD_ODD_COMPOSITION_FALSIFIER`
- target: `juggler_sequence`
- attack: `odd_odd_branch_composition`
- composition depth: `2`
- classification: **JUGGLER_ODD_ODD_GREEN_LOOT**
- lean: `PROVED`
- green loot: `JUGGLER_ODD_ODD_GREEN_LOOT`
- global consequence: `LOCAL_BRANCH_LAW`
- decision reason: thresholded T^2 > n on D_OO, n>=3 is the dual of odd-even descent; strict growth fails at the fixed point 1; T^2 is not odd-cylinder invariant

Candidate list frozen at three. `odd_even_two_step_decrease` is unchanged.
`DEFAULT_ATTACK_ORDER` is unchanged. No production odd-odd attack.

## Domains

- `D_OE = {odd x : T(x) even and T^2(x) defined}`
- `D_OO = {odd x : T(x) odd and T^2(x) defined}`
- Positive control: `floorPower_odd_even_two_step_lt`
- Odd-even theorem unchanged: `True`

## Anti-tautology

- Rejected identities: ['T(x)=floor(x^(3/2)) for odd x', 'T^2(x)=floor(floor(x^(3/2))^(3/2)) when T(x) is odd', 'the successor is odd']
- Scope: `LOCAL_BRANCH_LAW`
- Not investigated: `k>2`
- T^2(n)>n on D_OO, n>=3 uses the second-step odd parity to select the expanding formula, then the comparison (n+1)^2 <= n^3. It is not T=floor(n^(3/2)) written twice. T(n)>n for odd n>=3 holds on D_OE as well, but T^2>n does not: the even second step contracts.

## Candidate 1: `strict_two_step_growth` (failed)

- Statement: T^2(x) > x on D_OO
- Domain: D_OO = {odd x : T(x) odd and T^2(x) defined}
- Motivation: The odd branch is expanding. The smallest dual of the proved odd-even descent is strict two-step growth on the complementary cylinder.
- Expected yield: exact two-step growth law, or a threshold/equality obstruction
- Cheapest falsifier: the first frozen D_OO seed with T^2(x) <= x
- Arithmetic class: `BRANCH_SPECIFIC`
- Checked: 1

- Counterexample: `1 -> 1 -> 1`
- Failure class: `THRESHOLD_FAILURE`
- Mechanism: Strict growth fails at 1->1->1: T^2(1)=1 is not > 1. Fixed point or threshold.

## Candidate 2: `thresholded_two_step_growth` (survived)

- Statement: For n in D_OO with n >= 3, T^2(n) > n. The threshold 3 is the exact comparison (n+1)^2 <= n^3, not a fitted constant.
- Domain: D_OO intersect {n >= 3}
- Motivation: For n>=3, isqrt(n^3) >= n+1. If T(n) is odd then T is nondecreasing on that image, so two odd steps grow. Dual of T^2 < n on D_OE.
- Expected yield: exact complementary inequality with a derived threshold
- Cheapest falsifier: the first frozen D_OO seed n>=3 with T^2(n) <= n
- Arithmetic class: `FLOOR_POWER_BRANCH_SPECIFIC`
- Checked: 8

- Assessed: `FLOOR_POWER_BRANCH_SPECIFIC`

## Candidate 3: `odd_cylinder_preservation` (failed)

- Statement: x in D_OO implies T^2(x) is odd
- Domain: D_OO = {odd x : T(x) odd and T^2(x) defined}
- Motivation: Parity is the floor-power branch bit. Two successive odd steps might remain in the odd cylinder. Modulus 2 is the branch mechanism, not a residue sweep.
- Expected yield: exact T^2 parity / cylinder-invariance law
- Cheapest falsifier: the first frozen D_OO seed whose T^2 is even
- Arithmetic class: `BRANCH_SPECIFIC`
- Checked: 3

- Counterexample: `5 -> 11 -> 36`
- Failure class: `PARITY_DOMAIN_LEAK`
- Mechanism: Odd-cylinder leaks at 5->11->36: T^2(5)=36 is even, so T^2 leaves D_OO.

## Existing samples

- Frozen D_OO two-step samples: 9
- Frozen D_OE control samples: 11
- Required probe: `3 -> 5 -> 11`
- `1 -> 1 -> 1` (T^2 odd=True)
- `3 -> 5 -> 11` (T^2 odd=True)
- `5 -> 11 -> 36` (T^2 odd=False)
- `9 -> 27 -> 140` (T^2 odd=False)
- `25 -> 125 -> 1397` (T^2 odd=True)
- `33 -> 189 -> 2598` (T^2 odd=False)
- `35 -> 207 -> 2978` (T^2 odd=False)
- `37 -> 225 -> 3375` (T^2 odd=True)
- `39 -> 243 -> 3787` (T^2 odd=True)

## Decision

**JUGGLER_ODD_ODD_GREEN_LOOT**

thresholded T^2 > n on D_OO, n>=3 is the dual of odd-even descent; strict growth fails at the fixed point 1; T^2 is not odd-cylinder invariant.

Green loot: `JUGGLER_ODD_ODD_GREEN_LOOT`. Lean: `PROVED`.
Scope: `LOCAL_BRANCH_LAW`. Not `GLOBAL_TERMINATION`.
Not a production attack. `odd_even_two_step_decrease` is unchanged.
Top-3 #1 is `odd_odd_symbolic_composition` (proposed, not registered).
`odd_odd_branch_composition` is not in `DEFAULT_ATTACK_ORDER`.

## Best next question

The odd-odd cylinder is not T^2-invariant (5->11->36). Does that leakage feed the existing odd-even lemma without raising composition depth?
