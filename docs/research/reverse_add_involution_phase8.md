# Reverse-add involution-interaction Phase-8 falsifier

Status: **PHASE_8_REVERSE_INVOLUTION_FALSIFIER**

This is not a reverse-and-add solver, not a ranking synthesizer, and not a
digit-language engine. It tests whether the reversal involution produces a
compressed exact relation among `x`, `W(x)`, `T(x)=x+W(x)`, and `W(T(x))`
that is not generic balanced-ternary arithmetic.

## Branch budget

```text
Mathematical target     Does W(W(x))=x create a non-generic exact law
                        among x, W(x), T(x), W(T(x))?
Novelty hypothesis      The useful reverse-and-add structure is the
                        involution interaction, not a scalar summary.
Falsifier               An exact one-step sample violating each candidate,
                        a tautology, or a generic arithmetic restatement.
Existing machinery      ReverseAddSpec, encode, bt_reverse, bt_length,
                        reverse_gap L1, WINDOW, seed-196 orbit.
Maximum Phase-8 scope   k=1; four objects; three pre-ranked candidates;
                        frozen window+orbit.
Promotion criterion     Reverse-specific non-tautological law, Lean path.
Stop criterion          word algebra, T^2 attack, ranking, census growth,
                        digit-language engine.
```

## Metadata

- engine_control_version: `0.2.7`
- source_engine: `v2.3`
- experimental_status: `PHASE_8_REVERSE_INVOLUTION_FALSIFIER`
- target: `reverse_and_add_base3`
- composition depth: 1
- classification: **REVERSE_INVOLUTION_REFUTED**
- lean: `FORMALIZATION_BLOCKED`
- green loot: `NO_NEW_LOOT`
- decision reason: the only survivors are generic arithmetic, not reverse-involution loot

Candidate list frozen at three. reverse_gap is not reopened as ranking.
`DEFAULT_ATTACK_ORDER` is unchanged. No production involution attack.
`W(W(x))=x` is not loot. Canonical reverse is involutive iff `x=0` or `3` does not divide `x`.

## Anti-tautology

- Rejected identities: ['W(W(x))=x', 'T(x)=x+W(x)', 'W(T(x))=bt_reverse(encode(T(x)))']
- Objects: ['x', 'W(x)', 'T(x)', 'W(T(x))']
- Not investigated: `T^2(x)`

## Candidate 1: `reverse_sum_residual_bound` (failed)

- Statement: |W(T(x)) - W(x)| <= |T(x) - x|, equivalently |R(x)| <= |W(x)| with R(x)=W(T(x))-W(x)
- Domain: one-step reverse-plus-add states
- Motivation: Reversing the newly formed sum should not create a residual larger than the original reverse contribution that produced T.
- Expected yield: an exact residual bound relating W(T) to W(x)
- Cheapest falsifier: the first frozen seed with |W(T)-W(x)| > |W(x)|
- Reverse-specificity (declared): `REVERSE_SPECIFIC`
- Checked: 1

- Counterexample: `1 -> 2` (W=1, W(T)=-2, R=-3, gap 0->4, WW=1, involutive=True)
- Failure class: `INVOLUTION_RESIDUAL_MISMATCH`
- Mechanism: Reverse-sum residual exceeds the original reverse: R(1)=-3, |W(1)|=1, W(T)=-2.

## Candidate 2: `successor_reverse_gap_length_bound` (failed)

- Statement: reverse_gap(T(x)) <= reverse_gap(x) + bt_length(x), where reverse_gap is the L1 MSD-word discrepancy, not a ranking
- Domain: one-step reverse-plus-add states
- Motivation: Phase-1 reverse_gap ranking failed. The question here is only whether the successor's reversal defect is controlled by the original defect plus word length, the natural size of one word.
- Expected yield: an exact successor-gap relation without reopening ranking
- Cheapest falsifier: the first frozen seed whose successor gap exceeds gap(x)+bt_length(x)
- Reverse-specificity (declared): `REVERSE_SPECIFIC`
- Checked: 1

- Counterexample: `1 -> 2` (W=1, W(T)=-2, R=-3, gap 0->4, WW=1, involutive=True)
- Failure class: `SUCCESSOR_REVERSAL_UNCONTROLLED`
- Mechanism: Successor reverse_gap is uncontrolled: gap(T(1))=4 > gap(1)+L=0+1.

## Candidate 3: `successor_msd_from_operand_pair` (survived)

- Statement: If T(x)!=0 then the MSD trit of T(x) lies in {MSD(x), MSD(W(x)), -MSD(x), -MSD(W(x))}
- Domain: one-step reverse-plus-add states with T(x)!=0
- Motivation: The summands are an involution pair, so the leading trit of the normalized sum should be inherited from one operand or its negative, not from a generic unrelated digit.
- Expected yield: an exact leading-trit constraint caused by the operand pairing
- Cheapest falsifier: the first frozen nonzero successor whose MSD is outside the operand MSD set
- Reverse-specificity (declared): `GENERIC_ARITHMETIC_RISK`
- Checked: 42

## Reverse-specificity check

- `reverse_sum_residual_bound`: survived=False, assessed=`N/A` — failed before reverse-specificity loot could be claimed
- `successor_reverse_gap_length_bound`: survived=False, assessed=`N/A` — failed before reverse-specificity loot could be claimed
- `successor_msd_from_operand_pair`: survived=True, assessed=`GENERAL_ARITHMETIC` — generic leading-digit inheritance of a sum

## Special probes

- `positive palindrome`: x=1 -> T=2, W=1, W(T)=-2, WW=1, involutive=True, R=-3, gap 0->4
- `reverse-as-negation`: x=2 -> T=0, W=-2, W(T)=0, WW=2, involutive=True, R=2, gap 4->0
- `sign-changing successor`: x=5 -> T=-6, W=-11, W(T)=2, WW=5, involutive=True, R=13, gap 4->2
- `phase-7 collision counterexample`: x=6 -> T=4, W=-2, W(T)=4, WW=2, involutive=False, R=6, gap 2->0
- `successor 0`: x=8 -> T=0, W=-8, W(T)=0, WW=8, involutive=True, R=8, gap 4->0
- `packet seed`: x=196 -> T=392, W=196, W(T)=-1064, WW=196, involutive=True, R=-1260, gap 0->4
- `phase-6 pair-count counterexample`: x=-672 -> T=-448, W=224, W(T)=-376, WW=-224, involutive=False, R=-600, gap 6->2

## Transition window

- Frozen discovery window: range(1, 41)
- Packet orbit seed: 196
- One-step samples: 49

## Decision

**REVERSE_INVOLUTION_REFUTED**

the only survivors are generic arithmetic, not reverse-involution loot.

Green loot: `NO_NEW_LOOT`. Lean: `FORMALIZATION_BLOCKED`.
Not a halt theorem. Not a production attack.
Top-3 #1 remains `symbolic_nonlinear_composition`.
`reverse_involution_not_sufficient_at_this_level`.
`reverse_involution_structure` is not registered.

## Best next question

If compressed involution summaries fail, should reverse-and-add return to the existing symbolic-nonlinear frontier without a digit-language engine?
