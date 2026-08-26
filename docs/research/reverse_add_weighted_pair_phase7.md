# Reverse-add weighted reverse-pair Phase-7 falsifier

Status: **PHASE_7_WEIGHTED_REVERSE_PAIR_FALSIFIER**

This is not a reverse-and-add solver, not a ranking synthesizer, and not a
digit-language engine. It tests whether a low-information positional
summary of raw pair sums predicts successor sign without reconstructing
`T(x)=sum_i s_i 3^i`.

## Branch budget

```text
Mathematical target     Does highest-significance reverse-pair position
                        determine sign(T) without the full weighted sum?
Novelty hypothesis      Positional dominance, not pair counts, is the
                        missing middle coordinate between counts and T.
Falsifier               An exact one-step sample violating each candidate,
                        or a survivor that reconstructs T.
Existing machinery      ReverseAddSpec, encode, bt_reverse, pair_sums_lsd,
                        WINDOW, seed-196 orbit, Phase-6 pair convention.
Maximum Phase-7 scope   k=1; three pre-ranked positional summaries;
                        frozen window+orbit.
Promotion criterion     Exact coarser-than-T sign law, Lean path.
Stop criterion          full-sum reconstruction, digit-language engine,
                        k>1, census growth, ranking.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_7_WEIGHTED_REVERSE_PAIR_FALSIFIER`
- target: `reverse_and_add_base3`
- composition depth: 1
- classification: **WEIGHTED_PAIR_PROMISING**
- lean: `FORMALIZATION_READY`
- green loot: `NO_NEW_LOOT`
- decision reason: the highest-nonzero-pair sign law survived; a coarser collision summary is not sufficient on its own

Candidate list frozen at three. reverse_gap is not reopened.
`DEFAULT_ATTACK_ORDER` is unchanged. No production weighted-pair attack.

## Pair convention

- Digit index: LSD-first: index i is the coefficient of 3^i
- Alignment: LSD-align encode(x) with encode(W(x)); pad the shorter word with 0 on the MSD side
- Pair sum: left_i + right_i, raw pair sum before rewrite_sum, in {-2,...,2}
- Identity: T(x)=sum_i s_i 3^i is definitional and is not a candidate

## Anti-tautology

- Definitional identity rejected as a candidate: `T(x)=sum_i s_i 3^i is not a candidate`
- Candidates reconstruct T: `False`
- Stored statistics coarser than the full sum: `True`

## Candidate 1: `highest_nonzero_pair_determines_sign` (survived)

- Statement: If some s_i != 0 and h=max{i:s_i!=0}, then sign(T(x))=sign(s_h). Equivalently s_h>0 implies T(x)>0 and s_h<0 implies T(x)<0
- Motivation: Phase-6 pair-sign majority failed because counts ignore 3^i. The minimal positional repair uses only the highest nonzero pair, not the full weighted sum.
- Domain: one-step reverse-plus-add states with at least one nonzero pair
- Expected yield: an exact sign(T) law from a single pair position
- Cheapest falsifier: the first frozen seed whose highest nonzero pair has the opposite sign of T
- Checked: 42

## Candidate 2: `highest_positive_vs_highest_negative` (survived)

- Statement: If m+=max{i:s_i>0} and m-=max{i:s_i<0} are compared, then m+>m- implies T(x)>0 and m->m+ implies T(x)<0; a missing side is treated as strictly dominated
- Motivation: The Phase-6 count comparison P+>P- failed. The natural repair compares the most significant positive position with the most significant negative position, still without the full sum.
- Domain: one-step reverse-plus-add states with at least one nonzero pair
- Expected yield: an exact mixed-sign positional dominance law for sign(T)
- Cheapest falsifier: the first frozen seed whose higher signed position disagrees with sign(T)
- Checked: 42

## Candidate 3: `highest_mag2_determines_sign` (failed)

- Statement: If h2=max{i:|s_i|=2} is defined, then sign(T(x))=sign(s_{h2}), even when a higher |s|=1 pair exists
- Motivation: Phase 5 showed internal |s|=2 activity without length change. This tests whether the highest constructive/destructive collision captures sign, or whether a higher |s|=1 pair can dominate it.
- Domain: one-step reverse-plus-add states with some |s_i|=2
- Expected yield: an exact collision-position law for sign(T)
- Cheapest falsifier: the first frozen seed whose highest |s|=2 pair has the opposite sign of T
- Checked: 4

- Counterexample: `6 -> 4` (h=2, sign_h=1, m+=2, m-=1, h2=1, sign_h2=-1)
- Failure class: `MULTI_POSITION_INTERFERENCE`
- Mechanism: Highest |s|=2 pair does not determine sign: h2=1, sign(s_h2)=-1, h=2, sign(s_h)=1, 6->4.

## Special probes

- `positive palindrome`: x=1 -> T=2, s=[2], h=0, sign_h=1, m+=0, m-=None, h2=0, sign_h2=1
- `reverse-as-negation`: x=2 -> T=0, s=[0, 0], h=None, sign_h=None, m+=None, m-=None, h2=None, sign_h2=None
- `sign-changing successor`: x=5 -> T=-6, s=[0, -2, 0], h=1, sign_h=-1, m+=None, m-=1, h2=1, sign_h2=-1
- `successor 0`: x=8 -> T=0, s=[0, 0, 0], h=None, sign_h=None, m+=None, m-=None, h2=None, sign_h2=None
- `packet seed`: x=196 -> T=392, s=[2, -2, 2, 2, -2, 2], h=5, sign_h=1, m+=5, m-=4, h2=5, sign_h2=1
- `phase-6 pair-count counterexample`: x=-672 -> T=-448, s=[-1, 1, 1, -2, 1, 1, -1], h=6, sign_h=-1, m+=5, m-=6, h2=3, sign_h2=-1

## Secondary length observation

length was not a primary candidate. On the frozen sample, 17 one-step states have ΔL>=1; positional sign laws do not claim a length identity.

## Transition window

- Frozen discovery window: range(1, 41)
- Packet orbit seed: 196
- One-step samples: 49

## Decision

**WEIGHTED_PAIR_PROMISING**

the highest-nonzero-pair sign law survived; a coarser collision summary is not sufficient on its own.

Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_READY`.
Not a halt theorem. Not a production attack.

## Best next question

If highest-pair sign is an exact but general place-value fact, does reverse-and-add still need a target-specific nonlinear identity, or is the remaining gap only formalization of that bound?
