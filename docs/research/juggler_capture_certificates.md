# Juggler descent and capture certificates

Status: **DESCENT_CAPTURE_FRAMEWORK_GREEN**

Standalone application phase. Not a Research Engine experiment and
not a termination theorem. A realized finite block may descend or
land in the certified basin `{1}`.

## Branch budget

```text
Mathematical target     Capture into {1} plus descent, with composition
Novelty hypothesis      Changing-family collapses are basin captures
Falsifier               Large changing-family T not in {1} and no descent
Existing machinery      image_append, even_tower_to_one, nested 2500
Maximum Phase-0 scope   Capture/Descent props; append; normalize families
```

## Metadata

- basin: `[1]`
- engine control layer modified: `False`
- classification: **DESCENT_CAPTURE_FRAMEWORK_GREEN**
- sorry-free: `True`

large changing-family witnesses capture into {1}; short EOO at 12 and 14 are descent, not capture; capture composes and a minimal non-1 value admits neither certificate.

## Known blocks

- n=`2` word=`E` T=`1` kind=`CAPTURE`
- n=`2` word=`EOO` T=`1` kind=`CAPTURE`
- n=`12` word=`EOO` T=`11` kind=`DESCENT`
- n=`14` word=`EOO` T=`11` kind=`DESCENT`
- n=`4` word=`EEOOOO` T=`1` kind=`CAPTURE`
- n=`3` word=`OO` T=`11` kind=`NO_CERTIFICATE`
- n=`7` word=`OEEEOOOOOOOOO` T=`1` kind=`CAPTURE`
- n=`2500` word=`EEOEEEOOOOOOOOOOOO` T=`1` kind=`CAPTURE`
- n=`4` word=`EEOOOOOO` T=`1` kind=`CAPTURE`
- n=`16` word=`EEEOOOOOOOOO` T=`1` kind=`CAPTURE`
- n=`256` word=`EEEEOOOOOOOOOOOO` T=`1` kind=`CAPTURE`

## Capture composition

- `16` via `EEE` then `OOOOOOOOO`: mid=`1` concat=`CAPTURE`

## Small states

- s=`1` inert=`True` reaches_one=`True` path=`[1, 1, 1, 1, 1, 1, 1]`
- s=`2` inert=`False` reaches_one=`True` path=`[2, 1, 1, 1, 1, 1, 1]`
- s=`3` inert=`False` reaches_one=`True` path=`[3, 5, 11, 36, 6, 2, 1]`
- s=`4` inert=`False` reaches_one=`True` path=`[4, 2, 1, 1, 1, 1, 1]`
- s=`5` inert=`False` reaches_one=`True` path=`[5, 11, 36, 6, 2, 1, 1]`
- s=`6` inert=`False` reaches_one=`True` path=`[6, 2, 1, 1, 1, 1, 1]`
- s=`7` inert=`False` reaches_one=`True` path=`[7, 18, 4, 2, 1, 1, 1]`
- s=`8` inert=`False` reaches_one=`True` path=`[8, 2, 1, 1, 1, 1, 1]`

## Lean

- `InertBasin`: `True`
- `Capture`: `True`
- `Descent`: `True`
- `ReachesOne`: `True`
- `capture_of_suffix`: `True`
- `capture_append`: `True`
- `even_tower_capture`: `True`
- `even_tower_odd_tail_capture`: `True`
- `odd_even_tower_seven_capture`: `True`
- `nested_even_collapse_2500_capture`: `True`
- `first_even_cell_capture`: `True`
- `capture_reachesOne`: `True`
- `descent_of_below`: `True`
- `minimal_avoids_progress`: `True`
- `power_bound_compensated_contracts`: `True`
- `first_even_freeze`: `True`
- certificate unchanged: `True`
- `PowerHeight` absent: `True`
- no global halt theorem: `True`

## Anti-overclaim

- global_termination: `False`
- global_divergence: `False`
- every_trajectory_contains_word: `False`
- parity_frequency_theorem: `False`
- finite_macro_transition_grammar: `False`
- average_formal_energy_decreases: `False`
- floating_point_verdict: `False`

## Decision

**DESCENT_CAPTURE_FRAMEWORK_GREEN**

large changing-family witnesses capture into {1}; short EOO at 12 and 14 are descent, not capture; capture composes and a minimal non-1 value admits neither certificate.

This is not a halt result.

