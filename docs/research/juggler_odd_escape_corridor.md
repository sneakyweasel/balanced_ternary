# Juggler odd-escape two-sided corridor

Status: **ODD_ESCAPE_CORRIDOR_CLOSED**

Event-triggered `PowerCorridor` on named AboveAnchor residuals.
Not a halt theorem. Not a pivot-corridor reopen.

## Branch budget

```text
Mathematical target     proved L>1 plus EnvelopeState U
                        constrains leftover odd escape
Novelty hypothesis      Gamma = U-L is new leverage
Maximum Phase-0 scope   named starts; no Lean; no Sigma
```

## Metadata

- classification: **ODD_ESCAPE_CORRIDOR_CLOSED**
- new odd lowers: `[]`
- new even lowers: `[]`
- realized collisions: `0`
- novel even-reset: `0`
- all odd nontrivial named: `True`

odd L>1 is CubeOddLanding / cube_odd_lift / cube_lift_odd_ge_fourth; even L>1 is even_ge_sq or even-run; collisions do not occur on realized prefixes; even-reset U<2L is the existing cube-even cell.

## First L>1 event

- `37`: i=`2` x=`3375` event=`cube_odd` [2,3) Gamma=`1`
- `69`: i=`2` x=`13716` event=`cube_even` [2,3) Gamma=`1`
- `89`: i=`2` x=`24302` event=`cube_even` [2,3) Gamma=`1`
- `365`: i=`2` x=`582276` event=`cube_even` [2,3) Gamma=`1`
- `501`: i=`2` x=`1187360` event=`cube_even` [2,3) Gamma=`1`
- `1517`: i=`2` x=`14362030` event=`cube_even` [2,3) Gamma=`1`
- `6187`: i=`2` x=`339491658` event=`cube_even` [2,3) Gamma=`1`

## 37 chain

- x=`3375` i=`2` event=`cube_odd` [2,3) Gamma=`1` U_rat=`9/4`
- x=`196069` i=`3` event=`cube_lift` [3,4) Gamma=`1` U_rat=`27/8`
- x=`86818724` i=`4` event=`cube_oo` [4,6) Gamma=`2` U_rat=`81/16`
- x=`9317` i=`5` event=`cube_odd` [2,3) Gamma=`1` U_rat=`81/32`
- 3375→9317 x_grew=`True` gamma_shrunk=`False` gamma_held=`True` [2, 3]→[2, 3]

## Type recurrence with growing x

- n=`37` [2,3) O count=`3` x=`2233`..`9317`
- n=`37` [3,4) O count=`3` x=`105519`..`899319`
- n=`69` [2,3) E count=`2` x=`13716`..`44992`
- n=`89` [2,3) E count=`2` x=`24302`..`84722`
- n=`365` [2,3) E count=`4` x=`582276`..`19782308`
- n=`501` [2,3) E count=`5` x=`582916`..`19782308`
- n=`501` [2,3) O count=`3` x=`296551`..`48693935`
- n=`501` [3,4) E count=`2` x=`161491284`..`17781526790`
- n=`1517` [2,3) E count=`4` x=`6217088`..`1143235850`
- n=`6187` [2,3) E count=`2` x=`125201440`..`339491658`
- n=`6187` [2,3) O count=`2` x=`3955183437`..`62634329559`

## x grew and Gamma shrunk

- none on consecutive L>1 states

## Existing Lean (unchanged)

- `EnvelopeState`: `True`
- `PowerCorridor`: `True`
- `envelope_corridor_contradiction`: `True`
- `even_below_anchor_pow`: `True`
- `AboveAnchor`: `True`
- `even_ge_sq_of_aboveAnchor`: `True`
- `aboveAnchor_even_run_ge_pow`: `True`
- `CubeOddLanding`: `True`
- `cube_odd_lift`: `True`
- `cube_lift_odd_ge_fourth`: `True`
- `FiniteProgress`: `True`
- new Lean file: `False`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`
- independent_corridor_gap: `False`
- new_odd_lower: `False`
- sigma_automaton: `False`
- scale_reopen: `False`
- pivot_corridor_reopen: `False`
- corridor_lean: `False`

## Decision

**ODD_ESCAPE_CORRIDOR_CLOSED**

odd L>1 is CubeOddLanding / cube_odd_lift / cube_lift_odd_ge_fourth; even L>1 is even_ge_sq or even-run; collisions do not occur on realized prefixes; even-reset U<2L is the existing cube-even cell.

